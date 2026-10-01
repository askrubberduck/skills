#!/usr/bin/env python3
"""Run one reviewer seat end to end and record it in the dispatch ledger: a `pending` row before
launch, the CLI bounded by `[bounds].dispatch_timeout` with stdin closed, the output classified as a
verdict or an outage with its cause, and the row finalized on every exit. It refuses a round past
the recorded bound unless the owner's extension is given, and reports a candidate the seat changed.
Writing rows is this script's job; ledger.py stays the reader. Stdlib only, like ledger.py.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime
import fcntl
import hashlib
import math
import os
import re
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ inside an installed skill
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ledger import (DISPATCH_COLUMNS, DISPATCH_ENUMS, arm_of, default_origin, home,  # noqa: E402
                    load_config, read_table, validate_row)

VIA = {"openai": "codex", "google": "agy"}  # by the pin's family; `--via` overrides
VERDICT_LINE = re.compile(
    r"^[\s>#*_`]*(?:(?:VERDICT|PLAN)\s*:[\s*_`]*)?(APPROVE|REJECT|NOTE|CONCUR|OBJECT|DIFF)[\s*_`.]*$")
# Checked only when no verdict was found, first match wins: while credits are out, codex reports
# that before anything else, so a later pin rejection proves nothing.
OUTAGES = (("credits", r"out of credits|insufficient credits?|credit balance"),
           ("capacity", r"at capacity|over capacity|overloaded"),
           ("quota", r"quota|RESOURCE_EXHAUSTED|\b429\b|rate.?limit"),
           ("model rejected", r"not supported|unknown model|invalid model|model.not.found"),
           ("permission denied", r"permission\b.*\b(?:auto-)?denied"))
TOKENS = re.compile(r"tokens used\s*:?\s*([\d,]+)", re.IGNORECASE)
CODEX_ANSWER = "codex"  # codex exec prints this line alone before its final answer
# A stage with its own ceiling counts against it; review and disposition share the round bound.
STAGE_BOUNDS = {"plan": ("plan_rounds", 2), "rally": ("rally_turns", 10), "roast": ("roast_passes", 2)}


def seconds(value: str) -> float:
    match = re.fullmatch(r"(\d+(?:\.\d+)?)([smh]?)", value.strip())
    if not match:
        raise SystemExit(f"[bounds].dispatch_timeout: not a duration: {value!r}")
    return float(match[1]) * {"": 1, "s": 1, "m": 60, "h": 3600}[match[2]]


def transport(via: str, family: str, model: str, effort: str, prompt: str, workdir: Path,
              add_dirs: list[str], limit: float) -> list[str]:
    dirs = [part for d in add_dirs for part in ("--add-dir", str(Path(d).resolve()))]
    if via == "codex":
        reasoning = ["-c", f"model_reasoning_effort={effort}"] if effort != "-" else []
        return ["codex", "exec", "-m", model, *reasoning, "-s", "workspace-write", "-C",
                str(workdir), "--skip-git-repo-check", *dirs, prompt]
    # agy takes the effort as part of the model id: `gemini-3.1-pro-high`
    pinned = model if effort == "-" else f"{model}-{effort}"
    return ["agy", "--model", pinned, *dirs, "--print-timeout", f"{math.ceil(limit)}s", "-p", prompt]


def classify(text: str, via: str, timed_out: bool, code: int) -> tuple[str, str]:
    """(verdict, outage cause). A seat that timed out or exited nonzero is an outage whatever it
    printed — a verdict before the crash belongs to a review that never finished; otherwise a found
    verdict is never an outage, whatever else the output says."""
    lines = text.splitlines()
    if via == "codex" and CODEX_ANSWER in lines:  # before it, codex echoes the prompt
        lines = lines[len(lines) - lines[::-1].index(CODEX_ANSWER):]
    verdicts = [match[1] for match in map(VERDICT_LINE.match, lines) if match]
    if timed_out:
        return "-", "timeout"
    if verdicts and code == 0:
        return verdicts[-1], ""
    answer = "\n".join(lines)
    for cause, pattern in OUTAGES:
        if re.search(pattern, answer, re.IGNORECASE):
            return "-", cause
    if code != 0:
        return "-", f"exit {code}"
    return "-", "no verdict" if answer.strip() else "empty output"


def tokens_of(text: str) -> str:
    found = TOKENS.findall(text)
    return found[-1].replace(",", "") if found else "-"


def snapshot(checkout: str) -> list[str]:
    """HEAD, the status lines, and a digest of the bytes behind them: a reviewed candidate is often
    a dirty worktree, and a second edit to an already-modified file leaves the status unchanged."""
    def git(*argv: str) -> bytes:
        return subprocess.run(["git", "-C", checkout, *argv], capture_output=True, check=True).stdout

    head = git("rev-parse", "HEAD").decode().strip()
    status = git("status", "--porcelain=v1", "-uall").decode()
    content = hashlib.sha256(git("diff", "HEAD", "--binary"))
    for name in git("ls-files", "-o", "--exclude-standard", "-z").split(b"\0"):
        if name:
            content.update(name + b"\0" + (Path(checkout) / name.decode()).read_bytes())
    return [f"HEAD {head}", *status.splitlines(), f"content {content.hexdigest()[:12]}"]


def bad_values(row: dict) -> list[str]:
    bad = [c for c, allowed in DISPATCH_ENUMS.items() if row[c] != "-" and row[c] not in allowed]
    bad += [c for c, value in row.items() if not value or re.search(r"[\t\r\n]", value)]
    return bad if validate_row("dispatches.tsv", 0, row) else bad + ["numbers"]


@contextlib.contextmanager
def locked_ledger():
    """The home directory is the lock, not the table: the table is replaced on every write, and a
    lock on a replaced file guards nothing."""
    home().mkdir(parents=True, exist_ok=True)
    fd = os.open(home(), os.O_RDONLY)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield home() / "dispatches.tsv"
    finally:
        os.close(fd)


def record(row: dict, new: bool) -> bool:
    """Append `row`, or replace the line carrying its id; False when a new row's id is taken."""
    if bad_values(row):
        raise ValueError(f"refusing to write {', '.join(bad_values(row))}: {row}")
    line = "\t".join(row[c] for c in DISPATCH_COLUMNS) + "\n"
    with locked_ledger() as path:
        try:
            lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        except FileNotFoundError:
            lines = []
        lines = lines or ["\t".join(DISPATCH_COLUMNS) + "\n"]
        lines[-1] = lines[-1] if lines[-1].endswith("\n") else lines[-1] + "\n"
        ids = [other.split("\t", 1)[0] for other in lines]
        if new and row["id"] in ids[1:]:
            return False
        if not new and row["id"] in ids[1:]:
            lines[ids.index(row["id"], 1)] = line
        else:  # a new row, or a pending one somebody removed while the seat ran
            lines.append(line)
        target = path.resolve()  # a symlinked table stays a symlink
        spare = target.with_name(f".{target.name}.{os.getpid()}")
        spare.write_text("".join(lines), encoding="utf-8")
        os.replace(spare, target)
    return True


def stop(child: subprocess.Popen) -> None:
    """Kill the seat's whole process group and wait until it is gone: a seat still writing after
    the wait returns hands the next reader a shared file."""
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(child.pid, sig)
        except (ProcessLookupError, PermissionError):
            return
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            child.poll()  # reap the leader, or its zombie keeps the group alive
            try:
                os.killpg(child.pid, 0)
            except (ProcessLookupError, PermissionError):  # macOS: EPERM once only zombies remain
                return
            time.sleep(0.05)
    raise RuntimeError(f"process group {child.pid} survived SIGKILL")


def launch(argv: list[str], out: Path, limit: float, workdir: Path) -> tuple[bool, int]:
    """Run to completion or the limit: (whether the limit ended it, the exit code)."""
    with out.open("w") as sink:
        child = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=sink,
                                 stderr=subprocess.STDOUT, cwd=workdir, start_new_session=True)
    try:
        return False, child.wait(timeout=limit)
    except subprocess.TimeoutExpired:
        return True, -1
    finally:
        stop(child)


def refuse(reason: str) -> int:
    print(f"refused: {reason}", file=sys.stderr)
    return 2


def run_seat(args) -> int:
    repo = args.repo or default_origin()
    if repo is None:
        return refuse("no origin resolved: pass --repo <origin>")
    config = load_config(repo)
    family, model, effort = arm_of(args.pin)
    via = args.via or VIA.get(family)
    if via is None or model == "-":
        return refuse(f"no transport for pin {args.pin!r}: pass family:model[:effort] and --via")
    if args.workdir and via == "agy":
        return refuse("agy cannot write headless (it auto-denies write_file): a --workdir seat, "
                      "a race or rally rival, needs codex")
    row_id = args.id or f"{args.gate}-r{args.round}-{model}"

    trust = args.trust == "1"
    key, default = STAGE_BOUNDS.get(args.stage, ("trust_rounds", 2) if trust else ("review_rounds", 3))
    limit = int(config.get(key, default))
    # Renumbering does not reset the bound: the gate's recorded rounds count too.
    rounds = {d["round"] for d in read_table("dispatches.tsv", DISPATCH_COLUMNS, DISPATCH_ENUMS)
              if d["repo"] == repo and d["gate_id"] == args.gate and d["stage"] == args.stage}
    rounds |= {str(args.round)}
    reached = max(args.round, len(rounds))
    if reached > limit and not args.extended:
        return refuse(f"round {reached} is past the bound of {limit}; the owner's words go in "
                      "--extended")

    try:
        prompt = Path(args.prompt).read_text(encoding="utf-8")
        before = snapshot(args.candidate) if args.candidate else None
    except (OSError, UnicodeDecodeError, subprocess.CalledProcessError) as error:
        return refuse(f"unreadable input: {error}")
    timeout = seconds(str(config.get("dispatch_timeout", "45m")))
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    workdir = Path(args.workdir).resolve() if args.workdir else out.parent
    if not workdir.is_dir():
        return refuse(f"--workdir is not a directory: {workdir}")
    argv = transport(via, family, model, effort, prompt, workdir, args.add_dir, timeout)
    if args.cmd:
        argv = [args.cmd, *argv]
    candidate = args.sha or (before[0].removeprefix("HEAD ")[:7] if before else "") or "-"
    row = dict(id=row_id, gate_id=args.gate, round=str(args.round),
               date=datetime.date.today().isoformat(), repo=repo, stage=args.stage,
               setup=args.setup, trust=args.trust, candidate=candidate, family=family,
               model=model, effort=effort, minutes="-", tokens="-", verdict="-",
               status="pending", outage="-")
    if bad_values(row):
        return refuse(f"not a ledger value in {', '.join(bad_values(row))}")
    if not record(row, new=True):
        return refuse(f"{row_id} is already recorded; a rerun takes a new --id")
    if reached > limit:
        print(f"extended past the bound of {limit} rounds by the owner: {args.extended}")

    cancelled = []  # a signal to this script is the caller cancelling: no verdict, no outage

    def cancel(number, _):
        cancelled.append(number)
        sys.exit(128 + number)  # an interrupted run still finalizes its row

    for sig in (signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, cancel)
    started = time.monotonic()
    verdict, cause, moved = "-", "crashed", []
    try:
        timed_out, code = launch(argv, out, timeout, workdir)
        text = out.read_text(encoding="utf-8", errors="replace")
        verdict, cause = classify(text, via, timed_out, code)
        row["tokens"] = tokens_of(text)
        if before is not None:
            after = snapshot(args.candidate)
            moved = [f"- {line}" for line in before if line not in after]
            moved += [f"+ {line}" for line in after if line not in before]
    finally:
        row.update(minutes=str(math.ceil((time.monotonic() - started) / 60)), verdict=verdict,
                   status="final", outage="0" if verdict != "-" else "-" if cancelled else "1")
        record(row, new=False)
        if cancelled:
            print(f"{row_id} cancelled {row['minutes']}m")
    for line in moved:
        print(f"candidate moved: {line}")
    print(f"{row_id} {verdict if verdict != '-' else f'outage: {cause}'} {row['minutes']}m")
    return 3 if moved else 0 if verdict != "-" else 1


CONFIG_FIXTURE = """\
[bounds]
review_rounds = 3
trust_rounds = 2
dispatch_timeout = "1s"
[repo."r"]
dispatch_timeout = "20s"
"""
STUBS = {
    # codex echoes the prompt after `user`; only the text after its answer marker is the answer
    "reject": 'printf \'%s\\0\' "$@" > "$0.argv"; pwd -P > "$0.cwd"; cut -f1,16 "$ASKRUBBERDUCK_HOME/dispatches.tsv"'
              ' > "$0.seen"\nprintf \'user\\nAPPROVE\\ncodex\\n**VERDICT: REJECT**\\n'
              'tokens used\\n1,234\\n\'',
    "greeting": "printf 'user\\nVERDICT: REJECT\\ncodex\\nHello! How can I help?\\n'",
    "credits": "echo \"ERROR: You're out of credits. Add credits to continue.\"; exit 1",
    "sleep": 'sleep 30 & echo $! > "$0.pid"; wait',
    "touch": 'touch "$CANDIDATE/new.txt"; echo APPROVE',
    "slow": "sleep 0.5; echo NOTE",
    "stdin": "cat > /dev/null; echo APPROVE",
    "diff": "echo DIFF",
    "crash": "echo APPROVE; exit 7",
    "append": 'echo more >> "$CANDIDATE/new.txt"; echo APPROVE',
    "hang": "echo APPROVE; sleep 30",
    "denied": "echo 'Error: a tool required the \"write_file\" permission that headless mode'"
              " 'cannot prompt for, so it was auto-denied'",
    "cancel": 'sleep 30 & echo $! > "$0.pid"; touch "$0.up"; wait',
}


def self_check() -> int:
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
        env = {**os.environ, "CANDIDATE": str(checkout)}
        outs = iter(range(100))  # parallel seats of one gate must not share an output file

        def seat(stub: str, gate: str, *extra: str, rnd: int = 1, repo: str = "r",
                 stdin=subprocess.DEVNULL) -> subprocess.Popen:
            argv = [sys.executable, __file__, "--gate", gate, "--round", str(rnd), "--stage",
                    "review", "--setup", "independent", "--trust", "0", "--pin",
                    "openai:gpt-6-sol:high", "--prompt", str(prompt), "--out",
                    str(root / "scratch" / f"{gate}-{next(outs)}.out"), "--repo", repo,
                    "--cmd", str(root / stub), *extra]
            return subprocess.Popen(argv, stdin=stdin, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True, cwd=root, env=env)

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

        # 1. a REJECT after codex's answer marker is the verdict, not the echoed APPROVE; round 2
        # of trust work sits on its bound of 2 and runs; the row was pending while the seat ran
        code, out = run("reject", "g1", "--trust", "1", rnd=2)
        assert code == 0 and final("g1-r2-gpt-6-sol") == ("REJECT", "final", "0"), (code, out)
        assert rows()["g1-r2-gpt-6-sol"]["tokens"] == "1234", rows()["g1-r2-gpt-6-sol"]
        assert "g1-r2-gpt-6-sol\tpending" in (root / "reject.seen").read_text()
        assert (root / "reject.argv").read_text().split("\0")[:-1] == [
            "codex", "exec", "-m", "gpt-6-sol", "-c", "model_reasoning_effort=high", "-s",
            "workspace-write", "-C", str(root / "scratch"), "--skip-git-repo-check",
            prompt.read_text()]
        assert (root / "reject.cwd").read_text().strip() == str(root / "scratch")
        code, out = run("reject", "g1", "--pin", "google:gemini-3.1-pro-high", "--add-dir",
                        str(checkout))
        assert code == 0 and final("g1-r1-gemini-3.1-pro-high") == ("REJECT", "final", "0"), out
        assert (root / "reject.argv").read_text().split("\0")[:-1] == [
            "agy", "--model", "gemini-3.1-pro-high", "--add-dir", str(checkout),
            "--print-timeout", "20s", "-p", prompt.read_text()]
        # a second agy seat of the same gate and round takes its own default id
        code, out = run("reject", "g1", "--pin", "google:gemini-3.1-flash")
        assert code == 0 and final("g1-r1-gemini-3.1-flash") == ("REJECT", "final", "0"), out
        # --workdir moves the seat into a rival's worktree: codex -C and the cwd
        rival = root / "rival"
        rival.mkdir()
        code, out = run("reject", "g1w", "--workdir", str(rival))
        assert code == 0 and "-C\0" + str(rival) + "\0" in (root / "reject.argv").read_text(), out
        assert (root / "reject.cwd").read_text().strip() == str(rival)
        count = len(rows())  # agy auto-denies write_file headless: a rival needs codex
        code, out = run("reject", "g1w", "--workdir", str(rival), "--pin", "google:gemini-3.1-pro")
        assert code == 2 and "needs codex" in out and len(rows()) == count, out
        code, out = run("greeting", "g1b")  # the prompt's verdict is no answer
        assert code == 1 and final("g1b-r1-gpt-6-sol") == ("-", "final", "1"), out
        assert "no verdict" in out, out

        # 2. the credits error is an outage with its cause
        code, out = run("credits", "g2")
        assert code == 1 and final("g2-r1-gpt-6-sol") == ("-", "final", "1"), out
        assert "outage: credits" in out, out
        code, out = run("denied", "g2", "--id", "g2-denied")  # agy headless auto-deny
        assert code == 1 and "outage: permission denied" in out, out

        # 3. past the 1s limit the whole group is killed, its grandchild included
        started = time.monotonic()
        code, out = run("sleep", "g3", repo="t")
        assert code == 1 and "outage: timeout" in out and time.monotonic() - started < 10, out
        assert final("g3-r1-gpt-6-sol") == ("-", "final", "1")
        with contextlib.suppress(ProcessLookupError):
            os.kill(int((root / "sleep.pid").read_text()), 0)
            raise AssertionError("the seat's child outlived the timeout")

        # 4. round 4 of trust work past trust_rounds = 2: refused with no row, run when extended
        count = len(rows())
        code, out = run("reject", "g4", "--trust", "1", rnd=4)
        assert code == 2 and "past the bound of 2" in out and len(rows()) == count, out
        code, out = run("reject", "g4", "--trust", "1", "--extended", "owner: one more", rnd=4)
        assert code == 0 and "owner: one more" in out, out
        assert final("g4-r4-gpt-6-sol")[1] == "final"
        code, out = run("reject", "g4", "--trust", "1", "--extended", "owner: one more", rnd=4)
        assert code == 2 and "already recorded" in out and len(rows()) == count + 1, out
        code, out = run("reject", "g1", rnd=3)  # g1 holds rounds 1 and 2: 3 is within 3
        assert code == 0, out
        code, out = run("reject", "g1", "--trust", "1", "--id", "g1-again")  # renumbered to 1
        assert code == 2 and "round 3 is past the bound of 2" in out, out

        # a rally counts against rally_turns (default 10), not trust_rounds, and returns DIFF
        code, out = run("diff", "g4r", "--trust", "1", "--stage", "rally", "--setup", "rally", rnd=4)
        assert code == 0 and final("g4r-r4-gpt-6-sol") == ("DIFF", "final", "0"), out
        code, out = run("diff", "g4r", "--trust", "1", "--stage", "rally", "--setup", "rally", rnd=11)
        assert code == 2 and "past the bound of 10" in out, out

        # 5. a seat that writes into the candidate is reported, and its row still finalized
        code, out = run("touch", "g5", "--candidate", str(checkout))
        assert code == 3 and "candidate moved: + ?? new.txt" in out, out
        assert final("g5-r1-gpt-6-sol") == ("APPROVE", "final", "0")
        assert rows()["g5-r1-gpt-6-sol"]["candidate"] != "-"
        # the candidate is now dirty; a second edit to the same file changes no status line (rally r2)
        code, out = run("append", "g5", "--id", "g5-append", "--candidate", str(checkout))
        assert code == 3 and "candidate moved: - content" in out, out

        # 6. seats at once all finalize, the table intact; eight, because two rarely collide
        seats = [seat("slow", "g6", "--id", f"g6-{n}") for n in range(8)]
        assert [s.communicate(timeout=60) and s.returncode for s in seats] == [0] * 8
        assert {final(f"g6-{n}") for n in range(8)} == {("NOTE", "final", "0")}
        lines = (root / "dispatches.tsv").read_text().splitlines()
        assert len(lines) == len(rows()) + 1 and all(l.count("\t") == 16 for l in lines), lines

        # 7. a CLI that reads stdin gets EOF, not the caller's open pipe (repo t: 1s limit)
        held = seat("stdin", "g7", repo="t", stdin=subprocess.PIPE)
        code = held.wait(timeout=60)
        held.stdin.close()
        out = held.communicate()[0]
        assert code == 0 and final("g7-r1-gpt-6-sol") == ("APPROVE", "final", "0"), out

        # a verdict printed before a crash or the timeout belongs to an unfinished review (rally r1)
        code, out = run("crash", "g9")
        assert code == 1 and final("g9-r1-gpt-6-sol") == ("-", "final", "1"), out
        assert "exit 7" in out, out
        code, out = run("hang", "g9", "--id", "g9-hang", repo="t")
        assert code == 1 and final("g9-hang") == ("-", "final", "1") and "timeout" in out, out

        # a signal to the script is a cancel: the row is final with the outage flag unknown
        child = seat("cancel", "g10")
        for _ in range(400):
            if (root / "cancel.up").exists():
                break
            time.sleep(0.05)
        child.send_signal(signal.SIGTERM)
        out = child.communicate(timeout=60)[0]
        assert final("g10-r1-gpt-6-sol") == ("-", "final", "-") and "cancelled" in out, out
        with contextlib.suppress(ProcessLookupError):  # a cancel takes the seat's children too
            os.kill(int((root / "cancel.pid").read_text()), 0)
            raise AssertionError("the cancelled seat's child outlived it")

        # a launch that raises still finalizes its row
        code, out = run("absent", "g8")
        assert code == 1 and final("g8-r1-gpt-6-sol") == ("-", "final", "1"), out
    print("dispatch self-check passed")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--self-check", action="store_true", help="run the falsifying checks")
    parser.add_argument("--gate", help="gate id")
    parser.add_argument("--round", type=int, help="this gate's round, from 1")
    parser.add_argument("--stage", choices=sorted(DISPATCH_ENUMS["stage"]))
    parser.add_argument("--setup", choices=sorted(DISPATCH_ENUMS["setup"]))
    parser.add_argument("--trust", choices=sorted(DISPATCH_ENUMS["trust"]))
    parser.add_argument("--pin", help="family:model[:effort], as config.toml spells it")
    parser.add_argument("--prompt", help="the brief; it travels as an argument")
    parser.add_argument("--out", help="the seat's output file; its directory is the scratch dir")
    parser.add_argument("--repo", help="default: this checkout's origin")
    parser.add_argument("--candidate", help="checkout the seat must not change")
    parser.add_argument("--sha", help="candidate revision for the row; default: --candidate's HEAD")
    parser.add_argument("--via", choices=sorted(set(VIA.values())), help="default: by family")
    parser.add_argument("--workdir", help="the seat's working directory; default: --out's")
    parser.add_argument("--add-dir", action="append", default=[], help="material directory")
    parser.add_argument("--extended", help="the owner's words extending the round bound")
    parser.add_argument("--id", help="row id; default: <gate>-r<round>-<model>")
    parser.add_argument("--cmd", help=argparse.SUPPRESS)  # self-check: a stub ahead of the argv
    args = parser.parse_args(argv)
    if args.self_check:
        return self_check()
    missing = [f"--{name}" for name in ("gate", "round", "stage", "setup", "trust", "pin",
                                         "prompt", "out") if getattr(args, name) is None]
    if missing:
        parser.error(f"required: {' '.join(missing)}")
    if args.round < 1:
        parser.error("--round counts from 1")
    try:
        return run_seat(args)
    except OSError as error:  # the CLI is missing or the scratch dir unwritable; the row is final
        print(f"outage: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
