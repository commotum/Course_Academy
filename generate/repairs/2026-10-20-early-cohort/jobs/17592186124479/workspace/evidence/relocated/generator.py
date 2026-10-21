#!/usr/bin/env python3
"""Pivot-column counts, observed moderate radio templates only.

Pure generator: no database writes. See the sibling package for source evidence,
classification, exact source-bank replay, native grading and validation receipts.
Source replay retains every original stage and complete bank. Normal sampling
chooses residual survival cases before constructing compatible row operations.
"""
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
from math_format import checked_math_content, normalize_prose, matrix_tex
HERE = Path(__file__).resolve().parent
SOURCE = json.loads((HERE/'source-data.json').read_text())
KP = SOURCE['record']; ID = 17592186124479; VERSION = 'pivot-columns-2'
MATRIX = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)
LEVELS = ('moderate',)

def matrices(text):
    return [s.Matrix([[s.Rational(c.strip()) for c in row.split('&')] for row in body.split(r'\\')]) for body in MATRIX.findall(text)]

def data(m): return [[str(x) for x in row] for row in m.tolist()]
def matrix(rows): return s.Matrix([[s.Rational(x) for x in row] for row in rows])
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(x): return str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),digest(x)))
def tex(m): return matrix_tex([[s.latex(c) for c in row] for row in m.tolist()], augmented=False)
def mask(m): return tuple(x != 0 for x in m)
def rank(m): return int(m.rank())
def fingerprint(m):
    # Primitive integer representatives of rows exclude trivial row rescaling.
    # Preserve the column positions; their values affect elimination arithmetic.
    rows=[]
    for row in m.tolist():
        values=[s.Rational(x) for x in row]
        den=s.ilcm(1,*[x.q for x in values]);ints=[int(x*den) for x in values]
        g=s.igcd(*ints) if any(ints) else 1
        ints=[x//abs(g) for x in ints]
        first=next((x for x in ints if x),1)
        rows.append([x*(1 if first>0 else -1) for x in ints])
    return digest({'task':'count-pivot-columns','matrix':rows})

def extract(q):
    states=matrices(q[':question/worked-solution']);a=matrices(q[':question/problem'])[0]
    assert states and states[0]==a
    operations=[]
    for before,after in zip(states,states[1:]):
        changed=[i for i in range(a.rows) if before.row(i)!=after.row(i)];assert len(changed)==1
        i=changed[0];delta=after.row(i)-before.row(i);matches=[]
        for j in range(a.rows):
            if i==j:continue
            pivot=next((k for k in range(a.cols) if before[j,k]),None)
            if pivot is None:continue
            c=delta[pivot]/before[j,pivot]
            if c and delta==c*before.row(j): matches.append((i,j,c))
        assert len(matches)==1,(q[':question/math-academy-id'],matches)
        operations.append(matches[0])
    assert states[-1].is_echelon
    f=q[':question/answer-fields'][0]
    bank=sorted(int(a[':answer/value']) for a in f[':answer-field/choices'])
    assert len(bank)==len(set(bank))==5
    assert rank(a)==int(f[':answer-field/correct'][':answer/value'])
    return {'source':q,'states':states,'operations':operations,'bank':bank,'profile':'counts-'+','.join(map(str,bank)), 'name':re.search(r'\$([A-Z])',q[':question/problem'])[1]}

TEMPLATES={q[':question/math-academy-id']:extract(q) for q in KP[':knowledge-point/questions'] if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/moderate' and q.get(':question/worked-solution') and q[':question/answer-fields'][0].get(':answer-field/correct')}
EXCLUDED=[q[':question/math-academy-id'] for q in KP[':knowledge-point/questions'] if q[':question/math-academy-id'] not in TEMPLATES]

def render(template,states,ops,seed,parameters):
    t=TEMPLATES[template];name=parameters.get('name',t['name']);answer=rank(states[0]);assert answer in t['bank']
    prompt=f'Determine the number of pivot columns of the matrix ${name},$ given by\n\n$$\n{name}={tex(states[0])}.\n$$'
    rows=[name+' & ='+tex(states[0])]
    for (i,j,c),after in zip(ops,states[1:]):
        # Give the annotation its own line so six-column matrices fit the player.
        rows.append(fr' & \quad {{R}}_{{{i+1}}} :={{R}}_{{{i+1}}}+({s.latex(c)}){{R}}_{{{j+1}}}')
        rows.append(' & ∼'+tex(after))
    solution=f'First, we need to convert ${name}$ to row echelon form:\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$\n\n'+f'Looking at the row echelon form, we see that ${name}$ has ${answer}$ pivots, and therefore the number of pivot columns is ${answer}.$'
    prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    # Identity depends on normalized visible content and bank, never seed/order.
    qid=uid([VERSION,prompt,t['bank']]);fid=uid([qid,'selection'])
    choices=[{':answer/id':uid([fid,str(n)]),':answer/type':':answer.type/math',':answer/value':str(n)} for n in t['bank']]
    random.Random(str(seed)+'/choices').shuffle(choices)
    f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid([fid,str(answer)])]}
    q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',':question/answer-fields':[f]}
    return {'knowledge_point':{'db_id':ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':template,'profile':t['profile'],'seed':seed,'parameters':parameters,'states':[data(m) for m in states],'operations':[[i,j,str(c)] for i,j,c in ops],'mathematical_fingerprint':fingerprint(states[0]),'eligible_for_learning':True,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_question_id':t['source'][':question/id'],'python':sys.version.split()[0],'sympy':s.__version__}}

def permitted_ranks(t):
    m=t['states'][0].rows
    return [r for r in range(max(2,m-2),m+1) if r in t['bank']]


def reconstruct(final,ops):
    states=[final]
    for i,j,c in reversed(ops):
        before=states[0].copy()
        before[i,:]=before.row(i)-c*before.row(j)
        states.insert(0,before)
    return states


def valid_instance(states,ops):
    if not states[-1].is_echelon:return False
    if any(v.q!=1 or abs(v)>40 for a in states for v in a):return False
    for before,after,(i,j,c) in zip(states,states[1:],ops):
        lead=next((h for h in range(before.cols) if before[j,h]),None)
        if lead is None or not c or not before[i,lead] or after[i,lead]:return False
        if any(before[i,h] for h in range(lead)):return False
    return True


@checked_math_content
def generate(level='moderate',seed=0,template=None,parameters=None,profile=None,decision=None):
    if level not in LEVELS:raise ValueError('Unsupported difficulty: only source-calibrated moderate is validated')
    rng=random.Random(seed);template=template or rng.choice(list(TEMPLATES));t=TEMPLATES[template]
    if profile not in (None,t['profile']):raise ValueError('Source-bank profile must match template')
    m,n=t['states'][0].shape;k=len(t['operations'])
    ranks=permitted_ranks(t)
    active_options=list(range(max(3,min(ranks)+1),m+1))
    if parameters is not None:
        active=int(parameters['active_rows']);prefix=active-k
        if active not in active_options:raise ValueError('Unsupported active block')
        final=matrix(parameters['echelon'])
        ops=[(int(i),int(j),s.Rational(c)) for i,j,c in parameters['operations']]
        if final.shape!=(m,n) or len(ops)!=k:raise ValueError('Shape or operation count outside workload')
        if [i for i,j,c in ops]!=list(range(prefix,active)) or any(not 0<=j<prefix for i,j,c in ops):raise ValueError('Invalid operation roles')
        if any(c not in (-3,-2,-1,1,2,3) for i,j,c in ops):raise ValueError('Multiplier outside normal range')
        if rank(final) not in permitted_ranks(t):raise ValueError('Unsupported residual survival case')
        name=parameters['name']
        if name not in 'ABCDPQ':raise ValueError('Invalid matrix name')
    else:
        # Decide which residual rows survive before filling values or labels.
        if decision is None:
            r=rng.choice(ranks)
            active=rng.choice([a for a in active_options if max(min(ranks),a-k)<=r<=a])
        else:
            r,active=decision
            if r not in ranks or active not in active_options or not active-k<=r<=active:
                raise ValueError('Unsupported residual-survival assignment')
        prefix=active-k
        pivots=sorted(rng.sample(range(n),r))
        final=s.zeros(m,n)
        for i,pivot in enumerate(pivots):
            final[i,pivot]=rng.choice([-4,-3,-2,-1,1,2,3,4])
            for h in range(pivot+1,n):final[i,h]=rng.randint(-3,3)
        ops=[(i,rng.randrange(prefix),s.Integer(rng.choice([-3,-2,-1,1,2,3]))) for i in range(prefix,active)]
        name=rng.choice('ABCDPQ')
    states=reconstruct(final,ops)
    if any(any(states[0].row(i)) != (i<active) for i in range(m)):raise ValueError('Initial active rows must be an initial segment')
    if not valid_instance(states,ops):raise ValueError('Invalid elimination; no fallback or silent case rejection')
    p={'mode':'normal','active_rows':active,'name':name,'echelon':data(final),'operations':[[i,j,str(c)] for i,j,c in ops],
       'surviving_rows':rank(final),'pivot_columns':[j+1 for j in final.rref()[1]]}
    return render(template,states,ops,seed,p)


def source_replay(template):
    t=TEMPLATES[template]
    p={'mode':'source-replay','name':t['name'],'echelon':data(t['states'][-1]),
       'operations':[[i,j,str(c)] for i,j,c in t['operations']]}
    return checked_math_content(render)(template,t['states'],t['operations'],0,p)

def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)


def generate_batch(level='moderate',count=1,seed=0,template=None):
    """Cover contrasting survival cases without conditioning the item sampler.

    Blocks share workload and initial active-row count, so those visible cues
    cannot fix the pivot count. Shuffle afterwards: block order is not a key.
    Singletons retain the original independent-item behavior.
    """
    if count<0:raise ValueError('count must be nonnegative')
    if level not in LEVELS:raise ValueError('Unsupported difficulty')
    if count==0:return []
    if count==1:return [generate(level,seed,template)]
    rng=random.Random(str(seed)+'/batch-survival-v1')
    sizes=([3] if count%2 else [])+[2]*(count//2-(1 if count%2 else 0))
    records=[];seen=set();item_seed=seed
    for size in sizes:
        chosen=template or rng.choice(list(TEMPLATES))
        t=TEMPLATES[chosen];m=t['states'][0].rows;k=len(t['operations'])
        ranks=permitted_ranks(t)
        active=rng.choice(list(range(max(3,min(ranks)+1),m+1)))
        cases=[r for r in ranks if active-k<=r<=active]
        rng.shuffle(cases)
        assignments=(cases*((size+len(cases)-1)//len(cases)))[:size]
        for r in assignments:
            for _ in range(1000):
                record=generate(level,item_seed,chosen,decision=(r,active));item_seed+=1
                fp=record['generation']['mathematical_fingerprint']
                if fp not in seen:break
            else:raise ValueError('Distinct semantic instance limit reached')
            seen.add(fp);records.append(record)
    rng.shuffle(records)
    return records

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=LEVELS,default='moderate');p.add_argument('--seed',type=int,default=0);p.add_argument('--template',choices=list(TEMPLATES));p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--output',type=Path);a=p.parse_args()
    if a.count<0:p.error('--count must be nonnegative')
    records=generate_batch(a.difficulty,a.count,a.seed,a.template)
    if a.format=='json':out=json.dumps(records,indent=2)+'\n'
    else:
        out='\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+r['question'][':question/worked-solution'] for r in records)+'\n'
    if a.output:a.output.write_text(out)
    else:print(out,end='')
