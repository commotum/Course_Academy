#!/usr/bin/env python3
"""Seeded, database-free easy practice for signed special sets."""
import argparse
import copy
from fractions import Fraction
from functools import lru_cache
import json
from math import isqrt
from pathlib import Path
import random
import re
import uuid
from math_format import checked_math_content, normalize_prose

VERSION = '1.0.0'
KP = {'db_id':17592186054815, 'id':'abc6b3ee-0251-5c9c-9358-bd192c434dd1',
      'title':'Identifying Elements Belonging to Scripted Special Sets'}
TARGETS = ('Q-', 'R0-', 'Z0-', 'Q0+', 'R0+')
SOURCES = ['9392ab96-5be3-5aab-8c35-808d0b88162a','c2a941ac-46f5-56a9-b5ba-03889446453a',
 '016b340f-7aa5-5001-aeb3-927982c5cf50','c84fa181-6eb1-5e84-b542-36ff40a06a4c',
 '0e62d29f-2834-5b4e-b720-bc361e2a5dc0','12109bd9-1ea8-5fd9-b15c-ba4373902b35',
 'ac020dea-1486-5e82-bd01-29594c8fbf7a','4eae16cb-f514-5e15-a012-1e904a842a1d']


def identity(*parts):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, json.dumps(parts, sort_keys=True, ensure_ascii=False)))


def symbol(target):
    return r'\mathbb{' + target[0] + '}' + ('_0' if '0' in target else '') + '^{' + target[-1] + '}'


def definition(target):
    return ('positive' if target[-1] == '+' else 'negative') + ' ' + {
        'Z':'integers','Q':'rational numbers','R':'real numbers'}[target[0]] + (' and zero' if '0' in target else '')


def number(kind, a, b=1):
    """Construct display and exact, simplified classification from one instance."""
    sign = (a > 0) - (a < 0)
    prefix = '-' if a < 0 else ''
    rational = kind in ('integer','fraction','decimal') or (kind in ('sqrt','scaled-root') and isqrt(b)**2 == b)
    if kind == 'integer':
        tex = str(a); value = Fraction(a)
    elif kind == 'fraction':
        tex = prefix + rf'\frac{{{abs(a)}}}{{{b}}}'; value = Fraction(a,b)
    elif kind == 'decimal':
        tex = prefix + f'{abs(a)//10}.{abs(a)%10}'; value = Fraction(a,10)
    elif kind in ('sqrt','scaled-root'):
        tex = prefix + (str(abs(a)) if abs(a) != 1 else '') + rf'\sqrt{{{b}}}'
        value = Fraction(a*isqrt(b)) if rational else None
    elif kind == 'pi':
        tex = prefix + (r'\pi' if b == 1 else rf'\frac{{\pi}}{{{b}}}'); value = None
    else:
        raise ValueError(kind)
    integer = rational and value.denominator == 1
    if rational:
        semantic = 'rational:' + str(value)
        simple = str(value.numerator) if integer else ('-' if value < 0 else '') + rf'\frac{{{abs(value.numerator)}}}{{{value.denominator}}}'
    elif kind == 'pi':
        semantic = f'pi:{Fraction(a,b)}'; simple = tex
    else:
        factor = 1; remainder = b
        for n in range(2,isqrt(b)+1):
            while remainder % (n*n) == 0:
                factor *= n; remainder //= n*n
        coef = a*factor
        simple = ('-' if coef < 0 else '') + (str(abs(coef)) if abs(coef) != 1 else '') + rf'\sqrt{{{remainder}}}'
        semantic = f'root:{remainder}:{coef}'
    return {'kind':kind,'a':a,'b':b,'tex':tex,'sign':sign,'rational':rational,
            'integer':integer,'simple':simple,'semantic':semantic}


def belongs(n, target):
    if n['sign'] == 0:
        return '0' in target
    return (n['sign'] == (1 if target[-1] == '+' else -1)
            and (target[0] == 'R' or n['rational'])
            and (target[0] != 'Z' or n['integer']))


@lru_cache(maxsize=1)
def pool():
    result = [number('integer',a) for a in range(-70,71)]
    for sign in (-1,1):
        result += [number('fraction',sign*a,b) for b in range(2,10) for a in range(1,36)]
        result += [number('decimal',sign*a) for a in range(1,100) if a % 10]
        result += [number('sqrt',sign,b) for b in range(2,50)]
        result += [number('scaled-root',sign*a,b) for a in (2,3) for b in (2,3,5,6,7)]
        result += [number('pi',sign,b) for b in (1,2)]
    return tuple(result)


@lru_cache(maxsize=None)
def eligible(target, desired):
    return tuple(n for n in pool() if belongs(n,target) == desired)


def sample(rng, target=None, mask=None):
    # Select answer-bearing roles first; no count, sign, or position is fixed.
    target = target if target is not None else rng.choice(TARGETS)
    mask = mask if mask is not None else rng.randrange(16)
    if target not in TARGETS or not 0 <= mask < 16:
        raise ValueError('Unsupported target or mask')
    numbers = []; used = set(); rejections = 0
    for i in range(4):
        # Exercise mathematical distinctions before choosing magnitude. A flat
        # value pool would bury zero and square roots under numerous fractions.
        groups = {}
        for n in eligible(target, bool(mask & (1 << i))):
            if n['semantic'] in used: continue
            category = (n['sign'], 'integer' if n['integer'] else 'rational' if n['rational'] else 'irrational')
            groups.setdefault(category, {}).setdefault(n['kind'], []).append(n)
        by_form = groups[rng.choice(list(groups))]
        candidates = by_form[rng.choice(list(by_form))]
        n = rng.choice(candidates)
        numbers.append(dict(n)); used.add(n['semantic'])
    return target,numbers,rejections


def explanation(n, target):
    displayed = '$' + n['tex'] + (('=' + n['simple']) if n['simple'] != n['tex'] else '') + '$'
    if n['sign'] == 0:
        reason = 'Zero is included by the subscript $0$' if '0' in target else 'Zero is not negative or positive, and this set does not include zero'
    else:
        family = 'an integer' if n['integer'] else ('a rational number but not an integer' if n['rational'] else 'an irrational real number')
        reason = ('It is positive' if n['sign'] > 0 else 'It is negative') + ', and it is ' + family
        if n['rational'] and not n['integer'] and n['kind'] == 'decimal':
            value = Fraction(n['a'],10)
            reason += ', since it can be written as $' + ('-' if value < 0 else '') + rf'\frac{{{abs(value.numerator)}}}{{{value.denominator}}}' + '$'
    tail = ('belongs to' if belongs(n,target) else 'does *not* belong to') + ' $' + symbol(target) + '$.'
    return '- ' + displayed + ': ' + reason + '. Therefore, it ' + tail


@checked_math_content
def generate(target, numbers, *, seed=0, index=0, rejection_count=0, replay=None):
    if target not in TARGETS or len(numbers) != 4:
        raise ValueError('Four entries and a supported target are required')
    correct = [belongs(n,target) for n in numbers]
    keys = ['$' + n['tex'] + '$' for n in numbers]
    prompt = 'Which of the numbers below belong to $' + symbol(target) + '$?\n\nSelect all that apply. If none apply, leave all boxes unchecked.'
    selected = [keys[i] for i in range(4) if correct[i]]
    conclusion = ('; '.join(selected) + '.' if selected else 'None of those listed.')
    solution = 'Remember that $' + symbol(target) + '$ is the set of all ' + definition(target) + '.\n\n'
    solution += '\n\n'.join(explanation(n,target) for n in numbers)
    solution += '\n\nIn conclusion, the correct answer is: ' + conclusion
    # Replay preserves observed prose and keys, with documented punctuation repairs.
    if replay is not None:
        prompt = replay[':question/problem'].replace('?$', '$?')
        solution = replay[':question/worked-solution'].replace(r'\,✓$', r'$ $\checkmark$').replace(r'\,\times $', r'$ $\times$')
        keys = [f[':answer-field/key'] for f in replay[':question/answer-fields']]
    prompt = normalize_prose(prompt); solution = normalize_prose(solution)
    keys = [normalize_prose(k) for k in keys]
    content = [prompt,keys,correct]
    qid = identity(KP['id'],content)
    fields = []
    for i,key in enumerate(keys):
        fid = identity(qid,'field',i,key)
        values = ['true','false'] if replay is None else [a[':answer/value'] for a in replay[':question/answer-fields'][i][':answer-field/choices']]
        answers = [{':answer/id':identity(fid,v),':answer/type':':answer.type/text',':answer/value':v} for v in values]
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',
                       ':answer-field/choices':answers,':answer-field/correct':[':answer/id',identity(fid,str(correct[i]).lower())]})
    return {'knowledge_point':KP,'question':{':question/id':qid,':question/problem':prompt,
        ':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':fields},
        'generation':{'generator_version':VERSION,'template':'four-number-membership','profile':target,
            'seed':seed,'index':index,'parameters':[{'kind':n['kind'],'a':n['a'],'b':n['b']} for n in numbers],
            'membership_mask':sum(1 << i for i,c in enumerate(correct) if c),
            'duplicate_value_rejections':rejection_count,'source_question_ids': [replay[':question/id']] if replay else SOURCES,
            'domain':'four distinct real numbers; signed integer/rational/irrational classification',
            'dependencies':{'python':'3.13.5','packages':{}}},'assets':{}}


def parse_source_number(key):
    tex = re.search(r'\$(.*?)\$',key)[1].replace(' ','')
    sign = -1 if tex.startswith('-') else 1
    body = tex.lstrip('-')
    if re.fullmatch(r'\d+',body): return number('integer',int(tex))
    match = re.fullmatch(r'\\frac\{(\d+|\\pi)\}\{(\d+)\}',body)
    if match:
        return number('pi' if match[1] == r'\pi' else 'fraction',sign if match[1] == r'\pi' else sign*int(match[1]),int(match[2]))
    match = re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}',body)
    if match: return number('sqrt' if not match[1] else 'scaled-root',sign*int(match[1] or 1),int(match[2]))
    if body == r'\pi': return number('pi',sign)
    raise ValueError('Unrecognized source: '+tex)


def replay_sources():
    data = json.loads(Path(__file__).with_name('source_cases.json').read_text())
    output = []
    for q in data[':knowledge-point/questions']:
        if not q.get(':question/worked-solution'): continue
        p = q[':question/problem']
        family = re.search(r'\{([QRZ])\}',p)[1]
        target = family + ('0' if '_{0}' in p else '') + ('+' if '^{+}' in p else '-')
        output.append(generate(target,[parse_source_number(f[':answer-field/key']) for f in q[':question/answer-fields']],replay=q))
    return output


def batch(difficulty, count, seed):
    if difficulty != 'easy': raise ValueError('Only source-supported easy difficulty is available')
    if count < 0: raise ValueError('count must be nonnegative')
    rng = random.Random(seed); output = []
    for i in range(count):
        target,numbers,rejections = sample(rng)
        output.append(generate(target,numbers,seed=seed,index=i,rejection_count=rejections))
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=('easy','moderate','hard'),default='easy')
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=('json',),default='json')
    parser.add_argument('--replay-source',action='store_true')
    args = parser.parse_args()
    try:
        records = replay_sources() if args.replay_source else batch(args.difficulty,args.count,args.seed)
    except ValueError as exc: parser.error(str(exc))
    print(json.dumps(records,ensure_ascii=False,indent=2))



# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__ == '__main__': main()
