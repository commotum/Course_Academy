#!/usr/bin/env python3
"""Adapt the local writer's stdin lifecycle to a systemd Type=notify service."""

from __future__ import annotations

import os
from pathlib import Path
import signal
import socket
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent


def notify_ready() -> None:
    address = os.environ.get("NOTIFY_SOCKET")
    if not address:
        return
    if address.startswith("@"):
        address = "\0" + address[1:]
    with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as notification:
        notification.connect(address)
        notification.sendall(b"READY=1")


def supervise(command: list[str]) -> int:
    child: subprocess.Popen | None = None
    stopping = False
    stop_sent = False

    def request_stop(_signum=None, _frame=None) -> None:
        nonlocal stopping, stop_sent
        stopping = True
        if child is None or stop_sent:
            return
        stop_sent = True
        try:
            # The writer drops its listener and releases its lease after a line
            # on stdin. A signal must not bypass that graceful shutdown path.
            child.stdin.write("\n")
            child.stdin.flush()
        except (BrokenPipeError, OSError):
            pass  # A writer that already exited needs no shutdown request.

    previous = {sig: signal.signal(sig, request_stop) for sig in (signal.SIGTERM, signal.SIGINT)}
    try:
        child = subprocess.Popen(
            command, cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace", bufsize=1,
        )
        if stopping:
            request_stop()
        ready = False
        for line in child.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
            if not ready and not stopping and line.startswith("READY endpoint="):
                notify_ready()
                ready = True
        status = child.wait()
        return status if status >= 0 else 128 - status
    finally:
        if child is not None:
            if child.poll() is None:
                request_stop()
                # The service's TimeoutStopSec/KillMode=mixed provide the hard
                # deadline without sending SIGTERM directly to the writer.
                child.wait()
            try:
                child.stdin.close()
            except (BrokenPipeError, OSError):
                pass
            child.stdout.close()
        for sig, handler in previous.items():
            signal.signal(sig, handler)


def main() -> int:
    try:
        return supervise(["/bin/bash", str(ROOT / "scripts/start_local_edb.sh")])
    except OSError:
        print("Could not supervise the local EDB writer.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
