import json,sys
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import connection
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());targets=['q-167332','q-167786','q-166079','q-167322','q-167775'];qs=[q for q in D['questions']if q.get(':question/math-academy-id')in targets or q[':db/id']in[17592186235434,17592186235482,17592186514385]];db=connection();ids=[q[':db/id']for q in qs]
a=db.query('[:find ?q ?s ?m (pull ?m [:db/id :multistep/id :multistep/context]) :in $ [?q ...] :where [?s :step/content ?q] [?m :multistep/steps ?s]]',[ids],H,'context-parents',9122)
b=db.query('[:find ?q ?s (pull ?s [*]) :in $ [?q ...] :where [?s :step/content ?q]]',[ids],H,'context-any-steps',9122)
(H/'context-parent-evidence.json').write_text(json.dumps({'questions':[{'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'problem':q.get(':question/problem')}for q in qs],'parents':a,'steps':b},indent=2,default=str));print(json.dumps({'questions':[(q[':db/id'],q.get(':question/math-academy-id'))for q in qs],'parents':a,'steps':[(r[0],r[1])for r in b]},indent=2,default=str))
