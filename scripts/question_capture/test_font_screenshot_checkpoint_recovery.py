import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch
from browser import CaptureBrowser

class FontScreenshotCheckpointRecoveryTests(unittest.TestCase):
    def restore(self, directory, grade_available):
        item = {'dom_id':'step-q1', 'problem':'Find x.', 'result':'Correct',
                'worked_solution':'x=1.', 'errors':[], 'assets':[]}
        (directory/'q-1-after.json').write_text(json.dumps(item))
        page = Mock()
        reader = CaptureBrowser(page, SimpleNamespace(timeout_ms=3000), Mock(), Mock())
        reader.wait_activity_ready = Mock()
        reader.current_step = Mock(return_value='stepButton-q2')
        reader.is_staged_question = Mock(return_value=False)
        reader.read = Mock(return_value=(item, directory/'q-1-after.png'))
        reader.enter = Mock()
        reader.finalize_question = Mock(side_effect=RuntimeError('stop after reconciliation'))
        scope = Mock()
        scope.locator.return_value.count.return_value = int(grade_available)
        scope.locator.return_value.inner_text.return_value = 'Correct'
        scope.is_visible.return_value = True
        record = {'status':'submitting', 'before':{'problem':'Find x.'}}
        state = {'task_type':'lesson', 'kps':{}, 'questions':{'q-1':record}}
        with patch('browser.by_id', return_value=scope):
            with self.assertRaisesRegex(RuntimeError,'stop after reconciliation'):
                reader.activity(state,directory,{})
        self.assertEqual(record['status'],'graded')
        self.assertEqual(record['actual_result'],'Correct')
        self.assertEqual(record['after'],item)
        reader.enter.assert_not_called()
        scope.locator.return_value.click.assert_not_called()
        return reader,scope

    def test_good_json_missing_or_empty_png_recaptures_available_grade_without_submit(self):
        for empty in (False,True):
            with self.subTest(empty=empty), tempfile.TemporaryDirectory() as work:
                directory = Path(work)
                if empty: (directory/'q-1-after.png').touch()
                reader,scope = self.restore(directory,True)
                reader.read.assert_called_once_with(scope,directory,'q-1-after')
                saved = json.loads((directory/'state.json').read_text())['questions']['q-1']
                recovery = saved['after_capture_recovery']
                archived = Path(recovery['archived_original_json'])
                self.assertEqual(hashlib.sha256(archived.read_bytes()).hexdigest(), recovery['original_json_sha256'])
                self.assertEqual(json.loads(archived.read_text())['dom_id'], 'step-q1')
                self.assertEqual(json.loads(archived.read_text())['worked_solution'], 'x=1.')
                self.assertEqual(recovery['recaptured_screenshot'], str(directory/'q-1-after.png'))

    def test_existing_png_avoids_redundant_grade_capture(self):
        with tempfile.TemporaryDirectory() as work:
            directory=Path(work)
            (directory/'q-1-after.png').write_bytes(b'original saved screenshot')
            reader,_=self.restore(directory,True)
            reader.read.assert_not_called()

    def test_absent_live_grade_preserves_complete_json_for_history_binding(self):
        with tempfile.TemporaryDirectory() as work:
            reader,_=self.restore(Path(work),False)
            reader.read.assert_not_called()
