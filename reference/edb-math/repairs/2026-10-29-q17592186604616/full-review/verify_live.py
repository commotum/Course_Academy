"""Read complete repaired scope at the last confirmed transaction basis."""
import copy,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;P=H.parent;R=P.parents[3];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection
s1=json.loads((P/'lesson.json').read_text());s2=json.loads((P/'expanded-scope/current.json').read_text());qs=s1['questions']+s2['questions'];contents=s1['contents']+s2['contents'];dirs=[P/'initial-repair',P/'lesson-repair',H/'repair',H/'color-repair'];changes={};transactions=[]
for d in dirs:
 v=json.loads((d/'verification.json').read_text());assert v['committed']and v['only_exact_reviewed_datoms_changed'];transactions.append(v['basis_t'])
 for p in json.loads((d/'plan.json').read_text())['cas']:changes[p['entity'],':'+p['attribute']]=p['after']
def patch(obj):
 if isinstance(obj,list):return[patch(x)for x in obj]
 if not isinstance(obj,dict):return obj
 out={k:patch(v)for k,v in obj.items()}
 for(e,a),v in changes.items():
  if out.get(':db/id')==e:out[a]={':db/id':v}if a==':answer-field/correct'else v
 return out
expected={q[':db/id']:q for q in patch(qs)};basis=max(transactions);db=connection();pattern='[* {:question/answer-fields [* {:answer-field/type [:db/ident]} {:answer-field/choices [* {:answer/type [:db/ident]}]} {:answer-field/correct [:db/id]}]}]';ids=sorted(expected);actual={}
for offset in range(0,len(ids),60):
 rows=db.query('[:find (pull ?q '+pattern+') :in $ [?q ...] :where [?q :question/id _]]',[ids[offset:offset+60]],H,'live-questions-'+str(offset),basis);actual.update({r[0][':db/id']:r[0]for r in rows})
actual=json.loads(json.dumps(actual,default=str));actual={int(k):v for k,v in actual.items()};assert expected.keys()==actual.keys();extras=[];fields=answers=0
for e,q in expected.items():
 got=actual[e]
 for attr in[':question/id',':question/math-academy-id',':question/difficulty',':question/problem',':question/worked-solution']:assert got.get(attr)==q.get(attr),(e,attr)
 ef={f[':db/id']:f for f in q.get(':question/answer-fields',[])};gf={f[':db/id']:f for f in got.get(':question/answer-fields',[])};assert ef.keys()==gf.keys()
 for fid,f in ef.items():
  g=gf[fid];fields+=1
  for a in[':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/correct']:assert f.get(a)==g.get(a),(fid,a)
  ea={a[':db/id']:a for a in f[':answer-field/choices']};ga={a[':db/id']:a for a in g[':answer-field/choices']};assert ea.keys()<=ga.keys()
  for aid,a in ea.items():
   answers+=1
   for attr in[':answer/id',':answer/type',':answer/value']:assert a.get(attr)==ga[aid].get(attr),(aid,attr)
  if ea.keys()!=ga.keys():
   assert f[':answer-field/type'][':db/ident']==':answer-field.type/blank'
   extras.extend({'field':fid,'answer':aid}for aid in ga.keys()-ea.keys())
if extras:
 used=db.query('[:find ?a :in $ [?a ...] :where [?item :task-item/responses ?a]]',[[r['answer']for r in extras]],H,'additional-learner-responses',basis);assert{r[0]for r in used}=={r['answer']for r in extras}
tu={c[':db/id']:c for c in patch(contents)if ':tutorial/content'in c};actual_tu=db.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e :tutorial/id _]]',[sorted(tu)],H,'live-tutorials',basis)
assert len(actual_tu)==len(tu)
for c, in json.loads(json.dumps(actual_tu,default=str)):
 for attr in[':tutorial/id',':tutorial/math-academy-id',':tutorial/title',':tutorial/content']:assert c.get(attr)==tu[c[':db/id']].get(attr),(c[':db/id'],attr)
(H/'committed-questions.json').write_text(json.dumps(list(actual.values()),indent=2,default=str)+'\n');report={'passed':True,'basis_t':basis,'content_transactions':transactions,'questions_and_examples_verified':len(actual),'tutorials_verified':len(tu),'fields_with_UUIDs_types_keys_and_correct_links_verified':fields,'existing_answers_with_UUIDs_types_values_verified':answers,'distinct_repaired_fields_verified':len(changes),'existing_answer_banks_and_history_preserved':True,'additional_live_learner_answers_preserved':extras,'database_writes':0};(H/'live-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
