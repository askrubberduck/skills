#!/usr/bin/env python3
"""Outage causes for a seat without a usable verdict: rally serves 3-4 (GPT-6.1 Sol, 2026-10-10)."""
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "duck-review" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from dispatch import classify


class OutageCause(unittest.TestCase):
    def test_crashed_verdict_preserves_log_outage_classification(self):
        self.assertEqual(
            classify("VERDICT: APPROVE", "codex", False, 7,
                     "ERROR: You're out of credits."),
            ("-", "credits"))

    def test_outage_matching_preserves_answer_characters(self):
        diagnostic = "Error: rate\vlimit reached"
        self.assertEqual(classify("", "codex", False, 0, diagnostic), ("-", "quota"))
        self.assertEqual(classify(diagnostic, "codex", False, 0, ""), ("-", "quota"))


if __name__ == "__main__":
    unittest.main()
