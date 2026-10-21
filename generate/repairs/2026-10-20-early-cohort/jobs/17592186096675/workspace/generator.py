#!/usr/bin/env python3
"""Relocatable, seeded moderate Gauss–Jordan practice with explicit source replay.

Retains the supplied entrypoint's source-stage/RHS construction. Normal practice
selects an eligible answer-bank role before translating the whole bank.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import uuid
import sympy as sp
from math_format import matrix_tex, system_tex, normalize_prose, normalize_tex, checked_math_content

HERE = Path(__file__).resolve().parent
KP_ID = 17592186096675
KP_UUID = '95a32907-8304-5dfd-8759-9e91503445bf'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'gauss-jordan-generator-v1'))
SUPPORTED_LEVELS = ('moderate',)
VERSION = '2.0.0'
SOURCE = json.loads((HERE / 'source.json').read_text())
MATRIX = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)

def number(text):
    text = re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}', r'(\1/\2)', text.strip())
    return sp.Rational(text.strip('()')) if '/' not in text else sp.sympify(text)

def matrices(text):
    pattern = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}|\\left\[\\begin\{array\}\{ccc\|c\}(.*?)\\end\{array\}\\right\]', re.S)
    return [sp.Matrix([[number(v) for v in row.split('&')] for row in (m[1] if m[1] is not None else m[2]).split(r'\\')]) for m in pattern.finditer(text)]

def matrix(m):
    return matrix_tex([[sp.latex(v) for v in row] for row in m.tolist()], augmented=True)

def vector(v):
    return r'\langle ' + ','.join(sp.latex(x) for x in v) + r'\rangle'

def value_vector(value):
    if r'\begin{' in value:
        m = matrices(value)[0]
        assert m[:, :3] == sp.eye(3)
        return m[:, 3]
    value = value.replace(r'\langle', '⟨').replace(r'\rangle', '⟩').strip()
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

@checked_math_content
def generate(difficulty='moderate', seed=0, template=None, parameters=None, replay=False):
    if difficulty != 'moderate':
        raise ValueError('Only source-supported Moderate is implemented; Easy/Hard are unclassified.')
    rng = random.Random(seed)
    template = template or rng.choice(list(QUESTIONS))
    q = QUESTIONS[template]
    stages = matrices(q[':question/worked-solution'])
    original_field = q[':question/answer-fields'][0]
    source_bank = [value_vector(a[':answer/value']) for a in original_field[':answer-field/choices']]
    source_correct = next(i for i, a in enumerate(original_field[':answer-field/choices']) if a[':answer/id'] == original_field[':answer-field/correct'][':answer/id'])
    parameters = parameters or {}
    if replay:
        role = source_correct
        scale = 1
        translation = sp.zeros(3, 1)
    else:
        # Decide the answer-bearing role before numerical translation.
        role = parameters.get('answer_role', rng.randrange(5))
        scale = 2 if template == 'q-10644' else 1
        translation = sp.Matrix(parameters.get('translation', [rng.randint(-3, 3) for _ in range(3)]))
    if role not in range(5) or translation.shape != (3, 1):
        raise ValueError('Invalid bank role or translation')
    if any(x.q != 1 or abs(x) > 3 for x in translation):
        raise ValueError('Translation must be three integers in [-3,3]')
    candidate_vectors = [scale*v + translation for v in source_bank]
    solution = candidate_vectors[role]
    rendered = [m[:, :3].row_join(m[:, :3] * solution) for m in stages]
    is_matrix = bool(MATRIX.search(original_field[':answer-field/choices'][0][':answer/value']))
    bank = [('M\\sim ' + matrix(sp.eye(3).row_join(v)) if is_matrix else vector(v)) for v in candidate_vectors]
    recipes = [{'source_answer_id': answer[':answer/id'], 'source_vector': list(map(str, v)), 'scale': scale, 'translation': list(map(str, translation))} for answer, v in zip(original_field[':answer-field/choices'], source_bank)]
    assert len(bank) == len(set(bank)) == 5
    correct_index = role
    assert value_vector(bank[correct_index]) == solution
    # Preserve all source instructional sentences and row-operation placement.
    it = iter(rendered)
    worked = MATRIX.sub(lambda _: matrix(next(it)), q[':question/worked-solution'])
    if template == 'q-10636':
        worked = worked.replace(r'{R}_{2} & :={R}_{1}+(-2){R}_{2}', r'{R}_{1} & :={R}_{1}+(-2){R}_{2}')
    if template == 'q-10646':
        worked = worked.replace(r'{R}_{1} & :={R}_{1}+2{R}_{3}', r'{R}_{1} & :={R}_{1}+2{R}_{2}')
    if not is_matrix and not replay:
        prefix = worked.split('The corresponding system is now')[0]
        x, y, z = map(sp.latex, solution)
        worked = prefix + 'The corresponding system is now\n\n$$\n' + r'\left\{\begin{aligned}x &=' + x + r' \\ y &=' + y + r' \\ z &=' + z + r'.\end{aligned}\right.' + '\n$$\n\n' + f'So, we have the solution $x={x}$, $y={y}$, and $z={z}.$ Or, in vector form, ${vector(solution)}$.'
    x, y, z = sp.symbols('x y z')
    a = rendered[0][:, :3]
    b = rendered[0][:, 3]
    equations = [sp.latex(sum(a[i,j]*v for j,v in enumerate((x,y,z)))) + '=' + sp.latex(b[i]) for i in range(3)]
    problem = 'Consider the following system of linear equations:\n\n$$\n' + system_tex(equations) + '\n$$\n\nUse the standard' + q[':question/problem'].split('Use the standard')[1]
    if replay:
        problem = q[':question/problem']
    problem = normalize_prose(problem)
    worked = normalize_prose(worked)
    bank = [normalize_tex(v) for v in bank]
    correct_value = bank[correct_index]
    if not replay:
        rng.shuffle(bank)
    correct_index = bank.index(correct_value)
    # Identity includes complete authored bank and content, never seed or order.
    key = json.dumps({'system':str(rendered[0].tolist()), 'shape':'matrix' if is_matrix else 'vector', 'profile':template, 'bank':sorted(bank)},sort_keys=True)
    qid = str(uuid.uuid5(uuid.UUID(GENERATOR_UUID), key))
    fid = str(uuid.uuid5(uuid.UUID(qid), 'selection'))
    choices = [{':answer/id':str(uuid.uuid5(uuid.UUID(fid), v)), ':answer/type':':answer.type/math', ':answer/value':v} for v in bank]
    question = {':question/id':qid, ':question/problem':problem, ':question/worked-solution':worked, ':question/difficulty':':question.difficulty/moderate', ':question/answer-fields':[{':answer-field/id':fid, ':answer-field/key':'selection', ':answer-field/type':':answer-field.type/radio', ':answer-field/choices':choices, ':answer-field/correct':[':answer/id',choices[correct_index][':answer/id']]}]}
    return {'question':question, 'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE[':knowledge-point/title']}, 'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'seed':seed,'template':template,'profile':template,'parameters':{'solution':list(map(str,solution)), 'answer_role':role, 'translation':list(map(str,translation)), 'scale':scale},'mode':'source-replay' if replay else 'bank-role-extension','source_question_id':q[':question/id'],'source_math_academy_id':template,'sympy_version':sp.__version__,'recipes':recipes,'domains':{'translation':[-3,3], 'answer_roles':[0,1,2,3,4]},'plot_rating':'none'}}

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
