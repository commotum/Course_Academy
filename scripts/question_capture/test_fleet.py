"""Account isolation, launcher ownership and checkpoint shutdown, without MA requests."""
import contextlib
import io
import json
import os
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import fleet
from core import atomic_json


class FleetTests(unittest.TestCase):
    def setUp(self):
        self.work=tempfile.TemporaryDirectory()
        self.root=Path(self.work.name)
        raw=json.loads(fleet.CONFIG.read_text())
        for worker in raw['workers']:
            worker['state_dir']=str(self.root/worker['id']/'state')
            worker['output']=str(self.root/worker['id']/'captures')
        source=self.root/'workers.json';atomic_json(source,raw)
        self.data=fleet.config(source)
        self.worker=self.data['workers'][2]

    def tearDown(self):
        self.work.cleanup()

    def configure(self, worker=None):
        worker=worker or self.worker
        cookies=worker['profile']/'Default/Cookies'
        cookies.parent.mkdir(parents=True,exist_ok=True);cookies.touch()
        atomic_json(worker['auth_file'],{'username':'test-user','course_name':worker['course'],'course_id':54})

    def test_default_layout_keeps_original_paths_and_has_four_courses(self):
        data=fleet.config()
        self.assertEqual([w['window'] for w in data['workers']],
                         ['Mathematical Foundations','Linear Algebra','Multivariable Calculus','Differential Equations'])
        self.assertEqual(data['workers'][0]['state_dir'],fleet.ROOT/'.local/question_capture')
        self.assertEqual(data['workers'][0]['output'],fleet.ROOT/'reference/mathacademy/question-capture')
        self.assertEqual(len({w['profile'] for w in data['workers']}),4)
        self.assertTrue(all(Path(w['topics']).is_file() for w in data['workers']))

    def test_commands_use_saved_account_and_all_capture_roots_without_recopied_cookies(self):
        from capture import arguments
        self.configure()
        command=fleet.worker_command(self.data,self.worker,dry_run=True,limit=2)
        args=arguments(command[3:])
        self.assertEqual(args.profile,self.worker['profile'])
        self.assertEqual(args.output,self.worker['output'])
        self.assertEqual(args.state_dir,self.worker['state_dir'])
        self.assertEqual(args.progress_mode,'sidebar')
        self.assertIsNone(args.progress_urls)
        self.assertEqual(args.diagnostic_course_id,54)
        self.assertEqual(set(args.capture_root),{w['output'] for w in self.data['workers']})
        self.assertIsNone(args.browser_spec)
        self.assertTrue(args.headless and args.dry_run)
        self.assertEqual(args.limit,2)
        args=arguments(fleet.worker_command(self.data,self.data['workers'][0])[3:])
        self.assertEqual(args.progress_mode,'sidebar')

    def test_account_locks_are_independent(self):
        with fleet.file_lock(self.worker['state_dir']/'capture.lock'):
            self.assertTrue(fleet.capture_running(self.worker))
            self.assertFalse(fleet.capture_running(self.data['workers'][0]))
        self.assertFalse(fleet.capture_running(self.worker))

    def test_hidden_account_menu_is_read_as_text_not_visibility(self):
        page=Mock();user=Mock();course=Mock()
        user.text_content.return_value=' multiwilliam '
        course.text_content.return_value=' Multivariable Calculus '
        course.get_attribute.return_value='/courses/54/progress'
        page.locator.side_effect=lambda selector:user if selector=='#userMenu-username' else Mock(first=course)
        self.assertEqual(fleet.profile_identity(page),
                         {'username':'multiwilliam','course_name':'Multivariable Calculus','course_id':54})
        user.inner_text.assert_not_called()

    def test_start_skips_active_unconfigured_and_busy_windows(self):
        for worker in self.data['workers']:self.configure(worker)
        self.data['workers'][1]['auth_file'].unlink()
        windows={w['window']:str(i) for i,w in enumerate(self.data['workers'])}
        def tmux(*args,**kwargs):
            if args[0]=='list-panes':
                command='vim' if args[2]=='3' else 'bash'
                return Mock(stdout='%9\t\t'+command+'\t0\n')
            return Mock(stdout='')
        with patch('fleet.FLEET_DIR',self.root/'fleet'),patch('fleet.ensure_layout',return_value=windows), \
             patch('fleet.capture_running',side_effect=lambda w:w['id']=='foundations'), \
             patch('fleet.supervisor_running',return_value=False),patch('fleet.tmux',side_effect=tmux) as calls, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            fleet.start(self.data,self.data['workers'],dry_run=True)
        starts=[c for c in calls.call_args_list if c.args[0]=='respawn-pane']
        self.assertEqual(len(starts),1)
        self.assertIn('worker multivariable --dry-run',starts[0].args[-1])
        self.assertIn('foundations: already running',output.getvalue())
        self.assertIn('linear: not configured',output.getvalue())
        self.assertIn('differential: window is busy',output.getvalue())

    def test_real_supervisor_signal_allows_owned_child_to_checkpoint(self):
        ready=self.root/'child-ready';checkpoint=self.root/'checkpoint'
        code=('import signal,time,pathlib,sys\n'
              'def finish(*args):\n'
              f' pathlib.Path({str(checkpoint)!r}).write_text("saved")\n'
              ' print("checkpoint saved",flush=True)\n'
              ' sys.exit(0)\n'
              'signal.signal(signal.SIGTERM,finish)\n'
              f'pathlib.Path({str(ready)!r}).touch()\n'
              'while True: time.sleep(.01)\n')
        def request_stop():
            deadline=time.monotonic()+5
            while not ready.exists() and time.monotonic()<deadline:time.sleep(.01)
            os.kill(os.getpid(),signal.SIGTERM)
        old_handler=signal.getsignal(signal.SIGTERM)
        timer=threading.Thread(target=request_stop)
        with patch('fleet.worker_command',return_value=[sys.executable,'-u','-c',code]), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            timer.start()
            result=fleet.run_worker(self.data,self.worker)
            timer.join()
        saved=fleet.read_json(self.worker['supervision']/'fleet-worker.json')
        self.assertEqual(result,0)
        self.assertEqual(checkpoint.read_text(),'saved')
        self.assertIn('checkpoint saved',output.getvalue())
        self.assertEqual(saved['exit_code'],0)
        self.assertIsNone(fleet.process_token(saved['worker_pid']))
        self.assertEqual(signal.getsignal(signal.SIGTERM),old_handler)
        with fleet.file_lock(self.worker['supervision']/'fleet-supervisor.lock'):pass

    def test_status_reads_checkpoint_and_fits_an_eighty_column_display(self):
        self.configure()
        atomic_json(self.worker['output']/'123/state.json',
                    {'task_id':123,'task_type':'lesson','questions':{'1':{'actual_result':'incorrect'},'2':{}}})
        row=fleet.worker_status(self.worker)
        self.assertEqual(row['status'],'READY')
        self.assertEqual(row['activity'],'lesson 123')
        self.assertEqual(row['questions'],'1/2 graded')
        with patch('fleet.shutil.get_terminal_size',return_value=os.terminal_size((80,24))):
            text=fleet.render([fleet.worker_status(w) for w in self.data['workers']])
        self.assertTrue(all(len(line)<=80 for line in text.splitlines()))
        self.assertIn('Linear Algebra',text)
        self.assertIn('Differential Equations',text)
        self.assertIn('1 ready / 2 unset',fleet.render([row,*[fleet.worker_status(w) for w in self.data['workers'][1::2]]],compact=True))

    def test_status_does_not_display_yesterdays_xp_as_today(self):
        self.configure()
        atomic_json(self.worker['state_dir']/'dashboard.json',
                    {'percent_complete':70,'daily_xp':{'date':'2026-10-07','earned':237,'base':388}})
        with patch('dashboard.local_date',return_value='2026-10-08'):
            row=fleet.worker_status(self.worker)
        self.assertEqual(row['daily_xp'],{})
        self.assertEqual(row['percent_complete'],70)

    def test_finished_diagnostic_distinguishes_pending_import_from_completion(self):
        self.configure()
        path=self.worker['output']/'123/state.json'
        state={'task_id':123,'task_type':'diagnostic','activity_complete':True,'history_complete':True,
               'questions':{'1':{'actual_result':'Incorrect','finalized':True}},
               'deferred_error':{'phase':'import','message':'Field identity mismatch'}}
        atomic_json(path,state)
        self.assertEqual(fleet.worker_status(self.worker)['status'],'IMPORT PENDING')
        self.assertEqual(fleet.worker_status(self.worker)['recent'],'Field identity mismatch')
        with patch('fleet.capture_running',return_value=True):
            row=fleet.worker_status(self.worker)
            self.assertEqual(row['status'],'RUNNING')
            self.assertNotIn('deferred',row['activity'])
        state.pop('deferred_error');state['import_complete']=True
        atomic_json(path,state)
        self.assertEqual(fleet.worker_status(self.worker)['status'],'COMPLETE')
        state.pop('history_complete');state.pop('import_complete')
        state['deferred_error']={'phase':'history','message':'Unrecognized source grade'}
        atomic_json(path,state)
        self.assertEqual(fleet.worker_status(self.worker)['status'],'HISTORY PENDING')

    def test_shared_repair_install_waits_for_current_install(self):
        import coordination
        entered=self.root/'installed'
        code=(f'import sys;sys.path.insert(0,{str(fleet.PACKAGE)!r})\n'
              f'import coordination;from pathlib import Path;coordination.ROOT=Path({str(self.root)!r})\n'
              f'with coordination.source_install_lock(): Path({str(entered)!r}).touch()\n')
        process=None
        try:
            with patch('coordination.ROOT',self.root),coordination.source_install_lock():
                process=subprocess.Popen([sys.executable,'-c',code])
                time.sleep(.2)
                self.assertIsNone(process.poll())
                self.assertFalse(entered.exists())
            self.assertEqual(process.wait(timeout=5),0)
            self.assertTrue(entered.exists())
        finally:
            if process and process.poll() is None:process.kill();process.wait()


if __name__=='__main__':unittest.main()
