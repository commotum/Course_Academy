"""Failures must preserve decisions and escalate without abandoning an activity."""
from copy import deepcopy
from pathlib import Path
import tempfile
import threading
import unittest

from scripts.activity.capture import ActivityCapture
from scripts.activity.policy import AnswerPolicy
from scripts.config import Config
from scripts.storage import read_json
from scripts.tests.test_activity_capture import Agent, Browser, question


class ActivityRecoveryRegressions(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.now = 1000.0
        self.delays = []
        self.stop = threading.Event()
        self.config = Config(repo_root=self.root, seed=17, recovery_jitter=0)

    def sleep(self, seconds):
        self.delays.append(seconds)
        self.now += seconds

    def capture(self, browser=None, kind='review', details=None):
        capture = ActivityCapture(self.config, browser or Browser([]), self.stop,
                                  solver=Agent(), clock=lambda: self.now, sleeper=self.sleep)
        capture.activity = {'task_id': '99', 'kind': kind, 'details': details or {}}
        capture.directory = self.root / 'task'
        capture.directory.mkdir(exist_ok=True)
        capture.checkpoint_path = capture.directory / 'checkpoint.json'
        capture.state = {'stage': 'activity', 'recoveries': 0, 'presentations': {}, 'steps': [],
                         'policy': {}, 'judgments': {}, 'activity': capture.activity}
        capture.policy = AnswerPolicy(capture.activity, capture.state['policy'], rng=capture.rng,
                                      clock=lambda: self.now)
        return capture

    def test_unchanged_accepted_question_preserves_continue_failures_across_resume(self):
        class BrokenContinue(Browser):
            def advance(self, *args):
                raise TimeoutError('Continue control did not advance')
        browser = BrokenContinue([question()])
        browser.accepted = True
        capture = self.capture(browser)
        for attempt in range(1, 4):
            observation = capture._browser_call('observe', capture.directory)
            capture._browser_call('advance', observation, capture.directory)
            capture._browser_call('observe', capture.directory)
            self.assertEqual(capture.state['pending_browser_error']['attempt'], attempt)
        restored = self.capture(browser)
        restored.state = read_json(capture.checkpoint_path)
        observation = restored._browser_call('observe', restored.directory)
        restored._browser_call('advance', observation, restored.directory)
        self.assertEqual(self.delays, [30, 60, 90, 120])
        self.assertEqual(restored.state['pending_browser_error']['attempt'], 4)

    def test_continue_failure_uses_agent_recovery_and_restarts_same_activity(self):
        class RecoverableContinue(Browser):
            def __init__(self):
                super().__init__([question()])
                self.accepted = True
                self.restarts = 0

            def advance(self, *args):
                self.advances += 1
                raise TimeoutError('Continue control did not advance')

            def restart(self):
                self.restarts += 1
                self.index = len(self.questions)
        browser = RecoverableContinue()
        capture = self.capture(browser)
        capture._execute()
        self.assertEqual(browser.advances, 3)
        self.assertEqual(browser.restarts, 1)
        self.assertEqual(browser.opens, 1)
        self.assertEqual(self.delays, [30, 60, 90])
        self.assertEqual([call[0] for call in capture.solver.calls], ['interpret_page'])
        self.assertEqual(capture.state['stage'], 'history')
        self.assertEqual(capture.activity['task_id'], '99')

    def test_loading_observation_before_start_does_not_suppress_assessment_plan(self):
        capture = self.capture(kind='assessment', details={'question_count': 10, 'time_limit': '15 minutes'})
        capture._observe_timing({'kind': 'unknown', 'key': 'loading'})
        capture._observe_timing({'kind': 'instructions', 'key': 'start', 'action': 'start'})
        capture._start_assessment_timing({'kind': 'instructions', 'action': 'start'})
        plan = deepcopy(capture.state['assessment_timing'])
        self.assertEqual(plan['started_at'], 1000)
        self.assertEqual(plan['deadline_at'], 1900)
        self.assertEqual(plan['time_limit_seconds'], 900)
        self.assertEqual(len(plan['answer_offsets_seconds']), 10)
        self.assertTrue(630 <= plan['target_seconds'] <= 765)
        self.now += 200
        restored = self.capture(kind='assessment', details=capture.activity['details'])
        restored.state = read_json(capture.checkpoint_path)
        restored._start_assessment_timing({'kind': 'instructions', 'action': 'start'})
        self.assertEqual(restored.state['assessment_timing'], plan)

    def test_same_diagnostic_retry_offer_keeps_saved_yes_decision_after_resume(self):
        capture = self.capture(kind='diagnostic')
        capture.state['presentations']['q1'] = {'decision': {'intended': 'C', 'distance': 1}}
        offer = {'kind': 'instructions', 'key': 'retry', 'action': 'decline_retry'}
        for _ in range(3):
            self.assertTrue(capture._diagnostic_retry(offer)['retry_diagnostic'])
        restored = self.capture(kind='diagnostic')
        restored.state = read_json(capture.checkpoint_path)
        self.assertTrue(restored._diagnostic_retry(offer)['retry_diagnostic'])
        self.assertEqual(self.delays, [])

    def test_second_retry_offer_keeps_saved_no_decision_after_resume(self):
        capture = self.capture(kind='diagnostic')
        offer = {'kind': 'instructions', 'key': 'retry', 'action': 'decline_retry'}
        capture.state['presentations']['q1'] = {'decision': {'intended': 'C', 'distance': 1}}
        self.assertTrue(capture._diagnostic_retry(offer)['retry_diagnostic'])
        # The next source question is another failed attempt, so the single
        # immediate retry has already been consumed.
        capture.state['presentations']['q2'] = {'decision': {'intended': 'C', 'distance': 1}}
        for _ in range(3):
            self.assertFalse(capture._diagnostic_retry(offer)['retry_diagnostic'])
        restored = self.capture(kind='diagnostic')
        restored.state = read_json(capture.checkpoint_path)
        self.assertFalse(restored._diagnostic_retry(offer)['retry_diagnostic'])
        self.assertEqual(self.delays, [])


if __name__ == '__main__':
    unittest.main()
