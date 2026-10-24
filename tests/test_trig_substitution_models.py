"""Regressions for source-copy repetition and unshown solution conversions."""
import copy
import importlib.util
import json
from pathlib import Path
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'generate/scratch/17592186068915'))
sys.path.insert(0,str(ROOT))
from scripts.trig_substitution_batch_policy import validate_delivery_batch


class TrigSubstitutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('trig_substitution_models',ROOT/'generate/scratch/trig_substitution.py')
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)
        cls.evidence={kp:json.loads((ROOT/f'generate/scratch/{kp}/source-evidence.json').read_text()) for kp in cls.g.CASE}

    def rows(self,kp,band,count=8,seed=17):
        return self.g.batch(kp,band,count,seed,evidence=self.evidence[kp])

    def test_reciprocal_pool_covers_all_four_families_and_both_derivative_signs(self):
        rows=self.rows(17592186068916,'moderate')
        for case in self.g.RECIP:
            self.assertEqual({self.g.s.sign(self.g.s.sympify(r['generation']['parameters']['a']))
                              for r in rows if r['generation']['family']==case},{-1,1})
        # Moderate endpoint work cannot always end at the old pi/2 shortcut.
        self.assertTrue(any('pi/2' not in r['generation']['model']['upper'] for r in rows))

    def test_log_keys_are_the_literal_worked_solution_final_not_independent_cas_forms(self):
        for case in ('sin2','csc','rearranged'):
            r=self.g.generate(17592186068918,'hard',17,case,evidence=self.evidence[17592186068918])
            field=r['question'][':question/answer-fields'][0]
            self.assertEqual(len(field[':answer-field/choices']),1)
            final=re.findall(r'\$\$\s*(.*?)\s*\$\$',r['question'][':question/worked-solution'],re.S)[-1].strip().rstrip('.')
            self.assertEqual(final,field[':answer-field/choices'][0][':answer/value'])
            if case!='rearranged':self.assertIn(r'\ln A-\ln B=\ln(A/B)',r['question'][':question/worked-solution'])
            validate_delivery_batch([r],17592186068918)

    def test_delivery_rejects_the_original_unshown_conversion_failure(self):
        r=self.rows(17592186068918,'hard',1)[0]
        r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']+=' + 0'
        with self.assertRaisesRegex(ValueError,'exact displayed canonical answer'):
            validate_delivery_batch([r],17592186068918)

    def test_delivery_rejects_amplitude_only_clones_and_lost_families(self):
        rows=self.rows(17592186068917,'moderate')
        clone=copy.deepcopy(rows[0])
        clone['generation']['model']['factor']='999'
        with self.assertRaisesRegex(ValueError,'Amplitude-only'):
            validate_delivery_batch([rows[0],clone],17592186068917)
        # Distinct numerical tasks from the same family still fail a full batch.
        family=rows[0]['generation']['family']
        narrow=[self.g.generate(17592186068917,'moderate',i,family,evidence=self.evidence[17592186068917]) for i in range(8)]
        with self.assertRaises(ValueError):validate_delivery_batch(narrow,17592186068917)

    def test_product_hard_does_not_repeat_the_zero_result_source_families(self):
        rows=self.rows(17592186068917,'hard',16)
        self.assertEqual(len({r['generation']['mathematical_fingerprint'] for r in rows}),16)
        self.assertTrue(all(self.g.s.sympify(r['generation']['model']['result'])!=0 for r in rows))
        self.assertEqual({r['generation']['family'] for r in rows},set(self.g.CASE[17592186068917]['hard']))

    def test_small_refills_change_family_with_seed_and_do_not_freeze_the_first_case(self):
        for kp in self.g.CASE:
            families={self.rows(kp,'easy',1,seed)[0]['generation']['family'] for seed in range(24)}
            self.assertEqual(families,set(self.g.CASE[kp]['easy']))

    def test_tangent_derivative_uses_the_familiar_secant_rule(self):
        r=self.g.generate(17592186068918,'moderate',17,'tan',evidence=self.evidence[17592186068918])
        blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',r['question'][':question/worked-solution'],re.S)
        self.assertIn(r'\sec',blocks[0])
        self.assertNotIn(r'\tan',blocks[0])


if __name__=='__main__':unittest.main()
