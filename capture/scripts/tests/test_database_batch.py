from contextlib import redirect_stdout
from copy import deepcopy
import io
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.config import Config
from scripts.database.client import StaleBasis
from scripts.database.batch import combine, size, union
from scripts.database.commit import VerificationError
from scripts.database.edn import kw
from scripts.database.pipeline import DatabasePipeline
from scripts.database.prepare import digest
from scripts.monitor_data import _import_ids
from scripts.outbox import DatabaseWorker, enqueue
from scripts.storage import atomic_json, read_json
from scripts.tests.test_database import QueryBackedFakeClient, question, source_snapshot


class SnapshotMergeTests(unittest.TestCase):
    def test_internal_aliases_do_not_merge_unrelated_sibling_paths(self):
        shared = ['original']
        left = {':first': shared, ':second': shared}
        self.assertEqual(union(left, {':first': ['new']}),
                         {':first': ['original', 'new'], ':second': ['original']})
        nested = {':db/id': 2, ':labels': shared}
        left = [{':db/id': 1, ':child': nested}, nested]
        merged = union(left, [{':db/id': 1, ':child': {':db/id': 2, ':labels': ['new']}}])
        self.assertEqual(merged[0][':child'][':labels'], ['original', 'new'])
        self.assertEqual(merged[1][':labels'], ['original'])
        self.assertEqual(shared, ['original'])

    def test_nested_union_is_independent_of_both_inputs(self):
        left = {':db/id': 1, ':ref': {':db/id': 2, ':name': 'retained'},
                ':items': [{':db/id': 3, ':labels': ['first']}], ':rows': [[1, 'x']]}
        right = {':db/id': 1, ':ref': 2,
                 ':items': [{':db/id': 3, ':labels': ['second']}, {':db/id': 4, ':labels': ['new']}],
                 ':rows': [[1, 'x'], [2, 'y']]}
        originals = deepcopy((left, right))
        merged = union(left, right)
        self.assertEqual(merged[':ref'], left[':ref'])
        self.assertEqual(merged[':items'][0][':labels'], ['first', 'second'])
        self.assertEqual(merged[':rows'], [[1, 'x'], [2, 'y']])
        merged[':ref'][':name'] = 'changed'
        merged[':items'][1][':labels'].append('changed')
        merged[':rows'][1].append('changed')
        self.assertEqual((left, right), originals)
        self.assertEqual(union(2, {':db/id': 2, ':name': 'full'}), {':db/id': 2, ':name': 'full'})

    def test_conflicting_nested_scalar_leaves_inputs_untouched(self):
        left = [{':db/id': 1, ':items': [{':db/id': 2, ':title': 'first'}]}]
        right = [{':db/id': 1, ':items': [{':db/id': 2, ':title': 'different'}]}]
        originals = deepcopy((left, right))
        with self.assertRaisesRegex(VerificationError, 'snapshots disagree'):
            union(left, right)
        self.assertEqual((left, right), originals)

    def test_combining_owned_aggregate_preserves_snapshots_and_prepared_forms(self):
        members = []
        for label in ['first', 'second']:
            snapshot = {'basis': 1, 'lineage': 'same', 'entities': [
                {':db/id': 1, ':items': [{':db/id': 2, ':labels': [label]}]}],
                'facts': [[1, ':labels', label, 5]], 'attributes': [], 'idents': []}
            prepared = {'batches': [{'source': ':source',
                'forms': [{kw('db/id'): 'same', kw('items'): [{':db/id': 2, ':labels': [label]}]}],
                'assertions': [['same', ':labels', label]], 'retractions': []}]}
            members.append(({}, prepared, snapshot))
        originals = deepcopy(members)
        batches, snapshot = combine(members)
        self.assertEqual(snapshot['entities'][0][':items'][0][':labels'], ['first', 'second'])
        self.assertEqual(batches[0]['forms'][0][kw('items')][0][':labels'], ['first', 'second'])
        snapshot['entities'][0][':items'][0][':labels'].append('changed')
        batches[0]['forms'][0][kw('items')][0][':labels'].append('changed')
        self.assertEqual(members, originals)

    def test_combine_detaches_aliases_in_initial_and_added_snapshots(self):
        shared = ['original']
        entity = {':db/id': 1, ':first': shared, ':second': shared}
        additions = [[], [entity]]
        for initial in additions:
            with self.subTest(initial=bool(initial)):
                snapshots = [{'basis': 1, 'lineage': 'same', 'entities': initial},
                             {'basis': 1, 'lineage': 'same', 'entities': [entity]},
                             {'basis': 1, 'lineage': 'same', 'entities': [{':db/id': 1, ':first': ['new']}]}]
                members = [({}, {'batches': []}, snapshot) for snapshot in snapshots]
                originals = deepcopy(members)
                _, snapshot = combine(members)
                self.assertEqual(snapshot['entities'], [
                    {':db/id': 1, ':first': ['original', 'new'], ':second': ['original']}])
                self.assertEqual(members, originals)


class BatchTests(unittest.TestCase):
    def test_parallel_cached_reads_preserve_atomic_commit_and_exact_receipt(self):
        from scripts.database.client import SnapshotReads
        self.client.snapshot_reader = lambda basis: SnapshotReads(self.client,basis)
        self.config.database_batch_questions=3
        directories=[self.capture(20,['q-11']),self.capture(21,['q-12']),self.capture(22,['q-13'])]
        result=self.pipeline.process_batch(directories,self.root/'batch')
        self.assertEqual(result['status'],'verified',result)
        self.assertEqual(len(self.client.receipts),1)
        self.assertEqual(self.client.t,2)
        initial_schema_reads=[q for q in self.client.queries if q[0]=='attributes' and q[2]==1]
        self.assertEqual(len(initial_schema_reads),1)
        for directory in directories:
            self.assertEqual(read_json(directory/'database/result.json')['status'],'verified')
        self.assertTrue(all(q[2] in (1,2) for q in self.client.queries))

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = Config(repo_root=self.root, math_root=self.root / 'math', retry_delay=.01,
                             database_batch_questions=1)
        self.stop = threading.Event()
        self.client = QueryBackedFakeClient()
        self.pipeline = DatabasePipeline(self.config, self.stop, client=self.client)
        self.worker = DatabaseWorker(self.config, self.stop, lambda: self.pipeline)

    def capture(self, task, mids, kind='multistep'):
        directory = self.config.output_root / str(task)
        qs = [question(mid) for mid in mids]
        for q in qs:
            q['knowledge_point_id'] = str(source_snapshot()['entities'][1][':knowledge-point/id'])
            q['local_problem'] = q['problem']
        content = {'task_type': kind, 'task_id': str(task), 'topic_id': 1, 'course_id': 7,
                   'questions': qs, 'question_order': mids, 'multistep_id': task,
                   'shared_context': 'Shared setup', 'question_outcomes': {mid: 'correct' for mid in mids}}
        atomic_json(directory / 'content.json', content)
        atomic_json(directory / 'capture-complete.json', {'complete': True})
        return directory

    def test_whole_multisteps_share_one_commit_and_each_has_exact_receipt(self):
        self.config.database_batch_questions = 3
        directories = [self.capture(20, ['q-11', 'q-12']), self.capture(21, ['q-13'])]
        result = self.pipeline.process_batch(directories, self.root / 'batch')
        self.assertEqual(result['status'], 'verified', result)
        self.assertEqual(len(result['activities']), 2)
        self.assertEqual(len(self.client.receipts), 1)
        self.assertEqual(self.client.t, 2)
        keys = set()
        for directory, expected in zip(directories, ({'q-11', 'q-12'}, {'q-13'})):
            archive = list((directory / 'database/requests').glob('*/request.json'))
            self.assertEqual(len(archive), 1)
            keys.add(read_json(archive[0])['request_key'])
            self.assertEqual(_import_ids({'capture_directory': str(directory), 'status': 'verified'}), (expected, expected))
            self.assertEqual(self.pipeline.process(directory)['status'], 'no_changes')
        self.assertEqual(len(keys), 1)
        self.assertEqual(len({e for e, attr in self.client.facts if attr == 'multistep/id'}), 2)

    def test_lost_reply_replays_exact_group_before_new_content(self):
        self.config.database_batch_questions = 2
        directories = [self.capture(20, ['q-11']), self.capture(21, ['q-12'])]
        self.client.timeout_once = True
        batch = self.root / 'batch'
        first = self.pipeline.process_batch(directories, batch)
        self.assertTrue(first['unknown_or_unverified_commit'], first)
        saved = read_json(batch / 'request.json')
        changed = read_json(directories[0] / 'content.json')
        changed['questions'][0]['problem'] = 'Revised source'
        atomic_json(directories[0] / 'content.json', changed)
        fresh = DatabasePipeline(self.config, self.stop, client=self.client)
        result = fresh.process_batch(directories[::-1], batch)
        self.assertEqual(result['status'], 'verified', result)
        calls = [opts for cmd, opts in self.client.calls if cmd == 'transact']
        self.assertEqual([opts['--request-key'] for opts in calls], [saved['request_key']] * 2)
        self.assertEqual(len(self.client.receipts), 1)
        self.assertNotEqual(result['activities'][str(directories[0])]['content_sha256'], digest(changed))
        archive = batch / 'requests' / saved['request_key'] / 'request.json'
        self.assertEqual(read_json(archive)['transaction'], saved['transaction'])

    def test_new_shared_question_revisions_stop_at_boundary_and_first_capture_is_retained(self):
        self.config.database_batch_questions = 200
        first, second = self.capture(20, ['q-11']), self.capture(21, ['q-11'])
        content = read_json(second / 'content.json')
        content['questions'][0]['problem'] = 'A later source revision'
        atomic_json(second / 'content.json', content)
        result = self.pipeline.process_batch([first, second], self.root / 'batch1', allow_underfilled=True)
        self.assertEqual(result['status'], 'verified', result)
        self.assertEqual(list(result['activities']), [str(first)])
        self.assertEqual(result['boundary'], 'shared_content_revision')
        retained = {key: deepcopy(values) for key, values in self.client.facts.items()
                    if key[1].startswith(('question/', 'answer-field/', 'answer/'))}
        self.assertEqual(self.pipeline.process_batch([second], self.root / 'batch2', allow_underfilled=True)['status'], 'verified')
        self.assertTrue(all(self.client.facts[key] == values for key, values in retained.items()))
        values = [v for (e, a), vals in self.client.facts.items() if a == 'question/problem' for v, _ in vals]
        self.assertIn(question()['problem'], values)
        self.assertNotIn('A later source revision', values)
        self.assertEqual(len({e for e, attr in self.client.facts if attr == 'multistep/id'}), 2)

    def test_complete_question_recaptures_share_a_batch_without_overwriting_stored_content(self):
        self.config.database_batch_questions = 200
        original = self.capture(19, ['q-11'])
        self.assertEqual(self.pipeline.process(original)['status'], 'verified')
        retained = {key: deepcopy(values) for key, values in self.client.facts.items()
                    if key[1].startswith(('question/', 'answer-field/', 'answer/'))}
        first, second = self.capture(20, ['q-11']), self.capture(21, ['q-11'])
        content = read_json(first / 'content.json')
        content['questions'][0]['problem'] = 'Earlier revision'
        atomic_json(first / 'content.json', content)
        result = self.pipeline.process_batch([first, second], self.root / 'batch1', allow_underfilled=True)
        self.assertEqual(result['status'], 'verified', result)
        self.assertEqual(result['boundary'], 'queue_end', result)
        self.assertEqual(set(result['activities']), {str(first), str(second)})
        self.assertTrue(all(self.client.facts[key] == values for key, values in retained.items()))
        self.assertEqual(len({e for e, attr in self.client.facts if attr == 'multistep/id'}), 3)
        self.assertEqual(self.pipeline.process_batch([second], self.root / 'batch2', allow_underfilled=True)['status'], 'no_changes')

    def test_size_target_never_splits_a_large_complete_activity(self):
        self.config.database_batch_questions = 2
        first = self.capture(20, ['q-11', 'q-12', 'q-13'])
        second = self.capture(21, ['q-14'])
        result = self.pipeline.process_batch([first, second], self.root / 'batch')
        self.assertEqual(result['status'], 'verified', result)
        self.assertEqual(result['questions'], 3)
        self.assertEqual(list(result['activities']), [str(first)])
        self.assertEqual(len(self.client.receipts), 1)

    def test_safety_limit_retains_oversized_activity_without_any_write(self):
        self.config.database_batch_max_bytes = 100
        first = self.capture(20, ['q-11'])
        result = self.pipeline.process_batch([first], self.root / 'batch')
        self.assertEqual(result['status'], 'pending')
        self.assertIn('without splitting', result['reason'])
        self.assertFalse(self.client.receipts)

    def test_byte_and_operation_counts_are_measured_on_complete_edn(self):
        capture = self.capture(20, ['q-11', 'q-12'])
        result = self.pipeline.process_batch([capture], self.root / 'batch')
        self.assertEqual(result['status'], 'verified', result)
        measured = read_json(self.root / 'batch/batch-size.json')
        self.assertGreater(measured['bytes'], 1)
        self.assertGreater(measured['ops'], 1)

    def test_crash_during_receipt_fanout_completes_without_another_commit(self):
        self.config.database_batch_questions = 2
        directories = [self.capture(20, ['q-11']), self.capture(21, ['q-12'])]
        batch = self.root / 'batch'
        real_atomic = atomic_json
        failed = []
        def write(path, value):
            if Path(path).name == 'result.json' and str(directories[1] / 'database/requests') in str(path) and not failed:
                failed.append(True)
                raise OSError('interrupted receipt copy')
            real_atomic(path, value)
        with patch('scripts.database.batch.atomic_json', side_effect=write):
            result = self.pipeline.process_batch(directories, batch)
        self.assertTrue(result['unknown_or_unverified_commit'], result)
        self.assertEqual(self.pipeline.process_batch(directories, batch)['status'], 'verified')
        self.assertEqual(len(self.client.receipts), 1)
        self.assertEqual(len([c for c in self.client.calls if c[0] == 'transact']), 1)
        for directory in directories:
            self.assertEqual(len(list((directory / 'database/requests').glob('*/receipt.edn'))), 1)

    def test_legacy_pending_request_recovers_before_new_batch(self):
        first, second = self.capture(20, ['q-11']), self.capture(21, ['q-12'])
        first_spool, second_spool = enqueue(self.config, first), enqueue(self.config, second)
        self.client.timeout_once = True
        self.assertEqual(self.pipeline.process(first)['status'], 'pending')
        self.assertEqual(self.worker.process_one(force=True)['status'], 'verified')
        self.assertEqual(read_json(first_spool)['status'], 'verified')
        self.assertEqual(read_json(second_spool)['attempts'], 0)
        self.assertEqual(self.worker.process_one(force=True)['status'], 'verified')
        self.assertEqual(len(self.client.receipts), 2)

    def test_old_small_queue_never_flushes_automatically_across_accounts(self):
        self.config.database_batch_questions = 200
        directories = [self.capture(20, ['q-11']), self.capture(21, ['q-12'])]
        first = enqueue(self.config, directories[0])
        self.config.account = 'linear'
        second = enqueue(self.config, directories[1])
        self.assertEqual(self.worker.process_one()['status'], 'accumulating')
        self.assertFalse(self.client.calls)
        self.assertEqual(read_json(first)['attempts'], 0)
        item = read_json(first)
        item['created_ns'] = int((time.time() - 7 * 86400) * 1e9)
        atomic_json(first, item)
        result = self.worker.process_one()
        self.assertEqual(result['status'], 'accumulating', result)
        self.assertFalse(self.client.calls)
        self.assertEqual(read_json(first)['attempts'], 0)
        result = self.worker.process_one(force=True)
        self.assertEqual(result['status'], 'verified', result)
        self.assertFalse(self.worker.pending())
        self.assertEqual(read_json(first)['status'], read_json(second)['status'])
        self.assertEqual(len(self.client.receipts), 1)

    def test_threshold_flush_and_forced_drain(self):
        self.config.database_batch_questions = 2
        for task, mid in ((20, 'q-11'), (21, 'q-12')):
            enqueue(self.config, self.capture(task, [mid]))
        self.assertEqual(self.worker.process_one()['status'], 'verified')
        enqueue(self.config, self.capture(22, ['q-13']))
        self.assertEqual(self.worker.process_one()['status'], 'accumulating')
        self.assertEqual(self.worker.process_one(force=True)['status'], 'verified')
        self.assertEqual(len(self.client.receipts), 2)

    def test_later_preparation_failure_is_visible_and_retried_with_backoff(self):
        self.config.database_batch_questions = 2
        first, second = self.capture(20, ['q-11']), self.capture(21, ['q-12'])
        first_spool, second_spool = enqueue(self.config, first), enqueue(self.config, second)
        content = read_json(second / 'content.json')
        content['questions'][0]['problem'] = r'$x+\(y\)$'
        atomic_json(second / 'content.json', content)
        result = self.worker.process_one()
        self.assertEqual(result['status'], 'pending', result)
        self.assertIn(str(second), result['reason'])
        self.assertIn('Nested math delimiter', result['reason'])
        self.assertEqual(set(result['activities']), {str(second)})
        self.assertEqual(read_json(first_spool)['attempts'], 0)
        self.assertEqual(read_json(second_spool)['attempts'], 1)
        active_path = self.worker.batch_root / 'active.json'
        active = read_json(active_path)
        self.assertGreater(active['next_attempt_at'], active['last_attempt_at'])
        self.assertFalse(self.client.receipts)
        self.assertTrue((Path(active['directory']) / 'pending.json').exists())
        # A fixed capture can enter a fresh plan without replacing saved intent.
        content['questions'][0]['problem'] = question('q-12')['problem']
        atomic_json(second / 'content.json', content)
        active['next_attempt_at'] = 0
        atomic_json(active_path, active)
        self.assertEqual(self.worker.process_one()['status'], 'verified')
        self.assertFalse(active_path.exists())
        self.assertEqual(read_json(first_spool)['status'], 'verified')
        self.assertEqual(read_json(second_spool)['status'], 'verified')

    def test_unresolved_batch_blocks_new_work_and_recovers_after_restart(self):
        self.config.database_batch_questions = 2
        directories = [self.capture(20, ['q-11']), self.capture(21, ['q-12'])]
        for directory in directories:
            enqueue(self.config, directory)
        self.client.timeout_once = True
        self.assertEqual(self.worker.process_one(force=True)['status'], 'pending')
        third = enqueue(self.config, self.capture(22, ['q-13']))
        active_path = self.worker.batch_root / 'active.json'
        active = read_json(active_path)
        active['next_attempt_at'] = time.time() + 100
        atomic_json(active_path, active)
        self.assertEqual(self.worker.process_one(force=True)['status'], 'waiting')
        self.assertEqual(read_json(third)['attempts'], 0)
        active['next_attempt_at'] = 0
        atomic_json(active_path, active)
        fresh = DatabaseWorker(self.config, self.stop, lambda: self.pipeline)
        result = fresh.process_one(force=True)
        self.assertEqual(result['status'], 'verified', result)
        self.assertEqual(len(fresh.pending()), 1)
        self.assertEqual(len(self.client.receipts), 1)

    def test_explicit_stale_basis_reprepares_without_replaying_rejected_intent(self):
        original = self.client.command
        rejected = []
        def command(cmd, *options):
            if cmd == 'transact' and not rejected:
                rejected.append(dict(zip(options[::2], options[1::2]))['--request-key'])
                self.client.t += 1
                raise StaleBasis('basis advanced')
            return original(cmd, *options)
        self.client.command = command
        result = self.pipeline.process_batch([self.capture(20, ['q-11'])], self.root / 'batch')
        self.assertEqual(result['status'], 'verified', result)
        self.assertEqual(len(self.client.receipts), 1)
        self.assertNotIn(rejected[0], self.client.receipts)

    def test_lineage_change_retains_exact_request_and_blocks_other_writes(self):
        self.client.timeout_once = True
        batch = self.root / 'batch'
        capture = self.capture(20, ['q-11'])
        self.pipeline.process_batch([capture], batch)
        saved = read_json(batch / 'request.json')
        self.client.lineage = 'another-lineage'
        result = self.pipeline.process_batch([capture], batch)
        self.assertEqual(result['status'], 'pending')
        self.assertEqual(read_json(batch / 'request.json'), saved)
        self.assertEqual(len(self.client.receipts), 1)

    def test_source_changed_during_unknown_outcome_is_rechecked_without_rewriting_completed_capture(self):
        capture = self.capture(20, ['q-11'])
        spool = enqueue(self.config, capture)
        self.client.timeout_once = True
        self.assertEqual(self.worker.process_one(force=True)['status'], 'pending')
        retained = deepcopy(self.client.facts)
        submitted = [opts for cmd, opts in self.client.calls if cmd == 'transact']
        self.assertEqual(len(submitted), 1)
        content = read_json(capture / 'content.json')
        content['questions'][0]['problem'] = 'Updated while outcome unknown'
        atomic_json(capture / 'content.json', content)
        active_path = self.worker.batch_root / 'active.json'
        active = read_json(active_path)
        active['next_attempt_at'] = 0
        atomic_json(active_path, active)
        self.assertEqual(self.worker.process_one(force=True)['status'], 'verified')
        self.assertEqual(read_json(spool)['status'], 'pending')
        submitted = [opts for cmd, opts in self.client.calls if cmd == 'transact']
        self.assertEqual(len(submitted), 2)
        self.assertEqual(submitted[0]['--request-key'], submitted[1]['--request-key'])
        item = read_json(spool)
        item['next_attempt_at'] = 0
        atomic_json(spool, item)
        self.assertEqual(self.worker.process_one(force=True)['status'], 'no_changes')
        self.assertEqual(read_json(spool)['status'], 'no_changes')
        self.assertEqual(len(self.client.receipts), 1)
        self.assertEqual(self.client.facts, retained)
        self.assertFalse(self.worker.pending())

    def test_default_200_floor_waits_then_commits_whole_activities_above_floor(self):
        self.config.database_batch_questions = 200
        first = self.capture(20, ['q-' + str(i) for i in range(11, 210)])
        enqueue(self.config, first)
        result = self.worker.process_one()
        self.assertEqual(result['status'], 'accumulating')
        self.assertEqual(result['questions'], 199)
        self.assertFalse(self.client.calls)
        second = self.capture(21, ['q-210', 'q-211'])
        enqueue(self.config, second)
        result = self.worker.process_one()
        self.assertEqual(result['status'], 'verified', result)
        self.assertEqual(result['questions'], 201)
        self.assertEqual(set(result['activities']), {str(first), str(second)})
        self.assertEqual(len(self.client.receipts), 1)
        self.assertFalse(self.worker.pending())

    def test_related_revisions_wait_while_independent_activities_fill_floor(self):
        self.config.database_batch_questions = 2
        first = self.capture(20, ['q-11'])
        revised = self.capture(21, ['q-11'])
        related = self.capture(22, ['q-11', 'q-12'])
        for target, label in ((revised, 'revision'), (related, 'dependent revision')):
            content = read_json(target / 'content.json')
            content['questions'][0]['problem'] = label
            content['questions'][0]['local_problem'] = label
            atomic_json(target / 'content.json', content)
        independent = self.capture(23, ['q-13'])
        result = self.pipeline.process_batch([first, revised, related], self.root / 'waiting')
        self.assertEqual(result['status'], 'accumulating', result)
        self.assertEqual(result['questions'], 1)
        self.assertFalse(self.client.receipts)
        result = self.pipeline.process_batch([first, revised, related, independent], self.root / 'waiting')
        self.assertEqual(result['status'], 'verified', result)
        self.assertEqual(set(result['activities']), {str(first), str(independent)})
        self.assertEqual(result['questions'], 2)
        self.assertEqual(len(self.client.receipts), 1)

    def test_duplicate_observations_do_not_inflate_question_floor(self):
        self.config.database_batch_questions = 2
        for task in range(20, 80):
            enqueue(self.config, self.capture(task, ['q-11']))
        result = self.worker.process_one()
        self.assertEqual(result['status'], 'accumulating', result)
        self.assertEqual(result['questions'], 1)
        self.assertEqual(result['activities'], 60)
        self.assertFalse(self.client.calls)

    def test_raw_admission_estimate_cannot_commit_an_underfilled_prepared_group(self):
        self.config.database_batch_questions = 2
        first, second = self.capture(20, ['q-11']), self.capture(21, ['q-11', 'q-12'])
        for directory in (first, second):
            enqueue(self.config, directory)
        result = self.worker.process_one()
        self.assertEqual(result['status'], 'accumulating', result)
        self.assertEqual(result['questions'], 1)
        self.assertFalse(self.client.receipts)
        self.assertFalse(read_json(self.worker.batch_root / 'active.json'))
        self.assertTrue(all(item['attempts'] == 0 for _, item in self.worker.pending()))

    def test_submitted_small_batch_recovers_even_after_minimum_is_raised(self):
        capture = self.capture(20, ['q-11'])
        enqueue(self.config, capture)
        self.client.timeout_once = True
        self.assertEqual(self.worker.process_one()['status'], 'pending')
        active_path = self.worker.batch_root / 'active.json'
        active = read_json(active_path)
        active['next_attempt_at'] = 0
        atomic_json(active_path, active)
        request = read_json(Path(active['directory']) / 'request.json')
        self.config.database_batch_questions = 200
        result = self.worker.process_one()
        self.assertEqual(result['status'], 'verified', result)
        keys = [opts['--request-key'] for cmd, opts in self.client.calls if cmd == 'transact']
        self.assertEqual(keys, [request['request_key']] * 2)
        self.assertFalse(self.worker.pending())

    def test_retired_configuration_settings_cannot_restore_automatic_small_flushes(self):
        path = self.root / 'config.json'
        atomic_json(path, {'database_batch_max_age': 1, 'database_batch_max_activities': 1,
                           'database_batch_target_bytes': 1, 'database_batch_target_ops': 1})
        config = Config.from_file(path, repo_root=self.root, math_root=self.root / 'math')
        self.assertEqual(config.database_batch_questions, 200)
        enqueue(config, self.capture(20, ['q-11']))
        worker = DatabaseWorker(config, self.stop, lambda: self.pipeline)
        self.assertEqual(worker.process_one()['status'], 'accumulating')
        self.assertFalse(self.client.calls)

    def test_safety_limits_never_force_a_commit_below_minimum(self):
        self.config.database_batch_questions = 2
        directories = [self.capture(20, ['q-11']), self.capture(21, ['q-12']), self.capture(22, ['q-13'])]
        prepared, _ = self.pipeline._prepare(read_json(directories[0] / 'content.json'),
                                             directories[0] / 'database', self.client.basis())
        measured = size(prepared['batches'][0])
        for unit in ('bytes', 'ops'):
            with self.subTest(unit=unit):
                field = 'database_batch_max_' + unit
                previous = getattr(self.config, field)
                setattr(self.config, field, measured[unit])
                result = self.pipeline.process_batch(directories, self.root / unit)
                self.assertEqual(result['status'], 'accumulating', result)
                self.assertEqual(result['questions'], 1)
                self.assertEqual(result['boundary'], 'safety_limit')
                self.assertFalse(self.client.receipts)
                setattr(self.config, field, previous)

    def test_cli_drain_only_overrides_floor_with_explicit_flush(self):
        from scripts.cli import main
        for extra, expected in (([], False), (['--flush'], True)):
            with self.subTest(extra=extra), patch('scripts.cli.DatabaseWorker') as factory, redirect_stdout(io.StringIO()):
                factory.return_value.process_one.return_value = {'status': 'accumulating'}
                main(['drain', '--once', '--repo-root', str(self.root), *extra])
                factory.return_value.process_one.assert_called_once_with(force=expected)

    def test_questions_omitted_after_catalog_checks_do_not_count_toward_floor(self):
        self.config.database_batch_questions = 2
        first, second = self.capture(20, ['q-11']), self.capture(21, ['q-12'])
        content = read_json(second / 'content.json')
        content['questions'][0]['topic_id'] = 999
        atomic_json(second / 'content.json', content)
        self.pipeline.resolver = lambda task, payload: {'status': 'unavailable', 'answers': [],
                                                       'reasoning': 'Source topic is absent from the catalog'}
        result = self.pipeline.process_batch([first, second], self.root / 'waiting')
        self.assertEqual(result['status'], 'accumulating', result)
        self.assertEqual(result['questions'], 1)
        self.assertFalse(self.client.receipts)
        prepared = read_json(second / 'database/preparation.json')
        self.assertEqual(prepared['content']['questions'], [])
        self.assertTrue(any(o.get('id') == 'q-12' for o in prepared['omissions']))
        third = self.capture(22, ['q-13'])
        result = self.pipeline.process_batch([first, second, third], self.root / 'waiting')
        self.assertEqual(result['status'], 'verified', result)
        self.assertEqual(result['questions'], 2)
        self.assertEqual(len(self.client.receipts), 1)


if __name__ == '__main__':
    unittest.main()
