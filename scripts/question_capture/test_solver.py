"""Session lifecycle and context checks without model calls or live activities."""
import json
import subprocess
import tempfile
import unittest
import uuid
import sys
import threading
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from core import atomic_json
from solver import Solver, run_cli, process_token


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory()
        self.root = Path(self.work.name)
        self.args = SimpleNamespace(solver_command=None,codex_bin='codex',solver_model=None,solver_timeout=5)
        self.calls = []

    def tearDown(self):
        self.work.cleanup()

    def question(self, number, option='a'):
        return {'dom_id':'step-q'+str(number),'problem':'Compute '+str(number)+'+1.',
                'fields':[{'key':'selection','type':'radio','choices':[
                    {'option':option,'type':'math','value':str(number+1)},
                    {'option':'z','type':'math','value':'0'}]}]}

    def fake_cli(self, command, **kwargs):
        payload = json.loads(kwargs['input'].rsplit('\n',1)[1])
        if 'resume' in command:
            sid = command[-2]
        else:
            sid = str(uuid.uuid4())
        self.calls.append({'command':command,'payload':payload,'sid':sid})
        choice = payload['fields'][0]['choices'][0]
        result = {'confident':True,'explanation':'Arithmetic checked.', 'answers':[
            {'key':'selection','correct_option':choice['option'],'correct_value':choice['value'],
             'value_type':choice['type'],'wrong_value':None,'correct_keys':[],'wrong_keys':[]}]}
        Path(command[command.index('--output-last-message')+1]).write_text(json.dumps(result))
        events = '\n'.join(json.dumps(e) for e in [{'type':'thread.started','thread_id':sid},
                                                {'type':'turn.completed'}])
        return subprocess.CompletedProcess(command,0,stdout=events,stderr='')

    def activity(self, name, task_type):
        root = self.root / name
        state = {'task_id':int(name),'task_type':task_type,'topic_id':10,'examples':{},'questions':{}}
        atomic_json(root/'state.json',state)
        return root,state

    def test_prompt_preserves_displayed_unicode_and_rejects_corrupted_choice(self):
        root,_=self.activity('100','lesson')
        item=self.question(1)
        choice=item['fields'][0]['choices'][0]
        choice['value']='{11}^{x}ln\u206111-\\frac{5}{x}'
        with patch('solver.run_cli',side_effect=self.fake_cli) as cli:
            result=Solver(self.args).solve(item,None,root/'q-1')
        prompt=cli.call_args.kwargs['input']
        self.assertIn('ln\u206111',prompt)
        self.assertNotIn(r'\u2061',prompt)
        result['answers'][0]['correct_value']=choice['value'].replace('\u2061','\x06')
        with self.assertRaisesRegex(ValueError,'exact displayed choice'):
            Solver.validate(item,result)

    def test_one_session_for_entire_activity_including_verification_and_restart(self):
        for kind in ('lesson','review'):
            root,state = self.activity('100' if kind=='lesson' else '200',kind)
            first, second = self.question(1),self.question(2,'b')
            state['examples']['e-10'] = {'math_academy_id':'e-10','knowledge_point':'Addition',
                                        'problem':'1+1','worked_solution':'1+1=2'}
            atomic_json(root/'state.json',state)
            (root/'example-10.png').write_bytes(b'fixture')
            with patch('solver.run_cli',side_effect=self.fake_cli):
                Solver(self.args).solve(first,None,root/'q-1')
                sid=self.calls[-1]['sid']
                self.assertNotIn('--ephemeral',self.calls[-1]['command'])
                self.assertNotIn('resume',self.calls[-1]['command'])
                self.assertEqual(self.calls[-1]['payload']['activity_context']['examples'][0]['math_academy_id'],'e-10')
                self.assertIn(str(root/'example-10.png'),self.calls[-1]['command'])
                state['questions']['q-1']={'intended':'W','actual_result':'Incorrect','before':first,
                                          'after':{**first,'worked_solution':'1+1=2'}}
                atomic_json(root/'state.json',state)
                # A new Python Solver object must continue the persisted activity.
                Solver(self.args).solve({**first,'worked_solution':'1+1=2'},None,root/'q-1','verify')
                self.assertIn('resume',self.calls[-1]['command'])
                self.assertEqual(self.calls[-1]['sid'],sid)
                feedback=self.calls[-1]['payload']['activity_context']['feedback']
                self.assertTrue(feedback[0]['deliberately_incorrect_submission'])
                state['current_kp'] = str(uuid.uuid4())
                state['examples']['e-20'] = {'math_academy_id':'e-20','knowledge_point':'Another KP',
                                            'problem':'2+1','worked_solution':'2+1=3'}
                atomic_json(root/'state.json',state)
                Solver(self.args).solve(second,None,root/'q-2')
                self.assertEqual(self.calls[-1]['sid'],sid)
                self.assertEqual(self.calls[-1]['payload']['fields'][0]['choices'][0]['option'],'b')
                self.assertEqual([e['math_academy_id'] for e in self.calls[-1]['payload']['activity_context']['examples']],['e-20'])
                self.assertNotIn(str(root/'example-10.png'),self.calls[-1]['command'])
                self.assertEqual(self.calls[-1]['payload']['activity_context']['feedback'],[])
                self.assertEqual(self.calls[-1]['command'][self.calls[-1]['command'].index('--sandbox')+1],'read-only')
                self.assertNotIn('--last',self.calls[-1]['command'])
        self.assertNotEqual(self.calls[0]['sid'],self.calls[3]['sid'])

    def test_correct_submission_explanation_is_passed_to_the_next_question(self):
        root,state=self.activity('100','lesson')
        first=self.question(1)
        with patch('solver.run_cli',side_effect=self.fake_cli):
            Solver(self.args).solve(first,None,root/'q-1')
            state['questions']['q-1']={'intended':'C','actual_result':'Correct','before':first,
                                      'after':{**first,'worked_solution':'1+1=2'}}
            atomic_json(root/'state.json',state)
            Solver(self.args).solve(self.question(2),None,root/'q-2')
        feedback=self.calls[-1]['payload']['activity_context']['feedback']
        self.assertEqual(feedback[0]['worked_solution'],'1+1=2')
        self.assertFalse(feedback[0]['deliberately_incorrect_submission'])

    def test_diagnostic_classification_skip_recovery_and_verification_share_activity_session(self):
        root,state=self.activity('100','diagnostic')
        policy={'course_id':54,'topics':[{'topic_id':3052,'title':'Joint Distributions'}]}
        item={**self.question(1),'diagnostic_policy':policy}
        def diagnostic_cli(command,**kwargs):
            response=self.fake_cli(command,**kwargs)
            schema=json.loads(Path(command[command.index('--output-schema')+1]).read_text())
            if self.calls[-1]['payload'].get('diagnostic_policy'):
                self.assertIn('diagnostic_topic_id',schema['required'])
                answer={'confident':True,'explanation':'Course topic','answers':[],
                        'diagnostic_classification':'in_course','diagnostic_topic_id':3052}
                Path(command[command.index('--output-last-message')+1]).write_text(json.dumps(answer))
            else:
                self.assertNotIn('diagnostic_topic_id',schema['properties'])
            return response
        def interrupted(command,**kwargs):
            response=diagnostic_cli(command,**kwargs)
            raise subprocess.CalledProcessError(1,command,output=response.stdout)
        with patch('solver.run_cli',side_effect=interrupted),self.assertRaises(subprocess.CalledProcessError):
            Solver(self.args).solve(item,None,root/'question-001','diagnostic')
        sid=self.calls[-1]['sid']
        with patch('solver.run_cli') as cli:
            answer=Solver(self.args).solve(item,None,root/'question-001','diagnostic')
            cli.assert_not_called()
            self.assertEqual(answer['answers'],[])
        state['questions']['question-001']={'intended':'skip','actual_result':'Skipped Question',
                                          'before':self.question(1),'after':{**self.question(1),'worked_solution':'2'}}
        atomic_json(root/'state.json',state)
        with patch('solver.run_cli',side_effect=diagnostic_cli):
            Solver(self.args).solve(self.question(2),None,root/'question-002')
            Solver(self.args).solve({**self.question(1),'worked_solution':'2'},None,root/'question-001','verify')
        self.assertTrue(all(c['sid']==sid for c in self.calls))
        self.assertFalse(json.loads((root/'solver-session/state.json').read_text()).get('pending_turn'))

    def test_completed_answer_recovers_after_cli_exit_before_checkpoint(self):
        root,state=self.activity('100','lesson')
        state['examples']['e-10']={'math_academy_id':'e-10','problem':'1+1','worked_solution':'2'}
        atomic_json(root/'state.json',state)
        def interrupted(command,**kwargs):
            result=self.fake_cli(command,**kwargs)
            raise subprocess.CalledProcessError(1,command,output=result.stdout,stderr='Interrupted after completion')
        with patch('solver.run_cli',side_effect=interrupted):
            with self.assertRaises(subprocess.CalledProcessError):
                Solver(self.args).solve(self.question(1),None,root/'q-1')
        with patch('solver.run_cli') as cli:
            answer=Solver(self.args).solve(self.question(1,'b'),None,root/'q-1')
            cli.assert_not_called()
        self.assertEqual(answer['answers'][0]['correct_option'],'b')
        checkpoint=json.loads((root/'solver-session/state.json').read_text())
        self.assertFalse(checkpoint.get('pending_turn'))
        self.assertIn('example:e-10',checkpoint['context_keys'])

    def test_completed_answer_is_reused_without_another_solver_turn(self):
        root,_=self.activity('100','lesson')
        with patch('solver.run_cli',side_effect=self.fake_cli) as cli:
            Solver(self.args).solve(self.question(1),None,root/'q-1')
            answer=Solver(self.args).solve(self.question(1,'b'),None,root/'q-1')
            self.assertEqual(cli.call_count,1)
        self.assertEqual(answer['answers'][0]['correct_option'],'b')

    def test_completed_event_answer_recovers_when_output_file_is_missing(self):
        root,_=self.activity('100','lesson')
        def interrupted(command,**kwargs):
            result=self.fake_cli(command,**kwargs)
            output=Path(command[command.index('--output-last-message')+1])
            answer=output.read_text();output.unlink()
            lines=result.stdout.splitlines()
            lines.insert(-1,json.dumps({'type':'item.completed','item':{'type':'agent_message','text':answer}}))
            raise subprocess.CalledProcessError(1,command,output='\n'.join(lines)+'\n')
        with patch('solver.run_cli',side_effect=interrupted),self.assertRaises(subprocess.CalledProcessError):
            Solver(self.args).solve(self.question(1),None,root/'q-1')
        with patch('solver.run_cli') as cli:
            answer=Solver(self.args).solve(self.question(1),None,root/'q-1')
            cli.assert_not_called()
        self.assertTrue(answer['confident'])
        checkpoint=json.loads((root/'solver-session/state.json').read_text())
        self.assertFalse(checkpoint.get('pending_turn'))

    def test_incomplete_event_message_is_not_used_as_completed_answer(self):
        path=self.root/'missing.json'
        message=json.dumps({'type':'item.completed','item':{'type':'agent_message','text':'{"confident":true}'}})
        self.assertIsNone(Solver.turn_answer(path,message))

    def test_completed_turn_without_answer_repeats_prompt_in_same_session(self):
        root,_=self.activity('100','lesson')
        def interrupted(command,**kwargs):
            result=self.fake_cli(command,**kwargs)
            Path(command[command.index('--output-last-message')+1]).unlink()
            raise subprocess.CalledProcessError(1,command,output=result.stdout)
        with patch('solver.run_cli',side_effect=interrupted),self.assertRaises(subprocess.CalledProcessError):
            Solver(self.args).solve(self.question(1),None,root/'q-1')
        sid=self.calls[-1]['sid']
        with patch('solver.run_cli',side_effect=self.fake_cli) as cli:
            answer=Solver(self.args).solve(self.question(1),None,root/'q-1')
            self.assertEqual(cli.call_count,1)
        self.assertTrue(answer['confident'])
        self.assertEqual(self.calls[-1]['sid'],sid)

    def test_capacity_retry_reuses_confirmed_session_and_is_bounded(self):
        root,_=self.activity('100','lesson')
        sid=str(uuid.uuid4())
        events='\n'.join(json.dumps(e) for e in [
            {'type':'thread.started','thread_id':sid},
            {'type':'error','message':'Selected model is at capacity. Please try a different model.'}])
        def fail(command,**kwargs):
            raise subprocess.CalledProcessError(1,command,output=events)
        count=0
        def recover(command,**kwargs):
            nonlocal count
            count+=1
            if count==1:return fail(command,**kwargs)
            return self.fake_cli(command,**kwargs)
        with patch('solver.run_cli',side_effect=recover),patch('solver.time.sleep'):
            Solver(self.args).solve(self.question(1),None,root/'q-1')
        self.assertEqual(count,2)
        self.assertEqual(self.calls[-1]['sid'],sid)
        root,_=self.activity('200','review')
        with patch('solver.run_cli',side_effect=fail) as cli,patch('solver.time.sleep'):
            with self.assertRaises(subprocess.CalledProcessError):
                Solver(self.args).solve(self.question(2),None,root/'q-2')
        self.assertEqual(cli.call_count,3)

    def test_other_cli_failure_is_not_retried(self):
        root,_=self.activity('100','lesson')
        with patch('solver.run_cli',side_effect=subprocess.CalledProcessError(1,'codex',output='auth required')) as cli:
            with self.assertRaises(subprocess.CalledProcessError):
                Solver(self.args).solve(self.question(1),None,root/'q-1')
        self.assertEqual(cli.call_count,1)

    def test_full_displayed_asset_rechecks_uncertainty_once_in_same_session(self):
        root,_=self.activity('100','lesson')
        item=self.question(1);asset=root/'assets/diagram.png'
        asset.parent.mkdir();asset.write_bytes(b'fixture')
        item['problem']+=' ![]('+str(asset)+')'
        with patch('solver.run_cli',side_effect=self.fake_cli):
            Solver(self.args).solve(item,None,root/'q-1')
        sid=self.calls[-1]['sid'];answer=root/'q-1/solve-answer.json'
        saved=json.loads(answer.read_text());saved['confident']=False;atomic_json(answer,saved)
        item['assets']=[{'path':str(asset)}]
        with patch('solver.run_cli',side_effect=self.fake_cli) as cli:
            Solver(self.args).solve(item,None,root/'q-1')
            self.assertEqual(cli.call_count,1)
        self.assertEqual(self.calls[-1]['sid'],sid)
        self.assertIn(str(asset),self.calls[-1]['command'])
        self.assertTrue((root/'q-1/solve-before-full-images-answer.json').exists())

    def test_real_cli_timeout_preserves_streamed_events_and_stops_process(self):
        events,errors=self.root/'events.jsonl',self.root/'errors.txt'
        sid=str(uuid.uuid4());started=[]
        command=[sys.executable,'-c', 'import json,time;print(json.dumps('+repr({'type':'thread.started','thread_id':sid})+'),flush=True);time.sleep(30)']
        with self.assertRaises(subprocess.TimeoutExpired):
            run_cli(command,input='',timeout=.3,events_path=events,diagnostics_path=errors,started=started.append)
        self.assertEqual(Solver.event_session_id(events.read_text()),sid)
        self.assertIsNone(process_token(started[0]))

    def test_headless_repair_stop_request_terminates_child_group_promptly(self):
        events,errors=self.root/'repair-events.jsonl',self.root/'repair-errors.txt'
        stop=threading.Event();started=[]
        timer=threading.Timer(.2,stop.set);timer.start()
        try:
            with self.assertRaises(KeyboardInterrupt):
                run_cli([sys.executable,'-c','import time;time.sleep(30)'],input='',timeout=30,
                        events_path=events,diagnostics_path=errors,started=started.append,stop_event=stop)
        finally:timer.cancel()
        self.assertIsNone(process_token(started[0]))

    def test_timeout_repeats_solver_prompt_in_same_session_without_website_submission(self):
        root,_=self.activity('100','review')
        sid=str(uuid.uuid4())
        error=subprocess.TimeoutExpired('codex',5,output=(json.dumps({'type':'thread.started','thread_id':sid})+'\n').encode())
        with patch('solver.run_cli',side_effect=error) as process:
            with self.assertRaises(subprocess.TimeoutExpired):
                Solver(self.args).solve(self.question(1),None,root/'q-1')
            state=json.loads((root/'solver-session/state.json').read_text())
            self.assertEqual(state['session_id'],sid)
            self.assertTrue(state['pending_turn'])
        with patch('solver.run_cli',side_effect=self.fake_cli):
            Solver(self.args).solve(self.question(1),None,root/'q-1')
        self.assertEqual(self.calls[-1]['sid'],sid)
        self.assertIn('resume',self.calls[-1]['command'])
        self.assertFalse(json.loads((root/'solver-session/state.json').read_text()).get('pending_turn'))

    def test_resume_rejects_a_different_session_instead_of_silently_resetting_context(self):
        root,_=self.activity('100','review')
        with patch('solver.run_cli',side_effect=self.fake_cli):
            Solver(self.args).solve(self.question(1),None,root/'q-1')
        sid=json.loads((root/'solver-session/state.json').read_text())['session_id']
        def wrong_session(command,**kwargs):
            result=self.fake_cli(command,**kwargs)
            result.stdout=json.dumps({'type':'thread.started','thread_id':str(uuid.uuid4())})+'\n'+json.dumps({'type':'turn.completed'})
            return result
        with patch('solver.run_cli',side_effect=wrong_session):
            with self.assertRaisesRegex(ValueError,'expected activity session'):
                Solver(self.args).solve(self.question(2),None,root/'q-2')
        state=json.loads((root/'solver-session/state.json').read_text())
        self.assertEqual(state['session_id'],sid)
        self.assertTrue(state['pending_turn'])

    def test_partial_output_without_completed_turn_is_not_used(self):
        root,_=self.activity('100','review')
        def incomplete(command,**kwargs):
            result=self.fake_cli(command,**kwargs)
            result.stdout=result.stdout.splitlines()[0]
            return result
        with patch('solver.run_cli',side_effect=incomplete):
            with self.assertRaisesRegex(ValueError,'did not complete'):
                Solver(self.args).solve(self.question(1),None,root/'q-1')
        self.assertTrue(json.loads((root/'solver-session/state.json').read_text())['pending_turn'])

    def test_shared_context_cannot_return_an_old_choice_for_a_new_question(self):
        root,_=self.activity('100','lesson')
        with patch('solver.run_cli',side_effect=self.fake_cli):
            first=Solver(self.args).solve(self.question(1),None,root/'q-1')
        def stale_answer(command,**kwargs):
            result=self.fake_cli(command,**kwargs)
            Path(command[command.index('--output-last-message')+1]).write_text(json.dumps(first))
            return result
        with patch('solver.run_cli',side_effect=stale_answer):
            with self.assertRaisesRegex(ValueError,'exact displayed choice'):
                Solver(self.args).solve(self.question(2,'b'),None,root/'q-2')

    def test_session_identity_is_bound_to_its_activity_and_new_screenshots_are_attached(self):
        root,state=self.activity('100','review')
        image=self.root/'question.png';image.write_bytes(b'fixture')
        with patch('solver.run_cli',side_effect=self.fake_cli) as process:
            Solver(self.args).solve(self.question(1),image,root/'q-1')
            self.assertEqual(self.calls[-1]['command'][self.calls[-1]['command'].index('--image')+1],str(image.resolve()))
            state['task_id']=999
            atomic_json(root/'state.json',state)
            with self.assertRaisesRegex(ValueError,'another activity'):
                Solver(self.args).solve(self.question(2),image,root/'q-2')
            self.assertEqual(process.call_count,1)


if __name__ == '__main__':
    unittest.main()
