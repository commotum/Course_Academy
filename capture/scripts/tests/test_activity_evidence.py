from copy import deepcopy
import unittest

from scripts.activity.evidence import finalize_answers, merge_question


class Evidence(unittest.TestCase):
    def setUp(self):
        self.question = {'math_academy_id': 'q-1', 'problem': 'One plus one?', 'worked_solution': 'The answer is 2.',
                         'html_path': '/source.html', 'fields': [{'key': 'x', 'type': 'blank'}]}

    def test_guess_is_never_promoted(self):
        question = deepcopy(self.question)
        question['fields'][0]['correct_value'] = '8'
        result = finalize_answers(question, [], {'answers': [{'key': 'x', 'correct_value': '2', 'ma_basis': 'none'}]})
        self.assertNotIn('correct_value', result['answer_fields'][0])

    def test_accepted_submission_does_not_prove_correctness(self):
        attempt = {'accepted': True, 'submissions': [{'responses': [{'key': 'x', 'value': '8'}]}]}
        result = finalize_answers(self.question, [attempt], {'answers': []})
        self.assertNotIn('correct_value', result['answer_fields'][0])

    def test_correct_grade_confirms_actual_response(self):
        attempt = {'key': 'live', 'feedback': {'grade': 'Correct', 'html_path': '/grade.html'},
                   'submissions': [{'responses': [{'key': 'x', 'value': '2'}]}]}
        field = finalize_answers(self.question, [attempt], {'answers': []})['answer_fields'][0]
        self.assertEqual((field['correct_value'], field['evidence']['grade']), ('2', 'correct'))
        self.assertEqual(field['evidence']['source_file'], '/grade.html')

    def test_final_source_error_preserves_ma_answer_and_agent_judgment_separately(self):
        question = deepcopy(self.question)
        question['worked_solution'] = 'The answer is 3.'
        judgment = {'status': 'source_error', 'answers': [{'key': 'x', 'correct_value': '2', 'ma_value': '3',
            'ma_basis': 'worked_solution', 'ma_evidence': 'The answer is 3.', 'disagrees': True, 'value_type': 'math'}]}
        result = finalize_answers(question, [], judgment)
        self.assertEqual(result['answer_fields'][0]['correct_value'], '3')
        self.assertEqual(judgment['answers'][0]['correct_value'], '2')

    def test_invented_solution_quote_cannot_supply_answer(self):
        judgment = {'answers': [{'key': 'x', 'ma_value': '3', 'ma_basis': 'worked_solution', 'ma_evidence': 'Answer: 3'}]}
        field = finalize_answers(self.question, [], judgment)['answer_fields'][0]
        self.assertNotIn('correct_value', field)

    def test_missing_history_fields_do_not_erase_live_choices(self):
        before = {'fields': [{'key': 'x', 'choices': [{'value': '2'}, {'value': '3'}]}], 'worked_solution': 'answer'}
        after = {'fields': [{'key': 'x', 'choices': []}], 'difficulty': 'easy', 'worked_solution': ''}
        merged = merge_question(before, after)
        self.assertEqual(len(merged['fields'][0]['choices']), 2)
        self.assertEqual(merged['worked_solution'], 'answer')

    def test_direct_parser_source_evidence_alias_is_preserved(self):
        self.question['fields'][0].update(correct_value='2', correct_evidence={'kind': 'ma_answer', 'value': '2', 'source_file': '/source.html'})
        field = finalize_answers(self.question, [], {'answers': []})['answer_fields'][0]
        self.assertEqual(field['evidence']['kind'], 'ma_answer')


if __name__ == '__main__':
    unittest.main()
