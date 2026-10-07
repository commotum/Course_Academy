import copy
import json
import random
import unittest
from pathlib import Path
from types import SimpleNamespace
from browser import CaptureBrowser, EXTRACT, mathquill_keys
from core import Pacer, normalize
import test_capture as existing

HERE = Path(__file__).parent/'fixtures'

class PreparedTests(unittest.TestCase):
    setUpClass = classmethod(existing.DOMTests.setUpClass.__func__)
    tearDownClass = classmethod(existing.DOMTests.tearDownClass.__func__)
    setUp = existing.DOMTests.setUp
    tearDown = existing.DOMTests.tearDown
    mathquill_fixture = existing.DOMTests.mathquill_fixture

    def test_saved_fraction_actions_preserve_whole_numerator(self):
        saved = json.loads((HERE/'unfinished-fraction-record.json').read_text())
        for intended in ['C','W']:
            scope, record = self.mathquill_fixture()
            record['decision'] = copy.deepcopy(saved['decision'])
            record['intended'] = intended
            args = SimpleNamespace(timeout_ms=3000,event_min=0,event_max=0)
            reader = CaptureBrowser(self.page,args,Pacer(args,random.Random(42)),None)
            reader.enter(scope,record)
            reader.verify_entered(scope,record)
            observed = record['before']['fields'][0]['observed_mathquill_latex']
            self.assertNotEqual(normalize(observed),normalize(r'2x+\frac{1}{x^2+1}'))
            self.assertEqual(self.page.evaluate('window.submissions'),0)

    def test_saved_matrix_explanation_preserves_boxed_dimensions(self):
        self.page.set_content((HERE/'unfinished-matrix-question.html').read_text())
        item = self.page.locator('#step-q42377').evaluate(EXTRACT)
        self.assertEqual(item['result'],'Correct')
        self.assertFalse(item['errors'])
        self.assertIn(r'\boxed{\text{3}}',item['worked_solution'])
        self.assertIn('statements II and III',item['worked_solution'])
        self.page.set_content('<div class="questionText"><mjx-container><mjx-assistive-mml><math><menclose notation="unknown"><mn>3</mn></menclose></math></mjx-assistive-mml></mjx-container></div>')
        item = self.page.locator('body').evaluate(EXTRACT)
        self.assertIn('Unsupported MathML enclosure',item['errors'])

if __name__=='__main__':unittest.main()

class ResumeTests(unittest.TestCase):
    setUpClass = classmethod(existing.DOMTests.setUpClass.__func__)
    tearDownClass = classmethod(existing.DOMTests.tearDownClass.__func__)
    setUp = existing.DOMTests.setUp
    tearDown = existing.DOMTests.tearDown
    mathquill_fixture = existing.DOMTests.mathquill_fixture

    def test_restored_graded_blank_matches_template_and_retains_values(self):
        from browser import same_question_problem
        before = {'problem':'Solve x.\n$x$\n{{field-1}}{{field-2}}', 'fields':[
            {'key':'field-1','observed_mathquill_latex':'<'},
            {'key':'field-2','observed_mathquill_latex':r'\frac{10}{3}'}]}
        after = {'problem':r'Solve x. $x$ $<$ $\frac{10}{3}$'}
        self.assertTrue(same_question_problem(before,after))
        self.assertFalse(same_question_problem(before,{'problem':after['problem'].replace('10','11')}))

    def test_fresh_empty_blank_can_resume_but_entered_or_graded_cannot(self):
        scope, record = self.mathquill_fixture()
        self.page.evaluate('''() => document.querySelector('.questionWidget-submitButton').classList.add('disabledButton')''')
        args = SimpleNamespace(timeout_ms=3000,resume='saved-activity')
        reader = CaptureBrowser(self.page,args,None,None)
        record['status'] = 'submitting'
        self.assertTrue(reader.restore_unanswered_submission(scope,record))
        self.assertEqual(record['status'],'prepared')
        editor = scope.locator('.mq-textarea textarea')
        editor.focus();editor.press_sequentially('1')
        record['status'] = 'submitting'
        self.assertFalse(reader.restore_unanswered_submission(scope,record))
        editor.press('ControlOrMeta+A');editor.press('Backspace')
        self.page.evaluate('''() => document.querySelector('#test').insertAdjacentHTML('beforeend','<div class="questionWidget-result">Correct</div>')''')
        self.assertFalse(reader.restore_unanswered_submission(scope,record))
        self.assertEqual(self.page.evaluate('window.submissions'),0)

    def test_previous_graded_submission_recovers_explanation_without_submit(self):
        import tempfile
        from unittest.mock import Mock
        self.page.set_content('<div id="step-q1"><div class="questionWidget-result">Correct</div></div>')
        reader = CaptureBrowser(self.page,SimpleNamespace(timeout_ms=3000),None,None)
        reader.wait_activity_ready=Mock()
        reader.current_step=Mock(return_value='stepButton-q2')
        recovered={'problem':'Find x.','result':'Correct','worked_solution':'x=1.','errors':[],'assets':[]}
        reader.read=Mock(return_value=(recovered,None))
        reader.finalize_question=Mock(side_effect=RuntimeError('stop after reconciliation'))
        record={'status':'submitting','before':{'problem':'Find x.'}}
        state={'task_type':'lesson','kps':{},'questions':{'q-1':record}}
        with tempfile.TemporaryDirectory() as work:
            with self.assertRaisesRegex(RuntimeError,'stop after reconciliation'):
                reader.activity(state,Path(work),{})
        self.assertEqual(record['status'],'graded')
        self.assertEqual(record['actual_result'],'Correct')
        self.assertEqual(record['after'],recovered)
        reader.read.assert_called_once()
