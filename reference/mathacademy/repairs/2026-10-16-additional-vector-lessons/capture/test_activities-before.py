import copy
import json
import tempfile
import unittest
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from activities import (build_activity_transaction, html_to_markdown, parse_lesson_html,
                        source_uuid, ref, capture_lesson)
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

    def test_replacement_with_multiple_old_candidates_is_held(self):
        content, topics, snapshot = fixture()
        lesson = snapshot['lessons'][1]
        lesson[':activity/steps'].insert(1, step(105, tutorial(5)))
        route(lesson[':activity/steps'])
        content['lesson_definition']['steps'][0].update(math_academy_id=901, content_id=9)
        content['tutorials'][0].update(math_academy_id=9)
        with self.assertRaisesRegex(ValueError, 'Ambiguous tutorial replacement'):
            build_activity_transaction(content, topics, snapshot, [])

    def test_replacement_with_additional_unmatched_sections_is_held(self):
        content, topics, snapshot = fixture()
        content['lesson_definition']['steps'][0].update(math_academy_id=901, content_id=9)
        content['tutorials'][0].update(math_academy_id=9)
        content['lesson_definition']['steps'].insert(1,
            {'math_academy_id': 908, 'type': 'tutorial', 'content_id': 8, 'title': 'Additional explanation'})
        content['tutorials'].append({'math_academy_id': 8, 'title': 'Additional explanation', 'content': 'Source explanation'})
        with self.assertRaisesRegex(ValueError, 'Ambiguous tutorial replacement'):
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

    def test_existing_multistep_is_noop_and_reorder_keeps_step_uuids(self):
        _, topics, snapshot = fixture()
        mid = source_uuid('multistep', 77)
        pid = source_uuid('multistep-assigned-problem', 77)
        aid = source_uuid('multistep-activity', 77)
        inner = route([{':db/id': 501 + i, ':step/id': uid('inner-' + str(i)),
                        ':step/content': {':db/id': 601 + i, ':question/id': uid('q-' + str(i)),
                                          ':question/math-academy-id': 'q-' + str(i)}} for i in (1, 2)])
        multi = {':db/id': 700, ':multistep/id': mid, ':multistep/context': 'Source setup',
                 ':multistep/steps': inner, ':multistep/first-step': {':db/id': inner[0][':db/id'], ':step/id': inner[0][':step/id']}}
        assigned = {':db/id': 701, ':assigned-problem/id': pid, ':assigned-problem/content': multi,
                    ':assigned-problem/topic-coverage': [topics[1]]}
        outer = {':db/id': 702, ':step/id': uid('outer'), ':step/content': assigned}
        activity = {':db/id': 703, ':activity/id': aid, ':activity/title': 'Multipart task',
                    ':activity/type': {':db/ident': kw('activity.type/assignment')}, ':activity/steps': [outer],
                    ':activity/first-step': {':db/id': 702, ':step/id': uid('outer')}}
        snapshot['multisteps'][str(mid)] = multi
        snapshot['assigned_problems'][str(pid)] = assigned
        snapshot['activities'][str(aid)] = activity
        content = {'task_type': 'multistep', 'multistep_id': 77, 'title': 'Multipart task',
                   'question_order': ['q-1', 'q-2'], 'shared_contexts': [{'problem': 'Source setup'}],
                   'questions': [{'math_academy_id': 'q-' + str(i), 'topic_id': 1, 'local_problem': 'Part ' + str(i),
                                  'problem': 'Part ' + str(i)} for i in (1, 2)]}
        tx, _ = build_activity_transaction(content, topics, snapshot, [])
        self.assertEqual(tx, [])
        content['question_order'].reverse()
        tx, report = build_activity_transaction(content, topics, snapshot, [])
        self.assertFalse(any(isinstance(f, dict) and ':step/id' in f for f in tx))
        self.assertTrue(any(isinstance(f, list) and f[1] == ref('step/id', uid('inner-1')) and f[2] == ':step/next' for f in tx))
        self.assertEqual(report['decisions'][0]['reused_steps'], 2)

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

    def test_capture_definition_downloads_tutorial_images_and_saves_source_examples(self):
        html = '''<h1 id="topicName">A Lesson</h1>
        <div class="step" stepId="333" stepType="tutorial" contentId="9">
         <div class="stepHeader"><div class="stepName">Intro</div></div>
         <p>Diagram <img src="/graphics/example.png"></p>
         <svg viewBox="0 0 7 3" preserveAspectRatio="xMidYMid meet"><path d="M0 0 L7 3"/></svg>
        </div><div class="step" stepId="444" stepType="example" contentId="10">
         <div class="stepName">Example: Compute</div>
         <div class="exampleQuestion"><p>Find it.</p></div>
         <div class="exampleExplanation"><p>Here it is.</p></div></div>'''
        from io import BytesIO
        from PIL import Image
        buffer = BytesIO()
        Image.new('RGB', (2, 2), 'blue').save(buffer, format='PNG')
        png = buffer.getvalue()
        page_response = SimpleNamespace(ok=True, url='https://mathacademy.com/topics/1', text=lambda: html)
        image_response = SimpleNamespace(ok=True, body=lambda: png, headers={'content-type': 'image/png'})
        request = Mock()
        request.get.side_effect = [page_response, image_response]
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder) / 'capture'
            directory.mkdir()
            root = Path(folder) / 'math'
            reader = SimpleNamespace(page=SimpleNamespace(context=SimpleNamespace(request=request)),
                                     args=SimpleNamespace(math_root=root, timeout_ms=1000), image_responses={})
            state = {'topic_id': 1, 'examples': {}}
            capture_lesson(reader, state, directory, {':topic/knowledge-points': []})
            self.assertEqual((directory / 'lesson-topic.html').read_text(), html)
            self.assertIn('images/', state['tutorials'][0]['content'])
            self.assertEqual(len(list((root / 'images').glob('*/*.png'))), 1)
            svg_files = list((root / 'images').glob('*/*.svg'))
            self.assertEqual(len(svg_files), 1)
            self.assertIn('viewBox="0 0 7 3"', svg_files[0].read_text())
            self.assertIn('preserveAspectRatio="xMidYMid meet"', svg_files[0].read_text())
            self.assertNotIn('viewbox=', svg_files[0].read_text())
            example_capture = json.loads((directory / 'lesson-example-10.json').read_text())
            self.assertEqual(example_capture['worked_solution'], 'Here it is.')
            self.assertIn('exampleExplanation', example_capture['html'])
            self.assertEqual(len(state['lesson_new_knowledge_points']), 1)
            self.assertEqual(request.get.call_count, 2)
            from core import atomic_json
            from saved_imports import eligible
            question = {'math_academy_id': 'q-1', 'problem': 'Problem', 'worked_solution': 'Solution'}
            state.update(task_id=1, task_type='lesson', activity_complete=True, lesson_complete=True,
                         history_complete=True, completion="You've completed the lesson.",
                         questions={'q-1': {'finalized': True, 'history': {'worked_solution': 'Solution'}, 'content': question}})
            content = {'task_id': 1, 'task_type': 'lesson', 'capture_version': 2, 'content_only': True,
                       'questions': [question], 'canonical_examples': state['lesson_examples'],
                       'tutorials': state['tutorials'], 'lesson_definition': state['lesson_definition'],
                       'new_knowledge_points': state['lesson_new_knowledge_points']}
            atomic_json(directory / 'activity-metadata.json', [{'id': 'question-1'}])
            self.assertTrue(eligible(directory, state, content))
            (directory / 'lesson-topic.html').unlink()
            self.assertFalse(eligible(directory, state, content))

    def test_source_get_uses_rate_limit_and_authentication_exceptions(self):
        from browser import AccessBlocked, RateLimited
        for status, exception in ((429, RateLimited), (403, AccessBlocked)):
            request = Mock()
            request.get.return_value = SimpleNamespace(status=status, ok=False,
                headers={'retry-after': '7'}, url='https://mathacademy.com/topics/1')
            reader = SimpleNamespace(page=SimpleNamespace(context=SimpleNamespace(request=request)),
                                     args=SimpleNamespace(timeout_ms=1000))
            with tempfile.TemporaryDirectory() as directory:
                with self.assertRaises(exception) as caught:
                    capture_lesson(reader, {'topic_id': 1}, directory, {})
                if status == 429:
                    self.assertEqual(caught.exception.retry_after, 7)


if __name__ == '__main__':
    unittest.main()
