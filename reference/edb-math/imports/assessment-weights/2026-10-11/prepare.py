"""Prepare the approved assessment transaction from the preserved basis 1178."""
from pathlib import Path
import hashlib
import json
import sys
import uuid

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import loads, dumps, kw, Tagged

policies = loads((OUT / 'before.edn').read_text())
assert len(policies) == 1
policy = policies[0][0]
children = policy[':policy/question-selection-weights']
assert {str(c[':question-weights/activity-type'][':db/ident']) for c in children} == {
    ':activity.type/lesson', ':activity.type/review'
}
idents = {str(r[1]): (r[0], r[2]) for r in loads((OUT / 'idents.edn').read_text())}
source = ':agent/gpt-6.1-sol-high'
assert source in idents
for name in ['question-weights/validate', 'activity.type/assessment', 'policy/question-selection-weights']:
    assert ':' + name in idents

schema_text = (ROOT / 'schema/engine/2-question-weights.edn').read_text()
# The small codec does not parse comments: remove full comment lines only.
schema = loads('\n'.join(line for line in schema_text.splitlines() if not line.lstrip().startswith(';;')))
docs = {str(e[':db/ident']): e[':db/doc'] for e in schema if str(e[':db/ident']) in {
    ':question-weights/activity-type', ':question-weights/validate'
}}
weights = {'initial-easy': 50.0, 'initial-moderate': 40.0, 'initial-hard': 10.0,
           'remedial-easy': 45.0, 'remedial-moderate': 40.0, 'remedial-hard': 15.0}
forms = []
for ident, doc in docs.items():
    old = idents[ident][1][':db/doc']
    forms.append([kw('db/cas'), kw(ident), kw('db/doc'), old, doc])
forms.append({kw('db/id'): Tagged('edb/ref', policy[':db/id']),
              kw('policy/question-selection-weights'): [{
                  kw('db/id'): 'assessment-weights',
                  kw('question-weights/activity-type'): kw('activity.type/assessment'),
                  **{kw('question-weights/' + name): value for name, value in weights.items()},
                  kw('db/ensure'): kw('question-weights/validate'),
              }], kw('db/ensure'): kw('policy/validate')})
tx = OUT / 'transaction.edn'
tx.write_text(dumps(forms) + '\n')
intent_path = OUT / 'intent.json'
assert not intent_path.exists(), 'Do not overwrite a preserved request; recover its original intent.'
intent = {'database': 'math', 'endpoint': '/tmp/edb-math/writer.sock',
          'source': source, 'source_entity': idents[source][0],
          'lineage': '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1', 'read_basis': 1178,
          'request_key': 'assessment-question-weights-2026-10-11-' + str(uuid.uuid4()),
          'transaction_sha256': hashlib.sha256(tx.read_bytes()).hexdigest(),
          'policy_entity': policy[':db/id'], 'assessment_weights': weights,
          'schema_docs': docs,
          'preserved_lesson_review_children': [c[':db/id'] for c in children],
          'reason': 'User gave final approval to assessment initial 50/40/10, remedial 45/40/15, existing six-field validation, synchronized engine reads, seed and schema documentation updates.'}
intent_path.write_text(json.dumps(intent, indent=2) + '\n')
print('Prepared one assessment child and two schema documentation updates; source', source)
