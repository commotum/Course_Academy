import json,sys
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import connection
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());ids={q[':db/id']for q in D['questions']};owners=json.loads((H/'all-context-owners.json').read_text());steps=sorted({r[0]for r in owners});db=connection();refs=[]
for n in range(0,len(steps),100):refs+=db.query('[:find ?s ?q :in $ [?s ...] :where [?s :step/content ?q]]',[steps[n:n+100]],H,'context-owner-content-'+str(n),9122)
by={s:q for s,q in refs};rows=[[by[s],s,m,v]for s,m,v in owners if by.get(s)in ids];(H/'all-contexts.json').write_text(json.dumps(rows,indent=2));fields=[{'entity':m,'attribute':'multistep/context','value':v}for m,v in sorted({(r[2],r[3])for r in rows})];(H/'context-render-input.json').write_text(json.dumps(fields,indent=2));print('contexts',len(fields),'containedquestions',len({r[0]for r in rows}))
