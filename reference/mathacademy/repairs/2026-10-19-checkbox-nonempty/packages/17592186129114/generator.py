#!/usr/bin/env python3
"""Source-backed row-echelon identification. Standard library, relocatable, no writes.

The legacy parser, leading-entry classifier, deterministic IDs and semantic batch
rejection are retained; current field layout and role-first sampling are repaired.
"""
import argparse
import itertools
import json
from pathlib import Path
import random
import re
import uuid
from math_format import checked_math_content, normalize_prose, matrix_tex

S = json.loads(Path(__file__).with_name('source-data.json').read_text())
KP_ID = 17592186129114
KP_UUID = S[':knowledge-point/id']
VERSION = 'echelon-identification-2.0.0'
SOURCES = {q[':question/math-academy-id']: q for q in S[':knowledge-point/questions']}
EXCLUDED = {'q-42369': 'Unrated radio source lacks correct answer and worked solution.'}
PROFILES = tuple(q for q in SOURCES if q not in EXCLUDED)
CASES = ('valid', 'zero', 'equal', 'left', 'both')
MATRIX = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)
CORRECTIONS = {'q-129225': 'C witness is c_45, not a_45.',
               'q-42366': 'C solution entry (3,4) is -2, matching the question.'}


def matrices(text):
    result = []
    for body in MATRIX.findall(text):
        rows = [[int(x.strip()) for x in row.split('&')] for row in body.split(r'\\')]
        if not rows or len({len(row) for row in rows}) != 1:
            raise ValueError('Ragged matrix')
        result.append(rows)
    return result


def leading(m):
    return [next((j for j, v in enumerate(row) if v != 0), None) for row in m]


def facts(m):
    p = leading(m)
    zero = next((i for i, x in enumerate(p) if x is None and any(y is not None for y in p[i+1:])), None)
    nonzero = [(i, j) for i, j in enumerate(p) if j is not None]
    pair = next(((a, b) for a, b in zip(nonzero, nonzero[1:]) if b[1] <= a[1]), None)
    return {'echelon': zero is None and pair is None, 'zero_witness': zero, 'pivot_pair': pair}


def original(profile):
    by_label = {}
    for field in SOURCES[profile][':question/answer-fields']:
        key = field[':answer-field/key']
        label = re.search(r'\$([ABC])\s*=', key)[1]
        by_label[label] = matrices(key)[0]
    return {'matrices': [by_label[x] for x in 'ABC']}


def make_matrix(rows, cols, case, rng):
    """Choose structural evidence before magnitudes or trailing entries."""
    if case not in CASES:
        raise ValueError('Unknown case')
    n = rng.randint(2, min(rows - int(case in ('zero', 'both')), cols))
    if case == 'equal':
        p = sorted(rng.sample(range(cols), n-1))
        at = rng.randrange(n-1)
        p.insert(at, p[at])
    else:
        p = sorted(rng.sample(range(cols), n))
        if case in ('left', 'both'):
            at = rng.randrange(n-1)
            p[at], p[at+1] = p[at+1], p[at]
    p += [None] * (rows-n)
    if case in ('zero', 'both'):
        p.pop()
        p.insert(rng.randrange(n), None)
    nonzero = tuple(range(-9, 0)) + tuple(range(1, 10))
    return [[0] * cols if j is None else [0] * j + [rng.choice(nonzero)] +
            [rng.randint(-9, 9) for _ in range(cols-j-1)] for j in p]


def sample(profile, rng):
    cases = ['valid' if rng.choice((False, True)) else rng.choice(CASES[1:]) for _ in 'ABC']
    # Classify first; conditional violation type second. No balancing quotas or
    # selected-count rejection: all eight classification assignments are eligible.
    ms = [make_matrix(len(old), len(old[0]), case, rng)
          for old, case in zip(original(profile)['matrices'], cases)]
    return {'matrices': ms, 'cases': cases}


def latex(m):
    return matrix_tex(m)


def fingerprint(question):
    ms = [matrices(f[':answer-field/key'])[0] for f in question[':question/answer-fields']]
    signatures = sorted((len(m), len(m[0]), tuple(-1 if p is None else p for p in leading(m))) for m in ms)
    return json.dumps(['not' if '**not**' in question[':question/problem'] else 'in', signatures], separators=(',', ':'))


def corrected_solution(profile):
    source = SOURCES[profile][':question/worked-solution']
    if profile == 'q-129225':
        source = source.replace('${a}_{45}', '${c}_{45}')
    if profile == 'q-42366':
        correct = original(profile)['matrices'][2]
        at = [0]
        def fix(match):
            at[0] += 1
            return latex(correct) if at[0] == 3 else match[0]
        source = MATRIX.sub(fix, source)
    return normalize_prose(source)


def render_solution(profile, ms):
    source = SOURCES[profile][':question/worked-solution']
    intro = source[:source.index('- The matrix')].rstrip()
    pieces = [intro]
    for label, m in zip('ABC', ms):
        f = facts(m)
        if f['echelon']:
            sentence = f'- The matrix ${label}$ is in row echelon form (both conditions are satisfied).'
        elif f['zero_witness'] is not None:
            names = ('first', 'second', 'third', 'fourth', 'fifth')
            sentence = (f'- The matrix ${label}$ is not in row echelon form since the '
                        f'{names[f["zero_witness"]]} row contains only zeros and it is not at the bottom '
                        'of the matrix (condition I is violated).')
        else:
            (i, a), (j, b) = f['pivot_pair']
            symbol = label.lower()
            relation = 'in the same column as' if a == b else 'to the left of'
            sentence = (f'- The matrix ${label}$ is not in row echelon form since the leading entry '
                        f'${symbol}_{{{j+1}{b+1}}}={m[j][b]}$ is {relation} the leading entry '
                        f'${symbol}_{{{i+1}{a+1}}}={m[i][a]}$ (condition II is violated).')
        pieces.append(sentence + '\n\n$$\n' + label + '=' + latex(m) + '\n$$')
    negate = '**not**' in SOURCES[profile][':question/problem']
    selected = [f'${label}$' for label, m in zip('ABC', ms) if facts(m)['echelon'] != negate]
    verb = '**not** in' if negate else 'in'
    if not selected:
        conclusion = ('Therefore, all three matrices are in row echelon form.' if negate else
                      'Therefore, none of the matrices are in row echelon form.')
    elif len(selected) == 1:
        conclusion = f'Therefore, only {selected[0]} is {verb} row echelon form.'
    elif len(selected) == 2:
        conclusion = f'Therefore, only {selected[0]} and {selected[1]} are {verb} row echelon form.'
    else:
        conclusion = f'Therefore, $A,$ $B,$ and $C$ are {verb} row echelon form.'
    return normalize_prose('\n\n'.join(pieces + [conclusion]))


@checked_math_content
def generate(difficulty, seed, profile=None, parameters=None, replay=False):
    if difficulty == 'unclassified':
        difficulty = 'easy'
    if difficulty != 'easy':
        raise ValueError('Unsupported difficulty: '+difficulty)
    rng = random.Random(seed)
    profile = profile or rng.choice(PROFILES)
    if profile not in PROFILES:
        raise ValueError('Unsupported profile')
    source = SOURCES[profile]
    p = parameters if parameters is not None else sample(profile, rng)
    ms = p['matrices']
    if len(ms) != 3:
        raise ValueError('Exactly three matrices required')
    for old, m in zip(original(profile)['matrices'], ms):
        if len(m) != len(old) or any(len(row) != len(old[0]) for row in m):
            raise ValueError('Shape profile mismatch')
        if any(type(v) is not int for row in m for v in row):
            raise ValueError('Integer entries required')
    if replay and p != original(profile):
        raise ValueError('Replay must use original parameters')
    problem = normalize_prose(source[':question/problem'])
    solution = corrected_solution(profile) if replay else render_solution(profile, ms)
    negate = '**not**' in problem
    keys = ['$'+label+'='+latex(m)+'$' for label, m in zip('ABC', ms)]
    identity = json.dumps([problem, keys, solution], separators=(',', ':'))
    qid = str(uuid.uuid5(uuid.UUID(KP_UUID), VERSION+'|'+identity))
    source_fields = source[':question/answer-fields']
    order = [re.search(r'\$([ABC])\s*=', f[':answer-field/key'])[1] for f in source_fields] if replay else list('ABC')
    fields = []
    for index, label in enumerate(order):
        m = ms['ABC'.index(label)]
        yes = facts(m)['echelon'] != negate
        fid = str(uuid.uuid5(uuid.UUID(qid), 'field/'+label))
        values = [a[':answer/value'] for a in source_fields[index][':answer-field/choices']] if replay else ['false', 'true']
        answers = [{':answer/id': str(uuid.uuid5(uuid.UUID(fid), value)), ':answer/type': ':answer.type/text', ':answer/value': value} for value in values]
        right = next(a for a in answers if a[':answer/value'] == str(yes).lower())
        key = normalize_prose(source_fields[index][':answer-field/key']) if replay else keys['ABC'.index(label)]
        fields.append({':answer-field/id': fid, ':answer-field/key': key,
                       ':answer-field/type': ':answer-field.type/checkbox', ':answer-field/choices': answers,
                       ':answer-field/correct': [':answer/id', right[':answer/id']]})
    q = {':question/id': qid, ':question/problem': problem, ':question/worked-solution': solution,
         ':question/difficulty': ':question.difficulty/easy', ':question/answer-fields': fields}
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': S[':knowledge-point/title']},
            'question': q, 'generation': {'version': VERSION, 'seed': seed,
            'template': 'select-not-echelon' if negate else 'select-echelon', 'profile': profile,
            'source_db_id': source[':db/id'], 'source_difficulty': source[':question/difficulty'],
            'parameters': p, 'replay': replay, 'source_correction': CORRECTIONS.get(profile),
            'mathematical_fingerprint': fingerprint(q), 'assets': []}}


def batch(difficulty, count, seed, stats=None):
    if difficulty not in ('easy', 'unclassified'):
        raise ValueError('Unsupported difficulty: '+difficulty)
    if not 0 <= count <= 1000:
        raise ValueError('Count must be 0..1000')
    out, seen, rejected = [], set(), 0
    for offset in range(max(200, 50*count)):
        if len(out) == count:
            break
        r = generate(difficulty, seed+offset)
        fp = r['generation']['mathematical_fingerprint']
        if fp in seen:
            rejected += 1
            continue
        seen.add(fp)
        out.append(r)
    if stats is not None:
        stats.update(attempted=len(out)+rejected, accepted=len(out), semantic_duplicates=rejected)
    if len(out) != count:
        raise ValueError('Bounded structural sampler exhausted; shortage explicit.')
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--difficulty', required=True)
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json'], default='json')
    args = parser.parse_args()
    print(json.dumps(batch(args.difficulty, args.count, args.seed), indent=2))



# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__ == '__main__':
    main()
