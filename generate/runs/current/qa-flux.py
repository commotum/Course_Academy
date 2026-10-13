"""Parent derives flux from printed vectors, not generator mathematics metadata."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
R=Path(__file__).resolve().parent;S=R.parents[2]/'generate/scratch'
x,y,z,u,v,a,b,c=s.symbols('x y z u v a b c',real=True)
LOC={str(t):t for t in (x,y,z,u,v,a,b,c)};LOC.update(sin=s.sin,cos=s.cos,exp=s.exp)
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def math(t):
 t=t.strip().rstrip('.,').replace('\u2061','').replace('⁡','').replace('−','-')
 for old,new in [(r'\left',''),(r'\right',''),(r'\,',''),(r'\cdot','*'),(r'\operatorname{sin}','sin'),(r'\operatorname{cos}','cos'),(r'\sin','sin'),(r'\cos','cos'),(r'\end{aligned}','')]:t=t.replace(old,new)
 t=re.sub(r'(?:\{e\}|e)\^\{([^{}]+)\}',r'(exp(\1))',t)
 def group(pos):
  assert t[pos]=='{';end=pos+1;depth=1
  while depth:
   if t[end]=='{':depth+=1
   if t[end]=='}':depth-=1
   end+=1
  return t[pos+1:end-1],end
 while r'\frac' in t:
  i=t.rfind(r'\frac');num,j=group(i+5);den,end=group(j);t=t[:i]+'(('+num+')/('+den+'))'+t[end:]
 t=re.sub(r'(sin|cos)\^\{(\d+)\}\{\(([^()]*)\)\}',r'(\1(\3))**\2',t)
 t=re.sub(r'(sin|cos)\^(\d+)\s*v',r'(\1(v))**\2',t)
 t=re.sub(r'(sin|cos)\s*v',r'(\1(v))',t)
 t=t.replace('{','(').replace('}',')').replace('\\','')
 return parse_expr(t,local_dict=LOC,transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
def eq(a,b):return s.simplify(s.trigsimp(a-b))==0
def vectors(t):
 t=t.replace(r'\left\langle','⟨').replace(r'\right\rangle','⟩')
 return re.findall('⟨([^⟨⟩]+)⟩',t)
def vector(t):return s.Matrix([math(e) for e in t.replace(r'\,','').split(',')])
def determinant(t):
 rows=t.split(r'\\');assert len(rows)==2
 i,j=[math(q) for q in rows[0].split('&')];k,l=[math(q) for q in rows[1].split('&')]
 return s.latex(i*l-j*k)
def objects(prompt):
 ff,rr=[vector(t) for t in vectors(prompt)[:2]];du=rr.diff(u);dv=rr.diff(v)
 n=s.Matrix([du[1]*dv[2]-du[2]*dv[1],du[2]*dv[0]-du[0]*dv[2],du[0]*dv[1]-du[1]*dv[0]])
 pull=ff.subs(dict(zip((x,y,z),rr)),simultaneous=True);g=s.expand(sum(pull[i]*n[i] for i in range(3)))
 return ff,rr,du,dv,n,pull,g
def check(r,kp):
 q=r['question'];ff,rr,du,dv,n,pull,g=objects(q[':question/problem']);f=q[':question/answer-fields'][0]
 if kp==17592186198378:
  if 'what is the value of' in q[':question/problem']:
   part=q[':question/problem'].split(r'\iint_D',1)[1].split(r'\,\mathrm{d}A')[0]
   poly=math(part);letters=[t for t in (a,b,c) if t in poly.free_symbols]
   sols=s.solve(s.Poly(s.expand(poly-g),u,v,s.exp(v),s.exp(-v)).coeffs(),letters,dict=True)
   assert len(sols)==1,(part,g,sols);correct=sum(sols[0][t] for t in letters)
  else:correct=g
 else:
  token=r'-?(?:\\frac\{\d+\}\{\d+\}|\d+)'
  bounds=re.findall('('+token+r')\s*\\le\s*(u|v)\s*\\le\s*('+token+')',q[':question/problem'])
  assert len(bounds)==2,(q[':question/problem'],bounds)
  domain={variable:(math(lo),math(hi)) for lo,variable,hi in bounds}
  correct=sum(coeff*(domain['u'][1]**(i+1)-domain['u'][0]**(i+1))*(domain['v'][1]**(j+1)-domain['v'][0]**(j+1))/((i+1)*(j+1)) for (i,j),coeff in s.Poly(g,u,v).terms())
 for ans in f[':answer-field/choices']:assert eq(math(ans[':answer/value']),correct)==(ans[':answer/id']==f[':answer-field/correct'][1])
 # Parse every evaluated vector and scalar dot-product row from the displayed solution.
 solution=q[':question/worked-solution'];allowed=(ff,rr,du,dv,n,pull)
 for t in vectors(solution):
  if 'partial' in t or '∂' in t:continue
  if r'\begin{vmatrix}' in t:t=re.sub(r'\\begin\{vmatrix\}(.*?)\\end\{vmatrix\}',lambda m:'('+determinant(m[1])+')',t)
  elif '|' in t:continue # Legacy determinant vectors also checked by worker.
  value=vector(t);assert any(all(eq(i,j) for i,j in zip(value,expected)) for expected in allowed),(t,value,allowed)
 part=solution.split('we calculate the dot product')[1].split('$$')[1]
 for row in part.split(' & =')[1:]:
  if vectors(row):continue
  scalar=row.split(r'\\')[0].strip().replace(r'\end{aligned}','').strip().rstrip('.')
  assert eq(math(scalar),g),(kp,scalar,g)
 return ff,rr
counts={}
for kp in (17592186198378,17592186198380):
 gmod=module('parent_flux_'+str(kp),S/f'{kp}.py');raw=json.loads((R/'sources'/f'{kp}.json').read_text())['record'];qs={q[':question/math-academy-id']:q for q in raw[':knowledge-point/questions']};byuuid={q[':question/id']:q for q in raw[':knowledge-point/questions']};count=dict(source_banks=0,source_values=0,source_designations=0,displayed_instances=0)
 for case in json.loads((S/str(kp)/'source-cases.json').read_text()):
  old=qs.get(case['source_id']) or byuuid[case['source_id']];level=case.get('level') or old[':question/difficulty'][':db/ident'].split('/')[-1]
  r=gmod.generate(level,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);ff,rr=check(r,kp);of,orr,*_=objects(old[':question/problem']);assert all(eq(i,j) for i,j in zip(ff,of));assert all(eq(i,j) for i,j in zip(rr,orr)),(kp,case['source_id'],rr,orr)
  f=r['question'][':question/answer-fields'][0];oldf=old[':question/answer-fields'][0];bank=[math(t[':answer/value']) for t in f[':answer-field/choices']]
  for ans in oldf[':answer-field/choices']:
   found=[i for i,t in enumerate(bank) if eq(t,math(ans[':answer/value']))];assert len(found)==1;bank.pop(found[0]);count['source_values']+=1
  assert not bank
  chosen=next(t for t in f[':answer-field/choices'] if t[':answer/id']==f[':answer-field/correct'][1]);assert eq(math(chosen[':answer/value']),math(oldf[':answer-field/correct'][':answer/value']));count['source_designations']+=1;count['source_banks']+=1
 for level in ('easy','moderate','hard'):
  for seed in range(20):check(gmod.generate(level,seed),kp);count['displayed_instances']+=1
 counts[str(kp)]=count
(R/'qa/flux-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
