#!/usr/bin/env python3
"""Finite half-open endpoint translation; frozen basis2275, no database operations.

Five MA originals comprise two unrated raw captures and three rated profiles.
Raw profiles preserve missing assessment fields; completed profiles derive a key
and canonical-anchored solution. Normal workload is signed integer / exact
rational / signed surd reading, always the same two endpoint decisions. No
solving, graphs, unions, or unbounded tasks are added. The observed unbounded
option is retained as a distractor in its complete bank profile.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid, importlib.util, copy, functools
from pathlib import Path
import sympy as sp
KP_ID=17592186059827
KP_UUID='bdf77469-6c2a-5339-b216-3bc5e2316e4d'
TITLE='Translating Between Half-Open Intervals and Inequalities'
VERSION='half-open-v6-portable'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
ROOT=Path(__file__).resolve().parent
TEMPLATES=('inequality_to_interval','interval_to_inequality')
LEVELS=('easy','moderate','hard')
NS=uuid.UUID(KP_UUID)
SOURCE={'database':'math','basis':4467,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
OPENING=("Every interval can be expressed as an inequality. We use the following notations:\n\n"
 r"- Parentheses ${\color{red}{(}}\phantom{0} \phantom{0}{\color{red}{)}}$ to indicate that the endpoints are *not* included."+"\n"+
 r"- Brackets ${\color{blue}{[}}\phantom{0}\phantom{0}{\color{blue}{]}}$ to indicate that the endpoints *are* included.")

import math_format as fmt
def checked_public_math_content(fn):
    @functools.wraps(fn)
    def checked(*args,**kwargs):
        record=fn(*args,**kwargs)
        if record['generation']['raw_missing_fields_preserved']:
            # Validate the captured omission without inventing a served solution.
            probe=copy.deepcopy(record);probe['question'][':question/worked-solution']=''
            fmt.checked_math_content(lambda r:r)(probe)
            record['generation']['math_format']=fmt.FORMAT_VERSION
            return record
        return fmt.checked_math_content(lambda r:r)(record)
    return checked

PROFILES={
    'inequality_to_interval':('reversed_endpoints','unbounded_upper','reflected_interval'),
    'interval_to_inequality':('reflected_inequality','sign_omission'),
}
OBSERVED={'observed_1253':'reversed_endpoints','observed_1253_raw':'reversed_endpoints',
          'observed_25754':'sign_omission','observed_25754_raw':'sign_omission',
          'observed_28834':'unbounded_upper','observed_73902':'reflected_inequality',
          'observed_102205':'reflected_interval'}

def recipe(profile):return OBSERVED.get(profile,profile)
def compatible(a,b,profile):
    p=recipe(profile)
    return not ((p in ('reflected_interval','reflected_inequality') and a==-b)
                or (p=='sign_omission' and a==0))

def mathematical_bank(a,b,c,t,p):
    def span(x,y,lc,rc):return sp.EmptySet if x>y else sp.Interval(x,y,left_open=not lc,right_open=not rc)
    base=[span(a,b,lc,rc) for lc,rc in ((False,False),(True,False),(True,True),(False,True))]
    name=recipe(p)
    if name=='unbounded_upper':extra=span(a,sp.oo,True,False)
    elif name=='reflected_inequality':extra=span(-b,-a,False,True)
    elif name=='reflected_interval':extra=span(-b,-a,True,False)
    elif name=='sign_omission':extra=span(-a,b,True,False)
    else:extra=span(b,a,False,True)
    return base+[extra]

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(NS,x))
@functools.lru_cache(maxsize=2048)
def expr(s):
    try:e=sp.sympify(str(s))
    except Exception as exc:raise ValueError('Invalid endpoint') from exc
    if e.free_symbols or e.is_real is not True or not e.is_finite:raise ValueError('Endpoints must be finite exact real numbers')
    if e.has(sp.Float):raise ValueError('Use exact endpoints')
    return e

def tex(e):return sp.latex(e).replace(r' \sqrt',r'\sqrt')
def inequality(a,b,v,c):return f'{tex(a)} '+(r'\le' if c else '<')+f' {v} '+('<' if c else r'\le')+f' {tex(b)}'
def interval(a,b,v,c):return f'{v} ∈ '+('[' if c else '(')+f'{tex(a)}, {tex(b)}'+(')' if c else ']')
def bank(a,b,v,c,t,p):
    # Select one complete profile. Extra inclusion signs do not depend on c.
    p=recipe(p)
    if t=='inequality_to_interval':
        base=[f'{v}\\in ({tex(a)}, {tex(b)})', interval(a,b,v,True),
              f'{v}\\in [{tex(a)}, {tex(b)}]', interval(a,b,v,False)]
        if p=='unbounded_upper':extra=f'{v}\\in [{tex(a)}, \\infty)'
        elif p=='reflected_interval':extra=interval(-b,-a,v,True)
        else:extra=interval(b,a,v,False)
    else:
        base=[f'{tex(a)} < {v} < {tex(b)}',inequality(a,b,v,True),
              f'{tex(a)} \\le {v} \\le {tex(b)}',inequality(a,b,v,False)]
        extra=inequality(-a,b,v,True) if p=='sign_omission' else inequality(-b,-a,v,False)
    return base+[extra]

def guard(level,p,observed=False):
    if set(p)!={'a','b','variable','left_closed'}:raise ValueError('Exact parameter keys: a,b,variable,left_closed')
    a,b=expr(p['a']),expr(p['b'])
    if a>=b or p['variable'] not in ('x','y','t','u') or type(p['left_closed']) is not bool:raise ValueError('Ordered endpoints, supported variable, and Boolean inclusion required')
    if observed:
        if abs(a)>20 or abs(b)>20:raise ValueError('Replay bounds |endpoint|<=20')
    elif level=='easy':
        if not (a.is_Integer and b.is_Integer and -15<=a<b<=15):raise ValueError('Easy: signed integers -15..15')
    elif level=='moderate':
        if not (a.is_Rational and b.is_Rational and a<0 and abs(a)<=10 and abs(b)<=10 and a.q<=5 and b.q<=5):raise ValueError('Moderate: signed rational endpoints; denominator<=5, magnitude<=10')
    else:
        if a.is_Rational or b.is_Rational:
            irrational=b if a.is_Rational else a
            if not irrational.has(sp.Pow) or irrational.is_Rational is True:raise ValueError('Hard: nonrational square-root endpoint required')
        for e in (a,b):
            if abs(e)>15 or not(e.is_Integer or e**2 in [sp.Integer(i) for i in range(1,145)]):raise ValueError('Hard: integer or coefficient-times-small-square-root endpoints, magnitude<=15')
        if a>=0:raise ValueError('Hard: signed endpoint required')
    return a,b

def catalog(level):
    if level=='easy':pairs=[(sp.Integer(a),sp.Integer(b)) for a in range(-15,15) for b in range(a+1,16)]
    elif level=='moderate':
        vals=sorted({sp.Rational(n,d) for d in range(1,6) for n in range(-15,16) if abs(sp.Rational(n,d))<=10})
        pairs=[(a,b) for a in vals for b in vals if a<0 and a<b]
    else:
        vals=sorted(set([sp.Integer(i) for i in range(-8,9)]+[s*k*sp.sqrt(n) for s in (-1,1) for k in (1,2,3) for n in (2,3,5,6,7)]))
        pairs=[(a,b) for a in vals for b in vals if a<0 and a<b and not(a.is_Rational and b.is_Rational)]
    return [{'a':str(a),'b':str(b),'variable':'x','left_closed':c} for a,b in pairs for c in (False,True)]

@functools.lru_cache(maxsize=3)
def get_catalog(level):return catalog(level)
def solution(a,b,v,c,t):
    left='*is*' if c else '*is not*';right='*is not*' if c else '*is*'
    result=interval(a,b,v,c) if t=='inequality_to_interval' else inequality(a,b,v,c)
    given=inequality(a,b,v,c) if t=='inequality_to_interval' else interval(a,b,v,c)
    return OPENING+'\n\nFor the given '+('inequality' if t=='inequality_to_interval' else 'interval')+'\n\n$$\n'+given+'\n$$\n\nwe note the following:\n\n'+f'- The left endpoint ${tex(a)}$ {left} included in the interval. Therefore, we use '+(('$[$.' if c else '$( $.') if t=='inequality_to_interval' else ('$\\le$.' if c else '$<$.'))+'\n'+f'- The right endpoint ${tex(b)}$ {right} included in the interval. Therefore, we use '+(('$) $.' if c else '$]$.') if t=='inequality_to_interval' else ('$<$.' if c else '$\\le$.'))+'\n\nTherefore, the '+('interval' if t=='inequality_to_interval' else 'inequality')+' that corresponds to the given '+('inequality' if t=='inequality_to_interval' else 'interval')+' is\n\n$$\n'+result+'\n$$'

def current_render(a,b,v,profile,c):
    """Exact newly captured source masks, parameterized by complete endpoint slots."""
    aa,bb=tex(a),tex(b)
    lop,rop=(r'\le','<') if c else ('<',r'\le')
    lb,rb=('[',')') if c else ('(',']')
    if profile in ('observed_28834','observed_102205'):
        prompt=f'The inequality ${aa}{lop} {v}{rop}{bb}$ can be expressed in interval notation as'
        opening="Every inequality can be expressed as an interval. We use the following notations:\n\n- Parentheses $()$ if the endpoints are *not* included.\n\n- Brackets $[]$ if the endpoints *are* included."
        given=f'{aa}\\,\\,{lop} \\,\\,{v}\\,\\,{rop}\\,\\,{bb}'
        left=lb+r'\,.';right=rb+r'\,.'
        end=f'Therefore, the corresponding interval is\n\n$$\n{v}\\in {lb}{aa},{bb}{rb}.\n$$'
        noun='inequality'
    else:
        prompt=f'The interval ${v}\\in {lb}{aa},{bb}{rb}$ corresponds to the inequality'
        opening="Every interval can be expressed as an inequality. We use the following notations:\n\n- Parentheses $()$ to indicate that the endpoints are *not* included.\n\n- Brackets $[]$ to indicate that the endpoints *are* included."
        given=f'{lb}{aa},{bb}\\,{rb}'
        left=lop+r' \,.';right=rop+r'\,.'
        end=f'Therefore, the inequality that corresponds to the given interval is \n\n$$\n{aa}\\,\\,{lop} \\,\\,{v}\\,\\,{rop}\\,\\,{bb}.\n$$'
        noun='interval'
    leftword='*is*' if c else 'is *not*';rightword='is *not*' if c else '*is*'
    sol=opening+f'\n\nFor the given {noun} \n\n$$\n{given}\n$$\n\nwe note the following:\n\n'+f'- The left endpoint ${aa}$ {leftword} included in the interval. Therefore, we use ${left}$\n\n'+f'- The right endpoint ${bb}$ {rightword} included in the interval. Therefore, we use ${right}$\n\n'+end
    return prompt,sol

@checked_public_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if type(seed) is not int:raise ValueError('seed must be a built-in int')
    if level not in LEVELS:raise ValueError('Unknown level')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio fields supported')
    rng=random.Random(seed);template=template or rng.choice(TEMPLATES)
    if template not in TEMPLATES:raise ValueError('Unknown template')
    observed=profile in OBSERVED
    c=rng.choice((False,True)) if parameters is None else parameters['left_closed']
    profile=profile or rng.choice(PROFILES[template])
    if profile not in (*OBSERVED,*PROFILES[template]):raise ValueError('Unknown profile')
    raw=profile.endswith('_raw')
    if observed and template!=('inequality_to_interval' if ('1253' in profile or '28834' in profile or '102205' in profile) else 'interval_to_inequality'):raise ValueError('Profile/template mismatch')
    if observed and parameters is None:raise ValueError('Observed profiles require explicit parameters')
    p=dict(parameters) if parameters is not None else dict(rng.choice([p for p in get_catalog(level) if p['left_closed']==c and compatible(expr(p['a']),expr(p['b']),profile)]))
    if parameters is None:p['variable']=rng.choice(('x','y','t','u'))
    a,b=guard(level,p,raw or profile=='observed_73902');v=p['variable'];c=p['left_closed']
    if profile in ('observed_28834','observed_73902','observed_102205'):
        if profile in ('observed_28834','observed_102205') and level!='easy':raise ValueError('Observed28834 is easy')
        if profile=='observed_73902' and (level!='moderate' or not(a.is_Integer and b.is_Integer and -15<=a<0<b<=15)):
            raise ValueError('Observed73902: moderate signed integer straddling zero')
    if not compatible(a,b,profile):raise ValueError('Profile has a duplicate choice at these endpoints')
    if recipe(profile) not in PROFILES[template]:raise ValueError('Profile/template mismatch')
    values=bank(a,b,v,c,template,profile)
    if profile=='observed_28834':
        values=[f'{v}\\in ({tex(a)},{tex(b)})',f'{v}\\in [{tex(a)},\\infty )',f'{v}\\in [{tex(a)},{tex(b)}]',f'{v}\\in ({tex(a)},{tex(b)}]',f'{v}\\in [{tex(a)},{tex(b)})']
    elif profile=='observed_102205':
        values=[f'{v}\\in [{tex(a)},{tex(b)}]', interval(a,b,v,False),interval(-b,-a,v,True),f'{v}\\in ({tex(a)},{tex(b)})',interval(a,b,v,True)]
    elif profile=='observed_73902':
        values=[f'{tex(-b)}<{v}\\le {tex(-a)}',f'{tex(a)}<{v}\\le {tex(b)}',f'{tex(a)}\\le {v}\\le {tex(b)}',f'{tex(a)}<{v}<{tex(b)}',f'{tex(a)}\\le {v}<{tex(b)}']
    if len(set(values))!=5 or len(set(mathematical_bank(a,b,c,template,profile)))!=5:raise ValueError('Whole bank rejected: duplicate or mathematically equivalent choice')
    correct=interval(a,b,v,c) if template=='inequality_to_interval' else inequality(a,b,v,c)
    if profile in ('observed_28834','observed_73902','observed_102205'):correct=(values[-1] if c else values[3]) if profile=='observed_28834' else (values[4] if c else values[1])
    if values.count(correct)!=1:raise ValueError('Whole bank rejected: missing/nonunique correct')
    if template=='inequality_to_interval':prompt='The inequality $'+inequality(a,b,v,c)+'$ can be expressed in interval notation as'
    else:
        left=tex(a)
        # The source spaced minus is a complete endpoint-format component.
        if observed and a.is_Integer and a<0:left='- '+str(abs(a))
        prompt='The interval $'+v+' ∈ '+('[' if c else '(')+left+', '+tex(b)+(')' if c else ']')+'$ corresponds to the inequality'
    sol=solution(a,b,v,c,template)
    if profile in ('observed_28834','observed_73902','observed_102205'):
        prompt,sol=current_render(a,b,v,profile,c)
    prompt=fmt.normalize_prose(prompt);sol=fmt.normalize_prose(sol)
    normalized=[fmt.normalize_tex(value) for value in values]
    correct=fmt.normalize_tex(correct);values=normalized
    task=digest({'a':str(a),'b':str(b),'left_closed':c,'direction':template})
    content=digest({'version':VERSION,'prompt':prompt,'solution':None if raw else sol,'bank':sorted(values),'key':None if raw else correct,'level':None if raw else level})
    qid=uid(content);fid=uid(qid+':selection')
    choices=[{':answer/id':uid(fid+':'+val),':answer/type':':answer.type/math',':answer/value':val} for val in values]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
    if not raw:field[':answer-field/correct']=[':answer/id',uid(fid+':'+correct)]
    rng.shuffle(choices)
    question={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if not raw:question.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':sol})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'source':SOURCE,'difficulty':level,'difficulty_origin':('observed' if profile in ('observed_28834','observed_73902','observed_102205') else 'authored band extension; original labels preserved in observed replay'),'template':template,'profile':profile,'parameters':{'a':str(a),'b':str(b),'variable':v,'left_closed':c},'mathematical_fingerprint':task,'content_fingerprint':content,'seed':seed,'source_id':('q-'+profile.split('_')[1] if observed else None),'raw_missing_fields_preserved':raw,'solution_origin':('observed full solution' if profile in ('observed_28834','observed_73902','observed_102205') else 'authored from canonical shared opening and endpoint sequence'),'semantic_catalog_count':len(get_catalog(level))*2,'plot_rating':'none'}}

# Easy: signed integer endpoint reading; same two endpoint decisions in either direction.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: signed rational endpoint reading; no arithmetic or solving added.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: signed surd endpoint reading, anchored to the canonical example.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join(f"- ${a[':answer/value']}$" for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[No worked solution captured.]')
def generate_many(level,seed=0,count=1,template=None,field_type=None,parameters=None,profile=None):
    """Choose decision roles/profile first, then compatible unused endpoint data."""
    if type(seed) is not int or type(count) is not int:raise ValueError('seed and count must be built-in int')
    if level not in (*LEVELS,'all'):raise ValueError('Unknown level')
    if count<1:raise ValueError('count must be positive')
    levels=LEVELS if level=='all' else (level,)
    if parameters is not None or profile in OBSERVED:
        if count!=1:raise ValueError('Explicit replay has capacity one')
        return [generate(l,seed,template,field_type,parameters,profile) for l in levels]
    if template not in (None,*TEMPLATES):raise ValueError('Unknown template')
    result=[];rng=random.Random(seed)
    for l in levels:
        directions=(template,) if template else TEMPLATES
        if profile is not None:
            directions=tuple(t for t in directions if profile in PROFILES[t])
            if not directions:raise ValueError('Profile/template mismatch')
        pools={(t,c):[p for p in get_catalog(l) if p['left_closed']==c and
                     (profile is None or compatible(expr(p['a']),expr(p['b']),profile))]
               for t in directions for c in (False,True)}
        if count>sum(map(len,pools.values())):raise ValueError('count exceeds semantic task capacity')
        for i in range(count):
            t,c=rng.choice([g for g,rows in pools.items() if rows])
            profiles=(profile,) if profile else PROFILES[t]
            if any(p not in PROFILES[t] for p in profiles):raise ValueError('Profile/template mismatch')
            chosen=rng.choice(profiles)
            eligible=[j for j,p in enumerate(pools[t,c]) if compatible(expr(p['a']),expr(p['b']),chosen)]
            if not eligible:
                # A depleted recipe is not a depleted task catalog. Keep the
                # normal seeded path unchanged, but retry decision groups and
                # complete profiles that can still supply an unused task.
                remaining=[]
                for (other_t,other_c),rows in pools.items():
                    options=[]
                    for other_profile in ((profile,) if profile else PROFILES[other_t]):
                        indices=[j for j,p in enumerate(rows) if compatible(expr(p['a']),expr(p['b']),other_profile)]
                        if indices:options.append((other_profile,indices))
                    if options:remaining.append((other_t,other_c,options))
                if not remaining:raise ValueError('No compatible semantic tasks remain')
                t,c,options=rng.choice(remaining)
                chosen,eligible=rng.choice(options)
            p=dict(pools[t,c].pop(rng.choice(eligible)));p['variable']=rng.choice(('x','y','t','u'))
            result.append(generate(l,seed+i,t,field_type,p,chosen))
    return result

def main():
    a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=(*LEVELS,'all'),default='easy');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=('markdown','json'),default='json');a.add_argument('--template');a.add_argument('--profile');a.add_argument('--parameters',help='JSON parameters for explicit replay');n=a.parse_args()
    try:records=generate_many(n.difficulty,n.seed,n.count,n.template,parameters=json.loads(n.parameters) if n.parameters else None,profile=n.profile)
    except ValueError as exc:a.error(str(exc))
    print(json.dumps(records,indent=2,ensure_ascii=False) if n.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
