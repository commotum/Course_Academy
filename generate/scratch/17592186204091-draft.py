#!/usr/bin/env python3
"""No-solution parameter equations: direct and scaled cancellation, real domain."""
import copy
import importlib.util
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import re
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
VERSION = '2.0.0-draft'
ARTIFACTS = Path(__file__).with_suffix('')
spec = importlib.util.spec_from_file_location('kp04091_private_math_format', ARTIFACTS/'math_format.py')
math_format = importlib.util.module_from_spec(spec); spec.loader.exec_module(math_format)
SOURCE = json.loads((ARTIFACTS/'source.json').read_text())
ORIGINALS = {q[':question/math-academy-id']: q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
SUPPORTED_LEVELS = ('easy', 'moderate', 'hard')
DOMAIN = {'variables': 'xuvzw', 'parameters': 'pkmqr', 'shift': [-9, 9],
          'left_constant': [-9, 9], 'right_constant': [-10, 10],
          'easy_scale': [1], 'moderate_scale': [-9, -2, 2, 9], 'hard_scale': [-9, -2],
          'constraints': 'Nonzero shift and left constant; unequal constants; real variable; nonzero outer scale with absolute value 2..9 for scaled questions. Hard is a conservative authored rating of the same scaled method, using negative outer scales, without added steps.',
          'sampling_policy': 'Integer bounds include every complete source value; nonzero shift/left constant retain observed solution steps. Observed scales include 2,3,-7; bounded scale/constant combinations are conservative extensions. Hard has no observed rating evidence; no numerical or instructional progression is claimed.'}

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def uid(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), value))

CONSTANT_PAIRS = ((-9,10),(9,-10),(-3,5),(2,7),(8,1),(-8,1),(8,-10),(9,0))
SCALES = {'easy': (1,), 'moderate': (-7,-2,2,3), 'hard': (-9,-7,-2)}

def source_parameters(q):
    match = re.search(r'(-?\d*)\(([pkmqr])([+-]\d+)\)([xuvzw])([+-]\d+)=(-?\d+)', re.sub(r'\s+', '', q[':question/problem']))
    if not match: raise ValueError('Unreadable original equation')
    scale,k,h,x,b,c = match.groups()
    return dict(variable=x,parameter=k,scale=int(scale or 1),shift=int(h),left=int(b),right=int(c))

def numeric_tuple(p): return tuple(p[k] for k in ('scale','shift','left','right'))

def fingerprint(p):
    # Normalize the full supplied equation up to uniform nonzero scaling.
    # Names, seeds, rating and IDs are not new mathematical tasks.
    return digest(['direct' if p['scale']==1 else 'scaled', p['shift'],
                   str(sp.Rational(p['left'],p['scale'])), str(sp.Rational(p['right'],p['scale']))])

CATALOG = {level: sorted({(scale,shift,left,right) for scale in SCALES[level]
    for shift in list(range(-9,0))+list(range(1,10)) for left,right in CONSTANT_PAIRS}) for level in SUPPORTED_LEVELS}
for q in ORIGINALS.values():
    level=q.get(':question/difficulty',{}).get(':db/ident','unrated').split('/')[-1]
    if level in CATALOG and ':question/worked-solution' in q:
        t=numeric_tuple(source_parameters(q))
        if t not in CATALOG[level]: CATALOG[level].append(t)
CAPACITY = {level: len({fingerprint(dict(zip(('scale','shift','left','right'),t))) for t in tuples}) for level,tuples in CATALOG.items()}
DOMAIN.update(constant_pairs=[list(pair) for pair in CONSTANT_PAIRS],normal_scales={level:list(scales) for level,scales in SCALES.items()},
              numeric_policy='Finite cross product: 18 shifts × eight listed constant pairs × listed level scales, plus complete original MA tuples; arbitrary tuples outside this set fail closed.',
              capacity=CAPACITY)

def parameters(level, p):
    if not isinstance(p, dict): raise ValueError('Parameters must be a dictionary')
    if set(p) != {'variable', 'parameter', 'scale', 'shift', 'left', 'right'}:
        raise ValueError('Invalid parameter keys')
    if type(p['variable']) is not str or len(p['variable']) != 1 or p['variable'] not in DOMAIN['variables'] or type(p['parameter']) is not str or len(p['parameter']) != 1 or p['parameter'] not in DOMAIN['parameters']:
        raise ValueError('Invalid variable names')
    if any(type(p[k]) is not int for k in ('scale', 'shift', 'left', 'right')):
        raise ValueError('Integer parameters required')
    if not ((p['scale'] == 1 or 2 <= abs(p['scale']) <= 9) and 0 < abs(p['shift']) <= 9 and 0 < abs(p['left']) <= 9 and abs(p['right']) <= 10 and p['left'] != p['right']):
        raise ValueError('Parameter boundary or no-solution constraint violated')
    if (level == 'easy') != (p['scale'] == 1) or (level == 'hard' and p['scale'] >= 0):
        raise ValueError('Scale does not match difficulty')
    if numeric_tuple(p) not in CATALOG[level]: raise ValueError('Parameters outside finite eligible catalog')
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
    scale,shift,left,right = rng.choice(CATALOG[level])
    return dict(variable=rng.choice(DOMAIN['variables']),parameter=rng.choice(DOMAIN['parameters']),
                scale=scale,shift=shift,left=left,right=right)

@math_format.checked_math_content
def generate(level, seed=0, template=None, parameters=None, profile=None):
    if type(level) is not str or level not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty: '+str(level))
    if type(seed) is not int: raise ValueError('Seed must be an integer')
    if template is not None and type(template) is not str: raise ValueError('Template must be a string')
    if profile is not None and type(profile) is not str: raise ValueError('Profile must be a string')
    template = template if template is not None else ('direct' if level == 'easy' else 'scaled')
    if template != ('direct' if level == 'easy' else 'scaled') or profile not in (None, 'blank-integer'):
        raise ValueError('Unsupported template/profile')
    p = globals()['parameters'](level, parameters if parameters is not None else sample(random.Random(seed), level))
    root = sp.solve(sp.Symbol(p['parameter']) + p['shift'], sp.Symbol(p['parameter']))[0]
    prompt, solution = render(p)
    prompt, solution = map(math_format.normalize_prose, (prompt, solution))
    answer = math_format.normalize_tex(str(root))
    content = digest({'problem': prompt, 'solution': solution, 'answer': answer, 'difficulty': level})
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
                           'evidence_role': ('authored sparse-level same-method variation' if level == 'hard' else 'source-backed bounded variation'),
                           'source_analysis': {'basis': 2275, 'lineage': '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1',
                                               'reference': 'generate/scratch/17592186204091-draft/source-cases.json'}}}

def replay_source(source_id, parameters=None):
    '''Return the unmodified full frozen Pull record, for evidence only.'''
    if type(source_id) is not str or source_id not in ORIGINALS: raise ValueError('Unknown MA source ID')
    if parameters is not None:
        from_params = json.loads((ARTIFACTS/'source-cases.json').read_text())
        case = next(c for c in from_params if c['source_id'] == source_id)
        if digest(parameters) != digest(case['parameters']): raise ValueError('Raw replay requires original parameters')
    return copy.deepcopy(ORIGINALS[source_id])

def generate_easy(seed=0, **kwargs): return generate('easy', seed, **kwargs)
def generate_moderate(seed=0, **kwargs): return generate('moderate', seed, **kwargs)

def generate_hard(seed=0, **kwargs): return generate('hard', seed, **kwargs)

def batch(level, count=5, seed=0):
    if type(level) is not str or level not in SUPPORTED_LEVELS: raise ValueError('Unsupported difficulty')
    if type(seed) is not int: raise ValueError('Seed must be an integer')
    if type(count) is not int or not 0 <= count <= CAPACITY[level]: raise ValueError('Count exceeds finite mathematical capacity')
    rng=random.Random(seed); tuples=list(CATALOG[level]); rng.shuffle(tuples)
    rows=[];seen=set()
    for t in tuples:
        if len(rows)==count:return rows
        slots=dict(zip(('scale','shift','left','right'),t))
        key=fingerprint(slots)
        if key in seen:continue
        slots.update(variable=rng.choice(DOMAIN['variables']),parameter=rng.choice(DOMAIN['parameters']))
        rows.append(generate(level,seed,parameters=slots));seen.add(key)
    if len(rows)!=count:raise ValueError('Finite variant limit reached')
    return rows

def markdown(rec): return rec['question'][':question/problem']+'\n\n'+rec['question'][':question/worked-solution']

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--difficulty', required=True)
    parser.add_argument('--count', type=int, default=5); parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=('json', 'markdown'), default='json'); parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    levels = SUPPORTED_LEVELS if args.difficulty == 'all' else (args.difficulty,)
    rows = [record for level in levels for record in batch(level, args.count, args.seed)]
    text = (json.dumps(rows, indent=2) if args.format == 'json' else '\n\n---\n\n'.join(markdown(r) for r in rows))+'\n'
    if args.output: args.output.write_text(text)
    else: print(text, end='')

if __name__ == '__main__': main()
