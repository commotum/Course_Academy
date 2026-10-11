import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from scripts.activity.solver import SolverClient, SolverUnavailable, validate_result
from scripts.config import Config


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
