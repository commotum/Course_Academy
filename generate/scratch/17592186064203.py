#!/usr/bin/env python3
"""Bounded, source-faithful positive-integer power integral generator."""
import argparse
import hashlib
import json
import random
import re
import sys
import uuid
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError:
    import os
    runtime = Path(__file__).resolve().parents[2] / '.venv/bin/python'
    if not runtime.is_file() or Path(sys.executable).absolute() == runtime.absolute():
        raise
    os.execv(str(runtime), [str(runtime), str(Path(__file__).resolve()), *sys.argv[1:]])
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

HERE = Path(__file__).with_suffix('')
SOURCE = json.loads((HERE / 'source.json').read_text())
KP_ID = 17592186064203
KP_UUID = SOURCE['record'][':knowledge-point/id']
TITLE = SOURCE['record'][':knowledge-point/title']
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
VERSION = '1.0.0'
SUPPORTED_LEVELS = ('easy', 'moderate')
DOMAIN = range(1, 21)
TEMPLATES = json.loads((HERE / 'templates.json').read_text())
X, U, C = sp.symbols('x u C', real=True)

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def expression(text):
    text = text.replace(r'\,', '').strip().rstrip('.,')
    while (m := re.search(r'\\d?frac', text)) is not None:
        def group(start):
            if text[start] != '{':
                raise ValueError('Braced fraction required')
            depth = 1
            end = start + 1
            while depth:
                if end >= len(text):
                    raise ValueError('Unbalanced fraction')
                depth += (text[end] == '{') - (text[end] == '}')
                end += 1
            return text[start+1:end-1], end
        numerator, end = group(m.end())
        denominator, end = group(end)
        text = text[:m.start()]+'(('+numerator+')/('+denominator+'))'+text[end:]
    text = text.replace(r'\,', '').replace(r'\cdot', '*').replace('✓', '').strip().rstrip('*')
    text = text.replace('^', '**').replace('{', '(').replace('}', ')')
    return parse_expr(text, local_dict={'x': X, 'u': U, 'C': C},
        transformations=standard_transformations + (implicit_multiplication_application,))

def integrand(problem):
    match = re.search(r'\\int\s*(.*?)(?:\\text\{d\}|\\textrm\{d\}|d[xu])', problem)
    if not match:
        raise ValueError('Unreadable integral prompt')
    return expression(match[1])

def fingerprint_text(problem):
    return digest(sp.srepr(sp.expand(integrand(problem))))

def inner(t, b):
    return f"{t['slope']}x-{b}" if t['slope'] > 0 else f"{b}-{abs(t['slope'])}x"

def render(text, t, b):
    # Only the complete linear expression changes. Exponents, slopes, bank
    # coefficients, substitution factors, and all source prose stay fixed.
    return text.replace(t['inner'], inner(t, b))

def generate(level, seed=0, template=None, parameters=None, profile=None):
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty; hard has no complete rated source')
    rng = random.Random(seed)
    profile = profile or template or rng.choice([k for k,t in TEMPLATES.items() if t['difficulty'] == level])
    if profile not in TEMPLATES or TEMPLATES[profile]['difficulty'] != level or (template and template != profile):
        raise ValueError('Ineligible source profile')
    t = TEMPLATES[profile]
    p = parameters if parameters is not None else {'b': rng.choice(list(DOMAIN))}
    if set(p) != {'b'} or type(p['b']) is not int or p['b'] not in DOMAIN:
        raise ValueError('b must be an integer in 1..20')
    problem, solution = (render(t[k], t, p['b']) for k in ('problem', 'solution'))
    values = [render(a, t, p['b']) for a in t['choices']]
    correct = t['correct_index']
    mathematical = integrand(problem)
    bank = [expression(a) for a in values]
    valid = [sp.expand(sp.diff(a, X) - mathematical) == 0 for a in bank]
    if sum(valid) != 1 or not valid[correct] or len({sp.srepr(sp.expand(a)) for a in bank}) != len(bank):
        raise ValueError('Incorrect or ambiguous bank')
    fp = fingerprint_text(problem)
    content = digest([level, profile, problem, solution, sorted(values), values[correct]])
    qid = str(uuid.uuid5(uuid.UUID(GENERATOR_UUID), content))
    fid = str(uuid.uuid5(uuid.UUID(qid), 'selection'))
    choices = [{':answer/id': str(uuid.uuid5(uuid.UUID(fid), a)), ':answer/type': ':answer.type/math', ':answer/value': a} for a in values]
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': TITLE},
        'question': {':question/id': qid, ':question/problem': problem, ':question/worked-solution': solution,
            ':question/difficulty': ':question.difficulty/' + level,
            ':question/answer-fields': [{':answer-field/id': fid, ':answer-field/key': 'selection',
                ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': choices,
                ':answer-field/correct': [':answer/id', choices[correct][':answer/id']]}]},
        'generation': {'generator_id': GENERATOR_UUID, 'version': VERSION, 'seed': seed,
            'template': profile, 'bank_profile': profile, 'parameters': dict(p),
            'parameter_fingerprint': fp, 'content_fingerprint': content,
            'domain': 'All real x; C an arbitrary integration constant.',
            'sampling_policy': 'Narrower policy: vary only positive constant magnitude b in 1..20. Keep each source slope, exponent, outer coefficient, full bank, notation and solution sequence fixed.',
            'source_analysis': {'basis': SOURCE['basis'], 'lineage': SOURCE['lineage'], 'source_id': profile,
                'source_db_id': t['source_db_id'], 'reference': 'generate/scratch/17592186064203/templates.json'},
            'plot_rating': 'none', 'assets': [], 'dependencies': {'python': sys.version.split()[0], 'sympy': sp.__version__}}}

def batch(level, count=5, seed=0):
    if level not in SUPPORTED_LEVELS or type(count) is not int or count < 0:
        raise ValueError('Unsupported level or invalid count')
    candidates = [(k,b) for k,t in TEMPLATES.items() if t['difficulty'] == level for b in DOMAIN]
    random.Random(seed).shuffle(candidates)
    rows, seen = [], set()
    for k,b in candidates:
        if len(rows) == count:
            break
        r = generate(level, seed, k, {'b': b}, k)
        fp = r['generation']['parameter_fingerprint']
        if fp not in seen:
            rows.append(r)
            seen.add(fp)
    return rows  # Exhaustion is explicit; never pad with seeds or shuffled banks.

def generate_easy(seed=0, **kwargs):
    return generate('easy', seed, **kwargs)

def generate_moderate(seed=0, **kwargs):
    return generate('moderate', seed, **kwargs)

def markdown(r):
    q = r['question']
    return q[':question/problem'] + '\n\n' + '\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']) + '\n\n' + q[':question/worked-solution']

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--difficulty', required=True)
    ap.add_argument('--count', type=int, default=5)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--format', choices=['json', 'markdown'], default='json')
    ap.add_argument('--output', type=Path)
    a = ap.parse_args()
    rows = batch(a.difficulty, a.count, a.seed)
    out = (json.dumps(rows, indent=2) if a.format == 'json' else '\n\n---\n\n'.join(map(markdown, rows)))+'\n'
    if a.output:
        a.output.write_text(out)
    else:
        print(out, end='')
