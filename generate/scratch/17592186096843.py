"""Source-faithful chain-rule generator; finite, explicitly bounded slices.

Keep each observed outer exponent, inner slope and complete radio bank fixed.
Vary only the affine shift or one documented polynomial coefficient/constant.
See the adjacent package for full source replay, native grading and capabilities.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import uuid
import sympy as s

KP_ID = 17592186096843
KP_UUID = '0a312840-0d35-50bb-94b3-b04778f4efc3'
TITLE = 'Differentiating a Function Using the Chain Rule and Prime Notation'
HERE = Path(__file__).with_suffix('')
VERSION = '1.0.0'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'course-academy-generator'))
SUPPORTED_LEVELS = ('moderate', 'hard')
SOURCES = {q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
DEFAULTS = {'q-107293':{'b':4}, 'q-342804':{'b':3}, 'q-71954':{'b':-7}, 'q-71956':{'b':2}, 'q-342875':{'c':4}, 'q-342883':{'b':-4}, 'q-342891':{'c':5}}
x = s.Symbol('x', real=True)

def parameters_for(m):
    key=next(iter(DEFAULTS[m]))
    values=range(1,13) if key=='c' else range(1,10) if m=='q-71956' else range(-9,10)
    return [{key:v} for v in values]

def transform(t,m,p):
    if m in ('q-107293','q-342804','q-71954','q-342883'):
        old={'q-107293':'+4','q-342804':'+3','q-71954':'-7','q-342883':'-4'}[m]
        return t.replace(old,format(p['b'],'+d'))
    if m=='q-71956':return t.replace('2-5x',str(p['b'])+'-5x').replace('2+5x',str(p['b'])+'+5x')
    if m=='q-342875':return t.replace('4{x}^{4}',str(p['c'])+'{x}^{4}').replace('16{x}^{3}',str(4*p['c'])+'{x}^{3}')
    if m=='q-342891':return t.replace('+5','+'+str(p['c']))
    raise ValueError(m)

def model(m,p):
    b=p.get('b');c=p.get('c')
    if m=='q-107293':inner=3*x+b;fun=inner**5
    elif m=='q-342804':inner=4*x+b;fun=inner**5
    elif m=='q-71954':inner=8*x+b;fun=inner**4
    elif m=='q-71956':inner=b-5*x;fun=inner**3
    elif m=='q-342875':inner=x**5-c*x**4;fun=inner**2
    elif m=='q-342883':inner=5*x+b;fun=s.sqrt(inner)
    elif m=='q-342891':inner=2*x**4-x**2+c;fun=1/s.sqrt(inner)
    else:raise ValueError(m)
    answer=s.diff(inner,x) if m=='q-342875' else -s.diff(inner,x)/2 if m=='q-342891' else s.diff(fun,x)
    return inner,fun,answer

def task_fingerprint(m,p):
    _,fun,_=model(m,p)
    shape='inner-derivative-fragment' if m=='q-342875' else 'reciprocal-radical-numerator-fragment' if m=='q-342891' else 'full-derivative'
    return hashlib.sha256((s.srepr(s.expand(fun))+'|'+shape).encode()).hexdigest()

def generate(difficulty,seed=0,template=None,parameters=None,bank_profile=None):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Easy unsupported: no complete rated easy source')
    rng=random.Random(seed)
    eligible=[m for m in DEFAULTS if SOURCES[m][':question/difficulty'][':db/ident']==':question.difficulty/'+difficulty]
    m=template or rng.choice(eligible)
    if m not in eligible:raise ValueError('Template/level mismatch')
    p=dict(parameters) if parameters is not None else rng.choice(parameters_for(m))
    if p not in parameters_for(m) or any(type(v)!=int for v in p.values()):raise ValueError('Outside documented finite parameter slice')
    old=SOURCES[m];f=old[':question/answer-fields'][0]
    profile='blank' if f[':answer-field/type'][':db/ident']==':answer-field.type/blank' else m+'-bank'
    if bank_profile not in (None,profile):raise ValueError('Unknown bank profile')
    fp=task_fingerprint(m,p)
    uid=lambda text:str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),text))
    qid=uid('question|'+fp+'|'+profile);fid=uid(qid+'|field|'+f[':answer-field/key'])
    answers=[];correct=None
    for a in f[':answer-field/choices']:
        value=transform(a[':answer/value'],m,p);aid=uid(fid+'|'+value)
        answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
        if a[':answer/id']==f[':answer-field/correct'][':answer/id']:correct=aid
    field={':answer-field/id':fid,':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/correct':[':answer/id',correct],':answer-field/choices':answers}
    q={':question/id':qid,':question/problem':transform(old[':question/problem'],m,p),':question/worked-solution':transform(old[':question/worked-solution'],m,p),':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[field]}
    domain='5x'+format(p['b'],'+d')+'>0' if m=='q-342883' else 'real x; radicand >= c-1/8 > 0' if m=='q-342891' else 'real x'
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'seed':seed,'template':m,'bank_profile':profile,'parameters':p,'parameter_fingerprint':fp,'domains':domain,'source_references':[m],'dependencies':{'sympy':s.__version__},'plots':'none','sampling_policy':'finite shift/coefficient slice; fixed observed outer function and complete source bank'}}

def batch(difficulty,count,seed=0):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported level')
    if type(count)!=int or count<0:raise ValueError('Count must be a nonnegative integer')
    if count==0:return []
    pairs=[(m,p) for m in DEFAULTS if SOURCES[m][':question/difficulty'][':db/ident']==':question.difficulty/'+difficulty for p in parameters_for(m)]
    random.Random(seed).shuffle(pairs)
    result=[];seen=set()
    for m,p in pairs:
        fp=task_fingerprint(m,p)
        if fp in seen:continue
        seen.add(fp);result.append(generate(difficulty,seed,m,p))
        if len(result)==count:break
    return result

def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join(('* ' if a[':answer/id']==f[':answer-field/correct'][1] else '- ')+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',required=True);parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json','markdown'],default='json');parser.add_argument('--output',type=Path);args=parser.parse_args()
    records=batch(args.difficulty,args.count,args.seed)
    text=(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')
