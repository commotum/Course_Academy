"""Complete bounded snapshot for the explicitly assigned new audit scope."""
import concurrent.futures,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,loads
inventory=json.loads((H.parent/'inventory.json').read_text());scope=json.loads((H.parent/'group-1.json').read_text())
B=scope['basis_t'];assert B==9837 and inventory['basis_t']==B
ids=scope['topics'];topics=[t for t in inventory['topics']if t['entity']in ids];links=[l for l in inventory['links']if l[0]in ids];questions_ids=sorted({l[2]for l in links});assert len(questions_ids)==scope['questions']
pattern='[* {:question/difficulty [:db/id :db/ident]} {:question/answer-fields [* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]} {:answer-field/choices [* {:answer/type [:db/id :db/ident]}]}]}]'
def qbatch(offset):
    db=connection();batch=questions_ids[offset:offset+30];saved=H/('questions-'+str(offset)+'.edn')
    rows=loads(saved.read_text())if saved.exists()else db.query('[:find (pull ?q '+pattern+') :in $ [?q ...] :where [?q :question/id ?id]]',[batch],H,'questions-'+str(offset),B)
    records=[row[0]for row in rows];assert{q[':db/id']for q in records}==set(batch);return records
questions=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
    for records in pool.map(qbatch,range(0,len(questions_ids),30)):
        questions.extend(records);print('Questions',len(questions),'/',len(questions_ids),flush=True)
db=connection()
activity_scopes=db.query('[:find ?a ?t :where [?a :activity/type :activity.type/lesson] [?a :activity/scope ?t]]',[],H,'lesson-activity-scopes',B)
activity_ids=sorted({a for a,t in activity_scopes if t in ids});scope_by_activity={a:t for a,t in activity_scopes if t in ids};activities=[]
for offset in range(0,len(activity_ids),15):
    activities.extend(row[0]for row in db.query('[:find (pull ?a [:db/id :activity/id :activity/scope {:activity/steps [*]}]) :in $ [?a ...] :where [?a :activity/type :activity.type/lesson]]',[activity_ids[offset:offset+15]],H,'activity-forward-'+str(offset),B))
steps=[[scope_by_activity[a[':db/id']],a[':db/id'],s[':db/id'],s[':step/content'][':db/id']]for a in activities for s in a.get(':activity/steps',[])if ':step/content'in s]
content_ids=sorted({r[3]for r in steps});contents=[]
for offset in range(0,len(content_ids),20):
    contents.extend(row[0]for row in db.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[content_ids[offset:offset+20]],H,'contents-'+str(offset),B))
kps=sorted({l[1]for l in links});generators=db.query('[:find ?kp (pull ?g [*]) :in $ [?kp ...] :where [?kp :knowledge-point/question-generator ?g]]',[kps],H,'generators',B)
snapshot={'basis_t':B,'topics':topics,'links':links,'questions':sorted(questions,key=lambda q:q[':db/id']),'steps':steps,'activities':activities,'contents':contents,'generators':generators}
(H/'current.json').write_text(json.dumps(snapshot,default=str,indent=2)+'\n');print('Complete',len(questions),'questions/examples',len(contents),'activity content entities',len(generators),'active generators',flush=True)
