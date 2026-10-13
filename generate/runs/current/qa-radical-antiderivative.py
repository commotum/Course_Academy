"""Root complete-source and actual root/power/stage/fragment QA."""
import importlib.util,json,re,hashlib,sys
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186064168'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'power-rule-readback.py','p');g=load(D.with_suffix('.py'),'g');s=p.s
n=dict(records=0,choices=0,whole_banks=0,printed_equalities=0,source_prompts=0,source_solutions=0,source_banks=0,source_values=0,source_designations=0,source_absent_designations=0,source_fieldless=0,source_unrated=0)
def integrand(prompt):
 math=re.search(r'\$([^$]+)\$',prompt).group(1).rstrip('.');return p.scalar(math)
def check(r):
 q=r['question'];gm=r['generation'];raw=gm['evidence_only'];assert gm['eligible_for_learning']==(not raw);f=integrand(q[':question/problem']);primitive=s.integrate(f,p.x)
 if not raw:assert 'Work on $x>0$.' in q[':question/problem']
 for field in q.get(':question/answer-fields',[]):
  vals=[p.scalar(a[':answer/value']) for a in field[':answer-field/choices']];assert all(not p.same_derivative(z,t) for i,z in enumerate(vals) for t in vals[:i]);good=[i for i,z in enumerate(vals) if p.eq(s.diff(z,p.x),f)];assert len(good)==1
  if ':answer-field/correct' in field:assert field[':answer-field/correct'][1]==field[':answer-field/choices'][good[0]][':answer/id']
  if field[':answer-field/type'].endswith('/blank'):
   assert '{{'+field[':answer-field/key']+'}}' in q[':question/problem'];assert all(not v.has(p.C) for v in vals)
   if not raw:assert 'Enter only the term before $+C$, with no additive constant.' in q[':question/problem']
  elif gm['bank_profile']=='authored':
   degree=f.as_powers_dict()[p.x];bank=[primitive+p.C,(degree+1)*p.x**(degree+1)+p.C,p.x**(degree+1)+p.C,p.x**degree/(degree+1)+p.C,s.diff(f,p.x)+p.C];assert all(sum(p.eq(z,t) for z in vals)==1 for t in bank);n['whole_banks']+=1
  n['choices']+=len(vals)
 sol=q.get(':question/worked-solution')
 if sol:
  blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==2
  rows=blocks[0].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows) in (3,4)
  for row in rows:
   for part in row.split('& ='):
    if part.strip():assert p.same_derivative(p.value(part),primitive),(gm['template'],part);n['printed_equalities']+=1
  rows=blocks[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==5
  assert [row.count(p.DER) for row in rows]==[1,2,1,0,0]
  for row in rows:assert p.eq(p.value(row.replace('& =','')),f);n['printed_equalities']+=1
  for tex in re.findall(r'(?<!\$)\$(?!\$)([^$]+)\$(?!\$)',sol):
   if '=' in tex and not tex.startswith('n='):
    left,right=tex.rstrip('.').split('=');assert p.eq(p.scalar(left),p.scalar(right));n['printed_equalities']+=1
  assert ('check our answer' in sol or 'check by differentiating' in sol)
 n['records']+=1
if __name__=='__main__':
 cases=json.load(open(D/'source-cases.json'));old={q[':question/math-academy-id']:q for q in json.load(open(D/'source.json'))['record'][':knowledge-point/questions']}
 for c in cases:
  r=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(r);q=r['question'];o=old[c['source_id']];assert q[':question/problem']==o[':question/problem'];n['source_prompts']+=1
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in o)
  if ':question/difficulty' not in o:n['source_unrated']+=1
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];n['source_solutions']+=1
  if ':question/answer-fields' not in o:n['source_fieldless']+=1
  for of,gf in zip(o.get(':question/answer-fields',[]),q.get(':question/answer-fields',[])):
   assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in gf[':answer-field/choices']);assert (':answer-field/correct' in gf)==(':answer-field/correct' in of);n['source_banks']+=1;n['source_values']+=len(gf[':answer-field/choices'])
   if ':answer-field/correct' in of:assert of[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1]);n['source_designations']+=1
   else:n['source_absent_designations']+=1
  params={'p':1,'d':2} if c['level']=='easy' else {'p':3,'d':2} if c['level']=='moderate' else {'p':2,'d':7};check(g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=params))
 tasks={}
 for level,templates in g.TEMPLATES.items():
  seen=set()
  for template in templates:
   for a,b in g.domain(level,template):
    r=g.generate(level,seed=19,template=template,parameters={'p':a,'d':b});check(r);seen.add(r['generation']['mathematical_fingerprint']);z=g.generate(level,seed=44,template=template,parameters={'p':a,'d':b});assert r['question'][':question/id']==z['question'][':question/id']
  tasks[level]=len(seen)
 n['finite_meaningful_tasks']=tasks
 for group in json.load(open(D/'review.json')).values():
  for r in group:check(r.get('record',r))
 for level,params in [('easy',{'p':2,'d':4}),('moderate',{'p':1,'d':3}),('hard',{'p':2,'d':9}),('hard',{'p':21,'d':5}),('hard',{'p':19,'d':8})]:
  try:g.generate(level,parameters=params)
  except ValueError:pass
  else:raise AssertionError('Workload guard bypassed')
 (R/'qa/17592186064168-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
