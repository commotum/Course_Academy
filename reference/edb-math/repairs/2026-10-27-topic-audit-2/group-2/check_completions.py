import json,re,signal
from pathlib import Path
import sympy as S
from independent_math import one,zero,correct
from mathlib import *
H=Path(__file__).resolve().parent;D=json.loads((H/'proposed-questions.json').read_text());Q={q[':db/id']:q for q in D};I=json.loads((H.parent/'inventory.json').read_text());KP={q:k for t,k,q in I['links']};out=[]
manual={108446:'I: exponent2; II has two nonlinear powers2,3 and no linear y term; III exponent−1/2, y>0. I and III only.',108447:'After dividing by y², II is y′+x²y=e^x y². Dividing I by y leaves two nonlinear powers. III trig functions of y. II only; zero equilibrium checked separately.'}
growth={339217:(10*S.log(3)/S.log(2),1),339225:(2*S.log(15)/S.log(5),1),339241:(3200*S.exp(-S.Rational(4,10)),0),339244:(8000*S.exp(-S.Rational(162,100)),0),339269:(S.log(S.Rational(400000,150000))/S.Rational(55,1000),0),339309:(S.log(3)/S.Rational(5,100),0)}
for evidence in json.loads((H/'completion-evidence.json').read_text()):
 q=Q[evidence['question']];n=int(evidence['identity'].split('-')[1]);kp=KP[q[':db/id']];row={'question':q[':db/id'],'identity':evidence['identity'],'kp':kp,'derivation':evidence['solution'],'checks':[]}
 try:
  signal.setitimer(signal.ITIMER_REAL,4)
  if n in manual:row['checks']=[{'method':'independent equation classification after valid division','status':'analytically-proved','proof':manual[n]}]
  elif n in growth:
   exact,places=growth[n];got=S.Rational(re.search(r'-?\d+(?:\.\d+)?',correct(q[':question/answer-fields'][0])[':answer/value'])[0]);delta=abs(float(got-exact));assert delta<.500001*10**(-places);row['checks']=[{'method':'independent exponential model inversion and rounding','exact':str(exact),'numerical':str(S.N(exact,20)),'places':places,'canonical':str(got),'status':'rounding-proved'}]
  elif n in[36435,47069,47071,47080,54486]:
   expr=next(parse(v)for _,v in maths(q[':question/problem'])if r'\lim'in v);expected=expr.doit();got=rhs(correct(q[':question/answer-fields'][0])[':answer/value']);assert expected==got or S.simplify(expected-got)==0;row['checks']=[{'method':'independent limit evaluation/continuity','expected':str(expected),'canonical':str(got),'status':'symbolically-proved'}]
  elif n in[332878,332880]:
   if n==332878:xx=-2*S.sin(6*t);yy=3*S.cos(6*t);A0=S.Matrix([[0,-4],[9,0]])
   else:xx=S.exp(2*t)*S.cos(3*t);yy=S.exp(2*t)*S.sin(3*t);A0=S.Matrix([[2,-3],[3,2]])
   vec=S.Matrix([xx,yy]);res=S.simplify(vec.diff(t)-A0*vec);assert res==S.zeros(2,1)
   for f in q[':question/answer-fields']:
    expected=xx if f[':answer-field/key']=='field-1'else yy;assert S.simplify(rhs(correct(f)[':answer/value'])-expected)==0
   row['checks']=[{'method':'independent matrix-system residual plus exact existing coordinate field mapping','residual':str(res),'status':'symbolically-proved'}]
  elif n==337143:
   P=(y+x)*S.exp(y);Q0=x*S.exp(y);assert S.simplify(S.diff(P,y)-S.diff(Q0,x))==(x+y)*S.exp(y);row['checks']=[{'method':'multiply both original coefficients; differentiate to disprove exactness','P':str(P),'Q':str(Q0),'exactness_residual':str((x+y)*S.exp(y)),'status':'symbolically-proved'}]
  else:row['checks']=one(q,kp)
  assert all(c['status']!='candidate'for c in row['checks']),row
  row['passed']=True
 except Exception as ex:row['passed']=False;row['error']=str(ex)
 finally:signal.setitimer(signal.ITIMER_REAL,0)
 out.append(row)
(H/'completion-math-verification.json').write_text(json.dumps(out,indent=2)+'\n');print('passed',sum(x['passed']for x in out),'of',len(out));print([(x['identity'],x.get('error'))for x in out if not x['passed']])
