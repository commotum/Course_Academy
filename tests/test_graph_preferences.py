"""Local and proxied graph views share a file without touching learner data."""
from concurrent.futures import ThreadPoolExecutor
from email.message import Message
from io import BytesIO
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from graph_preferences import read_preferences, update_preferences
from serve_graph_explorer import handler, save_json


class GraphPreferences(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / 'graph-preferences.json'
        with patch('serve_graph_explorer.InventoryJobs'), patch('serve_graph_explorer.NativeWorker') as worker:
            self.worker = worker.return_value
            self.request_class = handler(Path('/unused'), 'test', 'learner', {
                'LEARNING_REQUEST_DIR': str(Path(self.temporary.name) / 'requests'),
                'COURSE_ACADEMY_GRAPH_PREFERENCES': str(self.path),
                'COURSE_ACADEMY_PUBLIC_ORIGIN': 'https://eve.example.ts.net:8443',
            })

    def request(self, host='127.0.0.1:8765', changes=None, origin=None):
        request = self.request_class.__new__(self.request_class)
        request.path = '/api/graph-preferences'
        request.server = SimpleNamespace(server_port=8765)
        request.headers = Message()
        request.headers['Host'] = host
        if origin:
            request.headers['Origin'] = origin
        request.send_bytes = Mock()
        if changes is None:
            request.do_GET()
        else:
            body = json.dumps({'changes': changes}).encode()
            request.headers['Content-Type'] = 'application/json'
            request.headers['Content-Length'] = str(len(body))
            request.rfile = BytesIO(body)
            request.do_POST()
        status, body, _ = request.send_bytes.call_args.args
        return status, json.loads(body) if status != 403 else None

    def test_local_save_is_visible_through_public_origin_and_after_handler_restart(self):
        self.assertEqual(self.request(changes={'colorCode': False, 'courses': ['341']})[0], 200)
        status, settings = self.request('eve.example.ts.net:8443')
        self.assertEqual(status, 200)
        self.assertFalse(settings['colorCode'])
        self.assertEqual(settings['courses'], ['341'])
        self.assertEqual(read_preferences(self.path), settings)
        self.worker.request.assert_not_called()
        self.assertFalse((Path(self.temporary.name) / 'requests').exists())

    def test_disjoint_concurrent_changes_are_merged(self):
        changes = [{'colorCode': False}, {'includeQueue': False}, {'splitByCourse': True}, {'courses': []}]
        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(lambda change: update_preferences(self.path, change, save_json), changes))
        value = read_preferences(self.path)
        for change in changes:
            for key, expected in change.items():
                self.assertEqual(value[key], expected)

    def test_invalid_settings_and_cross_origin_posts_cannot_change_saved_file(self):
        self.request(changes={'colorCode': True})
        before = self.path.read_bytes()
        for change in [{'colorCode': 'true'}, {'courses': ['999']}, {'weeks': {'kind': []}},
                       {'weeks': {'kind': 'range', 'start': 5, 'end': 1, 'anchor': 2}},
                       {'learner': 'someone-else'}]:
            self.assertEqual(self.request(changes=change)[0], 400)
        self.assertEqual(self.request(changes={'colorCode': False}, origin='https://other.example')[0], 403)
        self.assertEqual(self.path.read_bytes(), before)

    def test_absent_settings_use_defaults_without_creating_a_file(self):
        status, settings = self.request()
        self.assertEqual(status, 200)
        self.assertTrue(settings['colorCode'])
        self.assertEqual(settings['courses'], ['255', '256', '341'])
        self.assertFalse(self.path.exists())


if __name__ == '__main__':
    unittest.main()
