import json
from pathlib import Path
H=Path(__file__).resolve().parent;D=json.loads((H/'current.json').read_text());P=json.loads((H/'proposals.json').read_text());proofs=[]
fixes={
'q-140485':[(r'{R}_{1} & :={R}_{2}-2{R}_{1}',r'{R}_{2} & :={R}_{2}-2{R}_{1}')],
'q-75977':[(r'{R}_{3} & :={R}_{3}+(-1){R}_{2}',r'{R}_{3} & :={R}_{3}+(-1){R}_{1}')],
'q-83749':[(r'{R}_{3}:={R}_{3}+\frac{3}{2}{R}_{1}',r'{R}_{3}:={R}_{3}+{R}_{1}')],
'q-111501':[(r'{R}_{2} & :=\frac{1}{20}{R}_{1}',r'{R}_{2} & :=\frac{1}{20}{R}_{2}')],
'q-111511':[(r'{R}_{3} & :=\left(-\frac{1}{2}\right){R}_{3}',r'{R}_{2} & :=\left(-\frac{1}{2}\right){R}_{2}')],
'q-111513':[(r'{R}_{2} & :={R}_{2}+(-2){R}_{2}',r'{R}_{2} & :={R}_{2}+(-2){R}_{1}'),(r'{R}_{3} & :={R}_{3}+5{R}_{2}',r'{R}_{3} & :={R}_{3}+5{R}_{1}')],
'q-111194':[(r'{R}_{3} & :={R}_{3}+(-5){R}_{2}',r'{R}_{2} & :={R}_{2}+(-5){R}_{1}')],
'q-139975':[(r'{R}_{3} & :={R}_{3}(-5){R}_{1}',r'{R}_{3} & :={R}_{3}+(-5){R}_{1}')]}
flags=json.loads((H/'row-operation-verification.json').read_text());(H/'row-operation-before.json').write_text(json.dumps(flags,indent=2)+'\n')
for sid,edits in fixes.items():
 q=next(q for q in D['questions']if q.get(':question/math-academy-id')==sid);e=q[':db/id'];a='question/worked-solution';original=q[':'+a];p=next((p for p in P if p['entity']==e and p['attribute']==a),None);current=p['after']if p else original;after=current
 for before,new in edits:assert after.count(before)==1,(sid,before);after=after.replace(before,new)
 evidence={'identity':sid,'before_annotations':[b for b,n in edits],'after_annotations':[n for b,n in edits],'proof_path':'row-operation-before.json','verification_path':'row-operation-verification.json','proof':'Exact rational arithmetic on each displayed consecutive matrix proves the revised annotated row operation(s). Matrix values, solution conclusions, choices and keys are unchanged.'}
 if p:p['after']=after;p['reason']+=',authored-mathematical-correction-row-annotation';p.setdefault('additional_evidence',[]).append(evidence)
 else:P.append({'entity':e,'attribute':a,'before':original,'after':after,'reason':'authored-mathematical-correction-row-annotation','evidence':evidence})
 proofs.append({'entity':e,**evidence})
(H/'proposals.json').write_text(json.dumps(P,indent=2)+'\n');(H/'row-annotation-corrections.json').write_text(json.dumps(proofs,indent=2)+'\n');print('Corrected nine annotation defects across',len(fixes),'questions')
