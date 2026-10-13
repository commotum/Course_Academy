"""Parent source fidelity and alternative affine-span classification oracle."""
import importlib.util,json
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;S=R.parents[2]/'generate/scratch/17592186087867';kp=17592186087867
spec=importlib.util.spec_from_file_location('parent_linear_ode',S.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def linear(eq):
 if eq.has(g.D2):return False
 result=s.solve(eq,g.D)
 if len(result)!=1 or result[0].has(g.D):return False
 f=result[0]
 # Compare with the affine interpolation itself, independently of generator's
 # derivative-coefficient and second-derivative test.
 if f.subs(g.Y,0).has(s.zoo,s.oo,s.nan):return False
 affine=f.subs(g.Y,0)+(f.subs(g.Y,1)-f.subs(g.Y,0))*g.Y
 return s.simplify(f-affine)==0
n=dict(source_banks=0,source_values=0,source_designations=0,source_solutions_exact=0,supported_solution_repairs=0,displayed_banks=0)
def check(r):
 q=r['question'];f=q[':question/answer-fields'][0];target='**NOT**' not in q[':question/problem'];valid=[]
 for a in f[':answer-field/choices']:
  residual=g.read_equation(a[':answer/value'])
  if linear(residual)==target:valid.append(a[':answer/id'])
 assert valid==[f[':answer-field/correct'][1]],(q,valid)
raw=json.loads((R/'sources'/f'{kp}.json').read_text())['record'];qs={q[':question/math-academy-id']:q for q in raw[':knowledge-point/questions']}
for c in json.loads((S/'source-cases.json').read_text()):
 old=qs[c['source_id']];r=g.generate(g.TEMPLATES[c['template']]['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);check(r);q=r['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
 assert q[':question/problem']==old[':question/problem'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);n['source_banks']+=1;n['source_values']+=5
 correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct[':answer/value']==of[':answer-field/correct'][':answer/value'];n['source_designations']+=1
 expected=old[':question/worked-solution']
 if c['source_id']=='q-79750':expected=expected.replace('right-hand side depends on $y.$','right-hand side depends on $y$ through the nonlinear term $y^2.$');n['supported_solution_repairs']+=1
 else:n['source_solutions_exact']+=1
 assert q[':question/worked-solution']==expected
for name,t in g.TEMPLATES.items():
 for seed in range(10):check(g.generate(t['level'],seed,template=name));n['displayed_banks']+=1
(R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
