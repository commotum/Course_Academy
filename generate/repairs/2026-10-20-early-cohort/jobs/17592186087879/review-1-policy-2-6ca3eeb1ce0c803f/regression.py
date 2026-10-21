"""Strict regression: same-method easy coefficient change must be supported.
Run: PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python regression.py
Expected on reviewed package: exit 1, with regression-results.json retaining failure.
"""
import sys,json
sys.dont_write_bytecode=True
from audit import g,save,expr,eq,s,x
cases=[];rows=[]
for a in [1,2]:
 p={'a':a,'b':2,'h':-1}
 try:
  r=g.generate('easy',seed=991,parameters=p);rows.append(r)
  f=r['question'][':question/answer-fields'][0];v=next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);ok=eq(expr(v),s.exp(a*x))
  cases.append({'parameters':p,'accepted':True,'correct_IF':v,'expected_IF':str(s.exp(a*x)),'passed':ok})
 except ValueError as e:cases.append({'parameters':p,'accepted':False,'expected_IF':str(s.exp(a*x)),'expected_y':str(2-3*s.exp(-a*x)),'exception':str(e),'passed':False})
save('regression-records.json',rows);save('regression-results.json',{'command':__doc__,'cases':cases,'passed':all(v['passed'] for v in cases),'reason':'Both integrate constant P and apply y(0)=-1 to y=2+C exp(-a x). a=2 introduces no operator, prerequisite, or extra solution stage.'})
assert all(v['passed'] for v in cases), 'Eligible a=2 easy counterfactual rejected: Easy fixes unit P'
