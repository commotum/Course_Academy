"""Source-bound math imports: preview guards, retries and deferred answer evidence."""
import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from capture import arguments
from database import Database
from edn import dumps, kw
from math_database import SOURCE, digest, import_directory, validate_receipt


class MathDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.args = arguments(['run', '--math-root', str(self.root/'math')])
        self.db = Database(self.args)
        self.directory = self.root/'capture'/'edb-import-math'
        self.content = {'task_type':'review', 'topic_id':1, 'questions':[]}
        self.prepared = {**self.content, 'authoritative':True}
        self.basis = 100
        self.source = 900
        self.submissions = []
        self.failures = []
        self.db.basis = Mock(side_effect=lambda:self.basis)
        self.db.query = Mock(return_value=[[self.source]])
        self.attrs = [[1,kw('question/problem')], [2,kw('learner/name')],
                      [3,kw('answer/value')], [4,kw('answer-field/choices')]]
        self.db.attributes = Mock(return_value=self.attrs)
        self.db.command = Mock(side_effect=self.command)
        self.prepare = patch('authoritative.prepare_authoritative_content',
            return_value=(self.prepared, {'held_questions':[], 'disagreements':[]})).start()
        self.images = patch('image_library.ImageLibrary').start()
        self.images.return_value.prepare_content.side_effect=lambda c,d:c
        self.planner = patch('math_database.plan', side_effect=self.plan).start()
        self.addCleanup(patch.stopall)

    def plan(self, db, prepared, directory, basis):
        guards = {'retractions':[], 'immutable_answers':[], 'immutable_fields':[],
                  'questions':[], 'structures':{}}
        return ([] if Path(directory).name=='after' else [{kw('question/problem'):'MA problem'}]), guards

    def receipt(self, committed=False):
        return {kw('edb/committed'):committed, kw('edb/db-before-t'):self.basis,
                kw('edb/db-after-t'):self.basis+1,
                kw('edb/tx-data'):[[20,1,'MA problem',self.basis+1,self.source,True]]}

    def command(self, command, *options):
        self.assertEqual(options[options.index('--source')+1], SOURCE)
        if command=='with':
            return dumps(self.receipt())
        self.assertEqual(command, 'transact')
        intent = json.loads((self.directory/'commit-intent.json').read_text())
        frozen = {p:(self.directory/p).read_bytes() for p in (
            'commit-intent.json','transaction.edn','prepared-content.json','reconciliation.edn')}
        self.submissions.append((intent, frozen))
        self.assertEqual(options[options.index('--basis')+1],intent['basis'])
        if self.failures:
            error = self.failures.pop(0)
            if isinstance(error,subprocess.CalledProcessError) and 'postgres/stale-basis' in error.stderr:
                self.basis += 1
            raise error
        return dumps(self.receipt(True))

    def test_source_propagates_to_preview_commit_and_verification(self):
        result = self.db.import_content(self.content,self.directory)
        self.assertTrue(result['reimport_is_noop'])
        self.assertEqual(result['source'],SOURCE)
        self.assertEqual(result['database'],'math')
        intent = self.submissions[0][0]
        self.assertEqual(intent['source'],SOURCE)
        self.assertEqual(intent['source_eid'],self.source)
        self.assertEqual(intent['prepared_content_sha256'],digest(self.prepared))
        self.assertEqual(import_directory(self.directory.parent,self.args),self.directory)

    def test_unknown_outcome_replays_frozen_preparation_without_replanning(self):
        self.failures = [subprocess.TimeoutExpired(['edb'],210)]
        with self.assertRaises(subprocess.TimeoutExpired):
            self.db.import_content(self.content,self.directory)
        self.prepare.reset_mock(); self.images.reset_mock(); self.planner.reset_mock()
        self.db.import_content(self.content,self.directory)
        self.assertEqual(self.submissions[0],self.submissions[1])
        self.prepare.assert_not_called(); self.images.assert_not_called()
        self.assertEqual(len(self.planner.call_args_list),1)  # Verification only.
        self.assertEqual(self.planner.call_args.args[2].name,'after')

    def test_retry_refuses_changed_target_evidence_and_preparation(self):
        self.failures = [subprocess.TimeoutExpired(['edb'],210)]
        with self.assertRaises(subprocess.TimeoutExpired):
            self.db.import_content(self.content,self.directory)
        for field,value in [('database','other'),('endpoint','/tmp/other.sock'),('source',':person/jake')]:
            old = getattr(self.args,field)
            with self.subTest(field=field):
                setattr(self.args,field,value)
                with self.assertRaises(ValueError):
                    self.db.import_content(self.content,self.directory)
                setattr(self.args,field,old)
        with self.assertRaisesRegex(ValueError,'Exact retry'):
            self.db.import_content({**self.content,'changed':True},self.directory)
        path = self.directory/'prepared-content.json'
        path.write_text(json.dumps({**self.prepared,'changed':True}))
        with self.assertRaisesRegex(ValueError,'Prepared content differs'):
            self.db.import_content(self.content,self.directory)
        self.assertEqual(len(self.submissions),1)

    def test_confirmed_stale_basis_replans_with_source_preserved(self):
        self.failures = [subprocess.CalledProcessError(1,['edb'],
            stderr='ERROR category=Conflict code=postgres/stale-basis\n')]
        result = self.db.import_content(self.content,self.directory)
        self.assertTrue(result['committed'])
        self.assertEqual([s[0]['basis'] for s in self.submissions],[100,101])
        self.assertTrue(all(s[0]['source']==SOURCE for s in self.submissions))
        self.assertEqual(len(list((self.directory/'rejected-commits').iterdir())),1)

    def test_held_answer_writes_review_and_stops_before_images_or_database(self):
        from authoritative import AuthoritativeReview
        self.prepare.return_value=(self.prepared,{'held_questions':[{'id':'q-1','reason':'No MA key'}]})
        with self.assertRaises(AuthoritativeReview):
            self.db.import_content(self.content,self.directory)
        self.assertTrue(json.loads((self.directory/'answer-review.json').read_text())['held_questions'])
        self.images.assert_not_called(); self.db.basis.assert_not_called(); self.db.command.assert_not_called()

    def test_preview_is_noncommitting_and_binds_source(self):
        result = self.db.import_content(self.content,self.directory,apply=False)
        self.assertTrue(result['previewed'])
        self.assertEqual(self.submissions,[])
        self.assertFalse((self.directory/'commit-intent.json').exists())

    def test_pending_preview_does_not_replay_commit(self):
        self.failures = [subprocess.TimeoutExpired(['edb'],210)]
        with self.assertRaises(subprocess.TimeoutExpired):
            self.db.import_content(self.content,self.directory)
        result = self.db.import_content(self.content,self.directory,apply=False)
        self.assertTrue(result['pending_commit'])
        self.assertEqual(len(self.submissions),1)

    def test_noop_receipt_is_bound_to_new_database_source_and_content(self):
        self.planner.side_effect=lambda *a:([],self.plan(*a)[1])
        result = self.db.import_content(self.content,self.directory)
        self.assertTrue(result['already_complete'])
        self.assertEqual(result['source'],SOURCE)
        self.assertEqual(result['content_sha256'],digest(self.content))
        self.db.command.assert_not_called()

    def test_six_slot_receipt_rejects_wrong_source_protected_changes_and_unapproved_retractions(self):
        cases = [[20,1,'text',101,899,True], [20,1,'text',101,True],
                 [20,2,'learner',101,900,True], [20,1,'old',101,900,False]]
        for row in cases:
            with self.subTest(row=row), self.assertRaises(ValueError):
                validate_receipt({':edb/tx-data':[row]},self.attrs,900,[])
        validate_receipt({':edb/tx-data':[[20,1,'old',101,900,False]]},self.attrs,900,
                         [[20,kw('question/problem'),'old']])

    def test_receipt_rejects_changes_to_existing_answer_and_field_definitions(self):
        for row in [[30,3,'changed',101,900,True],[40,4,30,101,900,True]]:
            with self.subTest(row=row), self.assertRaises(ValueError):
                validate_receipt({':edb/tx-data':[row]},self.attrs,900,[],[30],[[40,kw('answer-field/choices')]])


if __name__=='__main__':
    unittest.main()
