#!/usr/bin/env python3
"""Seeded amplitude practice. No database, runtime repository paths, or assets.

Coefficient/argument TeX helpers and the quotient/factored derivation are adapted
from generate/scratch/17592186129121.py. See instructional-account.md for scope.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import random
import sys
import uuid
import sympy as sp
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP_ID = 17592186129121
KP_UUID = '7f8fa2b3-ccaa-5390-89fa-03e338cf8690'
TITLE = 'Determining the Amplitude of a Transformed Sinusoidal Function'
VERSION = '2.0.0'
LEVELS = ('easy', 'moderate', 'hard')
SOURCE_IDS = {
    'direct_easy': ['1489edd6-f3f4-5ab1-9410-746b5fd6547f', '3e84da28-f1c2-5f42-8b28-8c5abbfd888a', '149ae65f-0d63-59f5-9ea2-35fcac7e5bad'],
    'direct_moderate': ['7867732e-c747-51f4-a678-9910706e6d84', '5a43e6b6-5512-53d1-b032-03f28416a804'],
    'quotient': ['86dec134-c288-5f12-9971-6b0570d7076d'],
    'factored': ['86dec134-c288-5f12-9971-6b0570d7076d', 'e2e5002a-d3ae-5831-b405-41618960aee4'],
}

# Profiles are selected whole, before sampling their compatible numerical instance.
# a=amplitude, b=horizontal magnitude, c=phase magnitude, n=numerator magnitude,
# d=numerator constant magnitude, q=denominator, p=outer scale magnitude.
PROFILES = {
    'direct': {
        'horizontal': ['a', 'b', '1/b', 'c', '1/c'],
        'stretch': ['a', '1/a', 'a*b', 'a/b', 'b'],
        'height': ['a', '2*a', 'a/2', 'b', 'c'],
    },
    'quotient': {
        'division': ['a', 'n', 'd/q', 'q/n', '1/q'],
        'parameters': ['a', 'd/q', 'd', '1/q', 'q/d'],
        'height': ['a', '2*a', 'a/2', 'd/q', 'n'],
    },
    'factored': {
        'scales': ['a', 'n/q', 'p*n', 'p*d/q', 'q/(p*n)'],
        'division': ['a', 'n/q', 'p/q', 'd/q', '1/q'],
        'height': ['a', '2*a', 'a/2', 'n/q', 'p*d/q'],
    },
}

class SampleRejected(ValueError):
    pass

def number(v):
    if isinstance(v, (bool, float)):
        raise ValueError('Exact numbers required')
    return sp.sympify(v, locals={'pi': sp.pi})

def tex(z):
    z = number(z)
    if z.is_Rational:
        n, d = int(z.p), int(z.q)
        return str(n) if d == 1 else ('-' if n < 0 else '') + r'\frac{' + str(abs(n)) + '}{' + str(d) + '}'
    return normalize_tex(sp.latex(z))

def coeff(z):
    return '' if z == 1 else '-' if z == -1 else tex(z)

def signed(z):
    return ('+' if z >= 0 else '-') + tex(abs(z))

def argument(p):
    return coeff(p['B']) + 'x' + (signed(p['C']) if p['C'] else '')

def term(p):
    return '\\' + p['trig'] + r'\left(' + argument(p) + r'\right)'

def expression(kind, p):
    t = term(p)
    if kind == 'direct':
        return coeff(p['A']) + t + (signed(p['D']) if p['D'] else '')
    # Constant-first and trig-first are both legitimate coefficient locations.
    numerator = tex(p['D']) + signed(p['N']) + t
    if p.get('order') == 'trig-first':
        numerator = coeff(p['N']) + t + signed(p['D'])
    fraction = r'\frac{' + numerator + '}{' + tex(p['Q']) + '}'
    if kind == 'quotient':
        return fraction
    return tex(p['P']) + r'\left(' + fraction + r'\right)' + (signed(p['E']) if p['E'] else '')

def coefficient(kind, p):
    return p['A'] if kind == 'direct' else sp.simplify(p.get('P', 1) * p['N'] / p['Q'])

def solution(kind, p, expr):
    a = coefficient(kind, p)
    t = term(p)
    text = ''
    if kind != 'direct':
        shift = sp.simplify(p.get('P', 1) * p['D'] / p['Q'] + p.get('E', 0))
        rows = ['f(x)&=' + expr]
        if kind == 'factored':
            rows.append(r'&=\frac{' + tex(p['P']) + r'\cdot(' + tex(p['N']) + ')}{' + tex(p['Q']) + r'}\cdot ' + t + r'+\frac{' + tex(p['P']) + r'\cdot(' + tex(p['D']) + ')}{' + tex(p['Q']) + '}' + (signed(p['E']) if p['E'] else ''))
        rows.append('&=' + coeff(a) + t + (signed(shift) if shift else ''))
        text = 'First, rewrite the function to identify the whole coefficient:\n\n$$\n' + r'\begin{aligned}' + r' \\ '.join(rows) + r'\end{aligned}' + '\n$$\n\n'
    text += 'For a function in the form $f(x)=A\\' + p['trig'] + '(Bx+C)+D$, the amplitude is $|A|$.\n\n'
    text += 'Here, $A=' + tex(a) + '$, so the amplitude is $\\left|' + tex(a) + r'\right|=' + tex(abs(a)) + '$. '
    text += 'Horizontal transformations and additive constants do not change the amplitude.'
    return text

def recipes(kind, p, profile):
    env = dict(a=abs(coefficient(kind, p)), b=abs(p['B']), c=abs(p['C']))
    if kind != 'direct':
        env.update(n=abs(p['N']), d=abs(p['D']), q=p['Q'], p=abs(p.get('P', 1)))
    selected = PROFILES[kind][profile]
    if kind == 'direct' and env['a'].has(sp.pi) and profile == 'horizontal':
        # Retain several pi-valued alternatives, as in source q-81512.
        selected = ['a', 'a/pi', 'a/2', '2*a', 'b']
    values = [sp.simplify(sp.sympify(r, locals=env)) for r in selected]
    if len(set(values)) != 5 or any(not v.is_real or v <= 0 for v in values):
        raise SampleRejected('Complete profile has duplicate or invalid choices')
    return values

def make(level, kind, params, profile, seed=0, bank=None, sources=None):
    p = {k: v if k in ('trig', 'order') else number(v) for k, v in params.items()}
    if p['trig'] not in ('sin', 'cos') or p['B'] == 0 or coefficient(kind, p) == 0:
        raise ValueError('Nonconstant sine/cosine required')
    if kind != 'direct' and p['Q'] <= 0:
        raise ValueError('Positive shared denominator required')
    expr = expression(kind, p)
    prompt = normalize_prose('What is the amplitude of the function $f(x)=' + expr + '$?')
    worked = normalize_prose(solution(kind, p, expr))
    values = recipes(kind, p, profile) if bank is None else list(map(number, bank))
    correct = abs(coefficient(kind, p))
    if len(values) != 5 or len(set(values)) != 5 or values.count(correct) != 1:
        raise SampleRejected('Ambiguous or missing correct answer')
    displays = list(map(tex, values))
    payload = [VERSION, level, prompt, worked, sorted(displays)]
    fingerprint = hashlib.sha256(json.dumps(payload, ensure_ascii=False).encode()).hexdigest()
    qid = uuid.uuid5(uuid.UUID(KP_UUID), fingerprint)
    fid = uuid.uuid5(qid, 'selection')
    choices = [{':answer/id': str(uuid.uuid5(fid, 'math:' + value)), ':answer/type': ':answer.type/math', ':answer/value': value} for value in displays]
    correct_id = choices[values.index(correct)][':answer/id']
    random.Random(seed).shuffle(choices)
    q = {':question/id': str(qid), ':question/difficulty': ':question.difficulty/' + level,
         ':question/problem': prompt, ':question/worked-solution': worked,
         ':question/answer-fields': [{':answer-field/id': str(fid), ':answer-field/key': 'selection',
          ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': choices,
          ':answer-field/correct': [':answer/id', correct_id]}]}
    task = [kind, str(p['A'])] if kind == 'direct' else [kind, str(p['N']), str(p['Q']), str(p.get('P', 1))]
    record = {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': TITLE}, 'question': q,
        'generation': {'version': VERSION, 'seed': seed, 'template': kind, 'bank_profile': profile,
            'parameters': {k: str(v) for k, v in p.items()}, 'mathematical_task': task,
            'parameter_fingerprint': hashlib.sha256(json.dumps(task).encode()).hexdigest(),
            'content_fingerprint': fingerprint,
            'source_ids': sources if sources is not None else SOURCE_IDS[kind + '_' + level if kind == 'direct' else kind],
            'authored_extension': bank is None, 'eligible_for_learning': True,
            'recipes': (['a', 'a/pi', 'a/2', '2*a', 'b'] if kind == 'direct' and abs(coefficient(kind,p)).has(sp.pi) and profile == 'horizontal' else PROFILES[kind].get(profile)), 'plot_rating': 'none', 'plot_assets': {},
            'domain': 'x real; nonzero slope and sinusoidal coefficient',
            'python_version': sys.version.split()[0], 'sympy_version': sp.__version__}}
    return validate_generated_record(record)

def sample(level, kind, rng, index=0):
    p = dict(trig=rng.choice(['sin', 'cos']), B=rng.choice([sp.Rational(1,2), sp.Rational(1,3), 1, 2, 3, 4]), C=rng.choice([-3,-2,-1,1,2,3]), D=0)
    if kind == 'direct':
        # Unit is an intended source decision, shared with nonunit coefficients
        # at the same argument forms, not a separate always-one shape mask.
        a = 1 if index == -1 else rng.choice(sorted({sp.Rational(n,d) for n in range(1,13) for d in range(1,7)}))
        if level == 'moderate':
            a *= -sp.pi if index == -2 else -rng.choice([1, 1, 1, sp.pi])
            p['D'] = rng.choice([-2,-1,0,1,2])
        p['A'] = a
    else:
        p.update(N=rng.choice([-6,-5,-4,-3,-2,-1,1,2,3,4,5,6]), Q=rng.choice([2,3,4,5,6]), D=rng.choice([-2,-1,1,2,3]), order=rng.choice(['constant-first', 'trig-first']))
        if kind == 'quotient':
            p.update(B=1, C=0)
        else:
            p.update(P=rng.choice([-3,-2,2,3]), E=rng.choice([-1,0,1]), B=rng.choice([1,2,3]), C=rng.choice([-1,1,sp.pi/3,-sp.pi/3]))
    return p

def rank_position(record):
    f = record['question'][':question/answer-fields'][0]
    vals = [float(sp.N(parse_tex(a[':answer/value']))) for a in f[':answer-field/choices']]
    pos = next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id'] == f[':answer-field/correct'][1])
    return sorted(vals).index(vals[pos]), pos

def parse_tex(t):
    # Only the numeric TeX emitted by tex(), for batch-selection summaries.
    import re
    t = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'((\1)/(\2))', t)
    return sp.sympify(t.replace(r'\pi', 'pi').replace(' ', '*'), locals={'pi':sp.pi})

def batch(level, count, seed):
    if level == 'unclassified':
        level = 'moderate'
    if level not in LEVELS or count < 1:
        raise ValueError('A supported level and positive count are required')
    rng = random.Random(seed)
    # Visible operation types are scheduled before values; banks remain complete.
    schedule = ['direct'] if level == 'easy' else ['direct', 'quotient'] if level == 'moderate' else ['factored']
    if rng.randrange(2):
        schedule.reverse()
    unit_slot = rng.randrange(count) if level == 'easy' and count >= 3 else None
    direct_slots = [i for i in range(count) if schedule[i % len(schedule)] == 'direct']
    pi_slot = rng.choice(direct_slots) if level == 'moderate' and len(direct_slots) >= 2 else None
    chosen, seen = [], set()
    for i in range(count):
        kind = schedule[i % len(schedule)]
        found = False
        for attempt in range(3000):
            profile = rng.choice(list(PROFILES[kind]))
            p = sample(level, kind, rng, -1 if i == unit_slot else -2 if i == pi_slot else i)
            try:
                rec = make(level, kind, p, profile, rng.getrandbits(63))
            except SampleRejected:
                continue
            task = rec['generation']['parameter_fingerprint']
            if task in seen:
                continue
            # Reject finite-pool incidental invariants, not mathematical outcomes.
            # For each visible form, the second instance must supply a different
            # key rank/position. This persists in every longer prefix as well.
            def cue_groups(r):
                data = r['generation']
                form = data['template']
                trig = data['parameters']['trig']
                family = form + ('/pi' if form == 'direct' and 'pi' in data['parameters']['A'] else '/rational')
                return {form, form + '/' + trig, family, family + '/' + trig}
            reject_cue = False
            for cue in cue_groups(rec):
                same = [r for r in chosen if cue in cue_groups(r)]
                if len(same) == 1:
                    oldrank, oldpos = rank_position(same[0]); rank,pos = rank_position(rec)
                    if rank == oldrank or pos == oldpos:
                        reject_cue = True
                        break
            if reject_cue:
                continue
            chosen.append(rec); seen.add(task); found = True; break
        if not found:
            raise ValueError('Requested count exceeds bounded distinct valid coefficient tasks')
    return chosen

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty', choices=(*LEVELS,'unclassified','all'), default='moderate')
    ap.add_argument('--count', type=int, default=1)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--format', choices=['json'], default='json')
    a = ap.parse_args()
    levels = LEVELS if a.difficulty == 'all' else [a.difficulty]
    result = [r for level in levels for r in batch(level, a.count, a.seed)]
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
