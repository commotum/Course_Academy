#!/usr/bin/env python3
"""Unit normals to plane level curves, local step-3–7 draft.

API: generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), plus three difficulty entrypoints. Supplied math basis 2847; standalone package.
All normal questions ask for ANY unit normal, so both gradient orientations are
mathematically valid. Complete banks reject antipodal distractors. Historical
opaque banks are public evidence-only profiles; they are not default samplers.
Source formal derivative/evaluation/normalization stages and shared prose persist
in normal variants. Number notation is normalized, separately from fidelity.
Only this script and its private evidence directory are written. No EDB access.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import random
import re
import sys
import uuid
import sympy as s

from math_format import normalize_prose, normalize_tex, checked_math_content

ROOT = Path(__file__).resolve().parent
KP_ID = 17592186124461
VERSION = 'level-curve-unit-normal-package-3'
SOURCE = json.loads((ROOT/'source.json').read_text())
KP = SOURCE['record']
CASES = json.loads((ROOT/'source-cases.json').read_text())
QUESTIONS = {z[':question/math-academy-id']: z for z in KP[':knowledge-point/questions']}
BY_FAMILY = {c['template']:c for c in CASES}
X,Y = s.symbols('x y',real=True)
FUNCTIONS = {
 'axisquad':2*X**2+2*Y**2-Y, 'mixed':2*X+4*Y+5*X*Y,
 'roots':s.sqrt(X)+2*s.sqrt(Y), 'log':s.log(X*Y),
 'circle':X**2+Y**2, 'bilinear':X+3*Y-2*X*Y,
 'exp':s.exp(X+Y)+X+Y, 'quotient':(X+Y)/(X-Y),
 'angle':s.atan(Y/X), 'radical':s.sqrt(X**2-Y**2),
 'canonical':X**2+2*Y**2+X,
}
TEX = {
 'axisquad':r'2x^{2}+2y^{2}-y', 'mixed':'2x+4y+5xy',
 'roots':r'\sqrt{x}+2\sqrt{y}', 'log':r'\operatorname{ln}⁡(xy)',
 'circle':r'{x}^{2}+{y}^{2}', 'bilinear':'x+3y-2xy',
 'exp':r'{e}^{x+y}+x+y','quotient':r'\frac{x+y}{x-y}',
 'angle':r'\operatorname{arctan}⁡(\frac{y}{x})',
 'radical':r'\sqrt{{x}^{2}-{y}^{2}}','canonical':r'{x}^{2}+2{y}^{2}+x',
}
FAMILIES = {'easy':tuple(BY_FAMILY)}
LEVELS = tuple(FAMILIES)
LEARNER_PROFILES = {
    family: (('method-balanced',) if family in ('log','circle') else ('method-generic',))
    + (('method-axis', 'method-axis-unit') if family in
       ('axisquad','circle','bilinear','quotient','angle') else
       ('method-axis-unit',) if family=='radical' else ())
    + (('method-bilinear-axis','method-balanced') if family=='bilinear' else
       ('method-generic',) if family=='log' else ())
    for family in FAMILIES['easy']
}
PARTIALS = {k:tuple(s.simplify(s.diff(f,z)) for z in (X,Y)) for k,f in FUNCTIONS.items()}

def function_for(family,c=1,d=1):
    return s.exp(X+Y)+c*X+d*Y if family=='exp' else FUNCTIONS[family]

def function_tex(family,c=1,d=1):
    if family!='exp':return TEX[family]
    return r'{e}^{x+y}+'+('' if c==1 else str(c))+'x+'+('' if d==1 else str(d))+'y'

def tex(z):
    return s.latex(s.sympify(z),ln_notation=True).replace('- ', '-')

def point(p,q):
    return tex(p)+','+tex(q)

def vec(a,b):
    """Two complete components, omitting zeros and unit coefficients."""
    a,b=s.simplify(a),s.simplify(b)
    if a==b==0:return '0'
    out=''
    for z,v in ((a,'i'),(b,'j')):
        if z==0:continue
        negative=bool(z.could_extract_minus_sign())
        magnitude=-z if negative else z
        term=('' if magnitude==1 else tex(magnitude)+r'\,')+v
        out+=('-' if negative else ('+' if out else ''))+term
    return out

def rational_direction(a,b):
    """Positive common factor; signs stay in the ordered direction."""
    if not (a.is_Rational and b.is_Rational):raise ValueError('gradient must have rational components')
    den=s.ilcm(a.q,b.q);ai,bi=int(a*den),int(b*den)
    g=math.gcd(abs(ai),abs(bi));return s.Rational(g,den),s.Integer(ai//g),s.Integer(bi//g)

def unit(a,b):
    m=s.sqrt(a*a+b*b)
    return tuple(s.simplify(z/m) for z in (a,b))

def normalized_tex(a,b):
    c,A,B=rational_direction(a,b)
    n=A*A+B*B
    if n==1:return vec(A,B)
    # Source convention: rationalized scalar times a primitive direction.
    return tex(s.sqrt(n)/n)+'('+vec(A,B)+')'

def choice_tex(a,b):
    # All unit choices use the same notation, so factorization cannot reveal
    # which unit direction is correct before the learner differentiates.
    if s.simplify(a*a+b*b-1)==0:
        if a==0 or b==0:return vec(a,b)
        ratio=s.simplify(a/b)
        if ratio.is_Rational:
            orientation=s.sign(b)
            return normalized_tex(ratio.p*orientation,ratio.q*orientation)
    return vec(a,b)

def factored_tex(a,b):
    c,A,B=rational_direction(a,b)
    return ('' if c==1 else tex(c))+'('+vec(A,B)+')'

def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(o):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+digest(o)))

def rational(z):
    if isinstance(z,bool):raise ValueError('boolean coordinate')
    try:v=s.Rational(str(z))
    except Exception as e:raise ValueError('coordinates must be exact rationals') from e
    return v

def allowed(level,family,p,q,c=1,d=1):
    """Identical explicit/sampled bounds. Workload policies are authored, not labels recovered from sources."""
    if level not in LEVELS or family not in FAMILIES[level]:raise ValueError('family unavailable at level')
    if level=='easy':
        if abs(p)>16 or abs(q)>16 or max(p.q,q.q)>2:raise ValueError('easy coordinate bounds')
        if family in ('axisquad','mixed','log','quotient','angle','exp') and (not(p.is_Integer and q.is_Integer) or max(abs(p),abs(q))>4):raise ValueError('easy integer coordinates bounded by four')
        if family in ('circle','bilinear') and max(abs(p),abs(q))>4:raise ValueError('easy halves bounded by four')
        if family=='bilinear' and p.q>1 and q.q>1:raise ValueError('easy bilinear uses at most one fractional coordinate')
        if family=='roots' and not (p in (1,4,9,16) and q in (1,4,9,16)):raise ValueError('easy familiar square roots')
        if family=='radical' and (not (p.is_Integer and q.is_Integer) or not s.sqrt(p*p-q*q).is_Integer):raise ValueError('easy perfect-square radicand')
        if family=='exp' and p+q!=0:raise ValueError('easy exponential evaluates at zero')
    if family=='roots' and (p<=0 or q<=0):raise ValueError('square roots require positive coordinates')
    if family=='log' and p*q<=0:raise ValueError('log requires xy>0')
    if family=='quotient' and p==q:raise ValueError('quotient requires x != y')
    if family=='angle' and p==0:raise ValueError('arctan(y/x) requires x != 0')
    if family=='radical' and p*p<=q*q:raise ValueError('radical requires x²>y²')
    if family=='exp':
        if c not in range(1,5) or d not in range(1,5):raise ValueError('exponential affine coefficients 1–4')
        a,b=s.Integer(1+c),s.Integer(1+d)
    else:a,b=(s.simplify(v.subs({X:p,Y:q})) for v in PARTIALS[family])
    if a==b==0:raise ValueError('zero gradient')
    if not all(v.is_Rational for v in (a,b)):raise ValueError('workload uses exact rational gradient components')
    return a,b

def raw_component(family,p,q,c=1,d=1):
    """Held-coordinate formal masks and unsimplified evaluation masks, preserving operations."""
    P,Q='('+tex(p)+')','('+tex(q)+')'
    if family=='axisquad':return ('4x','4y-1'),('4'+P,'4'+Q+'-1')
    if family=='mixed':return ('2+5y','4+5x'),('2+5'+Q,'4+5'+P)
    if family=='roots':return (r'\frac{1}{2\sqrt{x}}',r'\frac{1}{\sqrt{y}}'),(r'\frac{1}{2\sqrt{'+tex(p)+'}}',r'\frac{1}{\sqrt{'+tex(q)+'}}')
    if family=='log':return (r'\frac{1}{x}',r'\frac{1}{y}'),(r'\frac{1}{'+P+'}',r'\frac{1}{'+Q+'}')
    if family=='circle':return ('2x','2y'),('2'+P,'2'+Q)
    if family=='bilinear':return ('1-2y','3-2x'),('1-2'+Q,'3-2'+P)
    if family=='exp':return (r'{e}^{x+y}+'+str(c),r'{e}^{x+y}+'+str(d)),(r'{e}^{'+tex(p)+'+'+Q+'}+'+str(c),r'{e}^{'+tex(p)+'+'+Q+'}+'+str(d))
    if family=='quotient':
        return (r'-\frac{2y}{(x-y)^{2}}',r'\frac{2x}{(x-y)^{2}}'),(r'-\frac{2'+Q+'}{('+tex(p)+'-'+Q+r')^{2}}',r'\frac{2'+P+'}{('+tex(p)+'-'+Q+r')^{2}}')
    if family=='angle':return (r'-\frac{y}{{x}^{2}+{y}^{2}}',r'\frac{x}{{x}^{2}+{y}^{2}}'),(r'-\frac{'+Q+'}{'+P+r'^{2}+'+Q+r'^{2}}',r'\frac{'+P+'}{'+P+r'^{2}+'+Q+r'^{2}}')
    if family=='radical':return (r'\frac{x}{\sqrt{{x}^{2}-{y}^{2}}}',r'-\frac{y}{\sqrt{{x}^{2}-{y}^{2}}}'),(r'\frac{'+P+r'}{\sqrt{'+P+r'^{2}-'+Q+r'^{2}}}',r'-\frac{'+Q+r'}{\sqrt{'+P+r'^{2}-'+Q+r'^{2}}}')
    if family=='canonical':return ('2x+1','4y'),('2'+P+'+1','4'+Q)
    raise ValueError(family)

def pair_tex(parts):return '('+parts[0]+r')\,i+('+parts[1]+r')\,j'
def aligned(rows):return '\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n'

def solution_blocks(family,p,q,a,b,c=1,d=1):
    """Per-family source stage structure. No CAS collapse of arithmetic masks."""
    name='g' if family=='log' else 'f';pt=point(p,q);g='∇'+name
    parts,evaluation=raw_component(family,p,q,c,d)
    definition=g+'(x,y) & ={'+name+r'}_{x}(x,y)\,i+{'+name+r'}_{y}(x,y)\,j'
    formal=g+r'(x,y) & =\frac{∂}{∂x}('+function_tex(family,c,d)+r')\,i+\frac{∂}{∂y}('+function_tex(family,c,d)+r')\,j'
    if family not in ('mixed','circle','bilinear','exp','radical'):
        formal=' & ='+formal.split('& =',1)[1]
    derivative=' & ='+pair_tex(parts)
    substitute=g+'('+pt+') & ='+pair_tex(evaluation)
    evaluated=' & ='+vec(a,b)
    factored=' & ='+factored_tex(a,b)
    if family=='roots':rows=[definition,formal,derivative,substitute,evaluated,factored]
    elif family=='log':rows=[definition,formal,r' & =\frac{1}{xy}\cdot y\,i+\frac{1}{xy}\cdot x\,j',derivative,substitute,evaluated]
    elif family in ('mixed','circle','bilinear','exp'):rows=[formal,derivative,substitute,evaluated]
    elif family=='quotient':rows=[definition,formal,r' & =\frac{1(x-y)-(x+y)(1)}{(x-y)^{2}}\,i+\frac{1(x-y)-(x+y)(-1)}{(x-y)^{2}}\,j',derivative,substitute,evaluated]
    elif family=='angle':
        den=p*p+q*q
        individual=' & ='+r'\frac{'+tex(-q)+'}{'+tex(den)+r'}\,i+\frac{'+tex(p)+'}{'+tex(den)+r'}\,j'
        rows=[definition,formal,r' & =\frac{(-\frac{y}{{x}^{2}})}{1+{(\frac{y}{x})}^{2}}\,i+\frac{(\frac{1}{x})}{1+{(\frac{y}{x})}^{2}}\,j',derivative,substitute,individual,factored]
    elif family=='radical':
        rad=p*p-q*q
        individual=' & ='+r'\frac{'+tex(p)+r'}{\sqrt{'+tex(rad)+r'}}\,i-\frac{'+tex(q)+r'}{\sqrt{'+tex(rad)+r'}}\,j'
        rows=[formal,derivative,substitute,individual,evaluated]
    else:
        # Canonical zero held-coordinate terms remain visible before reduction.
        zeros={'canonical':r'(2x+0+1)\,i+(0+4y+0)\,j','axisquad':r'(4x+0+0)\,i+(0+4y-1)\,j','mixed':r'(2+0+5y)\,i+(0+4+5x)\,j'}
        rows=[definition,formal,' & ='+zeros[family],derivative,substitute,evaluated]
    c,A,B=rational_direction(a,b);N=A*A+B*B;m=s.sqrt(a*a+b*b)
    lhs=r'\frac{'+g+'('+pt+')}{‖'+g+'('+pt+')‖}'
    magnitude=r'\sqrt{('+tex(a)+r')^{2}+('+tex(b)+r')^{2}}'
    initial=lhs+r' & =\frac{'+vec(a,b)+'}{'+magnitude+'}'
    final=' & ='+normalized_tex(a,b)
    if family in ('roots','angle'):
        fv=factored_tex(a,b)
        norms=[lhs+r' & =\frac{'+fv+'}{‖'+fv+'‖}',r' & =\frac{1}{('+tex(c)+r'\cdot\sqrt{('+tex(A)+r')^{2}+('+tex(B)+r')^{2}})}\cdot '+fv,r' & =\frac{1}{\sqrt{'+tex(N)+'}}('+vec(A,B)+')',final]
    elif family=='log':norms=[initial,final]
    elif family in ('circle','mixed'):norms=[initial,r' & =\frac{'+vec(a,b)+'}{'+tex(m)+'}',final]
    elif family=='bilinear':
        norms=[initial+'='+normalized_tex(a,b)] if N==1 else [initial,r' & =\frac{'+vec(a,b)+'}{'+tex(m)+'}',final]
    elif family=='exp':norms=[initial,r' & =\frac{'+vec(a,b)+'}{'+tex(m)+'}',final]
    elif family=='quotient':norms=[initial,r' & =\frac{1}{'+tex(m)+'}('+vec(a,b)+')',r' & =\frac{1}{\sqrt{'+tex(N)+'}}('+vec(A,B)+')',final]
    elif family=='radical':norms=[initial,r' & =\frac{'+vec(a,b)+'}{'+tex(m)+'}',final]
    elif family=='axisquad' and N==1:norms=[lhs+r' & =\frac{'+vec(a,b)+'}{'+tex(m)+'}='+normalized_tex(a,b)]
    else:norms=[initial,final]
    # Wrap long vector sums at the component boundary; this is one equation,
    # with an indented + continuation, not an extra differentiation stage.
    rendered=[]
    for row in rows:
        wrap=(row==formal or (family=='quotient' and '1(x-y)' in row)
              or (row==substitute and family in ('quotient','angle','radical')))
        rendered.append(row.replace(r'\,i+',r'\,i \\ &\quad +',1) if wrap else row)
    return aligned(rendered),aligned(norms),{'gradient_rows':len(rows),'normalization_rows':len(norms)}

def solution(family,p,q,a,b,c=1,d=1):
    """Use full captured shared prose, slot complete points and math blocks only."""
    if family in BY_FAMILY:
        source=QUESTIONS[BY_FAMILY[family]['source_id']]
    else:source=KP[':knowledge-point/canonical-example']
    original=source.get(':question/worked-solution')
    name='g' if family=='log' else 'f';pt=point(p,q)
    blocks,normal,structure=solution_blocks(family,p,q,a,b,c,d)
    if original is None:
        original=('A normal vector to the level curve that passes through the point where $(x,y)=({point})$ can be found by computing $∇f({point}).$\n\n'
                  'So, we first find the gradient and evaluate it at $(x,y)=({point}):$\n\n$${gradient}$$\n\nFinally, we normalize $∇f({point}):$\n\n$${normal}$$')
        return original.replace('{point}',pt).replace('{gradient}',blocks).replace('{normal}',normal),structure
    # Complete original point tokens are masked before replacement, protecting x,y and basis labels.
    pieces=original.split('$$')
    if len(pieces)!=5:raise ValueError('unexpected source solution layout')
    old=BY_FAMILY[family]['parameters'] if family in BY_FAMILY else {'p':'1','q':'1'}
    oldpt=point(rational(old['p']),rational(old['q']))
    oldtokens={oldpt}
    if family=='canonical':oldtokens.add('1,1')
    for index in (0,2,4):
        for token in oldtokens:pieces[index]=pieces[index].replace('('+token+')','({point})')
        pieces[index]=pieces[index].replace('{point}',pt)
    pieces[1],pieces[3]=blocks,normal
    return '$$'.join(pieces),structure

def observed_bank(family,p,q,a,b):
    """Parameterized mathematical bank patterns; opaque operations remain evidence only.

    Complete source expression values are computed, never looked up by answer.
    Constants in legacy shapes do not assert recovered author intent. Rendered
    values are computed from these operations, including at original parameters.
    """
    U=unit(a,b);nx,ny=U
    if family=='axisquad':return [('-k',None),('diagonal',unit(1,1)),('normal',U),('horizontal',(s.Integer(1),s.Integer(0))),('negative diagonal',(-s.Integer(1),-s.Integer(1)))],2
    if family=='mixed':return [('opaque altered y',(a,-(b-2))),('repeat x',(a,a)),('normal',U),('opaque fixed',(s.Integer(1),-s.Integer(4))),('swapped',unit(b,a))],2
    if family=='roots':return [('normal',U),('double y',unit(a,2*b)),('flip y',unit(a,-b)),('down',(s.Integer(0),-s.Integer(1))),('halve y',unit(a,b/2))],0
    if family=='log':return [('flip y',unit(a,-b)),('unnormalized',(a,b)),('opaque root3',(s.sqrt(3)*a,s.sqrt(3)*b)),('opaque wrong norm',(s.sqrt(3)*a/2,-s.sqrt(3)*b/2)),('normal',U)],4
    if family=='circle':return [('flip y',unit(a,-b)),('horizontal',(s.Integer(1),s.Integer(0))),('normal',U),('l1 normalized',(a/(abs(a)+abs(b)),b/(abs(a)+abs(b)))),('down',(s.Integer(0),-s.Integer(1)))],2
    if family=='bilinear':return [('down',(s.Integer(0),-s.Integer(1))),('repeated basis',(s.Integer(2),s.Integer(0))),('cancel basis',(s.Integer(0),s.Integer(0))),('normal',U),('opaque repeated basis',(-1/s.sqrt(5),s.Integer(0)))],3
    if family=='exp':return [('l1 flip',(a/(abs(a)+abs(b)),-b/(abs(a)+abs(b)))),('horizontal',(s.Integer(1),s.Integer(0))),('vertical',(s.Integer(0),s.Integer(1))),('flip y',unit(a,-b)),('normal',U)],4
    if family=='quotient':return [('swap flip',unit(-b,a)),('normal',U),('opaque repeated j',(s.Integer(0),1/s.sqrt(5))),('diagonal flip',unit(1,-1)),('flip y',unit(a,-b))],1
    if family=='angle':return [('unnormalized primitive',(s.Integer(1),-s.Integer(1))),('flip x',unit(-a,b)),('normal',U),('sum primitive',(s.Integer(1),s.Integer(1))),('flip y',unit(a,-b))],2
    if family=='radical':return [('flip y',unit(a,-b)),('horizontal',(s.Integer(1),s.Integer(0))),('diagonal',unit(1,1)),('vertical',(s.Integer(0),s.Integer(1))),('normal',U)],4
    raise ValueError('no observed bank')

def method_bank(family,p,q,a,b,profile):
    """Five complete method-derived operations selected before parameters."""
    U=unit(a,b)
    if profile=='method-axis-unit':
        if (a!=0 and b!=0) or a*a+b*b!=1:
            raise ValueError('unit axis bank requires an already unit axial gradient')
        swapped=(b,a)
        return [('normal',U),('swap partials',swapped),
                ('swap and negate partials',(-b,-a)),
                ('retain zero partial with same sign',unit(a+b,b+a)),
                ('retain zero partial with opposite sign',unit(a-b,b-a))],0
    if profile=='method-bilinear-axis':
        if family!='bilinear' or a==0 or b!=0:raise ValueError('bilinear x-axis bank')
        return [('normal',U),('omit constant x partial',(-2*q,s.Integer(0))),('swap normal components',unit(b,a)),('omit mixed partials',unit(1,3)),('exchange substitution coordinates',unit(1-2*p,3-2*q))],0
    if profile=='method-axis':
        # This complete bank works for both large and fractional magnitudes.
        if a!=0 and b!=0:raise ValueError('axis bank needs an axis normal')
        z=a or b
        if abs(z)==1:raise ValueError('use unit axis bank for |component|=1')
        wrong=unit(b,a)
        return [('normal',U),('swap partials',wrong),('omit normalization',(a,b)),('normalize by squared norm',(a/(a*a+b*b),b/(a*a+b*b))),('swap then omit normalization',(b,a))],0
    if profile not in ('method-generic','method-balanced'):raise ValueError('unknown method profile')
    if a==0 or b==0 or abs(a)==abs(b):
        # Balanced derivatives use the actual partials and L1/wrong-magnitude
        # normalization; swap would be another valid normal.
        if a==0 or b==0:raise ValueError('generic bank needs two nonzero components')
        fourth=('omit normalization',(a,b)) if profile=='method-balanced' else ('squared magnitude',(a/(a*a+b*b),b/(a*a+b*b)))
        return [('normal',U),('flip one partial',unit(a,-b)),('l1 normalization',(a/(abs(a)+abs(b)),b/(abs(a)+abs(b)))),fourth,('hold y partial at zero',(s.sign(a),s.Integer(0)))],0
    return [('normal',U),('flip one partial',unit(a,-b)),('swap partials',unit(b,a)),('omit normalization',(a,b)),('l1 normalization',(a/(abs(a)+abs(b)),b/(abs(a)+abs(b))))],0

def valid_unit(v,a,b):
    if v is None:return False
    u,w=v
    return s.simplify(u*u+w*w-1)==0 and s.simplify(u*b-w*a)==0

def validate_bank(bank,index,a,b):
    if len(bank)!=5:raise ValueError('complete bank must contain five choices')
    for i,(_,v) in enumerate(bank):
        if v is None:raise ValueError('out-of-plane legacy option')
        if valid_unit(v,a,b)!=(i==index):raise ValueError('ambiguous or incorrectly designated unit normal')
        for _,w in bank[:i]:
            if all(s.simplify(v[j]-w[j])==0 for j in (0,1)):raise ValueError('equivalent option collision')

def sampling_domain(level,family):
    if level=='easy':
        if family=='roots':return [(s.Integer(a*a),s.Integer(b*b)) for a in range(1,5) for b in range(1,5)]
        if family=='exp':return [(s.Integer(a),s.Integer(-a)) for a in range(-4,5)]
        if family=='radical':return [(s.Integer(a),s.Integer(b)) for a in range(-16,17) for b in range(-16,17) if a*a>b*b and s.sqrt(a*a-b*b).is_Integer]
        grid=[s.Rational(a,2) for a in range(-8,9)]
        if family in ('mixed','axisquad','log','quotient','angle'):grid=[s.Integer(a) for a in range(-4,5)]
        return [(a,b) for a in grid for b in grid]
    raise ValueError('unsupported difficulty')

def prompt(family,p,q,raw,c=1,d=1):
    if family in BY_FAMILY:
        text=prompt_original_notation(family,p,q)
        if family=='exp':
            text=re.sub(r'(\$f\(x,y\)=)(.*?)(\$)',lambda m:m[1]+function_tex(family,c,d)+m[3],text,count=1)
        return text
    return 'Find a unit normal vector to the level curve of the function $f(x,y)='+TEX[family]+'$ that passes through the point where $(x,y)=('+point(p,q)+').$'

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio field supported')
    rng=random.Random(seed)
    raw=bool(profile and profile.startswith('observed-'))
    if raw:
        sid=profile.split('-',1)[1]
        if sid not in QUESTIONS:raise ValueError('unknown source profile')
        family=next(k for k,c in BY_FAMILY.items() if c['source_id']==sid)
        if template and template!=family:raise ValueError('profile/template mismatch')
        template=family
        if parameters is None:parameters=dict(BY_FAMILY[family]['parameters'])
        original=BY_FAMILY[family]['parameters']
        if any(rational(parameters.get(k, '0'))!=rational(v) for k,v in original.items()):
            raise ValueError('observed profiles are original-parameter evidence replay only')
    else:sid=BY_FAMILY[template]['source_id'] if template in BY_FAMILY else None
    family=template or rng.choice(FAMILIES[level])
    if family not in FAMILIES[level]:raise ValueError('family unavailable at level')
    sid=BY_FAMILY[family]['source_id'] if family in BY_FAMILY else 'e-3432'
    # Sample a whole profile before targets. Explicit targets can instead pick
    # their applicable whole profile after evaluation, before building choices.
    selected=profile or (rng.choice(LEARNER_PROFILES[family]) if parameters is None else None)
    if not raw and selected is not None and selected not in LEARNER_PROFILES[family]:
        raise ValueError('profile is not supported for this function family')
    c=d=1
    if family=='exp' and not raw:
        if parameters is None:c,d=rng.randint(1,4),rng.randint(1,4)
        else:c,d=parameters.get('c',1),parameters.get('d',1)
        if isinstance(c,bool) or isinstance(d,bool) or not isinstance(c,int) or not isinstance(d,int):raise ValueError('exponential affine coefficients must be integers')
    if parameters is not None:
        if set(parameters)-({'p','q','c','d'} if family=='exp' else {'p','q'}) or not {'p','q'}<=set(parameters):raise ValueError('p,q required; optional c,d only for exp')
        if raw and (parameters.get('c',1)!=1 or parameters.get('d',1)!=1):raise ValueError('historical exponential bank retains unit affine coefficients')
        p,q=(rational(parameters[k]) for k in ('p','q'));a,b=allowed(level,family,p,q,c,d)
        if selected is None:
            selected=('method-axis-unit' if a*a+b*b==1 else 'method-axis') if a==0 or b==0 else ('method-balanced' if family in ('log','circle') else 'method-generic')
            if family=='log' and abs(a)==abs(b)==s.Rational(1,2):
                selected='method-generic'
            if family=='bilinear' and abs(a)==abs(b)==1:
                selected='method-balanced'
    else:
        candidates=sampling_domain(level,family);rng.shuffle(candidates)
        for p,q in candidates:
            try:
                a,b=allowed(level,family,p,q,c,d)
                bank,correct=(observed_bank(family,p,q,a,b) if raw else method_bank(family,p,q,a,b,selected))
                if not raw:
                    validate_bank(bank,correct,a,b)
                break
            except ValueError:continue
        else:raise ValueError('no valid complete-bank instance')
    bank,correct=(observed_bank(family,p,q,a,b) if raw else method_bank(family,p,q,a,b,selected))
    if not raw:validate_bank(bank,correct,a,b)
    problem=prompt(family,p,q,raw,c,d)
    worked,structure=solution(family,p,q,a,b,c,d)
    source=QUESTIONS.get(sid)
    values=[]
    for i,(recipe,v) in enumerate(bank):
        if v is None:values.append('-k')
        elif i==correct:values.append(normalized_tex(a,b))
        else:values.append(choice_tex(*v))
    problem=normalize_prose(problem)
    worked=normalize_prose(worked)
    values=[normalize_tex(v) for v in values]
    outer={'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']}
    # Mathematical task fingerprints omit bank/layout aliases; exp depends only
    # on x+y, so points on the same exponent are a single assessed task.
    task={'family':family,'function':s.srepr(function_for(family,c,d)),'assessment':'any unit normal','p':str(p),'q':str(q)}
    if family=='exp':task.pop('p');task.pop('q');task['exponent']=str(p+q)
    content={'version':VERSION,'prompt':problem,'solution':None if raw and ':question/worked-solution' not in source else worked,'bank':sorted(values),'level':None if raw and ':question/difficulty' not in source else level,'field_type':'radio','correct_value':None if raw and ':answer-field/correct' not in source[':question/answer-fields'][0] else values[correct]}
    identity=digest(content);qid=uid(content);fid=uid({'q':qid,'field':'selection'})
    choices=[{':answer/id':uid({'field':fid,'value':v}),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct_id=choices[correct][':answer/id']
    rng.shuffle(choices)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct_id]}
    question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':worked,':question/answer-fields':[field]}
    if raw:
        for key in (':question/difficulty',':question/worked-solution'):
            if key not in source:question.pop(key)
        if ':answer-field/correct' not in source[':question/answer-fields'][0]:field.pop(':answer-field/correct')
    return {'knowledge_point':outer,'question':question,'generation':{
        'version':VERSION,'seed':seed,'difficulty':level,'template':family,'profile':selected,
        'parameters':dict({'p':str(p),'q':str(q)},**({'c':c,'d':d} if family=='exp' else {})),'source':{k:SOURCE[k] for k in ('database','basis','lineage')},
        'source_ids':[sid],'original_refs':copy.deepcopy(source) if raw else None,
        'evidence_only':raw,'eligible_for_learning':not raw,
        'authored_level':False,
        'answer_criterion':'any real two-dimensional unit normal; antipodal orientation accepted mathematically',
        'content_identity':identity,'mathematical_fingerprint':digest(task),
        'recipes':[k for k,v in bank],'solution_structure':structure,
        'domain':{'point':[str(p),str(q)],'level_value':str(s.simplify(function_for(family,c,d).subs({X:p,Y:q}))), 'nonzero_gradient':True},
        'runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'plots':[]}}

def prompt_original_notation(family,p,q):
    """Source prompt mask, with its complete coordinate pair as the sole slot.
    Functions are fixed in this generator, so this is parameterized source
    notation, not a literal payload replay branch.
    """
    z=QUESTIONS[BY_FAMILY[family]['source_id']][':question/problem']
    # Preserve separator spacing from each prompt, also in unrated originals.
    return re.sub(r'(\(x,\s*y\)\s*=\s*)\((.*?)\)',lambda m:m[1]+'('+tex(p)+(','+' ' if ', ' in m[2] else ',')+tex(q)+')',z,count=1)

# EASY: observed source families, familiar rational/half-integer substitution,
# square-root inputs remain familiar perfect squares. Ten source banks retained.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)

# No distinct moderate/hard difficulty evidence is supplied.
def generate_moderate(*args, **kwargs):
    raise ValueError('moderate is unsupported: all supplied questions are easy')

def generate_hard(*args, **kwargs):
    raise ValueError('hard is unsupported: all supplied questions are easy')


def markdown(record):
    q=record['question'];lines=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        for i,a in enumerate(f.get(':answer-field/choices',[])):lines.append(chr(65+i)+'. $'+a[':answer/value']+'$')
    if ':question/worked-solution' in q:lines+=['','Worked solution:',q[':question/worked-solution']]
    return '\n\n'.join(lines)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=(*LEVELS,'all'),default='easy');parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=('markdown','json'),default='json')
    parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
    if args.count<1:parser.error('--count must be positive')
    levels=LEVELS if args.difficulty=='all' else (args.difficulty,)
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(z) for z in records))
