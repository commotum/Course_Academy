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

VERSION = '1.1.0'
KP = {'db_id':17592186054815, 'id':'abc6b3ee-0251-5c9c-9358-bd192c434dd1',
      'title':'Identifying Elements Belonging to Scripted Special Sets'}
TARGETS = ('Q-', 'R0-', 'Z0-', 'Q0+', 'R0+', 'Q0-', 'Z0+')
SOURCES = ['9392ab96-5be3-5aab-8c35-808d0b88162a','c2a941ac-46f5-56a9-b5ba-03889446453a',
 '016b340f-7aa5-5001-aeb3-927982c5cf50','c84fa181-6eb1-5e84-b542-36ff40a06a4c',
 '0e62d29f-2834-5b4e-b720-bc361e2a5dc0','12109bd9-1ea8-5fd9-b15c-ba4373902b35',
 'ac020dea-1486-5e82-bd01-29594c8fbf7a','4eae16cb-f514-5e15-a012-1e904a842a1d',
 '891fa895-d529-5c21-9765-4d2a287c7001','c620ed83-c013-5ff0-8983-14697bd50f1b',
 '59f3318f-8861-5823-9f55-694de5f640be']


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


ROMANS = ('I', 'II', 'III', 'IV')


def subset_label(mask):
    labels = [v for i,v in enumerate(ROMANS) if mask & (1 << i)]
    return ' and '.join(labels) + ' only' if labels else 'None'


def subset_mask(label):
    if label == 'None': return 0
    return sum(1 << ROMANS.index(v) for v in re.findall(r'\b(?:IV|III|II|I)\b', label))


def enum(value):
    return value[':db/ident'] if isinstance(value, dict) else value


@checked_math_content
def generate(target, numbers, *, seed=0, index=0, rejection_count=0, replay=None,
             response='checkbox'):
    if target not in TARGETS or len(numbers) != 4:
        raise ValueError('Four entries and a supported target are required')
    if replay is not None:
        response = enum(replay[':question/answer-fields'][0][':answer-field/type']).split('/')[-1]
    if response not in ('checkbox', 'radio'):
        raise ValueError('Unsupported response contract')
    correct = [belongs(n,target) for n in numbers]
    mask = sum(1 << i for i,c in enumerate(correct) if c)
    keys = ['$' + n['tex'] + '$' for n in numbers]
    prompt = 'Which of the numbers below belong to $' + symbol(target) + '$?'
    if response == 'radio':
        prompt += '\n\n' + '\n\n'.join(v + '. ' + k for v,k in zip(ROMANS,keys))
        rng = random.Random(identity(seed,index,target,[n['tex'] for n in numbers],'bank'))
        masks = [mask] + rng.sample([m for m in range(16) if m != mask],4)
        rng.shuffle(masks)
        specs = [('selection', [subset_label(m) for m in masks], subset_label(mask))]
        conclusion = subset_label(mask) + '.'
    else:
        prompt += '\n\nSelect all that apply.'
        specs = [(k, ['true','false'],str(c).lower()) for k,c in zip(keys,correct)]
        conclusion = '; '.join(k for k,c in zip(keys,correct) if c) + '.' if mask else 'None of those listed.'
    solution = 'Remember that $' + symbol(target) + '$ is the set of all ' + definition(target) + '.\n\n'
    solution += '\n\n'.join(explanation(n,target) for n in numbers)
    solution += '\n\nIn conclusion, the correct answer is: ' + conclusion
    if replay is not None:
        # Preserve the complete captured bank, not a global checkbox extension.
        prompt = replay[':question/problem'].replace('?$', '$?')
        if replay.get(':question/worked-solution'):
            solution = replay[':question/worked-solution']
            solution = re.sub(r'\\,✓\$', r'$ $\\checkmark$', solution)
            solution = re.sub(r'\\,\\times\s*\$', r'$ $\\times$', solution)
        specs = []
        ordinary_index = 0
        for f in replay[':question/answer-fields']:
            values = [a[':answer/value'] for a in f[':answer-field/choices']]
            key = f[':answer-field/key']
            if response == 'radio':
                matching = [v for v in values if subset_mask(v) == mask]
                if len(matching) != 1: raise ValueError('Source bank lacks a unique correct subset')
                answer = matching[0]
            elif key in ('None', 'None of the above'):
                answer = str(not any(correct)).lower()
            else:
                answer = str(correct[ordinary_index]).lower()
                ordinary_index += 1
            specs.append((key,values,answer))
    prompt = normalize_prose(prompt); solution = normalize_prose(solution)
    specs = [(normalize_prose(k),vs,c) for k,vs,c in specs]
    qid = identity(KP['id'],prompt,specs,response)
    fields = []
    for i,(key,values,answer) in enumerate(specs):
        fid = identity(qid,'field',i,key)
        answers = [{':answer/id':identity(fid,v),':answer/type':':answer.type/text',':answer/value':v} for v in values]
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+response,
                       ':answer-field/choices':answers,':answer-field/correct':[':answer/id',identity(fid,answer)]})
    record = {'knowledge_point':KP,'question':{':question/id':qid,':question/problem':prompt,
        ':question/worked-solution':solution,':question/difficulty':enum(replay.get(':question/difficulty', ':question.difficulty/easy')) if replay else ':question.difficulty/easy',':question/answer-fields':fields},
        'generation':{'generator_version':VERSION,'template':'four-number-membership','profile':target,
            'response_contract':response,'bank_profile':'captured' if replay else 'authored-five-subsets' if response == 'radio' else 'source-backed-explicit-none',
            'seed':seed,'index':index,'parameters':[{'kind':n['kind'],'a':n['a'],'b':n['b']} for n in numbers],
            'membership_mask':mask,
            'duplicate_value_rejections':rejection_count,'source_question_ids': [replay[':question/id']] if replay else SOURCES,
            'domain':'four distinct real numbers; signed integer/rational/irrational classification',
            'dependencies':{'python':'3.13.5','packages':{}}},'assets':{}}
    if replay is not None and not replay.get(':question/worked-solution'):
        record['generation']['source_missing_key_and_solution'] = True
    if replay is None and response == 'checkbox':
        record = explicit_none_checkbox(record, 'None of the above')
    return record


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


def source_target(q):
    p = q[':question/problem'].split('?',1)[0]
    family = re.search(r'(?:\\mathbb\{)?([QRZ])',p)[1]
    return family + ('0' if re.search(r'_\{?0',p) else '') + ('+' if '+' in p else '-')


def source_numbers(q):
    fields = q[':question/answer-fields']
    if enum(fields[0][':answer-field/type']) == ':answer-field.type/radio':
        entries = re.findall(r'(?m)^(?:IV|III|II|I|[1-4])\.\s*(\$[^$]+\$)',q[':question/problem'])
    else:
        entries = [f[':answer-field/key'] for f in fields if f[':answer-field/key'] not in ('None','None of the above')]
    return [parse_source_number(k) for k in entries]


def replay_sources():
    data = json.loads(Path(__file__).with_name('source_cases.json').read_text())
    return [generate(source_target(q),source_numbers(q),replay=q)
            for q in data[':knowledge-point/questions']]


def batch(difficulty, count, seed):
    if difficulty != 'easy': raise ValueError('Only source-supported easy difficulty is available')
    if count < 0: raise ValueError('count must be nonnegative')
    rng = random.Random(seed); output = []
    for i in range(count):
        response = rng.choice(('radio','checkbox'))
        target,numbers,rejections = sample(rng)
        output.append(generate(target,numbers,seed=seed,index=i,rejection_count=rejections,response=response))
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
from generator_policy import nonempty_checkbox as _nonempty_checkbox, explicit_none_checkbox
for _policy_name in ['batch', 'generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__ == '__main__': main()
