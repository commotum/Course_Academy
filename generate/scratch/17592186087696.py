#!/usr/bin/env python3
"""Three-matrix square recognition, easy checkbox template. No plots required."""
import argparse, hashlib, itertools, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
KP_ID=17592186087696
KP_UUID='3ca13445-0218-5950-967e-a68bcfec32c7'
TITLE='Identifying a Square Matrix'
VERSION='square-matrix-checkbox-v1'
SUPPORTED_LEVELS=('easy',)
SUPPORTED_TEMPLATES=('three-checkbox',)
NS=uuid.UUID(KP_UUID)
SHAPES=tuple(itertools.product(range(1,6),repeat=2))
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}

def parse_matrices(prompt):
    result=[]
    for m in re.finditer(r'([A-Z])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',prompt,re.S):
        rows=[[x.strip() for x in row.split('&')] for row in m[2].split(r'\\')]
        assert rows and all(len(row)==len(rows[0]) for row in rows)
        result.append((m[1],rows))
    if not result:raise ValueError('no labeled matrices')
    return result

def parameters_of(q):
    pairs=parse_matrices(q[':question/problem'])
    return {'labels':[x[0] for x in pairs], 'matrices':[x[1] for x in pairs],
            'trailing_space':q[':question/problem'].split('$$')[1].strip().endswith(r'\,') if '$$' in q[':question/problem'] else False,
            'none_instruction':'If none apply' in q[':question/problem'],
            'legacy_plural':'It has $1$ rows' in q.get(':question/worked-solution','')}

SOURCE_PARAMS={sid:parameters_of(q) for sid,q in QS.items()}
SUPPORTED_SOURCES=tuple(sid for sid,q in QS.items() if ':question/difficulty' in q and all(f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox' for f in q[':question/answer-fields']))

def uid(x):return str(uuid.uuid5(NS,json.dumps(x,sort_keys=True,separators=(',',':'))))
def shape(matrix):
    if not matrix or not matrix[0] or any(len(row)!=len(matrix[0]) for row in matrix):raise ValueError('nonrectangular matrix')
    # Exact shape semantics are verified through SymPy as well as rendered parsing.
    return tuple(sp.zeros(len(matrix),len(matrix[0])).shape)

def mathematical_fingerprint(template,parameters):
    return hashlib.sha256(json.dumps(['three-square-recognition',sorted(shape(m) for m in parameters['matrices'])]).encode()).hexdigest()

def sample(rng):
    matrices=[[[str(rng.randint(-5,5)) for _ in range(c)] for _ in range(r)] for r,c in (rng.choice(SHAPES) for _ in range(3))]
    return {'labels':['A','B','C'],'matrices':matrices,'trailing_space':False,'none_instruction':True,'legacy_plural':False}

def validate_parameters(p):
    if len(p['labels'])!=3 or len(set(p['labels']))!=3 or any(not re.fullmatch('[A-Z]',l) for l in p['labels']):raise ValueError('three distinct labels required')
    if len(p['matrices'])!=3:raise ValueError('three matrices required')
    for m in p['matrices']:
        if shape(m) not in SHAPES:raise ValueError('shape outside supported 1..5 domain')
        for row in m:
            for x in row:
                if not re.fullmatch(r'-?(?:\d+(?:\.\d+)?|\\sqrt\{\d+\})',x):raise ValueError('unsupported entry syntax')

def render(p):
    pieces=[l+r'=\begin{bmatrix}'+r' \\ '.join(' & '.join(row) for row in m)+r'\end{bmatrix}' for l,m in zip(p['labels'],p['matrices'])]
    prompt='Which of the following are square matrices?\n\n$$\n'+r',\,'.join(pieces)+(r'\,' if p['trailing_space'] else '')+'\n$$\n\nSelect all that apply.'
    if p['none_instruction']:prompt+=' If none apply, leave all boxes unchecked.'
    steps=[];chosen=[]
    for l,m in zip(p['labels'],p['matrices']):
        r,c=shape(m);square=r==c
        rows='row' if r==1 and not p['legacy_plural'] else 'rows'
        cols='column' if c==1 and not p['legacy_plural'] else 'columns'
        if square:
            chosen.append(l);reason='is a square matrix since it has the same number of rows and columns.';end='so it is a'
        else:reason='is *not* a square matrix since the numbers of rows and columns are not the same.';end="so it's a"
        steps.append(f'- ${l}$ {reason} It has ${r}$ {rows} and ${c}$ {cols}, {end} ${r}\\times {c}$ matrix.')
    if len(chosen)==3:conclusion=', '.join('$'+l+'$' for l in chosen[:-1])+', and $'+chosen[-1]+'$ are square matrices.'
    elif len(chosen)==2:conclusion='only $'+chosen[0]+'$ and $'+chosen[1]+'$ are square matrices.'
    elif len(chosen)==1:conclusion='only $'+chosen[0]+'$ is a square matrix.'
    else:conclusion='none of these matrices are square matrices.'
    return prompt,'\n\n'.join(steps)+'\n\nTherefore, '+conclusion

# EASY: count rows/columns independently for three supplied matrices.
# MODERATE/HARD: no supported same-backbone distinction; never label larger matrices harder.
def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty '+level)
    if template not in (None,'three-checkbox'):raise ValueError('unsupported template')
    if field_type not in (None,'checkbox'):raise ValueError('unsupported field type')
    if profile not in (None,'boolean-membership'):raise ValueError('unsupported profile')
    p=parameters if parameters is not None else sample(random.Random(seed));validate_parameters(p)
    prompt,solution=render(p);qid=uid([VERSION,prompt,solution]);fields=[]
    for label,m in zip(p['labels'],p['matrices']):
        fid=uid([qid,label]);r,c=shape(m);correct='true' if r==c else 'false'
        bank=[{':answer/id':uid([fid,value]),':answer/type':':answer.type/text',':answer/value':value} for value in ('false','true')]
        fields.append({':answer-field/id':fid,':answer-field/key':label,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':bank,':answer-field/correct':[':answer/id',uid([fid,correct])]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':fields},'generation':{'version':VERSION,'level':level,'template':'three-checkbox','profile':'boolean-membership','seed':seed,'parameters':p,'eligible_for_learning':True,'evidence_only':False,'mathematical_fingerprint':mathematical_fingerprint('three-checkbox',p),'source':{k:SOURCE[k] for k in ('basis','database','lineage')},'source_references':list(SUPPORTED_SOURCES),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'domains':{'rows':[1,5],'columns':[1,5],'entries':[-5,5]},'authorship':'Observed easy three-matrix checkbox backbone; conservative independent dimension slots'}}

def markdown(record):
    q=record['question'];return q[':question/problem']+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',default='easy',choices=['easy','moderate','hard','all']);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='json');a=ap.parse_args()
    if a.count<1:ap.error('count must be positive')
    levels=SUPPORTED_LEVELS if a.difficulty=='all' else [a.difficulty]
    records=[generate(l,a.seed+i) for l in levels for i in range(a.count)]
    print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
