"""Calibration checks for temporal leakage, sparse evidence, and display noise."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from scripts import calibrate_encompassing_pilot as pilot


def row(task=1, **changes):
    values = dict(account='foundations', task_id=str(task), source='D', target='D',
                  direct=True, kind='review', before=1, after=2, positive_steps=1,
                  accuracy=.6, pipeline='legacy', hours_since_target_direct=12.,
                  hours_since_potential_target_practice=6.)
    values.update(changes)
    values['positive_steps'] = max(0, values['after'] - values['before'])
    return values


def constant_model(amplitude=1., residual=.1):
    return dict(clock=None, growth=2, half_life_hours=None, amplitude=amplitude,
                residual=residual, age_quantiles={})


def write_fixture(folder, rows):
    (folder / 'timing-magnitude').mkdir(exist_ok=True)
    (folder / 'timing-magnitude/foundations.json').write_text(json.dumps({'observations': rows}))
    audit = [{'task_id': str(i), 'time': f'2026-10-{i:02}T00:00:00Z'} for i in range(1, 11)]
    (folder / 'foundations.json').write_text(json.dumps({'activity_audit': audit}))


def fixture_rows():
    rows = [row(i, after=1 + i % 2, hours_since_target_direct=float(i * 3)) for i in range(1, 11)]
    rows[7][pilot.DIRECT_CLOCK] = None
    rows[7][pilot.POTENTIAL_CLOCK] = None
    # One early observation still nominates a relationship; its later outcomes
    # must not alter the training weight or the training age distribution.
    rows.extend(row(i, source='S', target='T', direct=False) for i in (2, 8, 9))
    # A rise first seen during evaluation must not nominate a new relationship.
    rows.append(row(10, source='FUTURE', target='ONLY', direct=False))
    return rows


class PilotTests(unittest.TestCase):
    def test_recommendations_use_requested_fractions_and_upward_ties(self):
        self.assertEqual([str(pilot.recommended_fraction(w)) for w in
                          (.11078, .225, .27046, .375, .55, .55988, .63972, .65968, .73952, .77944, .9)],
                         ['1/5', '1/4', '1/4', '2/5', '3/5', '3/5', '2/3', '2/3', '3/4', '4/5', '1'])
        self.assertEqual([pilot.recommended_fraction(f) for f in pilot.RECOMMENDED_FRACTIONS],
                         list(pilot.RECOMMENDED_FRACTIONS))
        with self.assertRaises(ValueError):
            pilot.round_fraction(-.1)

    def test_split_preserves_whole_tasks_and_equal_timestamp_group(self):
        audit = [dict(task_id=str(i), time=f'{i:02}') for i in range(10)]
        audit[7]['time'] = audit[6]['time']
        train, test, detail = pilot.split_tasks(audit)
        self.assertEqual(train, {str(i) for i in range(8)})
        self.assertEqual(test, {'8', '9'})
        self.assertFalse(train & test)
        self.assertLess(detail['last_train_time'], detail['first_test_time'])
        with self.assertRaisesRegex(ValueError, 'Duplicate task IDs'):
            pilot.split_tasks(audit + [audit[0]])
        with self.assertRaises(ValueError):
            pilot.split_tasks([])
        with self.assertRaises(ValueError):
            pilot.split_tasks([dict(task_id=str(i), time='same') for i in range(10)])

    def test_probability_mass_survives_saturation_and_signed_residual(self):
        rows = [row(before=5, after=6), row(before=4, after=2)]
        p = pilot.probabilities(rows, np.full((2, 11), 3.), residual=.2)
        np.testing.assert_allclose(p.sum(axis=1), 1.)
        self.assertTrue(np.all(p >= 0))
        self.assertAlmostEqual(p[0, 6], .8 + .2 / 7)
        self.assertAlmostEqual(p[1, 2], .2 / 7)
        self.assertTrue(np.isfinite(pilot.likelihood(rows, p)))

    def test_fractional_coverage_changes_magnitude_and_crossing_probability(self):
        rows = [row(before=1, after=2)]
        weak = pilot.predict(rows, constant_model(residual=0), weight=.25)
        strong = pilot.predict(rows, constant_model(residual=0), weight=.75)
        self.assertAlmostEqual(pilot.rise_probability(rows, weak)[0], .25)
        self.assertAlmostEqual(pilot.rise_probability(rows, strong)[0], .75)
        self.assertGreater((strong @ np.arange(7)).item(), (weak @ np.arange(7)).item())

    def test_unknown_age_uses_training_distribution_and_spacing_saturates(self):
        training = [row(hours_since_target_direct=12.)]
        pools = pilot.age_pools(training, pilot.DIRECT_CLOCK)
        model = dict(clock=pilot.DIRECT_CLOCK, half_life_hours=24., growth=2, amplitude=2.)
        observed = [row(hours_since_target_direct=None), row(hours_since_target_direct=0.),
                    row(hours_since_target_direct=24.), row(hours_since_target_direct=240.)]
        doses = pilot.dose(observed, model, pools)
        self.assertGreater(doses[0, 0], 0.)
        np.testing.assert_allclose(doses[1], 0.)
        np.testing.assert_allclose(doses[2], doses[3])
        np.testing.assert_allclose(doses[3], 2.)

    def test_future_outcomes_do_not_change_training_or_heldout_predictions(self):
        rows = fixture_rows()
        grid = dict(half_life_hours=[6, 24], amplitude=[.5, 1, 3], residual=[.05, .2])
        # A matching prior in another account must not influence this fit.
        other_account_prior = dict(account='linear', source='S', target='T', prior_mean=.99)
        with tempfile.TemporaryDirectory() as tmp, patch.object(pilot, 'GRID', grid):
            folder = Path(tmp)
            write_fixture(folder, rows)
            original = pilot.account_pilot(folder, 'foundations', [other_account_prior])
            changed = copy.deepcopy(rows)
            for r in changed:
                if int(r['task_id']) >= 8:
                    r['after'] = 6
                    r['positive_steps'] = 6 - r['before']
            write_fixture(folder, changed)
            future_changed = pilot.account_pilot(folder, 'foundations', [])

        self.assertEqual(original['models_trained_on_early_data'], future_changed['models_trained_on_early_data'])
        self.assertEqual(original['pairs'], future_changed['pairs'])
        self.assertNotEqual(original['full_data_models'], future_changed['full_data_models'])
        for label in ('direct_test_predictions', 'relationship_test_predictions'):
            self.assertEqual([r['predictions'] for r in original[label]],
                             [r['predictions'] for r in future_changed[label]])
        pairs = {(p['source'], p['target']): p for p in original['pairs']}
        self.assertNotIn(('FUTURE', 'ONLY'), pairs)
        self.assertEqual(pairs['S', 'T']['train_n'], 1)
        self.assertEqual(pairs['S', 'T']['test_n'], 2)
        self.assertEqual(pairs['S', 'T']['prior_mean'], .5)
        self.assertEqual(original['panels']['single_training_observation']['spacing']['n'], 2)

    def test_future_known_ages_do_not_leak_into_unknown_age_predictions(self):
        rows = fixture_rows()
        grid = dict(half_life_hours=[12], amplitude=[.5, 1], residual=[.1])
        with tempfile.TemporaryDirectory() as tmp, patch.object(pilot, 'GRID', grid):
            folder = Path(tmp)
            write_fixture(folder, rows)
            original = pilot.account_pilot(folder, 'foundations', [])
            changed = copy.deepcopy(rows)
            for r in changed:
                if int(r['task_id']) >= 9:
                    r[pilot.DIRECT_CLOCK] = 99999.
                    r[pilot.POTENTIAL_CLOCK] = 99999.
            write_fixture(folder, changed)
            future_changed = pilot.account_pilot(folder, 'foundations', [])
        self.assertEqual(original['models_trained_on_early_data'], future_changed['models_trained_on_early_data'])
        a = next(r for r in original['direct_test_predictions'] if r['task_id'] == '8')
        b = next(r for r in future_changed['direct_test_predictions'] if r['task_id'] == '8')
        self.assertIsNone(a[pilot.DIRECT_CLOCK])
        self.assertEqual(a['predictions'], b['predictions'])

    def test_mixed_account_observations_are_rejected_before_fitting(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            write_fixture(folder, [row(account='linear')])
            with self.assertRaises(AssertionError):
                pilot.account_pilot(folder, 'foundations', [])


if __name__ == '__main__':
    unittest.main()
