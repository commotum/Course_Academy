"""Root complete actual expansion expressions, whole banks and ordered stages."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186059655'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'rational-trig-readback.py','p');g=load(D.with_suffix('.py'),'g')
n=dict(records=0,choices=0,whole_banks=0,printed_equalities=0,source_prompts=0,source_solutions=0,source_values=0,source_designations=0)
def scalar(t):return p.scalar(t.strip().rstrip('.,='))
def check(r):
 q=r['question'];m=r['generation'];assert m['evidence_only']==m['profile'].startswith('observed_') and m['eligible_for_learning']==(not m['evidence_only']);truth=scalar(q[':question/problem'].split('$')[1]);f=q[':question/answer-fields'][0];vs=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vs)==5 and all(not p.equal(a,b) for i,a in enumerate(vs) for b in vs[:i]);good=[i for i,v in enumerate(vs) if p.equal(v,truth)];assert len(good)==1
 if ':answer-field/correct' in f:assert f[':answer-field/choices'][good[0]][':answer/id']==f[':answer-field/correct'][1]
 if m['profile']=='authored':
  name=m['template'];z=m['parameters'];a,b,d=[z[k] for k in ('a','b','d')];S,C=p.S,p.C
  if name=='paired_squares':expected=[2*a*a,a*a,-a*a,0,-2*a*a]
  elif name in ('cos_ratio','cubic'):expected=[a,-a,2*a,0,-2*a]
  elif name=='cross_ratio':expected=[a,0,-2*a,-a,2*a]
  elif name=='cos_reciprocal':expected=[a+1,a,1,0,-a-1] if a!=1 else [2,1,0,-1,-2]
  elif name=='linear_cos':expected=[a*C-b,a*C+b,-a*C,-a*C-b,a*C]
  elif name=='linear_sin':expected=[b-a*S,-b-a*S,a*S,-a*S,b+a*S]
  else:
   cross=a if name=='cross_single' else a+d
   expected=[cross*S*C-b,cross*S*C+b,-a*S*C-b if name=='cross_single' else (a-d)*S*C-b,cross*S*C,cross*S*C-b*S*S]
  assert all(sum(p.equal(v,e) for v in vs)==1 for e in expected),'Complete method bank mismatch'
 sol=q.get(':question/worked-solution')
 if sol:
  blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==(4 if m['profile']=='authored' else 2 if m['template'] not in ('paired_squares','cos_ratio') else 4)
  for b in blocks:
   last=None
   for row in b.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
    for term in row.replace('&','').split('='):
     if not term.strip():continue
     v=scalar(term);assert p.equal(v,truth),(m['template'],row,v,truth)
     if last is not None:assert p.equal(v,last);n['printed_equalities']+=1
     last=v
  for inline in re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',re.sub(r'\$\$.*?\$\$','',sol,flags=re.S),re.S):
   if '=' in inline:
    a,b=inline.split('=');assert p.equal(scalar(a),scalar(b));n['printed_equalities']+=1
 n['records']+=1;n['choices']+=5;n['whole_banks']+=1
if __name__=='__main__':
 assert json.load(open(D/'source.json'))==json.load(open(R/'sources/17592186059655.json'));old={q[':question/math-academy-id']:q for q in json.load(open(D/'source.json'))['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  level=c['assigned_level'];r=g.generate(level,template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(r);q=r['question'];o=old[c['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:
   ov=next(a[':answer/value'] for a in of[':answer-field/choices'] if a[':answer/id']==of[':answer-field/correct'][':answer/id']);gv=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert ov==gv;n['source_designations']+=1
  n['source_prompts']+=1;n['source_solutions']+=int(':question/worked-solution' in o);n['source_values']+=5
  for k in (1,3,6):check(g.generate(level,template=c['template'],profile='observed_completed',parameters={**c['parameters'],'a':k,'angle':'t'}))
 for level,templates in g.LEVELS.items():
  for template in templates:
   for seed in range(7):
    r=g.generate(level,template=template,seed=13000+seed);check(r);z=g.generate(level,template=template,seed=14000+seed,parameters=r['generation']['parameters']);assert r['question'][':question/id']==z['question'][':question/id']
 for r in json.load(open(D/'review.json')):check(r.get('record',r))
 (R/'qa/17592186059655-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
