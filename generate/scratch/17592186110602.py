#!/usr/bin/env python3
"""Axis-perpendicular equation generator, steps 3–7 only.

Observed: six easy five-choice radios, two unrated two-blank equations.
Each source bank is a complete parameterized profile; its original distractor
intent is not recoverable from one example. Default banks are explicitly authored.
Moderate/hard labels are authored numeric-reading policies, not source labels.
The categorical operation has a difficulty ceiling: swap horizontal/vertical,
then retain the required coordinate. No slopes or general line algebra are added.
Exact SymPy rationals; deterministic banks; field-owned UUIDs; no database IO.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import random
import uuid
from dataclasses import dataclass
import sympy as sp

KP_ID = 17592186110602
KP_UUID = 'a6fee8d5-e1f7-599d-a74c-abc44d973065'
TITLE = 'Finding Equations of Perpendicular Horizontal and Vertical Lines'
VERSION = 'axis-perpendicular-1'
SOURCE = {'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}

@dataclass(frozen=True)
class Template:
    axis: str
    kind: str
    layout: str
    sources: tuple[str,...]

TEMPLATES = {
    'line_first_vertical_radio':Template('x','radio','line_first',('q-110139','q-110140','q-110143')),
    'line_first_horizontal_radio':Template('y','radio','line_first',('q-110142',)),
    'point_first_vertical_radio':Template('x','radio','point_first',('q-23628',)),
    'determine_horizontal_radio':Template('y','radio','determine',('q-44691',)),
    'standard_horizontal_blank':Template('y','blank','standard',('q-215418',)),
    'standard_vertical_blank':Template('x','blank','standard',('q-215951',)),
}

# A profile is chosen whole, before sampling. These explicit coordinate/input
# operations reproduce each complete observed bank; inferred author intent is
# unresolved. In particular reciprocal c is retained only in its observed profile.
PROFILES = {
    'observed_q110139':('line_first_vertical_radio',('y:a','y:b','x:b','x:a','y:-c'),'q-110139'),
    'observed_q110140':('line_first_vertical_radio',('x:-a','y:-c','y:a','x:b','y:b'),'q-110140'),
    'observed_q110142':('line_first_horizontal_radio',('x:c','x:a','y:a','y:1/c','x:b'),'q-110142'),
    'observed_q110143':('line_first_vertical_radio',('y:b','y:-a','y:-c','x:b','x:a'),'q-110143'),
    'observed_q23628':('point_first_vertical_radio',('y:-b','x:b','y:b','y:a','x:a'),'q-23628'),
    'observed_q44691':('determine_horizontal_radio',('x:a','x:b','y:a','x:c','y:b'),'q-44691'),
}
AUTHORED_PROFILES = ('authored_coordinate_sign','authored_zero_coordinate')

def rational(value):
    if isinstance(value,(bool,float)):
        raise ValueError('Use exact integer/rational strings, never floating-point values')
    result=sp.Rational(value)
    if not result.is_finite:
        raise ValueError('Coordinates must be finite rational values')
    return result

def tex(value,style='fraction'):
    value=rational(value)
    if style=='decimal':
        if 100 % int(value.q):
            raise ValueError('Decimal policy allows at most two exact decimal places')
        n=int(value*100)
        sign='-' if n<0 else ''
        n=abs(n)
        return sign+str(n//100)+('.'+str(n%100).zfill(2).rstrip('0') if n%100 else '')
    return ('-' if value<0 else '')+(str(abs(value.p)) if value.q==1 else rf'\frac{{{abs(value.p)}}}{{{value.q}}}')

def normalize_parameters(parameters):
    if set(parameters)-{'c','a','b','style'} or not {'c','a','b'}<=set(parameters):
        raise ValueError('Parameters are exactly c, a, b and optional style')
    p={key:rational(parameters[key]) for key in ('c','a','b')}
    p['style']=parameters.get('style','fraction')
    if p['style'] not in ('fraction','decimal'):
        raise ValueError('Unknown number style')
    if p['style']=='decimal':
        for value in (p['c'],p['a'],p['b']):tex(value,'decimal')
    return p

def validate_parameters(level,spec,p):
    target=p['b'] if spec.axis=='x' else p['a']
    if any(abs(p[k])>12 for k in ('a','b','c')):
        raise ValueError('Coordinate and reference-constant magnitude bound is 12')
    if level=='easy':
        if p['style']!='fraction' or any(p[k].q!=1 for k in ('a','b')) or p['c'].q>10:
            raise ValueError('Easy uses integer point coordinates and a simple reference constant')
    elif level=='moderate':
        if p['style']!='fraction' or target.q not in range(2,6) or abs(target.p)>24 or any(p[k].q>5 for k in ('a','b','c')):
            raise ValueError('Moderate target is a noninteger rational with denominator 2..5 and numerator magnitude <=24')
    elif level=='hard':
        if p['style']=='fraction':
            if target.q not in range(6,11) or abs(target.p)>60 or any(p[k].q>10 for k in ('a','b','c')):
                raise ValueError('Hard fractional target has denominator 6..10 and numerator magnitude <=60')
        elif target.q==1:
            raise ValueError('Hard decimal target must be noninteger')
    else:raise ValueError('Unknown difficulty')

def sample(level,spec,rng):
    if level=='easy':
        values=[sp.Integer(i) for i in range(-12,13)]
        return {'a':rng.choice(values),'b':rng.choice(values),'c':rng.choice(values),'style':'fraction'}
    if level=='moderate':
        targets=sorted({sp.Rational(n,d) for d in range(2,6) for n in range(-24,25) if n and sp.Rational(n,d).q in range(2,6) and abs(sp.Rational(n,d))<=12})
        style='fraction'
    else:
        style=rng.choice(('fraction','decimal'))
        targets=sorted({sp.Rational(n,d) for d in (range(6,11) if style=='fraction' else (10,20,25,50,100)) for n in range(-60,61) if n and abs(sp.Rational(n,d))<=12 and (sp.Rational(n,d).q in range(6,11) if style=='fraction' else sp.Rational(n,d).q>1)})
    target=rng.choice(targets)
    unused=sp.Integer(rng.randint(-12,12))
    return {'a':unused if spec.axis=='x' else target,'b':target if spec.axis=='x' else unused,'c':sp.Integer(rng.randint(-12,12)),'style':style}

def bank(spec,p,profile):
    axis='y' if spec.axis=='x' else 'x'
    k=p['b'] if axis=='y' else p['a']
    unused=p['a'] if axis=='y' else p['b']
    if profile in PROFILES:
        if PROFILES[profile][0] not in TEMPLATES or TEMPLATES[PROFILES[profile][0]]!=spec:
            raise ValueError('Profile does not belong to the selected template')
        recipes=PROFILES[profile][1]
        out=[]
        for recipe in recipes:
            letter,expression=recipe.split(':')
            value=sp.sympify(expression,locals={key:p[key] for key in ('a','b','c')})
            if not value.is_Rational or not value.is_finite:raise ValueError('Invalid whole bank')
            out.append((letter,value,recipe))
    elif profile=='authored_coordinate_sign':
        if k==0:raise ValueError('Sign bank requires nonzero required coordinate')
        out=[(axis,k,'retain_required_coordinate'),(axis,unused,'select_unused_coordinate'),(spec.axis,k,'retain_given_axis_with_required_coordinate'),(spec.axis,unused,'retain_given_axis_with_unused_coordinate'),(axis,-k,'reverse_required_coordinate_sign')]
    elif profile=='authored_zero_coordinate':
        if k!=0:raise ValueError('Zero bank requires zero required coordinate')
        out=[(axis,k,'retain_required_coordinate'),(axis,unused,'select_unused_coordinate'),(spec.axis,k,'retain_given_axis_with_required_coordinate'),(spec.axis,unused,'retain_given_axis_with_unused_coordinate'),(axis,p['c'],'select_reference_constant')]
    else:raise ValueError('Unknown bank profile')
    keys=[(a,str(v)) for a,v,_ in out]
    if len(set(keys))!=5 or sum(a==axis and v==k for a,v,_ in out)!=1:
        raise ValueError('Reject whole bank: equivalent choices or missing/ambiguous correct answer')
    return out

def render_prompt(spec,p):
    c,a,b=(tex(p[key],p['style']) for key in ('c','a','b'))
    line=spec.axis+'='+c
    point='('+a+','+b+')'
    if spec.layout=='line_first':
        return f'Find the equation of the line that is perpendicular to ${line}$ and passes through the point ${point}.$'
    if spec.layout=='point_first':
        return f'Find the equation of the line that passes through the point ${point}$ and is perpendicular to ${line}.$'
    if spec.layout=='determine':
        return f'Determine the equation of the line that passes through the point ${point}$ and is perpendicular to ${line}.$'
    line=spec.axis+' = '+c
    point='('+a+', '+b+')'
    return f'Find the equation of the line that is perpendicular to ${line}$ and passes through the point ${point}$. Write your answer in **standard form.** {{{{field-1}}}} $=$\n{{{{field-2}}}}'

def render_solution(spec,p):
    given_orientation,needed=('vertical','horizontal') if spec.axis=='x' else ('horizontal','vertical')
    axis='y' if spec.axis=='x' else 'x'
    k=p['b'] if axis=='y' else p['a']
    c,a,b=(tex(p[key],p['style']) for key in ('c','a','b'))
    return f'Since the line ${spec.axis}={c}$ is a {given_orientation} line, a perpendicular line would need to be {needed}. So, the perpendicular line must take the form ${axis}=k$ for some value of $k.$\n\nThe perpendicular line needs to go through the point $({a},{b}),$ which has '+('a' if axis=='y' else 'an')+f' ${axis}$-coordinate of ${tex(k,p["style"])}.$ So, the perpendicular line is ${axis}={tex(k,p["style"])}.$'

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(value):return str(uuid.uuid5(uuid.NAMESPACE_URL,value))

def assemble(level,name,p,seed,profile):
    spec=TEMPLATES[name]
    axis='y' if spec.axis=='x' else 'x'
    k=p['b'] if axis=='y' else p['a']
    if spec.kind=='radio':
        options=bank(spec,p,profile)
        values=[a+'='+tex(v,p['style']) for a,v,_ in options]
        correct=axis+'='+tex(k,p['style'])
        field_values=[values]
        correct_values=[correct]
        keys=['selection']
    else:
        if profile is not None:raise ValueError('Blanks have no bank profile')
        options=[]
        # Standard-form fragments have coprime integer coefficient/constant.
        lhs=(str(k.q) if k.q!=1 else '')+axis
        rhs=str(k.p)
        field_values=[[lhs],[rhs]]
        correct_values=[lhs,rhs]
        keys=['field-1','field-2']
    prompt=render_prompt(spec,p)
    solution=render_solution(spec,p)
    if spec.kind=='blank' and k.q!=1:
        solution+=f'\n\nIn standard form, this is ${k.q}{axis}={k.p}.$'
    # Axis and actual required coordinate fully determine the assessed task.
    # Reference constant, unused coordinate, level, layout, notation and banks
    # do not inflate substantive task counts.
    math_fingerprint=digest({'required_axis':axis,'required_coordinate':str(k)})
    canonical_p={key:str(p[key]) for key in ('a','b','c')}|{'style':p['style']}
    content_key=digest({'version':VERSION,'level':level,'template':name,'parameters':canonical_p,'profile':profile,'domain':'rational coordinate plane','prompt':prompt,'solution':solution,'banks':[sorted(v) for v in field_values]})
    qid=ident(content_key)
    fields=[]
    for i,(key,values,corr) in enumerate(zip(keys,field_values,correct_values)):
        fid=ident(qid+':'+key)
        answers=[{':answer/id':ident(fid+':'+value),':answer/type':':answer.type/math',':answer/value':value} for value in values]
        correctid=next(answer[':answer/id'] for answer in answers if answer[':answer/value']==corr)
        # Correct identity is fixed before display shuffle; seed is not identity.
        if spec.kind=='radio':random.Random(str(seed)+':options').shuffle(answers)
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+spec.kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correctid]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':canonical_p,'bank_profile':profile,'bank_origin':'observed' if profile in PROFILES else 'authored' if profile else 'none','authored_level':level!='easy' or spec.kind=='blank','source_analysis':SOURCE|{'question_ids':[PROFILES[profile][2]] if profile in PROFILES else list(spec.sources)},'answer_origin':'mathematically_derived_missing_source_refs' if spec.kind=='blank' else 'derived','parameter_fingerprint':math_fingerprint,'content_fingerprint':content_key,'plot_rating':'none','plot_assets':{},'domain':'rational coordinate plane','distractor_recipes':[r for _,_,r in options],'sympy_version':sp.__version__}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    if field_type is not None and field_type not in ('radio','blank'):raise ValueError('Unknown field type')
    if profile in PROFILES:
        implied=PROFILES[profile][0]
        if template is not None and template!=implied:raise ValueError('Profile/template mismatch')
        template=implied
    elif profile is not None and profile not in AUTHORED_PROFILES:raise ValueError('Unknown profile')
    eligible=[name for name,spec in TEMPLATES.items() if (field_type is None or spec.kind==field_type) and (profile is None or spec.kind=='radio')]
    if template is not None and template not in eligible:raise ValueError('Invalid template/field/profile combination')
    rng=random.Random(seed)
    name=template or rng.choice(eligible)
    spec=TEMPLATES[name]
    for _ in range(256):
        p=normalize_parameters(parameters) if parameters is not None else sample(level,spec,rng)
        validate_parameters(level,spec,p)
        selected=profile
        if spec.kind=='radio' and selected is None:
            selected='authored_zero_coordinate' if (p['b'] if spec.axis=='x' else p['a'])==0 else 'authored_coordinate_sign'
        try:return assemble(level,name,p,seed,selected)
        except ValueError:
            if parameters is not None:raise
    raise ValueError('Bounded whole-bank rejection did not find a valid instance')

# EASY: observed integer-coordinate method plus explicitly assigned unrated blanks.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE: authored bounded signed fractions; identical categorical operation.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)

# HARD: authored less familiar fractions/exact decimals; no new line algebra.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q,g=record['question'],record['generation']
    out=[f'## Generated {q[":question/difficulty"].split("/")[-1]} — {g["template"]}',f'Profile: `{g["bank_profile"]}`; numeric policy {"authored" if g["authored_level"] else "easy"}.','',q[':question/problem'],'']
    for field in q[':question/answer-fields']:
        for answer in field[':answer-field/choices']:
            mark=' **correct**' if answer[':answer/id']==field[':answer-field/correct'][1] else ''
            out.append(f'- {field[":answer-field/key"]}: ${answer[":answer/value"]}$'+mark)
    return '\n'.join(out+['','**Worked solution**','',q[':question/worked-solution']])

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all')
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--format',choices=('json','markdown'),default='markdown')
    parser.add_argument('--template',choices=TEMPLATES)
    parser.add_argument('--profile',choices=tuple(PROFILES)+AUTHORED_PROFILES)
    parser.add_argument('--field-type',choices=('radio','blank'))
    args=parser.parse_args()
    if args.count<1:parser.error('Count must be positive')
    levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
    try:records=[generate(level,args.seed+i,args.template,args.field_type,profile=args.profile) for level in levels for i in range(args.count)]
    except ValueError as exc:parser.error(str(exc))
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))

if __name__=='__main__':main()
