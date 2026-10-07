"""Network recovery retries navigation and finishes failed intercepted requests."""
import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from playwright.sync_api import Error, sync_playwright
from browser import CaptureBrowser, repair_math_editor_document


class NetworkRecoveryTests(unittest.TestCase):
    def reader(self, page):
        reader = object.__new__(CaptureBrowser)
        reader.page, reader.pacer, reader.check = page, Mock(), Mock()
        return reader

    def test_dns_route_failure_aborts_without_logging_headers(self):
        route = Mock()
        route.request.resource_type, route.request.method = 'document', 'GET'
        route.fetch.side_effect = Error('Route.fetch: getaddrinfo EAI_AGAIN mathacademy.com\n - cookie: private-test-value')
        with self.assertLogs(level='WARNING') as logs:
            repair_math_editor_document(route)
        route.abort.assert_called_once_with('connectionfailed')
        self.assertNotIn('private-test-value', '\n'.join(logs.output))
        self.assertIn('EAI_AGAIN', '\n'.join(logs.output))
        route.fetch.assert_called_once_with(max_redirects=0, timeout=30000)

    def test_closed_route_does_not_escape_callback(self):
        route = Mock()
        route.request.resource_type, route.request.method = 'document', 'GET'
        route.fetch.side_effect = Error('getaddrinfo EAI_AGAIN')
        route.abort.side_effect = Error('Target closed')
        with self.assertLogs(level='WARNING'):
            repair_math_editor_document(route)

    def test_more_than_three_dns_failures_can_recover(self):
        page = Mock()
        page.url = 'about:blank'
        response = SimpleNamespace(status=200, request=SimpleNamespace(redirected_from=None))
        page.goto.side_effect = [Error('net::ERR_NAME_NOT_RESOLVED')] * 4 + [response]
        reader = self.reader(page)
        with self.assertLogs(level='WARNING'):
            reader.navigate('https://mathacademy.com/learn', force=True)
        self.assertEqual(page.goto.call_count, 5)
        self.assertEqual([c.args[0] for c in reader.pacer.backoff.call_args_list], [1, 2, 3, 4])
        page.locator.return_value.first.wait_for.assert_called_once_with(state='visible')

    def test_unrelated_error_is_not_retried(self):
        page = Mock()
        page.goto.side_effect = Error('Invalid URL')
        reader = self.reader(page)
        with self.assertRaises(Error):
            reader.navigate('invalid', force=True)
        reader.pacer.backoff.assert_not_called()

    def test_stop_interrupts_network_recovery(self):
        page = Mock()
        page.goto.side_effect = Error('net::ERR_NAME_NOT_RESOLVED')
        reader = self.reader(page)
        reader.check.side_effect = KeyboardInterrupt('Stopped')
        with self.assertRaises(KeyboardInterrupt):
            reader.navigate('https://mathacademy.com/learn', force=True)
        reader.pacer.backoff.assert_not_called()

    def test_http_503_recovers_after_more_than_three_attempts(self):
        page = Mock()
        page.goto.side_effect = [SimpleNamespace(status=n, request=SimpleNamespace(redirected_from=None))
                                 for n in [503, 503, 503, 503, 200]]
        reader = self.reader(page)
        with self.assertLogs(level='WARNING'):
            reader.navigate('https://mathacademy.com/learn', force=True)
        self.assertEqual(page.goto.call_count, 5)
        self.assertEqual(reader.pacer.backoff.call_count, 4)

    def test_real_browser_failed_route_releases_navigation(self):
        # All requests are intercepted locally; this test never contacts MA.
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            pacer, attempts = Mock(), []
            def handler(route):
                attempts.append(route.request.url)
                if len(attempts) == 1:
                    proxy = Mock(wraps=route)
                    proxy.request = route.request
                    proxy.fetch.side_effect = Error('Route.fetch: getaddrinfo EAI_AGAIN mathacademy.com')
                    repair_math_editor_document(proxy)
                else:
                    route.fulfill(status=200, content_type='text/html', body='<body>Recovered queue</body>')
            context.route('http://network-test.invalid/**', handler)
            try:
                reader = CaptureBrowser(page, SimpleNamespace(timeout_ms=2000), pacer, None)
                reader.navigate('http://network-test.invalid/learn', force=True)
                self.assertEqual(page.locator('body').inner_text(), 'Recovered queue')
                self.assertEqual(len(attempts), 2)
                pacer.backoff.assert_called_once_with(1)
            finally:
                context.close()
                browser.close()


if __name__ == '__main__':
    unittest.main()
