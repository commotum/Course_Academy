"""Owned history fallback preserves source identity and unanswered outcomes."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from scripts.browser.history import HistoryChoices, task_answers


class TaskAnswerIdentityTests(unittest.TestCase):
    def test_response_requires_matching_task_and_unique_question_identity(self):
        payload={'task':{'id':7,'answers':[{'question':{'id':42}}]}}
        self.assertEqual(list(task_answers(payload,'7')),['q-42'])
        with self.assertRaises(ValueError):task_answers(payload,'8')
        payload['task']['answers']*=2
        with self.assertRaises(ValueError):task_answers(payload,'7')


class HistoryChoiceRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.pw=sync_playwright().start();cls.browser=cls.pw.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.pw.stop()

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.directory=Path(self.temp.name)
        self.context=self.browser.new_context();self.addCleanup(self.context.close)
        self.context.route('**/*',lambda route:route.abort())
        self.renderer=HistoryChoices(self.context,Path(__file__).resolve().parents[3]);self.addCleanup(self.renderer.close)
        self.record={'math_academy_id':'q-42','problem':'$0^{100}=$','fields':[],
            'grade':'Incorrect','time_elapsed':'0:00','extraction_parts':['problem','solution'],
            'html':'<div id="question-42"><div class="questionText"><p><math><msup><mn>0</mn><mn>100</mn></msup><mo>=</mo></math></p></div></div>'}
        self.answer={'selectedChoice':None,'correct':0,'timeElapsed':0,'question':{
            'id':42,'format':'MC','text':'<p>$0^{100}=$</p>',
            **{'choice'+str(i):v for i,v in enumerate(('$0$','$1$','$100$',r'$\dfrac{1}{100}$','$10$'),1)}}}

    def test_missing_choices_are_recovered_without_inventing_attempt_or_correct_key(self):
        before=deepcopy(self.record)
        result=self.renderer.recover(self.record,self.answer,self.directory/'raw.json',self.directory)
        self.assertEqual(self.record,before)
        self.assertEqual(result['problem'],self.record['problem'])
        self.assertEqual([c['value'] for c in result['fields'][0]['choices']],['0','1','100',r'\frac{1}{100}','10'])
        self.assertNotIn('correct_value',result['fields'][0]);self.assertNotIn('submissions',result)
        self.assertEqual((result['grade'],result['time_elapsed']),('Incorrect','0:00'))
        self.assertIsNone(result['field_recovery']['learner_answer']['selectedChoice'])
        self.assertTrue(Path(result['field_recovery']['rendered_file']).is_file())

    def test_identity_and_prompt_must_both_match(self):
        for change in ({'math_academy_id':'q-43'},
                       {'html':self.record['html'].replace('question-42','question-43')},
                       {'html':self.record['html'].replace('<mn>100</mn>','<mn>99</mn>')}):
            with self.subTest(change=change),self.assertRaises(ValueError):
                self.renderer.recover({**self.record,**change},self.answer,self.directory/'raw.json',self.directory)

    def test_local_extension_does_not_require_external_network(self):
        self.answer['question']['choice5']=r'$\bbox[1pt, border: 1pt solid black]{\phantom{A}}$'
        result=self.renderer.recover(self.record,self.answer,self.directory/'raw.json',self.directory)
        self.assertTrue(result['answer_fields_complete'])
        self.assertIn(r'\bbox',result['fields'][0]['choices'][-1]['value'])

    def test_currency_uses_native_tex_delimiters_and_matches_live_mathml(self):
        from scripts.browser.adapter import EXTRACT
        self.answer['question']['choice5']=r'The initial price is $\$25\, 500$'
        result=self.renderer.recover(self.record,self.answer,self.directory/'raw.json',self.directory)
        choice=result['fields'][0]['choices'][-1]
        self.assertEqual(choice['value'],r'The initial price is $\$25\,500$')
        self.assertIn('<math',choice['html'])
        self.renderer.page.set_content('<div id="live"><div class="questionText">'+
            'The initial price is <math><mi mathvariant="normal">$</mi><mn>25</mn>'+
            '<mstyle><mspace width="0.167em"></mspace></mstyle><mn>500</mn></math></div></div>')
        live=self.renderer.page.locator('#live').evaluate(EXTRACT)
        self.assertEqual(live['problem'],choice['value'])
        self.assertEqual(live['errors'],[])

    def test_native_finder_handles_multiple_formulas_and_escaped_currency_in_prose(self):
        self.answer['question']['choice5']=r'Pay \$5 for $x+1$ or \(y+2\).'
        result=self.renderer.recover(self.record,self.answer,self.directory/'raw.json',self.directory)
        choice=result['fields'][0]['choices'][-1]
        self.assertEqual(choice['value'],r'Pay $5 for $x+1$ or $y+2$.')
        self.assertEqual(choice['html'].count('<math '),2)

    def test_refresh_requires_owned_task_provenance_and_replaces_stale_fields(self):
        record=deepcopy(self.record);record['fields']=[{'key':'selection','choices':[{'value':'old'}]}]
        with self.assertRaises(ValueError):
            self.renderer.recover(record,self.answer,self.directory/'raw.json',self.directory,refresh=True)
        record['field_recovery']={'kind':'owned_task_answers','question_id':'q-42'}
        record['answer_fields']=deepcopy(record['fields'])
        result=self.renderer.recover(record,self.answer,self.directory/'raw.json',self.directory,refresh=True)
        self.assertEqual(result['fields'][0]['choices'][0]['value'],'0')
        self.assertNotIn('answer_fields',result)
        self.assertEqual(record['fields'][0]['choices'][0]['value'],'old')


if __name__=='__main__':unittest.main()
