#!/usr/bin/env python3
"""Bounded easy vector-linear-combination generator. No database access.

Source banks replay exactly. New banks assign the correct role independently
of candidate values and derive compatible vector data. Explicit diagnostic paths
retain source dilation and eligible component pairs.
Moderate collects vector terms on both sides. Hard distributes and tests cancellation.
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
from vector_notation import vector_prose, plain_vector_prose

HERE = Path(__file__).resolve().with_suffix('')
SOURCE = json.loads((HERE / 'source.json').read_text())
KP_ID = 17592186119806
KP_UUID = SOURCE['record'][':knowledge-point/id']
GENERATOR_UUID = str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy:generator:' + str(KP_ID)))
VERSION='vector-linear-combination-3-notation-v1'
SUPPORTED_LEVELS = ('easy','moderate','hard')
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
    problem=plain_vector_prose(problem)
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
    if level != 'easy':
        return extended(level,seed,profile,parameters)
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
    problem=vector_prose(problem,'abx');solution=vector_prose(solution,'abx')
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


def extended(level,seed,profile=None,parameters=None):
    """Same vector rules: collect terms; then distribute and inspect cancellation."""
    rng=random.Random(seed)
    if parameters is None:
        n=rng.choice([3,4]);a=[rng.randint(-4,4) for _ in range(n)]
        x=[rng.randint(-5,5) for _ in range(n)]
        k=rng.choice([2,3,4]);s=rng.choice([-1,1]);q=rng.choice([-3,-2,2,3]);r=rng.choice([-3,-2,-1,1,2,3])
        if level=='moderate':r=rng.choice([v for v in [-3,-2,-1,1,2,3] if v!=q])
        # hard adds distribution; all outcome roles remain eligible.
        outcome=profile or rng.choice(['unique','unique','none','all']) if level=='hard' else 'unique'
        if outcome not in ['unique','none','all']: raise ValueError('Unknown extension profile')
        d=0 if outcome!='unique' else q
        t=(k*s+r-d) if level=='hard' else r-d
        b=[k*u+d*v for u,v in zip(a,x)]
        if outcome=='none':b[rng.randrange(n)]+=rng.choice([-2,-1,1,2])
        params={'a':a,'b':b,'k':k,'s':s,'r':r,'t':t}
    else:
        if set(parameters)!={'a','b','k','s','r','t'}:raise ValueError('Invalid extension parameters')
        params=parameters.copy();a=params['a'];b=params['b'];k=params['k'];s=params['s'];r=params['r'];t=params['t']
        if len(a) not in (3,4) or len(a)!=len(b) or any(type(z)!=int for z in a+b+[k,s,r,t]):raise ValueError('Integral equal-dimensional vectors required')
    a=sp.ImmutableMatrix(a);b=sp.ImmutableMatrix(b);n=len(a)
    d=(k*s+r-t) if level=='hard' else r-t
    residual=b-k*a
    outcome='unique' if d else 'all' if residual==sp.zeros(n,1) else 'none'
    if level=='moderate' and (not d or not r or not t):raise ValueError('Moderate requires nonzero unknown terms on both sides and a unique vector')
    def term(c,v):
        return ('+' if c>=0 else '-')+(str(abs(c)) if abs(c)!=1 else '')+v
    A=r'\mathbf{a}';X=r'\mathbf{x}';B=r'\mathbf{b}'
    left=str(k)+A+term(r,X)
    if level=='hard':left=str(k)+r'\left('+A+term(s,X)+r'\right)'+term(r,X)
    right=B+term(t,X)
    eq=left+'='+right
    rows=[left+'&='+right]
    if level=='hard':rows.append(str(k)+A+term(k*s,X)+term(r,X)+'&='+right)
    rows += [str(d)+X+'&='+B+'-'+str(k)+A, str(d)+X+'&='+tex(residual)]
    if d:
        x=sp.ImmutableMatrix(residual/d)
        rows += [X+r'&=\frac{1}{'+str(d)+'}'+tex(residual),X+'&='+tex(x)]
        answer=tex(x)
        errors=[-x,residual,(b+k*a)/d,b/d-k*a,sp.ImmutableMatrix(list(x)[::-1])]
        values=[x]
        for v in errors:
            v=sp.ImmutableMatrix(v)
            if v not in values:values.append(v)
        # At least two distinct instance-specific mathematical errors, never filler.
        if len(values)<3:raise ValueError('Degenerate error bank')
        wrong=values[1:];rng.shuffle(wrong);values=[x]+wrong
        values=values[:3] if level=='hard' else values[:5]
        if level=='moderate' and len(values)<5:raise ValueError('Degenerate error bank')
        texts=[(tex(v),':answer.type/math') for v in values]
        if level=='hard':texts += [('No solution',':answer.type/text'),('Every vector in $'+r'\mathbb{R}^'+str(n)+'$',':answer.type/text')]
        tail='Divide every component by $'+str(d)+'$. Substitution into the original equation verifies this vector.'
    else:
        answer='No solution' if outcome=='none' else 'Every vector in $'+r'\mathbb{R}^'+str(n)+'$'
        texts=[('No solution',':answer.type/text'),('Every vector in $'+r'\mathbb{R}^'+str(n)+'$',':answer.type/text')]
        # Zero residual does not imply x=0; a nonzero residual cannot be divided by zero.
        candidates=[sp.zeros(n,1),residual,a,b,-a]
        unique=[]
        for v in candidates:
            if v not in unique:unique.append(v)
        if len(unique)<3:raise ValueError('Degenerate cancellation bank')
        texts += [(tex(v),':answer.type/math') for v in unique[:3]]
        tail=('The unknown vector cancels. The residual is nonzero, so the equation is false for every vector: **no solution**.' if outcome=='none' else 'The unknown vector cancels and the residual is the zero vector. The equation is true for **every vector** in $'+r'\mathbb{R}^'+str(n)+'$.')
    problem='Solve for $'+X+r'\in\mathbb{R}^'+str(n)+'$ if\n\n$$\n'+eq+'\n$$\n\nwhere\n\n$$\n'+A+'='+tex(a)+r',\qquad '+B+'='+tex(b)+'.\n$$'
    solution=('Distribute the scalar and collect the unknown vector terms.' if level=='hard' else 'Collect the unknown vector terms, then subtract the known vector term.')+'\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$\n\n'+tail
    content=hashlib.sha256(json.dumps([VERSION,level,problem,solution,sorted(texts)]).encode()).hexdigest()
    uid=lambda s:str(uuid.uuid5(uuid.NAMESPACE_URL,str(KP_ID)+':'+content+':'+s))
    choices=[{':answer/id':uid(v),':answer/type':typ,':answer/value':v} for v,typ in texts];rng.shuffle(choices)
    qn={':question/id':uid('question'),':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':uid('field'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(answer)]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE['record'][':knowledge-point/title']},'question':qn,'generation':{'version':VERSION,'seed':seed,'template':level+'-'+outcome,'parameters':params,'correct_value':answer,'assets':[],'mathematical_fingerprint':hashlib.sha256(problem.encode()).hexdigest(),'source_id':'e-4790; investigation exemplars','mode':'authored-extension'}}


def catalog():
    """Small deterministic representative catalog, not an exhaustive domain."""
    return [generate('easy',s,sid) for sid in sorted(CASES) for s in range(10)]



def batch_shortcut(records):
    """Reject deterministic rank/position cues within recognizable displayed families."""
    groups={'all':records}
    for record in records:
        prompt=record['question'][':question/problem']
        signature=('distributed-minus' if r'\mathbf{a}-' in prompt else 'distributed-plus') if r'\left(' in prompt else ('scalar-target' if 'value of' in prompt else 'vector-target')
        groups.setdefault(signature,[]).append(record)
    for group in groups.values():
        if len(group)<2:continue
        observations=[]
        for record in group:
            f=record['question'][':question/answer-fields'][0];choices=f[':answer-field/choices'];key=f[':answer-field/correct'][1]
            bank=[]
            for i,c in enumerate(choices):
                text=c[':answer/value'];m=MATRIX.fullmatch(text)
                if m:value=tuple(sp.Rational(z.strip()) for z in m[1].split(r'\\'))
                elif re.fullmatch(r'-?\d+',text):value=(sp.Rational(text),)
                else:continue
                bank.append((value,i))
            observations.append((next(i for i,c in enumerate(choices) if c[':answer/id']==key),[i for value,i in sorted(bank)]))
        for rank in range(5):
            limit=max(1, (2*len(group)+4)//5) if len(group)>2 else 1
            if sum(i==rank for i,order in observations)>limit:return True
            if sum(rank<len(order) and order[rank]==i for i,order in observations)>limit:return True
    return False


def batch(level,count,seed=0):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported level: '+level)
    if count<0:raise ValueError('Count must be nonnegative')
    rng=random.Random(seed);seen=set();result=[]
    for _ in range(max(1000,count*200)):
        if len(result)==count:
            if count<3 or not batch_shortcut(result):break
            result=[];seen=set()
        try:r=generate(level,rng.getrandbits(63))
        except ValueError as exc:
            if 'Degenerate' not in str(exc):raise
            continue
        fp=r['generation']['mathematical_fingerprint']
        if fp in seen:continue
        seen.add(fp);result.append(r)
    if len(result)!=count or (count>=3 and batch_shortcut(result)):raise ValueError('Unable to generate requested distinct instances without a batch shortcut')
    return result


def markdown(record):
    q=record['question'];return q[':question/problem']+'\n\n'+'\n'.join('$'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=5);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--profile');args=p.parse_args()
    records=batch(args.difficulty,args.count,args.seed) if not args.profile else [generate(args.difficulty,args.seed+i,args.profile) for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n'.join(map(markdown,records)))
