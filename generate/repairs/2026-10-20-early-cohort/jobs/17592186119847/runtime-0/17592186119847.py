"""Rank from pivot counts. Exact source profiles; easy/moderate only.

Conservative finite domain: 1..12 pivot counts, dimensions 3..15.
Matrix name/dimensions and bank order never establish distinct task identity.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError:
    import os, sys
    interpreter=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    os.execv(str(interpreter),[str(interpreter),str(Path(__file__).resolve()),*sys.argv[1:]])

KP_ID=17592186119847
KP_UUID='be3d5a74-259e-58b9-948d-47ba7412ab08'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'rank-count-generator-v1'))
VERSION='rank-count-v1'
SUPPORTED_LEVELS=('easy','moderate')
HERE=Path(__file__).with_suffix('')
SOURCES={q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
PROFILES={'easy':('q-139950','q-34805','q-79157','q-79405'), 'moderate':('q-34806','q-139953','q-34826','q-79408')}

def source_parameters(q):
    text=q[':question/problem']
    name,m,n,c=re.search(r'\$([A-Z])\$.*?\$(\d+)\s*\\(?:times|cdot)\s*(\d+)\$.*?\$(\d+)\$',text).groups()
    return {'name':name,'rows':int(m),'columns':int(n),'count':int(c),'kind':'non-pivot' if '**non-pivot**' in text else 'pivot'}

def recipes(profile,p):
    m,n,c=p['rows'],p['columns'],p['count'];r=n-c if p['kind']=='non-pivot' else c
    return {
        'q-139950':[r-1,r+1,r-2,r,r-3],
        'q-34805':[m,r,r-2,1,n],
        'q-79157':[r,m,r-1,1,n],
        'q-79405':[r-1,n,r,r+1,m],
        'q-34806':[n,c,r,m,c-1],
        'q-139953':[n,c,n-1,r,m],
        'q-34826':[m,n,c,n-1,r],
        'q-79408':[r+1,m,r,c,n],
        'q-34825':[n,n-c,c-1,c-2,c],
    }[profile]

def fingerprint(text):
    p=source_parameters({':question/problem':text})
    # Ignore irrelevant matrix dimensions/name and every answer-bank choice.
    task=[p['kind'],p['count']] if p['kind']=='pivot' else [p['kind'],p['columns'],p['count']]
    return hashlib.sha256(json.dumps(task,separators=(',',':')).encode()).hexdigest()

def valid(p,level,profile):
    m,n,c=p['rows'],p['columns'],p['count'];r=n-c if level=='moderate' else c
    bank=recipes(profile,p)
    return 3<=m<=15 and 3<=n<=15 and 1<=r<=min(m,n,12) and (1<=c<n if level=='moderate' else c==r) and len(set(bank))==5 and min(bank)>=0 and bank.count(r)==1

def generate(difficulty='easy',seed=0,*,parameters=None,bank_profile=None):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    rng=random.Random(seed);profile=bank_profile or rng.choice(PROFILES[difficulty])
    if profile not in PROFILES[difficulty]:raise ValueError('Profile does not belong to difficulty')
    if parameters is None:
        for _ in range(10000):
            p={'name':rng.choice('ABCPQT'),'rows':rng.randint(3,15),'columns':rng.randint(3,15),'count':rng.randint(1,12),'kind':'pivot' if difficulty=='easy' else 'non-pivot'}
            if valid(p,difficulty,profile):break
        else:raise ValueError('Bounded parameter search exhausted')
    else:p=dict(parameters)
    assert p['kind']==('pivot' if difficulty=='easy' else 'non-pivot') and valid(p,difficulty,profile)
    r=sp.Integer(p['count']) if difficulty=='easy' else sp.Integer(p['columns'])-sp.Integer(p['count'])
    assert 0<=r<=min(p['rows'],p['columns'])
    original=source_parameters(SOURCES[profile])
    name,m,n,c=p['name'],p['rows'],p['columns'],p['count']
    if difficulty=='easy':
        problem=f'Let ${name}$ be a ${m}\\times {n}$ matrix that has ${c}$ **pivot** columns. What is the rank of the matrix?'
        solution=f'We know that $\\text{{rank}}({name})$ is the number of pivot columns in ${name}.$ \n\nSince we are told that ${name}$ has ${c}$ pivot columns, we have \n\n$$\n\\text{{rank}}({name})={r}.\n$$'
    else:
        problem=f'If ${name}$ is a ${m}\\times {n}$ matrix that has ${c}$ **non-pivot** columns, then $\\text{{rank}}({name})=$'
        solution=f'We know that $\\text{{rank}}({name})$ is the number of pivot columns in ${name}.$ \n\nSince ${name}$ has ${n}$ columns and ${c}$ of them are non-pivots, then the number of pivot columns in ${name}$ is \n\n$$\n{n}-{c}={r}.\n$$\n\nTherefore, $\\text{{rank}}({name})={r}.$'
    if c==1:
        problem=problem.replace('** columns','** column')
        solution=solution.replace('$1$ pivot columns','$1$ pivot column').replace('$1$ of them are non-pivots','$1$ of them is a non-pivot')
    # Original spelling/layout is retained on exact source replay.
    if p==original:problem=SOURCES[profile][':question/problem'];solution=SOURCES[profile][':question/worked-solution']
    content={'problem':problem,'solution':solution,'difficulty':difficulty,'profile':profile,'bank':sorted(recipes(profile,p))}
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION+json.dumps(content,sort_keys=True)))
    fid=str(uuid.uuid5(uuid.UUID(qid),'field:selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'value:'+str(v))),':answer/type':':answer.type/math',':answer/value':str(v)} for v in recipes(profile,p)]
    correct=next(a[':answer/id'] for a in answers if a[':answer/value']==str(r))
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Determining the Rank of a Matrix Given the Number of Pivot Columns'},'question':q,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':difficulty+'-rank-count','bank_profile':profile,'parameters':p,'parameter_fingerprint':fingerprint(problem),'dependencies':{'sympy':sp.__version__},'domain':'dimensions 3..15; positive rank <=12; non-pivot count positive; feasible rank <= min(rows,columns)','source_question':profile}}

def batch(difficulty,count=100,seed=0):
    out=[];seen=set()
    for i in range(count*100):
        r=generate(difficulty,seed+i);fp=r['generation']['parameter_fingerprint']
        if fp not in seen:out.append(r);seen.add(fp)
        if len(out)==count:break
    return out

def markdown(r):
    q=r['question'];return q[':question/problem']+'\n\n'+', '.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=SUPPORTED_LEVELS,default='easy');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='json');a=ap.parse_args();rs=batch(a.difficulty,a.count,a.seed);print(json.dumps({'instances':rs},indent=2) if a.format=='json' else '\n\n'.join(map(markdown,rs)))
