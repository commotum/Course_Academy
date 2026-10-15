#!/usr/bin/env python3
"""Identify pivot columns in REF. Easy only; no live database operations.

One instructional template, thirteen observed complete bank profiles. Column
substitution is a bijection with increasing pivot targets. Fresh matrices retain
source dimensions/rank and REF; their trailing integer entries are incidental.
Semantic inventory deduplication deliberately ignores those incidental values.
"""
import argparse, hashlib, itertools, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp

PACKAGE = Path(__file__).with_suffix('')
CAPTURE = json.loads((PACKAGE/'source.json').read_text())
SOURCE = CAPTURE['record']
KP_ID = 17592186124477
VERSION = 'pivot-columns-ref-1'
LEVELS = ('easy',)
SOURCES = {q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}

def matrix(text):
    body = re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', text, re.S).group(1)
    return [[int(v.strip()) for v in row.split('&')] for row in body.split(r'\\')]

def pivots(a):
    return tuple(next(j+1 for j,x in enumerate(row) if x) for row in a if any(row))

def tex(a):
    return r'\begin{bmatrix}' + r' \\ '.join(' & '.join(map(str,row)) for row in a) + r'\end{bmatrix}'

def ordinal(n):
    return f'${n}$'+('st' if n==1 else 'nd' if n==2 else 'rd' if n==3 else 'th')

def columns(text, permutation):
    if permutation!=list(range(1,len(permutation)+1)) and re.fullmatch(r'\$\d+\$(?:st|nd|rd|th)[\s\S]*',text) and '\\' not in text:
        indices=sorted(permutation[int(n)-1] for n in re.findall(r'\$(\d+)\$(?:st|nd|rd|th)',text))
        parts=list(map(ordinal,indices))
        result=parts[0] if len(parts)==1 else ' and '.join(parts) if len(parts)==2 else ', '.join(parts[:-1])+', and '+parts[-1]
        return result+(' only' if text.endswith(' only') else '')
    return re.sub(r'\$(\d+)\$(?:st|nd|rd|th)', lambda m:ordinal(permutation[int(m[1])-1]), text)

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def uid(value):
    return str(uuid.uuid5(uuid.UUID(SOURCE[':knowledge-point/id']), digest(value)))

def fingerprint(q):
    a=matrix(q[':question/problem'])
    return digest(['pivot-columns',len(a),len(a[0]),pivots(a)])

def targets(profile):
    a=matrix(SOURCES[profile][':question/problem'])
    return list(itertools.combinations(range(1,len(a[0])+1),len(pivots(a))))

def permutation(profile,target):
    a=matrix(SOURCES[profile][':question/problem']);old=pivots(a);n=len(a[0])
    rest=[j for j in range(1,n+1) if j not in target]
    mapping=dict(zip(old,target));mapping.update(zip((j for j in range(1,n+1) if j not in old),rest))
    return [mapping[j] for j in range(1,n+1)]

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('Unsupported difficulty; see capabilities.json')
    if template not in (None,'pivot-columns-ref'):raise ValueError('Unsupported template')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Unsupported field type')
    rng=random.Random(seed);profile=profile or rng.choice(sorted(SOURCES));src=SOURCES[profile]
    original=matrix(src[':question/problem']);m=len(original);n=len(original[0]);old=pivots(original)
    if parameters is None:
        target=rng.choice(targets(profile));perm=permutation(profile,target)
        a=[[0]*n for _ in range(m)]
        for i,p in enumerate(target):
            a[i][p-1]=rng.choice([v for v in range(-9,10) if v])
            for j in range(p,n):a[i][j]=rng.randint(-9,9)
        parameters={'columns':perm,'matrix':a}
    else:
        parameters=json.loads(json.dumps(parameters));perm=parameters['columns'];a=parameters['matrix']
    assert set(parameters)=={'columns','matrix'} and sorted(perm)==list(range(1,n+1))
    target=tuple(perm[j-1] for j in old)
    assert perm==permutation(profile,target)
    assert target in targets(profile) and len(a)==m and all(len(row)==n for row in a)
    assert all(type(v)==int and -9<=v<=9 for row in a for v in row)
    assert pivots(a)==target and all(any(row) for row in a[:len(target)]) and not any(any(row) for row in a[len(target):])
    # Exact REF and rank are also checked independently in validate.py.
    def render(text):
        text=columns(text,perm)
        return re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}',lambda _:tex(a),text,flags=re.S)
    q={':question/problem':render(src[':question/problem']),':question/worked-solution':render(src[':question/worked-solution']),':question/difficulty':':question.difficulty/easy'}
    sf=src[':question/answer-fields'][0]
    values=[columns(v[':answer/value'],perm) for v in sf[':answer-field/choices']]
    identity=digest([VERSION,q,sorted(values)]);qid=uid(identity);fid=uid([qid,sf[':answer-field/key']])
    answers=[{':answer/id':uid([fid,value]),':answer/type':':answer.type/text',':answer/value':value} for value in values]
    correct=next(a[':answer/id'] for a,s in zip(answers,sf[':answer-field/choices']) if s[':answer/id']==sf[':answer-field/correct'][':answer/id'])
    q.update({':question/id':qid,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':sf[':answer-field/key'],':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]})
    return {'knowledge_point':{'db_id':KP_ID,'id':SOURCE[':knowledge-point/id'],'title':SOURCE[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':'pivot-columns-ref','level':level,'profile':profile,'seed':seed,'parameters':parameters,'mathematical_fingerprint':fingerprint(q),'content_identity':identity,'eligible_for_learning':True,'evidence_only':False,'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'python':sys.version.split()[0],'sympy':sp.__version__}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)

def generate_many(level,count,seed=0,profile=None):
    if level not in LEVELS:raise ValueError('Unsupported difficulty; see capabilities.json')
    if count<0:raise ValueError('count must be nonnegative')
    rng=random.Random(seed);domain=[(p,t) for p in ([profile] if profile else sorted(SOURCES)) for t in targets(p)]
    rng.shuffle(domain);records=[];seen=set()
    for p,target in domain:
        if len(records)>=count:break
        rec=generate(level,seed=seed+len(records),profile=p)
        a=rec['generation']['parameters']['matrix'];n=len(a[0]);a=[[0]*n for _ in a]
        for i,column in enumerate(target):
            a[i][column-1]=rng.choice([v for v in range(-9,10) if v])
            for j in range(column,n):a[i][j]=rng.randint(-9,9)
        rec=generate(level,seed=seed+len(records),profile=p,parameters={'columns':permutation(p,target),'matrix':a})
        fp=fingerprint(rec['question'])
        if fp not in seen:seen.add(fp);records.append(rec)
    if len(records)<count:raise ValueError(f'Finite structural limit {len(records)}; requested {count}. See capabilities.json; shortage remains explicit.')
    return records

def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=LEVELS,default='easy');parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--template',default='pivot-columns-ref');parser.add_argument('--profile',choices=sorted(SOURCES))
    parser.add_argument('--count',type=int,help='Emit distinct structural tasks as an array, up to the documented finite bound')
    parser.add_argument('--format',choices=['json','markdown'],default='json');parser.add_argument('--parameters',type=json.loads)
    args=parser.parse_args()
    if args.count is None:
        r=generate(args.difficulty,args.seed,template=args.template,profile=args.profile,parameters=args.parameters)
    else:
        if args.parameters is not None:parser.error('--parameters is for a single instance')
        if args.template!='pivot-columns-ref':parser.error('Unsupported template')
        r=generate_many(args.difficulty,args.count,args.seed,args.profile)
    print(json.dumps(r,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,r)) if isinstance(r,list) else markdown(r))
