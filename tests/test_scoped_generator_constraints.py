"""Source-supported neighbors survive removal of incidental design mandates."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'generate'))
import sympy as s
import substitution_pedagogy as model
from scripts.substitution_pedagogy_batch_policy import validate_delivery_batch
from scripts.inverse_substitution_batch_policy import validate_delivery_batch as inverse_guard
from scripts.kp2_integration_policy import validate_delivery_batch as sum_guard, shortcut_failures

CAPTURE = ROOT / 'reference/edb-math/repairs/2026-10-25-restore-substitution-recognition'


class ScopedConstraintTests(unittest.TestCase):
    def evidence(self, kp):
        return json.loads((CAPTURE / str(kp) / 'package/source-evidence.json').read_text())

    def test_source_hard_positive_derivative_and_quartic_remain_available(self):
        # q-211992 is a positive-inner-derivative hard example; canonical
        # e-14403 uses x^4. Neither sign nor excluding fourth powers is a law.
        kp = 17592186184350
        source = json.loads((CAPTURE / str(kp) / 'source.json').read_text())['material']['kp']
        self.assertTrue(any(q.get(':question/math-academy-id') == 'q-211992'
                            for q in source[':knowledge-point/questions']))
        rows = [model.generate(kp, 'hard', seed, template='quartic', evidence=self.evidence(kp))
                for seed in range(8)]
        self.assertEqual({s.Rational(r['generation']['parameters']['slope']) > 0 for r in rows}, {True, False})
        for row in rows:
            validate_delivery_batch([row], kp)
            m = row['generation']['model']
            primitive = s.sympify(m['primitive'], locals={'x': model.X})
            integrand = s.sympify(m['integrand'], locals={'x': model.X})
            self.assertEqual(s.simplify(s.diff(primitive, model.X) - integrand), 0)
            self.assertNotIn('Use the substitution', row['question'][':question/problem'])

    def test_definite_hard_can_use_the_canonical_power_family(self):
        kp = 17592186184352
        for seed in (2, 7):
            row = model.generate(kp, 'hard', seed, template='square_e', evidence=self.evidence(kp))
            validate_delivery_batch([row], kp)
            m = row['generation']['model']
            primitive = s.sympify(m['primitive'], locals={'x': model.X})
            actual = s.simplify(primitive.subs(model.X, s.sympify(m['upper'])) - primitive.subs(model.X, s.sympify(m['lower'])))
            self.assertEqual(s.simplify(actual - s.sympify(m['result'])), 0)
            self.assertEqual(row['generation']['family'], 'square_e')

    def test_plausible_smaller_bank_is_not_rejected_to_preserve_five_choices(self):
        for kp in (17592186184349, 17592186064218):
            row = model.generate(kp, 'easy', 7, evidence=self.evidence(kp))
            field = row['question'][':question/answer-fields'][0]
            correct = field[':answer-field/correct'][1]
            indices = [i for i, a in enumerate(field[':answer-field/choices']) if a[':answer/id'] == correct]
            indices += [i for i, a in enumerate(field[':answer-field/choices']) if a[':answer/id'] != correct][:2]
            field[':answer-field/choices'] = [field[':answer-field/choices'][i] for i in indices]
            row['generation']['bank_recipes'] = [row['generation']['bank_recipes'][i] for i in indices]
            (inverse_guard if kp == 17592186064218 else validate_delivery_batch)([row], kp)
            self.assertEqual(len(field[':answer-field/choices']), 3)

    def test_inverse_canonical_scalings_reachable_in_ordinary_generation(self):
        targets={17592186064218:('sine',7,{'A':'1','B':'9','numerator':'9/4'}),
                 17592186064219:('tangent',101,{'A':'2','B':'50','numerator':'3'})}
        for kp,(family,seed,params) in targets.items():
            evidence=self.evidence(kp)
            # Demonstrate the normal mathematical domain before the separate
            # exclusion of already-imported/served exact tasks.
            evidence['excluded_tasks']=[]
            found=model.generate(kp,'moderate',seed,template=family,evidence=evidence)
            self.assertTrue(all(found['generation']['parameters'][key]==value for key,value in params.items()))
            inverse_guard([found],kp)
            m=found['generation']['model']
            derivative=s.diff(s.sympify(m['primitive'],locals={'x':model.X}),model.X)
            self.assertEqual(s.simplify(derivative-s.sympify(m['integrand'],locals={'x':model.X})),0)

    def test_small_fragment_observation_does_not_become_a_rank_or_family_quota(self):
        # These two valid two-term instances happen to have the same key rank.
        # Their fragment is not evidence of a generator-wide construction law.
        from test_integration_batch_policy import g, KP
        rows = g.sample(KP, 8, 41, 'easy')[:2]
        for row in rows:
            row['generation']['batch_contract'] = 'sum-factor-kp2-v3'
            field = row['question'][':question/answer-fields'][0]
            pairs = list(zip(field[':answer-field/choices'], row['generation']['bank_terms']))
            pairs.sort(key=lambda p: p[0][':answer/id'] != field[':answer-field/correct'][1])
            field[':answer-field/choices'] = [p[0] for p in pairs]
            row['generation']['bank_terms'] = [p[1] for p in pairs]
        self.assertTrue(shortcut_failures(rows))
        sum_guard(rows, KP)
        broken = copy.deepcopy(rows)
        broken[0]['generation']['bank_terms'][0][0][1] = '19'
        with self.assertRaisesRegex(ValueError, 'powers'):
            sum_guard(broken, KP)


if __name__ == '__main__':
    unittest.main()
