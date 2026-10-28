import json,sys
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import connection
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());owners={f[':db/id']:q[':db/id']for q in D['questions']for f in q.get(':question/answer-fields',[])if f[':answer-field/type'][':db/id']==17592186408166};ids=sorted(owners);db=connection();basis=db.basis();rows=[]
for offset in range(0,len(ids),100):
 rows+=db.query('[:find ?f ?key ?correct :in $ [?f ...] :where [?f :answer-field/key ?key] [?f :answer-field/correct ?correct]]',[ids[offset:offset+100]],H,'checkbox-labels-current-batch-'+str(offset),basis)
(H/'checkbox-labels-current.json').write_text(json.dumps({'basis_t':basis,'labels':[{'question':owners[f],'entity':f,'attribute':'answer-field/key','value':label,'correct':correct}for f,label,correct in rows]},indent=2));print('basis',basis,'labels',len(rows));assert len(rows)==476
