import json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH,validate_math_structure
D=json.loads((H/'current.json').read_text());Q={q[':db/id']:q for q in D['questions']};out=[]
ids=[17592186124797,17592186278206,17592186278207,17592186278209,17592186378787,17592186378815]
for e in ids:
 q=Q[e];before=q[':question/worked-solution'];after=re.sub(r'\{\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}',lambda m:r'\begin{cases}'+m[1]+r'\end{cases}',before)
 def setfix(m):
  whole=m[0];edge=2 if whole.startswith('$$')else 1;inner=whole[edge:-edge]
  if inner.strip().startswith('{(x,y)'):
   inner=inner.replace('{(x,y)',r'\{(x,y)',1);position=inner.rfind('}');inner=inner[:position]+r'\}'+inner[position+1:];inner=inner.replace(r'\in {R}^{2}',r'\in \mathbb{R}^{2}')
  return whole[:edge]+inner+whole[-edge:]
 after=MATH.sub(setfix,after)
 proof='Necessary and sufficient real-domain conditions independently obtained from logarithm argument>0, real radicand≥0, and nonzero denominator; original source MathML confirms fenced condition rows and visible domain set.'
 if e==17592186378815:after=after.replace(r'-1<x+\sqrt{y}<1',r'-1\le x+\sqrt{y}\le1');proof+=' Arccos includes both endpoints; (1,0) and (-1,0) are valid, proving the source strict intermediate inequality is wrong.'
 validate_math_structure(after);out.append({'entity':e,'attribute':'question/worked-solution','before':before,'after':after,'reason':'Recover source cases/visible set braces and domain font'+('; correct independently disproved strict arccos endpoint inequality'if e==17592186378815 else''),'evidence':{'basis':9837,'identity':q.get(':question/math-academy-id'),'independent_proof':proof},'confidence':'high'})
for e in[17592186176191,17592186176192,17592186176194,17592186176400]:
 q=Q[e];before=q[':question/problem'];after=re.sub(r'_{3,}',lambda _:r'\underline{\phantom{xxxx}}',before)
 if e==17592186176194:after=after.replace('$f(x, z)$','$f(x, y)$')
 validate_math_structure(after);out.append({'entity':e,'attribute':'question/problem','before':before,'after':after,'reason':'Recover source visual blank without treating underscores as TeX subscripts'+('; keep free cylinder parameters consistent with displayed f(x,y)'if e==17592186176194 else''),'evidence':{'basis':9837,'identity':q.get(':question/math-academy-id'),'source':'3596/Source/3596.html','independent_proof':'This is a radio response selecting the missing vector component, not an embedded math input. The unchanged parameter pair and remaining components determine its role.'},'confidence':'high'})
q=Q[17592186504931];before=q[':question/worked-solution'];after=before.replace(r'\neqe',r'\neq e');validate_math_structure(after);out.append({'entity':q[':db/id'],'attribute':'question/worked-solution','before':before,'after':after,'reason':'Separate inequality operator from following vector label e','evidence':{'basis':9837,'proof':'Adjacent prose and statement say b=e is false, because directions are opposite; valid operator is b≠e.'},'confidence':'high'})
(H/'structural-proposals.json').write_text(json.dumps(out,indent=2)+'\n');print(len(out))
