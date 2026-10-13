#!/usr/bin/env python3
"""General-base exponential chain rule, frozen math basis 1356.

No EDB access or writes. Public observed:<qid> profiles preserve captured attribute
presence, both legacy fields and opaque complete historical banks; they are
evidence-only. Normal method profiles use the source family and operative stages,
one supported field, normalized ln notation and unambiguous multiplication.
Easy = derivative; moderate = derivative then familiar point evaluation; authored
hard = the same slope demand with three nonconstant exponent terms and an outside
scale. This is extra chain-rule bookkeeping, never a new mathematical branch.
Source q-312462 is a coefficient FRAGMENT blank, not a full derivative blank.

Historical banks below are explicit parameterized expression patterns, not claims
to know the original author's distractor intent. The masks replace COMPLETE
components simultaneously, so replacing 2 cannot corrupt a base, prose or exponent.
All numerical sampling and explicit inputs share the same workload guards.
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

ROOT = Path(__file__).with_suffix('')
CAPTURE = json.loads((ROOT/'source.json').read_text())
RECORD = CAPTURE['record']
SOURCES = {q[':question/math-academy-id']: q for q in RECORD[':knowledge-point/questions']}
X = sp.Symbol('x', real=True)
U = sp.Symbol('u', real=True)
VERSION = 'general-exponential-chain-1'
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
 'authored-three-term-slope':dict(level='hard',b=3,c=2,a=1,n=3,k=-1,l=2,d=-2,name='y',order='low',braces=True,log='normal',kind='blank',point='1',authored=True),
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


def guard(qid,p):
    s=SPECS[qid];level=s['level']
    if p['b'] not in range(2,7) or not 1<=p['c']<=5 or not 1<=abs(p['a'])<=9:
        raise ValueError('base 2..6; outside scale 1..5; nonzero exponent coefficient magnitude 1..9')
    if p['n']!=s['n'] or not -5<=p['d']<=5 or not -3<=p['l']<=3 or not -3<=p['k']<=3:
        raise ValueError('Exponent family or coefficient bound violated')
    if qid!='authored-three-term-slope' and p['k']!=0:
        raise ValueError('Observed family has no quadratic middle term')
    if qid not in ('q-71881','q-340969','authored-three-term-slope') and p['l']!=0:
        raise ValueError('This family has no separate linear term')
    if s['c']==1 and p['c']!=1:
        raise ValueError('This source family has no outside scale')
    if qid in ('q-48565','q-1952') and p['d']!=0:
        raise ValueError('This source family has no constant term')
    if qid=='q-71881' and (not p['l'] or p['d']!=0):
        raise ValueError('Two nonconstant terms are required')
    if qid=='q-107461' and (p['a']>=0 or p['d']!=1):
        raise ValueError('Retain the decreasing linear exponent with constant 1')
    if qid=='q-107458' and (p['a']>=0 or p['d']<1):
        raise ValueError('Retain a positive constant minus a cubic')
    if qid in ('q-107459','q-48631') and p['d']==0:
        raise ValueError('Retain the shifted quadratic family')
    if level=='moderate':
        t=sp.Rational(p['point'])
        if p['c']!=1:
            raise ValueError('Moderate observed families have unit outside scale')
        if qid=='q-48659':
            if not 2<=p['a']<=9 or p['d']!=0 or t!=sp.Rational(1,p['a']):
                raise ValueError('Linear slope uses the familiar point 1/a')
        elif abs(p['a'])>3 or not p['l'] or t not in (-1,1) or abs(inner(p).subs(X,t))>2:
            raise ValueError('Moderate cubic/linear slope: a,l nonzero magnitude <=3, point +/-1, familiar exponent magnitude <=2')
    if level=='hard':
        t=sp.Rational(p['point'])
        if not 2<=p['c']<=4 or not all(1<=abs(p[k])<=3 for k in ('a','k','l')) or t not in (-1,1) or inner(p).subs(X,t) not in (-1,0,1,2):
            raise ValueError('Authored hard needs outside 2..4 and three nonzero terms magnitude <=3; point +/-1; exponent -1..2')
    if 'point' in p and sp.diff(inner(p),X).subs(X,sp.Rational(p['point']))==0:
        raise ValueError('Avoid a zero-slope collapse')


def sample(qid,rng):
    for _ in range(1000):
        p=default_params(qid);p['b']=rng.randint(2,6)
        p['a']=rng.randint(1,9)*( -1 if SPECS[qid]['a']<0 else 1)
        if SPECS[qid]['c']!=1:p['c']=rng.randint(2,5)
        if qid in ('q-107459','q-48631'):p['d']=rng.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
        if qid=='q-107458':p['d']=rng.randint(1,5)
        if qid=='q-312462':p['d']=rng.randint(-5,5)
        if qid=='q-71881':p['l']=rng.choice([-3,-2,-1,1,2,3])
        if qid=='q-48659':p['a']=rng.randint(2,9);p['point']=str(sp.Rational(1,p['a']))
        if qid=='q-340969':
            p['a']=rng.choice([-3,-2,-1,1,2,3]);p['l']=rng.choice([-3,-2,-1,1,2,3]);p['point']=str(rng.choice([-1,1]));p['d']=rng.randint(-2,2)
        if qid=='authored-three-term-slope':
            p['c']=rng.randint(2,4)
            for k in ('a','k','l'):p[k]=rng.choice([-3,-2,-1,1,2,3])
            p['point']=str(rng.choice([-1,1])); t=sp.Rational(p['point']);p['d']=int(rng.choice([-1,0,1,2])-(p['a']*t**3+p['k']*t**2+p['l']*t))
        q=complete(qid,p)
        try:guard(qid,q)
        except ValueError:continue
        return p
    raise ValueError('No eligible sample')


def apply_slots(text,replacements):
    """Simultaneous longest complete-component masking; never recursive replace."""
    if not replacements:return text
    pat=re.compile('|'.join(re.escape(k) for k in sorted(replacements,key=len,reverse=True)))
    return pat.sub(lambda m:replacements[m.group()],text)


def source_slots(qid,p):
    old=complete(qid,None)
    def components(v):
        return {'inner':poly(v),'du':poly(v,True),'cdu':poly(v,True,v['c']),
                'scaled-inner':scaled(v,poly(v)),'scaled-u':scaled(v,'u'),
                'power-inner':bp(v,poly(v)),'power-u':bp(v,'u'),'log':log(v)}
    a=components(old);b=components(p)
    repl={a[k]:b[k] for k in a}
    # Captured q48631 alone spells the base without braces.
    if qid=='q-48631':
        repl['3^{6x^{2} - 4}']=str(p['b'])+'^{'+poly(p)+'}'
    if qid=='q-107459':
        repl.update({'6x':poly(p,True,p['c']),'3x':str(p['c'])+'x'})
    if qid=='q-48659':
        t=sp.Rational(p['point']);aa=p['a'];bb=p['b']; lp=log(p,'paren')
        repl.update({r'7ln⁡(4)\cdot {4}^{7(1/7)}':str(aa)+lp+r'\cdot '+bp(p,str(aa)+'('+str(t)+')'),
                     r'7ln⁡(4)\cdot 4':str(aa)+lp+r'\cdot '+str(bb),
                     '28ln⁡(4)':str(aa*bb)+lp,
                     'ln⁡(4)':lp, r'\frac{1}{7}':scalar(t),'x=1/7':'x='+str(t),
                     '7':str(aa)})
    if qid=='q-340969':
        t=sp.Rational(p['point']);u=inner(p);du=sp.diff(u,X);dv=du.subs(X,t);uv=u.subs(X,t)
        lp=log(p); answer=tex(p['c']*dv*p['b']**uv)+lp
        exp_sub=poly(p,substitute=t)
        # The original evaluates the linear component before displaying the cubic.
        linear_component=('' if abs(p['l'])==1 else scalar(abs(p['l'])))+'('+scalar(t)+')'
        linear_value=scalar(abs(p['l'])*t)
        if abs(p['l'])*t<0:linear_value='('+linear_value+')'
        exp_sub=exp_sub.replace(linear_component,linear_value,1)
        repl.update({'(1-3(1)^{2}){5}^{1-(1)^{3}}ln⁡(5)':'('+poly(p,True,substitute=t)+')'+bp(p,exp_sub)+lp,
                     '-2\\cdot {5}^{0}ln⁡(5)':scalar(dv)+r'\cdot '+bp(p,scalar(uv))+lp,
                     '-2ln⁡(5)':answer,'x=1':'x='+scalar(t)})
    return repl


def normalized(text):
    text=text.replace('\u2061','').replace(r'\operatorname{ln}',r'\ln')
    text=re.sub(r'(?<![A-Za-z\\])ln',lambda _:r'\ln',text)
    # Critical source juxtaposition: 4x3^u means (4x)*3^u, never a base 43.
    text=re.sub(r'(?<=[0-9x)}])(?=\{?\d+\}?\^)',lambda _:r'\cdot ',text)
    return text


def source_prompt_solution(qid,p,raw=False):
    src=SOURCES[qid];repl=source_slots(qid,p)
    prompt=apply_slots(src[':question/problem'],repl)
    solution=apply_slots(src.get(':question/worked-solution',''),repl)
    if not raw:
        prompt,solution=normalized(prompt),normalized(solution)
        if SPECS[qid].get('fieldless'):
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
    return normalized(solution)


def target(p):
    v=p['c']*p['b']**inner(p)*sp.log(p['b'])*sp.diff(inner(p),X)
    if 'point' in p:return sp.expand(v.subs(X,sp.Rational(p['point'])))
    if p.get('fragment'):return p['c']*sp.diff(inner(p),X)*sp.log(p['b'])
    return v


def historical_bank(qid,p,field_index):
    """Every observed value is a complete expression-pattern recipe.

    q48565 altered exponent / q48631 x^(n+1) patterns and the half coefficient
    in q107461 are opaque historical evidence; never used by normal defaults.
    """
    a=p['a'];b=p['b'];c=p['c'];n=p['n'];d=p['d'];u=inner(p);du=sp.diff(u,X);L=sp.log(b);B=b**u
    q=qid
    if q=='q-48565':values=[a*b**(a*X)*L,du*B,a*X*B,du*B*L,X*b**(a*X)*L]
    elif q=='q-48631':values=[du*B,du*B*L,(du+d)*B,(du+d)*B*L,(n*a*X**(n+1))*b**(n*a*X)*L]
    elif q=='q-107459':values=[-du*B*L,-c*du*B*L,c*du*B*L,du*B*L,c*X*B*L]
    elif q=='q-107461':values=[-sp.Rational(a,2)*B*L,-a*B*L,-a*b*B*L,a*B*L,a*b*B*L]
    elif q=='q-1952':values=[a*B,u,B,a*L*B,L*B]
    elif q=='q-48659':
        t=sp.Rational(p['point']);z=u.subs(X,t);bv=b**z;values=[z,a*L,c*a*bv*L,bv,bv*L]
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
    elif q=='q-340969':strings=[tex(p['c']*du.subs(X,sp.Rational(p['point']))*b**u.subs(X,sp.Rational(p['point'])))+r'\operatorname{ln}('+str(b)+')']
    else:strings=[tex(target(p))]
    return list(zip(strings,values,strict=True))


def method_bank(p):
    """Whole authored bank from actual chain rule operations; no unrelated shifts."""
    if p['kind']=='blank':return [(tex(target(p)),target(p),'correct')]
    u=inner(p);du=sp.diff(u,X);c=p['c'];b=p['b'];L=sp.log(b)
    values=[c*du*b**u*L,c*du*b**u,c*b**u*L,-c*du*b**u*L,c*du*u*b**(u-1)]
    recipes=['correct','omit-natural-log','omit-inner-derivative','reverse-inner-sign','use-power-rule-on-base-power']
    if 'point' in p:
        t=sp.Rational(p['point']);values=[sp.expand(v.subs(X,t)) for v in values]
    return [(tex(v),v,r) for v,r in zip(values,recipes,strict=True)]


def validate_bank(bank,correct):
    vals=[v for _,v,*_ in bank]
    if len(vals)>1:
        for i,a in enumerate(vals):
            for b in vals[:i]:
                if sp.simplify(a-b)==0:raise ValueError('Whole bank rejected: equivalent options')
    if sum(sp.simplify(v-correct)==0 for v in vals)!=1:
        raise ValueError('Whole bank rejected: correct value missing or ambiguous')


def build(qid,p,seed,profile):
    raw=profile.startswith('observed:');legacy=profile.startswith('historical:')
    source=SOURCES.get(qid);level=p['level']
    if qid=='authored-three-term-slope':
        prompt='Find the slope $m$ of the tangent to the curve $y='+scaled(p,poly(p))+'$ at the point where $x='+scalar(p['point'])+'.$\n\n$m=$\n{{field-1}}'
        prompt=normalized(prompt);solution=authored_solution(p)
    else:prompt,solution=source_prompt_solution(qid,p,raw)
    if raw:field_sources=source.get(':question/answer-fields',[])
    else:field_sources=[None]
    fields=[];semantic=[]
    for i,sf in enumerate(field_sources):
        if raw or legacy:
            # Normal historical profile uses the authoritative recent field for q48565.
            actual_i=i if raw else (1 if qid=='q-48565' else 0)
            bank=[(s,v,'observed-pattern-'+str(j)) for j,(s,v) in enumerate(historical_bank(qid,p,actual_i))]
        else:bank=method_bank(p)
        if not raw:bank=[(normalized(s),v,r) for s,v,r in bank]
        validate_bank(bank,target(p))
        typ=sf[':answer-field/type'][':db/ident'] if sf else ':answer-field.type/'+p['kind']
        key=sf[':answer-field/key'] if sf else ('selection' if p['kind']=='radio' else 'field-1')
        has_correct=not raw or ':answer-field/correct' in sf
        fields.append({'key':key,'type':typ,'bank':bank,'has_correct':has_correct})
        semantic.append([key,typ,has_correct,sorted(s for s,_,_ in bank)])
    params={k:p[k] for k in PARAM_KEYS if k in p}
    # The assessed derivative ignores vertical shift inside exponent only when it
    # cancels at evaluation? It still affects the derivative, so fingerprint the
    # actual requested mathematical object, plus the point for a slope demand.
    demand=('slope' if 'point' in p else 'coefficient-fragment' if p.get('fragment') else 'derivative')
    assessed=target(p) if demand=='coefficient-fragment' else p['c']*sp.diff(inner(p),X)*p['b']**inner(p)*sp.log(p['b'])
    fingerprint=digest({'criterion':demand,'derivative':sp.srepr(assessed),'point':p.get('point')})
    content=[VERSION,level if not(raw and p.get('unrated')) else None,prompt,solution if not(raw and ':question/worked-solution' not in source) else None,semantic]
    identity=uid(content);rendered_fields=[];answer_math={};recipes={}
    for i,f in enumerate(fields):
        fid=uid([identity,'field',i,f['key']]);answers=[];correct=None
        for s,v,r in f['bank']:
            aid=uid([fid,s]);answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':s})
            answer_math[aid]=str(v);recipes[aid]=r
            if sp.simplify(v-target(p))==0:correct=aid
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
        if p.get('unrated'):repairs+=['authored easy difficulty','independently inferred correct designation','authored completion of missing worked solution']
        if qid=='q-48565':repairs.append('one authoritative radio widget replaces duplicate legacy fields')
    return {'knowledge_point':KP.copy(),'question':question,'generation':{'version':VERSION,'template':qid,'profile':profile,'parameters':params,
            'seed':seed,'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'source_ids':[qid] if source else [],
            'difficulty_design':'observed' if source and not p.get('unrated') else 'authored',
            'answer_shape':'coefficient-fragment' if p.get('fragment') else demand,
            'evidence_only':raw or legacy,'eligible_for_learning':not(raw or legacy),
            'presentation_and_completion_repairs':repairs,
            'mathematical_fingerprint':fingerprint,'answer_math':answer_math,'recipes':recipes,
            'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'plot_rating':'none'}}


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
    rng=random.Random(seed)
    if profile and (profile.startswith('observed:') or profile.startswith('historical:')):
        qid=profile.split(':',1)[1]
        if template is not None and template!=qid:raise ValueError('Profile/template mismatch')
        template=qid
    eligible=[q for q,s in SPECS.items() if s['level']==level and (field_type is None or s['kind']==field_type)]
    qid=template or rng.choice(eligible)
    if qid not in eligible:raise ValueError('Template/level/field type mismatch')
    if profile is None:profile='method:'+qid
    if profile not in ('method:'+qid,'observed:'+qid,'historical:'+qid):raise ValueError('Unknown complete profile')
    if qid not in SOURCES and not profile.startswith('method:'):raise ValueError('Authored template has no historical profile')
    for _ in range(1000 if parameters is None else 1):
        p=complete(qid,sample(qid,rng) if parameters is None else parameters);guard(qid,p)
        try:return build(qid,p,seed,profile)
        except ValueError:
            if parameters is not None:raise
    raise ValueError('Whole-bank eligible sampling exhausted')


# EASY: observed derivative families, including completed fieldless captures and
# supplied-exponential coefficient fragment. Bases 2..6, powers 1/2/3, a<=9.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)


# MODERATE: observed tangent slope evaluation, unit outer coefficient; reciprocal
# linear point 1/a or two-term cubic/linear exponent at +/-1, |u(point)|<=2.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)


# HARD (authored): slope evaluation after three nonconstant inner derivatives and
# nonunit outside coefficient. All |a,k,l|<=3, c=2..4, point +/-1, u(point)=-1..2.
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
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all')
    parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--format',choices=['markdown','json'],default='markdown')
    parser.add_argument('--template');parser.add_argument('--profile')
    args=parser.parse_args()
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
