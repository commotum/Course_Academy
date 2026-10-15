"""Root readback of complete primitive families and every printed power-rule operation."""
import sys,json,re,hashlib,importlib.util,copy
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186064167;D=R.parents[2]/f'generate/scratch/{K}-draft';SCRIPT_SHA=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()
def module(name,path):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=module('root_monomial_scalar',R/'ode-scalar-parser.py');s=p.s;x=p.x;C=p.u;g=module('root_monomial_gen',D.with_suffix('.py'));DER=r'\frac{\text{d}}{\text{d}x}'
counts=dict(records=0,choices=0,full_banks=0,actual_integral_operands=0,formal_derivatives=0,primitive_and_identity_sides=0,derivative_sides=0,source_prompts=0,source_solutions=0,source_banks=0,source_values=0,source_keys=0,source_fieldless=0,inventory=0);tasks=set()
def expr(raw):return p.scalar(raw.strip().rstrip('.,').replace(r'\dfrac',r'\frac').replace(r'\displaystyle','').replace('C','u').replace('✓','').replace('&',''))
def family(a,b):return bool(s.diff(a,C)!=0)==bool(s.diff(b,C)!=0) and s.expand(s.diff(a-b,x))==0
def degree(prompt):
 if r'\int 1'in prompt:return 0
 if r'\intxdx'in prompt:return 1
 m=re.search(r'(?:\{x\}|x)\^(?:\{(\d+)\}|(\d+))',prompt);assert m,prompt;return int(m[1]or m[2])
def val(raw,n):
 raw=raw.strip().rstrip('.,').replace('&','').replace(r'\displaystyle','').replace(r'\dfrac',r'\frac').replace('✓','');primitive=x**(n+1)/s.Integer(n+1)+C
 raw=re.sub(r'\{F\}\^\{[′\']\}\(x\)',lambda _:s.latex(x**n),raw)
 raw=raw.replace('f(x)','('+s.latex(x**n)+')').replace('F(x)','('+s.latex(primitive).replace('u','C')+')')
 while DER in raw:
  at=raw.index(DER);start=at+len(DER);assert raw[start]=='(';end=start+1;depth=1
  while depth:depth+=(raw[end]=='(')-(raw[end]==')');end+=1
  derivative=s.diff(expr(raw[start+1:end-1]),x);raw=raw[:at]+'('+s.latex(derivative)+')'+raw[end:];counts['formal_derivatives']+=1
 while r'\int'in raw:
  at=raw.index(r'\int');tail=raw[at+4:];m=re.search(r'\\(?:text|textrm)\{d\}\s*x|\\textrm\s+d\s*x|dx',tail);assert m,(raw,n)
  operand=tail[:m.start()].replace(r'\,','').strip();assert s.expand(expr(operand)-x**n)==0,(operand,n);counts['actual_integral_operands']+=1;raw=raw[:at]+'('+s.latex(primitive).replace('u','C')+')'+tail[m.end():]
 return expr(raw)
def check(r):
 r=r.get('record',r);q=r['question'];n=degree(q[':question/problem']);primitive=x**(n+1)/s.Integer(n+1)+C;fs=q.get(':question/answer-fields',[])
 for f in fs:
  values=[expr(a[':answer/value'])for a in f[':answer-field/choices']];assert all(not family(v,w)for i,v in enumerate(values)for w in values[:i]);good=[a[':answer/id']for a,v in zip(f[':answer-field/choices'],values)if family(v,primitive)];assert len(good)==1
  if f.get(':answer-field/correct'):assert f[':answer-field/correct']==[':answer/id',good[0]]
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}'in q[':question/problem']
  counts['choices']+=len(values);counts['full_banks']+=int(len(values)==5)
  if len(values)==5 and r.get('generation'):
   profile=r.get('generation',{}).get('bank_profile')or'authored_power';profile=profile.replace('raw:q-','observed_');m=n+1
   if profile=='observed_2005':expected=[m*x**m,primitive,m+C,x**m/s.Integer(m),x**m+C]
   elif profile=='observed_2022':expected=[x**m+C,n*x**(n-1)+C,x**n/s.Integer(n)+C,primitive,x**(n-1)+C]
   elif profile=='observed_113665':expected=[primitive,m*x**(n-1)+C,x**m/s.Integer(n-1)+C,x**(n-1)/s.Integer(n-1)+C,n*x**m+C]
   elif profile=='observed_113668':expected=[x**(n-1)/s.Integer(n)+C,primitive,x**(n-1)/s.Integer(n-1)+C,x**m+C,n*x**m+C]
   elif profile=='observed_29994':expected=[n*x**m+C,x**n/s.Integer(n)+C,m*x**m+C,primitive,x**n/s.Integer(m)+C]
   else:expected=[primitive,x**m+C,x**n/s.Integer(m)+C,x**(m+1)/s.Integer(m+1)+C,m*x**m+C]
   assert all(sum(family(v,w)for v in values)==1 for w in expected),(profile,n,values,expected)
   counts['complete_recipe_banks']=counts.get('complete_recipe_banks',0)+1
 sol=q.get(':question/worked-solution','')
 if sol:
  blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)>=2
  for bi,block in enumerate(blocks):
   body=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
   for row in body.split(r'\\'):
    parts=[z.strip()for z in row.replace('&','').split('=')if z.strip()];assert parts,(row,sol)
    values=[val(z,n)for z in parts]
    if bi==len(blocks)-1:
     assert all(s.expand(v-x**n)==0 for v in values),(row,n,values);counts['derivative_sides']+=len(values)
    else:
     if all(s.expand(v-x**n)==0 for v in values):pass # Formal given F'=f.
     else:assert all(family(v,primitive)for v in values),(row,values,primitive)
     counts['primitive_and_identity_sides']+=len(values)
  assert "Let's check by differentiating:"in sol
 counts['records']+=1;tasks.add(n);return q
src=json.loads((D/'source.json').read_text())['record'];ma=[q for q in src[':knowledge-point/questions']if ':question/math-academy-id'in q]
for old in [src[':knowledge-point/canonical-example'],*ma]:
 sid=old[':question/math-academy-id'];r=g.generate('easy',profile='raw:'+sid);q=check(r);assert q[':question/problem']==old[':question/problem'];counts['source_prompts']+=1
 if old.get(':question/worked-solution'):assert q[':question/worked-solution']==old[':question/worked-solution'];counts['source_solutions']+=1
 if not old.get(':question/answer-fields'):assert not q.get(':question/answer-fields');counts['source_fieldless']+=1
 for f,of in zip(q.get(':question/answer-fields',[]),old.get(':question/answer-fields',[])):
  assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(a[':answer/value']for a in of[':answer-field/choices']);counts['source_banks']+=1;counts['source_values']+=len(f[':answer-field/choices'])
  if of.get(':answer-field/correct'):assert family(expr(of[':answer-field/correct'][':answer/value']),x**(degree(q[':question/problem'])+1)/s.Integer(degree(q[':question/problem'])+1)+C);counts['source_keys']+=1
for old in src[':knowledge-point/questions']:
 if ':question/math-academy-id'in old:continue
 q=copy.deepcopy(old);q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 for f in q[':question/answer-fields']:f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
 check({'question':q});counts['inventory']+=1
for r in json.loads((D/'review.json').read_text())+json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level in g.SUPPORTED_LEVELS:
 for n in range(21):
  for kind in (('blank',)if n==0 else('blank','radio')):check(g.generate(level,parameters={'n':n},template='constant'if n==0 else'function',field_type=kind))
for profile in g.BANK_PROFILES:
 for n in (9,17):check(g.generate('easy',parameters={'n':n},profile=profile))
assert tasks==set(range(21));batch=g.generate_batch('all',count=7,seed=23);assert len(batch)==len({r['generation']['mathematical_fingerprint']for r in batch})==21
base=g.generate('easy',parameters={'n':4});mutations=[(r'\frac{{x}^{4+1}}{4+1}',r'\frac{{x}^{4+2}}{4+1}'),(r'\frac{1}{5}\cdot 5',r'\frac{1}{5}\cdot 6')]
for old,new in mutations:
 bad=copy.deepcopy(base);text=bad['question'][':question/worked-solution'];assert old in text;bad['question'][':question/worked-solution']=text.replace(old,new,1)
 try:check(bad)
 except AssertionError:pass
 else:raise AssertionError('bad formal/intermediate step passed')
assert hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()==SCRIPT_SHA
proof={'status':'passed','script_sha256':SCRIPT_SHA,'source_and_readback':counts,'mathematical_tasks_total_across_all_levels':len(tasks),'scope':'Unit-coefficient nonnegative integer monomial power rule only;21actual integrands total, no coefficient/reciprocal/log extension. Moderate/hard share same allowed method and are explicitly uncalibrated authored labels, not claimed additional workload or63tasks.','native_limitations':'Current grader rejects24tested equivalent arbitrary-C blank families, documented and retained; no served math pruned.','database_writes':0};(R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(proof,indent=2)+'\n');print(proof)
