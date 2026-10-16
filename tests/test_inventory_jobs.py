import json
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from inventory_jobs import InventoryJobs

class InventoryJobTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        self.jobs = InventoryJobs(self.directory, self.directory / 'jobs', 'learner')
        self.request = dict(knowledgePoint=1, topic=2, difficulty='hard', available=0,
                            missing=5, urgency=0, proximity=1, priority=12,
                            stage='create-generator', script=None, basis=10)
    def tearDown(self):
        self.temp.cleanup()
    def accept(self, jobs=None, topics=None, **changes):
        self.jobs.accept(dict(basis=10, lineage='same', jobs=[self.request] if jobs is None else jobs,
                              qualifyingTopics=[2] if topics is None else topics, **changes))
    def records(self):
        return [json.loads(p.read_text()) for p in self.jobs.directory.glob('*.json') if p.name != 'cursor.json']
    def test_overlapping_triggers_restart_and_cursor_do_not_duplicate_jobs(self):
        self.accept(); self.accept()
        restarted = InventoryJobs(self.directory, self.jobs.directory, 'learner')
        self.assertEqual(len(self.records()), 1)
        self.assertEqual(self.records()[0]['state'], 'pending')
        self.assertEqual(json.loads((restarted.directory / 'cursor.json').read_text())['basis'],10)
        with self.assertRaises(ValueError):
            restarted.accept(dict(basis=11,lineage='different',jobs=[],qualifyingTopics=[]))
        with self.assertRaises(ValueError):
            restarted.accept(dict(basis=9,lineage='same',jobs=[],qualifyingTopics=[]))
    def test_disappearing_trigger_is_withdrawn_and_only_observed_stock_is_verified(self):
        self.accept(); self.accept(jobs=[],topics=[])
        self.assertEqual(self.records()[0]['state'],'withdrawn')
        self.accept(); self.assertEqual(self.records()[0]['state'],'pending')
        self.accept(jobs=[])
        self.assertEqual(self.records()[0]['state'],'verified')
    def test_worker_exit_is_not_inventory_verification_and_transport_failures_resume(self):
        self.accept()
        with patch('inventory_jobs.subprocess.run') as run:
            run.return_value.returncode=0
            self.assertTrue(self.jobs.run_one())
        self.assertEqual(self.records()[0]['state'],'awaiting-verification')
        self.accept(jobs=[])
        self.assertEqual(self.records()[0]['state'],'verified')
        self.accept()
        with patch('inventory_jobs.subprocess.run') as run, patch('inventory_jobs.time.time',return_value=100000000000):
            run.return_value.returncode=1
            # Explicitly advance time between retries.
            for index in range(3):
                with patch('inventory_jobs.time.time',return_value=100000000000+index*10000):
                    self.jobs.run_one()
        self.assertEqual(self.records()[0]['state'],'pending')
        self.assertFalse(self.jobs.run_one())

    def test_registered_generator_uses_pipeline_and_stale_result_is_not_reused(self):
        script = self.directory / 'generator.py'
        script.write_text('raise RuntimeError("unsupported band")\n')
        self.request.update(stage='generate', script='generator.py')
        self.accept()
        path = next(p for p in self.jobs.directory.glob('*.json') if p.name != 'cursor.json')
        path.with_suffix('.result').write_text(json.dumps({'outcome': 'unsupported'}))
        with patch('inventory_jobs.subprocess.run') as run:
            run.return_value = subprocess.CompletedProcess(['pipeline'], 0)
            self.assertTrue(self.jobs.run_one())
        self.assertEqual(run.call_count, 1)
        self.assertIn('scripts/generator_pipeline.py', run.call_args.args[0][1])
        self.assertIn('--inventory-cycle', run.call_args.args[0])
        self.assertEqual(self.records()[0]['state'], 'awaiting-verification')
        self.assertTrue(path.with_suffix('.result.previous-1').exists())

    def test_content_failure_stops_retrying_and_old_cycle_cannot_finish_new_work(self):
        self.accept()
        path = next(p for p in self.jobs.directory.glob('*.json') if p.name != 'cursor.json')
        def rejected(*args, **kwargs):
            path.with_suffix('.result').write_text(json.dumps({'outcome': 'failed'}))
            return subprocess.CompletedProcess(args[0], 1)
        with patch('inventory_jobs.subprocess.run', side_effect=rejected):
            self.jobs.run_one()
        self.assertEqual(self.records()[0]['state'], 'rejected')
        self.assertFalse(self.jobs.run_one())
        self.accept(jobs=[])
        self.accept()
        self.jobs.finish(path, {'state': 'rejected'}, cycle=1)
        self.assertEqual(self.records()[0]['state'], 'pending')
        self.assertEqual(self.records()[0]['cycle'], 2)

    def test_remaining_shortage_starts_new_cycle_after_verified_publication(self):
        self.accept()
        path = next(p for p in self.jobs.directory.glob('*.json') if p.name != 'cursor.json')
        self.jobs.finish(path, {'state': 'awaiting-verification', 'replenishments': 1, 'retryAt': 0})
        self.accept()
        self.assertEqual(self.records()[0]['state'], 'pending')
        self.assertEqual(self.records()[0]['cycle'], 2)

    def test_service_finds_creator_without_shell_path_and_reopens_environment_failure(self):
        creator = self.directory / 'codex'
        creator.touch()
        self.jobs.environment['COURSE_ACADEMY_CODEX_EXECUTABLE'] = str(creator)
        self.jobs.environment['PATH'] = '/usr/bin'
        self.accept()
        path = next(p for p in self.jobs.directory.glob('*.json') if p.name != 'cursor.json')
        self.jobs.finish(path, {'state': 'rejected', 'attempts': 3,
                                'error': "[Errno 2] No such file or directory: 'codex'"})
        self.accept()
        self.assertEqual(self.records()[0]['state'], 'pending')
        self.assertEqual(self.records()[0]['attempts'], 0)
        self.assertEqual(self.jobs.creator_executable(), str(creator))

    def test_interrupted_worker_recovers_same_attempt(self):
        self.accept()
        path = next(p for p in self.jobs.directory.glob('*.json') if p.name != 'cursor.json')
        self.jobs.finish(path, {'state': 'running', 'attempts': 3})
        # Recover unknown work before starting a higher-ranked fresh job.
        self.accept(jobs=[self.request, {**self.request, 'knowledgePoint': 3, 'priority': 9999}])
        with patch('inventory_jobs.subprocess.run') as run:
            run.return_value.returncode = 0
            self.assertTrue(self.jobs.run_one())
        recovered = json.loads(path.read_text())
        self.assertEqual(recovered['attempts'], 3)
        self.assertEqual(recovered['state'], 'awaiting-verification')
        self.assertEqual(len([j for j in self.records() if j['state'] == 'pending']), 1)

if __name__ == '__main__': unittest.main()
