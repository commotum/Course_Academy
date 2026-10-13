#!/usr/bin/env python3
"""Bounded exact vector-magnitude generator. Local output only; see package README."""
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
    import os, sys
    runtime = Path(__file__).resolve().parents[2] / '.venv/bin/python'
    os.execv(str(runtime), [str(runtime), str(Path(__file__).resolve()), *sys.argv[1:]])

HERE = Path(__file__).with_suffix('')
SOURCE = json.loads((HERE / 'source.json').read_text())
KP_ID = 17592186059714
KP_UUID = 'a6b4ebe4-9baa-5ff0-847a-49d99ba69795'
TITLE = SOURCE['record'][':knowledge-point/title']
VERSION = 'vector-magnitude-1.0.0'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
SUPPORTED_LEVELS = ('easy',)
SCALES_BY_PROFILE = {'q-1325': tuple(range(1, 9)), 'q-18046': tuple(range(1, 4))}
ROWS = {q[':question/math-academy-id']: q for q in SOURCE['record'][':knowledge-point/questions']}
# Complete observed banks, not inferred misconception recipes. A positive scale
# multiplies the entire source bank and the source vector. Homogeneity proves
# all observed distractors stay wrong and all bank values stay distinct.
SPECS = {
    'q-1325': {'vector': (4, -1), 'variable': 'v', 'squared_bank': (25, 9, 17, 5, 7),
               'correct_index': 2, 'lexemes': ('5', '3', r'\sqrt{17}', r'\sqrt{5}', r'\sqrt{7}')},
    'q-18046': {'vector': (-12, 3), 'variable': 'a', 'squared_bank': (171, 152, 135, 153, 157),
                'correct_index': 3, 'lexemes': (r'3\sqrt{19}', r'\sqrt{152}', r'3\sqrt{15}', r'3\sqrt{17}', r'\sqrt{157}')},
}

def uid(text):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), text))

def fingerprint_squared(n):
    # Conservative: equal norms are the same exercise even if coordinates differ.
    return hashlib.sha256(('two-component-magnitude:' + str(int(n))).encode()).hexdigest()

def generate_profile(mid, scale, seed=0):
    if mid not in SPECS or scale not in SCALES_BY_PROFILE[mid]:
        raise ValueError('Outside validated template/positive-scale bounds')
    spec = SPECS[mid]
    x, y = (c * scale for c in spec['vector'])
    n = x*x + y*y
    correct = sp.sqrt(n)
    values = [sp.simplify(scale * sp.sqrt(v)) for v in spec['squared_bank']]
    assert len(set(values)) == 5 and values.count(correct) == 1
    assert values[spec['correct_index']] == correct
    original = ROWS[mid]
    problem = original[':question/problem'] if scale == 1 else re.sub(
        r'⟨[^⟩]*⟩', lambda _: f'⟨{x},{y}⟩', original[':question/problem'], count=1)
    fp = fingerprint_squared(n)
    # Bank/template participates in authored identity, never seed or option order.
    qid = uid('question:' + VERSION + ':' + fp + ':' + mid)
    fid = uid(qid + ':field:selection')
    answers = [{':answer/id': uid(fid + ':value:' + sp.srepr(v)),
                ':answer/type': ':answer.type/math',
                ':answer/value': spec['lexemes'][i] if scale == 1 else sp.latex(v)}
               for i, v in enumerate(values)]
    var = spec['variable']
    # Original radio solutions are absent. This is a supported authored completion
    # following canonical and easy-source formula/substitution/squares/radical steps.
    steps = [rf'\mid {var} \mid &= \sqrt{{{var}_{{x}}^{{2}} + {var}_{{y}}^{{2}}}}',
             rf'&= \sqrt{{({x})^{{2}} + ({y})^{{2}}}}',
             rf'&= \sqrt{{{x*x} + {y*y}}}', rf'&= \sqrt{{{n}}}']
    if correct != sp.sqrt(n, evaluate=False):
        steps.append('&= ' + sp.latex(correct))
    solution = 'Using the formula, we have\n\n$$\n\\begin{aligned}\n' + ' \\\\\n'.join(steps) + '\n\\end{aligned}\n$$'
    of = original[':question/answer-fields'][0]
    question = {':question/id': qid, ':question/problem': problem,
        ':question/worked-solution': solution, ':question/difficulty': ':question.difficulty/easy',
        ':question/requires-calculator': True,
        ':question/answer-fields': [{':answer-field/id': fid,
            ':answer-field/key': of[':answer-field/key'],
            ':answer-field/type': of[':answer-field/type'][':db/ident'],
            ':answer-field/choices': answers,
            ':answer-field/correct': [':answer/id', answers[spec['correct_index']][':answer/id']]}]}
    return {'question': question, 'knowledge_point': {'id': KP_UUID, 'title': TITLE},
        'generation': {'version': VERSION, 'generator_id': GENERATOR_UUID,
            'template': mid, 'profile': mid + '-positive-homothety',
            'recipes': ['positive scale times observed value ' + t for t in spec['lexemes']],
            'parameters': {'scale': scale, 'vector': [x, y]}, 'seed': seed,
            'parameter_fingerprint': fp, 'source_basis': SOURCE['basis'],
            'lineage': SOURCE['lineage'], 'source_references': [mid, 'e-4297', 'q-18047', 'q-18048'],
            'domain': 'two real integer components; scale in 1..8 for q-1325 or 1..3 for q-18046; nonzero vector',
            'difficulty_evidence': 'Easy two-component integer formula and radical simplification; q-18047/q-18048',
            'authored_fields': ['difficulty', 'correct designation', 'worked solution'],
            'distractor_interpretation': 'Observed value pattern only; misconception intent unresolved',
            'sympy': sp.__version__}}

def batch(level, count, seed):
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty: ' + level)
    if count < 0:
        raise ValueError('Count must be nonnegative')
    if count == 0:
        return []
    catalog = [(mid, s) for mid in SPECS for s in SCALES_BY_PROFILE[mid]]
    random.Random(seed).shuffle(catalog)
    out, used = [], set()
    for mid, s in catalog:
        r = generate_profile(mid, s, seed)
        fp = r['generation']['parameter_fingerprint']
        if fp not in used:
            out.append(r)
            used.add(fp)
        if len(out) >= count:
            break
    return out

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--difficulty', required=True)
    p.add_argument('--count', type=int, default=5)
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('--format', choices=['json', 'markdown'], default='json')
    a = p.parse_args()
    try:
        rows = batch(a.difficulty, a.count, a.seed)
    except ValueError as error:
        p.error(str(error))
    print(json.dumps(rows, indent=2) if a.format == 'json' else '\n\n'.join(
        r['question'][':question/problem'] + '\n\n' + r['question'][':question/worked-solution'] for r in rows))
