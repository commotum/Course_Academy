"""Historical recovery credits only proven quota turns and retains real budgets."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import generator_quota_recovery as R
from inventory_jobs import save


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.inventory = self.root / 'inventory'
        self.pipeline = self.inventory / 'abc.pipeline/1'
        self.session = self.pipeline / 'investigation'
        self.session.mkdir(parents=True)
        self.output = self.root / 'recovery'
        self.manifest = self.root / 'manifest.json'
        self.item = {'key': 'abc', 'kp': 12, 'role': 'investigate', 'rejected_turns': 2}
        save(self.manifest, [self.item])
        events = [{'type': 'turn.started'}, {'type': 'turn.failed', 'error': {'message': 'real failure'}},
                  {'type': 'turn.started'}, {'type': 'error', 'message': "You've hit your usage limit."},
                  {'type': 'turn.failed', 'error': {'message': "You've hit your usage limit."}},
                  {'type': 'turn.started'}, {'type': 'error', 'message': "You've hit your usage limit."},
                  {'type': 'turn.failed', 'error': {'message': "You've hit your usage limit."}}]
        (self.session / 'events.jsonl').write_text(''.join(json.dumps(row) + '\n' for row in events))
        self.execution = {'launches': 3, 'status': 'failed', 'result_directory': str(self.session),
                          'error': 'quota returncode', 'launch_id': 'original-id'}
        save(self.session / 'execution.json', self.execution)
        cause = {'code': 'agent_session_retry_exhausted', 'role': 'investigate', 'launches': 3,
                 'session_directory': str(self.session), 'execution_path': str(self.session / 'execution.json')}
        error = {'code': 'agent_session_retry_exhausted', 'cause': cause, 'resume_stage': 'investigate'}
        self.state = {'request': {'kp': 12}, 'stage': 'blocked', 'error': error, 'attempt': 1,
                      'author_attempt_limit': 3, 'review_sessions': ['old'], 'review_session_limit': 9,
                      'source_account_rounds': {'investigate': 1}, 'progress_failures': {'real-failure': 1}}
        save(self.pipeline / 'job.json', self.state)
        self.job = {'key': 'abc', 'cycle': 1, 'request': {'knowledgePoint': 12}, 'state': 'blocked',
                    'outcome': {'outcome': 'blocked', 'reason': error}, 'attempts': 3, 'processFailures': 0}
        save(self.inventory / 'abc.json', self.job)

    def tearDown(self):
        self.temp.cleanup()

    def prepare(self):
        return R.prepare(self.inventory, self.manifest, self.output)

    def test_quota_events_count_once_and_ignore_tool_text(self):
        events = (self.session / 'events.jsonl').read_bytes()
        self.assertEqual(R.quota_turns(events), 2)
        with self.assertRaises(ValueError):
            R.quota_turns(b'{"type":"item.completed","message":"You\'ve hit your usage limit."}\n')

    def test_apply_preserves_real_budgets_and_can_resume_after_partial_writes(self):
        result = self.prepare()
        self.assertEqual((result['eligible_jobs'], result['quota_launch_credits']), (1, 2))
        plan, originals = R.load_plan(self.output)
        first = plan['jobs'][0]['files'][0]
        save(Path(first['path']), {**json.loads(originals[first['backup']]), **first['updates']})
        applied = R.apply(self.output, self.root / 'daemon.lock')
        self.assertEqual(applied['written_files'], 2)
        new_execution = json.loads((self.session / 'execution.json').read_text())
        self.assertEqual((new_execution['launches'], new_execution['launch_limit']), (3, 5))
        pipeline = json.loads((self.pipeline / 'job.json').read_text())
        for field in ('attempt', 'author_attempt_limit', 'review_sessions', 'review_session_limit',
                      'source_account_rounds', 'progress_failures'):
            self.assertEqual(pipeline[field], self.state[field])
        root = json.loads((self.inventory / 'abc.json').read_text())
        self.assertEqual((root['state'], root['attempts'], root['processFailures']), ('pending', 3, 0))
        self.assertEqual(root['outcome']['outcome'], 'paused')
        self.assertTrue(R.verify(self.output)['verified'])
        self.assertEqual(R.apply(self.output, self.root / 'daemon.lock')['written_files'], 0)

    def test_changed_member_prevents_all_changes_to_that_job(self):
        self.prepare()
        path = self.pipeline / 'job.json'
        save(path, {**self.state, 'attempt': 2})
        with self.assertRaisesRegex(ValueError, 'Concurrent change'):
            R.apply(self.output, self.root / 'daemon.lock')
        self.assertEqual(json.loads((self.session / 'execution.json').read_text()), self.execution)
        self.assertEqual(json.loads((self.inventory / 'abc.json').read_text()), self.job)

    def test_inventory_ranking_refresh_after_recovery_is_preserved(self):
        self.prepare()
        R.apply(self.output, self.root / 'daemon.lock')
        path = self.inventory / 'abc.json'
        root = json.loads(path.read_text())
        root.update(state='running', request={**root['request'], 'basis': 999, 'score': 45})
        save(path, root)
        self.assertEqual(R.apply(self.output, self.root / 'daemon.lock')['written_files'], 0)
        self.assertEqual(json.loads(path.read_text()), root)
        self.assertTrue(R.verify(self.output)['verified'])
        root['attempts'] += 1
        save(path, root)
        with self.assertRaisesRegex(ValueError, 'Concurrent change'):
            R.apply(self.output, self.root / 'daemon.lock')

    def test_publication_intent_and_other_blockers_are_not_recovered(self):
        save(self.pipeline / 'publication/request.json', {'request_id': 'pending'})
        result = self.prepare()
        self.assertEqual(result['eligible_jobs'], 0)
        self.assertEqual(result['skipped_jobs'], 1)

    def test_real_final_error_or_changed_evidence_does_not_receive_quota_credits(self):
        path = self.session / 'events.jsonl'
        with path.open('a') as stream:
            stream.write('{"type":"turn.started"}\n{"type":"turn.failed","error":{"message":"real failure"}}\n')
        self.assertEqual(self.prepare()['eligible_jobs'], 0)

    def test_changed_log_or_live_daemon_is_not_mutated(self):
        self.prepare()
        with R.lock_file(self.root / 'daemon.lock'):
            with self.assertRaises(BlockingIOError):
                R.apply(self.output, self.root / 'daemon.lock')
        with (self.session / 'events.jsonl').open('a') as stream:
            stream.write('\n')
        with self.assertRaisesRegex(ValueError, 'Agent evidence changed'):
            R.apply(self.output, self.root / 'daemon.lock')


if __name__ == '__main__':
    unittest.main()
