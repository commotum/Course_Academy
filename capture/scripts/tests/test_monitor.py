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
        self.assertLessEqual(len(text.splitlines()), 18)
        self.assertIn('Today — XP', text)
        self.assertIn('1/4 running', render(rows, compact=True))
        self.assertTrue(all(len(line) == 100 for line in text.splitlines()))


if __name__ == '__main__':
    unittest.main()
