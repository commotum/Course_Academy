#!/usr/bin/env python3
"""Seeded special-set membership and universal-containment practice; no I/O assets."""
import argparse
import copy
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path
import random
import re
import uuid

from math_format import checked_math_content, normalize_prose

VERSION = '1.1.0'
KP = {'db_id': 17592186054816, 'id': '1d132801-b9cc-5c0c-a8fa-0c8b840c05bd',
      'title': 'Identifying Sets Containing a Given Element'}
SYMBOLS = ['N', 'N0', 'C'] + [b + s for b in ('Z', 'Q', 'R') for s in ('', '+', '-', '0+', '0-')]
CATEGORIES = ['posint', 'negint', 'zero', 'posrat', 'negrat', 'posirr', 'negirr']
CAT_NAMES = {'posint': 'a positive integer', 'negint': 'a negative integer', 'zero': 'zero',
             'posrat': 'a positive rational number that is not an integer',
             'negrat': 'a negative rational number that is not an integer',
             'posirr': 'a positive irrational number', 'negirr': 'a negative irrational number'}
WITNESSES = dict(zip(CATEGORIES, ['1', '-1', '0', r'\frac{1}{2}', r'-\frac{1}{2}', r'\sqrt{2}', r'-\sqrt{2}']))
GROUPS = {'positive integers': ['posint'], 'natural numbers': ['posint'],
          'negative integers': ['negint'], 'integers': ['posint', 'negint', 'zero'],
          'nonnegative integers': ['posint', 'zero'],
          'positive rational numbers': ['posint', 'posrat'],
          'negative rational numbers': ['negint', 'negrat'],
          'rational numbers': ['posint', 'negint', 'zero', 'posrat', 'negrat'],
          'real numbers': CATEGORIES}
PROFILES = ('root', 'fraction', 'pi', 'reciprocal', 'universal', 'decimal')
RADIO_BANKS = {
    'radio-0': ('I and II only', 'None', 'II only', 'I, II, III, and IV', 'II and III only'),
    'radio-1': ('I and IV only', 'I and II only', 'I only', 'III only', 'III and IV only'),
    'radio-2': ('I and IV only', 'III only', 'II and IV only', 'II and III only', 'I and III only'),
    'radio-10': ('I and IV only', 'II and IV only', 'I and III only', 'II and III only', 'None'),
}
ROMANS = ('I', 'II', 'III', 'IV')


def selection(label):
    return {ROMANS.index(s) for s in re.findall(r'\b(?:IV|III|II|I)\b', label)}
SOURCE_IDS = ['1da25f7d-182b-5d2d-b5c8-9d3f66bb445c', 'cedbe49b-bcb9-5d4b-9edb-8a333a5510e3',
              'a76aa6b8-9cdb-5c77-a90e-5b72a9324e9b', 'e51e86f2-eaf4-5f67-aebb-f55a23118243',
              '7e2347db-9785-54d2-a2a4-893dc1f56ec9', 'f51862bd-578b-533f-86e5-e297bb989e9a',
              '4fc9ff9e-591c-5172-b83a-e2856d63bd94',
              'a3dec5c5-6226-58b5-981a-1d9be8ed928c', 'fbe70e06-2b02-5b5d-9ff3-573e87348689',
              '6a8f22cc-a913-5e4d-85f6-bfc29e71f1a0', '17cf8bd5-1b50-5ea6-9196-c8cc3bb865c7']


def uid(*parts):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy/special-sets/' + json.dumps(parts, sort_keys=True)))


def tex(symbol):
    if symbol == 'N0': return r'\mathbb{N}_0'
    base, suffix = symbol[0], symbol[1:]
    return r'\mathbb{' + base + '}' + ('_0' if '0' in suffix else '') + (('^{' + suffix[-1] + '}') if suffix else '')


def meaning(symbol):
    if symbol == 'N': return 'the positive integers (natural numbers)'
    if symbol == 'N0': return 'the nonnegative integers'
    if symbol == 'C': return 'all complex numbers'
    names = {'Z': 'integers', 'Q': 'rational numbers', 'R': 'real numbers'}
    suffix = symbol[1:]
    qualifier = {'': 'all ', '+': 'the positive ', '-': 'the negative ', '0+': 'the nonnegative ', '0-': 'the nonpositive '}[suffix]
    return qualifier + names[symbol[0]]


def belongs(category, symbol):
    if symbol == 'C': return True
    if symbol == 'N': return category == 'posint'
    if symbol == 'N0': return category in ('zero', 'posint')
    base, suffix = symbol[0], symbol[1:]
    integral = category in ('posint', 'negint', 'zero')
    rational = category not in ('posirr', 'negirr')
    family = base == 'R' or (base == 'Q' and rational) or (base == 'Z' and integral)
    sign = 0 if category == 'zero' else (-1 if category.startswith('neg') else 1)
    allowed_signs = {'': (-1, 0, 1), '+': (1,), '-': (-1,), '0+': (0, 1), '0-': (-1, 0)}[suffix]
    return family and sign in allowed_signs


def target_categories(instance):
    return GROUPS[instance['group']] if instance['profile'] == 'universal' else [instance['category']]


def qualifies(instance, symbol):
    return all(belongs(c, symbol) for c in target_categories(instance))


def frac_tex(n, d):
    return ('-' if n < 0 else '') + r'\frac{' + str(abs(n)) + '}{' + str(d) + '}'


def number_instance(profile, **values):
    """Derive display, semantic class and first solution stage from the same values."""
    result = {'profile': profile, **values}
    if profile == 'root':
        n, sign = values['radicand'], values['sign']
        if n < 0 or sign not in (-1, 1): raise ValueError('real roots and a unit sign required')
        k = isqrt(n)
        expression = ('-' if sign < 0 else '') + r'\sqrt{' + str(n) + '}'
        category = 'zero' if n == 0 else ('pos' if sign > 0 else 'neg') + ('int' if k*k == n else 'irr')
        opening = (f'First, we note that ${expression}={sign*k}$ is {CAT_NAMES[category]}.' if k*k == n else
                   f'The radicand ${n}$ is not a perfect square, so ${expression}$ is {CAT_NAMES[category]}.')
    elif profile == 'fraction':
        n, d = values['numerator'], values['denominator']
        if d <= 0: raise ValueError('positive denominator required')
        f = Fraction(n, d)
        expression = frac_tex(n, d)
        category = 'zero' if not f else ('pos' if f > 0 else 'neg') + ('int' if f.denominator == 1 else 'rat')
        reduced = str(f.numerator) if f.denominator == 1 else frac_tex(f.numerator, f.denominator)
        opening = f'First, we note that ${expression}={reduced}$ is {CAT_NAMES[category]}.'
    elif profile in ('pi', 'reciprocal'):
        sign = values['sign']
        if sign not in (-1, 1): raise ValueError('unit sign required')
        expression = ('-' if sign < 0 else '') + (r'\pi' if profile == 'pi' else r'\frac{1}{\pi}')
        category = 'posirr' if sign > 0 else 'negirr'
        opening = f'The number ${expression}$ is {CAT_NAMES[category]}. It is not a rational number.'
    elif profile == 'decimal':
        expression = values['value']
        f = Fraction(expression)
        category = 'zero' if not f else ('pos' if f > 0 else 'neg') + ('int' if f.denominator == 1 else 'rat')
        opening = f'The terminating decimal ${expression}={frac_tex(f.numerator, f.denominator)}$ is {CAT_NAMES[category]}.'
    else: raise ValueError('unsupported number profile')
    result.update(expression=expression, category=category, opening=opening)
    return result


def solution(instance, candidates, bank_profile='checkbox'):
    if instance['profile'] == 'universal':
        group = instance['group']
        opening = f'We must check whether each set contains all the {group}.'
    else:
        opening = instance['opening']
    lines = [opening]
    for symbol in candidates:
        name = '$' + tex(symbol) + '$'
        verdict = qualifies(instance, symbol)
        definition = f'The set {name} contains {meaning(symbol)}.'
        if instance['profile'] == 'universal':
            if verdict:
                reason = f'By the number-set hierarchy and the sign restrictions, every member of the given class belongs to {name}.'
            else:
                counter = next(c for c in target_categories(instance) if not belongs(c, symbol))
                reason = f'For instance, ${WITNESSES[counter]}$ is in the given class but not in {name}. Therefore, this set does not contain all the {instance["group"]}.'
        else:
            reason = f'Therefore, ${instance["expression"]}$ ' + ('belongs' if verdict else 'does not belong') + f' to {name}.'
        lines.append('- ' + definition + ' ' + reason)
    selected = ['$' + tex(s) + '$' for s in candidates if qualifies(instance, s)]
    if bank_profile == 'checkbox':
        conclusion = ', '.join(selected) + ' only' if selected else '"None of the above"'
    else:
        actual = {i for i, s in enumerate(candidates) if qualifies(instance, s)}
        conclusion = '"' + next(label for label in RADIO_BANKS[bank_profile] if selection(label) == actual) + '"'
    lines.append('Therefore, select ' + conclusion + '.')
    return '\n\n'.join(lines)


@checked_math_content
def make_record(instance, candidates, seed=None, bank_profile='checkbox'):
    if len(candidates) != 4 or len(set(candidates)) != 4 or not set(candidates) <= set(SYMBOLS):
        raise ValueError('four distinct lesson sets required')
    if instance['profile'] == 'universal':
        prompt = f'To which of the following sets do all the {instance["group"]} belong?'
    else:
        prompt = f'To which of the following sets does the number ${instance["expression"]}$ belong?'
    if bank_profile == 'checkbox':
        prompt += '\n\nSelect all that apply. If none of the sets apply, select "None of the above".'
    elif bank_profile in RADIO_BANKS:
        prompt += '\n\n' + '\n\n'.join(f'{ROMANS[i]}. ${tex(s)}$' for i, s in enumerate(candidates))
    else:
        raise ValueError('unknown response bank')
    explanation = normalize_prose(solution(instance, candidates, bank_profile))
    identity = uid(normalize_prose(prompt), candidates, explanation)
    fields = []
    for symbol in candidates + ['None'] if bank_profile == 'checkbox' else []:
        field_id = uid(identity, symbol)
        choices = [{':answer/id': uid(field_id, v), ':answer/type': ':answer.type/text', ':answer/value': v}
                   for v in ('false', 'true')]
        answer = str(not any(qualifies(instance, s) for s in candidates) if symbol == 'None' else qualifies(instance, symbol)).lower()
        fields.append({':answer-field/id': field_id, ':answer-field/key': 'None of the above' if symbol == 'None' else '$' + tex(symbol) + '$',
                       ':answer-field/type': ':answer-field.type/checkbox', ':answer-field/choices': choices,
                       ':answer-field/correct': [':answer/id', uid(field_id, answer)]})
    if bank_profile != 'checkbox':
        fid = uid(identity, 'selection')
        actual = {i for i,s in enumerate(candidates) if qualifies(instance,s)}
        choices = [{':answer/id': uid(fid, label), ':answer/type': ':answer.type/text', ':answer/value': label}
                   for label in RADIO_BANKS[bank_profile]]
        key = next(a for a in choices if selection(a[':answer/value']) == actual)
        fields.append({':answer-field/id': fid, ':answer-field/key': 'selection',
                       ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': choices,
                       ':answer-field/correct': [':answer/id', key[':answer/id']]})
    return {'knowledge_point': KP.copy(), 'question': {':question/id': identity,
                ':question/difficulty': ':question.difficulty/easy', ':question/problem': normalize_prose(prompt),
                ':question/worked-solution': explanation, ':question/answer-fields': fields},
            'generation': {'generator': VERSION, 'template': 'universal' if instance['profile'] == 'universal' else 'individual',
                           'profile': instance['profile'], 'seed': seed, 'instance': copy.deepcopy(instance),
                           'candidates': list(candidates), 'source_ids': SOURCE_IDS,
                           'bank_profile': bank_profile, 'source_difficulty': 'easy'}, 'assets': []}


def sample_instance(rng, profile=None, target=None):
    profile = profile or rng.choice(PROFILES)
    if profile == 'universal': return {'profile': profile, 'group': target or rng.choice(list(GROUPS))}
    allowed = {'root': ['posint','negint','zero','posirr','negirr'], 'fraction': CATEGORIES[:5],
               'pi': ['posirr','negirr'], 'reciprocal': ['posirr','negirr'], 'decimal': CATEGORIES[:5]}[profile]
    category = target or rng.choice(allowed)
    if category not in allowed: raise ValueError('category outside representation domain')
    # Select semantic target before constructing compatible surface values.
    sign = -1 if category.startswith('neg') else 1
    if profile == 'root':
        radicand = 0 if category == 'zero' else (rng.randint(1,12)**2 if category.endswith('int') else rng.choice([n for n in range(2,145) if isqrt(n)**2 != n]))
        return number_instance(profile, radicand=radicand, sign=sign)
    if profile == 'fraction':
        d = rng.randint(2,12)
        if category == 'zero': n = 0
        elif category.endswith('int'): n = sign*rng.randint(1,12)*d
        else: n = sign*(rng.randint(0,8)*d + rng.randint(1,d-1))
        return number_instance(profile, numerator=n, denominator=d)
    if profile == 'decimal':
        places = rng.randint(1,4)
        scale = 10**places
        units = 0 if category == 'zero' else rng.randint(1,12)*scale if category.endswith('int') else rng.randint(0,8)*scale + rng.randint(1,scale-1)
        value = ('-' if sign < 0 else '') + str(units//scale) + '.' + str(units%scale).zfill(places)
        return number_instance(profile, value=value)
    return number_instance(profile, sign=sign)


def sample(rng, seed):
    profile = rng.choice(PROFILES)
    if profile == 'universal':
        target = rng.choice(list(GROUPS))
        skeleton = {'profile': profile, 'group': target}
    else:
        domains = {'root': ['posint','negint','zero','posirr','negirr'],
                   'fraction': CATEGORIES[:5], 'pi': ['posirr','negirr'],
                   'reciprocal': ['posirr','negirr'], 'decimal': CATEGORIES[:5]}
        target = rng.choice(domains[profile])
        skeleton = {'profile': profile, 'category': target}
    good = [s for s in SYMBOLS if qualifies(skeleton,s)]
    bad = [s for s in SYMBOLS if not qualifies(skeleton,s)]
    counts = [n for n in range(5) if n <= len(good) and 4-n <= len(bad)]
    bank_profile = rng.choice(['checkbox'] + list(RADIO_BANKS))
    if bank_profile == 'checkbox':
        positions = set(rng.sample(range(4), rng.choice(counts)))
    else:
        eligible = [selection(label) for label in RADIO_BANKS[bank_profile] if len(selection(label)) in counts]
        positions = rng.choice(eligible)
    count = len(positions)
    # Assign answer-bearing roles first; incidental parameter values do not affect these choices.
    positives, negatives = iter(rng.sample(good,count)), iter(rng.sample(bad,4-count))
    candidates = [next(positives) if i in positions else next(negatives) for i in range(4)]
    instance = sample_instance(rng, profile, target)
    return make_record(instance,candidates,seed,bank_profile)


def generate(difficulty='easy', count=5, seed=0):
    if difficulty == 'unclassified': difficulty = 'easy'
    if difficulty != 'easy': raise ValueError('Only easy is supported by the source evidence')
    if count < 0: raise ValueError('count must be nonnegative')
    rng = random.Random(seed)
    records, seen = [], set()
    attempts = 0
    while len(records) < count:
        attempts += 1
        if attempts > max(100, count*100): raise ValueError('could not fill unique batch')
        record = sample(rng,seed)
        identity = record['question'][':question/id']
        if identity in seen: continue
        seen.add(identity)
        record['generation']['attempt'] = attempts
        records.append(record)
    return records


SOURCE_SPECS = [
    (number_instance('root',radicand=2,sign=1), ['Q+','R','Q','Z']),
    (number_instance('decimal',value='1.4142'), ['Q0+','Q','Z','Q-']),
    ({'profile':'universal','group':'natural numbers'}, ['Q-','Q','R','Z-']),
    (number_instance('root',radicand=121,sign=1), ['Q-','N','Z','Z-']),
    (number_instance('pi',sign=-1), ['C','Q','Q-','R']),
    (number_instance('reciprocal',sign=1), ['Q','Z','Q+','R']),
    ({'profile':'universal','group':'real numbers'}, ['Q-','Z-','N','Q']),
    ({'profile':'universal','group':'positive integers'}, ['Z-','N','Q-','R+']),
    (number_instance('fraction',numerator=72,denominator=9), ['Q0-','N','R','Q+']),
    (number_instance('root',radicand=81,sign=-1), ['Z0-','Z-','R','Z']),
    ({'profile':'universal','group':'negative integers'}, ['Z','Z+','Q+','Q-']),
]


def source_symbol(key):
    if key in ('None', 'None of the above'): return None
    base = re.search(r'[NZQRC]', key).group()
    return base + ('0' if '0' in key else '') + ('+' if '+' in key else '-' if '-' in key else '')


@checked_math_content
def replay_source(index):
    """Source presentation replay, with independently derived keys, retaining complete banks.

    Exact source prose is a replay fixture, not a claim that missing prose was observed.
    Normal generation always computes its prose from the parameterized solution above.
    """
    sources = json.loads(Path(__file__).with_name('source_cases.json').read_text())
    source = sources[index]
    instance, candidates = SOURCE_SPECS[index]
    profile = 'radio-'+str(index) if index in (0,1,2,10) else 'checkbox'
    record = make_record(instance,candidates,bank_profile=profile)
    q = record['question']
    q[':question/problem'] = normalize_prose(source[':question/problem'])
    q[':question/worked-solution'] = normalize_prose(source.get(':question/worked-solution',solution(instance,candidates,profile)))
    fields = []
    for j, old in enumerate(source[':question/answer-fields']):
        f = {k: copy.deepcopy(v) for k,v in old.items() if k != ':db/id'}
        f[':answer-field/type'] = old[':answer-field/type'][':db/ident']
        f[':answer-field/choices'] = [{':answer/id': a[':answer/id'], ':answer/type': a[':answer/type'][':db/ident'], ':answer/value': a[':answer/value']} for a in old[':answer-field/choices']]
        if profile != 'checkbox':
            actual = {i for i,s in enumerate(candidates) if qualifies(instance,s)}
            expected = next(a[':answer/value'] for a in f[':answer-field/choices'] if selection(a[':answer/value']) == actual)
        else:
            symbol = source_symbol(f[':answer-field/key'])
            expected = str(qualifies(instance,symbol) if symbol else not any(qualifies(instance,s) for s in candidates)).lower()
        correct = next(a for a in f[':answer-field/choices'] if a[':answer/value']==expected)
        f[':answer-field/correct'] = [':answer/id',correct[':answer/id']]
        fields.append(f)
    q[':question/answer-fields'] = fields
    q[':question/id'] = uid(q[':question/problem'],q[':question/worked-solution'],fields)
    record['generation'].update(source_id=source[':question/id'], replay_only=True,
        source_difficulty=source.get(':question/difficulty'),
        recovery_note='Missing key/solution/difficulty reconstructed; no original difficulty asserted.' if index<3 else None,
        bank_profile=profile)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',default='easy')
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    parser.add_argument('--replay-source',choices=['all']+[str(i) for i in range(len(SOURCE_SPECS))])
    args = parser.parse_args()
    try:
        if args.difficulty not in ('easy','unclassified'): raise ValueError('Only easy is supported')
        records = ([replay_source(i) for i in range(len(SOURCE_SPECS))] if args.replay_source=='all' else
                   [replay_source(int(args.replay_source))] if args.replay_source else
                   generate(args.difficulty,args.count,args.seed))
    except ValueError as error: parser.error(str(error))
    print(json.dumps(records,indent=2,ensure_ascii=False))


# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__ == '__main__': main()
