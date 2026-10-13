from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import uuid

from scripts.config import Config
from scripts.database.edn import dumps, kw
from scripts.monitor import render, snapshot, xp_bars, _width
from scripts.monitor_data import question_yield
from scripts.outbox import target_id
from scripts.storage import atomic_json, atomic_text
from scripts import terminal


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = Config(repo_root=self.root, account='linear', course_id='113')
        self.now = datetime.now().timestamp()
        self.today = datetime.now().astimezone().date().isoformat()

    def test_saved_output_has_base_xp_activity_mix_course_percent_and_bounded_logs(self):
        records = {}
        completed = {}
        for index, (kind, earned, base) in enumerate([('lesson', 8, 13), ('review', -2, 5), ('assessment', 10, None)]):
            task = str(index)
            source = self.config.output_root / task
            records[task] = {'task_id': task, 'kind': kind, 'date': self.today,
                             'earned_xp': earned, 'base_xp': base, 'source': str(source)}
            completed[task] = {'capture_completed_at': self.now + index, 'kind': kind}
            atomic_json(source / 'post-activity.json', {'observations': {'observed_at': self.now,
                'dashboard': {'course_progress': {'course_id': '113', 'displayed_progress': '23%'}}}})
        atomic_json(self.config.state_root / 'xp.json', records)
        atomic_json(self.config.state_root / 'completed.json', completed)
        atomic_json(self.config.state_root / 'daily-xp.json', {self.today: {'earned_xp': 16}})
        log = self.config.state_root / 'console.log'
        atomic_text(log, '\n'.join(f'message {i}' for i in range(100)) + '\n')
        row = snapshot(self.config, running=True)
        self.assertEqual((row['today_xp'], row['today_base_xp'], row['base_xp_unknown_tasks']), (16, 18, 1))
        self.assertEqual(row['activity_counts'], {'lesson': 1, 'review': 1, 'assessment': 1, 'multistep': 0, 'diagnostic': 0})
        self.assertEqual(row['percent_complete'], 23)
        self.assertEqual([a['earned_xp'] for a in row['recent_activities']], [8, -2, 10])
        self.assertEqual((len(row['log_lines']), row['log_lines'][-1]), (80, 'message 99'))
        text = render([row], include_logs=True, width=100, height=24)
        self.assertIn('16/18* XP', text)
        self.assertIn('L1 R1 Q1 M0 D0', text)
        self.assertIn('23%', text)
        self.assertIn('message 99', text)
        self.assertNotIn('message 0\n', text)
        # Moving to another course must not reuse the earlier course's percentage.
        self.config.course_id = '155'
        self.assertIsNone(snapshot(self.config, running=True)['percent_complete'])

    def import_fixture(self, name='one', status='verified'):
        directory = self.config.output_root / name
        root = directory / 'database'
        atomic_json(root / 'preparation.json', {'content': {
            'questions': [{'math_academy_id': 'q-1'}, {'math_academy_id': 'q-2'}, {'math_academy_id': 'q-bad'}],
            'canonical_examples': [{'math_academy_id': 'e-1'}]},
            'omissions': [{'kind': 'question', 'id': 'q-bad'}]})
        archive = root / 'requests' / 'request-1'
        atomic_json(archive / 'request.json', {'snapshot_edn': dumps({
            'attributes': [[1, kw('question/math-academy-id')]],
            'entities': [{kw('question/math-academy-id'): 'q-1'}]})})
        atomic_json(archive / 'result.json', {'status': 'verified'})
        atomic_text(archive / 'receipt.edn', dumps({kw('edb/committed'): True,
            kw('edb/tx-data'): [[1, 1, 'q-1', 1, 42, True], [2, 1, 'q-2', 1, 42, True], [3, 1, 'e-1', 1, 42, True]]}))
        return {'account': 'linear', 'capture_directory': str(directory), 'status': status,
                'last_attempt_at': self.now, 'target_id': target_id(self.config)}

    def test_database_yield_uses_verified_receipts_deduplicates_and_excludes_omissions(self):
        item = self.import_fixture()
        self.assertEqual(question_yield([item, item], self.today), {'added': 2, 'existing': 1, 'unknown_imports': 0})
        self.assertEqual(question_yield([item], '2000-01-01'), {'added': 0, 'existing': 0, 'unknown_imports': 0})
        atomic_json(self.config.spool_root / 'verified.json', item)
        atomic_json(self.config.spool_root / 'pending.json', {**item, 'status': 'pending'})
        atomic_json(self.config.spool_root / 'other.json', {**item, 'account': 'differential'})
        row = snapshot(self.config)
        self.assertEqual(row['database_questions']['added'], 2)
        self.assertEqual(row['database_questions']['existing'], 1)
        self.assertEqual(row['pending_imports'], 1)

    def test_unknown_import_evidence_is_marked_instead_of_fabricating_yield(self):
        item = {'capture_directory': str(self.config.output_root / 'missing'), 'status': 'verified', 'last_attempt_at': self.now}
        self.assertEqual(question_yield([item], self.today)['unknown_imports'], 1)

    def test_recent_chart_distinguishes_negative_zero_missing_and_positive_awards(self):
        chart, scale = xp_bars([{'earned_xp': value} for value in [-2, 0, None, 10, 20, 40]], length=6)
        self.assertEqual((chart, scale), ('↓·?▂▄█', 40))

    def rows(self):
        return [{'account': f'runner-{i}', 'label': f'Course {i}', 'running': True, 'status': 'RUNNING',
                 'answer_profile': 'capture', 'today_xp': 30, 'today_base_xp': 50,
                 'activity_counts': {'lesson': 2, 'review': 3}, 'percent_complete': 12.5,
                 'database_questions': {'added': 5, 'existing': 10}, 'pending_imports': 2,
                 'recent_activities': [{'earned_xp': 8}], 'kind': 'lesson', 'task_id': str(i),
                 'stage': 'Answering', 'title': f'Lesson title {i}',
                 'log_lines': [f'runner-{i} log-{j}' for j in range(30)], 'log_age': 1}
                for i in range(4)]

    def test_responsive_panels_keep_each_runners_latest_logs_inside_the_viewport(self):
        for width, height in [(123, 42), (80, 24), (80, 60), (60, 60), (80, 12)]:
            with self.subTest(size=(width, height)):
                text = render(self.rows(), include_logs=True, width=width, height=height)
                self.assertLessEqual(len(text.splitlines()), height)
                self.assertTrue(all(_width(line) <= width for line in text.splitlines()))
                for i in range(4):
                    self.assertIn(f'Course {i}', text)
                    self.assertIn(f'runner-{i} log-29', text)
                self.assertNotIn('log-0', text)
        rows = self.rows()
        rows[0]['log_lines'].append('new message arrived')
        self.assertIn('new message arrived', render(rows, include_logs=True, width=123, height=42))

    def test_status_and_log_text_cannot_move_the_cursor_or_emit_terminal_commands(self):
        rows = self.rows()
        rows[0]['log_lines'] = ['\x1b[2Junsafe\x1b]0;new title\x07漢字']
        text = render(rows, include_logs=True, width=123, height=42)
        self.assertNotIn('\x1b', text)
        self.assertIn('unsafe漢字', text)
        self.assertTrue(all(_width(line) == 123 for line in text.splitlines()))

    def test_course_headings_preserve_physical_sciences_and_original_codes(self):
        rows = self.rows()
        rows[0].update(account='multivariable', label='Mathematical Methods for the Physical Sciences II',
                       original_course_code='mvc')
        rows[1].update(account='foundations', label='Mathematical Methods for the Physical Sciences I',
                       original_course_code='MF3')
        for width, height in [(123, 42), (100, 42), (80, 24), (80, 12)]:
            with self.subTest(size=(width,height)):
                text = render(rows, include_logs=True, width=width, height=height)
                self.assertIn('Physical Sciences II (MVC)', text)
                self.assertIn('Physical Sciences I (MF3)', text)
                self.assertLessEqual(len(text.splitlines()),height)
                self.assertTrue(all(_width(line)==width for line in text.splitlines()))
                for i in range(4):
                    self.assertIn(f'runner-{i} log-29', text)


class LayoutMigrationTests(unittest.TestCase):
    def test_migration_preserves_worker_panes_and_pids_and_is_repeatable(self):
        socket = 'capture-test-' + uuid.uuid4().hex[:12]
        def tmux(*args, check=True):
            result = subprocess.run(['tmux', '-L', socket, *map(str, args)], text=True, capture_output=True)
            if check and result.returncode:
                raise RuntimeError(result.stderr)
            return result
        self.addCleanup(lambda: tmux('kill-server', check=False))
        with tempfile.TemporaryDirectory() as root:
            config = Path(root) / 'config.json'
            atomic_json(config, {'repo_root': root})
            args = type('Args', (), {'session': 'capture-test', 'config': config, 'capture_only': None,
                'visible': False, 'learner_id': None, 'finish_started': False})()
            tmux('new-session', '-d', '-s', args.session, '-n', 'first', 'exec sleep 300')
            tmux('set-option', '-t', args.session, '@capture_version', '2')
            first = tmux('list-windows', '-t', args.session, '-F', '#{window_id}').stdout.strip()
            tmux('set-window-option', '-t', first, '@capture_account', 'foundations')
            dashboard = tmux('split-window', '-d', '-P', '-F', '#{pane_id}', '-t', first, 'exec sleep 300').stdout.strip()
            tmux('set-option', '-p', '-t', dashboard, '@capture_dashboard', '1')
            for account in terminal.ACCOUNTS[1:]:
                window = tmux('new-window', '-d', '-P', '-F', '#{window_id}', '-t', args.session,
                              '-n', account, 'exec sleep 300').stdout.strip()
                tmux('set-window-option', '-t', window, '@capture_account', account)
            before = tmux('list-panes', '-s', '-t', args.session, '-F', '#{pane_id}|#{pane_pid}').stdout.splitlines()
            with patch.object(terminal, 'tmux', side_effect=tmux), patch.object(terminal, 'invocation', return_value='exec sleep 300'):
                panes = terminal.ensure_layout(args)
                repeated = terminal.ensure_layout(args)
            self.assertEqual(panes, repeated)
            self.assertEqual(set(panes), set(terminal.ACCOUNTS))
            after = tmux('list-panes', '-a', '-F', '#{pane_id}|#{pane_pid}').stdout.splitlines()
            self.assertEqual(set(before), set(after))
            self.assertEqual(tmux('list-windows', '-t', args.session, '-F', '#{window_name}').stdout.strip(), 'Capture')
            self.assertEqual(tmux('list-panes', '-s', '-t', args.session, '-F', '#{pane_id}').stdout.strip(), dashboard)
            self.assertEqual(len(tmux('list-windows', '-t', args.session + '-workers').stdout.splitlines()), 4)
