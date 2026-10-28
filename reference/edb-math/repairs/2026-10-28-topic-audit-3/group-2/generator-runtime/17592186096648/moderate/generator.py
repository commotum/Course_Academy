#!/usr/bin/env python3
"""Seeded common-vector scalar factoring; no database or asset writes.

Adapted from the supplied 17592186096648.py. Historical evidence replay is
separate from served generation; see instructional-account.md for scope.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, math, random, sys, uuid
from pathlib import Path
import sympy as sp
from math_format import normalize_prose, normalize_tex, checked_math_content

KP_ID=17592186096648
KP_UUID='27d5c96d-ca13-5c1e-83d3-0dc9f6da0f83'
TITLE='Determining Whether Two Vectors are Parallel'
VERSION='parallel-scalar-2'
TEMPLATES=('target_first','lambda_first')
EASY_FACTORS=tuple(sp.Rational(s)*sp.Rational(x) for s in (-1,1) for x in ('2','3','4','1/2','1/3','1/4','2/3','3/2','3/4','4/3'))
RATIONAL_FACTORS=tuple(sp.Integer(s*n) for s in (-1,1) for n in sorted({p*q for p in range(2,10) for q in range(2,10) if p*q<=30 and math.gcd(p,q)==1}))
RADICANDS=(2,3,5,6,7,10,11,13)


def tex(x):
    x=sp.simplify(x)
    if x.is_Rational:
        if x.q==1:return str(x.p)
        return ('-' if x<0 else '')+r'\frac{'+str(abs(x.p))+'}{'+str(x.q)+'}'
    return sp.latex(x, order='lex')

def decimal(x):
    x=sp.Rational(x)
    if x.q==1:return str(x.p)
    if x.q not in (2,4,5):raise ValueError('only familiar terminating decimals allowed')
    return str(float(x)).rstrip('0').rstrip('.')

def lin(u,v,dec=False):
    """Complete two-term slots; never replace scalar substrings across prose."""
    fmt=decimal if dec else tex
    a=('a' if u==1 else '-a' if u==-1 else fmt(u)+'a')
    b=('b' if abs(v)==1 else fmt(abs(v))+'b')
    return a+(' + ' if v>0 else ' - ')+b

def math_key(p):
    # Normalize common scaling AND common sign of both vectors. Names/order/
    # profiles are incidental; k and base coefficient ratio retain the divisions.
    return [str(p['k']),str(p['v']/p['u'])]

def hashof(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:'+s))

# Source anchors, including the legacy decimal pair. Parameters describe
# base=u*a+v*b and target=k*base, independent of presentation order.
ANCHORS={
 'q-12135':('easy','target_first','historical-12135','1','-3','4'),
 'q-12139':('easy','lambda_first','historical-12139','-1/2','6','-2'),
 'q-20395':('easy','lambda_first','historical-20395','12','-52','-1/4'),
 'q-20398':('moderate','lambda_first','historical-20398','2/7','7/2','14'),
 'q-324233':('moderate','lambda_first','radical_blank','4','sqrt(7)','sqrt(7)'),
}


def source_data():
    return json.loads(Path(__file__).with_name('source_cases.json').read_text())


def solution(p):
    u,v,k=(p[n] for n in ('u','v','k'))
    base,target=lin(u,v),lin(sp.simplify(k*u),sp.simplify(k*v))
    # Retain the exact five-stage sequence of the current complete sources.
    return ('Since the vectors are equal, we can write\n\n$$\n'+target+r'=\lambda ('+base+').\n$$\n\n'
      'Next, we factor the left-hand side, which gives\n\n$$\n'+tex(k)+'('+base+r')=\lambda ('+base+').\n$$\n\n'
      'Notice that we have $('+base+')$ on both sides. So, let\'s define a new vector $u$ as\n\n$$\n'
      'u='+base+'.\n$$\n\nThen, our equation becomes\n\n$$\n'+tex(k)+r'\,u=\lambda u.'+'\n$$\n\n'
      'Since $u$ is non-zero,\n\n$$\n'+r'\lambda='+tex(k)+'.\n$$')


def source_replay(source_id, complete=False):
    """Exact source content, with normalization; optional documented supplements.

    Complete=False preserves omitted source attributes. Complete=True supplies
    the inferred key and factoring solution only for the two historical cases,
    for grader validation. It never invents their difficulty labels.
    """
    q=copy.deepcopy(next(q for q in source_data()['questions'] if q[':question/math-academy-id']==source_id))
    q[':question/problem']=normalize_prose(q[':question/problem'])
    if ':question/worked-solution' in q:q[':question/worked-solution']=normalize_prose(q[':question/worked-solution'])
    _,template,profile,u,v,k=ANCHORS[source_id]
    p={n:sp.sympify(x) for n,x in zip(('u','v','k'),(u,v,k))}
    for f in q[':question/answer-fields']:
        for a in f[':answer-field/choices']:
            a[':answer/value']=(normalize_tex if a[':answer/type']==':answer.type/math' else normalize_prose)(a[':answer/value'])
        if ':answer-field/correct' in f:
            f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
        elif complete:
            f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==tex(p['k']))]
    if complete and ':question/worked-solution' not in q:q[':question/worked-solution']=normalize_prose(solution(p))
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
      'generation':{'version':VERSION,'source_ids':[source_id],'source_replay':True,
       'supplemented_missing_fields':bool(complete and source_id in ('q-12135','q-12139')),
       'parameters':{n:str(x) for n,x in p.items()},'template':template,'bank_profile':profile}}


def validate_instance(level,profile,p):
    if set(p)!={'u','v','k'}:raise ValueError('parameters must be exactly u,v,k')
    u,v,k=(sp.simplify(p[n]) for n in ('u','v','k'))
    if not all(x.is_real and x!=0 for x in (u,v,k)):raise ValueError('real nonzero coefficients and factor required')
    if level=='easy' and profile=='factor_radio':
        ok=k in EASY_FACTORS and u.is_Integer and v.is_Integer and (k*u).is_Integer and (k*v).is_Integer and max(abs(u),abs(v),abs(k*u),abs(k*v))<=64
    elif level=='moderate' and profile=='rational_radio':
        ok=k in RATIONAL_FACTORS and u.is_Rational and v.is_Rational and u.q>1 and v.q>1 and abs(u*v)==1 and 2<=abs(u.p)<=9 and 2<=u.q<=9 and (k*u).is_Integer and (k*v).is_Integer and max(abs(k*u),abs(k*v))<=100
    elif level=='moderate' and profile=='radical_blank':
        ds=[d for d in RADICANDS if sp.simplify(k/sp.sqrt(d)).is_Integer and 1<=abs(k/sp.sqrt(d))<=3]
        ok=bool(ds) and u.is_Integer and 2<=u<=6 and any(sp.simplify(v/sp.sqrt(d)) in (-3,-2,-1,1,2,3) for d in ds)
    else:raise ValueError('unsupported difficulty/profile')
    if not ok:raise ValueError('parameters outside documented '+level+'/'+profile+' bounds')


def sample_instance(level,profile,rng,k=None):
    """Assign answer-bearing scalar first, then compatible coefficients."""
    if profile=='factor_radio':
        k=sp.sympify(k) if k is not None else rng.choice(EASY_FACTORS)
        d=k.q
        u=d*rng.choice((-1,1))*rng.randint(1,6)
        v=d*rng.choice((-1,1))*rng.randint(1,8)
    elif profile=='rational_radio':
        k=sp.sympify(k) if k is not None else rng.choice(RATIONAL_FACTORS)
        p,q=rng.choice([(p,q) for p in range(2,10) for q in range(2,10) if p!=q and math.gcd(p,q)==1 and abs(k)%(p*q)==0 and max(abs(k)*p/q,abs(k)*q/p)<=100])
        u=sp.Rational(rng.choice((-1,1))*p,q)
        v=sp.Rational(rng.choice((-1,1))*q,p)
    else:
        if k is None:
            d=rng.choice(RADICANDS);k=rng.choice((-3,-2,-1,1,2,3))*sp.sqrt(d)
        else:
            k=sp.sympify(k);d=next(d for d in RADICANDS if sp.simplify(k/sp.sqrt(d)).is_Integer)
        u=sp.Integer(rng.randint(2,6));v=rng.choice((-3,-2,-1,1,2,3))*sp.sqrt(d)
    return dict(u=sp.sympify(u),v=sp.sympify(v),k=sp.sympify(k))


@checked_math_content
def generate(level='easy', seed=0, template=None, field_type=None, parameters=None, profile=None, candidates=None):
    if level not in ('easy','moderate'):raise ValueError('supported difficulties: easy, moderate; hard unsupported')
    rng=random.Random(seed)
    profile=profile or ('factor_radio' if level=='easy' else rng.choice(('rational_radio','radical_blank')))
    if profile not in (('factor_radio',) if level=='easy' else ('rational_radio','radical_blank')):raise ValueError('unsupported profile for difficulty')
    template=template or rng.choice(TEMPLATES)
    if template not in TEMPLATES:raise ValueError('unknown template')
    field_kind='blank' if profile=='radical_blank' else 'radio'
    if field_type not in (None,field_kind,':answer-field.type/'+field_kind):raise ValueError('field type/profile mismatch')
    # Choose k once, before compatible-value rejection. Rejection must not
    # overweight easy small factors by resampling answer roles with coefficients.
    fixed_k=(sp.sympify(parameters['k']) if parameters is not None else
             rng.choice(EASY_FACTORS if level=='easy' else RATIONAL_FACTORS) if field_kind=='radio' else
             rng.choice((-3,-2,-1,1,2,3))*sp.sqrt(rng.choice(RADICANDS)))
    attempts=0
    while True:
        attempts+=1
        p={n:sp.sympify(x) for n,x in parameters.items()} if parameters is not None else sample_instance(level,profile,rng,fixed_k)
        try:validate_instance(level,profile,p)
        except ValueError:
            if parameters is not None:raise
            if attempts>=1000:raise RuntimeError('compatible coefficient sampling exhausted')
            continue
        break
    u,v,k=(p[n] for n in ('u','v','k'))
    base,target=lin(u,v),lin(sp.simplify(k*u),sp.simplify(k*v))
    lhs,rhs=(target,r'\lambda ('+base+')') if template=='target_first' else (r'\lambda ('+base+')',target)
    prompt='Given that $'+lhs+'$ and $'+rhs+r'$ are equal (non-zero) vectors, find the scale factor $\lambda .$'
    key='field-1' if field_kind=='blank' else 'selection'
    if field_kind=='blank':prompt+='\n\n'+r'$\lambda =$'+'\n{{field-1}}'
    values=[(':answer.type/math',tex(k))]
    if field_kind=='radio':
        pool=EASY_FACTORS if level=='easy' else RATIONAL_FACTORS
        n=4 if level=='easy' else 5
        numbers=([sp.sympify(x) for x in candidates] if candidates is not None else [k]+rng.sample([x for x in pool if x!=k],n-1))
        if len(numbers)!=n or len(set(numbers))!=n or k not in numbers or any(x not in pool for x in numbers):raise ValueError('invalid complete candidate bank')
        values=[(':answer.type/math',tex(x)) for x in numbers]
        if level=='easy':values.append((':answer.type/text',r'No such $\lambda$'))
    prompt=normalize_prose(prompt);sol=normalize_prose(solution(p))
    values=[(t,normalize_tex(v) if t==':answer.type/math' else normalize_prose(v)) for t,v in values]
    identity=hashof([VERSION,prompt,sol,sorted(values),level])
    qid=uid(identity);fid=uid(identity+':'+key)
    choices=[{':answer/id':uid(fid+':'+t+':'+value),':answer/type':t,':answer/value':value} for t,value in values]
    rng.shuffle(choices)
    correct=next(a for a in choices if a[':answer/value']==normalize_tex(tex(k)))
    f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+field_kind,
       ':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct[':answer/id']]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
      'question':{':question/id':qid,':question/problem':prompt,':question/difficulty':':question.difficulty/'+level,
                  ':question/worked-solution':sol,':question/answer-fields':[f]},
      'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,
        'parameters':{n:str(x) for n,x in p.items()},'attempts':attempts,
        'source_ids':['q-20395'] if level=='easy' else ['q-324233' if field_kind=='blank' else 'q-20398'],
        'source':{'database':'math','basis':4478,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},
        'mathematical_fingerprint':hashof([str(sp.simplify(k)),str(sp.simplify(v/u))]),
        'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}


def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=('easy','moderate','hard'),default='easy')
    ap.add_argument('--count',type=int,default=1)
    ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=('json',),default='json')
    ns=ap.parse_args()
    if ns.count<1:ap.error('--count must be positive')
    try:records=[generate(ns.difficulty,ns.seed+i) for i in range(ns.count)]
    except ValueError as exc:ap.error(str(exc))
    print(json.dumps(records,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
