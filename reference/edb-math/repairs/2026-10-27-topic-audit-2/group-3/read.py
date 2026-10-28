import json,sys
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import connection
H=Path(__file__).resolve().parent;P=H.parent;D=json.loads((P/'inventory.json').read_text());ids=json.loads((P/'group-3.json').read_text())['topics'];db=connection();basis=9122
query=lambda q,i,n:db.query(q,i,H,n,basis)
links=[r for r in D['links']if r[0]in ids];qs=sorted({r[2]for r in links});records=[]
for n in range(0,len(qs),30):
 records.extend(r[0]for r in query('[:find (pull ?q [*]) :in $ [?q ...] :where [?q :question/id ?id]]',[qs[n:n+30]],'questions-'+str(n)))
steps=[]
for tid in ids:steps+=query('[:find ?t ?a ?s ?c :in $ ?t :where [?a :activity/scope ?t] [?a :activity/steps ?s] [?s :step/content ?c]]',[tid],'steps-'+str(tid))
cs=sorted({r[3]for r in steps});content=[]
for n in range(0,len(cs),12):content.extend(r[0]for r in query('[:find (pull ?c [:db/id :tutorial/id :tutorial/math-academy-id :tutorial/title :tutorial/content :knowledge-point/id :knowledge-point/title :knowledge-point/canonical-example]) :in $ [?c ...] :where [?c ?a ?v]]',[cs[n:n+12]],'content-'+str(n)))
kps=sorted({r[1]for r in links});kp=[r[0]for r in query('[:find (pull ?kp [:db/id :knowledge-point/id :knowledge-point/title :knowledge-point/canonical-example]) :in $ [?kp ...] :where [?kp :knowledge-point/id ?id]]',[kps],'kps')]
gens=query('[:find ?kp ?g ?script :in $ [?kp ...] :where [?kp :knowledge-point/question-generator ?g] [?g :question-generator/script ?script]]',[kps],'generators');idents=query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],'idents')
for name,val in [('snapshot',{'basis_t':basis,'topics':[t for t in D['topics']if t['entity']in ids],'links':links,'steps':steps,'content':content,'questions':records,'kps':kp}),('generators',gens),('idents',idents)]: (H/(name+'.json')).write_text(json.dumps(val,indent=2,default=str))
print('questions',len(records),'content',len(content),'steps',len(steps),'generators',len(gens))
