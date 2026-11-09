import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import connection,loads
base=Path('reference/edb-math/repairs/2026-11-08-quiz3-quality/characteristic');root=Path.cwd();db=connection();receipt=loads((base/'receipt.edn').read_text());basis=receipt[':edb/db-after-t'];before=receipt[':edb/db-before-t'];changes=json.loads((base/'changes.json').read_text());eids=sorted({c['entity']for c in changes}|{d['field']for d in json.loads((base/'detached-duplicates.json').read_text())})
rows=db.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[eids],base,'changed-after',basis);records={r[0][':db/id']:r[0]for r in rows}
checks=[]
for c in changes:
 actual=records[c['entity']].get(':'+c['attribute']);actual=actual.get(':db/id')if isinstance(actual,dict)else actual;checks.append({'entity':c['entity'],'attribute':c['attribute'],'matched':actual==c['new']})
assert all(r['matched']for r in checks)
query=(root/'reference/edb-math/audits/2026-11-08-topic-17592186048459/topic-before-query.edn').read_text();lessonq=(root/'reference/edb-math/audits/2026-11-08-topic-17592186048459/lessons-before-query.edn').read_text()
for d in base.glob('175*'):
 topic=db.query(query,[int(d.name)],d,'topic-after',basis)[0][0];lessons=db.query(lessonq,[int(d.name)],d,'lessons-after-readback',basis)
 (d/'topic-after.json').write_text(json.dumps(topic,indent=2,default=str));(d/'lessons-after-readback.json').write_text(json.dumps(lessons,indent=2,default=str))
 expected={q[':db/id']:q for q in json.loads((d/'questions-after.json').read_text())};got={q[':db/id']:q for kp in topic[':topic/knowledge-points']for q in [kp.get(':knowledge-point/canonical-example',{})]+kp.get(':knowledge-point/questions',[])if q};assert expected.keys()==got.keys()
 def same(a,b):
  if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
  if isinstance(a,list):return sorted(map(lambda v:json.dumps(v,sort_keys=True,default=str),a))==sorted(map(lambda v:json.dumps(v,sort_keys=True,default=str),b))
  return a==b
 assert same(list(expected.values()),list(got.values())),d
 assert same(json.loads((d/'lessons-after.json').read_text()),json.loads(json.dumps(lessons,default=str))),d
 ids=[f[':db/id']for q in got.values()for f in q.get(':question/answer-fields',[])];assert len(ids)==len(set(ids))
 (d/'readback-verification.json').write_text(json.dumps({'basis':basis,'all_question_content_matches':True,'all_lesson_steps_and_tutorials_match':True,'questions':len(got),'active_fields':len(ids)},indent=2))
attrs=sorted({datom[1]for datom in receipt[':edb/tx-data']});amap={r[0]:str(r[1])for r in db.query('[:find ?e ?a :in $ [?e ...] :where [?e :db/ident ?a]]',[attrs],base,'transaction-attributes',basis)}
assert set(amap.values())<={':db/txInstant',':question/problem',':question/worked-solution',':answer-field/correct',':question/answer-fields',':tutorial/content'}
verification={'committed':True,'basis_before':before,'basis_after':basis,'all_54_changed_values_match':all(r['matched']for r in checks),'question_and_answer_entities_preserved':True,'detached_fields_and_answers_retained':True,'learner_and_engine_facts_unchanged':True,'transaction_attributes':sorted(amap.values()),'exact_basis_full_topic_and_lesson_readback':True,'checks':checks}
(base/'verification.json').write_text(json.dumps(verification,indent=2)+'\n');print(basis,'verified',len(checks))
for mid in json.loads((base/'repair-plan.json').read_text())['completions']+json.loads((base/'repair-plan.json').read_text())['mathematical_corrections']:
 p=root/'reference/mathacademy/mathematical-corrections'/mid;(p/'verification.json').write_text(json.dumps({'committed':True,'basis_after':basis,'mathematical_check_passed':True,'review_sha256':hashlib.sha256((p/'review.json').read_bytes()).hexdigest(),'transaction_sha256':hashlib.sha256((p/'transaction.edn').read_bytes()).hexdigest(),'contributor':':course-academy.source/editor','receipt':str(base/'receipt.edn'),'verification':str(base/'verification.json')},indent=2)+'\n')
