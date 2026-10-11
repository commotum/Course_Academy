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


if __name__ == '__main__':
    unittest.main()
