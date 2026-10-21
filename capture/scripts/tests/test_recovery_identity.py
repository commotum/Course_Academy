"""Historical rereads clear failures only under a verified source-root identity."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.recovery import _verified_recovery_identity, reextract_record, version


REPO = Path(__file__).resolve().parents[3]
FIXTURE = Path(__file__).parent / 'fixtures/q343408-recovery.json'
ERROR = 'Select frame has no ID: selectList-999-0'


class RecoveryIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.playwright = sync_playwright().start()
        try:
            cls.browser = cls.playwright.chromium.launch(headless=True)
        except Exception:
            cls.playwright.stop()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.context.route('**/*', lambda route: route.abort())
        self.page = self.context.new_page()
        self.temp = tempfile.TemporaryDirectory()
        self.repair = Path(self.temp.name)

    def tearDown(self):
        self.context.close()
        self.temp.cleanup()

    def test_solution_only_reread_keeps_unread_prompt_image_binding(self):
        asset = {'index':0, 'tag':'img', 'path':'/original/diagram.png',
                 'source_url':'https://mathacademy.com/graphics/q-42', 'extraction_part':'problem'}
        record = {'math_academy_id':'q-42', 'dom_id':'questionExplanation-42',
            'problem':'![](/original/diagram.png) Find x.', 'assets':[asset],
            'worked_solution':'Old explanation.', 'extraction_parts':['problem','solution'],
            'html':'<div id="questionExplanation-42" class="questionExplanation"><p>The answer is 2.</p></div>'}
        original = deepcopy(record)
        recovered = reextract_record(record,self.page,self.repair,history=True)
        self.assertEqual(recovered['problem'],original['problem'])
        self.assertEqual(recovered['assets'],[asset])
        self.assertIn('The answer is 2.',recovered['worked_solution'])
        self.assertEqual(record,original)

    def test_actual_no_credit_history_retires_old_frame_errors_preserving_originals(self):
        fixture = json.loads(FIXTURE.read_text())
        record = fixture['record']
        source = REPO / 'reference/mathacademy/capture/multivariable/14111253/observations' / Path(record['html_path']).name
        record['html_path'] = str(source)
        original = deepcopy(record)
        raw = source.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), fixture['source_sha256'])
        recovered = reextract_record(record, self.page, self.repair, history=True)
        self.assertEqual(recovered['math_academy_id'], 'q-343408')
        self.assertEqual(recovered['errors'], [])
        self.assertTrue(recovered['answer_fields_complete'])
        self.assertEqual([len(field['choices']) for field in recovered['fields']], [4, 2, 4, 4])
        self.assertTrue(all(field['disabled'] and field['frame_id'] for field in recovered['fields']))
        history = recovered['extraction_error_history'][-1]
        self.assertEqual(history['errors'], original['errors'])
        self.assertEqual(history['source']['html_path'], str(source))
        self.assertEqual(history['replaced_by']['html_path'], recovered['html_path'])
        self.assertEqual(Path(recovered['html_path']).read_bytes(), raw)
        self.assertEqual(source.read_bytes(), raw)
        self.assertEqual(record, original)

    def test_conflicting_saved_identity_refuses_before_evidence_or_merge(self):
        record = {'dom_id': 'step-q999', 'math_academy_id': 'q-998',
                  'html': '<div id="step-q999"><div class="questionWidget-text">Source problem.</div></div>'}
        original = deepcopy(record)
        with self.assertRaisesRegex(ValueError, 'conflicts with its DOM root'):
            reextract_record(record, self.page, self.repair)
        self.assertEqual(record, original)
        self.assertEqual(list(self.repair.iterdir()), [])

    def test_generic_diagnostic_root_never_binds_from_control_or_saved_id(self):
        markup = '''<div id="questionContainer"><div class="questionWidget-text">Choose
          <select id="selectList-999-0"><option>One</option><option>Two</option></select>
          </div></div>'''
        for saved in (None, 'q-999'):
            with self.subTest(saved=saved):
                record = {'dom_id': 'questionContainer', 'html': markup, 'errors': [ERROR],
                          'extraction_parts': ['problem', 'fields'],
                          'extraction_error_parts': {ERROR: ['fields']},
                          'fields': [{'key': 'field-1', 'type': 'select'}]}
                if saved:
                    record['math_academy_id'] = saved
                recovered = reextract_record(record, self.page, self.repair)
                self.assertEqual(recovered['errors'], [ERROR])
                self.assertTrue(recovered['answer_fields_complete'])
                if saved:
                    self.assertEqual(recovered['math_academy_id'], saved)
                else:
                    self.assertNotIn('math_academy_id', recovered)
                self.assertNotIn('extraction_error_history', recovered)

    def test_numbered_live_root_without_saved_identity_stays_unbound(self):
        record = {'dom_id': 'question-12', 'html': '<div id="question-12">Diagnostic question 12.</div>'}
        self.assertNotIn('math_academy_id', reextract_record(record, self.page, self.repair))

    def test_stable_roots_require_saved_and_actual_root_agreement(self):
        for root, saved, history, expected in (
            ('step-q17', None, False, 'q-17'), ('step-e18', 'e-18', False, 'e-18'),
            ('questionExplanation-19', None, False, 'q-19'), ('question-20', 'q-20', True, 'q-20'),
            ('question-21', None, True, 'q-21'), ('questionContainer', 'q-22', True, None),
        ):
            with self.subTest(root=root):
                record = {'dom_id': root}
                if saved:
                    record['math_academy_id'] = saved
                self.assertEqual(_verified_recovery_identity(record, {'dom_id': root}, root, history=history), expected)
        for record, parsed, actual in (
            ({'dom_id': 'step-q17'}, {'dom_id': 'step-q18'}, 'step-q18'),
            ({'dom_id': 'step-q17'}, {'dom_id': 'step-q18'}, 'step-q17'),
            ({'dom_id': 'step-e17', 'math_academy_id': 'q-17'}, {'dom_id': 'step-e17'}, 'step-e17'),
        ):
            with self.subTest(record=record, actual=actual), self.assertRaises(ValueError):
                _verified_recovery_identity(record, parsed, actual)


class RecoveryVersionTests(unittest.TestCase):
    def test_recovery_and_markdown_changes_invalidate_the_selected_recovery_cache(self):
        baseline = version()
        read_bytes = Path.read_bytes
        for dependency in ('recovery.py', 'database/text.py'):
            with self.subTest(dependency=dependency):
                def changed(path):
                    data = read_bytes(path)
                    return data + b'\n# changed dependency\n' if path == REPO / 'capture/scripts' / dependency else data
                with patch.object(Path, 'read_bytes', changed):
                    self.assertNotEqual(version(), baseline)
        self.assertEqual(version(), baseline)
