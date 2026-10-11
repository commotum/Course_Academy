"""Offline regressions for selection context and account observation recovery."""
from contextlib import contextmanager
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from scripts.activity.capture import ActivityCapture
from scripts.activity.policy import AnswerPolicy
from scripts.activity.solver import SolverUnavailable
from scripts.config import Config
from scripts.context import ContextProvider
from scripts.post_activity import record
from scripts.runner import CaptureRunner
from scripts.runtime import StopRequested
from scripts.storage import atomic_json, read_json


class WorkflowResilienceTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.config = Config(repo_root=self.root, profile=self.root / 'profile')
        self.stop = threading.Event()

    def activity(self, task='1'):
        return {'task_id': task, 'kind': 'lesson', 'topic_id': '8', 'details': {}}

    def test_cache_paths_follow_database_connection_and_learner(self):
        provider = ContextProvider(self.config, lambda: None)
        first = provider._path({'course_id': '55'})
        self.config.database = 'different'
        self.assertNotEqual(first, provider._path({'course_id': '55'}))
        second = provider._path({'course_id': '55'})
        self.config.endpoint = '/tmp/different.sock'
        self.assertNotEqual(second, provider._path({'course_id': '55'}))
        third = provider._path({'course_id': '55'})
        self.config.postgres_url = 'different server'
        self.assertNotEqual(third, provider._path({'course_id': '55'}))
        learner_key = provider._identity_key(self.config.learner_id)
        self.config.learner_id = 'someone-else'
        self.assertNotEqual(learner_key, provider._identity_key(self.config.learner_id))

    def test_fresh_persisted_graph_is_reused_after_restart_but_targets_are_read(self):
        calls = []
        class Pipeline:
            def context(_, activity):
                raise AssertionError('fresh full graph should not be read again')
            def targets(_):
                calls.append('targets')
                return {'targets': ['8']}
        provider = ContextProvider(self.config, Pipeline)
        atomic_json(provider._path({'course_id': '55'}), {'graph': {'1': ['8']}, 'cached_at': 1000})
        with patch('scripts.context.time.time', return_value=1100):
            context = provider({'course_id': '55'})
        self.assertEqual(context['graph'], {'1': ['8']})
        self.assertEqual(calls, ['targets'])

    def test_pending_initial_graph_is_visible_instead_of_an_empty_success(self):
        class PendingThread:
            def __init__(_, **kwargs):
                pass
            def start(_):
                pass
            def is_alive(_):
                return True
            def join(_, timeout):
                self.assertEqual(timeout, 30)
        class Pipeline:
            def targets(_):
                return {'targets': ['8']}
        with patch('scripts.context.threading.Thread', PendingThread):
            context = ContextProvider(self.config, Pipeline)({'course_id': '55'})
        self.assertTrue(context['context_refresh_pending'])
        self.assertTrue(context['snapshot_unavailable'])

    def test_empty_and_completed_queue_do_not_read_database_context(self):
        runner = CaptureRunner(self.config, self.stop, pipeline_factory=lambda: None)
        runner.context = lambda activity: self.fail('empty queue must not read database context')
        class Browser:
            def queue(_, directory):
                return []
        self.assertFalse(runner.cycle(Browser()))
        atomic_json(self.config.state_root / 'completed.json', {'1': {}})
        class CompletedBrowser:
            def queue(_, directory):
                return [self.activity()]
        self.assertFalse(runner.cycle(CompletedBrowser()))

    def test_pending_graph_cannot_pin_a_queue_order_selection(self):
        runner = CaptureRunner(self.config, self.stop, pipeline_factory=lambda: None)
        runner.context = lambda activity: {'context_refresh_pending': True}
        class Browser:
            def queue(_, directory):
                return [self.activity()]
        self.assertFalse(runner.cycle(Browser()))
        self.assertFalse(runner.active_path.exists())
        self.assertEqual(read_json(self.config.state_root / 'status.json')['status'], 'waiting_for_context')

    def test_late_reads_preserve_baseline_initial_observation_and_completion_evidence(self):
        directory = self.config.output_root / '1'
        atomic_json(directory / 'capture-complete.json', {'completed_at': 100})
        atomic_json(self.config.state_root / 'progress.json', {'observed_at': 50, 'progress': ['before']})
        record(self.config, self.activity(), directory, {}, {'observed_at': 101, 'missing': ['progress'],
                                                         'completion': {'earned_xp': 5, 'base_xp': 8}})
        atomic_json(self.config.state_root / 'progress.json', {'observed_at': 150, 'progress': ['another task']})
        record(self.config, self.activity(), directory, {}, {'observed_at': 200, 'late_read': True, 'progress': ['later'],
                                                         'completion': {'base_xp': 0}})
        record(self.config, self.activity(), directory, {}, {'observed_at': 300, 'late_read': True, 'progress': ['latest']})
        saved = read_json(directory / 'post-activity.json')
        self.assertEqual(read_json(directory / 'progress-before.json')['progress'], ['before'])
        self.assertEqual(saved['first_observed_at'], 101)
        self.assertEqual([row['observed_at'] for row in saved['observation_history']], [101, 200, 300])
        self.assertEqual(saved['completion']['earned_xp'], 5)
        self.assertEqual(read_json(self.config.state_root / 'xp.json')['1']['base_xp'], 0)

    def test_later_partial_read_does_not_restore_stale_captured_completion(self):
        directory = self.config.output_root / '1'
        content = {'completion': {'earned_xp': -5}}
        record(self.config, self.activity(), directory, content, {'observed_at': 100})
        record(self.config, self.activity(), directory, content,
               {'observed_at': 200, 'completion': {'earned_xp': 5}})
        record(self.config, self.activity(), directory, content,
               {'observed_at': 300, 'completion': {'earned_xp': None, 'base_xp': 8}})
        self.assertEqual(read_json(directory / 'post-activity.json')['completion']['earned_xp'], 5)
        self.assertEqual(read_json(self.config.state_root / 'xp.json')['1']['earned_xp'], 5)

    def test_positive_xp_does_not_clear_retake_until_source_grades_are_all_correct(self):
        first = self.config.output_root / '1'
        second = self.config.output_root / '2'
        atomic_json(first / 'capture-complete.json', {'completed_at': 100})
        atomic_json(second / 'capture-complete.json', {'completed_at': 200})
        record(self.config, self.activity(), first, {}, {'completion': {'earned_xp': -5}})
        retake = self.activity('2')
        retake['details']['force_correct'] = True
        record(self.config, retake, second, {'attempts': [{'accepted': True, 'grade': 'Incorrect'}]},
               {'completion': {'earned_xp': 5}})
        self.assertTrue(read_json(self.config.state_root / 'retakes.json')['lesson:8']['force_correct'])
        record(self.config, retake, second, {'attempts': [{'accepted': True, 'grade': 'Correct'}]},
               {'completion': {'earned_xp': 5}})
        self.assertFalse(read_json(self.config.state_root / 'retakes.json')['lesson:8']['force_correct'])

    def test_missing_observation_retry_rotates_and_stamps_the_actual_late_read(self):
        for task in ['1', '2']:
            directory = self.config.output_root / task
            atomic_json(directory / 'activity.json', self.activity(task))
            atomic_json(directory / 'content.json', {})
            atomic_json(directory / 'post-activity.json', {'observed_at': 1, 'missing_observations': ['progress']})
        calls = []
        class Browser:
            def postprocess(_, activity, directory):
                calls.append(activity['task_id'])
                return {'observed_at': 1, 'missing': ['progress']}
        runner = CaptureRunner(self.config, self.stop, pipeline_factory=lambda: None)
        with patch('scripts.runner.time.time', return_value=100):
            runner._retry_observations(Browser())
        with patch('scripts.runner.time.time', return_value=200):
            runner._retry_observations(Browser())
        self.assertEqual(calls, ['1', '2'])
        self.assertEqual(read_json(self.config.output_root / '2/post-activity.json')['observed_at'], 200)

    def test_deterministic_solver_dependency_keeps_task_pinned_without_browser_restart(self):
        restarts, statuses = [], []
        class Browser:
            def restart(_):
                restarts.append(True)
        @contextmanager
        def browser():
            yield Browser()
        runner = CaptureRunner(self.config, self.stop, browser_factory=browser, pipeline_factory=lambda: None)
        runner.database_worker.start = lambda: None
        active = {'activity': self.activity(), 'directory': str(self.config.output_root / '1')}
        atomic_json(runner.active_path, active)
        runner._status = lambda status, **details: statuses.append(status)
        runner.cycle = lambda browser: (_ for _ in ()).throw(SolverUnavailable('invalid CLI option', retryable=False))
        def stop_wait(event, seconds):
            event.set()
            raise StopRequested()
        with patch('scripts.runner.wait', stop_wait):
            runner.run()
        self.assertEqual(restarts, [])
        self.assertIn('waiting_for_solver_dependency', statuses)
        self.assertEqual(read_json(runner.active_path), active)

    def test_recovered_diagnostic_context_changes_only_future_intentions(self):
        state = {}
        policy = AnswerPolicy({'kind': 'diagnostic'}, state, {'snapshot_unavailable': True}, clock=lambda: 10)
        old = dict(policy.decide('old', {'topic_id': '1'}))
        policy.refresh_context({'graph': {'1': ['2']}, 'course_topics': ['2']})
        self.assertEqual(policy.decide('old', {'topic_id': '1'}), old)
        new = policy.decide('new', {'topic_id': '1'})
        self.assertEqual(new['distance'], 1)
        self.assertEqual(new['action'], 'answer')

    def test_new_diagnostic_classification_refreshes_unavailable_context_without_llm(self):
        capture = ActivityCapture(self.config, None, self.stop, context_provider=lambda activity:
                                  {'graph': {'1': ['2']}, 'course_topics': ['2']})
        capture.directory = self.root
        capture.checkpoint_path = self.root / 'checkpoint.json'
        capture.activity = {'kind': 'diagnostic'}
        capture.state = {'context': {'snapshot_unavailable': True}, 'policy': {}}
        capture.policy = AnswerPolicy(capture.activity, capture.state['policy'], capture.state['context'])
        question = {'topic_id': '1'}
        capture._classify(question, {})
        self.assertEqual(capture.state['policy']['distances']['1'], 1)


if __name__ == '__main__':
    unittest.main()
