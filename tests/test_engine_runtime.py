"""Exercise item completion through real schema loading and write generation.

The small fixture writer applies the generated map/CAS forms to an in-memory
entity capture, then reloads it. It is not an EDB implementation or a substitute
for the native transaction/predicate checks.
"""
from collections.abc import Mapping
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
import unittest
from uuid import UUID

from engine.fire import Policy
from engine.runtime import complete_item, expire_task, scope_topics, transition_item
from engine.schema import EntitySnapshot, Keyword, POLICY_FIELDS, load_runtime


START = datetime(2026, 9, 28, tzinfo=timezone.utc)


class RuntimeFixture:
    def __init__(self, kind):
        self.entities = {}
        self.basis = 10
        self.enums = {}
        for index, name in enumerate((
            'policy.retention-update/decay-before-add',
            'task-item.status/started', 'task-item.status/paused', 'task-item.status/completed',
            'task-item.status/correct', 'task-item.status/incorrect', 'task-item.status/skipped',
            'learner-task.status/locked', 'learner-task.status/unlocked',
            'learner-task.status/started', 'learner-task.status/paused', 'learner-task.status/completed',
            'learner-task.status/failed',
            'answer-field.type/blank', 'question.difficulty/moderate', 'answer.type/math',
        ), 9000):
            self.enums[name] = index
            self.entities[index] = {'db/ident': Keyword(name)}
        settings = asdict(Policy())
        self.entities[2] = {'policy/id': UUID(int=2), **{
            'policy/' + attr: settings[field] for attr, field in POLICY_FIELDS.items()
        }}
        self.entities[2]['policy/retention-update-order'] = self.enums['policy.retention-update/decay-before-add']
        self.entities[1] = {'learner/id': 'learner', 'learner/activity': [3]}
        self.entities[3] = {'learner-task/id': UUID(int=3), 'learner-task/activity': 4,
                            'learner-task/status': self.enums['learner-task.status/started'],
                            'learner-task/items': []}
        self.status_history = [{'entity': 3, 'attribute': 'learner-task/status',
                                'value': self.enums['learner-task.status/started'], 't': self.basis, 'at': START}]
        self.entities[10] = {'course/id': UUID(int=10), 'course/title': 'Course', 'course/units': [11]}
        self.entities[11] = {'unit/id': UUID(int=11), 'unit/title': 'Unit', 'unit/modules': [12]}
        self.entities[12] = {'module/id': UUID(int=12), 'module/title': 'Module', 'module/topics': [20, 22, 23]}
        for index, topic in enumerate((20, 21, 22, 23)):
            kp, example = 40 + index, 200 + index
            questions = list(range(100 + 10 * index, 105 + 10 * index))
            self.entities[topic] = {'topic/id': UUID(int=topic), 'topic/title': f'Topic {topic}',
                                    'topic/knowledge-points': [kp]}
            self.entities[kp] = {'knowledge-point/id': UUID(int=kp), 'knowledge-point/title': f'Skill {kp}',
                                'knowledge-point/canonical-example': example,
                                'knowledge-point/questions': questions}
            self.entities[example] = {'question/id': UUID(int=example), 'question/is-example': True,
                                      'question/problem': 'Solve $x+1=2$.',
                                      'question/worked-solution': 'Subtract one: $x=1$.'}
            for question in questions:
                self.entities[question] = {'question/id': UUID(int=question),
                                           'question/is-example': False,
                                           'question/problem': f'Solve $x+{question}=0$; x = {{x}}.',
                                           'question/answer-fields': [2000 + question],
                                           'question/difficulty': self.enums['question.difficulty/moderate']}
                self.entities[2000 + question] = {'answer-field/id': UUID(int=2000 + question),
                                                  'answer-field/key': 'x',
                                                  'answer-field/type': self.enums['answer-field.type/blank'],
                                                  'answer-field/choices': [3000 + question],
                                                  'answer-field/correct': 3000 + question}
                self.entities[3000 + question] = {'answer/id': UUID(int=3000 + question),
                                                  'answer/type': self.enums['answer.type/math'],
                                                  'answer/value': str(-question)}
        activity = {kind + '/id': UUID(int=4)}
        if kind == 'review':
            activity.update({'review/topic': 20, 'review/questions': list(range(100, 105))})
        elif kind == 'lesson':
            self.entities[210] = {'tutorial/id': UUID(int=210), 'tutorial/title': 'Introduction',
                                  'tutorial/content': 'Subtract the constant from both sides.'}
            self.entities[220] = {'lesson-step/id': UUID(int=220), 'lesson-step/index': 1,
                                  'lesson-step/content': 210}
            self.entities[221] = {'lesson-step/id': UUID(int=221), 'lesson-step/index': 2,
                                  'lesson-step/content': 40}
            activity.update({'lesson/topic': 20, 'lesson/steps': [221, 220]})
        elif kind == 'assessment':
            activity.update({'assessment/title': 'Mixed topics', 'assessment/questions': [100, 101, 110]})
        elif kind == 'diagnostic':
            self.entities[21]['topic/next'] = [20]
            for probe, question in ((300, 100), (301, 120), (302, 130), (303, 101)):
                self.entities[probe] = {'diagnostic-probe/id': UUID(int=probe),
                                        'diagnostic-probe/question': question}
            self.entities[300].update({'diagnostic-probe/on-correct': 301,
                                       'diagnostic-probe/on-incorrect': 302,
                                       'diagnostic-probe/on-skipped': 302,
                                       'diagnostic-probe/on-silly-mistake': 303})
            self.entities[303].update({'diagnostic-probe/on-correct': 301,
                                       'diagnostic-probe/on-incorrect': 302,
                                       'diagnostic-probe/on-skipped': 302})
            activity.update({'diagnostic/title': 'Placement', 'diagnostic/scope': 10,
                             'diagnostic/probes': [300, 301, 302, 303], 'diagnostic/start': 300})
        else:
            raise ValueError(kind)
        self.entities[4] = activity

    def seed(self, topic, *, repetitions=0, memory_at=None, interval=1):
        eid = 500 + topic
        self.entities[eid] = {
            'progress/id': f'learner-topic-{topic}', 'progress/topic': topic, 'progress/policy': 2,
            'progress/repetitions': float(repetitions), 'progress/memory': 1.0,
            'progress/memory-at': memory_at or START - timedelta(days=2),
            'progress/interval-days': float(interval), 'progress/learned': True,
            'progress/assessment-accuracy': .8, 'progress/practice-accuracy': .8,
            'progress/assessment-mass': 0., 'progress/practice-mass': 0.,
        }
        self.entities[1].setdefault('learner/knowledge-profile', []).append(eid)

    def load(self):
        return load_runtime(EntitySnapshot(self.entities, self.basis, self.status_history), 1, 2)

    def present(self, content, at=None):
        items = self.entities[3]['learner-task/items']
        index = len(items) + 1
        eid = 1000 + index
        self.entities[eid] = {'task-item/id': UUID(int=eid), 'task-item/content': content,
                              'task-item/status': self.enums['task-item.status/started']}
        self.basis += 1
        self.status_history.append({'entity': eid, 'attribute': 'task-item/status',
                                    'value': self.enums['task-item.status/started'], 't': self.basis,
                                    'at': at or max(e['at'] for e in self.status_history)})
        if items:
            tail = next(item for item in items if 'task-item/next' not in self.entities[item])
            self.entities[tail]['task-item/next'] = eid
        items.append(eid)
        return eid

    def apply(self, plan):
        """Apply exactly the emitted fixture facts; use the real loader next."""
        if plan.compare_basis_t != self.basis:
            raise ValueError('fixture basis conflict')
        records = deepcopy(self.entities)
        tempids = {}
        for form in plan.forms:
            if isinstance(form, Mapping) and isinstance(form['db/id'], str) and form['db/id'] != 'edb.tx':
                tempid = form['db/id']
                if tempid not in tempids:
                    eid = max(records) + 1
                    tempids[tempid] = eid
                    records[eid] = {}
        def resolve(value):
            if isinstance(value, Keyword):
                return self.enums[str(value)]
            if isinstance(value, str) and value in tempids:
                return tempids[value]
            return value
        tx_at = next(form['db/txInstant'] for form in plan.forms if isinstance(form, Mapping) and form.get('db/id') == 'edb.tx')
        def record_status(eid, attr, value):
            if attr in {'task-item/status', 'learner-task/status'} and records[eid].get(attr) != value:
                self.status_history.append({'entity': eid, 'attribute': attr, 'value': value, 't': self.basis + 1, 'at': tx_at})
        for form in plan.forms:
            if isinstance(form, Mapping):
                if form['db/id'] == 'edb.tx':
                    continue
                target = resolve(form['db/id'])
                for attr, value in form.items():
                    if attr in {'db/id', 'db/ensure'}:
                        continue
                    if isinstance(value, (tuple, list)):
                        existing = records[target].setdefault(attr, [])
                        for ref in value:
                            if resolve(ref) not in existing:
                                existing.append(resolve(ref))
                    else:
                        record_status(target, attr, resolve(value))
                        records[target][attr] = resolve(value)
            elif str(form[0]) == 'db/cas':
                _, eid, attr, old, new = form
                if records[eid].get(str(attr)) != resolve(old):
                    raise ValueError('fixture CAS conflict')
                record_status(eid, str(attr), resolve(new))
                records[eid][str(attr)] = resolve(new)
            elif str(form[0]) == 'db/retract':
                _, eid, attr, old = form
                if records[eid].get(str(attr)) == old:
                    del records[eid][str(attr)]
            else:
                raise AssertionError(f'unsupported fixture form {form!r}')
        self.entities = records
        self.basis += 1

    def answer(self, content, result=None, *, seconds=None, **kwargs):
        eid = self.present(content)
        loaded = self.load()
        before = loaded.engine.snapshot()
        completed_at = START + timedelta(seconds=seconds or len(self.entities[3]['learner-task/items']))
        completion = complete_item(loaded, eid, completed_at=completed_at, result=result, **kwargs)
        if loaded.engine.snapshot() != before:
            raise AssertionError('completion mutated the source engine')
        self.apply(completion.transaction)
        return completion

    def state(self, topic):
        loaded = self.load()
        return loaded.engine.states[loaded.learner][loaded.topic_eid_to_id[topic]]


class RuntimeTests(unittest.TestCase):
    def test_pause_resume_timing_comes_from_history_and_sums_instruction_time(self):
        fixture = RuntimeFixture('lesson')
        item = fixture.present(210, at=START)
        loaded = fixture.load()
        before = loaded.engine.snapshot()
        paused = transition_item(loaded, item, 'paused', START + timedelta(seconds=5))
        self.assertEqual(loaded.engine.snapshot(), before)
        self.assertEqual(paused, transition_item(loaded, item, 'paused', START + timedelta(seconds=5)))
        self.assertEqual(paused.forms[0], (Keyword('db/cas'), item, Keyword('task-item/status'),
                         fixture.enums['task-item.status/started'], Keyword('task-item.status/paused')))
        fixture.apply(paused)
        self.assertEqual(fixture.entities[item]['task-item/elapsed-seconds'], 5)
        self.assertEqual(fixture.entities[3]['learner-task/elapsed-seconds'], 5)
        self.assertEqual(fixture.load().snapshot.item_elapsed(item, START + timedelta(seconds=15)), 5)
        with self.assertRaisesRegex(ValueError, 'started item'):
            complete_item(fixture.load(), item, completed_at=START + timedelta(seconds=15))
        fixture.apply(transition_item(fixture.load(), item, 'started', START + timedelta(seconds=15)))
        completed = complete_item(fixture.load(), item, completed_at=START + timedelta(seconds=20))
        fixture.apply(completed.transaction)
        self.assertEqual(fixture.entities[item]['task-item/elapsed-seconds'], 10)
        self.assertEqual(fixture.load().snapshot.item_completed_at(item), START + timedelta(seconds=20))
        example = fixture.present(200, at=START + timedelta(seconds=25))
        completed = complete_item(fixture.load(), example, completed_at=START + timedelta(seconds=30))
        fixture.apply(completed.transaction)
        self.assertEqual(fixture.entities[example]['task-item/elapsed-seconds'], 5)
        self.assertEqual(fixture.entities[3]['learner-task/elapsed-seconds'], 15)
        self.assertNotIn('learner', fixture.load().engine.global_ability)

    def test_pause_does_not_extend_exam_deadline_and_expiry_closes_paused_task(self):
        fixture = RuntimeFixture('assessment')
        fixture.entities[4]['assessment/time-limit-seconds'] = 60.
        item = fixture.present(100, at=START)
        fixture.apply(transition_item(fixture.load(), item, 'paused', START + timedelta(seconds=10)))
        fixture.entities[3]['learner-task/status'] = fixture.enums['learner-task.status/paused']
        fixture.basis += 1
        fixture.status_history.append({'entity': 3, 'attribute': 'learner-task/status',
            'value': fixture.enums['learner-task.status/paused'], 't': fixture.basis, 'at': START + timedelta(seconds=10)})
        with self.assertRaisesRegex(ValueError, 'not expired'):
            expire_task(fixture.load(), 3, completed_at=START + timedelta(seconds=59))
        completed = expire_task(fixture.load(), 3, completed_at=START + timedelta(seconds=60))
        fixture.apply(completed.transaction)
        self.assertEqual(fixture.entities[3]['learner-task/elapsed-seconds'], 10)
        self.assertEqual(fixture.entities[item]['task-item/status'], fixture.enums['task-item.status/paused'])
        self.assertIsNone(fixture.load().snapshot.item_completed_at(item))
        with self.assertRaises(ValueError):
            transition_item(fixture.load(), item, 'started', START + timedelta(seconds=61))

        fixture = RuntimeFixture('assessment')
        fixture.entities[4]['assessment/time-limit-seconds'] = 60.
        item = fixture.present(100, at=START)
        fixture.apply(transition_item(fixture.load(), item, 'paused', START + timedelta(seconds=10)))
        fixture.apply(transition_item(fixture.load(), item, 'started', START + timedelta(seconds=59)))
        with self.assertRaisesRegex(ValueError, 'time limit'):
            complete_item(fixture.load(), item, completed_at=START + timedelta(seconds=61), result=True)
        completed = expire_task(fixture.load(), 3, completed_at=START + timedelta(seconds=60))
        fixture.apply(completed.transaction)
        self.assertEqual(fixture.entities[item]['task-item/elapsed-seconds'], 11)
        self.assertEqual(fixture.entities[3]['learner-task/elapsed-seconds'], 11)
        self.assertEqual(fixture.entities[item]['task-item/status'], fixture.enums['task-item.status/paused'])

    def test_resuming_cannot_overlap_another_active_item_for_the_learner(self):
        fixture = RuntimeFixture('review')
        first = fixture.present(100)
        fixture.apply(transition_item(fixture.load(), first, 'paused', START + timedelta(seconds=1)))
        fixture.entities[4000] = {'learner-task/id': UUID(int=4000), 'learner-task/activity': 4,
            'learner-task/status': fixture.enums['learner-task.status/started'], 'learner-task/items': [4001]}
        fixture.entities[4001] = {'task-item/id': UUID(int=4001), 'task-item/content': 101,
            'task-item/status': fixture.enums['task-item.status/started']}
        fixture.entities[1]['learner/activity'].append(4000)
        fixture.basis += 1
        for eid, attr in ((4000, 'learner-task/status'), (4001, 'task-item/status')):
            fixture.status_history.append({'entity': eid, 'attribute': attr, 'value': fixture.entities[eid][attr],
                                          't': fixture.basis, 'at': START + timedelta(seconds=1)})
        with self.assertRaisesRegex(ValueError, 'one item'):
            transition_item(fixture.load(), first, 'started', START + timedelta(seconds=2))

    def test_next_chain_order_controls_completion_and_expiry_not_entity_ids(self):
        def present(fixture, eid, question):
            original = fixture.present(question)
            fixture.entities[eid] = fixture.entities.pop(original)
            fixture.entities[eid]['task-item/id'] = UUID(int=eid)
            fixture.status_history[-1]['entity'] = eid
            fixture.entities[3]['learner-task/items'] = list(reversed([
                eid if item == original else item for item in fixture.entities[3]['learner-task/items']]))
            for entity in fixture.entities.values():
                if entity.get('task-item/next') == original:
                    entity['task-item/next'] = eid
        for finish_all in (False, True):
            fixture = RuntimeFixture('assessment')
            fixture.seed(20)
            fixture.seed(21)
            fixture.entities[4]['assessment/time-limit-seconds'] = 60.
            sequence = ((700, 100), (600, 110), (800, 101)) if finish_all else ((700, 100),)
            for second, (eid, question) in enumerate(sequence, 1):
                present(fixture, eid, question)
                completed = complete_item(fixture.load(), eid,
                    completed_at=START + timedelta(seconds=second), result=True)
                fixture.apply(completed.transaction)
            if not finish_all:
                present(fixture, 600, 110)
                completed = expire_task(fixture.load(), 3, completed_at=START + timedelta(seconds=60))
                fixture.apply(completed.transaction)
                self.assertIsNone(fixture.load().snapshot.item_completed_at(600))
            self.assertTrue(completed.delivery.complete)

        fixture = RuntimeFixture('assessment')
        fixture.entities[4]['assessment/time-limit-seconds'] = 60.
        completed = expire_task(fixture.load(), 3, completed_at=START + timedelta(seconds=60))
        self.assertTrue(completed.delivery.complete)
        self.assertEqual(fixture.entities[3]['learner-task/items'], [])

    def test_malformed_task_item_chains_rejected_before_completion_or_expiry(self):
        for problem in ('multiple-heads', 'merge', 'cycle', 'disconnected-cycle',
                        'foreign-next', 'foreign-predecessor', 'shared-item'):
            fixture = RuntimeFixture('assessment')
            fixture.entities[4]['assessment/time-limit-seconds'] = 60.
            a, b, c = (fixture.present(q) for q in (100, 110, 101))
            if problem == 'multiple-heads':
                del fixture.entities[a]['task-item/next']
            elif problem == 'merge':
                fixture.entities[a]['task-item/next'] = c
            elif problem == 'cycle':
                fixture.entities[c]['task-item/next'] = a
            elif problem == 'disconnected-cycle':
                del fixture.entities[a]['task-item/next']
                fixture.entities[c]['task-item/next'] = b
            else:
                fixture.entities[6000] = {'task-item/id': UUID(int=6000), 'task-item/content': 100}
                fixture.entities[5000] = {'learner-task/id': UUID(int=5000),
                                         'learner-task/items': [a if problem == 'shared-item' else 6000]}
                if problem == 'foreign-next':
                    fixture.entities[c]['task-item/next'] = 6000
                elif problem == 'foreign-predecessor':
                    fixture.entities[6000]['task-item/next'] = a
            loaded = fixture.load()
            before = loaded.engine.snapshot()
            with self.subTest(problem=problem), self.assertRaises(ValueError):
                complete_item(loaded, a, completed_at=START + timedelta(seconds=1), result=True)
            with self.subTest(problem=problem), self.assertRaises(ValueError):
                expire_task(loaded, 3, completed_at=START + timedelta(seconds=60))
            self.assertEqual(loaded.engine.snapshot(), before)

    def test_only_started_tasks_accept_answers_or_timer_expiry(self):
        for status in ('locked', 'unlocked', 'completed', 'failed'):
            fixture = RuntimeFixture('assessment')
            fixture.entities[4]['assessment/time-limit-seconds'] = 60.
            fixture.entities[3]['learner-task/status'] = fixture.enums['learner-task.status/' + status]
            fixture.status_history[0]['value'] = fixture.enums['learner-task.status/' + status]
            item = fixture.present(100)
            loaded = fixture.load()
            before = loaded.engine.snapshot()
            with self.subTest(status=status), self.assertRaisesRegex(ValueError, 'started'):
                complete_item(loaded, item, completed_at=START + timedelta(seconds=1), result=True)
            with self.subTest(status=status), self.assertRaisesRegex(ValueError, 'started'):
                expire_task(loaded, 3, completed_at=START + timedelta(seconds=60))
            self.assertEqual(loaded.engine.snapshot(), before)

    def test_next_edges_supply_inbound_foundations_without_requiring_dependents(self):
        fixture = RuntimeFixture('lesson')
        fixture.entities[21]['topic/next'] = [20]
        fixture.entities[23]['topic/next'] = [21]
        fixture.entities[20]['topic/next'] = [22]
        snapshot = fixture.load().snapshot
        self.assertEqual(scope_topics(snapshot, 20), {20, 21, 23})
        self.assertEqual(scope_topics(snapshot, 10), {20, 21, 22, 23})

        fixture = RuntimeFixture('lesson')
        fixture.entities[20]['topic/next'] = [21]
        # An unlearned dependent is not a readiness requirement for its prerequisite.
        self.assertEqual(fixture.answer(210).delivery.next_content, (200,))

    def test_review_answers_count_once_and_three_correct_close_one_retention_unit(self):
        fixture = RuntimeFixture('review')
        fixture.seed(20)
        for index, question in enumerate((100, 101, 102), 1):
            completed = fixture.answer(question, True)
            state = fixture.state(20)
            self.assertEqual(state.ability.practice_mass, index)
            self.assertEqual(fixture.load().engine.global_ability['learner'].practice_mass, index)
            retention = [r for r in completed.engine.receipts.values() if r['mode'] == 'retention']
            if index < 3:
                self.assertFalse(completed.delivery.complete)
                self.assertEqual(state.repetitions, 0)
                self.assertEqual(retention, [])
            else:
                self.assertTrue(completed.delivery.passed)
                self.assertEqual(len(retention), 1)
                self.assertGreater(state.repetitions, 1)
                self.assertIn(':learner-task.status/completed', completed.transaction.edn)
        self.assertEqual(len(fixture.entities[3]['learner-task/items']), 3)
        self.assertNotIn('learner-task/outcome', fixture.entities[3])

    def test_lesson_requires_tutorial_example_and_two_correct_before_mastery(self):
        fixture = RuntimeFixture('lesson')
        tutorial = fixture.answer(210)
        self.assertEqual(tutorial.delivery.next_content, (200,))
        self.assertNotIn('learner', tutorial.engine.global_ability)
        example = fixture.answer(200)
        self.assertEqual(set(example.delivery.next_content), set(range(100, 105)))
        first = fixture.answer(100, True)
        self.assertFalse(first.delivery.complete)
        self.assertFalse(fixture.state(20).learned)
        last = fixture.answer(101, True)
        self.assertTrue(last.delivery.complete)
        self.assertTrue(fixture.state(20).learned)
        self.assertEqual(fixture.state(20).evidence_mass, 2)
        self.assertEqual(fixture.load().engine.global_ability['learner'].practice_mass, 2)

    def test_failed_first_lesson_retains_answers_without_learning(self):
        fixture = RuntimeFixture('lesson')
        fixture.answer(210)
        fixture.answer(200)
        for question, result in zip(range(100, 105), (True, False, True, False, True)):
            completed = fixture.answer(question, result)
        self.assertTrue(completed.delivery.complete)
        self.assertFalse(completed.delivery.passed)
        state = fixture.state(20)
        self.assertFalse(state.learned)
        self.assertEqual((state.repetitions, state.memory, state.evidence_mass), (0, 0, 5))
        self.assertIn(':learner-task.status/failed', completed.transaction.edn)
        self.assertEqual(fixture.entities[3]['learner-task/status'], fixture.enums['learner-task.status/failed'])
        self.assertNotIn('learner-task/outcome', fixture.entities[3])

    def test_failed_review_ends_with_failed_status(self):
        fixture = RuntimeFixture('review')
        fixture.seed(20, repetitions=3)
        for question, result in zip(range(100, 105), (True, True, False, False, True)):
            completed = fixture.answer(question, result)
        self.assertFalse(completed.delivery.passed)
        self.assertEqual(fixture.entities[3]['learner-task/status'], fixture.enums['learner-task.status/failed'])
        self.assertLess(fixture.state(20).repetitions, 3)

    def test_exhausted_lesson_bank_commits_the_answer_and_requests_more_questions(self):
        fixture = RuntimeFixture('lesson')
        fixture.entities[40]['knowledge-point/questions'] = [100]
        fixture.answer(210)
        fixture.answer(200)
        completed = fixture.answer(100, True)
        self.assertFalse(completed.delivery.complete)
        self.assertEqual(completed.delivery.next_content, ())
        self.assertEqual(completed.delivery.needs_questions_for, 40)
        self.assertEqual(fixture.state(20).evidence_mass, 1)
        self.assertFalse(fixture.state(20).learned)
        self.assertEqual(fixture.entities[1003]['task-item/status'], fixture.enums['task-item.status/correct'])

    def test_assessment_updates_each_topic_and_global_assessment_channel(self):
        fixture = RuntimeFixture('assessment')
        fixture.seed(20, repetitions=3)
        fixture.seed(21, repetitions=3)
        fixture.answer(100, True)
        self.assertEqual(fixture.state(21).evidence_mass, 0)
        fixture.answer(110, False)
        completed = fixture.answer(101, True)
        self.assertTrue(completed.delivery.complete)
        self.assertIsNone(completed.delivery.passed)
        self.assertEqual(fixture.entities[3]['learner-task/status'], fixture.enums['learner-task.status/completed'])
        self.assertGreater(fixture.state(20).repetitions, 3)
        self.assertLess(fixture.state(21).repetitions, 3)
        self.assertEqual(fixture.state(20).ability.assessment_mass, 2)
        self.assertEqual(fixture.state(21).ability.assessment_mass, 1)
        global_ability = fixture.load().engine.global_ability['learner']
        self.assertEqual((global_ability.assessment_mass, global_ability.practice_mass), (3, 0))

    def test_explicit_review_skip_records_presentation_without_accuracy(self):
        fixture = RuntimeFixture('review')
        fixture.seed(20)
        completed = fixture.answer(100, None)
        self.assertFalse(completed.delivery.complete)
        self.assertEqual(fixture.state(20).evidence_mass, 0)
        self.assertEqual(fixture.state(20).repetitions, 0)
        self.assertNotIn('learner', fixture.load().engine.global_ability)
        self.assertIn(':task-item.status/skipped', completed.transaction.edn)
        self.assertNotIn('task-item/performance', fixture.entities[1001])

    def test_skip_rejects_an_existing_entered_response(self):
        fixture = RuntimeFixture('review')
        fixture.seed(20)
        eid = fixture.present(100)
        fixture.entities[eid]['task-item/responses'] = [3100]
        loaded = fixture.load()
        before = loaded.engine.snapshot()
        with self.assertRaisesRegex(ValueError, 'skipped question cannot contain submitted responses'):
            complete_item(loaded, eid, completed_at=START + timedelta(seconds=1), result=None)
        self.assertEqual(loaded.engine.snapshot(), before)

    def test_diagnostic_retry_fork_must_have_unambiguous_question_history(self):
        fixture = RuntimeFixture('diagnostic')
        fixture.entities[302]['diagnostic-probe/question'] = 101
        eid = fixture.present(100)
        loaded = fixture.load()
        before = loaded.engine.snapshot()
        with self.assertRaises(ValueError):
            complete_item(loaded, eid, completed_at=START + timedelta(seconds=1),
                          result=False, take_retry=True)
        self.assertEqual(loaded.engine.snapshot(), before)
        # Sharing the same probe would hide whether the original result should
        # be replaced for placement, even though delivery itself is unambiguous.
        fixture = RuntimeFixture('diagnostic')
        fixture.entities[300]['diagnostic-probe/on-incorrect'] = 303
        with self.assertRaisesRegex(ValueError, 'must be distinguishable'):
            fixture.answer(100, False, take_retry=True)

    def test_diagnostic_retry_needs_choice_and_preserves_both_submitted_answers(self):
        fixture = RuntimeFixture('diagnostic')
        eid = fixture.present(100)
        loaded = fixture.load()
        before = loaded.engine.snapshot()
        with self.assertRaisesRegex(ValueError, 'choose whether'):
            complete_item(loaded, eid, completed_at=START + timedelta(seconds=1), result=False)
        self.assertEqual(loaded.engine.snapshot(), before)
        first = complete_item(loaded, eid, completed_at=START + timedelta(seconds=1),
                              result=False, take_retry=True)
        self.assertEqual(first.delivery.next_content, (101,))
        fixture.apply(first.transaction)
        retry = fixture.answer(101, True)
        self.assertEqual(retry.delivery.next_content, (120,))
        completed = fixture.answer(120, True)
        self.assertTrue(completed.delivery.complete)
        self.assertTrue(fixture.state(20).learned)
        self.assertEqual(fixture.state(20).repetitions, 1)  # Retry replaces the original -1.
        self.assertEqual(fixture.state(20).evidence_mass, 2)
        self.assertEqual(fixture.state(21).repetitions, 1)  # Implied prerequisite evidence.
        self.assertEqual(fixture.state(22).repetitions, 1)
        loaded = fixture.load()
        self.assertNotIn(loaded.topic_eid_to_id[23], loaded.engine.states['learner'])
        self.assertEqual(loaded.engine.global_ability['learner'].practice_mass, 3)
        self.assertEqual(len(fixture.entities[3]['learner-task/items']), 3)

    def test_diagnostic_retry_uses_its_own_weight_for_the_whole_frontier(self):
        fixture = RuntimeFixture('diagnostic')
        fixture.entities[20]['topic/next'] = [22]
        fixture.answer(100, False, take_retry=True)
        fixture.answer(101, True, performance=.25)
        fixture.answer(120, True, performance=.5)
        # The original wrong answer must not keep penalizing postrequisites.
        self.assertEqual(fixture.state(20).repetitions, .75)
        self.assertEqual(fixture.state(21).repetitions, .75)
        self.assertEqual(fixture.state(22).repetitions, .5)

    def test_same_topic_ordinary_continuation_does_not_replace_original(self):
        fixture = RuntimeFixture('diagnostic')
        fixture.entities[302]['diagnostic-probe/question'] = 102
        fixture.answer(100, False, take_retry=False)
        fixture.answer(102, True)
        self.assertFalse(fixture.state(20).learned)  # Ordinary -1 + 1 still balances to zero.
        self.assertEqual(fixture.state(20).evidence_mass, 2)

    def test_incorrect_or_skipped_retry_contributes_one_negative_not_two(self):
        for result in (False, None):
            with self.subTest(result=result):
                fixture = RuntimeFixture('diagnostic')
                fixture.entities[20]['topic/next'] = [23]
                fixture.entities[304] = {'diagnostic-probe/id': UUID(int=304),
                                         'diagnostic-probe/question': 131}
                fixture.entities[4]['diagnostic/probes'].append(304)
                fixture.entities[302]['diagnostic-probe/on-correct'] = 304
                fixture.answer(100, False, take_retry=True)
                fixture.answer(101, result)
                fixture.answer(130, True)
                fixture.answer(131, True)
                # Two subsequent positives outweigh one retry negative. Keeping
                # the original negative too would incorrectly leave balance zero.
                self.assertEqual(fixture.state(20).repetitions, 1)
                self.assertEqual(fixture.state(23).repetitions, 1)

    def test_declined_retry_and_explicit_skip_follow_their_real_branches(self):
        for result, options, answer_count in ((False, {'take_retry': False}, 2), (None, {}, 1)):
            with self.subTest(result=result):
                fixture = RuntimeFixture('diagnostic')
                first = fixture.answer(100, result, **options)
                self.assertEqual(first.delivery.next_content, (130,))
                last = fixture.answer(130, True)
                self.assertTrue(last.delivery.complete)
                loaded = fixture.load()
                self.assertEqual(loaded.engine.global_ability['learner'].practice_mass, answer_count)
                self.assertNotIn(loaded.topic_eid_to_id[21], loaded.engine.states['learner'])
                self.assertNotIn(loaded.topic_eid_to_id[22], loaded.engine.states['learner'])
                self.assertTrue(fixture.state(23).learned)

    def test_diagnostic_positive_weight_places_foundations_without_phantom_skips(self):
        fixture = RuntimeFixture('diagnostic')
        fixture.answer(100, True, performance=.25)
        completed = fixture.answer(120, True)
        self.assertTrue(completed.delivery.complete)
        self.assertEqual(fixture.state(20).repetitions, .25)
        self.assertEqual(fixture.state(21).repetitions, .25)
        self.assertEqual(fixture.state(21).evidence_mass, 0)
        self.assertEqual(fixture.state(22).repetitions, 1)
        self.assertEqual([fixture.entities[e]['task-item/content']
                          for e in fixture.entities[3]['learner-task/items']], [100, 120])

    def test_late_rejection_and_retries_do_not_mutate_loaded_engine(self):
        fixture = RuntimeFixture('review')
        fixture.seed(20)
        eid = fixture.present(100)
        loaded = fixture.load()
        before = loaded.engine.snapshot()
        args = {'completed_at': START + timedelta(seconds=1), 'result': True}
        with self.assertRaisesRegex(ValueError, 'XP can be awarded only at completion'):
            complete_item(loaded, eid, **args, xp_award=7)
        self.assertEqual(loaded.engine.snapshot(), before)
        accepted = complete_item(loaded, eid, **args)
        retry = complete_item(loaded, eid, **args)
        self.assertEqual(accepted.transaction, retry.transaction)
        self.assertEqual(loaded.engine.snapshot(), before)
        fixture.apply(accepted.transaction)
        # Exact transaction retries belong to EDB's native request receipts;
        # this fixture writer deliberately does not emulate that subsystem.
        with self.assertRaisesRegex(ValueError, 'only a started item'):
            complete_item(fixture.load(), eid, **args)
        self.assertEqual(fixture.state(20).evidence_mass, 1)

    def test_authored_sequence_and_unready_prerequisite_cannot_be_bypassed(self):
        for prerequisite in (False, True):
            with self.subTest(prerequisite=prerequisite):
                fixture = RuntimeFixture('lesson')
                if prerequisite:
                    fixture.entities[21]['topic/next'] = [20]
                eid = fixture.present(210 if prerequisite else 100)
                loaded = fixture.load()
                before = loaded.engine.snapshot()
                with self.assertRaises(ValueError):
                    complete_item(loaded, eid, completed_at=START + timedelta(seconds=1),
                                  result=None if prerequisite else True)
                self.assertEqual(loaded.engine.snapshot(), before)

    def test_diagnostic_retry_rejects_equal_but_non_enum_difficulties(self):
        fixture = RuntimeFixture('diagnostic')
        fixture.entities[100]['question/difficulty'] = .5
        fixture.entities[101]['question/difficulty'] = .5
        eid = fixture.present(100)
        loaded = fixture.load()
        before = loaded.engine.snapshot()
        with self.assertRaises(ValueError):
            complete_item(loaded, eid, completed_at=START + timedelta(seconds=1),
                          result=False, take_retry=True)
        self.assertEqual(loaded.engine.snapshot(), before)

    def test_skip_cannot_insert_older_evidence(self):
        fixture = RuntimeFixture('review')
        fixture.seed(20)
        fixture.answer(100, True, seconds=10)
        eid = fixture.present(101)
        loaded = fixture.load()
        before = loaded.engine.snapshot()
        with self.assertRaisesRegex(ValueError, 'predates accepted learner evidence'):
            complete_item(loaded, eid, completed_at=START + timedelta(seconds=5), result=None)
        self.assertEqual(loaded.engine.snapshot(), before)

    def test_assessment_timer_closes_without_answers_for_pending_questions(self):
        fixture = RuntimeFixture('assessment')
        fixture.seed(20)
        fixture.seed(21)
        fixture.entities[4]['assessment/time-limit-seconds'] = 60.
        fixture.entities[3]['learner-task/xp-base'] = 15
        fixture.answer(100, True)
        pending = fixture.present(110)
        loaded = fixture.load()
        before = loaded.engine.snapshot()
        with self.assertRaisesRegex(ValueError, 'has not expired'):
            expire_task(loaded, 3, completed_at=START + timedelta(seconds=59))
        completed = expire_task(loaded, 3, completed_at=START + timedelta(seconds=60))
        self.assertEqual(loaded.engine.snapshot(), before)
        self.assertTrue(completed.delivery.complete)
        fixture.apply(completed.transaction)
        self.assertEqual(fixture.entities[3]['learner-task/status'], fixture.enums['learner-task.status/completed'])
        self.assertEqual(fixture.entities[pending]['task-item/status'], fixture.enums['task-item.status/paused'])
        self.assertIsNone(fixture.load().snapshot.item_completed_at(pending))
        self.assertNotIn('learner-task/xp-earned', fixture.entities[3])
        self.assertEqual(fixture.state(20).evidence_mass, 1)
        self.assertEqual(fixture.state(21).evidence_mass, 0)
        self.assertEqual(fixture.load().engine.global_ability['learner'].assessment_mass, 1)
        with self.assertRaises(ValueError):
            expire_task(fixture.load(), 3, completed_at=START + timedelta(seconds=60))

    def test_diagnostic_timer_places_only_observed_positive_evidence(self):
        fixture = RuntimeFixture('diagnostic')
        fixture.entities[4]['diagnostic/time-limit-seconds'] = 60.
        fixture.answer(100, True, performance=.5)
        pending = fixture.present(120)
        loaded = fixture.load()
        self.assertFalse(fixture.state(20).learned)
        completed = expire_task(loaded, 3, completed_at=START + timedelta(seconds=60))
        fixture.apply(completed.transaction)
        self.assertEqual(fixture.state(20).repetitions, .5)
        self.assertEqual(fixture.state(21).repetitions, .5)
        reloaded = fixture.load()
        self.assertNotIn(reloaded.topic_eid_to_id[22], reloaded.engine.states['learner'])
        self.assertEqual(reloaded.engine.global_ability['learner'].practice_mass, 1)
        self.assertEqual(fixture.entities[pending]['task-item/status'], fixture.enums['task-item.status/paused'])

    def test_unanswered_diagnostic_retry_does_not_erase_original_evidence(self):
        fixture = RuntimeFixture('diagnostic')
        fixture.entities[4]['diagnostic/time-limit-seconds'] = 60.
        fixture.answer(100, False, take_retry=True)
        pending = fixture.present(101)
        completed = expire_task(fixture.load(), 3, completed_at=START + timedelta(seconds=60))
        fixture.apply(completed.transaction)
        self.assertFalse(fixture.state(20).learned)
        self.assertEqual(fixture.state(20).evidence_mass, 1)
        self.assertEqual(fixture.entities[pending]['task-item/status'], fixture.enums['task-item.status/paused'])


if __name__ == '__main__':
    unittest.main()
