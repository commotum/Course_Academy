import copy
from contextlib import contextmanager
import json
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from study_outbox import StudyOutbox
from serve_graph_explorer import save_json


class Grader:
    def __init__(self):
        self.calls = []
        self.reference = [1, 2, 3]

    def request(self, body):
        self.calls.append(copy.deepcopy(body))
        if body['action'] == 'study-capture':
            return {'ok': True, 'data': {'reference': copy.deepcopy(self.reference), 'basis': 1}}
        if body['action'] == 'study-read':
            return {'ok': True, 'data': {'action': body['operation']['action'], 'visibleLocal': True}}
        action = body['operation']['action']
        view = {'taskId': 4000000000000001, 'type': 'lesson', 'status': 'started',
                'step': {'itemId': 4000000000000002, 'status': 'correct' if action == 'answer' else 'started'}}
        return {'ok': True, 'data': {'view': view, 'views': {str(view['taskId']): view},
                                   'overlay': {'entities': {'4000000000000001': {}, '4000000000000002': {}}},
                                   'operation': {**body['operation'], '_queuedStudy': {'at': body['receivedAt']}}}}


class StudyOutboxTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.stop = threading.Event()
        self.grader, self.writer = Grader(), Mock()
        self.writer.request.return_value = {'ok': True, 'data': {'view': {'taskId': 100, 'step': {'itemId': 101}},
                                                        'aliases': {'4000000000000001': 100, '4000000000000002': 101}}}
        self.queue = self.make()

    def make(self):
        return StudyOutbox(self.temp.name, self.grader, self.writer, save_json, self.stop)

    def request(self, action='start', request='request-0001'):
        return self.queue.request({'action': action, 'taskId': 4000000000000001,
                                   'itemId': 4000000000000002, 'requestId': request}, 1000)

    def test_start_answer_next_and_other_reads_do_not_wait_for_writer(self):
        first = self.request()
        entered, release = threading.Event(), threading.Event()
        def blocked(body):
            entered.set()
            release.wait(3)
            return self.writer.request.return_value
        self.writer.request.side_effect = blocked
        thread = threading.Thread(target=self.queue.run_one)
        thread.start()
        try:
            self.assertTrue(entered.wait(1))
            start = time.monotonic()
            answer = self.request('answer', 'request-0002')
            self.request('continue', 'request-0003')
            activity = self.queue.overlay_view('activity-history', {'action': 'activity-history'})
            self.assertLess(time.monotonic() - start, .2)
            self.assertEqual(answer['step']['status'], 'correct')
            self.assertTrue(activity['visibleLocal'])
            self.assertEqual(self.queue.status()['pending'], 3)
            restarted = self.make()
            self.assertEqual(restarted.request({'action': 'start', 'taskId': 4000000000000001,
                                                'itemId': 4000000000000002, 'requestId': 'request-0001'}, 1000), first)
        finally:
            release.set()
            thread.join(2)

    def test_background_queue_planning_never_holds_actor_or_publishes_over_new_progress(self):
        entered, release = threading.Event(), threading.Event()
        planner = Mock()
        def slow_plan(body):
            entered.set()
            release.wait(3)
            return self.grader.request(body)
        planner.request.side_effect = slow_plan
        self.queue.planner = planner
        result = []
        thread = threading.Thread(target=lambda: result.append(self.queue.request(
            {'action': 'queue', 'background': True, 'requestId': 'background-queue-0001'}, 1000)))
        thread.start()
        try:
            self.assertTrue(entered.wait(1))
            start = time.monotonic()
            self.assertEqual(self.queue.status()['pending'], 0)
            self.assertTrue(self.queue.overlay_view('home', {'action': 'home'})['visibleLocal'])
            other = self.make()
            answer = other.request({'action': 'answer', 'taskId': 4000000000000001,
                                    'itemId': 4000000000000002, 'requestId': 'new-answer-0001'}, 1100)
            self.assertEqual(answer['step']['status'], 'correct')
            self.assertLess(time.monotonic() - start, .2)
        finally:
            release.set()
            thread.join(2)
        self.assertEqual(result, [{'_superseded': True}])
        state = self.queue.load()
        self.assertEqual([op['input']['action'] for op in state['operations']], ['answer'])
        self.assertEqual(planner.request.call_args.args[0]['overlay'], None)

    def test_background_queue_can_prepare_from_pending_overlay_without_blocking_it(self):
        self.request('answer', 'answer-before-queue-0001')
        planner = Mock(wraps=self.grader)
        self.queue.planner = planner
        view = self.queue.request({'action': 'queue', 'background': True,
                                   'requestId': 'background-pending-0001'}, 1200)
        self.assertEqual(view['saveState']['pending'], 2)
        self.assertIsNotNone(planner.request.call_args.args[0]['overlay'])
        duplicate = self.queue.request({'action': 'queue', 'background': True,
                                        'requestId': 'background-pending-0001'}, 1300)
        self.assertEqual(duplicate, view)
        self.assertEqual(planner.request.call_count, 1)

    def test_only_one_background_planner_uses_captured_state_across_instances(self):
        entered, release = threading.Event(), threading.Event()
        planner = Mock()
        def slow_plan(body):
            entered.set(); release.wait(3)
            return self.grader.request(body)
        planner.request.side_effect = slow_plan
        self.queue.planner = planner
        result = []
        thread = threading.Thread(target=lambda: result.append(self.queue.request(
            {'action': 'queue', 'background': True, 'requestId': 'exclusive-queue-0001'}, 1000)))
        thread.start()
        try:
            self.assertTrue(entered.wait(1))
            other = self.make()
            self.assertEqual(other.request({'action': 'queue', 'background': True,
                                            'requestId': 'exclusive-queue-0002'}, 1100), {'_superseded': True})
            self.assertEqual(other.status()['pending'], 0)
        finally:
            release.set(); thread.join(2)
        self.assertEqual(result[0]['saveState']['pending'], 1)

    def test_background_publication_rechecks_mode_without_holding_state_lock(self):
        observed = []
        @contextmanager
        def publication():
            # This would deadlock on the file lock if the state actor were held.
            observed.append(self.queue.status()['pending'])
            yield False
        self.queue.publication = publication
        result = self.queue.request({'action': 'queue', 'background': True,
                                     'requestId': 'disabled-queue-0001'}, 1000)
        self.assertEqual(result, {'_disabled': True})
        self.assertEqual(observed, [0])
        self.assertEqual(self.queue.status()['pending'], 0)

    def test_detached_planner_is_pinned_and_discarded_if_hot_authored_base_changes(self):
        planner = Mock()
        captured = []
        def plan(body):
            captured.append(copy.deepcopy(body['baseReference']))
            result = self.grader.request(body)
            self.grader.reference = [4, 5, 6]  # A repaired bank became visible.
            return result
        planner.request.side_effect = plan
        self.queue.planner = planner
        result = self.queue.request({'action': 'queue', 'background': True,
                                     'requestId': 'changed-bank-queue-0001'}, 1000)
        self.assertEqual(captured, [[1, 2, 3]])
        self.assertEqual(result, {'_superseded': True})
        self.assertEqual(self.queue.status()['pending'], 0)

    def test_detached_planner_waits_without_blocking_for_committed_base_after_drain(self):
        planner = Mock()
        self.queue.planner = planner
        original = self.grader.request
        def capture_not_ready(body):
            if body['action'] == 'study-capture':
                return {'ok': True, 'data': {'ready': False, 'basis': 10}}
            return original(body)
        self.grader.request = capture_not_ready
        self.assertEqual(self.queue.request({'action': 'queue', 'background': True,
                                             'requestId': 'lagging-base-queue-0001'}, 1000), {'_superseded': True})
        planner.request.assert_not_called()
        self.assertEqual(self.queue.status()['pending'], 0)

    def test_unknown_outcome_replays_exact_operation_across_restart(self):
        self.request()
        self.writer.request.return_value = {'ok': False, 'code': 'unavailable', 'error': 'lost receipt'}
        self.queue.run_one()
        attempted = copy.deepcopy(self.writer.request.call_args.args[0])
        self.queue = self.make()
        self.queue.retry()
        self.writer.request.return_value = {'ok': True, 'data': {}}
        self.queue.run_one()
        self.assertEqual(attempted, self.writer.request.call_args.args[0])
        self.assertEqual(self.queue.status()['status'], 'saved')

    def test_saved_receipts_are_archived_and_resolve_aliases_without_hiding_live_reads(self):
        first = self.request()
        self.queue.run_one()
        state = json.loads(self.queue.state_path.read_text())
        self.assertEqual(state['operations'], [])
        self.assertEqual(state['views'], {})
        self.assertIsNone(state['overlay'])
        self.assertIsNone(self.queue.task_view(4000000000000001))
        self.assertEqual(self.queue.resolve_ids({'taskId': 4000000000000001, 'itemId': 4000000000000002}), {'taskId': 100, 'itemId': 101})
        self.queue = self.make()
        self.assertEqual(self.request(), first)
        self.assertEqual(len(self.grader.calls), 1)
        self.assertEqual(self.queue.decorate({'taskId': 100})['idAliases']['4000000000000001'], 100)

    def test_second_process_writer_lane_does_not_duplicate_admission_or_overlap(self):
        self.request()
        other = self.make()
        entered, release = threading.Event(), threading.Event()
        def blocked(body):
            entered.set(); release.wait(3)
            return {'ok': True, 'data': {}}
        self.writer.request.side_effect = blocked
        thread = threading.Thread(target=self.queue.run_one)
        thread.start()
        try:
            self.assertTrue(entered.wait(1))
            self.assertFalse(other.run_one())
            other.request({'action': 'pause', 'taskId': 4000000000000001, 'requestId': 'pause-0001'}, 2000)
            self.assertEqual(other.status()['pending'], 2)
        finally:
            release.set(); thread.join(2)

    def test_confirmed_basis_rejection_rotates_attempt_only_and_validation_retains_work(self):
        self.request()
        self.writer.request.return_value = {'ok': False, 'code': 'basis-conflict', 'error': 'stale'}
        self.queue.run_one()
        first = self.writer.request.call_args.args[0]['operation']
        self.queue.retry()
        self.writer.request.return_value = {'ok': False, 'code': 'validation', 'error': 'route changed'}
        self.queue.run_one()
        second = self.writer.request.call_args.args[0]['operation']
        self.assertNotEqual(first['requestId'], second['requestId'])
        self.assertEqual(first['_queuedStudy'], second['_queuedStudy'])
        self.assertEqual(self.queue.status()['status'], 'error')
        self.assertEqual(self.queue.status()['pending'], 1)
        with self.assertRaisesRegex(ValueError, 'needs attention'):
            self.request('continue', 'request-0002')

if __name__ == '__main__':
    unittest.main()
