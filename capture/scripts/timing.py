"""Shared pacing with interruptible waits and absolute deadline bounds."""
from __future__ import annotations

import logging
import math
import random
import time

from .runtime import check_stop, wait


class Pacer:
    def __init__(self, config, stop_event, *, clock=None, rng=None, sleeper=None):
        self.config, self.stop_event = config, stop_event
        self.clock = clock or time.time
        self.rng = rng or random.Random(getattr(config, 'seed', None))
        self.sleeper = sleeper

    def duration(self, kind, elapsed=0):
        if not math.isfinite(elapsed) or elapsed < 0:
            raise ValueError('Elapsed pacing credit must be finite and nonnegative')
        low = getattr(self.config, kind + '_min', 0)
        high = getattr(self.config, kind + '_max', low)
        return max(0, self.rng.uniform(low, high) - elapsed)

    def backoff(self, attempt, retry_after=0):
        """Return the original linear recovery delay with independent jitter."""
        base = min(getattr(self.config, 'recovery_max_delay', 180),
                   getattr(self.config, 'retry_delay', 30) * max(1, attempt))
        return max(0, retry_after, base) + self.rng.uniform(0, getattr(self.config, 'recovery_jitter', 0))

    def wait(self, kind, reason='', elapsed=0, deadline=None):
        delay = self.duration(kind, elapsed)
        if delay:
            logging.info('Waiting %.1fs (%s)', delay, reason or kind)
        return self.sleep(delay, deadline=deadline)

    def sleep(self, seconds, deadline=None):
        """Sleep at most until the epoch deadline; shutdown always wins."""
        if not math.isfinite(seconds):
            raise ValueError('Wait duration must be finite')
        check_stop(self.stop_event)
        remaining = max(0, seconds)
        slept = 0.0
        while remaining > 0:
            if deadline is not None:
                remaining = min(remaining, max(0, deadline - self.clock()))
            if remaining <= 0:
                break
            # Chunk custom sleepers too, so test clocks and real sleeps share
            # stop/deadline behavior without requiring a particular Event API.
            step = min(.25, remaining)
            if self.sleeper is None:
                wait(self.stop_event, step)
            else:
                self.sleeper(step)
            check_stop(self.stop_event)
            slept += step
            remaining = max(0, remaining - step)
        return slept
