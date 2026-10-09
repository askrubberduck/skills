#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import csv
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


class PromoteTest(unittest.TestCase):
    def test_semicolon_in_cause_id_stays_on_one_missed_line(self):
        incumbent = "openai:gpt-6-inc:high"
        pin = "openai:gpt-6-trial:high"
        cause = "parser; delimiter"
        dispatches = []
        for ident, model, setup in (("inc", "gpt-6-inc", "independent"),
                                    ("trial", "gpt-6-trial", "shadow")):
            row = dict.fromkeys(DISPATCH_COLUMNS, "-")
            row.update(id=ident, gate_id="g1", round="1", repo="r", candidate="c1",
                       stage="review", setup=setup, status="final", outage="0",
                       family="openai", model=model, effort="high")
            dispatches.append(row)
        findings = []
        for ident, cause_id in (("inc", cause), ("trial", "another-cause")):
            row = dict.fromkeys(FINDING_COLUMNS, "-")
            row.update(dispatch_id=ident, gate_id="g1", candidate="c1",
                       cause_id=cause_id, severity="BLOCKER", substantiated="1")
            findings.append(row)

        with tempfile.TemporaryDirectory(prefix="rally-up24-") as directory:
            root = Path(directory)
            (root / "config.toml").write_text(
                f'[families]\nreviewers = ["{incumbent}"]\n'
                f'[learn]\nshadow = 1\ntrial = ["{pin}"]\n', encoding="utf-8")
            for name, columns, rows in (("dispatches.tsv", DISPATCH_COLUMNS, dispatches),
                                        ("findings.tsv", FINDING_COLUMNS, findings)):
                with (root / name).open("w", encoding="utf-8", newline="") as stream:
                    writer = csv.DictWriter(stream, fieldnames=columns, delimiter="\t")
                    writer.writeheader()
                    writer.writerows(rows)

            with patch.dict(os.environ, {"ASKRUBBERDUCK_HOME": directory}):
                config = load_config("r")
                loaded_dispatches, loaded_findings = load_tables()
                self.assertEqual(
                    trial_verdict(config, loaded_dispatches, loaded_findings, pin),
                    ("replace", f"{incumbent}; missed BLOCKER {cause}"))
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    code = main(["promote", "--repo", "r"])
                self.assertEqual(code, 0)
                self.assertEqual(output.getvalue(),
                                 f"replace {incumbent} with {pin} in review\n"
                                 f"  missed BLOCKER {cause}\n")

    def test_unknown_severity_does_not_change_replace_verdict(self):
        incumbent = "openai:gpt-6-inc:high"
        pin = "openai:gpt-6-trial:high"
        config = {"reviewers": [incumbent], "trial": [pin], "shadow": 1}
        dispatches = []
        for ident, model, setup in (("inc", "gpt-6-inc", "independent"),
                                    ("trial", "gpt-6-trial", "shadow")):
            row = dict.fromkeys(DISPATCH_COLUMNS, "-")
            row.update(id=ident, gate_id="g1", round="1", repo="r", candidate="c1",
                       stage="review", setup=setup, status="final", outage="0",
                       family="openai", model=model, effort="high")
            dispatches.append(row)
        findings = []
        for ident, cause, severity in (("inc", "incumbent-cause", "-"),
                                       ("trial", "trial-cause", "NOTE")):
            row = dict.fromkeys(FINDING_COLUMNS, "-")
            row.update(dispatch_id=ident, gate_id="g1", candidate="c1",
                       cause_id=cause, severity=severity, substantiated="1")
            findings.append(row)

        with tempfile.TemporaryDirectory(prefix="rally-up24-") as directory:
            root = Path(directory)
            for name, columns, rows in (("dispatches.tsv", DISPATCH_COLUMNS, dispatches),
                                        ("findings.tsv", FINDING_COLUMNS, findings)):
                with (root / name).open("w", encoding="utf-8", newline="") as stream:
                    writer = csv.DictWriter(stream, fieldnames=columns, delimiter="\t")
                    writer.writeheader()
                    writer.writerows(rows)
            with patch.dict(os.environ, {"ASKRUBBERDUCK_HOME": directory}):
                loaded_dispatches, loaded_findings = load_tables()
                self.assertEqual(loaded_findings, findings)
                self.assertEqual(
                    trial_verdict(config, loaded_dispatches, loaded_findings, pin)[0],
                    "replace")

    def test_missing_severity_preserves_existing_replace_verdict(self):
        incumbent = "openai:gpt-6-inc:high"
        pin = "openai:gpt-6-trial:high"
        config = {"reviewers": [incumbent], "trial": [pin], "shadow": 1}
        dispatches = []
        for ident, model, setup in (("inc", "gpt-6-inc", "independent"),
                                    ("trial", "gpt-6-trial", "shadow")):
            row = dict.fromkeys(DISPATCH_COLUMNS, "-")
            row.update(id=ident, gate_id="g1", round="1", repo="r", candidate="c1",
                       stage="review", setup=setup, status="final", outage="0",
                       family="openai", model=model, effort="high")
            dispatches.append(row)
        # The pre-UP24 comparison accepts these same minimal finding dictionaries.
        findings = [{"dispatch_id": "inc", "cause_id": "incumbent-cause",
                     "substantiated": "1"},
                    {"dispatch_id": "trial", "cause_id": "trial-cause",
                     "substantiated": "1"}]
        self.assertEqual(trial_verdict(config, dispatches, findings, pin)[0], "replace")

if __name__ == "__main__":
    unittest.main()
