#!/usr/bin/env python3
"""Cylindrical evaluation, frozen math basis1356; local review only.

Raw profiles are parameterized scalar-integrand evidence masks, not default banks.
Their opaque source scalars scale with the integrand and do not imply recovered
error intent. Normal families retain each source operative chain and use complete
method-derived banks. See private classification/extraction/validation evidence.
Easy is an authored constant-height radial specialization of the canonical method;
moderate and hard retain the captured labels even when their workload overlaps.
No database API or writes. Matplotlib projection assets use atomic cache writes.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, math, os, random, re, sys, tempfile, uuid
from functools import lru_cache
from pathlib import Path
import sympy as sp

KP_ID=17592186129278
ROOT=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
KP=SOURCE['record']
VERSION='cylindrical-evaluate-2'
r=sp.Symbol('r',positive=True); t=sp.Symbol('theta',real=True); z=sp.Symbol('z',real=True)
x,y=sp.symbols('x y',real=True)
SOURCES={q[':db/id']:q for q in KP[':knowledge-point/questions']}
SPECS={
 'radial_tilt':('moderate',17592186129518,{'n':4,'h':12,'b':4,'c':1}),
 'cross_z':('hard',17592186129767,{'n':9,'h':2,'b':1,'c':2}),
 'half_xradial':('hard',17592186367687,{'n':3,'h':4,'b':1,'c':1}),
 'reciprocal':('moderate',17592186367694,{'n':9,'h':9,'b':1,'c':1}),
 'cone':('moderate',17592186367701,{'n':1,'h':1,'b':1,'c':1}),
 'half_xz':('hard',17592186367708,{'n':1,'h':2,'b':1,'c':2}),
 'half_constant':('hard',17592186367715,{'n':2,'h':6,'b':2,'c':4}),
 'quarter_x':('hard',17592186411857,{'n':4,'h':3,'b':1,'c':4}),
 'half_linear':('hard',17592186427903,{'n':3,'h':9,'b':1,'c':1}),
 'power_tilt':('moderate',17592186427904,{'n':1,'h':4,'b':1,'c':1}),
 'easy_radial':('easy',None,{'n':4,'h':3,'b':0,'c':1}),
}
TEMPLATES={k:{'level':v[0],'source_id':v[1],'plot':'light'} for k,v in SPECS.items()}


def tex(e):
    """Small unambiguous exact-expression printer, deliberately no eager trig CAS."""
    e=sp.sympify(e)
    if e==sp.pi:return r'\pi'
    if e==t:return r'\theta'
    if e.is_Symbol:return str(e)
    if e.is_Integer:return str(e)
    if e.is_Rational:
        sign='-' if e<0 else '';return sign+r'\frac{'+str(abs(e.p))+'}{'+str(e.q)+'}'
    if e.func in (sp.sin,sp.cos):return ('\\sin' if e.func==sp.sin else '\\cos')+'('+tex(e.args[0])+')'
    if e.is_Add:
        terms=e.as_ordered_terms();out=tex(terms[0])
        for v in terms[1:]:out+=('-'+tex(-v)) if v.could_extract_minus_sign() else '+'+tex(v)
        return out
    if e.is_Mul:
        sign='-' if e.could_extract_minus_sign() else '';e=-e if sign else e
        if not e.is_Mul:return sign+tex(e)
        return sign+r'\cdot '.join('('+tex(a)+')' if a.is_Add else tex(a) for a in e.args)
    if e.is_Pow:
        a,b=e.args
        if b==sp.Rational(1,2):return r'\sqrt{'+tex(a)+'}'
        return '('+tex(a)+')^{'+tex(b)+'}'
    raise ValueError(e)


def parse_tex(s):
    """Independent displayed-expression reader; never reads generation metadata."""
    from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
    s=s.strip().replace('π',r'\pi').replace('⁡','').replace(r'\left','').replace(r'\right','')
    def group(text,i):
        if text[i]!='{':raise ValueError(('expected brace',text[i:]))
        depth=1;j=i+1
        while depth:
            if j>=len(text):raise ValueError('unbalanced brace')
            depth+=(text[j]=='{')-(text[j]=='}');j+=1
        return text[i+1:j-1],j
    def expand(text):
        out='';i=0
        while i<len(text):
            if text.startswith(r'\frac',i):
                a,j=group(text,i+5);b,j=group(text,j);out+='(('+expand(a)+')/('+expand(b)+'))';i=j
            elif text.startswith(r'\sqrt',i):
                a,j=group(text,i+5);out+='sqrt('+expand(a)+')';i=j
            elif text[i]=='{':
                a,j=group(text,i);out+='('+expand(a)+')';i=j
            else:out+=text[i];i+=1
        return out
    s=expand(s).replace(r'\theta','theta').replace(r'\pi','pi').replace(r'\cdot','*').replace(r'\sin','sin').replace(r'\cos','cos').replace('^','**')
    return parse_expr(s,local_dict={'r':r,'theta':t,'z':z,'x':x,'y':y,'pi':sp.pi,'sin':sp.sin,'cos':sp.cos,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))


def model(f,p):
    n,h,b,c=map(sp.sympify,[p[k] for k in ('n','h','b','c')]);R=sp.sqrt(n)
    a,d=0,2*sp.pi;low=sp.Integer(0);high=h-b*r*sp.cos(t);F=c*r**3;cart=c*(x*x+y*y)
    if f in ('radial_tilt','easy_radial'):F=c*r**2;cart=c*sp.sqrt(x*x+y*y);high=h-b*r*sp.sin(t)
    elif f=='reciprocal':F=c*z;cart=c*z/sp.sqrt(x*x+y*y);high=sp.sqrt(h-b*r*r*sp.cos(2*t))
    elif f=='cone':low=b*r;high=h;F=c*r**3;cart=c*(x*x+y*y)
    elif f=='half_xradial':a,d=-sp.pi/2,sp.pi/2;low=b*r*sp.sin(t);high=low+h;F=c*r**3*sp.cos(t);cart=c*x*sp.sqrt(x*x+y*y)
    elif f in ('half_xz','cross_z'):a,d=0,sp.pi;low=-b*r*sp.cos(t);high=b*r*sp.cos(t)+h;F=c*z*r**(2 if f=='half_xz' else 1)*(sp.cos(t) if f=='half_xz' else 1);cart=c*x*z if f=='half_xz' else c*z
    elif f=='half_constant':a,d=0,sp.pi;F=c*r;cart=c
    elif f=='quarter_x':a,d=0,sp.pi/2;high=b*r*sp.sin(t)+h;F=c*r*r*sp.cos(t);cart=c*x
    elif f=='half_linear':a,d=-sp.pi/2,sp.pi/2;low=b*r*sp.cos(t);high=low+h;F=c*r*r*(sp.cos(t)-sp.sin(t));cart=c*(x-y)
    return {'R':R,'a':sp.sympify(a),'d':sp.sympify(d),'low':low,'high':high,'F':F,'cart':cart}


@lru_cache(maxsize=5000)
def stages(f,n,h,b,c):
    p=dict(n=n,h=h,b=b,c=c);m=model(f,p)
    zp=sp.integrate(m['F'],z);ze=sp.expand(zp.subs(z,m['high'])-zp.subs(z,m['low']))
    rp=sp.integrate(ze,r);reduced=sp.expand(rp.subs(r,m['R'])-rp.subs(r,0))
    te=sp.expand_trig(reduced)
    if f=='half_xz':te=sp.expand(reduced.subs(sp.cos(t)**2,(1+sp.cos(2*t))/2))
    if f=='quarter_x':te=sp.expand(reduced.subs(sp.sin(t)*sp.cos(t),sp.sin(2*t)/2))
    tp=sp.integrate(te,t);value=sp.simplify(tp.subs(t,m['d'])-tp.subs(t,m['a']))
    return m,zp,ze,rp,reduced,te,tp,value


def eligible(f,p,evidence=False):
    if set(p)!={'n','h','b','c'} or any(type(v)!=int for v in p.values()):raise ValueError('Expected integer n,h,b,c')
    if not(1<=p['n']<=16 and 1<=p['c']<=5 and 1<=p['h']<=18 and 0<=p['b']<=4):raise ValueError('Arithmetic bounds exceeded')
    if evidence:return
    if f=='cross_z':raise ValueError('Crossed-surfaces source is evidence-only')
    if f=='easy_radial':
        if p['b']!=0 or p['n'] not in (1,4,9,16) or not 1<=p['h']<=6:raise ValueError('Easy requires constant height and integer radius')
    else:
        if p['b']==0:raise ValueError('Observed family requires nonzero geometric coefficient')
        if f=='reciprocal' and p['h']<p['b']*p['n']:raise ValueError('Radical height must be real throughout disk')
        if f=='cone' and p['h']!=p['b']*sp.sqrt(p['n']):raise ValueError('Cone/cap source meets on cylinder boundary')
        if f=='half_xz' and p['h']<2*p['b']*sp.sqrt(p['n']):raise ValueError('Ordered z bounds required')
        if f in ('radial_tilt','power_tilt','half_constant') and p['h']<=p['b']*sp.sqrt(p['n']):raise ValueError('Plane must remain above lower surface')
        if f=='reciprocal' and p['n'] not in (1,4,9,16):raise ValueError('Source workload uses familiar integer radius')
        if f=='cone' and p['n'] not in (1,4,9,16):raise ValueError('Source workload uses integer cone-cap height')


BANKS={
 'radial':('correct','extra_jacobian','radial_half','angular_half','angular_double'),
 'xz':('correct','extra_jacobian','radial_half','angular_half','angular_double'),
 'reciprocal':('correct','extra_jacobian','radial_half','angular_half','angular_double'),
}
DEFAULT_PROFILE='method_bank'

N,H,B,C=sp.symbols('N H B C',positive=True)
@lru_cache(maxsize=20)
def bank_expressions(f):
    m=model(f,dict(n=N,h=H,b=B,c=C));zp=sp.integrate(m['F'],z)
    ze=sp.expand(zp.subs(z,m['high'])-zp.subs(z,m['low']))
    radial=sp.integrate(ze,(r,0,m['R']))
    if f=='reciprocal':
        # Half-radius and half-angle coincide here; use a complete distinct bank
        # with duplicated Jacobian twice and the erroneous cos(2theta)->1 step.
        return tuple(sp.simplify(e) for e in (
            sp.integrate(radial,(t,m['a'],m['d'])),
            sp.integrate(sp.integrate(ze*r**2,(r,0,m['R'])),(t,m['a'],m['d'])),
            sp.integrate(sp.integrate(ze,(r,0,m['R']/2)),(t,m['a'],m['d'])),
            sp.integrate(radial,(t,m['a'],m['a']+2*(m['d']-m['a']))),
            sp.integrate(sp.integrate(ze.subs(sp.cos(2*t),1),(r,0,m['R'])),(t,m['a'],m['d']))))
    return tuple(sp.simplify(e) for e in (
        sp.integrate(radial,(t,m['a'],m['d'])),
        sp.integrate(sp.integrate(ze*r,(r,0,m['R'])),(t,m['a'],m['d'])),
        sp.integrate(sp.integrate(ze,(r,0,m['R']/2)),(t,m['a'],m['d'])),
        sp.integrate(radial,(t,0,sp.pi)) if f=='half_linear' else sp.integrate(radial,(t,m['a'],(m['a']+m['d'])/2)),
        sp.integrate(radial,(t,m['a'],m['a']+2*(m['d']-m['a'])))))

def bank(f,p):
    values={N:p['n'],H:p['h'],B:p['b'],C:p['c']}
    vals=[sp.expand(e.subs(values)) for e in bank_expressions(f)]
    if any(not q.is_finite for q in vals):raise ValueError('Nonfinite complete bank')
    if any(sp.expand(vals[i]-vals[j])==0 for i in range(5) for j in range(i)):raise ValueError('Ambiguous complete bank')
    return vals


def projection(f,p):
    os.environ.setdefault('MPLCONFIGDIR','/tmp/cylindrical-mpl-'+str(KP_ID))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    m=model(f,p);data={'n':p['n'],'a':str(m['a']),'d':str(m['d']),'version':'projection-2'}
    key=hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()[:24]
    assets=ROOT/'assets';assets.mkdir(exist_ok=True);png=assets/(key+'.png');side=assets/(key+'.json')
    if png.exists() and side.exists():return str(png)
    R=float(m['R']);a=float(m['a']);d=float(m['d']);angle=np.linspace(a,d,361)
    fig,ax=plt.subplots(figsize=(4,4),dpi=120)
    ax.fill(np.r_[0,R*np.cos(angle),0],np.r_[0,R*np.sin(angle),0],color='#e0ebf2',edgecolor='#2679bd',lw=1.6)
    lim=1.4*R;ax.set(xlim=(-lim,lim),ylim=(-lim,lim),aspect='equal');ax.axis('off')
    ax.annotate('',xy=(lim,0),xytext=(-lim,0),arrowprops={'arrowstyle':'->','color':'#333'})
    ax.annotate('',xy=(0,lim),xytext=(0,-lim),arrowprops={'arrowstyle':'->','color':'#333'})
    ax.text(lim,.04*R,'$x$');ax.text(.04*R,lim,'$y$')
    label='$'+sp.latex(m['R'])+'$'
    for xx,yy in ((R,0),(-R,0),(0,R),(0,-R)):
        if a==0 and d<=math.pi and yy<0:continue
        if a==0 and d<=math.pi/2 and xx<0:continue
        if a<0 and xx<0:continue
        sign='-' if xx<0 or yy<0 else ''
        ax.text(xx if yy else xx, yy-.11*R if yy<0 else yy+.04*R, '$'+sign+sp.latex(m['R'])+'$',ha='center',va='top' if yy<=0 else 'bottom',fontsize=10)
    ax.text(.37*R,1.1*R,'$x^2+y^2='+str(p['n'])+'$',fontsize=11)
    fd,tmp=tempfile.mkstemp(prefix='projection-',suffix='.png',dir=assets);os.close(fd)
    try:
        fig.savefig(tmp,bbox_inches='tight',facecolor='white');os.replace(tmp,png)
    finally:
        plt.close(fig)
        if os.path.exists(tmp):os.unlink(tmp)
    fd,tmp=tempfile.mkstemp(prefix='sidecar-',suffix='.json',dir=assets)
    with os.fdopen(fd,'w') as stream:json.dump({**data,'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'sha256':hashlib.sha256(png.read_bytes()).hexdigest()},stream,indent=2)
    os.replace(tmp,side);return str(png)


def I3(m,e):return r'\int_{'+tex(m['a'])+'}^{'+tex(m['d'])+r'}\int_0^{'+tex(m['R'])+r'}\int_{'+tex(m['low'])+'}^{'+tex(m['high'])+'}'+e+r'\,dz\,dr\,d\theta'
def I2(m,e):return r'\int_{'+tex(m['a'])+'}^{'+tex(m['d'])+r'}\int_0^{'+tex(m['R'])+'}'+e+r'\,dr\,d\theta'
def I1(m,e):return r'\int_{'+tex(m['a'])+'}^{'+tex(m['d'])+'}'+e+r'\,d\theta'
def bracket(e,var,lo,hi):return '['+e+']_{'+var+'='+tex(lo)+'}^{'+var+'='+tex(hi)+'}'
def component_endpoint(e,var,lo,hi):
    parts=e.as_ordered_terms() if e.is_Add else [e]
    return '+'.join('('+tex(term.subs(var,hi))+')-('+tex(term.subs(var,lo))+')' for term in parts)
def substituted_endpoint(e,var,lo,hi):
    parts=e.as_ordered_terms() if e.is_Add else [e]
    # Do not CAS-collapse endpoint arithmetic before the operative evaluation row.
    pattern=re.escape(tex(var)) if var==t else r'(?<![A-Za-z\\])'+re.escape(tex(var))+r'(?![A-Za-z])'
    def put(term,value):return re.sub(pattern,lambda _: '('+tex(value)+')',tex(term))
    return '+'.join('('+put(term,hi)+')-('+put(term,lo)+')' for term in parts)


def normal_text(f,p):
    m,zp,ze,rp,rr,trig,tp,v=stages(f,**p)
    radius=tex(m['R']);restriction='' if m['d']==2*sp.pi else (r' for $x\ge 0,$ $y\ge 0$' if f=='quarter_x' else r' for $x\ge 0$' if m['a']<0 else r' for $y\ge 0$')
    cart_low=m['low'].subs({r*sp.sin(t):y,r*sp.cos(t):x})
    if f=='cone':cart_low=p['b']*sp.sqrt(x*x+y*y)
    if f=='reciprocal':cart_high=sp.sqrt(p['h']-p['b']*(x*x-y*y))
    else:cart_high=m['high'].subs({r*sp.sin(t):y,r*sp.cos(t):x})
    problem='Evaluate the triple integral\n\n$$\n'+r'\iiint_R '+tex(m['cart'])+r'\,\mathrm{d}V'+'\n$$\n\nover the region $R$ enclosed inside the cylinder $x^2+y^2='+str(p['n'])+'$'+restriction+' and between the surfaces $z='+tex(cart_low)+'$ and $z='+tex(cart_high)+'.$'
    intro=("We will use the change of variables formula in the form\n\n$$\n"+r'\iiint_R f(x,y,z)\,dV=\iiint_\Delta f(r\cos\theta,r\sin\theta,z)\,r\,dz\,dr\,d\theta.'+'\n$$\n\n'+"If $(r,\\theta,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas\n\n$$\nx=r\\cos\\theta,\\quad y=r\\sin\\theta,\\quad z=z.\n$$\n\nFirst, let's sketch the projection of $R$ onto the $xy$-plane:\n\n![]("+projection(f,p)+")\n\nThe region $R$ is a right vertical cylinder of radius $"+radius+"$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is\n\n- bounded below by $z="+tex(cart_low)+'='+tex(m['low'])+",$ and\n\n- bounded above by $z="+tex(cart_high)+'='+tex(m['high'])+'.$\n\nAs a result, in cylindrical polar coordinates, our region can be expressed as\n\n$$\n'+r'\Delta=\{(r,\theta,z):0\le r\le '+radius+r',\ '+tex(m['a'])+r'\le\theta<'+tex(m['d'])+r',\ '+tex(m['low'])+r'\le z\le '+tex(m['high'])+r'\}.'+'\n$$\n\nTherefore, using the change of variables formula, we obtain\n\n$$\n')
    # Actual Cartesian substitution retains both squared trig terms before reduction.
    substitution=m['cart'].subs({x:r*sp.cos(t),y:r*sp.sin(t)},simultaneous=True)
    if f in ('easy_radial','radial_tilt','half_xradial','power_tilt','cone','reciprocal'):
        sq='('+tex(r*sp.cos(t))+')^2+('+tex(r*sp.sin(t))+')^2'
        C='' if p['c']==1 else str(p['c'])+r'\cdot '
        substituted={'easy_radial':C+r'\sqrt{'+sq+'}', 'radial_tilt':C+r'\sqrt{'+sq+'}', 'half_xradial':C+tex(r*sp.cos(t))+r'\cdot\sqrt{'+sq+'}', 'power_tilt':C+'('+sq+')','cone':C+'('+sq+')','reciprocal':C+r'\frac{z}{\sqrt{'+sq+'}}'}[f]
    else:substituted=tex(substitution)
    rows=[r'\iiint_\Delta ('+substituted+r')\cdot r\,dz\,dr\,d\theta',I3(m,tex(m['F']))]
    if m['F'].has(z):
        if f=='half_xz':
            outer=tex(p['c']*r*r*sp.cos(t)/2)
            rows +=[I2(m,outer+bracket('(z)^2','z',m['low'],m['high'])),I2(m,outer+'(('+tex(m['high'])+')^2-('+tex(m['low'])+')^2)')]
        else:
            rows +=[I2(m,bracket(tex(zp),'z',m['low'],m['high'])),I2(m,substituted_endpoint(zp,z,m['low'],m['high']))]
        if f=='half_xz':
            # Preserve source squared-height expansion before distribution.
            rows += [I2(m,tex(p['c']*r*r*sp.cos(t)/2)+'('+tex(sp.expand(m['high']**2))+'-('+tex(sp.expand(m['low']**2))+'))')]
        rows += [I2(m,tex(ze))]
    else:
        rows +=[I2(m,tex(m['F'])+bracket('z','z',m['low'],m['high'])),I2(m,tex(m['F'])+'(('+tex(m['high'])+')-('+tex(m['low'])+'))')]
        # Source constant-height families show height cancellation and factorization.
        if f in ('half_xradial','half_linear','easy_radial'):rows +=[I2(m,tex(p['h']*m['F']))]
        else:rows +=[I2(m,tex(ze))]
    if f=='quarter_x':
        rr_pre=ze.subs(sp.sin(t)*sp.cos(t),sp.sin(2*t)/2);rows +=[I2(m,tex(rr_pre))];rp=sp.integrate(rr_pre,r);rr=sp.expand(rp.subs(r,m['R']))
    rows +=[I1(m,bracket(tex(rp),'r',0,m['R'])),I1(m,substituted_endpoint(rp,r,0,m['R'])),I1(m,component_endpoint(rp,r,0,m['R'])),I1(m,tex(rr))]
    if f=='half_xz':
        coeff=sp.expand(rr).coeff(sp.cos(t)**2);rest=sp.expand(rr)-coeff*sp.cos(t)**2
        rows +=[I1(m,tex(coeff)+'('+tex(sp.Rational(1,2))+'(1+'+tex(sp.cos(2*t))+'))+'+tex(rest)),I1(m,tex(trig))]
    if f=='quarter_x':trig=rr;tp=sp.integrate(trig,t)
    rows +=[bracket(tex(tp),r'\theta',m['a'],m['d']),component_endpoint(tp,t,m['a'],m['d']),tex(v)]
    if f=='half_linear':
        # Preserve q161621's operative grouping, including the scalar OUTSIDE
        # the angular primitive bracket. Extra endpoint rows supplement it.
        angular=r'\cos(\theta)-\sin(\theta)'
        factor=lambda coefficient,power=0: tex(sp.sympify(coefficient)*r**power)+r'\cdot ('+angular+')'
        scalar_primitive=sp.Rational(p['c']*p['h'],3)*r**3
        scalar=sp.simplify(scalar_primitive.subs(r,m['R']))
        primitive_text=factor(sp.Rational(p['c']*p['h'],3),3)
        delta=r'\sin(\theta)+\cos(\theta)'
        angle_parts=[sp.sin(t),sp.cos(t)]
        angle_endpoint='+'.join(tex(scalar)+r'\cdot (('+tex(term.subs(t,m['d']))+')-('+tex(term.subs(t,m['a']))+'))' for term in angle_parts)
        angle_components='+'.join('('+tex(scalar*term.subs(t,m['d']))+')-('+tex(scalar*term.subs(t,m['a']))+')' for term in angle_parts)
        rows=[r'\iiint_\Delta ('+tex(p['c'])+r'\cdot ('+tex(r*sp.cos(t))+'-'+tex(r*sp.sin(t))+r'))\cdot r\,dz\,dr\,d\theta',
              I3(m,factor(p['c'],2)),
              I2(m,factor(p['c'],2)+bracket('z','z',m['low'],m['high'])),
              I2(m,factor(p['c'],2)+'(('+tex(m['high'])+')-('+tex(m['low'])+'))'),
              I2(m,factor(p['c']*p['h'],2)),
              I1(m,bracket(primitive_text,'r',0,m['R'])),
              I1(m,'('+substituted_endpoint(scalar_primitive,r,0,m['R'])+')'+r'\cdot ('+angular+')'),
              I1(m,'('+component_endpoint(scalar_primitive,r,0,m['R'])+')'+r'\cdot ('+angular+')'),
              I1(m,factor(scalar)),
              tex(scalar)+r'\cdot '+bracket(delta,r'\theta',m['a'],m['d']),
              angle_endpoint,angle_components,tex(v)]
    worked=intro+r'\begin{aligned}\iiint_R '+tex(m['cart'])+r'\,dV &='+rows[0]+''.join(r' \\ &='+a for a in rows[1:])+r'\end{aligned}'+'\n$$'
    return problem,worked


def scaled(s,c):return s if c==1 else str(c)+r'\left('+s+r'\right)'
def raw_text(f,c):
    """Template replay with scalar-integrand slot; no original-question return branch."""
    q=SOURCES[SPECS[f][1]];problem=q[':question/problem'];solution=q.get(':question/worked-solution')
    # Complete assessed integrand spans, each restricted to its actual integral.
    m=model(f,SPECS[f][2]);source_integrands={
      'radial_tilt':r'\sqrt{x^{2} + y^{2}}','cross_z':'2z','half_xradial':r'x\sqrt{{x}^{2}+{y}^{2}}','reciprocal':r'\frac{z}{\sqrt{{x}^{2}+{y}^{2}}}',
      'cone':r'{x}^{2}+{y}^{2}','half_xz':'2xz','half_constant':'4','quarter_x':'4x','half_linear':'(x-y)','power_tilt':r'{x}^{2}+{y}^{2}'}
    fragment=source_integrands[f];problem=problem.replace(fragment,scaled(fragment,c),1)
    if solution is not None:
        # Scalar multiplication commutes with every captured evaluation stage.
        # Preserve each complete expression and prose; this is evidence only.
        split=solution.split(r'\begin{aligned}',1);prefix=split[0];chain=split[1].split(r'\end{aligned}',1)
        rows=chain[0].split(r'\\');first=rows[0].split('&',1)
        left=first[0];left=left.replace(fragment,scaled(fragment,c),1)
        rhs=first[1];rhs=rhs.replace('=', '= '+str(c)+r'\left(',1)+r'\right)' if c!=1 else rhs
        out=[left+'&'+rhs]
        for row in rows[1:]:
            before,expression=row.split('=',1)
            leading=expression[:len(expression)-len(expression.lstrip())]
            trailing=expression[len(expression.rstrip()):]
            core=expression.strip()
            punctuation='.' if core.endswith('.') else ''
            core=core.removesuffix('.')
            out.append(before+'='+leading+scaled(core,c)+punctuation+trailing)
        solution=prefix+r'\begin{aligned}'+r'\\'.join(out)+r'\end{aligned}'+chain[1]
    return problem,solution


def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:'+v))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError(level)
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only source-shaped radio fields')
    rng=random.Random(seed);profile=profile or DEFAULT_PROFILE
    raw=profile=='source_raw'
    if profile not in (DEFAULT_PROFILE,'source_raw'):raise ValueError(profile)
    choices=[k for k,v in SPECS.items() if v[0]==level and k!='cross_z']
    f=template or rng.choice(choices)
    if f not in SPECS or SPECS[f][0]!=level:raise ValueError('Template/level mismatch')
    if raw:
        if SPECS[f][1] is None:raise ValueError('No source bank')
        p=parameters or {'scale':1}
        if set(p)!={'scale'} or type(p['scale'])!=int or not 1<=p['scale']<=5:raise ValueError('Raw profile accepts only scalar1..5')
        source=SOURCES[SPECS[f][1]];problem,solution=raw_text(f,p['scale'])
        vals=[scaled(a[':answer/value'],p['scale']) for a in source[':question/answer-fields'][0][':answer-field/choices']]
        field0=source[':question/answer-fields'][0]
        correct=next((i for i,a in enumerate(field0[':answer-field/choices']) if a[':answer/id']==field0.get(':answer-field/correct',{}).get(':answer/id')),None)
        mathmodel=model(f,SPECS[f][2]);mathmodel['F']*=p['scale']
        inferred_value=stages(f,**SPECS[f][2])[-1]*p['scale']
        fingerprint=digest({'assessed':str(mathmodel['F']),'bounds':[str(mathmodel[k]) for k in ('R','a','d','low','high')]})
    else:
        for attempt in range(500):
            p=copy.deepcopy(parameters) if parameters is not None else sample(f,rng)
            eligible(f,p)
            try:vals0=bank(f,p)
            except ValueError:
                if parameters is not None:raise
                continue
            break
        else:raise ValueError('No eligible complete bank')
        vals=list(map(tex,vals0));correct=0;problem,solution=normal_text(f,p);source=None
        mathmodel=model(f,p);inferred_value=vals0[0]
        fingerprint=digest({'assessed':str(mathmodel['F']),'bounds':[str(mathmodel[k]) for k in ('R','a','d','low','high')]})
    attributes={':question/problem':problem}
    if solution is not None:attributes[':question/worked-solution']=solution
    if not raw or ':question/difficulty' in source:attributes[':question/difficulty']=':question.difficulty/'+level
    identity=digest({'version':VERSION,'question':attributes,'bank':sorted(vals),'correct_value':None if correct is None else vals[correct]})
    fid=uid(identity+':field:selection');answers=[{':answer/id':uid(fid+':'+str(i)+':'+value),':answer/type':':answer.type/math',':answer/value':value} for i,value in enumerate(vals)]
    correctid=answers[correct][':answer/id'] if correct is not None else None;rng.shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    if correctid is not None:field[':answer-field/correct']=[':answer/id',correctid]
    attributes[':question/id']=uid(identity);attributes[':question/answer-fields']=[field]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':attributes,'generation':{'version':VERSION,'template':f,'level':level,'parameters':p,'profile':profile,'seed':seed,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_id':SPECS[f][1],'content_identity':identity,'mathematical_fingerprint':fingerprint,'evidence_only':raw,'eligible_for_learning':not raw,'inferred_exact_value':str(inferred_value),'bank_recipes':None if raw else ['correct','duplicate_jacobian_twice','halve_radial_bound','double_angular_span','omit_cos_double_angle'] if f=='reciprocal' else ['correct','duplicate_jacobian','halve_radial_bound','wrong_halfplane' if f=='half_linear' else 'halve_angular_span','double_angular_span'],'python':sys.version.split()[0],'sympy':sp.__version__}}


def sample(f,rng):
    while True:
        n=rng.choice([1,4,9,16] if f in ('easy_radial','cone','reciprocal') else list(range(1,10)))
        c=rng.randint(1,5);b=0 if f=='easy_radial' else rng.randint(1,3)
        if f=='easy_radial':h=rng.randint(1,6)
        elif f=='cone':h=b*math.isqrt(n)
        elif f=='reciprocal':h=rng.randint(b*n,min(18,b*n+6)) if b*n<=18 else 99
        elif f=='half_xz':h=rng.randint(math.ceil(2*b*math.sqrt(n)),min(18,math.ceil(2*b*math.sqrt(n))+5))
        elif f in ('radial_tilt','power_tilt','half_constant'):h=rng.randint(math.floor(b*math.sqrt(n))+1,min(18,math.floor(b*math.sqrt(n))+7))
        else:h=rng.randint(1,12)
        p=dict(n=n,h=h,b=b,c=c)
        try:eligible(f,p);return p
        except ValueError:continue

# Easy: authored fixed-height radial specialization, no expansion/identities.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: captured cone, reciprocal-radius, radial-plane templates; unrated radial tilt is explicitly authored moderate.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: captured labels retained; squared-height, angular identity, product or signed sum stages as applicable.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)


def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[No captured worked solution.]')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    output=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(output,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,output)))
if __name__=='__main__':main()
