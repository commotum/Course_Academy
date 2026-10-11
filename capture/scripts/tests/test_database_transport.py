"""Only transaction previews use the deployed native-predicate helper."""
from pathlib import Path
from types import SimpleNamespace
import threading
import unittest
from unittest.mock import Mock, patch

from scripts.database.client import EDBClient


class DatabaseTransportTests(unittest.TestCase):
    def client(self, preview_bin=None):
        config = SimpleNamespace(edb_bin=Path('/edb'), preview_bin=preview_bin,
                                 database='math', postgres_url='', capture_only=False)
        return EDBClient(config, threading.Event())

    def test_only_with_uses_cached_native_preview_builder(self):
        builder = Mock(return_value=Path('/cached-native-preview'))
        completed = SimpleNamespace(returncode=0, stdout='result', stderr='')
        with patch.dict('sys.modules', {'scripts.database.preview': SimpleNamespace(preview_executable=builder)}), \
                patch('scripts.database.client.subprocess.run', return_value=completed) as run:
            client = self.client()
            self.assertEqual(client.command('with', '--file', Path('/transaction.edn'), '--source', ':org/Math-Academy'), 'result')
            self.assertEqual(run.call_args.args[0], ['/cached-native-preview', 'with', '--database', 'math',
                                                   '--file', '/transaction.edn', '--source', ':org/Math-Academy'])
            builder.assert_called_once_with(client.config, client.stop_event)
            for command in ('status', 'query', 'pull', 'transact'):
                client.command(command)
                self.assertEqual(run.call_args.args[0], ['/edb', command, '--database', 'math'])
            self.assertEqual(builder.call_count, 1)

    def test_explicit_override_bypasses_builder_and_missing_helper_does_not_fall_back(self):
        builder = Mock(side_effect=AssertionError('Explicit deployment must bypass build'))
        with patch.dict('sys.modules', {'scripts.database.preview': SimpleNamespace(preview_executable=builder)}), \
                patch('scripts.database.client.subprocess.run', side_effect=FileNotFoundError('missing preview')) as run:
            with self.assertRaises(FileNotFoundError):
                self.client(Path('/explicit-preview')).command('with', '--file', '/transaction.edn')
            self.assertEqual(run.call_args.args[0][0], '/explicit-preview')
            self.assertEqual(run.call_count, 1)
            builder.assert_not_called()

    def test_build_failure_cannot_fall_back_to_old_cli_preview(self):
        builder = Mock(side_effect=RuntimeError('Native helper build failed'))
        with patch.dict('sys.modules', {'scripts.database.preview': SimpleNamespace(preview_executable=builder)}), \
                patch('scripts.database.client.subprocess.run') as run:
            with self.assertRaisesRegex(RuntimeError, 'Native helper build failed'):
                self.client().command('with')
            run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
