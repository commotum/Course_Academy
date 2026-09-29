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
from engine.runtime import complete_item, expire_task
from engine.schema import EntitySnapshot, Keyword, POLICY_FIELDS, load_runtime


START = datetime(2026, 9, 28, tzinfo=timezone.utc)


class RuntimeFixture:
    def __init__(self, kind):
        self.entities = {}
        self.basis = 10
        self.enums = {}
        for index, name in enumerate((
            'policy.retention-update/decay-before-add',
            'task-item.result/correct', 'task-item.result/incorrect', 'task-item.result/skipped',
            'learner-task.status/in-progress', 'learner-task.status/completed',
            'learner-task.outcome/passed', 'learner-task.outcome/failed',
            'question.type/fill-in-the-blank', 'question.difficulty/moderate', 'answer.type/math',
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
                            'learner-task/status': self.enums['learner-task.status/in-progress'],
                            'learner-task/started-at': START, 'learner-task/items': []}
        self.entities[10] = {'course/id': UUID(int=10), 'course/title': 'Course', 'course/units': [11]}
        self.entities[11] = {'unit/id': UUID(int=11), 'unit/title': 'Unit', 'unit/modules': [12]}
        self.entities[12] = {'module/id': UUID(int=12), 'module/title': 'Module', 'module/topics': [20, 22, 23]}
        for index, topic in enumerate((20, 21, 22, 23)):
            kp, example = 40 + index, 200 + index
            questions = list(range(100 + 10 * index, 105 + 10 * index))
            self.entities[topic] = {'topic/id': UUID(int=topic), 'topic/title': f'Topic {topic}',
                                    'topic/knowledge-points': [kp]}
            self.entities[kp] = {'knowledge-point/id': UUID(int=kp), 'knowledge-point/title': f'Skill {kp}',
                                'knowledge-point/example': example,
                                'knowledge-point/questions': questions}
            self.entities[example] = {'example/id': UUID(int=example), 'example/problem': 'Solve $x+1=2$.',
                                      'example/explanation': 'Subtract one: $x=1$.'}
            for question in questions:
                self.entities[question] = {'question/id': UUID(int=question),
                                           'question/type': self.enums['question.type/fill-in-the-blank'],
                                           'question/problem': f'Solve $x+{question}=0$; x = {{x}}.',
                                           'question/answer-fields': [2000 + question],
                                           'question/difficulty': self.enums['question.difficulty/moderate']}
                self.entities[2000 + question] = {'answer-field/id': UUID(int=2000 + question),
                                                  'answer-field/key': 'x',
                                                  'answer-field/correct-answer': 3000 + question}
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
            self.entities[20]['topic/prerequisites'] = [21]
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
        return load_runtime(EntitySnapshot(self.entities, self.basis), 1, 2)

    def present(self, content):
        index = len(self.entities[3]['learner-task/items']) + 1
        eid = 1000 + index
        self.entities[eid] = {'task-item/id': UUID(int=eid), 'task-item/index': index,
                              'task-item/content': content}
        self.entities[3]['learner-task/items'].append(eid)
        return eid

    def apply(self, plan):
        """Apply exactly the emitted fixture facts; use the real loader next."""
        if plan.compare_basis_t != self.basis:
            raise ValueError('fixture basis conflict')
        records = deepcopy(self.entities)
        tempids = {}
        for form in plan.forms:
            if isinstance(form, Mapping) and isinstance(form['db/id'], str):
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
        for form in plan.forms:
            if isinstance(form, Mapping):
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
                        records[target][attr] = resolve(value)
            elif str(form[0]) == 'db/cas':
                _, eid, attr, old, new = form
                if records[eid].get(str(attr)) != resolve(old):
                    raise ValueError('fixture CAS conflict')
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
                self.assertIn(':learner-task.outcome/passed', completed.transaction.edn)
        self.assertEqual(len(fixture.entities[3]['learner-task/items']), 3)

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
        self.assertIn(':learner-task.outcome/failed', completed.transaction.edn)

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
        self.assertEqual(fixture.entities[1003]['task-item/result'], fixture.enums['task-item.result/correct'])

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
        self.assertIn(':task-item.result/skipped', completed.transaction.edn)
        self.assertNotIn('task-item/performance', fixture.entities[1001])

    def test_skip_rejects_an_existing_entered_response(self):
        fixture = RuntimeFixture('review')
        fixture.seed(20)
        eid = fixture.present(100)
        fixture.entities[800] = {'learner-response/field': 2100, 'learner-response/value': '-100'}
        fixture.entities[eid]['task-item/responses'] = [800]
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
        # Two labels can point to the same probe without creating two possible
        # interpretations of the next recorded question.
        fixture = RuntimeFixture('diagnostic')
        fixture.entities[300]['diagnostic-probe/on-incorrect'] = 303
        fixture.answer(100, False, take_retry=True)
        next_answer = fixture.answer(101, True)
        self.assertEqual(next_answer.delivery.next_content, (120,))

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
        self.assertFalse(fixture.state(20).learned)  # -1 + 1 is not positive placement.
        self.assertEqual(fixture.state(20).evidence_mass, 2)
        self.assertEqual(fixture.state(21).repetitions, 1)  # Implied prerequisite evidence.
        self.assertEqual(fixture.state(22).repetitions, 1)
        loaded = fixture.load()
        self.assertNotIn(loaded.topic_eid_to_id[23], loaded.engine.states['learner'])
        self.assertEqual(loaded.engine.global_ability['learner'].practice_mass, 3)
        self.assertEqual(len(fixture.entities[3]['learner-task/items']), 3)

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
        with self.assertRaisesRegex(ValueError, 'already has completion evidence'):
            complete_item(fixture.load(), eid, **args)
        self.assertEqual(fixture.state(20).evidence_mass, 1)

    def test_authored_sequence_and_unready_prerequisite_cannot_be_bypassed(self):
        for prerequisite in (False, True):
            with self.subTest(prerequisite=prerequisite):
                fixture = RuntimeFixture('lesson')
                if prerequisite:
                    fixture.entities[20]['topic/prerequisites'] = [21]
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
        self.assertNotIn('task-item/result', fixture.entities[pending])
        self.assertNotIn('task-item/completed-at', fixture.entities[pending])
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
        self.assertNotIn('task-item/result', fixture.entities[pending])


if __name__ == '__main__':
    unittest.main()
