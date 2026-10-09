import ast
import json
import unittest
from pathlib import Path
from unittest.mock import Mock, call

import browser
from playwright.sync_api import TimeoutError as PlaywrightTimeout

ROOT = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/linear/14041065')
DIAGNOSTICS = ROOT / 'diagnostics/1791451157299418113'


class FontScreenshotRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((DIAGNOSTICS / 'error.json').read_text())
        cls.message = cls.report['message']
        tree = ast.parse(Path(browser.__file__).read_text())
        reader = next(node for node in ast.walk(tree)
                      if isinstance(node, ast.FunctionDef) and node.name == 'read')
        # Execute the actual reader's screenshot statement or retry loop only.
        # No browser, network, filesystem writes, or submission methods execute.
        statement = next(node for node in reader.body
                         if isinstance(node, (ast.Expr, ast.For)) and any(
                             isinstance(child, ast.Call) and
                             isinstance(child.func, ast.Attribute) and
                             isinstance(child.func.value, ast.Name) and
                             child.func.value.id == 'scope' and
                             child.func.attr == 'screenshot'
                             for child in ast.walk(node)))
        cls.code = compile(ast.fix_missing_locations(
            ast.Module(body=[statement], type_ignores=[])), '<reader-screenshot>', 'exec')

    def run_capture(self, effects):
        scope = Mock()
        scope.screenshot.side_effect = effects
        player = Mock()
        namespace = {'scope': scope, 'screenshot': Path('offline.png'),
                     'self': player, 'PlaywrightTimeout': PlaywrightTimeout}
        return scope, player, namespace

    def test_local_evidence_records_font_timeout_after_grade(self):
        self.assertIn('waiting for fonts to load', self.message)
        self.assertEqual(self.report['exception_type'], 'TimeoutError')
        state = json.loads((DIAGNOSTICS / 'state.json').read_text())
        self.assertEqual(state['questions']['q-131333']['status'], 'submitting')
        item = json.loads((ROOT / 'q-131333-after.json').read_text())
        self.assertEqual(item['result'], 'Incorrect')
        self.assertEqual(item['errors'], [])
        # The original single screenshot call reproduces the supplied failure.
        scope = Mock()
        scope.screenshot.side_effect = PlaywrightTimeout(self.message)
        with self.assertRaisesRegex(PlaywrightTimeout, 'waiting for fonts to load'):
            scope.screenshot(path='offline.png')

    def test_transient_font_wait_recovers_with_pacing(self):
        scope, player, namespace = self.run_capture([PlaywrightTimeout(self.message), None])
        exec(self.code, namespace)
        self.assertEqual(scope.screenshot.call_args_list,
                         [call(path='offline.png'), call(path='offline.png')])
        player.pacer.backoff.assert_called_once_with(1)
        player.check.assert_called_once_with()
        player.page.assert_not_called()

    def test_persistent_font_wait_still_fails(self):
        scope, player, namespace = self.run_capture([PlaywrightTimeout(self.message)] * 3)
        with self.assertRaisesRegex(PlaywrightTimeout, 'waiting for fonts to load'):
            exec(self.code, namespace)
        self.assertEqual(scope.screenshot.call_count, 3)
        self.assertEqual(player.pacer.backoff.call_args_list, [call(1), call(2)])
        self.assertEqual(player.check.call_count, 2)

    def test_visibility_timeout_is_not_retried_or_bypassed(self):
        scope, player, namespace = self.run_capture([PlaywrightTimeout('element is not visible')])
        with self.assertRaisesRegex(PlaywrightTimeout, 'element is not visible'):
            exec(self.code, namespace)
        scope.screenshot.assert_called_once_with(path='offline.png')
        player.pacer.backoff.assert_not_called()
        player.check.assert_not_called()

    def test_stop_check_interrupts_retry(self):
        scope, player, namespace = self.run_capture([PlaywrightTimeout(self.message), None])
        player.check.side_effect = KeyboardInterrupt('Stopped')
        with self.assertRaises(KeyboardInterrupt):
            exec(self.code, namespace)
        scope.screenshot.assert_called_once_with(path='offline.png')


if __name__ == '__main__':
    unittest.main()
