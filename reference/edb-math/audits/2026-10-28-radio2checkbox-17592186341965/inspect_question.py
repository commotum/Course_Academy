from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
p=Publisher.from_environment(source=':agent/codex');status=p.client.status();basis=status['basis'];eid=17592186341965
query='''[:find (pull ?q [* {:question/difficulty [:db/ident]}
 {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/ident]}
 {[:answer-field/choices :limit nil] [* {:answer/type [:db/ident]}]}
 {:answer-field/correct [* {:answer/type [:db/ident]}]}]}
 {[:knowledge-point/_questions :limit nil] [:db/id :knowledge-point/id :knowledge-point/title {:knowledge-point/question-generator [*]}]}
 {[:knowledge-point/_canonical-example :limit nil] [:db/id :knowledge-point/id :knowledge-point/title]}
 {[:task-item/_content :limit nil] [* {:task-item/status [:db/ident]} {[:task-item/responses :limit nil] [* {:answer/type [:db/ident]}]}]}])
 :in $ ?q :where [?q :question/id _]]'''
rows=p.client.query(query,[eid],H,'question',basis);q=jsonable(rows[0][0]);topics=[]
for kp in q.get(':knowledge-point/_questions',[])+q.get(':knowledge-point/_canonical-example',[]):
 topics+=p.client.query('[:find (pull ?t [:db/id :topic/id :topic/title]) :in $ ?kp :where [?t :topic/knowledge-points ?kp]]',[kp[':db/id']],H,f"topic-{kp[':db/id']}",basis)
uses=p.client.query('''[:find ?field ?answer (pull ?item [* {:task-item/status [:db/ident]} {[:task-item/responses :limit nil] [*]}])
 :in $ ?q :where [?q :question/answer-fields ?field] [?field :answer-field/choices ?answer] [?item :task-item/responses ?answer]]''',[eid],H,'response-uses',basis)
out={'basis':basis,'lineage':status['lineage'],'read_source':':agent/codex','question':q,'topics':jsonable(topics),'response_uses':jsonable(uses),'database_writes':0}
(H/'capture.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
