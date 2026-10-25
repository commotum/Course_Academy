"""Interrupted verifier edits remain repairable without weakening admission."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from generator_review import REVIEW_POLICY_VERSION
from test_generator_pipeline import FakeSession, GeneratorPipelineTests, finalize_fixture_review


class GeneratorUnfinishedReviewTests(unittest.TestCase):
    setUp = GeneratorPipelineTests.setUp
    tearDown = GeneratorPipelineTests.tearDown
    pipeline = GeneratorPipelineTests.pipeline

    def checkpoint(self, *, image=False):
        pipeline = self.pipeline(FakeSession(image=image))
        pipeline.run('generate')
        pipeline.ensure_inventory()
        evidence = pipeline.review_directory()
        evidence.mkdir()
        (evidence / 'review-binding.json').write_text(json.dumps(pipeline.review_binding()))
        (evidence / 'final-binding.json').write_text(json.dumps(pipeline.review_binding()))
        (evidence / 'events.jsonl').write_text(json.dumps({'type': 'thread.started', 'thread_id': 'unfinished-verifier'}) + '\n')
        (evidence / 'execution.json').write_text(json.dumps({'status': 'running', 'persistent_session': True, 'launches': 1}))
        pipeline.persist(active_review_directory=str(evidence), verification_policy_version=REVIEW_POLICY_VERSION,
                         review_sessions=[str(evidence)], review_session_limit=6)
        config = self.job / 'workspace/config.json'
        value = json.loads(config.read_text())
        value['interrupted_repair'] = True
        config.write_text(json.dumps(value))
        return pipeline, evidence

    def test_current_policy_interrupted_edit_resumes_same_verifier_and_requires_finalization(self):
        old, evidence = self.checkpoint()
        previous_hash = old.state['package_hash']
        pipeline = None
        test = self

        class Resumed(FakeSession):
            def __call__(self, role, context, directory):
                test.assertEqual(role, 'review')
                test.assertEqual(context['resume_session_id'], 'unfinished-verifier')
                test.assertEqual(Path(directory), evidence)
                test.assertIn('unfinalized generator repair', context['review_contract_feedback']['error']['error'])
                test.assertFalse((evidence / 'final-binding.json').exists())
                test.assertNotEqual(context['review_binding']['package_hash'], previous_hash)
                test.assertEqual(set(context['verification_batches']), {'easy', 'moderate', 'hard'})
                context = finalize_fixture_review(pipeline, context)
                return super().__call__(role, context, directory)

        session = Resumed()
        pipeline = self.pipeline(session)
        result = pipeline.run()
        self.assertEqual(result['stage'], 'verified')
        self.assertEqual([role for role, _ in session.calls], ['review'])
        self.assertEqual(result['attempt'], old.state['attempt'])
        self.assertEqual(result['review_sessions'], old.state['review_sessions'])
        self.assertEqual(result['review_session_limit'], 6)
        self.assertEqual(len(list(evidence.glob('draft-recovery-before-*'))), 1)
        self.assertEqual(json.loads((evidence / 'final-binding.json').read_text()), pipeline.review_binding())

    def test_missing_finalization_still_blocks_acceptance(self):
        _, evidence = self.checkpoint()

        class Unfinalized(FakeSession):
            def __call__(self, role, context, directory):
                report = super().__call__(role, context, directory)
                (evidence / 'final-binding.json').unlink(missing_ok=True)
                return report

        result = self.pipeline(Unfinalized()).run()
        self.assertEqual(result['stage'], 'blocked')
        self.assertEqual(result['error']['code'], 'verification_unfinished')
        self.assertFalse((self.job / 'publication/request.json').exists())
        self.assertEqual(self.publisher.publishes, 0)

    def test_changed_immutable_evidence_is_not_resampled_away(self):
        for kind in ('source', 'inventory', 'publication_batch', 'other_band', 'asset'):
            with self.subTest(kind=kind):
                self.job = self.root / ('job-' + kind)
                old, _ = self.checkpoint(image=True)
                if kind == 'source':
                    path = self.job / 'source/source.json'
                    value = json.loads(path.read_text()); value['basis'] += 1
                    path.write_text(json.dumps(value))
                elif kind == 'inventory':
                    path = self.job / 'source/inventory.json'
                    value = json.loads(path.read_text()); value['basis'] += 1
                    path.write_text(json.dumps(value))
                elif kind in ('publication_batch', 'other_band'):
                    path = self.job / 'samples.json' if kind == 'publication_batch' else Path(old.state['verification_batches']['hard']['batch_file'])
                    value = json.loads(path.read_text()); value[0]['question'][':question/problem'] = 'changed evidence'
                    path.write_text(json.dumps(value))
                else:
                    path = Path(next(iter(old.state['verification_batches']['hard']['assets'])))
                    path.write_text('changed image')
                session = FakeSession()
                pipeline = self.pipeline(session)
                with patch.object(pipeline, 'sample', wraps=pipeline.sample) as sample:
                    with self.assertRaises(ValueError):
                        pipeline.run()
                sample.assert_not_called()
                self.assertEqual(session.calls, [])
                self.assertFalse((self.job / 'publication/request.json').exists())

    def test_completed_or_unowned_draft_cannot_use_interruption_recovery(self):
        for kind in ('accepted_report', 'missing_execution', 'finished_execution', 'no_active_verifier'):
            with self.subTest(kind=kind):
                self.job = self.root / ('job-' + kind)
                old, evidence = self.checkpoint()
                if kind == 'accepted_report':
                    (evidence / 'result.json').write_text(json.dumps({'verdict': 'accepted'}))
                elif kind == 'missing_execution':
                    (evidence / 'execution.json').unlink()
                elif kind == 'finished_execution':
                    (evidence / 'execution.json').write_text(json.dumps({'status': 'completed', 'persistent_session': True}))
                else:
                    old.persist(active_review_directory=None)
                pipeline = self.pipeline(FakeSession())
                with patch.object(pipeline, 'sample', wraps=pipeline.sample) as sample:
                    with self.assertRaisesRegex(ValueError, 'Reviewed package'):
                        pipeline.run()
                sample.assert_not_called()

    def test_pending_publication_recovers_exact_intent_before_any_draft_repair(self):
        pipeline = self.pipeline(FakeSession())
        pipeline.run('prepare')
        request = self.job / 'publication/request.json'
        original = request.read_bytes()
        pipeline.persist(stage='validate')
        with (self.job / 'workspace/generator.py').open('a') as out:
            out.write('\n# later unreviewed edit\n')
        resumed = self.pipeline(FakeSession())
        with patch.object(resumed, 'resume_unfinished_review_draft', side_effect=AssertionError('Exact recovery comes first')) as recover:
            with self.assertRaisesRegex(ValueError, 'Reviewed package'):
                resumed.run()
        recover.assert_not_called()
        self.assertEqual(self.publisher.publishes, 1)
        self.assertEqual(request.read_bytes(), original)
        self.assertTrue((self.root / 'committed.json').exists())


del GeneratorPipelineTests

if __name__ == '__main__':
    unittest.main()
