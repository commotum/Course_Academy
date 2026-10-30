import copy
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

    def request(self, body):
        self.calls.append(copy.deepcopy(body))
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
