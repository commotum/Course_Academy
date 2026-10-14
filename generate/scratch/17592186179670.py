#!/usr/bin/env python3
"""Draft scalar ds line-segment generator; immutable math basis 2275.

Seven recovered MA banks are empirical evidence profiles; default banks are
separately authored method errors. No EDB client, registration, or transactions.
Raw source replay preserves missing difficulty/solution/correct attributes.
Normal levels: bounded linear primitive (authored easy), quadratic/radical/linear
exponential (moderate), familiar-angle sec² or derivative-matched exp(xy) (hard).
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as S
ROOT=Path(__file__).with_suffix('')
KP_ID=17592186179670
KP_UUID='11fb303b-053a-56d1-9b96-acd75c748b51'
TITLE='Calculating a Line Integral Along a Segment in the Cartesian Plane'
VERSION='segment-scalar-2275-draft-1'
x,y,t,u=S.symbols('x y t u',real=True)
SOURCE={'database':'math','basis':2275,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
SECANT_DOMAINS=tuple((dx,dy,abs(dy-dx)*den) for dx in [-2,-1,1,2,3] for dy in [-3,-2,-1,1,2,3,4,5] if dx!=dy and 1<=abs(dy-dx)<=4 for den in [3,4,6])
FAMILIES={'easy':['linear','odd_linear'],'moderate':['product','radical','exponential'],'hard':['secant','matched_exponential']}
ANCHORS={
 'q-39954':('moderate','product',dict(a=1,b=2,dx=1,dy=-1,c=2)),
 'q-76565':('easy','odd_linear',dict(a=1,b=0,dx=-2,dy=0,c=2,d=-3)),
 'q-123363':('moderate','radical',dict(a=2,b=0,dx=0,dy=2,k=2)),
 'q-123366':('moderate','exponential',dict(a=0,b=0,dx=-1,dy=4,c=3,d=1)),
 'q-76564':('moderate','product',dict(a=1,b=2,dx=3,dy=5,c=1)),
 'q-76605':('hard','secant',dict(a=1,b=1,dx=1,dy=3,n=8)),
 'q-76650':('hard','matched_exponential',dict(a=0,b=1,dx=2,dy=2)),
}

def tex(e):
 return S.latex(e,mul_symbol='dot').replace(r'\log',r'\ln')
def simp(e):return S.simplify(S.expand(e))
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,str(s)))
def digest(s):return hashlib.sha256(json.dumps(s,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def equivalent(a,b):
 d=S.simplify(a-b)
 if d==0:return True
 return False

def parameters(f,r):
 if f=='linear':return dict(a=r.randint(-3,3),b=r.randint(-3,3),dx=r.choice([-3,-2,2,3]),dy=r.choice([-3,-2,2,3]),c=r.choice([-3,-2,1,2,3]),d=r.choice([-3,-2,1,2,3]))
 if f=='odd_linear':
  a=r.randint(1,4);return dict(a=a,b=0,dx=-2*a,dy=0,c=r.choice([1,2,3,4]),d=-3)
 if f=='product':return dict(a=r.randint(1,3),b=r.randint(1,3),dx=r.choice([-2,-1,1,2,3]),dy=r.choice([-2,-1,1,2,3,4,5]),c=r.randint(1,3))
 if f=='radical':
  k,dy=r.choice([(1,1),(1,4),(2,2),(2,8),(3,3),(4,1),(4,4)])
  return dict(a=r.randint(1,4),b=0,dx=0,dy=dy,k=k)
 if f=='exponential':
  return dict(a=0,b=0,dx=r.choice([-3,-2,-1,1,2,3]),dy=r.choice([-4,-3,-2,2,3,4]),c=r.choice([-3,-2,-1,1,2,3]),d=r.choice([-2,-1,1,2]))
 if f=='secant':
  a=r.randint(-3,3);dx,dy,n=r.choice(SECANT_DOMAINS)
  return dict(a=a,b=a,dx=dx,dy=dy,n=n)
 if f=='matched_exponential':return dict(a=r.randint(-1,1),b=r.randint(1,3),dx=r.choice([1,2,3]),dy=r.choice([1,2,3]))
 raise ValueError('unknown template')

def validate_parameters(level,f,p):
 expected={'linear':{'a','b','dx','dy','c','d'},'odd_linear':{'a','b','dx','dy','c','d'},'product':{'a','b','dx','dy','c'},'radical':{'a','b','dx','dy','k'},'exponential':{'a','b','dx','dy','c','d'},'secant':{'a','b','dx','dy','n'},'matched_exponential':{'a','b','dx','dy'}}[f]
 if set(p)!=expected or any(type(v)!=int for v in p.values()):raise ValueError('exact integer parameter keys required')
 if p['dx']==p['dy']==0:raise ValueError('zero-length segment')
 a,b,dx,dy=(p[z] for z in ('a','b','dx','dy'))
 if f=='linear':
  if level!='easy' or max(abs(a),abs(b),abs(dx),abs(dy),abs(p['c']),abs(p['d']))>3 or not dx or not dy or not p['c'] or not p['d']:raise ValueError('easy bounds')
  if p['c']*dx+p['d']*dy==0:raise ValueError('nonconstant linear primitive required')
 if f=='odd_linear':
  if level!='easy' or not 1<=a<=4 or b or dy or dx!=-2*a or not 1<=p['c']<=4 or p['d']!=-3:raise ValueError('odd anchor family bounds')
 if f=='product':
  if level!='moderate' or not 1<=p['c']<=3 or not 1<=a<=3 or not 1<=b<=3 or dx not in [-2,-1,1,2,3] or dy not in [-2,-1,1,2,3,4,5]:raise ValueError('product bounds')
  if a+dx<0 or b+dy<0:raise ValueError('nonnegative product path')
 if f=='radical':
  if level!='moderate' or not 1<=a<=4 or b or dx or (p['k'],dy) not in [(1,1),(1,4),(2,2),(2,8),(3,3),(4,1),(4,4)]:raise ValueError('radical perfect-square bounds')
 if f=='exponential':
  slope=p['c']*dx+p['d']*dy
  if level!='moderate' or a or b or dx not in [-3,-2,-1,1,2,3] or dy not in [-4,-3,-2,2,3,4] or not 1<=abs(p['c'])<=3 or not 1<=abs(p['d'])<=2 or not 1<=abs(slope)<=4:raise ValueError('exponential bounds/slope')
 if f=='secant':
  if level!='hard' or not -3<=a<=3 or b!=a or (dx,dy,p['n']) not in SECANT_DOMAINS:raise ValueError('secant familiar angle bounds')
 if f=='matched_exponential':
  if level!='hard' or not -1<=a<=1 or not 1<=b<=3 or dx not in [1,2,3] or dy not in [1,2,3]:raise ValueError('matched exponential bounds')
  if not 1<=dx*b+dy*a<=10 or (a+dx)*(b+dy)>18:raise ValueError('matched quadratic monotone/endpoint bounds')

def instance(f,p):
 a,b,dx,dy=(S.Integer(p[z]) for z in ('a','b','dx','dy'));X=a+dx*t;Y=b+dy*t;speed=S.sqrt(dx**2+dy**2)
 if f in ('linear','odd_linear'):fn=p['c']*x+p['d']*y
 elif f=='product':fn=p['c']*x*y
 elif f=='radical':fn=x+S.sqrt(p['k']*y)
 elif f=='exponential':fn=S.exp(p['c']*x+p['d']*y)
 elif f=='secant':fn=S.sec(S.pi*(y-x)/p['n'])**2
 else:
  m=2*dy;n=dx*b-dy*a;fn=(m*x+n)*S.exp(x*y)
 pulled=S.simplify(fn.subs({x:X,y:Y},simultaneous=True))
 if f=='product':pulled=S.expand(pulled)
 if f=='matched_exponential':pulled=S.diff(S.expand(X*Y),t)*S.exp(S.expand(X*Y))
 if f=='matched_exponential':primitive=S.exp(S.expand(X*Y))
 elif f=='secant':
  inner=S.expand(S.pi*(Y-X)/p['n']);primitive=S.tan(inner)/S.diff(inner,t)
 elif f=='exponential':
  inner=S.expand(p['c']*X+p['d']*Y);primitive=S.exp(inner)/S.diff(inner,t)
 elif f=='radical':primitive=a*t+S.Rational(2,3)*S.sqrt(p['k']*dy)*t**S.Rational(3,2)
 else:primitive=S.integrate(pulled,t)
 lo=simp(primitive.subs(t,0));hi=simp(primitive.subs(t,1));ans=simp(speed*(hi-lo))
 if not equivalent(S.diff(primitive,t),pulled):raise ValueError('primitive derivative mismatch')
 return dict(f=fn,X=X,Y=Y,speed=speed,pulled=pulled,primitive=primitive,lo=lo,hi=hi,answer=ans)

def authored_bank(f,p,z):
 v,s,g=z['answer'],z['speed'],z['pulled'];I=simp(z['hi']-z['lo'])
 if f=='odd_linear':
  # Correct cancellation, false endpoint quadratures, absolute-value substitution,
  # and using the displacement as a signed integration measure.
  c,a=p['c'],p['a'];vals=[0,-2*c*a*a,2*c*a*a,c*a*a,c*a]
 elif f=='product':
  a,b,dx,dy,c=(p[k] for k in ('a','b','dx','dy','c'));C0=c*a*b;C1=c*(a*dy+b*dx);C2=c*dx*dy
  vals=[v,I,s*(S.Rational(C2,3)+C0),s*(S.Rational(C1,2)+C0),s*(S.Rational(C2,2)+S.Rational(C1,2)+C0)]
 elif f=='linear':
  vals=[v,I,s*g.subs(t,0),s*g.subs(t,1),s*(z['hi']+z['lo']) if z['lo']!=0 else s*S.integrate(g,t).subs(t,S.Rational(1,2))]
 elif f=='radical':
  h=S.sqrt(p['k']*p['dy']);a=p['a'];vals=[v,I,s*(a+h),s*(a+h/S.Integer(2)),s*(a+S.Rational(3,2)*h)]
 elif f=='exponential':
  k=p['c']*p['dx']+p['d']*p['dy'];vals=[v,I,s*S.exp(k)/k,s*(S.exp(2*k)-1)/k,s*(S.exp(k)+1)/k]
 elif f=='secant':
  k=S.pi*(p['dy']-p['dx'])/p['n'];delta=S.tan(k);vals=[v,I,s*k*delta,delta*k,s*delta]
 else:
  q0=p['a']*p['b'];q1=(p['a']+p['dx'])*(p['b']+p['dy']);vals=[v,I,s*(S.exp(q1)+S.exp(q0)),s*(S.exp(q1)-S.exp(q0+1)),p['dx']*(S.exp(q1)-S.exp(q0))]
 vals=list(map(simp,vals))
 for i in range(5):
  for j in range(i):
   if equivalent(vals[i],vals[j]):raise ValueError('complete bank collision')
 labels={
 'linear':['correct','omit_speed','left_endpoint_rectangle','right_endpoint_rectangle','integrate_only_half_segment'],
 'product':['correct','omit_speed','omit_cross_term','omit_quadratic_term','quadratic_primitive_divide_by_two'],
 'odd_linear':['correct','left_endpoint_rectangle','right_endpoint_rectangle','integrate_absolute_integrand','absolute_endpoint_omit_length'],
 'radical':['correct','omit_speed','right_endpoint_rectangle','treat_sqrt_as_linear_t','invert_power_rule_multiplier'],
 'exponential':['correct','omit_speed','omit_lower_endpoint','double_upper_parameter','add_lower_endpoint'],
 'secant':['correct','omit_speed','multiply_by_inner_slope','multiply_by_inner_slope_and_omit_speed','omit_inner_slope'],
 'matched_exponential':['correct','omit_speed','add_lower_endpoint','increment_lower_exponent','use_x_displacement_as_speed']}
 return vals,labels[f]

def source_bank(source_id,p,z):
 """Empirical algebraic expression banks, not assertions of author intent.

All operands derive from the instance. Offsets/scales in opaque banks are fitted
source expression features; these profiles are explicitly evidence-only.
"""
 a,b,dx,dy=(S.Integer(p[k]) for k in ('a','b','dx','dy'));s=z['speed'];v=z['answer'];I=simp(v/s)
 if source_id=='q-39954':
  c=p['c'];vals=[c*s,v,S.Rational(3,8)*c*s,c*s/3,S.Rational(5,2)*c]
 elif source_id=='q-76565':
  c=p['c'];vals=[S.sqrt(a*a+c*c),v,c*a,c*a*a*2,S.sqrt(c*a)]
 elif source_id=='q-123363':
  h=S.sqrt(p['k']*dy);vals=[a+1,I-S.Rational(7,6),a+2*h,v-1,v]
 elif source_id=='q-123366':
  k=p['c']*dx+p['d']*dy;vals=[dy*S.exp(k)-1,dy*(S.exp(2*k)-1),dy*(S.exp(k)-1),v,s*(S.exp(2*k)-1)/k]
 elif source_id=='q-76564':vals=[2*v,v,v/dy,s/S.Integer(2),dy*S.sqrt(dx)/S.Integer(2)]
 elif source_id=='q-76605':
  k=S.pi*(dy-dx)/p['n'];D=S.tan(k);vals=[v,D/k,s*k*D,k*D,s*D/S.pi]
 else:
  q0=a*b;q1=(a+dx)*(b+dy);vals=[s*S.exp(q0+1)*(S.exp(q1-q0-1)-1),S.exp(q1)-S.exp(q0),v,v/2,dx*(S.exp(q1)-S.exp(q0))]
 vals=list(map(simp,vals))
 for i in range(5):
  for j in range(i):
   if equivalent(vals[i],vals[j]):raise ValueError('empirical bank collision')
 return vals,['empirical_source_expression']*5

def points(p,spaces=False):
 sep=', ' if spaces else ','
 return '('+str(p['a'])+sep+str(p['b'])+')','('+str(p['a']+p['dx'])+sep+str(p['b']+p['dy'])+')'

def normal_prompt(f,p,z):
 A,B=points(p)
 if f in ['secant','matched_exponential']:return 'Evaluate the integral $'+r'\int_C '+tex(z['f'])+r'\,\mathrm{d}s$ along the line segment from $'+A+'$ to $'+B+'.$'
 return 'Evaluate the integral of the function $f(x,y)='+tex(z['f'])+'$ along the line segment from $'+A+'$ to $'+B+'.$'

def block(rows):
 text=rows[0]
 for row in rows[1:]:text+=(r' \\ '+row[1:]) if row.startswith('#') else (r' \\  & ='+row)
 return '$$\n'+r'\begin{aligned}'+text+r'\end{aligned}'+'\n$$'

def normal_solution(f,p,z):
 A,B=points(p);X,Y=z['X'],z['Y'];a,b,dx,dy=(p[k] for k in ('a','b','dx','dy'));s=z['speed'];g=z['pulled'];P=z['primitive'];v=z['answer'];lo,hi=z['lo'],z['hi']
 vec=lambda a,b:'('+tex(a)+r')\,i+('+tex(b)+r')\,j'
 text='We will use the formula\n\n$$\n'+r'\int_C f(x,y)\,\mathrm{d}s=\int_{t_a}^{t_b} f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t,'+'\n$$\n\nwhere $C$ is the line segment from $'+A+'$ to $'+B+'.$\n\n'
 text+='The position vectors of the endpoints of our line segment are $a='+vec(S.Integer(a),S.Integer(b))+'$ and $b='+vec(S.Integer(a+dx),S.Integer(b+dy))+'.$ So, the parametrization of the line segment is given by\n\n'
 param=[r'r(t) & =a+t\,(b-a)',vec(S.Integer(a),S.Integer(b))+r'+t[('+vec(S.Integer(a+dx),S.Integer(b+dy))+')-('+vec(S.Integer(a),S.Integer(b))+')]',vec(S.Integer(a),S.Integer(b))+r'+t('+vec(S.Integer(dx),S.Integer(dy))+')',vec(X,Y)]
 # Preserve origin simplification workload of source exponential family.
 if f=='exponential':param=[r'r(t) & =a+t\,(b-a)',r'0+t\,(b-0)',r't\,(b)',r't('+vec(S.Integer(dx),S.Integer(dy))+')',vec(X,Y)]
 if f=='radical':param.pop(2)
 text+=block(param)+'\n\nwhere $0\\le t\\le 1.$ Thus, we have that $x='+tex(X)+'$ and $y='+tex(Y)+'$ along the segment.\n\n'
 text+=r"Computing $r\prime(t)$ and $\|r\prime(t)\|,$ we get the following:"+'\n\n'
 text+=block([r"r\prime(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j",r'\frac{\mathrm{d}}{\mathrm{d}t}('+tex(X)+r')i+\frac{\mathrm{d}}{\mathrm{d}t}('+tex(Y)+')j',vec(S.Integer(dx),S.Integer(dy)),r'#\|r\prime(t)\| & =\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}',r'\sqrt{('+str(dx)+')^2+('+str(dy)+')^2}',tex(s)])+'\n\n'
 text+='Now, since $f(x,y)='+tex(z['f'])+'$, we obtain\n\n'
 if f=='product':sub=tex(p['c'])+'('+tex(X)+')('+tex(Y)+')'
 elif f in ('linear','odd_linear'):sub=tex(p['c'])+'('+tex(X)+')+'+tex(p['d'])+'('+tex(Y)+')'
 elif f=='radical':sub=tex(X)+r'+\sqrt{'+str(p['k'])+'('+tex(Y)+')}'
 elif f=='exponential':sub=r'e^{'+str(p['c'])+'('+tex(X)+')+'+str(p['d'])+'('+tex(Y)+')}'
 elif f=='secant':sub=r'\sec^2\left(\frac{\pi(('+tex(Y)+')-('+tex(X)+'))}{'+str(p['n'])+r'}\right)'
 else:sub='('+tex(2*S.Integer(dy))+'('+tex(X)+')+'+tex(S.Integer(dx*b-dy*a))+r')e^{('+tex(X)+')('+tex(Y)+')}'
 g_tex=tex(g)
 if f=='secant':g_tex=r'\sec^2\left('+tex(S.expand(S.pi*(Y-X)/p['n']))+r'\right)'
 if f=='matched_exponential':g_tex='('+tex(S.diff(S.expand(X*Y),t))+r')e^{'+tex(S.expand(X*Y))+'}'
 text+=block([r'f(r(t)) & ='+sub,g_tex+'.'])+'\n\nTherefore, we can write the integral as\n\n'
 rows=[r'\int_C '+tex(z['f'])+r'\,\mathrm{d}s & =\int_0^1 f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t',r'\int_0^1 ('+g_tex+r')\cdot '+tex(s)+r'\,\mathrm{d}t',tex(s)+r'\int_0^1 ('+g_tex+r')\,\mathrm{d}t']
 if f in ('secant','matched_exponential'):
  text+=block(rows)+ '\n\n'
  inner=S.expand(S.pi*(Y-X)/p['n']) if f=='secant' else S.expand(X*Y)
  du=S.diff(inner,t);L=inner.subs(t,0);H=inner.subs(t,1)
  text+='We can solve this using the substitution $u='+tex(inner)+',$ $'+r'\mathrm{d}u=('+tex(du)+r')\,\mathrm{d}t$ as follows: '+'\n\n'
  if f=='secant':
   fac=s/du
   rr=[tex(s)+r'\int_0^1 '+tex(g)+r'\,\mathrm{d}t & ='+tex(fac)+r'\int_{'+tex(L)+'}^{'+tex(H)+r'}\sec^2 u\,\mathrm{d}u',tex(fac)+r'[\tan u]_{'+tex(L)+'}^{'+tex(H)+'}',tex(fac)+r'(\tan('+tex(H)+r')-\tan('+tex(L)+'))',tex(fac)+'('+tex(S.tan(H))+'-'+tex(S.tan(L))+')',tex(v)]
  else:rr=[tex(s)+r'\int_0^1 '+tex(g)+r'\,\mathrm{d}t & ='+tex(s)+r'\int_{'+tex(L)+'}^{'+tex(H)+r'}e^u\,\mathrm{d}u',tex(s)+r'[e^u]_{'+tex(L)+'}^{'+tex(H)+'}',tex(s)+r'(e^{'+tex(H)+r'}-e^{'+tex(L)+'})',tex(v)]
  text+=block(rr)
 else:
  if f=='radical':
   # Source pulls a common coefficient before using the t^(3/2) primitive.
   fac=s*S.Integer(a);inside=1+S.sqrt(p['k']*dy)*S.sqrt(t)/a
   rows[-1]=tex(fac)+r'\int_0^1 ('+tex(inside)+r')\,\mathrm{d}t'
   rows.extend([tex(fac)+'['+tex(P/a)+']_0^1',tex(fac)+'('+tex(hi/a)+')-'+tex(s*lo),tex(v)])
  else:
   if f=='product':
    endpoint='+'.join('('+tex(S.Rational(p['c']*p['dx']*p['dy'],3))+')' if i==0 else '('+tex(e)+')' for i,e in enumerate([S.Rational(p['c']*p['dx']*p['dy'],3),S.Rational(p['c']*(a*dy+b*dx),2),S.Integer(p['c']*a*b)]))
   elif f in ('linear','odd_linear'):
    endpoint='('+tex(S.Rational(p['c']*dx+p['d']*dy,2))+')+('+tex(S.Integer(p['c']*a+p['d']*b))+')'
   else:endpoint=tex(hi)
   rows.extend([tex(s)+'['+tex(P)+']_0^1',tex(s)+'('+endpoint+')-'+tex(s)+'('+tex(lo)+')',tex(v)])
  text+=block(rows)
 return text

# The source skeletons contain only shared prose, operators, structural rows,
# and fixed integration bounds; all instance expressions are substitution slots.
# Slot operand notation hints preserve original MA TeX without an anchor question
# lookup. The evidence profile is never the normal learner default.
def source_render(source_id,p,z):
 data=json.loads((ROOT/'source-templates.json').read_text())[source_id]
 az=instance(data['family'],data['anchor'])
 vals={'A':points(p,source_id in ['q-39954','q-76565'])[0],'B':points(p,source_id in ['q-39954','q-76565'])[1]}
 for name,node in data['slots'].items():
  def evaluated(formula,parameters):
   expr=S.sympify(formula,locals=dict(x=x,y=y,t=t,pi=S.pi,exp=S.exp,sqrt=S.sqrt,sec=S.sec,tan=S.tan))
   return simp(expr.subs({S.Symbol(k):S.Integer(v) for k,v in parameters.items()}))
  if 'components' in node:
   val=[evaluated(e,p) for e in node['components']];anchor=[evaluated(e,data['anchor']) for e in node['components']]
   vals[name]=node['notation'] if all(equivalent(a,b) for a,b in zip(val,anchor)) else '(('+tex(val[0])+r')\,i+('+tex(val[1])+r')\,j)'
  else:
   val=evaluated(node['formula'],p);anchor=evaluated(node['formula'],data['anchor'])
   vals[name]=node['notation'] if equivalent(val,anchor) else ('('+tex(val)+')' if val.is_Add else tex(val))

 hints={'product':('1+3t','2+5t'),'radical':('2','2t'),'exponential':('-t','4t'),'secant':('1+t','1+3t'),'matched_exponential':('2t','1+2t')}
 if data['family'] in hints:
  def operand(value,anchor,hint):return hint if equivalent(value,anchor) else ('('+tex(value)+')' if value.is_Add else tex(value))
  SX=operand(z['X'],az['X'],hints[data['family']][0]);SY=operand(z['Y'],az['Y'],hints[data['family']][1]);f=data['family']
  for name,node in data['slots'].items():
   if node.get('kind')=='substitution':
    if f=='product':vals[name]=('' if p['c']==1 else str(p['c']))+'('+SX+')('+SY+')'
    elif f=='radical':vals[name]=SX+r'+\sqrt{'+str(p['k'])+'('+SY+')}'
    elif f=='exponential':vals[name]=r'{e}^{'+str(p['c'])+'('+SX+')+'+('' if p['d']==1 else str(p['d'])+'('+SY+')')+(SY if p['d']==1 else '')+'}'
    elif f=='secant':vals[name]=r'{sec}^{2}⁡(\frac{\pi (('+SY+')-('+SX+'))}{'+str(p['n'])+'})'
    else:
     m=2*p['dy'];n=p['dx']*p['b']-p['dy']*p['a']
     vals[name]='('+str(m)+'('+SX+')+'+str(n)+r'){e}^{'+SX+'('+SY+')}'
   elif node.get('kind')=='secant_function':vals[name]=r'{sec}^{2}⁡(\frac{\pi (y-x)}{'+str(p['n'])+'})'
   elif node.get('kind')=='secant_collected':
    inner=S.pi*(p['dy']-p['dx'])*t/p['n'];oldinner=S.pi*(data['anchor']['dy']-data['anchor']['dx'])*t/data['anchor']['n']
    vals[name]=r'{sec}^{2}⁡('+operand(inner,oldinner,r'\frac{\pi t}{4}')+')'
   elif node.get('kind')=='matched_expanded':
    inner=S.expand(z['X']*z['Y']);D=S.diff(inner,t)
    dt=operand(D,S.diff(S.expand(az['X']*az['Y']),t),'8t+2');qt=operand(inner,S.expand(az['X']*az['Y']),'2t+4{t}^{2}')
    vals[name]='('+dt+r')\,{e}^{'+qt+'}'
 def render(mask):
  for key,value in vals.items():mask=mask.replace('{{'+key+'}}',value)
  return mask
 return render(data['problem']),render(data['solution']) if data['solution'] is not None else None

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in FAMILIES:raise ValueError('difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
 r=random.Random(seed);raw=profile is not None and profile.startswith('source:')
 sid=profile.split(':',1)[1] if raw else None
 if raw:
  if sid not in ANCHORS:raise ValueError('unknown source profile')
  lev,f,anchor=ANCHORS[sid]
  if level!=lev or template not in (None,f):raise ValueError('profile mismatch')
  template=f
 elif profile not in (None,'method'):raise ValueError('unknown profile')
 f=template or r.choice(FAMILIES[level])
 if f not in FAMILIES[level] and not(f=='odd_linear' and level=='easy'):raise ValueError('family/level')
 for attempt in range(1000):
  p=dict(parameters) if parameters is not None else globals()['parameters'](f,r)
  try:
   validate_parameters(level,f,p);z=instance(f,p)
   vals,recipes=source_bank(sid,p,z) if raw else authored_bank(f,p,z)
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('sampler exhausted')
 if raw:
  prompt,solution=source_render(sid,p,z)
  # Each scalar source expression has its own notation mask, including raw Euler e.
  bankdata=json.loads((ROOT/'source-templates.json').read_text())[sid]
  strings=[mask if equivalent(value,anchorvalue) else tex(value) for mask,value,anchorvalue in zip(bankdata['bank_notation'],vals,source_bank(sid,ANCHORS[sid][2],instance(f,ANCHORS[sid][2]))[0])]
 else:prompt,solution=normal_prompt(f,p,z),normal_solution(f,p,z);strings=list(map(tex,vals))
 fingerprint=digest({'weighted_pulled':S.srepr(simp(z['speed']*z['pulled'])),'speed':S.srepr(z['speed']),'primitive_workload':f,'bounds':[0,1]})
 identity=digest({'version':VERSION,'level':level if not(raw and sid in ['q-39954','q-76565']) else None,'prompt':prompt,'solution':solution,'bank':sorted(strings),'math':fingerprint})
 answers=[{':answer/id':uid(identity+'/answer/'+str(i)),':answer/type':':answer.type/math',':answer/value':v} for i,v in enumerate(strings)]
 correctindex=next(i for i,v in enumerate(vals) if equivalent(v,z['answer']))
 correctid=answers[correctindex][':answer/id'];r.shuffle(answers)
 field={':answer-field/id':uid(identity+'/field'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if not(raw and sid in ['q-39954','q-76565']):field[':answer-field/correct']=[':answer/id',correctid]
 q={':question/id':uid(identity),':question/problem':prompt,':question/answer-fields':[field]}
 if solution is not None:q[':question/worked-solution']=solution
 if not(raw and sid in ['q-39954','q-76565']):q[':question/difficulty']=':question.difficulty/'+level
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'source':SOURCE,'seed':seed,'template':f,'profile':profile or 'method','parameters':p,'mathematical_fingerprint':fingerprint,'content_identity':identity,'source_id':sid,'evidence_only':raw,'eligible_for_learning':not raw,'source_missing_key':sid in ['q-39954','q-76565'],'inferred_correct_id':correctid,'recipes':recipes,'calculator_policy':'unknown; not inferred','python':sys.version.split()[0],'sympy':S.__version__}}

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def markdown(r):
 q=r['question'];out=q[':question/problem']+'\n\n'
 for a in q[':question/answer-fields'][0][':answer-field/choices']:out+='- $'+a[':answer/value']+'$\n'
 return out+'\n'+q.get(':question/worked-solution','[Source worked solution absent.]')+'\n'
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 rows=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (FAMILIES if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(rows,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
