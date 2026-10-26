"""Rounded calculator answers must not become adjacent-rounding quizzes."""
import copy
from decimal import Decimal
import importlib.util
import json
from pathlib import Path
import random
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'generate'))
from rounded_finance import away_from_halfway
from scripts.rounded_finance_batch_policy import validate_delivery_batch,displayed_number

def load(kp):
    folder=ROOT/f'generate/scratch/{kp}'
    sys.path.insert(0,str(folder))
    spec=importlib.util.spec_from_file_location('finance_'+str(kp),folder/'generator.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

class RoundedFinanceSpacingTests(unittest.TestCase):
    def test_reported_gas_case_has_no_one_cent_alternative(self):
        kp=17592186059796;g=load(kp)
        r=g.make('gas',2.23,-2.2,6,3,1,random.Random(7))
        validate_delivery_batch([r],kp)
        self.assertEqual(r['generation']['final_expression'],'2.54')
        self.assertIn('2.54467155',r['question'][':question/worked-solution'])
        values=[displayed_number(a[':answer/value'])for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
        self.assertIn(Decimal('2.54'),values)
        self.assertNotIn(Decimal('2.55'),values)
        self.assertTrue(all(b-a>=Decimal('.05')for a,b in zip(sorted(values),sorted(values)[1:])))

    def test_false_metadata_cannot_hide_the_actual_reported_bank(self):
        kp=17592186059796;g=load(kp);r=g.make('gas',2.23,-2.2,6,3,1,random.Random(7))
        f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
        wrong=next(a for a in f[':answer-field/choices']if a[':answer/id']!=correct)
        wrong[':answer/value']=r'$\$2.55$ per gallon'
        with self.assertRaisesRegex(ValueError,'too close'):validate_delivery_batch([r],kp)

    def test_imported_initial_amount_banks_remain_valid(self):
        kp=17592186059796;g=load(kp)
        for context,current,rate,time in(('profit',16700,15,5),('gas',3.11,-1,5)):
            validate_delivery_batch([g.make(context,current,rate,time,2,2,random.Random(1),replay=True)],kp)

    def test_rate_and_time_banks_use_the_source_separations(self):
        kp=17592186059797;g=load(kp)
        for family in('rate','time'):
            for i in range(50):
                values=g.sample_bank(family,random.Random(i))
                self.assertGreaterEqual(min(b-a for a,b in zip(values,values[1:])),3 if family=='rate'else 2)

    def test_all_fresh_families_obey_the_displayed_spacing(self):
        for kp in(17592186059796,17592186059797,17592186059798):
            g=load(kp)
            for seed in(7,37,20261026):validate_delivery_batch(g.generate(20,seed),kp)

    def test_generated_initial_cases_do_not_land_near_a_half_unit(self):
        g=load(17592186059796)
        for r in g.generate(50,31):
            self.assertTrue(away_from_halfway(Decimal(r['generation']['unrounded_answer']),r['generation']['rounding_places']))

    def test_legacy_unreviewed_generator_is_not_silently_published(self):
        kp=17592186059796;r=load(kp).generate(1,7)[0];r['generation'].pop('batch_contract')
        with self.assertRaisesRegex(ValueError,'contract'):validate_delivery_batch([r],kp)

if __name__=='__main__':unittest.main()
