"""Upgrade recovery keeps already acknowledged review progress and receipts."""
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from review_outbox import ReviewOutbox
from study_outbox_compat import CompatibleStudyOutbox
from serve_graph_explorer import save_json
from test_review_outbox import Grader


class OutboxUpgradeTests(unittest.TestCase):
    def test_learner_namespaces_and_legacy_recovery_do_not_cross_profiles(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'review-outbox'
            writer, stop = Mock(), threading.Event()
            old = ReviewOutbox(root, Grader(), writer, save_json, stop)
            old.request({'action': 'pause', 'taskId': 1, 'requestId': 'old-pause-001'}, 2000)
            state = old.load(old.path(1))
            state['view']['learner'] = {'id': 'learner-one'}
            save_json(old.path(1), state)
            one = CompatibleStudyOutbox(root, Grader(), writer, save_json, stop, learner='learner-one')
            two = CompatibleStudyOutbox(root, Grader(), writer, save_json, stop, learner='learner-two')
            self.assertNotEqual(one.study.state_path, two.study.state_path)
            self.assertEqual(one.status()['pending'], 1)
            self.assertEqual(two.status()['pending'], 0)
            self.assertFalse(two.legacy.run_one())
            writer.request.assert_not_called()

    def test_pending_legacy_answer_recovers_and_saved_receipt_remains_exact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'review-outbox'
            grader, writer, stop = Grader(), Mock(), threading.Event()
            writer.request.return_value = {'ok': True, 'data': {}}
            old = ReviewOutbox(root, grader, writer, save_json, stop)
            body = {'action': 'answer', 'taskId': 1, 'itemId': 100,
                    'requestId': 'old-answer-001', 'responses': [{'fieldId': 30, 'choiceId': 20}]}
            original = old.request(body, 2000)
            upgraded = CompatibleStudyOutbox(root, grader, writer, save_json, stop)
            self.assertEqual(upgraded.request(body, 9000), original)
            self.assertEqual(upgraded.task_view(1)['step']['status'], 'correct')
            self.assertEqual(upgraded.status()['pending'], 1)
            self.assertTrue(upgraded.legacy.run_one())
            self.assertEqual(writer.request.call_args.args[0]['action'], 'persist-review')
            self.assertEqual(upgraded.status()['pending'], 0)
            self.assertIsNone(upgraded.task_view(1))
            self.assertEqual(upgraded.request(body, 10000), original)
            # On the next service restart the archived legacy receipt still
            # answers a duplicate without creating any second learner credit.
            restarted = CompatibleStudyOutbox(root, grader, writer, save_json, stop)
            self.assertEqual(restarted.request(body, 11000), original)
            self.assertEqual(writer.request.call_count, 1)

    def test_new_work_uses_general_outbox_when_legacy_recovery_is_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'review-outbox'
            grader, writer, stop = Mock(), Mock(), threading.Event()
            operation = {'action': 'pause', 'taskId': 7, 'requestId': 'new-pause-001'}
            grader.request.return_value = {'ok': True, 'data': {
                'view': {'taskId': 7, 'status': 'paused'}, 'views': {},
                'operation': operation, 'overlay': {}}}
            upgraded = CompatibleStudyOutbox(root, grader, writer, save_json, stop)
            response = upgraded.request(operation, 1000)
            self.assertEqual(response['status'], 'paused')
            self.assertEqual(grader.request.call_args.args[0]['action'], 'study-project')
            self.assertEqual(upgraded.status()['pending'], 1)
            writer.request.assert_not_called()
            self.assertTrue((root.parent / 'study-outbox/study.json').exists())


if __name__ == '__main__':
    unittest.main()
