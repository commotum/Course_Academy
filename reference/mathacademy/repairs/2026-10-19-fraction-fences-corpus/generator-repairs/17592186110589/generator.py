#!/usr/bin/env python3
"""Seeded, database-free quotient-rule questions. See instructional-account.md."""
import argparse
import json
import random
import sys
import uuid

from math_format import checked_math_content, normalize_prose, normalize_tex

VERSION = '1.0.1'
KP = {'db_id': 17592186110589, 'id': '48581e81-b2de-5be0-9e97-1057bedc16f3',
      'title': 'Separating a Logarithm Into Two Logarithms Using the Quotient Rule'}
SOURCE = {'symbolic': '20936b5f-864e-5ae6-90f1-dfba78a6f020',
          'natural': '46d440a6-1c70-56f2-8920-e5415a5e3165',
          'coefficient': '64d0c1d6-d1d1-543e-953b-1850c41d8e50'}


def log(base, argument):
    return rf'\log_{{{base}}} ({argument})'


def ln(argument):
    return rf'\ln({argument})'


def fraction(a, b):
    return rf'\frac{{{a}}}{{{b}}}'


def domain(difficulty):
    if difficulty == 'easy':
        return [{'template': 'symbolic', 'orientation': orientation, 'base': base}
                for orientation in (0, 1) for base in range(2, 13)]
    if difficulty == 'moderate':
        return [{'template': 'natural', 'orientation': orientation, 'k': k, 'n': n}
                for orientation in (0, 1) for k in range(2, 7) for n in range(2, 16)]
    raise ValueError('Unsupported difficulty: ' + difficulty)


@checked_math_content
def generate(instance, rng=None, *, seed=None):
    """One shared instance determines every learner-facing dependent component."""
    rng = random.Random(0) if rng is None else rng
    p = dict(instance)
    template = p['template']
    orientation = p.get('orientation', 0)
    if orientation not in (0, 1):
        raise ValueError('orientation must be 0 or 1')
    if template == 'symbolic':
        base = p['base']
        if type(base) is not int or not 2 <= base <= 12:
            raise ValueError('base outside supported range')
        x, y = log(base, 'x'), log(base, 'y')
        numerator, denominator = ('x', 'y') if orientation == 0 else ('y', 'x')
        expression = log(base, fraction(numerator, denominator))
        bank = [f'{y} - {x}', rf'{x}\cdot {y}', fraction(x, y), f'{x}+{y}', f'{x}-{y}']
        correct = bank[4] if orientation == 0 else bank[0]
        problem = f'${expression}=$'
        rule = r'\log_n(a)-\log_n(b)=\log_n(\frac{a}{b})'
        first = "First, let's recall the quotient rule for logarithms:"
        second = 'Using the quotient rule for logarithms, we obtain:'
        derivation = rf'\begin{{aligned}}{expression} &= {correct}\end{{aligned}}'
        difficulty = 'easy'
        domain_note = '\n\nAssume $x>0$ and $y>0$.'
    elif template == 'natural':
        k, n = p['k'], p['n']
        if type(k) is not int or type(n) is not int or not (2 <= k <= 6 and 2 <= n <= 15):
            raise ValueError('natural-log parameters outside supported range')
        epower = rf'e^{{{k}}}'
        numerator, denominator = (epower, str(n)) if orientation == 0 else (str(n), epower)
        expression = ln(fraction(numerator, denominator))
        N = ln(n)
        bank = [fraction('e', N), fraction(k, N), f'{k}-{N}', f'e-{N}', f'{N}-{k}']
        correct = bank[2] if orientation == 0 else bank[4]
        problem = f'${expression}=$'
        rule = r'\ln(a)-\ln(b)=\ln(\frac{a}{b})'
        first = "First, let's recall the quotient rule for natural logarithms:"
        second = 'Using the quotient rule for natural logarithms, the given expression can be rewritten as:'
        separated = f'{ln(numerator)}-{ln(denominator)}'
        derivation = rf'\begin{{aligned}}{expression} &= {separated} \\ &= {correct}\end{{aligned}}'
        difficulty = 'moderate'
        domain_note = ''
    elif template == 'coefficient':
        # The incomplete source is retained only for faithful, corrected replay.
        if p != {'template': 'coefficient', 'orientation': 0, 'base': 5, 'c': 2}:
            raise ValueError('coefficient profile is replay-only at source parameters')
        x, y = log(5, 'p'), log(5, 'q')
        bank = [f'{log(5, "2p")} - {log(5, "2q")}', f'2{x} - 2{y}',
                f'2{x} - {y}', f'2({x})/({y})', f'{log(5, "2p")} - {y}']
        correct = bank[1]
        expression = '2' + log(5, fraction('p', 'q'))
        problem = f'What is ${expression}$?'
        rule = r'\log_n(a)-\log_n(b)=\log_n(\frac{a}{b})'
        first = "First, let's recall the quotient rule for logarithms:"
        second = 'Using the quotient rule and distributing the outside coefficient, we obtain:'
        derivation = (rf'\begin{{aligned}}{expression} &= 2({x}-{y}) \\ '
                      rf'&= {correct}\end{{aligned}}')
        difficulty = None
        domain_note = '\n\nAssume $p>0$ and $q>0$.'
    else:
        raise ValueError('unknown template')
    problem = normalize_prose(problem + domain_note)
    solution = normalize_prose(f'{first}\n\n$$\n{rule}\n$$\n\n{second}\n\n$$\n{derivation}\n$$')
    bank = [normalize_tex(v) for v in bank]
    correct = normalize_tex(correct)
    # Identities depend on content, not seeds or presentation order. Delivery
    # subsequently applies the publisher's own authoritative stable identities.
    content = json.dumps([problem, solution, difficulty, sorted(bank), correct], separators=(',', ':'))
    qid = uuid.uuid5(uuid.UUID(KP['id']), content)
    fid = uuid.uuid5(qid, 'selection')
    choices = [{':answer/id': str(uuid.uuid5(fid, v)), ':answer/type': ':answer.type/math', ':answer/value': v}
               for v in bank]
    rng.shuffle(choices)
    field = {':answer-field/id': str(fid), ':answer-field/key': 'selection',
             ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': choices,
             ':answer-field/correct': [':answer/id', str(uuid.uuid5(fid, correct))]}
    question = {':question/id': str(qid), ':question/problem': problem,
                ':question/worked-solution': solution, ':question/answer-fields': [field]}
    if difficulty:
        question[':question/difficulty'] = ':question.difficulty/' + difficulty
    # Make the source's implicit positive-variable assumptions explicit.
    return {'knowledge_point': dict(KP), 'question': question,
            'generation': {'generator_version': VERSION, 'template': template, 'parameters': p,
                           'bank_profile': template + '-source-complete', 'seed': seed,
                           'source_question_ids': [SOURCE[template]],
                           'original_difficulty': difficulty,
                           'domain': domain_note.strip() or 'Positive real logarithm arguments; base e.',
                           'replay_only': template == 'coefficient',
                           'source_repair': 'Missing key and solution inferred by quotient rule and distribution.'
                                            if template == 'coefficient' else None,
                           'dependencies': {'python': sys.version.split()[0], 'packages': {}}}}


def generate_many(difficulty='moderate', count=5, seed=0):
    if difficulty == 'unclassified':
        difficulty = 'moderate'
    available = domain(difficulty)
    if count < 0 or count > len(available):
        raise ValueError(f'count must be between 0 and {len(available)} distinct semantic instances')
    rng = random.Random(seed)
    records = []
    for _ in range(count):
        # Choose the answer-bearing assignment before compatible numeric values.
        orientation = rng.choice(sorted({p['orientation'] for p in available}))
        instance = rng.choice([p for p in available if p['orientation'] == orientation])
        available.remove(instance)
        records.append(generate(instance, rng, seed=seed))
    return records


def source_replays():
    return [generate({'template': 'symbolic', 'orientation': 0, 'base': 3}),
            generate({'template': 'natural', 'orientation': 0, 'k': 3, 'n': 8}),
            generate({'template': 'coefficient', 'orientation': 0, 'base': 5, 'c': 2})]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', default='moderate', choices=['unclassified', 'easy', 'moderate', 'hard'])
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json'], default='json')
    args = parser.parse_args()
    try:
        records = generate_many(args.difficulty, args.count, args.seed)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
