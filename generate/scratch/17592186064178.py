#!/usr/bin/env python3
"""Source-profile integration generator; no plots, no database operations."""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186064178-source-policy.json'))
    raise SystemExit(0)

import argparse
import hashlib
import json
import random
import re
import uuid
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError:
    # The inventory worker may invoke system Python. Use the repository's
    # existing generator environment rather than altering application setup.
    import os
    import sys
    runtime = Path(__file__).resolve().parents[2] / '.venv/bin/python'
    if not runtime.is_file() or Path(sys.executable).absolute() == runtime.absolute():
        raise
    os.execv(str(runtime), [str(runtime), str(Path(__file__).resolve()), *sys.argv[1:]])
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

KP_ID = 17592186064178
KP_UUID = '0cae5c1b-57bd-51f6-a360-db946d25532f'
TITLE = 'Integrating Sine and Cosine'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
VERSION = '1.0.0'
SUPPORTED_LEVELS = ('easy', 'moderate')
HERE = Path(__file__).with_suffix('')
TEMPLATES = json.loads((HERE / 'templates.json').read_text())
SUPPORTED_PROFILES = tuple(k for k in TEMPLATES if k != 'q-17654')
SOURCE_BASIS = 1874
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def uid(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), value))

def expression(text):
    """Parse the small frozen source notation, retaining different variables."""
    text = re.sub(r'\\operatorname\{(sin|cos|sec|csc|tan|cot)\}', r'\1', text)
    text = text.replace('⁡', '').replace(r'\theta', 'theta').replace('θ', 'theta')
    text = re.sub(r'\\(sin|cos|sec|csc|tan|cot)', r'\1', text)
    text = re.sub(r'\{(sin|cos|sec|csc|tan|cot)\}\^\{(\d+)\}', r'\1**\2', text)
    text = re.sub(r'(sin|cos|sec|csc|tan|cot)\^\{(\d+)\}', r'\1**\2', text)
    text = re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}', r'(\1/\2)', text)
    text = re.sub(r'\{(theta|x|y)\}', r'\1', text)
    text = text.replace(r'\,', '').strip().rstrip('.')
    text = re.sub(r'(sin|cos|sec|csc|tan|cot)(?:\*\*(\d+))?\s*(theta|x|y)',
                  lambda m: m[1] + '(' + m[3] + ')' + ('**' + m[2] if m[2] else ''), text)
    local = {n: sp.Symbol(n, real=True) for n in ('x', 'y', 'theta', 'C')}
    local.update({n: getattr(sp, n) for n in ('sin', 'cos', 'sec', 'csc', 'tan', 'cot')})
    return parse_expr(text, local_dict=local, transformations=standard_transformations + (implicit_multiplication_application,))

def reduced(expression):
    """Exact trig rational reduction modulo sin(v)^2+cos(v)^2=1.

    All accepted expressions are rational combinations of six trig functions
    at a fixed variable. Poles are excluded by the recorded instance domain.
    """
    substitutions, circles = {}, []
    args = sorted({f.args[0] for f in expression.atoms(sp.Function)}, key=str)
    for v in args:
        sine, cosine = sp.Symbol('_sin_' + str(v)), sp.Symbol('_cos_' + str(v))
        substitutions.update({sp.sin(v): sine, sp.cos(v): cosine,
            sp.tan(v): sine/cosine, sp.cot(v): cosine/sine,
            sp.sec(v): 1/cosine, sp.csc(v): 1/sine})
        circles.append((sine, cosine))
    numerator, _ = sp.fraction(sp.cancel(expression.xreplace(substitutions)))
    for sine, cosine in circles:
        if numerator != 0:
            numerator = sp.rem(numerator, sine**2+cosine**2-1, sine)
    return sp.expand(numerator)

def integrand(problem):
    text = re.search(r'\\int\s*(.*?)(?:\\text\{d\}|\\textrm\s*d|d[xyθ])', problem)[1]
    return expression(text)

def fingerprint_text(problem):
    e = integrand(problem)
    x = sp.Symbol('x', real=True)
    return digest(sp.srepr(sp.expand(e.subs({v: x for v in e.free_symbols}))))

def validate_parameters(profile, parameters):
    t = TEMPLATES[profile]
    if set(parameters) != set(t['parameters']):
        raise ValueError('parameter keys')
    if any(type(v) is not int or not 1 <= v <= 9 for v in parameters.values()):
        raise ValueError('positive integer magnitudes 1..9 required')
    if profile in ('q-113907', 'q-113908') and parameters['a'] < 2:
        raise ValueError('nonunit coefficient bank requires a>=2')
    if profile == 'q-113909' and parameters['a'] == parameters['b']:
        raise ValueError('equal coefficients duplicate two source bank options')
    return dict(parameters)

def render(text, p):
    values = dict(p, sum=p.get('a', 0) + p.get('b', 0))
    return re.sub(r'\{(a|b|sum)\}', lambda m: str(values[m[1]]), text)

def generate(level, seed=0, template=None, parameters=None, profile=None):
    if level not in SUPPORTED_LEVELS:
        raise ValueError('unsupported difficulty: ' + str(level))
    rng = random.Random(seed)
    profile = profile or template or rng.choice([k for k, t in TEMPLATES.items() if k in SUPPORTED_PROFILES and t['difficulty'] == level])
    if profile not in SUPPORTED_PROFILES or TEMPLATES[profile]['difficulty'] != level or (template is not None and template != profile):
        raise ValueError('ineligible source bank profile')
    t = TEMPLATES[profile]
    if parameters is None and profile == 'q-113909':
        parameters = dict(a=rng.randint(1,9), b=rng.randint(1,9))
        while parameters['a'] == parameters['b']:
            parameters['b'] = rng.randint(1,9)
    p = validate_parameters(profile, parameters if parameters is not None else
                            {k: rng.randint(2 if profile in ('q-113907', 'q-113908') else 1, 9) for k in t['parameters']})
    prompt, solution = render(t['problem'], p), render(t['solution'], p)
    values = [render(a, p) for a in t['choices']]
    correct = t['correct_index']
    variable = sp.Symbol(t['variable'], real=True)
    # Compute the canonical primitive before checking the frozen bank recipe.
    target = sp.integrate(integrand(prompt), variable)
    rhs = expression(values[correct])
    if reduced(rhs - sp.Symbol('C', real=True) - target) != 0:
        raise ValueError('source canonical recipe disagrees with computed integral')
    if reduced(sp.diff(rhs, variable) - integrand(prompt)) != 0:
        raise ValueError('incorrect canonical antiderivative')
    expressions = [expression(a) for a in values]
    for i, e in enumerate(expressions):
        if i != correct and reduced(sp.diff(e, variable) - integrand(prompt)) == 0:
            raise ValueError('ambiguous correct bank option')
        if any(reduced(sp.diff(e - prev, variable)) == 0 for prev in expressions[:i]):
            raise ValueError('equivalent bank options')
    content = digest([level, profile, prompt, solution, sorted(values), values[correct]])
    qid = uid('question:' + content)
    fid = uid(qid + ':field:selection')
    answers = [{':answer/id': uid(fid + ':answer:' + a), ':answer/type': ':answer.type/math', ':answer/value': a} for a in values]
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': TITLE},
            'question': {':question/id': qid, ':question/problem': prompt, ':question/worked-solution': solution,
                         ':question/difficulty': ':question.difficulty/' + level,
                         ':question/answer-fields': [{':answer-field/id': fid, ':answer-field/key': 'selection',
                            ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': answers,
                            ':answer-field/correct': [':answer/id', answers[correct][':answer/id']]}]},
            'generation': {'version': VERSION, 'sympy_version': sp.__version__, 'seed': seed, 'template': profile,
                'bank_profile': profile, 'parameters': p, 'parameter_fingerprint': fingerprint_text(prompt),
                'content_fingerprint': content, 'variable': t['variable'], 'domain': 'All real values of the source variable; C arbitrary.',
                'sampling_policy': 'Positive magnitudes 1..9, observed signs and fixed variables; easy coefficient profiles a>=2, moderate a!=b. Unit profiles are singleton replays. Bounds are a documented policy, not an inferred source limit.',
                'plot_rating': 'none', 'source_analysis': {'basis': SOURCE_BASIS, 'lineage': LINEAGE,
                    'source_id': profile, 'reference': 'generate/scratch/17592186064178/templates.json'}}}

def batch(level, count=5, seed=0):
    if level not in SUPPORTED_LEVELS or type(count) is not int or count < 0:
        raise ValueError('unsupported difficulty or invalid count')
    # Enumerate finite parameter capability once; seed changes only traversal.
    import itertools
    candidates = []
    for profile, t in TEMPLATES.items():
        if profile not in SUPPORTED_PROFILES or t['difficulty'] != level:
            continue
        keys = list(t['parameters'])
        bounds = range(2, 10) if profile in ('q-113907', 'q-113908') else range(1, 10)
        candidates.extend((profile, dict(zip(keys, values))) for values in itertools.product(bounds, repeat=len(keys)))
    random.Random(seed).shuffle(candidates)
    records, seen = [], set()
    for profile, p in candidates:
        if len(records) == count:
            break
        try:
            r = generate(level, seed, profile, p, profile)
        except ValueError:
            continue  # Ineligible equal-coefficient bank; never pad.
        fp = r['generation']['parameter_fingerprint']
        if fp not in seen:
            seen.add(fp)
            records.append(r)
    return records  # Bounded exhaustion remains explicit; never pad.

def generate_easy(seed=0, **kwargs):
    return generate('easy', seed, **kwargs)

def generate_moderate(seed=0, **kwargs):
    return generate('moderate', seed, **kwargs)

def markdown(r):
    q = r['question']
    f = q[':question/answer-fields'][0]
    return q[':question/problem'] + '\n\n' + '\n'.join('- $' + a[':answer/value'] + '$' for a in f[':answer-field/choices']) + '\n\n' + q[':question/worked-solution']

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--difficulty', required=True)
    ap.add_argument('--count', type=int, default=5)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--format', choices=['json', 'markdown'], default='json')
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    rows = batch(args.difficulty, args.count, args.seed)
    text = (json.dumps(rows, indent=2) if args.format == 'json' else '\n\n---\n\n'.join(map(markdown, rows))) + '\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')


from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186064178-source-policy.json'))

if __name__ == '__main__':
    main()
