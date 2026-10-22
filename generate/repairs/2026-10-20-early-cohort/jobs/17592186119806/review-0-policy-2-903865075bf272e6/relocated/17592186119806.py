#!/usr/bin/env python3
"""Bounded easy vector-linear-combination generator. No database access.

Each source owns a complete bank profile. Integral dilation preserves its
component arithmetic; eligible component pairs preserve sum/subtraction roles.
Offsets are observed value patterns, not claims about learner error intent.
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
try:
    import sympy as sp
except ModuleNotFoundError:
    # Inventory invokes sys.executable; use the project's existing dependency
    # environment when the application process uses /usr/bin/python3.
    if __name__ != '__main__':
        raise
    import os, sys
    interpreter = Path(__file__).resolve().parents[2] / '.venv/bin/python'
    os.execv(str(interpreter), [str(interpreter), str(Path(__file__).resolve()), *sys.argv[1:]])

HERE = Path(__file__).resolve().with_suffix('')
SOURCE = json.loads((HERE / 'source.json').read_text())
KP_ID = 17592186119806
KP_UUID = SOURCE['record'][':knowledge-point/id']
GENERATOR_UUID = str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy:generator:' + str(KP_ID)))
VERSION = 'vector-linear-combination-1'
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

def generate(level,seed=0,profile=None,parameters=None):
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported level: '+level+'; see capabilities.json')
    rng=random.Random(seed)
    sid=profile or rng.choice(sorted(CASES))
    if sid not in CASES: raise ValueError('Unknown complete source bank profile')
    old=CASES[sid];p,q,a0,b0,old_target=parse_problem(old[':question/problem']);x0=(b0-p*a0)/q
    if parameters is None:
        k=rng.choice((1,2,3));target=rng.choice(eligible_targets(sid))
    else:
        if set(parameters)!={'scale','target'}: raise ValueError('Exactly scale and target required')
        k=parameters['scale'];target=tuple(parameters['target']) if parameters['target'] is not None else None
    if type(k) is not int or k not in (1,2,3) or target not in eligible_targets(sid):
        raise ValueError('Scale must be 1,2,3; target must retain source response role')
    a,b=k*a0,k*b0
    # Compute from supplied information; no stored answer lookup.
    x=sp.simplify((b-p*a)/q);answer=target_value(x,target)
    problem=old[':question/problem']
    ms=list(MATRIX.finditer(problem)); replacements={ms[0].span():tex(a),ms[-1].span():tex(b)}
    for (start,end),value in sorted(replacements.items(),reverse=True): problem=problem[:start]+value+problem[end:]
    if target is not None:problem=TARGET.sub(lambda _:target_tex(target),problem,count=1)
    solution=old[':question/worked-solution']
    # All four numeric matrices are coherently dilated: supplied, intermediate,
    # and solved vectors. Symbols and ordered isolation steps remain exact.
    solution=MATRIX.sub(lambda m:tex(k*vector(m.group())),solution)
    if target is not None and (k!=1 or target!=old_target):
        head=solution.split('Therefore,')[0]
        u,w=x[target[0]],x[target[1]];op=target[2]
        if op=='+': arithmetic=str(u)+('+'+str(w) if w>=0 else str(w))
        else: arithmetic=str(u)+'-'+('('+str(w)+')' if w<0 else str(w))
        spacing='' if 'Therefore,${' in old[':question/worked-solution'] else ' '
        solution=head+'Therefore,'+spacing+'$'+target_tex(target)+'='+arithmetic+'='+str(answer)+'.$'
    field0=old[':question/answer-fields'][0]
    base=target_value(x0,old_target)
    values=[]
    for option in field0[':answer-field/choices']:
        val=vector(option[':answer/value']) if old_target is None else sp.Integer(option[':answer/value'])
        # At source targets this is k*val. A changed target translates the entire
        # observed bank by the changed correct value; no profiles are pooled.
        values.append(sp.simplify(answer+k*(val-base)))
    assert len(set(map(tex,values)))==5 and sum(v==answer for v in values)==1
    bank=sorted(map(tex,values));content=hashlib.sha256(json.dumps([VERSION,problem,solution,bank],sort_keys=True).encode()).hexdigest()
    uid=lambda s:str(uuid.uuid5(uuid.NAMESPACE_URL,str(KP_ID)+':'+content+':'+s))
    choices=[{':answer/id':uid('selection:'+tex(v)),':answer/type':':answer.type/math',':answer/value':tex(v)} for v in values]
    correct=next(c[':answer/id'] for c,v in zip(choices,values) if v==answer)
    # Seed may reorder display; identities and mathematical novelty ignore order.
    rng.shuffle(choices)
    field={':answer-field/id':uid('selection'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}
    question={':question/id':uid('question'),':question/difficulty':':question.difficulty/easy',':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[field]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE['record'][':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'seed':seed,'template':template_id(sid),'bank_profile':sid,'source_id':sid,'parameters':{'scale':k,'target':list(target) if target else None},'mathematical_fingerprint':fingerprint(question),'content_fingerprint':content,'source':{'database':'math','basis':SOURCE['basis'],'lineage':SOURCE['lineage']},'dependencies':{'sympy':sp.__version__},'assets':[],'correct_value':tex(answer),'domain':'Source coefficients/dimensions/sign convention; uniform integer dilation 1..3; eligible same-operation component pairs','bank_policy':'complete observed affine-offset profile; underlying distractor intent unresolved; changed-target translation is a conservative authored extension'}}

def catalog():
    seen=set();result=[]
    for sid in sorted(CASES):
        for k in (1,2,3):
            for target in eligible_targets(sid):
                r=generate('easy',0,sid,{'scale':k,'target':list(target) if target else None})
                fp=r['generation']['mathematical_fingerprint']
                if fp not in seen:seen.add(fp);result.append(r)
    return result

def batch(level,count,seed=0):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported level: '+level)
    if count<0:raise ValueError('Count must be nonnegative')
    records=catalog();random.Random(seed).shuffle(records)
    if count>len(records):raise ValueError('Finite variant limit: '+str(len(records)))
    return records[:count]

def markdown(record):
    q=record['question'];return q[':question/problem']+'\n\n'+'\n'.join('$'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=5);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--profile');args=p.parse_args()
    records=batch(args.difficulty,args.count,args.seed) if not args.profile else [generate(args.difficulty,args.seed+i,args.profile) for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n'.join(map(markdown,records)))
