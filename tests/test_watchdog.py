#!/usr/bin/env python3
"""The seat's watchdog: however dispatch ends, SIGKILL included, the seat stops and its row is final;
a seat's leftover children are stopped even when its leader exits first. Fake CLIs only."""
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


def alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False


class Watchdog(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="duck-watchdog-")
        self.root = Path(self.directory.name).resolve()
        (self.root / "brief").write_text("review the fixture")
        self.env = {**os.environ, "PATH": f"{self.root}:{os.environ['PATH']}", "HOME": str(self.root),
                    "CODEX_HOME": str(self.root / "owner"), "ASKRUBBERDUCK_HOME": str(self.root / "ledger")}

    def tearDown(self):
        for name in ("seat.pid", "child.pid"):
            if (self.root / name).exists():
                try:
                    os.kill(int((self.root / name).read_text()), signal.SIGKILL)
                except ProcessLookupError:
                    pass
        self.directory.cleanup()

    def fake(self, body: str) -> None:
        codex = self.root / "codex"  # a codex review seat's HOME is its own: name the root outright
        codex.write_text(f"#!/bin/sh\nROOT={self.root}\n{body}\n")
        codex.chmod(0o755)

    def dispatch(self, gate: str, **popen) -> subprocess.Popen:
        return subprocess.Popen(
            [sys.executable, str(SCRIPTS / "dispatch.py"), "--gate", gate, "--round", "1", "--stage",
             "review", "--setup", "independent", "--trust", "0", "--pin", "openai:fixture",
             "--prompt", str(self.root / "brief"), "--out", str(self.root / "out"), "--repo", "r"],
            env=self.env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, **popen)

    def row(self, row_id: str, wait: bool = True) -> dict:
        with patch.dict(os.environ, self.env):
            for _ in range(200 if wait else 1):
                rows = {r["id"]: r for r in ledger.read_table("dispatches.tsv", ledger.DISPATCH_COLUMNS,
                                                              ledger.DISPATCH_ENUMS)}
                if row_id in rows and rows[row_id]["status"] == "final":
                    break
                time.sleep(0.05)
        return rows[row_id]

    def test_sigkill_to_dispatch_stops_the_seat_and_finalizes_its_row(self):
        self.fake('echo $$ > "$ROOT/seat.pid"; sleep 30 & echo $! > "$ROOT/child.pid"; wait')
        child = self.dispatch("kill9")
        for _ in range(200):
            if (self.root / "child.pid").exists():
                break
            time.sleep(0.05)
        child.kill()  # SIGKILL: nothing in dispatch runs after this
        child.communicate(timeout=30)
        row = self.row("kill9-r1-review-fixture")
        self.assertEqual((row["status"], row["outage"], row["verdict"]), ("final", "-", "-"))
        time.sleep(0.3)
        self.assertFalse(alive(int((self.root / "child.pid").read_text())), "the seat outlived dispatch")

    def test_sigkill_before_the_seat_starts_finalizes_its_row(self):
        self.fake("exit 0")
        killed = subprocess.run(
            [sys.executable, "-c", "import os, sys; sys.path.insert(0, sys.argv.pop(1)); import dispatch\n"
             "dispatch.launch = lambda *a: os.kill(os.getpid(), 9)\n"
             "dispatch.main(sys.argv[1:])", str(SCRIPTS), "--gate", "early", "--round", "1",
             "--stage", "review", "--setup", "independent", "--trust", "0", "--pin", "openai:fixture",
             "--prompt", str(self.root / "brief"), "--out", str(self.root / "out"), "--repo", "r"],
            env=self.env, capture_output=True, timeout=30)
        self.assertEqual(killed.returncode, -signal.SIGKILL, killed.stderr)
        row = self.row("early-r1-review-fixture")
        self.assertEqual((row["status"], row["outage"], row["verdict"]), ("final", "-", "-"))

    def test_sigterm_the_caller_blocked_still_ends_dispatch(self):
        self.fake('echo $$ > "$ROOT/seat.pid"; sleep 30')
        child = self.dispatch("blocked", preexec_fn=lambda: signal.pthread_sigmask(
            signal.SIG_BLOCK, {signal.SIGTERM}))
        for _ in range(200):
            if (self.root / "seat.pid").exists():
                break
            time.sleep(0.05)
        child.terminate()
        child.communicate(timeout=30)
        self.assertEqual(child.returncode, -signal.SIGTERM)
        row = self.row("blocked-r1-review-fixture")
        self.assertEqual((row["status"], row["outage"], row["verdict"]), ("final", "-", "-"))

    def test_a_seat_child_still_gets_sigterm_time_after_its_leader_exits(self):
        self.fake("(trap 'sleep 0.2; : > \"$ROOT/answer\"; exit 0' TERM; while :; do sleep 0.05; done) &\n"
                  "sleep 0.5; printf 'VERDICT: NOTE\\n' > \"$3\"; exit 0")
        out = self.dispatch("grace").communicate(timeout=60)[0]
        self.assertTrue((self.root / "answer").exists(), out)  # it ran its handler, not a SIGKILL

    def test_a_term_to_dispatch_and_its_watchdog_still_stops_the_seat(self):
        self.fake('echo $$ > "$ROOT/seat.pid"; sleep 30 & echo $! > "$ROOT/child.pid"; wait')
        child = self.dispatch("pkill")
        for _ in range(200):
            if (self.root / "child.pid").exists():
                break
            time.sleep(0.05)
        watchdogs = subprocess.run(["pgrep", "-f", "dispatch.py --watchdog"], capture_output=True,
                                   text=True).stdout.split()
        for pid in [child.pid, *map(int, watchdogs)]:  # what pkill -f dispatch.py would do
            os.kill(pid, signal.SIGTERM)
        child.communicate(timeout=30)
        row = self.row("pkill-r1-review-fixture")
        self.assertEqual((row["status"], row["outage"], row["verdict"]), ("final", "-", "-"))
        time.sleep(0.3)
        self.assertFalse(alive(int((self.root / "child.pid").read_text())), "the seat outlived dispatch")

    def test_a_seat_child_that_ignores_sigterm_is_stopped_when_its_leader_exits(self):
        self.fake("(trap '' TERM; sleep 30) & echo $! > \"$ROOT/child.pid\"\n"
                  "printf 'VERDICT: NOTE\\n' > \"$3\"; exit 0")
        child = self.dispatch("left")
        out = child.communicate(timeout=60)[0]
        self.assertEqual(child.returncode, 0, out)
        self.assertEqual(self.row("left-r1-review-fixture", wait=False)["verdict"], "NOTE")
        self.assertFalse(alive(int((self.root / "child.pid").read_text())), "a seat child outlived it")


if __name__ == "__main__":
    unittest.main()
