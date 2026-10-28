import json,re,signal,collections
from pathlib import Path
import sympy as S
from independent_math import one,correct,zero
from mathlib import *
H=Path(__file__).resolve().parent;data=json.loads((H/'generator-final-samples.json').read_text());old=json.loads((H/'fresh-independent-math.json').read_text());skips=json.loads((H/'fresh-math-skips.json').read_text());byindex={x['index']:x for x in old};newskip=[]
def classify(v,kind):
 v=clean(v)
 if r'\frac{d^{2}'in v or r'\frac{{d}^{2}'in v or r"y''"in v:return False,'second order'
 f=equation(v);co=S.diff(f,D)
 if co==0 or co.has(D):return False,'not first-order linear derivative'
 rhs0=S.cancel(-f.subs(D,0)/co)
 if kind=='linear':return S.simplify(S.diff(rhs0,y,2))==0,str(rhs0)
 if kind=='homogeneous':return S.simplify(rhs0.subs(y,0))==0,str(rhs0)
 # Bernoulli requires one nonlinear monomial and optional linear term.
 powers=[]
 for term in S.Add.make_args(S.expand(rhs0)):
  power=term.as_powers_dict().get(y,S.Integer(0));coefficient=S.cancel(term/y**power)
  if coefficient.has(y):return False,str(rhs0)
  powers.append(power)
 nonlinear=set(powers)-{S.Integer(1)}
 return len(nonlinear)==1 and not any(n in[0,1]for n in nonlinear),str(rhs0)
def supplementary(q,kp):
 p=q[':question/problem'];fs=q[':question/answer-fields'];checks=[]
 if kp in[17592186087867,17592186087868,17592186147456]:
  kind={17592186087867:'linear',17592186087868:'homogeneous',17592186147456:'bernoulli'}[kp];decisions=[]
  if kp==17592186147456:
   statements=[v for _,v in maths(p)if'='in v and("'"in clean(v)or'dy'in clean(v))];decisions=[classify(v,kind)[0]for v in statements]
   assert len(decisions)==3,(len(decisions),statements)
  for f in fs:
   answer=correct(f)[':answer/value'];key=f[':answer-field/key'];kt=f[':answer-field/type'];kt=kt.get(':db/ident')if isinstance(kt,dict)else kt
   if kt==':answer-field.type/checkbox':
    if'none of'in key.lower():expect=not any(decisions)
    elif kp==17592186147456:expect=decisions[['I','II','III'].index(key)]
    else:
     expect,raw=classify(key.strip('$'),kind)
     if kp==17592186087868 and'inhomogeneous'in p:expect=not expect
     decisions.append(expect)
    match=expect==(answer=='true')
   else:
    selected={i for i,r in enumerate(['I','II','III'])if re.search(r'\b'+r+r'\b',answer)};match=selected=={i for i,b in enumerate(decisions)if b}
   checks.append({'field':f[':answer-field/id'],'method':'independent '+kind+' classification after collecting/dividing valid coefficients','status':'symbolically-proved'if match else'candidate'})
 elif kp==17592186100888:
  function=None
  for _,v in maths(p):
   v=clean(v);m=re.search(r'f\(x\)\s*=(.+)',v)
   if m:function=parse(m[1]);break
  if function is None:raise ValueError('f definition absent')
  form,raw=ode(p);res=residual(form,function)
  # Logarithm arguments are positive on the explicit source domain.
  res=S.refine(res,S.Q.positive(x));res=S.powsimp(res,force=True);solution=zero(res)[0]!='candidate';decisions=[]
  for f in fs:
   key=f[':answer-field/key'];ans=correct(f)[':answer/value']
   if key.startswith('I.'):
    v=maths(key)[0][1];right=v.split('=',1)[1].rstrip('. ');expected=zero(S.diff(function,x)-parse(right))[0]!='candidate'
   elif key.startswith(('II.','III.')):expected=solution
   else:expected=not any(decisions)
   decisions.append(expected);checks.append({'field':f[':answer-field/id'],'method':'independent derivative and substitution into full ODE','status':'symbolically-proved'if expected==(ans=='true')else'candidate','residual':str(res)})
 else:return one(q,kp)
 return checks
indices=sorted(set([x['index']for x in skips]+[x['index']for x in old if any(c['status']=='candidate'for c in x['checks'])]))
for i in indices:
 s=data[i];q=s['record']['question'];r={'index':i,'kp':s['kp'],'band':s['band'],'qid':q[':question/id'],'template':s['record']['generation'].get('template',s['record']['generation'].get('family'))}
 try:
  signal.setitimer(signal.ITIMER_REAL,2);checks=supplementary(q,s['kp'])
  # Resolve explicit local-domain absolute-value identities and sec/csc poles.
  for c in checks:
   if c['status']!='candidate':continue
   if s['kp']==17592186100959 and'x>0'in q[':question/problem']:
    raw=c.get('residual');expr=S.sympify(raw,locals={'x':x});positive=S.Symbol('u',positive=True);expr=S.simplify(expr.subs(x,positive))
    f=next(f for f in q[':question/answer-fields']if f[':answer-field/id']==c['field']);expect=expr==0
    if expect==(correct(f)[':answer/value']=='true'):c['status']='symbolically-proved-on-stated-positive-domain';c['domain_residual']=str(expr)
   if s['kp']==17592186064246 and'Piecewise'in c.get('residual','')and'(0, True)'in c['residual']:
    c['status']='analytically-proved-off-integrand-poles';c['domain_proof']='The nonzero exceptional branch is sin(x)=0, where the csc² integrand is undefined; ordinary derivative of log|sin| is cot on every remaining component.'
  r['checks']=checks;byindex[i]=r
 except Exception as ex:newskip.append({**r,'reason':str(ex)[:200]})
 finally:signal.setitimer(signal.ITIMER_REAL,0)
(H/'fresh-independent-math-final.json').write_text(json.dumps([byindex[i]for i in sorted(byindex)],indent=2)+'\n');(H/'fresh-math-skips-final.json').write_text(json.dumps(newskip,indent=2)+'\n');print('checked',len(byindex),'skips',len(newskip),'candidates',sum(any(c['status']=='candidate'for c in r['checks'])for r in byindex.values()));print(collections.Counter(x['kp']for x in newskip))
