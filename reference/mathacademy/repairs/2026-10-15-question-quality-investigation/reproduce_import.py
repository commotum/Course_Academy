"""Check current import reconciliation against the five existing duplicates."""
import copy,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts/question_capture'))
from edn import loads
from math_content import build_math_content
out=[]
for path in sorted(H.glob('175*.edn')):
 q=loads(path.read_text());fields=q[':question/answer-fields']
 if len(fields)!=2:continue
 keyed=next(f for f in fields if f.get(':answer-field/correct'));point=copy.deepcopy(q[':knowledge-point/_questions'][0]);point.pop(':topic/_knowledge-points',None)
 incoming={'math_academy_id':q[':question/math-academy-id'],'knowledge_point_id':str(point[':knowledge-point/id']),'knowledge_point':point[':knowledge-point/title'],'topic_id':999,'problem':q[':question/problem'],'worked_solution':q[':question/worked-solution'],'difficulty':q[':question/difficulty'][':db/ident'].split('/')[-1], 'answer_fields':[{'key':keyed[':answer-field/key'],'type':keyed[':answer-field/type'][':db/ident'].split('/')[-1],'correct_value':keyed[':answer-field/correct'][':answer/value'],'choices':[{'type':a[':answer/type'][':db/ident'].split('/')[-1],'value':a[':answer/value']} for a in keyed[':answer-field/choices']]}]}
 forms,report=build_math_content({'task_type':'review','topic_id':999,'questions':[incoming],'canonical_examples':[]},{999:{':topic/math-academy-id':999,':topic/knowledge-points':[point]}},{q[':question/math-academy-id']:q})
 detached=[f for f in forms if isinstance(f,list) and str(f[0])==':db/retract' and str(f[2])==':question/answer-fields']
 out.append({'question':q[':db/id'],'source_id':q[':question/math-academy-id'],'field_retractions':detached,'duplicate_removed_by_reimport':bool(detached),'planned_forms':len(forms)})
(H/'import-reproduction.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps(out))
