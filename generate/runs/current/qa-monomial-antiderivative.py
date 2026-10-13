"""Root independent full-family, printed primitive and derivative-chain readback."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186064167'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','p');g=load(D.with_suffix('.py'),'g');x=p.x;C=p.u
n=dict(records=0,choices=0,complete_banks=0,printed_equalities=0,source_prompts=0,source_solutions=0,source_banks=0,source_values=0,source_absent_designations=0,source_fieldless=0,source_unrated=0)
def expr(t):return p.scalar(t.replace('C','u').replace('✓',''))
def eq(a,b):return s.simplify(a-b)==0
def family(a,b):return bool(s.diff(a,C)!=0)==bool(s.diff(b,C)!=0) and eq(s.diff(a-b,x),0)
DER=r'\frac{\text{d}}{\text{d}x}'
def value(t):
 while DER in t:
  i=t.index(DER);start=i+len(DER);assert t[start]=='(';end=start+1;depth=1
  while depth:depth+=(t[end]=='(')-(t[end]==')');end+=1
  v=s.diff(expr(t[start+1:end-1]),x);t=t[:i]+'('+s.latex(v)+')'+t[end:]
 return expr(t)
def read_n(prompt):
 if r'\int 1' in prompt:return 0
 if r'\intxdx' in prompt:return 1
 m=re.search(r'(?:\{x\}|x)\^\{(\d+)\}',prompt);assert m,prompt;return int(m[1])
def check(r):
 q=r['question'];raw=r['generation']['evidence_only'];assert r['generation']['eligible_for_learning']==(not raw);degree=read_n(q[':question/problem']);integrand=x**degree;primitive=x**(degree+1)/s.Integer(degree+1)+C
 fs=q.get(':question/answer-fields',[])
 for f in fs:
  vals=[expr(a[':answer/value']) for a in f[':answer-field/choices']];assert all(not family(z,t) for i,z in enumerate(vals) for t in vals[:i]);good=[i for i,z in enumerate(vals) if family(z,primitive)];assert len(good)==1
  if not raw:assert f[':answer-field/correct'][1]==f[':answer-field/choices'][good[0]][':answer/id']
  n['choices']+=len(vals)
  if f[':answer-field/type'].endswith('/radio'):
   n['complete_banks']+=1;profile=r['generation']['bank_profile'];profile=('observed_2005' if profile=='raw:q-2005' else 'observed_2022' if profile=='raw:q-2022' else profile);m=degree+1
   if profile=='observed_2005':bank=[m*x**m,primitive,m+C,x**m/s.Integer(m),x**m+C]
   elif profile=='observed_2022':bank=[x**m+C,degree*x**(degree-1)+C,x**degree/s.Integer(degree)+C,primitive,x**(degree-1)+C]
   else:bank=[primitive,x**m+C,x**degree/s.Integer(m)+C,x**(m+1)/s.Integer(m+1)+C,m*x**m+C]
   assert all(sum(eq(z,t) for z in vals)==1 for t in bank)
 sol=q.get(':question/worked-solution')
 if sol:
  blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);derivative=blocks[-1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(derivative)==(4 if degree==0 else 5)
  for row in derivative:assert eq(value(row.replace('& =','').strip()),integrand);n['printed_equalities']+=1
  block=blocks[-2]
  assert r'\frac{{x}^{'+str(degree)+'+1}}{'+str(degree)+'+1}+C' in block
  if r'\begin{aligned}' in block:
   rows=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');targets=[row.split('& =')[-1] for row in rows[-2:]]
  else:targets=block.split('=')[-2:]
  for t in targets:assert family(expr(t),primitive);n['printed_equalities']+=1
  if degree>0:assert '$n='+str(degree)+'$' in sol
  assert "Let's check by differentiating:" in sol
 n['records']+=1
if __name__=='__main__':
 frozen=json.load(open(D/'freeze.json'));assert frozen['generator_sha256']==hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()
 cases=json.load(open(D/'source-cases.json'));old={q[':question/math-academy-id']:q for q in json.load(open(D/'source.json'))['record'][':knowledge-point/questions']}
 for c in cases:
  r=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(r);q=r['question'];o=old[c['source_id']];assert q[':question/problem']==o[':question/problem'];n['source_prompts']+=1
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in o)
  if ':question/difficulty' not in o:n['source_unrated']+=1
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];n['source_solutions']+=1
  if ':question/answer-fields' not in o:n['source_fieldless']+=1
  for of,gf in zip(o.get(':question/answer-fields',[]),q.get(':question/answer-fields',[])):
   assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in gf[':answer-field/choices']);assert ':answer-field/correct' not in gf and ':answer-field/correct' not in of;n['source_banks']+=1;n['source_values']+=len(gf[':answer-field/choices']);n['source_absent_designations']+=1
  if c['template']!='constant':check(g.generate('easy',template=c['template'],profile=c['bank_profile'],parameters={'n':9}))
 for level,domain in g.DOMAINS.items():
  tasks=set()
  for degree in domain:
   template='constant' if degree==0 else 'function'
   for kind in (('blank',) if degree==0 else ('radio','blank')):
    r=g.generate(level,seed=39,template=template,parameters={'n':degree},field_type=kind);check(r);tasks.add(r['generation']['mathematical_fingerprint']);z=g.generate(level,seed=92,template=template,parameters={'n':degree},field_type=kind);assert r['question'][':question/id']==z['question'][':question/id']
  assert len(tasks)==len(domain)
 for r in json.load(open(D/'review.json')):check(r['record'])
 for level,degree in [('easy',21),('moderate',20),('hard',40),('hard',61),('easy',True),('easy','4')]:
  try:g.generate(level,parameters={'n':degree})
  except ValueError:pass
  else:raise AssertionError('Workload guard bypassed')
 n['finite_meaningful_tasks']={level:len(domain) for level,domain in g.DOMAINS.items()}
 (R/'qa/17592186064167-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
