"""Only transaction previews use the deployed native-predicate helper."""
from pathlib import Path
from types import SimpleNamespace
import threading
import unittest
from unittest.mock import Mock, patch

from scripts.database.client import EDBClient
from scripts.database.client import EDBCommandError, StaleBasis
import subprocess


class DatabaseTransportTests(unittest.TestCase):
    def test_source_dependencies_include_missing_topics_and_new_kp_titles(self):
        client = self.client()
        rows = [[{':topic/math-academy-id': 1, ':topic/knowledge-points': [
            {':knowledge-point/title': 'Known skill'}]}],
            [{':topic/math-academy-id': 2, ':topic/knowledge-points': []}]]
        questions = [{'topic_id': '1', 'knowledge_point': 'Known skill'},
                     {'topic_id': '2', 'knowledge_point': 'New skill'},
                     {'topic_id': '3', 'knowledge_point': 'Missing topic skill'}]
        with patch.object(client, 'basis', return_value=42), patch.object(client, 'query', return_value=rows) as query:
            self.assertEqual(client.source_dependencies(questions, Path('/tmp/read')), ['2', '3'])
            self.assertEqual(query.call_args.args[-1], 42)
            self.assertEqual(query.call_args.args[1], [[1, 2, 3]])

    def client(self, preview_bin=None):
        config = SimpleNamespace(edb_bin=Path('/edb'), preview_bin=preview_bin,
                                 database='math', postgres_url='', capture_only=False)
        return EDBClient(config, threading.Event())

    def test_preview_and_submission_use_their_native_helpers(self):
        builder = Mock(return_value=Path('/cached-native-preview'))
        submitter = Mock(return_value=Path('/cached-native-submit'))
        completed = SimpleNamespace(returncode=0, stdout='result', stderr='')
        with patch.dict('sys.modules', {'scripts.database.preview': SimpleNamespace(preview_executable=builder,
                                                                                  submission_executable=submitter)}), \
                patch('scripts.database.client.subprocess.run', return_value=completed) as run:
            client = self.client()
            self.assertEqual(client.command('with', '--file', Path('/transaction.edn'), '--source', ':org/Math-Academy'), 'result')
            self.assertEqual(run.call_args.args[0], ['/cached-native-preview', 'with', '--database', 'math',
                                                   '--file', '/transaction.edn', '--source', ':org/Math-Academy'])
            builder.assert_called_once_with(client.config, client.stop_event)
            for command in ('status', 'query', 'pull'):
                client.command(command)
                self.assertEqual(run.call_args.args[0], ['/edb', command, '--database', 'math'])
            self.assertEqual(builder.call_count, 1)
            client.command('transact', '--request-key', 'original-key', '--basis', '42')
            self.assertEqual(run.call_args.args[0], ['/cached-native-submit', 'transact', '--database', 'math',
                                                   '--request-key', 'original-key', '--basis', '42'])
            submitter.assert_called_once_with(client.config, client.stop_event)

    def test_structured_remote_stale_rejection_is_the_only_reprepare_signal(self):
        for stderr, expected in [
            ('ERROR category=Conflict code=transport/remote-error\nremote_code=postgres/stale-basis\n', StaleBasis),
            ('ERROR category=Unavailable code=transport/remote-error\nremote_code=service/unavailable\n', EDBCommandError),
            ('ERROR category=UnknownOutcome code=transport/invalid-outcome\n', EDBCommandError),
            ('ERROR category=Conflict code=transport/remote-error\n', EDBCommandError),
        ]:
            with self.subTest(stderr=stderr), patch('scripts.database.client.subprocess.run',
                    return_value=SimpleNamespace(returncode=1, stdout='retained-output', stderr=stderr)):
                with self.assertRaises(expected) as raised:
                    self.client().command('query')
                if expected is EDBCommandError:
                    self.assertEqual(raised.exception.stdout, 'retained-output')
                    self.assertEqual(raised.exception.stderr, stderr)
                    self.assertNotIn('/edb', str(raised.exception))

    def test_error_display_uses_remote_code_without_dumping_argv(self):
        e = EDBCommandError(1, ['/long/private/path/edb', 'transact', '--file', '/capture/question.edn'], '',
                            'ERROR category=Unavailable code=transport/remote-error\nremote_code=service/unavailable\n')
        self.assertIn('service/unavailable', str(e))
        self.assertNotIn('/capture/', str(e))
        self.assertIsInstance(e, subprocess.CalledProcessError)

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
