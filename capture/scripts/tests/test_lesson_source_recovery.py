"""A broken supplementary topic page must not pin completed task history."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import MagicMock, patch

from scripts.activity import ActivityCapture
from scripts.browser.adapter import (
    BrowserUnavailable, MathAcademyBrowser, SourceHTTPError, SourceUnavailable,
)
from scripts.config import Config
from scripts.runtime import StopRequested
from scripts.tests.test_activity_capture import Agent, Browser, question


class LessonSourceRecoveryTests(unittest.TestCase):
    activity = {'task_id': '99', 'kind': 'lesson', 'topic_id': '7',
                'title': 'Sample', 'details': {}}
    url = 'https://mathacademy.com/topics/7'

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name) / 'task'
        self.directory.mkdir()
        self.config = Config(repo_root=Path(self.temp.name), retry_delay=.001, seed=3)
        self.stop = threading.Event()
        self.adapter = self.make_adapter()

    def make_adapter(self):
        adapter = MathAcademyBrowser(self.config, self.stop)
        adapter.directory = self.directory
        adapter.state = {'task_id': '99'}
        adapter.page = MagicMock()
        adapter.context = MagicMock()
        adapter._check = MagicMock()
        adapter._pause = MagicMock()
        adapter._settle_content = MagicMock()

        def evidence(page, directory, name):
            path = Path(directory) / (name + '.html')
            path.write_text('<html>Captured source response</html>')
            return {'html_path': str(path)}

        adapter._evidence = MagicMock(side_effect=evidence)
        return adapter

    def fail_topic(self, adapter, error):
        def goto(url, page=None):
            if url == self.url:
                raise error
        adapter._goto = MagicMock(side_effect=goto)

    def test_server_failure_budget_survives_browser_recreation(self):
        self.fail_topic(self.adapter, SourceHTTPError(502, self.url))
        for attempts in (1, 2):
            with self.assertRaises(SourceHTTPError):
                self.adapter._lesson(self.activity, self.directory)
            saved = json.loads((self.directory / 'browser-state.json').read_text())
            self.assertEqual(saved['lesson_source_failures'][self.url]['attempts'], attempts)
            replacement = self.make_adapter()
            replacement.state = saved
            self.adapter = replacement
            self.fail_topic(self.adapter, SourceHTTPError(502, self.url))

        original_page = self.adapter.page
        result = self.adapter._lesson(self.activity, self.directory)
        definition = result['lesson_definition']
        self.assertFalse(definition['complete'])
        self.assertEqual(definition['steps'], [])
        issue = definition['issues'][0]
        self.assertEqual((issue['http_status'], issue['attempts']), (502, 3))
        self.assertEqual(issue['source_url'], self.url)
        self.assertTrue(Path(issue['source_file']).is_file())
        self.assertIs(self.adapter.page, original_page)
        self.adapter.context.new_page.return_value.close.assert_called_once()

        # The final source-review pass gets one fresh probe, without a new budget.
        result = self.adapter._lesson(self.activity, self.directory)
        self.assertEqual(result['lesson_definition']['issues'][0]['attempts'], 4)
        self.assertEqual(self.adapter._goto.call_count, 2)

    def test_successful_later_read_clears_failure_and_restores_definition(self):
        self.adapter.state['lesson_source_failures'] = {
            self.url: {'attempts': 3, 'first_failed_at': 10}}
        html = '''<h1 id="topicName">Sample</h1><div id="steps">
          <div class="step" stepid="71" steptype="tutorial" contentid="10">
          <span class="stepName">Introduction</span>Content</div></div>'''
        self.adapter.context.new_page.return_value.content.return_value = html
        self.adapter._goto = MagicMock()
        self.adapter._read = MagicMock(return_value={
            'problem': 'Content', 'html_path': '/source.html', 'errors': []})
        result = self.adapter._lesson(self.activity, self.directory)
        self.assertTrue(result['lesson_definition']['complete'])
        self.assertEqual(result['tutorials'][0]['math_academy_id'], 10)
        saved = json.loads((self.directory / 'browser-state.json').read_text())
        self.assertNotIn(self.url, saved['lesson_source_failures'])

    def test_account_failures_and_interruptions_never_become_source_omissions(self):
        errors = [SourceHTTPError(status, self.url) for status in (401, 403, 429)]
        errors += [BrowserUnavailable('Account access challenge'),
                   TimeoutError('Navigation timed out'), StopRequested()]
        for error in errors:
            with self.subTest(error=repr(error)):
                adapter = self.make_adapter()
                adapter.state['lesson_source_failures'] = {self.url: {'attempts': 20}}
                self.fail_topic(adapter, error)
                with self.assertRaises(type(error)):
                    adapter._lesson(self.activity, self.directory)
                self.assertEqual(adapter.state['lesson_source_failures'][self.url]['attempts'], 20)
                adapter._evidence.assert_not_called()
                adapter.context.new_page.return_value.close.assert_called_once()

    def test_explicit_missing_source_still_records_immediate_limitation(self):
        for status in (404, 410):
            with self.subTest(status=status):
                adapter = self.make_adapter()
                self.fail_topic(adapter, SourceUnavailable(f'Source page HTTP {status}: {self.url}'))
                definition = adapter._lesson(self.activity, self.directory)['lesson_definition']
                self.assertFalse(definition['complete'])
                self.assertIn(str(status), definition['issues'][0]['reason'])
                self.assertNotIn('lesson_source_failures', adapter.state)

    def test_goto_retains_typed_status_without_swallowing_error(self):
        adapter = self.make_adapter()
        adapter._wait_cooldown = MagicMock()
        for status in (401, 403, 429, 500, 502, 503):
            with self.subTest(status=status):
                adapter.page.goto.return_value.status = status
                with self.assertRaises(SourceHTTPError) as caught:
                    adapter._goto(self.url)
                self.assertEqual(caught.exception.http_status, status)
                self.assertEqual(caught.exception.request_url, self.url)

    def test_completed_history_is_judged_and_saved_after_bounded_topic_failures(self):
        self.fail_topic(self.adapter, SourceHTTPError(502, self.url))
        metadata = [{'dom_id': 'question-1', 'math_academy_id': 'q-1',
                     'grade': 'Correct', 'topic_id': '7', 'difficulty': 'easy',
                     'sequence_position': 1}]
        source_question = {**question(), 'worked_solution': 'The answer is 2.',
                           'html_path': '/history.html', 'assets': [], 'errors': []}
        self.adapter._read = MagicMock(side_effect=lambda *args, **kwargs: deepcopy(source_question))
        browser = Browser([], kind='lesson')
        browser.history = self.adapter.history
        waits = []
        capture = ActivityCapture(self.config, browser, self.stop,
                                  lambda _: {'course_topics': ['7'], 'graph': {}},
                                  solver=Agent(), sleeper=waits.append)
        with patch('scripts.browser.adapter.parse_history_metadata', return_value=metadata):
            content = capture.run(self.activity, self.directory)

        # Three failures close the first read; the final recovery pass probes once.
        topic_calls = [call for call in self.adapter._goto.call_args_list if call.args[0] == self.url]
        self.assertEqual(len(topic_calls), 4)
        self.assertEqual(len(waits), 2)
        self.assertTrue((self.directory / 'capture-complete.json').is_file())
        saved = json.loads((self.directory / 'history-content.json').read_text())
        self.assertEqual(saved['questions'][0]['math_academy_id'], 'q-1')
        self.assertEqual(saved['questions'][0]['worked_solution'], 'The answer is 2.')
        self.assertEqual(content['questions'][0]['answer_fields'][0]['correct_value'], '2')
        self.assertEqual(len(content['judgments']), 1)
        self.assertFalse(content['lesson_definition']['complete'])
        self.assertTrue(any('lesson_definition_complete' in issue.get('missing', [])
                            for issue in content['source_limitations']))
        self.assertEqual(browser.responses, [])
        self.assertEqual(browser.advances, 0)


if __name__ == '__main__':
    unittest.main()
