"""Recapture fills absent components and preserves every captured component."""
import copy
import unittest

from scripts.database.edn import kw
from scripts.database.evidence import authoritative_question
from scripts.database.prepare import Plan, Preparation, source_uuid
from scripts.tests.test_database import question, source_snapshot


def captured_snapshot(*, kind='blank'):
    data = source_snapshot()
    answers = [{':db/id': eid, ':answer/id': source_uuid('answer', eid),
                ':answer/type': {':db/ident': kw('answer.type/math')}, ':answer/value': value}
               for eid, value in ((20, '2'), (21, '3'))]
    field = {':db/id': 10, ':answer-field/id': source_uuid('field', 10),
             ':answer-field/key': 'x', ':answer-field/type': {':db/ident': kw('answer-field.type/' + kind)},
             ':answer-field/choices': answers, ':answer-field/correct': answers[0]}
    old = {':db/id': 5, ':question/id': source_uuid('question', 5),
           ':question/math-academy-id': 'q-11', ':question/problem': question()['problem'],
           ':question/difficulty': {':db/ident': kw('question.difficulty/easy')},
           ':question/requires-calculator': False, ':question/worked-solution': 'Retained solution.',
           ':question/answer-fields': [field]}
    data['entities'].extend([old, field, *answers])
    data['entities'][1][':knowledge-point/questions'] = [old]
    return data, old, field


def plan_question(data, old, incoming=None):
    incoming = incoming or question()
    prep = Preparation(data)
    plan = Plan(prep.snapshot)
    prep.question(plan, authoritative_question(incoming), old, False)
    return plan.finish()


class CaptureFillOnlyTests(unittest.TestCase):
    def test_complete_capture_ignores_invalid_recapture_and_preserves_owner(self):
        data, old, _ = captured_snapshot()
        original = question()
        original.update(problem=r'$\matrix{$', difficulty='H', answer_fields=[],
                        knowledge_point='A stale title', answer_fields_complete=False)
        before = copy.deepcopy(original)
        prepared = Preparation(data).prepare({'questions': [original]})
        self.assertEqual(prepared['batches'], [])
        self.assertEqual(prepared['omissions'], [])
        self.assertEqual(prepared['preserved_captures'], ['q-11'])
        self.assertEqual(prepared['content']['questions'][0]['problem'], old[':question/problem'])
        self.assertEqual(prepared['content']['questions'][0]['worked_solution'], 'Retained solution.')
        self.assertEqual(prepared['content']['questions'][0]['knowledge_point'], 'Addition')
        self.assertEqual(original, before)

    def test_missing_solution_alone_does_not_reopen_capture(self):
        data, old, _ = captured_snapshot()
        old.pop(':question/worked-solution')
        prepared = Preparation(data).prepare({'questions': [question()]})
        self.assertEqual(prepared['batches'], [])
        self.assertNotIn('worked_solution', prepared['content']['questions'][0])

    def test_missing_difficulty_fills_only_difficulty(self):
        data, old, _ = captured_snapshot()
        old.pop(':question/difficulty')
        original = question(answer='99')
        original.update(problem='Revised source wording.', requires_calculator=True)
        batch = plan_question(data, old, original)
        self.assertEqual(batch['assertions'], [[5, kw('question/difficulty'), kw('question.difficulty/easy')]])
        self.assertEqual(batch['retractions'], [])

    def test_missing_difficulty_does_not_reopen_existing_kp_ownership(self):
        for reverse_only in (False, True):
            with self.subTest(reverse_only=reverse_only):
                data, old, _ = captured_snapshot()
                old.pop(':question/difficulty')
                owner = data['entities'][1]
                if reverse_only:
                    owner.pop(':knowledge-point/questions')
                    old[':knowledge-point/_questions'] = [{':db/id': owner[':db/id']}]
                other = {':db/id': 7, ':knowledge-point/id': source_uuid('kp', 7),
                         ':knowledge-point/title': 'Other captured skill', ':knowledge-point/questions': []}
                data['entities'].append(other)
                data['entities'][0][':topic/knowledge-points'].append(other)
                incoming = question()
                incoming.update(knowledge_point_id=str(other[':knowledge-point/id']), knowledge_point='Revised title')
                prepared = Preparation(data).prepare({'questions': [incoming]})
                assertions = [row for batch in prepared['batches'] for row in batch['assertions']]
                self.assertEqual(assertions, [[5, kw('question/difficulty'), kw('question.difficulty/easy')]])
                self.assertFalse(any(batch['retractions'] for batch in prepared['batches']))

    def test_missing_entire_field_structure_is_filled_without_other_revisions(self):
        data, old, _ = captured_snapshot()
        old.pop(':question/answer-fields')
        original = question()
        original.update(difficulty='H', requires_calculator=True, worked_solution='New source solution.')
        batch = plan_question(data, old, original)
        self.assertTrue(any(row[1] == ':question/answer-fields' for row in batch['assertions']))
        self.assertTrue(any(row[1] == ':answer-field/correct' for row in batch['assertions']))
        self.assertFalse(any(row[0] == 5 and row[1] != ':question/answer-fields' for row in batch['assertions']))
        self.assertEqual(batch['retractions'], [])

    def test_missing_correct_reuses_retained_owned_answer_without_rewriting_it(self):
        data, old, field = captured_snapshot()
        field.pop(':answer-field/correct')
        field[':answer-field/choices'][0][':task-item/_responses'] = [{':db/id': 30}]
        batch = plan_question(data, old)
        self.assertEqual(batch['assertions'], [[10, kw('answer-field/correct'), 20]])
        self.assertEqual(batch['retractions'], [])

    def test_missing_correct_requires_agreement_with_retained_radio_bank(self):
        for source_values in (('2', '3'), ('2', '4')):
            data, old, field = captured_snapshot(kind='radio')
            field.pop(':answer-field/correct')
            original = question()
            original['answer_fields'][0].update(type='radio', choices=[{'type': 'math', 'value': v} for v in source_values])
            batch = plan_question(data, old, original)
            self.assertEqual(batch['assertions'], [[10, kw('answer-field/correct'), 20]] if source_values == ('2', '3') else [])
            self.assertEqual(batch['retractions'], [])

    def test_missing_correct_is_not_guessed_among_duplicate_stored_answers(self):
        data, old, field = captured_snapshot()
        field.pop(':answer-field/correct')
        field[':answer-field/choices'][1][':answer/value'] = '2'
        self.assertEqual(plan_question(data, old)['forms'], [])

    def test_populated_field_collection_is_not_extended(self):
        data, old, field = captured_snapshot()
        old.pop(':question/difficulty')
        original = question()
        extra = copy.deepcopy(original['answer_fields'][0])
        extra['key'] = 'y'
        original['answer_fields'].append(extra)
        batch = plan_question(data, old, original)
        self.assertEqual(batch['assertions'], [[5, kw('question/difficulty'), kw('question.difficulty/easy')]])
        self.assertEqual(batch['retractions'], [])

    def test_missing_field_type_can_be_filled_from_matching_bank(self):
        data, old, field = captured_snapshot(kind='radio')
        field.pop(':answer-field/type')
        original = question()
        original['answer_fields'][0].update(type='radio', choices=[{'type': 'math', 'value': v} for v in ('2', '3')])
        batch = plan_question(data, old, original)
        self.assertEqual(batch['assertions'], [[10, kw('answer-field/type'), kw('answer-field.type/radio')]])
        self.assertEqual(batch['retractions'], [])

    def test_missing_choice_bank_keeps_field_and_existing_correct_identity(self):
        data, old, field = captured_snapshot(kind='radio')
        field.pop(':answer-field/choices')
        original = question()
        original['answer_fields'][0].update(type='radio', choices=[{'type': 'math', 'value': v} for v in ('2', '3')])
        batch = plan_question(data, old, original)
        self.assertIn([10, kw('answer-field/choices'), 20], batch['assertions'])
        self.assertFalse(any(row[0] == 20 or row[1] == ':answer-field/correct' for row in batch['assertions']))
        self.assertEqual(batch['retractions'], [])

    def test_changed_source_problem_cannot_supply_a_missing_key(self):
        data, old, field = captured_snapshot()
        field.pop(':answer-field/correct')
        original = question()
        original['problem'] = 'A distinct revision.'
        self.assertEqual(plan_question(data, old, original)['forms'], [])

    def test_preserved_canonical_still_resolves_new_practice_source_kp(self):
        data = source_snapshot()
        example, practice = question('e-10'), question('q-12')
        for original in (example, practice):
            original['knowledge_point_id'] = 'source-kp-1'
            original.pop('knowledge_point')
        prepared = Preparation(data).prepare({'canonical_examples': [example], 'questions': [practice]})
        self.assertEqual(prepared['omissions'], [])
        self.assertEqual(prepared['content']['questions'][0]['knowledge_point_id'], str(data['entities'][1][':knowledge-point/id']))
        self.assertEqual(prepared['preserved_captures'], ['e-10'])

    def test_missing_source_id_still_gets_source_judgment_not_identity_resolution(self):
        calls = []
        def resolve(operation, payload):
            calls.append(operation)
            return {'status': 'unavailable', 'reasoning': 'Source identity is unavailable', 'answers': []}
        prepared = Preparation(source_snapshot(), resolve=resolve).prepare({'questions': [{'problem': 'Unidentified source'}]})
        self.assertEqual(calls, ['judge_question'])
        self.assertEqual(prepared['batches'], [])

    def test_complete_canonical_cannot_be_reintroduced_as_practice(self):
        data, old, _ = captured_snapshot()
        data['entities'][1][':knowledge-point/canonical-example'] = old
        prepared = Preparation(data).prepare({'questions': [question()]})
        self.assertEqual(prepared['batches'], [])
        self.assertEqual(prepared['omissions'][0]['reason'], 'Canonical example cannot enter a practice pool')

    def test_preserved_questions_remain_in_workload_sample_and_activity_refs(self):
        data, old, field = captured_snapshot()
        another = copy.deepcopy(old)
        another.update({':db/id': 6, ':question/id': source_uuid('question', 6), ':question/math-academy-id': 'q-12'})
        data['entities'].append(another)
        data['entities'][1][':knowledge-point/questions'].append(another)
        content = {'task_type': 'lesson', 'base_xp': 7, 'topic_id': 1,
                   'lesson_definition': {'complete': True, 'steps': [{'type': 'example', 'content_id': 10}]},
                   'questions': [question(), question('q-12')], 'canonical_examples': [question('e-10')]}
        prepared = Preparation(data).prepare(content)
        self.assertIn('multiplier', prepared['calibration'])
        self.assertEqual(set(prepared['preserved_captures']), {'q-11', 'q-12', 'e-10'})
        self.assertEqual(prepared['omissions'], [])
        content.update(task_type='review', question_order=['q-11', 'q-12'])
        prepared = Preparation(data).prepare(content)
        self.assertEqual(prepared['omissions'], [])
        refs = {row[2] for batch in prepared['batches'] for row in batch['assertions'] if row[1] == ':step/content'}
        self.assertTrue({5, 6}.issubset(refs))

    def test_recapture_keeps_separately_authored_tutorial_correction(self):
        data, _, _ = captured_snapshot()
        tutorial = {':db/id': 40, ':tutorial/id': source_uuid('tutorial', 40),
                    ':tutorial/math-academy-id': 30, ':tutorial/title': 'Introduction',
                    ':tutorial/content': r'Corrected $\begin{bmatrix}1 & 2\end{bmatrix}$.'}
        data['entities'].append(tutorial)
        data['idents'].append([950, kw('application/ca-engine')])
        data['facts'] = [[40, attr[1:], value, 950 if attr == ':tutorial/content' else 900]
                         for attr, value in tutorial.items() if attr != ':db/id']
        incoming = {'questions': [question()], 'topic_id': 1,
                    'lesson_definition': {'complete': True, 'steps': [{'type': 'tutorial', 'content_id': 30}]},
                    'tutorials': [{'math_academy_id': 30, 'title': 'Introduction', 'content': r'$\matrix{$'}]}
        prepared = Preparation(data).prepare(incoming)
        self.assertEqual(prepared['omissions'], [])
        assertions = [row for batch in prepared['batches'] for row in batch['assertions']]
        self.assertFalse(any(row[0] == 40 for row in assertions))
        self.assertTrue(any(row[1] == ':step/content' and row[2] == 40 for row in assertions))
        self.assertEqual(prepared['content']['tutorials'][0]['content'], tutorial[':tutorial/content'])


if __name__ == '__main__':
    unittest.main()
