"""Checks that magnitude, missing history, and spacing controls survive analysis."""
import tempfile
import unittest
from pathlib import Path

from scripts.analyze_encompassing_timing import age_bin, magnitude_profiles, summarize, within_spacing
from scripts.prepare_encompassing_weights import prepare


def row(**changes):
    return dict(account='linear',task_id='1',source='S',target='T',before=1,after=2,
        delta=1,positive_steps=1,kind='review',accuracy=.6,pipeline='legacy',
        nominated=True,direct=False,hours_since_target_direct=7,
        background_signed_steps=0,**{}) | changes


class TimingTests(unittest.TestCase):
    def test_magnitude_is_not_binary_and_flat_remains(self):
        stats=summarize([row(after=6,delta=5),row(before=3,after=4,delta=1),row(after=1,delta=0)])
        self.assertEqual(stats['rises'],2)
        self.assertEqual(stats['flats'],1)
        self.assertEqual(stats['mean_positive_steps'],2)
        self.assertEqual(stats['multi_band_rises'],1)

    def test_unknown_age_is_not_zero(self):
        self.assertEqual(age_bin(None),'unknown')
        self.assertEqual(age_bin(0),'<6h')
        self.assertEqual(age_bin(12),'12–24h')

    def test_regression_controls_starting_band_and_omits_unknown_age(self):
        rows=[row(delta=0,hours_since_target_direct=7),row(task_id='2',delta=1,hours_since_target_direct=15),
              row(task_id='3',before=2,delta=50,hours_since_target_direct=7),
              row(task_id='4',before=2,delta=51,hours_since_target_direct=15),
              row(task_id='5',delta=1000,hours_since_target_direct=None)]
        fit=within_spacing(rows)
        self.assertEqual(fit['n'],4)
        self.assertEqual(fit['strata'],2)
        self.assertAlmostEqual(fit['coefficients']['hours_since_target_direct'],1)

    def test_mixed_account_controls_are_rejected(self):
        with self.assertRaises(AssertionError):
            within_spacing([row(),row(account='foundations')])

    def test_single_activity_survives_but_zero_anchor_is_not_a_weight(self):
        previous=dict(account='linear',proposals=[dict(source='S',target='T',source_title='S',target_title='T',
            eligible_activities=1,frequency_weight_estimate=1)])
        rows=[row(),row(task_id='control',source='T',nominated=False,direct=True,delta=0,positive_steps=0)]
        profile=magnitude_profiles(rows,previous)[0]
        self.assertEqual(profile['n'],1)
        self.assertEqual(profile['scale_status'],'zero_direct_anchor')
        self.assertIsNone(profile['operational_weight'])
        self.assertIsNone(profile['relative_display_response'])

    def test_magnitude_ratio_above_one_is_not_silently_clamped(self):
        previous=dict(account='linear',proposals=[dict(source='S',target='T',source_title='S',target_title='T',
            eligible_activities=1,frequency_weight_estimate=1)])
        profiles=magnitude_profiles([row(after=6,delta=5,positive_steps=5),
            row(task_id='control',source='T',direct=True,nominated=False)],previous)
        self.assertEqual(profiles[0]['relative_display_response'],5)
        self.assertEqual(profiles[0]['scale_status'],'above_full_coverage_scale')
        self.assertIsNone(profiles[0]['operational_weight'])

    def test_superseded_transaction_cannot_be_regenerated(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)
            (path/'superseded.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'superseded'):
                prepare(path,path,path)


if __name__=='__main__':
    unittest.main()
