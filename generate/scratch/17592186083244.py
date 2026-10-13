#!/usr/bin/env python3
"""Finite-slope tangent lines and tangent-axis intersections, math basis 1356.

Six public observed profiles preserve captured layout/presence; opaque banks are
EVIDENCE ONLY. Normal families use operation-derived complete banks. Easy is an
explicit canonical-grounded authored extension, not an observed difficulty.
No DB/registration operations. See adjacent evidence folder for bounds/QA.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as S

KP_ID=17592186083244
TITLE='Computing the Tangent Line to a Parametric Curve'
KP_UUID='145eff6a-ad61-5001-ab14-cf77e93a7958'
VERSION='parametric-tangent-1'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
QUESTIONS={str(q[':db/id']):q for q in SOURCE['record'][':knowledge-point/questions']}
T,X,Y=S.symbols('t x y',real=True)
TEMPLATES={'linear_cubic': 'easy','polynomial_radio':'moderate','polynomial_blank':'moderate','quintic_radio':'moderate','exponential_y_intercept':'hard','trig_x_intercept':'hard','log_y_intercept':'hard'}
CASES=[
 {'source_id':'17592186083912','template':'polynomial_radio','level':'moderate','parameters':{'a':2,'b':3,'c':3,'d':-5,'u':1},'bank_profile':'observed_17592186083912'},
 {'source_id':'17592186083913','template':'quintic_radio','level':'moderate','parameters':{'a':1,'b':2,'c':1,'u':-1},'bank_profile':'observed_17592186083913'},
 {'source_id':'17592186256700','template':'exponential_y_intercept','level':'hard','parameters':{'a':3,'h':1,'w':1},'bank_profile':'observed_17592186256700'},
 {'source_id':'17592186275337','template':'trig_x_intercept','level':'hard','parameters':{'a':1,'b':1,'c':1,'h':'1/3','k':1},'bank_profile':'observed_17592186275337'},
 {'source_id':'17592186319229','template':'polynomial_blank','level':'moderate','parameters':{'a':1,'b':4,'c':2,'d':1,'u':2},'bank_profile':'observed_17592186319229'},
 {'source_id':'17592186319230','template':'log_y_intercept','level':'hard','parameters':{'n':1,'k':2},'bank_profile':'observed_17592186319230'},
]
BY_TEMPLATE={c['template']:c for c in CASES}

def tex(v):
 value=S.latex(S.sympify(v),order='lex').replace(r'\log',r'\ln')
 value=re.sub(r' *([+-]) *',r'\1',value).replace(' e','e').replace(r' \pi',r'\pi')
 return value.replace(r'\pi}',r'\pi }')
def num(v): return tex(S.simplify(v))
def cf(v): return '' if v==1 else '-' if v==-1 else num(v)
def term(c,s): return cf(c)+s

def plus(v):return ('+' if v>=0 else '-')+num(abs(v))
def minus(v):return ('-' if v>=0 else '+')+num(abs(v))
def shift(variable,v):return variable+minus(v)
def frac(a,b):return r'\frac{'+str(a)+'}{'+str(b)+'}'
def block(s):return '$$\n'+s+'\n$$'
def align(s):return block(r'\begin{aligned}'+s+r'\end{aligned}')
def sl(v):return num(v).replace(' }','}')
def co(v):return '('+num(v)+')' if v<0 else num(v)
def operator(name):return '\\operatorname{'+name+'}\u2061'
def exp(k,arg='t'):return '{e}^{'+(cf(k)+arg if arg=='t' else str(k)+r'\cdot '+arg)+'}' if k!=1 or arg!='t' else '{e}^{t}'
def point(x,y,space=False):return '('+num(x)+(','+r'\,' if space else ',')+num(y)+')'
def line(m,x0,y0,unit=True):return shift('y',y0)+'='+('' if m==1 and not unit else num(m))+'('+shift('x',x0)+')'
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def ident(o):return str(uuid.uuid5(uuid.NAMESPACE_URL,digest(o)))

class Rejected(ValueError): pass

def exact_parameters(name,parameters):
 keys={'linear_cubic':('a','b','c','d','u'),'polynomial_radio':('a','b','c','d','u'),'polynomial_blank':('a','b','c','d','u'),'quintic_radio':('a','b','c','u'),'exponential_y_intercept':('a','h','w'),'trig_x_intercept':('a','b','c','h','k'),'log_y_intercept':('n','k')}[name]
 if set(parameters)!=set(keys):raise ValueError('Expected parameter keys '+repr(keys))
 p={k:S.sympify(str(v),locals={'pi':S.pi,'e':S.E}) for k,v in parameters.items()}
 if any(v.is_real is not True or v.is_number is not True for v in p.values()):raise ValueError('Exact real numerical parameters required')
 for k,v in p.items():
  if k=='h' and name=='trig_x_intercept':
   if not v.is_Rational or not 2<=v.q<=6 or not 1<=abs(v.p)<=6:raise ValueError('h must be a nonintegral reduced rational, numerator magnitude 1..6, denominator 2..6')
  elif not v.is_Integer:raise ValueError('Integer parameter required: '+k)
 if name=='linear_cubic':
  if not (1<=abs(p['a'])<=4 and 1<=abs(p['c'])<=3 and 1<=abs(p['d'])<=5 and abs(p['b'])<=5 and p['u'] in [-2,-1,1,2]):raise ValueError('Easy bounds')
 elif name.startswith('polynomial'):
  if not (1<=p['a']<=3 and 1<=p['b']<=6 and 1<=p['c']<=4 and 1<=abs(p['d'])<=6 and p['u'] in [-2,-1,1,2]):raise ValueError('Moderate polynomial bounds')
 elif name=='quintic_radio':
  if not (1<=p['a']<=3 and 1<=p['b']<=4 and 1<=p['c']<=3 and p['u'] in [-1,1]):raise ValueError('Moderate quintic bounds: familiar fifth powers')
 elif name=='exponential_y_intercept':
  if not (2<=p['a']<=5 and 1<=p['h']<=4 and 1<=p['w']<=3):raise ValueError('Hard exponential bounds')
 elif name=='trig_x_intercept':
  if not (all(1<=p[k]<=4 for k in ['a','b','c','k'])):raise ValueError('Hard trig coefficient bounds')
 elif not (1<=p['n']<=3 and 1<=p['k']<=4):raise ValueError('Hard log bounds')
 return p

def mathematics(name,p):
 if name=='linear_cubic':xt=p['a']*T+p['b'];yt=p['c']*T**3+p['d']*T;u=p['u']
 elif name.startswith('polynomial'):xt=p['a']*T**3-p['b']*T;yt=p['c']*T**2+p['d'];u=p['u']
 elif name=='quintic_radio':xt=p['a']*T**2-p['b']*T;yt=p['c']*T**5;u=p['u']
 elif name=='exponential_y_intercept':xt=S.exp(p['a']*T)+p['h'];yt=S.exp(T)*S.sin(p['w']*S.pi*T);u=S.Integer(0)
 elif name=='trig_x_intercept':xt=p['a']*S.sin(T)+p['b']*S.cos(T)+p['h'];yt=p['c']*S.cos(T)+p['k'];u=S.pi/2
 else:xt=T*(S.log(T)+p['k']);yt=S.log(T);u=S.exp(p['n'])
 dx=S.diff(xt,T);dy=S.diff(yt,T);xp=S.simplify(xt.subs(T,u));yp=S.simplify(yt.subs(T,u));dxp=S.simplify(dx.subs(T,u));dyp=S.simplify(dy.subs(T,u))
 if dxp==0 or dyp==0:raise Rejected('Finite nonzero slope required; vertical/horizontal search belongs to sibling KP')
 m=S.simplify(dyp/dxp);rhs=S.expand(m*(X-xp)+yp);yi=S.simplify(rhs.subs(X,0));xi=S.simplify(-yi/m)
 return dict(xt=xt,yt=yt,u=u,dx=dx,dy=dy,xp=xp,yp=yp,dxp=dxp,dyp=dyp,m=m,rhs=rhs,yi=yi,xi=xi)

def sample(name,r):
 if name=='linear_cubic':return dict(a=r.choice([-4,-3,-2,-1,1,2,3,4]),b=r.randint(-5,5),c=r.choice([-3,-2,-1,1,2,3]),d=r.choice([-5,-4,-3,-2,-1,1,2,3,4,5]),u=r.choice([-2,-1,1,2]))
 if name.startswith('polynomial'):return dict(a=r.randint(1,3),b=r.randint(1,6),c=r.randint(1,4),d=r.choice([-6,-5,-4,-3,-2,-1,1,2,3,4,5,6]),u=r.choice([-2,-1,1,2]))
 if name=='quintic_radio':return dict(a=r.randint(1,3),b=r.randint(1,4),c=r.randint(1,3),u=r.choice([-1,1]))
 if name=='exponential_y_intercept':return dict(a=r.randint(2,5),h=r.randint(1,4),w=r.randint(1,3))
 if name=='trig_x_intercept':return dict(a=r.randint(1,4),b=r.randint(1,4),c=r.randint(1,4),h=str(r.choice([S.Rational(a,b) for a in range(-6,7) if a for b in range(2,7) if S.Rational(a,b).q>1])),k=r.randint(1,4))
 return dict(n=r.randint(1,3),k=r.randint(1,4))

# Source prose is retained; every mathematical span is slotted as a complete
# component. This avoids replacing short numerals in TeX commands or prose.
def prose_mask(source_id, replacements):
 text=QUESTIONS[source_id][':question/worked-solution']
 spans=list(re.finditer(r'\$\$[\s\S]*?\$\$|\$[^$]*\$',text))
 for i,m in reversed(list(enumerate(spans))):
  if i in replacements:text=text[:m.start()]+replacements[i]+text[m.end():]
 return text

# ============================================================================
# MODERATE — source cubic/quadratic line radio and supplied-RHS blank layouts
# ============================================================================
def polynomial(name,p,z):
 a,b,c,d,u=[p[k] for k in ['a','b','c','d','u']];xp,yp,m=z['xp'],z['yp'],z['m']
 radio=name=='polynomial_radio'
 xpform=term(a,'{t}^{3}')+'-'+num(b)+'t';ypform=term(c,'{t}^{2}')+plus(d)
 prompt='A curve is defined by the parametric equations\n\n'+block('x='+xpform+r',\,y='+ypform+r',\,-\infty <t<\infty .')+'\n\n'+('Calculate the equation of the tangent to the curve at the point where $t='+num(u)+'.$' if radio else 'Find the Cartesian equation of the tangent to the curve at the point where $t='+num(u)+'.$\n\nThe Cartesian equation of the tangent line is $y=$\n{{field-1}}.')
 derx=num(3*a)+'{t}^{2}-'+num(b);dery=num(2*c)+'t'
 xp_sub=cf(a)+'('+num(u)+')^{3}-'+num(b)+'('+num(u)+')';yp_sub=cf(c)+'('+num(u)+')^{2}'+plus(d)
 if radio:
  coords=align('x & ='+xp_sub+'='+num(a*u**3)+'-'+co(b*u)+'='+num(xp)+r', \\ y & ='+yp_sub+'='+num(c*u**2)+plus(d)+'='+num(yp)+r'\,.')
  slope=align(r'm={\frac{dy}{dx}|}_{t='+num(u)+'} & ='+frac(num(2*c)+r'\cdot '+co(u),num(3*a)+r'\cdot ('+num(u)+')^{2}-'+num(b))+r' \\  & ='+frac(num(2*c*u),num(3*a*u**2)+'-'+num(b))+r' \\  & ='+num(m)+r'\,.')
  final=align(shift('y',yp)+' & ='+num(m)+'('+shift('x',xp)+').')
 else:
  coords=align('x & ='+xp_sub+'='+num(a*u**3)+'-'+co(b*u)+'='+num(xp)+r' \\ y & ='+yp_sub+'='+num(c)+'('+num(u**2)+')'+plus(d)+'='+num(yp))
  slope=align(r'm={\frac{dy}{dx}|}_{t\,=\,'+num(u)+'} & ='+frac(num(2*c)+'('+num(u)+')',num(3*a)+'('+num(u)+')^{2}-'+num(b))+r' \\  & ='+frac(num(2*c*u),num(3*a)+'('+num(u**2)+')-'+num(b))+r' \\  & ='+frac(num(2*c*u),num(3*a*u**2)+'-'+num(b))+r' \\  & ='+frac(num(2*c*u),num(z['dxp']))+r' \\  & ='+num(m)+'.')
  # Preserve point-slope, distributed RHS, isolated y stages, including x-0.
  final=align(shift('y',yp)+' & ='+num(m)+'('+shift('x',xp)+r') \\ '+shift('y',yp)+' & ='+tex(S.expand(m*(X-xp)))+r' \\ y & ='+tex(z['rhs'])+'.')
 replacements={0:'$t='+num(u)+'$',1:coords,2:'$'+point(xp,yp)+'.$',6:block('{x}^{′}(t)='+derx+r',\,{y}^{′}(t)='+dery+('.' if radio else '')),7:align(r'\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & ='+frac(dery,derx)+(r'\,.' if radio else '.')),8:'$t='+num(u)+',$',9:slope,10:'$({x}_{1},{y}_{1})='+point(xp,yp)+'$',11:'$m='+num(m)+'.$',12:final}
 if not radio:replacements[13]='$y='+tex(z['rhs'])+'.$'
 solution=prose_mask(BY_TEMPLATE[name]['source_id'],replacements)
 return prompt,solution

# ============================================================================
# HARD — full family-specific source chains, not a shared collapsed CAS answer
# ============================================================================
def exponential(p,z):
 a,h,w=p['a'],p['h'],p['w'];omega=w*S.pi;O=cf(w)+r'\pi ';op=O.rstrip();xp=z['xp'];m=z['m'];yi=z['yi'];sin=operator('sin');cos=operator('cos')
 prompt='A curve is defined by the parametric equations\n\n'+block('x='+exp(a)+plus(h)+r',\,y={e}^{t}'+sin+'('+O+r't),\,-\infty <t<\infty .')+'\n\nLet $C$ be the point that corresponds to $t=0$ on the curve. Determine the point at which the tangent to the curve at $C$ crosses the $y$-axis.'
 dy='{e}^{t}('+sin+'('+O+'t)+'+op+' '+cos+'('+O+'t))';dx=num(a)+exp(a)
 dy_source=dy # product-rule factored chain retained
 ratio=frac(dy,dx);reduced=frac(sin+'('+O+'t)+'+op+' '+cos+'('+O+'t)',num(a)+exp(a-1))
 coords=align('x & ='+exp(a,'0')+plus(h)+'=1'+plus(h)+'='+num(xp)+r', \\ y & ={e}^{0}'+sin+'('+op+r'\cdot 0)=0\,.')
 # source carries an ordinary space between pi and \cdot; stage masks retain it.
 coords=coords.replace(op+r'\cdot',op+r' \cdot')
 slope=align(r'm={\frac{dy}{dx}|}_{t=0} & ='+frac(sin+'('+op+r' \cdot 0)+'+op+' '+cos+'('+op+r' \cdot 0)',num(a)+exp(a-1,'0'))+r' \\  & ='+frac('0+'+O,num(a))+r' \\  & ='+tex(m)+r'\endREMOVE')
 slope=slope.replace(r'\endREMOVE','')
 # Exact source whitespace is a notation concern; expressions/stages are complete.
 replacements={2:coords,3:'$'+point(xp,0)+'.$',7:block('{x}^{′}(t)='+dx+r',\,{y}^{′}(t)='+dy_source+','),8:align(r'\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & ='+ratio+r' \\  & ='+reduced+'.'),10:slope,11:'$({x}_{1},{y}_{1})='+point(xp,0)+'$',12:'$m='+tex(m)+'.$',13:align('y-0 & ='+tex(m)+'(x-'+num(xp)+').'),16:align('y-0 & ='+tex(m)+'(0-'+num(xp)+r') \\ y & ='+tex(yi)+r'\,.'),17:'$'+point(0,yi)+'$'}
 return prompt,prose_mask('17592186256700',replacements)

def trigonometric(p,z):
 a,b,c,h,k=[p[v] for v in ['a','b','c','h','k']];xp,yp,m=z['xp'],z['yp'],z['m'];xi=z['xi'];sin=operator('sin');cos=operator('cos');arg=r'\frac{\pi }{2}'
 xt=term(a,sin+'t')+'+'+term(b,cos+'t')+plus(h);yt=term(c,cos+'t')+'+'+num(k)
 prompt='A curve is defined by the parametric equations\n\n'+block('x='+xt+r',\,y='+yt+r',\,-\infty <t<\infty .')+'\n\nLet $C$ be the point that corresponds to $t='+arg+'$ on the curve. Determine the point at which the tangent to the curve at $C$ crosses the $x$-axis.'
 derx=term(a,cos+'t')+'-'+term(b,sin+'t');dery='-'+term(c,sin+'t');reduced=frac(term(c,sin+'t'),term(b,sin+'t')+'-'+term(a,cos+'t'))
 coords=align('x & ='+term(a,sin+'('+arg+')')+'+'+term(b,cos+'('+arg+')')+plus(h)+'='+num(a)+'+0'+plus(h)+'='+tex(xp)+r', \\ y & ='+term(c,cos+'('+arg+')')+'+'+num(k)+'=0+'+num(k)+'='+num(yp)+r'\,.')
 slope=align(r'm={\frac{dy}{dx}|}_{t=\pi /2} & ='+frac(term(c,sin+'('+arg+')'),term(b,sin+'('+arg+')')+'-'+term(a,cos+'('+arg+')'))+r' \\  & ='+frac(num(c),num(b)+'-0')+r' \\  & ='+num(m)+r'\,.')
 final=align(shift('y',yp)+' & ='+num(m)+r'\cdot ('+shift('x',xp)+').')
 intercept=align('0-'+num(yp)+' & ='+num(m)+r'\cdot ('+shift('x',xp)+r') \\ -'+num(yp)+' & ='+tex(S.expand(m*(X-xp)))+r' \\ x & ='+tex(xi))
 replacements={2:coords,3:'$'+point(xp,yp)+'.$',7:block('{x}^{′}(t)='+derx+r',\,{y}^{′}(t)='+dery+'.'),8:align(r'\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & ='+dery+'('+frac('1',derx)+r') \\  & ='+reduced+r'\,.'),10:slope,11:'$({x}_{1},{y}_{1})='+point(xp,yp)+'$',12:'$m='+num(m)+'.$',13:final,16:intercept,17:'$'+point(xi,0,True)+'$'}
 return prompt,prose_mask('17592186275337',replacements)

def logarithmic(p,z,raw):
 n,k=p['n'],p['k'];u=z['u'];xp=z['xp'];m=z['m'];yi=z['yi'];ln=operator('ln');ut=tex(u);xptex=tex(xp);nkp=num(n+k);nkp1=num(n+k+1)
 prompt='A curve is defined by the parametric equations\n\n'+block('x=t('+ln+'t+'+num(k)+r'),\,y='+ln+r't,\,t\in (0,\infty ).')+'\n\nLet $C$ be the point that corresponds to $t='+ut+'$ on the curve. Determine the coordinates of the point at which the tangent to the curve at $C$ crosses the $y$-axis. '+('Do not round the answers.' if raw else 'Give exact answers.')+'\n\nThe tangent to the curve at $C$ crosses the $y$-axis at $(${{field-1}},\n{{field-2}}$).$'
 coords=align('x & ='+ut+'('+ln+ut+'+'+num(k)+')='+xptex+r' \\ y & ='+ln+ut+'='+num(n))
 ratio=frac('1','t('+ln+'t+'+num(k+1)+')')
 replacements={1:'$t='+ut+'$',2:coords,3:'$'+point(xp,n)+'.$',7:block('{x}^{′}(t)='+ln+'t+'+num(k+1)+r',\,{y}^{′}(t)=\frac{1}{t}'),8:align(r'\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & ='+ratio+'.'),9:'$t='+ut+',$',10:align(r'm={\frac{dy}{dx}|}_{t\,=\,'+ut+'} & ='+frac('1',ut+'('+ln+ut+'+'+num(k+1)+')')+r' \\  & ='+tex(m)+'.'),11:'$({x}_{1},{y}_{1})='+point(xp,n)+'$',12:'$m='+tex(m)+'.$',13:align(shift('y',n)+'='+tex(m)+'('+shift('x',xp)+').'),16:align(shift('y',n)+' & ='+tex(m)+'(0-'+xptex+r') \\ '+shift('y',n)+' & ='+tex(-S.Rational(n+k,n+k+1))+r' \\ y & ='+tex(yi)+'.'),19:'$'+point(0,yi,True)+'.$'}
 return prompt,prose_mask('17592186319230',replacements)

# ============================================================================
# EASY — authored: one constant coordinate derivative, as in canonical e-597
# ============================================================================
def authored_solution(name,p,z):
 u,xp,yp,m=[z[k] for k in ['u','xp','yp','m']]
 xt,yt=z['xt'],z['yt']
 prompt='A curve is defined by the parametric equations\n\n'+block('x='+tex(xt)+r',\qquad y='+tex(yt)+r',\qquad -\infty<t<\infty.')+'\n\nCalculate the equation of the tangent to the curve at the point where $t='+tex(u)+'.$'
 substitution=lambda ex:tex(ex).replace('t','('+tex(u)+')')
 rows=[]
 for v,ex in [('x',xt),('y',yt)]:
  comps=[coefficient*T**powers[0] for powers,coefficient in S.Poly(ex,T).terms()]
  evaluated=''.join(('+' if i and val>=0 else '')+num(val) for i,part in enumerate(comps) for val in [part.subs(T,u)])
  rows.append(v+' & ='+substitution(ex)+'='+evaluated+'='+num(ex.subs(T,u)))
 sol='First, we find the coordinates of the point by substituting $t='+tex(u)+'$ into the parametric equations:\n\n'+align(r' \\ '.join(rows))+'\n\nSo we\'re looking to find the equation of the tangent line to the curve at the point $'+point(xp,yp)+'.$\n\nTo find the slope of the tangent line, we need to find $\\dfrac{\\mathrm{d}y}{\\mathrm{d}x}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:\n\n'+block("x'(t)="+tex(z['dx'])+r",\qquad y'(t)="+tex(z['dy'])+'.')+'\n\nSo, we have\n\n'+block(r"\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{y'(t)}{x'(t)}="+frac(tex(z['dy']),tex(z['dx']))+'.')+'\n\nAt the point where $t='+tex(u)+',$ the slope of the tangent line is given by\n\n'+align('m & ='+frac(substitution(z['dy']),substitution(z['dx']))+'='+frac(num(z['dyp']),num(z['dxp']))+'='+tex(m)+'.')+'\n\nFinally, to calculate the equation of the tangent line, we use point-slope form with the point $(x_1,y_1)='+point(xp,yp)+'$ and the slope $m='+tex(m)+'.$ We get\n\n'+block(line(m,xp,yp)+'.')
 return prompt,sol

def quintic(p,z,raw):
 a,b,c,u=[p[k] for k in ['a','b','c','u']]
 prompt='A curve is defined by the parametric equations\n$x = '+term(a,'t^{2}')+' - '+num(b)+'t, y = '+term(c,'t^{5}')+', - ∞ < t < ∞$.\n\nCalculate the equation of the tangent to the curve at the point where $t ='+num(u)+'$.\n\n> A scientific calculator is required to answer this question.'
 if raw:return prompt,''
 _,sol=authored_solution('quintic_radio',p,z)
 return prompt,sol

# Complete normal bank operations chosen before sampling; reject whole bank on
# collisions. No inferred opaque source error is used in normal defaults.
def normal_bank(name,p,z):
 xp,yp,m,dxp,dyp=[z[k] for k in ['xp','yp','m','dxp','dyp']]
 if 'intercept' not in name:
  slopes=[m,dxp/dyp,-m,m,m]
  points=[(xp,yp),(xp,yp),(xp,yp),(-xp,yp),(xp,-yp)]
  lines=[Y-yy-mm*(X-xx) for mm,(xx,yy) in zip(slopes,points)]
  labels=['correct','reverse_derivative_ratio','reverse_slope_sign','reverse_point_x_sign','reverse_point_y_sign']
  values=[line(mm,xx,yy) for mm,(xx,yy) in zip(slopes,points)]
  return values,lines,labels
 if name=='exponential_y_intercept':
  # At t=0: omit chain coefficient, reverse slope, mistake C for axis point,
  # use slope as intercept. Each is a complete slope/intersection operation.
  vals=[z['yi'],-dyp*xp, m*xp, yp,m]
  values=[point(0,v) for v in vals];objects=[(S.Integer(0),S.simplify(v)) for v in vals]
  labels=['correct','omit_exponential_chain_factor','reverse_slope_sign','return_point_y_coordinate','return_slope_as_intercept']
 elif name=='trig_x_intercept':
  vals=[z['xi'],xp-yp*(p['a']+p['b'])/p['c'],xp+yp/m,xp, -yp/m]
  values=[point(v,0,True) for v in vals];objects=[(S.simplify(v),S.Integer(0)) for v in vals]
  labels=['correct','evaluate_cosine_as_negative_one_in_x_derivative','reverse_intercept_sign','return_point_x_coordinate','omit_point_x_coordinate']
 else:raise ValueError('Log source uses two blanks')
 return values,objects,labels

# Explicit parameterized evidence-only profiles. The opaque recipes are merely
# affine expressions of real tangent components reproducing a historical bank;
# no claim of recovered pedagogical intent and no default promotion is made.
def observed_bank(name,p,z):
 xp,yp,m=z['xp'],z['yp'],z['m']
 if name=='polynomial_radio':
  vals=['y='+frac(num(12*m), '11')+r'\,x+'+frac(num(m),'11'),line(m/2,xp,yp,False),line(m,xp,yp),line(m,yp,yp),line(m/2,yp,yp,False)]
  objects=[Y-S.Rational(12,11)*m*X-m/11,Y-yp-m/2*(X-xp),Y-yp-m*(X-xp),Y-yp-m*(X-yp),Y-yp-m/2*(X-yp)];correct=2
 elif name=='quintic_radio':
  vals=[shift('y',-yp)+' ='+num(m*S.Rational(3,5))+'('+shift('x',xp)+')',shift('y',yp)+' ='+num(m)+'('+shift('x',-xp)+')',shift('y',yp)+' ='+num(m)+'('+shift('x',xp)+')',shift('y',-yp)+' ='+num(2*m)+'('+shift('x',xp)+')',shift('y',yp)+' = '+num(-m)+'('+shift('x',xp)+')']
  objects=[Y+yp-m*S.Rational(3,5)*(X-xp),Y-yp-m*(X+xp),Y-yp-m*(X-xp),Y+yp-2*m*(X-xp),Y-yp+m*(X-xp)];correct=None
 elif name=='exponential_y_intercept':
  omega=p['w']*S.pi
  v=[m,omega/xp,-omega,z['yi'],-m/xp]
  vals=[point(0,w) for w in v];objects=[(S.Integer(0),S.simplify(w)) for w in v];correct=3
 elif name=='trig_x_intercept':
  xi=z['xi'];v=[2*xi/3,xi,6*xi/7,6*xi/5,3*xi/4]
  vals=[point(w,0,True) for w in v];objects=[(S.simplify(w),S.Integer(0)) for w in v];correct=1
 elif name=='polynomial_blank':return [tex(z['rhs'])],[z['rhs']],['correct'],0
 else:return [tex(z['yi']),'0'],[z['yi'],S.Integer(0)],['correct_y','correct_x'],0
 return vals,objects,['raw_component_affine_recipe_'+str(i) for i in range(len(vals))],correct

def equivalent(a,b):
 if isinstance(a,tuple):return all(S.simplify(u-v)==0 for u,v in zip(a,b))
 a,b=S.expand(a),S.expand(b)
 if a.has(X,Y) and b.has(X,Y):
  if S.Poly(a,X,Y,domain='EX').total_degree()!=1 or S.Poly(b,X,Y,domain='EX').total_degree()!=1:return False
  # Whole line relation modulo a nonzero scalar; compare all three coefficients.
  av=[a.coeff(X),a.coeff(Y),a.subs({X:0,Y:0})];bv=[b.coeff(X),b.coeff(Y),b.subs({X:0,Y:0})]
  pivot=next((i for i,v in enumerate(bv) if v!=0),None)
  return pivot is not None and av[pivot]!=0 and S.simplify(a*bv[pivot]-b*av[pivot])==0
 return S.simplify(a-b)==0

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if profile:
  if profile.startswith('observed_'):
   case=next((c for c in CASES if c['bank_profile']==profile),None)
   if not case:raise ValueError('Unknown observed profile')
   if template and template!=case['template']:raise ValueError('Profile/template mismatch')
   template=case['template']
  elif profile!='authored_operations':raise ValueError('Unknown profile')
 if level not in ['easy','moderate','hard']:raise ValueError('Unknown difficulty')
 allowed=[n for n,l in TEMPLATES.items() if l==level]
 if template and template not in allowed:raise ValueError('Template/difficulty mismatch')
 raw=bool(profile and profile.startswith('observed_'))
 r=random.Random(seed);name=template or r.choice(allowed)
 kind='blank' if name in ['polynomial_blank','log_y_intercept'] else 'radio'
 if field_type and field_type not in [kind,':answer-field.type/'+kind]:raise ValueError('Requested field type not source shaped')
 if raw and parameters is None:parameters=dict(BY_TEMPLATE[name]['parameters'])
 for attempt in range(1000):
  p=exact_parameters(name,parameters if parameters is not None else sample(name,r))
  try:
   z=mathematics(name,p)
   if name.startswith('polynomial'):prompt,sol=polynomial(name,p,z)
   elif name=='exponential_y_intercept':prompt,sol=exponential(p,z)
   elif name=='trig_x_intercept':prompt,sol=trigonometric(p,z)
   elif name=='log_y_intercept':prompt,sol=logarithmic(p,z,raw)
   elif name=='quintic_radio':prompt,sol=quintic(p,z,raw)
   else:prompt,sol=authored_solution(name,p,z)
   if raw:values,objects,recipes,correct=observed_bank(name,p,z)
   elif kind=='radio':values,objects,recipes=normal_bank(name,p,z);correct=0
   elif name=='polynomial_blank':values,objects,recipes,correct=[tex(z['rhs'])],[z['rhs']],['correct'],0
   else:values,objects,recipes,correct=[tex(z['yi']),'0'],[z['yi'],S.Integer(0)],['correct_y','correct_x'],0
   if any(S.sympify(v).has(S.zoo,S.nan,S.oo,-S.oo) for obj in objects for v in (obj if isinstance(obj,tuple) else [obj])):raise Rejected('Invalid bank expression')
   if kind=='radio' and any(equivalent(objects[i],objects[j]) for i in range(len(objects)) for j in range(i)):raise Rejected('Whole bank ambiguous')
   break
  except Rejected:
   if parameters is not None:raise
 else:raise Rejected('No eligible bank within bounded sampler')
 params={k:int(v) if v.is_Integer else str(v) for k,v in p.items()}
 # Independent task identity excludes bank and presentation aliases; traversal
 # is not assessed but parameter value/parametric functions define tangent task.
 task=digest({'x':S.srepr(z['xt']),'y':S.srepr(z['yt']),'u':S.srepr(z['u']),'request':('x_intercept' if 'x_intercept' in name else 'y_intercept' if 'y_intercept' in name else 'tangent')})
 source_q=QUESTIONS[BY_TEMPLATE[name]['source_id']] if raw else None
 difficulty=source_q.get(':question/difficulty',{}).get(':db/ident') if raw else ':question.difficulty/'+level
 content=digest({'version':VERSION,'difficulty':difficulty,'problem':prompt,'solution':sol,'kind':kind,'values':sorted(values),'correct':values[correct] if correct is not None else None})
 q={':question/id':ident(['question',content]),':question/problem':prompt,':question/worked-solution':sol}
 if difficulty is not None:q[':question/difficulty']=difficulty
 fields=[]
 if kind=='radio':groups=[('selection',list(range(len(values))),correct)]
 elif name=='log_y_intercept':groups=[('field-2',[0],0),('field-1',[1],1)] # captured collection order retained
 else:groups=[('field-1',[0],0)]
 for key,indices,ci in groups:
  fid=ident(['field',content,key]);answers=[{':answer/id':ident(['answer',fid,values[i]]),':answer/type':':answer.type/math',':answer/value':values[i]} for i in indices]
  f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
  if ci is not None:f[':answer-field/correct']=[':answer/id',ident(['answer',fid,values[ci]])]
  if kind=='radio':r.shuffle(answers)
  fields.append(f)
 q[':question/answer-fields']=fields
 if raw and ':question/worked-solution' not in source_q:q.pop(':question/worked-solution',None)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':S.__version__,'seed':seed,'template':name,'parameters':params,'parameter_fingerprint':task,'content_fingerprint':content,'bank_profile':profile or 'authored_operations','bank_origin':'observed_evidence' if raw else 'authored','evidence_only':raw,'eligible_for_learning':not raw,'authored_extension':name=='linear_cubic' or not raw,'source':{k:SOURCE[k] for k in ['database','basis','lineage']},'source_ids':[BY_TEMPLATE[name]['source_id']] if name in BY_TEMPLATE else ['e-597'],'plot_rating':'none','plot_assets':{},'domain':'t>0' if name=='log_y_intercept' else 'real t; trigonometric arguments in radians','mathematics':{k:S.srepr(v) for k,v in z.items()},'bank_objects':[list(map(S.srepr,v)) if isinstance(v,tuple) else S.srepr(v) for v in objects],'recipes':recipes,'inferred_correct_index':2 if name=='quintic_radio' else None}}

# MODERATE: both coordinate derivatives depend on t; evaluate and form line.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# EASY: one coordinate derivative constant, canonical polynomial method.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# HARD: source product/trig/log derivative and explicit axis intersection.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];meta=r['generation'];anchor=(meta['template'] in BY_TEMPLATE and meta['parameters']==BY_TEMPLATE[meta['template']]['parameters'])
 label=('original raw replay' if anchor else 'changed-parameter raw evidence variant') if meta['evidence_only'] else 'generated variant (authored bank)'
 s='## '+meta['template']+' — '+label+'\n\nProfile: `'+meta['bank_profile']+'`; parameters: `'+json.dumps(meta['parameters'],sort_keys=True)+'`.\n\n'+q[':question/problem']+'\n'
 for f in q.get(':question/answer-fields',[]):
  s+='\n'+f[':answer-field/key']+':\n'
  for a in f[':answer-field/choices']:s+='\n- $'+a[':answer/value']+'$'+(' **correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else '')
 s+='\n\n'+q.get(':question/worked-solution','')+'\n'
 return s

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile');ap.add_argument('--field-type');args=ap.parse_args()
 if args.count<1:ap.error('Positive count required')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
