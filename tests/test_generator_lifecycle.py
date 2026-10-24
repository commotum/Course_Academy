"""Real process lifecycle and exact controlled-stop credits; no database work."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from generator_lifecycle import (OWNER_ENV, INTERRUPTED_EXIT, ControlledServiceStop,
    begin_launch, credit_interruption, create_owner, finish_launch, mark_stopped, read)
from generator_pipeline import CodexSession, SessionRetryExhausted
from inventory_jobs import InventoryJobs, save


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.job = self.root / 'jobs/job.json'
        self.job.parent.mkdir()
        self.owner = create_owner(self.job, 1)
        self.pipeline = self.job.with_suffix('.pipeline') / '1'
        self.directory = self.pipeline / 'author-1'
        self.directory.mkdir()
        self.execution_path = self.directory / 'execution.json'
        self.processes = []

    def tearDown(self):
        for process in self.processes:
            if process.poll() is None:
                process.kill()
            process.wait()
        self.temp.cleanup()

    def spawn(self):
        process = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'])
        self.processes.append(process)
        return process

    def launch(self, launches=3):
        return begin_launch(self.execution_path, {'launches': launches, 'status': 'running'},
                            {OWNER_ENV: str(self.owner)}, self.spawn)[0]

    def test_exact_interrupted_launch_gets_one_replacement_not_fresh_budget(self):
        execution = self.launch()
        marker = mark_stopped(self.owner)
        self.assertEqual(len(marker['sessions']), 1)
        self.assertEqual(read(self.execution_path), execution, 'Shutdown must not rewrite execution')
        credited = credit_interruption(self.execution_path, execution, 3)
        self.assertEqual((credited['launches'], credited['launch_limit']), (3, 4))
        self.assertEqual(credit_interruption(self.execution_path, credited, 3), credited)
        # Two genuine failures plus one interruption leave exactly one launch.
        next_owner = create_owner(self.job, 1)
        failed, _ = begin_launch(self.execution_path,
            {**credited, 'launches': 4, 'status': 'running'}, {OWNER_ENV: str(next_owner)}, self.spawn)
        failed.update(status='failed', error='genuine failure')
        finish_launch(self.execution_path, failed)
        mark_stopped(next_owner)
        self.assertEqual(credit_interruption(self.execution_path, failed, 3), failed)
        session = CodexSession(root=ROOT)
        with self.assertRaises(SessionRetryExhausted):
            session('author', {'workspace': str(self.directory)}, self.directory)

    def test_unmarked_or_changed_execution_is_not_credited(self):
        execution = self.launch()
        self.assertEqual(credit_interruption(self.execution_path, execution, 3), execution)
        mark_stopped(self.owner)
        changed = {**execution, 'launches': 4}
        self.assertEqual(credit_interruption(self.execution_path, changed, 3), changed)
        failed = {**execution, 'status': 'failed'}
        self.assertEqual(credit_interruption(self.execution_path, failed, 3), failed)

    def test_real_session_finishes_with_the_single_controlled_replacement(self):
        self.launch()
        mark_stopped(self.owner)
        self.processes[-1].kill(); self.processes[-1].wait()
        executable = self.root / 'fake-codex'
        executable.write_text('#!' + sys.executable + '\n'
            'import json,sys\nfrom pathlib import Path\n'
            'sys.stdin.read()\n'
            'path=Path(sys.argv[sys.argv.index("--output-last-message")+1])\n'
            'path.write_text(json.dumps({"status":"ready","manifest":"package.json"}))\n')
        executable.chmod(0o755)
        next_owner = create_owner(self.job, 1)
        session = CodexSession(root=ROOT, environment={OWNER_ENV: str(next_owner),
                               'COURSE_ACADEMY_CODEX_EXECUTABLE': str(executable)})
        self.assertEqual(session('author', {'workspace': str(self.directory)}, self.directory)['status'], 'ready')
        result = read(self.execution_path)
        self.assertEqual((result['launches'], result['launch_limit'], result['status']), (4, 4, 'completed'))
        self.assertEqual(len(result['controlled_interruptions']), 1)

    def test_exited_agent_with_stale_running_status_is_not_marked(self):
        execution = self.launch()
        self.processes[-1].kill(); self.processes[-1].wait()
        self.assertEqual(mark_stopped(self.owner)['sessions'], [])
        self.assertEqual(credit_interruption(self.execution_path, execution, 3), execution)

    def test_completed_result_wins_over_marker(self):
        execution = self.launch()
        mark_stopped(self.owner)
        expected = {'status': 'ready', 'manifest': 'package.json'}
        save(self.directory / 'result.json', expected)
        self.assertEqual(credit_interruption(self.execution_path, execution, 3), execution)
        with patch('generator_pipeline.subprocess.Popen') as spawn:
            result = CodexSession(root=ROOT)('author', {'workspace': str(self.directory)}, self.directory)
        self.assertEqual(result, expected)
        spawn.assert_not_called()

    def test_partial_result_does_not_hide_an_interrupted_launch(self):
        execution = self.launch()
        (self.directory / 'result.json').write_text('{"status":')
        self.assertEqual(len(mark_stopped(self.owner)['sessions']), 1)
        self.assertEqual(credit_interruption(self.execution_path, execution, 3)['launch_limit'], 4)

    def test_stopped_owner_prevents_actual_agent_spawn_without_spending_launch(self):
        mark_stopped(self.owner)
        with patch('generator_pipeline.subprocess.Popen') as spawn:
            session = CodexSession(root=ROOT, environment={OWNER_ENV: str(self.owner)})
            with self.assertRaises(ControlledServiceStop):
                session('author', {'workspace': str(self.directory)}, self.directory)
        spawn.assert_not_called()
        self.assertFalse(self.execution_path.exists())

    def test_agent_spawn_and_stop_share_critical_section(self):
        spawning, release, marked = threading.Event(), threading.Event(), threading.Event()
        failures = []
        def spawn():
            spawning.set()
            self.assertTrue(release.wait(3))
            return self.spawn()
        def launch():
            try:
                begin_launch(self.execution_path, {'launches': 1, 'status': 'running'},
                             {OWNER_ENV: str(self.owner)}, spawn)
            except BaseException as error: failures.append(error)
        def stop():
            mark_stopped(self.owner); marked.set()
        worker = threading.Thread(target=launch); worker.start()
        self.assertTrue(spawning.wait(3))
        stopper = threading.Thread(target=stop); stopper.start()
        self.assertFalse(marked.wait(.05), 'Stop must wait until spawn identity is durable')
        release.set(); worker.join(3); stopper.join(3)
        self.assertEqual(failures, [])
        self.assertTrue(marked.is_set())
        self.assertEqual(len(read(self.owner / 'stopped.json')['sessions']), 1)

    def test_inventory_marks_only_owned_live_pipeline(self):
        execution = self.launch()
        jobs = InventoryJobs(self.root, self.job.parent, 'learner')
        unrelated = create_owner(self.job, 1)
        jobs._active_owners.add(self.owner)
        markers = jobs.mark_service_interruption()
        self.assertEqual(len(markers), 1)
        self.assertFalse((unrelated / 'stopped.json').exists())
        self.assertEqual(credit_interruption(self.execution_path, execution, 3)['launch_limit'], 4)

    def test_pipeline_stop_prevents_actual_spawn_and_preserves_publication_intent(self):
        jobs = InventoryJobs(self.root, self.job.parent, 'learner')
        publication = self.pipeline / 'publication/request.json'
        save(publication, {'request_id': 'already-reviewed-intent'})
        jobs.mark_service_interruption()
        with patch('inventory_jobs.subprocess.Popen') as spawn:
            result = jobs._run_pipeline(['unused'], env={OWNER_ENV: str(self.owner)}, timeout=10, check=False)
        spawn.assert_not_called()
        self.assertEqual(result.returncode, INTERRUPTED_EXIT)
        self.assertEqual(read(publication), {'request_id': 'already-reviewed-intent'})

    def test_pipeline_spawn_stop_lock_released_during_wait(self):
        jobs = InventoryJobs(self.root, self.job.parent, 'learner')
        entered, release, marked = threading.Event(), threading.Event(), threading.Event()
        class Process:
            def wait(self, timeout=None): entered.set(); release.wait(3); return 0
            def kill(self): pass
        result = []
        with patch('inventory_jobs.subprocess.Popen', return_value=Process()):
            worker = threading.Thread(target=lambda: result.append(jobs._run_pipeline(
                ['unused'], env={OWNER_ENV: str(self.owner)}, timeout=10, check=False)))
            worker.start(); self.assertTrue(entered.wait(3))
            stopper = threading.Thread(target=lambda: (jobs.mark_service_interruption(), marked.set()))
            stopper.start(); self.assertTrue(marked.wait(3))
            release.set(); worker.join(3); stopper.join(3)
        self.assertEqual(result[0].returncode, 0)
        self.assertFalse(jobs._active_owners)

    def test_controlled_outer_exit_preserves_prior_process_failures(self):
        jobs = InventoryJobs(self.root, self.job.parent, 'learner')
        save(self.job, {'key': 'job', 'cycle': 1, 'state': 'pending', 'attempts': 1,
                       'processFailures': 2, 'retryAt': 0,
                       'request': {'knowledgePoint': 1, 'topic': 2, 'jobKind': 'build'}})
        def interrupted(command, **kwargs):
            mark_stopped(kwargs['env'][OWNER_ENV])
            return subprocess.CompletedProcess(command, INTERRUPTED_EXIT)
        with patch.object(jobs, '_run_pipeline', side_effect=interrupted):
            self.assertTrue(jobs.run_one())
        self.assertEqual((read(self.job)['state'], read(self.job)['processFailures']), ('pending', 2))
        with patch.object(jobs, '_run_pipeline', return_value=subprocess.CompletedProcess([], 1)):
            self.assertTrue(jobs.run_one())
        self.assertEqual((read(self.job)['state'], read(self.job)['processFailures']), ('blocked', 3))


if __name__ == '__main__':
    unittest.main()
