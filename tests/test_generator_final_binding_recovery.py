"""Finalizer paths and interrupted review evidence retain the same verifier."""
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

from generator_pipeline import read, save
from generator_review import REVIEW_POLICY_VERSION
from test_generator_pipeline import FakeSession, GeneratorPipelineTests


class GeneratorFinalBindingRecoveryTests(unittest.TestCase):
    setUp = GeneratorPipelineTests.setUp
    tearDown = GeneratorPipelineTests.tearDown
    pipeline = GeneratorPipelineTests.pipeline

    def checkpoint(self, *, image=False, changed=True):
        pipeline = self.pipeline(FakeSession(image=image))
        pipeline.run('generate')
        pipeline.ensure_inventory()
        evidence = pipeline.review_directory()
        evidence.mkdir()
        save(evidence / 'review-binding.json', pipeline.review_binding())
        save(evidence / 'execution.json', {'status': 'failed', 'persistent_session': True, 'launches': 1})
        (evidence / 'events.jsonl').write_text(json.dumps({'type': 'thread.started', 'thread_id': 'original-verifier'}) + '\n')
        pipeline.persist(active_review_directory=str(evidence), verification_policy_version=REVIEW_POLICY_VERSION,
                         review_sessions=[str(evidence)], review_session_limit=6)
        if changed:
            config = self.job / 'workspace/config.json'
            save(config, {**read(config), 'verifier_repair': True})
        pipeline.finalize_review(evidence)
        misplaced = self.job / evidence.relative_to(self.root) / 'final-binding.json'
        misplaced.parent.mkdir(parents=True)
        (evidence / 'final-binding.json').rename(misplaced)
        return pipeline, evidence, misplaced

    def test_finalizer_accepts_absolute_repo_relative_and_job_relative_paths(self):
        pipeline = self.pipeline(FakeSession())
        pipeline.run('generate')
        evidence = pipeline.review_directory()
        original_cwd = Path.cwd()
        try:
            os.chdir(self.root)
            for path in (evidence, evidence.relative_to(self.root), evidence.relative_to(self.job)):
                with self.subTest(path=path):
                    (evidence / 'final-binding.json').unlink(missing_ok=True)
                    result = pipeline.finalize_review(path)
                    self.assertEqual(read(evidence / 'final-binding.json'), result['binding'])
                    self.assertEqual(set(result['verification_batches']), {'easy', 'moderate', 'hard'})
            with self.assertRaisesRegex(ValueError, 'escapes'):
                pipeline.finalize_review(self.root / 'outside-review')
        finally:
            os.chdir(original_cwd)
        self.assertFalse((self.job / 'job').exists())

    def test_exact_misplaced_finalization_resumes_original_session_without_resampling(self):
        for changed in (False, True):
            with self.subTest(changed=changed):
                self.job = self.root / ('job-' + str(changed))
                old, evidence, misplaced = self.checkpoint(changed=changed)
                binding = old.review_binding()
                original = misplaced.read_bytes()
                test = self

                class Resumed(FakeSession):
                    def __call__(self, role, context, directory):
                        test.assertEqual(role, 'review')
                        test.assertEqual(context['resume_session_id'], 'original-verifier')
                        test.assertEqual(Path(directory), evidence)
                        test.assertEqual(read(evidence / 'final-binding.json'), binding)
                        test.assertEqual(context['review_binding'], binding)
                        return super().__call__(role, context, directory)

                session = Resumed()
                pipeline = self.pipeline(session)
                with patch.object(pipeline, 'sample', side_effect=AssertionError('Final batches already exist')):
                    result = pipeline.run()
                self.assertEqual(result['stage'], 'verified')
                self.assertEqual([role for role, _ in session.calls], ['review'])
                self.assertEqual(result['review_sessions'], old.state['review_sessions'])
                self.assertEqual(result['attempt'], old.state['attempt'])
                self.assertEqual(misplaced.read_bytes(), original)

    def test_mismatched_misplaced_binding_cannot_be_recovered(self):
        for key in ('package_hash', 'batch_hash', 'source_hash', 'inventory_hash', 'verification_batches'):
            with self.subTest(key=key):
                self.job = self.root / ('job-' + key)
                _, evidence, misplaced = self.checkpoint()
                binding = read(misplaced)
                binding[key] = {} if key == 'verification_batches' else 'stale'
                save(misplaced, binding)
                session = FakeSession()
                result = self.pipeline(session).run()
                self.assertEqual(result['error']['code'], 'review_binding_changed')
                self.assertEqual(session.calls, [])
                self.assertFalse((evidence / 'final-binding.json').exists())

    def test_changed_immutable_inputs_are_not_hidden_by_path_recovery(self):
        for kind in ('source', 'inventory', 'publication_batch', 'other_band', 'asset'):
            with self.subTest(kind=kind):
                self.job = self.root / ('job-' + kind)
                old, evidence, _ = self.checkpoint(image=True)
                if kind in ('source', 'inventory'):
                    path = self.job / ('source/' + kind + '.json')
                    save(path, {**read(path), 'basis': 999})
                elif kind in ('publication_batch', 'other_band'):
                    path = self.job / 'samples.json' if kind == 'publication_batch' else Path(old.state['verification_batches']['hard']['batch_file'])
                    records = read(path)
                    records[0]['question'][':question/problem'] = 'altered'
                    save(path, records)
                else:
                    Path(next(iter(old.state['verification_batches']['hard']['assets']))).write_text('altered')
                session = FakeSession()
                pipeline = self.pipeline(session)
                with patch.object(pipeline, 'sample', side_effect=AssertionError('Do not overwrite changed evidence')):
                    with self.assertRaises(ValueError):
                        pipeline.run()
                self.assertEqual(session.calls, [])
                self.assertFalse((evidence / 'final-binding.json').exists())

    def test_restored_finalization_does_not_replace_required_three_band_review(self):
        _, evidence, _ = self.checkpoint()

        class MissingBand(FakeSession):
            def __call__(self, role, context, directory):
                report = super().__call__(role, context, directory)
                report['band_verification'].pop('hard')
                return report

        result = self.pipeline(MissingBand()).run()
        self.assertEqual(result['stage'], 'blocked')
        self.assertEqual(result['error']['code'], 'verification_unfinished')
        self.assertTrue((evidence / 'final-binding.json').exists())
        self.assertEqual(self.publisher.publishes, 0)


del GeneratorPipelineTests

if __name__ == '__main__':
    unittest.main()
