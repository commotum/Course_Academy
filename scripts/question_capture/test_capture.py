"""Regression checks using actual Sum Rule DOM and EDB capture fixtures."""
import copy
import json
import random
import tempfile
import unittest
import uuid
from pathlib import Path
from types import SimpleNamespace

from browser import EXTRACT, CaptureBrowser, kp_for_example
from core import ROOT, ALLOWED, Pacer, build_transaction, choose_lesson, choose_sequence, normalize
from database import Database
from edn import dumps, loads, kw
from solver import Solver
from progress import changes, normalize_course

FIXTURE = ROOT/'reference/mathacademy/sum-rule-13925458'


class PolicyTests(unittest.TestCase):
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

    def test_normalization_preserves_fraction_grouping(self):
        self.assertEqual(normalize(r'\frac{{x}^{3}}{3}'),normalize(r'\frac{x^{3}}{3}'))
        self.assertNotEqual(normalize(r'\frac{1}{23}'),normalize(r'\frac{12}{3}'))


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
        cls.page = cls.context.new_page()

    @classmethod
    def tearDownClass(cls):
        cls.context.close()
        cls.browser.close()
        cls.runtime.stop()

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

    def test_svg_duplicate_title_ids_are_scoped_locally(self):
        self.page.set_content('<span class="mjpage"><svg><title id="same">x+1</title></svg></span><div id="test"><div class="exampleQuestion"><span class="mjpage"><svg><title id="same">x^2+1</title></svg></span></div><div class="exampleExplanation">solution</div></div>')
        item = self.page.locator('#test').evaluate(EXTRACT)
        self.assertEqual(item['problem'],'$x^2+1$')

    def test_mixed_native_fields_keep_field_locations_and_choice_values(self):
        self.page.set_content('<div id="test"><div class="questionWidget-text">x=<input id="blank" type="text">; sign=<select id="select"><option disabled value="">Choose</option><option value="plus">+</option><option value="minus">−</option></select></div></div>')
        item = self.page.locator('#test').evaluate(EXTRACT)
        self.assertFalse(item['errors'])
        self.assertEqual([f['type'] for f in item['fields']],['blank','select'])
        self.assertIn('{{field-1}}',item['problem'])
        self.assertIn('{{field-2}}',item['problem'])
        self.assertEqual([c['option'] for c in item['fields'][1]['choices']],['plus','minus'])

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
            document.getElementById('step-'+token).querySelector('.questionWidget-submitButton').classList.remove('disabledButton');}
          if(n.classList.contains('questionWidget-submitButton')){const token=order[position],number=token.slice(1);
            const node=document.getElementById('step-'+token);node.outerHTML=after[number];
            document.getElementById('step-'+token).querySelector('.questionWidget-result').textContent=selected[token]===correct[number]?'Correct':'Incorrect';
            if(!document.getElementById('continueButton-'+token)){const b=document.createElement('button');b.id='continueButton-'+token;b.textContent='Continue';document.getElementById('step-'+token).append(b);}
            document.body.dataset.submissions=String(Number(document.body.dataset.submissions||0)+1);}
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
        def respond(route):
            nonlocal submitted_count
            url = route.request.url
            if '/courses/' in url:
                course = int(url.split('/courses/')[1].split('/')[0])
                submissions = int(self.page.locator('body').get_attribute('data-submissions') or 0)
                submitted_count = max(submitted_count, submissions)
                body = progress[course]
                if course == 111 and submitted_count:
                    body += '''<script>document.querySelector('.topicLink[href="/topics/3769?courseId=111"]').closest('tr').querySelector('.topicCircle').style.background='rgb(165, 207, 243)';</script>'''
            else:
                body = lesson if '/lesson' in url else activity if '?taskId=' in url else '<div id="incompleteTasks"></div>'
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
            self.assertEqual(len(state['knowledge_snapshots']),20)  # baseline, 18 steps, completion
            snapshots = [json.loads((Path(work)/s['path']).read_text()) for s in state['knowledge_snapshots'].values()]
            self.assertTrue(all(sum(len(c['topics']) for c in s['courses'])==1040 for s in snapshots))
            first_question = next(s for s in snapshots if s['event'].startswith('after-q'))
            self.assertEqual([(d['topic_id'],d['before_band'],d['after_band']) for d in first_question['changes']],[(3769,0,2)])
            self.assertEqual(snapshots[-1]['changes'],[])
            # Durable snapshots are reused when restoring the same event, without refreshing history.
            before_count = len(state['knowledge_snapshots'])
            browser.knowledge_snapshot(state,work,first_question['event'])
            self.assertEqual(len(state['knowledge_snapshots']),before_count)
            self.assertEqual(self.page.url,'https://mathacademy.com/learn?taskId=13925458')
            existing = {r[0][':question/math-academy-id']:r[0] for r in loads((FIXTURE/'id-matches.edn').read_text())}
            transaction,_ = build_transaction(content,topic,existing)
            self.assertTrue(transaction)

    def test_snapshot_failure_resumes_without_resubmitting_answer(self):
        correct = self.lesson_fixture()
        args = SimpleNamespace(timeout_ms=5000,cwcwc_weight=0.7,settle_ms=0,event_min=0,event_max=0,answer_min=0,answer_max=0)
        browser = CaptureBrowser(self.page,args,Pacer(args,random.Random(42)),self.fixture_solver(correct))
        state = {'task_id':13925458,'topic_id':3769,'kps':{},'examples':{},'questions':{}}
        topic = loads((FIXTURE/'database-before.edn').read_text())[0][0]
        original = browser.knowledge_snapshot
        def fail_once(state,directory,event,**kwargs):
            if event == 'after-q71168': raise RuntimeError('Simulated snapshot interruption')
            return original(state,directory,event,**kwargs)
        browser.knowledge_snapshot = fail_once
        with tempfile.TemporaryDirectory() as work:
            with self.assertRaisesRegex(RuntimeError,'Simulated snapshot interruption'):
                browser.lesson(state,work,topic)
            self.assertEqual(self.page.locator('body').get_attribute('data-submissions'),'1')
            self.assertEqual(state['pending_knowledge_snapshot']['event'],'after-q71168')
            browser.knowledge_snapshot = original
            browser.lesson(state,work,topic)
            saved = json.loads((Path(work)/'knowledge-state/after-q71168.json').read_text())
            self.assertTrue(saved['recovered_after_interruption'])
            self.assertTrue(state['lesson_complete'])
            self.assertEqual(len(state['questions']),15)
            self.assertNotIn('pending_knowledge_snapshot',state)

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
            self.assertIn('unexpected-grade-q71168',state['knowledge_snapshots'])


if __name__=='__main__':
    unittest.main()
