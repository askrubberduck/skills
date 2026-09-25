#!/usr/bin/env python3
"""Read the dispatch ledger under ~/.askrubberduck/ and answer the questions a gate asks between
rounds: how many findings a capture is still missing, which reviewer arm to send next, whether a
paired trial has separated yet, and what a setup costs. Every number here is an estimate over rows
somebody wrote down; this script never judges the work, only counts what the ledger says about it.
Stdlib only, for the same reason the distribution gate is: no install step anywhere it runs.
"""

from __future__ import annotations

import argparse
import contextlib
import csv
import io
import math
import os
import random
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

DISPATCH_COLUMNS = ("id", "gate_id", "round", "date", "repo", "stage", "setup", "trust",
                    "candidate", "family", "model", "effort", "minutes", "tokens", "verdict",
                    "status", "outage")
FINDING_COLUMNS = ("dispatch_id", "gate_id", "candidate", "cause_id", "class", "tier", "severity",
                   "substantiated", "adjudicated_by")
DISPATCH_ENUMS = {
    # `disposition` is Broad's cross-family adjudication call: a dispatch, never a capture.
    "stage": {"review", "disposition", "plan", "proof", "break", "race", "rally"},
    "setup": {"self-check", "independent", "broad", "race", "rally"},
    "trust": {"0", "1"}, "status": {"pending", "final"}, "outage": {"0", "1"},
    "verdict": {"APPROVE", "REJECT", "NOTE", "DIFF", "CONCUR", "OBJECT"},
}
FINDING_ENUMS = {
    "tier": {"executed", "static", "read", "production"},
    "severity": {"BLOCKER", "SHOULD", "NOTE"}, "substantiated": {"0", "1"},
}
NUMERIC_COLUMNS = ("round", "minutes", "tokens")
# Broad is two reviews plus two cross-family dispositions (challenge.md).
SETUP_DISPATCHES = {"self-check": 0, "independent": 1, "broad": 4, "race": 1}
DEFAULT_RALLY_TURNS = 10
# Roles whose unset list falls back to the reviewer roster; worker and explore fall back to the host.
REVIEWER_FALLBACK = {"review", "disposition", "race", "plan"}
OUTAGE_LIMIT = 0.2
DRIFT_LIMIT = 0.5


def home() -> Path:
    return Path(os.environ.get("ASKRUBBERDUCK_HOME", "~/.askrubberduck")).expanduser()


def normalize_origin(url: str) -> str:
    """Both spellings of one remote name one repo: drop the transport, the login, the `.git`, and
    the scp-style colon standing in for the first slash."""
    url = url.strip().removesuffix("/").removesuffix(".git")
    _, _, url = url.rpartition("://")
    _, _, url = url.rpartition("@")
    host, colon, path = url.partition(":")
    return f"{host}/{path.lstrip('/')}" if colon else url


def default_origin() -> str | None:
    try:
        done = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True,
                              text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return None
    return normalize_origin(done.stdout) if done.returncode == 0 else None


def load_config(repo: str | None = None) -> dict:
    """Flattened: sections collapse into one namespace because a repo override table carries keys
    from any of them, and lists replace wholesale rather than merging."""
    try:
        raw = tomllib.loads((home() / "config.toml").read_text())
    except (OSError, tomllib.TOMLDecodeError):
        return {}
    config: dict = {}
    for key, value in raw.items():
        if key != "repo" and isinstance(value, dict):
            config.update(value)
        elif key != "repo":
            config[key] = value
    if repo:
        config.update(raw.get("repo", {}).get(repo, {}))
    return config


def validate_row(name: str, line: int, row: dict) -> bool:
    bad = [c for c in NUMERIC_COLUMNS if c in row and row[c] != "-" and number(row[c]) is None]
    if bad:
        print(f"{name}:{line}: not a non-negative number in {', '.join(bad)}", file=sys.stderr)
    return not bad


def read_table(name: str, columns: tuple[str, ...], enums: dict[str, set]) -> list[dict]:
    path = home() / name
    try:
        lines = path.read_text().splitlines()
    except OSError:
        return []
    reader = csv.reader(lines, delimiter="\t")
    if next(reader, None) != list(columns):
        print(f"{name}:1: header does not match {', '.join(columns)}", file=sys.stderr)
        return []
    rows = []
    for line, values in enumerate(reader, start=2):
        if len(values) != len(columns):
            print(f"{name}:{line}: {len(values)} columns, expected {len(columns)}", file=sys.stderr)
            continue
        row = dict(zip(columns, values))
        bad = [c for c, allowed in enums.items() if row[c] != "-" and row[c] not in allowed]
        if bad:
            print(f"{name}:{line}: unknown value in {', '.join(bad)}", file=sys.stderr)
            continue
        if validate_row(name, line, row):
            rows.append(row)
    return rows


def load_tables() -> tuple[list[dict], list[dict]]:
    return (read_table("dispatches.tsv", DISPATCH_COLUMNS, DISPATCH_ENUMS),
            read_table("findings.tsv", FINDING_COLUMNS, FINDING_ENUMS))


def number(value: str) -> float | None:
    # `-` is unknown, not zero: an unknown must leave every mean it appears in untouched. A negative
    # minute or token count is malformed rather than small, so it reads as unknown too.
    try:
        parsed = float(value)
    except ValueError:
        return None
    return parsed if parsed >= 0 else None


def minutes_mean(rows: list[dict]) -> float | None:
    known = [m for m in (number(d["minutes"]) for d in rows) if m is not None]
    return sum(known) / len(known) if known else None


def chapman(n1: int, n2: int, m: int) -> float:
    return (n1 + 1) * (n2 + 1) / (m + 1) - 1


def unique_blocker_dispatches(dispatches: list[dict], findings: list[dict]) -> set[str]:
    """A cause seen by exactly one review dispatch of its gate, round and candidate — what a second
    reviewer of that same candidate would have missed. Uniqueness cannot span rounds or candidates:
    rediscovering a cause later must not retroactively cancel the credit round one earned."""
    scope = {d["id"]: (d["gate_id"], d["round"], d["candidate"]) for d in dispatches
             if d["stage"] == "review"}
    holders: dict[tuple, set[str]] = {}
    for f in findings:
        if f["dispatch_id"] in scope:
            key = scope[f["dispatch_id"]] + (f["cause_id"],)
            holders.setdefault(key, set()).add(f["dispatch_id"])
    return {f["dispatch_id"] for f in findings
            if f["dispatch_id"] in scope and f["severity"] == "BLOCKER"
            and f["substantiated"] == "1"
            and len(holders[scope[f["dispatch_id"]] + (f["cause_id"],)]) == 1}


def cmd_remaining(args) -> int:
    dispatches, findings = load_tables()
    # Only substantiated findings are captures: a dismissed claim caught nothing.
    gate = [f for f in findings if f["gate_id"] == args.gate_id and f["substantiated"] == "1"]
    # An outage or a pending run is not a capture, and a plan or break dispatch is not looking for
    # the same causes; only completed reviews of one candidate can be marked against each other.
    eligible = [d for d in dispatches if d["gate_id"] == args.gate_id and d["stage"] == "review"
                and d["status"] == "final" and d["outage"] == "0"]
    latest = args.round or max((d["round"] for d in eligible), key=lambda r: number(r) or 0,
                               default="-")
    eligible = [d for d in eligible if d["round"] == latest]
    if args.candidate:
        eligible = [d for d in eligible if d["candidate"] == args.candidate]
    candidates = {d["candidate"] for d in eligible}
    if len(candidates) > 1:
        print(f"insufficient evidence: {len(candidates)} candidates in round {latest}, "
              "pass --candidate")
        return 0
    if len(eligible) > 2:  # never quietly mark the two biggest against each other
        print(f"insufficient evidence: {len(eligible)} eligible captures, expected two")
        return 0
    if len(eligible) < 2:
        print(f"insufficient evidence: {len(eligible)} eligible captures in round {latest}")
        return 0
    # An empty capture is a capture: a clean review of size 0 is evidence about the overlap.
    first, second = ({f["cause_id"] for f in gate if f["dispatch_id"] == d["id"]} for d in eligible)
    n1, n2, m = len(first), len(second), len(first & second)
    estimate = chapman(n1, n2, m)
    found = len(first | second)
    for label, value in (("round", latest), ("n1", n1), ("n2", n2), ("m", m),
                         ("chapman", f"{estimate:.3f}"), ("found", found),
                         ("remaining", f"{max(estimate - found, 0):.3f}")):
        print(f"{label} = {value}")
    if estimate > 0 and n1 and n2:
        print(f"independence ratio = {m / (n1 * n2 / estimate):.3f}")
    return 0


def precision_table(dispatches: list[dict], findings: list[dict],
                    repo: str | None = None) -> dict[tuple, tuple[int, int]]:
    family = {d["id"]: d["family"] for d in dispatches if repo is None or d["repo"] == repo}
    table: dict[tuple, list[int]] = {}
    for f in findings:
        if f["substantiated"] == "-":  # never adjudicated: it is neither a hit nor a miss
            continue
        if f["dispatch_id"] not in family:  # another repository's history, or a production row
            continue
        key = (family[f["dispatch_id"]], f["class"], f["tier"])
        counts = table.setdefault(key, [0, 0])
        counts[0] += 1
        counts[1] += f["substantiated"] == "1"
    return {key: tuple(counts) for key, counts in table.items()}


def cmd_precision(args) -> int:
    repo = None if args.all else (args.repo or default_origin())
    if repo is None and not args.all:
        # Pooling every repository is a choice, never a fallback: the stop rule that reads this
        # asks about one repository, and a foreign 0.9 would stop a review that has no history.
        print("no origin resolved: pass --repo <origin> or --all", file=sys.stderr)
        return 1
    table = precision_table(*load_tables(), repo=repo)
    print(f"repo = {repo or 'all'}")
    for key, (claimed, substantiated) in sorted(table.items()):
        posterior = (substantiated + 1) / (claimed + 2)
        print(f"{' '.join(key)} claimed={claimed} substantiated={substantiated} "
              f"precision={posterior:.3f}")
    return 0


def cmd_missed(args) -> int:
    """What each arm signed off on and production found anyway. A production cause is charged to
    every arm that approved that candidate; arms that rejected it are not on the hook."""
    dispatches, findings = load_tables()
    approved: dict[str, set[tuple]] = {}
    for d in dispatches:
        if d["verdict"] == "APPROVE":
            approved.setdefault(d["candidate"], set()).add((d["family"], d["model"]))
    missed: dict[tuple, set[str]] = {}
    for f in findings:
        if f["dispatch_id"] == "-" and f["tier"] == "production" and f["substantiated"] == "1":
            for arm in approved.get(f["candidate"], ()):
                missed.setdefault(arm, set()).add(f["cause_id"])
    for arm, causes in sorted(missed.items()):
        print(f"{' '.join(arm)} missed={len(causes)}")
    if not missed:
        print("none")
    return 0


def pin_of(arm: tuple[str, str, str]) -> str:
    """The config spelling of an arm: an unknown effort is left out, not written as `-`."""
    return ":".join(arm if arm[2] != "-" else arm[:2])


def arm_of(reviewer: str) -> tuple[str, str, str]:
    parts = reviewer.split(":")
    return (parts[0], parts[1] if len(parts) > 1 else "-", parts[2] if len(parts) > 2 else "-")


def roster_for(config: dict, role: str) -> list[str]:
    if role == "disposition":  # dispositions are reviews of findings: same list
        role = "review"
    listed = config.get(role)
    if isinstance(listed, list):
        return listed
    return config.get("reviewers", []) if role in REVIEWER_FALLBACK else []


def with_effort(arm: tuple[str, str, str], config: dict, trust: bool) -> tuple[str, str, str]:
    level = config.get("trust" if trust else "ordinary")
    return (arm[0], arm[1], level) if isinstance(level, str) else arm


def pick_arms(config: dict, dispatches: list[dict], findings: list[dict], stage: str,
              trust: bool) -> tuple[list[tuple], dict[tuple, tuple]]:
    wins = unique_blocker_dispatches(dispatches, findings)
    rows = [d for d in dispatches if d["stage"] == stage and d["status"] == "final"]
    # Arms are the role's configured list and nothing else: history says how an arm has done, never
    # that a one-off dispatch is a reviewer we may send again. An arm is the whole (family, model,
    # effort) triple, so a version change starts a fresh window.
    arms = [with_effort(arm_of(r), config, trust) for r in roster_for(config, stage)]
    overall = minutes_mean(rows)

    stats = {}
    for arm in arms:
        mine = [d for d in rows if (d["family"], d["model"], d["effort"]) == arm]
        successes = sum(1 for d in mine if d["id"] in wins)
        minutes = minutes_mean(mine)
        theta = random.betavariate(1 + successes, 1 + len(mine) - successes)
        divisor = minutes if minutes else overall if overall else 1
        stats[arm] = (successes, len(mine) - successes, minutes, theta / divisor)

    doer = config.get("doer")
    ranked = (arms if config.get("select") == "fixed"
              else sorted(arms, key=lambda a: stats[a][3], reverse=True))
    if stage not in REVIEWER_FALLBACK:  # worker and explore serve the doer; they judge nothing
        return ranked[:1], stats
    chosen = [a for a in ranked if a[0] != doer][:1]
    if trust and chosen:
        # Broad needs two families, one outside the doer's; the first arm is it, so the second only
        # has to differ from the first.
        chosen += [a for a in ranked if a[0] != chosen[0][0]][:1]
    return chosen, stats


def cmd_pick(args) -> int:
    if args.seed is not None:
        random.seed(args.seed)
    config = load_config(args.repo or default_origin())
    if not config.get("doer"):
        print("doer family unknown: set [families].doer")
        return 1
    dispatches, findings = load_tables()
    chosen, stats = pick_arms(config, dispatches, findings, args.stage, args.trust)
    for arm, (successes, failures, minutes, score) in stats.items():
        shown = "-" if minutes is None else f"{minutes:.1f}"
        print(f"arm {pin_of(arm)} s={successes} f={failures} minutes={shown} score={score:.4f}")
    for arm in chosen:
        print(f"chosen {pin_of(arm)}")
    if len(chosen) < (2 if args.trust else 1):
        missing = "a second family" if chosen else f"an arm outside {config['doer']}"
        print(f"required set unmet: the {args.stage} roster holds no {missing}")
        return 1
    return 0


def sign_test(n: int, k: int) -> tuple[float, float, float, str]:
    """Two one-sided log-likelihood ratios against the 0.75 alternative, one per arm, because a
    single ratio failing its bound says only "not A yet", never "B"."""
    below = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    above = sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n
    llr_a = k * math.log(0.75 / 0.5) + (n - k) * math.log(0.25 / 0.5)
    llr_b = (n - k) * math.log(0.75 / 0.5) + k * math.log(0.25 / 0.5)
    bound = math.log(19)
    state = ("arm A better" if llr_a > bound else
             "arm B better" if llr_b > bound else "continue")
    return min(1.0, 2 * min(below, above)), llr_a, llr_b, state


def cmd_paired(args) -> int:
    rows = list(csv.DictReader(Path(args.results).read_text().splitlines(), delimiter="\t"))
    arms = list(dict.fromkeys(row["arm"] for row in rows))
    if len(arms) != 2:
        print(f"expected two arms, found {len(arms)}")
        return 1
    results: dict[str, dict[str, str]] = {arm: {} for arm in arms}
    for row in rows:
        results[row["arm"]][row["case_id"]] = row["pass"]
    shared = set(results[arms[0]]) & set(results[arms[1]])
    known = {c for c in shared if "-" not in (results[arms[0]][c], results[arms[1]][c])}
    discordant = [c for c in known if results[arms[0]][c] != results[arms[1]][c]]
    n = len(discordant)
    k = sum(1 for c in discordant if results[arms[0]][c] == "1")
    p, llr_a, llr_b, state = sign_test(n, k)
    for label, value in (("pairs", len(shared)), ("discordant", n), (f"{arms[0]} wins", k),
                         ("sign test p", f"{p:.7g}"), ("sprt llr A", f"{llr_a:.3f}"),
                         ("sprt llr B", f"{llr_b:.3f}"), ("sprt", state)):
        print(f"{label} = {value}")
    return 0


def cmd_thresholds(args) -> int:
    dispatches, findings = load_tables()
    wins = unique_blocker_dispatches(dispatches, findings)
    groups: dict[tuple, list[dict]] = {}
    for d in dispatches:
        if d["status"] == "final":
            groups.setdefault((d["family"], d["model"]), []).append(d)

    lessons = []
    for key, rows in sorted(groups.items()):
        window, prior = rows[-20:], rows[-40:-20]
        flagged = [d for d in window if d["outage"] != "-"]  # a blank flag is not a clean run
        outage = sum(1 for d in flagged if d["outage"] == "1") / len(flagged) if flagged else None
        reviews = [d for d in window if d["stage"] == "review"]  # only reviews can catch
        blind = sum(1 for d in reviews if d["id"] not in wins)
        now, was = minutes_mean(window), minutes_mean(prior)
        print(f"{' '.join(key)} n={len(window)} "
              f"outage={'-' if outage is None else f'{outage:.2f}'} zero-blocker={blind} "
              f"minutes={'-' if now is None else f'{now:.1f}'}")
        if outage is not None and outage > OUTAGE_LIMIT:
            lessons.append(f"{' '.join(key)} outage rate {outage:.2f}")
        if blind == len(reviews) >= 5:  # one dry dispatch is noise, five is a pattern
            lessons.append(f"{' '.join(key)} found no unique blocker in {blind} dispatches")
        if now is not None and was:
            drift = (now - was) / was
            if abs(drift) > DRIFT_LIMIT:
                lessons.append(f"{' '.join(key)} minutes drifted {drift:+.0%} against the prior 20")
    for lesson in lessons:
        print(f"lesson candidate: {lesson}")
    if not lessons:
        print("none")
    return 0


def cmd_cost(args) -> int:
    config = load_config(args.repo or default_origin())
    dispatches, _ = load_tables()
    turns = None
    if args.setup == "rally":
        # Only the rival's turns are dispatches; the doer answers inline, on this side of the wire.
        turns = int(config.get("rally_turns", DEFAULT_RALLY_TURNS))
        count = math.ceil(turns / 2)
    elif args.setup in SETUP_DISPATCHES:
        count = SETUP_DISPATCHES[args.setup]
    else:
        print("unknown setup")
        return 1
    if args.trust:
        count = max(count, SETUP_DISPATCHES["broad"])  # trust-touching is Broad whatever was asked
    minutes = minutes_mean([d for d in dispatches
                            if d["setup"] == args.setup and d["status"] == "final"])
    if turns is not None:
        print(f"turns = {turns}")
    print(f"dispatches = {count}")
    print(f"mean minutes = {'-' if minutes is None else f'{minutes:.1f}'}")
    print(f"expected minutes = {'-' if minutes is None else f'{count * minutes:.1f}'}")
    return 0


def cmd_schema(args) -> int:
    print("dispatches.tsv: " + "\t".join(DISPATCH_COLUMNS))
    print("findings.tsv: " + "\t".join(FINDING_COLUMNS))
    for table, enums in (("dispatches.tsv", DISPATCH_ENUMS), ("findings.tsv", FINDING_ENUMS)):
        for column, allowed in sorted(enums.items()):
            print(f"{table} {column} = {', '.join(sorted(allowed))} or -")
    return 0


CONFIG_FIXTURE = """\
[families]
doer = "anthropic"
reviewers = ["openai:gpt-6-astra:high", "google:gemini-3.1-pro-high"]
[bounds]
review_rounds = 3
rally_turns = 10
[repo."github.com/askrubberduck/skills"]
review_rounds = 2
"""
DISPATCH_FIXTURE = [
    "d1\tg1\t1\t2026-09-01\tr\treview\tindependent\t1\tc1\tanthropic\tclaude-opus-5\thigh\t12\t900\tREJECT\tfinal\t0",
    "d2\tg1\t1\t2026-09-01\tr\treview\tindependent\t1\tc1\topenai\tgpt-6-astra\thigh\t20\t800\tREJECT\tfinal\t0",
    "d3\tg2\t1\t2026-09-02\tr\treview\tindependent\t1\tc2\tanthropic\tclaude-opus-5\thigh\t-\t700\tREJECT\tfinal\t0",
    "d4\tg2\t1\t2026-09-02\tr\treview\tindependent\t1\tc2\tgoogle\tgemini-3.1-pro-high\t-\t30\t600\tNOTE\tfinal\t0",
    "d5\tg3\t1\t2026-09-03\tr\treview\tbroad\t0\tc3\tanthropic\tclaude-opus-5\thigh\t10\t500\tAPPROVE\tfinal\t0",
    "d6\tg3\t2\t2026-09-03\tr\treview\tbroad\t0\tc3\topenai\tgpt-6-astra\thigh\t25\t400\t-\tpending\t0",
    "d7\tg4\t1\t2026-09-04\tr\treview\tindependent\t1\tc4\tanthropic\tclaude-opus-5\thigh\t8\t300\tREJECT\tfinal\t0",
    "d8\tg4\t1\t2026-09-04\tr\treview\tindependent\t1\tc4\topenai\tgpt-6-astra\thigh\t9\t300\tAPPROVE\tfinal\t0",
    "d9\tg5\t1\t2026-09-05\tr\treview\tbroad\t1\tc5\topenai\tgpt-6-astra\thigh\t9\t-\tREJECT\tfinal\t0",
    "d10\tg5\t1\t2026-09-05\tr\treview\tbroad\t1\tc5\tgoogle\tgemini-3.1-pro-high\thigh\t5\t-\tREJECT\tfinal\t0",
    "d11\tg5\t1\t2026-09-05\tr\tdisposition\tbroad\t1\tc5\tgoogle\tgemini-3.1-pro-high\thigh\t2\t-\tNOTE\tfinal\t0",
    "d12\tg5\t1\t2026-09-05\tr\tdisposition\tbroad\t1\tc5\topenai\tgpt-6-astra\thigh\t3\t-\tNOTE\tfinal\t0",
    "d13\tg6\t1\t2026-09-06\telsewhere\treview\tindependent\t0\tc6\topenai\tgpt-6-astra\thigh\t4\t-\tAPPROVE\tfinal\t0",
]
FINDING_FIXTURE = [
    "d1\tg1\tc1\ta1\tcorrectness\texecuted\tBLOCKER\t1\thuman",
    "d1\tg1\tc1\ta2\tcorrectness\texecuted\tSHOULD\t1\thuman",
    "d1\tg1\tc1\ta3\tstyle\tread\tNOTE\t0\t-",
    "d2\tg1\tc1\ta2\tcorrectness\tstatic\tSHOULD\t1\thuman",
    "d2\tg1\tc1\tb1\tstyle\tread\tNOTE\t1\thuman",
    "d3\tg2\tc2\tc1\tcorrectness\texecuted\tBLOCKER\t1\thuman",
    "d3\tg2\tc2\tc2\tcorrectness\texecuted\tNOTE\t-\t-",
    "d4\tg2\tc2\tc3\tcorrectness\tstatic\tBLOCKER\t0\thuman",
    "d4\tg2\tc2\tc4\tperf\tstatic\tSHOULD\t1\thuman",
    "d5\tg3\tc3\te1\tstyle\tread\tNOTE\t1\thuman",
    "d5\tg3\tc3\te2\tstyle\tread\tNOTE\t0\t-",
    "d6\tg3\tc3\te3\tcorrectness\tstatic\tBLOCKER\t1\thuman",
    "d7\tg4\tc4\tf1\tcorrectness\texecuted\tBLOCKER\t1\thuman",
    "-\tg3\tc3\te4\tcorrectness\tproduction\tBLOCKER\t1\towner",
    "-\tg1\tc1\ta9\tcorrectness\tproduction\tBLOCKER\t1\towner",
    "d9\tg5\tc5\th1\tcorrectness\texecuted\tSHOULD\t1\tgoogle",
    "d10\tg5\tc5\th1\tcorrectness\tstatic\tSHOULD\t1\topenai",
    "d10\tg5\tc5\th2\tstyle\tread\tNOTE\t1\topenai",
    "-\tg4\tc4\tp9\tcorrectness\tproduction\tBLOCKER\t0\towner",
    "d13\tg6\tc6\tz1\tcorrectness\texecuted\tSHOULD\t1\thuman",
]


def run(argv: list[str]) -> tuple[int, str]:
    with contextlib.redirect_stdout(io.StringIO()) as out:
        code = main(argv)
    return code, out.getvalue()


ROLES_CONFIG = """\
[families]
doer = "anthropic"
reviewers = ["openai:gpt-6-astra:high", "google:gemini-3.1-pro-high"]
[models]
race = ["google:gemini-3.8-flash-high"]
worker = ["anthropic:claude-sonnet-5:medium"]
[effort]
trust = "xhigh"
"""
ROLES_DISPATCHES = [
    "s1\tg7\t1\t2026-09-07\tr\treview\tbroad\t1\tc7\topenai\tgpt-6-astra\thigh\t5\t-\tREJECT\tfinal\t0",
    "s2\tg7\t1\t2026-09-07\tr\treview\tbroad\t1\tc7\tgoogle\tgemini-3.1-pro-high\t-\t4\t-\tAPPROVE\tfinal\t0",
    "s8\tg9\t1\t2026-09-09\tr\treview\tbroad\t1\tc9\topenai\tgpt-6-astra\txhigh\t5\t-\tREJECT\tfinal\t0",
]
ROLES_FINDINGS = [
    "s1\tg7\tc7\tk1\tcorrectness\tread\tBLOCKER\t1\thuman",
    "s8\tg9\tc9\tk9\tcorrectness\tread\tBLOCKER\t1\thuman",
]


def roles_check(root: Path) -> None:
    """Role lists, their fallback, fixed order, effort by risk, and who may judge."""
    (root / "config.toml").write_text(ROLES_CONFIG)
    for name, columns, fixture in (("dispatches.tsv", DISPATCH_COLUMNS, ROLES_DISPATCHES),
                                   ("findings.tsv", FINDING_COLUMNS, ROLES_FINDINGS)):
        (root / name).write_text("\t".join(columns) + "\n" + "\n".join(fixture) + "\n")
    config = load_config()
    assert roster_for(config, "race") == ["google:gemini-3.8-flash-high"]
    assert roster_for(config, "plan") == config["reviewers"]  # unset reviewer-side role falls back
    assert roster_for(config, "explore") == []  # the host chooses
    assert roster_for(dict(config, review=["x:y:z"]), "disposition") == ["x:y:z"]
    assert roster_for(dict(config, review=[]), "review") == []  # an explicit empty list stays empty
    assert with_effort(("openai", "m", "high"), config, trust=True) == ("openai", "m", "xhigh")
    assert with_effort(("openai", "m", "high"), config, trust=False) == ("openai", "m", "high")
    dispatches, findings = load_tables()
    fixed = dict(config, select="fixed")
    for seed in range(10):
        random.seed(seed)
        chosen, _ = pick_arms(fixed, dispatches, findings, "review", trust=True)
        assert chosen == [with_effort(arm_of(p), config, True) for p in config["reviewers"]], chosen
    # a trust pick is the xhigh arm, and its history is the xhigh rows it writes (s8), not high's
    _, stats = pick_arms(config, dispatches, findings, "review", trust=True)
    assert stats[("openai", "gpt-6-astra", "xhigh")][:2] == (1, 0), stats
    # workers serve the doer and may share its family; judges may not
    assert pick_arms(config, [], [], "worker", trust=True)[0] == [
        ("anthropic", "claude-sonnet-5", "xhigh")]
    own = {"doer": "anthropic", "review": ["anthropic:claude-x:high"]}
    assert pick_arms(own, [], [], "review", trust=False)[0] == []
    assert pin_of(("google", "gemini-3.1-pro-high", "-")) == "google:gemini-3.1-pro-high"
    for argv, wanted in ((["pick", "race", "--repo", "r"], "chosen google:gemini-3.8-flash-high\n"),
                         (["pick", "review", "--trust", "--repo", "r"],
                          "chosen openai:gpt-6-astra:xhigh")):
        code, out = run(argv)
        assert code == 0 and wanted in out, (argv, out)


def self_check() -> int:
    with tempfile.TemporaryDirectory(prefix="askrubberduck-ledger-") as directory:
        root = Path(directory)
        os.environ["ASKRUBBERDUCK_HOME"] = str(root)
        (root / "config.toml").write_text(CONFIG_FIXTURE)
        for name, columns, fixture in (("dispatches.tsv", DISPATCH_COLUMNS, DISPATCH_FIXTURE),
                                       ("findings.tsv", FINDING_COLUMNS, FINDING_FIXTURE)):
            (root / name).write_text("\t".join(columns) + "\n" + "\n".join(fixture) + "\n")
            assert all(len(line) < 4096 for line in (root / name).read_text().splitlines())
        repo = ["--repo", "github.com/askrubberduck/skills"]

        assert round(chapman(10, 7, 6), 3) == 11.571 and chapman(4, 4, 4) == 4.0
        assert normalize_origin("git@github.com:askrubberduck/skills.git") == \
            normalize_origin("https://github.com/askrubberduck/skills.git") == repo[1]
        assert load_config()["review_rounds"] == 3 and load_config(repo[1])["review_rounds"] == 2

        dispatches, findings = load_tables()
        assert len(dispatches) == 13 and len(findings) == 20
        assert number("-3") is None and number("3") == 3.0
        with contextlib.redirect_stderr(io.StringIO()) as complaint:
            assert not validate_row("t", 2, {"minutes": "-4", "round": "1", "tokens": "-"})
        assert complaint.getvalue() == "t:2: not a non-negative number in minutes\n", complaint
        assert max(["2", "10"], key=lambda r: number(r) or 0) == "10"

        # d3's c2 is `-`: an unadjudicated claim is neither a hit nor a miss, so it never counts.
        assert precision_table(dispatches, findings)[("anthropic", "correctness", "executed")] == (4, 4)
        # foreign history stays foreign: repo "r" never sees the elsewhere row
        key = ("openai", "correctness", "executed")
        assert precision_table(dispatches, findings)[key] == (2, 2)
        assert precision_table(dispatches, findings, "r")[key] == (1, 1)
        assert precision_table(dispatches, findings, "elsewhere")[key] == (1, 1)

        wins = unique_blocker_dispatches(dispatches, findings)
        assert wins == {"d1", "d3", "d6", "d7"}, wins
        rediscovery = dispatches + [dict(dispatches[0], id="d9", round="2", candidate="c1b")]
        rediscovery_f = findings + [dict(findings[0], dispatch_id="d9", candidate="c1b")]
        again = unique_blocker_dispatches(rediscovery, rediscovery_f)
        assert {"d1", "d9"} <= again, again  # round two cannot cancel round one's credit

        config = load_config()
        for seed in range(20):
            random.seed(seed)
            chosen, stats = pick_arms(config, dispatches, findings, "review", trust=True)
            assert len(chosen) == 2, chosen
            assert chosen[0][0] != "anthropic" and chosen[0][0] != chosen[1][0], chosen
        assert ("anthropic", "claude-opus-5", "high") not in stats, stats  # history is not a roster
        assert stats[("openai", "gpt-6-astra", "high")][:3] == (0, 4, 10.5), stats
        unmet, _ = pick_arms({"doer": "openai", "reviewers": ["openai:gpt-6-astra:high"]},
                             dispatches, findings, "review", trust=False)
        assert unmet == [], unmet

        assert sign_test(22, 11)[3] == "continue", sign_test(22, 11)
        assert sign_test(8, 8)[3] == "arm A better", sign_test(8, 8)
        assert sign_test(8, 0)[3] == "arm B better", sign_test(8, 0)
        assert sign_test(8, 8)[0] == 0.0078125
        results = root / "results.tsv"
        results.write_text("case_id\tarm\tpass\n" + "".join(
            f"k{i}\tA\t1\nk{i}\tB\t0\n" for i in range(8)) + "k9\tA\t-\nk9\tB\t0\n")

        # d8 of g4 caught nothing and is still a capture; g3's round 2 has only pending d6.
        os.chdir(root)  # no checkout here, so no origin resolves: pooling must be asked for
        with contextlib.redirect_stderr(io.StringIO()) as err:
            code, out = run(["precision"])
        assert code == 1 and "no origin resolved" in err.getvalue(), (code, out)
        for argv, expected, wanted in (
                (["remaining", "g1"], 0, ["remaining = 0.500"]),
                (["remaining", "g4"], 0, ["n2 = 0", "remaining = 0.000"]),
                (["remaining", "g3"], 0, ["insufficient evidence: 1 eligible captures"]),
                (["precision", "--repo", "r"], 0, ["anthropic correctness executed claimed=4"]),
                (["missed"], 0, ["anthropic claude-opus-5 missed=1"]),  # the c4 production row is unsubstantiated: openai is not charged
                (["remaining", "g5"], 0, ["n1 = 1", "n2 = 2", "m = 1", "remaining = 0.000"]),  # two dispositions present, not captures
                (["pick", "review", "--trust", "--seed", "1", *repo], 0,
                 ["chosen openai:gpt-6-astra:high", "chosen google:gemini-3.1-pro-high\n"]),
                (["paired", str(results)], 0, ["discordant = 8", "sprt = arm A better"]),
                (["thresholds"], 0, ["anthropic claude-opus-5 n=4"]),
                (["cost", "broad", *repo], 0, ["dispatches = 4"]),
                (["cost", "rally", *repo], 0, ["turns = 10", "dispatches = 5"]),
                (["cost", "independent", "--trust", *repo], 0, ["dispatches = 4"]),  # trust is Broad whatever was asked
                (["cost", "sideways", *repo], 1, ["unknown setup"]),
                (["schema"], 0, ["candidate", "CONCUR"])):
            code, out = run(argv)
            assert code == expected, (argv, code, out)
            assert all(want in out for want in wanted), (argv, out)
        roles_check(root)
    print("ledger self-check passed")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--self-check", action="store_true", help="run against a fixture home")
    subparsers = parser.add_subparsers(dest="command")
    remaining = subparsers.add_parser("remaining", help="Chapman estimate of uncaught findings")
    remaining.add_argument("gate_id")
    remaining.add_argument("--round", help="default: the gate's latest round")
    remaining.add_argument("--candidate", help="default: the round's only candidate")
    remaining.set_defaults(run=cmd_remaining)
    precision = subparsers.add_parser("precision",
                                      help="substantiation rate per family, class and tier")
    precision.add_argument("--repo", help="default: this checkout's origin")
    precision.add_argument("--all", action="store_true", help="pool every repository")
    precision.set_defaults(run=cmd_precision)
    subparsers.add_parser("missed", help="production causes per arm that approved the candidate"
                          ).set_defaults(run=cmd_missed)
    pick = subparsers.add_parser("pick", help="Thompson-sample the next arm for a stage")
    pick.add_argument("stage")
    pick.add_argument("--trust", action="store_true")
    pick.add_argument("--seed", type=int)
    pick.add_argument("--repo", help="default: this checkout's origin")
    pick.set_defaults(run=cmd_pick)
    paired = subparsers.add_parser("paired", help="sign test and SPRT over a paired trial")
    paired.add_argument("results")
    paired.set_defaults(run=cmd_paired)
    subparsers.add_parser("thresholds", help="drift and outage flags worth a lesson"
                          ).set_defaults(run=cmd_thresholds)
    cost = subparsers.add_parser("cost", help="expected dispatches and minutes for a setup")
    cost.add_argument("setup")
    cost.add_argument("--trust", action="store_true")
    cost.add_argument("--repo", help="default: this checkout's origin")
    cost.set_defaults(run=cmd_cost)
    subparsers.add_parser("schema", help="the ledger's columns and enum domains"
                          ).set_defaults(run=cmd_schema)

    args = parser.parse_args(argv)
    if args.self_check:
        return self_check()
    if not args.command:
        parser.print_help()
        return 1
    return args.run(args)


if __name__ == "__main__":
    raise SystemExit(main())
