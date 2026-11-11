"""Real local IPC and subprocess checks for generic resumable turn admission."""
import json
import os
from pathlib import Path
import socketserver
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from generator_control import CONTROL_ENV, PAUSED_EXIT, GenerationPaused
from generator_pipeline import CodexSession, SessionRetryExhausted
from inventory_jobs import InventoryJobs, save


class Parent:
    def __init__(self, path, respond):
        self.path, self.messages = path, []
        parent = self
        class Handler(socketserver.StreamRequestHandler):
            def handle(self):
                message = json.loads(self.rfile.readline())
                parent.messages.append(message)
                result = respond(message)
                if result is not None:
                    self.wfile.write((json.dumps(result) + '\n').encode())
        self.server = socketserver.ThreadingUnixStreamServer(str(path), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(3)
        self.path.unlink(missing_ok=True)


class ParentControlTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.directory = self.root / 'session'
        self.directory.mkdir()
        self.socket = self.root / 'control.sock'
        self.parents = []
        self.environment = {CONTROL_ENV: str(self.socket)}
        self.context = {'workspace': str(self.directory)}

    def tearDown(self):
        for parent in reversed(self.parents):
            parent.close()
        self.temp.cleanup()

    def parent(self, respond):
        parent = Parent(self.socket, respond)
        self.parents.append(parent)
        return parent

    def executable(self, text):
        path = self.root / 'fake-codex'
        path.write_text('#!' + sys.executable + '\nimport json,sys\nfrom pathlib import Path\n'
                        'sys.stdin.read()\n' + text)
        path.chmod(0o755)
        self.environment['COURSE_ACADEMY_CODEX_EXECUTABLE'] = str(path)

    def call(self, directory=None, context=None):
        return CodexSession(root=ROOT, environment=self.environment)(
            'author', context or self.context, directory or self.directory)

    def execution(self):
        return json.loads((self.directory / 'execution.json').read_text())

    def test_denied_admission_and_parent_loss_never_spend_launches(self):
        parent = self.parent(lambda _: {'action': 'halt', 'reason': 'requested stop'})
        with patch('generator_pipeline.subprocess.Popen') as spawn:
            with self.assertRaises(GenerationPaused) as caught:
                self.call()
            self.assertEqual(caught.exception.code, PAUSED_EXIT)
            spawn.assert_not_called()
        self.assertFalse((self.directory / 'execution.json').exists())
        parent.close(); self.parents.remove(parent)
        with self.assertRaises(GenerationPaused):
            self.call()
        self.assertFalse((self.directory / 'execution.json').exists())

    def test_wait_is_retried_without_launching_then_stop_is_respected(self):
        replies = iter([{'action': 'wait'}, {'action': 'halt', 'reason': 'stopping'}])
        self.parent(lambda _: next(replies))
        with patch('generator_control.time.sleep') as wait, patch('generator_pipeline.subprocess.Popen') as spawn:
            with self.assertRaises(GenerationPaused):
                self.call()
        wait.assert_called_once_with(1)
        spawn.assert_not_called()

    def test_parent_exemption_keeps_history_and_exactly_one_retry_credit(self):
        complete = {'action': 'halt', 'reason': 'parent administrative rejection', 'exempt': True}
        parent = self.parent(lambda m: {'action': 'run', 'ticket': 'first'} if m['event'] == 'admit' else complete)
        self.executable('print(json.dumps({"type":"turn.failed","error":{"message":"raw failure"}}))\nsys.exit(1)\n')
        save(self.directory / 'execution.json', {'launches': 2, 'status': 'failed', 'error': 'prior real failures'})
        prior = '{"type":"error","message":"old output must not be rescanned: λ"}\n'
        (self.directory / 'events.jsonl').write_text(prior)
        with self.assertRaises(GenerationPaused):
            self.call()
        execution = self.execution()
        self.assertEqual((execution['launches'], execution['launch_limit'], execution['status']), (3, 4, 'deferred'))
        self.assertEqual(len(execution['parent_deferrals']), 1)
        event = parent.messages[-1]
        self.assertEqual(event['events_offset'], len(prior.encode()))
        self.assertEqual(event['returncode'], 1)
        self.assertEqual(event['events_path'], str(self.directory / 'events.jsonl'))
        self.assertNotIn('parent_completion', execution)
        complete.clear(); complete.update(action='continue')
        with self.assertRaises(SessionRetryExhausted):
            self.call()
        self.assertEqual((self.execution()['launches'], self.execution()['launch_limit']), (4, 4))
        self.assertEqual(len(self.execution()['parent_deferrals']), 1)

    def test_genuine_agent_failures_keep_the_original_retry_budget(self):
        parent = self.parent(lambda m: {'action': 'run', 'ticket': str(len(parent.messages))}
                             if m['event'] == 'admit' else {'action': 'continue'})
        self.executable('sys.exit(1)\n')
        for _ in range(2):
            with self.assertRaises(subprocess.CalledProcessError):
                self.call()
        with self.assertRaises(SessionRetryExhausted):
            self.call()
        self.assertEqual(self.execution()['launches'], 3)
        self.assertNotIn('launch_limit', self.execution())
        self.assertNotIn('parent_deferrals', self.execution())

    def test_parent_loss_after_failure_replays_completion_before_budget_check(self):
        parent = self.parent(lambda m: {'action': 'run', 'ticket': 'lost-parent'} if m['event'] == 'admit' else None)
        self.executable('sys.exit(1)\n')
        save(self.directory / 'execution.json', {'launches': 2})
        with self.assertRaises(GenerationPaused):
            self.call()
        saved = self.execution()
        self.assertEqual((saved['launches'], saved['status']), (3, 'awaiting-parent'))
        event = saved['parent_completion']
        parent.close(); self.parents.remove(parent)
        replacement = self.parent(lambda _: {'action': 'halt', 'exempt': True, 'reason': 'reconciled deferral'})
        with self.assertRaises(GenerationPaused):
            self.call()
        self.assertEqual(replacement.messages, [event])
        self.assertEqual(self.execution()['launch_limit'], 4)

    def test_completed_turn_survives_stop_and_does_not_start_another(self):
        running, release = self.root / 'running', self.root / 'release'
        stopping = threading.Event()
        parent = self.parent(lambda m: ({'action': 'halt'} if stopping.is_set() else {'action': 'run', 'ticket': 'active'})
                             if m['event'] == 'admit' else {'action': 'halt', 'reason': 'draining'})
        self.executable('import time\n'
                        f'Path({str(running)!r}).touch()\n'
                        f'while not Path({str(release)!r}).exists(): time.sleep(.01)\n'
                        'Path(sys.argv[sys.argv.index("--output-last-message")+1]).write_text(json.dumps({"status":"ready"}))\n')
        result, errors = [], []
        def work():
            try: result.append(self.call())
            except BaseException as error: errors.append(error)
        worker = threading.Thread(target=work)
        worker.start()
        import time
        deadline = time.monotonic() + 5
        while not running.exists() and time.monotonic() < deadline:
            time.sleep(.01)
        self.assertTrue(running.exists())
        stopping.set()
        self.assertTrue(worker.is_alive(), 'Stop must let the current turn finish')
        release.touch(); worker.join(5)
        self.assertFalse(worker.is_alive())
        self.assertEqual(errors, [])
        self.assertEqual(result, [{'status': 'ready'}])
        self.assertEqual(self.execution()['status'], 'completed')
        self.assertEqual(self.call(), {'status': 'ready'}, 'Completed result is reusable without admission')
        other = self.root / 'next'
        with self.assertRaises(GenerationPaused):
            self.call(directory=other, context={'workspace': str(other)})
        self.assertEqual([m['event'] for m in parent.messages], ['admit', 'complete', 'admit'])

    def test_spawn_failure_releases_parent_admission(self):
        parent = self.parent(lambda m: {'action': 'run', 'ticket': 'spawn'} if m['event'] == 'admit' else {'action': 'continue'})
        self.environment['COURSE_ACADEMY_CODEX_EXECUTABLE'] = str(self.root / 'missing-executable')
        with self.assertRaises(FileNotFoundError):
            self.call()
        self.assertEqual([m['event'] for m in parent.messages], ['admit', 'complete'])
        self.assertIsNone(parent.messages[-1]['returncode'])
        self.assertEqual(self.execution()['status'], 'failed')

    def test_timeout_releases_parent_admission_and_keeps_failure_budget(self):
        parent = self.parent(lambda m: {'action': 'run', 'ticket': 'timeout'} if m['event'] == 'admit' else {'action': 'continue'})
        self.executable('import time\ntime.sleep(30)\n')
        with self.assertRaises(subprocess.TimeoutExpired):
            CodexSession(root=ROOT, environment=self.environment, timeout=.1)(
                'author', self.context, self.directory)
        self.assertEqual([m['event'] for m in parent.messages], ['admit', 'complete'])
        self.assertLess(parent.messages[-1]['returncode'], 0)
        self.assertEqual(self.execution()['status'], 'failed')
        self.assertNotIn('launch_limit', self.execution())

    def test_successful_result_survives_missing_completion_reply(self):
        self.parent(lambda m: {'action': 'run', 'ticket': 'result'} if m['event'] == 'admit' else None)
        self.executable('Path(sys.argv[sys.argv.index("--output-last-message")+1]).write_text(json.dumps({"status":"ready"}))\n')
        self.assertEqual(self.call(), {'status': 'ready'})
        self.assertEqual(self.execution()['status'], 'completed')
        self.environment[CONTROL_ENV] = str(self.root / 'missing.sock')
        self.assertEqual(self.call(), {'status': 'ready'})

    def test_shared_source_account_budget_keeps_one_credit_across_revision(self):
        response = {'action': 'halt', 'reason': 'deferred', 'exempt': True}
        self.parent(lambda m: {'action': 'run', 'ticket': 'source'} if m['event'] == 'admit' else response)
        self.executable('sys.exit(1)\n')
        budget = self.root / 'source-account/execution.json'
        context = {**self.context, 'phase': 'source_account', '_execution_budget_file': str(budget),
                   'source_account_identity': 'fixed', 'source_account_isolation': 1,
                   'source_account_revision': 'first'}
        save(budget, {'launches': 2, 'source_account_aggregate': True})
        with self.assertRaises(GenerationPaused):
            self.call(context=context)
        self.assertEqual(json.loads(budget.read_text())['launch_limit'], 4)
        response.clear(); response.update(action='continue')
        self.executable('Path(sys.argv[sys.argv.index("--output-last-message")+1]).write_text(json.dumps({"status":"ready"}))\n')
        second = self.root / 'second-revision'
        self.assertEqual(self.call(directory=second, context={**context, 'source_account_revision': 'second'}), {'status': 'ready'})
        execution = json.loads(budget.read_text())
        self.assertEqual((execution['launches'], execution['launch_limit']), (4, 4))
        self.assertEqual(len(execution['parent_deferrals']), 1)

    def test_inventory_deferral_keeps_failure_budgets_and_publication_intent(self):
        jobs = InventoryJobs(ROOT, self.root / 'jobs', 'learner', self.environment)
        request = dict(knowledgePoint=1, topic=2, difficulty='hard', available=0,
                       missing=5, urgency=0, proximity=1, priority=12,
                       stage='create-generator', script=None, basis=10)
        jobs.accept(dict(basis=10, lineage='same', jobs=[request], qualifyingTopics=[2]))
        path = next(p for p in jobs.directory.glob('*.json') if p.name != 'cursor.json')
        before = json.loads(path.read_text())
        before.update(attempts=2, processFailures=2, replenishments=1, error='previous real failure')
        save(path, before)
        publication = path.with_suffix('.pipeline') / '1/publication/request.json'
        save(publication, {'request_id': 'already-reviewed-intent'})
        with patch.object(jobs, '_run_pipeline', return_value=subprocess.CompletedProcess([], PAUSED_EXIT)):
            self.assertTrue(jobs.run_one())
        after = json.loads(path.read_text())
        self.assertEqual(after['state'], 'pending')
        self.assertEqual(after['exitCode'], PAUSED_EXIT)
        for key in ('attempts', 'processFailures', 'replenishments', 'error', 'request'):
            self.assertEqual(after[key], before[key])
        self.assertEqual(json.loads(publication.read_text()), {'request_id': 'already-reviewed-intent'})


class PipelinePauseTests(unittest.TestCase):
    def test_pause_reuses_author_attempt_and_source_review_rounds(self):
        import test_generator_pipeline as fixtures
        from generator_pipeline import Pipeline
        for stopped_role, stopped_phase in [('investigate', 'source_account'), ('review', 'source_account'),
                                            ('author', None), ('review', None)]:
            with self.subTest(role=stopped_role, phase=stopped_phase), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                publisher = fixtures.FakePublisher(root)
                class PauseOnce(fixtures.FakeSession):
                    paused = False
                    def maybe_pause(self, role, context):
                        if not self.paused and role == stopped_role and context.get('phase') == stopped_phase:
                            self.paused = True
                            raise GenerationPaused('administrative stop')
                    def phase_call(self, role, context, directory):
                        self.maybe_pause(role, context)
                        return super().phase_call(role, context, directory)
                    def __call__(self, role, context, directory):
                        self.maybe_pause(role, context)
                        return super().__call__(role, context, directory)
                session = fixtures.PhaseSession(PauseOnce())
                def pipeline():
                    return Pipeline(root / 'job', {'kp': 123, 'difficulty': 'easy', 'count': 3,
                        'existing_entrypoint': None}, publisher, root=root,
                        environment={**os.environ, 'EDB_MATH_ROOT': str(root / 'math'),
                                     'COURSE_ACADEMY_GENERATOR_PYTHON': sys.executable},
                        session=session, max_attempts=2, investigation_preparer=fixtures.fixture_investigation)
                with self.assertRaises(GenerationPaused):
                    pipeline().run()
                paused = json.loads((root / 'job/job.json').read_text())
                self.assertNotEqual(paused['stage'], 'blocked')
                self.assertEqual(paused.get('source_account_rounds', {}), {})
                result = pipeline().run()
                self.assertEqual(result['stage'], 'verified')
                self.assertEqual(result['attempt'], 1)
                self.assertEqual(len(result['review_sessions']), 3)


if __name__ == '__main__':
    unittest.main()
