"""Observed polynomial-proof stages: accepted answers survive partial submissions."""
import copy,json,random,tempfile,unittest
from pathlib import Path
from unittest.mock import Mock
from playwright.sync_api import sync_playwright
from browser import CaptureBrowser,EXTRACT
from core import Pacer
from capture import arguments

FIXTURE=Path(__file__).parent/'fixtures/staged-proof'
class StagedProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw=sync_playwright().start();cls.browser=cls.pw.chromium.launch(headless=True)
    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.pw.stop()
    def setUp(self):
        self.page=self.browser.new_page();self.page.route('**/*',lambda r:r.abort())
        self.page.set_content((FIXTURE/'accepted.html').read_text())
    def tearDown(self):self.page.close()
    def test_real_math_select_markers_and_accepted_fields(self):
        item=self.page.locator('#step-q334055').evaluate(EXTRACT)
        self.assertEqual(item['errors'],[])
        self.assertEqual(len(item['fields']),5)
        for field in item['fields']:
            self.assertIn('{{'+field['key']+'}}',item['problem'])
        self.assertEqual([f.get('source_result') for f in item['fields']],['Correct','Correct',None,None,None])
        self.assertEqual(item['fields'][1]['source_correct'],{'type':'math','value':r'|f(x)|\le K|g(x)|'})
        self.assertNotIn('(S',item['problem'])
    def test_server_accepted_stage_recovery_preserves_first_fields_without_resubmit(self):
        self.page.set_content((FIXTURE/'before.html').read_text())
        before=self.page.locator('#step-q334055').evaluate(EXTRACT)
        answers=[dict(key=f['key'],correct_option='0',correct_value=f['choices'][0]['value'],value_type=f['choices'][0]['type'],wrong_value=f['choices'][-1]['value'],correct_keys=[],wrong_keys=[]) for f in before['fields']]
        for f in before['fields']:f.update(submitted_value=f['choices'][0]['value'],submitted_option='0')
        record=dict(before=before,decision=dict(confident=True,explanation='fixture',answers=answers),intended='C',status='submitting')
        self.page.set_content((FIXTURE/'accepted.html').read_text())
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--state-dir',work,'--event-min','0','--event-max','0','--answer-min','0','--answer-max','0'])
            solver=Mock();b=CaptureBrowser(self.page,args,Pacer(args,random.Random(1)),solver)
            # Stop at the next read-only solver call. No answer entry may happen
            # before the old submission is recognized as accepted.
            solver.solve.side_effect=RuntimeError('next stage solve')
            with self.assertRaisesRegex(RuntimeError,'next stage solve'):
                b.proof_question(self.page.locator('#step-q334055'),record,Path(work),'q-334055',lambda:None)
            self.assertEqual(len(record['before']['fields']),5)
            self.assertEqual(record['proof_stages'][0]['outcome'],'accepted')
            self.assertEqual(record['proof_stages'][0]['submitted_keys'],['field-1','field-2'])
            self.assertEqual(record['before']['fields'][0]['submitted_value'],'positive')
            self.assertEqual(len(record['decision']['answers']),2)
    def test_no_source_grade_does_not_replay_uncertain_submission(self):
        self.page.set_content((FIXTURE/'before.html').read_text())
        scope=self.page.locator('#step-q334055');item=scope.evaluate(EXTRACT)
        record=dict(before=item,decision={'answers':[]},intended='C',status='submitting')
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--state-dir',work]);solver=Mock()
            b=CaptureBrowser(self.page,args,Pacer(args,random.Random(1)),solver)
            with self.assertRaisesRegex(ValueError,'source outcome'):
                b.proof_question(scope,record,Path(work),'q-334055',lambda:None)
            solver.solve.assert_not_called()
    def test_recovered_stage_submits_only_new_fields_and_saves_terminal_artifacts(self):
        self.page.set_content((FIXTURE/'before.html').read_text())
        initial=self.page.locator('#step-q334055').evaluate(EXTRACT)
        answers=[dict(key=f['key'],correct_option='0',correct_value=f['choices'][0]['value'],value_type=f['choices'][0]['type'],wrong_value=f['choices'][-1]['value'],correct_keys=[],wrong_keys=[]) for f in initial['fields']]
        for f in initial['fields']:f.update(submitted_value=f['choices'][0]['value'],submitted_option='0')
        record=dict(before=initial,decision=dict(confident=True,explanation='fixture',answers=answers),intended='C',status='submitting')
        self.page.set_content((FIXTURE/'accepted.html').read_text())
        self.page.evaluate('''()=>{let n=document.querySelector('#step-q334055');n.insertAdjacentHTML('afterend','<div id="continueButton-q334055" style="display:none">Continue</div>');n.querySelector('.questionWidget-submitButton').onclick=()=>{window.submissions=(window.submissions||0)+1;n.insertAdjacentHTML('beforeend','<div class="questionWidget-result">Correct</div><div class="questionWidget-explanation">By the triangle inequality the polynomial is bounded by 11 for |x|&lt;1.</div>');document.getElementById('continueButton-q334055').style.display='block';};}''')
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--state-dir',work,'--event-min','0','--event-max','0','--answer-min','0','--answer-max','0'])
            solver=Mock()
            def solve(item,*args):
                ans=[]
                for f in item['fields']:
                    c=next((c for c in f['choices'] if {k:c[k] for k in ('type','value')}==f.get('source_correct')),f['choices'][0])
                    ans.append(dict(key=f['key'],correct_option=c['option'],correct_value=c['value'],value_type=c['type'],wrong_value=f['choices'][-1]['value'],correct_keys=[],wrong_keys=[]))
                return dict(confident=True,explanation='fixture',answers=ans)
            solver.solve.side_effect=solve
            b=CaptureBrowser(self.page,args,Pacer(args,random.Random(1)),solver)
            entered=[]
            def enter(scope,record):
                entered.extend(record['entry_keys'])
                for f in record['before']['fields']:
                    if f['key'] in record['entry_keys']:
                        c=f['choices'][0];f.update(submitted_value=c['value'],submitted_option=c['option'])
                        self.page.locator('#'+f['frame_id']).evaluate('(n,html)=>n.innerHTML=html',c['html'])
                self.page.locator('.questionWidget-submitButton').evaluate("n=>n.classList.remove('disabledButton')")
            b.enter=enter;b.verify_entered=Mock()
            b.proof_question(self.page.locator('#step-q334055'),record,Path(work),'q-334055',lambda:None)
            self.assertEqual(entered,['field-3','field-4','field-5'])
            self.assertEqual(self.page.evaluate('window.submissions'),1)
            self.assertEqual(record['status'],'graded')
            self.assertEqual(len(record['decision']['answers']),5)
            self.assertEqual(len(record['proof_stages']),2)
            for stem in ('q-334055-before','q-334055-after'):
                self.assertTrue((Path(work)/(stem+'.json')).is_file())
                self.assertTrue((Path(work)/(stem+'.png')).is_file())
    def test_one_wrong_choice_across_retry_and_later_stage(self):
        self.page.set_content('<select id="s1"><option value="0">positive</option><option value="1">real</option></select><select id="s2"><option value="0">bounded</option><option value="1">unbounded</option></select>')
        fields=[dict(key='field-'+str(i),dom_id='s'+str(i),type='select',tag='select',choices=[dict(option='0',type='text',value=value),dict(option='1',type='text',value=wrong)]) for i,value,wrong in [(1,'positive','real'),(2,'bounded','unbounded')]]
        answers=[dict(key=f['key'],correct_option='0',correct_value=f['choices'][0]['value']) for f in fields]
        record=dict(before={'fields':fields},decision={'answers':answers},intended='W',entry_keys=['field-1'])
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--state-dir',work,'--event-min','0','--event-max','0'])
            b=CaptureBrowser(self.page,args,Pacer(args,random.Random(1)),None)
            b.enter(self.page.locator('body'),record)
            self.assertEqual(self.page.locator('#s1').input_value(),'1')
            self.assertTrue(record['wrong_submission_used'])
            b.enter(self.page.locator('body'),record)
            self.assertEqual(self.page.locator('#s1').input_value(),'0')
            record['entry_keys']=['field-2'];b.enter(self.page.locator('body'),record)
            self.assertEqual(self.page.locator('#s2').input_value(),'0')
            self.assertEqual(record['intended'],'W')
