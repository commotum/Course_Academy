import ast
import copy
import json
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/14043928/diagnostics/1791459523675930549')


class MultistepRestorationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = Path(__file__).with_name('multistep.py').read_text()
        tree = ast.parse(cls.source)
        node = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'restore_empty_multistep'), None)
        if node is None:
            cls.restore = staticmethod(lambda *args: False)
        else:
            namespace = {'normalize': lambda value: value, 'time': SimpleNamespace(time=lambda: 123)}
            exec(compile(ast.Module(body=[node], type_ignores=[]), 'multistep.py', 'exec'), namespace)
            cls.restore = staticmethod(namespace['restore_empty_multistep'])
        cls.saved = json.loads((ROOT / 'state.json').read_text())['questions']['q-128660']
        cls.html = (ROOT / 'page.html').read_text()

    def setUp(self):
        self.record = copy.deepcopy(self.saved)
        self.fresh = copy.deepcopy(self.record['before'])
        self.fresh['problem'] = self.record['local_problem']
        self.fresh['result'] = None
        self.fresh['errors'] = []
        self.reads = []
        def read(*args):
            self.reads.append(args)
            return self.fresh, None
        self.reader = SimpleNamespace(read=read)
        self.scope = SimpleNamespace(evaluate=lambda script: True)
        self.submit = SimpleNamespace(is_visible=lambda: True, get_attribute=lambda name: 'submitButton disabledButton')
        self.continuation = SimpleNamespace(is_visible=lambda: False)

    def call(self):
        return self.restore(self.reader, self.scope, self.submit, self.continuation,
                            self.record, ROOT, 'q-128660')

    def test_saved_empty_restoration_reuses_decision_and_timing(self):
        self.assertEqual(self.record['status'], 'submitting')
        self.assertIn('id="submitButton-4" class="submitButton disabledButton"', self.html)
        self.assertIn('id="continueButton-4" class="continueButton" style="display: none;"', self.html)
        decision = copy.deepcopy(self.record['decision'])
        elapsed = self.record['solver_elapsed_seconds']
        self.assertTrue(self.call())
        self.assertEqual(self.record['status'], 'prepared')
        self.assertEqual(self.record['decision'], decision)
        self.assertEqual(self.record['solver_elapsed_seconds'], elapsed)
        self.assertEqual(len(self.reads), 1)

    def test_recorded_grade_prevents_retry(self):
        self.record['actual_result'] = 'Correct'
        self.assertFalse(self.call())
        self.assertEqual(self.record['status'], 'submitting')

    def test_nonempty_or_pending_editor_prevents_retry(self):
        self.scope.evaluate = lambda script: False
        self.assertFalse(self.call())
        self.assertEqual(self.reads, [])

    def test_visible_continue_prevents_retry(self):
        self.continuation.is_visible = lambda: True
        self.assertFalse(self.call())

    def test_changed_or_graded_fresh_question_prevents_retry(self):
        for change in ({'problem': 'different'}, {'result': 'Correct'}, {'errors': ['incomplete']}):
            with self.subTest(change=change):
                original = copy.deepcopy(self.fresh)
                self.fresh.update(change)
                self.assertFalse(self.call())
                self.assertEqual(self.record['status'], 'submitting')
                self.fresh = original

    def test_recovery_is_before_prepared_submission_branch(self):
        tree = ast.parse(self.source)
        take = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'take_multistep')
        recovery = next(n.lineno for n in ast.walk(take) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'restore_empty_multistep')
        enter = next(n.lineno for n in ast.walk(take) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'enter')
        self.assertLess(recovery, enter)


if __name__ == '__main__':
    unittest.main()
