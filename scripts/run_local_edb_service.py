#!/usr/bin/env python3
"""Supervise the math database, reusing processes already serving capture jobs."""

from __future__ import annotations

import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import threading
import time


ROOT = Path(__file__).resolve().parent.parent
MATH_ROOT = Path(os.environ.get("EDB_MATH_ROOT", "/media/jake/SSD/EDB/math"))
PG_CTL = Path(os.environ.get(
    "PG_CTL", "/usr/local/MATLAB/R2025b/sys/postgresql/glnxa64/PostgreSQL/bin/pg_ctl",
))
PG_DATA = Path(os.environ.get("EDB_PG_DATA_DIR", str(MATH_ROOT / "postgres")))
PG_RUN = Path(os.environ.get("EDB_PG_RUN_DIR", "/tmp/edb-math"))
PG_PORT = os.environ.get("EDB_PG_PORT", "55432")
ENDPOINT = Path(os.environ.get("EDB_ENDPOINT", str(PG_RUN / "writer.sock")))
WRITER_BINARY = Path(os.environ.get(
    "EDB_WRITER_BINARY", str(MATH_ROOT / "bin/course-academy-transactor"),
))


def postgres_running() -> bool:
    return subprocess.run(
        [str(PG_CTL), "-D", str(PG_DATA), "status"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def private_directory(path: Path) -> None:
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    path.chmod(0o700)


def writer_running() -> bool:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.settimeout(1)
        try:
            connection.connect(str(ENDPOINT))
            return True
        except (FileNotFoundError, ConnectionRefusedError):
            return False


def reuse_writer() -> int:
    """Observe an existing writer without taking ownership of its lifetime."""
    stopping = threading.Event()
    previous = {
        sig: signal.signal(sig, lambda _signum, _frame: stopping.set())
        for sig in (signal.SIGTERM, signal.SIGINT)
    }
    try:
        print(f"REUSE endpoint={ENDPOINT}", flush=True)
        notify_ready()
        while not stopping.wait(2):
            if not writer_running():
                # Restart the service to recover the writer only after its
                # external owner is no longer serving the shared endpoint.
                return 1
        return 0
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)


def supervise_postgres() -> int:
    """Own newly started PostgreSQL; only observe an already running cluster."""
    stopping = threading.Event()
    previous = {
        sig: signal.signal(sig, lambda _signum, _frame: stopping.set())
        for sig in (signal.SIGTERM, signal.SIGINT)
    }
    child = None
    log = None
    try:
        if not (PG_DATA / "PG_VERSION").is_file():
            raise OSError(f"PostgreSQL cluster is missing: {PG_DATA}")
        if not postgres_running():
            private_directory(PG_RUN)
            log = (MATH_ROOT / "postgres.log").open("a")
            child = subprocess.Popen(
                [str(PG_CTL.with_name("postgres")), "-D", str(PG_DATA)],
                stdout=log, stderr=subprocess.STDOUT,
            )
        ready = False
        deadline = time.monotonic() + 60
        while not stopping.is_set():
            if child is not None:
                if child.poll() is not None:
                    return child.returncode or 1
            elif not postgres_running():
                return 1
            if not ready:
                result = subprocess.run(
                    [str(PG_CTL.with_name("pg_isready")), "-h", str(PG_RUN), "-p", PG_PORT],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
                if result.returncode == 0:
                    print(f"{'START' if child else 'REUSE'} postgres={PG_DATA}", flush=True)
                    notify_ready()
                    ready = True
                elif time.monotonic() >= deadline:
                    raise OSError(f"PostgreSQL did not become ready at {PG_RUN}:{PG_PORT}")
            stopping.wait(2)
        return 0
    finally:
        if child is not None and child.poll() is None:
            child.send_signal(signal.SIGINT)
            child.wait()
        if log is not None:
            log.close()
        for sig, handler in previous.items():
            signal.signal(sig, handler)


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
        if sys.argv[1:] == ["--postgres"]:
            return supervise_postgres()
        if sys.argv[1:] not in ([], ["--writer"]):
            print("usage: start_local_edb.sh [--postgres | --writer]", file=sys.stderr)
            return 2
        if writer_running():
            return reuse_writer()
        if not WRITER_BINARY.is_file() or not os.access(WRITER_BINARY, os.X_OK):
            raise OSError(f"Math writer binary is missing or not executable: {WRITER_BINARY}")
        private_directory(PG_RUN)
        private_directory(ENDPOINT.parent)
        if not postgres_running():
            if sys.argv[1:] == ["--writer"]:
                raise OSError("Math PostgreSQL is unavailable; waiting for its service to recover")
            # Supports manual startup too. Under systemd, the separate math
            # PostgreSQL unit has already started before this writer unit.
            subprocess.run(
                [str(PG_CTL), "-D", str(PG_DATA), "-l", str(MATH_ROOT / "postgres.log"),
                 "-w", "-t", "60", "start"],
                check=True,
            )
        os.environ.setdefault(
            "EDB_POSTGRES_URL",
            f"host={PG_RUN} port={PG_PORT} dbname=math user=edb_writer "
            "sslmode=disable options='-c search_path=public'",
        )
        return supervise([
            str(WRITER_BINARY), os.environ.get("EDB_DATABASE", "math"), str(ENDPOINT),
        ])
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"Could not supervise math EDB: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
