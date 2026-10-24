"""Shared repairs preserve unrelated work and undo failed source/binary changes."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from generator_shared_repair import apply_repair


class SharedRepairTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True, capture_output=True)
        self.source = self.root / 'shared.py'
        self.source.write_text('VALUE = 1\n')
        self.unrelated = self.root / 'unrelated.py'
        self.unrelated.write_text('KEEP = 9\n')
        self.binary = self.root / 'generate/runs/current/check-engine'
        self.binary.parent.mkdir(parents=True)
        self.patch = self.root / 'repair.patch'
        self.patch.write_text('diff --git a/shared.py b/shared.py\n--- a/shared.py\n+++ b/shared.py\n'
                              '@@ -1 +1 @@\n-VALUE = 1\n+VALUE = 2\n')

    def tearDown(self):
        self.temp.cleanup()

    def check(self, *, fail=False):
        return [sys.executable, '-c',
            "from pathlib import Path; "
            "assert Path('shared.py').read_text() == 'VALUE = 2\\n'; "
            "p = Path('generate/runs/current/check-engine'); "
            "p.write_bytes(b'new executable'); p.chmod(0o700); "
            + ("raise RuntimeError('independent regression failed')" if fail else "assert p.read_bytes() == b'new executable'")]

    def test_success_keeps_tested_source_and_rebuilt_binary(self):
        self.binary.write_bytes(b'old executable')
        result = apply_repair(self.patch, [self.check()], root=self.root)
        self.assertTrue(result['passed'])
        self.assertEqual(self.source.read_text(), 'VALUE = 2\n')
        self.assertEqual(self.binary.read_bytes(), b'new executable')
        self.assertEqual(self.unrelated.read_text(), 'KEEP = 9\n')

    def test_failed_check_restores_source_and_exact_existing_binary_and_mode(self):
        self.binary.write_bytes(b'original\x00executable')
        self.binary.chmod(0o755)
        with self.assertRaises(subprocess.CalledProcessError):
            apply_repair(self.patch, [self.check(fail=True)], root=self.root)
        self.assertEqual(self.source.read_text(), 'VALUE = 1\n')
        self.assertEqual(self.binary.read_bytes(), b'original\x00executable')
        self.assertEqual(self.binary.stat().st_mode & 0o777, 0o755)
        self.assertEqual(self.unrelated.read_text(), 'KEEP = 9\n')

    def test_failed_check_removes_newly_created_binary(self):
        self.assertFalse(self.binary.exists())
        with self.assertRaises(subprocess.CalledProcessError):
            apply_repair(self.patch, [self.check(fail=True)], root=self.root)
        self.assertFalse(self.binary.exists())
        self.assertEqual(self.source.read_text(), 'VALUE = 1\n')

    def test_conflicting_patch_does_not_overwrite_other_worker_changes(self):
        self.source.write_text('VALUE = 3\n')
        self.binary.write_bytes(b'other worker executable')
        with self.assertRaises(subprocess.CalledProcessError):
            apply_repair(self.patch, [self.check()], root=self.root)
        self.assertEqual(self.source.read_text(), 'VALUE = 3\n')
        self.assertEqual(self.binary.read_bytes(), b'other worker executable')


if __name__ == '__main__':
    unittest.main()
