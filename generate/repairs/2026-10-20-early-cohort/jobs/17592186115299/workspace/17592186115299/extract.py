"""One-time full-component template extraction from immutable basis-1356 capture."""
import json,re
from pathlib import Path
D=Path(__file__).parent
src=json.loads((D/'source.json').read_text())
ops={
'q-32242':[['add',1,0,2],['add',2,0,5],['add',2,1,-9]],
'q-42061':[['add',1,0,4]],
'q-131719':[['add',1,0,-2],['add',2,0,3]],
'q-131723':[['add',1,0,3]],
'q-131724':[['add',1,0,3],['add',2,0,-2]],
'q-74635':[['add',1,0,'1/2']],
'q-74637':[['swap',0,1],['add',1,0,-2],['add',2,0,1],['add',2,1,1]],
'q-131718':[['add',1,0,2]],
'q-74643':[['swap',0,1],['add',1,0,-3],['add',2,0,-1],['add',2,1,'-1/2']],
'q-131720':[['scale',0,'1/2'],['add',1,0,-3]],
'q-131721':[['add',1,0,-3],['add',2,0,2]],
'q-131722':[['scale',0,'1/3'],['add',1,0,2],['add',2,0,-4],['scale',1,-1]],
'q-42020':[['add',1,0,-3],['add',2,0,2],['add',2,1,1]],
'q-74634':[['add',1,0,-1],['add',2,0,'-1/2'],['add',2,1,'1/2']]}
# Save component masks, never a source-ID branch returning a literal source question.
result={}
for q in src['record'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id']; problem=q[':question/problem']; solution=q[':question/worked-solution']
 # Store complete mathematical components as slots. All are recomputed by the generator.
 slots=[]
 def slot(m):
  name='slot_'+str(len(slots));slots.append(m.group());return '{{'+name+'}}'
 pm=re.sub(r'\$\$.*?\$\$',slot,problem,flags=re.S)
 sm=re.sub(r'\$\$.*?\$\$|(?<!\$)\$(?!\$).*?\$(?!\$)',slot,solution,flags=re.S)
 f=q[':question/answer-fields'][0]
 result[sid]={'problem_mask':pm,'solution_mask':sm,'math_components':slots,'operations':ops[sid],
  'bank':[a[':answer/value'] for a in f[':answer-field/choices']], 'raw_correct':f[':answer-field/correct'][':answer/value']}
(D/'templates.json').write_text(json.dumps(result,indent=2)+'\n')
print(len(result),'complete masks extracted')
