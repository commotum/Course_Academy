"""Fresh server task IDs must survive historical topic capture after placement."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from capture import arguments, observe_queue


def lesson(task=14073429, topic=803, **changes):
    return dict(task_id=task, topic_id=topic, task_type='lesson', title='Parametric curves',
        card_id='task-'+str(task), start_id='taskStartButton-'+str(task),
        href='/tasks/%s/topics/%s/lesson' % (task,topic), capture_supported=True,
        progress=0, in_progress=False, **changes)


class ReassignedQueueTests(unittest.TestCase):
    def observe(self, queue, captured=(), outcomes=()):
        with tempfile.TemporaryDirectory() as temporary:
            args = arguments(['run','--state-dir',temporary])
            browser = SimpleNamespace(queue=lambda:queue,completed_outcomes=list(outcomes))
            database = Mock()
            database.priorities.return_value = {803:1328,232:708,773:1,730:1,1106:1}
            with patch('capture.previous_activity_snapshot',return_value=None):
                result = observe_queue(args,database,browser,{803,232,773,730,1106},set(captured))
            self.assertEqual(result,json.loads((Path(temporary)/'selection/queue.json').read_text(),
                object_hook=lambda d:{int(k) if k.isdecimal() else k:v for k,v in d.items()}))
            return result

    def test_all_five_methods_assignments_are_eligible(self):
        queue = [lesson(task,topic) for task,topic in
            [(14071098,773),(14071101,730),(14073429,803),(14073808,232),(14073957,1106)]]
        result = self.observe(queue)
        self.assertEqual(result['selected']['task_id'],14073429)
        self.assertEqual(len(result['reassigned_lessons']),5)

    def test_already_captured_task_stays_excluded(self):
        self.assertIsNone(self.observe([lesson()],captured=[14073429])['selected'])

    def test_server_completed_same_task_stays_excluded(self):
        self.assertIsNone(self.observe([lesson()],outcomes=[dict(task_id=14073429,
            task_type='lesson',topic_id=803,earned_xp=5)])['selected'])

    def test_missing_or_changed_unlock_evidence_stays_excluded(self):
        for changes in [dict(in_progress=True),dict(progress=1),dict(capture_supported=False),
                dict(card_id='taskLocked-14073429'),dict(start_id=None),dict(href=None),
                dict(href='/tasks/14073428/topics/803/lesson'),dict(href='/tasks/14073429/topics/232/lesson')]:
            with self.subTest(changes=changes):
                item=lesson();item.update(changes)
                self.assertIsNone(self.observe([item])['selected'])

    def test_same_topic_ambiguous_row_does_not_receive_exception(self):
        ambiguous=lesson(14070000);ambiguous['href']=None
        result=self.observe([ambiguous,lesson()])
        self.assertEqual(result['selected']['task_id'],14073429)
        self.assertEqual([i['task_id'] for i in result['reassigned_lessons']],[14073429])

    def test_review_retains_normal_selection_without_lesson_override(self):
        review=lesson();review['task_type']='review'
        result=self.observe([review])
        self.assertEqual(result['selected']['task_type'],'review')
        self.assertEqual(result['reassigned_lessons'],[])

    def test_inprogress_nonlesson_stays_excluded(self):
        review=lesson();review.update(task_type='review',in_progress=True)
        self.assertIsNone(self.observe([review])['selected'])

    def test_required_assessment_still_precedes_reassigned_lesson(self):
        quiz=dict(task_id=2,topic_id=None,task_type='assessment',title='Quiz',
            capture_supported=True,in_progress=False,assessment_requirement='required')
        self.assertEqual(self.observe([lesson(),quiz])['selected']['task_id'],2)


if __name__ == '__main__':
    unittest.main()
