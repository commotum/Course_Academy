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
from .timing import Pacer


class CaptureRunner:
    def __init__(self, config, stop_event, browser_factory=None, capture_factory=None, pipeline_factory=None, *, pacer=None, clock=None, finish_started=False):
        self.config, self.stop_event = config, stop_event
        self.finish_started = finish_started
        self.clock = clock or time.time
        self.pacer = pacer or Pacer(config, stop_event, clock=self.clock)
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
        self.pacing_path = config.state_root / "pacing.json"

    def _schedule_boundary(self, task_id, completed_count):
        """Save the sampled due time before handing off a completed activity."""
        state = read_json(self.pacing_path, {})
        if state.get('last_completed_task') == task_id:
            return
        delay = self.pacer.duration('lesson')
        every = self.config.rest_every
        rest = self.pacer.duration('rest') if every and completed_count % every == 0 else 0
        state.update(last_completed_task=task_id, completed_count=completed_count,
                     boundary_due_at=self.clock() + delay + rest,
                     boundary_delay=delay, rest_delay=rest, idle_attempts=0, idle_due_at=0)
        atomic_json(self.pacing_path, state)

    def _schedule_queue_retry(self):
        state = read_json(self.pacing_path, {})
        attempt = state.get('idle_attempts', 0) + 1
        delay = backoff(attempt, self.config.retry_delay, self.config.recovery_max_delay)
        delay += self.pacer.rng.uniform(0, self.config.recovery_jitter)
        state.update(idle_attempts=attempt, idle_due_at=self.clock() + delay)
        atomic_json(self.pacing_path, state)

    def _wait_between(self, queue=()):
        # A task already started on Math Academy takes precedence over planned
        # rests, including one that began outside this process.
        if any(item.get('started') for item in queue) or read_json(self.active_path, None) or self._recover_orphan():
            return 0
        state = read_json(self.pacing_path, {})
        due = max(state.get('boundary_due_at', 0), state.get('idle_due_at', 0))
        seconds = max(0, due - self.clock())
        if seconds:
            self._status('pacing', due_at=due, rest_delay=state.get('rest_delay', 0))
        return self.pacer.sleep(seconds)

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
        pending = []
        now = time.time()
        for source in self.config.output_root.glob("*/post-activity.json"):
            saved = read_json(source, {})
            last_attempt = saved.get("retry_at", saved.get("observed_at", 0))
            if saved.get("missing_observations") and now - last_attempt >= 60:
                pending.append((last_attempt, str(source), source, saved))
        # Least recently attempted first: one permanently missing dashboard must
        # not monopolize every gap between activities.
        for _, _, source, saved in sorted(pending):
            directory = source.parent
            saved["retry_at"] = time.time()
            atomic_json(source, saved)
            try:
                activity = read_json(directory / "activity.json")
                observation = browser.postprocess(activity, directory)
                observation["late_read"] = True
                observation["observed_at"] = time.time()
                record_post_activity(self.config, activity, directory, read_json(directory / "content.json"), observation)
            except StopRequested:
                raise
            except Exception as error:
                logging.warning("Account observations will retry later: %s", type(error).__name__)
            break

    def cycle(self, browser):
        check_stop(self.stop_event)
        active = read_json(self.active_path, None) or self._recover_orphan()
        if active and self.finish_started:
            directory = Path(active['directory'])
            checkpoint = read_json(directory / 'checkpoint.json', {})
            if not ((directory / 'capture-complete.json').exists() or checkpoint.get('completion')
                    or checkpoint.get('presentations') or checkpoint.get('steps')):
                queue = read_queue(browser, self.config.output_root / 'queue')
                if read_json(self.config.output_root / 'queue/queue.json', {}).get('unreadable'):
                    raise ValueError('Cannot confirm started activities from unreadable queue cards')
                saved = next((item for item in queue if item['task_id'] == active['activity']['task_id']), None)
                if saved is None or not saved.get('started'):
                    self._status('stopped', reason='saved_selection_not_confirmed_started', active=active)
                    self.stop_event.set()
                    return False
        if not active:
            queue = read_queue(browser, self.config.output_root / "queue")
            if self.finish_started:
                if read_json(self.config.output_root / 'queue/queue.json', {}).get('unreadable'):
                    raise ValueError('Cannot confirm started activities from unreadable queue cards')
                queue = [item for item in queue if item.get('started')]
                if not queue:
                    self._status('stopped', reason='all_started_activities_finished')
                    self.stop_event.set()
                    return False
            if self._wait_between(queue):
                queue = read_queue(browser, self.config.output_root / "queue")
                if self.finish_started:
                    if read_json(self.config.output_root / 'queue/queue.json', {}).get('unreadable'):
                        raise ValueError('Cannot confirm started activities from unreadable queue cards')
                    queue = [item for item in queue if item.get('started')]
            if not any(item.get("started") for item in queue):
                self._retry_observations(browser)
            completed = read_json(self.config.state_root / "completed.json", {})
            if not choose(queue, completed=completed):
                self._status("waiting_for_queue", queue_count=len(queue))
                self._schedule_queue_retry()
                return False
            context = self.context({"course_id": self.config.course_id})
            check_stop(self.stop_event)
            # The provider already gives the first graph a bounded opportunity
            # to load. Use available scores or queue order while it refreshes;
            # a started activity must not wait for an optional ranking snapshot.
            activity = choose(queue, context, completed)
            if not activity:
                self._status("waiting_for_queue", queue_count=len(queue))
                self._schedule_queue_retry()
                return False
            if context.get("context_refresh_pending"):
                activity['selection']['context_refresh_pending'] = True
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
        self._schedule_boundary(activity['task_id'], len(completed))
        atomic_json(directory / "handoff-complete.json", {"at": time.time(), "capture_only": self.config.capture_only})
        atomic_json(self.active_path, None)
        self._status("selecting", last_completed=activity["task_id"])
        return True

    def run(self):
        failures = 0
        dependency_error = None
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
                                dependency_error = None
                                if not made_progress:
                                    self._wait_between()
                            except StopRequested:
                                raise
                            except Exception as error:
                                if getattr(error, "retryable", True) is False:
                                    # A solver configuration/schema failure cannot be
                                    # repaired by relaunching the browser. Keep the
                                    # task pinned while the solver checks for changed
                                    # configuration/evidence on its next request.
                                    detail = str(error)[:1200]
                                    self._status("waiting_for_solver_dependency", error_type=type(error).__name__, detail=detail,
                                                 active=read_json(self.active_path, None))
                                    if dependency_error != detail:
                                        append_event(self.config.state_root / "events.jsonl", "solver_dependency", detail=detail)
                                        logging.warning("Pinned activity awaits solver dependency: %s", detail)
                                        dependency_error = detail
                                    wait(self.stop_event, max(1, self.config.recovery_max_delay))
                                    continue
                                failures += 1
                                logging.exception("Recovering the current activity after %s", type(error).__name__)
                                self._status("recovering", error_type=type(error).__name__, attempts=failures)
                                append_event(self.config.state_root / "events.jsonl", "recovery", error_type=type(error).__name__, detail=str(error)[:1200])
                                self.pacer.sleep(self.pacer.backoff(failures))
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
                    self.pacer.sleep(self.pacer.backoff(failures))
                except StopRequested:
                    break
        try:
            self._status("stopped", active=read_json(self.active_path, None))
        except OSError:
            logging.error("Stop requested while local storage is unavailable; previous checkpoint retained")
