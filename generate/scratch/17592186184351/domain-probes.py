#!/usr/bin/env python3
"""Exact displayed log-absolute derivatives on negative-denominator intervals."""
import importlib.util,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('domain_validator',HERE/'validate.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
rows=[]
for k in range(2,8):
 for c in range(3,7):
  r=v.g.generate('hard',template='derivative_ratio',parameters=dict(k=k,c=c));q=r['question'];f=q[':question/answer-fields'][0]
  point=v.s.Rational(1,k);inner=v.s.exp(k*v.x)-k*c*v.x
  assert inner.subs(v.x,point).is_negative,'Probe must lie on negative denominator branch'
  displayed=next(b for b in v.p.blocks(q[':question/problem']) if r'\int' in b);integrand,var=v.read_integral(displayed)
  checks=[]
  for a in f[':answer-field/choices']:
   F=v.scalar(re.sub(r'\+\s*C\s*$','',a[':answer/value']))
   # SymPy's real-variable derivative retains sign(U)/Abs(U); exact evaluation
   # on U<0 independently verifies the custom U'/U chain rule, including the
   # original log(abs(U)) factor in the product rule of wrong options.
   assert v.s.simplify((v.derivative(F,var)-v.s.diff(F,var)).subs(var,point))==0
   difference=v.s.simplify((v.derivative(F,var)-integrand).subs(var,point))
   correct=a[':answer/id']==f[':answer-field/correct'][1]
   if correct:assert difference==0
   else:assert abs(complex(difference.evalf(50)))>1e-30
   checks.append({'displayed_answer':a[':answer/value'],'correct':correct,'chain_rule_exact':True,'ordinary_wrong_probe':'nonzero derivative difference at 50 digits' if not correct else None})
  rows.append({'parameters':{'k':k,'c':c},'point':str(point),'denominator':str(inner.subs(var,point)),'checks':checks})
(HERE/'domain-probes.json').write_text(json.dumps({'passed':True,'negative_branch_instances':len(rows),'exact_displayed_derivative_comparisons':5*len(rows),'correct_primitive_probes':len(rows),'ordinary_wrong_probes':4*len(rows),'rows':rows},indent=2)+'\n')
print('Negative branches:',len(rows),'instances;',len(rows)*5,'exact displayed derivative comparisons')
