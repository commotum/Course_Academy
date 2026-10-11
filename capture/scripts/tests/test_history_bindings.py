"""History positions must not attach another question's identity or grade."""
from copy import deepcopy
import unittest

from scripts.activity.capture import ActivityCapture
from scripts.activity.evidence import finalize_answers


def question(problem='One plus one?', identity=None, **extra):
    return {'math_academy_id': identity, 'problem': problem,
            'fields': [{'key': 'answer', 'type': 'blank'}], **extra}


def presentation(q, position=0, value='2'):
    return {'key': 'live-' + str(position), 'question': q, 'observed_position': position,
            'submissions': [{'outcome': 'observe_to_confirm',
                             'responses': [{'key': 'answer', 'value': value}]}]}


class HistoryBindingTests(unittest.TestCase):
    def capture(self, records):
        capture = ActivityCapture.__new__(ActivityCapture)
        capture.activity = {'task_id': '1', 'kind': 'diagnostic'}
        capture.state = {'steps': [], 'presentations': {r['key']: r for r in records}}
        capture._save = lambda: None
        return capture

    def test_position_does_not_assign_different_question_id_or_correct_grade(self):
        record = presentation(question())
        capture = self.capture([record])
        history = question('Three plus three?', 'q-9', sequence_position=1,
                           worked_solution='The answer is 6.', grade='Correct')
        content = capture._merge_history({'questions': [history]})
        self.assertIsNone(record['question']['math_academy_id'])
        self.assertEqual(len(content['questions']), 2)
        saved = next(q for q in content['questions'] if q.get('math_academy_id') == 'q-9')
        result = finalize_answers(saved, capture._question_presentations(saved), {'answers': []})
        self.assertNotIn('correct_value', result['answer_fields'][0])
        self.assertTrue(content['source_limitations'])

    def test_matching_position_with_shuffled_choices_gets_source_id(self):
        live = question('Choose two.')
        live['fields'] = [{'key': 'answer', 'type': 'radio', 'choices': [
            {'option': 'a', 'type': 'text', 'value': '2'}, {'option': 'b', 'type': 'text', 'value': '3'}]}]
        history = deepcopy(live)
        history.update(math_academy_id='q-2', sequence_position=1, grade='Correct')
        history['fields'][0]['choices'].reverse()
        record = presentation(live)
        capture = self.capture([record])
        content = capture._merge_history({'questions': [history]})
        self.assertEqual(record['question']['math_academy_id'], 'q-2')
        self.assertEqual(len(content['questions']), 1)
        self.assertEqual(record['feedback']['grade'], 'Correct')

    def test_permanent_id_conflict_preserves_both_originals_without_grade_transfer(self):
        record = presentation(question(identity='q-1'))
        capture = self.capture([record])
        history = question('Three plus three?', 'q-1', sequence_position=1, grade='Correct')
        content = capture._merge_history({'questions': [history]})
        self.assertEqual(len(content['questions']), 2)
        live = next(q for q in content['questions'] if q.get('observed_math_academy_id'))
        self.assertEqual(live['observed_math_academy_id'], 'q-1')
        self.assertEqual(live['problem'], 'One plus one?')
        self.assertEqual(capture._question_presentations(history), [])
        self.assertEqual(capture._question_presentations(live), [record])

    def test_explicit_fieldless_history_merges_text_but_cannot_confirm_submission(self):
        record = presentation(question(identity='q-1'))
        capture = self.capture([record])
        history = {'math_academy_id': 'q-1', 'problem': 'One plus one?', 'fields': [],
                   'worked_solution': 'The answer is 2.', 'extraction_parts': ['problem', 'solution'],
                   'sequence_position': 1, 'grade': 'Correct'}
        content = capture._merge_history({'questions': [history]})
        self.assertEqual(len(content['questions']), 1)
        self.assertEqual(content['questions'][0]['fields'], record['question']['fields'])
        self.assertEqual(content['source_limitations'], [])
        self.assertNotIn('feedback', record)
        result = finalize_answers(content['questions'][0], [record], {'answers': []})
        self.assertNotIn('correct_value', result['answer_fields'][0])

    def test_fieldless_history_still_requires_verified_id_scope_and_identical_prompt(self):
        for change in ({'math_academy_id': None}, {'extraction_parts': ['solution']},
                       {'problem': 'Three plus three?'}, {'extraction_parts': ['problem', 'solution', 'fields']},
                       {'fields': [{'key': 'different', 'type': 'blank'}]}):
            with self.subTest(change=change):
                history = {'math_academy_id': 'q-1', 'problem': 'One plus one?', 'fields': [],
                           'worked_solution': 'The answer is 2.', 'extraction_parts': ['problem', 'solution'], **change}
                self.assertFalse(ActivityCapture._history_content_matches(question(identity='q-1'), history))

    def test_deduplicated_history_grade_is_not_assigned_to_first_repeat(self):
        for known in (None, 'q-1'):
            first = presentation(question(identity=known), value='9')
            second = presentation(question(identity=known), position=1, value='2')
            capture = self.capture([first, second])
            history = question(identity='q-1', sequence_position=1, grade='Correct')
            capture._merge_history({'questions': [history]})
            self.assertNotIn('feedback', first)
            finalized = finalize_answers(history, capture._question_presentations(history), {'answers': []})
            self.assertNotIn('correct_value', finalized['answer_fields'][0])

    def test_prior_misbound_feedback_is_retained_but_not_used_for_confirmation(self):
        record = presentation(question(identity='q-1'), value='9')
        record['feedback'] = question('Three plus three?', 'q-1', grade='Correct')
        capture = self.capture([record])
        content = capture._merge_history({'questions': [record['feedback']]})
        self.assertEqual(record['feedback'], {})
        self.assertEqual(record['unmatched_history_feedback']['grade'], 'Correct')
        live = next(q for q in content['questions'] if q.get('observed_math_academy_id'))
        result = finalize_answers(live, capture._question_presentations(live), {'answers': []})
        self.assertNotIn('correct_value', result['answer_fields'][0])


if __name__ == '__main__':
    unittest.main()
