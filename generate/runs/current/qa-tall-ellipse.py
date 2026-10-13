"""Root tall-ellipse complete polynomial/ordered teaching-stage/raster oracle."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186087840'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','p');g=load(D.with_suffix('.py'),'g');X,Y,V,Z=p.x,p.y,p.v,p.z
n=dict(records=0,choices=0,displayed_equalities=0,whole_method_banks=0,raster_checks=0,source_banks=0,source_values=0,source_solutions=0,source_designations=0,source_missing_designations=0,source_geometry_visually_inspected=22,generated_review_plots_visually_inspected=28)
def val(t):return s.expand(p.scalar(re.sub(r'\bb\b','z',re.sub(r'\ba\b','v',t.replace('&','')))))
def lhs(t):
 parts=t.strip().rstrip('.').split('=');assert len(parts)<=2
 if len(parts)==2:assert val(parts[1])==1
 return val(parts[0])
cache={}
def bluebox(path):
 if str(path) in cache:return cache[str(path)]
 im=Image.open(path).convert('RGB');pix=im.load();pts=[(x,y) for y in range(im.height) for x in range(im.width) if (lambda c:c[2]>c[0]*1.2 and c[2]>c[1]*1.03 and c[0]<130)(pix[x,y])];assert pts
 bb=(min(x for x,y in pts),max(x for x,y in pts),min(y for x,y in pts),max(y for x,y in pts));cache[str(path)]=(im.size,bb);return cache[str(path)]
def check(r):
 q=r['question'];gm=r['generation'];f=q[':question/answer-fields'][0];ref=re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]
 if ref.startswith('images/'):
  a,b=map(s.Rational,g.SOURCE_GEOMETRY[gm['source_id']])
 else:
  side=json.load(open(Path(ref).with_suffix('.json')));a,b=map(s.Rational,(side['a'],side['b']));assert side['equal_scale']
  size,bb=bluebox(ref);assert size==(480,400);bounds=side['bounds'];scale=min(.90*480/(bounds[1]-bounds[0]),.88*400/(bounds[3]-bounds[2]));assert abs((bb[1]-bb[0])-2*float(a)*scale)<4 and abs((bb[3]-bb[2])-2*float(b)*scale)<4,(bb,a,b,scale);n['raster_checks']+=1
 assert a<b and a>0;expected=X**2/a**2+Y**2/b**2;vals=[lhs(z[':answer/value']) for z in f[':answer-field/choices']];assert len(set(vals))==len(vals)
 good=[i for i,z in enumerate(vals) if s.expand(z-expected)==0];assert len(good)==1
 if ':answer-field/correct' in f:assert f[':answer-field/correct'][1]==f[':answer-field/choices'][good[0]][':answer/id']
 assert gm['evidence_only']==(gm['source_id'] is not None) and gm['eligible_for_learning']==(gm['source_id'] is None)
 if gm['bank_profile']=='authored':
  bank=[expected,X**2/b**2+Y**2/a**2,X**2/a+Y**2/b,X**2/b+Y**2/a,X**2/(2*a)+Y**2/(2*b)];assert set(vals)==set(bank);n['whole_method_banks']+=1
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];aa=val(re.search(r'\$a=(.*?)\$',sol)[1]);bb=val(re.search(r'\$b=(.*?)\$',sol)[1]);assert (aa,bb)==(a,b)
  for block in re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S):
   rows=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r' \\ ')
   for row in rows:assert s.expand(lhs(row).subs({V:a,Z:b})-expected)==0,row;n['displayed_equalities']+=1
   if len(rows)>1:assert len(rows)==(3 if a.q==b.q==1 else 4)
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}$=1$' in q[':question/problem']
 n['records']+=1;n['choices']+=len(vals)
frozen=json.load(open(D/'manifest.json'));assert all(hashlib.sha256(Path(q).read_bytes()).hexdigest()==h for q,h in frozen['files'].items());n['frozen_worker_hashes']=len(frozen['files'])
old={q[':question/math-academy-id']:q for q in json.load(open(D/'source.json'))['record'][':knowledge-point/questions']}
for c in json.load(open(D/'source-cases.json')):
 r=g.generate(c['level'],parameters=c['parameters'],profile=c['bank_profile']);check(r);q=r['question'];o=old[c['source_id']];assert q[':question/problem']==o[':question/problem']
 for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in o)
 if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];n['source_solutions']+=1
 of=o[':question/answer-fields'][0];gf=q[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in of[':answer-field/choices'])==sorted(z[':answer/value'] for z in gf[':answer-field/choices']);n['source_banks']+=1;n['source_values']+=len(gf[':answer-field/choices']);assert (':answer-field/correct' in of)==(':answer-field/correct' in gf)
 if ':answer-field/correct' in of:assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in gf[':answer-field/choices'] if z[':answer/id']==gf[':answer-field/correct'][1]);n['source_designations']+=1
 else:n['source_missing_designations']+=1
review=json.load(open(D/'review.json'))
for key,records in review.items():
 if isinstance(records,list):
  for r in records:check(r.get('record',r))
for level in ('easy','moderate','hard'):
 seen=set()
 for seed in range(18):
  r=g.generate(level,seed+9100);check(r);seen.add(r['generation']['mathematical_fingerprint']);z=g.generate(level,seed+7100,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['bank_profile']);assert r['question'][':question/id']==z['question'][':question/id']
 assert len(seen)>=10;n[level+'_meaningful_sample']=len(seen)
 values=list(map(s.Rational,range(1,13))) if level=='easy' else [s.Rational(i,2) for i in range(2,21)] if level=='moderate' else sorted(set(s.Rational(i,j) for j in (3,4) for i in range(j,8*j+1) if s.Rational(i,j).q==j))
 tasks=[(a,b) for a in values for b in values if a<b and b/a<=(3 if level=='hard' else 4) and (level!='moderate' or a.q==2 or b.q==2)];n[level+'_finite_mathematical_tasks']=len(tasks)
 assert set(g.domain(level))==set(tasks)
 for params in [{'a':'2/997','b':'3/997'},{'a':'7/3','b':'10/3'}] if level!='hard' else [{'a':'2/997','b':'3/997'},{'a':'1','b':'2'}]:
  try:g.generate(level,parameters=params)
  except ValueError:pass
  else:raise AssertionError(('reduced workload guard',level,params))
(R/'qa/17592186087840-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
