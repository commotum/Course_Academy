"""Offline regressions for restored pacing and persisted activity boundaries."""
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from scripts.cli import configuration, parser
from scripts.config import Config
from scripts.runner import CaptureRunner
from scripts.runtime import StopRequested
from scripts.storage import atomic_json, read_json
from scripts.timing import Pacer


class Clock:
    def __init__(self):
        self.now = 1000.0
        self.sleeps = []

    def __call__(self):
        return self.now

    def sleep(self, delay):
        self.now += delay
        self.sleeps.append(delay)


class TimingTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.config = Config(repo_root=self.root, profile=self.root / 'profile',
                             lesson_min=10, lesson_max=10, rest_min=120, rest_max=120,
                             recovery_jitter=0)
        self.stop = threading.Event()
        self.clock = Clock()
        self.pacer = Pacer(self.config, self.stop, clock=self.clock, sleeper=self.clock.sleep)

    def runner(self):
        return CaptureRunner(self.config, self.stop, pipeline_factory=lambda: None,
                             pacer=self.pacer, clock=self.clock)

    def test_defaults_restore_original_delays_and_cli_cannot_remove_ui_floor(self):
        config = Config(repo_root=self.root)
        self.assertEqual((config.ui_delay_ms, config.settle_ms, config.timeout_ms), (500, 1000, 45000))
        self.assertEqual((config.event_min, config.event_max), (.8, 2.5))
        self.assertEqual((config.answer_min, config.answer_max), (5, 12))
        self.assertEqual((config.lesson_min, config.lesson_max), (10, 25))
        self.assertEqual((config.rest_every, config.rest_min, config.rest_max), (20, 120, 360))
        self.assertEqual(config.solver_timeout, 300)
        with self.assertRaises(ValueError):
            configuration(parser().parse_args(['check', '--ui-delay-ms', '499']))
        overridden = configuration(parser().parse_args(['check', '--ui-delay-ms', '750', '--event-min', '1.2']))
        self.assertEqual((overridden.ui_delay_ms, overridden.event_min), (750, 1.2))

    def test_answer_wait_credits_solver_time_and_respects_absolute_deadline(self):
        self.config.answer_min = self.config.answer_max = 12
        self.assertEqual(self.pacer.wait('answer', elapsed=7), 5)
        self.assertEqual(self.clock.now, 1005)
        self.assertEqual(self.pacer.wait('answer', deadline=1007), 2)
        self.assertEqual(self.clock.now, 1007)
        self.assertEqual(self.pacer.wait('answer', elapsed=20), 0)

    def test_stop_interrupts_any_wait_without_waiting_for_whole_rest(self):
        def stop_after_first_chunk(seconds):
            self.clock.sleep(seconds)
            self.stop.set()
        self.pacer.sleeper = stop_after_first_chunk
        with self.assertRaises(StopRequested):
            self.pacer.wait('rest')
        self.assertEqual(self.clock.sleeps, [.25])

    def test_recovery_backoff_is_linear_capped_and_honors_server_minimum(self):
        self.assertEqual([self.pacer.backoff(n) for n in (1, 2, 3, 20)], [30, 60, 90, 180])
        self.assertEqual(self.pacer.backoff(1, retry_after=240), 240)
        self.config.recovery_jitter = 5
        with patch.object(self.pacer.rng, 'uniform', return_value=3):
            self.assertEqual(self.pacer.backoff(1), 33)

    def test_periodic_rest_and_boundary_due_survive_repeated_handoff_and_restart(self):
        runner = self.runner()
        runner._schedule_boundary('twentieth', 20)
        original = read_json(runner.pacing_path)
        self.assertEqual(original['boundary_due_at'], 1130)
        self.clock.now += 40
        resumed = self.runner()
        resumed._schedule_boundary('twentieth', 20)
        self.assertEqual(read_json(resumed.pacing_path), original)
        self.assertEqual(resumed._wait_between(), 90)
        self.assertEqual(self.clock.now, 1130)
        self.assertEqual(resumed._wait_between(), 0)

    def test_rest_never_delays_a_pinned_or_server_started_activity(self):
        runner = self.runner()
        runner._schedule_boundary('twentieth', 20)
        self.assertEqual(runner._wait_between([{'started': True}]), 0)
        atomic_json(runner.active_path, {'activity': {'task_id': 'active'}})
        self.assertEqual(runner._wait_between(), 0)
        atomic_json(runner.active_path, None)
        atomic_json(self.config.output_root / 'orphan/activity.json', {'task_id': 'orphan'})
        self.assertEqual(runner._wait_between(), 0)
        self.assertEqual(self.clock.sleeps, [])

    def test_empty_queue_backoff_persists_escalates_and_resets_after_progress(self):
        runner = self.runner()
        for expected in (30, 60, 120, 180):
            runner._schedule_queue_retry()
            resumed = self.runner()
            self.assertEqual(resumed._wait_between(), expected)
        state = read_json(runner.pacing_path)
        self.assertEqual(state['idle_attempts'], 4)
        runner._schedule_boundary('done', 1)
        state = read_json(runner.pacing_path)
        self.assertEqual((state['idle_attempts'], state['idle_due_at']), (0, 0))


if __name__ == '__main__':
    unittest.main()
