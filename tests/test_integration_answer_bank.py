"""Regressions for full-answer support and logarithmic equivalence."""
import json
from pathlib import Path
import sys
import unittest
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'generate'))
from integration_answer_bank import answer_bank
from scripts.integration_support_policy import validate_prerequisite_recall


class CompleteIntegralBankTests(unittest.TestCase):
    def test_log_argument_multiples_are_not_false_distractors(self):
        x,u=s.symbols('x u',positive=True)
        bank=answer_bank(s.log(x*x+1),s.log(u),x*x+1,x,u,'log-regression',str)
        values=[s.sympify(text.removesuffix('+C'),locals={'x':x})for text,_ in bank]
        for i,a in enumerate(values):
            for b in values[:i]:
                self.assertNotEqual(s.simplify(s.diff(a-b,x)),0)
        self.assertNotIn('double_inner',[label for _,label in bank])
        self.assertNotIn('half_inner',[label for _,label in bank])

    def test_definite_bank_contains_complete_distinct_values(self):
        x,u=s.symbols('x u',real=True)
        bank=answer_bank(s.Rational(1,2),u*u/2,x,x,u,'definite',str,lower=s.Integer(0),upper=s.Integer(1))
        self.assertEqual(len(bank),5)
        self.assertEqual(len({s.sympify(text)for text,_ in bank}),5)
        self.assertEqual(next(text for text,label in bank if label=='correct'),'1/2')
        self.assertTrue(all('+C'not in text for text,_ in bank))

    def test_leaked_substitution_is_rejected_despite_false_metadata(self):
        for hint in ('Use the substitution $u=x^2$.','Let $u=x^2$.'):
            record={'question':{':question/problem':'Find an antiderivative. '+hint},
                    'generation':{'support_policy':'mastered-prerequisite-recall',
                                  'provided_primitive':False,'provided_endpoint_values':False,
                                  'provided_substitution':False,'operation':'evaluate'}}
            with self.assertRaisesRegex(ValueError,'recognition'):
                validate_prerequisite_recall(record)

    def test_secant_bands_have_distinct_differential_work(self):
        h=ROOT/'reference/edb-math/repairs/2026-10-25-restore-substitution-recognition/17592186064250'
        rows=json.loads((h/'accepted-pool.json').read_text())
        for r in rows:
            factor=s.Rational(r['generation']['model']['factor'])
            band=r['question'][':question/difficulty'].rsplit('/',1)[-1]
            if band=='easy':
                self.assertEqual(factor.q,1)
                self.assertLessEqual(factor,3)
            if band=='moderate':self.assertNotEqual(factor.q,1)


if __name__=='__main__':unittest.main()
