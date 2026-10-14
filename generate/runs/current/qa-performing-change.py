"""Root reader of supplied two-dimensional maps, complete integrals and stages."""
import importlib.util,json,re,hashlib,sys,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186198361;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','change_parent_scalar');x,y=p.x,p.y;u,v=s.symbols('u v',positive=True);p.locals_.update(u=u,v=v)
def math(raw):
 raw=re.sub(r'\\text\{[^}]*\}','',raw).replace('\xa0','').replace(r'\quad','').replace(r'\qquad','').replace(r'\:','')
 raw=re.sub(r'\\frac([0-9])([0-9])',r'\\frac{\1}{\2}',raw)
 raw=re.sub(r'\|([^|]+)\|',r'Abs(\1)',raw)
 return p.scalar(raw.replace('[','(').replace(']',')'))
def eq(a,b):return s.simplify(s.expand_log(a-b,force=True))==0
def group(text,pos):
 assert text[pos]=='{';start=pos+1;depth=1;pos+=1
 while depth:depth+=(text[pos]=='{')-(text[pos]=='}');pos+=1
 return text[start:pos-1],pos
def integral(raw):
 raw=raw.strip().rstrip('.,').replace(r'{\int }',r'\int').replace(r'\text{d}','d')
 first=raw.index(r'\int');coefficient=math(raw[:first] or '1');pos=first;bounds=[]
 while raw[pos:].startswith(r'\int'):
  pos+=4;assert raw[pos]=='_';lo,pos=group(raw,pos+1);assert raw[pos]=='^';hi,pos=group(raw,pos+1);bounds.append((math(lo),math(hi)))
 tail=raw[pos:];matches=list(re.finditer(r'd([uv])',tail));assert len(matches)==len(bounds)==2
 variables=[{'u':u,'v':v}[m[1]] for m in matches];fn=coefficient*math(tail[:matches[0].start()]);limits=dict(zip(reversed(variables),bounds))
 return s.integrate(fn,(variables[0],*limits[variables[0]]),(variables[1],*limits[variables[1]])),fn,limits
C=dict(records=0,components=0,jacobian_entries=0,inverse_definitions=0,substitution_stages=0,complete_choices=0,whole_banks=0,primitive_derivatives=0,individual_endpoints=0,operative_checks=0)
def check(rec):
 q=rec['question'];prompt=q[':question/problem'];name=rec['generation']['template'];sol=q[':question/worked-solution'];assert not re.search(r'(?<!\\)\{\([xu],\s*[yv]\)',prompt+sol)
 U,V=[math(re.search(r'\b'+z+r'\s*=\s*(.*?)\$',prompt,re.S)[1].rstrip(',')) for z in 'uv'];J=s.Matrix([U,V]).jacobian((x,y));det=J.det();C['components']+=2
 F=math(re.search(r'(?:\{∬\}_\{D\}|∬_\(D\))(.*?)dx',prompt,re.S)[1])
 nonlinear=J.has(x,y)
 if nonlinear:
  assert eq(U,y/x**2) and eq(V,x*y)
  inverse={x:(v/u)**s.Rational(1,3),y:u**s.Rational(1,3)*v**s.Rational(2,3)}
  b=re.search(r'(\d*)\{x\}\^\{2\}\\le y\\le (\d+)\{x\}\^\{2\}',prompt);c=re.search(r'(\d+)\\le xy\\le (\d+)',prompt)
  bounds={u:(s.Integer(b[1] or 1),s.Integer(b[2])),v:tuple(map(s.Integer,c.groups()))}
  density=s.simplify(F.subs(inverse,simultaneous=True)/(3*u))
 else:
  inverse=s.solve([U-u,V-v],(x,y));cs=re.findall(r'(-?\d+)\s*\\le\s*(.*?)\s*\\le\s*(-?\d+)',prompt,re.S);assert len(cs)==2
  bounds={var:(s.Integer(lo),s.Integer(hi)) for var,(lo,expression,hi),expected in zip((u,v),cs,(U,V)) if eq(math(expression),expected)};assert len(bounds)==2
  density=s.simplify(F.subs(inverse,simultaneous=True)/abs(det))
 answer=s.integrate(density,(u,*bounds[u]),(v,*bounds[v]));field=q[':question/answer-fields'][0]
 values=[math(a[':answer/value']) if nonlinear else integral(a[':answer/value'])[0] for a in field[':answer-field/choices']];assert len(values)==5 and all(not eq(a,b) for a,b in itertools.combinations(values,2))
 hits=[a[':answer/id'] for a,val in zip(field[':answer-field/choices'],values) if eq(val,answer)];assert hits==[field[':answer-field/correct'][1]]
 if nonlinear:wrong=[v**(2 if s.degree(F,x)==2 else 1)/u,-density,1/(3*u),density*v]
 elif name=='difference':wrong=[2*density,4*density,-density,(u*u-v*v)/2]
 elif name=='triangular_quadratic':
  bx=(u+v)/2;wrong=[2*density,4*density,(2*bx*v+bx*bx)/2,inverse[x]*v]
 elif name=='product':wrong=[2*density,4*density,(v-u)**2,(v+u)**2]
 elif name=='exponential':wrong=[2*s.exp(3*u-2*v),s.exp(2*u-v),s.exp(u+v),s.exp(3*u-2*v)/2]
 elif name=='sum_square':wrong=[6*u*u,s.Rational(3,2)*(u+v)**2,s.Rational(3,4)*(u+v)**2,s.Rational(9,2)*u*u]
 else:raise AssertionError(name)
 wanted=[answer]+[s.integrate(f,(u,*bounds[u]),(v,*bounds[v])) for f in wrong];assert all(sum(eq(z,w) for w in wanted)==1 for z in values);C['whole_banks']+=1;C['complete_choices']+=5
 assert sol.count('**Step')==4
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S)
 section=sol.split('**Step 2**')[1].split('**Step 3**')[0]
 arrays=re.findall(r'\\begin\{(?:aligned|vmatrix)\}(.*?)\\end\{(?:aligned|vmatrix)\}',section,re.S)
 numeric=[a for a in arrays if '∂' not in a and r'\frac{\partial' not in a];assert numeric
 matrix=s.Matrix([[math(cell) for cell in row.split('&')] for row in numeric[-1].split(r'\\')]);assert matrix==J;C['jacobian_entries']+=4
 tail=section.rsplit(r'\end{aligned}|',1)[-1] if name!='difference' else section.rsplit(r'\end{vmatrix}',1)[-1]
 assert eq(math(tail.split('=')[-1].replace(r'\end{aligned}','').replace('$$','')),det)
 section3=sol.split('**Step 3**')[1].split('**Step 4**')[0];raw=section3.split('$$')[1].rsplit('=',1)[1];assert eq(math(raw),-1/(3*u) if nonlinear else 1/det)
 for var in (u,v):
  m=re.search(r'(-?\d+)\\le '+str(var)+r'\\le (-?\d+)',sol);assert tuple(map(s.Integer,m.groups()))==bounds[var]
 last=blocks[-1];chain=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',last,re.S)[1];rows=chain.split(r'\\')
 if not nonlinear:
  expectedcount={'difference':3,'triangular_quadratic':3,'product':4,'exponential':4,'sum_square':3}[name];assert len(rows)==expectedcount
  for row in rows[:-1]:
   raw=row.split('=',1)[1].replace('&','').strip();raw=re.sub(r'^(?:\{∬\}_\{Δ\}|\\iint_Δ)','',raw);raw=re.sub(r'\\(?:text\{d\}|,)?[duv].*$','',raw) if False else raw
   raw=raw.split(r'\text{d}u')[0].split(r'\,du')[0].split(r'\,dv')[0]
   raw=raw.replace(r'|\frac{∂(x,y)}{∂(u,v)}|',s.latex(1/abs(det))).replace(r'\left|\frac{∂(x,y)}{∂(u,v)}\right|',s.latex(1/abs(det)))
   assert eq(math(raw),density),(name,raw,density);C['substitution_stages']+=1
  val,fn,lim=integral(rows[-1].split('=',1)[1].replace('&',''));assert eq(val,answer) and eq(fn,density) and lim==bounds
  if name=='triangular_quadratic':assert r'{u}^{2}-2uv+{v}^{2}' in rows[1]
  if name=='exponential':assert '3u-5v+2v-u' in rows[0] and '2u-3v' in rows[1]
  if name=='product':assert r'(\frac{v-u}{2})(\frac{v+u}{2})' in rows[0]
  C['operative_checks']+=1
  if name in ('difference','triangular_quadratic','product','exponential'):
   xy=re.search(r'x=(.*?),(?:\\,|\\qquad)\s*y=(.*?)\.\s*\$\$',sol,re.S)
   assert xy and eq(math(xy[1]),inverse[x]) and eq(math(xy[2]),inverse[y]);C['inverse_definitions']+=2
 else:
  assert len(rows)==10
  val,fn,lim=integral(rows[2].split('=',1)[1].replace('&',''));assert eq(val,answer) and eq(fn,density) and lim==bounds,(val,answer,fn,density,lim,bounds)
  power=s.degree(F,x);a,b=bounds[u];c,d=bounds[v]
  prim=re.search(r'\[(.*?)\\,\{\|\}',rows[4])[1];assert eq(s.diff(math(prim),u).subs(u,s.Symbol('positive_u',positive=True)),1/s.Symbol('positive_u',positive=True));C['primitive_derivatives']+=1
  operands=re.search(r'(?:v|\{v\})(?:\^\{2\})?\((.*?)\)\\,dv',rows[5])[1].split('-');assert len(operands)==2 and eq(math(operands[0]),s.log(b)) and eq(math(operands[1]),s.log(a));C['individual_endpoints']+=2
  prim=re.search(r'\\cdot (.*?)\\,\{\|\}',rows[7])[1];assert eq(s.diff(math(prim),v),v**power);C['primitive_derivatives']+=1
  numbers=re.search(r'\\cdot \((\d+)-(\d+)\)',rows[8]);assert tuple(map(int,numbers.groups()))==(int(d**(power+1)),int(c**(power+1)));C['individual_endpoints']+=2
  coefficient=math(rows[8].split('=',1)[1].split(r'\cdot')[0].replace('&',''));assert eq(coefficient,(s.log(b)-s.log(a))/(3*(power+1)))
  assert eq(math(rows[-1].split('=',1)[1].replace('&','')),answer);C['operative_checks']+=1
 C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'root_change_gen');old={q[':db/id']:q for q in json.load(open(R/f'sources/{K}.json'))['record'][':knowledge-point/questions']};source=dict(prompts=0,solutions=0,values=0,refs=0,missing_refs=0,missing_ratings=0)
 for case in json.load(open(D/'source-cases.json')):
  q=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'];o=old[case['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (key in q)==(key in o)
  assert q[':question/problem']==o[':question/problem'];source['prompts']+=1
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];source['solutions']+=1
  source['missing_ratings']+=int(':question/difficulty' not in o)
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);source['values']+=len(of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];source['refs']+=1
   else:source['missing_refs']+=1
 records=json.load(open(R/f'qa/{K}-sampled.json'))
 for family,level in g.LEVELS.items():
  if family!='sum_product_evidence':records.append(g.generate(level,seed=673,template=family))
 for rec in records:check(rec)
 for case in json.load(open(D/'source-cases.json')):
  if case['template']=='sum_product_evidence':continue
  if case['template']=='product':continue # Original zero-valued duplicate bank is preserved only as evidence.
  check(g.generate(case['level'],template=case['template'],parameters=case['parameters']))
 out=dict(status='passed',source=source,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
