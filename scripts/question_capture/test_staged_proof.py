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
    def test_intermediate_stage_ignores_css_hidden_spinner(self):
        self.page.set_content((FIXTURE/'before.html').read_text())
        scope=self.page.locator('#step-q334055');initial=scope.evaluate(EXTRACT)
        answers=[dict(key=f['key'],correct_option='0',correct_value=f['choices'][0]['value'],value_type=f['choices'][0]['type'],wrong_value=f['choices'][-1]['value'],correct_keys=[],wrong_keys=[]) for f in initial['fields']]
        record=dict(before=initial,decision=dict(confident=True,explanation='fixture',answers=answers),intended='C',status='prepared')
        accepted=(FIXTURE/'accepted.html').read_text().replace('class="questionWidget-spinnerFrame"','class="questionWidget-spinnerFrame" style="visibility:hidden"').replace('class="questionWidget-spinner"','class="questionWidget-spinner" style="display:block"')
        self.page.evaluate('(html)=>document.querySelector(".questionWidget-submitButton").onclick=()=>document.getElementById("step-q334055").outerHTML=html',accepted)
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--state-dir',work,'--timeout-ms','500','--event-min','0','--event-max','0','--answer-min','0','--answer-max','0'])
            solver=Mock();solver.solve.side_effect=RuntimeError('next stage solve')
            b=CaptureBrowser(self.page,args,Pacer(args,random.Random(1)),solver)
            def enter(scope,record):
                for f in record['before']['fields']:
                    f.update(submitted_value=f['choices'][0]['value'],submitted_option='0')
                self.page.locator('.questionWidget-submitButton').evaluate("n=>n.classList.remove('disabledButton')")
            b.enter=enter;b.verify_entered=Mock()
            with self.assertRaisesRegex(RuntimeError,'next stage solve'):
                b.proof_question(scope,record,Path(work),'q-334055',lambda:None)
            self.assertEqual(record['proof_stages'][0]['outcome'],'accepted')
    def test_rejected_wrong_stage_retries_correctly_before_next_stage(self):
        self.page.set_content((FIXTURE/'before.html').read_text())
        scope=self.page.locator('#step-q334055');initial=scope.evaluate(EXTRACT)
        answers=[dict(key=f['key'],correct_option='0',correct_value=f['choices'][0]['value'],value_type=f['choices'][0]['type'],wrong_value=f['choices'][-1]['value'],correct_keys=[],wrong_keys=[]) for f in initial['fields']]
        for f in initial['fields']:
            c=f['choices'][-1] if f['key']=='field-1' else f['choices'][0]
            f.update(submitted_value=c['value'],submitted_option=c['option'])
            self.page.locator('#'+f['frame_id']).evaluate('(n,html)=>n.innerHTML=html',c['html'])
        self.page.locator('#step-q334055').evaluate('(n,html)=>n.insertAdjacentHTML("beforeend",html)', "<div class='questionWidget-feedback'>Oops, that's not quite right. Please try again.</div>")
        record=dict(before=initial,decision=dict(confident=True,explanation='fixture',answers=answers),intended='W',status='submitting')
        self.page.evaluate('(html)=>document.querySelector(".questionWidget-submitButton").onclick=()=>document.getElementById("step-q334055").outerHTML=html',(FIXTURE/'accepted.html').read_text())
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--state-dir',work,'--timeout-ms','1000','--event-min','0','--event-max','0','--answer-min','0','--answer-max','0'])
            solver=Mock();solver.solve.side_effect=RuntimeError('next stage solve')
            b=CaptureBrowser(self.page,args,Pacer(args,random.Random(1)),solver)
            entered=[]
            def enter(scope,record):
                self.assertTrue(record['wrong_submission_used'])
                entered.append(record['entry_keys'])
                for f in record['before']['fields']:
                    c=f['choices'][0];f.update(submitted_value=c['value'],submitted_option=c['option'])
                self.page.locator('.questionWidget-submitButton').evaluate("n=>n.classList.remove('disabledButton')")
            b.enter=enter;b.verify_entered=Mock()
            with self.assertRaisesRegex(RuntimeError,'next stage solve'):
                b.proof_question(scope,record,Path(work),'q-334055',lambda:None)
            self.assertEqual(entered,[['field-1','field-2']])
            self.assertEqual([s['outcome'] for s in record['proof_stages']],['rejected','accepted'])
            self.assertEqual(record['intended'],'W')
    def test_actual_accepted_disabled_frame_is_captured_before_whole_grade(self):
        self.page.set_content((FIXTURE/'accepted-disabled.html').read_text())
        item=self.page.locator('#step-q334055').evaluate(EXTRACT)
        self.assertEqual(item['errors'],[])
        self.assertEqual(len(item['fields']),8)
        self.assertEqual(item['fields'][5]['frame_id'],'selectListFrame-334055-5')
        self.assertEqual(item['fields'][5]['source_correct'],{'type':'math','value':'3'})
        record=json.loads((FIXTURE/'pending-six.json').read_text())
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--state-dir',work]);solver=Mock();solver.solve.side_effect=RuntimeError('next stage solve')
            b=CaptureBrowser(self.page,args,Pacer(args,random.Random(1)),solver)
            with self.assertRaisesRegex(RuntimeError,'next stage solve'):
                b.proof_question(self.page.locator('#step-q334055'),record,Path(work),'q-334055',lambda:None)
            self.assertEqual(record['proof_stages'][0]['submitted_keys'],['field-6'])
            self.assertEqual(record['proof_stages'][0]['outcome'],'accepted')
            self.assertEqual(len(record['before']['fields']),8)
    def test_actual_stage_wait_accepts_disabled_frame_and_zero_area_spinner(self):
        self.page.set_content((FIXTURE/'before-six.html').read_text())
        self.page.evaluate('(html)=>document.querySelector(".questionWidget-submitButton").onclick=()=>document.getElementById("step-q334055").outerHTML=html',(FIXTURE/'accepted-disabled.html').read_text())
        record=json.loads((FIXTURE/'pending-six.json').read_text());record['status']='prepared';record.pop('proof_pending')
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--state-dir',work,'--timeout-ms','1000','--event-min','0','--event-max','0','--answer-min','0','--answer-max','0'])
            solver=Mock();solver.solve.side_effect=RuntimeError('next stage solve')
            b=CaptureBrowser(self.page,args,Pacer(args,random.Random(1)),solver)
            def enter(scope,record):
                self.assertEqual(record['entry_keys'],['field-6'])
                self.page.locator('.questionWidget-submitButton').evaluate("n=>n.classList.remove('disabledButton')")
                for f in record['before']['fields']:
                    if f['key']=='field-6':f.update(submitted_value='3',submitted_option='2')
            b.enter=enter;b.verify_entered=Mock()
            with self.assertRaisesRegex(RuntimeError,'next stage solve'):
                b.proof_question(self.page.locator('#step-q334055'),record,Path(work),'q-334055',lambda:None)
            self.assertEqual(record['proof_stages'][0]['outcome'],'accepted')
    def test_initial_dynamic_select_dispatches_before_proof_sections_exist(self):
        self.page.set_content('<div id="stepButton-q334064" class="stepButton current"></div><div id="finalScreen" style="display:none"></div>'+(FIXTURE/'initial-dynamic.html').read_text())
        scope=self.page.locator('#step-q334064')
        self.assertEqual(scope.locator('.proofSection').count(),0)
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--state-dir',work,'--event-min','0','--event-max','0'])
            solver=Mock()
            def solve(item,*args):
                answers=[dict(key=f['key'],correct_option='0',correct_value=f['choices'][0]['value'],value_type=f['choices'][0]['type'],wrong_value=f['choices'][-1]['value'],correct_keys=[],wrong_keys=[])for f in item['fields']]
                return dict(confident=True,explanation='fixture',answers=answers)
            solver.solve.side_effect=solve
            b=CaptureBrowser(self.page,args,Pacer(args,random.Random(1)),solver)
            b.proof_question=Mock(side_effect=RuntimeError('staged player'))
            b.enter=Mock(side_effect=RuntimeError('ordinary player'))
            state=dict(task_id=1,task_type='lesson',questions={},current_kp='kp',kps={'kp':dict(id='kp',title='Polynomial order',sequence='CWCWC')})
            with self.assertRaisesRegex(RuntimeError,'staged player'):b.activity(state,Path(work),{})
            b.proof_question.assert_called_once()
            b.enter.assert_not_called()
            self.page.locator('.questionWidget-healthFrame').evaluate('n=>n.remove()')
            self.assertFalse(b.is_staged_question(scope))
    def test_saved_rejection_binds_restored_same_selections_and_lower_health(self):
        restored=json.loads((FIXTURE/'restored-rejected.json').read_text())
        self.page.set_content(restored['html'])
        record=json.loads((FIXTURE/'pending-rejected.json').read_text())
        with tempfile.TemporaryDirectory() as work:
            source=Path(work)/'diagnostics/saved/current-question.json';source.parent.mkdir(parents=True)
            source.write_bytes((FIXTURE/'rejected.json').read_bytes())
            args=arguments(['run','--state-dir',work,'--event-min','0','--event-max','0'])
            b=CaptureBrowser(self.page,args,Pacer(args,random.Random(1)),Mock())
            b.enter=Mock(side_effect=RuntimeError('correct retry'))
            with self.assertRaisesRegex(RuntimeError,'correct retry'):
                b.proof_question(self.page.locator('#step-q334064'),record,Path(work),'q-334064',lambda:None)
            self.assertTrue(record['wrong_submission_used'])
            self.assertEqual(record['proof_stages'][0]['outcome'],'rejected')
            evidence=record['proof_stages'][0]['restored_rejection_evidence']
            self.assertEqual(evidence['before_health_percent'],0)
            self.assertEqual(evidence['restored_health_percent'],20)
            self.assertEqual(evidence['path'],str(source.resolve()))
    def test_saved_rejection_rejects_changed_health_or_selection(self):
        restored=json.loads((FIXTURE/'restored-rejected.json').read_text())
        record=json.loads((FIXTURE/'pending-rejected.json').read_text())
        with tempfile.TemporaryDirectory() as work:
            source=Path(work)/'diagnostics/saved/current-question.json';source.parent.mkdir(parents=True)
            source.write_bytes((FIXTURE/'rejected.json').read_bytes())
            wrong=copy.deepcopy(restored);wrong['html']=wrong['html'].replace('width: 20%;','width: 40%;')
            self.assertIsNone(CaptureBrowser.restored_proof_rejection(work,record,wrong))
            wrong=copy.deepcopy(restored);wrong['fields'][0]['source_selected']['value']='positive'
            self.assertIsNone(CaptureBrowser.restored_proof_rejection(work,record,wrong))
    def test_completed_proof_is_finalized_when_restored_on_next_question(self):
        for actual in ('Correct','Partial Credit'):
            with self.subTest(actual=actual),tempfile.TemporaryDirectory() as work:
                before=json.loads((FIXTURE/'completed-first.json').read_text());before['status']='submitting'
                after=json.loads((FIXTURE/'completed-first-after.json').read_text());after['result']=actual
                (Path(work)/'q-334055-after.json').write_text(json.dumps(after))
                self.page.set_content('<div id="stepButton-q334064" class="stepButton current"></div><div id="finalScreen" style="display:none"></div>'+after['html'].replace('class="step questionWidget"','class="step questionWidget" hidden')+(FIXTURE/'initial-dynamic.html').read_text())
                args=arguments(['run','--state-dir',work,'--event-min','0','--event-max','0'])
                solver=Mock();solver.solve.side_effect=RuntimeError('next question solve')
                b=CaptureBrowser(self.page,args,Pacer(args,random.Random(1)),solver)
                b.finalize_question=Mock(side_effect=lambda state,directory,mid,record:record.update(finalized=True))
                state=dict(task_id=1,task_type='lesson',questions={'q-334055':before},current_kp=before['kp_id'],kps=json.loads((FIXTURE/'completed-first-kps.json').read_text()))
                with self.assertRaisesRegex(RuntimeError,'next question solve'):b.activity(state,Path(work),{})
                self.assertTrue(before['finalized'])
                self.assertEqual(before['actual_result'],actual)
                b.finalize_question.assert_called_once()
