"""Matrix-product dimensions: source-faithful easy/moderate generators.

The three independent dimensions m,n,p range from 1 to 10 and are distinct.
All products are conformable. Forward ordering is easy; reversed ordering is
moderate. Profiles retain entire observed banks. No hard generator is claimed.
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

KP_ID = 17592186100870
KP_UUID = 'f38167e2-3c1d-5c00-9691-ba8e6ac6fdce'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
VERSION = '1.0.0'
SUPPORTED_LEVELS = ('easy', 'moderate')
HERE = Path(__file__).with_suffix('')
SNAPSHOT = json.loads((HERE / 'source.json').read_text())
SOURCES = {q[':question/math-academy-id']: q for q in SNAPSHOT['record'][':knowledge-point/questions']}
DEFAULTS = {
    'q-129461': dict(m=2,n=4,p=6), 'q-129486': dict(m=2,n=8,p=7),
    'q-320315': dict(m=4,n=3,p=7), 'q-320344': dict(m=10,n=5,p=7),
    'q-70702': dict(m=2,n=4,p=5), 'q-70705': dict(m=5,n=2,p=3),
    'q-77473': dict(m=3,n=7,p=5), 'q-129480': dict(m=5,n=7,p=1),
    'q-70703': dict(m=4,n=3,p=6),
}

def level_of(template):
    return SOURCES[template][':question/difficulty'][':db/ident'].split('/')[-1]

def substitute(text, template, parameters):
    """Simultaneous substitution prevents replaced numbers being replaced again."""
    old = {str(v): str(parameters[k]) for k,v in DEFAULTS[template].items()}
    return re.sub(r'\{\{field-[12]\}\}|\d+', lambda m: old.get(m[0],m[0]), text)

def corrected_solution(template):
    text = SOURCES[template][':question/worked-solution']
    if template == 'q-70702':
        # The source's prose and prompt request SR, but its display labels RS.
        text = text.replace('{R}', '{@}').replace('{S}', '{R}').replace('{@}', '{S}')
    return text

def task_key(q):
    text = q[':question/problem']
    dims = [tuple(map(int,x)) for x in re.findall(r'(\d+)\s*\\(?:times|cdot)\s*(\d+)', text)]
    if len(dims) != 2:
        return 'unrecognized:' + hashlib.sha256(text.encode()).hexdigest()
    labels = re.findall(r'\$([A-Z])\$ is a', text)
    # Easy forward questions may list the requested product before the factors.
    target = re.search(r'\$([A-Z]{2})\??\$',text)
    if len(labels) != 2 or target is None:
        return 'unrecognized:' + hashlib.sha256(text.encode()).hexdigest()
    bylabel = dict(zip(labels,dims))
    a,b = [bylabel[c] for c in target[1]]
    # Ignore labels, field type, bank, seed, and option ordering for novelty.
    return json.dumps([a,b])

def generate(difficulty, seed=0, template=None, parameters=None, bank_profile=None):
    if difficulty not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty: '+difficulty)
    rng = random.Random(seed)
    eligible = sorted(t for t in DEFAULTS if level_of(t) == difficulty)
    template = template or rng.choice(eligible)
    if template not in eligible or bank_profile not in (None,template):
        raise ValueError('Template/profile does not support the requested difficulty')
    p = dict(parameters) if parameters is not None else dict(zip(('m','n','p'),rng.sample(range(1,11),3)))
    if parameters is None:
        while (template=='q-129461' and p['p']==5) or (template=='q-70702' and p['m']==3):
            p=dict(zip(('m','n','p'),rng.sample(range(1,11),3)))
    if set(p) != {'m','n','p'} or any(type(v) is not int or not 1<=v<=10 for v in p.values()) or len(set(p.values())) != 3:
        raise ValueError('Dimensions must be distinct integers in 1..10')
    # Exact symbolic shape computation precedes rendering.
    left=sp.MatrixSymbol('L',p['m'],p['n']);right=sp.MatrixSymbol('R',p['n'],p['p'])
    assert (left*right).shape == (p['m'],p['p'])
    source=SOURCES[template]
    problem=substitute(source[':question/problem'],template,p)
    solution=substitute(corrected_solution(template),template,p)
    fields=[]
    # Stable identity includes the full authored bank/layout, never the seed.
    content={'problem':problem,'solution':solution,'difficulty':difficulty,
             'fields':[{ 'key':f[':answer-field/key'], 'type':f[':answer-field/type'][':db/ident'],
                        'values': sorted((a[':answer/type'][':db/ident'],substitute(a[':answer/value'],template,p)) for a in f[':answer-field/choices']),
                        'correct':substitute(f[':answer-field/correct'][':answer/value'],template,p)}
                       for f in sorted(source[':question/answer-fields'],key=lambda f:f[':answer-field/key'])]}
    qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),json.dumps(content,sort_keys=True)))
    for old in sorted(source[':question/answer-fields'],key=lambda f:f[':answer-field/key']):
        fid=str(uuid.uuid5(uuid.UUID(qid),old[':answer-field/key']))
        choices=[];correct=None
        for a in old[':answer-field/choices']:
            value=substitute(a[':answer/value'],template,p)
            aid=str(uuid.uuid5(uuid.UUID(fid),a[':answer/type'][':db/ident']+'|'+value))
            choices.append({':answer/id':aid,':answer/type':a[':answer/type'][':db/ident'],':answer/value':value})
            if a[':answer/id'] == old[':answer-field/correct'][':answer/id']: correct=aid
        if len({(a[':answer/type'],a[':answer/value']) for a in choices}) != len(choices):
            raise ValueError('bank_collision: complete observed profile would have duplicate options')
        fields.append({':answer-field/id':fid,':answer-field/key':old[':answer-field/key'],
                       ':answer-field/type':old[':answer-field/type'][':db/ident'],
                       ':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]})
    return {'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,
                        ':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':fields},
            'knowledge_point':{'id':KP_UUID,'db_id':KP_ID,'title':SNAPSHOT['record'][':knowledge-point/title']},
            'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'seed':seed,'template':template,
                          'bank_profile':template,'parameters':p,'domains':'Distinct integers m,n,p in 1..10; inner dimensions equal',
                          'source_basis':SNAPSHOT['basis'],'source_question':source[':question/id'],
                          'sympy_version':sp.__version__,'solution_correction':template=='q-70702'}}

def batch(difficulty,count,seed=0):
    if difficulty not in SUPPORTED_LEVELS: raise ValueError('Unsupported difficulty: '+difficulty)
    if type(count) is not int or count<0: raise ValueError('Count must be nonnegative')
    rng=random.Random(seed)
    triples=list(itertools.permutations(range(1,11),3));rng.shuffle(triples)
    templates=sorted(t for t in DEFAULTS if level_of(t)==difficulty)
    existing={task_key(q) for q in SOURCES.values()}
    # Canonical example is not a practice inventory item, but also is not novel.
    existing.add(json.dumps([(3,4),(4,2)]))
    result=[]
    for i,triple in enumerate(triples):
        if len(result)==count: break
        try:rec=generate(difficulty,seed,templates[i%len(templates)],dict(zip(('m','n','p'),triple)))
        except ValueError as error:
            if not str(error).startswith('bank_collision:'):raise
            continue
        key=task_key(rec['question'])
        if key in existing:continue
        existing.add(key);result.append(rec)
    if len(result)<count: raise ValueError(f'Finite domain: requested {count}, produced {len(result)} distinct tasks')
    return result

def markdown(rec):
    q=rec['question']
    rows=[q[':question/problem']]
    for f in q[':question/answer-fields']:
        rows.append('\n'+f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']))
        rows.append('Answer: '+next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))
    return '\n\n'.join(rows+[q[':question/worked-solution']])

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',required=True,choices=(*SUPPORTED_LEVELS,'all'))
    ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=('json','markdown'),default='json');args=ap.parse_args()
    levels=SUPPORTED_LEVELS if args.difficulty=='all' else (args.difficulty,)
    records=[r for level in levels for r in batch(level,args.count,args.seed)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
