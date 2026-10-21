#!/usr/bin/env python3
"""Relocatable source-backed coefficient-echelon identification.

Retains coefficient(), leading(), facts(), seeded CLI and record identity design
from the supplied entry point. Replaces its frozen-role sampler and adds current
checkbox-key captures and complete radio-bank support. Standard library only.
"""
import argparse
import functools
import hashlib
import itertools
import json
from pathlib import Path
import random
import re
import uuid
from math_format import checked_math_content, normalize_prose, matrix_tex

S = json.loads(Path(__file__).with_name('source-data.json').read_text())
KP_ID = 17592186129113
KP_UUID = S['record'][':knowledge-point/id']
VERSION = 'coefficient-echelon-2.0.0'
SOURCES = {q[':question/math-academy-id']: q for q in S['record'][':knowledge-point/questions']}
PROFILES = tuple(SOURCES)
MATRIX = re.compile(r'\\left\[\s*\\begin\{array\}\{c+\|c\}(.*?)\\end\{array\}\s*\\right\]|\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)
NONZERO = tuple(range(-9, 0)) + tuple(range(1, 12))


def ident(x):
    return x[':db/ident'] if isinstance(x, dict) else x


def coefficient(m):
    return [row[:-1] for row in m]


def matrices(text):
    return [[[int(x.strip()) for x in row.split('&')] for row in (a or b).split(r'\\')]
            for a, b in MATRIX.findall(text)]


def leading(m):
    return [next((j for j, v in enumerate(row) if v != 0), None) for row in m]


def facts(m):
    pivots = leading(m)
    zero = next((i for i, p in enumerate(pivots) if p is None and any(q is not None for q in pivots[i+1:])), None)
    previous = None
    bad = None
    for i, p in enumerate(pivots):
        if p is None:
            continue
        if previous is not None and p <= previous and bad is None:
            bad = (i, p)
        previous = p
    return {'echelon': zero is None and bad is None, 'zero_witness': zero, 'pivot_witness': bad}


def case_of(pivots):
    if any(p is None and any(q is not None for q in pivots[i+1:]) for i,p in enumerate(pivots)):
        return 'zero'
    nz = [p for p in pivots if p is not None]
    if any(b < a for a,b in zip(nz,nz[1:])):
        return 'left'
    if any(b == a for a,b in zip(nz,nz[1:])):
        return 'equal'
    return 'valid'


def field_type(profile):
    return ident(SOURCES[profile][':question/answer-fields'][0][':answer-field/type']).split('/')[-1]


def original(profile):
    q = SOURCES[profile]
    if field_type(profile) == 'checkbox':
        fields = sorted(q[':question/answer-fields'], key=lambda f: re.search(r'([ABC])\s*=', f[':answer-field/key'])[1])
        ms = [matrices(f[':answer-field/key'])[0] for f in fields]
    else:
        ms = matrices(q[':question/problem'])
    assert len(ms) == 3
    return {'matrices': ms}


def bank(profile):
    return [a[':answer/value'] for a in SOURCES[profile][':question/answer-fields'][0][':answer-field/choices']]


def subset(value):
    return ''.join(x for x in 'ABC' if x in value)


def eligible_subsets(profile):
    return [subset(v) for v in bank(profile)] if field_type(profile) == 'radio' else [''.join(c) for n in range(4) for c in itertools.combinations('ABC', n)]


@functools.lru_cache(maxsize=None)
def pivot_domain(rows, cols, nonzero_rows):
    """Partition all same-workload patterns by their decisive rule case."""
    out = {k: [] for k in ('valid', 'zero', 'equal', 'left')}
    for nz_positions in itertools.combinations(range(rows), nonzero_rows):
        for cols_used in itertools.product(range(cols), repeat=nonzero_rows):
            it = iter(cols_used)
            pivots = tuple(next(it) if i in nz_positions else None for i in range(rows))
            out[case_of(pivots)].append(pivots)
    return {k:tuple(v) for k,v in out.items() if v}


def domains(profile, index):
    m = original(profile)['matrices'][index]
    return pivot_domain(len(m), len(m[0])-1, sum(p is not None for p in leading(coefficient(m))))


def fill(pivots, cols, rng):
    rows = []
    for p in pivots:
        if p is None:
            rows.append([0]*cols + [rng.randint(-9,11)])
        else:
            rows.append([0]*p + [rng.choice(NONZERO)] + [rng.randint(-9,11) for _ in range(cols-p)])
    return rows


def sample(profile, rng, target=None, cases=None):
    target = rng.choice(eligible_subsets(profile)) if target is None else target
    assert target in eligible_subsets(profile)
    negate = '**not**' in SOURCES[profile][':question/problem']
    ms = []
    for i, label in enumerate('ABC'):
        valid = (label in target) != negate
        domain = domains(profile, i)
        available = ['valid'] if valid else [k for k in domain if k != 'valid']
        case = cases[i] if cases is not None else rng.choice(available)
        assert case in available
        p = rng.choice(domain[case])
        ms.append(fill(p, len(original(profile)['matrices'][i][0])-1, rng))
    return {'matrices': ms}


def latex(m):
    return matrix_tex([[str(v) for v in row] for row in m], augmented=True)


def selected(profile, ms):
    negate = '**not**' in SOURCES[profile][':question/problem']
    return ''.join(label for label,m in zip('ABC',ms) if facts(coefficient(m))['echelon'] != negate)


def explanation(profile, ms):
    intro = ('A coefficient matrix, obtained by omitting the final column of its augmented matrix, is in row echelon form if it satisfies the following conditions:\n\n'
             'I. All the zero rows (rows with only zeros), if any, are placed at the *bottom* of the matrix.\n\n'
             'II. Each leading entry of a nonzero row is in a column *to the right* of the leading entry of the preceding nonzero row.\n\n'
             "With that in mind, let's look at each matrix in turn.")
    parts = [intro]
    for label,m in zip('ABC',ms):
        p = leading(coefficient(m))
        f = facts(coefficient(m))
        if f['echelon']:
            reason = 'is in row echelon form (both conditions are satisfied).'
        elif f['zero_witness'] is not None:
            i = f['zero_witness']
            later = next(j for j in range(i+1,len(p)) if p[j] is not None)
            reason = f'is not in row echelon form since coefficient row ${i+1}$ contains only zeros, but row ${later+1}$ is nonzero (condition I is violated).'
        else:
            i,j = f['pivot_witness']
            prev = max(k for k in range(i) if p[k] is not None)
            relation = 'in the same column as' if j == p[prev] else 'to the left of'
            reason = (f'is not in row echelon form since the leading entry in row ${i+1}$, column ${j+1}$ is {relation} '
                      f'the leading entry in row ${prev+1}$, column ${p[prev]+1}$ (condition II is violated).')
        parts.append(f'- The coefficient matrix of ${label}$ '+reason+'\n\n$$\n'+label+'='+latex(m)+'\n$$')
    labels = selected(profile,ms)
    if not labels:
        conclusion = 'Therefore, none of the matrices should be selected.'
    else:
        objects = ', '.join('$'+x+'$' for x in labels)
        conclusion = 'Therefore, select '+objects+'.'
    return '\n\n'.join(parts+[conclusion])


def fingerprint(record):
    # Ignore numeric values, source profile and permutations of matrix labels.
    # Keep role coverage separately; a cosmetic permutation is not new practice.
    signatures = sorted((len(m), len(m[0]), tuple(-1 if p is None else p for p in leading(coefficient(m))))
                        for m in record['generation']['parameters']['matrices'])
    return json.dumps([record['generation']['template'], signatures], separators=(',', ':'))


@checked_math_content
def generate(difficulty, seed, profile=None, parameters=None, replay=False, target=None, cases=None):
    if difficulty != 'easy':
        raise ValueError('Unsupported difficulty '+difficulty+': only the source-backed easy band is supported.')
    rng = random.Random(seed)
    profile = profile or rng.choice(PROFILES)
    source = SOURCES[profile]
    p = original(profile) if replay else parameters if parameters is not None else sample(profile,rng,target,cases)
    ms = p['matrices']
    for i,m in enumerate(ms):
        old = original(profile)['matrices'][i]
        assert len(m) == len(old) and all(len(row) == len(old[0]) for row in m)
        assert all(type(v) is int and -99 <= v <= 99 for row in m for v in row)
        assert tuple(leading(coefficient(m))) in sum((list(v) for v in domains(profile,i).values()), [])
    answer = selected(profile,ms)
    assert answer in eligible_subsets(profile)
    if replay:
        prompt = source[':question/problem']
        solution = source.get(':question/worked-solution') or explanation(profile,ms)
        if profile == 'q-129227':
            solution = solution.replace(r'B=\begin{bmatrix}9 &',r'B=\begin{bmatrix}8 &')
    else:
        polarity = 'that are **not** in' if '**not**' in source[':question/problem'] else 'in'
        prompt = ('Which of the following augmented matrices have coefficient matrices '+polarity+' row echelon form? '
                  'Treat the final column of each augmented matrix as its constants column.')
        if field_type(profile) == 'checkbox':
            prompt += '\n\nSelect all that apply.'
        else:
            prompt += '\n\n'+'\n\n'.join('$$\n'+label+'='+latex(m)+'\n$$' for label,m in zip('ABC',ms))
    if not replay:
        solution = explanation(profile,ms)
    prompt, solution = normalize_prose(prompt), normalize_prose(solution)
    # Include bank profile in identity, as two radio profiles have different banks.
    qid = str(uuid.uuid5(uuid.UUID(KP_UUID), VERSION+'|'+profile+'|'+prompt+'|'+json.dumps(ms)+'|'+solution))
    fields = []
    source_fields = source[':question/answer-fields']
    if field_type(profile) == 'checkbox':
        if replay:
            order = [re.search(r'([ABC])\s*=', f[':answer-field/key'])[1] for f in source_fields]
        else:
            order = list('ABC')
        for label in order:
            i = 'ABC'.index(label)
            sf = next(f for f in source_fields if re.search(r'([ABC])\s*=', f[':answer-field/key'])[1] == label)
            key = sf[':answer-field/key'] if replay else '$'+label+'='+latex(ms[i])+'$'
            values = [a[':answer/value'] for a in sf[':answer-field/choices']] if replay else ['false','true']
            fields.append(make_field(qid,label,key,'checkbox',values,'true' if label in answer else 'false'))
    else:
        values = bank(profile).copy()
        if not replay:
            rng.shuffle(values)
        correct = next(v for v in values if subset(v) == answer)
        fields.append(make_field(qid,'selection','selection','radio',values,correct))
    q = {':question/id':qid, ':question/problem':prompt, ':question/worked-solution':solution,
         ':question/difficulty':':question.difficulty/easy', ':question/answer-fields':fields}
    r = {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':S['record'][':knowledge-point/title']},'question':q,
         'generation':{'version':VERSION,'seed':seed,'profile':profile,'template':field_type(profile)+('-not' if '**not**' in prompt else '-in'),
                       'source_db_id':source[':db/id'],'source_difficulty':source.get(':question/difficulty'),
                       'parameters':p,'cases':[case_of(leading(coefficient(m))) for m in ms],
                       'replay':replay,'source_repairs':(['missing key and solution; easy is authored'] if profile=='q-42026' else ['solution B first entry 9 corrected to prompt 8'] if profile=='q-129227' else []),
                       'assets':[]}}
    r['generation']['mathematical_fingerprint'] = fingerprint(r)
    return r


def make_field(qid, label, key, kind, values, correct):
    fid = str(uuid.uuid5(uuid.UUID(qid), 'field/'+label))
    choices = [{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/text',':answer/value':v} for v in values]
    return {':answer-field/id':fid, ':answer-field/key':key, ':answer-field/type':':answer-field.type/'+kind,
            ':answer-field/choices':choices, ':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in choices if a[':answer/value']==correct)]}


def batch(difficulty, count, seed):
    if difficulty != 'easy':
        raise ValueError('Unsupported difficulty '+difficulty)
    if not 0 <= count <= 1000:
        raise ValueError('count must be between 0 and 1000')
    out, seen = [], set()
    for offset in range(max(200,50*count)):
        if len(out)==count:
            break
        # Random profile order avoids seed-independent first-profile schedules.
        r = generate(difficulty,seed+offset)
        fp = fingerprint(r)
        if fp not in seen:
            seen.add(fp); out.append(r)
    if len(out)!=count:
        raise ValueError(f'Bounded sampler produced {len(out)} of {count} distinct tasks')
    return out


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--difficulty',required=True)
    a.add_argument('--count',type=int,default=5)
    a.add_argument('--seed',type=int,default=0)
    a.add_argument('--format',choices=['json'],default='json')
    args = a.parse_args()
    print(json.dumps(batch(args.difficulty,args.count,args.seed),indent=2))



# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__ == '__main__':
    main()
