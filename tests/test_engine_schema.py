"""Current-schema loading and atomic item writeback boundary checks."""
from copy import deepcopy
from dataclasses import asdict, replace
from datetime import datetime, timezone
import unittest
from uuid import UUID

from engine.fire import Event, Policy, TopicState
from engine.schema import (EntitySnapshot, Keyword, POLICY_FIELDS, completion_transaction,
                           edn, instant, instant_days, load_runtime, task_transaction)

AT = datetime(2026, 9, 28, tzinfo=timezone.utc)

def identity(number):
    return UUID(int=number)


def records():
    policy = Policy()
    values = {'policy/id': identity(1)}
    for attr, field in POLICY_FIELDS.items():
        values['policy/' + attr] = 100 if field == 'memory_order' else getattr(policy, field)
    return {
        1: values,
        2: {'learner/id': 'alice', 'learner/activity': [3]},
        3: {'learner-task/id': identity(3), 'learner-task/activity': 4,
            'learner-task/status': 101, 'learner-task/items': [5]},
        4: {'review/id': identity(4), 'review/topic': 6},
        5: {'task-item/id': identity(5), 'task-item/index': 1, 'task-item/content': 8},
        6: {'topic/id': identity(6), 'topic/knowledge-points': [7], 'topic/encompasses': [12]},
        7: {'knowledge-point/id': identity(7), 'knowledge-point/questions': [8]},
        8: {'question/id': identity(8), 'question/answer-fields': [9]},
        9: {'answer-field/id': identity(9), 'answer-field/key': 'answer', 'answer-field/answer-choices': [10, 11]},
        10: {'answer/id': identity(10)}, 11: {'answer/id': identity(11)},
        12: {'encompassing/topic': 13, 'encompassing/weight': .25},
        13: {'topic/id': identity(13)},
        100: {'db/ident': Keyword('policy.retention-update/decay-before-add')},
        101: {'db/ident': Keyword('learner-task.status/in-progress')},
        102: {'db/ident': Keyword('learner-task.status/completed')},
        103: {'db/ident': Keyword('task-item.result/correct')},
        104: {'db/ident': Keyword('learner-task.outcome/passed')},
        105: {'db/ident': Keyword('task-item.result/incorrect')},
    }


def loaded(data=None):
    return load_runtime(EntitySnapshot(records() if data is None else data, 31), 2, 1)


class SchemaTests(unittest.TestCase):
    def test_policy_graph_unknown_difficulty_and_missing_state(self):
        runtime = loaded()
        self.assertEqual(runtime.engine.policy, Policy())
        self.assertEqual(runtime.engine.graph.coverage(str(identity(6))),
                         {str(identity(6)): 1., str(identity(13)): .25})
        self.assertEqual(runtime.engine.difficulty_accuracy, {})
        self.assertEqual(runtime.engine.states, {})
        self.assertEqual(runtime.snapshot.topic_for_question(8), 6)
        for attr in POLICY_FIELDS:
            data = records()
            del data[1]['policy/' + attr]
            with self.subTest(attr=attr), self.assertRaises(ValueError): loaded(data)

    def test_snapshot_freezes_caller_data_and_resolves_refs(self):
        data = records()
        snapshot = EntitySnapshot(data, 12)
        data[7]['knowledge-point/questions'].append(10)
        self.assertEqual(snapshot.refs(7, 'knowledge-point/questions'), (8,))
        self.assertEqual(snapshot.eid(':task-item.result/correct'), 103)
        with self.assertRaises(TypeError): snapshot.entity(7)['knowledge-point/questions'] = ()
        for bad in [True, -1, '12']:
            with self.assertRaises(ValueError): EntitySnapshot(data, bad)

    def test_curriculum_neighbors_inform_priors_without_adding_coverage(self):
        data = records()
        data[6]['topic/prerequisites'] = [13]
        data[7]['knowledge-point/key-prerequisites'] = [14]
        data[14] = {'topic/id': identity(14)}
        data[15] = {'topic/id': identity(15)}
        data[16] = {'module/id': identity(16), 'module/topics': [6, 15]}
        runtime = loaded(data)
        topic = str(identity(6))
        self.assertEqual(set(runtime.engine.neighborhoods[topic]),
                         {str(identity(i)) for i in (13, 14, 15)})
        self.assertEqual(runtime.engine.graph.coverage(topic),
                         {topic: 1., str(identity(13)): .25})
        updated = deepcopy(runtime.engine)
        updated.neighborhoods = {}
        with self.assertRaisesRegex(ValueError, 'captured policy'):
            completion_transaction(runtime, 5, AT, [], updated)
        data[6]['topic/prerequisites'] = [10]
        with self.assertRaisesRegex(ValueError, 'known topics'): loaded(data)

    def test_ambiguous_banks_or_task_ownership_rejected(self):
        data = records()
        data[20] = {'knowledge-point/id': identity(20), 'knowledge-point/questions': [8]}
        data[6]['topic/knowledge-points'].append(20)
        with self.assertRaisesRegex(ValueError, 'one knowledge-point'):
            loaded(data).snapshot.topic_for_question(8)
        data = records()
        data[20] = {'learner/id': 'bob', 'learner/activity': [3]}
        with self.assertRaisesRegex(ValueError, 'multiple learner'): loaded(data)

    def test_item_writeback_is_atomic_guarded_and_leaves_input_unchanged(self):
        runtime = loaded()
        updated = deepcopy(runtime.engine)
        topic = str(identity(6))
        updated.apply_accuracy(Event('accuracy', 'alice', topic, instant_days(AT), True, kind='review'))
        plan = completion_transaction(runtime, 5, AT,
            [{'db/id': 5, 'task-item/result': Keyword('task-item.result/correct'),
              'task-item/responses': [10], 'task-item/elapsed-seconds': 2}], updated)
        self.assertEqual(plan.compare_basis_t, 31)
        self.assertEqual(plan.forms[0], (Keyword('db/cas'), 5, Keyword('task-item/completed-at'), None, AT))
        self.assertIn(':task-item/elapsed-seconds 2.0', plan.edn)
        self.assertIn(':progress/validate', plan.edn)
        self.assertIn(':performance/validate', plan.edn)
        self.assertIn(':learner/knowledge-profile ["engine-progress-', plan.edn)
        self.assertIn(':learner/performance "engine-global-performance"', plan.edn)
        self.assertEqual(runtime.engine.states, {})
        self.assertEqual(runtime.engine.global_ability, {})
        changed = completion_transaction(runtime, 5, AT, [], updated)
        self.assertEqual(plan.request_key, changed.request_key)
        self.assertNotEqual(plan.edn, changed.edn)
        without_state = completion_transaction(runtime, 5, AT, [], deepcopy(runtime.engine))
        self.assertEqual(plan.request_key, without_state.request_key)
        data = records()
        data[3]['learner-task/items'].append(25)
        data[25] = dict(data[5], **{'task-item/id': identity(25)})
        other = loaded(data)
        other_plan = completion_transaction(other, 25, AT, [], updated)
        self.assertNotEqual(plan.request_key, other_plan.request_key)
        self.assertNotIn('fire-event', plan.edn)
        self.assertNotIn('engine-update', plan.edn)

    def test_existing_progress_and_global_performance_reused(self):
        data = records()
        data[2]['learner/knowledge-profile'] = [20]
        data[2]['learner/performance'] = 21
        data[20] = {'progress/id': 'alice-topic', 'progress/topic': 6, 'progress/policy': 1,
                    'progress/repetitions': 2., 'progress/memory': 1.5, 'progress/memory-at': AT,
                    'progress/interval-days': 4., 'progress/learned': True}
        for prefix, target in [('progress', data[20]), ('performance', data.setdefault(21, {}))]:
            target.update({prefix + '/assessment-accuracy': .8, prefix + '/practice-accuracy': .8,
                           prefix + '/assessment-mass': 0., prefix + '/practice-mass': 0.})
        runtime = loaded(data)
        self.assertEqual(runtime.engine.states['alice'][str(identity(6))].memory, 1.5)
        updated = deepcopy(runtime.engine)
        updated.apply_accuracy(Event('a', 'alice', str(identity(6)), instant_days(AT), False, kind='review'))
        plan = completion_transaction(runtime, 5, AT, [], updated)
        by_eid = {f['db/id']: f for f in plan.forms if hasattr(f, 'keys')}
        self.assertIn('progress/memory', by_eid[20])
        self.assertIn('performance/practice-mass', by_eid[21])
        self.assertNotIn('learner/knowledge-profile', by_eid[2])
        self.assertNotIn('learner/performance', by_eid[2])
        self.assertNotIn('progress/id', by_eid[20])

    def test_completion_rejects_old_time_terminal_and_changed_inputs(self):
        for modify in [lambda d: d[5].update({'task-item/completed-at': AT}),
                       lambda d: d[3].update({'learner-task/status': 102}),
                       lambda d: d[3].update({'learner-task/started-at': '2026-09-29T00:00:00Z'})]:
            data = records(); modify(data); runtime = loaded(data)
            with self.assertRaises(ValueError): completion_transaction(runtime, 5, AT, [], deepcopy(runtime.engine))
        runtime = loaded(); updated = deepcopy(runtime.engine)
        updated.policy = replace(updated.policy, accuracy_alpha=.3)
        with self.assertRaisesRegex(ValueError, 'captured policy'):
            completion_transaction(runtime, 5, AT, [], updated)

    def test_selection_and_entered_response_field_validation(self):
        runtime = loaded()
        for responses in [[10, 11], [13], [True]]:
            with self.subTest(responses=responses), self.assertRaises(ValueError):
                completion_transaction(runtime, 5, AT, [{'db/id': 5, 'task-item/responses': responses}], deepcopy(runtime.engine))
        data = records(); del data[9]['answer-field/answer-choices']; runtime = loaded(data)
        valid = [{'db/id': 5, 'task-item/responses': ['typed']},
                 {'db/id': 'typed', 'learner-response/field': 9, 'learner-response/value': 'x^2'}]
        plan = completion_transaction(runtime, 5, AT, valid, deepcopy(runtime.engine))
        self.assertIn(':learner-response/validate', plan.edn)
        for changes in [valid[1:], [valid[0], dict(valid[1], **{'learner-response/field': 13})],
                        [dict(valid[1], **{'db/id': 'engine-global-performance'})]]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                completion_transaction(runtime, 5, AT, changes, deepcopy(runtime.engine))

    def test_expiry_guards_task_without_fabricating_item(self):
        runtime = loaded()
        plan = task_transaction(runtime, 3, AT,
            [{'db/id': 3, 'learner-task/status': Keyword('learner-task.status/completed'),
              'learner-task/outcome': Keyword('learner-task.outcome/passed')}], deepcopy(runtime.engine))
        self.assertEqual(plan.forms[0], (Keyword('db/cas'), 3, Keyword('learner-task/status'), 101,
                                      Keyword('learner-task.status/completed')))
        self.assertNotIn('task-item/', plan.edn)
        self.assertIn(':learner-task/completed-at #inst', plan.edn)
        self.assertTrue(plan.request_key.startswith('expire-task-'))

    def test_edn_keeps_types_and_normalizes_millisecond_instants(self):
        self.assertEqual(edn({'a/id': identity(1), 'a/ref': Keyword('a/value'), 'a/text': 'a/value'}),
                         '{:a/id #uuid "00000000-0000-0000-0000-000000000001" :a/ref :a/value :a/text "a/value"}')
        self.assertEqual(instant(AT.replace(microsecond=123456)).microsecond, 123000)
        for value in [float('nan'), float('inf'), {1, 2}]:
            with self.assertRaises(ValueError): edn(value)
        with self.assertRaises(ValueError): instant(datetime(2026, 9, 28))


if __name__ == '__main__': unittest.main()
