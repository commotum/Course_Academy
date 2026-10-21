"""Reconcile current source banks with the frozen mathematical templates."""
import json,copy
from pathlib import Path
import replenish as p
v=p.v;g=p.g
kp=p.loads((p.OUT/'initial/kp.edn').read_text())[0][0]
rows=[];native=[]
for q in kp[':knowledge-point/questions']:
 mid=q[':question/math-academy-id'];r=g.generate('easy',profile=mid,parameters={'scale':1,'offsets':[0]*(len(g.BASE[mid][0])-1)})
 assert p.matrix_from_prompt(q[':question/problem'])==v.sp.Matrix(g.BASE[mid])
 f=q[':question/answer-fields'][0];gf=r['question'][':question/answer-fields'][0]
 values=[v.signature(g.parse_vector(a[':answer/value'])) for a in f[':answer-field/choices']]
 replay=[v.signature(g.parse_vector(a[':answer/value'])) for a in gf[':answer-field/choices']]
 assert sorted(map(str,values))==sorted(map(str,replay)),mid
 correct=f.get(':answer-field/correct')
 if correct:
  assert v.signature(g.parse_vector(correct[':answer/value']))==v.signature(g.parse_vector(next(a[':answer/value'] for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1])))
  r['question']=p.normalize(q);v.check_record(r);native.append(r)
 rows.append({'source_id':mid,'choices_matched':len(values),'complete_bank_matched':True,'correct_designation_matched':bool(correct),'current_worked_solution_independently_validated':bool(correct)})
p.save(p.OUT/'initial/current-source-bank-replay.json',{'passed':True,'basis':json.loads((p.OUT/'initial/kp.json').read_text()).get('basis',2701),'complete_banks_matched':len(rows),'answer_values_matched':sum(r['choices_matched'] for r in rows),'correct_designations_matched':len(native),'current_changes':'Canonical matrix/system formatting repairs; q-42040 now has easy difficulty, a correct answer and a worked solution. All existing vector banks retain the same mathematical values. Original frozen source retained unchanged.','rows':rows})
p.native(native,p.OUT/'initial/current-source-grading')
inv,raw=p.inventory(p.OUT/'initial/inventory.json');counts=p.validated_counts(kp,raw);p.save(p.OUT/'initial/validated-counts.json',counts)
print(json.dumps({'inventory_basis':inv['basis'],'counts':counts},indent=2))
