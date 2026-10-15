#!/usr/bin/env python3
"""Moderate 3x3 Gauss–Jordan source-stage replay and RHS variants.

Only RHS entries vary: coefficient matrices and row operations stay fixed.
The homogeneous family is replay-only. See the package extraction for banks.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import os
import sys
import uuid
try:
    import sympy as sp
except ModuleNotFoundError:
    interpreter=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if not interpreter.is_file():raise
    os.execv(str(interpreter),[str(interpreter),str(Path(__file__).resolve()),*sys.argv[1:]])

HERE = Path(__file__).with_suffix('')
KP_ID = 17592186096675
KP_UUID = '95a32907-8304-5dfd-8759-9e91503445bf'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'gauss-jordan-generator-v1'))
SUPPORTED_LEVELS = ('moderate',)
VERSION = '1.0.0'
SOURCE = json.loads((HERE / 'source.json').read_text())
MATRIX = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)

def number(text):
    text = re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}', r'(\1/\2)', text.strip())
    return sp.Rational(text.strip('()')) if '/' not in text else sp.sympify(text)

def matrices(text):
    return [sp.Matrix([[number(v) for v in row.split('&')] for row in m.group(1).split(r'\\')]) for m in MATRIX.finditer(text)]

def matrix(m):
    return r'\begin{bmatrix}' + r' \\ '.join(' & '.join(sp.latex(v) for v in row) for row in m.tolist()) + r'\end{bmatrix}'

def vector(v):
    return '⟨' + ','.join(sp.latex(x) for x in v) + '⟩'

def value_vector(value):
    if MATRIX.search(value):
        m = matrices(value)[0]
        assert m[:, :3] == sp.eye(3)
        return m[:, 3]
    assert value.startswith('⟨') and value.endswith('⟩')
    return sp.Matrix([number(v) for v in value[1:-1].split(',')])

QUESTIONS = {q[':question/math-academy-id']: q for q in SOURCE[':knowledge-point/questions'] if q.get(':question/difficulty') and q.get(':question/worked-solution')}
DEFAULTS = {mid: {'solution': [str(x) for x in matrices(q[':question/worked-solution'])[-1][:, 3]]} for mid, q in QUESTIONS.items()}

def fingerprint(q):
    """Underlying augmented system, independent of answer order or response shape."""
    ms = matrices(q.get(':question/worked-solution', ''))
    if not ms:
        return hashlib.sha256(q[':question/problem'].encode()).hexdigest()
    return hashlib.sha256(str(ms[0].tolist()).encode()).hexdigest()

def generate(difficulty='moderate', seed=0, template=None, parameters=None):
    if difficulty != 'moderate':
        raise ValueError('Only source-supported Moderate is implemented; Easy/Hard are unclassified.')
    rng = random.Random(seed)
    template = template or rng.choice([k for k in QUESTIONS if k != 'q-10636'])
    q = QUESTIONS[template]
    stages = matrices(q[':question/worked-solution'])
    original = stages[-1][:, 3]
    if parameters is None:
        solution = original if template == 'q-10636' else sp.Matrix([rng.randint(-12, 12) for _ in range(3)])
    else:
        solution = sp.Matrix([sp.Rational(x) for x in parameters['solution']])
    assert solution.shape == (3, 1)
    if template == 'q-10636' and solution != original:
        raise ValueError('The homogeneous source template has one finite variant.')
    assert all(x.q == 1 and abs(x) <= 40 for x in solution)
    rendered = [m[:, :3].row_join(m[:, :3] * solution) for m in stages]
    original_field = q[':question/answer-fields'][0]
    is_matrix = bool(MATRIX.search(original_field[':answer-field/choices'][0][':answer/value']))
    bank = []
    recipes = []
    for answer in original_field[':answer-field/choices']:
        # Complete source profile, never pooled. Observed additive offsets are
        # exact affine recipes; causal error interpretations remain unresolved.
        offset = value_vector(answer[':answer/value']) - original
        v = solution + offset
        bank.append('M∼' + matrix(sp.eye(3).row_join(v)) if is_matrix else vector(v))
        recipes.append({'source_answer_id': answer[':answer/id'], 'offset': [str(x) for x in offset]})
    assert len(bank) == len(set(bank)) == 5
    correct_index = next(i for i, a in enumerate(original_field[':answer-field/choices']) if a[':answer/id'] == original_field[':answer-field/correct'][':answer/id'])
    assert value_vector(bank[correct_index]) == solution
    # Preserve all source instructional sentences and row-operation placement.
    it = iter(rendered)
    worked = MATRIX.sub(lambda _: matrix(next(it)), q[':question/worked-solution'])
    if template == 'q-10636':
        worked = worked.replace(r'{R}_{2} & :={R}_{1}+(-2){R}_{2}', r'{R}_{1} & :={R}_{1}+(-2){R}_{2}')
    if not is_matrix:
        prefix = worked.split('The corresponding system is now')[0]
        x, y, z = map(sp.latex, solution)
        worked = prefix + 'The corresponding system is now\n\n$$\n' + r'\left\{\begin{aligned}x &=' + x + r' \\ y &=' + y + r' \\ z &=' + z + r'.\end{aligned}\right.' + '\n$$\n\n' + f'So, we have the solution $x={x}$, $y={y}$, and $z={z}.$ Or, in vector form, ${vector(solution)}$.'
    x, y, z = sp.symbols('x y z')
    a = rendered[0][:, :3]
    b = rendered[0][:, 3]
    equations = [sp.latex(sum(a[i,j]*v for j,v in enumerate((x,y,z)))) + '=' + sp.latex(b[i]) for i in range(3)]
    problem = 'Consider the following system of linear equations:\n\n$$\n' + r'\left\{\begin{aligned} & ' + r' \\ & '.join(equations) + r'\end{aligned}\right.' + '\n$$\n\nUse the standard' + q[':question/problem'].split('Use the standard')[1]
    # Identity includes complete authored bank and content, never seed or order.
    key = json.dumps({'system':str(rendered[0].tolist()), 'shape':'matrix' if is_matrix else 'vector', 'profile':template, 'bank':sorted(bank)},sort_keys=True)
    qid = str(uuid.uuid5(uuid.UUID(GENERATOR_UUID), key))
    fid = str(uuid.uuid5(uuid.UUID(qid), 'selection'))
    choices = [{':answer/id':str(uuid.uuid5(uuid.UUID(fid), v)), ':answer/type':':answer.type/math', ':answer/value':v} for v in bank]
    question = {':question/id':qid, ':question/problem':problem, ':question/worked-solution':worked, ':question/difficulty':':question.difficulty/moderate', ':question/answer-fields':[{':answer-field/id':fid, ':answer-field/key':'selection', ':answer-field/type':':answer-field.type/radio', ':answer-field/choices':choices, ':answer-field/correct':[':answer/id',choices[correct_index][':answer/id']]}]}
    return {'question':question, 'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE[':knowledge-point/title']}, 'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'seed':seed,'template':template,'profile':template,'parameters':{'solution':list(map(str,solution))},'source_question_id':q[':question/id'],'source_math_academy_id':template,'sympy_version':sp.__version__,'recipes':recipes,'domains':{'sample_solution':[-12,12],'replay_solution':[-40,40]},'plot_rating':'none'}}

def batch(difficulty='moderate', count=5, seed=96675):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    if count<0:raise ValueError('count must be nonnegative')
    if count==0:return []
    records=[]; seen=set()
    for i in range(count*20):
        r=generate(difficulty,seed+i)
        fp=fingerprint(r['question'])
        if fp not in seen:
            records.append(r);seen.add(fp)
        if len(records)==count:return records
    raise ValueError('Bounded sampler could not supply distinct instances')

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',default='moderate');p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=96675);p.add_argument('--output',type=Path);p.add_argument('--format',choices=['json','markdown'],default='json');args=p.parse_args()
    result=batch(args.difficulty,args.count,args.seed)
    text=json.dumps(result,indent=2)+'\n' if args.format=='json' else '\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in result)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')
