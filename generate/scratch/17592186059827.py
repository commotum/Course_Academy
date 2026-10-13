#!/usr/bin/env python3
"""Half-open endpoint translation; basis1356, no database operations.

Two unrated practice families have complete radio banks but no key or solution.
`observed_1253_raw` / `observed_25754_raw` preserve those absences through the
public parameterized API. Unsuffixed observed profiles supply independently
verified keys and canonical-anchored authored solutions. All levels are authored
workload claims: integer / signed rational / signed surd endpoints, with exactly
one included endpoint. No solving, graphing, unions or unbounded intervals.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186059827
KP_UUID='bdf77469-6c2a-5339-b216-3bc5e2316e4d'
TITLE='Translating Between Half-Open Intervals and Inequalities'
VERSION='half-open-v4'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
ROOT=Path(__file__).with_suffix('')
TEMPLATES=('inequality_to_interval','interval_to_inequality')
LEVELS=('easy','moderate','hard')
NS=uuid.UUID(KP_UUID)
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
OPENING=("Every interval can be expressed as an inequality. We use the following notations:\n\n"
 r"- Parentheses ${\color{red}{(}}\phantom{0} \phantom{0}{\color{red}{)}}$ to indicate that the endpoints are *not* included."+"\n"+
 r"- Brackets ${\color{blue}{[}}\phantom{0}\phantom{0}{\color{blue}{]}}$ to indicate that the endpoints *are* included.")

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(NS,x))
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
    if t=='inequality_to_interval':
        # Full observed endpoint-inclusion bank plus reversed endpoints.
        return [interval(a,b,v,False),f'{v} ∈ ({tex(a)}, {tex(b)})',f'{v} ∈ [{tex(a)}, {tex(b)}]',interval(a,b,v,True),interval(b,a,v,c)]
    rows=[f'{tex(a)} < {v} < {tex(b)}',f'{tex(a)} '+r'\le'+f' {v} < {tex(b)}',f'{tex(a)} '+r'\le'+f' {v} '+r'\le'+f' {tex(b)}',f'{tex(a)} < {v} '+r'\le'+f' {tex(b)}']
    # Observed sign omission is an explicit operation, not a fitted scalar.
    extra=inequality(-a,b,v,c) if p.startswith('observed_25754') else inequality(b,a,v,c)
    return rows[:2]+[extra]+rows[2:]

def guard(level,p,observed=False):
    if set(p)!={'a','b','variable','left_closed'}:raise ValueError('Exact parameter keys: a,b,variable,left_closed')
    a,b=expr(p['a']),expr(p['b'])
    if a>=b or p['variable'] not in ('x','y','t','u') or type(p['left_closed']) is not bool:raise ValueError('Ordered endpoints, supported variable, and Boolean inclusion required')
    if observed:
        if abs(a)>20 or abs(b)>20:raise ValueError('Replay bounds |endpoint|<=20')
    elif level=='easy':
        if not (a.is_Integer and b.is_Integer and -15<=a<b<=15):raise ValueError('Easy: signed integers -15..15')
    elif level=='moderate':
        if not (a.is_Rational and b.is_Rational and not(a.is_Integer and b.is_Integer) and a<0 and abs(a)<=10 and abs(b)<=10 and a.q<=5 and b.q<=5):raise ValueError('Moderate: signed rational endpoints; denominator<=5, magnitude<=10, noninteger present')
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
        pairs=[(a,b) for a in vals for b in vals if a<0 and a<b and not(a.is_Integer and b.is_Integer)]
    else:
        vals=sorted(set([sp.Integer(i) for i in range(-8,9)]+[s*k*sp.sqrt(n) for s in (-1,1) for k in (1,2,3) for n in (2,3,5,6,7)]))
        pairs=[(a,b) for a in vals for b in vals if a<0 and a<b and not(a.is_Rational and b.is_Rational)]
    return [{'a':str(a),'b':str(b),'variable':'x','left_closed':c} for a,b in pairs for c in (False,True)]

_CATALOG={l:catalog(l) for l in LEVELS}
def solution(a,b,v,c,t):
    left='*is*' if c else '*is not*';right='*is not*' if c else '*is*'
    result=interval(a,b,v,c) if t=='inequality_to_interval' else inequality(a,b,v,c)
    given=inequality(a,b,v,c) if t=='inequality_to_interval' else interval(a,b,v,c)
    return OPENING+'\n\nFor the given '+('inequality' if t=='inequality_to_interval' else 'interval')+'\n\n$$\n'+given+'\n$$\n\nwe note the following:\n\n'+f'- The left endpoint ${tex(a)}$ {left} included in the interval. Therefore, we use '+(('$[$.' if c else '$( $.') if t=='inequality_to_interval' else ('$\\le$.' if c else '$<$.'))+'\n'+f'- The right endpoint ${tex(b)}$ {right} included in the interval. Therefore, we use '+(('$) $.' if c else '$]$.') if t=='inequality_to_interval' else ('$<$.' if c else '$\\le$.'))+'\n\nTherefore, the '+('interval' if t=='inequality_to_interval' else 'inequality')+' that corresponds to the given '+('inequality' if t=='inequality_to_interval' else 'interval')+' is\n\n$$\n'+result+'\n$$'

def current_render(a,b,v,profile):
    """Exact newly captured source masks, parameterized by complete endpoint slots."""
    aa,bb=tex(a),tex(b)
    if profile=='observed_28834':
        prompt=f'The inequality ${aa}\\le {v}<{bb}$ can be expressed in interval notation as'
        opening="Every inequality can be expressed as an interval. We use the following notations:\n\n- Parentheses $()$ if the endpoints are *not* included.\n\n- Brackets $[]$ if the endpoints *are* included."
        given=f'{aa}\\,\\,\\le \\,\\,{v}\\,\\,<\\,\\,{bb}'
        left=r'[\,.';right=r')\,.'
        end=f'Therefore, the corresponding interval is\n\n$$\n{v}\\in [{aa},{bb}).\n$$'
        noun='inequality'
    else:
        prompt=f'The interval ${v}\\in [{aa},{bb})$ corresponds to the inequality'
        opening="Every interval can be expressed as an inequality. We use the following notations:\n\n- Parentheses $()$ to indicate that the endpoints are *not* included.\n\n- Brackets $[]$ to indicate that the endpoints *are* included."
        given=f'[{aa},{bb}\\,)'
        left=r'\le \,.';right=r'<\,.'
        end=f'Therefore, the inequality that corresponds to the given interval is \n\n$$\n{aa}\\,\\,\\le \\,\\,{v}\\,\\,<\\,\\,{bb}.\n$$'
        noun='interval'
    sol=opening+f'\n\nFor the given {noun} \n\n$$\n{given}\n$$\n\nwe note the following:\n\n'+f'- The left endpoint ${aa}$ *is* included in the interval. Therefore, we use ${left}$\n\n'+f'- The right endpoint ${bb}$ is *not* included in the interval. Therefore, we use ${right}$\n\n'+end
    return prompt,sol

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('Unknown level')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio fields supported')
    rng=random.Random(seed);template=template or rng.choice(TEMPLATES)
    if template not in TEMPLATES:raise ValueError('Unknown template')
    profile=profile or 'authored_endpoint_bank'
    if profile not in ('authored_endpoint_bank','observed_1253','observed_1253_raw','observed_25754','observed_25754_raw','observed_28834','observed_73902'):raise ValueError('Unknown profile')
    observed=profile.startswith('observed');raw=profile.endswith('_raw')
    if observed and template!=('inequality_to_interval' if ('1253' in profile or '28834' in profile) else 'interval_to_inequality'):raise ValueError('Profile/template mismatch')
    if observed and parameters is None:raise ValueError('Observed profiles require explicit parameters')
    p=dict(parameters) if parameters is not None else dict(rng.choice(_CATALOG[level]))
    if parameters is None:p['variable']=rng.choice(('x','y','t','u'))
    a,b=guard(level,p,raw or profile=='observed_73902');v=p['variable'];c=p['left_closed']
    if profile in ('observed_28834','observed_73902'):
        if not c:raise ValueError('New observed banks require left-closed input')
        if profile=='observed_28834' and level!='easy':raise ValueError('Observed28834 is easy')
        if profile=='observed_73902' and (level!='moderate' or not(a.is_Integer and b.is_Integer and -15<=a<0<b<=15)):
            raise ValueError('Observed73902: moderate signed integer straddling zero')
    if '25754' in profile and (not c or a==0):raise ValueError('Observed sign-omission bank requires left-closed and nonzero left endpoint')
    if '1253' in profile and c:raise ValueError('Observed1253 requires right-closed interval')
    values=bank(a,b,v,c,template,profile)
    if profile=='observed_28834':
        values=[f'{v}\\in ({tex(a)},{tex(b)})',f'{v}\\in [{tex(a)},\\infty )',f'{v}\\in [{tex(a)},{tex(b)}]',f'{v}\\in ({tex(a)},{tex(b)}]',f'{v}\\in [{tex(a)},{tex(b)})']
    elif profile=='observed_73902':
        values=[f'{tex(-b)}<{v}\\le {tex(-a)}',f'{tex(a)}<{v}\\le {tex(b)}',f'{tex(a)}\\le {v}\\le {tex(b)}',f'{tex(a)}<{v}<{tex(b)}',f'{tex(a)}\\le {v}<{tex(b)}']
    if len(set(values))!=5:raise ValueError('Whole bank rejected: duplicate choice')
    correct=interval(a,b,v,c) if template=='inequality_to_interval' else inequality(a,b,v,c)
    if profile in ('observed_28834','observed_73902'):correct=values[-1]
    if values.count(correct)!=1:raise ValueError('Whole bank rejected: missing/nonunique correct')
    if template=='inequality_to_interval':prompt='The inequality $'+inequality(a,b,v,c)+'$ can be expressed in interval notation as'
    else:
        left=tex(a)
        # The source spaced minus is a complete endpoint-format component.
        if observed and a.is_Integer and a<0:left='- '+str(abs(a))
        prompt='The interval $'+v+' ∈ '+('[' if c else '(')+left+', '+tex(b)+(')' if c else ']')+'$ corresponds to the inequality'
    sol=solution(a,b,v,c,template)
    if profile in ('observed_28834','observed_73902'):
        prompt,sol=current_render(a,b,v,profile)
    task=digest({'a':str(a),'b':str(b),'left_closed':c,'direction':template})
    content=digest({'version':VERSION,'prompt':prompt,'solution':None if raw else sol,'bank':sorted(values),'key':None if raw else correct,'level':None if raw else level})
    qid=uid(content);fid=uid(qid+':selection')
    choices=[{':answer/id':uid(fid+':'+val),':answer/type':':answer.type/math',':answer/value':val} for val in values]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
    if not raw:field[':answer-field/correct']=[':answer/id',uid(fid+':'+correct)]
    rng.shuffle(choices)
    question={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if not raw:question.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':sol})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'source':(SOURCE|{'basis':2081} if profile in ('observed_28834','observed_73902') else SOURCE),'difficulty':level,'difficulty_origin':('observed' if profile in ('observed_28834','observed_73902') else 'authored; initial originals unrated'),'template':template,'profile':profile,'parameters':{'a':str(a),'b':str(b),'variable':v,'left_closed':c},'mathematical_fingerprint':task,'content_fingerprint':content,'seed':seed,'source_id':('q-'+profile.split('_')[1] if observed else None),'raw_missing_fields_preserved':raw,'solution_origin':('observed full solution' if profile in ('observed_28834','observed_73902') else 'absent in initial practice capture; authored using canonical shared opening/endpoint sequence'),'semantic_catalog_count':len(_CATALOG[level])*2,'plot_rating':'none'}}

# Easy: signed integer endpoint reading; same two endpoint decisions in either direction.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: signed rational endpoint reading; no arithmetic or solving added.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: signed surd endpoint reading, anchored to canonical and Surds prerequisites.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join(f"- ${a[':answer/value']}$" for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[No worked solution captured.]')
def main():
    a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=('markdown','json'),default='markdown');a.add_argument('--template');a.add_argument('--profile');a.add_argument('--parameters',help='JSON parameters for explicit replay');n=a.parse_args()
    records=[generate(l,n.seed+i,n.template,parameters=json.loads(n.parameters) if n.parameters else None,profile=n.profile) for l in (LEVELS if n.difficulty=='all' else (n.difficulty,)) for i in range(n.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if n.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
