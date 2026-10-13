#!/usr/bin/env python3
"""Bounded parallel-line standard-form generator; never writes to EDB.

Two incomplete, unrated sources captured at basis 1913. Local easy/moderate
labels and answer/solution additions are authored, not recovered source facts.
New prompts explicitly normalize A,B to coprime integers, A>0: independent
blank grading cannot compare two sides under a shared scale. Source replay
omits this explicitly documented prompt extension and is never submitted.
Only target y varies, t in [-8,8]; reference equations/points remain fixed.
Distinctness uses the resulting whole line (slope, intercept), not seed/UUID.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, re, sys, uuid
from pathlib import Path
try:
    import sympy as sp
except ImportError:
    runtime = Path(__file__).resolve().parents[2] / '.venv/bin/python'
    if __name__ == '__main__' and runtime.exists():
        os.execv(str(runtime), [str(runtime), __file__, *sys.argv[1:]])
    raise

KP_ID = 17592186175912
KP_UUID = '1a27c6f2-b81b-5b62-bcd0-14936842fe83'
TITLE = 'Working With Lines in Standard Form'
VERSION = 'parallel-standard-two-blank-1'
HERE = Path(__file__).resolve().with_suffix('')
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
DATA = {'q-214093': ('easy', (-2, 1), (8, 2, 1), None),
        'q-216399': ('moderate', (-2, -1), None, ((3, -1), (6, 5)))}
x, y = sp.symbols('x y', real=True)
CONVENTION = (' Use $Ax+By=C$ with integer $A,B,C$, $A>0$, and coprime $A$ and $B$ '
              '(their greatest common divisor is $1$). Enter $Ax+By$ in the first blank '
              'and $C$ in the second blank.')

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def sources():
    return {q[':question/math-academy-id']: q for q in
            json.loads((HERE / 'source.json').read_text())['record'][':knowledge-point/questions']}

def tex(value):
    return sp.latex(sp.expand(value)).replace('- ', '-')

def direction(template):
    _, _, abc, pts = DATA[template]
    return -sp.Rational(abc[0], abc[1]) if abc else sp.Rational(pts[1][1]-pts[0][1], pts[1][0]-pts[0][0])

def fingerprint(q):
    # Parse learner-visible reference data, including the canonical example.
    p = q[':question/problem']
    pairs = [tuple(map(int, pair)) for pair in re.findall(r'\((-?\d+),\s*(-?\d+)\)', p)]
    u, v = pairs[0]
    if 'line passing through the points' in p:
        (a, b), (c, d) = pairs[1:3]
        m = sp.Rational(d-b, c-a)
    else:
        match = re.search(r'parallel to \$([0-9]+)x \+ ([0-9]+)y = (-?\d+)\$', p)
        if not match:
            raise ValueError('Unrecognized mathematical task; review before committing')
        m = -sp.Rational(int(match[1]), int(match[2]))
    return digest([str(m), str(v-m*u)])

def candidates(level):
    if level not in ('easy', 'moderate'):
        raise ValueError('Unsupported level: no validated hard template')
    template = next(s for s, d in DATA.items() if d[0] == level)
    for t in range(-8, 9):
        yield template, {'t': t}

def solution(template, t):
    _, (u, v), abc, pts = DATA[template]
    v += t
    m = direction(template)
    intercept = sp.Integer(v)-m*u
    A, B = -m.p, m.q
    if A < 0:
        A, B = -A, -B
    C = A*u+B*v
    start = 'Since parallel lines have equal slopes, both lines should have the same slope.\n\n'
    if abc:
        a, b, c = abc
        start += (f'First, write the given line in slope-intercept form:\n\n$$\n'
                  f'\\begin{{aligned}}{tex(a*x+b*y)} &= {c} \\\\ '
                  f'{tex(b*y)} &= {tex(-a*x+c)} \\\\ '
                  f'y &= {tex(m*x+sp.Rational(c,b))}\\end{{aligned}}\n$$')
    else:
        (a, b), (c, d) = pts
        start += (f"First, let's find the slope of the line passing through the points $({a},{b})$ and $({c},{d})$:\n\n$$\n"
                  f'\\begin{{aligned}}m &= \\frac{{y_2-y_1}}{{x_2-x_1}} \\\\ '
                  f'&= \\frac{{{d}-({b})}}{{{c}-({a})}} \\\\ '
                  f'&= {tex(m)}\\end{{aligned}}\n$$')
    return (start + f'\n\nTherefore, we wish to find a line that has a slope of ${tex(m)}$ '
            f'and passes through the point $({u},{v})$. To find the equation of this line, we use point-slope form:\n\n$$\n'
            f'\\begin{{aligned}}y-y_1 &= m(x-x_1) \\\\ '
            f'y-({v}) &= {tex(m)}(x-({u})) \\\\ '
            f'y-({v}) &= {tex(m*(x-u))} \\\\ '
            f'y &= {tex(m*x+intercept)}\\end{{aligned}}\n$$\n\n'
            'Finally, write the equation in standard form with coprime integer coefficients and a positive $x$-coefficient.\n\n$$\n'
            f'\\begin{{aligned}}y &= {tex(m*x+intercept)} \\\\ '
            f'{tex(A*x+B*y)} &= {tex(C)}\\end{{aligned}}\n$$\n\n'
            f'The first blank is ${tex(A*x+B*y)}$ and the second blank is ${tex(C)}$.')

def generate(level, seed=0, template=None, parameters=None, replay=False):
    if level not in ('easy', 'moderate'):
        raise ValueError('Unsupported level: no validated hard template')
    template = template or next(s for s, d in DATA.items() if d[0] == level)
    p = parameters if parameters is not None else {'t': random.Random(seed).randint(-8, 8)}
    if template not in DATA or DATA[template][0] != level or set(p) != {'t'} or type(p['t']) is not int or not -8 <= p['t'] <= 8:
        raise ValueError('Outside bounded parameter/template domain')
    t = p['t']
    if replay and t != 0:
        raise ValueError('Source replay requires original parameters')
    old = sources()[template]
    u, v = DATA[template][1]
    v += t
    m = direction(template)
    A, B = -m.p, m.q
    if A < 0:
        A, B = -A, -B
    C = A*u+B*v
    prompt = old[':question/problem']
    if t:
        prompt = re.sub(r'point \$\((-?\d+),\s*(-?\d+)\)\$', f'point $({u},{v})$', prompt, count=1)
    if not replay:
        prompt = prompt.replace(' {{field-1}}', CONVENTION + '\n\n{{field-1}}')
    fp = fingerprint({':question/problem': prompt})
    qid = str(uuid.uuid5(uuid.UUID(KP_UUID), VERSION + ':' + fp))
    fields = []
    for key, value in [('field-1', tex(A*x+B*y)), ('field-2', tex(C))]:
        fid = str(uuid.uuid5(uuid.UUID(qid), key))
        aid = str(uuid.uuid5(uuid.UUID(fid), 'value:' + value))
        fields.append({':answer-field/id': fid, ':answer-field/key': key, ':answer-field/type': ':answer-field.type/blank',
                       ':answer-field/correct': [':answer/id', aid], ':answer-field/choices': [
                           {':answer/id': aid, ':answer/type': ':answer.type/math', ':answer/value': value}]})
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': TITLE},
            'question': {':question/id': qid, ':question/problem': prompt, ':question/worked-solution': solution(template, t),
                         ':question/difficulty': ':question.difficulty/' + level, ':question/answer-fields': fields},
            'generation': {'version': VERSION, 'seed': seed, 'template': template, 'parameters': dict(p),
                           'source_question': template, 'source_basis': 1913,
                           'source_lineage': '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1',
                           'mathematical_fingerprint': fp, 'bank_profile': None,
                           'domain': 'real x,y; integer vertical target translations t in [-8,8]; finite nonzero source slopes',
                           'difficulty_origin': 'authored local workload: supplied equation easy; calculate two-point slope moderate; sources unrated',
                           'answer_origin': 'mathematically derived; source has no answers',
                           'solution_origin': 'authored canonical-example move sequence: slope, point-slope expansion, standard form',
                           'prompt_extension': None if replay else 'explicit coprime A,B and positive A convention for independent blanks',
                           'replay': replay, 'dependencies': {'sympy': sp.__version__}}}

def batch(level, count, seed):
    pool = list(candidates(level))
    if type(count) is not int or not 1 <= count <= len(pool):
        raise ValueError(f'Finite capacity {len(pool)}; requested {count}')
    random.Random(seed).shuffle(pool)
    return [generate(level, seed, s, p) for s, p in pool[:count]]

def markdown(record):
    q = record['question']
    return q[':question/problem'] + '\n\n' + '\n'.join(
        f[":answer-field/key"] + ': ' + f[':answer-field/choices'][0][':answer/value']
        for f in q[':question/answer-fields']) + '\n\n' + q[':question/worked-solution']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--difficulty', required=True)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--format', choices=('json', 'markdown'), default='json')
    args = parser.parse_args()
    records = batch(args.difficulty, args.count, args.seed)
    print(json.dumps(records, indent=2) if args.format == 'json' else '\n\n'.join(map(markdown, records)))
