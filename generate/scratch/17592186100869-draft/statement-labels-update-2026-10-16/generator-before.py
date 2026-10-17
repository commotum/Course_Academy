#!/usr/bin/env python3
"""Conformability recognition only; three Boolean checkbox statements.

Backbone: read three displayed arrays; identify their dimensions; for each
ordered pair compare left columns with right rows; box equal inner dimensions;
conclude the complete true-statement subset. No matrix entries are multiplied.
Source layout profiles preserve all three independent false/true banks.
"""
import sys
sys.dont_write_bytecode = True
import argparse, copy, hashlib, itertools, json, random, re, uuid
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import checked_math_content, matrix_operands, matrix_tex, normalize_prose
D=Path(__file__).with_suffix('')
SNAPSHOT=json.loads((D/'source.json').read_text())
KP=SNAPSHOT['record']; VERSION='conformability-checkbox-1'
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
LEVELS=('easy','moderate','hard'); KEYS=('I','II','III')
MAT=re.compile(r'([A-Z])=\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)

def uid(*parts): return str(uuid.uuid5(uuid.NAMESPACE_URL,json.dumps(parts,sort_keys=True,separators=(',',':'))))
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def source_parameters(t):
    q=SOURCES[t]; labels=[]; arrays=[]
    for m in MAT.finditer(q[':question/problem']):
        labels.append(m[1]); arrays.append([[v.strip() for v in r.split('&')] for r in m[2].split(r'\\')])
    products=re.findall(r'The product \$([A-Z])([A-Z])\$',q[':question/problem'])
    return {'arrays':arrays,'products':[[labels.index(a),labels.index(b)] for a,b in products]}
def source_level(t):return SOURCES[t][':question/difficulty'][':db/ident'].split('/')[-1]

def mathematical_task(dims,pairs):
    # Supplied shape multiset and ordered comparison multiset; names, array
    # positions, statement order, entries and profile are presentation aliases.
    return [sorted(dims),sorted((dims[i],dims[j]) for i,j in pairs)]
def shape(a): return (len(a),len(a[0]))
def validate_parameters(level,t,p,raw=False):
    if set(p)!={'arrays','products'}: raise ValueError('Expected arrays and products')
    arrays=p['arrays']; pairs=p['products']
    if not isinstance(arrays,list) or len(arrays)!=3: raise ValueError('Exactly three arrays')
    for a in arrays:
        if not isinstance(a,list) or not a or not isinstance(a[0],list) or not a[0] or len({len(r) for r in a})!=1:raise ValueError('Rectangular nonempty arrays required')
        if any(not isinstance(v,(int,str)) or not re.fullmatch(r'-?\d+',str(v)) or abs(int(v))>9 for row in a for v in row):raise ValueError('Integer entries -9..9')
        if max(shape(a))>5 or len(a)*len(a[0])>20:raise ValueError('Dimension maximum 5, cell maximum 20')
    if not isinstance(pairs,list) or len(pairs)!=3 or len({tuple(x) for x in pairs})!=3 or any(not isinstance(x,list) or len(x)!=2 or any(type(i)!=int or i not in range(3) for i in x) or x[0]==x[1] for x in pairs):raise ValueError('Three distinct ordered pairs of different factors')
    dims=list(map(shape,arrays))
    if raw:return p
    if level=='easy':
        if any(max(x)>4 or (min(x)<2 and not (t=='q-22063' and i==2 and x[1]==1 and x[0]>=2)) for i,x in enumerate(dims)):raise ValueError('Easy normal: ordinary matrices dimensions 2..4; source q-22063 retains last column-vector role')
    elif level=='moderate':
        roles=[r==1 for r,c in map(shape,source_parameters(t)['arrays'])]
        if any((r!=1 if roles[i] else r<2) or c<2 for i,(r,c) in enumerate(dims)):raise ValueError('Moderate normal: preserve source row-vector roles, dimensions 2..5 otherwise')
    else:
        if sorted([r==1 for r,c in dims]).count(True)!=1 or sum(c==1 for r,c in dims)!=1 or any(r==c for r,c in dims):raise ValueError('Hard: one row vector, one column vector, one nonsquare ordinary matrix')
        row=next(i for i,(r,c) in enumerate(dims) if r==1);col=next(i for i,(r,c) in enumerate(dims) if c==1)
        if dims[row][1]==dims[col][0]:raise ValueError('Hard vector lengths distinct to require order discrimination')
        if [row,col] not in pairs or [col,row] not in pairs:raise ValueError('Hard must assess both vector orders')
    return p

def conclusion(truth):
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
    stages.append(conclusion(truth))
    return '\n\n'.join(stages),truth

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,bank_profile=None):
    if level not in LEVELS:raise ValueError('Unknown level')
    if field_type and field_type.split('/')[-1]!='checkbox':raise ValueError('Only checkbox supported')
    if bank_profile:
        if profile and profile!=bank_profile:raise ValueError('Conflicting profiles')
        profile=bank_profile
    rng=random.Random(seed)
    eligible=[t for t in SOURCES if source_level(t)==level] if level!='hard' else ['mixed-orientations']
    template=template or rng.choice(eligible)
    if template not in eligible:raise ValueError('Template/level mismatch')
    raw=bool(profile and profile.startswith('raw-'))
    if raw and (template not in SOURCES or profile!='raw-'+template):raise ValueError('Raw profile mismatch')
    if profile not in (None,'boolean-pairs','raw-'+template):raise ValueError('Unknown complete profile')
    profile=profile or 'boolean-pairs'
    t='q-42381' if template=='mixed-orientations' else template
    labels=[m[1] for m in MAT.finditer(SOURCES[t][':question/problem'])]
    if parameters is None:
        # Whole Boolean bank is fixed before parameters. No option fallback.
        if raw:raise ValueError('Raw replay requires explicit parameters')
        if level=='easy':
            dims=[(rng.randint(2,4),rng.randint(2,4)) for _ in range(3)]
            if t=='q-22063':dims[2]=(rng.randint(2,4),1)
        elif level=='moderate':
            roles=[r==1 for r,c in map(shape,source_parameters(t)['arrays'])]
            ordinary=[x for x in itertools.product(range(2,6),repeat=2) if x[0]*x[1]<=20]
            dims=[(1,rng.randint(2,5)) if roles[i] else rng.choice(ordinary) for i in range(3)]
        else:
            n,m=rng.sample(range(2,6),2); third=rng.choice([x for x in itertools.permutations(range(2,6),2)]);dims=[(1,n),(m,1),third];rng.shuffle(dims)
        pairs=rng.sample(list(itertools.permutations(range(3),2)),3)
        if level=='hard':
            a=next(i for i,x in enumerate(dims) if x[0]==1);b=next(i for i,x in enumerate(dims) if x[1]==1)
            pairs=[(a,b),(b,a),rng.choice([x for x in itertools.permutations(range(3),2) if x not in [(a,b),(b,a)]])];rng.shuffle(pairs)
        parameters={'arrays':[[[rng.randint(-9,9) for _ in range(c)] for _ in range(r)] for r,c in dims],'products':list(map(list,pairs))}
    p=validate_parameters(level,t,copy.deepcopy(parameters),raw)
    arrays,pairs=p['arrays'],p['products']
    oldpairs=source_parameters(t)['products'];prompt=SOURCES[t][':question/problem']
    ai=iter(zip(labels,arrays));prompt=MAT.sub(lambda _: next_matrix(ai),prompt)
    counter=iter(pairs)
    prompt=re.sub(r'(The product \$)[A-Z]{2}(\$)',lambda m:m[1]+''.join(labels[x] for x in next(counter))+m[2],prompt)
    if not raw and t=='q-42374':
        prompt=prompt.replace('following statement are','following statements are')
        prompt=re.sub(r'(?m)^(I{1,3})\. (The product .*?)$',lambda m:'- **'+m[1]+'.** '+m[2],prompt)
    worked,truth=solution(t,labels,arrays,pairs,raw)
    prompt=normalize_prose(prompt);worked=normalize_prose(worked)
    # Identity ignores shuffle/seed but includes every rendered component and bank.
    signature=digest([VERSION,level,prompt,worked,[(k,truth[i],['false','true']) for i,k in enumerate(KEYS)]])
    q={':question/id':uid(signature),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[]}
    for k,ok in zip(KEYS,truth):
        fid=uid(signature,k); choices=[{':answer/id':uid(fid,v),':answer/type':':answer.type/text',':answer/value':v} for v in ['false','true']]
        q[':question/answer-fields'].append({':answer-field/id':fid,':answer-field/key':k,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid,str(ok).lower())]})
    # Keep replay and identity inputs stable; let learner-facing operands wrap
    # independently instead of requiring one wide three-matrix display.
    if not raw:
        end=prompt.index('$$',2)+2
        q[':question/problem']=matrix_operands([m[0] for m in MAT.finditer(prompt[:end])])+prompt[end:]
    dims=list(map(shape,arrays))
    return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'level':level,'seed':seed,'template':template,'profile':profile,'parameters':p,'task_fingerprint':digest(mathematical_task(dims,pairs)),'content_fingerprint':signature,'source_basis':SNAPSHOT['basis'],'source_lineage':SNAPSHOT['lineage'],'source_ids':[t] if template!='mixed-orientations' else [],'authored_extension':template=='mixed-orientations','eligible_for_learning':not raw,'evidence_only':raw}}

def next_matrix(iterator):
    label,array=next(iterator);return label+'='+matrix_tex(array)

# Easy: three ordinary arrays, three independent ordered comparisons.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: row-vector recognition alongside ordinary arrays; same comparison rule.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard authored: one row and one column vector, both orders assessed; no new operation.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(rec):
    q=rec['question'];g=rec['generation'];rows=[f"### {g['level']} / {g['template']} / {g['profile']}",q[':question/problem']]
    for f in q[':question/answer-fields']:
        rows.append(f"Field {f[':answer-field/key']} ({f[':answer-field/type']})")
        for a in f[':answer-field/choices']:rows.append('- '+a[':answer/value']+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else ''))
    rows.extend(['Worked solution',q.get(':question/worked-solution','[raw worked solution absent]')]);return '\n\n'.join(rows)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('markdown','json'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    out=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (LEVELS if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(out,indent=2) if args.format=='json' else '\n\n'.join(map(markdown,out)))
