"""Source-preserving matrix-power blanks; deterministic, field-owned identities."""
import argparse
import hashlib
import json
import random
import re
import sys
import uuid
import os
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError:
    runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if __name__=='__main__' and runtime.exists():os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
    raise

H=Path(__file__).with_suffix(''); VERSION='matrix-power-blank-v1'
SOURCE=json.loads((H/'source.json').read_text()); KP_ID=17592186115229
KP_UUID=SOURCE['record'][':knowledge-point/id']
GENERATOR_ID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
SUPPORTED_LEVELS=('easy','moderate')
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
MASKS={'q-279444':[0,2,3,4,8],'q-279446':[0,2,4,6,8],'q-279448':[2,3,4,6,8]}

def parse_matrix(text):
    m=MATRIX.search(text)
    if not m:raise ValueError('No matrix')
    rows=[[int(x.strip()) for x in row.split('&')] for row in m[1].split(r'\\')]
    return sp.Matrix(rows)

def tex(m):return r'\begin{bmatrix}'+' \\\\ '.join(' & '.join(str(x) for x in row) for row in m.tolist())+r'\end{bmatrix}'
def task_key(a,p):return json.dumps({'matrix':list(map(int,a)),'shape':list(a.shape),'power':p},sort_keys=True,separators=(',',':'))
def prompt_data(q):
    a=parse_matrix(q[':question/problem']);p=int(re.search(r'\^\{(\d+)\}',q[':question/problem'])[1]);return a,p
def fingerprint(q):
    try:a,p=prompt_data(q);return task_key(a,p)
    except (ValueError,TypeError,AttributeError):return None

PROFILES={}
for q in SOURCE['record'][':knowledge-point/questions']:
    fs=q.get(':question/answer-fields',[])
    if not fs or any(f[':answer-field/type'][':db/ident']!=':answer-field.type/blank' for f in fs):continue
    a,p=prompt_data(q);sid=q[':question/math-academy-id']
    PROFILES[sid]={'source':q,'a':a,'power':p,'mask':MASKS.get(sid,list(range(4))),'level':q[':question/difficulty'][':db/ident'].split('/')[-1]}

def generate(difficulty,seed=0,template=None,parameters=None):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    rng=random.Random(seed);templates=sorted(s for s,t in PROFILES.items() if t['level']==difficulty)
    sid=template or rng.choice(templates)
    if sid not in templates:raise ValueError('Template/difficulty mismatch')
    t=PROFILES[sid];old=t['a'];n=old.rows;p=t['power']
    if parameters is None:
        # Conservative source sparsity: preserve source zero cells; vary all nonzero cells.
        for attempt in range(1000):
            vals=[0 if z==0 else rng.choice([-4,-3,-2,-1,1,2,3,4,5]) for z in old]
            # Trace-zero cube source retains its observed scalar-square shortcut.
            if sid=='q-279430':vals[3]=-vals[0]
            a=sp.Matrix(n,n,vals)
            if max(abs(z) for z in a**p)<=1000 and a**2!=sp.zeros(n) and a!=a**p:break
        else:raise ValueError('Sampling bound exhausted')
    else:
        if len(parameters)!=n*n or any(type(z)!=int or not -5<=z<=5 for z in parameters):raise ValueError('Invalid matrix parameters')
        a=sp.Matrix(n,n,parameters)
    answer=a**p;orig=t['source']
    # Replace the exact source matrices in every ordered solution stage.
    substitutions={tuple(old**k):a**k for k in [1,2,p]}
    def matrices(text):return MATRIX.sub(lambda m:tex(substitutions[tuple(parse_matrix(m[0]))]),text)
    problem=matrices(orig[':question/problem']);solution=matrices(orig[':question/worked-solution'])
    if n==3:
        # The four supplied entries are dependent slots, not copied constants.
        remaining=[i for i in range(9) if i not in t['mask']];it=iter(remaining)
        prefix,body=problem.split('\n\n',1)
        body=re.sub(r'\$(-?\d+)\$',lambda m:'$'+str(answer[next(it)])+'$',body)
        problem=prefix+'\n\n'+body
    key=task_key(a,p);qid=str(uuid.uuid5(uuid.UUID(GENERATOR_ID),key+'|'+sid))
    fields=[]
    for k,i in enumerate(t['mask'],1):
        fid=str(uuid.uuid5(uuid.UUID(qid),'field-'+str(k)));aid=str(uuid.uuid5(uuid.UUID(fid),'canonical'))
        fields.append({':answer-field/id':fid,':answer-field/key':'field-'+str(k),':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':str(answer[i])}],':answer-field/correct':[':answer/id',aid]})
    return {'knowledge_point':{'id':KP_ID,'uuid':KP_UUID,'title':SOURCE['record'][':knowledge-point/title']},'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':fields},'generation':{'version':VERSION,'generator_id':GENERATOR_ID,'seed':seed,'template':sid,'parameters':list(map(int,a)),'power':p,'target_cells':t['mask'],'mathematical_key':key,'source_ids':[orig[':db/id']],'source_basis':SOURCE['basis'],'domain':'integer entries; normal nonzero slots in -4..5, fixed observed zero cells; rendered output <=1000','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plots':'none'}}

def batch(difficulty,count,seed):
    if count<1 or count>500:raise ValueError('Count outside bounded batch limit')
    out=[];used=set()
    for i in range(max(100,count*100)):
        r=generate(difficulty,seed+i)
        if r['generation']['mathematical_key'] in used:continue
        used.add(r['generation']['mathematical_key']);out.append(r)
        if len(out)==count:break
    if len(out)!=count:raise ValueError('Distinct batch limit reached')
    return out
def markdown(r):
    q=r['question'];return q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\n'+ '\n'.join(f[':answer-field/key']+': $'+f[':answer-field/choices'][0][':answer/value']+'$' for f in q[':question/answer-fields'])
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',required=True);parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json','markdown'],default='json');args=parser.parse_args()
    rows=batch(args.difficulty,args.count,args.seed);print(json.dumps(rows) if args.format=='json' else '\n\n'.join(markdown(r) for r in rows))
