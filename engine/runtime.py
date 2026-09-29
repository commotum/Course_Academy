"""Automatic item-completion boundary for the current schema records.

Call ``complete_item`` after application grading, then submit its transaction
through EDB with the returned request key and exact basis guard. Nothing is
persisted here: rejected/conflicting writes cannot mutate the loaded engine.
The numerical core is FIRe; activity stopping, placement and XP are application
rules. Local choices below are deliberately separate from the FIRe policy.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Mapping

from .activities import (DiagnosticBalance, assessment_xp_candidate,
                         evaluate_kp_prefix, evaluate_review_prefix,
                         lesson_xp_candidate, multistep_xp_candidate,
                         review_xp_candidate)
from .fire import Event, TopicState
from .fire.core import finite
from .schema import Keyword, LoadedRuntime, completion_transaction, instant, task_transaction


@dataclass(frozen=True)
class ActivityRules:
    """Local delivery choices, not recovered proprietary coefficients.

    Assessment/multistep questions share at most one base retention unit per
    topic in a task. Diagnostic skips affect placement but not answer accuracy.
    XP candidates are opt-in because the non-perfect equations are inferred.
    """
    diagnostic_skip_policy: str = 'negative'
    diagnostic_uses_assessment_accuracy: bool = False
    use_fitted_xp: bool = False

    def __post_init__(self):
        if self.diagnostic_skip_policy not in {'negative', 'neutral'}:
            raise ValueError('diagnostic skip policy must be negative or neutral')
        if any(type(v) is not bool for v in
               (self.diagnostic_uses_assessment_accuracy, self.use_fitted_xp)):
            raise ValueError('activity switches must be boolean')


@dataclass(frozen=True)
class Delivery:
    complete: bool
    passed: bool | None = None
    next_content: tuple[int, ...] = ()
    retry_question: int | None = None
    needs_questions_for: int | None = None


@dataclass
class Completion:
    transaction: object
    engine: object
    delivery: Delivery


def _owners(snapshot, attr, child):
    return [eid for eid in snapshot.entities if child in snapshot.refs(eid, attr)]


def _kind(snapshot, eid, names):
    kinds = [name for name in names if name + '/id' in snapshot.entity(eid)]
    if len(kinds) != 1:
        raise ValueError(f'{eid} must identify exactly one of {names}')
    return kinds[0]


def _ordered(snapshot, ids, index):
    indices = [snapshot.entity(e)[index] for e in ids]
    if any(type(i) is not int or i < 1 for i in indices) or len(set(indices)) != len(indices):
        raise ValueError(f'{index} must be positive and unique within its owner')
    return sorted(ids, key=lambda e: snapshot.entity(e)[index])


def _result(snapshot, entity):
    value = entity.get('task-item/result')
    if value is None:
        return None
    ident = str(snapshot.ident(value)).lstrip(':')
    if ident not in {'task-item.result/correct', 'task-item.result/incorrect', 'task-item.result/skipped'}:
        raise ValueError('unknown question result')
    return {'task-item.result/correct': True, 'task-item.result/incorrect': False,
            'task-item.result/skipped': None}[ident]


def _question(snapshot, item):
    content = item.get('task-item/content')
    return content is not None and 'question/id' in snapshot.entity(content)


def _question_pool(snapshot, activity, attr):
    pool = tuple(snapshot.refs(activity, attr))
    if not pool:
        raise ValueError('activity needs an available question pool')
    for question in pool:
        snapshot.topic_for_question(question)
    return pool


def scope_topics(snapshot, scope):
    """Resolve one curriculum scope plus prerequisite foundations."""
    topics, active = set(), set()
    children = {'course': 'course/units', 'unit': 'unit/modules', 'module': 'module/topics'}
    def walk(eid):
        if eid in active:
            raise ValueError('curriculum scope contains a cycle')
        kind = _kind(snapshot, eid, ('course', 'unit', 'module', 'topic'))
        if kind == 'topic':
            topics.add(eid)
            return
        active.add(eid)
        for child in snapshot.refs(eid, children[kind]):
            walk(child)
        active.remove(eid)
    walk(scope)
    pending = list(topics)
    while pending:
        topic = pending.pop()
        for prerequisite in snapshot.refs(topic, 'topic/prerequisites'):
            if _kind(snapshot, prerequisite, ('topic',)) != 'topic':
                raise ValueError('prerequisite must be a topic')
            if prerequisite not in topics:
                topics.add(prerequisite)
                pending.append(prerequisite)
    return topics


def _lesson_delivery(snapshot, activity, items):
    topic = snapshot.ref(activity, 'lesson/topic')
    members = set(snapshot.refs(topic, 'topic/knowledge-points'))
    steps = _ordered(snapshot, snapshot.refs(activity, 'lesson/steps'), 'lesson-step/index')
    if not steps or not members:
        raise ValueError('lesson needs steps and at least one assessed knowledge point')
    placements, seen_kps = [], set()
    for step in steps:
        content = snapshot.ref(step, 'lesson-step/content')
        kind = _kind(snapshot, content, ('tutorial', 'knowledge-point'))
        if kind == 'knowledge-point':
            if content not in members or content in seen_kps:
                raise ValueError('lesson knowledge-point membership is invalid or repeated')
            seen_kps.add(content)
            presentation = snapshot.ref(content, 'knowledge-point/example')
        else:
            presentation = content
        placements.append((content, kind, presentation))
    if seen_kps != members:
        raise ValueError('lesson does not cover all topic knowledge points')
    cursor = 0
    for content, kind, presentation in placements:
        if cursor == len(items):
            return Delivery(False, next_content=(presentation,))
        if items[cursor].get('task-item/content') != presentation:
            raise ValueError('item does not follow the authored lesson sequence')
        cursor += 1
        if kind == 'tutorial':
            continue
        pool = _question_pool(snapshot, content, 'knowledge-point/questions')
        outcomes, used = [], set()
        while cursor < len(items) and items[cursor].get('task-item/content') in pool:
            current = items[cursor]
            question = current['task-item/content']
            if question in used:
                raise ValueError('lesson practice must use a fresh question')
            if snapshot.topic_for_question(question) != topic:
                raise ValueError('lesson question resolves to another topic')
            used.add(question)
            outcomes.append(_result(snapshot, current))
            cursor += 1
            decision = evaluate_kp_prefix(outcomes)
            if decision.complete:
                break
        decision = evaluate_kp_prefix(outcomes)
        if not decision.complete:
            remaining = tuple(q for q in pool if q not in used)
            if cursor != len(items):
                raise ValueError('cannot advance before knowledge-point mastery')
            if not remaining:
                # Keep the observed answer even when the next question cannot
                # be prepared. Exhaustion establishes neither mastery nor failure.
                return Delivery(False, needs_questions_for=content)
            return Delivery(False, next_content=remaining)
        if not decision.passed:
            if cursor != len(items):
                raise ValueError('items follow a failed lesson')
            return Delivery(True, False)
    if cursor != len(items):
        raise ValueError('items follow the end of the lesson')
    return Delivery(True, True)


def _diagnostic_delivery(snapshot, activity, items, take_retry):
    probes = set(snapshot.refs(activity, 'diagnostic/probes'))
    start = snapshot.ref(activity, 'diagnostic/start')
    if not probes or start not in probes:
        raise ValueError('diagnostic start must be an owned probe')
    eligible = scope_topics(snapshot, snapshot.ref(activity, 'diagnostic/scope'))
    # Validate the whole graph before following a path, not just visited nodes.
    branches = ('on-correct', 'on-incorrect', 'on-skipped', 'on-silly-mistake')
    for probe in probes:
        question = snapshot.ref(probe, 'diagnostic-probe/question')
        topic = snapshot.topic_for_question(question)
        if topic not in eligible:
            raise ValueError('probe topic is outside diagnostic scope and its foundations')
        for branch in branches:
            target = snapshot.ref(probe, 'diagnostic-probe/' + branch, required=False)
            if target is not None and target not in probes:
                raise ValueError('diagnostic branch leaves its owner')
        alternate = snapshot.ref(probe, 'diagnostic-probe/on-silly-mistake', required=False)
        if alternate is not None:
            other = snapshot.ref(alternate, 'diagnostic-probe/question')
            difficulty = snapshot.ident(snapshot.ref(question, 'question/difficulty'))
            other_difficulty = snapshot.ident(snapshot.ref(other, 'question/difficulty'))
            if (other == question or snapshot.topic_for_question(other) != topic
                    or difficulty not in {'question.difficulty/easy', 'question.difficulty/moderate', 'question.difficulty/hard'}
                    or difficulty != other_difficulty
                    or snapshot.ref(alternate, 'diagnostic-probe/on-silly-mistake', required=False) is not None):
                raise ValueError('retry must be one different same-topic/same-difficulty question')
            ordinary = snapshot.ref(probe, 'diagnostic-probe/on-incorrect', required=False)
            if (ordinary is not None and ordinary != alternate and
                    snapshot.ref(ordinary, 'diagnostic-probe/question') == other):
                raise ValueError('incorrect and retry branches must be distinguishable from recorded question identity')
    active, finished = set(), set()
    def visit(probe):
        if probe in active:
            raise ValueError('diagnostic branches must terminate')
        if probe in finished:
            return
        active.add(probe)
        for branch in branches:
            target = snapshot.ref(probe, 'diagnostic-probe/' + branch, required=False)
            if target is not None:
                visit(target)
        active.remove(probe)
        finished.add(probe)
    for probe in probes:
        visit(probe)
    probe = start
    for index, item in enumerate(items):
        if probe is None or item.get('task-item/content') != snapshot.ref(probe, 'diagnostic-probe/question'):
            raise ValueError('item does not follow the diagnostic graph')
        result = _result(snapshot, item)
        branch = 'on-correct' if result is True else 'on-incorrect' if result is False else 'on-skipped'
        ordinary = snapshot.ref(probe, 'diagnostic-probe/' + branch, required=False)
        retry = snapshot.ref(probe, 'diagnostic-probe/on-silly-mistake', required=False) if result is False else None
        if index + 1 < len(items):
            next_question = items[index + 1].get('task-item/content')
            choices = [p for p in set((ordinary, retry)) if p is not None and
                       snapshot.ref(p, 'diagnostic-probe/question') == next_question]
            if len(choices) != 1:
                raise ValueError('recorded diagnostic continuation is ambiguous or invalid')
            probe = choices[0]
        else:
            if retry is not None and take_retry is None:
                raise ValueError('choose whether to accept the offered retry before completing this item')
            if take_retry and retry is None:
                raise ValueError('no retry is available for this result')
            selected = retry if take_retry else ordinary
            return Delivery(selected is None, next_content=() if selected is None else
                            (snapshot.ref(selected, 'diagnostic-probe/question'),),
                            retry_question=None if retry is None else snapshot.ref(retry, 'diagnostic-probe/question'))
    return Delivery(False, next_content=(snapshot.ref(start, 'diagnostic-probe/question'),))


def _delivery(snapshot, activity, kind, items, take_retry=False):
    if kind == 'lesson':
        return _lesson_delivery(snapshot, activity, items)
    if kind == 'diagnostic':
        return _diagnostic_delivery(snapshot, activity, items, take_retry)
    if any(not _question(snapshot, item) for item in items):
        raise ValueError(f'{kind} contains only questions')
    questions = [item['task-item/content'] for item in items]
    if kind == 'multistep':
        steps = _ordered(snapshot, snapshot.refs(activity, 'multistep/steps'), 'multistep-step/index')
        ordered = [snapshot.ref(step, 'multistep-step/question') for step in steps]
        if not ordered or questions != ordered[:len(questions)]:
            raise ValueError('items must follow multistep question placements')
        if len(questions) == len(ordered):
            return Delivery(True)
        return Delivery(False, next_content=(ordered[len(questions)],))
    pool = _question_pool(snapshot, activity, kind + '/questions')
    if len(set(questions)) != len(questions) or not set(questions).issubset(pool):
        raise ValueError('questions must be distinct members of the activity')
    remaining = tuple(q for q in pool if q not in questions)
    if kind == 'review':
        topic = snapshot.ref(activity, 'review/topic')
        if len(pool) != 5 or any(snapshot.topic_for_question(q) != topic for q in pool):
            raise ValueError('live review requires five questions from its target topic')
        decision = evaluate_review_prefix([_result(snapshot, item) for item in items])
        return Delivery(decision.complete, decision.passed if decision.complete else None,
                        () if decision.complete else remaining)
    return Delivery(not remaining, next_content=remaining)


def _place_diagnostic(loaded, engine, items, at, rules):
    snapshot = loaded.snapshot
    prerequisites = {t: tuple(loaded.topic_eid_to_id[p] for p in snapshot.refs(e, 'topic/prerequisites'))
                     for e, t in loaded.topic_eid_to_id.items()}
    balance = DiagnosticBalance(prerequisites, skip_policy=rules.diagnostic_skip_policy)
    for observed in items:
        t = loaded.topic_eid_to_id[snapshot.topic_for_question(observed['task-item/content'])]
        correct = _result(snapshot, observed)
        # The application may supply a reduced correct-answer weight. Neither
        # elapsed seconds nor a retry implies an undisclosed MA weight curve.
        weight = observed.get('task-item/performance', 1.0) if correct is True else 1.0
        balance.apply(t, correct, weight=weight)
    states = engine.states.setdefault(loaded.learner, {})
    for target, repetitions in balance.positive_repetitions().items():
        state = states.get(target)
        if state is not None and state.learned:
            continue  # Placement must not erase an established retention history.
        if state is None:
            state = TopicState(accuracy=engine.policy.prior_accuracy, learned=False)
            states[target] = state
        state.learned = True
        state.repetitions = repetitions
        state.memory = engine.policy.restored_memory
        state.memory_at = at
        state.interval_days = engine.policy.interval(repetitions)


def complete_item(loaded: LoadedRuntime, item_eid: int, *, completed_at: datetime,
                  result: bool | None = None, elapsed_seconds: float | None = None,
                  performance: float = 1.0, response_refs: tuple[int | str, ...] = (),
                  response_entities: tuple[Mapping, ...] = (), take_retry: bool | None = None,
                  xp_award: int | None = None, rules: ActivityRules | None = None) -> Completion:
    """Handle a newly completed presentation using authoritative app grading.

    ``None`` is an explicit skip for a question and simple completion for
    instruction. Typed responses are explicit-tempid maps; selected responses
    reference canonical answers. The grader owns answer verification. Selection
    from the learner queue never changes these credit rules.

    ``take_retry`` records the learner's choice made with an incorrect diagnostic
    submission. Returning a retry offer alone does not create a task item.
    """
    rules = rules or ActivityRules()
    snapshot = loaded.snapshot
    completed_at = instant(completed_at)
    at = completed_at.timestamp() / 86400.0
    if at < loaded.engine.latest.get(loaded.learner, float('-inf')):
        raise ValueError('completion predates accepted learner evidence')
    if result is not None and type(result) is not bool:
        raise ValueError('result must be bool or explicit skip None')
    if take_retry is not None and type(take_retry) is not bool:
        raise ValueError('retry selection must be boolean or unspecified')
    if xp_award is not None and (type(xp_award) is not int):
        raise ValueError('XP award must be an integer')
    if elapsed_seconds is not None:
        finite(elapsed_seconds, 'elapsed seconds', 0)
    finite(performance, 'performance', 0)
    if performance <= 0:
        raise ValueError('performance must be positive')
    item = dict(snapshot.entity(item_eid))
    if item.get('task-item/completed-at') is not None or item.get('task-item/result') is not None:
        raise ValueError('item already has completion evidence')
    owners = _owners(snapshot, 'learner-task/items', item_eid)
    if len(owners) != 1:
        raise ValueError('item must have one learner-task owner')
    task_eid = owners[0]
    task = snapshot.entity(task_eid)
    if _owners(snapshot, 'learner/activity', task_eid) != [loaded.learner_eid]:
        raise ValueError('task must belong to the loaded learner')
    status = str(snapshot.ident(snapshot.ref(task_eid, 'learner-task/status'))).lstrip(':')
    if status != 'learner-task.status/in-progress':
        raise ValueError('only an in-progress task can accept completion')
    started = instant(task['learner-task/started-at']) if 'learner-task/started-at' in task else None
    if started is not None and completed_at < started:
        raise ValueError('completion predates task start')
    activity = snapshot.ref(task_eid, 'learner-task/activity')
    kind = _kind(snapshot, activity, ('lesson', 'review', 'assessment', 'multistep', 'diagnostic'))
    if kind == 'diagnostic' and performance > 1:
        raise ValueError('diagnostic positive evidence weight must be at most one')
    if kind == 'lesson':
        # Conservative local readiness rule: prerequisites are learned and not
        # currently due. The queue origin cannot bypass this mastery boundary.
        target = snapshot.ref(activity, 'lesson/topic')
        states = loaded.engine.states.get(loaded.learner, {})
        for prerequisite in snapshot.refs(target, 'topic/prerequisites'):
            state = states.get(loaded.topic_eid_to_id[prerequisite])
            if (state is None or not state.learned or
                    state.memory_now(completed_at.timestamp() / 86400) <= loaded.engine.policy.due_threshold):
                raise ValueError('lesson prerequisite is not currently ready')
    if take_retry and kind != 'diagnostic':
        raise ValueError('retry branching applies only to diagnostics')
    item_ids = _ordered(snapshot, snapshot.refs(task_eid, 'learner-task/items'), 'task-item/index')
    prefix = []
    for eid in item_ids:
        if eid == item_eid:
            break
        previous = snapshot.entity(eid)
        if previous.get('task-item/completed-at') is None:
            raise ValueError('previous presentation has not completed')
        if instant(previous['task-item/completed-at']) > completed_at:
            raise ValueError('item completion order must be chronological')
        if _question(snapshot, previous) and previous.get('task-item/result') is None:
            raise ValueError('previous question result is unknown')
        prefix.append(previous)
    if any(snapshot.entity(e).get('task-item/completed-at') is not None for e in item_ids[item_ids.index(item_eid)+1:]):
        raise ValueError('cannot insert evidence before completed presentations')
    question = _question(snapshot, item)
    if not question and (result is not None or response_refs or response_entities):
        raise ValueError('instruction completion cannot have an answer result')
    content = item.get('task-item/content')
    if content is None:
        raise ValueError('new presentation needs known content')
    item_change = {'db/id': item_eid}
    if elapsed_seconds is not None:
        item_change['task-item/elapsed-seconds'] = float(elapsed_seconds)
    if question:
        name = 'correct' if result is True else 'incorrect' if result is False else 'skipped'
        # For replay through snapshot helpers, find the installed enum entity.
        ident = 'task-item.result/' + name
        matches = [eid for eid, entity in snapshot.entities.items()
                   if str(entity.get('db/ident', '')).lstrip(':') == ident]
        if len(matches) != 1:
            raise ValueError('result enum must be installed exactly once')
        item['task-item/result'] = matches[0]
        item_change['task-item/result'] = Keyword(ident)
        if result is not None:
            item_change['task-item/performance'] = float(performance)
            item['task-item/performance'] = float(performance)
        elif response_refs or response_entities or snapshot.refs(item_eid, 'task-item/responses'):
            raise ValueError('a skipped question cannot contain submitted responses')
        if response_refs:
            item_change['task-item/responses'] = list(response_refs)
    items = prefix + [item]
    before = _delivery(snapshot, activity, kind, prefix, take_retry=False)
    if before.complete or content not in before.next_content:
        # A recorded retry can follow the available alternate of the prior item.
        if content != before.retry_question:
            raise ValueError('presentation is not a permitted continuation')
    delivery = _delivery(snapshot, activity, kind, items, take_retry)
    limit = snapshot.entity(activity).get(kind + '/time-limit-seconds')
    if limit is not None:
        finite(limit, 'time limit', 0)
        if limit <= 0 or started is None:
            raise ValueError('timed task requires a positive limit and actual start time')
        if (completed_at - started).total_seconds() > limit:
            raise ValueError('answer arrived after the task time limit')
        if (completed_at - started).total_seconds() == limit:
            delivery = Delivery(True, delivery.passed)
    engine = deepcopy(loaded.engine)
    topic_eid = snapshot.topic_for_question(content) if question else None
    topic = loaded.topic_eid_to_id[topic_eid] if question else None
    event_id = str(item['task-item/id'])
    assessment = kind == 'assessment' or kind == 'diagnostic' and rules.diagnostic_uses_assessment_accuracy
    if question and result is not None:
        engine.apply_accuracy(Event(event_id + ':answer', loaded.learner, topic, at,
                                    result, assessment=assessment, kind=kind))
    if kind in {'assessment', 'multistep'} and question and result is not None:
        questions = (snapshot.refs(activity, 'assessment/questions') if kind == 'assessment' else
                     [snapshot.ref(step, 'multistep-step/question') for step in snapshot.refs(activity, 'multistep/steps')])
        counts = Counter(snapshot.topic_for_question(q) for q in questions)
        engine.apply_retention(Event(event_id + ':retention', loaded.learner, topic, at, result,
                                     quality=performance / counts[topic_eid], assessment=assessment, kind=kind))
    if kind in {'lesson', 'review'} and delivery.complete:
        target = snapshot.ref(activity, kind + '/topic')
        submitted = [i for i in items if _question(snapshot, i) and _result(snapshot, i) is not None]
        quality = (sum(performance if i is item else i.get('task-item/performance', 1.0)
                       for i in submitted) / len(submitted)) if submitted else 1.0
        engine.apply_retention(Event(event_id + ':retention', loaded.learner,
                                     loaded.topic_eid_to_id[target], at, bool(delivery.passed),
                                     quality=quality, learned=kind == 'lesson' and bool(delivery.passed), kind=kind))
    if kind == 'diagnostic' and delivery.complete:
        _place_diagnostic(loaded, engine, items, at, rules)
    changes = [dict(entity) for entity in response_entities] + [item_change]
    if delivery.complete:
        change = {'db/id': task_eid, 'learner-task/status': Keyword('learner-task.status/completed'),
                  'learner-task/completed-at': completed_at}
        if delivery.passed is not None:
            change['learner-task/outcome'] = Keyword('learner-task.outcome/' + ('passed' if delivery.passed else 'failed'))
        outcomes = [_result(snapshot, i) for i in items if _question(snapshot, i)]
        award = xp_award
        base = task.get('learner-task/xp-base')
        if award is None and base is not None and kind in {'lesson', 'review', 'assessment', 'multistep'}:
            calculators = {'lesson': lesson_xp_candidate, 'review': review_xp_candidate,
                           'assessment': assessment_xp_candidate, 'multistep': multistep_xp_candidate}
            # Perfect-work observations are supported; partial fitted awards require opt-in.
            if kind in {'lesson', 'review'} and all(o is True for o in outcomes) or rules.use_fitted_xp and kind in {'assessment', 'multistep'}:
                award = calculators[kind](base, outcomes)
        if award is not None:
            change['learner-task/xp-earned'] = award
        changes.append(change)
    elif xp_award is not None:
        raise ValueError('task XP can be awarded only at completion')
    engine.latest[loaded.learner] = at
    transaction = completion_transaction(loaded, item_eid, completed_at, changes, engine)
    return Completion(transaction, engine, delivery)


def expire_task(loaded: LoadedRuntime, task_eid: int, *, completed_at: datetime,
                xp_award: int | None = None, rules: ActivityRules | None = None) -> Completion:
    """Timer callback for an assessment or diagnostic; invent no answer results.

    Already submitted answers keep their one-time accuracy/retention effects.
    Diagnostic placement uses only observed answers. No XP formula is guessed
    for a partially delivered timed exam; pass an explicit award when defined.
    The application owns the actual timer and submits the returned guarded plan.
    """
    rules = rules or ActivityRules()
    completed_at = instant(completed_at)
    at = completed_at.timestamp() / 86400
    snapshot = loaded.snapshot
    task = snapshot.entity(task_eid)
    if _owners(snapshot, 'learner/activity', task_eid) != [loaded.learner_eid]:
        raise ValueError('task must belong to the loaded learner')
    if snapshot.ident(snapshot.ref(task_eid, 'learner-task/status')) != 'learner-task.status/in-progress':
        raise ValueError('only an in-progress task can expire')
    activity = snapshot.ref(task_eid, 'learner-task/activity')
    kind = _kind(snapshot, activity, ('assessment', 'diagnostic'))
    limit = snapshot.entity(activity).get(kind + '/time-limit-seconds')
    finite(limit, 'time limit', 0)
    if limit <= 0 or 'learner-task/started-at' not in task:
        raise ValueError('expiry requires a positive limit and known start')
    if (completed_at - instant(task['learner-task/started-at'])).total_seconds() < limit:
        raise ValueError('task time limit has not expired')
    if at < loaded.engine.latest.get(loaded.learner, float('-inf')):
        raise ValueError('expiry predates accepted learner evidence')
    if xp_award is not None and type(xp_award) is not int:
        raise ValueError('XP award must be an integer')
    items, pending = [], False
    for eid in _ordered(snapshot, snapshot.refs(task_eid, 'learner-task/items'), 'task-item/index'):
        item = snapshot.entity(eid)
        if 'task-item/completed-at' not in item:
            pending = True
            continue
        if pending or not _question(snapshot, item) or 'task-item/result' not in item:
            raise ValueError('timed activity has an incomplete or invalid answer history')
        items.append(item)
    _delivery(snapshot, activity, kind, items, take_retry=False)
    engine = deepcopy(loaded.engine)
    if kind == 'diagnostic':
        _place_diagnostic(loaded, engine, items, at, rules)
    engine.latest[loaded.learner] = at
    change = {'db/id': task_eid, 'learner-task/completed-at': completed_at}
    if xp_award is not None:
        change['learner-task/xp-earned'] = xp_award
    transaction = task_transaction(loaded, task_eid, completed_at, [change], engine)
    return Completion(transaction, engine, Delivery(True))
