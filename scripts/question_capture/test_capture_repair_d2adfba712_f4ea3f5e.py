import json
import re
import unittest
from pathlib import Path
from unittest.mock import Mock

from playwright.sync_api import TimeoutError
from browser import CaptureBrowser

EVIDENCE = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/multivariable/14060920/diagnostics/1791492060679689046')


class SavedGatewayRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        html = (EVIDENCE / 'page.html').read_text()
        body = re.search(r'<body[^>]*>(.*?)</body>', html, re.S).group(1)
        cls.body = re.sub(r'<[^>]+>', '', body).strip()
        assert cls.body == '502 Bad Gateway'
        events = json.loads((EVIDENCE / 'browser-events.json').read_text())
        failures = [e for e in events if e.get('event') == 'http_error' and e.get('status') == 502]
        assert failures
        cls.url = failures[-1]['url']

    def reader(self, texts):
        reader = object.__new__(CaptureBrowser)
        reader.page = Mock()
        reader.page.url = self.url
        reader.page.locator.return_value.inner_text.side_effect = texts
        reader.check = Mock()
        reader.pacer = Mock()
        reader.navigate = Mock()
        return reader

    def test_original_readiness_failure(self):
        reader = self.reader([self.body])
        reader.page.wait_for_function.side_effect = TimeoutError('Timeout 45000ms exceeded')
        # Original readiness path waited only for activity controls.
        with self.assertRaises(TimeoutError):
            reader.page.wait_for_function('original activity readiness predicate')
        reader.navigate.assert_not_called()

    def test_saved_gateway_page_reloads_after_backoff(self):
        reader = self.reader([self.body, 'Restored activity'])
        reader.wait_activity_ready()
        reader.pacer.backoff.assert_called_once_with(1)
        reader.navigate.assert_called_once_with(self.url, force=True)
        reader.page.wait_for_function.assert_called_once()

    def test_repeated_gateway_pages_are_paced(self):
        reader = self.reader([self.body] * 4 + ['Restored activity'])
        reader.wait_activity_ready()
        self.assertEqual([c.args[0] for c in reader.pacer.backoff.call_args_list], [1, 2, 3, 4])
        self.assertEqual(reader.navigate.call_count, 4)
        reader.page.wait_for_function.assert_called_once()

    def test_ordinary_content_with_gateway_words_is_not_reloaded(self):
        reader = self.reader(['Question: explain a 502 Bad Gateway error'])
        reader.page.wait_for_function.side_effect = TimeoutError('Missing activity controls')
        with self.assertRaises(TimeoutError):
            reader.wait_activity_ready()
        reader.navigate.assert_not_called()
        self.assertEqual([c.args[0] for c in reader.pacer.backoff.call_args_list], [1, 2])
        self.assertEqual(reader.page.wait_for_function.call_count, 3)

    def test_access_block_or_stop_is_not_bypassed(self):
        reader = self.reader([self.body])
        reader.check.side_effect = KeyboardInterrupt('Stopped')
        with self.assertRaises(KeyboardInterrupt):
            reader.wait_activity_ready()
        reader.navigate.assert_not_called()
        reader.pacer.backoff.assert_not_called()


if __name__ == '__main__':
    unittest.main()
