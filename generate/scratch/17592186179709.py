#!/usr/bin/env python3
"""Construct scalar ds line integrals with y=t. Frozen local draft; no DB writes.

Observed replay profiles scale the scalar density uniformly, preserving every
historical option's expression pattern and every worked-solution stage. Their
opaque distractor interpretations are NOT used for normal learning. Raw replay
retains omitted difficulty, solution and correct refs. Completed replay infers
two missing keys independently and repairs placeholder presentation.
Normal E/M/H recipes vary curve, density and endpoints within stated bounds.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix(''); SOURCE=json.loads((HERE/'source.json').read_text()); KP=SOURCE['record']
VERSION='function-of-y-1.0'; X,Y=s.symbols('x y',real=True); T=s.Symbol('t',positive=True)
QS=KP[':knowledge-point/questions']; NS=uuid.UUID('4b638f71-529a-5a6f-a68e-805f11080587')
def tex(e): return s.latex(s.sympify(e)).replace(r'\log',r'\ln')
def digest(o): return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def block(z): return '$$\n'+z+'\n$$'
def aligned(rows): return block(r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}')
def integ(e,a,b): return r'\int_{'+tex(a)+'}^{'+tex(b)+'}'+tex(e)+r'\,\mathrm{d}t'
def enums(v):
 if isinstance(v,dict):
  if set(v)=={':db/ident'}: return v[':db/ident']
  return {k:enums(x) for k,x in v.items() if k!=':db/id'}
 if isinstance(v,list): return [enums(x) for x in v]
 return v
# Parameters of every observed mathematical object, with full owned bank formulas.
OBS=[
 ('parabola_missing','moderate',-T**2/16,32*X*Y,-8,4,[T**3*s.sqrt(T**2+16),T**3*s.sqrt(T**2+1),T**3*s.sqrt(T**2+64),T**2*s.sqrt(T**2+64),T**2*s.sqrt(T**2+16)],2,r'32xy'),
 ('cubic_integral','moderate',2*T**3,X*Y**2,0,2,[(2*s.sqrt(36*T**4+1),0,2),(2*T**5*s.sqrt(36*T**4+1),0,2),(2*s.sqrt(36*T**4+1),0,16),(T**5*s.sqrt(T**4+1),0,2),(2*T**5*s.sqrt(36*T**4+1),0,16)],1,r'xy^{2}'),
 ('line_monomial','easy',T/3,9*X**2*Y,0,9,[1-T**3,T**3,T**3+3,3*T**2-1,T**2+1],1,r'9{x}^{2}y'),
 ('log_integral','moderate',s.log(T),s.exp(X)*Y**2,1,s.exp(2),[(T**2*s.sqrt(1+T**2),1,s.exp(2)),(T**2*s.sqrt(1+T**2),s.E,2*s.E),(T*s.sqrt(1+T**4),s.E,2*s.E),(T**3*s.sqrt(1+T**2),1,s.exp(2)),(T*s.sqrt(1+T**4),1,s.exp(2))],0,r'{e}^{x}{y}^{2}'),
 ('scaled_log_integral','moderate',2*s.log(T),4*Y*s.exp(2*X),1,s.E,[(4*T**2*s.sqrt(4*T**2+1),1,s.E),(2*T**2*s.sqrt(T**2+4),1,s.E),(2*T**4*s.sqrt(4*T**2+1),1,s.E),(T**3*s.sqrt(T**2+4),1,s.E),(4*T**4*s.sqrt(T**2+4),1,s.E)],4,r'4y{e}^{2x}'),
 ('reciprocal_integral','moderate',2/T,4*X*Y**2,1,6,[(s.sqrt(T**4+8)/T,s.Rational(1,3),2),(4*s.sqrt(T**4+1)/T,1,6),(8*s.sqrt(T**4+4)/T,s.Rational(1,3),2),(8*s.sqrt(T**4+4)/T,1,6),(s.sqrt(T**4+8)/T,1,6)],3,r'4x{y}^{2}'),
 ('line_affine','easy',2-3*T,2*X-3*Y,0,2,[4-9*T,2*T+5,2-5*T,4*T-1,1-3*T],0,r'2x-3y')]
# Seven practice records; source and recipe arrays preserve capture order.
TEMPLATES={o[0]:o[1] for o in OBS}|{'authored_line':'easy','authored_power':'moderate','authored_shifted_power':'hard'}
OBS_BY_NAME={o[0]:(i,o) for i,o in enumerate(OBS)}

def source_case(i):
 o=OBS[i]; q=QS[i]
 return {'source_id':q[':question/math-academy-id'],'template':o[0],'level':o[1],'parameters':{'density_scale':1},'bank_profile':'observed_raw'}

def scale_expression(z,c):
 # Complete scalar expressions are grouped, never replaced by short tokens.
 return z if c==1 else tex(c)+r'\left('+z+r'\right)'

def observed(name,c,profile):
 i,o=OBS_BY_NAME[name]; _,level,g,f,a,b,bank,ci,density=o; raw=QS[i]
 if not isinstance(c,int) or isinstance(c,bool) or not 1<=c<=5: raise ValueError('density_scale must be integer 1..5')
 correct=c*f.subs({X:g,Y:T})*s.sqrt(s.diff(g,T)**2+1)
 if name=='parabola_missing': correct/=s.Rational(-1,4)
 elif name in ('line_monomial','line_affine'): correct/=s.sqrt(s.diff(g,T)**2+1)
 matches=[j for j,z in enumerate(bank) if s.simplify(c*(z[0] if isinstance(z,tuple) else z)-correct)==0 and (not isinstance(z,tuple) or (z[1],z[2])==(a,b))]
 if len(matches)!=1: raise ValueError('Observed complete bank has no unique derived answer')
 ci=matches[0]
 q=enums(raw)  # Raw replay preserves every captured schema attribute's presence.
 # Original density is a complete template component. Every f-substitution row
 # is also a complete component, masked before reassembly.
 q[':question/problem']=q[':question/problem'].replace(density,scale_expression(density,c))
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'].replace(density,scale_expression(density,c))
  # Mask scalar values in the f(r(t)) aligned block and the following ds product.
  marker=r'\begin{aligned}f(r(t))'; start=sol.index(marker); end=sol.index(r'\end{aligned}',start)
  chunk=sol[start:end]; parts=chunk.split('& =')
  for j in range(1,len(parts)):
   split=parts[j].split(r'\\',1); expr=split[0].strip(); period='.' if expr.endswith('.') else ''; expr=expr.rstrip('.')
   if expr!=scale_expression(density,c): expr=scale_expression(expr,c)
   parts[j]=' '+expr+period+(' '+r'\\'+split[1] if len(split)>1 else '')
  replacement='& ='.join(parts) if c!=1 else sol[start:end]; sol=sol[:start]+replacement+sol[end:]
  # The last two equality rows contain f(r(t)) and its reduced density.
  begin=sol.rindex(r'\begin{aligned}'); final=sol[begin:]
  if c!=1:
   rows=final.split(r'\\')
   for j in range(1,len(rows)):
    rows[j]=rows[j].replace('& =','& ='+tex(c)+r'\cdot ',1)
   sol=sol[:begin]+r'\\'.join(rows)
  q[':question/worked-solution']=sol
 fields=q[':question/answer-fields']; field=fields[0]
 original_choices=raw[':question/answer-fields'][0][':answer-field/choices']
 for j,choice in enumerate(field[':answer-field/choices']): choice[':answer/value']=scale_expression(original_choices[j][':answer/value'],c)
 if ':answer-field/correct' in field:
  field[':answer-field/correct']=[':answer/id',field[':answer-field/choices'][ci][':answer/id']]
 if profile=='observed_completed':
  field[':answer-field/correct']=[':answer/id',field[':answer-field/choices'][ci][':answer/id']]
  q[':question/difficulty']=':question.difficulty/'+level
  if name=='parabola_missing': q[':question/problem']=q[':question/problem'].replace('AAAAA',r'\boxed{\phantom{t}}').replace(r'\int_(C)',r'\int_{C}')
  elif name=='cubic_integral': q[':question/problem']=q[':question/problem'].replace(r'\int_(C)',r'\int_{C}')
 return q, {'curve':str(g),'density':str(c*f),'bounds':[str(a),str(b)],'correct_index':ci,'bank_math':[str(c*x[0])+'|'+str(x[1])+'|'+str(x[2]) if isinstance(x,tuple) else str(c*x) for x in bank],'density_scale':c}

def guard(level,p):
 keys={'a','b','k','u','v','lo','hi','n'}
 if set(p)!=keys: raise ValueError('Expected exactly '+str(sorted(keys)))
 if any(type(p[k]) is not int for k in keys): raise ValueError('Integer parameters required')
 if not (1<=abs(p['a'])<=4 and 1<=p['k']<=5 and 1<=p['u']<=2 and 1<=p['v']<=3 and 0<=p['lo']<p['hi']<=5): raise ValueError('Parameter bounds violated')
 if level=='easy' and not(p['n']==1 and -4<=p['b']<=4): raise ValueError('Easy uses a line')
 if level=='moderate' and not(p['n'] in (2,3) and p['b']==0): raise ValueError('Moderate uses an unshifted power')
 if level=='hard' and not(p['n'] in (2,3) and 1<=abs(p['b'])<=4 and p['u']==2): raise ValueError('Hard requires shifted nonlinear curve and x squared')

def authored(level,p):
 guard(level,p); a,b,k,u,v,lo,hi,n=(p[z] for z in ('a','b','k','u','v','lo','hi','n'))
 g=a*T**n+b; f=k*X**u*Y**v; ft=f.subs({X:g,Y:T}); gp=s.diff(g,T); speed=s.sqrt(gp**2+1); exact=ft*speed
 # Complete bank chosen before sampling: omit density y power; omit density
 # x power; omit arc speed; differentiate without the exponent n.
 bank=[exact,k*g**u*speed,k*g*T**v*speed,ft,ft*s.sqrt((a*T**(n-1))**2+1)]
 if level=='easy': bank=[ft,k*(a*T+b)**u,k*(a*T)**u*T**v,k*(a*T+b)**v*T**u,k*(b-a*T)**u*T**v]
 # reject entire banks, including numerically equal complete definite integrals
 for i in range(5):
  for j in range(i):
   if s.simplify(bank[i]-bank[j])==0: raise ValueError('Complete bank collision')
 if level!='easy':
  import mpmath as mp
  with mp.workdps(35):
   vals=[mp.quad(s.lambdify(T,z,'mpmath'),[lo,hi]) for z in bank]
   if any(abs(vals[i]-vals[j])<mp.mpf('1e-25')*max(1,abs(vals[i]),abs(vals[j])) for i in range(5) for j in range(i)): raise ValueError('Equivalent definite-integral bank values')
 g_y=g.subs(T,Y); speedtex=tex(speed); prefix=tex(speed) if level=='easy' else ''
 missing=level=='easy'
 prompt=('Consider the line integral\n\n'+block(r'\int_C '+tex(f)+r'\,\mathrm{d}s='+prefix+r'\int_{'+str(lo)+'}^{'+str(hi)+r'}\boxed{}\,\mathrm{d}t') if missing else 'Which of the following is equivalent to the integral $'+r'\int_C '+tex(f)+r'\,\mathrm{d}s$')
 prompt+=('\n\nwhere $C$ is the '+('segment of the line' if missing else 'section of the curve')+' $x='+tex(g_y)+'$ traversed between the points $('+tex(g.subs(T,lo))+','+str(lo)+')$ and $('+tex(g.subs(T,hi))+','+str(hi)+')$.'+(' Which of the following is the missing expression under the integral on the right?' if missing else '')+'\n\n*Hint: Use the parameter $y=t.$*')
 sol='Notice that the given curve is of the form $x=x(y).$ Therefore, by setting $y=t,$ we have \n\n'+block('x=x(t)='+tex(g)+'.')
 sol+='\n\nThis gives the following parametrization of the curve:\n\n'+block(r'r(t)=\langle '+tex(g)+r',\,t\rangle,\quad '+str(lo)+r'\le t\le '+str(hi))
 sol+='\n\nNote that the domain $'+str(lo)+r'\le t\le '+str(hi)+'$ is defined by the $y$-coordinates of the end-points on the path.'
 sol+='\n\nComputing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: \n\n'+aligned([r'r^{\prime}(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j',r'&=\frac{\mathrm{d}}{\mathrm{d}t}('+tex(g)+r')i+\frac{\mathrm{d}}{\mathrm{d}t}(t)j',r'&=('+tex(gp)+r')i+j',r'\|r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}',r'&=\sqrt{('+tex(gp)+r')^2+1^2}',r'&='+speedtex])
 # Keep the literal substituted factors and reduce only on the next row.
 sol+='\n\nNow, if $f(x,y)='+tex(f)+',$ then we obtain\n\n'+aligned([r'f(r(t))&='+str(k)+r'\left('+tex(g)+r'\right)^{'+str(u)+r'}t^{'+str(v)+'}',r'&='+tex(ft)])
 sol+='\n\nTherefore, we can write the integral as\n\n'+aligned([r'\int_C '+tex(f)+r'\,\mathrm{d}s&=\int_{'+str(lo)+'}^{'+str(hi)+r'}f(r(t))\|r^{\prime}(t)\|\,\mathrm{d}t',r'&=\int_{'+str(lo)+'}^{'+str(hi)+r'}('+tex(ft)+r')\cdot '+speedtex+r'\,\mathrm{d}t',r'&='+((speedtex+r'\int_{'+str(lo)+'}^{'+str(hi)+'}'+tex(ft)+r'\,\mathrm{d}t') if missing else integ(exact,lo,hi))+'.'])
 values=[tex(z) if missing else integ(z,lo,hi) for z in bank]
 return {':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol}, values, {'curve':str(g),'density':str(f),'bounds':[str(lo),str(hi)],'correct_index':0,'bank_math':[str(z) if missing else str(z)+'|'+str(lo)+'|'+str(hi) for z in bank]}

def sample(level,rng):
 return {'a':rng.choice([-4,-3,-2,-1,1,2,3,4]),'b':rng.randint(-4,4) if level=='easy' else 0 if level=='moderate' else rng.choice([-4,-3,-2,-1,1,2,3,4]),'k':rng.randint(1,5),'u':2 if level=='hard' else rng.randint(1,2),'v':rng.randint(1,3),'lo':rng.randint(0,2),'hi':rng.randint(3,5),'n':1 if level=='easy' else rng.choice([2,3])}

# Additional normal source-shaped families. Their masks retain each source's
# sentences and complete stage sequence; banks are authored method operations.
FAMILY_SOURCES={'authored_line_monomial':2,'authored_affine':6,'authored_log':3,'authored_scaled_log':4,'authored_reciprocal':5}
TEMPLATES.update({'authored_line_monomial':'easy','authored_affine':'easy','authored_log':'moderate','authored_scaled_log':'moderate','authored_reciprocal':'moderate'})

def sample_family(name,rng):
 if name=='authored_line_monomial':return {'m':rng.randint(2,5),'k':rng.randint(1,4),'v':rng.randint(1,3),'lo':rng.randint(0,1),'hi':rng.randint(2,9)}
 if name=='authored_affine':return {'a':rng.choice([-4,-3,-2,-1,1,2,3,4]),'b':rng.randint(1,4),'p':rng.randint(1,4),'q':rng.choice([-4,-3,-2,-1,1,2,3,4]),'lo':rng.randint(0,1),'hi':rng.randint(2,5)}
 if name in ('authored_log','authored_scaled_log'):return {'a':rng.randint(1 if name=='authored_log' else 2,4),'k':rng.randint(1,5),'c':rng.randint(1,2),'v':rng.randint(1,3 if name=='authored_log' else 2),'lo':rng.randint(0,1),'hi':rng.randint(1 if name=='authored_scaled_log' else 2,3)}
 return {'a':rng.randint(2,4),'k':rng.randint(2,5),'v':rng.randint(2,3),'lo':rng.randint(1,2),'hi':rng.randint(3,6)}

def family_guard(name,p):
 keys={'a','b','p','q','lo','hi'} if name=='authored_affine' else {'a','k','v','lo','hi'}|({'c'} if name in ('authored_log','authored_scaled_log') else set())
 if set(p)!=keys or any(type(z)is not int for z in p.values()):raise ValueError('Invalid source-shaped family parameter keys or integer forms')
 if name=='authored_affine':
  valid=1<=abs(p['a'])<=4 and 1<=p['b']<=4 and 1<=p['p']<=4 and 1<=abs(p['q'])<=4 and 0<=p['lo']<=1 and 2<=p['hi']<=5
 elif name in ('authored_log','authored_scaled_log'):
  valid=(1 if name=='authored_log' else 2)<=p['a']<=4 and 1<=p['k']<=5 and 1<=p['c']<=2 and 1<=p['v']<=(3 if name=='authored_log' else 2) and p['a']*p['c']+p['v']<=7 and 0<=p['lo']<=1 and (1 if name=='authored_scaled_log' else 2)<=p['hi']<=3 and p['lo']<p['hi']
 else:valid=2<=p['a']<=4 and 2<=p['k']<=5 and 2<=p['v']<=3 and 1<=p['lo']<=2 and 3<=p['hi']<=6
 if not valid:raise ValueError('Source-shaped family workload bounds violated')

def source_prose_solution(i,blocks,g,f,lo,hi):
 original=QS[i][':question/worked-solution'];old=OBS[i];old_domain=tex(old[4])+r'\le t\le '+tex(old[5]);new_domain=tex(lo)+r'\le t\le '+tex(hi)
 # Original e-bound spelling uses nested braces; replace the complete domain
 # rather than a short number or single symbol anywhere in the prose.
 original=re.sub(r'(?<!\$)\$(?!\$)[^$]*\\le t\\le [^$]*\$(?!\$)' ,lambda m:'$'+new_domain+'$',original)
 original=original.replace(old[8],tex(f))
 chunks=re.split(r'\$\$\n.*?\n\$\$',original,flags=re.S)
 assert len(chunks)==len(blocks)+1,(i,len(chunks),len(blocks))
 return ''.join(chunks[j]+block(z) for j,z in enumerate(blocks))+chunks[-1]

def source_shaped(name,p):
 if name=='authored_line_monomial':return source_monomial(p)
 family_guard(name,p);a=p['a'];lo0,hi0=p['lo'],p['hi'];is_affine=name=='authored_affine';is_log=name in ('authored_log','authored_scaled_log');is_scaled=name=='authored_scaled_log'
 if is_affine:
  b,P,Q=p['b'],p['p'],p['q'];g=a*T+b;f=P*X+Q*Y;lo,hi=lo0,hi0;curveeq=r'\frac{x}{'+str(b)+'}='+tex(1+s.Rational(a,b)*Y)
 elif is_log:
  k,c,v=p['k'],p['c'],p['v'];g=a*s.log(T);f=k*s.exp(c*X)*Y**v;lo,hi=s.exp(lo0),s.exp(hi0);curveeq=(r'\frac{x}{'+str(a)+r'}=\ln y' if is_scaled else 'x='+tex(g.subs(T,Y)))
 else:
  k,v=p['k'],p['v'];g=a/T;f=k*X*Y**v;lo,hi=lo0,hi0;curveeq='x='+tex(g.subs(T,Y))
 gp=s.diff(g,T);ft=s.simplify(f.subs({X:g,Y:T}));speed=s.sqrt(gp**2+1);correct=s.simplify(ft*speed)
 if is_affine:
  bank=[ft,P*g,P*a*T+Q*T,P*g-Q*T,P*T+Q*g];values=[tex(z) for z in bank]
 else:
  if is_log:
   root=s.sqrt(T**2+a*a);power=a*c+v
   integrands=[correct,k*T**(v-1)*root,k*T**power*root,ft*s.sqrt(a*a+1),correct];bounds=[(lo,hi)]*4+[(a*lo0,a*hi0)]
  else:
   root=s.sqrt(T**4+a*a)
   integrands=[correct,k*T**(v-3)*root,a*T**(v-3)*root,ft*root,correct];bounds=[(lo,hi)]*4+[(s.Rational(a,hi0),s.Rational(a,lo0))]
  bank=list(zip(integrands,[z[0] for z in bounds],[z[1] for z in bounds]));values=[integ(z,u,w) for z,u,w in bank]
 # Complete operation banks are built as a unit. Integral value equality is a
 # separate eligibility criterion from different integrand/bounds structure.
 for i,z in enumerate(bank):
  for w in bank[:i]:
   if not isinstance(z,tuple) and s.simplify(z-w)==0:raise ValueError('Complete bank collision')
   if isinstance(z,tuple) and z[1:]==w[1:] and s.simplify(z[0]-w[0])==0:raise ValueError('Complete bank collision')
 if not is_affine:
  import mpmath as mp
  with mp.workdps(35):
   numerical=[mp.quad(s.lambdify(T,z,'mpmath'),[mp.mpf(str(s.N(u,40))),mp.mpf(str(s.N(w,40)))]) for z,u,w in bank]
   if any(abs(numerical[i]-numerical[j])<mp.mpf('1e-24')*max(1,abs(numerical[i]),abs(numerical[j])) for i in range(5) for j in range(i)):raise ValueError('Equal complete integral values')
 prompt=('Consider the line integral\n\n'+block(r'\int_C '+tex(f)+r'\,\mathrm{d}s='+tex(speed)+r'\int_{'+tex(lo)+'}^{'+tex(hi)+r'}\boxed{}\,\mathrm{d}t') if is_affine else 'Which of the following is equivalent to the integral $'+r'\int_C '+tex(f)+r'\,\mathrm{d}s$')
 prompt+='\n\nwhere $C$ is the '+('segment of the line' if is_affine else 'section of the curve')+' $'+curveeq+'$ traversed between the points $('+tex(g.subs(T,lo))+','+tex(lo)+')$ and $('+tex(g.subs(T,hi))+','+tex(hi)+')$.'
 if is_affine:prompt+=' Which of the following is the missing expression under the integral on the right?'
 prompt+='\n\n*Hint: Use the parameter $y=t.$*'
 blocks=[]
 if is_affine or is_scaled:blocks.append(curveeq+r'\,\Longrightarrow\,x='+tex(g.subs(T,Y)))
 blocks+=[r'x=x(t)='+tex(g)+'.',r'r(t)=\langle '+tex(g)+r',\,t\rangle,\quad '+tex(lo)+r'\le t\le '+tex(hi)]
 rows=[r'r^{\prime}(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j',r'&=\frac{\mathrm{d}}{\mathrm{d}t}('+tex(g)+r')i+\frac{\mathrm{d}}{\mathrm{d}t}(t)j',r'&=('+tex(gp)+r')i+j',r'\|r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}',r'&=\sqrt{('+tex(gp)+r')^2+1^2}']
 if is_affine:rows+=[r'&=\sqrt{'+str(a*a)+'+1}',r'&='+tex(speed)]
 elif is_log:
  rows+=[r'&=\sqrt{\frac{'+str(a*a)+r'}{t^2}+1}']
  if not is_scaled:rows+=[r'&=\sqrt{\frac{'+tex(T**2+a*a)+r'}{t^2}}',r'&=\frac{\sqrt{'+tex(T**2+a*a)+r'}}{|t|}',r'&=\frac{\sqrt{'+tex(T**2+a*a)+r'}}{t}']
  else:rows+=[r'&=\frac{1}{t}\sqrt{'+tex(T**2+a*a)+'}']
 else:rows+=[r'&=\sqrt{\frac{'+str(a*a)+r'}{t^4}+1}',r'&=\sqrt{\frac{'+tex(T**4+a*a)+r'}{t^4}}',r'&=\frac{\sqrt{'+tex(T**4+a*a)+r'}}{t^2}']
 blocks.append(r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}')
 if is_affine:fr=[r'f(r(t))&='+str(P)+r'\left('+tex(g)+r'\right)'+('+' if Q>0 else '-')+str(abs(Q))+'t',r'&='+tex(ft)+'.']
 elif is_log:
  if is_scaled:fr=[r'f(r(t))&='+tex(f),r'&='+str(k)+r'\cdot t^{'+str(v)+r'}e^{'+str(a*c)+r'\ln t}',r'&='+str(k)+r'\cdot t^{'+str(v)+r'}\left(t^{'+str(a*c)+r'}\right)',r'&='+tex(ft)+'.']
  else:fr=[r'f(r(t))&='+str(k)+r'\left(e^{'+str(a*c)+r'\ln t}\right)t^{'+str(v)+'}',r'&='+str(k)+r'\left(t^{'+str(a*c)+r'}\right)t^{'+str(v)+'}',r'&='+tex(ft)+'.']
 else:fr=[r'f(r(t))&='+str(k)+r'\left(\frac{'+str(a)+r'}{t}\right)t^{'+str(v)+'}',r'&='+tex(ft)+'.']
 blocks.append(r'\begin{aligned}'+r' \\ '.join(fr)+r'\end{aligned}')
 final=(tex(speed)+r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}('+tex(ft)+r')\,\mathrm{d}t') if is_affine else integ(correct,lo,hi)
 ir=[r'\int_C '+tex(f)+r'\,\mathrm{d}s&=\int_{'+tex(lo)+'}^{'+tex(hi)+r'}f(r(t))\|r^{\prime}(t)\|\,\mathrm{d}t',r'&=\int_{'+tex(lo)+'}^{'+tex(hi)+r'}('+tex(ft)+r')\cdot '+tex(speed)+r'\,\mathrm{d}t',r'&='+final+'.']
 blocks.append(r'\begin{aligned}'+r' \\ '.join(ir)+r'\end{aligned}')
 solution=source_prose_solution(FAMILY_SOURCES[name],blocks,g,f,lo,hi)
 return {':question/difficulty':':question.difficulty/'+TEMPLATES[name],':question/problem':prompt,':question/worked-solution':solution},values,{'curve':str(g),'density':str(f),'bounds':[str(lo),str(hi)],'correct_index':0,'bank_math':[str(z) for z in bank],'response_shape':'fragment' if is_affine else 'complete_integral','source_stage_reference':QS[FAMILY_SOURCES[name]][':question/math-academy-id']}

def source_monomial(p):
 if set(p)!={'m','k','v','lo','hi'} or any(type(z)is not int for z in p.values()):raise ValueError('Monomial line requires m,k,v,lo,hi integers')
 m,k,v,lo,hi=(p[z] for z in ('m','k','v','lo','hi'))
 if not(2<=m<=5 and 1<=k<=4 and 1<=v<=3 and 0<=lo<=1 and 2<=hi<=9):raise ValueError('Fractional-slope monomial line bounds violated')
 g=T/m;f=k*m*m*X**2*Y**v;ft=k*T**(v+2);gp=s.Rational(1,m);speed=s.sqrt(m*m+1)/m
 bank=[ft,k*m*T**(v+2),k*T**2,k*m**4*T**(v+2),k*T**(v+2)/m**v];values=[tex(z) for z in bank]
 if any(s.simplify(bank[i]-bank[j])==0 for i in range(5) for j in range(i)):raise ValueError('Complete monomial bank collision')
 eq=str(m)+'x=y';prompt='Consider the line integral\n\n'+block(r'\int_C '+tex(f)+r'\,\mathrm{d}s='+tex(speed)+r'\int_{'+str(lo)+'}^{'+str(hi)+r'}\boxed{}\,\mathrm{d}t')+'\n\nwhere $C$ is the segment of the line $'+eq+'$ traversed between the points $('+tex(g.subs(T,lo))+','+str(lo)+')$ and $('+tex(g.subs(T,hi))+','+str(hi)+')$. Which of the following is the missing expression under the integral on the right?\n\n*Hint: Use the parameter $y=t.$*'
 blocks=[eq+r'\,\Longrightarrow\,x=\frac{y}{'+str(m)+'}',r'x=x(t)=\frac{t}{'+str(m)+'}.',r'r(t)=\langle\frac{t}{'+str(m)+r'},\,t\rangle,\quad '+str(lo)+r'\le t\le '+str(hi)]
 dr=[r'r^{\prime}(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j',r'&=\frac{\mathrm{d}}{\mathrm{d}t}(\frac{t}{'+str(m)+r'})i+\frac{\mathrm{d}}{\mathrm{d}t}(t)j',r'&=(\frac{1}{'+str(m)+r'})i+j',r'\|r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}',r'&=\sqrt{(\frac{1}{'+str(m)+r'})^2+1^2}',r'&=\sqrt{\frac{1}{'+str(m*m)+r'}+1}',r'&=\sqrt{\frac{'+str(m*m+1)+'}{'+str(m*m)+'}}',r'&='+tex(speed)]
 blocks.append(r'\begin{aligned}'+r' \\ '.join(dr)+r'\end{aligned}')
 fr=[r'f(r(t))&='+str(k*m*m)+r'\left(\frac{t}{'+str(m)+r'}\right)^2t^{'+str(v)+'}',r'&='+str(k*m*m)+r'\left(\frac{t^2}{'+str(m*m)+r'}\right)t^{'+str(v)+'}',r'&='+tex(ft)+'.']
 blocks.append(r'\begin{aligned}'+r' \\ '.join(fr)+r'\end{aligned}')
 ir=[r'\int_C '+tex(f)+r'\,\mathrm{d}s&=\int_{'+str(lo)+'}^{'+str(hi)+r'}f(r(t))\|r^{\prime}(t)\|\,\mathrm{d}t',r'&=\int_{'+str(lo)+'}^{'+str(hi)+r'}('+tex(ft)+r')\cdot '+tex(speed)+r'\,\mathrm{d}t',r'&='+tex(speed)+r'\int_{'+str(lo)+'}^{'+str(hi)+'}'+tex(ft)+r'\,\mathrm{d}t.']
 blocks.append(r'\begin{aligned}'+r' \\ '.join(ir)+r'\end{aligned}')
 return {':question/difficulty':':question.difficulty/easy',':question/problem':prompt,':question/worked-solution':source_prose_solution(2,blocks,g,f,lo,hi)},values,{'curve':str(g),'density':str(f),'bounds':[str(lo),str(hi)],'correct_index':0,'bank_math':[str(z) for z in bank],'response_shape':'fragment','source_stage_reference':'q-122530'}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'): raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio'): raise ValueError('Only observed radio shape is supported')
 rng=random.Random(seed)
 template=template or rng.choice({'easy':['authored_line','authored_line_monomial','authored_affine'],'moderate':['authored_power','authored_log','authored_scaled_log','authored_reciprocal'],'hard':['authored_shifted_power']}[level])
 if TEMPLATES.get(template)!=level: raise ValueError('Template difficulty mismatch')
 profile=profile or ('authored_operations' if template.startswith('authored_') else 'observed_raw')
 if template in OBS_BY_NAME:
  if profile not in ('observed_raw','observed_completed'): raise ValueError('Unknown observed profile')
  p=parameters if parameters is not None else {'density_scale':rng.randint(1,5)}
  if set(p)!={'density_scale'}: raise ValueError('Observed parameters are density_scale only')
  q,m=observed(template,p['density_scale'],profile); field=q[':question/answer-fields'][0]
 else:
  if profile!='authored_operations': raise ValueError('Unknown authored profile')
  for trial in range(128):
   p=parameters if parameters is not None else (sample_family(template,rng) if template in FAMILY_SOURCES else sample(level,rng))
   try: q,values,m=source_shaped(template,p) if template in FAMILY_SOURCES else authored(level,p); break
   except ValueError:
    if parameters is not None: raise
  else: raise ValueError('No eligible complete bank')
  field={':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':z} for z in values]}; q[':question/answer-fields']=[field]
  field[':answer-field/correct']=[':answer/id','TEMP']
 # Preserve historical IDs only as separate source evidence. Generated identities
 # derive from rendered full content and complete bank independent of seed/order.
 bank=sorted(a[':answer/value'] for a in field[':answer-field/choices']); content=digest([VERSION,level,q.get(':question/difficulty'),q[':question/problem'],q.get(':question/worked-solution'),bank,':answer-field/correct' in field])
 q[':question/id']=str(uuid.uuid5(NS,content)); field[':answer-field/id']=str(uuid.uuid5(NS,content+'selection'))
 ci=m['correct_index']; original_correct=field[':answer-field/choices'][ci][':answer/value']
 for ans in field[':answer-field/choices']: ans[':answer/id']=str(uuid.uuid5(NS,content+'selection'+ans[':answer/value']))
 if ':answer-field/correct' in field: field[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in field[':answer-field/choices'] if a[':answer/value']==original_correct)]
 rng.shuffle(field[':answer-field/choices'])
 task=digest([m['curve'],m['density'],m['bounds'],'fragment' if template in ('line_monomial','line_affine','parabola_missing','authored_line','authored_line_monomial','authored_affine') else 'complete_integral'])
 return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'source':{**{k:SOURCE[k] for k in ('database','basis','lineage')},'question_ids':[QS[OBS_BY_NAME[template][0]][':question/math-academy-id']] if template in OBS_BY_NAME else [QS[FAMILY_SOURCES[template]][':question/math-academy-id']] if template in FAMILY_SOURCES else ['e-9435','q-122530','q-122527','q-122446']},'python_version':sys.version.split()[0],'sympy_version':s.__version__,'mathematical_fingerprint':task,'content_fingerprint':content,'evidence_only':profile.startswith('observed_'),'eligible_for_learning':profile=='authored_operations','authored_level':level=='hard' or template in ('parabola_missing','cubic_integral'),'plot_rating':'none' if template.startswith('authored_') else 'none (unchanged geometry under density scaling)','math':m}}

# EASY: observed fractional monomial and affine fragments, plus polynomial line extension.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: isolated/scaled logs, reciprocal and unshifted polynomial full ds setups.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: shifted nonlinear curve, square substitution, variable metric; setup only.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question']; f=q[':question/answer-fields'][0];gen=r.get('generation',{});level=q.get(':question/difficulty','unrated').split('/')[-1]
 status='Generated — '+('historical evidence' if gen.get('evidence_only') else 'authored normal') if gen else 'Original source'
 lines=['## '+status+' — '+level.title(),q[':question/problem'],'']
 for letter,a in zip('ABCDE',f[':answer-field/choices']):
  ref=f.get(':answer-field/correct');correct=(ref[1]==a[':answer/id']) if isinstance(ref,list) else (ref.get(':answer/id')==a[':answer/id']) if isinstance(ref,dict) else False
  lines.append('- **'+letter+(' (correct)' if correct else '')+'.** $'+a[':answer/value']+'$')
 if ':answer-field/correct' not in f:lines.append('**Original correct designation: absent.**')
 lines+=['','**Worked solution**','',q.get(':question/worked-solution','*(No source worked solution.)*')]
 return '\n'.join(lines)

def main():
 a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['json','markdown'],default='markdown');a.add_argument('--template');a.add_argument('--profile');z=a.parse_args()
 if z.count<1:a.error('Positive count required')
 levels=['easy','moderate','hard'] if z.difficulty=='all' else [z.difficulty]; records=[generate(l,z.seed+i,z.template,profile=z.profile) for l in levels for i in range(z.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if z.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
