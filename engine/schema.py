"""Read current EDB entities and prepare guarded, atomic item-completion writes.

This module does not connect to a database. A writer submits ``plan.edn`` using
``TransactionRequest::from_edn(plan.request_key, ...).comparing_basis(plan.compare_basis_t)``
and the registered EDB progress/configuration predicates. Retain the entire plan
for exact retries; do not recompute it after an uncertain submission result.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
from types import MappingProxyType
from uuid import UUID

from .fire.calibration import AccuracyEstimate
from .fire.core import Edge, EncompassingGraph, FireEngine, Policy, TopicState


class Keyword(str):
    """An EDN keyword, distinct from an ordinary string or string tempid."""
    def __new__(cls, value: str):
        if not isinstance(value, str):
            raise ValueError('EDN keyword must be text')
        value = value.removeprefix(':')
        if not value or any(c.isspace() or c in '[]{}()";,' for c in value):
            raise ValueError('invalid EDN keyword')
        return super().__new__(cls, value)


def instant(value: datetime | str | int) -> datetime:
    """Canonical UTC instant at EDB's millisecond resolution (truncate sub-ms)."""
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace('Z', '+00:00'))
    elif type(value) is int:
        value = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(milliseconds=value)
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError('an instant needs an explicit timezone or integer epoch milliseconds')
    value = value.astimezone(timezone.utc)
    return value.replace(microsecond=value.microsecond // 1000 * 1000)


def instant_days(value: datetime | str | int) -> float:
    return (instant(value) - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds() / 86400


def _day_instant(value: float) -> datetime:
    _number(value, 'engine timestamp')
    return datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(milliseconds=round(value * 86400000))


def _number(value, label: str, low=None, high=None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{label} must be finite numeric data')
    if low is not None and value < low or high is not None and value > high:
        raise ValueError(f'{label} outside its allowed range')
    return float(value)


def _freeze(value):
    if isinstance(value, Mapping):
        return MappingProxyType({str(k).removeprefix(':'): _freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple, set, frozenset)):
        return tuple(_freeze(v) for v in value)
    return deepcopy(value)


class EntitySnapshot:
    """A captured EDB basis and entity records keyed by numeric EID.

    Attribute names are strings, with an optional leading colon. References are
    EIDs; enum refs can also be idents present in the capture. UUID values can be
    UUID objects or UUID strings; instants accept aware datetime, ISO text, or
    integer epoch milliseconds. Missing facts stay absent.
    """
    def __init__(self, entities: Mapping[int, Mapping], basis_t: int, status_history=()):
        if type(basis_t) is not int or basis_t < 0:
            raise ValueError('basis_t must be a nonnegative integer')
        records = {}
        for eid, record in entities.items():
            if type(eid) is not int or eid < 0 or not isinstance(record, Mapping):
                raise ValueError('entities must map numeric EIDs to attribute maps')
            names = [str(k).removeprefix(':') for k in record]
            if len(set(names)) != len(names):
                raise ValueError('duplicate normalized attribute name')
            records[eid] = _freeze(record)
        self.entities = MappingProxyType(records)
        self._canonical_examples = frozenset(record['knowledge-point/canonical-example']
            for record in records.values() if 'knowledge-point/canonical-example' in record)
        self.basis_t = basis_t
        self._idents = {}
        for eid, record in self.entities.items():
            if 'db/ident' in record:
                ident = str(Keyword(record['db/ident']))
                if ident in self._idents:
                    raise ValueError(f'duplicate ident {ident}')
                self._idents[ident] = eid
        history, seen, tx_times = [], set(), {}
        for raw in status_history:
            if not isinstance(raw, Mapping) or set(raw) != {'entity', 'attribute', 'value', 't', 'at'}:
                raise ValueError('status history needs entity, attribute, value, t, and at')
            eid = self.eid(raw['entity'])
            attr = str(raw['attribute']).removeprefix(':')
            choices = {'learner-task/status': {'locked', 'unlocked', 'started', 'paused', 'completed', 'failed'},
                       'task-item/status': {'started', 'paused', 'completed', 'skipped', 'correct', 'incorrect'}}
            if attr not in choices or attr.split('/')[0] not in self.types(eid):
                raise ValueError('status history attribute must match its entity')
            value = self.eid(raw['value'])
            if self.ident(value) not in {attr.replace('/', '.') + '/' + name for name in choices[attr]}:
                raise ValueError('invalid status history value')
            t = raw['t']
            if type(t) is not int or not 0 <= t <= basis_t or (eid, attr, t) in seen:
                raise ValueError('status history needs unique assertions within the captured basis')
            at = instant(raw['at'])
            if t in tx_times and tx_times[t] != at:
                raise ValueError('one transaction must have one timestamp')
            seen.add((eid, attr, t)); tx_times[t] = at
            history.append({'entity': eid, 'attribute': attr, 'value': value, 't': t, 'at': at})
        times = [at for _, at in sorted(tx_times.items())]
        if times != sorted(times):
            raise ValueError('status history timestamps must follow transaction order')
        history.sort(key=lambda row: (row['t'], row['entity'], row['attribute']))
        self.status_history = _freeze(history)
        for eid, attr, _ in seen:
            events = self.status_events(eid, attr)
            if self.ref(eid, attr) != events[-1]['value']:
                raise ValueError('current status must match its latest history assertion')

    def eid(self, reference: int | str) -> int:
        if isinstance(reference, str):
            reference = self._idents.get(str(Keyword(reference)))
        if type(reference) is not int or reference not in self.entities:
            raise ValueError(f'unresolved entity reference {reference!r}')
        return reference

    def entity(self, reference: int | str) -> Mapping:
        return self.entities[self.eid(reference)]

    def ident(self, reference: int | str) -> str:
        value = self.entity(reference).get('db/ident')
        if not isinstance(value, str):
            raise ValueError(f'entity {reference!r} is not an enum ident')
        return str(Keyword(value))

    def ref(self, eid: int, attribute: str, *, required: bool = True) -> int | None:
        value = self.entity(eid).get(attribute.removeprefix(':'))
        if value is None and not required:
            return None
        return self.eid(value)

    def refs(self, eid: int, attribute: str) -> tuple[int, ...]:
        values = self.entity(eid).get(attribute.removeprefix(':'), ())
        if not isinstance(values, tuple):
            raise ValueError(f'{attribute} must be a collection of references')
        return tuple(sorted({self.eid(value) for value in values}))

    def owners(self, target: int, attribute: str) -> tuple[int, ...]:
        target = self.eid(target)
        result = []
        for eid, record in self.entities.items():
            if attribute not in record:
                continue
            value = record[attribute]
            refs = self.refs(eid, attribute) if isinstance(value, tuple) else (self.ref(eid, attribute),)
            if target in refs:
                result.append(eid)
        return tuple(sorted(result))

    def types(self, eid: int) -> frozenset[str]:
        return frozenset(name[:-3] for name in self.entity(eid) if name.endswith('/id') and name != 'db/id')

    def is_example(self, question: int) -> bool:
        """Requires all canonical-example references in this captured projection."""
        return question in self._canonical_examples

    def knowledge_points_for_question(self, question: int) -> tuple[int, ...]:
        if 'question' not in self.types(question):
            raise ValueError('content is not a question')
        if self.is_example(question):
            raise ValueError('canonical examples cannot belong to practice banks')
        owners = self.owners(question, 'knowledge-point/questions')
        if len(owners) != 1 or 'knowledge-point' not in self.types(owners[0]):
            raise ValueError('question needs exactly one knowledge-point bank')
        return owners

    def topic_for_question(self, question: int) -> int:
        topics = set()
        for kp in self.knowledge_points_for_question(question):
            parents = self.owners(kp, 'topic/knowledge-points')
            if not parents or any('topic' not in self.types(t) for t in parents):
                raise ValueError('knowledge point needs a topic')
            topics.update(parents)
        if len(topics) != 1:
            raise ValueError('question must resolve to exactly one topic')
        return next(iter(topics))

    def item_task(self, item_eid: int, learner_eid: int) -> int:
        if 'task-item' not in self.types(item_eid):
            raise ValueError('completion target is not a task item')
        owners = self.owners(item_eid, 'learner-task/items')
        if len(owners) != 1 or 'learner-task' not in self.types(owners[0]):
            raise ValueError('task item must have exactly one task owner')
        task = owners[0]
        if self.owners(task, 'learner/activity') != (self.eid(learner_eid),):
            raise ValueError('task must belong exclusively to this learner')
        return task

    def status_events(self, eid, attr):
        return tuple(event for event in self.status_history
                     if event['entity'] == eid and event['attribute'] == attr)

    def first_started(self, task):
        events = self.status_events(task, 'learner-task/status')
        starts = [e['at'] for e in events if self.ident(e['value']) == 'learner-task.status/started']
        if not starts:
            raise ValueError('task timing requires its started status history')
        return starts[0]

    def item_completed_at(self, item):
        events = self.status_events(item, 'task-item/status')
        if events and self.ident(events[-1]['value']) in {
                'task-item.status/' + name for name in ('completed', 'skipped', 'correct', 'incorrect')}:
            return events[-1]['at']
        return None

    def item_elapsed(self, item, at):
        at = instant(at)
        events = self.status_events(item, 'task-item/status')
        if not events:
            raise ValueError('item timing requires its status history')
        previous, active, total = None, None, 0.0
        for event in events:
            status = self.ident(event['value']).split('/')[-1]
            if event['at'] > at:
                raise ValueError('operation predates status history')
            if (previous is None and status != 'started'
                    or previous == 'started' and status not in {'paused', 'completed', 'skipped', 'correct', 'incorrect'}
                    or previous == 'paused' and status != 'started'
                    or previous in {'completed', 'skipped', 'correct', 'incorrect'}):
                raise ValueError('invalid item status history transition')
            if active is not None:
                total += (event['at'] - active).total_seconds()
                active = None
            if status == 'started':
                active = event['at']
            previous = status
        if active is not None:
            total += (at - active).total_seconds()
        return total

    def task_elapsed(self, task, at):
        self.first_started(task)
        return sum(self.item_elapsed(item, at) for item in self.refs(task, 'learner-task/items'))

    def active_items(self, learner):
        return tuple(item for task in self.refs(learner, 'learner/activity')
                     for item in self.refs(task, 'learner-task/items')
                     if self.ident(self.ref(item, 'task-item/status')) == 'task-item.status/started')


POLICY_FIELDS = {
    'base-half-life-days': 'base_interval_days', 'interval-growth': 'interval_growth',
    'maximum-half-life-days': 'maximum_interval_days', 'review-threshold': 'due_threshold',
    'initial-retention': 'restored_memory', 'early-practice-discount-power': 'discount_power',
    'initial-accuracy': 'prior_accuracy', 'accuracy-update-rate': 'accuracy_alpha',
    'speed-exponent': 'speed_exponent', 'minimum-speed': 'minimum_speed',
    'maximum-speed': 'maximum_speed', 'overdue-failure-slope': 'failure_overdue_slope',
    'maximum-failure-multiplier': 'maximum_failure_multiplier',
    'gate-slow-implicit': 'gate_slow_implicit', 'retention-update-order': 'memory_order',
    'future-horizon-days': 'future_horizon_days',
}
STATE_FIELDS = {
    'repetitions': 'repetitions', 'memory': 'memory', 'interval-days': 'interval_days',
    'learned': 'learned',
}
ABILITY_FIELDS = ('assessment_accuracy', 'practice_accuracy', 'assessment_mass', 'practice_mass')


def _uuid(record: Mapping, attribute: str) -> str:
    try:
        return str(UUID(str(record[attribute])))
    except (KeyError, ValueError, TypeError, AttributeError) as error:
        raise ValueError(f'{attribute} requires a UUID') from error


def _ability(record: Mapping, prefix: str) -> AccuracyEstimate:
    try:
        return AccuracyEstimate(**{field: record[f'{prefix}/{field.replace("_", "-")}'] for field in ABILITY_FIELDS})
    except KeyError as error:
        raise ValueError(f'incomplete {prefix} accuracy state') from error


@dataclass
class LoadedRuntime:
    snapshot: EntitySnapshot
    engine: FireEngine
    learner_eid: int
    learner: str
    policy_eid: int
    topic_eid_to_id: dict[int, str]
    topic_id_to_eid: dict[str, int]
    progress_by_topic: dict[str, int]
    performance_eid: int | None


def load_runtime(snapshot: EntitySnapshot, learner_eid: int, policy_eid: int) -> LoadedRuntime:
    learner_eid, policy_eid = snapshot.eid(learner_eid), snapshot.eid(policy_eid)
    learner = snapshot.entity(learner_eid).get('learner/id')
    if not isinstance(learner, str) or not learner:
        raise ValueError('learner/id must be a nonempty string')
    record = snapshot.entity(policy_eid)
    _uuid(record, 'policy/id')
    try:
        settings = {field: record['policy/' + attribute] for attribute, field in POLICY_FIELDS.items()}
    except KeyError as error:
        raise ValueError(f'incomplete persisted policy: {error.args[0]}') from error
    order = snapshot.ident(settings['memory_order'])
    orders = {'policy.retention-update/decay-before-add': 'decay-before-add',
              'policy.retention-update/add-before-decay': 'literal-add-before-decay'}
    if order not in orders:
        raise ValueError('unsupported retention update order')
    settings['memory_order'] = orders[order]
    policy = Policy(**settings)
    topic_eid_to_id = {eid: _uuid(entity, 'topic/id') for eid, entity in snapshot.entities.items() if 'topic/id' in entity}
    topic_id_to_eid = {identity: eid for eid, identity in topic_eid_to_id.items()}
    if len(topic_id_to_eid) != len(topic_eid_to_id):
        raise ValueError('duplicate topic UUID')
    edges, difficulty = [], {}
    for eid, identity in topic_eid_to_id.items():
        topic = snapshot.entity(eid)
        if 'topic/difficulty' in topic:
            difficulty[identity] = _number(topic['topic/difficulty'], 'topic difficulty', 0, 1)
        for edge in snapshot.refs(eid, 'topic/encompasses'):
            if snapshot.owners(edge, 'topic/encompasses') != (eid,):
                raise ValueError('encompassing record must have one source topic')
            target = snapshot.ref(edge, 'encompassing/topic')
            if target not in topic_eid_to_id:
                raise ValueError('encompassing target must be a topic')
            weight = _number(snapshot.entity(edge).get('encompassing/weight'), 'coverage', 0, 1)
            edges.append(Edge(identity, topic_eid_to_id[target], weight))
    # These are priors from curriculum neighbors, not inferred encompassing edges.
    neighborhoods = {}
    for eid, identity in topic_eid_to_id.items():
        if any(target not in topic_eid_to_id for target in snapshot.refs(eid, 'topic/next')):
            raise ValueError('curriculum neighbors must reference known topics')
        neighbors = set(snapshot.owners(eid, 'topic/next'))
        for kp in snapshot.refs(eid, 'topic/knowledge-points'):
            if 'knowledge-point' not in snapshot.types(kp):
                raise ValueError('topic knowledge-points must reference knowledge points')
            neighbors.update(snapshot.refs(kp, 'knowledge-point/key-prerequisites'))
        for module in snapshot.owners(eid, 'module/topics'):
            if 'module' not in snapshot.types(module):
                raise ValueError('topic module owner must be a module')
            neighbors.update(snapshot.refs(module, 'module/topics'))
        if any(neighbor not in topic_eid_to_id for neighbor in neighbors):
            raise ValueError('curriculum neighbors must reference known topics')
        neighbors.discard(eid)
        if neighbors:
            neighborhoods[identity] = [topic_eid_to_id[n] for n in sorted(neighbors)]
    engine = FireEngine(EncompassingGraph(edges, topic_id_to_eid), policy, difficulty, neighborhoods)
    performance_eid = snapshot.ref(learner_eid, 'learner/performance', required=False)
    if performance_eid is not None:
        if snapshot.owners(performance_eid, 'learner/performance') != (learner_eid,):
            raise ValueError('global performance must have exactly one learner owner')
        engine.global_ability[learner] = _ability(snapshot.entity(performance_eid), 'performance')
    progress_by_topic = {}
    for progress in snapshot.refs(learner_eid, 'learner/knowledge-profile'):
        if snapshot.owners(progress, 'learner/knowledge-profile') != (learner_eid,):
            raise ValueError('progress must have exactly one learner owner')
        state = snapshot.entity(progress)
        if not isinstance(state.get('progress/id'), str) or not state['progress/id']:
            raise ValueError('progress needs its stable string identity')
        topic = snapshot.ref(progress, 'progress/topic')
        if topic not in topic_eid_to_id or topic_eid_to_id[topic] in progress_by_topic:
            raise ValueError('profile needs one progress record per known topic')
        _uuid(snapshot.entity(snapshot.ref(progress, 'progress/policy')), 'policy/id')
        try:
            values = {field: state['progress/' + attribute] for attribute, field in STATE_FIELDS.items()}
            values['memory_at'] = instant_days(state['progress/memory-at'])
        except KeyError as error:
            raise ValueError(f'incomplete progress state: {error.args[0]}') from error
        values['ability'] = _ability(state, 'progress')
        if 'progress/last-direct-at' in state:
            values['last_direct_at'] = instant_days(state['progress/last-direct-at'])
        topic_id = topic_eid_to_id[topic]
        engine.seed(learner, topic_id, TopicState(**values))
        progress_by_topic[topic_id] = progress
    # No separate event clock is invented. Available task/item history and the
    # stored state anchors bound chronological processing after a restart.
    observed = set()
    for task in snapshot.refs(learner_eid, 'learner/activity'):
        if snapshot.owners(task, 'learner/activity') != (learner_eid,):
            raise ValueError('learner task has multiple learner associations')
        observed.add(task)
        observed.update(snapshot.refs(task, 'learner-task/items'))
    times = [instant_days(event['at']) for event in snapshot.status_history if event['entity'] in observed]
    if times:
        engine.latest[learner] = max(engine.latest.get(learner, -math.inf), *times)
    return LoadedRuntime(snapshot, engine, learner_eid, learner, policy_eid,
                         topic_eid_to_id, topic_id_to_eid, progress_by_topic, performance_eid)


def edn(value) -> str:
    """Encode the small native EDN value vocabulary used by engine writes."""
    if isinstance(value, Keyword):
        return ':' + str(value)
    if value is None:
        return 'nil'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, UUID):
        return '#uuid ' + json.dumps(str(value))
    if isinstance(value, datetime):
        return '#inst ' + json.dumps(instant(value).isoformat(timespec='milliseconds').replace('+00:00', 'Z'))
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, (int, float)):
        _number(value, 'EDN number')
        return repr(value)
    if isinstance(value, Mapping):
        return '{' + ' '.join(edn(Keyword(str(key))) + ' ' + edn(item)
                              for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))) + '}'
    if isinstance(value, (list, tuple)):
        return '[' + ' '.join(edn(item) for item in value) + ']'
    raise ValueError(f'unsupported EDN value {type(value).__name__}')


@dataclass(frozen=True)
class TransactionPlan:
    request_key: str
    compare_basis_t: int
    edn: str
    forms: tuple


def _check_task(loaded, task, completed_at, *, allow_paused=False):
    snapshot = loaded.snapshot
    if snapshot.owners(task, 'learner/activity') != (loaded.learner_eid,):
        raise ValueError('task must belong exclusively to this learner')
    status = snapshot.ident(snapshot.ref(task, 'learner-task/status'))
    allowed = {'learner-task.status/started'}
    if allow_paused:
        allowed.add('learner-task.status/paused')
    if status not in allowed:
        raise ValueError('only a started task can accept completion')
    at = instant_days(completed_at)
    if at < loaded.engine.latest.get(loaded.learner, -math.inf):
        raise ValueError('completion predates accepted learner evidence')
    if completed_at < snapshot.first_started(task):
        raise ValueError('completion predates its task start')


def _task_change(snapshot, raw, task, completed_at):
    change = {str(k).removeprefix(':'): deepcopy(v) for k, v in raw.items()}
    allowed = {'db/id', 'learner-task/status',
               'learner-task/xp-earned', 'learner-task/xp-base'}
    if type(change.get('db/id')) is not int or change['db/id'] != task or not set(change) <= allowed:
        raise ValueError('task changes contain an unsupported target or attribute')
    if ('learner-task/status' in change
            and snapshot.ident(change['learner-task/status']) not in {
                'learner-task.status/' + status for status in
                ('locked', 'unlocked', 'started', 'paused', 'completed', 'failed')}):
        raise ValueError('invalid learner-task/status')
    for name in ('learner-task/xp-earned', 'learner-task/xp-base'):
        if name in change and type(change[name]) is not int:
            raise ValueError(f'{name} must be an integer')
    change['db/ensure'] = Keyword('learner-task/validate')
    return change


def _check_responses(snapshot, item, additions, new_answers):
    existing = snapshot.refs(item, 'task-item/responses')
    responses = tuple(existing) + tuple(additions)
    if not responses and not new_answers:
        return []
    question = snapshot.ref(item, 'task-item/content')
    if 'question' not in snapshot.types(question) or snapshot.is_example(question):
        raise ValueError('only ordinary question items can carry responses')
    fields = set(snapshot.refs(question, 'question/answer-fields'))
    seen_fields, used_tempids = set(), set()
    ownership = []
    for response in responses:
        if isinstance(response, str) and not isinstance(response, Keyword) and response in new_answers:
            record = new_answers[response]
            field = snapshot.eid(record['field'])
            used_tempids.add(response)
            if snapshot.ident(snapshot.ref(field, 'answer-field/type')) != 'answer-field.type/blank':
                raise ValueError('new entered answers require a blank field')
            for prior in snapshot.refs(field, 'answer-field/choices'):
                old = snapshot.entity(prior)
                if (snapshot.eid(old['answer/type']) == snapshot.eid(record['answer/type'])
                        and old['answer/value'] == record['answer/value']):
                    raise ValueError('reuse the existing answer value in this field')
            ownership.append({'db/id': field, 'answer-field/choices': [response],
                              'db/ensure': Keyword('answer-field/validate')})
        else:
            response = snapshot.eid(response)
            owners = snapshot.owners(response, 'answer-field/choices')
            if len(owners) != 1 or 'answer' not in snapshot.types(response):
                raise ValueError('answer must belong to exactly one field')
            field = owners[0]
        if field not in fields or field in seen_fields:
            raise ValueError('response field is outside this question or answered more than once')
        seen_fields.add(field)
    if used_tempids != set(new_answers):
        raise ValueError('new answers must be attached to this task item')
    return ownership


def completion_transaction(loaded: LoadedRuntime, item_eid: int, completed_at: datetime,
                           changes: Sequence[Mapping], updated_engine: FireEngine) -> TransactionPlan:
    """Compose one item completion and all numerical updates into one EDB request.

    The basis guard is REQUIRED at submission: item CAS alone cannot detect a
    concurrently changed policy, graph, or another task's progress update.
    Native request receipts provide exact retry behavior without domain receipts.
    """
    snapshot = loaded.snapshot
    item_eid = snapshot.eid(item_eid)
    task = snapshot.item_task(item_eid, loaded.learner_eid)
    item = snapshot.entity(item_eid)
    old_status = snapshot.ref(item_eid, 'task-item/status')
    if snapshot.ident(old_status) != 'task-item.status/started':
        raise ValueError('only a started item can accept completion')
    if snapshot.active_items(loaded.learner_eid) != (item_eid,):
        raise ValueError('only one item may be actively timed per learner')
    completed_at = instant(completed_at)
    _check_task(loaded, task, completed_at)
    forms = []
    terminal_status = None
    task_change = None
    elapsed = snapshot.item_elapsed(item_eid, completed_at)
    task_elapsed = snapshot.task_elapsed(task, completed_at)
    new_answers, responses, seen_targets = {}, [], set()
    answer_ids = {_uuid(record, 'answer/id') for record in snapshot.entities.values()
                  if 'answer/id' in record}
    for raw in changes:
        change = {str(k).removeprefix(':'): deepcopy(v) for k, v in raw.items()}
        target = change.get('db/id')
        if isinstance(target, bool) or target in seen_targets:
            raise ValueError('change targets must be distinct numeric EIDs or response tempids')
        seen_targets.add(target)
        if target == item_eid:
            allowed = {'db/id', 'task-item/status', 'task-item/responses', 'task-item/performance'}
            if not set(change) <= allowed:
                raise ValueError('item changes contain an unsupported attribute')
            terminal_status = change.pop('task-item/status', None)
            ident = snapshot.ident(terminal_status) if terminal_status is not None else None
            content = snapshot.ref(item_eid, 'task-item/content')
            question = ('question' in snapshot.types(content)
                        and not snapshot.is_example(content))
            valid = {'task-item.status/' + s for s in ('correct', 'incorrect', 'skipped')} if question else {'task-item.status/completed'}
            if ident not in valid:
                raise ValueError('completion requires an appropriate terminal item status')
            if 'task-item/performance' in change:
                if ident not in {'task-item.status/correct', 'task-item.status/incorrect'}:
                    raise ValueError('only graded question attempts carry performance')
                change['task-item/performance'] = _number(change['task-item/performance'], 'performance', 0)
                if change['task-item/performance'] == 0:
                    raise ValueError('task-item/performance must be positive')
            if ident == 'task-item.status/skipped' and (change.get('task-item/responses') or snapshot.refs(item_eid, 'task-item/responses')):
                raise ValueError('a skipped question cannot contain submitted responses')
            change['task-item/elapsed-seconds'] = elapsed
            if 'task-item/responses' in change:
                if not isinstance(change['task-item/responses'], (list, tuple)):
                    raise ValueError('responses must be a collection of references')
                responses.extend(change['task-item/responses'])
            change['db/ensure'] = Keyword('task-item/validate')
        elif target == task:
            change = _task_change(snapshot, change, task, completed_at)
            change['learner-task/elapsed-seconds'] = task_elapsed
            task_change = change
        elif (type(target) is str and target and not target.startswith((':', 'engine-'))
              and target != 'edb.tx'):
            if set(change) != {'db/id', 'field', 'answer/id', 'answer/type', 'answer/value'}:
                raise ValueError('new answer needs a tempid, field, UUID, type, and value')
            if not isinstance(change['answer/value'], str):
                raise ValueError('entered answer value must be exact text')
            answer_id = _uuid(change, 'answer/id')
            if answer_id in answer_ids:
                raise ValueError('new answer UUID already belongs to another answer; reuse its reference')
            answer_ids.add(answer_id)
            field = snapshot.eid(change.pop('field'))
            change['answer/type'] = snapshot.eid(change['answer/type'])
            if snapshot.ident(change['answer/type']) not in {'answer.type/math', 'answer.type/text', 'answer.type/image'}:
                raise ValueError('unsupported answer type')
            new_answers[target] = dict(change, field=field)
            change['db/ensure'] = Keyword('answer/validate')
        else:
            raise ValueError('changes may target this item, its task, or a new answer')
        forms.append(change)
    if terminal_status is None:
        raise ValueError('completion requires an explicit terminal item status')
    forms.insert(0, [Keyword('db/cas'), item_eid, Keyword('task-item/status'), old_status, terminal_status])
    forms.extend(_check_responses(snapshot, item_eid, responses, new_answers))
    if task_change is None:
        forms.append({'db/id': task, 'learner-task/elapsed-seconds': task_elapsed, 'db/ensure': Keyword('learner-task/validate')})
    forms.append({'db/id': item_eid, 'db/ensure': Keyword('task-item/validate')})
    identity = _uuid(item, 'task-item/id')
    return _writeback(loaded, updated_engine, forms, 'complete-item', identity, completed_at)


def task_transaction(loaded: LoadedRuntime, task_eid: int, completed_at: datetime,
                     changes: Sequence[Mapping], updated_engine: FireEngine) -> TransactionPlan:
    """Close an expired active task without fabricating a question completion.

    ``changes`` contains a single map for this task, normally XP.
    This boundary owns the completed status and timestamp. The numerical state
    must have been derived solely from the task's already accepted observations.
    """
    snapshot = loaded.snapshot
    task = snapshot.eid(task_eid)
    completed_at = instant(completed_at)
    _check_task(loaded, task, completed_at, allow_paused=True)
    status = snapshot.ref(task, 'learner-task/status')
    if len(changes) > 1:
        raise ValueError('task expiry accepts one task change map')
    change = _task_change(snapshot, changes[0] if changes else {'db/id': task}, task, completed_at)
    if 'learner-task/status' in change and snapshot.ident(change['learner-task/status']) != 'learner-task.status/completed':
        raise ValueError('timer expiry must complete its task')
    change.pop('learner-task/status', None)
    change['learner-task/elapsed-seconds'] = snapshot.task_elapsed(task, completed_at)
    forms = [[Keyword('db/cas'), task, Keyword('learner-task/status'), status,
              Keyword('learner-task.status/completed')], change]
    active = snapshot.active_items(loaded.learner_eid)
    if len(active) > 1:
        raise ValueError('only one item may be actively timed per learner')
    for item in snapshot.refs(task, 'learner-task/items'):
        if item in active:
            forms.append([Keyword('db/cas'), item, Keyword('task-item/status'), snapshot.ref(item, 'task-item/status'), Keyword('task-item.status/paused')])
            forms.append({'db/id': item, 'task-item/elapsed-seconds': snapshot.item_elapsed(item, completed_at), 'db/ensure': Keyword('task-item/validate')})
    return _writeback(loaded, updated_engine, forms, 'expire-task',
                      _uuid(snapshot.entity(task), 'learner-task/id'), completed_at)


def _writeback(loaded, updated_engine, forms, operation, identity, at):
    if (asdict(updated_engine.policy) != asdict(loaded.engine.policy)
            or updated_engine.graph.id != loaded.engine.graph.id
            or updated_engine.difficulty_accuracy != loaded.engine.difficulty_accuracy
            or updated_engine.neighborhoods != loaded.engine.neighborhoods):
        raise ValueError('writeback must use the captured policy, graph, and difficulty inputs')
    for learner in set(loaded.engine.states) | set(updated_engine.states):
        if learner != loaded.learner and loaded.engine.states.get(learner) != updated_engine.states.get(learner):
            raise ValueError('completion cannot change another learner')
    for learner in set(loaded.engine.global_ability) | set(updated_engine.global_ability):
        if learner != loaded.learner and loaded.engine.global_ability.get(learner) != updated_engine.global_ability.get(learner):
            raise ValueError('completion cannot change another learner')
    links = []
    before_states = loaded.engine.states.get(loaded.learner, {})
    after_states = updated_engine.states.get(loaded.learner, {})
    if not set(before_states) <= set(after_states):
        raise ValueError('completion cannot delete existing topic state')
    for topic, state in sorted(after_states.items()):
        if topic not in loaded.topic_id_to_eid:
            raise ValueError('engine output refers to an unknown topic')
        state.__post_init__()
        if topic in before_states and asdict(state) == asdict(before_states[topic]):
            continue
        target = loaded.progress_by_topic.get(topic)
        if target is None:
            target = 'engine-progress-' + topic
            links.append(target)
        record = {'db/id': target, 'progress/topic': loaded.topic_id_to_eid[topic],
                  'progress/policy': loaded.policy_eid, 'progress/memory-at': _day_instant(state.memory_at),
                  'db/ensure': Keyword('progress/validate')}
        if isinstance(target, str):
            progress_identity = hashlib.sha256(json.dumps([loaded.learner, topic], separators=(',', ':')).encode()).hexdigest()
            record['progress/id'] = 'learner-topic-' + progress_identity
        for attribute, field in STATE_FIELDS.items():
            record['progress/' + attribute] = getattr(state, field) if field == 'learned' else float(getattr(state, field))
        record.update({'progress/' + field.replace('_', '-'): float(getattr(state.ability, field)) for field in ABILITY_FIELDS})
        if state.last_direct_at is not None:
            record['progress/last-direct-at'] = _day_instant(state.last_direct_at)
        elif topic in before_states and before_states[topic].last_direct_at is not None:
            forms.append([Keyword('db/retract'), target, Keyword('progress/last-direct-at'),
                          _day_instant(before_states[topic].last_direct_at)])
        forms.append(record)
    old_global = loaded.engine.global_ability.get(loaded.learner)
    new_global = updated_engine.global_ability.get(loaded.learner)
    if old_global is not None and new_global is None:
        raise ValueError('completion cannot remove global performance')
    learner_change = {'db/id': loaded.learner_eid, 'db/ensure': Keyword('learner/validate')}
    if links:
        learner_change['learner/knowledge-profile'] = links
    if new_global is not None and (old_global is None or asdict(new_global) != asdict(old_global)):
        new_global.__post_init__()
        target = loaded.performance_eid if loaded.performance_eid is not None else 'engine-global-performance'
        record = {'db/id': target, 'db/ensure': Keyword('performance/validate')}
        record.update({'performance/' + field.replace('_', '-'): float(getattr(new_global, field)) for field in ABILITY_FIELDS})
        forms.append(record)
        if loaded.performance_eid is None:
            learner_change['learner/performance'] = target
    forms.append(learner_change)
    forms.append({'db/id': 'edb.tx', 'db/txInstant': instant(at)})
    request_key = operation + '-' + hashlib.sha256(json.dumps([loaded.learner, identity], separators=(',', ':')).encode()).hexdigest()
    return TransactionPlan(request_key, loaded.snapshot.basis_t, edn(forms), _freeze(forms))
