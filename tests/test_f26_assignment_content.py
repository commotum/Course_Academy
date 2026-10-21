"""Checks for the explicit-field vault format and additive assignment imports."""
import sys
import copy
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from f26_assignment_content import Builder
from import_school_assignments import Import, stable_id
from sync_f26_assignments import prepare as refresh_assignments


class CanonicalFields(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.vault = Path(self.directory.name)
        self.path = self.vault / 'assignment.md'
        self.path.write_text('')
        self.builder = Builder(self.vault)

    def convert(self, fields, content='Answer: {{value}}.', **attrs):
        return self.builder.question('source', 'problem-1/question',
            dict(id='q-1', content=content, fields=fields, **attrs), self.path)

    def test_mixed_radio_blank_preserves_keys_and_option_feedback(self):
        qid, audit = self.convert([
            {'key': 'value', 'type': 'blank', 'correct': {'type': 'math', 'value': '0'}},
            {'key': 'decision', 'type': 'radio', 'correct': 'a', 'choices': [
                {'id': 'a', 'type': 'text', 'value': 'Yes', 'feedback': 'Reason.'},
                {'id': 'b', 'type': 'text', 'value': 'No'}]}], feedback='Explanation.')
        self.builder.validate()
        rows = {r[':db/id']: r for r in self.builder.entities}
        question = rows[qid]
        self.assertEqual(question[':question/problem'], 'Answer: {{value}}.')
        self.assertEqual(question[':question/worked-solution'], 'Explanation.')
        self.assertEqual({rows[f][':answer-field/key'] for f in question[':question/answer-fields']}, {'value', 'decision'})
        correct = audit['fields'][1]['correct_answer_id']
        self.assertEqual(rows[correct][':answer/feedback'], 'Reason.')

    def test_free_reference_remains_written_response(self):
        qid, audit = self.convert([
            {'key': 'value', 'type': 'blank', 'correct': {'type': 'math', 'value': '0'}},
            {'key': 'proof', 'type': 'free', 'correct': {'type': 'text', 'value': 'A proof.'}}],
            content='Answer: {{value}}. Explain: {{proof}}.')
        self.builder.validate()
        question = next(r for r in self.builder.entities if r[':db/id'] == qid)
        self.assertEqual(len(question[':question/answer-fields']), 1)
        self.assertIn('A proof.', question[':question/worked-solution'])
        self.assertIn('[proof: written response]', question[':question/problem'])
        self.assertEqual(audit['fields'][1]['field_id'], None)
        self.assertEqual(len(self.builder.audit['grading_limitations']), 1)

    def test_selection_rejects_key_outside_its_choices(self):
        with self.assertRaisesRegex(ValueError, 'outside choices'):
            self.convert([{'key': 'value', 'type': 'radio', 'correct': 'c', 'choices': [
                {'id': 'a', 'type': 'text', 'value': 'Yes'}, {'id': 'b', 'type': 'text', 'value': 'No'}]}])

    def test_existing_assignments_and_targets_are_preserved(self):
        snapshot = {'entities': {'1': {'learner/id': 'learner', 'learner/assignments': [7], 'learner/targets': [8]}}}
        model = Import(self.vault, {})
        forms = model.transaction(snapshot, 'learner', [])
        self.assertEqual(forms, [])
        self.assertEqual(snapshot['entities']['1']['learner/assignments'], [7])
        self.assertEqual(snapshot['entities']['1']['learner/targets'], [8])

    def test_study_guide_with_file_uri_lesson_mapping(self):
        lesson = self.vault / 'Lessons' / 'Partial Derivatives.md'
        lesson.parent.mkdir()
        lesson.write_text('lesson-id: 1932\n')
        guide = self.vault / 'F26' / '256' / '10-20-26_SG-2.md'
        guide.parent.mkdir(parents=True)
        guide.write_text('Due: 2026-10-20\n\n## Problem 1\n\n'
                         '```quiz\nid: q-1\ncontent: Explain.\nfields:\n'
                         '- key: response\n  type: free\n  correct:\n'
                         '    type: text\n    value: Explanation.\n```\n\n'
                         f'**Topics:** [Partial derivatives](<{lesson.as_uri()}>)\n')
        self.builder.assignment(str(guide.relative_to(self.vault)))
        self.builder.validate()
        activity = self.builder.audit['activities'][0]
        self.assertEqual(activity['title'], 'MTH 256 — SG-2')
        self.assertEqual(activity['due'], '2026-10-21T06:59:59Z')
        self.assertEqual(activity['problems'][0]['topics'], [1932])
        self.assertEqual(len(self.builder.audit['grading_limitations']), 1)


class AssignmentTargets(unittest.TestCase):
    def setUp(self):
        self.snapshot = {'basis_t': 1, 'entities': {
            '1': {'learner/id': 'learner', 'learner/targets': [8], 'learner/assignments': []},
            '8': {'topic/id': {'$uuid': stable_id('test', 'manual')}, 'topic/math-academy-id': 808},
            '9': {'topic/id': {'$uuid': stable_id('test', 'mapped')}, 'topic/math-academy-id': 909},
            '10': {'topic/id': {'$uuid': stable_id('test', 'other')}, 'topic/math-academy-id': 910},
            '20': {'db/ident': {'$keyword': 'activity.type/assignment'}},
        }}

    def assignment(self, name, topic):
        def identity(kind):
            return stable_id(name, kind)

        def row(kind, **attrs):
            record = {':db/id': identity(kind), f':{kind}/id': {'$uuid': identity(kind)},
                      ':db/ensure': f':{kind}/validate'}
            record.update({':' + key.replace('__', '/').replace('_', '-'): value
                           for key, value in attrs.items()})
            return record

        # Coverage is beneath new steps and multistep content, all in this batch.
        entities = [
            row('activity', activity__type=':activity.type/assignment',
                activity__steps=[identity('step')], activity__first_step=identity('step')),
            row('step', step__content=identity('multistep')),
            row('multistep', multistep__steps=[identity('inner-step')],
                multistep__first_step=identity('inner-step')),
            {':db/id': identity('inner-step'), ':step/id': {'$uuid': identity('inner-step')},
             ':step/content': identity('assigned-problem'), ':db/ensure': ':step/validate'},
            row('assigned-problem', assigned_problem__content=identity('question'),
                assigned_problem__topic_coverage=[{'$ref': [':topic/math-academy-id', topic]}]),
            row('question', question__problem='Original question.'),
        ]
        return entities, identity('activity')

    def store(self, entities, start=700, linked=True):
        identities = {row[':db/id']: start + index for index, row in enumerate(entities)}

        def resolve(value):
            if isinstance(value, dict) and '$ref' in value:
                self.assertEqual(value['$ref'][0], ':topic/math-academy-id')
                return {909: 9, 910: 10}[value['$ref'][1]]
            if isinstance(value, list):
                return [resolve(child) for child in value]
            if isinstance(value, str):
                return identities.get(value, 20 if value == ':activity.type/assignment' else value)
            return value

        for row in entities:
            self.snapshot['entities'][str(identities[row[':db/id']])] = {
                attr[1:]: resolve(value) for attr, value in row.items()
                if attr not in (':db/id', ':db/ensure')}
        if linked:
            self.snapshot['entities']['1']['learner/assignments'].append(start)

    def prepare(self, method, entities, activities):
        if method == 'refresh':
            return refresh_assignments(self.snapshot, entities, activities, [909, 910], 'learner')[0]
        model = Import(Path(tempfile.gettempdir()), {})
        model.entities = entities
        return model.transaction(self.snapshot, 'learner', activities)

    @staticmethod
    def target_writes(forms):
        return [form for form in forms if isinstance(form, list) and form[2] == ':learner/targets']

    def test_new_assignment_adds_nested_coverage_and_preserves_manual_targets(self):
        entities, activity = self.assignment('new', 909)
        untouched = copy.deepcopy(self.snapshot)
        for method in ['import', 'refresh']:
            with self.subTest(method=method):
                forms = self.prepare(method, entities, [activity])
                writes = self.target_writes(forms)
                self.assertEqual([(form[0], form[3]) for form in writes], [(':db/add', 9)])
                self.assertTrue(any(isinstance(form, list) and form[2] == ':learner/assignments'
                                    for form in forms))
                self.assertEqual(self.snapshot, untouched)

    def test_refresh_does_not_restore_explicitly_removed_target(self):
        entities, activity = self.assignment('existing', 909)
        self.store(entities)
        for method in ['import', 'refresh']:
            with self.subTest(method=method):
                self.assertEqual(self.prepare(method, entities, [activity]), [])

    def test_existing_content_newly_linked_adds_target_once(self):
        entities, activity = self.assignment('existing-unlinked', 909)
        self.store(entities, linked=False)
        for method in ['import', 'refresh']:
            with self.subTest(method=method):
                self.assertEqual([form[3] for form in self.target_writes(
                    self.prepare(method, entities, [activity]))], [9])
        self.snapshot['entities']['1']['learner/targets'].append(9)
        for method in ['import', 'refresh']:
            self.assertEqual(self.target_writes(self.prepare(method, entities, [activity])), [])

    def test_mixed_batch_targets_only_new_links(self):
        existing, old_activity = self.assignment('existing', 909)
        new, new_activity = self.assignment('new', 910)
        self.store(existing)
        for method in ['import', 'refresh']:
            with self.subTest(method=method):
                forms = self.prepare(method, existing + new, [old_activity, new_activity])
                self.assertEqual([form[3] for form in self.target_writes(forms)], [10])

    def test_unlinked_generated_content_is_not_a_target(self):
        selected, activity = self.assignment('selected', 909)
        unrelated, _ = self.assignment('unrelated', 910)
        for method in ['import', 'refresh']:
            with self.subTest(method=method):
                forms = self.prepare(method, selected + unrelated, [activity])
                self.assertEqual([form[3] for form in self.target_writes(forms)], [9])

    def test_refreshing_mapping_on_existing_link_does_not_add_targets(self):
        entities, activity = self.assignment('existing', 909)
        self.store(entities)
        updated = copy.deepcopy(entities)
        problem = next(row for row in updated if ':assigned-problem/id' in row)
        problem[':assigned-problem/topic-coverage'] = [{'$ref': [':topic/math-academy-id', 910]}]
        forms = self.prepare('refresh', updated, [activity])
        self.assertTrue(any(isinstance(form, list) and form[2] == ':assigned-problem/topic-coverage'
                            for form in forms))
        self.assertEqual(self.target_writes(forms), [])


if __name__ == '__main__':
    unittest.main()
