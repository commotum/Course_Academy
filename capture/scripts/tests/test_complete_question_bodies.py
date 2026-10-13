"""Regression evidence from the completeness audit, with all network blocked."""
import json
from pathlib import Path
import unittest
from scripts.browser.adapter import EXTRACT
from scripts.activity.capture import ActivityCapture

ROOT = Path(__file__).resolve().parents[3] / 'reference/mathacademy/capture'

class CompleteBodyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(headless=True)
    @classmethod
    def tearDownClass(cls):
        cls.browser.close(); cls.pw.stop()
    def setUp(self):
        self.context = self.browser.new_context()
        self.context.route('**/*', lambda route: route.abort())
        self.page = self.context.new_page()
        self.addCleanup(self.context.close)
    def records(self, task, mid):
        cp = json.loads((ROOT/'linear'/task/'checkpoint.json').read_text())
        history = next(q for q in cp['history']['questions'] if q.get('math_academy_id') == mid)
        live = next(p['question'] for p in cp['presentations'].values()
                    if p['question'].get('dom_id') == 'step-' + mid.replace('-', ''))
        return live, history
    def extract(self, q, history=False):
        self.page.set_content(q['html'])
        return self.page.locator('[id="'+q['dom_id']+'"]').evaluate(EXTRACT, {'history_grade': q.get('grade')} if history else {})
    def test_complete_history_proof_keeps_all_reasoning_and_field_positions(self):
        live, history = self.records('14114805', 'q-221707')
        after = self.extract(history, True)
        self.assertIn('counterexample', after['problem'])
        self.assertEqual(len(after['fields']), 9)
        self.assertTrue(after['answer_fields_complete'])
        self.assertEqual(after['errors'], [])
        for field in after['fields']:
            self.assertEqual(after['problem'].count('{{'+field['key']+'}}'), 1)
        self.assertTrue(ActivityCapture._source_binding_matches(self.extract(live), after))
    def test_field_grades_alone_do_not_finish_a_proof_and_hidden_stage_is_incomplete(self):
        _, history = self.records('14114805', 'q-221707')
        self.assertFalse(self.extract(history)['answer_fields_complete'])
        self.page.locator('.proofSection').last.evaluate("n => n.style.display='none'")
        after = self.page.locator('[id="'+history['dom_id']+'"]').evaluate(EXTRACT, {'history_grade':'Correct'})
        self.assertFalse(after['answer_fields_complete'])
    def test_truth_table_and_each_answer_position_survive(self):
        _, history = self.records('14109722', 'q-182663')
        after = self.extract(history, True)
        self.assertIn('| ---', after['problem'])
        self.assertIn('P', after['problem'])
        self.assertIn('Q', after['problem'])
        self.assertEqual(len(after['fields']), 4)
        self.assertEqual(len(after['problem_field_keys']), 4)
        for field in after['fields']:
            self.assertEqual(after['problem'].count('{{'+field['key']+'}}'), 1)
    def test_matrix_proof_tables_do_not_repeat_nested_rows(self):
        live, history = self.records('14114643', 'q-363823')
        before, after = self.extract(live), self.extract(history, True)
        self.assertIn('orthogonal', after['problem'])
        self.assertTrue(after['answer_fields_complete'])
        for field in after['fields']:
            self.assertEqual(after['problem'].count('{{'+field['key']+'}}'), 1)
        self.assertTrue(ActivityCapture._source_binding_matches(before, after))
    def test_nested_body_renders_prompt_once_and_excludes_grading(self):
        self.page.set_content('''<div id="q"><div class="questionWidget-body"><p class="questionWidget-text">Unique prompt.</p>
        <p>Choose <select><option>A</option><option>B</option></select>.</p>
        <div class="questionWidget-result">Correct</div><div class="questionWidget-explanation">Private explanation.</div></div></div>''')
        after = self.page.locator('#q').evaluate(EXTRACT)
        self.assertEqual(after['problem'].count('Unique prompt.'), 1)
        self.assertNotIn('Correct', after['problem'])
        self.assertNotIn('Private explanation', after['problem'])
    def test_no_credit_history_selects_keep_the_original_controls(self):
        cp = json.loads((ROOT/'multivariable'/'14111253'/'checkpoint.json').read_text())
        history = next(q for q in cp['history']['questions'] if q.get('math_academy_id') == 'q-343408')
        self.assertEqual(history['grade'], 'No Credit')
        after = self.extract(history, True)
        self.assertEqual(after['errors'], [])
        self.assertEqual(len(after['fields']), 4)
        self.assertTrue(all(f.get('frame_id') and len(f['choices']) > 1 for f in after['fields']))
        self.assertTrue(after['answer_fields_complete'])
        self.page.locator('.proofSection').last.evaluate("n => n.style.display='none'")
        hidden = self.page.locator('#question-343408').evaluate(EXTRACT, {'history_grade':'No Credit'})
        self.assertFalse(hidden['answer_fields_complete'])

    def test_real_nullcline_question_matches_despite_paragraph_wrapper_spacing(self):
        cp = json.loads((ROOT/'multivariable'/'14118584'/'checkpoint.json').read_text())
        history = next(q for q in cp['history']['questions'] if q.get('math_academy_id') == 'q-332651')
        live = next(p['question'] for p in cp['presentations'].values() if p['question'].get('math_academy_id') == 'q-332651')
        before, after = self.extract(live), self.extract(history, True)
        self.assertTrue(ActivityCapture._source_binding_matches(before, after))

    def test_hidden_proof_stage_ancestor_is_not_complete(self):
        self.page.set_content('''<div id="question-1" class="question"><div class="questionText">Choose.</div>
            <div class="questionBody" style="display:none"><div class="proofSection">
            <div class="selectList" id="selectList-1-0"><div class="selectListFrameDisabled" id="frame-1">A</div>
            <div class="selectListOptions"><div class="selectListOption">A</div><div class="selectListOption">B</div></div>
            </div></div></div></div>''')
        node=self.page.locator('#question-1')
        self.assertFalse(node.evaluate(EXTRACT, {'history_grade':'No Credit'})['answer_fields_complete'])
        self.page.locator('.questionBody').evaluate("n => n.style.display='block'")
        self.assertTrue(node.evaluate(EXTRACT, {'history_grade':'No Credit'})['answer_fields_complete'])
