#!/usr/bin/env python3
"""Bounded source-profile generator for integration with logarithmic constants."""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError:
    import os,sys
    runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
KP_ID=17592186105720
KP_UUID='df7dddc6-a4fd-5b1b-9b73-8528e5224ca9'
TITLE='Integrating a Reciprocal Function and Simplifying the Arbitrary Constant Using the Laws of Logarithms'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='1.0.0'
SOURCE_BASIS=1935
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SUPPORTED_LEVELS=('moderate','hard')
HERE=Path(__file__).with_suffix('')
TEMPLATES=json.loads((HERE/'templates.json').read_text())
X=sp.Symbol('x',real=True)
K=sp.Symbol('K',positive=True)
def clean(text,answer=False):
    text=text.replace('⁡','').replace(r'\operatorname{ln}',r'\ln')
    text=re.sub(r'(?<![a-z\\])ln',lambda _:r'\ln',text)
    return re.sub(r'\\ln(?=[A-Za-z])',lambda _:r'\ln ',text)
def domain(kind):
    if kind=='square':return [{'n':n} for n in range(3,32,2)]
    if kind=='linear':return [{'n':n} for n in range(2,17)]
    d=int(kind[-1]);return [{'n':n} for n in range(d+1,32) if sp.gcd(n,d)==1]
def integrand(kind,p):
    n=p['n']
    if kind=='square':return (1+sp.Rational(n,2)/X)**2
    if kind=='linear':return n-1/X
    return (-1 if kind.startswith('negative') else 1)*sp.Rational(n,int(kind[-1]))/X
def fingerprint_expression(e):return sp.srepr(sp.cancel(e))
def uid(text):return str(uuid.uuid5(uuid.UUID(KP_UUID),text))
def render(text,p):
    return clean(text.replace('@@square@@',str(p['n']**2)).replace('@@n@@',str(p['n'])))
def generate(level,seed=0,template=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
    if profile is not None:
        if template is not None and template!=profile:raise ValueError('Profile mismatch')
        template=profile
    rng=random.Random(seed)
    template=template or rng.choice([k for k,t in TEMPLATES.items() if t['level']==level])
    if template not in TEMPLATES or TEMPLATES[template]['level']!=level:raise ValueError('Unsupported template/level')
    t=TEMPLATES[template];p=dict(parameters) if parameters is not None else dict(rng.choice(domain(t['kind'])))
    if any(type(v)!=int for v in p.values()) or p not in domain(t['kind']):raise ValueError('Outside frozen parameter domain')
    n=sp.Integer(p['n']);kind=t['kind']
    # Compute the exact answer before constructing the complete observed bank.
    if kind=='square':correct=X-n**2/(4*X)+n*sp.log(K*sp.Abs(X))
    elif kind=='linear':correct=n*X-sp.log(K*sp.Abs(X))
    else:correct=(-1 if kind.startswith('negative') else 1)*n/int(kind[-1])*sp.log(K*sp.Abs(X))
    fp=fingerprint_expression(integrand(kind,p));values=[render(v,p) for v in t['values']]
    key=json.dumps([VERSION,fp,template,values],separators=(',',':'));qid=uid('question:'+key);fid=uid('field:'+qid+':selection')
    answers=[{':answer/id':uid('answer:'+fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    q={':question/id':qid,':question/problem':render(t['problem'],p),':question/worked-solution':render(t['solution'],p),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':t['field_key'],':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[t['correct_index']][':answer/id']]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':template,'bank_profile':template,'parameters':p,'parameter_fingerprint':fp,'correct_antiderivative':str(correct),'domains':['x>0, K>0','x<0, K>0'],'source_basis':SOURCE_BASIS,'lineage':LINEAGE,'source_questions':[template],'dependencies':{'sympy':sp.__version__},'plot_requirements':'none'}}
def batch(level,count,seed=0):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
    if type(count)!=int or count<0:raise ValueError('Nonnegative count required')
    pool=[(mid,p) for mid,t in TEMPLATES.items() if t['level']==level for p in domain(t['kind'])];random.Random(seed).shuffle(pool)
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
    a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--count',type=int,default=5);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');a.add_argument('--template');p=a.parse_args()
    rows=batch(p.difficulty,p.count,p.seed) if not p.template else [generate(p.difficulty,p.seed,p.template)]
    print(json.dumps(rows,indent=2) if p.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
