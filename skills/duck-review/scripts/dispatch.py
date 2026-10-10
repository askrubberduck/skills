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
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ inside an installed skill
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ledger import (DEFAULT_RALLY_TURNS, DISPATCH_COLUMNS, DISPATCH_ENUMS, arm_of,  # noqa: E402
                    default_origin, home, load_config, read_table, validate_row)

VIA = {"openai": "codex", "google": "agy", "anthropic": "claude"}  # by the pin's family
# Only boundary lines carry results; body markup only guards against quoted boundary examples.
# A heading or bold marker around the label is allowed.
VERDICT_LINE = re.compile(
    r" {0,3}(?:#{1,6} +)?[*_]*(?:VERDICT[\s*_]*:[\s*_]*(?P<verdict>APPROVE|REJECT|NOTE|DIFF)"
    r"|PLAN[\s*_]*:[\s*_]*(?P<plan>CONCUR|OBJECT))[\s*_]*\.?\s*")
BARE_RESULT = re.compile(r"\s*[*_]*(?:APPROVE|REJECT|CONCUR|OBJECT|DIFF)[*_]*\.?\s*")
# Checked only when no verdict was found, first match wins: while credits are out, codex reports
# that before anything else, so a later pin rejection proves nothing.
OUTAGES = (("credits", r"out of credits|insufficient credits?|credit balance"),
           ("capacity", r"at capacity|over capacity|overloaded"),
           ("quota", r"quota|RESOURCE_EXHAUSTED|\b429\b|rate.?limit"),
           ("model rejected", r"not supported|unknown model|invalid model|model.not.found"),
           ("permission denied", r"permission\b[\s\S]{0,200}?\bdenied"))  # a wrapped message too
CANCELS = {signal.SIGTERM, signal.SIGHUP, signal.SIGINT}  # the caller cancelling a seat
TOKENS = re.compile(r"tokens used\s*:?\s*(\d[\d,]*)", re.IGNORECASE)  # a count starts with a digit
# A stage with its own ceiling counts against it; review and disposition share the round bound.
STAGE_BOUNDS = {"plan": ("plan_rounds", 2), "rally": ("rally_turns", DEFAULT_RALLY_TURNS),
                "roast": ("roast_passes", 2)}


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
    if via == "claude":
        reasoning = ["--effort", effort] if effort != "-" else []
        return ["claude", "-p", "--model", model, *reasoning, "--permission-mode", "plan",
                "--permission-prompts", "none", "--setting-sources", "project", "--safe-mode",
                "--no-session-persistence", "--tools", "Read,Glob,Grep", "--strict-mcp-config",
                "--mcp-config", '{"mcpServers":{}}', *dirs, "--", prompt]
    # agy takes the effort as part of the model id: `gemini-3.1-pro-high`
    pinned = model if effort == "-" else f"{model}-{effort}"
    # headless agy auto-denies any tool it would ask about, reads included; plan mode reads freely
    # and still denies writes
    return ["agy", "--model", pinned, "--mode", "plan", *dirs, "--print-timeout",
            f"{math.ceil(limit)}s", "-p", prompt]


def classify(text: str, via: str, timed_out: bool, code: int, log: str = "") -> tuple[str, str]:
    """(verdict, outage cause). A seat that timed out or exited nonzero is an outage whatever it
    printed — a verdict before the crash belongs to a review that never finished; otherwise a found
    verdict is never an outage, whatever else the output says."""
    lines = text.splitlines()
    body = [i for i, line in enumerate(lines) if line.strip()]
    results = []
    boundaries = set(body[:1] + body[-1:])
    fence = None
    quoted = False
    for i, line in enumerate(lines):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            if fence is None:
                fence = marker[1]
            elif (marker[1][0] == fence[0] and len(marker[1]) >= len(fence)
                  and not line[marker.end():].strip()):
                fence = None
            continue
        if fence is not None:
            pass
        elif line.lstrip().startswith(">"):
            quoted = True
        elif not line.strip() or re.match(r"^ {0,3}#{1,6} ", line):
            quoted = False  # a heading starts a new block, not a quote continuation
        if i not in boundaries:
            continue
        if fence is not None or quoted:
            if VERDICT_LINE.fullmatch(line):
                results.append(None)  # a result that may be an example cannot be dropped silently
            continue
        if match := VERDICT_LINE.fullmatch(line):
            results.append(match["verdict"] or match["plan"])
        elif BARE_RESULT.fullmatch(line):
            results.append(None)  # an unlabeled result conflicts with a labeled one
    results = list(dict.fromkeys(results))
    verdict = results[0] if len(results) == 1 else None
    if timed_out:
        return "-", "timeout"
    if verdict and code == 0:
        return verdict, ""
    answer = "\n".join(lines)
    # a seat that answered and exited cleanly is judged by its answer, not its log
    seen = text if text.strip() and code == 0 else text + "\n" + log
    for cause, pattern in OUTAGES:
        if re.search(pattern, seen, re.IGNORECASE):
            return "-", cause
    if code != 0:
        return "-", f"exit {code}"
    return "-", "ambiguous verdict" if len(results) > 1 else "no verdict" if answer.strip() else "empty output"


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
    # one physical row per record: anything splitlines() breaks at would split it (record, ledger)
    bad += [c for c, value in row.items() if not value or "\t" in value
            or value.splitlines() != [value]]
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
        try:  # rows end only at a newline, as ledger.read_table reads them
            text = path.read_text(encoding="utf-8")
            lines = [f"{line}\n" for line in text.removesuffix("\n").split("\n")] if text else []
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
    the wait returns hands the next reader a shared file. A cancel waits until it is done."""
    held = signal.pthread_sigmask(signal.SIG_BLOCK, CANCELS)
    try:
        _stop(child)
    finally:
        signal.pthread_sigmask(signal.SIG_SETMASK, held)


def _stop(child: subprocess.Popen) -> None:
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


def codex_env(home: Path, rival: bool) -> dict[str, str]:
    """A codex seat's environment: `home` as CODEX_HOME holding only the owner's login, so the
    owner's AGENTS.md, config, plugins, memories and skills stay out. A review seat also gets it as
    HOME, which hides ~/.agents/skills; a rival keeps HOME, and those skills, for the owner's
    toolchains."""
    login = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex") / "auth.json"
    if login.exists():  # a link, not a copy: a token the seat refreshes stays the owner's login
        (home / "auth.json").symlink_to(login.resolve())
    return {**os.environ, "CODEX_HOME": str(home), **({} if rival else {"HOME": str(home)})}


def agy_env(home: Path) -> dict[str, str]:
    """An agy seat's environment: `home` as HOME, holding only the owner's login, so the owner's
    ~/.gemini/config rules and skills stay out. The login is two files under ~/.gemini plus the
    keychain, which macOS finds under HOME."""
    owner = Path.home()
    (home / ".gemini").mkdir()
    (home / "Library").mkdir()
    for part in (".gemini/oauth_creds.json", ".gemini/google_accounts.json", "Library/Keychains"):
        if (owner / part).exists():  # links, not copies: a refreshed token stays the owner's
            (home / part).symlink_to((owner / part).resolve())
    return {**os.environ, "HOME": str(home)}


def seat_signals() -> None:
    """In the seat, before exec: cancel signals at their defaults and unblocked, whatever dispatch
    inherited or holds, so stop()'s SIGTERM reaches it."""
    for sig in CANCELS:
        signal.signal(sig, signal.SIG_DFL)
    signal.pthread_sigmask(signal.SIG_UNBLOCK, CANCELS)


def launch(argv: list[str], out: Path, limit: float, workdir: Path,
           env: dict[str, str] | None = None) -> tuple[bool, int]:
    """Run to completion or the limit: (whether the limit ended it, the exit code)."""
    # A cancel during the spawn would skip stop(child) and leave the seat running: hold cancels for
    # the spawn alone, then let one land inside the guard. The output is opened first, so an open
    # that blocks stays cancellable.
    with out.open("w") as sink:
        signal.pthread_sigmask(signal.SIG_BLOCK, CANCELS)
        try:
            child = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=sink,
                                     stderr=subprocess.STDOUT, cwd=workdir, env=env,
                                     start_new_session=True, preexec_fn=seat_signals)
        except BaseException:
            signal.pthread_sigmask(signal.SIG_UNBLOCK, CANCELS)  # no child: release a held cancel
            raise
    try:
        signal.pthread_sigmask(signal.SIG_UNBLOCK, CANCELS)
        return False, child.wait(timeout=limit)
    except subprocess.TimeoutExpired:
        return True, -1
    finally:
        stop(child)

def capture(workdir: Path, base: str, dest: Path) -> str:
    """`add -A`, then the diff against `base`, landed whole: a reader never sees half a diff.
    "" when it landed, else the outage cause."""
    spare = dest.with_name(f".{dest.name}.{os.getpid()}")
    try:
        subprocess.run(["git", "-C", str(workdir), "add", "-A"], capture_output=True, check=True)
        with spare.open("wb") as sink:
            subprocess.run(["git", "-C", str(workdir), "diff", "--binary", base], stdout=sink,
                           stderr=subprocess.DEVNULL, check=True)
        if not spare.stat().st_size:
            return "empty diff"
        os.replace(spare, dest)
        return ""
    except (OSError, subprocess.CalledProcessError):
        return "diff capture failed"
    finally:
        spare.unlink(missing_ok=True)


def refuse(reason: str) -> int:
    print(f"refused: {reason}", file=sys.stderr)
    return 2


def run_seat(args) -> int:
    repo = args.repo or default_origin()
    if repo is None:
        return refuse("no origin resolved: pass --repo <origin>")
    config = load_config(repo)
    family, model, effort = arm_of(args.pin)
    via = VIA.get(family)
    if via is None or model == "-":
        return refuse(f"no transport for pin {args.pin!r}: pass family:model[:effort], family "
                      f"{' or '.join(VIA)}")
    if args.workdir == "":  # an unset $WT expands to nothing; the seat would run in scratch
        return refuse("--workdir is empty")
    if args.workdir and via == "agy":
        return refuse("agy seats review, they are not rivals: a --workdir seat, "
                      "a race or rally rival, needs codex")
    if args.workdir and via == "claude":
        return refuse("claude review seats are read-only: a --workdir seat needs codex")
    if (args.diff_base, args.diff_out) != (None, None):
        if not (args.diff_base and args.diff_out):
            return refuse("--diff-base and --diff-out each take a value, and go together")
        if not args.workdir:
            return refuse("--diff-out needs --workdir: the diff is of the seat's worktree")
    row_id = args.id or f"{args.gate}-r{args.round}-{args.stage}-{model}"

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
    if args.diff_out and Path(args.diff_out).is_dir():
        return refuse(f"--diff-out names a directory: {args.diff_out}")
    if args.diff_out and not Path(args.diff_out).resolve().parent.is_dir():
        return refuse(f"--diff-out's directory does not exist: {args.diff_out}")
    if args.diff_base and subprocess.run(
            ["git", "-C", str(workdir), "rev-parse", "--verify", f"{args.diff_base}^{{commit}}"],
            capture_output=True).returncode:
        return refuse(f"--diff-base is not a commit in {workdir}: {args.diff_base}")
    argv = transport(via, family, model, effort, prompt, workdir, args.add_dir, timeout)
    # codex's log echoes the prompt and repeats the answer; its last message is the answer alone
    answer = out.with_name(out.name + ".answer") if via == "codex" else out
    if via == "codex":
        argv[2:2] = ["--output-last-message", str(answer)]
    candidate = (before[0].removeprefix("HEAD ")[:7] if before else "") or "-"
    row = dict(id=row_id, gate_id=args.gate, round=str(args.round),
               date=datetime.date.today().isoformat(), repo=repo, stage=args.stage,
               setup=args.setup, trust=args.trust, candidate=candidate, family=family,
               model=model, effort=effort, minutes="-", tokens="-", verdict="-",
               status="pending", outage="-")
    if bad_values(row):
        return refuse(f"not a ledger value in {', '.join(bad_values(row))}")
    cancelled = []  # a signal to this script is the caller cancelling: no verdict, no outage

    def cancel(number, _):
        cancelled.append(number)
        sys.exit(128 + number)  # an interrupted run still finalizes its row

    for sig in CANCELS:
        signal.signal(sig, cancel)
    # handlers first: an inherited SIG_IGN would drop a cancel held across the pending write.
    # From the pending row on, a cancel must finalize it: held until the guard below is in place
    signal.pthread_sigmask(signal.SIG_BLOCK, CANCELS)
    if not record(row, new=True):
        signal.pthread_sigmask(signal.SIG_UNBLOCK, CANCELS)
        return refuse(f"{row_id} is already recorded; a rerun takes a new --id")

    started = time.monotonic()
    verdict, cause, moved = "-", "crashed", []
    diff = Path(args.diff_out).resolve() if args.diff_out else None
    isolated = None
    try:
        signal.pthread_sigmask(signal.SIG_UNBLOCK, CANCELS)  # a held cancel lands here, guarded
        if reached > limit:  # a print can block on a full pipe: never while cancels are held
            print(f"extended past the bound of {limit} rounds by the owner: {args.extended}")
        isolated = Path(tempfile.mkdtemp(prefix=f"askrubberduck-{via}-")) if via != "claude" else None
        if diff:
            diff.unlink(missing_ok=True)  # a reader waiting for it must not take a stale one
        answer.unlink(missing_ok=True)  # a stale answer from an earlier run is no answer
        env = (codex_env(isolated, rival=bool(args.workdir)) if via == "codex"
               else agy_env(isolated) if isolated else None)
        timed_out, code = launch(argv, out, timeout, workdir, env)
        text = out.read_text(encoding="utf-8", errors="replace")
        reply = answer.read_text(encoding="utf-8", errors="replace") if answer.exists() else ""
        found, cause = classify(reply, via, timed_out, code, text)
        if diff and found != "-" and (failed := capture(workdir, args.diff_base, diff)):
            found, cause = "-", failed
        verdict = found  # only now: a cancel during the capture records a cancel, not a verdict
        row["tokens"] = tokens_of(text)
        if before is not None:
            after = snapshot(args.candidate)
            moved = [f"- {line}" for line in before if line not in after]
            moved += [f"+ {line}" for line in after if line not in before]
    finally:
        signal.pthread_sigmask(signal.SIG_BLOCK, CANCELS)  # a second cancel waits for the final row
        if isolated:
            shutil.rmtree(isolated, ignore_errors=True)
        row.update(minutes=str(math.ceil((time.monotonic() - started) / 60)), verdict=verdict,
                   status="final", outage="0" if verdict != "-" else "-" if cancelled else "1")
        record(row, new=False)
        if cancelled:
            print(f"{row_id} cancelled {row['minutes']}m")
        signal.pthread_sigmask(signal.SIG_UNBLOCK, CANCELS)
    for line in moved:
        print(f"candidate moved: {line}")
    print(f"{row_id} {verdict if verdict != '-' else f'outage: {cause}'} {row['minutes']}m")
    return 3 if moved else 0 if verdict != "-" else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--gate", required=True, help="gate id")
    parser.add_argument("--round", required=True, type=int, help="this gate's round, from 1")
    parser.add_argument("--stage", required=True, choices=sorted(DISPATCH_ENUMS["stage"]))
    parser.add_argument("--setup", required=True, choices=sorted(DISPATCH_ENUMS["setup"]))
    parser.add_argument("--trust", required=True, choices=sorted(DISPATCH_ENUMS["trust"]))
    parser.add_argument("--pin", required=True,
                        help="family:model[:effort], as config.toml spells it")
    parser.add_argument("--prompt", required=True,
                        help="UTF-8 brief file path; its contents become the CLI prompt argument")
    parser.add_argument("--out", required=True,
                        help="the seat's output file; its directory is the scratch dir")
    parser.add_argument("--repo", help="default: this checkout's origin")
    parser.add_argument("--candidate", help="checkout the seat must not change")
    parser.add_argument("--workdir", help="the seat's working directory; default: --out's")
    parser.add_argument("--add-dir", action="append", default=[], help="material directory")
    parser.add_argument("--diff-base", help="with --diff-out: the base SHA the worktree diffs from")
    parser.add_argument("--diff-out", help="after a verdict, the --workdir diff lands here")
    parser.add_argument("--extended", help="the owner's words extending the round bound")
    parser.add_argument("--id", help="row id; default: <gate>-r<round>-<stage>-<model>")
    args = parser.parse_args(argv)
    if args.round < 1:
        parser.error("--round counts from 1")
    try:
        return run_seat(args)
    except OSError as error:  # the CLI is missing or the scratch dir unwritable; the row is final
        print(f"outage: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
