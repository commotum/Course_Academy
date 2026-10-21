#!/usr/bin/env python3
"""Seeded quotient-rule practice; only moderate is source-supported."""
import argparse
import copy
import json
import math
from pathlib import Path
import random
import uuid
from math_format import checked_math_content, normalize_prose, normalize_tex

VERSION = '1.0.1'
KP = {'db_id': 17592186110592, 'id': '543da446-8e2b-5978-b5fd-886a3b89e57c',
      'title': 'Evaluating an Expression Using the Quotient Rule'}
BASES = ['2', '3', '5', '7', '11', 'common', 'natural']
LABELS = [('p', 'q'), ('k', 'm'), ('r', 's'), ('u', 'v')]
ARGUMENTS = [('x', 'y'), ('a', 'b'), ('c', 'd')]
SOURCES = {
 'direct': ['401099a0-a99c-5a60-b909-8cc3beb26f5a', '99f3a3dc-a29b-56b3-b6b2-eb00c09e4e97'],
 'implicit': ['1cafb86d-67ee-5dc9-8df3-72a8bf590a76'],
 'nested': ['ada9c1dd-522d-5138-9cfe-44ee7af19872']}


def frac(a, b):
    return rf'\frac{{{a}}}{{{b}}}'


def log(base, arg):
    op = r'\log' if base == 'common' else r'\ln' if base == 'natural' else rf'\log_{{{base}}}'
    return op + rf'\left({arg}\right)'


def bank(labels, profile):
    a, b = labels
    if profile == 'D':
        return [f'{a}-{b}', f'{b}-{a}', f'{a}+{b}', frac(a, b), frac(b, a)]
    return [f'{a}-{b}', f'{a}+{b}', frac(a, b), a+b, f'{b}-{a}']


def numeric_values(i):
    """Concrete log values only for the numerical implicit-quotient family."""
    base = math.e if i['base'] == 'natural' else 10 if i['base'] == 'common' else int(i['base'])
    a, b = [math.log(int(x), base) for x in i['arguments']]
    return [a-b, b-a, a+b, a/b, b/a]


def admissible(i):
    if i['family'] != 'implicit':
        return True
    values = numeric_values(i)
    return all(not math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-11)
               for j, a in enumerate(values) for b in values[j+1:])


def sample_instance(rng, stats=None):
    # Select mathematical role assignments before numbers, bases, or display order.
    family = rng.choice(['direct', 'implicit', 'nested'])
    target = rng.randrange(2) if family != 'nested' else 0
    assignment = rng.randrange(2)
    given_order = rng.randrange(2)
    mode = rng.choice(['symbolic', 'constant-first', 'constant-second']) if family == 'direct' else family
    while True:
        labels = list(rng.choice(LABELS))
        if assignment:
            labels.reverse()
        base = rng.choice(BASES)
        symbols = list(rng.choice(ARGUMENTS))
        if family == 'implicit':
            m, d = rng.randint(2, 15), rng.randint(2, 9)
            arguments = [str(m*d), str(m)]
        elif family == 'nested':
            # The whole expression and its quotient are the two known objects.
            arguments = [symbols[1], frac(symbols[1], symbols[0])]
        else:
            arguments = symbols
            if mode == 'constant-first':
                arguments[0] = str(rng.randint(2, 12))
            elif mode == 'constant-second':
                arguments[1] = str(rng.randint(2, 12))
        i = dict(family=family, base=base, arguments=arguments, labels=labels,
                 target=target, given_order=given_order, assignment=assignment,
                 mode=mode, symbols=symbols, profile='N' if family == 'nested' else 'D')
        if admissible(i):
            if stats is not None:
                stats['accepted_instances'] = stats.get('accepted_instances', 0) + 1
            return i
        if stats is not None:
            stats['numeric_bank_rejections'] = stats.get('numeric_bank_rejections', 0) + 1


def identity(text):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy/quotient-rule/v1/' + text))


@checked_math_content
def generate(instance, rng=None, seed=None, source_fixture=None):
    i = copy.deepcopy(instance)
    family, base, args, labels = i['family'], i['base'], i['arguments'], i['labels']
    if not admissible(i):
        raise ValueError('Coincident numerical choice values')
    order = [0, 1] if i['given_order'] == 0 else [1, 0]
    givens = [f'${log(base, args[j])}={labels[j]}$' for j in order]
    first, second = (i['target'], 1-i['target']) if family != 'nested' else (0, 1)
    left, right = args[first], args[second]
    correct = labels[first] + '-' + labels[second]
    if family == 'nested':
        requested = i['symbols'][0]
    elif family == 'implicit':
        from fractions import Fraction
        value = Fraction(int(left), int(right))
        requested = str(value.numerator) if value.denominator == 1 else frac(value.numerator, value.denominator)
    else:
        requested = frac(left, right)
    prompt = f'If {givens[0]} and {givens[1]}, then ${log(base, requested)}=$'
    adjective = 'common logarithms' if base == 'common' else 'natural logarithms' if base == 'natural' else 'logarithms'
    rule_base = base if base in ('common', 'natural') else 'n'
    rule = f'{log(rule_base, "a")}-{log(rule_base, "b")}={log(rule_base, frac("a", "b"))}'
    solution = f"First, let's recall the quotient rule for {adjective}:\n\n$$\n{rule}\n$$\n\n"
    solution += f'Using the quotient rule for {adjective}, we have\n\n$$\n'
    steps = [log(base, requested)]
    if family == 'nested':
        steps.append(log(base, frac(left, rf'\left({right}\right)')))
    elif family == 'implicit':
        steps.append(log(base, frac(left, right)))
    steps.extend([f'{log(base, left)}-{log(base, right)}', correct])
    solution += r'\begin{aligned}' + steps[0] + ''.join((' &=' if j == 0 else r' \\ & =') + step for j, step in enumerate(steps[1:])) + r'\end{aligned}' + '\n$$'
    # Keep bank orientation independent of the known-log role assignment.
    # In profile N, otherwise its sole fraction would reveal the subtraction order.
    values = bank(sorted(labels), i['profile'])
    source_difficulty = None
    if source_fixture is not None:
        # Original presentation is retained only at the verified source parameters.
        prompt = source_fixture[':question/problem']
        solution = source_fixture.get(':question/worked-solution', solution)
        values = [a[':answer/value'] for a in source_fixture[':question/answer-fields'][0][':answer-field/choices']]
        source_difficulty = source_fixture.get(':question/difficulty', {}).get(':db/ident')
        # Repair captured operator spelling without changing any mathematical content.
        for old, new in [(r'\operatorname{log}', r'\log'), ('{log}', r'\log'), ('\u2061', '')]:
            prompt, solution = prompt.replace(old, new), solution.replace(old, new)
    prompt, solution = normalize_prose(prompt), normalize_prose(solution)
    values = [normalize_tex(v) for v in values]
    # IDs depend on content, not seed. Choice ordering is cosmetic and reproducible.
    signature = json.dumps([prompt, sorted(values)], ensure_ascii=False)
    qid = identity(signature)
    fid = identity(qid + '/selection')
    choices = [{':answer/id': identity(fid+'/'+v), ':answer/type': ':answer.type/math', ':answer/value': v} for v in values]
    def canonical(v):
        return v.replace(' ', '').replace(labels[1]+'+'+labels[0], labels[0]+'+'+labels[1])
    correct_choice = next(a for a in choices if canonical(a[':answer/value']) == correct)
    if rng is not None:
        rng.shuffle(choices)
    field = {':answer-field/id': fid, ':answer-field/key': 'selection', ':answer-field/type': ':answer-field.type/radio',
             ':answer-field/choices': choices, ':answer-field/correct': [':answer/id', correct_choice[':answer/id']]}
    generation = dict(generator_version=VERSION, template=family, profile=i['profile'], parameters=i, seed=seed,
                      source_question_ids=SOURCES[family], source_difficulty=source_difficulty if source_fixture else 'moderate',
                      source_replay=source_fixture is not None,
                      domain='Positive real arguments; common base > 0 and != 1. Numeric arguments > 1.',
                      correct_expression=correct, python='3.13.5')
    if source_fixture:
        generation['replayed_source_question_id'] = source_fixture[':question/id']
        generation['reconstructed_fields'] = [name for name in (':question/difficulty', ':question/worked-solution') if name not in source_fixture]
        if ':answer-field/correct' not in source_fixture[':question/answer-fields'][0]:
            generation['reconstructed_fields'].append(':answer-field/correct')
    return {'knowledge_point': KP.copy(), 'question': {':question/id': qid, ':question/difficulty': ':question.difficulty/moderate',
            ':question/problem': prompt, ':question/worked-solution': solution, ':question/answer-fields': [field]},
            'generation': generation, 'assets': []}


def replay_sources():
    fixtures = json.loads(Path(__file__).with_name('source-fixtures.json').read_text())
    params = [
        dict(family='direct', base='2', arguments=['x','y'], labels=['p','q'], target=0, symbols=['x','y'], mode='symbolic'),
        dict(family='implicit', base='3', arguments=['4','8'], labels=['p','q'], target=1, symbols=['x','y'], mode='implicit'),
        dict(family='direct', base='common', arguments=['2','y'], labels=['p','q'], target=0, symbols=['x','y'], mode='constant-first'),
        dict(family='nested', base='common', arguments=['y',frac('y','x')], labels=['k','m'], target=0, symbols=['x','y'], mode='nested')]
    return [generate(p | dict(given_order=0, assignment=0, profile='N' if p['family']=='nested' else 'D'), source_fixture=q)
            for p,q in zip(params,fixtures)]


def make_batch(count, seed, difficulty='moderate', stats=None):
    if difficulty != 'moderate':
        raise ValueError('Only moderate is supported by the captured practice questions')
    if count < 1:
        raise ValueError('count must be positive')
    rng = random.Random(seed)
    return [generate(sample_instance(rng, stats), rng, seed) for _ in range(count)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', default='moderate', choices=['easy','moderate','hard'])
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json'], default='json')
    parser.add_argument('--replay-source', action='store_true')
    args = parser.parse_args()
    if args.difficulty != 'moderate':
        parser.error('Only moderate is supported by the captured practice questions')
    try:
        records = replay_sources() if args.replay_source else make_batch(args.count, args.seed, args.difficulty)
    except ValueError as e:
        parser.error(str(e))
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
