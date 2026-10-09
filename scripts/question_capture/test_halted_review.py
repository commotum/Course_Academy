import copy,json,random,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
from browser import CaptureBrowser
from retry_policy import completion_outcome,earned_xp
from saved_imports import confirmed_completion
ROOT=Path('/home/jake/Developer/Course_Academy')
FIXTURE=ROOT/'reference/mathacademy/question-capture/14042747'
EXTRACT=Path(__file__).with_name('dom.js').read_text()
class HaltedReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.runtime=sync_playwright().start();cls.browser=cls.runtime.chromium.launch(headless=True)
    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.runtime.stop()
    def setUp(self):
        self.page=self.browser.new_page();self.page.route('**/*',lambda r:r.abort())
    def tearDown(self):self.page.close()
    def test_exact_terminal_is_failed_and_not_passed(self):
        state=json.loads((FIXTURE/'state.json').read_text())
        html=(FIXTURE/'diagnostics/1791457125356707055/page.html').read_text()
        self.page.set_content(html)
        completion=self.page.locator('#finalScreen').inner_text()
        self.assertEqual(completion_outcome(completion,'review'),'failed');self.assertEqual(earned_xp(completion),-2)
        for article in ('This','The'):
            for kind in ('lesson','review'):
                self.assertEqual(completion_outcome(f'{article} {kind} has been halted due to poor performance.',kind),'failed')
                self.assertIsNone(completion_outcome(f'{article} other has been halted due to poor performance.',kind))
        reader=CaptureBrowser(self.page,SimpleNamespace(timeout_ms=3000),Mock(),None)
        reader.check=Mock();reader.wait_activity_ready=Mock();reader.knowledge_snapshot=Mock();reader.page.wait_for_url=Mock()
        reader.answer_question=Mock(side_effect=AssertionError('answered terminal review'))
        self.page.evaluate('window.submits=0; document.addEventListener("click",e=>{if(e.target.closest(".questionWidget-submitButton"))window.submits++});')
        before=copy.deepcopy(state['questions'])
        with tempfile.TemporaryDirectory() as directory:reader.activity(state,Path(directory),{})
        self.assertEqual(state['questions'],before);self.assertEqual(state['review_sequence'],'CWCWC')
        self.assertEqual(state['activity_outcome'],'failed');self.assertTrue(confirmed_completion(state));self.assertEqual(self.page.evaluate('window.submits'),0)
        reader.answer_question.assert_not_called()
    def test_real_binomial_prompt_choices_and_solution_preserve_notation(self):
        before=json.loads((FIXTURE/'q-69726-before.json').read_text())
        self.page.set_content(before['html']);item=self.page.locator('#step-q69726').evaluate(EXTRACT)
        self.assertIn(r'\genfrac{}{}{0pt}{}{5}{3}',item['problem']);self.assertIn(r'\genfrac{}{}{0pt}{}{4}{3}',item['problem'])
        self.assertEqual(item['fields'][0]['choices'][0]['value'],r'(\genfrac{}{}{0pt}{}{4}{2})')
        self.assertEqual(item['fields'][0]['choices'][2]['value'],r'(\genfrac{}{}{0pt}{}{1}{0})')
        self.assertFalse(item['errors'])
        after=json.loads((FIXTURE/'q-69726-after.json').read_text());self.page.set_content(after['html'])
        item=self.page.locator('#step-q69726').evaluate(EXTRACT)
        self.assertIn(r'\genfrac{}{}{0pt}{}{5}{3}',item['worked_solution']);self.assertEqual(item['result'],'Incorrect')
    def test_review_context_retains_real_topic_title(self):
        from solver import Solver
        context,_=Solver.activity_context(FIXTURE,[])
        self.assertEqual(context['topic_title'],"Pascal's Triangle and the Binomial Coefficients")
    def test_regular_fraction_vector_and_unfenced_stack_are_distinct(self):
        self.page.set_content('<div id="q"><div class="questionWidget-text"><math><mfrac><mn>5</mn><mn>3</mn></mfrac></math><math><mrow><mo>(</mo><mtable><mtr><mtd><mn>5</mn></mtd></mtr><mtr><mtd><mn>3</mn></mtd></mtr></mtable><mo>)</mo></mrow></math><math><mfrac linethickness="0"><mn>5</mn><mn>3</mn></mfrac></math></div></div>')
        item=self.page.locator('#q').evaluate(EXTRACT)
        self.assertIn(r'\frac{5}{3}',item['problem']);self.assertIn(r'\begin{aligned}',item['problem']);self.assertIn(r'\genfrac{}{}{0pt}{}{5}{3}',item['problem']);self.assertNotIn(r'\binom',item['problem']);self.assertFalse(item['errors'])
if __name__=='__main__':unittest.main()
