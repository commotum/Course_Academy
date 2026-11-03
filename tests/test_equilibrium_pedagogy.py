import copy
import importlib.util
from pathlib import Path
import random
import sys
import unittest
import sympy as S
from generate.equilibrium_pedagogy import KP, validate_delivery_batch

PACKAGE = Path(__file__).resolve().parents[1] / 'reference/edb-math/repairs/2026-11-02-equilibrium-generator/package'
sys.path.insert(0, str(PACKAGE))
spec = importlib.util.spec_from_file_location('equilibrium_repair', PACKAGE / 'generator.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


class EquilibriumPedagogyTests(unittest.TestCase):
    def test_reported_shifted_log_uses_one_factored_residual(self):
        y = g.Y
        residual = (y-1)**2*S.log(y-1)+S.exp(-2)
        # The retained original equation must still be explainable clearly.
        rhs = S.Add(y+1, residual, evaluate=False)
        record = g.render(g.model(y+1, rhs, [2, 1+S.E, 1+S.exp(-1)],
                                'logarithmic', [('positive', y-1)]), 'moderate')
        solution = record['question'][':question/worked-solution']
        self.assertIn(r'\left(c - 1\right)^{2}', solution)
        self.assertNotIn('L(c)', solution)
        self.assertNotIn('R(c)', solution)
        self.assertEqual([p['key'] for p in record['generation']['solution_path']], [False, False, True])
        # New delivery must reject the old padding even with a repaired solution.
        with self.assertRaisesRegex(ValueError, 'cancelling'):
            validate_delivery_batch([record], KP)

    def test_sources_retain_all_complete_banks(self):
        replay = g.replay()
        self.assertEqual([[p['key'] for p in r['generation']['solution_path']] for r in replay],
                         [[False, False, True], [False, False, True], [True, True, False],
                          [False, False, True], [False, False, True]])
        validate_delivery_batch(replay, KP)

    def test_delivered_progression_is_deterministic_and_varied(self):
        for i, band in enumerate(('easy', 'moderate', 'hard')):
            a = g.generate(band, 202611020+i, 5)
            self.assertEqual(a, g.generate(band, 202611020+i, 5))
            validate_delivery_batch(a, KP)
            self.assertEqual(len({r['question'][':question/problem'] for r in a}), 5)
            self.assertEqual({r['generation']['template'] for r in a}, set(g.FAMILIES[band]))
            self.assertFalse(g.repeated_label_cue(a))
            for record in a:
                self.assertNotIn('constant function', record['question'][':question/problem'])
                self.assertLess(len(record['question'][':question/worked-solution']), 2500)

    def test_hard_requires_valid_nonroot_as_well_as_excluded_value(self):
        y = g.Y
        m = g.model(0, (y-1)*S.log(y), [0, 1, S.E], 'logarithmic-domain', [('positive', y)])
        record = g.render(m, 'hard')
        validate_delivery_batch([record], KP)
        # This is the old shortcut: every valid choice is an equilibrium.
        bad = g.render(g.model(0, (y-S.E)*S.log(y), [0, 1, S.E],
                               'logarithmic-domain', [('positive', y)]), 'hard')
        with self.assertRaisesRegex(ValueError, 'valid non-equilibrium'):
            validate_delivery_batch([bad], KP)

    def test_wrong_key_hint_and_expanded_work_are_rejected(self):
        base = g.generate('moderate', 202611021, 5)[1]
        mutants = []
        hint = copy.deepcopy(base)
        hint['question'][':question/problem'] += ' A constant function makes the derivative zero.'
        mutants.append(hint)
        key = copy.deepcopy(base)
        field = key['question'][':question/answer-fields'][0]
        field[':answer-field/correct'][1] = next(a[':answer/id'] for a in field[':answer-field/choices']
            if a[':answer/id'] != field[':answer-field/correct'][1])
        mutants.append(key)
        expanded = copy.deepcopy(base)
        original = expanded['generation']['printed_residual']
        expanded['question'][':question/worked-solution'] = expanded['question'][':question/worked-solution'].replace(original, 'c^2+2c+1')
        mutants.append(expanded)
        for mutant in mutants:
            with self.assertRaises(ValueError):
                validate_delivery_batch([mutant], KP)

    def test_other_kps_unaffected(self):
        validate_delivery_batch([{'question': {}}], KP+1)

    def test_valid_wrapped_residuals_survive_delivery(self):
        y = g.Y
        m = g.model(y-1, 2*S.sin(y-1)+S.pi, [1, 1+S.pi, 1-S.pi], 'trigonometric')
        validate_delivery_batch([g.render(m, 'moderate')], KP)
        for band in ('easy', 'moderate', 'hard'):
            for family in g.FAMILIES[band]:
                for seed in (0, 1):
                    record = g.render(g.sampled_model(random.Random(seed), band, family), band)
                    validate_delivery_batch([record], KP)


if __name__ == '__main__':
    unittest.main()
