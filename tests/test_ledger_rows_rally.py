#!/usr/bin/env python3
"""A value dispatch writes is read back as one row: rally serves 8-9 (GPT-6.1 Sol, 2026-10-10)."""
"""B3: every accepted dispatch value must survive as one ledger row."""
import csv
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "duck-review" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from dispatch import record
from ledger import DISPATCH_COLUMNS, DISPATCH_ENUMS, read_table


class AcceptedRowTest(unittest.TestCase):
    def test_accepted_large_model_reads_back_as_one_row(self):
        row = dict.fromkeys(DISPATCH_COLUMNS, "-")
        row.update(id="large-model", gate_id="g", round="1", date="2026-10-10",
                   repo="r", stage="review", setup="independent", trust="0",
                   family="openai", model="x" * (csv.field_size_limit() + 1),
                   status="pending")
        with tempfile.TemporaryDirectory(prefix="rally-v3151-") as directory:
            with patch.dict(os.environ, {"ASKRUBBERDUCK_HOME": directory}):
                self.assertTrue(record(row, new=True))
                try:
                    rows = read_table("dispatches.tsv", DISPATCH_COLUMNS, DISPATCH_ENUMS)
                except csv.Error as error:
                    self.fail(f"B3: accepted {len(row['model'])}-character model "
                              f"cannot be read back: {error}")
                self.assertEqual(rows, [row])

    def test_accepted_unmatched_quote_id_reads_back_as_one_row(self):
        row = dict.fromkeys(DISPATCH_COLUMNS, "-")
        row.update(id='"seat', gate_id="g", round="1", date="2026-10-10",
                   repo="r", stage="review", setup="independent", trust="0",
                   family="openai", model="fixture", status="pending")
        with tempfile.TemporaryDirectory(prefix="rally-v3151-") as directory:
            with patch.dict(os.environ, {"ASKRUBBERDUCK_HOME": directory}):
                self.assertTrue(record(row, new=True))
                rows = read_table("dispatches.tsv", DISPATCH_COLUMNS, DISPATCH_ENUMS)
                self.assertEqual(len(rows), 1,
                                 'B3: accepted id \'"seat\' was written but no row read back')


if __name__ == "__main__":
    unittest.main()
