import sys,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection
D=json.loads((H/'current.json').read_text());q=next(q for q in D['questions']if q[':db/id']==17592186106313);ids=[q[':db/id']]+[f[':db/id']for f in q[':question/answer-fields']]+[a[':db/id']for f in q[':question/answer-fields']for a in f[':answer-field/choices']];db=connection();rows=[];errors=[]
for v in ids:
 try:r=db.query('[:find ?e ?a :in $ ?v :where [?e ?a ?v]]',[v],H,'duplicate-scalar-'+str(v),9047);rows.extend([v,e,a]for e,a in r);print(v,r,flush=True)
 except subprocess.CalledProcessError as e:errors.append({'id':v,'stderr':e.stderr});print(v,e.stderr,flush=True)
attrs=sorted({r[2]for r in rows});attrnames=db.query('[:find ?a ?n :in $ [?a ...] :where [?a :db/ident ?n]]',[attrs],H,'duplicate-attr-names',9047)
ents=sorted({r[1]for r in rows});records=[]
for i in range(0,len(ents),15):records +=[r[0]for r in db.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[ents[i:i+15]],H,'duplicate-referrers-'+str(i),9047)]
(H/'duplicate-history.json').write_text(json.dumps({'basis_t':9047,'question':q, 'incoming':rows,'attributes':attrnames,'referrers':records,'errors':errors},default=str,indent=2));print('done')
