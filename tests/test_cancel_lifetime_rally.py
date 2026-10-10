#!/usr/bin/env python3
"""A cancel at any moment finalizes the row and stops the seat: cancel-lifetime rally serves 2, 4-7 (GPT-6.1 Sol, 2026-10-10)."""

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


class CancelDuringCleanup(unittest.TestCase):
    def test_second_cancel_during_home_cleanup_still_finalizes_cancelled_row(self):
        with tempfile.TemporaryDirectory(prefix="duck-rally-cleanup-cancel-") as directory:
            root = Path(directory).resolve()
            fake = root / "codex"
            fake.write_text(f"#!{sys.executable}\n" + """
import os
import time
from pathlib import Path

root = Path(__file__).parent
(root / "seat.pid").write_text(str(os.getpid()))
while not (root / "release").exists():
    time.sleep(0.01)
(root / "late-write").write_text("seat continued after cancel")
""")
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

real_rmtree = dispatch.shutil.rmtree

def cancel_during_cleanup(*args, **kwargs):
    # A second caller cancel lands while unwinding the first, before the final row.
    os.kill(os.getpid(), signal.SIGTERM)
    return real_rmtree(*args, **kwargs)

with patch.object(dispatch.shutil, "rmtree", cancel_during_cleanup):
    raise SystemExit(dispatch.main(sys.argv[1:]))
"""
            env = {**os.environ, "PATH": str(root), "HOME": str(root),
                   "CODEX_HOME": str(root / "owner"), "TMPDIR": str(root),
                   "ASKRUBBERDUCK_HOME": str(root / "ledger")}
            child = subprocess.Popen(
                [sys.executable, "-c", driver, str(SCRIPTS),
                 "--gate", "cleanup-cancel", "--round", "1", "--stage", "review",
                 "--setup", "independent", "--trust", "0", "--pin", "openai:fixture",
                 "--prompt", str(brief), "--out", str(root / "out"), "--repo", "r"],
                env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True)
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
                stdout, stderr = child.communicate(timeout=10)
                try:
                    os.killpg(seat_pid, 0)
                    seat_survived = True
                except (ProcessLookupError, PermissionError):
                    seat_survived = False
                (root / "release").touch()
                with patch.dict(os.environ, env):
                    rows = ledger.read_table("dispatches.tsv", ledger.DISPATCH_COLUMNS,
                                             ledger.DISPATCH_ENUMS)
                self.assertEqual(len(rows), 1, stdout + stderr)
                observed = (child.returncode, rows[0]["status"], rows[0]["outage"],
                            rows[0]["verdict"], seat_survived)
                self.assertEqual(
                    observed, (128 + signal.SIGTERM, "final", "-", "-", False),
                    "C1: another cancel during cleanup must still finalize the cancelled row; "
                    f"observed (exit, status, outage, verdict, seat_survived)={observed!r}; "
                    f"stdout={stdout!r}, stderr={stderr!r}")
            finally:
                if child.poll() is None:
                    child.kill()
                child.communicate(timeout=10)
                if seat_pid is not None:
                    try:
                        os.killpg(seat_pid, signal.SIGKILL)
                    except (ProcessLookupError, PermissionError):
                        pass


class CancelEnteringFinalizer(unittest.TestCase):
    def test_first_cancel_entering_finalizer_after_output_read_failure_finalizes_row(self):
        with tempfile.TemporaryDirectory(prefix="duck-rally-finalizer-entry-") as directory:
            root = Path(directory).resolve()
            fake = root / "codex"
            fake.write_text(f"#!{sys.executable}\n" + """
import sys
from pathlib import Path

root = Path(__file__).parent
Path(sys.argv[3]).write_text("VERDICT: NOTE\\n")
# The open stdout descriptor remains valid, but dispatch's subsequent read fails.
(root / "out").unlink()
""")
            fake.chmod(0o755)
            brief = root / "brief"
            brief.write_text("Review the fixture")
            driver = """
import os
import signal
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv.pop(1))
import dispatch

armed = False

def cancel_at_finalizer_entry(frame, event, arg):
    global armed
    if frame.f_code is dispatch.run_seat.__code__:
        if event == "exception" and isinstance(arg[1], FileNotFoundError):
            armed = bool(frame.f_locals.get("ours"))
        elif event == "line" and armed:
            # Deliver at the first finalizer instruction, before it holds signals.
            # The output read failed before classify() could decide an outcome.
            armed = False
            sys.settrace(None)
            os.kill(os.getpid(), signal.SIGTERM)
    return cancel_at_finalizer_entry

sys.settrace(cancel_at_finalizer_entry)
raise SystemExit(dispatch.main(sys.argv[1:]))
"""
            env = {**os.environ, "PATH": str(root), "HOME": str(root),
                   "CODEX_HOME": str(root / "owner"), "TMPDIR": str(root),
                   "ASKRUBBERDUCK_HOME": str(root / "ledger")}
            completed = subprocess.run(
                [sys.executable, "-c", driver, str(SCRIPTS),
                 "--gate", "finalizer-entry-cancel", "--round", "1", "--stage", "review",
                 "--setup", "independent", "--trust", "0", "--pin", "openai:fixture",
                 "--prompt", str(brief), "--out", str(root / "out"), "--repo", "r"],
                env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10)
            with patch.dict(os.environ, env):
                rows = ledger.read_table("dispatches.tsv", ledger.DISPATCH_COLUMNS,
                                         ledger.DISPATCH_ENUMS)
            self.assertEqual(len(rows), 1, completed.stdout + completed.stderr)
            observed = (completed.returncode, rows[0]["status"], rows[0]["outage"],
                        rows[0]["verdict"])
            self.assertEqual(
                observed, (128 + signal.SIGTERM, "final", "-", "-"),
                "C1: a first cancel entering finalization, after pending and before an outcome "
                "is decided, must finalize the cancelled row; "
                f"observed (exit, status, outage, verdict)={observed!r}; "
                f"stdout={completed.stdout!r}, stderr={completed.stderr!r}")


class CancelWithBackpressuredStdout(unittest.TestCase):
    def test_cancel_exits_without_a_reader_draining_its_open_stdout_pipe(self):
        with tempfile.TemporaryDirectory(prefix="duck-rally-full-stdout-") as directory:
            root = Path(directory).resolve()
            fake = root / "codex"
            fake.write_text(f"#!{sys.executable}\n" + """
import os
import time
from pathlib import Path

root = Path(__file__).parent
(root / "seat.pid").write_text(str(os.getpid()))
while True:
    time.sleep(0.01)
""")
            fake.chmod(0o755)
            brief = root / "brief"
            brief.write_text("Review the fixture")
            env = {**os.environ, "PATH": str(root), "HOME": str(root),
                   "CODEX_HOME": str(root / "owner"),
                   "ASKRUBBERDUCK_HOME": str(root / "ledger")}
            reader, writer = os.pipe()
            child, seat_pid = None, None
            try:
                # Keep the read end open: this is backpressure, not closed stdout (C2).
                os.set_blocking(writer, False)
                for chunk in (b"x" * 4096, b"x"):
                    while True:
                        try:
                            os.write(writer, chunk)
                        except BlockingIOError:
                            break
                os.set_blocking(writer, True)
                child = subprocess.Popen(
                    [sys.executable, str(SCRIPTS / "dispatch.py"),
                     "--gate", "full-stdout-cancel", "--round", "1", "--stage", "review",
                     "--setup", "independent", "--trust", "0", "--pin", "openai:fixture",
                     "--prompt", str(brief), "--out", str(root / "out"), "--repo", "r"],
                    env=env, stdin=subprocess.DEVNULL, stdout=writer,
                    stderr=subprocess.PIPE, text=True)
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
                    child.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    pass
                with patch.dict(os.environ, env):
                    rows = ledger.read_table("dispatches.tsv", ledger.DISPATCH_COLUMNS,
                                             ledger.DISPATCH_ENUMS)
                self.assertEqual(len(rows), 1)
                try:
                    os.killpg(seat_pid, 0)
                    seat_survived = True
                except (ProcessLookupError, PermissionError):
                    seat_survived = False
                observed = (child.poll(), rows[0]["status"], rows[0]["outage"],
                            rows[0]["verdict"], seat_survived)
                self.assertEqual(
                    observed, (128 + signal.SIGTERM, "final", "-", "-", False),
                    "C1: SIGTERM after pending must end dispatch without requiring its caller "
                    "to drain an open, full stdout pipe; "
                    f"observed (exit, status, outage, verdict, seat_survived)={observed!r}")
            finally:
                if child is not None:
                    if child.poll() is None:
                        child.kill()
                    child.communicate(timeout=10)
                if seat_pid is not None:
                    try:
                        os.killpg(seat_pid, signal.SIGKILL)
                    except (ProcessLookupError, PermissionError):
                        pass
                os.close(writer)
                os.close(reader)


class CancelEnteringSeatStop(unittest.TestCase):
    def test_first_cancel_entering_seat_cleanup_leaves_no_running_seat(self):
        with tempfile.TemporaryDirectory(prefix="duck-rally-stop-entry-") as directory:
            root = Path(directory).resolve()
            fake = root / "codex"
            fake.write_text(f"#!{sys.executable}\n" + """
import os
import time
from pathlib import Path

root = Path(__file__).parent
(root / "seat.pid").write_text(str(os.getpid()))
while not (root / "release").exists():
    time.sleep(0.01)
(root / "late-write").write_text("seat continued after dispatch exited")
while True:
    time.sleep(0.01)
""")
            fake.chmod(0o755)
            brief = root / "brief"
            brief.write_text("Review the fixture")
            home = root / "ledger"
            home.mkdir()
            (home / "config.toml").write_text('[bounds]\ndispatch_timeout = "1s"\n')
            driver = """
import os
import signal
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv.pop(1))
import dispatch

def cancel_at_stop_entry(frame, event, arg):
    if event == "call" and frame.f_code is dispatch.stop.__code__:
        # The real wait timed out; classification has not decided the row's outcome.
        # Deliver the first cancel before the cleanup function can hold signals.
        sys.settrace(None)
        os.kill(os.getpid(), signal.SIGTERM)
    return cancel_at_stop_entry

sys.settrace(cancel_at_stop_entry)
raise SystemExit(dispatch.main(sys.argv[1:]))
"""
            env = {**os.environ, "PATH": str(root), "HOME": str(root),
                   "CODEX_HOME": str(root / "owner"), "TMPDIR": str(root),
                   "ASKRUBBERDUCK_HOME": str(home)}
            child, seat_pid = None, None
            try:
                child = subprocess.Popen(
                    [sys.executable, "-c", driver, str(SCRIPTS),
                     "--gate", "stop-entry-cancel", "--round", "1", "--stage", "review",
                     "--setup", "independent", "--trust", "0", "--pin", "openai:fixture",
                     "--prompt", str(brief), "--out", str(root / "out"), "--repo", "r"],
                    env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, text=True)
                stdout, stderr = child.communicate(timeout=10)
                self.assertTrue((root / "seat.pid").exists(), stdout + stderr)
                seat_pid = int((root / "seat.pid").read_text())
                try:
                    os.killpg(seat_pid, 0)
                    seat_survived = True
                except (ProcessLookupError, PermissionError):
                    seat_survived = False
                # Only release after dispatch exits, so the write proves continued execution.
                (root / "release").touch()
                deadline = time.monotonic() + 1
                while not (root / "late-write").exists() and time.monotonic() < deadline:
                    time.sleep(0.01)
                with patch.dict(os.environ, env):
                    rows = ledger.read_table("dispatches.tsv", ledger.DISPATCH_COLUMNS,
                                             ledger.DISPATCH_ENUMS)
                self.assertEqual(len(rows), 1, stdout + stderr)
                observed = (child.returncode, rows[0]["status"], rows[0]["outage"],
                            rows[0]["verdict"], seat_survived, (root / "late-write").exists())
                self.assertEqual(
                    observed, (128 + signal.SIGTERM, "final", "-", "-", False, False),
                    "C1: a first cancel entering seat cleanup must stop the process group "
                    "before dispatch exits; observed "
                    f"(exit, status, outage, verdict, seat_survived, late_write)={observed!r}; "
                    f"stdout={stdout!r}, stderr={stderr!r}")
            finally:
                if child is not None:
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


if __name__ == "__main__":
    unittest.main()
