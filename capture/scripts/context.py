"""Nonblocking refresh of read-only target and course graph snapshots."""
import logging
from pathlib import Path
import threading
import time

from .storage import atomic_json, read_json


class ContextProvider:
    def __init__(self, config, pipeline_factory):
        self.config = config
        self.pipeline_factory = pipeline_factory
        self._threads = {}
        self._last = {}
        self._lock = threading.Lock()

    def _path(self, activity):
        course = str(activity.get("course_id") or self.config.course_id or "unknown")
        if not course.isalnum():
            course = "unknown"
        return self.config.state_root / "context" / (course + ".json")

    def __call__(self, activity):
        path = self._path(activity)
        with self._lock:
            current = self._threads.get(str(path))
            if (not current or not current.is_alive()) and time.monotonic() - self._last.get(str(path), -1000) >= 60:
                current = threading.Thread(target=self._refresh, args=(activity, path), daemon=True, name="capture-context")
                self._threads[str(path)] = current
                self._last[str(path)] = time.monotonic()
                current.start()
        if not path.exists() and current:
            # Obtain the first diagnostic graph before starting whenever possible.
            # A genuinely unavailable database still has the explicit unknown-topic fallback.
            current.join(timeout=30 if activity.get("kind") == "diagnostic" else 2)
        context = read_json(path, {"graph": {}, "targets": [], "course_topics": [], "snapshot_unavailable": True})
        if self.config.targets:
            context["targets"] = list(self.config.targets)
        return context

    def _refresh(self, activity, path):
        try:
            context = self.pipeline_factory().context(activity)
            context["cached_at"] = time.time()
            atomic_json(path, context)
        except Exception as error:
            logging.warning("Keeping saved course/target context after %s", type(error).__name__)
