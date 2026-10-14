#!/usr/bin/env python3
"""Green's-theorem area *setup*, fixed math snapshot basis 1356.

Source families and complete operation banks are parameterized; no source-payload
return branch. Public `observed_raw` profiles retain legacy duplicate fields,
missing correct/solution/difficulty attributes and malformed captured notation.
These evidence profiles are explicitly ineligible for learner delivery. Normal
profiles repair presentation and legacy fields, with repair counts separate.

Easy (authored, canonical-example anchored): clockwise circles, one coefficient
1..6 and P=-y,Q=0. Moderate (observed): counterclockwise ellipses with unequal
positive integer semiaxes 1..6, P=0,Q=x. Hard (observed): same source curve/field
families, positive outer scales 1..6, or odd trig powers 3,5,7. Variations remain
fixed-workload setup tasks; no primitive or evaluated area is requested.

Every complete profile is selected before parameters; invalid banks reject the
whole instance. Every source option has an operation-derived formula. Plot
geometry, labels and arrows use the displayed parametrization and domain;
Matplotlib writes only private, atomically committed PNG/JSON assets.

API: generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), generate_easy/moderate/hard. CLI: --difficulty --seed --count
--format markdown|json --template --profile. No EDB operations or registrations.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, random, re, tempfile, uuid, threading
from functools import lru_cache
from pathlib import Path
import sympy as sp

KP_ID=17592186133896
KP_UUID='8644454b-ee25-59fd-ae65-9770a0b44442'
TITLE='Expressing the Area Bounded by a Closed Curve Using Green’s Theorem'
VERSION='green-area-setup-v4'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
t=sp.Symbol('t',real=True)
S,C,S2,C2=sp.sin(t),sp.cos(t),sp.sin(2*t),sp.cos(2*t)
SIN=r'\operatorname{sin}⁡t'; COS=r'\operatorname{cos}⁡t'
SIN2=r'\operatorname{sin}⁡2t'; COS2=r'\operatorname{cos}⁡2t'
TEMPLATES={
 'circle_cw':('easy','q-42238',{'a':2,'b':2}),
 'ellipse_ccw':('moderate','q-41466',{'a':3,'b':2}),
 'ellipse_cw':('hard','q-42238',{'a':2,'b':3}),
 'exp_ccw':('hard','q-42221',{'a':1,'b':1}),
 'exp_cw':('hard','q-126750',{'a':1,'b':1}),
 'double_sine':('hard','q-126751',{'a':2,'b':3}),
 'double_cos':('hard','q-126748',{'a':2,'b':1}),
 'mixed':('hard','q-126760',{'a':1,'b':1}),
 'power':('hard','q-126761',{'a':1,'b':1,'m':5}),
}
PROFILES=('observed','observed_raw','authored')

def coeff(n,body):
 return ('-' if n==-1 else '' if n==1 else str(n))+body

def powtrig(fn,m): return '{'+fn+'}^{'+str(m)+'}⁡t' if m!=1 else (SIN if fn=='sin' else COS)
def exponential(inner):return r'{e}^{'+inner+'}'
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'green-area:'+str(v)))

def mathematical_data(template,p):
 a,b=p['a'],p['b']; m=p.get('m',5)
 if template in ('circle_cw','ellipse_cw'):x,y=a*S,b*C; domain=(0,2*sp.pi);sign=-1;field='P'
 elif template=='ellipse_ccw':x,y=a*C,b*S;domain=(0,2*sp.pi);sign=1;field='Q'
 elif template=='exp_ccw':x,y=a*sp.exp(C),b*sp.exp(S);domain=(0,2*sp.pi);sign=1;field='Q'
 elif template=='exp_cw':x,y=a*sp.exp(S),b*sp.exp(C);domain=(0,2*sp.pi);sign=-1;field='P'
 elif template=='double_sine':x,y=a*S,b*S2;domain=(0,sp.pi);sign=-1;field='Q'
 elif template=='double_cos':x,y=a*S2,b*C;domain=(-sp.pi/2,sp.pi/2);sign=-1;field='P'
 elif template=='mixed':x,y=a*(S-S2),b*(C-C2);domain=(sp.pi/3,5*sp.pi/3);sign=-1;field='Q'
 elif template=='power':x,y=a*S**m,b*C**m;domain=(0,2*sp.pi);sign=-1;field='Q'
 else:raise ValueError('unknown template')
 dx,dy=sp.diff(x,t),sp.diff(y,t)
 first,second=(-sign*y,dx) if field=='P' else (sign*x,dy)
 correct=sp.expand(first*second,power_exp=False) if template!='mixed' else first*second
 return dict(x=x,y=y,dx=dx,dy=dy,domain=domain,sign=sign,field=field,first=first,second=second,correct=correct)

def components(template,p):
 """Unevaluated, source-shaped coordinate/derivative/substitution masks."""
 a,b=p['a'],p['b'];m=p.get('m',5)
 if template in ('circle_cw','ellipse_cw'):
  xy=[coeff(a,SIN),coeff(b,COS)];dxy=[coeff(a,COS),coeff(-b,SIN)]
  product=coeff(b,COS)+r'\cdot '+coeff(a,COS);final=coeff(a*b,powtrig('cos',2))
 elif template=='ellipse_ccw':
  xy=[coeff(a,COS),coeff(b,SIN)];dxy=[coeff(-a,SIN),coeff(b,COS)]
  product=coeff(a,COS)+r'\cdot '+coeff(b,COS);final=coeff(a*b,powtrig('cos',2))
 elif template=='exp_cw':
  es,ec=exponential(SIN),exponential(COS)
  xy=[coeff(a,es),coeff(b,ec)];dxy=[coeff(a,COS+r'\,'+es),coeff(-b,SIN+r'\,'+ec)]
  product=coeff(b,ec)+r'\cdot '+coeff(a,COS+r'\,'+es)
  final=coeff(a*b,COS+r'\,'+exponential(COS+'+'+SIN))
 elif template=='exp_ccw':
  xy=[coeff(a,r'e^{\cos t}'),coeff(b,r'e^{\sin t}')];dxy=[coeff(-a,r'\sin t e^{\cos t}'),coeff(b,r'\cos t e^{\sin t}')]
  product=xy[0]+r'\cdot '+dxy[1];final=coeff(a*b,r'\cos te^{\cos t + \sin t}')
 elif template=='double_sine':
  xy=[coeff(a,SIN),coeff(b,SIN2)];dxy=[coeff(a,COS),coeff(2*b,COS2)]
  product='('+coeff(-a,SIN)+r')\cdot '+coeff(2*b,COS2);final=coeff(-2*a*b,SIN+COS2)
 elif template=='double_cos':
  xy=[coeff(a,SIN2),coeff(b,COS)];dxy=[coeff(2*a,COS2),coeff(-b,SIN)]
  product=coeff(b,COS)+r'\cdot '+coeff(2*a,COS2);final=coeff(2*a*b,COS+COS2)
 elif template=='mixed':
  xy=[coeff(a,SIN+'-'+SIN2) if a==1 else str(a)+'('+SIN+'-'+SIN2+')',coeff(b,COS+'-'+COS2) if b==1 else str(b)+'('+COS+'-'+COS2+')']
  dxy=[COS+'-2'+COS2 if a==1 else str(a)+'('+COS+'-2'+COS2+')','-'+SIN+'+2'+SIN2 if b==1 else str(b)+'(-'+SIN+'+2'+SIN2+')']
  first='(-'+SIN+'+'+SIN2+')' if a==1 else str(a)+'(-'+SIN+'+'+SIN2+')'
  second='(-'+SIN+'+2'+SIN2+')' if b==1 else str(b)+'(-'+SIN+'+2'+SIN2+')'
  product=first+r'\cdot '+second
  final=coeff(a*b,'('+SIN2+'-'+SIN+')(2'+SIN2+'-'+SIN+')')
 elif template=='power':
  xy=[coeff(a,powtrig('sin',m)),coeff(b,powtrig('cos',m))]
  dxy=[coeff(a*m,powtrig('sin',m-1)+COS),coeff(-b*m,powtrig('cos',m-1)+SIN)]
  product='('+coeff(-a,powtrig('sin',m))+r')\cdot ('+coeff(-b*m,powtrig('cos',m-1)+SIN)+')'
  final=coeff(a*b*m,powtrig('sin',m+1)+powtrig('cos',m-1))
 return {'curve':'⟨'+(', ' if template=='exp_ccw' else r',\,').join(xy)+'⟩','derivative':'⟨'+r',\,'.join(dxy)+'⟩','product':product,'final':final}

def bank(template,p,legacy=False):
 """Five recipes, returned together. Forms derive from coordinate swaps,
 derivative swaps, omitted factors and sign errors, never random offsets.
 Observed expressions alone do not establish the original author's intent.
 """
 a,b=p['a'],p['b'];k=a*b;m=p.get('m',5)
 sc=SIN+COS;s2=powtrig('sin',2);c2=powtrig('cos',2)
 if template in ('circle_cw','ellipse_cw'):
  vals=[coeff(-k,s2),coeff(k,sc),coeff(-k,c2),coeff(-k,sc),coeff(k,c2)]
  recipes=['swap_coordinate','omit_coordinate_derivative_sign','omit_orientation','swap_coordinate_with_sign','correct']
 elif template=='ellipse_ccw':
  vals=[coeff(k,sc),coeff(k,'('+s2+'-'+c2+')'),coeff(k,'('+c2+'-'+s2+')'),coeff(k,s2),coeff(k,c2)]
  recipes=['wrong_derivative','antisymmetric_difference_reversed','antisymmetric_difference','wrong_coordinate_and_derivative','correct']
 elif template=='exp_ccw':
  vals=[coeff(k,r'\cos te^{\cos t + \sin t}'),coeff(b,r'\cos te^{\cos t}'),coeff(a,r'\sin te^{\cos t}'),coeff(-b,r'\sin te^{\sin t}'),coeff(-k,r'\sin te^{\cos t + \sin t}')]
  recipes=['correct','omit_x_and_wrong_exponent','wrong_sign_x_derivative','wrong_y_derivative','use_dx_in_place_of_dy']
 elif template=='exp_cw':
  sumexp=exponential(COS+'+'+SIN)
  vals=[coeff(-k,SIN+r'\,'+sumexp),coeff(k,COS+r'\,'+sumexp),coeff(-b*b,SIN+r'\,'+exponential('2'+COS)),coeff(a*a,COS+r'\,'+exponential('2'+SIN)),coeff(-k,COS+r'\,'+sumexp)]
  recipes=['use_y_derivative','correct','use_y_times_y_derivative','use_x_times_x_derivative','omit_orientation']
 elif template=='double_sine':
  vals=[coeff(-2*b*b,SIN2+COS2),coeff(-2*k,SIN+COS2),coeff(-a*a,SIN+COS),coeff(k,SIN2+COS),coeff(-k,SIN2+COS)]
  recipes=['use_y_times_y_derivative','correct','use_x_times_x_derivative','use_y_times_x_derivative','use_negative_y_times_x_derivative']
 elif template=='double_cos':
  vals=[coeff(2*k,COS+COS2),coeff(k,SIN2+SIN),coeff(-b*b,COS+SIN),coeff(-k,SIN2+SIN),coeff(-2*a*a,SIN2+COS2)]
  recipes=['correct','use_negative_x_times_y_derivative','use_y_times_y_derivative','use_x_times_y_derivative','use_negative_x_times_x_derivative']
 elif template=='mixed':
  u='('+SIN2+'-'+SIN+')';v='(2'+SIN2+'-'+SIN+')';w='('+COS2+'-'+COS+')';z='('+COS+'-2'+COS2+')'
  vals=[coeff(k,u+z),coeff(k,w+v),coeff(k,'('+SIN+'-'+SIN2+')'+v),coeff(k,w+z),coeff(k,u+v)]
  recipes=['wrong_coordinate_derivative','wrong_coordinate','omit_orientation','wrong_coordinate_and_derivative','correct']
 elif template=='power':
  vals=[coeff(k*m,powtrig('cos',m+1)+powtrig('sin',m-1)),coeff(-k*m,powtrig('cos',m)+powtrig('sin',m)),coeff(b*m,powtrig('cos',m)+SIN),coeff(-k*m,powtrig('sin',m+1)+powtrig('cos',m-1)),coeff(k*m,powtrig('sin',m+1)+powtrig('cos',m-1))]
  recipes=['swap_axes','multiply_coordinates_with_derivative_coefficient','omit_x_and_wrong_power','omit_orientation','correct']
 if legacy and template in ('circle_cw','ellipse_cw'):
  # Authoritative original widget's equivalent legacy bank, distinct notation/order.
  vals=[coeff(-k,r'\cos^{2} t'),coeff(-k,r'\sin^{2} t'),coeff(k,r'\cos^{2} t'),coeff(-k,r'\sin t\cos t'),coeff(k,r'\sin t\cos t')]
  recipes=['omit_orientation','swap_coordinate','correct','swap_coordinate_with_sign','omit_coordinate_derivative_sign']
 return list(zip(recipes,vals))

def authored_bank(template,p):
 """One complete default operation bank, chosen before sampling scales.
 Each distractor comes from the actual substitution: reverse orientation,
 omit the first coordinate's scale, incorrectly double the derivative, or
 substitute the coordinate itself for its derivative. The full integral
 values, not just the formulas, must all differ. a=1 is thus ineligible.
 """
 d=mathematical_data(template,p)
 scale=p['b'] if d['field']=='P' else p['a']
 coordinate=d['x'] if d['field']=='P' else d['y']
 vals=[d['correct'],-d['correct'],d['correct']/scale,2*d['correct'],d['first']*coordinate]
 return [(name,sp.latex(sp.expand(value,power_exp=False))) for name,value in zip(['correct','reverse_orientation','omit_first_coordinate_scale','double_derivative','use_coordinate_in_place_of_derivative'],vals)]

@lru_cache(maxsize=4096)
def integral_value(expr,domain):
 """Exact full definite value, with exponential Fourier/Bessel reduction."""
 if expr.has(sp.exp):
  # Display families contain only exp(cos), exp(sin), exp(cos+sin),
  # exp(2cos), exp(2sin), multiplied by one trig factor or a constant.
  total=0
  for term in sp.Add.make_args(sp.expand(expr,power_exp=False)):
   term=sp.powsimp(term,combine='exp')
   expatoms=list(term.atoms(sp.exp))
   if len(expatoms)!=1:raise ValueError('unsupported exponential integral')
   ex=expatoms[0];arg=sp.expand(ex.args[0]);A=arg.coeff(C);B=arg.coeff(S)
   if sp.simplify(arg-A*C-B*S)!=0:raise ValueError('unsupported exponential phase')
   R=sp.sqrt(A*A+B*B);factor=sp.simplify(term/ex)
   if not factor.has(t):val=2*sp.pi*sp.besseli(0,R)*factor
   elif factor.coeff(C)!=0 and sp.simplify(factor/factor.coeff(C))==C:
    val=2*sp.pi*A/R*sp.besseli(1,R)*factor.coeff(C)
   elif factor.coeff(S)!=0 and sp.simplify(factor/factor.coeff(S))==S:
    val=2*sp.pi*B/R*sp.besseli(1,R)*factor.coeff(S)
   else:raise ValueError('unsupported exponential multiplier '+str(factor))
   total+=val
  return total
 return sp.integrate(sp.expand_trig(expr),(t,*domain))

def equivalent_scalar(a,b):
 diff=sp.simplify(a-b)
 if diff==0:return True
 if diff.is_zero is False:return False
 # Bessel constants have no known symbolic equality here; high precision
 # confirms strictly separated values. Record numeric separation in validation.
 return abs(complex(sp.N(diff,70)))<1e-50


def parse_math(value):
 """Independent restricted display reader for the actual rendered trig/exp values."""
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 s=value.replace('⁡','').replace(r'\,','').replace(r'\cdot','*')
 s=s.replace(r'\left','').replace(r'\right','')
 s=re.sub(r'(\\(?:sin|cos)(?:\^\{\d+\})?)\{\((2?)\s*t\s*\)\}',r'\1\2t',s)
 s=re.sub(r'(\\(?:sin|cos)(?:\^\{\d+\})?)\((2?)\s*t\s*\)',r'\1\2t',s)
 s=re.sub(r'\\operatorname\{(sin|cos)\}',r'\\\1',s)
 s=re.sub(r'\{(sin|cos)\}',r'\\\1',s)
 # Every trig input in the source is t or 2t; function powers precede the input.
 pat=r'\\(sin|cos)(?:\^\{(\d+)\})?\s*(2?)(?:\s*)t'
 s=re.sub(pat,lambda m:'('+m[1]+'('+('2*' if m[3] else '')+'t)'+('**'+m[2] if m[2] else '')+')',s)
 s=s.replace('{e}','e').replace('^','**').replace('{','(').replace('}',')')
 if re.search(r'[^0-9a-zA-Z+\-*/().\s]',s):raise ValueError('unsupported display '+repr(value))
 return parse_expr(s,local_dict={'t':t,'sin':sp.sin,'cos':sp.cos,'e':sp.E},transformations=standard_transformations+(implicit_multiplication_application,))

def normalized(value):
 s=value.replace('⁡','')
 s=re.sub(r'\\operatorname\{(sin|cos)\}',r'\\\1',s)
 s=re.sub(r'\{(sin|cos)\}',r'\\\1',s)
 # Explicit trig argument parentheses improve renderer and engine support.
 s=re.sub(r'\\(sin|cos)(\^\{\d+\})?\s*(2?)t',lambda m:'\\'+m[1]+(m[2] or '')+'('+('2' if m[3] else '')+'t)',s)
 return s

def source_masks(template):
 source_id=TEMPLATES[template][1];q=QUESTIONS[source_id];orig=TEMPLATES['ellipse_cw' if template=='circle_cw' else template][2]
 c=components(template,orig)
 prompt=q[':question/problem'];curve=re.search('⟨.*?⟩',prompt)[0]
 prompt=prompt.replace(curve,'@@curve@@')
 sol=q.get(':question/worked-solution')
 if sol is not None:
  derivative=re.search('⟨.*?⟩',sol)[0];sol=sol.replace(derivative,'@@derivative@@')
  if c['product'] not in sol:raise AssertionError(('product mask mismatch',source_id,c['product']))
  if c['final'] not in sol:raise AssertionError(('final mask mismatch',source_id,c['final']))
  sol=sol.replace(c['product'],'@@product@@').replace(c['final'],'@@final@@')
 return prompt,sol

def fill(mask,c):
 for key,value in c.items():mask=mask.replace('@@'+key+'@@',value)
 return mask

def standard_solution(template,p):
 d=mathematical_data(template,p);c=components(template,p);positive=d['sign']==1;pf=d['field']=='P'
 orientation='positively' if positive else 'negatively';P,Q=('-y','0') if pf else ('0','x')
 curl='0-(-1)' if pf else '1-0';sign='' if positive else '-'
 boundary=('−y' if positive else 'y')+r'\,\mathrm{d}x' if pf else ('x' if positive else '-x')+r'\,\mathrm{d}y'
 lo,hi=map(sp.latex,d['domain']);integ=lambda z:r'\int_{'+lo+'}^{'+hi+'}'+z+r'\,\mathrm{d}t'
 return (f'Our simple, smooth, closed path $C$ is {orientation} oriented, and  \n\n$$\n'+r'\frac{∂Q}{∂x}-\frac{∂P}{∂y}='+curl+'=1.\n$$\n\n'+
 "So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:\n\n$$\n"+
 r'\begin{aligned}\text{Area}(D)&=\iint_D\mathrm{d}A\\&=\iint_D(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\mathrm{d}A\\&='+sign+r'\oint_C(P\,\mathrm{d}x+Q\,\mathrm{d}y)\end{aligned}'+'\n$$\n\n'+
 ("Notice that we have to take the line integral with a minus sign since the path is negatively oriented.\n\n" if not positive else '')+
 f'Substituting $P(x,y)={P}$ and $Q(x,y)={Q},$ we get\n\n$$\n'+sign+r'\oint_C(P\,\mathrm{d}x+Q\,\mathrm{d}y)=\oint_C'+boundary+'.\n$$\n\nThe derivative of $r(t)$ is\n\n$$\n'+r"r'(t)="+c['derivative']+'.\n$$\n\nTherefore, we can write our line integral as\n\n$$\n'+r'\begin{aligned}\oint_C'+boundary+'&='+integ(c['product'])+r'\\&='+integ(c['final'])+r'.\end{aligned}'+'\n$$')


_PLOT_LOCK=threading.RLock()

def render_plots(template,p,output_dir=None):
 with _PLOT_LOCK:
  return _render_plots(template,p,output_dir)

def _render_plots(template,p,output_dir=None):
 """Render same-instance closed curve with four increasing-t traversal arrows."""
 output_dir=Path(output_dir or ROOT/'plots');output_dir.mkdir(parents=True,exist_ok=True)
 key=digest({'renderer':'matplotlib-v2','template':template,'parameters':p})
 path=output_dir/(key+'.png');sidecar=output_dir/(key+'.json')
 if path.exists() and sidecar.exists():return {'prompt':str(path),'data':str(sidecar)}
 os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'mpl-cache'))
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 import numpy as np
 d=mathematical_data(template,p);lo,hi=map(float,d['domain']);tv=np.linspace(lo,hi,1001)
 xx=np.asarray(sp.lambdify(t,d['x'],'numpy')(tv)); yy=np.asarray(sp.lambdify(t,d['y'],'numpy')(tv))
 xr=float(np.ptp(xx));yr=float(np.ptp(yy));span=max(xr,yr);pad=.18*span
 xmin=min(0,float(xx.min()))-pad;xmax=max(0,float(xx.max()))+pad
 ymin=min(0,float(yy.min()))-pad;ymax=max(0,float(yy.max()))+pad
 fig,ax=plt.subplots(figsize=(4.8,4.2),dpi=140);ax.set_aspect('equal');ax.set_xlim(xmin,xmax);ax.set_ylim(ymin,ymax)
 ax.fill(xx,yy,color='#d7e8f6');ax.plot(xx,yy,color='#ec9b00',lw=1.7)
 for axis in ['top','right']:ax.spines[axis].set_visible(False)
 ax.spines['left'].set_position('zero');ax.spines['bottom'].set_position('zero')
 ax.plot(xmax,0,'>k',clip_on=False,markersize=4);ax.plot(0,ymax,'^k',clip_on=False,markersize=4)
 ax.text(xmax,.035*span,'$x$');ax.text(.035*span,ymax,'$y$')
 label_x,label_y=float(xx.mean()),float(yy.mean())
 if abs(label_x)<.03*xr:label_x=.03*xr
 if abs(label_y)<.03*yr:label_y=.03*yr
 ax.text(label_x,label_y,'$D$',color='#286caa',fontsize=12)
 ci=110;ax.text(float(xx[ci])+.04*span,float(yy[ci])+.04*span,'$C$',color='#df9000',fontsize=12)
 arrows=[]
 for i in [130,370,620,860]:
  # Arrow tip lies later in the actual parameter interval, never inferred from a label.
  start=[float(xx[i]),float(yy[i])];end=[float(xx[i+18]),float(yy[i+18])]
  ax.annotate('',xy=end,xytext=start,arrowprops={'arrowstyle':'->','lw':1,'color':'black'});arrows.append({'t_start':float(tv[i]),'t_end':float(tv[i+18]),'start':start,'end':end})
 ax.tick_params(labelsize=9);fig.tight_layout()
 fd,tmp=tempfile.mkstemp(prefix='render-',suffix='.png',dir=output_dir);os.close(fd)
 try:fig.savefig(tmp,facecolor='white');os.replace(tmp,path)
 finally:plt.close(fig);Path(tmp).unlink(missing_ok=True)
 data={'template':template,'parameters':p,'x':str(d['x']),'y':str(d['y']),'domain':[str(z) for z in d['domain']], 'orientation':d['sign'],'arrows':arrows,'bounds':[xmin,xmax,ymin,ymax],'samples':{'t':tv.tolist(),'x':xx.tolist(),'y':yy.tolist()},'renderer':'Matplotlib','version':matplotlib.__version__}
 fd,tmp=tempfile.mkstemp(prefix='render-',suffix='.json',dir=output_dir);os.close(fd)
 try:Path(tmp).write_text(json.dumps(data,indent=2)+'\n');os.replace(tmp,sidecar)
 finally:Path(tmp).unlink(missing_ok=True)
 return {'prompt':str(path),'data':str(sidecar)}


def guard(level,template,p):
 if set(p)!=({'a','b','m'} if template=='power' else {'a','b'}):raise ValueError('parameters must exactly match template slots')
 if any(type(p[z]) is not int or not 1<=p[z]<=(20 if level=='easy' else 12 if level=='moderate' else 6) for z in ('a','b')):raise ValueError('outer scales must be integers 1..20 at easy,1..12 at moderate,1..6 at hard')
 if level=='easy' and (p['a']!=p['b'] or p['a']>20):raise ValueError('easy requires circles of radius 1..20')
 if level=='moderate' and p['a']==p['b']:raise ValueError('moderate requires unequal semiaxes')
 if level=='hard' and template=='ellipse_cw' and p['a']==p['b']:raise ValueError('hard ellipse requires unequal semiaxes; authored easy uses circles')
 if template=='power' and p['m'] not in (3,5,7):raise ValueError('hard power workload uses odd m=3,5,7')


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('invalid difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('sources support radio only')
 rng=random.Random(seed);eligible=[k for k,v in TEMPLATES.items() if v[0]==level]
 if template is None:template=rng.choice(eligible)
 if template not in eligible:raise ValueError('template not eligible at requested level')
 # Select one complete bank BEFORE sampling. Authored circles inherit the
 # documented canonical shape; defaults use all observed source-shaped families.
 profile=profile or 'authored'
 if profile not in PROFILES:raise ValueError('unknown profile')
 if level=='easy' and profile!='authored':raise ValueError('circle level is authored; no observed easy evidence')
 raw=profile=='observed_raw';source_id=TEMPLATES[template][1];source=QUESTIONS[source_id]
 for attempt in range(100):
  p=dict(parameters) if parameters is not None else {'a':rng.randint(1,12 if level=='moderate' else 6),'b':rng.randint(1,12 if level=='moderate' else 6)}
  if parameters is None:
   if profile=='authored':p['a']=rng.randint(2,20 if level=='easy' else 12 if level=='moderate' else 6)
   if level=='easy':p['b']=p['a']
   if template=='power':p['m']=rng.choice((3,5,7))
  try:
   guard(level,template,p)
   d=mathematical_data(template,p)
   if profile=='authored' and (p['b'] if d['field']=='P' else p['a'])==1:raise ValueError('authored omitted-scale option requires first coordinate scale >1')
   bvals=authored_bank(template,p) if profile=='authored' else bank(template,p)
   expressions=[parse_math(v) for _,v in bvals]
   if any(sp.trigsimp(expressions[i]-expressions[j])==0 for i in range(5) for j in range(i)):raise ValueError('bank collision')
   ci=[i for i,e in enumerate(expressions) if sp.trigsimp(e-d['correct'])==0]
   if len(ci)!=1:raise ValueError('correct pointwise expression not unique')
   if profile=='authored':
    iv=[integral_value(e,d['domain']) for e in expressions]
    if any(equivalent_scalar(iv[i],iv[j]) for i in range(5) for j in range(i)):raise ValueError('complete integral bank collision')
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('no complete eligible bank')
 c=components(template,p);prompt_mask,solution_mask=source_masks(template)
 prompt=fill(prompt_mask,c);solution=fill(solution_mask,c) if solution_mask is not None else None
 if raw:
  # Retain original source image whenever mathematical geometry is unchanged;
  # changed-parameter evidence still obtains its plot from the same instance.
  original=TEMPLATES[template][2]
  plots=None
  if p!=original:
   plots=render_plots(template,p);prompt=re.sub(r'!\[\]\(.*?\)',f"![]({plots['prompt']})",prompt)
 else:
  plots=render_plots(template,p);prompt=re.sub(r'!\[\]\(.*?\)',f"![]({plots['prompt']})",prompt)
  prompt=normalized(prompt);solution=normalized(solution or standard_solution(template,p))
  if template=='exp_ccw':
   # Presentation repair AAAAAAA/legacy integral syntax; no mathematical change.
   curve=normalized(c['curve'])
   prompt=(f"![]({plots['prompt']})\n\nLet $D$ be the region enclosed by the curve $C$ parametrized as\n$r(t)={curve}$ for $t\\in[0,2\\pi].$ The area of $D$ can be written as\n\n$$\n"+r'\text{Area}(D)=\iint_D(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\mathrm{d}A=\int_0^{2\pi}\boxed{}\,\mathrm{d}t,'+'\n$$\n\nwhere $P(x,y)=0$ and $Q(x,y)=x.$ Determine the missing part of the equation.')
  # For setup questions, assess the requested pointwise integrand, not arbitrary
  # integrands having equal definite integral. This already appears in q-126748.
  if 'Determine the missing part of the equation.' in prompt:
   prompt=prompt.replace('Determine the missing part of the equation.','Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green\'s theorem, with the sign adjusted for the orientation of $C$.')
  if level=='easy':solution=normalized(standard_solution(template,p))
 field_specs=[]
 if raw:
  for i,f in enumerate(source[':question/answer-fields']):
   legacy=source_id=='q-42238' and i==0
   vals=bank(template,p,legacy)
   field_specs.append((f,vals,':answer-field/correct' in f))
 else:
  f=source[':question/answer-fields'][-1];field_specs=[(f,[(r,normalized(v)) for r,v in bvals],True)]
 # Identity from actual display and whole complete banks; option order excluded.
 identity={'version':VERSION,'prompt':prompt,'solution':solution,'difficulty':level if not raw or ':question/difficulty' in source else None,'fields':[{'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'bank':sorted(v for _,v in vals),'correct_presence':cp} for f,vals,cp in field_specs]}
 content_fp=digest(identity);qid=uid(content_fp);fields=[]
 for i,(f,vals,cp) in enumerate(field_specs):
  fid=uid(qid+':field:'+str(i));answers=[];correct=None
  for recipe,value in vals:
   aid=uid(fid+':value:'+value)
   answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
   if sp.trigsimp(parse_math(value)-d['correct'])==0:correct=aid
  rng.shuffle(answers)
  field={':answer-field/id':fid,':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/choices':answers}
  if cp:field[':answer-field/correct']=[':answer/id',correct]
  fields.append(field)
 q={':question/id':qid,':question/problem':prompt,':question/answer-fields':fields}
 if solution is not None:q[':question/worked-solution']=solution
 if not raw or ':question/difficulty' in source:q[':question/difficulty']=':question.difficulty/'+level
 # Mathematical object demanded is the pointwise integrand on the stated domain;
 # same product scales/geometry aliases have one task FP even across profiles.
 task={'integrand':str(sp.expand_trig(sp.expand(d['correct']))),'domain':[str(z) for z in d['domain']]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'source_id':source_id,'source':{k:v for k,v in SOURCE.items() if k!='record'},'mathematical_fingerprint':digest(task),'content_fingerprint':content_fp,'domain':[str(z) for z in d['domain']],'orientation':d['sign'],'field':d['field'],'recipes':[r for r,_ in bvals],'plots':plots,'learner_eligible':profile=='authored','authored_level':level=='easy' or source_id=='q-42221','repairs':[] if raw else (['infer_missing_correct','author_missing_solution','repair_placeholder_and_integral'] if source_id=='q-42221' else ['remove_duplicate_legacy_field'] if source_id=='q-42238' else [])+['pointwise_response_criterion','notation_normalization']}}

# EASY — authored canonical-example circle workload; no source easy label.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — observed unequal ellipse, single product with simple derivatives.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — observed source families and same-method positive scaling/odd powers.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question'];g=record['generation'];out=f"## {g['template']} ({g['profile']}; {g['parameters']})\n\n"+q[':question/problem']+'\n\n'
 for f in q[':question/answer-fields']:
  out+='\n'.join(f"- ${a[':answer/value']}$" for a in f[':answer-field/choices'])+'\n\n'
 return out+'Worked solution:\n\n'+q.get(':question/worked-solution','[Absent in raw evidence]')+'\n'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile',choices=PROFILES);args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
