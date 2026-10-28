import json,sys
from pathlib import Path
sys.path.insert(0,'scripts')
from migrate_learner_history import connection
H=Path(__file__).resolve().parent; P=H.parent
D=json.loads((P/'inventory.json').read_text()); ids=json.loads((P/'group-3.json').read_text())['topics']; db=connection()
links=[r for r in D['question_links'] if r[0] in ids] if 'question_links' in D else None
print(D.keys())
def query(q,i,n):return db.query(q,i,H,n,9047)
links=query('[:find ?t ?kp ?q :in $ [?t ...] :where [?t :topic/knowledge-points ?kp] (or [?kp :knowledge-point/questions ?q] [?kp :knowledge-point/canonical-example ?q])]',[ids],'links')
qs=sorted({r[2] for r in links}); records=[]
for n in range(0,len(qs),35):records += [r[0] for r in query('[:find (pull ?q [*]) :in $ [?q ...] :where [?q :question/id ?id]]',[qs[n:n+35]],'questions-'+str(n))]
steps=query('[:find ?t ?a ?s ?c :in $ [?t ...] :where [?a :activity/scope ?t] [?a :activity/type :activity.type/lesson] [?a :activity/steps ?s] [?s :step/content ?c]]',[ids],'steps')
cs=sorted({r[3] for r in steps});content=[]
for n in range(0,len(cs),15):content += [r[0] for r in query('[:find (pull ?c [*]) :in $ [?c ...] :where [?c ?a ?v]]',[cs[n:n+15]],'content-'+str(n))]
kps=sorted({r[1] for r in links});kp=[r[0] for r in query('[:find (pull ?kp [:db/id :knowledge-point/id :knowledge-point/title :knowledge-point/generator-script :knowledge-point/generator-package :knowledge-point/canonical-example]) :in $ [?kp ...] :where [?kp :knowledge-point/id ?id]]',[kps],'kps')]
(H/'snapshot.json').write_text(json.dumps({'basis_t':9047,'topics':[t for t in D['topics'] if t['entity'] in ids],'links':links,'steps':steps,'content':content,'questions':records,'kps':kp},indent=2))
print('questions',len(records),'content',len(content),'steps',len(steps))
