"""List reads and mode confirmation must not queue behind scheduler writes."""
from concurrent.futures import ThreadPoolExecutor
import fcntl
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from serve_graph_explorer import handler, admit_answer


class PageReadAdmission(unittest.TestCase):
    def test_submission_time_is_server_observed_and_survives_retries_and_new_transaction_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            body = {'action': 'answer', 'requestId': 'request-one', 'submissionId': 'submission-one', 'itemId': 1, 'responses': [{'fieldId': 2, 'value': '3'}], 'submittedAt': -1}
            first = admit_answer(body, Path(directory), 'learner', 1000)
            retry = admit_answer({**body, 'requestId': 'request-two'}, Path(directory), 'learner', 61000)
            self.assertEqual(first['submittedAt'], 1000)
            self.assertEqual(retry['submittedAt'], 1000)
            self.assertEqual(retry['requestId'], 'request-two')
            with self.assertRaises(ValueError):
                admit_answer({**body, 'itemId': 3}, Path(directory), 'learner', 62000)
            with self.assertRaises(ValueError):
                admit_answer({**body, 'submissionId': '../bad'}, Path(directory), 'learner', 62000)

    def test_preexisting_answer_receipts_keep_their_original_input(self):
        with tempfile.TemporaryDirectory() as directory:
            body = {'action': 'answer', 'requestId': 'legacy-request', 'itemId': 1, 'responses': []}
            (Path(directory) / 'learner-legacy-request.json').write_text(json.dumps({'input': body}))
            self.assertEqual(admit_answer(body, Path(directory), 'learner', 61000), body)

    def test_study_now_response_does_not_wait_for_inventory_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            environment = {"LEARNING_REQUEST_DIR": directory, "EDB_ENDPOINT": "/unused"}
            with patch("serve_graph_explorer.InventoryJobs"), patch("serve_graph_explorer.NativeWorker") as workers:
                def respond(body):
                    self.assertEqual(body["action"], "study-topic", "Inventory must run after the API response")
                    return {"ok": True, "data": {"taskId": 1}}
                workers.return_value.request.side_effect = respond
                cls = handler(Path("/unused"), "test", "learner", environment, Path("/unused"))
                request = cls.__new__(cls)
                replies = []
                request.send_bytes = lambda status, body, content_type: replies.append((status, json.loads(body)))
                request.learning_request({"action": "study-topic", "topicId": 2})
                self.assertEqual(replies, [(200, {"taskId": 1})])
                self.assertTrue(cls.inventory_refresh.is_set())
                self.assertEqual(workers.return_value.request.call_count, 1)

    def test_lists_and_mode_read_finish_while_writer_lock_is_held(self):
        with tempfile.TemporaryDirectory() as directory:
            environment = {"LEARNING_REQUEST_DIR": directory, "EDB_ENDPOINT": "/unused"}
            with patch("serve_graph_explorer.InventoryJobs"), patch("serve_graph_explorer.NativeWorker") as workers:
                workers.return_value.request.return_value = {"ok": True, "data": {"list": []}}
                cls = handler(Path("/unused"), "test", "learner", environment, Path("/unused"))
                with (Path(directory) / "api.lock").open("a") as lock:
                    fcntl.flock(lock, fcntl.LOCK_EX)
                    with ThreadPoolExecutor(max_workers=1) as executor:
                        for action in ["assignments", "activity-history", "study-stats", "mode", "answer"]:
                            request = cls.__new__(cls)
                            replies = []
                            request.send_bytes = lambda status, body, content_type: replies.append((status, json.loads(body)))
                            if action == "mode":
                                pending = executor.submit(request.mode_request)
                            else:
                                body = {"action": action}
                                if action == 'answer':
                                    body.update(requestId='answer-test-request', submissionId='answer-test-submission', itemId=1, responses=[])
                                pending = executor.submit(request.learning_request, body)
                            try:
                                pending.result(timeout=1)
                            except TimeoutError:
                                # Let a regressed request finish so the executor
                                # can exit instead of hanging the test runner.
                                fcntl.flock(lock, fcntl.LOCK_UN)
                                pending.result(timeout=2)
                                self.fail(f"{action} waited for the writer lock")
                            self.assertEqual(replies[0][0], 200)
                    fcntl.flock(lock, fcntl.LOCK_UN)


if __name__ == "__main__":
    unittest.main()
