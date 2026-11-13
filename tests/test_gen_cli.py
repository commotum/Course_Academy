"""Parent admission, quota exhaustion, CLI syntax, and detached launch safety."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import gen_cli as G
from inventory_jobs import InventoryJobs, save


class SupervisorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.jobs = SimpleNamespace(directory=self.root / 'jobs', run_one=Mock(return_value=False))
        self.jobs.directory.mkdir()
        self.runtime = self.root / 'run'
        self.runtime.mkdir()
        self.now = 1000

    def tearDown(self):
        self.temp.cleanup()

    def supervisor(self, **kwargs):
        return G.Supervisor(self.jobs, self.runtime, clock=lambda: self.now, **kwargs)

    def admit(self, supervisor):
        return supervisor.handle({'event': 'admit', 'pid': os.getpid(), 'role': 'author',
                                  'directory': str(self.jobs.directory / 'work')})

    def evidence(self, supervisor, lines, *, offset=0, ticket=None):
        directory = self.jobs.directory / 'work'
        directory.mkdir(exist_ok=True)
        path = directory / 'events.jsonl'
        path.write_text(''.join(json.dumps(row) + '\n' for row in lines))
        return supervisor.handle({'event': 'complete', 'pid': os.getpid(), 'directory': str(directory),
                                  'events_path': str(path), 'events_offset': offset, 'returncode': 1,
                                  'ticket': ticket or 'old-run-ticket'})

    def test_thresholds_use_remaining_percentage_points_and_round_down_workers_gradually(self):
        self.assertEqual(G.policy(36, 25, 6), (6, 1800))
        self.assertEqual(G.policy(35, 25, 6), (3, 900))
        self.assertEqual(G.policy(31, 25, 5), (3, 900))
        self.assertEqual(G.policy(30, 25, 6), (1, 300))
        self.assertEqual(G.policy(25, 25, 6), (0, 300))
        self.assertEqual(G.policy(0, 25, 6), (0, 300))

    def test_no_until_never_polls_and_quota_error_stops_all_other_admissions(self):
        reader = Mock(side_effect=AssertionError('quota reader must stay unused'))
        supervisor = self.supervisor(quota_reader=reader)
        supervisor.quota_poll()
        first, second = self.admit(supervisor), self.admit(supervisor)
        self.assertEqual(first['action'], 'run')
        reply = self.evidence(supervisor, [{'type': 'turn.failed', 'error': {
            'message': 'You’ve hit your usage limit. Try again later.'}}], ticket=first['ticket'])
        self.assertTrue(reply['exempt'])
        self.assertEqual(reply['action'], 'halt')
        self.assertEqual(self.admit(supervisor)['action'], 'halt')
        # An already running worker stays active; no kill or retry is sent.
        self.assertIn(second['ticket'], supervisor.tickets)
        self.assertEqual(supervisor.allowed, 0)
        reader.assert_not_called()

    def test_throttling_does_not_interrupt_active_leases_and_expired_quota_blocks_admission(self):
        reader = Mock(side_effect=[{'remaining_percent': 50}, {'remaining_percent': 33},
                                   {'remaining_percent': 29}, {'remaining_percent': 25}])
        supervisor = self.supervisor(until=25, quota_reader=reader)
        self.assertEqual(self.admit(supervisor)['action'], 'wait')
        supervisor.quota_poll()
        tickets = [self.admit(supervisor)['ticket'] for _ in range(6)]
        self.assertEqual(self.admit(supervisor)['action'], 'wait')
        self.now = supervisor.next_poll
        self.assertEqual(self.admit(supervisor)['action'], 'wait')
        supervisor.quota_poll()
        self.assertEqual(supervisor.allowed, 3)
        self.assertEqual(len(supervisor.tickets), 6)
        self.assertEqual(supervisor.next_poll, self.now + 900)
        supervisor.quota_poll()
        self.assertEqual(supervisor.allowed, 1)
        self.assertEqual(set(tickets), set(supervisor.tickets))
        supervisor.quota_poll()
        self.assertTrue(supervisor.draining)
        self.assertEqual(self.admit(supervisor)['action'], 'halt')

    def test_unavailable_quota_or_explicit_denial_drains_without_inventing_remaining(self):
        for reader in (Mock(side_effect=RuntimeError('offline')),
                       Mock(return_value={'remaining_percent': 99, 'exhausted': True}),
                       Mock(return_value={'remaining_percent': float('nan')})):
            supervisor = self.supervisor(until=25, quota_reader=reader)
            supervisor.quota_poll()
            self.assertTrue(supervisor.draining)
            self.assertEqual(supervisor.allowed, 0)

    def test_old_quota_events_and_tool_output_do_not_override_current_real_failure(self):
        supervisor = self.supervisor()
        old = {'type': 'error', 'message': "You've hit your usage limit."}
        offset = len((json.dumps(old) + '\n').encode())
        current = {'type': 'turn.failed', 'error': {'message': 'tool execution failed'}}
        result = self.evidence(supervisor, [old, current], offset=offset)
        self.assertEqual(result, {'action': 'continue'})
        result = self.evidence(supervisor, [{'type': 'item.completed', 'item': {
            'type': 'command_execution', 'aggregated_output': "You've hit your usage limit."}}])
        self.assertEqual(result, {'action': 'continue'})
        self.assertFalse(supervisor.draining)

    def test_previous_parent_completion_can_replay_without_releasing_a_current_worker(self):
        supervisor = self.supervisor()
        current = self.admit(supervisor)
        result = self.evidence(supervisor, [{'type': 'error', 'code': 'insufficient_quota'}])
        self.assertTrue(result['exempt'])
        self.assertIn(current['ticket'], supervisor.tickets)
        self.assertFalse(supervisor.draining, 'Old quota evidence must not stop an explicit restart')

    def test_exact_capacity_rejection_stops_admissions_without_charging_content_failure(self):
        message = 'Selected model is at capacity. Please try a different model.'
        for row in ({'type': 'error', 'message': message},
                    {'type': 'turn.failed', 'error': {'message': message}}):
            with self.subTest(row=row):
                supervisor = self.supervisor()
                ticket = self.admit(supervisor)['ticket']
                response = self.evidence(supervisor, [row], ticket=ticket)
                self.assertEqual(response['action'], 'halt')
                self.assertTrue(response['exempt'])
                self.assertIn('at capacity', supervisor.reason)
                self.assertNotIn('quota', supervisor.reason)
                self.assertEqual(self.admit(supervisor)['action'], 'halt')
                self.assertFalse(G.usage_failure(self.jobs.directory / 'work/events.jsonl'))
                # A fresh explicit run reconciles an old rejected turn without
                # treating that old failure as evidence of current capacity.
                restarted = self.supervisor()
                self.assertTrue(self.evidence(restarted, [row], ticket=ticket)['exempt'])
                self.assertFalse(restarted.draining)

    def test_provider_output_schema_error_is_distinct_and_requires_exact_structured_evidence(self):
        provider = {'message': "Invalid schema for response_format 'codex_output_schema'",
                    'type': 'invalid_request_error', 'code': 'invalid_json_schema',
                    'param': 'text.format.schema'}
        for row in ({'type': 'error', 'message': json.dumps({'error': provider})},
                    {'type': 'turn.failed', 'error': provider}):
            with self.subTest(row=row):
                supervisor = self.supervisor()
                ticket = self.admit(supervisor)['ticket']
                response = self.evidence(supervisor, [row], ticket=ticket)
                self.assertEqual(response['action'], 'halt')
                self.assertTrue(response['exempt'])
                self.assertIn('output schema', supervisor.reason)
                self.assertNotIn('quota', supervisor.reason)
                self.assertEqual(self.admit(supervisor)['action'], 'halt')
        supervisor = self.supervisor()
        lookalikes = [
            {'type': 'item.completed', 'item': {'aggregated_output': json.dumps({'error': provider})}},
            {'type': 'error', 'message': 'Tool says invalid_json_schema'},
            {'type': 'error', 'message': json.dumps({'error': {**provider, 'param': 'some-tool-input'}})},
            {'type': 'turn.failed', 'error': {'message': 'The worksheet describes model capacity.'}},
            {'type': 'error', 'message': 'Reconnecting... stream disconnected before completion'},
        ]
        self.assertEqual(self.evidence(supervisor, lookalikes), {'action': 'continue'})
        self.assertFalse(supervisor.draining)

    def test_developer_mode_prevents_new_agent_turns_inside_an_existing_pipeline(self):
        supervisor = self.supervisor()
        supervisor.developer_mode = lambda: True
        self.assertEqual(self.admit(supervisor)['action'], 'wait')
        supervisor.drain('stop requested')
        self.assertEqual(self.admit(supervisor)['action'], 'halt')

    def test_quota_reserve_at_start_runs_no_inventory_or_workers(self):
        supervisor = self.supervisor(until=100, quota_reader=lambda: {'remaining_percent': 99})
        refresh = Mock()
        supervisor.run(refresh)
        refresh.assert_not_called()
        self.jobs.run_one.assert_not_called()
        saved = json.loads((self.runtime / 'run.json').read_text())
        self.assertEqual(saved['state'], 'stopped')
        self.assertFalse((self.runtime / 'control.sock').exists())

    def test_socket_stop_returns_while_running_worker_finishes_and_saves_stopped(self):
        entered, finish = threading.Event(), threading.Event()
        supervisor = self.supervisor(workers=1)
        completions = []
        def work(lane, slot):
            if lane == 'refill':
                return False
            ticket = G.request(self.runtime / 'control.sock', {'event': 'admit', 'pid': os.getpid()})
            completions.append(ticket['action'])
            entered.set()
            self.assertTrue(finish.wait(5))
            completions.append(G.request(self.runtime / 'control.sock', {'event': 'admit', 'pid': os.getpid()})['action'])
            return False
        self.jobs.run_one = work
        failures = []
        def run():
            try:
                supervisor.run(lambda: None)
            except BaseException as error:
                failures.append(error)
        parent = threading.Thread(target=run)
        parent.start()
        try:
            self.assertTrue(entered.wait(5))
            reply = G.request(self.runtime / 'control.sock', {'event': 'stop'})
            self.assertEqual(reply['state'], 'draining')
            self.assertTrue(parent.is_alive())
            self.assertEqual(completions, ['run'])
        finally:
            finish.set()
            parent.join(6)
        self.assertFalse(parent.is_alive())
        self.assertEqual(failures, [])
        self.assertEqual(completions, ['run', 'halt'])
        self.assertEqual(json.loads((self.runtime / 'run.json').read_text())['state'], 'stopped')

    def test_real_worker_processes_stop_on_first_quota_failure_without_blocking_queue(self):
        fake_codex = self.root / 'fake-codex'
        fake_codex.write_text(f'#!{sys.executable}\n' +
            'import json,sys,time\n'
            'sys.stdin.read()\ntime.sleep(.1)\n'
            'print(json.dumps({"type":"turn.failed","error":{"message":"You’ve hit your usage limit."}}))\n'
            'sys.exit(1)\n')
        fake_codex.chmod(0o755)
        pipeline = self.root / 'pipeline.py'
        pipeline.write_text('import json,os,sys\nfrom pathlib import Path\n' +
            f'sys.path.insert(0, {str(G.ROOT / "scripts")!r})\n' +
            'from generator_pipeline import CodexSession\n'
            'job=Path(sys.argv[1]); directory=job.with_suffix(".pipeline")/"1"/"author"\n'
            f'CodexSession(root=Path({str(G.ROOT)!r}))("author", {{"workspace":str(directory)}}, directory)\n')
        environment = {**os.environ,
            G.CONTROL_ENV: str(self.runtime / 'control.sock'),
            'COURSE_ACADEMY_GENERATOR_COMMAND': json.dumps([sys.executable, str(pipeline)]),
            'COURSE_ACADEMY_GENERATOR_BUILD_WORKERS': '3',
            'COURSE_ACADEMY_CODEX_EXECUTABLE': str(fake_codex)}
        jobs = InventoryJobs(G.ROOT, self.jobs.directory, 'learner', environment)
        jobs.accept({'basis': 1, 'lineage': 'test', 'qualifyingTopics': [], 'jobs': [
            {'knowledgePoint': index, 'topic': 100, 'difficulty': 'easy', 'missing': 5,
             'available': 0, 'stage': 'create-generator', 'script': None,
             'urgency': 0, 'proximity': 1, 'priority': 1, 'basis': 1}
            for index in range(1, 21)]})
        reader = Mock(side_effect=AssertionError('No quota polling without -u'))
        supervisor = G.Supervisor(jobs, self.runtime, workers=3, quota_reader=reader)
        supervisor.run(lambda: None)
        records = [json.loads(p.read_text()) for p in jobs.directory.glob('*.json') if p.name != 'cursor.json']
        self.assertEqual(len(records), 20)
        self.assertEqual({row['state'] for row in records}, {'pending'})
        self.assertTrue(all(row.get('attempts', 0) == 0 for row in records))
        executions = list(jobs.directory.glob('*.pipeline/1/author/execution.json'))
        self.assertGreaterEqual(len(executions), 1)
        self.assertLessEqual(len(executions), 3)
        for path in executions:
            value = json.loads(path.read_text())
            self.assertEqual((value['launches'], value['launch_limit'], value['status']), (1, 4, 'deferred'))
            self.assertEqual(len(value['parent_deferrals']), 1)
        reader.assert_not_called()


class CliTests(unittest.TestCase):
    def test_flags_defaults_and_aliases(self):
        with patch.object(G, 'start', return_value=0) as start:
            self.assertEqual(G.main([]), 0)
            start.assert_called_once_with(6, None, None)
            self.assertEqual(G.main(['--w', '4', '--u', '25']), 0)
            start.assert_called_with(4, 25, None)
            self.assertEqual(G.main(['-w', '2', '--until', '30']), 0)
            start.assert_called_with(2, 30, None)
        with patch.object(G, 'read_status', return_value={'state': 'stopped'}), patch.object(G, 'request') as rpc:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(G.main(['--s']), 0)
                self.assertEqual(G.main(['-k']), 0)
            rpc.assert_not_called()

    def test_invalid_flags_do_not_start(self):
        with patch.object(G, 'start') as start, contextlib.redirect_stderr(io.StringIO()):
            for args in (['-w', '0'], ['-u', '101'], ['-u', 'nan'], ['-k', '-u', '25'], ['-s', '-w', '1'],
                         ['-t', '0'], ['-t', '-1'], ['-t', 'abc'], ['-t', '1.5'],
                         ['-t', str(2**63)], ['-s', '-t', '123'], ['-k', '-t', '123']):
                with self.subTest(args=args), self.assertRaises(SystemExit):
                    G.main(args)
            start.assert_not_called()

    def test_topic_aliases_accept_entity_ids_and_compose_with_worker_and_quota_options(self):
        with patch.object(G, 'start', return_value=0) as start:
            for flag in ('-t', '--t', '--topic'):
                for value in ('17592186050938', ':db/id=17592186050938'):
                    self.assertEqual(G.main([flag, value, '-w', '2', '-u', '25']), 0)
                    start.assert_called_with(2, 25, 17592186050938)

    def test_topic_scope_is_passed_to_detached_service(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(G, 'RUNTIME', Path(temp)), \
                patch.object(G, 'read_status', side_effect=[{'state': 'stopped'}, {
                    'state': 'starting', 'started_at': time.time() + 100, 'workers': 6,
                    'topic': 17592186050938}]), \
                patch.object(G.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')) as run, \
                contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(G.start(6, None, 17592186050938), 0)
            self.assertEqual(run.call_args.args[0][-2:], ['-t', '17592186050938'])
            self.assertIn('Topic: 17592186050938', output.getvalue())

    def test_running_generator_cannot_silently_ignore_a_different_requested_scope(self):
        for old_topic, new_topic in ((None, 123), (123, None), (123, 456)):
            with self.subTest(old=old_topic, new=new_topic), tempfile.TemporaryDirectory() as temp, \
                    patch.object(G, 'RUNTIME', Path(temp)), \
                    patch.object(G, 'read_status', return_value={'state': 'running', 'topic': old_topic}), \
                    patch.object(G.subprocess, 'run') as run:
                with self.assertRaisesRegex(RuntimeError, 'already running'):
                    G.start(6, None, new_topic)
                run.assert_not_called()

    def test_detached_launch_is_owned_by_user_service_without_auto_restart(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(G, 'RUNTIME', Path(temp)), \
                patch.object(G, 'read_status', side_effect=[{'state': 'stopped'}, {
                    'state': 'starting', 'started_at': time.time() + 100, 'workers': 6}]), \
                patch.object(G.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')) as run, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(G.start(6, 25), 0)
            command = run.call_args.args[0]
            self.assertIn('systemd-run', command)
            self.assertIn('--property=Restart=no', command)
            self.assertIn('--property=TimeoutStopSec=infinity', command)
            self.assertEqual(command[-2:], ['-u', '25'])
            self.assertNotIn('--pty', command)

    def test_detached_launch_keeps_shell_database_and_codex_overrides_without_exposing_values(self):
        environment = {'PATH': '/custom/bin', 'EDB_POSTGRES_URL': 'private-database-credentials',
                       'COURSE_ACADEMY_CODEX_EXECUTABLE': '/custom/codex',
                       'CODEX_HOME': '/custom/account', 'UNRELATED_SECRET': 'leave-out'}
        with tempfile.TemporaryDirectory() as temp, patch.object(G, 'RUNTIME', Path(temp)), \
                patch.dict(os.environ, environment, clear=True), \
                patch.object(G, 'read_status', side_effect=[{'state': 'stopped'}, {
                    'state': 'starting', 'started_at': time.time() + 100, 'workers': 6}]), \
                patch.object(G.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')) as run, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(G.start(6, None), 0)
            command = run.call_args.args[0]
            for key in environment.keys() - {'UNRELATED_SECRET'}:
                self.assertIn('--setenv=' + key, command)
            self.assertNotIn('--setenv=UNRELATED_SECRET', command)
            self.assertNotIn('private-database-credentials', ' '.join(command))

    def test_status_and_stop_succeed_if_daemon_exits_before_socket_connect(self):
        for flag in ('-s', '-k'):
            with self.subTest(flag=flag), \
                    patch.object(G, 'read_status', side_effect=[{'state': 'running'}, {
                        'state': 'stopped', 'reason': 'stop requested'}]), \
                    patch.object(G, 'request', side_effect=ConnectionRefusedError), \
                    contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(G.main([flag]), 0)
                self.assertIn('Generator stopped', output.getvalue())

    def test_unavailable_socket_of_live_daemon_is_not_reported_as_stopped(self):
        with patch.object(G, 'read_status', return_value={'state': 'running'}), \
                patch.object(G, 'request', side_effect=ConnectionRefusedError('socket unavailable')), \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(G.main(['-k']), 1)

    def test_dead_parent_and_reused_pid_cannot_look_running(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            save(root / 'run.json', {'state': 'running', 'pid': os.getpid(), 'start_ticks': 'not-this-process'})
            self.assertEqual(G.read_status(root)['state'], 'stopped')


if __name__ == '__main__':
    unittest.main()
