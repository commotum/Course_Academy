import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from scripts.activity.solver import SolverClient, SolverUnavailable, validate_result
from scripts.config import Config
from scripts.runtime import StopRequested
from scripts.timing import Pacer


class SolverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = Config(repo_root=self.root, solver_timeout=10)
        self.stop = threading.Event()
        self.payload = {'question': {'problem': '1+1?', 'fields': [{'key': 'answer', 'type': 'blank'}]}}
        self.result = {'status': 'confirmed', 'reasoning': 'One plus one is two.', 'answers': [
            {'key': 'answer', 'correct_value': '2', 'ma_basis': 'none', 'correct_keys': [], 'wrong_keys': []}]}

    def test_external_command_receives_task_and_durable_context_and_returns_session(self):
        script = "import json,sys; x=json.load(sys.stdin); print(json.dumps({'session_id':'same-session','result':{'status':'confirmed','reasoning':str(len(x.get('conversation',[]))), 'answers':[{'key':'answer','correct_value':'2','ma_basis':'none'}]}}))"
        self.config.solver_command = [sys.executable, '-c', script]
        client = SolverClient(self.config, self.root, self.stop)
        first = client.request('solve_question', self.payload)
        second = client.request('judge_question', self.payload)
        self.assertEqual((first['reasoning'], second['reasoning']), ('0', '1'))
        self.assertEqual(client.state['session_id'], 'same-session')
        with patch.object(client, '_call', side_effect=AssertionError('cached turn must not invoke agent')):
            self.assertEqual(client.request('judge_question', self.payload), second)
        self.assertEqual(len(client.state['turns']), 2)

    def test_codex_initial_readonly_and_explicit_session_resume(self):
        commands = []
        def fake_process(command, prompt, prefix, timeout):
            commands.append(command)
            return '\n'.join([json.dumps({'type': 'thread.started', 'thread_id': 'saved-id'}),
                              json.dumps({'type': 'item.completed', 'item': {'type': 'agent_message', 'text': json.dumps(self.result)}})])
        client = SolverClient(self.config, self.root, self.stop)
        with patch.object(client, '_process', side_effect=fake_process):
            client.request('solve_question', self.payload)
            client.request('judge_question', self.payload)
        self.assertIn('read-only', commands[0])
        self.assertEqual(commands[1][1:4], ['exec', 'resume', 'saved-id'])
        self.assertNotIn('--last', commands[1])

    def test_failed_session_is_replaced_with_context(self):
        client = SolverClient(self.config, self.root, self.stop)
        results = [(self.result, 'first'), SolverUnavailable('Session expired'), (self.result, 'replacement')]
        envelopes = []
        def fake_call(envelope, *args):
            envelopes.append(envelope)
            value = results.pop(0)
            if isinstance(value, Exception):
                raise value
            return value
        with patch.object(client, '_call', side_effect=fake_call):
            client.request('solve_question', self.payload)
            client.request('judge_question', self.payload)
        self.assertEqual(envelopes[1]['session_id'], 'first')
        self.assertIsNone(envelopes[2]['session_id'])
        self.assertEqual(len(envelopes[2]['conversation']), 1)

    def test_invalid_confirmed_answer_requires_replacement(self):
        client = SolverClient(self.config, self.root, self.stop)
        bad = {'status': 'confirmed', 'reasoning': 'Missing all required fields', 'answers': []}
        with patch.object(client, '_call', side_effect=[(bad, 'bad'), (self.result, 'good')]) as invoke:
            self.assertEqual(client.request('solve_question', self.payload), self.result)
        self.assertEqual(invoke.call_count, 2)

    def test_invented_worked_example_field_replaces_session(self):
        client = SolverClient(self.config, self.root, self.stop)
        example = {'question': {'problem': 'Worked example: one plus one is two.', 'fields': []}}
        verified = {**self.result, 'answers': []}
        envelopes = []
        results = [(self.result, 'first'), (self.result, 'first'), (verified, 'replacement')]
        def call(envelope, *args):
            envelopes.append(envelope)
            return results.pop(0)
        with patch.object(client, '_call', side_effect=call):
            client.request('solve_question', self.payload)
            self.assertEqual(client.request('judge_question', example), verified)
        self.assertEqual(envelopes[1]['session_id'], 'first')
        self.assertIsNone(envelopes[2]['session_id'])
        self.assertEqual(client.state['generation'], 1)

    def test_rejected_remote_compaction_replaces_session_with_answer_context(self):
        client = SolverClient(self.config, self.root, self.stop)
        envelopes = []
        results = [(self.result, 'broken'), SolverUnavailable(
            'Error running remote compact task: {"detail":"Bad Request"}'), (self.result, 'fresh')]
        def call(envelope, *args):
            envelopes.append(envelope)
            result = results.pop(0)
            if isinstance(result, Exception):
                raise result
            return result
        with patch.object(client, '_call', side_effect=call):
            client.request('solve_question', self.payload)
            client.request('judge_question', self.payload)
        self.assertEqual(envelopes[1]['session_id'], 'broken')
        self.assertIsNone(envelopes[2]['session_id'])
        self.assertEqual(envelopes[2]['conversation'][0]['answers'][0]['correct_value'], '2')

    def test_topic_catalog_delivered_once_per_session_and_refreshed_when_changed(self):
        client = SolverClient(self.config, self.root, self.stop)
        envelopes = []
        def classify(envelope, *args):
            envelopes.append(envelope)
            return {'topic_id': '2', 'confidence': 1, 'reasoning': 'Exact candidate skill'}, 'same'
        topics = [{'topic_id': '2', 'title': 'Addition'}]
        with patch.object(client, '_call', side_effect=classify):
            client.request('match_topic', {'question': {'problem': 'Add 1+1'}, 'topics': topics})
            client.request('match_topic', {'question': {'problem': 'Add 2+2'}, 'topics': topics})
            client.request('match_topic', {'question': {'problem': 'Add 3+3'}, 'topics': topics + [{'topic_id': '3', 'title': 'Subtraction'}]})
            client.request('match_topic', {'question': {'problem': 'Add 4+4'}, 'topics': topics}, force_new=True)
        self.assertIn('topics', envelopes[0]['payload'])
        self.assertNotIn('topics', envelopes[1]['payload'])
        self.assertTrue(envelopes[1]['payload']['topic_catalog_reused'])
        self.assertIn('topics', envelopes[2]['payload'])
        self.assertIn('topics', envelopes[3]['payload'])
        self.assertIsNone(envelopes[3]['session_id'])

    def test_legacy_raw_capture_session_is_rotated_once_with_results_preserved(self):
        directory = self.root / 'solver'
        directory.mkdir()
        (directory / 'session.json').write_text(json.dumps({'session_id': 'legacy', 'turns': ['old'], 'generation': 3}))
        old = directory / 'old'
        old.mkdir()
        (old / 'request.json').write_text(json.dumps({'task': 'solve_question', 'payload': {
            **self.payload, 'instructional_content': [{'html': 'raw oversized lessons'}]}}))
        (old / 'result.json').write_text(json.dumps(self.result))
        client = SolverClient(self.config, self.root, self.stop)
        self.assertIsNone(client.state['session_id'])
        self.assertEqual(client.state['generation'], 4)
        self.assertEqual(client.state['retired_sessions'][0]['session_id'], 'legacy')
        self.assertEqual(client._conversation('judge_question', self.payload)[0]['answers'][0]['correct_value'], '2')
        self.assertEqual(json.loads((old / 'result.json').read_text()), self.result)
        with patch.object(client, '_call', return_value=(self.result, 'healthy')):
            client.request('judge_question', self.payload)
        resumed = SolverClient(self.config, self.root, self.stop)
        self.assertEqual(resumed.state['session_id'], 'healthy')
        self.assertEqual(resumed.state['generation'], 4)
        self.assertEqual(len(resumed.state['retired_sessions']), 1)

    def test_transient_failure_preserves_the_activity_session(self):
        client = SolverClient(self.config, self.root, self.stop)
        envelopes = []
        values = [(self.result, 'same'), SolverUnavailable('Temporary service outage'), (self.result, 'same')]
        def fake_call(envelope, *args):
            envelopes.append(envelope)
            result = values.pop(0)
            if isinstance(result, Exception):
                raise result
            return result
        with patch.object(client, '_call', side_effect=fake_call):
            client.request('solve_question', self.payload)
            client.request('judge_question', self.payload)
        self.assertEqual(envelopes[1]['session_id'], 'same')
        self.assertEqual(envelopes[2]['session_id'], 'same')
        self.assertNotIn('conversation', envelopes[2])

    def test_deterministic_failure_is_not_relaunched_until_dependency_changes(self):
        client = SolverClient(self.config, self.root, self.stop)
        failure = SolverUnavailable('invalid CLI option', retryable=False)
        with patch.object(client, '_call', side_effect=failure) as invoke:
            for _ in range(2):
                with self.assertRaises(SolverUnavailable) as raised:
                    client.request('solve_question', self.payload)
                self.assertFalse(raised.exception.retryable)
            self.assertEqual(invoke.call_count, 1)
        self.config.codex_bin = str(self.root / 'repaired-cli')
        (self.root / 'repaired-cli').write_text('repaired dependency')
        with patch.object(client, '_call', return_value=(self.result, 'new')) as invoke:
            self.assertEqual(client.request('solve_question', self.payload), self.result)
            self.assertEqual(invoke.call_count, 1)

    def test_replacement_context_contains_no_unrelated_raw_requests(self):
        client = SolverClient(self.config, self.root, self.stop)
        with patch.object(client, '_call', return_value=(self.result, 'session')):
            client.request('solve_question', {**self.payload, 'instructional_content': [{'html': 'raw tutorial'}]})
        context = client._conversation('judge_question', self.payload)
        self.assertEqual(context[0]['answers'][0]['correct_value'], '2')
        self.assertNotIn('request', context[0])
        self.assertNotIn('raw tutorial', json.dumps(context))
        self.assertEqual(client._conversation('solve_question', {'question': {'problem': 'Different question'}}), [])

    def test_agent_cannot_submit_via_typing_keys(self):
        result = {**self.result, 'answers': [{'key': 'answer', 'correct_keys': [{'key': 'Enter', 'text': None}]}]}
        with self.assertRaises(ValueError):
            validate_result('solve_question', self.payload, result)

    def test_topic_classification_rejects_invented_ids(self):
        with self.assertRaises(ValueError):
            validate_result('match_topic', {'topics': [{'topic_id': '2'}]}, {'topic_id': '99'})

    def test_final_unavailable_is_a_valid_agent_judgment(self):
        validate_result('judge_question', self.payload,
                        {'status': 'unavailable', 'reasoning': 'The diagram is unavailable and determines the answer.', 'answers': []})

    def test_first_attempt_has_full_deadline_budget(self):
        self.config.solver_timeout = 300
        client = SolverClient(self.config, self.root, self.stop)
        with patch.object(client, '_call', return_value=(self.result, 'same')) as invoke:
            client.request('solve_question', self.payload)
        self.assertGreater(invoke.call_args.args[-1], 299)

    def test_capacity_recovery_waits_then_resumes_same_session(self):
        now = [1000.0]
        def sleep(seconds):
            now[0] += seconds
        self.config.solver_timeout = 100
        self.config.capacity_min = self.config.capacity_max = 30
        pacer = Pacer(self.config, self.stop, clock=lambda: now[0], sleeper=sleep)
        client = SolverClient(self.config, self.root, self.stop, pacer=pacer)
        client.state['session_id'] = 'same'
        calls = []
        def invoke(envelope, prefix, schema, timeout):
            calls.append((envelope['session_id'], now[0], timeout))
            if len(calls) == 1:
                raise SolverUnavailable('Selected model is at capacity. Please try a different model.')
            return self.result, 'same'
        with patch('scripts.activity.solver.time.monotonic', side_effect=lambda: now[0]), patch.object(client, '_call', side_effect=invoke):
            self.assertEqual(client.request('solve_question', self.payload), self.result)
        self.assertEqual(calls, [('same', 1000, 100), ('same', 1030, 70)])

    def test_capacity_wait_is_bounded_by_short_assessment_budget(self):
        now = [1000.0]
        def sleep(seconds):
            now[0] += seconds
        pacer = Pacer(self.config, self.stop, clock=lambda: now[0], sleeper=sleep)
        client = SolverClient(self.config, self.root, self.stop, pacer=pacer)
        with patch('scripts.activity.solver.time.monotonic', side_effect=lambda: now[0]), patch.object(client, '_call', side_effect=SolverUnavailable('Model is at capacity')) as invoke:
            with self.assertRaises(SolverUnavailable):
                client.request('solve_question', self.payload, timeout=4)
        self.assertEqual(now[0], 1004)
        self.assertEqual(invoke.call_count, 1)

    def test_capacity_gets_two_retries_but_other_failures_keep_configured_limit(self):
        self.config.capacity_min = self.config.capacity_max = 0
        client = SolverClient(self.config, self.root, self.stop)
        with patch.object(client, '_call', side_effect=[SolverUnavailable('Model at capacity'),
                SolverUnavailable('Model at capacity'), (self.result, 'same')]) as invoke:
            self.assertEqual(client.request('solve_question', self.payload), self.result)
        self.assertEqual(invoke.call_count, 3)
        with patch.object(client, '_call', side_effect=SolverUnavailable('Temporary transport error')) as invoke:
            with self.assertRaises(SolverUnavailable):
                client.request('judge_question', self.payload)
        self.assertEqual(invoke.call_count, 2)

    def test_capacity_wait_stop_retains_cooldown_for_resume(self):
        now = [1000.0]
        def stop_sleep(seconds):
            now[0] += seconds
            self.stop.set()
        self.config.solver_timeout = 100
        self.config.capacity_min = self.config.capacity_max = 30
        pacer = Pacer(self.config, self.stop, clock=lambda: now[0], sleeper=stop_sleep)
        client = SolverClient(self.config, self.root, self.stop, pacer=pacer)
        with patch.object(client, '_call', side_effect=SolverUnavailable('Model is at capacity')):
            with self.assertRaises(StopRequested):
                client.request('solve_question', self.payload)
        self.stop.clear()
        pacer.sleeper = lambda seconds: now.__setitem__(0, now[0] + seconds)
        resumed = SolverClient(self.config, self.root, self.stop, pacer=pacer)
        with patch.object(resumed, '_call', return_value=(self.result, 'same')):
            self.assertEqual(resumed.request('solve_question', self.payload), self.result)
        self.assertEqual(now[0], 1030)

    def test_unknown_page_can_only_select_exact_observed_current_control(self):
        payload = {'observation': {'kind': 'unknown', 'buttons': [{'selector': '#continue', 'text': 'Continue'}]}}
        result = {'action': 'advance', 'reasoning': 'Continue the current activity.',
                  'button_selector': '#continue', 'button_text': 'Continue'}
        validate_result('interpret_page', payload, result)
        for change in ({'button_selector': 'body button'}, {'button_text': 'Start'}, {'button_selector': None, 'button_text': None}):
            with self.assertRaises(ValueError):
                validate_result('interpret_page', payload, {**result, **change})

    def test_unknown_page_cannot_select_abandon_logout_or_queue_control(self):
        for text in ('Abandon activity', 'Log out', 'Return to queue', 'Cancel'):
            payload = {'observation': {'kind': 'unknown', 'buttons': [{'selector': '#button', 'text': text}]}}
            with self.assertRaises(ValueError):
                validate_result('interpret_page', payload, {'action': 'advance', 'reasoning': 'Incorrect proposed recovery',
                    'button_selector': '#button', 'button_text': text})


if __name__ == '__main__':
    unittest.main()
