"""Parent oracle: read the displayed IVP, not the generator's math metadata."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent; K=17592186100893; S=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('parent_ivp',S.with_suffix('.py'));p=module('parent_ivp_parser',S/'parse_math.py')
X,Y=p.X,p.Y
def zero(e):return e==0 or s.trigsimp(s.simplify(e))==0
def read(prompt):
 maths=re.findall(r'(?<!\$)\$([^$]*)\$(?!\$)',prompt)
 derivatives=[v for v in maths if r'\frac{\text{d}y}{\text{d}x}' in v or '′' in v or "y'" in v]
 assert len(derivatives)==1,prompt
 ode=derivatives[0].replace(r'\frac{\text{d}y}{\text{d}x}','C').replace('{y}^{′}','C').replace("y'",'C')
 left,right=p.relation(ode);rhs=s.solve(left-right,p.C)
 assert len(rhs)==1
 initial=next(v for v in maths if re.match(r'y\(',v))
 match=re.fullmatch(r'y\((.*?)\)\s*=\s*(.*)',initial.rstrip('.,'))
 assert match,initial
 x0,y0=map(p.expression,match.groups())
 return rhs[0],x0,y0
def lhs_for_blank(prompt):
 fragment=re.findall(r'(?<!\$)\$([^$]*)\$(?!\$)',prompt)[-1].rstrip('.,')
 assert fragment.endswith('=')
 return Y if fragment[:-1] in ('y(x)','y') else p.expression(fragment[:-1])
def valid_curve(curve,ode,x0,y0):
 lhs,rhs=curve
 if not zero(lhs.subs(Y,y0)-rhs.subs(X,x0)):return False
 if lhs==Y:
  residual=s.diff(rhs,X)-ode.subs(Y,rhs)
  # ln(exp(sqrt(...))) simplifies on the positive-real local IVP branch.
  residual=residual.replace(lambda z:z.func==s.log and z.args[0].func==s.exp,lambda z:z.args[0].args[0])
  residual=s.powdenest(residual,force=True)
 else:residual=s.diff(lhs,Y)*ode-s.diff(rhs,X)
 return zero(residual)
def check(record):
 q=record['question'];prompt=q[':question/problem'];f=q[':question/answer-fields'][0]
 if 'previous part' in prompt:
  # The original dependent item has no standalone differential equation.
  # Default must supply the given general solution; replay is audited against
  # the original worked model, preserving the explicit dependency.
  ambient=p.expression(re.search(r'T=([^+]+)\+K',prompt)[1]) if 'general solution' in prompt else s.Integer(25)
  ode=-s.Rational(3,100)*(Y-ambient);x0=s.Integer(0)
  y0=p.expression(re.search(r'T\}\(0\)=([^$]+)',prompt)[1].rstrip('.,'))
  for a in f[':answer-field/choices']:
   v=p.expression(a[':answer/value']).subs(p.T,X)
   assert valid_curve((Y,v),ode,x0,y0)
  return
 ode,x0,y0=read(prompt); matches=[]
 for a in f[':answer-field/choices']:
  lhs,rhs=p.relation(a[':answer/value']);lhs=lhs if lhs is not None else lhs_for_blank(prompt)
  if valid_curve((lhs,rhs),ode,x0,y0):matches.append(a[':answer/id'])
 assert matches==[f[':answer-field/correct'][1]],(prompt,matches)
def normalized_tex_spaces(text):return re.sub(r'\\pi\s+}',r'\\pi}',text)
n={'source_questions':0,'source_values':0,'complete_radio_banks':0,'blanks':0,'exact_prompts':0,'exact_worked_solutions':0,'tex_space_normalized_prompts':0,'tex_space_normalized_solutions':0,'source_designations':0,'displayed_default_questions':0}
raw=json.loads((R/'sources'/f'{K}.json').read_text())['record'];qs={q[':question/math-academy-id']:q for q in raw[':knowledge-point/questions']}
for c in json.loads((S/'source-cases.json').read_text()):
 old=qs[c['source_id']];r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);check(r)
 q=r['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
 assert normalized_tex_spaces(q[':question/problem'])==normalized_tex_spaces(old[':question/problem'])
 n['exact_prompts' if q[':question/problem']==old[':question/problem'] else 'tex_space_normalized_prompts']+=1
 assert normalized_tex_spaces(q[':question/worked-solution'])==normalized_tex_spaces(old[':question/worked-solution'])
 n['exact_worked_solutions' if q[':question/worked-solution']==old[':question/worked-solution'] else 'tex_space_normalized_solutions']+=1
 bank=[p.relation(a[':answer/value']) for a in f[':answer-field/choices']]
 for a in of[':answer-field/choices']:
  target=p.relation(a[':answer/value']);hits=[i for i,b in enumerate(bank) if p.equivalent(target,b)];assert len(hits)==1
  bank.pop(hits[0]);n['source_values']+=1
 assert not bank
 expected=p.relation(of[':answer-field/correct'][':answer/value'])
 actual=p.relation(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))
 assert p.equivalent(expected,actual);n['source_designations']+=1
 assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'] and f[':answer-field/key']==of[':answer-field/key']
 n['source_questions']+=1;n['complete_radio_banks' if f[':answer-field/type'].endswith('/radio') else 'blanks']+=1
for name,t in g.TEMPLATES.items():
 for seed in range(8):check(g.generate(t['level'],seed,template=name));n['displayed_default_questions']+=1
a=g.generate('moderate',template='source_347853',parameters={'h':0})
b=g.generate('moderate',template='reciprocal_initial',parameters={'h':0,'a':2,'b':2})
assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
assert a['question'][':question/id']!=b['question'][':question/id']
n['semantic_cross_template_deduplication']='passed'
(R/'qa'/f'{K}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
