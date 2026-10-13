"""Parent independent classification of displayed inhibited-decay equations."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
R=Path(__file__).resolve().parent;S=R.parents[2]/'generate/scratch/17592186078582';kp=17592186078582
spec=importlib.util.spec_from_file_location('parent_decay',S.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
y=s.Symbol('y',real=True)
def parse(t):
 rhs=t.split('=',1)[1];init=None
 if r',\,y(0)=' in rhs:rhs,init=rhs.split(r',\,y(0)=');init=s.Rational(init.replace(r'\,',''))
 return parse_expr(rhs.replace('^','**').replace(r'\,','').replace('{','(').replace('}',')'),local_dict={'y':y},transformations=standard_transformations+(implicit_multiplication_application,rationalize)),init
def check(r):
 q=r['question'];f=q[':question/answer-fields'][0];threshold=re.search(r'\$y\s*>\s*(\d+)\$',q[':question/problem']);valid=[]
 for ans in f[':answer-field/choices']:
  rhs,init=parse(ans[':answer/value']);poly=s.Poly(s.expand(rhs),y)
  if poly.degree()!=1:continue
  slope=poly.coeff_monomial(y);intercept=poly.coeff_monomial(1)
  if slope>=0:continue
  equilibrium=-intercept/slope
  if init is not None and init>equilibrium or init is None and equilibrium==s.Integer(threshold[1]):valid.append(ans[':answer/id'])
 assert valid==[f[':answer-field/correct'][1]],(q,valid)
raw=json.loads((R/'sources'/f'{kp}.json').read_text())['record'];qs={q[':question/math-academy-id']:q for q in raw[':knowledge-point/questions']};n={'source_banks':0,'source_values':0,'source_designations':0,'source_solutions':0,'displayed_classifications':0}
for c in json.loads((S/'source-cases.json').read_text()):
 old=qs[c['source_id']];r=g.generate(c['level'],parameters=c['parameters'],profile=c['bank_profile']);check(r);q=r['question'];assert q[':question/problem']==old[':question/problem']
 of=old[':question/answer-fields'][0];f=q[':question/answer-fields'][0];assert sorted(t[':answer/value'] for t in f[':answer-field/choices'])==sorted(t[':answer/value'] for t in of[':answer-field/choices']);n['source_banks']+=1;n['source_values']+=5
 if ':answer-field/correct' in of:
  chosen=next(t for t in f[':answer-field/choices'] if t[':answer/id']==f[':answer-field/correct'][1]);assert chosen[':answer/value']==of[':answer-field/correct'][':answer/value'];n['source_designations']+=1
 if ':question/worked-solution' in old:assert q[':question/worked-solution']==old[':question/worked-solution'];n['source_solutions']+=1
for level in ('easy','moderate','hard'):
 for seed in range(40):check(g.generate(level,seed));n['displayed_classifications']+=1
(R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
