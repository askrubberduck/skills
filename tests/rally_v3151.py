#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "duck-review" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from ledger import DISPATCH_COLUMNS, FINDING_COLUMNS, trial_verdict


class RallyV3151(unittest.TestCase):
    def test_dropped_trial_reports_missed_cause_on_shared_gate(self):
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
        for ident, cause, severity in (("inc", "shared-cause", "NOTE"),
                                       ("inc", "missed-blocker", "BLOCKER"),
                                       ("trial", "shared-cause", "NOTE")):
            row = dict.fromkeys(FINDING_COLUMNS, "-")
            row.update(dispatch_id=ident, gate_id="g1", candidate="c1", cause_id=cause,
                       severity=severity, substantiated="1")
            findings.append(row)
        self.assertEqual(
            trial_verdict(config, dispatches, findings, pin),
            ("drop", "1 vs 2 causes on shared gates", [("BLOCKER", "missed-blocker")]))


if __name__ == "__main__":
    unittest.main()
