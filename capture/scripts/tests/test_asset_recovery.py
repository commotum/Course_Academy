"""Offline regressions for original-byte recovery and delayed diagram drawing."""
import base64
import hashlib
from pathlib import Path
from types import SimpleNamespace
import tempfile
import threading
import unittest
from unittest.mock import Mock, patch

from scripts.browser.assets import AssetCapture, GRAPHIC_STATE
from scripts.runtime import StopRequested
from scripts.storage import atomic_json, read_json


PNG = b'\x89PNG\r\n\x1a\noriginal image payload'


def response(status=200, data=PNG):
    return SimpleNamespace(ok=status < 400, status=status, body=Mock(return_value=data),
                           headers={'content-type': 'image/png'}, url='https://mathacademy.com/image.png')


class AssetRecovery(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        self.browser = SimpleNamespace(config=SimpleNamespace(timeout_ms=1000, retry_delay=2),
            stop_event=threading.Event(), image_responses={}, context=SimpleNamespace(request=Mock()))
        self.capture = AssetCapture(self.browser)
        self.capture._sleep = Mock()
        self.url = 'https://mathacademy.com/image.png'

    def tearDown(self):
        self.temp.cleanup()

    def item(self):
        return {'problem': '![](@asset-0@)', 'assets': [{'tag': 'img', 'index': 0, 'source_url': self.url}]}

    def test_transient_http_retries_once_and_permanent_http_does_not(self):
        self.browser.context.request.get.side_effect = [response(503), response()]
        result = self.capture.collect(self.item(), None, self.directory, 'question')
        self.assertEqual(Path(result['assets'][0]['path']).read_bytes(), PNG)
        self.assertEqual(self.browser.context.request.get.call_count, 2)
        self.capture._sleep.assert_called_once_with(2)
        self.browser.context.request.get.reset_mock(side_effect=True)
        self.browser.context.request.get.return_value = response(404)
        item = self.item()
        item['assets'][0]['source_url'] += '?missing'
        result = self.capture.collect(item, None, self.directory, 'missing')
        self.assertIn('404', result['assets'][0]['unavailable'])
        self.browser.context.request.get.assert_called_once()

    def test_rate_limit_enters_shared_cooldown_before_retry(self):
        calls = []
        self.browser.safety = SimpleNamespace(response=lambda r: calls.append(('response', r.status)))
        self.browser._wait_cooldown = lambda: calls.append(('cooldown', None))
        self.browser.context.request.get.side_effect = [response(429), response()]
        self.capture.collect(self.item(), None, self.directory, 'question')
        self.assertEqual(calls, [('cooldown', None), ('response', 429), ('cooldown', None), ('response', 200)])

    def test_verified_manifest_survives_discarded_browser_response(self):
        self.browser.context.request.get.return_value = response()
        first = self.capture.collect(self.item(), None, self.directory, 'before')
        self.browser.context.request.get.reset_mock()
        self.browser.image_responses[self.url] = SimpleNamespace(body=Mock(side_effect=RuntimeError('discarded')))
        later = self.capture.collect(self.item(), None, self.directory, 'after')
        self.assertEqual(first['assets'][0]['path'], later['assets'][0]['path'])
        self.assertEqual(Path(later['assets'][0]['path']).read_bytes(), PNG)
        self.browser.context.request.get.assert_not_called()

    def test_corrupt_manifest_bytes_are_refetched(self):
        path = self.directory / 'assets' / (hashlib.sha256(PNG).hexdigest() + '.png')
        path.parent.mkdir()
        path.write_bytes(b'corruption')
        atomic_json(self.directory / 'assets/manifest.json', {self.url: {'path': str(path),
            'sha256': hashlib.sha256(PNG).hexdigest(), 'content_type': 'image/png', 'representation': 'original'}})
        self.browser.context.request.get.return_value = response()
        result = self.capture.collect(self.item(), None, self.directory, 'after')
        self.browser.context.request.get.assert_called_once()
        self.assertEqual(Path(result['assets'][0]['path']).read_bytes(), PNG)

    def test_original_download_survives_failed_dom_rendering(self):
        self.capture._rendered_assets = Mock(return_value={0: {'error': 'Image did not load'}})
        self.browser.context.request.get.return_value = response()
        result = self.capture.collect(self.item(), None, self.directory, 'question')
        self.assertEqual(Path(result['assets'][0]['path']).read_bytes(), PNG)
        self.assertEqual(result['assets'][0]['render_unavailable'], 'Image did not load')
        self.assertTrue(result['errors'])

    def test_unfinished_canvas_is_not_saved_as_valid_diagram(self):
        self.capture._rendered_assets = Mock(return_value={0: {'error': 'Graphic has not finished rendering'}})
        result = self.capture.collect({'assets': [{'tag': 'canvas', 'index': 0}]}, Mock(), self.directory, 'canvas')
        self.assertNotIn('path', result['assets'][0])
        self.assertIn('unavailable', result['assets'][0])

    def test_manual_stop_propagates_from_response_and_readiness(self):
        self.browser.image_responses[self.url] = SimpleNamespace(body=Mock(side_effect=StopRequested()))
        with self.assertRaises(StopRequested):
            self.capture.collect(self.item(), None, self.directory, 'question')
        with self.assertRaises(StopRequested):
            self.capture.collect(self.item(), SimpleNamespace(evaluate=Mock(side_effect=StopRequested())), self.directory, 'question')
        self.assertIsNone(read_json(self.directory / 'assets/manifest.json'))

    def test_delayed_canvas_requires_half_second_of_stable_pixels(self):
        now = [100.0]
        self.capture._sleep = lambda seconds: now.__setitem__(0, now[0] + seconds)
        def snapshot(*_, **__):
            elapsed = now[0] - 100
            return [{'index': 0, 'ready': elapsed >= .3,
                     'signature': 'drawn' if elapsed >= .3 else 'blank',
                     'encoded': 'data:image/png;base64,' + base64.b64encode(PNG).decode()}]
        with patch('scripts.browser.assets.time.monotonic', lambda: now[0]):
            result = self.capture._rendered_assets({'assets': [{'tag': 'canvas', 'index': 0}]}, SimpleNamespace(evaluate=snapshot))
        self.assertGreaterEqual(now[0] - 100, .8)
        self.assertTrue(result[0]['ready'])

    def test_graphic_wait_and_locator_timeout_respect_assessment_deadline(self):
        now = [100.0]
        self.browser.deadline_at = 100.25
        self.browser.pacer = SimpleNamespace(sleep=lambda seconds, **_: now.__setitem__(0, now[0] + seconds))
        capture = AssetCapture(self.browser)
        scope = SimpleNamespace(evaluate=Mock(return_value=[{'index': 0, 'ready': False}]))
        with patch('scripts.browser.assets.time.monotonic', lambda: now[0]), patch('scripts.browser.assets.time.time', lambda: now[0]):
            result = capture._rendered_assets({'assets': [{'tag': 'canvas', 'index': 0}]}, scope)
        self.assertLessEqual(now[0], self.browser.deadline_at)
        self.assertIn('error', result[0])
        self.assertTrue(all(call.kwargs['timeout'] <= 250 for call in scope.evaluate.call_args_list))

    def test_broken_image_uses_shared_backoff_then_a_fresh_readiness_window(self):
        now, sleeps = [100.0], []
        def sleep(seconds, **_):
            sleeps.append(seconds)
            now[0] += seconds
        self.browser.pacer = SimpleNamespace(sleep=sleep, backoff=Mock(return_value=30))
        node = Mock()
        scope = SimpleNamespace(evaluate=Mock(return_value=[{'index': 0, 'ready': False, 'broken': True}]),
                                locator=Mock(return_value=SimpleNamespace(nth=lambda _: node)))
        capture = AssetCapture(self.browser)
        with patch('scripts.browser.assets.time.monotonic', lambda: now[0]):
            capture._rendered_assets({'assets': [{'tag': 'img', 'index': 0}]}, scope)
        self.browser.pacer.backoff.assert_called_once_with(1)
        self.assertEqual(sleeps[0], 30)
        node.evaluate.assert_called_once()
        self.assertGreaterEqual(now[0], 131)
        self.assertLess(now[0], 131.2)


class GraphicDOM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise unittest.SkipTest('Playwright is required for offline DOM tests')
        cls.pw = sync_playwright().start()
        try:
            cls.browser = cls.pw.chromium.launch(headless=True)
        except Exception:
            cls.pw.stop()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def test_real_canvas_stays_unready_until_it_draws(self):
        context = self.browser.new_context()
        context.route('**/*', lambda route: route.abort())
        try:
            page = context.new_page()
            page.set_content('<div id="scope"><canvas width="20" height="20"></canvas></div>')
            scope = page.locator('#scope')
            targets = [{'tag': 'canvas', 'index': 0, 'dom_index': 0}]
            self.assertFalse(scope.evaluate(GRAPHIC_STATE, targets)[0]['ready'])
            page.evaluate("setTimeout(() => {const c=document.querySelector('canvas');c.getContext('2d').fillRect(2,2,5,5)}, 200)")
            capture = AssetCapture(SimpleNamespace(config=SimpleNamespace(timeout_ms=1500), stop_event=threading.Event()))
            state = capture._rendered_assets({'assets': targets}, scope)
            self.assertTrue(state[0]['ready'])
            self.assertTrue(state[0]['encoded'].startswith('data:image/png;base64,'))
        finally:
            context.close()


if __name__ == '__main__':
    unittest.main()
