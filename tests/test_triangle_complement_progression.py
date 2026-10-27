"""Protect the assessed operation, not just answer formatting."""
import copy,json
from pathlib import Path
import unittest
from generate.triangle_complement_contract import inspect_record,validate_delivery_batch,KP
from scripts.generator_publish import prepare_records

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/'reference/edb-math/repairs/2026-10-27-triangle-area-progression'

class TriangleProgressionTests(unittest.TestCase):
    def setUp(self):
        self.rows=json.loads((FIXTURE/'candidate-pool.json').read_text())

    def test_each_band_requires_the_same_two_steps(self):
        validate_delivery_batch(self.rows,KP)
        self.assertEqual({r['question'][':question/difficulty'].split('/')[-1] for r in self.rows},{'easy','moderate','hard'})

    def test_original_given_area_question_fails(self):
        q=next(q for q in json.loads((FIXTURE/'before.json').read_text())[':knowledge-point/questions'] if q[':db/id']==17592186561416)
        q=copy.deepcopy(q);q[':question/difficulty']=':question.difficulty/easy'
        with self.assertRaisesRegex(ValueError,'Both sides'):inspect_record({'question':q})

    def test_method_hint_is_rejected_even_with_correct_answer(self):
        row=copy.deepcopy(self.rows[0]);row['question'][':question/problem']+=' Hint: first calculate the triangle area.'
        with self.assertRaisesRegex(ValueError,'leave the triangle'):inspect_record(row)

    def test_wrong_key_cannot_be_hidden_by_metadata(self):
        row=copy.deepcopy(self.rows[0]);f=row['question'][':question/answer-fields'][0]
        f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
        with self.assertRaisesRegex(ValueError,'answer does not match'):inspect_record(row)

    def test_publisher_runs_the_guard_after_delivery_filtering(self):
        row=copy.deepcopy(self.rows[0]);row['question'][':question/problem']+=' Hint: use half the product.'
        with self.assertRaisesRegex(ValueError,'leave the triangle'):
            prepare_records([row],KP,row['knowledge_point']['id'],set(),ROOT,ROOT,localizer=lambda r,*args:r)

    def test_other_kps_are_unaffected(self):
        validate_delivery_batch([{}],17592186105907)

if __name__=='__main__':unittest.main()
