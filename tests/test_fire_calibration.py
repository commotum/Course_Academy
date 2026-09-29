"""Calibration checks independent of task mastery and repetition scheduling."""

from dataclasses import asdict
import json
import math
import unittest

from engine.fire.calibration import AccuracyEstimate, DifficultyEstimate


class AccuracyEstimateTests(unittest.TestCase):
    def test_equal_channel_weight_does_not_follow_answer_volume(self):
        estimate = AccuracyEstimate()
        estimate.update((True,) * 100, assessment=False, alpha=1)
        estimate.update((False,), assessment=True, alpha=1)
        self.assertEqual(estimate.accuracy, 0.5)
        self.assertEqual(estimate.practice_mass, 100)
        self.assertEqual(estimate.assessment_mass, 1)

    def test_unobserved_channel_keeps_prior(self):
        estimate = AccuracyEstimate()
        estimate.update((True,), assessment=False, alpha=1)
        self.assertEqual(estimate.assessment_accuracy, 0.8)
        self.assertEqual(estimate.accuracy, 0.9)

    def test_fractional_weight_matches_composed_evidence(self):
        whole = AccuracyEstimate()
        split = AccuracyEstimate()
        whole.update((False,), assessment=True, alpha=0.2)
        split.update((False,), assessment=True, alpha=0.2, weight=0.5)
        self.assertAlmostEqual(split.assessment_accuracy, 0.8 * math.sqrt(0.8))
        split.update((False,), assessment=True, alpha=0.2, weight=0.5)
        self.assertAlmostEqual(split.assessment_accuracy, whole.assessment_accuracy)
        self.assertEqual(split.assessment_mass, whole.assessment_mass)
        self.assertEqual(split.practice_accuracy, 0.8)

    def test_ordered_mixed_answers_include_failure_evidence(self):
        estimate = AccuracyEstimate()
        returned = estimate.update((True, False), assessment=False, alpha=0.2)
        self.assertIs(returned, estimate)
        self.assertAlmostEqual(estimate.practice_accuracy, 0.672)
        self.assertEqual(estimate.practice_mass, 2)

    def test_immediate_answers_match_ordered_batch_calibration(self):
        answers = (False, True, True, False)
        stream, batch = AccuracyEstimate(), AccuracyEstimate()
        for answer in answers:
            stream.update((answer,), assessment=True, weight=.25)
        batch.update(answers, assessment=True, weight=.25)
        self.assertEqual(stream, batch)
        self.assertEqual(stream.assessment_mass, 1)

    def test_empty_and_zero_weight_are_no_ops(self):
        estimate = AccuracyEstimate()
        initial = asdict(estimate)
        estimate.update((), assessment=True)
        estimate.update((False,), assessment=False, weight=0)
        self.assertEqual(asdict(estimate), initial)

    def test_invalid_constructor_values(self):
        for arguments in ({'assessment_accuracy': -0.1}, {'practice_accuracy': 1.1},
                          {'assessment_mass': -1}, {'practice_mass': math.inf},
                          {'assessment_accuracy': True}, {'practice_accuracy': math.nan},
                          {'assessment_mass': 10 ** 1000}):
            with self.subTest(arguments=arguments), self.assertRaises(ValueError):
                AccuracyEstimate(**arguments)

    def test_invalid_update_is_atomic(self):
        estimate = AccuracyEstimate()
        initial = asdict(estimate)
        cases = [((True, None), {}), ((True, 1), {}), ((True,), {'assessment': None}),
                 ((False,), {'alpha': 0}), ((False,), {'alpha': 1.1}),
                 ((False,), {'alpha': math.nan}), ((False,), {'weight': -1}),
                 ((False,), {'weight': math.inf}), ((False,), {'weight': True}),
                 ((True, False), {'weight': 1e308})]
        for outcomes, options in cases:
            with self.subTest(options=options, outcomes=outcomes), self.assertRaises(ValueError):
                estimate.update(outcomes, **{'assessment': True, **options})
            self.assertEqual(asdict(estimate), initial)

    def test_json_round_trip_preserves_fields_and_future_update(self):
        estimate = AccuracyEstimate()
        estimate.update((False, True), assessment=True, weight=0.25)
        estimate.update((True, False, True), assessment=False)
        restored = AccuracyEstimate(**json.loads(json.dumps(asdict(estimate), allow_nan=False)))
        self.assertEqual(restored, estimate)
        for value in (estimate, restored):
            value.update((True,), assessment=True, weight=0.5)
        self.assertEqual(restored, estimate)


class DifficultyEstimateTests(unittest.TestCase):
    def test_only_serious_assessments_contribute(self):
        estimate = DifficultyEstimate(prior_accuracy=0.7)
        self.assertEqual(estimate.accuracy, 0.7)
        estimate.update((True,) * 20, serious=True, assessment=False)
        estimate.update((False,) * 20, serious=False, assessment=True)
        self.assertEqual(estimate.assessment_total, 0)
        returned = estimate.update((True, True, False), serious=True, assessment=True)
        self.assertIs(returned, estimate)
        self.assertEqual(estimate.assessment_correct, 2)
        self.assertEqual(estimate.assessment_total, 3)
        self.assertAlmostEqual(estimate.accuracy, 2 / 3)

    def test_unknown_classification_cannot_be_silently_inferred(self):
        estimate = DifficultyEstimate()
        for options in ({'serious': None, 'assessment': True},
                        {'serious': True, 'assessment': None},
                        {'serious': True, 'assessment': 1}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                estimate.update((True,), **options)
        self.assertEqual(estimate.assessment_total, 0)

    def test_invalid_counts_and_invalid_batch(self):
        for options in ({'assessment_correct': 2, 'assessment_total': 1},
                        {'assessment_total': -1}, {'assessment_correct': math.nan},
                        {'prior_accuracy': 1.1}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                DifficultyEstimate(**options)
        estimate = DifficultyEstimate(1, 2)
        with self.assertRaises(ValueError):
            estimate.update((True, None), serious=True, assessment=True)
        self.assertEqual(asdict(estimate), asdict(DifficultyEstimate(1, 2)))

    def test_json_round_trip(self):
        estimate = DifficultyEstimate()
        estimate.update((True, False), serious=True, assessment=True)
        restored = DifficultyEstimate(**json.loads(json.dumps(asdict(estimate), allow_nan=False)))
        self.assertEqual(restored, estimate)
        self.assertEqual(restored.accuracy, 0.5)


if __name__ == '__main__':
    unittest.main()
