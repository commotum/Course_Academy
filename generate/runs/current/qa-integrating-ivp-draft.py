"""Root actual ODE/initial-condition, complete two-field banks and operative stages."""
import importlib.util,itertools,json,re,sys,hashlib
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186087879;D=R.parents[2]/f'generate/scratch/{K}-draft'
def mod(n,path):
 z=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(z);sys.modules[n]=m;z.loader.exec_module(m);return m
p=mod('root_ivp_math',R/'integrating-factor-parser.py');g=mod('root_ivp_draft',D.with_suffix('.py'));F=mod('root_ivp_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(g,K,D);x=p.x;C=p.C
T=dict(records=0,actual_odes=0,actual_conditions=0,values=0,factor_banks=0,solution_banks=0,factor_pairs=0,solution_pairs=0,prose_conditions=0,factor_inputs=0,product_derivative_stages=0,general_families=0,substitution_definitions=0,domain_guards=0,raw_duplicate_banks=0,raw_missing_solutions=0)
def eq(a,b):return p.positive_equal(a,b)
def check(r,raw=False):
 q,m=r['question'],r['generation'];P,Q=p.ode(q[':question/problem']);t,h=p.initial(q[':question/problem']);T['actual_odes']+=1;T['actual_conditions']+=1;fields={f[':answer-field/key']:f for f in q[':question/answer-fields']};assert set(fields)=={'field-1','field-2'}
 I=s.exp(s.integrate(P,x));F=s.integrate(s.expand(I*Q),x);c=s.simplify(h*I.subs(x,t)-F.subs(x,t));answer=s.simplify((F+c)/I)
 for key,f in fields.items():
  vals=[p.scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert f[':answer-field/type']==':answer-field.type/select';T['values']+=len(vals)
  factor=(key=='field-1');good=[v!=0 and eq(s.diff(v,x),P*v) if factor else eq(s.diff(v,x)+P*v,Q) and eq(v.subs(x,t),h) for v in vals]
  if ':answer-field/correct' in f:assert next(z for z,a in zip(good,f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
  duplicates=0
  for a,b in itertools.combinations(vals,2):
   same=not s.simplify(a/b).has(x) and a!=0 and b!=0 if factor else eq(a,b);duplicates+=same
   if not raw:assert not same;T['factor_pairs' if factor else 'solution_pairs']+=1
  if raw:T['raw_duplicate_banks']+=bool(duplicates)
  else:
   assert sum(good)==1
   if factor:
    family=g.TEMPLATES[m['template']][1]
    if family in ('nonstandard','cosine'):expected=[I,1/I,s.exp(x),P]
    elif family=='sine':expected=[I,1/I,s.exp(x),s.log(x)]
    else:expected=[I,1/I,s.integrate(P,x),I**2]
    assert len(vals)==4 and all(sum(not s.simplify(v/e).has(x) and v!=0 for v in vals)==1 for e in expected);T['factor_banks']+=1
   else:
    if m['template']=='q-335811' and c==0:expected=[answer,-answer,F*I,F/x,F*x]
    else:expected=[answer,(F-c)/I,c/I,F+c,F/I+c]
    if m['template']=='q-335810':expected=expected[:4]
    assert len(vals)==len(expected) and all(sum(eq(v,e) for v in vals)==1 for e in expected);T['solution_banks']+=1
 sol=q.get(':question/worked-solution')
 if sol:
  given=re.search(r'initial condition \$y\((.*?)\)=(.*?)\$',sol);assert given and eq(p.scalar(given[1]),t) and eq(p.scalar(given[2]),h);T['prose_conditions']+=1
  for key,n in p.stages(sol,P,Q,True).items():T[key]=T.get(key,0)+n
  T['antiderivative_rows']=T.get('antiderivative_rows',0)+p.antiderivative_rows(sol,P,Q)
  for key,n in p.initial_rows(sol,P,Q,t,h).items():T[key]=T.get(key,0)+n
  if not raw:
   blocks=p.p.blocks(sol);ib=next(b for b in blocks if p.p.clean(b).startswith('I(x)') and r'\int' in b);rr=p.p.clean(ib).split(r'\\');assert len(rr)>=3 and r'\int P(x)' in rr[0]
   rhs=rr[1].split('=')[-1].replace(r'\text{d}x','dx');v=re.search(r'\\int\s*(.*?)(?:\\,)?\s*dx',rhs);assert v and eq(p.scalar(v[1]),P);T['factor_inputs']+=1
   mul=next(b for b in blocks if p.p.clean(b).count(r'\\')==2 and r'\int' not in b and r'\frac{\text{d}y}{\text{d}x}' in b and r'\frac{\text{d}}{\text{d}x}' in b);rr=p.p.clean(mul).split(r'\\');assert r'\cdot (\frac{\text{d}y}{\text{d}x}' in rr[0] and r'\cdot \frac{\text{d}y}{\text{d}x}' in rr[1];T['product_derivative_stages']+=1
   # General family has a nonzero arbitrary-constant coefficient, and a correct
   # primitive with exactly one +C before division; no selected particular-only shortcut.
   general=next(b for b in blocks if r'\int' in b and 'C' in b and 'y' in b);rr=p.p.clean(general).split(r'\\');assert rr[0].count(r'\int')==2 and any('+C' in row for row in rr)
   last=rr[-1];lhs,right=last.split('=');assert lhs.strip()=='y';Y=p.scalar(right);assert s.diff(Y,C)!=0 and eq(s.diff(Y,x)+P*Y,Q);T['general_families']+=1
   if m['template'] in ('q-335808','q-339145','hard_cubic'):
    u=next(b for b in blocks if b.startswith('u='));U=p.scalar(u.split('=')[1].rstrip(':'));assert eq(s.diff(U,x),P);assert len(rr)==5 and r'\text{d}u' in rr[1] and 'e^u+C' in rr[2] and '+C' in rr[3];T['substitution_definitions']+=1
 else:assert raw and m['template']=='q-334916';T['raw_missing_solutions']+=1
 if not raw:
  assert m.get('eligible_for_learning',m.get('eligible')) and not m['evidence_only']
  if m['domain']=='x>0':assert t>0 and any(re.search(r'x\s*>\s*0',b) for b in p.p.blocks(q[':question/problem']));T['domain_guards']+=1
  else:assert m['domain']=='real x' and not P.has(1/x,s.log(x))
 T['records']+=1
for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):check(r)
for template,(level,family) in g.TEMPLATES.items():
 for seed in (37,271):check(g.generate(level,seed,template=template))
for c in json.loads((D/'source-cases.json').read_text()):check(g.generate(c.get('level',c.get('difficulty')),template=c['template'],parameters=c['parameters'],profile=c.get('profile',c.get('bank_profile'))),True)
result=dict(status='passed',source=fidelity,readback=T,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
