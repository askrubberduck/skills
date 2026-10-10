#!/usr/bin/env python3
"""Read the dispatch ledger under ~/.askrubberduck/ and answer the questions a gate asks between
rounds: how many findings a capture is still missing, which reviewer arm to send next, whether a
paired trial has separated yet, and what a setup costs. Every number here is an estimate over rows
somebody wrote down; this script never judges the work, only counts what the ledger says about it.
Stdlib only, for the same reason the distribution gate is: no install step anywhere it runs.
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import random
import subprocess
import sys
import tomllib
from pathlib import Path

DISPATCH_COLUMNS = ("id", "gate_id", "round", "date", "repo", "stage", "setup", "trust",
                    "candidate", "family", "model", "effort", "minutes", "tokens", "verdict",
                    "status", "outage")
FINDING_COLUMNS = ("dispatch_id", "gate_id", "candidate", "cause_id", "class", "tier", "severity",
                   "substantiated", "adjudicated_by")
DISPATCH_ENUMS = {
    # `disposition` is Broad's cross-family adjudication call: a dispatch, never a capture.
    "stage": {"review", "disposition", "plan", "proof", "break", "race", "rally", "roast"},
    # `shadow`: a pin on trial riding along as an extra reviewer that never counts toward the gate.
    "setup": {"self-check", "independent", "broad", "race", "rally", "shadow"},
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
DEFAULT_SHADOW = 3
# Judging roles draw on the reviewer roster when unset and must come from a family other than the
# doer's; worker and explore serve the doer and fall back to the host.
JUDGING_ROLES = {"review", "disposition", "race", "plan"}
# Trust-touching review is Broad: two families. A race or plan still takes one rival.
BROAD_ROLES = {"review", "disposition"}
# Host model ids carry no family field; their prefix names the vendor.
FAMILY_PREFIXES = (("gemini", "google"), ("claude", "anthropic"), ("gpt", "openai"))
OUTAGE_LIMIT = 0.2
DRIFT_LIMIT = 0.5


def home() -> Path:
    return Path(os.environ.get("ASKRUBBERDUCK_HOME") or "~/.askrubberduck").expanduser()


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
        # rows end only at a newline: splitlines would also break at U+2028 and its kin in a field
        lines = path.read_text(encoding="utf-8").removesuffix("\n").split("\n")
    except FileNotFoundError:
        if path.is_symlink() or home().is_symlink():  # dangling: configured, not absent
            raise SystemExit(f"{path}: dangling symlink")
        if name == "dispatches.tsv":
            print(f"{path}: no dispatch recorded yet", file=sys.stderr)
        return []  # no findings.tsv is a clean history
    except OSError as error:
        raise SystemExit(f"{path}: {error.strerror}")  # an unread table is no answer, not an empty one
    except UnicodeDecodeError as error:
        raise SystemExit(f"{path}: not UTF-8 ({error.reason} at byte {error.start})")
    reader = csv.reader(lines, delimiter="\t", quoting=csv.QUOTE_NONE)  # written unquoted: a " is text
    if next(reader, None) != list(columns):
        raise SystemExit(f"{path}:1: header does not match {', '.join(columns)}")
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
    rediscovering a cause later must not retroactively cancel the credit round one earned. Only
    counted reviewers can take credit from a counted reviewer: a shadow finding the same cause takes
    none away. A shadow competes with everyone, other shadows included, so two trials that find one
    cause both go without."""
    scope = {d["id"]: (d["repo"], d["gate_id"], d["round"], d["candidate"]) for d in dispatches
             if d["stage"] == "review"}
    shadows = {d["id"] for d in dispatches if d["setup"] == "shadow"}
    holders: dict[tuple, set[str]] = {}
    for f in findings:
        if f["dispatch_id"] in scope and f["substantiated"] == "1":  # a dismissed claim held nothing
            key = scope[f["dispatch_id"]] + (f["cause_id"],)
            holders.setdefault(key, set()).add(f["dispatch_id"])

    def rivals(f: dict) -> set[str]:
        others = holders[scope[f["dispatch_id"]] + (f["cause_id"],)] - {f["dispatch_id"]}
        return others if f["dispatch_id"] in shadows else others - shadows

    return {f["dispatch_id"] for f in findings
            if f["dispatch_id"] in scope and f["severity"] == "BLOCKER"
            and f["substantiated"] == "1" and not rivals(f)}


def cmd_remaining(args) -> int:
    repo = args.repo or default_origin()
    if repo is None:  # a gate id names a gate only within its repository
        print("no origin resolved: pass --repo <origin>", file=sys.stderr)
        return 1
    dispatches, findings = load_tables()
    # Only substantiated findings are captures: a dismissed claim caught nothing.
    gate = [f for f in findings if f["gate_id"] == args.gate_id and f["substantiated"] == "1"]
    # An outage or a pending run is not a capture, and a plan or break dispatch is not looking for
    # the same causes; only completed reviews of one candidate can be marked against each other.
    eligible = [d for d in dispatches if d["repo"] == repo and d["gate_id"] == args.gate_id
                and d["stage"] == "review"
                and d["status"] == "final" and d["outage"] == "0" and d["setup"] != "shadow"]
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
    first, second = ({f["cause_id"] for f in gate if f["dispatch_id"] == d["id"]} for d in eligible)
    n1, n2, m = len(first), len(second), len(first & second)
    if not n1 or not n2:
        print(f"insufficient evidence: empty capture (n1 = {n1}, n2 = {n2})")
        return 0
    estimate = chapman(n1, n2, m)
    found = len(first | second)
    for label, value in (("round", latest), ("n1", n1), ("n2", n2), ("m", m),
                         ("chapman", f"{estimate:.3f}"), ("found", found),
                         ("remaining", f"{max(estimate - found, 0):.3f}")):
        print(f"{label} = {value}")
    print("advisory estimate: correlated reviewers can share blind spots")
    if estimate > 0:
        print(f"independence ratio = {m / (n1 * n2 / estimate):.3f}")
    return 0


def precision_table(dispatches: list[dict], findings: list[dict],
                    repo: str | None = None) -> dict[tuple, tuple[int, int]]:
    # a shadow's record is its own trial's business: it never vouches for its family at a gate
    family = {d["id"]: d["family"] for d in dispatches
              if (repo is None or d["repo"] == repo) and d["stage"] == "review"
              and d["setup"] != "shadow"}
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
    return config.get("reviewers", []) if role in JUDGING_ROLES else []


def with_effort(arm: tuple[str, str, str], config: dict, trust: bool) -> tuple[str, str, str]:
    level = config.get("trust" if trust else "ordinary")
    return (arm[0], arm[1], level) if isinstance(level, str) else arm


def pick_arms(config: dict, dispatches: list[dict], findings: list[dict], stage: str,
              trust: bool) -> tuple[list[tuple], dict[tuple, tuple]]:
    adaptive = config.get("select", "fixed") == "adaptive" and stage == "review"
    wins = unique_blocker_dispatches(dispatches, findings) if stage == "review" else set()
    rows = [d for d in dispatches if d["stage"] == stage and d["status"] == "final"]
    # Arms are the role's configured list and nothing else: history says how an arm has done, never
    # that a one-off dispatch is a reviewer we may send again. An arm is the whole (family, model,
    # effort) triple, so a version change starts a fresh window.
    # a pin on trial never counts toward a review, whatever list also names it; trials are reviews
    on_trial = ({arm_of(p)[:2] for p in config.get("trial", [])}
                if stage in BROAD_ROLES else set())
    arms = [with_effort(arm_of(r), config, trust) for r in roster_for(config, stage)
            if arm_of(r)[:2] not in on_trial]
    overall = minutes_mean(rows)

    stats = {}
    for arm in arms if stage == "review" else []:
        mine = [d for d in rows if (d["family"], d["model"], d["effort"]) == arm]
        successes = sum(1 for d in mine if d["id"] in wins)
        minutes = minutes_mean(mine)
        theta = random.betavariate(1 + successes, 1 + len(mine) - successes) if adaptive else 0
        divisor = minutes if minutes else overall if overall else 1
        stats[arm] = (successes, len(mine) - successes, minutes, theta / divisor)

    doer = config.get("doer")
    ranked = sorted(arms, key=lambda a: stats[a][3], reverse=True) if adaptive else arms
    if stage not in JUDGING_ROLES:  # worker and explore serve the doer; they judge nothing
        return ranked[:1], stats
    chosen = [a for a in ranked if a[0] != doer][:1]
    if trust and chosen and stage in BROAD_ROLES:
        # Broad needs two families, one outside the doer's; the first arm is it, so the second only
        # has to differ from the first.
        chosen += [a for a in ranked if a[0] != chosen[0][0]][:1]
    return chosen, stats


def cmd_pick(args) -> int:
    config = load_config(args.repo or default_origin())
    if not config.get("doer"):
        print("doer family unknown: set [families].doer")
        return 1
    dispatches, findings = load_tables()
    chosen, stats = pick_arms(config, dispatches, findings, args.stage, args.trust)
    adaptive = config.get("select", "fixed") == "adaptive" and args.stage == "review"
    print(f"selection = {'adaptive' if adaptive else 'fixed'}")
    for arm, (successes, failures, minutes, score) in stats.items():
        shown = "-" if minutes is None else f"{minutes:.1f}"
        print(f"arm {pin_of(arm)} s={successes} f={failures} minutes={shown} score={score:.4f}")
    for arm in chosen:
        print(f"chosen {pin_of(arm)}")
    if args.stage == "review":
        for pin, reason in shadow_status(config, dispatches, findings):
            print(f"shadow {pin_of(with_effort(arm_of(pin), config, args.trust))} {reason}")
    if len(chosen) < (2 if args.trust and args.stage in BROAD_ROLES else 1):
        missing = ("a second family" if chosen
                   else f"an arm outside {config['doer']}" if args.stage in JUDGING_ROLES
                   else "any arm")
        print(f"required set unmet: the {args.stage} roster holds no {missing}")
        return 1
    return 0


def shadow_rows(dispatches: list[dict], pin: str) -> list[dict]:
    """Final shadow reviews of a pin whose outage flag is known; an unknown flag is neither a clean
    run nor an outage, so the row does not count toward a trial either way."""
    family, model, _ = arm_of(pin)  # effort may be overridden by risk, so it does not identify
    return [d for d in dispatches if d["stage"] == "review" and d["setup"] == "shadow"
            and d["status"] == "final"
            and d["outage"] in ("0", "1") and (d["family"], d["model"]) == (family, model)]


def trial_verdict(config: dict, dispatches: list[dict], findings: list[dict],
                  pin: str) -> tuple[str, str, list[tuple[str, str]]]:
    """(verdict, reason, missed) for a trial pin: `shadow` while it still rides along, then
    `replace`, `add` or `drop`; missed holds the (severity, cause_id) pairs the trial missed on
    its shared gates. A trial that
    cannot decide keeps riding up to twice its shadow count, then drops, so no pin sits in `trial`
    forever and blocks its family's next model."""
    needed = int(config.get("shadow", DEFAULT_SHADOW))
    family = arm_of(pin)[0]
    on_trial = {arm_of(p)[:2] for p in config.get("trial", [])}
    incumbent = next((arm for arm in map(arm_of, roster_for(config, "review"))
                      if arm[0] == family and arm[:2] not in on_trial), None)
    # a gate id names a gate within its repository; "pr43" recurs across repositories
    gate = lambda d: (d["repo"], d["gate_id"], d["round"], d["candidate"])
    theirs = {gate(d): d for d in dispatches
              if incumbent and d["stage"] == "review" and d["status"] == "final"
              and d["setup"] != "shadow"
              and d["outage"] == "0"  # an incumbent that never answered, or may not have, is no baseline
              and (d["family"], d["model"]) == incumbent[:2]}
    by_gate: dict[str, dict] = {}
    for d in shadow_rows(dispatches, pin):  # a gate counts once: its round with a baseline if any
        kept = by_gate.get((d["repo"], d["gate_id"]))
        if kept is None or (gate(d) in theirs and gate(kept) not in theirs):
            by_gate[(d["repo"], d["gate_id"])] = d
    rows = list(by_gate.values())[:2 * needed]
    counted = {(d["repo"], d["gate_id"]) for d in rows}  # any round of a counted gate
    distinct: dict[str, set[str]] = {}  # a cause recorded twice is still one cause
    for f in findings:
        if f["substantiated"] == "1":
            distinct.setdefault(f["dispatch_id"], set()).add(f["cause_id"])
    shared = [d for d in rows if gate(d) in theirs]
    # the sum ignores severity: whoever applies the verdict sees what the trial missed so far
    rank = {"BLOCKER": 0, "SHOULD": 1, "NOTE": 2}
    known = lambda f: f.get("severity") if f.get("severity") in rank else "-"  # unknown sorts last
    missed = [(severity, cause) for _, severity, cause in sorted(
        {(rank.get(known(f), 3), known(f), f["cause_id"]) for d in shared
         for f in findings if f["dispatch_id"] == theirs[gate(d)]["id"]
         and f["substantiated"] == "1"
         and f["cause_id"] not in distinct.get(d["id"], set())})]
    if any(d["outage"] == "1" for d in shadow_rows(dispatches, pin)
           if (d["repo"], d["gate_id"]) in counted):
        return "drop", "outage on a shadow gate", missed
    if len(rows) < needed:
        return "shadow", f"{len(rows)}/{needed}", missed
    caught = {ident: len(found) for ident, found in distinct.items()}
    undecided = "drop" if len(rows) >= 2 * needed else "shadow"
    if incumbent is None:
        if sum(caught.get(d["id"], 0) for d in rows):
            return "add", "no reviewer of its family; it substantiated a cause", missed
        return undecided, "no substantiated cause yet", missed
    # ponytail: "not worse on the shared gates" by summed substantiated causes; three gates cannot
    # reach significance, so this only keeps out a clearly worse model. `paired` over more gates is
    # the upgrade.
    own = sum(caught.get(d["id"], 0) for d in shared)
    found = sum(caught.get(theirs[gate(d)]["id"], 0) for d in shared)
    if len(shared) < needed or not (own or found):
        # too few gates beside the incumbent, or all clean: nothing says which model is better
        return undecided, f"{len(shared)} shared gates, {own} vs {found} causes", missed
    if own >= found:
        return "replace", pin_of(incumbent), missed
    return "drop", f"{own} vs {found} causes on shared gates", missed

def shadow_status(config: dict, dispatches: list[dict],
                  findings: list[dict]) -> list[tuple[str, str]]:
    return [(pin, reason) for pin in config.get("trial", [])
            for verdict, reason, _ in [trial_verdict(config, dispatches, findings, pin)]
            if verdict == "shadow"]


def family_of(model: str) -> str | None:
    return next((family for prefix, family in FAMILY_PREFIXES if model.startswith(prefix)), None)


def cmd_roster(args) -> int:
    """Host model ids nobody has configured, trialled or dispatched yet: the new-model signal."""
    config = load_config(args.repo or default_origin())
    dispatches, _ = load_tables()
    known = {d["model"] for d in dispatches}
    for value in config.values():
        if isinstance(value, list):
            known |= {arm_of(pin)[1] for pin in value if isinstance(pin, str) and ":" in pin}
    source = sys.stdin if args.models == "-" else open(args.models)
    new = []
    for line in source:
        model = line.split()[0] if line.split() else ""
        family = family_of(model)
        if family and model not in known:
            new.append(f"{family}:{model}")
    for arm in new:
        print(f"new {arm}")
    if not new:
        print("none")
    return 0


def cmd_promote(args) -> int:
    """One line per trial pin: keep riding, replace its family's reviewer, join the review list,
    or leave the trial."""
    config = load_config(args.repo or default_origin())
    dispatches, findings = load_tables()
    for pin in config.get("trial", []):
        verdict, reason, missed = trial_verdict(config, dispatches, findings, pin)
        if verdict == "replace":
            print(f"replace {reason} with {pin} in review")
            for severity, cause in missed:
                print(f"  missed {severity} {cause}")
        elif verdict == "add":
            print(f"add {pin} to review")
        else:
            print(f"{verdict} {pin}: {reason}")
    if not config.get("trial"):
        print("none")
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
    dispatches, findings = load_tables()
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
    if args.setup in ("independent", "broad"):
        riding = len(shadow_status(config, dispatches, findings))
        if riding:
            print(f"shadow dispatches = {riding}")
            count += riding
    # A roast shares the independent setup but critiques the whole solution: not a review's price.
    minutes = minutes_mean([d for d in dispatches if d["setup"] == args.setup
                            and d["stage"] != "roast" and d["status"] == "final"])
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    subparsers = parser.add_subparsers(dest="command")
    remaining = subparsers.add_parser("remaining", help="Chapman estimate of uncaught findings")
    remaining.add_argument("gate_id")
    remaining.add_argument("--round", help="default: the gate's latest round")
    remaining.add_argument("--candidate", help="default: the round's only candidate")
    remaining.add_argument("--repo", help="default: this checkout's origin")
    remaining.set_defaults(run=cmd_remaining)
    precision = subparsers.add_parser("precision",
                                      help="substantiation rate per family, class and tier")
    precision.add_argument("--repo", help="default: this checkout's origin")
    precision.add_argument("--all", action="store_true", help="pool every repository")
    precision.set_defaults(run=cmd_precision)
    subparsers.add_parser("missed", help="production causes per arm that approved the candidate"
                          ).set_defaults(run=cmd_missed)
    pick = subparsers.add_parser("pick", help="pick in list order; opt-in adaptive review ranking")
    pick.add_argument("stage")
    pick.add_argument("--trust", action="store_true")
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
    roster = subparsers.add_parser("roster", help="host model ids not yet configured or tried")
    roster.add_argument("models", help="file of host model ids, one per line, or - for stdin")
    roster.add_argument("--repo", help="default: this checkout's origin")
    roster.set_defaults(run=cmd_roster)
    promote = subparsers.add_parser("promote", help="verdict for each trial pin past its shadow")
    promote.add_argument("--repo", help="default: this checkout's origin")
    promote.set_defaults(run=cmd_promote)

    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 1
    return args.run(args)


if __name__ == "__main__":
    raise SystemExit(main())
