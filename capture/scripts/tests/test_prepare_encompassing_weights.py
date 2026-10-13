"""Check reconciliation of independent account estimates for shared topic data."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.prepare_encompassing_weights import (choose_account_estimate, coverage_audit,
                                                  graph_coverage, prepare, validate_fraction_estimate)


class InitialEncompassingPreparationTests(unittest.TestCase):
    def test_uses_one_most_observed_account_estimate_without_averaging(self):
        first = dict(account='foundations',eligible_activities=2,proposed_starting_coverage_weight=1.)
        second = dict(account='linear',eligible_activities=3,proposed_starting_coverage_weight=.35)
        self.assertIs(choose_account_estimate([first,second]),second)

    def test_equal_sample_counts_choose_lower_weight(self):
        first = dict(account='foundations',eligible_activities=2,proposed_starting_coverage_weight=1.)
        second = dict(account='linear',eligible_activities=2,proposed_starting_coverage_weight=.5)
        self.assertIs(choose_account_estimate([first,second]),second)

    def test_single_activity_estimate_is_kept(self):
        estimate = dict(account='multivariable',eligible_activities=1,proposed_starting_coverage_weight=1.)
        self.assertIs(choose_account_estimate([estimate]),estimate)

    def test_remaining_tie_is_deterministic(self):
        first = dict(account='multivariable',eligible_activities=1,proposed_starting_coverage_weight=1.)
        second = dict(account='linear',eligible_activities=1,proposed_starting_coverage_weight=1.)
        self.assertIs(choose_account_estimate([first,second]),second)
        self.assertIs(choose_account_estimate([second,first]),second)

    def test_fraction_rounding_uses_raw_ratio_including_thirds(self):
        for rises, total, label, weight in [(1, 4, '1/4', .25), (1, 3, '1/3', 1/3),
                                            (2, 3, '2/3', 2/3), (1, 100, '1/5', .2),
                                            (1, 1, '1', 1.)]:
            with self.subTest(fraction=label):
                estimate = dict(rising_activities=rises, eligible_activities=total,
                                frequency_weight_estimate=rises/total,
                                proposed_starting_coverage_weight=weight, weight_fraction=label)
                self.assertEqual(validate_fraction_estimate(estimate), label)

    def test_exact_midpoint_rounds_up(self):
        estimate = dict(rising_activities=9, eligible_activities=40,
                        frequency_weight_estimate=9/40,
                        proposed_starting_coverage_weight=.25, weight_fraction='1/4')
        self.assertEqual(validate_fraction_estimate(estimate), '1/4')

    def test_rejects_fraction_from_previously_rounded_score(self):
        # 7/19 is nearer 2/5. The old 0.05-rounded value .35 is nearer 1/3.
        estimate = dict(rising_activities=7, eligible_activities=19,
                        frequency_weight_estimate=7/19,
                        proposed_starting_coverage_weight=1/3, weight_fraction='1/3')
        with self.assertRaisesRegex(AssertionError, 'nearest raw K/N'):
            validate_fraction_estimate(estimate)

    def test_superseded_exact_request_is_never_overwritten(self):
        with TemporaryDirectory() as directory:
            folder = Path(directory)
            (folder/'superseded.json').write_text('{}')
            request = folder/'request.json'
            request.write_text('{"preserve": true}')
            with self.assertRaisesRegex(ValueError, 'superseded'):
                prepare(folder, folder, folder)
            self.assertEqual(request.read_text(), '{"preserve": true}')

    def test_lower_explicit_edge_replaces_inferred_coverage_and_propagates(self):
        existing = {('A', 'B'): .8, ('B', 'C'): .75, ('C', 'D'): .5}
        audit = coverage_audit(existing, {('A', 'C'): .25})
        self.assertEqual(audit['added_direct_edges_overriding_higher_inference'], 1)
        self.assertEqual(audit['actual_effective_coverage_decreases'], 2)
        direct = audit['prepared_pairs'][0]
        self.assertAlmostEqual(direct['previous_effective_coverage'], .6)
        self.assertEqual(direct['prepared_effective_coverage'], .25)
        downstream = next(row for row in audit['decreased_pairs'] if row['target'] == 'D')
        self.assertAlmostEqual(downstream['previous_effective_coverage'], .3)
        self.assertEqual(downstream['prepared_effective_coverage'], .125)

    def test_override_within_new_graph_is_not_reported_as_prior_reduction(self):
        audit = coverage_audit({}, {('A', 'B'): .8, ('B', 'C'): .75, ('A', 'C'): .25})
        self.assertEqual(audit['added_direct_edges_overriding_higher_inference'], 1)
        self.assertEqual(audit['actual_effective_coverage_decreases'], 0)

    def test_zero_explicit_edge_also_overrides(self):
        effective, _ = graph_coverage({('A', 'B'): 1., ('B', 'C'): 1., ('A', 'C'): 0.})
        self.assertNotIn(('A', 'C'), effective)
        self.assertEqual(effective['B', 'C'], 1.)

    def test_coverage_audit_rejects_cycles_and_existing_edge_replacement(self):
        with self.assertRaisesRegex(ValueError, 'cycle'):
            coverage_audit({('A', 'B'): 1.}, {('B', 'A'): .5})
        with self.assertRaisesRegex(AssertionError, 'preserved'):
            coverage_audit({('A', 'B'): 1.}, {('A', 'B'): .5})


if __name__=='__main__':
    unittest.main()
