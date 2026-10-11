"""Real saved MA DOM -> checked activity answers -> new-schema EDN, entirely offline."""

from copy import deepcopy
from pathlib import Path
import unittest

from scripts.activity.evidence import finalize_answers, merge_question
from scripts.browser.adapter import EXTRACT
from scripts.browser.parsing import parse_history_metadata
from scripts.database.edn import dumps
from scripts.database.evidence import authoritative_question
from scripts.database.prepare import Preparation
from scripts.tests.test_database import source_snapshot


class SavedSourceIntegration(unittest.TestCase):
    def test_saved_live_choices_join_history_grade_and_prepare_full_answer_structure(self):
        from playwright.sync_api import sync_playwright
        fixtures = Path(__file__).parent / 'fixtures'
        [metadata] = parse_history_metadata((fixtures / 'review-history-question.html').read_text())
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                context = browser.new_context()
                context.route('**/*', lambda route: route.abort())
                page = context.new_page()
                page.set_content((fixtures / 'q-1396-before.html').read_text())
                live = page.locator('#step-q1396').evaluate(EXTRACT)
            finally:
                browser.close()
        correct = next(choice for choice in live['fields'][0]['choices'] if choice['option'] == 'c')
        self.assertEqual(correct['value'], '2j+4k')
        question = merge_question(live, {**metadata, 'html_path': str(fixtures / 'review-history-question.html'),
                                        'kp_id': str(metadata['knowledge_point_source_id'])})
        attempts = [{'key': 'step-q1396', 'feedback': metadata,
                     'submissions': [{'responses': [{'key': 'selection', 'value': correct['value'], 'option': 'c'}]}]}]
        # This test supplies the observed correct submission. An independent agent
        # judgment remains separate; it cannot manufacture the source answer.
        judgment = {'status': 'confirmed', 'reasoning': 'Cross product is 2j+4k.', 'answers': []}
        final = finalize_answers(question, attempts, judgment)
        checked = authoritative_question(final)
        self.assertEqual(checked['answer_fields'][0]['correct_value'], '2j+4k')
        self.assertEqual(len(checked['answer_fields'][0]['choices']), 5)
        self.assertEqual(checked['answer_fields'][0]['evidence']['kind'], 'ma_correct_grade')
        snapshot = source_snapshot()
        snapshot['entities'][0][':topic/math-academy-id'] = int(metadata['topic_id'])
        snapshot['entities'][1][':knowledge-point/title'] = metadata['knowledge_point']
        snapshot['entities'][1][':knowledge-point/canonical-example'][':question/math-academy-id'] = 'e-' + str(metadata['knowledge_point_source_id'])
        snapshot['entities'][2][':question/math-academy-id'] = 'e-' + str(metadata['knowledge_point_source_id'])
        plan = Preparation(snapshot).prepare({'kind': 'review', 'questions': [checked], 'judgments': [judgment]})
        edn = dumps(plan['batches'][0]['forms'])
        self.assertIn(':question/math-academy-id "q-1396"', edn)
        self.assertIn(':answer-field/correct', edn)
        self.assertIn(':knowledge-point/questions', edn)
        self.assertEqual(plan['omissions'], [])


if __name__ == '__main__':
    unittest.main()
