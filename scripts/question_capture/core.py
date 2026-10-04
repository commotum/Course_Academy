"""Capture policy, durable files, and additive content reconciliation."""
import hashlib
import json
import logging
import math
import os
import random
import re
import time
import uuid
from pathlib import Path

from edn import kw
from math_notation import identity as math_identity

ROOT = Path(__file__).resolve().parents[2]
ALLOWED = {
    'question/id', 'question/math-academy-id', 'question/is-example', 'question/problem',
    'question/worked-solution', 'question/difficulty', 'question/requires-calculator',
    'question/answer-fields', 'answer-field/id', 'answer-field/key', 'answer-field/type',
    'answer-field/choices', 'answer-field/correct', 'answer/id', 'answer/type',
    'answer/value', 'answer/feedback', 'knowledge-point/questions',
    'knowledge-point/canonical-example',
}


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    with temporary.open('w') as stream:
        stream.write(json.dumps(value, indent=2, default=str, allow_nan=False) + '\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    descriptor = os.open(path.parent, os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def journal(path, event, **values):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a') as stream:
        stream.write(json.dumps({'event': event, 'timestamp': time.time(), **values}, default=str) + '\n')
        stream.flush()
        os.fsync(stream.fileno())


class Pacer:
    def __init__(self, args, rng=None, sleeper=time.sleep):
        self.args, self.rng, self.sleeper = args, rng or random.Random(), sleeper

    def wait(self, kind, reason, elapsed=0):
        low, high = getattr(self.args, kind + '_min'), getattr(self.args, kind + '_max')
        if not math.isfinite(elapsed) or elapsed < 0:
            raise ValueError('Elapsed pacing credit must be finite and nonnegative')
        budget = self.rng.uniform(low, high)
        delay = max(0, budget - elapsed)
        logging.info('Waiting %.1fs (%s)%s', delay, reason,
                     ' [%.1fs budget, %.1fs solver time]' % (budget, elapsed) if kind == 'answer' else '')
        if delay:
            self.sleeper(delay)
        return delay

    def backoff(self, attempt, retry_after=0):
        delay = max(retry_after, min(30 * attempt, 180)) + self.rng.uniform(0, 5)
        logging.info('Backing off %.1fs before a read-only retry', delay)
        self.sleeper(delay)


def choose_sequence(rng, weight=0.7):
    if not math.isfinite(weight) or not 0 <= weight <= 1:
        raise ValueError('Sequence weight must be in [0, 1]')
    return 'CWCWC' if rng.random() < weight else 'WCWCC'


def choose_lesson(queue, priorities, completed_topics=()):
    candidates = []
    for item in queue:
        if item.get('task_type', 'lesson') != 'lesson':
            continue
        if item['topic_id'] in completed_topics:
            continue
        priority = priorities.get(item['topic_id'])
        if priority is not None and math.isfinite(priority):
            candidates.append({**item, 'priority': priority})
    return max(candidates, key=lambda i: (i['priority'], -i['topic_id']), default=None)


def choose_activity(queue, priorities, completed_topics=(), captured_tasks=()):
    """Prefer ranked lessons, then reviews, then the next uncaptured queue item."""
    available = [item for item in queue if item['task_id'] not in captured_tasks and
                 not (item.get('task_type', 'lesson') == 'lesson' and item['topic_id'] in completed_topics)]
    lesson = choose_lesson(available, priorities, completed_topics)
    if lesson:
        return {**lesson, 'task_type': 'lesson', 'selection_reason': 'priority'}
    # Reviews do not use lesson priorities and do not mark a topic lesson captured.
    review = next((item for item in available if item.get('task_type') == 'review'), None)
    if review:
        return {**review, 'selection_reason': 'review_queue_order'}
    if available:
        return {**available[0], 'task_type': available[0].get('task_type', 'lesson'),
                'selection_reason': 'queue_fallback'}
    return None


def choose_review_sequence(rng, weight=0.7):
    return choose_sequence(rng, weight)


def normalize(value, representation='math'):
    if representation == 'image':
        # The same source image can be saved under another activity directory or
        # exposed by MA under a second URL. Reuse the existing owned answer when
        # local bytes agree, without changing its persisted path.
        path = Path(value)
        if path.is_file():
            return 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()
        return value
    if representation != 'math':
        return value
    return math_identity(value)


def stable_id(kind, source):
    return uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy:ma:capture:' + kind + ':' + source)


def ref(attribute, value):
    return [kw(attribute), value]


def ensured(kind, **attrs):
    return {**{kw(k): v for k, v in attrs.items()}, kw('db/ensure'): [kw(kind + '/validate')]}


def validate_question(question):
    mid = question['math_academy_id']
    if not re.fullmatch(r'[qe]-\d+', mid):
        raise ValueError('Invalid Math Academy ID: ' + mid)
    if question['is_example'] != mid.startswith('e-'):
        raise ValueError('Example flag/ID mismatch: ' + mid)
    uuid.UUID(str(question['knowledge_point_id']))
    if not question.get('problem') or not question.get('worked_solution'):
        raise ValueError('Missing problem or solution: ' + mid)
    if question.get('difficulty') not in (None, 'easy', 'moderate', 'hard'):
        raise ValueError('Invalid difficulty: ' + mid)
    if not question['is_example'] and not question.get('difficulty'):
        raise ValueError('Practice needs activity difficulty metadata: ' + mid)
    fields = question.get('answer_fields', [])
    if not fields and not question['is_example']:
        raise ValueError('Practice needs locally observed answer fields: ' + mid)
    if len({f['key'] for f in fields}) != len(fields):
        raise ValueError('Duplicate field keys: ' + mid)
    for field in fields:
        if field['type'] not in ('radio', 'blank', 'select'):
            raise ValueError('Unsupported field type: ' + mid)
        correct = field.get('correct_value')
        values = [(c['type'], c['value']) for c in field['choices']]
        if correct is None or not any(v == correct for _, v in values):
            raise ValueError('Correct answer must be a choice: ' + mid)
        if len(set(values)) != len(values):
            raise ValueError('Duplicate answer values: ' + mid)
        if any(t not in ('math', 'text', 'image') or not isinstance(v, str) for t, v in values):
            raise ValueError('Invalid answer representation: ' + mid)


def build_transaction(content, topic, existing):
    """Fill missing facts only. Existing owned components and values are reused."""
    if content['topic_id'] != topic[':topic/math-academy-id']:
        raise ValueError('Topic mismatch')
    kps = {str(k[':knowledge-point/id']): k for k in topic[':topic/knowledge-points']}
    transaction, report = [], []
    records = content['questions'] + content.get('canonical_examples', [])
    if len({q['math_academy_id'] for q in records}) != len(records):
        raise ValueError('Duplicate question identities in capture')
    for question in records:
        validate_question(question)
        mid, kp_id = question['math_academy_id'], str(question['knowledge_point_id'])
        if kp_id not in kps:
            raise ValueError('KP is not a member of the selected topic: ' + kp_id)
        kp, old = kps[kp_id], existing.get(mid)
        example = question['is_example']
        canonical = kp.get(':knowledge-point/canonical-example')
        if example and canonical and canonical[':question/math-academy-id'] != mid:
            raise ValueError('Live example differs from this KP canonical ID; review ' + mid)
        if old and old.get(':question/is-example', example) != example:
            raise ValueError('Existing example flag conflicts: ' + mid)
        if old:
            owners = old.get(':knowledge-point/_canonical-example' if example else ':knowledge-point/_questions', [])
            if any(str(o[':knowledge-point/id']) != kp_id for o in owners):
                raise ValueError('Existing question belongs to another KP: ' + mid)
        target = ref('question/math-academy-id', mid) if old else mid
        update = {kw('db/id'): target}
        candidates = {'question/id': stable_id('question', mid), 'question/math-academy-id': mid,
                      'question/is-example': example, 'question/problem': question['problem'],
                      'question/worked-solution': question['worked_solution']}
        if question.get('difficulty'):
            candidates['question/difficulty'] = kw('question.difficulty/' + question['difficulty'])
        if question.get('requires_calculator') is not None:
            candidates['question/requires-calculator'] = question['requires_calculator']
        for attr, value in candidates.items():
            if not old or ':' + attr not in old:
                update[kw(attr)] = value
        old_fields = {f[':answer-field/key']: f for f in (old or {}).get(':question/answer-fields', [])}
        captured_fields = {f['key'] for f in question.get('answer_fields', [])}
        if not example and set(old_fields) - captured_fields:
            raise ValueError('Live capture omitted existing fields: ' + mid)
        field_links = []
        for field in question.get('answer_fields', []):
            key = field['key']
            previous = old_fields.get(key)
            field_token = mid + '/' + key
            field_target = previous[':db/id'] if previous else field_token
            fupdate = {kw('db/id'): field_target}
            if previous and previous[':answer-field/type'][':db/ident'] != ':answer-field.type/' + field['type']:
                raise ValueError('Field type conflict: ' + field_token)
            for attr, value in {'answer-field/id': stable_id('field', field_token),
                                'answer-field/key': key, 'answer-field/type': kw('answer-field.type/' + field['type'])}.items():
                if not previous or ':' + attr not in previous:
                    fupdate[kw(attr)] = value
            values = (previous or {}).get(':answer-field/choices', [])
            old_values = {(a[':answer/type'][':db/ident'].split('/')[-1], normalize(a[':answer/value'], a[':answer/type'][':db/ident'].split('/')[-1])): a for a in values}
            correct_target, choice_links = None, []
            for choice in field['choices']:
                signature = (choice['type'], normalize(choice['value'], choice['type']))
                answer = old_values.get(signature)
                token = field_token + '/' + hashlib.sha256((choice['type'] + ':' + choice['value']).encode()).hexdigest()
                answer_target = answer[':db/id'] if answer else token
                if not answer:
                    transaction.append(ensured('answer', **{'db/id': token, 'answer/id': stable_id('answer', token),
                                                           'answer/type': kw('answer.type/' + choice['type']), 'answer/value': choice['value']}))
                    choice_links.append(answer_target)
                    old_values[signature] = {':db/id': answer_target}
                if choice['value'] == field['correct_value']:
                    correct_target = answer_target
            old_correct = (previous or {}).get(':answer-field/correct')
            if old_correct:
                kind = old_correct[':answer/type'][':db/ident'].split('/')[-1]
                captured_kind = next(c['type'] for c in field['choices'] if c['value'] == field['correct_value'])
                if captured_kind != kind:
                    raise ValueError('Correct answer type conflict: ' + field_token)
                if normalize(old_correct[':answer/value'], kind) != normalize(field['correct_value'], kind):
                    raise ValueError('Correct answer conflict: ' + field_token + '; stored '
                                     + repr(old_correct[':answer/value']) + ', captured ' + repr(field['correct_value']))
            else:
                fupdate[kw('answer-field/correct')] = correct_target
            if choice_links:
                fupdate[kw('answer-field/choices')] = choice_links
            if len(fupdate) > 1:
                fupdate[kw('db/ensure')] = [kw('answer-field/validate')]
                transaction.append(fupdate)
            if not previous:
                field_links.append(field_target)
        if field_links:
            update[kw('question/answer-fields')] = field_links
        if len(update) > 1:
            update[kw('db/ensure')] = [kw('question/validate')]
            transaction.append(update)
        relation = 'knowledge-point/canonical-example' if example else 'knowledge-point/questions'
        linked = canonical is not None if example else mid in {q[':question/math-academy-id'] for q in kp.get(':knowledge-point/questions', [])}
        if not linked:
            transaction.append(ensured('knowledge-point', **{'db/id': ref('knowledge-point/id', uuid.UUID(kp_id)),
                                relation: target if example else [target]}))
        report.append({'math_academy_id': mid, 'existing': bool(old), 'knowledge_point_id': kp_id,
                       'added_question_attributes': [str(a)[1:] for a in update if a not in (':db/id', ':db/ensure')],
                       'missing_source_fields': question.get('missing_source_fields', [])})
    for item in transaction:
        forbidden = {str(a)[1:] for a in item} - ALLOWED - {'db/id', 'db/ensure'}
        if forbidden:
            raise ValueError('Forbidden transaction attributes: ' + repr(forbidden))
    return transaction, report
