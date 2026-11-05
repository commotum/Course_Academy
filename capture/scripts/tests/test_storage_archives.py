import gzip
import errno
import os
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.storage import atomic_json, read_json, read_json_backup, write_json_backup
from scripts.database.archive_store import publish


class StorageArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_unchanged_write_keeps_prior_recovery_value_and_current_inode(self):
        path = self.root/'checkpoint.json'
        atomic_json(path, {'version': 1})
        atomic_json(path, {'version': 2})
        current = path.stat()
        prior = path.with_name(path.name+'.previous').read_bytes()
        atomic_json(path, {'version': 2})
        self.assertEqual(path.stat().st_ino, current.st_ino)
        self.assertEqual(path.stat().st_mtime_ns, current.st_mtime_ns)
        self.assertEqual(path.with_name(path.name+'.previous').read_bytes(), prior)
        path.write_text('{')
        self.assertEqual(read_json(path), {'version': 1})

    def test_unchanged_initial_value_still_gets_standalone_recovery_copy(self):
        path = self.root/'checkpoint.json'
        atomic_json(path, {'version': 1})
        atomic_json(path, {'version': 1})
        path.write_text('{')
        self.assertEqual(read_json(path), {'version': 1})

    def test_compressed_backup_preserves_exact_bytes_and_recovers_corrupt_current(self):
        path = self.root/'content.json'
        first = {'source': 'unchanged original evidence '*1000}
        with patch('scripts.storage.BACKUP_COMPRESSION_BYTES', 100):
            atomic_json(path, first)
            original = path.read_bytes()
            atomic_json(path, {'revision': 2})
        saved = path.with_name(path.name+'.previous.gz')
        self.assertEqual(gzip.decompress(saved.read_bytes()), original)
        self.assertFalse(path.with_name(path.name+'.previous').exists())
        path.write_text('{')
        self.assertEqual(read_json(path), first)
        atomic_json(path, {'recovered': True})
        self.assertEqual(gzip.decompress(saved.read_bytes()), original)

    def test_switching_backup_formats_keeps_only_new_recovery_value(self):
        path = self.root/'content.json'
        with patch('scripts.storage.BACKUP_COMPRESSION_BYTES', 100):
            atomic_json(path, {'large':'x'*1000})
            atomic_json(path, {'small':1})
            atomic_json(path, {'small':2})
        self.assertFalse(path.with_name(path.name+'.previous.gz').exists())
        self.assertEqual(json.loads(path.with_name(path.name+'.previous').read_bytes()), {'small':1})

    def test_bad_newer_backup_falls_back_to_other_readable_format(self):
        path = self.root/'checkpoint.json'
        atomic_json(path, {'v':1}); atomic_json(path, {'v':2})
        path.with_name(path.name+'.previous.gz').write_bytes(b'broken gzip')
        path.write_text('{')
        self.assertEqual(read_json(path), {'v':1})

    def test_immutable_archives_share_storage_and_atomic_replacement_detaches(self):
        first, second = self.root/'a/request.json', self.root/'b/request.json'
        store = self.root/'objects'
        data = b'{"source":"original evidence"}\n'
        blob = publish(first, data, store)
        publish(second, data, store)
        self.assertEqual(first.stat().st_ino, second.stat().st_ino)
        self.assertEqual(first.stat().st_ino, blob.stat().st_ino)
        self.assertEqual(blob.stat().st_mode & 0o222, 0)
        atomic_json(first, {'source':'new independent record'})
        self.assertEqual(second.read_bytes(), data)
        self.assertEqual(blob.read_bytes(), data)
        self.assertNotEqual(first.stat().st_ino, second.stat().st_ino)

    def test_distinct_evidence_or_corrupt_object_is_never_overwritten(self):
        path, store = self.root/'request.json', self.root/'objects'
        blob = publish(path, b'original', store)
        with self.assertRaisesRegex(ValueError, 'distinct'):
            publish(path, b'replacement', store)
        blob.chmod(0o644); blob.write_bytes(b'corrupt')
        with self.assertRaisesRegex(ValueError, 'checksum'):
            publish(self.root/'other.json', b'original', store)
        self.assertFalse((self.root/'other.json').exists())

    def test_cross_device_archive_root_keeps_a_readable_independent_copy(self):
        path, store = self.root/'archive/request.json', self.root/'objects'
        link = os.link
        def cross_device(source, target):
            if Path(target).parent == path.parent:
                raise OSError(errno.EXDEV, 'different device')
            return link(source, target)
        with patch('scripts.database.archive_store.os.link',side_effect=cross_device):
            blob = publish(path,b'exact request',store)
        self.assertEqual(path.read_bytes(),b'exact request')
        self.assertNotEqual(path.stat().st_ino,blob.stat().st_ino)
