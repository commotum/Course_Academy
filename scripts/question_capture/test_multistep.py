"""Offline regressions from the manually completed six-part pool activity."""
import base64
import json
import random
import tempfile
import unittest
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import Mock, patch

from browser import CaptureBrowser
from capture import arguments, run
from core import Pacer, build_content_transaction, choose_activity
from solver import Solver

FIXTURES = Path(__file__).parent / 'fixtures'
POOL = json.loads((FIXTURES / 'multistep-pool.json').read_text())


class MultistepRunnerTests(unittest.TestCase):
    def test_queue_activity_is_automatically_taken_without_a_single_topic_lookup(self):
        activity = {'task_id':1,'task_type':'multistep','multistep_id':1780,'title':'Pool','topic_id':None,
                    'href':'/tasks/1/multisteps/1780','capture_supported':True}
        selected=[]
        class FixtureBrowser:
            def __init__(self,*args):pass
            def queue(self):return [activity] if not selected else []
            def start(self,a):selected.append(a)
            def activity(self,state,*args):state['activity_complete']=True
            def history(self,state,*args):return {'task_id':1,'task_type':'multistep','questions':[]}
        db=Mock();db.priorities.return_value={};db.import_content.return_value={'previewed':True}
        runtime=Mock();runtime.__enter__=Mock(return_value=runtime);runtime.__exit__=Mock(return_value=False)
        runtime.chromium.launch_persistent_context.return_value=SimpleNamespace(pages=[Mock()],close=Mock(),route=Mock())
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--preview','--state-dir',work+'/state','--output',work+'/captures'])
            with patch('capture.Database',return_value=db), patch('browser.CaptureBrowser',FixtureBrowser), \
                 patch('playwright.sync_api.sync_playwright',return_value=runtime), patch('builtins.print'):
                run(args)
            state=json.loads((args.output/'1/state.json').read_text())
            self.assertEqual(state['multistep_id'],1780)
            self.assertEqual(state['answer_policy'],'all_correct')
            self.assertTrue(state['preview_complete'])
            self.assertEqual(json.loads((args.output/'1/multistep-queue.json').read_text())['title'],'Pool')
            self.assertEqual(selected[0]['selection_reason'],'queue_fallback')
            db.topic.assert_not_called()
            db.import_content.assert_called_once()
            self.assertEqual(runtime.chromium.launch_persistent_context.call_args.kwargs['slow_mo'],500)


class MultistepTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.runtime = sync_playwright().start()
        cls.browser = cls.runtime.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.runtime.stop()

    def setUp(self):
        self.context = self.browser.new_context(offline=True)
        self.page = self.context.new_page()
        self.graded, self.submissions, self.current = set(), [], 0
        self.context.route('https://mathacademy.com/**', self.respond)

    def tearDown(self):
        self.context.close()

    def activity_html(self):
        body = '<div id="steps">' + POOL['context_html']
        for i, q in enumerate(POOL['questions']):
            body += ('<div id="step-' + str(i+2) + '" class="step" style="display:' +
                     ('block' if i <= self.current else 'none') + '">' + q['live_html'] + '</div>')
            body += '<div id="continueButton-' + str(i+2) + '" style="display:none">Continue</div>'
        body += '</div><div id="finalScreen" style="display:none">Congratulations! You\'ve completed the task. You\'ve been awarded all 10 XP, plus a bonus of 3 XP for answering every question correctly.<a id="finalScreen-doneButton" href="/learn">CONTINUE</a></div>'
        grades = {str(i):q['grade_html'] for i,q in enumerate(POOL['questions'])}
        body += '<script src="/vendor/jquery-3.7.1.min.js"></script><script src="/vendor/mathquill-ma.v2.1.min.js"></script><script>'
        body += 'const grades=' + json.dumps(grades) + ';const restored=' + json.dumps(sorted(self.graded)) + ';'
        body += '''const MQ=MathQuill.getInterface(2);
        document.querySelectorAll('.matheditor-wrapper-answer').forEach(n=>{const e=document.createElement('div');n.append(e);MQ.MathField(e,{handlers:{edit:()=>n.closest('.question').querySelector('.submitButton').classList.remove('disabledButton')}})});
        function grade(i,html){document.querySelector('#step-'+(i+2)+' [id$="explanationFrame"]').outerHTML=html;document.querySelector('#submitButton-'+(i+2)).style.display='none';document.querySelector('#continueButton-'+(i+2)).style.display='block'};
        restored.forEach(i=>{grade(i,grades[i]);document.querySelector('#continueButton-'+(i+2)).style.display=i===CURRENT?'block':'none'});
        document.querySelectorAll('.submitButton').forEach((b,i)=>b.onclick=()=>fetch('/fixture/grade/'+i).then(r=>r.text()).then(html=>grade(i,html)));
        document.querySelectorAll('[id^="continueButton-"]').forEach((b,i)=>b.onclick=()=>fetch('/fixture/next/'+i).then(()=>{b.style.display='none';const next=document.querySelector('#step-'+(i+3));if(next)next.style.display='block';else{document.querySelector('#steps').style.display='none';document.querySelector('#finalScreen').style.display='block'}}));
        '''.replace('CURRENT', str(self.current))
        return body + '</script><link rel="stylesheet" href="/vendor/mathquill-0.10.1.css">'

    def respond(self, route):
        url = route.request.url
        if '/graphics/' in url:
            a = POOL['assets'][url]
            route.fulfill(status=200, content_type=a['content_type'], body=base64.b64decode(a['bytes']))
            return
        if '/vendor/' in url:
            f = FIXTURES / 'vendor' / url.rsplit('/', 1)[1]
            route.fulfill(status=200 if f.exists() else 404,
                          content_type=('text/css' if f.suffix=='.css' else 'text/javascript') + '; charset=utf-8',
                          body=f.read_bytes() if f.exists() else b'')
            return
        if '/fixture/grade/' in url:
            i = int(url.rsplit('/',1)[1]); self.graded.add(i); self.submissions.append(i)
            body = POOL['questions'][i]['grade_html']
        elif '/fixture/next/' in url:
            self.current = int(url.rsplit('/',1)[1]) + 1; body = 'OK'
        elif '/multisteps/' in url:
            body = self.activity_html()
        elif '?taskId=' in url:
            body = ''.join(q['history_html'].replace('class="questionExplanation"', 'class="questionExplanation" style="display:none"') for q in POOL['questions'])
            body += '<script>document.querySelectorAll(".answerDetails").forEach(n=>n.onclick=()=>n.closest(".question").nextElementSibling.style.display="block")</script>'
        elif '/img/' in url:
            route.fulfill(status=404, body=''); return
        else:
            body = '<div id="incompleteTasks">' + POOL['card_html'] + '</div>'
        route.fulfill(status=200, content_type='text/html; charset=utf-8', body=body)

    def reader(self):
        args = arguments(['run','--event-min','0','--event-max','0','--answer-min','0','--answer-max','0','--settle-ms','0','--timeout-ms','5000'])
        questions = {q['math_academy_id']:q for q in POOL['questions']}
        class FixtureSolver:
            def solve(self, item, *unused):
                q = questions[item['dom_id'].replace('question-', 'q-')]
                answers = []
                for field, original in zip(item['fields'], q['answer_fields']):
                    value = original['correct_value']
                    if '\\sqrt' in value:
                        prefix, stem = value.split('\\sqrt{'); stem = stem[:-1]
                        keys = [{'text':prefix or None,'key':None}] if prefix else []
                        keys += [{'text':'\\sqrt','key':None},{'text':None,'key':'Space'}, {'text':stem,'key':None}]
                    elif '^2' in value:
                        prefix, rest = value.split('^2')
                        keys = [{'text':prefix+'^2','key':None},{'text':None,'key':'ArrowRight'},{'text':rest,'key':None}]
                    else:
                        keys = [{'text':value,'key':None}]
                    answers.append({'key':field['key'],'correct_option':None,'correct_value':value,'value_type':'math',
                                    'wrong_value':'0','correct_keys':keys,'wrong_keys':[{'text':'0','key':None}]})
                return {'confident':True,'explanation':'Fixture math solution','answers':answers}
        reader = CaptureBrowser(self.page, args, Pacer(args, random.Random(1)), FixtureSolver())
        reader.knowledge_snapshot = Mock(side_effect=lambda state,*args,**kw:state.setdefault('knowledge_snapshots',{}).update({'multistep-completed':{}}))
        return reader

    @staticmethod
    def state(activity):
        return {'task_id':activity['task_id'], 'task_type':'multistep','topic_id':None,
                'multistep_id':activity['multistep_id'],'title':activity['title'],
                'questions':{},'examples':{},'kps':{},'activity_url':'https://mathacademy.com'+activity['href']}

    @staticmethod
    def topic(tid,*unused):
        q = next(q for q in POOL['questions'] if q['topic_id'] == tid)
        return {':topic/math-academy-id':tid, ':topic/knowledge-points':[
            {':knowledge-point/title':q['knowledge_point'], ':knowledge-point/id':q['knowledge_point_id']}]}

    def test_full_capture_has_context_seven_fields_original_images_history_and_content_transaction(self):
        reader = self.reader(); activity, = reader.queue()
        self.assertTrue(activity['capture_supported'])
        self.assertEqual(activity['multistep_id'],1780)
        self.assertEqual(choose_activity([activity], {})['task_type'], 'multistep')
        state = self.state(activity)
        with tempfile.TemporaryDirectory() as work:
            directory = Path(work); reader.start(activity)
            reader.activity(state,directory,None)
            self.assertTrue(state['activity_complete'])
            self.assertEqual(self.submissions,list(range(6)))
            reader.knowledge_snapshot.assert_called_once()
            content = reader.history(state,directory,self.topic)
            self.assertEqual(content['question_order'], ['q-'+str(n) for n in range(167521,167527)])
            self.assertEqual(sum(len(q['answer_fields']) for q in content['questions']),7)
            self.assertTrue(all(q['difficulty'] and q['worked_solution'] and q['knowledge_point_id'] for q in content['questions']))
            last = content['questions'][-1]
            self.assertEqual(last['problem'],last['local_problem'])
            self.assertNotIn('Earlier part 5:',last['problem'])
            self.assertTrue(any('Lucy' in c['problem'] for c in content['shared_contexts']))
            # Solver-only expansion remains in attempt evidence, separate from
            # the source part stored in the reusable multistep.
            self.assertIn('Earlier part 5:',state['questions'][last['math_academy_id']]['before']['problem'])
            self.assertEqual(last['problem'].count('{{field-1}}'),1)
            self.assertIn('| ---',content['questions'][3]['worked_solution'])
            self.assertEqual(content['questions'][1]['answer_fields'][0]['type'],'blank')
            manifest = json.loads((directory/'assets/manifest.json').read_text())
            self.assertEqual(len(manifest),3)
            self.assertTrue(all(a['representation']=='original' for a in manifest.values()))
            tx, report = build_content_transaction(content, {q['topic_id']:self.topic(q['topic_id']) for q in content['questions']}, {})
            self.assertEqual(len(report),6)
            self.assertEqual(sum(':question/math-academy-id' in entry for entry in tx),6)
            self.assertFalse(any(any('learner' in str(k) or 'engine' in str(k) for k in entry) for entry in tx))
            context, _ = Solver.activity_context(directory, [])
            self.assertEqual(len(context['shared_contexts']),1)
            self.assertEqual(len(context['feedback']),6)
            reader.activity(state,directory,None)
            self.assertEqual(self.submissions,list(range(6)))

    def test_shared_context_waits_for_page_initialization_before_answering(self):
        original=self.activity_html
        def delayed_page():
            return original().replace('<div id="steps">','<div id="steps" style="display:none">',1)+(
                '<script>setTimeout(()=>document.getElementById("steps").style.display="block",500)</script>')
        self.activity_html=delayed_page
        reader=self.reader();activity,=reader.queue();state=self.state(activity)
        with tempfile.TemporaryDirectory() as work:
            reader.start(activity)
            self.assertFalse(self.page.locator('#steps > .step').first.is_visible())
            reader.activity(state,Path(work),None)
            self.assertTrue(state['activity_complete'])
            self.assertEqual(self.submissions,list(range(6)))
            self.assertEqual(len(state['shared_contexts']),1)
            self.assertTrue(state['shared_contexts'][0]['assets'])

    def test_resume_reuses_prepared_answer_after_solver_interruption(self):
        reader = self.reader(); activity, = reader.queue(); state=self.state(activity)
        with tempfile.TemporaryDirectory() as work:
            directory=Path(work); reader.start(activity)
            original=reader.enter
            def interrupted(scope,record):
                if record['sequence_position']==3:raise KeyboardInterrupt()
                return original(scope,record)
            reader.enter=interrupted
            with self.assertRaises(KeyboardInterrupt):reader.activity(state,directory,None)
            self.assertEqual(self.submissions,[0,1])
            restored=self.reader(); restored.solver.solve=Mock(wraps=restored.solver.solve)
            restored.navigate(state['activity_url'],force=True)
            restored.activity(state,directory,None)
            self.assertEqual(restored.solver.solve.call_count,3)
            self.assertEqual(self.submissions,list(range(6)))
            self.assertTrue(state['activity_complete'])

    def test_submission_interruption_reads_grade_without_submitting_again(self):
        reader = self.reader(); activity, = reader.queue(); state=self.state(activity)
        with tempfile.TemporaryDirectory() as work:
            directory=Path(work); reader.start(activity)
            original=reader.read
            def interrupted(scope,directory,stem):
                if stem=='q-167521-after':raise KeyboardInterrupt()
                return original(scope,directory,stem)
            reader.read=interrupted
            with self.assertRaises(KeyboardInterrupt):reader.activity(state,directory,None)
            self.assertEqual(state['questions']['q-167521']['status'],'submitting')
            self.assertEqual(self.submissions,[0])
            restored=self.reader(); restored.navigate(state['activity_url'],force=True)
            restored.activity(state,directory,None)
            self.assertEqual(self.submissions,list(range(6)))

    def test_lazy_multistep_card_expansion_does_not_toggle_closed_before_start(self):
        collapsed = '<div id="task-13931219" class="taskUnlocked" progress="0"><span class="taskTypeUnlocked">Multistep</span></div>'
        body = '<div id="incompleteTasks">' + collapsed + '</div><script>document.querySelector(".taskUnlocked").onclick=()=>document.querySelector("#incompleteTasks").innerHTML=' + json.dumps(POOL['card_html']) + '</script>'
        self.context.route('https://mathacademy.com/learn', lambda r:r.fulfill(status=200,content_type='text/html; charset=utf-8',body=body))
        reader=self.reader();activity,=reader.queue()
        self.assertTrue(activity['capture_supported'])
        reader.start(activity)
        self.assertIn('/multisteps/1780',self.page.url)

    def submit_poll_fixture(self, mode='enable'):
        evidence=json.loads((FIXTURES/'multistep-submit-poll.json').read_text())
        self.page.set_content('<div id="steps"><div id="step-2" class="step">'
            '<div id="question-167566" class="question"><span class="correctAnswerText">Correct</span></div>'
            '<div id="continueButton-2" style="display:none">Continue</div></div>'
            '<div id="step-3" class="step">'+evidence['question_html']+
            '<div id="continueButton-3" style="display:none">Continue</div></div></div>'
            '<div id="finalScreen" style="display:none">Congratulations! You have completed the task.'
            '<a id="finalScreen-doneButton" href="https://mathacademy.com/learn">Continue</a></div>')
        for script in ('jquery-3.7.1.min.js','mathquill-ma.v2.1.min.js','math-editor-ma.js'):
            self.page.add_script_tag(path=str(FIXTURES/'vendor'/script))
        self.page.add_style_tag(path=str(FIXTURES/'vendor/mathquill-0.10.1.css'))
        self.page.add_style_tag(content='.mathIcon {width:25px;height:25px;background:#ddd}')
        self.page.expose_function('record_submission',lambda:self.submissions.append('q-167567'))
        self.page.evaluate(r'''mode => {
          window.Core={getHeight:n=>n.getBoundingClientRect().height};
          window.submissions=0;
          const wrapper=document.querySelector('#question-167567 .matheditor-wrapper-answer');
          const editor=new MathEditor(wrapper,['infty']);
          // Keep the real editor's 500ms initial / 200ms repeating poll. Delay
          // its callback enough to reproduce the saved race deterministically.
          editor.onChange=response=>setTimeout(()=>{
            if(mode==='disabled') return;
            if(mode==='changed') editor.mathField.latex('0');
            document.getElementById('submitButton-3').className='submitButton enabledButton';
          },500);
          document.getElementById('submitButton-3').onclick=()=>{
            window.submissions++;
            window.record_submission();
            document.getElementById('question-167567').insertAdjacentHTML('beforeend',
              '<div class="correctAnswerText">Correct</div><div class="questionExplanation">'
              +'As sin(t) approaches zero, 2 / sin²(t) increases without bound.</div>');
            document.getElementById('submitButton-3').style.display='none';
            document.getElementById('continueButton-3').style.display='block';
          };
          document.getElementById('continueButton-3').onclick=()=>{
            document.getElementById('steps').style.display='none';
            document.getElementById('finalScreen').style.display='block';
          };
        }''',mode)
        reader=self.reader();reader.args.timeout_ms=1800
        reader.solver.solve=Mock(side_effect=AssertionError('Prepared answer must be reused'))
        return reader,evidence['state']

    def test_saved_infinity_waits_for_site_editor_poll_and_reuses_prior_grade(self):
        reader,state=self.submit_poll_fixture()
        with tempfile.TemporaryDirectory() as work:
            reader.activity(state,Path(work),None)
        self.assertTrue(state['activity_complete'])
        self.assertEqual(self.submissions,['q-167567'])
        q=state['questions']['q-167567']
        self.assertEqual(q['before']['fields'][0]['observed_mathquill_latex'],r'\infty')
        self.assertEqual(q['before']['fields'][0]['clicked_symbols'][0]['symbol'],'infty')
        self.assertEqual(q['status'],'graded')
        reader.solver.solve.assert_not_called()

    def test_disabled_multistep_still_stops_without_submission(self):
        reader,state=self.submit_poll_fixture('disabled')
        with tempfile.TemporaryDirectory() as work:
            with self.assertRaisesRegex(ValueError,'Multistep Submit is disabled'):
                reader.activity(state,Path(work),None)
        self.assertEqual(self.page.evaluate('window.submissions'),0)
        self.assertEqual(state['questions']['q-167567']['status'],'prepared')

    def test_multistep_rechecks_value_after_waiting_for_submit(self):
        reader,state=self.submit_poll_fixture('changed')
        with tempfile.TemporaryDirectory() as work:
            with self.assertRaisesRegex(ValueError,'Actual MathQuill value differs'):
                reader.activity(state,Path(work),None)
        self.assertEqual(self.page.evaluate('window.submissions'),0)
        self.assertEqual(state['questions']['q-167567']['status'],'prepared')


if __name__ == '__main__':
    unittest.main()
