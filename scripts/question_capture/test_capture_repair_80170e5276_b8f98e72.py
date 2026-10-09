import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, call
from playwright.sync_api import TimeoutError as PlaywrightTimeout
from browser import CaptureBrowser, ACTIVE_STEP

EVIDENCE = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/differential/14060230/diagnostics/1791492066641444931')

class ReviewReadinessRetryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((EVIDENCE / 'error.json').read_text())
        events = json.loads((EVIDENCE / 'browser-events.json').read_text())
        cls.html = (EVIDENCE / 'page.html').read_text()
        if not any(e.get('status') == 502 and e.get('url', '').endswith('/api/tasks/14060230/review/6680/state') for e in events):
            raise AssertionError('Missing saved review-state outage')
        if 'id="stepButton-q332850" class="stepButton current"' not in cls.html:
            raise AssertionError('Missing saved placeholder navigation')

    def reader(self, outcomes):
        page = Mock()
        page.locator.return_value.inner_text.return_value = ' '.join(self.html.split())
        page.wait_for_function.side_effect = outcomes
        return SimpleNamespace(page=page, pacer=Mock(), check=Mock(), navigate=Mock())

    def test_original_single_wait_failure(self):
        reader = self.reader([PlaywrightTimeout(self.report['message'])])
        with self.assertRaises(PlaywrightTimeout):
            reader.page.wait_for_function('() => !!('+ACTIVE_STEP+')() || ' +
                "!!document.querySelector('#finalScreen')?.getClientRects().length")

    def test_transient_outage_recovers(self):
        reader = self.reader([PlaywrightTimeout(self.report['message']), None])
        CaptureBrowser.wait_activity_ready(reader)
        reader.pacer.backoff.assert_called_once_with(1)
        reader.page.reload.assert_called_once_with(wait_until='domcontentloaded')
        self.assertEqual(reader.check.call_count, 2)
        self.assertEqual(reader.page.wait_for_function.call_count, 2)
        calls = reader.page.wait_for_function.call_args_list
        self.assertEqual(calls[0], calls[1])
        self.assertIn(ACTIVE_STEP, calls[0].args[0])
        reader.navigate.assert_not_called()

    def test_persistent_empty_page_still_fails(self):
        reader = self.reader([PlaywrightTimeout(self.report['message']) for _ in range(3)])
        with self.assertRaises(PlaywrightTimeout):
            CaptureBrowser.wait_activity_ready(reader)
        self.assertEqual(reader.page.wait_for_function.call_count, 3)
        self.assertEqual(reader.pacer.backoff.call_args_list, [call(1), call(2)])
        self.assertEqual(reader.page.reload.call_count, 2)

    def test_non_timeout_is_not_retried(self):
        reader = self.reader([ValueError('invalid readiness evaluation')])
        with self.assertRaisesRegex(ValueError, 'invalid readiness evaluation'):
            CaptureBrowser.wait_activity_ready(reader)
        reader.page.reload.assert_not_called()
        reader.pacer.backoff.assert_not_called()

    def test_access_failure_after_reload_stops(self):
        reader = self.reader([PlaywrightTimeout(self.report['message']), None])
        reader.check.side_effect = [None, RuntimeError('authentication challenge')]
        with self.assertRaisesRegex(RuntimeError, 'authentication challenge'):
            CaptureBrowser.wait_activity_ready(reader)
        self.assertEqual(reader.page.wait_for_function.call_count, 1)

if __name__ == '__main__':
    unittest.main()
