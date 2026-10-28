#!/usr/bin/env python3
"""Seeded four-vertex parallelepiped practice; no service or database access.

The displacement/cofactor construction reuses the existing 17592186105909
scratch generator's mathematical backbone. Current source cases replace its
obsolete basis-1356 data, and banks are constructed from concrete error paths.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP_ID = 17592186105909
KP_UUID = '57c790ad-c7fb-596c-8b60-cddd9b4e2165'
TITLE = 'Calculating the Volume of a Parallelepiped Spanned by Three Position Vectors Given Their Coordinates'
VERSION = 'vertex-volume-3'
ROOT = Path(__file__).resolve().parent


def determinant(rows):
    return (rows[0][0]*(rows[1][1]*rows[2][2]-rows[1][2]*rows[2][1])
            - rows[0][1]*(rows[1][0]*rows[2][2]-rows[1][2]*rows[2][0])
            + rows[0][2]*(rows[1][0]*rows[2][1]-rows[1][1]*rows[2][0]))


def vectors(points):
    return [[x-y for x,y in zip(p,points[0])] for p in points[1:]]


def data(points):
    u,v,w = vectors(points)
    products = [(v[1]*w[2],v[2]*w[1]), (v[0]*w[2],v[2]*w[0]), (v[0]*w[1],v[1]*w[0])]
    terms = [u[i]*(1 if i != 1 else -1)*(p-q) for i,(p,q) in enumerate(products)]
    return u,v,w,products,terms,sum(terms)


def scalar(n):
    return '('+str(n)+')' if n < 0 else str(n)


def vec(v):
    return r'\langle'+','.join(map(str,v))+r'\rangle'


def matrix(rows):
    return r'\begin{vmatrix}'+r' \\ '.join(' & '.join(map(str,row)) for row in rows)+r'\end{vmatrix}'


def aligned(rows):
    return '$$\n'+r'\begin{aligned}'+'\n'+('\\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$'


def expansion(points):
    edges=vectors(points)
    row=min(range(3),key=lambda i:sum(x!=0 for x in edges[i]))
    others=[i for i in range(3) if i!=row]
    minors=[];terms=[]
    for col in range(3):
        cols=[i for i in range(3) if i!=col]
        minor=[[edges[r][c] for c in cols] for r in others]
        minor_value=minor[0][0]*minor[1][1]-minor[0][1]*minor[1][0]
        minors.append((minor,minor_value))
        terms.append((-1)**(row+col)*edges[row][col]*minor_value)
    return edges,row,minors,terms


def solution(points):
    edges,row,minors,terms=expansion(points);total=sum(terms)
    rows=[]
    for name,point,edge in zip('BCD',points[1:],edges):
        subtraction=','.join(str(x)+'-'+scalar(y) for x,y in zip(point,points[0]))
        rows.append(r'\overrightarrow{A'+name+r'}&=\langle'+subtraction+r'\rangle='+vec(edge))
    text='Subtract the common vertex $A$ from each endpoint:\n\n'+aligned(rows)
    text+='\n\nUse the scalar triple product:\n\n'
    text+='$T=\\overrightarrow{AB}\\cdot(\\overrightarrow{AC}\\times\\overrightarrow{AD})$.\n\n'
    text+=aligned(['T&='+matrix(edges)])
    signs='$+,-,+$' if row%2==0 else '$-,+,-$'
    text+='\n\nExpand along row $'+str(row+1)+'$, whose cofactor signs are '+signs+'. Zero entries make no contribution. Evaluate the needed minors:\n\n'
    minor_rows=[]
    for i,(m,value) in enumerate(minors):
        if not edges[row][i]: continue
        minor_rows.extend([
            'M_'+str(i+1)+'&='+matrix(m),
            '&='+scalar(m[0][0])+r'\cdot'+scalar(m[1][1])+'-'+scalar(m[0][1])+r'\cdot'+scalar(m[1][0])+'='+str(value)])
    text+=aligned(minor_rows)
    coeff=[(-1)**(row+i)*edges[row][i] for i in range(3)]
    text+='\n\nCombine the signed contributions before taking the absolute value:\n\n'
    text+=aligned(['T&='+'+'.join(scalar(c)+'M_'+str(i+1) for i,c in enumerate(coeff) if edges[row][i]),
                   '&='+'+'.join(scalar(c)+r'\cdot'+scalar(m[1]) for i,(c,m) in enumerate(zip(coeff,minors)) if edges[row][i]),
                   '&='+'+'.join(scalar(t) for i,t in enumerate(terms) if edges[row][i])+'='+str(total)])
    text+='\n\n'+aligned(['V&=|'+str(total)+'|='+str(abs(total))+r'\text{ cubic units}.'])
    return text


def prompt(points,band,kind):
    text=r'Calculate the volume $V$ of the parallelepiped spanned by $\overrightarrow{AB}$, $\overrightarrow{AC}$, and $\overrightarrow{AD}$, given'+'\n\n'
    # Two lines avoid long coordinate rows in the actual UI.
    coords=[name+'('+','.join(map(str,p))+')' for name,p in zip('ABCD',points)]
    text+=aligned([coords[0]+r',&\quad '+coords[1]+',',coords[2]+r',&\quad '+coords[3]+'.'])
    if band=='easy':
        text+='\n\nFirst subtract the coordinates of $A$ from each endpoint to find the edge vectors. Then use\n\n'
        text+='$$\n'+r'V=\left|\overrightarrow{AB}\cdot\left(\overrightarrow{AC}\times\overrightarrow{AD}\right)\right|.'+'\n$$'
    text+='\n\n'+('Select the volume in cubic units.' if kind=='radio' else 'Enter the volume in cubic units.\n\n$V=$ {{field-1}}')
    return text


def make_record(points,band,kind,values,rng,profile='authored',source=None,problem=None,worked=None,recipes=None):
    total=data(points)[-1]; correct=str(abs(total))
    problem=normalize_prose(problem or prompt(points,band,kind))
    worked=normalize_prose(worked or solution(points))
    values=[normalize_tex(str(x)) for x in values]
    identity={'version':VERSION,'problem':problem,'solution':worked,'values':sorted(values),'correct':correct,'kind':kind,'band':band}
    digest=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),digest));fid=str(uuid.uuid5(uuid.UUID(qid),'field'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    aid=next(a[':answer/id'] for a in answers if a[':answer/value']==correct)
    rng.shuffle(answers)
    record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{
        ':question/id':qid,':question/difficulty':':question.difficulty/'+band,
        ':question/problem':problem,':question/worked-solution':worked,
        ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection' if kind=='radio' else 'field-1',
        ':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',aid]}]},
        'generation':{'version':VERSION,'parameters':{'points':points},'profile':profile,'source_id':source,
                      'bank_origin':'source-replay' if source else 'authored-error-paths','recipes':recipes or {},
                      'signed_contributions':data(points)[-2],'signed_triple_product':total,'content_fingerprint':digest}}
    return validate_generated_record(record)


def bank(points,profile,rng=None):
    rng = rng or random.Random(json.dumps(points))
    u,v,w,prod,terms,total=data(points);value=abs(total); edges=[u,v,w]
    position=abs(determinant(points[1:]))
    if profile=='origin':
        # All nonempty subsets of forgotten origin subtractions are plausible.
        # Choosing four from the seven breaks the fixed single/all parity relation.
        candidates=[]
        for flags in itertools.product([False,True],repeat=3):
            if not any(flags):continue
            rows=[points[i+1][:] if flags[i] else edges[i][:] for i in range(3)]
            candidates.append((abs(determinant(rows)), 'omit A subtraction for edges '+','.join('A'+'BCD'[i] for i in range(3) if flags[i])))
        rng.shuffle(candidates);wrong=[];seen={value}
        for candidate,reason in candidates:
            if candidate>0 and candidate not in seen:
                seen.add(candidate);wrong.append((candidate,reason))
            if len(wrong)==4:break
        if len(wrong)!=4:raise ValueError('Insufficient distinct origin errors')
    elif profile=='minor':
        axis=next((i for i,row in enumerate(edges) if sum(x!=0 for x in row)==1),None)
        if axis is None: raise ValueError('minor profile requires an axis edge')
        ordered=[edges[axis]]+[edges[i] for i in range(3) if i!=axis]
        a,b,c=ordered;k=next(i for i,x in enumerate(a) if x)
        j,l=[i for i in range(3) if i!=k]
        p=b[j]*c[l];q=b[l]*c[j];coef=a[k]
        wrong=[(abs(coef*p),'omit second minor product'),(abs(coef*q),'omit first minor product'),
               (abs(coef*(p+q)),'add the two minor products'),(position,'use endpoint position vectors')]
    elif profile=='cofactor':
        active=[i for i,t in enumerate(terms) if t]
        if len(active)==2:
            i,j=active
            # Missing either cofactor; reversing one cofactor sign; wrong origin.
            wrong=[(abs(total-terms[i]),'omit contribution '+str(i+1)),(abs(total-terms[j]),'omit contribution '+str(j+1)),
                   (abs(total-2*terms[j]),'reverse cofactor sign '+str(j+1)),(position,'use endpoint position vectors')]
        elif len(active)==3:
            wrong=[(abs(total-t),'omit contribution '+str(i+1)) for i,t in enumerate(terms)]+[(position,'use endpoint position vectors')]
        else: raise ValueError('cofactor profile needs multiple contributions')
    else: raise ValueError('Unknown profile')
    vals=[value]+[v for v,_ in wrong]
    if len(set(vals))!=5 or any(v<=0 for v in vals):raise ValueError('Whole-bank collision or nonpositive volume choice')
    if sum(v%2 for v in vals) in (1,4):raise ValueError('Isolated parity cue in whole bank')
    return vals,{str(value):'absolute displacement determinant',**{str(v):why for v,why in wrong}}


def sample_points(band,rng):
    if band=='easy':
        # Choose the answer-bearing axis and edge before components.
        axis=rng.randrange(3);slot=rng.randrange(3)
        edges=[[rng.randint(-3,3) for _ in range(3)] for _ in range(3)]
        edges[slot]=[0,0,0];edges[slot][axis]=rng.choice([-3,-2,-1,1,2,3])
    elif band=='moderate':
        missing=rng.randrange(3)
        edges=[[rng.choice([-3,-2,-1,1,2,3]) for _ in range(3)] for _ in range(3)]
        edges[0][missing]=0
    else:
        edges=[[rng.choice([-3,-2,-1,1,2,3]) for _ in range(3)] for _ in range(3)]
    origin=[rng.randint(-3,3) for _ in range(3)]
    return [origin]+[[a+b for a,b in zip(origin,e)] for e in edges]


def generate(band,seed=0,kind=None,profile=None,points=None):
    rng=random.Random(seed)
    kind=kind or (rng.choice(['radio','blank']) if band=='hard' else 'radio')
    # Complete bank profile is fixed before numerical rejection sampling.
    profile=profile or (rng.choice(['origin','minor']) if band=='easy' else rng.choice(['origin','cofactor']))
    for attempt in range(10000):
        pts=points or sample_points(band,rng)
        u,v,w,products,terms,total=data(pts)
        good=(pts[0]!=[0,0,0] and total!=0 and abs(total)<=90 and max(map(abs,terms))<=100)
        if band=='moderate':good=good and sum(t!=0 for t in terms)==2
        if band=='hard':good=good and sum(t!=0 for t in terms)>=2
        if not good:
            if points is not None:raise ValueError('Unsupported diagnostic parameters')
            continue
        try:vals,recipes=bank(pts,profile,rng) if kind=='radio' else ([abs(total)],{})
        except ValueError:
            if points is not None:raise
            continue
        rec=make_record(pts,band,kind,vals,rng,profile,recipes=recipes)
        rec['generation'].update(seed=seed,rejections=attempt)
        return rec
    raise RuntimeError('Compatible full-bank sampling exhausted')


def source_replay(source_id,seed=0):
    case=next(c for c in json.loads((ROOT/'source_cases.json').read_text()) if c['source_id']==source_id)
    worked=case['solution']
    if source_id=='q-73744':worked=worked.replace('=3j+3k','=j+3k')
    if source_id=='q-281027':worked=worked.replace('=-9-8+8','=-9+8-8')
    start=worked.index('$$');end=worked.index('$$',start+2)+2
    prefix=worked[:end]+'\n\n'
    derived=solution(case['points'])
    worked=prefix+derived[derived.index('Use the scalar triple product:'):]
    return make_record(case['points'],case.get('band','hard'),case['kind'],case['values'],random.Random(seed),profile='source-replay',source=source_id,problem=case['problem'],worked=worked)


def visible_groups(record):
    """Only prompt-visible sparsity, with no access to the key or error profile."""
    edges=vectors(record['generation']['parameters']['points'])
    groups=['all-radio']
    for edge,row in enumerate(edges):
        if sum(x!=0 for x in row)==1:
            groups.append('axis-edge-'+str(edge)+'/'+str(next(i for i,x in enumerate(row) if x)))
        elif sum(x!=0 for x in row)==2:
            groups.append('two-component-edge-'+str(edge)+'/zero-'+str(row.index(0)))
    return groups


def bank_coordinates(record):
    field=record['question'][':question/answer-fields'][0]
    if not field[':answer-field/type'].endswith('/radio'):return None
    vals=[int(a[':answer/value']) for a in field[':answer-field/choices']]
    key=abs(data(record['generation']['parameters']['points'])[-1])
    return sorted(vals).index(key), vals.index(key)


def batch(band,count,seed):
    rng=random.Random(seed);out=[];seen=set();groups={}
    # A repeated visible family must not acquire a constant numerical-rank or
    # position shortcut solely through finite-batch selection. Values remain
    # authored mathematical errors; resample whole instances rather than filler.
    for attempt in range(max(10000,1000*count)):
        if len(out)==count:return out
        record=generate(band,rng.getrandbits(64));edges=vectors(record['generation']['parameters']['points'])
        fingerprint=json.dumps(edges)
        if fingerprint in seen:continue
        coordinates=bank_coordinates(record)
        if coordinates is not None:
            labels=visible_groups(record)
            if any(len(groups.get(label,[]))==1 and any(coordinates[i]==groups[label][0][i] for i in (0,1)) for label in labels):continue
            for label in labels:groups.setdefault(label,[]).append(coordinates)
        seen.add(fingerprint);out.append(record)
    raise RuntimeError('Diverse deterministic batch sampling exhausted')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='hard')
    parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    parser.add_argument('--replay',help='Replay one captured complete source question, evidence only')
    args=parser.parse_args()
    if args.count<1:parser.error('count must be positive')
    records=[source_replay(args.replay,args.seed)] if args.replay else batch('hard' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed)
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
