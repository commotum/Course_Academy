#!/usr/bin/env python3
"""No-solution parameter equations: direct and scaled cancellation, real domain."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import sys
import uuid
try:
    import sympy as sp
except ModuleNotFoundError:
    interpreter = Path(__file__).resolve().parents[2] / '.venv/bin/python'
    if __name__ == '__main__' and interpreter.is_file() and Path(sys.executable).resolve() != interpreter.resolve():
        os.execv(str(interpreter), [str(interpreter), str(Path(__file__).resolve()), *sys.argv[1:]])
    raise

KP_ID = 17592186204091
KP_UUID = 'ba644b27-7245-5b7b-8cd6-2493836a7d03'
TITLE = 'Solving For an Unknown Parameter - Constants on Both Sides'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
VERSION = '1.0.0'
SUPPORTED_LEVELS = ('easy', 'moderate')
DOMAIN = {'variables': 'xuvzw', 'parameters': 'pkmqr', 'shift': [-9, 9],
          'left_constant': [-9, 9], 'right_constant': [-10, 10],
          'easy_scale': [1], 'moderate_scale': [2, 9],
          'constraints': 'Nonzero shift and left constant; unequal constants; real variable; positive nonzero scale.',
          'sampling_policy': 'Integer bounds include every complete source value; nonzero shift/left constant retain observed solution steps. Scales 4..9 and new constant combinations extend the observed 2,3 scales.'}

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def uid(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), value))

def fingerprint(p):
    # Constants, variable names and nonzero outer scale do not create a new task.
    # The scaled family separately requires division before isolating the parameter.
    return digest(['direct' if p['scale'] == 1 else 'scaled', -p['shift']])

def parameters(level, p):
    if set(p) != {'variable', 'parameter', 'scale', 'shift', 'left', 'right'}:
        raise ValueError('Invalid parameter keys')
    if p['variable'] not in DOMAIN['variables'] or len(p['variable']) != 1 or p['parameter'] not in DOMAIN['parameters'] or len(p['parameter']) != 1:
        raise ValueError('Invalid variable names')
    if any(type(p[k]) is not int for k in ('scale', 'shift', 'left', 'right')):
        raise ValueError('Integer parameters required')
    if not (1 <= p['scale'] <= 9 and 0 < abs(p['shift']) <= 9 and 0 < abs(p['left']) <= 9 and abs(p['right']) <= 10 and p['left'] != p['right']):
        raise ValueError('Parameter boundary or no-solution constraint violated')
    if (level == 'easy') != (p['scale'] == 1):
        raise ValueError('Scale does not match difficulty')
    return dict(p)

def signed(n):
    return ('+' if n >= 0 else '-') + str(abs(n))

def render(p):
    x, k, s, h, b, c = (p[v] for v in ('variable', 'parameter', 'scale', 'shift', 'left', 'right'))
    inner = k + signed(h)
    coefficient = (str(s) if s != 1 else '') + '(' + inner + ')'
    eq = coefficient + x + signed(b) + '=' + str(c)
    prompt = f'Consider the equation in the variable ${x},$ given by\n\n$$\n{eq}\n$$\n\nwhere ${k}$ is a constant. Given that this equation has no solution, what is the value of ${k}?$\n\n${k}=$\n{{{{field-1}}}}'
    solution = 'Suppose we have an equation of the form\n\n$$\nax=b\n$$\n\nwhere $a$ and $b$ are constants, and $b\\ne 0.$ If $a=0,$ then the equation has no solution.\n\n'
    solution += f"First, let's write our equation in the form $a{x}=b:$\n\n$$\n"
    lines = [coefficient+x+signed(b)+' & ='+str(c), coefficient+x+signed(b)+signed(-b)+' & ='+str(c)+signed(-b), '{{'+coefficient+'}_{⏟}}_{a}'+x+' & ={{'+str(c-b)+'}_{⏟}}_{b}']
    solution += r'\begin{aligned}' + r' \\ '.join(lines) + r'\end{aligned}' + '\n$$\n\nTherefore, the equation has no solution if\n\n$$\n'
    solution += (coefficient if s != 1 else inner) + '=0.\n$$\n\n' + f'Solving this for ${k},$ we get\n\n$$\n'
    lines = [coefficient+' & =0'] if s != 1 else []
    if s != 1:
        lines += [r'\frac{'+coefficient+'}{'+str(s)+'} & ='+r'\frac{0}{'+str(s)+'}']
    lines += [inner+' & =0', k+' & ='+str(-h)+'.']
    solution += r'\begin{aligned}' + r' \\ '.join(lines) + r'\end{aligned}' + '\n$$'
    return prompt, solution

def sample(rng, level):
    b = rng.choice([n for n in range(-9, 10) if n])
    return {'variable': rng.choice(DOMAIN['variables']), 'parameter': rng.choice(DOMAIN['parameters']),
            'scale': 1 if level == 'easy' else rng.randint(2, 9),
            'shift': rng.choice([n for n in range(-9, 10) if n]), 'left': b,
            'right': rng.choice([n for n in range(-10, 11) if n != b])}

def generate(level, seed=0, template=None, parameters=None, profile=None):
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty: '+str(level))
    template = template or ('direct' if level == 'easy' else 'scaled')
    if template != ('direct' if level == 'easy' else 'scaled') or profile not in (None, 'blank-integer'):
        raise ValueError('Unsupported template/profile')
    p = globals()['parameters'](level, parameters if parameters is not None else sample(random.Random(seed), level))
    root = sp.solve(sp.Symbol(p['parameter']) + p['shift'], sp.Symbol(p['parameter']))[0]
    prompt, solution = render(p)
    content = digest({'problem': prompt, 'solution': solution, 'answer': str(root)})
    qid = uid('question:'+content); fid = uid(qid+':field:field-1'); aid = uid(fid+':answer:'+str(root))
    field = {':answer-field/id': fid, ':answer-field/key': 'field-1', ':answer-field/type': ':answer-field.type/blank',
             ':answer-field/choices': [{':answer/id': aid, ':answer/type': ':answer.type/math', ':answer/value': str(root)}],
             ':answer-field/correct': [':answer/id', aid]}
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': TITLE},
            'question': {':question/id': qid, ':question/problem': prompt, ':question/worked-solution': solution,
                         ':question/difficulty': ':question.difficulty/'+level, ':question/answer-fields': [field]},
            'generation': {'version': VERSION, 'sympy_version': sp.__version__, 'seed': seed, 'template': template,
                           'parameters': p, 'bank_profile': 'blank-integer', 'parameter_fingerprint': fingerprint(p),
                           'content_fingerprint': content, 'domain': DOMAIN, 'plot_rating': 'none',
                           'source_analysis': {'basis': 1850, 'lineage': '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1',
                                               'reference': 'generate/scratch/17592186204091/source-cases.json'}}}

def generate_easy(seed=0, **kwargs): return generate('easy', seed, **kwargs)
def generate_moderate(seed=0, **kwargs): return generate('moderate', seed, **kwargs)

def batch(level, count=5, seed=0):
    if level not in SUPPORTED_LEVELS: raise ValueError('Unsupported difficulty: '+str(level))
    if type(count) is not int or not 0 <= count <= 18:
        raise ValueError('Finite capability: at most 18 distinct parameter roots per supported level; no duplicate padding')
    rows = []; seen = set()
    for i in range(2000):
        if len(rows) == count: return rows
        r = generate(level, seed+i); key = r['generation']['parameter_fingerprint']
        if key not in seen: rows.append(r); seen.add(key)
    raise ValueError('Finite variant limit reached')

def markdown(rec): return rec['question'][':question/problem']+'\n\n'+rec['question'][':question/worked-solution']

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--difficulty', required=True)
    parser.add_argument('--count', type=int, default=5); parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=('json', 'markdown'), default='json'); parser.add_argument('--output', type=Path)
    args = parser.parse_args(); rows = batch(args.difficulty, args.count, args.seed)
    text = (json.dumps(rows, indent=2) if args.format == 'json' else '\n\n---\n\n'.join(markdown(r) for r in rows))+'\n'
    if args.output: args.output.write_text(text)
    else: print(text, end='')

if __name__ == '__main__': main()
