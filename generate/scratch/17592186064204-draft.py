#!/usr/bin/env python3
"""Frozen, review-only negative affine-power integration generator (docs 3–7).

Observed templates parameterize the entire affine factor only, retaining complete
banks and source-specific solution rows. Authored defaults sample numerator,
slope, intercept and exponent within documented equal-level workload bounds.
"""
import argparse
import hashlib
import importlib.util
import itertools
import json
import random
import uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186064204
KP_UUID='387d85df-b839-5837-89b9-5e4bb4daa073'
TITLE='Integrating an Algebraic Function With Negative Integer Exponent'
VERSION='negative-affine-draft-v2'
HERE=Path(__file__).with_suffix('')
def private(name):
    spec=importlib.util.spec_from_file_location('kp64204_private_'+name,HERE/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
fmt=private('math_format')
PROFILES=json.loads((HERE/'templates.json').read_text())
LEVELS=('easy','moderate','hard')
x=sp.Symbol('x',real=True)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def integer(value,name):
    if type(value) is not int:raise TypeError(name+' must be a built-in int (bool is invalid)')
def affine(a,b):
    if a<0:return str(b)+('-x' if a==-1 else str(a)+'x')
    return ('x' if a==1 else str(a)+'x')+('+' if b>0 else '')+str(b)
def fingerprint(p):
    n,a,b,m=p
    return digest(['rational-integrand',str(sp.Rational(n,a**m)),str(sp.Rational(b,a)),m])
def valid(level,p):
    n,a,b,m=p
    if not (1<=abs(b)<=12 and 3<=m<=7):return False
    if level=='easy':return n in (1,2,3) and a in (2,3,4,5)
    if level=='moderate':return n in (1,2,3,4) and a in (-2,-3,-4,-5)
    return n in (-2,-3,-4,-5) and a in (-2,-3,-4,-5,-6,-7) and sp.gcd(n,a)==1

def primitive_tex(c,L,k):
    c=sp.Rational(c);sign='-' if c<0 else '';c=abs(c)
    numerator=str(c.p);denominator=('' if c.q==1 else str(c.q))+f'({L})^{{{k}}}'
    return sign+rf'\frac{{{numerator}}}{{{denominator}}}+C'

def authored(p):
    n,a,b,m=p;L=affine(a,b);k=m-1;c=sp.Rational(n,a*(1-m));na=sp.Rational(n,a)
    z=lambda v:'('+sp.latex(v)+')'
    cn='' if n==1 else str(n)
    I=rf'\int {cn}({L})^{{-{m}}}\,\text{{d}}x'
    problem=rf'Calculate the integral $\int \frac{{{n}}}{{({L})^{{{m}}}}}\,\text{{d}}x.$'
    bank=[primitive_tex(c,L,k),primitive_tex(-c,L,k),primitive_tex(c*a,L,k),primitive_tex(sp.Rational(n,a*(-m-1)),L,m+1),primitive_tex(c*a*a,L,k)]
    if abs(a)>1 and len(set(bank))!=5:raise ValueError('Complete bank collision')
    final=bank[0]
    rows=[I+rf' & ={z(n)}\int {{u}}^{{-{m}}}\cdot {z(sp.Rational(1,a))}\,\text{{d}}u',
          rf' & ={z(n)}\cdot {z(sp.Rational(1,a))}\int {{u}}^{{-{m}}}\,\text{{d}}u',
          rf' & ={z(na)}\int {{u}}^{{-{m}}}\,\text{{d}}u',
          rf' & ={z(na)}\cdot \frac{{{{u}}^{{-{k}}}}}{{(-{k})}}+C',
          rf' & ={z(c)}({L})^{{-{k}}}+C',rf' & ={final}']
    D=r'\frac{\text{d}}{\text{d}x}'
    check=[D+rf'[{final}] & ={D}[{final[:-2]}]+{D}(C)',
           rf' & ={z(c)}{D}[({L})^{{-{k}}}]+{D}(C)',
           rf' & ={z(c)}\cdot (-{k})\cdot ({L})^{{-{m}}}\cdot {D}({L})+0',
           rf' & ={z(c)}\cdot (-{k})\cdot ({L})^{{-{m}}}\cdot {z(a)}',
           rf' & =\frac{{{n}}}{{({L})^{{{m}}}}}\,✓']
    aligned=lambda rs:r'\begin{aligned}'+r' \\ '.join(rs)+r'\end{aligned}'
    solution=('First, we rewrite the integral as\n\n$$\n'+I+'.\n$$\n\n'+rf'Let $u={L}.$ Then differentiating with respect to $x$ gives'+'\n\n$$\n'+rf'\frac{{\text{{d}}u}}{{\text{{d}}x}}={a}\,⟹\,\text{{d}}x={sp.latex(sp.Rational(1,a))}\text{{d}}u.'+'\n$$\n\n'+'We now write our integral in terms of $u,$ calculate the integral as normal, and write the final answer in terms of $x$ at the very end:\n\n$$\n'+aligned(rows)+"\n$$\n\nLet's double-check that our result is correct. If we differentiate the result, then it should come out to the original integrand:\n\n$$\n"+aligned(check)+'\n$$')
    return problem,solution,bank,0

@fmt.checked_math_content
def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None,**kwargs):
    if kwargs:raise TypeError('Unexpected arguments: '+str(list(kwargs)))
    integer(seed,'seed')
    if level not in LEVELS:raise ValueError('Unsupported level')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only source radio field is supported')
    if template is not None and type(template) is not str:raise TypeError('template must be string')
    if profile is not None and type(profile) is not str:raise TypeError('profile must be string')
    sid=profile or template or 'authored'
    if template is not None and profile is not None and template!=profile:raise ValueError('template/profile mismatch')
    rng=random.Random(seed)
    if parameters is not None:
        if type(parameters) not in (list,tuple) or len(parameters)!=4:raise TypeError('parameters must contain four built-in ints')
        for v in parameters:integer(v,'parameter')
        p=list(parameters)
    else:p=None
    raw=sid=='q-12499-raw'
    if sid in PROFILES:
        t=PROFILES[sid]
        if t['level']!=level:raise ValueError('Source level mismatch')
        if p is None:p=list(t['parameters']);p[2]=rng.randint(*t['bounds'])
        n,a,b,m=p;pn,pa,pb,pm=t['parameters']
        if (n,a,m)!=(pn,pa,pm) or not t['bounds'][0]<=b<=t['bounds'][1]:raise ValueError('Outside source slots')
        render=lambda text:text.replace('@@L@@',affine(a,b))
        prompt,solution=render(t['prompt']),render(t['solution'])
        values=[render(o['mask']) for o in t['bank']];ci=next(i for i,o in enumerate(t['bank']) if o['correct']);role=t['role'];sources=[t['source_id']];correction=t['source_correction']
    elif sid in ('authored','q-12499','q-12499-raw'):
        if sid!='authored':
            if level!='easy':raise ValueError('Unrated legacy receives authored easy assignment')
            if p is None:p=[1,1,-3,8]
            if p[:2]!=[1,1] or p[3]!=8 or not -12<=p[2]<=-1:raise ValueError('Outside legacy affine-slot domain')
        else:
            if p is None:
                options=domain(level);p=list(rng.choice(options))
            if not valid(level,p):raise ValueError('Outside authored level bounds')
        prompt,solution,values,ci=authored(p) if sid=='authored' else legacy(p,raw)
        role='authored' if sid=='authored' else 'legacy-evidence' if raw else 'legacy-repair';sources=[] if sid=='authored' else ['q-12499'];correction=None
    else:raise ValueError('Unknown template/profile')
    prompt=fmt.normalize_prose(prompt);solution=fmt.normalize_prose(solution);values=[fmt.normalize_tex(v) for v in values]
    # Content IDs exclude seed, ordering, and aliases. Field owns each answer.
    qid=ident([VERSION,level,prompt,solution,sorted(values)]);fid=ident([qid,'selection'])
    choices=[{':answer/id':ident([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for i,v in enumerate(values)]
    correct=choices[ci][':answer/id'];order=random.Random(digest(['option-order',seed,qid]));choices.sort(key=lambda answer:answer[':answer/value']);order.shuffle(choices)
    q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
    n,a,b,m=p
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':sid,'parameters':p,'field_type':'radio','role':role,'source_ids':sources,'source_basis':2275,'source_lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','mathematical_fingerprint':fingerprint(p),'domain':f'x real; x != {sp.Rational(-b,a)}; separate primitive family on each connected interval','source_correction':correction,'option_shuffle':'independent SHA-derived RNG','dependency_versions':{'sympy':sp.__version__},'raw_ambiguous_evidence':raw,'evidence_only':raw,'eligible_for_learning':not raw}}

def legacy(p,raw):
    # Preserve the legacy full mathematical bank through the public API. Normal
    # repair changes only the two modulo-C duplicates, and authors absent solution.
    n,a,b,m=p;L=affine(a,b)
    # Source shape, without malformed capture spacing/displaystyle wrappers.
    prompt=rf'Calculate $\int(1)/(({L})^{{8}})dx$.'
    _,solution,_,_=authored([1,1,b,8])
    values=[primitive_tex(-sp.Rational(1,7),L,7),primitive_tex(sp.Rational(1,7),L,7),primitive_tex(-sp.Rational(1,7),L,7)[:-2],primitive_tex(sp.Rational(1,9),L,9)[:-2],primitive_tex(sp.Rational(1,9),L,9)]
    if not raw:values[2]=primitive_tex(-1,L,7);values[3]=primitive_tex(-sp.Rational(1,9),L,9)
    return prompt,solution,values,0

_DOMAINS={}
def domain(level):
    if level not in _DOMAINS:
        ns={'easy':(1,2,3),'moderate':(1,2,3,4),'hard':(-2,-3,-4,-5)}[level];aa={'easy':(2,3,4,5),'moderate':(-2,-3,-4,-5),'hard':(-2,-3,-4,-5,-6,-7)}[level]
        _DOMAINS[level]=[p for p in itertools.product(ns,aa,(*range(-12,0),*range(1,13)),range(3,8)) if valid(level,p)]
    return _DOMAINS[level]
def batch(level,count=3,seed=0,template=None,profile=None):
    integer(seed,'seed');integer(count,'count')
    if count<1:raise ValueError('count must be positive')
    if level not in LEVELS:raise ValueError('Unsupported level')
    sid=profile or template or 'authored'
    if template and profile and template!=profile:raise ValueError('template/profile mismatch')
    if sid=='authored':pool=domain(level)
    elif sid in PROFILES:
        t=PROFILES[sid]
        if t['level']!=level:raise ValueError('Source level mismatch')
        pool=[(t['parameters'][0],t['parameters'][1],b,t['parameters'][3]) for b in range(t['bounds'][0],t['bounds'][1]+1)]
    elif sid in ('q-12499','q-12499-raw'):
        if level!='easy':raise ValueError('Legacy level mismatch')
        pool=[(1,1,b,8) for b in range(-12,0)]
    else:raise ValueError('Unknown profile')
    # Domain is finite and deduplication uses the actual rational integrand.
    unique={fingerprint(p):p for p in pool}
    if count>len(unique):raise ValueError(f'count exceeds finite capacity {len(unique)}')
    candidates=list(unique.values());random.Random(seed).shuffle(candidates)
    return [generate(level,seed,template=sid,parameters=p) for p in candidates[:count]]
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
    q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');p.add_argument('--count',type=int,default=3);p.add_argument('--seed',type=int,default=0);p.add_argument('--template');p.add_argument('--profile');p.add_argument('--format',choices=('json','markdown'),default='json');args=p.parse_args()
    records=[r for level in (LEVELS if args.difficulty=='all' else [args.difficulty]) for r in batch(level,args.count,args.seed,args.template,args.profile)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
