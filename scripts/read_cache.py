"""Bounded last-good page responses with coalesced background refresh.

Only read-only, display data belongs here. Task state, grading, and mutation
preconditions must always use their authoritative or locally journaled state.
"""
from collections import OrderedDict
import copy
import json
import threading
import time


class ReadCache:
    def __init__(self, *, fresh_seconds=1, max_stale_seconds=60,
                 max_entries=128, max_bytes=32 * 1024 * 1024):
        self.fresh_seconds = fresh_seconds
        self.max_stale_seconds = max_stale_seconds
        self.max_entries, self.max_bytes = max_entries, max_bytes
        self.entries = OrderedDict()
        self.pending = {}
        self.lock = threading.Lock()
        self.bytes = 0
        self.generation = 0

    def invalidate(self):
        # Preserve the last good page while a fresh projection is prepared.
        # A read begun before this mutation must not become the fresh result.
        with self.lock:
            self.generation += 1

    def _load(self, key, loader, pending, generation):
        try:
            result = loader()
            pending['result'] = result
            if result.get('ok'):
                size = len(json.dumps(result, separators=(',', ':')).encode())
                with self.lock:
                    if size <= self.max_bytes and generation == self.generation:
                        old = self.entries.pop(key, None)
                        if old:
                            self.bytes -= old[2]
                        self.entries[key] = (time.monotonic(), copy.deepcopy(result), size, generation)
                        self.bytes += size
                        while len(self.entries) > self.max_entries or self.bytes > self.max_bytes:
                            _, entry = self.entries.popitem(last=False)
                            self.bytes -= entry[2]
        except Exception as error:
            pending['error'] = error
        finally:
            with self.lock:
                self.pending.pop(key, None)
                pending['done'].set()

    def request(self, key, loader):
        with self.lock:
            entry = self.entries.get(key)
            age = time.monotonic() - entry[0] if entry else float('inf')
            if entry:
                self.entries.move_to_end(key)
            if entry and age < self.fresh_seconds and entry[3] == self.generation:
                return copy.deepcopy(entry[1])
            pending = self.pending.get(key)
            if pending is None:
                pending = {'done': threading.Event()}
                self.pending[key] = pending
                threading.Thread(target=self._load,
                                 args=(key, loader, pending, self.generation), daemon=True).start()
            if entry and age < self.max_stale_seconds:
                return copy.deepcopy(entry[1])
        # First load (or an expired snapshot) shares the one pending read.
        pending['done'].wait()
        if 'error' in pending:
            raise pending['error']
        return copy.deepcopy(pending['result'])
