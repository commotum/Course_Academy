"""Root independent standard-form/ordered-axis/complete-bank/solution oracle."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186087841'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','p');g=load(D.with_suffix('.py'),'g');X,Y,V,Z=p.x,p.y,p.v,p.z
n=dict(records=0,choices=0,printed_equalities=0,whole_method_banks=0,source_banks=0,source_values=0,source_solutions=0,source_designations=0,source_missing_designations=0,public_changed_profiles=0)
def val(tex):
 tex=tex.strip().rstrip('.,?');tex=re.sub(r'\\sqrt\[4\]\{(\d+)\}',r'(\1)^(1/4)',tex);tex=re.sub(r'(?<![A-Za-z])a(?![A-Za-z])','v',tex);tex=re.sub(r'(?<![A-Za-z])b(?![A-Za-z])','z',tex);return p.scalar(tex)
def pair(text):
 t=re.fullmatch(r'\$(.*?)\$ and \$(.*?)\$',text);assert t,text;return tuple(val(z) for z in t.groups())
def eq(x,y):return s.simplify(x-y)==0
def check(r):
 q=r['question'];gm=r['generation'];math=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q[':question/problem'],re.S);t=next(z for z in math if r'\frac' in z);lhs,rhs=t.rstrip('.,?').split('=');assert val(rhs)==1
 lhs=s.expand(val(lhs));dx=1/lhs.coeff(X,2);dy=1/lhs.coeff(Y,2);assert eq(lhs,X**2/dx+Y**2/dy) and dx>0 and dy>0 and dx!=dy
 a,b=s.sqrt(dx),s.sqrt(dy);M,m=max(a,b),min(a,b);correct=(2*M,2*m)
 assert gm['evidence_only']==bool(gm['source_id']);assert gm['eligible_for_learning']==(not gm['evidence_only'])
 for f in q[':question/answer-fields']:
  radio=f[':answer-field/type'].endswith('/radio');values=[pair(z[':answer/value']) if radio else val(z[':answer/value']) for z in f[':answer-field/choices']]
  assert len(values)==(5 if radio else 1);n['choices']+=len(values)
  if radio:
   assert all(any(not eq(v,w) for v,w in zip(z,t)) for i,z in enumerate(values) for t in values[:i]);good=[i for i,z in enumerate(values) if all(eq(v,w) for v,w in zip(z,correct))];assert len(good)==1
   if gm['profile']=='authored_axes':
    bank=[correct,(M,m),(2*M,m),(M,2*m),(M**2,m**2)];assert all(sum(all(eq(v,w) for v,w in zip(z,t)) for z in values)==1 for t in bank);n['whole_method_banks']+=1
  else:
   assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem'];assert eq(values[0],correct[0 if f[':answer-field/key']=='field-1' else 1]);good=[0]
  if ':answer-field/correct' in f:assert f[':answer-field/correct'][1]==f[':answer-field/choices'][good[0]][':answer/id']
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];sub={V:a,Z:b};blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==1
  left,right=blocks[0].strip().rstrip('.').split('=');assert val(right)==1 and eq(val(left).subs(sub),lhs);n['printed_equalities']+=1
  inline=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',sol,re.S)
  for t in inline:
   if '=' not in t:continue
   chain=[val(z).subs(sub) for z in t.split('=')];assert all(eq(z,chain[0]) for z in chain[1:]),t;n['printed_equalities']+=len(chain)-1
  horizontal=re.search(r'horizontal radius must be\s*\$(.*?)\$',sol);vertical=re.search(r'vertical radius must be\s*\$(.*?)\$',sol);assert horizontal and vertical
  assert horizontal[1].startswith('a=') and vertical[1].startswith('b=')
  major=re.search(r'semi-major axis has length \$(.*?)\$',sol);minor=re.search(r'semi-minor axis has length \$(.*?)\$',sol);assert major and minor
  assert eq(val(major[1].split('=')[-1]),M) and eq(val(minor[1].split('=')[-1]),m)
 n['records']+=1
frozen=json.load(open(D/'manifest.json'));assert all(hashlib.sha256(Path(q).read_bytes()).hexdigest()==h for q,h in frozen['files'].items());n['frozen_worker_hashes']=len(frozen['files'])
old={q[':question/math-academy-id']:q for q in json.load(open(D/'source.json'))['record'][':knowledge-point/questions']}
for c in json.load(open(D/'source-cases.json')):
 r=g.generate(c['level'],template=c['template'],profile=c.get('bank_profile') or 'source_'+c['source_id'],parameters=c['parameters']);check(r);q=r['question'];o=old[c['source_id']]
 assert q[':question/problem']==o[':question/problem']
 for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in o)
 if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];n['source_solutions']+=1
 for of,gf in zip(o[':question/answer-fields'],q[':question/answer-fields']):
  assert of[':answer-field/key']==gf[':answer-field/key'];assert sorted(z[':answer/value'] for z in of[':answer-field/choices'])==sorted(z[':answer/value'] for z in gf[':answer-field/choices']);n['source_values']+=len(gf[':answer-field/choices']);n['source_banks']+=1
  assert (':answer-field/correct' in of)==(':answer-field/correct' in gf)
  if ':answer-field/correct' in of:assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in gf[':answer-field/choices'] if z[':answer/id']==gf[':answer-field/correct'][1]);n['source_designations']+=1
  else:n['source_missing_designations']+=1
 z=g.generate(c['level'],seed=2469,template=c['template'],profile=c.get('bank_profile') or 'source_'+c['source_id']);check(z);assert z['question']!=q;n['public_changed_profiles']+=1
for level in ('easy','moderate','hard'):
 seen=set()
 for kind in ('radio','blank'):
  for seed in range(12):
   r=g.generate(level,seed+3700+(100 if kind=='blank' else 0),field_type=kind);check(r);seen.add(r['generation']['mathematical_fingerprint']);z=g.generate(level,seed+9600,template=r['generation']['template'],profile=r['generation']['profile'],parameters=r['generation']['parameters']);assert z['question'][':question/id']==r['question'][':question/id']
 assert len(seen)>=20;n[level+'_meaningful_sample']=len(seen)
for r in json.load(open(D/'review.json')):check(r.get('record',r))
# Independent finite number-form catalogs, using reduced rational values.
for level in ('easy','moderate','hard'):
 values=set(s.Rational(i,j) for i in range(1,101) for j in (1,4,9,16))
 def valid(v):
  if v.p>100:return False
  if level=='easy':return v.q==1
  if level=='moderate':return v.q in (1,4,9)
  if v.q not in (4,9,16) or s.sqrt(v.p).is_Integer:return False
  sf=s.prod(q for q,power in s.factorint(v.p).items() if power%2)
  return sf in (2,3,5,6,7) and s.sqrt(v.p/sf)<=3
 values=sorted(v for v in values if valid(v));count=0
 for i,a in enumerate(values):
  for b in values[:i]:
   if level=='moderate' and sum(v.q>1 for v in (a,b))!=1:continue
   count+=1
 n[level+'_finite_mathematical_tasks']=count
 invalid={'dx':'1/997','dy':'2/997'}
 try:g.generate(level,parameters=invalid)
 except ValueError:pass
 else:raise AssertionError('Unbounded reduced denominators admitted')
(R/'qa/17592186087841-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
