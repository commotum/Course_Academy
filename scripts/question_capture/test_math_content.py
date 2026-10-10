"""Source-aware content plans tested against native EDB pull-shaped fixtures."""
import copy
import unittest
import uuid

from core import stable_id
from edn import kw
from math_content import build_math_content, resolve_knowledge_points


class MathContentTests(unittest.TestCase):
    def setUp(self):
        # Deliberately differ from the old capture UUID generator: migration
        # already established these identities and must remain authoritative.
        self.kp = uuid.UUID('1652eebf-b779-5f49-80cf-530bc3257006')
        self.qid = uuid.UUID('18784448-1521-4ae0-8759-c0576efc4d7a')
        self.field_id = uuid.UUID('a091b737-5527-4e6c-af4a-4de0cbe97282')
        self.answers = [
            {':db/id':201, ':answer/id':uuid.UUID('9bbf9e83-d8b8-4661-9c9c-520ba26914bf'),
             ':answer/type':{':db/ident':kw('answer.type/math')}, ':answer/value':'120'},
            {':db/id':202, ':answer/id':uuid.UUID('26b05999-3ead-4898-8c49-e91054b15a8a'),
             ':answer/type':{':db/ident':kw('answer.type/math')}, ':answer/value':'25'}]
        self.field = {':db/id':200, ':answer-field/id':self.field_id,
                      ':answer-field/key':'selection',
                      ':answer-field/type':{':db/ident':kw('answer-field.type/radio')},
                      ':answer-field/choices':self.answers,
                      ':answer-field/correct':self.answers[0]}
        self.old = {':db/id':100, ':question/id':self.qid, ':question/math-academy-id':'q-5370',
                    ':question/problem':'Evaluate $5!$.',
                    ':question/worked-solution':'$5!=120$.',
                    ':question/difficulty':{':db/id':99, ':db/ident':kw('question.difficulty/easy')},
                    ':question/answer-fields':[self.field],
                    ':knowledge-point/_questions':[{':knowledge-point/id':self.kp}]}
        self.point = {':db/id':300, ':knowledge-point/id':self.kp,
                      ':knowledge-point/title':'Evaluating Factorials',
                      ':knowledge-point/canonical-example':{
                          ':db/id':101, ':question/math-academy-id':'e-1234'},
                      ':knowledge-point/questions':[{
                          ':db/id':100, ':question/math-academy-id':'q-5370'}]}
        self.topics = {774:{':db/id':400, ':topic/math-academy-id':774,
                            ':topic/knowledge-points':[self.point]}}
        self.question = {'math_academy_id':'q-5370', 'knowledge_point_id':str(self.kp),
                         'knowledge_point':'Evaluating Factorials', 'topic_id':774,
                         'problem':self.old[':question/problem'],
                         'worked_solution':self.old[':question/worked-solution'], 'difficulty':'easy',
                         'answer_fields':[{'key':'selection', 'type':'radio', 'correct_value':'120',
                             'choices':[{'type':'math','value':'25'}, {'type':'math','value':'120'}]}]}
        self.content = {'task_type':'review', 'topic_id':774,
                        'questions':[self.question], 'canonical_examples':[]}
        self.existing = {'q-5370':self.old}

    def plan(self):
        before = copy.deepcopy((self.content, self.topics, self.existing))
        planned = build_math_content(self.content, self.topics, self.existing)
        self.assertEqual((self.content, self.topics, self.existing), before)
        return planned

    def test_existing_identity_and_answer_choices_are_a_noop(self):
        self.assertNotEqual(self.qid, stable_id('question', 'q-5370'))
        transaction, guards = self.plan()
        self.assertEqual(transaction, [])
        self.assertEqual(guards['retractions'], [])

    def test_changed_source_body_updates_existing_uuid_and_plans_prior_value_retraction(self):
        self.question['worked_solution'] = 'Expanded explanation: $5!=5(4)(3)(2)(1)=120$.'
        transaction, guards = self.plan()
        self.assertEqual(len(transaction), 1)
        self.assertEqual(transaction[0][':db/id'], [kw('question/id'), self.qid])
        self.assertEqual(transaction[0][':question/worked-solution'], self.question['worked_solution'])
        self.assertNotIn(':question/id', transaction[0])
        self.assertEqual(guards['retractions'], [
            [100, kw('question/worked-solution'), '$5!=120$.']])

    def test_source_correct_answer_revision_replaces_field_ownership_without_mutating_components(self):
        self.question['answer_fields'][0]['correct_value'] = '25'
        transaction, guards = self.plan()
        self.assertIn([kw('db/retract'), 100, kw('question/answer-fields'), 200], transaction)
        self.assertEqual(guards['retractions'], [[100, kw('question/answer-fields'), 200]])
        created_answers = {item[':db/id']:item for item in transaction
                           if isinstance(item, dict) and ':answer/value' in item}
        new_field = next(item for item in transaction
                         if isinstance(item, dict) and ':answer-field/id' in item)
        self.assertNotEqual(new_field[':answer-field/id'], self.field_id)
        self.assertEqual(created_answers[new_field[':answer-field/correct']][':answer/value'], '25')
        question_update = next(item for item in transaction
                               if isinstance(item, dict) and ':question/answer-fields' in item)
        self.assertEqual(question_update[':db/id'], [kw('question/id'), self.qid])
        self.assertEqual(question_update[':question/answer-fields'], [new_field[':db/id']])
        self.assertFalse(any(isinstance(item, dict) and item[':db/id'] in (200, 201, 202)
                             for item in transaction))
        # Database pull after this planned ownership change must reconcile to
        # no work, independent of transaction-local tempids or entity numbers.
        answers = {key:{':db/id':500+i, ':answer/id':item[':answer/id'],
                    ':answer/type':{':db/ident':item[':answer/type']}, ':answer/value':item[':answer/value']}
                   for i,(key,item) in enumerate(created_answers.items())}
        self.old[':question/answer-fields'] = [{':db/id':600,
            ':answer-field/id':new_field[':answer-field/id'],
            ':answer-field/key':new_field[':answer-field/key'],
            ':answer-field/type':{':db/ident':new_field[':answer-field/type']},
            ':answer-field/choices':[answers[key] for key in new_field[':answer-field/choices']],
            ':answer-field/correct':answers[new_field[':answer-field/correct']]}]
        self.assertEqual(self.plan()[0], [])

    def test_removed_field_is_explicitly_unlinked(self):
        second = copy.deepcopy(self.field)
        second.update({':db/id':205, ':answer-field/key':'old-extra', ':answer-field/id':uuid.uuid4()})
        self.old[':question/answer-fields'].append(second)
        transaction, guards = self.plan()
        self.assertEqual(transaction, [[kw('db/retract'),100,kw('question/answer-fields'),205]])
        self.assertEqual(guards['retractions'], [[100,kw('question/answer-fields'),205]])

    def test_examples_without_observed_fields_preserve_stored_fields_and_difficulty(self):
        example = copy.deepcopy(self.question)
        example.update(math_academy_id='e-1234', answer_fields=[], difficulty=None)
        self.content.update(questions=[], canonical_examples=[example])
        old = copy.deepcopy(self.old)
        old.update({':question/math-academy-id':'e-1234', ':knowledge-point/_questions':[],
                    ':knowledge-point/_canonical-example':[{':knowledge-point/id':self.kp}]})
        self.existing = {'e-1234':old}
        self.assertEqual(self.plan()[0], [])

    def test_matching_source_example_remaps_old_database_knowledge_point_uuid(self):
        stale = str(uuid.UUID('dc365fde-ac9b-43f8-990d-b9a2d1a84931'))
        self.question['knowledge_point_id'] = stale
        example = copy.deepcopy(self.question)
        example.update(math_academy_id='e-1234', answer_fields=[])
        self.content.update(task_type='lesson', canonical_examples=[example])
        before = copy.deepcopy(self.content)
        resolved = resolve_knowledge_points(self.content, self.topics, {})
        self.assertEqual(self.content, before)
        self.assertEqual(resolved['questions'][0]['knowledge_point_id'], str(self.kp))
        self.assertEqual(resolved['canonical_examples'][0]['knowledge_point_id'], str(self.kp))
        self.assertEqual(resolved['new_knowledge_points'], [])

    def test_title_match_reuses_existing_kp_before_declaring_new_one(self):
        stale = str(uuid.UUID('dc365fde-ac9b-43f8-990d-b9a2d1a84931'))
        self.question['knowledge_point_id'] = stale
        self.content['new_knowledge_points'] = [{
            'id':stale, 'title':'Evaluating Factorials', 'source_example_id':'e-9999'}]
        self.content['task_type'] = 'lesson'
        self.content['lesson_definition'] = {'complete':True}
        resolved = resolve_knowledge_points(self.content, self.topics, {})
        self.assertEqual(resolved['questions'][0]['knowledge_point_id'], str(self.kp))
        self.assertEqual(resolved['new_knowledge_points'], [])

    def test_unknown_kp_requires_complete_lesson_and_source_example(self):
        self.question['knowledge_point_id'] = str(uuid.uuid4())
        self.question['knowledge_point'] = 'New MA-authored skill'
        self.content.update(task_type='lesson', lesson_definition={'complete':True})
        with self.assertRaisesRegex(ValueError, 'Cannot resolve'):
            resolve_knowledge_points(self.content, self.topics, {})
        example = copy.deepcopy(self.question)
        example.update(math_academy_id='e-789', answer_fields=[])
        self.content['canonical_examples'] = [example]
        resolved = resolve_knowledge_points(self.content, self.topics, {})
        self.assertEqual(len(resolved['new_knowledge_points']), 1)
        expected = str(stable_id('knowledge-point', '774:e-789'))
        self.assertEqual(resolved['questions'][0]['knowledge_point_id'], expected)
        transaction, _ = build_math_content(resolved, self.topics, {})
        target = 'kp-' + expected
        self.assertTrue(any(isinstance(item, dict) and item.get(':db/id') == target and
                            item.get(':knowledge-point/canonical-example') == 'e-789'
                            for item in transaction))
        self.content['lesson_definition']['complete'] = False
        with self.assertRaisesRegex(ValueError, 'Cannot resolve'):
            resolve_knowledge_points(self.content, self.topics, {})

    def test_ambiguous_kp_titles_stop_import(self):
        duplicate = copy.deepcopy(self.point)
        duplicate[':knowledge-point/id'] = uuid.uuid4()
        self.topics[774][':topic/knowledge-points'].append(duplicate)
        self.question['knowledge_point_id'] = str(uuid.uuid4())
        with self.assertRaisesRegex(ValueError, 'Ambiguous'):
            resolve_knowledge_points(self.content, self.topics, {})

    def test_practice_without_complete_answer_fields_is_not_prepared(self):
        self.question['answer_fields'] = []
        with self.assertRaisesRegex(ValueError, 'Authoritative practice'):
            self.plan()

    def test_existing_practice_cannot_be_silently_added_to_a_different_kp(self):
        different = copy.deepcopy(self.point)
        different[':knowledge-point/id'] = uuid.uuid4()
        different[':knowledge-point/title'] = 'A different skill'
        different[':knowledge-point/questions'] = []
        self.topics[774][':topic/knowledge-points'].append(different)
        self.question['knowledge_point_id'] = str(different[':knowledge-point/id'])
        with self.assertRaisesRegex(ValueError, 'another KP|different knowledge point|different KP'):
            self.plan()

    def test_canonical_role_does_not_become_practice(self):
        self.point[':knowledge-point/canonical-example'][':question/math-academy-id'] = 'q-5370'
        with self.assertRaisesRegex(ValueError, 'Canonical example cannot enter practice'):
            self.plan()


if __name__ == '__main__':
    unittest.main()
