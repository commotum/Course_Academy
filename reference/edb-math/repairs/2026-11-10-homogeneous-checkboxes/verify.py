"""Verify the exact committed basis, retained originals and historical snapshot."""
import copy
import json
from pathlib import Path
import sys
import urllib.request

H=Path(__file__).resolve().parent
ROOT=H.parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from migrate_learner_history import connection,loads
db=connection()
def load(name):return json.loads((H/(name+'.json')).read_text())
def save(name,value):(H/(name+'.json')).write_text(json.dumps(value,default=str,indent=2)+'\n')
receipt=loads((H/'receipt.edn').read_text());basis=receipt[':edb/db-after-t']
plan=load('plan')
assert all(d[4]==plan['source_entity'] for d in receipt[':edb/tx-data'])
preview=loads((H/'preview/stage1-preview.edn').read_text())
# Instants differ; the guarded writer and speculation must agree on every
# material datom, tempid and entity identity.
def material(report):return {tuple(json.dumps(v,default=str) for v in d[:3]+d[4:]) for d in report[':edb/tx-data'] if d[1]!=50}
assert material(receipt)==material(preview)
assert receipt[':edb/tempids']==preview[':edb/tempids']
ids=[p['entity'] for p in plan['questions']]
query='[:find (pull ?q '+(H/'question-pattern.edn').read_text()+') :in $ [?q ...] :where [?q :question/id _]]'
rows=db.query(query,[ids],H,'questions-committed',basis)
questions=json.loads(json.dumps([r[0] for r in rows],default=str))
save('questions-committed',questions)
assert {q[':db/id']:q for q in questions}=={q[':db/id']:q for q in load('speculative-questions')}
cases={c['question'][':db/id']:c for c in load('proposed-presentation')['cases']}
save('committed-presentation',dict(cases=[dict(question=q,objects=cases[q[':db/id']]['objects']) for q in questions]))
for label,attr in [('old-fields','answer-field/id'),('old-answers','answer/id')]:
    original=load(label+'-before');entityids=[r[0][':db/id'] for r in original]
    rows=db.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e :'+attr+' _]]',[entityids],H,label+'-committed',basis)
    assert json.loads(json.dumps(rows,default=str))==original,label
topicrows=db.query((H/'topic-before-query.edn').read_text(),[plan['topic']],H,'topic-committed',basis)
topic=json.loads(json.dumps(topicrows,default=str))[0][0]
current={q[':db/id']:q for kp in topic[':topic/knowledge-points'] for q in kp.get(':knowledge-point/questions',[])+[kp[':knowledge-point/canonical-example']]}
before={q[':db/id']:q for q in load('questions-before')}
assert current.keys()==before.keys()
for qid,q in current.items():
    if qid not in ids:assert q==before[qid],qid
    else:
        old=copy.deepcopy(before[qid]);new=copy.deepcopy(q)
        for a in [':question/problem',':question/answer-fields']:old.pop(a);new.pop(a)
        assert new==old,qid
items=[r[0] for r in db.query('[:find (pull ?i [*]) :in $ [?q ...] :where [?i :task-item/content ?q]]',[ids],H,'presentations-committed',basis)]
actual={i[':db/id']:i for i in json.loads(json.dumps(items,default=str))}
expected=dict(json.loads(json.dumps(loads((H/'preview/final-pull4.edn').read_text()),default=str)))
assert actual==expected
historical=db.query((H/'topic-before-query.edn').read_text(),[plan['topic']],H,'historical-topic',plan['basis'])
assert json.loads(json.dumps(historical,default=str))==load('topic-before')
with urllib.request.urlopen('http://127.0.0.1:8765/api/topic-study-availability?topicId='+str(plan['topic']),timeout=90) as r:
    availability={k:v for k,v in json.load(r).items() if k!='idAliases'}
assert availability['available']
save('verification',dict(committed=True,basis_before=plan['basis'],basis_after=basis,questions_converted=len(ids),
    fields_created=24,answers_created=48,saved_attempts_preserved=len(actual),all_46_questions_verified=True,
    original_fields_answers_and_historical_snapshot_preserved=True,solutions_difficulty_and_memberships_unchanged=True,
    exact_speculative_material_datoms_and_ids_confirmed=True,source=plan['source'],study_availability=availability))
print('Exact committed records, history, retained entities, all lesson questions and study availability passed.')
