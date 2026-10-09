"""Reviewed mathematical corrections survive later erroneous source captures."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from edn import kw
from provenance import Reconciler, mathematical_correction_records
import test_replacement


class CorrectionRetentionTests(unittest.TestCase):
    setUp = test_replacement.ReplacementTests.setUp
    tearDown = test_replacement.ReplacementTests.tearDown
    evidence = test_replacement.ReplacementTests.evidence
    plan = test_replacement.ReplacementTests.plan
    def test_original_source_cannot_restore_wrong_problem_solution_or_key(self):
        for attr, value in [('question/problem', self.old[':question/problem']),
                            ('question/worked-solution', self.old[':question/worked-solution'])]:
            self.evidence(attr, value, 'mathematical_correction', local=True)
        self.evidence('answer-field/correct', [kw('answer.type/math'), '120'],
                      'mathematical_correction', 'selection', local=True)
        self.q['problem'] = 'Erroneous original source prompt'
        self.q['worked_solution'] = 'Erroneous original source solution'
        self.q['answer_fields'][0]['correct_value'] = '25'
        self.evidence('question/problem', self.q['problem'])
        self.evidence('question/worked-solution', self.q['worked_solution'])
        self.evidence('answer-field/correct', [kw('answer.type/math'), '25'], 'ma_successful_grade', 'selection')
        self.assertEqual(self.plan(), [])
        self.assertFalse(self.reconciler.needs_review)
        self.assertEqual({d['action'] for d in self.reconciler.decisions}, {'retain'})

    def test_correction_is_bound_to_exact_old_value(self):
        self.evidence('question/problem', 'A different reviewed prompt', 'mathematical_correction', local=True)
        self.q['problem'] = 'New authentic source prompt'
        self.evidence('question/problem', self.q['problem'])
        self.assertTrue(self.plan())


class CorrectionEvidenceTests(unittest.TestCase):
    def test_canonical_example_correction_has_scalar_evidence_without_answer_fields(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name);directory=root/'mathematical-corrections/e-21715';directory.mkdir(parents=True)
            review=directory/'review.json';tx=directory/'transaction.edn'
            review.write_text(json.dumps({'rationale':'Correct circular premise labels.',
                'corrected_content':{'math_academy_id':'e-21715','problem':'Original blank-box prompt',
                    'worked_solution':'L3 follows from L1 and L2; L4 follows from L3.', 'answer_fields':[]}}))
            tx.write_text('[]')
            (directory/'verification.json').write_text(json.dumps({'committed':True,
                'mathematical_check_passed':True,'basis_after':12,
                'review_sha256':hashlib.sha256(review.read_bytes()).hexdigest(),
                'transaction_sha256':hashlib.sha256(tx.read_bytes()).hexdigest()}))
            records=mathematical_correction_records(root,{'e-21715'})
            self.assertEqual([r['attribute'] for r in records],['question/problem','question/worked-solution'])
            self.assertTrue(all(r['field'] is None for r in records))

    def test_requires_committed_verification_and_unchanged_review_and_transaction(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            directory = root/'mathematical-corrections/q-1'
            directory.mkdir(parents=True)
            review = directory/'review.json'
            tx = directory/'transaction.edn'
            proof = directory/'verification.json'
            review.write_text(json.dumps({'rationale':'Substitution verifies the corrected result.',
                'corrected_content':{'math_academy_id':'q-1', 'problem':'Corrected prompt',
                    'worked_solution':'Corrected solution', 'answer_fields':[{'key':'field-1',
                        'correct_value':'1', 'choices':[{'type':'math','value':'1'}]}]}}))
            tx.write_text('[]')
            self.assertEqual(mathematical_correction_records(root, {'q-1'}), [])
            verification = {'committed':True, 'mathematical_check_passed':True, 'basis_after':12,
                'review_sha256':hashlib.sha256(review.read_bytes()).hexdigest(),
                'transaction_sha256':hashlib.sha256(tx.read_bytes()).hexdigest()}
            proof.write_text(json.dumps(verification))
            self.assertEqual(len(mathematical_correction_records(root, {'q-1'})), 3)
            self.assertEqual(mathematical_correction_records(root, {'q-2'}), [])
            tx.write_text('[changed]')
            self.assertEqual(mathematical_correction_records(root, {'q-1'}), [])
            tx.write_text('[]')
            review.write_text(review.read_text()+' ')
            self.assertEqual(mathematical_correction_records(root, {'q-1'}), [])


if __name__ == '__main__':
    unittest.main()
