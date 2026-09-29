"""FIRe's published structure with explicitly replaceable reconstruction policies.

Graph edges go from an advanced topic to an encompassed component skill. They
are NOT prerequisite edges. Time is real elapsed days, independent of earned XP.
See reference/fire-reconstruction.md for equations, assumptions and limitations.
Only the two equations in public_recurrence are a literal published recurrence.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
import hashlib
import json
import math
from typing import Iterable

from .calibration import AccuracyEstimate


def finite(value: float, name: str, low: float | None = None, high: float | None = None) -> None:
    try:
        valid = not isinstance(value, bool) and isinstance(value, (float, int)) and math.isfinite(value)
    except OverflowError:
        valid = False
    if not valid:
        raise ValueError(f'{name} must be finite')
    if low is not None and value < low or high is not None and value > high:
        raise ValueError(f'{name} outside [{low}, {high}]')


def fingerprint(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def public_recurrence(repetitions: float, memory: float, speed: float, decay: float,
                      failed: bool, raw_delta: float, days: float, interval: float) -> tuple[float, float]:
    """Literal published algebra, without inventing undisclosed subfunctions.

The publication does not specify the operational timestamp/update convention.
This function preserves its add-then-decay expression exactly. FireEngine also
offers an explicit decay-before-add interpretation for event-time persistence.
"""
    for name, value in [('repetitions', repetitions), ('memory', memory), ('speed', speed),
                        ('decay', decay), ('days', days), ('interval', interval)]:
        finite(value, name, 0)
    finite(raw_delta, 'raw_delta')
    if interval <= 0 or speed <= 0 or decay < 1 or type(failed) is not bool:
        raise ValueError('positive interval/speed, decay >= 1, and boolean failed required')
    updated = (max(0.0, repetitions + speed * (decay if failed else 1.0) * raw_delta),
               max(0.0, memory + raw_delta) * 2.0 ** (-days / interval))
    for name, value in zip(('updated repetitions', 'updated memory'), updated):
        finite(value, name, 0)
    return updated


@dataclass(frozen=True)
class Edge:
    advanced: str
    component: str
    weight: float

    def __post_init__(self):
        if not all(isinstance(t, str) and t for t in (self.advanced, self.component)) or self.advanced == self.component:
            raise ValueError('distinct, nonempty topic IDs required')
        finite(self.weight, 'weight', 0, 1)


class EncompassingGraph:
    """Weighted DAG with max-product inferred coverage and explicit overrides.

Path multiplication, max aggregation, and override precedence are reconstruction
choices. Max avoids counting one practiced skill repeatedly through a diamond.
An explicit pair, INCLUDING zero, overrides the inferred coverage for that pair.
Failure uses the transpose of exactly the same coverage relation.
"""
    def __init__(self, edges: Iterable[Edge] = (), topics: Iterable[str] = ()):
        topics = tuple(topics)
        if not all(isinstance(t, str) and t for t in topics):
            raise ValueError('graph topic IDs must be nonempty strings')
        self.edges = tuple(sorted(edges, key=lambda e: (e.advanced, e.component)))
        self.topics = frozenset(topics) | frozenset(t for e in self.edges for t in (e.advanced, e.component))
        self._direct = {}
        self._out = {t: [] for t in self.topics}
        indegree = dict.fromkeys(self.topics, 0)
        for e in self.edges:
            pair = (e.advanced, e.component)
            if pair in self._direct:
                raise ValueError(f'duplicate encompassing pair: {pair}')
            self._direct[pair] = e.weight
            self._out[e.advanced].append((e.component, e.weight))
            indegree[e.component] += 1
        ready = sorted(t for t, n in indegree.items() if n == 0)
        order = []
        while ready:
            t = ready.pop(0)
            order.append(t)
            for child, _ in self._out[t]:
                indegree[child] -= 1
                if indegree[child] == 0:
                    ready.append(child)
                    ready.sort()
        if len(order) != len(self.topics):
            raise ValueError('encompassing cycles require resolution before use')
        self._order = tuple(order)
        self._cache: dict[str, dict[str, float]] = {}
        self.id = fingerprint({'topics': sorted(self.topics), 'edges': [asdict(e) for e in self.edges]})

    def coverage(self, advanced: str) -> dict[str, float]:
        if advanced in self._cache:
            return dict(self._cache[advanced])
        weights = {advanced: 1.0}
        for topic in self._order:
            if topic != advanced and (advanced, topic) in self._direct:
                weights[topic] = self._direct[advanced, topic]
            for child, weight in self._out[topic]:
                weights[child] = max(weights.get(child, 0), weights.get(topic, 0) * weight)
        result = {t: w for t, w in weights.items() if w > 0}
        self._cache[advanced] = result
        return dict(result)

    def affected(self, topic: str, passed: bool) -> dict[str, float]:
        if passed:
            return self.coverage(topic)
        return {t: w for t in sorted(self.topics | {topic}) if (w := self.coverage(t).get(topic, 0)) > 0}


@dataclass(frozen=True)
class Policy:
    """All numeric defaults are OUR assumptions, not recovered MA constants.

    ``name`` is a legacy runtime label, not a required database attribute. ``id``
    fingerprints the current configuration; it is not the stable EDB policy ID.
    Replacing a policy does not retroactively recompute stored topic intervals.
    """
    name: str = 'fire-reconstruction-v1'
    base_interval_days: float = 1.0
    interval_growth: float = 2.0
    maximum_interval_days: float = 36500.0
    due_threshold: float = 0.5
    restored_memory: float = 1.0
    discount_power: float = 1.0
    failure_overdue_slope: float = 1.0
    maximum_failure_multiplier: float = 4.0
    prior_accuracy: float = 0.8
    accuracy_alpha: float = 0.2
    speed_exponent: float = 2.0
    minimum_speed: float = 0.25
    maximum_speed: float = 4.0
    gate_slow_implicit: bool = True
    memory_order: str = 'decay-before-add'
    future_horizon_days: float = 7.0

    def __post_init__(self):
        for name, value in asdict(self).items():
            if name not in {'name', 'gate_slow_implicit', 'memory_order'}:
                finite(value, name, 0)
        if not (self.base_interval_days > 0 and self.interval_growth > 1 and
                self.maximum_interval_days >= self.base_interval_days and
                0 < self.due_threshold < self.restored_memory and
                0 < self.prior_accuracy < 1 and 0 < self.accuracy_alpha <= 1 and
                0 < self.minimum_speed <= 1 <= self.maximum_speed and
                self.maximum_failure_multiplier >= 1 and self.discount_power > 0):
            raise ValueError('invalid FIRe policy bounds')
        if not isinstance(self.memory_order, str) or self.memory_order not in {'decay-before-add', 'literal-add-before-decay'}:
            raise ValueError('unknown memory timestamp convention')
        if type(self.gate_slow_implicit) is not bool:
            raise ValueError('gate_slow_implicit must be boolean')

    @property
    def id(self) -> str:
        return fingerprint(asdict(self))

    def interval(self, repetitions: float) -> float:
        finite(repetitions, 'repetitions', 0)
        log_base, log_growth = math.log(self.base_interval_days), math.log(self.interval_growth)
        ceiling = (math.log(self.maximum_interval_days) - log_base) / log_growth
        if repetitions >= ceiling:
            return self.maximum_interval_days
        try:
            interval = self.base_interval_days * self.interval_growth ** repetitions
        except OverflowError:
            # The power can overflow even when multiplying by a small base
            # yields an ordinary, representable half-life.
            interval = math.exp(log_base + repetitions * log_growth)
        return min(self.maximum_interval_days, interval)

    def speed(self, accuracy: float, difficulty_accuracy: float) -> float:
        finite(accuracy, 'accuracy', 0, 1)
        finite(difficulty_accuracy, 'difficulty accuracy', 0, 1)
        if self.speed_exponent == 0:
            return 1.0
        if accuracy == 0:
            return self.minimum_speed
        # Same ratio of powers as before, in log space to avoid overflow or
        # division by zero before applying the configured speed bounds.
        baseline = math.log(self.prior_accuracy)
        log_speed = self.speed_exponent * (math.log(accuracy) - baseline +
                                          math.log(max(difficulty_accuracy, 1e-12)) - baseline)
        if log_speed <= math.log(self.minimum_speed):
            return self.minimum_speed
        if log_speed >= math.log(self.maximum_speed):
            return self.maximum_speed
        return min(self.maximum_speed, max(self.minimum_speed, math.exp(log_speed)))

    def discount(self, memory_now: float) -> float:
        finite(memory_now, 'memory_now', 0)
        # No new spaced credit at restored memory; full credit at/below due.
        return min(1.0, max(0.0, (self.restored_memory - memory_now) /
                            (self.restored_memory - self.due_threshold))) ** self.discount_power

    def failure_multiplier(self, memory_now: float) -> float:
        finite(memory_now, 'memory_now', 0)
        if memory_now >= self.due_threshold or self.failure_overdue_slope == 0:
            return 1.0
        if memory_now == 0:
            return self.maximum_failure_multiplier
        overdue_intervals = math.log2(self.due_threshold) - math.log2(memory_now)
        return min(self.maximum_failure_multiplier, 1 + self.failure_overdue_slope * overdue_intervals)


@dataclass(init=False)
class TopicState:
    repetitions: float = 0.0
    memory: float = 1.0
    memory_at: float = 0.0
    interval_days: float = 1.0
    ability: AccuracyEstimate = field(default_factory=AccuracyEstimate)
    learned: bool = True
    last_direct_at: float | None = None

    def __init__(self, repetitions=0.0, memory=1.0, memory_at=0.0, interval_days=1.0,
                 accuracy=0.8, evidence_mass=0.0, learned=True, last_direct_at=None,
                 ability: AccuracyEstimate | dict | None = None):
        self.repetitions, self.memory, self.memory_at = repetitions, memory, memory_at
        self.interval_days, self.learned, self.last_direct_at = interval_days, learned, last_direct_at
        if ability is None:
            self.ability = AccuracyEstimate(accuracy, accuracy, 0, evidence_mass)
        else:
            self.ability = AccuracyEstimate(**ability) if isinstance(ability, dict) else deepcopy(ability)
        self.__post_init__()

    @property
    def accuracy(self):
        return self.ability.accuracy

    @accuracy.setter
    def accuracy(self, value):
        finite(value, 'accuracy', 0, 1)
        self.ability.assessment_accuracy = self.ability.practice_accuracy = value

    @property
    def evidence_mass(self):
        return self.ability.assessment_mass + self.ability.practice_mass

    def __post_init__(self):
        if not isinstance(self.ability, AccuracyEstimate):
            raise ValueError('ability must be an AccuracyEstimate or its field mapping')
        self.ability.__post_init__()
        for name in ['repetitions', 'memory', 'interval_days', 'evidence_mass']:
            finite(getattr(self, name), name, 0)
        finite(self.memory_at, 'memory_at')
        finite(self.accuracy, 'accuracy', 0, 1)
        if self.interval_days <= 0 or type(self.learned) is not bool:
            raise ValueError('positive interval and boolean learned required')
        if self.last_direct_at is not None:
            finite(self.last_direct_at, 'last_direct_at')

    def memory_now(self, at: float) -> float:
        finite(at, 'at')
        if at < self.memory_at:
            raise ValueError('cannot read a state before its observation time')
        return self.memory * 2.0 ** (-(at - self.memory_at) / self.interval_days)

    def due_at(self, policy: Policy) -> float:
        if self.memory <= policy.due_threshold:
            return self.memory_at
        return self.memory_at + self.interval_days * (math.log2(self.memory) - math.log2(policy.due_threshold))


@dataclass(frozen=True)
class Event:
    """Runtime input for one answer or one graded topic-level unit.

    quality is a positive magnitude, not accuracy or earned XP. Its mapping from
    task answers is deliberately outside FIRe. question_results, when retained,
    are used for ability updates, independently of repetition credit. learned
    marks a successful first lesson or explicitly supplied diagnostic placement.
    This is not a persisted schema entity. Use apply_accuracy for submitted
    answers and apply_retention when the controller closes a graded unit.
    """
    id: str
    learner: str
    topic: str
    at: float
    passed: bool
    quality: float = 1.0
    kind: str = 'review'
    learned: bool = False
    question_results: tuple[bool, ...] = ()
    source: str = 'direct'
    assessment: bool = False

    def __post_init__(self):
        if not all(isinstance(x, str) and x for x in [self.id, self.learner, self.topic, self.kind, self.source]):
            raise ValueError('nonempty string event/learner/topic/kind/source required')
        finite(self.at, 'at')
        finite(self.quality, 'quality', 0)
        if self.quality <= 0 or type(self.passed) is not bool or type(self.learned) is not bool:
            raise ValueError('positive quality and boolean outcomes required')
        if self.learned and not self.passed:
            raise ValueError('failed evidence cannot initialize learned status')
        if type(self.assessment) is not bool:
            raise ValueError('assessment channel must be explicitly boolean')
        try:
            outcomes = tuple(self.question_results)
        except TypeError as error:
            raise ValueError('question outcomes must contain booleans') from error
        if any(type(x) is not bool for x in outcomes):
            raise ValueError('question outcomes must be boolean, not unknown')
        object.__setattr__(self, 'question_results', outcomes)


class FireEngine:
    """Deterministic FIRe transition engine, dry-run compression and JSON snapshots.

    Applying an event is atomic; identical retries do nothing and conflicting
    event IDs fail. Topics without a learned state never silently gain mastery.
    Selection source is recorded but has no effect on the credit rules.
    """
    def __init__(self, graph: EncompassingGraph | None = None, policy: Policy | None = None,
                 difficulty_accuracy: dict[str, float] | None = None,
                 neighborhoods: dict[str, Iterable[str]] | None = None):
        self.graph = graph or EncompassingGraph()
        self.policy = policy or Policy()
        self.difficulty_accuracy = dict(difficulty_accuracy or {})
        for value in self.difficulty_accuracy.values():
            finite(value, 'difficulty accuracy', 0, 1)
        self.states: dict[str, dict[str, TopicState]] = {}
        self.receipts: dict[str, dict] = {}
        self.latest: dict[str, float] = {}
        self.global_ability: dict[str, AccuracyEstimate] = {}
        self.neighborhoods = {topic: tuple(sorted(set(neighbors)))
                              for topic, neighbors in (neighborhoods or {}).items()}

    def _prior(self, learner: str, topic: str, states: dict[str, TopicState]) -> float:
        neighbors = set(self.neighborhoods.get(topic, ())) | set(self.graph.coverage(topic))
        values = [s.accuracy for t, s in states.items() if t != topic and t in neighbors and s.evidence_mass > 0]
        if values:
            return sum(values) / len(values)
        return self.global_ability.get(learner, AccuracyEstimate(self.policy.prior_accuracy,
                                                               self.policy.prior_accuracy)).accuracy

    def seed(self, learner: str, topic: str, state: TopicState) -> None:
        if not all(isinstance(t, str) and t for t in (learner, topic)):
            raise ValueError('learner and topic IDs must be nonempty strings')
        if topic in self.states.get(learner, {}):
            raise ValueError('seed cannot overwrite learner state')
        state.__post_init__()
        self.states.setdefault(learner, {})[topic] = deepcopy(state)
        # A seeded profile is already an observation. Later events cannot use
        # that observation as a prior for an earlier point on the learner clock.
        self.latest[learner] = max(self.latest.get(learner, -math.inf), state.memory_at,
                                   state.last_direct_at if state.last_direct_at is not None else -math.inf)

    def speed(self, topic: str, state: TopicState) -> float:
        return self.policy.speed(state.accuracy, self.difficulty_accuracy.get(topic, self.policy.prior_accuracy))

    def due(self, learner: str, at: float) -> list[str]:
        finite(at, 'at')
        return sorted(t for t, s in self.states.get(learner, {}).items()
                      if s.learned and (s.memory_now(at) <= self.policy.due_threshold or
                                       math.isclose(s.memory_now(at), self.policy.due_threshold,
                                                    rel_tol=1e-12, abs_tol=0)))

    def apply(self, event: Event) -> dict:
        """Legacy combined update, using ability from before this event.

        Kept for historical replays and research inputs. A controller that has
        already submitted answer evidence must close the unit with
        apply_retention instead, so those answers are not counted twice.
        """
        return self._apply(event, 'combined')

    def apply_accuracy(self, event: Event) -> dict:
        """Apply submitted answers immediately, without awarding retention.

        Missing topics get unlearned ability states. Existing retention values
        and their observation timestamps stay unchanged. An empty results tuple
        denotes one answer with outcome ``passed``; it never denotes a skip.
        """
        if event.learned:
            raise ValueError('accuracy evidence cannot establish learned status')
        return self._apply(event, 'accuracy')

    def apply_retention(self, event: Event) -> dict:
        """Apply one graded unit's retention credit without counting answers.

        Speed uses the currently accumulated ability, including any answers
        previously applied by the controller. Unit grading and grouping remain
        outside FIRe. Use a distinct event ID from its constituent answers.
        """
        return self._apply(event, 'retention')

    def _apply(self, event: Event, mode: str) -> dict:
        update_accuracy, update_retention = mode != 'retention', mode != 'accuracy'
        key = json.dumps([event.learner, event.id], separators=(',', ':'))
        # Keep legacy combined-event hashes readable in existing snapshots.
        digest = fingerprint(asdict(event) if mode == 'combined' else {'mode': mode, 'event': asdict(event)})
        if key in self.receipts:
            if self.receipts[key]['event_hash'] != digest or self.receipts[key].get('mode', 'combined') != mode:
                raise ValueError('event ID reused with different evidence or update mode')
            return deepcopy(self.receipts[key])
        if event.at < self.latest.get(event.learner, -math.inf):
            raise ValueError('events must be chronological; rebuild to insert older evidence')
        working = deepcopy(self.states.get(event.learner, {}))
        p = self.policy
        global_before = deepcopy(self.global_ability.get(event.learner, AccuracyEstimate(p.prior_accuracy, p.prior_accuracy)))
        global_before.__post_init__()
        global_after = deepcopy(global_before)
        answers = event.question_results or (event.passed,)
        if update_accuracy:
            global_after.update(answers, assessment=event.assessment, alpha=p.accuracy_alpha)
        initializing = (update_retention and event.learned and
                        (event.topic not in working or not working[event.topic].learned))
        updates = []
        retention_coverage = self.graph.affected(event.topic, event.passed) if update_retention else {}
        accuracy_evidence: dict[str, list[tuple[bool, float]]] = {}
        for correct in answers if update_accuracy else ():
            for target, weight in self.graph.affected(event.topic, correct).items():
                accuracy_evidence.setdefault(target, []).append((correct, weight))
        for topic in sorted(retention_coverage.keys() | accuracy_evidence.keys()):
            coverage = retention_coverage.get(topic, 0.0)
            state = working.get(topic)
            if state is None:
                state = TopicState(memory=0, memory_at=event.at, learned=False,
                                   interval_days=p.base_interval_days,
                                   accuracy=self._prior(event.learner, topic, self.states.get(event.learner, {})))
                working[topic] = state
            state.__post_init__()
            before = asdict(state)
            if event.at < state.memory_at:
                raise ValueError('event predates the topic state')
            created = topic not in self.states.get(event.learner, {})
            if initializing and topic == event.topic:
                state.learned = True
            # Even failed first lessons inform ability. Retention starts only
            # after an explicit learned/placement decision from the caller.
            if not update_retention or not state.learned:
                for correct, weight in accuracy_evidence.get(topic, []):
                    state.ability.update((correct,), assessment=event.assessment, alpha=p.accuracy_alpha, weight=weight)
                if topic == event.topic:
                    state.last_direct_at = event.at
                updates.append({'topic': topic, 'coverage': coverage,
                                'skipped': 'accuracy-only' if not update_retention else 'not-learned',
                                'created': created,
                                'accuracy_evidence': accuracy_evidence.get(topic, []),
                                'before': before, 'after': asdict(state)})
                continue
            direct = topic == event.topic
            now = state.memory_now(event.at)
            speed = self.speed(topic, state)
            gated = coverage > 0 and event.passed and not direct and p.gate_slow_implicit and speed < 1 - 1e-12
            discount = 1.0 if initializing and direct else p.discount(now)
            raw = (-1 if not event.passed else 1) * event.quality * coverage * discount
            if gated:
                raw = 0.0
            decay = p.failure_multiplier(now) if not event.passed else 1.0
            if initializing and direct:
                # The public speed diagram labels the initial lesson as one
                # speed-adjusted repetition. Memory normalization is our policy.
                repetitions, memory = speed * event.quality, p.restored_memory
            else:
                repetitions = max(0.0, state.repetitions + speed * decay * raw)
                if p.memory_order == 'literal-add-before-decay':
                    _, memory = public_recurrence(state.repetitions, state.memory, speed, decay,
                                                  not event.passed, raw, event.at-state.memory_at,
                                                  state.interval_days)
                else:
                    memory = max(0.0, now + raw)
            # Accuracy evidence is separate from retention credit and recency discount.
            for correct, evidence_weight in accuracy_evidence.get(topic, []):
                state.ability.update((correct,), assessment=event.assessment, alpha=p.accuracy_alpha, weight=evidence_weight)
            finite(repetitions, 'updated repetitions', 0)
            finite(memory, 'updated memory', 0)
            state.repetitions = repetitions
            state.memory = memory
            state.memory_at = event.at
            if raw != 0 or initializing and direct:
                state.interval_days = p.interval(repetitions)
            if direct:
                state.last_direct_at = event.at
            updates.append({'topic': topic, 'direct': direct, 'coverage': coverage,
                            'created': created,
                            'memory_before_decay': before['memory'], 'memory_now': now,
                            'discount': discount, 'raw_delta': raw, 'speed': speed,
                            'accuracy_evidence': accuracy_evidence.get(topic, []),
                            'failure_multiplier': decay, 'implicit_gated': gated,
                            'before': before, 'after': asdict(state), 'due_at': state.due_at(p)})
        receipt = {'event': asdict(event), 'event_hash': digest, 'mode': mode, 'policy_id': p.id,
                   'graph_id': self.graph.id, 'updates': updates,
                   'global_ability_before': asdict(global_before), 'global_ability_after': asdict(global_after),
                   'difficulty_id': fingerprint(self.difficulty_accuracy), 'neighborhood_id': fingerprint(self.neighborhoods)}
        # Receipts have one JSON-compatible representation both before and after
        # persistence, so a retried event returns the same logical and Python value.
        receipt = json.loads(json.dumps(receipt, allow_nan=False))
        self.states[event.learner] = working
        if update_accuracy:
            self.global_ability[event.learner] = global_after
        self.latest[event.learner] = event.at
        self.receipts[key] = receipt
        return deepcopy(receipt)

    def rank(self, learner: str, at: float, candidates: list[dict]) -> list[dict]:
        """Greedy review compression by simulated due removals per expected minute.

        Input candidates must already satisfy curriculum/readiness eligibility.
        Successful-outcome simulation is an optimistic estimate, not a prediction
        that the student will pass. Useful coverage of upcoming reviews breaks ties.
        """
        due = set(self.due(learner, at))
        ranked = []
        for candidate in candidates:
            topic = candidate['topic']
            minutes = candidate['expected_minutes']
            finite(minutes, 'expected_minutes', 0)
            if minutes <= 0:
                raise ValueError('candidate expected time must be positive')
            trial = deepcopy(self)
            preview_id = 'preview:' + topic
            suffix = 0
            while json.dumps([learner, preview_id], separators=(',', ':')) in trial.receipts:
                suffix += 1
                preview_id = f'preview:{topic}:{suffix}'
            event = Event(preview_id, learner, topic, at, True,
                          learned=candidate.get('kind') == 'lesson', kind=candidate.get('kind', 'review'))
            trial.apply_retention(event)
            removed = sorted(due - set(trial.due(learner, at)))
            future_gain = 0.0
            for t, before in self.states.get(learner, {}).items():
                if not before.learned:
                    continue
                after = trial.states[learner][t]
                b = max(0, min(self.policy.future_horizon_days, before.due_at(self.policy) - at))
                a = max(0, min(self.policy.future_horizon_days, after.due_at(self.policy) - at))
                future_gain += max(0, a-b)
            ranked.append({**candidate, 'due_removed': removed, 'due_removed_per_minute': len(removed)/minutes,
                           'future_days_gained_per_minute': future_gain/minutes})
        return sorted(ranked, key=lambda c: (-c['due_removed_per_minute'], -c['future_days_gained_per_minute'], c['topic']))

    def snapshot(self) -> dict:
        return {'format': 1, 'policy': asdict(self.policy), 'graph': [asdict(e) for e in self.graph.edges],
                'topics': sorted(self.graph.topics), 'difficulty_accuracy': dict(self.difficulty_accuracy),
                'states': {learner: {topic: asdict(state) for topic, state in sorted(states.items())}
                           for learner, states in sorted(self.states.items())},
                'receipts': deepcopy(self.receipts), 'latest': dict(self.latest),
                'global_ability': {learner: asdict(value) for learner, value in self.global_ability.items()},
                'neighborhoods': dict(self.neighborhoods)}

    @classmethod
    def restore(cls, data: dict) -> FireEngine:
        if data['format'] != 1:
            raise ValueError('unsupported snapshot format')
        result = cls(EncompassingGraph((Edge(**e) for e in data['graph']), data['topics']),
                     Policy(**data['policy']), data['difficulty_accuracy'], data.get('neighborhoods'))
        for learner, states in data['states'].items():
            for topic, state in states.items():
                result.seed(learner, topic, TopicState(**state))
        result.receipts = deepcopy(data['receipts'])
        for learner, at in data['latest'].items():
            if not isinstance(learner, str) or not learner:
                raise ValueError('learner IDs must be nonempty strings')
            finite(at, 'latest observation time')
            result.latest[learner] = max(at, result.latest.get(learner, -math.inf))
        result.global_ability = {learner: AccuracyEstimate(**value) for learner, value in data.get('global_ability', {}).items()}
        return result
