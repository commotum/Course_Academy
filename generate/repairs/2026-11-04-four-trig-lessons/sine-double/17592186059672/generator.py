#!/usr/bin/env python3
"""Two linked double-angle applications. Seeded, relocatable, database-free."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import random
import uuid
import sympy as sp
from math_format import normalize_prose, normalize_tex, validate_generated_record

VERSION = '2.1.0'
KP = 17592186059672
ENDS = (30, 45, 60, 90, 135, 150, 210, 225, 270, 300, 315, 330)
GROUPS = ((30, 150, 210, 330), (45, 135, 225, 315), (60, 300), (90, 270))
NAMESPACE = uuid.UUID('174eb3cd-4bd9-457e-88c5-9caf43e99ae5')

def standard_intermediate(end):
    half=sp.Rational(end)/2
    return half % 30 == 0 or half % 45 == 0

TWO_APPLICATION_ENDS=tuple(end for end in ENDS if not standard_intermediate(end))

def tex(v):
    return normalize_tex(sp.latex(sp.simplify(v)))

def angle(degrees, unit):
    d = sp.Rational(degrees)
    if unit == 'degrees':
        # Sampled degree angles have terminating decimal representations.
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

def cancellation_bank(c, end, unit, rng):
    """Source-like symbolic error recipes; no evaluation of unnecessary angles."""
    a = sp.Rational(c, 2)
    small, doubled = angle(sp.Rational(end)/4, unit), angle(sp.Rational(end)/2, unit)
    x=float(end)*math.pi/720
    candidates = [(tex(2*a), float(2*a), 'omitted half-factor'),
                  (tex(a/2), float(a/2), 'applied a half-factor twice'),
                  (tex(4*a), float(4*a), 'multiplied by two instead of dividing by two'),
                  (times(a,trig('sin',doubled)),float(a)*math.sin(2*x),'dropped cosecant without cancellation'),
                  (times(a,trig('csc',small)),float(a)/math.sin(x),'retained the wrong reciprocal angle'),
                  (times(a/2,trig('csc',small)),float(a/2)/math.sin(x),'extra half-factor and wrong reciprocal angle'),
                  (times(a,trig('cos',doubled)),float(a)*math.cos(2*x),'used cosine after doubling'),
                  (times(2*a,trig('sin',doubled)),float(2*a)*math.sin(2*x),'retained coefficient and dropped cosecant')]
    for _ in range(100):
        selected=rng.sample(candidates,4)
        # A numerical key must not be the only numerical option.
        if not any(not any('\\'+f in t for f in ('sin','cos','csc')) for t,_,_ in selected):continue
        vals=[float(a)]+[v for _,v,_ in selected]
        if all(abs(v-w)>1e-9 for i,v in enumerate(vals) for w in vals[:i]):
            choices=[(tex(a),'correct')]+[(t,why) for t,_,why in selected]
            rng.shuffle(choices);return choices
    raise ValueError('Cancellation instance cannot supply a distinct source-like bank')

def symbolic_bank(c,end,unit,rng):
    c=sp.Rational(c)
    key=(c/4,1)
    candidates=[(c/2,1,'omit a half-factor'),(c,1,'omit both half-factors'),
                (c/8,1,'add an extra half-factor'),(c/4,sp.Rational(1,2),'stop after one angle doubling'),
                (c/2,sp.Rational(1,2),'miss a half-factor and stop early'),
                (c/4,2,'double the angle once too often'),
                (c/8,2,'add a half-factor and double once too often')]
    for _ in range(100):
        selected=rng.sample(candidates,4)
        specs=[key]+[(scale,freq) for scale,freq,_ in selected]
        vals=[float(scale)*math.sin(float(end)*float(freq)*math.pi/180) for scale,freq in specs]
        if all(abs(v-w)>1e-9 for i,v in enumerate(vals) for w in vals[:i]):
            choices=[(times(c/4,trig('sin',angle(end,unit))),'correct')]+[(times(scale,trig('sin',angle(sp.Rational(end)*freq,unit))),why) for scale,freq,why in selected]
            rng.shuffle(choices);return choices
    raise ValueError('Symbolic product has a degenerate bank')


def construct(difficulty, end, c, unit, family='product', profile=0, rng=None, replay=None, _with_bank_cue=False, symbolic=False):
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
    symbolic = symbolic or bool(replay and replay.get('symbolic'))
    if symbolic:
        answer = times(c/4,sd) if family!='sec_over_pair' else frac(tex(4*c),sd)
    prompt = 'Without using a calculator, find the exact value of\n$$\n'+expression+'.\n$$'
    if symbolic and not replay:
        prompt = 'Express the following as a constant multiple of a single trigonometric ratio.\n$$\n'+expression+'.\n$$'
    shape = 'blank' if difficulty == 'hard' else 'radio'
    if replay:
        shape = replay['shape']
    if shape == 'blank':
        prompt += '\n{{field-1}}'
    solution = 'Let $E$ denote the given expression. '+explanation+'\n'+display(rows)
    if family != 'cancellation' and not symbolic:
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
            choices = cancellation_bank(c, end, unit, rng)
        elif symbolic:
            choices = symbolic_bank(c,end,unit,rng)
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
    source_ids = ['b22f045c-0b9c-53f1-b536-66fda02ca447'] if family=='product' else ['6a88295e-a9f4-5381-9209-7cdc6c3b161d','5749738c-9ac0-51f9-9b71-e3d7fdfbde49'] if family=='pair_over_sec' else ['4fabc70d-25ca-5a30-9a52-90a915524efa','19bb82ee-2583-57ae-92ec-48971505d385']
    if family=='cancellation':source_ids=['f30309d1-f3e3-55ac-be8a-acbe0c0f980a','8883bfa3-8f36-5e8a-8a63-990442c2b246']
    if symbolic and family=='product':source_ids=['91b3ae38-a411-55e5-ba0c-b0976c1d82dd']
    if replay:source_ids=[replay['id']]
    record = {'knowledge_point':KP,'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[field]},'generation':{'generator_version':VERSION,'template':family,'parameters':{'end_degrees':str(end),'coefficient':str(c),'unit':unit},'symbolic_terminal':symbolic, 'historical_single_application_bypass':bool(replay and family!='cancellation' and standard_intermediate(end)), 'difficulty_basis':'workload-sensitive reclassification; independent easy is authored from product sources', 'bank_profile':'source-replay' if replay else profile if shape=='radio' else None,'choice_errors':{a[':answer/id']:why for a,(_,why) in zip(answers,choices)},'source_question_ids':source_ids,'angle_chain':[a,b,d],'shown_final':answer,'domain':'All displayed trigonometric factors and denominators are defined.'}}
    record = validate_generated_record(record)
    return (record, modal_cue) if _with_bank_cue else record

def generate(difficulty, count, seed):
    if difficulty == 'unclassified':difficulty='moderate'
    if count < 0:raise ValueError('count must be nonnegative')
    if difficulty=='easy' and count>4:raise ValueError('Easy supports four distinct two-application instances; count must be at most 4')
    rng = random.Random(seed)
    families={'easy':['product'], 'moderate':['cancellation','product','cancellation','symbolic_product'],
              'hard':['pair_over_sec','sec_over_pair']}[difficulty]
    schedule=families.copy();rng.shuffle(schedule)
    out=[];seen=set()
    for i in range(count):
        if i and i%len(schedule)==0:rng.shuffle(schedule)
        selected=schedule[i%len(schedule)]
        symbolic=selected=='symbolic_product'
        family='product' if symbolic else selected
        for attempt in range(300):
            unit=rng.choice(('degrees','radians'))
            if symbolic:
                unit='radians'
                end=rng.choice([sp.Rational(45,2),sp.Rational(135,2),sp.Rational(225,2),sp.Rational(315,2)])
                c=rng.choice((2,4,6,8))
            elif family=='cancellation':
                # Includes the five imported cancellation cases at their actual angles.
                end=4*rng.choice((17,25,35,40,55,65,70,75,80)) if unit=='degrees' else rng.choice([sp.Rational(720,n) for n in (5,7,9,10,11)])
                c=rng.choice((2,4,6,8,10))
            else:
                endpoints=(30,45) if difficulty=='easy' else TWO_APPLICATION_ENDS
                end=rng.choice(endpoints)
                c=rng.choice((4,8)) if difficulty=='easy' else rng.choice((1,2)) if difficulty=='hard' else rng.choice((1,2,3,4,6))
            # Unit spelling, bank permutation and error profile do not create a new instance.
            semantic=(family,str(end),str(c),symbolic)
            if semantic in seen:continue
            try:
                record,cue=construct(difficulty,end,c,unit,family,rng.randrange(6),rng,symbolic=symbolic,_with_bank_cue=True)
                if family=='product' and not symbolic and cue:
                    for profile in rng.sample(range(6),6):
                        candidate,cue=construct(difficulty,end,c,unit,family,profile,rng,_with_bank_cue=True)
                        if not cue:
                            record=candidate;break
                    else:continue
            except ValueError:continue
            seen.add(semantic)
            record['generation'].update(seed=seed,index=i)
            out.append(record);break
        else:raise ValueError('Requested batch exceeds distinct mathematical instances for a scheduled family')
    return out

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
