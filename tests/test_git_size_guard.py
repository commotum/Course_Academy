import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from check_staged_file_sizes import oversized


class GitSizeGuardTests(unittest.TestCase):
    def test_checks_staged_blob_not_newer_worktree_and_allows_deletion(self):
        with tempfile.TemporaryDirectory()as directory:
            root=Path(directory)
            def git(*args):return subprocess.run(['git',*args],cwd=root,check=True,capture_output=True)
            git('init','-q');path=root/'audit.json';path.write_bytes(b'x'*8192);git('add','audit.json')
            path.write_bytes(b'small')
            self.assertEqual(oversized(root,4096),[('audit.json',8192)])
            git('add','audit.json');self.assertEqual(oversized(root,4096),[])
            git('-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','baseline')
            path.unlink();git('add','-u');self.assertEqual(oversized(root,4096),[])
