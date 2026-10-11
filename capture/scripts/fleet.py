"""Supervise independent account processes; each has one persistent profile."""
import logging
import os
from pathlib import Path
import signal
import subprocess
import sys
import threading
import time

from .runtime import StopRequested, shutdown_signals, wait

ACCOUNTS = ("foundations", "linear", "multivariable", "differential")


def run_fleet(argv):
    from .cli import parser
    from .storage import read_json
    args = parser().parse_args(argv)
    saved = read_json(args.config, {}) if args.config else {}
    scoped = ("account", "profile", "state_root", "output_root", "course_id")
    if any(getattr(args, key) for key in scoped) or any(saved.get(key) for key in scoped):
        parser().error("fleet uses all four separate account profiles; use run for account-specific overrides")
    forwarded = list(argv)
    forwarded[forwarded.index("fleet")] = "run"
    script = str(Path(__file__).resolve().parent)
    stop = threading.Event()
    children = {}
    with shutdown_signals(stop):
        try:
            while not stop.is_set():
                for account in ACCOUNTS:
                    process = children.get(account)
                    if process is None or process.poll() is not None:
                        if process is not None:
                            logging.warning("Restarting %s from its saved checkpoint (exit %s)", account, process.returncode)
                        children[account] = subprocess.Popen([sys.executable, script, *forwarded, "--account", account], start_new_session=True)
                wait(stop, 5)
        except StopRequested:
            pass
        finally:
            stop.set()
            for child in children.values():
                if child.poll() is None:
                    os.killpg(child.pid, signal.SIGTERM)
            deadline = time.monotonic() + 60
            for child in children.values():
                try:
                    child.wait(timeout=max(0, deadline - time.monotonic()))
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    child.wait()
    return 0
