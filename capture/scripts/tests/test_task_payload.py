from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from scripts.activity.task_payload import task_payload, semantic_identity
from scripts.activity.solver import _image_paths


class TaskPayloadTests(unittest.TestCase):
    def setUp(self):
        self.question = {'math_academy_id': 'q-1', 'problem': r'Find $x$ and $y$ in the diagram.',
            'worked_solution': r'Therefore $x=2$ and $y=3$.', 'screenshot': '/question.png',
            'html': '<div>browser markup</div>' * 1000, 'raw_html': '<div>history</div>',
            'html_path': '/original.html', 'solution_evidence': '/solution.html',
            'fields': [{'key': 'x', 'type': 'select', 'source_correct': {'value': '2', 'type': 'math'},
                'evidence': {'kind': 'ma_answer', 'value': '2', 'source_file': '/grade.html'},
                'choices': [{'option': 'A', 'value': '2', 'type': 'math', 'html': '<math>2</math>'}]},
                {'key': 'y', 'type': 'blank'}],
            'assets': [{'path': '/diagram.png', 'sha256': 'diagram-hash', 'html': '<img src="x">'}]}
        self.question['answer_fields'] = deepcopy(self.question['fields'])

    def test_current_math_fields_solution_images_and_provenance_survive(self):
        payload = task_payload('judge_question', {'question': self.question,
            'instructional_content': [{'html': 'huge irrelevant tutorial'}]})
        question = payload['question']
        self.assertEqual(question['problem'], self.question['problem'])
        self.assertEqual(question['worked_solution'], self.question['worked_solution'])
        self.assertEqual(question['screenshot'], '/question.png')
        self.assertEqual(question['assets'][0]['path'], '/diagram.png')
        self.assertEqual(question['fields'][0]['choices'][0], {'option': 'A', 'type': 'math', 'value': '2'})
        self.assertEqual(question['fields'][0]['evidence']['source_file'], '/grade.html')
        self.assertEqual(question['solution_evidence'], '/solution.html')
        self.assertNotIn('html', question)
        self.assertNotIn('answer_fields', question)
        self.assertNotIn('instructional_content', payload)
        self.assertEqual(task_payload('judge_question', payload), payload)

    def test_solve_keeps_only_current_example_and_multistep_answer_summaries(self):
        previous = {'question': {'math_academy_id': 'q-0', 'problem': 'Find velocity.', 'html': 'huge'},
            'solution': {'status': 'confirmed', 'answers': [{'key': 'v', 'correct_value': '4'}]},
            'feedback': {'grade': 'Correct'}}
        raw = {'question': self.question, 'activity': {'kind': 'multistep'}, 'shared_context': [
            {'id': 'setup', 'problem': 'A particle starts at rest.', 'html': 'huge setup'}],
            'current_example': {'math_academy_id': 'e-1', 'problem': 'Useful example', 'worked_solution': 'Its method.', 'html': 'raw'},
            'earlier_parts': [previous], 'instructional_content': [{'html': 'other tutorial'}]}
        payload = task_payload('solve_question', raw)
        self.assertEqual(payload['shared_context'][0]['problem'], 'A particle starts at rest.')
        self.assertEqual(payload['earlier_parts'][0]['answers'][0]['correct_value'], '4')
        self.assertEqual(payload['current_example']['worked_solution'], 'Its method.')
        self.assertNotIn('html', payload['current_example'])
        self.assertEqual(task_payload('solve_question', payload), payload)
        independent = task_payload('solve_question', {'question': self.question, 'earlier_parts': [previous]})
        self.assertNotIn('earlier_parts', independent)

    def test_judge_retains_actual_responses_grades_and_deduplicates_ui_attempts(self):
        submissions = [{'responses': [{'key': 'x', 'value': '2', 'option': 'B', 'keys': ['huge typing trace']}],
                        'outcome': 'unknown', 'started_at': index} for index in range(30)]
        payload = task_payload('judge_question', {'question': self.question, 'presentations': [{
            'key': 'live', 'question': self.question, 'last_observation': self.question,
            'submissions': submissions, 'feedback': {'grade': 'Correct', 'field_grades': {'x': 'Correct'},
            'html_path': '/graded.html', 'html': 'huge'}}]})
        presentation = payload['presentations'][0]
        self.assertEqual(len(presentation['submissions']), 1)
        self.assertEqual(presentation['submissions'][0]['attempt_count'], 30)
        self.assertEqual(presentation['submissions'][0]['responses'][0]['value'], '2')
        self.assertEqual(presentation['feedback']['grade'], 'Correct')
        self.assertEqual(presentation['feedback']['html_path'], '/graded.html')
        self.assertNotIn('question', presentation)
        self.assertEqual(task_payload('judge_question', payload), payload)

    def test_cache_ignores_capture_noise_but_not_changed_math_or_graphic(self):
        first = task_payload('judge_question', {'question': self.question})
        changed = deepcopy(self.question)
        changed.update(html='different markup', captured_at=999, html_path='/elsewhere.html', solution_evidence='/elsewhere-solution.html')
        changed['fields'][0]['evidence']['source_file'] = '/other-grade.html'
        second = task_payload('judge_question', {'question': changed})
        self.assertEqual(semantic_identity('judge_question', first), semantic_identity('judge_question', second))
        second['question']['problem'] += ' plus one'
        self.assertNotEqual(semantic_identity('judge_question', first), semantic_identity('judge_question', second))
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / 'image.png'
            image.write_bytes(b'first')
            payload = {'question': {'assets': [{'path': str(image)}]}}
            before = semantic_identity('solve_question', payload)
            image.write_bytes(b'changed diagram')
            self.assertNotEqual(before, semantic_identity('solve_question', payload))

    def test_svg_or_unavailable_graphic_keeps_scoped_screenshot_fallback(self):
        for asset in ({'path': '/diagram.svg', 'content_type': 'image/svg+xml', 'html': '<svg>raw defs</svg>'},
                      {'source_url': 'diagram.png', 'unavailable': 'download failed'}):
            payload = task_payload('solve_question', {'question': {'problem': 'Find the diagram area.',
                'screenshot': '/question.png', 'assets': [asset]}})
            self.assertEqual(payload['question']['screenshot'], '/question.png')
            self.assertNotIn('html', payload['question']['assets'][0])

    def test_all_required_graphics_attach_without_arbitrary_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / ('%s.png' % index) for index in range(14)]
            for path in paths:
                path.write_bytes(b'image')
            self.assertEqual(_image_paths({'assets': [{'path': str(path)} for path in paths]}), paths)

    def test_complete_text_and_graphics_do_not_duplicate_question_screenshot(self):
        payload = task_payload('solve_question', {'question': {'problem': 'Find {{x}}.', 'screenshot': '/question.png',
            'fields': [{'key': 'x', 'type': 'blank'}], 'assets': [{'path': '/diagram.png'}]}})
        self.assertNotIn('screenshot', payload['question'])
        self.assertEqual(payload['question']['assets'][0]['path'], '/diagram.png')
