"""Focused source reviews must not be suppressed by stale answer evidence."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from scripts.activity.evidence import finalize_answers
from scripts.database.evidence import authoritative_question, UnsupportedContent


class AnswerFinalizationTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads((Path(__file__).parent / 'fixtures/q42074-finalizer.json').read_text())
        self.question = deepcopy(self.fixture['question'])
        self.judgment = deepcopy(self.fixture['judgment'])

    def premise_case(self):
        question = {'math_academy_id': 'q-1', 'problem': 'Find $f(2)$.',
            'worked_solution': 'Given $f(2)=3$, the answer is $3$.', 'source_file': 'solution.html',
            'answer_fields': [{'key': 'selection', 'type': 'radio', 'correct_value': '2',
                'correct_type': 'math', 'value_type': 'math',
                'choices': [{'type': 'math', 'value': '2'}, {'type': 'math', 'value': '3'}],
                'evidence': {'kind': 'worked_solution', 'value': '2', 'source_file': 'solution.html',
                             'solution_quote': '2', 'matches_worked_solution': True}}]}
        judgment = {'status': 'confirmed', 'answers': [{'key': 'selection', 'ma_value': '3',
            'correct_value': '3', 'value_type': 'math', 'ma_basis': 'worked_solution',
            'ma_evidence': 'the answer is $3$.'}]}
        return question, judgment

    def test_fresh_checked_answer_supersedes_old_quote_of_a_premise(self):
        question, judgment = self.premise_case()
        original = deepcopy(question)
        self.assertEqual(authoritative_question(question)['answer_fields'][0]['correct_value'], '2')
        field = authoritative_question(finalize_answers(question, [], judgment))['answer_fields'][0]
        self.assertEqual(field['correct_value'], '3')
        self.assertEqual(field['evidence']['solution_quote'], 'the answer is $3$.')
        self.assertEqual(question, original)

    def test_checked_premise_cannot_be_replaced_by_unquoted_or_wrong_typed_answer(self):
        for change in ({'ma_evidence': 'Invented answer: 3'}, {'value_type': 'text'}, {'ma_value': '4'}):
            with self.subTest(change=change):
                question, judgment = self.premise_case()
                judgment['answers'][0].update(change)
                field = finalize_answers(question, [], judgment)['answer_fields'][0]
                self.assertEqual(field['correct_value'], '2')
                self.assertEqual(field['evidence']['solution_quote'], '2')

    def test_direct_ma_key_and_bound_grade_are_not_superseded_by_fresh_prose(self):
        for kind in ('ma_answer', 'ma_correct_grade'):
            with self.subTest(kind=kind):
                question, judgment = self.premise_case()
                question['answer_fields'][0]['evidence'] = {'kind': kind, 'value': '2',
                    'source_file': 'visible-source.html', 'grade': 'correct'}
                field = finalize_answers(question, [], judgment)['answer_fields'][0]
                self.assertEqual(field['correct_value'], '2')
                self.assertEqual(field['evidence']['kind'], kind)

    def test_fresh_source_error_supersedes_premise_but_remains_unimportable(self):
        question, judgment = self.premise_case()
        question['worked_solution'] = 'Given $f(2)=8$, the source answer is $8$.'
        judgment.update(status='source_error')
        judgment['answers'][0].update(ma_value='8', correct_value='3', disagrees=True,
                                      ma_evidence='the source answer is $8$.')
        result = finalize_answers(question, [], judgment)
        field = result['answer_fields'][0]
        self.assertEqual(field['correct_value'], '8')
        self.assertFalse(field['evidence']['choice_present'])
        self.assertEqual(judgment['answers'][0]['correct_value'], '3')
        with self.assertRaises(UnsupportedContent):
            authoritative_question(result)

    def test_radio_filename_fact_is_not_superseded_by_fresh_prose(self):
        question, judgment = self.premise_case()
        images = ['assets/question-a-' + str(i) + '.png' for i in (1, 2, 3)]
        field = question['answer_fields'][0]
        field.update(correct_value=images[0], correct_type='image', value_type='image',
            choices=[{'type': 'image', 'value': value} for value in images],
            evidence={'kind': 'radio_image_filename', 'value': images[0]})
        judgment['answers'][0].update(ma_value=images[1], value_type='image')
        field = finalize_answers(question, [], judgment)['answer_fields'][0]
        self.assertEqual(field['correct_value'], images[0])
        self.assertEqual(field['evidence']['kind'], 'radio_image_filename')

    def test_real_green_theorem_review_replaces_nonchoice_interpretation(self):
        before = deepcopy(self.question)
        checked = authoritative_question(finalize_answers(self.question, [], self.judgment))
        field = checked['answer_fields'][0]
        self.assertEqual(field['correct_value'], self.judgment['answers'][0]['ma_value'])
        self.assertEqual(field['correct_type'], 'math')
        self.assertTrue(field['evidence']['choice_present'])
        self.assertIn(field['evidence']['solution_quote'], checked['worked_solution'])
        self.assertEqual(field['evidence']['solution_quote'], self.judgment['answers'][0]['ma_evidence'])
        self.assertEqual(self.question, before)

    def test_nonchoice_source_fact_survives_without_supported_replacement(self):
        field = finalize_answers(self.question, [], {'answers': []})['answer_fields'][0]
        self.assertEqual(field['correct_value'], self.question['answer_fields'][0]['correct_value'])
        self.assertEqual(field['evidence'], self.question['answer_fields'][0]['evidence'])
        self.assertEqual(field['source_answer_status'], 'unavailable')
        with self.assertRaises(UnsupportedContent):
            authoritative_question({**self.question, 'answer_fields': [field]})

    def test_invented_fresh_quote_cannot_override_preserved_source_fact(self):
        self.judgment['answers'][0]['ma_evidence'] = 'This quote is absent from the source.'
        field = finalize_answers(self.question, [], self.judgment)['answer_fields'][0]
        self.assertEqual(field['correct_value'], self.question['answer_fields'][0]['correct_value'])
        self.assertFalse(field['evidence']['choice_present'])

    def test_valid_explicit_ma_key_takes_precedence_over_solution_interpretation(self):
        old = self.question['answer_fields'][0]
        old['evidence'] = {'kind': 'ma_answer', 'value': old['correct_value'], 'source_file': 'visible-answer.html'}
        field = finalize_answers(self.question, [], self.judgment)['answer_fields'][0]
        self.assertEqual(field['correct_value'], old['correct_value'])
        self.assertEqual(field['evidence']['kind'], 'ma_answer')

    def test_stale_quote_and_type_are_replaced_by_exact_current_typed_choice(self):
        old = self.question['answer_fields'][0]
        old['evidence']['solution_quote'] = 'Quotation from an obsolete solution.'
        old['correct_type'] = 'text'
        old['correct_option'] = 'a'
        old['source_answer_status'] = 'unavailable'
        field = authoritative_question(finalize_answers(self.question, [], self.judgment))['answer_fields'][0]
        self.assertEqual((field['correct_value'], field['correct_type']),
                         (self.judgment['answers'][0]['ma_value'], 'math'))
        self.assertNotIn('source_answer_status', field)
        self.assertNotIn('correct_option', field)

    def test_source_error_keeps_ma_value_separate_from_agent_correction(self):
        self.question['worked_solution'] = 'The source answer is 8.'
        self.judgment.update(status='source_error', answers=[{'key': 'selection', 'value_type': 'math',
            'correct_value': '2', 'ma_value': '8', 'ma_basis': 'worked_solution',
            'ma_evidence': 'The source answer is 8.', 'disagrees': True}])
        field = finalize_answers(self.question, [], self.judgment)['answer_fields'][0]
        self.assertEqual(field['correct_value'], '8')
        self.assertFalse(field['evidence']['choice_present'])
        self.assertEqual(self.judgment['answers'][0]['correct_value'], '2')
        self.assertTrue(self.judgment['answers'][0]['disagrees'])

    def test_existing_exact_source_choice_quote_repair_remains_supported(self):
        source = r'{\begin{aligned}x=-2 \\ z=-4y+8\end{aligned}'
        agent_value = source + '}'
        self.question['worked_solution'] = 'The tangent is $' + source + '$.'
        self.question['answer_fields'] = [{'key': 'selection', 'type': 'radio',
            'choices': [{'type': 'math', 'value': source}, {'type': 'math', 'value': 'wrong'}],
            'correct_value': agent_value, 'value_type': 'math',
            'evidence': {'kind': 'worked_solution', 'value': agent_value, 'source_file': 'solution.html',
                         'solution_quote': source, 'matches_worked_solution': True}}]
        field = authoritative_question(finalize_answers(self.question, [], {'answers': []}))['answer_fields'][0]
        self.assertEqual(field['correct_value'], source)
        self.assertEqual(field['evidence']['agent_value'], agent_value)
        self.assertTrue(field['evidence']['source_choice_quote'])


if __name__ == '__main__':
    unittest.main()
