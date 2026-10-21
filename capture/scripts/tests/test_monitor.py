from datetime import datetime
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.config import Config
from scripts.monitor import process_running, render, snapshot
from scripts.outbox import target_id
from scripts.storage import append_event, atomic_json


class MonitorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = Config(repo_root=self.root, account='linear', profile=self.root / 'profile')

    def save(self, name, value):
        atomic_json(self.config.state_root / name, value)

    def test_snapshot_combines_active_stage_daily_counts_and_only_this_accounts_pending_imports(self):
        now = datetime.now().timestamp()
        today = datetime.now().astimezone().date().isoformat()
        directory = self.config.output_root / '123'
        self.save('active.json', {'activity': {'task_id': '123', 'kind': 'lesson', 'title': 'Eigenvectors'},
                                  'directory': str(directory)})
        self.save('status.json', {'status': 'capturing', 'at': now})
        self.save('worker.json', {'pid': 99, 'started_at': now - 20})
        self.save('daily-xp.json', {today: {'earned_xp': 45, 'unknown_tasks': 1}})
        self.save('completed.json', {'1': {'capture_completed_at': now}, '2': {'capture_completed_at': 0}})
        atomic_json(directory / 'checkpoint.json', {'stage': 'history'})
        for key, changes in [('pending', {}), ('other-account', {'account': 'differential'}),
                             ('done', {'status': 'verified'}), ('capture-only', {'capture_only': True}),
                             ('other-db', {'target_id': 'different-target'})]:
            atomic_json(self.config.spool_root / (key + '.json'), {
                'account': 'linear', 'status': 'pending', 'target_id': target_id(self.config),
                'error': {'type': 'TimeoutError', 'message': 'writer unavailable'}, **changes})
        row = snapshot(self.config, running=True)
        self.assertEqual((row['task_id'], row['kind'], row['title']), ('123', 'lesson', 'Eigenvectors'))
        self.assertEqual(row['stage'], 'Reviewing history')
        self.assertEqual((row['today_xp'], row['today_completed'], row['pending_imports']), (45, 1, 1))
        self.assertEqual(row['status'], 'RUNNING')
        self.assertIn('Import: TimeoutError: writer unavailable', row['errors'])

    def test_missing_or_corrupt_state_is_read_only_and_not_reported_running(self):
        row = snapshot(self.config)
        self.assertFalse(self.config.state_root.exists())
        self.assertEqual(row['status'], 'STOPPED')
        self.assertIsNone(row['today_xp'])
        self.config.state_root.mkdir(parents=True)
        path = self.config.state_root / 'status.json'
        path.write_text('{broken')
        row = snapshot(self.config)
        self.assertIn('Cannot read status.json', row['errors'])
        self.assertEqual(path.read_text(), '{broken')
        self.assertEqual(list(self.config.state_root.iterdir()), [path])

    def test_orphan_capture_is_running_with_missing_supervisor_reported(self):
        pid = os.getpid()
        token = Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()[19]
        self.save('worker.json', {'pid': pid, 'process_token': 'expired',
                                 'child_pid': pid, 'child_token': token})
        row = snapshot(self.config)
        self.assertTrue(row['running'])
        self.assertIn('Supervisor exited; capture process is still running', row['errors'])
        self.save('worker.json', {'pid': pid, 'process_token': 'expired',
                                 'child_pid': pid, 'child_token': 'expired'})
        self.assertFalse(snapshot(self.config)['running'])

    def test_original_course_code_stays_with_account_after_course_switch(self):
        self.save('current-course.json', {'course_id': '113', 'course_name': 'Mathematical Foundations I'})
        row = snapshot(self.config, running=True, details=False)
        self.assertEqual(row['original_course_code'], 'LAL')
        self.assertEqual(row['label'], 'Mathematical Foundations I')
        self.config.account = 'foundations'
        self.assertEqual(snapshot(self.config, running=True, details=False)['original_course_code'], 'MF3')

    def test_verified_omissions_are_visible_separately_from_pending_imports(self):
        atomic_json(self.config.spool_root/'partial.json', {'account':'linear', 'target_id':target_id(self.config),
            'status':'verified','result':{'omissions':[{'id':'q-1','reason':'Unavailable source'}]}})
        atomic_json(self.config.spool_root/'pending.json', {'account':'linear', 'target_id':target_id(self.config),
            'status':'pending','result':{'reason':'Readback failed'}})
        row=snapshot(self.config)
        self.assertEqual(row['captures_with_omissions'],1)
        self.assertEqual(row['pending_imports'],1)
        self.assertIn('Import: Readback failed',row['errors'])
        self.assertIn('Pending imports 1',render([row]))
        self.assertIn('Gaps 1',render([row]))

    def test_activity_browser_retry_is_visible_and_completed_capture_changes_stage(self):
        directory = self.config.output_root / '123'
        self.save('active.json', {'activity': {'task_id': '123'}, 'directory': str(directory)})
        self.save('status.json', {'status': 'capturing'})
        append_event(directory / 'activity-events.jsonl', 'browser_retry', error='Source unavailable')
        self.assertIn('Capture: Source unavailable', snapshot(self.config)['errors'])
        atomic_json(directory / 'capture-complete.json', {'task_id': '123'})
        self.assertEqual(snapshot(self.config)['stage'], 'Post-activity processing')
        atomic_json(directory / 'post-activity.json', {})
        self.assertEqual(snapshot(self.config)['stage'], 'Saving capture')

    def test_persistent_capture_error_survives_unrelated_log_events(self):
        directory = self.config.output_root / '123'
        self.save('active.json', {'activity': {'task_id': '123'}, 'directory': str(directory)})
        self.save('status.json', {'status': 'capturing'})
        atomic_json(directory / 'checkpoint.json', {'stage': 'activity',
            'pending_browser_error': {'error': 'Source binding mismatch'}})
        append_event(directory / 'activity-events.jsonl', 'page_interpretation', judgment={'action': 'reload'})
        self.assertIn('Capture: Source binding mismatch', snapshot(self.config)['errors'])
        atomic_json(directory / 'checkpoint.json', {'stage': 'activity',
            'pending_capture_blocker': {'error': 'Source binding mismatch'}})
        row = snapshot(self.config)
        self.assertEqual(row['stage'], 'Waiting for capture recovery')
        self.assertIn('Capture: Source binding mismatch', row['errors'])

    def test_solver_dependency_reason_remains_visible_while_activity_is_pinned(self):
        self.save('status.json', {'status': 'waiting_for_solver_dependency',
                  'error_type': 'SolverUnavailable', 'detail': 'Configured model unavailable'})
        row = snapshot(self.config)
        self.assertEqual(row['stage'], 'Waiting for solver recovery')
        self.assertIn('Configured model unavailable', row['errors'])

    def test_restarted_worker_is_starting_until_it_writes_a_fresh_status(self):
        self.save('worker.json', {'started_at': datetime.now().timestamp()})
        self.save('status.json', {'status': 'stopped', 'at': 1})
        self.assertEqual(snapshot(self.config, running=True)['stage'], 'Starting')

    def test_process_requires_current_start_token_not_merely_a_reused_pid(self):
        pid = os.getpid()
        token = Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()[19]
        self.assertTrue(process_running({'pid': pid, 'process_token': token}))
        self.assertFalse(process_running({'pid': pid, 'process_token': 'old-token'}))
        self.assertFalse(process_running({'pid': pid}))
        self.assertFalse(process_running({'pid': -1, 'process_token': token}))

    def test_render_shows_all_accounts_activity_and_errors_without_terminal_injection(self):
        rows = [{**snapshot(self.config, running=index == 0), 'account': account, 'label': label,
                 'task_id': '123', 'kind': 'review', 'title': 'Eigenvectors\n\033[31m',
                 'stage': 'Answering', 'errors': ['A source read failed'] if index == 0 else []}
                for index, (account, label) in enumerate([
                    ('foundations', 'Mathematical Methods'), ('linear', 'Linear Algebra'),
                    ('multivariable', 'Multivariable Calculus'), ('differential', 'Differential Equations')])]
        with patch('scripts.monitor.shutil.get_terminal_size', return_value=os.terminal_size((100, 30))):
            text = render(rows)
        for label in ('Mathematical Methods', 'Linear Algebra', 'Multivariable Calculus', 'Differential Equations'):
            self.assertIn(label, text)
        self.assertIn('Review 123', text)
        self.assertIn('Error: A source read failed', text)
        self.assertNotIn('\033', text)
        self.assertLessEqual(len(text.splitlines()), 30)
        self.assertIn('Today — XP', text)
        self.assertIn('1/4 running', render(rows, compact=True))
        self.assertTrue(all(len(line) == 100 for line in text.splitlines()))


if __name__ == '__main__':
    unittest.main()
