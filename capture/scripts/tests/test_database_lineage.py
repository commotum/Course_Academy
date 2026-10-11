"""A same-name rebuild must never receive an earlier lineage's numeric IDs."""
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.commit import Committer
from scripts.database.edn import dumps, kw
from scripts.database.prepare import Preparation
from scripts.storage import atomic_json
from scripts.tests.test_database import FakeClient, question


OLD = '01a1233a-f21a-7b66-a19a-29c200135e3c'
NEW = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'


class StatusIdentityTests(unittest.TestCase):
    def test_status_parses_real_cli_format_and_basis_api_remains_an_integer(self):
        client = EDBClient(Config(), threading.Event())
        with patch.object(client, 'command', return_value=f'STATUS database="math" lineage={NEW} basis_t=249 generation=0\n') as command:
            self.assertEqual(client.status(), {'database': 'math', 'lineage': NEW, 'basis': 249})
            self.assertEqual(client.basis(), 249)
            command.assert_called_with('status', timeout=30)

    def test_missing_ambiguous_or_invalid_identity_fails_closed(self):
        client = EDBClient(Config(), threading.Event())
        invalid = [f'STATUS database="math" basis_t=249',
                   f'STATUS database="other" lineage={NEW} basis_t=249',
                   f'STATUS database="math" lineage={NEW} basis_t=-1',
                   f'STATUS database="math" lineage={NEW} lineage={OLD} basis_t=249',
                   'STATUS database="math" lineage=unknown basis_t=249',
                   f'STATUS database="math" lineage={NEW} basis_t=249\n' * 2]
        for output in invalid:
            with self.subTest(output=output), patch.object(client, 'command', return_value=output):
                with self.assertRaises(ValueError):
                    client.status()


class DurableLineageTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.config = Config(repo_root=self.root, math_root=self.root / 'math')
        self.client = FakeClient()
        self.client.lineage = OLD
        self.committer = Committer(self.config, self.client, self.root / 'database')
        self.snapshot = self.client.snapshot({}, self.root, self.client.basis())
        self.batch = Preparation(self.snapshot).prepare({'questions': [question()]})['batches'][0]
        self.committer.preview(self.batch, self.snapshot)

    def request(self):
        return self.committer.save_request(self.batch, self.snapshot, 'source-content-hash')

    def test_rebuilt_same_name_same_basis_rejected_before_transact_and_files_unchanged(self):
        request = self.request()
        self.assertEqual(request['database_lineage'], OLD)
        self.client.lineage = NEW
        self.assertEqual(self.client.basis(), request['basis'])
        paths = [self.committer.intent_path, self.committer.directory / 'transaction.edn']
        original = {path: path.read_bytes() for path in paths}
        with self.assertRaisesRegex(ValueError, 'another database lineage'):
            self.committer.submit(request)
        self.assertEqual(original, {path: path.read_bytes() for path in paths})
        self.assertFalse(any(command == 'transact' for command, options in self.client.calls))

    def test_changed_lineage_cannot_reuse_an_old_cached_receipt(self):
        request = self.request()
        atomic_json(self.committer.directory / 'receipt-request.json', {
            'request_key': request['request_key'], 'transaction_sha256': request['transaction_sha256'],
            'receipt_edn': dumps({kw('edb/committed'): True})})
        self.client.lineage = NEW
        with self.assertRaisesRegex(ValueError, 'another database lineage'):
            self.committer.submit(request)
        self.assertTrue(self.committer.intent_path.exists())
        self.assertFalse(any(command == 'transact' for command, options in self.client.calls))

    def test_legacy_request_without_lineage_is_retained_and_not_submitted(self):
        request = self.request()
        request.pop('database_lineage')
        atomic_json(self.committer.intent_path, request)
        original = self.committer.intent_path.read_bytes()
        with self.assertRaisesRegex(ValueError, 'no database lineage'):
            self.committer.submit(request)
        self.assertEqual(self.committer.intent_path.read_bytes(), original)
        self.assertFalse(any(command == 'transact' for command, options in self.client.calls))

    def test_exact_same_lineage_replay_uses_saved_receipt_after_basis_advances(self):
        request = self.request()
        original = self.committer.intent_path.read_bytes()
        receipt = self.committer.submit(request)
        self.assertGreater(self.client.basis(), request['basis'])
        self.assertEqual(self.committer.submit(request), receipt)
        self.assertEqual(self.committer.intent_path.read_bytes(), original)
        self.assertEqual(len([command for command, options in self.client.calls if command == 'transact']), 1)

    def test_changed_or_unknown_snapshot_lineage_cannot_be_bound_to_new_database(self):
        self.client.lineage = NEW
        for snapshot in (self.snapshot, {key: value for key, value in self.snapshot.items() if key != 'lineage'}):
            with self.subTest(lineage=snapshot.get('lineage')):
                with self.assertRaisesRegex(ValueError, 'snapshot belongs to another or unknown database lineage'):
                    self.committer.save_request(self.batch, snapshot, 'source-content-hash')
        self.assertFalse(self.committer.intent_path.exists())


if __name__ == '__main__':
    unittest.main()
