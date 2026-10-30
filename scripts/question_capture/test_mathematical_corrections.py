"""Reviewed mathematical corrections survive later erroneous source captures."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from edn import kw
from provenance import Reconciler, mathematical_correction_records, field_value
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

    def test_attested_bank_prevents_scalar_to_set_distractor_regression(self):
        values = [r'\{0\}', '0', 'n']
        for answer, value in zip(self.answers, values):
            answer[':answer/value'] = value
        incoming = self.q['answer_fields'][0]
        incoming.update(correct_value=values[0], choices=[{'type':'math','value':v} for v in values])
        self.evidence('answer-field/choices', field_value(self.field, 'answer-field/choices'),
                      'mathematical_correction', 'selection', local=True)
        incoming['choices'][1]['value'] = r'\{0\}'
        self.evidence('answer-field/choices', sorted(('math', a['value']) for a in incoming['choices']),
                      'ma_complete_choices', 'selection')
        self.assertEqual(self.plan(), [])
        self.assertFalse(self.reconciler.needs_review)
        self.assertEqual([(d['attribute'], d.get('action')) for d in self.reconciler.decisions],
                         [('answer-field/choices', 'retain')])

    def test_identical_protected_bank_keeps_normal_merge(self):
        self.evidence('answer-field/choices', field_value(self.field, 'answer-field/choices'),
                      'mathematical_correction', 'selection', local=True)
        self.assertEqual(self.reconciler.field_action(self.mid, self.field, self.q['answer_fields'][0]), 'merge')
        self.assertEqual(self.reconciler.decisions, [])

    def test_bank_protection_requires_exact_attested_value(self):
        self.evidence('answer-field/choices', [('math', 'different bank')],
                      'mathematical_correction', 'selection', local=True)
        self.q['answer_fields'][0]['choices'] = [{'type':'math','value':v} for v in ['120', '60']]
        self.evidence('answer-field/choices', [('math', '120'), ('math', '60')],
                      'ma_complete_choices', 'selection')
        self.assertEqual(self.reconciler.field_action(self.mid, self.field, self.q['answer_fields'][0]), 'version')
        self.assertFalse(self.reconciler.needs_review)


class CorrectionEvidenceTests(unittest.TestCase):
    def test_full_bank_evidence_is_opt_in_and_transaction_bound(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            directory = root/'mathematical-corrections/q-1'
            directory.mkdir(parents=True)
            review, tx = directory/'review.json', directory/'transaction.edn'
            content = {'math_academy_id':'q-1', 'problem':'Null-space theorem', 'worked_solution':'Null(A)={0}.',
                       'answer_fields':[{'key':'selection', 'correct_value':r'\{0\}', 'protect_choices':True,
                                         'choices':[{'type':'math','value':r'\{0\}'}, {'type':'math','value':'0'}]}]}
            review.write_text(json.dumps({'rationale':'Scalar zero differs from the singleton-zero set.',
                                          'corrected_content':content}))
            tx.write_text('[]')
            proof = {'committed':True, 'mathematical_check_passed':True, 'basis_after':12,
                     'review_sha256':hashlib.sha256(review.read_bytes()).hexdigest(),
                     'transaction_sha256':hashlib.sha256(tx.read_bytes()).hexdigest()}
            (directory/'verification.json').write_text(json.dumps(proof))
            records = mathematical_correction_records(root, {'q-1'})
            bank = [r for r in records if r['attribute']=='answer-field/choices']
            self.assertEqual(len(bank), 1)
            self.assertEqual(bank[0]['value'], [('math', '0'), ('math', r'\{0\}')])
            tx.write_text('[changed]')
            self.assertEqual(mathematical_correction_records(root, {'q-1'}), [])

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
