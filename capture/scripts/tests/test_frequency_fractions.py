"""Protect original account evidence while selecting the requested weight fractions."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.round_encompassing_frequency import convert_account, generate, nearest_fraction


class FrequencyFractionTests(unittest.TestCase):
    def test_thirds_remain_exact_and_single_observation_is_retained(self):
        self.assertEqual(nearest_fraction(1, 3), Fraction(1, 3))
        self.assertEqual(nearest_fraction(2, 3), Fraction(2, 3))
        self.assertEqual(nearest_fraction(1, 1), Fraction(1))

    def test_exact_midpoint_rounds_up(self):
        self.assertEqual(nearest_fraction(9, 40), Fraction(1, 4))
        self.assertEqual(nearest_fraction(11, 30), Fraction(2, 5))
        self.assertEqual(nearest_fraction(9, 10), Fraction(1))

    def test_requested_minimum_fraction_is_used(self):
        self.assertEqual(nearest_fraction(1, 100), Fraction(1, 5))

    def test_nonpositive_candidates_and_invalid_counts_are_rejected(self):
        for counts in ((0, 3), (1, 0), (4, 3), (1.0, 3), (True, 3)):
            with self.subTest(counts=counts), self.assertRaises(ValueError):
                nearest_fraction(*counts)

    def make_report(self, folder, account='foundations'):
        original = folder / (account + '.json')
        original.write_text('{}\n')
        report = dict(account=account, source_report=str(original),
                      source_report_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),
                      created_at='frozen', method='original frequency method',
                      proposals=[dict(account=account, source='10', target='20',
                                      eligible_activities=3, rising_activities=1,
                                      frequency_weight_estimate=1 / 3,
                                      proposed_starting_coverage_weight=.35,
                                      sequence=[dict(account=account, before=1, after=after)
                                                for after in (6, 1, 1)])])
        path = folder / (account + '-frequency-estimates.json')
        path.write_text(json.dumps(report))
        return path, report

    def test_raw_frequency_sequences_and_original_file_are_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            path, original = self.make_report(Path(temporary))
            before = path.read_bytes()
            result = convert_account(path, 'foundations')
            item = result['proposals'][0]
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(item['sequence'], original['proposals'][0]['sequence'])
            self.assertEqual(item['frequency_weight_estimate'], 1 / 3)
            self.assertEqual(item['rising_activities'], 1)  # 1→6 counts once.
            self.assertEqual(item['weight_fraction'], '1/3')
            self.assertEqual(item['original_proposed_starting_coverage_weight'], .35)
            self.assertEqual(result['source_report_sha256'], original['source_report_sha256'])
            self.assertEqual(result['original_frequency_estimates_sha256'], hashlib.sha256(before).hexdigest())

    def test_account_mismatch_and_cross_account_sequence_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path, report = self.make_report(Path(temporary))
            with self.assertRaisesRegex(ValueError, 'Source account'):
                convert_account(path, 'linear')
            report['proposals'][0]['sequence'][0]['account'] = 'linear'
            path.write_text(json.dumps(report))
            with self.assertRaisesRegex(ValueError, 'Cross-account'):
                convert_account(path, 'foundations')

    def test_generator_keeps_account_estimates_separate_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            snapshots = {}
            for account in ('foundations', 'linear', 'multivariable', 'differential'):
                path, _ = self.make_report(folder, account)
                snapshots[path] = path.read_bytes()
            with self.assertRaisesRegex(ValueError, 'separate'):
                generate(folder, folder)
            summary = generate(folder)
            self.assertEqual(summary['account_specific_relationships'], 4)
            self.assertEqual(summary['unique_source_target_pairs'], 1)
            self.assertEqual(summary['fraction_counts']['1/3'], 4)
            for path, content in snapshots.items():
                self.assertEqual(path.read_bytes(), content)
                output = json.loads((folder / 'frequency-fractions' / path.name).read_text())
                self.assertEqual(output['account'], output['proposals'][0]['account'])

    def test_modified_underlying_report_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path, report = self.make_report(Path(temporary))
            Path(report['source_report']).write_text('{"modified": true}')
            with self.assertRaisesRegex(ValueError, 'hash'):
                convert_account(path, 'foundations')


if __name__ == '__main__':
    unittest.main()
