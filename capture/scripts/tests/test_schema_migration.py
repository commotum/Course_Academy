"""Capture writes the rebuilt schema without changing presentation evidence."""
from copy import deepcopy
import unittest
import uuid

from scripts.database.edn import dumps
from scripts.database.evidence import authoritative_question
from scripts.database.prepare import ALLOWED, Plan, Preparation, source_uuid
from scripts.tests.test_database import question


class RemovedPresentationTests(unittest.TestCase):
    def prepare_question(self, captured, old=None):
        entities = [old, *old[':question/answer-fields'], *old[':question/answer-fields'][0][':answer-field/choices']] if old else []
        preparation = Preparation({'basis': 249, 'entities': entities,
            'idents': [[900, ':answer.type/math'], [901, ':answer-field.type/blank']]})
        plan = Plan(preparation.snapshot)
        preparation.question(plan, authoritative_question(captured), old, False)
        return plan.finish()

    def test_removed_attribute_is_rejected_and_never_emitted(self):
        self.assertNotIn('answer-field/presentation', ALLOWED)
        preparation = Preparation({'basis': 249})
        with self.assertRaisesRegex(ValueError, 'non-content attribute'):
            Plan(preparation.snapshot).set('field', None, 'answer-field/presentation', 'checkbox')
        captured = question()
        captured['answer_fields'][0]['presentation'] = 'checkbox'
        result = self.prepare_question(captured)
        self.assertNotIn(':answer-field/presentation', dumps(result))
        self.assertEqual(captured['answer_fields'][0]['presentation'], 'checkbox')

    def test_presentation_metadata_does_not_change_new_entity_identity(self):
        captured = question()
        original = self.prepare_question(captured)
        captured['answer_fields'][0]['presentation'] = 'checkbox'
        self.assertEqual(self.prepare_question(captured), original)

    def test_existing_field_and_answer_uuids_survive_presentation_only_differences(self):
        captured = question()
        captured.pop('difficulty')
        answer = {':db/id': 303, ':answer/id': uuid.UUID('00000000-0000-0000-0000-000000000303'),
                  ':answer/type': {':db/id': 900, ':db/ident': ':answer.type/math'}, ':answer/value': '2'}
        field = {':db/id': 202, ':answer-field/id': uuid.UUID('00000000-0000-0000-0000-000000000202'),
                 ':answer-field/key': 'x', ':answer-field/type': {':db/id': 901, ':db/ident': ':answer-field.type/blank'},
                 ':answer-field/choices': [answer], ':answer-field/correct': answer}
        old = {':db/id': 101, ':question/id': source_uuid('question', 'q-11'), ':question/math-academy-id': 'q-11',
               ':question/problem': captured['problem'], ':question/worked-solution': captured['worked_solution'],
               ':question/answer-fields': [field]}
        for stored, observed in ((None, 'checkbox'), ('checkbox', None), ('old-hint', 'new-hint')):
            with self.subTest(stored=stored, observed=observed):
                previous, fresh = deepcopy(old), deepcopy(captured)
                if stored is not None:
                    previous[':question/answer-fields'][0][':answer-field/presentation'] = stored
                if observed is not None:
                    fresh['answer_fields'][0]['presentation'] = observed
                result = self.prepare_question(fresh, previous)
                self.assertEqual(result['forms'], [])
                self.assertEqual(result['assertions'], [])
                self.assertEqual(result['retractions'], [])
                self.assertEqual(previous[':question/answer-fields'][0][':answer-field/id'], field[':answer-field/id'])
                self.assertEqual(previous[':question/answer-fields'][0][':answer-field/correct'][':answer/id'], answer[':answer/id'])


if __name__ == '__main__':
    unittest.main()
