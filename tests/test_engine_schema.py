"""Current-schema loading and atomic item writeback boundary checks."""
from copy import deepcopy
from dataclasses import asdict, replace
from datetime import datetime, timezone, timedelta
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
        5: {'task-item/id': identity(5), 'task-item/content': 8, 'task-item/status': 108},
        6: {'topic/id': identity(6), 'topic/knowledge-points': [7], 'topic/encompasses': [12]},
        7: {'knowledge-point/id': identity(7), 'knowledge-point/questions': [8]},
        8: {'question/id': identity(8), 'question/is-example': False, 'question/answer-fields': [9]},
        9: {'answer-field/id': identity(9), 'answer-field/key': 'answer', 'answer-field/type': 113,
            'answer-field/choices': [10, 11], 'answer-field/correct': 10},
        10: {'answer/id': identity(10), 'answer/type': 114, 'answer/value': 'x^2'},
        11: {'answer/id': identity(11), 'answer/type': 114, 'answer/value': 'x^3'},
        12: {'encompassing/topic': 13, 'encompassing/weight': .25},
        13: {'topic/id': identity(13)},
        100: {'db/ident': Keyword('policy.retention-update/decay-before-add')},
        101: {'db/ident': Keyword('learner-task.status/started')},
        102: {'db/ident': Keyword('learner-task.status/completed')},
        103: {'db/ident': Keyword('task-item.status/correct')},
        104: {'db/ident': Keyword('learner-task.status/failed')},
        105: {'db/ident': Keyword('task-item.status/incorrect')},
        106: {'db/ident': Keyword('learner-task.status/locked')},
        107: {'db/ident': Keyword('learner-task.status/unlocked')},
        108: {'db/ident': Keyword('task-item.status/started')},
        109: {'db/ident': Keyword('task-item.status/paused')},
        110: {'db/ident': Keyword('task-item.status/completed')},
        111: {'db/ident': Keyword('task-item.status/skipped')},
        112: {'db/ident': Keyword('learner-task.status/paused')},
        113: {'db/ident': Keyword('answer-field.type/radio')},
        114: {'db/ident': Keyword('answer.type/math')},
        115: {'db/ident': Keyword('answer-field.type/blank')},
    }


def loaded(data=None, history=None):
    data = records() if data is None else data
    if history is None:
        history = [{'entity': 3, 'attribute': 'learner-task/status', 'value': data[3]['learner-task/status'], 't': 30, 'at': AT - timedelta(seconds=2)}]
        history.extend({'entity': item, 'attribute': 'task-item/status', 'value': data[item]['task-item/status'], 't': 30, 'at': AT - timedelta(seconds=2)} for item in data[3]['learner-task/items'])
    return load_runtime(EntitySnapshot(data, 31, history), 2, 1)


class SchemaTests(unittest.TestCase):
    def test_status_history_is_required_for_timing_and_validates_transaction_evidence(self):
        data = records()
        without_history = loaded(data, history=[])
        with self.assertRaisesRegex(ValueError, 'status history'):
            completion_transaction(without_history, 5, AT,
                [{'db/id': 5, 'task-item/status': Keyword('task-item.status/correct')}],
                deepcopy(without_history.engine))
        history = [dict(event) for event in loaded().snapshot.status_history]
        invalid = [
            [dict(history[0], t=32)],
            [dict(history[0], entity=99999)],
            [dict(history[0], attribute='task-item/status')],
            [dict(history[0], value=103)],
            [history[0], history[0]],
            [history[0], dict(history[1], at=AT)],
            [dict(history[0], t=29, at=AT), history[1]],
            [dict(history[1], value=103)],
        ]
        for events in invalid:
            with self.subTest(events=events), self.assertRaises(ValueError):
                EntitySnapshot(data, 31, events)
        snapshot = EntitySnapshot(data, 31, history)
        history[0]['at'] = AT + timedelta(days=1)
        self.assertEqual(snapshot.first_started(3), AT - timedelta(seconds=2))

    def test_elapsed_summaries_cannot_be_supplied_by_the_caller(self):
        runtime = loaded()
        for change in ({'db/id': 5, 'task-item/status': Keyword('task-item.status/correct'),
                        'task-item/elapsed-seconds': 900},
                       {'db/id': 3, 'learner-task/elapsed-seconds': 900}):
            with self.subTest(change=change), self.assertRaisesRegex(ValueError, 'unsupported'):
                completion_transaction(runtime, 5, AT, [change], deepcopy(runtime.engine))

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
        self.assertEqual(snapshot.eid(':task-item.status/correct'), 103)
        with self.assertRaises(TypeError): snapshot.entity(7)['knowledge-point/questions'] = ()
        for bad in [True, -1, '12']:
            with self.assertRaises(ValueError): EntitySnapshot(data, bad)

    def test_curriculum_neighbors_inform_priors_without_adding_coverage(self):
        data = records()
        data[13]['topic/next'] = [6]
        data[7]['knowledge-point/key-prerequisites'] = [14]
        data[14] = {'topic/id': identity(14)}
        data[15] = {'topic/id': identity(15)}
        data[16] = {'module/id': identity(16), 'module/topics': [6, 15]}
        runtime = loaded(data)
        topic = str(identity(6))
        self.assertEqual(set(runtime.engine.neighborhoods[topic]),
                         {str(identity(i)) for i in (13, 14, 15)})
        # Topic 13 is outside the module but remains an inbound prerequisite;
        # its dependent topic 6 does not become its prerequisite in turn.
        self.assertNotIn(str(identity(13)), runtime.engine.neighborhoods)
        self.assertEqual(runtime.engine.graph.coverage(topic),
                         {topic: 1., str(identity(13)): .25})
        updated = deepcopy(runtime.engine)
        updated.neighborhoods = {}
        with self.assertRaisesRegex(ValueError, 'captured policy'):
            completion_transaction(runtime, 5, AT, [{'db/id': 5, 'task-item/status': Keyword('task-item.status/correct')}], updated)
        for source, target in ((10, 6), (6, 10)):
            invalid = deepcopy(data)
            invalid[source]['topic/next'] = [target]
            with self.subTest(source=source, target=target), self.assertRaisesRegex(ValueError, 'known topics'):
                loaded(invalid)

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
            [{'db/id': 5, 'task-item/status': Keyword('task-item.status/correct'),
              'task-item/responses': [10]}], updated)
        self.assertEqual(plan.compare_basis_t, 31)
        self.assertEqual(plan.forms[0], (Keyword('db/cas'), 5, Keyword('task-item/status'), 108, Keyword('task-item.status/correct')))
        self.assertIn(':task-item/elapsed-seconds 2.0', plan.edn)
        self.assertIn(':progress/validate', plan.edn)
        self.assertIn(':performance/validate', plan.edn)
        self.assertIn(':learner/knowledge-profile ["engine-progress-', plan.edn)
        self.assertIn(':learner/performance "engine-global-performance"', plan.edn)
        self.assertEqual(runtime.engine.states, {})
        self.assertEqual(runtime.engine.global_ability, {})
        changed = completion_transaction(runtime, 5, AT, [{'db/id': 5, 'task-item/status': Keyword('task-item.status/correct')}], updated)
        self.assertEqual(plan.request_key, changed.request_key)
        self.assertNotEqual(plan.edn, changed.edn)
        without_state = completion_transaction(runtime, 5, AT, [{'db/id': 5, 'task-item/status': Keyword('task-item.status/correct')}], deepcopy(runtime.engine))
        self.assertEqual(plan.request_key, without_state.request_key)
        data = records()
        data[3]['learner-task/items'] = [25]
        data[25] = dict(data[5], **{'task-item/id': identity(25)})
        other = loaded(data)
        other_plan = completion_transaction(other, 25, AT, [{'db/id': 25, 'task-item/status': Keyword('task-item.status/correct')}], updated)
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
        plan = completion_transaction(runtime, 5, AT, [{'db/id': 5, 'task-item/status': Keyword('task-item.status/correct')}], updated)
        by_eid = {f['db/id']: f for f in plan.forms if hasattr(f, 'keys')}
        self.assertIn('progress/memory', by_eid[20])
        self.assertIn('performance/practice-mass', by_eid[21])
        self.assertNotIn('learner/knowledge-profile', by_eid[2])
        self.assertNotIn('learner/performance', by_eid[2])
        self.assertNotIn('progress/id', by_eid[20])

    def test_completion_rejects_old_time_terminal_and_changed_inputs(self):
        for modify in [lambda d: d[5].update({'task-item/status': 103}),
                       lambda d: d[3].update({'learner-task/status': 102}),
                       lambda d: d[5].update({'task-item/status': 109})]:
            data = records(); modify(data); runtime = loaded(data)
            with self.assertRaises(ValueError): completion_transaction(runtime, 5, AT, [{'db/id': 5, 'task-item/status': Keyword('task-item.status/correct')}], deepcopy(runtime.engine))
        runtime = loaded(); updated = deepcopy(runtime.engine)
        updated.policy = replace(updated.policy, accuracy_alpha=.3)
        with self.assertRaisesRegex(ValueError, 'captured policy'):
            completion_transaction(runtime, 5, AT, [{'db/id': 5, 'task-item/status': Keyword('task-item.status/correct')}], updated)

    def test_completion_boundaries_require_started_and_reject_removed_outcome(self):
        for status in (102, 104, 106, 107):
            data = records()
            data[3]['learner-task/status'] = status
            runtime = loaded(data)
            for writer, target in ((completion_transaction, 5), (task_transaction, 3)):
                with self.subTest(status=status, writer=writer.__name__), self.assertRaisesRegex(ValueError, 'started'):
                    writer(runtime, target, AT, [], deepcopy(runtime.engine))
        runtime = loaded()
        with self.assertRaisesRegex(ValueError, 'unsupported'):
            completion_transaction(runtime, 5, AT,
                [{'db/id': 3, 'learner-task/outcome': 'passed'}], deepcopy(runtime.engine))
        with self.assertRaisesRegex(ValueError, 'must complete'):
            task_transaction(runtime, 3, AT,
                [{'db/id': 3, 'learner-task/status': Keyword('learner-task.status/failed')}],
                deepcopy(runtime.engine))

    def test_selection_and_entered_response_field_validation(self):
        runtime = loaded()
        for responses in [[10, 11], [13], [True]]:
            with self.subTest(responses=responses), self.assertRaises(ValueError):
                completion_transaction(runtime, 5, AT, [{'db/id': 5, 'task-item/status': Keyword('task-item.status/correct'), 'task-item/responses': responses}], deepcopy(runtime.engine))
        data = records(); data[9]['answer-field/type'] = 115; runtime = loaded(data)
        valid = [{'db/id': 5, 'task-item/status': Keyword('task-item.status/correct'), 'task-item/responses': ['typed']},
                 {'db/id': 'typed', 'field': 9, 'answer/id': identity(15),
                  'answer/type': 114, 'answer/value': '\\frac{'}]
        plan = completion_transaction(runtime, 5, AT, valid, deepcopy(runtime.engine))
        self.assertIn(':answer/validate', plan.edn)
        self.assertIn(':answer-field/choices ["typed"]', plan.edn)
        self.assertIn('\\\\frac{', plan.edn)
        for changes in [valid[1:], [valid[0], dict(valid[1], **{'field': 13})],
                        [dict(valid[1], **{'db/id': 'engine-global-performance'})],
                        [valid[0], dict(valid[1], **{'answer/value': 'x^2'})]]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                completion_transaction(runtime, 5, AT, changes, deepcopy(runtime.engine))

    def test_new_answer_identity_cannot_upsert_existing_or_duplicate_new_value(self):
        data = records()
        data[9]['answer-field/type'] = 115
        runtime = loaded(data)
        item = {'db/id': 5, 'task-item/status': Keyword('task-item.status/incorrect'),
                'task-item/responses': ['typed']}
        answer = {'db/id': 'typed', 'field': 9, 'answer/id': identity(10),
                  'answer/type': 114, 'answer/value': 'malformed {'}
        with self.assertRaisesRegex(ValueError, 'UUID already belongs'):
            completion_transaction(runtime, 5, AT, [item, answer], deepcopy(runtime.engine))
        answer['answer/id'] = identity(15)
        duplicate = dict(answer, **{'db/id': 'other'})
        with self.assertRaisesRegex(ValueError, 'UUID already belongs'):
            completion_transaction(runtime, 5, AT, [item, answer, duplicate], deepcopy(runtime.engine))
        plan = completion_transaction(runtime, 5, AT, [item, answer], deepcopy(runtime.engine))
        self.assertIn('malformed {', plan.edn)

    def test_worked_example_completion_cannot_carry_score_or_responses(self):
        data = records()
        data[8]['question/is-example'] = True
        data[8]['question/worked-solution'] = 'Demonstration.'
        runtime = loaded(data)
        for extra in ({'task-item/performance': 1.0}, {'task-item/responses': [10]}):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                completion_transaction(runtime, 5, AT,
                    [dict({'db/id': 5, 'task-item/status': Keyword('task-item.status/completed')}, **extra)],
                    deepcopy(runtime.engine))
        plan = completion_transaction(runtime, 5, AT,
            [{'db/id': 5, 'task-item/status': Keyword('task-item.status/completed')}],
            deepcopy(runtime.engine))
        self.assertIn(':task-item.status/completed', plan.edn)

    def test_expiry_guards_task_without_fabricating_item(self):
        runtime = loaded()
        plan = task_transaction(runtime, 3, AT,
            [{'db/id': 3, 'learner-task/status': Keyword('learner-task.status/completed')}], deepcopy(runtime.engine))
        self.assertEqual(plan.forms[0], (Keyword('db/cas'), 3, Keyword('learner-task/status'), 101,
                                      Keyword('learner-task.status/completed')))
        self.assertNotIn(':task-item.status/correct', plan.edn)
        self.assertIn(':db/txInstant #inst', plan.edn)
        self.assertIn(':learner-task/elapsed-seconds 2.0', plan.edn)
        self.assertTrue(plan.request_key.startswith('expire-task-'))

    def test_edn_keeps_types_and_normalizes_millisecond_instants(self):
        self.assertEqual(edn({'a/id': identity(1), 'a/ref': Keyword('a/value'), 'a/text': 'a/value'}),
                         '{:a/id #uuid "00000000-0000-0000-0000-000000000001" :a/ref :a/value :a/text "a/value"}')
        self.assertEqual(instant(AT.replace(microsecond=123456)).microsecond, 123000)
        for value in [float('nan'), float('inf'), {1, 2}]:
            with self.assertRaises(ValueError): edn(value)
        with self.assertRaises(ValueError): instant(datetime(2026, 9, 28))


if __name__ == '__main__': unittest.main()
