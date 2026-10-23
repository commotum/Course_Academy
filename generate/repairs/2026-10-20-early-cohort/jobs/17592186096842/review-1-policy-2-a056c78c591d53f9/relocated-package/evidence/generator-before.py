#!/usr/bin/env python3
"""Exact radical-chain generator; local review only, no database operations.

Seventeen captured questions, original scaffolds and full source banks retained
for explicit replay. Normal samples use declared whole banks. See
instructional-account.md for authored repairs, variation and limitations.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid, re
from pathlib import Path
import sympy as sp
from math_format import normalize_prose, normalize_tex, checked_math_content
KP_ID=17592186096842
KP_UUID='2f0cdac9-57b2-5634-8d98-d6adf8a85204'
TITLE='Differentiating a Radical Function Using the Chain Rule'
VERSION='radical-chain-3'
ROOT=Path(__file__).resolve().parent/'data'
X=sp.Symbol('x', real=True)
U=sp.Symbol('u', positive=True)
D=r'\frac{\text{d}y}{\text{d}x}'
DU=r'\frac{\text{d}y}{\text{d}u}'
UX=r'\frac{\text{d}u}{\text{d}x}'
SOURCE={'database':'math','basis':3951,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
# Each layout is independent, never an ordered progression within a level.
TEMPLATES={
 'reciprocal_radio':dict(level='moderate',field='radio',family='reciprocal',degree=1,source='q-48730',style='linear'),
 'sqrt_spaced_radio':dict(level='moderate',field='radio',family='sqrt',degree=1,source='q-48846',style='spaced',repair=True),
 'sqrt_constfirst_radio':dict(level='moderate',field='radio',family='sqrt',degree=1,source='q-107291',style='constfirst'),
 'slope_sqrt_radio':dict(level='easy',field='radio',family='sqrt',degree=1,source='q-107360',style='constfirst',slope=True),
 'reciprocal_blank':dict(level='moderate',field='blank',family='reciprocal',degree=1,source='q-342764',style='linear'),
 'reciprocal_blank_braced':dict(level='moderate',field='blank',family='reciprocal',degree=1,source='q-314194',style='linear',braced=True),
 'sqrt_quadratic_blank':dict(level='hard',field='blank',family='sqrt',degree=2,source='q-342680',style='quadratic'),
 'sqrt_linear_blank':dict(level='hard',field='blank',family='sqrt',degree=1,source='q-342683',style='linear'),
 'slope_reciprocal_blank':dict(level='easy',field='blank',family='reciprocal',degree=2,source='q-342802',style='quadratic',slope=True),
}
PROFILES={
 'source_reciprocal':('reciprocal_radio','observed empirical; coefficient -3 unresolved'),
 'source_spaced':('sqrt_spaced_radio','observed operation shapes'),
 'source_constfirst':('sqrt_constfirst_radio','observed operation shapes'),
 'source_slope':('slope_sqrt_radio','observed empirical; wrong scalar intent unresolved'),
 'authored_operations':(None,'authored full four-error bank'),
 'blank':(None,'observed single expression fragment'),
}

TEMPLATES.update({
 'sqrt_linear_radio':dict(level='moderate',field='radio',family='sqrt',degree=1,source='q-107303',style='linear'),
 'slope_sqrt_positive_radio':dict(level='easy',field='radio',family='sqrt',degree=1,source='q-107288',style='linear',slope=True),
 'slope_sqrt_linear_blank':dict(level='easy',field='blank',family='sqrt',degree=1,source='q-314192',style='linear',slope=True),
 'slope_sqrt_quadratic_blank':dict(level='easy',field='blank',family='sqrt',degree=2,source='q-342792',style='quadratic',slope=True),
 'slope_sqrt_quadratic_radio':dict(level='hard',field='radio',family='sqrt',degree=2,source='q-48848',style='quadratic',slope=True,constant=True),
 'slope_sum_radio':dict(level='easy',field='radio',family='sqrt',degree=1,source='q-20181',style='linear',slope=True,sum=True),
})
PROFILES.update({
 'source_linear':('sqrt_linear_radio','observed whole bank'),
 'source_slope_positive':('slope_sqrt_positive_radio','observed whole bank q-107288'),
 'source_quadratic_slope':('slope_sqrt_quadratic_radio','observed whole bank'),
 'source_sum':('slope_sum_radio','observed whole bank'),
 'operations_chain':(None,'authored full bank: omit inner, reverse sign, double inner, divide inner'),
})
DEFAULT_PROFILES={
 'reciprocal_radio':['source_reciprocal','authored_operations','operations_chain'],
 'sqrt_spaced_radio':['source_spaced','authored_operations','operations_chain'],
 'sqrt_constfirst_radio':['source_constfirst','authored_operations','operations_chain'],
 'sqrt_linear_radio':['source_linear','authored_operations','operations_chain'],
 'slope_sqrt_radio':['source_slope','authored_operations','operations_chain'],
 'slope_sqrt_positive_radio':['source_slope_positive','authored_operations','operations_chain'],
 'slope_sqrt_quadratic_radio':['source_quadratic_slope','authored_operations','operations_chain'],
 'slope_sum_radio':['source_sum','authored_operations','operations_chain'],
}

PROFILES['scale_bank']=(None,'authored whole bank: contiguous coefficient ladder, correct role selected first')
DEFAULT_PROFILES={name:['scale_bank'] for name,spec in TEMPLATES.items() if spec['field']=='radio'}

def tex(v):return sp.latex(sp.sympify(v)).replace(' ', '').replace(r'\left(', '(').replace(r'\right)', ')')
def poly(p,spec,var='x'):
    a,b,c=p['a'],p['b'],p.get('c',0)
    def term(co,n):
        if co==0:return ''
        sign='-' if co<0 else '+'
        co=abs(co)
        return sign+('' if co==1 and n else str(co))+(var if n==1 else ((var[:-1]+r'{)}^{2}' if var.startswith('(') else '{'+var+'}^{2}') if n==2 else ''))
    if spec['degree']==1:
        parts=[term(a,1),term(b,0)] if spec['style']!='constfirst' else [term(b,0),term(a,1)]
    else:parts=[term(a,2),term(b,1),term(c,0)]
    text=''.join(parts).lstrip('+')
    if spec['style']=='spaced':text=text.replace('+',' + ').replace('-',' - ').strip()
    return text

def model(spec,p):
    inner=p['a']*X**spec['degree']+p['b']*(X if spec['degree']==2 else 1)+p.get('c',0)
    exponent=sp.Rational(1,2) if spec['family']=='sqrt' else -sp.Rational(1,2)
    du=sp.diff(inner,X)
    derivative=exponent*inner**(exponent-1)*du
    if spec.get('sum'):derivative+=3*p['k']*X**2
    answer=sp.simplify(derivative.subs(X,p['t'])) if spec.get('slope') else derivative
    return inner,du,exponent,derivative,answer

def frac(n,d):
    n=sp.sympify(n)
    if n==0:return '0'
    neg=n.could_extract_minus_sign()
    if n.is_Rational and n.q!=1:
        prefix=re.match(r'^([0-9]+)',d)
        d=str(n.q*(int(prefix.group(1)) if prefix else 1))+d[len(prefix.group(1)) if prefix else 0:]
        n=sp.Integer(n.p)
    return ('-' if neg else '')+r'\frac{'+tex(-n if neg else n)+'}{'+d+'}'

def derivative_tex(spec,p,at_u=False,simplified=True):
    inner,du,e,der,ans=model(spec,p)
    z='u' if at_u else poly(p,spec)
    z3=r'{u}^{3}' if at_u else '('+z+(r'{)}^{3}' if spec.get('braced') or spec['source'] in ('q-48730','q-342802') else r')^{3}')
    radical=r'\sqrt{'+(z if e>0 else z3)+'}'
    num=du if e>0 else -du
    if simplified:
        coeff=sp.Rational(1,2)
        # Cancel integer factor 2 in numerator, preserving source radical shape.
        g=sp.polys.polytools.terms_gcd(num)
        if all(co%2==0 for co in sp.Poly(num,X).all_coeffs()):num=sp.expand(num/2);den=radical
        else:den='2'+radical
    else:den='2'+radical
    return frac(num,den)

def aligned(rows):return r'\begin{aligned}'+r' \\  & ='.join([D+' & ='+rows[0]]+rows[1:])+r'.\end{aligned}'
def blocks(spec,p):
    """All displayed mathematical blocks are computed, including substitutions."""
    inner,du,e,der,ans=model(spec,p)
    z=poly(p,spec)
    function=r'\sqrt{'+z+'}' if e>0 else r'\frac{1}{\sqrt{'+z+'}}'
    outer=r'\sqrt{u}' if e>0 else r'\frac{1}{\sqrt{u}}={u}^{-1/2}'
    power_stages=spec['source'] in ('q-107291','q-107303') or (spec['degree']==2 and not spec.get('slope') and p['b']==0)
    if power_stages:outer=r'\sqrt{u}={u}^{1/2}'
    outer_deriv=DU+('='+r'\frac{1}{2}{u}^{-1/2}=\frac{1}{2\sqrt{u}}' if power_stages else '='+r'\frac{1}{2\sqrt{u}}') if e>0 else DU+r'=-\frac{1}{2}{u}^{-3/2}=-\frac{1}{2\sqrt{{u}^{3}}}'
    if spec['field']=='blank':outer_deriv+=','
    if spec.get('repair'):outer_deriv=DU+r'=\frac{1}{2\sqrt{u}},'
    outer_factor=r'\frac{1}{2\sqrt{u}}' if e>0 else r'-\frac{1}{2\sqrt{{u}^{3}}}'
    du_tex=tex(du)
    if spec['degree']==1:du_tex=str(p['a'])
    product_du='('+du_tex+')'
    if spec['field']=='blank' and spec['degree']==1:product_du=du_tex
    rows=[outer_factor+r'\cdot '+product_du]
    if spec['level']=='hard':rows.insert(0,DU+r'\cdot '+UX)
    if (spec['family']=='reciprocal' and spec['field']=='blank' and not spec.get('slope')) or spec['source'] in ('q-107303','q-107288','q-20181'):
        rows+=[derivative_tex(spec,p,at_u=True),derivative_tex(spec,p)]
    elif spec['degree']==2 and spec['family']=='sqrt':
        num=sp.factor(du)
        rows += [frac(num,'2'+r'\sqrt{'+z+'}'),derivative_tex(spec,p)]
    elif spec.get('slope') and spec['family']=='reciprocal':
        rows += [derivative_tex(spec,p,simplified=False)]
    else:rows += [derivative_tex(spec,p)]
    multiplication=aligned(rows)
    evaluation=''
    if spec.get('slope'):
        t=p['t']; val=inner.subs(X,t); derivative_render=derivative_tex(spec,p,simplified=spec['family']=='sqrt')
        target=r'{'+D+r'|}_{x='+str(t)+'}'
        subst=poly(p,spec,'('+str(t)+')')
        if e>0:
            half=sp.Rational(p['a'],2)
            evrows=[r'{('+derivative_render+r')|}_{x='+str(t)+'}',frac(half,r'\sqrt{'+subst+'}'),tex(ans)+r'\,']
        else:
            # Keep the source's unreduced numerator for quadratic substitution.
            vdu=tex(du).replace('x','('+str(t)+')')
            first=r'{('+derivative_render+r')|}_{x='+str(t)+'}'
            second='-'+r'\frac{'+vdu+r'}{2\sqrt{('+subst+r'{)}^{3}}}'
            third=frac(-du.subs(X,t),'2'+r'\sqrt{{'+str(val)+r'}^{3}}')
            evrows=[first,second,third,tex(ans)]
        evaluation=r'\begin{aligned}'+target+' & ='+r' \\  & ='.join(evrows)+r'.\end{aligned}'
    return {'z':z,'function':function+(('+' if p['k']>0 else '-')+str(abs(p['k']))+r'{x}^{3}' if spec.get('sum') else ''),'outer':outer,'chain':D+'='+DU+r'\cdot '+UX+'.','outer_deriv':outer_deriv,'inner_deriv':UX+'='+du_tex+'.','multiplication':multiplication,'evaluation':evaluation,'t':str(p.get('t',''))}

_original_blocks=blocks
def blocks(spec,p):
    parts=_original_blocks(spec,p)
    inner,du,e,d,ans=model(spec,p)
    if spec.get('slope') and spec['family']=='sqrt':
        t=p['t'];z=poly(p,spec);dt=derivative_tex(spec,p)
        value=inner.subs(X,t);numerator=du.subs(X,t)
        rows=[r'{('+dt+r')|}_{x='+str(t)+'}',
              r'\frac{'+tex(du).replace('x','('+str(t)+')')+'}{2'+r'\sqrt{'+poly(p,spec,'('+str(t)+')')+'}}',
              r'\frac{'+tex(numerator)+'}{2'+r'\sqrt{'+tex(value)+'}}',tex(ans)]
        parts['evaluation']=r'\begin{aligned}{'+D+r'|}_{x='+str(t)+'} & ='+r' \\  & ='.join(rows)+r'.\end{aligned}'
    if spec.get('sum'):
        # Apply the source's chain-rule stages to f, then its sum-rule stage to y.
        parts['chain']=parts['chain'].replace('y','f')
        parts['outer_deriv']=DU+r'=\frac{1}{2}{u}^{-1/2}=\frac{1}{2\sqrt{u}}'
        parts['outer_deriv']=parts['outer_deriv'].replace('y','f')
        parts['outer']=r'\sqrt{u}={u}^{1/2}'
        parts['radical']=r'\sqrt{'+poly(p,spec)+'}'
        parts['multiplication']=parts['multiplication'].replace('y','f')
        contribution=3*p['k']*X**2
        parts['sum_derivative']=D+'='+derivative_tex(spec,p)+('+' if p['k']>0 else '')+tex(contribution)+'.'
        t=p['t'];rad=inner.subs(X,t);root=sp.sqrt(rad)
        radical_slope=du.subs(X,t)/(2*root)
        first=frac(p['a'],'2'+r'\sqrt{'+poly(p,spec,'('+str(t)+')')+'}')+('+' if p['k']>0 else '')+str(3*p['k'])+'('+str(t)+r')^{2}'
        cubic_value=contribution.subs(X,t)
        second=tex(radical_slope)+('+' if cubic_value>=0 else '')+tex(cubic_value)
        parts['evaluation']=r'\begin{aligned}{'+D+r'|}_{x='+str(t)+'} & ='+r' \\  & ='.join([first,second,tex(ans)])+r'.\end{aligned}'
    return parts

def render(scaffold,parts):
    for key,value in parts.items():scaffold=scaffold.replace('<<'+key+'>>',value)
    if '<<' in scaffold:raise ValueError('Unfilled template')
    return scaffold

def bank(spec,p,profile,assignment=None):
    inner,du,e,d,ans=model(spec,p)
    def assessed(v):return sp.simplify(v.subs(X,p['t'])) if spec.get('slope') else v
    answer_spec={**spec,'braced':False} if spec['source']=='q-314194' else spec
    out=[('correct',ans,tex(ans) if spec.get('slope') or profile=='scale_bank' else derivative_tex(answer_spec,p))]
    if spec['field']=='blank':return out
    if profile=='scale_bank':
        rank=assignment
        # Replace only the radical's inner-derivative coefficient. In sum
        # questions the cubic contribution is identical in all five options:
        # scaling the whole slope would let nearest-cubic guessing bypass it.
        extra=3*p['k']*p['t']**2 if spec.get('sum') else 0
        values=[('coefficient_'+str(q),extra+(ans-extra)*sp.Rational(q,p['a']),None) for q in range(p['a']-rank,p['a']-rank+5) if q!=p['a']]
    elif profile=='source_reciprocal':
        values=[('empirical_minus_three_over_inner',-3/inner,frac(-3,poly(p,spec))),('omit_inner_and_wrong_exponent',1/(2*sp.sqrt(inner)),frac(1,'2'+r'\sqrt{'+poly(p,spec)+'}')),('keep_square_root_exponent',-du/(2*sp.sqrt(inner)),frac(-du,'2'+r'\sqrt{'+poly(p,spec)+'}')),('omit_inner_and_negative_sign',1/(2*inner**sp.Rational(3,2)),frac(1,'2'+r'\sqrt{('+poly(p,spec)+r'{)}^{3}}'))]
    elif profile=='source_spaced':
        reverse=p.copy();reverse['b']=-p['b']; revinner=p['a']*X-p['b'];revz=poly(reverse,spec)
        values=[('omit_half',du/sp.sqrt(inner),frac(du,r'\sqrt{'+poly(p,spec)+'}')),('reverse_constant_and_omit_inner',1/(2*sp.sqrt(revinner)),frac(1,'2'+r'\sqrt{'+revz+'}')),('reverse_constant',du/(2*sp.sqrt(revinner)),frac(du/2,r'\sqrt{'+revz+'}')),('omit_inner',1/(2*sp.sqrt(inner)),frac(1,'2'+r'\sqrt{'+poly(p,spec)+'}'))]
    elif profile=='source_constfirst':
        z=poly(p,spec)
        values=[('divide_by_inner_magnitude',-1/(2*du*sp.sqrt(inner)),frac(-1/du,'2'+r'\sqrt{'+z+'}')),('use_constant_as_divisor',du/(2*p['b']*sp.sqrt(inner)),frac(du/(2*p['b']),r'\sqrt{'+z+'}')),('omit_half_and_reverse_sign',-du/sp.sqrt(inner),frac(-du,r'\sqrt{'+z+'}')),('omit_inner_magnitude',sp.sign(du)/(2*sp.sqrt(inner)),frac(sp.sign(du),'2'+r'\sqrt{'+z+'}'))]
    elif profile=='source_slope':
        v=inner.subs(X,p['t']); root=sp.sqrt(v)
        # Empirical expression shapes, not a claim to recover cognitive errors.
        values=[('empirical_minus_five_over_root',-5/root,None),('empirical_one_over_root',1/root,None),('empirical_root_over_linear_coefficient',root/p['a'],None),('empirical_negative_half_coefficient',-sp.Rational(p['a'],2),None)]
    elif profile=='source_linear':
        z=r'\sqrt{'+poly(p,spec)+'}'
        values=[('omit_inner',1/(2*sp.sqrt(inner)),frac(1,'2'+z)),('reverse_sign',-ans,frac(-du/2,z)),('divide_by_inner',1/(2*du*sp.sqrt(inner)),frac(1/(2*du),z)),('divide_and_reverse',-1/(2*du*sp.sqrt(inner)),frac(-1/(2*du),z))]
    elif profile=='source_slope_positive':
        r=sp.sqrt(inner.subs(X,p['t']))
        values=[('omit_half',p['a']/r,None),('root_instead_of_slope',r,None),('reciprocal_point',sp.Rational(1,p['t']),None),('inner_derivative',sp.Integer(p['a']),None)]
    elif profile=='source_quadratic_slope':
        values=[('extra_half',ans/2,None),('reverse_sign',-ans,None),('reverse_and_double',-2*ans,None),('omit_half',2*ans,None)]
    elif profile=='source_sum':
        r=sp.sqrt(inner.subs(X,p['t'])); k=p['k']; t=p['t']
        values=[('empirical_half_cubic_derivative',p['a']/(2*r)+sp.Rational(3,2)*k*t**2,None),('empirical_add_point',p['a']/(2*r)+t,None),('lower_power_twice',p['a']/(2*r)+3*k*t,None),('empirical_add_point_squared',p['a']/(2*r)+t**2,None)]
    elif profile=='operations_chain':
        extra=3*p['k']*p['t']**2 if spec.get('sum') else 0
        radans=ans-extra
        base=assessed(e*inner**(e-1))
        factor=assessed(du)
        values=[('omit_inner',base+extra,None),('reverse_radical_sign',-radans+extra,None),('double_inner',2*radans+extra,None),('divide_inner',base/factor+extra,None)]
    elif profile=='authored_operations':
        extra=3*p['k']*p['t']**2 if spec.get('sum') else 0
        values=[('omit_inner_derivative',assessed(e*inner**(e-1))+extra,None),('reverse_derivative_sign',-(ans-extra)+extra,None),('omit_half',2*(ans-extra)+extra,None),('do_not_lower_outer_power',assessed(e*inner**e*du)+extra,None)]
    else:raise ValueError('Unknown bank')
    for label,value,latex in values:out.append((label,sp.simplify(value),latex or tex(value)))
    for i,(_,value,_) in enumerate(out):
        if value.has(sp.zoo,sp.nan,sp.oo) or value.is_real is False:raise ValueError('Invalid whole bank')
        for _,other,_ in out[:i]:
            if sp.simplify(value-other)==0:raise ValueError('Ambiguous whole bank')
    return out

def check_parameters(spec,p):
    expected={'a','b'} | ({'c'} if spec['degree']==2 else set()) | ({'t'} if spec.get('slope') else set()) | ({'k'} if spec.get('sum') else set())
    if set(p)!=expected or any(type(v)!=int for v in p.values()):raise ValueError('Exact integer parameters required: '+str(sorted(expected)))
    if p['a']==0:raise ValueError('Nonconstant inner function required')
    if spec['degree']==2 and not spec.get('constant'):
        if spec.get('slope') and p['c']!=0:raise ValueError('Evaluated quadratic shape requires c=0')
        if not spec.get('slope') and p['b']!=0 and p['c']!=0:raise ValueError('Derivative quadratic retains two polynomial terms')
    if spec['degree']==1 and abs(p['a'])==1 and spec['field']=='radio' and not spec.get('sum'):raise ValueError('Radio coefficient magnitude >=2 avoids omitted-chain collision')
    inner,du,e,d,ans=model(spec,p)
    if spec.get('slope') and inner.subs(X,p['t'])<=0:raise ValueError('Slope requires positive radicand')
    if spec.get('constant') and p['b']!=0:raise ValueError('Two-term constant quadratic required')
    if spec.get('sum') and p['k']==0:raise ValueError('Nonzero cubic term required')
    if spec.get('slope') and not sp.sqrt(inner.subs(X,p['t'])).is_Integer:raise ValueError('Easy slope requires a perfect-square radicand')
    if spec['family']=='sqrt' and spec['degree']==2 and p['a']<0 and sp.discriminant(inner,X)<=0:raise ValueError('No positive real domain')

RECIPROCAL_QUADRATIC_POOLS={case:[] for case in [-1,0,1]}
for _a in range(-6,7):
    for _b in range(-24,25):
        for _t in [-4,-3,-2,-1,1,2,3,4]:
            _v=_a*_t*_t+_b*_t
            if _a and _b and _v>0 and int(_v**.5)**2==_v and _v<=144:
                _sgn=(2*_a*_t+_b>0)-(2*_a*_t+_b<0)
                RECIPROCAL_QUADRATIC_POOLS[_sgn].append(dict(a=_a,b=_b,c=0,t=_t))

def sample(spec,rng):
    # Choose answer-bearing sign/case first; derive compatible real radicands.
    sign=rng.choice([-1,1])
    a=sign*rng.randint(2,8)
    if spec.get('slope') and spec['degree']==1:
        t=rng.randint(-4,4);r=rng.randint(1,9)
        return dict(a=a,b=r*r-a*t,t=t,**({'k':rng.choice([-4,-3,-2,-1,1,2,3,4])} if spec.get('sum') else {}))
    if spec.get('slope') and spec.get('constant'):
        a=rng.choice([i for i in range(-6,7) if i]);t=sign*(1 if a>0 else -1)*rng.randint(1,4);r=rng.randint(1,12)
        return dict(a=a,b=0,c=r*r-a*t*t,t=t)
    if spec.get('slope') and spec['family']=='sqrt':
        case=rng.choice([-1,0,1]); t=rng.choice([-4,-3,-2,-1,1,2,3,4])
        # This finite pool preserves c=0, small integers, square radicands and all slope cases.
        pool=SQRT_QUADRATIC_POOLS[case]
        return dict(rng.choice(pool))
    if spec.get('slope'):return dict(rng.choice(RECIPROCAL_QUADRATIC_POOLS[rng.choice([-1,0,1])]))
    if spec['degree']==1:return dict(a=a,b=rng.choice([i for i in range(-12,13) if i]))
    # Canonical e-182 and q-342680 justify both two-term quadratic shapes.
    if rng.choice(['linear','constant'])=='constant':
        c=rng.randint(1,12) if a<0 else rng.choice([i for i in range(-12,13) if i])
        return dict(a=a,b=0,c=c)
    return dict(a=a,b=rng.choice([i for i in range(-12,13) if i]),c=0)

SQRT_QUADRATIC_POOLS={case:[] for case in [-1,0,1]}
for _a in range(-5,6):
    for _b in range(-12,13):
        for _t in [-4,-3,-2,-1,1,2,3,4]:
            _v=_a*_t*_t+_b*_t
            if _a and _b and _v>0 and int(_v**.5)**2==_v and _v<=144:
                SQRT_QUADRATIC_POOLS[(2*_a*_t+_b>0)-(2*_a*_t+_b<0)].append(dict(a=_a,b=_b,c=0,t=_t))

# EASY: evaluated slopes; source evidence includes linear sqrt and quadratic
# reciprocal. These are alternatives, never a progression in this difficulty.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: radical or reciprocal radical with linear inner function.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: preserve both observed blank layouts, including the linear source.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,replay=False,bank_role=None):
    rng=random.Random(seed)
    if profile not in (None,'scale_bank','blank') and not replay:
        raise ValueError('Historical banks are available only through source replay')
    if profile not in (None,'scale_bank','authored_operations','operations_chain','blank'):
        if profile not in PROFILES:raise ValueError('Unknown profile')
        required=PROFILES[profile][0]
        if template is not None and template!=required:raise ValueError('Ineligible source profile')
        template=required
    eligible=[k for k,v in TEMPLATES.items() if v['level']==level and (field_type is None or field_type in (v['field'],':answer-field.type/'+v['field']))]
    if template is None:
        if not eligible:raise ValueError('No eligible templates')
        template=rng.choice(eligible)
    if template not in eligible:raise ValueError('Template incompatible with level or field')
    spec=TEMPLATES[template];profile=profile or ('blank' if spec['field']=='blank' else rng.choice(DEFAULT_PROFILES[template]))
    assignment=(rng.randrange(5) if bank_role is None else bank_role) if profile=='scale_bank' else None
    if assignment is not None and (type(assignment)!=int or assignment not in range(5)):raise ValueError('Bank role must be 0..4')
    if (spec['field']=='blank')!=(profile=='blank'):raise ValueError('Profile incompatible with field')
    for attempt in range(1000):
        p=dict(parameters) if parameters is not None else sample(spec,rng)
        try:check_parameters(spec,p); options=bank(spec,p,profile,assignment);break
        except ValueError:
            if parameters is not None:raise
    else:raise ValueError('No valid whole-bank instance')
    parts=blocks(spec,p)
    scaffold=json.loads((ROOT/'templates.json').read_text())[template]
    prompt=normalize_prose(render(scaffold['prompt'],parts));solution=normalize_prose(render(scaffold['solution'],parts))
    options=[(label,value,normalize_tex(latex)) for label,value,latex in options]
    inner,du,e,d,ans=model(spec,p)
    domain=tex(inner)+'>0'
    mathematical_identity={'inner':str(sp.expand(inner)), 'outer_exponent':str(e), 'evaluation_point':p.get('t'), 'cubic_coefficient':p.get('k'), 'response_kind':'slope' if spec.get('slope') else 'derivative RHS', 'domain':str(sp.expand(inner))+'>0'}
    fingerprint=hashlib.sha256(json.dumps(mathematical_identity,sort_keys=True).encode()).hexdigest()
    display={'version':VERSION,'template':template,'parameters':p,'profile':profile,'domain':domain,'prompt':prompt,'solution':solution,'bank':sorted(v for _,_,v in options),'field':spec['field']}
    identity=hashlib.sha256(json.dumps(display,sort_keys=True).encode()).hexdigest()
    def uid(role):return str(uuid.uuid5(uuid.UUID(KP_UUID),identity+':'+role))
    answers=[{':answer/id':uid('answer:'+value),':answer/type':':answer.type/math',':answer/value':value} for _,_,value in options]
    correct=answers[0][':answer/id'];rng.shuffle(answers)
    field={':answer-field/id':uid('field'),':answer-field/key':'selection' if spec['field']=='radio' else 'field-1',':answer-field/type':':answer-field.type/'+spec['field'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':uid('question'),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'generator_version':VERSION,'template':template,'seed':seed,'parameters':p,'bank_profile':profile,'bank_origin':PROFILES[profile][1],'source':SOURCE,'source_ids':[spec['source']],'source_repair':bool(spec.get('repair')),'domain':domain,'plot_rating':'none','parameter_fingerprint':fingerprint,'content_fingerprint':identity,'sympy_version':sp.__version__,'exact':{'inner':str(inner),'inner_derivative':str(du),'outer_exponent':str(e),'derivative':str(d),'answer':str(ans)},'bank_assignment':assignment,'attempts':attempt+1,'recipes':{value:label for label,_,value in options}}}

def replay_sources():
    """Recompute every original instance; retain entire immutable capture separately.

    Blank choice lists contain historical submissions, including incomplete TeX;
    they are evidence, not an authored choice bank. The served blank is computed.
    """
    sources={q[':question/math-academy-id']:q for q in json.loads((ROOT/'source-questions.json').read_text())}
    records=[]
    for case in json.loads((ROOT/'source-cases.json').read_text()):
        rec=generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'],replay=True)
        rec['generation']['source_capture']=sources[case['source_id']]
        rec['generation']['replay_source_id']=case['source_id']
        rec['generation']['repairs']=case['repairs']
        records.append(rec)
    return records

def markdown(rec):
    q=rec['question'];field=q[':question/answer-fields'][0]
    s=q[':question/problem']+'\n\n'
    if field[':answer-field/type'].endswith('/radio'):
        s+='\n'.join('- $'+a[':answer/value']+'$' for a in field[':answer-field/choices'])+'\n\n'
    return s+q[':question/worked-solution']

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='json');ap.add_argument('--template');ap.add_argument('--profile',choices=['scale_bank','blank']);ap.add_argument('--replay-source',action='store_true');a=ap.parse_args()
    records=replay_sources() if a.replay_source else [generate(level,a.seed+i,a.template,profile=a.profile) for level in (['moderate'] if a.difficulty=='unclassified' else [a.difficulty]) for i in range(a.count)]
    print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
