"""Root parses actual direct-circulation prompts and every printed stage."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186133926'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
g=load(D.with_suffix('.py'),'g');p=load(R/'ode-scalar-parser.py','p');T=p.t
n=dict(records=0,choices=0,formal_derivatives=0,field_components=0,dot_stages=0,primitives=0,individual_endpoint_terms=0,source_prompts=0,source_solutions=0,source_choices=0,source_keys=0);seen=set()
def same(a,b):return s.simplify(s.trigsimp(a-b))==0
def scalar(t):return p.scalar(t.replace('[','(').replace(']',')'))
def vector(t,formal=False):
 parts=re.split(r'\\,([ijk])',t);assert len(parts)==7 and not parts[-1].strip();out=[]
 for i in range(3):
  assert parts[2*i+1]=='ijk'[i];term=parts[2*i].lstrip('+')
  if formal:
   prefix=r'\frac{\mathrm d}{\mathrm dt}';assert term.startswith(prefix);term=term[len(prefix):];out.append(s.diff(scalar(term),T));n['formal_derivatives']+=1
  else:out.append(scalar(term))
 return s.Matrix(out)
def integral(t):
 m=re.match(r'\\int_\{(.*?)\}\^\{(.*?)\}(.*)',t);assert m;return scalar(m[1]),scalar(m[2]),m[3].removesuffix(r'\,\mathrm dt')
def normal(r):
 if not r['generation']['eligible_for_learning']:return
 q=r['question'];identity=q[':question/id']
 if identity in seen:return
 prompt=q[':question/problem'];F=vector(re.search(r'F\(x,y,z\)=(.*?)\$',prompt)[1]);curve=vector(re.search(r'r\(t\)=(.*?)\$',prompt)[1]);lo,hi=map(scalar,re.search(r't\\in \[(.*?),(.*?)\)',prompt).groups());assert hi>lo and all(same(v.subs(T,lo),v.subs(T,hi)) for v in curve)
 dr=curve.diff(T);fr=F.subs(dict(zip((p.x,p.y,p.z),curve)),simultaneous=True);dot=s.trigsimp(fr.dot(dr));answer=s.simplify(s.integrate(s.expand_trig(dot),(T,lo,hi)))
 sol=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);rows=[[x.split('& =',1)[1].strip() for x in b.split(r'\\')] for b in blocks];assert list(map(len,rows))==[2,2,4,5]
 coords=re.search(r'\$\$\s*x=(.*?)\.\s*\$\$',sol,re.S)[1].split(',\\quad ');assert len(coords)==3
 for axis,part,v in zip('xyz',coords,curve):assert same(scalar(part.split('=',1)[1] if part.startswith(axis+'=') else part),v)
 for row,want in zip(rows[0],(F,fr)):
  assert all(same(a,b) for a,b in zip(vector(row),want));n['field_components']+=3
 assert all(same(a,b) for a,b in zip(vector(rows[1][0],True),dr));assert all(same(a,b) for a,b in zip(vector(rows[1][1]),dr))
 m=re.fullmatch(r'\\left\((.*)\\right\)\\cdot\\left\((.*)\\right\)',rows[2][0]);assert m
 assert all(same(a,b) for a,b in zip(vector(m[1]),fr)) and all(same(a,b) for a,b in zip(vector(m[2]),dr))
 for row in rows[2][1:]:assert same(scalar(row),dot);n['dot_stages']+=1
 l,h,body=integral(rows[3][0]);assert l==lo and h==hi and body==r'F(r(t))\cdot r^{\prime}(t)'
 l,h,body=integral(rows[3][1]);assert l==lo and h==hi and same(scalar(body),dot)
 m=re.fullmatch(r'\\left\[(.*?)\\right\]_\{(.*?)\}\^\{(.*?)\}',rows[3][2]);assert m;primitive=scalar(m[1]);assert same(s.diff(primitive,T),dot) and scalar(m[2])==lo and scalar(m[3])==hi;n['primitives']+=1
 ep=re.fullmatch(r'\[(.*)\]-\[(.*)\]',rows[3][3]);assert ep
 terms=sorted(s.Add.make_args(s.expand(primitive)),key=s.default_sort_key)
 for displayed,endpoint in ((ep[1],hi),(ep[2],lo)):
  values=re.findall(r'\\left\((.*?)\\right\)',displayed);assert len(values)==len(terms)
  for val,term in zip(values,terms):assert same(scalar(val),term.subs(T,endpoint));n['individual_endpoint_terms']+=1
 assert same(scalar(rows[3][3]),answer) and same(scalar(rows[3][4]),answer)
 f=q[':question/answer-fields'][0];values=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5 and all(not same(a,b) for i,a in enumerate(values) for b in values[:i]) and sum(same(v,answer) for v in values)==1
 assert same(scalar(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])),answer)
 kind=r['generation']['template']
 if kind in ('xy_rotation','xy_rotation_z','yz_rotation'):expected=[answer,-answer,answer/2,0,2*answer]
 elif kind=='xy_symmetric':
  a,b=[s.integrate(fr[j]*dr[j],(T,lo,hi)) for j in (0,1)];expected=[answer,a-b,-a+b,a,b]
 elif kind=='polynomial_sine':
  px=s.integrate(fr[0]*dr[0],T);pz=s.integrate(fr[2]*dr[2],T);end=px.subs(T,hi)+px.subs(T,lo);peak=2*pz.subs(T,s.Rational(1,2));expected=[answer,-end,end,-peak,peak]
 else:
  a=s.Poly(curve[0],T).nth(2);b=s.Poly(curve[1],T).nth(3)
  omit_y=F[0].subs(p.y,0).subs(p.x,curve[0]);omit_cubic=F[0].subs({p.x:curve[0],p.y:curve[1]-b*T**3},simultaneous=True)
  expected=[answer,-answer,s.integrate(omit_y*dr[0],(T,lo,hi)),s.integrate(omit_cubic*dr[0],(T,lo,hi)),s.integrate(fr[0]*(dr[0]+a),(T,lo,hi))]
 assert all(sum(same(v,s.sympify(e)) for e in expected)==1 for v in values)
 seen.add(identity);n['records']+=1;n['choices']+=5
for case in json.loads((D/'source-cases.json').read_text()):
 r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=r['question'];o=g.ORIGINALS[case['source_id']];assert q[':question/problem']==o[':question/problem'];assert (':question/difficulty' in q)==(':question/difficulty' in o) and (':question/worked-solution' in q)==(':question/worked-solution' in o)
 if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];n['source_solutions']+=1
 f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
 if ':answer-field/correct' in f:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];n['source_keys']+=1
 assert not r['generation']['eligible_for_learning'];n['source_prompts']+=1;n['source_choices']+=5
for item in json.loads((D/'native-input.json').read_text()):normal(item['record'])
for level in ('easy','moderate','hard'):
 for seed in range(18):normal(g.generate(level,seed))
out={'status':'passed','independent_readback':n,'scope':'Closed-curve direct work only; no curl, normals or Stokes calculation. Source omissions and two intermediate teaching errors remain in public ineligible raw profiles.'};(R/'qa/17592186133926-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
