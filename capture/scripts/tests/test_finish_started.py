from contextlib import contextmanager
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import Mock, patch

from scripts.cli import configuration, parser
from scripts.config import Config
from scripts.fleet import run_fleet
from scripts.runner import CaptureRunner
from scripts.storage import atomic_json, read_json


class FinishStartedTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.config = Config(repo_root=self.root, profile=self.root / 'profile')
        self.stop = threading.Event()
        self.queue = []
        self.captured = []
        outer = self

        class Browser:
            def queue(self, directory):
                return outer.queue

            def postprocess(self, activity, directory):
                return {}

        class Capture:
            def run(self, activity, directory):
                outer.captured.append(activity['task_id'])
                return {'activity': activity, 'questions': [], 'canonical_examples': []}

        self.browser = Browser()
        self.runner = CaptureRunner(self.config, self.stop, finish_started=True,
            capture_factory=lambda browser, provider: Capture(), pipeline_factory=lambda: None)
        self.runner.context = Mock(return_value={})
        self.runner._wait_between = Mock(return_value=0)
        self.runner._retry_observations = Mock()

    def activity(self, task, started=False):
        return {'task_id': task, 'kind': 'review', 'topic_id': '1', 'started': started}

    def test_unstarted_queue_stops_before_rest_context_or_selection(self):
        self.queue = [self.activity('new')]
        self.assertFalse(self.runner.cycle(self.browser))
        self.assertTrue(self.stop.is_set())
        self.assertEqual(self.captured, [])
        self.runner.context.assert_not_called()
        self.runner._wait_between.assert_not_called()
        self.runner._retry_observations.assert_not_called()
        self.assertFalse(self.runner.active_path.exists())

    def test_finishes_server_started_then_stops_without_new_activity(self):
        self.queue = [self.activity('new'), self.activity('started', True)]
        with patch('scripts.runner.record_post_activity'):
            self.assertTrue(self.runner.cycle(self.browser))
        self.assertEqual(self.captured, ['started'])
        self.assertIsNone(read_json(self.runner.active_path))
        self.queue = [self.activity('new')]
        self.assertFalse(self.runner.cycle(self.browser))
        self.assertTrue(self.stop.is_set())
        self.assertEqual(self.captured, ['started'])
        self.assertTrue((self.config.output_root / 'started/handoff-complete.json').exists())

    def test_unreadable_queue_cannot_establish_no_started_activity(self):
        self.queue = [{'started': True, 'kind': 'review'}]
        with self.assertRaisesRegex(ValueError, 'unreadable queue'):
            self.runner.cycle(self.browser)
        self.assertFalse(self.stop.is_set())
        self.assertEqual(self.captured, [])

    def test_pinned_started_capture_keeps_accepted_progress_then_stops(self):
        directory = self.config.output_root / 'saved'
        active = {'activity': self.activity('saved'), 'directory': str(directory)}
        atomic_json(self.runner.active_path, active)
        atomic_json(directory / 'checkpoint.json', {'presentations': {'own-question': {'accepted': True}}})
        self.queue = [self.activity('new')]
        with patch('scripts.runner.record_post_activity'):
            self.assertTrue(self.runner.cycle(self.browser))
        self.assertFalse(self.runner.cycle(self.browser))
        self.assertEqual(self.captured, ['saved'])
        self.assertTrue(read_json(directory / 'checkpoint.json')['presentations']['own-question']['accepted'])

    def test_saved_unstarted_selection_is_preserved_without_starting_it(self):
        directory = self.config.output_root / 'planned'
        active = {'activity': self.activity('planned'), 'directory': str(directory)}
        atomic_json(self.runner.active_path, active)
        atomic_json(directory / 'checkpoint.json', {'stage': 'opening'})
        self.queue = [self.activity('planned')]
        self.assertFalse(self.runner.cycle(self.browser))
        self.assertTrue(self.stop.is_set())
        self.assertEqual(self.captured, [])
        self.assertEqual(read_json(self.runner.active_path), active)

    def test_cli_flag_is_runtime_only_and_fleet_exits_after_four_successes(self):
        args = parser().parse_args(['run', '--finish-started'])
        self.assertTrue(args.finish_started)
        self.assertFalse(hasattr(configuration(args), 'finish_started'))

        @contextmanager
        def signals(stop):
            yield

        process = Mock()
        process.poll.return_value = 0
        with patch('scripts.fleet.subprocess.Popen', return_value=process) as launch, \
             patch('scripts.fleet.shutdown_signals', signals), patch('scripts.fleet.wait'):
            self.assertEqual(run_fleet(['fleet', '--finish-started']), 0)
        self.assertEqual(launch.call_count, 4)


if __name__ == '__main__':
    unittest.main()
