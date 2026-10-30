import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection
D=json.loads((H/'requested.json').read_text());b=D['basis_t'];db=connection();ids=[17592186049548,17592186049043,17592186050092]
topics=[r[0]for r in db.query('[:find (pull ?t [:db/id :topic/id :topic/title :topic/math-academy-id {:topic/knowledge-points [* {:knowledge-point/question-generator [*]}]}]) :in $ [?t ...] :where [?t :topic/id _]]',[ids],H,'topics',b)]
qids=sorted({q[':db/id']for t in topics for k in t[':topic/knowledge-points']for key in [':knowledge-point/questions',':knowledge-point/canonical-example']for q in(k.get(key,[])if isinstance(k.get(key,[]),list)else[k[key]])})
pattern='[* {:question/answer-fields [* {:answer-field/type [:db/ident]} {:answer-field/choices [* {:answer/type [:db/ident]}]} {:answer-field/correct [:db/id]}]}]';qs=[]
for offset in range(0,len(qids),60):qs.extend(r[0]for r in db.query('[:find (pull ?q '+pattern+') :in $ [?q ...] :where [?q :question/id _]]',[qids[offset:offset+60]],H,'questions-'+str(offset),b));print('Read questions',len(qs),'/',len(qids),flush=True)
acts=[r[0]for r in db.query('[:find (pull ?a [* {:activity/steps [*]}]) :in $ [?t ...] :where [?a :activity/scope ?t] [?a :activity/type :activity.type/lesson]]',[ids],H,'activities',b)]
cids=sorted({s[':step/content'][':db/id']for a in acts for s in a.get(':activity/steps',[])if ':step/content'in s})
contents=[r[0]for r in db.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[cids],H,'step-contents',b)]
snapshot={'basis_t':b,'topics':topics,'questions':qs,'activities':acts,'contents':contents};(H/'current.json').write_text(json.dumps(snapshot,default=str,indent=2)+'\n')
print([(t[':db/id'],t[':topic/title'])for t in topics]);print('Complete:',len(qs),'questions/examples,',len(contents),'step contents,',sum(':'+a in c for c in contents for a in['tutorial/content']),'tutorials');print('Generators',[(k[':db/id'],k.get(':knowledge-point/question-generator'))for t in topics for k in t[':topic/knowledge-points']if ':knowledge-point/question-generator'in k])
