"""Ordered database persistence, independent of the live activity loop."""
from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
import threading
import time

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

    def process_one(self):
        if self.config.capture_only:
            return {"status": "capture_only"}
        try:
            with file_lock(self.config.database_lock, blocking=False):
                candidates = self.pending()
                if not candidates:
                    return {"status": "idle"}
                path, item = candidates[0]
                if item.get("next_attempt_at", 0) > time.time():
                    return {"status": "waiting", "capture_directory": item["capture_directory"]}
                directory = Path(item["capture_directory"])
                item["attempts"] += 1
                item["last_attempt_at"] = time.time()
                atomic_json(path, item)
                try:
                    result = self.pipeline_factory().process(directory, apply=True)
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
                return item
        except BlockingIOError:
            return {"status": "another_worker"}

    def run(self):
        failures = 0
        while not self.stop_event.is_set():
            try:
                result = self.process_one()
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
