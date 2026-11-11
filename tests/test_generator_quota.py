"""The quota monitor uses account reads only, fails closed, and reaps its reader."""
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from generator_quota import fetch_quota, normalise_quota, QuotaUnavailable


def bucket(primary=20, secondary=60, **extra):
    return {'limitId': 'codex',
            'primary': {'usedPercent': primary, 'windowDurationMins': 300, 'resetsAt': 123},
            'secondary': {'usedPercent': secondary, 'windowDurationMins': 10080, 'resetsAt': 456},
            **extra}


class QuotaTests(unittest.TestCase):
    def test_both_windows_constrain_remaining_and_metadata_is_private(self):
        result = normalise_quota({'rateLimits': bucket(), 'accountId': 'secret',
                                  'ordinaryUsageAllowed': True}, checked_at=42)
        self.assertEqual(result['remaining_percent'], 40)
        self.assertEqual(result['checked_at'], 42)
        self.assertEqual([w['reset_at'] for w in result['windows']], [123, 456])
        self.assertNotIn('secret', json.dumps(result))
        self.assertFalse(result['exhausted'])

    def test_model_specific_bucket_applies_but_unrelated_model_does_not(self):
        result = normalise_quota({'rateLimits': bucket(), 'rateLimitsByLimitId': {
            'codex': bucket(10, 20),
            'other': bucket(100, 100, normalModelSlug='different-model'),
            'generator': bucket(75, 90, normalModelSlug='gpt-6.1-sol')}})
        self.assertEqual(result['remaining_percent'], 10)
        self.assertEqual(len(result['windows']), 4)
        self.assertFalse(any(w['name'].startswith('other') for w in result['windows']))
        with self.assertRaises(QuotaUnavailable):
            normalise_quota({'rateLimits': bucket(limitId='other', normalModelSlug='different-model')})

    def test_individual_spend_limit_and_explicit_denial_are_respected(self):
        result = normalise_quota({'ordinaryUsageAllowed': False, 'rateLimits': bucket(
            individualLimit={'remainingPercent': 12, 'resetsAt': 789})})
        self.assertEqual(result['remaining_percent'], 12)
        self.assertTrue(result['exhausted'])
        self.assertTrue(normalise_quota({'rateLimits': bucket(spendControlReached=True)})['exhausted'])
        self.assertIsNone(normalise_quota({'rateLimits': bucket()})['ordinary_usage_allowed'])

    def test_unknown_or_invalid_percentages_are_not_fabricated(self):
        for payload in ({}, {'rateLimits': {}}, {'rateLimits': bucket(primary=True)},
                        {'rateLimits': bucket(primary=float('nan'))}, {'rateLimits': bucket(primary=-1)},
                        {'rateLimitsByLimitId': []},
                        {'rateLimits': bucket(), 'rateLimitsByLimitId': []}):
            with self.subTest(payload=payload), self.assertRaises(QuotaUnavailable):
                normalise_quota(payload)
        self.assertEqual(normalise_quota({'rateLimits': bucket(primary=110)})['remaining_percent'], 0)

    def fake_reader(self, directory, action):
        path = directory / 'codex'
        path.write_text(f'#!{sys.executable}\n' + '''import json, os, sys, time
from pathlib import Path
root = Path(__file__).parent
(root / 'pid').write_text(str(os.getpid()))
with (root / 'requests').open('w') as requests:
    for line in sys.stdin:
        requests.write(line); requests.flush()
        message = json.loads(line)
        if message['method'] == 'initialize':
            print(json.dumps({'method': 'notification'}) + '\\n' + json.dumps({'id': 1, 'result': {}}), flush=True)
        elif message['method'] == 'account/rateLimits/read':
''' + '\n'.join('            ' + line for line in action.splitlines()) + '\n')
        path.chmod(0o755)
        return path

    def test_rpc_has_no_thread_or_turn_and_normalises_actual_payload(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            executable = self.fake_reader(root,
                "print(json.dumps({'id': 2, 'result': " + repr({'rateLimits': bucket()}) + "}), flush=True)")
            result = fetch_quota(executable=executable, timeout=3)
            self.assertEqual(result['remaining_percent'], 40)
            requests = [json.loads(line) for line in (root / 'requests').read_text().splitlines()]
            self.assertEqual([r['method'] for r in requests],
                             ['initialize', 'initialized', 'account/rateLimits/read'])
            self.assertEqual(requests[-1]['params'], {'excludeResetCreditDetails': True})
            self.assert_reaped(root)

    def assert_reaped(self, root):
        with self.assertRaises(ProcessLookupError):
            os.kill(int((root / 'pid').read_text()), 0)

    def test_timeout_error_eof_and_invalid_json_all_reap_process(self):
        actions = ['time.sleep(10)', 'sys.exit(0)', "print('not json', flush=True)",
                   "print(json.dumps({'id': 2, 'error': {'message': 'secret-token'}}), flush=True)"]
        for action in actions:
            with self.subTest(action=action), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                executable = self.fake_reader(root, action)
                start = time.monotonic()
                with self.assertRaises(QuotaUnavailable) as error:
                    fetch_quota(executable=executable, timeout=0.2)
                self.assertNotIn('secret-token', str(error.exception))
                self.assertLess(time.monotonic() - start, 3)
                self.assert_reaped(root)


if __name__ == '__main__':
    unittest.main()
