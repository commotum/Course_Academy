#!/usr/bin/env python3
"""Seeded dimension-identification generator; no I/O except CLI JSON and replay fixture.

Adapted from supplied 17592186087713.py. Current source checkbox fields carry
matrices. Choose qualifying roles before target/foil shapes and inert entries.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import uuid
from itertools import combinations
from math_format import checked_math_content, matrix_tex, normalize_prose, validate_prose

KP_ID = 17592186087713
KP_UUID = 'ed7286fe-b6e2-5544-8bc6-86afc6cdb813'
TITLE = 'Identifying a Matrix by Its Description'
VERSION = 'matrix-description-checkbox-4'
ENTRIES = ('0','1','-1','2','-2','3','-3','4','5','7',r'\sqrt{2}',r'\sqrt{3}','-0.1','1.1')
ROLES = tuple(s for n in (1,2) for s in combinations(range(3),n))
SHAPES = tuple((r,c) for r in range(1,5) for c in range(1,5))
EASY_SHAPES = tuple((r,c) for r in range(1,4) for c in range(1,4))
LABELS = ('ABC','EFG','LMN','PQR','BCD','FGH')

def digest(v):
    return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def uid(s):
    return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:'+s))

def dimensions(a):
    return [len(a),len(a[0])]

def constraints(p):
    if set(p) != {'target','labels','matrices'}:
        raise ValueError('Exact parameter keys: target, labels, matrices')
    if len(p['target']) != 2 or any(type(n) is not int or not 1 <= n <= 4 for n in p['target']):
        raise ValueError('Target dimensions must be integers 1..4')
    if len(p['labels']) != 3 or len(set(p['labels'])) != 3 or any(not re.fullmatch('[A-Z]',l) for l in p['labels']):
        raise ValueError('Three distinct uppercase labels required')
    if len(p['matrices']) != 3:
        raise ValueError('Three matrices required')
    for a in p['matrices']:
        if not isinstance(a,list) or not 1 <= len(a) <= 4 or not all(isinstance(row,list) and 1 <= len(row) <= 4 and len(row)==len(a[0]) for row in a):
            raise ValueError('Invalid rectangular matrix')
        for row in a:
            for s in row:
                if not isinstance(s,str) or not re.fullmatch(r'-?\d+(?:\.\d+)?|\\sqrt\{[23]\}',s):
                    raise ValueError('Entry must be a supported number token')
    match = [i for i,a in enumerate(p['matrices']) if dimensions(a)==list(p['target'])]
    if len(match) not in (1,2):
        raise ValueError('Exactly one or two candidates must match')
    return match

def sample(rng, level='moderate'):
    # Decide roles first; no correctness-dependent rejection or resampling.
    matches = rng.choice(ROLES)
    domain = EASY_SHAPES if level == 'easy' else SHAPES
    target = rng.choice(domain)
    foils = [s for s in domain if s != target]
    shapes = [target if i in matches else rng.choice(foils) for i in range(3)]
    # A valid single-match case can contain TWO identical foils. This blocks
    # inferring the answer from repeated dimensions without reading the target.
    if len(matches)==1 and rng.choice((False,True)):
        wrong = [i for i in range(3) if i not in matches]
        shapes[wrong[1]] = shapes[wrong[0]]
    return {'target':list(target),'labels':list(rng.choice(LABELS)),
            'matrices':[[[rng.choice(ENTRIES) for _ in range(c)] for _ in range(r)] for r,c in shapes]}

def field_key(label,a):
    return normalize_prose('$'+label+' = '+matrix_tex(a)+'$')

def render(p):
    r,c=p['target']
    problem=f'Which of the following is a ${r}\\times {c}$ matrix?\n\nSelect all that apply.'
    matches=constraints(p)
    lines=[]
    for i,(label,a) in enumerate(zip(p['labels'],p['matrices'])):
        ar,ac=dimensions(a)
        mark=r'$\,\checkmark$' if i in matches else r'$\,\times$'
        lines.append(f'- The matrix ${label}$ has ${ar}$ '+('row' if ar==1 else 'rows')+f' and ${ac}$ '+('column' if ac==1 else 'columns')+f'. So, its dimensions are ${ar}\\times {ac}.$ '+mark)
    labels=' and '.join('$'+p['labels'][i]+'$' for i in matches)
    solution='\n\n'.join(lines)+'\n\nTherefore, only '+labels+(' is a ' if len(matches)==1 else ' are ')+f'${r}\\times {c}$ '+('matrix.' if len(matches)==1 else 'matrices.')
    return normalize_prose(problem),normalize_prose(solution)

def record(p,problem,solution,difficulty,seed,source=None,source_fields=None):
    matches=constraints(p)
    keys=[field_key(l,a) for l,a in zip(p['labels'],p['matrices'])]
    for key in keys: validate_prose(key)
    identity=digest({'version':VERSION,'prompt':problem,'solution':solution,'keys':keys,'difficulty':difficulty})
    fields=[]
    for i,key in enumerate(keys):
        fid=uid(identity+':'+key)
        values=[a[':answer/value'] for a in source_fields[i][':answer-field/choices']] if source_fields else ['false','true']
        choices=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/text',':answer/value':v} for v in values]
        value=str(i in matches).lower()
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid+':'+value)]})
    q={':question/id':uid(identity),':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields}
    if difficulty is not None:q[':question/difficulty']=':question.difficulty/'+difficulty
    task={'target':p['target'],'candidate_dimensions':sorted(dimensions(a) for a in p['matrices'])}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
            'generation':{'version':VERSION,'seed':seed,'level':difficulty,'template':'dimension_match',
                          'profile':'three-owned-boolean-banks','parameters':p,'qualifying_positions':matches,
                          'mathematical_task_fingerprint':digest(task),'source_question':source,
                          'source_basis':3970,'content_hash':identity}}

@checked_math_content
def generate(level='easy',seed=0,parameters=None):
    if level not in ('easy','moderate'):raise ValueError('Supported bands: easy, moderate')
    p=json.loads(json.dumps(parameters)) if parameters is not None else sample(random.Random(seed),level)
    constraints(p)
    if level == 'easy' and (tuple(p['target']) not in EASY_SHAPES or any(tuple(dimensions(a)) not in EASY_SHAPES for a in p['matrices'])):
        raise ValueError('Easy matrices have at most three rows and columns')
    problem,solution=render(p)
    return record(p,problem,solution,level,seed)

def source_cases():
    return json.loads(Path(__file__).with_name('source-cases.json').read_text())

def source_parameters(q):
    target=[int(v) for v in re.search(r'\$(\d+)\s*\\times\s*(\d+)\$',q[':question/problem']).groups()]
    labels=[];matrices=[]
    for f in q[':question/answer-fields']:
        key=f[':answer-field/key']
        labels.append(re.search(r'\$([A-Z])\s*=',key)[1])
        body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',key,re.S)[1]
        matrices.append([[v.strip() for v in row.split('&')] for row in body.split(r'\\')])
    return {'target':target,'labels':labels,'matrices':matrices}

@checked_math_content
def replay(source_id):
    q=next(q for q in source_cases() if q.get(':question/math-academy-id')==source_id or q[':question/id']==source_id)
    p=source_parameters(q);matches=constraints(p)
    for i,f in enumerate(q[':question/answer-fields']):
        assert f[':answer-field/correct'][':answer/value']==str(i in matches).lower()
    d=q.get(':question/difficulty');level=d[':db/ident'].split('/')[-1] if d else None
    return record(p,normalize_prose(q[':question/problem']),normalize_prose(q[':question/worked-solution']),level,None,source_id,q[':question/answer-fields'])

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=('easy','moderate'),default='easy')
    ap.add_argument('--count',type=int,default=1)
    ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=('json',),default='json')
    args=ap.parse_args()
    if args.count<1:ap.error('count must be positive')
    print(json.dumps([generate(args.difficulty,args.seed+i) for i in range(args.count)],ensure_ascii=False,indent=2))


# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':main()
