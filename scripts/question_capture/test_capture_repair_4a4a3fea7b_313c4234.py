import ast
import unittest
from pathlib import Path
from types import SimpleNamespace
import browser
from playwright.sync_api import TimeoutError as PlaywrightTimeout

EVIDENCE = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/multivariable/14063808/diagnostics/1791501512894527056/page.html')
OLD = "        button.wait_for(state='visible')\n        if button.get_attribute('href') != activity['href']:"
NEW = """        from playwright.sync_api import TimeoutError as PlaywrightTimeout
        try:
            button.wait_for(state='visible')
        except PlaywrightTimeout:
            self.check()
            if kind == 'assessment' or card.locator('.taskDetails').is_visible():
                raise
            self.pacer.wait('event', 'retry expanding the selected ' + kind)
            card.click()
            button.wait_for(state='visible')
        if button.get_attribute('href') != activity['href']:"""

class StartRecovery(unittest.TestCase):
    def run_start(self, original=False, stuck=False, expanded=False, href=None):
        html = EVIDENCE.read_text()
        self.assertIn('id="task-14063808" class="taskUnlocked"', html)
        self.assertIn('id="taskDetails-14063808" class="taskDetails"', html)
        expected = '/tasks/14063808/topics/1177/review'
        self.assertIn('href="' + expected + '"', html)
        state = dict(expanded=expanded, clicks=0, starts=0, checks=0)
        def expand():
            state['clicks'] += 1
            if state['clicks'] == 2 and not stuck:
                state['expanded'] = True
        def wait_for(**kw):
            self.assertEqual(kw, {'state':'visible'})
            if not state['expanded'] or stuck:
                raise PlaywrightTimeout('Start remains hidden')
        def start_click(**kw):
            self.assertEqual(kw, {})
            wait_for(state='visible')
            state['starts'] += 1
        card = SimpleNamespace(locator=lambda s: SimpleNamespace(is_visible=lambda: state['expanded']), click=expand)
        button = SimpleNamespace(wait_for=wait_for, get_attribute=lambda s: href or expected, click=start_click)
        def check():
            state['checks'] += 1
        player = SimpleNamespace(page=SimpleNamespace(wait_for_url=lambda *a, **k: None),
                                 pacer=SimpleNamespace(wait=lambda *a: None), check=check)
        source = Path(browser.__file__).read_text()
        if original:
            source = source.replace(NEW, OLD)
        tree = ast.parse(source)
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'CaptureBrowser')
        method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == 'start')
        namespace = dict(vars(browser))
        namespace['by_id'] = lambda p, i: card if i == 'task-14063808' else button
        exec(compile(ast.Module(body=[method], type_ignores=[]), '<offline-start>', 'exec'), namespace)
        activity = dict(task_type='review', task_id=14063808, topic_id=1177,
                        card_id='task-14063808', start_id='taskStartButton-14063808', href=expected)
        namespace['start'](player, activity)
        return state

    def test_original_hidden_start(self):
        with self.assertRaises(PlaywrightTimeout):
            self.run_start(original=True)

    def test_second_expansion_recovers(self):
        state = self.run_start()
        self.assertEqual(state['clicks'], 2)
        self.assertEqual(state['starts'], 1)
        self.assertEqual(state['checks'], 2)

    def test_persistent_hidden_start_fails(self):
        with self.assertRaises(PlaywrightTimeout):
            self.run_start(stuck=True)

    def test_expanded_card_is_not_toggled(self):
        state = self.run_start(expanded=True)
        self.assertEqual(state['clicks'], 0)
        self.assertEqual(state['starts'], 1)

    def test_changed_href_fails(self):
        with self.assertRaisesRegex(ValueError, 'Queue activity changed'):
            self.run_start(href='/tasks/other')

if __name__ == '__main__':
    unittest.main()
