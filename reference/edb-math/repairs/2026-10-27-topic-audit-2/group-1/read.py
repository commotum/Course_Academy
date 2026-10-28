import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection
D=json.loads((H.parent/'inventory.json').read_text());ids=json.loads((H.parent/'group-1.json').read_text())['topics'];topics=[t for t in D['topics'] if t['entity'] in ids];links=[l for l in D['links'] if l[0] in ids];qs=sorted({l[2] for l in links});db=connection();B=9122
pattern='[* {:question/answer-fields [* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]} {:answer-field/choices [* {:answer/type [:db/id :db/ident]}]}]}]'
questions=[]
for i in range(0,len(qs),35):
 questions += [r[0] for r in db.query('[:find (pull ?q '+pattern+') :in $ [?q ...] :where [?q :question/id ?id]]',[qs[i:i+35]],H,'questions-'+str(i),B)]
 assert len(questions)==min(i+35,len(qs))
 print('questions',len(questions),flush=True)
steps=db.query('[:find ?t ?a ?s ?c :in $ [?t ...] :where [?a :activity/scope ?t] [?a :activity/type :activity.type/lesson] [?a :activity/steps ?s] [?s :step/content ?c]]',[ids],H,'steps',B)
cs=sorted({r[3] for r in steps});contents=[]
for i in range(0,len(cs),20):contents += [r[0] for r in db.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[cs[i:i+20]],H,'contents-'+str(i),B)]
kps=sorted({l[1] for l in links});gens=db.query('[:find ?kp (pull ?g [*]) :in $ [?kp ...] :where [?kp :knowledge-point/question-generator ?g]]',[kps],H,'generators',B)
(H/'current.json').write_text(json.dumps({'basis_t':B,'topics':topics,'links':links,'questions':questions,'steps':steps,'contents':contents,'generators':gens},default=str,indent=2)+'\n')
print('done',len(questions),len(contents),len(gens))
