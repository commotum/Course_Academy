"""Preview builds must follow the current validator and fail closed on ambiguity."""
import json
import os
from pathlib import Path
import tempfile
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from scripts.database import preview
from scripts.runtime import StopRequested


class NativePreviewBuildTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.config = SimpleNamespace(repo_root=self.root, math_root=self.root / 'math', preview_bin=None)
        self.stop = threading.Event()
        self.library = self.root / 'edb/target/release/deps/libedb_core-current.rlib'
        self.library.parent.mkdir(parents=True)
        self.library.write_bytes(b'library-v1')
        self.manifest = self.config.math_root / 'bin/source/current/build.json'
        self.manifest.parent.mkdir(parents=True)
        self.manifest.write_text(json.dumps({'edb_library': str(self.library),
            'executable': str(self.config.math_root / 'bin/course-academy-transactor')}))
        for name in preview.SOURCE_FILES:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(name)
        self.addCleanup(patch.stopall)
        patch.object(preview, 'ROOT', self.root).start()
        patch.dict(os.environ, {}, clear=True).start()
        self.commands = []
        def compile_helper(command, stop_event):
            self.commands.append(command)
            output = Path(command[command.index('-o') + 1])
            output.write_bytes(b'compiled executable')
            output.chmod(0o700)
        self.compiler = patch.object(preview, '_compile', side_effect=compile_helper).start()

    def test_cache_reused_but_predicate_and_library_changes_force_new_builds(self):
        first = preview.preview_executable(self.config, self.stop)
        self.assertEqual(preview.preview_executable(self.config, self.stop), first)
        self.assertEqual(len(self.commands), 1)
        (self.root / 'engine/edb/answer_fields.rs').write_text('updated validator')
        second = preview.preview_executable(self.config, self.stop)
        self.library.write_bytes(b'library-v2')
        third = preview.preview_executable(self.config, self.stop)
        self.assertEqual(len({first, second, third}), 3)
        self.assertEqual(len(self.commands), 3)
        manifest = json.loads(third.with_suffix('.json').read_text())
        self.assertEqual(manifest['edb_library'], str(self.library))
        self.assertIn('edb_core=' + str(self.library), self.commands[-1])
        self.assertTrue(all(path.is_file() for path in (first, second, third)))

    def test_ambiguous_manifest_requires_explicit_library_without_choosing_newest(self):
        other = self.manifest.parent.with_name('another') / 'build.json'
        other.parent.mkdir()
        other.write_text(self.manifest.read_text())
        with self.assertRaisesRegex(ValueError, 'one deployed writer'):
            preview.preview_executable(self.config, self.stop)
        self.assertEqual(self.commands, [])
        os.environ['EDB_CORE_RLIB'] = str(self.library)
        self.assertTrue(preview.preview_executable(self.config, self.stop).is_file())

    def test_missing_library_and_wrong_writer_manifest_fail_closed(self):
        self.library.unlink()
        with self.assertRaisesRegex(ValueError, 'existing edb_core'):
            preview.preview_executable(self.config, self.stop)
        self.manifest.write_text(json.dumps({'edb_library': str(self.library), 'executable': '/different/writer'}))
        with self.assertRaisesRegex(ValueError, 'configured math writer'):
            preview.preview_executable(self.config, self.stop)
        self.assertEqual(self.commands, [])

    def test_override_bypasses_build_and_manual_stop_prevents_any_build(self):
        self.config.preview_bin = self.root / 'explicit-preview'
        self.assertEqual(preview.preview_executable(self.config, self.stop), self.config.preview_bin)
        self.assertEqual(self.commands, [])
        self.stop.set()
        with self.assertRaises(StopRequested):
            preview.preview_executable(self.config, self.stop)

    def test_inputs_changing_during_compile_cannot_publish_stale_fingerprint(self):
        def changed(command, stop_event):
            Path(command[-1]).write_bytes(b'compiled')
            self.library.write_bytes(b'replaced concurrently')
        self.compiler.side_effect = changed
        with self.assertRaisesRegex(RuntimeError, 'inputs changed'):
            preview.preview_executable(self.config, self.stop)
        directory = self.root / '.local/edb/capture-runtime'
        self.assertEqual(list(directory.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
