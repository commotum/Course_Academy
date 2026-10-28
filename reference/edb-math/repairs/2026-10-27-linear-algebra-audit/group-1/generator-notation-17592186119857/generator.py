#!/usr/bin/env python3
"""Seeded pivot-column basis practice. Runtime is standard library only."""
import argparse
import copy
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

VERSION='1.1.0-notation-v1'
KP = {'db_id':17592186119857,'id':'6f644bed-7adb-5907-87b4-99b1902e7850',
      'title':'Finding a Basis of the Space Spanned by a Set of Vectors by Identifying Pivot Columns'}
SOURCES = {
 'easy':['c69f867a-804d-5cf3-bc38-00ede80f0b28','0e4db7b3-e6f9-5f5c-a603-6b52766bfd31','888a94bc-a946-5c39-ab2a-45c8b3016b1d'],
 'moderate':['6fe4864a-ed27-50fc-8816-ad1ec4b0dfc8','dd91b565-0528-53ef-9896-e748c3fd0d1c','163f4ab1-e459-544e-b3ef-fa78330fc316','f1784b5b-02c0-53d5-a72c-54b398014a93','aae38027-b7af-521b-95e6-7933abfbe980'],
 'hard':['c41cfbf0-e58f-58a2-ace1-4048059e3167']}
CASES = {'easy':[(0,1),(0,2),(1,2)],
         'moderate':[(0,),(1,),(2,),(0,1),(0,2),(1,2)],
         'hard':[(0,1),(0,2),(0,1,2),(0,1,3),(0,2,3),(1,2,3)]}

def tex(x):
    x=F(x)
    if x.denominator==1:return str(x.numerator)
    return ('-' if x<0 else '')+r'\frac{'+str(abs(x.numerator))+'}{'+str(x.denominator)+'}'

def matrix(rows):
    return r'\begin{bmatrix}' + r' \\ '.join(' & '.join(tex(x) for x in row) for row in rows)+r'\end{bmatrix}'

def vector(v):return matrix([[x] for x in v])
def basis(vs):return normalize_tex(r'\mathcal{B}=\left\{'+r',\;'.join(vector(v) for v in vs)+r'\right\}')
def columns(vs):return [list(row) for row in zip(*vs)]
def signature(vs):return tuple(sorted(tuple(F(x) for x in v) for v in vs))

def eliminate(rows):
    """Forward elimination, retaining each row operation and resulting matrix."""
    a=[[F(x) for x in row] for row in rows]; r=0; pivots=[]; steps=[]
    for col in range(len(a[0])):
        found=next((i for i in range(r,len(a)) if a[i][col]),None)
        if found is None:continue
        if found!=r:
            a[r],a[found]=a[found],a[r]
            steps.append((r'R_{'+str(r+1)+r'}\leftrightarrow R_{'+str(found+1)+'}',copy.deepcopy(a)))
        for i in range(r+1,len(a)):
            if not a[i][col]:continue
            factor=a[i][col]/a[r][col]
            a[i]=[x-factor*y for x,y in zip(a[i],a[r])]
            op=r'R_{'+str(i+1)+r'}\leftarrow R_{'+str(i+1)+r'}'+('-' if factor>0 else '+')
            op+=('' if abs(factor)==1 else tex(abs(factor)))+r'R_{'+str(r+1)+'}'
            steps.append((op,copy.deepcopy(a)))
        pivots.append(col);r+=1
        if r==len(a):break
    return a,tuple(pivots),steps

def rank(vs):return len(eliminate(columns(vs))[1]) if vs else 0

def is_basis(vs, original):
    r=rank(original)
    return len(vs)==r and rank(vs)==r and rank(original+vs)==r

def make_vectors(difficulty,pivots,rng):
    m,n={'easy':(3,3),'moderate':(2,3),'hard':(4,4)}[difficulty]
    r=len(pivots); e=[[0]*n for _ in range(m)]
    for i,c in enumerate(pivots):
        e[i][c]=rng.choice([-1,1]) if difficulty=='hard' else rng.choice([-3,-2,-1,1,2,3])
        for j in range(i):e[j][c]=rng.randint(-2,2)
    for c in range(n):
        if c in pivots:continue
        before=[p for p in pivots if p<c]
        if not before:continue
        # A later nonpivot may combine several previous directions, not just one.
        coeff=[rng.choice([-2,-1,1,2]) for _ in before]
        for i in range(m):e[i][c]=sum(k*e[i][j] for k,j in zip(coeff,before))
    a=copy.deepcopy(e)
    if difficulty=='moderate':
        q=rng.choice([-2,-1,1,2]);a[1]=[x+q*y for x,y in zip(e[1],e[0])]
    elif difficulty=='hard':
        # Unit lower-triangular shears retain small integer elimination factors.
        for i in range(1,m):
            co=[rng.choice([-2,-1,1,2]) for j in range(i)]
            a[i]=[e[i][c]+sum(co[j]*e[j][c] for j in range(i)) for c in range(n)]
    return [list(v) for v in zip(*a)]

def bank(vs,pivots,rng,profile):
    """Whole error profiles; every alternative must actually fail to be a basis."""
    correct=[vs[i] for i in pivots]; r=len(pivots); pool={}
    def add(c,kind):
        if not c or len(set(map(tuple,c)))!=len(c) or is_basis(c,vs):return
        sig=signature(c)
        if sig not in pool:pool[sig]=(copy.deepcopy(c),kind)
    for size in range(1,len(vs)+1):
        for ids in itertools.combinations(range(len(vs)),size):
            c=[vs[i] for i in ids]
            add(c, 'incomplete-span' if len(c)<r else 'dependent-originals')
    reduced,_,_=eliminate(columns(vs))
    add([list(v) for v in zip(*reduced) if any(v)],'reduced-columns')
    add([[reduced[i][c] for i in range(len(reduced))] for c in pivots],'reduced-pivot-columns')
    # Single-coordinate transcription mistakes: lost sign, lost coordinate,
    # or a pivot's 1 copied to a zero coordinate. They are not arbitrary offsets.
    for index,v in enumerate(correct):
        for c,x in enumerate(v):
            for new in ([-x,0] if x else [1,-1]):
                changed=copy.deepcopy(correct);changed[index][c]=new
                add(changed,'coordinate-copy')
    # Mistake: take two copies/scalings of the same direction as independent.
    if r>=2:
        for i in range(len(vs)):
            if not any(vs[i]):continue
            for k in [-2,-1,2,3]:
                c=copy.deepcopy(correct);c[-1]=[k*x for x in vs[i]]
                for j in range(r-1):
                    d=copy.deepcopy(c);d[j]=vs[i];add(d,'dependent-scalings')
    entries=list(pool.values());rng.shuffle(entries)
    profiles=[['dependent-originals','incomplete-span','coordinate-copy','dependent-scalings'],
              ['coordinate-copy','dependent-originals','dependent-scalings','incomplete-span'],
              ['reduced-pivot-columns','coordinate-copy','dependent-originals','incomplete-span']]
    chosen=[];used=set()
    def take(test):
        item=next((x for x in entries if signature(x[0]) not in used and test(x)),None)
        if item:chosen.append(item);used.add(signature(item[0]));return True
        return False
    # Cardinality alone must never isolate the key. The rank-one line needs
    # incorrect singleton coordinates; rank-two planes need dependent pairs.
    take(lambda x:len(x[0])==r)
    # Nor can merely matching the listed vectors isolate the key.
    take(lambda x:all(v in vs for v in x[0]))
    for kind in profiles[profile]:
        if len(chosen)==4:break
        take(lambda x:x[1]==kind)
    while len(chosen)<4:
        if not take(lambda x:True):raise ValueError('Insufficient plausible distinct distractors')
    result=[(correct,'correct')]+chosen;rng.shuffle(result)
    return result

def ui_hash(value):
    """Exact unsigned FNV order used by ui/learning.js choiceOrder."""
    n=2166136261
    for c in value:n=((n ^ ord(c))*16777619) & 0xffffffff
    return n

def publication_ids(record):
    """Predict publisher stable IDs for this package's single math-radio shape.

    No normalization/filtering is duplicated here. build() already emits canonical
    prose and TeX; check_delivery independently checks identity parity. These IDs
    let batch construction measure the order the actual UI will display.
    """
    q=record['question'];f=q[':question/answer-fields'][0]
    old_key=f[':answer-field/correct'][1]
    strip=lambda c:{':answer/type':c[':answer/type'],':answer/value':c[':answer/value']}
    k=next(c for c in f[':answer-field/choices'] if c[':answer/id']==old_key)
    payload={':question/problem':q[':question/problem'],':question/answer-fields':[
      {':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'],
       ':answer-field/choices':sorted([strip(c) for c in f[':answer-field/choices']],key=lambda c:json.dumps(c,sort_keys=True)),
       ':answer-field/correct':strip(k)}]}
    digest=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    qid=uuid.uuid5(uuid.UUID(KP['id']),'generated-question:'+digest(payload))
    fid=uuid.uuid5(qid,'field:'+f[':answer-field/key']);q[':question/id']=str(qid);f[':answer-field/id']=str(fid)
    for c in f[':answer-field/choices']:
        was_key=c[':answer/id']==old_key
        c[':answer/id']=str(uuid.uuid5(fid,digest([c[':answer/type'],c[':answer/value']])))
        if was_key:f[':answer-field/correct']=[':answer/id',c[':answer/id']]
    return record

def visible_position(record,item):
    f=record['question'][':question/answer-fields'][0]
    ids=[c[':answer/id'] for c in sorted(f[':answer-field/choices'],key=lambda c:ui_hash(str(item)+':'+f[':answer-field/id']+':'+c[':answer/id']))]
    return ids.index(f[':answer-field/correct'][1])

def build(vs,difficulty,rng,profile=0,replay=None):
    a=columns(vs); echelon,pivots,steps=eliminate(a)
    selected=[vs[i] for i in pivots]
    if replay:
        entries=[(x,'source-replay' if signature(x)!=signature(replay['correct']) else 'correct') for x in replay['bank']]
        if signature(selected)!=signature(replay['correct']):raise ValueError('Source key is not the pivot basis')
    else:entries=bank(vs,pivots,rng,profile)
    names=','.join(r'\mathbf{a}_{'+str(i+1)+'}' for i in range(len(vs)))
    # Two vectors per display row prevents horizontal overflow in the real UI.
    rows=[]
    for i in range(0,len(vs),2):
        rows.append(r'\qquad '.join(r'\mathbf{a}_{'+str(j+1)+'} &='+vector(vs[j]) for j in range(i,min(i+2,len(vs)))))
    prompt='Consider the vectors\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$\n\n'
    prompt+='Find a basis $\\mathcal{B}$ of $S=\\operatorname{Span}\\{'+names+r'\}$ by identifying pivot columns.'
    solution='Place the vectors in the columns of a matrix:\n\n$$\nA='+matrix(a)+'\n$$\n\n'
    if not steps:solution+='This matrix is already in row echelon form.\n\n'
    for op,state in steps:
        solution+='Apply $'+op+'$:\n\n$$\nA\\sim '+matrix(state)+'\n$$\n\n'
    labels=', '.join(str(x+1) for x in pivots)
    refs=r',\;'.join(r'\mathbf{a}_{'+str(i+1)+'}' for i in pivots)
    solution+='The leading nonzero entries are in columns $'+labels+'$. Select the corresponding columns from the **original matrix**, giving $\\mathcal{B}=\\{'+refs+r'\}$:'+'\n\n$$\n'+basis(selected)+'.\n$$\n\n'
    solution+='These pivot columns are linearly independent and span the column space of $A$, which is $S$. The nonpivot columns can be removed without changing the span. Row operations locate the pivot indices; use the original vectors when writing the basis.'
    prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    values=[basis(x) for x,_ in entries]
    identity=json.dumps([VERSION,difficulty,prompt,sorted(values)],sort_keys=True)
    digest=hashlib.sha256(identity.encode()).hexdigest()
    uid=lambda role:str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/basis/'+digest+'/'+role))
    choices=[{':answer/id':uid('choice/'+value),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    index=next(i for i,(x,kind) in enumerate(entries) if kind=='correct')
    record={'knowledge_point':KP.copy(),'question':{':question/id':uid('question'),':question/problem':prompt,
        ':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,
        ':question/answer-fields':[{':answer-field/id':uid('field'),':answer-field/key':'selection',
            ':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,
            ':answer-field/correct':[':answer/id',choices[index][':answer/id']]}]},
        'generation':{'version':VERSION,'template':difficulty+'-pivot-basis','profile':profile,
            'source_question_ids':[replay['source_id']] if replay else SOURCES[difficulty],
            'parameters':{'vectors':vs,'pivot_columns':[i+1 for i in pivots]},
            'choice_errors':[kind for _,kind in entries],'row_operations':[op for op,_ in steps]}}
    return validate_generated_record(publication_ids(record))

def generate(difficulty,count,seed):
    if count<0:raise ValueError('count must be nonnegative')
    rng=random.Random(seed);records=[];seen=set(); schedule=[];position_history={}
    while len(records)<count:
        if not schedule:
            schedule=list(CASES[difficulty]);rng.shuffle(schedule)
        pivots=schedule.pop();profile=len(records)%3
        for attempt in range(10000):
            vs=make_vectors(difficulty,pivots,rng)
            record=build(vs,difficulty,rng,profile)
            semantic=json.dumps(vs)
            # UI sorts by hashed *published* identities, so reordering the raw
            # bank has no effect. Resample complete plausible banks/instances
            # until each visible rank group cycles through all five key positions
            # in the primary preview, with distinct successive keys in two
            # additional contexts. Requiring three simultaneous full cycles can
            # exhaust the small rank-one family, so only primary is a full cycle.
            # The publisher assigns real entity IDs later; no finite batch rule
            # can promise balance for every unknown learner/task identity.
            positions=tuple(visible_position(record,len(records)+1+offset) for offset in (0,5,10))
            used=position_history.setdefault(len(pivots),[set(),set(),set()])
            if semantic not in seen and all(x not in group for x,group in zip(positions,used)):break
        else:raise RuntimeError('Could not obtain another semantic instance')
        for context,(x,group) in enumerate(zip(positions,used)):
            if context:group.clear()
            group.add(x)
            if context==0 and len(group)==5:group.clear()
        seen.add(semantic);record['generation'].update(seed=seed,batch_index=len(records))
        records.append(record)
    return records

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='easy')
    parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    args=parser.parse_args();difficulty='easy' if args.difficulty=='unclassified' else args.difficulty
    print(json.dumps(generate(difficulty,args.count,args.seed),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
