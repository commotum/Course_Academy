"""Parent independently checks Cartesian density before any integral evaluation."""
import importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186129200;D=P.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_convert_eval_reader',P/'polar-evaluation-readback.py');g=module('root_convert_eval_generator',D.with_suffix('.py'));X,Y,R,T=p.p.X,p.p.Y,p.R,p.T
C=dict(instances=0,displayed_choices=0,cartesian_initial_checks=0,pointwise_polar_stages=0,angular_integrand_checks=0,angular_primitive_checks=0,scalar_stage_sides=0,boundary_equations=0,complete_authored_banks=0,source_banks=0,source_choices=0,source_refs=0,source_full_prose_sequences=0)
def density(raw):
 return p.p.scalar(raw.replace(r'\text{ }','').replace(r'\text{ d}',r'\mathrm{d}'))
def equal(a,b):return p.equal(a,b)
def delta(sol):
 raw=next(z for z in re.findall(r'\$\$(.*?)\$\$',sol,re.S) if z.strip().startswith(('Δ=',r'\Delta=')))
 raw=raw.replace(r'\leq',r'\le').replace(r'\,','').replace(r'\ ','');raw=re.sub(r'\s+','',raw).rstrip('.')
 m=re.search(r'0\\ler\\le(.*?),(.+?)\\le(?:\\theta|θ)\\le(.+?)(?:\\?\})$',raw);assert m,raw
 return density(m[1]),density(m[2]),density(m[3])
def d_integrand(raw):
 raw=re.sub(r'^(?:\\iint_D|\{∬\}_\{D\})\s*','',raw.strip());return density(re.split(r'\\,\\(?:mathrm|text)\{d\}A|\\,dA',raw)[0])
def check(rec):
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];meta=rec['generation'];name=meta['template']
 if '$f(x,y)=' in prompt:F=density(prompt.split('$f(x,y)=')[1].split('$')[0])
 else:F=d_integrand(re.search(r'\$((?:\\iint_D|\{∬\}_\{D\}).*?)\$',prompt,re.S)[1].rstrip(','))
 up,a,b=delta(sol);pol=s.refine(s.trigsimp(F.subs({X:R*s.cos(T),Y:R*s.sin(T)},simultaneous=True)*R),s.Q.nonnegative(R))
 h=s.simplify(p.integrate(pol,R,0,up));answer=s.simplify(p.integrate(h,T,a,b))
 if name in ('lower_sqrt','upper_ratio'):
  side=json.loads(Path(meta['plot']).with_suffix('.json').read_text())['parameters'];signed=s.Rational(str(side['R']))*side['sign'];assert equal(up,signed*s.sin(T))
  assert side['kind']=='shift' and equal(a,-s.pi/2 if signed<0 else 0) and equal(b,0 if signed<0 else s.pi/2)
 else:
  radius=s.Integer(re.search(r'radius \$(\d+)\$',prompt)[1]);assert equal(up,radius)
  compact=re.sub(r'\s+','',prompt)
  compact=compact.replace(r'\geq',r'\ge').replace(r'\leq',r'\le')
  aa,bb=(0,s.pi) if 'y\\ge0' in compact and 'x\\ge0' not in compact else (s.pi,3*s.pi/2) if 'x\\le0' in compact else (0,s.pi/2) if 'x\\ge0' in compact else (0,2*s.pi)
  assert equal(a,aa) and equal(b,bb),(name,prompt,a,b,aa,bb)
 field=q[':question/answer-fields'][0];values=[density(z[':answer/value']) for z in field[':answer-field/choices']];assert len(values)==5
 assert all(not equal(v,w) for i,v in enumerate(values) for w in values[i+1:]);assert [z[':answer/id'] for z,v in zip(field[':answer-field/choices'],values) if equal(v,answer)]==[field[':answer-field/correct'][1]];C['displayed_choices']+=5
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);rows=blocks[-1].split('\\\\');first=rows[0].split('&=')[0];assert equal(d_integrand(first),F);C['cartesian_initial_checks']+=1
 for row in rows:
  raw=row.split('&=')[1].strip()
  if r'\iint_\Delta ' in raw:
   prefix,body=raw.split(r'\iint_\Delta ');body=body.split(r'\,\mathrm')[0];f=(density(prefix) if prefix else 1)*density(body);assert equal(f,pol),(name,raw,f,pol);C['pointwise_polar_stages']+=1;continue
  value,nodes,primitives=p.read(raw);assert equal(value,answer),(name,raw,value,answer);C['scalar_stage_sides']+=1
  angular_nodes=[z for z in nodes if z[1]==T]
  if angular_nodes:
   normalized=p.normalize(raw);position=normalized.index(r'\int');prefix=normalized[:position];factor=density(prefix) if prefix else s.S.One
   assert len(angular_nodes)==1;f,var,lo,hi=angular_nodes[0];assert equal(factor*f,h) and equal(lo,a) and equal(hi,b),(name,'angular body',raw,factor*f,h);C['angular_integrand_checks']+=1
  for primitive,var,lo,hi in primitives:
   if var!=T:continue
   normalized=p.normalize(raw);position=normalized.index('[');prefix=normalized[:position];factor=density(prefix) if prefix else s.S.One
   assert equal(s.diff(factor*primitive,T),h) and equal(lo,a) and equal(hi,b),(name,'primitive',raw);C['angular_primitive_checks']+=1
 if name in ('lower_sqrt','upper_ratio'):
  boundary=blocks[-2].split('\\\\');assert len(boundary)==8
  sign=-1 if name=='lower_sqrt' else 1;diam=s.Rational(str(meta['parameters']['R']));target=R**2-sign*diam*R*s.sin(T)
  for i,row in enumerate(boundary):
   l,rhs=row.split('&=');left,right=density(l),density(rhs)
   if i==0:assert equal(left,X) and equal(right**2,sign*diam*Y-Y**2)
   elif i in (1,2):assert equal(left-right,X**2+Y**2-sign*diam*Y)
   else:assert equal(left-right,target)
   C['boundary_equations']+=1
  assert set(s.solve(target,R))=={s.S.Zero,up}
 if meta['bank_profile']=='authored':
  def V(f=pol,upper=up,lo=a,hi=b):return s.simplify(p.integrate(p.integrate(f,R,0,upper),T,lo,hi))
  if name=='odd_disk':expected=[answer,V(lo=0,hi=s.pi/2),V(lo=0,hi=s.pi),V(f=s.expand(pol).replace(s.sin(T),s.Abs(s.sin(T)))),V(lo=s.pi,hi=3*s.pi/2)]
  elif name=='quarter_difference':expected=[answer,V(f=F.subs(Y,0).subs(X,R*s.cos(T))*R),V(f=F.subs(Y,-Y).subs({X:R*s.cos(T),Y:R*s.sin(T)},simultaneous=True)*R),V(f=F.subs(X,0).subs(Y,R*s.sin(T))*R),V(lo=s.pi/2,hi=s.pi)]
  elif name=='upper_linear':expected=[answer,V(f=F.subs(Y,-Y).subs({X:R*s.cos(T),Y:R*s.sin(T)},simultaneous=True)*R),V(lo=-s.pi/2,hi=s.pi/2),V(f=pol/R),V(lo=0,hi=2*s.pi)]
  elif name in ('square_y','radial_square'):expected=[answer,V(f=pol/R),V(upper=up/2),V(hi=(a+b)/2),V(lo=b,hi=a)]
  elif name=='exponential':
   primitive=s.integrate(pol,R);expected=[answer,p.integrate(primitive.subs(R,up),T,a,b),2*answer,V(upper=s.sqrt(up)),V(lo=b,hi=a)]
  elif name=='rational_quarter':expected=[answer,V(hi=a+s.pi),V(hi=a+2*s.pi),h,V(lo=b,hi=a)]
  elif name=='lower_sqrt':expected=[answer,V(f=pol/R),5*answer,V(upper=up/2),V(lo=b,hi=a)]
  else:expected=[answer,V(f=pol/R),V(upper=up/2),V(f=pol*s.tan(T)),V(lo=b,hi=a)]
  assert all(sum(equal(v,w) for w in values)==1 for v in expected),(name,expected,values);C['complete_authored_banks']+=1
 C['instances']+=1;return q,answer
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
oracle={z['source_id']:s.sympify(z['computed']) for z in json.loads((P/'qa'/f'{K}-source-oracle.json').read_text())}
for case in json.loads((D/'source-cases.json').read_text()):
 q,answer=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['source_id']];nf=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
 oldvalues=[density(z[':answer/value']) for z in of[':answer-field/choices']];newvalues=[density(z[':answer/value']) for z in nf[':answer-field/choices']];assert all(sum(equal(v,w) for w in newvalues)==1 for v in oldvalues);C['source_banks']+=1;C['source_choices']+=5;assert equal(density(of[':answer-field/correct'][':answer/value']),answer);C['source_refs']+=1
 assert equal(answer,oracle[case['source_id']])
 def prose(text):
  text=re.sub(r'!\[\]\([^)]*\)','ASSET',text);text=re.sub(r'\$\$.*?\$\$|\$[^$]*\$','MATH',text,flags=re.S);text=re.sub(r'MATH[.,]','MATH',text);return re.sub(r'\s+',' ',text).strip()
 normal=q[':question/worked-solution'].split('\n\nThe integrand is defined for')[0]
 assert prose(normal)==prose(old[':question/worked-solution']),(case['source_id'],prose(normal),prose(old[':question/worked-solution']));C['source_full_prose_sequences']+=1
for rec in json.loads((D/'review.json').read_text())+json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(rec)
raw_expected_failures=[]
for case in json.loads((D/'source-cases.json').read_text()):
 rec=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile='observed_raw')
 try:check(rec)
 except AssertionError:
  assert case['source_id'] in ('q-161050','q-161053');raw_expected_failures.append(case['source_id'])
 else:assert case['source_id'] not in ('q-161050','q-161053')
assert sorted(raw_expected_failures)==['q-161050','q-161053'];C['public_raw_expected_false_stages']=raw_expected_failures
freeze=json.loads((D/'freeze.json').read_text())
for path,digest in freeze['files'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
C['frozen_hashes_verified']=len(freeze['files']);C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
