"""Capture policy, durable files, and evidence-backed content reconciliation."""
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
# Keep capture independent of rebuilds in the EDB development checkout.
CAPTURE_EDB_BIN = ROOT / '.local/edb/capture-runtime/math-edb'
ALLOWED = {
    'question/id', 'question/math-academy-id', 'question/problem',
    'question/worked-solution', 'question/difficulty', 'question/requires-calculator',
    'question/answer-fields', 'answer-field/id', 'answer-field/key', 'answer-field/type',
    'answer-field/choices', 'answer-field/correct', 'answer/id', 'answer/type',
    'answer/value', 'answer/feedback', 'knowledge-point/questions',
    'knowledge-point/canonical-example',
    'knowledge-point/id', 'knowledge-point/title', 'topic/knowledge-points',
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
        self.check_stop()
        low, high = getattr(self.args, kind + '_min'), getattr(self.args, kind + '_max')
        if not math.isfinite(elapsed) or elapsed < 0:
            raise ValueError('Elapsed pacing credit must be finite and nonnegative')
        budget = self.rng.uniform(low, high)
        delay = max(0, budget - elapsed)
        logging.info('Waiting %.1fs (%s)%s', delay, reason,
                     ' [%.1fs budget, %.1fs solver time]' % (budget, elapsed) if kind == 'answer' else '')
        if delay:
            self.sleep(delay)
        return delay

    def backoff(self, attempt, retry_after=0):
        delay = max(retry_after, min(30 * attempt, 180)) + self.rng.uniform(0, 5)
        logging.info('Backing off %.1fs before a read-only retry', delay)
        self.sleep(delay)

    def check_stop(self):
        stop = getattr(self.args, 'stop_event', None)
        if stop is not None and stop.is_set():
            raise KeyboardInterrupt('Stopped; saved checkpoints are retained')

    def sleep(self, delay):
        stop = getattr(self.args, 'stop_event', None)
        if stop is not None and self.sleeper is time.sleep:
            stop.wait(delay)
            self.check_stop()
        else:
            self.sleeper(delay)


def choose_sequence(rng, weight=0.7):
    if not math.isfinite(weight) or not 0 <= weight <= 1:
        raise ValueError('Sequence weight must be in [0, 1]')
    return 'CWCWC' if rng.random() < weight else 'WCWCC'


def choose_topic_activity(queue, priorities, completed_topics=()):
    """Rank lessons and reviews together by their topic's capture priority."""
    candidates = []
    for item in queue:
        kind = item.get('task_type', 'lesson')
        if kind not in ('lesson', 'review'):
            continue
        if kind == 'lesson' and item['topic_id'] in completed_topics:
            continue
        priority = priorities.get(item['topic_id'])
        if priority is not None and math.isfinite(priority):
            candidates.append({**item, 'priority': priority})
    return max(candidates, key=lambda i: (i['priority'], -i['topic_id'],
                                         i.get('task_type', 'lesson') == 'lesson'), default=None)


def choose_lesson(queue, priorities, completed_topics=()):
    return choose_topic_activity([i for i in queue if i.get('task_type', 'lesson') == 'lesson'],
                                 priorities, completed_topics)


def choose_activity(queue, priorities, completed_topics=(), captured_tasks=()):
    """Placement, required assessments/retakes, then ranked practice and queue order."""
    diagnostic = next((item for item in queue if item.get('task_type') == 'diagnostic' and
                       item.get('capture_supported') and not item.get('in_progress') and
                       item['task_id'] not in captured_tasks), None)
    if diagnostic:
        return {**diagnostic, 'selection_reason':'placement_diagnostic'}
    tests = [item for item in queue if item.get('task_type') == 'assessment' and
             not item.get('in_progress') and item['task_id'] not in captured_tasks]
    required = next((item for item in tests if item.get('assessment_requirement') == 'required' and
                     item.get('capture_supported')), None)
    if required:
        return {**required, 'selection_reason': 'required_assessment'}
    retake = next((item for item in tests if item.get('assessment_is_retake') and
                   assessment_can_start(item) and item.get('capture_supported')), None)
    if retake:
        return {**retake, 'selection_reason': 'quiz_retake'}
    available = [item for item in queue if item.get('task_type','lesson') in ('lesson','review','multistep') and
                 item.get('capture_supported',True) and not item.get('in_progress',False) and
                 item['task_id'] not in captured_tasks and
                 not (item.get('task_type', 'lesson') == 'lesson' and item['topic_id'] in completed_topics)]
    ranked = choose_topic_activity(available, priorities, completed_topics)
    if ranked:
        return {**ranked, 'task_type': ranked.get('task_type', 'lesson'), 'selection_reason': 'priority'}
    # Unscored reviews retain queue order and never mark a topic lesson captured.
    review = next((item for item in available if item.get('task_type') == 'review'), None)
    if review:
        return {**review, 'selection_reason': 'review_queue_order'}
    if available:
        return {**available[0], 'task_type': available[0].get('task_type', 'lesson'),
                'selection_reason': 'queue_fallback'}
    optional = next((item for item in tests if item.get('assessment_requirement') == 'optional' and
                     item.get('capture_supported') and assessment_can_start(
                         {**item,'assessment_optional_fallback':True})), None)
    if optional:
        excluded = set(captured_tasks) | {item['task_id'] for item in queue
            if item.get('task_type','lesson') == 'lesson' and item.get('topic_id') in completed_topics}
        return {**optional,'assessment_optional_fallback':True,
                'assessment_fallback_excluded_tasks':sorted(excluded),
                'selection_reason':'optional_assessment_fallback'}
    unknown = next((item for item in tests if item.get('assessment_requirement') != 'optional'), None)
    if unknown:
        return {**unknown, 'selection_reason': 'assessment_requires_inspection', 'stop_before_start': True}
    return None


def assessment_requirement(details, *, only_activity=False, title=''):
    """Keep the source requirement notice and identify quiz-retake metadata."""
    notes = next((value for key, value in details.items() if key.lower() == 'notes'), None)
    metadata = {'assessment_is_retake': bool(re.search(r'\(retake\)\s*$', title, re.I) or
                                            re.search(r'\bquiz retake\b', notes or '', re.I))}
    count = re.search(r'optional\s+until\s+([\d,]+)\s+more\s+XP\s+have\s+been\s+earned', notes or '', re.I)
    if count:
        remaining = int(count[1].replace(',', ''))
        return {**metadata, 'assessment_notice': notes, 'optional_xp_remaining': remaining,
                'assessment_requirement': 'optional' if remaining else 'required'}
    if notes is not None and re.search(r'\brequired\b|\bmust\b.{0,30}\b(?:take|complete)\b', notes, re.I):
        return {**metadata, 'assessment_notice': notes, 'optional_xp_remaining': 0, 'assessment_requirement': 'required'}
    fields = {key.lower(): value for key, value in details.items()}
    # Required quizzes omit the optional Notes row. Recognize this only when
    # the expanded details are complete and the quiz is the sole offered task.
    if (notes is None and only_activity and
            re.fullmatch(r'[1-9]\d*', fields.get('questions') or '') and
            re.fullmatch(r'[1-9]\d*\s+minutes?', fields.get('time limit') or '', re.I)):
        return {**metadata, 'assessment_notice': None, 'optional_xp_remaining': 0,
                'assessment_requirement': 'required',
                'assessment_requirement_evidence': 'sole_queue_activity_without_optional_notice'}
    return {**metadata, 'assessment_notice': notes, 'optional_xp_remaining': None, 'assessment_requirement': 'unknown'}


def assessment_can_start(activity):
    """Optional quizzes need a selected no-alternative fallback and complete details."""
    if activity.get('assessment_requirement') == 'required':
        return True
    fields = {key.lower(): value for key, value in activity.get('assessment_details', {}).items()}
    allowed = (activity.get('assessment_is_retake') or
               (activity.get('assessment_optional_fallback') and activity.get('assessment_requirement') == 'optional'))
    return bool(allowed and
                re.fullmatch(r'[1-9]\d*', fields.get('questions') or '') and
                re.fullmatch(r'[1-9]\d*\s+minutes?', fields.get('time limit') or '', re.I))


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
    if representation == 'text':
        # Preserve prose exactly, but compare explicitly delimited inline math
        # structurally (for example "$x = 0$ only" versus "$x=0$ only").
        parts = re.split(r'(?<![\\$])\$(?!\$)([^$\n]+?)(?<!\\)\$(?!\$)', value)
        if len(parts) > 1:
            return repr(tuple(('math', math_identity(part)) if i % 2 else ('text', part)
                              for i, part in enumerate(parts)))
        return value
    if representation != 'math':
        return value
    return math_identity(value)


def stable_id(kind, source):
    return uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy:ma:capture:' + kind + ':' + source)


def compare_answers(a, b, representation='math', *, prompt='', kp_titles=()):
    """Notation identity first; only the native checker can prove more math."""
    prompt = re.sub(r'(?<!\S)Do not round the answer\.(?=\s|$)', '', prompt, flags=re.I)
    form_sensitive = any(term in prompt.lower() for term in
        ('round','decimal place','significant figure','significant digit',
         'simplest form','lowest terms','reduced fraction'))
    same_notation = (math_identity(a, preserve_form=True) == math_identity(b, preserve_form=True)
                     if form_sensitive and representation == 'math' else
                     normalize(a, representation) == normalize(b, representation))
    if a == b or same_notation:
        return {'outcome':'equivalent'}
    if representation != 'math':
        return {'outcome':'different'}
    from native_comparison import compare
    return compare(a, b, prompt=prompt, kp_titles=kp_titles)


def matching_answer(choice, values, **context):
    matches = [a for a in values if a[':answer/type'][':db/ident'] == ':answer.type/'+choice['type']
               and a[':answer/value'] == choice['value']]
    if matches:
        return matches[0]
    matches = [a for a in values if a[':answer/type'][':db/ident'] == ':answer.type/'+choice['type']
               and compare_answers(a[':answer/value'], choice['value'], choice['type'], **context)['outcome'] == 'equivalent']
    return matches[0] if len(matches) == 1 else None


def ref(attribute, value):
    return [kw(attribute), value]


def ensured(kind, **attrs):
    return {**{kw(k): v for k, v in attrs.items()}, kw('db/ensure'): [kw(kind + '/validate')]}


def validate_question(question, *, canonical=False, existing=None):
    if 'is_example' in question:
        raise ValueError('Retired capture field is_example; migrate saved content')
    mid = question['math_academy_id']
    if not re.fullmatch(r'[qe]-\d+', mid):
        raise ValueError('Invalid Math Academy ID: ' + mid)
    uuid.UUID(str(question['knowledge_point_id']))
    if (not (question.get('problem') or (existing or {}).get(':question/problem')) or
            not (question.get('worked_solution') or (existing or {}).get(':question/worked-solution'))):
        raise ValueError('Missing problem or solution: ' + mid)
    if question.get('difficulty') not in (None, 'easy', 'moderate', 'hard'):
        raise ValueError('Invalid difficulty: ' + mid)
    if not canonical and not (question.get('difficulty') or (existing or {}).get(':question/difficulty')):
        raise ValueError('Practice needs activity difficulty metadata: ' + mid)
    fields = question.get('answer_fields', [])
    if not fields and not canonical and not (existing or {}).get(':question/answer-fields'):
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
        # MA sometimes displays identical distractors in separate positions.
        # Keep those positions in the capture; EDB stores unique answer refs.
        if any(t not in ('math', 'text', 'image') or not isinstance(v, str) for t, v in values):
            raise ValueError('Invalid answer representation: ' + mid)


def build_transaction(content, topic, existing, reconciler=None):
    """Fill gaps and replace only attributes attested by saved evidence."""
    if content['topic_id'] != topic[':topic/math-academy-id']:
        raise ValueError('Topic mismatch')
    kps = {str(k[':knowledge-point/id']): k for k in topic[':topic/knowledge-points']}
    transaction, report = [], []
    # Collections describe the observed lesson role. Prefixes identify MA's
    # source ID namespace; canonical refs establish the database role.
    records = [(q, False) for q in content['questions']] + [
        (q, True) for q in content.get('canonical_examples', [])]
    if len({q['math_academy_id'] for q, _ in records}) != len(records):
        raise ValueError('Duplicate question identities in capture')
    canonical_ids = {q['math_academy_id'] for q, canonical in records if canonical}
    canonical_ids.update(k[':knowledge-point/canonical-example'][':question/math-academy-id']
                         for k in kps.values() if k.get(':knowledge-point/canonical-example'))
    canonical_ids.update(mid for mid, q in existing.items() if q.get(':knowledge-point/_canonical-example'))
    practice_ids = {q[':question/math-academy-id'] for k in kps.values()
                    for q in k.get(':knowledge-point/questions', [])}
    practice_ids.update(mid for mid, q in existing.items() if q.get(':knowledge-point/_questions'))
    for point in content.get('new_knowledge_points', []):
        kp_id, title, source = point['id'], point['title'], point['source_example_id']
        expected = str(stable_id('knowledge-point',str(content['topic_id'])+':'+source))
        example = [q for q in content.get('canonical_examples', []) if q['math_academy_id']==source
                   and str(q['knowledge_point_id'])==kp_id and q.get('knowledge_point')==title]
        practice = [q for q in content['questions'] if str(q['knowledge_point_id'])==kp_id]
        if (content.get('task_type')!='lesson' or kp_id!=expected or not title or
            len(example)!=1 or not practice or any(q.get('knowledge_point')!=title for q in practice)):
            raise ValueError('New KP needs its observed lesson example and matching practice pool')
        if kp_id in kps:
            if kps[kp_id][':knowledge-point/title']!=title:
                raise ValueError('Captured KP title conflicts with existing identity')
            continue
        if any(k[':knowledge-point/title']==title for k in kps.values()):
            raise ValueError('New KP duplicates an existing topic skill')
        identity = uuid.UUID(kp_id)
        target = 'kp-' + kp_id
        kps[kp_id] = {':knowledge-point/id':identity, ':knowledge-point/title':title, '_capture_target':target}
        transaction.append(ensured('knowledge-point', **{'db/id':target,
            'knowledge-point/id':identity,'knowledge-point/title':title}))
        # This only adds membership to an existing topic; its identity and
        # difficulty are unchanged. Validate the complete new KP separately.
        transaction.append({kw('db/id'):ref('topic/math-academy-id',content['topic_id']),
                            kw('topic/knowledge-points'):[target]})
    for question, example in records:
        mid, kp_id = question['math_academy_id'], str(question['knowledge_point_id'])
        validate_question(question, canonical=example, existing=existing.get(mid))
        if kp_id not in kps:
            raise ValueError('KP is not a member of the selected topic: ' + kp_id)
        kp, old = kps[kp_id], existing.get(mid)
        comparison = {'prompt':(old or {}).get(':question/problem', question.get('problem','')),
                      'kp_titles':[kp.get(':knowledge-point/title','')]}
        canonical = kp.get(':knowledge-point/canonical-example')
        if example and canonical and canonical[':question/math-academy-id'] != mid:
            raise ValueError('Live example differs from this KP canonical ID; review ' + mid)
        if not example and mid in canonical_ids:
            raise ValueError('Canonical example cannot enter a practice pool: ' + mid)
        if example and mid in practice_ids:
            raise ValueError('Practice question cannot become a canonical example: ' + mid)
        if old and not example:
            owners = old.get(':knowledge-point/_questions', [])
            if any(str(o[':knowledge-point/id']) != kp_id for o in owners):
                raise ValueError('Existing question belongs to another KP: ' + mid)
        if old and reconciler:
            owners = old.get(':knowledge-point/_questions', []) + old.get(':knowledge-point/_canonical-example', [])
            if not any(str(o[':knowledge-point/id']) == kp_id for o in owners):
                raise ValueError('Replacement needs an existing matching KP association: ' + mid)
        target = ref('question/math-academy-id', mid) if old else mid
        update = {kw('db/id'): target}
        candidates = {'question/id': stable_id('question', mid), 'question/math-academy-id': mid,
                      'question/problem': question.get('problem'),
                      'question/worked-solution': question.get('worked_solution')}
        candidates = {attr:value for attr,value in candidates.items() if value is not None and value != ''}
        if question.get('difficulty'):
            candidates['question/difficulty'] = kw('question.difficulty/' + question['difficulty'])
        if question.get('requires_calculator') is not None:
            candidates['question/requires-calculator'] = question['requires_calculator']
        for attr, value in candidates.items():
            if not old or ':' + attr not in old:
                update[kw(attr)] = value
            elif reconciler and attr in ('question/problem', 'question/worked-solution', 'question/difficulty'):
                prior = old[':' + attr]
                if attr == 'question/difficulty':
                    prior = prior[':db/ident']
                if reconciler.replace(mid, None, attr, prior, value, {'ma_capture'}):
                    update[kw(attr)] = value
        comparison['prompt'] = update.get(kw('question/problem'), comparison['prompt'])
        old_fields = {f[':answer-field/key']: f for f in (old or {}).get(':question/answer-fields', [])}
        captured_fields = {f['key'] for f in question.get('answer_fields', [])}
        layout_version = bool(old_fields and reconciler and
                              (reconciler.field_layout_action(mid, old, question) or
                               reconciler.single_answer_widget_action(mid, old, question, **comparison)))
        if layout_version:
            for previous in old_fields.values():
                transaction.append([kw('db/retract'), old[':db/id'], kw('question/answer-fields'), previous[':db/id']])
            # An unchanged key may now name a different component. The new
            # ownership set cannot inherit old values, feedback, or identities.
            old_fields = {}
        # Earlier imports used authored keys for a single radio field. The
        # live extractor calls it "selection". Match this one observed field,
        # then version its ownership; do not mutate the historical field key.
        if (reconciler and len(old_fields) == 1 and captured_fields == {'selection'} and
                next(iter(old_fields.values()))[':answer-field/type'][':db/ident'] == ':answer-field.type/radio' and
                question['answer_fields'][0]['type'] == 'radio'):
            old_fields = {'selection':next(iter(old_fields.values()))}
        if not example and captured_fields and set(old_fields) - captured_fields:
            raise ValueError('Live capture omitted existing fields: ' + mid)
        field_links = []
        for field in question.get('answer_fields', []):
            key = field['key']
            previous = old_fields.get(key)
            field_token = mid + '/' + key
            if layout_version:
                layout = {'problem':question['problem'], 'answer_fields':question['answer_fields']}
                field_token += '/ma-layout-v1/' + hashlib.sha256(json.dumps(layout, sort_keys=True).encode()).hexdigest()
            if previous and reconciler:
                action = reconciler.field_action(mid, previous, field, **comparison)
                if action == 'retain':
                    continue
                if action == 'version':
                    # Detach ownership only: retractEntity would cascade and
                    # destroy retained fields/answers. Fresh component identities
                    # keep historical answer strings immutable.
                    transaction.append([kw('db/retract'), old[':db/id'], kw('question/answer-fields'), previous[':db/id']])
                    feedback = {(a[':answer/type'][':db/ident'].split('/')[-1],
                                 normalize(a[':answer/value'], a[':answer/type'][':db/ident'].split('/')[-1])):a.get(':answer/feedback')
                                for a in previous[':answer-field/choices']}
                    field = {**field, 'choices':[dict(c) for c in field['choices']]}
                    for c in field['choices']:
                        retained = feedback.get((c['type'], normalize(c['value'], c['type'])))
                        if retained is not None:
                            c.setdefault('feedback', retained)
                    if field['type'] == 'blank':
                        field = {**field, 'choices': list(field['choices'])}
                        signatures = {(c['type'], normalize(c['value'], c['type'])) for c in field['choices']}
                        for a in previous[':answer-field/choices']:
                            kind = a[':answer/type'][':db/ident'].split('/')[-1]
                            if (kind, normalize(a[':answer/value'], kind)) not in signatures:
                                retained = {'type':kind, 'value':a[':answer/value']}
                                if ':answer/feedback' in a:
                                    retained['feedback'] = a[':answer/feedback']
                                field['choices'].append(retained)
                    version = {**field, 'choices':sorted(field['choices'], key=lambda c:(c['type'], c['value']))}
                    field_token += '/ma-v1/' + hashlib.sha256(json.dumps(version, sort_keys=True).encode()).hexdigest()
                    previous = None
            field_target = previous[':db/id'] if previous else field_token
            fupdate = {kw('db/id'): field_target}
            if previous and previous[':answer-field/type'][':db/ident'] != ':answer-field.type/' + field['type']:
                raise ValueError('Field type conflict: ' + field_token)
            for attr, value in {'answer-field/id': stable_id('field', field_token),
                                'answer-field/key': key, 'answer-field/type': kw('answer-field.type/' + field['type'])}.items():
                if not previous or ':' + attr not in previous:
                    fupdate[kw(attr)] = value
            values = (previous or {}).get(':answer-field/choices', [])
            correct_target, choice_links = None, []
            seen_choices = set()
            for choice in field['choices']:
                signature = (choice['type'], choice['value'])
                if signature in seen_choices:
                    continue
                seen_choices.add(signature)
                answer = matching_answer(choice, values, **comparison)
                token = field_token + '/' + hashlib.sha256((choice['type'] + ':' + choice['value']).encode()).hexdigest()
                answer_target = answer[':db/id'] if answer else token
                if not answer:
                    attrs = {'db/id': token, 'answer/id': stable_id('answer', token),
                             'answer/type': kw('answer.type/' + choice['type']), 'answer/value': choice['value']}
                    if choice.get('feedback') is not None:
                        if not isinstance(choice['feedback'], str):
                            raise ValueError('Invalid answer feedback')
                        attrs['answer/feedback'] = choice['feedback']
                    transaction.append(ensured('answer', **attrs))
                    choice_links.append(answer_target)
                if choice['value'] == field['correct_value']:
                    correct_target = answer_target
            old_correct = (previous or {}).get(':answer-field/correct')
            if old_correct:
                kind = old_correct[':answer/type'][':db/ident'].split('/')[-1]
                captured_kind = next(c['type'] for c in field['choices'] if c['value'] == field['correct_value'])
                if captured_kind != kind:
                    raise ValueError('Correct answer type conflict: ' + field_token)
                compared = compare_answers(old_correct[':answer/value'], field['correct_value'], kind, **comparison)
                if compared['outcome'] != 'equivalent':
                    raise ValueError('Correct answer conflict: ' + field_token + '; stored '
                                     + repr(old_correct[':answer/value']) + ', captured ' + repr(field['correct_value'])
                                     + '; comparison '+compared['outcome']+': '+compared.get('reason',''))
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
            transaction.append(ensured('knowledge-point', **{'db/id': kp.get('_capture_target',ref('knowledge-point/id', uuid.UUID(kp_id))),
                                relation: target if example else [target]}))
        report.append({'math_academy_id': mid, 'existing': bool(old), 'knowledge_point_id': kp_id,
                       'added_question_attributes': [str(a)[1:] for a in update if a not in (':db/id', ':db/ensure')],
                       'missing_source_fields': question.get('missing_source_fields', [])})
    for item in transaction:
        if isinstance(item, list):
            if len(item) != 4 or item[0] != ':db/retract' or item[2] != ':question/answer-fields':
                raise ValueError('Forbidden transaction operation')
            continue
        forbidden = {str(a)[1:] for a in item} - ALLOWED - {'db/id', 'db/ensure'}
        if forbidden:
            raise ValueError('Forbidden transaction attributes: ' + repr(forbidden))
    return transaction, report


def build_content_transaction(content, topics, existing, reconciler=None):
    """Assessments and multisteps span topics in one guarded content transaction."""
    records = content['questions'] + content.get('canonical_examples', [])
    if len({q['math_academy_id'] for q in records}) != len(records):
        raise ValueError('Duplicate question identities in capture')
    if content.get('task_type') not in ('assessment','multistep','diagnostic'):
        return build_transaction(content,topics[content['topic_id']],existing,reconciler)
    transaction, report = [], []
    if content.get('canonical_examples'):
        raise ValueError('Unexpected assessment canonical examples')
    for topic_id in sorted({q['topic_id'] for q in records}):
        group = {**content,'topic_id':topic_id,'questions':[q for q in records if q['topic_id']==topic_id]}
        changes, matches = build_transaction(group,topics[topic_id],existing,reconciler)
        transaction.extend(changes)
        report.extend(matches)
    return transaction, report
