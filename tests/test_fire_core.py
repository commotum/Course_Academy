"""Published examples and counterexamples for the FIRe reconstruction.

These verify operational behavior and disclosed algebra, NOT agreement with
unobserved MA schedules. Unknown numeric policies are tested as explicit choices.
"""
from dataclasses import replace
import json
import math
import unittest

from engine.fire import Edge, EncompassingGraph, Event, FireEngine, Policy, TopicState, public_recurrence


class FireTests(unittest.TestCase):
    def make_engine(self, edges=(), topics=('A', 'B', 'C'), **policy):
        engine = FireEngine(EncompassingGraph(edges), Policy(**policy))
        for topic in topics:
            engine.seed('learner', topic, TopicState())
        return engine

    def event(self, topic='A', at=1, passed=True, **kwargs):
        return Event(kwargs.pop('id', 'e1'), 'learner', topic, at, passed, **kwargs)

    def test_literal_published_recurrence(self):
        self.assertEqual(public_recurrence(3, 1, 2, 1, False, 0.5, 2, 2), (4, 0.75))
        self.assertEqual(public_recurrence(1, 0.2, 2, 3, True, -0.5, 2, 2), (0, 0))

    def test_multiplication_example_positive_down_negative_up(self):
        edges = (Edge('advanced', 'addition', 1), Edge('advanced', 'multiplication', 1))
        engine = self.make_engine(edges, ('advanced', 'addition', 'multiplication'))
        receipt = engine.apply(self.event('advanced'))
        self.assertEqual({u['topic'] for u in receipt['updates']}, set(engine.states['learner']))
        self.assertTrue(all(u['raw_delta'] == 1 for u in receipt['updates']))
        engine = self.make_engine(edges, ('advanced', 'addition', 'multiplication'))
        receipt = engine.apply(self.event('addition', passed=False))
        self.assertEqual({u['topic'] for u in receipt['updates']}, {'addition', 'advanced'})
        self.assertTrue(all(u['raw_delta'] == -1 for u in receipt['updates']))

    def test_fractional_path_and_diamond_not_double_counted(self):
        graph = EncompassingGraph([Edge('A', 'B', .5), Edge('A', 'C', .8),
                                   Edge('B', 'D', .5), Edge('C', 'D', .5)])
        self.assertEqual(graph.coverage('A')['D'], .4)
        self.assertEqual(graph.affected('D', False)['A'], .4)

    def test_explicit_lower_weight_and_zero_override(self):
        for override in [0, .1]:
            graph = EncompassingGraph([Edge('A', 'B', 1), Edge('B', 'C', 1), Edge('A', 'C', override)])
            self.assertEqual(graph.coverage('A').get('C', 0), override)
            self.assertEqual(graph.affected('C', False).get('A', 0), override)

    def test_cycles_duplicates_and_invalid_weights_rejected(self):
        for edges in [[Edge('A', 'B', 1), Edge('B', 'A', 1)], [Edge('A', 'B', 1)] * 2]:
            with self.assertRaises(ValueError): EncompassingGraph(edges)
        for weight in [-1, 1.01, float('nan'), float('inf')]:
            with self.assertRaises(ValueError): Edge('A', 'B', weight)
        with self.assertRaises(ValueError): Edge(1, 'B', 1)
        with self.assertRaises(ValueError): EncompassingGraph(topics=(1,))

    def test_speed_below_one_blocks_only_incoming_positive_credit(self):
        engine = self.make_engine([Edge('A', 'B', 1)])
        engine.states['learner']['B'].accuracy = .4
        receipt = engine.apply(self.event())
        b = next(u for u in receipt['updates'] if u['topic'] == 'B')
        self.assertTrue(b['implicit_gated'])
        self.assertEqual(b['raw_delta'], 0)
        self.assertEqual(b['after']['repetitions'], 0)
        engine.apply(self.event('B', at=2, id='explicit'))
        self.assertGreater(engine.states['learner']['B'].repetitions, 0)

    def test_slow_target_does_not_block_transit_to_other_topics(self):
        engine = self.make_engine([Edge('A', 'B', 1), Edge('B', 'C', 1)])
        engine.states['learner']['B'].accuracy = .4
        engine.apply(self.event())
        self.assertEqual(engine.states['learner']['B'].repetitions, 0)
        self.assertEqual(engine.states['learner']['C'].repetitions, 1)

    def test_early_credit_discount_is_destination_local(self):
        engine = self.make_engine([Edge('A', 'B', 1)])
        engine.states['learner']['A'].memory_at = 1
        receipt = engine.apply(self.event())
        delta = {u['topic']: u['raw_delta'] for u in receipt['updates']}
        self.assertEqual(delta, {'A': 0, 'B': 1})

    def test_partial_encompassing_postpones_due_review(self):
        engine = self.make_engine([Edge('A', 'B', .25)])
        before = engine.states['learner']['B'].due_at(engine.policy)
        engine.apply(self.event())
        state = engine.states['learner']['B']
        self.assertEqual(state.repetitions, .25)
        self.assertGreater(state.due_at(engine.policy), before)

    def test_severe_overdue_failure_penalizes_more(self):
        timely = self.make_engine(topics=('A',))
        overdue = self.make_engine(topics=('A',))
        for engine in [timely, overdue]: engine.states['learner']['A'].repetitions = 5
        a = timely.apply(self.event(passed=False))['updates'][0]
        b = overdue.apply(self.event(at=10, passed=False))['updates'][0]
        self.assertGreater(b['failure_multiplier'], a['failure_multiplier'])
        self.assertLess(b['after']['repetitions'], a['after']['repetitions'])
        self.assertGreaterEqual(b['after']['memory'], 0)

    def test_initial_lesson_accrues_speed_and_no_unlearned_implicit_mastery(self):
        engine = FireEngine(EncompassingGraph([Edge('A', 'B', 1)]))
        receipt = engine.apply(self.event(at=0, learned=True, kind='lesson'))
        self.assertEqual(engine.states['learner']['A'].repetitions, 1)
        self.assertEqual(engine.states['learner']['A'].memory, 1)
        self.assertFalse(engine.states['learner']['B'].learned)
        self.assertEqual(engine.states['learner']['B'].repetitions, 0)
        self.assertEqual(receipt['updates'][1]['skipped'], 'not-learned')

    def test_quality_may_exceed_one_as_in_author_podcast(self):
        engine = self.make_engine()
        engine.apply(self.event(quality=1.5))
        self.assertEqual(engine.states['learner']['A'].repetitions, 1.5)

    def test_failed_first_lesson_retains_ability_without_awarding_mastery(self):
        engine = FireEngine()
        engine.apply(self.event(at=0, passed=False, kind='lesson', question_results=(False, False)))
        state = engine.states['learner']['A']
        self.assertFalse(state.learned)
        self.assertLess(state.accuracy, .8)
        previous_mass = state.evidence_mass
        prior_speed = engine.speed('A', state)
        receipt = engine.apply(self.event(at=1, id='learn', learned=True, kind='lesson', question_results=(True,)))
        state = engine.states['learner']['A']
        self.assertTrue(state.learned)
        self.assertEqual(state.evidence_mass, previous_mass + 1)
        self.assertAlmostEqual(state.repetitions, prior_speed)
        self.assertFalse(receipt['updates'][0]['before']['learned'])
        self.assertTrue(receipt['updates'][0]['after']['learned'])
        self.assertFalse(receipt['updates'][0]['created'])

    def test_assessment_and_practice_channels_global_and_local(self):
        engine = self.make_engine([Edge('A', 'B', 1)])
        engine.apply(self.event(question_results=(True, True, True)))
        state = engine.states['learner']['A']
        practice = state.ability.practice_accuracy
        self.assertEqual(state.ability.assessment_accuracy, .8)
        engine.apply(self.event(at=2, id='quiz', passed=False, assessment=True,
                                kind='assessment', question_results=(False,)))
        self.assertEqual(state.ability.practice_accuracy, practice)  # prior snapshot object
        state = engine.states['learner']['A']
        self.assertEqual(state.ability.practice_accuracy, practice)
        self.assertAlmostEqual(state.ability.assessment_accuracy, .64)
        self.assertAlmostEqual(state.accuracy, (practice + .64) / 2)
        self.assertEqual(engine.global_ability['learner'].practice_mass, 3)
        self.assertEqual(engine.global_ability['learner'].assessment_mass, 1)

    def test_published_two_times_speed_scales_credit(self):
        engine = self.make_engine(speed_exponent=2)
        # Equal .8 ability / prior; difficulty accuracy chosen to yield speed 2.
        engine.states['learner']['A'].accuracy = 1
        engine.difficulty_accuracy['A'] = .64 * math.sqrt(2)
        engine.apply(self.event())
        self.assertAlmostEqual(engine.states['learner']['A'].repetitions, 2)

    def test_mixed_answer_accuracy_flows_independently_of_task_pass(self):
        engine = self.make_engine([Edge('A', 'B', 1), Edge('C', 'A', 1)])
        receipt = engine.apply(self.event(question_results=(True, False, True)))
        states = engine.states['learner']
        self.assertGreater(states['B'].accuracy, .8)
        self.assertLess(states['C'].accuracy, .8)
        self.assertEqual(states['C'].repetitions, 0)
        c = next(u for u in receipt['updates'] if u['topic'] == 'C')
        self.assertEqual(c['raw_delta'], 0)

    def test_question_order_is_preserved_in_recency_weighting(self):
        first = self.make_engine()
        last = self.make_engine()
        first.apply(self.event(question_results=(False, True)))
        last.apply(self.event(question_results=(True, False)))
        self.assertGreater(first.states['learner']['A'].accuracy, last.states['learner']['A'].accuracy)

    def test_memory_order_is_an_explicit_observable_difference(self):
        standard = self.make_engine()
        literal = self.make_engine(memory_order='literal-add-before-decay')
        standard.apply(self.event())
        literal.apply(self.event())
        self.assertEqual(standard.states['learner']['A'].memory, 1.5)
        self.assertEqual(literal.states['learner']['A'].memory, 1)

    def test_duplicate_retries_and_conflict(self):
        engine = self.make_engine()
        event = self.event()
        receipt = engine.apply(event)
        snapshot = deepcopy_json(engine.snapshot())
        self.assertEqual(engine.apply(event), receipt)
        self.assertEqual(deepcopy_json(engine.snapshot()), snapshot)
        with self.assertRaises(ValueError): engine.apply(replace(event, passed=False))

    def test_out_of_order_and_atomic_failure(self):
        engine = self.make_engine([Edge('A', 'B', 1)])
        engine.states['learner']['B'].memory_at = 3
        before = deepcopy_json(engine.snapshot())
        with self.assertRaises(ValueError): engine.apply(self.event())
        self.assertEqual(deepcopy_json(engine.snapshot()), before)
        engine.apply(self.event(at=3))
        with self.assertRaises(ValueError): engine.apply(self.event(at=2, id='older'))

    def test_snapshot_round_trip_and_retry(self):
        engine = self.make_engine([Edge('A', 'B', .5)])
        event = self.event()
        original_receipt = engine.apply(event)
        restored = FireEngine.restore(deepcopy_json(engine.snapshot()))
        self.assertEqual(restored.apply(event), original_receipt)
        next_event = self.event(at=4, id='next')
        self.assertEqual(restored.apply(next_event), engine.apply(next_event))

    def test_snapshot_configuration_is_detached_from_live_engine(self):
        engine = FireEngine(difficulty_accuracy={'A': .8}, neighborhoods={'A': ('B',)})
        snapshot = engine.snapshot()
        snapshot['difficulty_accuracy']['A'] = .1
        snapshot['neighborhoods']['A'] = ('C',)
        self.assertEqual(engine.difficulty_accuracy, {'A': .8})
        self.assertEqual(engine.neighborhoods, {'A': ('B',)})

    def test_json_replay_preserves_neighborhood_and_isolated_topics(self):
        from engine.fire.__main__ import replay
        data = {
            'topics': ['A', 'B', 'isolated'], 'neighborhoods': {'A': ['B']},
            'initial_states': [{'learner': 'learner', 'topic': 'B',
                                'state': {'accuracy': .4, 'evidence_mass': 1}}],
            'events': [{'id': 'learn', 'learner': 'learner', 'topic': 'A',
                        'at': 1, 'passed': True, 'kind': 'lesson', 'learned': True}],
        }
        direct = FireEngine(EncompassingGraph(topics=data['topics']), neighborhoods=data['neighborhoods'])
        direct.seed('learner', 'B', TopicState(accuracy=.4, evidence_mass=1))
        expected = direct.apply(Event(**data['events'][0]))
        actual = replay(data)
        self.assertEqual(actual['receipts'][0], expected)
        self.assertEqual(deepcopy_json(actual['snapshot']), deepcopy_json(direct.snapshot()))

    def test_seed_observation_blocks_earlier_unrelated_events(self):
        engine = FireEngine(neighborhoods={'A': ('B',)})
        engine.seed('learner', 'B', TopicState(memory_at=5, accuracy=.3, evidence_mass=4))
        before = engine.snapshot()
        with self.assertRaises(ValueError):
            engine.apply(self.event(at=1, learned=True))
        self.assertEqual(engine.snapshot(), before)

    def test_student_selected_and_recommended_have_same_transition(self):
        engine = self.make_engine([Edge('A', 'B', 1)])
        other = FireEngine.restore(deepcopy_json(engine.snapshot()))
        engine.apply(self.event(source='student-selected'))
        other.apply(self.event(source='recommended'))
        self.assertEqual(engine.states, other.states)

    def test_compression_uses_actual_due_removals_and_falls_back_to_review(self):
        engine = self.make_engine([Edge('A', 'B', 1), Edge('A', 'C', 1)])
        before = deepcopy_json(engine.snapshot())
        ranked = engine.rank('learner', 1, [{'topic': 'A', 'expected_minutes': 5},
                                          {'topic': 'B', 'expected_minutes': 3}])
        self.assertEqual(ranked[0]['topic'], 'A')
        self.assertEqual(ranked[0]['due_removed'], ['A', 'B', 'C'])
        self.assertEqual(deepcopy_json(engine.snapshot()), before)
        self.assertEqual(engine.rank('learner', 1, [{'topic': 'B', 'expected_minutes': 3}])[0]['due_removed'], ['B'])

    def test_rank_preview_cannot_collide_with_real_event_ids(self):
        engine = self.make_engine(topics=('A',))
        engine.apply(self.event(id='preview:A'))
        engine.apply(self.event(at=2, id='preview:A:1'))
        snapshot = engine.snapshot()
        self.assertEqual(engine.rank('learner', 10, [{'topic': 'A', 'expected_minutes': 1}])[0]['topic'], 'A')
        self.assertEqual(engine.snapshot(), snapshot)

    def test_invalid_policy_and_event_inputs(self):
        for args in [{'base_interval_days': 0}, {'interval_growth': 1}, {'accuracy_alpha': 2},
                     {'due_threshold': 1}, {'minimum_speed': 2}, {'memory_order': 'hidden'}]:
            with self.assertRaises(ValueError): Policy(**args)
        for args in [{'quality': 0}, {'quality': float('nan')}, {'passed': 'true'},
                     {'learned': True, 'passed': False}, {'question_results': (None,)}]:
            with self.assertRaises(ValueError): self.event(**args)


def deepcopy_json(value):
    return json.loads(json.dumps(value, sort_keys=True, allow_nan=False))


if __name__ == '__main__':
    unittest.main()
