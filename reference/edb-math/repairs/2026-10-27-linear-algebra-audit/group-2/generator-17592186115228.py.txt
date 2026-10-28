#!/usr/bin/env python3
"""Seeded finite matrix-law practice. All runtime files are local and stdlib-only."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import uuid
from math_format import normalize_prose, validate_generated_record, validate_prose

HERE = Path(__file__).resolve().parent
KP = {'db_id': 17592186115228, 'id': '5a870c4a-daa5-5df2-8968-d8bf9ac0bd75',
      'title': 'Identifying True Statements Regarding Matrix Multiplication'}
VERSION = 'matrix-laws-2.0.1'
M = lambda *xs: ('mul', *xs)
A = lambda x,y: ('add',x,y)
S = lambda x,y: ('sub',x,y)
P = lambda x: ('pow',x)
I = 'I'


def tex(e):
    if isinstance(e,str): return 'I_2' if e == I else e
    op,*xs=e
    if op=='pow': return tex(xs[0])+'^2'
    if op=='mul':
        return ''.join(('('+tex(x)+')') if not isinstance(x,str) and x[0] in ('add','sub','mul') else tex(x) for x in xs)
    return tex(xs[0])+('+' if op=='add' else '-')+tex(xs[1])


def poly(e):
    """Free noncommutative ring over three generators; I is its unit."""
    if isinstance(e,str): return {() if e==I else (e,):1}
    op,*xs=e
    if op=='pow': return poly(M(xs[0],xs[0]))
    out=poly(xs[0])
    for x in xs[1:]:
        q=poly(x)
        if op=='mul':
            z={}
            for a,c in out.items():
                for b,d in q.items(): z[a+b]=z.get(a+b,0)+c*d
        else:
            z=dict(out)
            for a,c in q.items(): z[a]=z.get(a,0)+(c if op=='add' else -c)
        out={a:c for a,c in z.items() if c}
    return out


def evaluate(e,env):
    if isinstance(e,str): return env[e]
    op,*xs=e
    if op=='pow': return evaluate(M(xs[0],xs[0]),env)
    l,r=map(lambda x:evaluate(x,env),xs)
    if op=='mul': return tuple(tuple(sum(l[i][k]*r[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    return tuple(tuple(l[i][j]+(r[i][j] if op=='add' else -r[i][j]) for j in range(2)) for i in range(2))


def matrix(m): return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(map(str,row)) for row in m)+r'\end{bmatrix}'


def witness(l,r):
    pool=[((1,0),(0,1)),((1,0),(0,0)),((0,1),(0,0)),((0,0),(1,0)),((0,0),(0,0)),((1,1),(0,1))]
    for vals in itertools.product(pool,repeat=3):
        env=dict(zip('ABC',vals))|{'I':pool[0]}
        lv,rv=evaluate(l,env),evaluate(r,env)
        if lv!=rv: return env,lv,rv
    raise ValueError('False claim has no tested witness')


def claim(family, truth, rng, *, letters=None, side=None, sign=None, error=None):
    x,y,z=letters or rng.sample(list('ABC'),3)
    side=side if side is not None else rng.randrange(2)
    sign=sign if sign is not None else rng.choice(['+','-'])
    error=error if error is not None else rng.randrange(3)
    add=A if sign=='+' else S
    if family in ('associate','hidden'):
        lhs=M(x,M(y,z)); stages=[lhs,M(M(x,y),z)]
        rhs=stages[-1] if truth else (M(M(y,x),z) if error%2==0 else M(M(x,z),y))
        reason='Associativity moves parentheses while retaining the order of every factor.'
    elif family=='square':
        lhs=M(P(x),y); stages=[lhs,M(M(x,x),y),M(x,M(x,y))]
        rhs=stages[-1] if truth else (M(x,M(y,x)) if error%2==0 else M(y,M(x,x)))
        reason='A square is a repeated product. Expand it first, then regroup without swapping factors.'
    elif family=='unit':
        lhs=M(x,I) if side==0 else M(I,x); stages=[lhs,x]
        rhs=x if truth else I
        reason='The identity factor disappears; the arbitrary matrix remains.'
    elif family in ('distribute','sum_order'):
        if family=='sum_order': sign='+'; add=A
        lhs=M(x,add(y,z)) if side==0 else M(add(y,z),x)
        u,v=(M(x,y),M(x,z)) if side==0 else (M(y,x),M(z,x))
        stages=[lhs,add(u,v)]
        if family=='sum_order': stages.append(A(v,u))
        rhs=stages[-1]
        if not truth:
            swap=lambda t:M(t[2],t[1])
            a,b=(v,u) if family=='sum_order' else (u,v)
            if error==0: a=swap(a)
            elif error==1: b=swap(b)
            else: a,b=swap(a),swap(b)
            rhs=add(a,b)
        reason='Distribute with the outside factor on the same side in each product.'
        if family=='sum_order': reason+=' The two summands may then be interchanged because matrix addition is commutative.'
    elif family=='unit_dist':
        lhs=M(x,add(y,I)) if side==0 else M(add(y,I),x)
        prod=M(x,y) if side==0 else M(y,x)
        unit=M(x,I) if side==0 else M(I,x)
        stages=[lhs,add(prod,unit),add(prod,x)]
        rhs=stages[-1] if truth else (prod if error%2==0 else add(M(prod[2],prod[1]),x))
        reason='First distribute, keeping the outside factor on its original side. Then remove the identity factor; its entire term must remain.'
    else: raise ValueError(family)
    assert (poly(lhs)==poly(rhs))==truth
    assert all(poly(t)==poly(lhs) for t in stages)
    return {'family':family,'lhs':lhs,'rhs':rhs,'stages':stages,'truth':truth,'reason':reason,
            'parameters':{'letters':[x,y,z],'side':side,'sign':sign,'error':error}}


def canonical_claim(c):
    # Independent alpha-renaming per claim: letter roles across independent claims add no work.
    raw=json.dumps([c['lhs'],c['rhs']],separators=(',',':'))
    return min(raw.translate(str.maketrans(dict(zip('ABC',p)))) for p in itertools.permutations('ABC'))


def semantic(cs): return tuple(sorted(canonical_claim(c) for c in cs))


def subset_text(mask):
    parts=[v for i,v in enumerate(['I','II','III']) if mask&(1<<i)]
    return ' and '.join(parts)+' only'


def make_record(level,cs,*,shape='checkbox',rng=None,seed=0):
    rng=rng or random.Random(seed)
    assert len(cs)==3 and any(c['truth'] for c in cs)
    intro=r'Let $A$, $B$, and $C$ be $2\times 2$ real matrices'
    if any('I_2' in tex(c['lhs'])+tex(c['rhs']) for c in cs): intro+=r', and let $I_2$ be the identity matrix'
    intro+='.'
    if level=='easy': intro+='\n\nRemember: regrouping a product changes its parentheses without changing the order of its factors.'
    intro+='\n\nWhich statements are always true?'
    equations=[tex(c['lhs'])+'='+tex(c['rhs']) for c in cs]
    if shape=='checkbox': intro+=' Select all that apply.'
    else:
        intro+='\n\n'+'\n\n'.join('**'+label+'.** $'+eq+'$' for label,eq in zip(['I','II','III'],equations))
    solution=[]
    for c,eq in zip(cs,equations):
        status='always true' if c['truth'] else 'not always true'
        block='- $'+eq+'$ is **'+status+'**. '+c['reason']+'\n\n'
        stages=c['stages']
        rows=[tex(stages[0])+r' &='+tex(stages[1])]+[r' &='+tex(t) for t in stages[2:]]
        block+='$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
        if not c['truth']:
            env,lv,rv=witness(c['lhs'],c['rhs'])
            block+='\n\nThe proposed right side is not guaranteed to equal this result. For example, take\n\n$$\n'
            block+=r',\quad '.join(k+'='+matrix(env[k]) for k in 'ABC')+'.\n$$\n\n'
            block+='Then the left side is $'+matrix(lv)+'$ and the proposed right side is $'+matrix(rv)+'$, so this is a counterexample.'
        solution.append(block)
    mask=sum(1<<i for i,c in enumerate(cs) if c['truth'])
    solution.append('Select '+', '.join('$'+e+'$' for c,e in zip(cs,equations) if c['truth'])+'.')
    prompt=normalize_prose(intro); worked=normalize_prose('\n\n'.join(solution))
    # Normalize all visible content before deriving content identities.
    payload={'prompt':prompt,'solution':worked,'claims':equations,'shape':shape,'level':level}
    qid=str(uuid.uuid5(uuid.UUID(KP['id']),json.dumps(payload,sort_keys=True)))
    uid=lambda label:str(uuid.uuid5(uuid.UUID(qid),label))
    fields=[]
    def field(key,values,correct):
        key=normalize_prose(key); validate_prose(key)
        values=[normalize_prose(v) for v in values]
        fid=uid('field:'+key)
        choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/text',':answer/value':v} for v in values]
        rng.shuffle(choices)
        return {':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+shape,
                ':answer-field/choices':choices,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in choices if a[':answer/value']==correct)]}
    if shape=='checkbox':
        for c,eq in zip(cs,equations): fields.append(field('$'+eq+'$',['false','true'],str(c['truth']).lower()))
    else:
        # Five complete response subsets. Every distractor makes an inclusion/omission error.
        candidates=[m for m in range(1,7) if m!=mask]
        chosen=[mask]+rng.sample(candidates,4)
        fields=[field('selection',[subset_text(m) for m in chosen],subset_text(mask))]
    record={'knowledge_point':dict(KP),'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,
            ':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':fields},
            'generation':{'version':VERSION,'seed':seed,'template':level+'-matrix-laws','profile':shape,
                          'parameters':[{'family':c['family'],'truth':c['truth'],**c['parameters']} for c in cs],
                          'semantic_instance':hashlib.sha256(repr(semantic(cs)).encode()).hexdigest(),
                          'source_support':['tutorial-2997','tutorial-2998','tutorial-3129','q-42265','q-130449','q-130446','q-75662']}}
    return validate_generated_record(record)


def sample(level,mask,rng):
    families={'easy':['unit','associate','distribute'],
              'moderate':['associate','unit_dist','distribute'],
              'hard':['square','sum_order','hidden']}[level]
    cs=[claim(f,bool(mask&(1<<i)),rng,sign='+' if level=='easy' else None) for i,f in enumerate(families)]
    rng.shuffle(cs)
    return cs


def _candidate_batch(level,count,seed,rng):
    records=[]; seen=set(); masks=[]
    for i in range(count):
        if not masks: masks=list(range(1,7)); rng.shuffle(masks)
        mask=masks.pop()
        for attempt in range(10000):
            cs=sample(level,mask,rng); sig=semantic(cs)
            if sig not in seen: break
        else: raise ValueError('Finite catalog exhausted; requested batch exceeds available decision instances')
        seen.add(sig)
        shape='radio' if level=='moderate' and rng.randrange(2) else 'checkbox'
        records.append(make_record(level,cs,shape=shape,rng=rng,seed=seed))
    return records


def generate_batch(level,count,seed):
    if count<0: raise ValueError('count must be nonnegative')
    rng=random.Random(seed)
    # Balancing truth masks before statement shuffling does not prevent a
    # displayed position becoming a constant answer-producing cue. Reject such
    # whole batches using the same deterministic stream, never a replacement seed.
    for _ in range(1000):
        records=_candidate_batch(level,count,seed,rng)
        if count<4: return records
        outcomes=[]
        for record in records:
            parameters=record['generation']['parameters']
            outcomes.append([p['truth'] for p in parameters])
        if all(len({row[i] for row in outcomes})==2 for i in range(3)):
            return records
    raise ValueError('Could not construct a batch with varying displayed truth roles')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=['easy','moderate','hard'],required=True)
    ap.add_argument('--count',type=int,default=1)
    ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json'],default='json')
    ap.add_argument('--replay-source',action='store_true')
    args=ap.parse_args()
    if args.replay_source:
        data=json.loads((HERE/'source_replays.json').read_text())
        records=[r for r in data if r['question'][':question/difficulty']==':question.difficulty/'+args.difficulty]
    else: records=generate_batch(args.difficulty,args.count,args.seed)
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
