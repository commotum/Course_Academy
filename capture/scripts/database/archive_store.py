"""Immutable archive bytes, shared without changing existing evidence paths."""
import hashlib
import errno
import json
import os
from pathlib import Path
import tempfile

from ..storage import _sync_directory


def publish(path, data, store):
    """Publish a read-only hardlink to a durable, checksum-addressed object."""
    path, store = Path(path), Path(store)
    digest = hashlib.sha256(data).hexdigest()
    blob = store / digest[:2] / digest
    blob.parent.mkdir(parents=True, exist_ok=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != data:
        raise ValueError('Refusing to replace distinct immutable archive evidence: ' + str(path))
    if not blob.exists():
        fd, temporary = tempfile.mkstemp(prefix='.object-', dir=blob.parent)
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data); stream.flush()
                os.fchmod(stream.fileno(), 0o444)
                os.fsync(stream.fileno())
            try:
                os.link(temporary, blob)
                _sync_directory(blob.parent)
            except FileExistsError:
                pass
        finally:
            os.unlink(temporary)
    if blob.read_bytes() != data:
        raise ValueError('Immutable archive object checksum mismatch: ' + str(blob))
    if path.exists() and path.stat().st_ino == blob.stat().st_ino and path.stat().st_dev == blob.stat().st_dev:
        return blob
    fd, temporary = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    os.close(fd); os.unlink(temporary)
    try:
        try:
            os.link(blob, temporary)
        except OSError as error:
            if error.errno != errno.EXDEV:
                raise
            # Custom capture roots can live on another device. Keep the same
            # readable archive and atomic publication even without link sharing.
            with open(temporary, 'xb') as stream:
                stream.write(data); stream.flush()
                os.fchmod(stream.fileno(), 0o444); os.fsync(stream.fileno())
        os.replace(temporary, path)
        _sync_directory(path.parent)
    finally:
        if os.path.exists(temporary): os.unlink(temporary)
    return blob


def publish_json(path, value, store):
    data = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()
    return publish(path, data, store)
