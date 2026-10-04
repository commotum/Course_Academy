"""Offline regression coverage from the manually captured eight-question Quiz 5."""
import base64
import json
import random
import tempfile
import unittest
import contextlib
import io
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from browser import CaptureBrowser, EXTRACT, deduplicate_math_editor, repair_math_editor_document
from capture import arguments, observe_queue, run
from core import Pacer, assessment_requirement, build_content_transaction, choose_activity
from retry_policy import apply_policy, earned_xp, update_policy

FIXTURES = Path(__file__).parent/'fixtures'
QUIZ = json.loads((FIXTURES/'quiz-5-assessment.json').read_text())


class AssessmentPolicyTests(unittest.TestCase):
    def test_duplicate_editor_tags_removed_without_changing_other_markup(self):
        tag='<script type="text/javascript" src="/js/math-editor.js"></script>'
        html='<head>'+tag+'</head><body><script src="/js/core.js"></script>'+tag+'</body>'
        self.assertEqual(deduplicate_math_editor(html),
                         '<head>'+tag+'</head><body><script src="/js/core.js"></script></body>')
        self.assertEqual(deduplicate_math_editor(tag),tag)

    def test_normal_runner_automatically_takes_required_assessment_and_saves_queue_notice(self):
        notice='This quiz is optional until 0 more XP have been earned.'
        quiz={'task_id':1,'topic_id':None,'test_id':10,'task_type':'assessment','title':'Quiz',
              'href':'/tasks/1/tests/10/start','capture_supported':True,
              'assessment_details':{'Notes':notice,'Questions':'8','Time Limit':'15 minutes'},
              **assessment_requirement({'Notes':notice})}
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
            args=arguments(['run','--preview','--state-dir',work+'/state','--output',work+'/captures'])
            with patch('capture.Database',return_value=db),patch('browser.CaptureBrowser',FixtureBrowser), \
                 patch('playwright.sync_api.sync_playwright',return_value=runtime),contextlib.redirect_stdout(io.StringIO()):
                run(args)
            self.assertEqual(selected[0]['selection_reason'],'required_assessment')
            state=json.loads((args.output/'1/state.json').read_text())
            self.assertEqual(state['assessment_notice'],notice)
            self.assertTrue(state['preview_complete'])
            recorded=json.loads((args.output/'1/assessment-queue.json').read_text())
            self.assertEqual(recorded['optional_xp_remaining'],0)
            db.topic.assert_not_called()  # No single-topic lookup before the assessment is taken.
            db.import_content.assert_called_once()

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
        args=arguments(['run','--event-min','0','--event-max','0','--answer-min','0','--answer-max','0','--settle-ms','0','--timeout-ms','5000'])
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
        with self.assertRaisesRegex(ValueError,'requirement is unknown'):
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
        reader=self.reader()
        quiz,=reader.queue()
        self.assertEqual(quiz['assessment_notice'],'This quiz is optional until 0 more XP have been earned.')
        self.assertEqual(quiz['assessment_requirement'],'required')
        with tempfile.TemporaryDirectory() as work:
            directory=Path(work)
            state={'task_id':quiz['task_id'],'task_type':'assessment','test_id':quiz['test_id'],'topic_id':None,
                   'assessment_details':quiz['assessment_details'],'assessment_requirement':quiz['assessment_requirement'],
                   'assessment_notice':quiz['assessment_notice'],'optional_xp_remaining':0,
                   'questions':{},'examples':{},'kps':{}}
            reader.start(quiz)
            try:
                reader.activity(state,directory,None)
            except Exception as error:
                raise AssertionError(list(reader.diagnostic_events)) from error
            self.assertTrue(state['activity_complete'])
            self.assertEqual((self.starts,self.submissions),(1,1))
            reader.knowledge_snapshot.assert_called_once()
            def topic(tid,*args):
                q=next(q for q in QUIZ['questions'] if q['topic_id']==tid)
                return {':topic/knowledge-points':[{':knowledge-point/title':q['knowledge_point'],':knowledge-point/id':q['knowledge_point_id']}]}
            content=reader.history(state,directory,topic)
            self.assertEqual(len(content['questions']),8)
            self.assertEqual(sum(len(f['choices']) for q in content['questions'] for f in q['answer_fields']),32)
            self.assertTrue(all(q['worked_solution'] and q['difficulty'] and q['knowledge_point_id'] for q in content['questions']))
            self.assertEqual(content['assessment_notice'],quiz['assessment_notice'])
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

    def test_uncertain_submission_never_replays_or_starts_timer(self):
        reader=self.reader()
        self.page.goto('https://mathacademy.com/tasks/13930620/tests/589340')
        with tempfile.TemporaryDirectory() as work:
            state={'task_id':13930620,'task_type':'assessment','test_id':589340,'questions':{},
                   'test_submission_status':'confirming','assessment_started':True}
            with self.assertRaisesRegex(ValueError,'unconfirmed'):
                reader.activity(state,Path(work),None)
        self.assertEqual(self.submissions,0)

    def test_interrupted_unsubmitted_quiz_reuses_answers_and_resumes_without_starting_again(self):
        reader=self.reader();quiz,=reader.queue()
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
            self.assertEqual(self.submissions,0)
            # A restored live page can lose UI selections; reuse saved values and fill them again.
            resumed=self.reader();resumed.solver.solve=Mock(wraps=resumed.solver.solve)
            resumed.navigate(state['activity_url'],force=True)
            resumed.activity(state,directory,None)
            self.assertEqual(resumed.solver.solve.call_count,6)
            self.assertEqual(self.instruction_pages,1)
            self.assertEqual(self.submissions,1)
            self.assertTrue(state['activity_complete'])


if __name__=='__main__':
    unittest.main()
