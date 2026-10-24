#!/usr/bin/env python3
"""Linear trig substitution: controlled easy, moderate and authored hard cases."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import sys
import uuid

import sympy as sp

# The same entrypoint also works at the retained legacy repository path.
LOCAL = Path(__file__).with_suffix('')
if not (LOCAL / 'trig_format.py').is_file():
    LOCAL = Path(__file__).resolve().parent
sys.path.insert(0, str(LOCAL))
from trig_format import normalize_prose, normalize_tex

KP = {'db_id': 17592186068915, 'id': '746d1bc6-98ec-59a1-bec6-9dcfb7081a5d',
      'title': 'Integrating Trigonometric Functions With Linear Arguments'}
VERSION = '2.0.0-structural-bands'
R = sp.Rational
PI = sp.pi
X, U = sp.symbols('x u', real=True)
EASY_SLOPES = tuple(map(sp.Integer, range(2, 9))) + (R(1, 2), R(1, 3), R(1, 4))
RATIONAL_SLOPES = (R(2, 3), R(3, 2), R(3, 4), R(4, 3), R(5, 2), R(2, 5))
AMPLITUDES = (R(2, 3), R(3, 2), R(4, 3), R(5, 3), R(5, 2), R(7, 3), R(3, 4), R(5, 4))
SHIFTS = (PI/6, -PI/6, PI/3, -PI/3, PI/2, 2*PI/3, PI)
CASES = {
    'easy': ('indef_sin', 'indef_cos', 'def_sin', 'def_cos'),
    'moderate': ('shift_sin', 'shift_cos', 'pi_sin', 'pi_cos', 'fraction_sin', 'fraction_cos'),
    'hard': ('compound_sin_positive', 'compound_sin_negative', 'compound_cos_positive', 'compound_cos_negative'),
}


def tex(value):
    # Preserve the chosen affine input; a CAS factorization is not a display
    # policy for the learner's substitution or its derivative.
    return normalize_tex(sp.latex(value))


def trig(fn, argument):
    return getattr(sp, fn)(argument, evaluate=False)


def term(coefficient, fn, argument):
    """Keep the chosen operator and input visible, including negative slopes."""
    coefficient = sp.sympify(coefficient)
    prefix = '' if coefficient == 1 else '-' if coefficient == -1 else tex(coefficient)
    return prefix + '\\' + fn + r'\left(' + tex(argument) + r'\right)'


def data(fn, a, b, c, lo=None, hi=None):
    arg = b*X+c
    primitive_fn, sign = ('cos', -1) if fn == 'sin' else ('sin', 1)
    coefficient = sp.cancel(sign*a/b)
    primitive = coefficient*trig(primitive_fn, arg)
    if lo is None:
        answer = primitive
        u0 = u1 = None
    else:
        u0, u1 = sp.simplify(b*lo+c), sp.simplify(b*hi+c)
        answer = sp.simplify(coefficient*(getattr(sp, primitive_fn)(u1)-getattr(sp, primitive_fn)(u0)))
    return arg, primitive_fn, coefficient, primitive, answer, u0, u1


def support(case):
    if case.startswith('indef'):
        return ['q-10061', 'q-10064', 'q-2191', 'e-464']
    if case.startswith('def'):
        return ['q-350039', 'q-350040', 'q-13644']
    if case.startswith('shift'):
        return ['q-10574', 'q-10575']
    if case.startswith('pi'):
        return ['q-346081', 'q-350036']
    if case.startswith('fraction'):
        return ['e-464', 'q-10574', 'q-10575']
    return ['e-464', 'q-10064', 'q-10574', 'q-10575', 'q-350036']


def parameters(case, rng, *, slope_sign=None, difference_kind=None):
    fn = 'sin' if 'sin' in case else 'cos'
    a = sp.Integer(rng.randint(1, 9))
    c = sp.Integer(0)
    if case.startswith('indef'):
        b = rng.choice(EASY_SLOPES)*(slope_sign or rng.choice((-1, 1)))
        c = sp.Integer(rng.randint(-6, 6))
        return fn, a, b, c, None, None
    if case.startswith('def'):
        b = sp.Integer(rng.randint(2, 9))
        u0, u1 = rng.choice(((0,PI/2),(PI/2,PI),(PI,3*PI/2),(3*PI/2,2*PI),
                             (0,PI),(PI/2,3*PI/2),(PI,2*PI)))
    elif case.startswith('shift'):
        b = sp.Integer(rng.randint(2, 7))
        c = rng.choice(SHIFTS)
        pairs = ((PI/3, 2*PI/3), (0, PI/3), (PI/3, PI/2), (PI/6, 5*PI/6)) if fn == 'sin' else (
            (-PI/6, PI/6), (PI/6, PI/2), (0, PI/3), (PI/3, 2*PI/3))
        u0, u1 = rng.choice(pairs)
    elif case.startswith('pi'):
        b = PI*rng.choice((R(1, 2), R(1, 3), R(2, 3), R(3, 4), R(1, 4), R(2, 5)))
        pairs = ((0, PI/2), (0, PI/3), (0, PI), (PI/2, PI)) if fn == 'sin' else (
            (0, PI/6), (0, PI/3), (0, PI/2), (PI/2, PI))
        u0, u1 = rng.choice(pairs)
    elif case.startswith('fraction'):
        b = rng.choice(RATIONAL_SLOPES)*rng.choice((-1, 1))
        while sp.cancel(a/b).q == 1:
            a = sp.Integer(rng.randint(1, 9))
        pairs = ((PI/3, 2*PI/3), (0, PI/3), (PI/3, PI/2)) if fn == 'sin' else (
            (-PI/6, PI/6), (PI/6, PI/2), (PI/6, 5*PI/6))
        u0, u1 = rng.choice(pairs)
        if b < 0:
            u0, u1 = u1, u0
    else:
        b = rng.choice(RATIONAL_SLOPES)*(-1 if case.endswith('negative') else 1)
        a = rng.choice([value for value in AMPLITUDES if sp.cancel(value/b).q != 1])
        c = rng.choice(SHIFTS)
        # The primitive has unlike, nonzero radical endpoint values. Choose
        # their sign relation as a reasoning case before choosing endpoints.
        first = (PI/4, 3*PI/4, 5*PI/4, 7*PI/4)
        second = (PI/6, 5*PI/6, 7*PI/6, 11*PI/6) if fn == 'sin' else (PI/3, 2*PI/3, 4*PI/3, 5*PI/3)
        primitive_fn = sp.cos if fn == 'sin' else sp.sin
        kind = difference_kind or rng.choice(('same', 'opposite'))
        pairs = [(left, right) for left in first for right in second
                 if (sp.sign(primitive_fn(left)*primitive_fn(right)) == 1) == (kind == 'same')]
        u0, u1 = sorted(rng.choice(pairs), key=float, reverse=bool(b < 0))
    lo, hi = sp.simplify((u0-c)/b), sp.simplify((u1-c)/b)
    return fn, a, b, c, lo, hi


def wrong_answers(fn, a, b, c, lo, hi):
    arg, pf, coefficient, primitive, answer, u0, u1 = data(fn, a, b, c, lo, hi)
    if lo is None:
        # Whole authored bank: sign error, multiply instead of divide by b,
        # both errors together, and integrate to the wrong trig function.
        return [(-coefficient*trig(pf, arg), term(-coefficient, pf, arg), 'reverse antiderivative sign'),
                (coefficient*b*b*trig(pf, arg), term(coefficient*b*b, pf, arg), 'multiply by inner slope'),
                (-coefficient*b*b*trig(pf, arg), term(-coefficient*b*b, pf, arg), 'multiply by inner slope and reverse sign'),
                (coefficient*trig(fn, arg), term(coefficient, fn, arg), 'retain original trig function')]
    p = getattr(sp, pf)
    delta = p(u1)-p(u0)
    if answer == 0:
        # Generalize the complete q-13644 zero-outcome bank. These errors
        # replace the endpoint difference or omit its amplitude, so they do not
        # all collapse to zero when the correct endpoints cancel.
        scale = sp.cancel(a/b)
        return [(value,tex(value),recipe) for value,recipe in (
            (scale,'replace endpoint difference by one'),(1/b,'omit amplitude and replace endpoint difference by one'),
            (sp.Integer(1),'report one'),(sp.Integer(-1),'report negative one'),
            (-scale,'reverse sign and replace endpoint difference by one'),
            (-1/b,'omit amplitude and reverse endpoint sign'))]
    return [(sp.simplify(-answer), tex(-answer), 'reverse endpoint subtraction'),
            (sp.simplify(answer*b), tex(answer*b), 'omit reciprocal inner derivative'),
            (sp.simplify(answer*b*b), tex(answer*b*b), 'multiply by inner derivative'),
            (sp.simplify(coefficient*p(u1)), tex(coefficient*p(u1)), 'omit lower endpoint'),
            (sp.simplify(coefficient*p(u0)), tex(coefficient*p(u0)), 'use lower endpoint only'),
            (sp.simplify(coefficient*(p(u1)+p(u0))), tex(coefficient*(p(u1)+p(u0))), 'add endpoint values'),
            (sp.simplify(delta), tex(delta), 'omit coefficient and derivative factor')]


def worked(fn, a, b, c, lo, hi):
    arg, pf, coefficient, primitive, answer, u0, u1 = data(fn, a, b, c, lo, hi)
    scale = sp.cancel(a/b)
    integral = r'\int ' + term(a, fn, arg) + r'\,\mathrm{d}x'
    if lo is not None:
        integral = r'\int_{'+tex(lo)+'}^{'+tex(hi)+'} '+term(a, fn, arg)+r'\,\mathrm{d}x'
    solution = ('Let $u='+tex(arg)+r'.$ Then'+'\n\n$$\n'+r'\frac{\mathrm{d}u}{\mathrm{d}x}='+tex(b)
                +r',\qquad \mathrm{d}x=\left('+tex(1/b)+r'\right)\mathrm{d}u.'+'\n$$\n\n')
    if lo is not None:
        solution += ('Transform both bounds using the same substitution:\n\n$$\n'+r'\begin{aligned}'
            + 'x='+tex(lo)+r'&\quad\Longrightarrow\quad u='+tex(b)+r'\left('+tex(lo)+r'\right)+\left('+tex(c)+r'\right)='+tex(u0)
            +r'\\ x='+tex(hi)+r'&\quad\Longrightarrow\quad u='+tex(b)+r'\left('+tex(hi)+r'\right)+\left('+tex(c)+r'\right)='+tex(u1)
            +r'.\end{aligned}'+'\n$$\n\n')
        if b < 0:
            solution += 'The transformed bounds decrease because the inner derivative is negative. Keep their order together with the negative substitution factor.\n\n'
    limits = '' if lo is None else '_{'+tex(u0)+'}^{'+tex(u1)+'}'
    rows = ['&'+integral,'&='+tex(a)+r'\left('+tex(1/b)+r'\right)\int'+limits+' '+term(1, fn, U)+r'\,\mathrm{d}u',
            '&='+tex(scale)+r'\int'+limits+' '+term(1, fn, U)+r'\,\mathrm{d}u']
    intrinsic = '-'+term(1, pf, U) if fn == 'sin' else term(1, pf, U)
    if lo is None:
        rows.extend(['&='+tex(scale)+r'\left('+intrinsic+r'\right)+C', '&='+term(coefficient, pf, arg)+'+C'])
    else:
        rows.extend(['&='+tex(scale)+r'\left['+intrinsic+r'\right]'+limits,
            '&='+tex(coefficient)+r'\left('+term(1,pf,u1)+'-'+term(1,pf,u0)+r'\right)',
            '&='+tex(coefficient)+r'\left(\left('+tex(getattr(sp,pf)(u1))+r'\right)-\left('+tex(getattr(sp,pf)(u0))+r'\right)\right)',
            '&='+tex(answer)])
    solution += 'Substitute and integrate:\n\n$$\n'+r'\begin{aligned}'+r'\\ '.join(rows)+r'.\end{aligned}'+'\n$$'
    return integral, solution


def build(level, case, values, *, response='blank', seed=0):
    if case not in CASES.get(level, ()) or response not in ('blank', 'radio'):
        raise ValueError('Unsupported band, case or response')
    if level == 'hard' and response != 'blank':
        raise ValueError('The authored hard band uses independent exact entry')
    fn, a, b, c, lo, hi = values
    a,b,c = map(sp.sympify,(a,b,c))
    lo = None if lo is None else sp.sympify(lo)
    hi = None if hi is None else sp.sympify(hi)
    if fn not in ('sin','cos') or a == 0 or b == 0 or (lo is not None and not lo < hi):
        raise ValueError('Invalid linear-substitution instance')
    if fn != ('sin' if 'sin' in case else 'cos'):
        raise ValueError('Function/case mismatch')
    if case.startswith('indef'):
        valid = a.is_Integer and 1 <= a <= 9 and abs(b) in EASY_SLOPES and c.is_Integer and -6 <= c <= 6 and lo is None and hi is None
    elif case.startswith('def'):
        valid = a.is_Integer and 1 <= a <= 9 and b.is_Integer and 2 <= b <= 9 and c == 0 and lo is not None
    elif case.startswith('shift'):
        valid = a.is_Integer and 1 <= a <= 9 and b.is_Integer and 2 <= b <= 7 and c in SHIFTS and lo is not None
    elif case.startswith('pi'):
        valid = a.is_Integer and 1 <= a <= 9 and (b/PI).is_Rational and b > 0 and c == 0 and lo is not None
    elif case.startswith('fraction'):
        valid = a.is_Integer and 1 <= a <= 9 and abs(b) in RATIONAL_SLOPES and sp.cancel(a/b).q != 1 and c == 0 and lo is not None
    else:
        valid = a in AMPLITUDES and abs(b) in RATIONAL_SLOPES and sp.cancel(a/b).q != 1 and c in SHIFTS and lo is not None
        valid = valid and (b < 0) == case.endswith('negative')
    if not valid:
        raise ValueError('Instance does not satisfy the declared band contract')
    arg, pf, coefficient, primitive, answer, u0, u1 = data(fn,a,b,c,lo,hi)
    if case.startswith('def') and (u0 < 0 or u1 > 2*PI or sp.simplify((u1-u0)/PI) not in (R(1,2),1)
                                   or not all((2*value/PI).is_Integer for value in (u0,u1))):
        raise ValueError('Easy definite endpoints must retain elementary quarter-turn values')
    if level == 'hard':
        endpoint_magnitudes = {sp.simplify(abs(getattr(sp,pf)(value))) for value in (u0,u1)}
        if endpoint_magnitudes != {sp.sqrt(2)/2,sp.sqrt(3)/2}:
            raise ValueError('Hard endpoint work must contain unlike nonzero radicals')
    integral, solution = worked(fn,a,b,c,lo,hi)
    correct = term(coefficient,pf,arg) if lo is None else tex(answer)
    choices = [(answer, correct, 'correct')]
    if response == 'radio':
        for candidate, text, recipe in wrong_answers(fn,a,b,c,lo,hi):
            if all(sp.simplify(candidate-existing[0]) != 0 for existing in choices):
                choices.append((candidate,text,recipe))
            if len(choices) == 5:
                break
        if len(choices) != 5:
            raise ValueError('This instance has no complete distinct five-choice bank')
    correct += '+C' if lo is None and response == 'radio' else ''
    rendered = [(text+('+C' if lo is None and response=='radio' else ''),recipe) for _,text,recipe in choices]
    prompt = 'Evaluate the integral. Give an exact answer.\n\n$$\n'+integral+(' =' if response=='blank' else '')+'\n$$'
    key = 'answer' if response == 'blank' else 'selection'
    if response == 'blank':
        prompt += '\n\n{{answer}}'+(' $+C$' if lo is None else '')
    prompt, solution = normalize_prose(prompt), normalize_prose(solution)
    # Mathematical identity ignores response format, bank and sampling seed.
    f = a*trig(fn,arg)
    fingerprint = hashlib.sha256(json.dumps([sp.srepr(sp.expand(sp.expand_trig(f))),None if lo is None else sp.srepr(lo),None if hi is None else sp.srepr(hi)]).encode()).hexdigest()
    uid = lambda namespace,text: str(uuid.uuid5(uuid.UUID(namespace),text))
    qid = uid(KP['id'],json.dumps([VERSION,fingerprint,response,sorted(v for v,_ in rendered)]))
    fid = uid(qid,key)
    answers = [{':answer/id':uid(fid,text),':answer/type':':answer.type/math',':answer/value':text} for text,_ in rendered]
    correct_id = next(row[':answer/id'] for row in answers if row[':answer/value']==correct)
    random.Random(seed).shuffle(answers)
    params = dict(zip(('function','amplitude','slope','shift','lower','upper'),(fn,str(a),str(b),str(c),None if lo is None else str(lo),None if hi is None else str(hi))))
    sources = support(case)
    if response=='radio' and answer==0 and 'q-13644' not in sources:
        sources.append('q-13644')
    metadata = {'version':VERSION,'template':case,'source_ids':sources,'parameters':params,'seed':seed,
        'mathematical_fingerprint':fingerprint,'response':response,'bank_origin':'authored rule-error recipes' if response=='radio' else 'exact entry',
        'bank_recipes':dict(rendered),'u_bounds':None if lo is None else [str(u0),str(u1)],
        'difficulty_origin':'authored compound of established skills; no imported hard examples' if level=='hard' else 'source-supported workload; labels are not copied from individual templates',
        'domain':'x real; constant nonzero inner derivative; exact special-angle endpoints'}
    return {'knowledge_point':KP,'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,
        ':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{
            ':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+response,
            ':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]},'generation':metadata}


def batch(level, count=5, seed=0, exclude_fingerprints=()):
    if level not in CASES or type(count) is not int or not 0 <= count <= 200:
        raise ValueError('Use an available band and count 0..200; shortages are explicit')
    rng = random.Random(seed)
    schedule = list(CASES[level]);rng.shuffle(schedule)
    starts = {case:('blank' if index%2 == 0 else 'radio') for index,case in enumerate(schedule)}
    served = {case:0 for case in schedule}
    evidence = json.loads((LOCAL/'source-evidence.json').read_text())
    records, seen = [], set(evidence.get('excluded_practice_fingerprints', ())) | set(exclude_fingerprints)
    first_sign = rng.choice((-1,1))
    indefinite_starts = {'indef_sin':first_sign,'indef_cos':-first_sign}
    pair_starts = {case:rng.choice(('same','opposite')) for case in schedule}
    for index in range(count):
        case = schedule[index % len(schedule)]
        response = 'blank' if level=='hard' else starts[case]
        if level != 'hard' and served[case] % 2:
            response = 'radio' if response=='blank' else 'blank'
        # Period four for slope signs and period two for response forms cover
        # their cross-product instead of locking a sign to a field type.
        slope_sign = indefinite_starts.get(case,1)*(1 if served[case]%4 in (0,3) else -1)
        pair_kind = pair_starts[case]
        if served[case]%2:
            pair_kind = 'opposite' if pair_kind=='same' else 'same'
        for attempt in range(100):
            values = parameters(case,rng,slope_sign=slope_sign,
                                difference_kind=pair_kind)
            try:
                record = build(level,case,values,response=response,seed=rng.getrandbits(64))
            except ValueError:
                continue
            fingerprint = record['generation']['mathematical_fingerprint']
            if fingerprint in seen:
                continue
            records.append(record);seen.add(fingerprint)
            served[case] += 1
            break
        else:
            raise ValueError('Finite compatible family exhausted; no duplicate padding')
    rng.shuffle(records)
    return records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',required=True,choices=tuple(CASES))
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=('json',),default='json')
    args=parser.parse_args()
    print(json.dumps(batch(args.difficulty,args.count,args.seed),indent=2,ensure_ascii=False))


if __name__=='__main__':
    main()
