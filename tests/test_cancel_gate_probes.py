#!/usr/bin/env python3
"""The v3.15.2 gate's cancel reproductions (GPT-6.1 Sol, round 1), kept as tests: the first cancel wins,
the seat is stopped, the row is final, and dispatch leaves even with a full stdout."""
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "duck-review" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import ledger  # noqa: E402

PRELUDE = "import os, signal, sys\nsys.dont_write_bytecode = True\nsys.path.insert(0, sys.argv.pop(1))\nimport dispatch\n"
DRIVERS = {
    # a second signal during cleanup must not replace the first, nor cut cleanup short
    "second_signal": """
from unittest.mock import patch
real_rmtree = dispatch.shutil.rmtree
def second(*a, **kw):
    os.kill(os.getpid(), signal.SIGHUP)
    return real_rmtree(*a, **kw)
with patch.object(dispatch.shutil, 'rmtree', second):
    raise SystemExit(dispatch.main(sys.argv[1:]))
""",
    # a cancel at finish() entry, with stdout a full pipe and output already buffered
    "fallback_stdout": """
def inject(frame, event, arg):
    if event == 'call' and frame.f_code.co_name == 'finish':
        sys.settrace(None)
        os.kill(os.getpid(), signal.SIGTERM)
    return inject
sys.settrace(inject)
raise SystemExit(dispatch.main(sys.argv[1:]))
""",
    # a first cancel at stop() entry, then a second one at once
    "fallback_second": """
from unittest.mock import patch
real_stop = dispatch.stop
fired = []
def first_at_stop(child):
    if not fired:
        fired.append(1)
        os.kill(os.getpid(), signal.SIGTERM)
        os.kill(os.getpid(), signal.SIGHUP)
    return real_stop(child)
with patch.object(dispatch, 'stop', first_at_stop):
    raise SystemExit(dispatch.main(sys.argv[1:]))
""",
}


class GateProbes(unittest.TestCase):
    def run_probe(self, name: str) -> None:
        with tempfile.TemporaryDirectory(prefix=f"duck-gate-{name}-") as directory:
            root = Path(directory).resolve()
            home = root / "ledger"
            home.mkdir()
            (home / "config.toml").write_text('[bounds]\ndispatch_timeout = "0.5s"\n')
            (root / "brief").write_text("Review fixture")
            body = ("import os, sys, time\nfrom pathlib import Path\nroot = Path(__file__).parent\n"
                    "(root / 'seat.pid').write_text(str(os.getpid()))\n")
            if name == "fallback_stdout":
                body += "Path(sys.argv[3]).write_text('VERDICT: NOTE\\n')\n(root / 'out').unlink()\n"
            else:
                body += ("while not (root / 'release').exists(): time.sleep(0.01)\n"
                         "(root / 'late-write').write_text('seat survived dispatch')\n")
            fake = root / "codex"
            fake.write_text(f"#!{sys.executable}\n" + body)
            fake.chmod(0o755)
            env = {**os.environ, "PATH": str(root), "HOME": str(root), "CODEX_HOME": str(root / "owner"),
                   "ASKRUBBERDUCK_HOME": str(home)}
            args = ["--gate", name, "--round", "4", "--extended", "owner extension", "--stage", "review",
                    "--setup", "independent", "--trust", "0", "--pin", "openai:fixture",
                    "--prompt", str(root / "brief"), "--out", str(root / "out"), "--repo", "r"]
            reader = writer = None
            stdout = subprocess.PIPE
            if name == "fallback_stdout":  # a full pipe nobody reads
                reader, writer = os.pipe()
                os.set_blocking(writer, False)
                while True:
                    try:
                        os.write(writer, b"x" * 4096)
                    except BlockingIOError:
                        break
                os.set_blocking(writer, True)
                stdout = writer
            child = subprocess.Popen([sys.executable, "-c", PRELUDE + DRIVERS[name], str(SCRIPTS), *args],
                                     env=env, stdout=stdout, stderr=subprocess.PIPE)
            seat_pid = None
            try:
                deadline = time.monotonic() + 5
                while not (root / "seat.pid").exists() and child.poll() is None and time.monotonic() < deadline:
                    time.sleep(0.01)
                if (root / "seat.pid").exists():
                    seat_pid = int((root / "seat.pid").read_text())
                if name == "second_signal":
                    child.send_signal(signal.SIGTERM)
                try:
                    child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.fail(f"{name}: dispatch hung")
                alive = False
                if seat_pid:
                    try:
                        os.kill(seat_pid, 0)
                        alive = True
                    except ProcessLookupError:
                        pass
                (root / "release").touch()
                time.sleep(0.2)
                os.environ["ASKRUBBERDUCK_HOME"], saved = str(home), os.environ.get("ASKRUBBERDUCK_HOME")
                try:
                    rows = ledger.read_table("dispatches.tsv", ledger.DISPATCH_COLUMNS, ledger.DISPATCH_ENUMS)
                finally:
                    if saved is None:
                        del os.environ["ASKRUBBERDUCK_HOME"]
                    else:
                        os.environ["ASKRUBBERDUCK_HOME"] = saved
                self.assertEqual((child.returncode, alive, (root / "late-write").exists(),
                                  rows[0]["status"], rows[0]["outage"]),
                                 (128 + signal.SIGTERM, False, False, "final", "-"), name)
            finally:
                if child.poll() is None:
                    child.kill()
                child.wait(timeout=5)
                if seat_pid:
                    try:
                        os.killpg(seat_pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                for fd in (writer, reader):
                    if fd is not None:
                        os.close(fd)

    def test_second_signal(self):
        self.run_probe("second_signal")

    def test_fallback_stdout(self):
        self.run_probe("fallback_stdout")

    def test_fallback_second(self):
        self.run_probe("fallback_second")


if __name__ == "__main__":
    unittest.main()
