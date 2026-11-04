#!/usr/bin/env python3
"""Seeded, relocatable cosine double-angle practice. No database or assets."""
import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = 17592186087671
TITLE = 'Finding Exact Values of Trigonometric Expressions Using the Double-Angle Formula'
NS = uuid.UUID('bcaa0451-4344-498d-93cd-87b9a552850e')
# Values at doubled angles. The table is an implementation, not the verifier.
COS = {30:r'\frac{\sqrt{3}}{2}',45:r'\frac{\sqrt{2}}{2}',60:r'\frac{1}{2}',
       90:'0',120:r'-\frac{1}{2}',135:r'-\frac{\sqrt{2}}{2}',150:r'-\frac{\sqrt{3}}{2}',
       210:r'-\frac{\sqrt{3}}{2}',225:r'-\frac{\sqrt{2}}{2}',240:r'-\frac{1}{2}',
       270:'0',300:r'\frac{1}{2}',315:r'\frac{\sqrt{2}}{2}',330:r'\frac{\sqrt{3}}{2}'}
DIRECT = [30,45,135,150,210,225,315,330]
SQUARE = list(DIRECT)  # Original angles stay unfamiliar; no zero known-angle bypass.
ANCHORS = {'difference':['q-24514','q-120367','q-332138','q-332139'],
           'sine':['q-26706','q-120369','q-332147','q-7473'],
           'cosine':[], 'square':['q-275706','q-332148','q-332150']}


def uid(text):
    return str(uuid.uuid5(NS, text))


def angle(degrees, unit):
    degrees = Fraction(degrees)
    if unit == 'degrees':
        number = str(degrees.numerator) if degrees.denominator == 1 else str(float(degrees))
        return number + r'^\circ'
    f = degrees / 180
    n, d = f.numerator, f.denominator
    top = ('' if n == 1 else str(n)) + r'\pi'
    return top if d == 1 else r'\frac{' + top + '}{' + str(d) + '}'


def expression(a, form):
    c = r'\cos^2\left(' + a + r'\right)'
    s = r'\sin^2\left(' + a + r'\right)'
    if form == 'difference': return c + '-' + s
    if form == 'sine': return '1-2' + s
    if form == 'cosine': return '2' + c + '-1'
    if form == 'square':
        return (r'\cos^4\left(' + a + r'\right)-2' + c + s +
                r'+\sin^4\left(' + a + r'\right)')
    raise ValueError(form)


def result(doubled, form):
    value = COS[doubled]
    if form != 'square': return value
    if value == '0': return '0'
    if r'sqrt{3}' in value: return r'\frac{3}{4}'
    if r'sqrt{2}' in value: return r'\frac{1}{2}'
    return r'\frac{1}{4}'


def aligned(rows):
    return '$$\n' + r'\begin{aligned}' + '\n' + ' \\\\\n'.join(rows) + '\n' + r'\end{aligned}' + '\n$$'


def make(band, doubled, form, unit, shape, filler=1, rng=None, replay=None, correct_position=None):
    if band == 'hard' and (form != 'square' or shape != 'blank'): raise ValueError('Hard contract')
    if form == 'square' and doubled not in SQUARE: raise ValueError('Square angle outside catalog')
    if form != 'square' and doubled not in DIRECT: raise ValueError('Original-angle evaluations must require the identity')
    rng = rng or random.Random(0)
    a, b = angle(Fraction(doubled,2), unit), angle(doubled, unit)
    expr, answer, inner = expression(a, form), result(doubled, form), COS[doubled]
    basic = expression('x', 'difference' if form == 'square' else form)
    solution = ''
    if form == 'square':
        solution += 'Let $E$ denote the expression in the question. Recognize the expanded perfect square:\n\n' + aligned([
            r'E &= \left(' + expression(a,'difference') + r'\right)^2']) + '\n\n'
    solution += 'Use the cosine double-angle identity:\n\n$$\n' + basic + r'=\cos(2x)' + '\n$$\n\n'
    target = expression(a, 'difference' if form == 'square' else form)
    rows = [r'&' + target, r'&= \cos\left(2\cdot ' + a + r'\right)',
            r'&= \cos\left(' + b + r'\right)']
    # Explicit quadrant/reference-angle transition; no hidden CAS rewrite.
    ref = doubled if doubled <= 90 else (180-doubled if doubled < 180 else (doubled-180 if doubled<=270 else 360-doubled))
    if doubled not in (30,45,60,90,270):
        sign = '-' if 90 < doubled < 270 else ''
        rows.append(r'&= ' + sign + r'\cos\left(' + angle(ref,unit) + r'\right)')
    rows.append(r'&= ' + inner)
    solution += 'Substitute the angle and evaluate the standard-angle cosine:\n\n' + aligned(rows)
    if form == 'square':
        solution += '\n\nFinally, square the value:\n\n' + aligned([
            r'E &= \left(' + inner + r'\right)^2',
            r'&= ' + answer])
    if form == 'square':
        first,rest = expr.split('-2',1)
        middle,last = rest.split('+',1)
        display = aligned([r'&'+first, r'&\quad -2'+middle, r'&\quad +'+last+'='])
    else:
        display = '$$\n' + expr + ('=' if shape=='blank' else '') + '\n$$'
    prompt = 'Without using a calculator, find the **exact** value.\n\n' + display
    if shape == 'blank': prompt += '\n{{field-1}}'
    if replay is not None:
        # Complete historical banks, preserving their designation. Prompt and
        # derivation are recomputed at the original parameter, not copied keys.
        values = replay['choices']
        assert normalize_tex(replay['correct']) == answer
    elif shape == 'radio':
        values = [r'\frac{\sqrt{2}}{2}',r'-\frac{\sqrt{2}}{2}',
                  r'\frac{\sqrt{3}}{2}',r'-\frac{\sqrt{3}}{2}',
                  ('' if filler>0 else '-') + r'\frac{1}{2}']
        rng.shuffle(values)
        if correct_position is not None:
            # Batch-level position planning is independent of the mathematics.
            # Keep the shuffled error alternatives while placing the answer.
            values.remove(answer)
            values.insert(correct_position, answer)
    else: values = [answer]
    values = [normalize_tex(v) for v in values]
    prompt, solution = normalize_prose(prompt), normalize_prose(solution)
    # Normalize all content before assigning identities.
    semantic = json.dumps([band,prompt,solution,shape,values],ensure_ascii=False,separators=(',',':'))
    qid = uid(semantic)
    fid = uid(qid + ':field')
    choices = [{':answer/id':uid(fid+':'+v), ':answer/type':':answer.type/math', ':answer/value':v} for v in values]
    q = {':question/id':qid, ':question/difficulty':':question.difficulty/'+band,
         ':question/problem':prompt, ':question/worked-solution':solution,
         ':question/answer-fields':[{':answer-field/id':fid, ':answer-field/key':'field-1' if shape=='blank' else 'selection',
            ':answer-field/type':':answer-field.type/'+shape, ':answer-field/choices':choices,
            ':answer-field/correct':[':answer/id', uid(fid+':'+answer)]}]}
    rec = {'knowledge_point':{'db_id':KP,'title':TITLE},'question':q,
           'generation':{'version':2,'template':form,'parameters':{'doubled_degrees':doubled,'unit':unit,'shape':shape},
                         'source_ids':[replay['source_id']] if replay else (['q-120370'] if band=='moderate' and form=='difference' else ANCHORS[form]),
                         'source_support':('archival target-KP imported case' if replay else 'authored complementary-identity transfer; related prerequisite canonical e-3667, not target-KP import' if form=='cosine' else 'target-KP imported family'),
                         'bank_profile':'source-replay' if replay else ('paired-standard-values' if shape=='radio' else 'exact-entry'),
                         'domain':'real fixed angle; exact evaluation', 'final_expression':answer}}
    return validate_generated_record(rec)


def source_replay():
    data = json.loads(Path(__file__).with_name('replay-data.json').read_text())
    return [make(r['band'],r['doubled'],r['form'],r['unit'],r['shape'],replay=r) for r in data if r['form']!='square' or r['doubled'] in SQUARE]


def generate(band, count, seed):
    if band == 'unclassified': band = 'easy'
    if band not in ('easy','moderate','hard') or count < 0: raise ValueError('Invalid band/count')
    rng = random.Random(seed)
    forms = {'easy':['difference'],'moderate':['sine','cosine','difference'],'hard':['square']}[band]
    shapes = ['blank'] if band=='hard' else ['radio','blank']
    # Construct answer-bearing role pools first. Cycle shuffled outcomes so a
    # finite batch is not merely a random run of one answer/sign case.
    groups = {}
    for d,form,unit,shape in itertools.product(SQUARE if band=='hard' else DIRECT, forms, ['degrees','radians'], shapes):
        for filler in ([-1,1] if shape=='radio' else [1]):
            groups.setdefault(result(d,form),[]).append((d,form,unit,shape,filler))
    for pool in groups.values(): rng.shuffle(pool)
    capacity = sum(map(len,groups.values()))
    if count > capacity: raise ValueError(f'Request {count} exceeds finite semantic catalog {capacity}')
    output=[]
    used_math=set()
    positions = {form: [] for form in forms}
    while len(output)<count:
        roles=[k for k,pool in groups.items() if any((p[0],p[1]) not in used_math for p in pool)]
        if not roles:
            # All available mathematical instances have been served once.
            # Only then begin another presentation cycle, still without exact
            # record repetition and without a seed-specific exception.
            used_math.clear()
            continue
        rng.shuffle(roles)
        for role in roles:
            if len(output)==count: break
            pool=groups[role]
            index=next(i for i in range(len(pool)-1,-1,-1) if (pool[i][0],pool[i][1]) not in used_math)
            d,form,unit,shape,filler=pool.pop(index)
            used_math.add((d,form))
            correct_position = None
            if shape == 'radio':
                if not positions[form]:
                    positions[form] = list(range(5))
                    rng.shuffle(positions[form])
                correct_position = positions[form].pop()
            record=make(band,d,form,unit,shape,filler,rng,correct_position=correct_position)
            record['generation'].update(seed=seed,index=len(output),difficulty=band)
            output.append(record)
    return output


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', choices=['unclassified','easy','moderate','hard'],default='easy')
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    a=parser.parse_args()
    print(json.dumps(generate(a.difficulty,a.count,a.seed),ensure_ascii=False))

if __name__=='__main__': main()
