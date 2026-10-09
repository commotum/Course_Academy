import ast
import re
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import browser

EVIDENCE = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/differential/14042307/diagnostics/1791451263371696983/page.html')
OLD = "if kind not in ('multistep','diagnostic') or not card.locator('.taskDetails').is_visible():"
NEW = "if not card.locator('.taskDetails').is_visible():"

class HiddenStart(Exception):
    pass

class Card:
    def __init__(self, expanded):
        self.expanded = expanded
        self.clicks = 0
    def locator(self, selector):
        assert selector == '.taskDetails'
        return self
    def is_visible(self):
        return self.expanded
    def click(self):
        self.clicks += 1
        self.expanded = not self.expanded

class Button:
    def __init__(self, card, href, hidden=False):
        self.card, self.href, self.hidden = card, href, hidden
        self.clicked = False
    def wait_for(self, state):
        assert state == 'visible'
        if not self.card.expanded or self.hidden:
            raise HiddenStart('Start remains hidden')
    def get_attribute(self, name):
        assert name == 'href'
        return self.href
    def click(self):
        self.wait_for('visible')
        self.clicked = True

class ExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        html = EVIDENCE.read_text()
        match = re.search(r'<a id="taskStartButton-14042307"[^>]*href="([^"]+)"', html)
        if not match:
            raise AssertionError('Missing saved Start link')
        cls.href = match.group(1)
        if 'id="taskDetails-14042307" class="taskDetails"' not in html:
            raise AssertionError('Missing saved details container')
        cls.activity = dict(task_type='lesson', task_id=14042307, topic_id=3837,
                            card_id='task-14042307', start_id='taskStartButton-14042307', href=cls.href)

    def run_start(self, expanded, original=False, hidden=False, href=None):
        card = Card(expanded)
        button = Button(card, self.href if href is None else href, hidden)
        player = SimpleNamespace(page=SimpleNamespace(wait_for_url=lambda *a, **k: None),
                                 pacer=SimpleNamespace(wait=lambda *a: None), check=lambda: None)
        start = browser.CaptureBrowser.start
        if original:
            source = Path(browser.__file__).read_text().replace(NEW, OLD)
            tree = ast.parse(source)
            cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'CaptureBrowser')
            method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == 'start')
            namespace = dict(vars(browser))
            exec(compile(ast.Module(body=[method], type_ignores=[]), '<original-start>', 'exec'), namespace)
            start = namespace['start']
        def lookup(page, identifier):
            return card if identifier == self.activity['card_id'] else button
        with patch.object(browser, 'by_id', lookup):
            if original:
                start.__globals__['by_id'] = lookup
            start(player, self.activity)
        return card, button

    def test_original_expanded_card_reproduces_hidden_start(self):
        with self.assertRaises(HiddenStart):
            self.run_start(True, original=True)

    def test_expanded_card_stays_open(self):
        card, button = self.run_start(True)
        self.assertEqual(card.clicks, 0)
        self.assertTrue(button.clicked)

    def test_collapsed_card_expands_once(self):
        card, button = self.run_start(False)
        self.assertEqual(card.clicks, 1)
        self.assertTrue(button.clicked)

    def test_hidden_start_is_not_bypassed(self):
        with self.assertRaises(HiddenStart):
            self.run_start(True, hidden=True)

    def test_changed_href_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Queue activity changed before starting'):
            self.run_start(True, href='/tasks/other')

if __name__ == '__main__':
    unittest.main()
