import json
import copy
import fcntl
from concurrent.futures import ThreadPoolExecutor
import subprocess
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from inventory_jobs import InventoryJobs, build_worker_count, review_worker_count, priority_key, ranked_requests, save
from generator_priority import PRIORITY_POLICY

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
        with patch('inventory_jobs.InventoryJobs._run_pipeline') as run:
            run.return_value.returncode=0
            self.assertTrue(self.jobs.run_one())
        self.assertEqual(self.records()[0]['state'],'awaiting-verification')
        self.accept(jobs=[])
        self.assertEqual(self.records()[0]['state'],'verified')
        self.accept()
        with patch('inventory_jobs.InventoryJobs._run_pipeline') as run, patch('inventory_jobs.time.time',return_value=100000000000):
            run.return_value.returncode=1
            # Explicitly advance time between retries.
            for index in range(3):
                with patch('inventory_jobs.time.time',return_value=100000000000+index*10000):
                    self.jobs.run_one()
        self.assertEqual(self.records()[0]['state'],'blocked')
        self.assertFalse(self.jobs.run_one())

    def test_registered_generator_uses_pipeline_and_stale_result_is_not_reused(self):
        script = self.directory / 'generator.py'
        script.write_text('raise RuntimeError("unsupported band")\n')
        self.request.update(stage='generate', script='generator.py')
        self.accept()
        path = next(p for p in self.jobs.directory.glob('*.json') if p.name != 'cursor.json')
        path.with_suffix('.result').write_text(json.dumps({'outcome': 'unsupported'}))
        with patch('inventory_jobs.InventoryJobs._run_pipeline') as run:
            run.return_value = subprocess.CompletedProcess(['pipeline'], 0)
            self.assertTrue(self.jobs.run_one())
        self.assertEqual(run.call_count, 1)
        self.assertIn('scripts/generator_pipeline.py', run.call_args.args[0][1])
        self.assertIn('--inventory-cycle', run.call_args.args[0])
        self.assertEqual(self.records()[0]['state'], 'awaiting-verification')
        self.assertTrue(path.with_suffix('.result.previous-1').exists())

    def test_terminal_pipeline_failure_stays_blocked_across_refreshes(self):
        self.accept()
        path = next(p for p in self.jobs.directory.glob('*.json') if p.name != 'cursor.json')
        def rejected(*args, **kwargs):
            path.with_suffix('.result').write_text(json.dumps({'outcome': 'blocked', 'reason': {'code': 'no_progress'}}))
            return subprocess.CompletedProcess(args[0], 1)
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=rejected) as run:
            self.jobs.run_one()
            self.accept(jobs=[])
            self.accept()
            self.assertFalse(self.jobs.run_one())
        self.assertEqual(run.call_count, 1)
        self.assertEqual(self.records()[0]['state'], 'blocked')
        self.assertEqual(self.records()[0]['cycle'], 1)
        self.assertEqual(self.records()[0]['outcome']['reason']['code'], 'no_progress')

    def test_legacy_repair_yield_stops_without_rearming_pipeline(self):
        self.accept()
        path = next(p for p in self.jobs.directory.glob('*.json') if p.name != 'cursor.json')
        before = json.loads(path.read_text())
        def repair(*args, **kwargs):
            path.with_suffix('.result').write_text(json.dumps({'outcome': 'repair-pending', 'needs_repair': True}))
            return subprocess.CompletedProcess(args[0], 1)
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=repair):
            self.assertTrue(self.jobs.run_one())
        self.accept()
        after = json.loads(path.read_text())
        self.assertEqual(after['state'], 'blocked')
        self.assertEqual(after['request'], before['request'])
        self.assertEqual(after['cycle'], before['cycle'])
        self.assertFalse(self.jobs.run_one())

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
        with patch('inventory_jobs.InventoryJobs._run_pipeline') as run:
            run.return_value.returncode = 0
            self.assertTrue(self.jobs.run_one())
        recovered = json.loads(path.read_text())
        self.assertEqual(recovered['attempts'], 3)
        self.assertEqual(recovered['state'], 'awaiting-verification')
        self.assertEqual(len([j for j in self.records() if j['state'] == 'pending']), 1)

class RankedInventoryJobTests(unittest.TestCase):
    setUp = InventoryJobTests.setUp
    tearDown = InventoryJobTests.tearDown
    accept = InventoryJobTests.accept
    records = InventoryJobTests.records
    def kp(self, entity=1, topic=2, *, script=None, score=64200, urgency=4, purpose='lesson-shortage'):
        return {'db/id': entity, 'topic_entity': topic, 'generator_script': script,
                'generator_usable': bool(script), 'urgency_value': urgency,
                'score': score, 'purpose': purpose, 'shortage': 4, 'next_activity': 'lesson',
                'first_studied_at': None, 'waiting_since': None,
                'inventory': {'available': {'easy': 1, 'moderate': 0, 'hard': 0}},
                'refill_deficits': {'easy': 4, 'moderate': 5, 'hard': 5},
                'priority_reasons': [{'score': score, 'purpose': purpose, 'shortage': 4}]}

    def ranked(self, *kps, basis=10):
        return {'basis': basis, 'cursor': {'basis': basis, 'lineage': 'same'},
                'topics': [{'db/id': kp['topic_entity'], 'knowledge_points': [copy.deepcopy(kp)]} for kp in kps],
                'knowledge_points': [copy.deepcopy(kp) for kp in kps if not kp['generator_usable'] and kp['urgency_value']]}

    def relevant(self, kp, tier, **context):
        metadata = {'priority_policy': PRIORITY_POLICY, 'relevance_tier': tier,
                    'baseline_relevance_tier': tier, 'topic_layer': 10,
                    'selected_support_count': 1, 'engine_priority': 0, **context}
        kp.update(metadata)
        kp['priority_reasons'] = [{**reason, **metadata} for reason in kp['priority_reasons']]
        return kp

    def gated(self, inventory, *, opened=False, missing=(), understocked=(1,)):
        return {**inventory, 'selection_gate': {
            'open': opened, 'selected_knowledge_points': [1],
            'missing_generators': list(missing), 'understocked_knowledge_points': list(understocked),
            'required_per_band': 5,
        }}

    def path_for(self, kp, kind=None, difficulty=None):
        for path in self.jobs.directory.glob('*.json'):
            job = json.loads(path.read_text())
            request = job.get('request', {})
            if (request.get('knowledgePoint') == kp and (kind is None or request.get('jobKind') == kind)
                    and (difficulty is None or request.get('difficulty') == difficulty)):
                return path
        self.fail('Job not found')

    def study_scope_inventory(self, *specifications):
        # Native discovery supplies the bounded lesson scope before Python ranks
        # it. Keep this fixture explicit so the test exercises the real finder,
        # durable handoff and worker claim rather than a preordered request list.
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'generate/scripts'))
        from find_candidates import ranked_candidates
        topics = []
        for topic, layer, group, activity, tier, available, new_lesson in specifications:
            stock = {'available': {'easy': available, 'moderate': 0, 'hard': 0},
                     'available_total': available, 'rated_total': available,
                     'supported_difficulties': ['easy', 'moderate', 'hard']}
            topics.append({'db/id': topic, 'topic/title': f'Topic {topic}',
                'topic_layer': layer, 'relevance_tier': tier,
                'selected_support_count': 1, 'engine_priority': 0,
                'new_scoped_lesson': new_lesson, 'urgency_groups': [group],
                'studied': not new_lesson, 'reviewed': not new_lesson,
                'completed_local_lesson': not new_lesson,
                'next_activity': activity,
                'activity_demands': [{'activity_type': activity, 'relevance_tier': tier}],
                'topic_inventory': copy.deepcopy(stock),
                'knowledge_points': [{'db/id': topic * 10, 'generator_script': None,
                    'generator_usable': False, 'has_generator': False,
                    'inventory': copy.deepcopy(stock)}]})
        return ranked_candidates({'basis': 10, 'cursor': {'basis': 10, 'lineage': 'same'},
                                  'self_directed': True, 'topics': topics})

    def test_study_scope_shortages_reach_workers_before_later_direct_and_maintenance_work(self):
        inventory = self.study_scope_inventory(
            (1, 60, 'target', 'lesson', 1, 0, True),
            (2, 37, 'selected-prerequisite', 'lesson', 1, 0, True),
            (3, 29, 'target', 'review', 1, 5, False),
            (4, 80, 'current-need', 'review', 0, 0, False),
        )
        # An empty later target bank cannot close admission to the earlier
        # depth-two lesson; actual active work still leads the ordinary backlog.
        gate = inventory['selection_gate']
        self.assertTrue(gate['open'])
        self.assertEqual(gate['mode'], 'study-scope')
        self.assertTrue({10, 20}.issubset(gate['selected_knowledge_points']))
        self.assertEqual([kp['db/id'] for kp in inventory['knowledge_points']], [40, 20, 10, 30])
        self.assertEqual([request['knowledgePoint'] for request in ranked_requests(inventory)],
                         [40, 20, 10, 30])
        self.jobs.accept(inventory)
        claimed = []
        def execute(command, **kwargs):
            claimed.append(json.loads(Path(command[3]).read_text())['request']['knowledgePoint'])
            return subprocess.CompletedProcess(command, 0)
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=execute):
            for _ in range(4):
                self.assertTrue(self.jobs.run_one())
        self.assertEqual(claimed, [40, 20, 10, 30])
        self.assertFalse(self.jobs.run_one())

    def test_explicit_build_ineligibility_cannot_be_revived_by_urgency(self):
        outside = self.relevant(self.kp(1, topic=2), 1)
        outside.update(build_eligible=False, build_required=False)
        self.assertEqual(ranked_requests(self.ranked(outside)), [])
        self.jobs.accept(self.ranked(outside))
        self.assertEqual(self.records(), [])
        # An approved package may still replenish independently; it receives
        # routine demand, never the excluded context's lesson-shortage priority.
        outside.update(generator_script='generators/aa/hash/main.py', generator_usable=True)
        requests = ranked_requests(self.ranked(outside))
        self.assertTrue(requests)
        self.assertTrue(all(request['jobKind'] == 'refill' for request in requests))
        self.assertTrue(all(request['purpose'] == 'routine-replenishment' for request in requests))

    def test_ended_study_demand_withdraws_build_until_actual_package_is_observed(self):
        selected = self.relevant(self.kp(1, topic=2), 1)
        selected.update(build_eligible=True, build_required=True)
        self.jobs.accept(self.ranked(selected))
        build = self.path_for(1, 'build')
        outside = {**selected, 'build_eligible': False, 'build_required': False}
        inventory = self.ranked(outside)
        inventory['selection_gate'] = {'open': True, 'mode': 'study-scope',
                                       'selected_knowledge_points': []}
        self.jobs.accept(inventory)
        self.assertEqual(json.loads(build.read_text())['state'], 'withdrawn')
        self.assertFalse(self.jobs.run_one())
        # A subsequently observed usable package is completion evidence even
        # when the topic no longer requires an ordinary first-learning lesson.
        outside.update(generator_script='generators/aa/hash/main.py', generator_usable=True)
        self.jobs.accept(self.ranked(outside))
        self.assertEqual(json.loads(build.read_text())['state'], 'verified')
        self.assertTrue(any(job['request']['jobKind'] == 'refill' for job in self.records()))

    def test_study_scope_workers_skip_blocked_or_locked_early_lessons(self):
        self.jobs.accept(self.study_scope_inventory(
            (1, 37, 'selected-prerequisite', 'lesson', 1, 0, True),
            (2, 41, 'selected-prerequisite', 'lesson', 1, 0, True),
            (3, 44, 'target', 'lesson', 1, 0, True),
        ))
        blocked = self.path_for(10)
        self.jobs.finish(blocked, {'state': 'blocked'})
        claimed = []
        def execute(command, **kwargs):
            claimed.append(json.loads(Path(command[3]).read_text())['request']['knowledgePoint'])
            return subprocess.CompletedProcess(command, 0)
        with (self.jobs.directory / 'kp-20.lock').open('a') as busy:
            fcntl.flock(busy, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=execute):
                self.assertTrue(self.jobs.run_one())
        self.assertEqual(claimed, [30])
        self.assertEqual(json.loads(blocked.read_text())['state'], 'blocked')
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=execute):
            self.assertTrue(self.jobs.run_one())
        self.assertEqual(claimed, [30, 20])

    def test_ranking_matches_finder_and_deduplicates_legacy_builds(self):
        self.accept(jobs=[self.request, {**self.request, 'difficulty': 'easy'}])
        self.jobs.accept(self.ranked(self.kp(), self.kp(topic=3, score=65100)))
        pending = [job for job in self.records() if job['state'] == 'pending']
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]['request']['score'], 65100)
        self.assertEqual(pending[0]['request']['topic'], 3)
        self.assertEqual(pending[0]['request']['difficulty'], 'unclassified')
        self.assertEqual(pending[0]['request']['jobKind'], 'build')

    def test_old_content_failure_is_not_reopened_by_ranking_refresh(self):
        inventory = self.ranked(self.kp())
        self.jobs.accept(inventory)
        path = self.path_for(1)
        before = json.loads(path.read_text())
        self.jobs.finish(path, {'state':'rejected','outcome':{'outcome':'failed'},
                               'rejectedVariants':['legacy-failure']})
        self.jobs.accept(inventory)
        after = json.loads(path.read_text())
        self.assertEqual(after['state'], 'rejected')
        self.assertEqual(after['cycle'], before['cycle'])
        self.assertEqual(after['rejectedVariants'], ['legacy-failure'])

    def test_refresh_retains_pending_repair_inputs_and_workspace_cycle(self):
        self.jobs.accept(self.ranked(self.kp()))
        path = self.path_for(1)
        job = json.loads(path.read_text())
        state = path.with_suffix('.pipeline') / str(job['cycle']) / 'job.json'
        save(state, {'stage':'repair'})
        changed = self.kp(script='generate/scratch/repaired.py')
        self.jobs.accept(self.ranked(changed))
        after = json.loads(path.read_text())
        self.assertEqual(after['cycle'], job['cycle'])
        self.assertEqual(after['request']['script'], job['request']['script'])
        self.assertEqual(after['request']['difficulty'], job['request']['difficulty'])
        self.assertTrue(state.exists())

    def test_basis_only_refresh_advances_cursor_without_rewriting_every_job(self):
        self.jobs.accept(self.ranked(self.kp()))
        with patch('inventory_jobs.save', wraps=save) as write:
            self.jobs.accept(self.ranked(self.kp(), basis=11))
        self.assertEqual(write.call_count, 1)
        self.assertEqual(write.call_args.args[0].name, 'cursor.json')
        self.assertEqual(json.loads((self.jobs.directory / 'cursor.json').read_text())['ranking'], PRIORITY_POLICY)

    def test_selected_review_precedes_speculative_lesson_regardless_of_score(self):
        review = self.relevant(self.kp(purpose='review-shortage', score=100), 1)
        speculative = self.relevant(self.kp(3, topic=4, score=999999), 4)
        requests = ranked_requests(self.ranked(speculative, review))
        self.assertEqual([r['knowledgePoint'] for r in requests], [1, 3])
        self.jobs.accept(self.ranked(speculative, review))
        with patch('inventory_jobs.InventoryJobs._run_pipeline') as run:
            run.return_value.returncode = 1
            self.jobs.run_one()
        self.assertEqual(Path(run.call_args.args[0][3]), self.path_for(1))

    def test_direct_lesson_precedes_earlier_prerequisite_with_unfinished_draft(self):
        prerequisite = self.relevant(self.kp(3, topic=4, score=999999), 2, topic_layer=0)
        self.jobs.accept(self.ranked(prerequisite))
        draft = self.path_for(3)
        save(draft.with_suffix('.pipeline') / '1/job.json', {'stage': 'validate'})
        self.jobs.finish(draft, {'state': 'running', 'attempts': 2})
        direct = self.relevant(self.kp(1, topic=2, score=1), 1, topic_layer=38)
        self.jobs.accept(self.ranked(prerequisite, direct))
        with patch('inventory_jobs.InventoryJobs._run_pipeline') as run:
            run.return_value.returncode = 1
            self.jobs.run_one()
        self.assertEqual(Path(run.call_args.args[0][3]), self.path_for(1))
        preserved = json.loads(draft.read_text())
        self.assertEqual(preserved['cycle'], 1)
        self.assertEqual(preserved['attempts'], 2)

    def test_direct_review_precedes_prerequisite_lesson_in_both_lanes(self):
        for lane in ('build', 'refill'):
            with self.subTest(lane=lane):
                script = 'generators/aa/hash/main.py' if lane == 'refill' else None
                direct = self.relevant(self.kp(1, topic=2, script=script,
                                               purpose='review-shortage', score=1), 1, topic_layer=38)
                prerequisite = self.relevant(self.kp(3, topic=4, script=script, score=999999),
                                              2, topic_layer=0)
                ranked = self.ranked(prerequisite, direct)
                self.assertEqual(ranked_requests(ranked)[0]['knowledgePoint'], 1)
                self.jobs.accept(ranked)
                with patch('inventory_jobs.InventoryJobs._run_pipeline') as run:
                    run.return_value.returncode = 1
                    self.assertTrue(self.jobs.run_one(lane))
                selected = json.loads(Path(run.call_args.args[0][3]).read_text())
                self.assertEqual(selected['request']['knowledgePoint'], 1)
                self.assertEqual(selected['request']['purpose'], 'review-shortage')

    def test_gate_blocks_outside_builds_but_keeps_automatic_refills(self):
        selected = self.relevant(self.kp(1, script='generators/aa/hash/main.py'), 1)
        selected['inventory']['available'] = {'easy': 5, 'moderate': 5, 'hard': 4}
        selected['refill_deficits'] = {'easy': 0, 'moderate': 0, 'hard': 1}
        # Immediate outside agent work still waits, but existing packages refill.
        outside_build = self.relevant(self.kp(3, topic=4), 0)
        outside_refill = self.relevant(self.kp(5, topic=6, script='generators/bb/hash/main.py'), 0)
        outside_migration = self.relevant(self.kp(7, topic=8, script='generate/legacy.py'), 0)
        closed = self.gated(self.ranked(selected, outside_build, outside_refill, outside_migration))
        requests = ranked_requests(closed)
        self.assertEqual({(r['knowledgePoint'], r['jobKind'], r['difficulty']) for r in requests},
                         {(1, 'refill', 'hard'), (5, 'refill', 'easy'),
                          (5, 'refill', 'moderate'), (5, 'refill', 'hard')})
        self.jobs.accept(closed)
        self.assertFalse(self.jobs.run_one('build'))
        with patch('inventory_jobs.InventoryJobs._run_pipeline') as run:
            run.return_value.returncode = 1
            self.assertTrue(self.jobs.run_one('refill'))
        request = json.loads(Path(run.call_args.args[0][3]).read_text())['request']
        self.assertEqual(request['knowledgePoint'], 5)
        self.assertEqual(request['jobKind'], 'refill')
        cursor = json.loads((self.jobs.directory / 'cursor.json').read_text())
        self.assertEqual(cursor['selection_gate'], closed['selection_gate'])
        selected['inventory']['available']['hard'] = 5
        selected['refill_deficits']['hard'] = 0
        opened = self.gated(self.ranked(selected, outside_build, outside_refill),
                            opened=True, understocked=())
        requests = ranked_requests(opened)
        self.assertEqual({r['knowledgePoint'] for r in requests}, {3, 5})
        self.assertEqual({r['jobKind'] for r in requests}, {'build', 'refill'})

    def test_rejected_selected_build_does_not_open_gate_for_outside_work(self):
        selected = self.relevant(self.kp(1), 1)
        outside = self.relevant(self.kp(3, topic=4), 2)
        closed = self.gated(self.ranked(selected, outside), missing=(1,))
        self.jobs.accept(closed)
        self.jobs.finish(self.path_for(1), {'state': 'rejected'})
        self.jobs.accept(closed)
        self.assertFalse(self.jobs.run_one('build'))
        self.assertEqual({r['request']['knowledgePoint'] for r in self.records()}, {1})

    def test_closed_gate_preserves_shared_selected_kp_despite_other_topic_context(self):
        shared = self.relevant(self.kp(1, topic=999), 2)
        closed = self.gated(self.ranked(shared), missing=(1,))
        self.assertEqual([r['knowledgePoint'] for r in ranked_requests(closed)], [1])

    def test_gate_withdraws_outside_draft_then_resumes_saved_cycle_and_inputs(self):
        selected = self.relevant(self.kp(1), 1)
        outside = self.relevant(self.kp(3, topic=4), 2)
        self.jobs.accept(self.ranked(selected, outside))
        draft = self.path_for(3)
        state_file = draft.with_suffix('.pipeline') / '1/job.json'
        save(state_file, {'stage': 'validate'})
        before = json.loads(draft.read_text())
        self.jobs.accept(self.gated(self.ranked(selected, outside), missing=(1,)))
        self.assertEqual(json.loads(draft.read_text())['state'], 'withdrawn')
        self.assertTrue(state_file.exists())
        outside['generator_script'] = 'generate/new-registration.py'
        self.jobs.accept(self.gated(self.ranked(outside), opened=True, understocked=()))
        resumed = json.loads(draft.read_text())
        self.assertEqual(resumed['state'], 'running')
        self.assertEqual(resumed['cycle'], before['cycle'])
        for field in ('stage', 'missing', 'script', 'difficulty'):
            self.assertEqual(resumed['request'][field], before['request'][field])

    def test_gate_withdraws_outside_pending_job_without_claiming_stock_is_verified(self):
        selected, outside = self.kp(1), self.kp(3, topic=4)
        self.jobs.accept(self.ranked(selected, outside))
        pending = self.path_for(3)
        self.jobs.accept(self.gated(self.ranked(selected, outside), missing=(1,)))
        self.assertEqual(json.loads(pending.read_text())['state'], 'withdrawn')

    def test_closed_gate_verifies_observed_outside_refill_stock(self):
        selected = self.kp(1)
        outside = self.kp(3, topic=4, script='generators/aa/hash/main.py')
        self.jobs.accept(self.gated(self.ranked(selected, outside), missing=(1,)))
        refill = self.path_for(3, 'refill', 'hard')
        self.jobs.finish(refill, {'state': 'awaiting-verification', 'retryAt': 999999999999})
        outside['inventory']['available']['hard'] = 5
        outside['refill_deficits']['hard'] = 0
        self.jobs.accept(self.gated(self.ranked(selected, outside), missing=(1,)))
        self.assertEqual(json.loads(refill.read_text())['state'], 'verified')

    def test_closed_gate_does_not_verify_an_uncaptured_outside_refill(self):
        selected = self.kp(1)
        outside = self.kp(3, topic=4, script='generators/aa/hash/main.py')
        self.jobs.accept(self.gated(self.ranked(selected, outside), missing=(1,)))
        refill = self.path_for(3, 'refill', 'hard')
        self.jobs.finish(refill, {'state': 'awaiting-verification', 'retryAt': 999999999999})
        self.jobs.accept(self.gated(self.ranked(selected), missing=(1,)))
        self.assertEqual(json.loads(refill.read_text())['state'], 'withdrawn')

    def test_closed_gate_still_resolves_an_uncertain_outside_publication(self):
        selected = self.relevant(self.kp(1), 1)
        outside = self.relevant(self.kp(3, topic=4), 2)
        self.jobs.accept(self.ranked(selected, outside))
        publication = self.path_for(3)
        directory = publication.with_suffix('.pipeline') / '1'
        save(directory / 'job.json', {'stage': 'validate'})
        save(directory / 'publication/request.json', {'request_id': 'exact-intent'})
        self.jobs.accept(self.gated(self.ranked(selected, outside), missing=(1,)))
        kept = json.loads(publication.read_text())
        self.assertEqual(kept['state'], 'running')
        self.assertTrue(kept['recoveryOnly'])
        with patch('inventory_jobs.InventoryJobs._run_pipeline') as run:
            run.return_value.returncode = 1
            self.jobs.run_one()
        self.assertEqual(Path(run.call_args.args[0][3]), publication)
        self.assertEqual(json.loads((directory / 'publication/request.json').read_text()),
                         {'request_id': 'exact-intent'})

    def test_mixed_pre_score_running_job_waits_behind_refreshed_priority(self):
        self.accept()
        legacy = self.path_for(1)
        self.jobs.finish(legacy, {'state': 'running', 'attempts': 2})
        kp = self.relevant(self.kp(3, purpose='advance-build'), 4)
        request = ranked_requests(self.ranked(kp))[0]
        current = self.jobs.directory / 'refreshed.json'
        save(current, {'key': 'refreshed', 'request': request, 'state': 'pending', 'cycle': 1})
        with patch('inventory_jobs.InventoryJobs._run_pipeline') as run:
            run.return_value.returncode = 1
            self.jobs.run_one()
        self.assertEqual(Path(run.call_args.args[0][3]), current)
        self.assertEqual(json.loads(legacy.read_text())['attempts'], 2)

    def test_refills_use_reason_context_and_baseline_for_routine_work(self):
        kp = self.relevant(self.kp(script='generators/aa/hash/main.py'), 0,
                           baseline_relevance_tier=1, topic_layer=50)
        kp['priority_reasons'] = [
            {**kp['priority_reasons'][0], 'purpose': 'lesson-shortage', 'relevance_tier': 4,
             'generated_band': 'hard', 'score': 999999},
            {**kp['priority_reasons'][0], 'purpose': 'review-shortage', 'relevance_tier': 1,
             'generated_band': 'hard', 'topic_entity': 7, 'topic_layer': 3, 'score': 1},
        ]
        by_band = {r['difficulty']: r for r in ranked_requests(self.ranked(kp))}
        self.assertEqual(by_band['hard']['purpose'], 'review-shortage')
        self.assertEqual(by_band['hard']['topic'], 7)
        self.assertEqual(by_band['hard']['topic_layer'], 3)
        self.assertEqual(by_band['hard']['relevance_tier'], 1)
        self.assertEqual(by_band['easy']['purpose'], 'routine-replenishment')
        self.assertEqual(by_band['easy']['relevance_tier'], 1)

    def test_finder_and_worker_share_the_comparator(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'generate/scripts'))
        from find_candidates import ranking_key
        kps = [self.relevant(self.kp(1, topic=2), 1, topic_layer=8),
               self.relevant(self.kp(3, topic=4, score=99999), 1, topic_layer=9),
               self.relevant(self.kp(5, topic=6, purpose='review-shortage'), 1),
               self.relevant(self.kp(7, topic=8), 4)]
        expected = [kp['db/id'] for kp in sorted(kps, key=ranking_key)]
        self.assertEqual([r['knowledgePoint'] for r in ranked_requests(self.ranked(*kps))], expected)

    def test_assessment_age_and_waiting_tiebreakers_match_finder(self):
        common = dict(score=41500, purpose='assessment-shortage', topic=2, knowledgePoint=1)
        first = {**common, 'first_studied_at': '2025-01-01T00:00:00Z'}
        second = {**common, 'first_studied_at': '2025-02-01T00:00:00Z', 'waiting_since': '2024-01-01T00:00:00Z'}
        self.assertLess(priority_key(first), priority_key(second))
        first['purpose'] = second['purpose'] = 'lesson-shortage'
        self.assertGreater(priority_key(first), priority_key(second))

    def test_usable_legacy_registration_requires_one_migration_build(self):
        requests = ranked_requests(self.ranked(self.kp(script='generate/legacy.py')))
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0]['jobKind'], 'build')
        self.assertEqual(requests[0]['stage'], 'migrate-generator')

    def test_hashed_packages_outside_urgency_groups_are_replenished(self):
        requests = ranked_requests(self.ranked(self.kp(script='generators/aa/hash/main.py', urgency=0, score=65000)))
        self.assertEqual({request['difficulty'] for request in requests}, {'easy', 'moderate', 'hard'})
        self.assertEqual({request['jobKind'] for request in requests}, {'refill'})
        self.assertEqual({request['purpose'] for request in requests}, {'routine-replenishment'})
        self.assertEqual(max(request['score'] for request in requests), 5000)
        self.assertEqual(ranked_requests(self.ranked(self.kp(urgency=0, score=0))), [])

    def test_refill_variety_reason_only_applies_to_useful_band(self):
        kp = self.kp(script='generators/aa/hash/main.py', score=31500, purpose='hard-variety')
        kp['priority_reasons'] = [{'purpose': 'hard-variety', 'score': 31500, 'shortage': 1, 'generated_band': 'hard'}]
        by_band = {r['difficulty']: r for r in ranked_requests(self.ranked(kp))}
        self.assertEqual(by_band['hard']['score'], 31500)
        self.assertEqual(by_band['moderate']['purpose'], 'routine-replenishment')

    def test_arbitrary_running_flag_does_not_override_current_scoring(self):
        self.jobs.accept(self.ranked(self.kp(), self.kp(3, score=65000)))
        low_path = self.path_for(1)
        self.jobs.finish(low_path, {'state': 'running', 'attempts': 3})
        with patch('inventory_jobs.InventoryJobs._run_pipeline') as run:
            run.return_value.returncode = 1
            self.assertTrue(self.jobs.run_one())
        self.assertEqual(Path(run.call_args.args[0][3]), self.path_for(3))
        self.assertEqual(json.loads(low_path.read_text())['attempts'], 3)

    def test_unfinished_draft_preserves_inputs_without_overriding_priority(self):
        self.jobs.accept(self.ranked(self.kp()))
        draft = self.path_for(1)
        before = json.loads(draft.read_text())
        save(draft.with_suffix('.pipeline') / '1/job.json', {'stage': 'validate'})
        self.jobs.finish(draft, {'state': 'running', 'attempts': 2})
        current = self.kp(script='generate/new-registration.py')
        self.jobs.accept(self.ranked(current, self.kp(3, score=99999)))
        preserved = json.loads(draft.read_text())
        self.assertEqual(preserved['cycle'], 1)
        for field in ('stage', 'missing', 'script', 'difficulty'):
            self.assertEqual(preserved['request'][field], before['request'][field])
        with patch('inventory_jobs.InventoryJobs._run_pipeline') as run:
            run.return_value.returncode = 1
            self.jobs.run_one()
        self.assertEqual(Path(run.call_args.args[0][3]), self.path_for(3))

    def test_disappearing_draft_withdraws_and_resumes_same_cycle_on_new_demand(self):
        self.jobs.accept(self.ranked(self.kp()))
        draft = self.path_for(1)
        state_file = draft.with_suffix('.pipeline') / '1/job.json'
        save(state_file, {'stage': 'validate'})
        before = json.loads(draft.read_text())
        self.jobs.accept(self.ranked())
        self.assertEqual(json.loads(draft.read_text())['state'], 'withdrawn')
        self.assertFalse(self.jobs.run_one())
        self.jobs.accept(self.ranked(self.kp(script='generate/new-registration.py')))
        resumed = json.loads(draft.read_text())
        self.assertEqual(resumed['state'], 'running')
        self.assertEqual(resumed['cycle'], before['cycle'])
        self.assertTrue(state_file.exists())
        for field in ('stage', 'missing', 'script', 'difficulty'):
            self.assertEqual(resumed['request'][field], before['request'][field])

    def test_saved_publication_intent_recovers_before_priority_but_finished_review_does_not(self):
        self.jobs.accept(self.ranked(self.kp(), self.kp(3, score=99999)))
        pending = self.path_for(1)
        directory = pending.with_suffix('.pipeline') / '1'
        save(directory / 'job.json', {'stage': 'validate'})
        save(directory / 'publication/request.json', {'request_id': 'exact-intent'})
        with patch('inventory_jobs.InventoryJobs._run_pipeline') as run:
            run.return_value.returncode = 1
            self.jobs.run_one()
        self.assertEqual(Path(run.call_args.args[0][3]), pending)
        self.assertEqual(json.loads((directory / 'publication/request.json').read_text()),
                         {'request_id': 'exact-intent'})
        save(directory / 'job.json', {'stage': 'validate', 'review_after_publication': True})
        self.jobs.finish(pending, {'retryAt': 0})
        with patch('inventory_jobs.InventoryJobs._run_pipeline') as run:
            run.return_value.returncode = 1
            self.jobs.run_one()
        self.assertEqual(Path(run.call_args.args[0][3]), self.path_for(3))

    def test_migration_preserves_active_workspace_inputs_and_recovers_before_new_build(self):
        self.accept()
        path = self.path_for(1)
        save(path.with_suffix('.pipeline') / '1/job.json', {'stage': 'push'})
        self.jobs.finish(path, {'state': 'running', 'attempts': 2})
        self.jobs.accept(self.ranked(self.kp(), self.kp(3, score=65000)))
        migrated = json.loads(path.read_text())
        self.assertEqual(migrated['request']['difficulty'], 'hard')
        self.assertEqual(migrated['cycle'], 1)
        with patch('inventory_jobs.InventoryJobs._run_pipeline') as run:
            run.return_value.returncode = 1
            self.jobs.run_one()
        self.assertEqual(Path(run.call_args.args[0][3]), path)
        self.assertEqual(json.loads(path.read_text())['attempts'], 2)

    def test_migration_prefers_publication_identity_over_a_second_unfinished_draft(self):
        self.accept(jobs=[self.request, {**self.request, 'difficulty': 'easy'}])
        paths = sorted(p for p in self.jobs.directory.glob('*.json') if p.name != 'cursor.json')
        draft, publication = paths
        save(draft.with_suffix('.pipeline') / '1/job.json', {'stage': 'validate'})
        save(publication.with_suffix('.pipeline') / '1/job.json', {'stage': 'push'})
        before = json.loads(publication.read_text())['request']
        self.jobs.accept(self.ranked(self.kp()))
        kept = json.loads(publication.read_text())
        self.assertEqual(kept['state'], 'running')
        self.assertFalse(kept['recoveryOnly'])
        self.assertEqual(kept['request']['difficulty'], before['difficulty'])
        self.assertEqual(json.loads(draft.read_text())['state'], 'withdrawn')

    def test_disappearing_trigger_keeps_pending_publication_recoverable(self):
        self.jobs.accept(self.ranked(self.kp()))
        path = self.path_for(1)
        save(path.with_suffix('.pipeline') / '1/job.json', {'stage': 'push'})
        self.jobs.accept(self.ranked())
        job = json.loads(path.read_text())
        self.assertEqual(job['state'], 'running')
        self.assertTrue(job['recoveryOnly'])

    def test_lanes_run_independently_and_child_inherits_both_locks(self):
        self.jobs.accept(self.ranked(self.kp(), self.kp(3, script='generators/aa/hash/main.py')))
        lanes = []
        def execute(command, **kwargs):
            job = json.loads(Path(command[3]).read_text())
            lanes.append(job['request']['jobKind'])
            self.assertEqual(len(kwargs['pass_fds']), 2)
            self.assertEqual(json.loads(kwargs['env']['COURSE_ACADEMY_GENERATOR_LOCK_FDS']), list(kwargs['pass_fds']))
            if len(lanes) == 1:
                self.assertTrue(self.jobs.run_one(lane='refill'))
            return subprocess.CompletedProcess(command, 1)
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=execute):
            self.assertTrue(self.jobs.run_one(lane='build'))
        self.assertEqual(lanes, ['build', 'refill'])

    def test_three_build_slots_claim_distinct_highest_priority_kps_and_bound_restarts(self):
        self.jobs.environment['COURSE_ACADEMY_GENERATOR_BUILD_WORKERS'] = '3'
        self.jobs.accept(self.ranked(*(self.kp(entity, score=70000 - entity) for entity in range(1, 6))))
        claimed, errors = [], []
        entered, release = threading.Event(), threading.Event()
        guard = threading.Lock()
        def execute(command, **kwargs):
            request = json.loads(Path(command[3]).read_text())['request']
            with guard:
                claimed.append(request['knowledgePoint'])
                if len(claimed) == 3:
                    entered.set()
            if not release.wait(5):
                errors.append('Timed out waiting for concurrent claims')
            return subprocess.CompletedProcess(command, 0)
        restarted = InventoryJobs(self.directory, self.jobs.directory, 'learner', self.jobs.environment)
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=execute), ThreadPoolExecutor(max_workers=3) as pool:
            futures = [pool.submit(self.jobs.run_one, 'build', slot) for slot in range(3)]
            try:
                self.assertTrue(entered.wait(3), 'Three builders did not run concurrently')
                self.assertEqual(set(claimed), {1, 2, 3})
                for slot in range(3):
                    self.assertFalse(restarted.run_one('build', slot))
                self.assertEqual(len([j for j in self.records() if j['state'] == 'running']), 3)
            finally:
                release.set()
            self.assertTrue(all(future.result(timeout=3) for future in futures))
        self.assertEqual(errors, [])
        self.assertEqual(len([j for j in self.records() if j['state'] == 'pending']), 2)

    def test_build_slot_count_is_configurable_and_refill_remains_single(self):
        self.assertEqual(build_worker_count({}), 3)
        self.assertEqual(build_worker_count({'COURSE_ACADEMY_GENERATOR_BUILD_WORKERS': '1'}), 1)
        for value in ('0', '-1', 'nope', '1.5'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                build_worker_count({'COURSE_ACADEMY_GENERATOR_BUILD_WORKERS': value})
        self.jobs.environment['COURSE_ACADEMY_GENERATOR_BUILD_WORKERS'] = '1'
        for lane, slot in (('build', 1), ('build', -1), ('refill', 1), ('build', True)):
            with self.subTest(lane=lane, slot=slot), self.assertRaises(ValueError):
                self.jobs.run_one(lane, slot)

    def admit_review_backlog(self, *lessons):
        packaged = self.relevant(self.kp(90, topic=900, script='generators/aa/hash/main.py',
                                         purpose='advance-build'), 1)
        inventory = self.ranked(*lessons, packaged)
        self.jobs.accept(inventory)
        self.jobs.finish(self.path_for(90, 'refill', 'hard'),
                         {'state': 'repair-needed', 'completedAt': 10})
        self.jobs.accept(inventory)
        return self.path_for(90, 'build')

    def test_review_capacity_uses_existing_slots_and_keeps_one_normal_builder(self):
        self.assertEqual(review_worker_count({}), 1)
        self.assertEqual(review_worker_count({'COURSE_ACADEMY_GENERATOR_BUILD_WORKERS': '6'}), 1)
        self.assertEqual(review_worker_count({'COURSE_ACADEMY_GENERATOR_BUILD_WORKERS': '1'}), 0)
        self.assertEqual(review_worker_count({'COURSE_ACADEMY_GENERATOR_REVIEW_WORKERS': '0'}), 0)
        self.assertEqual(review_worker_count({'COURSE_ACADEMY_GENERATOR_REVIEW_WORKERS': '2'}), 2)
        for value in ('-1', '3', 'nope', '1.5'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                review_worker_count({'COURSE_ACADEMY_GENERATOR_REVIEW_WORKERS': value})
        with self.assertRaises(ValueError):
            review_worker_count({'COURSE_ACADEMY_GENERATOR_BUILD_WORKERS': '1',
                                 'COURSE_ACADEMY_GENERATOR_REVIEW_WORKERS': '1'})

    def test_six_builders_include_one_approval_review_without_displacing_five_shortages(self):
        self.jobs.environment['COURSE_ACADEMY_GENERATOR_BUILD_WORKERS'] = '6'
        self.admit_review_backlog(*(self.relevant(self.kp(i, topic=i), 1) for i in range(1, 9)))
        claimed, errors = [], []
        entered, release = threading.Event(), threading.Event()
        guard = threading.Lock()
        def execute(command, **kwargs):
            request = json.loads(Path(command[3]).read_text())['request']
            with guard:
                claimed.append(request['knowledgePoint'])
                if len(claimed) == 6:
                    entered.set()
            if not release.wait(5):
                errors.append('Timed out waiting for six concurrent claims')
            return subprocess.CompletedProcess(command, 0)
        restarted = InventoryJobs(self.directory, self.jobs.directory, 'learner', self.jobs.environment)
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=execute), ThreadPoolExecutor(max_workers=6) as pool:
            futures = [pool.submit(self.jobs.run_one, 'build', slot) for slot in range(6)]
            try:
                self.assertTrue(entered.wait(3), 'Six workers did not claim their jobs')
                self.assertEqual(set(claimed), {1, 2, 3, 4, 5, 90})
                for slot in range(6):
                    self.assertFalse(restarted.run_one('build', slot))
            finally:
                release.set()
            self.assertTrue(all(f.result(timeout=3) for f in futures))
        self.assertEqual(errors, [])

    def test_immediate_deficit_and_publication_recovery_precede_review_reservation(self):
        self.admit_review_backlog(self.relevant(self.kp(1, topic=1), 0),
                                 self.relevant(self.kp(2, topic=2), 1))
        publication = self.path_for(2, 'build')
        directory = publication.with_suffix('.pipeline') / '1'
        save(directory / 'job.json', {'stage': 'push'})
        save(directory / 'publication/request.json', {'request_id': 'exact-intent'})
        claimed = []
        def execute(command, **kwargs):
            claimed.append(json.loads(Path(command[3]).read_text())['request']['knowledgePoint'])
            return subprocess.CompletedProcess(command, 0)
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=execute):
            self.assertTrue(self.jobs.run_one('build', 2))
            self.assertTrue(self.jobs.run_one('build', 2))
            self.assertTrue(self.jobs.run_one('build', 2))
        self.assertEqual(claimed, [2, 1, 90])
        self.assertEqual(json.loads((directory / 'publication/request.json').read_text()),
                         {'request_id': 'exact-intent'})

    def test_review_slot_falls_back_when_review_is_locked_and_never_rearms_blocked_work(self):
        review = self.admit_review_backlog(self.relevant(self.kp(1, topic=1), 1),
                                          self.relevant(self.kp(2, topic=2), 1))
        claimed = []
        def execute(command, **kwargs):
            claimed.append(json.loads(Path(command[3]).read_text())['request']['knowledgePoint'])
            return subprocess.CompletedProcess(command, 0)
        with (self.jobs.directory / 'kp-90.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=execute):
                self.assertTrue(self.jobs.run_one('build', 2))
        self.jobs.finish(review, {'state': 'blocked', 'outcome': {'reason': 'unresolved source defect'}})
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=execute):
            self.assertTrue(self.jobs.run_one('build', 2))
        self.assertEqual(claimed, [1, 2])
        self.assertEqual(json.loads(review.read_text())['state'], 'blocked')

    def test_review_reservation_can_be_disabled_and_single_builder_keeps_normal_order(self):
        self.admit_review_backlog(self.relevant(self.kp(1, topic=1), 1),
                                 self.relevant(self.kp(2, topic=2), 1))
        claimed = []
        def execute(command, **kwargs):
            claimed.append(json.loads(Path(command[3]).read_text())['request']['knowledgePoint'])
            return subprocess.CompletedProcess(command, 0)
        self.jobs.environment['COURSE_ACADEMY_GENERATOR_REVIEW_WORKERS'] = '0'
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=execute):
            self.assertTrue(self.jobs.run_one('build', 2))
            self.jobs.environment.pop('COURSE_ACADEMY_GENERATOR_REVIEW_WORKERS')
            self.jobs.environment['COURSE_ACADEMY_GENERATOR_BUILD_WORKERS'] = '1'
            self.assertTrue(self.jobs.run_one('build', 0))
        self.assertEqual(claimed, [1, 2])

    def test_routine_review_selects_observed_band_without_dropping_other_reserves(self):
        kp = self.relevant(self.kp(script='generators/aa/hash/main.py', purpose='advance-build'), 1)
        kp['inventory']['supported_difficulties'] = ['moderate']
        inventory = self.ranked(kp)
        self.jobs.accept(inventory)
        for band in ('easy', 'moderate', 'hard'):
            self.jobs.finish(self.path_for(1, 'refill', band), {'state': 'repair-needed', 'completedAt': 10})
        self.jobs.accept(inventory)
        build = self.path_for(1, 'build')
        request = json.loads(build.read_text())['request']
        self.assertEqual(request['difficulty'], 'moderate')
        self.assertEqual(request['observed_difficulties'], ['moderate'])
        self.assertEqual({job['request']['difficulty'] for job in self.records()
                          if job['request']['jobKind'] == 'refill'}, {'easy', 'moderate', 'hard'})
        # Rejecting a band is definitive for this variant even if inventory
        # continues to report observations of that band. Other bands can run.
        def fail(command, **kwargs):
            build.with_suffix('.result').write_text(json.dumps({'outcome': 'unsupported'}))
            return subprocess.CompletedProcess(command, 1)
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=fail):
            self.assertTrue(self.jobs.run_one('build', 2))
        self.jobs.accept(inventory)
        self.assertNotEqual(json.loads(build.read_text())['request']['difficulty'], 'moderate')
        self.assertEqual(len(json.loads(build.read_text())['rejectedVariants']), 1)

    def test_review_slot_prefers_observed_reserves_then_falls_back_to_unobserved(self):
        kps = [self.relevant(self.kp(entity, topic=entity, script=f'generators/{entity}/main.py',
                                    purpose='advance-build'), 1) for entity in (1, 2)]
        kps[0]['inventory']['supported_difficulties'] = ['easy']
        kps[1]['inventory']['supported_difficulties'] = ['hard']
        inventory = self.ranked(*kps)
        self.jobs.accept(inventory)
        for entity in (1, 2):
            self.jobs.finish(self.path_for(entity, 'refill', 'hard'), {'state': 'repair-needed', 'completedAt': 10})
        self.jobs.accept(inventory)
        claimed = []
        def execute(command, **kwargs):
            claimed.append(json.loads(Path(command[3]).read_text())['request']['knowledgePoint'])
            return subprocess.CompletedProcess(command, 0)
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=execute):
            self.assertTrue(self.jobs.run_one('build', 2))
            self.assertTrue(self.jobs.run_one('build', 2))
        self.assertEqual(claimed, [2, 1])

    def test_review_prefers_eligible_source_bands_and_ignores_mismatched_capture(self):
        for mismatch in (None, 'kp_id', 'lineage', 'registered_generator', 'material'):
            with self.subTest(mismatch=mismatch), tempfile.TemporaryDirectory() as directory:
                self.jobs = InventoryJobs(self.directory, Path(directory), 'learner')
                kp = self.relevant(self.kp(script='generators/aa/hash/main.py', purpose='advance-build'), 1)
                kp['inventory']['supported_difficulties'] = ['hard']
                inventory = self.ranked(kp)
                self.jobs.accept(inventory)
                source = {'kp_id': 1, 'lineage': 'same', 'basis': 9,
                          'registered_generator': {':question-generator/script': kp['generator_script']},
                          'material': {'source_eligibility': {'policy_version': 1}},
                          'available_difficulties': ['moderate']}
                if mismatch:
                    source[mismatch] = {'kp_id': 99, 'lineage': 'different', 'registered_generator': {},
                                        'material': {}}[mismatch]
                for band in ('moderate', 'hard'):
                    refill = self.path_for(1, 'refill', band)
                    self.jobs.finish(refill, {'state': 'repair-needed', 'completedAt': 10})
                    save(refill.with_suffix('.pipeline') / '1/source/source.json', source)
                self.jobs.accept(inventory)
                request = json.loads(self.path_for(1, 'build').read_text())['request']
                self.assertEqual(request['difficulty'], 'hard' if mismatch else 'moderate')
                self.assertEqual(request['difficulty_evidence'], 'inventory' if mismatch else 'captured-eligible-source')

    def test_shortage_and_variety_reviews_precede_observed_routine_band(self):
        for purpose in ('lesson-shortage', 'hard-variety'):
            with self.subTest(purpose=purpose), tempfile.TemporaryDirectory() as directory:
                self.jobs = InventoryJobs(self.directory, Path(directory), 'learner')
                kp = self.relevant(self.kp(script='generators/aa/hash/main.py', purpose=purpose), 1)
                kp['inventory']['supported_difficulties'] = ['moderate']
                kp['priority_reasons'][0]['generated_band'] = 'hard'
                inventory = self.ranked(kp)
                self.jobs.accept(inventory)
                for band in ('moderate', 'hard'):
                    self.jobs.finish(self.path_for(1, 'refill', band), {'state': 'repair-needed', 'completedAt': 10})
                self.jobs.accept(inventory)
                request = json.loads(self.path_for(1, 'build').read_text())['request']
                self.assertEqual(request['difficulty'], 'hard')
                self.assertEqual(request['purpose'], purpose)

    def test_shared_kp_lock_prevents_cross_lane_publication(self):
        self.jobs.accept(self.ranked(self.kp(script='generators/aa/hash/main.py')))
        path = self.path_for(1, 'refill', 'hard')
        self.jobs.finish(path, {'state': 'repair-needed', 'completedAt': 10})
        self.jobs.accept(self.ranked(self.kp(script='generators/aa/hash/main.py')))
        with patch('inventory_jobs.InventoryJobs._run_pipeline') as run:
            def execute(command, **kwargs):
                self.assertFalse(self.jobs.run_one(lane='refill'))
                return subprocess.CompletedProcess(command, 1)
            run.side_effect = execute
            self.assertTrue(self.jobs.run_one(lane='build'))
        self.assertEqual(run.call_count, 1)

    def test_refill_missing_approval_becomes_explicit_band_review_and_resumes_after_review(self):
        ranked = self.ranked(self.kp(script='generators/aa/hash/main.py'))
        self.jobs.accept(ranked)
        path = self.path_for(1, 'refill', 'hard')
        self.jobs.finish(path, {'state': 'repair-needed', 'completedAt': 10})
        self.jobs.accept(ranked)
        build = self.path_for(1, 'build')
        self.assertEqual(json.loads(build.read_text())['request']['difficulty'], 'hard')
        self.jobs.finish(build, {'state': 'awaiting-verification', 'completedAt': 20,
                                 'outcome': {'outcome': 'generated'}})
        self.jobs.accept(ranked)
        repaired = json.loads(path.read_text())
        self.assertEqual(repaired['state'], 'pending')
        self.assertEqual(repaired['cycle'], 2)
        self.assertEqual(json.loads(build.read_text())['state'], 'verified')

    def test_closed_gate_defers_outside_refill_review_but_keeps_selected_reviews(self):
        selected = self.kp(1, script='generators/aa/hash/main.py')
        outside = self.kp(3, topic=4, script='generators/bb/hash/main.py')
        ranked = self.gated(self.ranked(selected, outside))
        self.jobs.accept(ranked)
        for kp in (1, 3):
            self.jobs.finish(self.path_for(kp, 'refill', 'hard'),
                             {'state': 'repair-needed', 'completedAt': 10})
        self.jobs.accept(ranked)
        builds = [job for job in self.records() if job['request']['jobKind'] == 'build']
        self.assertEqual(len(builds), 1)
        self.assertEqual(builds[0]['request']['knowledgePoint'], 1)
        self.assertEqual(builds[0]['request']['stage'], 'review-generator')
        self.assertEqual(json.loads(self.path_for(3, 'refill', 'hard').read_text())['state'], 'repair-needed')
        self.jobs.accept(self.gated(self.ranked(selected, outside), opened=True, understocked=()))
        outside_build = json.loads(self.path_for(3, 'build').read_text())
        self.assertEqual(outside_build['state'], 'pending')
        self.assertEqual(outside_build['request']['stage'], 'review-generator')

    def test_closed_gate_withdraws_existing_outside_review_and_resumes_its_draft(self):
        outside = self.kp(3, topic=4, script='generators/bb/hash/main.py')
        ranked = self.ranked(outside)
        self.jobs.accept(ranked)
        self.jobs.finish(self.path_for(3, 'refill', 'hard'),
                         {'state': 'repair-needed', 'completedAt': 10})
        self.jobs.accept(ranked)
        build = self.path_for(3, 'build')
        save(build.with_suffix('.pipeline') / '1/job.json', {'stage': 'validate'})
        self.jobs.accept(self.gated(ranked))
        self.assertEqual(json.loads(build.read_text())['state'], 'withdrawn')
        self.assertFalse(self.jobs.run_one('build'))
        self.jobs.accept(self.gated(ranked, opened=True, understocked=()))
        resumed = json.loads(build.read_text())
        self.assertEqual(resumed['state'], 'running')
        self.assertEqual(resumed['cycle'], 1)

    def test_closed_gate_reopens_outside_refill_after_already_successful_review(self):
        outside = self.kp(3, topic=4, script='generators/bb/hash/main.py')
        ranked = self.ranked(outside)
        self.jobs.accept(ranked)
        refill = self.path_for(3, 'refill', 'hard')
        self.jobs.finish(refill, {'state': 'repair-needed', 'completedAt': 10})
        self.jobs.accept(ranked)
        build = self.path_for(3, 'build')
        self.jobs.finish(build, {'state': 'awaiting-verification', 'completedAt': 20,
                                'outcome': {'outcome': 'generated'}})
        self.jobs.accept(self.gated(ranked))
        reopened = json.loads(refill.read_text())
        self.assertEqual(reopened['state'], 'pending')
        self.assertEqual(reopened['cycle'], 2)
        self.assertFalse(self.jobs.run_one('build'))

    def test_rejected_band_does_not_retry_unchanged_or_block_another_band(self):
        ranked = self.ranked(self.kp(script='generators/aa/hash/main.py'))
        self.jobs.accept(ranked)
        for band in ('hard', 'moderate'):
            self.jobs.finish(self.path_for(1, 'refill', band), {'state': 'repair-needed', 'completedAt': 10})
        self.jobs.accept(ranked)
        build = self.path_for(1, 'build')
        first_band = json.loads(build.read_text())['request']['difficulty']
        def fail(command, **kwargs):
            build.with_suffix('.result').write_text(json.dumps({'outcome': 'unsupported'}))
            return subprocess.CompletedProcess(command, 1)
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=fail):
            self.jobs.run_one()
        self.jobs.accept(ranked)
        self.assertNotEqual(json.loads(build.read_text())['request']['difficulty'], first_band)
        with patch('inventory_jobs.InventoryJobs._run_pipeline', side_effect=fail):
            self.jobs.run_one()
        self.jobs.accept(ranked)
        self.assertFalse(self.jobs.run_one())
        self.assertEqual(len(json.loads(build.read_text())['rejectedVariants']), 2)

    def test_successful_band_review_cannot_be_mistaken_for_next_bands_approval(self):
        ranked = self.ranked(self.kp(script='generators/aa/hash/main.py'))
        self.jobs.accept(ranked)
        for band in ('hard', 'moderate'):
            self.jobs.finish(self.path_for(1, 'refill', band), {'state': 'repair-needed', 'completedAt': 10})
        self.jobs.accept(ranked)
        build = self.path_for(1, 'build')
        first_band = json.loads(build.read_text())['request']['difficulty']
        self.jobs.finish(build, {'state': 'awaiting-verification', 'completedAt': 20,
                                 'retryAt': 999999999999, 'outcome': {'outcome': 'generated'}})
        self.jobs.accept(ranked)
        next_review = json.loads(build.read_text())
        self.assertNotEqual(next_review['request']['difficulty'], first_band)
        self.assertEqual(next_review['state'], 'pending')
        self.assertEqual(next_review['outcome'], {})
        self.jobs.accept(ranked)
        waiting = self.path_for(1, 'refill', next_review['request']['difficulty'])
        self.assertEqual(json.loads(waiting.read_text())['state'], 'repair-needed')


if __name__ == '__main__': unittest.main()
