#!/usr/bin/env python3
"""First-quadrant unit-circle coordinate generator. No database writes.

Seven complete observed radio banks; conservative same-method parameter slots.
Easy only: no new operations, quadrants, response shapes or difficulty inflation.
Seeds order a finite domain; coordinate swapping and bank changes are not novelty.
"""
from __future__ import annotations
import argparse, functools, hashlib, json, math, os, random, re, sys, uuid
from pathlib import Path
try:
    import sympy as sp
except ImportError:
    if __name__ == '__main__':
        runtime = Path(__file__).resolve().parents[2] / '.venv/bin/python'
        os.execv(str(runtime), [str(runtime), __file__, *sys.argv[1:]])
    raise

KP_ID = 17592186110754
KP_UUID = '87c18ea8-af12-52bd-8420-ec24ed63de65'
TITLE = 'Using the Pythagorean Theorem on the Unit Circle'
VERSION = 'first-quadrant-unit-circle-1'
HERE = Path(__file__).resolve().with_suffix('')
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
SOURCE_PARAMETERS = {
    'q-23274': dict(n=49, d=8, known='y'),
    'q-65027': dict(n=9, d=5, known='x'),
    'q-124608': dict(n=2, d=3, known='y'),
    'q-124611': dict(n=5, d=3, known='y'),
    'q-124613': dict(n=5, d=4, known='x'),
    'q-23216': dict(n=1, d=4, known='x'),
    'q-65031': dict(n=4, d=5, known='x'),
}
EQUATION_PROFILES = {'q-23274', 'q-65027', 'q-65031'}
RATIONAL_PROFILES = {'q-23274', 'q-65027', 'q-23216', 'q-65031'}

def digest(v):
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def tex(v):
    return sp.latex(sp.simplify(v))

@functools.lru_cache(None)
def sources():
    return {q[':question/math-academy-id']: q for q in json.loads((HERE / 'source.json').read_text())['record'][':knowledge-point/questions']}

def values(profile, p):
    """Whole observed banks. Opaque offsets retain their expression patterns."""
    n, d = p['n'], sp.Integer(p['d'])
    m = d*d-n
    correct = sp.sqrt(m)/d
    banks = {
        'q-23274': [correct, sp.sqrt(d-1)/d, -sp.sqrt(m+2*d)/d, -correct, sp.sqrt(m+2*d)/d],
        'q-65027': [sp.sqrt(m+2*sp.sqrt(n))/d, sp.sqrt(m)/d**2, m/d, m/d**2, correct],
        'q-124608': [-sp.sqrt(d*d+n)/d**2, correct, sp.sqrt(m-n)/d, -sp.sqrt(m-1)/d**2, sp.sqrt(d*d+n)/d],
        'q-124611': [sp.sqrt(m-1)/d, sp.sqrt(m)/d**2, correct, sp.sqrt(m-1)/d**2, sp.sqrt(n+1)/d],
        'q-124613': [sp.sqrt(m-2)/d, -sp.sqrt(n-2)/d, -sp.sqrt(m+2)/d, correct, sp.sqrt(m)/d**2],
        'q-23216': [sp.sqrt(n+1)/(d-1), m/(2*d*d), (d-sp.sqrt(n))/d, correct, d/(d+sp.sqrt(n))],
        'q-65031': [sp.sqrt(m)/d**2, m/d**2, correct, sp.sqrt(n-1)/d, m/d],
    }
    return [sp.simplify(v) for v in banks[profile]], sp.simplify(correct)

def allowed(level, profile, p, replay=False):
    if level != 'easy' or profile not in SOURCE_PARAMETERS or set(p) != {'n', 'd', 'known'}:
        return False
    n, d = p['n'], p['d']
    if type(n) is not int or type(d) is not int or p['known'] not in ('x', 'y'):
        return False
    if replay:
        if p != SOURCE_PARAMETERS[profile]:
            return False
    elif not (3 <= d <= 8 and 1 <= n <= min(12, d*d-1)):
        return False
    if not 0 < n < d*d:
        return False
    square = math.isqrt(n)**2 == n
    if square != (profile in RATIONAL_PROFILES):
        return False
    bank, correct = values(profile, p)
    if any(v.is_real is not True or v.is_finite is not True for v in bank):
        return False
    return len(set(map(str, bank))) == 5 and sum(sp.simplify(v-correct) == 0 for v in bank) == 1

def candidates(level):
    if level != 'easy':
        raise ValueError(f'Unsupported {level}: no validated within-backbone difficulty template')
    for profile in SOURCE_PARAMETERS:
        for d in range(3, 9):
            for n in range(1, min(12, d*d-1)+1):
                for known in ('x', 'y'):
                    p = dict(n=n, d=d, known=known)
                    if allowed(level, profile, p):
                        yield dict(profile=profile, **p)

def mathematical_fingerprint(p):
    # Symmetry is excluded conservatively: swapping x/y alone is not a new task.
    square = sp.Rational(p['n'], p['d']**2)
    return digest(sorted([str(square), str(1-square)]))

def parse_math(t):
    """Tiny independent parser for the printed arithmetic/radical vocabulary."""
    t = t.strip().replace(' ', '').replace('\\dfrac', '\\frac')
    while '\\sqrt{' in t or '\\frac{' in t:
        prior = t
        t = re.sub(r'\\sqrt\{([^{}]+)\}', r'sqrt(\1)', t)
        t = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'((\1)/(\2))', t)
        if t == prior:
            raise ValueError('Unparsed LaTeX: '+t)
    t = re.sub(r'(\d|\))sqrt\(', r'\1*sqrt(', t)
    return sp.simplify(sp.sympify(t))

def fingerprint(q):
    prompt = q[':question/problem']
    match = re.search(r'The \$(x|y)\$-coordinate of \$A\$ is \$(.+?)\$', prompt)
    if not match:
        raise ValueError('Unrecognized existing unit-circle prompt')
    given = parse_math(match[2].rstrip('.'))
    square = sp.simplify(given**2)
    if not (square.is_Rational and 0 < square < 1):
        raise ValueError('Unrecognized source coordinate')
    return digest(sorted([str(square), str(1-square)]))

def render_solution(profile, p):
    known = p['known']; target = 'y' if known == 'x' else 'x'
    n, d = p['n'], sp.Integer(p['d'])
    given, square, missing, answer = [tex(v) for v in (sp.sqrt(n)/d, sp.Rational(n,d*d), sp.Rational(d*d-n,d*d), sp.sqrt(d*d-n)/d)]
    substituted = f'{{({given})}}^{{2}}'
    row2 = f'{substituted}+{{y}}^{{2}}' if known == 'x' else f'{{x}}^{{2}}+{substituted}'
    row3 = f'{square}+{{y}}^{{2}}' if known == 'x' else f'{{x}}^{{2}}+({square})'
    return ('Since the point $A$ lies on the unit circle, it must satisfy the Pythagorean theorem: \n\n$$\n{x}^{2}+{y}^{2}=1\n$$\n\n'
        f'Substituting ${known}={given}$ into the above and solving for ${target}$ gives\n\n$$\n'
        f'\\begin{{aligned}}{{x}}^{{2}}+{{y}}^{{2}} & =1 \\\\ {row2} & =1 \\\\ {row3} & =1 \\\\ '
        f'{{{target}}}^{{2}} & =1-{square} \\\\ {{{target}}}^{{2}} & ={missing} \\\\ '
        f'{target} & =\\sqrt{{{missing}}} \\\\ {target} & =\\pm {answer}.\\end{{aligned}}\n$$\n\n'
        f'Since $A$ lies in the first quadrant, ${target}$ must be positive, so we select the positive answer. '
        f'Therefore, our final answer is ${target}={answer}.$')

def generate(level, seed=0, template=None, parameters=None, replay=False):
    if parameters is None:
        pool = [p for p in candidates(level) if template is None or p['profile'] == template]
        if not pool:
            raise ValueError('Unsupported profile/domain')
        picked = random.Random(seed).choice(pool)
        profile = picked['profile']; p = {k:v for k,v in picked.items() if k != 'profile'}
    else:
        profile = template; p = dict(parameters)
    if not allowed(level, profile, p, replay):
        raise ValueError('Unsupported level or invalid/ambiguous bounded parameters')
    known = p['known']; target = 'y' if known == 'x' else 'x'
    given = tex(sp.sqrt(p['n'])/p['d'])
    prompt = (f'The point $A$ is located in the first quadrant and lies on the unit circle. '
              f'The ${known}$-coordinate of $A$ is ${given}.$ What is the ${target}$-coordinate of $A?$')
    if replay:
        prompt = sources()[profile][':question/problem']
    bank, correct = values(profile, p)
    content = [f'{target}={tex(v)}' if profile in EQUATION_PROFILES else tex(v) for v in bank]
    fp = mathematical_fingerprint(p)
    identity = digest([VERSION, profile, p, content])
    qid = str(uuid.uuid5(uuid.UUID(KP_UUID), identity)); fid = str(uuid.uuid5(uuid.UUID(qid), 'selection'))
    choices = [{':answer/id': str(uuid.uuid5(uuid.UUID(fid), value)), ':answer/type': ':answer.type/math', ':answer/value': value} for value in content]
    key = bank.index(correct)
    solution = render_solution(profile, p)
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': TITLE},
        'question': {':question/id': qid, ':question/problem': prompt, ':question/worked-solution': solution,
            ':question/difficulty': ':question.difficulty/easy', ':question/answer-fields': [{':answer-field/id': fid,
                ':answer-field/key': 'selection', ':answer-field/type': ':answer-field.type/radio',
                ':answer-field/correct': [':answer/id', choices[key][':answer/id']], ':answer-field/choices': choices}]},
        'generation': {'version': VERSION, 'seed': seed, 'template': 'coordinate-equation' if profile in EQUATION_PROFILES else 'coordinate-value',
            'profile': profile, 'parameters': p, 'replay': replay, 'mathematical_fingerprint': fp,
            'source_ids': [profile], 'domain': 'first quadrant; x^2+y^2=1; 0<known<1',
            'dependencies': {'sympy': sp.__version__, 'python': sys.version.split()[0]}}}

def batch(level, count, seed=0):
    if count < 0:
        raise ValueError('Negative count')
    pool = list(candidates(level)); random.Random(seed).shuffle(pool)
    result = []; seen = set()
    for entry in pool:
        profile = entry['profile']; p = {k:v for k,v in entry.items() if k != 'profile'}
        fp = mathematical_fingerprint(p)
        if fp in seen:
            continue
        if len(result) == count:
            break
        seen.add(fp); result.append(generate(level, seed, profile, p))
    if len(result) < count:
        raise ValueError(f'Finite-limit: {len(result)} distinct tasks available in declared domain; requested {count}')
    return result

def markdown(r):
    q = r['question']; f = q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', default='easy'); parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0); parser.add_argument('--format', choices=('json', 'markdown'), default='json')
    args = parser.parse_args()
    records = batch(args.difficulty, args.count, args.seed)
    print(json.dumps(records, indent=2) if args.format == 'json' else '\n\n---\n\n'.join(map(markdown, records)))
