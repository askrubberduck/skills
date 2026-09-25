import importlib.util
import unittest
from pathlib import Path


spec = importlib.util.spec_from_file_location("ledger", Path(__file__).with_name("ledger.py"))
ledger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ledger)


class LedgerTrialsTest(unittest.TestCase):
    def test_dismissed_counted_claim_does_not_take_shadow_uniqueness(self):
        dispatches = [
            {"id": "counted", "gate_id": "g1", "round": "1", "candidate": "c1",
             "stage": "review", "setup": "independent"},
            {"id": "trial", "gate_id": "g1", "round": "1", "candidate": "c1",
             "stage": "review", "setup": "shadow"},
        ]
        findings = [
            {"dispatch_id": "counted", "cause_id": "bug", "severity": "BLOCKER",
             "substantiated": "0"},
            {"dispatch_id": "trial", "cause_id": "bug", "severity": "BLOCKER",
             "substantiated": "1"},
        ]

        self.assertEqual({"trial"}, ledger.unique_blocker_dispatches(dispatches, findings))

    def test_outage_drops_trial_before_it_reaches_its_gate_count(self):
        # contract: "An outage ("1") on any shadow round of a counted gate drops the trial."
        config = {"doer": "anthropic", "review": ["openai:gpt-6-inc:high"],
                  "trial": ["openai:gpt-6-t:high"], "shadow": 3}
        dispatches = [{"id": "t1", "gate_id": "g1", "round": "1", "candidate": "c1",
                       "stage": "review", "setup": "shadow", "status": "final",
                       "family": "openai", "model": "gpt-6-t", "effort": "high", "outage": "1"}]
        verdict, _ = ledger.trial_verdict(config, dispatches, [], "openai:gpt-6-t:high")
        self.assertEqual("drop", verdict)

    def test_duplicate_finding_rows_do_not_turn_one_cause_into_two(self):
        config = {"review": ["openai:gpt-6-inc:high"],
                  "trial": ["openai:gpt-6-t:high"], "shadow": 3}
        dispatches = [
            {"id": f"{model}-{gate}", "gate_id": gate, "round": "1", "candidate": gate,
             "stage": "review", "setup": setup, "status": "final", "outage": "0",
             "family": "openai", "model": model}
            for gate in ("g1", "g2", "g3")
            for model, setup in (("gpt-6-inc", "independent"), ("gpt-6-t", "shadow"))
        ]
        findings = [
            {"dispatch_id": "gpt-6-inc-g1", "cause_id": cause, "substantiated": "1"}
            for cause in ("a", "b")
        ] + [
            {"dispatch_id": "gpt-6-t-g1", "cause_id": "c", "substantiated": "1"}
            for _ in range(2)
        ]

        verdict, _ = ledger.trial_verdict(config, dispatches, findings, "openai:gpt-6-t:high")
        self.assertEqual("drop", verdict)

    def test_only_shadow_reviews_count_toward_a_trial(self):
        # contract: "fewer final shadow reviews than `[learn].shadow`"; a disposition is no review
        config = {"doer": "anthropic", "review": ["google:gem:high"],
                  "trial": ["openai:gpt-6-t:high"], "shadow": 1}
        row = {"id": "d1", "gate_id": "g1", "round": "1", "candidate": "c1",
               "stage": "disposition", "setup": "shadow", "status": "final",
               "family": "openai", "model": "gpt-6-t", "effort": "high", "outage": "0"}
        findings = [{"dispatch_id": "d1", "cause_id": "k", "substantiated": "1"}]
        verdict, _ = ledger.trial_verdict(config, [row], findings, "openai:gpt-6-t:high")
        self.assertEqual("shadow", verdict)

    def test_shadow_findings_never_vouch_for_their_family(self):
        # a trial must not shorten a gate: the stop rule reads family precision
        dispatches = [{"id": "s1", "repo": "r", "family": "openai", "setup": "shadow"},
                      {"id": "c1", "repo": "r", "family": "openai", "setup": "independent"}]
        findings = [{"dispatch_id": "s1", "class": "correctness", "tier": "read",
                     "substantiated": "1"} for _ in range(3)]
        findings.append({"dispatch_id": "c1", "class": "correctness", "tier": "read",
                         "substantiated": "0"})
        table = ledger.precision_table(dispatches, findings, "r")
        self.assertEqual((1, 0), table[("openai", "correctness", "read")])

    def test_cost_counts_a_riding_shadow(self):
        import contextlib, io, os, tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as home:
            Path(home, "config.toml").write_text(
                '[families]\ndoer = "anthropic"\n[learn]\ntrial = ["openai:gpt-6-t:high"]\n')
            with patch.dict(os.environ, {"ASKRUBBERDUCK_HOME": home}):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    ledger.main(["cost", "broad", "--repo", "r"])
        self.assertIn("dispatches = 5", out.getvalue())


if __name__ == "__main__":
    unittest.main()
