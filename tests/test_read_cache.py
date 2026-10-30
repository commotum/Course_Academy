"""Page responses remain responsive when their database refresh stalls."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
import threading
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from read_cache import ReadCache


class ReadCacheTests(unittest.TestCase):
    def test_cached_page_returns_during_blocked_refresh_and_coalesces(self):
        cache = ReadCache(fresh_seconds=0)
        self.assertEqual(cache.request('page', lambda: {'ok': True, 'data': [1]})['data'], [1])
        entered, release = threading.Event(), threading.Event()
        calls = []
        def blocked():
            calls.append(1)
            entered.set()
            release.wait(3)
            return {'ok': True, 'data': [2]}
        try:
            with ThreadPoolExecutor() as pool:
                self.assertEqual(pool.submit(cache.request, 'page', blocked).result(timeout=.5)['data'], [1])
                self.assertTrue(entered.wait(.5))
                for _ in range(10):
                    self.assertEqual(pool.submit(cache.request, 'page', blocked).result(timeout=.5)['data'], [1])
                self.assertEqual(calls, [1])
                # Results are caller-owned, never mutable references to cache.
                cache.request('page', blocked)['data'].append(99)
                self.assertEqual(cache.request('page', blocked)['data'], [1])
        finally:
            release.set()

    def test_cold_reads_coalesce_and_errors_are_not_cached(self):
        cache = ReadCache()
        calls = []
        entered, release = threading.Event(), threading.Event()
        def load():
            calls.append(1)
            entered.set()
            release.wait(2)
            return {'ok': False, 'error': 'offline'}
        with ThreadPoolExecutor() as pool:
            first = pool.submit(cache.request, 'page', load)
            self.assertTrue(entered.wait(.5))
            second = pool.submit(cache.request, 'page', load)
            release.set()
            self.assertFalse(first.result(timeout=1)['ok'])
            self.assertFalse(second.result(timeout=1)['ok'])
        self.assertEqual(cache.entries, {})
        self.assertTrue(cache.request('page', lambda: {'ok': True})['ok'])

    def test_invalidation_does_not_publish_an_inflight_old_result(self):
        cache = ReadCache()
        entered, release = threading.Event(), threading.Event()
        def load():
            entered.set()
            release.wait(2)
            return {'ok': True, 'data': 'old'}
        with ThreadPoolExecutor() as pool:
            result = pool.submit(cache.request, 'page', load)
            self.assertTrue(entered.wait(.5))
            cache.invalidate()
            release.set()
            result.result(timeout=1)
        self.assertNotIn('page', cache.entries)
        self.assertEqual(cache.request('page', lambda: {'ok': True, 'data': 'new'})['data'], 'new')

    def test_expired_stale_data_is_not_returned_and_memory_is_bounded(self):
        cache = ReadCache(fresh_seconds=0, max_stale_seconds=0, max_entries=2)
        for value in range(3):
            cache.request(str(value), lambda: {'ok': True, 'data': value})
        self.assertEqual(list(cache.entries), ['1', '2'])
        self.assertFalse(cache.request('2', lambda: {'ok': False})['ok'])
        tiny = ReadCache(max_bytes=1)
        tiny.request('x', lambda: {'ok': True})
        self.assertFalse(tiny.entries)


if __name__ == '__main__':
    unittest.main()
