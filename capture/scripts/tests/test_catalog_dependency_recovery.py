"""A later verified pool unblocks retained topic source without replaying tasks."""
import json
from pathlib import Path
import tempfile
import threading
import unittest

from scripts.config import Config
from scripts.outbox import DatabaseWorker, enqueue
from scripts.storage import atomic_json, read_json


class CatalogDependencyRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.config = Config(repo_root=Path(self.temp.name), math_root=Path(self.temp.name)/'math')
        self.worker = DatabaseWorker(self.config, threading.Event(), lambda: None)
        self.old = self.config.output_root/'old'
        self.new = self.config.output_root/'new'
        for directory in (self.old, self.new):
            atomic_json(directory/'content.json', {'canonical_examples': [{'math_academy_id': 'e-20'}]})
            atomic_json(directory/'capture-complete.json', {'completed_at': 1})
        self.spool = enqueue(self.config, self.old)
        self.item = read_json(self.spool)
        self.item.update(status='verified', result={'status': 'verified', 'omissions': [
            {'kind': 'question', 'id': 'e-20', 'reason': 'New KP lacks a complete example and practice pool', 'final': True}]})
        atomic_json(self.spool, self.item)
        self.seed = {str(self.new): {'status': 'verified', 'omissions': []}}

    def test_verified_pool_requeues_source_and_keeps_original_omission_visible(self):
        marker = (self.old/'capture-complete.json').read_bytes()
        self.assertEqual(self.worker.requeue_catalog_dependencies(self.seed), [str(self.old)])
        item = read_json(self.spool)
        self.assertEqual(item['status'], 'pending')
        self.assertEqual(item['next_attempt_at'], 0)
        self.assertEqual(item['catalog_dependency_checks'], ['e-20'])
        self.assertEqual(item['result'], self.item['result'])
        self.assertEqual((self.old/'capture-complete.json').read_bytes(), marker)
        self.assertFalse((self.config.state_root/'xp.json').exists())
        item['status'] = 'verified'
        atomic_json(self.spool, item)
        self.assertEqual(self.worker.requeue_catalog_dependencies(self.seed), [])

    def test_omitted_or_unverified_pool_cannot_trigger_recovery(self):
        for outcome in [{'status': 'pending'}, {'status': 'verified', 'omissions': [{'id': 'e-20'}]}]:
            with self.subTest(outcome=outcome):
                self.assertEqual(self.worker.requeue_catalog_dependencies({str(self.new): outcome}), [])
                self.assertEqual(read_json(self.spool)['status'], 'verified')

    def test_exact_pending_request_and_unrelated_source_failure_are_preserved(self):
        request = self.old/'database/request.json'
        atomic_json(request, {'request_key': 'saved-exact-intent'})
        original = request.read_bytes()
        self.assertEqual(self.worker.requeue_catalog_dependencies(self.seed), [])
        self.assertEqual(request.read_bytes(), original)
        request.unlink()
        self.item['result']['omissions'][0]['reason'] = 'Image unavailable'
        atomic_json(self.spool, self.item)
        self.assertEqual(self.worker.requeue_catalog_dependencies(self.seed), [])


if __name__ == '__main__':
    unittest.main()
