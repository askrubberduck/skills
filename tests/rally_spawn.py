#!/usr/bin/env python3
"""Cancellation immediately after the pending row is durable must finalize it (C1)."""

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


class CancelDuringStop(unittest.TestCase):
    def test_cancel_during_term_grace_period_stops_seat_before_exit(self):
        with tempfile.TemporaryDirectory(prefix="duck-rally-stop-") as directory:
            root = Path(directory).resolve()
            fake = root / "codex"
            fake.write_text(f"#!{sys.executable}\n" + """
import os
import signal
import time
from pathlib import Path

root = Path(__file__).parent

def term_received(number, frame):
    (root / "term-received").write_text("SIGTERM")

signal.signal(signal.SIGTERM, term_received)
(root / "seat.pid").write_text(str(os.getpid()))
while not (root / "release").exists():
    time.sleep(0.01)
(root / "late-write").write_text("seat ran after dispatch exited")
""")
            fake.chmod(0o755)
            brief = root / "brief"
            brief.write_text("Review the fixture")
            home = root / "ledger"
            home.mkdir()
            (home / "config.toml").write_text('[bounds]\ndispatch_timeout = "1s"\n')
            env = {**os.environ, "PATH": str(root), "HOME": str(root),
                   "CODEX_HOME": str(root / "owner"), "ASKRUBBERDUCK_HOME": str(home)}
            seat_pid = None
            child = subprocess.Popen(
                [sys.executable, str(SCRIPTS / "dispatch.py"),
                 "--gate", "stop-cancel", "--round", "1", "--stage", "review",
                 "--setup", "independent", "--trust", "0", "--pin", "openai:fixture",
                 "--prompt", str(brief), "--out", str(root / "out"), "--repo", "r"],
                env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True)
            try:
                deadline = time.monotonic() + 10
                while not (root / "term-received").exists():
                    if child.poll() is not None or time.monotonic() >= deadline:
                        self.fail("fixture did not reach stop()'s SIGTERM grace period")
                    time.sleep(0.01)
                seat_pid = int((root / "seat.pid").read_text())
                child.send_signal(signal.SIGTERM)
                stdout, stderr = child.communicate(timeout=10)
                try:
                    os.killpg(seat_pid, 0)
                    seat_survived = True
                except (ProcessLookupError, PermissionError):
                    seat_survived = False
                # Release only after dispatch exits, so the write proves continued execution.
                (root / "release").touch()
                deadline = time.monotonic() + 1
                while not (root / "late-write").exists() and time.monotonic() < deadline:
                    time.sleep(0.01)
                with patch.dict(os.environ, env):
                    rows = ledger.read_table("dispatches.tsv", ledger.DISPATCH_COLUMNS,
                                             ledger.DISPATCH_ENUMS)
                self.assertEqual(len(rows), 1, stdout + stderr)
                observed = (child.returncode, rows[0]["status"], rows[0]["outage"],
                            seat_survived, (root / "late-write").exists())
                self.assertEqual(
                    observed, (128 + signal.SIGTERM, "final", "-", False, False),
                    "C1: cancel during stop() must finish killing the seat before dispatch exits; "
                    f"observed (exit, status, outage, seat_survived, late_write)={observed!r}; "
                    f"stdout={stdout!r}, stderr={stderr!r}")
            finally:
                if child.poll() is None:
                    child.kill()
                child.communicate(timeout=10)
                if seat_pid is None and (root / "seat.pid").exists():
                    seat_pid = int((root / "seat.pid").read_text())
                if seat_pid is not None:
                    try:
                        os.killpg(seat_pid, signal.SIGKILL)
                    except (ProcessLookupError, PermissionError):
                        pass


class IgnoredTermInheritance(unittest.TestCase):
    def test_launch_resets_inherited_ignored_sigterm_in_seat(self):
        with tempfile.TemporaryDirectory(prefix="duck-rally-ignored-term-") as directory:
            root = Path(directory).resolve()
            fake = root / "codex"
            fake.write_text(f"#!{sys.executable}\n" + """
import signal
import time
from pathlib import Path

root = Path(__file__).parent
(root / "disposition").write_text(str(int(signal.getsignal(signal.SIGTERM))))
time.sleep(0.6)
(root / "late-write").write_text("seat ignored stop()'s SIGTERM")
""")
            fake.chmod(0o755)
            driver = """
import signal
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
import dispatch

root = Path(sys.argv[2])
# POSIX exec preserves SIG_IGN; exercise launch() with that inherited state.
signal.signal(signal.SIGTERM, signal.SIG_IGN)
print(dispatch.launch([str(root / "codex")], root / "out", 0.3, root))
"""
            completed = subprocess.run(
                [sys.executable, "-c", driver, str(SCRIPTS), str(root)],
                stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            self.assertEqual(completed.stdout.strip(), "(True, -1)")
            observed = (int((root / "disposition").read_text()),
                        (root / "late-write").exists())
            self.assertEqual(
                observed, (int(signal.SIG_DFL), False),
                "C2: the seat must start with default SIGTERM even when launch() inherits "
                "SIG_IGN, so stop() can end it with SIGTERM; "
                f"observed (SIGTERM disposition, late_write)={observed!r}")


class CancelDuringSeatHomeFailure(unittest.TestCase):
    def test_cancel_finalizes_pending_row_when_seat_home_creation_fails(self):
        with tempfile.TemporaryDirectory(prefix="duck-rally-home-failure-") as directory:
            root = Path(directory).resolve()
            fake = root / "codex"
            fake.write_text("#!/bin/sh\nprintf 'started' > \"$0.started\"\n")
            fake.chmod(0o755)
            brief = root / "brief"
            brief.write_text("Review the fixture")
            unavailable = root / "temp-parent"
            unavailable.write_text("a file cannot hold temporary seat directories")
            driver = """
import os
import signal
import sys
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv.pop(1))
import dispatch

unavailable = sys.argv.pop(1)
real_mkdtemp = dispatch.tempfile.mkdtemp

def cancel_during_home_creation(*args, **kwargs):
    os.kill(os.getpid(), signal.SIGTERM)
    # Exercise a real filesystem failure after the pending row, before the guard.
    return real_mkdtemp(*args, dir=unavailable, **kwargs)

with patch.object(dispatch.tempfile, "mkdtemp", cancel_during_home_creation):
    raise SystemExit(dispatch.main(sys.argv[1:]))
"""
            env = {**os.environ, "PATH": str(root), "HOME": str(root),
                   "CODEX_HOME": str(root / "owner"),
                   "ASKRUBBERDUCK_HOME": str(root / "ledger")}
            completed = subprocess.run(
                [sys.executable, "-c", driver, str(SCRIPTS), str(unavailable),
                 "--gate", "home-failure-cancel", "--round", "1", "--stage", "review",
                 "--setup", "independent", "--trust", "0", "--pin", "openai:fixture",
                 "--prompt", str(brief), "--out", str(root / "out"), "--repo", "r"],
                env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10)
            with patch.dict(os.environ, env):
                rows = ledger.read_table("dispatches.tsv", ledger.DISPATCH_COLUMNS,
                                         ledger.DISPATCH_ENUMS)
            self.assertEqual(len(rows), 1, completed.stdout + completed.stderr)
            self.assertFalse((root / "codex.started").exists())
            observed = (completed.returncode, rows[0]["status"], rows[0]["outage"])
            self.assertEqual(
                observed, (128 + signal.SIGTERM, "final", "-"),
                "C1: a cancel after the pending row must exit 143 and finalize it even when "
                "seat-home creation fails before the guard; "
                f"observed {observed!r}. stdout={completed.stdout!r}, "
                f"stderr={completed.stderr!r}")


if __name__ == "__main__":
    unittest.main()
