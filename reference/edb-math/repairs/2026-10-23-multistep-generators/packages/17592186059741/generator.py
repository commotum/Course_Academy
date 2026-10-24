"""Seeded, database-free scalar recovery. See instructional-account.md.

Adapted from the supplied 17592186059741-draft.py: retains source templating,
exact matrix parsing and field-owned stable identities, with repaired source
coverage, difficulty, complete empirical banks and relocatable imports.
"""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186059741-source-policy.json'))
    raise SystemExit(0)

import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import sys
import uuid

sys.dont_write_bytecode = True
import sympy as sp
from math_format import matrix_tex, normalize_prose, normalize_tex, checked_math_content

VERSION = '3.0.0'
HERE = Path(__file__).resolve().parent
SOURCE = json.loads((HERE / 'source-cases.json').read_text())
KP = SOURCE['record']
CASES = {q[':question/math-academy-id']: q for q in KP[':knowledge-point/questions']}
NS = uuid.UUID(KP[':knowledge-point/id'])
MAT = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)
K = sp.Symbol('k')
SUPPORTED_LEVELS = ('easy',)
POSITIONS = {'q-11442': [0, 0], 'q-981': [0, 0], 'q-139431': [0, 2],
             'q-320536': [1, 0], 'q-320551': [2, 0], 'q-320563': [0, 2],
             'q-69670': [0, 0], 'q-139630': [3, 0]}
PAYOFF = {'q-139431', 'q-139630'}


def parse(s):
    s = re.sub(r'\\(?:d?frac)\{(-?\d+)\}\{(\d+)\}', r'(\1/\2)', s)
    s = s.replace(' ', '').rstrip('.')
    s = re.sub(r'(\d|\))(?=k)', r'\1*', s)
    return sp.sympify(s, locals={'k': K}, rational=True)


def matrices(s):
    return [sp.Matrix([[parse(c) for c in row.split('&')]
                       for row in body.split(r'\\')]) for body in MAT.findall(s)]


def tex(v):
    return normalize_tex(sp.latex(v).replace(' ', ''))


def mat(a):
    return matrix_tex([[tex(a[i, j]) for j in range(a.cols)] for i in range(a.rows)])


def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()


DEFAULTS = {}
BANKS = {}
for sid, q in CASES.items():
    ms = matrices(q[':question/problem'])
    if sid == 'q-139431':
        a, b = ms
    else:
        b = ms[0]
        a = ms[1] if len(ms) > 1 else matrices(q[':question/worked-solution'])[0]
    c = next(y / x for x, y in zip(a, b) if x)
    DEFAULTS[sid] = {'matrix': [[str(x) for x in row] for row in a.tolist()],
                     'scalar': str(c), 'target': POSITIONS[sid]}
    f = q[':question/answer-fields'][0]
    if f[':answer-field/type'][':db/ident'].endswith('/radio'):
        BANKS[sid] = sorted(parse(z[':answer/value'].split('=')[-1])
                            for z in f[':answer-field/choices'])


def scalar_case(c):
    return ('positive' if c > 0 else 'negative') + ('_integer' if c.q == 1 else '_reciprocal')


def sample(rng, sid):
    # The correct bank member is assigned BEFORE values and presentation.
    role = rng.randrange(5) if sid in BANKS else None
    case = rng.choice(('positive_integer',) if sid in PAYOFF else
                      ('positive_integer', 'negative_integer') if sid in BANKS else
                      ('positive_integer', 'negative_integer', 'positive_reciprocal', 'negative_reciprocal'))
    sign = -1 if case.startswith('negative') else 1
    c = sp.Integer(sign * rng.randint(2, 9)) if case.endswith('integer') else sp.Rational(sign, rng.randint(2, 6))
    old = sp.Matrix(DEFAULTS[sid]['matrix'])
    if sid in PAYOFF:
        stake = rng.randint(1, 12)
        perm = list(range(old.rows))
        rng.shuffle(perm)
        a = sp.Matrix([[sp.sign(old[perm[i], perm[j]]) * stake
                        for j in range(old.cols)] for i in range(old.rows)])
    else:
        cells = [sp.Integer(0) if x == 0 else
                 sp.Integer(rng.choice((-1, 1)) * rng.randint(1, 12) * c.q) for x in old]
        rng.shuffle(cells)
        a = sp.Matrix(old.rows, old.cols, cells)
    target = rng.choice([[i, j] for i in range(a.rows) for j in range(a.cols) if a[i, j]])
    return {'matrix': [[str(x) for x in row] for row in a.tolist()], 'scalar': str(c), 'target': target}, role


def validate_parameters(p, sid, replay=False):
    if not isinstance(p, dict) or set(p) != {'matrix', 'scalar', 'target'}:
        raise ValueError('matrix/scalar/target required')
    a = sp.Matrix(p['matrix'])
    c = sp.Rational(p['scalar'])
    old = sp.Matrix(DEFAULTS[sid]['matrix'])
    if a.shape != old.shape or any(x.is_Integer is not True or abs(x) > 144 for x in a):
        raise ValueError('source-sized integral matrix with entries bounded by 144 required')
    if sum(x == 0 for x in a) != sum(x == 0 for x in old):
        raise ValueError('preserve zero count for comparable workload')
    target = p['target']
    if not isinstance(target, list) or len(target) != 2 or any(type(x) != int for x in target):
        raise ValueError('integer target pair required')
    i, j = target
    if not (0 <= i < a.rows and 0 <= j < a.cols) or a[i, j] == 0:
        raise ValueError('nonzero corresponding target required')
    allowed = (c.q == 1 and 2 <= abs(c) <= 9) or (abs(c.p) == 1 and 2 <= c.q <= 6)
    if sid in BANKS and c.q != 1:
        raise ValueError('empirical radio profiles support integer scalars only')
    if not allowed or any(x.is_Integer is not True or abs(x) > 864 for x in c * a):
        raise ValueError('small integer or reciprocal scalar and integral products required')
    if sid in PAYOFF:
        if c.q != 1 or not 2 <= c <= 9 or any(a[i, i] != 0 for i in range(a.rows)):
            raise ValueError('increased positive integral payoff multiplier required')
        if a != -a.T or len({abs(x) for x in a if x}) != 1:
            raise ValueError('common payoff stake with antisymmetric outcomes required')
    return a, c, i, j


def replace_matrices(s, values):
    values = list(values)
    if len(MAT.findall(s)) != len(values):
        raise ValueError('source matrix placeholder mismatch')
    it = iter(values)
    return MAT.sub(lambda _: mat(next(it)), s)


def components(sid, a, c, i, j, replay=False):
    q = CASES[sid]
    b, ak = c * a, K * a
    if sid == 'q-139431':
        problem = replace_matrices(q[':question/problem'], [a, b])
    elif sid == 'q-139630':
        problem = replace_matrices(q[':question/problem'], [b])
        # Original P is present in the solution but missing in the source prompt.
        problem = problem.replace('After increasing,', 'Her original payoff matrix was\n\n$$\nP=' + mat(a) + '\n$$\n\nAfter increasing,')
        problem = problem.replace('where$\\,k=$', 'where $k=$')
    else:
        problem = replace_matrices(q[':question/problem'], [b, a])
    if sid == 'q-11442' and replay:
        solution = q[':question/worked-solution']
    else:
        solution = q[':question/worked-solution']
        if sid == 'q-11442':
            solution = CASES['q-69670'][':question/worked-solution'].replace('kS', 'kG').replace('$S$', '$G$')
        solution = replace_matrices(solution, [a, ak, ak, b])
        if sid == 'q-139630' and not replay:
            # Keep each 4x4 side visible in the learner's narrow content card.
            solution = solution.replace(mat(ak) + '=' + mat(b),
                r'\begin{aligned} & ' + mat(ak) + r' \\ ={} & ' + mat(b) + r'\end{aligned}')
        start = solution.index("Let's choose ")
        end = solution.index('Equating these elements', start)
        if replay and [i, j] == POSITIONS[sid]:
            target_text = solution[start + len("Let's choose "):].split(', $')[0]
        else:
            target_text = f'the elements in row ${i+1}$ and column ${j+1}$'
        solution = solution[:start] + f"Let's choose {target_text}, ${tex(a[i,j]*K)}$ and ${tex(b[i,j])}.$ " + solution[end:]
        start = solution.index(r'\begin{aligned}', solution.index('Equating these elements'))
        end = solution.index(r'\end{aligned}', start) + len(r'\end{aligned}')
        solution = solution[:start] + r'\begin{aligned}' + tex(a[i,j]*K) + ' & =' + tex(b[i,j]) + r' \\ k & =' + tex(c) + r'.\end{aligned}' + solution[end:]
    return normalize_prose(problem), normalize_prose(solution)


@checked_math_content
def generate(level='easy', seed=0, template=None, parameters=None, bank_role=None, replay=False):
    if type(seed) != int:
        raise TypeError('seed must be an integer')
    if level not in SUPPORTED_LEVELS:
        raise ValueError('unsupported difficulty: only source-justified easy is supported')
    rng = random.Random(seed)
    sid = template or rng.choice(list(CASES))
    if sid not in CASES:
        raise ValueError('unknown source template')
    if replay:
        if parameters is not None or bank_role is not None:
            raise ValueError('replay fixes original parameters and bank role')
        p = DEFAULTS[sid]
        role = BANKS[sid].index(sp.Rational(p['scalar'])) if sid in BANKS else None
    elif parameters is None:
        p, role = sample(rng, sid)
        if bank_role is not None:
            role = bank_role
    else:
        p = parameters
        role = rng.randrange(5) if sid in BANKS else None
        if bank_role is not None:
            role = bank_role
    if sid in BANKS and (type(role) != int or not 0 <= role < 5):
        raise ValueError('bank role must be 0..4')
    if sid not in BANKS and bank_role is not None:
        raise ValueError('blank has no bank role')
    a, c, i, j = validate_parameters(p, sid, replay)
    radio = sid in BANKS
    values = [c + v - BANKS[sid][role] for v in BANKS[sid]] if radio else [c]
    if len(set(values)) != len(values):
        raise ValueError('complete bank collision')
    problem, solution = components(sid, a, c, i, j, replay)
    f = CASES[sid][':question/answer-fields'][0]
    ft = f[':answer-field/type'][':db/ident']
    fmt = (lambda v: normalize_tex('k=' + tex(v))) if radio else tex
    answers = [fmt(v) for v in values]
    identity = digest([VERSION, level, problem, solution, sorted(answers), ft])
    qid = str(uuid.uuid5(NS, identity))
    fid = str(uuid.uuid5(uuid.UUID(qid), f[':answer-field/key']))
    bank = [{':answer/id': str(uuid.uuid5(uuid.UUID(fid), v)), ':answer/type': ':answer.type/math', ':answer/value': v} for v in answers]
    correct = next(z[':answer/id'] for z in bank if z[':answer/value'] == fmt(c))
    rng.shuffle(bank)
    field = {':answer-field/id': fid, ':answer-field/key': f[':answer-field/key'],
             ':answer-field/type': ft, ':answer-field/choices': bank,
             ':answer-field/correct': [':answer/id', correct]}
    out = {':question/id': qid, ':question/problem': problem,
           ':question/worked-solution': solution, ':question/answer-fields': [field]}
    if not replay or ':question/difficulty' in CASES[sid]:
        out[':question/difficulty'] = ':question.difficulty/easy'
    pivot = next(x for x in a if x)
    fingerprint = digest([a.shape, [str(x / pivot) for x in a], str(c), sid in PAYOFF, radio])
    return {'knowledge_point': {'db_id': 17592186059741, 'id': KP[':knowledge-point/id'], 'title': KP[':knowledge-point/title']},
            'question': out,
            'generation': {'version': VERSION, 'seed': seed, 'template': sid,
                           'profile': ('empirical-' + sid) if radio else 'blank',
                           'bank_role': role, 'parameters': p, 'scalar_case': scalar_case(c),
                           'source_question_id': CASES[sid][':question/id'],
                           'source_difficulty': CASES[sid].get(':question/difficulty'),
                           'source_basis': SOURCE['basis'], 'source_lineage': SOURCE['lineage'],
                           'mathematical_fingerprint': fingerprint, 'replay': replay,
                           'candidate_rejections': 0, 'python': sys.version.split()[0], 'sympy': sp.__version__,
                           'repairs': ['first expansion -4 and -4k signs'] if sid == 'q-320536' else
                                      ['supply omitted original P from source solution'] if sid == 'q-139630' else []}}


def batch(level='easy', seed=0, count=5, **kw):
    if type(seed) != int or type(count) != int or count < 1:
        raise ValueError('integer seed and positive integer count required')
    if level not in SUPPORTED_LEVELS:
        raise ValueError('unsupported difficulty: ' + level)
    out, seen = [], set()
    for n in range(count * 1000):
        r = generate(level, seed + n, **kw)
        fingerprint = r['generation']['mathematical_fingerprint']
        if fingerprint not in seen:
            seen.add(fingerprint)
            out.append(r)
        if len(out) == count:
            return out
    raise ValueError('not enough distinct tasks')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty', choices=['easy', 'moderate', 'hard'], default='easy')
    p.add_argument('--count', type=int, default=5)
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('--format', choices=['json'], default='json')
    p.add_argument('--template', choices=list(CASES))
    p.add_argument('--replay', action='store_true')
    args = p.parse_args()
    if args.difficulty not in SUPPORTED_LEVELS:
        p.error('unsupported difficulty: only easy is source-justified')
    if args.replay:
        if not args.template:
            p.error('--replay requires --template')
        records = [generate(args.difficulty, args.seed, args.template, replay=True)]
    else:
        records = batch(args.difficulty, args.seed, args.count, template=args.template)
    print(json.dumps(records, indent=2, ensure_ascii=False))



from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186059741-source-policy.json'))

if __name__ == '__main__':
    main()
