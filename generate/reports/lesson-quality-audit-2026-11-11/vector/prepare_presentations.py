import copy,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import normalized_question
suspects=[(17592186096652,17592186735008),(17592186096652,17592186292807),(17592186096653,17592186734994),(17592186096701,17592186735416),(17592186096701,17592186735423),(17592186235285,17592186735570),(17592186235285,17592186735575)]
rows=[];mapping=[]
for kp,qid in suspects:
 k=json.loads((H/str(kp)/'inventory/kp.json').read_text());q=next(q for q in k[':knowledge-point/questions'] if q[':db/id']==qid);clean=normalized_question(q)
 for f in clean[':question/answer-fields']:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct']]
 rows.append(dict(knowledge_point={'db_id':kp,'id':k[':knowledge-point/id'],'title':k[':knowledge-point/title']},question=clean,generation={'template':'stored-audit','stored_entity':qid}));mapping.append(dict(index=len(rows)-1,kp=kp,entity=qid))
(H/'stored-suspects.json').write_text(json.dumps(rows,indent=2)+'\n');(H/'stored-suspects-map.json').write_text(json.dumps(mapping,indent=2)+'\n')
