from contextlib import contextmanager, redirect_stdout
import io
import json
import os
from pathlib import Path
import shlex
import sys
import tempfile
import threading
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from scripts.config import Config
from scripts.storage import file_lock, read_json
from scripts import terminal


class TerminalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config_path = self.root / 'shared settings.json'
        self.config_path.write_text(json.dumps({'repo_root': str(self.root)}))
        self.args = SimpleNamespace(config=self.config_path, session='test-capture', capture_only=None,
                                    visible=False, learner_id=None, dry_run=False)

    def test_child_uses_new_capture_and_preserves_arguments(self):
        self.args.capture_only = True
        self.args.learner_id = 'some learner'
        command = terminal.child_command(self.args, 'linear')
        self.assertEqual(command[3:6], ['run', '--account', 'linear'])
        self.assertNotIn('--session', command)
        self.assertIn(str(self.config_path), command)
        invocation = shlex.split(terminal.invocation(self.args, 'worker', 'linear'))
        self.assertIn('some learner', invocation)
        self.assertIn(str(self.config_path), invocation)
        self.assertNotIn('question_capture', ' '.join(invocation))

    def test_existing_profile_owner_is_detected(self):
        config = terminal.config_for(self.args, 'linear')
        self.assertFalse(terminal.profile_busy(config))
        with file_lock(config.profile.parent / 'capture.lock'):
            self.assertTrue(terminal.profile_busy(config))
        self.assertFalse(terminal.profile_busy(config))

    def test_shared_browser_endpoint_is_rejected_before_launch(self):
        self.config_path.write_text(json.dumps({'browser_cdp_url': 'http://localhost:9222'}))
        with redirect_stdout(io.StringIO()), patch('sys.stderr', io.StringIO()), self.assertRaises(SystemExit) as error:
            terminal.main(['start', '--config', str(self.config_path)])
        self.assertEqual(error.exception.code, 2)

    def test_crash_restarts_and_explicit_stop_preserves_logs(self):
        config = terminal.config_for(self.args, 'linear')
        stub = self.root / 'stub.py'
        marker = self.root / 'launches'
        descendant = self.root / 'descendant'
        stub.write_text('''import pathlib, subprocess, sys, time
root = pathlib.Path(sys.argv[1])
marker = root / 'launches'
count = int(marker.read_text()) + 1 if marker.exists() else 1
marker.write_text(str(count))
print('stub launch', count, flush=True)
if count == 1:
    child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])
    (root / 'descendant').write_text(str(child.pid))
    raise SystemExit(3)
time.sleep(60)
''')
        state = {}
        @contextmanager
        def signals(stop):
            state['stop'] = stop
            yield
        def stop_second_launch():
            deadline = time.monotonic() + 15
            while time.monotonic() < deadline:
                if marker.exists() and marker.read_text() == '2':
                    break
                time.sleep(.05)
            state['stop'].set()
        observer = threading.Thread(target=stop_second_launch, daemon=True)
        observer.start()
        with patch.object(terminal, 'child_command', return_value=[sys.executable, str(stub), str(self.root)]), \
             patch.object(terminal, 'shutdown_signals', signals), redirect_stdout(io.StringIO()):
            terminal.supervise(self.args, 'linear')
        observer.join(timeout=2)
        self.assertEqual(marker.read_text(), '2')
        record = read_json(config.state_root / 'worker.json')
        self.assertEqual(record['restarts'], 1)
        self.assertTrue(record['stop_requested'])
        self.assertIn('finished_at', record)
        log = (config.state_root / 'console.log').read_text()
        self.assertIn('stub launch 1', log)
        self.assertIn('stub launch 2', log)
        status = Path('/proc') / descendant.read_text() / 'stat'
        if status.exists():
            self.assertIn(status.read_text().rsplit(')', 1)[1].split()[0], ('Z', 'X'))


if __name__ == '__main__':
    unittest.main()
