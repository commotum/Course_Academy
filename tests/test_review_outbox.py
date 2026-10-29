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
from review_outbox import ReviewOutbox
from serve_graph_explorer import save_json


class Grader:
    def __init__(self):
        steps = [{'itemId': None, 'contentId': q, 'status': 'started', 'fields': [], 'canContinue': False} for q in range(10, 15)]
        view = {'taskId': 1, 'type': 'review', 'status': 'started', 'step': {**steps[0], 'itemId': 100},
                'elapsedSeconds': 0, 'progress': {'stepNumber': 1, 'presented': 1}, 'history': []}
        view['step']['elapsedSeconds'] = 0
        self.initial = {'view': view, 'steps': steps, 'periods': [{'id': 'period-1', 'start': 1000, 'end': None}]}

    def request(self, body):
        action = body['action']
        if action == 'review-session':
            return {'ok': True, 'data': copy.deepcopy(self.initial)}
        if action in {'review-grade', 'review-skip'}:
            correct = body.get('responses', [{}])[0].get('choiceId') == 20
            return {'ok': True, 'data': {'step': {'contentId': body['questionId'], 'status': 'skipped' if action == 'review-skip' else 'correct' if correct else 'incorrect', 'fields': [], 'canContinue': True, 'solution': 'Complete solution'}}}
        if action == 'review-decision':
            outcomes = body['outcomes']
            complete = outcomes[-3:] == ['correct'] * 3 or len(outcomes) == 5 or outcomes[-2:] == ['incorrect'] * 2
            return {'ok': True, 'data': {'complete': complete, 'passed': complete and outcomes[-1] == 'correct', 'xp': 7}}
        raise AssertionError(action)


class ReviewOutboxTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.stop = threading.Event()
        self.grader, self.writer = Grader(), Mock()
        self.writer.request.return_value = {'ok': True, 'data': {}}
        self.queue = self.make_queue()

    def make_queue(self):
        return ReviewOutbox(Path(self.tmp.name), self.grader, self.writer, save_json, self.stop)

    def answer(self, item=100, key='answer-0001', now=2000):
        return self.queue.request({'action': 'answer', 'taskId': 1, 'itemId': item, 'responses': [{'fieldId': 30, 'choiceId': 20}], 'requestId': key}, now)

    def advance(self, item=100, key='continue-0001', now=2100):
        return self.queue.request({'action': 'continue', 'taskId': 1, 'itemId': item, 'requestId': key}, now)

    def test_feedback_next_and_second_answer_do_not_wait_for_blocked_edb_write(self):
        feedback = self.answer()
        self.assertEqual(feedback['step']['status'], 'correct')
        self.assertEqual(feedback['saveState']['pending'], 1)
        entered, release = threading.Event(), threading.Event()
        def blocked(body):
            entered.set()
            release.wait(2)
            return {'ok': True, 'data': {}}
        self.writer.request.side_effect = blocked
        thread = threading.Thread(target=self.queue.run_one)
        thread.start()
        try:
            self.assertTrue(entered.wait(1))
            start = time.monotonic()
            next_step = self.advance()
            second = self.answer(next_step['step']['itemId'], 'answer-0002', 2600)
            self.assertLess(time.monotonic() - start, .2)
            self.assertEqual(second['step']['contentId'], 11)
            self.assertEqual(second['step']['status'], 'correct')
            self.assertEqual(second['saveState']['pending'], 3)
        finally:
            release.set()
            thread.join(2)
        self.writer.request.side_effect = None
        while self.queue.run_one(): pass
        operations = [call.args[0]['operation'] for call in self.writer.request.call_args_list]
        self.assertEqual([op['action'] for op in operations], ['answer', 'continue', 'answer'])
        self.assertEqual([op['_queuedReview']['questionId'] for op in operations], [10, 10, 11])
        self.assertEqual(self.queue.status(1)['status'], 'saved')

    def test_restart_and_lost_ack_replay_keep_exact_request_and_never_duplicate_queue(self):
        first = self.answer()
        self.queue = self.make_queue()
        self.assertEqual(self.answer(), first)
        self.assertEqual(self.queue.status(1)['pending'], 1)
        # Simulate a lost save acknowledgement after the database committed.
        self.writer.request.return_value = {'ok': False, 'code': 'unavailable', 'error': 'lost reply'}
        self.queue.run_one()
        attempted = self.writer.request.call_args.args[0]
        self.queue = self.make_queue()
        self.queue.retry(1)
        self.writer.request.return_value = {'ok': True, 'data': {}}
        self.queue.run_one()
        self.assertEqual(self.writer.request.call_args.args[0], attempted)
        self.assertEqual(self.queue.status(1)['status'], 'saved')

    def test_confirmed_basis_rejection_changes_only_write_request_identity(self):
        self.answer()
        self.writer.request.return_value = {'ok': False, 'code': 'basis-conflict', 'error': 'stale'}
        self.queue.run_one()
        first = self.writer.request.call_args.args[0]['operation']
        self.queue.retry(1)
        self.writer.request.return_value = {'ok': True, 'data': {}}
        self.queue.run_one()
        second = self.writer.request.call_args.args[0]['operation']
        self.assertNotEqual(first['requestId'], second['requestId'])
        self.assertEqual({k:v for k,v in first.items() if k != 'requestId'}, {k:v for k,v in second.items() if k != 'requestId'})

    def test_pause_resume_work_intervals_exclude_save_and_pause_waits(self):
        self.queue.request({'action': 'pause', 'taskId': 1, 'requestId': 'pause-0001'}, 2000)
        self.queue.request({'action': 'resume', 'taskId': 1, 'requestId': 'resume-0001'}, 10000)
        feedback = self.answer(now=11000)
        self.assertEqual(feedback['elapsedSeconds'], 2)
        state = json.loads(self.queue.path(1).read_text())
        self.assertEqual([(p['start'],p['end']) for p in state['periods']], [(1000,2000),(10000,11000)])

    def test_invalid_save_is_visible_and_retains_every_accepted_operation(self):
        self.answer()
        self.writer.request.return_value = {'ok': False, 'code': 'validation', 'error': 'Task changed in another tab'}
        self.queue.run_one()
        self.assertEqual(self.queue.status(1)['status'], 'error')
        with self.assertRaisesRegex(ValueError, 'needs attention'):
            self.advance()
        self.assertEqual(self.queue.status(1)['pending'], 1)

    def test_review_stops_on_shared_decision_and_keeps_three_answers_queued(self):
        item = 100
        for n in range(3):
            self.answer(item, f'answer-{n:04}', 2000+n*1000)
            view = self.advance(item, f'continue-{n:04}', 2100+n*1000)
            item = view['step']['itemId']
        self.assertEqual(view['status'], 'completed')
        self.assertEqual(view['xp'], 7)
        self.assertEqual(view['saveState']['pending'], 6)
        self.assertEqual(len(view['history']), 3)

    def test_switching_activity_pauses_the_queued_clock_before_draining(self):
        self.answer()
        next_step = self.advance()
        thread = threading.Thread(target=self.queue.loop, daemon=True)
        thread.start()
        try:
            self.queue.drain(timeout=2, pause_active=True)
            self.assertEqual(self.queue.task_view(1)['status'], 'paused')
            operations = [call.args[0]['operation']['action'] for call in self.writer.request.call_args_list]
            self.assertEqual(operations, ['answer', 'continue', 'pause'])
        finally:
            self.stop.set()
            self.queue.wake.set()
            thread.join(2)

    def test_assessments_keep_synchronous_submission_and_never_use_fast_grade(self):
        self.grader.request = Mock(return_value={'ok': False, 'error': 'Fast interaction requires a review'})
        self.assertIsNone(self.answer())
        self.assertFalse(self.queue.path(1).exists())
        self.writer.request.assert_not_called()

    def test_different_payload_cannot_reuse_accepted_request_identity(self):
        self.answer()
        with self.assertRaisesRegex(ValueError, 'already used'):
            self.queue.request({'action': 'skip', 'taskId': 1, 'itemId': 100, 'requestId': 'answer-0001'}, 2100)


if __name__ == '__main__': unittest.main()
