"""Unresolved source identities must not pin the ordered database outbox."""
from copy import deepcopy
from pathlib import Path
import tempfile
import threading
import unittest

from scripts.config import Config
from scripts.database.evidence import UnsupportedContent
from scripts.database.pipeline import DatabasePipeline
from scripts.database.prepare import Preparation, activity_identity
from scripts.outbox import DatabaseWorker, enqueue
from scripts.storage import atomic_json, read_json
from scripts.tests.test_database import QueryBackedFakeClient, question, source_snapshot


def unresolved(key, problem, *, null_id=False):
    q = {'source_id': key, 'problem': problem, 'observed_math_academy_id': 'q-99',
         'topic_id': 1, 'fields': [{'key': 'x', 'type': 'blank'}]}
    if null_id:
        q['math_academy_id'] = None
    return q


def final(key, reason, kind='questions'):
    return {'capture_key': key, 'question_id': None, 'record_kind': kind,
            'final': True, 'status': 'unavailable', 'reasoning': reason, 'answers': []}


def captured():
    supported = question()
    supported['knowledge_point_id'] = str(source_snapshot()['entities'][1][':knowledge-point/id'])
    return {'kind': 'review', 'topic_id': 1, 'course_id': 7,
            'questions': [unresolved('unreconciled:one', 'First uncertain source'),
                          unresolved('unreconciled:two', 'Second uncertain source', null_id=True), supported],
            'judgments': [final('unreconciled:one', 'First source identity unavailable'),
                          final('unreconciled:two', 'Second source identity unavailable')]}


class UnreconciledPreparationTests(unittest.TestCase):
    def test_every_unresolved_original_gets_its_own_judgment_and_supported_content_survives(self):
        content = captured()
        original = deepcopy(content)
        result = Preparation(source_snapshot()).prepare(content)
        omitted = [o for o in result['omissions'] if o['kind'] == 'question']
        self.assertEqual([o['capture_key'] for o in omitted], ['unreconciled:one', 'unreconciled:two'])
        self.assertEqual([o['judgment']['reasoning'] for o in omitted],
                         ['First source identity unavailable', 'Second source identity unavailable'])
        self.assertEqual([o['observed_math_academy_id'] for o in omitted], ['q-99', 'q-99'])
        self.assertEqual([q['math_academy_id'] for q in result['content']['questions']], ['q-11'])
        attributes = [str(row[1]) for batch in result['batches'] for row in batch['assertions']]
        self.assertIn(':question/problem', attributes)
        self.assertNotIn(':activity/steps', attributes)
        self.assertTrue(any(o['kind'] == 'review' for o in result['omissions']))
        self.assertEqual(content, original)

    def test_capture_key_judgment_fallback_does_not_cross_record_kinds(self):
        content = {'judgments': [final('unreconciled:one', 'Wrong example', 'canonical_examples'),
                                final('unreconciled:one', 'Right question')]}
        result = Preparation(source_snapshot()).final_judgment(content,
            unresolved('unreconciled:one', 'Question'), UnsupportedContent('Missing identity'))
        self.assertEqual(result['reasoning'], 'Right question')

    def test_missing_key_cannot_reuse_an_unrelated_null_id_judgment(self):
        calls = []
        def resolve(task, payload):
            calls.append(payload['question']['source_id'])
            return final(payload['question']['source_id'], 'Resolved this source')
        result = Preparation(source_snapshot(), resolve=resolve).final_judgment(
            {'judgments': [final('unreconciled:first', 'Unrelated')]},
            unresolved('unreconciled:second', 'Second'), UnsupportedContent('Missing identity'))
        self.assertEqual(calls, ['unreconciled:second'])
        self.assertEqual(result['reasoning'], 'Resolved this source')

    def test_snapshot_ignores_unverified_ids_and_existing_route_uuid_is_unchanged(self):
        content = captured()
        old_shape = {'questions': [question()], 'topic_id': 1, 'course_id': 7}
        explicit_order = {**old_shape, 'question_order': ['q-11']}
        self.assertEqual(activity_identity(old_shape, 'review'), activity_identity(explicit_order, 'review'))
        self.assertEqual(activity_identity(content, 'review'), activity_identity(deepcopy(content), 'review'))
        client = QueryBackedFakeClient()
        with tempfile.TemporaryDirectory() as directory:
            client.snapshot(content, Path(directory), 1)
        reads = [inputs for name, inputs, *_ in client.queries if name == 'questions-0']
        self.assertEqual(reads, [[['q-11']]])

    def test_outbox_imports_supported_content_and_moves_on_after_unresolved_omissions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = Config(repo_root=root, math_root=root / 'math', retry_delay=.01)
            stop = threading.Event()
            client = QueryBackedFakeClient()
            first, second = config.output_root / 'first', config.output_root / 'second'
            for target, content in ((first, captured()), (second, {'kind': 'review', 'topic_id': 1,
                    'questions': [{**captured()['questions'][-1], 'math_academy_id': 'q-12'}]})):
                atomic_json(target / 'capture-complete.json', {'task_id': target.name})
                atomic_json(target / 'content.json', content)
                enqueue(config, target)
            pipeline = lambda: DatabasePipeline(config, stop, client=client)
            worker = DatabaseWorker(config, stop, pipeline)
            first_result = worker.process_one()
            self.assertEqual(first_result['status'], 'verified')
            self.assertEqual(len([o for o in first_result['result']['omissions'] if o['kind'] == 'question']), 2)
            second_result = worker.process_one()
            self.assertEqual(second_result['status'], 'verified')
            self.assertEqual(Path(second_result['capture_directory']), second)
            self.assertFalse(worker.pending())
            no_changes = pipeline().process(first)
            self.assertEqual(no_changes['status'], 'no_changes')
            stored_ids = {value for (entity, attr), values in client.facts.items()
                          if attr == 'question/math-academy-id' for value, source in values}
            self.assertTrue({'q-11', 'q-12'} <= stored_ids)
            self.assertFalse(any(str(value).startswith('unreconciled:') for value in stored_ids))
            self.assertEqual(read_json(first / 'content.json')['questions'][0]['observed_math_academy_id'], 'q-99')


if __name__ == '__main__':
    unittest.main()
