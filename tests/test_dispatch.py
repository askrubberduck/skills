#!/usr/bin/env python3
"""dispatch.py end to end: fake `codex`, `agy` and `claude` on PATH, a fixture home, every exit path.
Run: python3 tests/test_dispatch.py"""

from __future__ import annotations

import contextlib
import os
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ inside the shipped skill
SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "duck-review" / "scripts"
DISPATCH = SCRIPTS / "dispatch.py"
sys.path.insert(0, str(SCRIPTS))
from dispatch import classify
from ledger import DISPATCH_COLUMNS, DISPATCH_ENUMS, read_table  # noqa: E402

CONFIG_FIXTURE = """\
[bounds]
review_rounds = 3
trust_rounds = 2
dispatch_timeout = "5s"
[repo."r"]
dispatch_timeout = "20s"
"""
STUBS = {
    # codex echoes the prompt after `user`; only the text after its answer marker is the answer
    "reject": 'printf \'%s\\0\' "$@" > "$0.argv"; pwd -P > "$0.cwd"; cut -f1,16 "$ASKRUBBERDUCK_HOME/dispatches.tsv"'
              ' > "$0.seen"\n[ "$1" != codex ] || printf \'user\\nAPPROVE\\ncodex\\n\' >&2\n'
              'printf \'**VERDICT: REJECT**\\n\'\n[ "$1" != codex ] || printf \'tokens used\\n1,234\\n\' >&2',
    "severity": "printf 'VERDICT: APPROVE\\n\\nNOTE\\nCoverage limit\\n'",
    "bare-severity": "printf 'VERDICT: APPROVE\\n\\nNOTE\\nCoverage limit\\n'",
    "plan-severity": "printf 'PLAN: OBJECT\\n\\nNOTE\\nCoverage limit\\n'",
    "terminal-diff": "printf '## NOTE\\nNonblocking observation\\nVERDICT: DIFF\\n'",
    "earlier-severity": "printf 'NOTE\\nCoverage limit\\n**VERDICT: REJECT**\\n'",
    "greeting": "printf 'user\\nVERDICT: REJECT\\ncodex\\nHello! How can I help?\\n'",
    "credits": "echo \"ERROR: You're out of credits. Add credits to continue.\"; exit 1",
    "sleep": 'sleep 30 & echo $! > "$0.pid"; wait',
    "touch": 'touch "$CANDIDATE/new.txt"; echo "VERDICT: APPROVE"',
    "slow": "sleep 0.5; echo 'VERDICT: NOTE'",
    "stdin": "cat > /dev/null; echo 'VERDICT: APPROVE'",
    "diff": "echo 'VERDICT: DIFF'",
    "crash": "echo 'VERDICT: APPROVE'; exit 7",
    "append": 'echo more >> "$CANDIDATE/new.txt"; echo "VERDICT: APPROVE"',
    "hang": "echo 'VERDICT: APPROVE'; sleep 30",
    "denied": "echo 'Error: a tool required the \"write_file\" permission that headless mode'"
              " 'cannot prompt for, so it was auto-denied'",
    "wrapped": "printf 'Error: a tool required the permission that headless mode\\n"
               "cannot prompt for, so it was auto-denied\\n'",
    "race": "echo raced > raced.txt; printf '\\0\\1' > raced.bin; echo 'VERDICT: DIFF'",
    "cancel": 'sleep 30 & echo $! > "$0.pid"; touch "$0.up"; wait',
    "env": 'ls -A "$CODEX_HOME" > "$0.ls"; printf %s "$CODEX_HOME" > "$0.codex"; '
           'printf %s "$HOME" > "$0.HOME"; readlink "$CODEX_HOME/auth.json" > "$0.auth"; '
           'echo "VERDICT: APPROVE"',
}


def self_check() -> int:
    for answer in ("> VERDICT: APPROVE\nREJECT", "NOTE\nREJECT",
                   "VERDICT: APPROVE\nVERDICT: REJECT", "VERDICT: NOTE\nVERDICT: DIFF",
                   "VERDICT: NOTE\nDIFF", "VERDICT: APPROVE\nREJECT",
                   "```\nVERDICT: APPROVE\n```", "APPROVE\nNOTE",
                   "````markdown\n```text\nVERDICT: APPROVE\n```\n````",
                   "    VERDICT: APPROVE", "\tVERDICT: APPROVE",
                   "> The reviewer returned:\nVERDICT: APPROVE",
                   "```text\n``` example continues\nVERDICT: APPROVE\n```"):
        assert classify(answer, "claude", False, 0)[0] == "-", answer
    assert classify("> VERDICT: APPROVE\n\nVERDICT: REJECT", "claude", False, 0) == ("REJECT", "")
    assert classify("```\nVERDICT: APPROVE\n```\nVERDICT: REJECT", "claude", False, 0) == ("REJECT", "")
    for answer in ("```text\nexample\nVERDICT: APPROVE",
                   "> example\ncontinued quotation\nVERDICT: APPROVE"):
        assert classify(answer, "claude", False, 0)[0] == "-", answer
    # the body is never parsed: a quote ended by a heading, then a second result, is ambiguous
    assert classify("VERDICT: APPROVE\n\n> Prior rationale was incomplete.\n## Final judgment\n"
                    "VERDICT: REJECT", "claude", False, 0) == ("-", "ambiguous verdict")
    assert classify("## VERDICT: REJECT\n\n## BLOCKER\nNOTE\n> VERDICT: APPROVE\nfindings",
                    "agy", False, 0) == ("REJECT", "")
    for label in ("**VERDICT:** APPROVE", "**VERDICT**: APPROVE", "VERDICT: ** APPROVE **"):
        assert classify(label, "claude", False, 0) == ("APPROVE", ""), label
    assert classify("**PLAN:** CONCUR", "claude", False, 0) == ("CONCUR", "")
    assert classify("VERDICT: APPROVE\n\nNOTE", "claude", False, 0) == ("APPROVE", "")
    # a final result hidden by quote or fence state is a conflict, never silently dropped
    for tail in ("> Prior rationale.\n- Final judgment\nVERDICT: REJECT",
                 "> Prior rationale.\nVERDICT: REJECT", "```\nVERDICT: REJECT",
                 "> q\n---\nVERDICT: REJECT", "> q\n| a | b |\nVERDICT: REJECT"):
        assert classify("VERDICT: APPROVE\n\n" + tail, "claude", False, 0) == (
            "-", "ambiguous verdict"), tail
    # a real codex exec log echoes the prompt and repeats the answer: never parsed for a result
    real = "user\nReply with VERDICT: NOTE\ncodex\nVERDICT: NOTE\ndone\ntokens used\n8,187\nVERDICT: NOTE\ndone\n"
    assert classify("VERDICT: NOTE\ndone\n", "codex", False, 0, real) == ("NOTE", "")
    assert classify("", "codex", False, 0, real)[0] == "-"
    with tempfile.TemporaryDirectory(prefix="askrubberduck-dispatch-") as directory:
        root = Path(directory).resolve()  # macOS: /var is /private/var
        os.environ["ASKRUBBERDUCK_HOME"] = str(root)
        (root / "config.toml").write_text(CONFIG_FIXTURE)
        prompt = root / "prompt.md"
        prompt.write_text("Review /abs/diff. End with VERDICT: APPROVE | REJECT | NOTE")
        checkout = root / "candidate"
        git = ["git", "-C", str(checkout), "-c", "user.name=t", "-c", "user.email=t@t",
               "-c", "commit.gpgsign=false"]
        subprocess.run(["git", "init", "-q", str(checkout)], check=True)
        subprocess.run([*git, "commit", "-q", "--allow-empty", "--no-verify", "-m", "c"], check=True)
        for name, body in STUBS.items():
            stub = root / name
            stub.write_text(f"#!/bin/sh\n{body}\n")
            stub.chmod(0o755)
            # Each CLI on the seat's PATH runs the stub with its own name as the first argument
            (root / "bin" / name).mkdir(parents=True)
            for cli in ("codex", "agy", "claude"):
                fake = root / "bin" / name / cli
                if cli == "codex":  # like codex exec, the last message also lands in its file
                    fake.write_text(f'#!/bin/sh\n[ "$2" = --output-last-message ] || exit 91\n'
                                    f'{shlex.quote(str(stub))} codex "$@" > "$3"; s=$?; cat "$3"; exit $s\n')
                else:
                    fake.write_text(f'#!/bin/sh\nexec {shlex.quote(str(stub))} "${{0##*/}}" "$@"\n')
                fake.chmod(0o755)
        env = {**os.environ, "CANDIDATE": str(checkout)}
        outs = iter(range(100))  # parallel seats of one gate must not share an output file

        def seat(stub: str, gate: str, *extra: str, rnd: int = 1, repo: str = "r",
                 stdin=subprocess.DEVNULL, **more_env: str) -> subprocess.Popen:
            argv = [sys.executable, str(DISPATCH), "--gate", gate, "--round", str(rnd), "--stage",
                    "review", "--setup", "independent", "--trust", "0", "--pin",
                    "openai:gpt-6-sol:high", "--prompt", str(prompt), "--out",
                    str(root / "scratch" / f"{gate}-{next(outs)}.out"), "--repo", repo,
                    *extra]
            return subprocess.Popen(argv, stdin=stdin, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True, cwd=root,
                                    env={**env, "PATH": f"{root / 'bin' / stub}:{os.environ['PATH']}",
                                         **more_env})

        def run(*args, **kwargs) -> tuple[int, str]:
            child = seat(*args, **kwargs)
            out = child.communicate(timeout=60)[0]
            return child.returncode, out

        def rows() -> dict[str, dict]:
            return {d["id"]: d for d in read_table("dispatches.tsv", DISPATCH_COLUMNS,
                                                   DISPATCH_ENUMS)}

        def final(row_id: str) -> tuple[str, str, str]:
            row = rows()[row_id]
            return row["verdict"], row["status"], row["outage"]

        # 1. the verdict comes from codex's last-message file, not the log's echoed APPROVE; round 2
        # of trust work sits on its bound of 2 and runs; the row was pending while the seat ran
        code, out = run("reject", "g1", "--trust", "1", rnd=2)
        assert code == 0 and final("g1-r2-review-gpt-6-sol") == ("REJECT", "final", "0"), out
        assert rows()["g1-r2-review-gpt-6-sol"]["tokens"] == "1234", rows()
        assert "g1-r2-review-gpt-6-sol\tpending" in (root / "reject.seen").read_text()
        argv = (root / "reject.argv").read_text().split("\0")[:-1]
        assert argv[2] == "--output-last-message" and argv[3].endswith(".answer"), argv
        assert argv[:2] + argv[4:] == [
            "codex", "exec", "-m", "gpt-6-sol", "-c", "model_reasoning_effort=high", "-s",
            "workspace-write", "-C", str(root / "scratch"), "--skip-git-repo-check",
            prompt.read_text()]
        assert (root / "reject.cwd").read_text().strip() == str(root / "scratch")
        code, out = run("reject", "g1", "--pin", "google:gemini-3.1-pro-high", "--add-dir",
                        str(checkout))
        assert code == 0, out
        assert final("g1-r1-review-gemini-3.1-pro-high") == ("REJECT", "final", "0"), out
        assert (root / "reject.argv").read_text().split("\0")[:-1] == [
            "agy", "--model", "gemini-3.1-pro-high", "--dangerously-skip-permissions", "--sandbox",
            "--add-dir", str(checkout),
            "--print-timeout", "20s", "-p", prompt.read_text()]
        code, out = run("reject", "g1c", "--pin", "anthropic:claude-test:high", "--add-dir",
                        str(checkout))
        assert code == 0 and final("g1c-r1-review-claude-test") == ("REJECT", "final", "0"), out
        assert (root / "reject.argv").read_text().split("\0")[:-1] == [
            "claude", "-p", "--model", "claude-test", "--effort", "high", "--permission-mode",
            "plan", "--permission-prompts", "none", "--setting-sources", "project", "--safe-mode",
            "--no-session-persistence", "--tools", "Read,Glob,Grep",
            "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--add-dir", str(checkout),
            "--", prompt.read_text()]
        code, out = run("reject", "g1c", "--pin", "anthropic:claude-other")
        assert code == 0 and "--effort" not in (root / "reject.argv").read_text(), out
        # a second agy seat of the same gate and round takes its own default id
        code, out = run("reject", "g1", "--pin", "google:gemini-3.1-flash")
        assert code == 0 and final("g1-r1-review-gemini-3.1-flash") == ("REJECT", "final", "0"), out
        # --workdir moves the seat into a rival's worktree: codex -C and the cwd
        rival = root / "rival"
        rival.mkdir()
        code, out = run("reject", "g1w", "--workdir", str(rival))
        assert code == 0 and "-C\0" + str(rival) + "\0" in (root / "reject.argv").read_text(), out
        assert (root / "reject.cwd").read_text().strip() == str(rival)
        count = len(rows())  # agy auto-denies write_file headless: a rival needs codex
        code, out = run("reject", "g1w", "--workdir", str(rival), "--pin", "google:gemini-3.1-pro")
        assert code == 2 and "needs codex" in out and len(rows()) == count, out
        code, out = run("reject", "g1w", "--workdir", str(rival), "--pin", "anthropic:claude-test")
        assert code == 2 and "read-only" in out and len(rows()) == count, out
        code, out = run("reject", "g1w", "--workdir", "", "--id", "g1w-empty")
        assert code == 2 and "--workdir is empty" in out and len(rows()) == count, out
        # a codex seat gets its own CODEX_HOME with only the owner's login linked in, and as HOME
        # too unless it is a rival; the home is gone after the run
        owner = root / "owner-codex"
        owner.mkdir()
        (owner / "auth.json").write_text("{}")
        (owner / "AGENTS.md").write_text("private")
        code, out = run("env", "g1h", CODEX_HOME=str(owner))
        seat_home = (root / "env.codex").read_text()
        assert code == 0 and (root / "env.ls").read_text() == "auth.json\n", out
        assert (root / "env.HOME").read_text() == seat_home != str(owner), seat_home
        assert (root / "env.auth").read_text().strip() == str(owner / "auth.json")
        assert not Path(seat_home).exists(), "the seat's home outlived the run"
        code, out = run("env", "g1h", "--workdir", str(rival), "--id", "g1h-rival", CODEX_HOME=str(owner))
        assert code == 0 and (root / "env.HOME").read_text() == os.environ["HOME"], out
        (owner / "auth.json").unlink()  # an API-key login has no file to link
        code, out = run("env", "g1h", "--id", "g1h-key", CODEX_HOME=str(owner))
        assert code == 0 and (root / "env.ls").read_text() == "", out
        code, out = run("env", "g1h", "--pin", "google:gemini-3.1-pro", CODEX_HOME=str(owner))
        assert code == 0 and (root / "env.codex").read_text() == str(owner), out
        code, out = run("greeting", "g1b")  # the prompt's verdict is no answer
        assert code == 1 and final("g1b-r1-review-gpt-6-sol") == ("-", "final", "1"), out
        assert "no verdict" in out, out
        # a review and a disposition by one model in one round take their own default ids
        code, out = run("reject", "g1d", "--stage", "disposition")
        assert code == 0 and final("g1d-r1-disposition-gpt-6-sol")[1] == "final", out
        code, out = run("reject", "g1d")
        assert code == 0 and final("g1d-r1-review-gpt-6-sol")[1] == "final", out

        for stub, verdict in (("severity", "APPROVE"), ("bare-severity", "APPROVE"),
                              ("earlier-severity", "REJECT"), ("plan-severity", "OBJECT"),
                              ("terminal-diff", "DIFF")):
            code, out = run(stub, "verdict-"+stub)
            assert code == 0 and final("verdict-"+stub+"-r1-review-gpt-6-sol") == (
                verdict, "final", "0"), out

        # 2. the credits error is an outage with its cause
        code, out = run("credits", "g2")
        assert code == 1 and final("g2-r1-review-gpt-6-sol") == ("-", "final", "1"), out
        assert "outage: credits" in out, out
        code, out = run("denied", "g2", "--id", "g2-denied")  # agy headless auto-deny
        assert code == 1 and "outage: permission denied" in out, out
        code, out = run("wrapped", "g2", "--id", "g2-wrapped")  # the message wraps
        assert code == 1 and "outage: permission denied" in out, out

        # 3. past the 5s limit the whole group is killed, its grandchild included
        started = time.monotonic()
        code, out = run("sleep", "g3", repo="t")
        assert code == 1 and "outage: timeout" in out and time.monotonic() - started < 20, out
        assert final("g3-r1-review-gpt-6-sol") == ("-", "final", "1")
        with contextlib.suppress(ProcessLookupError):
            os.kill(int((root / "sleep.pid").read_text()), 0)
            raise AssertionError("the seat's child outlived the timeout")

        # 4. round 4 of trust work past trust_rounds = 2: refused with no row, run when extended
        count = len(rows())
        code, out = run("reject", "g4", "--trust", "1", rnd=4)
        assert code == 2 and "past the bound of 2" in out and len(rows()) == count, out
        code, out = run("reject", "g4", "--trust", "1", "--extended", "owner: one more", rnd=4)
        assert code == 0 and "owner: one more" in out, out
        assert final("g4-r4-review-gpt-6-sol")[1] == "final"
        code, out = run("reject", "g4", "--trust", "1", "--extended", "owner: one more", rnd=4)
        assert code == 2 and "already recorded" in out and len(rows()) == count + 1, out
        code, out = run("reject", "g1", rnd=3)  # g1 holds rounds 1 and 2: 3 is within 3
        assert code == 0, out
        code, out = run("reject", "g1", "--trust", "1", "--id", "g1-again")  # renumbered to 1
        assert code == 2 and "round 3 is past the bound of 2" in out, out

        # a rally counts against rally_turns (default 10), not trust_rounds, and returns DIFF
        code, out = run("diff", "g4r", "--trust", "1", "--stage", "rally", "--setup", "rally", rnd=4)
        assert code == 0 and final("g4r-r4-rally-gpt-6-sol") == ("DIFF", "final", "0"), out
        code, out = run("diff", "g4r", "--trust", "1", "--stage", "rally", "--setup", "rally", rnd=11)
        assert code == 2 and "past the bound of 10" in out, out

        # 5. a seat that writes into the candidate is reported, and its row still finalized
        code, out = run("touch", "g5", "--candidate", str(checkout))
        assert code == 3 and "candidate moved: + ?? new.txt" in out, out
        assert final("g5-r1-review-gpt-6-sol") == ("APPROVE", "final", "0")
        assert rows()["g5-r1-review-gpt-6-sol"]["candidate"] != "-"
        # the candidate is now dirty; a second edit to the same file changes no status line (rally r2)
        code, out = run("append", "g5", "--id", "g5-append", "--candidate", str(checkout))
        assert code == 3 and "candidate moved: - content" in out, out

        # 6. seats at once all finalize, the table intact; eight, because two rarely collide
        seats = [seat("slow", "g6", "--id", f"g6-{n}") for n in range(8)]
        assert [s.communicate(timeout=60) and s.returncode for s in seats] == [0] * 8
        assert {final(f"g6-{n}") for n in range(8)} == {("NOTE", "final", "0")}
        lines = (root / "dispatches.tsv").read_text().splitlines()
        assert len(lines) == len(rows()) + 1 and all(l.count("\t") == 16 for l in lines), lines

        # 7. a CLI that reads stdin gets EOF, not the caller's open pipe (repo t: 5s limit)
        held = seat("stdin", "g7", repo="t", stdin=subprocess.PIPE)
        code = held.wait(timeout=60)
        held.stdin.close()
        out = held.communicate()[0]
        assert code == 0 and final("g7-r1-review-gpt-6-sol") == ("APPROVE", "final", "0"), out

        # a verdict printed before a crash or the timeout belongs to an unfinished review (rally r1)
        code, out = run("crash", "g9")
        assert code == 1 and final("g9-r1-review-gpt-6-sol") == ("-", "final", "1"), out
        assert "exit 7" in out, out
        code, out = run("hang", "g9", "--id", "g9-hang", repo="t")
        assert code == 1 and final("g9-hang") == ("-", "final", "1") and "timeout" in out, out

        # a signal to the script, Ctrl-C included, is a cancel: the row is final with the outage
        # flag unknown
        for sig, gate in ((signal.SIGTERM, "g10"), (signal.SIGINT, "g10i")):
            (root / "cancel.up").unlink(missing_ok=True)
            child = seat("cancel", gate)
            for _ in range(400):
                if (root / "cancel.up").exists():
                    break
                time.sleep(0.05)
            child.send_signal(sig)
            out = child.communicate(timeout=60)[0]
            assert final(f"{gate}-r1-review-gpt-6-sol") == ("-", "final", "-"), out
            assert "cancelled" in out, out
            with contextlib.suppress(ProcessLookupError):  # a cancel takes the seat's children too
                os.kill(int((root / "cancel.pid").read_text()), 0)
                raise AssertionError("the cancelled seat's child outlived it")

        # a race rival's diff against the base, new files included, lands before the row is final
        racer = root / "racer"
        subprocess.run(["git", "init", "-q", str(racer)], check=True)
        subprocess.run([*git[:2], str(racer), *git[3:], "commit", "-q", "--allow-empty",
                        "--no-verify", "-m", "c"], check=True)
        base = subprocess.run(["git", "-C", str(racer), "rev-parse", "HEAD"], capture_output=True,
                              text=True, check=True).stdout.strip()
        race = ("--stage", "race", "--setup", "race", "--workdir", str(racer), "--diff-base")
        rival_diff = root / "scratch" / "rival.diff"
        fakes = root / "fakes"  # a git ahead on the seat's PATH sees the ledger at `add -A`
        fakes.mkdir()
        (fakes / "git").write_text('#!/bin/sh\n[ "$3" != add ] || { cut -f1,16 '
                                   '"$ASKRUBBERDUCK_HOME/dispatches.tsv" > "$0.seen"\n'
                                   '[ -z "$GIT_SLOW" ] || { echo $$ > "$0.pid"; exec sleep 30; }; }\n'
                                   'PATH="${PATH#*:}" exec git "$@"\n')
        (fakes / "git").chmod(0o755)
        fake_path = f"{fakes}:{root / 'bin' / 'race'}:{os.environ['PATH']}"
        code, out = run("race", "g11", *race, base, "--diff-out", str(rival_diff), PATH=fake_path)
        assert code == 0 and final("g11-r1-race-gpt-6-sol") == ("DIFF", "final", "0"), out
        assert "+raced" in rival_diff.read_text(), rival_diff.read_text()
        assert "GIT binary patch" in rival_diff.read_text(), rival_diff.read_text()
        assert "g11-r1-race-gpt-6-sol\tpending" in (fakes / "git.seen").read_text()
        # a cancel during the capture is a cancel, not a verdict, and leaves no diff
        child = seat("race", "g11", *race, base, "--diff-out", str(rival_diff), "--id",
                     "g11-cancel", PATH=fake_path, GIT_SLOW="1")
        for _ in range(400):
            if (fakes / "git.pid").exists():
                break
            time.sleep(0.05)
        else:
            raise AssertionError("the capture never started; the cancel would test nothing")
        child.send_signal(signal.SIGTERM)
        out = child.communicate(timeout=60)[0]
        assert final("g11-cancel") == ("-", "final", "-") and not rival_diff.exists(), out
        with contextlib.suppress(ProcessLookupError):  # the capture's git dies with the cancel
            os.kill(int((fakes / "git.pid").read_text()), 0)
            raise AssertionError("the cancelled capture's git outlived it")
        # a rival that leaves no change is an outage
        subprocess.run(["git", "-C", str(racer), "reset", "-q", "--hard", base], check=True)
        subprocess.run(["git", "-C", str(racer), "clean", "-qfd"], check=True)
        code, out = run("diff", "g11", *race, base, "--diff-out", str(rival_diff), "--id",
                        "g11-empty")
        assert code == 1 and "outage: empty diff" in out and not rival_diff.exists(), out
        # an outage captures nothing, and a stale diff from an earlier run is gone
        code, out = run("credits", "g11", *race, base, "--diff-out", str(rival_diff), "--id",
                        "g11-out")
        assert code == 1 and not rival_diff.exists(), out
        count = len(rows())  # the caller's own errors are refused before the row, not outages
        code, out = run("race", "g11", *race, "0" * 40, "--diff-out", str(rival_diff), "--id",
                        "g11-bad")
        assert code == 2 and "not a commit" in out and len(rows()) == count, out
        code, out = run("race", "g11", *race, base, "--diff-out", str(root / "absent" / "r.diff"),
                        "--id", "g11-nodir")
        assert code == 2 and "does not exist" in out and len(rows()) == count, out
        code, out = run("race", "g11", *race, base, "--diff-out", str(root), "--id", "g11-isdir")
        assert code == 2 and "names a directory" in out and len(rows()) == count, out
        code, out = run("race", "g11", "--diff-base", base, "--diff-out", str(rival_diff), "--id",
                        "g11-nowd")
        assert code == 2 and "needs --workdir" in out and len(rows()) == count, out
        code, out = run("race", "g11", *race, base, "--id", "g11-half")
        assert code == 2 and "go together" in out and len(rows()) == count, out
        code, out = run("reject", "g12", "--pin", "unknown:claude:high")  # transport by family only
        assert code == 2 and "no transport" in out and "--via" not in out, out
        code, out = run("reject", "g12", "--prompt", str(root / "missing-brief.md"))
        assert code == 2 and "unreadable input" in out and len(rows()) == count, out
        code, out = run("reject", "g12", rnd=0)
        assert code == 2 and "--round counts from 1" in out, out
        for gone in (["--self-check"], ["--cmd", "true"], ["--sha", "abc"], ["--via", "codex"]):
            code, out = run("reject", "g12", *gone)
            assert code == 2 and "unrecognized arguments" in out, (gone, out)
        assert len(rows()) == count, rows()
        out = subprocess.run([sys.executable, str(DISPATCH)], capture_output=True, text=True).stderr
        assert "required: --gate, --round, --stage, --setup, --trust, --pin, --prompt, --out" in out, out

        # a launch that raises still finalizes its row
        code, out = run("absent", "g8", PATH=str(root / "bin" / "absent"))  # no codex anywhere
        assert code == 1 and final("g8-r1-review-gpt-6-sol") == ("-", "final", "1"), out
        assert "outage: [Errno 2]" in out and "'codex'" in out, out
    # the rally bound's default is ledger's, read at import, not a second literal
    import ledger
    ledger.DEFAULT_RALLY_TURNS = 7
    import dispatch
    import importlib
    importlib.reload(dispatch)
    assert dispatch.STAGE_BOUNDS["rally"] == ("rally_turns", 7), dispatch.STAGE_BOUNDS
    print("dispatch self-check passed")
    return 0


def claude_canary() -> int:
    """Opt-in real CLI probe; fake API key and loopback response server, no vendor requests."""
    import http.server
    import json
    import shutil
    import threading
    from dispatch import transport

    cli = shutil.which("claude")
    assert cli, "claude must be installed for --claude-canary"
    hits = []

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            request = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            hits.append(request.decode())
            message = {"id": "msg_canary", "type": "message", "role": "assistant",
                       "model": "claude-sonnet-4-6", "content": [], "stop_reason": None,
                       "stop_sequence": None, "usage": {"input_tokens": 1, "output_tokens": 1}}
            events = [("message_start", {"message": message}),
                      ("content_block_start", {"index": 0, "content_block": {"type": "text", "text": ""}}),
                      ("content_block_delta", {"index": 0, "delta": {"type": "text_delta", "text": "OK"}}),
                      ("content_block_stop", {"index": 0}),
                      ("message_delta", {"delta": {"stop_reason": "end_turn", "stop_sequence": None},
                                         "usage": {"output_tokens": 1}}),
                      ("message_stop", {})]
            body = "".join(f"event: {kind}\ndata: {json.dumps({'type': kind, **data})}\n\n"
                           for kind, data in events).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with tempfile.TemporaryDirectory(prefix="duck-claude-canary-") as directory:
            root = Path(directory)
            config = root / "config"
            config.mkdir()
            scratch = root / "scratch"
            scratch.mkdir()
            marker = root / "hook-ran"
            instruction = "DUCK_CANARY_PRIVATE_INSTRUCTION"
            (config / "CLAUDE.md").write_text(instruction)
            (scratch / "CLAUDE.md").write_text(instruction)
            hook = {"hooks": {"SessionStart": [{"hooks": [{"type": "command",
                    "command": "touch " + shlex.quote(str(marker))}]}]}}
            (config / "settings.json").write_text(json.dumps(hook))
            (config / ".claude.json").write_text(json.dumps({"hasCompletedOnboarding": True}))
            (scratch / ".claude").mkdir()
            (scratch / ".claude" / "settings.json").write_text(json.dumps(hook))
            env = {key: os.environ[key] for key in ("PATH", "HOME", "USER", "TMPDIR")
                   if key in os.environ}
            env.update(CLAUDE_CONFIG_DIR=str(config), ANTHROPIC_API_KEY="local-canary-only",
                       ANTHROPIC_BASE_URL=f"http://127.0.0.1:{server.server_port}",
                       CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1")
            argv = transport("claude", "anthropic", "claude-sonnet-4-6", "-", "OK",
                             scratch, [], 20)
            argv[0] = cli
            argv[1:1] = ["--debug-file", str(root / "cli-debug.log")]
            # Positive control proves startup reached the hooks, not just that nothing ran.
            control = [part for part in argv if part not in
                       ("--setting-sources", "project", "--safe-mode")]
            subprocess.run(control, env=env, cwd=scratch, stdin=subprocess.DEVNULL,
                           capture_output=True, timeout=25, check=True)
            assert marker.exists() and hits, "positive control did not reach SessionStart/API"
            assert instruction in "".join(hits), "control did not load canary CLAUDE.md"
            marker.unlink()
            hits.clear()
            subprocess.run(argv, env=env, cwd=scratch, stdin=subprocess.DEVNULL,
                           capture_output=True, timeout=25, check=True)
            assert hits, "isolated seat did not initialize and reach the loopback API"
            assert not marker.exists(), "review seat ran a user/project hook"
            assert instruction not in "".join(hits), "review seat leaked canary instructions"
            assert not list(config.rglob("*.jsonl")), "review seat persisted a transcript"
    finally:
        server.shutdown()
        server.server_close()
    print("real Claude hook canary passed (loopback API only)")
    return 0


def codex_canary() -> int:
    """Opt-in real CLI probe: a fake owner home and a loopback Responses API, no vendor requests."""
    import http.server
    import json
    import threading
    from unittest import mock
    from dispatch import codex_env, transport

    cli = shutil.which("codex")
    assert cli, "codex must be installed for --codex-canary"
    hits = []

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            hits.append(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode())
            item = {"type": "message", "role": "assistant", "id": "msg_canary",
                    "content": [{"type": "output_text", "text": "OK", "annotations": []}]}
            usage = {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2}
            events = [("response.created", {"response": {"id": "resp_canary"}}),
                      ("response.output_item.done", {"output_index": 0, "item": item}),
                      ("response.completed", {"response": {"id": "resp_canary", "usage": usage}})]
            body = "".join(f"event: {kind}\ndata: {json.dumps({'type': kind, **data})}\n\n"
                           for kind, data in events).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with tempfile.TemporaryDirectory(prefix="duck-codex-canary-") as directory:
            root = Path(directory)
            home = root / "home"
            owner = home / ".codex"
            skill = home / ".agents" / "skills" / "duck-canary"
            skill.mkdir(parents=True)
            owner.mkdir()
            scratch = root / "scratch"
            scratch.mkdir()
            agents, skilled = "DUCK_CANARY_PRIVATE_INSTRUCTION", "DUCK_CANARY_PRIVATE_SKILL"
            (owner / "AGENTS.md").write_text(agents)
            (owner / "auth.json").write_text("{}")
            (skill / "SKILL.md").write_text(f"---\nname: duck-canary\ndescription: {skilled}\n---\n")
            env = {key: os.environ[key] for key in ("PATH", "USER", "TMPDIR") if key in os.environ}
            env.update(HOME=str(home), CODEX_HOME=str(owner), DUCK_CANARY_KEY="local-canary-only")
            argv = transport("codex", "openai", "duck-canary", "-", "OK", scratch, [], 20)
            argv[0] = cli
            argv[2:2] = ["-c", 'model_provider="duck_canary"', "-c",
                         "model_providers.duck_canary={name=\"duck canary\", base_url=\"http://"
                         f"127.0.0.1:{server.server_port}/v1\", env_key=\"DUCK_CANARY_KEY\", "
                         "wire_api=\"responses\"}"]
            # Positive control proves the owner's home reaches the request, not just that it is absent.
            subprocess.run(argv, env=env, cwd=scratch, stdin=subprocess.DEVNULL,
                           capture_output=True, timeout=60, check=True)
            assert hits and agents in hits[-1] and skilled in hits[-1], "control missed the owner home"
            hits.clear()
            seat = root / "seat"
            seat.mkdir()
            with mock.patch.dict(os.environ, env, clear=True):
                isolated = codex_env(seat, rival=False)
            subprocess.run(argv, env=isolated, cwd=scratch, stdin=subprocess.DEVNULL,
                           capture_output=True, timeout=60, check=True)
            assert hits, "isolated seat did not reach the loopback API"
            assert agents not in hits[-1], "review seat read the owner's AGENTS.md"
            assert skilled not in hits[-1], "review seat loaded the owner's skills"
    finally:
        server.shutdown()
        server.server_close()
    print("real Codex home canary passed (loopback API only)")
    return 0


if __name__ == "__main__":
    if "--claude-canary" in sys.argv:
        raise SystemExit(claude_canary())
    if "--codex-canary" in sys.argv:
        raise SystemExit(codex_canary())
    code = self_check()
    # seat isolation is a security property: check it wherever the real CLI exists
    for name, canary in (("Claude hook", claude_canary), ("Codex home", codex_canary)):
        cli = name.split()[0].lower()
        if not code and shutil.which(cli):
            code = canary()
        elif not code:
            print(f"real {name} canary skipped: {cli} is not installed")
    raise SystemExit(code)
