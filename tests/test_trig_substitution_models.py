"""Regressions for the revised scaffolded topic478 pedagogy and delivery gates."""
import copy
import importlib.util
from pathlib import Path
import random
import sys
import unittest
import uuid

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'generate/scratch/17592186068915'))
sys.path.insert(0,str(ROOT))
from scripts.trig_substitution_batch_policy import validate_delivery_batch


def load_model():
    spec=importlib.util.spec_from_file_location('reviewed_trig_scaffold',ROOT/'generate/trig_scaffold.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m


def evidence(kp):
    return {'kp':{'db_id':kp,'id':str(uuid.uuid5(uuid.NAMESPACE_URL,'test:'+str(kp))),'title':'Trig substitution fixture'},
            'basis':0,'excluded_tasks':[],'band_origin':{b:'test fixture'for b in('easy','moderate','hard')}}


class TrigSubstitutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.g=load_model()

    def rows(self,kp,band,count=8):
        return self.g.batch(kp,band,count,17,evidence=evidence(kp))

    def test_easy_supplies_the_substitution_and_stops_at_transformation(self):
        for kp in self.g.CASES:
            rows=self.rows(kp,'easy')
            validate_delivery_batch(rows,kp)
            for row in rows:
                q=row['question'];f=q[':question/answer-fields'][0]
                self.assertIn('Use the substitution $u=',q[':question/problem'])
                self.assertEqual(f[':answer-field/type'],':answer-field.type/radio')
                self.assertEqual(len(f[':answer-field/choices']),5)
                self.assertTrue(all(r'\int'in a[':answer/value']for a in f[':answer-field/choices']))
                self.assertEqual(row['generation']['operation'],'transform')

    def test_full_questions_supply_the_prerequisite_formula_and_endpoint_facts(self):
        for kp in self.g.CASES:
            for band in('moderate','hard'):
                rows=self.rows(kp,band)
                validate_delivery_batch(rows,kp)
                for r in rows:
                    self.assertIn('You may use $',r['question'][':question/problem'])
                    if r['generation']['model']['lower']is not None:
                        self.assertIn('Endpoint values:',r['question'][':question/problem'])

    def test_same_instance_cannot_become_fresh_by_resampling_distractors(self):
        kp=17592186068915;g=self.g
        m=g.trig_instance(kp,'easy','indef_sin',random.Random(81))
        a=g.render(kp,'easy','indef_sin',m,1,evidence(kp),random.Random(1))
        b=g.render(kp,'easy','indef_sin',m,2,evidence(kp),random.Random(2))
        self.assertEqual(a['question'],b['question'])

    def test_delivery_rejects_large_rendered_components_even_with_small_metadata(self):
        r=self.rows(17592186068915,'easy',1)[0]
        r['question'][':question/problem']+=' The multiplier is $24$.'
        with self.assertRaisesRegex(ValueError,'arithmetic budget'):
            validate_delivery_batch([r],17592186068915)

    def test_delivery_rejects_removed_support_and_unshown_final_conversion(self):
        r=self.rows(17592186068918,'moderate',1)[0]
        bad=copy.deepcopy(r);bad['question'][':question/problem']=bad['question'][':question/problem'].replace('You may use','Recall')
        with self.assertRaises(ValueError):validate_delivery_batch([bad],17592186068918)
        bad=copy.deepcopy(r);bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']+=' + 0'
        with self.assertRaisesRegex(ValueError,'canonical answer fragment'):validate_delivery_batch([bad],17592186068918)

    def test_products_hard_uses_inner_recognition_without_radical_bounds(self):
        rows=self.rows(17592186068917,'hard')
        self.assertEqual({r['generation']['family']for r in rows},set(self.g.CASES[17592186068917]['hard']))
        for r in rows:
            m=r['generation']
            self.assertIn(m['parameters']['inner_role'],('reciprocal','sqrt'))
            self.assertIsNone(m['model']['lower'])

    def test_actual_batch_rejects_clones_and_legacy_contracts(self):
        kp=17592186068917;r=self.rows(kp,'moderate',1)[0]
        with self.assertRaisesRegex(ValueError,'Amplitude-only'):validate_delivery_batch([r,copy.deepcopy(r)],kp)
        old=copy.deepcopy(r);old['generation']['batch_contract']='trig-substitution-v3'
        with self.assertRaisesRegex(ValueError,'scaffolded'):validate_delivery_batch([old],kp)


if __name__=='__main__':unittest.main()
