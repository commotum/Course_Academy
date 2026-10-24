#!/usr/bin/env python3
"""Seeded exponential chain-rule questions, base capture 3948; bank repair 6468.

Original banks are retained as historical profiles. Normal method profiles retain
source demands and solution stages, with signed coefficient and point variations.
No database or network access; no generated assets are needed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
import uuid
from pathlib import Path

import sympy as sp
from math_format import normalize_prose, normalize_tex, checked_math_content

ROOT = Path(__file__).resolve().parent
CAPTURE = json.loads((ROOT/'source.json').read_text())
RECORD = CAPTURE['record']
SOURCES = {q[':question/math-academy-id']: q for q in RECORD[':knowledge-point/questions']}
CANONICAL = RECORD[':knowledge-point/canonical-example']
SOURCES[CANONICAL[':question/math-academy-id']] = CANONICAL
X = sp.Symbol('x', real=True)
U = sp.Symbol('u', real=True)
VERSION = 'general-exponential-chain-3'
KP = {'db_id': 17592186092261, 'id': RECORD[':knowledge-point/id'],
      'title': RECORD[':knowledge-point/title']}
# c*b^(a*x^n + k*x^2 + l*x + d), source term order is kept separately.
SPECS = {
 'q-48565': dict(level='easy', b=3,c=1,a=2,n=2,k=0,l=0,d=0,name='f', order='high', braces=True,log='opparen',kind='radio'),
 'q-48631': dict(level='easy', b=3,c=1,a=6,n=2,k=0,l=0,d=-4,name='y',order='high',braces=False,log='slashparen',kind='radio',unrated=True),
 'q-107458':dict(level='easy',b=2,c=1,a=-1,n=3,k=0,l=0,d=3,name='f',order='constant',braces=True,log='opbareplain',kind='blank',fieldless=True),
 'q-71881':dict(level='easy',b=5,c=2,a=1,n=3,k=0,l=1,d=0,name='y',order='low',braces=True,log='opbareplain',kind='blank',fieldless=True),
 'q-107459':dict(level='easy',b=4,c=3,a=1,n=2,k=0,l=0,d=-1,name='y',order='high',braces=True,log='bare',kind='radio'),
 'q-107461':dict(level='easy',b=6,c=1,a=-4,n=1,k=0,l=0,d=1,name='f',order='constant',braces=True,log='bare',kind='radio'),
 'q-1952':dict(level='easy',b=2,c=1,a=9,n=1,k=0,l=0,d=0,name='y',order='high',braces=True,log='opbare',kind='radio'),
 'q-312462':dict(level='easy',b=5,c=1,a=1,n=3,k=0,l=0,d=1,name='f',order='high',braces=True,log='paren',kind='blank',fragment=True),
 'q-340969':dict(level='moderate',b=5,c=1,a=-1,n=3,k=0,l=1,d=0,name='y',order='low',braces=True,log='paren',kind='blank',point='1'),
 'q-48659':dict(level='moderate',b=4,c=1,a=7,n=1,k=0,l=0,d=0,name='y',order='high',braces=True,log='bare',kind='radio',point='1/7'),
 'q-1951':dict(level='easy',b=4,c=1,a=7,n=1,k=0,l=0,d=0,name='f',order='high',braces=True,log='opbare',kind='radio'),
 'q-340970':dict(level='moderate',b=5,c=2,a=-3,n=1,k=0,l=0,d=1,name='y',order='constant',braces=True,log='opparen',kind='blank',point='0'),
 'q-107463':dict(level='hard',b=4,c=1,a=2,n=1,k=0,l=0,d=1,name='y',order='high',braces=True,log='opparen',kind='radio',point='-1',equation=True),
 'e-728':dict(level='easy',b=2,c=3,a=-1,n=1,k=0,l=0,d=1,name='y',order='constant',braces=True,log='opparen',kind='blank',fieldless=True,unrated=True),
}
PARAM_KEYS = ('b','c','a','n','k','l','d','point')


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def uid(value):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy/'+digest(value)))


def tex(expr):
    return sp.latex(sp.sympify(expr)).replace(r'\log',r'\ln')


def scalar(v):
    return tex(sp.Rational(v))


def power_x(n, braces=True):
    return 'x' if n == 1 else (r'{x}^{'+str(n)+'}' if braces else 'x^{'+str(n)+'}')


def polynomial_terms(p, derivative=False, scale=1):
    terms = [(p['n'],p['a']),(2,p['k']),(1,p['l']),(0,p['d'])]
    if derivative:
        terms = [(n-1,c*n) for n,c in terms if n]
    merged = {}
    for n,c in terms:
        merged[n] = merged.get(n,0)+c*scale
    order = sorted(merged,reverse=True)
    if p['order'] == 'constant':
        order = [0]+[n for n in order if n]
    elif p['order'] == 'low':
        order = sorted(merged)
    return [(n,merged[n]) for n in order if merged[n]]


def poly(p, derivative=False, scale=1, substitute=None):
    result = ''
    spaced = p.get('spaced',False)
    for n,c in polynomial_terms(p,derivative,scale):
        neg = c<0
        magnitude = abs(c)
        if n:
            factor = power_x(n,p['braces']) if substitute is None else '('+scalar(substitute)+')'+('^{'+str(n)+'}' if n>1 else '')
            term = ('' if magnitude==1 else scalar(magnitude))+factor
        else:
            term = scalar(magnitude)
        sign = (' - ' if neg else ' + ') if result and spaced else ('-' if neg else '+' if result else '')
        result += sign+term
    return result or '0'


def inner(p):
    return p['a']*X**p['n']+p['k']*X**2+p['l']*X+p['d']


def log(p,style=None):
    s = style or p['log']; b = str(p['b'])
    return {'opparen':r'\operatorname{ln}⁡('+b+')','opbare':r'\operatorname{ln}⁡'+b,'opbareplain':r'\operatorname{ln}'+b,
            'bare':'ln⁡'+b,'paren':'ln⁡('+b+')','slashparen':r'\ln ('+b+')',
            'normal':r'\ln('+b+')'}[s]


def bp(p,exponent):
    return '{'+str(p['b'])+'}^{'+exponent+'}'


def scaled(p,exponent):
    return (str(p['c'])+r'\cdot ' if p['c']!=1 else '')+bp(p,exponent)


def default_params(qid):
    s=SPECS[qid]
    return {k:s[k] for k in PARAM_KEYS if k in s}


def complete(qid,parameters):
    base=default_params(qid)
    if parameters is not None:
        if set(parameters)!=set(base):
            raise ValueError('Explicit parameters require exactly '+str(sorted(base)))
        base=dict(parameters)
    for k,v in base.items():
        if k=='point':
            base[k]=str(sp.Rational(v))
        elif isinstance(v,bool) or not isinstance(v,int):
            raise ValueError(k+' must be an integer')
    s=dict(SPECS[qid]);s.update(base);s['spaced']=qid=='q-48631'
    return s


REJECTIONS = {'sampling': 0, 'bank': 0}


def guard(qid,p):
    src=SPECS[qid]
    if not 2<=p['b']<=6 or not 1<=abs(p['a'])<=9 or not 1<=p['c']<=5:
        raise ValueError('Base/coefficient outside source-scale bounds')
    if p['n']!=src['n'] or p['k']!=0 or abs(p['l'])>3 or abs(p['d'])>5:
        raise ValueError('Degree, term count or arithmetic bounds')
    if (src['l']==0)!=(p['l']==0) or (src['d']==0 and p['d']!=0):
        raise ValueError('Preserve source polynomial term presence')
    if src['d']!=0 and p['d']==0:
        raise ValueError('Preserve shifted exponent')
    variable_scale = qid in ('e-728','q-107461')
    if not variable_scale and ((src['c']==1 and p['c']!=1) or (src['c']>1 and p['c']<2)):
        raise ValueError('Preserve outside scale workload')
    if qid in ('q-1951','q-1952','q-107461') and abs(p['a'])<2:
        raise ValueError('Avoid unit inner derivative colliding with omission')
    if 'point' in p:
        t=sp.Rational(p['point'])
        if qid=='q-48659':
            if abs(p['a'])<2 or t not in (sp.Rational(1,p['a']),-sp.Rational(1,p['a'])):
                raise ValueError('Familiar reciprocal point required')
        elif t not in (-1,0,1):raise ValueError('Familiar integer point required')
        if abs(inner(p).subs(X,t))>2 or sp.diff(inner(p),X).subs(X,t)==0:
            raise ValueError('Nonzero slope and small evaluated exponent required')
        if qid=='q-340969' and abs(p['a'])>3:raise ValueError('Cubic slope coefficient bound')


def sample(qid,rng):
    # Decide the answer-bearing sign and evaluation case before incidental values.
    for _ in range(1000):
        p=default_params(qid)
        sign=rng.choice([-1,1]);p['a']=sign*rng.randint(1 if SPECS[qid]['n']>1 or qid=='e-728' else 2,9)
        p['b']=rng.randint(2,6)
        if qid in ('e-728','q-107461'):p['c']=rng.randint(1,5)
        elif SPECS[qid]['c']!=1:p['c']=rng.randint(2,5)
        if SPECS[qid]['d']!=0:p['d']=rng.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
        if SPECS[qid]['l']!=0:p['l']=rng.choice([-3,-2,-1,1,2,3])
        if qid=='q-48659':p['point']=str(sp.Rational(rng.choice([-1,1]),p['a']))
        elif 'point' in p:
            p['point']=str(rng.choice([-1,0,1]))
            if qid=='q-340969':p['a']=sign*rng.randint(1,3)
            # Pick a small final exponent; a constant is allowed only in sources
            # with an existing constant term.
            if SPECS[qid]['d']!=0:
                t=sp.Rational(p['point']);p['d']=int(rng.choice([-2,-1,0,1,2])-p['a']*t**p['n']-p['l']*t)
        q=complete(qid,p)
        try:guard(qid,q)
        except ValueError:
            REJECTIONS['sampling']+=1;continue
        return p
    raise ValueError('No eligible sample')


def normalized(text):
    text=text.replace('\u2061','').replace(r'\operatorname{ln}',r'\ln')
    text=re.sub(r'(?<![A-Za-z\\])ln',lambda _:r'\ln',text)
    # Critical source juxtaposition: 4x3^u means (4x)*3^u, never a base 43.
    text=re.sub(r'(?<=[0-9x)}])(?=\{?\d+\}?\^)',lambda _:r'\cdot ',text)
    # Original positive ungrouped factors can become signed under explicit inputs.
    text=re.sub(r'(\\cdot\s*)(-\d+(?:x)?)',lambda m:m[1]+'('+m[2]+')',text)
    return text


def source_prompt_solution(qid,p,raw=False):
    src=SOURCES[qid]
    original=all(p[k]==v for k,v in default_params(qid).items())
    if original:
        prompt=src[':question/problem'];solution=src.get(':question/worked-solution','')
        if raw:return prompt,solution
        prompt=normalized(prompt);solution=normalized(solution)
        if qid=='q-1951':solution=solution.replace(r'\text{d}y',r'\text{d}f')
    else:
        function=scaled(p,poly(p))
        if 'point' in p:
            demand='equation of the tangent' if p.get('equation') else 'slope $m$ of the tangent'
            prompt='Find the '+demand+' to the curve $y='+function+'$ at the point where $x='+scalar(p['point'])+'.$'
            if p['kind']=='blank':prompt+='\n\n$m=$\n{{field-1}}'
        else:
            demand=r"${f}^{\prime}(x)$" if p['name']=='f' else r'$\frac{\mathrm{d}y}{\mathrm{d}x}$'
            prompt=('If $f(x)=' if p['name']=='f' else 'Given that $y=')+function+'$, find '+demand+'.'
            if p.get('fragment'):prompt+='\n\n'+demand+'$=$\n{{field-1}}'+r'$\cdot '+bp(p,poly(p))+'$'
        solution=authored_solution(p)
    if p.get('fieldless'):
        prompt+='\n\n'+(r'$f^{\prime}(x)=$' if p['name']=='f' else r'$\frac{\mathrm{d}y}{\mathrm{d}x}=$')+'\n{{field-1}}'
    if not solution:solution=authored_solution(p)
    return prompt,solution


def authored_solution(p):
    """Same composite/derivative/operator/substitution/product/restoration stages."""
    u=inner(p);du=sp.diff(u,X);name=p['name'];lp=log(p,'normal')
    outer=scaled(p,'u');du_tex=poly(p,True)
    coefficient=poly(p,True,p['c'])
    if len(polynomial_terms(p,True,p['c']))>1:coefficient='('+coefficient+')'
    derivative=coefficient+r'\cdot '+bp(p,poly(p))+lp
    formal=r'\frac{\mathrm{d}'+name+r'}{\mathrm{d}x}'
    solution=('First, we express $'+name+'$ as the composite function\n\n$$\n'+name+'='+outer+r',\,u='+poly(p)+'.\n$$\n\nDifferentiating gives\n\n$$\n'+
       r'\frac{\mathrm{d}'+name+r'}{\mathrm{d}u}='+outer+lp+r',\,\frac{\mathrm{d}u}{\mathrm{d}x}='+du_tex+'.\n$$\n\nWe now apply the chain rule and get\n\n$$\n'+
       r'\begin{aligned}'+formal+r' & =\frac{\mathrm{d}'+name+r'}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x} \\ & ='+outer+lp+r'\cdot ('+du_tex+r') \\ & =('+du_tex+r')\cdot '+outer+lp+r' \\ & ='+derivative+r'.\end{aligned}'+'\n$$')
    if 'point' in p:
        t=sp.Rational(p['point']);dv=du.subs(X,t);uv=u.subs(X,t);ans=p['c']*dv*p['b']**uv*sp.log(p['b'])
        sub='('+poly(p,True,p['c'],substitute=t)+r')\cdot '+bp(p,poly(p,substitute=t))+lp
        solution+='\n\nFinally, to find the slope $m$ of the tangent to the curve at $x='+scalar(t)+'$, we have to evaluate $'+formal+'$ at that point as follows:\n\n$$\n'+r'\begin{aligned}m='+formal+r'\big|_{x='+scalar(t)+r'} & ='+sub+r' \\ & ='+scalar(p['c']*dv)+r'\cdot '+bp(p,scalar(uv))+lp+r' \\ & ='+tex(ans)+r'.\end{aligned}'+'\n$$\n\nTherefore, the slope of the tangent to the curve at the point where $x='+scalar(t)+'$ is $'+tex(ans)+'.$'
    if p.get('equation'):
        t=sp.Rational(p['point']);ordinate=p['c']*p['b']**inner(p).subs(X,t)
        slope=p['c']*sp.diff(inner(p),X).subs(X,t)*p['b']**inner(p).subs(X,t)*sp.log(p['b'])
        solution+='\n\nAlso, the $y$-value of the point on the curve where $x='+scalar(t)+'$ is\n\n$$\n'+r'y_1='+scaled(p,scalar(inner(p).subs(X,t)))+'='+tex(ordinate)+'.\n$$'
        solution+='\n\nFinally, we find the equation of the tangent at that point:\n\n$$\n'+r'\begin{aligned}y-y_1&=m(x-x_1) \\ y-('+tex(ordinate)+')&=('+tex(slope)+')'+r'\left(x-('+scalar(t)+r')\right) \\ y&='+tex(sp.expand(slope*(X-t)+ordinate))+r'.\end{aligned}'+'\n$$'
    return normalized(solution)


def target(p):
    v=p['c']*p['b']**inner(p)*sp.log(p['b'])*sp.diff(inner(p),X)
    if p.get('equation'):
        t=sp.Rational(p['point']);return sp.expand(v.subs(X,t)*(X-t)+p['c']*p['b']**inner(p).subs(X,t))
    if 'point' in p:return v.subs(X,sp.Rational(p['point']))
    if p.get('fragment'):return p['c']*sp.diff(inner(p),X)*sp.log(p['b'])
    return v


def historical_bank(qid,p,field_index):
    """Every observed value is a complete expression-pattern recipe.

    q48565 altered exponent / q48631 x^(n+1) patterns and the half coefficient
    in q107461 are opaque historical evidence; never used by normal defaults.
    """
    a=p['a'];b=p['b'];c=p['c'];n=p['n'];d=p['d'];u=inner(p);du=sp.diff(u,X);L=sp.log(b);B=b**u
    q='q-1952' if qid=='q-1951' else qid
    if q=='q-48565':values=[a*b**(a*X)*L,du*B,a*X*B,du*B*L,X*b**(a*X)*L]
    elif q=='q-48631':values=[du*B,du*B*L,(du+d)*B,(du+d)*B*L,(n*a*X**(n+1))*b**(n*a*X)*L]
    elif q=='q-107459':values=[-du*B*L,-c*du*B*L,c*du*B*L,du*B*L,c*X*B*L]
    elif q=='q-107461':values=[-sp.Rational(a,2)*B*L,-a*B*L,-a*b*B*L,a*B*L,a*b*B*L]
    elif q=='q-1952':values=[a*B,u,B,a*L*B,L*B]
    elif q=='q-48659':
        t=sp.Rational(p['point']);z=u.subs(X,t);bv=b**z;values=[z,a*L,c*a*bv*L,bv,bv*L]
    elif q=='q-107463':
        t=sp.Rational(p['point']);ordinate=b**u.subs(X,t);m=sp.expand_log(a*ordinate*L,force=True)
        # Repaired source bank at basis 6468; the original defective bank is
        # archived outside the runtime package as a negative regression fixture.
        values=[sp.expand(scale*m*(X-t)+ordinate) for scale in [1,2,-1,-2,sp.Rational(1,2)]]
    elif q=='q-340969':values=[target(p),target(p)]
    else:values=[target(p)]
    # Source-order shape masks are stored as component renderings, not answer strings.
    if q=='q-48565':
        lx=log(p,'slashparen');pi=str(b)+'^{'+str(a)+'x}';pi2=str(b)+'^{'+str(a)+'x^{2}}'
        first=[str(a)+r' \cdot '+pi+r'\ln ('+str(b)+')',poly(p,True)+pi2,str(a)+'x'+pi2,poly(p,True)+pi2+lx,'x'+pi+lx]
        if field_index==0:strings=first
        else:
            # Fresh migrated legacy bank order is correct, altered exponent, no ln,
            # omitted power multiplier, exponent treated linearly.
            strings=[poly(p,True)+bp(p,poly(p))+log(p),'x'+bp(p,str(a)+'x')+log(p),poly(p,True)+bp(p,poly(p)),str(a)+'x'+bp(p,poly(p)),str(a)+r'\cdot '+bp(p,str(a)+'x')+log(p)]
            values=[values[3],values[4],values[1],values[2],values[0]]
    elif q=='q-48631':
        powstr=str(b)+'^{'+poly(p)+'}';dt=poly(p,True);dtplus=poly({**p,'d':0,'l':d},True) # overwritten below using du+d
        dtplus=dt+(' + ' if d>0 else ' - ')+str(abs(d))
        strings=['('+dt+')'+powstr,'('+dt+')'+powstr+log(p),'('+dtplus+')'+powstr,'('+dtplus+')'+powstr+log(p),'('+str(n*a)+'x^{'+str(n+1)+'})'+str(b)+'^{'+str(n*a)+'x}'+log(p)]
    elif q=='q-107459':
        coeffs=[-du,-c*du,c*du,du,c*X]
        strings=[tex(v).replace(' x','x').replace('- ','-')+r'\cdot '+bp(p,poly(p))+log(p) for v in coeffs]
    elif q=='q-107461':strings=[scalar(v)+r'\cdot '+bp(p,poly(p))+log(p) for v in [-sp.Rational(a,2),-a,-a*b,a,a*b]]
    elif q=='q-1952':strings=[str(a)+r'\cdot '+bp(p,poly(p)),poly(p),bp(p,poly(p)),str(a)+log(p)+r'\cdot '+bp(p,poly(p)),log(p)+r'\cdot '+bp(p,poly(p))]
    elif q=='q-48659':strings=[scalar(z),str(a)+log(p,'paren'),scalar(a*bv)+log(p,'paren'),scalar(bv),scalar(bv)+log(p,'paren')]
    elif q=='q-312462':strings=[poly(p,True)+r'\operatorname{ln}('+str(b)+')']
    elif q=='q-340969':strings=[tex(v) for v in values]
    elif q=='q-107463':strings=['y='+tex(v) for v in values]
    else:strings=[tex(target(p))]
    return list(zip(strings,values,strict=True))


def tangent_coefficients(p):
    """Every bank slope can be the tangent of a supported alternate curve.

    Fix the base, point and evaluated exponent. Changing the linear coefficient
    while compensating its constant keeps the ordinate and changes the slope.
    The ordinary sampler uses |a|>=2; explicit unit-coefficient controls retain
    their existing supported domain without introducing never-keyed distractors.
    """
    t=sp.Rational(p['point']); evaluated=inner(p).subs(X,t)
    minimum=1 if abs(p['a'])==1 else 2
    eligible=[]
    for coefficient in range(-9,10):
        if abs(coefficient)<minimum:continue
        alternate={**p,'a':coefficient,'d':int(evaluated-coefficient*t)}
        try:guard('q-107463',alternate)
        except ValueError:continue
        eligible.append(coefficient)
    return eligible


def tangent_bank(p):
    """Uniform complete-bank sampling; no slope/sign/intercept role is the key.

    At a fixed base, point and ordinate, every eligible coefficient is equally
    sampled by the existing parameter sampler. Each five-member bank containing
    that coefficient has the same probability. Thus any of its five members can
    be the key for another supported target, without changing the bank.
    """
    rng=random.Random(p['_bank_seed']); eligible=tangent_coefficients(p)
    coefficients=sorted([p['a'],*rng.sample([a for a in eligible if a!=p['a']],4)])
    t=sp.Rational(p['point']); ordinate=p['c']*p['b']**inner(p).subs(X,t)
    values=[sp.expand_log(sp.expand(a*ordinate*sp.log(p['b'])*(X-t)+ordinate),force=True)
            for a in coefficients]
    p['_bank_role']='uniform-supported-tangent-slopes'
    return [('y='+tex(value),value,'correct' if a==p['a'] else 'incorrect-inner-derivative-coefficient')
            for a,value in zip(coefficients,values)]


def method_bank(p):
    """Complete coefficient bank, grounded in source q-107459's shared factors.

    Distractor numerators have the same decimal width and a source-grounded
    two-pair/one-singleton sign structure. The correct magnitude can occupy any
    role. Choose that role before filling compatible distractor numerators.
    """
    if p['kind']=='blank':return [(tex(target(p)),target(p),'correct')]
    if p.get('equation'):
        return tangent_bank(p)
    rng=random.Random(p['_bank_seed'])
    n=p['n'];u=inner(p);b=p['b'];c=p['c'];L=sp.log(b)
    coefficient=sp.Integer(c*n*p['a'])
    common=X**(n-1)*b**u*L
    if 'point' in p:
        t=sp.Rational(p['point']);coefficient*=b**u.subs(X,t);common=L
    coefficient=sp.Rational(coefficient)
    sign=-1 if coefficient<0 else 1
    magnitude=abs(coefficient.p);denominator=coefficient.q
    width=len(str(magnitude));lo=1 if width==1 else 10**(width-1);hi=10**width-1
    # q-107459 supplies two opposite-sign pairs and a singleton. None of
    # those roles is mathematically privileged: choose the correct magnitude's
    # role first, then fill the other roles. A sign-only or singleton-only action
    # cannot consistently solve this bank.
    role=rng.randrange(3);p['_bank_role']=('pair-1','pair-2','singleton')[role]
    others=rng.sample([v for v in range(lo,hi+1) if v!=magnitude],2)
    magnitudes=others[:];magnitudes.insert(role,magnitude)
    signed=[]
    for i,numerator in enumerate(magnitudes):
        signs=(-1,1) if i<2 else (sign if i==role else rng.choice([-1,1]),)
        signed.extend((sg,numerator) for sg in signs)
    # Common denominator and numeral width avoid typography revealing a key.
    suffix=(r'\cdot '+tex(X**(n-1)*b**u)+r'\ln('+str(b)+')') if 'point' not in p else r'\ln('+str(b)+')'
    bank=[]
    for candidate_sign,numerator in signed:
        scalar=(('-' if candidate_sign<0 else '')+str(numerator)) if denominator==1 else (('-' if candidate_sign<0 else '')+r'\frac{'+str(numerator)+'}{'+str(denominator)+'}')
        value=sp.Rational(candidate_sign*numerator,denominator)*common
        correct=numerator==magnitude and candidate_sign==sign
        bank.append((scalar+suffix,value,'correct' if correct else 'coefficient-sign-or-arithmetic-slip'))
    return bank


def validate_bank(bank,correct):
    vals=[v for _,v,*_ in bank]
    if len(vals)>1:
        for i,a in enumerate(vals):
            for b in vals[:i]:
                if sp.simplify(a-b)==0:raise ValueError('Whole bank rejected: equivalent options')
    if sum(sp.simplify(v-correct)==0 for v in vals)!=1:
        raise ValueError('Whole bank rejected: correct value missing or ambiguous')


def original_bank(qid,p,field):
    """Map every immutable source option to a complete mathematical recipe.

    Source-order maps are explicit because duplicate migrated fields changed order.
    Historical bank routines retain their parameterized recipes; no string guessing.
    """
    a=p['a'];b=p['b'];c=p['c'];u=inner(p);du=sp.diff(u,X);B=b**u;L=sp.log(b)
    maps={
      'q-48565': [a*b**(a*X)*L,X*b**(a*X)*L,du*B*L,du*B,a*X*B],
      'q-48631': [2*a*X**3*b**(2*a*X)*L,du*B,du*B*L,(du+p['d'])*B,(du+p['d'])*B*L],
      'q-107459': [-du*B*L,-c*du*B*L,c*du*B*L,du*B*L,c*X*B*L],
      'q-107461': [-a*B*L/2,-a*B*L,-a*b*B*L,a*B*L,a*b*B*L],
      'q-1952': [a*B,u,B,a*L*B,L*B],
      'q-1951': [a*B,u,L*B,B,a*L*B],
      'q-48659': [sp.Integer(1),a*L,a*b*L,sp.Integer(b),b*L],
    }
    if qid=='q-48565' and field is SOURCES[qid][':question/answer-fields'][1]:
        vals=[X*b**(a*X)*L,a*b**(a*X)*L,du*B,a*X*B,du*B*L]
    elif qid=='q-107463':vals=[v for _,v in historical_bank(qid,p,0)]
    elif qid in maps:vals=maps[qid]
    else:vals=[target(p)]*len(field[':answer-field/choices'])
    assert len(vals)==len(field[':answer-field/choices'])
    return [(v[':answer/value'],math,'source-pattern-'+str(i)) for i,(v,math) in enumerate(zip(field[':answer-field/choices'],vals,strict=True))]


def build(qid,p,seed,profile):
    raw=False;legacy=profile.startswith('historical:')
    source=SOURCES.get(qid);level=p['level']
    prompt,solution=source_prompt_solution(qid,p)
    field_sources=[None]
    fields=[];semantic=[]
    for i,sf in enumerate(field_sources):
        if raw or legacy:
            # Normal historical profile uses the authoritative recent field for q48565.
            actual_i=1 if qid=='q-48565' else 0
            bank=[(s,v,'observed-pattern-'+str(j)) for j,(s,v) in enumerate(historical_bank(qid,p,actual_i))]
        else:bank=method_bank(p)
        if legacy and all(p[k]==v for k,v in default_params(qid).items()) and source.get(':question/answer-fields'):
            sf0=source[':question/answer-fields'][0]
            bank=original_bank(qid,p,sf0)
        bank=[(normalize_tex(normalized(s)),v,r) for s,v,r in bank]
        if p['kind']=='blank':
            assert all(sp.simplify(v-target(p))==0 for _,v,_ in bank)
        else:validate_bank(bank,target(p))
        typ=sf[':answer-field/type'][':db/ident'] if sf else ':answer-field.type/'+p['kind']
        key=sf[':answer-field/key'] if sf else ('selection' if p['kind']=='radio' else 'field-1')
        has_correct=not raw or ':answer-field/correct' in sf
        fields.append({'key':key,'type':typ,'bank':bank,'has_correct':has_correct})
        semantic.append([key,typ,has_correct,sorted(s for s,_,_ in bank)])
    params={k:p[k] for k in PARAM_KEYS if k in p}
    # The assessed derivative ignores vertical shift inside exponent only when it
    # cancels at evaluation? It still affects the derivative, so fingerprint the
    # actual requested mathematical object, plus the point for a slope demand.
    prompt=normalize_prose(normalized(prompt));solution=normalize_prose(normalized(solution))
    demand=('tangent-equation' if p.get('equation') else 'slope' if 'point' in p else 'coefficient-fragment' if p.get('fragment') else 'derivative')
    if demand=='coefficient-fragment':
        assessed=sp.expand_log(target(p),force=True)
    else:
        # Normalize the only perfect-power general base in 2..6 (4=2^2), and
        # factor constant exponent offsets. This merges genuinely equivalent
        # derivative tasks across base/scale/offset parameter spellings.
        base,exponent,log_factor=p['b'],inner(p),sp.log(p['b'])
        if base==4:base,exponent,log_factor=2,2*exponent,2*sp.log(2)
        assessed=sp.expand(sp.expand_power_exp(p['c']*sp.diff(inner(p),X)*base**exponent*log_factor),log=False)
    fingerprint=digest({'criterion':demand,'derivative':sp.srepr(assessed),'point':p.get('point')})
    content=[VERSION,level if not(raw and p.get('unrated')) else None,prompt,solution if not(raw and ':question/worked-solution' not in source) else None,semantic]
    identity=uid(content);rendered_fields=[];answer_math={};recipes={}
    for i,f in enumerate(fields):
        fid=uid([identity,'field',i,f['key']]);answers=[];correct=None
        for s,v,r in f['bank']:
            aid=uid([fid,s]);answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':s})
            answer_math[aid]=str(v);recipes[aid]=r
            if correct is None and sp.simplify(v-target(p))==0:correct=aid
        if f['type'].endswith('/radio'):random.Random(seed+i*104729).shuffle(answers)
        rf={':answer-field/id':fid,':answer-field/key':f['key'],':answer-field/type':f['type'],':answer-field/choices':answers}
        if f['has_correct']:rf[':answer-field/correct']=[':answer/id',correct]
        rendered_fields.append(rf)
    question={':question/id':identity,':question/problem':prompt}
    if not(raw and ':question/worked-solution' not in source):question[':question/worked-solution']=solution
    if not(raw and ':question/difficulty' not in source):question[':question/difficulty']=':question.difficulty/'+level
    if not(raw and ':question/answer-fields' not in source):question[':question/answer-fields']=rendered_fields
    repairs=[]
    if not raw and source:
        repairs=['normalize natural-log spelling and invisible function-apply characters','make numeric-base multiplication explicit']
        if p.get('fieldless'):repairs.append('authored supported full-derivative blank with matching placeholder')
        if p.get('unrated'):
            repairs.append('authored easy difficulty')
            if not source.get(':question/worked-solution'):repairs+=['independently inferred correct designation','authored completion of missing worked solution']
        if qid=='q-48565':repairs.append('one authoritative radio widget replaces duplicate legacy fields')
    return {'knowledge_point':KP.copy(),'question':question,'generation':{'version':VERSION,'template':qid,'profile':profile,'parameters':params,
            'seed':seed,'bank_seed':p['_bank_seed'],'bank_role':p.get('_bank_role'),'source':{**{k:CAPTURE[k] for k in ('database','basis','lineage')},'basis':CAPTURE.get('source_updates',{}).get(qid,{}).get('basis',CAPTURE['basis'])},'source_ids':[qid] if source else [],
            'difficulty_design':'observed' if source and not p.get('unrated') else 'authored',
            'answer_shape':'coefficient-fragment' if p.get('fragment') else demand,
            'evidence_only':raw or legacy,'eligible_for_learning':not(raw or legacy),
            'presentation_and_completion_repairs':repairs,
            'mathematical_fingerprint':fingerprint,'answer_math':answer_math,'recipes':recipes,
            'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'plot_rating':'none'}}


@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
    rng=random.Random(seed)
    if profile and profile.startswith('historical:'):
        qid=profile.split(':',1)[1]
        if template is not None and template!=qid:raise ValueError('Profile/template mismatch')
        template=qid
    eligible=[q for q,s in SPECS.items() if s['level']==level and (field_type is None or s['kind']==field_type)]
    qid=template or rng.choice(eligible)
    if qid not in eligible:raise ValueError('Template/level/field type mismatch')
    if profile is None:profile='method:'+qid
    if profile not in ('method:'+qid,'historical:'+qid):raise ValueError('Unknown complete profile')
    if qid not in SOURCES and not profile.startswith('method:'):raise ValueError('Authored template has no historical profile')
    for _ in range(1000 if parameters is None else 1):
        # Bank-role RNG is fixed before parameter sampling, independent of values.
        bank_seed=rng.randrange(2**63)
        p=complete(qid,sample(qid,rng) if parameters is None else parameters);p['_bank_seed']=bank_seed;guard(qid,p)
        try:return build(qid,p,seed,profile)
        except ValueError:
            REJECTIONS['bank']+=1
            if parameters is not None:raise
    raise ValueError('Whole-bank eligible sampling exhausted')


# EASY: observed derivative families, including completed fieldless captures and
# supplied-exponential coefficient fragment. Bases 2..6, powers 1/2/3, a<=9.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)


# MODERATE: source slope families, familiar points and small evaluated exponents.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)


# HARD: source tangent equation from a linear exponent and a familiar point.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)


def markdown(record):
    q=record['question'];rows=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        if f[':answer-field/type'].endswith('/radio'):
            rows.extend(letter+'. $'+a[':answer/value']+'$' for letter,a in zip('ABCDE',f[':answer-field/choices']))
    rows+=['\nWorked solution',q.get(':question/worked-solution','[absent in raw capture]')]
    return '\n\n'.join(rows)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard'],default='easy')
    parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--format',choices=['markdown','json'],default='json')
    parser.add_argument('--template');parser.add_argument('--profile')
    args=parser.parse_args()
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    if args.count<1:parser.error('--count must be positive')
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
