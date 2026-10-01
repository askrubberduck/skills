#!/usr/bin/env python3
"""ledger.py against fixture homes: the arithmetic, the trial rules, and every reader command.
Run: python3 tests/test_ledger.py"""

from __future__ import annotations

import contextlib
import io
import os
import random
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ inside the shipped skill
SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "duck-review" / "scripts"
LEDGER = SCRIPTS / "ledger.py"
sys.path.insert(0, str(SCRIPTS))
# a seeded Thompson draw: a reader's output compares equal across runs
SEEDED = (f"import random, sys; random.seed(1); sys.path.insert(0, {str(SCRIPTS)!r}); "
          "import ledger; raise SystemExit(ledger.main(sys.argv[1:]))")
from ledger import (DEFAULT_SHADOW, DISPATCH_COLUMNS, FINDING_COLUMNS, arm_of,  # noqa: E402
                    chapman, load_config, load_tables, main, normalize_origin, number, pick_arms,
                    pin_of, precision_table, roster_for, sign_test, trial_verdict,
                    unique_blocker_dispatches, validate_row, with_effort)

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
[learn]
shadow = 1
trial = ["openai:gpt-6-sol:high", "anthropic:claude-x:high", "google:gemini-9-pro:high",
         "openai:gpt-6-nova:high", "google:gemini-3.8-flash-high"]
"""
ROLES_DISPATCHES = [
    "s1\tg7\t1\t2026-09-07\tr\treview\tbroad\t1\tc7\topenai\tgpt-6-astra\thigh\t5\t-\tREJECT\tfinal\t0",
    "s2\tg7\t1\t2026-09-07\tr\treview\tbroad\t1\tc7\tgoogle\tgemini-3.1-pro-high\t-\t4\t-\tAPPROVE\tfinal\t0",
    "s3\tg7\t1\t2026-09-07\tr\treview\tshadow\t1\tc7\topenai\tgpt-6-sol\thigh\t6\t-\tREJECT\tfinal\t0",
    "s4\tg7\t1\t2026-09-07\tr\treview\tshadow\t1\tc7\tanthropic\tclaude-x\thigh\t6\t-\tREJECT\tfinal\t0",
    "s5\tg7\t1\t2026-09-07\tr\treview\tshadow\t1\tc7\tgoogle\tgemini-9-pro\thigh\t6\t-\t-\tfinal\t1",
    "s6\tg8\t1\t2026-09-08\tr\treview\tindependent\t0\tc8\tgoogle\tgemini-3.1-pro-high\t-\t4\t-\tAPPROVE\tfinal\t0",
    "s7\tg8\t1\t2026-09-08\tr\treview\tshadow\t0\tc8\tgoogle\tgemini-3.8-flash-high\thigh\t3\t-\tAPPROVE\tfinal\t0",
    "s8\tg9\t1\t2026-09-09\tr\treview\tbroad\t1\tc9\topenai\tgpt-6-astra\txhigh\t5\t-\tREJECT\tfinal\t0",
]
ROLES_FINDINGS = [
    "s1\tg7\tc7\tk1\tcorrectness\tread\tBLOCKER\t1\thuman",
    "s3\tg7\tc7\tk1\tcorrectness\tread\tBLOCKER\t1\thuman",
    "s3\tg7\tc7\tk2\tcorrectness\tread\tBLOCKER\t1\thuman",
    "s4\tg7\tc7\tk3\tcorrectness\tread\tSHOULD\t1\thuman",
    "s4\tg7\tc7\tk2\tcorrectness\tread\tBLOCKER\t1\thuman",
    "s8\tg9\tc9\tk9\tcorrectness\tread\tBLOCKER\t1\thuman",
]


def reference_verdict(config: dict, dispatches: list[dict], findings: list[dict],
                      pin: str) -> str:
    """The trial rules written a second time, straight from dispatch.md and duck-learn, sharing no
    helper with `trial_verdict`: the class check compares the two over generated ledgers."""
    needed = int(config.get("shadow", DEFAULT_SHADOW))
    family, model = pin.split(":")[0], pin.split(":")[1]
    trialled = {tuple(t.split(":")[:2]) for t in config.get("trial", [])}
    listed = config["review"] if isinstance(config.get("review"), list) else config.get("reviewers", [])
    incumbent = None
    for entry in listed:
        fam, mod = entry.split(":")[:2]
        if fam == family and (fam, mod) not in trialled:
            incumbent = (fam, mod)
            break
    causes = {}
    for f in findings:
        if f["substantiated"] == "1":
            causes.setdefault(f["dispatch_id"], set()).add(f["cause_id"])
    causes = {ident: len(found) for ident, found in causes.items()}

    def baseline(row):
        for d in dispatches:
            if (incumbent and (d["family"], d["model"]) == incumbent and d["stage"] == "review"
                    and d["status"] == "final" and d["setup"] != "shadow" and d["outage"] == "0"
                    and d["repo"] == row["repo"] and d["gate_id"] == row["gate_id"]
                    and d["round"] == row["round"]
                    and d["candidate"] == row["candidate"]):
                return d
        return None

    order, by_gate = [], {}
    for d in dispatches:
        if (d["stage"] == "review" and d["setup"] == "shadow" and d["status"] == "final"
                and d["outage"] != "-"
                and (d["family"], d["model"]) == (family, model)):
            key = (d["repo"], d["gate_id"])
            if key not in by_gate:
                order.append(key)
                by_gate[key] = []
            by_gate[key].append(d)
    picked = []
    for gate_id in order[:2 * needed]:
        rows = by_gate[gate_id]
        paired = [d for d in rows if baseline(d)]
        picked.append(paired[0] if paired else rows[0])
    if any(d["outage"] == "1" for gate_id in order[:2 * needed] for d in by_gate[gate_id]):
        return "drop"
    if len(picked) < needed:
        return "shadow"
    out_of_time = len(picked) >= 2 * needed
    if incumbent is None:
        if sum(causes.get(d["id"], 0) for d in picked) > 0:
            return "add"
        return "drop" if out_of_time else "shadow"
    shared = [d for d in picked if baseline(d)]
    own = sum(causes.get(d["id"], 0) for d in shared)
    theirs = sum(causes.get(baseline(d)["id"], 0) for d in shared)
    if len(shared) < needed or own + theirs == 0:
        return "drop" if out_of_time else "shadow"
    return "replace" if own >= theirs else "drop"


def eligibility_check(cases: int = 3000) -> None:
    """Class check over the trial-eligibility surface: rounds per gate, which round carries the
    baseline, trial and incumbent outages, missing incumbents, another shadow on the same gate, a
    trial pin also named in the review list, finding counts, and gate counts around N and 2N."""
    rng = random.Random(7)
    pin = "openai:gpt-6-trial:high"
    for case in range(cases):
        needed = rng.choice([1, 2, 3])
        review = rng.choice([["openai:gpt-6-inc:high", "google:gem:high"], ["google:gem:high"],
                             [pin, "openai:gpt-6-inc:high"], []])
        config = {"doer": "anthropic", "review": review, "trial": [pin], "shadow": needed}
        dispatches, findings, n = [], [], 0

        def add(gate_id, rnd, setup, model, outage, repo="r"):
            nonlocal n
            n += 1
            ident = f"x{n}"
            dispatches.append({"id": ident, "gate_id": gate_id, "round": rnd, "repo": repo,
                               "candidate": gate_id, "stage": "review", "setup": setup,
                               "status": rng.choice(["final"] * 9 + ["pending"]),
                               "family": "openai", "model": model, "effort": "high",
                               "outage": outage})
            for k in range(rng.choice([0, 0, 1, 2])):
                findings.append({"dispatch_id": ident, "cause_id": f"c{n}{k}",
                                 "substantiated": rng.choice(["1", "1", "0"])})

        for g in range(rng.randint(0, 2 * needed + 2)):
            for rnd in rng.sample(["1", "2", "3"], rng.randint(1, 2)):
                add(f"g{g}", rnd, "shadow", "gpt-6-trial", rng.choice(["0"] * 8 + ["1", "-"]))
                if rng.random() < 0.6:
                    add(f"g{g}", rnd, "broad", "gpt-6-inc", rng.choice(["0"] * 5 + ["1", "-"]))
                if rng.random() < 0.2:  # the same gate id in another repository is another gate
                    add(f"g{g}", rnd, "broad", "gpt-6-inc", "0", repo="elsewhere")
                if rng.random() < 0.2:
                    add(f"g{g}", rnd, "shadow", "gpt-6-other", "0")
        got = trial_verdict(config, dispatches, findings, pin)[0]
        want = reference_verdict(config, dispatches, findings, pin)
        assert got == want, (case, got, want, config, dispatches, findings)


def roles_check(root: Path) -> None:
    """Role lists, fixed order, effort by risk, and shadow trials, on a fixture of their own."""
    (root / "config.toml").write_text(ROLES_CONFIG)
    for name, columns, fixture in (("dispatches.tsv", DISPATCH_COLUMNS, ROLES_DISPATCHES),
                                   ("findings.tsv", FINDING_COLUMNS, ROLES_FINDINGS)):
        (root / name).write_text("\t".join(columns) + "\n" + "\n".join(fixture) + "\n")
    config = load_config()
    assert roster_for(config, "race") == ["google:gemini-3.8-flash-high"]
    assert roster_for(config, "plan") == config["reviewers"]  # unset reviewer-side role falls back
    assert roster_for(config, "explore") == []  # the host chooses
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
    # s3 shares k1 with counted s1 (s1 keeps its credit) and k2 with shadow s4 (neither earns it)
    assert unique_blocker_dispatches(dispatches, findings) == {"s1", "s8"}
    for argv, expected, wanted, unwanted in (
            (["pick", "race", "--repo", "r"], 0, ["chosen google:gemini-3.8-flash-high"], ["shadow"]),
            (["remaining", "g7", "--repo", "elsewhere"], 0, ["insufficient evidence: 0"], []),
            (["pick", "review", "--trust", "--repo", "r"], 0,
             ["chosen openai:gpt-6-astra:xhigh", "shadow openai:gpt-6-nova:xhigh 0/1"],
             ["shadow openai:gpt-6-sol"]),  # past its shadow gates, it no longer rides along
            (["remaining", "g7", "--repo", "r"], 0, ["n1 = 1", "n2 = 0"], []),  # shadows are not captures
            (["promote", "--repo", "r"], 0,
             ["replace openai:gpt-6-astra:high with openai:gpt-6-sol:high in review",
              "add anthropic:claude-x:high to review", "drop google:gemini-9-pro:high",
              "shadow openai:gpt-6-nova:high: 0/1",
              "shadow google:gemini-3.8-flash-high: 1 shared gates, 0 vs 0 causes"], [])):
        code, out = run(argv)
        assert code == expected and all(w in out for w in wanted), (argv, out)
        assert not any(u in out for u in unwanted), (argv, out)
    # undecided trials keep riding to twice their count, then leave; the comparison is shared gates
    assert roster_for(dict(config, review=["x:y:z"]), "disposition") == ["x:y:z"]
    assert roster_for(dict(config, review=[]), "review") == []  # an explicit empty list stays empty
    code, out = run(["pick", "worker", "--trust", "--repo", "r"])
    assert code == 0 and "chosen anthropic:claude-sonnet-5" in out, out  # one worker, no 2nd family
    (root / "config.toml").write_text('[families]\ndoer = "anthropic"\n')
    code, out = run(["pick", "explore", "--repo", "r"])
    assert code == 1 and "holds no any arm" in out, out  # not "outside anthropic": explore may share it
    (root / "config.toml").write_text(ROLES_CONFIG)
    clean = dict(dispatches[6], id="s9", gate_id="g10", candidate="c10")
    assert trial_verdict(config, dispatches + [clean], findings,
                         "google:gemini-3.8-flash-high")[0] == "drop"
    elsewhere = dict(dispatches[2], id="s10", gate_id="g11", candidate="c11")
    worse = dispatches + [elsewhere]
    extra = findings + [dict(findings[2], dispatch_id="s10", cause_id="q1", candidate="c11")]
    config2 = dict(config, shadow=2)  # s10's cause sits on a gate astra never saw: it cannot count
    assert trial_verdict(config2, worse, extra, "openai:gpt-6-sol:high")[0] == "shadow"
    # worse beside the incumbent (0 vs s1's 1 on g7), better only where it ran alone: drop
    beside = dict(dispatches[2], id="z1", model="gpt-6-zeta")
    alone = dict(dispatches[2], id="z2", model="gpt-6-zeta", gate_id="g12", candidate="c12")
    alone_f = findings + [dict(findings[2], dispatch_id="z2", cause_id="q2", candidate="c12")]
    assert trial_verdict(config, dispatches + [beside, alone], alone_f,
                         "openai:gpt-6-zeta:high")[0] == "drop"
    # gate review round 1: three rounds of one gate are one gate; an incumbent outage is no baseline
    rounds = [dict(dispatches[2], id=f"r{k}", model="gpt-6-omega", round=str(k)) for k in (2, 3)]
    rounds_f = findings + [dict(findings[2], dispatch_id=f"r{k}", cause_id=f"w{k}") for k in (2, 3)]
    three = dict(config, shadow=3)
    assert trial_verdict(three, dispatches + [dict(dispatches[2], id="r1", model="gpt-6-omega")]
                         + rounds, rounds_f, "openai:gpt-6-omega:high") == ("shadow", "1/3")
    down = [dict(dispatches[0], id=f"o{g}", gate_id=g, candidate=g, outage="1") for g in "xyz"]
    ride = [dict(dispatches[2], id=f"t{g}", gate_id=g, candidate=g, model="gpt-6-tau") for g in "xyz"]
    tau_f = findings + [dict(findings[2], dispatch_id="tx", cause_id="u1", candidate="x")]
    assert trial_verdict(three, dispatches + down + ride, tau_f,
                         "openai:gpt-6-tau:high")[0] == "shadow"  # no shared baseline yet
    # gate review round 2: a trial pin never counts even when a list names it, and a gate's paired
    # round is the one compared
    both = dict(config, review=["google:gemini-trial:high", "openai:gpt-6-astra:high"],
                trial=["google:gemini-trial:high"], select="fixed")  # listed first: no luck
    chosen, _ = pick_arms(both, dispatches, findings, "review", trust=False)
    assert ("google", "gemini-trial") not in {a[:2] for a in chosen}, chosen
    paired_rows, paired_f = [], list(findings)
    for g in "pqr":
        paired_rows += [dict(dispatches[2], id=f"{g}1", gate_id=g, candidate=g, model="gpt-6-pi"),
                        dict(dispatches[2], id=f"{g}2", gate_id=g, candidate=g, round="2",
                             model="gpt-6-pi"),
                        dict(dispatches[0], id=f"{g}i", gate_id=g, candidate=g, round="2")]
        paired_f.append(dict(findings[2], dispatch_id=f"{g}2", cause_id=f"v{g}", candidate=g))
    assert trial_verdict(three, dispatches + paired_rows, paired_f,
                         "openai:gpt-6-pi:high")[0] == "replace"
    # gate review round 3: an outage in any round of a counted gate drops the trial, even when a
    # later round of that gate is the one compared
    retried = [dict(dispatches[2], id=f"{g}{k}", gate_id=g, candidate=g, model="gpt-6-rho",
                    round=k, outage="1" if (g, k) == ("m", "1") else "0")
               for g in "mno" for k in ("1", "2")]
    base = [dict(dispatches[0], id=f"{g}b", gate_id=g, candidate=g, round="2") for g in "mno"]
    rho_f = findings + [dict(findings[2], dispatch_id="m2", cause_id="h1", candidate="m")]
    assert trial_verdict(three, dispatches + retried + base, rho_f,
                         "openai:gpt-6-rho:high")[0] == "drop"
    # gate review round 4: worker and explore pick from their own list, doer's family included
    own_family = {"doer": "anthropic", "worker": ["anthropic:claude-sonnet-5:medium"]}
    assert pick_arms(own_family, [], [], "worker", trust=True)[0] == [
        ("anthropic", "claude-sonnet-5", "medium")]
    assert pick_arms(own_family, [], [], "review", trust=False)[0] == []  # judges stay independent
    assert pin_of(("google", "gemini-3.1-pro-high", "-")) == "google:gemini-3.1-pro-high"
    models = root / "models.txt"
    models.write_text("Fetching available models...\ngemini-3.1-pro-high\tGemini 3.1 Pro\n"
                      "gemini-10-pro-high\tGemini 10 Pro\ngpt-6-sol\n")
    code, out = run(["roster", str(models), "--repo", "r"])
    assert code == 0 and out.strip() == "new google:gemini-10-pro-high", out


def rally_check(root: Path) -> None:
    """Cases the duck-race rally on trials served; each failed against the code it was served on."""
    # a dismissed counted claim takes no shadow's unique credit
    dispatches = [{"id": "counted", "gate_id": "g1", "round": "1", "candidate": "c1",
                   "stage": "review", "setup": "independent", "repo": "r"},
                  {"id": "trial", "gate_id": "g1", "round": "1", "candidate": "c1",
                   "stage": "review", "setup": "shadow", "repo": "r"}]
    findings = [{"dispatch_id": "counted", "cause_id": "bug", "severity": "BLOCKER",
                 "substantiated": "0"},
                {"dispatch_id": "trial", "cause_id": "bug", "severity": "BLOCKER",
                 "substantiated": "1"}]
    assert unique_blocker_dispatches(dispatches, findings) == {"trial"}
    # an outage drops a trial before it reaches its gate count
    config = {"doer": "anthropic", "review": ["openai:gpt-6-inc:high"],
              "trial": ["openai:gpt-6-t:high"], "shadow": 3}
    outage = [{"id": "t1", "gate_id": "g1", "round": "1", "candidate": "c1", "stage": "review", "repo": "r",
               "setup": "shadow", "status": "final", "family": "openai", "model": "gpt-6-t",
               "effort": "high", "outage": "1"}]
    assert trial_verdict(config, outage, [], "openai:gpt-6-t:high")[0] == "drop"
    # one cause recorded twice is one cause
    rows = [{"id": f"{model}-{gate}", "gate_id": gate, "round": "1", "candidate": gate, "repo": "r",
             "stage": "review", "setup": setup, "status": "final", "outage": "0",
             "family": "openai", "model": model}
            for gate in ("g1", "g2", "g3")
            for model, setup in (("gpt-6-inc", "independent"), ("gpt-6-t", "shadow"))]
    twice = ([{"dispatch_id": "gpt-6-inc-g1", "cause_id": c, "substantiated": "1"} for c in "ab"]
             + [{"dispatch_id": "gpt-6-t-g1", "cause_id": "c", "substantiated": "1"}] * 2)
    assert trial_verdict(config, rows, twice, "openai:gpt-6-t:high")[0] == "drop"
    # only shadow reviews count toward a trial, not dispositions
    one = dict(config, review=["google:gem:high"], shadow=1)
    disposition = dict(outage[0], id="d1", stage="disposition", outage="0")
    assert trial_verdict(one, [disposition],
                         [{"dispatch_id": "d1", "cause_id": "k", "substantiated": "1"}],
                         "openai:gpt-6-t:high")[0] == "shadow"
    # a shadow's findings never vouch for its family's precision
    vouch = [{"id": "s1", "repo": "r", "stage": "review", "family": "openai", "setup": "shadow"},
             {"id": "c1", "repo": "r", "stage": "review", "family": "openai",
              "setup": "independent"}]
    claims = ([{"dispatch_id": "s1", "class": "correctness", "tier": "read", "substantiated": "1"}]
              * 3 + [{"dispatch_id": "c1", "class": "correctness", "tier": "read",
                      "substantiated": "0"}])
    assert precision_table(vouch, claims, "r")[("openai", "correctness", "read")] == (1, 0)
    # a gate id recurs across repositories: another repository's gate is no shared baseline
    other = [dict(rows[0], id="x-inc", repo="elsewhere", gate_id="g9", candidate="g9"),
             dict(rows[1], id="x-t", gate_id="g9", candidate="g9")]
    lone = dict(config, shadow=1)
    assert trial_verdict(lone, other, [{"dispatch_id": "x-inc", "cause_id": "q",
                                        "substantiated": "1"}],
                         "openai:gpt-6-t:high")[0] == "shadow"  # no baseline in its own repo yet
    # a race takes one rival even when the work is trust-touching; review still takes two
    race_cfg = {"doer": "anthropic", "race": ["google:gem:high", "openai:o:high"],
                "trust": "xhigh", "select": "fixed"}
    assert pick_arms(race_cfg, [], [], "race", trust=True)[0] == [("google", "gem", "xhigh")]
    (root / "config.toml").write_text('[families]\ndoer = "anthropic"\n[models]\n'
                                      'race = ["google:gem:high"]\n')
    code, out = run(["pick", "race", "--trust", "--repo", "r"])
    assert code == 0 and "chosen google:gem:high" in out, out  # one rival, no second family
    with contextlib.redirect_stderr(io.StringIO()):
        code, out = run(["remaining", "g1"])
    assert code == 1, out  # no origin, no --repo: a gate id alone names no gate
    # same gate id, another repository: no shared uniqueness, no shared capture
    twin = [dict(rows[0], id="a1", stage="review", setup="independent", gate_id="gx",
                 candidate="gx"),
            dict(rows[0], id="b1", stage="review", setup="independent", gate_id="gx",
                 candidate="gx", repo="elsewhere")]
    both = [{"dispatch_id": d, "cause_id": "same", "severity": "BLOCKER",
             "substantiated": "1"} for d in ("a1", "b1")]
    assert unique_blocker_dispatches(twin, both) == {"a1", "b1"}
    # cost prices a riding shadow
    (root / "config.toml").write_text(
        '[families]\ndoer = "anthropic"\n[learn]\ntrial = ["openai:gpt-6-t:high"]\n')
    code, out = run(["cost", "broad", "--repo", "r"])
    assert code == 0 and "dispatches = 5" in out, out


def home_check(parent: Path) -> None:
    """Through the command: a missing ledger warns once, a missing findings table is a clean
    history, and a table that exists but cannot be read ends the command instead of answering."""
    header = {"dispatches.tsv": "\t".join(DISPATCH_COLUMNS) + "\n",
              "findings.tsv": "\t".join(FINDING_COLUMNS) + "\n"}
    parent.mkdir()
    models = parent / "models.txt"
    models.write_text("gpt-6-sol\n")
    readers = (["remaining", "g", "--repo", "r"], ["precision", "--all"], ["missed"],
               ["pick", "review", "--repo", "r"], ["thresholds"],
               ["cost", "broad", "--repo", "r"], ["roster", str(models), "--repo", "r"],
               ["promote", "--repo", "r"])

    def call(root: Path, argv: list[str]) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "-B", "-c", SEEDED, *argv], capture_output=True,
                              text=True, cwd=parent, env={**os.environ, "ASKRUBBERDUCK_HOME": str(root)})

    for n, argv in enumerate(readers):
        root = parent / f"r{n}"
        root.mkdir()
        (root / "config.toml").write_text('[families]\ndoer = "anthropic"\n'
                                          'reviewers = ["openai:gpt-6-sol:high"]\n')
        missing = call(root, argv)
        (root / "dispatches.tsv").write_text(header["dispatches.tsv"])
        empty = call(root, argv)
        assert missing.returncode == 0 and (missing.returncode, missing.stdout) == \
            (empty.returncode, empty.stdout), argv
        assert empty.stderr == "", (argv, empty.stderr)
        assert missing.stderr == f"{root / 'dispatches.tsv'}: no dispatch recorded yet\n", missing

    ways = {"Is a directory": lambda path: path.mkdir(),
            "header does not match": lambda path: path.write_text("id\tother\n"),
            "not UTF-8": lambda path: path.write_bytes(b"\xff\xfe\n"),
            "dangling symlink": lambda path: path.symlink_to(path.parent / "gone")}
    if os.geteuid() != 0:  # root reads a mode-0 file
        ways["Permission denied"] = lambda path: (path.write_text(header[path.name]),
                                                  path.chmod(0))
    for name in header:
        for reason, spoil in ways.items():
            root = parent / f"{len(reason)}-{name}"
            root.mkdir()
            for other in set(header) - {name}:
                (root / other).write_text(header[other])
            spoil(root / name)
            done = call(root, ["promote"])
            if (root / name).is_file():
                (root / name).chmod(0o600)
            assert done.returncode != 0 and done.stdout == "", (reason, name, done)
            assert done.stderr.startswith(f"{root / name}") and reason in done.stderr, \
                (reason, name, done.stderr)
    if os.geteuid() != 0:
        locked = parent / "locked"
        locked.mkdir()
        (locked / "dispatches.tsv").write_text(header["dispatches.tsv"])
        locked.chmod(0)
        done = call(locked, ["promote"])
        locked.chmod(0o700)
        assert done.returncode != 0 and done.stdout == "", done
        assert done.stderr == f"{locked / 'dispatches.tsv'}: Permission denied\n", done.stderr
    dangling = parent / "dangling"
    dangling.symlink_to(parent / "gone")
    done = call(dangling, ["promote"])
    assert done.returncode != 0 and "dangling symlink" in done.stderr, done
    roast = parent / "roast"  # a roast row is recorded, yet never a review capture
    roast.mkdir()
    (roast / "dispatches.tsv").write_text(header["dispatches.tsv"] + "\t".join(
        ["x", "g", "1", "-", "r", "roast", "independent", "0", "c", "openai", "gpt-r", "-", "3",
         "-", "NOTE", "final", "0"]) + "\n")
    done = call(roast, ["thresholds"])
    assert done.returncode == 0 and done.stderr == "" and "gpt-r n=1" in done.stdout, done
    done = call(roast, ["remaining", "g", "--repo", "r"])
    assert "insufficient evidence: 0 eligible captures" in done.stdout, done
    done = call(roast, ["cost", "independent", "--repo", "r"])
    assert done.returncode == 0 and "mean minutes = -" in done.stdout, done
    (roast / "findings.tsv").write_text(header["findings.tsv"] + "\t".join(
        ["x", "g", "c", "cause", "roastclass", "read", "SHOULD", "0", "doer"]) + "\n")
    done = call(roast, ["precision", "--all"])
    assert done.returncode == 0 and "roastclass" not in done.stdout, done
    latin = parent / "latin"  # the table is UTF-8 whatever the reader's locale says
    latin.mkdir()
    (latin / "dispatches.tsv").write_text(header["dispatches.tsv"] + "\t".join(
        ["x", "g", "1", "-", "r", "review", "independent", "0", "c", "openai", "gpt-é", "-", "-",
         "-", "-", "final", "0"]) + "\n", encoding="utf-8")
    done = subprocess.run([sys.executable, str(LEDGER), "thresholds"], capture_output=True,
                          env={**os.environ, "ASKRUBBERDUCK_HOME": str(latin), "PYTHONUTF8": "0",
                               "LC_ALL": "en_US.ISO8859-1", "PYTHONIOENCODING": "utf-8"})
    assert done.returncode == 0 and "gpt-é".encode() in done.stdout, done


def self_check() -> int:
    with tempfile.TemporaryDirectory(prefix="askrubberduck-ledger-") as directory:
        root = Path(directory)
        os.environ["ASKRUBBERDUCK_HOME"] = str(root)
        (root / "config.toml").write_text(CONFIG_FIXTURE)
        home_check(root / "homes")
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
                (["remaining", "g1", "--repo", "r"], 0, ["remaining = 0.500"]),
                (["remaining", "g4", "--repo", "r"], 0, ["n2 = 0", "remaining = 0.000"]),
                (["remaining", "g3", "--repo", "r"], 0, ["insufficient evidence: 1 eligible captures"]),
                (["precision", "--repo", "r"], 0, ["anthropic correctness executed claimed=4"]),
                (["missed"], 0, ["anthropic claude-opus-5 missed=1"]),  # the c4 production row is unsubstantiated: openai is not charged
                (["remaining", "g5", "--repo", "r"], 0, ["n1 = 1", "n2 = 2", "m = 1", "remaining = 0.000"]),  # two dispositions present, not captures
                (["pick", "review", "--trust", *repo], 0,
                 ["chosen openai:gpt-6-astra:high", "chosen google:gemini-3.1-pro-high\n"]),
                (["paired", str(results)], 0, ["discordant = 8", "sprt = arm A better"]),
                (["thresholds"], 0, ["anthropic claude-opus-5 n=4"]),
                (["cost", "broad", *repo], 0, ["dispatches = 4"]),
                (["cost", "rally", *repo], 0, ["turns = 10", "dispatches = 5"]),
                (["cost", "independent", "--trust", *repo], 0, ["dispatches = 4"]),  # trust is Broad whatever was asked
                (["cost", "sideways", *repo], 1, ["unknown setup"]),
                (["schema"], 0, ["candidate", "CONCUR"])):
            random.seed(1)
            code, out = run(argv)
            assert code == expected, (argv, code, out)
            assert all(want in out for want in wanted), (argv, out)
        roles_check(root)
        eligibility_check()
        rally_check(root)
    for gone in (["--self-check"], ["pick", "review", "--seed", "1"]):  # test hooks stay in tests/
        result = subprocess.run([sys.executable, "-B", str(LEDGER), *gone], capture_output=True,
                                text=True)
        assert result.returncode == 2 and "unrecognized arguments" in result.stderr, (gone, result)
    print("ledger self-check passed")
    return 0



if __name__ == "__main__":
    raise SystemExit(self_check())
