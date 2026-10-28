from pathlib import Path
import sys,json
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
p=Publisher.from_environment(source=':agent/codex');status=p.client.status();basis=status['basis'];topic=17592186048123
scope=p.client.query('''[:find (pull ?t [* {[:topic/knowledge-points :limit nil] [:db/id :knowledge-point/id :knowledge-point/title {:knowledge-point/question-generator [*]} {[:knowledge-point/questions :limit nil] [:db/id]} {:knowledge-point/canonical-example [:db/id]}]}]) :in $ ?t :where [?t :topic/id _]]''',[topic],H/'capture','topic',basis)
t=jsonable(scope[0][0]);(H/'topic.json').write_text(json.dumps(t,indent=2)+'\n')
ids=sorted({q[':db/id'] for k in t[':topic/knowledge-points'] for q in k.get(':knowledge-point/questions',[])+([k[':knowledge-point/canonical-example']] if k.get(':knowledge-point/canonical-example') else [])})
query='''[:find (pull ?q [* {:question/difficulty [:db/ident]}
 {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/ident]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/ident]}]} {:answer-field/correct [* {:answer/type [:db/ident]}]}]}
 {[:knowledge-point/_questions :limit nil] [:db/id :knowledge-point/id :knowledge-point/title]}
 {[:knowledge-point/_canonical-example :limit nil] [:db/id :knowledge-point/id :knowledge-point/title]}
 {[:task-item/_content :limit nil] [* {:task-item/status [:db/ident]} {[:task-item/responses :limit nil] [* {:answer/type [:db/ident]}]}]}]) :in $ [?q ...] :where [?q :question/id _]]'''
rows=[]
for start in range(0,len(ids),20):rows+=p.client.query(query,[ids[start:start+20]],H/'capture',f'questions-{start}',basis)
qs=sorted([jsonable(q) for [q] in rows],key=lambda q:q[':db/id'])
(H/'questions.json').write_text(json.dumps(qs,indent=2)+'\n')
(H/'capture.json').write_text(json.dumps({'basis':basis,'lineage':status['lineage'],'source':':agent/codex','topic':topic,'question_ids':ids,'question_count':len(qs),'database_writes':0},indent=2)+'\n')
print('Captured',len(qs),'questions at',basis)
for kp in t[':topic/knowledge-points']:print('KP',kp[':db/id'],kp[':knowledge-point/title'],'practice',len(kp.get(':knowledge-point/questions',[])),'generator',kp.get(':knowledge-point/question-generator'))
for q in qs:
 types=[f[':answer-field/type'][':db/ident'] for f in q.get(':question/answer-fields',[])]
 print(q[':db/id'],q.get(':question/math-academy-id'),types,'canonical',bool(q.get(':knowledge-point/_canonical-example')),'used',len(q.get(':task-item/_content',[])))
 if any(x.endswith('/radio') for x in types):print('STEM',q[':question/problem']);print('OPTIONS',[(a[':db/id'],a[':answer/value']) for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]);print('KEY',[f.get(':answer-field/correct',{}).get(':answer/value') for f in q[':question/answer-fields']])
