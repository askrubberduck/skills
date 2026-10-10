#!/usr/bin/env python3
"""Missed-cause listing on a trial replace: rally serves 1-4 (GPT-6.1 Sol, 2026-10-10)."""
from __future__ import annotations

import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "duck-review" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from ledger import (DISPATCH_COLUMNS, FINDING_COLUMNS, load_config, load_tables,
                    main, trial_verdict)

INCUMBENT = "openai:gpt-6-inc:high"
PIN = "openai:gpt-6-trial:high"
CONFIG = {"reviewers": [INCUMBENT], "trial": [PIN], "shadow": 1}


def dispatches() -> list[dict]:
    """The incumbent and the trial pin, side by side on one gate."""
    rows = []
    for ident, model, setup in (("inc", "gpt-6-inc", "independent"),
                                ("trial", "gpt-6-trial", "shadow")):
        row = dict.fromkeys(DISPATCH_COLUMNS, "-")
        row.update(id=ident, gate_id="g1", round="1", repo="r", candidate="c1",
                   stage="review", setup=setup, status="final", outage="0",
                   family="openai", model=model, effort="high")
        rows.append(row)
    return rows


def findings(*causes: tuple[str, str, str]) -> list[dict]:
    """Substantiated finding rows from (dispatch_id, cause_id, severity)."""
    rows = []
    for ident, cause, severity in causes:
        row = dict.fromkeys(FINDING_COLUMNS, "-")
        row.update(dispatch_id=ident, gate_id="g1", candidate="c1",
                   cause_id=cause, severity=severity, substantiated="1")
        rows.append(row)
    return rows


def write_tables(root: Path, found: list[dict]) -> None:
    for name, columns, rows in (("dispatches.tsv", DISPATCH_COLUMNS, dispatches()),
                                ("findings.tsv", FINDING_COLUMNS, found)):
        # as dispatch writes them: plain tab-joined fields, no quoting
        (root / name).write_text("".join("\t".join(r) + "\n" for r in
                                         [columns, *[[row[c] for c in columns] for row in rows]]),
                                 encoding="utf-8")


class PromoteTest(unittest.TestCase):
    def test_semicolon_in_cause_id_stays_on_one_missed_line(self):
        cause = "parser; delimiter"
        with tempfile.TemporaryDirectory(prefix="rally-up24-") as directory:
            root = Path(directory)
            (root / "config.toml").write_text(
                f'[families]\nreviewers = ["{INCUMBENT}"]\n'
                f'[learn]\nshadow = 1\ntrial = ["{PIN}"]\n', encoding="utf-8")
            write_tables(root, findings(("inc", cause, "BLOCKER"),
                                        ("trial", "another-cause", "BLOCKER")))
            with patch.dict(os.environ, {"ASKRUBBERDUCK_HOME": directory}):
                config = load_config("r")
                loaded_dispatches, loaded_findings = load_tables()
                self.assertEqual(
                    trial_verdict(config, loaded_dispatches, loaded_findings, PIN),
                    ("replace", INCUMBENT, [("BLOCKER", cause)]))
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    code = main(["promote", "--repo", "r"])
                self.assertEqual(code, 0)
                self.assertEqual(output.getvalue(),
                                 f"replace {INCUMBENT} with {PIN} in review\n"
                                 f"  missed BLOCKER {cause}\n")

    def test_unknown_severity_does_not_change_replace_verdict(self):
        found = findings(("inc", "incumbent-cause", "-"), ("trial", "trial-cause", "NOTE"))
        with tempfile.TemporaryDirectory(prefix="rally-up24-") as directory:
            write_tables(Path(directory), found)
            with patch.dict(os.environ, {"ASKRUBBERDUCK_HOME": directory}):
                loaded_dispatches, loaded_findings = load_tables()
                self.assertEqual(loaded_findings, found)
                self.assertEqual(
                    trial_verdict(CONFIG, loaded_dispatches, loaded_findings, PIN)[0],
                    "replace")

    def test_missing_severity_preserves_existing_replace_verdict(self):
        # The pre-UP24 comparison accepts these same minimal finding dictionaries.
        found = [{"dispatch_id": "inc", "cause_id": "incumbent-cause", "substantiated": "1"},
                 {"dispatch_id": "trial", "cause_id": "trial-cause", "substantiated": "1"}]
        self.assertEqual(trial_verdict(CONFIG, dispatches(), found, PIN)[0], "replace")

    def test_null_and_unknown_severities_preserve_existing_replace_verdict(self):
        found = [
            {"dispatch_id": "inc", "cause_id": "null-severity",
             "substantiated": "1", "severity": None},
            {"dispatch_id": "inc", "cause_id": "unknown-severity",
             "substantiated": "1", "severity": "-"},
            {"dispatch_id": "trial", "cause_id": "trial-a",
             "substantiated": "1", "severity": "NOTE"},
            {"dispatch_id": "trial", "cause_id": "trial-b",
             "substantiated": "1", "severity": "NOTE"},
        ]
        # Before UP24, this tie returns replace without consulting severity.
        self.assertEqual(trial_verdict(CONFIG, dispatches(), found, PIN)[0], "replace")


if __name__ == "__main__":
    unittest.main()
