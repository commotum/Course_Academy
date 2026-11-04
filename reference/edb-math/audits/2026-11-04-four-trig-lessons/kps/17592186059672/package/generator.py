#!/usr/bin/env python3
"""Two linked double-angle applications. Seeded, relocatable, database-free."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import uuid
import sympy as sp
from math_format import normalize_prose, normalize_tex, validate_generated_record

VERSION = '1.0.1'
KP = 17592186059672
ENDS = (30, 45, 60, 90, 135, 150, 210, 225, 270, 300, 315, 330)
GROUPS = ((30, 150, 210, 330), (45, 135, 225, 315), (60, 300), (90, 270))
NAMESPACE = uuid.UUID('174eb3cd-4bd9-457e-88c5-9caf43e99ae5')

def tex(v):
    return normalize_tex(sp.latex(sp.simplify(v)))

def angle(degrees, unit):
    d = sp.Rational(degrees)
    if unit == 'degrees':
        # All ordinary degree angles are terminating quarter-degree numbers.
        n = str(float(d)).rstrip('0').rstrip('.') if d.q != 1 else str(d.p)
        return n + r'^\circ'
    return tex(d * sp.pi / 180)

def trig(name, a):
    return '\\' + name + r'\left(' + a + r'\right)'

def times(c, value):
    return value if c == 1 else tex(c) + r'\,' + value

def frac(a, b):
    return r'\frac{' + a + '}{' + b + '}'

def display(rows):
    return '$$\n' + r'\begin{aligned}' + '\n' + r'\\'.join(rows) + '\n' + r'\end{aligned}' + '\n$$'

def uid(payload):
    return str(uuid.uuid5(NAMESPACE, payload))

def bank(c, s, profile, rng, raw=False):
    """Sample a complete error profile, then reject collisions as a whole."""
    k = sp.Rational(c, 4)
    a = sp.simplify(k*s)
    others = [v*sp.sign(s) for v in (sp.Rational(1,2), sp.sqrt(2)/2, sp.sqrt(3)/2, sp.Integer(1)) if v != abs(s)]
    for _ in range(100):
        rng.shuffle(others)
        if profile == 0:
            errors = [(a/2, 'extra half-factor'), (2*a, 'omitted half-factor'), (k*others[0], 'wrong endpoint sine'), (k*others[1], 'wrong endpoint sine')]
        elif profile == 1:
            errors = [(a/4, 'two extra half-factors'), (a/2, 'extra half-factor'), (2*a, 'omitted half-factor'), (k*others[0], 'wrong endpoint sine')]
        elif profile == 2:
            errors = [(2*a, 'omitted half-factor'), (4*a, 'both half-factors omitted'), (k*others[0], 'wrong endpoint sine'), (k*others[1]/2, 'extra half-factor and wrong endpoint sine')]
        elif profile == 3:
            errors = [(a/2, 'extra half-factor'), (k*others[0]*2, 'omitted half-factor and wrong endpoint sine'), (k*others[1]/2, 'extra half-factor and wrong endpoint sine'), (k*others[2], 'wrong endpoint sine')]
        elif profile == 4:
            errors = [(2*a, 'omitted half-factor'), (4*a, 'both half-factors omitted'), (2*k*others[0], 'omitted half-factor and wrong endpoint sine'), (2*k*others[1], 'omitted half-factor and wrong endpoint sine')]
        else:
            errors = [(a/2, 'extra half-factor'), (a/4, 'two extra half-factors'), (k*others[0]/2, 'extra half-factor and wrong endpoint sine'), (k*others[1]/2, 'extra half-factor and wrong endpoint sine')]
        values = [(a, 'correct')] + [(sp.simplify(v), why) for v,why in errors]
        if len({sp.srepr(v) for v,_ in values}) == 5:
            rng.shuffle(values)
            return values if raw else [(tex(v), why) for v,why in values]
    raise ValueError('No distinct bank in complete error profile')

def cancellation_bank(c, sine, cosine, rng):
    """Errors in the displayed one-identity-and-reciprocal cancellation path."""
    a = sp.Rational(c, 2)
    candidates = [
        (2*a, 'omitted half-factor'),
        (a/2, 'applied a half-factor twice'),
        (4*a, 'multiplied by two instead of dividing by two'),
        (a*sine, 'dropped the cosecant without cancelling the sine'),
        (a/sine, 'dropped the sine without cancelling the cosecant'),
        (a*cosine, 'used cosine instead of sine after doubling'),
        (a/cosine, 'used secant instead of cosecant'),
    ]
    unique = {}
    for value, why in candidates:
        value = sp.simplify(value)
        if value.is_finite and sp.simplify(value-a) != 0:
            unique.setdefault(sp.srepr(value), (value, why))
    errors = list(unique.values())
    if len(errors) < 4:
        raise ValueError('Cancellation instance cannot supply four distinct plausible errors')
    rng.shuffle(errors)
    values = [(a, 'correct')] + errors[:4]
    rng.shuffle(values)
    return [(tex(value), why) for value, why in values]

def construct(difficulty, end, c, unit, family='product', profile=0, rng=None, replay=None, _with_bank_cue=False):
    rng = rng or random.Random(0)
    c = sp.Rational(c)
    a,b,d = (angle(sp.Rational(end)*i/4, unit) for i in (1,2,4))
    sa,ca,cb,sb,sd = trig('sin',a),trig('cos',a),trig('cos',b),trig('sin',b),trig('sin',d)
    pair = sa+ca
    s = sp.simplify(sp.sin(sp.Rational(end)*sp.pi/180))
    if family == 'product':
        expression = times(c, pair+cb)
        rows = [r'E&=' + times(c/2, sb+cb), r'&=' + times(c/4, sd)]
        answer = tex(c*s/4)
        explanation = 'Use $\\sin x\\cos x=\\frac{1}{2}\\sin(2x)$ first at $x='+a+'$ and then at $x='+b+'$. Each application introduces a factor of $\\frac{1}{2}$.'
    elif family == 'pair_over_sec':
        expression = frac(times(c,pair),trig('sec',b))
        rows = [r'E&=' + frac(times(c/2,sb),trig('sec',b)), r'&=' + times(c/2,sb+cb), r'&=' + times(c/4,sd)]
        answer = tex(c*s/4)
        explanation = 'Apply $\\sin x\\cos x=\\frac{1}{2}\\sin(2x)$ at $x='+a+'$. Dividing by secant multiplies by cosine because $1/\\sec x=\\cos x$. The resulting pair at $x='+b+'$ permits a second application.'
    elif family == 'sec_over_pair':
        expression = frac(times(c,trig('sec',b)),pair)
        rows = [r'E&=' + frac(times(2*c,trig('sec',b)),sb), r'&=' + frac(tex(2*c),sb+cb), r'&=' + frac(tex(4*c),sd)]
        answer = tex(4*c/s)
        explanation = 'Apply $\\sin x\\cos x=\\frac{1}{2}\\sin(2x)$ at $x='+a+'$ in the denominator. Use $\\sec x=1/\\cos x$, then apply the double-angle identity again at $x='+b+'$.'
    elif family == 'cancellation':
        expression = times(c,pair+trig('csc',b))
        rows = [r'E&=' + times(c/2,sb+trig('csc',b)), r'&=' + times(c/2,frac(sb,sb)), r'&='+tex(c/2)]
        answer = tex(c/2)
        explanation = 'Use $\\sin x\\cos x=\\frac{1}{2}\\sin(2x)$ at $x='+a+'$, then $\\csc x=1/\\sin x$. The nonzero sine cancels.'
    else:
        raise ValueError(family)
    if replay and replay.get('symbolic'):
        answer = times(c/4,sd)
    prompt = 'Without using a calculator, find the exact value of\n$$\n'+expression+'.\n$$'
    if difficulty == 'easy':
        prompt += '\nUse $2\\sin x\\cos x=\\sin(2x)$, first with $x='+a+'$ and then with $x='+b+'$.'
    shape = 'blank' if difficulty == 'hard' else 'radio'
    if replay:
        shape = replay['shape']
    if shape == 'blank':
        prompt += '\n{{field-1}}'
    solution = 'Let $E$ denote the given expression. '+explanation+'\n'+display(rows)
    if family != 'cancellation' and not (replay and replay.get('symbolic')):
        solution += '\nThe terminal sine is $'+sd+'='+tex(s)+'$.\n'
        evaluated = frac(tex(4*c),r'\left('+tex(s)+r'\right)') if family == 'sec_over_pair' else times(c/4,r'\left('+tex(s)+r'\right)')
        final_rows = [r'E&='+evaluated]
        if family == 'sec_over_pair' and abs(s) in (sp.sqrt(2)/2,sp.sqrt(3)/2):
            m = 2 if abs(s) == sp.sqrt(2)/2 else 3
            final_rows.append(r'&='+frac(tex(8*c*sp.sign(s)),r'\sqrt{'+str(m)+'}'))
            solution += 'Rationalize the denominator by multiplying numerator and denominator by $\\sqrt{'+str(m)+'}$:\n'
        else:
            solution += 'Therefore,\n'
        final_rows.append(r'&='+answer+'.')
        solution += display(final_rows)
    choices = [(answer,'correct')]
    modal_cue = False
    if shape == 'radio':
        if family == 'cancellation':
            choices = cancellation_bank(c, sp.sin(sp.Rational(end)*sp.pi/360), sp.cos(sp.Rational(end)*sp.pi/360), rng)
        else:
            raw_choices = bank(c, s, profile, rng, raw=True)
            choices = [(tex(v), why) for v, why in raw_choices]
            parts = [sp.simplify(v).as_coeff_Mul() for v, _ in raw_choices]
            coeffs = Counter(p[0] for p in parts)
            radicals = Counter(p[1] for p in parts)
            candidates = [i for i, p in enumerate(parts) if coeffs[p[0]] == max(coeffs.values()) and radicals[p[1]] == max(radicals.values())]
            correct = next(i for i, (_, why) in enumerate(raw_choices) if why == 'correct')
            modal_cue = candidates == [correct]
    if replay:
        choices = [(normalize_tex(v), 'correct' if i == replay['correct_index'] else 'source distractor') for i,v in enumerate(replay['choices'])]
        answer = choices[replay['correct_index']][0]
    problem, solution = normalize_prose(prompt), normalize_prose(solution)
    values = [normalize_tex(v) for v,_ in choices]
    # Include complete authored banks in identity; never seed/index/UUID noise.
    identity = json.dumps([difficulty,problem,solution,sorted(values)],ensure_ascii=False)
    qid = uid(identity)
    answers = [{':answer/id':uid(qid+':answer:'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct_id = answers[values.index(answer)][':answer/id']
    field = {':answer-field/id':uid(qid+':field'),':answer-field/key':'field-1' if shape=='blank' else 'selection',':answer-field/type':':answer-field.type/'+shape,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}
    source_ids = ['b22f045c-0b9c-53f1-b536-66fda02ca447','0abb88c3-b1d8-5fd6-9259-e93980f1b3ad'] if family=='product' else ['87e7afa8-1798-5127-a9ff-a08924db07de','6a88295e-a9f4-5381-9209-7cdc6c3b161d'] if family=='pair_over_sec' else ['4fabc70d-25ca-5a30-9a52-90a915524efa','1043af1e-be8e-50e8-a088-c079feee421f']
    if family=='cancellation':source_ids=['f30309d1-f3e3-55ac-be8a-acbe0c0f980a','8883bfa3-8f36-5e8a-8a63-990442c2b246']
    if difficulty=='easy':source_ids=['23700599-02b8-5b30-905e-86d4d7a86aa5']
    if replay:source_ids=[replay['id']]
    record = {'knowledge_point':KP,'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[field]},'generation':{'generator_version':VERSION,'template':family,'parameters':{'end_degrees':str(end),'coefficient':str(c),'unit':unit},'bank_profile':'source-replay' if replay else profile if shape=='radio' else None,'choice_errors':{a[':answer/id']:why for a,(_,why) in zip(answers,choices)},'source_question_ids':source_ids,'angle_chain':[a,b,d],'shown_final':answer,'domain':'All displayed trigonometric factors and denominators are defined.'}}
    record = validate_generated_record(record)
    return (record, modal_cue) if _with_bank_cue else record

def generate(difficulty, count, seed):
    if difficulty == 'unclassified':difficulty='moderate'
    if count < 0:raise ValueError('count must be nonnegative')
    rng = random.Random(seed)
    records=[]; cues=[]; groups=list(range(4)); rng.shuffle(groups)
    families=('pair_over_sec','sec_over_pair') if difficulty=='hard' else ('product',)
    coefficients=(1,2,3) if difficulty=='hard' else (1,2,3,4,6,8)
    def catalog():
        pools={}
        for group in range(4):
            endpoints=[e for e in GROUPS[group] if difficulty!='easy' or e<180]
            pools[group]=[(family,e,c,unit) for family in families for e in endpoints for c in coefficients for unit in ('degrees','radians')]
            rng.shuffle(pools[group])
        return pools
    pools=catalog();capacity=sum(map(len,pools.values()))
    for i in range(count):
        # Exhaust distinct mathematical presentations before sampling another epoch.
        # Small batches visit each sine-magnitude decision case before repetition.
        if not any(pools.values()):pools=catalog()
        group=next(groups[(i+j)%4] for j in range(4) if pools[groups[(i+j)%4]])
        family,end,c,unit=pools[group].pop()
        profile=(i+seed+i//4)%6
        record,cue=construct(difficulty,end,c,unit,family,profile,rng,_with_bank_cue=True)
        record['generation'].update(seed=seed,index=i,finite_presentation_capacity=capacity)
        records.append(record); cues.append(cue)
    if difficulty != 'hard':
        # A complete error bank must not make its modal coefficient/radical
        # intersection a perfect answer rule in a visible sign or unit subgroup.
        # Keep every chosen mathematical instance; replace a whole error profile.
        subgroups = [list(range(len(records)))]
        for unit in ('degrees', 'radians'):
            subgroups.append([i for i, r in enumerate(records) if r['generation']['parameters']['unit'] == unit])
        for sign in (-1, 1):
            subgroups.append([i for i, r in enumerate(records) if sp.sign(sp.sin(sp.Rational(r['generation']['parameters']['end_degrees'])*sp.pi/180)) == sign])
        for indices in subgroups:
            if len(indices) < 2 or not all(cues[i] for i in indices):
                continue
            i = indices[-1]
            params = records[i]['generation']['parameters']
            profiles = list(range(6)); rng.shuffle(profiles)
            for profile in profiles:
                candidate, cue = construct(difficulty, sp.Rational(params['end_degrees']), sp.Rational(params['coefficient']), params['unit'], 'product', profile, rng, _with_bank_cue=True)
                if not cue:
                    for name in ('seed', 'index', 'finite_presentation_capacity'):
                        candidate['generation'][name] = records[i]['generation'][name]
                    records[i], cues[i] = candidate, cue
                    break
            else:
                raise ValueError('No complete error profile defeats the conditional modal bank cue')
    return records

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=('easy','moderate','hard','unclassified'),default='moderate')
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=('json',),default='json')
    parser.add_argument('--replay-source',help='Replay complete source evidence at its original parameters (not ordinary sampling).')
    args=parser.parse_args()
    if args.replay_source:
        catalog=json.loads(Path(__file__).with_name('source-replay.json').read_text())
        item=next(x for x in catalog if x['id']==args.replay_source)
        records=[construct(item['difficulty'],sp.Rational(item['end']),item['c'],item['unit'],item['family'],replay=item)]
    else:records=generate(args.difficulty,args.count,args.seed)
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
