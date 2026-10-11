"""Durable local records and process locks shared by every phase."""
from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
import fcntl
import json
import logging
import os
from pathlib import Path
import tempfile
import time


def _sync_directory(directory: Path) -> None:
    descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def atomic_bytes(path, data: bytes) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        _sync_directory(path.parent)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def atomic_text(path, text: str) -> None:
    atomic_bytes(path, text.encode("utf-8"))


def atomic_json(path, value) -> None:
    path = Path(path)
    # Preserve insertion order: presentation order survives a restart and is used
    # by lesson sampling. Hashing callers canonicalize their own request payloads.
    data = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    if path.exists():
        previous = path.read_bytes()
        # A malformed record must not replace the last readable checkpoint.
        try:
            json.loads(previous)
        except (ValueError, UnicodeError):
            pass
        else:
            atomic_bytes(path.with_name(path.name + ".previous"), previous)
    atomic_bytes(path, data)


def read_json(path, default=None):
    path = Path(path)
    if not path.exists():
        return deepcopy(default)
    try:
        return json.loads(path.read_text())
    except (ValueError, UnicodeError):
        previous = path.with_name(path.name + ".previous")
        if not previous.exists():
            raise
        result = json.loads(previous.read_text())
        logging.warning("Recovered readable prior checkpoint for %s; source actions will be reconciled", path)
        return result


def append_event(path, event, **values) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"at": time.time(), "event": event, **values}
    data = (json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n").encode()
    with path.open("ab") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


@contextmanager
def file_lock(path, blocking=True):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB))
        try:
            yield stream
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)
