"""Parent derivative/point oracle reads functions from displayed questions."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;S=R.parents[2]/'generate/scratch/17592186096841';kp=17592186096841
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
g=module('parent_polynomial',S.with_suffix('.py'));p=module('parent_polynomial_parser',S/'validate.py')
def eq(a,b):return s.expand(a-b)==0
def expected(prompt):
 if 'f(x)' in prompt:
  fn=p.parse(re.search(r'f\(x\)\s*=\s*([^$]+)',prompt)[1].rstrip('.,'));v=s.Symbol('x')
 else:fn=p.parse(re.search(r'\[(.*?)\]',prompt)[1]);v=s.Symbol('t')
 d=s.diff(fn,v)
 if 'slope' in prompt or 'tangent' in prompt:
  point=re.search(r'\$\(([^$]+?)\)\.?\$',prompt);z,y=map(p.parse,point[1].split(','));assert eq(fn.subs(v,z),y)
  m=d.subs(v,z)
  return m*v+y-m*z if 'tangent' in prompt else m
 return d
def check(r):
 q=r['question'];correct=expected(q[':question/problem']);f=q[':question/answer-fields'][0]
 vals=[(a[':answer/id'],p.parse(a[':answer/value'].split('=',1)[-1])) for a in f[':answer-field/choices']]
 assert [aid for aid,a in vals if eq(a,correct)]==[f[':answer-field/correct'][1]]
 return vals
n=dict(source_questions=0,radio_banks=0,blank_layouts=0,source_values=0,source_designations=0,displayed_default_questions=0)
raw=json.loads((R/'sources'/f'{kp}.json').read_text())['record'];qs={q[':question/math-academy-id']:q for q in raw[':knowledge-point/questions']}
for c in json.loads((S/'source-cases.json').read_text()):
 old=qs[c['source_id']];r=g.generate(g.TEMPLATES[c['template']][0],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);check(r);q=r['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
 assert eq(expected(q[':question/problem']),expected(old[':question/problem']))
 assert p.skeleton(q[':question/problem'])==p.skeleton(old[':question/problem'])
 if ':question/worked-solution' in old:assert p.skeleton(q[':question/worked-solution'])==p.skeleton(old[':question/worked-solution'])
 bank=[t for _,t in check(r)]
 for a in of[':answer-field/choices']:
  val=p.parse(a[':answer/value'].split('=',1)[-1]);found=[i for i,b in enumerate(bank) if eq(val,b)];assert len(found)==1;bank.pop(found[0]);n['source_values']+=1
 assert not bank
 if ':answer-field/correct' in of:
  assert eq(expected(q[':question/problem']),p.parse(of[':answer-field/correct'][':answer/value'].split('=',1)[-1]));n['source_designations']+=1
 assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident']
 n['source_questions']+=1;n['radio_banks' if f[':answer-field/type'].endswith('/radio') else 'blank_layouts']+=1
for name,t in g.TEMPLATES.items():
 for seed in range(12):check(g.generate(t[0],seed,template=name));n['displayed_default_questions']+=1
(R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
