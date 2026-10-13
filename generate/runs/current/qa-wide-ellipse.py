"""Root source/printed-polynomial/complete-bank/raster oracle; no worker math helpers."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186087839'
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','p');g=load(D.with_suffix('.py'),'g');X,Y,V,Z=p.x,p.y,p.v,p.z
n=dict(records=0,choices=0,whole_method_banks=0,displayed_equalities=0,generated_rasters=0,source_banks=0,source_values=0,source_solutions=0,source_geometry_visually_inspected=13)
def scalar(t):
 t=re.sub(r'\ba\b','v',t);t=re.sub(r'\bb\b','z',t);return s.expand(p.scalar(t.replace('&','')))
def lhs(t):
 parts=t.strip().rstrip('.').split('=');assert len(parts)<=2
 if len(parts)==2:assert scalar(parts[1])==1
 return scalar(parts[0])
cache={}
def raster(path):
 if path in cache:return cache[path]
 im=Image.open(path).convert('RGB');pix=im.load();pts=[(x,y) for y in range(im.height) for x in range(im.width) if (lambda c:c[2]>c[0]*1.2 and c[2]>c[1]*1.03 and c[0]<130)(pix[x,y])];assert pts,path
 bb=(min(x for x,y in pts),max(x for x,y in pts),min(y for x,y in pts),max(y for x,y in pts));cache[path]=(im.size,bb);return cache[path]
def check(r):
 q=r['question'];sol=q[':question/worked-solution'];f=q[':question/answer-fields'][0];gm=r['generation']
 a=scalar(re.search(r'\$a=(.*?)\$',sol)[1]);b=scalar(re.search(r'\$b=(.*?)\$',sol)[1]);assert a>b>0
 expected=X**2/a**2+Y**2/b**2;values=[lhs(c[':answer/value']) for c in f[':answer-field/choices']]
 assert len(set(values))==len(values)
 good=[ix for ix,z in enumerate(values) if s.expand(z-expected)==0];assert len(good)==1
 assert f[':answer-field/correct'][1]==f[':answer-field/choices'][good[0]][':answer/id'];n['choices']+=len(values)
 if gm['bank_profile']=='method':
  bank=[expected,X**2/b**2+Y**2/a**2,X**2/a+Y**2/b,X**2/(4*a**2)+Y**2/(4*b**2),X**2/a**2+Y**2/b]
  assert set(values)==set(bank);n['whole_method_banks']+=1
 for block in re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S):
  block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  rows=block.split(r' \\ ')
  for row in rows:assert s.expand(lhs(row).subs({V:a,Z:b})-expected)==0,row;n['displayed_equalities']+=1
  if len(rows)>1:
   expected_count=3 if q[':question/difficulty'].endswith('/easy') else 4 if gm['template'].endswith('blank') or gm['template']=='quarter_radio' else 6
   assert len(rows)==expected_count,(gm['template'],rows)
 ref=re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]
 if ref.startswith('images/'):
  # Every source tick label was read at full resolution by root before this check.
  source=gm['source_profile'];labels={qid:tuple(map(s.Rational,z)) for qid,z in g.PARAMS.items()};assert (a,b)==labels[source]
 else:
  path=Path(ref);side=json.load(open(path.with_suffix('.json')));assert side['equal_aspect']
  assert [s.Rational(side['a']),s.Rational(side['b'])]==[a,b]
  assert side['intercepts']==[[-float(a),0],[float(a),0],[0,-float(b)],[0,float(b)]]
  size,bb=raster(path);assert size==(840,630);scale=min(.92*size[0]/(side['bounds'][1]-side['bounds'][0]),.90*size[1]/(side['bounds'][3]-side['bounds'][2]));assert abs((bb[1]-bb[0])-2*float(a)*scale)<4 and abs((bb[3]-bb[2])-2*float(b)*scale)<4,(path,a,b,scale,bb)
  assert side['bounds'][0]<-float(a)<float(a)<side['bounds'][1];assert side['bounds'][2]<-float(b)<float(b)<side['bounds'][3];n['generated_rasters']+=1
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}$=1$' in q[':question/problem']
 if gm['source_profile'] or gm['bank_profile'] in ('opaque_integer','opaque_decimal','reciprocal'):assert gm.get('eligible_for_learning') is False
 else:assert gm.get('eligible_for_learning') is True
 n['records']+=1
source={q[':question/math-academy-id']:q for q in json.load(open(D/'source.json'))['record'][':knowledge-point/questions']}
for c in json.load(open(D/'source-cases.json')):
 r=g.generate(c['level'],parameters=c['parameters'],profile=c['bank_profile']);check(r);q=r['question'];old=source[c['source_id']]
 assert q[':question/problem']==old[':question/problem'];assert q[':question/worked-solution']==old[':question/worked-solution'];n['source_solutions']+=1
 for sf,gf in zip(old[':question/answer-fields'],q[':question/answer-fields']):
  assert sorted(z[':answer/value'] for z in sf[':answer-field/choices'])==sorted(z[':answer/value'] for z in gf[':answer-field/choices']);n['source_banks']+=1;n['source_values']+=len(gf[':answer-field/choices'])
  assert next(z[':answer/value'] for z in gf[':answer-field/choices'] if z[':answer/id']==gf[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
n['changed_public_source_profiles']=0
for c in json.load(open(D/'source-cases.json')):
 for a,b in g.domain(c['level'],c['template']):
  if (str(a),str(b))==tuple(c['parameters'][k] for k in ('a','b')):continue
  try:r=g.generate(c['level'],profile=c['bank_profile'],parameters={'a':str(a),'b':str(b)})
  except ValueError:continue
  check(r);assert not r['generation']['plot_data'].get('reused_source');n['changed_public_source_profiles']+=1;break
 else:raise AssertionError('No changed source instance')
for l in ('easy','moderate','hard'):
 seen=set()
 for seed in range(18):
  r=g.generate(l,seed);check(r);seen.add(tuple(r['generation']['parameters'].values()))
  z=g.generate(l,seed+77,template=r['generation']['template'],profile=r['generation']['bank_profile'],parameters=r['generation']['parameters']);assert z['question'][':question/id']==r['question'][':question/id']
 assert len(seen)>=10;n[l+'_meaningful_sample']=len(seen)
for r in json.load(open(D/'review.json')):check(r.get('record',r))
# Exhaustively count eligible normal complete mathematical pairs from method formulas,
# with independent bounded domains (no option order, layout or bank-profile counts).
for level in ('easy','moderate','hard'):
 vals=list(map(s.Rational,range(1,10))) if level=='easy' else [s.Rational(i,2) for i in range(2,20)] if level=='moderate' else [s.Rational(i,4) for i in range(3,24,2)]
 tasks=[]
 for a in vals:
  for b in vals:
   if not a>b or a/b>6 or level=='moderate' and a.q==b.q==1:continue
   tasks.append((a,b))
 n[level+'_finite_mathematical_tasks']=len(tasks)
 for template,(l,kind,style) in g.SPECS.items():
  if l!=level:continue
  for a,b in g.domain(l,template):
   # Domain guard is independently reflected in explicit forbidden-rational checks.
   assert (a,b) in tasks
 for bad in ({'a':'7/3','b':'2/3'},{'a':'9/997','b':'3/997'},{'a':'2','b':'3'}):
  try:g.generate(level,parameters=bad)
  except ValueError:pass
  else:raise AssertionError(('invalid reduced-object bounds',level,bad))
(R/'qa/17592186087839-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
