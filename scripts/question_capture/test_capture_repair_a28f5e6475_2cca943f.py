import copy
import tempfile
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import browser

class CompletedReviewTests(unittest.TestCase):
    def setUp(self):
        capture = tempfile.TemporaryDirectory()
        self.addCleanup(capture.cleanup)
        self.directory = Path(capture.name)

    def setup_reader(self):
        # A completed review reached /learn while its last submission was still
        # pending locally. Keep that interrupted checkpoint in the test: the
        # real archived task was subsequently recovered and can change again.
        state = {'task_id': 14099030, 'topic_id': 3179, 'task_type': 'review',
                 'review_sequence': 'CWCWC', 'knowledge_snapshots': {},
                 'questions': {
                     'q-108805': {'status': 'graded', 'actual_result': 'Correct', 'finalized': True},
                     'q-108839': {'status': 'graded', 'actual_result': 'Incorrect', 'finalized': True},
                     'q-149711': {'status': 'submitting', 'decision': {'answers': [
                         {'key': 'selection', 'correct_value': 'source answer'}]}}
                 }}
        reader = browser.CaptureBrowser.__new__(browser.CaptureBrowser)
        reader.args = SimpleNamespace()
        reader.page = Mock()
        reader.page.url = browser.LEARN
        card = Mock()
        card.is_visible.return_value = True
        card.evaluate.return_value = dict(kind='review', topic='/topics/3179', points='2/4 XP')
        rows = Mock()
        # Simulated fresh history response; the saved dashboard lacks the final grade.
        grades = [dict(id=k.replace('q-', 'question-'), result=v.get('actual_result', 'Correct'))
                  for k, v in state['questions'].items()]
        rows.evaluate_all.return_value = grades
        reader.page.locator.side_effect = lambda selector: card if selector.startswith('#completedTasks') else rows
        reader.navigate = Mock()
        reader.pacer = Mock()
        reader.wait_activity_ready = Mock(side_effect=TimeoutError('original readiness timeout'))
        reader.read_history = Mock(return_value=({'worked_solution':'Simulated fresh explanation', 'errors':[]}, None))
        reader.finalize_question = Mock(side_effect=lambda s, d, m, r: r.update(finalized=True))
        reader.knowledge_snapshot = Mock()
        return reader, state, rows, grades

    def run_activity(self, reader, state):
        with patch.object(browser, 'atomic_json'), patch.object(browser, 'by_id', return_value=Mock()):
            reader.activity(state, self.directory, {})

    def test_recover_without_submission_or_solver_reset(self):
        reader, state, rows, grades = self.setup_reader()
        decision = copy.deepcopy(state['questions']['q-149711']['decision'])
        self.run_activity(reader, state)
        self.assertTrue(state['activity_complete'])
        self.assertEqual(state['earned_xp'], 2)
        self.assertEqual(state['activity_outcome'], 'passed')
        self.assertEqual(state['questions']['q-149711']['decision'], decision)
        reader.finalize_question.assert_called_once()
        reader.wait_activity_ready.assert_not_called()
        reader.knowledge_snapshot.assert_called_once()

    def test_wrong_history_and_grade_conflict_rejected(self):
        for variant in ('missing', 'conflict'):
            reader, state, rows, grades = self.setup_reader()
            original = copy.deepcopy(state)
            if variant == 'missing':
                grades.pop()
            else:
                first = next(iter(state['questions']))
                grades[0]['result'] = 'Incorrect' if state['questions'][first]['actual_result'] == 'Correct' else 'Correct'
            with self.assertRaises(ValueError):
                self.run_activity(reader, state)
            self.assertEqual(state, original)
            reader.finalize_question.assert_not_called()
            reader.knowledge_snapshot.assert_not_called()

    def test_nonstring_url_keeps_ordinary_completion(self):
        reader, state, rows, grades = self.setup_reader()
        reader.page.url = Mock()
        for record in state['questions'].values():
            record.update(status='graded', finalized=True)
        reader.check = Mock()
        reader.wait_activity_ready = Mock()
        rows.is_visible.return_value = True
        rows.inner_text.return_value = 'You completed the review. You earned 2 XP.'
        self.run_activity(reader, state)
        self.assertTrue(state['activity_complete'])
        self.assertEqual(state['activity_outcome'], 'passed')
        reader.read_history.assert_not_called()

if __name__ == '__main__':
    unittest.main()
