"""Interruptible recovery; only explicit shutdown ends a running capture."""
from __future__ import annotations

import logging
import signal
from contextlib import contextmanager


class StopRequested(Exception):
    """A requested stop, distinct from an operational failure."""


def wait(stop_event, seconds):
    if stop_event.wait(max(0.0, float(seconds))):
        raise StopRequested()


def check_stop(stop_event):
    if stop_event.is_set():
        raise StopRequested()


def backoff(attempt, initial=2.0, maximum=60.0):
    return min(maximum, max(0.01, initial) * 2 ** min(max(0, attempt - 1), 12))


@contextmanager
def shutdown_signals(stop_event):
    previous = {}

    def request(signum, frame):
        logging.info("Stop requested; retaining the current activity checkpoint")
        stop_event.set()

    for signum in (signal.SIGINT, signal.SIGTERM):
        previous[signum] = signal.signal(signum, request)
    try:
        yield
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)
