"""Source-bound legacy blank to radio presentation migration for q-87562."""
import copy
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from core import build_transaction
from database import Database
from edn import kw, loads
from provenance import Reconciler, source_records

FIXTURE = Path(__file__).parent / 'fixtures/single-answer-widget'


class SingleAnswerWidgetTests(unittest.TestCase):
    def setUp(self):
        self.content = json.loads((FIXTURE / 'content.json').read_text())
        self.q = self.content['questions'][0]
        self.mid = self.q['math_academy_id']
        self.old = loads((FIXTURE / 'previous-question.edn').read_text())[0][0]
        self.sources = source_records(self.content, FIXTURE)
        self.usage = {self.mid: []}
        self.no_history = []
        self.authored = []
        self.topic = {':topic/math-academy-id': self.content['topic_id'], ':topic/knowledge-points': [
            {':knowledge-point/id': self.old[':knowledge-point/_questions'][0][':knowledge-point/id'],
             ':knowledge-point/title': self.q['knowledge_point'],
             ':knowledge-point/questions': [{':question/math-academy-id': self.mid}]}]}

    def plan(self):
        old, content = copy.deepcopy(self.old), copy.deepcopy(self.content)
        self.reconciler = Reconciler(self.authored, self.sources, 2700, self.usage, self.no_history)
        tx, _ = build_transaction(self.content, self.topic, {self.mid: self.old}, self.reconciler)
        self.assertEqual(self.old, old)
        self.assertEqual(self.content, content)
        return tx

    def test_authentic_single_answer_versions_ownership_and_preserves_original_entities(self):
        tx = self.plan()
        field = self.old[':question/answer-fields'][0]
        self.assertIn([kw('db/retract'), self.old[':db/id'], kw('question/answer-fields'), field[':db/id']], tx)
        new_fields = [m for m in tx if isinstance(m, dict) and ':answer-field/id' in m]
        self.assertEqual(len(new_fields), 1)
        new = new_fields[0]
        self.assertIn('/ma-layout-v1/', new[':db/id'])
        self.assertNotEqual(new[':answer-field/id'], field[':answer-field/id'])
        self.assertEqual(new[':answer-field/key'], 'selection')
        self.assertEqual(new[':answer-field/type'], kw('answer-field.type/radio'))
        self.assertEqual([m[':answer/value'] for m in tx if isinstance(m, dict) and ':answer/value' in m],
                         ['2', '7', '6', '4', '3'])
        self.assertFalse(any(isinstance(m, dict) and m[':db/id'] in
                             (field[':db/id'], field[':answer-field/correct'][':db/id']) for m in tx))
        self.assertEqual(field[':answer-field/key'], 'answer')
        self.assertEqual(field[':answer-field/correct'][':answer/value'], '4')
        self.assertFalse(self.reconciler.needs_review)
        self.assertIn([self.old[':db/id'], kw('question/answer-fields'), field[':db/id']],
                      Database(SimpleNamespace()).replacement_guards(self.reconciler, {self.mid: self.old}))

    def test_repeat_import_is_noop(self):
        tx = self.plan()
        field = next(m for m in tx if isinstance(m, dict) and ':answer-field/id' in m)
        answers = {m[':db/id']: m for m in tx if isinstance(m, dict) and ':answer/value' in m}
        installed = {str(k): v for k, v in field.items() if k != kw('db/ensure')}
        installed[':answer-field/type'] = {':db/ident': installed[':answer-field/type']}
        for a in answers.values():
            a[':answer/type'] = {':db/ident': a[':answer/type']}
        installed[':answer-field/choices'] = [answers[a] for a in field[':answer-field/choices']]
        installed[':answer-field/correct'] = answers[field[':answer-field/correct']]
        self.old[':question/answer-fields'] = [installed]
        self.old[':question/problem'] = self.q['problem']
        self.assertEqual(self.plan(), [])

    def test_each_source_requirement_is_independent(self):
        for category in ('ma_capture', 'ma_widget', 'ma_complete_choices', 'ma_successful_grade'):
            with self.subTest(category=category):
                before = self.sources
                self.sources = [r for r in before if r['category'] != category]
                with self.assertRaisesRegex(ValueError, 'omitted existing fields'):
                    self.plan()
                self.sources = before

    def test_missing_parts_and_incompatible_widgets_still_reject(self):
        for mutation in ('old_multipart', 'new_multipart', 'select', 'blank', 'nonselection', 'old_radio'):
            with self.subTest(mutation=mutation):
                self.setUp()
                f = self.old[':question/answer-fields'][0]
                if mutation == 'old_multipart':
                    self.old[':question/answer-fields'].append({**f, ':db/id': 99, ':answer-field/key': 'second'})
                elif mutation == 'new_multipart':
                    self.q['answer_fields'].append({**self.q['answer_fields'][0], 'key': 'second'})
                elif mutation == 'old_radio':
                    f[':answer-field/type'][':db/ident'] = kw('answer-field.type/select')
                elif mutation == 'nonselection':
                    self.q['answer_fields'][0]['key'] = 'other'
                else:
                    self.q['answer_fields'][0]['type'] = mutation
                with self.assertRaisesRegex(ValueError, 'omitted existing fields'):
                    self.plan()

    def test_prompt_and_correct_value_must_match_even_with_source_evidence(self):
        for mutation in ('stem', 'footer_key', 'extra_placeholder', 'correct', 'type'):
            with self.subTest(mutation=mutation):
                self.setUp()
                if mutation == 'stem':
                    self.old[':question/problem'] = self.old[':question/problem'].replace('117', '118')
                elif mutation == 'footer_key':
                    self.old[':question/problem'] = self.old[':question/problem'].replace('{{answer}}', '{{second}}')
                elif mutation == 'extra_placeholder':
                    self.old[':question/problem'] = '{{second}}\n' + self.old[':question/problem']
                elif mutation == 'correct':
                    self.old[':question/answer-fields'][0][':answer-field/correct'][':answer/value'] = '3'
                else:
                    self.old[':question/answer-fields'][0][':answer-field/correct'][':answer/type'][':db/ident'] = kw('answer.type/text')
                with self.assertRaisesRegex(ValueError, 'omitted existing fields'):
                    self.plan()

    def test_unresolved_equivalence_does_not_authorize_migration(self):
        with patch('core.compare_answers', return_value={'outcome': 'unresolved'}):
            with self.assertRaisesRegex(ValueError, 'omitted existing fields'):
                self.plan()

    def test_usage_retention_and_mathematical_corrections_remain_guarded(self):
        for mutation in ('unchecked', 'presented', 'responded', 'no_history', 'correction'):
            with self.subTest(mutation=mutation):
                self.setUp()
                if mutation == 'unchecked': self.usage = {}
                elif mutation in ('presented', 'responded'): self.usage[self.mid] = [{'kind': mutation, 'entity': 99}]
                elif mutation == 'no_history': self.no_history = [kw('question/answer-fields')]
                else: self.authored = [{'question': self.mid, 'field': None,
                    'attribute': 'question/problem', 'value': self.old[':question/problem'],
                    'category': 'mathematical_correction'}]
                with self.assertRaisesRegex(ValueError, 'omitted existing fields'):
                    self.plan()


if __name__ == '__main__':
    unittest.main()
