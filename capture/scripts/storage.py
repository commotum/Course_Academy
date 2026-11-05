"""Durable local records and process locks shared by every phase."""
from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
import fcntl
import gzip
import json
import logging
import os
from pathlib import Path
import tempfile
import time

BACKUP_COMPRESSION_BYTES = 1024 * 1024


def json_backup_paths(path):
    path = Path(path)
    return (path.with_name(path.name + '.previous'), path.with_name(path.name + '.previous.gz'))


def read_json_backup(path):
    """Return the selected backup path and its exact uncompressed bytes."""
    candidates = [p for p in json_backup_paths(path) if p.exists()]
    if not candidates:
        return None, None
    # A crash between publishing a new backup and removing the old format can
    # leave both. The most recently published readable copy is authoritative.
    for candidate in sorted(candidates, key=lambda p: p.stat().st_mtime_ns, reverse=True):
        try:
            data = candidate.read_bytes()
            if candidate.suffix == '.gz':
                data = gzip.decompress(data)
            json.loads(data)
            return candidate, data
        except (ValueError, UnicodeError, OSError, EOFError):
            continue
    raise ValueError('No readable JSON backup for ' + str(path))


def write_json_backup(path, data):
    """Keep a standalone recovery copy; large backups retain exact bytes in gzip."""
    plain, compressed = json_backup_paths(path)
    target, stale = (compressed, plain) if len(data) >= BACKUP_COMPRESSION_BYTES else (plain, compressed)
    stored = gzip.compress(data, compresslevel=3, mtime=0) if target == compressed else data
    atomic_bytes(target, stored)
    stale.unlink(missing_ok=True)
    _sync_directory(target.parent)


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
        if previous == data:
            if not any(p.exists() for p in json_backup_paths(path)):
                write_json_backup(path, previous)
            return
        # A malformed record must not replace the last readable checkpoint.
        try:
            json.loads(previous)
        except (ValueError, UnicodeError):
            pass
        else:
            write_json_backup(path, previous)
    atomic_bytes(path, data)


def read_json(path, default=None):
    path = Path(path)
    if not path.exists():
        return deepcopy(default)
    try:
        return json.loads(path.read_text())
    except (ValueError, UnicodeError):
        previous, data = read_json_backup(path)
        if previous is None:
            raise
        result = json.loads(data)
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
