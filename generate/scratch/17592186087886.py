#!/usr/bin/env python3
"""Bounded, source-replayed homogeneous-ODE substitution generator (easy only)."""
import argparse, json, random, sys, uuid
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError:
    import os
    interpreter = Path(__file__).resolve().parents[2] / '.venv/bin/python'
    os.execv(str(interpreter), [str(interpreter), str(Path(__file__).resolve()), *sys.argv[1:]])
HERE = Path(__file__).with_suffix('')
sys.path.insert(0, str(HERE))
from math_reader import x, y, v, D, fingerprint
KP_ID = 17592186087886
KP_UUID = 'a8edbecf-59d3-5f32-a0ac-d6e8f2128dc0'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
VERSION = '1.0.0'
SUPPORTED_LEVELS = ('easy',)
SOURCES = {q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
# Each source owns one complete bank. No pooled or inferred replacement banks.
ORIGINAL = {'q-14315':3, 'q-8745':1, 'q-14314':3, 'q-14316':1, 'q-14323':1, 'q-8747':1, 'q-90601':2}
DOMAINS = {t:list(range(2,8)) if t in ('q-14315','q-14314') else list(range(1,7)) for t in ORIGINAL}

def mathematics(t, k):
    if t == 'q-14315':
        rhs = k*y**3/(x*y**2+y*x**2); z = (k-1)*v**2-v
        bank = [((v+1)/((k-2)*v**2+1),1/x),((v+1)/z,1/x),(z/(v+1),x),((v+1)/(v*z),x),((v**2+v)/(k*v**2-v),1/x)]
    elif t == 'q-8745':
        rhs = sp.sec(k*x/y)+y/x; c = sp.cos(k/v); s = sp.sec(k/v)
        bank = [(c,1/x),(1/(2*v+s),1/x),(1/c,x),(c,sp.Integer(1)),(1/(v+s),1/x)]
    elif t == 'q-14314':
        rhs = sp.tan(x**2/y**2)+k*y/x; f = sp.tan(1/v**2); h = sp.tan(1/v); z = f+(k-1)*v
        bank = [(z,x),(1/(h+(k-2)*v),1/x),(1/z,1/x),(h+(k-1)*v**2,1/x),(f,x)]
    elif t == 'q-14316':
        rhs = (k*x**2-x*y+y**2)/(y**2+x**2)
        bank = [((v**2+1)/(k+v+4*v**2),1/x),((v**2+1)/(k-2*v+v**2-v**3),1/x),((k-3*v-4*v**2)/(1+v**2),x),((v**2+1)/(k-v-v**3),1/x),((v**2+1)/(k-3*v-4*v**2),sp.Integer(1))]
    elif t == 'q-14323':
        rhs = (k*x**3+x*y**2-y**3)/(x*y**2+2*y*x**2)
        bank = [((v**2-1)/(k-2*v**3),1/x),((v**3+2*v**2)/(k-v**2),x),((v**2+2*v)/(k-v**2-2*v**3),1/x),((v+2)/(k-3*v-2*v**2),1/x),((k-2*v-3*v**2)/(v**2+2*v),x)]
    elif t == 'q-8747':
        rhs = sp.exp(sp.sin(k*y/x)); a = sp.exp(sp.sin(k*v)); b = sp.exp(sp.cos(k*v))
        bank = [(1/(b+3),1/x),(a-3*v**2,sp.Integer(1)),(1/(b-5*v),sp.Integer(1)),(a,1/x),(1/(a-v),1/x)]
    elif t == 'q-90601':
        rhs = y/x-k*sp.sin(y/x)
        bank = [(sp.sin(1/v),-k/x),(1/sp.sin(v),-k/x),(1/sp.sin(v),1/x**2),(1/(v-k*sp.sin(v)),1/x),(k*v-sp.sin(1/v),1/x)]
    else: raise ValueError('Unknown source template')
    return rhs, bank

def render_source(text, t, k):
    """Replace declared slots in the original ordered solution and prompt."""
    if k == ORIGINAL[t]: return text
    if t == 'q-14315':
        text = text.replace('3{', str(k)+'{').replace('3(', str(k)+'(')
        text = text.replace('2{v}^{2}-v', str(k-1)+'{v}^{2}-v').replace('2{v}^{3}-{v}^{2}', str(k-1)+'{v}^{3}-{v}^{2}')
    elif t == 'q-8745':
        for a,b in [(r'\frac{x}{y}',r'\frac{'+str(k)+r'x}{y}'),(r'\frac{x}{vx}',r'\frac{'+str(k)+r'x}{vx}'),(r'\frac{1}{v}',r'\frac{'+str(k)+r'}{v}')]: text = text.replace(a,b)
    elif t == 'q-14314':
        text = text.replace('3y','@K@y').replace('3vx','@K@vx').replace('3v','@K@v')
        text = text.replace('+2v','+'+str(k-1)+'v').replace('@K@',str(k))
    elif t == 'q-14316':
        text = text.replace(r'{x}^{2}-xy',str(k)+r'{x}^{2}-xy').replace(r'{x}^{2}-x(vx)',str(k)+r'{x}^{2}-x(vx)')
        text = text.replace('1-v',str(k)+'-v').replace('1-2v',str(k)+'-2v')
    elif t == 'q-14323':
        text = text.replace(r'{x}^{3}+x',str(k)+r'{x}^{3}+x').replace('1+',str(k)+'+').replace('1-',str(k)+'-')
    elif t == 'q-8747':
        text = text.replace(r'\frac{y}{x}',r'\frac{'+str(k)+r'y}{x}').replace(r'\frac{vx}{x}',r'\frac{'+str(k)+r'vx}{x}')
        text = text.replace('⁡v', '⁡('+str(k)+'v)')
    elif t == 'q-90601':
        text = text.replace('-2', '-'+str(k)).replace(r'-\frac{2}{x}',r'-\frac{'+str(k)+r'}{x}')
    return text

def generate(difficulty='easy', seed=0, template=None, parameters=None, profile=None):
    if difficulty not in SUPPORTED_LEVELS: raise ValueError('Unsupported band: no moderate/hard source backbone or validated grading contract')
    rng = random.Random(seed); t = template or rng.choice(list(ORIGINAL)); k = (parameters or {}).get('k', rng.choice(DOMAINS[t]))
    if type(k) is not int or k not in DOMAINS[t]: raise ValueError('Outside certified parameter domain')
    if profile not in (None,t): raise ValueError('Each template requires its own complete source bank')
    src = SOURCES[t]; rhs, bank = mathematics(t,k)
    expected = sp.cancel((rhs.subs(y,v*x)-v)/x)
    # Correctness before rendering: identify exactly one equation equal to the transformed ODE.
    rates = [sp.cancel(b/a) for a,b in bank]
    good = [i for i,r in enumerate(rates) if sp.simplify(r-expected)==0]
    if len(good)!=1 or any(sp.simplify(a-b)==0 for i,a in enumerate(rates) for b in rates[:i]): raise ValueError('Colliding or ambiguous complete bank')
    problem = render_source(src[':question/problem'],t,k); solution = render_source(src[':question/worked-solution'],t,k)
    # Equations retain derivative notation, source answer shape, and five choices.
    values = [sp.latex(a)+D+'='+sp.latex(b) for a,b in bank]
    if k == ORIGINAL[t]:
        values = [a[':answer/value'] for a in src[':question/answer-fields'][0][':answer-field/choices']]
    fp = fingerprint(problem)
    # Mathematical prompt, version and full bank establish identity, never seed or ordering.
    qid = str(uuid.uuid5(uuid.UUID(KP_UUID),json.dumps([VERSION,fp,sorted(sp.srepr(r) for r in rates)])))
    fid = str(uuid.uuid5(uuid.UUID(qid),'field:selection'))
    answers = [{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'recipe:'+str(i))),':answer/type':':answer.type/math',':answer/value':value} for i,value in enumerate(values)]
    question = {':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[good[0]][':answer/id']]}]}
    return {'question':question,'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Transforming a Homogeneous Differential Equation into a Separable Equation Using a Substitution'},'generation':{'version':VERSION,'seed':seed,'template':t,'bank_profile':t,'parameters':{'k':k},'source_question_id':src[':question/id'],'source_db_id':src[':db/id'],'parameter_fingerprint':fp,'domains':'x != 0; original RHS defined; separated coefficient defined; exclude equilibria where F(v)-v=0 when dividing. Transformation does not assert equivalence across excluded branches.','dependencies':{'sympy':sp.__version__}}}

def batch(difficulty,count,seed=0,template=None):
    if difficulty not in SUPPORTED_LEVELS: raise ValueError('Unsupported difficulty')
    if template is not None and template not in DOMAINS:raise ValueError('Unknown template')
    tasks = [(t,k) for t,domain in DOMAINS.items() if template is None or t==template for k in domain];random.Random(seed).shuffle(tasks)
    if count>len(tasks):raise ValueError('Finite domain: at most '+str(len(tasks))+' mathematical tasks, including source tasks')
    return [generate(difficulty,seed,t,{'k':k}) for t,k in tasks[:count]]

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--template');a=p.parse_args()
    rows=batch(a.difficulty,a.count,a.seed,a.template)
    print(json.dumps(rows,indent=2) if a.format=='json' else '\n\n'.join(markdown(r) for r in rows))
