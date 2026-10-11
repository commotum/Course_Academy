"""One owner for activity selection, with durable resume and independent imports."""
from __future__ import annotations

from contextlib import ExitStack
import logging
from pathlib import Path
import time

from .context import ContextProvider
from .models import normalize_activity
from .outbox import DatabaseWorker, enqueue
from .post_activity import record as record_post_activity, retake_policy
from .queue_processing import read_queue
from .runtime import StopRequested, backoff, check_stop, wait
from .selection import choose
from .storage import append_event, atomic_json, file_lock, read_json


class CaptureRunner:
    def __init__(self, config, stop_event, browser_factory=None, capture_factory=None, pipeline_factory=None):
        self.config, self.stop_event = config, stop_event
        if browser_factory is None:
            from .browser import MathAcademyBrowser
            browser_factory = lambda: MathAcademyBrowser(config, stop_event)
        if capture_factory is None:
            from .activity import ActivityCapture
            capture_factory = lambda browser, context: ActivityCapture(config, browser, stop_event, context_provider=context)
        if pipeline_factory is None:
            from .database import DatabasePipeline
            pipeline_factory = lambda: DatabasePipeline(config, stop_event)
        self.browser_factory, self.capture_factory = browser_factory, capture_factory
        self.context = ContextProvider(config, pipeline_factory)
        self.database_worker = DatabaseWorker(config, stop_event, pipeline_factory)
        self.active_path = config.state_root / "active.json"

    def _status(self, status, **details):
        atomic_json(self.config.state_root / "status.json", {"status": status, "at": time.time(), **details})

    def _recover_orphan(self):
        """Recover a selection saved before its active pointer, never search old imports."""
        candidates = []
        for path in self.config.output_root.glob("*/activity.json"):
            directory = path.parent
            if not (directory / "handoff-complete.json").exists():
                item = read_json(path, {})
                candidates.append((path.stat().st_mtime_ns, {"activity": item, "directory": str(directory)}))
        return min(candidates, key=lambda item: item[0])[1] if candidates else None

    def _retry_observations(self, browser):
        """Use the browser only between activities; each retry is timestamped."""
        for source in sorted(self.config.output_root.glob("*/post-activity.json")):
            saved = read_json(source, {})
            if not saved.get("missing_observations") or time.time() - saved.get("retry_at", saved.get("observed_at", 0)) < 60:
                continue
            directory = source.parent
            saved["retry_at"] = time.time()
            atomic_json(source, saved)
            try:
                activity = read_json(directory / "activity.json")
                observation = browser.postprocess(activity, directory)
                observation["late_read"] = True
                record_post_activity(self.config, activity, directory, read_json(directory / "content.json"), observation)
            except StopRequested:
                raise
            except Exception as error:
                logging.warning("Account observations will retry later: %s", type(error).__name__)
            break

    def cycle(self, browser):
        check_stop(self.stop_event)
        active = read_json(self.active_path, None) or self._recover_orphan()
        if not active:
            queue = read_queue(browser, self.config.state_root / "queue")
            if not any(item.get("started") for item in queue):
                self._retry_observations(browser)
            completed = read_json(self.config.state_root / "completed.json", {})
            context = self.context({"course_id": self.config.course_id})
            activity = choose(queue, context, completed)
            if not activity:
                self._status("waiting_for_queue", queue_count=len(queue))
                return False
            activity = retake_policy(self.config, activity)
            activity.setdefault("course_id", self.config.course_id)
            directory = self.config.output_root / activity["task_id"]
            atomic_json(directory / "activity.json", activity)
            active = {"activity": activity, "directory": str(directory), "selected_at": time.time()}
            atomic_json(self.active_path, active)
        else:
            atomic_json(self.active_path, active)
        activity = normalize_activity(active["activity"])
        directory = Path(active["directory"])
        self._status("capturing", task_id=activity["task_id"], kind=activity["kind"])
        if (directory / "capture-complete.json").exists():
            content = read_json(directory / "content.json")
            if not isinstance(content, dict):
                raise ValueError("Capture completion marker has no readable content")
        else:
            capture = self.capture_factory(browser, self.context)
            content = capture.run(activity, directory)
            atomic_json(directory / "content.json", content)
            if not (directory / "capture-complete.json").exists():
                atomic_json(directory / "capture-complete.json", {"task_id": activity["task_id"], "completed_at": time.time(), "version": 1})
        check_stop(self.stop_event)
        if not (directory / "post-activity.json").exists():
            try:
                observation = browser.postprocess(activity, directory)
            except StopRequested:
                raise
            except Exception as error:
                observation = {"observed_at": time.time(), "missing": ["dashboard/progress"],
                    "error": {"type": type(error).__name__, "message": str(error)[:800]}}
            record_post_activity(self.config, activity, directory, content, observation)
        enqueue(self.config, directory)
        completed = read_json(self.config.state_root / "completed.json", {})
        completed[activity["task_id"]] = {"capture_completed_at": time.time(), "directory": str(directory), "kind": activity["kind"]}
        atomic_json(self.config.state_root / "completed.json", completed)
        atomic_json(directory / "handoff-complete.json", {"at": time.time(), "capture_only": self.config.capture_only})
        atomic_json(self.active_path, None)
        self._status("selecting", last_completed=activity["task_id"])
        return True

    def run(self):
        failures = 0
        # The legacy profile lock also prevents the old worker and the rewrite
        # from submitting work on the same account at the same time.
        locks = sorted({self.config.state_root / "capture.lock", self.config.profile.parent / "capture.lock"}, key=str)
        while not self.stop_event.is_set():
            try:
                with ExitStack() as stack:
                    for path in locks:
                        stack.enter_context(file_lock(path, blocking=False))
                    self.database_worker.start()
                    with self.browser_factory() as browser:
                        while not self.stop_event.is_set():
                            try:
                                made_progress = self.cycle(browser)
                                failures = 0
                                if not made_progress:
                                    wait(self.stop_event, max(1, self.config.retry_delay))
                            except StopRequested:
                                raise
                            except Exception as error:
                                failures += 1
                                logging.exception("Recovering the current activity after %s", type(error).__name__)
                                self._status("recovering", error_type=type(error).__name__, attempts=failures)
                                append_event(self.config.state_root / "events.jsonl", "recovery", error_type=type(error).__name__, detail=str(error)[:1200])
                                wait(self.stop_event, backoff(failures, self.config.retry_delay, self.config.recovery_max_delay))
                                # Reconstruct a broken browser; the pinned active record
                                # makes the next cycle resume this same task.
                                try:
                                    browser.restart()
                                except Exception:
                                    raise error
            except StopRequested:
                break
            except Exception as error:
                failures += 1
                logging.warning("Capture recovery will retry: %s", type(error).__name__)
                try:
                    wait(self.stop_event, backoff(failures, self.config.retry_delay, self.config.recovery_max_delay))
                except StopRequested:
                    break
        try:
            self._status("stopped", active=read_json(self.active_path, None))
        except OSError:
            logging.error("Stop requested while local storage is unavailable; previous checkpoint retained")
