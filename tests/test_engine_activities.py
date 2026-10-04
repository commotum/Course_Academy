"""Activity transitions and observed XP examples, not assertions of MA parity."""
from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path
import unittest

from engine.activities import (
    DiagnosticBalance, assessment_xp_candidate, evaluate_kp_prefix,
    evaluate_review_prefix, lesson_xp_candidate, multistep_xp_candidate,
    review_xp_candidate, round_half_up, earned_xp,
)


class PracticeTests(unittest.TestCase):
    def test_lesson_advances_after_recovery_and_fails_at_five(self):
        self.assertEqual(evaluate_kp_prefix([]).status, 'continue')
        self.assertIsNone(evaluate_kp_prefix([True]).passed)
        self.assertTrue(evaluate_kp_prefix([True, False, True, True]).passed)
        final = evaluate_kp_prefix([True, False, True, False, True])
        self.assertTrue(final.complete)
        self.assertFalse(final.passed)
        self.assertEqual((final.attempted, final.correct, final.streak), (5, 3, 1))

    def test_published_review_order_counterexample(self):
        self.assertTrue(evaluate_review_prefix([False, False, True, True, True]).passed)
        self.assertFalse(evaluate_review_prefix([True, True, False, False, True]).passed)
        self.assertTrue(evaluate_review_prefix([True, True, True]).passed)

    def test_skip_consumes_attempt_and_breaks_streak(self):
        state = evaluate_kp_prefix([True, None, True])
        self.assertEqual((state.status, state.attempted, state.correct, state.streak),
                         ('continue', 3, 2, 1))
        self.assertFalse(evaluate_review_prefix([True, True, None, True, True]).passed)

    def test_no_answers_after_terminal_prefix_and_no_bool_coercion(self):
        for evaluator, outcomes in [
            (evaluate_kp_prefix, [True, True, False]),
            (evaluate_review_prefix, [True] * 4),
            (evaluate_kp_prefix, [False] * 6),
        ]:
            with self.assertRaises(ValueError): evaluator(outcomes)
        for value in [0, 1, 'correct', [], {}, 0.0]:
            with self.assertRaises(ValueError): evaluate_kp_prefix([value])


class XpTests(unittest.TestCase):
    def test_rounding_matches_analysis_including_ties(self):
        for value, expected in [(Fraction(21, 2), 11), (Decimal('2.5'), 3),
                                (2.5, 3), (-2.5, -2), (Fraction(-8, 3), -3)]:
            self.assertEqual(round_half_up(value), expected)

    def test_assessment_observed_awards(self):
        # All twelve inspected assessments retained in the analysis.
        for base, correct, count, award in [
            (15, 7, 10, 10), (15, 5, 8, 8), (15, 7, 9, 12),
            (15, 10, 11, 15), (13, 7, 7, 16), (15, 8, 8, 18),
            (13, 7, 8, 13), (11, 2, 8, 0), (15, 8, 12, 9),
            (12, 11, 11, 14), (11, 6, 9, 6), (12, 4, 9, 2),
        ]:
            self.assertEqual(assessment_xp_candidate(base, [True] * correct +
                                                    [False] * (count - correct)), award)
        self.assertEqual(assessment_xp_candidate(12, [True] * 4 + [None] * 5), 2)

    def test_multistep_observed_awards(self):
        for base, correct, count, award in [
            (10, 7, 7, 13), (10, 5, 7, 6), (15, 8, 10, 12),
            (7, 5, 9, 2), (14, 7, 9, 11), (7, 7, 8, 7),
        ]:
            self.assertEqual(multistep_xp_candidate(base, [True] * correct +
                                                   [False] * (count - correct)), award)
        self.assertEqual(multistep_xp_candidate(7, [None]), -1)

    def test_perfect_bonus_and_explicit_partial_awards(self):
        self.assertEqual(lesson_xp_candidate(16, [True] * 8), 20)
        self.assertEqual(review_xp_candidate(7, [True] * 3), 9)
        for scorer in [lesson_xp_candidate, review_xp_candidate]:
            for outcomes in [[True, False], [True, None]]:
                self.assertEqual(scorer(7, outcomes), 3 if scorer is lesson_xp_candidate else 0)
                self.assertEqual(scorer(7, outcomes, award=0), 0)
                self.assertEqual(scorer(7, outcomes, award=-1), -1)
            with self.assertRaises(ValueError): scorer(7, [True], award=True)

    def test_accepted_boundaries_and_review_ending(self):
        self.assertEqual(earned_xp('lesson', 20, 1, 4), -1)
        self.assertEqual(earned_xp('lesson', 20, 1, 2), 9)
        self.assertEqual(earned_xp('lesson', 20, 3, 5), 12)
        self.assertEqual(earned_xp('lesson', 20, 9, 10), 20)
        self.assertEqual(earned_xp('lesson', 20, 10, 10), 25)
        self.assertEqual(earned_xp('assessment', 15, 0, 9), -1)
        self.assertEqual(earned_xp('assessment', 15, 1, 5), 0)
        self.assertEqual(earned_xp('review', 6, 2, 5, final_correct=False), -1)
        self.assertEqual(earned_xp('review', 6, 3, 5, final_correct=False), 0)
        self.assertEqual(earned_xp('review', 6, 3, 5, final_correct=True), 4)
        self.assertEqual(earned_xp('review', 6, 2, 3), 6)
        with self.assertRaisesRegex(ValueError, 'final_correct'):
            earned_xp('review', 6, 3, 5)
        # Final ties use half-up rounding, including arbitrary precision bases.
        self.assertEqual(earned_xp('lesson', 10, 1, 2), 5)
        self.assertEqual(earned_xp('lesson', 10**30, 1, 2), 45 * 10**28)

    def test_all_frozen_observed_awards(self):
        path = Path(__file__).resolve().parents[1] / 'reference/mathacademy-earned-xp/observations.json'
        rows = json.loads(path.read_text())['rows']
        self.assertEqual(len(rows), 168)
        calculators = {'lesson': lesson_xp_candidate, 'review': review_xp_candidate,
                       'assessment': assessment_xp_candidate, 'multistep': multistep_xp_candidate}
        for row in rows:
            with self.subTest(task=row['task_id']):
                self.assertEqual(calculators[row['type']](row['base'], [q['correct'] for q in row['questions']]),
                                 row['earned'])

    def test_invalid_xp_inputs(self):
        for scorer in [assessment_xp_candidate, multistep_xp_candidate,
                       lesson_xp_candidate, review_xp_candidate]:
            for base in [-1, float('nan'), float('inf'), True, '15']:
                with self.assertRaises(ValueError): scorer(base, [True])
            with self.assertRaises(ValueError): scorer(15, [])
            with self.assertRaises(ValueError): scorer(15, [1])


class DiagnosticTests(unittest.TestCase):
    def make_balance(self, skip_policy='negative'):
        return DiagnosticBalance({'advanced': ['left', 'right'],
                                  'left': ['basic'], 'right': ['basic'],
                                  'unrelated': []}, skip_policy=skip_policy)

    def test_positive_downward_negative_upward_diamond_once(self):
        balance = self.make_balance()
        self.assertEqual(balance.apply('advanced', True),
                         dict.fromkeys(['advanced', 'basic', 'left', 'right'], 1.0))
        self.assertEqual(balance.snapshot()['basic'], 1)
        self.assertEqual(balance.apply('basic', False),
                         dict.fromkeys(['advanced', 'basic', 'left', 'right'], -1.0))
        self.assertEqual(balance.positive_repetitions(), {})
        self.assertEqual(balance.snapshot()['unrelated'], 0)

    def test_slow_correct_reduces_but_does_not_reverse_credit(self):
        balance = self.make_balance()
        balance.apply('advanced', True, weight=.25)
        balance.apply('right', True)
        self.assertEqual(balance.positive_repetitions(),
                         {'advanced': .25, 'basic': 1.25, 'left': .25, 'right': 1.25})
        balance.apply('left', False)
        self.assertEqual(balance.snapshot()['advanced'], -.75)
        self.assertNotIn('advanced', balance.positive_repetitions())

    def test_skip_policy_required_and_explicit(self):
        with self.assertRaises(TypeError): DiagnosticBalance({'A': []})
        with self.assertRaises(ValueError): DiagnosticBalance({'A': []}, skip_policy='guess')
        negative = self.make_balance('negative')
        negative.apply('left', None)
        self.assertEqual(negative.snapshot(),
                         {'advanced': -1, 'basic': 0, 'left': -1, 'right': 0, 'unrelated': 0})
        neutral = self.make_balance('neutral')
        self.assertEqual(neutral.apply('left', None), {})
        self.assertTrue(all(value == 0 for value in neutral.snapshot().values()))

    def test_invalid_graphs(self):
        for graph in [{'A': ['A']}, {'A': ['B'], 'B': ['A']},
                      {'A': ['B', 'B']}, {'A': 'B'}, {'A': None}, {'': []}, {'A': [1]}]:
            with self.assertRaises(ValueError): DiagnosticBalance(graph, skip_policy='neutral')

    def test_invalid_evidence_is_atomic_and_snapshots_are_detached(self):
        balance = self.make_balance()
        balance.apply('basic', True)
        before = balance.snapshot()
        for topic, outcome, weight in [('unknown', True, 1), ('basic', 1, 1),
                                        ('basic', True, 0), ('basic', True, -1),
                                        ('basic', True, 1.1), ('basic', True, float('nan')),
                                        ('basic', True, Decimal('1e-400')),
                                        ('basic', False, .5), ('basic', None, .5)]:
            with self.assertRaises(ValueError): balance.apply(topic, outcome, weight=weight)
            self.assertEqual(balance.snapshot(), before)
        detached = balance.snapshot()
        detached['basic'] = 99
        self.assertEqual(balance.snapshot()['basic'], 1)


if __name__ == '__main__':
    unittest.main()
