import json,sys
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import connection
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());db=connection();ids=[q[':db/id']for q in D['questions']];rows=[]
for n in range(0,len(ids),30):
 rows+=db.query('[:find ?q ?s ?m ?context :in $ [?q ...] :where [?s :step/content ?q] [?m :multistep/steps ?s] [?m :multistep/context ?context]]',[ids[n:n+30]],H,'all-contexts-'+str(n),9122)
(H/'all-contexts.json').write_text(json.dumps(rows,indent=2,default=str));print('contexts',len(set(r[2]for r in rows)),'containedquestions',len(set(r[0]for r in rows)))
