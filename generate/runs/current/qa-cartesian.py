"""Parent oracle reconstructs equations and exact x images from printed curves."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186100889;S=R.parents[2]/f'generate/scratch/{K}'
sys.path.insert(0,str(S))
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('parent_cartesian',S.with_suffix('.py'));p=module('parent_cartesian_parser',S/'validate.py');X,Y,T=p.X,p.Y,p.T
def eq(a,b):return s.simplify(a-b)==0
def image(xt,td):
 if td==s.S.Reals:
  assert s.degree(xt,T)==1 and s.diff(xt,T)!=0;return s.S.Reals
 if isinstance(td,s.Interval):
  assert td.end==s.oo and td.start>=0
  lo=s.simplify(xt.subs(T,td.start));assert s.limit(xt,T,s.oo)==s.oo
  assert all(s.diff(xt,T).subs(T,td.start+d)>0 for d in (s.Rational(1,10),1,10))
  return s.Interval(lo,s.oo,left_open=td.left_open)
 excluded=td.args[1]
 if xt.is_polynomial(T) and s.degree(xt,T)==2:
  a,b,c=s.Poly(xt,T).all_coeffs();assert a>0
  vertex=-b/(2*a);lo=xt.subs(T,vertex)
  # All captured quadratic exclusions remove only the vertex.
  assert excluded==s.FiniteSet(vertex)
  return s.Interval.open(lo,s.oo)
 numerator,denominator=s.fraction(s.cancel(xt));assert s.degree(numerator,T)<=1 and s.degree(denominator,T)<=1
 bad=[s.simplify(xt.subs(T,z)) for z in excluded if denominator.subs(T,z)!=0]
 if s.degree(denominator,T)==1:
  a,b=s.Poly(numerator,T).all_coeffs() if s.degree(numerator,T)==1 else (0,numerator)
  c,d=s.Poly(denominator,T).all_coeffs();assert a*d-b*c!=0;bad.append(s.Rational(a,c))
 return s.Complement(s.S.Reals,s.FiniteSet(*bad),evaluate=False)
def read(r,raw=False):
 q=r['question'];xt,yt,parts=p.displayed_parameterization(q);td=p.domain_from_prompt(parts);xd=image(xt,td)
 fields=q[':question/answer-fields']
 # Pull collections do not order fields; the prompt's named slots do.
 f=next((f for f in fields if f[':answer-field/key']=='field-1'),fields[0])
 if f[':answer-field/type'].endswith('/radio'):
  truth=[]
  for a in f[':answer-field/choices']:
   obj,domain=p.answer_object(a[':answer/value']);assert len(obj)==2
   if eq(obj[0].subs({X:xt,Y:yt}),obj[1].subs({X:xt,Y:yt})):truth.append(a[':answer/id'])
  assert f[':answer-field/correct'][1] in truth
  if not raw:assert truth==[f[':answer-field/correct'][1]],(q[':question/problem'],truth)
  selected=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  range_text=selected.split(',',1)[1] if ',' in selected else ''
 else:
  v=p.e(f[':answer-field/choices'][0][':answer/value'])
  residual=s.refine(v.subs(X,xt)-yt,s.Q.nonnegative(T-td.start)) if isinstance(td,s.Interval) else v.subs(X,xt)-yt
  assert eq(residual,0),(q[':question/problem'],v,xt,yt,residual)
  range_text=q[':question/problem'].split('{{field-1}}',1)[1]
  for field in q[':question/answer-fields']:range_text=range_text.replace('{{'+field[':answer-field/key']+'}}',field[':answer-field/choices'][0][':answer/value'])
 shown=p.range_from_text(range_text)
 if not raw:assert shown==xd,('actual Cartesian image',shown,xd,q[':question/problem'])
 # Check all printed isolation/substitution/factoring rows against the printed
 # parametric curve, including non-final stages and domain-derived blanks.
 steps=0
 for a,b,row in p.equations_in_solution(q[':question/worked-solution']):
  assert eq(a.subs({X:xt,Y:yt}),b.subs({X:xt,Y:yt})),row;steps+=1
 return xt,yt,td,xd,steps
n={'source_questions':0,'source_values':0,'source_designations':0,'raw_exact_prompts':0,'raw_exact_existing_solutions':0,'repaired_source_instances':0,'displayed_default_questions':0,'displayed_worked_rows':0,'known_source_ambiguities':['q-15678: two equivalent correct equations'],'known_source_range_errors':['q-6828: x>5 required']}
raw=json.loads((R/'sources'/f'{K}.json').read_text())['record'];qs={q[':question/math-academy-id']:q for q in raw[':knowledge-point/questions']}
for c in json.loads((S/'source-cases.json').read_text()):
 old=qs[c['source_id']];r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='raw_observed');_,_,_,_,steps=read(r,True);n['displayed_worked_rows']+=steps
 q=r['question'];assert q[':question/problem']==old[':question/problem'];n['raw_exact_prompts']+=1
 if ':question/worked-solution' in old:
  assert q[':question/worked-solution']==old[':question/worked-solution'];n['raw_exact_existing_solutions']+=1
 for of,f in zip(old[':question/answer-fields'],q[':question/answer-fields']):
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);n['source_values']+=len(of[':answer-field/choices'])
  assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident']
  if ':answer-field/correct' in of:
   assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];n['source_designations']+=1
 normal=g.generate(c['level'],template=c['template'],parameters=c['parameters']);read(normal);n['repaired_source_instances']+=1;n['source_questions']+=1
for name,t in g.TEMPLATES.items():
 for seed in range(8):
  _,_,_,_,steps=read(g.generate(t['level'],seed,template=name));n['displayed_default_questions']+=1;n['displayed_worked_rows']+=steps
(R/'qa'/f'{K}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
