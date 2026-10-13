"""Only exact own solution originals can retire a failed raster history alias."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import threading
import unittest
from unittest.mock import Mock

from scripts.browser.assets import AssetCapture, solution_image_bindings
from scripts.browser.adapter import MathAcademyBrowser
from scripts.config import Config
from scripts.storage import read_json


REPO = Path(__file__).resolve().parents[3]


class SolutionAliasRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        fixture = json.loads((Path(__file__).parent / 'fixtures/q226134-solution-alias.json').read_text())
        self.current, self.prior = fixture['current'], fixture['prior']
        asset = self.prior['assets'][0]
        source = REPO / 'reference/mathacademy/capture/multivariable/14123192/assets' / Path(asset['path']).name
        self.original = source.read_bytes()
        self.assertEqual(hashlib.sha256(self.original).hexdigest(), asset['sha256'])
        path = self.directory / source.name
        path.write_bytes(self.original)
        self.prior['worked_solution'] = self.prior['worked_solution'].replace(asset['path'], str(path))
        asset['path'] = str(path)
        self.url = self.current['assets'][0]['source_url']
        self.browser = SimpleNamespace(config=SimpleNamespace(timeout_ms=1000, retry_delay=0),
            image_responses={}, context=SimpleNamespace(request=Mock()))
        # The actual alias returned non-image bytes; no request is made in tests.
        self.browser.context.request.get.return_value = SimpleNamespace(ok=True, status=200,
            body=lambda: b'', headers={'content-type': ''})
        self.capture = AssetCapture(self.browser)
        self.capture._rendered_assets = Mock(return_value={0: {'error': 'Image did not load'}})
        self.capture._sleep = Mock()

    def test_actual_q226134_alias_restores_original_evidence_without_claiming_dom_readiness(self):
        prior = deepcopy(self.prior)
        self.current['errors'] = ['Independent source failure']
        recovered = self.capture.collect(self.current, Mock(), self.directory, 'history-solution-q-226134', self.prior)
        asset = recovered['assets'][0]
        self.assertEqual(Path(asset['path']).read_bytes(), self.original)
        self.assertEqual(asset['sha256'], self.prior['assets'][0]['sha256'])
        self.assertEqual(recovered['errors'], ['Independent source failure'])
        self.assertNotIn('unavailable', asset)
        self.assertNotIn('render_unavailable', asset)
        self.assertNotIn('render_ready', asset)
        self.assertEqual(asset['source_url'], self.url)
        self.assertEqual(asset['recovered_from']['render_failure'], 'Image did not load')
        validation = asset['original_image_validation']
        self.assertEqual(validation['question_id'], 'q-226134')
        self.assertEqual(validation['format'], 'PNG')
        self.assertTrue(all(size > 0 for size in validation['dimensions']))
        history = recovered['extraction_error_history'][-1]
        self.assertEqual(history['failed_source_url'], self.url)
        self.assertEqual(history['source_dom_id'], 'questionExplanation-226134')
        self.assertEqual(history['errors'], ['Graphic rendering unavailable: ' + self.url])
        self.assertEqual(self.prior, prior)
        self.assertEqual(recovered['worked_solution'], self.prior['worked_solution'])

    def test_wrong_or_missing_identity_never_recovers(self):
        variants = [('current', 'dom_id', 'questionExplanation-1'), ('current', 'dom_id', 'questionContainer'),
                    ('current', 'math_academy_id', 'q-1'), ('prior', 'math_academy_id', 'q-1'),
                    ('prior', 'dom_id', 'step-q1')]
        for target, key, value in variants:
            with self.subTest(target=target, key=key):
                current, prior = deepcopy(self.current), deepcopy(self.prior)
                (current if target == 'current' else prior)[key] = value
                self.assertEqual(solution_image_bindings(current, prior), {})
        current = deepcopy(self.current)
        current['assets'][0]['source_url'] = 'https://mathacademy.com/graphics/q-1-e-0'
        self.assertEqual(solution_image_bindings(current, self.prior), {})

    def test_choice_and_solution_can_share_bytes_without_losing_occurrence_identity(self):
        prior = deepcopy(self.prior)
        choice = {**prior['assets'][0], 'extraction_part':'fields','source_url':'https://mathacademy.com/graphics/q-226134-a-1'}
        prior['assets'].insert(0,choice)
        recovered = self.capture.collect(deepcopy(self.current),Mock(),self.directory,'history',prior)
        self.assertEqual(recovered['assets'][0]['sha256'],self.prior['assets'][0]['sha256'])
        self.assertEqual(recovered['assets'][0]['source_url'],self.url)
        self.assertNotIn('unavailable',recovered['assets'][0])
        self.assertEqual(prior['assets'][0],choice)

    def test_changed_complete_solution_or_image_count_cannot_reuse_original(self):
        for changed in (self.current['worked_solution'].replace('=16.', '=17.'),
                        self.current['worked_solution'] + '\n![](@asset-0@)'):
            with self.subTest(solution=changed[-40:]):
                self.assertEqual(solution_image_bindings({**self.current, 'worked_solution': changed}, self.prior), {})
        prior = deepcopy(self.prior)
        prior['assets'].append(deepcopy(prior['assets'][0]))
        self.assertEqual(solution_image_bindings(self.current, prior), {})

    def test_corrupt_digest_or_full_png_decode_failure_preserves_alias_error(self):
        for corrupt_digest in (True, False):
            with self.subTest(corrupt_digest=corrupt_digest):
                prior = deepcopy(self.prior)
                if corrupt_digest:
                    prior['assets'][0]['sha256'] = 'incorrect'
                else:
                    bad = self.directory / 'truncated.png'
                    data = self.original[:50]
                    bad.write_bytes(data)
                    previous = prior['assets'][0]['path']
                    prior['assets'][0].update(path=str(bad), sha256=hashlib.sha256(data).hexdigest())
                    prior['worked_solution'] = prior['worked_solution'].replace(previous, str(bad))
                recovered = self.capture.collect(deepcopy(self.current), Mock(), self.directory, 'invalid', prior)
                self.assertIn('unavailable', recovered['assets'][0])
                self.assertIn('render_unavailable', recovered['assets'][0])
                self.assertNotIn('extraction_error_history', recovered)

    def test_unavailable_prior_or_non_original_representation_never_restores(self):
        for key, value in (('unavailable', 'missing'), ('render_unavailable', 'not rendered'),
                           ('representation', 'canvas_render'), ('tag', 'canvas'), ('tag', 'svg'),
                           ('extraction_part', 'problem')):
            with self.subTest(key=key, value=value):
                prior = deepcopy(self.prior)
                prior['assets'][0][key] = value
                self.assertEqual(solution_image_bindings(self.current, prior), {})

    def test_current_canvas_and_svg_keep_render_failures(self):
        for tag in ('canvas', 'svg'):
            with self.subTest(tag=tag):
                current = deepcopy(self.current)
                current['assets'][0].update(tag=tag, html='<svg><circle r="1"/></svg>')
                recovered = self.capture.collect(current, Mock(), self.directory, tag, self.prior)
                self.assertIn('render_unavailable', recovered['assets'][0])
                self.assertIn('Graphic rendering unavailable: ' + self.url, recovered['errors'])
                self.assertNotIn('extraction_error_history', recovered)

    def test_owning_history_question_keeps_actual_alias_recovery_history_and_deduplicates(self):
        from playwright.sync_api import sync_playwright
        solution = self.capture.collect(deepcopy(self.current), Mock(), self.directory, 'history-solution-q-226134', self.prior)
        solution['html_path'] = 'original-solution-source.html'
        alias_history = solution['extraction_error_history'][0]
        question_history = {'errors': ['Earlier independent prompt failure'], 'parts': ['problem'],
                            'source_dom_id': 'question-226134'}
        # One prior alias record already exists in the owning source; reading
        # the solution must retain it once and append its distinct records.
        solution['extraction_error_history'].append({'errors': ['Earlier distinct solution failure'], 'parts': ['solution']})
        owning = {'problem': 'Own source prompt', 'worked_solution': '', 'fields': [], 'assets': [],
                  'errors': [], 'html_path': 'original-question-source.html',
                  'extraction_error_history': [question_history, deepcopy(alias_history)]}
        originals = deepcopy((owning, solution))
        adapter = MathAcademyBrowser(Config(repo_root=self.directory), threading.Event())
        adapter.state = {'task_id': '1'}
        adapter._goto = Mock()
        adapter._settle_content = Mock()
        adapter._evidence = Mock(return_value={})
        adapter._read = Mock(side_effect=lambda node, *a, **kw:
                             deepcopy(solution if node.get_attribute('id') == 'questionExplanation-226134' else owning))
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context()
            context.route('**/*', lambda route: route.abort())
            try:
                adapter.page = context.new_page()
                adapter.page.set_content('<div class="question" id="question-226134"><div class="questionText">Own source prompt</div>'
                    '<span class="answerResult">Correct</span><div class="questionExplanation" id="questionExplanation-226134">Own solution</div></div>')
                result = adapter.history({'task_id': '1', 'kind': 'review'}, self.directory)
            finally:
                context.close()
                browser.close()
        question = result['questions'][0]
        self.assertEqual(question['math_academy_id'], 'q-226134')
        self.assertEqual(question['extraction_error_history'], [question_history, alias_history, solution['extraction_error_history'][1]])
        self.assertEqual(question['assets'][0]['original_image_validation']['question_id'], 'q-226134')
        self.assertNotIn('render_ready', question['assets'][0])
        self.assertEqual(read_json(self.directory / 'history-content.json')['questions'][0]['extraction_error_history'], question['extraction_error_history'])
        self.assertEqual((owning, solution), originals)
