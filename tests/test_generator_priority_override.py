"""Explicit scratch backlog uses the normal workers, resumes, and quality gates."""
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

from inventory_jobs import save
from test_inventory_jobs import RankedInventoryJobTests


class GeneratorPriorityOverrideTests(unittest.TestCase):
    setUp = RankedInventoryJobTests.setUp
    tearDown = RankedInventoryJobTests.tearDown
    kp = RankedInventoryJobTests.kp
    ranked = RankedInventoryJobTests.ranked
    relevant = RankedInventoryJobTests.relevant
    gated = RankedInventoryJobTests.gated
    path_for = RankedInventoryJobTests.path_for
    records = RankedInventoryJobTests.records
    admit_review_backlog = RankedInventoryJobTests.admit_review_backlog

    def prioritize(self, *kps, **values):
        path = self.jobs.directory / 'overrides/priority-builds.json'
        save(path, {'lineage': 'same', 'knowledge_points': list(kps), **values})
        return path

    def execute(self, claimed):
        def run(command, **kwargs):
            claimed.append(json.loads(Path(command[3]).read_text())['request']['knowledgePoint'])
            return subprocess.CompletedProcess(command, 0)
        return run

    def test_withdrawn_outside_scope_jobs_return_without_duplicating_or_restarting_drafts(self):
        ordinary, scratch, draft = (self.relevant(self.kp(i, topic=i), 1) for i in (1, 2, 3))
        initial = self.ranked(ordinary, scratch, draft)
        self.jobs.accept(initial)
        path = self.path_for(3, 'build')
        self.jobs.finish(path, {'attempts': 2, 'processFailures': 1})
        checkpoint = path.with_suffix('.pipeline') / '1/job.json'
        state = {'stage': 'validate', 'attempt': 2, 'active_review_directory': 'original-thread'}
        save(checkpoint, state)
        outside = self.gated(self.ranked(ordinary), missing=(1,))
        self.jobs.accept(outside)
        self.assertEqual({j['state'] for j in self.records() if j['request']['knowledgePoint'] in (2, 3)}, {'withdrawn'})
        self.prioritize(2, 3)
        self.jobs.accept(outside)
        self.jobs.accept(outside)
        records = self.records()
        self.assertEqual(len(records), 3)
        self.assertEqual(sum(j['state'] in {'pending', 'running'} for j in records), 3)
        resumed = json.loads(path.read_text())
        self.assertEqual((resumed['cycle'], resumed['attempts'], resumed['processFailures']), (1, 2, 1))
        self.assertEqual(json.loads(checkpoint.read_text()), state)
        claimed = []
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=self.execute(claimed)):
            self.jobs.run_one()
            self.jobs.run_one()
        self.assertEqual(set(claimed), {2, 3})

    def test_all_six_slots_prioritize_explicit_backlog_ahead_of_ordinary_and_reserved_reviews(self):
        self.jobs.environment['COURSE_ACADEMY_GENERATOR_BUILD_WORKERS'] = '6'
        self.admit_review_backlog(self.relevant(self.kp(1, topic=1), 0),
                                 *(self.relevant(self.kp(i, topic=i), 4) for i in range(2, 8)))
        self.prioritize(*range(2, 8))
        claimed = []
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=self.execute(claimed)):
            for slot in range(6):
                self.assertTrue(self.jobs.run_one('build', slot))
        self.assertEqual(set(claimed), set(range(2, 8)))

    def test_exact_publication_recovery_still_precedes_explicit_backlog(self):
        self.jobs.accept(self.ranked(self.kp(1), self.kp(2)))
        self.prioritize(1)
        path = self.path_for(2, 'build')
        directory = path.with_suffix('.pipeline') / '1'
        save(directory / 'job.json', {'stage': 'push'})
        save(directory / 'publication/request.json', {'request_key': 'exact-original-request'})
        claimed = []
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=self.execute(claimed)):
            self.jobs.run_one('build', 2)
            self.jobs.run_one('build', 2)
        self.assertEqual(claimed, [2, 1])
        self.assertEqual(json.loads((directory / 'publication/request.json').read_text()),
                         {'request_key': 'exact-original-request'})

    def test_only_verified_three_band_publication_releases_priority_and_release_persists(self):
        self.jobs.accept(self.ranked(*(self.relevant(self.kp(i, topic=i), 0 if i == 1 else 4)
                                      for i in range(1, 6))))
        path = self.prioritize(2, 3, 4, 5)
        package = 'generators/aa/' + 'a' * 64 + '/generator.py'
        complete = {'outcome': 'generated', 'generator': package, 'verified_package': package,
                    'verified_bands': ['easy', 'moderate', 'hard'],
                    'publication': {'passed': True, 'package_sha256': 'a' * 64}}
        outcomes = {2: complete, 3: {**complete, 'verified_bands': ['hard']},
                    4: {**complete, 'publication': {'passed': False, 'package_sha256': 'a' * 64}},
                    5: {**complete, 'publication': {'passed': True, 'package_sha256': 'b' * 64}}}
        for kp, outcome in outcomes.items():
            job = self.path_for(kp, 'build')
            self.jobs.finish(job, {'state': 'awaiting-verification', 'outcome': outcome})
        self.jobs.accept(self.ranked(self.relevant(self.kp(1), 0)))
        self.assertEqual(json.loads(path.read_text())['completed_knowledge_points'], [2])
        # Later unrelated work for this KP cannot bring the finished migration back.
        job = self.path_for(2, 'build')
        record = json.loads(job.read_text())
        save(job, {**record, 'state': 'pending', 'outcome': {}, 'retryAt': 0})
        for kp in (3, 4, 5):
            self.jobs.finish(self.path_for(kp, 'build'), {'state': 'blocked'})
        claimed = []
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=self.execute(claimed)):
            self.jobs.run_one()
            self.jobs.run_one()
        self.assertEqual(claimed, [1, 2])
        self.assertEqual(json.loads(path.read_text())['completed_knowledge_points'], [2])

    def test_override_never_resets_blocked_or_rejected_failure_budgets(self):
        self.jobs.accept(self.ranked(self.kp(1), self.kp(2)))
        for kp, state in ((1, 'blocked'), (2, 'rejected')):
            self.jobs.finish(self.path_for(kp, 'build'), {'state': state, 'attempts': 7,
                              'processFailures': 3, 'outcome': {'reason': 'needs repair'}})
        self.prioritize(1, 2)
        self.jobs.accept(self.ranked())
        self.jobs.accept(self.ranked(self.kp(1), self.kp(2)))
        self.assertEqual([(j['state'], j['attempts'], j['processFailures'])
                          for j in sorted(self.records(), key=lambda j: j['request']['knowledgePoint'])],
                         [('blocked', 7, 3), ('rejected', 7, 3)])
        self.assertFalse(self.jobs.run_one())

    def test_removing_override_restores_normal_order_without_restart(self):
        self.jobs.accept(self.ranked(self.relevant(self.kp(1), 0), self.relevant(self.kp(2), 4)))
        path = self.prioritize(2)
        path.unlink()
        claimed = []
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=self.execute(claimed)):
            self.jobs.run_one()
        self.assertEqual(claimed, [1])

    def test_lineage_or_invalid_ids_cannot_retarget_an_override(self):
        self.jobs.accept(self.ranked(self.kp(1)))
        for values in ({'lineage': 'other'}, {'knowledge_points': [True]},
                       {'completed_knowledge_points': [2]}):
            with self.subTest(values=values):
                self.prioritize(1, **values)
                with self.assertRaises(ValueError):
                    self.jobs.accept(self.ranked(self.kp(1)))


del RankedInventoryJobTests

if __name__ == '__main__':
    unittest.main()
