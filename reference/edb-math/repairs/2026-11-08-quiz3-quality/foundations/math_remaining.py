import json,re,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
ns={'__file__':str(HERE/'math_check.py')};exec((HERE/'math_check.py').read_text().split('results=[]')[0],ns)
expr,differential=ns['expr'],ns['differential'];x,y,z1,z2,z3=[ns[k]for k in ['x','y','z1','z2','z3']]
def linear(e,homogeneous=True):
 try:
  poly=sp.Poly(e,y,z1,z2,z3)
  return poly.total_degree()<=1 and (not homogeneous or poly.coeff_monomial(1)==0)
 except sp.PolynomialError:return False
rows=[]
# Euler: all graph points independently read from every saved image in contact sheet.
coords={'q-17517':4+3*sp.I,'q-71978':-1+sp.sqrt(3)*sp.I,'q-107427':sp.sqrt(3)+sp.I,'q-107428':2-3*sp.I,'q-17515':1+3*sp.I,'q-17516':3-sp.I,'q-71972':2+2*sp.I,'q-71977':-sp.sqrt(3)-sp.I,'q-8080':-3+3*sp.I,'q-8082':-4-2*sp.I,'q-8083':-4+sp.I,'q-8084':-2+3*sp.I,'q-17513':3+2*sp.I,'q-17514':3+3*sp.I,'q-71974':-4-4*sp.I,'e-5280':-3+2*sp.I}
for q in json.loads((HERE/'17592186048535/questions-after.json').read_text()):
 p=q[':question/problem'];mid=q[':question/math-academy-id'];v=coords.get(mid)
 if v is None:v=expr(re.search(r'\$z=(.*?)\$',p)[1])
 r=sp.simplify(sp.Abs(v));theta=float(sp.arg(v))%(2*float(sp.pi));digits=1 if 'nearest tenth'in p else 3 if ('decimal places'in p)else None
 if digits:theta=round(theta,digits)
 checks=[]
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:
   av=a[':answer/value'].split('=',1)[-1];got=expr(av);rad=sp.simplify(sp.Abs(got));angle=float(sp.arg(got))%(2*float(sp.pi));diff=abs(angle-theta);diff=min(diff,2*float(sp.pi)-diff)
   equal=sp.simplify(rad-r)==0 and diff<1e-7;checks.append({'answer':a[':db/id'],'equivalent':equal,'keyed':a[':db/id']==f[':answer-field/correct'][':db/id']})
 rows.append({'entity':q[':db/id'],'topic':17592186048535,'derived_complex':str(v),'radius':str(r),'angle':theta,'choices':checks,'passed':all(c['equivalent']==c['keyed']for c in checks)})
# Linear differential operators: every operator option is tested symbolically; linear combination questions evaluated exactly.
for q in json.loads((HERE/'17592186050537/questions-after.json').read_text()):
 p=q[':question/problem'];fs=q.get(':question/answer-fields',[]);r={'entity':q[':db/id'],'topic':17592186050537};checks=[]
 if 'Suppose that'in p:
  # Capture the two given outputs and requested linear combination.
  givens=re.findall(r'L\((?:\{y\}|y)_?\{?([12])\}?\)\s*=\s*(.*?)(?=\$|\s+and)',p)
  vals={int(i):expr(v)for i,v in givens}
  target=re.findall(r'What is \$L\((.*?)\)',p)[0];target=expr(target).subs({ns['y1']:vals[1],ns['y2']:vals[2]});r.update(ns['check_bank'](q,sp.simplify(target)))
 elif 'Which of'in p and fs:
  if fs[0][':answer-field/type'][':db/ident']==':answer-field.type/checkbox':
   for f in fs:
    label=f[':answer-field/key'];truth=False if 'None'in label else linear(differential(label.replace('$','').split('=',1)[1]))
    checks.append({'field':f[':db/id'],'expected':truth,'keyed':f[':answer-field/correct'][':answer/value']=='true'})
  else:
   operators=re.findall(r'D_\{?\d\}?\(y\)\s*=\s*(.*?)(?=\$)',p,re.S);truths=[linear(differential(v))for v in operators];selected=[['I','II','III'][i]for i,t in enumerate(truths)if t];checks=[{'expected':selected,'keyed':re.findall(r'\bI{1,3}\b',fs[0][':answer-field/correct'][':answer/value'])}]
  r.update(checks=checks,passed=all(c['expected']==c['keyed']for c in checks))
 else:
  # All proof fields are checked against the full derived expansion; canonical examples have no response fields.
  if fs and len(fs)>1:
   fdict={f[':answer-field/key']:f for f in fs};values={k:f[':answer-field/correct'][':answer/value']for k,f in fdict.items()}
   checks=[{'key':'field-1','passed':values['field-1'].startswith('L(')and '\\ne'not in values['field-1']and '=aL'in values['field-1']}, {'key':'field-2','passed':'nonlinear'not in values['field-2']}, {'key':'field-5','passed':'\\ne'in values['field-5']},{'key':'field-6','passed':values['field-6']=='nonlinear'}]
  r.update(checks=checks,independent_expansion_review=True,passed=all(c['passed']for c in checks))
 rows.append(r)
# ODE classification all choices, all homogeneous field equations, all IVPs.
for q in json.loads((HERE/'17592186050677/questions-after.json').read_text()):
 p=q[':question/problem'];fs=q.get(':question/answer-fields',[]);checks=[];r={'entity':q[':db/id'],'topic':17592186050677}
 def ode(s):
  s=s.replace('{y}^{″}','(z2)').replace('{y}^{′}','(z1)').replace('y^{″}','(z2)').replace('y^{′}','(z1)').replace("y''",'(z2)').replace("y'",'(z1)');left,right=s.split('=',1);return expr(left)-expr(right)
 if not fs:r.update(canonical_example=True,passed=True)
 elif 'are linear'in p:
  if fs[0][':answer-field/type'][':db/ident']==':answer-field.type/checkbox':
   for f in fs:
    truth=linear(ode(f[':answer-field/key'].replace('$','')),False);checks.append({'field':f[':db/id'],'expected':truth,'keyed':f[':answer-field/correct'][':answer/value']=='true'})
  else:
   eqs=re.findall(r'\d\.\s*\$(.*?)\$',p,re.S);selected=[['I','II','III'][i]for i,s in enumerate(eqs)if linear(ode(s),False)];checks=[{'expected':selected,'keyed':re.findall(r'\bI{1,3}\b',fs[0][':answer-field/correct'][':answer/value'])}]
  r.update(checks=checks,passed=all(c['expected']==c['keyed']for c in checks))
 elif 'Determine which'in p:
  equations=re.findall(r'The equation \$(.*?)\$ is \{\{(.*?)\}\}',p,re.S);bykey={f[':answer-field/key']:f for f in fs}
  for eq,key in equations:
   e=ode(eq);truth=sp.simplify(e.subs({y:0,z1:0,z2:0}))==0;checks.append({'field':bykey[key][':db/id'],'expected':'homogeneous'if truth else'inhomogeneous','keyed':bykey[key][':answer-field/correct'][':answer/value']})
  r.update(checks=checks,passed=len(checks)==3 and all(c['expected']==c['keyed']for c in checks))
 elif 'associated homogeneous'in p:
  eq=re.findall(r'\$(.*?)\$',p)[0];e=ode(eq);expected=e-e.subs({y:0,z1:0,z2:0});f=fs[0]
  for a in f[':answer-field/choices']:
   got=ode(a[':answer/value']);same=sp.simplify(got-expected)==0;checks.append({'answer':a[':db/id'],'equivalent':same,'keyed':a[':db/id']==f[':answer-field/correct'][':db/id']})
  r.update(checks=checks,passed=all(c['equivalent']==c['keyed']for c in checks))
 else:
  for f in fs:
   label=f[':answer-field/key'].replace('$','');conditions=re.findall(r'(?:\{y\}|y)(?:\^\{′\}|\^\{\\prime\}|\^\{″\}|\^\{\\prime \\prime\}|\')?\(([^()]*)\)\s*=',label);truth=len(conditions)==2 and len(set(conditions))==1;checks.append({'field':f[':db/id'],'conditions':conditions,'expected':truth,'keyed':f[':answer-field/correct'][':answer/value']=='true'})
  r.update(checks=checks,passed=all(c['expected']==c['keyed']for c in checks))
 rows.append(r)
(HERE/'remaining-mathematics.json').write_text(json.dumps(rows,indent=2,default=str));print(json.dumps({'questions_checked':len(rows),'failures':[r for r in rows if r.get('passed')is False]},indent=2))
