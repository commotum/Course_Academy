import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from serve_graph_explorer import NativeWorker, focused_mode, focused_mode_path, save_json


class FocusedModePreferenceTests(unittest.TestCase):
    def test_preference_is_per_learner_persistent_and_strict(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first, second = [focused_mode_path(root, name) for name in ('first', 'second')]
            self.assertIsNone(focused_mode(first))
            save_json(first, {'enabled': False})
            self.assertIs(focused_mode(first), False)
            self.assertIsNone(focused_mode(second))
            save_json(first, {'enabled': True})
            self.assertIs(focused_mode(first), True)
            save_json(first, {'enabled': 'false'})
            with self.assertRaises(ValueError):
                focused_mode(first)

    def test_worker_uses_saved_preference_each_request_and_ignores_client_override(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            executable = root / 'echo-worker'
            executable.write_text('#!' + sys.executable + '\n'
                'import json,sys\n'
                'for line in sys.stdin:\n'
                ' print(json.dumps({"ok":True,"data":json.loads(line)}),flush=True)\n')
            executable.chmod(0o700)
            preference = focused_mode_path(root, 'learner')
            worker = NativeWorker([str(executable), 'math', 'learner', 'endpoint', '--serve'],
                {**os.environ, 'LEARNING_REQUEST_DIR': str(root)}, 'focused-preference-test')
            try:
                save_json(preference, {'enabled': False})
                first = worker.request({'action': 'home', '_focusedMode': True})['data']
                self.assertIs(first['_focusedMode'], False)
                save_json(preference, {'enabled': True})
                second = worker.request({'action': 'home'})['data']
                self.assertIs(second['_focusedMode'], True)
                preference.unlink()
                self.assertNotIn('_focusedMode', worker.request({'action': 'home', '_focusedMode': False})['data'])
            finally:
                worker.close()


if __name__ == '__main__':
    unittest.main()
