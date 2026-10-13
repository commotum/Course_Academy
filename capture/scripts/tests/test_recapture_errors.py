"""Successful source rereads replace capture failures without erasing originals."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from scripts.activity.capture import ActivityCapture
from scripts.activity.evidence import capture_gaps, finalize_answers, merge_question
from scripts.browser.adapter import EXTRACT, MathAcademyBrowser
from scripts.database.evidence import authoritative_question, UnsupportedContent
from scripts.database.prepare import Preparation
from scripts.tests.test_database import question, source_snapshot


MATH_ERROR = 'MathJax formula has no assistive MathML'
SOLUTION_ERROR = 'Unsupported MathML node: maligngroup'


def captured(**changes):
    result = question()
    result.update(html_path='/original.html', errors=[MATH_ERROR],
                  extraction_parts=['problem', 'fields', 'solution'],
                  extraction_error_parts={MATH_ERROR: ['problem']})
    result.update(changes)
    return result


def prepare(record):
    record = deepcopy(record)
    record['knowledge_point_id'] = str(source_snapshot()['entities'][1][':knowledge-point/id'])
    return Preparation(source_snapshot()).prepare({'questions': [record]})


class RecaptureErrorTests(unittest.TestCase):
    def test_verified_reread_retires_decorated_phantom_parser_failure(self):
        error='Unsupported decorated MathML phantom: border style'
        before=captured(errors=[error],extraction_error_parts={error:['problem']})
        recovered=merge_question(before,captured(errors=[]))
        self.assertEqual(recovered['errors'],[])
        self.assertEqual(recovered['extraction_error_history'][0]['errors'],[error])
    def test_clean_full_read_replaces_legacy_failure_and_preserves_source_history(self):
        before = captured()
        before.pop('extraction_error_parts')
        before.pop('extraction_parts')
        after = captured(errors=[], html_path='/recaptured.html')
        merged = merge_question(before, after)
        self.assertEqual(merged['errors'], [])
        self.assertEqual(before['errors'], [MATH_ERROR])
        self.assertFalse(capture_gaps({'questions': [merged]}))
        self.assertEqual(authoritative_question(merged)['math_academy_id'], 'q-11')
        self.assertFalse(prepare(merged)['omissions'])
        history = merged['extraction_error_history']
        self.assertEqual(history[0]['source']['html_path'], '/original.html')
        self.assertEqual(history[-1]['replaced_by']['html_path'], '/recaptured.html')
        self.assertEqual(merge_question(merged, after)['extraction_error_history'], history)

    def test_fieldless_history_repairs_prompt_and_retains_live_controls(self):
        before = captured(answer_fields_complete=True)
        after = {'math_academy_id': 'q-11', 'problem': 'What is $1+1$?',
                 'worked_solution': '$1+1=2$', 'fields': [], 'answer_fields_complete': None,
                 'errors': [], 'extraction_parts': ['problem', 'solution'],
                 'extraction_error_parts': {}, 'html_path': '/history.html'}
        merged = merge_question(before, after)
        self.assertEqual(merged['errors'], [])
        self.assertEqual(merged['answer_fields'], before['answer_fields'])
        self.assertTrue(merged['answer_fields_complete'])
        self.assertFalse(prepare(merged)['omissions'])

    def test_solution_only_read_cannot_clear_failed_prompt(self):
        after = {'math_academy_id': 'q-11', 'worked_solution': 'The answer is 2.',
                 'extraction_parts': ['solution'], 'errors': [], 'html_path': '/solution.html'}
        merged = merge_question(captured(), after)
        self.assertEqual(merged['errors'], [MATH_ERROR])
        self.assertEqual(merged['problem'], 'What is $1+1$?')
        with self.assertRaises(UnsupportedContent):
            authoritative_question(merged)

    def test_prompt_repair_does_not_erase_unrelated_solution_failure(self):
        before = captured(errors=[MATH_ERROR, SOLUTION_ERROR],
                          extraction_error_parts={MATH_ERROR: ['problem'], SOLUTION_ERROR: ['solution']})
        after = {'math_academy_id': 'q-11', 'problem': before['problem'], 'errors': [],
                 'extraction_parts': ['problem'], 'html_path': '/prompt.html'}
        merged = merge_question(before, after)
        self.assertEqual(merged['errors'], [SOLUTION_ERROR])
        self.assertEqual(merged['extraction_error_parts'], {SOLUTION_ERROR: ['solution']})
        self.assertEqual(merged['worked_solution'], before['worked_solution'])
        self.assertEqual(merged['extraction_error_history'][-1]['errors'], [MATH_ERROR])

    def test_new_solution_failure_does_not_block_successful_prompt_repair(self):
        for error in (SOLUTION_ERROR, MATH_ERROR):
            with self.subTest(error=error):
                after = captured(errors=[error], html_path='/history.html',
                                 extraction_parts=['problem', 'solution'], answer_fields=[], fields=[],
                                 extraction_error_parts={error: ['solution']})
                merged = merge_question(captured(), after)
                self.assertEqual(merged['errors'], [error])
                self.assertEqual(merged['extraction_error_parts'], {error: ['solution']})
                self.assertEqual(merged['extraction_error_history'][-1]['error_parts'], {MATH_ERROR: ['problem']})

    def test_absent_error_update_or_missing_source_does_not_claim_recovery(self):
        for missing in ('errors', 'html_path', 'math_academy_id'):
            with self.subTest(missing=missing):
                after = captured(errors=[])
                after.pop(missing)
                self.assertEqual(merge_question(captured(), after)['errors'], [MATH_ERROR])

    def test_authored_source_errors_and_agent_judgments_survive_clean_read(self):
        authored = 'Math Academy source answer contradicts its worked solution'
        finding = {'status': 'source_error', 'ma_value': '3', 'agent_value': '2'}
        before = captured(errors=[MATH_ERROR, authored], source_errors=[authored], judgment=finding)
        merged = merge_question(before, captured(errors=[], html_path='/clean.html'))
        self.assertEqual(merged['errors'], [authored])
        self.assertEqual(merged['source_errors'], [authored])
        self.assertEqual(merged['judgment'], finding)

    def test_changed_identity_does_not_resolve_and_conflicting_source_stays_quarantined(self):
        before = captured()
        self.assertEqual(merge_question(before, captured(math_academy_id='q-99', errors=[]))['errors'], [MATH_ERROR])
        record = {'key': 'live', 'question': before, 'observed_position': 0, 'submissions': []}
        capture = ActivityCapture.__new__(ActivityCapture)
        capture.exposures = None
        capture.activity = {'task_id': '1', 'kind': 'diagnostic'}
        capture.state = {'steps': [], 'presentations': {'live': record}}
        capture._save = lambda: None
        changed = captured(problem='An unrelated source problem', errors=[], sequence_position=1)
        content = capture._merge_history({'questions': [changed]})
        quarantined = next(q for q in content['questions'] if q.get('source_id') == 'unreconciled:live')
        self.assertEqual(quarantined['errors'], [MATH_ERROR])
        self.assertNotIn('math_academy_id', quarantined)
        self.assertEqual(quarantined['observed_math_academy_id'], 'q-11')
        self.assertEqual(len(content['questions']), 2)

    def test_invalid_or_partial_controls_cannot_resolve_field_failure(self):
        error = 'Unsupported math editor: answer'
        before = captured(errors=[error], extraction_error_parts={error: ['fields']})
        variants = [{'fields_complete': False}, {'answer_fields_complete': False},
                    {'answer_fields': [{'key': '', 'type': 'blank'}]},
                    {'answer_fields': [{'key': 'x', 'type': 'unknown'}]},
                    {'answer_fields': [{'key': 'x', 'type': 'blank'}, {'key': 'x', 'type': 'blank'}]},
                    {'answer_fields': [{'key': 'x', 'type': 'radio', 'choices': []}]},
                    {'problem': 'Enter {{field-99}}'}]
        for variant in variants:
            with self.subTest(variant=variant):
                self.assertEqual(merge_question(before, captured(errors=[], **variant))['errors'], [error])
        self.assertEqual(merge_question(before, captured(errors=[]))['errors'], [])

    def test_null_error_update_and_legacy_field_incompleteness_do_not_claim_recovery(self):
        self.assertEqual(merge_question(captured(), captured(errors=None))['errors'], [MATH_ERROR])
        before = captured(answer_fields_complete=False)
        after = {'math_academy_id': 'q-11', 'problem': before['problem'], 'worked_solution': before['worked_solution'],
                 'errors': [], 'fields': [], 'extraction_parts': ['problem', 'solution'], 'html_path': '/history.html'}
        merged = merge_question(before, after)
        self.assertFalse(merged['answer_fields_complete'])
        with self.assertRaisesRegex(UnsupportedContent, 'explicitly incomplete'):
            authoritative_question(merged)

    def test_clean_empty_prompt_assets_retire_failure_and_keep_original_evidence(self):
        error = 'Image unavailable: https://example.invalid/prompt.svg'
        failed = {'source_url': 'https://example.invalid/prompt.svg', 'extraction_part': 'problem',
                  'unavailable': 'initial download failed'}
        before = captured(errors=[error], extraction_error_parts={error: ['problem']}, assets=[failed])
        after = {'math_academy_id': 'q-11', 'problem': before['problem'], 'errors': [], 'assets': [],
                 'extraction_parts': ['problem'], 'html_path': '/history.html'}
        merged = merge_question(before, after)
        self.assertEqual(merged['errors'], [])
        self.assertEqual(merged['assets'], [])
        self.assertFalse(capture_gaps({'questions': [merged]}))
        self.assertEqual(merged['extraction_error_history'][0]['assets'], [failed])
        self.assertEqual(before['assets'], [failed])

    def test_solution_asset_reread_retains_prompt_and_choice_assets(self):
        prompt = {'path': '/prompt.svg', 'sha256': 'prompt', 'extraction_part': 'problem'}
        choice = {'path': '/choice.svg', 'sha256': 'choice', 'extraction_part': 'fields'}
        old_solution = {'path': '/old-solution.svg', 'sha256': 'old', 'extraction_part': 'solution'}
        fresh = {'path': '/solution.svg', 'sha256': 'new', 'extraction_part': 'solution'}
        legacy = {'path': '/unknown.svg', 'sha256': 'unknown'}
        before = captured(errors=[], assets=[prompt, choice, old_solution, legacy])
        after = {'math_academy_id': 'q-11', 'worked_solution': 'Updated solution', 'errors': [],
                 'assets': [fresh], 'extraction_parts': ['solution'], 'html_path': '/solution.html'}
        merged = merge_question(before, after)
        self.assertEqual(merged['assets'], [prompt, choice, legacy, fresh])
        self.assertEqual(merged['answer_fields'], before['answer_fields'])
        after['assets'].append(legacy)
        replayed = merge_question(merged, after)
        self.assertEqual(replayed['assets'], merged['assets'])
        self.assertEqual(merge_question(replayed, after)['assets'], replayed['assets'])

    def test_scoped_image_repair_does_not_require_absent_history_fields(self):
        error = 'Image unavailable: https://example.invalid/prompt.svg'
        before = captured(errors=[error], extraction_error_parts={error: ['problem']})
        after = {'math_academy_id': 'q-11', 'problem': before['problem'], 'errors': [],
                 'extraction_parts': ['problem'], 'html_path': '/history.html'}
        self.assertEqual(merge_question(before, after)['errors'], [])
        after['assets'] = [{'extraction_part': 'problem', 'unavailable': 'download failed'}]
        self.assertEqual(merge_question(before, after)['errors'], [error])


class OfflineExtractionScopesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.context.route('**/*', lambda route: route.abort())
        self.addCleanup(self.context.close)
        self.page = self.context.new_page()

    def extract(self, markup):
        self.page.set_content(markup)
        return self.page.locator('#q').evaluate(EXTRACT)

    def test_saved_review_history_blanks_keep_live_identity_and_prepare(self):
        fixture = json.loads((Path(__file__).parent / 'fixtures' /
                              'review-14114793-history-blanks.json').read_text())
        expected = {'q-332291': '-2', 'q-332303': '-2x+1',
                    'q-332541': 'Ae^{-6x}+2x+1', 'q-332544': 'A{e}^{-4x}-2'}
        records, history = {}, []
        for row in fixture['questions']:
            live, source = deepcopy(row['live']), row['history']
            identity = source['math_academy_id']
            with self.subTest(identity=identity):
                self.page.set_content(source['html'])
                item = self.page.locator('.question').evaluate(EXTRACT)
                self.assertEqual(item['errors'], [])
                self.assertEqual(item['problem'], live['problem'])
                self.assertEqual([f['key'] for f in item['fields']], ['field-1'])
                self.assertTrue(item['fields'][0]['readonly_history'])
                self.assertEqual(item['fields'][0]['input_html'],
                                 self.page.locator('.freeResponseTextbox').evaluate('n=>n.outerHTML'))
                self.assertNotIn('correct_value', item['fields'][0])
                item.update({k: source[k] for k in ('math_academy_id', 'sequence_position', 'grade', 'worked_solution')})
                item.update(html_path='/history-' + identity + '.html', extraction_parts=['problem', 'fields', 'solution'])
                self.assertTrue(ActivityCapture._source_binding_matches(live, item))
                key = 'live-' + identity
                records[key] = {'key': key, 'question': live, 'observed_position': item['sequence_position'] - 1,
                                'submissions': []}
                history.append(item)
        capture = ActivityCapture.__new__(ActivityCapture)
        capture.exposures = None
        capture.activity = {'task_id': '14114793', 'kind': 'review'}
        capture.state = {'steps': [], 'presentations': records}
        capture._save = lambda: None
        content = capture._merge_history({'questions': history})
        self.assertEqual(len(content['questions']), 4)
        self.assertEqual(content['source_limitations'], [])
        for q in content['questions']:
            presentations = capture._question_presentations(q)
            self.assertEqual(len(presentations), 1)
            # A rendered history value/overall grade without a verified attempt
            # is not enough to promote a learner response into an answer key.
            unsupported = finalize_answers(q, presentations, {'answers': []})
            with self.assertRaises(UnsupportedContent):
                authoritative_question(unsupported)
            answer = expected[q['math_academy_id']]
            finalized = finalize_answers(q, presentations, {'answers': [
                {'key': 'field-1', 'ma_basis': 'worked_solution', 'ma_value': answer,
                 'value_type': 'math', 'ma_evidence': q['worked_solution']}]})
            self.assertEqual(authoritative_question(finalized)['answer_fields'][0]['correct_value'], answer)
            finalized.update(topic_id=1, knowledge_point_id=str(source_snapshot()['entities'][1][':knowledge-point/id']))
            self.assertFalse(Preparation(source_snapshot()).prepare({'questions': [finalized]})['omissions'])

    def test_history_blanks_exclude_student_answers_and_solution_controls(self):
        item = self.extract('''<div id="q" class="question"><div class="questionText">Ordinary static content
            <div class="freeResponseTextbox">2</div></div></div>''')
        self.assertEqual(item['fields'], [])  # Unscoped static boxes are not controls.
        self.page.set_content('''<div id="question-1" class="question"><div class="questionText">Enter
            <div id="freeResponseTextbox-1" class="freeResponseTextbox"><math><mn>2</mn></math></div></div>
            <div class="studentAnswer"><div class="freeResponseTextbox">999</div><input value="999"></div>
            <div class="questionExplanation"><div class="freeResponseTextbox">888</div></div></div>''')
        item = self.page.locator('#question-1').evaluate(EXTRACT)
        self.assertEqual([field['key'] for field in item['fields']], ['field-1'])
        self.assertEqual(' '.join(item['problem'].split()), 'Enter {{field-1}}')
        self.assertEqual(item['fields'][0]['rendered_text'], '2')
        self.assertNotIn('correct_value', item['fields'][0])
        changed = deepcopy(item)
        changed['fields'].append({'key': 'field-2', 'type': 'blank'})
        self.assertFalse(ActivityCapture._source_binding_matches(item, changed))

    def test_real_prompt_error_then_fieldless_history_recovery_prepares(self):
        before = self.extract('''<div id="q"><div class="questionWidget-text">What is
            <mjx-container></mjx-container>?</div><input type="text"></div>''')
        self.assertEqual(before['extraction_error_parts'], {MATH_ERROR: ['problem']})
        self.assertTrue(before['answer_fields_complete'])
        before.update(math_academy_id='q-11', html_path='/live.html', topic_id=1)
        before['fields'][0].update(correct_value='2', choices=[{'type': 'math', 'value': '2'}],
            evidence={'kind': 'ma_answer', 'value': '2', 'source_file': '/grade.html'})
        after = self.extract('''<div id="q"><div class="questionText">What is
            <math><mn>1</mn><mo>+</mo><mn>1</mn></math>?</div>
            <div class="questionExplanation">The answer is 2.</div></div>''')
        after.update(math_academy_id='q-11', html_path='/history.html')
        self.assertEqual(after['fields'], [])
        self.assertEqual(after['errors'], [])
        merged = ActivityCapture._merge_content({'questions': [before]}, {'questions': [after]})['questions'][0]
        self.assertEqual(merged['errors'], [])
        self.assertTrue(merged['answer_fields_complete'])
        self.assertEqual(len(merged['answer_fields']), 1)
        self.assertFalse(prepare(merged)['omissions'])
        self.assertIn('$1+1$', merged['problem'])

    def test_real_history_merge_recovers_same_prompt_without_attaching_history_grade(self):
        before = self.extract('''<div id="q"><div class="questionWidget-text">What is
            <math><unsupported>1</unsupported></math>?</div><input type="text"></div>''')
        before.update(math_academy_id='q-11', html_path='/live.html', topic_id=1)
        before['fields'][0].update(correct_value='1', choices=[{'type': 'math', 'value': '1'}],
            evidence={'kind': 'ma_answer', 'value': '1', 'source_file': '/source-answer.html'})
        after = self.extract('''<div id="q"><div class="questionText">What is
            <math><mn>1</mn></math>?</div><div class="questionExplanation">The answer is 1.</div></div>''')
        after.update(math_academy_id='q-11', html_path='/history.html', grade='Correct', sequence_position=1)
        self.assertEqual(before['problem'], after['problem'])
        self.assertTrue(before['errors'])
        record = {'key': 'live', 'question': before, 'observed_position': 0,
                  'submissions': [{'outcome': 'observe_to_confirm', 'responses': [{'key': 'field-1', 'value': '9'}]}]}
        capture = ActivityCapture.__new__(ActivityCapture)
        capture.exposures = None
        capture.activity = {'task_id': '1', 'kind': 'diagnostic'}
        capture.state = {'steps': [], 'presentations': {'live': record}}
        capture._save = lambda: None
        content = capture._merge_history({'questions': [after]})
        self.assertEqual(len(content['questions']), 1)
        merged = content['questions'][0]
        self.assertEqual(merged['errors'], [])
        self.assertFalse(content['source_limitations'])
        self.assertNotIn('feedback', record)
        self.assertEqual(merged['answer_fields'][0]['correct_value'], '1')
        self.assertFalse(prepare(merged)['omissions'])

    def test_choice_and_solution_errors_have_separate_scopes(self):
        item = self.extract('''<div id="q"><div class="questionText">Choose one.</div>
            <select><option>a</option><option>b</option></select>
            <div class="questionExplanation"><math><maligngroup>2</maligngroup></math></div></div>''')
        self.assertEqual(item['extraction_error_parts'], {SOLUTION_ERROR: ['solution']})
        self.assertTrue(item['answer_fields_complete'])
        self.assertTrue(item['fields'][0]['choices_complete'])
        item = self.extract('''<div id="q"><div class="questionText">Choose.</div>
            <table class="questionWidget-choicesTable"><tr><td><span class="choiceLetterCircle" id="a">a</span>
            <span class="choiceText"><mjx-container></mjx-container></span></td></tr></table>
            <div class="questionExplanation"><mjx-container></mjx-container></div></div>''')
        self.assertEqual(item['extraction_error_parts'], {MATH_ERROR: ['fields', 'solution']})
        self.assertFalse(item['answer_fields_complete'])

    def test_adapter_attaches_asset_failures_to_their_observed_section(self):
        self.page.set_content('''<div id="q"><div class="questionText">Prompt <img src="data:image/png;base64,AA=="></div>
            <div class="questionExplanation">Solution <canvas></canvas></div></div>''')
        with tempfile.TemporaryDirectory() as directory:
            adapter = MathAcademyBrowser(SimpleNamespace(timeout_ms=1000), threading.Event())
            adapter.page = self.page
            def collect(item, *args, **kwargs):
                for asset in item['assets']:
                    identity = asset.get('source_url') or 'read:' + str(asset['index'])
                    item['errors'].append('Graphic rendering unavailable: ' + identity)
                return item
            with patch.object(adapter.assets, 'collect', side_effect=collect), patch.object(adapter, '_screenshot'):
                item = adapter._read(self.page.locator('#q'), Path(directory), 'read')
            scopes = item['extraction_error_parts']
            self.assertEqual(scopes['Graphic rendering unavailable: data:image/png;base64,AA=='], ['problem'])
            self.assertEqual(scopes['Graphic rendering unavailable: read:1'], ['solution'])


if __name__ == '__main__':
    unittest.main()
