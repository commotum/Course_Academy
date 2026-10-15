"""Root source-parameter semantic replay, separate from raw copying."""
import sys,json,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186096620-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_polysource_gen',D.with_suffix('.py'));H=load('root_polysource_scalar',R/'ode-scalar-parser.py');x=H.x
parse=lambda z:H.scalar(z.replace('[','(').replace(']',')'))
eq=lambda a,b:s.cancel(a-b)==0
result=dict(normal_anchor_prompts=0,normal_anchor_banks=0,normal_anchor_values=0,normal_anchor_designations=0)
for sid,o in G.SOURCES.items():
 profile='observed-'+sid[2:]if G.TEMPLATES[sid]['field']=='radio'else'fragment';q=G.generate('easy',template=sid,parameters=G.TEMPLATES[sid]['p'],profile=profile)['question'];F=parse(re.search(r'\$f\(x\)\s*=\s*(.*?)\$',q[':question/problem'])[1]);sol=o.get(':question/worked-solution')
 if sol:
  u=parse(re.search(r'\$u\(x\)\s*=\s*(.*?)\$',sol)[1]);v=parse(re.search(r'\$v\(x\)\s*=\s*(.*?)\$',sol)[1]);assert eq(F,u/v)
 else:assert sid=='q-11966'and eq(F,-5*x/(2*x-1))
 result['normal_anchor_prompts']+=1
 for f,of in zip(q.get(':question/answer-fields',[]),o.get(':question/answer-fields',[])):
  vals=[parse(a[':answer/value'])for a in f[':answer-field/choices']];original=[parse(a[':answer/value'])for a in of[':answer-field/choices']];assert len(vals)==len(original)
  assert all(sum(eq(v,w)for w in vals)==1 for v in original);assert all(sum(eq(w,v)for v in original)==1 for w in vals);result['normal_anchor_banks']+=1;result['normal_anchor_values']+=len(vals)
  if ':answer-field/correct'in of:assert eq(parse(of[':answer-field/correct'][':answer/value']),next(v for a,v in zip(f[':answer-field/choices'],vals)if a[':answer/id']==f[':answer-field/correct'][1]));result['normal_anchor_designations']+=1
(R/'qa/17592186096620-source-anchor-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
