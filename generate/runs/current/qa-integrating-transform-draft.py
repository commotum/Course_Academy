"""Root actual linear ODE/product-equation banks and factor/multiplication stages."""
import importlib.util,itertools,json,re,sys,hashlib
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186087877;D=R.parents[2]/f'generate/scratch/{K}-draft'
def mod(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m
p=mod('root_factor_transform_parser',R/'integrating-factor-parser.py');g=mod('root_factor_transform_generator',D.with_suffix('.py'));F=mod('root_factor_transform_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(g,K,D);x=p.x;y=p.y;YP=p.YP
C=dict(records=0,actual_odes=0,values=0,whole_banks=0,pairs=0,factor_inputs=0,factor_definitions=0,named_coefficients=0,equation_rows=0,integrating_factor_rows=0,multiplication_stages=0,distribution_stages=0,product_derivative_inputs=0,prose_factor_references=0,domain_guards=0,raw_duplicate_banks=0,raw_malformed_operators=0,raw_sign_errors=0)
def eq(a,b):return p.positive_equal(a,b)
def factor(v):
 lhs,rhs=v.split('=');prefix=next(z for z in (r'\frac{d}{dx}',r'\frac{\text{d}}{\text{d}x}') if lhs.startswith(z));body=p.scalar(lhs[len(prefix):]);I=s.expand(body).coeff(y);assert eq(body,I*y) and I!=0;return I
def check(r,raw=False):
 q,m=r['question'],r['generation'];t=m['template'];prompt=q[':question/problem'];P,Q=p.ode(prompt);C['actual_odes']+=1;field=q[':question/answer-fields'][0];values=field[':answer-field/choices'];assert len(values)==5
 parsed=[];factors=[]
 for a in values:
  v=a[':answer/value'].replace(r'\operatorname{ln}',r'\ln').replace('⁡','').replace(r'\u2061','')
  if raw and r'\ln|' in v:
   assert t=='linear_sin' and r'\ln|2x|' in v;v=v.replace(r'\ln|2x|',r'\ln(2x)') # raw branch read on x>0 only; original bytes checked separately
  if r'\frac{d}{dx^{2}}' in v:assert raw and m['evidence_only'];parsed.append(None);factors.append(None);C['raw_malformed_operators']+=1
  else:parsed.append(p.transformed(v));factors.append(factor(v))
 good=[v is not None and eq(v[0],P) and eq(v[1],Q) for v in parsed];assert sum(good)==1
 if ':answer-field/correct' in field:assert next(z for z,a in zip(good,values) if a[':answer/id']==field[':answer-field/correct'][1])
 pairs=[(a,b) for a,b in itertools.combinations(parsed,2) if a is not None and b is not None]
 duplicates=sum(all(eq(z,w) for z,w in zip(a,b)) for a,b in pairs)
 if raw:C['raw_duplicate_banks']+=bool(duplicates)
 else:assert not duplicates;C['pairs']+=len(pairs)
 sol=q.get(':question/worked-solution')
 if sol:
  if raw and t=='signed_constant_power':
   old=sol;sol=sol.replace(r'+\frac{1}{2}{e}^{-x/2}',r'-\frac{1}{2}{e}^{-x/2}');assert old!=sol;C['raw_sign_errors']+=1
  for key,n in p.stages(sol,P,Q).items():C[key]=C.get(key,0)+n
  # The factor-definition row and actual integral-input row are separately read.
  blocks=p.p.blocks(sol);ib=next(b for b in blocks if p.p.clean(b).startswith('I(x)') and r'\int' in b)
  rows=p.p.clean(ib).split(r'\\');assert len(rows)>=3
  first=rows[0].split('=')[-1];assert r'\int P(x)' in first;C['factor_definitions']+=1
  second=rows[1].split('=')[-1].replace(r'\text{d}x','dx').replace(r'\mathrm{d}x','dx');match=re.search(r'\\int\s*(.*?)(?:\\,)?\s*dx',second);assert match,second;assert eq(p.scalar(match[1]),P);C['factor_inputs']+=1
  I=p.integrating_stage(rows[-1].split('=')[-1],P);assert eq(s.diff(I,x),P*I)
  # Read the given P,Q once more from actual operative inline bindings.
  named={name:p.scalar(body) for name,body in re.findall(r'\$(P|Q)\(x\)=(.*?)\$',sol)};assert set(named)=={'P','Q'} and eq(named['P'],P) and eq(named['Q'],Q)
  reference=re.search(r'multiply our differential equation through by \$I\(x\)=(.*?)\$',sol);assert reference and eq(p.scalar(reference[1]),I);C['prose_factor_references']+=1
  if not raw:
   mulblock=next(b for b in blocks if r'\begin{aligned}' in b and len(p.p.clean(b).split(r'\\'))==2 and r'\frac{dy}{dx}' in b and r'\int' not in b)
   multiply,distribute=p.p.clean(mulblock).split(r'\\');assert raw or r'\cdot \left(\frac{dy}{dx}' in multiply and r'\cdot \frac{dy}{dx}' in distribute and ('+' in distribute or '-' in distribute);C['multiplication_stages']+=1;C['distribution_stages']+=1
  final=next(b for b in reversed(blocks) if p.p.clean(b).startswith((r'\frac{d}{dx}',r'\frac{\text{d}}{\text{d}x}')))
  actual=p.expanded_equation(p.p.clean(final));assert all(eq(a,b) for a,b in zip(actual,(P,Q))) and eq(factor(p.p.clean(final)),I);C['product_derivative_inputs']+=1
 if not raw:
  assert m['eligible_for_learning'] and not m['evidence_only'];H=s.integrate(P,x);I=s.exp(H);domain=m['domain']
  if t in ('scaled_reciprocal_cos','reciprocal_exp','scaled_reciprocal_rhs'):
   k=s.simplify(P*x);assert k.is_Integer and k!=0 and not k.has(x);I=x**k;expected=[I,x**(2*k),s.exp(k*x),s.exp(-k*x),s.log(x)]
  elif t=='linear_sin':
   a=s.simplify(P/(2*x));assert not a.has(x) and a!=0;expected=[s.log(abs(2*a)*x),x**2,s.exp(2*a*x),2*a*x,s.exp(a*x**2)]
  elif t in ('linear_exp','polynomial_transform'):
   degree=s.degree(H,x);a=s.expand(H).coeff(x,degree);expected=[I,1/I,s.exp(P),s.exp(a*x**(degree-1)),x**degree]
  else:expected=[I,1/I,s.exp(2*H),H,s.exp(P)]
  assert all(sum(eq(actual[0],s.diff(E,x)/E) and eq(actual[1],Q) for actual in parsed)==1 for E in expected);C['whole_banks']+=1
  if domain=='x>0':assert any(re.search(r'x\s*>\s*0',b) for b in p.p.blocks(prompt));C['domain_guards']+=1
  else:assert domain=='x in R' and not P.has(s.log(x),1/x)
  assert r'\int' not in ''.join(a[':answer/value'] for a in values) and not any('C' in b or re.match(r'y\s*=',p.p.clean(b)) for b in p.p.blocks(sol))
 C['values']+=5;C['records']+=1
for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):check(r)
for t,(level,sid) in g.TEMPLATES.items():
 for seed in (29,37,257):check(g.generate(level,seed,template=t))
for c in json.loads((D/'source-cases.json').read_text()):check(g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c.get('profile',c.get('bank_profile'))),True)
for t,(l,sid) in g.TEMPLATES.items():
 for call in (g.generate,g._generate_normal):
  try:call(l,template=t,profile='observed_raw')
  except ValueError:pass
  else:raise AssertionError('legacy eligibility bypass')
result=dict(status='passed',source=fidelity,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
