import contextlib
import io
from pathlib import Path
import tempfile
import threading
import unittest

from scripts.cli import configuration, parser
from scripts.config import Config
from scripts.context import ContextProvider
from scripts.database.client import EDBClient
from scripts.database.pipeline import DatabasePipeline
from scripts.runtime import StopRequested
from scripts.selection import choose
from scripts.storage import atomic_json


class TargetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = Config(repo_root=self.root, profile=self.root / 'profile')
        self.state = {'targets': ['8'], 'basis': 10, 'completed': False}
        outer = self

        class Client(EDBClient):
            def basis(self):
                return outer.state['basis']

            def query(self, source, inputs, directory, name, basis=None):
                outer.assertEqual(name, 'learner-targets')
                outer.assertIn(':learner/targets', source)
                outer.assertNotIn(':learner/assignments', source)
                outer.assertNotIn(':learner/activity', source)
                outer.assertEqual(inputs, [outer.config.learner_id])
                outer.assertEqual(basis, outer.state['basis'])
                return [[int(target)] for target in outer.state['targets']]

        self.client = Client(self.config, threading.Event())

        class Pipeline:
            def context(self, activity):
                # The old graph cache may contain assignment-derived targets.
                return {'graph': {'1': ['8'], '2': ['9']}, 'basis': 9,
                        'targets': ['8', '9'], 'target_origins': {'assignment_targets': ['8', '9']}}

            def targets(self):
                return outer.client.targets(outer.root / 'reads')

        self.provider = ContextProvider(self.config, Pipeline)
        self.queue = [{'task_id': '1', 'topic_id': '1', 'kind': 'lesson'},
                      {'task_id': '2', 'topic_id': '2', 'kind': 'review'}]

    def context(self):
        return self.provider({'course_id': '55'})

    def test_target_addition_and_removal_change_selection_without_waiting_for_graph_refresh(self):
        first = self.context()
        self.assertEqual(first['targets'], ['8'])
        self.assertEqual(choose(self.queue, first)['task_id'], '1')
        self.state.update(targets=['9'], basis=11)
        second = self.context()
        self.assertEqual(second['targets'], ['9'])
        selection = choose(self.queue, second)
        self.assertEqual(selection['task_id'], '2')
        self.assertEqual(selection['selection']['target_basis'], 11)
        self.assertEqual(second['basis'], first['basis'])  # Graph cache has not refreshed.
        self.state.update(targets=[], basis=12)
        third = self.context()
        self.assertEqual(third['targets'], [])
        self.assertEqual(choose(self.queue, third)['task_id'], '1')
        self.assertEqual(choose(self.queue, third)['selection']['score'], 0)

    def test_assignment_completion_changes_neither_targets_nor_scores(self):
        before = self.context()
        score = choose(self.queue, before)['selection']['score']
        self.state.update(completed=True, basis=11)
        after = self.context()
        self.assertEqual(after['targets'], before['targets'])
        self.assertEqual(after['target_origins'], {'learner_targets': ['8']})
        self.assertEqual(choose(self.queue, after)['selection']['score'], score)

    def test_outage_retains_persisted_target_cache_but_never_old_assignment_union(self):
        before = self.context()
        self.client.basis = lambda: (_ for _ in ()).throw(ConnectionError('offline'))
        after = self.context()
        self.assertEqual(after['targets'], before['targets'])
        self.assertTrue(after['targets_unavailable'])
        # Switching learners cannot reuse either learner targets or old graph targets.
        self.config.learner_id = 'another-learner'
        self.assertEqual(self.context()['targets'], [])

    def test_config_and_cli_cannot_override_persisted_targets(self):
        path = self.root / 'config.json'
        atomic_json(path, {'targets': ['8']})
        with self.assertRaisesRegex(ValueError, ':learner/targets'):
            Config.from_file(path)
        with self.assertRaisesRegex(ValueError, ':learner/targets'):
            Config.from_file(None, targets=['8'])
        # An old, unused empty setting can be loaded without changing target behavior.
        atomic_json(path, {'targets': []})
        self.assertFalse(hasattr(Config.from_file(path), 'targets'))
        errors = io.StringIO()
        with contextlib.redirect_stderr(errors), self.assertRaises(SystemExit):
            parser().parse_args(['run', '--target', '8'])
        self.assertIn(':learner/targets', errors.getvalue())
        self.assertFalse(hasattr(configuration(parser().parse_args(['check'])), 'targets'))


class ExactQuestionBindingTests(unittest.TestCase):
    def test_exact_binding_query_is_scoped_and_pinned(self):
        calls=[]
        class Client(EDBClient):
            def __init__(self):pass
            def basis(self):return 17
            def query(self,source,inputs,directory,name,basis=None):
                calls.append((source,inputs,name,basis))
                return [[209],[209]]
        client=Client()
        with tempfile.TemporaryDirectory() as directory:
            config=Config(repo_root=Path(directory),profile=Path(directory)/'profile')
            pipeline=DatabasePipeline(config,threading.Event(),client=client)
            binding=pipeline.question_topic('q-391')
        self.assertEqual(binding['topic_id'],'209')
        self.assertEqual(binding['question_id'],'q-391')
        self.assertEqual(binding['basis'],17)
        self.assertEqual(binding['source'],'database_math_academy_question_binding')
        source,inputs,name,basis=calls[0]
        self.assertEqual(inputs,['q-391'])
        self.assertEqual((name,basis),('question-topic',17))
        self.assertIn(':question/math-academy-id ?question _ ?source',source)
        self.assertIn(':org/Math-Academy',source)
        self.assertIn(':knowledge-point/questions',source)
        self.assertIn(':knowledge-point/canonical-example',source)
        self.assertNotIn(':course/',source)
        self.assertNotIn(':topic/next',source)
        self.assertNotIn(':learner/',source)

    def test_absent_and_ambiguous_binding_remain_unknown(self):
        class Client(EDBClient):
            def __init__(self):self.rows=[];self.calls=0
            def basis(self):self.calls+=1;return 17
            def query(self,*args):return self.rows
        client=Client()
        for source_id in (None,'','391','unavailable'):
            self.assertIsNone(client.question_topic(source_id,Path('/tmp')))
        self.assertEqual(client.calls,0)
        self.assertIsNone(client.question_topic('q-391',Path('/tmp')))
        client.rows=[[209],[210]]
        self.assertIsNone(client.question_topic('q-391',Path('/tmp')))

    def test_provider_uses_lookup_and_falls_back_when_database_is_unavailable(self):
        calls=[]
        class Pipeline:
            def question_topic(_,source_id):
                calls.append(source_id)
                if source_id=='q-1':return {'question_id':source_id,'topic_id':'209','basis':17,'source':'database_math_academy_question_binding'}
                if source_id=='q-2':raise ConnectionError('offline')
                if source_id=='q-3':raise StopRequested()
                return None
        with tempfile.TemporaryDirectory() as directory:
            config=Config(repo_root=Path(directory),profile=Path(directory)/'profile')
            provider=ContextProvider(config,Pipeline)
            self.assertIsNone(provider.question_topic(None))
            self.assertEqual(provider.question_topic('q-1')['topic_id'],'209')
            self.assertIsNone(provider.question_topic('q-2'))
            self.assertIsNone(provider.question_topic('q-4'))
            with self.assertRaises(StopRequested):provider.question_topic('q-3')
        self.assertEqual(calls,['q-1','q-2','q-4','q-3'])


if __name__ == '__main__':
    unittest.main()
