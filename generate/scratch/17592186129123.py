#!/usr/bin/env python3
"""Midlines from extrema: steps 3–7, math basis 1356, no database operations.

The observed sine/cosine prompt masks share one average-of-extrema operation.
Raw source profiles preserve missing attributes and opaque banks for evidence;
they are never eligible for learner defaults. Every raw bank is parameterized
by exact affine positions relative to the center and half-range; this reproduces
evidence without claiming recovery of the unknown wrong-answer operations.

Normal profiles are separately authored complete method banks selected before
parameters. A collision rejects the whole instance. Difficulty is arithmetic:
easy integral extrema/even sum; moderate integral extrema/odd sum; hard reduced
nonintegral extrema with unequal denominators and common-denominator addition.
The latter two are explicit authored scope claims, not recovered source levels.
See the private extraction/evidence directory. No plots are needed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
import uuid
from functools import lru_cache
from pathlib import Path

import sympy as sp

KP_ID = 17592186129123
KP_UUID = '933b20c7-323f-5443-9cf4-97e87fa2c6fc'
TITLE = 'Finding the Midline of a Transformed Sinusoidal Function'
VERSION = 'midline-extrema-1'
ROOT = Path(__file__).with_suffix('')
SOURCE = json.loads((ROOT/'source.json').read_text())
QUESTIONS = {q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
TEMPLATES = ('sine_extrema', 'cosine_extrema')
NORMAL_PROFILES = ('method_average', 'method_reverse_difference', 'zero_minimum', 'zero_maximum')
RAW_PROFILES = tuple('raw_'+s for s in QUESTIONS)


def tex(value):
    return sp.latex(sp.Rational(value))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',',':')).encode()).hexdigest()


def uid(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), str(value)))


def source_parameters(q):
    m = re.search(r'transformed (sine|cosine).*minimum value of \$([^$]+)\$ and a maximum value of \$([^$]+)\$',q[':question/problem'])
    return {'minimum':str(sp.Rational(m[2])), 'maximum':str(sp.Rational(m[3].rstrip('.')))}


def parse_parameters(parameters):
    if set(parameters) != {'minimum','maximum'}:
        raise ValueError('Exactly minimum and maximum parameters are required.')
    try:
        lo, hi = (sp.Rational(parameters[k]) for k in ('minimum','maximum'))
    except (TypeError,ValueError) as exc:
        raise ValueError('Extrema must be exact finite rational values.') from exc
    if not lo < hi or max(abs(lo),abs(hi)) > 16:
        raise ValueError('Require minimum < maximum and absolute extrema at most 16.')
    return lo,hi


def workload_eligible(level, lo, hi):
    """Apply disjoint workload bounds to reduced mathematical values."""
    if level == 'easy':
        return lo.q == hi.q == 1 and (lo+hi).q == 1 and int(lo+hi)%2 == 0
    if level == 'moderate':
        return lo.q == hi.q == 1 and int(lo+hi)%2 != 0
    if level == 'hard':
        return (lo.q in (2,3,4,6) and hi.q in (2,3,4,6) and lo.q != hi.q
                and 6 <= sp.ilcm(lo.q,hi.q) <= 12 and (lo+hi).q > 1)
    raise ValueError('Difficulty must be easy, moderate, or hard.')


def normal_values(profile, lo, hi):
    center, amplitude = (lo+hi)/2, (hi-lo)/2
    if profile == 'method_average':
        values = (center, lo, hi, amplitude, lo+hi)
        recipes = ('average','use_minimum','use_maximum','use_half_difference','omit_division_by_two')
    elif profile == 'method_reverse_difference':
        values = (center, lo, hi, (lo-hi)/2, lo+hi)
        recipes = ('average','use_minimum','use_maximum','subtract_extrema_instead_of_add','omit_division_by_two')
    elif profile == 'zero_minimum':
        if lo != 0: raise ValueError('zero_minimum requires minimum zero.')
        values = (center, lo, hi, -hi, -(lo+hi)/2)
        recipes = ('average','use_minimum','use_maximum','negate_maximum','negate_average')
    elif profile == 'zero_maximum':
        if hi != 0: raise ValueError('zero_maximum requires maximum zero.')
        values = (center, lo, hi, -lo, -(lo+hi)/2)
        recipes = ('average','use_minimum','use_maximum','negate_minimum','negate_average')
    else:
        raise ValueError('Unknown authored bank profile.')
    if len(set(values)) != 5:
        raise ValueError('Complete selected bank has equivalent choices; reject whole instance.')
    return values,recipes


@lru_cache(None)
def parameter_domain(level, profile):
    """Finite exact domains; zero profiles are only eligible at integral levels."""
    if level == 'hard':
        numbers = sorted({sp.Rational(n,d) for d in (2,3,4,6) for n in range(-16*d,16*d+1)
                          if sp.Rational(n,d).q == d})
    else:
        numbers = list(map(sp.Rational,range(-16,17)))
    valid=[]
    for i,lo in enumerate(numbers):
        for hi in numbers[i+1:]:
            if not workload_eligible(level,lo,hi): continue
            try: normal_values(profile,lo,hi)
            except ValueError: continue
            valid.append((lo,hi))
    return tuple(valid)


def solution(lo, hi, level='easy'):
    """Source sentences and ordered substitution, sum, division, conclusion."""
    prefix = QUESTIONS['q-236896'][':question/worked-solution'].split('\\begin{aligned}')[0]
    second = '('+tex(hi)+')' if hi < 0 else tex(hi)
    common=''
    if level == 'hard':
        lcd=sp.ilcm(lo.q,hi.q)
        nt=tex(lo*lcd)
        pt=tex(hi*lcd)
        pt='('+r'\frac{'+pt+'}{'+str(lcd)+'})' if hi<0 else r'\frac{'+pt+'}{'+str(lcd)+'}'
        common=r' \\  & =\frac{\frac{'+nt+'}{'+str(lcd)+'}+'+pt+r'}{2}'
    rows = (r'\begin{aligned}\frac{{y}_{\text{min}}+{y}_{\text{max}}}{2} & =\frac{'
            +tex(lo)+'+'+second+r'}{2}'+common+r' \\  & =\frac{'+tex(lo+hi)
            +r'}{2} \\  & ='+tex((lo+hi)/2)+r'.\end{aligned}')
    return prefix+rows+'\n$$\n\nTherefore, the midline is $y='+tex((lo+hi)/2)+'.$'


def raw_values(q,lo,hi):
    """Affine evidence profiles. Unknown error interpretations remain opaque."""
    original = source_parameters(q)
    a,b = sp.Rational(original['minimum']),sp.Rational(original['maximum'])
    old_center,old_amplitude = (a+b)/2,(b-a)/2
    values=[]
    for choice in q.get(':question/answer-fields',[{}])[0].get(':answer-field/choices',[]):
        text = choice[':answer/value']
        value = sp.Rational(text.split('=')[1].strip())
        ratio = (value-old_center)/old_amplitude
        changed = (lo+hi)/2+ratio*(hi-lo)/2
        # Slot only the complete RHS; source equality whitespace is retained.
        rhs = text.split('=')[1]
        whitespace = rhs[:len(rhs)-len(rhs.lstrip())]
        values.append((text.split('=')[0]+'='+whitespace+tex(changed), changed, str(ratio)))
    return values


def generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None):
    if level not in ('easy','moderate','hard'): raise ValueError('Unknown difficulty.')
    if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('Only radio fields are supported.')
    rng=random.Random(seed)
    raw = profile is not None and profile.startswith('raw_')
    original = QUESTIONS.get(profile[4:]) if raw else None
    if raw and original is None: raise ValueError('Unknown raw profile.')
    source_template = ('cosine' if 'transformed cosine' in original[':question/problem'] else 'sine')+'_extrema' if raw else None
    if template is None: template=source_template or rng.choice(TEMPLATES)
    if template not in TEMPLATES or (raw and template != source_template): raise ValueError('Invalid template for profile.')
    if profile is None:
        # Choose a complete bank before drawing its parameter tuple.
        eligible=[p for p in NORMAL_PROFILES if parameter_domain(level,p)]
        if parameters is not None:
            # Explicit inputs are already fixed: filter complete bank eligibility,
            # never change those inputs or replace individual bank members.
            explicit_lo,explicit_hi=parse_parameters(parameters)
            eligible=[]
            for candidate in NORMAL_PROFILES:
                try: normal_values(candidate,explicit_lo,explicit_hi)
                except ValueError: continue
                eligible.append(candidate)
        if not eligible: raise ValueError('No complete authored bank is eligible for the explicit instance.')
        profile=rng.choice(eligible)
    if not raw and profile not in NORMAL_PROFILES: raise ValueError('Unknown profile.')
    if parameters is None:
        if raw: raise ValueError('Raw evidence replay requires explicit parameters.')
        lo,hi=rng.choice(parameter_domain(level,profile))
    else:
        lo,hi=parse_parameters(parameters)
    if not raw and not workload_eligible(level,lo,hi): raise ValueError('Parameters violate difficulty workload bounds.')
    if raw and level != 'easy': raise ValueError('All observed/raw sources belong to easy; q236750 is authored-assigned easy.')
    center=(lo+hi)/2
    kind=template.split('_')[0]
    terminal='$.' if raw and ':question/worked-solution' not in original else '.$'
    prompt=f'Find the equation of the midline for a transformed {kind} function with a minimum value of ${tex(lo)}$ and a maximum value of ${tex(hi)}'+terminal
    if raw:
        bank=raw_values(original,lo,hi)
        values=[x[1] for x in bank]
        texts=[x[0] for x in bank]
        recipes=['opaque_affine_position_'+x[2] for x in bank]
    else:
        values,recipes=normal_values(profile,lo,hi)
        texts=['y='+tex(v) for v in values]
    if len(set(values)) != len(values): raise ValueError('Ambiguous raw bank under changed parameters.')
    solved=solution(lo,hi,level)
    payload={'version':VERSION,'difficulty':None if raw and ':question/difficulty' not in original else level,
             'prompt':prompt,'solution':solved if not raw or ':question/worked-solution' in original else None,
             'bank':sorted(texts),'field_presence':not raw or ':question/answer-fields' in original,
             'correct_presence':not raw or any(':answer-field/correct' in f for f in original.get(':question/answer-fields',[]))}
    content_hash=digest(payload)
    qid=uid(content_hash)
    question={':question/id':qid,':question/problem':prompt}
    if not raw or ':question/difficulty' in original: question[':question/difficulty']=':question.difficulty/'+level
    if not raw or ':question/worked-solution' in original: question[':question/worked-solution']=solved
    fields=[]
    recipe_metadata={}
    if not raw or ':question/answer-fields' in original:
        fid=uid(qid+':selection')
        choices=[]
        for i,(text,val,recipe) in enumerate(zip(texts,values,recipes)):
            aid=uid(fid+':'+text)
            choice={':answer/id':aid,':answer/type':':answer.type/math',':answer/value':text}
            if raw: choice[':db/id']=original[':question/answer-fields'][0][':answer-field/choices'][i][':db/id']
            choices.append(choice)
            recipe_metadata[aid]={'recipe':recipe,'value':str(val)}
        rng.shuffle(choices)
        field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
        if not raw or ':answer-field/correct' in original[':question/answer-fields'][0]:
            value_by_text=dict(zip(texts,values))
            field[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in choices if value_by_text[a[':answer/value']]==center)]
        if raw: field[':db/id']=original[':question/answer-fields'][0][':db/id']
        fields.append(field)
        question[':question/answer-fields']=fields
    if raw:
        question[':db/id']=original[':db/id']
        question[':question/math-academy-id']=original[':question/math-academy-id']
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,
            'generation':{'version':VERSION,'difficulty':level,'template':template,'bank_profile':profile,'seed':seed,
                          'parameters':{'minimum':str(lo),'maximum':str(hi)},'domain':{'absolute_extrema_max':16,'response':'complete horizontal-line equation'},
                          'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_id':original[':question/math-academy-id'] if raw else None,
                          'evidence_only':raw,'eligible_for_learning':not raw,'authored_level':not raw and level != 'easy',
                          'answer_math':str(center),'recipes':recipe_metadata,'content_hash':content_hash,
                          'mathematical_fingerprint':digest({'assessment':'mean_of_two_extrema','minimum':str(lo),'maximum':str(hi)}),
                          'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plots':[]}}


# EASY: observed integral extrema with even sum. Zero extrema use separate banks.
def generate_easy(seed=0, **kwargs):
    return generate('easy',seed,**kwargs)


# MODERATE: authored odd integer sum; same average, nonintegral half-integer answer.
def generate_moderate(seed=0, **kwargs):
    return generate('moderate',seed,**kwargs)


# HARD: authored unequal reduced denominators, LCD 6 or 12, noninteger sum.
def generate_hard(seed=0, **kwargs):
    return generate('hard',seed,**kwargs)


def markdown(record):
    q=record['question']
    rows=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        rows.extend(f'- ${a[":answer/value"]}$' for a in f[':answer-field/choices'])
    if ':question/worked-solution' in q: rows.extend(['',q[':question/worked-solution']])
    return '\n'.join(rows)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all')
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--format',choices=('markdown','json'),default='markdown')
    parser.add_argument('--template',choices=TEMPLATES)
    parser.add_argument('--profile',choices=NORMAL_PROFILES+RAW_PROFILES)
    parser.add_argument('--parameters',type=json.loads)
    args=parser.parse_args()
    levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile,parameters=args.parameters) for l in levels for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
