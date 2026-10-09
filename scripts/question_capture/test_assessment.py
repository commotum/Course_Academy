"""Offline regression coverage from the manually captured eight-question Quiz 5."""
import base64
import json
import random
import tempfile
import unittest
import contextlib
import io
import threading
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from browser import CaptureBrowser, EXTRACT, deduplicate_math_editor, repair_math_editor_document
from capture import arguments, observe_queue, run
from core import Pacer, assessment_can_start, assessment_requirement, build_content_transaction, choose_activity, normalize
from retry_policy import apply_policy, earned_xp, update_policy

FIXTURES = Path(__file__).parent/'fixtures'
QUIZ = json.loads((FIXTURES/'quiz-5-assessment.json').read_text())


class AssessmentPolicyTests(unittest.TestCase):
    def test_started_quiz_timeout_reloads_same_activity_and_keeps_session_and_clock(self):
        from assessment import take_assessment
        from playwright.sync_api import TimeoutError
        with tempfile.TemporaryDirectory() as work:
            reader=Mock();reader.page.locator.return_value.is_visible.return_value=False
            reader.page.content.return_value='<html>Saved source</html>'
            state={'assessment_started':True,'activity_url':'https://mathacademy.com/tasks/1/tests/2',
                   'assessment_pacing':{'started_at':123},'questions':{'q-1':{'intended':'W','status':'filled'}},
                   'solver_session':'saved-session'}
            with patch('assessment._take_assessment',side_effect=[TimeoutError('transient navigation'),None]) as take:
                take_assessment(reader,state,Path(work))
            self.assertEqual(take.call_count,2)
            reader.navigate.assert_called_once_with(state['activity_url'],force=True)
            self.assertEqual(state['assessment_pacing']['started_at'],123)
            self.assertEqual(state['questions']['q-1']['intended'],'W')
            self.assertEqual(state['solver_session'],'saved-session')

    def test_quiz_recovery_burst_is_bounded_and_does_not_dismiss_unknown_dialogs(self):
        from assessment import take_assessment,AssessmentRequestError
        from playwright.sync_api import TimeoutError
        for mode in ('persistent','unknown-dialog'):
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as work:
                reader=Mock();reader.page.content.return_value='<html></html>'
                reader.page.locator.return_value.is_visible.return_value=(mode=='unknown-dialog')
                reader.page.locator.return_value.inner_text.return_value='Unrecognized error'
                state={'assessment_started':True,'activity_url':'https://mathacademy.com/tasks/1/tests/2'}
                with patch('assessment._take_assessment',side_effect=TimeoutError('navigation')):
                    with self.assertRaises(AssessmentRequestError if mode=='persistent' else TimeoutError):
                        take_assessment(reader,state,Path(work))
                self.assertEqual(reader.navigate.call_count,2 if mode=='persistent' else 0)

    def test_quiz_intent_probability_threshold_and_sampling(self):
        from assessment import choose_quiz_intent
        self.assertEqual(arguments(['run']).assessment_correct_weight,0.8717)
        rng=Mock();rng.random.side_effect=[0,0.87169,0.8717,0.99999]
        self.assertEqual([choose_quiz_intent(rng,0.8717) for _ in range(4)],['C','C','W','W'])
        rng=random.Random(17)
        rate=sum(choose_quiz_intent(rng,0.8717)=='C' for _ in range(20000))/20000
        self.assertTrue(0.865<rate<0.878,rate)
        for weight in ('-0.1','1.1','nan'):
            with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):
                arguments(['run','--assessment-correct-weight',weight])

    def test_prepared_wrong_choice_is_distinct_and_preserves_correct_answer(self):
        from assessment import prepare_wrong_choice
        record={'intended':'W','before':{'fields':[{'key':'selection','type':'radio','choices':[
            {'option':'a','type':'math','value':'1/2'},
            {'option':'b','type':'math','value':'0.5'},
            {'option':'c','type':'math','value':'1/3'}]}]},
            'decision':{'answers':[{'key':'selection','correct_option':'a','value_type':'math','correct_value':'1/2'}]}}
        prepare_wrong_choice(record,random.Random(1))
        self.assertEqual(record['wrong_choice'],{'key':'selection','type':'math','value':'1/3'})
        self.assertEqual(record['decision']['answers'][0]['correct_value'],'1/2')

    def test_quiz_pacing_credits_solver_time_and_reuses_saved_schedule(self):
        from assessment import begin_pacing, pace_before_answer
        args=arguments(['run','--assessment-time-min','0.8','--assessment-time-max','0.8'])
        clock=[1000.0];sleeps=[]
        def sleep(seconds):sleeps.append(seconds);clock[0]+=seconds
        rng=Mock();rng.uniform.side_effect=[0.8]+[1]*8
        pacer=Pacer(args,rng,sleeper=sleep)
        reader=SimpleNamespace(pacer=pacer,check=Mock(),page=Mock())
        reader.page.locator.return_value.is_visible.return_value=True
        reader.page.locator.return_value.inner_text.return_value='15 minutes remaining'
        state={'assessment_details':{'Time Limit':'15 minutes'},'assessment_question_count':8}
        with patch('assessment.time.time',side_effect=lambda:clock[0]):
            begin_pacing(state,pacer)
            plan=json.loads(json.dumps(state['assessment_pacing']))
            clock[0]+=20  # Time spent solving counts toward the first 90-second slot.
            pace_before_answer(reader,state,0)
            self.assertAlmostEqual(sum(sleeps),70)
            self.assertTrue(all(s<=30 for s in sleeps))
            begin_pacing(state,pacer)
            self.assertEqual(state['assessment_pacing'],plan)
            sleeps.clear();pace_before_answer(reader,state,0)
            self.assertEqual(sleeps,[])  # Elapsed slots are not replayed after resume.
            clock[0]+=100;pace_before_answer(reader,state,1)
            self.assertEqual(sleeps,[])  # Slow solving does not add redundant waits.

    def test_quiz_pacing_shortens_waits_near_expiry_and_honors_shutdown(self):
        from assessment import pace_before_answer
        clock=[840.0];sleeps=[]
        args=arguments(['run']);args.stop_event=threading.Event()
        def sleep(seconds):sleeps.append(seconds);clock[0]+=seconds
        pacer=Pacer(args,sleeper=sleep)
        reader=SimpleNamespace(pacer=pacer,check=pacer.check_stop,page=Mock())
        reader.page.locator.return_value.is_visible.return_value=True
        reader.page.locator.return_value.inner_text.return_value='1 minute remaining'
        state={'assessment_question_count':8,'assessment_pacing':{
            'started_at':0,'time_limit_seconds':900,'answer_offsets_seconds':[900]*8}}
        with patch('assessment.time.time',side_effect=lambda:clock[0]):
            pace_before_answer(reader,state,0)
            self.assertEqual(sleeps,[])
            reader.page.locator.return_value.inner_text.return_value='55 seconds remaining'
            pace_before_answer(reader,state,7)
            self.assertEqual(sum(sleeps),15)  # 45-second margin remains on the actual clock.
            clock[0]=0
            reader.page.locator.return_value.inner_text.return_value='15 minutes remaining'
            pacer.sleeper=lambda seconds:args.stop_event.set()
            with self.assertRaises(KeyboardInterrupt):pace_before_answer(reader,state,0)

    def test_old_started_quizzes_do_not_acquire_a_new_pacing_plan(self):
        from assessment import begin_pacing
        state={'assessment_started':True,'assessment_details':{'Time Limit':'15 minutes'},
               'assessment_question_count':8}
        begin_pacing(state,Pacer(arguments(['run'])))
        self.assertNotIn('assessment_pacing',state)

    def test_quiz_pacing_fractions_reject_invalid_ranges(self):
        for lo,hi in (('-1','0.8'),('0.9','0.7'),('0.8','1'),('nan','0.8')):
            with self.subTest(lo=lo,hi=hi),contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):
                arguments(['run','--assessment-time-min',lo,'--assessment-time-max',hi])

    def test_duplicate_editor_tags_removed_without_changing_other_markup(self):
        tag='<script type="text/javascript" src="/js/math-editor.js"></script>'
        html='<head>'+tag+'</head><body><script src="/js/core.js"></script>'+tag+'</body>'
        self.assertEqual(deduplicate_math_editor(html),
                         '<head>'+tag+'</head><body><script src="/js/core.js"></script></body>')
        self.assertEqual(deduplicate_math_editor(tag),tag)

    def test_normal_runner_automatically_takes_required_assessment_and_saves_queue_notice(self):
        self.assert_runner_assessment('This quiz is optional until 0 more XP have been earned.')

    def test_normal_runner_takes_retake_and_persists_metadata(self):
        self.assert_runner_assessment('XP earned from a quiz retake are in addition to the XP earned from the original quiz.',retake=True)

    def test_normal_runner_takes_optional_fallback_and_saves_actual_notice(self):
        self.assert_runner_assessment('This quiz is optional until 13 more XP have been earned.',fallback=True)

    def assert_runner_assessment(self, notice, retake=False, fallback=False):
        title='Quiz 7 (Retake)' if retake else 'Quiz'
        details={'Notes':notice,'Questions':'8','Time Limit':'15 minutes'}
        quiz={'task_id':1,'topic_id':None,'test_id':10,'task_type':'assessment','title':title,
              'href':'/tasks/1/tests/10/start','capture_supported':True,
              'assessment_details':details,**assessment_requirement(details,title=title)}
        selected=[]
        class FixtureBrowser:
            def __init__(self,*args):pass
            def queue(self):return [quiz] if not selected else []
            def start(self,activity):selected.append(activity)
            def activity(self,state,*args):state['activity_complete']=True
            def history(self,state,*args):return {'task_id':state['task_id'],'task_type':'assessment','questions':[]}
        db=Mock();db.priorities.return_value={};db.import_content.return_value={'previewed':True}
        runtime=Mock();runtime.__enter__=Mock(return_value=runtime);runtime.__exit__=Mock(return_value=False)
        runtime.chromium.launch_persistent_context.return_value=SimpleNamespace(pages=[Mock()],close=Mock(),route=Mock())
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--preview','--limit','1','--state-dir',work+'/state','--output',work+'/captures'])
            with patch('capture.Database',return_value=db),patch('browser.CaptureBrowser',FixtureBrowser), \
                 patch('playwright.sync_api.sync_playwright',return_value=runtime),contextlib.redirect_stdout(io.StringIO()):
                run(args)
            self.assertEqual(selected[0]['selection_reason'],'quiz_retake' if retake else
                             'optional_assessment_fallback' if fallback else 'required_assessment')
            state=json.loads((args.output/'1/state.json').read_text())
            self.assertEqual(state['assessment_notice'],notice)
            self.assertTrue(state['preview_complete'])
            recorded=json.loads((args.output/'1/assessment-queue.json').read_text())
            self.assertEqual(recorded['optional_xp_remaining'],None if retake else 13 if fallback else 0)
            self.assertEqual(state['assessment_is_retake'],retake)
            self.assertEqual(bool(state['assessment_optional_fallback']),fallback)
            db.topic.assert_not_called()  # No single-topic lookup before the assessment is taken.
            db.import_content.assert_called_once()

    def test_retake_precedes_lessons_and_reviews_but_excludes_saved_or_in_progress(self):
        details={'Questions':'8','Time Limit':'12 minutes',
                 'Notes':'XP earned from a quiz retake are in addition to the XP earned from the original quiz.'}
        retake={'task_id':1,'topic_id':None,'task_type':'assessment','capture_supported':True,
                'assessment_details':details,**assessment_requirement(details,title='Quiz 7 (Retake)')}
        lesson={'task_id':2,'topic_id':10,'task_type':'lesson'}
        review={'task_id':3,'topic_id':11,'task_type':'review'}
        self.assertEqual(choose_activity([lesson,review,retake],{10:999})['selection_reason'],'quiz_retake')
        self.assertTrue(assessment_can_start(retake))
        self.assertEqual(retake['assessment_requirement'],'unknown')  # Keep the observed requirement separate.
        for skipped in ({**retake,'in_progress':True},{**retake,'capture_supported':False}):
            self.assertEqual(choose_activity([skipped,lesson],{10:999})['task_id'],2)
        self.assertEqual(choose_activity([retake,lesson],{10:999},captured_tasks={1})['task_id'],2)
        for incomplete in ({'Questions':'8'}, {'Time Limit':'12 minutes'},
                           {'Questions':'loading','Time Limit':'12 minutes'}):
            self.assertFalse(assessment_can_start({**retake,'assessment_details':incomplete}))
        # Either local retake marker is sufficient, including when an optional allowance appears.
        optional={**details,'Notes':'This quiz is optional until 26 more XP have been earned.'}
        metadata=assessment_requirement(optional,title='Quiz 7 (Retake)')
        self.assertTrue(assessment_can_start({**retake,**metadata,'assessment_details':optional}))
        self.assertTrue(assessment_requirement(details)['assessment_is_retake'])
        self.assertFalse(assessment_requirement({'Notes':'Optional under another rule'})['assessment_is_retake'])

    def test_optional_required_and_unknown_notices(self):
        notice = 'This quiz is optional until 26 more XP have been earned.'
        optional = assessment_requirement({'Notes':notice})
        self.assertEqual((optional['assessment_notice'],optional['optional_xp_remaining'],optional['assessment_requirement']),
                         (notice,26,'optional'))
        required = assessment_requirement({'Notes':notice.replace('26','0')})
        quiz = {'task_id':1,'topic_id':None,'task_type':'assessment','capture_supported':True,**optional}
        lesson = {'task_id':2,'topic_id':10,'task_type':'lesson'}
        self.assertEqual(choose_activity([quiz,lesson],{10:100})['task_id'],2)
        self.assertIsNone(choose_activity([quiz],{}))
        self.assertEqual(choose_activity([{**quiz,**required},lesson],{10:100})['task_id'],1)
        self.assertTrue(choose_activity([{**quiz,**assessment_requirement({'Notes':'Optional under another rule'})}],{})['stop_before_start'])
        self.assertTrue(choose_activity([{**quiz,**assessment_requirement({})}],{})['stop_before_start'])
        self.assertEqual(assessment_requirement({'Notes':'This assessment is required.'})['assessment_requirement'],'required')

    def test_optional_quiz_fallback_when_only_other_task_is_deferred_or_in_progress(self):
        details = {'Questions':'8','Time Limit':'15 minutes',
                   'Notes':'This quiz is optional until 13 more XP have been earned.'}
        quiz = {'task_id':13939908,'topic_id':None,'task_type':'assessment','capture_supported':True,
                'assessment_details':details,**assessment_requirement(details)}
        lesson = {'task_id':13941097,'topic_id':305,'task_type':'lesson'}
        self.assertEqual(choose_activity([lesson,quiz],{305:1293})['task_id'],lesson['task_id'])
        for queue, captured in [([quiz],[]),([{**lesson,'in_progress':True},quiz],[]),
                                ([lesson,quiz],[lesson['task_id']])]:
            selected = choose_activity(queue,{305:1293},captured_tasks=captured)
            self.assertEqual(selected['selection_reason'],'optional_assessment_fallback')
            self.assertEqual(selected['assessment_requirement'],'optional')
            self.assertEqual(selected['optional_xp_remaining'],13)
            self.assertTrue(assessment_can_start(selected))
        self.assertFalse(assessment_can_start(quiz))
        self.assertIsNone(choose_activity([{**quiz,'in_progress':True}],{}))
        self.assertIsNone(choose_activity([quiz],{},captured_tasks=[quiz['task_id']]))

    def test_optional_quiz_fallback_requires_complete_details(self):
        for details in ({'Questions':'8'},{'Time Limit':'15 minutes'},{'Questions':'0','Time Limit':'15 minutes'}):
            details['Notes'] = 'This quiz is optional until 13 more XP have been earned.'
            quiz = {'task_id':1,'topic_id':None,'task_type':'assessment','capture_supported':True,
                    'assessment_details':details,**assessment_requirement(details)}
            self.assertIsNone(choose_activity([quiz],{}))

    def test_negative_xp_retake_survives_restart_and_only_clears_after_perfect_attempt(self):
        with tempfile.TemporaryDirectory() as work:
            root=Path(work)
            failure={'task_id':13929099,'topic_id':893,'task_type':'review','earned_xp':-1}
            pending=update_policy(root,[failure])
            next_review={'task_id':13931000,'topic_id':893,'task_type':'review'}
            self.assertEqual(apply_policy(next_review,pending)['answer_policy'],'all_correct')
            self.assertNotIn('answer_policy',apply_policy({**next_review,'topic_id':10},pending))
            self.assertEqual(apply_policy(next_review,update_policy(root))['perfect_retake_of'],13929099)
            partial={**next_review,'answer_policy':'all_correct','activity_complete':True,
                     'questions':{'q-1':{'actual_result':'Correct'},'q-2':{'actual_result':'Incorrect'}}}
            self.assertIn('review:893',update_policy(root,completed_state=partial)['pending'])
            partial['questions']['q-2']['actual_result']='Correct'
            self.assertNotIn('review:893',update_policy(root,completed_state=partial)['pending'])
            # Re-reading the old negative-XP card must not re-arm an already recovered failure.
            self.assertNotIn('review:893',update_policy(root,[failure])['pending'])
        self.assertEqual(earned_xp("You've been awarded 2 of the task's 4 XP."),2)
        self.assertEqual(earned_xp("You've lost 1 XP."),-1)
        self.assertEqual(earned_xp("You've been awarded -1 of the task's 4 XP."),-1)
        self.assertEqual(earned_xp("You've been assigned a penalty of -2 XP for this task."),-2)
        self.assertEqual(earned_xp('No XP were awarded.'),0)

    def test_failed_completion_is_terminal_but_not_a_pass(self):
        from retry_policy import completion_outcome
        for kind in ('lesson','review'):
            self.assertEqual(completion_outcome(f'This {kind} has been halted due to poor performance and has been assigned a penalty.',kind),'failed')
            self.assertEqual(completion_outcome(f'This {kind} has been halted due to poor performance.',kind),'failed')
            self.assertEqual(completion_outcome(f'Congratulations! You have completed the {kind}.',kind),'passed')
            self.assertIsNone(completion_outcome('There was an error while loading the lesson. Please continue.',kind))

    def test_required_quiz_omits_notes_only_with_complete_details_and_sole_task(self):
        details={'Questions':'10','Time Limit':'14 minutes'}
        required=assessment_requirement(details,only_activity=True)
        self.assertEqual(required['assessment_requirement'],'required')
        self.assertIsNone(required['assessment_notice'])
        self.assertEqual(required['optional_xp_remaining'],0)
        self.assertEqual(assessment_requirement(details)['assessment_requirement'],'unknown')
        for incomplete in ({},{'Questions':'10'},{'Time Limit':'14 minutes'},
                           {**details,'Questions':'loading'}, {**details,'Notes':'Optional under another rule'}):
            self.assertEqual(assessment_requirement(incomplete,only_activity=True)['assessment_requirement'],'unknown')
        optional={**details,'Notes':'This quiz is optional until 23 more XP have been earned.'}
        self.assertEqual(assessment_requirement(optional,only_activity=True)['assessment_requirement'],'optional')

    def test_queue_records_optional_notice_and_recovers_failed_topic_even_if_previously_captured(self):
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--state-dir',work])
            browser=Mock()
            browser.queue.return_value=[{'task_id':2,'topic_id':893,'task_type':'lesson','title':'Argument'},
                {'task_id':3,'topic_id':None,'task_type':'assessment','title':'Quiz',
                 'capture_supported':True,**assessment_requirement({'Notes':'This quiz is optional until 26 more XP have been earned.'})}]
            browser.completed_outcomes=[{'task_id':1,'topic_id':893,'task_type':'lesson','earned_xp':-1}]
            db=Mock();db.priorities.return_value={893:100}
            observation=observe_queue(args,db,browser,{893},set())
            self.assertEqual(observation['selected']['answer_policy'],'all_correct')
            saved=json.loads((args.state_dir/'selection/queue.json').read_text())
            self.assertEqual(saved['queue'][1]['optional_xp_remaining'],26)
            self.assertEqual(saved['perfect_retakes_pending']['lesson:893']['earned_xp'],-1)

    def test_assessment_transaction_spans_eight_exact_source_kps(self):
        content={'task_type':'assessment','questions':QUIZ['questions'],'canonical_examples':[]}
        topics={q['topic_id']:{':topic/math-academy-id':q['topic_id'],':topic/knowledge-points':[
            {':knowledge-point/id':q['knowledge_point_id'],':knowledge-point/title':q['knowledge_point']}]}
            for q in QUIZ['questions']}
        # Observed blanks have their correct answer as a content choice, like lesson blanks.
        content=json.loads(json.dumps(content))
        for q in content['questions']:
            f=q['answer_fields'][0]
            if f['type']=='blank':f['choices']=[{'type':'math','value':f['correct_value']}]
        tx,report=build_content_transaction(content,topics,{})
        self.assertEqual(len(report),8)
        links=[r for r in tx if ':knowledge-point/questions' in r]
        self.assertEqual(len(links),8)
        self.assertFalse(any(str(a).startswith((':learner/',':task-item/')) for row in tx for a in row))


class AssessmentDOMTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.runtime=sync_playwright().start()
        cls.browser=cls.runtime.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.runtime.stop()

    def setUp(self):
        self.context=self.browser.new_context(offline=True)
        self.page=self.context.new_page()
        self.starts=0
        self.instruction_pages=0
        self.submissions=0
        card=(FIXTURES/'quiz-5-card.html').read_text().replace('26 more XP','0 more XP')
        instructions='<div id="screen"><ul id="instructions"><li>Timer continues to run.</li></ul><a id="startButton" href="/tasks/13930620/tests/589340">START</a></div>'
        html='<div id="questionNavigator">'+('<button class="questionButton">Question</button>'*8)+'</div><div id="questions">'+''.join(q['live_html'] for q in QUIZ['questions'])+'</div>'
        html+='<div id="questionsAnswered"></div><div id="timeRemaining">15 minutes remaining</div><button id="submitTestButton">Submit Test</button><div id="confirmationDialog" style="display:none">Are you sure you want to submit this test?<button id="yes">Yes</button></div>'
        html+='<script src="/vendor/jquery-3.7.1.min.js"></script><script src="/vendor/mathquill-ma.v2.1.min.js"></script><script>'
        html+='''const qs=[...document.querySelectorAll('#questions>.question')];
        function show(i){qs.forEach((q,j)=>q.style.display=i===j?'block':'none')};show(0);
        document.querySelectorAll('.questionButton').forEach((b,i)=>b.onclick=()=>show(i));
        document.querySelectorAll('.choiceLetterCircle').forEach(c=>c.onclick=()=>{c.closest('.question').querySelectorAll('.selectedChoice').forEach(n=>n.classList.remove('selectedChoice'));c.classList.add('selectedChoice')});
        const MQ=MathQuill.getInterface(2);document.querySelectorAll('.matheditor-wrapper-answer').forEach(n=>{const editor=document.createElement('div');n.append(editor);MQ.MathField(editor)});
        document.querySelector('#submitTestButton').onclick=()=>document.querySelector('#confirmationDialog').style.display='block';
        document.querySelector('#yes').onclick=()=>location.href='/tasks/13930620/tests/589340/finished';
        </script><link rel="stylesheet" href="/vendor/mathquill-0.10.1.css">'''
        self.live_html=html
        history=''.join(q['history_html'] for q in QUIZ['questions'])+'<script>document.querySelectorAll(".answerDetails").forEach(n=>n.onclick=()=>n.closest(".question").nextElementSibling.style.display="block")</script>'
        completion='<div id="finalScreen">Congratulations! You answered 8 of 8 questions correctly for a score of 100%.<a id="finalScreen-doneButton" href="/learn">CONTINUE</a></div>'
        def respond(route):
            url=route.request.url
            if '/graphics/' in url:
                asset=QUIZ['assets'][url]
                route.fulfill(status=200,content_type=asset['content_type'],body=base64.b64decode(asset['bytes']));return
            if '/vendor/' in url:
                f=FIXTURES/'vendor'/url.rsplit('/',1)[1]
                if not f.exists():
                    route.fulfill(status=404,body='');return
                route.fulfill(status=200,content_type=('text/css' if f.suffix=='.css' else 'text/javascript')+'; charset=utf-8',body=f.read_bytes());return
            if '?taskId=' in url:body=history
            elif url.endswith('/finished'):self.submissions+=1;body=completion
            elif url.endswith('/start'):self.instruction_pages+=1;body=instructions
            elif '/tests/' in url:self.starts+=1;body=html
            else:body='<div id="incompleteTasks">'+card+'</div>'
            route.fulfill(status=200,content_type='text/html; charset=utf-8',body=body)
        self.context.route('https://mathacademy.com/**',respond)

    def tearDown(self):
        self.context.close()

    def reader(self):
        args=arguments(['run','--event-min','0','--event-max','0','--answer-min','0','--answer-max','0',
                        '--assessment-time-min','0','--assessment-time-max','0','--assessment-correct-weight','1',
                        '--settle-ms','0','--timeout-ms','5000'])
        records={q['math_academy_id']:q for q in QUIZ['questions']}
        class FixtureSolver:
            def solve(self,item,*args):
                q=records[item['dom_id'].replace('question-','q-')]
                fields=[]
                for f in item['fields']:
                    original=q['answer_fields'][0]
                    if f['type']=='radio':
                        correct=next(c['option'] for c in original['choices'] if c['value']==original['correct_value'])
                        choice=next(c for c in f['choices'] if c['option']==correct)
                        value,typ=choice['value'],choice['type'];keys=[]
                    else:
                        correct=None;value=original['correct_value'];typ='math'
                        keys=([{'text':'7x^2','key':None},{'text':None,'key':'ArrowRight'},{'text':'-63x+105','key':None}]
                              if q['math_academy_id']=='q-288831' else [{'text':'6','key':None}])
                    fields.append({'key':f['key'],'correct_option':correct,'correct_value':value,'value_type':typ,
                                   'wrong_value':'0','correct_keys':keys,'wrong_keys':[{'text':'0','key':None}]})
                return {'confident':True,'explanation':'Fixture math solution','answers':fields}
        reader=CaptureBrowser(self.page,args,Pacer(args,random.Random(1)),FixtureSolver())
        reader.knowledge_snapshot=Mock(side_effect=lambda state,*args,**kwargs:
                                      state.setdefault('knowledge_snapshots',{}).update({'assessment-completed':{}}))
        return reader

    def test_duplicate_const_script_does_not_break_page_initialization(self):
        tag='<script src="/js/math-editor.js"></script>'
        html='<body style="display:none">'+tag+tag+'<script>MathEditor; document.body.style.display="block"</script></body>'
        script='const OPERATIONS={}; class MathEditor {}'
        self.context.unroute('https://mathacademy.com/**')
        self.context.route('https://mathacademy.com/**',lambda r:r.fulfill(status=200,
            content_type='application/javascript' if r.request.resource_type=='script' else 'text/html',
            body=script if r.request.resource_type=='script' else deduplicate_math_editor(html)))
        errors=[]
        self.page.on('pageerror',lambda e:errors.append(str(e)))
        self.page.goto('https://mathacademy.com/learn')
        self.assertTrue(self.page.locator('body').is_visible())
        self.assertEqual(errors,[])
        self.page.reload()
        self.assertTrue(self.page.locator('body').is_visible())
        self.assertEqual(errors,[])

    def test_navigation_accepts_positioned_content_with_zero_height_body(self):
        html='<!doctype html><body style="margin:0"><div style="position:fixed;top:20px;left:20px">Question 1</div></body>'
        self.context.unroute('https://mathacademy.com/**')
        self.context.route('https://mathacademy.com/**',lambda r:r.fulfill(
            status=200,content_type='text/html',body=html))
        reader=self.reader()
        reader.navigate('https://mathacademy.com/tasks/1/tests/2')
        self.assertFalse(self.page.locator('body').is_visible())
        self.assertTrue(self.page.get_by_text('Question 1',exact=True).is_visible())

    def test_navigation_still_rejects_hidden_body_and_content(self):
        from playwright.sync_api import TimeoutError
        self.context.unroute('https://mathacademy.com/**')
        self.context.route('https://mathacademy.com/**',lambda r:r.fulfill(
            status=200,content_type='text/html',body='<body style="display:none"><div>Question 1</div></body>'))
        reader=self.reader();self.page.set_default_timeout(100)
        with self.assertRaises(TimeoutError):
            reader.navigate('https://mathacademy.com/tasks/1/tests/2')

    def test_lazy_queue_details_capture_optional_notice_and_negative_xp(self):
        card=(FIXTURES/'quiz-5-card.html').read_text()
        placeholder='<div id="task-13930620" class="taskUnlocked" progress="0"><span class="taskTypeUnlocked">Assessment</span><div id="taskDetails-13930620" class="taskDetails"></div></div>'
        failed='<div id="completedTasks"><div id="task-13929099" class="taskCompleted"><span class="taskTypeLocked">Review</span><span class="taskPoints">-1/4 XP</span><a id="taskTopicLink-13929099" href="/topics/893">Argument</a></div></div>'
        body='<div id="incompleteTasks">'+placeholder+'</div>'+failed+'<script>document.querySelector(".taskUnlocked").onclick=()=>document.querySelector("#incompleteTasks").innerHTML='+json.dumps(card)+'</script>'
        self.context.unroute('https://mathacademy.com/**')
        self.context.route('https://mathacademy.com/**',lambda r:r.fulfill(status=200,content_type='text/html; charset=utf-8',body=body))
        reader=self.reader()
        quiz,=reader.queue()
        self.assertEqual(quiz['optional_xp_remaining'],26)
        self.assertEqual(quiz['assessment_requirement'],'optional')
        self.assertEqual(reader.completed_outcomes,[{'task_id':13929099,'topic_id':893,'task_type':'review','earned_xp':-1}])

    def test_observed_required_quiz_without_notes_can_start(self):
        card=(FIXTURES/'quiz-6-required-card.html').read_text()
        self.context.unroute('https://mathacademy.com/**')
        self.context.route('https://mathacademy.com/**',lambda r:r.fulfill(
            status=200,content_type='text/html; charset=utf-8',
            body='<div id="incompleteTasks">'+card+'</div>'))
        reader=self.reader()
        quiz,=reader.queue()
        self.assertEqual(quiz['assessment_requirement'],'required')
        self.assertIsNone(quiz['assessment_notice'])
        self.assertEqual(choose_activity([quiz],{})['selection_reason'],'required_assessment')
        reader.start(quiz)
        self.assertTrue(self.page.url.endswith('/tasks/13932272/tests/589414/start'))

    def test_start_rechecks_sole_task_requirement(self):
        card=(FIXTURES/'quiz-6-required-card.html').read_text()
        self.context.unroute('https://mathacademy.com/**')
        self.context.route('https://mathacademy.com/**',lambda r:r.fulfill(
            status=200,content_type='text/html; charset=utf-8',
            body='<div id="incompleteTasks">'+card+'</div>'))
        reader=self.reader()
        quiz,=reader.queue()
        self.page.locator('#incompleteTasks').evaluate("n=>n.insertAdjacentHTML('beforeend','<div class=\"taskUnlocked\" id=\"task-2\">Another task</div>')")
        with self.assertRaisesRegex(ValueError,'stop before Start'):
            reader.start(quiz)
        self.assertEqual(self.page.url,'https://mathacademy.com/learn')

    def test_document_repair_preserves_browser_redirect_destination(self):
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
        from threading import Thread
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args): pass
            def do_GET(self):
                if self.path=='/learn':
                    self.send_response(302);self.send_header('Location','/tasks/1/tests/589487')
                    self.send_header('Content-Length','0');self.end_headers();return
                if self.path=='/js/math-editor.js':
                    body='const OPERATIONS={};';mime='text/javascript'
                else:
                    body='<body style="visibility:hidden"><script src="/js/math-editor.js"></script>'
                    body+='<script src="/js/math-editor.js"></script><script>'
                    body+='document.body.dataset.testId=location.pathname.split("/")[4];document.body.style.visibility="visible";'
                    body+='</script></body>';mime='text/html'
                data=body.encode();self.send_response(200);self.send_header('Content-Type',mime)
                self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        thread=Thread(target=server.serve_forever,daemon=True);thread.start()
        context=self.browser.new_context();page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        base='http://127.0.0.1:'+str(server.server_port)
        context.route(base+'/**',repair_math_editor_document)
        try:
            reader=CaptureBrowser(page,SimpleNamespace(timeout_ms=3000),Mock(),None)
            reader.navigate(base+'/learn');page.locator('body').wait_for(state='visible')
            self.assertEqual(page.url,base+'/tasks/1/tests/589487')
            self.assertEqual(page.locator('body').get_attribute('data-test-id'),'589487')
            self.assertEqual(page.locator('script[src="/js/math-editor.js"]').count(),1)
            self.assertTrue(all('OPERATIONS' in error for error in errors))
        finally:
            context.close();server.shutdown();server.server_close();thread.join()

    def test_assessment_waits_for_delayed_navigator_without_restarting_timer(self):
        buttons='<button class="questionButton">Question</button>'*8
        body=self.live_html.replace('<div id="questionNavigator">'+buttons+'</div>','<div id="questionNavigator"></div>')
        body+='<script>setTimeout(()=>{document.querySelector("#questionNavigator").innerHTML='+json.dumps(buttons)+';document.querySelectorAll(".questionButton").forEach((b,i)=>b.onclick=()=>show(i));},300)</script>'
        self.context.route('https://mathacademy.com/tasks/13930620/tests/589340',
            lambda r:r.fulfill(status=200,content_type='text/html',body=body))
        reader=self.reader();self.page.goto('https://mathacademy.com/tasks/13930620/tests/589340')
        state={'task_id':13930620,'task_type':'assessment','test_id':589340,'topic_id':None,
               'assessment_started':True,'assessment_question_count':8,'questions':{},'examples':{},'kps':{}}
        with tempfile.TemporaryDirectory() as work:
            reader.activity(state,Path(work),None)
        self.assertTrue(state['activity_complete']);self.assertEqual(self.submissions,1)
        self.assertEqual(self.instruction_pages,0)

    def test_whole_quiz_capture_preserves_choices_blanks_images_metadata_and_single_submission(self):
        self.assert_whole_quiz_capture()

    def test_quiz_pacing_occurs_before_entry_and_records_real_elapsed_time(self):
        reader=self.reader();quiz,=reader.queue()
        reader.args.assessment_time_min=reader.args.assessment_time_max=0.8
        clock=[1000.0];entered=[]
        reader.pacer.sleeper=lambda seconds:clock.__setitem__(0,clock[0]+seconds)
        original_enter=reader.enter
        def enter(*args):entered.append(clock[0]);return original_enter(*args)
        reader.enter=enter
        solve=reader.solver.solve
        def slower_solver(*args):clock[0]+=5;return solve(*args)
        reader.solver.solve=slower_solver
        state={'task_id':quiz['task_id'],'task_type':'assessment','test_id':quiz['test_id'],'topic_id':None,
               'assessment_details':quiz['assessment_details'],'assessment_requirement':'required',
               'questions':{},'examples':{},'kps':{}}
        reader.start(quiz)
        with tempfile.TemporaryDirectory() as work,patch('assessment.time.time',side_effect=lambda:clock[0]):
            reader.activity(state,Path(work),None)
            saved=json.loads((Path(work)/'state.json').read_text())
        plan=state['assessment_pacing']
        self.assertAlmostEqual(plan['actual_elapsed_seconds'],720)
        self.assertEqual(saved['assessment_pacing'],plan)
        self.assertEqual(self.submissions,1)
        for actual,offset in zip(entered,plan['answer_offsets_seconds']):
            self.assertAlmostEqual(actual-plan['started_at'],offset)
        durations=[entered[0]-plan['started_at']]+[b-a for a,b in zip(entered,entered[1:])]
        self.assertGreater(max(durations)-min(durations),10)

    def test_weighted_wrong_quiz_still_imports_verified_correct_answers(self):
        reader=self.reader();quiz,=reader.queue()
        reader.args.assessment_correct_weight=0
        reader.solver.solve=Mock(wraps=reader.solver.solve)
        history=''.join(q['history_html'] for q in QUIZ['questions'])
        history=history.replace('class="answerResult"><span style="color: green;">Correct</span>',
                                'class="answerResult"><span style="color: red;">Incorrect</span>')
        history+='<script>document.querySelectorAll(".answerDetails").forEach(n=>n.onclick=()=>n.closest(".question").nextElementSibling.style.display="block")</script>'
        self.context.route('https://mathacademy.com/learn?taskId=13930620',lambda r:r.fulfill(
            status=200,content_type='text/html',body=history))
        state={'task_id':quiz['task_id'],'task_type':'assessment','test_id':quiz['test_id'],'topic_id':None,
               'assessment_details':quiz['assessment_details'],'assessment_requirement':'required',
               'questions':{},'examples':{},'kps':{}}
        reader.start(quiz)
        with tempfile.TemporaryDirectory() as work:
            directory=Path(work);reader.activity(state,directory,None)
            def topic(tid,*args):
                q=next(q for q in QUIZ['questions'] if q['topic_id']==tid)
                return {':topic/knowledge-points':[{
                    ':knowledge-point/title':q['knowledge_point'],':knowledge-point/id':q['knowledge_point_id']}]}
            content=reader.history(state,directory,topic)
            self.assertEqual(reader.solver.solve.call_count,16)  # Eight solutions and eight graded verifications.
            self.assertEqual(content['answer_policy'],'independent_weighted')
            self.assertEqual(content['assessment_correct_weight'],0)
            self.assertEqual(len(content['questions']),8)
            self.assertTrue(all(q['intended']=='W' and q['actual_result']=='Incorrect' for q in state['questions'].values()))
            for q in content['questions']:
                original=next(v for v in QUIZ['questions'] if v['math_academy_id']==q['math_academy_id'])
                field=q['answer_fields'][0]
                original_field=original['answer_fields'][0]
                kind=next((c['type'] for c in original_field['choices'] if c['value']==original_field['correct_value']),'math')
                self.assertEqual(normalize(field['correct_value'],kind),normalize(original_field['correct_value'],kind))
                submitted=state['questions'][q['math_academy_id']]['before']['fields'][0]['submitted_value']
                self.assertNotEqual(normalize(submitted,kind),normalize(field['correct_value'],kind))
                self.assertIn(submitted,[c['value'] for c in field['choices']])

    def test_wrong_multifield_question_changes_only_one_field(self):
        reader=self.reader()
        self.page.set_content('<div id="q"><input id="first"><input id="second"></div>')
        record={'intended':'W','before':{'fields':[
            {'key':'field-'+str(i),'type':'blank','tag':'input','dom_id':name,'choices':[]}
            for i,name in [(1,'first'),(2,'second')]]},'decision':{'answers':[
            {'key':'field-'+str(i),'correct_value':str(i),'wrong_value':'0',
             'correct_keys':[],'wrong_keys':[],'value_type':'math'} for i in (1,2)]}}
        reader.enter(self.page.locator('#q'),record)
        reader.verify_entered(self.page.locator('#q'),record)
        self.assertEqual([f['submitted_value'] for f in record['before']['fields']],['0','2'])

    def test_unexpected_correct_grade_for_wrong_response_uses_activity_solver_judgment(self):
        reader=self.reader();quiz,=reader.queue();reader.args.assessment_correct_weight=0
        state={'task_id':quiz['task_id'],'task_type':'assessment','test_id':quiz['test_id'],'topic_id':None,
               'assessment_details':quiz['assessment_details'],'assessment_requirement':'required',
               'questions':{},'examples':{},'kps':{}}
        reader.start(quiz)
        with tempfile.TemporaryDirectory() as work:
            directory=Path(work);reader.activity(state,directory,None)
            def topic(tid,*args):
                q=next(q for q in QUIZ['questions'] if q['topic_id']==tid)
                return {':topic/knowledge-points':[{
                    ':knowledge-point/title':q['knowledge_point'],':knowledge-point/id':q['knowledge_point_id']}]}
            # The fixture grades deliberately wrong inputs correct. Reconcile
            # these disagreements with the same solver and retain both values.
            content=reader.history(state,directory,topic)
            self.assertEqual(len(content['questions']),8)
            self.assertTrue((directory/'content.json').exists())
            self.assertTrue(all(q['answer_reconciliations'] and q['predicted_answers']
                                for q in state['questions'].values()))

    def test_saved_wrong_choice_follows_value_when_display_order_changes(self):
        reader=self.reader()
        self.page.set_content('<div id="q">'+''.join(
            '<button id="choice-'+option+'">'+option+'</button>' for option in ('a','b','c'))+'</div>')
        field={'key':'selection','type':'radio','choices':[
            {'option':option,'dom_id':'choice-'+option,'type':'math','value':value}
            for option,value in [('a','2'),('b','4'),('c','3')]]}
        record={'intended':'W','before':{'fields':[field]},
                'decision':{'answers':[{'key':'selection','correct_option':'a','correct_value':'2'}]},
                'wrong_choice':{'key':'selection','type':'math','value':'3'}}
        reader.enter(self.page.locator('#q'),record)
        self.assertEqual(field['submitted_option'],'c')
        self.assertEqual(field['submitted_value'],'3')
        field['choices'][2]['value']='5'
        with self.assertRaisesRegex(ValueError,'Saved incorrect choice does not match exactly one'):
            reader.enter(self.page.locator('#q'),record)

    def test_observed_retake_among_other_tasks_uses_normal_quiz_capture(self):
        card=(FIXTURES/'quiz-7-retake-card.html').read_text().replace('13938136','13930620').replace('589650','589340')
        lesson='<div id="task-2" class="taskUnlocked" progress="0"><span class="taskTypeUnlocked">Lesson</span><div class="taskNameUnlocked">Lesson</div><a class="taskStartButton" href="/tasks/2/topics/10/lesson">Start</a></div>'
        self.context.route('https://mathacademy.com/learn',lambda r:r.fulfill(
            status=200,content_type='text/html',body='<div id="incompleteTasks">'+card+lesson+'</div>'))
        self.assert_whole_quiz_capture(retake=True)

    def test_optional_fallback_uses_normal_quiz_capture_and_retains_optional_notice(self):
        card=(FIXTURES/'quiz-5-card.html').read_text().replace('26 more XP','13 more XP')
        self.context.route('https://mathacademy.com/learn',lambda r:r.fulfill(
            status=200,content_type='text/html',body='<div id="incompleteTasks">'+card+'</div>'))
        self.assert_whole_quiz_capture(fallback=True)

    def test_start_rechecks_retake_marker_before_navigating(self):
        card=(FIXTURES/'quiz-7-retake-card.html').read_text().replace('13938136','13930620').replace('589650','589340')
        self.context.route('https://mathacademy.com/learn',lambda r:r.fulfill(
            status=200,content_type='text/html',body='<div id="incompleteTasks">'+card+'</div>'))
        reader=self.reader();quiz,=reader.queue()
        self.page.locator('.taskNameUnlocked').evaluate("e => e.textContent='Quiz 7'")
        self.page.locator('.testFieldValue').last.evaluate("e => e.textContent='Optional under another rule'")
        with self.assertRaisesRegex(ValueError,'stop before Start'):
            reader.start(quiz)
        self.assertEqual(self.instruction_pages,0)

    def test_optional_fallback_rechecks_live_alternatives_before_start(self):
        card=(FIXTURES/'quiz-5-card.html').read_text()
        lesson='<div id="task-2" class="taskUnlocked" progress="1"><span class="taskTypeUnlocked">Lesson</span><div class="taskNameUnlocked">Lesson</div><a class="taskStartButton" href="/tasks/2/topics/10/lesson">Start</a></div>'
        self.context.route('https://mathacademy.com/learn',lambda r:r.fulfill(
            status=200,content_type='text/html',body='<div id="incompleteTasks">'+card+lesson+'</div>'))
        reader=self.reader()
        selected=choose_activity(reader.queue(),{10:999})
        self.assertEqual(selected['selection_reason'],'optional_assessment_fallback')
        self.page.locator('#task-2').evaluate("n=>n.setAttribute('progress','0')")
        with self.assertRaisesRegex(ValueError,'stop before Start'):
            reader.start(selected)
        self.assertEqual(self.instruction_pages,0)
        self.page.locator('#task-2').evaluate("n=>n.setAttribute('progress','1')")
        reader.start(selected)
        self.assertEqual(self.instruction_pages,1)

    def test_actual_mathquill_negative_quotient_is_verified_without_submit(self):
        reader=self.reader()
        self.page.goto('https://mathacademy.com/tasks/13930620/tests/589340')
        scope=self.page.locator('#question-288831')
        editor=scope.locator('.mq-editable-field')
        evidence=json.loads((FIXTURES/'negative-trig-quotient.json').read_text())
        editor.evaluate('(n,tex)=>MathQuill.getInterface(2).MathField(n).latex(tex)',evidence['observed'])
        item=scope.evaluate(EXTRACT)
        field=item['fields'][0]
        field['submitted_value']=evidence['intended']
        record={'before':item}
        reader.verify_entered(scope,record)
        field['submitted_value']=evidence['intended'].replace('-6','6')
        with self.assertRaisesRegex(ValueError,'Actual MathQuill value differs'):
            reader.verify_entered(scope,record)
        self.assertEqual(self.submissions,0)

    def test_request_error_before_eighth_question_recovers_complete_quiz(self):
        # Reproduce the site's request-error cover, triggered on the final
        # navigator button. Reloading serves the same questions without it.
        html=self.live_html+'''<div id="messageBox-message" style="display:none">Oops, there was an error processing your request. Please check your internet connection.</div>
        <script>document.querySelectorAll('.questionButton')[7].onclick=()=>{
          document.querySelector('#messageBox-message').style.display='block';
          const cover=document.createElement('div');cover.className='screenCover';
          cover.style='position:fixed;inset:0;z-index:10000';document.body.append(cover);
        };</script>'''
        def first_document(route):
            self.context.unroute('https://mathacademy.com/tasks/13930620/tests/589340',first_document)
            self.starts+=1
            route.fulfill(status=200,content_type='text/html; charset=utf-8',body=html)
        self.context.route('https://mathacademy.com/tasks/13930620/tests/589340',first_document)
        self.assert_whole_quiz_capture(reloads=1)

    def test_queue_redirect_to_active_quiz_does_not_reload_or_wait_for_queue(self):
        reader=self.reader()
        self.page.goto('https://mathacademy.com/tasks/13930620/tests/589340')
        # Playwright routes intercept only the initial request of redirects;
        # emulate its destination response while retaining the real quiz DOM.
        response=SimpleNamespace(request=SimpleNamespace(redirected_from=True))
        with patch.object(self.page,'goto',return_value=response) as navigate:
            with self.assertRaisesRegex(ValueError,'unfinished assessment'):
                reader.queue()
        navigate.assert_called_once_with('https://mathacademy.com/learn',wait_until='domcontentloaded')

    def assert_whole_quiz_capture(self, retake=False, fallback=False, reloads=0):
        reader=self.reader()
        quiz=choose_activity(reader.queue(),{10:999})
        self.assertEqual(quiz['assessment_notice'],
                         'XP earned from a quiz retake are in addition to the XP earned from the original quiz.' if retake
                         else 'This quiz is optional until 13 more XP have been earned.' if fallback
                         else 'This quiz is optional until 0 more XP have been earned.')
        self.assertEqual(quiz['assessment_requirement'],'unknown' if retake else 'optional' if fallback else 'required')
        with tempfile.TemporaryDirectory() as work:
            directory=Path(work)
            state={'task_id':quiz['task_id'],'task_type':'assessment','test_id':quiz['test_id'],'topic_id':None,
                   'assessment_details':quiz['assessment_details'],'assessment_requirement':quiz['assessment_requirement'],
                   'assessment_notice':quiz['assessment_notice'],'optional_xp_remaining':quiz['optional_xp_remaining'],
                   'assessment_is_retake':quiz['assessment_is_retake'],
                   'assessment_optional_fallback':quiz.get('assessment_optional_fallback',False),
                   'questions':{},'examples':{},'kps':{}}
            reader.start(quiz)
            try:
                reader.activity(state,directory,None)
            except Exception as error:
                raise AssertionError(list(reader.diagnostic_events)) from error
            self.assertTrue(state['activity_complete'])
            self.assertEqual((self.starts,self.submissions),(1+reloads,1))
            self.assertEqual(state.get('assessment_recovery_attempts',0),reloads)
            self.assertEqual(self.instruction_pages,1)
            self.assertEqual(len(state['questions']),8)
            self.assertIn('question-82938',(directory/'assessment-live.html').read_text())
            reader.knowledge_snapshot.assert_called_once()
            def topic(tid,*args):
                q=next(q for q in QUIZ['questions'] if q['topic_id']==tid)
                return {':topic/knowledge-points':[{':knowledge-point/title':q['knowledge_point'],':knowledge-point/id':q['knowledge_point_id']}]}
            content=reader.history(state,directory,topic)
            self.assertEqual(len(content['questions']),8)
            self.assertEqual(sum(len(f['choices']) for q in content['questions'] for f in q['answer_fields']),32)
            self.assertTrue(all(q['worked_solution'] and q['difficulty'] and q['knowledge_point_id'] for q in content['questions']))
            self.assertEqual(content['assessment_notice'],quiz['assessment_notice'])
            self.assertEqual(content['assessment_is_retake'],retake)
            self.assertEqual(content['assessment_optional_fallback'],fallback)
            q=next(q for q in state['questions'].values() if q['before']['dom_id']=='question-82938')
            self.assertEqual(q['before']['fields'][0]['observed_selected_option'],'c')
            self.assertTrue(q['before']['fields'][0]['choices'][2]['value'].endswith('.png'))
            manifest=json.loads((directory/'assets/manifest.json').read_text())
            self.assertEqual(len(manifest),7)
            self.assertTrue(all(a['representation']=='original' for a in manifest.values()))
            self.assertTrue(next(q for q in content['questions'] if q['math_academy_id']=='q-74721')['requires_calculator'])
            # Completion recovery must not start or submit the test again.
            reader.activity(state,directory,None)
            self.assertEqual(self.submissions,1)

    def test_uncertain_submission_uses_fresh_server_unsubmitted_test(self):
        reader=self.reader()
        self.page.goto('https://mathacademy.com/tasks/13930620/tests/589340')
        with tempfile.TemporaryDirectory() as work:
            state={'task_id':13930620,'task_type':'assessment','test_id':589340,'questions':{},
                   'assessment_details':{'Questions':'8','Time Limit':'15 minutes'}, 'assessment_question_count':8,
                   'test_submission_status':'confirming','assessment_started':True}
            reader.activity(state,Path(work),None)
            self.assertTrue(state['activity_complete'])
            self.assertEqual(state['assessment_intent_recoveries'][0]['reason'],'server_restored_unsubmitted_test')
        self.assertEqual(self.submissions,1)
        self.assertEqual(self.instruction_pages,0)

    def test_interrupted_unsubmitted_quiz_reuses_answers_and_resumes_without_starting_again(self):
        self.assert_interrupted_quiz_resumes()

    def test_interrupted_wrong_quiz_keeps_intents_and_selected_distractor(self):
        self.assert_interrupted_quiz_resumes(wrong=True)

    def assert_interrupted_quiz_resumes(self, wrong=False):
        reader=self.reader();quiz,=reader.queue()
        if wrong:reader.args.assessment_correct_weight=0
        with tempfile.TemporaryDirectory() as work:
            directory=Path(work)
            state={'task_id':quiz['task_id'],'task_type':'assessment','test_id':quiz['test_id'],'topic_id':None,
                   'assessment_details':quiz['assessment_details'],'assessment_requirement':'required',
                   'questions':{},'examples':{},'kps':{}}
            original_solve=reader.solver.solve
            calls=[]
            def interrupted(item,*args):
                calls.append(item['dom_id'])
                if len(calls)==3:raise KeyboardInterrupt()
                return original_solve(item,*args)
            reader.solver.solve=interrupted
            reader.start(quiz)
            with self.assertRaises(KeyboardInterrupt):reader.activity(state,directory,None)
            self.assertEqual(len(state['questions']),2)
            self.assertTrue(all(q['status']=='filled' for q in state['questions'].values()))
            submitted={mid:[f['submitted_value'] for f in q['before']['fields']] for mid,q in state['questions'].items()}
            self.assertEqual(self.submissions,0)
            # A restored live page can lose UI selections; reuse saved values and fill them again.
            resumed=self.reader();resumed.solver.solve=Mock(wraps=resumed.solver.solve)
            resumed.navigate(state['activity_url'],force=True)
            resumed.activity(state,directory,None)
            self.assertEqual(resumed.solver.solve.call_count,6)
            self.assertEqual(self.instruction_pages,1)
            self.assertEqual(self.submissions,1)
            self.assertTrue(state['activity_complete'])
            for mid,values in submitted.items():
                self.assertEqual([f['submitted_value'] for f in state['questions'][mid]['before']['fields']],values)
            self.assertEqual(state['assessment_correct_weight'],0 if wrong else 1)
            self.assertTrue(all(q['intended']==('W' if wrong else 'C') for q in state['questions'].values()))


if __name__=='__main__':
    unittest.main()
