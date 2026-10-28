import concurrent.futures,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection
D=json.loads((H/'current.json').read_text());questions=[q for q in D['questions']if q[':db/id']in[17592186115783,17592186115785,17592186125222,17592186125224,17592186147768,17592186657619]];ids={q[':db/id']for q in questions}
for q in questions:
 for f in q.get(':question/answer-fields',[]):
  ids.add(f[':db/id']);ids.update(a[':db/id']for a in f.get(':answer-field/choices',[]))
def read(v):
 db=connection();rows=db.query('[:find ?e ?a :in $ ?v :where [?e ?a ?v]]',[v],H,'incoming-'+str(v),9122);return v,rows
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:incoming=dict(pool.map(read,sorted(ids)))
attrs=sorted({a for rows in incoming.values()for e,a in rows});db=connection();names=db.query('[:find ?a ?n :in $ [?a ...] :where [?a :db/ident ?n]]',[attrs],H,'incoming-attr-names',9122);ents=sorted({e for rows in incoming.values()for e,a in rows});records=[]
for i in range(0,len(ents),20):records +=[r[0]for r in db.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[ents[i:i+20]],H,'referrer-records-'+str(i),9122)]
out={'basis_t':9122,'questions':questions,'incoming':incoming,'attributes':names,'referrers':records};(H/'history-refs.json').write_text(json.dumps(out,default=str,indent=2));print('checked',len(ids),'entity IDs','incoming refs',sum(len(r)for r in incoming.values()),'attribute kinds',names)
