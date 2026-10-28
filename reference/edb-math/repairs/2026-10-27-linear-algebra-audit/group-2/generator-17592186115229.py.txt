"""Seeded matrix powers. Runtime is relocatable and standard-library only."""
import argparse
import json
import random
import re
import uuid
from pathlib import Path
from math_format import matrix_tex, matrix_answer, normalize_prose, normalize_tex, validate_generated_record

KP = {'db_id':17592186115229, 'id':'82e970fe-cff8-50e3-9b94-67ad97b03da7', 'title':'Finding a Power of a Matrix'}
VERSION = 'matrix-powers-v2'
LEVELS = ('easy','moderate','hard')
FAMILIES = {'easy':[(2,2)], 'moderate':[(2,3),(2,4),(3,2)], 'hard':[(3,3)]}
STRUCTURES = ('general','triangular','trace-zero','idempotent','nilpotent')
MATRIX = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
SOURCE_IDS = {(2,2):['b7ee3245-be46-5b91-9f47-fc17aebf1da1','49538b11-2cc9-55ec-b3f4-d0592d2d086e'],
 (2,3):['9af9d60f-891d-5b3e-9bc8-dbf34ec4be81','b47ca15a-ddfb-5bef-bdaa-d65e81339106'],
 (2,4):['a5e7f7a5-ffc5-5b07-aba7-9fd9dcbaae98','43ff301f-7fa9-522b-9191-9365c52a3db0','b599ded3-c09a-5f0e-81c0-0028d7937178'],
 (3,2):['d40d4525-2e40-5377-9893-10dea4b0a3c5','7e2f5758-dec0-5006-94af-278f989726ad','ccd2400f-e477-5772-b36d-b9c99ce24efe'],
 (3,3):['812ad39a-35a8-5d8f-9bb3-4d47c582659b']}

def mul(a,b):
    n=len(a)
    return [[sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def power(a,p):
    out=[[int(i==j) for j in range(len(a))] for i in range(len(a))]
    for _ in range(p):out=mul(out,a)
    return out

def parse_matrix(text):
    m=MATRIX.search(text)
    if m is None:raise ValueError('Missing matrix')
    return [[int(x.strip()) for x in row.split('&')] for row in m[1].split(r'\\')]

def positive_power(text):
    # Imported notation uses both A^{3} and {A}^{3}.
    return int(re.search(r'\^\{?(\d+)',text)[1])

def uid(text):return str(uuid.uuid5(uuid.UUID(KP['id']),text))
def display(text):return '\n\n$$\n'+text+'\n$$\n'
def integer_tex(n):return '('+str(n)+')' if n<0 else str(n)

def derivation(a,p,name):
    square=mul(a,a)
    stages=[(2,a,a)]
    if p>2:stages.append((p,square,a if p==3 else square))
    chunks=[]
    for exponent,left,right in stages:
        n=len(a);value=mul(left,right)
        products=[['+'.join(integer_tex(left[i][k])+r'\cdot '+integer_tex(right[k][j]) for k in range(n)) for j in range(n)] for i in range(n)]
        intro=('First multiply the matrix by itself:' if exponent==2 else
               'Now use $'+name+'^'+str(p)+'='+name+'^2'+r'\cdot '+name+('' if p==3 else '^2')+'$:')
        # Individual equations keep every three-term dot product visible in the UI.
        entry_rows=[('('+name+'^'+str(exponent)+')_{'+str(i+1)+str(j+1)+'} &= '+products[i][j]+'='+str(value[i][j])) for i in range(n) for j in range(n)]
        chunks.append(intro+display(name+'^'+str(exponent)+'='+matrix_tex(left)+r'\cdot '+matrix_tex(right))+
                      '\nCompute the entries by row-by-column products:'+display(r'\begin{aligned}'+r' \\ '.join(entry_rows)+r'\end{aligned}')+
                      '\nThus,'+display(name+'^'+str(exponent)+'='+matrix_tex(value)+'.'))
    return '\n'.join(chunks)

def make_record(level,a,p,mask=None,name='A',bank=None,source_ids=None,seed=0,structure='explicit'):
    n=len(a)
    if n not in (2,3) or any(len(row)!=n for row in a) or p not in (2,3,4):raise ValueError('Invalid matrix power')
    result=power(a,p)
    mask=sorted(range(n*n) if mask is None else mask)
    if len(mask)!=len(set(mask)) or any(i<0 or i>=n*n for i in mask):raise ValueError('Invalid target cells')
    problem='Consider the matrix $'+name+'='+matrix_tex(a)+'$. Find '+('the missing entries of ' if n==3 and bank is None else '')+'$'+name+'^'+str(p)+'$.'
    values=[]
    if bank is not None:
        problem+='\n\n$'+name+'^'+str(p)+'=$'
        values=[('selection',[matrix_tex(b) for b in bank],bank.index(result),'radio')]
    else:
        cells=[];k=0
        for i in range(n):
            row=[]
            for j in range(n):
                if i*n+j in mask:
                    k+=1;key='field-'+str(k);row.append('{{'+key+'}}')
                    values.append((key,[str(result[i][j])],0,'blank'))
                else:row.append(str(result[i][j]))
            cells.append(row)
        problem+='\n\n'+matrix_answer(name+'^'+str(p),cells)
    problem=normalize_prose(problem);solution=normalize_prose(derivation(a,p,name))
    # Content is normalized before stable identities are calculated.
    spec=json.dumps([level,problem,solution,values],sort_keys=True,separators=(',',':'))
    qid=uid(VERSION+spec);fields=[]
    for key,choices,correct,kind in values:
        fid=uid(qid+key);options=[]
        for idx,value in enumerate(choices):
            value=normalize_tex(value)
            options.append({':answer/id':uid(fid+str(idx)+value),':answer/type':':answer.type/math',':answer/value':value})
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':options,':answer-field/correct':[':answer/id',options[correct][':answer/id']]})
    record={'knowledge_point':KP.copy(),'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields},
      'generation':{'version':VERSION,'seed':seed,'template':str(n)+'x'+str(n)+'-power-'+str(p),'structure':structure,'parameters':a,'power':p,'target_cells':mask,'source_ids':source_ids or SOURCE_IDS[(n,p)],'semantic_key':json.dumps([a,p]),'response_contract':'complete matrix choice' if bank else 'scalar entries at visible matrix cells'}}
    return validate_generated_record(record)

def sample_matrix(rng,n,level,structure):
    cap=3 if level=='easy' else (1 if level=='hard' else 2)
    nonzero=[i for i in range(-cap,cap+1) if i]
    a=[[rng.randint(-cap,cap) for _ in range(n)] for _ in range(n)]
    if structure=='triangular':
        upper=rng.choice([True,False])
        for i in range(n):
            for j in range(n):
                if (i>j if upper else i<j):a[i][j]=0
    elif structure=='trace-zero':a[1][1]=-a[0][0]
    elif structure=='idempotent':
        # Dense rank-one projections require the same cancellation as the source.
        projections=[[[t,b],[c,1-t]] for t in range(-cap,cap+1) if abs(1-t)<=cap
                     for b in nonzero for c in nonzero if t not in (0,1) and b*c==t*(1-t)]
        a=rng.choice(projections)
    elif structure=='nilpotent':
        # A nonzero dense input: zero results arise from dot-product cancellations.
        cancellations=[[[t,b],[c,-t]] for t in nonzero for b in nonzero for c in nonzero if b*c==-t*t]
        a=rng.choice(cancellations)
    return a

def generate(difficulty,seed=0,family=None,structure=None,mask=None):
    if difficulty not in LEVELS:raise ValueError('Expected easy, moderate or hard')
    rng=random.Random(seed);n,p=family or rng.choice(FAMILIES[difficulty])
    if (n,p) not in FAMILIES[difficulty]:raise ValueError('Family does not belong to this band')
    # Assign target roles before incidental entries.
    mask=sorted(rng.sample(range(9),5)) if mask is None and n==3 else mask
    structures=STRUCTURES if difficulty=='easy' else (('general','triangular','trace-zero') if n==2 else ('general',))
    structure=structure or rng.choice(structures)
    if structure not in structures:raise ValueError('Unsupported structure')
    for attempt in range(1000):
        a=sample_matrix(rng,n,difficulty,structure);b=power(a,p)
        if difficulty=='moderate' and max(abs(v) for row in b for v in row)>100:continue
        if difficulty=='hard' and (sum(v==0 for row in a for v in row)>2 or power(a,2)==a or b==power(a,2) or b==a or all(i==j or v==0 for i,row in enumerate(power(a,2)) for j,v in enumerate(row))):continue
        return make_record(difficulty,a,p,mask,seed=seed,structure=structure)
    raise ValueError('Workload constraints exhausted')

def batch(difficulty,count,seed):
    if count<1 or count>500:raise ValueError('Count must be in 1..500')
    if difficulty=='unclassified':difficulty='easy'
    if difficulty not in LEVELS:raise ValueError('Unknown difficulty')
    rng=random.Random(seed);families=list(FAMILIES[difficulty]);rng.shuffle(families)
    structures=list(STRUCTURES);rng.shuffle(structures)
    out=[];seen=set()
    for i in range(count):
        family=families[i%len(families)]
        structure=structures[i%len(structures)] if difficulty=='easy' else None
        # Exhausting a small legitimate special family must not exhaust the batch.
        candidates=[structure]+[s for s in structures if s!=structure] if difficulty=='easy' else [None]
        found=False
        for candidate in candidates:
            for _ in range(200):
                item=generate(difficulty,rng.getrandbits(64),family,candidate)
                key=item['generation']['semantic_key']
                if key not in seen:
                    seen.add(key);out.append(item);found=True;break
            if found:break
        if not found:raise ValueError('Distinct semantic batch exhausted')
    return out

def source_cases():return json.loads(Path(__file__).with_name('source-cases.json').read_text())
def replay(q):
    text=q[':question/problem'];a=parse_matrix(text);p=positive_power(text);n=len(a)
    level=q[':question/difficulty'][':db/ident'].split('/')[-1]
    fs=q[':question/answer-fields'];kind=fs[0][':answer-field/type'][':db/ident'].split('/')[-1]
    mask=None;bank=None
    if kind=='radio':bank=[parse_matrix(c[':answer/value']) for c in fs[0][':answer-field/choices']]
    elif n==3:
        # Parse logical answer cells, ignoring source padding and answer-label cells.
        part=text.split('\n\n',1)[1]
        tokens=re.findall(r'\{\{field-\d+\}\}|\$-?\d+\$',part)
        if len(tokens)!=9:raise ValueError('Incomplete replay response layout')
        mask=[i for i,t in enumerate(tokens) if t.startswith('{{')]
    return make_record(level,a,p,mask,bank=bank,source_ids=[q[':question/id']],structure='source-replay')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',required=True,choices=[*LEVELS,'unclassified']);parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json'],default='json')
    args=parser.parse_args();print(json.dumps(batch(args.difficulty,args.count,args.seed)))
