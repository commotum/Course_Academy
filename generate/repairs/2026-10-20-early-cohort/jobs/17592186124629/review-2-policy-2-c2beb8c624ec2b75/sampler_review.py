"""Independent targeted batch audit. Run with job Python -B sampler_review.py."""
import collections, hashlib, importlib.util, json, re, subprocess, sys, types
from pathlib import Path
sys.dont_write_bytecode = True
E=Path(__file__).resolve().parent; W=E.parent/'workspace'
sys.path.insert(0,str(W))
sp=importlib.util.spec_from_file_location('current_generator',W/'17592186124629.py')
g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def save(n,x): (E/n).write_text(json.dumps(x,indent=2)+'\n')
def value(f):return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def bits(r):
 fs=r['question'][':question/answer-fields']
 return tuple(value(f)=='true' for f in fs) if len(fs)==3 else tuple(bool(re.search(r'\b'+x+r'\b',value(fs[0]))) for x in ('I','II','III'))
def statements(r):
 q=r['question'];fs=q[':question/answer-fields']
 return [f[':answer-field/key'] for f in fs] if len(fs)==3 else re.findall(r'^I{1,3}\. (.+)$',q[':question/problem'],re.M)
def family(r):
 def concept(s):
  for cue,c in [('basis','basis'),('Ax=','null-solution'),('nullity','nullity'),('Null','null'),('Col','col'),('rank','rank'),('det','det'),('pivot','pivot'),('invertible','inv')]:
   if cue in s:return c
  raise AssertionError(s)
 return ('checkbox' if len(r['question'][':question/answer-fields'])==3 else 'radio')+':'+','.join(map(concept,statements(r)))
def stats(rows):
 groups=collections.defaultdict(list)
 for r in rows:groups[family(r)].append(r)
 result=[]
 for f,rs in sorted(groups.items()):
  masks=collections.Counter(bits(r) for r in rs)
  pos=collections.Counter(tuple(i for i,b in enumerate(bits(r)) if b) if f.startswith('checkbox') else tuple(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/value']==value(r['question'][':question/answer-fields'][0])) for r in rs)
  result.append({'family':f,'records':len(rs),'masks':{str(k):v for k,v in masks.items()},'best_constant_subset':max(masks.values()),'best_constant_position':max(pos.values()),'selection_counts':dict(collections.Counter(sum(bits(r)) for r in rs)), 'ids':[r['question'][':question/id'] for r in rs]})
 return result
def semantic(r):return (r['question'][':question/problem'],tuple(statements(r)))
seed=2086806769
batch=json.load(open(E/'runner-batch.json')); assert g.batch(seed=seed,count=5)==batch
before=types.ModuleType('before');before.__file__=str(W/'17592186124629.py')
old_code=(W/'evidence/batch-repair/before-generator.py').read_text()
exec(compile(old_code,'retained-before-generator.py','exec'),before.__dict__)
save('retained-before-generator.py.txt',old_code)
legacy=before.batch(seed=seed,count=5);save('before-batch.json',legacy)
executions=[]
# Execute the unweakened retained independent assertion against both versions.
for label,entry in [('failing',None),('current',W/'17592186124629.py')]:
 if entry is None:
  # Load retained code with original source path: no changes to construction.
  code="import sys,types;from pathlib import Path;sys.dont_write_bytecode=True;sys.path.insert(0,sys.argv[1]);m=types.ModuleType('old');m.__file__=sys.argv[2];exec(compile(Path(sys.argv[3]).read_text(),'retained-before-generator.py','exec'),m.__dict__);import importlib.util;original=importlib.util.module_from_spec;importlib.util.module_from_spec=lambda spec:m;exec(Path(sys.argv[4]).read_text())"
  # spec loader would reload current; use a local verbatim strict test with injected old g.
  strict=(E/'failing_batch_check.py').read_text();tail=strict[strict.index('rows=g.batch'):]
  command=[sys.executable,'-B','-c',"import sys,types,json;from pathlib import Path;from collections import defaultdict;sys.path.insert(0,sys.argv[1]);g=types.ModuleType('old');g.__file__=sys.argv[2];exec(compile(Path(sys.argv[3]).read_text(),'retained-before-generator.py','exec'),g.__dict__);exec(Path(sys.argv[4]).read_text().split('rows=g.batch',1)[1].join(['rows=g.batch','']))",str(W),str(W/'17592186124629.py'),str(W/'evidence/batch-repair/before-generator.py'),str(E/'failing_batch_check.py')]
 else:command=[sys.executable,'-B',str(E/'failing_batch_check.py'),str(entry)]
 p=subprocess.run(command,capture_output=True,text=True)
 executions.append({'version':label,'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
assert executions[0]['exit_code']==1 and 'all 2 surviving questions share' in executions[0]['stderr']
assert executions[1]['exit_code']==0
save('retained-regression-results.json',executions)
# One complete changed selection pass, then three small fresh seeded regressions.
prefix=g.batch(seed=seed,count=73);save('decision-prefix.json',prefix)
prefix_stats=stats(prefix)
assert len(prefix)==73 and len(prefix_stats)==13
for s in prefix_stats:
 assert s['records']==len(s['masks'])==(7 if s['family'].startswith('checkbox') else 5)
 assert len(s['selection_counts'])>1
small=[]
for fresh_seed in (927461,34017,85901):
 rs=g.batch(seed=fresh_seed,count=5)
 st=stats(rs)
 assert all(len(s['masks'])==s['records'] for s in st)
 small.append({'seed':fresh_seed,'records':rs,'coverage':st})
save('small-regression-batches.json',small)
# Ordering repair must retain the unchanged complete finite semantic domain.
old=before.batch(seed=seed,count=10000);new=g.batch(seed=seed,count=10000)
oldset={semantic(r) for r in old};newset={semantic(r) for r in new}
assert oldset==newset and len(newset)==len(new)
save('domain-preservation.json',{'command':'python -B sampler_review.py','old_count':len(old),'current_count':len(new),'semantic_count':len(newset),'lost':len(oldset-newset),'added':len(newset-oldset),'semantic_sha256':hashlib.sha256(json.dumps(sorted(newset)).encode()).hexdigest(),'comparison':'Visible prompt and conclusion labels; semantic domain equality only, not a repeated exhaustive correctness audit.'})
save('sampling-results.json',{'seed':seed,'matches_exact_runner_batch':True,'before_batch':stats(legacy),'current_batch':stats(batch),'decision_prefix':prefix_stats,'finite_domain':len(newset),'small_regression_seeds':[x['seed'] for x in small],'retained_preflight':'Read all retained findings and repair-preflight.json (script check_batch_selection.py). Independent unweakened failing_batch_check.py demonstrates old failure and current pass; own prefix and domain checks corroborate claims. Author scripts not executed in package because they write there.'})
print(json.dumps({'retained_failure':executions[0]['exit_code'],'current':executions[1]['exit_code'],'prefix':len(prefix),'families':len(prefix_stats),'domain':len(newset)}))
