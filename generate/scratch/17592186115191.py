#!/usr/bin/env python3
"""Cotangent derivative evaluation, source-anchored numeric response adaptation.

Version 1 supports only the requested hard family. It does not claim replay of
the lost source multiple-choice bank. See classification and capability.json.
Negative cotangent coefficients -1..-24 extend the observed -6; angle pi/6
and the differentiate-then-evaluate solution sequence remain fixed.
"""
import argparse
import hashlib
import json
import random
import sys
import uuid
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError:
    # The application's worker invokes system Python. Reuse the project's
    # installed pure-Python SymPy and mpmath rather than installing packages.
    for packages in (Path(__file__).resolve().parents[2]/'.venv/lib').glob('python*/site-packages'):
        sys.path.insert(0,str(packages))
    import sympy as sp

KP_ID = 17592186115191
KP_UUID = '9699341b-c4e2-547f-8d98-bcda30567272'
TITLE = 'Differentiating Expressions Involving the Cotangent Function'
VERSION = 'cotangent-evaluation-blank-v1'
PACKAGE = Path(__file__).with_suffix('')
SOURCE = json.loads((PACKAGE/'source.json').read_text())
HARD = next(q for q in SOURCE['record'][':knowledge-point/questions'] if q.get(':question/math-academy-id') == 'q-31288')
GENERATOR_ID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
DOMAIN = tuple(range(1, 25))

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',', ':')).encode()).hexdigest()

def uid(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), digest(value)))

def mathematical_key(n):
    return digest(['cotangent-derivative-evaluation', -n, 'pi/6'])

def generate(difficulty='hard', seed=0, *, n=None):
    if difficulty != 'hard':
        raise ValueError('Version 1 supports hard only; easy/moderate source families are deferred, not classified impossible')
    if n is None:
        n = random.Random(seed).choice(DOMAIN)
    if type(n) is not int or n not in DOMAIN:
        raise ValueError('n must be an integer in 1..24')
    x=sp.Symbol('x', real=True)
    answer=sp.simplify(sp.diff(-n*sp.cot(x),x).subs(x,sp.pi/6))
    assert answer == 4*n
    problem=HARD[':question/problem'].replace('-6\\operatorname{cot}', f'-{n}\\operatorname{{cot}}')+'\n\nAnswer: {{answer}}'
    solution=HARD[':question/worked-solution']
    solution=solution.replace('-6\\operatorname{cot}', f'-{n}\\operatorname{{cot}}').replace('-6(-', f'-{n}(-')
    solution=solution.replace('=6{csc}', f'={n}{{csc}}').replace('=6{(2)}', f'={n}{{(2)}}').replace('=24.', f'={answer}.')
    # Correct source roman-operator rendering and flatten redundant aligned.
    solution=solution.replace('{csc}', r'\csc').replace(r'\begin{aligned}\begin{aligned}', r'\begin{aligned}').replace(r'\end{aligned}\end{aligned}', r'\end{aligned}')
    semantic=mathematical_key(n)
    qid=uid([VERSION, semantic, 'numeric-blank'])
    fid=uid([qid, 'answer'])
    aid=uid([fid, str(answer)])
    question={':question/id':qid, ':question/problem':problem, ':question/worked-solution':solution,
              ':question/difficulty':':question.difficulty/hard', ':question/answer-fields':[
                  {':answer-field/id':fid, ':answer-field/key':'answer', ':answer-field/type':':answer-field.type/blank',
                   ':answer-field/choices':[{':answer/id':aid, ':answer/type':':answer.type/math', ':answer/value':str(answer)}],
                   ':answer-field/correct':[':answer/id',aid]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE}, 'question':question,
            'generation':{'version':VERSION,'template':'q-31288-numeric-response-adaptation','profile':'numeric-blank',
                          'seed':seed,'parameters':{'n':n,'angle':'pi/6'},'mathematical_key':semantic,
                          'source_basis':SOURCE['basis'],'source_question':'q-31288',
                          'domain':'Real x with sin(x) != 0; evaluated at pi/6',
                          'extensions':['Negative coefficient -1..-24 instead of observed -6',
                                        'Explicit numeric blank; original response bank is absent'],
                          'dependencies':{'sympy':sp.__version__}}}

def batch(difficulty,count,seed):
    if difficulty != 'hard':
        generate(difficulty,seed)
    if type(count) is not int or not 1 <= count <= len(DOMAIN):
        raise ValueError('finite-limit: this version has 24 distinct hard mathematical tasks')
    domain=list(DOMAIN);random.Random(seed).shuffle(domain)
    return [generate(difficulty,seed,n=n) for n in domain[:count]]

def markdown(record):
    q=record['question']
    return q[':question/problem']+'\n\nAnswer: $'+q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']+'$\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',default='hard');p.add_argument('--count',type=int,default=1)
    p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json')
    a=p.parse_args()
    try:
        rows=batch(a.difficulty,a.count,a.seed)
    except ValueError as e:
        p.error(str(e))
    print(json.dumps(rows,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
