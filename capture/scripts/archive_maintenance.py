"""Lossless maintenance for reviewed, retired capture evidence."""
import collections
import gzip
import hashlib
import json
from pathlib import Path

from .database.archive_store import publish
from .storage import BACKUP_COMPRESSION_BYTES, atomic_bytes, read_json, _sync_directory

ARCHIVE_NAMES = {'request.json', 'receipt.edn', 'preview.edn', 'transaction.edn'}
RETIRED = {'verified', 'confirmed_needs_reconciliation', 'rejected_stale_basis'}


def archive_candidate(path, repo):
    path, repo = Path(path), Path(repo)
    if path.is_symlink() or not path.is_file() or path.name not in ARCHIVE_NAMES:
        return False
    if path.parent.parent.name != 'requests' or not path.parent.name.startswith('capture-'):
        return False
    roots = [repo/'reference/mathacademy/capture', repo/'reference/mathacademy/capture-database/batches']
    if not any(path.resolve().is_relative_to(root.resolve()) for root in roots):
        return False
    result = read_json(path.parent/'result.json', {})
    if result.get('status') not in RETIRED:
        return False
    pending = read_json(path.parent.parent.parent/'request.json', {})
    return not pending or pending.get('request_key') != path.parent.name


def share_archived_group(paths, expected_sha256, repo, *, apply=False):
    paths = [Path(p) for p in paths if archive_candidate(p, repo)]
    if len(paths) < 2:
        return None
    data = paths[0].read_bytes()
    if hashlib.sha256(data).hexdigest() != expected_sha256:
        return {'status':'preserved_changed_group', 'sha256':expected_sha256}
    inodes, links = {}, collections.Counter()
    for path in paths:
        info = path.stat(); key = (info.st_dev,info.st_ino)
        if path.read_bytes() != data:
            return {'status':'preserved_changed_group', 'sha256':expected_sha256}
        inodes[key] = info; links[key] += 1
    row = {'status':'candidate', 'sha256':expected_sha256, 'paths':list(map(str,paths)),
           'bytes_per_copy':len(data), 'allocated_bytes_saved':0}
    if apply:
        store = Path(repo)/'reference/mathacademy/capture-database/objects'
        blob = store/expected_sha256[:2]/expected_sha256
        existed = blob.exists()
        for path in paths:
            publish(path, data, store)
        current = blob.stat(); current_key = (current.st_dev,current.st_ino)
        freed = sum(info.st_blocks*512 for key,info in inodes.items()
                    if key != current_key and info.st_nlink == links[key])
        row.update(status='shared', allocated_bytes_saved=freed-(0 if existed else current.st_blocks*512))
    return row


def compress_identical_backup(path, expected_sha256, repo, *, apply=False):
    path, repo = Path(path), Path(repo)
    root = repo/'reference/mathacademy/capture'
    if path.is_symlink() or not path.is_file() or not path.name.endswith('.previous'):
        return None
    if not path.resolve().is_relative_to(root.resolve()):
        return None
    info = path.stat()
    if info.st_size < BACKUP_COMPRESSION_BYTES or info.st_nlink > 1:
        return None
    current = path.with_name(path.name[:-9])
    if current.is_symlink() or not current.is_file():
        return None
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected_sha256 or current.read_bytes() != data:
        return {'status':'preserved_changed_backup', 'path':str(path)}
    json.loads(data)
    target = path.with_name(path.name+'.gz')
    if target.exists() and gzip.decompress(target.read_bytes()) != data:
        return {'status':'preserved_distinct_compressed_backup','path':str(path)}
    row = {'status':'backup_candidate','path':str(path),'sha256':expected_sha256,
           'uncompressed_bytes':len(data),'allocated_bytes_saved':0}
    if apply:
        existed = target.exists()
        if not existed:
            atomic_bytes(target,gzip.compress(data,compresslevel=3,mtime=0))
        if gzip.decompress(target.read_bytes()) != data:
            raise ValueError('Compressed backup failed byte verification: '+str(target))
        now = path.stat()
        if (now.st_ino,now.st_mtime_ns,now.st_ctime_ns) != (info.st_ino,info.st_mtime_ns,info.st_ctime_ns):
            raise ValueError('Backup changed during maintenance: '+str(path))
        path.unlink(); _sync_directory(path.parent)
        row.update(status='backup_compressed', compressed_path=str(target),
                   compressed_bytes=target.stat().st_size,
                   allocated_bytes_saved=info.st_blocks*512-(0 if existed else target.stat().st_blocks*512))
    return row
