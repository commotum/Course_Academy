"""Regression checks using actual Sum Rule DOM and EDB capture fixtures."""
import copy
import base64
import contextlib
import io
import json
import random
import tempfile
import unittest
import uuid
from unittest.mock import Mock, patch
from pathlib import Path
from types import SimpleNamespace

from browser import EXTRACT, CaptureBrowser, kp_for_example, normalize_mathquill
from core import ROOT, ALLOWED, Pacer, build_transaction, choose_activity, choose_lesson, choose_sequence, choose_review_sequence, normalize
from database import Database
from edn import dumps, loads, kw
from solver import Solver
from progress import changes, normalize_course
from capture import arguments, run, unfinished_run, read_journal, previous_activity_snapshot

FIXTURE = ROOT/'reference/mathacademy/sum-rule-13925458'
REVIEW_FIXTURE = ROOT/'reference/mathacademy/review-13925710'


class PolicyTests(unittest.TestCase):
    def test_priority_lookup_uses_schema_string_learner_id(self):
        db = Database(arguments(['priorities']))
        db.query = Mock(return_value=[[462, 'Continuity', 1244.0]])
        learner = uuid.UUID('59d5cf13-351c-4114-be19-4c3bb64ee051')
        self.assertEqual(db.priorities(learner, Path('/tmp/selection')), {462:1244.0})
        self.assertEqual(db.query.call_args.args[1], [str(learner)])

    def test_sequences_maximize_without_terminating(self):
        rng = random.Random(42)
        values = [choose_sequence(rng) for _ in range(10000)]
        self.assertEqual(set(values),{'CWCWC','WCWCC'})
        self.assertLess(abs(values.count('CWCWC')/len(values)-0.7),0.02)
        for sequence in set(values):
            self.assertNotIn('CC',sequence[:4])
            self.assertNotIn('WW',sequence)
            self.assertEqual(sequence.count('W'),2)

    def test_queue_intersection_uses_priority_and_skips_captured(self):
        queue = [{'topic_id':i,'task_id':100+i} for i in (1,2,3,4)]
        self.assertEqual(choose_lesson(queue,{1:4,2:9,3:float('nan')})['topic_id'],2)
        self.assertEqual(choose_lesson(queue,{1:4,2:9},[2])['topic_id'],1)
        self.assertIsNone(choose_lesson(queue,{}))

    def test_pacing_draws_between_configured_bounds(self):
        slept = []
        args = SimpleNamespace(event_min=0.8,event_max=2.5)
        pacer = Pacer(args,random.Random(3),slept.append)
        draws = [pacer.wait('event','test') for _ in range(20)]
        self.assertEqual(draws,slept)
        self.assertTrue(all(0.8<=d<=2.5 for d in draws))
        self.assertGreater(len(set(draws)),1)

    def test_answer_budget_credits_solver_time(self):
        slept=[]
        pacer=Pacer(SimpleNamespace(answer_min=5,answer_max=12),Mock(uniform=Mock(return_value=9)),slept.append)
        self.assertEqual(pacer.wait('answer','fast solver',elapsed=4),5)
        self.assertEqual(pacer.wait('answer','equal budget',elapsed=9),0)
        self.assertEqual(pacer.wait('answer','slow solver',elapsed=20),0)
        self.assertEqual(slept,[5])
        with self.assertRaises(ValueError):
            pacer.wait('answer','invalid elapsed',elapsed=float('nan'))

    def test_review_fallback_does_not_mark_its_topic_lesson_completed(self):
        queue = [{'task_id':1,'topic_id':10,'task_type':'review'},
                 {'task_id':2,'topic_id':20,'task_type':'review'},
                 {'task_id':3,'topic_id':10,'task_type':'lesson'}]
        self.assertEqual(choose_activity(queue,{10:4})['task_id'],3)
        self.assertEqual(choose_activity(queue,{})['task_id'],1)
        self.assertEqual(choose_activity(queue,{},captured_tasks=[1])['task_id'],2)
        self.assertEqual(choose_activity(queue,{10:4},captured_tasks=[1])['task_id'],3)
        self.assertEqual(choose_activity(queue,{},captured_tasks=[1,2])['task_id'],3)
        self.assertIsNone(choose_activity(queue,{},completed_topics=[10],captured_tasks=[1,2]))

    def test_queue_fallback_uses_visible_order_and_skips_completed_captures(self):
        queue = [{'task_id':1,'topic_id':10,'task_type':'lesson'},
                 {'task_id':2,'topic_id':20,'task_type':'lesson'},
                 {'task_id':3,'topic_id':30,'task_type':'lesson'}]
        selected = choose_activity(queue,{})
        self.assertEqual((selected['task_id'],selected['selection_reason']),(1,'queue_fallback'))
        self.assertEqual(choose_activity(queue,{},captured_tasks=[1])['task_id'],2)
        self.assertEqual(choose_activity(queue,{},completed_topics=[10])['task_id'],2)
        self.assertEqual(choose_activity(queue,{30:9})['task_id'],3)
        self.assertIsNone(choose_activity([],{}))
        self.assertIsNone(choose_activity(queue,{},captured_tasks=[1,2,3]))

    def test_reviews_and_lessons_draw_identical_sequences_with_same_weights(self):
        lesson_rng,review_rng=random.Random(42),random.Random(42)
        lessons=[choose_sequence(lesson_rng) for _ in range(10000)]
        reviews=[choose_review_sequence(review_rng) for _ in range(10000)]
        self.assertEqual(lessons,reviews)
        self.assertEqual(set(reviews),{'CWCWC','WCWCC'})

    def test_normalization_preserves_fraction_grouping(self):
        self.assertEqual(normalize(r'\frac{{x}^{3}}{3}'),normalize(r'\frac{x^{3}}{3}'))
        self.assertNotEqual(normalize(r'\frac{1}{23}'),normalize(r'\frac{12}{3}'))

    def test_mathquill_normalization_accepts_rational_exponent_notation_and_keeps_grouping(self):
        expected = normalize_mathquill('(x+8)^{1/3}')
        self.assertEqual(expected,normalize_mathquill(r'\left(x+8\right)^{\frac{1}{3}}'))
        self.assertEqual(expected,normalize_mathquill(r'\left(x+8\right)^{\tfrac{1}{3}}'))
        for different in ('(x+8)^1/3','(x+8)^{1}/3','(x+8)^{3}',
                          '(x+8)^{1/23}','(x+8)^{12/3}',r'(x+8)^{\frac{1}{3x}}'):
            self.assertNotEqual(expected,normalize_mathquill(different))
        self.assertNotEqual(normalize_mathquill(r'\frac{11\pi}{6}'),
                            normalize_mathquill(r'\frac{11pi}{6}'))

    def test_image_identity_reuses_identical_local_bytes_across_captures(self):
        with tempfile.TemporaryDirectory() as work:
            first,second=Path(work)/'first.png',Path(work)/'alias.png'
            first.write_bytes((REVIEW_FIXTURE/'assets/q-28197-a-1.png').read_bytes())
            second.write_bytes((REVIEW_FIXTURE/'assets/q-28197-e-0.png').read_bytes())
            self.assertEqual(normalize(str(first),'image'),normalize(str(second),'image'))
            second.write_bytes((REVIEW_FIXTURE/'assets/q-28197-a-2.png').read_bytes())
            self.assertNotEqual(normalize(str(first),'image'),normalize(str(second),'image'))


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.content = json.loads((FIXTURE/'content.json').read_text())
        self.topic = loads((FIXTURE/'database-before.edn').read_text())[0][0]
        self.existing = {r[0][':question/math-academy-id']:r[0] for r in loads((FIXTURE/'id-matches.edn').read_text())}

    def test_real_capture_preserves_three_existing_fields_and_all_examples(self):
        transaction, report = build_transaction(self.content,self.topic,self.existing)
        self.assertEqual(sum(r['existing'] for r in report),6)
        self.assertEqual(sum(not r['existing'] for r in report),12)
        for row in transaction:
            self.assertTrue({str(k)[1:] for k in row}<=ALLOWED|{'db/id','db/ensure'})
            if isinstance(row[':db/id'],list) and row[':db/id'][0]==':question/math-academy-id':
                self.assertEqual(set(row),{':db/id',':db/ensure',':question/difficulty',':question/worked-solution'})
        self.assertEqual(sum(':knowledge-point/questions' in r for r in transaction),12)
        self.assertFalse(any(':knowledge-point/canonical-example' in r for r in transaction))
        self.assertEqual(sum(':answer/id' in r for r in transaction),60)
        self.assertEqual(loads(dumps(transaction)),transaction)

    def test_correct_answer_conflict_aborts(self):
        content = copy.deepcopy(self.content)
        q = next(q for q in content['questions'] if q['math_academy_id']=='q-29828')
        q['answer_fields'][0]['correct_value'] = q['answer_fields'][0]['choices'][1]['value']
        with self.assertRaisesRegex(ValueError,'Correct answer conflict'):
            build_transaction(content,self.topic,self.existing)

    def test_wrong_kp_aborts(self):
        content = copy.deepcopy(self.content)
        content['questions'][0]['knowledge_point_id'] = str(uuid.uuid4())
        with self.assertRaisesRegex(ValueError,'KP is not a member'):
            build_transaction(content,self.topic,self.existing)

    def test_retractions_and_learner_writes_rejected(self):
        db = Database(SimpleNamespace())
        attrs = [(1,kw('question/problem')),(2,kw('learner/id')),(3,kw('db/txInstant'))]
        db.validate_datoms({':edb/tx-data':[[10,1,'problem',100,True]]},attrs)
        for row in ([10,2,uuid.uuid4(),100,True],[10,1,'problem',100,False]):
            with self.assertRaises(ValueError):
                db.validate_datoms({':edb/tx-data':[row]},attrs)

    def test_kp_mapping_uses_example_id_before_title(self):
        kp = kp_for_example(self.topic,'e-371','Example: Changed display title')
        self.assertEqual(kp[':knowledge-point/title'],'Computing an Integral Using the Sum Rule')


class ProgressTests(unittest.TestCase):
    def observation(self):
        return {'declared_topics':['1 topic'], 'units_html':'<div id="units"></div>',
                'rows':[{'title':'Topic', 'href':'/topics/1060?courseId=111', 'color':'white'}]}

    def test_incomplete_unknown_color_and_wrong_course_stop_capture(self):
        self.assertEqual(normalize_course(111,self.observation())[0]['display_band'],0)
        for key,value in [('declared_topics',['2 topics']),('rows',[{'title':'Topic','href':'/topics/1060?courseId=111','color':'purple'}])]:
            observed = self.observation(); observed[key] = value
            with self.assertRaises(ValueError): normalize_course(111,observed)
        with self.assertRaises(ValueError): normalize_course(136,self.observation())

    def test_changes_preserve_course_context_for_shared_topics(self):
        before = {'courses':[{'course_id':c,'topics':[{'topic_id':1060,'title':'Shared','color':'white','display_band':0}]} for c in (111,136)]}
        after = copy.deepcopy(before)
        after['courses'][0]['topics'][0].update(color='rgb(165, 207, 243)',display_band=2)
        diff = changes(before,after)
        self.assertEqual(len(diff),1)
        self.assertEqual((diff[0]['course_id'],diff[0]['before_band'],diff[0]['after_band']),(111,0,2))


class RunnerTests(unittest.TestCase):
    def test_run_discovers_unfinished_capture_and_import_before_new_activity(self):
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--output',work+'/captures','--state-dir',work+'/state'])
            done=Path(work)/'captures/1'; pending=Path(work)/'captures/2'
            for path in (done,pending):
                path.mkdir(parents=True)
                (path/'state.json').write_text(json.dumps({'task_id':int(path.name)}))
            (done/'edb-import').mkdir()
            (done/'edb-import/verification.json').write_text('{"committed":true}')
            self.assertEqual(unfinished_run(args),pending.resolve())
            # Even a finished website activity resumes if its content import failed.
            (pending/'state.json').write_text('{"task_id":2,"activity_complete":true,"history_complete":true}')
            self.assertEqual(unfinished_run(args),pending.resolve())
            (pending/'state.json').write_text('{"task_id":2,"import_complete":true}')
            self.assertIsNone(unfinished_run(args))

    def test_required_review_then_lesson_refreshes_queue_and_keeps_lesson_eligible(self):
        selected = []
        queues = iter([[{'task_id':1,'topic_id':2084,'task_type':'review','title':'Review','href':'/tasks/1/topics/2084/review'}],
                       [{'task_id':2,'topic_id':2084,'task_type':'lesson','title':'Lesson','href':'/tasks/2/topics/2084/lesson'}], []])
        class FixtureBrowser:
            def __init__(self,*args): pass
            def queue(self): return next(queues)
            def start(self,activity): selected.append(activity['task_type'])
            def knowledge_snapshot(self,*args): pass
            def activity(self,state,*args): state['activity_complete']=True
            def history(self,state,*args): return {'task_id':state['task_id'],'task_type':state['task_type']}
        db=Mock()
        db.priorities.return_value={2084:10}
        db.topic.return_value={}
        db.import_content.return_value={'previewed':True,'database_writes':0}
        context=SimpleNamespace(pages=[SimpleNamespace()],close=Mock())
        runtime=Mock()
        runtime.__enter__=Mock(return_value=runtime)
        runtime.__exit__=Mock(return_value=False)
        runtime.chromium.launch_persistent_context.return_value=context
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--limit','2','--preview','--state-dir',work+'/state','--output',work+'/capture',
                            '--lesson-min','0','--lesson-max','0'])
            with patch('capture.Database',return_value=db),patch('browser.CaptureBrowser',FixtureBrowser), \
                 patch('playwright.sync_api.sync_playwright',return_value=runtime),contextlib.redirect_stdout(io.StringIO()):
                run(args)
            self.assertEqual(selected,['review','lesson'])
            self.assertEqual(db.priorities.call_count,3)
            self.assertEqual(db.import_content.call_count,2)
            self.assertTrue(all(call.args[2] is False for call in db.import_content.call_args_list))
            entries=[json.loads(line) for line in (Path(work)/'state/journal.jsonl').read_text().splitlines()]
            captured=[e for e in entries if e['event']=='activity_captured']
            self.assertEqual([e['task_type'] for e in captured],['review','lesson'])
            observed=[e for e in entries if e['event']=='queue_observed']
            self.assertEqual([e['after_task_id'] for e in observed],[None,1,2])
            first=json.loads((Path(work)/'capture/1/queue-after.json').read_text())
            last=json.loads((Path(work)/'capture/2/queue-after.json').read_text())
            self.assertEqual(first['selected']['task_id'],2)
            self.assertEqual(last['queue'],[])
        context.close.assert_called_once()

    def test_unranked_lesson_runs_and_logs_remaining_queue_at_batch_limit(self):
        queue = [{'task_id':1,'topic_id':10,'task_type':'lesson','title':'First unranked',
                  'href':'/tasks/1/topics/10/lesson'},
                 {'task_id':2,'topic_id':20,'task_type':'lesson','title':'Next unranked',
                  'href':'/tasks/2/topics/20/lesson'}]
        selected=[]
        class FixtureBrowser:
            def __init__(self,*args): pass
            def queue(self): return queue if not selected else queue[1:]
            def start(self,activity): selected.append(activity)
            def activity(self,state,*args): state['activity_complete']=True
            def history(self,state,*args): return {'task_id':state['task_id']}
        db=Mock()
        db.priorities.return_value={}
        db.topic.return_value={}
        db.import_content.return_value={'previewed':True}
        context=SimpleNamespace(pages=[SimpleNamespace()],close=Mock())
        runtime=Mock()
        runtime.__enter__=Mock(return_value=runtime)
        runtime.__exit__=Mock(return_value=False)
        runtime.chromium.launch_persistent_context.return_value=context
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--limit','1','--preview','--state-dir',work+'/state','--output',work+'/capture'])
            with patch('capture.Database',return_value=db),patch('browser.CaptureBrowser',FixtureBrowser), \
                 patch('playwright.sync_api.sync_playwright',return_value=runtime), \
                 contextlib.redirect_stdout(io.StringIO()),self.assertLogs(level='INFO') as logs:
                run(args)
            self.assertEqual([a['task_id'] for a in selected],[1])
            self.assertEqual(selected[0]['selection_reason'],'queue_fallback')
            after=json.loads((Path(work)/'capture/1/queue-after.json').read_text())
            self.assertEqual(after['after_task_id'],1)
            self.assertEqual(after['selected']['task_id'],2)
            self.assertTrue(any('Available queue after task 1: 1 activities' in l for l in logs.output))
            self.assertTrue(any('Next unranked' in l for l in logs.output))


class DOMTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise unittest.SkipTest('Playwright not installed; use the MA Python environment')
        cls.runtime = sync_playwright().start()
        cls.browser = cls.runtime.chromium.launch(headless=True)
        cls.context = cls.browser.new_context(offline=True)

    def setUp(self):
        # Each fixture starts with a fresh URL and page timeout. A previous test
        # ending at /learn must not make queue() skip loading its own fixture.
        self.page = self.context.new_page()

    def tearDown(self):
        for page in self.context.pages:
            page.close()

    @classmethod
    def tearDownClass(cls):
        cls.context.close()
        cls.browser.close()
        cls.runtime.stop()

    def test_activity_wait_ignores_initial_numbered_placeholder(self):
        self.page.set_content('<div id="stepButton-1" class="stepButton current"></div>'
            '<script>setTimeout(()=>document.querySelector(".current").id="stepButton-t2583",150)</script>')
        args=SimpleNamespace(timeout_ms=5000)
        browser=CaptureBrowser(self.page,args,None,None)
        browser.wait_activity_ready()
        self.assertEqual(self.page.locator('.current').get_attribute('id'),'stepButton-t2583')

    def test_restore_uses_unanswered_widget_when_navigation_marker_is_stale(self):
        self.page.set_content('<div id="stepButton-q1" class="stepButton current"></div>'
            '<div id="step-q1" class="step questionWidget"><div class="questionWidget-result">Correct</div></div>'
            '<div id="continueButton-q1" style="display:none">Continue</div>'
            '<div id="step-q2" class="step questionWidget"><div class="questionWidget-submitButton">Submit</div></div>')
        browser=CaptureBrowser(self.page,SimpleNamespace(timeout_ms=5000),None,None)
        browser.wait_activity_ready()
        self.assertEqual(browser.current_step(),'stepButton-q2')

    def test_all_fifteen_real_widgets_before_and_after_submission(self):
        live = json.loads((FIXTURE/'live-capture.json').read_text())
        for record in live['responses']:
            before = next(s for s in live['steps'] if s['dom_id']=='step-q'+record['question_id'])
            self.page.set_content(before['html'])
            captured = self.page.locator('#'+before['dom_id']).evaluate(EXTRACT)
            self.assertFalse(captured['errors'],record['question_id'])
            self.assertEqual(len(captured['fields']),1)
            self.assertEqual(captured['fields'][0]['type'],'radio')
            self.assertEqual(len(captured['fields'][0]['choices']),5)
            self.assertEqual(normalize(captured['problem']),normalize(before['prompt']['markdown']))
            self.page.set_content(record['after']['html'])
            after = self.page.locator('#'+before['dom_id']).evaluate(EXTRACT)
            self.assertFalse(after['errors'])
            self.assertTrue(after['worked_solution'])
            self.assertEqual(after['result'],record['actual_result'])

    def test_queue_and_start_support_both_kinds_and_ignore_in_progress_tasks(self):
        queue_html = '<div id="incompleteTasks">'+''.join(
            '<div id="task-'+str(task)+'" class="taskUnlocked" progress="'+progress+'">'
            '<span class="taskTypeUnlocked">'+kind.title()+'</span><span id="taskName-'+str(task)+'">Topic</span>'
            '<a class="taskStartButton" id="start-'+str(task)+'" style="display:none" href="/tasks/'+str(task)+'/topics/2084/'+kind+'">Start</a></div>'
            for task,kind,progress in [(100,'review','0'),(101,'lesson','0'),(102,'review','2')])+'</div>'
        queue_html += '<script>document.querySelectorAll(".taskUnlocked").forEach(n=>n.onclick=()=>n.querySelector("a").style.display="block");</script>'
        self.context.unroute('https://mathacademy.com/**')
        self.context.route('https://mathacademy.com/**',lambda route:route.fulfill(status=200,content_type='text/html',body=queue_html if route.request.url.endswith('/learn') else '<p>Activity</p>'))
        args=SimpleNamespace(timeout_ms=5000,settle_ms=0,event_min=0,event_max=0)
        browser=CaptureBrowser(self.page,args,Pacer(args,random.Random(42)),None)
        queue=browser.queue()
        self.assertEqual([(a['task_id'],a['task_type']) for a in queue],[(100,'review'),(101,'lesson')])
        for activity in queue:
            browser.navigate('https://mathacademy.com/learn',force=True)
            browser.start(activity)
            self.assertEqual(self.page.url,'https://mathacademy.com'+activity['href'])

    def test_svg_duplicate_title_ids_are_scoped_locally(self):
        self.page.set_content('<span class="mjpage"><svg><title id="same">x+1</title></svg></span><div id="test"><div class="exampleQuestion"><span class="mjpage"><svg><title id="same">x^2+1</title></svg></span></div><div class="exampleExplanation">solution</div></div>')
        item = self.page.locator('#test').evaluate(EXTRACT)
        self.assertEqual(item['problem'],'$x^2+1$')

    def complex_argument_fixture(self):
        # Actual explanation that stopped task 13929099 after a correct submission.
        html = (Path(__file__).parent/'fixtures/q-8257-after.html').read_text()
        self.page.set_content(html)
        scope = self.page.locator('#step-q8257')
        # Use a local fixture image; the failed live capture did not save its graph.
        pixels = (REVIEW_FIXTURE/'assets/q-28197-a-1.png').read_bytes()
        source = 'data:image/png;base64,' + base64.b64encode(pixels).decode()
        scope.locator('.graphic img').evaluate('(n, src) => n.src = src',source)
        return scope, source

    def test_real_complex_argument_explanation_omits_invisible_phantom_fraction(self):
        scope, _ = self.complex_argument_fixture()
        item = scope.evaluate(EXTRACT)
        self.assertEqual(item['result'],'Correct')
        self.assertFalse(item['errors'])
        self.assertIn(r'≈0.927\,30.',item['worked_solution'])
        self.assertNotIn(r'\frac{1}{1}',item['worked_solution'])

    def test_read_waits_for_delayed_explanation_graph(self):
        scope, source = self.complex_argument_fixture()
        graphic = scope.locator('.graphic img')
        graphic.evaluate("n => { n.style.display = 'none'; n.removeAttribute('src'); }")
        self.assertFalse(graphic.is_visible())
        graphic.evaluate('''(n, src) => setTimeout(() => {
          n.src = src; n.style.display = 'block';
        }, 300)''',source)
        browser = CaptureBrowser(self.page,SimpleNamespace(timeout_ms=3000),None,None)
        with tempfile.TemporaryDirectory() as work:
            item, screenshot = browser.read(scope,work,'q-8257-after')
            self.assertFalse(item['errors'])
            self.assertTrue(screenshot.exists())
            self.assertTrue(Path(item['assets'][0]['path']).exists())
            self.assertNotIn('@asset-',item['worked_solution'])

    def test_unrendered_graph_still_stops_and_preserves_diagnostics(self):
        scope, _ = self.complex_argument_fixture()
        scope.locator('.graphic img').evaluate("n => n.style.display = 'none'")
        browser = CaptureBrowser(self.page,SimpleNamespace(timeout_ms=1000),None,None)
        with tempfile.TemporaryDirectory() as work:
            with self.assertRaisesRegex(ValueError,'Visual asset is not rendered'):
                browser.read(scope,work,'q-8257-after')
            item = json.loads((Path(work)/'q-8257-after.json').read_text())
            self.assertEqual(item['errors'],['Visual asset is not rendered'])
            self.assertTrue((Path(work)/'q-8257-after.png').exists())

    def test_submitting_checkpoint_recovers_real_correct_grade_without_resubmitting(self):
        scope, _ = self.complex_argument_fixture()
        self.page.evaluate('''() => {
          const b = document.createElement('button'); b.id = 'continueButton-q8257';
          b.textContent = 'Continue'; document.body.append(b);
          const final = document.createElement('div'); final.id = 'finalScreen';
          final.style.display = 'none'; document.body.append(final);
          window.submissions = 0;
          document.addEventListener('click', e => {
            if (e.target.closest('.questionWidget-submitButton')) window.submissions++;
          });
        }''')
        item = scope.evaluate(EXTRACT)
        decision = {'confident':True,'answers':[{'key':'selection','correct_option':'d',
                    'correct_value':'2.21','value_type':'math'}]}
        state = {'task_id':13929099,'topic_id':893,'task_type':'review',
                 'review_sequence':'CWCWC','kps':{},'examples':{},'questions':{
                     'q-8257':{'kp_id':None,'before':item,'decision':decision,
                               'intended':'C','status':'submitting'}}}
        solver = Mock()
        browser = CaptureBrowser(self.page,SimpleNamespace(timeout_ms=3000),None,solver)
        browser.advance = Mock(side_effect=RuntimeError('Stop after recovered grade'))
        with tempfile.TemporaryDirectory() as work:
            with self.assertRaisesRegex(RuntimeError,'Stop after recovered grade'):
                browser.review(state,work,{})
            restored = json.loads((Path(work)/'state.json').read_text())
            question = restored['questions']['q-8257']
            self.assertEqual(question['status'],'graded')
            self.assertEqual(question['actual_result'],'Correct')
            self.assertTrue(question['finalized'])
            self.assertNotIn(r'\frac{1}{1}',question['content']['worked_solution'])
            self.assertEqual(self.page.evaluate('window.submissions'),0)
            solver.solve.assert_not_called()

    def test_mixed_native_fields_keep_field_locations_and_choice_values(self):
        self.page.set_content('<div id="test"><div class="questionWidget-text">x=<input id="blank" type="text">; sign=<select id="select"><option disabled value="">Choose</option><option value="plus">+</option><option value="minus">−</option></select></div></div>')
        item = self.page.locator('#test').evaluate(EXTRACT)
        self.assertFalse(item['errors'])
        self.assertEqual([f['type'] for f in item['fields']],['blank','select'])
        self.assertIn('{{field-1}}',item['problem'])
        self.assertIn('{{field-2}}',item['problem'])
        self.assertEqual([c['option'] for c in item['fields'][1]['choices']],['plus','minus'])

    def mathquill_fixture(self, menu=False):
        vendor = Path(__file__).parent/'fixtures/vendor'
        self.page.set_content('<div id="test"><div class="questionWidget-text">Enter the answer</div>'
            '<div id="answer" class="matheditor-wrapper-answer"><span id="mq"></span></div>'
            '<button class="questionWidget-submitButton">Submit</button></div>')
        self.page.add_style_tag(path=str(vendor/'mathquill-0.10.1.css'))
        self.page.add_script_tag(path=str(vendor/'jquery-3.7.1.min.js'))
        # This is the exact public MathQuill distribution loaded by Math Academy.
        self.page.add_script_tag(path=str(vendor/'mathquill-ma.v2.1.min.js'))
        self.page.evaluate('''menu => {
          const MQ = MathQuill.getInterface(2);
          const field = MQ.MathField(document.querySelector('#mq'));
          window.submissions = 0;
          document.querySelector('.questionWidget-submitButton').onclick = () => window.submissions++;
          if (menu) {
            const toolbox = document.createElement('div'); toolbox.id = 'mathEditorToolbox';
            const pi = document.createElement('button'); pi.className = 'mathIcon piIcon'; pi.textContent = 'π';
            pi.onmousedown = e => e.preventDefault();
            pi.onclick = () => { field.cmd('\\\\pi'); field.focus(); };
            toolbox.append(pi); document.body.append(toolbox);
          }
        }''',menu)
        scope = self.page.locator('#test')
        item = scope.evaluate(EXTRACT)
        decision = {'answers':[{'key':'field-1','correct_value':r'\frac{11\pi}{6}',
                    'value_type':'math',
                    'wrong_value':r'\frac{\pi}{6}',
                    'correct_keys':[{'text':'11pi/6','key':None},{'text':None,'key':'ArrowRight'}],
                    'wrong_keys':[{'text':'pi/6','key':None},{'text':None,'key':'ArrowRight'}]}]}
        return scope, {'before':item,'decision':decision,'intended':'C'}

    def test_mathquill_pi_uses_visible_symbol_menu_and_verifies_the_value(self):
        scope, record = self.mathquill_fixture(menu=True)
        args = SimpleNamespace(timeout_ms=3000,event_min=0,event_max=0)
        browser = CaptureBrowser(self.page,args,Pacer(args,random.Random(42)),None)
        browser.enter(scope,record)
        browser.verify_entered(scope,record)
        field = record['before']['fields'][0]
        self.assertEqual(normalize(field['observed_mathquill_latex']),normalize(r'\frac{11\pi}{6}'))
        self.assertEqual(field['clicked_symbols'][0]['symbol'],'pi')
        self.assertEqual(self.page.evaluate('window.submissions'),0)

    def test_mathquill_pi_falls_back_to_explicit_command_and_handles_wrong_answers(self):
        for intended, value in [('C',r'\frac{11\pi}{6}'),('W',r'\frac{\pi}{6}')]:
            scope, record = self.mathquill_fixture()
            record['intended'] = intended
            args = SimpleNamespace(timeout_ms=3000,event_min=0,event_max=0)
            browser = CaptureBrowser(self.page,args,Pacer(args,random.Random(42)),None)
            browser.enter(scope,record)
            browser.verify_entered(scope,record)
            field = record['before']['fields'][0]
            self.assertEqual(normalize(field['observed_mathquill_latex']),normalize(value))
            self.assertFalse(field.get('clicked_symbols'))

    def test_mathquill_rejects_original_literal_pi_and_incorrect_fraction_grouping(self):
        for typed in ('11pi/6','11/6pi'):
            scope, record = self.mathquill_fixture()
            args = SimpleNamespace(timeout_ms=3000)
            browser = CaptureBrowser(self.page,args,None,None)
            editor = scope.locator('.mq-textarea textarea')
            editor.focus()
            editor.press_sequentially(typed)
            record['before']['fields'][0]['submitted_value'] = r'\frac{11\pi}{6}'
            with self.assertRaisesRegex(ValueError,'Actual MathQuill value differs'):
                browser.verify_entered(scope,record)
            self.assertEqual(self.page.evaluate('window.submissions'),0)

    def test_real_two_field_answer_accepts_mathquill_fraction_inside_exponent(self):
        scope, record = self.mathquill_fixture()
        self.page.evaluate('''() => {
          const wrapper = document.createElement('div'); wrapper.id = 'answer2';
          wrapper.className = 'matheditor-wrapper-answer';
          const node = document.createElement('span'); wrapper.append(node);
          document.querySelector('#test').append(wrapper);
          MathQuill.getInterface(2).MathField(node);
        }''')
        record['before'] = scope.evaluate(EXTRACT)
        record['decision']['answers'] = [
            {'key':'field-1','correct_value':'(x+8)^{1/3}','wrong_value':'(x+8)^3',
             'correct_keys':[{'text':'(x+8)^1/3','key':None},
                             {'text':None,'key':'ArrowRight'},{'text':None,'key':'ArrowRight'}],
             'wrong_keys':[{'text':'(x+8)^3','key':None},{'text':None,'key':'ArrowRight'}]},
            {'key':'field-2','correct_value':'2','wrong_value':'3',
             'correct_keys':[{'text':'2','key':None}],
             'wrong_keys':[{'text':'3','key':None}]}]
        args = SimpleNamespace(timeout_ms=3000,event_min=0,event_max=0)
        browser = CaptureBrowser(self.page,args,Pacer(args,random.Random(42)),None)
        browser.enter(scope,record)
        browser.verify_entered(scope,record)
        first,second = record['before']['fields']
        self.assertEqual(first['observed_mathquill_latex'],r'\left(x+8\right)^{\frac{1}{3}}')
        self.assertEqual(second['observed_mathquill_latex'],'2')
        first['submitted_value'] = '(x+8)^3'
        with self.assertRaisesRegex(ValueError,'Actual MathQuill value differs'):
            browser.verify_entered(scope,record)
        self.assertEqual(self.page.evaluate('window.submissions'),0)

    def test_moved_past_submission_reconciles_saved_grade_before_next_question(self):
        scope, _ = self.complex_argument_fixture()
        item = scope.evaluate(EXTRACT)
        pixels = (REVIEW_FIXTURE/'assets/q-28197-a-1.png').resolve()
        item['assets'][0]['path'] = str(pixels)
        record = {'kp_id':None,'before':item,'decision':{'answers':[{'key':'selection',
                  'correct_value':'2.21','value_type':'math'}]},'intended':'C','status':'submitting'}
        state = {'task_id':13929099,'topic_id':893,'task_type':'review','review_sequence':'CWCWC',
                 'questions':{'q-8257':record},'kps':{},'examples':{}}
        self.page.set_content('<div id="step-q2" class="step questionWidget">'
                              '<button class="questionWidget-submitButton">Submit</button></div>')
        solver = Mock()
        browser = CaptureBrowser(self.page,SimpleNamespace(timeout_ms=3000),None,solver)
        browser.check = Mock(side_effect=RuntimeError('Stop before next answer'))
        with tempfile.TemporaryDirectory() as work:
            source = Path(work)/'q-8257-after.json'
            source.write_text(json.dumps(item))
            with self.assertRaisesRegex(RuntimeError,'Stop before next answer'):
                browser.review(state,work,{})
            self.assertEqual(record['actual_result'],'Correct')
            self.assertTrue(record['finalized'])
            solver.solve.assert_not_called()
            record.update(status='submitting',finalized=False)
            item['errors'] = ['Visual asset is not rendered']
            source.write_text(json.dumps(item))
            with self.assertRaisesRegex(ValueError,'Previous submission needs a complete saved result'):
                browser.review(state,work,{})

    def test_content_retains_correct_pi_and_actual_literal_pi_as_distinct_choices(self):
        scope, record = self.mathquill_fixture()
        record['before']['fields'][0]['submitted_value'] = r'\frac{11pi}{6}'
        record['after'] = {'worked_solution':r'The argument is $\frac{11\pi}{6}$.'}
        content = CaptureBrowser.question_content('q-319581',record,{'id':None,'title':None})
        field = content['answer_fields'][0]
        self.assertEqual(field['correct_value'],r'\frac{11\pi}{6}')
        self.assertEqual([c['value'] for c in field['choices']],[r'\frac{11\pi}{6}',r'\frac{11pi}{6}'])

    def test_activity_solution_does_not_include_student_answer(self):
        history = json.loads((FIXTURE/'activity-capture.json').read_text())
        for kp in history['kps']:
            for q in kp['questions']:
                self.page.set_content(q['explanation_html'])
                item = self.page.locator('#'+q['id'].replace('question-','questionExplanation-')).evaluate(EXTRACT)
                self.assertTrue(item['worked_solution'])
                self.assertNotIn('Your Answer',item['worked_solution'])
                self.assertFalse(item['errors'])

    def lesson_fixture(self):
        live = json.loads((FIXTURE/'live-capture.json').read_text())
        content = json.loads((FIXTURE/'content.json').read_text())
        correct = {q['math_academy_id'][2:]:q['answer_fields'][0]['correct_letter'] for q in content['questions']}
        before = {s['dom_id']:s for s in live['steps']}
        after = {r['question_id']:r['after']['html'] for r in live['responses']}
        order = ['e371'] + ['q'+q['math_academy_id'][2:] for q in content['questions'][:5]] + ['e372'] + ['q'+q['math_academy_id'][2:] for q in content['questions'][5:10]] + ['e373'] + ['q'+q['math_academy_id'][2:] for q in content['questions'][10:]]
        raw = '\n'.join(before['step-'+token]['html'] for token in order)
        setup = '''const order=ORDER, after=AFTER, correct=CORRECT; let position=0, selected={};
        localStorage.setItem("fixture-submissions","0");localStorage.setItem("fixture-results","{}");
        const bar=document.createElement('div'); document.body.prepend(bar);
        for(const token of order){const b=document.createElement('div');b.id='stepButton-'+token;b.className='stepButton';bar.append(b);
          if(token[0]==='e'&&!document.getElementById('continueButton-'+token)){const c=document.createElement('button');c.id='continueButton-'+token;c.textContent='Continue';document.body.append(c);}}
        const final=document.createElement('div');final.id='finalScreen';final.style.display='none';
        final.innerHTML="Congratulations! You've completed the lesson.<button id='finalScreen-doneButton'>Continue</button>";document.body.append(final);
        function move(){document.querySelectorAll('.stepButton').forEach(n=>n.classList.remove('current'));
          for(const token of order){document.getElementById('step-'+token).style.display='none';
            const b=document.getElementById('continueButton-'+token);if(b)b.style.display='none';}
          if(position===order.length){final.style.display='block';return;}
          const token=order[position];document.getElementById('stepButton-'+token).classList.add('current');
          document.getElementById('step-'+token).style.display='block';
          if(token[0]==='e')document.getElementById('continueButton-'+token).style.display='block';}
        document.addEventListener('click',event=>{const n=event.target;
          if(n.id==='finalScreen-doneButton'){location.href='/learn';return;}
          if(n.id.startsWith('continueButton-')){position++;move();return;}
          if(n.id.startsWith('questionWidget-choiceLetterCircle-')){const token=order[position];selected[token]=n.textContent.trim();
            document.getElementById('step-'+token).querySelectorAll('.questionWidget-choiceLetterCircle').forEach(c=>c.removeAttribute('style'));
            n.style.background='rgb(64, 64, 64)';n.style.color='white';
            document.getElementById('step-'+token).querySelector('.questionWidget-submitButton').classList.remove('disabledButton');}
          if(n.classList.contains('questionWidget-submitButton')){const token=order[position],number=token.slice(1);
            const node=document.getElementById('step-'+token);node.outerHTML=after[number];
            document.getElementById('step-'+token).querySelector('.questionWidget-result').textContent=selected[token]===correct[number]?'Correct':'Incorrect';
            if(!document.getElementById('continueButton-'+token)){const b=document.createElement('button');b.id='continueButton-'+token;b.textContent='Continue';document.getElementById('step-'+token).append(b);}
            document.body.dataset.submissions=String(Number(document.body.dataset.submissions||0)+1);
            localStorage.setItem('fixture-submissions',document.body.dataset.submissions);
            const outcomes=JSON.parse(localStorage.getItem('fixture-results'));outcomes[number]=document.getElementById('step-q'+number).querySelector('.questionWidget-result').textContent;
            localStorage.setItem('fixture-results',JSON.stringify(outcomes));}
        });move();'''
        setup = setup.replace('ORDER',json.dumps(order)).replace('AFTER',json.dumps(after)).replace('CORRECT',json.dumps(correct)).replace('</script','<\\/script')
        lesson = raw+'<script>'+setup+'</script>'
        history = json.loads((FIXTURE/'activity-capture.json').read_text())
        activity = ''.join(k['html'] for k in history['kps']) + '''<script>
          document.querySelectorAll('.questionExplanation').forEach(e=>e.style.display='none');
          document.querySelectorAll('.answerDetails').forEach(e=>e.onclick=()=>document.getElementById(e.closest('.question').id.replace('question-','questionExplanation-')).style.display='block');
        </script>'''
        progress = {113:(ROOT/'sequences-graphs/MF1.txt').read_text(),111:(ROOT/'sequences-graphs/MF2.txt').read_text(),136:(ROOT/'sequences-graphs/MF3.txt').read_text()}
        submitted_count = 0
        results = {}
        def respond(route):
            nonlocal submitted_count
            url = route.request.url
            if '/courses/' in url:
                course = int(url.split('/courses/')[1].split('/')[0])
                submissions = self.page.evaluate("Number(localStorage.getItem('fixture-submissions')||0)")
                submitted_count = max(submitted_count, submissions)
                results.update(self.page.evaluate("JSON.parse(localStorage.getItem('fixture-results')||'{}')"))
                body = progress[course]
                if course == 111 and submitted_count:
                    body += '''<script>document.querySelector('.topicLink[href="/topics/3769?courseId=111"]').closest('tr').querySelector('.topicCircle').style.background='rgb(165, 207, 243)';</script>'''
            else:
                body = lesson if '/lesson' in url else activity if '?taskId=' in url else '<div id="incompleteTasks"></div>'
                if '?taskId=' in url:
                    body += '<script>const results='+json.dumps(results)+''';document.querySelectorAll('.question').forEach(q=>q.querySelector('.answerResult').textContent=results[q.id.slice(9)]);</script>'''
            route.fulfill(status=200,content_type='text/html; charset=utf-8',body=body)
        self.context.unroute('https://mathacademy.com/**')
        self.context.route('https://mathacademy.com/**',respond)
        self.page.goto('https://mathacademy.com/tasks/13925458/topics/3769/lesson')
        return correct

    def fixture_solver(self, correct):
        class FixtureSolver:
            def solve(self,item,screenshot,directory,phase='solve'):
                number = item['dom_id'].removeprefix('step-q')
                choice = next(c for c in item['fields'][0]['choices'] if c['option']==correct[number])
                return {'confident':True,'answers':[{'key':'selection','correct_option':choice['option'],
                    'correct_value':choice['value'],'value_type':choice['type'],'wrong_value':None,'correct_keys':[],'wrong_keys':[]}]}
        return FixtureSolver()

    def review_fixture(self, misselect=False, wrong_kp=False):
        """Real served DOM, with two explicitly synthetic copies to test 5/6 steps."""
        history = json.loads((REVIEW_FIXTURE/'activity-capture.json').read_text())['questions']
        manifest = json.loads((REVIEW_FIXTURE/'assets/manifest.json').read_text())
        numbers = ['28197','39032','39091','112434','99001','99002']
        original_numbers = numbers[:4] + ['112434','112434']
        correct, before, after, activity = {}, {}, {}, {}
        for number, original in zip(numbers,original_numbers):
            raw_before = json.loads((REVIEW_FIXTURE/('q'+original+'-before.json')).read_text())
            raw_after = json.loads((REVIEW_FIXTURE/('q'+original+'-after.json')).read_text())
            correct[number] = {'28197':'a','39032':'a','39091':'c','112434':'c'}[original]
            before[number] = raw_before['html'].replace(original,number)
            after[number] = raw_after['html'].replace(original,number)
            h = next(q for q in history if q['id']=='question-'+original)
            activity[number] = (h['raw_html']+h['explanation_html']).replace(original,number)
            if wrong_kp:
                activity[number] = activity[number].replace('/topics/2084#','/topics/9999#')
        setup = '''const numbers=NUMBERS, after=AFTER, correct=CORRECT; let position=0, selected={},streak=0;
        localStorage.setItem("fixture-submissions","0");localStorage.setItem("fixture-results","{}");
        const bar=document.createElement('div');document.body.prepend(bar);
        for(const number of numbers){const b=document.createElement('div');b.id='stepButton-q'+number;b.className='stepButton';bar.append(b);}
        const final=document.createElement('div');final.id='finalScreen';final.style.display='none';
        final.innerHTML="Congratulations! You've completed the review.<button id='finalScreen-doneButton'>Continue</button>";document.body.append(final);
        function move(){document.querySelectorAll('.stepButton').forEach(n=>n.classList.remove('current'));
          numbers.forEach(number=>{document.getElementById('step-q'+number).style.display='none';});
          if(streak>=2){final.style.display='block';return;}
          const number=numbers[position];document.getElementById('stepButton-q'+number).classList.add('current');
          document.getElementById('step-q'+number).style.display='block';}
        document.addEventListener('click',event=>{const n=event.target,number=numbers[position];
          if(n.id==='finalScreen-doneButton'){location.href='/learn';return;}
          if(n.id.startsWith('continueButton-')){position++;move();return;}
          if(n.id.startsWith('questionWidget-choiceLetterCircle-')){
            const root=document.getElementById('step-q'+number);
            root.querySelectorAll('.questionWidget-choiceLetterCircle').forEach(c=>c.removeAttribute('style'));
            const actual=MISSELECT ? root.querySelector('.questionWidget-choiceLetterCircle') : n;
            selected[number]=actual.textContent.trim();actual.style.background='rgb(64, 64, 64)';actual.style.color='white';
            root.querySelector('.questionWidget-submitButton').classList.remove('disabledButton');}
          if(n.classList.contains('questionWidget-submitButton')){
            document.getElementById('step-q'+number).outerHTML=after[number];
            const root=document.getElementById('step-q'+number),result=selected[number]===correct[number]?'Correct':'Incorrect';
            root.querySelector('.questionWidget-result').textContent=result;
            root.querySelectorAll('.questionWidget-choiceLetterCircle').forEach(c=>{c.removeAttribute('style');
              if(c.textContent.trim()===selected[number]){c.style.background='rgb(64, 64, 64)';c.style.color='white';}});
            streak=result==='Correct'?streak+1:0;
            if(!document.getElementById('continueButton-q'+number)){const b=document.createElement('button');b.id='continueButton-q'+number;b.textContent='Continue';root.append(b);}
            document.body.dataset.submissions=String(Number(document.body.dataset.submissions||0)+1);
            localStorage.setItem('fixture-submissions',document.body.dataset.submissions);
            const outcomes=JSON.parse(localStorage.getItem('fixture-results'));outcomes[number]=document.getElementById('step-q'+number).querySelector('.questionWidget-result').textContent;
            localStorage.setItem('fixture-results',JSON.stringify(outcomes));}
        });move();'''
        setup = setup.replace('NUMBERS',json.dumps(numbers)).replace('AFTER',json.dumps(after)).replace('CORRECT',json.dumps(correct)).replace('MISSELECT',str(misselect).lower()).replace('</script','<\\/script')
        review = ''.join(before.values())+'<script>'+setup+'</script>'
        progress = {c:(ROOT/('sequences-graphs/MF'+str(i)+'.txt')).read_text() for i,c in enumerate((113,111,136),1)}
        served, results = 0, {}
        def respond(route):
            nonlocal served, results
            url = route.request.url
            if '/graphics/' in url:
                original_url = url.replace('99001','112434').replace('99002','112434')
                asset = manifest.get(original_url)
                route.fulfill(status=200 if asset else 404,content_type='image/png',body=Path(asset['path']).read_bytes() if asset else b'')
                return
            if '/courses/' in url:
                served = max(served,self.page.evaluate("Number(localStorage.getItem('fixture-submissions')||0)"))
                results.update(self.page.evaluate("JSON.parse(localStorage.getItem('fixture-results')||'{}')"))
            if '/courses/' in url:
                course = int(url.split('/courses/')[1].split('/')[0]); body=progress[course]
            elif '/review' in url:
                body = review
            elif '?taskId=' in url:
                rows = [activity[n] for n in numbers[:served]]
                body = '<div class="reviewAnswerList">'+''.join(rows)+'</div><script>const results='+json.dumps(results)+''';
                document.querySelectorAll('.question').forEach(q=>q.querySelector('.answerResult').textContent=results[q.id.slice(9)]);
                document.querySelectorAll('.questionExplanation').forEach(e=>e.style.display='none');
                document.querySelectorAll('.answerDetails').forEach(e=>e.onclick=()=>document.getElementById(e.closest('.question').id.replace('question-','questionExplanation-')).style.display='block');</script>'''
            else: body='<div id="incompleteTasks"></div>'
            route.fulfill(status=200,content_type='text/html; charset=utf-8',body=body)
        self.context.unroute('https://mathacademy.com/**')
        self.context.route('https://mathacademy.com/**',respond)
        return correct

    def test_reviews_capture_shared_sequences_map_mixed_kps_and_original_images(self):
        for weight, base, served in [(0,'WCWCC','WCWCC'),(1,'CWCWC','CWCWCC')]:
            correct=self.review_fixture()
            args=SimpleNamespace(timeout_ms=5000,cwcwc_weight=weight,settle_ms=0,event_min=0,event_max=0,answer_min=0,answer_max=0)
            browser=CaptureBrowser(self.page,args,Pacer(args,random.Random(42)),self.fixture_solver(correct))
            self.page.goto('https://mathacademy.com/tasks/13925710/topics/2084/review')
            state={'task_id':13925710,'topic_id':2084,'kps':{},'examples':{},'questions':{}}
            topic=loads((REVIEW_FIXTURE/'database/topic.edn').read_text())[0][0]
            with tempfile.TemporaryDirectory() as work:
                browser.review(state,work,topic)
                self.assertEqual(state['review_sequence'],base)
                self.assertEqual(''.join(q['intended'] for q in state['questions'].values()),served)
                self.assertTrue(state['review_complete'])
                content=browser.history(state,work,topic)
                self.assertEqual(len(content['questions']),len(served))
                self.assertEqual(len(state['kps']),3)
                self.assertEqual(content['canonical_examples'],[])
                self.assertTrue(all(q['difficulty'] and q['knowledge_point_id'] and q['worked_solution'] for q in content['questions']))
                images=json.loads((Path(work)/'assets/manifest.json').read_text())
                self.assertTrue(all(a['representation']=='original' for a in images.values()))
                source='https://mathacademy.com/graphics/q-28197-'
                self.assertEqual(images[source+'a-1']['path'],images[source+'e-0']['path'])
                self.assertEqual(list(state['knowledge_snapshots']),['review-completed'])
                transaction,_=build_transaction(content,topic,{})
                self.assertEqual(sum(':knowledge-point/questions' in row for row in transaction),len(served))

    def test_actual_radio_selection_mismatch_stops_before_submit(self):
        correct=self.review_fixture(misselect=True)
        args=SimpleNamespace(timeout_ms=5000,cwcwc_weight=0,review_policy='maximize',settle_ms=0,event_min=0,event_max=0,answer_min=0,answer_max=0)
        browser=CaptureBrowser(self.page,args,Pacer(args,random.Random(42)),self.fixture_solver(correct))
        self.page.goto('https://mathacademy.com/tasks/13925710/topics/2084/review')
        state={'task_id':13925710,'topic_id':2084,'kps':{},'examples':{},'questions':{}}
        with tempfile.TemporaryDirectory() as work:
            with self.assertRaisesRegex(ValueError,'Actual selected radio option'):
                browser.review(state,work,{})
            self.assertIsNone(self.page.locator('body').get_attribute('data-submissions'))
            self.assertEqual(state['questions']['q-28197']['status'],'prepared')

    def test_review_activity_rejects_kp_link_to_another_topic(self):
        correct=self.review_fixture(wrong_kp=True)
        args=SimpleNamespace(timeout_ms=5000,cwcwc_weight=0,settle_ms=0,event_min=0,event_max=0,answer_min=0,answer_max=0)
        browser=CaptureBrowser(self.page,args,Pacer(args,random.Random(42)),self.fixture_solver(correct))
        self.page.goto('https://mathacademy.com/tasks/13925710/topics/2084/review')
        state={'task_id':13925710,'topic_id':2084,'kps':{},'examples':{},'questions':{}}
        topic=loads((REVIEW_FIXTURE/'database/topic.edn').read_text())[0][0]
        with tempfile.TemporaryDirectory() as work:
            browser.review(state,work,topic)
            self.assertEqual(state['review_sequence'],'WCWCC')
            self.assertEqual(len(state['questions']),5)
            with self.assertRaisesRegex(ValueError,'valid topic/KP source link'):
                browser.history(state,work,topic)

    def test_sequential_capture_and_activity_join_end_to_end_offline(self):
        correct = self.lesson_fixture()
        args = SimpleNamespace(timeout_ms=5000,cwcwc_weight=0.7,settle_ms=0,event_min=0,event_max=0,answer_min=0,answer_max=0)
        browser = CaptureBrowser(self.page,args,Pacer(args,random.Random(42)),self.fixture_solver(correct))
        state = {'task_id':13925458,'topic_id':3769,'kps':{},'examples':{},'questions':{}}
        topic = loads((FIXTURE/'database-before.edn').read_text())[0][0]
        with tempfile.TemporaryDirectory() as work:
            browser.lesson(state,work,topic)
            content = browser.history(state,work)
            self.assertTrue(state['lesson_complete'])
            self.assertTrue(state['history_complete'])
            self.assertEqual(len(content['questions']),15)
            self.assertEqual(len(content['canonical_examples']),3)
            self.assertTrue(all(q['difficulty'] for q in content['questions']))
            self.assertTrue((Path(work)/'lesson-completed.png').is_file())
            self.assertEqual(list(state['knowledge_snapshots']),['lesson-completed'])
            snapshot=json.loads((Path(work)/'knowledge-state/lesson-completed.json').read_text())
            self.assertEqual(sum(len(c['topics']) for c in snapshot['courses']),1040)
            browser.knowledge_snapshot(state,work,'lesson-completed')
            self.assertEqual(len(state['knowledge_snapshots']),1)
            self.assertEqual(self.page.url,'https://mathacademy.com/learn?taskId=13925458')
            existing = {r[0][':question/math-academy-id']:r[0] for r in loads((FIXTURE/'id-matches.edn').read_text())}
            transaction,_ = build_transaction(content,topic,existing)
            self.assertTrue(transaction)

    def test_completion_snapshot_failure_resumes_without_resubmitting_answer(self):
        correct = self.lesson_fixture()
        args = SimpleNamespace(timeout_ms=5000,cwcwc_weight=0.7,settle_ms=0,event_min=0,event_max=0,answer_min=0,answer_max=0)
        browser = CaptureBrowser(self.page,args,Pacer(args,random.Random(42)),self.fixture_solver(correct))
        state = {'task_id':13925458,'topic_id':3769,'kps':{},'examples':{},'questions':{}}
        topic = loads((FIXTURE/'database-before.edn').read_text())[0][0]
        original = browser.knowledge_snapshot
        browser.knowledge_snapshot = Mock(side_effect=RuntimeError('Simulated snapshot interruption'))
        with tempfile.TemporaryDirectory() as work:
            with self.assertRaisesRegex(RuntimeError,'snapshot interruption'):
                browser.lesson(state,work,topic)
            self.assertEqual(len(state['questions']),15)
            self.assertTrue(state['activity_complete'])
            self.assertTrue(all(q['finalized'] for q in state['questions'].values()))
            browser.knowledge_snapshot = original
            browser.lesson(state,work,topic)
            saved=json.loads((Path(work)/'knowledge-state/lesson-completed.json').read_text())
            self.assertTrue(saved['recovered_after_interruption'])
            self.assertEqual(len(state['questions']),15)
            self.assertEqual(list(state['knowledge_snapshots']),['lesson-completed'])

    def test_legacy_continue_checkpoint_resumes_without_repeating_answer(self):
        correct=self.lesson_fixture()
        args=SimpleNamespace(timeout_ms=5000,cwcwc_weight=1,settle_ms=0,event_min=0,event_max=0,answer_min=0,answer_max=0)
        browser=CaptureBrowser(self.page,args,Pacer(args,random.Random(42)),self.fixture_solver(correct))
        state={'task_id':13925458,'topic_id':3769,'kps':{},'examples':{},'questions':{}}
        topic=loads((FIXTURE/'database-before.edn').read_text())[0][0]
        original=browser._continue
        def interrupted(identifier):
            original(identifier)
            if identifier=='continueButton-q71168':
                raise KeyboardInterrupt()
        browser._continue=interrupted
        with tempfile.TemporaryDirectory() as work:
            with self.assertRaises(KeyboardInterrupt):
                browser.lesson(state,work,topic)
            self.assertEqual(self.page.locator('body').get_attribute('data-submissions'),'1')
            restored=json.loads((Path(work)/'state.json').read_text())
            # Shape of the user's checkpoint saved by the previous script.
            restored['pending_knowledge_snapshot']={**restored.pop('pending_continue'),'event':'after-q71168'}
            browser._continue=original
            browser.lesson(restored,work,topic)
            self.assertEqual(len(restored['questions']),15)
            self.assertEqual(self.page.evaluate("Number(localStorage.getItem('fixture-submissions'))"),15)
            self.assertNotIn('pending_knowledge_snapshot',restored)
            self.assertNotIn('pending_continue',restored)
            self.assertEqual(list(restored['knowledge_snapshots']),['lesson-completed'])

    def test_unexpected_wrong_answer_stops_before_second_submission(self):
        self.lesson_fixture()
        class IncorrectSolver:
            def solve(self,item,*args):
                choice = item['fields'][0]['choices'][0]  # First answer is demonstrably wrong.
                return {'confident':True,'answers':[{'key':'selection','correct_option':choice['option'],
                    'correct_value':choice['value'],'value_type':choice['type'],'wrong_value':None,'correct_keys':[],'wrong_keys':[]}]}
        args = SimpleNamespace(timeout_ms=5000,cwcwc_weight=1,settle_ms=0,event_min=0,event_max=0,answer_min=0,answer_max=0)
        browser = CaptureBrowser(self.page,args,Pacer(args,random.Random(42)),IncorrectSolver())
        state = {'task_id':13925458,'topic_id':3769,'kps':{},'examples':{},'questions':{}}
        topic = loads((FIXTURE/'database-before.edn').read_text())[0][0]
        with tempfile.TemporaryDirectory() as work:
            with self.assertRaisesRegex(ValueError,'expected Correct, received Incorrect'):
                browser.lesson(state,work,topic)
            self.assertEqual(self.page.locator('body').get_attribute('data-submissions'),'1')
            self.assertEqual(len(state['questions']),1)
            self.assertFalse(state.get('knowledge_snapshots'))


if __name__=='__main__':
    unittest.main()
