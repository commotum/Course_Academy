"""Combine reviewed layout corrections and necessary question completions."""
import copy
import json
from pathlib import Path
import re
import sys

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
sys.path.insert(0, str(ROOT))
from scripts.question_capture.math_format import validate_prose, validate_tex

def read(path):
    return json.loads((H/path).read_text())

questions = {q[':db/id']: q for q in read('capture/questions.json')}
after = copy.deepcopy(questions)
mutations = copy.deepcopy(read('proposals.json'))
for row in mutations:
    assert after[row['entity']][':'+row['attribute']] == row['before']
    after[row['entity']][':'+row['attribute']] = row['after']
by_q = {(r['entity'], r['attribute']): r for r in mutations}
fields = {f[':db/id']: f for q in after.values() for f in q.get(':question/answer-fields', [])}
creations, unlinks, completion_rows = [], [], []
for i in range(1, 4):
    d = Path(f'review-{i}')
    extra_completions = read(d/'supplemental-completion-proposals.json') if (H/d/'supplemental-completion-proposals.json').exists() else []
    extra_answers = read(d/'supplemental-answer-creations.json') if (H/d/'supplemental-answer-creations.json').exists() else []
    for row in read(d/'completion-proposals.json') + extra_completions:
        completion_rows.append(row)
    for raw in read(d/'answer-creations.json') + extra_answers:
        row = {**raw, 'answer_type': raw.get('answer_type', raw.get('type')),
               'answer_value': raw.get('answer_value', raw.get('value')),
               'field_key': raw.get('field_key', raw.get('key'))}
        field = fields[row['field_entity']]
        assert field[':answer-field/key'] == row['field_key']
        assert ':answer-field/correct' not in field
        validate_tex(row['answer_value'])
        node = {':db/id': row['answer_tempid'], ':answer/id': row['answer_uuid'],
                ':answer/type': {':db/ident': row['answer_type']}, ':answer/value': row['answer_value']}
        field.setdefault(':answer-field/choices', []).append(node)
        field[':answer-field/correct'] = copy.deepcopy(node)
        creations.append(row)
    unlink_path = H/d/'duplicate-field-retractions.json'
    if unlink_path.exists():
        for row in read(d/'duplicate-field-retractions.json'):
            q = after[row['question_entity']]
            old = next(f for f in q[':question/answer-fields'] if f[':db/id'] == row['field_entity'])
            retained = next(f for f in q[':question/answer-fields'] if f[':db/id'] == row['retained_valid_field_entity'])
            assert not old.get(':answer-field/choices') and ':answer-field/correct' not in old
            assert old[':answer-field/key'] == retained[':answer-field/key']
            q[':question/answer-fields'] = [f for f in q[':question/answer-fields'] if f[':db/id'] != row['field_entity']]
            unlinks.append(row)
    correction_path = H/d/'prompt-correction-proposals.json'
    if correction_path.exists():
        for row in read(d/'prompt-correction-proposals.json'):
            assert after[row['entity']][':'+row['attribute']] == row['before']
            after[row['entity']][':'+row['attribute']] = row['after']
            by_q[row['entity'], row['attribute']]['after'] = row['after']
            by_q[row['entity'], row['attribute']]['authored_source_typo_correction'] = True
for row in completion_rows:
    if row['attribute'] == 'answer-field/correct':
        field = fields[row['entity']]
        assert ':answer-field/correct' not in field and row['before'] is None
        node = next(a for a in field[':answer-field/choices'] if a[':db/id'] == row['after'])
        field[':answer-field/correct'] = copy.deepcopy(node)
    else:
        assert row['attribute'] == 'question/worked-solution'
        assert after[row['entity']].get(':'+row['attribute']) == row['before']
        after[row['entity']][':'+row['attribute']] = row['after']
    mutations.append(row)
ids = sorted({r['entity'] for r in mutations if r['entity'] in questions})
notation_repairs = []
for qid in ids:
    attr = ':question/worked-solution'
    old = after[qid].get(attr, '')
    new = re.sub(r'\\text\{\\boldsymbol\}\s*(?:\{([A-Za-z])\}|([A-Za-z]))',
                 lambda m: r'\boldsymbol{' + (m[1] or m[2]) + '}', old)
    if new != old:
        assert not any(r['entity'] == qid and r['attribute'] == attr[1:] for r in mutations)
        mutations.append({'entity': qid, 'attribute': attr[1:], 'before': old, 'after': new,
                          'rationale': 'Restore the bold vector-function command emitted as literal text by source MathML.'})
        after[qid][attr] = new
        notation_repairs.append(qid)
for qid in ids:
    q = after[qid]
    seen = set()
    for field in q.get(':question/answer-fields', []):
        assert field[':answer-field/key'] not in seen, (qid, 'Duplicate key')
        seen.add(field[':answer-field/key'])
        assert field.get(':answer-field/correct') in field.get(':answer-field/choices', [])
    for attr in (':question/problem', ':question/worked-solution'):
        if attr in q:
            assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', q[attr]), (qid, 'Control character')
            validate_prose(q[attr])
plan = {'mutations': mutations, 'answer_creations': creations, 'field_unlinks': unlinks,
        'question_ids': ids, 'source': ':agent/codex'}
for name, value in [('plan.json', plan), ('questions-after.json', [after[q] for q in ids]),
                     ('questions-before.json', [questions[q] for q in ids]), ('bold-function-notation-repairs.json', notation_repairs)]:
    (H/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')
print(json.dumps({'questions': len(ids), 'mutations': len(mutations), 'owned_answers_added': len(creations),
                  'orphan_field_links_removed': len(unlinks), 'completion_rows': len(completion_rows)}))
