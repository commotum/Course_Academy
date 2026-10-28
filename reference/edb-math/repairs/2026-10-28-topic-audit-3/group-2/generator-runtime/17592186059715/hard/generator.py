"""Seeded local continuation of draft 17592186059715; no database access.

The retained draft renderer is in plot_helper.py. Source omissions stay in replay;
normal records explicitly complete them. See instructional-account.md.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import random
import re
import uuid

os.environ.setdefault('MPLCONFIGDIR', '/tmp/course-academy-mpl-17592186059715')
import sympy as sp
from math_format import normalize_prose, normalize_tex, validate_generated_record
from plot_helper import render_plots

SOURCE = json.loads((Path(__file__).parent / 'source_data.json').read_text())
KP = SOURCE['record']
KP_ID = KP[':db/id']
KP_UUID = KP[':knowledge-point/id']
VERSION = 'position-magnitude-v4'
# Each bank member can be the target with the same instructional workload.
NORMS = sorted({x*x+y*y for x in range(1,9) for y in range(1,9)})
SPECS = {
    'q-18051': ('AB', [[-4,1],[3,0]], 'position', 'radio'),
    'q-18052': ('PQ', [[-2,2],[3,3]], 'position-displacement', 'radio'),
    'q-125118': ('PQ', [[1,2],[-2,1]], 'position-displacement', 'radio'),
    'q-18049': ('CD', [[-1,3],[1,-2]], 'position', 'radio'),
    'q-18055': ('PQ', [[1,1],[2,3]], 'grid', 'radio'),
    'q-320965': ('AB', [[0,3],[4,-1]], 'position', 'blank'),
    'q-18057': ('AC', [[0,3],[4,0]], 'grid', 'radio'),
    'q-320964': ('AB', [[-2,0],[3,3]], 'position', 'blank'),
    'q-18050': ('CD', [[0,2],[4,-1]], 'position-displacement', 'radio'),
    'q-18054': ('CD', [[-3,4],[2,3]], 'grid', 'radio'),
    'e-4298': ('AB', [[1,3],[2,-2]], 'position-displacement', 'radio'),
}
ORIGINALS = {q[':question/math-academy-id']: q for q in KP[':knowledge-point/questions']}
ORIGINALS['e-4298'] = KP[':knowledge-point/canonical-example']


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def identity(parent, value):
    return str(uuid.uuid5(uuid.UUID(parent), value))


def vector(x, y):
    # Retained draft convention: ordinary i,j components and omitted unit 1.
    return sp.latex(x*sp.Symbol('i') + y*sp.Symbol('j'))


def arrow(pair):
    return r'\overset{\to }{' + pair + '}'


def math_value(value):
    value = value.replace(' ', '')
    m = re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}', value)
    return sp.Integer(m[1] or 1)*sp.sqrt(int(m[2])) if m else sp.Integer(value)


def magnitude_class(n):
    root = sp.sqrt(n)
    if root.is_Integer:
        return 'integer'
    return 'irreducible' if root.args == (sp.Integer(n), sp.Rational(1,2)) else 'reducible'


def validate_points(points):
    if len(points) != 2 or any(len(p) != 2 for p in points):
        raise ValueError('two 2D endpoints required')
    if any(type(v) is not int or not -5 <= v <= 5 for p in points for v in p):
        raise ValueError('integer endpoints in [-5,5] required')
    d = [points[1][i] - points[0][i] for i in range(2)]
    if d == [0, 0] or any(abs(v) > 8 for v in d):
        raise ValueError('distinct endpoints with displacement components of size at most 8 required')
    return d


def solution(points, labels, graph):
    p, q = points
    a, b = labels
    aa, bb = a.lower(), b.lower()
    dx, dy = [q[i]-p[i] for i in range(2)]
    n = dx*dx+dy*dy
    v = arrow(labels)
    intro = (f'From the picture, we obtain ${a}({p[0]},{p[1]})$ and ${b}({q[0]},{q[1]})$. So, we have' if graph else 'We have')
    root = rf'\sqrt{{{n}}}'
    final = sp.latex(sp.sqrt(n))
    terminal = root + (r' \\ &= ' + final if final != root else '')
    return (intro + '\n\n$$\n' + rf'\begin{{aligned}} & {arrow("O"+a)}={aa}={vector(*p)}, \\ & {arrow("O"+b)}={bb}={vector(*q)}.\end{{aligned}}' + '\n$$\n\n'
        + f'Expressing ${v}$ as the difference of position vectors, we obtain:\n\n$$\n'
        + rf'\begin{{aligned}}{v} &= {arrow("O"+b)}-{arrow("O"+a)} \\ &= {bb}-{aa} \\ &= ({vector(*q)})-({vector(*p)}) \\ &= {vector(dx,dy)}\end{{aligned}}' + '\n$$\n\n'
        + 'Now, using the formula for the magnitude of a vector, we get\n\n$$\n'
        + rf'\begin{{aligned}}|{v}| &= \sqrt{{({dx})^{{2}}+({dy})^{{2}}}} \\ &= \sqrt{{{dx*dx}+{dy*dy}}} \\ &= {terminal}.\end{{aligned}}' + '\n$$')


def normalize_question(q):
    q = copy.deepcopy(q)
    q.pop(':db/id', None)
    for key in [':question/problem', ':question/worked-solution']:
        if key in q:
            q[key] = normalize_prose(q[key])
    if isinstance(q.get(':question/difficulty'), dict):
        q[':question/difficulty'] = q[':question/difficulty'][':db/ident']
    for f in q.get(':question/answer-fields', []):
        f.pop(':db/id', None)
        f[':answer-field/type'] = f[':answer-field/type'][':db/ident']
        for a in f[':answer-field/choices']:
            a.pop(':db/id', None)
            a[':answer/type'] = a[':answer/type'][':db/ident']
            a[':answer/value'] = normalize_tex(a[':answer/value'])
        if ':answer-field/correct' in f:
            f[':answer-field/correct'] = [':answer/id', f[':answer-field/correct'][':answer/id']]
    return q


def replay(mid):
    """Exact evidence replay (including omissions), not normal delivery output."""
    q = normalize_question(ORIGINALS[mid])
    return {'knowledge_point': knowledge_point(), 'question': q,
            'generation': {'version': VERSION, 'source_ids': [mid], 'evidence_only': True,
                           'parameters': {'points': SPECS[mid][1]}, 'basis': SOURCE['basis']}}


def knowledge_point():
    return {'db_id': KP_ID, 'id': KP_UUID, 'title': KP[':knowledge-point/title']}


def build(mid, points, seed=0, rank=None, choice_position=None, labels=None, source_bank=False, bank_radicands=None, difficulty="moderate", response_kind=None, plot_style=None):
    labels0, _, style, kind = SPECS[mid]
    kind = response_kind or kind
    style = plot_style or style
    labels = labels or labels0
    if labels not in ('AB', 'PQ', 'CD', 'AC'):
        raise ValueError('unsupported endpoint labels')
    d = validate_points(points)
    p, q = points
    n = sum(v*v for v in d)
    # Independent stream: never reuse template-selection draws for option order.
    rng = random.Random(digest({'seed': seed, 'stream': 'answer-bank-presentation'}))
    if rank is not None and (rank not in range(5) or rank > NORMS.index(n)):
        raise ValueError('rank must be 0..4 with enough smaller eligible norms')
    asset = render_plots(points, labels, style)
    a, b = labels
    v = arrow(labels)
    if style == 'grid':
        problem = f"![]({asset['reference']})\n\nPoints ${a}$ and ${b}$ are shown in the picture above. Find $|{v}|$."
    else:
        problem = f"![]({asset['reference']})\n\nLet ${a}({p[0]},{p[1]})$ and ${b}({q[0]},{q[1]})$. Find $|{v}|$."
    if kind == 'blank':
        problem += f' Do not round the answer.\n\n$|{v}|=$\n' + '{{field-1}}'
    values = [sp.latex(sp.sqrt(n))]
    profile = 'exact-blank' if kind == 'blank' else 'exchangeable-displacement-norms'
    if kind == 'radio':
        if source_bank:
            if points != SPECS[mid][1]:
                raise ValueError('source bank is an original-parameter anchor')
            values = [a[':answer/value'] for a in ORIGINALS[mid][':question/answer-fields'][0][':answer-field/choices']]
            profile = 'source-' + mid
        else:
            if bank_radicands is not None:
                bank = list(bank_radicands)
                if len(bank)!=5 or len(set(bank))!=5 or n not in bank or any(k not in NORMS for k in bank):
                    raise ValueError('bank requires five eligible distinct norms including target')
            elif rank is None:
                bank = [n] + rng.sample([k for k in NORMS if k!=n], 4)
            else:
                # Explicit validation intervention only: normal sampling chooses
                # the target uniformly from an independently sampled whole bank.
                below = rng.sample([k for k in NORMS if k<n], rank)
                above = rng.sample([k for k in NORMS if k>n], 4-rank)
                bank = [n]+below+above
            rank = sorted(bank).index(n)
            values = [sp.latex(sp.sqrt(k)) for k in bank]
        rng.shuffle(values)
        if choice_position is not None:
            if choice_position not in range(5):
                raise ValueError('choice position must be 0..4')
            index = next(i for i,value in enumerate(values) if sp.simplify(math_value(value)**2-n)==0)
            values[index], values[choice_position] = values[choice_position], values[index]
    problem = normalize_prose(problem)
    worked = normalize_prose(solution(points, labels, style == 'grid'))
    # Path-independent IDs: output relocation does not change question/field IDs.
    content = {'version': VERSION, 'mid': mid, 'points': points, 'labels': labels,
               'values': sorted(values), 'style': style, 'kind': kind, 'difficulty': difficulty}
    qid = identity(KP_UUID, digest(content))
    fid = identity(qid, 'field')
    answers = [{':answer/id': identity(fid, value), ':answer/type': ':answer.type/math', ':answer/value': normalize_tex(value)} for value in values]
    correct = next(a[':answer/id'] for a in answers if sp.simplify(math_value(a[':answer/value'])**2-n)==0)
    field = {':answer-field/id': fid, ':answer-field/key': 'field-1' if kind == 'blank' else 'selection',
             ':answer-field/type': ':answer-field.type/'+kind, ':answer-field/choices': answers,
             ':answer-field/correct': [':answer/id', correct]}
    question = {':question/id': qid, ':question/difficulty': ':question.difficulty/'+difficulty,
                ':question/problem': problem, ':question/worked-solution': worked,
                ':question/answer-fields': [field]}
    return validate_generated_record({'knowledge_point': knowledge_point(), 'question': question,
        'generation': {'version': VERSION, 'seed': seed, 'source_ids': [mid],
            'template': style+'/'+kind+'/'+labels, 'bank_profile': profile,
            'parameters': {'points': points, 'labels': labels, 'displacement': d,
                           'squared_norm': n, 'magnitude_class': magnitude_class(n), 'rank': rank if kind=='radio' else None},
            'basis': SOURCE['basis'], 'assets': [asset],
            'authored_completion': mid in ('q-18051','q-18052','q-125118','q-18049','q-18055'),
            'parameter_fingerprint': digest({'points':points, 'kind':kind, 'graph':style=='grid'}),
            'bank_radicands': [int(math_value(value)**2) for value in values]}})


def sample_points(rng, quadrant, target_class, rank=0):
    # Sample the answer-bearing case first; enumerate compatible displacements.
    signs = [(1,1),(1,-1),(-1,1),(-1,-1)][quadrant]
    compatible = [(signs[0]*x, signs[1]*y) for x in range(1,9) for y in range(1,9)
                  if magnitude_class(x*x+y*y) == target_class and rank <= NORMS.index(x*x+y*y)
                  and len(NORMS)-1-NORMS.index(x*x+y*y) >= 4-rank]
    dx, dy = rng.choice(compatible)
    p = [rng.randint(max(-5,-5-dx),min(5,5-dx)), rng.randint(max(-5,-5-dy),min(5,5-dy))]
    return [p, [p[0]+dx,p[1]+dy]]


def generate(difficulty='moderate', seed=0, template=None, parameters=None):
    """All bands retain endpoint subtraction followed by exact magnitude.

    Easy reduces signed-coordinate arithmetic; moderate supplies signed endpoints;
    hard removes coordinate text and requires reading the same small grid domain.
    Exact blank entry is evidenced by q-320965/q-320964. No answer bank can
    replace endpoint reasoning. Explicit build/replay retain original radio anchors.
    """
    difficulty = 'moderate' if difficulty == 'unclassified' else difficulty
    if difficulty not in ('easy', 'moderate', 'hard'):
        raise ValueError('unknown difficulty')
    rng = random.Random(seed)
    mid = template or ('q-18055' if difficulty == 'hard' else 'q-320965')
    if mid not in SPECS:
        raise ValueError('unknown template')
    labels = rng.choice(('AB', 'PQ', 'CD', 'AC'))
    if parameters:
        points = parameters['points']
        labels = parameters.get('labels', labels)
    else:
        # Enumerate a bounded domain rather than silently rejecting axis cases.
        # Every feasible translation of the chosen displacement is eligible.
        lo, hi, limit = (0, 4, 4) if difficulty == 'easy' else (-4, 4, 6)
        displacements = [(x,y) for x in range(-limit,limit+1)
                         for y in range(-limit,limit+1)
                         if 0 < x*x+y*y <= (25 if difficulty == 'easy' else 52)]
        dx,dy = rng.choice(displacements)
        p = [rng.randint(max(lo,lo-dx),min(hi,hi-dx)),
             rng.randint(max(lo,lo-dy),min(hi,hi-dy))]
        points = [p,[p[0]+dx,p[1]+dy]]
    return build(mid, points, seed=seed, labels=labels, difficulty=difficulty,
                 response_kind='blank', plot_style='grid' if difficulty == 'hard' else 'position')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--difficulty', default='moderate', choices=['easy','moderate','hard','unclassified'])
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json'], default='json')
    args = parser.parse_args()
    if args.count < 1:
        parser.error('count must be positive')
    print(json.dumps([generate(args.difficulty,args.seed+i) for i in range(args.count)], indent=2))


if __name__ == '__main__':
    main()
