#!/usr/bin/env python3
"""Cancellation immediately after the pending row is durable must finalize it (C1)."""

import os
import signal
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "duck-review" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import ledger  # noqa: E402


class CancelAfterPending(unittest.TestCase):
    def test_sigterm_immediately_after_pending_write_finalizes_row(self):
        with tempfile.TemporaryDirectory(prefix="duck-rally-pending-") as directory:
            root = Path(directory).resolve()
            fake = root / "codex"
            fake.write_text("#!/bin/sh\nprintf 'VERDICT: NOTE\\n' > \"$3\"\n")
            fake.chmod(0o755)
            brief = root / "brief"
            brief.write_text("Review the fixture")
            driver = """
import os
import signal
import sys
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv.pop(1))
import dispatch

real_record = dispatch.record

def cancel_after_pending(row, new):
    written = real_record(row, new)
    if new and written:
        os.kill(os.getpid(), signal.SIGTERM)
    return written

with patch.object(dispatch, "record", cancel_after_pending):
    raise SystemExit(dispatch.main(sys.argv[1:]))
"""
            env = {**os.environ, "PATH": str(root), "HOME": str(root),
                   "CODEX_HOME": str(root / "owner"),
                   "ASKRUBBERDUCK_HOME": str(root / "ledger")}
            completed = subprocess.run(
                [sys.executable, "-c", driver, str(SCRIPTS),
                 "--gate", "pending-cancel", "--round", "1", "--stage", "review",
                 "--setup", "independent", "--trust", "0", "--pin", "openai:fixture",
                 "--prompt", str(brief), "--out", str(root / "out"), "--repo", "r"],
                env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10)
            with patch.dict(os.environ, env):
                rows = ledger.read_table("dispatches.tsv", ledger.DISPATCH_COLUMNS,
                                         ledger.DISPATCH_ENUMS)
            self.assertEqual(len(rows), 1, completed.stdout + completed.stderr)
            observed = (completed.returncode, rows[0]["status"], rows[0]["outage"])
            self.assertEqual(
                observed, (128 + signal.SIGTERM, "final", "-"),
                "C1: SIGTERM after the pending write must exit 143 and finalize the row; "
                f"observed {observed!r}. stdout={completed.stdout!r}, "
                f"stderr={completed.stderr!r}")


if __name__ == "__main__":
    unittest.main()
