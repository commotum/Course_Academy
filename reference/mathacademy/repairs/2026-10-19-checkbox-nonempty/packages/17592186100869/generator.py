#!/usr/bin/env python3
"""Seeded conformability recognition, adapted from supplied existing entrypoint.
No database access or generated assets. Source replay uses original parameters.
"""
import sys
sys.dont_write_bytecode = True
import argparse, copy, hashlib, itertools, json, random, re, uuid
from pathlib import Path
from math_format import checked_math_content, matrix_operands, matrix_tex, normalize_prose
SNAPSHOT=json.loads(Path(__file__).with_name('source-data.json').read_text())
KP=SNAPSHOT['record']; VERSION='conformability-portable-3'
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
LEVELS=('easy','moderate'); KEYS=('I','II','III')
MAT=re.compile(r'([A-Z])=\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def ident(x): return x[':db/ident'] if isinstance(x,dict) else x
def uid(*parts): return str(uuid.uuid5(uuid.NAMESPACE_URL,json.dumps(parts,sort_keys=True,separators=(',',':'))))
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def source_parameters(t):
    q=SOURCES[t]; labels=[]; arrays=[]
    for m in MAT.finditer(q[':question/problem']):
        labels.append(m[1]); arrays.append([[v.strip() for v in r.split('&')] for r in m[2].split(r'\\')])
    products=re.findall(r'matrices \$([A-Z])\$ and \$([A-Z])\$ are',q[':question/worked-solution'])
    assert len(products)==3
    return {'arrays':arrays,'products':[[labels.index(a),labels.index(b)] for a,b in products]}
def source_level(t):return ident(SOURCES[t][':question/difficulty']).split('/')[-1]

def mathematical_task(dims,pairs):
    # Supplied shape multiset and ordered comparison multiset; names, array
    # positions, statement order, entries and profile are presentation aliases.
    return [sorted(dims),sorted((dims[i],dims[j]) for i,j in pairs)]
def shape(a): return (len(a),len(a[0]))
def conclusion(truth,products=None):
    if products is not None:
        yes=[p for p,b in zip(products,truth) if b]
        no=[p for p,b in zip(products,truth) if not b]
        def sentence(names,defined):
            subject=('The product ' if len(names)==1 else 'The products ')+' and '.join('$'+p+'$' for p in names)
            return subject+(' is ' if len(names)==1 else ' are ')+('well defined.' if defined else 'undefined.')
        return ' '.join(sentence(names,defined) for names,defined in [(yes,True),(no,False)] if names)
    yes=[k for k,b in zip(KEYS,truth) if b]; no=[k for k,b in zip(KEYS,truth) if not b]
    if len(yes)==3:return 'We conclude that all three statements are true.'
    if not yes:return 'We conclude that all three statements are false.'
    def words(a):return ('statement '+a[0] if len(a)==1 else 'statements '+' and '.join(a))
    return 'Therefore, '+words(yes)+(' is true' if len(yes)==1 else ' are true')+', while '+words(no)+(' is false.' if len(no)==1 else ' are false.')

def solution(t,labels,arrays,pairs,raw):
    dims=list(map(shape,arrays)); anchor=SOURCES[t][':question/worked-solution']
    opening=anchor.split('\n\n')[0]
    old=source_parameters(t); olddims=list(map(shape,old['arrays']))
    # Entire dimension+object components are slots; numbers elsewhere never replaced.
    for label,(r,c),(a,b) in zip(labels,dims,olddims):
        pat=r'\$'+label+r'\$ is a \$'+str(a)+r'\\times '+str(b)+r'\$ (?:matrix|row vector|column vector)'
        noun='row vector' if r==1 else 'column vector' if c==1 else 'matrix'
        opening=re.sub(pat,lambda _:f'${label}$ is a ${r}\\times {c}$ {noun}',opening,count=1)
    stages=[opening];truth=[]
    for n,(i,j) in enumerate(pairs):
        a,b=labels[i],labels[j];r,c=dims[i];s,u=dims[j];ok=c==s;truth.append(ok)
        # Punctuation variants are source layout evidence, not new mathematics.
        comma=('$,' if t=='q-42375' and n>0 else ',$')
        lead=('There are ' if n==0 else 'On the other hand, there are ' if n==1 else 'Finally, there are ')
        source_stage=anchor.split('\n\n')[1+2*n]
        rowword='row' if raw and re.search(r'\$\d+\$ row in',source_stage) and s==1 else 'rows'
        text=lead+f'${c}$ columns in ${a}$ and ${s}$ {rowword} in ${b}.$ '
        text+=f'Since the number of columns in ${a}$ '+('equals' if ok else 'does **not** equal')+f' the number of rows in ${b}'+comma+f' the matrices ${a}$ and ${b}$ are '+('' if ok else '**not** ')+'conformable for multiplication:'
        if not raw:
            text=text.replace('There are $1$ columns','There is $1$ column').replace('there are $1$ columns','there is $1$ column').replace('$1$ rows','$1$ row')
        if ok: eq=f'{{{a}}}_{{{r}\\times '+r'\boxed{\text{'+str(c)+r'}}}{\times }_{✓}'+f'{{{b}}}_{{'+r'\boxed{\text{'+str(s)+r'}}\times '+str(u)+r'}=\text{well defined}'
        else:eq=f'{{{a}}}_{{{r}\\times {c}}}'+r'{\times }_{\ne }'+f'{{{b}}}_{{{s}\\times {u}}}'+r'=\text{undefined}'
        stages.extend([text,'$$\n'+eq+'\n$$'])
    stages.append(conclusion(truth,None if raw else [labels[i]+labels[j] for i,j in pairs]))
    return '\n\n'.join(stages),truth

RADIO_BANK=['II only','I and II only','I and III only','III only','II and III only']
def subset_value(truth):
    yes=[k for k,b in zip(KEYS,truth) if b]
    return ' and '.join(yes)+(' only' if len(yes)<3 else '')
def orientation(dims):
    return (sum(r==1 for r,c in dims),sum(c==1 for r,c in dims))
def masks(t):
    if t=='q-129428':return [(False,True,False),(True,True,False),(True,False,True),(False,False,True),(False,True,True)]
    limit=2 if orientation(list(map(shape,source_parameters(t)['arrays'])))[0]==2 else 3
    return [x for x in itertools.product((False,True),repeat=3) if 0<sum(x)<=limit]
def validate_parameters(level,t,p):
    if set(p)!={'arrays','products'}:raise ValueError('Expected arrays and products')
    arrays=p['arrays'];pairs=p['products']
    if len(arrays)!=3:raise ValueError('Exactly three arrays')
    for a in arrays:
        if not a or not a[0] or len({len(row) for row in a})!=1:raise ValueError('Nonempty rectangular arrays')
        if any(not re.fullmatch(r'-?\d+',str(x)) or abs(int(x))>9 for row in a for x in row):raise ValueError('Small integer entries')
    if len(pairs)!=3 or len(set(map(tuple,pairs)))!=3 or any(len(x)!=2 or any(type(i)!=int or i not in range(3) for i in x) or x[0]==x[1] for x in pairs):raise ValueError('Three distinct ordered pairs')
    dims=list(map(shape,arrays)); original=list(map(shape,source_parameters(t)['arrays']))
    if any(r==c==1 for r,c in dims):raise ValueError('No scalar arrays')
    if orientation(dims)!=orientation(original):raise ValueError('Preserve orientation counts, allow reassignment')
    if any(max(x)>(4 if level=='easy' else 5) or r*c>20 for x in dims for r,c in [x]):raise ValueError('Dimension bound')
    truth=tuple(dims[i][1]==dims[j][0] for i,j in pairs)
    if truth not in masks(t):raise ValueError('Unsupported subset for source bank/profile')
    return p

def sample(t,level,rng,truth):
    # Choose decision mask before compatible dimensions, pairs, and irrelevant entries.
    original=list(map(shape,source_parameters(t)['arrays'])); roles=[('row' if r==1 else 'col' if c==1 else 'matrix') for r,c in original]
    hi=4 if level=='easy' else 5
    for attempt in range(1,20001):
        rng.shuffle(roles);dims=[]
        for role in roles:
            r,c=rng.randint(2,hi),rng.randint(2,hi)
            if role=='row':r=1
            if role=='col':c=1
            dims.append((r,c))
        if any(r*c>20 for r,c in dims):continue
        pairs=rng.sample(list(itertools.permutations(range(3),2)),3)
        if tuple(dims[i][1]==dims[j][0] for i,j in pairs)!=truth:continue
        arrays=[[[rng.randint(-9,9) for _ in range(c)] for _ in range(r)] for r,c in dims]
        return {'arrays':arrays,'products':list(map(list,pairs))},attempt
    raise RuntimeError('Compatible dimension sampling exhausted')

@checked_math_content
def generate(level='easy',seed=0,template=None,parameters=None,replay=False,decision=None):
    if level not in LEVELS:raise ValueError('Unsupported difficulty: '+level)
    rng=random.Random(seed);eligible=[t for t in SOURCES if source_level(t)==level]
    t=template or rng.choice(eligible)
    if t not in eligible:raise ValueError('Template difficulty mismatch')
    attempts=0
    if parameters is None:
        truth=tuple(decision) if decision is not None else rng.choice(masks(t))
        if truth not in masks(t):raise ValueError('Ineligible decision')
        parameters,attempts=sample(t,level,rng,truth)
    p=validate_parameters(level,t,copy.deepcopy(parameters));arrays=p['arrays'];pairs=p['products']
    labels=[m[1] for m in MAT.finditer(SOURCES[t][':question/problem'])]
    dims=list(map(shape,arrays));truth=[dims[i][1]==dims[j][0] for i,j in pairs]
    names=[labels[i]+labels[j] for i,j in pairs];radio=t=='q-129428'
    prompt=matrix_operands([label+'='+matrix_tex(a) for label,a in zip(labels,arrays)])
    prompt+='\n\nWhich of the following statements are true regarding the matrices $'+labels[0]+','+labels[1]+',$ and $'+labels[2]+'?$'
    if radio:prompt+='\n\n'+'\n\n'.join(k+'. The product $'+name+'$ is well defined' for k,name in zip(KEYS,names))
    else:prompt+='\n\nSelect all that apply.'
    worked,_=solution(t,labels,arrays,pairs,False)
    if radio:worked=worked.rsplit('\n\n',1)[0]+'\n\n'+conclusion(truth)
    prompt=normalize_prose(prompt);worked=normalize_prose(worked)
    signature=digest([VERSION,level,prompt,worked,truth])
    q={':question/id':uid(signature),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[]}
    bank=RADIO_BANK[:] if radio else ['false','true']
    if radio and not replay:rng.shuffle(bank)
    fields=[('selection',subset_value(truth))] if radio else [('The product $'+name+'$ is well defined.',str(ok).lower()) for name,ok in zip(names,truth)]
    for key,value in fields:
        fid=uid(signature,key)
        choices=[{':answer/id':uid(fid,v),':answer/type':':answer.type/text',':answer/value':v} for v in bank]
        q[':question/answer-fields'].append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+('radio' if radio else 'checkbox'),':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid,value)]})
    if replay and not radio:
        order=[f[':answer-field/key'] for f in SOURCES[t][':question/answer-fields']]
        q[':question/answer-fields'].sort(key=lambda f:order.index(f[':answer-field/key']))
    return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'level':level,'seed':seed,'template':t,'profile':('radio-subsets' if radio else 'boolean-pairs'),'parameters':p,'truth':truth,'sampling_attempts':attempts,'task_fingerprint':digest(mathematical_task(dims,pairs)),'source_ids':[t],'source_basis':SNAPSHOT['basis'],'source_lineage':SNAPSHOT['lineage'],'replay':replay}}

def replay_source(t):return generate(source_level(t),template=t,parameters=source_parameters(t),replay=True)

# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'hard'),default='easy');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--template');a=ap.parse_args()
    if a.difficulty not in LEVELS:ap.error('hard is unsupported: no supplied source practice evidence')
    if a.count<0:ap.error('count must be nonnegative')
    print(json.dumps([generate(a.difficulty,a.seed+i,template=a.template) for i in range(a.count)],indent=2))
