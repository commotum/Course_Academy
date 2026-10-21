#!/usr/bin/env python3
"""Seeded dependent-linear-system questions; portable, no database or assets.

Normal radio banks are target-first affine comparison grids. Historical banks
and complete source alternatives are retained by replay_source. Exact rational
arithmetic and the lesson's elimination / isolation / family stages are shared.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, math, random, sys, uuid
sys.dont_write_bytecode=True
import sympy as sp
from pathlib import Path
from math_format import system_tex, normalize_prose, normalize_tex, checked_math_content
KP_ID=17592186073778
KP_UUID='50351666-c691-510f-863c-168c61f9980b'
TITLE='Finding the General Solution to a System With Infinitely Many Intersection Points'
VERSION='dependent-general-family-3'
GENERATOR_UUID='d5afc560-f76b-53cb-8503-781e13a207d4'
LEVELS=('easy','moderate','hard')
TEMPLATES=('radio_family','blank_coordinate')
PROFILES=('method','raw_25524','raw_208832')
X=sp.Symbol('x')
SOURCE={'database':'math','basis':4673,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
def ident(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,x))
def tex(v):return sp.latex(sp.Rational(v))
def poly(terms):
    out=''
    for coeff,var in terms:
        coeff=sp.Rational(coeff)
        if not coeff:continue
        term=('' if abs(coeff)==1 and var else tex(abs(coeff)))+var
        out+=('-' if coeff<0 else '')+term if not out else (' - ' if coeff<0 else ' + ')+term
    return out or '0'
def lhs(a,b):return poly(((a,'x'),(b,'y')))
def aff(m,k,var='x',constant_first=False):return poly(((k,''),(m,var))) if constant_first else poly(((m,var),(k,'')))
def aligned(rows):return '$$\n'+r'\begin{aligned}'+'\n'+' \\\\\n'.join(rows)+'\n'+r'\end{aligned}'+'\n$$'
def rows(p):
    a,b,c,r=(sp.Rational(p[k]) for k in ('a','b','c','r'))
    return [(a,b,c),(r*a,r*b,r*c)]
def parameters(p):
    if set(p)-{'a','b','c','r','variable'} or not all(k in p for k in ('a','b','c','r')):raise ValueError('Require a,b,c,r; optional variable x/t/u')
    out={k:str(sp.Rational(p[k])) for k in ('a','b','c','r')}
    out['variable']=p.get('variable','x')
    if out['variable'] not in ('x','t','u'):raise ValueError('Unknown parameter alias')
    return out

def guard(level,p,raw=False):
    a,b,c,r=(sp.Rational(p[k]) for k in ('a','b','c','r'))
    if not all((a,b,c,r)) or not all(v.q==1 for row in rows(p) for v in row):raise ValueError('Nonzero coefficients/constant and integral displayed equations required')
    if max(abs(v) for row in rows(p) for v in row[:2])>24 or max(abs(row[2]) for row in rows(p))>36:raise ValueError('Displayed coefficient <=24 and constant <=36')
    if abs(r) not in (sp.Rational(1,4),sp.Rational(1,3),sp.Rational(1,2),1,2,3,4):raise ValueError('Source-grounded row multiplier')
    m,k=-a/b,c/b
    # Apply level claims to the reduced mathematical object, never hidden GCFs.
    if level=='easy':
        if m.q!=1 or k.q!=1 or not 2<=abs(m)<=6 or not 1<=abs(k)<=8:raise ValueError('Easy integral slope2..6/intercept1..8')
    elif level=='moderate':
        if (m.q>1)+(k.q>1)!=1 or max(m.q,k.q)>4 or max(abs(m),abs(k))>8:raise ValueError('Moderate exactly one fractional term, denominator2..4, magnitude<=8')
    elif level=='hard':
        if not(3<=m.q<=6 and 3<=k.q<=6 and max(abs(m),abs(k))<=8):raise ValueError('Hard both fractional terms, reduced denominators3..6, magnitude<=8')
    else:raise ValueError('Unknown difficulty')
    return m,k

def prompt(p,template,raw=False):
    eq=[lhs(a,b)+' &= '+tex(c) for a,b,c in rows(p)]
    display='$$\n'+r'\begin{aligned}'+'\n'+(' '+chr(92)*2+'[6pt]\n').join(eq)+'\n'+r'\end{aligned}'+'\n$$'
    if template=='radio_family':
        return 'Find all points of intersection of the following lines:\n\n'+display
    return ('Describe the points that lie on the intersection of the following lines:\n\n'+display+
            '\n\nExpress your answer in terms of $x$ only.\n\nThe intersection points are\n\n'+
            '$(x,$ {{field-1}} $),$\n\nwhere $x$ is any number.')

def solution(p):
    (a,b,c),(d,e,f)=rows(p);r=d/a;var=p['variable'];m,k=-a/b,c/b
    eq=[lhs(a,b)+' = '+tex(c),lhs(d,e)+' = '+tex(f)]
    out='The points of intersection of the lines correspond to the solutions of the following system:\n\n$$\n'+system_tex(eq)+'\n$$\n\n'
    out+=f'We will solve the system using elimination. Notice that if we multiply the first equation by ${tex(-r)}$, then we will get a ${poly(((-d,"x"),))}$ term that can cancel with the ${poly(((d,"x"),))}$ term in the second equation:\n\n'
    out+='$$\n'+system_tex([eq[0]+r' && \mid \cdot ('+tex(-r)+')',eq[1]])+'\n$$\n\n'
    out+='When we add the two equations, it turns out that both variables cancel, and we obtain a true statement:\n\n'
    sumtex=tex(-r*c)+(' + ' if f>=0 else ' - ')+tex(abs(f))
    out+=aligned([lhs(-d,-e)+' &= '+tex(-f),lhs(d,e)+' &= '+tex(f),'0 &= ('+sumtex+')','0 &= 0'])
    out+='\n\nBecause we obtained a true statement, we conclude that there are infinitely many solutions to the system. Therefore, the lines have infinitely many intersection points.\n\n'
    out+='We want to find an expression that represents every solution to the system. Any value of $x$ can be chosen, and we can find the corresponding $y$-coordinate for each $x$-coordinate by solving one of the lines for $y$, as follows:\n\n'
    numerator=poly(((c,''),(-a,'x')))
    out+=aligned([lhs(a,b)+' &= '+tex(c),poly(((b,'y'),))+' &= '+numerator,'y &= '+r'\frac{'+numerator+'}{'+tex(b)+'}','y &= '+aff(m,k,constant_first=True)])
    if var!='x':out+=f'\n\nLet ${var}=x$ be the free coordinate.'
    out+='\n\nTherefore, the points of intersection are\n\n$$\n'+r'\left('+var+','+aff(m,k,var,True)+r' \right)'+'\n$$\n\n'+f'where ${var}$ is any number.'
    return out

def bank(p,profile):
    a,b,c,r=(sp.Rational(p[k]) for k in ('a','b','c','r'));m,k=-a/b,c/b;v=p['variable']
    if profile=='raw_25524':
        # Exact structural historical pattern; interpretations deliberately opaque.
        return [f'({v}, '+aff(k,-m,v)+')',f'({v}, '+aff(1,k,v)+')',f'({v}, '+aff(m,k,v)+')',f'({v}, '+aff(1,m,v)+')',f'({v}, '+aff(m,-k,v)+')'],['swap_slope_intercept_negate','unit_slope','correct','unit_slope_swap_intercept','negate_intercept']
    return [f'({v}, '+aff(mm,kk,v)+')' for mm,kk in [(m,k),(-m,k),(m,-k),(-b/a,c/a),(0,k)]],['correct','move_x_without_sign_change','negate_constant','isolate_x_but_use_as_y','drop_x_term']

def canonical_family(pair):
    """Affine image signature, invariant to nonzero parameter rescale and shift."""
    xx,yy=map(sp.expand,pair);symbols=xx.free_symbols|yy.free_symbols
    if len(symbols)>1:raise ValueError('One free parameter required')
    z=next(iter(symbols),X)
    dx,dy=sp.diff(xx,z),sp.diff(yy,z)
    if dx.has(z) or dy.has(z) or (dx==0 and dy==0):return ('point',str(xx),str(yy)) if not symbols else ('non_affine',str(xx),str(yy))
    normal=sp.Matrix([dy,-dx,-dy*xx.subs(z,0)+dx*yy.subs(z,0)])
    pivot=next(v for v in normal if v!=0)
    return tuple(str(sp.simplify(v/pivot)) for v in normal)

def fingerprint(p,template=None):
    a,b,c,_=(sp.Rational(p[k]) for k in ('a','b','c','r'))
    return digest({'line':tuple(str(v/a) for v in (a,b,c)),'assessed':'complete_general_family'})

def sample(level,rng,profile):
    for _ in range(10000):
        if level=='easy':b=rng.choice([-1,1]);a=rng.choice([-6,-5,-4,-3,-2,2,3,4,5,6]);c=rng.choice([i for i in range(-8,9) if i])
        else:
            b=rng.choice([-1,1])*rng.randint(2,4 if level=='moderate' else 6)
            a=rng.choice([i for i in range(-12,13) if i]);c=rng.choice([i for i in range(-12,13) if i])
        r=rng.choice([-4,-3,-2,2,3,4]);p=parameters(dict(a=a,b=b,c=c,r=r,variable=rng.choice(['x','t','u'])))
        try:guard(level,p);eligible_bank(p,profile)
        except ValueError:continue
        return p
    raise ValueError('No eligible whole instance in bounded sampler')

def eligible_bank(p,profile):
    vals,recipes=bank(p,profile)
    if profile.startswith('raw_'):return vals,recipes
    a,b,c,r=(sp.Rational(p[k]) for k in ('a','b','c','r'));m,k=-a/b,c/b
    objects=[(X,mm*X+kk) for mm,kk in [(m,k),(-m,k),(m,-k),(-b/a,c/a),(0,k)]]
    signatures=[canonical_family(v) for v in objects]
    if len(set(signatures))!=5:raise ValueError('Whole bank has equivalent affine families')
    target=canonical_family((X,m*X+k))
    if signatures.count(target)!=1:raise ValueError('Whole bank ambiguous')
    return vals,recipes


def sample_instance(level,rng,template):
    """Choose rule/target roles first. Every bank member is eligible as target.

    No target-dependent rejection: all five must support an integer row ratio
    with magnitude >=2 before numerical data are accepted.
    """
    case=rng.choice(('slope','intercept')) if level=='moderate' else level
    missing=rng.randrange(6)
    target=rng.randrange(5)
    bsign=rng.choice((-1,1)); rsign=rng.choice((-1,1))
    rejected=0
    while True:
        d=1 if level=='easy' else rng.randint(2,4) if level=='moderate' else rng.randint(3,6)
        slope_signs=[rng.choice((-1,1)) for _ in range(2)]
        intercept_signs=[rng.choice((-1,1)) for _ in range(3)]
        if level=='easy':
            ms=[sp.Rational(s*rng.randint(2,6)) for s in slope_signs]
            ks=[sp.Rational(s*rng.randint(1,8)) for s in intercept_signs]
        elif case=='intercept':
            ms=[sp.Rational(s*rng.randint(2,3)) for s in slope_signs]
            ns=[n for n in range(1,13) if n%d]
            ks=[sp.Rational(s*rng.choice(ns),d) for s in intercept_signs]
        else:
            ns=[n for n in range(1,13) if n%d and (level!='hard' or math.gcd(n,d)==1)]
            ms=[sp.Rational(s*rng.choice(ns),d) for s in slope_signs]
            ks=([sp.Rational(s*rng.randint(1,4)) for s in intercept_signs] if level=='moderate'
                else [sp.Rational(s*rng.choice(ns),d) for s in intercept_signs])
        pairs=[(m,k) for m in ms for k in ks]
        if len(set(ms))!=2 or len(set(ks))!=3:
            rejected+=1;continue
        pairs=[pair for i,pair in enumerate(pairs) if i!=missing]
        params=[];valid=True
        for m,k in pairs:
            b=bsign*sp.ilcm(m.q,k.q);a=-m*b;c=k*b
            p=parameters(dict(a=a,b=b,c=c,r=2*rsign,variable='x'))
            try:guard(level,p)
            except ValueError:valid=False;break
            params.append(p)
        if not valid:
            rejected+=1;continue
        p=params[target]
        ratios=[]
        for r in (2*rsign,3*rsign,4*rsign):
            q=dict(p,r=str(r))
            try:guard(level,q);ratios.append(r)
            except ValueError:pass
        p['r']=str(rng.choice(ratios))
        return p,pairs,target,{'fractional_case':case,'missing_grid_slot':missing,
                             'target_grid_slot':target,'numeric_rejections':rejected}

@checked_math_content
def build_record(level,p,template,pairs,target,seed,details):
    m,k=guard(level,p)
    kind='radio' if template=='radio_family' else 'blank'
    problem=normalize_prose(prompt(p,template));worked=normalize_prose(solution(p))
    values=([f'(x, {aff(mm,kk)})' for mm,kk in pairs] if kind=='radio' else [aff(m,k)])
    values=[normalize_tex(v) for v in values]
    correct=values[target] if kind=='radio' else values[0]
    content=digest({'version':VERSION,'prompt':problem,'solution':worked,
                    'values':sorted(values),'correct':correct,'kind':kind,'difficulty':level})
    qid=ident(content);fid=ident(qid+':'+kind)
    answers=[{':answer/id':ident(fid+':'+value),':answer/type':':answer.type/math',
              ':answer/value':value} for value in values]
    answer_id=next(a[':answer/id'] for a in answers if a[':answer/value']==correct)
    if kind=='radio':random.Random(str(seed)+':presentation').shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection' if kind=='radio' else 'field-1',
           ':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,
           ':answer-field/correct':[':answer/id',answer_id]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
            'question':{':question/id':qid,':question/problem':problem,
                        ':question/answer-fields':[field],':question/difficulty':':question.difficulty/'+level,
                        ':question/worked-solution':worked},
            'generation':{'version':VERSION,'seed':seed,'template':template,
                          'bank_profile':'affine_grid' if kind=='radio' else 'coordinate',
                          'parameters':p,'parameter_fingerprint':fingerprint(p),
                          'source':SOURCE,'source_ids':['q-25524' if kind=='radio' else 'q-208832'],
                          'method_reference':'e-14014; tutorial9684','authored_extension':True,
                          'domain':'x is any real number','python_version':sys.version.split()[0],
                          'sympy_version':sp.__version__,'plot_rating':'none','plot_assets':{},
                          'candidate_pairs':[[str(m),str(k)] for m,k in pairs] if kind=='radio' else [],
                          **details}}

@checked_math_content
def generate(level,seed=0,template=None):
    if level not in LEVELS:raise ValueError('Unsupported difficulty')
    rng=random.Random(seed);template=template or rng.choice(TEMPLATES)
    if template not in TEMPLATES:raise ValueError('Unknown template')
    p,pairs,target,details=sample_instance(level,rng,template)
    return build_record(level,p,template,pairs,target,seed,details)

def source_cases():
    return json.loads(Path(__file__).with_name('source-cases.json').read_text())

def _public(value):
    if isinstance(value,dict):
        if set(value)=={':db/ident'}:return value[':db/ident']
        return {k:_public(v) for k,v in value.items() if k!=':db/id'}
    if isinstance(value,list):return [_public(v) for v in value]
    return value

@checked_math_content
def replay_source(source_id):
    """Replay captured content, repairing only explicitly documented defects."""
    case=next(c for c in source_cases() if source_id in (c['id'],c.get('ma_id')))
    q=_public(copy.deepcopy(case['question']));p=case['parameters']
    q[':question/problem']=normalize_prose(q[':question/problem'])
    q[':question/worked-solution']=normalize_prose(q.get(':question/worked-solution') or solution(p))
    if ':question/answer-fields' not in q: # canonical example has no response capture
        built=build_record(case['inferred_band'],p,'blank_coordinate',[],0,0,{})
        q[':question/answer-fields']=built['question'][':question/answer-fields']
        q[':question/problem']+='\n\nThe intersection points are $(x,$ {{field-1}} $),$ where $x$ is any number.'
    f=q[':question/answer-fields'][0];m,k=-sp.Rational(p['a'])/sp.Rational(p['b']),sp.Rational(p['c'])/sp.Rational(p['b'])
    if ':answer-field/choices' not in f:
        val=normalize_tex(aff(m,k));aid=ident(f[':answer-field/id']+':'+val)
        f[':answer-field/choices']=[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':val}]
    # Known source error: t is not the requested variable x. Keep its evidence in source-cases.json.
    if case['id']=='f2d5e6d3-70ba-56f0-872c-ec4406eeabb5':
        f[':answer-field/choices']=[a for a in f[':answer-field/choices'] if a[':answer/value']!=r'\frac{10-7t}{2}']
    for a in f[':answer-field/choices']:a[':answer/value']=normalize_tex(a[':answer/value'])
    if ':answer-field/correct' not in f:
        if f[':answer-field/type'].endswith('/radio'):
            wanted=normalize_tex(f'(x, {aff(m,k)})')
            chosen=next(a for a in f[':answer-field/choices'] if a[':answer/value']==wanted)
        else:chosen=f[':answer-field/choices'][0]
        f[':answer-field/correct']=[':answer/id',chosen[':answer/id']]
    elif isinstance(f[':answer-field/correct'],dict):
        f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
    q.setdefault(':question/difficulty',':question.difficulty/'+case['inferred_band'])
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
            'generation':{'version':VERSION,'source_replay':case['id'],'parameters':p,
                          'original_difficulty':case['question'].get(':question/difficulty'),
                          'repairs':case['repairs'],'source':SOURCE}}

def main():
    ap=argparse.ArgumentParser(description='Dependent equations: complete affine solution family.')
    ap.add_argument('--difficulty',choices=LEVELS,default='moderate')
    ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1)
    ap.add_argument('--format',choices=('json',),default='json')
    ap.add_argument('--template',choices=TEMPLATES);ap.add_argument('--replay-source')
    args=ap.parse_args()
    if args.count<1:ap.error('Positive count required')
    records=([replay_source(args.replay_source)] if args.replay_source else
             [generate(args.difficulty,args.seed+i,args.template) for i in range(args.count)])
    print(json.dumps(records,indent=2))
if __name__=='__main__':main()
