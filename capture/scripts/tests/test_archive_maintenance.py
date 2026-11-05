import gzip
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.archive_maintenance import compress_identical_backup, share_archived_group
from scripts.storage import atomic_json, read_json


class ArchiveMaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def archive(self, task, data, status='verified'):
        directory=self.root/'reference/mathacademy/capture/foundations'/str(task)/'database/requests/capture-key'
        directory.mkdir(parents=True)
        path=directory/'request.json';path.write_bytes(data)
        atomic_json(directory/'result.json',{'status':status})
        return path

    def test_dry_run_retains_bytes_and_apply_preserves_paths_with_shared_inode(self):
        data=b'{"request_key":"capture-key"}\n';sha=hashlib.sha256(data).hexdigest()
        a,b=self.archive(1,data),self.archive(2,data)
        before=a.stat().st_ino
        self.assertEqual(share_archived_group([a,b],sha,self.root)['status'],'candidate')
        self.assertEqual(a.stat().st_ino,before)
        row=share_archived_group([a,b],sha,self.root,apply=True)
        self.assertEqual(row['status'],'shared');self.assertGreater(row['allocated_bytes_saved'],0)
        self.assertEqual(a.stat().st_ino,b.stat().st_ino)
        self.assertEqual(a.read_bytes(),data)

    def test_pending_or_changed_request_is_preserved(self):
        data=b'{}\n';sha=hashlib.sha256(data).hexdigest()
        a,b=self.archive(1,data),self.archive(2,data)
        atomic_json(a.parent.parent.parent/'request.json',{'request_key':'capture-key'})
        self.assertIsNone(share_archived_group([a,b],sha,self.root,apply=True))
        (a.parent.parent.parent/'request.json').unlink()
        b.write_bytes(b'changed')
        self.assertEqual(share_archived_group([a,b],sha,self.root,apply=True)['status'],'preserved_changed_group')
        self.assertEqual(b.read_bytes(),b'changed')

    def test_backup_compression_preserves_recovery_and_distinct_values(self):
        path=self.root/'reference/mathacademy/capture/foundations/1/content.json'
        original={'evidence':'original source '*100000}
        atomic_json(path,original);data=path.read_bytes();atomic_json(path,original)
        backup=path.with_name(path.name+'.previous')
        # Create the legacy plain form that the migration accepts.
        compressed=path.with_name(path.name+'.previous.gz')
        backup.write_bytes(gzip.decompress(compressed.read_bytes()));compressed.unlink()
        sha=hashlib.sha256(data).hexdigest()
        row=compress_identical_backup(backup,sha,self.root,apply=True)
        self.assertEqual(row['status'],'backup_compressed')
        self.assertFalse(backup.exists());self.assertEqual(gzip.decompress(compressed.read_bytes()),data)
        path.write_text('{');self.assertEqual(read_json(path),original)
        atomic_json(path,{'different':True});backup.write_bytes(data)
        self.assertEqual(compress_identical_backup(backup,sha,self.root,apply=True)['status'],'preserved_changed_backup')
        self.assertTrue(backup.exists())
