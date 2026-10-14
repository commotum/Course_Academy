"""Bounded, faithful Gaussian elimination variants for this KP only.

The sole slot multiplies the augmented (right-hand-side) column by k=1..5.
Coefficient columns, pivot order, complete source banks and solution stages stay
fixed. k is coprime to observed denominators, so fractional workload is retained.
This changes both the system and its solution, unlike whole-row rescaling.
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

KP_ID = 17592186059775
KP_UUID = 'a10cafc6-9da7-5ffc-a0c7-686a7638fbd9'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'gaussian-elimination-generator-v1'))
VERSION = '1.0.0'
SUPPORTED_LEVELS = ('easy', 'moderate')
EXCLUDED_PROFILES = ('q-10512',)
HERE = Path(__file__).with_suffix('')
SOURCE = json.loads((HERE / 'source.json').read_text())
SOURCE_BASIS = json.loads((HERE / 'reference/initial/inventory.json').read_text())['basis']
CASES = {q[':question/math-academy-id']: q for q in SOURCE[':knowledge-point/questions']
         if q.get(':question/difficulty') and q.get(':question/worked-solution')
         and q[':question/answer-fields'][0].get(':answer-field/correct')}
DEFAULTS = {sid: [sid, 1] for sid in CASES}
NUMBER = r'-?(?:\\frac\{-?\d+\}\{\d+\}|\d+)'
MAT = re.compile(r'\\left\[\\begin\{array\}\{cc\|c\}(.*?)\\end\{array\}\\right\]', re.S)

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

def generate(difficulty='easy', seed=0, template=None, parameters=None):
    if template in EXCLUDED_PROFILES or parameters and parameters[0] in EXCLUDED_PROFILES:
        raise ValueError('Ambiguous source bank excluded: q-10512')
    return _render(difficulty, seed, template, parameters)

def source_replay(sid):
    """Audit-only source reconstruction, including excluded evidence."""
    return _render(level(sid), template=sid, parameters=DEFAULTS[sid])

def candidates(difficulty, seed=0):
    if difficulty not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty: ' + difficulty)
    parameters = [p for sid in CASES if sid not in EXCLUDED_PROFILES and level(sid) == difficulty for p in domain(sid)]
    random.Random(seed).shuffle(parameters)
    return [generate(difficulty, seed, parameters=p) for p in parameters]

def batch(difficulty, count, seed=0):
    records = candidates(difficulty, seed)
    unique = {fingerprint(r['question']): r for r in records}
    if count < 0 or count > len(unique):
        raise ValueError('Finite variant limit: ' + str(len(unique)))
    return list(unique.values())[:count]

def markdown(rec):
    q = rec['question']
    return q[':question/problem'] + '\n\n' + '\n'.join('- ' + (('$' + clean_answer(a[':answer/value']) + '$') if a[':answer/type'].endswith('/math') else clean_answer(a[':answer/value'])) for a in q[':question/answer-fields'][0][':answer-field/choices']) + '\n\n' + q[':question/worked-solution']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--difficulty', default='easy'); parser.add_argument('--seed', type=int, default=59775); parser.add_argument('--count', type=int, default=5)
    args = parser.parse_args()
    print(json.dumps({'instances': batch(args.difficulty, args.count, args.seed)}, indent=2))
