"""Reuse only immutable, scoped provenance reads; current readbacks stay fresh."""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from database import Database
from edn import loads


class HistoricalEvidenceTests(unittest.TestCase):
    def test_repeated_as_of_read_reuses_evidence_and_retains_each_import_readback(self):
        with tempfile.TemporaryDirectory() as work:
            db=Database(SimpleNamespace(database='fixture',endpoint='fixture.sock'))
            db.query=Mock(return_value=[[{':question/math-academy-id':'q-1',':question/problem':'original'}]])
            first=db.questions(['q-1'],Path(work)/'one','basis-3',3,immutable_evidence=True)
            first['q-1'][':question/problem']='mutated caller result'
            second=db.questions(['q-1'],Path(work)/'two','basis-3',3,immutable_evidence=True)
            self.assertEqual(second['q-1'][':question/problem'],'original')
            self.assertEqual(db.query.call_count,1)
            self.assertEqual(loads((Path(work)/'two/basis-3.edn').read_text()),[[second['q-1']]])
            # Normal committed content verification still performs a fresh read.
            db.questions(['q-1'],Path(work)/'current',basis=3)
            self.assertEqual(db.query.call_count,2)

    def test_new_question_basis_or_database_requires_new_query(self):
        with tempfile.TemporaryDirectory() as work:
            db=Database(SimpleNamespace(database='fixture',endpoint='fixture.sock'))
            db.query=Mock(return_value=[])
            for ids,basis in [(['q-1'],3),(['q-1'],3),(['q-1','q-2'],3),(['q-1'],4)]:
                db.questions(ids,Path(work),'evidence',basis,immutable_evidence=True)
            self.assertEqual(db.query.call_count,3)
            self.assertEqual(db.query.call_args_list[1].args[1],[['q-2']])
            db.args.database='another'
            db.questions(['q-1'],Path(work),'evidence',3,immutable_evidence=True)
            self.assertEqual(db.query.call_count,4)
            with self.assertRaisesRegex(ValueError,'explicit immutable basis'):
                db.questions(['q-1'],Path(work),immutable_evidence=True)
