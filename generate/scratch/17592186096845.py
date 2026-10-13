"""Chain/product-rule source-faithful generator. See adjacent classification and validation.

Sampling extends only numerical coefficients in six complete source templates.
Three slope/radical banks are exact finite replays; their distractor mechanisms
are not inferred from one observation. Hard is unsupported by this version.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import random
import re
import uuid
import sympy as sp

KP_ID = 17592186096845
KP_UUID = '1c269944-636a-50f2-bfc9-c32a7b2e7ca3'
TITLE = 'Calculating a Derivative Using the Chain and Product Rules'
HERE = Path(__file__).with_suffix('')
VERSION = '1.0.0'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'course-academy-generator'))
SUPPORTED_LEVELS = ('easy', 'moderate')
SOURCES = {q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
DEFAULTS = {'q-343332':{'k':4}, 'q-343333':{'k':5}, 'q-343354':{'c':2,'k':6}, 'q-11824':{'k':9}, 'q-2392':{'k':3}, 'q-9942':{'k':5,'b':2}, 'q-2401':{}, 'q-10009':{}, 'q-9944':{}}
VARIABLE = tuple(m for m,p in DEFAULTS.items() if p)
x = sp.Symbol('x', real=True)
a = sp.Symbol('a', positive=True)

def uid(name): return str(uuid.uuid5(uuid.UUID(GENERATOR_UUID), name))
def swap(text, mapping):
    if not mapping:return text
    return re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m[0]],text)

def transform(text, template, p):
    if template in ('q-343332','q-343333','q-11824','q-2392'):
        old={'q-343332':'4','q-343333':'5','q-11824':'9','q-2392':'3'}[template]
        mapping={old:str(p['k'])}
        if template=='q-11824':mapping['10']=str(p['k']+1)
        return swap(text,mapping)
    if template=='q-343354':
        return swap(text,{'12':str(p['c']*p['k']),'2':str(p['c']),'6':str(p['k'])})
    if template=='q-9942':
        # The power 2 and product coefficient 2 stay fixed. Only affine phase changes.
        text=swap(text,{'5':str(p['k'])})
        return text.replace(f"{p['k']}x+2",f"{p['k']}x{p['b']:+d}")
    return text

def model(template,p):
    k=p.get('k'); b=p.get('b');c=p.get('c')
    if template=='q-343332':return sp.exp(x)*sp.sin(k*x),sp.sin(k*x)+k*sp.cos(k*x)
    if template=='q-343333':return sp.exp(k*x)*sp.log(x),k*sp.log(x)+1/x
    if template=='q-343354':return c*x*sp.exp(k*x),c*k*x+c
    if template=='q-11824':return (x+1)*sp.exp(k*x),(k*x+k+1)*sp.exp(k*x)
    if template=='q-2392':return a**(k*x)*sp.tan(x),a**(k*x)*(sp.sec(x)**2+k*sp.log(a)*sp.tan(x))
    if template=='q-9942':return x**2*sp.sin(k*x+b),2*x*sp.sin(k*x+b)+k*x**2*sp.cos(k*x+b)
    if template=='q-2401':return 4*x**2*sp.sqrt(sp.sin(x)),(8*x*sp.sin(x)+2*x**2*sp.cos(x))/sp.sqrt(sp.sin(x))
    if template=='q-10009':return sp.sin(2*x)*sp.cos(3*x),sp.Integer(0)
    if template=='q-9944':return x**2*sp.sin(x)**3,sp.Integer(0)
    raise ValueError(template)

def fingerprint(template,p):
    # Exact mathematical task and requested fragment; ignores seed, choice order, UUIDs.
    function,answer=model(template,p)
    shape='fragment' if template.startswith('q-343') else ('slope@pi/2' if template=='q-10009' else 'slope@0' if template=='q-9944' else 'derivative')
    return hashlib.sha256((sp.srepr(function)+'|'+sp.srepr(answer)+'|'+shape).encode()).hexdigest()

def generate(difficulty,seed=0,template=None,parameters=None,bank_profile=None):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Hard unsupported: no rated source evidence')
    candidates=[m for m in VARIABLE if SOURCES[m][':question/difficulty'][':db/ident']==':question.difficulty/'+difficulty]
    rng=random.Random(seed);template=template or rng.choice(candidates)
    if template not in DEFAULTS or SOURCES[template][':question/difficulty'][':db/ident']!=':question.difficulty/'+difficulty:raise ValueError('Template/level mismatch')
    p=dict(parameters) if parameters is not None else ({'k':rng.choice([3,4,5,6,7,8,9,10,11,12])} if DEFAULTS[template] else {})
    if template=='q-343354' and parameters is None:p['c']=rng.choice([1,2,3,4,5,6])
    if template=='q-9942' and parameters is None:p['b']=rng.choice([-5,-3,-1,0,1,2,3,5])
    if set(p)!=set(DEFAULTS[template]) or any(type(v)!=int for v in p.values()):raise ValueError('Invalid parameter keys/types')
    if p and not 2<=p['k']<=12:raise ValueError('Coefficient sampling bound')
    if template=='q-9942' and p['k']==2:raise ValueError('Swapped coefficients collide with correct choice')
    if template=='q-343354' and not 1<=p['c']<=6:raise ValueError('Scale bound')
    if template=='q-9942' and not -5<=p['b']<=5:raise ValueError('Shift bound')
    profile='blank' if SOURCES[template][':question/answer-fields'][0][':answer-field/type'][':db/ident']==':answer-field.type/blank' else template+'-bank'
    if bank_profile not in (None,profile):raise ValueError('Unknown bank')
    original=SOURCES[template]; fp=fingerprint(template,p);qid=uid('question|'+fp+'|'+profile);fid=uid(qid+'|field')
    f=original[':question/answer-fields'][0];correct=str(f[':answer-field/correct'][':answer/id']);answers=[];correct_id=None
    for old in f[':answer-field/choices']:
        val=transform(old[':answer/value'],template,p);aid=uid(fid+'|'+val)
        answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':val})
        if old[':answer/id']==correct:correct_id=aid
    field={':answer-field/id':fid,':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}
    q={':question/id':qid,':question/problem':transform(original[':question/problem'],template,p),':question/worked-solution':transform(original[':question/worked-solution'],template,p),':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[field]}
    domain='x>0' if template=='q-343333' else 'a>0; cos(x)!=0' if template=='q-2392' else 'sin(x)>0 (differentiable real radical interior)' if template=='q-2401' else 'real x'
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'parameters':p,'parameter_fingerprint':fp,'domains':domain,'source_references':[template],'dependencies':{'sympy':sp.__version__},'plots':'none'}}

def batch(difficulty,count,seed=0):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported level')
    rng=random.Random(seed);pairs=[]
    for m in VARIABLE:
        if SOURCES[m][':question/difficulty'][':db/ident']!=':question.difficulty/'+difficulty:continue
        for k in range(2,13):
            if m=='q-9942' and k==2:continue
            for c in (range(1,7) if m=='q-343354' else [None]):
                for b in (range(-5,6) if m=='q-9942' else [None]):
                    p={'k':k}
                    if c is not None:p['c']=c
                    if b is not None:p['b']=b
                    pairs.append((m,p))
    rng.shuffle(pairs)
    if count>len(pairs):raise ValueError(f'Finite configured parameter space: {len(pairs)}')
    return [generate(difficulty,seed,m,p) for m,p in pairs[:count]]

def markdown(rec):
    q=rec['question'];return q[':question/problem']+'\n\n'+ '\n'.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',required=True);p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');args=p.parse_args()
    rows=batch(args.difficulty,args.count,args.seed);print(json.dumps(rows,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rows))
