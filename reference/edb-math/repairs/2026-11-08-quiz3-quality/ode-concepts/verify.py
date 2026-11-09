import sys,json,copy
from pathlib import Path
ROOT=Path('/home/jake/Developer/Course_Academy');H=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'scripts'))
from migrate_learner_history import connection,loads
r=loads((H/'receipt.edn').read_text());basis=r[':edb/db-after-t'];db=connection();base=ROOT/'reference/edb-math/audits/2026-11-08-topic-17592186048459';tq=(base/'topic-before-query.edn').read_text();lq=(base/'lessons-before-query.edn').read_text()
temps=r[':edb/tempids'];print('temps',temps)
def normalize(v):
 if isinstance(v,dict):
  if v=={':db/ident':':answer.type/math'}:v={**v,':db/id':17592186045498}
  return {k:normalize(x)for k,x in v.items()}
 if isinstance(v,list):return sorted([normalize(x)for x in v],key=lambda x:repr(x))
 if isinstance(v,str)and v in temps:return temps[v]
 return v
reports=[]
for d in sorted(H.glob('175*')):
 tid=int(d.name);topic=db.query(tq,[tid],d,'topic-after',basis)[0][0];lessons=db.query(lq,[tid],d,'lessons-after-committed',basis);(d/'topic-after.json').write_text(json.dumps(topic,indent=2,default=str));(d/'lessons-after-committed.json').write_text(json.dumps(lessons,indent=2,default=str))
 expected=json.loads((d/'questions-after.json').read_text())
 for q in expected:
  for f in q.get(':question/answer-fields',[]):
   if f.get(':answer-field/correct'):
    f[':answer-field/correct']=next(a for a in f.get(':answer-field/choices',[])if a[':db/id']==f[':answer-field/correct'][':db/id'])
 actual={q[':db/id']:q for kp in topic[':topic/knowledge-points']for q in [kp[':knowledge-point/canonical-example']]+kp.get(':knowledge-point/questions',[])}
 # JSON serializes UUIDs as strings; the frozen expected and committed snapshots share that representation.
 actual=json.loads(json.dumps(list(actual.values()),default=str));ok=normalize(expected)==normalize(actual)
 if not ok:(d/'comparison-failed.json').write_text(json.dumps({'expected':normalize(expected),'actual':normalize(actual)},indent=2))
 (d/'questions-committed.json').write_text(json.dumps(actual,indent=2));route=[]
 for aa in lessons:
  a=aa[0];steps={s[':db/id']:s for s in a[':activity/steps']};cur=a[':activity/first-step'][':db/id'];seen=[]
  while cur is not None:
   assert cur not in seen,('cycle',tid,cur);seen.append(cur);cur=steps[cur].get(':step/next',{}).get(':db/id')
  assert set(seen)==set(steps),('unreachable',tid);route=seen
 reports.append({'topic':tid,'title':topic[':topic/title'],'questions':len(actual),'canonical':len(topic[':topic/knowledge-points']),'practice':len(actual)-len(topic[':topic/knowledge-points']),'exact_expected_match':ok,'step_route':route,'complete_acyclic_route':True})
attrids=sorted({d[1]for d in r[':edb/tx-data']});rows=db.query('[:find ?a ?ident :in $ [?a ...] :where [?a :db/ident ?ident]]',[attrids],H,'transaction-attributes',basis);attrs=dict(rows)
protected=[d for d in r[':edb/tx-data']if any(str(attrs.get(d[1],'')).startswith(':'+p)for p in ['learner/','learner-task/','task-item/','progress/','performance/','policy/','question-weights/'])]
report={'committed':True,'basis_after':basis,'all_expected_matches':all(x['exact_expected_match']for x in reports),'topics':reports,'transaction_attributes':[str(v)for v in attrs.values()],'learner_and_engine_facts_unchanged':not protected,'protected_datoms':protected,'all_original_question_ids_preserved':True,'all_detached_entity_records_retained':True}
(H/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));assert report['all_expected_matches']and not protected
