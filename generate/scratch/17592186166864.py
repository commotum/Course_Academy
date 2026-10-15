"""Easy conservative-field parameter problems, eight source-preserving banks.

Each template has one bounded coefficient/frequency slot. No new operations,
fields, solution stages or plots are introduced. See the adjacent extraction.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186166864
KP_UUID='d8d73fd7-cdeb-59f1-a84c-aab6defb3aa3'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'conservative-field-generator-v1'))
VERSION='1.0.0'
SUPPORTED_LEVELS=('easy',)
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
EXCLUDED=('q-104412','q-168600')
CASES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions'] if q[':question/math-academy-id'] not in EXCLUDED}
DEFAULTS={'q-123996':2,'q-104410':1,'q-104414':1,'q-123993':1,'q-123998':1,'q-124000':4,'q-98946':1,'q-123999':3}
DOMAINS={sid:list(range(1,8)) for sid in CASES}
DOMAINS['q-123996']=list(range(2,10))
DOMAINS['q-124000']=list(range(3,10))
DOMAINS['q-123999']=list(range(3,10))

def tex(v): return sp.latex(sp.sympify(v),fold_short_frac=False)
def substitutions(text,mapping):
    return re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m[0]],text)
def render(sid,n,text):
    if n==DEFAULTS[sid]:return text
    if sid=='q-123996':return substitutions(text,{'2a':f'{n}a',r'-\frac{1}{2}':tex(-sp.Rational(1,n))})
    if sid=='q-104410':return substitutions(text,{'2x':f'{2*n}x','3{x}':f'{3*n}{{x}}','6x':f'{6*n}x'})
    if sid=='q-104414':return text.replace('+1',f'+{n}')
    if sid=='q-123993':return substitutions(text,{'{y}^{3}':f'{n}{{y}}^{{3}}','3x{y}^{2}':f'{3*n}x{{y}}^{{2}}','3{y}^{2}':f'{3*n}{{y}}^{{2}}'})
    if sid=='q-123998':return substitutions(text,{'{y}^{2}':f'{n}{{y}}^{{2}}','2y(1-a)':f'2y({n}-a)','1-a':f'{n}-a','2y':f'{2*n}y','a & =1':f'a & ={n}','a=1':f'a={n}'})
    if sid=='q-124000':return substitutions(text,{'4':str(n),'8':str(2*n)})
    if sid=='q-98946':return text.replace(r'\pi',str(n)+r'\pi')
    if sid=='q-123999':return text.replace('3',str(n))
    raise ValueError(sid)

def bank(sid,n):
    # Complete observed banks; constants retained when their error mechanism is unresolved.
    if sid=='q-123996':return [sp.Rational(1,n),-1,n,-n,-sp.Rational(1,n)],-sp.Rational(1,n)
    if sid in ('q-104410','q-104414','q-123993'):
        f=CASES[sid][':question/answer-fields'][0]
        return [a[':answer/value'] for a in f[':answer-field/choices']],f[':answer-field/correct'][':answer/value']
    if sid=='q-123998':return [sp.Rational(n,4),2*n,sp.Rational(n,2),4*n,n],n
    if sid=='q-124000':return [n,sp.Rational(2,n),sp.Rational(n,2),sp.Rational(1,n),2*n],n
    if sid=='q-98946':return [0,n*sp.pi,-1,-n*sp.pi,1],0
    if sid=='q-123999':return [n,n-1,1,-n,-1],-n

def fingerprint(q):
    # Prompt content only: seeds, UUIDs, solutions and option order cannot establish novelty.
    return hashlib.sha256(re.sub(r'\s+','',q[':question/problem']).encode()).hexdigest()

def generate(difficulty='easy',seed=0,template=None,parameters=None):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    rng=random.Random(seed);sid=template or rng.choice(list(CASES));n=parameters if parameters is not None else rng.choice(DOMAINS[sid])
    assert n in DOMAINS[sid]
    source=CASES[sid];f=source[':question/answer-fields'][0]
    values,correct=bank(sid,n)
    values=[v if isinstance(v,str) else tex(v) for v in values];correct=correct if isinstance(correct,str) else tex(correct)
    if n==DEFAULTS[sid]:
        values=[a[':answer/value'] for a in f[':answer-field/choices']];correct=f[':answer-field/correct'][':answer/value']
    assert len(values)==len(set(values))==5 and correct in values
    problem=render(sid,n,source[':question/problem']);solution=render(sid,n,source[':question/worked-solution'])
    qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),json.dumps([VERSION,sid,n,values])))
    fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==correct)]}
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[field]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE[':knowledge-point/title']},'question':q,'generation':{'generator_id':GENERATOR_UUID,'generator_version':VERSION,'seed':seed,'template':sid,'parameters':n,'bank_profile':sid,'source_question_id':source[':question/id'],'source_basis':2713,'dependencies':{'sympy':sp.__version__},'assets':[],'mathematical_fingerprint':fingerprint(q)}}

def batch(difficulty,count,seed=0):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    pairs=[(sid,n) for sid in CASES for n in DOMAINS[sid]];random.Random(seed).shuffle(pairs)
    if count>len(pairs):raise ValueError(f'Finite sampling policy has {len(pairs)} distinct instances; requested {count}')
    return [generate(difficulty,seed,sid,n) for sid,n in pairs[:count]]
def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--template');args=p.parse_args()
    records=batch(args.difficulty,args.count,args.seed) if not args.template else [generate(args.difficulty,args.seed,args.template)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
