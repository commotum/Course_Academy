#!/usr/bin/env python3
"""Scoped substitution generator: source-complete radio banks; no database writes.

Easy uses positive integer powers. Moderate preserves the observed square-root
or negative-inner-derivative workloads. Hard is an unsupported bounded capability.
"""
import sys
from pathlib import Path
try:
    import sympy as sp
except ImportError:
    import os
    interpreter = Path(__file__).resolve().parents[2] / '.venv/bin/python'
    if interpreter.exists() and Path(sys.executable).resolve() != interpreter.resolve():
        os.execv(str(interpreter), [str(interpreter), __file__, *sys.argv[1:]])
    raise
import argparse, hashlib, json, random, uuid

HERE = Path(__file__).with_suffix('')
SOURCE = json.loads((HERE / 'source.json').read_text())
KP_ID = 17592186068723
KP_UUID = SOURCE['record'][':knowledge-point/id']
TITLE = SOURCE['record'][':knowledge-point/title']
VERSION = '68723-v1'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
SUPPORTED_LEVELS = ('easy', 'moderate')
X = sp.Symbol('x', real=True)
# k*x^(m-1)*(a*x^m+b)^n. Each source bank is kept whole.
CASES = [
 ('q-12494','easy',1,1,2,5,10,'calculate'),
 ('q-12496','easy',1,1,4,11,9,'calculate'),
 ('q-113710','easy',2,1,6,4,5,'calculate'),
 ('q-113711','easy',1,1,7,2,2,'calculate'),
 ('q-113715','moderate',2,1,3,10,'1/2','calculate'),
 ('q-2379','moderate',1,-1,2,3,5,'equation'),
 ('q-2388','easy',1,1,2,-1,3,'calculate'),
 ('q-72385','easy',1,2,3,1,5,'equation'),
 ('q-72386','easy',2,1,8,1,7,'equation'),
 ('q-72467','moderate',1,1,2,-5,'1/2','calculate'),
]
SOURCES = {q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(s): return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def case(template): return next(c for c in CASES if c[0]==template)
def tex(x): return sp.latex(x,order='lex')
def defaults(c): return dict(zip(('k','a','m','b','n'),c[2:7]))
def data(p):
    k,a,m,b,n = (sp.Rational(p[key]) for key in ('k','a','m','b','n'))
    u=a*X**m+b
    f=k*X**(m-1)*u**n
    ratio=k/(a*m)
    correct=ratio*u**(n+1)/(n+1)
    return k,a,m,b,n,u,f,ratio,correct
def bank(template,p):
    k,a,m,b,n,u,f,r,c=data(p);up=u**(n+1);un=u**n
    recipes = {
      'q-12494':[up/(n+1),un/n,up/n,un/(m*n),c],
      'q-12496':[up/(m*b),c,un/n,un/(m*n),up/(n+1)],
      'q-113710':[up/(n+1),c,up/(m/k),up/k,k*up],
      'q-113711':[c,m*up/(n+1),up/(n+1),up/m,m*(n+1)*up],
      'q-113715':[m*up/k,k*up/m,c,a*m*(n+1)*up/k,up],
      'q-2379':[c,up/(n+1),-un/n,up/(n-1),-up/(n+1)],
      'q-2388':[c,m*(n+1)*up,u**(n+2)/(m*(n+2)),un/(m*n),n*un],
      'q-72385':[un/(a*n),un/n,c,up/(n+1),a*n*un],
      'q-72386':[c,(n+1)*up,n*un,up/(n+1),un/(m*n)],
      'q-72467':[m*up,m*(n+1)*up,up,c,up/m],
    }[template]
    if any(sp.simplify(z-w)==0 for i,z in enumerate(recipes) for w in recipes[i+1:]):
        raise ValueError('whole-bank collision')
    if sum(sp.simplify(z-c)==0 for z in recipes)!=1: raise ValueError('ambiguous canonical answer')
    return recipes
def render(template,p):
    k,a,m,b,n,u,f,r,c=data(p)
    outside=k*X**(m-1)
    inner=tex(u)
    factor=r'\sqrt{'+inner+'}' if n==sp.Rational(1,2) else r'\left('+inner+r'\right)^{'+tex(n)+'}'
    integrand=tex(outside)+factor
    integral=r'\int '+integrand+r'\,\text{d}x'
    prompt=('Calculate $'+integral+'.$') if case(template)[7]=='calculate' else '$'+integral+'=$'
    if n.q!=1:
        prompt+='\n\nWork on an interval where $'+inner+'>0$.'
    derivative=a*m*X**(m-1)
    # Preserve the observed instructional sentences and substitution sequence.
    solution=('In this case, the $'+tex(outside)+"$ outside the parentheses isn't quite the derivative of $("+inner+').$ But the derivative is $'+tex(derivative)+",$ so we're only out by a constant factor.\n\nSo we make the substitution\n\n$$\nu="+inner+'.\n$$\n\nIts derivative is given by\n\n$$\n'+r'\frac{\text{d}u}{\text{d}x}='+tex(derivative)+r'\quad\Longrightarrow\quad '+tex(r)+r'\,\text{d}u='+tex(outside)+r'\,\text{d}x.'+'\n$$\n\nand we can now write our integral in terms of $u,$ as follows:\n\n$$\n'+integral+'='+tex(r)+r'\int u^{'+tex(n)+r'}\,\text{d}u.'+'\n$$\n\nFinally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get\n\n$$\n'+r'\begin{aligned}'+tex(r)+r'\int u^{'+tex(n)+r'}\,\text{d}u &='+tex(r)+r'\frac{u^{'+tex(n+1)+'}}{'+tex(n+1)+r'}+C\\ &='+tex(r/(n+1))+r'u^{'+tex(n+1)+r'}+C\\ &='+tex(c)+r'+C.\end{aligned}'+'\n$$')
    return prompt,solution
def fingerprint(q):
    # Mathematical task identity ignores seeds, IDs, wording and choice order.
    from importlib.util import spec_from_file_location,module_from_spec
    spec=spec_from_file_location('bounded_parser',HERE/'parser.py');mod=module_from_spec(spec);spec.loader.exec_module(mod)
    f=mod.prompt(q[':question/problem'])
    return digest(sp.srepr(sp.expand(f)))
def generate(level,seed=0,template=None,parameters=None):
    if level not in SUPPORTED_LEVELS: raise ValueError('hard: no observed workload or validated hard template')
    rng=random.Random(seed);eligible=[c for c in CASES if c[1]==level]
    c=case(template) if template else rng.choice(eligible)
    if c not in eligible: raise ValueError('template difficulty mismatch')
    for attempt in range(200):
        p=defaults(c)
        if parameters is None:
            p['b']=rng.randint(1,20)*(-1 if c[5]<0 else 1)
            if c[6]!='1/2':p['n']=rng.randint(3,10)
        else:p=dict(parameters)
        if set(p)!=set(defaults(c)):raise ValueError('parameter keys')
        if any(sp.Rational(p[z])!=sp.Rational(defaults(c)[z])for z in ('k','a','m')):raise ValueError('fixed observed multiplier and inner degree')
        if type(p['b'])!=int or not 1<=abs(p['b'])<=20 or p['b']*c[5]<=0:raise ValueError('bounded signed shift')
        n=sp.Rational(p['n'])
        if c[6]=='1/2' and n!=sp.Rational(1,2) or c[6]!='1/2' and (n.q!=1 or not 2<=n<=10):raise ValueError('bounded outer power')
        try:vals=bank(c[0],p)
        except ValueError:
            if parameters is not None:raise
            continue
        p={k:str(v) if k=='n' and sp.Rational(v).q!=1 else int(v) for k,v in p.items()}
        prompt,sol=render(c[0],p);values=[tex(z)+'+C'for z in vals]
        _,_,_,_,_,u,f,r,correct=data(p)
        identity=digest({'prompt':prompt,'solution':sol,'bank':sorted(values),'level':level,'version':VERSION})
        qid=uid('question:'+identity);fid=uid('field:'+qid)
        choices=[{':answer/id':uid('answer:'+fid+':'+s),':answer/type':':answer.type/math',':answer/value':s}for s in values]
        cid=choices[next(i for i,z in enumerate(vals)if sp.simplify(z-correct)==0)][':answer/id'];rng.shuffle(choices)
        q={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',cid]}]}
        return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':c[0],'bank_profile':c[0],'parameters':p,'mathematical_fingerprint':fingerprint(q),'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'dependencies':{'sympy':sp.__version__},'domain':'real x; inner>0 for square roots','plot_requirement':'none','repairs':['standardized TeX and solution layout','q-12494: mathematically derived missing correct designation and solution'] if c[0]=='q-12494' else ['standardized TeX and solution layout']}}
    raise ValueError('bounded whole-bank sampling exhausted')
def batch(level,count,seed=0):
    result=[];seen=set()
    for i in range(count*200):
        rec=generate(level,seed+i);fp=rec['generation']['mathematical_fingerprint']
        if fp not in seen:result.append(rec);seen.add(fp)
        if len(result)==count:return result
    raise ValueError('finite distinct variant bound reached')
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');args=ap.parse_args()
    if args.count<1:ap.error('positive count required')
    records=batch(args.difficulty,args.count,args.seed)
    print(json.dumps(records,indent=2)if args.format=='json'else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+'\n'.join('$'+a[':answer/value']+'$'for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+r['question'][':question/worked-solution']for r in records))
if __name__=='__main__':main()
