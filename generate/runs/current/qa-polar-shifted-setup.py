"""Root derives tangent-circle polar geometry from actual Cartesian prompt."""
import importlib.util,re,json,hashlib
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186129275;D=P.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_shifted_setup_reader',P/'polar-setup-readback.py');g=module('root_shifted_setup_generator',D.with_suffix('.py'));X,Y,R,T=p.X,p.Y,p.R,p.T
C=dict(instances=0,displayed_choices=0,cartesian_circle_checks=0,circle_substitution_equations=0,pointwise_density_stages=0,domain_checks=0,source_banks=0,source_values=0,source_refs=0,source_missing_refs=0,source_full_prose=0,plot_geometry_checks=0)
def mathblocks(text):return re.findall(r'\$\$.*?\$\$|\$[^$]*\$',text,re.S)
def check(rec):
 q=rec['question'];prompt=q[':question/problem'];solution=q[':question/worked-solution'];pieces=[z for z in mathblocks(prompt) if 'D' in z]
 region=pieces[0].strip('$').replace(r'\leq',r'\le');assert '\\{' in region
 body=region.split('y)',1)[1].replace(r'\,','').lstrip(':, ');m=re.search(r'(.*?)\\le\s*(.*)',body);assert m,(region,body)
 right=m[2].split(',',1)[0].split(r'\}',1)[0]
 lhs=p.scalar(m[1]);rhs=p.scalar(right);cart=s.expand(lhs-rhs);poly=s.Poly(cart,X,Y);assert poly.coeff_monomial(X**2)==poly.coeff_monomial(Y**2)==1 and poly.coeff_monomial(X*Y)==0 and poly.coeff_monomial(1)==0
 cx=-poly.coeff_monomial(X)/2;cy=-poly.coeff_monomial(Y)/2;radius=s.sqrt(cx**2+cy**2);assert (cx==0)!=(cy==0);C['cartesian_circle_checks']+=1
 up=2*(cx*s.cos(T)+cy*s.sin(T));compact=re.sub(r'\s+','',region)
 if cx:
  a,b=(-s.pi/2,s.pi/2) if cx>0 else (s.pi/2,3*s.pi/2)
  if 'y\\ge0' in compact:a,b=(0,s.pi/2) if cx>0 else (s.pi/2,s.pi)
  if 'y\\le0' in compact:a,b=(-s.pi/2,0) if cx>0 else (s.pi,3*s.pi/2)
 else:
  a,b=(0,s.pi) if cy>0 else (s.pi,2*s.pi)
  if 'x\\ge0' in compact:a,b=(0,s.pi/2) if cy>0 else (3*s.pi/2,2*s.pi)
  if 'x\\le0' in compact:a,b=(s.pi/2,s.pi) if cy>0 else (s.pi,3*s.pi/2)
 raw=pieces[1].strip('$').strip();raw=re.sub(r'^(?:\\iint_D|\{∬\}_\{D\}|∬_\(D\))\s*','',raw);F=p.scalar(re.split(r'\\,?\\?(?:mathrm|text)\{d\}A|\\,dA|dA',raw)[0].strip())
 density=F.subs({X:R*s.cos(T),Y:R*s.sin(T)},simultaneous=True)*R
 f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];shapes=[];valid=[]
 for z in choices:
  bounds,h=p.integral(z[':answer/value']);aa,bb,lo,hi=bounds;shapes.append(p.shape(bounds,h));valid.append(p.equal(h,density) and p.equal(lo,0) and p.equal(hi,up) and p.sector_equal(aa,bb,a,b));C['displayed_choices']+=1
 assert len(shapes)==len(set(shapes))==5 and sum(valid)==1;assert [z[':answer/id'] for z,v in zip(choices,valid) if v]==[f[':answer-field/correct'][1]]
 ds=next(z.strip('$').strip() for z in mathblocks(solution) if z.strip('$').strip().startswith(('Δ=',r'\Delta=')));ds=re.sub(r'\s+','',ds.replace(r'\leq',r'\le').replace(r'\,',''))
 m=re.search(r'0\\ler\\le(.*?),(.+?)\\le(?:\\theta|θ)\\le(.+?)(?:\\?\})\.?$',ds);assert m,ds
 assert p.equal(p.scalar(m[1]),up) and p.sector_equal(p.scalar(m[2]),p.scalar(m[3]),a,b);C['domain_checks']+=1
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S);assert len(blocks)==3
 first=blocks[-1].split('\\\\')[0].split('&',1)[0].strip();first=re.sub(r'^(?:\\iint_D|\{∬\}_\{D\})\s*','',first);first=re.split(r'\\,?\\?(?:mathrm|text)\{d\}A|\\,dA|dA',first)[0]
 assert p.equal(p.scalar(first),F)
 expected=cart.subs({X:R*s.cos(T),Y:R*s.sin(T)},simultaneous=True)
 for row in blocks[1].split('\\\\'):
  lhs,rhs=row.replace('&','').split('=',1);left,right=p.scalar(lhs),p.scalar(rhs);actual=left-right
  if actual.has(X,Y):assert p.equal(actual,cart)
  else:assert p.equal(actual,expected)
  C['circle_substitution_equations']+=1
 for index,row in enumerate(blocks[-1].split('\\\\')):
  rhs=row.split('&',1)[1].strip().removeprefix('=').strip()
  if r'\int' in rhs:
   bounds,h=p.integral(rhs.rstrip('.'));aa,bb,lo,hi=bounds;assert p.equal(h,density) and p.equal(lo,0) and p.equal(hi,up) and p.sector_equal(aa,bb,a,b)
  else:
   rhs=re.sub(r'^(?:\\iint_\\Delta|\{∬\}_\{Δ\})\s*','',rhs);rhs=re.split(r'\\,?\\?(?:mathrm|text)\{d\}r|\\,dr',rhs)[0];rhs=rhs.replace(r'\text{ }','').removesuffix(r'\,');actual=p.scalar(rhs)
   if actual.has(X,Y):
    assert index==0;actual=actual.subs({X:R*s.cos(T),Y:R*s.sin(T)},simultaneous=True)
   assert p.equal(actual,density),(rec['generation']['template'],rhs,density)
  C['pointwise_density_stages']+=1
 paths=re.findall(r'!\[\]\(([^)]+)\)',solution);assert len(paths)==3
 for path in paths:
  asset=Path(path);assert asset.exists()
  if asset.with_suffix('.json').exists():
   meta=json.loads(asset.with_suffix('.json').read_text());geo=meta['geometry'];assert abs(geo['a']-float(radius))<1e-12 and geo['axis']==('x' if cx else 'y') and geo['sign']==(1 if cx+cy>0 else -1)
   assert p.equal(p.scalar(geo['upper_tex']),up) and p.equal(p.scalar(geo['square_tex']),radius**2) and p.sector_equal(*[p.scalar(z) for z in geo['bounds_tex']],a,b)
   C['plot_geometry_checks']+=1
 C['instances']+=1;return q
source={q[':db/id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=source[case['source_id']];nf=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
 assert sorted(z[':answer/value'] for z in nf[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);C['source_banks']+=1;C['source_values']+=5
 if of.get(':answer-field/correct'):assert next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];C['source_refs']+=1
 else:C['source_missing_refs']+=1
 if old.get(':question/worked-solution'):
  def prose(text):
   text=re.sub(r'!\[\]\([^)]*\)','ASSET',text);text=re.sub(r'\$\$.*?\$\$|\$[^$]*\$','MATH',text,flags=re.S);return re.sub(r'\s+',' ',text).strip()
  assert prose(q[':question/worked-solution'])==prose(old[':question/worked-solution']);C['source_full_prose']+=1
for rec in json.loads((D/'review.json').read_text())+json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(rec.get('record',rec))
freeze=json.loads((D/'freeze.json').read_text())
for path,digest in freeze['files'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
C['frozen_hashes_verified']=len(freeze['files']);C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
