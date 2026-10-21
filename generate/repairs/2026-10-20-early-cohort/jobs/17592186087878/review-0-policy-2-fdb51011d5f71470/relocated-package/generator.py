#!/usr/bin/env python3
"""First-order linear general solutions; supplied capture basis 3794; steps 3–7 only.

The immutable source prose is compiled into masks whose slots are WHOLE math
components, never substrings of prose. Each builder computes those components
from parameters. Original and authored bank profiles remain separate. No EDB IO.
"""
from pathlib import Path
import argparse, hashlib, itertools, json, random, re, uuid
import sympy as sp
from math_format import normalize_prose, normalize_tex, checked_math_content

KP_ID=17592186087878
KP_UUID='6bbeb4f6-23b2-586c-8cb9-9742cce5a9a9'
TITLE='Solving First-Order Linear ODEs Using Integrating Factors'
VERSION='2.1.0'
ROOT=Path(__file__).resolve().parent
SOURCE=json.loads((ROOT/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
x=sp.Symbol('x',positive=True); C=sp.Symbol('C',real=True)
D=r'\frac{\text{d}y}{\text{d}x}'
DP=r'\frac{\text{d}}{\text{d}x}'
DX=r'\,\text{d}x'
STD=D+'+P(x)y=Q(x)'
NS=uuid.UUID(KP_UUID)

# Each source has its own prompt/layout/ordered solution stage mask.
TEMPLATES={
 'exp_forcing':{'level':'easy','source':'q-335402','family':'exp','base':{'a':3,'b':6,'r':2}},
 'exp_cancel':{'level':'easy','source':'q-339138','family':'cancel','base':{'a':3,'m':1}},
 'exp_cancel_legacy':{'level':'easy','source':'q-335392','family':'cancel','base':{'a':2,'m':2}},
 'power_constant':{'level':'moderate','source':'q-339140','family':'power','base':{'n':5,'b':7}},
 'power_constant_legacy':{'level':'moderate','source':'q-334915','family':'powerlegacy','base':{'n':2,'b':3}},
 'power_exp':{'level':'moderate','source':'q-335412','family':'powerexp','base':{'n':3,'r':1}},
 'power_sin':{'level':'hard','source':'q-335409','family':'sin','base':{'n':2,'r':1}},
 'power_cos':{'level':'hard','source':None,'family':'cos','base':{'n':3,'r':1}},
 'normalize_linear':{'level':'hard','source':'q-335069','family':'normalize','base':{'k':2,'b':3}},
}
PROFILES={}
for t,s in TEMPLATES.items():
 if s['source']:PROFILES[s['source']]={'template':t,'origin':'observed'}
 PROFILES[t+'_authored']={'template':t,'origin':'authored'}
PROFILES['q-339139']={'template':'power_constant','origin':'observed'}
PROFILES['q-335409-repaired']={'template':'power_sin','origin':'minimal-repair'}
class SampleRejected(ValueError):pass

def tex(v):return sp.latex(sp.sympify(v)).replace(r'\log',r'\ln')
def cx(a):return ('x' if a==1 else '-x' if a==-1 else str(a)+'x')
def xp(n):return 'x' if n==1 else '{x}^{'+str(n)+'}'
def ep(a):return '{e}^{'+cx(a)+'}'
def frac(a,b):return r'\frac{'+a+'}{'+b+'}'
def mul(a,s):return s if a==1 else '-'+s if a==-1 else str(a)+s

def coeff(a,s):
 a=sp.Rational(a)
 if a.q==1:return mul(a.p,s)
 return ('-' if a<0 else '')+frac(mul(abs(a.p),s),str(a.q))
def alg(rows):return r'\begin{aligned}'+' \\\\ '.join(a+' & ='+b for a,b in rows)+r'\end{aligned}'
def block(s):return '$$\n'+s+'\n$$'
def inline(s):return '$'+s+'$'
def integral(s,dx=DX):return r'\int '+s+dx

def compile_math_mask(text):
 parts=re.split(r'(\$\$.*?\$\$|\$[^$]*\$)',text,flags=re.S)
 return parts

def fill_math(text,components):
 parts=compile_math_mask(text)
 if len(parts[1::2])!=len(components):raise AssertionError('Whole-component mask length differs')
 parts[1::2]=components
 return ''.join(parts)

def bounds(spec,p):
 fam=spec['family'];keys=set(spec['base'])
 if set(p)!=keys or any(type(v)!=int for v in p.values()):raise ValueError('Exact parameter keys and integer values required')
 if fam=='exp':ok=2<=abs(p['a'])<=6 and 2<=p['b']<=9 and 1<=p['r']<=5 and p['r']!=p['a']
 elif fam=='cancel':ok=2<=abs(p['a'])<=6 and 1<=p['m']<=2
 elif fam in ('power','powerlegacy'):ok=2<=p['n']<=6 and 2<=p['b']<=9
 elif fam in ('powerexp','sin','cos'):ok=2<=p['n']<=6 and 1<=p['r']<=3
 elif fam=='normalize':ok=2<=p['k']<=6 and 2<=p['b']<=6
 else:ok=False
 if not ok:raise ValueError('Parameters exceed the documented same-level workload bounds')

def sample(spec,rng):
 f=spec['family']
 if f=='exp':
  a=rng.choice([-1,1])*rng.randint(2,6)
  return {'a':a,'b':rng.randint(2,9),'r':rng.choice([r for r in range(1,6) if r!=a])}
 if f=='cancel':return {'a':rng.choice([-1,1])*rng.randint(2,6),'m':rng.randint(1,2)}
 if f in ('power','powerlegacy'):return {'n':rng.randint(2,6),'b':rng.randint(2,9)}
 if f in ('powerexp','sin','cos'):return {'n':rng.randint(2,6),'r':rng.randint(1,3)}
 return {'k':rng.randint(2,6),'b':rng.randint(2,6)}

def build(spec,p,profile):
 """Exact mathematics and complete bank, followed by whole-component masks."""
 fam=spec['family'];observed=PROFILES[profile]['origin']=='observed'
 if fam=='exp':
  a,b,r=p['a'],p['b'],p['r']; P=-sp.Integer(a);Q=b*sp.exp(r*x);I=sp.exp(-a*x);F=sp.Rational(b,r-a)*sp.exp((r-a)*x)
  pt=-a;Ptex=str(-a);Qtex=mul(b,ep(r));It=ep(-a);qt=mul(b,ep(r-a));Ft=coeff(sp.Rational(b,r-a),ep(r-a));Yt=coeff(sp.Rational(b,r-a),ep(r))+'+C'+ep(a)
  ifbank=[ep(r),ep(a),ep(-a),ep(-r)]
  ybank=[coeff(sp.Rational(b,r-a),ep(r-a))+'+C'+ep(-a),coeff(-sp.Rational(b,r-a),ep(r))+'+C'+ep(a),coeff(-sp.Rational(b,r-a),ep(-r))+'+C'+ep(-a),Yt]
 elif fam=='cancel':
  a,m=p['a'],p['m'];P=-sp.Integer(a);Q=x**m*sp.exp(a*x);I=sp.exp(-a*x);F=x**(m+1)/(m+1)
  pt=-a;Ptex=str(-a);Qtex=xp(m)+ep(a);It=ep(-a);qt=xp(m);Ft=frac(xp(m+1),str(m+1));Yt=frac(xp(m+1)+ep(a),str(m+1))+'+C'+ep(a)
  ifbank=[mul(a,r'\operatorname{ln}⁡x'),ep(a),str(-a),It]
  wrong=frac(xp(m)+ep(-a),str(m+1));rightpart=frac(xp(m+1)+ep(a),str(m+1))
  ybank=[wrong+'+C'+ep(-a),rightpart+'+C'+ep(-a),wrong+'+C'+ep(a),Yt]
 elif fam in ('power','powerlegacy'):
  n,b=p['n'],p['b'];P=sp.Integer(n)/x;Q=sp.Integer(b);I=x**n;F=sp.Rational(b,n+1)*x**(n+1)
  pt=n;Ptex=frac(str(n),'x');Qtex=str(b);It=xp(n);qt=mul(b,xp(n));Ft=frac(mul(b,xp(n+1)),str(n+1));Yt=coeff(sp.Rational(b,n+1),'x')+'+'+frac('C',xp(n))
  ifbank=[xp(n-1),r'\operatorname{ln}⁡x',frac('1','x'),It]
  if profile=='q-339139':
   ybank=[Yt,xp(2)+'+'+frac('C',xp(n-1)),frac(xp(2),'2')+'+'+frac('C',xp(n)),frac('x','2')+'+'+frac('C',xp(n-1))]
  elif fam=='powerlegacy':
   first=coeff(sp.Rational(b,n+1),'x');wrong=coeff(sp.Rational(b,n+1),xp(2))
   ybank=[first+'+'+frac('C',xp(n)),wrong+'+'+frac('C',xp(n)),wrong+'+'+frac('C',xp(n-1)),first+'+'+frac('C',xp(n-1))]
  else:
   wrong='x' if observed else coeff(sp.Rational(b,n),'x');part=coeff(sp.Rational(b,n+1),'x')
   ybank=[wrong+'+'+frac('C',xp(n-1)),Yt,part+'+'+frac('C',xp(n-1)),wrong+'+'+frac('C',xp(n))]
 elif fam=='powerexp':
  n,r=p['n'],p['r'];P=sp.Integer(n)/x;Q=sp.exp(r*x)/x**n;I=x**n;F=sp.exp(r*x)/r
  pt=n;Ptex=frac(str(n),'x');Qtex=frac(ep(r),xp(n));It=xp(n);qt=ep(r);Ft=coeff(sp.Rational(1,r),ep(r));Yt=frac(Ft+'+C',xp(n))
  ifbank=[Ptex,It,'{e}^{'+str(n)+'/x}', '{e}^{'+xp(n)+'}']
  ybank=[Yt,xp(n-1)+'('+Ft+'+C)',frac(Ft+'+C',xp(n-1)),xp(n)+'('+Ft+'+C)']
 elif fam in ('sin','cos'):
  n,r=p['n'],p['r'];f=sp.sin if fam=='sin' else sp.cos;P=sp.Integer(n)/x;Q=f(r*x)/x**(n-1);I=x**n
  F=-x*sp.cos(r*x)/r+sp.sin(r*x)/r**2 if fam=='sin' else x*sp.sin(r*x)/r+sp.cos(r*x)/r**2
  st=r'\operatorname{sin}⁡'+cx(r);ct=r'\operatorname{cos}⁡'+cx(r);fun=st if fam=='sin' else ct
  pt=n;Ptex=frac(str(n),'x');Qtex=frac(fun,xp(n-1));It=xp(n);qt='x'+fun
  Ft=('-'+coeff(sp.Rational(1,r),'x'+ct)+'+'+coeff(sp.Rational(1,r*r),st)) if fam=='sin' else coeff(sp.Rational(1,r),'x'+st)+'+'+coeff(sp.Rational(1,r*r),ct)
  small=coeff(sp.Rational(1,r*r),frac(st if fam=='sin' else ct,xp(n)));large=coeff(sp.Rational(1,r),frac(ct if fam=='sin' else st,xp(n-1)))
  Yt=small+('-' if fam=='sin' else '+')+large+'+'+frac('C',xp(n))
  ifbank=[Ptex,'{e}^{'+xp(n)+'}',It,'{e}^{'+str(n)+'/x}']
  swapped=coeff(sp.Rational(1,r*r),frac(st if fam=='sin' else ct,xp(n-1)))
  swapped2=coeff(sp.Rational(1,r),frac(ct if fam=='sin' else st,xp(n)))
  ybank=[Yt.replace('⁡',''),swapped+'+'+swapped2+'+'+frac('C',xp(n)),swapped+'-'+swapped2+'+'+frac('C',xp(n-1)),small+('+' if fam=='sin' else '-')+large+'+'+frac('C',xp(n-1)),Yt if observed else small+('-' if fam=='sin' else '+')+large+'+'+frac('C',xp(n-1))]
 elif fam=='normalize':
  k,b=p['k'],p['b'];P=sp.Rational(1,k);Q=sp.Rational(b,k)*x;I=sp.exp(x/k);F=b*(x-k)*I
  pt=sp.Rational(1,k);Ptex=frac('1',str(k));Qtex=coeff(sp.Rational(b,k),'x');It='{e}^{x/'+str(k)+'}';qt=Qtex+It;Ft=mul(b,'(x-'+str(k)+')')+It;Yt=mul(b,'(x - '+str(k)+')')+' + C'+'e^{-x/'+str(k)+'}'
  ifbank=([mul(k,'x'),'x^{'+str(k)+'}','e^{-x/'+str(k)+'}','e^{x/'+str(k)+'}'] if observed else [frac('1',str(k)),'e^{'+str(k)+'x}','e^{-x/'+str(k)+'}','e^{x/'+str(k)+'}'])
  ybank=[mul(b,'x')+' - '+str(k)+' + Ce^{x/'+str(k)+'}',mul(b,'(x - '+str(k)+')')+' + Ce^{-x/'+str(k)+'}',mul(b,'(x - '+str(k)+')')+' + Ce^{x/'+str(k)+'}',mul(b,'x')+' - '+str(k)+' + Ce^{-x/'+str(k)+'}']
 else:raise AssertionError(fam)
 Y=sp.simplify((F+C)/I)
 # Full equation slots: layouts retain original inline/display math and prose.
 if spec['source'] in ('q-334915','q-335069','q-335392'):
  if fam=='powerlegacy':eq=r'\frac{dy}{dx} + '+Ptex+'y = '+Qtex+', x > 0'
  elif fam=='normalize':eq=str(k)+r'\frac{dy}{dx} + y = '+str(b)+'x'
  else:eq=r'\frac{dy}{dx} '+('- '+str(a) if a>0 else '+ '+str(-a))+'y = x^{'+str(m)+'}e^{'+cx(a)+'}'
  prompt=fill_math(QUESTIONS[spec['source']][':question/problem'],[inline(eq),inline('I(x) ='),inline('y(x) =')])
 else:
  eq=D+('+'+Ptex if P>0 else Ptex)+'y='+Qtex+(r',\,x>0.' if fam in ('power','powerexp','sin','cos') else '.')
  base=QUESTIONS[spec['source'] or 'q-335409'][':question/problem']
  prompt=fill_math(base,[block(eq),r'$\,$',inline('I(x)='),r'$\,$',inline('y(x)=')])
 solution=solution_math(spec,p,Ptex,Qtex,It,qt,Ft,Yt)
 return dict(P=P,Q=Q,I=I,F=F,Y=Y,prompt=prompt,solution=solution,banks={'field-1':ifbank,'field-2':ybank},correct={'field-1':I,'field-2':Y})


def solution_math(spec,p,Ptex,Qtex,It,qt,Ft,Yt):
 f=spec['family'];src=spec['source'];power=f in ('power','powerlegacy','powerexp','sin','cos')
 dx=DX if not power or f in ('sin','cos') else r'\,dx'
 if power:
  n=p['n'];ifrows=[('I(x)',r'{e}^{\int P(x)'+dx+'}'),('',r'{e}^{\int ('+str(n)+'/x)'+dx+'}'),('',r'{e}^{'+str(n)+r'\operatorname{ln}⁡x}')]
  if f not in ('sin','cos'):ifrows.append(('',r'{e}^{\operatorname{ln}⁡('+xp(n)+')}'))
  ifrows.append(('',It));distributed=mul(n,xp(n-1))+('\\cdot y' if f=='powerexp' else 'y')
  first=It+r'\cdot ('+D+'+'+Ptex+'y)'
  second=It+(r'\cdot ' if f=='powerexp' else '')+D+'+'+distributed
 else:
  val=-p['a'] if f in ('exp','cancel') else sp.Rational(1,p['k'])
  ifrows=[('I(x)',r'{e}^{\int P(x)'+DX+'}'),('',r'{e}^{\int '+str(val)+DX+'}'),('',It)]
  first=It+r'\cdot ('+D+(('-'+str(p['a']) if p['a']>0 else '+'+str(-p['a'])) if f in ('exp','cancel') else '+'+Ptex)+'y)'
  second=It+r'\cdot '+D+(('-'+str(p['a']) if p['a']>0 else '+'+str(-p['a'])) if f in ('exp','cancel') else '+'+Ptex)+It+r'\cdot y'
 common=[block(STD),inline('P(x)='+Ptex),inline('Q(x)='+Qtex+'.'),inline('I(x)'),block(alg(ifrows)),inline('I(x)='+It),block(alg([(first,It+r'\cdot '+Qtex),(second,qt)])),inline(DP+'(y'+r'\cdot I(x))')]
 yI='y'+It
 if f in ('power','powerexp','powerlegacy'):
  final=alg([(r'\int \frac{d}{dx}('+yI+r')\,dx',integral(qt)),(yI,Ft+'+C'),('y',Yt+('.' if f in ('power','powerlegacy') else ''))])
 elif f in ('exp','cancel'):
  final=alg([(DP+'('+yI+')',qt),(r'\int '+DP+'('+yI+r')\text{d}x',integral(qt)),(yI,Ft+'+C'),('y',Yt)])
 else:final=None
 if f in ('sin','cos'):
  r=p['r'];s=r'\operatorname{sin}⁡'+cx(r);c=r'\operatorname{cos}⁡'+cx(r)
  vt='-'+coeff(sp.Rational(1,r),c) if f=='sin' else coeff(sp.Rational(1,r),s)
  next_integrand=coeff(sp.Rational(1,r),c if f=='sin' else s)
  partsrow='x('+vt+')-'+integral('('+vt+r')\cdot 1')
  nextrow='x('+vt+')'+('+' if f=='sin' else '-')+integral(next_integrand)
  # Source n=2,r=1 distributes the coefficient before its third row.
  if r==1:nextrow=('-x'+c if f=='sin' else 'x'+s)+('+' if f=='sin' else '-')+integral(next_integrand)
  tail=[block(alg([(DP+'('+yI+')',qt),(r'\int '+DP+'('+yI+r')\text{d}x',integral(qt))])),block(r'\int u{v}^{′}'+DX+r'=uv-\int {u}^{′}v'+DX),inline('u=x,{u}^{′}=1,{v}^{′}='+(s if f=='sin' else c)+','),inline('v='+vt+'.'),block(alg([(yI,integral(qt)),(yI,partsrow),(yI,nextrow),(yI,Ft+r'\,+C'),('y',Yt+'.')]))]
 else:tail=[block(final)] if final is not None else []
 if src and ':question/worked-solution' in QUESTIONS[src]:return fill_math(QUESTIONS[src][':question/worked-solution'],common+tail)
 # No observed solution exists: this is explicitly authored explanation.
 if f=='normalize':
  k,b=p['k'],p['b'];scaled=frac(str(b),str(k))
  v=mul(k,It)
  ibp=alg([(yI,integral(qt)),
           (yI,scaled+r'\left(x('+v+')-'+integral(v)+r'\right)'),
           (yI,mul(b,'x'+It)+'-'+str(b)+integral(It)),
           (yI,mul(b,'x'+It)+'-'+mul(b*k,It)+'+C'),
           (yI,Ft+'+C'),('y',Yt+'.')])
  return ('First divide the equation by $'+str(k)+'$ to write it in standard form.\n\n'+block(D+'+'+Ptex+'y='+Qtex)+
          '\n\nThis equation is in the standard form\n\n'+block(STD)+
          '\n\nwith '+inline('P(x)='+Ptex)+' and '+inline('Q(x)='+Qtex+'.')+' We proceed to find an integrating factor $I(x)$ using the definition:\n\n'+block(alg(ifrows))+
          '\n\nNow, we multiply our differential equation through by '+inline('I(x)='+It)+' as follows:\n\n'+common[6]+
          '\n\nFinally, we rewrite the left hand side as '+common[7]+' and carry out the integration:\n\n'+block(alg([(DP+'('+yI+')',qt),(r'\int '+DP+'('+yI+r')\text{d}x',integral(qt))]))+
          '\n\nTo solve this integral, we integrate by parts.\n\n'+block(r'\int u{v}^{′}'+DX+r'=uv-\int {u}^{′}v'+DX)+
          '\n\nLet '+inline('u=x,{u}^{′}=1,{v}^{′}='+It+',')+' and '+inline('v='+v+'.')+' Then, we have\n\n'+block(ibp))
 reference=QUESTIONS['q-339138' if f=='cancel' else 'q-339140' if f=='powerlegacy' else 'q-335409'][':question/worked-solution']
 return fill_math(reference,common+tail)


def authored_banks(spec,p,b,roles,rng,explicit_roles=False):
 """Sample the answer-bearing coefficient first, then compatible full banks.

 Every candidate IF belongs to the same supported coefficient domain. Selecting
 three competitors uniformly conditional on the target makes the bank alone
 symmetric among its four values, including parameter-domain boundaries.
 """
 delta,error=roles['homogeneous_delta'],roles['coefficient_error']
 f=spec['family'];I=b['I'];Y=b['Y'];H=sp.diff(Y,C);part=Y.subs(C,0)
 if f=='exp' and p['a']+delta==p['r']:
  delta=-delta;roles['homogeneous_delta']=delta
 if f in ('exp','cancel'):
  z=-p['a'];domain=list(range(-6,-1))+list(range(2,7));factor=lambda v:sp.exp(v*x)
 elif f=='normalize':
  z=sp.Rational(1,p['k']);domain=[sp.Rational(1,k) for k in range(2,7)];factor=lambda v:sp.exp(v*x)
 else:
  z=p['n'];domain=list(range(2,7));factor=lambda v:x**v
 sets=[sorted([z,*others]) for others in itertools.combinations([v for v in domain if v!=z],3)]
 # Explicit audit assignments can request a feasible numeric rank. Normal
 # sampling chooses among all compatible subsets without rank conditioning.
 if explicit_roles and 'factor_candidates' in roles:
  forced=sorted(sp.Rational(v) for v in roles['factor_candidates'])
  if len(set(forced))!=4 or z not in forced or any(v not in domain for v in forced):raise ValueError('Invalid fixed factor bank')
  sets=[forced]
 elif explicit_roles:
  preferred=[values for values in sets if values.index(z)==roles['if_rank']]
  if preferred:sets=preferred
 values=rng.choice(sets);roles['if_rank']=values.index(z)
 roles['factor_candidates']=[str(v) for v in values]
 factors=[factor(v) for v in values]
 altH=H*(sp.exp(delta*x) if f in ('exp','cancel','normalize') else x**delta)
 if f=='exp':
  d=p['r']-p['a'];wrongpart=sp.Rational(p['b'],d+error)*sp.exp(p['r']*x) if d+error else -part
 elif f=='cancel':wrongpart=x**(p['m']+1)*sp.exp(p['a']*x)/(p['m']+1+error)
 elif f in ('power','powerlegacy'):wrongpart=sp.Rational(p['b'],p['n']+1+error)*x
 elif f=='powerexp':wrongpart=sp.exp(p['r']*x)*sp.Rational(1,p['r']+error)/x**p['n'] if p['r']+error else -part
 elif f=='normalize':wrongpart=part+error*p['b']
 else:
  # Flip one required IBP sign, retaining trig powers and workload.
  n,r=p['n'],p['r']
  wrongpart=(x*sp.cos(r*x)/r+sp.sin(r*x)/r**2)/x**n if f=='sin' else (x*sp.sin(r*x)/r-sp.cos(r*x)/r**2)/x**n
 bank=[part+C*H,wrongpart+C*H,part+C*altH,wrongpart+C*altH]
 if f in ('sin','cos'):
  # Preserve source five-choice shape; the extra swapped-power error is wrong
  # independently of which homogeneous exponent is selected.
  swap=part.subs(x,x) * x
  bank.append(swap+C*(H if error>0 else altH))
 b['banks']={'field-1':[tex(v) for v in factors],'field-2':[tex(sp.expand(v)) for v in bank]}
 return b

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,roles=None):
 if field_type not in (None,'select',':answer-field.type/select'):raise ValueError('This KP preserves the two-select layout')
 if profile:
  if profile not in PROFILES:raise ValueError('Unknown complete bank profile')
  implied=PROFILES[profile]['template']
  if template and template!=implied:raise ValueError('Profile belongs to another template')
  template=implied
 eligible=[t for t,s in TEMPLATES.items() if s['level']==level]
 if not eligible or template and template not in eligible:raise ValueError('Unsupported level/template')
 rng=random.Random(seed);template=template or rng.choice(eligible);spec=dict(TEMPLATES[template])
 profile=profile or template+'_authored'
 if profile=='q-339139':spec['source']='q-339139'
 explicit_roles=roles is not None
 roles=dict(roles) if roles is not None else {'if_rank':rng.randrange(4),'homogeneous_delta':rng.choice([-1,1]),'coefficient_error':rng.choice([-1,1])}
 if set(roles)-{'factor_candidates'}!={'if_rank','homogeneous_delta','coefficient_error'} or roles['if_rank'] not in range(4) or roles['homogeneous_delta'] not in (-1,1) or roles['coefficient_error'] not in (-1,1):raise ValueError('Invalid bank role assignment')
 if PROFILES[profile]['origin']!='authored' and parameters is None:raise SampleRejected('Source profiles are explicit-parameter replay only')
 evidence_only=profile=='q-335409'
 if evidence_only and parameters is None:raise SampleRejected('Raw ambiguous source bank requires explicit parameters and is evidence only')
 for attempt in range(100):
  p=dict(parameters) if parameters is not None else sample(spec,rng)
  try:
   bounds(spec,p);built=build(spec,p,profile)
   if PROFILES[profile]['origin']=='authored':built=authored_banks(spec,p,built,roles,rng,explicit_roles)
   # Compare COMPLETE general-solution families, allowing reparameterization C.
   for key,bank in built['banks'].items():
    values=[parse_math(v) for v in bank]
    if not evidence_only and any(equivalent(a,b,key=='field-2') for i,a in enumerate(values) for b in values[i+1:]):raise SampleRejected('Complete bank contains equivalent options')
    hits=[i for i,v in enumerate(values) if equivalent(v,built['correct'][key],key=='field-2')]
    if len(hits)!=(2 if evidence_only and key=='field-2' else 1):raise SampleRejected('Bank does not contain one correct mathematical value')
   break
  except (ValueError,SampleRejected):
   if parameters is not None:raise
 else:raise SampleRejected('No complete valid sampled bank')
 built['prompt']=normalize_prose(built['prompt']);built['solution']=normalize_prose(built['solution'])
 built['banks']={k:[normalize_tex(v) for v in bank] for k,bank in built['banks'].items()}
 bank_payload={k:sorted(v) for k,v in built['banks'].items()}
 payload={'version':VERSION,'prompt':built['prompt'],'solution':built['solution'],'banks':bank_payload,'domain':'x>0' if spec['family'] in ('power','powerlegacy','powerexp','sin','cos') else 'real x'}
 content=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
 # Assessed task: normalized displayed ODE and general solution demand; excludes
 # banks, source labels, prose, seed and mathematically incidental scaling.
 task=hashlib.sha256(json.dumps([sp.srepr(built['P']),sp.srepr(built['Q']),'IF+general-solution',payload['domain']]).encode()).hexdigest()
 qid=str(uuid.uuid5(NS,content));fields=[]
 sourcefields=QUESTIONS[spec['source']][':question/answer-fields'] if spec['source'] else [{' :unused':None,':answer-field/key':'field-2'},{':answer-field/key':'field-1'}]
 for sf in sourcefields:
  key=sf[':answer-field/key'];fid=str(uuid.uuid5(uuid.UUID(qid),key));choices=[];correctid=None
  for i,v in enumerate(built['banks'][key]):
   aid=str(uuid.uuid5(uuid.UUID(fid),v));choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':v})
   if correctid is None and equivalent(parse_math(v),built['correct'][key],key=='field-2'):correctid=aid
  random.Random(str(seed)+key).shuffle(choices)
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/select',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correctid]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':built['prompt'],':question/worked-solution':built['solution'],':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'roles':roles,'rejections':attempt,'bank_profile':profile,'bank_origin':PROFILES[profile]['origin'],'evidence_only':evidence_only,'raw_ambiguous_bank':evidence_only,'source_analysis':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_id':spec['source'],'authored_level_assignment':spec['source'] in ('q-334915','q-335069','q-335392') or spec['source'] is None,'content_fingerprint':content,'parameter_fingerprint':task,'plot_rating':'none','plot_assets':{},'domain':payload['domain'],'sympy_version':sp.__version__}}

# EASY: exponential cancellation or one exponential antiderivative.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: logarithmic IF and cancellation/power integration on x>0.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: exactly one integration-by-parts step after multiplication by the IF.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

# Restricted TeX reader: reads the DISPLAYED components without answer metadata.
# Recursive fractions, grouping, powers, exp/log/trig, and implicit products.
def parse_math(text):
 text=text.replace('\\\\','\\').replace('⁡','').replace('\u2061','').replace('−','-')
 text=re.sub(r'\\operatorname\{(sin|cos|ln)\}',r'\\\1 ',text)
 text=text.replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').replace(r'\,','').replace(' ','')
 tokens=re.findall(r'\\(?:frac|sin|cos|ln)|\d+|[A-Za-z]|[^\s]',text);pos=0
 def group():
  nonlocal pos
  if tokens[pos] in ('{','('):
   close='}' if tokens[pos]=='{' else ')';pos+=1;v=expression();assert tokens[pos]==close,(text,tokens[pos]);pos+=1;return v
  return atom()
 def atom():
  nonlocal pos
  t=tokens[pos];pos+=1
  if t==r'\frac':return group()/group()
  if t in (r'\sin',r'\cos',r'\ln'):
   fn={r'\sin':sp.sin,r'\cos':sp.cos,r'\ln':sp.log}[t]
   # Function argument is the immediately following coefficient*x component.
   arg=group()
   if arg.is_number and pos<len(tokens) and tokens[pos]=='x':pos+=1;arg*=x
   return fn(arg)
  if t in ('{','('):
   pos-=1;return group()
  if t=='-':return -atom()
  if t=='+':return atom()
  if t.isdigit():return sp.Integer(t)
  if t=='x':return x
  if t=='C':return C
  if t=='e':return sp.E
  raise ValueError('Unsupported displayed token '+t+' in '+text)
 def factor():
  nonlocal pos
  v=atom()
  if pos<len(tokens) and tokens[pos]=='^':pos+=1;v=v**group()
  return v
 def product():
  nonlocal pos
  v=factor()
  while pos<len(tokens) and tokens[pos] not in ('+','-','}',')'):
   t=tokens[pos]
   if t=='*':pos+=1;v*=factor()
   elif t=='/':pos+=1;v/=factor()
   else:v*=factor()
  return v
 def expression():
  nonlocal pos
  v=product()
  while pos<len(tokens) and tokens[pos] in ('+','-'):
   t=tokens[pos];pos+=1;w=product();v=v+w if t=='+' else v-w
  return v
 result=expression()
 if pos!=len(tokens):raise ValueError('Unconsumed displayed input '+text)
 return result

def equivalent(a,b,general=False):
 if not general:
  if a==0 or b==0:return a==b
  ratio=sp.simplify(a/b)
  return ratio!=0 and sp.diff(ratio,x)==0
 # General solution is an affine family; C can absorb a constant shift/scale.
 aa,ab=sp.diff(a,C),sp.diff(b,C)
 if aa==0 or ab==0:return False
 ratio=sp.simplify(aa/ab)
 offset=sp.simplify((a.subs(C,0)-b.subs(C,0))/ab)
 return ratio!=0 and sp.diff(ratio,x)==0 and sp.diff(offset,x)==0

def markdown(record):
 q=record['question'];g=record['generation'];lines=[f"## {g['template']} — {q[':question/difficulty'].split('/')[-1]}",f"Profile: `{g['bank_profile']}`; parameters: `{g['parameters']}`.",'',q[':question/problem'],'']
 for f in q[':question/answer-fields']:
  lines.append('**'+f[':answer-field/key']+'**')
  for a in f[':answer-field/choices']:lines.append('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else ''))
 lines+=['','**Worked solution**','',q[':question/worked-solution']]
 return '\n'.join(lines)

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='moderate');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='json');parser.add_argument('--template',choices=list(TEMPLATES));parser.add_argument('--profile',choices=list(PROFILES));a=parser.parse_args()
 if a.count<1 or (a.template or a.profile) and a.difficulty=='all':parser.error('A template/profile needs a single difficulty and positive count')
 records=[generate(l,a.seed+i,a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
