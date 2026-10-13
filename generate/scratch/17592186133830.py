#!/usr/bin/env python3
"""Scalar ds integral evaluation, math basis 1356. Local review only; step 7.

Observed source banks use public raw_<family> profiles, preserve absent attributes,
and are evidence-only. They are opaque homogeneous scalar-field extensions, not
recovered error intent. Normal profiles derive five complete operations from the
printed substitution/speed/primitive. Explicit and sampled bounds are identical.
Easy: constant-speed affine substitution; moderate: observed trig identities or
polynomial/power integrands; hard: authored two-component direct integration with
involute derivative cancellation or the observed perfect-square speed recipe.
No change of variable, vector work, registration, network, or database writes.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp

HERE=Path(__file__).with_suffix(''); VERSION='scalar-evaluation-v1'
CAPTURE=json.loads((HERE/'source.json').read_text()); SOURCE={k:CAPTURE[k] for k in ('database','basis','lineage')}
REC=CAPTURE['record']; KP_ID=17592186133830
T=sp.Symbol('t',real=True); X,Y=sp.symbols('x y',real=True)
SOURCES={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
SOURCE_FAMILY={'q-167609':'sum','q-76434':'reciprocal','q-167621':'circle_cos','q-76433':'circle_sin','q-76447':'cubic','q-40258':'fractional','q-41160':'involute'}
FAMILY_SOURCE={v:k for k,v in SOURCE_FAMILY.items()}
TEMPLATES={'sum':'easy','reciprocal':'easy','circle_cos':'moderate','circle_sin':'moderate','cubic':'moderate','fractional':'moderate','involute':'hard','mixed_fractional':'hard'}
FORMULA=r'\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.'
PAIR_DOMAIN=((4,3),(3,4))
COEFF=(-3,-2,-1,1,2,3)
ANGLE_INTERVALS=((0,sp.pi/4),(-sp.pi/4,0),(sp.pi/4,sp.pi/2),(0,sp.pi/2),(-sp.pi/2,-sp.pi/4))
POWER_INTERVALS=((0,1),(0,2),(1,2),(1,3))
INV_INTERVALS=((0,1),(1,2),(0,sp.pi),(sp.pi/2,sp.pi),(1,3))

def L(e): return sp.latex(sp.sympify(e),ln_notation=True).replace(r'\log',r'\ln')
def G(e): return '('+L(e)+')'
def uid(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:'+s))
def digest(o): return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def eq(a,b): return sp.simplify(sp.trigsimp(a-b))==0

def parse(e):
    # Local exact grammar matching this KP's observed scalar banks.
    import importlib.util
    spec=importlib.util.spec_from_file_location('scalar_math_parser',HERE/'math_parser.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.expr(e)

def align(rows): return '$$\n\\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def scalar_scaled(e,c): return e if c==1 else L(c)+r'\left('+e+r'\right)'

RAW_F_SLOT={'sum':'x+y','reciprocal':r'\frac{1}{y-x}','circle_cos':r'2{x}^{2}-16','circle_sin':r'{y}^{2}','cubic':r'{x}^{3}-2{y}^{3}','fractional':'3x','involute':r'x^{2} + y^{2}'}

def raw_text(src,fam,c):
    """Component masks, never a source-payload-return path.

    The complete integrand is a slot. Raw solutions preserve all source rows,
    including the three documented math errors, and scale each scalar stage.
    Derivative/speed blocks and the formal definition remain fixed.
    """
    f=RAW_F_SLOT[fam]
    prompt=src[':question/problem'].replace(f,scalar_scaled(f,c))
    solution=src.get(':question/worked-solution')
    if solution is None:return prompt,None
    solution=solution.replace('f(x,y)='+f,'f(x,y)='+scalar_scaled(f,c))
    blocks=list(re.finditer(r'\$\$\n(.*?)\n\$\$',solution,re.S))
    replacements=[]
    for j,m in enumerate(blocks):
        b=m.group(1)
        if j<2:continue
        if c==1: new=b
        else:
            # The third block substitutes f, the fourth evaluates the ds integral.
            rows=b.split(r' \\ ')
            out=[]
            for i,row in enumerate(rows):
                end=r'\end{aligned}' if row.endswith(r'\end{aligned}') else ''
                if end:row=row[:-len(end)]
                if j==2:
                    parts=row.split('=');row=parts[0]+'='+ '='.join(scalar_scaled(p,c) for p in parts[1:])
                elif i==0:
                    row=row.replace(f,scalar_scaled(f,c))
                else:
                    parts=row.split('=',1);row=parts[0]+'='+scalar_scaled(parts[1],c)
                out.append(row+end)
            new=r' \\ '.join(out)
        replacements.append((m.start(1),m.end(1),new))
    for a,b,new in reversed(replacements):solution=solution[:a]+new+solution[b:]
    return prompt,solution


def sample(f,r):
    if f in ('sum','reciprocal'):
        lo=r.choice((-2,-1,0,1));return dict(a=r.choice((-4,-3,-2,-1,1,2,3,4)),b=r.choice((-6,-5,-4,-3,-2,-1,1,2,3,4,5,6)),c=r.choice(COEFF),lower=lo,upper=lo+r.choice((1,2,3,4)))
    if f.startswith('circle'):
        lo,hi=r.choice(ANGLE_INTERVALS);return dict(R=r.randint(1,6),c=r.choice(COEFF),orientation=r.choice((-1,1)),lower=str(lo),upper=str(hi))
    if f=='cubic':
        a,b=r.choice(PAIR_DOMAIN);lo,hi=0,1;return dict(a=a*r.choice((-1,1)),b=b*r.choice((-1,1)),c=r.choice(COEFF),k=r.choice((1,2,3)),lower=lo,upper=hi)
    if f in ('fractional','mixed_fractional'):
        lo,hi=r.choice(POWER_INTERVALS);p=dict(s=r.randint(1,5),c=r.choice(COEFF),lower=lo,upper=hi)
        if f=='mixed_fractional':p['d']=r.choice(COEFF)
        return p
    lo,hi=r.choice(INV_INTERVALS);return dict(A=r.randint(1,5),c=r.choice(COEFF),d=r.choice(COEFF),lower=str(lo),upper=str(hi))


def validate_parameters(f,p):
    base=sample(f,random.Random(0));expected=set(base)
    if set(p)!=expected:raise ValueError(f'Expected exactly {sorted(expected)} parameters')
    p={k:sp.sympify(v,locals={'pi':sp.pi}) for k,v in p.items()}
    if any(v.free_symbols or v.is_real is not True for v in p.values()):raise ValueError('All parameters must be exact real constants')
    lo,hi=p['lower'],p['upper']
    if f in ('sum','reciprocal'):
        if p['a'] not in (-4,-3,-2,-1,1,2,3,4) or p['b'] not in tuple(range(-6,0))+tuple(range(1,7)) or p['c'] not in COEFF or lo not in (-2,-1,0,1) or hi-lo not in (1,2,3,4):raise ValueError('Easy bounds/coefficient workload')
    elif f.startswith('circle'):
        if p['R'] not in range(1,7) or p['c'] not in COEFF or p['orientation'] not in (-1,1) or (lo,hi) not in ANGLE_INTERVALS:raise ValueError('Moderate circle workload')
    elif f=='cubic':
        if (abs(p['a']),abs(p['b'])) not in PAIR_DOMAIN or p['c'] not in COEFF or p['k'] not in (1,2,3) or (lo,hi)!=(0,1) or p['a']**3==p['k']*p['b']**3:raise ValueError('Cubic workload/nonzero substitution')
    elif f in ('fractional','mixed_fractional'):
        if p['s'] not in range(1,6) or p['c'] not in COEFF or (lo,hi) not in POWER_INTERVALS or ('d' in p and p['d'] not in COEFF):raise ValueError('Fractional workload')
    else:
        if p['A'] not in range(1,6) or p['c'] not in COEFF or p['d'] not in COEFF or (lo,hi) not in INV_INTERVALS:raise ValueError('Hard involute workload')
        if p['c']*p['A']**2+p['d']==0:raise ValueError('Hard requires both nonzero reduced primitive components')
    return p


def math_data(f,p):
    c=p['c'];lo,hi=p['lower'],p['upper']
    if f in ('sum','reciprocal'):
        a,b=p['a'],p['b'];x,y=a*T,a*T+b;v=abs(a)*sp.sqrt(2);F=c*(X+Y) if f=='sum' else c/(Y-X)
    elif f.startswith('circle'):
        R,o=p['R'],p['orientation'];x,y=R*sp.cos(T),o*R*sp.sin(T);v=R;F=c*(2*X**2-R**2) if f=='circle_cos' else c*Y**2
    elif f=='cubic':
        a,b=p['a'],p['b'];x,y=a*T**2,b*T**2;v=2*sp.sqrt(a*a+b*b)*T;F=c*(X**3-p['k']*Y**3)
    elif f in ('fractional','mixed_fractional'):
        s=p['s'];x,y=sp.Rational(4,3)*s*T**sp.Rational(3,2),s*(T*T/2-T);v=s*(T+1);F=c*X+(p.get('d',0))*Y
    else:
        A=p['A'];x,y=A*(sp.cos(T)+T*sp.sin(T)),A*(sp.sin(T)-T*sp.cos(T));v=A*T;F=c*(X**2+Y**2)+p['d']
    sub=sp.expand(F.subs({X:x,Y:y}));sub=sp.trigsimp(sub)
    if f=='circle_cos':sub=c*p['R']**2*sp.cos(2*T)
    if f=='involute':sub=c*p['A']**2*(1+T*T)+p['d']
    I=sp.expand(sub*v);primitive=sp.integrate(I,T);value=sp.simplify(primitive.subs(T,hi)-primitive.subs(T,lo))
    return x,y,F,v,sub,I,primitive,value


def integral(e,lo,hi):return r'\int_{'+L(lo)+'}^{'+L(hi)+'}'+e+r'\,\text{d}t'

def stages(f,p,data):
    """Each family owns its operative substitution/reduction/primitive stages."""
    x,y,F,v,sub,I,P,result=data;c=p['c'];lo,hi=p['lower'],p['upper']
    deriv=[r'r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j',r'&=\frac{\text{d}}{\text{d}t}'+G(x)+r'i+\frac{\text{d}}{\text{d}t}'+G(y)+'j',r'&='+G(sp.diff(x,T))+'i+'+G(sp.diff(y,T))+'j',r'\|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2}',r'&=\sqrt{'+G(sp.diff(x,T))+'^2+'+G(sp.diff(y,T))+'^2}']
    subst=[];extra=[];prim_terms=[]
    if f in ('sum','reciprocal'):
        deriv += [r'&=\sqrt{'+L(2*p['a']**2)+'}',r'&='+L(v)]
        if f=='sum':
            subst=[r'f(r(t))&='+G(c)+r'\left('+L(x)+'+'+G(y)+r'\right)',r'&='+L(sub)]
            prim_terms=[c*v*p['a']*T**2,c*v*p['b']*T]
        else:
            subst=[r'f(r(t))&=\frac{'+L(c)+'}{'+G(y)+'-'+G(x)+'}',r'&=\frac{'+L(c)+'}{'+L(p['b'])+'}',r'&='+L(sub)];prim_terms=[c*v/p['b']*T]
    elif f.startswith('circle'):
        R=p['R'];deriv += [r'&=\sqrt{'+L(R**2)+r'\sin^2t+'+L(R**2)+r'\cos^2t}',r'&=\sqrt{'+L(R**2)+r'(\sin^2t+\cos^2t)}',r'&=\sqrt{'+L(R**2)+'}',r'&='+L(v)]
        if f=='circle_cos':
            subst=[r'f(r(t))&='+G(c)+r'\left(2'+G(x)+'^2-'+L(R**2)+r'\right)',r'&='+G(c*R**2)+r'(2\cos^2t-1)',r'&='+L(sub)]
            extra=[r'&='+L(c*R**3)+integral(r'\cos 2t',lo,hi)];prim_terms=[c*R**3*sp.sin(2*T)/2]
        else:
            subst=[r'f(r(t))&='+G(c)+G(y)+'^2',r'&='+L(c*R**2)+r'\sin^2t']
            extra=[r'&='+L(c*R**3)+integral(r'\sin^2t',lo,hi),r'&='+L(c*R**3)+integral(r'\frac{1-\cos 2t}{2}',lo,hi),r'&='+L(c*R**3/2)+integral(r'1-\cos 2t',lo,hi)]
            prim_terms=[c*R**3*T/2,-c*R**3*sp.sin(2*T)/4]
    elif f=='cubic':
        a,b,k=p['a'],p['b'],p['k'];n=sp.sqrt(a*a+b*b)
        deriv += [r'&=\sqrt{'+L(4*a*a)+r't^2+'+L(4*b*b)+r't^2}',r'&=\sqrt{'+L(4*n*n)+r't^2}',r'&='+L(2*n)+r'|t|',r'&='+L(v)]
        subst=[r'f(r(t))&='+G(c)+r'\left('+G(x)+'^3-'+G(k)+G(y)+r'^3\right)',r'&='+G(c)+r'\left('+G(a)+r'^3t^6-'+G(k)+G(b)+r'^3t^6\right)',r'&='+G(c)+r'\left('+L(a**3)+r't^6-'+G(k*b**3)+r't^6\right)',r'&='+L(sub)]
        extra=[r'&='+L(c*(a**3-k*b**3)*2*n)+integral(r't^7',lo,hi)];prim_terms=[c*(a**3-k*b**3)*n*T**8/4]
    elif f in ('fractional','mixed_fractional'):
        s=p['s'];deriv += [r'&=\sqrt{'+L(4*s*s)+r't+'+L(s*s)+r'(t-1)^2}',r'&=\sqrt{'+L(s*s)+r'(t^2+2t+1)}',r'&='+L(s)+r'|t+1|',r'&='+L(v)]
        subst=[r'f(r(t))&='+G(c)+G(x)+(('+'+G(p['d'])+G(y)) if 'd' in p else ''),r'&='+L(sub)]
        # Preserve the distributed products before collecting powers.
        distributed=L(sp.Rational(4,3)*c*s*s)+r't^{3/2}(t+1)'
        if 'd' in p:distributed+='+'+G(p['d']*s*s)+r'(t^2/2-t)(t+1)'
        extra=[r'&='+integral(distributed,lo,hi),r'&='+integral(L(I),lo,hi)]
        prim_terms=[sp.Rational(8,21)*c*s*s*T**sp.Rational(7,2),sp.Rational(8,15)*c*s*s*T**sp.Rational(5,2)]
        if 'd' in p:prim_terms += [p['d']*s*s*T**4/8,-p['d']*s*s*T**3/6,-p['d']*s*s*T**2/2]
    else:
        A,d=p['A'],p['d']
        deriv[2:3]=[r'&='+G(A)+r'(-\sin t+\sin t+t\cos t)i+'+G(A)+r'(\cos t-\cos t+t\sin t)j',r'&='+G(A*T*sp.cos(T))+'i+'+G(A*T*sp.sin(T))+'j']
        deriv += [r'&=\sqrt{'+L(A*A)+r't^2(\cos^2t+\sin^2t)}',r'&='+L(A)+r'|t|',r'&='+L(v)]
        subst=[r'f(r(t))&='+G(c)+r'\left('+G(x)+'^2+'+G(y)+r'^2\right)+'+G(d),r'&='+G(c*A*A)+r'\left(\cos^2t+2t\sin t\cos t+t^2\sin^2t+\sin^2t-2t\sin t\cos t+t^2\cos^2t\right)+'+G(d),r'&='+G(c*A*A)+r'(1+t^2)+'+G(d),r'&='+L(sp.expand(sub))]
        extra=[r'&='+integral(L(I),lo,hi)];prim_terms=[A*(c*A*A+d)*T*T/2,c*A**3*T**4/4]
    rows=[r'\int_C '+L(F)+r'\,\text{d}s&='+integral(r'f(r(t))\|r^{\prime}(t)\|',lo,hi),r'&='+integral(G(sub)+r'\cdot '+G(v),lo,hi)]
    if f in ('sum','reciprocal'):rows.append(r'&='+G(v)+integral(L(sub),lo,hi))
    if f not in ('fractional','mixed_fractional','involute'):rows.append(r'&='+integral(L(I),lo,hi))
    rows+=extra
    brackets=lambda body: r'\left['+body+r'\right]_{'+L(lo)+'}^{'+L(hi)+'}'
    if f=='sum':rows.append(r'&='+G(v*c)+brackets(L(p['a']*T*T)+ '+'+G(p['b']*T)))
    if f=='reciprocal':rows.append(r'&='+G(v*c/p['b'])+brackets('t'))
    if f=='circle_cos':rows.append(r'&='+G(c*p['R']**3)+brackets(r'\frac{1}{2}\sin 2t'))
    if f=='circle_sin':rows.append(r'&='+G(c*p['R']**3/2)+brackets(r't-\frac{\sin 2t}{2}'))
    if f=='cubic':rows.append(r'&='+G(c*(p['a']**3-p['k']*p['b']**3)*2*sp.sqrt(p['a']**2+p['b']**2))+brackets(r'\frac{t^8}{8}'))
    primitive_mask='+'.join(G(e) for e in prim_terms)
    # Individually evaluated components at BOTH endpoints, before collection.
    endpoint_masks=[]
    endpoint_values=[]
    for z in (hi,lo):
        masks=[];vals=[]
        for e in prim_terms:
            masks.append(re.sub(r'(?<![A-Za-z])t(?![A-Za-z])',lambda _:G(z),L(e)))
            vals.append(e.subs(T,z))
        endpoint_masks.append('+'.join('('+m+')' for m in masks))
        endpoint_values.append(vals)
    rows += [r'&=\left['+primitive_mask+r'\right]_{'+L(lo)+'}^{'+L(hi)+'}',r'&=\left('+endpoint_masks[0]+r'\right)-\left('+endpoint_masks[1]+r'\right)',r'&=\left('+'+'.join(G(e) for e in endpoint_values[0])+r'\right)-\left('+'+'.join(G(e) for e in endpoint_values[1])+r'\right)',r'&='+L(result)+'.']
    assert eq(sum(prim_terms),P)
    note=''
    if f in ('cubic','involute'):note='Notice that $|t|=t$ since $t\\geq0$ along the path of $C.$\n\n'
    if f in ('fractional','mixed_fractional'):note='Notice that $|t+1|=t+1$ since $t\\geq0$ along the path of $C.$\n\n'
    sol='To calculate the line integral, we will use the formula\n\n$$\n'+FORMULA+'\n$$\n\nSince $r(t)=⟨'+L(x)+r',\,'+L(y)+'⟩,$ then along the curve we have $x='+L(x)+'$ and $y='+L(y)+'.$\n\nComputing $r^{\\prime}(t)$ and $\\|r^{\\prime}(t)\\|,$ we get the following:\n\n'+align(deriv)+'\n\n'+note+'Now, if $f(x,y)='+L(F)+'$, then we obtain\n\n'+align(subst)+'\n\nTherefore, we can write the integral as\n\n'+align(rows)
    return sol,{'derivative_rows':deriv,'substitution_rows':subst,'integral_rows':rows,'primitive_components':[str(e) for e in prim_terms],'endpoint_component_values':[[str(e) for e in a] for a in endpoint_values]}


def authored_bank(f,p,data):
    x,y,F,v,sub,I,P,result=data;lo,hi=p['lower'],p['upper'];c=p['c']
    def definite(e):return sp.simplify(sp.integrate(e,(T,lo,hi)))
    # Five operations selected together before parameter sampling. Duplicate speed
    # means integrating f(r)*speed^2, including nonconstant speed in hard families.
    if f=='sum':
        errors=[('omit_speed',definite(sub)),('speed_squared',definite(sub*v*v)),('omit_y_offset',definite(c*2*p['a']*T*v)),('omit_x_coordinate',definite(c*y*v))]
    elif f=='reciprocal':
        errors=[('omit_speed',definite(sub)),('speed_squared',definite(sub*v*v)),('reverse_denominator',definite(-sub*v)),('multiply_offset_instead_of_reciprocal',definite(c*p['b']*v))]
    elif f=='circle_cos':
        errors=[('omit_speed',definite(sub)),('speed_squared',definite(sub*v*v)),('omit_inner_chain_factor',2*result),('omit_constant_subtraction',definite(c*2*x*x*v))]
    elif f=='circle_sin':
        R=p['R'];wrong=c*R**3*(T/2+sp.sin(2*T)/4)
        wrong_chain=c*R**3*(T/2-sp.sin(2*T)/2)
        errors=[('omit_speed',definite(sub)),('speed_squared',definite(sub*v*v)),('reverse_half_angle_sign',sp.simplify(wrong.subs(T,hi)-wrong.subs(T,lo))),('omit_primitive_inner_chain_factor',sp.simplify(wrong_chain.subs(T,hi)-wrong_chain.subs(T,lo)))]
    elif f=='cubic':
        errors=[('omit_speed',definite(sub)),('speed_squared',definite(sub*v*v)),('omit_y_coefficient',definite(c*(x**3-y**3)*v)),('add_instead_of_subtract',definite(c*(x**3+p['k']*y**3)*v))]
    elif f=='fractional':
        errors=[('omit_speed',definite(sub)),('speed_squared',definite(sub*v*v)),('omit_speed_constant',definite(sub*p['s']*T)),('divide_by_old_power',sp.simplify((sp.Rational(4,3)*c*p['s']**2*(T**sp.Rational(7,2)/sp.Rational(5,2)+T**sp.Rational(5,2)/sp.Rational(3,2))).subs(T,hi)-(sp.Rational(4,3)*c*p['s']**2*(T**sp.Rational(7,2)/sp.Rational(5,2)+T**sp.Rational(5,2)/sp.Rational(3,2))).subs(T,lo)))]
    elif f=='mixed_fractional':
        errors=[('omit_speed',definite(sub)),('speed_squared',definite(sub*v*v)),('omit_y_term',definite(c*x*v)),('omit_x_term',definite(p['d']*y*v))]
    else:
        errors=[('omit_speed',definite(sub)),('speed_squared',definite(sub*v*v)),('omit_field_constant',definite(c*p['A']**2*(1+T*T)*v)),('omit_t_squared_in_radius',definite((c*p['A']**2+p['d'])*v))]
    bank=[('correct',result)]+errors
    if any(e.is_real is not True or e.has(sp.oo,sp.zoo,sp.nan) for _,e in bank):raise ValueError('Whole bank invalid domain')
    if any(eq(a[1],b[1]) for i,a in enumerate(bank) for b in bank[:i]):raise ValueError('Whole bank collision')
    return bank


def source_parameters(f,c):
    # Independently derived source mathematical components, not answer lookups.
    base={
        'sum':dict(a=1,b=1,c=c,lower=0,upper=1),
        'reciprocal':dict(a=1,b=-4,c=c,lower=0,upper=4),
        'circle_cos':dict(R=4,c=c,orientation=1,lower=0,upper=sp.pi/4),
        'circle_sin':dict(R=2,c=c,orientation=1,lower=0,upper=sp.pi/4),
        'cubic':dict(a=4,b=3,c=c,k=2,lower=0,upper=1),
        'fractional':dict(s=1,c=3*c,lower=0,upper=1),
        'involute':dict(A=3,c=c,d=0,lower=0,upper=2*sp.pi)}
    return {k:sp.sympify(v) for k,v in base[f].items()}

def task_fingerprint_data(data,p):
    x,y,F,v,sub,I,P,result=data
    return {'curve':[sp.srepr(sp.expand_trig(x)),sp.srepr(sp.expand_trig(y))],
            'field':sp.srepr(sp.cancel(sp.expand(F))),
            'integrand':sp.srepr(sp.trigsimp(sp.expand(I))),
            'bounds':[str(p['lower']),str(p['upper'])],
            'assessed_response':'evaluate_scalar_ds'}

def record(level,f,p,profile,seed):
    raw=profile.startswith(('raw_','completed_'));completed=profile.startswith('completed_');src=SOURCES[FAMILY_SOURCE[f]] if f in FAMILY_SOURCE else None
    if raw:
        if profile not in ('raw_'+f,'completed_'+f) or (completed and f not in ('fractional','involute')):raise ValueError('Profile incompatible with family')
        if set(p)!= {'c'} or sp.sympify(p['c']) not in COEFF:raise ValueError('Raw scalar c must be one of -3,-2,-1,1,2,3')
        c=sp.sympify(p['c']);p={'c':c};prompt,solution=raw_text(src,f,c)
        old=src[':question/answer-fields'][0]
        bank=[('observed_'+str(i),parse(a[':answer/value'])*c) for i,a in enumerate(old[':answer-field/choices'])]
        texts=[scalar_scaled(a[':answer/value'],c) for a in old[':answer-field/choices']]
        correct=next((i for i,a in enumerate(old[':answer-field/choices']) if old.get(':answer-field/correct',{}).get(':answer/id')==a[':answer/id']),None)
        detail={};anchor=source_parameters(f,c);d=math_data(f,anchor)
        if completed:
            solution,detail=stages(f,anchor,d)
            correct=next(i for i,(_,e) in enumerate(bank) if eq(e,d[-1]))
        fp=task_fingerprint_data(d,anchor)
    else:
        if profile!='method_'+f:raise ValueError('Unknown or incompatible complete bank')
        p=validate_parameters(f,p);data=math_data(f,p);bank=authored_bank(f,p,data);texts=[L(e) for _,e in bank];correct=0
        x,y,F,v,sub,I,P,res=data
        prompt='Evaluate the line integral of the function $f(x,y)='+L(F)+'$ along the curve $C$ parametrized by $r(t)=⟨'+L(x)+r',\,'+L(y)+'⟩$ for $t\\in ['+L(p['lower'])+','+L(p['upper'])+'].$'
        solution,detail=stages(f,p,data)
        # Parameterization/traversal matter here because derivatives and bounds
        # are assessed, even for geometrically identical reparameterized paths.
        fp=task_fingerprint_data(data,p)
    mathematical_fingerprint=digest(fp)
    actual_level=(':question.difficulty/'+level if completed else src.get(':question/difficulty',{}).get(':db/ident')) if raw else ':question.difficulty/'+level
    identity=digest({'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(texts),'difficulty':actual_level,'field_type':':answer-field.type/radio','correct':None if correct is None else texts[correct]})
    qid=uid(identity);fid=uid(identity+':selection');choices=[{':answer/id':uid(fid+':'+texts[i]),':answer/type':':answer.type/math',':answer/value':text} for i,text in enumerate(texts)]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
    if correct is not None:field[':answer-field/correct']=[':answer/id',choices[correct][':answer/id']]
    random.Random(seed).shuffle(choices)
    q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if actual_level is not None:q[':question/difficulty']=actual_level
    if solution is not None:q[':question/worked-solution']=solution
    return {'knowledge_point':{'db_id':KP_ID,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'source':SOURCE,'template':f,'bank_profile':profile,'seed':seed,'parameters':{k:str(v) for k,v in p.items()},'mathematical_fingerprint':mathematical_fingerprint,'content_fingerprint':identity,'evidence_only':raw,'eligible_for_learning':not raw,'difficulty_provenance':'inferred key; authored level; authored worked solution; opaque historical bank' if completed else 'observed label/absence' if raw else 'authored level policy' if f in ('fractional','involute','mixed_fractional') else 'observed family workload','source_ids':([] if src is None else [src[':question/math-academy-id']]),'recipe_values':{name:str(e) for name,e in bank},'stages':detail,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'domain':'increasing finite t bounds; scalar field defined on entire printed path; isolated stationary endpoints allowed'}}


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Invalid difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Source fields are radio; no blank extension is provided')
    r=random.Random(seed)
    if template is None and profile is not None:template=profile.removeprefix('raw_').removeprefix('completed_').removeprefix('method_')
    f=template or r.choice([k for k,v in TEMPLATES.items() if v==level])
    if f not in TEMPLATES:raise ValueError('Unknown template')
    if TEMPLATES[f]!=level:raise ValueError('Template level does not match authored policy')
    profile=profile or 'method_'+f
    if profile.startswith(('raw_','completed_')):
        return record(level,f,{'c':1} if parameters is None else parameters,profile,seed)
    if parameters is not None:return record(level,f,parameters,profile,seed)
    # Family and complete bank are fixed before sampling; reject entire instances.
    for _ in range(500):
        try:return record(level,f,sample(f,r),profile,seed)
        except ValueError as e:
            if not any(s in str(e) for s in ('collision','nonzero','components')):raise
    raise RuntimeError('No eligible whole instance in bounded sampler')

# Easy: two observed constant-speed affine families, no extra integration method.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: three rated families and explicitly assigned fractional source family.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: two authored unordered workloads, both direct primitives after ds reduction.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question'];out=[q[':question/problem'],'']
    for f in q.get(':question/answer-fields',[]):
        for i,a in enumerate(f[':answer-field/choices']):out.append(f'{i+1}. ${a[":answer/value"]}$')
    out+=['',q.get(':question/worked-solution','[No worked solution in raw source.]')]
    return '\n'.join(out)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('markdown','json'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
    if a.count<1:ap.error('--count must be positive')
    family=a.template or (a.profile.removeprefix('raw_').removeprefix('completed_').removeprefix('method_') if a.profile else None)
    levels=(TEMPLATES[family],) if a.difficulty=='all' and family in TEMPLATES else ('easy','moderate','hard') if a.difficulty=='all' else (a.difficulty,)
    rows=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in levels for i in range(a.count)]
    print(json.dumps(rows,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rows))
if __name__=='__main__':main()
