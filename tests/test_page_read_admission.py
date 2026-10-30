"""List reads and mode confirmation must not queue behind scheduler writes."""
from concurrent.futures import ThreadPoolExecutor
import fcntl
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "generate/scripts"))
from serve_graph_explorer import handler, admit_answer


class PageReadAdmission(unittest.TestCase):
    def test_task_and_profile_reads_do_not_share_the_blocked_write_worker(self):
        with tempfile.TemporaryDirectory() as directory:
            environment = {'LEARNING_REQUEST_DIR': directory, 'EDB_ENDPOINT': '/unused'}
            workers = {}
            def make_worker(command, env, name):
                worker = Mock()
                worker.request.return_value = {'ok': True, 'data': {'name': name}}
                workers[name] = worker
                return worker
            with patch('serve_graph_explorer.InventoryJobs'), patch('serve_graph_explorer.NativeWorker', side_effect=make_worker):
                cls = handler(Path('/unused'), 'test', 'learner', environment, Path('/unused'))
            workers['learning-worker'].request.side_effect = AssertionError('Read entered write lane')
            with (Path(directory) / 'api.lock').open('a') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX)
                with ThreadPoolExecutor() as executor:
                    for action in ['task', 'profile', 'learner', 'assignment', 'activity-history-detail']:
                        request = cls.__new__(cls)
                        replies = []
                        request.send_bytes = lambda status, body, ctype: replies.append(json.loads(body))
                        executor.submit(request.learning_request, {'action': action, 'taskId': 1}).result(timeout=1)
                        self.assertEqual([reply['name'] for reply in replies], ['study-read-worker'])
            workers['learning-worker'].request.assert_not_called()

    def test_activity_cache_returns_while_its_refresh_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            environment = {'LEARNING_REQUEST_DIR': directory, 'EDB_ENDPOINT': '/unused'}
            with patch('serve_graph_explorer.InventoryJobs'), patch('serve_graph_explorer.NativeWorker') as workers:
                workers.return_value.request.return_value = {'ok': True, 'data': {'activities': []}}
                cls = handler(Path('/unused'), 'test', 'learner', environment, Path('/unused'))
            def read():
                request = cls.__new__(cls)
                replies = []
                request.send_bytes = lambda status, body, ctype: replies.append(status)
                request.learning_request({'action': 'activity-history'})
                return replies
            self.assertEqual(read(), [200])
            cls.read_cache.invalidate()
            entered, release = threading.Event(), threading.Event()
            def blocked(_body):
                entered.set()
                release.wait(3)
                return {'ok': True, 'data': {'activities': [1]}}
            workers.return_value.request.side_effect = blocked
            try:
                with ThreadPoolExecutor() as executor:
                    self.assertEqual(executor.submit(read).result(timeout=.5), [200])
                    self.assertTrue(entered.wait(.5))
                    self.assertEqual(executor.submit(read).result(timeout=.5), [200])
            finally:
                release.set()

    def test_xp_read_finishes_while_forecast_worker_is_busy(self):
        with tempfile.TemporaryDirectory() as directory:
            environment = {"LEARNING_REQUEST_DIR": directory, "EDB_ENDPOINT": "/unused"}
            entered, release = threading.Event(), threading.Event()
            page, stats = Mock(), Mock()
            def forecast(body):
                entered.set()
                release.wait(3)
                return {"ok": True, "data": {"forecast": True}}
            page.request.side_effect = forecast
            stats.request.return_value = {"ok": True, "data": {"days": []}}
            with patch("serve_graph_explorer.InventoryJobs"), patch("serve_graph_explorer.NativeWorker", side_effect=[Mock(), Mock(), Mock(), stats, Mock(), Mock(), Mock(), Mock(), page]):
                cls = handler(Path("/unused"), "test", "learner", environment, Path("/unused"))
            def read(action):
                request = cls.__new__(cls)
                replies = []
                request.send_bytes = lambda status, body, content_type: replies.append(status)
                request.learning_request({"action": action})
                return replies
            with ThreadPoolExecutor(max_workers=2) as executor:
                pending = executor.submit(read, "forecast-inputs")
                try:
                    self.assertTrue(entered.wait(1))
                    self.assertEqual(executor.submit(read, "study-stats").result(timeout=1), [200])
                    stats.request.assert_called_once_with({"action": "study-stats"})
                finally:
                    release.set()
                    pending.result(timeout=2)
            self.assertIn(stats, cls.workers)

    def test_review_feedback_does_not_wait_for_scheduler_lock_or_persistence_worker(self):
        from test_review_outbox import Grader
        from serve_graph_explorer import save_json
        with tempfile.TemporaryDirectory() as directory:
            environment = {"LEARNING_REQUEST_DIR": directory, "EDB_ENDPOINT": "/unused"}
            workers = {name: Mock() for name in ['graph-worker','learning-worker','page-worker','stats-worker','scheduler-worker','feedback-worker','review-save-worker','study-read-worker','forecast-read-worker']}
            grader = Grader()
            def project(body):
                self.assertEqual(body['action'], 'study-project')
                view = grader.request({'action': 'review-session', 'taskId': 1})['data']['view']
                view['step'] = grader.request({'action': 'review-grade', 'taskId': 1, 'questionId': 10, 'responses': body['operation']['responses']})['data']['step']
                view['step']['itemId'] = 100
                return {'ok': True, 'data': {'view': view, 'views': {'1': view}, 'overlay': {}, 'operation': body['operation']}}
            workers['feedback-worker'].request.side_effect = project
            with patch("serve_graph_explorer.InventoryJobs"), patch("serve_graph_explorer.NativeWorker", side_effect=lambda cmd,env,name: workers[name]):
                cls = handler(Path('/unused'), 'test', 'learner', environment, Path('/unused'))
            # Simulate the scheduler/publication holding admission while EDB save is unavailable.
            with (Path(directory)/'api.lock').open('a') as lock:
                fcntl.flock(lock,fcntl.LOCK_EX)
                request = cls.__new__(cls)
                replies=[]
                request.send_bytes=lambda status,body,ctype:replies.append((status,json.loads(body)))
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future=executor.submit(request.learning_request,{'action':'answer','taskId':1,'itemId':100,'requestId':'review-answer-001','responses':[{'fieldId':30,'choiceId':20}]})
                    future.result(timeout=1)
            self.assertEqual(replies[0][0],200)
            self.assertEqual(replies[0][1]['step']['status'],'correct')
            self.assertEqual(replies[0][1]['saveState']['status'],'pending')
            workers['learning-worker'].request.assert_not_called()
            workers['scheduler-worker'].request.assert_not_called()
            workers['review-save-worker'].request.assert_not_called()
            self.assertTrue((Path(directory)/'study-outbox/study.json').exists())

    def test_forecast_get_uses_only_the_read_only_page_reader(self):
        with tempfile.TemporaryDirectory() as directory:
            environment = {"LEARNING_REQUEST_DIR": directory, "EDB_ENDPOINT": "/unused"}
            with patch("serve_graph_explorer.InventoryJobs"), patch("serve_graph_explorer.NativeWorker"):
                cls = handler(Path("/unused"), "test", "learner", environment, Path("/unused"))
                request = cls.__new__(cls)
                request.path = "/api/forecast-inputs?dayStarts=" + ",".join(str(i * 86400000) for i in range(8))
                request.trusted = lambda: True
                reads = []
                request.learning_request = reads.append
                request.do_GET()
                self.assertEqual(reads, [{"action": "forecast-inputs", "dayStarts": [i * 86400000 for i in range(8)]}])

    def test_topic_availability_get_validates_one_topic_id_and_only_reads(self):
        with tempfile.TemporaryDirectory() as directory:
            environment = {"LEARNING_REQUEST_DIR": directory, "EDB_ENDPOINT": "/unused"}
            with patch("serve_graph_explorer.InventoryJobs"), patch("serve_graph_explorer.NativeWorker"):
                cls = handler(Path("/unused"), "test", "learner", environment, Path("/unused"))
                for query in ["topicId=20", "", "topicId=0", "topicId=-1", "topicId=nope", "topicId=20&topicId=25", "topicId=9007199254740992"]:
                    request = cls.__new__(cls)
                    request.path = "/api/topic-study-availability?" + query
                    request.trusted = lambda: True
                    reads, replies = [], []
                    request.learning_request = reads.append
                    request.send_bytes = lambda status, body, content_type: replies.append(status)
                    request.do_GET()
                    if query == "topicId=20":
                        self.assertEqual(reads, [{"action": "topic-study-availability", "topicId": 20}])
                        self.assertEqual(replies, [])
                    else:
                        self.assertEqual(reads, [])
                        self.assertEqual(replies, [400])

    def test_both_generation_lanes_wait_for_ranked_inventory_and_refresh_after_work(self):
        with tempfile.TemporaryDirectory() as directory:
            environment = {"LEARNING_REQUEST_DIR": directory, "EDB_ENDPOINT": "/unused"}
            with patch("serve_graph_explorer.InventoryJobs") as jobs, patch("serve_graph_explorer.NativeWorker"):
                cls = handler(Path('/unused'), 'test', 'learner', environment, Path('/unused'))
                loops = [(fn, 'build' if fn.__name__ == 'generator_build_loop' else 'refill',
                          getattr(fn, 'worker_slot', 0)) for fn in cls.background
                         if fn.__name__ in {'generator_build_loop', 'generator_refill_loop'}]
                self.assertEqual([(lane, slot) for _, lane, slot in loops],
                                 [('build', 0), ('build', 1), ('build', 2), ('refill', 0)])
                for fn, lane, slot in loops:
                    cls.scheduler_stop.clear()
                    with patch.object(cls.scheduler_stop, 'wait', side_effect=lambda _: cls.scheduler_stop.set()):
                        fn()
                jobs.return_value.run_one.assert_not_called()
                cls.inventory_ready.set()
                for fn, lane, slot in loops:
                    cls.scheduler_stop.clear()
                    cls.inventory_refresh.clear()
                    jobs.return_value.run_one.reset_mock()
                    with patch.object(cls.scheduler_stop, 'wait', side_effect=lambda _: cls.scheduler_stop.set()):
                        fn()
                    jobs.return_value.run_one.assert_called_once_with(lane=lane, slot=slot)
                    self.assertTrue(cls.inventory_refresh.is_set())

    def test_unexpected_generator_error_keeps_lane_alive_and_retries_after_wait(self):
        with tempfile.TemporaryDirectory() as directory:
            environment = {'LEARNING_REQUEST_DIR': directory, 'EDB_ENDPOINT': '/unused'}
            with patch('serve_graph_explorer.InventoryJobs') as jobs, patch('serve_graph_explorer.NativeWorker'), \
                 patch('serve_graph_explorer.developer_mode', return_value=False), \
                 patch('serve_graph_explorer.traceback.print_exc') as diagnostic:
                cls = handler(Path('/unused'), 'test', 'learner', environment, Path('/unused'))
                loops = [fn for fn in cls.background
                         if fn.__name__ in {'generator_build_loop', 'generator_refill_loop'}]
                cls.inventory_ready.set()
                for fn in loops:
                    cls.scheduler_stop.clear()
                    cls.inventory_refresh.clear()
                    jobs.return_value.run_one.reset_mock()
                    jobs.return_value.run_one.side_effect = [KeyError('state'), True]
                    waits = []
                    def wait(seconds):
                        waits.append(seconds)
                        if len(waits) == 2:
                            cls.scheduler_stop.set()
                    with patch.object(cls.scheduler_stop, 'wait', side_effect=wait), patch('builtins.print'):
                        fn()
                    self.assertEqual(jobs.return_value.run_one.call_count, 2)
                    self.assertEqual(waits, [5, 5])
                    self.assertTrue(cls.inventory_refresh.is_set())
                self.assertEqual(diagnostic.call_count, len(loops))

    def test_configured_builder_count_controls_background_slots(self):
        with tempfile.TemporaryDirectory() as directory:
            environment = {'LEARNING_REQUEST_DIR': directory, 'EDB_ENDPOINT': '/unused',
                           'COURSE_ACADEMY_GENERATOR_BUILD_WORKERS': '2'}
            with patch('serve_graph_explorer.InventoryJobs'), patch('serve_graph_explorer.NativeWorker'):
                cls = handler(Path('/unused'), 'test', 'learner', environment, Path('/unused'))
                slots = [fn.worker_slot for fn in cls.background if fn.__name__ == 'generator_build_loop']
                self.assertEqual(slots, [0, 1])

    def test_both_lanes_honor_developer_mode_and_generation_disable(self):
        with tempfile.TemporaryDirectory() as directory:
            for disabled, developer in ((True, False), (False, True)):
                environment = {"LEARNING_REQUEST_DIR": directory, "EDB_ENDPOINT": "/unused",
                               "COURSE_ACADEMY_DISABLE_GENERATION": '1' if disabled else '0'}
                with patch("serve_graph_explorer.InventoryJobs") as jobs, patch("serve_graph_explorer.NativeWorker"), \
                     patch("serve_graph_explorer.developer_mode", return_value=developer):
                    cls = handler(Path('/unused'), 'test', 'learner', environment, Path('/unused'))
                    cls.inventory_ready.set()
                    for fn in cls.background:
                        if fn.__name__ not in {'generator_build_loop', 'generator_refill_loop'}:
                            continue
                        cls.scheduler_stop.clear()
                        with patch.object(cls.scheduler_stop, 'wait', side_effect=lambda _: cls.scheduler_stop.set()):
                            fn()
                    jobs.return_value.run_one.assert_not_called()

    def test_ranked_scan_does_not_take_api_lock_or_learning_worker(self):
        with tempfile.TemporaryDirectory() as directory:
            environment = {"LEARNING_REQUEST_DIR": directory, "EDB_ENDPOINT": "/unused"}
            with patch("serve_graph_explorer.InventoryJobs") as jobs, patch("serve_graph_explorer.NativeWorker") as workers, \
                 patch('find_candidates.build', return_value=Path('/unused')), patch('find_candidates.discover') as discover:
                cls = handler(Path('/unused'), 'test', 'learner', environment, Path('/unused'))
                entered, release = threading.Event(), threading.Event()
                snapshot = {'basis': 123, 'knowledge_points': []}
                def scan(*args, **kwargs):
                    self.assertTrue(kwargs['include_registered'])
                    entered.set()
                    release.wait(2)
                    return snapshot
                discover.side_effect = scan
                refresh = next(fn for fn in cls.background if fn.__name__ == 'inventory_refresh_loop')
                with (Path(directory) / 'api.lock').open('a') as lock:
                    fcntl.flock(lock, fcntl.LOCK_EX)
                    thread = threading.Thread(target=refresh, daemon=True)
                    thread.start()
                    try:
                        self.assertTrue(entered.wait(1), 'Finder blocked behind the API lock')
                        self.assertFalse(cls.inventory_ready.is_set())
                        workers.return_value.request.assert_not_called()
                    finally:
                        cls.scheduler_stop.set()
                        release.set()
                        thread.join(3)
                jobs.return_value.accept.assert_called_once_with(snapshot)
                self.assertTrue(cls.inventory_ready.is_set())

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
                    self.assertEqual(body["action"], "study-project", "Inventory must run after the API response")
                    self.assertEqual(body["operation"]["action"], "study-topic")
                    return {"ok": True, "data": {"view": {"taskId": 1}, "views": {}, "overlay": {}, "operation": body["operation"]}}
                workers.return_value.request.side_effect = respond
                cls = handler(Path("/unused"), "test", "learner", environment, Path("/unused"))
                request = cls.__new__(cls)
                replies = []
                request.send_bytes = lambda status, body, content_type: replies.append((status, json.loads(body)))
                request.learning_request({"action": "study-topic", "topicId": 2, "requestId": "study-topic-test"})
                self.assertEqual(replies[0][0], 200)
                self.assertEqual(replies[0][1]["taskId"], 1)
                self.assertEqual(replies[0][1]["saveState"]["status"], "pending")
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
                        for action in ["assignments", "activity-history", "study-stats", "forecast-inputs", "mode", "topic-study-availability", "profile", "learner", "task", "assignment", "activity-history-detail", "home", "preview", "preview-home"]:
                            request = cls.__new__(cls)
                            replies = []
                            request.send_bytes = lambda status, body, content_type: replies.append((status, json.loads(body)))
                            if action == "mode":
                                pending = executor.submit(request.mode_request)
                            else:
                                body = {"action": action, "taskId": 1}
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
