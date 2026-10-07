import copy
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import browser as module
from browser import CaptureBrowser, EXTRACT
from playwright.sync_api import sync_playwright

ROOT = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/13981762')
DIAG = ROOT / 'diagnostics/1791332157082229221'
MID = 'q-328412'

class Finalized(Exception):
    pass

class SameQuestionGradeRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = json.loads((DIAG / 'state.json').read_text())
        cls.html = (DIAG / 'page.html').read_text()
        cls.runtime = sync_playwright().start()
        cls.browser = cls.runtime.chromium.launch(headless=True)
        cls.context = cls.browser.new_context()
        cls.context.route('**/*', lambda route: route.abort())
        cls.page = cls.context.new_page()

    @classmethod
    def tearDownClass(cls):
        cls.context.close()
        cls.browser.close()
        cls.runtime.stop()

    def item(self):
        self.page.set_content(self.html, wait_until='domcontentloaded')
        return self.page.locator('#step-q328412').evaluate(EXTRACT)

    def player(self, item, grade='Correct'):
        state = copy.deepcopy(self.state)
        state['questions'] = {MID: state['questions'][MID]}
        state.pop('pending_continue', None)
        state.pop('pending_knowledge_snapshot', None)
        state['activity_complete'] = state['lesson_complete'] = False
        player = object.__new__(CaptureBrowser)
        player.args = SimpleNamespace(resume=None)
        player.pacer = Mock()
        player.page = Mock()
        player.wait_activity_ready = Mock()
        player.current_step = Mock(return_value='stepButton-q328412')
        player.restore_unanswered_submission = Mock(return_value=False)
        player.check = Mock()
        player.read = Mock(return_value=(item, None))
        player.finalize_question = Mock(side_effect=Finalized())
        scope = Mock()
        scope.is_visible.return_value = True
        scope.locator.return_value.count.return_value = 1
        scope.locator.return_value.inner_text.return_value = grade
        return player, state, scope

    def run_recovery(self, player, state, scope):
        # Missing saved result models the interrupted scrape, without changing captures.
        original_exists = Path.exists
        def exists(path):
            if path == ROOT / (MID + '-after.json'):
                return False
            return original_exists(path)
        with patch.object(module, 'by_id', return_value=scope), patch.object(module, 'atomic_json'), patch.object(Path, 'exists', exists):
            player.activity(state, ROOT, {})

    def test_saved_static_fields_preserve_question_identity(self):
        item = self.item()
        self.assertEqual(item['errors'], [])
        self.assertEqual(item['problem'], self.state['questions'][MID]['before']['problem'])
        self.assertEqual(item['result'], 'Correct')
        self.assertTrue(item['worked_solution'])
        self.assertEqual([f['dom_id'] for f in item['fields']], ['freeResponseTextbox-1', 'freeResponseTextbox-2'])

    def test_same_question_grade_is_recovered_before_readiness_wait(self):
        player, state, scope = self.player(self.item())
        try:
            self.run_recovery(player, state, scope)
        except Finalized:
            pass
        except Exception as exc:
            self.fail('Graded checkpoint was not recovered: ' + str(exc))
        else:
            self.fail('Recovery did not reach finalization')
        player.read.assert_called_once()
        player.finalize_question.assert_called_once()
        self.assertEqual(state['questions'][MID]['status'], 'graded')
        player.page.wait_for_function.assert_not_called()
        scope.click.assert_not_called()

    def test_changed_prompt_is_rejected(self):
        item = self.item()
        item['problem'] = 'Changed question. ' + item['problem']
        player, state, scope = self.player(item)
        with self.assertRaisesRegex(ValueError, 'complete saved result'):
            self.run_recovery(player, state, scope)
        player.finalize_question.assert_not_called()

    def test_unconfirmed_grade_cannot_recover(self):
        player, state, scope = self.player(self.item(), grade='Pending')
        with self.assertRaisesRegex(ValueError, 'complete saved result'):
            self.run_recovery(player, state, scope)
        player.read.assert_not_called()
        player.finalize_question.assert_not_called()

if __name__ == '__main__':
    unittest.main()
