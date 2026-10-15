"""Read-only audit of the current source pool; no source repairs are applied."""
import importlib.util,json,re,sys,copy
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
x,y,u,w=g.x,g.y,g.u,g.v

def math(t):
 t=t.replace('\\\\','\\').replace(r'\u2061','').replace('⁡','')
 t=re.sub(r'\{ln\}\^\{2\}\s*([124])',r'(\\ln(\1))^{2}',t)
 t=re.sub(r'\{cos\}\^\{2\}\((.*?)\)',r'(\\cos(\1))^{2}',t)
 return v.math(t)

def context(q):
 prompt=q[':question/problem']
 if r'\iint_D ' in prompt:
  r={'question':q,'generation':{'template':'radical' if r'\frac{x}{\sqrt' in prompt else 'normal','parameters':{'R':100}}}
  return v.read_context(r)
 F=math(prompt.split('{∬}_{D}')[1].split(r'\,dxdy')[0])
 conditions=prompt.split('where $D=')[1].split(')')[1]
 conditions=conditions.removeprefix(r'\,:\,')
 conditions=conditions.removesuffix(r'\}.$') if conditions.endswith(r'\}.$') else conditions.removesuffix('}.$')
 parts=conditions.split(r'\,');coords=[];bounds=[]
 for part in parts:
  if part.startswith('|'):
   VV,dd=part.split(r'\le ');coords.append(math(VV.strip('|')));hi=math(dd);bounds.append((-hi,hi))
  else:
   aa,UU,bb=part.split(r'\le ');coords.append(math(UU));bounds.append((math(aa),math(bb)))
 U,V=coords;(a,b),(c,d)=bounds
 inverse=s.solve([U-u,V-w],[x,y],dict=True)
 total=0
 for inv in inverse:
  X,Y=inv[x],inv[y];j=s.simplify(s.det(s.Matrix([X,Y]).jacobian([u,w])))
  # All captured rectangles have positive u,v where radicals occur. For the
  # noninjective xy,y/x map both disjoint branches must be integrated.
  if s.simplify(j*j)==4-w*w:absj=s.sqrt(4-w*w)
  elif not j.free_symbols:absj=abs(j)
  else:absj=s.refine(s.Abs(j),s.Q.positive(w)&s.Q.positive(u))
  weighted=s.simplify(F.subs(inv,simultaneous=True)*absj)
  total+=s.integrate(weighted,(u,a,b),(w,c,d))
 return dict(F=F,U=U,V=V,a=a,b=b,c=c,d=d,I=s.simplify(total),branches=len(inverse))

def task(q):
 z=context(q);constraints=[]
 for coord,lo,hi in ((z['U'],z['a'],z['b']),(z['V'],z['c'],z['d'])):
  coord=s.expand(coord)
  if coord.is_polynomial(x,y):
   leading=s.Poly(coord,x,y).coeffs()[0]
   coord=s.simplify(coord/leading);lo,hi=lo/leading,hi/leading
   if leading<0:lo,hi=hi,lo
  constraints.append([str(s.simplify(coord)),str(s.simplify(lo)),str(s.simplify(hi))])
 return g.digest([str(s.simplify(z['F'])),sorted(constraints)])

ISSUES={'q-160911':'Two outer differentials are dv rather than du in the worked solution.',
'q-38309':'Step 1 loses the negative lower endpoint; Step 2 and the integral use the correct interval.',
'q-160915':'The domain has two disjoint branches; the key -12/pi integrates only one. The actual integral is -24/pi. One solution row also changes the upper endpoint from 4 to 2.'}
def audit(kp):
 rows=[]
 for q in kp[':knowledge-point/questions']:
  if ':question/math-academy-id' not in q:continue
  z=context(q);f=q[':question/answer-fields'][0];values=[math(a[':answer/value']) for a in f[':answer-field/choices']];correct=math(f[':answer-field/correct'][':answer/value']);matching=[i for i,val in enumerate(values) if s.simplify(val-z['I'])==0]
  name=q[':question/math-academy-id'];valid=s.simplify(correct-z['I'])==0
  assert valid or name=='q-160915',(name,correct,z['I'])
  assert all(s.simplify(a-b)!=0 for i,a in enumerate(values) for b in values[:i])
  rows.append({'source_id':name,'question_id':str(q[':question/id']),'db_id':q[':db/id'],'difficulty':'moderate','field_type':'radio','choice_count':len(values),'complete_bank':[str(z) for z in values],'correct_value':str(correct),'independent_integral':str(z['I']),'key_correct':valid,'matching_choices':matching,'branches':z.get('branches',1),'task':task(q),'usable':valid and name not in ISSUES,'issue':ISSUES.get(name),'plots':'none','prompt':q[':question/problem'],'worked_solution':q[':question/worked-solution']})
 return rows
