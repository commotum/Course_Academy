#!/usr/bin/env python3
"""Pivot-column counts, observed moderate radio templates only.

Pure generator: no database writes. See the sibling package for source evidence,
classification, exact source-bank replay, native grading and validation receipts.
Variable slots are echelon entries and elimination multipliers; all stage roles,
zero patterns, dimensions, field contracts and complete source banks are retained.
"""
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
HERE = Path(__file__).with_suffix('')
SOURCE = json.loads((HERE/'reference/source.json').read_text())
KP = SOURCE['record']; ID = 17592186124479; VERSION = 'pivot-columns-1'
MATRIX = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)
LEVELS = ('moderate',)

def matrices(text):
    return [s.Matrix([[s.Rational(c.strip()) for c in row.split('&')] for row in body.split(r'\\')]) for body in MATRIX.findall(text)]

def data(m): return [[str(x) for x in row] for row in m.tolist()]
def matrix(rows): return s.Matrix([[s.Rational(x) for x in row] for row in rows])
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(x): return str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),digest(x)))
def tex(m): return r'\begin{bmatrix}' + r' \\ '.join(' & '.join(s.latex(c) for c in row) for row in m.tolist()) + r'\end{bmatrix}'
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
    t=TEMPLATES[template];name=t['name'];answer=rank(states[0]);assert answer in t['bank']
    prompt=f'Determine the number of pivot columns of the matrix ${name},$ given by\n\n$$\n{name}={tex(states[0])}.\n$$'
    rows=[name+' & ='+tex(states[0])]
    for (i,j,c),after in zip(ops,states[1:]):
        rows[-1]+=f' & {{R}}_{{{i+1}}} & :={{R}}_{{{i+1}}}+({s.latex(c)}){{R}}_{{{j+1}}}'
        rows.append(' & ∼'+tex(after))
    solution=f'First, we need to convert ${name}$ to row echelon form:\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$\n\n'+f'Looking at the row echelon form, we see that ${name}$ has ${answer}$ pivots, and therefore the number of pivot columns is ${answer}.$'
    # Identity depends on the actual mathematical task and bank, never seed/order.
    qid=uid([VERSION,fingerprint(states[0]),t['bank']]);fid=uid([qid,'selection'])
    choices=[{':answer/id':uid([fid,str(n)]),':answer/type':':answer.type/math',':answer/value':str(n)} for n in t['bank']]
    f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid([fid,str(answer)])]}
    q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',':question/answer-fields':[f]}
    return {'knowledge_point':{'db_id':ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':template,'profile':t['profile'],'seed':seed,'parameters':parameters,'states':[data(m) for m in states],'operations':[[i,j,str(c)] for i,j,c in ops],'mathematical_fingerprint':fingerprint(states[0]),'eligible_for_learning':True,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_question_id':t['source'][':question/id'],'python':sys.version.split()[0],'sympy':s.__version__}}

def generate(level='moderate',seed=0,template=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('Unsupported difficulty: only source-calibrated moderate is validated')
    rng=random.Random(seed);template=template or rng.choice(list(TEMPLATES));t=TEMPLATES[template]
    if profile not in (None,t['profile']):raise ValueError('Source-bank profile must match template')
    for _ in range(3000):
        if parameters is None:
            if rng.randrange(2):
                # A constrained proposal exercises coefficient slots even when
                # structural zeros impose several exact cancellation equations.
                ds=[rng.choice([-2,-1,1,2]) for _ in range(t['states'][-1].rows)]
                cs=[rng.choice([-2,-1,1,2]) for _ in range(t['states'][-1].cols)]
                final=t['states'][-1].copy()
                for i in range(final.rows):
                    for j in range(final.cols):final[i,j]*=ds[i]*cs[j]
                coeff=[c*s.Rational(ds[i],ds[j]) for i,j,c in t['operations']]
            else:
                final=t['states'][-1].applyfunc(lambda x:rng.choice([i for i in range(-9,10) if i]) if x else 0)
                coeff=[s.Rational(rng.choice([-3,-2,-1,1,2,3])) for op in t['operations']]
        else:
            final=matrix(parameters['echelon']);coeff=list(map(s.Rational,parameters['multipliers']))
        if final.shape!=t['states'][-1].shape or mask(final)!=mask(t['states'][-1]) or len(coeff)!=len(t['operations']) or not all(coeff):raise ValueError('Slot structure')
        if any(abs(x)>40 or x.q!=1 for x in final):
            if parameters is not None:raise ValueError('Integer entry bounds')
            continue
        if any(c not in [s.Rational(n,d) for n in range(-5,6) if n for d in (1,2,3,4,5)] for c in coeff):
            if parameters is not None:raise ValueError('Multiplier bounds')
            continue
        ops=[(i,j,c) for (i,j,_),c in zip(t['operations'],coeff)]
        states=[final]
        for i,j,c in reversed(ops):
            before=states[0].copy();before[i,:]=before.row(i)-c*before.row(j);states.insert(0,before)
        valid=all(mask(a)==mask(b) for a,b in zip(states,t['states'])) and all(x.q==1 and abs(x)<=40 for m in states for x in m)
        if not valid:
            if parameters is not None:raise ValueError('Parameters change stage structure or integer arithmetic')
            continue
        p={'echelon':data(final),'multipliers':list(map(str,coeff))}
        return render(template,states,ops,seed,p)
    raise ValueError('Bounded sampler exhausted; no duplicate fallback')

def source_replay(template):
    t=TEMPLATES[template]
    return generate(template=template,parameters={'echelon':data(t['states'][-1]),'multipliers':[str(c) for _,_,c in t['operations']]})
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',default='moderate');p.add_argument('--seed',type=int,default=0);p.add_argument('--template',choices=list(TEMPLATES));p.add_argument('--count',type=int,default=1);p.add_argument('--output',type=Path);a=p.parse_args()
    records=[];seen=set()
    for offset in range(max(1,a.count)*1000):
        if len(records)>=a.count:break
        r=generate(a.difficulty,a.seed+offset,a.template);fp=r['generation']['mathematical_fingerprint']
        if fp not in seen:records.append(r);seen.add(fp)
    out=json.dumps({'instances':records,'requested_count':a.count,'shortage':max(0,a.count-len(records))},indent=2)+'\n'
    if a.output:a.output.write_text(out)
    else:print(out,end='')
