from copy import deepcopy
import unittest

from scripts.activity.evidence import capture_gaps, finalize_answers, merge_question


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
                   'submissions': [{'outcome': 'observe_to_confirm', 'responses': [{'key': 'x', 'value': '2'}]}]}
        field = finalize_answers(self.question, [attempt], {'answers': []})['answer_fields'][0]
        self.assertEqual((field['correct_value'], field['evidence']['grade']), ('2', 'correct'))
        self.assertEqual(field['evidence']['source_file'], '/grade.html')

    def test_failed_or_unverified_entry_cannot_be_confirmed_by_later_grade(self):
        for outcome in ('entry_failed', 'not_submitted', 'unknown', None):
            attempt = {'key': 'live', 'feedback': {'grade': 'Correct'},
                       'submissions': [{'outcome': outcome, 'responses': [{'key': 'x', 'value': '8'}]}]}
            field = finalize_answers(self.question, [attempt], {'answers': []})['answer_fields'][0]
            self.assertNotIn('correct_value', field)

    def test_unknown_outcome_can_bind_observed_source_selected_value(self):
        self.question['fields'][0]['source_selected'] = {'type': 'math', 'value': '2'}
        attempt = {'key': 'live', 'feedback': {'grade': 'Correct'},
                   'submissions': [{'outcome': 'unknown', 'responses': [{'key': 'x', 'value': '2'}]}]}
        field = finalize_answers(self.question, [attempt], {'answers': []})['answer_fields'][0]
        self.assertEqual(field['correct_value'], '2')

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

    def test_example_missing_solution_and_tutorial_missing_content_need_source_recovery(self):
        content = {'kind': 'lesson', 'questions': [],
            'canonical_examples': [{'math_academy_id': 'e-3', 'problem': 'Example', 'worked_solution': '',
                                    'errors': ['MathJax formula has no assistive MathML']}],
            'tutorials': [{'math_academy_id': 7, 'title': 'Read this', 'content': ''}],
            'lesson_definition': {'complete': True, 'steps': [
                {'type': 'example', 'content_id': 3}, {'type': 'tutorial', 'content_id': 7}]}}
        gaps = capture_gaps(content)
        example = next(g for g in gaps if g.get('record_kind') == 'canonical_examples')
        tutorial = next(g for g in gaps if g.get('record_kind') == 'tutorials')
        self.assertIn('worked_solution', example['missing'])
        self.assertIn('extraction_errors', example['missing'])
        self.assertNotIn('answer_fields', example['missing'])
        self.assertIn('content', tutorial['missing'])

    def test_incomplete_fields_assets_and_missing_declared_lesson_steps_are_gaps(self):
        question = deepcopy(self.question)
        question.update(answer_fields_complete=False,
                        assets=[{'path': '/original.png', 'sha256': '123', 'render_unavailable': 'not drawn'}])
        question['fields'][0].update(type='select', choices=[], choices_complete=False)
        gaps = capture_gaps({'kind': 'lesson', 'questions': [question],
            'lesson_definition': {'complete': False, 'steps': [{'type': 'example', 'content_id': 9}]}})
        missing = {m for g in gaps for m in g['missing']}
        self.assertTrue({'answer_fields_complete', 'answer_choices', 'asset_rendering',
                         'lesson_definition_complete', 'lesson_step_content'} <= missing)

    def test_final_unavailable_finding_preserves_the_limitation_and_resolution(self):
        question = deepcopy(self.question)
        question['worked_solution'] = ''
        gaps = capture_gaps({'questions': [question], 'judgments': [{'question_id': 'q-1',
            'record_kind': 'questions', 'final': True, 'status': 'unavailable', 'reasoning': 'Source was removed.'}]})
        self.assertEqual(gaps[0]['missing'], ['worked_solution'])
        self.assertTrue(gaps[0]['final'])
        self.assertEqual(gaps[0]['reason'], 'Source was removed.')

    def test_conflicting_duplicate_source_id_is_not_silently_complete(self):
        changed = {**self.question, 'problem': 'Different source problem'}
        gaps = capture_gaps({'questions': [self.question, changed]})
        self.assertIn('source_identity_conflict', gaps[0]['missing'])

    def test_complete_worked_example_requires_no_interactive_answer_fields(self):
        example = {'math_academy_id': 'e-1', 'problem': 'One plus one?', 'worked_solution': 'The answer is 2.'}
        self.assertEqual(capture_gaps({'canonical_examples': [example]}), [])


if __name__ == '__main__':
    unittest.main()
