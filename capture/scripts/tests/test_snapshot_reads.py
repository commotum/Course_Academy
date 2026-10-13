import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from scripts.database.client import SnapshotReads
from scripts.runtime import StopRequested


class SnapshotReadTests(unittest.TestCase):
    def test_identical_parallel_reads_execute_once_and_return_isolated_values(self):
        entered, release = threading.Event(), threading.Event()
        def query(*args):
            entered.set()
            self.assertTrue(release.wait(5))
            return [[{'value': ['original']}]]
        client = SimpleNamespace(status=lambda: {'lineage':'same','basis':7},
                                 query=Mock(side_effect=query),stop_event=threading.Event())
        reader = SnapshotReads(client, 7)
        with tempfile.TemporaryDirectory() as tmp, ThreadPoolExecutor(max_workers=4) as pool:
            paths = [Path(tmp)/str(i) for i in range(4)]
            futures = [pool.submit(reader.query,'fixed EDN', ['same-input'],p,'read',7) for p in paths]
            self.assertTrue(entered.wait(5))
            release.set()
            results = [f.result() for f in futures]
            self.assertEqual(client.query.call_count,1)
            results[0][0][0]['value'].append('changed')
            self.assertEqual(results[1][0][0]['value'],['original'])
            for p in paths[1:]:
                self.assertEqual((p/'read-query.edn').read_text(),'fixed EDN')
                self.assertTrue((p/'read.edn').is_file())

    def test_inputs_and_basis_changes_cannot_reuse_an_unrelated_value(self):
        client = SimpleNamespace(status=lambda: {'lineage':'same','basis':7},
                                 query=Mock(return_value=[['value']]))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            reader = SnapshotReads(client,7)
            reader.query('query',[1],path,'one',7)
            reader.query('query',[2],path,'two',7)
            with self.assertRaises(ValueError):
                reader.query('query',[1],path,'wrong-basis',8)
            SnapshotReads(client,8).query('query',[1],path,'new-basis',8)
        self.assertEqual(client.query.call_count,3)

    def test_cached_reads_still_respect_a_manual_stop(self):
        client = SimpleNamespace(status=lambda: {'lineage':'same','basis':7},
                                 query=Mock(return_value=[]),stop_event=threading.Event())
        with tempfile.TemporaryDirectory() as tmp:
            reader=SnapshotReads(client,7)
            reader.query('query',[],Path(tmp),'first',7)
            client.stop_event.set()
            with self.assertRaises(StopRequested):
                reader.query('query',[],Path(tmp),'cached',7)
        self.assertEqual(client.query.call_count,1)
