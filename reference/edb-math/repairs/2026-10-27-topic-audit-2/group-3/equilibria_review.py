import json,re,signal,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));ns={'__file__':str(H/'math_check.py')};exec((H/'math_check.py').read_text().split('checks=[];unresolved=[];bad=[];completion_matches=[]')[0],ns);sp=ns['sp'];S=ns['SYMS'];parse=ns['parse'];checks=[];unresolved=[]
D=json.loads((H/'proposed-snapshot.json').read_text())
for q in D['questions']:
 if 'general solution'not in q[':question/problem'].lower():continue
 try:
  signal.alarm(2);res,state=ns['ode_task'](q)
  if state['order']!=1:continue
  y=S['y'];x=S[state['variable']];rhs=sp.solve(res,S['Z'])[0];num,den=sp.together(rhs).as_numer_denom();roots=sp.solve(num,y)
  for c in roots:
   if c.free_symbols or c.is_real is False or den.subs(y,c)==0:continue
   if sp.simplify(rhs.subs(y,c))!=0:continue
   prompt=q[':question/problem'];explicit_exclusion=c==0 and bool(re.search(r'y\s*\\ne(?:q)?\s*0|y\s*≠\s*0',prompt))or 'nonconstant'in prompt.lower()
   fs=q.get(':question/answer-fields',[])
   if not fs:continue
   f=fs[0];a=next(a for a in f[':answer-field/choices']if a[':db/id']==f.get(':answer-field/correct',{}).get(':db/id'));v=a[':answer/value'];left,right=v.split('=',1)if'='in v else('y',v);F=parse(left)-parse(right);constants=F.free_symbols-{x,y};sub=F.subs(y,c);contained=False
   if not sub.has(sp.zoo,sp.nan,sp.oo,-sp.oo):
    if sp.simplify(sub)==0:contained=True
    for C in constants:
     for cv in sp.solve(sub,C):
      if not cv.free_symbols&{x,y}and sp.simplify(sub.subs(C,cv))==0:contained=True
   checks.append({'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'equilibrium':str(c),'explicitly_excluded':bool(explicit_exclusion),'contained_in_key_family':bool(contained),'needs_completeness_note':not explicit_exclusion and not contained,'rhs':str(rhs),'canonical':v})
 except Exception as ex:unresolved.append({'entity':q[':db/id'],'reason':str(ex)[:180]})
 finally:signal.alarm(0)
(H/'equilibria-validation.json').write_text(json.dumps({'checks':checks,'unresolved':unresolved},indent=2));print('equilibria',len(checks),'gaps',[r for r in checks if r['needs_completeness_note']])
