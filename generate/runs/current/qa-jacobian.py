"""Parent checks immutable banks and derivatives of displayed transformations."""
import importlib.util,itertools,json,re
from pathlib import Path
import sympy as sp
R=Path(__file__).resolve().parent;F=R.parents[2]/'generate/scratch/17592186129187'
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=module('parent_jacobian',F.with_suffix('.py'));p=module('parent_scalar_parser',F/'math_parser.py')
def inputs(prompt):
 matches=re.findall(r'\\begin\{(?:bmatrix|aligned)\}(.*?)\\end\{(?:bmatrix|aligned)\}',prompt)
 return [p.parse(x) for x in matches[-1].split(r'\\')]
def equal(a,b):return sp.simplify(sp.trigsimp(a-b))==0
def check(r):
 x,y=inputs(r['question'][':question/problem']);expected=sp.diff(x,p.u)*sp.diff(y,p.v)-sp.diff(x,p.v)*sp.diff(y,p.u)
 f=r['question'][':question/answer-fields'][0]
 for answer in f[':answer-field/choices']:
  assert equal(p.parse(answer[':answer/value']),expected)==(answer[':answer/id']==f[':answer-field/correct'][1])
 return expected
source=json.loads((R/'sources/17592186129187.json').read_text())['record'];qs={q[':question/math-academy-id']:q for q in source[':knowledge-point/questions']}
counts={'source_banks':0,'source_values':0,'source_designations':0,'sampled_transformations':0,'hard_parameter_grid':0}
for c in json.loads((F/'source-cases.json').read_text()):
 s=qs[c['source_id']];r=g.generate(g.TEMPLATES[c['template']][0],24,c['template'],parameters=c['parameters'],profile=c['bank_profile']);check(r)
 assert all(equal(a,b) for a,b in zip(inputs(s[':question/problem']),inputs(r['question'][':question/problem'])))
 sf=s[':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0];remaining=[p.parse(a[':answer/value']) for a in f[':answer-field/choices']]
 for a in sf[':answer-field/choices']:
  matches=[i for i,b in enumerate(remaining) if equal(p.parse(a[':answer/value']),b)]
  assert len(matches)==1;remaining.pop(matches[0]);counts['source_values']+=1
 assert not remaining
 if ':answer-field/correct' in sf:
  a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert equal(p.parse(a[':answer/value']),p.parse(sf[':answer-field/correct'][':answer/value']));counts['source_designations']+=1
 counts['source_banks']+=1
for level in ('easy','moderate','hard'):
 for seed in range(30):check(g.generate(level,seed));counts['sampled_transformations']+=1
for a,b in itertools.product(range(1,4),repeat=2):
 for m,n in ((3,2),(2,3),(3,3)):
  for i,j,k,l in itertools.product((1,2),repeat=4):
   pars=dict(a=a,b=b,m=m,n=n,p=i,q=j,r=k,s=l)
   r=g.generate('hard',parameters=pars)
   expected=-a*b*m*n*(i*l+j*k)*(i*p.u+j*p.v)**(m-1)*(k*p.u-l*p.v)**(n-1)
   assert equal(check(r),expected);counts['hard_parameter_grid']+=1
(R/'qa/17592186129187-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(json.dumps(counts))
