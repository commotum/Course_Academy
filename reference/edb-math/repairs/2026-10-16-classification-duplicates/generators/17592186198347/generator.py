#!/usr/bin/env python3
"""Seeded, database-free slope-intercept system classification generator."""
import argparse
import itertools
import json
from pathlib import Path
import random
import sys
import uuid

from math_format import checked_math_content, normalize_prose, system_tex

DATA = json.loads(Path(__file__).with_name('source_data.json').read_text())
VERSION = '1.0.1'
SLOPES = tuple(range(-8, 0)) + tuple(range(1, 9))
INTERCEPTS = tuple(range(-9, 10))
# Coincident lines through the origin cannot use the two distinct term orders.
LINE_COUNT = len(SLOPES) * len(INTERCEPTS)
MAX_INSTANCES = LINE_COUNT * (LINE_COUNT + 1) // 2 - len(SLOPES)
RELATIONS = ('parallel', 'intersecting', 'coincident')
BANKS = (
    ('are parallel', 'intersect at one point', 'coincide with each other'),
    ('no solutions', 'only one solution', 'infinitely many solutions'),
    ('inconsistent', 'consistent independent', 'consistent dependent'),
)
SOURCE_PARAMETERS = ((-2, 1, -2, 1, True), (6, 5, 5, 6, False))
INTRO = DATA['canonical'][':question/worked-solution'].split('Notice that')[0]
TAIL = "Select the correct options in the following reasoning.\n\nThe lines corresponding to the equations {{field-1}}. Therefore, the system has {{field-2}}, meaning that it's {{field-3}}."


def identity(value):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy:17592186198347:' + value))


def relation(m1, b1, m2, b2):
    if m1 != m2:
        return 'intersecting'
    return 'coincident' if b1 == b2 else 'parallel'


def rhs(m, b, intercept_first=False):
    term = 'x' if abs(m) == 1 else f'{abs(m)}x'
    if intercept_first and b:
        return f'{b} {"+" if m > 0 else "-"} {term}'
    out = ('-' if m < 0 else '') + term
    return out + (f' {"+" if b > 0 else "-"} {abs(b)}' if b else '')


def box(text):
    return r'$\bbox[3pt,Gainsboro]{\color{blue}\textrm{' + text + '}}$'


def solution(m1, b1, m2, b2):
    r = relation(m1, b1, m2, b2)
    i = RELATIONS.index(r)
    if r == 'parallel':
        comparison = f'the same slopes (${m1}$) but distinct $y$-intercepts (${b1}$ and ${b2}$, respectively)'
        geometry = f'So, the lines {box(BANKS[0][i])} and do not intersect.'
    elif r == 'coincident':
        comparison = f'the same slopes (${m1}$) and the same $y$-intercepts (${b1}$)'
        geometry = f'So, the lines {box(BANKS[0][i])} and share every point.'
    else:
        comparison = f'distinct slopes (${m1}$ and ${m2}$, respectively)'
        geometry = f'So, the lines {box(BANKS[0][i])}.'
    return normalize_prose(INTRO + 'Notice that the equations in the system have ' + comparison + '. ' + geometry
                           + f"\n\nTherefore, the system has {box(BANKS[1][i])}, meaning that it's {box(BANKS[2][i])}.")


@checked_math_content
def generate(m1, b1, m2, b2, intercept_first=False, *, seed=None, source_index=None):
    """One validated public record; parameters can also be supplied for replay."""
    if any(type(x) is not int for x in (m1, b1, m2, b2)):
        raise ValueError('Integer coefficients required')
    if m1 not in SLOPES or m2 not in SLOPES or b1 not in INTERCEPTS or b2 not in INTERCEPTS:
        raise ValueError('Coefficients outside documented domain')
    r = relation(m1, b1, m2, b2)
    if r == 'coincident':
        if b1 == 0:
            raise ValueError('Coincident lines require a nonzero intercept so their displayed equations differ')
        intercept_first = True
    equations = [f'y = {rhs(m1, b1, intercept_first)}', f'y = {rhs(m2, b2)}']
    problem = normalize_prose('Consider the following system of equations.\n\n$$\n' + system_tex(equations) + '\n$$\n\n' + TAIL)
    worked = solution(m1, b1, m2, b2)
    qid = identity(problem + '\n' + worked + '\n' + json.dumps(BANKS))
    fields = []
    for n, bank in enumerate(BANKS, 1):
        key = f'field-{n}'
        fid = identity(qid + ':' + key)
        choices = [{':answer/id': identity(fid + ':' + v), ':answer/type': ':answer.type/text', ':answer/value': v} for v in bank]
        fields.append({':answer-field/id': fid, ':answer-field/key': key, ':answer-field/type': ':answer-field.type/select',
                       ':answer-field/choices': choices, ':answer-field/correct': [':answer/id', choices[RELATIONS.index(r)][':answer/id']]})
    src = DATA['practice'][source_index] if source_index is not None else None
    return {
        'knowledge_point': {'id': DATA['kp_uuid'], 'db_id': DATA['kp_id'], 'title': DATA['title']},
        'question': {':question/id': qid, ':question/difficulty': ':question.difficulty/easy', ':question/problem': problem,
                     ':question/worked-solution': worked, ':question/answer-fields': fields},
        'generation': {'generator': 'slope-intercept-classification', 'version': VERSION, 'template': 'classify-two-slope-intercept-lines',
                       'difficulty': 'easy', 'seed': seed, 'parameters': {'m1': m1, 'b1': b1, 'm2': m2, 'b2': b2, 'intercept_first': intercept_first},
                       'relation': r, 'bank_profile': 'three-classifications', 'source_basis': DATA['basis'],
                       'source_question_ids': [q[':question/id'] for q in DATA['practice']], 'canonical_example_id': DATA['canonical'][':question/id'],
                       'replay_source_id': src[':question/id'] if src else None, 'source_difficulty': src.get(':question/difficulty') if src else None,
                       'source_correct_links_present': False, 'practice_solution_status': 'authored from canonical example',
                       'dependencies': {'python': '3.13.5', 'packages': {}},
                       'domain': {'slopes': list(SLOPES), 'intercepts': [-9, 9], 'relations': list(RELATIONS),
                                  'coincident_intercepts': 'nonzero'}}}


def replay_sources():
    return [generate(*p, source_index=i) for i, p in enumerate(SOURCE_PARAMETERS)]


def sample(count, seed, difficulty='easy'):
    if difficulty not in ('easy', 'unclassified'):
        raise ValueError('Unsupported difficulty: ' + difficulty)
    if not 0 <= count <= MAX_INSTANCES:
        raise ValueError(f'count must be between 0 and {MAX_INSTANCES} semantic instances')
    # Uniformly shuffle each relation pool, then round-robin active pools. No
    # duplicate unordered line pairs, even if term order or line order differs.
    rng = random.Random(seed)
    lines = list(itertools.product(SLOPES, INTERCEPTS))
    pools = {r: [] for r in RELATIONS}
    for a, b in itertools.combinations_with_replacement(lines, 2):
        if a == b and a[1] == 0:
            continue
        pools[relation(*a, *b)].append((*a, *b))
    for pool in pools.values():
        rng.shuffle(pool)
    order = list(RELATIONS)
    rng.shuffle(order)
    out = []
    while len(out) < count:
        for r in order:
            if not pools[r] or len(out) == count:
                continue
            m1, b1, m2, b2 = pools[r].pop()
            if rng.randrange(2):
                m1, b1, m2, b2 = m2, b2, m1, b1
            out.append(generate(m1, b1, m2, b2, bool(rng.randrange(2)), seed=seed))
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', default='easy')
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json'], default='json')
    args = parser.parse_args()
    try:
        records = sample(args.count, args.seed, args.difficulty)
    except ValueError as exc:
        parser.error(str(exc))
    json.dump(records, sys.stdout, indent=2)
    print()


if __name__ == '__main__':
    main()
