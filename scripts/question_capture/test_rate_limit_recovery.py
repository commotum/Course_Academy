"""Throttling paces read-only retries and restores ambiguous submissions."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from browser import AccessBlocked, CaptureBrowser, RateLimited
from capture import arguments
import test_adaptive_run as adaptive


class RateLimitTests(unittest.TestCase):
    def reader(self):
        page = Mock()
        page.url = 'https://mathacademy.com/learn'
        page.locator.return_value.count.return_value = 0
        return CaptureBrowser(page, SimpleNamespace(timeout_ms=1000), Mock(), None)

    def response(self, code, delay='90'):
        response = Mock()
        response.url = 'https://mathacademy.com/learn'
        response.status = code
        response.ok = code == 200
        response.request.resource_type = 'document'
        response.request.redirected_from = None
        response.header_value.return_value = delay
        return response

    def test_navigation_honors_throttle_without_access_stop_or_clicks(self):
        reader = self.reader()
        replies = iter([self.response(429), self.response(200)])
        def navigate(*_, **__):
            response = next(replies)
            reader._observe_response(response)
            return response
        reader.page.goto.side_effect = navigate
        reader.navigate('https://mathacademy.com/learn', force=True)
        self.assertEqual(reader.page.goto.call_count, 2)
        reader.pacer.backoff.assert_called_once_with(1, retry_after=90)
        reader.page.locator.return_value.click.assert_not_called()
        self.assertIsNone(reader.http_block)

    def test_authentication_remains_blocking_and_foreign_throttle_is_ignored(self):
        reader = self.reader()
        for status in (401, 403):
            reader._observe_response(self.response(status))
            with self.assertRaises(AccessBlocked):
                reader.check()
        reader.http_block = None
        response = self.response(429)
        response.url = 'https://other.invalid/asset'
        reader._observe_response(response)
        reader.check()

    def test_bad_retry_header_uses_default_and_stop_interrupts_before_retry(self):
        reader = self.reader()
        reader._observe_response(self.response(429, 'nan'))
        with self.assertRaises(RateLimited) as raised:
            reader.check()
        self.assertEqual(raised.exception.retry_after, 30)
        reader.args.stop_event = Mock(is_set=Mock(return_value=True))
        with self.assertRaises(KeyboardInterrupt):
            reader.check()

    def test_ambiguous_submission_restores_checkpoint_without_restart_or_repair(self):
        helper = adaptive.AdaptiveRunTests()
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            args = arguments(['run', '--state-dir', str(root/'state'),
                              '--output', str(root/'capture'), '--limit', '2',
                              '--lesson-min', '0', '--lesson-max', '0'])
            fixture = helper.fixture(work, [1])
            browser = fixture[0]
            original = browser.activity
            calls = []
            navigations = []
            def activity(self, state, *values):
                calls.append(state['task_id'])
                if len(calls) == 1:
                    state['questions']['q-1'] = {'status': 'submitting'}
                    raise RateLimited(0)
                self.assert_restored = state['questions']['q-1']['status']
                original(self, state, *values)
                from core import atomic_json
                atomic_json(values[0]/'state.json', state)
            browser.activity = activity
            browser.navigate = lambda self, *a, **kw: navigations.append((a, kw))
            # Pacing is injectable, while the runner's checkpoints stay real.
            from unittest.mock import patch
            with patch('core.Pacer.backoff') as backoff:
                selected, cooldown = helper.execute(args, fixture)
            self.assertEqual(selected, [1])
            self.assertEqual(calls, [1, 1])
            self.assertEqual(len(navigations), 1)
            self.assertTrue(navigations[0][1]['force'])
            saved = json.loads((root/'capture/1/state.json').read_text())
            self.assertEqual(saved['questions']['q-1']['status'], 'submitting')
            self.assertTrue(saved['activity_complete'])
            backoff.assert_called_once_with(1, retry_after=0)
            cooldown.assert_not_called()


if __name__ == '__main__':
    unittest.main()
