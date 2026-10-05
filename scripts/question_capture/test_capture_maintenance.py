"""Cooldown scheduling, isolated patches, session reuse and batch restart checks."""
import contextlib
import fcntl
import io
import json
import random
import subprocess
import sys
import tempfile
import threading
import unittest
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch

from capture import arguments,idle_capture_repair,main,run
from capture_repair import RestartWorker,cooldown,next_failure,prepare,run_tests,safe_resume,tuple_tree
from core import Pacer,atomic_json

class CaptureMaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.args=arguments(['run','--state-dir',str(self.root/'state'),'--output',str(self.root/'captures')])
        self.pacer=Pacer(self.args,random.Random(1),sleeper=lambda seconds:None)
        self.sid=str(uuid.uuid4());self.commands=[]
        self.result={'status':'blocked','summary':'Missing source evidence.','file':'','edits':[],'regression_test':''}
    def tearDown(self):self.temp.cleanup()
    def test_excluded_only_queue_runs_early_repair_without_consuming_attempt(self):
        self.failure()
        fake=Mock();fake.rng=random.Random(1)
        with patch('capture_repair.cooldown') as repair:
            idle_capture_repair(self.args,fake,[{'task_id':1}],7,{10},{1})
        self.assertEqual(repair.call_args.args[2],{'attempted':7,'limit':None,
                         'completed_topics':[10],'captured_tasks':[1]})
        with patch('capture_repair.cooldown') as repair:
            idle_capture_repair(self.args,fake,[],7,set(),set())
            self.args.limit=7
            idle_capture_repair(self.args,fake,[{'task_id':1}],7,set(),set())
            repair.assert_not_called()

    def test_runner_reaches_early_repair_for_deferred_only_queue(self):
        directory,_=self.failure()
        atomic_json(directory/'state.json',{'task_id':1,'task_type':'lesson','topic_id':10,
            'questions':{},'deferred_error':{'phase':'activity','message':'Unknown visible widget'}})
        self.args.limit=2
        class Browser:
            def __init__(self,*args):pass
            def queue(self):return [{'task_id':1,'topic_id':10,'task_type':'lesson','title':'Deferred',
                                     'href':'/tasks/1/topics/10/lesson','in_progress':True}]
        db=Mock();db.priorities.return_value={}
        runtime=Mock();runtime.__enter__=Mock(return_value=runtime);runtime.__exit__=Mock(return_value=False)
        context=SimpleNamespace(pages=[Mock()],close=Mock(),route=Mock())
        runtime.chromium.launch_persistent_context.return_value=context
        with patch('capture.Database',return_value=db),patch('browser.CaptureBrowser',Browser), \
             patch('playwright.sync_api.sync_playwright',return_value=runtime), \
             patch('capture_repair.cooldown',side_effect=RestartWorker(self.root/'batch.json')) as repair:
            with self.assertRaises(RestartWorker):run(self.args)
        self.assertEqual(repair.call_args.args[2]['attempted'],0)
        context.close.assert_called_once()
    def test_complete_suite_has_a_separate_configurable_timeout(self):
        self.assertEqual(self.args.capture_repair_test_timeout,1800)
        custom=arguments(['run','--capture-repair-test-timeout','2400'])
        self.assertEqual(custom.capture_repair_test_timeout,2400)
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):
            arguments(['run','--capture-repair-test-timeout','0'])
        timeouts=[]
        def validate(command,**kwargs):
            timeouts.append(kwargs['timeout'])
            kwargs['events_path'].write_text('')
            kwargs['diagnostics_path'].write_text('OK')
            self.assertIs(kwargs['stop_event'],self.args.stop_event)
            return subprocess.CompletedProcess(command,0,stdout='',stderr='OK')
        self.args.stop_event=Mock()
        with patch('capture_repair.run_cli',side_effect=validate):
            self.assertEqual(run_tests(self.root,'discover',self.root/'suite.txt',self.args),(0,'OK'))
            self.args.capture_repair_test_timeout=2400
            run_tests(self.root,'discover',self.root/'custom.txt',self.args)
            run_tests(self.root,'targeted_regression',self.root/'targeted.txt',self.args)
        self.assertEqual(timeouts,[1800,2400,300])
    def failure(self,task=1,phase='activity',kind='ValueError'):
        d=self.args.output/str(task);(d/'diagnostics/1').mkdir(parents=True)
        atomic_json(d/'state.json',{'task_id':task,'task_type':'lesson','questions':{}})
        p=d/'diagnostics/1/error.json';atomic_json(p,{'phase':phase,'exception_type':kind,'message':'Unknown visible widget '+str(task)})
        return d,p
    def cli(self,command,**kwargs):
        self.commands.append(command);kwargs['started'](123456789)
        Path(command[command.index('--output-last-message')+1]).write_text(json.dumps(self.result))
        events='\n'.join(json.dumps(e) for e in ({'type':'thread.started','thread_id':self.sid},{'type':'turn.completed'}))
        kwargs['events_path'].write_text(events)
        return subprocess.CompletedProcess(command,0,stdout=events,stderr='')
    def test_no_failures_and_import_or_auth_errors_do_not_launch_capture_session(self):
        self.failure(1,'import');self.failure(2,kind='AccessBlocked');self.failure(3,kind='KeyboardInterrupt')
        with patch('capture_repair.run_cli') as cli:
            self.assertIsNone(prepare(self.args,self.pacer));cli.assert_not_called()
    def test_new_failures_reuse_dedicated_session_and_blocked_diagnosis_is_not_repeated(self):
        d,p=self.failure()
        with patch('capture_repair.run_cli',side_effect=self.cli) as cli:
            self.assertIsNone(prepare(self.args,self.pacer))
            self.assertIsNone(prepare(self.args,self.pacer));self.assertEqual(cli.call_count,1)
            self.failure(2)
            self.assertIsNone(prepare(self.args,self.pacer))
        self.assertNotIn('resume',self.commands[0]);self.assertIn('resume',self.commands[1])
        self.assertEqual(self.commands[1][-2],self.sid)
        self.assertTrue(all(c[c.index('--sandbox')+1]=='read-only' for c in self.commands))
    def test_cooldown_credits_repair_time_and_keeps_batch_and_rng(self):
        fake=Mock();fake.rng=random.Random(7)
        self.args.rest_min=self.args.rest_max=240
        plan={'diagnostic':str(self.failure()[1])}
        with patch('capture_repair.prepare',return_value=plan),patch('capture_repair.apply') as apply, \
             patch('capture_repair.time.monotonic',side_effect=[100,175]):
            with self.assertRaises(RestartWorker) as restart:
                cooldown(self.args,fake,{'attempted':20,'limit':60,'captured_tasks':[1],'completed_topics':[10]})
        fake.wait.assert_called_once_with('rest','periodic cooldown',elapsed=75)
        apply.assert_called_once_with(plan)
        saved=json.loads(restart.exception.checkpoint.read_text())
        self.assertEqual(saved['attempted'],20);self.assertEqual(saved['limit'],60)
        self.assertEqual(saved['next_resume'],str((self.args.output/'1').resolve()))
        restored=random.Random();restored.setstate(tuple_tree(saved['rng_state']))
        self.assertEqual(restored.random(),fake.rng.random())
    def test_unsafe_submissions_and_active_quizzes_are_never_scheduled_for_resume(self):
        d,p=self.failure();plan={'diagnostic':str(p)}
        for change in ({'questions':{'q-1':{'status':'submitting'}}},
                       {'pending_continue':{'source_step':'q-1'}},
                       {'task_type':'assessment'},{'test_submission_status':'confirming'}):
            atomic_json(d/'state.json',{'task_type':'lesson','questions':{},**change})
            self.assertIsNone(safe_resume(plan))
    def test_failed_regression_never_applies_live_source(self):
        self.failure();self.result={'status':'repair','summary':'Targeted fix.','file':'browser.py',
            'edits':[{'old':'never matches','new':'new'}],'regression_test':'import unittest'}
        with patch('capture_repair.run_cli',side_effect=self.cli), \
             patch('capture_repair.run_tests',return_value=(0,'OK')),patch('capture_repair.apply') as apply:
            with self.assertRaisesRegex(ValueError,'must fail by assertion'):prepare(self.args,self.pacer)
            apply.assert_not_called()

    def test_suite_timeout_or_failure_never_produces_applicable_patch(self):
        for task,outcome in enumerate((subprocess.TimeoutExpired('offline-suite',1800),(1,'FAIL: unrelated regression')),1):
            with self.subTest(outcome=outcome):
                self.failure(task);self.result={'status':'repair','summary':'Targeted fix.','file':'math_notation.py',
                    'edits':[{'old':'without algebra.','new':'without guessing algebra.'}],
                    'regression_test':'import unittest\nclass Regression(unittest.TestCase):\n def test_bug(self): self.fail("observed bug")\n'}
                source=Path(__file__).parent/'math_notation.py';original=source.read_bytes()
                with patch('capture_repair.run_cli',side_effect=self.cli), \
                     patch('capture_repair.run_tests',side_effect=[(1,'FAIL: observed bug'),outcome]):
                    with self.assertRaises((ValueError,subprocess.TimeoutExpired)):
                        prepare(self.args,self.pacer)
                self.assertEqual(source.read_bytes(),original)
                (self.args.state_dir/'capture-repair/failures.json').unlink(missing_ok=True)

    def test_offline_suite_shutdown_is_interruptible(self):
        stage=self.root/'stage';package=stage/'scripts/question_capture';package.mkdir(parents=True)
        (package/'test_wait.py').write_text('import time,unittest\nclass Waiting(unittest.TestCase):\n def test_wait(self): time.sleep(60)\n')
        self.args.stop_event=threading.Event()
        timer=threading.Timer(.1,self.args.stop_event.set);timer.start()
        try:
            with self.assertRaises(KeyboardInterrupt):
                run_tests(stage,'discover',self.root/'stop.txt',self.args)
        finally:timer.cancel();timer.join()

    def test_tested_candidate_retains_requested_source_file_after_fixture_copy(self):
        self.failure()
        self.result={'status':'repair','summary':'Targeted fix.','file':'math_notation.py',
                     'edits':[{'old':'without algebra.','new':'without symbolic algebra.'}],
                     'regression_test':'import unittest'}
        with patch('capture_repair.run_cli',side_effect=self.cli), \
             patch('capture_repair.run_tests',side_effect=[(1,'FAIL: observed bug'),(0,'OK')]) as tests:
            plan=prepare(self.args,self.pacer)
        self.assertEqual(plan['file'],'math_notation.py')
        self.assertIn('without symbolic algebra.',plan['candidate'])
        self.assertEqual(tests.call_args_list[1].args[1],'discover')
    def test_main_releases_lock_before_exec_and_preserves_original_cli_options(self):
        argv=['run','--limit','60','--seed','7','--state-dir',str(self.args.state_dir)]
        target=self.root/'batch.json'
        def execv(executable,command):
            with (self.args.state_dir/'capture.lock').open('a') as handle:
                fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
            self.assertEqual(command[2:2+len(argv)],argv)
            self.assertEqual(command[-2:],['--batch-checkpoint',str(target)])
        with patch('capture.run',side_effect=RestartWorker(target)),patch('capture.os.execv',side_effect=execv) as execute:
            self.assertEqual(main(argv),0);execute.assert_called_once()

    def test_real_exec_loads_batch_checkpoint_without_resetting_limit_or_opening_browser(self):
        checkpoint=self.root/'finished.json';atomic_json(checkpoint,{'attempted':20,'limit':20})
        script='''import sys
from unittest.mock import patch
from capture import main
from capture_repair import RestartWorker
with patch('capture.run',side_effect=RestartWorker(sys.argv[2])):
 raise SystemExit(main(['run','--limit','20','--headless','--state-dir',sys.argv[1],'--output',sys.argv[3]]))
'''
        result=subprocess.run([sys.executable,'-c',script,str(self.args.state_dir),str(checkpoint),str(self.args.output)],
                              cwd=Path(__file__).parent,capture_output=True,text=True,timeout=15)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('reached the activity limit',result.stderr)
        self.assertFalse((self.args.state_dir/'browser-profile').exists())
        with (self.args.state_dir/'capture.lock').open('a') as handle:
            fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
    def test_restarted_batch_keeps_remaining_limit_and_next_break_count(self):
        self.restarted_batch(22)

    def test_unlimited_default_survives_restart_and_runs_until_queue_exhausted(self):
        self.assertIsNone(arguments(['run']).limit)
        self.restarted_batch(None)

    def restarted_batch(self,limit):
        attempted=[];maintenance=[]
        checkpoint=self.root/'batch.json'
        atomic_json(checkpoint,{'attempted':19,'limit':limit,'completed_topics':[], 'captured_tasks':[],
                              'rng_state':random.Random(8).getstate(),'next_resume':None})
        limit_args=[] if limit is None else ['--limit',str(limit)]
        args=arguments(['run',*limit_args,'--preview','--state-dir',str(self.args.state_dir),
                        '--output',str(self.args.output),'--batch-checkpoint',str(checkpoint),
                        '--lesson-min','0','--lesson-max','0'])
        class Browser:
            def __init__(self,*args):pass
            def queue(self):
                return [{'task_id':i,'topic_id':i,'task_type':'lesson','title':'Lesson','href':'/tasks/'+str(i)+'/topics/'+str(i)+'/lesson'}
                        for i in range(1,5) if i not in attempted]
            def start(self,item):attempted.append(item['task_id'])
            def activity(self,state,*args):state['activity_complete']=True
            def history(self,state,*args):return {'task_id':state['task_id']}
        db=Mock();db.priorities.return_value={};db.topic.return_value={};db.import_content.return_value={'previewed':True}
        runtime=Mock();runtime.__enter__=Mock(return_value=runtime);runtime.__exit__=Mock(return_value=False)
        runtime.chromium.launch_persistent_context.return_value=SimpleNamespace(pages=[Mock()],close=Mock(),route=Mock())
        with patch('capture.Database',return_value=db),patch('browser.CaptureBrowser',Browser), \
             patch('playwright.sync_api.sync_playwright',return_value=runtime), \
             patch('capture_repair.cooldown',side_effect=lambda args,pacer,batch:maintenance.append(batch)), \
             contextlib.redirect_stdout(io.StringIO()):run(args)
        self.assertEqual(attempted,[1,2,3,4] if limit is None else [1,2,3])
        self.assertEqual(len(maintenance),1);self.assertEqual(maintenance[0]['attempted'],20)
        self.assertEqual(maintenance[0]['limit'],limit)

if __name__=='__main__':unittest.main()
