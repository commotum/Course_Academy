import fcntl
import json
from pathlib import Path
import tempfile
import unittest

from recover_engine_only_refills import recover


class EngineOnlyRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def job(self, name, *, kind='refill', code='approval_engine_changed', package='generators/ab/package/generator.py'):
        value = {'state': 'repair-needed' if kind == 'refill' else 'pending', 'cycle': 1,
                 'request': {'knowledgePoint': 123, 'jobKind': kind, 'script': package,
                             'stage': 'generate' if kind == 'refill' else 'review-generator'},
                 'outcome': {'reason': {'code': code}} if kind == 'refill' else {}}
        path = self.root / (name + '.json')
        path.write_text(json.dumps(value))
        return path

    def test_reopens_engine_only_failures_in_new_cycle_and_withdraws_only_unstarted_review(self):
        refill = self.job('refill')
        review = self.job('review', kind='build')
        old = refill.with_suffix('.pipeline') / '1'
        old.mkdir(parents=True)
        (old / 'job.json').write_text('{"stage":"unsupported"}')
        before = (old / 'job.json').read_bytes()
        proposed = recover(self.root)
        self.assertEqual(len(proposed['reopened_refills']), 1)
        self.assertEqual(json.loads(refill.read_text())['state'], 'repair-needed')
        result = recover(self.root, apply=True)
        new = json.loads(refill.read_text())
        self.assertEqual((new['state'], new['cycle'], new['processFailures']), ('pending', 2, 0))
        self.assertEqual(new['recovery_events'][0]['previous_outcome']['reason']['code'], 'approval_engine_changed')
        self.assertEqual((old / 'job.json').read_bytes(), before)
        self.assertEqual(json.loads(review.read_text())['state'], 'withdrawn')
        self.assertEqual(len(result['withdrawn_reviews']), 1)
        self.assertEqual(recover(self.root, apply=True)['reopened_refills'], [])

    def test_substantive_failure_keeps_review_and_is_not_reopened(self):
        self.job('engine')
        content = self.job('content', code='generator_failed')
        review = self.job('review', kind='build')
        result = recover(self.root, apply=True)
        self.assertEqual(len(result['reopened_refills']), 1)
        self.assertEqual(result['withdrawn_reviews'], [])
        self.assertEqual(json.loads(content.read_text())['state'], 'repair-needed')
        self.assertEqual(json.loads(review.read_text())['state'], 'pending')

    def test_held_kp_lock_and_publication_intents_preserve_jobs(self):
        refill = self.job('refill')
        self.job('review', kind='build')
        before = refill.read_bytes()
        with (self.root / 'kp-123.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.assertEqual(recover(self.root, apply=True)['locked_kps'], [123])
        publication = refill.with_suffix('.pipeline') / '1/publication'
        publication.mkdir(parents=True)
        (publication / 'request.json').write_text('{"request_key":"do-not-replace"}')
        result = recover(self.root, apply=True)
        self.assertEqual(result['preserved_publications'], [str(refill)])
        self.assertEqual(refill.read_bytes(), before)
        self.assertEqual(result['withdrawn_reviews'], [])

    def test_started_work_and_other_package_reviews_are_retained(self):
        self.job('refill', code='engine_changed')
        started = self.job('started', kind='build')
        (started.with_suffix('.pipeline') / '1').mkdir(parents=True)
        other = self.job('other', kind='build', package='generators/zz/another/generator.py')
        result = recover(self.root, apply=True)
        self.assertEqual(len(result['reopened_refills']), 1)
        self.assertEqual(result['withdrawn_reviews'], [])
        self.assertEqual(json.loads(started.read_text())['state'], 'pending')
        self.assertEqual(json.loads(other.read_text())['state'], 'pending')

    def test_preexisting_future_cycle_is_not_overwritten(self):
        refill = self.job('refill')
        future = refill.with_suffix('.pipeline') / '2'
        future.mkdir(parents=True)
        (future / 'job.json').write_text('{"stage":"validate"}')
        recover(self.root, apply=True)
        self.assertEqual(json.loads(refill.read_text())['cycle'], 3)
        self.assertEqual((future / 'job.json').read_text(), '{"stage":"validate"}')


if __name__ == '__main__':
    unittest.main()
