#!/usr/bin/env python3
"""Bounded reciprocal integration generator; pure, seeded, no database writes.

Four frozen complete source profiles, four mathematical prompt structures. All
are easy. Unobserved levels and ambiguous/incomplete source banks fail closed.
Task identity is the exact coefficient in c/x, independent of profile and seed.
"""
import argparse
import hashlib
import itertools
import json
import random
import re
import uuid
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError:
    import os,sys
    runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])

KP_ID=17592186105715
KP_UUID='cf98ee24-7774-5674-8a1e-63f4f6d225c0'
TITLE='Integrating a Reciprocal Function'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='1.0.0'
SOURCE_BASIS=1921
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SUPPORTED_LEVELS=('easy',)
HERE=Path(__file__).with_suffix('')
TEMPLATES=json.loads((HERE/'templates.json').read_text())
X=sp.Symbol('x',real=True)
C=sp.Symbol('C',real=True)

def clean(text,answer=False):
    if answer:text=text.replace('\\\\','\\').replace(r'\u2061','')
    text=text.replace('⁡','').replace(r'\operatorname{ln}',r'\ln')
    return re.sub(r'(?<![a-z\\])ln',lambda _:r'\ln',text)

def render(text,p,answer=False):
    for k,v in p.items():text=text.replace('@@'+k+'@@',str(v))
    if '@@' in text:raise ValueError('Unfilled parameter slot')
    return clean(text,answer)

def coefficient(kind,p):
    if kind=='integer':return sp.Integer(p['n'])
    if kind=='reciprocal':return sp.Rational(1,p['n'])
    if kind=='radical':return 1/sp.sqrt(p['n'])
    if kind=='negative_radical':return -1/sp.sqrt(p['n'])
    if kind=='negative_rational':return -sp.Rational(p['a'],p['b'])
    raise ValueError('Unknown structure')

def domain(kind):
    if kind=='negative_rational':
        return [{'a':a,'b':b} for a in range(2,6) for b in range(2,10) if sp.gcd(a,b)==1 and a!=b]
    values=range(2,13)
    if kind in ('radical','negative_radical'):values=[n for n in values if int(sp.sqrt(n))**2!=n]
    return [{'n':n} for n in values]

def fingerprint_coefficient(c):return sp.srepr(sp.simplify(c))
def uid(text):return str(uuid.uuid5(uuid.UUID(KP_UUID),text))

def generate(level,seed=0,template=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
    if profile is not None:
        if template and template!=profile:raise ValueError('Profile mismatch')
        template=profile
    rng=random.Random(seed)
    template=template or rng.choice(list(TEMPLATES))
    if template not in TEMPLATES:raise ValueError('Unsupported source profile')
    t=TEMPLATES[template]
    p=dict(parameters) if parameters is not None else dict(rng.choice(domain(t['kind'])))
    if any(type(v)!=int for v in p.values()) or p not in domain(t['kind']):raise ValueError('Outside frozen sampling domain')
    c=coefficient(t['kind'],p)
    fp=fingerprint_coefficient(c)
    problem=render(t['problem'],p)
    solution=render(t['solution'],p)
    values=[render(v,p,True) for v in t['values']]
    # Different complete authored banks have distinct record identities, but
    # replenishment still deduplicates their mathematical tasks by coefficient.
    key=json.dumps([VERSION,fp,template,values],separators=(',',':'))
    qid=uid('question:'+key);fid=uid('field:'+qid+':selection')
    answers=[{':answer/id':uid('answer:'+fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':t['field_key'],':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[t['correct_index']][':answer/id']]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':template,'bank_profile':template,'parameters':p,'parameter_fingerprint':fp,'coefficient':str(c),'domains':['x>0','x<0'],'source_basis':SOURCE_BASIS,'lineage':LINEAGE,'source_questions':[template],'dependencies':{'sympy':sp.__version__},'plot_requirements':'none'}}

def batch(level,count,seed):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
    if type(count)!=int or count<0:raise ValueError('Nonnegative count required')
    pool=[(mid,p) for mid,t in TEMPLATES.items() for p in domain(t['kind'])]
    random.Random(seed).shuffle(pool)
    result=[];seen=set()
    for mid,p in pool:
        r=generate(level,seed,mid,p);fp=r['generation']['parameter_fingerprint']
        if fp in seen:continue
        seen.add(fp);result.append(r)
        if len(result)==count:break
    return result if count else []

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--count',type=int,default=5);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');a.add_argument('--template')
    p=a.parse_args()
    rows=batch(p.difficulty,p.count,p.seed) if not p.template else [generate(p.difficulty,p.seed,p.template)]
    print(json.dumps(rows,indent=2) if p.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
