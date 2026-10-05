"""Protected snapshots remain complete under bounded scalar EDB reads."""
import subprocess
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from database import Database, fingerprint
from edn import Symbol, dumps, kw, loads


class ProtectedReadTests(unittest.TestCase):
    def test_schema_predicate_symbols_roundtrip_without_becoming_strings(self):
        source='[[1 70 [course-academy.topic/valid-difficulty?]]]'
        rows=loads(source)
        self.assertIsInstance(rows[0][2][0],Symbol)
        self.assertEqual(dumps(rows),source)
        self.assertNotEqual(fingerprint(rows),fingerprint([[1,70,['course-academy.topic/valid-difficulty?']]]))
    def test_scalar_reads_preserve_all_noncontent_facts_and_basis(self):
        db = Database(SimpleNamespace())
        attributes = [(1,kw('question/problem')),(2,kw('learner/name')),
                      (3,kw('topic/next')),(4,kw('db/ident')),(5,kw('engine/new-setting'))]
        facts = {2:[[12,2,'Jake']],3:[[13,3,14],[15,3,16]],5:[[17,5,True]]}
        db.query = Mock(side_effect=lambda query,inputs,*args:facts[inputs[0]])
        with tempfile.TemporaryDirectory() as work:
            rows = db.protected(attributes,Path(work),'protected',657)
            self.assertEqual(rows,facts[2]+facts[3]+facts[5])
            self.assertEqual(loads((Path(work)/'protected.edn').read_text()),rows)
            self.assertEqual(fingerprint(rows),fingerprint(list(reversed(rows))))
        self.assertEqual([c.args[1] for c in db.query.call_args_list],[[2],[3],[5]])
        self.assertTrue(all(':in $ ?a' in c.args[0] and c.args[-1]==657 for c in db.query.call_args_list))

    def test_failed_partition_never_publishes_partial_snapshot(self):
        db = Database(SimpleNamespace())
        failure = subprocess.CalledProcessError(1,['edb'],stderr='query/read-failed')
        db.query = Mock(side_effect=[[[1,2,'before']],failure])
        with tempfile.TemporaryDirectory() as work:
            with self.assertRaises(subprocess.CalledProcessError):
                db.protected([(2,kw('learner/name')),(3,kw('policy/new'))],Path(work),'protected',657)
            self.assertFalse((Path(work)/'protected.edn').exists())

    def test_large_attribute_uses_bounded_subjects_without_raising_budget(self):
        db=Database(SimpleNamespace())
        budget=subprocess.CalledProcessError(1,['edb'],stderr='query/value-byte-limit')
        calls=[]
        def query(template,inputs,*args):
            calls.append((template,inputs,args[-1]))
            if inputs==[1029] and ':find ?e ?a ?v' in template:raise budget
            if inputs==[1029]:return [[i] for i in range(1,130)]
            if len(inputs[1])>32:raise budget
            return [[i,1029,'tutorial '+str(i)] for i in inputs[1]]
        db.query=Mock(side_effect=query)
        with tempfile.TemporaryDirectory() as work:
            rows=db.protected([(1029,kw('tutorial/content'))],Path(work),'protected',657)
        self.assertEqual(rows,[[i,1029,'tutorial '+str(i)] for i in range(1,130)])
        self.assertTrue(all(c[2]==657 for c in calls))
        self.assertTrue(all(len(c[1][1])<=64 for c in calls if len(c[1])==2))

    def test_missing_subject_in_partition_is_a_verification_error(self):
        db=Database(SimpleNamespace())
        failure=subprocess.CalledProcessError(1,['edb'],stderr='query/value-byte-limit')
        db.query=Mock(side_effect=[failure,[[1],[2]],[[1,1029,'one']]])
        with tempfile.TemporaryDirectory() as work:
            with self.assertRaisesRegex(ValueError,'Incomplete protected-fact'):
                db.protected([(1029,kw('tutorial/content'))],Path(work),'protected',657)
            self.assertFalse((Path(work)/'protected.edn').exists())

    def test_shutdown_aborts_before_another_protected_read(self):
        stop=threading.Event();stop.set()
        db=Database(SimpleNamespace(stop_event=stop));db.query=Mock()
        with tempfile.TemporaryDirectory() as work,self.assertRaises(KeyboardInterrupt):
            db.protected([(2,kw('learner/name'))],Path(work),'protected',657)
        db.query.assert_not_called()
