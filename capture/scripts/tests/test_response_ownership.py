"""A field identity revision must preserve historical response ownership."""
import copy
import json
import tempfile
import threading
import unittest

from scripts.database.edn import kw
from scripts.database.evidence import UnsupportedContent
from scripts.database.pipeline import DatabasePipeline
from scripts.database.prepare import Plan, Preparation, source_uuid
from scripts.storage import atomic_json
from scripts.tests import test_database as database_tests
from scripts.tests.test_database import FakeClient, question, source_snapshot


def duplicate_fields(kind, *, referenced=True):
    fields = []
    for eid in (10, 11):
        choices = [{':db/id': eid * 10 + index, ':answer/id': source_uuid('answer', eid * 10 + index),
                    ':answer/type': {':db/ident': kw('answer.type/math')}, ':answer/value': value}
                   for index, value in enumerate(('2', '3'))]
        if referenced and eid == 11:
            choices[0][':task-item/_responses'] = [{':db/id': 30}]
        fields.append({':db/id': eid, ':answer-field/id': source_uuid('field', eid),
            ':answer-field/key': 'x', ':answer-field/type': {':db/ident': kw('answer-field.type/' + kind)},
            ':answer-field/choices': choices, ':answer-field/correct': choices[0]})
    return fields


class ResponseOwnershipTests(unittest.TestCase):
    def test_referenced_duplicate_exact_fields_are_refused_before_plan_mutation(self):
        for kind in ('blank', 'radio', 'select'):
            with self.subTest(kind=kind):
                old = {':db/id': 5, ':question/id': source_uuid('question', 5),
                       ':question/answer-fields': duplicate_fields(kind)}
                q = question()
                q['answer_fields'][0].update(type=kind, correct_type='math',
                    choices=[{'type': 'math', 'value': v} for v in ('2', '3')])
                prep = Preparation(source_snapshot())
                plan = Plan(prep.snapshot)
                with self.assertRaisesRegex(UnsupportedContent, 'ambiguous historical response ownership'):
                    prep.question(plan, q, old, False)
                self.assertEqual(plan.finish(), {'source': ':org/Math-Academy', 'forms': [],
                                                 'assertions': [], 'retractions': []})

    def test_duplicate_fields_without_responses_keep_conditional_identity_resolution(self):
        old = {':db/id': 5, ':question/id': source_uuid('question', 5),
               ':question/answer-fields': duplicate_fields('radio', referenced=False)}
        q = question(answer='3')
        q['answer_fields'][0].update(type='radio', correct_type='math',
            choices=[{'type': 'math', 'value': v} for v in ('2', '3')])
        calls = []
        def resolve(operation, payload):
            calls.append((operation, payload))
            return {'decision': 'existing', 'entity_id': 10, 'evidence': 'Continuing source field x.'}
        prep = Preparation(source_snapshot(), resolve=resolve)
        plan = Plan(prep.snapshot)
        prep.question(plan, q, old, False)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][0], 'resolve_identity')
        self.assertEqual(calls[0][1]['kind'], 'answer-field')
        self.assertEqual({c[':db/id'] for c in calls[0][1]['candidates']}, {10, 11})
        self.assertTrue(plan.finish()['forms'])

    def test_unobserved_duplicate_fields_in_partial_update_are_retained(self):
        old = {':question/answer-fields': duplicate_fields('blank')}
        q = question()
        q['answer_fields'][0]['key'] = 'y'
        Preparation(source_snapshot()).check_response_ownership(q, old)

    def test_ambiguous_owned_field_revision_is_terminal_and_sibling_import_settles(self):
        class DuplicateClient(FakeClient):
            inject_duplicates = False
            def snapshot(self, *args):
                result = super().snapshot(*args)
                if self.inject_duplicates:
                    for entity in result['entities']:
                        if entity.get(':question/math-academy-id') == 'q-11':
                            duplicate = copy.deepcopy(entity[':question/answer-fields'][0])
                            duplicate.update({':db/id': 99990, ':answer-field/id': source_uuid('field', 99990)})
                            for answer in duplicate[':answer-field/choices']:
                                answer.update({':db/id': 99991, ':answer/id': source_uuid('answer', 99991),
                                               ':task-item/_responses': [{':db/id': 99992}]})
                            entity[':question/answer-fields'].append(duplicate)
                return result
        with tempfile.TemporaryDirectory() as directory:
            capture, config = database_tests.PipelineTests().setup(directory)
            client = DuplicateClient()
            pipeline = DatabasePipeline(config, threading.Event(), client=client)
            self.assertEqual(pipeline.process(capture)['status'], 'verified')
            client.inject_duplicates = True
            content = json.loads((capture / 'content.json').read_text())
            original = content['questions'][0]
            original['problem'] = 'A revision with ambiguous field ownership.'
            sibling = question('q-12')
            sibling['knowledge_point_id'] = original['knowledge_point_id']
            content['questions'].append(sibling)
            atomic_json(capture / 'content.json', content)
            result = pipeline.process(capture)
            self.assertEqual(result['status'], 'verified', result)
            self.assertEqual(len(result['omissions']), 1)
            self.assertEqual(result['omissions'][0]['constraint'], 'historical_response_ownership')
            self.assertIn('ambiguous historical response ownership', result['omissions'][0]['reason'])
            self.assertTrue(result['omissions'][0]['final'])
            self.assertEqual(pipeline.process(capture)['status'], 'no_changes')
            self.assertIn('q-12', {value for (eid, attr), values in client.facts.items()
                                  if attr == 'question/math-academy-id' for value, source in values})
            self.assertFalse(any(value == original['problem'] for (eid, attr), values in client.facts.items()
                                 if attr == 'question/problem' for value, source in values))


if __name__ == '__main__':
    unittest.main()
