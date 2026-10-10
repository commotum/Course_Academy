import copy
import unittest
import uuid

from activities import (build_activity_transaction, html_to_markdown, parse_lesson_html,
                        source_uuid, ref)
from edn import kw


def uid(label):
    return uuid.uuid5(uuid.NAMESPACE_URL, label)


def tutorial(mid, title=None):
    return {':db/id': mid + 1000, ':tutorial/id': uid('tutorial-' + str(mid)),
            ':tutorial/math-academy-id': mid, ':tutorial/title': title or 'Tutorial ' + str(mid),
            ':tutorial/content': 'Body ' + str(mid)}


def step(mid, content):
    return {':db/id': mid + 2000, ':step/id': uid('step-' + str(mid)),
            ':step/math-academy-id': mid, ':step/content': content}


def example(mid):
    return {':db/id': mid + 3000, ':knowledge-point/id': uid('kp-' + str(mid)),
            ':knowledge-point/title': 'Skill ' + str(mid),
            ':knowledge-point/canonical-example': {':db/id': mid + 4000,
                ':question/id': uid('example-' + str(mid)), ':question/math-academy-id': 'e-' + str(mid)}}


def route(steps):
    for i, s in enumerate(steps):
        s.pop(':step/next', None)
        if i + 1 < len(steps):
            s[':step/next'] = {':db/id': steps[i+1][':db/id'], ':step/id': steps[i+1][':step/id']}
    return steps


def fixture():
    kp = example(2)
    topic = {':db/id': 10, ':topic/id': uid('topic'), ':topic/math-academy-id': 1,
             ':topic/title': 'Lesson', ':topic/knowledge-points': [kp]}
    steps = route([step(101, tutorial(1)), step(102, kp), step(103, tutorial(3))])
    lesson = {':db/id': 20, ':activity/id': uid('lesson'), ':activity/title': 'Lesson',
              ':activity/type': {':db/ident': kw('activity.type/lesson')}, ':activity/scope': topic,
              ':activity/steps': steps, ':activity/first-step': {':db/id': steps[0][':db/id'], ':step/id': steps[0][':step/id']}}
    definition = {'topic_id': 1, 'title': 'Lesson', 'complete': True, 'steps': [
        {'math_academy_id': 101, 'type': 'tutorial', 'content_id': 1, 'title': 'Tutorial 1'},
        {'math_academy_id': 102, 'type': 'example', 'content_id': 2, 'title': 'Skill 2'},
        {'math_academy_id': 103, 'type': 'tutorial', 'content_id': 3, 'title': 'Tutorial 3'}]}
    content = {'task_type': 'lesson', 'topic_id': 1, 'questions': [], 'canonical_examples': [],
               'lesson_definition': definition, 'tutorials': [
                   {'math_academy_id': i, 'title': 'Tutorial ' + str(i), 'content': 'Body ' + str(i)} for i in (1, 3)]}
    snapshot = {'lessons': {1: lesson}, 'tutorials': {1: tutorial(1), 3: tutorial(3)},
                'source_steps': {s[':step/math-academy-id']: s for s in steps},
                'multisteps': {}, 'assigned_problems': {}, 'activities': {}}
    return content, {1: topic}, snapshot


class ActivityTests(unittest.TestCase):
    def test_unchanged_lesson_is_noop(self):
        content, topics, snapshot = fixture()
        tx, report = build_activity_transaction(content, topics, snapshot, [])
        self.assertEqual(tx, [])
        self.assertEqual(report['retractions'], [])

    def test_new_tutorial_and_reorder_reuse_existing_step_ids(self):
        content, topics, snapshot = fixture()
        old = content['lesson_definition']['steps']
        content['lesson_definition']['steps'] = [old[2], old[0],
            {'math_academy_id': 104, 'type': 'tutorial', 'content_id': 4, 'title': 'Added'}, old[1]]
        content['tutorials'].append({'math_academy_id': 4, 'title': 'Added', 'content': 'New source body'})
        tx, report = build_activity_transaction(content, topics, snapshot, [])
        created = [f for f in tx if isinstance(f, dict) and ':step/id' in f]
        self.assertEqual([f[':step/id'] for f in created], [source_uuid('step', 104)])
        terminal = next(f for f in tx if isinstance(f, list) and f[2] == ':step/next')
        self.assertEqual(terminal[1], ref('step/id', uid('step-102')))
        self.assertEqual(report['decisions'][-1]['reused_steps'], 3)

    def test_removal_retracts_ownership_without_deleting_content(self):
        content, topics, snapshot = fixture()
        content['lesson_definition']['steps'].pop()
        tx, report = build_activity_transaction(content, topics, snapshot, [])
        removal = [f for f in tx if isinstance(f, list) and f[2] == ':activity/steps']
        self.assertEqual(len(removal), 1)
        self.assertEqual(removal[0][3], ref('step/id', uid('step-103')))
        self.assertFalse(any('retractEntity' in str(f) for f in tx))

    def test_replacement_retains_tutorial_and_step_uuid(self):
        content, topics, snapshot = fixture()
        content['lesson_definition']['steps'][2].update(math_academy_id=503, content_id=9)
        content['tutorials'][1].update(math_academy_id=9, content='Revised body')
        tx, report = build_activity_transaction(content, topics, snapshot, [])
        changed = next(f for f in tx if isinstance(f, dict) and f.get(':tutorial/math-academy-id') == 9)
        self.assertEqual(changed[':db/id'], ref('tutorial/id', uid('tutorial-3')))
        changed_step = next(f for f in tx if isinstance(f, dict) and f.get(':step/math-academy-id') == 503)
        self.assertEqual(changed_step[':db/id'], ref('step/id', uid('step-103')))
        self.assertFalse(any(isinstance(f, dict) and ':tutorial/id' in f for f in tx))
        self.assertEqual(report['decisions'][0]['kind'], 'tutorial_identity_update')

    def test_ambiguous_replacement_is_held(self):
        content, topics, snapshot = fixture()
        content['lesson_definition']['steps'][2].update(math_academy_id=503, content_id=9, title='Different purpose')
        content['tutorials'][1].update(math_academy_id=9, title='Different purpose')
        with self.assertRaisesRegex(ValueError, 'review before import'):
            build_activity_transaction(content, topics, snapshot, [])

    def test_new_kp_ref_uses_same_transaction_tempid(self):
        content, topics, snapshot = fixture()
        kid = uid('newkp')
        content['lesson_definition']['steps'].append({'math_academy_id': 900, 'type': 'example', 'content_id': 900, 'title': 'New skill'})
        content['new_knowledge_points'] = [{'id': str(kid), 'source_example_id': 'e-900', 'title': 'New skill'}]
        tx, _ = build_activity_transaction(content, topics, snapshot,
                                          [{kw('db/id'): 'new-kp', kw('knowledge-point/id'): kid}])
        newstep = next(f for f in tx if isinstance(f, dict) and f.get(':step/math-academy-id') == 900)
        self.assertEqual(newstep[':step/content'], 'new-kp')

    def test_global_placement_collision_is_held(self):
        content, topics, snapshot = fixture()
        snapshot['source_steps'][101] = step(555, tutorial(555))
        with self.assertRaisesRegex(ValueError, 'different step'):
            build_activity_transaction(content, topics, snapshot, [])

    def test_multistep_has_context_inner_order_and_separate_wrapper(self):
        _, topics, snapshot = fixture()
        content = {'task_type': 'multistep', 'multistep_id': 77, 'title': 'Multipart task',
                   'question_order': ['q-1', 'q-2'], 'shared_contexts': [{'problem': 'Source setup'}],
                   'questions': [{'math_academy_id': 'q-' + str(i), 'topic_id': 1, 'local_problem': 'Part ' + str(i),
                                  'problem': 'Part ' + str(i)} for i in (1, 2)]}
        qtx = [{kw('db/id'): 'q-' + str(i), kw('question/id'): uid('q-' + str(i)),
                kw('question/math-academy-id'): 'q-' + str(i)} for i in (1, 2)]
        tx, _ = build_activity_transaction(content, topics, snapshot, qtx)
        multi = next(f for f in tx if isinstance(f, dict) and ':multistep/id' in f)
        outer = next(f for f in tx if isinstance(f, dict) and ':activity/id' in f)
        self.assertEqual(multi[':multistep/context'], 'Source setup')
        self.assertEqual(len(multi[':multistep/steps']), 2)
        self.assertEqual(len(outer[':activity/steps']), 1)
        self.assertNotIn(outer[':activity/first-step'], multi[':multistep/steps'])
        self.assertTrue(any(isinstance(f, dict) and f.get(':step/content') == 'q-1' for f in tx))
        self.assertFalse(any(isinstance(f, dict) and ':step/math-academy-id' in f for f in tx))

    def test_multistep_missing_part_and_solver_expansion_are_held(self):
        _, topics, snapshot = fixture()
        content = {'task_type': 'multistep', 'multistep_id': 77, 'title': 'Task', 'question_order': ['q-1', 'q-2'],
                   'questions': [{'math_academy_id': 'q-1', 'topic_id': 1, 'local_problem': 'Part', 'problem': 'Earlier answer: 5. Part'}]}
        with self.assertRaisesRegex(ValueError, 'all original'):
            build_activity_transaction(content, topics, snapshot, [])
        content['question_order'] = ['q-1']
        with self.assertRaisesRegex(ValueError, 'local problem'):
            build_activity_transaction(content, topics, snapshot, [])

    def test_source_parser_uses_placement_ids_and_formula_titles(self):
        html = '''<h1 id="topicName">A Lesson</h1>
        <div class="step" stepId="333" stepType="tutorial" contentId="9">
         <div class="stepHeader"><div class="stepName">Intro</div></div>
         <p>Let <span class="mjpage"><svg><title>x^2</title></svg></span> grow.</p><!--tikz-->
        </div><div class="step" stepId="444" stepType="example" contentId="10">
         <div class="stepName">Example: Compute</div>
         <div class="exampleQuestion"><p>Find it.</p></div>
         <div class="exampleExplanation"><p>Here it is.</p></div></div>'''
        definition, tutorials, examples = parse_lesson_html(html, 1)
        self.assertEqual([s['math_academy_id'] for s in definition['steps']], [333, 444])
        self.assertEqual(tutorials[0]['content'], 'Let $x^2$ grow.')
        self.assertEqual(examples[0]['math_academy_id'], 'e-10')
        self.assertEqual(examples[0]['worked_solution'], 'Here it is.')


if __name__ == '__main__':
    unittest.main()
