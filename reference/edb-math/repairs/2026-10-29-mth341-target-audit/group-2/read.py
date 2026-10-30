import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection
inv=json.loads((H.parent/'inventory.json').read_text());conf=json.loads((H.parent/'group-2.json').read_text());topics=[t for t in inv['topics']if t[':db/id']in conf['topics']];ids=[k[':db/id']for t in topics for k in t[':topic/knowledge-points']];db=connection();basis=conf['basis_t']
kps=[r[0]for r in db.query('[:find (pull ?kp [* {:knowledge-point/question-generator [*]}]) :in $ [?kp ...] :where [?kp :knowledge-point/id _]]',[ids],H,'kps',basis)]
qids=sorted({q[':db/id']for k in kps for key in[':knowledge-point/questions',':knowledge-point/canonical-example']for q in(k.get(key,[])if isinstance(k.get(key,[]),list)else[k[key]])})
pattern='[* {:question/answer-fields [* {:answer-field/type [:db/ident]} {:answer-field/choices [* {:answer/type [:db/ident]}]} {:answer-field/correct [:db/id]}]}]';qs=[]
for offset in range(0,len(qids),60):qs +=[r[0]for r in db.query('[:find (pull ?q '+pattern+') :in $ [?q ...] :where [?q :question/id _]]',[qids[offset:offset+60]],H,'questions-'+str(offset),basis)]
acts=[r[0]for r in db.query('[:find (pull ?a [* {:activity/steps [*]}]) :in $ [?t ...] :where [?a :activity/scope ?t] [?a :activity/type :activity.type/lesson]]',[conf['topics']],H,'activities',basis)]
cids=sorted({s[':step/content'][':db/id']for a in acts for s in a.get(':activity/steps',[])if ':step/content'in s});contents=[r[0]for r in db.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[cids],H,'contents',basis)]
(H/'snapshot.json').write_text(json.dumps({'basis_t':basis,'topics':topics,'knowledge_points':kps,'questions':qs,'activities':acts,'contents':contents},default=str,indent=2)+'\n');print(len(kps),len(qs),len(acts),len(contents))
