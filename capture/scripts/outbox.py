"""Ordered database persistence, independent of the live activity loop."""
from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
import threading
import time
import uuid

from .runtime import StopRequested, backoff, wait
from .storage import atomic_json, file_lock, read_json

FINAL = {"verified", "no_changes"}


def target_id(config):
    value = [str(config.math_root), config.database, str(config.endpoint), config.postgres_url, config.source]
    return hashlib.sha256(json.dumps(value).encode()).hexdigest()


def enqueue(config, capture_directory):
    directory = Path(capture_directory).resolve()
    if not (directory / "capture-complete.json").exists() or not (directory / "content.json").exists():
        raise ValueError("Only a durably completed capture can enter the database queue")
    key = hashlib.sha256((target_id(config) + "\n" + str(directory)).encode()).hexdigest()
    path = config.spool_root / (key + ".json")
    with file_lock(config.spool_root / "enqueue.lock"):
        if not path.exists():
            atomic_json(path, {"capture_directory": str(directory), "account": config.account,
                "target_id": target_id(config), "created_ns": time.time_ns(), "status": "pending",
                "attempts": 0, "next_attempt_at": 0, "capture_only": config.capture_only})
    return path


class DatabaseWorker:
    def __init__(self, config, stop_event, pipeline_factory):
        self.config, self.stop_event, self.pipeline_factory = config, stop_event, pipeline_factory
        self.thread = None

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        self.thread = threading.Thread(target=self.run, daemon=True, name="capture-database")
        self.thread.start()

    def pending(self):
        items = []
        for path in self.config.spool_root.glob("*.json"):
            item = read_json(path, {})
            if item.get("target_id") == target_id(self.config) and item.get("status") not in FINAL and not item.get("capture_only"):
                items.append((path, item))
        return sorted(items, key=lambda pair: (pair[1]["created_ns"], pair[0].name))

    def requeue_catalog_dependencies(self, verified):
        """Retry older partial imports when a verified KP pool becomes available.

        Caller holds the database lock. This re-prepares retained source only;
        it never replays a lesson or changes a saved transaction request.
        """
        available = set()
        for directory, outcome in verified.items():
            if outcome.get('status') not in FINAL:
                continue
            omitted = {o.get('id') for o in outcome.get('omissions', [])}
            content = read_json(Path(directory) / 'content.json', {}) or {}
            available.update(q['math_academy_id'] for q in content.get('canonical_examples', [])
                             if q.get('math_academy_id') and q['math_academy_id'] not in omitted)
        if not available:
            return []
        queued = []
        for path in self.config.spool_root.glob('*.json'):
            item = read_json(path, {}) or {}
            if (item.get('target_id') != target_id(self.config) or item.get('status') not in FINAL
                    or item.get('capture_only')):
                continue
            dependencies = {o.get('id') for o in item.get('result', {}).get('omissions', [])
                            if o.get('reason') == 'New KP lacks a complete example and practice pool'}
            ready = (dependencies & available) - set(item.get('catalog_dependency_checks', []))
            directory = Path(item['capture_directory'])
            if not ready or (directory / 'database/request.json').exists():
                continue
            item.update(status='pending', next_attempt_at=0,
                        catalog_dependency_checks=sorted(set(item.get('catalog_dependency_checks', [])) | ready),
                        dependency_recovery={'examples': sorted(ready), 'queued_at': time.time()})
            atomic_json(path, item)
            atomic_json(directory / 'import-status.json', item)
            queued.append(str(directory))
        return queued

    @property
    def batch_root(self):
        return self.config.spool_root / 'batches' / target_id(self.config)

    def _batch(self, pipeline, candidates, active, force):
        active_path = self.batch_root / 'active.json'
        if active:
            if active.get('next_attempt_at', 0) > time.time():
                return {'status': 'waiting', 'batch_directory': active['directory']}
        else:
            from .database.batch import question_ids
            questions = set()
            for _, item in candidates:
                questions.update(question_ids(read_json(Path(item['capture_directory']) / 'content.json', {})))
            if not force and len(questions) < self.config.database_batch_questions:
                return {'status': 'accumulating', 'activities': len(candidates), 'questions': len(questions),
                        'minimum_questions': self.config.database_batch_questions}
            selected = [str(path) for path, _ in candidates]
            active = {'directory': str(self.batch_root / str(uuid.uuid4())), 'spool_paths': selected,
                      'attempts': 0, 'next_attempt_at': 0}
            atomic_json(active_path, active)
        active['attempts'] += 1
        active['last_attempt_at'] = time.time()
        atomic_json(active_path, active)
        directories = [read_json(Path(path))['capture_directory'] for path in active['spool_paths']]
        result = pipeline.process_batch(directories, Path(active['directory']), allow_underfilled=force)
        if result.get('status') not in FINAL | {'pending', 'accumulating'}:
            raise ValueError('Database batch returned an unknown completion state')
        if result['status'] == 'accumulating':
            # No submitted intent was created. Reconsider the whole queue next
            # time, so new independent activities can complete this group.
            active_path.unlink()
            from .storage import _sync_directory
            _sync_directory(self.batch_root)
            return result
        outcomes = result.get('activities', {})
        verified = {}
        if not outcomes and result['status'] == 'pending':
            outcomes = {directories[0]: result}
        for path in active['spool_paths']:
            item = read_json(Path(path))
            outcome = outcomes.get(item['capture_directory'])
            if outcome is None:
                continue  # The safe prefix stopped before this activity.
            if outcome['status'] in FINAL and outcome.get('content_sha256'):
                from .database.prepare import digest
                current = pipeline._with_post_activity_base(read_json(Path(item['capture_directory']) / 'content.json'),
                                                            item['capture_directory'])
                if digest(current) != outcome['content_sha256']:
                    outcome = {'status': 'pending', 'reason': 'Capture changed after batch intent was saved',
                               'verified_previous_content': outcome}
            item.update(attempts=item['attempts'] + 1, last_attempt_at=active['last_attempt_at'],
                        status=outcome['status'], result=outcome,
                        batch_directory=active['directory'],
                        next_attempt_at=time.time() + backoff(active['attempts'], self.config.retry_delay, self.config.recovery_max_delay))
            item.pop('error', None)
            atomic_json(Path(path), item)
            atomic_json(Path(item['capture_directory']) / 'import-status.json', item)
            if item['status'] in FINAL:
                verified[item['capture_directory']] = outcome
        if result['status'] in FINAL:
            active_path.unlink()
            from .storage import _sync_directory
            _sync_directory(self.batch_root)
            self.requeue_catalog_dependencies(verified)
            logging.info('Database batch %s: %s complete activities, %s questions (%s)',
                         Path(active['directory']).name, len(outcomes), result.get('questions'), result.get('boundary'))
        else:
            active['next_attempt_at'] = time.time() + backoff(active['attempts'], self.config.retry_delay, self.config.recovery_max_delay)
            atomic_json(active_path, active)
            logging.warning('Database batch remains pending: %s', result.get('reason', 'unverified outcome'))
        return result

    def process_one(self, force=False):
        if self.config.capture_only:
            return {"status": "capture_only"}
        try:
            with file_lock(self.config.database_lock, blocking=False):
                candidates = self.pending()
                active = read_json(self.batch_root / 'active.json')
                if not candidates and not active:
                    return {"status": "idle"}
                pipeline = self.pipeline_factory()
                if active:
                    return self._batch(pipeline, candidates, active, force)
                # Recover unknown writes first. Batch selection also preserves
                # the order of related revisions while gathering independent work.
                unresolved = [pair for pair in candidates
                              if (Path(pair[1]["capture_directory"]) / "database/request.json").exists()]
                path, item = (unresolved or candidates)[0]
                if item.get("next_attempt_at", 0) > time.time():
                    return {"status": "waiting", "capture_directory": item["capture_directory"]}
                if not unresolved and hasattr(pipeline, 'process_batch'):
                    return self._batch(pipeline, candidates, None, force)
                directory = Path(item["capture_directory"])
                item["attempts"] += 1
                item["last_attempt_at"] = time.time()
                atomic_json(path, item)
                try:
                    result = pipeline.process(directory, apply=True)
                    if result.get("status") not in FINAL | {"pending", "previewed"}:
                        raise ValueError("Database pipeline returned an unknown completion state")
                    item["status"] = result["status"] if result["status"] in FINAL else "pending"
                    item["result"] = result
                    item.pop("error", None)
                except StopRequested:
                    raise
                except Exception as error:
                    item["status"] = "pending"
                    item["error"] = {"type": type(error).__name__, "message": str(error)[:1200]}
                    logging.warning("Database work remains pending for %s: %s", directory.name, type(error).__name__)
                item["next_attempt_at"] = time.time() + backoff(item["attempts"], self.config.retry_delay, self.config.recovery_max_delay)
                atomic_json(path, item)
                atomic_json(directory / "import-status.json", item)
                if item['status'] in FINAL:
                    self.requeue_catalog_dependencies({str(directory): item['result']})
                return item
        except BlockingIOError:
            return {"status": "another_worker"}

    def run(self, force=False):
        failures = 0
        while not self.stop_event.is_set():
            try:
                result = self.process_one(force=force)
                failures = 0
                wait(self.stop_event, 0.1 if result.get("status") in FINAL else self.config.retry_delay)
            except StopRequested:
                return
            except Exception as error:
                failures += 1
                logging.exception("Database worker recovering from %s", type(error).__name__)
                try:
                    wait(self.stop_event, backoff(failures, self.config.retry_delay, self.config.recovery_max_delay))
                except StopRequested:
                    return
