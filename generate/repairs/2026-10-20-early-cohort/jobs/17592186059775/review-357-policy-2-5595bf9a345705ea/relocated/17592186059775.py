"""Seeded Gaussian elimination; exact source replay and authored decision banks.

Normal samples choose a decisive second-row constant before constructing the
input. All five alternatives are internally consistent normalized REF objects.
Legacy source banks remain available through source_replay for fidelity audits.
"""
import argparse
import hashlib
import json
import math
import random
import re
import uuid
from pathlib import Path
import sympy as sp
from math_format import matrix_tex, system_tex, normalize_prose, normalize_tex, checked_math_content

KP_ID = 17592186059775
KP_UUID = 'a10cafc6-9da7-5ffc-a0c7-686a7638fbd9'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'gaussian-elimination-generator-v1'))
VERSION = '1.1.1'
SUPPORTED_LEVELS = ('easy', 'moderate')
EXCLUDED_PROFILES = ('q-10512',)
HERE = Path(__file__).with_suffix('')
SOURCE = json.loads((HERE / 'source.json').read_text())
SOURCE_BASIS = 5461
KNOWN_SYSTEMS = set(json.loads(Path(__file__).with_name('known-systems.json').read_text())['fingerprints'])
CASES = {q[':question/math-academy-id']: q for q in SOURCE[':knowledge-point/questions']
         if q.get(':question/difficulty') and q.get(':question/worked-solution')
         and q[':question/answer-fields'][0].get(':answer-field/correct')}
DEFAULTS = {sid: [sid, 1] for sid in CASES}
NUMBER = r'-?(?:\\frac\{-?\d+\}\{\d+\}|\d+)'
MAT = re.compile(r'(?:\\left\[\\begin\{array\}\{cc\|c\}|\\begin\{bmatrix\})(.*?)(?:\\end\{array\}\\right\]|\\end\{bmatrix\})', re.S)

def scalar(text):
    text = re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}', r'(\1/\2)', text.strip())
    return sp.Rational(sp.sympify(text))

def tex(value):
    value = sp.Rational(value)
    return str(value) if value.q == 1 else ('-' if value < 0 else '') + r'\frac{' + str(abs(value.p)) + '}{' + str(value.q) + '}'

def clean_answer(text):
    # Captured answers double-escape TeX; new answers use delimiter-free math
    # values and ordinary TeX command escapes. Source records remain untouched.
    return text.replace('\\\\', '\\') if r'\\begin' in text else text

def matrices(text):
    if r'\\begin' in text:
        text = clean_answer(text)
    return [sp.Matrix([[scalar(c) for c in row.split('&')] for row in m.split(r'\\')]) for m in MAT.findall(text)]

def scale_matrices(text, k):
    def change(match):
        rows = match[1].split(r'\\')
        result = []
        for row in rows:
            cells = row.split('&')
            assert len(cells) == 3
            cells[2] = ' ' + tex(k * scalar(cells[2]))
            result.append('&'.join(cells))
        return r'\left[\begin{array}{cc|c}' + r' \\ '.join(result) + r'\end{array}\right]'
    return MAT.sub(change, text)

def level(sid):
    return CASES[sid][':question/difficulty'][':db/ident'].split('/')[-1]

def domain(sid):
    q = CASES[sid]
    text = q[':question/problem'] + q[':question/worked-solution'] + ''.join(clean_answer(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices'])
    denominators = [int(n) for n in re.findall(r'\\frac\{-?\d+\}\{(\d+)\}', text)]
    denominator = math.lcm(*denominators) if denominators else 1
    return [[sid, k] for k in range(1, 6) if math.gcd(k, denominator) == 1]

def solution(sid, k):
    old = CASES[sid][':question/worked-solution']
    if k == 1:
        return old
    text = scale_matrices(old, k)
    if 'back substitution' not in text:
        return text
    # The matrix algorithm prefix and its row operations retain their source
    # wording. Parameterize the same system and back-substitution stages below.
    end = text.index('$$', text.index('$$') + 2) + 2
    prefix, tail = text[:end], text[end:]
    ref = matrices(text)[-1]
    b, c, y = ref[0, 1], ref[0, 2], ref[1, 2]
    x = c - b*y
    tail = re.sub(r'(&=)(' + NUMBER + ')', lambda m: m[1] + tex(k*scalar(m[2])), tail)
    tail = re.sub(r'([xy]=)(' + NUMBER + ')', lambda m: m[1] + tex(k*scalar(m[2])), tail)
    coefficient = ('+' if b > 0 else '-') + ('' if abs(b) == 1 else tex(abs(b)))
    contribution = -b*y
    addition = ('+' if contribution >= 0 else '-') + tex(abs(contribution))
    body = 'x' + coefficient + '(' + tex(y) + ')=' + tex(c) + r'\,⇒\,x=' + tex(c) + addition + '=' + tex(x) + '.'
    blocks = list(re.finditer(r'\$\$\n(.*?)\n\$\$', tail, re.S))
    assert len(blocks) == 2
    last = blocks[-1]
    tail = tail[:last.start(1)] + body + tail[last.end(1):]
    return prefix + tail

def choice(text, k):
    text = clean_answer(text)
    text = scale_matrices(text, k)
    return re.sub(r'([xy]\s*=\s*)(' + NUMBER + ')', lambda m: m[1] + tex(k*scalar(m[2])), text)

def fingerprint(q):
    ms = matrices(q[':question/problem'])
    if not ms:
        return hashlib.sha256(q[':question/problem'].encode()).hexdigest()
    m = ms[0]
    # Row rescaling/permutation and answer-bank changes do not add novelty.
    rows = []
    for i in range(2):
        row = list(m[i, :]); pivot = next(z for z in row if z)
        rows.append(tuple(str(z/pivot) for z in row))
    response = 'ref-and-solution' if 'and then solve' in q[':question/problem'] else 'ref-only'
    return hashlib.sha256(json.dumps([response, sorted(rows)]).encode()).hexdigest()

def _render(difficulty='easy', seed=0, template=None, parameters=None):
    if difficulty not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty: ' + difficulty)
    rng = random.Random(seed)
    if parameters is None:
        template = template or rng.choice([sid for sid in CASES if sid not in EXCLUDED_PROFILES and level(sid) == difficulty])
        parameters = rng.choice(domain(template))
    sid, k = parameters
    if sid not in CASES or level(sid) != difficulty or template not in (None, sid) or parameters not in domain(sid):
        raise ValueError('Parameters outside validated source profile domain')
    old = CASES[sid]; f = old[':question/answer-fields'][0]
    problem = old[':question/problem'] if k == 1 else scale_matrices(old[':question/problem'], k)
    values = [a[':answer/value'] if k == 1 else choice(a[':answer/value'], k) for a in f[':answer-field/choices']]
    correct = f[':answer-field/correct'][':answer/value'] if k == 1 else choice(f[':answer-field/correct'][':answer/value'], k)
    qid = str(uuid.uuid5(uuid.UUID(GENERATOR_UUID), json.dumps([sid, k, values])))
    fid = str(uuid.uuid5(uuid.UUID(qid), 'selection'))
    answers = [{':answer/id': str(uuid.uuid5(uuid.UUID(fid), value)), ':answer/type': a[':answer/type'][':db/ident'], ':answer/value': value} for a, value in zip(f[':answer-field/choices'], values)]
    field = {':answer-field/id': fid, ':answer-field/key': 'selection', ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': answers, ':answer-field/correct': [':answer/id', next(a[':answer/id'] for a in answers if a[':answer/value'] == correct)]}
    q = {':question/id': qid, ':question/problem': problem, ':question/worked-solution': solution(sid, k), ':question/difficulty': ':question.difficulty/' + difficulty, ':question/answer-fields': [field]}
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': SOURCE[':knowledge-point/title']}, 'question': q, 'generation': {'generator_id': GENERATOR_UUID, 'generator_version': VERSION, 'seed': seed, 'parameters': parameters, 'template': sid, 'bank_profile': sid, 'source_question_id': old[':question/id'], 'source_basis': SOURCE_BASIS, 'dependencies': {'sympy': sp.__version__}, 'assets': [], 'mathematical_fingerprint': fingerprint(q)}}

def source_replay(sid):
    """Audit-only reconstruction of the complete captured bank, including errors."""
    return _render(level(sid), template=sid, parameters=DEFAULTS[sid])


def replace_rhs(text, point):
    """Transport each printed matrix using its own coefficient block."""
    def change(match):
        rows = [[scalar(c) for c in row.split('&')]
                for row in match[1].split(r'\\')]
        for row in rows:
            row[2] = row[0]*point[0] + row[1]*point[1]
        return matrix_tex([[tex(c) for c in row] for row in rows], augmented=True)
    return MAT.sub(change, text)


def solve_tail(ref):
    b, c, y = ref[0, 1], ref[0, 2], ref[1, 2]
    x = c-b*y
    coefficient = ('+' if b >= 0 else '-') + ('' if abs(b) == 1 else tex(abs(b)))
    lhs = 'x' + coefficient + 'y'
    system = system_tex([lhs+'='+tex(c), 'y='+tex(y)])
    contribution = -b*y
    addition = ('+' if contribution >= 0 else '-') + tex(abs(contribution))
    body = ('x'+coefficient+r'\left('+tex(y)+r'\right)='+tex(c)
            +r'\,\Rightarrow\,x='+tex(c)+addition+'='+tex(x)+'.')
    return ('\n\nThe system is now\n\n$$\n'+system+'\n$$\n\n'
            'and we can apply back substitution. The final equation $y='+tex(y)
            +'$ tells us the value of $y.$ Substituting this value into the first equation, we get\n\n'
            '$$\n'+body+'\n$$\n\nTherefore, the solution is $x='+tex(x)+'$ and $y='+tex(y)+'.$')


@checked_math_content
def decision_instance(difficulty, seed, sid, k, target):
    if (difficulty not in SUPPORTED_LEVELS or sid not in CASES
            or level(sid) != difficulty or [sid, k] not in domain(sid)
            or type(target) is not int or target not in range(5)):
        raise ValueError('Parameters outside the supported decision profile')
    old = CASES[sid]
    final = matrices(old[':question/worked-solution'])[-1]
    b, c, base_y = final[0, 1], k*final[0, 2], final[1, 2]
    ys = [k*(base_y+d) for d in range(-2, 3)]
    point = (c-b*ys[target], ys[target])
    problem = normalize_prose(replace_rhs(old[':question/problem'], point))
    solution_text = replace_rhs(old[':question/worked-solution'], point)
    solve = 'and then solve' in problem
    if solve:
        prefix = solution_text.split('The system is now', 1)[0].rstrip()
        ref = sp.Matrix([[1, b, c], [0, 1, ys[target]]])
        solution_text = prefix + solve_tail(ref)
    solution_text = normalize_prose(solution_text)
    values = []
    for y in ys:
        mat = matrix_tex([['1', tex(b), tex(c)], ['0', '1', tex(y)]], augmented=True)
        if solve:
            value = '$$\nM∼'+mat+',\n$$\n$\\,x='+tex(c-b*y)+'$ and $y='+tex(y)+'$'
            values.append(normalize_prose(value))
        else:
            values.append(normalize_tex('M∼'+mat))
    correct = values[target]
    # Content identities include the entire bank; seed and order are incidental.
    qid = str(uuid.uuid5(uuid.UUID(GENERATOR_UUID), json.dumps([problem, values, correct])))
    fid = str(uuid.uuid5(uuid.UUID(qid), 'selection'))
    answers = [{':answer/id': str(uuid.uuid5(uuid.UUID(fid), value)),
                ':answer/type': ':answer.type/text' if solve else ':answer.type/math',
                ':answer/value': value} for value in values]
    correct_id = answers[target][':answer/id']
    random.Random(str(seed)+':'+sid+':'+str(k)).shuffle(answers)
    field = {':answer-field/id': fid, ':answer-field/key': 'selection',
             ':answer-field/type': ':answer-field.type/radio',
             ':answer-field/choices': answers,
             ':answer-field/correct': [':answer/id', correct_id]}
    q = {':question/id': qid, ':question/problem': problem,
         ':question/worked-solution': solution_text,
         ':question/difficulty': ':question.difficulty/'+difficulty,
         ':question/answer-fields': [field]}
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': SOURCE[':knowledge-point/title']},
            'question': q,
            'generation': {'generator_id': GENERATOR_UUID, 'generator_version': VERSION,
                           'seed': seed, 'parameters': [sid, k, target], 'template': sid,
                           'bank_profile': 'common-coefficient-candidates-v1',
                           'source_question_id': old[':question/id'], 'source_basis': SOURCE_BASIS,
                           'dependencies': {'sympy': sp.__version__}, 'assets': [],
                           'mathematical_fingerprint': fingerprint(q)}}


def generate(difficulty='easy', seed=0, template=None, parameters=None):
    """Normal generation; use source_replay for captured source banks."""
    if difficulty not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty: '+difficulty)
    if parameters is not None and len(parameters) != 3:
        raise ValueError('Decision parameters require [source_profile, scale, target_rank]; use source_replay for source audits')
    rng = random.Random(seed)
    if parameters is None:
        sid = template or rng.choice([s for s in CASES if level(s) == difficulty])
        target = rng.randrange(5)
        k = rng.choice(domain(sid))[1]
    else:
        sid, k, target = parameters
        if template not in (None, sid):
            raise ValueError('Conflicting template and parameters')
    return decision_instance(difficulty, seed, sid, k, target)


def candidates(difficulty, seed=0):
    if difficulty not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty: '+difficulty)
    parameters = [[sid, k, t] for sid in CASES if level(sid) == difficulty
                  for _, k in domain(sid) for t in range(5)]
    random.Random(seed).shuffle(parameters)
    records = [generate(difficulty, seed, parameters=p) for p in parameters]
    # Revised answer banks do not make an already stored system new practice.
    return [r for r in records if fingerprint(r['question']) not in KNOWN_SYSTEMS]


def batch(difficulty, count, seed=0):
    records = candidates(difficulty, seed)
    unique = {fingerprint(r['question']): r for r in records}
    if count < 0 or count > len(unique):
        raise ValueError('Finite variant limit: '+str(len(unique)))
    # A shuffled catalog prefix can repeat scaled copies of one target role.
    # Prefer intact contrast banks: same coefficient family, scale and choices,
    # different decisive lower RHS. Inventory exclusions may fragment a bank;
    # retain those instances after the intact banks rather than dropping them.
    banks = {}
    for record in unique.values():
        sid, k, target = record['generation']['parameters']
        banks.setdefault((sid, k), []).append(record)
    rng = random.Random('contrast-banks:'+str(seed))
    families = {}
    fragments = []
    for (sid, k), bank in banks.items():
        if len(bank) == 5:
            rng.shuffle(bank)
            families.setdefault(sid, []).append(bank)
        else:
            fragments.extend(bank)
    profiles = sorted(families)
    rng.shuffle(profiles)
    for profile in profiles:
        rng.shuffle(families[profile])
    ordered = []
    while any(families.values()):
        for profile in profiles:
            if families[profile]:
                ordered.extend(families[profile].pop())
    rng.shuffle(fragments)
    ordered.extend(fragments)
    return ordered[:count]


def markdown(rec):
    q = rec['question']
    return q[':question/problem'] + '\n\n' + '\n'.join('- ' + (('$' + clean_answer(a[':answer/value']) + '$') if a[':answer/type'].endswith('/math') else clean_answer(a[':answer/value'])) for a in q[':question/answer-fields'][0][':answer-field/choices']) + '\n\n' + q[':question/worked-solution']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--difficulty', default='easy'); parser.add_argument('--seed', type=int, default=59775); parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--format', choices=['json'], default='json')
    args = parser.parse_args()
    print(json.dumps(batch(args.difficulty, args.count, args.seed), indent=2))
