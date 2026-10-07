"""Repeated queue observations must not reset a blocked repair's budget."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from capture_repair import evidence_version, failure_key, next_failure, source_version
from core import atomic_json


class RetryEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.reader = self.root/'edb'
        self.reader.write_bytes(b'compatible-reader')
        self.args = SimpleNamespace(output=self.root/'captures',state_dir=self.root/'state',
                                    edb_bin=str(self.reader))

    def diagnostic(self, number, stderr='ERROR code=tree/unsupported-version'):
        source = self.args.state_dir/'diagnostics'/str(number)/'error.json'
        source.parent.mkdir(parents=True,exist_ok=True)
        atomic_json(source, {'phase':'queue','task_id':None,'exception_type':'CalledProcessError',
                             'message':'EDB query exited with status 1','stderr':stderr})
        (source.parent/'page.html').write_text('Queue observation '+str(number))
        return source

    def ledger(self, source):
        return {failure_key(json.loads(source.read_text())):
                {'status':'blocked','attempts':2,'source_version':source_version(),
                 'evidence_version':evidence_version(source,self.reader)}}

    def test_new_diagnostic_and_queue_html_do_not_repeat_blocked_diagnosis(self):
        first = self.diagnostic(1)
        ledger = self.ledger(first)
        for number in range(2,8):
            later = self.diagnostic(number)
            self.assertEqual(evidence_version(first,self.reader),evidence_version(later,self.reader))
        self.assertIsNone(next_failure(self.args,ledger))

    def test_changed_reader_reopens_recovery(self):
        source = self.diagnostic(1)
        ledger = self.ledger(source)
        self.reader.write_bytes(b'replacement-compatible-reader')
        self.assertEqual(next_failure(self.args,ledger)[0],source)

    def test_changed_database_error_reopens_diagnosis(self):
        source = self.diagnostic(1)
        ledger = self.ledger(source)
        later = self.diagnostic(2,'ERROR code=storage/unavailable')
        self.assertEqual(next_failure(self.args,ledger)[0],later)

    def test_unchanged_activity_checkpoint_does_not_change_with_diagnostic_path(self):
        directory = self.args.output/'17'
        paths = []
        for number in (1,2):
            source = directory/'diagnostics'/str(number)/'error.json'
            source.parent.mkdir(parents=True,exist_ok=True)
            atomic_json(source,{'phase':'activity','task_id':17,'exception_type':'ValueError',
                               'message':'Unknown visible widget'})
            atomic_json(directory/'state.json',{'task_id':17,'questions':{},
                                               'deferred_error':{'diagnostics':str(source.parent)}})
            paths.append(source)
        self.assertEqual(evidence_version(paths[0]),evidence_version(paths[1]))
        original = evidence_version(paths[1])
        atomic_json(directory/'state.json',{'task_id':17,'questions':{'q-1':{'actual_result':'Correct'}}})
        self.assertNotEqual(original,evidence_version(paths[1]))


if __name__ == '__main__':
    unittest.main()
