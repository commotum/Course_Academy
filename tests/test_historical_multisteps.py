import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from repair_historical_multisteps import forms_for, identity


class HistoricalMultistepRepairTests(unittest.TestCase):
    def fixture(self):
        task = {'task_id': '123', 'title': 'Motion', 'questions': ['q-1', 'q-2']}
        questions = {f'q-{i}': {':db/id': i, ':question/math-academy-id': f'q-{i}'}
                     for i in (1, 2)}
        context = {'123': {'context': 'Given velocity.', 'evidence_questions': ['q-1']}}
        return [task], questions, context

    def test_recovered_sequence_owns_inner_steps_separately_and_reuses_questions(self):
        tasks, questions, context = self.fixture()
        forms, summary = forms_for(tasks, questions, context)
        multi = next(f for f in forms if ':multistep/id' in f)
        activity = next(f for f in forms if ':activity/id' in f)
        self.assertTrue(set(multi[':multistep/steps']).isdisjoint(activity[':activity/steps']))
        records = {f[':db/id']: f for f in forms}
        first = records[multi[':multistep/first-step']]
        second = records[first[':step/next']]
        self.assertEqual([first[':step/content'], second[':step/content']], [1, 2])
        self.assertNotIn(':step/next', second)
        self.assertFalse(any(':question/problem' in f or ':question/id' in f for f in forms))
        self.assertEqual(len(summary['restored']), 1)
        self.assertNotEqual(identity('activity', '123'), identity('activity', '124'))

    def test_missing_setup_withdraws_parts_without_fabricating_activity(self):
        tasks, questions, _ = self.fixture()
        forms, summary = forms_for(tasks, questions, {})
        self.assertEqual(forms, [[':db/add', 1, ':question/retired', True],
                                 [':db/add', 2, ':question/retired', True]])
        self.assertEqual(len(summary['withdrawn']), 1)

    def test_existing_containment_is_preserved_and_partial_containment_stops(self):
        tasks, questions, context = self.fixture()
        questions['q-1'][':step/_content'] = [{':db/id': 10, ':multistep/_steps': {':db/id': 30}}]
        with self.assertRaisesRegex(ValueError, 'Partially placed'):
            forms_for(tasks, questions, context)
        questions['q-2'][':step/_content'] = [{':db/id': 11, ':multistep/_steps': {':db/id': 30}}]
        forms, summary = forms_for(tasks, questions, context)
        self.assertEqual(forms, [])
        self.assertEqual(summary['existing'], ['123'])


if __name__ == '__main__':
    unittest.main()
