#!/usr/bin/env python3
"""A cancel that lands while dispatch spawns a seat still stops the seat (gate v3.15.1 r3, GPT-6.1 Sol)."""
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
import dispatch  # noqa: E402
import ledger  # noqa: E402


class CancelDuringSpawn(unittest.TestCase):
    def test_seat_stopped_when_cancel_arrives_during_spawn(self):
        with tempfile.TemporaryDirectory(prefix="duck-cancel-spawn-") as directory:
            root = Path(directory).resolve()
            worktree = root / "worktree"
            worktree.mkdir()
            (root / "brief").write_text("work in the throwaway checkout")
            fake = root / "codex"
            fake.write_text("#!/bin/sh\nsleep 0.3\necho late > late-write.txt\n")
            fake.chmod(0o755)
            real_popen = subprocess.Popen

            def cancel_during_spawn(*args, **kwargs):
                child = real_popen(*args, **kwargs)
                os.kill(os.getpid(), signal.SIGTERM)  # after the child exists, before the guard
                return child

            env = {"PATH": f"{root}:{os.environ['PATH']}", "ASKRUBBERDUCK_HOME": str(root / "ledger")}
            with patch.dict(os.environ, env), \
                    patch.object(dispatch.subprocess, "Popen", cancel_during_spawn):
                with self.assertRaises(SystemExit) as stopped:
                    dispatch.main(["--gate", "cancel-spawn", "--round", "1", "--stage", "race",
                                   "--setup", "race", "--trust", "0", "--pin", "openai:fixture",
                                   "--prompt", str(root / "brief"), "--out", str(root / "out"),
                                   "--repo", "r", "--workdir", str(worktree)])
                rows = ledger.read_table("dispatches.tsv", ledger.DISPATCH_COLUMNS,
                                         ledger.DISPATCH_ENUMS)
            self.assertEqual(stopped.exception.code, 128 + signal.SIGTERM)
            self.assertEqual((rows[0]["status"], rows[0]["outage"]), ("final", "-"))
            time.sleep(0.6)  # past the seat's own write, had it survived
            self.assertFalse((worktree / "late-write.txt").exists(), "the cancelled seat ran on")


if __name__ == "__main__":
    unittest.main()
