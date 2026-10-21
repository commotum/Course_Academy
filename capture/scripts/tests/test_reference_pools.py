"""Reference pool content must never become historical activity attempts."""
from copy import deepcopy
import unittest
from scripts.database.prepare import Preparation
from scripts.database.batch import question_ids
from scripts.database.edn import dumps
from scripts.activity.evidence import capture_gaps
from scripts.tests.test_database import question, source_snapshot


class ReferencePoolTests(unittest.TestCase):
    def test_reference_answer_metadata_does_not_invent_a_history_solution(self):
        reference = question()
        reference.pop('worked_solution')
        self.assertEqual(capture_gaps({'reference_questions': [reference]}), [])
        gaps = capture_gaps({'questions': [reference]})
        self.assertIn('worked_solution', gaps[0]['missing'])

    def test_reference_question_completes_kp_without_changing_observed_order_or_sample(self):
        example, reference = question('e-20'), question('q-21')
        for q in (example, reference):
            q.update(knowledge_point_id='20', knowledge_point='A new source skill')
        sample = {'questions_by_knowledge_point': {}, 'selection': 'actual lesson observations'}
        content = {'questions': [], 'reference_questions': [reference], 'canonical_examples': [example],
                   'source_lesson_definitions': {'1': {'topic_id': 1, 'complete': True}},
                   'lesson_workload_sample': sample}
        original = deepcopy(content)
        result = Preparation(source_snapshot()).prepare(content)
        self.assertEqual(result['omissions'], [])
        self.assertEqual(result['content']['questions'], [])
        self.assertEqual(result['content']['question_order'], [])
        self.assertEqual(result['content']['lesson_workload_sample'], sample)
        self.assertEqual([q['math_academy_id'] for q in result['content']['reference_questions']], ['q-21'])
        self.assertIn(':knowledge-point/questions', dumps(result['batches']))
        self.assertNotIn(':activity/steps', dumps(result['batches']))
        self.assertEqual(question_ids(content), {'q-21', 'e-20'})
        self.assertEqual(content, original)

    def test_reference_duplicate_keeps_actual_observation_once(self):
        observed = question()
        content = {'questions': [observed], 'reference_questions': [deepcopy(observed)]}
        result = Preparation(source_snapshot()).prepare(content)
        self.assertEqual(result['omissions'], [])
        self.assertEqual(len(result['content']['questions']), 1)
        self.assertEqual(result['content']['reference_questions'], [])
        self.assertEqual(result['content']['question_order'], ['q-11'])

    def test_reference_question_still_requires_confirmed_answer_evidence(self):
        reference = question()
        reference['answer_fields'][0].pop('evidence')
        with self.assertRaisesRegex(ValueError, 'final capture judgment'):
            Preparation(source_snapshot()).prepare({'questions': [], 'reference_questions': [reference]})


if __name__ == '__main__':
    unittest.main()
