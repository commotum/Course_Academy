"""Regression coverage for continuing batches and repair when progress stalls."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from capture import arguments, main, queued_resume, run, unfinished_run
from capture_repair import RestartWorker, failure_key
from core import atomic_json


class AdaptiveRunTests(unittest.TestCase):
    def fixture(self, work, tasks, failures=()):
        page = Mock()
        page.url = 'https://mathacademy.com/learn'
        page.content.return_value = '<body>saved local evidence</body>'
        selected = []
        queue = [{'task_id':i, 'topic_id':i, 'task_type':'lesson', 'title':str(i),
                  'href':'/tasks/%s/topics/%s/lesson' % (i,i)} for i in tasks]
        class Browser:
            def __init__(self,*_):
                self.page = page
                self.http_block = None
            def queue(self): return queue
            def current_step(self): return None
            def navigate(self,*_,**__): pass
            def start(self,activity): selected.append(activity['task_id'])
            def activity(self,state,*_):
                if state['task_id'] in failures: raise ValueError('Fixture capture failure')
                state['activity_complete'] = True
            def history(self,state,directory,*_):
                state['history_complete'] = True
                content = {'task_id':state['task_id']}
                atomic_json(directory/'content.json',content)
                return content
        context = SimpleNamespace(pages=[page],close=Mock(),route=Mock())
        runtime = Mock()
        runtime.__enter__ = Mock(return_value=runtime)
        runtime.__exit__ = Mock(return_value=False)
        runtime.chromium.launch_persistent_context.return_value = context
        db = Mock()
        db.priorities.return_value = {}
        db.topic.return_value = {}
        return Browser,runtime,db,selected

    def execute(self,args,fixture):
        browser,runtime,db,selected = fixture
        with patch('capture.Database',return_value=db), patch('browser.CaptureBrowser',browser), \
             patch('playwright.sync_api.sync_playwright',return_value=runtime), \
             patch('saved_imports.sweep',return_value=[]), \
             patch('saved_imports.complete'), \
             patch('import_repair.import_with_repair',return_value={'previewed':True}), \
             patch('capture_repair.cooldown') as cooldown, \
             contextlib.redirect_stdout(io.StringIO()):
            run(args)
        return selected,cooldown

    def test_completed_resume_does_not_override_maintenance_checkpoint(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            complete = root/'capture/1'
            atomic_json(complete/'state.json',{'task_id':1,'topic_id':1,'task_type':'lesson',
                         'activity_complete':True,'history_complete':True})
            atomic_json(complete/'content.json',{'task_id':1})
            atomic_json(root/'batch.json',{'attempted':0,'limit':1,'next_resume':None})
            args = arguments(['run','--state-dir',str(root/'state'),'--output',str(root/'capture'),
                 '--resume',str(complete),'--batch-checkpoint',str(root/'batch.json'),
                 '--limit','1','--no-capture-repair'])
            with patch('saved_imports.eligible',return_value=True) as shortcut:
                selected,_ = self.execute(args,self.fixture(work,[2]))
            self.assertEqual(selected,[2])
            shortcut.assert_not_called()

    def test_completed_explicit_resume_continues_without_limit(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            complete = root/'capture/1'
            atomic_json(complete/'state.json',{'task_id':1,'topic_id':1,'task_type':'lesson',
                         'activity_complete':True,'history_complete':True})
            atomic_json(complete/'content.json',{'task_id':1})
            args = arguments(['run','--state-dir',str(root/'state'),'--output',str(root/'capture'),
                 '--resume',str(complete),'--rest-every','0','--lesson-min','0','--lesson-max','0'])
            # Fixture retains completed tasks in queue; after task 2 capture,
            # an empty queue represents the service exhausting available work.
            fixture = self.fixture(work,[2])
            browser = fixture[0]
            count = [0]
            def queue(_):
                count[0] += 1
                return [{'task_id':2,'topic_id':2,'task_type':'lesson','title':'2',
                         'href':'/tasks/2/topics/2/lesson'}] if count[0] == 1 else []
            browser.queue = queue
            with patch('saved_imports.eligible',return_value=True):
                selected,_ = self.execute(args,fixture)
            self.assertEqual(selected,[2])
            self.assertIsNone(args.resume)

    def test_two_capture_failures_trigger_early_repair_then_fresh_task(self):
        with tempfile.TemporaryDirectory() as work:
            args = arguments(['run','--state-dir',work+'/state','--output',work+'/capture',
                 '--limit','3','--lesson-min','0','--lesson-max','0'])
            selected,cooldown = self.execute(args,self.fixture(work,[1,2,3],failures={1,2}))
            self.assertEqual(selected,[1,2,3])
            cooldown.assert_called_once()
            self.assertEqual(cooldown.call_args.kwargs,{'pause':False})
            self.assertEqual(cooldown.call_args.args[2]['attempted'],2)

    def test_three_fresh_lessons_progress_before_saved_recovery(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            for task in (1,2):
                atomic_json(root/'capture'/str(task)/'state.json',{
                    'task_id':task,'topic_id':task,'task_type':'lesson',
                    'lesson_url':'https://mathacademy.com/tasks/%s/topics/%s/lesson' % (task,task),
                    'deferred_error':{'phase':'activity','message':'Saved interrupted lesson'}})
            args = arguments(['run','--state-dir',str(root/'state'),'--output',str(root/'capture'),
                 '--limit','4','--lesson-min','0','--lesson-max','0'])
            fixture = self.fixture(work,[1,2,3,4,5])
            calls = []
            original = fixture[0].activity
            def activity(browser,state,*params):
                calls.append(state['task_id'])
                return original(browser,state,*params)
            fixture[0].activity = activity
            selected,cooldown = self.execute(args,fixture)
            self.assertEqual(selected,[3,4,5])
            self.assertEqual(calls,[3,4,5,1])
            cooldown.assert_not_called()

    def test_queue_failure_does_not_exhaust_three_attempt_gate(self):
        with tempfile.TemporaryDirectory() as work:
            args = arguments(['run','--state-dir',work+'/state','--output',work+'/capture',
                 '--limit','5','--lesson-min','0','--lesson-max','0'])
            fixture = self.fixture(work,[5])
            original = fixture[0].queue
            calls = [0]
            def queue(browser):
                calls[0] += 1
                if calls[0] <= 4:
                    raise ValueError('Temporary queue layout failure')
                return original(browser)
            fixture[0].queue = queue
            with patch('capture.Pacer.backoff'):
                selected,cooldown = self.execute(args,fixture)
            self.assertEqual(selected,[5])
            self.assertEqual(cooldown.call_count,4)

    def test_queued_recovery_is_bounded_and_respects_current_agent_decision(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            args = arguments(['run','--state-dir',str(root/'state'),'--output',str(root/'capture')])
            directory = root/'capture/1'
            diagnostic = directory/'diagnostics/1'
            report = {'phase':'activity','exception_type':'ValueError','message':'Fixture ambiguity'}
            atomic_json(diagnostic/'error.json',report)
            atomic_json(directory/'state.json',{'task_id':1,'task_type':'lesson',
                'deferred_error':{'diagnostics':str(diagnostic)},'questions':{'q-1':{'status':'submitting'}}})
            queue = [{'task_id':1,'in_progress':True}]
            self.assertEqual(queued_resume(args,queue,set()),directory.resolve())
            self.assertIsNone(queued_resume(args,queue,{1}))
            atomic_json(root/'state/capture-repair/failures.json',{
                failure_key(report):{'status':'blocked','source_version':'generation'}})
            with patch('capture_repair.source_version',return_value='generation'):
                self.assertIsNone(queued_resume(args,queue,set()))
            with patch('capture_repair.source_version',return_value='repaired-generation'):
                self.assertEqual(queued_resume(args,queue,set()),directory.resolve())

    def test_multiple_ordinary_interrupted_captures_do_not_require_user_selection(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            for task in (1,2):
                atomic_json(root/str(task)/'state.json',{'task_id':task,'task_type':'lesson'})
            args = arguments(['run','--output',work])
            self.assertIn(unfinished_run(args),[root/'1',root/'2'])

    def test_maintenance_exec_removes_completed_resume_argument(self):
        with tempfile.TemporaryDirectory() as work:
            checkpoint = Path(work)/'next.json'
            argv = ['run','--headless','--state-dir',work,'--resume',work+'/old',
                    '--batch-checkpoint='+work+'/previous.json']
            with patch('capture.run',side_effect=RestartWorker(checkpoint)), \
                 patch('capture.os.execv') as execute:
                self.assertEqual(main(argv),0)
            command = execute.call_args.args[1]
            self.assertNotIn('--resume',command)
            self.assertNotIn(work+'/old',command)
            self.assertIn('--headless',command)
            self.assertEqual(command[-2:],['--batch-checkpoint',str(checkpoint)])


if __name__ == '__main__': unittest.main()
