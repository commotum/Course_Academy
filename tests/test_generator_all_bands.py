"""End-to-end all-band boundaries with real generators and fake agent/EDB I/O."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from generator_packages import publish_package
from generator_pipeline import Pipeline, digest
from generator_review import REVIEW_POLICY_VERSION
from test_generator_pipeline import FakePublisher, FakeSession, finalize_fixture_review, fixture_investigation


BANDS = ('easy', 'moderate', 'hard')


class RecordingSession(FakeSession):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.roles = []
        self.contexts = []

    def __call__(self, role, context, directory):
        self.roles.append(role)
        self.contexts.append((role, context))
        return super().__call__(role, context, directory)


class GeneratorAllBandsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.math = self.root / 'math'
        self.job = self.root / 'job'
        self.publisher = FakePublisher(self.root / 'publisher')
        self.request = {'kp': 123, 'difficulty': 'easy', 'count': 3, 'existing_entrypoint': None}
        self.environment = {**os.environ, 'EDB_MATH_ROOT': str(self.math),
                            'COURSE_ACADEMY_GENERATOR_PYTHON': sys.executable}

    def tearDown(self):
        for path in self.root.rglob('*'):
            if path.is_dir() and not path.is_symlink():
                path.chmod(0o755)
        self.temp.cleanup()

    def pipeline(self, session, *, job=None, publisher=None, request=None):
        return Pipeline(job or self.job, request or self.request, publisher or self.publisher,
                        root=self.root, environment=self.environment, session=session,
                        investigation_preparer=fixture_investigation)

    def approval(self, state):
        return json.loads((self.math / 'generators/approvals' / state['package_hash'] / '123.json').read_text())

    def test_one_review_verifies_three_deterministic_batches_and_publishes_only_requested_inventory(self):
        session = RecordingSession(image=True)
        state = self.pipeline(session).run()
        self.assertEqual(state['stage'], 'verified')
        self.assertEqual(session.roles, ['investigate', 'author', 'review'])
        self.assertEqual(set(state['verification_batches']), set(BANDS))
        self.assertEqual(set(state['verified_bands']), set(BANDS))
        self.assertEqual(len({batch['batch_hash'] for batch in state['verification_batches'].values()}), 3)
        review = json.loads(Path(state['review']).read_text())
        for band, batch in state['verification_batches'].items():
            records = json.loads(Path(batch['batch_file']).read_text())
            self.assertEqual(len(records), 3 if band == 'easy' else 5)
            self.assertEqual({record['question'][':question/difficulty'] for record in records},
                             {':question.difficulty/' + band})
            self.assertEqual(digest(records), batch['batch_hash'])
            self.assertEqual(review['band_verification'][band]['batch_sha256'], batch['batch_hash'])
            runtime = Path(batch['runtime'])
            self.assertEqual((runtime / 'run-0.stdout').read_bytes(), (runtime / 'run-1.stdout').read_bytes())
            self.assertTrue(batch['assets'])
        publication = json.loads((self.job / 'publication/request.json').read_text())
        self.assertEqual(len(publication['records']), 3)
        self.assertEqual({record['question'][':question/difficulty'] for record in publication['records']},
                         {':question.difficulty/easy'})
        approval = self.approval(state)
        self.assertEqual(approval['publication']['difficulty'], 'easy')
        for band in BANDS:
            self.assertNotIn('publication', approval['bands'][band])
            publisher = FakePublisher(self.root / ('refill-publisher-' + band))
            publisher.registered_generator = {':question-generator/script': state['registration']}
            refill_session = RecordingSession()
            refill = self.pipeline(refill_session, job=self.root / ('refill-' + band), publisher=publisher,
                                   request={**self.request, 'job_kind': 'refill', 'difficulty': band,
                                            'registered_package': state['registration']}).run()
            self.assertEqual(refill['stage'], 'verified')
            self.assertEqual(refill_session.roles, [])
            self.assertEqual(publisher.publishes, 1)

    def test_nonrequested_band_batch_or_asset_tampering_cannot_reach_publication(self):
        for target in ('batch', 'image'):
            with self.subTest(target=target):
                job = self.root / ('tampered-' + target)
                publisher = FakePublisher(self.root / ('publisher-' + target))
                session = RecordingSession(image=True)
                state = self.pipeline(session, job=job, publisher=publisher).run('validate')
                self.assertEqual(state['stage'], 'prepare')
                hard = state['verification_batches']['hard']
                if target == 'batch':
                    path = Path(hard['batch_file'])
                    records = json.loads(path.read_text())
                    records[0]['question'][':question/worked-solution'] = 'Altered after verification.'
                    path.write_text(json.dumps(records))
                else:
                    path = Path(next(iter(hard['assets'])))
                    path.write_text(path.read_text() + '<!-- changed -->')
                with self.assertRaisesRegex(ValueError, 'Reviewed hard'):
                    self.pipeline(session, job=job, publisher=publisher).run()
                self.assertEqual((publisher.prepares, publisher.publishes), (0, 0))

    def test_verifier_repair_resamples_every_band_against_one_final_package(self):
        pipeline = None

        class RepairingSession(RecordingSession):
            def __call__(self, role, context, directory):
                if role == 'review':
                    self.initial_hash = context['review_binding']['package_hash']
                    (Path(context['workspace']) / 'helper.py').write_text('def square(n): return n ** 2\n')
                    context = finalize_fixture_review(pipeline, context)
                    self.final_binding = context['review_binding']
                return super().__call__(role, context, directory)

        session = RepairingSession()
        pipeline = self.pipeline(session)
        state = pipeline.run()
        self.assertEqual(state['stage'], 'verified')
        self.assertEqual(session.roles, ['investigate', 'author', 'review'])
        self.assertNotEqual(session.initial_hash, state['package_hash'])
        self.assertEqual(session.final_binding['package_hash'], state['package_hash'])
        self.assertEqual(set(session.final_binding['verification_batches']), set(BANDS))
        approval = self.approval(state)
        self.assertEqual(approval['verification_binding'], session.final_binding)
        self.assertEqual(len({entry['review_sha256'] for entry in approval['bands'].values()}), 1)
        for band in BANDS:
            self.assertEqual(approval['bands'][band]['batch_sha256'],
                             state['verification_batches'][band]['batch_hash'])
        self.assertEqual(self.publisher.publishes, 1)

    def test_catchup_reuses_matching_completed_investigation_and_authorship(self):
        prior = self.pipeline(RecordingSession()).run()
        publisher = FakePublisher(self.root / 'catchup-publisher')
        publisher.registered_generator = {':question-generator/script': prior['registration']}
        session = RecordingSession()
        state = self.pipeline(session, job=self.root / 'catchup', publisher=publisher,
                              request={**self.request, 'difficulty': 'hard',
                                       'registered_package': prior['registration'],
                                       'reuse_pipeline': str(self.job)}).run()
        self.assertEqual(state['stage'], 'verified')
        self.assertEqual(session.roles, ['review'])
        self.assertEqual(state['reused_pipeline'], str(self.job))
        self.assertEqual(state['package_hash'], prior['package_hash'])
        self.assertEqual(publisher.exemplar_publications, [])
        self.assertEqual(set(state['verified_bands']), set(BANDS))

    def test_catchup_rebases_legacy_absolute_manifest_into_new_workspace(self):
        prior = self.pipeline(RecordingSession()).run()
        old_manifest = self.job / 'workspace' / prior['manifest']
        prior['manifest'] = str(old_manifest.resolve())
        (self.job / 'job.json').write_text(json.dumps(prior))
        publisher = FakePublisher(self.root / 'absolute-catchup-publisher')
        publisher.registered_generator = {':question-generator/script': prior['registration']}
        session = RecordingSession()
        state = self.pipeline(session, job=self.root / 'absolute-catchup', publisher=publisher,
                              request={**self.request, 'difficulty': 'hard',
                                       'registered_package': prior['registration'],
                                       'reuse_pipeline': str(self.job)}).run()
        self.assertEqual(state['stage'], 'verified')
        self.assertEqual(session.roles, ['review'])
        self.assertEqual(state['manifest'], 'package.json')
        self.assertEqual(state['package_hash'], prior['package_hash'])
        self.assertEqual(json.loads((self.job / 'job.json').read_text())['manifest'],
                         str(old_manifest.resolve()))
        self.assertEqual(set(state['verified_bands']), set(BANDS))

    def test_changed_source_cannot_skip_investigation_and_authorship_via_reuse(self):
        prior = self.pipeline(RecordingSession()).run()
        publisher = FakePublisher(self.root / 'changed-source-publisher')
        publisher.registered_generator = {':question-generator/script': prior['registration']}
        publisher.material = {**publisher.material, 'question': 'Square 8.'}
        session = RecordingSession()
        state = self.pipeline(session, job=self.root / 'changed-source', publisher=publisher,
                              request={**self.request, 'registered_package': prior['registration'],
                                       'reuse_pipeline': str(self.job)}).run()
        self.assertEqual(state['stage'], 'verified')
        self.assertEqual(session.roles, ['investigate', 'author', 'review'])
        self.assertNotIn('reused_pipeline', state)

    def test_old_verified_checkpoint_only_reverifies_and_retains_original_publication_batch(self):
        original = self.pipeline(RecordingSession()).run()
        old_published_hash = original['batch_hash']
        saved_request = (self.job / 'publication/request.json').read_bytes()
        old = dict(original)
        for key in ('verification_batches', 'verification_policy_version', 'verified_bands', 'publication_batch_hash'):
            old.pop(key, None)
        old['review_policy_version'] = REVIEW_POLICY_VERSION - 1
        old['seed'] = (old['seed'] + 12345) % (2 ** 32)
        (self.job / 'job.json').write_text(json.dumps(old))
        session = RecordingSession()
        publisher = FakePublisher(self.root / 'recovery-publisher')
        state = self.pipeline(session, publisher=publisher).run()
        self.assertEqual(state['stage'], 'verified')
        self.assertEqual(session.roles, ['review'])
        self.assertEqual((publisher.prepares, publisher.publishes), (0, 0))
        self.assertEqual((self.job / 'publication/request.json').read_bytes(), saved_request)
        self.assertEqual(state['publication_batch_hash'], old_published_hash)
        self.assertNotEqual(state['batch_hash'], old_published_hash)
        approval = self.approval(state)
        self.assertEqual(approval['publication']['batch_sha256'], old_published_hash)
        self.assertEqual(approval['bands']['easy']['batch_sha256'], state['batch_hash'])
        self.assertEqual(set(approval['bands']), set(BANDS))

    def legacy_checkpoint(self, *, published, broken_other_bands):
        """Reproduce a real pre-upgrade easy-only checkpoint, including its thread."""
        pipeline = self.pipeline(RecordingSession(difficulty='easy' if broken_other_bands else None))
        with patch('generator_pipeline.VERIFICATION_BANDS', ('easy',)):
            pipeline.run('generate')
        evidence = self.job / 'review-legacy-policy-5'
        evidence.mkdir()
        old_binding = pipeline.review_binding()
        old_binding.pop('verification_batches')
        old_binding['policy_version'] = REVIEW_POLICY_VERSION - 1
        (evidence / 'review-binding.json').write_text(json.dumps(old_binding))
        (evidence / 'final-binding.json').write_text(json.dumps(old_binding))
        (evidence / 'result.json').write_text(json.dumps({'verdict': 'accepted', 'summary': 'Legacy easy-only review.'}))
        (evidence / 'events.jsonl').write_text(json.dumps({'type': 'thread.started', 'thread_id': 'original-legacy-verifier'}) + '\n')
        state = dict(pipeline.state)
        state.update(stage='verified' if published else 'validate', review=str(evidence / 'result.json'),
                     review_policy_version=REVIEW_POLICY_VERSION - 1, review_binding=digest(old_binding),
                     active_review_directory=str(evidence), approval_recorded=published)
        for key in ('verification_batches', 'verification_policy_version', 'verified_bands', 'publication_batch_hash'):
            state.pop(key, None)
        if published:
            workspace, manifest = pipeline.manifest()
            package = publish_package(workspace, manifest['entrypoint'], manifest['files'], self.math,
                                      dependencies=manifest['dependencies'])
            self.publisher.prepare(123, pipeline.publication_records(), package.reference, package.digest,
                                   self.job / 'publication')
            state.update(registration=package.reference, publication=self.publisher.publish(self.job / 'publication'))
        (self.job / 'job.json').write_text(json.dumps(state))
        return evidence, state

    def test_legacy_nonrequested_band_failure_goes_to_original_verifier_for_repair(self):
        evidence, legacy = self.legacy_checkpoint(published=True, broken_other_bands=True)
        pipeline = None
        test = self

        class RepairingLegacySession(RecordingSession):
            def __call__(self, role, context, directory):
                test.assertEqual(role, 'review')
                test.assertEqual(context['resume_session_id'], 'original-legacy-verifier')
                test.assertEqual(Path(context['evidence_root']), evidence)
                test.assertEqual(set(context['sampling_errors']), {'moderate', 'hard'})
                test.assertEqual(set(context['verification_batches']), {'easy'})
                test.assertIn('review_contract_feedback', context)
                # The permissive upgrade is only a route into repair: ordinary
                # finalization still refuses the generator's wrong-band output.
                with test.assertRaisesRegex(ValueError, 'wrong difficulty band'):
                    pipeline.finalize_review(evidence)
                config_path = Path(context['workspace']) / 'config.json'
                config = json.loads(config_path.read_text())
                config['difficulty'] = None
                config_path.write_text(json.dumps(config))
                context = finalize_fixture_review(pipeline, context)
                return super().__call__(role, context, directory)

        session = RepairingLegacySession()
        pipeline = self.pipeline(session)
        state = pipeline.run()
        self.assertEqual(state['stage'], 'verified')
        self.assertEqual(session.roles, ['review'])
        self.assertEqual(state['attempt'], legacy['attempt'])
        self.assertEqual(state['sampling_errors'], {})
        self.assertEqual(set(state['verified_bands']), set(BANDS))
        self.assertNotEqual(state['package_hash'], legacy['package_hash'])
        self.assertFalse(state.get('needs_repair'))
        self.assertIsNone(state.get('error'))
        self.assertEqual(state.get('progress_failures', {}), {})
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (2, 2))
        self.assertTrue(list(self.job.glob('publication-before-repair-*')))

    def test_cached_old_active_review_binding_resumes_same_thread_with_contract_feedback(self):
        evidence, _ = self.legacy_checkpoint(published=False, broken_other_bands=False)
        pipeline = None
        test = self

        class ResumingSession(RecordingSession):
            def __call__(self, role, context, directory):
                test.assertEqual(role, 'review')
                test.assertEqual(context['resume_session_id'], 'original-legacy-verifier')
                test.assertEqual(Path(context['evidence_root']), evidence)
                test.assertEqual(Path(directory), evidence / 'contract-repair')
                test.assertIn('review_contract_feedback', context)
                test.assertEqual(set(context['verification_batches']), set(BANDS))
                context = finalize_fixture_review(pipeline, context)
                return super().__call__(role, context, directory)

        session = ResumingSession()
        pipeline = self.pipeline(session)
        state = pipeline.run()
        self.assertEqual(state['stage'], 'verified')
        self.assertEqual(session.roles, ['review'])
        self.assertEqual(state['review'], str(evidence / 'result.json'))
        self.assertTrue(list(evidence.glob('binding-before-all-bands-*')))
        self.assertEqual(json.loads((evidence / 'review-binding.json').read_text())['policy_version'], REVIEW_POLICY_VERSION)
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))

    def test_unfinalized_workspace_repair_resumes_original_legacy_verifier(self):
        for published in (False, True):
            with self.subTest(published=published):
                self.job = self.root / ('interrupted-' + str(published))
                self.publisher = FakePublisher(self.root / ('publisher-' + str(published)))
                evidence, legacy = self.legacy_checkpoint(published=published, broken_other_bands=False)
                # The old verifier edited declared bytes, then was interrupted
                # before its finalization subprocess saved the new identity.
                (self.job / 'workspace/helper.py').write_text('def square(n): return n ** 2\n')
                pipeline = None
                test = self

                class ResumeUnfinalizedSession(RecordingSession):
                    def __call__(self, role, context, directory):
                        test.assertEqual(role, 'review')
                        test.assertEqual(context['resume_session_id'], 'original-legacy-verifier')
                        test.assertNotEqual(context['review_binding']['package_hash'], legacy['package_hash'])
                        test.assertEqual(context['review_binding']['package_hash'], pipeline.candidate_hash())
                        if published:
                            test.assertEqual(pipeline.state['publication_package_hash'], legacy['package_hash'])
                        context = finalize_fixture_review(pipeline, context)
                        return super().__call__(role, context, directory)

                session = ResumeUnfinalizedSession()
                pipeline = self.pipeline(session)
                state = pipeline.run()
                self.assertEqual(state['stage'], 'verified')
                self.assertEqual(session.roles, ['review'])
                self.assertEqual(state['review'], str(evidence / 'result.json'))
                self.assertEqual(state['attempt'], legacy['attempt'])
                self.assertNotEqual(state['package_hash'], legacy['package_hash'])
                self.assertEqual(Path(state['registration']).parts[2], state['package_hash'])
                self.assertEqual(self.approval(state)['identity']['package_sha256'], state['package_hash'])
                self.assertEqual((self.publisher.prepares, self.publisher.publishes),
                                 (2, 2) if published else (1, 1))
                self.assertEqual(bool(list(self.job.glob('publication-before-repair-*'))), published)
                self.assertIsNone(state.get('error'))

    def test_legacy_exhausted_review_budget_gets_one_bounded_upgrade_allowance(self):
        evidence, legacy = self.legacy_checkpoint(published=False, broken_other_bands=False)
        legacy.update(review_sessions=[str(evidence)] + [str(evidence / ('contract-repair' if index == 1
                          else 'contract-repair-' + str(index))) for index in range(1, 9)],
                      review_session_limit=9, review_report_rounds={str(evidence): 9},
                      review_report_limits={str(evidence): 9})
        (self.job / 'job.json').write_text(json.dumps(legacy))
        session = RecordingSession(reject=True)
        state = self.pipeline(session).run()
        self.assertEqual(state['stage'], 'blocked')
        self.assertEqual(state['error']['code'], 'verification_unfinished')
        self.assertEqual(session.roles, ['review', 'review', 'review'])
        self.assertEqual(state['review_session_limit'], 12)
        self.assertEqual(len(state['review_sessions']), 12)
        self.assertEqual(state['review_report_limits'][str(evidence)], 12)
        self.assertEqual(state['review_report_rounds'][str(evidence)], 12)
        self.assertEqual(state['verification_upgrade']['policy'], REVIEW_POLICY_VERSION)
        upgrade = state['verification_upgrade']
        restarted = RecordingSession()
        after_restart = self.pipeline(restarted).run()
        self.assertEqual(after_restart['stage'], 'blocked')
        self.assertEqual(restarted.roles, [])
        self.assertEqual(after_restart['verification_upgrade'], upgrade)
        self.assertEqual(after_restart['review_session_limit'], 12)
        self.assertEqual(after_restart['review_report_limits'][str(evidence)], 12)
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (0, 0))


if __name__ == '__main__':
    unittest.main()
