#!/usr/bin/env python3
"""Bounded easy vector-linear-combination generator. No database access.

Source banks replay exactly. New banks assign the correct role independently
of candidate values and derive compatible vector data. Explicit diagnostic paths
retain source dilation and eligible component pairs.
Moderate and hard have no evidenced template and are rejected explicitly.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import re
import uuid
import sympy as sp

HERE = Path(__file__).resolve().with_suffix('')
SOURCE = json.loads((HERE / 'source.json').read_text())
KP_ID = 17592186119806
KP_UUID = SOURCE['record'][':knowledge-point/id']
GENERATOR_UUID = str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy:generator:' + str(KP_ID)))
VERSION = 'vector-linear-combination-2'
SUPPORTED_LEVELS = ('easy',)
CASES = {q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if q.get(':question/worked-solution') and q.get(':question/difficulty', {}).get(':db/ident') == ':question.difficulty/easy'}
MATRIX = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)
TARGET = re.compile(r'\{x\}_\{(\d+)\}([+-])\{x\}_\{(\d+)\}')

def vector(text):
    return sp.ImmutableMatrix([sp.Integer(x.strip()) for x in MATRIX.fullmatch(text)[1].split(r'\\')])

def tex(value):
    if isinstance(value, sp.MatrixBase):
        return r'\begin{bmatrix}' + r' \\ '.join(str(x) for x in value) + r'\end{bmatrix}'
    return str(value)

def parse_problem(problem):
    m = re.search(r'\$(\d+)a([+-])(\d+)x=b\$', problem)
    if not m:
        raise ValueError('Unrecognized source equation')
    p, q = int(m[1]), int(m[3]) * (1 if m[2] == '+' else -1)
    matrices = [m.group() for m in MATRIX.finditer(problem)]
    a, b = vector(matrices[0]), vector(matrices[-1])
    target = TARGET.search(problem)
    return p, q, a, b, (int(target[1])-1, int(target[3])-1, target[2]) if target else None

def eligible_targets(source_id):
    _, _, a, _, target = parse_problem(CASES[source_id][':question/problem'])
    if target is None:
        return [None]
    pairs = itertools.combinations(range(len(a)), 2) if target[2] == '+' else itertools.permutations(range(len(a)), 2)
    return [(i,j,target[2]) for i,j in pairs]

def target_value(x, target):
    return x if target is None else x[target[0]] + (1 if target[2] == '+' else -1)*x[target[1]]

def target_tex(target):
    i,j,op=target
    return '{x}_{'+str(i+1)+'}'+op+'{x}_{'+str(j+1)+'}'

def fingerprint(question):
    p,q,a,b,target = parse_problem(question[':question/problem'])
    if target is None:
        task=['vector',p,q,list(map(str,a)),list(map(str,b))]
    else:
        i,j,op=target
        cells=[(str(a[z]),str(b[z])) for z in (i,j)]
        if op=='+': cells.sort()
        task=['components',p,q,op,cells]
    return hashlib.sha256(json.dumps(task,sort_keys=True).encode()).hexdigest()

def template_id(source_id):
    old=CASES[source_id];p,q,a,b,target=parse_problem(old[':question/problem'])
    stage='reverse-subtraction' if ' & ='+str(p)+'a-b' in old[':question/worked-solution'] else 'signed-division' if q<0 else 'positive-division'
    return ('vector' if target is None else 'sum' if target[2]=='+' else 'difference')+'-'+str(len(a))+'-'+stage

def authored_bank(answer, rng):
    """Diagnostic forced-answer bank, without inherited ranks/extrema."""
    if isinstance(answer, sp.MatrixBase):
        values=[answer]
        while len(values)<5:
            v=answer+sp.ImmutableMatrix([rng.randint(-6,6) for _ in answer])
            if v not in values:values.append(v)
    else:
        # Select the number of alternatives below the answer before their gaps.
        below=rng.randrange(5)
        values=[answer]+[answer-d for d in rng.sample(range(1,16),below)]
        values += [answer+d for d in rng.sample(range(1,16),4-below)]
    return values


def generate(level,seed=0,profile=None,parameters=None):
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported level: '+level)
    rng=random.Random(seed)
    sid=profile or rng.choice(sorted(CASES))
    if sid not in CASES:raise ValueError('Unknown complete source bank profile')
    old=CASES[sid];p,q,a0,b0,old_target=parse_problem(old[':question/problem'])
    mode='authored'
    if parameters is None:
        target=rng.choice(eligible_targets(sid))
        correct_role=rng.randrange(5)
        if target is None:
            values=[]
            while len(values)<5:
                v=sp.ImmutableMatrix([rng.randint(-9,9) for _ in a0])
                if v not in values:values.append(v)
            x=values[correct_role]
        else:
            values=list(map(sp.Integer,rng.sample(range(-12,13),5)))
            wanted=values[correct_role];i,j,op=target
            first=rng.choice([u for u in range(-9,10)
                              if -9 <= (wanted-u if op=='+' else u-wanted) <= 9])
            coords=[rng.randint(-9,9) for _ in a0]
            coords[i]=first;coords[j]=wanted-first if op=='+' else first-wanted
            x=sp.ImmutableMatrix(coords)
        a=sp.ImmutableMatrix([rng.randint(-6,6) for _ in a0]);b=p*a+q*x
        params={'a':list(map(int,a)),'x':list(map(int,x)),
                'target':list(target) if target else None,
                'choices':[tex(v) for v in values]}
    elif set(parameters)=={'scale','target'}:
        k=parameters['scale'];target=tuple(parameters['target']) if parameters['target'] is not None else None
        if type(k) is not int or k not in (1,2,3) or target not in eligible_targets(sid):
            raise ValueError('Scale must be 1,2,3; target must retain source response role')
        a,b=k*a0,k*b0;x=(b-p*a)/q
        answer=target_value(x,target)
        if k==1 and target==old_target:
            mode='source-replay'
            values=[vector(v[':answer/value']) if target is None else sp.Integer(v[':answer/value'])
                    for v in old[':question/answer-fields'][0][':answer-field/choices']]
        else:
            mode='diagnostic'
            bank_rng=random.Random(json.dumps([seed,sid,list(map(int,a)),list(map(int,b)),target]))
            values=authored_bank(answer,bank_rng)
        params={'scale':k,'target':list(target) if target else None}
    elif set(parameters)=={'a','x','target','choices'}:
        target=tuple(parameters['target']) if parameters['target'] is not None else None
        if target not in eligible_targets(sid):raise ValueError('Invalid target')
        if any(type(z) is not int for z in parameters['a']+parameters['x']):raise ValueError('Integral coordinates required')
        if len(parameters['a'])!=len(a0) or len(parameters['x'])!=len(a0):raise ValueError('Dimension mismatch')
        a=sp.ImmutableMatrix(parameters['a']);x=sp.ImmutableMatrix(parameters['x']);b=p*a+q*x
        if any(abs(z)>6 for z in a) or any(abs(z)>9 for z in x):raise ValueError('Coordinates outside authored domain')
        values=[vector(v) if target is None else sp.Integer(v) for v in parameters['choices']]
        outside=(any(len(v)!=len(a0) or any(abs(z)>9 for z in v) for v in values)
                 if target is None else any(abs(v)>12 for v in values))
        if outside:
            raise ValueError('Choices outside authored domain')
        params=parameters
    else:raise ValueError('Use scale/target or complete authored instance parameters')
    # Derive the answer from the displayed data, including replay paths.
    x=sp.ImmutableMatrix((b-p*a)/q);answer=target_value(x,target)
    if len(values)!=5 or len(set(map(tex,values)))!=5 or sum(v==answer for v in values)!=1:
        raise ValueError('Five distinct choices and exactly one correct response required')
    problem=old[':question/problem']
    ms=list(MATRIX.finditer(problem));replacements={ms[0].span():tex(a),ms[-1].span():tex(b)}
    for (start,end),value in sorted(replacements.items(),reverse=True):problem=problem[:start]+value+problem[end:]
    if target is not None:problem=TARGET.sub(lambda _:target_tex(target),problem,count=1)
    solution=old[':question/worked-solution']
    reverse='reverse-subtraction' in template_id(sid)
    mats=iter([a,b,p*a-b,x] if reverse else [b,a,b-p*a,x])
    solution=MATRIX.sub(lambda _:tex(next(mats)),solution)
    if target is not None and not (a==a0 and b==b0 and target==old_target):
        head=solution.split('Therefore,')[0]
        u,w=x[target[0]],x[target[1]];op=target[2]
        if op=='+':arithmetic=str(u)+('+'+str(w) if w>=0 else str(w))
        else:arithmetic=str(u)+'-'+('('+str(w)+')' if w<0 else str(w))
        spacing='' if 'Therefore,${' in old[':question/worked-solution'] else ' '
        solution=head+'Therefore,'+spacing+'$'+target_tex(target)+'='+arithmetic+'='+str(answer)+'.$'
    bank=sorted(map(tex,values));content=hashlib.sha256(json.dumps([VERSION,problem,solution,bank],sort_keys=True).encode()).hexdigest()
    uid=lambda s:str(uuid.uuid5(uuid.NAMESPACE_URL,str(KP_ID)+':'+content+':'+s))
    choices=[{':answer/id':uid('selection:'+tex(v)),':answer/type':':answer.type/math',':answer/value':tex(v)} for v in values]
    correct=next(c[':answer/id'] for c,v in zip(choices,values) if v==answer)
    random.Random(str(seed)+':'+content).shuffle(choices)
    field={':answer-field/id':uid('selection'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}
    question={':question/id':uid('question'),':question/difficulty':':question.difficulty/easy',':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[field]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE['record'][':knowledge-point/title']},'question':question,
            'generation':{'version':VERSION,'seed':seed,'template':template_id(sid),'bank_profile':sid,'source_id':sid,
                          'parameters':params,'mode':mode,'mathematical_fingerprint':fingerprint(question),'content_fingerprint':content,
                          'source':{'database':'math','basis':SOURCE['basis'],'lineage':SOURCE['lineage']},
                          'dependencies':{'sympy':sp.__version__},'assets':[],'correct_value':tex(answer),
                          'domain':'Source coefficients/dimensions; eligible same-operation pairs; authored integer a in [-6,6], x in [-9,9], scalar candidates in [-12,12]; legacy scale 1..3 for diagnostics/replay',
                          'bank_policy':'Exact captured source bank on replay; authored exchangeable candidate bank in normal sampling; fresh forced-answer bank for explicit diagnostic paths'}}


def catalog():
    """Small deterministic representative catalog, not an exhaustive domain."""
    return [generate('easy',s,sid) for sid in sorted(CASES) for s in range(10)]


def batch(level,count,seed=0):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported level: '+level)
    if count<0:raise ValueError('Count must be nonnegative')
    rng=random.Random(seed);seen=set();result=[]
    for _ in range(max(100,count*10)):
        if len(result)==count:break
        r=generate(level,rng.getrandbits(63));fp=r['generation']['mathematical_fingerprint']
        if fp in seen:continue
        seen.add(fp);result.append(r)
    if len(result)!=count:raise ValueError('Unable to generate requested distinct instances')
    return result


def markdown(record):
    q=record['question'];return q[':question/problem']+'\n\n'+'\n'.join('$'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=5);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--profile');args=p.parse_args()
    records=batch(args.difficulty,args.count,args.seed) if not args.profile else [generate(args.difficulty,args.seed+i,args.profile) for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n'.join(map(markdown,records)))
