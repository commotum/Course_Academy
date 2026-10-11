"""Save expanded source queue observations before making a selection."""
from pathlib import Path
import time

from .models import normalize_activity
from .storage import atomic_json, read_json


def read_queue(browser, directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    started_at = time.time()
    raw = browser.queue(directory)
    evidence = read_json(directory / "queue.json", {})
    if evidence.get("captured_at", 0) < started_at:
        evidence = {}
    queue, unreadable = [], []
    for position, record in enumerate(raw):
        try:
            queue.append(normalize_activity(record, position))
        except (ValueError, TypeError) as error:
            unreadable.append({"position": position, "record": record, "error": str(error)})
    atomic_json(directory / "queue.json", {**evidence, "observed_at": time.time(), "activities": queue, "unreadable": unreadable})
    return queue
