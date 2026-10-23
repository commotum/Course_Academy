"""Source-bank-preserving Gaussian elimination, easy/moderate.

Bounded policy: translate the two unknowns by integer offsets h,k in -3..3.
For EVERY displayed row (a,b,c), substitute c+a*h+b*k. This changes both
right-hand sides without changing elimination coefficients or difficulty.
Source banks replay at h=k=0. Other instances use competing elimination
constants with independently sampled correct rank and internally consistent
back substitution, preventing source-bank numerical ranks from leaking keys.
"""
import argparse
import hashlib
import itertools
import json
import random
import re
import uuid
from pathlib import Path
import sympy as sp

KP_ID = 17592186059776
KP_UUID = '07abc1cc-5794-51a6-bad4-40565eae52be'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'gaussian-elimination-generator-v1'))
VERSION = '1.1.1'
SUPPORTED_LEVELS = ('easy', 'moderate')
HERE = Path(__file__).with_suffix('')
SOURCE = json.loads((HERE / 'source.json').read_text())
SOURCE_BASIS = json.loads((HERE / 'reference/initial/basis.json').read_text())['basis']
CASES = {q[':question/math-academy-id']: q for q in SOURCE[':knowledge-point/questions']}
DEFAULTS = {sid: [0, 0] for sid in CASES}
MAT = re.compile(r'\\left\[\\begin\{array\}\{cc\|c\}(.*?)\\end\{array\}\\right\]', re.S)


def rational(s):
    s = s.replace(' ', '').strip()
    m = re.fullmatch(r'(-?)\\frac\{(-?\d+)\}\{(\d+)\}', s)
    return (-1 if m[1] else 1)*sp.Rational(m[2], m[3]) if m else sp.Rational(s)


def matrices(text):
    return [sp.Matrix([[rational(c) for c in row.split('&')] for row in body.split(r'\\')]) for body in MAT.findall(text)]


def latex(x):
    return sp.latex(x).replace('- \\', '-\\')


def matrix(m):
    return r'\left[\begin{array}{cc|c}' + r' \\ '.join(' & '.join(latex(x) for x in m[i, :]) for i in range(2)) + r'\end{array}\right]'


def translate(m, h, k):
    out = m.copy()
    for i in range(2):
        out[i, 2] += m[i, 0]*h + m[i, 1]*k
    return out


def expression(a, b):
    def term(c, var):
        return ('' if c == 1 else '-' if c == -1 else latex(c)) + var
    return term(a, 'x') + ('+' if b > 0 else '') + term(b, 'y')


def system(m, ending='.'):
    return r'\left\{\begin{aligned}' + expression(m[0, 0], m[0, 1]) + ' &=' + latex(m[0, 2]) + r' \\ ' + (expression(m[1, 0], m[1, 1]) if m[1, 0] else 'y') + ' &=' + latex(m[1, 2]) + ending + r'\end{aligned}\right.'


def original_matrix(sid):
    return matrices(CASES[sid][':question/worked-solution'])[0]


def task_key(q):
    # Conservatively merge all nonsingular systems with the same solution.
    # Banks, row scaling, seed, identity and option order never add novelty.
    ms = matrices(q.get(':question/problem', ''))
    if ms:
        m = ms[0]
    else:
        ms = matrices(q.get(':question/worked-solution', ''))
        if not ms:
            return 'opaque:' + hashlib.sha256(q[':question/problem'].encode()).hexdigest()
        m = ms[0]
    return json.dumps([str(x) for x in m[:, :2].inv()*m[:, 2]])


def fingerprint(q):
    return hashlib.sha256(task_key(q).encode()).hexdigest()


def render(sid, h, k):
    old = CASES[sid]
    m = translate(original_matrix(sid), h, k)
    old_problem = old[':question/problem']
    problem = re.sub(r'\\left\\\{\\begin\{aligned\}.*?\\end\{aligned\}\\right\.', lambda _: system(m), old_problem, count=1, flags=re.S)
    # All matrix and row-operation stages retain the source order and wording.
    solution = MAT.sub(lambda match: matrix(translate(matrices(match[0])[0], h, k)), old[':question/worked-solution'])
    if 'and then solve' in problem:
        final = translate(matrices(old[':question/worked-solution'])[-1], h, k)
        x, y = m[:, :2].inv()*m[:, 2]
        b, c = final[0, 1], final[0, 2]
        first = expression(1, b) + ' &=' + latex(c)
        tail = '\n\nThe system is now \n\n$$\n' + system(final, ',') + '\n$$\n\nand we can apply back substitution. The final equation $y=' + latex(y) + '$ tells us the value of $y.$ Substituting this value into the first equation, we get\n\n$$\n'
        tail += 'x' + ('+' if b > 0 else '') + ('' if b == 1 else '-' if b == -1 else latex(b)) + '(' + latex(y) + ')=' + latex(c) + r'\,⇒\,x='
        if sid == 'q-20500':
            product = b*y
            tail += latex(c) + ('-' + latex(product) if product >= 0 else '+' + latex(-product)) + '='
        tail += latex(x) + '.\n$$\n\n' + ('Thus' if sid == 'q-73544' else 'Therefore') + ', the solution is $x=' + latex(x) + '$ and $y=' + latex(y) + '.$'
        solution = solution.split('\n\nThe system is now')[0] + tail
    values = []
    f = old[':question/answer-fields'][0]
    for a in f[':answer-field/choices']:
        value = MAT.sub(lambda match: matrix(translate(matrices(match[0])[0], h, k)), a[':answer/value'])
        if a[':answer/type'][':db/ident'] == ':answer.type/text':
            value = re.sub(r'x=([^$]+)\$ and \$y=([^$]+)', lambda match: 'x=' + latex(rational(match[1])+h) + '$ and $y=' + latex(rational(match[2])+k), value)
        values.append(value)
    return problem, solution, values


def generate(difficulty='easy', seed=0, template=None, parameters=None):
    if difficulty not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty: ' + difficulty)
    rng = random.Random(seed)
    eligible = [s for s, q in CASES.items() if q[':question/difficulty'][':db/ident'].endswith('/'+difficulty)]
    sid = template or rng.choice(eligible)
    if sid not in eligible:
        raise ValueError('Template does not support requested difficulty')
    p = list(parameters) if parameters is not None else [rng.randint(-3, 3), rng.randint(-3, 3)]
    if len(p) != 2 or any(type(x) is not int or x not in range(-3, 4) for x in p):
        raise ValueError('Offsets must be integers in -3..3')
    problem, solution, values = render(sid, *p)
    old = CASES[sid]
    f = old[':question/answer-fields'][0]
    correct_index = [a[':answer/id'] for a in f[':answer-field/choices']].index(f[':answer-field/correct'][':answer/id'])
    if p != [0, 0]:
        # Bank roles vary within each coefficient family and explicit parameter
        # path, even when a caller reuses one seed across a batch of systems.
        bank_rng = random.Random(json.dumps([seed, sid, p, 'competing-constants']))
        rank = bank_rng.randrange(5)
        final = translate(matrices(old[':question/worked-solution'])[-1], *p)
        # Preserve the solution's number form in every pair. In the fractional
        # coefficient solve profile, unit y steps would make only the correct
        # x (or a small subset) integral, leaking an unintended number-form cue.
        step = int(final[0, 1].q) if 'and then solve' in problem else 1
        candidates = []
        for i in range(5):
            candidate = final.copy()
            candidate[1, 2] += step*(i - rank)
            value = 'M∼' + matrix(candidate)
            if 'and then solve' in problem:
                y = candidate[1, 2]
                x = candidate[0, 2] - candidate[0, 1]*y
                value = '$$\n' + value + ',\n$$\n$\\,x=' + latex(x) + '$ and $y=' + latex(y) + '$'
            candidates.append((value, i == rank))
        bank_rng.shuffle(candidates)
        values = [value for value, _ in candidates]
        correct_index = next(i for i, (_, correct) in enumerate(candidates) if correct)
    if len(set(values)) != 5:
        raise ValueError('Colliding bank')
    qid = str(uuid.uuid5(uuid.UUID(GENERATOR_UUID), json.dumps([problem, values], ensure_ascii=False)))
    fid = str(uuid.uuid5(uuid.UUID(qid), 'selection'))
    answers = [{':answer/id':str(uuid.uuid5(uuid.UUID(fid), value)), ':answer/type':f[':answer-field/choices'][i][':answer/type'][':db/ident'], ':answer/value':value} for i, value in enumerate(values)]
    field = {':answer-field/id':fid, ':answer-field/key':'selection', ':answer-field/type':':answer-field.type/radio', ':answer-field/choices':answers, ':answer-field/correct':[':answer/id', answers[correct_index][':answer/id']]}
    q = {':question/id':qid, ':question/problem':problem, ':question/worked-solution':solution, ':question/difficulty':':question.difficulty/'+difficulty, ':question/answer-fields':[field]}
    return {'knowledge_point':{'db_id':KP_ID, 'id':KP_UUID, 'title':SOURCE[':knowledge-point/title']}, 'question':q, 'generation':{'generator_id':GENERATOR_UUID, 'generator_version':VERSION, 'seed':seed, 'template':sid, 'bank_profile':sid, 'parameters':p, 'source_question_id':old[':question/id'], 'source_basis':SOURCE_BASIS, 'dependencies':{'sympy':sp.__version__}, 'assets':[], 'domains':{'h':[-3,3], 'k':[-3,3], 'determinant_nonzero':True}, 'mathematical_fingerprint':fingerprint(q)}}


def domain(sid):
    return [list(p) for p in itertools.product(range(-3,4), repeat=2)]


def batch(difficulty, count, seed=0):
    if difficulty not in SUPPORTED_LEVELS or count < 0:
        raise ValueError('Unsupported difficulty or count')
    if count == 0:
        return []
    candidates = [(s,p) for s,q in CASES.items() if q[':question/difficulty'][':db/ident'].endswith('/'+difficulty) for p in domain(s)]
    random.Random(seed).shuffle(candidates)
    out, seen, groups = [], set(), {}

    def select(r):
        fp = fingerprint(r['question'])
        if fp in seen:
            return
        q = r['question']
        m = matrices(q[':question/worked-solution'])[0]
        family = (tuple(m[:, :2]), 'and then solve' in q[':question/problem'])
        prior = groups.setdefault(family, [])
        # Keep the selected mathematical task. If the first two banks in a
        # visible family share a cue, resample only its incidental bank roles.
        # Store the effective seed so ordinary generate() exactly replays it.
        for attempt in range(1000):
            field = r['question'][':question/answer-fields'][0]
            choices = field[':answer-field/choices']
            pos = next(i for i, a in enumerate(choices)
                       if a[':answer/id'] == field[':answer-field/correct'][1])
            ys = [matrices(a[':answer/value'])[0][1, 2] for a in choices]
            role = (sorted(ys).index(ys[pos]), pos)
            if len(prior) != 1 or all(a != b for a, b in zip(prior[0], role)):
                break
            meta = r['generation']
            r = generate(difficulty, seed + attempt + 1, meta['template'], meta['parameters'])
        else:
            raise ValueError('Could not construct contrasting bank roles')
        seen.add(fp)
        prior.append(role)
        out.append(r)

    for sid, p in candidates:
        # Original banks remain replayable, but are not fresh practice.
        if p == [0, 0]:
            continue
        select(generate(difficulty, seed, sid, p))
        if len(out) == count:
            return out
    raise ValueError('Finite variant limit: '+str(len(out)))


def markdown(rec):
    q = rec['question']
    return q[':question/problem'] + '\n\n' + '\n'.join('- '+(('$'+a[':answer/value']+'$') if a[':answer/type']==':answer.type/math' else a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']) + '\n\n' + q[':question/worked-solution']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--difficulty', default='easy')
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=59776)
    parser.add_argument('--format', choices=['json','markdown'], default='json')
    args = parser.parse_args()
    records = batch(args.difficulty, args.count, args.seed)
    print(json.dumps(records, indent=2) if args.format == 'json' else '\n\n'.join(markdown(r) for r in records))
