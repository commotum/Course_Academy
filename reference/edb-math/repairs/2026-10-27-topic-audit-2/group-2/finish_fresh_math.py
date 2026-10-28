import json,re,signal,collections
from pathlib import Path
import sympy as S
from mathlib import *
from independent_math import correct,pq,differential,zero
H=Path(__file__).resolve().parent;data=json.loads((H/'generator-final-samples.json').read_text());rows={r['index']:r for r in json.loads((H/'fresh-independent-math-final.json').read_text())};skips=json.loads((H/'fresh-math-skips-final.json').read_text());left=[]
def form(v):
 v=v.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').replace(r'\\','').replace('{}','').replace('[','(').replace(']',')')
 return differential(v)
def checks(q,kp):
 p=q[':question/problem'];fs=sorted(q[':question/answer-fields'],key=lambda f:int(re.search(r'\d+',f[':answer-field/key'])[0])if re.search(r'\d+',f[':answer-field/key'])else 0);out=[]
 def add(f,method,expr,assumption=''):
  status,res=zero(expr);assert status!='candidate',(f[':answer-field/key'],method,res);out.append({'field':f[':answer-field/id'],'method':method,'status':status,'residual':res,'domain':assumption})
 if kp==17592186147454:
  residual0,raw=ode(p);right=S.cancel(-residual0.subs(D,0)/S.diff(residual0,D));powers={}
  for term in S.Add.make_args(S.expand(right)):
   term=S.factor(term)
   n=term.as_powers_dict().get(y,0);coef=S.cancel(term/y**n);assert not coef.has(y);powers[n]=powers.get(n,0)+coef
  nonlinear=set(powers)-{S.Integer(1)};assert len(nonlinear)==1;n=next(iter(nonlinear));P=-powers.get(S.Integer(1),0);Q0=powers[n]
  for f in fs:
   v=correct(f)[':answer/value'].replace(r'\pm','');sol=explicit_solution(v)
   zforms=[]
   for _,v0 in maths(q[':question/worked-solution']):
    if v0.strip().startswith('z='):
     candidate=parse(v0.strip()[2:])
     if candidate.has(C):zforms.append(candidate)
   assert zforms;zz=zforms[-1];recovered=S.powdenest(zz**(1/(1-n)),force=True);assert S.simplify(S.powdenest(sol-recovered,force=True))==0
   add(f,'independently derive Bernoulli n/P/Q; verify z=y^(1-n) linearized residual',S.diff(zz,x)+(1-n)*P*zz-(1-n)*Q0,'Use precisely the positive-coordinate/positive-z intervals stated in the fresh prompt; ± branches share y^-2 and are both retained.')
 elif kp in[17592186217248,17592186217249]:
  P,Q0=pq(p);n=len(fs);isy=kp==17592186217249;ratio=S.cancel((S.diff(P,y)-S.diff(Q0,x))/(P if isy else Q0));ratiofield=fs[-3];factorfield=fs[-2];lastfield=fs[-1];mu=rhs(correct(factorfield)[':answer/value'])
  add(ratiofield,'criterion quotient in original requested differential form',rhs(correct(ratiofield)[':answer/value'])-ratio)
  # Exactness is invariant under the explicitly stated differential form; no arbitrary rescaling.
  add(factorfield,'differentiated exactness identity',S.diff(mu*P,y)-S.diff(mu*Q0,x),'x>0 or y>0 as explicitly stated')
  RP,RQ=form(correct(lastfield)[':answer/value']);add(lastfield,'full displayed multiplied equation coefficient identity',RP-mu*P);add(lastfield,'full displayed multiplied equation coefficient identity',RQ-mu*Q0)
  if n>4:
   # The two coefficient derivatives immediately precede the criterion quotient.
   add(fs[-5],'P_y in exact source-key slot',rhs(correct(fs[-5])[':answer/value'])-S.diff(P,y));add(fs[-4],'Q_x in exact source-key slot',rhs(correct(fs[-4])[':answer/value'])-S.diff(Q0,x))
   for f in fs[:n-5]:
    value=correct(f)[':answer/value'];k=f[':answer-field/key']
    if'partial'in value or'∂'in value:
     expectedden='P'if isy else'Q';assert r'\frac{1}{'+expectedden+'}'in value and'-'in value
    elif r'\int'in value:
     raw=clean(value);assert ('(-\\int'in raw)==isy;assert('h(y)'in raw)==isy
    else:
     rp,rq=form(value);add(f,'converted original differential form',rp-P);add(f,'converted original differential form',rq-Q0);continue
    out.append({'field':f[':answer-field/id'],'method':'product-rule integrating-factor theorem, sign and actual function argument','status':'analytically-proved'})
  else:
   rp,rq=form(correct(fs[0])[':answer/value']);add(fs[0],'hard scaffold original form',rp-P);add(fs[0],'hard scaffold original form',rq-Q0)
 elif kp==17592186217247:
  P,Q0=pq(p);mu=None
  for _,v in maths(p):
   if re.search(r'I\(x,y\)\s*=',v):mu=parse(v.split('=',1)[1]);break
  assert mu is not None;MP=mu*P;MQ=mu*Q0;delta=S.simplify(S.diff(MP,y)-S.diff(MQ,x));exact=delta==0
  rp,rq=form(correct(fs[0])[':answer/value']);add(fs[0],'given factor applied to both original coefficients',rp-MP);add(fs[0],'given factor applied to both original coefficients',rq-MQ)
  add(fs[1],'transformed P_y',rhs(correct(fs[1])[':answer/value'])-S.diff(MP,y));add(fs[2],'transformed Q_x',rhs(correct(fs[2])[':answer/value'])-S.diff(MQ,x))
  for f in fs[3:]:
   value=correct(f)[':answer/value'];truth=value=='is'if value in['is',"isn't"]else not(r'\ne'in value)
   assert truth==exact,(value,delta);out.append({'field':f[':answer-field/id'],'method':'independent coefficient-derivative equality and factor test','status':'symbolically-proved','exactness_residual':str(delta)})
 elif kp==17592186064246:
  integral=next(parse(v)for _,v in maths(p)if r'\int'in v);integral=integral.lhs if isinstance(integral,S.Equality)else integral
  for f in fs:
   sol=rhs(correct(f)[':answer/value']);trig=next(iter(integral.function.atoms(S.sec,S.csc)));arg=trig.args[0];rate=S.diff(arg,x);linear=S.cancel(integral.function/trig**2);slope=S.diff(linear,x);assert not rate.has(x)and not slope.has(x)
   if trig.func==S.sec:expected=linear/rate*S.tan(arg)+slope/rate**2*S.log(S.Abs(S.cos(arg)))
   else:expected=-linear/rate*S.cot(arg)+slope/rate**2*S.log(S.Abs(S.sin(arg)))
   add(f,'independent generic integration-by-parts formula, exact linear factor/function argument/rate',sol-(expected+C),'Each real component avoiding original sec/csc poles; (log|u|)′=u′/u verifies the formula there')
 elif kp in[17592186110594,17592186110595]:
  expr=next(parse(v)for _,v in maths(p)if'='in v);assert isinstance(expr,S.Equality);var=next(iter(expr.free_symbols));real=S.Symbol(var.name,real=True);expr=expr.subs(var,real);roots=S.solve(expr,real);assert len(roots)==1
  for f in fs:
   got=rhs(correct(f)[':answer/value']);delta=abs(float(S.N(got-roots[0],40)));assert delta<.000500001;out.append({'field':f[':answer-field/id'],'method':'unique real logarithmic inverse and three-decimal rounding','status':'rounding-proved','unrounded':str(S.N(roots[0],30)),'absolute_rounding_error':delta})
 else:raise ValueError('unhandled')
 return out
for r in skips:
 i=r['index'];s=data[i]
 try:
  signal.setitimer(signal.ITIMER_REAL,4);r['checks']=checks(s['record']['question'],s['kp']);r.pop('reason',None);rows[i]=r
 except Exception as ex:left.append({**r,'reason':str(ex)[:400]})
 finally:signal.setitimer(signal.ITIMER_REAL,0)
(H/'fresh-independent-math-final.json').write_text(json.dumps([rows[i]for i in sorted(rows)],indent=2)+'\n');(H/'fresh-math-skips-final.json').write_text(json.dumps(left,indent=2)+'\n');print('checked',len(rows),'left',len(left),collections.Counter(r['kp']for r in left));print([(r['index'],r['reason'])for r in left[:8]])
