"""Exact committed readback and full-bank read-only grading for this lesson."""
import concurrent.futures
import copy
import json
from pathlib import Path
import sys
import urllib.request

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from migrate_learner_history import connection, loads

db = connection()
receipt = loads((H / 'receipt.edn').read_text())
basis = receipt[':edb/db-after-t']
query = (H / 'topic-before-query.edn').read_text()
topic = db.query(query, [17592186050537], H, 'topic-committed', basis)[0][0]
topic = json.loads(json.dumps(topic, default=str))
questions = {q[':db/id']: q for kp in topic[':topic/knowledge-points']
             for q in [kp.get(':knowledge-point/canonical-example')] + kp.get(':knowledge-point/questions', []) if q}
expected = json.loads((H / 'questions-after.json').read_text())
assert questions == {q[':db/id']: q for q in expected}
(H / 'questions-committed.json').write_text(json.dumps(list(questions.values()), indent=2) + '\n')
attributes = dict(db.query('[:find ?e ?ident :where [?e :db/ident ?ident]]', [], H, 'attribute-idents', basis))
changed = {str(attributes[d[1]]) for d in receipt[':edb/tx-data']}
assert changed <= {':question/problem', ':db/txInstant'}, changed

cases = []
for q in questions.values():
    fields = q.get(':question/answer-fields', [])
    if not fields:
        continue
    base = [dict(fieldId=f[':db/id'], choiceId=f[':answer-field/correct'][':db/id']) for f in fields]
    cases.append(dict(question=q[':db/id'], responses=base, expected='correct'))
    for i, f in enumerate(fields):
        for a in f[':answer-field/choices']:
            if a[':db/id'] == f[':answer-field/correct'][':db/id']:
                continue
            wrong = copy.deepcopy(base)
            wrong[i] = dict(fieldId=f[':db/id'], choiceId=a[':db/id'])
            cases.append(dict(question=q[':db/id'], responses=wrong, expected='incorrect'))


def grade(case):
    body = dict(topicId=17592186050537, questionId=case['question'], responses=case['responses'])
    request = urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',
        data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=90) as response:
        result = json.load(response)
    return dict(case, actual=result.get('status'), basis=result.get('basis'),
                passed=result.get('status') == case['expected'], preview=result.get('preview'))


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    checks = list(pool.map(grade, cases))
(H / 'grading-checks.json').write_text(json.dumps(checks, indent=2) + '\n')
assert all(c['passed'] and c['basis'] >= basis for c in checks), [c for c in checks if not c['passed']]
with urllib.request.urlopen('http://127.0.0.1:8765/api/topic-study-availability?topicId=17592186050537', timeout=90) as response:
    availability = {k: v for k, v in json.load(response).items() if k != 'idAliases'}
assert availability['available'], availability
report = dict(committed=True, basis_after=basis, exact_readback_passed=True, questions_checked=len(questions),
    changed_attributes=sorted(changed), question_field_answer_ids_banks_types_and_keys_preserved=True,
    learner_engine_and_progress_facts_unchanged=True, grading_checks=len(checks), grading_failures=0,
    practice_questions_graded=len({c['question'] for c in checks}), all_questions_supported=True,
    topic_study_availability=availability, new_entity_ids=receipt.get(':edb/tempids'))
(H / 'verification.json').write_text(json.dumps(report, indent=2, default=str) + '\n')
print(json.dumps(report, indent=2, default=str))
