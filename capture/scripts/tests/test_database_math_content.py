"""Formatting is enforced at final preparation, including saved-capture imports."""
import copy
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from scripts.database.math_content import formatter, prose, question as format_question
from scripts.database.evidence import UnsupportedContent
from scripts.database.prepare import Preparation, Plan, source_uuid, choice_signature
from scripts.database.pipeline import DatabasePipeline
from scripts.storage import atomic_json
from scripts.tests import test_database as fixtures
from scripts.tests.test_database import FakeClient, question, source_snapshot


LEGACY = r'[\begin{aligned}-1 & 1 & 5 & -2 \\ 0 & 0 & -3 & 1 \\ 0 & 0 & 0 & 1\end{aligned}]'
MATRIX = r'\begin{bmatrix}-1 & 1 & 5 & -2 \\ 0 & 0 & -3 & 1 \\ 0 & 0 & 0 & 1\end{bmatrix}'


def matrix_question(mid='q-11'):
    q = question(mid, LEGACY)
    q.update(problem='Use $B=' + LEGACY + '$.', worked_solution='The matrix is $' + LEGACY + '$.')
    q['answer_fields'][0]['choices'][0]['feedback'] = 'Compare $' + LEGACY + '$.'
    return q


class MathPreparationTests(unittest.TestCase):
    def test_question_example_choices_and_feedback_are_normalized_after_evidence(self):
        q, example = matrix_question(), matrix_question('e-10')
        q['local_problem'] = q['problem']
        q['answer_fields'][0]['evidence'] = {'kind': 'worked_solution', 'value': LEGACY,
            'solution_quote': LEGACY, 'source_file': 'history.html', 'matches_worked_solution': True}
        original = copy.deepcopy(q)
        result = Preparation(source_snapshot()).prepare({'questions': [q], 'canonical_examples': [example]})
        self.assertEqual(result['omissions'], [])
        self.assertEqual(q, original)
        for record in result['content']['questions'] + result['content']['canonical_examples']:
            self.assertEqual(record['problem'], 'Use $B=' + MATRIX + '$.')
            self.assertIn(MATRIX, record['worked_solution'])
            field = record['answer_fields'][0]
            self.assertEqual(field['correct_value'], MATRIX)
            self.assertEqual(field['choices'][0]['value'], MATRIX)
            self.assertEqual(field['choices'][0]['feedback'], 'Compare $' + MATRIX + '$.')
            self.assertEqual(field['evidence']['value'], LEGACY)
        self.assertEqual(result['content']['questions'][0]['local_problem'], result['content']['questions'][0]['problem'])
        assertions = [row for batch in result['batches'] for row in batch['assertions']]
        self.assertTrue(any(row[1] == ':answer/feedback' and MATRIX in row[2] for row in assertions))

    def test_text_choice_correct_link_uses_its_type_and_images_are_unchanged(self):
        q = matrix_question()
        q['answer_fields'][0].update(correct_type='text', correct_value='$' + LEGACY + '$', choices=[
            {'type': 'math', 'value': '$' + LEGACY + '$'},
            {'type': 'text', 'value': '$' + LEGACY + '$'},
            {'type': 'image', 'value': 'images/source.svg'}])
        normalized = format_question(q)
        field = normalized['answer_fields'][0]
        self.assertEqual(field['correct_value'], '$' + MATRIX + '$')
        self.assertEqual(field['choices'][0]['value'], MATRIX)
        self.assertEqual(field['choices'][2]['value'], 'images/source.svg')

    def test_tutorials_and_multistep_context_share_the_final_format(self):
        q = question()
        content = {'questions': [q], 'title': 'Matrices', 'lesson_definition': {'topic_id': 1,
            'title': 'Matrices', 'complete': True, 'steps': [
                {'math_academy_id': 50, 'content_id': 20, 'type': 'tutorial', 'title': 'Intro'}]},
            'tutorials': [{'math_academy_id': 20, 'title': 'Intro', 'content': '$' + LEGACY + '$'}]}
        prepared = Preparation(source_snapshot()).prepare(content)
        tutorials = [r[2] for b in prepared['batches'] for r in b['assertions'] if r[1] == ':tutorial/content']
        self.assertEqual(tutorials, ['$' + MATRIX + '$'])
        content = {'questions': [q], 'task_type': 'multistep', 'multistep_id': 20,
            'question_order': ['q-11'], 'shared_context': '$' + LEGACY + '$'}
        prepared = Preparation(source_snapshot()).prepare(content)
        self.assertEqual(prepared['content']['shared_context'], '$' + MATRIX + '$')
        self.assertEqual(prepared['omissions'], [])

    def test_authored_matrix_answer_and_operand_layouts_survive_html_conversion(self):
        layout = formatter().matrix_answer('A^T', [['{{field-0}}', '2'], ['3', '{{field-1}}']])
        operands = formatter().matrix_operands(['A=' + MATRIX])
        self.assertEqual(prose(layout), layout)
        self.assertEqual(prose(operands), operands)
        mixed = '<p>Complete the matrix.</p>' + layout + '<p>Use:</p>' + operands
        converted = prose(mixed)
        self.assertIn(layout, converted)
        self.assertIn(operands, converted)
        self.assertIn('{{field-0}}', converted)
        self.assertNotIn('<p>', converted)

    def test_format_revision_reuses_authored_choice_and_preserves_entered_values(self):
        for kind in ('radio', 'blank'):
            with self.subTest(kind=kind):
                chosen = {':db/id': 20, ':answer/id': source_uuid('answer', 20),
                    ':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': LEGACY}
                if kind == 'blank':
                    chosen[':task-item/_responses'] = [{':db/id': 30}]
                entered = {':db/id': 21, ':answer/id': source_uuid('answer', 21),
                    ':answer/type': {':db/ident': ':answer.type/math'},
                    ':answer/value': r'\matrix{' if kind == 'blank' else 'different learner entry',
                    ':task-item/_responses': [{':db/id': 31}]}
                field = {':db/id': 10, ':answer-field/id': source_uuid('field', 10), ':answer-field/key': 'x',
                    ':answer-field/type': {':db/ident': ':answer-field.type/' + kind},
                    ':answer-field/choices': [chosen, entered], ':answer-field/correct': chosen}
                old = {':db/id': 5, ':question/id': source_uuid('question', 5), ':question/answer-fields': [field]}
                before = copy.deepcopy(old)
                q = matrix_question()
                q['answer_fields'][0].update(type=kind, correct_type='math')
                if kind == 'radio':
                    q['answer_fields'][0]['choices'].append({'type': 'math', 'value': entered[':answer/value']})
                q = format_question(q)
                prep = Preparation(source_snapshot())
                plan = Plan(prep.snapshot)
                prep.question(plan, q, old, False)
                batch = plan.finish()
                if kind == 'radio':
                    self.assertIn([20, ':answer/value', MATRIX], batch['assertions'])
                    self.assertFalse(any(row[1] == ':answer/id' for row in batch['assertions']))
                else:
                    self.assertFalse(any(row[0] == 20 for row in batch['assertions'] + batch['retractions']))
                    self.assertTrue(any(row[1] == ':answer/value' and row[2] == MATRIX for row in batch['assertions']))
                self.assertFalse(any(row[0] == 21 for row in batch['assertions'] + batch['retractions']))
                self.assertFalse(any(row[1] == ':answer-field/choices' for row in batch['retractions']))
                self.assertFalse(any(row[1] == ':answer-field/id' for row in batch['assertions']))
                self.assertEqual(old, before)
        self.assertEqual(choice_signature('math', r'\matrix{'), ('math', r'\matrix{'))

    def test_referenced_radio_and_select_values_are_immutable_before_any_plan_change(self):
        for kind in ('radio', 'select'):
            with self.subTest(kind=kind):
                answer = {':db/id': 20, ':answer/id': source_uuid('answer', 20),
                    ':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': LEGACY,
                    ':task-item/_responses': [{':db/id': 30}]}
                field = {':db/id': 10, ':answer-field/id': source_uuid('field', 10), ':answer-field/key': 'x',
                    ':answer-field/type': {':db/ident': ':answer-field.type/' + kind},
                    ':answer-field/choices': [answer], ':answer-field/correct': answer}
                old = {':db/id': 5, ':question/id': source_uuid('question', 5), ':question/answer-fields': [field]}
                before = copy.deepcopy(old)
                q = matrix_question()
                q['answer_fields'][0].update(type=kind, correct_type='math')
                prep = Preparation(source_snapshot())
                plan = Plan(prep.snapshot)
                with self.assertRaisesRegex(UnsupportedContent, 'separate display migration is required'):
                    prep.question(plan, format_question(q), old, False)
                self.assertEqual(plan.finish()['forms'], [])
                self.assertEqual(old, before)


class MathRequestTests(unittest.TestCase):
    def test_invalid_math_stops_before_creating_an_immutable_request(self):
        for invalid in (r'$C^T=\=$', r'$$\begin{aligned}x &= 1 \[5pt] y &= 2\end{aligned}$$', r'$\matrix{$'):
            with self.subTest(invalid=invalid), tempfile.TemporaryDirectory() as directory:
                capture, config = fixtures.PipelineTests().setup(directory)
                content = json.loads((capture / 'content.json').read_text())
                content['questions'][0]['problem'] = invalid
                atomic_json(capture / 'content.json', content)
                client = FakeClient()
                result = DatabasePipeline(config, threading.Event(), client=client).process(capture)
                self.assertEqual(result['status'], 'pending', result)
                self.assertFalse(result['unknown_or_unverified_commit'])
                self.assertFalse((capture / 'database/request.json').exists())
                self.assertFalse(any(cmd == 'transact' for cmd, _ in client.calls))

    def test_legacy_pending_request_replays_exact_bytes_before_a_new_formatted_request(self):
        class RecordingClient(FakeClient):
            def __init__(self):
                super().__init__()
                self.submissions = []

            def command(self, cmd, *options):
                opts = dict(zip(options[::2], options[1::2]))
                if cmd == 'transact':
                    self.submissions.append((opts['--request-key'], Path(opts['--file']).read_bytes()))
                return super().command(cmd, *options)

        with tempfile.TemporaryDirectory() as directory:
            capture, config = fixtures.PipelineTests().setup(directory)
            content = json.loads((capture / 'content.json').read_text())
            q = matrix_question()
            q['knowledge_point_id'] = content['questions'][0]['knowledge_point_id']
            content['questions'] = [q]
            atomic_json(capture / 'content.json', content)
            original = (capture / 'content.json').read_bytes()
            client = RecordingClient()
            client.timeout_once = True
            pipeline = DatabasePipeline(config, threading.Event(), client=client)
            # Emulate a request saved by the earlier capture preparation code.
            with patch('scripts.database.prepare.formatted_question', side_effect=lambda q: q):
                first = pipeline.process(capture)
            self.assertTrue(first['unknown_or_unverified_commit'], first)
            saved = json.loads((capture / 'database/request.json').read_text())
            result = pipeline.process(capture)
            self.assertEqual(result['status'], 'verified', result)
            self.assertEqual(client.submissions[0], client.submissions[1])
            self.assertEqual(client.submissions[0][1], saved['transaction'].encode())
            self.assertNotEqual(client.submissions[-1][0], saved['request_key'])
            problems = [v for (e, attr), values in client.facts.items() if attr == 'question/problem' for v, _ in values]
            self.assertIn('Use $B=' + MATRIX + '$.', problems)
            self.assertEqual((capture / 'content.json').read_bytes(), original)
            self.assertEqual(pipeline.process(capture)['status'], 'no_changes')


if __name__ == '__main__':
    unittest.main()
