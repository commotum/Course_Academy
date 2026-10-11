import json
from pathlib import Path
import tempfile
import threading
import time
import unittest

from scripts.config import Config
from scripts.outbox import DatabaseWorker, enqueue
from scripts.post_activity import record, retake_policy
from scripts.queue_processing import read_queue
from scripts.runner import CaptureRunner
from scripts.selection import choose, target_support
from scripts.storage import atomic_json, read_json


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.config = Config(repo_root=self.root, profile=self.root / "profile", retry_delay=0.01)
        self.stop = threading.Event()

    def tearDown(self):
        self.stop.set()
        self.temp.cleanup()

    def activity(self, mid="1", kind="lesson", started=False, topic="10"):
        return {"task_id": mid, "kind": kind, "started": started, "topic_id": topic, "details": {}}

    def finished(self, mid):
        directory = self.config.output_root / mid
        atomic_json(directory / "activity.json", self.activity(mid))
        atomic_json(directory / "content.json", {"questions": []})
        atomic_json(directory / "capture-complete.json", {"task_id": mid})
        return directory

    def test_selection_combines_lessons_reviews_and_keeps_started_first(self):
        queue = [self.activity("1", "lesson", topic="1"), self.activity("2", "review", topic="2")]
        context = {"graph": {"1": ["8"], "2": ["8", "9"]}, "targets": ["8", "9"]}
        self.assertEqual(choose(queue, context)["task_id"], "2")
        queue[0]["started"] = True
        self.assertEqual(choose(queue, context)["task_id"], "1")
        queue.append(self.activity("3", "assessment", True))
        self.assertEqual(choose(queue, context)["task_id"], "3")

    def test_graph_cycles_terminate_and_self_target_counts(self):
        score = target_support("1", {"1": ["2"], "2": ["1", "3"]}, ["1", "3"])
        self.assertEqual(score["target_distances"], {"1": 0, "3": 2})

    def test_queue_ties_are_source_order_and_completions_excluded(self):
        queue = [self.activity("1"), self.activity("2", "review")]
        self.assertEqual(choose(queue)["task_id"], "1")
        self.assertEqual(choose(queue, completed=["1"])["task_id"], "2")

    def test_ledger_counts_task_once_and_late_old_xp_cannot_restore_penalty(self):
        first, second = self.finished("1"), self.finished("2")
        record(self.config, self.activity("1"), first, {}, {"completion": {"earned_xp": -5}})
        second_activity = self.activity("2")
        second_activity["details"]["force_correct"] = True
        record(self.config, second_activity, second, {}, {"completion": {"earned_xp": 10}})
        record(self.config, self.activity("1"), first, {}, {"completion": {"earned_xp": -5}})
        ledger = read_json(self.config.state_root / "xp.json")
        self.assertEqual(sum(item["earned_xp"] for item in ledger.values()), 5)
        daily = read_json(self.config.state_root / "daily-xp.json")
        self.assertEqual(sum(item["earned_xp"] for item in daily.values()), 5)
        self.assertEqual(sum(item["counted_tasks"] for item in daily.values()), 2)
        self.assertFalse(retake_policy(self.config, self.activity("3"))["details"]["force_correct"])

    def test_pending_oldest_write_blocks_later_writes_but_does_not_drop_them(self):
        first, second = self.finished("1"), self.finished("2")
        path1, path2 = enqueue(self.config, first), enqueue(self.config, second)
        calls = []

        class Database:
            def process(_, directory, apply=True):
                calls.append(directory.name)
                raise TimeoutError("receipt outcome unknown")

        worker = DatabaseWorker(self.config, self.stop, Database)
        self.assertEqual(worker.process_one()["status"], "pending")
        self.assertEqual(calls, ["1"])
        self.assertEqual(read_json(path2)["attempts"], 0)
        self.assertEqual(worker.process_one()["status"], "waiting")

    def test_saved_capture_continues_while_database_is_down(self):
        calls = []
        outer = self

        class Browser:
            def queue(_, directory):
                return [outer.activity("1"), outer.activity("2")]
            def postprocess(_, activity, directory):
                raise ConnectionError("progress page unavailable")

        class Capture:
            def run(_, activity, directory):
                calls.append(activity["task_id"])
                return {"questions": [], "completion": {"earned_xp": 5}}

        class Database:
            def context(_, activity):
                raise ConnectionError("database unavailable")
            def process(_, directory, apply=True):
                raise ConnectionError("database unavailable")

        runner = CaptureRunner(self.config, self.stop, capture_factory=lambda b, c: Capture(), pipeline_factory=Database)
        self.assertTrue(runner.cycle(Browser()))
        self.assertTrue(runner.cycle(Browser()))
        self.assertEqual(calls, ["1", "2"])
        self.assertEqual(len(runner.database_worker.pending()), 2)
        self.assertEqual(len(read_json(self.config.state_root / "completed.json")), 2)

    def test_recovery_keeps_same_task_and_completed_marker_prevents_replay(self):
        calls = []
        outer = self

        class Browser:
            def queue(_, directory):
                return [outer.activity("1"), outer.activity("2")]
            def postprocess(_, activity, directory):
                return {"completion": {"earned_xp": 2}}

        class Capture:
            def run(_, activity, directory):
                calls.append(activity["task_id"])
                atomic_json(directory / "content.json", {"questions": []})
                atomic_json(directory / "capture-complete.json", {"task_id": activity["task_id"]})
                raise ConnectionError("process interrupted after final capture save")

        runner = CaptureRunner(self.config, self.stop, capture_factory=lambda b, c: Capture(), pipeline_factory=lambda: None)
        runner.context = lambda activity: {}
        with self.assertRaises(ConnectionError):
            runner.cycle(Browser())
        self.assertEqual(read_json(runner.active_path)["activity"]["task_id"], "1")
        self.assertTrue(runner.cycle(Browser()))
        self.assertEqual(calls, ["1"])

    def test_capture_only_never_enters_write_processing(self):
        self.config.capture_only = True
        enqueue(self.config, self.finished("1"))
        worker = DatabaseWorker(self.config, self.stop, lambda: self.fail("unexpected database write"))
        self.assertEqual(worker.process_one()["status"], "capture_only")

    def test_capture_only_cannot_commit_older_normal_run_work(self):
        enqueue(self.config, self.finished("1"))
        self.config.capture_only = True
        worker = DatabaseWorker(self.config, self.stop, lambda: self.fail("unexpected database write"))
        self.assertEqual(worker.process_one()["status"], "capture_only")

    def test_queue_normalization_keeps_original_page_evidence(self):
        outer = self
        class Browser:
            def queue(_, directory):
                activities = [outer.activity()]
                atomic_json(directory / "queue.json", {"activities": activities,
                    "html_path": "/tmp/source-queue.html", "captured_at": time.time()})
                return activities
        directory = self.root / "queue"
        read_queue(Browser(), directory)
        self.assertEqual(read_json(directory / "queue.json")["html_path"], "/tmp/source-queue.html")

    def test_corrupt_current_state_recovers_prior_valid_checkpoint(self):
        path = self.root / "state.json"
        atomic_json(path, {"task_id": "1"})
        atomic_json(path, {"task_id": "1", "accepted": True})
        path.write_text("{")
        self.assertEqual(read_json(path), {"task_id": "1"})

    def test_presentation_order_survives_checkpoint_round_trip(self):
        path = self.root / "checkpoint.json"
        atomic_json(path, {"presentations": {"q-20": {}, "q-3": {}, "q-100": {}}})
        self.assertEqual(list(read_json(path)["presentations"]), ["q-20", "q-3", "q-100"])


if __name__ == "__main__":
    unittest.main()
