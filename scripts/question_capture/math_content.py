"""Source-only content updates for the Source-aware math database.

Existing domain identities are resolved from the current database. Answer values
and field definitions are immutable: changed source fields replace ownership,
leaving the old components available in history.
"""
import copy
import hashlib
import json
import uuid

from core import ALLOWED, ensured, ref, stable_id, validate_question
from edn import kw


def scalar(value):
    return value.get(':db/id', value.get(':db/ident')) if isinstance(value, dict) else value


def resolve_knowledge_points(content, topics, existing):
    content = copy.deepcopy(content)
    records = content.get('questions', []) + content.get('canonical_examples', [])
    examples = {str(q['knowledge_point_id']): q['math_academy_id']
                for q in content.get('canonical_examples', [])}
    declarations = {str(p['id']): p for p in content.get('new_knowledge_points', [])}
    remapped, additions = {}, {}
    for q in records:
        tid = q.get('topic_id') or content.get('topic_id')
        if tid not in topics:
            raise ValueError('Question has no resolved source topic: ' + q['math_academy_id'])
        points = topics[tid].get(':topic/knowledge-points', [])
        original = str(q['knowledge_point_id'])
        source_example = examples.get(original) or declarations.get(original, {}).get('source_example_id')
        matches = [p for p in points if source_example and
                   p.get(':knowledge-point/canonical-example', {}).get(':question/math-academy-id') == source_example]
        if not matches:
            matches = [p for p in points if str(p[':knowledge-point/id']) == original]
        if not matches:
            owners = existing.get(q['math_academy_id'], {}).get(':knowledge-point/_questions', []) + \
                     existing.get(q['math_academy_id'], {}).get(':knowledge-point/_canonical-example', [])
            owner_ids = {str(p[':knowledge-point/id']) for p in owners}
            matches = [p for p in points if str(p[':knowledge-point/id']) in owner_ids]
        if not matches:
            matches = [p for p in points if p[':knowledge-point/title'] == q.get('knowledge_point')]
        if len(matches) > 1:
            raise ValueError('Ambiguous source knowledge point: ' + q['math_academy_id'])
        if matches:
            identity = str(matches[0][':knowledge-point/id'])
        elif source_example and content.get('task_type') == 'lesson' and content.get('lesson_definition', {}).get('complete'):
            identity = str(stable_id('knowledge-point', str(tid) + ':' + source_example))
            additions[identity] = {'id': identity, 'title': q['knowledge_point'],
                                   'source_example_id': source_example, 'topic_id': tid}
        else:
            raise ValueError('Cannot resolve source knowledge point: ' + q['math_academy_id'])
        if original in remapped and remapped[original] != identity:
            raise ValueError('Capture knowledge point maps to multiple current identities')
        remapped[original] = identity
        q['knowledge_point_id'] = identity
        q['topic_id'] = tid
    content['new_knowledge_points'] = list(additions.values())
    return content


def field_signature(field, stored=False):
    if stored:
        choices = {(a[':answer/type'][':db/ident'].split('/')[-1], a[':answer/value'])
                   for a in field.get(':answer-field/choices', [])}
        correct = field.get(':answer-field/correct')
        correct = ((correct[':answer/type'][':db/ident'].split('/')[-1], correct[':answer/value'])
                   if correct else None)
        return (field[':answer-field/key'], field[':answer-field/type'][':db/ident'].split('/')[-1],
                tuple(sorted(choices)), correct)
    choices = {(a['type'], a['value']) for a in field['choices']}
    correct = {a for a in choices if a[1] == field['correct_value']}
    if len(correct) != 1:
        raise ValueError('Correct answer must identify one typed source value')
    return field['key'], field['type'], tuple(sorted(choices)), next(iter(correct))


def build_math_content(content, topics, existing):
    transaction, retractions, changes = [], [], []
    points = {str(p[':knowledge-point/id']): p for t in topics.values()
              for p in t.get(':topic/knowledge-points', [])}
    for point in content.get('new_knowledge_points', []):
        identity = str(point['id'])
        if identity in points:
            continue
        if not any(str(q['knowledge_point_id']) == identity for q in content.get('questions', [])):
            raise ValueError('New knowledge point needs captured authoritative practice: ' + point['title'])
        target = 'kp-' + identity
        points[identity] = {':knowledge-point/id': uuid.UUID(identity),
                            ':knowledge-point/title': point['title'], '_target': target}
        transaction.append(ensured('knowledge-point', **{'db/id': target,
            'knowledge-point/id': uuid.UUID(identity), 'knowledge-point/title': point['title']}))
        transaction.append({kw('db/id'): ref('topic/math-academy-id', point['topic_id']),
                            kw('topic/knowledge-points'): [target]})
    records = [(q, False) for q in content.get('questions', [])] + \
              [(q, True) for q in content.get('canonical_examples', [])]
    if len({q['math_academy_id'] for q, _ in records}) != len(records):
        raise ValueError('Duplicate source question identity')
    canonical_ids = {q['math_academy_id'] for q, is_example in records if is_example}
    canonical_ids.update(p[':knowledge-point/canonical-example'][':question/math-academy-id']
                         for p in points.values() if p.get(':knowledge-point/canonical-example'))
    for question, is_example in records:
        mid = question['math_academy_id']
        old = existing.get(mid)
        validate_question(question, canonical=is_example, existing=old)
        if not is_example and not question.get('answer_fields'):
            raise ValueError('Authoritative practice requires all captured answer fields: ' + mid)
        point = points[str(question['knowledge_point_id'])]
        if not is_example and any(str(owner[':knowledge-point/id']) != str(point[':knowledge-point/id'])
                for owner in (old or {}).get(':knowledge-point/_questions', [])):
            raise ValueError('Existing question belongs to another KP: ' + mid)
        if not is_example and mid in canonical_ids:
            raise ValueError('Canonical example cannot enter practice: ' + mid)
        if is_example and (old or {}).get(':knowledge-point/_questions'):
            raise ValueError('Practice question cannot become a canonical example: ' + mid)
        relation = 'knowledge-point/canonical-example' if is_example else 'knowledge-point/questions'
        if is_example and point.get(':' + relation, {}).get(':question/math-academy-id') not in (None, mid):
            raise ValueError('Canonical example identity changed; source placement review required')
        target = ref('question/id', old[':question/id']) if old else mid
        update = {kw('db/id'): target}
        if not old:
            update.update({kw('question/id'): stable_id('question', mid), kw('question/math-academy-id'): mid})
        candidates = {'question/problem': question['problem'], 'question/worked-solution': question['worked_solution']}
        if question.get('difficulty'):
            candidates['question/difficulty'] = kw('question.difficulty/' + question['difficulty'])
        if question.get('requires_calculator') is not None:
            candidates['question/requires-calculator'] = question['requires_calculator']
        for attr, value in candidates.items():
            previous = (old or {}).get(':' + attr)
            compare = previous.get(':db/ident') if isinstance(previous, dict) else previous
            if compare != value:
                update[kw(attr)] = value
                if previous is not None:
                    retractions.append([old[':db/id'], kw(attr), scalar(previous)])
        old_fields = {f[':answer-field/key']: f for f in (old or {}).get(':question/answer-fields', [])}
        incoming = question.get('answer_fields', [])
        # Examples without observed fields preserve previously captured fields.
        captured = {f['key'] for f in incoming}
        if incoming or not is_example:
            for key in old_fields.keys() - captured:
                previous = old_fields[key]
                triple = [old[':db/id'], kw('question/answer-fields'), previous[':db/id']]
                transaction.append([kw('db/retract'), *triple]); retractions.append(triple)
        links = []
        for field in incoming:
            signature = field_signature(field)
            previous = old_fields.get(field['key'])
            if previous and field_signature(previous, stored=True) == signature:
                continue
            if previous:
                triple = [old[':db/id'], kw('question/answer-fields'), previous[':db/id']]
                transaction.append([kw('db/retract'), *triple]); retractions.append(triple)
            digest = hashlib.sha256(json.dumps(signature, ensure_ascii=False).encode()).hexdigest()
            token = mid + '/ma-source-field/' + digest
            answers = []
            correct = None
            for kind, value in signature[2]:
                answer_token = token + '/' + hashlib.sha256((kind + ':' + value).encode()).hexdigest()
                transaction.append(ensured('answer', **{'db/id': answer_token,
                    'answer/id': stable_id('answer', answer_token), 'answer/type': kw('answer.type/' + kind),
                    'answer/value': value}))
                answers.append(answer_token)
                if (kind, value) == signature[3]:
                    correct = answer_token
            transaction.append(ensured('answer-field', **{'db/id': token,
                'answer-field/id': stable_id('field', token), 'answer-field/key': field['key'],
                'answer-field/type': kw('answer-field.type/' + field['type']),
                'answer-field/choices': answers, 'answer-field/correct': correct}))
            links.append(token)
        if links:
            update[kw('question/answer-fields')] = links
        if len(update) > 1:
            update[kw('db/ensure')] = [kw('question/validate')]
            transaction.append(update)
        canonical = point.get(':knowledge-point/canonical-example')
        linked = bool(canonical and canonical[':question/math-academy-id'] == mid) if is_example else \
                 mid in {q[':question/math-academy-id'] for q in point.get(':knowledge-point/questions', [])}
        if not linked:
            transaction.append(ensured('knowledge-point', **{'db/id': point.get('_target',
                ref('knowledge-point/id', point[':knowledge-point/id'])), relation: target if is_example else [target]}))
        changes.append({'math_academy_id': mid, 'existing': bool(old),
                        'knowledge_point_id': str(point[':knowledge-point/id'])})
    return transaction, {'retractions': retractions, 'questions': changes}
