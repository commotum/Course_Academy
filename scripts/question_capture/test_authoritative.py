"""Source keys take precedence over mathematical predictions and local repairs."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from authoritative import prepare_authoritative_content


def choice(value, option='a', kind='text'):
    return {'type': kind, 'value': value, 'option': option}


def field(key='selection', kind='radio', values=('wrong', 'right')):
    return {'key': key, 'type': kind, 'choices_complete': kind != 'blank',
            'choices': [choice(v, chr(97+i)) for i, v in enumerate(values)] if kind != 'blank' else []}


class AuthoritativeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        self.raw = field()
        self.before = {'problem': 'Source problem', 'fields': [self.raw], 'errors': [], 'assets': []}
        self.record = {'before': self.before, 'after': {'worked_solution': 'Source explanation', 'fields': []},
            'actual_result': 'Incorrect', 'decision': {'answers': [
                {'key': 'selection', 'value_type': 'text', 'correct_value': 'right'}]}}
        self.content = {'task_type': 'review', 'topic_id': 1, 'questions': [
            {'math_academy_id': 'q-12', 'problem': 'Locally changed', 'worked_solution': 'Locally changed',
             'answer_fields': [{'key': 'selection', 'type': 'radio', 'choices': [choice('right')],
                                'correct_value': 'right', 'correct_origin': 'ma_revealed_solution'}]}],
            'canonical_examples': []}

    def tearDown(self):
        self.temp.cleanup()

    def prepare(self):
        return prepare_authoritative_content(self.content, self.directory,
            state={'questions': {'q-12': self.record}})

    def test_source_error_wins_and_solver_disagreement_is_flagged(self):
        self.raw['source_correct'] = {'type': 'text', 'value': 'wrong'}
        prepared, report = self.prepare()
        result = prepared['questions'][0]
        self.assertEqual(result['problem'], 'Source problem')
        self.assertEqual(result['worked_solution'], 'Source explanation')
        self.assertEqual(result['answer_fields'][0]['correct_value'], 'wrong')
        self.assertEqual([c['value'] for c in result['answer_fields'][0]['choices']], ['wrong', 'right'])
        self.assertTrue(any(d['reason'] == 'assistant_answer_differs_from_math_academy' for d in report['disagreements']))
        self.assertTrue(report['ready'])
        self.assertEqual(self.content['questions'][0]['problem'], 'Locally changed')

    def test_model_label_is_not_evidence(self):
        _, report = self.prepare()
        self.assertEqual(report['held_questions'][0]['reasons'], ['unconfirmed_correct_answer:selection'])

    def test_successful_grade_uses_actual_submission(self):
        self.record['actual_result'] = 'Correct'
        self.raw['submitted_value'] = 'wrong'
        prepared, report = self.prepare()
        self.assertTrue(report['ready'])
        self.assertEqual(prepared['questions'][0]['answer_fields'][0]['correct_value'], 'wrong')

    def test_duplicate_identical_source_choices_preserve_positions_and_prepare(self):
        for evidence in ('successful_grade', 'explicit_source'):
            with self.subTest(evidence=evidence):
                self.raw['choices'] = [choice('wrong', 'a'), choice('wrong', 'b'), choice('right', 'c')]
                self.raw.pop('source_correct', None)
                self.record['actual_result'] = 'Incorrect'
                if evidence == 'successful_grade':
                    self.raw['submitted_value'] = 'wrong'
                    self.record['actual_result'] = 'Correct'
                else:
                    self.raw['source_correct'] = {'type': 'text', 'value': 'wrong'}
                prepared, report = self.prepare()
                self.assertTrue(report['ready'])
                answer_field = prepared['questions'][0]['answer_fields'][0]
                self.assertEqual(answer_field['correct_value'], 'wrong')
                self.assertEqual([c['value'] for c in answer_field['choices']], ['wrong', 'wrong', 'right'])

    def test_exact_source_value_wins_over_equivalent_choice_serializations(self):
        self.raw['choices'] = [choice('1/2', 'a', 'math'), choice(r'\frac{1}{2}', 'b', 'math')]
        self.raw['source_correct'] = {'type': 'math', 'value': r'\frac{1}{2}'}
        prepared, report = self.prepare()
        self.assertTrue(report['ready'])
        self.assertEqual(prepared['questions'][0]['answer_fields'][0]['correct_value'], r'\frac{1}{2}')

    def test_failed_submission_does_not_supply_key(self):
        self.raw['submitted_value'] = 'wrong'
        prepared, report = self.prepare()
        self.assertFalse(prepared['questions'])
        self.assertFalse(report['ready'])

    def test_after_answer_source_correct(self):
        after_field = deepcopy(self.raw)
        after_field['source_correct'] = {'type': 'text', 'value': 'wrong'}
        self.record['after']['fields'] = [after_field]
        prepared, report = self.prepare()
        self.assertTrue(report['ready'])
        self.assertEqual(prepared['questions'][0]['answer_fields'][0]['source_evidence']['stage'], 'after')

    def test_incomplete_choices_hold_even_with_explicit_key(self):
        self.raw.update(source_correct={'type': 'text', 'value': 'wrong'}, choices_complete=False)
        prepared, report = self.prepare()
        self.assertFalse(prepared['questions'])
        self.assertIn('incomplete_original_choices:selection', report['held_questions'][0]['reasons'])

    def test_authored_choice_is_not_added(self):
        self.raw['source_correct'] = {'type': 'text', 'value': 'third'}
        prepared, report = self.prepare()
        self.assertFalse(prepared['questions'])
        self.assertIn('source_key_not_in_original_choices:selection', report['held_questions'][0]['reasons'])

    def test_complete_question_is_held_if_one_field_unknown(self):
        first = field('field-1', 'blank')
        first['source_correct'] = {'type': 'text', 'value': '3'}
        self.before['fields'] = [first, field('field-2', 'blank')]
        prepared, report = self.prepare()
        self.assertFalse(prepared['questions'])
        self.assertIn('unconfirmed_correct_answer:field-2', report['held_questions'][0]['reasons'])

    def test_history_blank_values_are_keys_even_when_submission_was_wrong(self):
        self.before['fields'] = [field('field-1', 'blank'), field('field-2', 'blank')]
        raw_html = '<div class="studentAnswer"><div class="freeResponseTextbox">999</div></div>'
        raw_html += '<div class="freeResponseTextbox"><math><mn>2</mn></math></div><div class="freeResponseTextbox">yes</div>'
        (self.directory/'activity-metadata.json').write_text(json.dumps([{'id': 'question-12', 'raw_html': raw_html}]))
        prepared, report = self.prepare()
        self.assertTrue(report['ready'])
        fields = prepared['questions'][0]['answer_fields']
        self.assertEqual([f['correct_value'] for f in fields], ['2', 'yes'])
        self.assertEqual(fields[0]['choices'], [{'type': 'math', 'value': '2'}])

    def test_history_selects_restore_original_choice_and_ignore_solver_key(self):
        raw = field('field-1', 'select', values=('wrong', 'right'))
        self.before['fields'] = [raw]
        html = '<div class="selectList"><div class="selectListFrame correctSelection">wrong</div></div>'
        (self.directory/'activity-metadata.json').write_text(json.dumps([{'id': 'question-12', 'raw_html': html}]))
        prepared, report = self.prepare()
        self.assertTrue(report['ready'])
        self.assertEqual(prepared['questions'][0]['answer_fields'][0]['correct_value'], 'wrong')

    def test_history_layout_mismatch_does_not_shift_keys(self):
        self.before['fields'] = [field('field-1', 'blank'), field('field-2', 'blank')]
        html = '<div class="freeResponseTextbox">4</div>'
        (self.directory/'activity-metadata.json').write_text(json.dumps([{'id': 'question-12', 'raw_html': html}]))
        _, report = self.prepare()
        self.assertFalse(report['ready'])
        self.assertEqual(report['observations'][0]['reason'], 'history_field_layout_mismatch')

    def test_proof_stages_supply_accepted_fields_without_overall_correct_grade(self):
        self.before['fields'] = [field('field-1', 'select'), field('field-2', 'select')]
        stages = []
        for index, raw in enumerate(self.before['fields']):
            raw = deepcopy(raw)
            raw['source_correct'] = {'type': 'text', 'value': 'wrong'}
            stages.append({'observation': {'fields': [raw]}})
        self.record['proof_stages'] = stages
        self.record['actual_result'] = 'Partial Credit'
        prepared, report = self.prepare()
        self.assertTrue(report['ready'])
        self.assertEqual(len(prepared['questions'][0]['answer_fields']), 2)

    def test_changed_stage_choices_cannot_supply_stale_key(self):
        stage = deepcopy(self.raw)
        stage.update(choices=[choice('wrong'), choice('other', 'b')], source_correct={'type': 'text', 'value': 'wrong'})
        self.record['proof_stages'] = [{'observation': {'fields': [stage]}}]
        _, report = self.prepare()
        self.assertFalse(report['ready'])

    def test_explicit_solution_statement_is_accepted_but_incidental_formula_is_not(self):
        self.record['after']['worked_solution'] = 'The correct answer is (a).'
        prepared, report = self.prepare()
        self.assertTrue(report['ready'])
        self.assertEqual(prepared['questions'][0]['answer_fields'][0]['correct_value'], 'wrong')
        self.record['after']['worked_solution'] = 'We encounter right in an intermediate calculation.'
        _, report = self.prepare()
        self.assertFalse(report['ready'])

    def test_explicit_quoted_text_key_is_preserved(self):
        self.record['after']['worked_solution'] = 'Therefore, the correct answer is "wrong."'
        prepared, report = self.prepare()
        self.assertTrue(report['ready'])
        self.assertEqual(prepared['questions'][0]['answer_fields'][0]['correct_value'], 'wrong')

    def test_explicit_blank_solution_is_literal_not_inferred(self):
        self.before['fields'] = [field('field-1', 'blank')]
        self.record['after']['worked_solution'] = 'The correct answer is $4$.'
        prepared, report = self.prepare()
        self.assertTrue(report['ready'])
        self.assertEqual(prepared['questions'][0]['answer_fields'][0]['choices'], [{'type': 'math', 'value': '4'}])
        self.record['after']['worked_solution'] = 'Therefore $y=4$.'
        _, report = self.prepare()
        self.assertFalse(report['ready'])

    def test_history_key_preferred_to_accepted_alternative(self):
        self.before['fields'] = [field('field-1', 'blank')]
        self.before['fields'][0].update(tag='mathquill', submitted_value='2/4')
        self.record['actual_result'] = 'Correct'
        (self.directory/'activity-metadata.json').write_text(json.dumps([{
            'id': 'question-12', 'raw_html': '<div class="freeResponseTextbox"><math><mfrac><mn>1</mn><mn>2</mn></mfrac></math></div>'}]))
        prepared, report = self.prepare()
        self.assertTrue(report['ready'])
        self.assertEqual(prepared['questions'][0]['answer_fields'][0]['correct_value'], r'\frac{1}{2}')
        self.assertFalse(any(x['reason'] == 'source_answer_values_differ' for x in report['observations']))

    def test_explicit_final_choice_expression_is_copied_without_solving(self):
        self.raw['choices'] = [choice('x=4', 'a', 'math'), choice('x=5', 'b', 'math')]
        self.record['after']['worked_solution'] = 'An intermediate calculation gives $x=5$.\n\nTherefore, the solution is $x=4.$'
        prepared, report = self.prepare()
        self.assertTrue(report['ready'])
        self.assertEqual(prepared['questions'][0]['answer_fields'][0]['correct_value'], 'x=4')
        self.record['after']['worked_solution'] = 'An intermediate calculation gives $x=5$.'
        _, report = self.prepare()
        self.assertFalse(report['ready'])

    def test_multistep_restores_local_prompt(self):
        self.content['task_type'] = 'multistep'
        self.record['local_problem'] = 'Part 2 question'
        self.before['source_problem'] = 'LLM solution of previous part + part 2 question'
        self.raw['source_correct'] = {'type': 'text', 'value': 'wrong'}
        prepared, report = self.prepare()
        self.assertTrue(report['ready'])
        self.assertEqual(prepared['questions'][0]['problem'], 'Part 2 question')

    def test_canonical_source_absence_does_not_invent_fields(self):
        self.content['questions'] = []
        self.content['canonical_examples'] = [{'math_academy_id': 'e-99', 'problem': 'Local', 'worked_solution': 'Local',
            'difficulty': None, 'missing_source_fields': ['answer_fields', 'difficulty']}]
        (self.directory/'example-99.json').write_text(json.dumps({
            'problem': 'Example problem', 'worked_solution': 'Example solution', 'fields': []}))
        prepared, report = self.prepare()
        self.assertTrue(report['ready'])
        self.assertEqual(prepared['canonical_examples'][0]['answer_fields'], [])
        self.assertEqual(prepared['canonical_examples'][0]['problem'], 'Example problem')
        self.assertEqual(prepared['canonical_examples'][0]['missing_source_fields'], ['answer_fields', 'difficulty'])
        self.assertIsNone(prepared['canonical_examples'][0]['difficulty'])

    def test_other_question_grade_cannot_supply_key(self):
        self.raw['submitted_value'] = 'wrong'
        self.record['actual_result'] = 'Correct'
        self.record['after']['dom_id'] = 'step-q99'
        _, report = self.prepare()
        self.assertFalse(report['ready'])
        self.assertIn('source_question_identity_mismatch', report['held_questions'][0]['reasons'])

    def test_history_image_answer_reuses_local_source_asset(self):
        self.before['fields'] = [field('field-1', 'select')]
        self.before['fields'][0]['choices'] = [choice('/tmp/example.png', 'a', 'image'), choice('/tmp/other.png', 'b', 'image')]
        self.before['assets'] = [{'source_url': 'https://mathacademy.com/graphics/1.png', 'path': '/tmp/example.png'}]
        html = '<div class="selectList"><div class="selectListFrame correctSelection"><img src="/graphics/1.png"></div></div>'
        (self.directory/'activity-metadata.json').write_text(json.dumps([{'id': 'question-12', 'raw_html': html}]))
        prepared, report = self.prepare()
        self.assertTrue(report['ready'])
        self.assertEqual(prepared['questions'][0]['answer_fields'][0]['correct_value'], '/tmp/example.png')

    def test_topic_page_example_uses_its_saved_capture(self):
        self.content['questions'] = []
        source = self.directory/'lesson-topic.html'
        html = '<div class="step" steptype="example" contentid="99"><div class="exampleQuestion">New example</div><div class="exampleExplanation">New solution</div></div>'
        source.write_text(html)
        self.content['canonical_examples'] = [{'math_academy_id': 'e-99',
            'source_kind': 'topic_page_example', 'source_file': str(source)}]
        (self.directory/'lesson-example-99.json').write_text(json.dumps({
            'source_file': str(source), 'problem': 'New example', 'worked_solution': 'New solution',
            'fields': [], 'html': html}))
        prepared, report = self.prepare()
        self.assertTrue(report['ready'])
        self.assertEqual(prepared['canonical_examples'][0]['problem'], 'New example')
        source.write_text(html.replace('contentid="99"', 'contentid="98"'))
        _, report = self.prepare()
        self.assertFalse(report['ready'])


if __name__ == '__main__':
    unittest.main()
