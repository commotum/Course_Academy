"""Offline adaptive replay of authentic diagnostic DOM and recovery boundaries."""
import base64
import contextlib
import copy
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from browser import CaptureBrowser
from capture import arguments, run, unfinished_run
from core import Pacer, atomic_json, build_content_transaction, choose_activity, stable_id
from diagnostic import bind_history, classify, completed_url, configure, covered_policy, policy_fingerprint, take_diagnostic
from saved_imports import eligible
from solver import Solver, response_schema

FIXTURES = Path(__file__).parent/'fixtures'
EXAM = json.loads((FIXTURES/'diagnostic-multivariable.json').read_text())
POLICY = {'course_id':54,'topics':[{'topic_id':int(t['topic-id']),'title':t['topic-name']}
                                 for t in EXAM['policy']['topics']]}

COVERED = {'mode':'covered_topics_only','course_id':54,
           'covered_topics':[{'topic_id':2036,'title':'Covered prerequisite'},
                             {'topic_id':3052,'title':'Covered overlapping course topic'}],
           'blocked_topics':[{'topic_id':3340,'title':'Uncovered course topic'},
                             {'topic_id':2036,'title':'Covered overlap takes precedence'}],
           'provenance':{'account_id':'fixture','observed_at':'2026-10-09'}}


class DiagnosticPolicyTests(unittest.TestCase):
    def test_course_membership_uses_topic_identity_not_other_course_membership(self):
        self.assertEqual(classify(POLICY,{},2036),'prerequisite')
        self.assertEqual(classify(POLICY,{},3340),'in_course')
        self.assertEqual(classify(POLICY,{'diagnostic_classification':'in_course','diagnostic_topic_id':3052}),'in_course')
        with self.assertRaises(ValueError):
            classify(POLICY,{'diagnostic_classification':'in_course','diagnostic_topic_id':2036})

    def test_skips_need_classification_but_do_not_need_a_prediction_before_solution(self):
        item={'diagnostic_policy':POLICY,'fields':[{'key':'selection','type':'radio'}]}
        Solver.validate(item,{'confident':True,'answers':[],
                             'diagnostic_classification':'in_course','diagnostic_topic_id':3052})
        with self.assertRaises(ValueError):
            Solver.validate(item,{'confident':True,'answers':[],
                                 'diagnostic_classification':'prerequisite','diagnostic_topic_id':None})
        self.assertNotIn('diagnostic_classification',response_schema({})['properties'])
        self.assertIn('diagnostic_classification',response_schema(item)['required'])

    def test_policy_is_saved_before_start_and_resume_uses_it(self):
        with tempfile.TemporaryDirectory() as work:
            path=Path(work)/'Topics.csv';path.write_text('topic-id,topic-number,topic-name\n3052,1,Joint Distributions\n')
            args=arguments(['run','--diagnostic-topics',str(path)])
            state={};configure(args,{'course_id':54},state,Path(work)/'capture')
            self.assertEqual(state['progress_course_ids'],[54])
            self.assertEqual(state['diagnostic_policy']['topics'][0]['topic_id'],3052)
            path.unlink();configure(args,{},state,Path(work)/'capture')
            self.assertEqual(state['course_id'],54)

    def test_covered_allowlist_answers_overlap_and_skips_every_unsupplied_id(self):
        self.assertEqual(classify(COVERED,{},3052),'covered')
        self.assertEqual(classify(COVERED,{},2036),'covered')
        self.assertEqual(classify(COVERED,{},3340),'uncovered')
        self.assertEqual(classify(COVERED,{},9999),'uncovered')
        self.assertEqual(classify(COVERED,{'diagnostic_classification':'covered','diagnostic_topic_id':3052,'confident':True}),'covered')
        for decision in ({}, {'diagnostic_classification':'prerequisite','diagnostic_topic_id':None},
                         {'diagnostic_classification':'covered','diagnostic_topic_id':9999,'confident':True},
                         {'diagnostic_classification':'covered','diagnostic_topic_id':3052,'confident':False},
                         {'diagnostic_classification':'unknown','diagnostic_topic_id':None,'confident':True}):
            self.assertEqual(classify(COVERED,decision),'unknown')

    def test_covered_unknown_and_uncertain_classification_allow_skip_but_covered_requires_answer(self):
        item={'diagnostic_policy':COVERED,'fields':[{'key':'selection','type':'radio'}]}
        Solver.validate(item,{'confident':False,'answers':[],
                             'diagnostic_classification':'unknown','diagnostic_topic_id':None})
        with self.assertRaises(ValueError):
            Solver.validate(item,{'confident':True,'answers':[],
                                 'diagnostic_classification':'covered','diagnostic_topic_id':3052})
        schema=response_schema(item)
        self.assertEqual(schema['properties']['diagnostic_classification']['enum'],['covered','uncovered','unknown'])
        self.assertEqual(set(schema['properties']['diagnostic_topic_id']['enum']),{None,2036,3052,3340})

    def test_covered_snapshot_is_frozen_with_provenance_without_course_graph(self):
        with tempfile.TemporaryDirectory() as work:
            path=Path(work)/'covered.json';atomic_json(path,COVERED)
            args=arguments(['run','--diagnostic-covered-topics',str(path)])
            state={};directory=Path(work)/'capture'
            configure(args,{'course_id':54},state,directory)
            self.assertEqual(state['answer_policy'],'correct_covered_skip_unknown')
            self.assertEqual(state['diagnostic_policy']['covered_topics'],COVERED['covered_topics'])
            self.assertEqual(state['diagnostic_policy']['provenance'],COVERED['provenance'])
            self.assertEqual((directory/'diagnostic-covered-topics.json').read_bytes(),path.read_bytes())
            frozen=copy.deepcopy(state['diagnostic_policy'])
            path.unlink();configure(args,{},state,directory)
            self.assertEqual(state['diagnostic_policy'],frozen)

    def test_covered_snapshot_requires_provenance_and_allows_empty_covered_list(self):
        with tempfile.TemporaryDirectory() as work:
            path=Path(work)/'covered.json'
            atomic_json(path,{'covered_topics':[]})
            with self.assertRaises(ValueError):covered_policy(path,154)
            atomic_json(path,{'covered_topics':[],'provenance':{'account_id':'fixture'}})
            self.assertEqual(classify(covered_policy(path,154),{},2036),'uncovered')

    def test_strict_source_binding_refuses_every_unbound_semantic_match(self):
        strict={**COVERED,'require_source_binding':True}
        self.assertEqual(classify(strict,{},2036),'covered')
        self.assertEqual(classify(strict,{},3052),'covered')
        self.assertEqual(classify(strict,{},3340),'uncovered')
        self.assertEqual(classify(strict,{},99999),'uncovered')
        for topic in COVERED['covered_topics']:
            decision={'confident':True,'answers':[], 'diagnostic_classification':'covered',
                      'diagnostic_topic_id':topic['topic_id']}
            self.assertEqual(classify(strict,decision),'unknown')
            self.assertEqual(classify(COVERED,decision),'covered')

    def test_source_binding_flag_freezes_only_new_policies_and_validates_json_type(self):
        with tempfile.TemporaryDirectory() as work:
            path=Path(work)/'covered.json';atomic_json(path,{**COVERED,'require_source_binding':True})
            args=arguments(['run','--diagnostic-covered-topics',str(path)])
            state={};directory=Path(work)/'capture'
            configure(args,{'course_id':54},state,directory)
            self.assertTrue(state['diagnostic_policy']['require_source_binding'])
            legacy={'diagnostic_policy':copy.deepcopy(COVERED)}
            configure(args,{},legacy,directory)
            self.assertEqual(legacy['diagnostic_policy'],COVERED)
            atomic_json(path,{**COVERED,'require_source_binding':'yes'})
            with self.assertRaises(ValueError):covered_policy(path,54)
            atomic_json(path,{**COVERED,'require_source_binding':True})
            self.assertTrue(covered_policy(path,54)['require_source_binding'])

    def test_started_diagnostic_automatically_recovers_even_if_deferred(self):
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--output',work+'/captures','--state-dir',work+'/state'])
            root=args.output/'1'
            atomic_json(root/'state.json',{'task_id':1,'task_type':'diagnostic','diagnostic_started':True,
                                        'deferred_error':{'phase':'activity'}})
            self.assertEqual(unfinished_run(args),root.resolve())

    def test_completed_diagnostic_with_interrupted_history_recovers_without_retake(self):
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--output',work+'/captures','--state-dir',work+'/state'])
            root=args.output/'1'
            atomic_json(root/'state.json',{'task_id':1,'task_type':'diagnostic','diagnostic_started':True,
                                        'activity_complete':True,'deferred_error':{'phase':'history'}})
            self.assertEqual(unfinished_run(args),root.resolve())

    def test_diagnostic_selection_and_completion_are_distinct_from_fixed_quizzes(self):
        exam={'task_id':1,'task_type':'diagnostic','capture_supported':True}
        self.assertEqual(choose_activity([exam],{})['selection_reason'],'placement_diagnostic')
        self.assertIsNone(choose_activity([{**exam,'in_progress':True}],{}))
        state={'task_id':1,'diagnostic_id':2}
        self.assertTrue(completed_url(state,'https://mathacademy.com/tasks/1/diagnostics/2/analysis#'))
        self.assertFalse(completed_url(state,'https://mathacademy.com/tasks/1/diagnostics/3/analysis'))

    def test_batch_configures_diagnostic_before_start_and_imports_without_single_topic_lookup(self):
        activity={'task_id':1,'task_type':'diagnostic','diagnostic_id':2,'title':'Placement',
                  'topic_id':None,'course_id':54,'capture_supported':True,'href':'/tasks/1/diagnostics/2'}
        selected=[]
        class FixtureBrowser:
            def __init__(self,*args):pass
            def queue(self):return [] if selected else [activity]
            def start(self,a):
                checkpoint=json.loads((args.output/'1/state.json').read_text())
                self.policy=checkpoint['diagnostic_policy']
                selected.append(a)
            def activity(self,state,directory,topic):
                assert callable(topic)
                state['activity_complete']=True
            def history(self,state,*args):return {'task_id':1,'task_type':'diagnostic','questions':[]}
        db=Mock();db.priorities.return_value={};db.import_content.return_value={'previewed':True}
        runtime=Mock();runtime.__enter__=Mock(return_value=runtime);runtime.__exit__=Mock(return_value=False)
        runtime.chromium.launch_persistent_context.return_value=SimpleNamespace(pages=[Mock()],close=Mock(),route=Mock())
        with tempfile.TemporaryDirectory() as work:
            path=Path(work)/'Topics.csv';path.write_text('topic-id,topic-number,topic-name\n3052,1,Joint Distributions\n')
            args=arguments(['run','--preview','--state-dir',work+'/state','--output',work+'/captures',
                            '--diagnostic-topics',str(path),'--lesson-min','0','--lesson-max','0'])
            with patch('capture.Database',return_value=db),patch('browser.CaptureBrowser',FixtureBrowser), \
                 patch('playwright.sync_api.sync_playwright',return_value=runtime),patch('builtins.print'):
                run(args)
            state=json.loads((args.output/'1/state.json').read_text())
            self.assertTrue(state['preview_complete']);self.assertEqual(state['diagnostic_id'],2)
            self.assertEqual(selected[0]['selection_reason'],'placement_diagnostic')
            db.topic.assert_not_called();db.import_content.assert_called_once()

    def test_observation_timeout_retries_are_bounded_without_navigation(self):
        from playwright.sync_api import TimeoutError
        reader=Mock();state={}
        with tempfile.TemporaryDirectory() as work,patch('diagnostic._take_diagnostic',side_effect=TimeoutError('late response')) as take:
            with self.assertRaises(TimeoutError):take_diagnostic(reader,state,Path(work))
        self.assertEqual(take.call_count,3)
        self.assertEqual(reader.pacer.backoff.call_count,2)
        reader.navigate.assert_not_called()


class DiagnosticReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.runtime=sync_playwright().start()
        cls.browser=cls.runtime.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.runtime.stop()

    def setUp(self):
        self.work=tempfile.TemporaryDirectory();self.root=Path(self.work.name)
        self.context=self.browser.new_context(offline=True);self.page=self.context.new_page()
        self.page.set_default_timeout(1500)
        self.context.route('https://mathacademy.com/**',self.respond)
        self.started=False;self.current=0;self.graded=set();self.submissions=[];self.nexts=[]
        self.solver_calls=[]
        self.retry_indices=set();self.retries=[];self.direct_finish=False

    def tearDown(self):
        self.context.close();self.work.cleanup()

    def document(self):
        if not self.started:
            return '<div id="initialScreen"><div id="initialScreen-startButton" onclick="fetch(\'/fixture/start\').then(()=>location.reload())">START</div></div>'
        if self.current>=len(EXAM['questions']):
            return '<div class="courseFrame">Analysis</div>'
        q=EXAM['questions'][self.current]
        graded=self.current in self.graded
        body=q['after_html' if graded else 'before_html']
        body+='<div id="nextButton" style="display:'+('block' if graded else 'none')+'">Next</div><div id="doneButton" style="display:none">Done</div>'
        body+='<script src="/vendor/jquery-3.7.1.min.js"></script><script src="/vendor/mathquill-ma.v2.1.min.js"></script><link rel="stylesheet" href="/vendor/mathquill-0.10.1.css">'
        body+='<script>const after='+json.dumps(q['after_html'])+';'
        body+='''
          document.querySelectorAll('.matheditor-wrapper-answer').forEach(n=>{n.innerHTML='';const e=document.createElement('div');n.append(e);MathQuill.getInterface(2).MathField(e,{handlers:{edit:()=>document.querySelector('.questionWidget-submitButton').classList.remove('disabledButton')}})});
          document.querySelectorAll('.questionWidget-choiceLetterCircle').forEach(n=>n.onclick=()=>{document.querySelectorAll('.questionWidget-choiceLetterCircle').forEach(c=>{c.style.background='';c.style.color=''});n.style.background='rgb(64,64,64)';n.style.color='white';document.querySelector('.questionWidget-submitButton').classList.remove('disabledButton')});
          document.querySelectorAll('.questionWidget-submitButton,.questionWidget-skipButton').forEach(n=>n.onclick=()=>fetch('/fixture/grade/'+(n.classList.contains('questionWidget-skipButton')?'skip':'answer')).then(()=>{document.querySelector('#questionContainer').outerHTML=after;document.querySelector('#nextButton').style.display='block'}));
          document.querySelector('#nextButton').onclick=()=>fetch('/fixture/next').then(r=>r.text()).then(url=>location.href=url);
        </script>'''
        if self.current in self.retry_indices:
            body+='''<div id="retryScreen" style="display:none"><div id="retryScreen-yesButton">Yes</div><div id="retryScreen-noButton">No</div></div><script>
              document.querySelector('#nextButton').onclick=()=>document.querySelector('#retryScreen').style.display='block';
              ['yes','no'].forEach(choice=>document.querySelector('#retryScreen-'+choice+'Button').onclick=()=>{
                document.querySelector('#retryScreen').style.display='none';
                fetch('/fixture/retry/'+choice).then(r=>r.text()).then(url=>setTimeout(()=>location.href=url,150));
              });</script>'''
        if self.direct_finish and self.current == len(EXAM['questions'])-1:
            body += '''<script>document.querySelectorAll('.questionWidget-submitButton,.questionWidget-skipButton').forEach(n=>
              n.onclick=()=>fetch('/fixture/grade/'+(n.classList.contains('questionWidget-skipButton')?'skip':'answer'))
                .then(()=>location.href='/tasks/1/diagnostics/2/analysis#'));</script>'''
        return body

    def respond(self,route):
        url=route.request.url
        if url in EXAM['assets']:
            a=EXAM['assets'][url];route.fulfill(content_type=a['content_type'],body=base64.b64decode(a['bytes']));return
        if '/vendor/' in url:
            f=FIXTURES/'vendor'/url.rsplit('/',1)[1]
            if not f.exists():
                route.fulfill(status=404,body='');return
            route.fulfill(content_type='text/css' if f.suffix=='.css' else 'text/javascript',body=f.read_bytes());return
        if '/fixture/start' in url:
            self.started=True;body='OK'
        elif '/fixture/grade/' in url:
            self.graded.add(self.current);self.submissions.append((self.current,url.rsplit('/',1)[1]));body='OK'
            if self.direct_finish and self.current==len(EXAM['questions'])-1:self.current+=1
        elif '/fixture/next' in url or '/fixture/retry/' in url:
            if '/fixture/retry/' in url:self.retries.append((self.current,url.rsplit('/',1)[1]))
            self.nexts.append(self.current);self.current+=1
            body='/tasks/1/diagnostics/2'+('/analysis#' if self.current==len(EXAM['questions']) else '')
        elif '?taskId=' in url:
            body=''.join(q['history']['raw_html']+q['solution_html'].replace('class="questionExplanation"','class="questionExplanation" style="display:none"') for q in EXAM['questions'])
            body+='<script>document.querySelectorAll(".answerDetails").forEach(n=>n.onclick=()=>n.closest(".question").nextElementSibling.style.display="block")</script>'
        elif '/diagnostics/' in url:
            body=self.document()
        elif '/img/' in url:
            route.fulfill(status=404,body='');return
        else:
            body='<a class="courseNameLink" href="/courses/54/progress">Multivariable Calculus</a><div id="completedTasks"></div><div id="incompleteTasks"><div id="task-1" class="taskUnlocked" progress="0"><span class="taskTypeUnlocked">Diagnostic</span><div class="taskNameUnlocked">Multivariable Calculus: Placement Exam</div><div class="taskDetails" style="display:none"><a id="taskStartButton-1" class="taskStartButton" href="/tasks/1/diagnostics/2">Start</a></div></div></div><script>document.querySelector(".taskNameUnlocked").parentElement.onclick=()=>document.querySelector(".taskDetails").style.display="block"</script>'
        route.fulfill(content_type='text/html; charset=utf-8',body=body)

    def reader(self):
        args=arguments(['run','--timeout-ms','1500','--settle-ms','0','--event-min','0','--event-max','0','--answer-min','0','--answer-max','0'])
        owner=self
        class FixtureSolver:
            def solve(self,item,screenshot,directory,phase='solve'):
                owner.solver_calls.append((phase,str(directory)))
                if phase=='diagnostic' and any(f['type']=='radio' for f in item['fields']):
                    field=next(f for f in item['fields'] if f['type']=='radio')
                    source=int(field['choices'][0]['dom_id'].split('-')[-2])
                    topic=next(q['topic_id'] for q in EXAM['questions'] if q['history']['id']=='question-'+str(source))
                    return {'confident':True,'answers':[],'explanation':'Course skill',
                            'diagnostic_classification':'in_course','diagnostic_topic_id':topic}
                answers=[]
                for f in item['fields']:
                    if f['type']=='radio':
                        source=int(f['choices'][0]['dom_id'].split('-')[-2])
                        q=next(q for q in EXAM['questions'] if q['history']['id']=='question-'+str(source))
                        c=next(c for c in f['choices'] if c['option']==q['correct_answers'][0]['correct_option'])
                        answers.append({'key':f['key'],'correct_option':c['option'],'correct_value':c['value'],'value_type':c['type'],'wrong_value':None,'correct_keys':[],'wrong_keys':[]})
                    else:
                        answers.append({'key':f['key'],'correct_option':None,'correct_value':'2','value_type':'math','wrong_value':'0','correct_keys':[{'text':'2','key':None}],'wrong_keys':[{'text':'0','key':None}]})
                return {'confident':True,'answers':answers,'explanation':'Checked captured answer',
                        'diagnostic_classification':'prerequisite','diagnostic_topic_id':None}
        reader=CaptureBrowser(self.page,args,Pacer(args,sleeper=lambda _:None),FixtureSolver())
        reader.database=Mock();reader.database.query.side_effect=lambda _,inputs,*a:[[2036]] if inputs==['q-136396'] else []
        reader.knowledge_snapshot=Mock()
        return reader

    def state(self):
        return {'task_id':1,'diagnostic_id':2,'course_id':54,'task_type':'diagnostic','topic_id':None,
                'activity_url':'https://mathacademy.com/tasks/1/diagnostics/2','questions':{},'examples':{},
                'diagnostic_policy':POLICY,'answer_policy':'correct_prerequisites_skip_course'}

    def start(self,reader,state):
        atomic_json(self.root/'state.json',state)
        reader.navigate(state['activity_url']);take_diagnostic(reader,state,self.root)

    def load_topic(self,tid,*_):
        qs=[q for q in EXAM['questions'] if q['topic_id']==tid]
        return {':topic/id':stable_id('topic',str(tid)),':topic/math-academy-id':tid,':topic/title':str(tid),
                ':topic/knowledge-points':[{':knowledge-point/id':stable_id('kp',str(q['knowledge_point_source_id'])),
                                          ':knowledge-point/title':q['history']['kp_title']} for q in qs]}

    def test_queue_start_adaptive_radio_image_and_mathquill_history_and_import(self):
        reader=self.reader();queue=reader.queue()
        self.assertEqual(queue[0]['diagnostic_id'],2);self.assertEqual(queue[0]['course_id'],54)
        self.assertTrue(queue[0]['capture_supported']);reader.start(queue[0])
        state=self.state();atomic_json(self.root/'state.json',state)
        take_diagnostic(reader,state,self.root)
        self.assertEqual(self.submissions,[(0,'answer'),(1,'skip'),(2,'skip'),(3,'answer')])
        self.assertEqual(self.nexts,[0,1,2,3]);self.assertTrue(state['diagnostic_complete'])
        reader.knowledge_snapshot.assert_called_once_with(state,self.root,'diagnostic-completed')
        content=reader.history(state,self.root,self.load_topic)
        self.assertEqual(len(content['questions']),4);self.assertTrue(eligible(self.root,state,content))
        self.assertEqual(state['questions']['q-314250']['history_classification'],'prerequisite')
        self.assertEqual(state['questions']['q-111251']['live_result'],'Skipped Question')
        self.assertEqual(state['questions']['q-111251']['actual_result'],'Incorrect')
        tx,_=build_content_transaction(content,{q['topic_id']:self.load_topic(q['topic_id']) for q in content['questions']},{})
        self.assertTrue(tx);self.assertTrue(all('learner' not in str(d) and 'engine/' not in str(d) for d in tx))
        manifest=json.loads((self.root/'assets/manifest.json').read_text())
        self.assertTrue(manifest);self.assertTrue(all(a['representation']=='original' for a in manifest.values()))
        self.assertEqual(sum(phase=='verify' for phase,_ in self.solver_calls),2)

    def test_final_skip_direct_analysis_completion_recovers_authentic_history_grade(self):
        self.direct_finish=True
        reader=self.reader();state=self.state()
        state['diagnostic_policy']={**COVERED,'covered_topics':[]}
        reader.solver.solve=lambda *args: {'confident':True,'answers':[],
                                         'diagnostic_classification':'unknown','diagnostic_topic_id':None}
        self.start(reader,state)
        self.assertTrue(state['diagnostic_complete'])
        self.assertEqual(self.submissions,[(0,'skip'),(1,'skip'),(2,'skip'),(3,'skip')])
        last=state['questions']['question-004']
        self.assertEqual(last['status'],'submitting')
        self.assertNotIn('after',last)
        self.assertFalse((self.root/'question-004-after.json').exists())
        # History validates numbered question identity, KP, grade and source HTML.
        metadata=[q['history'] for q in EXAM['questions']]
        original_before=copy.deepcopy(last['before'])
        bind_history(state,metadata)
        last=state['questions']['q-314250']
        self.assertEqual(last['status'],'graded')
        self.assertEqual(last['actual_result'],metadata[-1]['result'])
        self.assertIsNone(last['live_result'])
        self.assertEqual(last['intended'],'skip')
        self.assertEqual(last['before'],original_before)
        self.assertEqual(last['history_grade_recovery']['raw_html'],metadata[-1]['raw_html'])
        submissions=list(self.submissions)
        take_diagnostic(reader,state,self.root)
        self.assertEqual(self.submissions,submissions)

    def test_missing_final_grade_does_not_recover_from_missing_or_wrong_history_evidence(self):
        record={'sequence_position':1,'source_question_id':136396,'status':'submitting'}
        state={**self.state(),'questions':{'question-001':record}}
        metadata=[copy.deepcopy(EXAM['questions'][0]['history'])]
        metadata[0]['result']=None
        with self.assertRaises(ValueError):bind_history(state,metadata)
        self.assertEqual(record['status'],'submitting')
        metadata=[copy.deepcopy(EXAM['questions'][0]['history'])]
        metadata[0]['id']='question-999999'
        with self.assertRaises(ValueError):bind_history(state,metadata)
        self.assertEqual(record['status'],'submitting')

    def test_strict_binding_replay_answers_known_source_and_skips_unbound_without_solver(self):
        reader=self.reader();state=self.state()
        state['diagnostic_policy']={**COVERED,'require_source_binding':True}
        self.start(reader,state)
        self.assertEqual(self.submissions,[(0,'answer'),(1,'skip'),(2,'skip'),(3,'skip')])
        self.assertEqual(self.solver_calls,[('solve',str(self.root/'question-001'))])
        self.assertEqual([r['classification'] for r in state['questions'].values()],['covered','unknown','unknown','unknown'])

    def test_history_metadata_is_durable_before_slow_verification_turn(self):
        reader=self.reader();state=self.state();self.start(reader,state)
        original=reader.solver.solve
        def stop_verify(item,screenshot,directory,phase='solve'):
            if phase=='verify':raise KeyboardInterrupt('stop before slow history verification')
            return original(item,screenshot,directory,phase)
        reader.solver.solve=stop_verify
        with self.assertRaises(KeyboardInterrupt):reader.history(state,self.root,self.load_topic)
        metadata=json.loads((self.root/'activity-metadata.json').read_text())
        self.assertEqual(len(metadata),len(EXAM['questions']))
        self.assertEqual({q['id'] for q in metadata},{q['history']['id'] for q in EXAM['questions']})
        self.assertTrue(all(q['source_result']==q['result'] and q['raw_html'] for q in metadata))
        self.assertFalse(state.get('history_complete'))

    def test_covered_policy_replay_uses_bound_overlap_and_unbound_blank_skill(self):
        reader=self.reader();state=self.state();state['diagnostic_policy']=COVERED
        state['answer_policy']='correct_covered_skip_unknown'
        reader.database.query.side_effect=lambda _,inputs,*a:[[2036]] if inputs==['q-136396'] else [[3052]]
        original=reader.solver.solve
        def classify_blank(item,screenshot,directory,phase='solve'):
            answer=original(item,screenshot,directory,phase)
            if phase=='diagnostic':
                answer.update(diagnostic_classification='unknown',diagnostic_topic_id=None)
                answer['answers']=[]
            return answer
        reader.solver.solve=classify_blank
        self.start(reader,state)
        self.assertEqual(self.submissions,[(0,'answer'),(1,'answer'),(2,'answer'),(3,'skip')])
        self.assertEqual([r['classification'] for r in state['questions'].values()],['covered','covered','covered','unknown'])

    def test_covered_policy_skips_uncovered_prerequisites_and_ambiguous_bindings(self):
        reader=self.reader();state=self.state();state['diagnostic_policy']=COVERED
        reader.database.query.return_value=[[2036],[3052]];reader.database.query.side_effect=None
        def no_known_blank(item,*args):
            return {'confident':False,'answers':[], 'diagnostic_classification':'unknown','diagnostic_topic_id':None}
        reader.solver.solve=no_known_blank
        self.start(reader,state)
        self.assertTrue(all(action=='skip' for _,action in self.submissions))
        self.assertEqual(len(self.submissions),4)
        self.assertEqual([r['classification'] for r in state['questions'].values()],['unknown']*4)

    def test_changed_policy_preserves_grade_and_reclassifies_unanswered_decision(self):
        reader=self.reader();state=self.state();original=reader.read
        def stop(scope,directory,stem):
            if stem=='question-001-after':raise KeyboardInterrupt('fixture stop after server grade')
            return original(scope,directory,stem)
        with patch.object(reader,'read',side_effect=stop),self.assertRaises(KeyboardInterrupt):self.start(reader,state)
        # The previous policy's current graded question must never resubmit.
        state['diagnostic_policy']={**COVERED,'covered_topics':[]}
        reader.solver.solve=lambda *args: {'confident':True,'answers':[],
                                         'diagnostic_classification':'unknown','diagnostic_topic_id':None}
        reader.navigate(state['activity_url'],force=True);state['diagnostic_restored']=True
        take_diagnostic(reader,state,self.root)
        self.assertEqual(self.submissions,[(0,'answer'),(1,'skip'),(2,'skip'),(3,'skip')])
        self.assertEqual(state['questions']['question-001']['classification'],'prerequisite')

    def test_interrupted_submit_reads_server_grade_without_submitting_twice(self):
        reader=self.reader();state=self.state();original=reader.read
        def stop(scope,directory,stem):
            if stem=='question-001-after':raise KeyboardInterrupt('fixture stop after server grade')
            return original(scope,directory,stem)
        with patch.object(reader,'read',side_effect=stop),self.assertRaises(KeyboardInterrupt):self.start(reader,state)
        self.assertEqual(state['questions']['question-001']['status'],'submitting')
        reader.navigate(state['activity_url'],force=True);state['diagnostic_restored']=True
        take_diagnostic(reader,state,self.root)
        self.assertEqual(self.submissions.count((0,'answer')),1)
        self.assertEqual(len(self.submissions),4)

    def test_no_credit_history_preserves_label_and_recovers_solution_without_retake(self):
        replay=copy.deepcopy(EXAM)
        question=next(q for q in replay['questions'] if q['history']['result']=='Incorrect')
        question['history']['raw_html']=question['history']['raw_html'].replace('Incorrect','No Credit')
        with patch(__name__+'.EXAM',replay):
            reader=self.reader();state=self.state();self.start(reader,state)
            submissions=list(self.submissions)
            content=reader.history(state,self.root,self.load_topic)
            self.assertEqual(self.submissions,submissions)
            mid=question['history']['id'].replace('question-','q-')
            self.assertEqual(state['questions'][mid]['actual_result'],'No Credit')
            self.assertTrue(state['questions'][mid]['verification']['answers'])
            metadata=json.loads((self.root/'activity-metadata.json').read_text())
            saved=next(q for q in metadata if q['id']==question['history']['id'])
            self.assertEqual(saved['source_result'],'No Credit')
            self.assertEqual(saved['result'],'No Credit')
            self.assertTrue(eligible(self.root,state,content))

    def test_diagnostic_pacing_credits_time_spent_capturing_and_solving(self):
        reader=self.reader();state=self.state()
        with patch.object(reader.pacer,'wait',wraps=reader.pacer.wait) as wait:
            self.start(reader,state)
        answers=[call for call in wait.call_args_list if call.args[0]=='answer']
        self.assertEqual(len(answers),len(EXAM['questions']))
        self.assertTrue(all(call.kwargs['elapsed']>0 for call in answers))

    def test_interrupted_next_observes_advanced_question_without_replaying_next(self):
        import diagnostic
        reader=self.reader();state=self.state();wait=diagnostic.wait_changed
        def stop(r,n):
            wait(r,n)
            if n==1:raise KeyboardInterrupt('fixture stop after Next')
        with patch('diagnostic.wait_changed',side_effect=stop),self.assertRaises(KeyboardInterrupt):self.start(reader,state)
        self.assertEqual(state['diagnostic_pending_next'],1)
        reader.navigate(state['activity_url'],force=True);state['diagnostic_restored']=True
        take_diagnostic(reader,state,self.root)
        self.assertEqual(self.nexts,[0,1,2,3]);self.assertEqual(len(self.submissions),4)

    def test_submitting_checkpoint_on_restored_unanswered_question_reenters_answer(self):
        reader=self.reader();state=self.state();original=reader.read
        def stop(scope,directory,stem):
            if stem=='question-001-after':raise KeyboardInterrupt('fixture checkpoint')
            return original(scope,directory,stem)
        with patch.object(reader,'read',side_effect=stop),self.assertRaises(KeyboardInterrupt):self.start(reader,state)
        self.graded.clear();self.submissions.clear()  # Server confirms the first request never committed.
        reader.navigate(state['activity_url'],force=True);state['diagnostic_restored']=True
        take_diagnostic(reader,state,self.root)
        self.assertEqual(self.submissions,[(0,'answer'),(1,'skip'),(2,'skip'),(3,'answer')])

    def test_retry_overlay_waits_for_async_question_and_skips_do_not_request_retries(self):
        self.retry_indices={0,1}
        reader=self.reader();state=self.state();self.start(reader,state)
        self.assertEqual(self.retries,[(0,'yes'),(1,'no')])
        self.assertEqual(self.nexts,[0,1,2,3])
        self.assertEqual(self.submissions,[(0,'answer'),(1,'skip'),(2,'skip'),(3,'answer')])

    def test_second_incorrect_prerequisite_in_retry_chain_moves_on(self):
        # Exercise the unobserved retry branch with two server-reported mistakes.
        exam=copy.deepcopy(EXAM)
        exam['questions'][0]['after_html']=exam['questions'][0]['after_html'].replace('>Correct<','>Incorrect<')
        exam['questions'][1]['after_html']=exam['questions'][1]['after_html'].replace('Skipped Question','Incorrect')
        self.retry_indices={0,1}
        with patch('test_diagnostic.EXAM',exam):
            reader=self.reader();state=self.state()
            reader.database.query.side_effect=lambda _,inputs,*a:[[2036]] if inputs in (['q-136396'],['q-111251']) else []
            self.start(reader,state)
        self.assertEqual(self.retries,[(0,'yes'),(1,'no')])
        self.assertEqual(self.submissions,[(0,'answer'),(1,'answer'),(2,'skip'),(3,'answer')])


if __name__=='__main__':
    unittest.main()
