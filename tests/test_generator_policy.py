import copy
import unittest
from scripts.generator_policy import EmptyCheckboxSelection, checkbox_selection, nonempty_checkbox, explicit_none_checkbox

def record(values):
    fields = []
    for index, value in enumerate(values):
        fields.append({':answer-field/type': ':answer-field.type/checkbox',
                       ':answer-field/correct': [':answer/id', f'{index}-{str(value).lower()}'],
                       ':answer-field/choices': [{':answer/id': f'{index}-{v}', ':answer/value': v}
                                                for v in ('false', 'true')]})
    return {'question': {':question/answer-fields': fields}}

class CheckboxPolicyTests(unittest.TestCase):
    def test_seeded_rejection_is_deterministic(self):
        @nonempty_checkbox
        def generate(level, seed=0):
            return record([seed != 0, False])
        self.assertEqual(generate('easy'), generate('easy'))
        self.assertTrue(any(checkbox_selection(generate('easy'))))

    def test_explicit_parameters_are_rejected_without_being_changed(self):
        @nonempty_checkbox
        def generate(seed=0, parameters=None):
            return record(parameters)
        values = [False, False]
        with self.assertRaises(EmptyCheckboxSelection): generate(parameters=values)
        self.assertEqual(values, [False, False])

    def test_large_batch_resamples_only_empty_slots(self):
        calls = []
        @nonempty_checkbox
        def generate(count=1000, seed=0):
            calls.append(count)
            return [record([i % 2 == 1 or seed != 0]) for i in range(count)]
        result = generate()
        self.assertEqual(len(result), 1000)
        self.assertTrue(all(any(checkbox_selection(r)) for r in result))
        self.assertEqual(calls.count(1000), 1)
        self.assertEqual(calls.count(1), 500)

    def test_no_supported_nonempty_case_fails_boundedly(self):
        @nonempty_checkbox
        def generate(seed=0): return record([False])
        with self.assertRaises(EmptyCheckboxSelection): generate()

    def test_historical_evidence_can_be_read(self):
        @nonempty_checkbox
        def generate(seed=0):
            return {**record([False]), 'generation': {'eligible_for_learning': False}}
        self.assertEqual(checkbox_selection(generate()), [False])

    def test_noncheckbox_content_is_unchanged(self):
        original = {'question': {':question/problem': 'Example', ':question/answer-fields': []}}
        @nonempty_checkbox
        def generate(seed=0): return copy.deepcopy(original)
        self.assertEqual(generate(), original)

class ExplicitNonePolicyTests(unittest.TestCase):
    def source(self, values):
        value = record(values)
        q = value['question']
        q[':question/id'] = 'question-fixture'
        q[':question/problem'] = 'Select all that apply. If none apply, leave all boxes unchecked.'
        for index, field in enumerate(q[':question/answer-fields']):
            field[':answer-field/id'] = 'field-' + str(index)
            field[':answer-field/key'] = 'Statement ' + str(index)
        return value

    def test_none_is_true_exactly_for_empty_ordinary_selection(self):
        for ordinary in ([False, False], [True, False], [False, True], [True, True]):
            original = self.source(ordinary)
            saved = copy.deepcopy(original)
            result = explicit_none_checkbox(original)
            self.assertEqual(checkbox_selection(result), [*ordinary, not any(ordinary)])
            self.assertEqual(original, saved)
            self.assertNotIn('leave all boxes unchecked', result['question'][':question/problem'])
            self.assertEqual(explicit_none_checkbox(result), result)
            self.assertEqual(explicit_none_checkbox(original), result)

    def test_changed_shape_gets_new_owned_identities(self):
        original = self.source([False, True])
        result = explicit_none_checkbox(original)
        self.assertNotEqual(original['question'][':question/id'], result['question'][':question/id'])
        old = {a[':answer/id'] for f in original['question'][':question/answer-fields'] for a in f[':answer-field/choices']}
        fields = result['question'][':question/answer-fields']
        ids = [a[':answer/id'] for f in fields for a in f[':answer-field/choices']]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertFalse(old & set(ids))
        for field in fields:
            self.assertIn(field[':answer-field/correct'][1], [a[':answer/id'] for a in field[':answer-field/choices']])

    def test_source_backed_empty_parameters_are_preserved_without_resampling(self):
        calls = []
        def generate(seed=0, parameters=None):
            calls.append(seed)
            return self.source(parameters)
        checked = nonempty_checkbox(generate, none_label='None of the above')
        result = checked(parameters=[False, False])
        self.assertEqual(calls, [0])
        self.assertEqual(checkbox_selection(result), [False, False, True])

    def test_nested_batch_decorators_do_not_duplicate_none(self):
        def single(seed=0): return self.source([False])
        single = nonempty_checkbox(single, none_label='None of the above')
        def batch(count=3, seed=0): return {'records': [single(seed=i) for i in range(count)]}
        batch = nonempty_checkbox(batch, none_label='None of the above')
        self.assertEqual([checkbox_selection(r) for r in batch()['records']], [[False, True]] * 3)

    def test_evidence_and_noncheckbox_records_remain_unchanged(self):
        evidence = self.source([False])
        evidence['generation'] = {'evidence_only': True}
        self.assertEqual(explicit_none_checkbox(evidence), evidence)
        self.assertEqual(explicit_none_checkbox({'question': {':question/answer-fields': []}}), {'question': {':question/answer-fields': []}})

    def test_existing_inconsistent_none_is_rejected(self):
        value = explicit_none_checkbox(self.source([False]))
        field = value['question'][':question/answer-fields'][-1]
        field[':answer-field/correct'] = [':answer/id', field[':answer-field/choices'][0][':answer/id']]
        with self.assertRaisesRegex(ValueError, 'disagrees'):
            explicit_none_checkbox(value)

if __name__ == '__main__': unittest.main()
