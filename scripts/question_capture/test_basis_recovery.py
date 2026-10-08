"""Offline optimistic-commit contention and exact-request recovery."""
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import database
from capture import arguments
from core import atomic_json
from edn import dumps, kw
from import_repair import import_with_repair


class BasisRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.args = arguments(['run', '--state-dir', str(self.root/'state'),
                               '--output', str(self.root/'captures')])
        self.content = {'task_id':1, 'topic_id':1, 'questions':[{'math_academy_id':'q-1'}]}
        self.directory = self.root/'capture'/'edb-import'
        self.db = database.Database(self.args)
        self.current_basis = 100
        self.submissions = []
        self.failures = []
        self.db.basis = Mock(side_effect=lambda:self.current_basis)
        self.db.content_topics = Mock(return_value={})
        self.db.questions = Mock(return_value={})
        self.db.reconciliation = Mock(return_value=SimpleNamespace(
            decisions=[], needs_review=False, authored=[], sources=[], usage={}, no_history=set()))
        self.db.replacement_guards = Mock(return_value=[])
        self.db.attributes = Mock(return_value=[])
        self.db.validate_datoms = Mock()
        self.db._verify = Mock(return_value={'committed':True})
        self.db.command = Mock(side_effect=self.command)
        self.build = patch('database.build_content_transaction', return_value=(
            [{kw('question/problem'):'Captured problem'}], [])).start()
        self.addCleanup(patch.stopall)

    def command(self, command, *options):
        if command == 'with':
            return dumps({kw('edb/db-before-t'):self.current_basis})
        self.assertEqual(command, 'transact')
        intent = json.loads((self.directory/'commit-intent.json').read_text())
        files = {name:(self.directory/name).read_bytes() for name in
                 ('commit-intent.json', 'transaction.edn', 'reconciliation.edn')}
        self.submissions.append((intent, files))
        if self.failures:
            error = self.failures.pop(0)
            if isinstance(error, subprocess.CalledProcessError) and error.stderr == self.stale_error().stderr:
                self.current_basis += 1  # Another client's successful transaction.
            raise error
        self.assertEqual(options[options.index('--basis')+1], intent['basis'])
        self.assertEqual(intent['basis'], self.current_basis)
        return dumps({kw('edb/committed'):True, kw('edb/db-before-t'):intent['basis'],
                      kw('edb/db-after-t'):intent['basis']+1})

    @staticmethod
    def stale_error():
        return subprocess.CalledProcessError(1, ['edb', 'transact'],
            stderr='ERROR category=Conflict code=postgres/stale-basis\n')

    def frozen_intent(self):
        self.directory.mkdir(parents=True)
        (self.directory/'transaction.edn').write_text('[]\n')
        (self.directory/'reconciliation.edn').write_text('{}\n')
        intent = {'database':self.args.database, 'endpoint':self.args.endpoint, 'basis':100,
                  'request_key':'original-request',
                  'content_sha256':hashlib.sha256(json.dumps(self.content, sort_keys=True).encode()).hexdigest(),
                  'sha256':hashlib.sha256((self.directory/'transaction.edn').read_bytes()).hexdigest(),
                  'reconciliation_sha256':hashlib.sha256((self.directory/'reconciliation.edn').read_bytes()).hexdigest()}
        atomic_json(self.directory/'commit-intent.json', intent)
        return intent

    def test_other_client_commit_replans_and_preserves_rejected_plan(self):
        self.failures = [self.stale_error()]
        self.assertEqual(self.db.import_content(self.content, self.directory), {'committed':True})
        first, second = [s[0] for s in self.submissions]
        self.assertEqual([first['basis'], second['basis']], [100, 101])
        self.assertEqual(first['sha256'], second['sha256'])
        self.assertNotEqual(first['request_key'], second['request_key'])
        archives = list((self.directory/'rejected-commits').iterdir())
        self.assertEqual(len(archives), 1)
        for name, data in self.submissions[0][1].items():
            self.assertEqual((archives[0]/name).read_bytes(), data)
        self.db._verify.assert_called_once()
        self.assertEqual(self.db.content_topics.call_args.args[-1], 101)

    def test_saved_intent_gets_exact_replay_before_stale_replan(self):
        original = self.frozen_intent()
        self.failures = [self.stale_error()]
        self.db.import_content(self.content, self.directory)
        self.assertEqual(self.submissions[0][0], original)
        self.assertEqual(self.submissions[1][0]['basis'], 101)
        self.db.basis.assert_called_once()

    def test_remote_stale_rejection_replans_after_exact_replay(self):
        original = self.frozen_intent()
        self.failures = [subprocess.CalledProcessError(1, ['edb', 'transact'],
            stderr='ERROR category=Conflict code=transport/remote-error\n')]
        def reject(command, **kwargs):
            self.current_basis = 101
            self.assertEqual(command[command.index('--request-key')+1], original['request_key'])
            raise subprocess.CalledProcessError(1, command,
                stderr='ERROR category=Conflict code=transport/remote-error\nremote_code=postgres/stale-basis\n')
        with patch('edb_transport.replay', side_effect=reject):
            self.assertEqual(self.db.import_content(self.content, self.directory), {'committed':True})
        self.assertEqual([s[0]['basis'] for s in self.submissions], [100, 101])

    def test_unknown_remote_conflict_retains_original_intent(self):
        self.frozen_intent()
        before = (self.directory/'commit-intent.json').read_bytes()
        error = subprocess.CalledProcessError(1, ['edb', 'transact'],
            stderr='ERROR category=Conflict code=transport/remote-error\n')
        self.failures = [error]
        with patch('edb_transport.replay', side_effect=error):
            with self.assertRaises(subprocess.CalledProcessError):
                self.db.import_content(self.content, self.directory)
        self.assertEqual((self.directory/'commit-intent.json').read_bytes(), before)
        self.assertFalse((self.directory/'rejected-commits').exists())

    def test_unknown_outcome_retries_same_intent_without_replanning(self):
        self.frozen_intent()
        self.failures = [subprocess.TimeoutExpired(['edb', 'transact'], 210)]
        with self.assertRaises(subprocess.TimeoutExpired):
            self.db.import_content(self.content, self.directory)
        self.assertFalse((self.directory/'rejected-commits').exists())
        self.db.import_content(self.content, self.directory)
        self.assertEqual(self.submissions[0], self.submissions[1])
        self.db.basis.assert_not_called()

    def test_unrelated_or_quoted_errors_do_not_retire_intent(self):
        for stderr in ('ERROR category=Conflict code=transaction/cas-failed\n',
                       'ERROR category=Fault code=postgres/stale-basis\n',
                       'log: ERROR category=Conflict code=postgres/stale-basis\n'):
            with self.subTest(stderr=stderr):
                if not (self.directory/'commit-intent.json').exists():
                    self.frozen_intent()
                before = (self.directory/'commit-intent.json').read_bytes()
                self.failures = [subprocess.CalledProcessError(1, ['edb', 'transact'], stderr=stderr)]
                with self.assertRaises(subprocess.CalledProcessError):
                    self.db.import_content(self.content, self.directory)
                self.assertEqual((self.directory/'commit-intent.json').read_bytes(), before)
                self.assertFalse((self.directory/'rejected-commits').exists())
        self.db.basis.assert_not_called()

    def test_contention_is_bounded_and_skips_model_repair(self):
        self.failures = [self.stale_error() for _ in range(3)]
        with patch('import_repair.repair') as repair:
            with self.assertRaises(database.StaleBasis):
                import_with_repair(self.db, self.content, self.directory.parent,
                                   {'activity_complete':True, 'history_complete':True}, self.args)
        repair.assert_not_called()
        self.assertEqual(len(self.submissions), 3)
        self.assertFalse((self.directory/'commit-intent.json').exists())
        self.assertEqual(len(list((self.directory/'rejected-commits').iterdir())), 3)
        self.assertEqual(self.db.import_content(self.content, self.directory), {'committed':True})

    def test_preview_contention_is_also_bounded_without_model_repair(self):
        self.db.command.side_effect=lambda *args:dumps({kw('edb/db-before-t'):101})
        with patch('import_repair.repair') as repair:
            with self.assertRaises(database.StaleBasis):
                import_with_repair(self.db, self.content, self.directory.parent,
                                   {'activity_complete':True, 'history_complete':True}, self.args)
        repair.assert_not_called()
        self.assertEqual(self.db.command.call_count, 3)
        self.assertTrue(all(call.args[0] == 'with' for call in self.db.command.call_args_list))
        self.assertFalse((self.directory/'commit-intent.json').exists())


if __name__ == '__main__':
    unittest.main()
