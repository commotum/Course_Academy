"""An EDB development rebuild must not change the capture reader."""
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from capture import arguments
from database import Database


class PinnedReaderTests(unittest.TestCase):
    def test_development_rebuild_leaves_default_reader_operational(self):
        with tempfile.TemporaryDirectory() as work:
            source = Path(work) / 'development-edb'
            pinned = Path(work) / 'capture-edb'
            source.write_text('#!/bin/sh\nprintf "STATUS basis_t=2892\\n"\n')
            source.chmod(0o755)
            shutil.copyfile(source, pinned)
            pinned.chmod(0o755)
            with patch.dict(os.environ, {}, clear=True), patch('capture.CAPTURE_EDB_BIN', pinned):
                args = arguments(['priorities'])
            db = Database(args)
            self.assertEqual(db.basis(), 2892)
            # Simulate cargo overwriting the development executable in place.
            source.write_text('#!/bin/sh\nprintf "incompatible reader\\n" >&2\nexit 1\n')
            self.assertEqual(db.basis(), 2892)
            self.assertNotEqual(source.stat().st_ino, pinned.stat().st_ino)

    def test_explicit_reader_overrides_remain_available(self):
        with patch.dict(os.environ, {'EDB_BIN': '/explicit/environment-edb'}):
            self.assertEqual(arguments(['priorities']).edb_bin, '/explicit/environment-edb')
            self.assertEqual(arguments(['priorities', '--edb-bin', '/explicit/cli-edb']).edb_bin,
                             '/explicit/cli-edb')


if __name__ == '__main__':
    unittest.main()
