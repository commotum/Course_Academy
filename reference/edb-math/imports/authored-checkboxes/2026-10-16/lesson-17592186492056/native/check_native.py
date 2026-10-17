"""Grade the actual speculative field banks and every preserved old radio choice."""
from pathlib import Path
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
ROOT = next(p for p in HERE.parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT / 'capture'))
from scripts.database.edn import loads

plan = json.loads((RUN / 'plan.json').read_text())
snapshot = loads((RUN / 'snapshot.edn').read_text())
after = {q[':db/id']: q for q in loads((RUN / 'preview-questions-after.edn').read_text())}
before = {q[':db/id']: q for [q] in snapshot['questions']}
records = []
for q in plan['questions']:
    actual = after[q['id']]
    original = before[q['id']]
    old = next(f for f in original[':question/answer-fields'] if f[':db/id'] == q['old_field'])
    old_key = old[':answer-field/correct'][':db/id']
    bank = {a[':db/id']: a for a in old[':answer-field/choices']}
    assert {c['old_answer'] for c in q['choice_mapping']} == set(bank)
    keyed = {f[':answer-field/key']: f for f in actual[':question/answer-fields']}
    assert set(keyed) == set(q['labels'])
    fields, checks, new_answers = [], [], {}
    for i, label in enumerate(q['labels']):
        f = keyed[label]
        assert f[':answer-field/type'][':db/ident'] == ':answer-field.type/checkbox'
        choices = [{':answer/id': str(a[':answer/id']), ':answer/type': a[':answer/type'][':db/ident'],
                    ':answer/value': a[':answer/value']} for a in f[':answer-field/choices']]
        assert {a[':answer/value'] for a in choices} == {'false', 'true'}
        correct = str(f[':answer-field/correct'][':answer/id'])
        fields.append({':answer-field/id': str(f[':answer-field/id']), ':answer-field/key': label,
                       ':answer-field/type': ':answer-field.type/checkbox', ':answer-field/choices': choices,
                       ':answer-field/correct': [':answer/id', correct]})
        for a in choices:
            new_answers[label, a[':answer/value']] = a[':answer/id']
            checks.append({'field_index': i, 'submitted_answer_id': a[':answer/id'],
                           'expected': 'accepted' if a[':answer/id'] == correct else 'rejected',
                           'purpose': 'Actual native db_after owned Boolean answer'})
    mapped = [{'old_answer': c['old_answer'],
               'answer_ids': [new_answers[l, str(l in c['selected']).lower()] for l in q['labels']],
               'expected': c['old_answer'] == old_key} for c in q['choice_mapping']]
    records.append({'label': q['ma_id'], 'record': {'question': {
        ':question/problem': actual[':question/problem'], ':question/answer-fields': fields},
        'knowledge_point': {'title': q.get('kp_title', 'Migrated lesson')},
        'generation': {'template': 'native-preview-db-after'}}, 'checks': checks,
        'mapped_responses': mapped})
(HERE / 'engine-input.json').write_text(json.dumps(records, indent=2) + '\n')
subprocess.run([str(HERE / 'check-checkbox-engine'), str(HERE / 'engine-input.json'),
                str(HERE / 'engine-report.json')], check=True)
report = json.loads((HERE / 'engine-report.json').read_text())
print(json.dumps({k: v for k, v in report.items() if k != 'records'}))
