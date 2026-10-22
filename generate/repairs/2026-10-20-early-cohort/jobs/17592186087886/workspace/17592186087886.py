#!/usr/bin/env python3
"""Bounded, source-replayed homogeneous-ODE substitution generator (easy only)."""
import argparse, json, random, sys, uuid
from pathlib import Path
import sympy as sp
HERE = Path(__file__).with_suffix('')
from math_reader import x, y, v, D, DY, fingerprint
KP_ID = 17592186087886
KP_UUID = 'a8edbecf-59d3-5f32-a0ac-d6e8f2128dc0'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
VERSION = '1.2.0'
SUPPORTED_LEVELS = ('easy',)
SOURCES = {q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
# Source banks are replayed intact; authored banks vary the surviving linear role.
ORIGINAL = {'q-14315':3, 'q-8745':1, 'q-14314':3, 'q-14316':1, 'q-14323':1, 'q-8747':1, 'q-90601':2, 'q-90600':3}
DOMAINS = {t:list(range(2,8)) if t in ('q-14315','q-14314') else list(range(1,7)) for t in ORIGINAL}
ROLES = (-2, -1, 0, 1, 2)

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
    elif t == 'q-90600':
        rhs = (y**2+k*x**2)/(x*y)
        bank = [(v/(v**2+k),1/x),(v,k/x),(v/(v+1),k/x),((v+1)/(k*v**2),1/x),(k*v,1/x**2)]
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
    elif t == 'q-90600':
        text = text.replace('3',str(k))
    return text

def equation(coefficient, right):
    return r'\left('+sp.latex(coefficient)+r'\right)'+D+'='+sp.latex(right)

def role_instance(t, k, shift):
    base = mathematics(t, k)[0]
    rhs = base + shift*y/x
    transformed = sp.cancel(base.subs(y, v*x))
    # A complete bank shared by all five assignments of the relevant evidence.
    bank = [(sp.cancel(1/(transformed+(j-1)*v)), 1/x) for j in ROLES]
    return rhs, bank

def role_text(src, rhs, shift):
    problem = src[':question/problem'].split('$$')
    problem[1] = '\n'+DY+'='+sp.latex(rhs)+'.\n'
    problem = '$$'.join(problem)
    substituted = rhs.xreplace({y:sp.Mul(v,x,evaluate=False)})
    base_F = sp.cancel((rhs-shift*y/x).subs(y,v*x))
    F = base_F+shift*v
    residual = sp.cancel(F-v)
    rows = [DY+' & ='+sp.latex(rhs),
            'x'+D+'+v & ='+sp.latex(substituted),
            'x'+D+'+v & ='+sp.latex(F),
            'x'+D+' & ='+sp.latex(base_F+(shift-1)*v),
            'x'+D+' & ='+sp.latex(residual),
            equation(sp.cancel(1/residual),1/x).replace('=', ' & =')]
    prefix = src[':question/worked-solution'].rsplit(r'\begin{aligned}',1)[0]
    solution = prefix+r'\begin{aligned}'+r' \\ '.join(rows)+r'.\end{aligned}'+'\n$$'
    return problem, solution

def generate(difficulty='easy', seed=0, template=None, parameters=None, profile=None):
    if difficulty not in SUPPORTED_LEVELS: raise ValueError('Unsupported band: no moderate/hard source backbone or validated grading contract')
    rng = random.Random(seed); t = template or rng.choice(list(ORIGINAL))
    parameters = parameters or {}
    shift = parameters.get('shift', 0 if parameters.get('k') == ORIGINAL[t] else rng.choice(ROLES))
    k = parameters.get('k', rng.choice(DOMAINS[t]))
    if type(k) is not int or k not in DOMAINS[t]: raise ValueError('Outside certified parameter domain')
    if type(shift) is not int or shift not in ROLES: raise ValueError('Outside certified linear-role domain')
    replay = k == ORIGINAL[t] and shift == 0
    bank_profile = t if replay else 'linear-role'
    if profile not in (None,bank_profile): raise ValueError('Profile does not match source replay / authored role case')
    src = SOURCES[t]
    rhs, bank = mathematics(t,k) if replay else role_instance(t,k,shift)
    expected = sp.cancel((rhs.subs(y,v*x)-v)/x)
    # Correctness before rendering: identify exactly one equation equal to the transformed ODE.
    rates = [sp.cancel(b/a) for a,b in bank]
    good = [i for i,r in enumerate(rates) if sp.simplify(r-expected)==0]
    if len(good)!=1 or any(sp.simplify(a-b)==0 for i,a in enumerate(rates) for b in rates[:i]): raise ValueError('Colliding or ambiguous complete bank')
    if replay:
        problem = src[':question/problem']; solution = src[':question/worked-solution']
    else:
        problem, solution = role_text(src,rhs,shift)
    # Equations retain derivative notation, source answer shape, and five choices.
    values = [equation(a,b) for a,b in bank]
    if replay:
        values = [a[':answer/value'] for a in src[':question/answer-fields'][0][':answer-field/choices']]
    fp = fingerprint(problem)
    # Mathematical prompt, version and full bank establish identity, never seed or ordering.
    qid = str(uuid.uuid5(uuid.UUID(KP_UUID),json.dumps([VERSION,fp,sorted(sp.srepr(r) for r in rates)])))
    fid = str(uuid.uuid5(uuid.UUID(qid),'field:selection'))
    answers = [{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'recipe:'+str(i))),':answer/type':':answer.type/math',':answer/value':value} for i,value in enumerate(values)]
    correct_id = answers[good[0]][':answer/id']
    random.Random(f'{seed}:{t}:{k}:{shift}:choice-order').shuffle(answers)
    question = {':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]}
    return {'question':question,'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Transforming a Homogeneous Differential Equation into a Separable Equation Using a Substitution'},'generation':{'version':VERSION,'seed':seed,'template':t,'bank_profile':bank_profile,'parameters':{'k':k,'shift':shift},'source_question_id':src[':question/id'],'source_db_id':src[':db/id'],'parameter_fingerprint':fp,'domains':'x != 0; original RHS defined; separated coefficient defined; exclude equilibria where F(v)-v=0 when dividing. Transformation does not assert equivalence across excluded branches.','dependencies':{'sympy':sp.__version__}}}

def batch(difficulty,count,seed=0,template=None):
    if difficulty not in SUPPORTED_LEVELS: raise ValueError('Unsupported difficulty')
    if template is not None and template not in DOMAINS:raise ValueError('Unknown template')
    tasks = [(t,k,s) for s in ROLES for t,domain in DOMAINS.items() if template is None or t==template for k in domain]
    rng=random.Random(seed);rng.shuffle(tasks)
    # Prefer exact source replays when several coefficient decompositions coincide.
    tasks.sort(key=lambda task: not (task[1]==ORIGINAL[task[0]] and task[2]==0))
    distinct = {}
    for t,k,s in tasks:
        rhs = mathematics(t,k)[0]+s*y/x
        semantic = sp.srepr(sp.cancel(rhs.subs(y,v*x)))
        distinct.setdefault(semantic,(t,k,s))
    tasks=list(distinct.values());rng.shuffle(tasks)
    if count>len(tasks):raise ValueError('Finite domain: at most '+str(len(tasks))+' mathematical tasks, including source tasks')
    return [generate(difficulty,seed,t,{'k':k,'shift':s}) for t,k,s in tasks[:count]]

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--template');a=p.parse_args()
    rows=batch(a.difficulty,a.count,a.seed,a.template)
    print(json.dumps(rows,indent=2) if a.format=='json' else '\n\n'.join(markdown(r) for r in rows))
