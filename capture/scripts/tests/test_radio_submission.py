"""Radio submission regressions from the three stalled 2026-10-10 workers.

HTML comes from task 14109531 (review q-11294) and task 14110945
(diagnostic q-94453). MA's multiple-choice-question-widget.js clears choices
on question-background clicks and stops propagation on choice clicks.
"""
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from scripts.browser.adapter import EXTRACT, RESPONSE_READY, RESPONSE_STATE, MathAcademyBrowser


class RadioSubmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise unittest.SkipTest("Playwright is required for offline DOM tests")
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def test_captured_image_choice_submits_once_and_changed_source_is_rejected(self):
        fixture = Path(__file__).parent / 'fixtures' / 'q-94453-diagnostic-radio.html'
        for changed in (False, True):
            with self.subTest(changed=changed), tempfile.TemporaryDirectory() as directory:
                context = self.browser.new_context()
                self.addCleanup(context.close)
                context.route('**/*', lambda route: route.abort())
                page = context.new_page()
                page.set_default_timeout(2000)
                page.set_content(fixture.read_text())
                page.evaluate('''() => {
                  const widget=document.querySelector('.questionWidget');
                  const first=widget.querySelector('.questionWidget-choicesTable tr');
                  first.querySelector('td:last-child').innerHTML='<svg width="10" height="10"><path d="M0 0L10 10"/></svg>';
                  const submit=widget.querySelector('.questionWidget-submitButton');
                  window.submissions=0;
                  widget.querySelectorAll('.questionWidget-choiceLetterCircle').forEach(choice => {
                    choice.onclick=event=>{event.stopPropagation();choice.style.background='rgb(64, 64, 64)';
                      submit.disabled=false;submit.classList.remove('disabledButton');};
                  });
                  submit.onclick=event=>{event.stopPropagation();++window.submissions;
                    const result=document.createElement('div');result.className='questionWidget-result';
                    result.textContent='Correct';widget.append(result);};
                }''')
                adapter = MathAcademyBrowser(SimpleNamespace(timeout_ms=2000), threading.Event())
                adapter.page, adapter.context = page, context
                adapter.directory = Path(directory)
                adapter.activity = {'task_id': 'offline', 'kind': 'diagnostic'}
                current = adapter._view()
                scope = page.locator(current['selector'])
                item = adapter._read(scope, directory, 'image-choice')
                choice = item['fields'][0]['choices'][0]
                self.assertEqual(choice['type'], 'image')
                self.assertTrue(Path(choice['value']).is_file())
                if changed:
                    scope.locator('.questionWidget-choicesTable tr').first.locator('td:last-child svg path').evaluate(
                        "n=>n.setAttribute('d','M0 10L10 0')")
                observation = {**current, 'question': item}
                result = adapter.respond(observation, [{'key': 'selection', 'value': choice['value'],
                                                         'option': choice['option']}], directory)
                if changed:
                    self.assertTrue(result['not_submitted'])
                    self.assertEqual(page.evaluate('window.submissions'), 0)
                else:
                    adapter.respond(observation, [{'key': 'selection', 'value': choice['value']}], directory)
                    self.assertEqual(page.evaluate('window.submissions'), 1)

    def test_radio_selection_survives_until_submit_in_review_and_diagnostic(self):
        fixtures = Path(__file__).parent / "fixtures"
        for kind, filename in [("review", "q-11294-radio.html"),
                               ("diagnostic", "q-94453-diagnostic-radio.html")]:
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                context = self.browser.new_context()
                self.addCleanup(context.close)
                context.route("**/*", lambda route: route.abort())
                page = context.new_page()
                page.set_default_timeout(1000)
                page.set_content((fixtures / filename).read_text())
                page.evaluate("""() => {
                  const widget = document.querySelector('.questionWidget');
                  const submit = widget.querySelector('.questionWidget-submitButton');
                  const choices = [...widget.querySelectorAll('.questionWidget-choiceLetterCircle')];
                  window.submissions = 0; window.backgroundClicks = 0;
                  widget.onclick = () => {
                    ++window.backgroundClicks;
                    choices.forEach(node => node.style.background = '');
                    submit.disabled = true; submit.classList.add('disabledButton');
                  };
                  choices.forEach(node => node.onclick = event => {
                    event.stopPropagation();
                    choices.forEach(other => other.style.background = '');
                    node.style.background = 'rgb(64, 64, 64)';
                    submit.disabled = false; submit.classList.remove('disabledButton');
                  });
                  submit.onclick = event => {
                    event.stopPropagation();
                    if (submit.disabled) return;
                    ++window.submissions;
                    let result = widget.querySelector('.questionWidget-result');
                    if (!result) { result = document.createElement('div');
                      result.className = 'questionWidget-result'; widget.append(result); }
                    result.textContent = 'Correct'; submit.style.display = 'none';
                  };
                }""")
                adapter = MathAcademyBrowser(SimpleNamespace(timeout_ms=1000), threading.Event())
                adapter.page, adapter.context = page, context
                adapter.directory = Path(directory)
                adapter.activity = {"task_id": "offline", "kind": kind}
                current = adapter._view()
                item = page.locator(current["selector"]).evaluate(EXTRACT)
                observation = {**current, "question": item}
                field = item["fields"][0]
                response = [{"key": field["key"], "option": field["choices"][0]["option"]}]
                with patch.object(adapter, "_read", side_effect=lambda scope, *args: scope.evaluate(EXTRACT)), \
                     patch.object(adapter, "_evidence", return_value={}):
                    adapter.respond(observation, response, directory)
                    adapter.respond(observation, response, directory)
                self.assertEqual(page.evaluate("window.backgroundClicks"), 0)
                self.assertEqual(page.evaluate("window.submissions"), 1)
                self.assertEqual(adapter.state["pending_action"]["action"], "submit")

    def test_math_sanitized_on_native_blur_is_not_submitted(self):
        with tempfile.TemporaryDirectory() as directory:
            context = self.browser.new_context()
            self.addCleanup(context.close)
            context.route("**/*", lambda route: route.abort())
            page = context.new_page()
            page.set_content('''<div class="step questionWidget" id="step-q1">
              <div class="questionWidget-text">Enter a value.</div>
              <div class="matheditor-wrapper-answer"><span class="mq-editable-field">
                <span class="mq-textarea"><textarea onblur="window.wasBlurred=true;window.value='5'"></textarea></span>
              </span></div><button class="questionWidget-submitButton"
                onclick="window.submissions=(window.submissions||0)+1">Submit</button></div>
              <script>window.value='';window.submissions=0;window.wasBlurred=false;
                window.MathQuill = node => ({latex: () => window.value});</script>''')
            adapter = MathAcademyBrowser(SimpleNamespace(timeout_ms=1000), threading.Event())
            adapter.page, adapter.context = page, context
            adapter.directory = Path(directory)
            adapter.activity = {"task_id": "offline", "kind": "review"}
            fresh = {"fields": [{"key": "value", "type": "blank", "tag": "mathquill", "dom_index": 0}]}
            observation = {**adapter._view(), "question": fresh}

            def enter_value(*args):
                page.evaluate("() => {window.value='4';document.querySelector('textarea').focus();}")
                return {"key": "value", "value": "4", "value_type": "math"}

            with patch.object(adapter, "_read", return_value=fresh), \
                 patch.object(adapter, "_evidence", return_value={}), \
                 patch('scripts.browser.adapter.enter', side_effect=enter_value):
                with self.assertRaises(ValueError):
                    adapter.respond(observation, [{"key": "value", "value": "4"}], directory)
            self.assertTrue(page.evaluate('window.wasBlurred'))
            self.assertEqual(page.evaluate('window.submissions'), 0)
            self.assertEqual(adapter.state["pending_action"]["action"], "entered")

    def test_stale_proof_feedback_waits_and_keeps_submission_intent(self):
        with tempfile.TemporaryDirectory() as directory:
            context = self.browser.new_context()
            self.addCleanup(context.close)
            context.route("**/*", lambda route: route.abort())
            page = context.new_page()
            page.set_content('''<div class="step questionWidget" id="step-q1">
              <div class="questionWidget-text">Complete the proof.</div>
              <div class="selectList" id="field"><div class="selectListFrame incorrectSelection">Old choice</div></div>
              <div class="questionWidget-feedback">Oops, that's not quite right. Please try again.</div>
              <div class="questionWidget-spinner">Loading</div>
              <button class="questionWidget-submitButton disabledButton" disabled>Submit</button></div>''')
            before = page.locator('#step-q1').evaluate(RESPONSE_STATE)
            waiting = {"selector": '#step-q1', "before": before}
            self.assertFalse(page.evaluate(RESPONSE_READY, waiting))
            adapter = MathAcademyBrowser(SimpleNamespace(timeout_ms=1000), threading.Event())
            adapter.page, adapter.context = page, context
            adapter.directory = Path(directory)
            adapter.activity = {"task_id": "offline", "kind": "review"}
            adapter.state = {"pending_action": {"action": "submit", "response_before": before}, "restored": False}
            item = {"dom_id": "step-q1", "html": '', "html_path": '', "screenshot": None,
                    "fields": [{"key": "field", "source_result": "Incorrect"}],
                    "proof_feedback": before['feedback']}
            with patch.object(adapter, '_read', return_value=item):
                adapter.observe(directory)
                self.assertIn('pending_action', adapter.state)
                # MA uses this class when a proof field becomes correct later.
                page.locator('.selectListFrame').evaluate("n=>n.className='selectListFrameDisabled correctSelectionMultipleAttempts'")
                self.assertTrue(page.evaluate(RESPONSE_READY, waiting))
                adapter.observe(directory)
                self.assertNotIn('pending_action', adapter.state)

    def test_repeated_incorrect_proof_waits_until_ma_enables_retry(self):
        context = self.browser.new_context()
        self.addCleanup(context.close)
        context.route("**/*", lambda route: route.abort())
        page = context.new_page()
        page.set_content('''<div id="question"><div class="selectListFrame incorrectSelection">Choice</div>
          <div class="questionWidget-feedback">Oops</div>
          <button class="questionWidget-submitButton disabledButton" disabled>Submit</button></div>''')
        waiting = {"selector": '#question', "before": page.locator('#question').evaluate(RESPONSE_STATE)}
        self.assertFalse(page.evaluate(RESPONSE_READY, waiting))
        page.locator('button').evaluate("n=>{n.disabled=false;n.classList.remove('disabledButton');}")
        self.assertTrue(page.evaluate(RESPONSE_READY, waiting))


if __name__ == "__main__":
    unittest.main()
