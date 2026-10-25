"""Regressions for the live inverse-trig pedagogy audit."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'generate'))
import substitution_pedagogy as model
from scripts.inverse_substitution_batch_policy import validate_delivery_batch,KPS,VERSION

H=ROOT/'reference/edb-math/repairs/2026-10-25-inverse-trig-quality'
OLD=H.with_name('2026-10-25-restore-substitution-recognition')
def rows(kp):return json.loads((H/str(kp)/'accepted-pool.json').read_text())

class InverseSubstitutionQualityTests(unittest.TestCase):
    def test_final_pools_preserve_quality_after_delivery(self):
        for kp in KPS:validate_delivery_batch(rows(kp),kp)

    def test_cancellation_is_easy_instead_of_forbidden(self):
        # The actual reported hard instance, after changing only its band and
        # current contract, must be accepted as a small direct-form question.
        kp=17592186064219
        r=next(r for r in json.loads((OLD/str(kp)/'accepted-pool.json').read_text())
               if r['generation']['parameters']=={'A':'4','B':'16','numerator':'4','scale':'2'})
        r['generation']['batch_contract']=VERSION
        with self.assertRaisesRegex(ValueError,'cancellation'):validate_delivery_batch([r],kp)
        r['question'][':question/difficulty']=':question.difficulty/easy'
        validate_delivery_batch([r],kp)

    def test_generic_filler_cannot_be_reintroduced(self):
        for kp in KPS:
            r=rows(kp)[0]
            r['generation']['bank_recipes'][0]='return_substitution'
            with self.assertRaisesRegex(ValueError,'filler'):validate_delivery_batch([r],kp)
        r=rows(17592186064220)[0];r['generation']['bank_recipes'][0]='endpoint_offset_2'
        with self.assertRaisesRegex(ValueError,'filler'):validate_delivery_batch([r],17592186064220)

    def test_endpoint_coverage_is_checked_on_the_delivered_batch(self):
        kp=17592186064220;pool=rows(kp)[16:]
        for r in pool:
            p=r['generation']['parameters'];p['normalized_lower']='0';p['normalized_upper']='1'
        with self.assertRaisesRegex(ValueError,'Endpoint coverage'):validate_delivery_batch(pool,kp)

    def test_sampling_retains_the_progression_for_new_seeds(self):
        for kp in KPS:
            ev=json.loads((H/str(kp)/'package/source-evidence.json').read_text())
            for seed in(7,112358):
                for band in('easy','moderate','hard'):
                    validate_delivery_batch(model.batch(kp,band,8,seed,evidence=ev),kp)

if __name__=='__main__':unittest.main()
