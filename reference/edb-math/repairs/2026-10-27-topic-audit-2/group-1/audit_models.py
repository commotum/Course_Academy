"""Independent mass-balance/Newton/decay checks from question givens."""
import collections,json,re,sys
from pathlib import Path
import sympy as S
from texmath import parse
H=Path(__file__).resolve().parent;D=json.loads((H/'current.json').read_text());topic={t['entity']:t['ma_id']for t in D['topics']};tq={q:topic[t]for t,k,q in D['links']};T=S.Symbol('t',positive=True)
def plain(s):
 s=s.replace(r'\,','').replace('$','').replace('−','-').replace(r'\mu','μ').replace(r'\%','%')
 for i in range(5):s=re.sub(r'\\(?:text|textrm|mathrm)\{([^{}]*)\}',r'\1',s)
 s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1/\2)',s)
 return s.replace('{','').replace('}','').replace('**','')
def nums(s):return [S.Rational(n)for n in re.findall(r'(?<![\d.])[\d]+(?:\.[\d]+)?',s)]
def answernum(s):
 s=plain(s);parts=re.findall(r'([\d.]+)\s*(billion|million|thousand)?',s);out=0
 for n,m in parts:out+=float(n)*{'':1,'billion':1e9,'million':1e6,'thousand':1e3}[m]
 return out
def eq(a,b):return S.simplify(a-b)==0
out=[]
for q in D['questions']:
 topicid=tq[q[':db/id']]
 if topicid not in[1712,6700,3673]:continue
 p=plain(q[':question/problem']);r={'question':q[':db/id'],'identity':q.get(':question/math-academy-id'),'topic':topicid,'status':'review','checks':[]}
 try:
  if topicid==3673:
   hm=re.search(r'half-life of .*? is ([\d.]+)\s*(million|billion|thousand)?',p,re.I);Hval=S.Rational(hm[1])if hm else None;scale={'million':1e6,'billion':1e9,'thousand':1e3,None:1}[hm[2]]if hm else 1
   if 'original'in p:
    percent=S.Rational(re.search(r'([\d.]+)\s*%',p)[1]);value=Hval*S.log(100/percent)/S.log(2);kind='decay-age';unit_scale=scale
    if re.search(r'million years old|billion years old',p):unit_scale=1
   elif 'initial mass'in p:
    initial=S.Rational(re.search(r'initial mass of ([\d.]+)',p)[1]);time=S.Rational(re.search(r'after ([\d.]+)',p)[1]);Hval=Hval or S.Rational(re.search(r'half-life of ([\d.]+)',p)[1]);value=initial*2**(-time/Hval);kind='remaining-mass';unit_scale=1
   elif 'reduce to'in p:
    Hval=Hval or S.Rational(re.search(r'half-life of .*? is ([\d.]+)',p)[1]);initial=S.Rational(re.search(r'for (?:a|an) ([\d.]+)',p)[1]);final=S.Rational(re.search(r'reduce to ([\d.]+)',p)[1]);value=Hval*S.log(initial/final)/S.log(2);kind='decay-time';unit_scale=1
   elif Hval is not None:value=S.log(2)/Hval;kind='decay-constant';unit_scale=1
   else:
    rate=S.Rational(re.search(r'e\^-([\d.]+)t',p)[1]);value=S.log(2)/rate;kind='half-life';unit_scale=1
   if kind=='half-life'and'time, in millions of years'in p:unit_scale=1e6
   r.update(kind=kind,expected=str(value),numeric=float(value),time_unit_scale=unit_scale,formula='M=M0*2**(-t/H); H=ln(2)/k')
   tolerance=0.000001
   if 'three significant'in p:tolerance=abs(float(value))*.005
   elif 'two decimal'in p:tolerance=.0051
   elif 'one decimal'in p:tolerance=.051
   elif 'nearest minute'in p or 'nearest integer'in p:tolerance=.501
   elif 'approximately'in p and 'original'in p:tolerance=1000/unit_scale # option words round geological ages
   for f in q.get(':question/answer-fields',[]):
    a=f.get(':answer-field/correct')
    if not a:continue
    observed=answernum(a[':answer/value']);target=float(value)*unit_scale
    if kind=='decay-age'and'original'in p:
     raw=plain(a[':answer/value']);num=re.search(r'([\d.]+)\s*(billion|million|thousand)',raw)
     if num:
      decimals=len(num[1].split('.')[1])if'.'in num[1]else 0;tolerance=max(tolerance,(.5*10**(-decimals)*{'billion':1e9,'million':1e6,'thousand':1e3}[num[2]])/unit_scale)
    r['checks'].append({'field':f[':db/id'],'canonical':a[':answer/value'],'observed':observed,'expected_numeric':target,'tolerance':tolerance*unit_scale,'pass':abs(observed-target)<=tolerance*unit_scale})
  elif topicid==6700:
   quantities=[(S.Rational(n.strip('()')),u)for n,u in re.findall(r'(\([\d.]+/[\d.]+\)|[\d.]+)\s*(kg/L|g/L|lb/gal|L/min|gal/min|kg|lb|gal|L)\b',p)]
   quantities=[(v/1000 if u=='g/L'else v,u)for v,u in quantities]
   capacity=None
   if 'hold up to'in p:capacity=quantities.pop(0)[0]
   V0,Q0,c,rin,rout=[v for v,u in quantities[:5]];delta=rin-rout;V=V0+delta*T
   model=c*V+(Q0-c*V0)*S.exp(-rin*T/V0)if delta==0 else c*V+(Q0-c*V0)*(V0/V)**(rout/delta)
   residual=S.simplify(S.diff(model,T)-(c*rin-rout*model/V));assert residual==0 and eq(model.subs(T,0),Q0)
   if 'α + β'in p or r'\alpha +\beta'in p:value=Q0;kind='initial-sum'
   elif 'α -β'in p or 'α - β'in p or r'\alpha -\beta'in p:value=2*c*V0-Q0;kind='coefficient-difference'
   elif capacity is not None:
    assert delta>0 and capacity>=V0;time=(capacity-V0)/delta;value=model.subs(T,time);kind='overflow-mass'
   elif 'Which expression'in p:value=model;kind='mass-function'
   else:
    time=S.Rational(re.search(r'(?:tank|reservoir|basin|vat|mixer) ([\d.]+) minutes',p)[1]);assert V.subs(T,time)>0;value=model.subs(T,time);kind='timed-mass'
   r.update(kind=kind,parameters=dict(V0=str(V0),Q0=str(Q0),concentration=str(c),inflow=str(rin),outflow=str(rout)),volume=str(V),model=str(model),expected=str(value),mass_balance_residual=str(residual),domain='t>=0, V(t)>0; stop at capacity/emptying boundary')
   for f in q.get(':question/answer-fields',[]):
    a=f.get(':answer-field/correct')
    if not a:continue
    av=a[':answer/value']
    if kind=='mass-function':passed=eq(parse(av.split('=')[-1]),value);obs=av
    else:
     obs=answernum(av);tol=.051 if kind=='overflow-mass'else .0051 if kind=='timed-mass'else 1e-8;passed=abs(obs-float(value))<=tol
    r['checks'].append({'field':f[':db/id'],'canonical':av,'observed':obs,'pass':passed})
  else:
   m=S.Rational(re.search(r'mass ([\d.]+)\s*kg',p)[1]);obs=re.search(r'velocity (?:is|of) ([\d.]+)\s*m/s.*?acceleration (?:is|of) ([\d.]+)',p);kexplicit=re.search(r'k\s*=\s*([\d.]+)',p);g=S.Rational('9.8')if'9.8'in p else S.Symbol('g',positive=True);k=m*(g-S.Rational(obs[2]))/S.Rational(obs[1])if obs else S.Rational(kexplicit[1])if kexplicit else S.Symbol('k',positive=True)
   initial=re.search(r'initial (?:downward )?velocity of ([\d.]+)',p);v0=S.Rational(initial[1])if initial else S.Integer(0)if'from rest'in p else None
   if 'negligible'in p:model=(v0 if v0 is not None else S.Symbol('v0'))+g*T;residual=S.diff(model,T)-g
   else:model=m*g/k+((v0 if v0 is not None else S.Symbol('v0'))-m*g/k)*S.exp(-k*T/m);residual=S.simplify(S.diff(model,T)+k*model/m-g)
   assert residual==0
   if 'terminal velocity'in p:value=m*g/k;kind='terminal-velocity'
   elif re.search(r'(?:after|t=)\s*([\d.]+)\s*(?:seconds|s)',p):time=S.Rational(re.search(r'(?:after|t=)\s*([\d.]+)\s*(?:seconds|s)',p)[1]);value=model.subs(T,time);kind='timed-velocity'
   elif 'Find the equation'in p or 'equation for'in p:value=model;kind='velocity-function'
   else:value=None;kind='ODE-coefficient-units-individual-review'
   r.update(kind=kind,mass=str(m),drag_constant=str(k),model=str(model),expected=str(value),newton_residual=str(residual),direction='down positive; drag force=-kv',domain='t>=0,k>0 for drag model')
   for f in q.get(':question/answer-fields',[]):
    a=f.get(':answer-field/correct')
    if not a or value is None:continue
    av=a[':answer/value'];av=av.split('=')[-1]
    if kind=='velocity-function':passed=eq(parse(av),value)
    else:passed=abs(answernum(av)-float(value))<(.051 if 'one decimal'in p else .0051)
    r['checks'].append({'field':f[':db/id'],'canonical':a[':answer/value'],'pass':passed})
  r['status']='key-verified'if r['checks']and all(c['pass']for c in r['checks'])else'expected-derived'if not r['checks']else'review'
 except Exception as ex:r['status']='unresolved';r['reason']=str(ex)
 out.append(r)
(H/'model-math-validation.json').write_text(json.dumps(out,indent=2));print(collections.Counter((r['topic'],r['status'])for r in out));print([(r['identity'],r.get('reason'),r.get('kind'),r.get('checks'))for r in out if r['status']in['unresolved','review']])
