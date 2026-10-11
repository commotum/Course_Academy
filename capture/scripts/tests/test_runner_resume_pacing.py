"""Started work and saved decisions outrank rests and unavailable ranking data."""
from pathlib import Path
import tempfile
import threading
import unittest

from scripts.config import Config
from scripts.runner import CaptureRunner
from scripts.runtime import StopRequested
from scripts.storage import atomic_json, read_json
from scripts.timing import Pacer


class RunnerResumePacingTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.config = Config(repo_root=self.root, profile=self.root / 'profile', recovery_jitter=0)
        self.stop = threading.Event()
        self.now = 1000.0
        self.sleeps, self.captured, self.queue_directories, self.contexts = [], [], [], []
        self.queue = []
        outer = self
        class Browser:
            def queue(_, directory):
                outer.queue_directories.append(directory)
                return outer.queue
        self.browser = Browser()

    def activity(self, task, kind='lesson', *, started=False, topic='1'):
        return {'task_id': task, 'kind': kind, 'started': started, 'topic_id': topic, 'details': {}}

    def runner(self, context):
        outer = self
        class Capture:
            def run(_, activity, directory):
                outer.captured.append(activity)
                raise StopRequested()
        def sleep(seconds):
            self.sleeps.append(seconds)
            self.now += seconds
        clock = lambda: self.now
        runner = CaptureRunner(self.config, self.stop,
            capture_factory=lambda browser, provider: Capture(), pipeline_factory=lambda: None,
            clock=clock, pacer=Pacer(self.config, self.stop, clock=clock, sleeper=sleep))
        def provider(activity):
            self.contexts.append(activity)
            return context
        runner.context = provider
        return runner

    def test_server_started_assessment_bypasses_saved_rest_and_pending_context(self):
        self.queue = [self.activity('new'), self.activity('live', 'assessment', started=True)]
        runner = self.runner({'context_refresh_pending': True, 'snapshot_unavailable': True})
        atomic_json(runner.pacing_path, {'boundary_due_at': 1360, 'idle_due_at': 1180, 'rest_delay': 360})
        with self.assertRaises(StopRequested):
            runner.cycle(self.browser)
        self.assertEqual(self.sleeps, [])
        self.assertEqual(self.captured[0]['task_id'], 'live')
        self.assertEqual(self.captured[0]['selection']['priority_level'], 1)
        self.assertTrue(self.captured[0]['selection']['context_refresh_pending'])
        self.assertEqual(read_json(runner.active_path)['activity']['task_id'], 'live')
        self.assertEqual(len(self.contexts), 1)

    def test_started_lesson_and_review_use_available_scores_during_refresh(self):
        self.queue = [self.activity('first', started=True, topic='1'),
                      self.activity('supported', 'review', started=True, topic='2')]
        runner = self.runner({'context_refresh_pending': True, 'graph': {'2': ['9']},
                              'targets': ['9'], 'basis': 42, 'target_basis': 43})
        atomic_json(runner.pacing_path, {'boundary_due_at': 1360})
        with self.assertRaises(StopRequested):
            runner.cycle(self.browser)
        selected = self.captured[0]
        self.assertEqual(selected['task_id'], 'supported')
        self.assertEqual(selected['selection']['supporting_targets'], ['9'])
        self.assertEqual(selected['selection']['context_basis'], 42)
        self.assertEqual(selected['selection']['target_basis'], 43)
        self.assertEqual(self.sleeps, [])

    def test_pinned_activity_resumes_without_queue_context_or_rest(self):
        runner = self.runner({})
        active = {'activity': self.activity('saved', 'diagnostic', started=True),
                  'directory': str(self.config.output_root / 'saved')}
        atomic_json(runner.active_path, active)
        atomic_json(runner.pacing_path, {'boundary_due_at': 1360, 'idle_due_at': 1180})
        with self.assertRaises(StopRequested):
            runner.cycle(self.browser)
        self.assertEqual(self.captured[0]['task_id'], 'saved')
        self.assertEqual(self.queue_directories, [])
        self.assertEqual(self.contexts, [])
        self.assertEqual(self.sleeps, [])
        self.assertEqual(read_json(runner.active_path), active)

    def test_manual_stop_during_context_read_does_not_select_new_activity(self):
        self.queue = [self.activity('new')]
        runner = self.runner({})
        def stopped_context(activity):
            self.stop.set()
            return {'context_refresh_pending': True}
        runner.context = stopped_context
        with self.assertRaises(StopRequested):
            runner.cycle(self.browser)
        self.assertEqual(self.captured, [])
        self.assertFalse(runner.active_path.exists())

    def test_new_queue_evidence_is_saved_under_reference_without_moving_old_cache(self):
        old = self.config.state_root / 'queue' / 'queue.json'
        atomic_json(old, {'previous_evidence': True})
        runner = self.runner({})
        self.assertFalse(runner.cycle(self.browser))
        destination = self.config.output_root / 'queue'
        self.assertEqual(self.queue_directories, [destination])
        self.assertEqual(read_json(destination / 'queue.json')['activities'], [])
        self.assertEqual(read_json(old), {'previous_evidence': True})


if __name__ == '__main__':
    unittest.main()
