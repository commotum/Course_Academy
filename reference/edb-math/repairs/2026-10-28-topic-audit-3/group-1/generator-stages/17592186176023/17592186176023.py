#!/usr/bin/env python3
"""Evaluate Green's-theorem line integrals in polar coordinates (basis1356).

Shared exact recipes, followed by individually bounded easy/moderate/hard APIs.
All10 original banks replay through public observed:<source> profiles; opaque
historical scalar banks are evidence-only. Their noise parameter changes a
univariate component whose cross partial vanishes, so the assessed integral is
computed from its curl, never retrieved from a source answer. Normal generation
uses source-shaped families with authored complete method-derived banks.
Raw profiles preserve absent difficulty/solution/correct attributes and source
bytes. They are not learning-eligible, including ambiguous q-126758 evidence.
Normal source-family solutions retain formal theorem, components, cross partials,
curl substitution/reduction, region, Jacobian, trig reduction, radial primitive,
radial evaluation, angular primitive and endpoint arithmetic, with documented
source repairs and explicit endpoint-detail additions. No DB writes.
"""
from __future__ import annotations
from audit_presentation import prose as _ca_prose, problem as _ca_problem, values as _ca_values, question as _ca_question, identity_material as _ca_material, asset_output as _ca_asset_output
import argparse, hashlib, json, os, random, re, sys, tempfile, uuid
from pathlib import Path
import sympy as sp
os.environ.setdefault('MPLCONFIGDIR','/tmp/green-polar-17592186176023-mpl-cache')
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
BASE=Path(__file__).with_suffix('')
SOURCE=json.loads((BASE/'source.json').read_text())
KP=SOURCE['record']; KP_ID=17592186176023
VERSION='green-polar-evaluation-v3-format-audit-9837-v1'
X,Y,R,T=sp.symbols('x y r theta',real=True)
Q={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
# Observed family anchors: c is the common derivative magnitude; s is R^2.
FAMILIES={
 'q-109119':dict(level='moderate',kind='negative',c=1,s=4,inner=0,lo=0,hi=2,noise=r'\operatorname{cos}⁡x'),
 'q-126733':dict(level='moderate',kind='cross',c=1,s=25,inner=0,lo=0,hi=2,noise='2-{x}^{2}y'),
 'q-126736':dict(level='moderate',kind='cross',c=2,s=1,inner=0,lo=0,hi=2,noise=r'\operatorname{sin}⁡x'),
 'q-126755':dict(level='moderate',kind='cubic',c=3,s=2,inner=0,lo=0,hi=2,noise='{4}^{x}'),
 'q-126759':dict(level='moderate',kind='quotient',c=1,s=4,inner=0,lo=0,hi=2,noise=r'\sqrt{x+5}'),
 'q-126753':dict(level='moderate',kind='cubic',c=3,s=9,inner=0,lo=0,hi=2,noise='{sin}^{3}⁡x'),
 'q-126747':dict(level='hard',kind='anisotropic',c=1,s=16,inner=0,lo=0,hi='1/3',noise='{3}^{x}'),
 'q-126756':dict(level='hard',kind='sector',c=2,s=9,inner=0,lo='1/2',hi=1,noise='{e}^{x}'),
 'q-126758':dict(level='hard',kind='annular',c=3,s=16,inner=2,lo=0,hi='1/2',noise=r'\sqrt{5+x}'),
 'q-125717':dict(level='hard',kind='sector',c=4,s=4,inner=0,lo=0,hi='1/2',noise=r'\sqrt{x}'),
 'supported_disk':dict(level='easy',kind='cross',c=1,s=4,inner=0,lo=0,hi=2),
}
# Whole historical banks: coefficients in units of pi, except q126747 entries.
# These are evidence expression patterns, NOT recovered error intentions.
HISTORICAL={
 'q-109119':['16*pi','-20*pi','13*pi/2','-8*pi','-9*pi/2'],
 'q-125717':['-4*pi','2*pi','-pi/2','8*pi','4*pi'],
 'q-126733':['5*pi/4','125*pi/2','25*pi/4','625*pi','625*pi/2'],
 'q-126736':['3*pi/2','2*pi','pi/4','pi/2','pi'],
 'q-126747':['-8*pi/3','-16*sqrt(3)','8*sqrt(3)','8*pi','sqrt(3)/2'],
 'q-126755':['pi/3','3*pi','6*pi','3*pi/2','pi/6'],
 'q-126756':['9*pi/4','81*pi/4','27*pi/4','3*pi/2','27*pi/2'],
 'q-126758':['90*pi','15*pi','90*pi/4','45*pi/2','45*pi'],
 'q-126759':['16*pi','8*pi','2*pi','4*pi','0'],
 'q-126753':['3*pi/2','729*pi/2','81*pi/2','243*pi/2','27*pi/2'],
}

def tex(v):return sp.latex(sp.sympify(v)).replace(r'\log',r'\ln')
def coeff(c,v):
 c=sp.sympify(c)
 return ('-' if c==-1 else '' if c==1 else tex(c))+v

def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+json.dumps(_ca_material(v),sort_keys=True,ensure_ascii=False)))
def digest(v):return hashlib.sha256(json.dumps(_ca_material(v),sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def anchor(name):return {k:str(v)for k,v in FAMILIES[name].items() if k in ['c','s','inner','lo','hi']}
def exact(p):return {k:sp.sympify(v) for k,v in p.items()}
def answer_value(f,p):
 c,s,a,l,h=[p[k]for k in ['c','s','inner','lo','hi']]; rad=(s*s-a**4)/4
 if f['kind']=='anisotropic':return sp.simplify(-c*rad*(sp.sin(2*sp.pi*h)-sp.sin(2*sp.pi*l))/2)
 return sp.simplify((-1 if f['kind']=='negative' else 1)*c*rad*sp.pi*(h-l))

def components(name,p):
 c=p['c']; n=1
 if name=='q-109119':return X**2*Y*c-sp.cos(X),4-c*X*Y**2,coeff(c,'x^2y')+r'-\cos x','4-'+coeff(c,'xy^2')
 if name=='q-126733':return 2-c*X**2*Y,1+c*X*Y**2,'2-'+coeff(c,'x^2y'),'1+'+coeff(c,'xy^2')
 if name=='q-126736':return sp.sin(X)-c*X**2*Y,sp.sqrt(Y+3)+c*X*Y**2,r'\sin x-'+coeff(c,'x^2y'),r'\sqrt{y+3}+'+coeff(c,'xy^2')
 if name=='q-126755':return 4**X-c*Y**3/3+2,2/(Y**2+1)+c*X**3/3,'4^x-'+coeff(c/3,'y^3')+'+2',r'\frac{2}{y^2+1}+'+coeff(c/3,'x^3')
 if name=='q-126759':return (sp.sqrt(X+5)-c*Y**3)/3,(sp.sqrt(Y+5)+c*X**3)/3,r'\frac{\sqrt{x+5}-'+coeff(c,'y^3')+'}{3}',r'\frac{\sqrt{y+5}+'+coeff(c,'x^3')+'}{3}'
 if name=='q-126753':return sp.sin(X)**3-c*Y**3/3,Y**4+c*X**3/3,r'\sin^3 x-'+coeff(c/3,'y^3'),'y^4+'+coeff(c/3,'x^3')
 if name=='q-126747':return 3**X+c*X**2*Y,2**Y+c*X*Y**2,'3^x+'+coeff(c,'x^2y'),'2^y+'+coeff(c,'xy^2')
 if name=='q-126756':return sp.exp(X)-c*X**2*Y,sp.exp(Y)+c*X*Y**2,'e^x-'+coeff(c,'x^2y'),'e^y+'+coeff(c,'xy^2')
 if name=='q-126758':return sp.sqrt(5+X)-c*X**2*Y,sp.exp(-Y**2)+c*X*Y**2,r'\sqrt{5+x}-'+coeff(c,'x^2y'),r'e^{-y^2}+'+coeff(c,'xy^2')
 if name=='q-125717':return sp.sqrt(X+1)-c*X**2*Y,sp.exp(Y)+c*X*Y**2,r'\sqrt{x+1}-'+coeff(c,'x^2y'),'e^y+'+coeff(c,'xy^2')
 return sp.exp(-X**2)-c*X**2*Y,Y+c*X*Y**2,r'e^{-x^2}-'+coeff(c,'x^2y'),'y+'+coeff(c,'xy^2')

def check_scope(level,name,p):
 if set(p)!={'c','s','inner','lo','hi'}:raise ValueError('exactly c,s,inner,lo,hi required')
 c,s,a,l,h=[p[k]for k in ['c','s','inner','lo','hi']]
 if not(c.is_integer and 1<=c<=6 and s.is_integer and 1<=s<=25 and a.is_integer and 0<=a<sp.sqrt(s) and l<h and 0<=l<h<=2):raise ValueError('parameter domain')
 if level=='easy' and not(c<=4 and s in [1,4,9,16,25] and a==0 and l==0 and h==2):raise ValueError('easy workload')
 if level=='moderate' and not(s in [1,2,4,9,16,25] and a==0 and l==0 and h==2):raise ValueError('moderate full disk')
 if name=='q-126736' and s>=9:raise ValueError('sqrt(y+3) C1 neighborhood requires radius<3')
 if name=='q-126759' and s>=25:raise ValueError('sqrt(x+5),sqrt(y+5) require radius<5')
 if level=='hard':
  if s not in [4,9,16,25]:raise ValueError('hard integral outer radii2..5')
  kind=FAMILIES[name]['kind']
  if kind=='anisotropic' and not(a==0 and l==0 and h in [sp.Rational(1,6),sp.Rational(1,3),sp.Rational(2,3)]):raise ValueError('anisotropic familiar angles')
  if kind=='sector' and not(a==0 and (l,h) in [(0,sp.Rational(1,2)),(sp.Rational(1,2),1),(0,1)]):raise ValueError('sector scope')
  if name=='q-125717' and not(l==0 and h in [sp.Rational(1,2),1] and (h==sp.Rational(1,2))):raise ValueError('sqrt(x+1) positive quadrant')
  if kind=='annular' and not(1<=a<=4 and s in [4,9,16,25] and l==0 and h==sp.Rational(1,2)):raise ValueError('quarter annulus bounds')

def sample(level,name,rng):
 p=anchor(name); p['c']=rng.randint(1,4 if level=='easy' else 6)
 if level=='easy':p['s']=rng.choice([1,4,9,16,25])
 elif level=='moderate':p['s']=rng.choice([1,2,4,9,16,25] if name not in ['q-126736','q-126759'] else [1,2,4] if name=='q-126736' else [1,2,4,9,16])
 else:
  p['s']=rng.choice([4,9,16,25])
  if name=='q-126747':p['hi']=rng.choice(['1/6','1/3','2/3'])
  elif name=='q-126756':p['lo'],p['hi']=rng.choice([(0,'1/2'),('1/2',1),(0,1)])
  elif name=='q-126758':p['inner']=rng.choice(list(range(1,int(sp.sqrt(p['s'])))))
 return exact(p)

_PLOT_LOCK=None

def render_plots(p,shaded):
 """Exact instance geometry; unique temporary file and atomic PNG+sidecar."""
 import threading
 global _PLOT_LOCK
 if _PLOT_LOCK is None:_PLOT_LOCK=threading.RLock()
 data={k:str(p[k])for k in ['s','inner','lo','hi']};data['shaded']=shaded;data['renderer_revision']=3
 key=digest(data); d=_ca_asset_output(BASE/'plots'/'plot').parent;d.mkdir(exist_ok=True); dst=d/(key+'.png'); side=dst.with_suffix('.json')
 with _PLOT_LOCK:
  if dst.exists() and side.exists():return str(dst.resolve())
  ro=float(sp.sqrt(p['s']));ri=float(p['inner']);a=float(sp.pi*p['lo']);b=float(sp.pi*p['hi']);ts=np.linspace(a,b,300)
  fig,ax=plt.subplots(figsize=(4.5,4.5),dpi=140);ax.set_aspect('equal');lim=ro*1.3;ax.set_xlim(-lim,lim);ax.set_ylim(-lim,lim);ax.axis('off')
  for end in [(lim,0),(0,lim)]:ax.annotate('',xy=end,xytext=(-lim,0)if end[1]==0 else(0,-lim),arrowprops=dict(arrowstyle='->',color='#333333',lw=1))
  ax.text(lim*.95,-ro*.09,'x');ax.text(ro*.06,lim*.93,'y')
  xs=ro*np.cos(ts);ys=ro*np.sin(ts)
  if shaded:
   ix=ri*np.cos(ts[::-1]);iy=ri*np.sin(ts[::-1]);ax.fill(np.r_[xs,ix],np.r_[ys,iy],color='#d3e9f9',zorder=0)
  paths=[np.column_stack([xs,ys])]
  if b-a<2*np.pi-1e-8:
   paths +=[np.column_stack([np.linspace(ro,ri,50)*np.cos(b),np.linspace(ro,ri,50)*np.sin(b)])]
  if ri:paths +=[np.column_stack([ri*np.cos(ts[::-1]),ri*np.sin(ts[::-1])])]
  if b-a<2*np.pi-1e-8:paths +=[np.column_stack([np.linspace(ri,ro,50)*np.cos(a),np.linspace(ri,ro,50)*np.sin(a)])]
  for path in paths:
   ax.plot(path[:,0],path[:,1],color='#eda900',lw=1.8)
   for fraction in ([.25,.68]if len(path)>100 else [.55]):
    i=int((len(path)-6)*fraction);ax.annotate('',xy=path[i+5],xytext=path[i],arrowprops=dict(arrowstyle='->',color='#222222',lw=1,mutation_scale=10))
  # Cardinal radius labels only where assessed boundary meets that axis.
  for t0 in [0,np.pi/2,np.pi,3*np.pi/2]:
   if a-1e-8<=t0<=b+1e-8:
    x,y=ro*np.cos(t0),ro*np.sin(t0);lab=tex(sp.sqrt(p['s']))
    if abs(y)<1e-7:ax.text(x, y-ro*.13,'$'+('-'if x<0 else '')+lab+'$',ha='center')
    else:ax.text(x-ro*.09,y,'$'+('-'if y<0 else '')+lab+'$',ha='right',va='center')
  if ri:ax.text(ri,-ro*.13,'$'+tex(p['inner'])+'$',ha='center');ax.text(-ro*.08,ri,'$'+tex(p['inner'])+'$',ha='right')
  if b-a<2*np.pi and b not in [np.pi/2,np.pi,3*np.pi/2]:
   tt=np.linspace(a,b,50);rr=ro*.28;ax.plot(rr*np.cos(tt),rr*np.sin(tt),'--',color='#999999',lw=1);mid=(a+b)/2;ax.text(ro*.36*np.cos(mid),ro*.36*np.sin(mid),'$'+tex(sp.pi*(p['hi']-p['lo']))+'$',fontsize=10)
  if shaded:
   mid=np.pi/4 if b-a>2*np.pi-1e-8 else (a+b)/2;mr=(ri+ro)/2;ax.text(mr*np.cos(mid),mr*np.sin(mid),'D',color='#6795b2',ha='center',va='center')
   cm=a+(b-a)*.3;ax.text(ro*1.06*np.cos(cm),ro*1.06*np.sin(cm),'C',color='#d89700')
  fd,tmp=tempfile.mkstemp(dir=d,suffix='.png');os.close(fd)
  try:fig.savefig(tmp,bbox_inches='tight',facecolor='white');os.replace(tmp,dst)
  finally:plt.close(fig);Path(tmp).unlink(missing_ok=True)
  fd,tmp=tempfile.mkstemp(dir=d,suffix='.json');os.close(fd);Path(tmp).write_text(json.dumps(dict(data,python=sys.version.split()[0],matplotlib=matplotlib.__version__),indent=2));os.replace(tmp,side)
 return str(dst.resolve())

def bank(f,p,answer):
 c,s,a,l,h=[p[k]for k in ['c','s','inner','lo','hi']];w=sp.pi*(h-l);rad=(s*s-a**4)/4
 if f['kind']=='anisotropic':
  angular=-(sp.sin(2*sp.pi*h)-sp.sin(2*sp.pi*l))/2
  vals=[answer,-answer,2*answer,c*(s**sp.Rational(3,2)-a**3)/3*angular,c*rad*w]
  ops=['correct','reverse_curl','omit_angular_chain_half','omit_polar_jacobian','use_squares_sum_identity']
 else:
  sign=-1 if f['kind']=='negative' else 1
  vals=[answer,-answer,sign*c*(s**sp.Rational(3,2)-a**3)*w/3,sign*c*(s*s-a**4)*w,answer/2]
  ops=['correct','reverse_curl','omit_polar_jacobian','omit_radial_primitive_denominator','omit_one_cross_partial']
 vals=list(map(sp.simplify,vals))
 if any(sp.simplify(x-y)==0 for i,x in enumerate(vals)for y in vals[i+1:]):raise ValueError('whole bank collision')
 return vals,ops

GREEN=r'\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.'
CHANGE=r'\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.'
def display(s):return '\n\n$$\n'+s+'\n$$\n\n'
def aligned(rows):return r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'
def integral(c):return r'\oint_C('+c[2]+r')\,dx+('+c[3]+r')\,dy'

def solution(name,p,plot):
 f=FAMILIES[name];P,Qv,pt,qt=components(name,p);pp=sp.diff(P,Y);qq=sp.diff(Qv,X);curl=sp.expand(qq-pp);c=p['c'];s=p['s'];a=p['inner'];lo=sp.pi*p['lo'];hi=sp.pi*p['hi'];ro=sp.sqrt(s);an=answer_value(f,p);rad=(s*s-a**4)/4
 C=integral((P,Qv,pt,qt));out=''
 if f['level']=='moderate':out="First, notice that we can rewrite our integral as"+display(r'\oint_C F\cdot dr='+C+'.')
 out+="Green's theorem states that"+display(GREEN)+"In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:\n\n![]("+plot+")\n\nNow, since"+display('P(x,y)='+pt+r',\quad Q(x,y)='+qt+',')+'we have that'+display(aligned([r'\frac{\partial P}{\partial y}='+tex(pp)+r',\quad \frac{\partial Q}{\partial x}='+tex(qq)+'.']))
 rows=[C+r'&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA',r'&=\iint_D\left('+tex(qq)+'-('+tex(pp)+r')\right)\,dA']
 if f['kind']!='anisotropic':rows.append(r'&=\iint_D '+coeff(-c if f['kind']=='negative' else c,r'(x^2+y^2)')+r'\,dA.')
 out+='Applying Green\'s theorem, we get'+display(aligned(rows))+'Now, notice that the region $D$ can be represented in polar coordinates as'+display(r'\Delta=\{(r,\theta):'+tex(a)+r'\le r\le '+tex(ro)+','+tex(lo)+r'\le\theta\le '+tex(hi)+r'\}.')+'The change of variables formula for plane polar coordinates states that'+display(CHANGE)+'Finally, we can calculate our double integral, as follows:'
 I=lambda expr:r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}'+expr+r'\,d\theta'
 J=lambda expr:r'\int_{'+tex(a)+'}^{'+tex(ro)+'}'+expr+r'\,dr'
 if f['kind']=='anisotropic':
  rows=[r'\iint_D '+tex(curl)+r'\,dA&=\iint_\Delta '+coeff(c,r'(r^2\sin^2\theta-r^2\cos^2\theta)')+r'\,r\,dr\,d\theta',r'&='+I(J(coeff(-c,r'r^3(\cos^2\theta-\sin^2\theta)'))),r'&=-'+coeff(c,I(r'\cos(2\theta)'+J('r^3'))),r'&=-'+coeff(c,I(r'\cos(2\theta)\left[\frac{r^4}{4}\right]_{'+tex(a)+'}^{'+tex(ro)+'}')),r'&=-'+coeff(c*rad,I(r'\cos(2\theta)')),r'&=-'+coeff(c*rad,r'\left[\frac{\sin(2\theta)}{2}\right]_{'+tex(lo)+'}^{'+tex(hi)+'}'),r'&=-'+tex(c*rad/2)+r'\left(\sin('+tex(2*hi)+r')-\sin('+tex(2*lo)+r')\right)',r'&='+tex(an)+'.']
 else:
  sg=-1 if f['kind']=='negative' else 1;outer=sg*c
  inside=name=='q-126756'; primitive=coeff(c,'r^4')+r'/4' if inside else r'\frac{r^4}{4}'
  # preserve the source's inside/outside coefficient convention per family.
  O=lambda expr:expr if inside else coeff(outer,expr)
  integrand=coeff(c,'r^3')if inside else 'r^3'
  trig=r'\sin^2\theta+\cos^2\theta' if name=='q-126756'else r'\cos^2\theta+\sin^2\theta'
  rows=[r'\iint_D '+coeff(outer,r'(x^2+y^2)')+r'\,dA&=\iint_\Delta '+coeff(outer,'(r^2('+trig+'))')+r'\,r\,dr\,d\theta',r'&='+O(I(J(integrand+'('+trig+')'))),r'&='+O(I(J(integrand))),r'&='+O(I(r'\left['+primitive+r'\right]_{'+tex(a)+'}^{'+tex(ro)+'}'))]
  # Explicit addition: evaluated signed endpoint components before collection.
  rows +=[r'&='+O(I(r'\left('+tex((c if inside else 1)*s*s/4)+'-'+tex((c if inside else 1)*a**4/4)+r'\right)'))]
  radial_value=(c if inside else 1)*rad
  evaluated_radial='' if name=='q-126755' and radial_value==1 else tex(radial_value)
  rows.append(r'&='+O(I(evaluated_radial)))
  rows.append(r'&='+coeff(outer*rad,r'[\theta]_{'+tex(lo)+'}^{'+tex(hi)+'}'))
  if name!='q-126736':rows.append(r'&='+tex(outer*rad)+r'\left('+tex(hi)+'-'+tex(lo)+r'\right)')
  rows.append(r'&='+tex(an)+'.')
 out+=display(aligned(rows));return out

def raw_replay(name,noise,seed):
 """Source-byte masks for independent univariate nuisance scaling.

 Mask components are complete expressions, including their mathematical input;
 no substring number substitutions or literal-source-return branch.
 """
 f=FAMILIES[name];q=Q[name];component=f['noise'];n=sp.sympify(noise)
 if not(n.is_integer and 1<=n<=6):raise ValueError('noise integer1..6')
 # Complete component masks protect powers and numerical exponential bases.
 if name=='q-126733':replacement=str(n+1)+'-{x}^{2}y'
 else:replacement=component if n==1 else tex(n)+r'\cdot('+component+')'
 prompt=q[':question/problem'].replace(component,'@@NOISE@@').replace('@@NOISE@@',replacement)
 sol=q.get(':question/worked-solution')
 if sol is not None:sol=sol.replace(component,'@@NOISE@@').replace('@@NOISE@@',replacement)
 vals=[sp.sympify(v)for v in HISTORICAL[name]];ans=answer_value(f,exact(anchor(name)))
 return assemble(f['level'],name,{'noise':str(n)},'observed:'+name,prompt,sol,[a[':answer/value']for a in q[':question/answer-fields'][0][':answer-field/choices']],vals,ans,seed,raw=q)

def assemble(level,name,p,profile,prompt,sol,strings,vals,answer,seed,raw=None,ops=None):
 if raw is None:prompt=_ca_problem(prompt);sol=_ca_prose(sol);strings=_ca_values(strings)
 content={'difficulty': None if raw is not None and ':question/difficulty'not in raw else level,'prompt':prompt,'solution':sol,'bank':sorted(strings)}
 key=uid(content);fid=uid([key,'selection']);choices=[{':answer/id':uid([fid,v]),':answer/type':':answer.type/math',':answer/value':v}for v in strings]
 # Use positional identities for legacy equal-spelling raw options, without treating
 # equivalent displayed values as mathematical validity.
 if len({a[':answer/id']for a in choices})<len(choices):raise ValueError('duplicate answer spelling')
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
 original_has_correct=raw is None or ':answer-field/correct'in raw[':question/answer-fields'][0]
 if original_has_correct:
  matches=[i for i,v in enumerate(vals)if sp.simplify(v-answer)==0]
  if len(matches)!=1:raise ValueError('correct option ambiguity')
  field[':answer-field/correct']=[':answer/id',choices[matches[0]][':answer/id']]
 random.Random(seed).shuffle(choices)
 q={':question/id':key,':question/problem':prompt,':question/answer-fields':[field]}
 if raw is None or ':question/difficulty'in raw:q[':question/difficulty']=':question.difficulty/'+level
 if sol is not None:q[':question/worked-solution']=sol
 mathpar=anchor(name) if raw is not None else p
 MP,MQ,_,_=components(name,exact(mathpar))
 fingerprint=digest({'assessed_components':[str(sp.expand(MP-MP.subs(Y,0))),str(sp.expand(MQ-MQ.subs(X,0)))],'assessed_information':'provided-polar-bounds'if level=='easy'else'circle-equation'if level=='moderate'else'boundary-plot','curl':tex(sp.expand(sp.diff(components(name,exact(mathpar))[1],X)-sp.diff(components(name,exact(mathpar))[0],Y))),'polar_bounds':{k:mathpar[k]for k in ['s','inner','lo','hi']}})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':name,'profile':profile,'seed':seed,'parameters':p,'source':{k:SOURCE[k]for k in ['database','basis','lineage']},'evidence_only':raw is not None,'eligible_for_learning':raw is None,'mathematical_fingerprint':fingerprint,'answer':str(answer),'bank_values':[str(v)for v in vals],'bank_recipes':ops or ['opaque-historical-pattern']*len(vals),'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ['easy','moderate','hard']:raise ValueError('unknown difficulty')
 if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('only observed radio shape')
 rng=random.Random(seed)
 if profile and profile.startswith('observed:'):
  name=profile.split(':',1)[1]
  if template not in [None,name] or name not in Q:raise ValueError('source profile mismatch')
  if level!=FAMILIES[name]['level']:raise ValueError('source level mismatch; unrated assigned hard for API routing only')
  if parameters is not None and set(parameters)!={'noise'}:raise ValueError('raw evidence accepts noise only; anchor geometry fixed')
  return raw_replay(name,(parameters or {}).get('noise',rng.randint(1,6)),seed)
 if profile not in [None,'authored-method']:raise ValueError('unknown bank profile')
 names=[n for n,f in FAMILIES.items()if f['level']==level]
 if template is not None and template not in names:raise ValueError('template/level mismatch')
 name=template or rng.choice(names)
 for _ in range(200):
  p=exact(parameters)if parameters is not None else sample(level,name,rng);check_scope(level,name,p);f=FAMILIES[name];ans=answer_value(f,p)
  try:vals,ops=bank(f,p,ans)
  except ValueError:
   if parameters is not None:raise
   continue
  P,Qv,pt,qt=components(name,p);C=integral((P,Qv,pt,qt));plot=render_plots(p,True)
  if level=='moderate':prompt="Use Green's theorem to evaluate $\\oint_C F\\cdot dr,$ where $F(x,y)=\\langle "+pt+','+qt+r'\rangle$ and $C$ is the circle $x^2+y^2='+tex(p['s'])+',$ oriented counterclockwise.'
  elif level=='hard':prompt='![]('+render_plots(p,False)+')\n\nEvaluate $'+C+',$ where the path $C$ is shown above.'
  else:prompt='Use Green\'s theorem to evaluate $'+C+',$ where $C$ is the counterclockwise boundary of the disk with polar description $0\\le r\\le '+tex(sp.sqrt(p['s']))+r',\ 0\le\theta\le2\pi$.'
  return assemble(level,name,{k:str(v)for k,v in p.items()},'authored-method',prompt,solution(name,p,plot),[tex(v)for v in vals],vals,ans,seed,ops=ops)
 raise RuntimeError('no eligible complete bank')

# EASY: authored supplied polar disk bounds remove the bound-reconstruction step;
# same tutorial quadratic curl, c1..4, integral-radius1..5, no harder algebra.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: observed six vector-field circle families, one radial fourth-power
# primitive; rational cubic coefficients retain the same formal differentiation.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: observed sector, quarter annulus and familiar double-angle families;
# geometry read from plot, no arbitrary sectors or new integration technique.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question'];parts=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  parts +=['- $'+a[':answer/value']+'$' for a in f[':answer-field/choices']]
 if ':question/worked-solution'in q:parts+=['\nWorked solution\n',q[':question/worked-solution']]
 return '\n\n'.join(parts)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=['easy','moderate','hard']if args.difficulty=='all'else[args.difficulty];records=[generate(l,args.seed+i,template=args.template,profile=args.profile)for l in levels for i in range(args.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2)if args.format=='json'else'\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
