"""Regressions for frozen subgroups and band-contract escape routes."""
import importlib.util
from pathlib import Path
import unittest


ROOT=Path(__file__).resolve().parents[1]


class LinearTrigGeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=ROOT/'generate/scratch/17592186068915.py'
        spec=importlib.util.spec_from_file_location('linear_trig_public_generator',path)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_each_easy_family_covers_response_shapes_and_indefinite_signs_independently(self):
        rows=self.g.batch('easy',16,17)
        self.assertEqual(len({r['generation']['mathematical_fingerprint'] for r in rows}),16)
        for case in self.g.CASES['easy']:
            members=[r['generation'] for r in rows if r['generation']['template']==case]
            self.assertEqual({r['response'] for r in members},{'radio','blank'})
            if case.startswith('indef'):
                roles={(r['response'],int(self.g.sp.sign(self.g.sp.sympify(r['parameters']['slope'])))) for r in members}
                self.assertEqual(roles,{('radio',1),('radio',-1),('blank',1),('blank',-1)})
        blanks=[r['generation']['parameters'] for r in rows if r['generation']['template'].startswith('def_') and r['generation']['response']=='blank']
        self.assertEqual({p['function'] for p in blanks},{'sin','cos'})
        self.assertGreater(len({p['amplitude'] for p in blanks}),1)

    def test_zero_outcome_has_a_complete_distinct_bank(self):
        r=self.g.build('easy','def_cos',('cos',2,3,0,0,self.g.PI/3),response='radio')
        field=r['question'][':question/answer-fields'][0]
        choices=field[':answer-field/choices'];self.assertEqual(len({a[':answer/value'] for a in choices}),5)
        correct=next(a for a in choices if a[':answer/id']==field[':answer-field/correct'][1])
        self.assertEqual(correct[':answer/value'],'0')

    def test_hard_requires_compounded_work_and_exact_entry(self):
        with self.assertRaises(ValueError):
            self.g.build('hard','compound_sin_positive',('sin',2,3,0,0,self.g.PI/6))
        g=self.g
        values=('sin',g.R(5,3),g.R(-3,2),g.PI,g.PI/9,g.PI/2)
        with self.assertRaises(ValueError):g.build('hard','compound_sin_negative',values,response='radio')
        record=g.build('hard','compound_sin_negative',values)
        self.assertEqual(record['question'][':question/difficulty'],':question.difficulty/hard')
        self.assertEqual(record['question'][':question/answer-fields'][0][':answer-field/type'],':answer-field.type/blank')


if __name__=='__main__':unittest.main()
