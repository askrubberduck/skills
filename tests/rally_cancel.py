#!/usr/bin/env python3
"""Cancel-lifetime rally, serve 1: an inherited blocked cancel must still end the seat."""

import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "duck-review" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import ledger  # noqa: E402


class InheritedBlockedCancel(unittest.TestCase):
    def test_sigterm_after_pending_cancels_even_with_inherited_blocked_sigterm(self):
        with tempfile.TemporaryDirectory(prefix="duck-rally-blocked-cancel-") as directory:
            root = Path(directory).resolve()
            fake = root / "codex"
            fake.write_text(f"#!{sys.executable}\n" + """
import os
import sys
import time
from pathlib import Path

root = Path(__file__).parent
(root / "seat.pid").write_text(str(os.getpid()))
while not (root / "release").exists():
    time.sleep(0.01)
(root / "late-write").write_text("seat continued after cancel")
Path(sys.argv[3]).write_text("VERDICT: NOTE\\n")
""")
            fake.chmod(0o755)
            brief = root / "brief"
            brief.write_text("Review the fixture")
            env = {**os.environ, "PATH": str(root), "HOME": str(root),
                   "CODEX_HOME": str(root / "owner"),
                   "ASKRUBBERDUCK_HOME": str(root / "ledger")}
            child = subprocess.Popen(
                [sys.executable, str(SCRIPTS / "dispatch.py"),
                 "--gate", "blocked-cancel", "--round", "1", "--stage", "review",
                 "--setup", "independent", "--trust", "0", "--pin", "openai:fixture",
                 "--prompt", str(brief), "--out", str(root / "out"), "--repo", "r"],
                env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True,
                preexec_fn=lambda: signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGTERM}))
            seat_pid = None
            try:
                deadline = time.monotonic() + 10
                while not (root / "seat.pid").exists():
                    if child.poll() is not None or time.monotonic() >= deadline:
                        self.fail("fixture did not start its fake seat")
                    time.sleep(0.01)
                seat_pid = int((root / "seat.pid").read_text())
                with patch.dict(os.environ, env):
                    before = ledger.read_table("dispatches.tsv", ledger.DISPATCH_COLUMNS,
                                               ledger.DISPATCH_ENUMS)
                self.assertEqual((len(before), before[0]["status"]), (1, "pending"))
                child.send_signal(signal.SIGTERM)
                try:
                    stdout, stderr = child.communicate(timeout=3)
                except subprocess.TimeoutExpired:
                    # The seat cannot decide an outcome before this external release.
                    (root / "release").touch()
                    stdout, stderr = child.communicate(timeout=10)
                with patch.dict(os.environ, env):
                    rows = ledger.read_table("dispatches.tsv", ledger.DISPATCH_COLUMNS,
                                             ledger.DISPATCH_ENUMS)
                self.assertEqual(len(rows), 1, stdout + stderr)
                observed = (child.returncode, rows[0]["status"], rows[0]["outage"],
                            rows[0]["verdict"], (root / "late-write").exists())
                self.assertEqual(
                    observed, (128 + signal.SIGTERM, "final", "-", "-", False),
                    "C1: SIGTERM after the pending row must cancel despite an inherited blocked "
                    "SIGTERM; observed (exit, status, outage, verdict, late_write)="
                    f"{observed!r}; stdout={stdout!r}, stderr={stderr!r}")
            finally:
                if child.poll() is None:
                    child.kill()
                child.communicate(timeout=10)
                if seat_pid is not None:
                    try:
                        os.killpg(seat_pid, signal.SIGKILL)
                    except (ProcessLookupError, PermissionError):
                        pass


if __name__ == "__main__":
    unittest.main()
