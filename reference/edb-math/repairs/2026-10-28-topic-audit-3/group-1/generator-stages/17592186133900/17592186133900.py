#!/usr/bin/env python3
"""Advanced Green's theorem with holes; basis 1356. Stops after guide step 7.

Easy (authored): supplied curl c(x²+y²) on an annulus, evaluate in polar coordinates.
Moderate (observed): six field families requiring held partial derivatives, radial
factorization or angular cancellation. Hard (observed): five polynomial families
on a rectangle minus a strict interior rectangle, with separated primitive stages.
Public raw source profiles use an amplitude transformation of extracted math masks;
opaque historical banks are evidence-only and never default distractor recipes.
Normal defaults choose a complete operation bank BEFORE sampling, reject the whole
instance on scalar equivalence, and serve every supported source-shaped family.
"""
from __future__ import annotations
from audit_presentation import prose as _ca_prose, problem as _ca_problem, values as _ca_values, question as _ca_question, identity_material as _ca_material, asset_output as _ca_asset_output

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186133900-source-policy.json'))
    raise SystemExit(0)

import argparse, hashlib, json, random, re, sys, uuid, os, tempfile, threading
from pathlib import Path
import sympy as S
os.environ.setdefault("MPLCONFIGDIR",str(ROOT) if "ROOT" in globals() else "/tmp/advanced-green-mpl")
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
ROOT=Path(__file__).with_suffix(''); SOURCE=json.loads((ROOT/'source.json').read_text()); REC=SOURCE['record']
KP_ID=17592186133900; VERSION='advanced-green-2-format-audit-9837-v1'; x,y,r,t=S.symbols('x y r theta',real=True)
QUESTIONS={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
FAMILIES={
'annulus_quadratic':('moderate','q-126566',-x*x*y,x*y*y,1,2),
'annulus_sin2':('moderate','q-169207',3*x*y*y,-y**3,1,2),
'annulus_fourth':('moderate','q-126935',-x**4*y-x*x*y**3/3,x*y**4+x**3*y*y/3,1,3),
'annulus_negative':('moderate','q-126937',y**3/3+S.cos(x),S.log(1+S.sin(y)**2)-x**3/3,2,4),
'annulus_odd':('moderate','q-126939',x*x-y**4,x**3*y-x*y**3,1,4),
'annulus_four':('moderate','q-126938',-x*x*y-y**3,x**3+x*y*y,1,3),
'rectangle_y2':('hard','q-126645',x*y*y,x*x*y+x*y*y,[-4,4,-3,3],[0,2,-1,2]),
'rectangle_x3y2':('hard','q-126941',x**3*y**3+x,x**4*y*y-y,[-2,2,-1,2],[0,1,0,1]),
'rectangle_xy':('hard','q-126945',x*y*y+x**3,2*x*x*y-y**3,[-2,2,-1,2],[-1,1,0,1]),
'rectangle_shift':('hard','q-126942',y*y*(x+1),3*x*x*y+2*x*y,[0,3,-1,2],[1,2,0,1]),
'rectangle_x2y3':('hard','q-126946',2*x*x*y**4-x,4*x**3*y**3-y*y,[-1,2,-2,2],[0,1,0,1]),
'annulus_supplied':('easy',None,0,0,1,2)}
BY_SOURCE={a[1]:k for k,a in FAMILIES.items() if a[1]}
OPEN=QUESTIONS['q-126566'][':question/worked-solution'].split('We have that')[0]
POLAR=QUESTIONS['q-126566'][':question/worked-solution'].split('Recall that')[1].split('Therefore, our')[0]
def tex(e): return S.latex(S.sympify(e)).replace('\\log','\\ln')
def par(e): return r'\left('+tex(e)+r'\right)'
def scaled(c,v): return v if c==1 else tex(c)+r'\left('+v+r'\right)'
def uid(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,'advanced-green:'+s))
def digest(v): return hashlib.sha256(json.dumps(_ca_material(v),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def scalar(v):
 v=v.strip().replace('\\pi','pi'); v=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'(\1)/(\2)',v);return S.sympify(re.sub(r'(?<=\d)\s*pi', '*pi',v),locals={'pi':S.pi})
def raw_scaled(c,v):
 # Named F and the generic curl of the newly parameterized P,Q already carry
 # amplitude; only explicit source components need multiplication.
 if 'F\\cdot' in v or (r'\frac{∂Q}{∂x}' in v and r'\frac{∂P}{∂y}' in v):return v
 if not v.strip():return v
 return scaled(c,v)
def raw_math_mask(v,c):
 """An extracted amplitude slot acts on COMPLETE components, never short strings.
 General theorem/change-of-variables/domain blocks are fixed. Every subsequent
 assessed equation side gets the same linear field amplitude. Identity amplitude
 renders the extracted source spelling, just as any optional coefficient slot.
 """
 if v.startswith('Δ') or 'f(x,y)' in v or '{∮}_{C}' in v or v in ('C','D','P','Q','R','∂R') or not any(z in v for z in ('=','{∮}','{∬}')): return v
 if '\\begin{aligned}' in v:
  prefix,body=v.split('\\begin{aligned}',1);body,suffix=body.split('\\end{aligned}',1)
  rows=body.split('\\\\');out=[]
  for row in rows:
   if '&' in row:
    left,right=row.split('&',1);space=right[:len(right)-len(right.lstrip())];rhs=right.lstrip();assert rhs.startswith('=')
    out.append(raw_scaled(c,left) if left.strip() else left)
    out[-1]+='&'+space+'='+raw_scaled(c,rhs[1:])
   else: out.append(raw_scaled(c,row))
  return prefix+'\\begin{aligned}'+'\\\\'.join(out)+'\\end{aligned}'+suffix
 if v.startswith(('P(x,y)=','Q(x,y)=')):
  left,right=v.split('=',1);return left+'='+raw_scaled(c,right)
 if '\\frac{∂P}' in v:
  parts=v.split('\\,');return '\\,'.join(a.split('=',1)[0]+'='+raw_scaled(c,a.split('=',1)[1]) if '=' in a else a for a in parts)
 if '=' in v:
  return '='.join(raw_scaled(c,z) for z in v.split('='))
 return raw_scaled(c,v)
def raw_text(v,c):
 return re.sub(r'\$\$(.*?)\$\$|\$(.*?)\$',lambda m: ('$$'+raw_math_mask(m[1],c)+'$$') if m[1] is not None else ('$'+raw_math_mask(m[2],c)+'$'),v,flags=re.S)
RENDER_LOCK=threading.RLock()
def render_plot(f,p):
 with RENDER_LOCK:return _render_plot(f,p)
def _render_plot(f,p):
 data={'family':f,'parameters':p,'renderer':'matplotlib','version':matplotlib.__version__,'plot_version':2};key=digest(data);dest=_ca_asset_output(ROOT/'plots'/'plot').parent;dest.mkdir(exist_ok=True);png=dest/(key+'.png');side=dest/(key+'.json')
 if png.exists() and side.exists():return str(png)
 fig,ax=plt.subplots(figsize=(4.0,3.6),dpi=140);ax.set_aspect('equal');edge='#ed9e00';fill='#d6e8f5'
 if f.startswith('annulus'):
  a,b=p['inner'],p['outer']; ax.add_patch(Circle((0,0),b,facecolor=fill,edgecolor=edge,lw=1.4));ax.add_patch(Circle((0,0),a,facecolor='white',edgecolor=edge,lw=1.4));lim=b*1.3; ax.set_xlim(-lim,lim);ax.set_ylim(-lim,lim);ax.set_xticks(sorted(set([-b,-a,a,b])));ax.set_yticks([]);ax.text(-.65*b,.55*b,'R' if f=='annulus_sin2' else 'D',color='#2480a5',fontstyle='italic')
  if f=='annulus_sin2':
   X,Y=S.symbols('X Y');import numpy as np
   g=np.linspace(-b*1.15,b*1.15,13);xx,yy=np.meshgrid(g,g);c=p['c'];u=3*c*xx*yy**2;v=-c*yy**3;mag=np.hypot(u,v);ax.quiver(xx,yy,np.divide(u,mag,out=np.zeros_like(u),where=mag!=0),np.divide(v,mag,out=np.zeros_like(v),where=mag!=0),color='#84bdf1',scale=35,width=.002)
 else:
  a,b,d,e=p['outer'];h,j,k,l=p['hole'];ax.add_patch(Rectangle((a,d),b-a,e-d,facecolor=fill,edgecolor=edge,lw=1.4));ax.add_patch(Rectangle((h,k),j-h,l-k,facecolor='white',edgecolor=edge,lw=1.4));pad=max(b-a,e-d)*.2;ax.set_xlim(min(a,0)-pad,max(b,0)+pad);ax.set_ylim(min(d,0)-pad,max(e,0)+pad);ax.set_xticks(sorted(set([a,b,h,j])));ax.set_yticks(sorted(set([d,e,k,l])));ax.text(a+(b-a)*.18,e-(e-d)*.2,'D',color='#2480a5',fontstyle='italic')
 for spine in ('top','right'):ax.spines[spine].set_visible(False)
 ax.spines['bottom'].set_position('zero');ax.spines['left'].set_position('zero');ax.tick_params(labelsize=9,length=2);ax.set_xlabel('x',loc='right');ax.set_ylabel('y',loc='top',rotation=0);fig.tight_layout()
 fd,tmp=tempfile.mkstemp(dir=dest,suffix='.png');os.close(fd)
 try:fig.savefig(tmp);os.replace(tmp,png)
 finally:plt.close(fig);Path(tmp).unlink(missing_ok=True)
 fd,tmp=tempfile.mkstemp(dir=dest,suffix='.json');os.close(fd);Path(tmp).write_text(json.dumps(_ca_material(data),indent=2));os.replace(tmp,side)
 return str(png)
def aligned(rows):return '$$\n'+r'\begin{aligned}'+rows[0]+''.join(r'\\ & ='+z for z in rows[1:])+r'.\end{aligned}'+'\n$$'
def integ(lo,hi,z,var):return r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}'+z+r'\,\mathrm d '+var
def evaluate(z,var,a,b):return z+r'\big|_{'+tex(a)+'}^{'+tex(b)+'}'
def endpoint(e,var,a,b):return '('+par(e.subs(var,b))+'-'+par(e.subs(var,a))+')'
def bound(a):return r'\{(x,y):'+tex(a[0])+r'\le x\le '+tex(a[1])+','+tex(a[2])+r'\le y\le '+tex(a[3])+r'\}'
def subtract_display(left,right):
 # Parentheses cover the COMPLETE negative-leading hole product. Positive
 # source anchors keep their original subtraction presentation unchanged.
 return left+'-'+(r'\left('+right+r'\right)' if right.lstrip().startswith('-') else right)
def rect_solution(f,p,P,Q,Py,Qx,C):
 # Per-family split factors reproduce the source's primitive conventions.
 gx,gy={'rectangle_y2':(1,y**2),'rectangle_x3y2':(x**3,y**2),'rectangle_xy':(2*x,y),'rectangle_shift':(2*x,2*y),'rectangle_x2y3':(x**2,4*y**3)}[f];gx=S.sympify(gx)*p['c'];gy=S.sympify(gy);G=S.integrate(gx,x);H=S.integrate(gy,y);A=p['outer'];B=p['hole']
 def repeated(a):return integ(a[2],a[3],integ(a[0],a[1],tex(C),'x'),'y')
 def product(a):return integ(a[0],a[1],tex(gx) if gx!=1 else '', 'x')+r'\cdot '+integ(a[2],a[3],tex(gy),'y')
 GT={'rectangle_y2':tex(p['c']*x),'rectangle_x3y2':r'\frac{'+('' if p['c']==1 else tex(p['c']))+r'x^4}{4}','rectangle_xy':tex(p['c']*x*x),'rectangle_shift':tex(p['c']*x*x),'rectangle_x2y3':r'\frac{'+('' if p['c']==1 else tex(p['c']))+r'x^3}{3}'}[f]
 HT={'rectangle_y2':r'\frac{y^3}{3}','rectangle_x3y2':r'\frac{y^3}{3}','rectangle_xy':r'\frac{y^2}{2}','rectangle_shift':'y^2','rectangle_x2y3':'y^4'}[f]
 def prim(a):return evaluate(GT,'x',a[0],a[1])+r'\cdot '+evaluate(HT,'y',a[2],a[3])
 def ends(a):return endpoint(G,x,a[0],a[1])+r'\cdot '+endpoint(H,y,a[2],a[3])
 def diffs(a):return [S.simplify(G.subs(x,a[1])-G.subs(x,a[0])),S.simplify(H.subs(y,a[3])-H.subs(y,a[2]))]
 av,bv=diffs(A),diffs(B);outer=S.prod(av);hole=S.prod(bv);ans=outer-hole
 sol='The region $D$ can be represented in Cartesian coordinates as $\\Delta_1\\setminus\\Delta_2,$ where\n\n- $\\Delta_1='+bound(A)+'$ is the region enclosed by the outer curve, and\n\n- $\\Delta_2='+bound(B)+'$ is the region enclosed by the inner curve.\n\nTherefore, our double integral becomes\n\n'
 sol+=aligned([r'\iint_D '+tex(C)+r'\,\mathrm dA & =\iint_{\Delta_1}'+tex(C)+r'\,\mathrm dA-\iint_{\Delta_2}'+tex(C)+r'\,\mathrm dA',subtract_display(repeated(A),repeated(B)),subtract_display(product(A),product(B)),subtract_display(prim(A),prim(B)),subtract_display(ends(A),ends(B)),par(av[0])+r'\cdot '+par(av[1])+'-'+par(bv[0])+r'\cdot '+par(bv[1]),tex(ans)])
 return sol,ans,outer,hole,{'gx':str(gx),'gy':str(gy),'G':str(G),'H':str(H),'primitive_tex':{'x':GT,'y':HT},'endpoint_components':[[str(G.subs(x,a[1])),str(G.subs(x,a[0])),str(H.subs(y,a[3])),str(H.subs(y,a[2]))] for a in (A,B)]}
def held_scale(c,base):
 return base if c==1 else tex(c)+r'\cdot\left('+base+r'\right)'
def held_power(v,n):
 return '('+tex(v)+')^{'+str(n)+'}'
def held_fraction(coefficient,v,n,denominator):
 numerator=(tex(coefficient)+r'\cdot ' if coefficient!=1 else '')+held_power(v,n)
 return r'\frac{'+numerator+'}{'+str(denominator)+'}'
def difference(u,v):
 return r'\left('+u+'-'+r'\left('+v+r'\right)'+r'\right)'
def polar_solution(f,p,C):
 """Each branch preserves its source's operative primitive/factor convention.

 Supplemental evaluated primitive components ADD to those original stages.
 Held powers/fractions prevent SymPy from collapsing the factoring operation.
 """
 a,b,c=p['inner'],p['outer'],p['c'];trig=r'\cos^2\theta+\sin^2\theta'
 domain='$$\\Delta=\\{(r,\\theta):'+tex(a)+r'\le r\le '+tex(b)+r',0\le\theta'+('<' if f=='annulus_sin2' else r'\le')+r'2\pi\}.'+'$$'
 R=lambda z:integ(0,2*S.pi,integ(a,b,z,'r'),r'\theta')
 def product(angular,radial):return integ(0,2*S.pi,angular,r'\theta')+r'\cdot '+integ(a,b,radial,'r')
 required=[];added=[]
 if f=='annulus_sin2':
  angular=S.sin(2*t);radial=r**3;factor=-3*c;G=-S.cos(2*t)/2;H=r**4/4
  integrand=tex(factor)+r'r^3\sin(2\theta)'
  conversion=r'\oint_{\partial R}('+tex(c*FAMILIES[f][2])+r')\,\mathrm dx+('+tex(c*FAMILIES[f][3])+r')\,\mathrm dy=\iint_\Delta '+integrand+r'\,\mathrm dr\,\mathrm d\theta'
  sol="As we saw earlier, we can use Green's theorem to write our line integral in polar coordinates as \n\n$$"+conversion+".$$\n\nBut this time, our region $R$ (in polar coordinates) is given by \n\n"+domain+"\n\nTherefore, we get\n\n"
  repeated=tex(factor)+r'\cdot '+R(r'r^3\sin(2\theta)')
  separated=tex(factor)+r'\cdot '+product(r'\sin(2\theta)',r'r^3')
  # Source cos(2theta)/(-2), including its denominator, stays explicit.
  angular_primitive=r'\frac{\cos(2\theta)}{-2}'
  primitive=tex(factor)+r'\cdot '+evaluate(angular_primitive,r'\theta',0,2*S.pi)+r'\cdot '+evaluate(r'\frac{r^4}{4}','r',a,b)
  primitive_values=tex(factor)+r'\cdot '+endpoint(G,t,0,2*S.pi)+r'\cdot '+endpoint(H,r,a,b)
  # Original pulls BOTH denominator factors outside the held powers.
  factored=held_scale(c,r'\frac{3}{2}')+r'\cdot (1-1)\cdot\frac{1}{4}\cdot '+difference(held_power(b,4),held_power(a,4))
  power_values=tex(S.Rational(3*c,2))+r'\cdot (1-1)\cdot\frac{1}{4}\cdot '+difference(tex(b**4),tex(a**4))
  required=[repeated,separated,primitive,factored];added=[primitive_values,power_values]
  rows=[r'\iint_\Delta '+integrand+r'\,\mathrm dr\,\mathrm d\theta & ='+repeated,separated,primitive,primitive_values,factored,power_values,'0']
 elif f=='annulus_odd':
  angular=S.sin(t);radial=3*c*r**4;factor=1;G=-S.cos(t);H=3*c*r**5/5
  sub=tex(3*c)+r'\cdot r\sin\theta\cdot ((r\cos\theta)^2+(r\sin\theta)^2)\cdot r'
  fact=tex(3*c)+r'r^2\sin\theta\cdot r^2('+trig+')'
  reduced=tex(3*c)+r'r^4\sin\theta'
  separated=product(r'\sin\theta',tex(3*c)+r'r^4')
  primitive=evaluate(r'-\cos\theta',r'\theta',0,2*S.pi)+r'\cdot '+evaluate(r'\frac{'+tex(3*c)+r'r^5}{5}','r',a,b)
  held_radial=difference(held_fraction(3*c,b,5,5),held_fraction(3*c,a,5,5))
  symbolic_angular=difference(r'-\cos(2\pi)',r'-\cos(0)')
  numeric_angular=difference('-1','-1')
  symbolic_endpoints=symbolic_angular+r'\cdot '+held_radial
  angular_values=numeric_angular+r'\cdot '+held_radial
  primitive_values=endpoint(G,t,0,2*S.pi)+r'\cdot '+endpoint(H,r,a,b)
  required=[R(sub),R(fact),R(reduced),separated,primitive,symbolic_endpoints,angular_values];added=[primitive_values]
  rows=[r'\iint_D '+tex(C)+r'\,\mathrm dA & ='+R(sub),R(fact),R(reduced),separated,primitive,symbolic_endpoints,angular_values,primitive_values,'0']
 else:
  n=6 if f=='annulus_fourth' else 4;angular=S.Integer(1);radial=r**(n-1);factor=-c if f=='annulus_negative' else 4*c if f=='annulus_four' else c;G=t;H=r**n/n;k=2*S.pi*factor
  sub=r'((r\cos\theta)^2+(r\sin\theta)^2)'+('^2' if n==6 else '')+r'\cdot r'
  fact='r^{'+str(n-2)+'}('+trig+')'+('^2' if n==6 else '')+r'\cdot r'
  reduced='r^{'+str(n-1)+'}'
  if f=='annulus_four':
   # Source external4 applies to the WHOLE double integral, never its integrand.
   repeated=tex(4*c)+r'\cdot '+R(sub);factored_integrand=tex(4*c)+r'\cdot '+R(fact);reduced_integral=tex(4*c)+r'\cdot '+R(reduced)
   separated=tex(4*c)+r'\cdot '+product('',reduced)
  else:
   repeated=R(scaled(factor,sub));factored_integrand=R(scaled(factor,fact));reduced_integral=R(tex(factor*radial));separated=product('',tex(factor*radial))
  angular_evaluated=tex(k)+r'\cdot '+integ(a,b,reduced,'r')
  # All radial source families use the unscaled r^n/n primitive.
  primitive=tex(k)+r'\cdot '+evaluate(r'\frac{r^{'+str(n)+'}}{'+str(n)+'}','r',a,b)
  primitive_values=tex(k)+r'\cdot '+endpoint(H,r,a,b)
  # This is the source operation: collect 2pi*(factor/n) OUTSIDE powers.
  base_factor=-S.pi/2 if f=='annulus_negative' else 2*S.pi if f=='annulus_four' else S.pi/3 if n==6 else S.pi/2
  factored_endpoints=held_scale(c,tex(base_factor))+r'\cdot '+difference(held_power(b,n),held_power(a,n))
  power_values=tex(k/n)+r'\cdot '+difference(tex(b**n),tex(a**n))
  required=[repeated,factored_integrand,reduced_integral,separated,angular_evaluated,primitive,factored_endpoints];added=[primitive_values,power_values]
  ans=S.simplify(k*(H.subs(r,b)-H.subs(r,a)))
  rows=[r'\iint_D '+tex(C)+r'\,\mathrm dA & ='+repeated,factored_integrand,reduced_integral,separated,angular_evaluated,primitive,primitive_values,factored_endpoints,power_values,tex(ans)]
 if f!='annulus_sin2':sol='The region $D$ can be represented in polar coordinates as \n\n'+domain+'\n\nRecall that'+POLAR+'Therefore, our double integral becomes\n\n'
 angularval=S.integrate(angular,(t,0,2*S.pi));rv=H.subs(r,b)-H.subs(r,a);ans=S.simplify(factor*angularval*rv)
 sol+=aligned(rows)
 return sol,ans,rv*factor,angularval,{'radial':str(radial),'angular':str(angular),'factor':str(factor),'G':str(G),'H':str(H),'endpoint_components':[str(G.subs(t,2*S.pi)),str(G.subs(t,0)),str(H.subs(r,b)),str(H.subs(r,a))],'source_operative_rows':required,'supplemental_rows':added}
def parameters_guard(f,p):
 if set(p)!={'c','inner','outer'} and f.startswith('annulus'):raise ValueError('annulus requires c,inner,outer')
 if not f.startswith('annulus') and set(p)!={'c','outer','hole'}:raise ValueError('rectangle requires c,outer,hole')
 if not isinstance(p['c'],int) or not 1<=abs(p['c'])<=3:raise ValueError('nonzero integer amplitude |c|<=3')
 if f.startswith('annulus'):
  if not all(isinstance(p[z],int) for z in ('inner','outer')) or not 1<=p['inner']<p['outer']<=5:raise ValueError('integer radii 1<=inner<outer<=5')
 else:
  A,B=p['outer'],p['hole']
  if len(A)!=4 or len(B)!=4 or not all(isinstance(z,int) and abs(z)<=6 for z in A+B) or not (A[0]<B[0]<B[1]<A[1] and A[2]<B[2]<B[3]<A[3]):raise ValueError('strict interior rectangles; integer bounds |bound|<=6')
def sample(f,rng):
 d=FAMILIES[f];c=rng.choice([-3,-2,-1,1,2,3])
 if f.startswith('annulus'):a=rng.randint(1,3);return {'c':c,'inner':a,'outer':rng.randint(a+1,5)}
 A=d[4][:];B=d[5][:];sx=rng.choice([-1,0,1]);sy=rng.choice([-1,0,1]);A=[A[0]+sx,A[1]+sx,A[2]+sy,A[3]+sy];B=[B[0]+sx,B[1]+sx,B[2]+sy,B[3]+sy];return {'c':c,'outer':A,'hole':B}
def record(level,f,p,profile,prompt,solution,fields,seed,mathkey,extra=None):
 if not str(profile).startswith('observed:'):
  prompt=_ca_problem(prompt);solution=_ca_prose(solution)
  for field in fields:
   for a in field[':answer-field/choices']:a[':answer/value']=_ca_values([a[':answer/value']])[0]
 bank=sorted([{'key':v[':answer-field/key'],'type':v[':answer-field/type'],'values':sorted(a[':answer/value'] for a in v[':answer-field/choices']),'correct':next((a[':answer/value'] for a in v[':answer-field/choices'] if v.get(':answer-field/correct',[None,None])[1]==a[':answer/id']),None)} for v in fields],key=lambda z:z['key']);h=digest([VERSION,level,prompt,solution,bank]);qid=uid(h);out=[]
 for i,v in enumerate(fields):
  correct=v.get(':answer-field/correct');oldcorrect=correct[1] if correct else None;v=dict(v);v[':answer-field/id']=uid(qid+':field:'+str(i));answers=[];newcorrect=None
  for a in v[':answer-field/choices']:
   a=dict(a);oldid=a[':answer/id'];a[':answer/id']=uid(v[':answer-field/id']+':'+a[':answer/value']);answers.append(a)
   if oldid==oldcorrect:newcorrect=a[':answer/id']
  if newcorrect:v[':answer-field/correct']=[':answer/id',newcorrect]
  v[':answer-field/choices']=answers;random.Random(seed+i).shuffle(answers);out.append(v)
 return {'knowledge_point':{'db_id':KP_ID,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':out},'generation':{'version':VERSION,'template':f,'profile':profile,'parameters':p,'seed':seed,'mathematical_fingerprint':digest(mathkey),'presentation_fingerprint':h,'provenance':{k:SOURCE[k] for k in ('database','basis','lineage')},'runtime':{'python':sys.version.split()[0],'sympy':S.__version__,'matplotlib':matplotlib.__version__},**(extra or {})}}
def task_key(level,f,p,Py,Qx,C):
 if f in ('annulus_sin2','annulus_odd'):return [level,f,'full-turn-angular-cancellation']
 return [level,str(S.expand(C)),str(S.expand(Py)) if f!='annulus_supplied' else None,str(S.expand(Qx)) if f!='annulus_supplied' else None,p.get('inner'),p.get('outer'),p.get('hole'),f=='annulus_supplied']
def raw_generate(level,f,p,profile,seed):
 sid=profile.removeprefix('raw:');q=QUESTIONS[sid];assert f==BY_SOURCE[sid]
 if set(p)!={'amplitude'} or not isinstance(p['amplitude'],int) or not 1<=abs(p['amplitude'])<=3:raise ValueError('raw replay accepts integer amplitude |amplitude|<=3')
 c=p['amplitude'];fields=[];d=FAMILIES[f];mathp=({'c':c,'inner':d[4],'outer':d[5]} if f.startswith('annulus') else {'c':c,'outer':d[4],'hole':d[5]});Py=S.diff(c*d[2],y);Qx=S.diff(c*d[3],x);curl=S.factor(Qx-Py)
 if f.startswith('annulus'):
  polar=S.trigsimp(curl.subs({x:r*S.cos(t),y:r*S.sin(t)})*r);expected=S.integrate(S.integrate(polar,(r,d[4],d[5])),(t,0,2*S.pi))
 else:
  def integral(B):return S.integrate(curl,(x,B[0],B[1]),(y,B[2],B[3]))
  expected=integral(d[4])-integral(d[5])
 for field in q[':question/answer-fields']:
  if ':answer-field/correct' in field:assert S.simplify(c*scalar(field[':answer-field/correct'][':answer/value'])-expected)==0

 for v in q[':question/answer-fields']:
  choices=[{':answer/id':a[':answer/id'],':answer/type':a[':answer/type'][':db/ident'],':answer/value':a[':answer/value'] if c==1 else tex(expected if a[':answer/id']==v.get(':answer-field/correct',{}).get(':answer/id') else c*scalar(a[':answer/value']))} for a in v[':answer-field/choices']];fd={':answer-field/id':v[':answer-field/id'],':answer-field/key':v[':answer-field/key'],':answer-field/type':v[':answer-field/type'][':db/ident'],':answer-field/choices':choices}
  if ':answer-field/correct' in v:fd[':answer-field/correct']=[':answer/id',v[':answer-field/correct'][':answer/id']]
  fields.append(fd)
 prompt=raw_text(q[':question/problem'],c)
 if c!=1:prompt=re.sub(r'!\[\]\([^)]*\)',lambda m:'![]('+render_plot(f,mathp)+')',prompt,count=1)
 return record(level,f,p,profile,prompt,raw_text(q[':question/worked-solution'],c),fields,seed,task_key(level,f,mathp,Py,Qx,S.factor(Qx-Py)),{'evidence_only':True,'source_id':sid,'raw_shape':True,'source_geometry_parameters':mathp,'derived_formal_integral':str(expected),'invalid_premise':sid=='q-126937'})
def build(level,f,p,profile,seed,calculation_only=False):
 parameters_guard(f,p);c=p['c'];d=FAMILIES[f];P=c*d[2];Q=c*d[3];Py=S.diff(P,y);Qx=S.diff(Q,x);C=S.factor(Qx-Py)
 if f=='annulus_supplied':C=c*(x*x+y*y)
 elif f=='rectangle_shift':Py=2*c*y*(x+1)
 expression=r'\oint_{\partial '+('R' if f=='annulus_sin2' else 'D')+'}('+tex(P)+r')\,\mathrm dx+('+tex(Q)+r')\,\mathrm dy'
 if f=='annulus_supplied':expression=r'\oint_{\partial D}P\,\mathrm dx+Q\,\mathrm dy';prompt='Given $'+r'\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}='+tex(C)+'$, calculate $'+expression+'$ over the positively oriented annular region shown above.';sol=OPEN+'Therefore, applying Green\'s theorem, we get\n\n'+aligned([expression+r' & =\iint_D '+tex(C)+r'\,\mathrm dA'])
 else:
  prompt='Calculate $'+expression+'$, where $D$ is the '+('annular ' if f.startswith('annulus') else '')+'region shown above.'
  sol=(QUESTIONS[d[1]][':question/worked-solution'].split('As we saw earlier' if f=='annulus_sin2' else 'We have that')[0])+'We have that $P(x,y)='+tex(P)+'$ and $Q(x,y)='+tex(Q)+'.$ '+('So,' if level=='moderate' else 'Therefore,')+'\n\n$$'+r'\frac{\partial P}{\partial y}='+tex(Py)+r',\qquad\frac{\partial Q}{\partial x}='+tex(Qx)+'.$$\n\nTherefore, applying Green\'s theorem, we get\n\n'
  formal=[]
  for name,var,field,base,derived in (('P',y,P,d[2],Py),('Q',x,Q,d[3],Qx)):
   parts=[S.diff(c*term,var) for term in S.Add.make_args(base)]
   formal.append(r'\frac{\partial '+name+r'}{\partial '+str(var)+r'}'+r' & =\frac{\partial}{\partial '+str(var)+'}'+par(field)+'='+ '+'.join(par(z) for z in parts)+'='+tex(derived))
  supplement='For $\\partial P/\\partial y$ we hold $x$ fixed, and for $\\partial Q/\\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are\n\n$$\n'+r'\begin{aligned}'+r'\\ '.join(formal)+r'.\end{aligned}'+'\n$$\n\n'
  sol=sol.replace('\n\n$$'+r'\frac{\partial P}', '\n\n'+supplement+'$$'+r'\frac{\partial P}',1)
  curlrows=[expression+r' & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA',r'\iint_D\left('+tex(Qx)+'-('+tex(Py)+r')\right)\,\mathrm dA']
  if f in ('annulus_fourth','annulus_odd','annulus_four','annulus_negative'):curlrows.append(r'\iint_D('+tex(S.expand(C))+r')\,\mathrm dA')
  curlrows.append(r'\iint_D '+tex(C)+r'\,\mathrm dA')
  if f=='annulus_sin2':curlrows=[v.replace('\\iint_D','\\iint_R') for v in curlrows]
  sol+=aligned(curlrows)
 if f.startswith('annulus'):tail,ans,rv,av,stages=polar_solution(f,p,C)
 else:tail,ans,outer,hole,stages=rect_solution(f,p,P,Q,Py,Qx,C)
 sol+='\n\n'+tail
 if f=='annulus_sin2':
  prompt="Let $\\partial R$ be the boundary of the region $R,$ shown above. Use Green's theorem to calculate the following integral:\n\n$\\oint_{\\partial R}\\mathbf F\\cdot\\mathrm d\\mathbf r="+expression+'=$'

 if calculation_only:return {'prompt':prompt,'solution':sol,'parameters':p,'template':f,'level':level,'source_id':d[1],'P':str(P),'Q':str(Q),'curl':str(C),'answer':str(ans),'stages':stages,'evidence_only':True,'reason':'normal calculation at source anchor; no bank eligibility claim'}
 if f.startswith('annulus'):
  if f in ('annulus_sin2',):values=[ans];recipes=['correct'];kind='blank';key='field-1';prompt+='\n\n{{field-1}}'
  elif f=='annulus_odd':values=[ans,2*rv,-2*rv,2*S.pi*rv,S.pi*rv];recipes=['correct','use_half_turn','add_cos_endpoints','omit_sine','use_pi_angular_measure'];kind='radio';key='selection'
  else:
   factor=(-c if f=='annulus_negative' else 4*c if f=='annulus_four' else c);n=6 if f=='annulus_fourth' else 4;a,b=p['inner'],p['outer'];values=[ans,-ans,2*S.pi*factor*b**n/n,2*S.pi*factor*(b**n+a**n)/n,2*S.pi*factor*S.Rational(b**(n-1)-a**(n-1),n-1)];recipes=['correct','reverse_curl','omit_inner','add_inner','omit_polar_jacobian'];kind='radio';key='selection'
 else:
  qonly=S.integrate(Qx,(x,p['outer'][0],p['outer'][1]),(y,p['outer'][2],p['outer'][3]))-S.integrate(Qx,(x,p['hole'][0],p['hole'][1]),(y,p['hole'][2],p['hole'][3]));values=[ans,outer+hole,outer,hole-outer,qonly];recipes=['correct','add_hole','omit_hole','reverse_outer_minus_hole','omit_P_partial'];kind='radio';key='selection'
 values=[S.simplify(z) for z in values]
 if any(S.simplify(a-b)==0 for i,a in enumerate(values) for b in values[i+1:]):raise ValueError('whole operation bank collision')
 fields=[{':answer-field/id':'field',':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':[{':answer/id':str(i),':answer/type':':answer.type/math',':answer/value':tex(z)} for i,z in enumerate(values)],':answer-field/correct':[':answer/id','0']}]
 plot=render_plot(f,p);prompt='![]('+plot+')\n\n'+prompt
 # Complete task excludes same-role hole ordering (one hole here) and unary field
 # terms with zero held partials; actual polynomial/geometry are still presentation.
 keymath=task_key(level,f,p,Py,Qx,C)
 return record(level,f,p,profile,prompt,sol,fields,seed,keymath,{'evidence_only':False,'source_id':d[1],'authored_level':level=='easy','bank_origin':'authored operations','recipes':recipes,'stages':stages,'curl':str(C),'P':str(P),'Q':str(Q),'answer':str(ans),'plot':plot})
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 rng=random.Random(seed)
 if profile and profile.startswith('raw:'):
  sid=profile[4:];f=BY_SOURCE[sid]
  if template and template!=f:raise ValueError('profile/template mismatch')
  if FAMILIES[f][0]!=level:raise ValueError('raw difficulty mismatch')
  return raw_generate(level,f,parameters or {'amplitude':1},profile,seed)
 names=[f for f,d in FAMILIES.items() if d[0]==level and (field_type is None or field_type==('blank' if f=='annulus_sin2' else 'radio'))]
 if template and template not in names:raise ValueError('unsupported template/level/field type')
 f=template or rng.choice(names);eligible='angular' if f=='annulus_odd' else 'blank' if f=='annulus_sin2' else 'radial' if f.startswith('annulus') else 'outer_minus_hole'
 if profile not in (None,eligible):raise ValueError('unsupported complete operation profile')
 if parameters is not None:return build(level,f,parameters,eligible,seed)
 for _ in range(300):
  p=sample(f,rng)
  try:return build(level,f,p,eligible,seed)
  except ValueError as e:
   if str(e)!='whole operation bank collision':raise
 raise ValueError('no eligible instance in declared domain')
# Easy: authored supplied-curl evaluation within the existing polar prerequisite.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: all six observed partial/factorization/angular families.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: all five observed outer-minus-hole families with separate endpoints.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=['json','markdown'],default='markdown');a=ap.parse_args();items=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 if a.format=='json':print(json.dumps(items,indent=2))
 else:
  for q in items:
   print(q['question'][':question/problem']);print('\n'+q['question'][':question/worked-solution']);print('\nChoices:',[v[':answer/value'] for v in q['question'][':question/answer-fields'][0][':answer-field/choices']])

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186133900-source-policy.json'))

if __name__=='__main__':main()
