"""Parent checks actual prompt density, regions, complete banks and all stages."""
import importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186129199;D=P.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_setup_reader',P/'polar-setup-readback.py');g=module('root_centered_setup_generator',D.with_suffix('.py'));X,Y,R,T=p.X,p.Y,p.R,p.T
GEOMETRY=json.loads((P/'qa/polar-source-regions.json').read_text())['regions'][str(K)]
C=dict(instances=0,displayed_choices=0,substitution_stages=0,full_integral_stages=0,domain_checks=0,source_banks=0,source_choices=0,source_refs=0,source_missing_refs=0,source_raw_exact_solutions=0,source_brace_only_repairs=0,source_asset_hashes=0,authored_complete_banks=0)
def integrand(prompt):
 m=re.search(r'\$(?:\\iint_D\s*|\{∬\}_\{D\}|∬_\(D\))(.*?)\$',prompt,re.S);assert m,prompt
 return p.scalar(re.split(r'\\,\\(?:text|mathrm)\{d\}A|dA',m[1])[0])
def domain(solution):
 raw=next(z for z in re.findall(r'\$\$(.*?)\$\$',solution,re.S) if z.strip().startswith(('Δ=',r'\Delta=')))
 raw=raw.replace(r'\leq',r'\le').replace(r'\,','').replace(r'\ ','');raw=re.sub(r'\s+','',raw)
 m=re.search(r'0\\ler\\le(.*?),(.+?)\\le(?:\\theta|θ)\\le(.+?)(?:\\?\}|\}\.)$',raw.rstrip('.'));assert m,raw
 return p.scalar(m[1]),p.scalar(m[2]),p.scalar(m[3])
def check(rec):
 q=rec['question'];F=integrand(q[':question/problem']);density=F.subs({X:R*s.cos(T),Y:R*s.sin(T)},simultaneous=True)*R
 radius,a,b=domain(q[':question/worked-solution']);C['domain_checks']+=1
 params=rec['generation']['parameters'];assert p.equal(radius,s.sqrt(params['radius_squared']))
 if rec['generation']['source_id']:
  geo=GEOMETRY[rec['generation']['source_id']];sa,sb=[s.sympify(v)*s.pi for v in geo['angular_pi']];rotation=params['rotation']*s.pi/2
  assert p.sector_equal(a,b,sa+rotation,sb+rotation)
 else:assert p.sector_equal(a,b,params['rotation']*s.pi/2,params['rotation']*s.pi/2+s.pi/2)
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];signatures=[];valid=[];read=[]
 for z in choices:
  bounds,f=p.integral(z[':answer/value']);aa,bb,lo,hi=bounds;signatures.append(p.shape(bounds,f));read.append((bounds,f));valid.append(p.equal(lo,0) and p.equal(hi,radius) and p.sector_equal(aa,bb,a,b) and p.equal(f,density));C['displayed_choices']+=1
 assert len(signatures)==len(set(signatures))==5 and sum(valid)==1
 assert [z[':answer/id'] for z,v in zip(choices,valid) if v]==[field[':answer-field/correct'][1]]
 body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)[1];rows=body.split('\\\\');assert len(rows)>=2
 for row in rows:
  rhs=row.split('&',1)[1].strip().removeprefix('=').strip()
  if r'\int' in rhs:
   bounds,f=p.integral(rhs);assert p.equal(f,density) and all(p.equal(x,y) for x,y in zip(bounds,(a,b,0,radius)));C['full_integral_stages']+=1
  else:
   rhs=re.sub(r'^\s*(?:\{∬\}_\{Δ\}|\\iint_\\Delta)\s*','',rhs);rhs=re.split(r'\\text\{d\}|\\mathrm\{d\}',rhs)[0].replace(r'\text{ }','').rstrip().removesuffix(r'\,')
   assert p.equal(p.scalar(rhs),density),(rhs,density);C['substitution_stages']+=1
 if rec['generation']['template'].startswith('root_'):
  assert len(rows)==4 and 'sqrt' in rows[0] and r'\sqrt{r' in rows[1] and r'\sqrt{r' not in rows[2]
  assert r'\sqrt{r^2}=r' in q[':question/worked-solution']
  expected=[((a,b,0,radius),density),((a,b,0,radius),density/R),((a,b,0,radius),density*R),((a,a+(b-a)/2,0,radius),density),((a,b,0,2*radius),density)]
  assert all(sum(all(p.equal(x,y) for x,y in zip(bounds,other)) and p.equal(f,ff) for other,ff in read)==1 for bounds,f in expected);C['authored_complete_banks']+=1
 plot=rec['generation']['plot'];assert Path(plot['prompt']).exists()
 if plot['sidecar']:
  meta=json.loads(Path(plot['sidecar']).read_text());assert meta['instance']==dict(radius_squared=params['radius_squared'],alpha_pi=str(s.simplify(a/s.pi)),beta_pi=str(s.simplify(b/s.pi))) and meta['arc_points']==401
 C['instances']+=1;return q
originals={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 old=originals[case['source_id']];q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));nf=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
 assert sorted(z[':answer/value'] for z in nf[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);C['source_banks']+=1;C['source_choices']+=5
 def without_assets(text):return re.sub(r'!\[\]\([^)]+\)','ASSET',text)
 assert without_assets(q[':question/problem'])==without_assets(old[':question/problem'])
 srcpath=Path('/media/jake/SSD/EDB/math')/re.search(r'!\[\]\(([^)]+)\)',old[':question/problem'])[1];newpath=Path(re.search(r'!\[\]\(([^)]+)\)',q[':question/problem'])[1]);assert srcpath.read_bytes()==newpath.read_bytes();C['source_asset_hashes']+=1
 if of.get(':answer-field/correct'):
  newvalue=next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]);assert newvalue==of[':answer-field/correct'][':answer/value'];C['source_refs']+=1
 else:C['source_missing_refs']+=1
 if old.get(':question/worked-solution'):
  if q[':question/worked-solution']==old[':question/worked-solution']:C['source_raw_exact_solutions']+=1
  else:
   raw=re.sub(r'\\([{}])',r'\1',q[':question/worked-solution']);assert raw==re.sub(r'\\([{}])',r'\1',old[':question/worked-solution']);C['source_brace_only_repairs']+=1
for rec in json.loads((D/'review.json').read_text())+json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(rec)
freeze=json.loads((D/'freeze-hashes.json').read_text())
for path,digest in freeze['files'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
C['frozen_hashes_verified']=len(freeze['files']);C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
