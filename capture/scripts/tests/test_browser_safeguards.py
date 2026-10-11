"""Offline regressions for browser timing and recovery restored from capture v1."""
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
import tempfile
import threading
import time
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from scripts.browser.adapter import BrowserUnavailable, EXTRACT, MathAcademyBrowser
from scripts.browser.safety import BrowserSafety, deduplicate_math_editor, retry_after_seconds


class BrowserSafetyTests(unittest.TestCase):
    def test_retry_after_numeric_and_http_date(self):
        self.assertEqual(retry_after_seconds('120', now=100), 120)
        date = format_datetime(datetime.fromtimestamp(220, timezone.utc), usegmt=True)
        self.assertEqual(retry_after_seconds(date, now=100), 120)
        self.assertEqual(retry_after_seconds('bad', now=100), 30)
        for invalid in ('inf', '-inf', 'nan'):
            self.assertEqual(retry_after_seconds(invalid, now=100), 30)

    def test_duplicate_editor_tags_only_identical_and_same_version(self):
        script = '<script src="/js/math-editor.js?v=1"></script>'
        distinct = '<script defer src="/js/math-editor.js?v=1"></script>'
        self.assertEqual(deduplicate_math_editor(script + distinct + script), script + distinct)
        self.assertIn('?v=2', deduplicate_math_editor(script + '<script src="/js/math-editor.js?v=2"></script>'))

    def test_xhr_cooldown_survives_browser_recreation_and_bounds_deadline(self):
        with tempfile.TemporaryDirectory() as directory:
            config = SimpleNamespace(timeout_ms=1000, state_root=Path(directory), output_root=Path(directory))
            browser = MathAcademyBrowser(config, threading.Event())
            response = SimpleNamespace(url='https://mathacademy.com/api/answer', status=429, headers={'retry-after': '120'},
                                       request=SimpleNamespace(resource_type='xhr'), ok=False)
            browser._response(response)
            resumed = MathAcademyBrowser(config, threading.Event())
            self.assertGreater(resumed.safety.remaining_cooldown(), 119)
            resumed.set_deadline(time.time() + 10)
            with self.assertRaises(BrowserUnavailable) as raised:
                resumed._wait_cooldown()
            self.assertGreater(raised.exception.retry_after, 119)
            self.assertTrue((Path(directory) / 'browser-cooldown.json').exists())

    def test_document_repair_preserves_raw_bytes_and_redirects(self):
        with tempfile.TemporaryDirectory() as directory:
            browser = MathAcademyBrowser(SimpleNamespace(timeout_ms=1000, output_root=Path(directory)), threading.Event())
            script = '<script src="/js/math-editor.js"></script>'
            original = ('<!doctype html>' + script + script).encode()
            route = Mock()
            route.request = SimpleNamespace(resource_type='document', method='GET', url='https://mathacademy.com/learn')
            response = SimpleNamespace(status=200, headers={'content-type': 'text/html'}, body=lambda: original)
            route.fetch.return_value = response
            browser.safety.repair_document(route)
            self.assertEqual(route.fulfill.call_args.kwargs['body'].count('/js/math-editor.js'), 1)
            originals = list((Path(directory) / 'browser-originals').glob('*.html'))
            self.assertEqual(originals[0].read_bytes(), original)
            self.assertTrue(originals[0].with_suffix('.json').exists())
            response.status = 302
            route.fulfill.reset_mock()
            browser.safety.repair_document(route)
            route.fulfill.assert_called_once_with(response=response)
            self.assertEqual(route.fetch.call_args.kwargs['max_redirects'], 0)

    def test_failed_document_route_always_released(self):
        browser = MathAcademyBrowser(SimpleNamespace(timeout_ms=1000), threading.Event())
        route = Mock()
        route.request = SimpleNamespace(resource_type='document', method='GET', url='https://mathacademy.com/learn')
        route.fetch.side_effect = RuntimeError('net::ERR_CONNECTION_RESET')
        browser.safety.repair_document(route)
        route.abort.assert_called_once_with('failed')
        self.assertEqual(browser.safety.events[-1]['reason'], 'net::ERR_CONNECTION_RESET')

    def test_font_screenshot_failure_retries_without_hiding_other_errors(self):
        browser = MathAcademyBrowser(SimpleNamespace(timeout_ms=1000), threading.Event())
        target = Mock()
        target.screenshot.side_effect = [RuntimeError('Timeout waiting for fonts'), b'png']
        with patch.object(browser.pacer, 'sleep'):
            self.assertEqual(browser._screenshot(target), b'png')
        self.assertEqual(target.screenshot.call_count, 2)
        target.screenshot.side_effect = RuntimeError('page closed')
        with self.assertRaisesRegex(RuntimeError, 'page closed'):
            browser._screenshot(target)

    def test_launch_and_cdp_enforce_minimum_500ms_latency(self):
        from playwright.sync_api import sync_playwright
        for cdp in (None, 'http://127.0.0.1:9222'):
            with self.subTest(cdp=cdp), tempfile.TemporaryDirectory() as directory:
                config = SimpleNamespace(timeout_ms=1000, browser_cdp_url=cdp, profile=Path(directory), headless=True,
                                         ui_delay_ms=10)
                runtime = Mock()
                context = Mock()
                page = Mock(url='https://mathacademy.com/learn')
                context.pages = [page]
                runtime.chromium.launch_persistent_context.return_value = context
                runtime.chromium.connect_over_cdp.return_value.contexts = [context]
                with patch('playwright.sync_api.sync_playwright') as start:
                    start.return_value.start.return_value = runtime
                    with MathAcademyBrowser(config, threading.Event()):
                        pass
                method = runtime.chromium.connect_over_cdp if cdp else runtime.chromium.launch_persistent_context
                self.assertEqual(method.call_args.kwargs['slow_mo'], 500)


class OfflineTimingTests(unittest.TestCase):
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
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.context = self.browser.new_context()
        self.context.route('**/*', lambda route: route.abort())
        self.addCleanup(self.context.close)
        self.page = self.context.new_page()
        self.page.set_default_timeout(1500)
        self.adapter = MathAcademyBrowser(SimpleNamespace(timeout_ms=1500), threading.Event())
        self.adapter.page, self.adapter.context, self.adapter.directory = self.page, self.context, self.directory
        self.adapter.activity = {'task_id': 'offline', 'kind': 'diagnostic'}

    def test_reused_diagnostic_container_rejects_old_question(self):
        self.page.set_content('''<div id="questionContainer"><div class="questionWidget-title">Question 2</div>
          <div class="questionWidget-text">Second question</div><input id="answer">
          <button class="questionWidget-submitButton" onclick="window.clicked=true">Submit</button></div>''')
        current = self.adapter._view()
        current['key'] = 'diagnostic-1'
        result = self.adapter.respond(current, [{'key': 'field-1', 'value': '4'}], self.directory)
        self.assertTrue(result['not_submitted'])
        self.assertEqual(self.page.locator('#answer').input_value(), '')
        self.assertIsNone(self.page.evaluate('window.clicked'))

    def test_same_diagnostic_title_but_changed_prompt_is_reobserved(self):
        self.page.set_content('''<div id="questionContainer"><div class="questionWidget-title">Question 2</div>
          <div class="questionWidget-text">Second question</div><input id="answer">
          <button class="questionWidget-submitButton">Submit</button></div>''')
        current = self.adapter._view()
        current['question'] = self.page.locator('#questionContainer').evaluate(EXTRACT)
        self.page.locator('.questionWidget-text').evaluate("n=>n.textContent='Changed question'")
        result = self.adapter.respond(current, [{'key': 'field-1', 'value': '4'}], self.directory)
        self.assertTrue(result['not_submitted'])
        self.assertEqual(self.page.locator('#answer').input_value(), '')

    def test_changed_prompt_during_pre_entry_evidence_is_not_answered(self):
        self.page.set_content('''<div id="questionContainer"><div class="questionWidget-title">Question 2</div>
          <div class="questionWidget-text">Original question</div><input id="answer">
          <button class="questionWidget-submitButton">Submit</button></div>''')
        observation = self.adapter._view()
        observation['question'] = self.page.locator('#questionContainer').evaluate(EXTRACT)
        def read_after_change(scope, *args):
            self.page.locator('.questionWidget-text').evaluate("n=>n.textContent='Changed question'")
            return scope.evaluate(EXTRACT)
        with patch.object(self.adapter, '_read', side_effect=read_after_change):
            result = self.adapter.respond(observation, [{'key': 'field-1', 'value': '4'}], self.directory)
        self.assertTrue(result['not_submitted'])
        self.assertEqual(self.page.locator('#answer').input_value(), '')

    def test_assessment_prompt_change_during_evidence_is_not_marked_filled(self):
        self.adapter.activity['kind'] = 'assessment'
        self.page.set_content('''<div id="questions"><div class="question" id="question-1">
          <div class="questionText">Original question</div><input id="answer"></div></div>''')
        observation = self.adapter.observe(self.directory)
        def evidence(*args):
            self.page.locator('.questionText').evaluate("n=>n.textContent='Changed question'")
        with patch.object(self.adapter, '_evidence', side_effect=evidence):
            result = self.adapter.respond(observation, [{'key': 'field-1', 'value': '4'}], self.directory)
        self.assertTrue(result['not_submitted'])
        self.assertFalse(self.adapter.state['assessment_filled'])

    def test_initial_500ms_math_poll_is_checked_before_accepting_entry(self):
        self.page.set_content('''<div id="q"><div class="matheditor-wrapper-answer"><span class="mq-editable-field">
          <span class="mq-textarea"><textarea></textarea></span></span></div></div>
          <script>window.value='4';window.MathQuill=n=>({latex:()=>window.value});
          setTimeout(()=>window.value='5',500);</script>''')
        question = {'fields': [{'key': 'value', 'type': 'blank', 'tag': 'mathquill', 'dom_index': 0}]}
        with self.assertRaisesRegex(ValueError, 'value changed'):
            self.adapter._settle_entry(self.page.locator('#q'), question, [{'key': 'value', 'value': '4'}])

    def test_after_evidence_value_change_cannot_submit(self):
        self.adapter.activity['kind'] = 'review'
        self.page.set_content('''<div class="step questionWidget" id="step-q1">
          <div class="questionWidget-text">Find x</div><input id="answer">
          <button class="questionWidget-submitButton" onclick="window.clicked=true">Submit</button></div>''')
        current = self.adapter._view()
        current['question'] = self.page.locator('#step-q1').evaluate(EXTRACT)
        def evidence(*args):
            self.page.locator('#answer').fill('5')
        with patch.object(self.adapter, '_evidence', side_effect=evidence):
            with self.assertRaisesRegex(ValueError, 'changed before submission'):
                self.adapter.respond(current, [{'key': 'field-1', 'value': '4'}], self.directory)
        self.assertIsNone(self.page.evaluate('window.clicked'))

    def test_graded_explanation_waits_for_math_then_captures_it(self):
        self.page.set_content('''<div id="questionContainer"><div class="questionWidget-title">Question 2</div>
          <div class="questionWidget-text">Find x</div><div class="questionWidget-result">Correct</div>
          <div class="questionWidget-explanation"><mjx-container></mjx-container></div></div>''')
        self.assertFalse(self.adapter._view()['ready'])
        self.page.evaluate("() => setTimeout(()=>document.querySelector('mjx-container').innerHTML='<mjx-assistive-mml><math><mn>4</mn></math></mjx-assistive-mml>',100)")
        observation = self.adapter.observe(self.directory)
        self.assertTrue(observation['accepted'])
        self.assertIn('4', observation['worked_solution'])

    def test_permanently_incomplete_graded_math_preserves_error_and_progress(self):
        self.adapter.config.timeout_ms = 100
        self.page.set_content('''<div id="questionContainer"><div class="questionWidget-title">Question 2</div>
          <div class="questionWidget-text">Find x</div><div class="questionWidget-result">Correct</div>
          <div class="questionWidget-explanation"><mjx-container></mjx-container></div></div>''')
        observation = self.adapter.observe(self.directory)
        self.assertTrue(observation['accepted'])
        self.assertTrue(observation['readiness_errors'])
        self.assertTrue(observation['question']['errors'])

    def test_empty_tutorial_header_and_continue_are_not_instructional_content(self):
        self.page.set_content('''<div class="step" id="step-t1"><span class="stepName">Tutorial</span>
          <button id="continueButton-t1">Continue</button></div>''')
        self.assertFalse(self.adapter._view()['ready'])

    def test_history_keeps_explanation_extraction_errors(self):
        self.adapter.activity['kind'] = 'review'
        self.page.set_content('''<div class="question" id="question-1"><div class="questionText">Find x</div>
          <span class="answerResult">Correct</span></div><div class="questionExplanation" id="questionExplanation-1">Solution</div>''')
        def read(scope, *args, **kwargs):
            is_solution = scope.get_attribute('id') == 'questionExplanation-1'
            return {'problem': 'Find x', 'worked_solution': 'Solution' if is_solution else '',
                    'fields': [], 'assets': [], 'html_path': 'source.html',
                    'errors': ['Unsupported MathML in explanation'] if is_solution else []}
        with patch.object(self.adapter, '_goto'), patch.object(self.adapter, '_settle_content'), \
                patch.object(self.adapter, '_read', side_effect=read):
            result = self.adapter.history(self.adapter.activity, self.directory)
        self.assertIn('Unsupported MathML in explanation', result['questions'][0]['errors'])

    def test_history_solution_stabilizes_before_reading(self):
        self.page.set_content('<div class="questionExplanation" id="solution"><mjx-container></mjx-container></div>')
        self.page.evaluate("() => setTimeout(()=>document.querySelector('mjx-container').innerHTML='<mjx-assistive-mml><math><mn>4</mn></math></mjx-assistive-mml>',100)")
        self.adapter._settle_content(self.page.locator('#solution'))
        self.assertIn('4', self.page.locator('#solution').evaluate(EXTRACT)['worked_solution'])

    def test_assessment_initial_evidence_contains_every_question_before_entry(self):
        self.adapter.activity['kind'] = 'assessment'
        self.page.set_content('''<div id="questions"><div class="question" id="question-1"><div class="questionText">One</div><input></div>
          <div class="question" id="question-2"><div class="questionText">Two</div><input></div></div>''')
        observation = self.adapter.observe(self.directory)
        evidence = self.adapter.state['assessment_initial_evidence']
        source = Path(evidence['html_path']).read_text()
        self.assertIn('question-1', source)
        self.assertIn('question-2', source)
        self.assertEqual(observation['question_count'], 2)

    def test_assessment_navigator_waits_for_all_buttons(self):
        self.adapter.activity['kind'] = 'assessment'
        self.page.set_content('''<div id="questionNavigator"></div><div id="questions">
          <div class="question" id="question-1"><div class="questionText">One</div><input></div></div>
          <script>setTimeout(()=>document.getElementById('questionNavigator').innerHTML='<button class="questionButton">1</button>',100)</script>''')
        self.adapter.observe(self.directory)
        self.assertEqual(self.page.locator('.questionButton').count(), 1)
        self.assertFalse(self.adapter.state.get('assessment_readiness_errors'))

    def test_visible_timer_can_shorten_but_never_extend_saved_deadline(self):
        self.page.set_content('<span id="timeRemaining">00:09</span>')
        self.adapter.set_deadline(time.time() + 100)
        self.assertEqual(self.adapter.read_remaining_seconds(), 9)
        self.adapter.set_deadline(time.time() + 5)
        self.assertLessEqual(self.adapter.read_remaining_seconds(), 5)

    def test_expired_assessment_can_still_confirm_submission(self):
        self.adapter.activity['kind'] = 'assessment'
        self.adapter.set_deadline(time.time() - 10)
        self.page.set_content('''<button id="submitTestButton" onclick="document.getElementById('confirmationDialog').style.display='block'">Submit</button>
          <div id="confirmationDialog" style="display:none">Submit this test?<button
          onclick="document.getElementById('finalScreen').style.display='block'">Yes</button></div>
          <div id="finalScreen" style="display:none">Complete</div>''')
        with patch.object(self.adapter, '_pause', wraps=self.adapter._pause) as pause:
            self.adapter.respond({'key': 'submit-assessment'}, {'action': 'submit_assessment'}, self.directory)
        pause.assert_called_once_with('assessment confirmation', reserve=15)
        self.assertTrue(self.page.locator('#finalScreen').is_visible())

    def test_expired_assessment_deadline_allows_server_reconciliation(self):
        self.adapter.activity['kind'] = 'assessment'
        expired = time.time() - 10
        with patch.object(self.page, 'goto', side_effect=lambda *args, **kwargs: self.page.set_content('<div id="finalScreen">Completed</div>')) as navigation:
            self.adapter.open({**self.adapter.activity, 'url': 'https://mathacademy.com/tasks/1/tests/1'}, self.directory,
                              {'assessment_timing': {'deadline_at': expired}})
        self.assertEqual(navigation.call_args.kwargs['timeout'], 1500)
        self.assertEqual(self.adapter.timeout_ms(), 1500)
        observation = self.adapter.observe(self.directory)
        self.assertEqual(observation['kind'], 'complete')

    def test_missing_canonical_solution_keeps_lesson_definition_incomplete(self):
        self.adapter.config.timeout_ms = 100
        self.adapter._goto = lambda url, page=None: page.set_content('''<h1 id="topicName">Example topic</h1>
          <div id="steps"><div class="step" id="step-e1" stepid="1" steptype="example" contentid="2">
          <span class="stepName">Example: Find x</span><div class="exampleQuestion">Find x</div>
          <div class="exampleExplanation"></div></div></div>''')
        result = self.adapter._lesson({'topic_id': '7'}, self.directory)
        self.assertFalse(result['lesson_definition']['complete'])
        self.assertTrue(result['lesson_definition']['issues'])
        self.assertTrue(result['canonical_examples'][0]['errors'])

    def test_policy_can_accept_offered_diagnostic_retry(self):
        self.page.set_content('''<div id="retryScreen"><button id="retryScreen-yesButton"
          onclick="this.parentNode.remove();document.body.innerHTML='<div id=finalScreen>Done</div>';window.accepted=true">Yes</button>
          <button id="retryScreen-noButton">No</button></div>''')
        observation = {**self.adapter._view(), 'retry_diagnostic': True}
        self.adapter.advance(observation, self.directory)
        self.assertTrue(self.page.evaluate('window.accepted'))


if __name__ == '__main__':
    unittest.main()
