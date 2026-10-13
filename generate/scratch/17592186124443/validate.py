"""Fail-closed printed-function, formal-operand, stage and full-bank audit."""
import importlib.util,json,re,sys,subprocess,hashlib
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('gradient_gen',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ps=importlib.util.spec_from_file_location('printed_parser',ROOT/'math_parser.py');p=importlib.util.module_from_spec(ps);ps.loader.exec_module(p)
x,y=p.x,p.y
STATS=dict(records=0,formal_operands=0,individual_partial_stages=0,gradient_stages=0,choice_vectors=0,supplied_component_stages=0)
def scalar(raw):
 raw=re.sub(r'\\text\{[^}]*\}','',raw).replace('\xa0','').replace(r'\;','').replace(r'\!','')
 return p.scalar(raw)
def eq(a,b):return s.simplify(a-b)==0
def vector(raw):
 raw=raw.strip().rstrip('.,').replace(r'\,','')
 if '⟨' in raw and not raw.startswith('⟨'):
  start=raw.index('⟨');factor=scalar(raw[:start]);return tuple(factor*z for z in vector(raw[start:]))
 if raw.startswith('⟨'):
  end=raw.index('⟩');assert end==len(raw)-1,raw
  return tuple(scalar(z) for z in raw[1:-1].split(','))
 z=s.expand(scalar(raw));A,B=z.coeff(p.i),z.coeff(p.j);assert eq(z,A*p.i+B*p.j),raw;return A,B

def parens(raw,start):
 assert raw[start]=='(';depth=0
 for j in range(start,len(raw)):
  depth+=(raw[j]=='(')-(raw[j]==')')
  if depth==0:return raw[start+1:j],j+1
 raise AssertionError(raw)
def prompt_math(r):
 q=r['question'];t=r['generation']['template'];text=q[':question/problem']
 if t=='components':
  if r['generation']['evidence_only']:return None,None,tuple(s.Integer(r['generation']['parameters'][z]) for z in ('P','Q'))
  vals=re.findall(r'E_[xy]=(-?\d+)',text);assert len(vals)==2;textpt=re.search(r'At \$\((.*?)\)',text);assert textpt
  return None,None,tuple(map(s.Integer,vals))
 m=re.search(r'[fgh]\(x,\s*y\)\s*=\s*(.*?)\$',text);assert m,text;F=scalar(m[1]);D=tuple(s.diff(F,z) for z in (x,y));pt=None
 m=re.search(r'(?:at|point)\s*\$?\((.*?)\)',text)
 if m:pt=tuple(scalar(z) for z in m[1].split(','));assert len(pt)==2
 V=tuple(s.simplify(z.subs(dict(zip((x,y),pt)),simultaneous=True)) for z in D) if pt else D
 return F,D,V

def structure(r):
 q=r['question'];t=r['generation']['template']
 if ':question/worked-solution' not in q:return
 bs=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S)
 rows=[[re.split(r'&\s*=',row,maxsplit=1)[1].strip().rstrip('.') for row in b.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')] for b in bs]
 if t=='polynomial':
  assert list(map(len,rows))==[6,4];assert rows[0][1].endswith('+0+0') and rows[0][4].startswith('0');assert rows[1][2].count(r'\cdot')==4
 elif t=='root':assert list(map(len,rows))==[4,4] and r'\sqrt' in rows[1][2] and r'\cdot' in rows[1][2]
 elif t=='log_cos':
  assert list(map(len,rows))==[6,2];assert r'\cdot y+0' in rows[0][1];assert r'\cdot x-' in rows[0][4] and rows[0][4].count(r'\cdot')==2;assert r'\cdot' not in rows[0][2] and r'\cdot' not in rows[0][5]
 elif t=='sin_log':assert list(map(len,rows))==[5,2] and r'\cdot \frac{1}{y}' in rows[0][3] and r'\cdot' not in rows[0][4]
 elif t=='atan_product':assert list(map(len,rows))==[4,5] and r'\operatorname{arctan}' in rows[1][2] and r'\cdot' in rows[1][3] and r'\pi' in rows[1][3] and r'\operatorname{arctan}' not in rows[1][3]
 elif t=='radial_log':
  assert list(map(len,rows))==[4,7];assert rows[1][3].count('^{2}')==2;assert '^{2}' not in rows[1][4];assert '⟨' in rows[1][4] and '⟨' in rows[1][5] and rows[1][4]!=rows[1][5]
 elif t=='atan_ratio':
  assert list(map(len,rows))==[8,2]
  for chain,common,reduced in ((1,2,3),(5,6,7)):
   assert rows[0][chain].startswith(r'\frac{1}{1+') and r'\cdot' in rows[0][chain]
   assert not rows[0][common].startswith(r'\frac{1}{1+') and r'\cdot' in rows[0][common] and rows[0][common].count(r'\frac')>=2
   assert r'\cdot' not in rows[0][reduced]
 elif t in ('quotient','hard_quotient'):
  assert len(rows[0])==6
  for idx in (1,4):assert ')-(' in rows[0][idx] and '^{2}' in rows[0][idx]
  assert len(rows[1])==(4 if t=='hard_quotient' else 2)
  if t=='hard_quotient':assert rows[1][2].count('(')>=8
 elif t=='components':
  assert list(map(len,rows))==([2,3] if r['generation']['evidence_only'] else [3])

def audit(r):
 q=r['question'];raw=r['generation']['evidence_only'];F,D,V=prompt_math(r);structure(r)
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 for text in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
  assert text.count('$')%2==0,text;balance=0
  for ch in text:
   balance+=(ch=='{')-(ch=='}');assert balance>=0,text
  assert balance==0,text
  assert '+-' not in text and '--' not in text,text
 for fi,f in enumerate(q[':question/answer-fields']):
  vals=[(scalar(a[':answer/value']),) if r['generation']['template']=='components' else vector(a[':answer/value']) for a in f[':answer-field/choices']]
  assert not any(all(eq(a,b) for a,b in zip(v,w)) for i,v in enumerate(vals) for w in vals[:i]),r
  for a,val in zip(f[':answer-field/choices'],vals):
   valid=all(eq(z,w) for z,w in zip(val,(V[fi],) if r['generation']['template']=='components' else V));STATS['choice_vectors']+=1
   if ':answer-field/correct' in f:assert valid==(a[':answer/id']==f[':answer-field/correct'][1]),(r,a,V)
  if f[':answer-field/type'].endswith('blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']

 if F is None and ':question/worked-solution' in q:
  bs=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S)
  rows=[[re.split(r'&\s*=',row,maxsplit=1)[1].strip().rstrip('.') for row in b.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')] for b in bs]
  if raw:
   declared=tuple(scalar(z) for z in rows[0]);assert all(eq(a,b) for a,b in zip(declared,V));STATS['supplied_component_stages']+=2
   eligible=rows[1][1:]
  else:
   declared=V;eligible=[z.replace('E_x','('+g.L(V[0])+')').replace('E_y','('+g.L(V[1])+')') for z in rows[0]]
  for rhs in eligible:
   got=vector(rhs);assert all(eq(a,b) for a,b in zip(got,declared)),(rhs,got,declared);STATS['supplied_component_stages']+=1
 if F is not None and ':question/worked-solution' in q:
  fname=re.search(r'([fgh])\(x,\s*y\)\s*=',q[':question/problem'])[1]
  if not raw:
   seen=re.findall(r'(?:∇|\{)([fgh])',q[':question/worked-solution']);assert all(z==fname for z in seen),(fname,seen)
  coord=None;gradient=False;evaluated=False
  for b in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S):
   for row in b.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
    lhs,rhs=re.split(r'&\s*=',row,maxsplit=1);lhs=lhs.strip();rhs=rhs.strip().rstrip('.')
    m=re.search(r'\{?[fgh]\}?_\{?([xy])\}?\(x,y\)',lhs)
    if m:coord=(x,y)['xy'.index(m[1])];gradient=False
    if '∇' in lhs:
     gradient=True;coord=None;args=re.search(r'\((.*?)\)',lhs)[1]
     evaluated=args!='x,y' and args!='x, y'
     actual=tuple(scalar(z) for z in args.replace(r'\,','').split(','));expected=tuple(s.diff(F,z).subs(dict(zip((x,y),actual)),simultaneous=True) for z in (x,y))
    fm=re.match(r'\\frac\{∂\}\{∂([xy])\}',rhs)
    if fm:
     operand,end=parens(rhs,fm.end());actual=scalar(operand);assert eq(actual,F),(operand,F);assert end==len(rhs);STATS['formal_operands']+=1;continue
    if gradient:
     def part(m):
      args=tuple(scalar(z) for z in m[2].replace(r'\,','').split(','));dv=s.diff(F,(x,y)['xy'.index(m[1])]).subs(dict(zip((x,y),args)),simultaneous=True)
      return '('+g.L(dv)+')'
     rhs=re.sub(r'\{?[fgh]\}?_\{?([xy])\}?\(([^()]*)\)',part,rhs)
     got=vector(rhs);assert all(eq(a,b) for a,b in zip(got,expected)),(r['generation'],rhs,got,expected);STATS['gradient_stages']+=1
    else:
     assert coord is not None,row;got=scalar(rhs);assert eq(got,s.diff(F,coord)),(r['generation'],rhs,got,s.diff(F,coord));STATS['individual_partial_stages']+=1
 STATS['records']+=1

def write(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def engine(r,label):
 checks=[]
 for fi,f in enumerate(r['question'][':question/answer-fields']):
  if ':answer-field/correct' not in f:continue
  for a in f[':answer-field/choices']:
   good=a[':answer/id']==f[':answer-field/correct'][1]
   if f[':answer-field/type'].endswith('blank'):
    value=a[':answer/value'];checks += [dict(field_index=fi,submitted=value,expected='accepted',purpose='canonical scalar'),dict(field_index=fi,submitted='('+value+')+0',expected='accepted',purpose='unreduced equivalent scalar'),dict(field_index=fi,submitted='('+value+')+1',expected='rejected',purpose='wrong scalar')]
   else:checks.append(dict(field_index=fi,submitted_answer_id=a[':answer/id'],expected='accepted' if good else 'rejected',purpose='all owned radio selections'))
 if not checks:return None
 # Native fixture requires complete fields: raw legacy field omissions cannot be
 # graded, so grade only the source's authoritative complete field, explicitly.
 rr=json.loads(json.dumps(r));rr['question'][':question/answer-fields']=[f for f in rr['question'][':question/answer-fields'] if ':answer-field/correct' in f]
 if len(rr['question'][':question/answer-fields'])!=len(r['question'][':question/answer-fields']):
  for c in checks:c['field_index']=0
 return dict(label=label,record=rr,checks=checks)

def main():
 cases=[];reviews=[];native=[];counts=dict(prompts=0,solutions=0,exact_solution_strings=0,fields=0,values=0,designations=0,missing_designations=0)
 for t,(level,sid) in g.TEMPLATES.items():
  if sid:
   c=dict(source_id=sid,template=t,parameters=g.BASE[t],bank_profile='raw',level=level);cases.append(c);r=g.generate(level,template=t,parameters=c['parameters'],profile='raw');q0=g.SOURCES[sid];q=r['question'];audit(r)
   assert q[':question/problem']==q0[':question/problem'],(t,'prompt');counts['prompts']+=1
   for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in q0),(t,key)
   if ':question/worked-solution' in q0:assert q[':question/worked-solution']==q0[':question/worked-solution'],(t,'solution');counts['solutions']+=1;counts['exact_solution_strings']+=1
   assert len(q[':question/answer-fields'])==len(q0[':question/answer-fields'])
   for f,f0 in zip(q[':question/answer-fields'],q0[':question/answer-fields']):
    assert f[':answer-field/key']==f0[':answer-field/key'];assert f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];counts['fields']+=1
    expected=[(scalar(a[':answer/value']),) if t=='components' else vector(a[':answer/value']) for a in f0[':answer-field/choices']]
    for a in f[':answer-field/choices']:
     val=(scalar(a[':answer/value']),) if t=='components' else vector(a[':answer/value']);i=next((i for i,z in enumerate(expected) if all(eq(a,b) for a,b in zip(val,z))),None);assert i is not None,(t,val,expected);expected.pop(i);counts['values']+=1
    assert not expected
    assert (':answer-field/correct' in f)==(':answer-field/correct' in f0)
    if ':answer-field/correct' in f0:
     actual=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);expected=f0[':answer-field/correct'][':answer/value'];assert all(eq(a,b) for a,b in zip((scalar(actual),) if t=='components' else vector(actual),(scalar(expected),) if t=='components' else vector(expected)));counts['designations']+=1
    else:counts['missing_designations']+=1
   item=engine(r,'raw/'+sid)
   if item:native.append(item)
   reviews.append(dict(label='Original parameterized raw replay '+sid,record=r,original=q0))
  for seed in range(8):
   r=g.generate(level,seed=seed,template=t);audit(r);native.append(engine(r,t+'/'+str(seed)))
   # A change of seed can shuffle choices, not alter content or task identity.
   rr=g.generate(level,seed=seed+1200,template=t,parameters=r['generation']['parameters']);assert rr['question'][':question/id']==r['question'][':question/id']
   if seed<2:reviews.append(dict(label='Generated '+level+' '+t+' seed '+str(seed),record=r))
 # Supported explicit signed and arithmetic boundaries, beyond sampled profiles.
 boundaries=[('polynomial',dict(a=-5,b=4,c=-3,d=2,u=-4,v=3)),('polynomial',dict(a=5,b=4,c=-3,d=-2,u=4,v=-3)),('root',dict(c=16,u=-5,v=9)),('log_cos',dict(n=6,a=6,b=5)),('sin_log',dict(n=6,a=5,b=6)),('atan_product',dict(a=8,u=-5,v=-1)),('radial_log',dict(u='-1/8',v=0)),('radial_log',dict(u='8',v=0)),('atan_ratio',dict(k='1/8')),('atan_ratio',dict(k='8')),('quotient',dict(a=8,b=7,k='1/8')),('quotient',dict(a=7,b=8,k='8')),('components',dict(P=-8,Q=8,u=-4,v=4)),('hard_quotient',dict(a=5,b=4,u=4,v=4))]
 for t,params in boundaries:
  r=g.generate(g.TEMPLATES[t][0],template=t,parameters=params);audit(r);native.append(engine(r,'explicit-boundary/'+t+'/'+json.dumps(params,sort_keys=True)))
 # Fail-closed regression: a wrong printed formal operand cannot be rescued by final correctness.
 probe=g.generate_easy(template='polynomial',parameters=g.BASE['polynomial']);probe['question'][':question/worked-solution']=probe['question'][':question/worked-solution'].replace('8x-3y+0+0','8x+3y+0+0');old=dict(STATS)
 try:audit(probe)
 except AssertionError:STATS.update(old)
 else:raise AssertionError('printed derivative mutation was not detected')
 probe=g.generate_moderate(template='atan_ratio',parameters=dict(k='5/7'));sol=probe['question'][':question/worked-solution'];bs=re.findall(r'\$\$(.*?)\$\$',sol,re.S);rows=bs[0].split(r'\\');rows[2]=rows[3];probe['question'][':question/worked-solution']=sol.replace(bs[0],r'\\'.join(rows));old=dict(STATS)
 try:audit(probe)
 except AssertionError:STATS.update(old)
 else:raise AssertionError('equivalent missing common-denominator stage was not detected')
 # Exercise historical complete banks under changed parameters, including opaque evidence.
 for t,(level,sid) in g.TEMPLATES.items():
  if not sid:continue
  for seed in (30,31):
   r=g.generate(level,seed=seed,template=t,profile='raw');audit(r);item=engine(r,'changed-raw/'+t+'/'+str(seed))
   if item:native.append(item)
   reviews.append(dict(label='Generated raw evidence '+level+' '+t+' seed '+str(seed),record=r))
 # Default family coverage and no cross-level overlap.
 coverage={}
 import random
 for lv in ('easy','moderate','hard'):
  families=[t for t,z in g.TEMPLATES.items() if z[0]==lv];first={}
  for seed in range(100):
   chosen=random.Random(seed).choice(families);first.setdefault(chosen,seed)
  coverage[lv]=sorted({g.generate(lv,seed=seed)['generation']['template'] for seed in first.values()})
 for lv,ts in coverage.items():assert set(ts)=={t for t,z in g.TEMPLATES.items() if z[0]==lv},coverage
 for t in g.TEMPLATES:
  bad=dict(g.BASE[t]);key=next(iter(bad));bad[key]=999
  try:g.generate(g.TEMPLATES[t][0],template=t,parameters=bad)
  except ValueError:pass
  else:raise AssertionError(('missing explicit guard',t))
 write('source-cases.json',cases);write('review.json',reviews);write('engine-input.json',native)
 run=ROOT.parents[1]/'runs/current/check-engine';subprocess.run([str(run),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
 output=dict(status='passed',source_fidelity=counts,printed_mathematics=STATS,default_family_coverage=coverage,native=json.loads((ROOT/'engine-validation.json').read_text()),runtime={'python':sys.version.split()[0],'sympy':s.__version__},plots='none',raw_limits=['q-35988 missing original difficulty/solution/correct designation','q-35990 duplicate legacy field without correct designation; only authoritative field graded','q-168115 relies on missing preceding parts: raw mathematical context underdetermined; normal output supplies scalar partials','Three evaluated scalar historical banks have unrecovered error intent; raw only'],source_sha256=hashlib.sha256((ROOT/'source.json').read_bytes()).hexdigest(),generator_sha256=hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),validator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),native_harness_sha256=hashlib.sha256(run.read_bytes()).hexdigest(),structural_mutations_detected=['wrong polynomial first distributed sign','algebraically equivalent missing atan common-denominator row'])
 write('validation.json',output)
 md=['# Originals and generated variants','Frozen math basis 1356. Raw captures remain in source.json. Each original below is a public parameterized replay; normalized choice notation is compared as complete vectors.']
 for rev in reviews:
  md += ['\n## '+rev['label'],g.markdown(rev['record'])]
 (ROOT/'review.md').write_text('\n\n'.join(md)+'\n');print(json.dumps({k:v for k,v in output.items() if k!='native'},indent=2))
if __name__=='__main__':main()
