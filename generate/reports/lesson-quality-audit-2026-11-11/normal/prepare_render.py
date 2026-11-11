import sys,json
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from generator_publish import normalized_question
records=json.loads((H/'render-input.json').read_text());extra=[(17592186092384,17592186317210),(17592186092384,17592186710692),(17592186092385,17592186710717),(17592186092385,17592186297306)];mapping=[]
for kp,eid in extra:
 K=json.loads((H/str(kp)/'kp.json').read_text());q=next(q for q in K[':knowledge-point/questions'] if q[':db/id']==eid);q=normalized_question(q)
 for f in q[':question/answer-fields']:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct']]
 mapping.append(dict(index=len(records),kp=kp,entity=eid));records.append(dict(knowledge_point=dict(db_id=kp,id=K[':knowledge-point/id'],title=K[':knowledge-point/title']),question=q))
(H/'render-final-input.json').write_text(json.dumps(records,indent=2)+'\n');(H/'render-stored-mapping.json').write_text(json.dumps(mapping,indent=2)+'\n');print(len(records),'records for actual UI')
