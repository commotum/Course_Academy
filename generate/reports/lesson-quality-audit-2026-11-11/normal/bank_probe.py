"""Bank-only largest-coordinate strategy on the entire captured radio subgroup."""
import json,sys,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from math_tools import tuple_tex,key_value
from generator_publish import normalized_question,enum
K=json.loads((H/'17592186092385/kp.json').read_text());cases=[];rows=[]
for q in K[':knowledge-point/questions']:
 fields=q.get(':question/answer-fields',[])
 if len(fields)!=1 or enum(fields[0][':answer-field/type'])!=':answer-field.type/radio':continue
 f=fields[0]
 # Infer the varying coordinate from choices alone, before inspecting prompt/key.
 points=[tuple_tex(a[':answer/value']) for a in f[':answer-field/choices']]
 varying=[i for i in (0,1) if len({v[i] for v in points})>1];assert len(varying)==1
 coordinate=varying[0];axis=('x','y')[coordinate]
 values=[(point[coordinate],a) for point,a in zip(points,f[':answer-field/choices'])]
 maximum=max(value for value,_ in values);selected=[a for value,a in values if value==maximum];assert len(selected)==1
 chosen=selected[0]
 # Only now inspect the key to measure strategy success.
 keyed=f[':answer-field/correct'][':answer/id'];success=chosen[':answer/id']==keyed
 rows.append(dict(entity=q[':db/id'],imported=bool(q.get(':question/math-academy-id')),ma_id=q.get(':question/math-academy-id'),axis=axis,choices=[a[':answer/value'] for a in f[':answer-field/choices']],strategy_selection=chosen[':answer/value'],key=key_value(f),success=success,retired=q.get(':question/retired',False)))
 record=dict(knowledge_point=dict(db_id=17592186092385,id=K[':knowledge-point/id'],title=K[':knowledge-point/title']),question=normalized_question(q));rf=record['question'][':question/answer-fields'][0];rf[':answer-field/correct']=[':answer/id',rf[':answer-field/correct']]
 checks=[dict(field_index=0,submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==chosen[':answer/id'] else 'rejected',control='equivalent' if a[':answer/id']==chosen[':answer/id'] else 'wrong',purpose='Entire offered bank: largest-coordinate strategy chosen without reading key; every alternative is mathematically distinct') for a in rf[':answer-field/choices']]
 cases.append(dict(label=str(q[':db/id']),record=record,checks=checks))
assert len(rows)==8 and all(row['success'] for row in rows)
(H/'bank-probe-input.json').write_text(json.dumps(cases,indent=2)+'\n')
subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'bank-probe-input.json'),str(H/'bank-probe-native-report.json')],check=True)
(H/'bank-probe.json').write_text(json.dumps(dict(status='confirmed-current-finite-subgroup-cue',basis=14220,subgroup='Every complete one-field ordered-pair radio in captured KP17592186092385 inventory',selection_rule='Infer which coordinate varies across the offered points; choose its unique numerical maximum',allowed_inputs='Answer choices only; no prompt, key, solution, function evaluation or catalog of correct outputs',coverage=len(rows),correct=sum(row['success'] for row in rows),removed_work=['differentiate','evaluate tangent slope','take negative reciprocal','construct normal','calculate intersection'],scope_limit='Demonstrated on the entire current8-question radio subgroup. No claim about future/random populations, blank questions or ordinary current generator output.',questions=rows),indent=2)+'\n')
print('Confirmed bounded radio bank cue on all8 current cases;8 accepted and32 rejected through native grader')
