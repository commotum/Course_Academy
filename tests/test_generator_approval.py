from copy import deepcopy
import unittest

from generator_approval import ApprovalError, BANDS, approved_band, make_approval


class GeneratorApprovalTests(unittest.TestCase):
    def setUp(self):
        self.policy = 6
        self.engine = 'e' * 64
        self.identity = {
            'database': 'math', 'lineage': 'fixture', 'kp_id': 123,
            'source_sha256': 'a' * 64, 'package_sha256': 'b' * 64,
            'registration': 'generators/packages/' + 'b' * 64 + '/generator.py',
        }
        self.binding = {
            'policy_version': self.policy, 'source_hash': 'c' * 64,
            'package_hash': self.identity['package_sha256'], 'engine_hash': self.engine,
            'batch_hash': '1' * 64,
            'verification_batches': {
                band: {'batch_hash': str(index + 1) * 64, 'seed': 42, 'count': 5, 'assets': {}}
                for index, band in enumerate(BANDS)
            },
        }
        self.review = {
            'verdict': 'accepted', 'band_verification': {
                band: {'status': 'passed', 'batch_sha256': batch['batch_hash'],
                       'evidence_paths': [band + '/checks.json'], 'details': 'Checked all samples'}
                for band, batch in self.binding['verification_batches'].items()
            },
        }
        self.publication = {'passed': True, 'request_key': 'publication-123', 'new_questions': 5}

    def make(self, **overrides):
        args = dict(identity=self.identity, review=self.review, binding=self.binding,
                    review_path='/evidence/result.json', publication=self.publication,
                    published_band='easy', policy_version=self.policy)
        args.update(overrides)
        return make_approval(**args)

    def assert_rejected(self, record, code, **overrides):
        args = dict(value=record, identity=self.identity, band='easy',
                    policy_version=self.policy, engine_hash=self.engine)
        args.update(overrides)
        with self.assertRaises(ApprovalError) as error:
            approved_band(**args)
        self.assertEqual(error.exception.code, code)

    def test_all_verified_bands_are_refill_eligible_after_only_easy_was_published(self):
        record = self.make()
        self.assertEqual(record['format'], 2)
        self.assertEqual(record['publication'], {
            'difficulty': 'easy', 'batch_sha256': self.binding['batch_hash'], 'receipt': self.publication,
        })
        for band in BANDS:
            eligible = approved_band(record, self.identity, band, self.policy, self.engine)
            self.assertEqual(eligible['difficulty'], band)
            self.assertEqual(eligible['approval']['batch_sha256'], self.review['band_verification'][band]['batch_sha256'])
            self.assertNotIn('publication', record['bands'][band])

    def test_catchup_keeps_actual_published_batch_separate_from_new_review_samples(self):
        record = self.make(publication_batch_hash='f' * 64)
        self.assertEqual(record['publication']['batch_sha256'], 'f' * 64)
        self.assertEqual(record['bands']['easy']['batch_sha256'], '1' * 64)
        approved_band(record, self.identity, 'hard', self.policy, self.engine)

    def test_missing_failed_or_stale_band_never_receives_approval(self):
        for problem in ('missing', 'failed', 'old_batch', 'no_evidence'):
            with self.subTest(problem=problem):
                review = deepcopy(self.review)
                if problem == 'missing':
                    review['band_verification'].pop('hard')
                elif problem == 'failed':
                    review['band_verification']['hard']['status'] = 'failed'
                elif problem == 'old_batch':
                    review['band_verification']['hard']['batch_sha256'] = 'f' * 64
                else:
                    review['band_verification']['hard']['evidence_paths'] = []
                with self.assertRaises(ValueError):
                    self.make(review=review)

    def test_final_package_and_complete_binding_are_required(self):
        for problem in ('package', 'engine', 'source', 'batch', 'missing_band', 'count', 'assets'):
            with self.subTest(problem=problem):
                binding = deepcopy(self.binding)
                if problem in ('package', 'engine', 'source'):
                    binding[problem + '_hash'] = 'changed'
                elif problem == 'missing_band':
                    binding['verification_batches'].pop('moderate')
                else:
                    binding['verification_batches']['hard'][{'batch': 'batch_hash', 'count': 'count', 'assets': 'assets'}[problem]] = {
                        'batch': 'wrong', 'count': 0, 'assets': {'image.svg': 'wrong'},
                    }[problem]
                with self.assertRaises(ValueError):
                    self.make(binding=binding)

    def test_no_approval_without_verified_publication(self):
        for publication in ({}, {'passed': False}, {'passed': 'true'}):
            with self.subTest(publication=publication), self.assertRaises(ValueError):
                self.make(publication=publication)

    def test_source_package_and_engine_changes_reject_refill(self):
        record = self.make()
        for name in ('source_sha256', 'package_sha256', 'registration', 'kp_id', 'lineage'):
            with self.subTest(name=name):
                identity = {**self.identity, name: 'changed'}
                self.assert_rejected(record, 'source_changed', identity=identity)
        self.assert_rejected(record, 'approval_engine_changed', engine_hash='f' * 64)

    def test_current_policy_is_required(self):
        self.assert_rejected(self.make(), 'approval_policy_stale', policy_version=self.policy + 1)

    def test_legacy_records_do_not_gain_unreviewed_bands(self):
        legacy = {'format': 1, 'identity': self.identity, 'bands': {'easy': {
            'review_policy_version': self.policy - 1, 'review_sha256': 'd' * 64,
            'batch_sha256': '1' * 64, 'publication': self.publication,
        }}}
        self.assert_rejected(legacy, 'approval_band_missing', band='hard')
        self.assert_rejected(legacy, 'approval_policy_stale')
        legacy['bands']['easy']['review_policy_version'] = self.policy
        self.assert_rejected(legacy, 'approval_policy_stale')

    def test_corrupt_cross_band_evidence_cannot_authorize_otherwise_valid_easy_refill(self):
        for problem in ('missing', 'policy', 'batch', 'engine', 'review', 'evidence', 'publication_copy'):
            with self.subTest(problem=problem):
                record = self.make()
                hard = record['bands']['hard']
                if problem == 'missing':
                    record['bands'].pop('hard')
                elif problem == 'policy':
                    hard['review_policy_version'] = self.policy - 1
                elif problem == 'batch':
                    hard['batch_sha256'] = 'f' * 64
                elif problem == 'engine':
                    hard['engine_sha256'] = 'f' * 64
                elif problem == 'review':
                    hard['review_sha256'] = 'f' * 64
                elif problem == 'evidence':
                    hard['evidence'] = '/other-review/result.json'
                else:
                    hard['publication'] = self.publication
                self.assert_rejected(record, 'approval_invalid')

    def test_mutating_inputs_or_returned_eligibility_cannot_mutate_saved_approval(self):
        record = self.make()
        eligible = approved_band(record, self.identity, 'easy', self.policy, self.engine)
        eligible['approval']['evidence_paths'].clear()
        self.binding['verification_batches']['easy']['assets']['new'] = 'f' * 64
        self.review['band_verification']['easy']['evidence_paths'].clear()
        self.publication['passed'] = False
        self.assertTrue(record['bands']['easy']['evidence_paths'])
        self.assertEqual(record['verification_binding']['verification_batches']['easy']['assets'], {})
        self.assertIs(record['publication']['receipt']['passed'], True)


if __name__ == '__main__':
    unittest.main()
