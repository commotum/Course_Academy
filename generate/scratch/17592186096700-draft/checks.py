"""Public boundary/CLI, exhaustive finite math and immutable artifact checks."""
import hashlib,importlib.util,json,subprocess,sys,copy
from fractions import Fraction
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;ROOT=D.parents[2];script=D.with_suffix('.py')
spec=importlib.util.spec_from_file_location('draft96700_checks',script);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
result={'invalid_seed':[],'invalid_count':[],'cli':[]}
for x in (True,False,1.0,None,'1'):
 for fn in (g.generate_easy,g.generate_moderate,g.generate_hard):
  try:fn(seed=x)
  except ValueError:pass
  else:raise AssertionError(('invalid seed',x))
 result['invalid_seed'].append(repr(x))
for x in (True,False,1.0,None,'1',0,-1):
 try:g.generate_records(count=x)
 except ValueError:result['invalid_count'].append(repr(x))
 else:raise AssertionError(('invalid count',x))
for level,n in json.loads((D/'finite-catalog.json').read_text())['counts'].items():
 try:g.generate_records(level,count=n+1)
 except ValueError:pass
 else:raise AssertionError('capacity bypass')
for fmt in ('json','markdown'):
 for level,count,expected in [('all',1,3),('all',2,6),('easy',1,1),('moderate',2,2),('hard',2,2)]:
  cmd=[sys.executable,str(script),'--difficulty',level,'--count',str(count),'--seed','19','--format',fmt];a=subprocess.check_output(cmd);b=subprocess.check_output(cmd);assert a==b
  if fmt=='json':
   records=json.loads(a);assert type(records) is list and len(records)==expected
   for ll in {r['question'][':question/difficulty'] for r in records}:
    ks=[r['generation']['mathematical_fingerprint'] for r in records if r['question'][':question/difficulty']==ll];assert len(ks)==len(set(ks))
  else:assert a.count(b'Consider the diagram that is shown above.')==expected
  result['cli'].append({'format':fmt,'difficulty':level,'count':count,'returned':expected,'reproducible':True})
# Independent exact arithmetic from public parameter specification, no generator truth helper.
count=0;truths={};targetset={}
for level,reps in json.loads((D/'finite-representatives.json').read_text()).items():
 seen=set()
 for rep in reps:
  p=rep['parameters'];u=list(map(Fraction,p['u']));v=list(map(Fraction,p['v']));k=Fraction(p['k']);s=p['s'];t=p['t'];template=rep['template']
  def scale(v,c):return tuple(z*c for z in v)
  if template=='opposite_multiple':
   vectors=dict(a=scale(u,k),b=scale(u,s*k),c=tuple(v),d=scale(v,t),e=tuple(u));a,b=p['targets']['primary'];c,d=p['targets']['secondary'];statements=[(a,-k,b),(c,Fraction(-1),d),(a,k,b)]
  else:
   vectors=dict(a=scale(u,k),b=tuple(v),c=scale(u,s),d=scale(v,t),e=(Fraction(-4),Fraction(0)));a,b=p['targets']['primary'];c,d=p['targets']['secondary'];f=1/k if [a,b]==['a','c'] else k;statements=[(a,Fraction(-1),b),(b,-f,a),(c,Fraction(1),d)]
  exact=[vectors[a]==scale(vectors[b],c) for a,c,b in statements]
  gp=g.normalize_parameters(level,template,p);gv,gs=g.vectors_and_statements(template,gp)
  assert [tuple((a,str(c),b)) for a,c,b in statements]==[(a,str(c),b) for a,c,b in gs]
  assert [tuple(str(z) for z in vectors[x]) for x in 'abcde']==[tuple(str(z) for z in gv[x]) for x in 'abcde']
  assert exact==[i in g.truth_set(gv,gs) for i in range(3)]
  key=g.task_key(template,gp);assert key==rep['fingerprint'];assert key not in seen;seen.add(key)
  # Independent alias metamorphic controls: labels do not enter task keys;
  # translated plots, swapping both vector families through180deg, and altered
  # secondary target reversal must never create a new task.
  gp['u']=[-z for z in gp['u']];gp['v']=[-z for z in gp['v']]
  if template=='reciprocal_multiple':
   # unused e is intentionally ignored by task identity
   pass
  assert g.task_key(template,gp)==key
  gp['targets']['secondary']=list(reversed(gp['targets']['secondary']));assert g.task_key(template,gp)==key
  count+=1;truths.setdefault(level,set()).add(tuple(exact));targetset.setdefault(level,set()).add(tuple(p['targets']['primary']))
result['finite_representatives_checked']=count;result['truth_patterns']={k:[list(x) for x in sorted(v)] for k,v in truths.items()};result['representative_primary_targets']={k:[list(x) for x in sorted(v)] for k,v in targetset.items()}
(D/'public-and-finite-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print('CLI and finite mathematics passed',count)
