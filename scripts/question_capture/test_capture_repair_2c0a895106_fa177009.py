import ast
import re
import unittest
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

EVIDENCE = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/14043928/diagnostics/1791459350921883513/page.html')


class ToolboxSubmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = Path(__file__).with_name('multistep.py').read_text()
        tree = ast.parse(cls.source)
        helper = next((n for n in tree.body if isinstance(n, ast.FunctionDef)
                       and n.name == 'dismiss_math_toolboxes'), None)
        if helper is None:
            cls.dismiss = staticmethod(lambda page, scope: None)
        else:
            namespace = {}
            exec(compile(ast.Module(body=[helper], type_ignores=[]), 'multistep.py', 'exec'), namespace)
            cls.dismiss = staticmethod(namespace['dismiss_math_toolboxes'])
        html = EVIDENCE.read_text()
        # Extract the actual blocking toolbox without loading page scripts/assets.
        match = re.search(r'<div id="mathEditorToolbox" style="[^"]*visibility: visible;[^"]*">((?:<div class="mathIcon [^"]+"></div>)+)</div>', html)
        if match is None:
            raise AssertionError('Saved visible toolbox missing')
        cls.toolbox = match.group(0)
        if 'id="submitButton-4"' not in html or 'mq-textarea' not in html:
            raise AssertionError('Saved submit/editor evidence missing')
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.page = self.browser.new_page()
        self.page.route('**/*', lambda route: route.abort())
        self.page.set_default_timeout(500)
        self.page.set_content('<div id="scope"><div class="mq-textarea"><textarea></textarea></div></div>'
                              '<button id="submitButton-4" style="position:absolute;left:20px;top:100px;width:100px;height:40px">Submit</button>'
                              + self.toolbox)
        self.page.evaluate('''() => {
          const menu=document.getElementById('mathEditorToolbox');
          Object.assign(menu.style,{left:'20px',top:'100px',width:'100px',height:'40px',pointerEvents:'auto'});
          window.submissions=0;
          document.getElementById('submitButton-4').onclick=()=>window.submissions++;
          const editor=document.querySelector('textarea');
          editor.value='1';
          editor.onblur=()=>setTimeout(()=>menu.style.visibility='hidden',20);
          editor.focus();
        }''')
        self.scope = self.page.locator('#scope')
        self.submit = self.page.locator('#submitButton-4')

    def tearDown(self):
        self.page.close()

    def test_saved_overlay_blocks_original_click(self):
        with self.assertRaises(PlaywrightTimeoutError):
            self.submit.click(timeout=150)
        self.assertEqual(self.page.evaluate('window.submissions'), 0)

    def test_normal_blur_allows_checked_click_and_preserves_value(self):
        self.dismiss(self.page, self.scope)
        self.submit.click(timeout=150)
        self.assertEqual(self.page.evaluate('window.submissions'), 1)
        self.assertEqual(self.scope.locator('textarea').input_value(), '1')

    def test_overlay_that_does_not_dismiss_still_stops(self):
        self.page.evaluate("document.querySelector('textarea').onblur=null")
        with self.assertRaises(PlaywrightTimeoutError):
            self.dismiss(self.page, self.scope)
            self.submit.click(timeout=150)
        self.assertEqual(self.page.evaluate('window.submissions'), 0)

    def test_dismissal_precedes_verification_and_submission_intent(self):
        tree = ast.parse(self.source)
        take = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'take_multistep')
        calls = [(n.lineno, ast.unparse(n.func)) for n in ast.walk(take) if isinstance(n, ast.Call)]
        dismissal = next(line for line, name in calls if name == 'dismiss_math_toolboxes')
        verification = next(line for line, name in calls if name == 'reader.verify_entered')
        click = next(line for line, name in calls if name == 'submit.click')
        self.assertLess(dismissal, verification)
        self.assertLess(verification, click)
        self.assertNotIn('force=True', self.source)


if __name__ == '__main__':
    unittest.main()
