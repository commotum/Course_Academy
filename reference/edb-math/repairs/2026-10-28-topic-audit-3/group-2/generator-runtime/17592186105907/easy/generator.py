#!/usr/bin/env python3
"""Seeded volume practice. Exact standard-library arithmetic; no external state.

Retains the legacy generator's cofactor/magnitude backbone and complete-profile
bank rejection. Source layouts are replayable; authored bands follow exemplars.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
import random
import re
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = {'db_id':17592186105907,'id':'fe9711f6-e2ad-5eed-8ded-a6153b0322bd',
      'title':'Calculating the Volume of a Parallelepiped Spanned by Three Vectors'}
VERSION='volume-edges-2'
DATA=json.loads(Path(__file__).with_name('source-cases.json').read_text())
LEVELS=('easy','moderate','hard')
PROFILES=('cofactor_and_minor','unit_coefficients')
NAMES=('a','b','c')

def fingerprint(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def vec(v): return r'\langle '+','.join(map(str,v))+r'\rangle'
def name(i): return r'\mathbf{'+NAMES[i]+'}'
def atom(v): return '('+str(v)+')' if v<0 else str(v)
def matrix(rows): return r'\begin{vmatrix}'+r'\\'.join('&'.join(map(str,row)) for row in rows)+r'\end{vmatrix}'
def block(rows): return '$$\n'+r'\begin{aligned}'+'\n'+('\\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$'
def data(v):
    a,b,c=v
    minors=[b[1]*c[2]-b[2]*c[1], b[0]*c[2]-b[2]*c[0], b[0]*c[1]-b[1]*c[0]]
    terms=[a[0]*minors[0],-a[1]*minors[1],a[2]*minors[2]]
    return minors,terms,sum(terms)

def combination(coeff):
    out=''
    for i,x in enumerate(coeff):
        if x:out+=('-' if x<0 else '+' if out else '')+('' if abs(x)==1 else str(abs(x)))+name(i)
    return out

def actual_edges(base, transform):
    return [[sum(row[k]*base[k][j] for k in range(3)) for j in range(3)] for row in transform]

def determinant_solution(edges):
    a,b,c=edges;mins,terms,d=data(edges);cofs=[];sub=[]
    for i,(j,k) in enumerate(((1,2),(0,2),(0,1))):
        cofs.append(('' if i==0 else '-' if i==1 else '+')+atom(a[i])+r'\cdot '+matrix([[b[j],b[k]],[c[j],c[k]]]))
        sub.append(('' if i==0 else '-' if i==1 else '+')+atom(a[i])+'('+atom(b[j])+r'\cdot '+atom(c[k])+'-'+atom(b[k])+r'\cdot '+atom(c[j])+')')
    return ('The volume is the absolute value of the scalar triple product of the actual edge vectors. Use those edges as the determinant rows:\n\n'+block([
        r'D&='+matrix(edges),r'&='+cofs[0],r'&\quad '+cofs[1],r'&\quad '+cofs[2],r'&='+sub[0],r'&\quad '+sub[1],r'&\quad '+sub[2],r'&='+'+'.join(atom(t) for t in terms)+'='+str(d)+'.'])+
        '\n\nFinally, take the absolute value:\n\n$$\nV=|'+str(d)+'|='+str(abs(d))+'.\n$$')

def bank(edges, profile):
    a,b,c=edges;_,t,d=data(edges);v=abs(d)
    plus=sum((1 if i!=1 else -1)*a[i]*(b[j]*c[k]+b[k]*c[j]) for i,(j,k) in enumerate(((1,2),(0,2),(0,1))))
    if profile=='cofactor_and_minor':
        vals=[v,abs(t[0]+t[1]),abs(t[1]+t[2]),abs(plus),abs(t[0]-t[1]+t[2])]
        recipes=['volume','omit third cofactor','omit first cofactor','add within each minor','reverse middle cofactor sign']
    elif profile=='unit_coefficients':
        minors=data(edges)[0]
        unweighted=sum((1 if i!=1 else -1)*((1 if a[i]>0 else -1) if a[i] else 0)*minors[i] for i in range(3))
        vals=[v,abs(plus),abs(t[0]-t[1]+t[2]),abs(unweighted),abs(t[0]+t[1])]
        recipes=['volume','add within each minor','reverse middle cofactor sign','replace nonzero first-row coefficients by their signs','omit third cofactor']
    else: raise ValueError(profile)
    if len(set(vals))!=5 or min(vals)<=0: raise ValueError('Complete bank collides or includes zero')
    return vals,recipes

def record(prompt, solution, level, kind, vals, correct, meta, rng):
    # Normalize before identities; local vendored canonicalizer is stdlib only.
    prompt,solution=map(normalize_prose,(prompt,solution))
    vals=[normalize_tex(str(x)) for x in vals];correct=normalize_tex(str(correct))
    qid=str(uuid.uuid5(uuid.NAMESPACE_URL, KP['id']+'/'+fingerprint([prompt,solution,level,kind,sorted(vals),correct])))
    key='selection' if kind=='radio' else 'volume'
    fid=str(uuid.uuid5(uuid.UUID(qid),key))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
    cid=next(a[':answer/id'] for a in answers if a[':answer/value']==correct)
    rng.shuffle(answers)
    question={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,
              ':question/difficulty':':question.difficulty/'+level,
              ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,
                  ':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]}]}
    return validate_generated_record({'knowledge_point':KP.copy(),'question':question,'generation':{'version':VERSION,'provenance':DATA['provenance'],**meta}})

def coordinate_prompt(base):
    return 'Let\n\n'+block([name(i)+'&='+vec(v)+('.' if i==2 else ',') for i,v in enumerate(base)])

def build(level, params, kind='blank', profile=None, seed=0):
    rng=random.Random(seed);meta={'template':level+'_'+kind,'seed':seed,'parameters':copy.deepcopy(params),'source_ids':[], 'authored_extension':True}
    if level=='moderate':
        signed=params['signed_product'];scales=params['scales'];order=params['order']
        edge_text=[('' if scales[i]==1 else '-' if scales[i]==-1 else str(scales[i]))+name(order[i]) for i in range(3)]
        product=scales[0]*scales[1]*scales[2]
        inversions=sum(order[i]>order[j] for i in range(3) for j in range(i+1,3));orient=(-1)**inversions
        d=orient*product*signed
        prompt='Suppose $'+name(0)+r'\cdot('+name(1)+r'\times '+name(2)+')='+str(signed)+'$. Calculate the volume $V$ of the parallelepiped whose three edge vectors are '+', '.join('$'+e+'$' for e in edge_text)+'.\n\n$V=${{volume}}'
        expression='('+edge_text[0]+r')\cdot(('+edge_text[1]+r')\times('+edge_text[2]+'))'
        reordered=name(order[0])+r'\cdot('+name(order[1])+r'\times '+name(order[2])+')'
        orientation='An even number of pairwise swaps preserves the triple product.' if orient==1 else 'An odd number of pairwise swaps reverses the triple product sign.'
        solution=('The volume is the magnitude of the scalar triple product of the actual edges. Factor each edge scale out separately. '+orientation+'\n\n'+block([
            'D&='+expression,
            '&='+str(product)+r'\bigl['+reordered+r'\bigr]',
            '&='+str(product)+r'\cdot '+atom(orient)+r'\cdot '+atom(signed)+'='+str(d)+'.'])+
            '\n\nTake the absolute value:\n\n$$\nV=|'+str(d)+'|='+str(abs(d))+'.\n$$')
        vals=[abs(d)];meta['signed_product']=d;meta['bank_profile']=None
    else:
        base=params['vectors'];edges=base
        prompt=coordinate_prompt(base)+'\n\n'
        prefix=''
        if level=='hard':
            transform=params['transform'];edges=actual_edges(base,transform)
            exprs=[combination(row) for row in transform]
            prompt+='Calculate the volume $V$ of the parallelepiped whose three edge vectors are\n\n$$\n'+r',\quad '.join(exprs)+'.\n$$'
            steps=[]
            for i,(row,edge) in enumerate(zip(transform,edges)):
                components=[]
                for j in range(3):
                    components.append(''.join(('-' if x<0 else '+' if ii else '')+atom(base[k][j]) for ii,(k,x) in enumerate((k,x) for k,x in enumerate(row) if x)))
                steps.extend([r'\mathbf{'+('u','v','w')[i]+'}&='+exprs[i],r'&=\langle '+','.join(components)+r'\rangle',r'&='+vec(edge)+'.'])
            prefix='First form the actual edge vectors component by component:\n\n'+block(steps)+'\n\n'
        else:
            prompt+='Calculate the volume'+(' $V$' if kind=='blank' else '')+' of the parallelepiped spanned by these three vectors.'
        if kind=='blank':prompt+='\n\n$V=${{volume}}'
        d=data(edges)[2];solution=prefix+determinant_solution(edges)
        vals,recipes=bank(edges,profile) if kind=='radio' else ([abs(d)],[])
        meta.update(signed_product=d,bank_profile=profile,bank_recipes=recipes)
    if not d:raise ValueError('Degenerate parallelepiped')
    return record(prompt,solution,level,kind,vals,abs(d),meta,rng)

def sample(level,rng,kind=None,profile=None):
    kind=kind or (rng.choice(('blank','radio')) if level=='easy' else 'blank')
    profile=profile or (rng.choice(PROFILES) if kind=='radio' else None)
    # Choose the instructional case/profile first. Only compatible values resample.
    order=list(rng.sample(range(3),3))
    if level=='moderate':
        scales=rng.choice(((2,1,3),(-2,1,3),(1,-3,2),(3,2,1),(2,-1,-2),(1,2,2),(-3,-2,1)))
        params={'signed_product':rng.choice(tuple(range(-12,0))+tuple(range(1,13))), 'scales':list(scales),'order':order}
        return params,kind,profile
    cancellation=rng.choice(('aligned','mixed')) if level=='easy' and kind=='radio' else None
    transform=None
    if level=='hard':
        p,q,r=order;sign=rng.choice((-1,1));other=rng.choice((-1,1))
        u=[0]*3;v=[0]*3;w=[0]*3;u[p]=1;u[q]=sign;w[r]=1
        if rng.choice(('paired','chain'))=='paired':v[p]=1;v[q]=-sign
        else:v[q]=1;v[r]=other
        transform=[u,v,w];rng.shuffle(transform)
    for _ in range(2000):
        bound=4 if level=='easy' else 3
        base=[[rng.randint(-bound,bound) for _ in range(3)] for _ in range(3)]
        if level=='easy' and not 1<=sum(x==0 for row in base for x in row)<=3:continue
        edges=actual_edges(base,transform) if transform else base
        d=data(edges)[2]
        if not d or abs(d)>120:continue
        if kind=='radio':
            _,terms,_=data(edges)
            aligned=sum(abs(x) for x in terms)==abs(d)
            if aligned!=(cancellation=='aligned'):continue
            try:bank(edges,profile)
            except ValueError:continue
        params={'vectors':base}
        if transform:params['transform']=transform
        return params,kind,profile
    raise RuntimeError('No compatible instance for selected case/profile')

def generate(level, seed=0, kind=None, profile=None, parameters=None):
    if level not in LEVELS:raise ValueError('Unknown difficulty')
    rng=random.Random(seed)
    if parameters is None:parameters,kind,profile=sample(level,rng,kind,profile)
    return build(level,parameters,kind or 'blank',profile,seed)

def replay(source_id):
    originals=DATA['complete']+[x for x in DATA['exemplars']]
    for original in originals:
        q=original.get('question',original)
        if q[':question/id']==source_id:break
    else:raise ValueError('Not a complete source or exemplar')
    f=q[':question/answer-fields'][0];kind=f[':answer-field/type'];kind=kind.get(':db/ident') if isinstance(kind,dict) else kind;kind=kind.rsplit('/',1)[1]
    correct=f[':answer-field/correct'];correct=correct[':answer/value'] if isinstance(correct,dict) else next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct[1])
    level=q[':question/difficulty'];level=level.get(':db/ident') if isinstance(level,dict) else level;level=level.rsplit('/',1)[1]
    # Re-key the sole scalar blank without altering the supplied formula fragment.
    prompt=q[':question/problem'].replace('{{'+f[':answer-field/key']+'}}','{{volume}}')
    return record(prompt,q[':question/worked-solution'],level,kind,[a[':answer/value'] for a in f[':answer-field/choices']],correct,{'template':'source_replay','source_ids':[source_id],'evidence_only':True},random.Random(0))

def batch(level,seed,count):
    rng=random.Random(seed);records=[];seen=set()
    for _ in range(count*100+100):
        r=generate(level,rng.randrange(2**63));qid=r['question'][':question/id']
        if qid in seen:continue
        seen.add(qid);records.append(r)
        if len(records)==count:return records
    raise RuntimeError('Insufficient distinct instances')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty',choices=(*LEVELS,'unclassified','all'),default='easy')
    p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0)
    p.add_argument('--format',choices=('json',),default='json');p.add_argument('--replay-source')
    a=p.parse_args()
    if a.count<1:p.error('count must be positive')
    levels=LEVELS if a.difficulty=='all' else ('easy' if a.difficulty=='unclassified' else a.difficulty,)
    rs=[replay(a.replay_source)] if a.replay_source else [r for level in levels for r in batch(level,a.seed,a.count)]
    print(json.dumps(rs,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
