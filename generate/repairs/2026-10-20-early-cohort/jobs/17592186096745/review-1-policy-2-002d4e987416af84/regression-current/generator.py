"""Seeded two-pivot 3x3 Gauss-Jordan generator; see instructional-account.md.

Started from the supplied legacy entrypoint. Source parsing, field-owned UUIDs,
seeded CLI and semantic deduplication are retained; all 17 supplied banks replay.
"""
import argparse
import hashlib
import json
import random
import re
import uuid
from pathlib import Path
import sympy as sp
from math_format import (checked_math_content, matrix_tex as format_matrix,
                         normalize_prose, normalize_tex, system_tex)

KP_ID = 17592186096745
KP_UUID = 'b010a518-7aa3-5b53-9a6d-ef0779ff0dfa'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
VERSION = 'two-pivot-affine-v2'
HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / 'source-data.json').read_text())
SOURCES = {q[':question/math-academy-id']: q for q in DATA['questions']}
PROFILES = tuple(SOURCES)
SLOPES = tuple(range(-3, 4))
INTERCEPTS = tuple(range(-4, 5))
MATRIX = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)
VARIABLES = sp.symbols('x y z')


def sources():
    return SOURCES


def parse_matrix(value):
    body = MATRIX.fullmatch(value.strip())
    if not body:
        raise ValueError('Expected complete matrix')
    return sp.Matrix([[sp.Rational(v.strip()) for v in row.split('&')]
                      for row in body[1].split('\\\\')])


def matrix_tex(matrix, augmented=False):
    return format_matrix([[sp.latex(v) for v in row] for row in matrix.tolist()],
                         augmented=augmented)


def prompt_matrix(text):
    body = text.split(r'\begin{aligned}', 1)[1].split(r'\end{aligned}', 1)[0]
    rows = []
    for row in body.split('\\\\'):
        lhs, rhs = row.replace('&', '').split('=')
        lhs = re.sub(r'(\d)\s*([xyz])', r'\1*\2', lhs)
        expr = sp.sympify(lhs, locals=dict(zip(('x', 'y', 'z'), VARIABLES)))
        rows.append([expr.coeff(v) for v in VARIABLES] + [sp.Rational(rhs.strip())])
    return sp.Matrix(rows)


def affine_matrix(values):
    sx, sy, bx, by = values
    return sp.Matrix([[1, 0, -sx, bx], [0, 1, -sy, by], [0, 0, 0, 0]])


def vector_tex(values):
    sx, sy, bx, by = values
    z = VARIABLES[2]
    return matrix_tex(sp.Matrix([sx*z + bx, sy*z + by, z])) + r',\,z\in (-\infty ,\infty )'


def fingerprint(q):
    reduced = prompt_matrix(q[':question/problem']).rref()[0]
    return hashlib.sha256(str(reduced.tolist()).encode()).hexdigest()


def system_from_matrix(m):
    return system_tex([sp.latex(sum(m[i,j]*VARIABLES[j] for j in range(3)))
                       + '=' + sp.latex(m[i,3]) for i in range(3)])


def display(tex):
    return '\n\n$$\n' + tex + '\n$$\n\n'


def row_reduction(m):
    """Forward Gaussian phase, then one backward clearing phase; trace each step."""
    m = m.copy()
    forward = []
    def swap(i, j):
        m.row_swap(i, j)
        forward.append((rf'R_{{{i+1}}}\leftrightarrow R_{{{j+1}}}', m.copy()))
    def scale(i, k):
        m[i,:] = k*m[i,:]
        forward.append((rf'R_{{{i+1}}}:=\left({sp.latex(k)}\right)R_{{{i+1}}}', m.copy()))
    def add(i, j, k, trace):
        m[i,:] = m[i,:] + k*m[j,:]
        trace.append((rf'R_{{{i+1}}}:=R_{{{i+1}}}+\left({sp.latex(k)}\right)R_{{{j+1}}}', m.copy()))
    # Prefer an available unit pivot, as in q-74532 and q-74627.
    pivot = next((i for i in range(3) if m[i,0] == 1),
                 next(i for i in range(3) if m[i,0]))
    if pivot:
        swap(0, pivot)
    if m[0,0] != 1:
        scale(0, 1/m[0,0])
    for i in (1, 2):
        if m[i,0]:
            add(i, 0, -m[i,0], forward)
    if not m[1,1]:
        swap(1, 2)
    if m[1,1] != 1:
        scale(1, 1/m[1,1])
    if m[2,1]:
        add(2, 1, -m[2,1], forward)
    echelon = m.copy()
    backward = []
    if m[0,1]:
        add(0, 1, -m[0,1], backward)
    return forward, echelon, backward, m


def worked_solution(m, vector):
    forward, echelon, backward, final = row_reduction(m)
    text = 'The augmented matrix for this system is' + display('M=' + matrix_tex(m, True))
    text += 'First reduce the matrix to row echelon form, making each pivot equal to $1$.'
    for operation, state in forward:
        text += display(operation + r'\qquad M\sim ' + matrix_tex(state, True))
    text += ('In the row echelon form above, we have only two pivots (in the $1$st and $2$nd columns). '
             'To transform the matrix to reduced row echelon form, we need to create zeros above the pivots only.')
    for operation, state in backward:
        text += display(operation + r'\qquad M\sim ' + matrix_tex(state, True))
    if not backward:
        text += ' The entry above the second pivot is already zero, so this is already reduced row echelon form.'
        text += display('M\\sim ' + matrix_tex(final, True))
    if vector:
        text += 'The corresponding system is now' + display(system_from_matrix(final))
        text += ('The final equation is $0=0$, so it imposes no restriction. '
                 'The basic variables are $x$ and $y$, and the free variable is $z$. '
                 'Find $x$ and $y$ in terms of $z$. Therefore, the general solution is')
        values = [-final[0,2], -final[1,2], final[0,3], final[1,3]]
        sx, sy, bx, by = values
        text += display(system_tex(['x=' + sp.latex(sx*VARIABLES[2]+bx),
                                    'y=' + sp.latex(sy*VARIABLES[2]+by), 'z=z']))
        text += 'where $z$ is an arbitrary real number. In vector form, the solution can be written as'
        text += display(matrix_tex(sp.Matrix(VARIABLES)) + '=' + vector_tex(values))
    return normalize_prose(text)


def replay_solution(source):
    text = source[':question/worked-solution']
    if source[':question/math-academy-id'] == 'q-74627':
        text = text.replace(r'{R}_{3} & :=\frac{1}{5}{R}_{3}',
                            r'{R}_{2} & :=\frac{1}{5}{R}_{2}')
    # The role is explicit: each 3-by-4 matrix in a solution is augmented.
    text = MATRIX.sub(lambda match: matrix_tex(parse_matrix(match[0]), True)
                      if parse_matrix_if_numeric(match[0]) else match[0], text)
    return normalize_prose(text)


def parse_matrix_if_numeric(value):
    try:
        return parse_matrix(value).shape == (3, 4)
    except (ValueError, TypeError):
        return False


def make_record(source, prompt, solution, choices, correct_index, metadata):
    prompt = normalize_prose(prompt)
    solution = normalize_prose(solution)
    choices = [(typ, normalize_tex(v) if typ == ':answer.type/math' else v)
               for typ, v in choices]
    identity_content = json.dumps([prompt, choices, correct_index], separators=(',', ':'))
    identity = uuid.uuid5(uuid.UUID(GENERATOR_UUID), VERSION + identity_content)
    fid = uuid.uuid5(identity, 'field:selection')
    answers = [{':answer/id':str(uuid.uuid5(fid, typ+'|'+value)),
                ':answer/type':typ, ':answer/value':value} for typ, value in choices]
    q = {':question/id':str(identity), ':question/problem':prompt,
         ':question/worked-solution':solution, ':question/difficulty':':question.difficulty/hard',
         ':question/answer-fields':[{':answer-field/id':str(fid), ':answer-field/key':'selection',
           ':answer-field/type':':answer-field.type/radio', ':answer-field/choices':answers,
           ':answer-field/correct':[':answer/id', answers[correct_index][':answer/id']]}]}
    generation = {'generator_id':GENERATOR_UUID, 'version':VERSION,
                  'source_question':source[':question/id'], 'source_db_id':source[':db/id'],
                  'source_basis':DATA['basis'], 'dependencies':{'sympy':sp.__version__},
                  'mathematical_fingerprint':fingerprint(q), **metadata}
    return {'question':q, 'knowledge_point':{'id':KP_UUID, 'db_id':KP_ID, 'title':DATA['kp_title']}, 'generation':generation}


def sample_parameters(rng):
    # Slot of the qualifying tuple is decided before its mathematical values.
    correct_index = rng.randrange(5)
    candidates = []
    while len(candidates) < 5:
        value = [rng.choice(SLOPES), rng.choice(SLOPES),
                 rng.choice(INTERCEPTS), rng.choice(INTERCEPTS)]
        if value not in candidates:
            candidates.append(value)
    return {'candidates':candidates, 'correct_index':correct_index,
            'row_order':[0,1,2], 'row_signs':[1,1,1]}


@checked_math_content
def generate(difficulty='hard', seed=0, template=None, parameters=None, replay=False):
    if difficulty != 'hard':
        raise ValueError('Only hard is source-supported')
    rng = random.Random(seed)
    profile = template or rng.choice(PROFILES)
    source = SOURCES[profile]
    if replay:
        field = source[':question/answer-fields'][0]
        choices = [(a[':answer/type'][':db/ident'], a[':answer/value']) for a in field[':answer-field/choices']]
        index = next(i for i,a in enumerate(field[':answer-field/choices'])
                     if a[':answer/id'] == field[':answer-field/correct'][':answer/id'])
        return make_record(source, source[':question/problem'], replay_solution(source), choices, index,
                           {'seed':seed, 'template':profile, 'profile':profile, 'replay':True,
                            'parameters':{'original_parameters':True}})
    p = parameters if parameters is not None else sample_parameters(rng)
    candidates = p['candidates']
    index = p['correct_index']
    if type(index) != int or not 0 <= index < 5 or len(candidates) != 5:
        raise ValueError('Expected five candidates and one correct slot')
    if len({tuple(c) for c in candidates}) != 5:
        raise ValueError('Candidate tuples must be distinct')
    for c in candidates:
        if (len(c) != 4 or any(type(v) != int for v in c)
            or any(v not in SLOPES for v in c[:2]) or any(v not in INTERCEPTS for v in c[2:])):
            raise ValueError('Outside declared affine domain')
    order = p.get('row_order', [0,1,2]); signs = p.get('row_signs', [1,1,1])
    if sorted(order) != [0,1,2] or len(signs) != 3 or any(s not in (-1,1) for s in signs):
        raise ValueError('Invalid equation presentation')
    b = prompt_matrix(source[':question/problem'])[:,:2]
    reduced = affine_matrix(candidates[index])
    m = b * reduced[:2,:]
    m = sp.Matrix([list(signs[i]*m[order[i],:]) for i in range(3)])
    vector = 'and then solve' in source[':question/problem']
    command = ('Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system '
               'to reduced row echelon form' + (', and then solve the linear system.' if vector else '.'))
    prompt = 'Consider the following system of linear equations:' + display(system_from_matrix(m)) + command
    choices = [(':answer.type/math', vector_tex(c) if vector else matrix_tex(affine_matrix(c))) for c in candidates]
    return make_record(source, prompt, worked_solution(m, vector), choices, index,
                       {'seed':seed, 'template':profile, 'profile':'authored-exchangeable-affine-bank',
                        'response_template':'vector' if vector else 'matrix', 'replay':False,
                        'parameters':p, 'domain':{'slopes':list(SLOPES), 'intercepts':list(INTERCEPTS)},
                        'rejection':'duplicate candidate tuples only; no correctness or sign-based rejection'})


def batch(difficulty, count, seed=0):
    if difficulty != 'hard':
        raise ValueError('Only hard is source-supported')
    if count < 0 or count > 7*7*9*9:
        raise ValueError('Count outside finite semantic domain')
    rng = random.Random(seed)
    result = []; seen = set()
    while len(result) < count:
        record = generate(difficulty, rng.getrandbits(64))
        fp = record['generation']['mathematical_fingerprint']
        if fp not in seen:
            result.append(record); seen.add(fp)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--difficulty', default='hard')
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=('json',), default='json')
    args = parser.parse_args()
    print(json.dumps(batch(args.difficulty, args.count, args.seed), indent=2))
