#!/usr/bin/env python3
"""Bounded, source-faithful positive-integer power integral generator."""
import argparse
import hashlib
import json
import random
import re
import sys
import uuid
import copy
import importlib.util
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
VERSION = '2.0.0-draft'
SUPPORTED_LEVELS = ('easy', 'moderate', 'hard')
DOMAIN = range(1, 81)
TEMPLATES = json.loads((HERE / 'templates.json').read_text())
X, U, C = sp.symbols('x u C', real=True)
_formatter_spec = importlib.util.spec_from_file_location('positive_power_private_math_format', HERE / 'math_format.py')
_formatter = importlib.util.module_from_spec(_formatter_spec)
_formatter_spec.loader.exec_module(_formatter)
normalize_prose = _formatter.normalize_prose
normalize_tex = _formatter.normalize_tex
checked_math_content = _formatter.checked_math_content

def builtin_int(value, name):
    if type(value) is not int:
        raise ValueError(name + ' must be a builtin int, excluding bool')

def source_record(source_id, raw=False):
    """Reference API only: preserve missing grade, key and solution on incomplete originals."""
    if type(source_id) is not str or type(raw) is not bool:
        raise ValueError('source_id must be str and raw must be bool')
    for q in SOURCE['record'][':knowledge-point/questions']:
        if source_id in (q.get(':question/math-academy-id'), str(q[':db/id'])):
            out = copy.deepcopy(q)
            if not raw:
                for key in (':question/problem', ':question/worked-solution'):
                    if key in out: out[key] = normalize_prose(out[key])
                for f in out.get(':question/answer-fields', []):
                    for a in f[':answer-field/choices']:
                        a[':answer/value'] = normalize_tex(a[':answer/value'])
                    if ':answer-field/correct' in f:
                        f[':answer-field/correct'][':answer/value'] = normalize_tex(f[':answer-field/correct'][':answer/value'])
            return out
    raise ValueError('Unknown source')

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def expression(text):
    text = text.replace(r'\\frac', r'\frac').replace(r'\displaystyle', '')
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

@checked_math_content
def generate(level, seed=0, template=None, parameters=None, profile=None):
    builtin_int(seed, 'seed')
    if type(level) is not str or (template is not None and type(template) is not str) or (profile is not None and type(profile) is not str):
        raise ValueError('level, template and profile must be strings')
    if any(value is not None and value not in TEMPLATES for value in (template, profile)):
        raise ValueError('Unknown template or bank profile')
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty')
    rng = random.Random(seed)
    profile = profile or template or rng.choice([k for k,t in TEMPLATES.items() if t['difficulty'] == level and t['evidence_role'] != 'independent_inventory'])
    if profile not in TEMPLATES or TEMPLATES[profile]['difficulty'] != level or (template and template != profile):
        raise ValueError('Ineligible source profile')
    t = TEMPLATES[profile]
    p = parameters if parameters is not None else {'b': rng.choice(list(DOMAIN))}
    if type(p) is not dict or set(p) != {'b'} or type(p['b']) is not int or p['b'] not in DOMAIN:
        raise ValueError('parameters must be exactly {b: builtin integer in 1..80}')
    problem, solution = (normalize_prose(render(t[k], t, p['b'])) for k in ('problem', 'solution'))
    values = [normalize_tex(render(a, t, p['b'])) for a in t['choices']]
    correct = t['correct_index']
    mathematical = integrand(problem)
    bank = [expression(a) for a in values]
    valid = [sp.expand(sp.diff(a, X) - mathematical) == 0 for a in bank]
    if sum(valid) != 1 or not valid[correct] or len({sp.srepr(sp.expand(sp.diff(a, X))) for a in bank}) != len(bank):
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
            'sampling_policy': 'Vary positive constant magnitude b in 1..80. Keep source slope, exponent, outer coefficient, complete bank and ordered solution fixed. Hard is explicitly authored same-method calibration.',
            'evidence_role': t['evidence_role'],
            'source_analysis': {'basis': SOURCE['basis'], 'lineage': SOURCE['lineage'], 'source_id': profile,
                'source_db_id': t['source_db_id'], 'reference': 'generate/scratch/17592186064203-draft/templates.json'},
            'plot_rating': 'none', 'assets': [], 'dependencies': {'python': sys.version.split()[0], 'sympy': sp.__version__}}}

def batch(level, count=5, seed=0):
    builtin_int(seed, 'seed')
    if type(level) is not str or level not in SUPPORTED_LEVELS or type(count) is not int or count < 0:
        raise ValueError('Unsupported level or invalid count')
    if count > capacity(level):
        raise ValueError('Requested count exceeds finite mathematical capacity')
    candidates = [(k,b) for k,t in TEMPLATES.items() if t['difficulty'] == level and t['evidence_role'] != 'independent_inventory' for b in DOMAIN]
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

def capacity(level):
    if type(level) is not str or level not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported level')
    # The five backbones have distinct polynomial degree or leading coefficient;
    # translating their nonzero linear base produces 80 distinct polynomials each.
    return {'easy': 80, 'moderate': 320, 'hard': 80}[level]

def generate_easy(seed=0, **kwargs):
    return generate('easy', seed, **kwargs)

def generate_moderate(seed=0, **kwargs):
    return generate('moderate', seed, **kwargs)

def generate_hard(seed=0, **kwargs):
    return generate('hard', seed, **kwargs)

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
    rows = [r for level in (SUPPORTED_LEVELS if a.difficulty == 'all' else (a.difficulty,)) for r in batch(level, a.count, a.seed)]
    out = (json.dumps(rows, indent=2) if a.format == 'json' else '\n\n---\n\n'.join(map(markdown, rows)))+'\n'
    if a.output:
        a.output.write_text(out)
    else:
        print(out, end='')
