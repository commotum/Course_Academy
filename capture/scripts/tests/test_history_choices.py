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


if __name__=='__main__':unittest.main()
