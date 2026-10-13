import unittest
import json
from copy import deepcopy
from pathlib import Path

from scripts.activity.policy import AnswerPolicy, prerequisite_distances, responses_for, supports_intentional_error


class Draws:
    def __init__(self, draws):
        self.draws = iter(draws)
        self.bounds = []

    def random(self):
        return next(self.draws)

    def uniform(self, low, high):
        self.bounds.append((low, high))
        return (low + high) / 2


class Policies(unittest.TestCase):
    def activity(self, kind, **details):
        return {'kind': kind, 'details': details}

    def test_lesson_patterns_are_per_kp_and_correct_after_five(self):
        state = {}
        policy = AnswerPolicy(self.activity('lesson'), state, rng=Draws([.1, .9]))
        first = ''.join(policy.decide(str(i), {'kp_id': 'a'})['planned'] for i in range(7))
        second = ''.join(policy.decide('b' + str(i), {'kp_id': 'b'})['planned'] for i in range(5))
        self.assertEqual((first, second), ('CWCWCCC', 'WCWCC'))

    def test_review_repeats_across_kps_and_resume_does_not_advance(self):
        state = {}
        policy = AnswerPolicy(self.activity('review'), state, rng=Draws([.9]))
        got = ''.join(policy.decide(str(i), {'kp_id': str(i)})['planned'] for i in range(8))
        self.assertEqual(got, 'WCWCCWCW')
        restored = AnswerPolicy(self.activity('review'), state, rng=Draws([]))
        self.assertEqual(restored.decide('0', {})['planned'], 'W')
        self.assertEqual(state['counts']['review'], 8)

    def test_all_correct_retake_and_multistep(self):
        for kind, details in [('lesson', {'force_correct': True}), ('review', {'force_correct': True}), ('multistep', {})]:
            policy = AnswerPolicy(self.activity(kind, **details), {}, rng=Draws([]))
            self.assertEqual(policy.decide('q', {})['planned'], 'C')

    def test_assessment_probability_boundary_is_independent_of_retake(self):
        policy = AnswerPolicy(self.activity('assessment', force_correct=True), {}, rng=Draws([.87169, .8717]))
        self.assertEqual(policy.decide('a', {})['planned'], 'C')
        self.assertEqual(policy.decide('b', {})['planned'], 'W')

    def test_graph_shortest_distance_direction_cycles_and_course_membership(self):
        graph = {'1': ['2'], '2': ['3'], '3': ['4'], '4': ['5'], '5': ['4'], '8': ['2', '4'], '9': ['10']}
        distances = prerequisite_distances(['4', '5'], graph)
        self.assertEqual(distances, {'4': 0, '5': 0, '3': 1, '8': 1, '2': 2, '1': 3})

    def test_diagnostic_wait_ranges_and_immediate_dont_know(self):
        context = {'course_topics': ['4'], 'graph': {'1': ['2'], '2': ['3'], '3': ['4']}}
        draws = Draws([.1, .8])
        state = {}
        policy = AnswerPolicy(self.activity('diagnostic'), state, context, draws, clock=lambda: 100)
        correct = policy.decide('course1', {'topic_id': '4'})
        dont = policy.decide('course2', {'topic_id': '4'})
        self.assertEqual((correct['delay_seconds'], correct['submit_at']), (315, 415))
        self.assertEqual((dont['action'], dont['delay_seconds']), ('dont_know', 0))
        for topic, delay in [('3', 105), ('2', 75), ('1', 45)]:
            self.assertEqual(policy.decide(topic, {'topic_id': topic})['delay_seconds'], delay)
        self.assertEqual(policy.decide('unknown', {'topic_id': '999'})['action'], 'dont_know')
        restored = AnswerPolicy(self.activity('diagnostic'), state, context, Draws([]), clock=lambda: 200)
        self.assertEqual(restored.decide('course1', {'topic_id': '4'})['submit_at'], 415)

    def test_wrong_answer_changes_one_field_and_rebinds_shuffled_choices(self):
        question = {'fields': [
            {'key': 'one', 'type': 'radio', 'choices': [{'option': 'b', 'value': 'yes'}, {'option': 'a', 'value': 'no'}]},
            {'key': 'two', 'type': 'blank'}]}
        solution = {'answers': [{'key': 'one', 'correct_value': 'yes', 'correct_option': 'a'},
                                {'key': 'two', 'correct_value': '2', 'wrong_value': '3'}]}
        correct = responses_for(question, solution, {'planned': 'C', 'intended': 'C'})
        self.assertEqual(correct[0]['option'], 'b')
        wrong = responses_for(question, solution, {'planned': 'W', 'intended': 'W'})
        self.assertEqual([r['value'] for r in wrong], ['no', '2'])

    def test_missing_wrong_answer_overrides_sequence_and_keeps_original_intent(self):
        decision = {'planned': 'W', 'intended': 'W'}
        responses_for({'fields': [{'key': 'x', 'type': 'blank'}]},
                      {'answers': [{'key': 'x', 'correct_value': '2'}]}, decision)
        self.assertEqual((decision['planned'], decision['intended']), ('W', 'C'))
        self.assertIn('deviation_reason', decision)

    def test_late_field_fallback_rebuilds_earlier_intentional_error(self):
        decision = {'planned': 'W', 'intended': 'W'}
        question = {'fields': [{'key': 'a', 'type': 'blank'}, {'key': 'b', 'type': 'blank'}]}
        solution = {'answers': [{'key': 'a', 'correct_value': '2', 'wrong_value': '3'}]}
        responses = responses_for(question, solution, decision)
        self.assertEqual((decision['planned'], decision['intended']), ('W', 'C'))
        self.assertEqual([r['value'] for r in responses], ['2', '0'])

    def test_recorded_ml_questions_keep_wrong_policy_without_a_revealed_ma_key(self):
        cases = json.loads((Path(__file__).parent / 'fixtures/ml-missing-ma-key.json').read_text())
        for case in cases:
            with self.subTest(lesson=case['title']):
                question, solution = case['question'], case['solution']
                self.assertEqual(solution['status'], 'ambiguous')
                self.assertTrue(supports_intentional_error(question, solution))
                decision = {'planned': 'W', 'intended': 'W'}
                responses = responses_for(question, solution, decision)
                correct = {answer['key']: answer['correct_value'] for answer in solution['answers']}
                self.assertTrue(any(response['value'] != correct[response['key']] for response in responses))
                self.assertEqual(decision['intended'], 'W')

    def test_intentional_error_requires_complete_current_mathematical_answers(self):
        question = {'fields': [{'key': 'a', 'type': 'blank'}, {'key': 'b', 'type': 'blank'}]}
        solution = {'status': 'ambiguous', 'confidence': 1,
                    'answers': [{'key': 'a', 'correct_value': '2'}]}
        self.assertFalse(supports_intentional_error(question, solution))
        question['fields'][1]['source_result'] = 'Correct'
        self.assertTrue(supports_intentional_error(question, solution))
        question['fields'][0]['choices'] = [{'value': '3'}]
        self.assertFalse(supports_intentional_error(question, solution))

    def test_completed_fields_are_not_recorded_as_new_submissions(self):
        responses = responses_for({'fields': [{'key': 'a', 'source_result': 'Correct'}, {'key': 'b', 'disabled': True}]},
                                  {'answers': []}, {'planned': 'C', 'intended': 'C'})
        self.assertEqual(responses, [])

    def source_preferred_fixture(self):
        return json.loads((Path(__file__).parent / 'fixtures/q184176-source-preferred.json').read_text())

    def test_actual_proof_retries_exact_source_choice_instead_of_unchanged_first_option(self):
        fixture = self.source_preferred_fixture()
        original = deepcopy(fixture)
        responses = responses_for(fixture['question'], fixture['solution'],
                                  {'planned': 'C', 'intended': 'C'}, source_preferred=True)
        self.assertEqual([r['key'] for r in responses], ['field-3', 'field-4', 'field-5', 'field-6'])
        self.assertEqual((responses[0]['option'], responses[0]['value'], responses[0]['value_type']),
                         ('8', '2{a}^{2}+2a-1', 'math'))
        self.assertEqual([r['value'] for r in responses[1:]], ['an integer', 'an integer', '2b+1'])
        self.assertEqual(fixture, original)  # The original source/solver judgment is retained.

    def test_source_paraphrase_fallback_requires_unique_exact_typed_value_and_option(self):
        for change in ('not_exact', 'wrong_type', 'duplicate', 'wrong_option'):
            with self.subTest(change=change):
                fixture = self.source_preferred_fixture()
                answer = fixture['solution']['answers'][2]
                if change == 'not_exact': answer['correct_value'] = '2a^2+2a-1'
                elif change == 'wrong_type': answer['value_type'] = 'text'
                elif change == 'wrong_option': answer['correct_option'] = '0'
                else:
                    field = fixture['question']['fields'][2]
                    field['choices'].append({**field['choices'][8], 'option': '9'})
                response = responses_for(fixture['question'], fixture['solution'],
                    {'planned': 'C', 'intended': 'C'}, source_preferred=True)[0]
                self.assertEqual(response['option'], '0')

    def test_source_paraphrase_fallback_requires_explicit_non_disagreement(self):
        for flag in (None, True, 0):
            with self.subTest(flag=flag):
                fixture = self.source_preferred_fixture()
                answer = fixture['solution']['answers'][2]
                if flag is None: answer.pop('disagrees')
                else: answer['disagrees'] = flag
                response = responses_for(fixture['question'], fixture['solution'],
                    {'planned': 'C', 'intended': 'C'}, source_preferred=True)[0]
                self.assertEqual(response['option'], '0')

    def test_source_paraphrase_fallback_does_not_override_direct_keys_or_correct_grades(self):
        for basis in ('ma_answer', 'correct_grade', 'ma_correct_grade'):
            with self.subTest(basis=basis):
                fixture = self.source_preferred_fixture()
                fixture['solution']['answers'][2]['ma_basis'] = basis
                response = responses_for(fixture['question'], fixture['solution'],
                    {'planned': 'C', 'intended': 'C'}, source_preferred=True)[0]
                self.assertEqual(response['option'], '0')

    def test_literal_current_ma_choice_keeps_precedence_over_solver_correct_choice(self):
        fixture = self.source_preferred_fixture()
        answer = fixture['solution']['answers'][2]
        answer.update(ma_value='2(2{a}^{2}-a)', ma_basis='ma_answer', disagrees=True)
        response = responses_for(fixture['question'], fixture['solution'],
            {'planned': 'C', 'intended': 'C'}, source_preferred=True)[0]
        self.assertEqual(response['option'], '0')


if __name__ == '__main__':
    unittest.main()
