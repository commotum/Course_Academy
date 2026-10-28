import sys,json
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection
D=json.loads((H/'current.json').read_text());q=next(q for q in D['questions']if q[':db/id']==17592186106313);ids=[f[':db/id']for f in q[':question/answer-fields']]+[a[':db/id']for f in q[':question/answer-fields']for a in f[':answer-field/choices']];db=connection();rows=db.query('[:find ?v ?e ?a :in $ [?v ...] :where [?e ?a ?v]]',[ids],H,'duplicate-incoming',9047)
ents=sorted({r[1]for r in rows});records=[]
for i in range(0,len(ents),30):records +=[r[0]for r in db.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[ents[i:i+30]],H,'duplicate-referrers-'+str(i),9047)]
(H/'duplicate-history.json').write_text(json.dumps({'basis':9047,'question':q, 'incoming':rows,'referrers':records},default=str,indent=2));print('incoming',rows,'referrers',len(records))
