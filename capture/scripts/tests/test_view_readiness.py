"""Wait for source question rendering without treating graded pages as unfinished."""
from pathlib import Path
import unittest

FIXTURES = Path(__file__).parent / 'fixtures'
VIEW = (Path(__file__).parents[1] / 'browser' / 'view.js').read_text()


class ViewReadinessTests(unittest.TestCase):
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
        self.page = self.context.new_page()
        self.page.set_default_timeout(2000)
        self.addCleanup(self.context.close)

    def view(self):
        return self.page.evaluate(VIEW)

    def test_captured_radio_waits_for_mathjax_after_next_step_appears(self):
        self.page.set_content((FIXTURES / 'q-11294-radio.html').read_text())
        self.assertTrue(self.view()['ready'])
        self.page.evaluate('''() => {
          const formula = document.querySelector('mjx-container');
          window.savedMath = formula.querySelector('mjx-assistive-mml');
          window.savedMath.remove();
        }''')
        pending = self.view()
        self.assertEqual(pending['kind'], 'question')
        self.assertEqual(pending['key'], 'step-q11294')
        self.assertFalse(pending['ready'])
        self.page.evaluate('''() => setTimeout(() =>
          document.querySelector('mjx-container').appendChild(window.savedMath), 80)''')
        self.page.wait_for_function('() => (' + VIEW + ')().ready')
        self.assertTrue(self.view()['ready'])

    def test_captured_radio_waits_for_answer_choices(self):
        self.page.set_content((FIXTURES / 'q-11294-radio.html').read_text())
        self.page.evaluate('''() => {
          window.savedChoices = document.querySelector('.questionWidget-choicesTable');
          window.savedChoices.remove();
        }''')
        self.assertFalse(self.view()['ready'])
        self.page.evaluate('''() => document.querySelector('.questionWidget').appendChild(window.savedChoices)''')
        self.assertTrue(self.view()['ready'])

    def test_image_only_prompt_is_ready(self):
        self.page.set_content('''<div class="step questionWidget" id="step-q1">
          <div class="questionWidget-text"><canvas width="40" height="40"></canvas></div>
          <input id="answer"><button class="questionWidget-submitButton">Submit</button>
        </div>''')
        self.assertTrue(self.view()['ready'])

    def test_diagnostic_preserves_identity_while_prompt_is_loading(self):
        self.page.set_content('''<div id="questionContainer" style="min-height:10px">
          <div class="questionWidget-title">Question 2</div>
        </div>''')
        pending = self.view()
        self.assertEqual(pending['kind'], 'question')
        self.assertEqual(pending['key'], 'diagnostic-2')
        self.assertFalse(pending['ready'])
        self.page.evaluate('''() => document.querySelector('#questionContainer').insertAdjacentHTML('beforeend',
          '<div class="questionWidget-text">Find x.</div><input>')''')
        self.assertTrue(self.view()['ready'])

    def test_captured_grade_needs_no_editable_fields(self):
        self.page.set_content((FIXTURES / 'diagnostic-skipped-select-after.html').read_text())
        self.page.evaluate('''() => document.querySelectorAll('.selectList,input,textarea,select,.matheditor-wrapper-answer')
          .forEach(n => n.remove())''')
        view = self.view()
        self.assertTrue(view['accepted'])
        self.assertTrue(view['ready'])

    def test_continuation_needs_no_editable_fields(self):
        self.page.set_content('''<div id="questionContainer" style="min-height:10px">
          <div class="questionWidget-title">Question 3</div>
          <div class="questionWidget-text">A saved response.</div>
        </div><button id="nextButton">Next</button>''')
        view = self.view()
        self.assertEqual(view['next'], '#nextButton')
        self.assertTrue(view['ready'])

    def test_example_waits_for_explanation_and_accepts_a_graphic(self):
        self.page.set_content('''<div class="stepButton current" id="stepButton-e1">Example</div>
          <div id="steps"><div class="step" id="step-e1">
            <div class="exampleQuestion">Find x.</div><div class="exampleExplanation"></div>
          </div></div>''')
        self.assertEqual(self.view()['kind'], 'example')
        self.assertFalse(self.view()['ready'])
        self.page.evaluate('''() => document.querySelector('.exampleExplanation').innerHTML='<svg width="20" height="20"><path d="M0 0 L20 20"/></svg>' ''')
        self.assertTrue(self.view()['ready'])

    def test_assessment_readiness_is_specific_to_each_question(self):
        question = (FIXTURES / 'assessment-105178-question.html').read_text()
        self.page.set_content('<div id="questions">' + question + '''
          <div class="question" id="question-2"><div class="questionText">Still rendering.</div></div>
        </div>''')
        view = self.view()
        self.assertEqual(view['kind'], 'assessment')
        self.assertTrue(view['question_ready']['question-105178'])
        self.assertFalse(view['question_ready']['question-2'])


if __name__ == '__main__':
    unittest.main()
