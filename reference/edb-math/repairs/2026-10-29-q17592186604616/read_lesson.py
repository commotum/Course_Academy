import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection
read=lambda p:json.loads(p.read_text());db=connection();basis=read(H/'basis.json')['basis_t'];topic=next(r[0]for r in read(H/'topic-lesson.json')if r[0][':db/id']==17592186050463);ids=[k[':db/id']for k in topic[':topic/knowledge-points']]
kps=[r[0]for r in db.query('[:find (pull ?kp [* {:knowledge-point/question-generator [*]}]) :in $ [?kp ...] :where [?kp :knowledge-point/id _]]',[ids],H,'all-kps',basis)]
qids=sorted({q[':db/id']for k in kps for key in [':knowledge-point/questions',':knowledge-point/canonical-example']for q in(k.get(key,[])if isinstance(k.get(key,[]),list)else[k[key]])})
pattern='[* {:question/answer-fields [* {:answer-field/type [:db/ident]} {:answer-field/choices [* {:answer/type [:db/ident]}]} {:answer-field/correct [:db/id]}]}]'
qs=[]
for offset in range(0,len(qids),60):qs +=[r[0]for r in db.query('[:find (pull ?q '+pattern+') :in $ [?q ...] :where [?q :question/id _]]',[qids[offset:offset+60]],H,'lesson-questions-'+str(offset),basis)]
acts=[r[0]for r in db.query('[:find (pull ?a [* {:activity/steps [*]}]) :in $ ?t :where [?a :activity/scope ?t] [?a :activity/type :activity.type/lesson]]',[topic[':db/id']],H,'lesson-activities',basis)]
cids=sorted({s[':step/content'][':db/id']for a in acts for s in a.get(':activity/steps',[])if ':step/content'in s})
contents=[r[0]for r in db.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[cids],H,'lesson-contents',basis)]
snapshot={'basis_t':basis,'topic':topic,'knowledge_points':kps,'questions':qs,'activities':acts,'contents':contents}
(H/'lesson.json').write_text(json.dumps(snapshot,indent=2,default=str)+'\n');print('Read',len(kps),'KPs,',len(qs),'questions/examples,',len(acts),'activities,',len(cids),'step contents')
for k in kps:print(k[':db/id'],k[':knowledge-point/title'],'questions',len(k.get(':knowledge-point/questions',[])),'generator',k.get(':knowledge-point/question-generator'))
for c in contents:print('CONTENT',c[':db/id'],[key for key in c if key not in [':db/id',':knowledge-point/questions']])
