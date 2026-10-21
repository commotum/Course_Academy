"""Fresh learner targets with a cached course graph for resilient selection."""
import hashlib
import json
import logging
import threading
import time

from .runtime import StopRequested
from .storage import atomic_json, read_json


class ContextProvider:
    def __init__(self, config, pipeline_factory):
        self.config = config
        self.pipeline_factory = pipeline_factory
        self._threads = {}
        self._last = {}
        self._lock = threading.Lock()

    def _identity_key(self, *values):
        # A shared state directory must not mix snapshots from different databases.
        identity = [str(self.config.database), str(self.config.endpoint),
                    str(self.config.postgres_url or ""), *map(str, values)]
        return hashlib.sha256(json.dumps(identity).encode()).hexdigest()[:24]

    def _path(self, activity):
        course = str(activity.get("course_id") or self.config.course_id or "unknown")
        if not course.isalnum():
            course = "unknown"
        return self.config.state_root / "context" / (course + "-" + self._identity_key(course) + ".json")

    def __call__(self, activity):
        path = self._path(activity)
        saved = read_json(path, None)
        # Course content changes much less often than learner priorities. Reuse the
        # persisted graph across restarts; failures can retry after one minute.
        refresh_due = not saved or time.time() - saved.get("cached_at", 0) >= 3600
        with self._lock:
            current = self._threads.get(str(path))
            if refresh_due and (not current or not current.is_alive()) and time.monotonic() - self._last.get(str(path), float("-inf")) >= 60:
                current = threading.Thread(target=self._refresh, args=(activity, path), daemon=True, name="capture-context")
                self._threads[str(path)] = current
                self._last[str(path)] = time.monotonic()
                current.start()
        if not path.exists() and current:
            # Obtain the first diagnostic graph before starting whenever possible.
            # A genuinely unavailable database still has the explicit unknown-topic fallback.
            current.join(timeout=30)
        context = read_json(path, {"graph": {}, "targets": [], "course_topics": [], "snapshot_unavailable": True})
        context["context_refresh_pending"] = bool(not path.exists() and current and current.is_alive())
        # Graph refresh can lag, but every selection rereads the persisted target
        # set. Never reuse the old cache's assignment union or CLI overrides.
        context.pop("targets", None)
        context.pop("target_origins", None)
        context.update(self._targets())
        return context

    def source_dependencies(self, questions):
        try:
            return self.pipeline_factory().source_dependencies(questions)
        except StopRequested:
            raise
        except Exception as error:
            logging.warning('Source dependency lookup unavailable after %s', type(error).__name__)
            return []

    def question_topic(self, question_id):
        if not question_id:
            return None
        try:
            return self.pipeline_factory().question_topic(question_id)
        except StopRequested:
            raise
        except Exception as error:
            logging.warning("Exact question topic unavailable after %s", type(error).__name__)
            return None

    def _targets(self):
        key = self._identity_key(self.config.learner_id)
        path = self.config.state_root / "context" / ("targets-" + key + ".json")
        try:
            targets = dict(self.pipeline_factory().targets())
            targets["target_cached_at"] = time.time()
            atomic_json(path, targets)
            return targets
        except StopRequested:
            raise
        except Exception as error:
            logging.warning("Keeping saved learner targets after %s", type(error).__name__)
            targets = read_json(path, {"targets": [], "target_origins": {"learner_targets": []},
                                      "learner_id": self.config.learner_id, "target_basis": None})
            targets["targets_unavailable"] = True
            return targets

    def _refresh(self, activity, path):
        try:
            context = self.pipeline_factory().context(activity)
            context["cached_at"] = time.time()
            atomic_json(path, context)
        except Exception as error:
            logging.warning("Keeping saved course graph after %s", type(error).__name__)
