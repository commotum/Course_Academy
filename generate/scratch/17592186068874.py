#!/usr/bin/env python3
"""Negative-linear already-isolated perfect-square expressions; basis 1356.

Shared exact helpers, source-shaped easy/moderate recipes, and authored hard
nonunit variable factors. No add/subtract trick, equation solving, plots or DB.
Raw profiles are public evidence-only parameterized replays preserving individual
missing attributes. Normal completions are authored. See adjacent extraction.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import random
import sys
import uuid
from dataclasses import dataclass
import sympy as sp

KP_ID = 17592186068874
KP_UUID = 'bf9b812d-0dbf-5a67-9d45-3cc5e373b2b1'
TITLE = 'Completing the Square When the Perfect Square is Isolated: Negative Linear Term'
VERSION = 'isolated-negative-square-v1'
SOURCE = {'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
OPENING = 'First, we recall the following formula:'
FACTORING = 'Notice that we have a perfect square in the parentheses that we can factor as follows:'
CONCLUSION = 'Therefore, we obtain'

@dataclass(frozen=True)
class Template:
    field: str
    style: str
    stages: str
    sources: tuple = ()

# Easy: one monic negative-linear identity, preserved source layouts/stages.
TEMPLATES = {
 'radio_power': Template('radio','power','power',('q-140277',)),
 'radio_numeric': Template('radio','numeric','numeric',('q-140279','q-140281','q-140283')),
 'blank_numeric': Template('blank','numeric','direct',('q-235868','q-250428')),
 'radio_spaced': Template('radio','spaced_power','power',('q-140276',)),
 'blank_spaced': Template('blank','spaced_power','power',('q-250431',)),
 # Hard: recognize both nonunit squared variable factor and positive constant root.
 'radio_scaled': Template('radio','scaled','scaled'),
 'blank_scaled': Template('blank','scaled','scaled'),
}
BANKS = {
 'half_coefficient': ('correct','sign','double','quarter_linear','positive_double'),
 'square_constant': ('correct','sign','constant','double','positive_double'),
 'both_constant_signs': ('correct','sign','constant','double','positive_constant'),
 'adjacent_opaque': ('correct','sign','adjacent','double','positive_adjacent'),
 'scaled_method': ('correct','sign','double','omit_variable_factor','use_squared_factor'),
}
CASES = [
 {'source_id':'q-140276','level':'easy','template':'radio_spaced','parameters':{'a':6,'b':1,'c':-10,'variable':'x'},'bank_profile':'half_coefficient','raw_missing':['difficulty','solution','correct']},
 {'source_id':'q-250431','level':'easy','template':'blank_spaced','parameters':{'a':7,'b':1,'c':2,'variable':'x'},'bank_profile':None,'raw_missing':['difficulty','solution','correct','choices']},
 {'source_id':'q-140277','level':'easy','template':'radio_power','parameters':{'a':3,'b':1,'c':6,'variable':'y'},'bank_profile':'both_constant_signs','raw_missing':[]},
 {'source_id':'q-140279','level':'easy','template':'radio_numeric','parameters':{'a':2,'b':1,'c':1,'variable':'y'},'bank_profile':'half_coefficient','raw_missing':[]},
 {'source_id':'q-140281','level':'easy','template':'radio_numeric','parameters':{'a':5,'b':1,'c':1,'variable':'x'},'bank_profile':'square_constant','raw_missing':[]},
 {'source_id':'q-140283','level':'moderate','template':'radio_numeric','parameters':{'a':11,'b':1,'c':-4,'variable':'x'},'bank_profile':'adjacent_opaque','raw_missing':[]},
 {'source_id':'q-235868','level':'easy','template':'blank_numeric','parameters':{'a':4,'b':1,'c':5,'variable':'x'},'bank_profile':None,'raw_missing':[]},
 {'source_id':'q-250428','level':'easy','template':'blank_numeric','parameters':{'a':9,'b':1,'c':2,'variable':'x'},'bank_profile':None,'raw_missing':[]},
]
RAW_PROFILES = {'raw_'+c['source_id']: c for c in CASES}


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False)


def uid(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID),canonical(value)))


def tex(value):
    return sp.latex(sp.sympify(value))


def suffix(c,spaced=False):
    gap = ' ' if spaced else ''
    return gap+('+' if c>0 else '-')+gap+str(abs(c))


def linear(v,b):
    return v if b==1 else str(b)+v


def square(v,b,a,style):
    op = '-' if a>=0 else '+'
    if style=='spaced_power':
        return f'({linear(v,b)} {op} {tex(abs(a))})^{{2}}'
    return f'({linear(v,b)}{op}{tex(abs(a))}{{)}}^{{2}}'


def inner(p,style):
    a,b,v = p['a'],p['b'],p['variable']
    if style=='spaced_power':
        return f'{v}^{{2}} - {2*a}{v} + {a}^{{2}}'
    constant = f'{{{a}}}^{{2}}' if style=='power' else str(a*a)
    leading = f'{{{v}}}^{{2}}' if b==1 else f'{b*b}{{{v}}}^{{2}}'
    return leading+f'-{2*a*b}{v}+'+constant


def expr(p,style):
    return '('+inner(p,style)+')'+suffix(p['c'],style=='spaced_power')


def solution(p,spec):
    a,b,c,v = p['a'],p['b'],p['c'],p['variable']
    formula = f'{{{v}}}^{{2}}-2a{v}+{{a}}^{{2}}=({v}-a{{)}}^{{2}}'
    rows=[inner(p,'power' if spec.style=='spaced_power' else spec.style)]
    if spec.stages=='numeric': rows.append(inner(p,'power'))
    if spec.stages=='scaled':
        rows.append(f'({linear(v,b)})^{{2}}-2\\cdot {a}\\cdot ({linear(v,b)})+{{{a}}}^{{2}}')
    else: rows.append(f'{{{v}}}^{{2}}-2\\cdot {a}{v}+{{{a}}}^{{2}}')
    rows.append(square(v,b,a,'numeric'))
    # Preserve the source's unevaluated identity/half-coefficient arithmetic.
    chain = r'\begin{aligned}'+r' & = \\ '.join(rows)+r' & \end{aligned}'
    final = r'\begin{aligned}'+expr(p,'power' if spec.style=='spaced_power' else spec.style)+r' & = \\ '+square(v,b,a,'numeric')+suffix(c)+r' & .\end{aligned}'
    return OPENING+'\n\n$$\n'+formula+'\n$$\n\n'+FACTORING+'\n\n$$\n'+chain+'\n$$\n\n'+CONCLUSION+'\n\n$$\n'+final+'\n$$'


def prompt(p,spec):
    c = p['c']; kind='sum of' if c>0 else 'difference between'
    if spec.field=='radio':
        return 'Rewrite the expression $'+expr(p,spec.style)+'$ as the '+kind+' a perfect square and a constant.'
    opening='Rewrite the following expression as the '+kind+' a perfect square and a constant.'
    if spec.style=='spaced_power':
        return opening+'$'+expr(p,spec.style)+r' = ($ {{field-1}} $)^{2} '+('+' if c>0 else '-')+'$\n{{field-2}}'
    return opening+'\n\n$'+expr(p,spec.style)+r'=(${{field-1}}${)}^{2}\,'+('+' if c>0 else '-')+'$\n{{field-2}}'


def bank_values(p,spec,profile):
    a,b,v,c=p['a'],p['b'],p['variable'],p['c']
    transforms={'correct':(b,a),'sign':(b,-a),'double':(b,2*a),
        'quarter_linear':(b,sp.Rational(a,2)),'positive_double':(b,-2*a),
        'constant':(b,a*a),'positive_constant':(b,-a*a),
        'adjacent':(b,a+1),'positive_adjacent':(b,-a-1),
        'omit_variable_factor':(1,a),'use_squared_factor':(b*b,a)}
    values=[(name,square(v,*transforms[name],spec.style)+suffix(c,spec.style=='spaced_power')) for name in BANKS[profile]]
    maths=[(sp.Symbol(v)*transforms[name][0]-transforms[name][1])**2+c for name,_ in values]
    if len(set(sp.expand(x) for x in maths))!=5: raise ValueError('whole bank has equivalent options')
    return values


def check_parameters(level,template,parameters):
    p=dict(parameters)
    if set(p)!={'a','b','c','variable'}: raise ValueError('parameters require exactly a,b,c,variable')
    if any(type(p[k]) is not int for k in ('a','b','c')): raise ValueError('integer coefficients required')
    if p['variable'] not in ('x','y','t','z'): raise ValueError('unsupported variable')
    if not 1<=abs(p['c'])<=12: raise ValueError('outer constant is signed nonzero integer magnitude 1..12')
    if level=='easy':
        if not 2<=p['a']<=9 or p['b']!=1: raise ValueError('easy requires a=2..9,b=1')
    elif level=='moderate':
        if not 10<=p['a']<=15 or p['b']!=1: raise ValueError('moderate requires a=10..15,b=1')
    elif level=='hard':
        if not 2<=p['a']<=9 or not 2<=p['b']<=5 or sp.gcd(p['a'],p['b'])!=1: raise ValueError('hard requires coprime a=2..9,b=2..5')
    else: raise ValueError('unknown difficulty')
    if (level=='hard')!=(template.endswith('_scaled')): raise ValueError('template outside difficulty scope')
    return p


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    rng=random.Random(seed)
    if field_type: field_type=field_type.removeprefix(':answer-field.type/')
    if field_type not in (None,'radio','blank'): raise ValueError('unsupported field_type')
    raw=RAW_PROFILES.get(profile)
    if raw:
        if level!=raw['level']: raise ValueError('raw source replay authored routing level mismatch')
        if template and template!=raw['template']: raise ValueError('raw profile/template mismatch')
        template=raw['template']; bank=raw['bank_profile']
    else:
        eligible=[k for k,s in TEMPLATES.items() if (level=='hard')==k.endswith('_scaled') and (field_type is None or s.field==field_type)]
        if level not in ('easy','moderate','hard'): raise ValueError('unknown difficulty')
        if template is None: template=rng.choice(eligible)
        if template not in eligible: raise ValueError('ineligible template/field type')
        bank=profile
    spec=TEMPLATES[template]
    if field_type and spec.field!=field_type: raise ValueError('field_type incompatible with explicit template')
    if spec.field=='blank' and bank is not None: raise ValueError('blank has no bank profile')
    if spec.field=='radio':
        eligible_banks=['scaled_method'] if level=='hard' else ['half_coefficient','square_constant','both_constant_signs']
        if bank is None: bank=rng.choice(eligible_banks)
        if bank not in BANKS: raise ValueError('unknown profile')
        if not raw and bank not in eligible_banks: raise ValueError('opaque or incompatible bank requires public raw replay')
    if parameters is None:
        if raw: parameters=raw['parameters']
        else:
            a_values=list(range(10,16)) if level=='moderate' else list(range(2,10))
            if bank in ('square_constant','both_constant_signs'): a_values=[a for a in a_values if a!=2]
            a=rng.choice(a_values)
            bs=[b for b in range(2,6) if sp.gcd(a,b)==1] if level=='hard' else [1]
            parameters={'a':a,'b':rng.choice(bs),'c':rng.choice([i for i in range(-12,13) if i]),'variable':rng.choice(['x','y','t','z'])}
    p=check_parameters(level,template,parameters)
    learner_prompt=prompt(p,spec); worked=solution(p,spec)
    values=bank_values(p,spec,bank) if spec.field=='radio' else [('field-1',linear(p['variable'],p['b'])+'-'+str(p['a'])),('field-2',str(abs(p['c'])))]
    missing=raw['raw_missing'] if raw else []
    # Content identity reflects actual grading presence/value, never profile alias,
    # seed, option order or unused evidence metadata. Mathematical identity omits
    # variable aliases, layout, answer banks and the arbitrary profile spelling.
    content={'version':VERSION,'prompt':learner_prompt,'solution':None if 'solution' in missing else worked,
             'difficulty':None if 'difficulty' in missing else level,'field':spec.field,
             'banks':None if 'choices' in missing else sorted(v for _,v in values),
             'correct':None if 'correct' in missing else (values[0][1] if spec.field=='radio' else [v for _,v in values])}
    qid=uid(content)
    fields=[]
    keys=['selection'] if spec.field=='radio' else ['field-1','field-2']
    for i,key in enumerate(keys):
        field={':answer-field/id':uid([qid,key]),':answer-field/key':key,':answer-field/type':':answer-field.type/'+spec.field}
        fieldvalues=values if spec.field=='radio' else [values[i]]
        answers=[{':answer/id':uid([qid,key,value]),':answer/type':':answer.type/math',':answer/value':value} for recipe,value in fieldvalues]
        if 'choices' not in missing: field[':answer-field/choices']=answers
        if 'correct' not in missing: field[':answer-field/correct']=[':answer/id',answers[0][':answer/id']]
        if spec.field=='radio': rng.shuffle(answers)
        fields.append(field)
    q={':question/id':qid,':question/problem':learner_prompt,':question/answer-fields':fields}
    if 'difficulty' not in missing:q[':question/difficulty']=':question.difficulty/'+level
    if 'solution' not in missing:q[':question/worked-solution']=worked
    mathematical={'method':'negative isolated perfect square','a':p['a'],'b':p['b'],'c':p['c']}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
      'generation':{'version':VERSION,'seed':seed,'level':level,'template':template,'profile':profile or bank,'parameters':p,
        'mathematical_fingerprint':hashlib.sha256(canonical(mathematical).encode()).hexdigest(),
        'content_fingerprint':hashlib.sha256(canonical(content).encode()).hexdigest(),
        'source':SOURCE,'source_id':raw['source_id'] if raw else None,'source_refs':list(spec.sources),
        'raw_missing':missing,'evidence_only':bool(raw),'eligible_for_learning':not bool(raw),
        'bank_origin':'opaque observed adjacent pattern' if bank=='adjacent_opaque' else ('observed operation pattern' if level!='hard' else 'authored method'),
        'authored_extension':level=='hard' or (level=='moderate' and template!='radio_numeric') or (not raw and template.endswith('_spaced')),
        'completion_authored':not raw and template.endswith('_spaced'),
        'recipe_names':[name for name,_ in values],
        'plot_rating':'none','plot_assets':{},'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}


# Easy: monic isolated square; source layouts and three/four factoring rows.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)


# Moderate: larger integer square recognition, source a=11; same monic stages.
# Other source-shaped layouts here are authored same-method extensions.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)


# Hard: nonunit squared variable factor; requires matching both square roots and
# checking the negative cross product. No new operation or later-topic trick.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)


def markdown(record):
    q=record['question']; text=q[':question/problem']+'\n'
    for field in q.get(':question/answer-fields',[]):
        text+='\n'+field[':answer-field/key']+' ('+field[':answer-field/type'].split('/')[-1]+')\n'
        text+='\n'.join('$'+a[':answer/value']+'$' for a in field.get(':answer-field/choices',[]))+'\n'
    return text+'\n'+q.get(':question/worked-solution','[Source worked solution absent.]')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all')
    parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--format',choices=['markdown','json'],default='markdown')
    parser.add_argument('--template');parser.add_argument('--profile');parser.add_argument('--field-type')
    args=parser.parse_args()
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,args.template,args.field_type,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

if __name__=='__main__':main()
