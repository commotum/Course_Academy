"""Separate-process finalizer state must survive a waiting reviewer parent."""
import copy
import json
from pathlib import Path
import unittest

import test_generator_pipeline as fixtures
from generator_pipeline import read, save


class ExternalFinalizationTests(unittest.TestCase):
    setUp = fixtures.GeneratorPipelineTests.setUp
    tearDown = fixtures.GeneratorPipelineTests.tearDown
    pipeline = fixtures.GeneratorPipelineTests.pipeline

    def test_external_finalizer_is_reloaded_before_parent_persist(self):
        test = self
        parent = None
        final = {}

        class ExternalVerifier(fixtures.FakeSession):
            def __call__(self, role, context, directory):
                if role == 'review':
                    test.assertFalse(final, 'A correct external finalization must not need another review round')
                    script = Path(context['workspace']) / 'generator.py'
                    script.write_text(script.read_text().replace('random.Random(args.seed).sample',
                                                                'random.Random(args.seed + 1).sample'))
                    external = test.pipeline(fixtures.FakeSession())
                    final.update(external.finalize_review(Path(context['evidence_root']))['binding'])
                    test.assertNotEqual(parent.state['package_hash'], final['package_hash'])
                    context = external.context(Path(context['evidence_root']))
                return super().__call__(role, context, directory)

        session = ExternalVerifier()
        parent = self.pipeline(session)
        result = parent.run()
        self.assertEqual(result['stage'], 'verified')
        self.assertEqual([role for role, _ in session.calls], ['author', 'review'])
        self.assertEqual(result['package_hash'], final['package_hash'])
        self.assertEqual(result['batch_hash'], final['batch_hash'])

    def prepared_external_finalization(self):
        parent = self.pipeline(fixtures.FakeSession())
        parent.run(stop_after='generate')
        evidence = parent.review_directory()
        evidence.mkdir(exist_ok=True)
        parent.persist(active_review_directory=str(evidence))
        stale = copy.deepcopy(parent.state)
        script = self.job / 'workspace/generator.py'
        script.write_text(script.read_text().replace('random.Random(args.seed).sample',
                                                    'random.Random(args.seed + 1).sample'))
        external = self.pipeline(fixtures.FakeSession())
        receipt = external.finalize_review(evidence)['binding']
        save(parent.path, stale)  # Reproduce the old parent's destructive save.
        return self.pipeline(fixtures.FakeSession()), evidence, receipt

    def test_receipt_recovery_restores_only_exact_candidate_and_preserves_budget(self):
        pipeline, evidence, receipt = self.prepared_external_finalization()
        budget = {key: copy.deepcopy(pipeline.state.get(key)) for key in
                  ('attempt', 'review_sessions', 'review_session_limit', 'review_report_rounds')}
        self.assertTrue(pipeline.recover_finalized_review_state())
        self.assertEqual(pipeline.review_binding(), receipt)
        pipeline.verify_approval_inputs()
        self.assertFalse(pipeline.recover_finalized_review_state())
        self.assertEqual(budget, {key: pipeline.state.get(key) for key in budget})
        self.assertEqual(pipeline.state['stage'], 'validate')
        self.assertFalse(pipeline.state['approval_recorded'])
        self.assertEqual(self.publisher.prepares, 0)
        self.assertEqual(self.publisher.publishes, 0)
        self.assertEqual(len(list(evidence.glob('state-before-finalizer-recovery-*'))), 1)

    def test_recovery_does_not_accept_changed_package_or_other_band(self):
        pipeline, evidence, receipt = self.prepared_external_finalization()
        script = self.job / 'workspace/generator.py'
        original = script.read_bytes()
        script.write_bytes(original + b'\n# unfinalized later edit\n')
        self.assertFalse(pipeline.recover_finalized_review_state())
        script.write_bytes(original)
        other = Path(pipeline.state['verification_batches']['hard']['batch_file'])
        records = read(other)
        records[0]['question'][':question/problem'] = 'Changed after finalization'
        save(other, records)
        self.assertFalse(pipeline.recover_finalized_review_state())
        self.assertNotEqual(pipeline.review_binding(), receipt)
        self.assertEqual(self.publisher.prepares, 0)
        self.assertEqual(self.publisher.publishes, 0)

    def test_recovery_does_not_accept_changed_source_or_pending_publication(self):
        pipeline, evidence, receipt = self.prepared_external_finalization()
        source = self.job / 'source/source.json'
        original = source.read_bytes()
        value = read(source); value['basis'] += 1; save(source, value)
        self.assertFalse(pipeline.recover_finalized_review_state())
        source.write_bytes(original)
        publication = self.job / 'publication'; publication.mkdir(exist_ok=True)
        save(publication / 'request.json', {'pending': True})
        self.assertFalse(pipeline.recover_finalized_review_state())
        self.assertNotEqual(pipeline.review_binding(), receipt)
        self.assertEqual(self.publisher.publishes, 0)


if __name__ == '__main__':
    unittest.main()
