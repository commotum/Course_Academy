#!/usr/bin/env python3
"""Seeded equilibrium-identification questions. No network, database or assets."""
import argparse
import json
from pathlib import Path
import random
import sys
import uuid
import sympy as S
from math_format import normalize_prose, checked_math_content

Y = S.Symbol('y', real=True)
KP = {'db_id':17592186166788, 'id':'6a6ca425-0e94-5b83-8729-fda13fbf3d7d',
      'title':'Identifying Equilibrium Solutions of a Differential Equation'}
SOURCES = {'polynomial':'4bdcd03c-4e33-5af2-a43a-72ec614b803e',
 'cubic':'73083626-cc38-5982-9c18-9459efa65b4d',
 'rational':'09328241-3b39-5707-a62b-8ca38e3a3a9c',
 'trigonometric':'c7b0ec58-a026-543f-8622-101c6f9cdc96',
 'logarithmic':'7617131b-e756-503f-ac7c-f76ae1870fab'}
FAMILIES = {'easy':['polynomial','rational','trigonometric','logarithmic'],
 'moderate':['polynomial','cubic','rational','trigonometric','logarithmic'],
 'hard':['rational-domain','logarithmic-domain']}

def tex(x):
    return S.latex(x, ln_notation=True, order='lex')

def uid(text):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'ca-equilibrium-v1/'+text))

def fraction(n,d):
    # Keep the ORIGINAL denominator even when numerator and denominator share factors.
    return S.Mul(n, S.Pow(d,-1,evaluate=False), evaluate=False)

def model(lhs, rhs, candidates, family, restrictions=(), independent='t', source=None):
    return {'lhs':lhs,'rhs':rhs,'candidates':list(candidates),'family':family,
            'restrictions':list(restrictions),'independent':independent,'source':source}

def valid(m,c):
    return all(bool((e.subs(Y,c)>0) if kind=='positive' else (e.subs(Y,c)!=0))
               for kind,e in m['restrictions'])

def decision(m,c):
    return valid(m,c) and S.simplify(m['rhs'].subs(Y,c)-m['lhs'].subs(Y,c))==0

def original_substitution(expr,c):
    # Substitute textually, retaining function arguments, powers and divisions.
    return tex(expr).replace('y',r'\left('+tex(c)+r'\right)')

@checked_math_content
def render(m,difficulty):
    lhs,rhs=m['lhs'],m['rhs']; var=m['independent']
    derivative=r'\frac{dy}{d'+var+'}'
    left=derivative if lhs==0 else derivative+r' + \left('+tex(lhs)+r'\right)'
    prompt='Consider the differential equation\n\n$$\n'+left+' = '+tex(rhs)+'.\n$$\n\n'
    if difficulty=='easy':
        prompt+='A constant function $y('+var+')=c$ is an **equilibrium solution** when it is in the domain of the equation and makes the derivative zero.\n\n'
    prompt+='Which of the following are equilibrium solutions? Select all that apply.'
    residual=S.factor_terms(S.expand(rhs-lhs)) if lhs!=0 else rhs
    steps=['A constant function $y('+var+')=c$ has derivative $dy/d'+var+'=0$. It must satisfy the original equation and its domain restrictions.']
    if m['restrictions']:
        conditions=[tex(e)+('>0' if kind=='positive' else r'\ne0') for kind,e in m['restrictions']]
        steps.append('The original equation requires $'+r',\quad '.join(conditions)+'$.')
    if lhs!=0:
        steps.append('Isolating the derivative gives\n\n$$\n'+derivative+' = '+tex(residual)+'.\n$$')
    steps.append('Test each supplied constant in the original equation, with the derivative set to zero.')
    truths=[]; paths=[]
    for c in m['candidates']:
        yes=decision(m,c); truths.append(yes)
        if not valid(m,c):
            bad=[]
            for kind,e in m['restrictions']:
                v=S.simplify(e.subs(Y,c))
                if (kind=='positive' and v<=0) or (kind=='nonzero' and v==0):
                    bad.append('$'+tex(e)+'='+original_substitution(e,c)+'='+tex(v)+'$')
            steps.append('- For $y=c='+tex(c)+'$, '+', '.join(bad)+' violates the original domain. This is *not* an equilibrium solution; cancellation cannot restore an excluded value.')
            paths.append({'candidate':tex(c),'domain':False,'key':False,'shown':'domain rejection before evaluation'})
            continue
        lv=S.expand(lhs.subs(Y,c)); rv=S.expand(rhs.subs(Y,c))
        # Declare c once instead of repeatedly nesting a translated e/pi value.
        # Each chain puts its evaluated result on a separate visible row.
        C=S.Symbol('c',real=True)
        rows=[]
        functions=sorted([f for f in set(lhs.atoms(S.Function))|set(rhs.atoms(S.Function)) if f.has(Y)],key=str)
        for func in functions:
            arg=func.args[0]; av=S.expand(arg.subs(Y,c))
            fv=S.expand(func.subs(Y,c))
            rows += [tex(func).replace('y','c')+' &= '+tex(func.func(av,evaluate=False)), ' &= '+tex(fv)]
        for label,expr,value in [('L',lhs,lv),('R',rhs,rv)]:
            rendered=tex(expr).replace('y','c')
            rows += [label+'(c) &= '+rendered,' &= '+tex(value)]
        status='is' if yes else 'is *not*'
        steps.append('- For $y=c='+tex(c)+'$, evaluate the non-derivative left and right sides, denoted $L(c)$ and $R(c)$:\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$\n\nThe values '+('agree' if yes else 'differ')+', so this '+status+' an equilibrium solution.')
        paths.append({'candidate':tex(c),'domain':True,'left':tex(lv),'right':tex(rv),'key':yes,
                      'operator_inputs':{'left':original_substitution(lhs,c),'right':original_substitution(rhs,c)},'shown_steps':rows})
    assert 0<sum(truths)<=len(truths)
    final='Select '+ ' and '.join('$y='+tex(c)+'$' for c,b in zip(m['candidates'],truths) if b)+'.'
    steps.append(final)
    prompt=normalize_prose(prompt); solution=normalize_prose('\n\n'.join(steps))
    identity=json.dumps([difficulty,prompt,[tex(c) for c in m['candidates']]],ensure_ascii=False)
    qid=uid(identity); fields=[]
    for i,(c,b) in enumerate(zip(m['candidates'],truths)):
        fid=uid(qid+'/field/'+str(i))
        choices=[{':answer/id':uid(fid+'/'+str(v)),':answer/type':':answer.type/text',':answer/value':str(v).lower()} for v in (False,True)]
        fields.append({':answer-field/id':fid,':answer-field/key':normalize_prose('$y='+tex(c)+'$'),
            ':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':choices,
            ':answer-field/correct':[':answer/id',choices[int(b)][':answer/id']]})
    family=m['family']; source=m['source'] or SOURCES[family.split('-')[0]]
    return {'knowledge_point':KP,'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+difficulty,
        ':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},
        'generation':{'version':'1.0.1','dependencies':{'python':'.'.join(map(str,sys.version_info[:3])),'sympy':S.__version__},'template':family,'source_question_ids':[source],
            'original_equation':{'lhs':str(lhs),'rhs':str(rhs)},
            'restrictions':[[k,str(e)] for k,e in m['restrictions']],
            'parameters':{'candidates':[str(c) for c in m['candidates']],'independent_variable':var},
            'solution_path':paths,'displayed_final':final}}

def sampled_model(rng,difficulty,family=None):
    family=family or rng.choice(FAMILIES[difficulty])
    ntrue=rng.choice([1,2]); a=rng.choice([-2,-1,1,2]); h=rng.randint(-2,2)
    candidates=[]; restrictions=[]
    if family in ['polynomial','cubic']:
        r,s=rng.sample(range(-2,4),2)
        if family=='polynomial':
            f=S.expand(a*(Y-r)*(Y-s)); good=[S.Integer(r),S.Integer(s)]
        else:
            if rng.choice([False,True]):
                q=rng.choice([x for x in range(-2,4) if x not in [r,s]])
                f=S.expand((Y-r)*(Y-s)*(Y-q)); good=list(map(S.Integer,[r,s,q]))
            else:
                f=S.expand((Y-r)*((Y-s)**2+1)); good=[S.Integer(r)]; ntrue=1
        bad=[S.Integer(x) for x in range(-3,5) if x not in good]
    elif family=='rational':
        k=rng.choice([1,2]); u=Y-h
        f=fraction(a*S.expand(u**2-k**2),u**2)
        restrictions=[('nonzero',u)]
        good=[S.Integer(h-k),S.Integer(h+k)]
        bad=[S.Integer(x) for x in range(h-3,h+4) if x!=h and x not in good]
    elif family=='rational-domain':
        r,s=rng.sample(range(-2,4),2)
        hole=rng.choice([r,s]+[x for x in range(-2,4) if x not in [r,s]])
        roots=[r,s]
        # A cubic permits two surviving roots even with a removable hole.
        if hole in roots and ntrue==2:
            roots.append(rng.choice([x for x in range(-2,4) if x not in roots]))
        num=S.expand(S.prod(Y-x for x in roots)); denom=Y-hole
        f=fraction(num,denom); restrictions=[('nonzero',denom)]
        good=[S.Integer(x) for x in roots if x!=hole]
        bad=[S.Integer(x) for x in range(-3,5) if x not in roots and x!=hole]
        candidates=[S.Integer(hole)]
    elif family=='trigonometric':
        h=0 if difficulty=='easy' else rng.choice([-1,0,1])
        u=Y-h; k=rng.choice([-1,0,1]); drift=rng.choice([False,True])
        f=a*S.sin(u)-(u-k*S.pi) if drift else a*S.sin(u)
        if drift:
            good=[h+k*S.pi];ntrue=1
            bad=[h+j*S.pi for j in [-1,0,1] if j!=k]
        else:
            good=[h+j*S.pi for j in [-1,0,1]]
            bad=[h+S.pi/2,h-S.pi/2]
    elif family in ['logarithmic','logarithmic-domain']:
        h=0 if difficulty=='easy' else rng.choice([-1,0,1])
        orientation=1 if difficulty=='easy' else rng.choice([-1,1])
        u=orientation*(Y-h); restrictions=[('positive',u)]
        product=family.endswith('-domain') or rng.choice([False,True])
        if product:
            k=rng.choice([-1,1,2]); root=S.exp(k)
            f=(u-root)*S.log(u);good=[S.Integer(h+orientation),h+orientation*root]
            bad=[h+orientation*S.exp(j) for j in [-1,0,1,2] if j not in [0,k]]
        else:
            k=rng.choice([-1,0,1,2]); f=u**2*S.log(u)-k*S.exp(2*k)
            good=[h+orientation*S.exp(k)]; ntrue=1
            bad=[h+orientation*S.exp(j) for j in [-1,0,1,2] if j!=k]
        if family.endswith('-domain'):candidates=[S.Integer(h-orientation*rng.choice([0,1]))]
    else:raise ValueError(family)
    candidates+=rng.sample(good,min(ntrue,len(good)))
    candidates+=rng.sample(bad,3-len(candidates)); rng.shuffle(candidates)
    lhs=S.Integer(0)
    rhs=f
    if difficulty=='moderate':
        # Deliberately require balance: same residual, extra term on both sides.
        lhs=rng.choice([-1,1,2])*Y+rng.choice([-1,0,1])
        rhs=S.Add(f,lhs,evaluate=False)
    return model(lhs,rhs,candidates,family,restrictions)

def label_strategies(record):
    """Choice-only actions, without inspecting the equation or target values."""
    values=[S.sympify(c) for c in record['generation']['parameters']['candidates']]
    order=sorted(range(3),key=lambda i:float(values[i]))
    actions={name:frozenset(indices) for name,indices in [
        ('first',[0]),('middle',[1]),('last',[2]),('first-two',[0,1]),
        ('last-two',[1,2]),('outer-two',[0,2]),('smallest',[order[0]]),
        ('median',[order[1]]),('largest',[order[2]]),
        ('two-smallest',order[:2]),('two-largest',order[1:]),
        ('rank-outer-two',[order[0],order[2]])]}
    actions.update({name:frozenset(i for i,c in enumerate(values) if predicate(c))
        for name,predicate in [('positive',lambda c:c>0),('negative',lambda c:c<0),('zero',lambda c:c==0)]})
    truth=frozenset(i for i,path in enumerate(record['generation']['solution_path']) if path['key'])
    return {name for name,action in actions.items() if action==truth}

def visible_profile(record):
    family=record['generation']['template']
    equation=record['generation']['original_equation']
    lhs=S.sympify(equation['lhs'],locals={'y':Y},evaluate=False)
    rhs=S.sympify(equation['rhs'],locals={'y':Y},evaluate=False)
    f=S.expand(rhs-lhs)
    if 'logarithmic' in family:
        logarithm=next(iter(f.atoms(S.log)))
        shape='product' if S.degree(f.coeff(logarithm),Y)==1 else 'square'
    elif family=='trigonometric':
        sine=next(iter(f.atoms(S.sin)))
        shape='drift' if f.xreplace({sine:S.Integer(0)}).has(Y) else 'sine-only'
    elif family=='cubic':
        shape='three-real' if S.Poly(f,Y).count_roots(-S.oo,S.oo)==3 else 'one-real'
    elif family=='rational-domain':
        numerator,denominator=rhs.as_numer_denom()
        shape=str(S.degree(numerator,Y))+('-removable' if S.degree(S.gcd(numerator,denominator),Y)>0 else '-pole')
    else:shape='standard'
    return family+'/'+shape

def repeated_label_cue(records):
    # A repeated visible family must not train a fixed sign, position or rank
    # action. Singleton coincidences cannot be eliminated without forbidding
    # every legitimate answer. Count-one generation remains ordinary practice.
    groups={'all':list(records)}
    for record in records:
        family=record['generation']['template'].split('-')[0]
        if family=='cubic':family='polynomial'
        groups.setdefault('family/'+family,[]).append(record)
        groups.setdefault('profile/'+visible_profile(record),[]).append(record)
    return any(len(group)>=2 and set.intersection(*(label_strategies(r) for r in group))
               for group in groups.values())

def generate(difficulty,seed,count):
    if difficulty=='unclassified': difficulty='easy'
    rng=random.Random(seed)
    for batch_attempt in range(500):
        out=[];seen=set()
        for _ in range(count):
            for attempt in range(500):
                m=sampled_model(rng,difficulty);record=render(m,difficulty)
                signature=json.dumps([record['question'][':question/problem'],
                    sorted(f[':answer-field/key'] for f in record['question'][':question/answer-fields'])])
                if signature not in seen:
                    seen.add(signature)
                    record['generation'].update({'seed':seed,'index':len(out),'difficulty':difficulty})
                    out.append(record);break
            else:raise ValueError('Requested count exhausted unique bounded instances')
        if not repeated_label_cue(out):return out
    raise ValueError('Requested batch could not avoid a recurring choice-label cue')

def replay():
    data=json.loads(Path(__file__).with_name('source-cases.json').read_text())
    local={'y':Y,'E':S.E,'pi':S.pi,'sin':S.sin,'log':S.log}
    out=[]
    for d in data:
        read=lambda s:S.sympify(s,locals=local)
        m=model(read(d['lhs']),read(d['rhs']),list(map(read,d['candidates'])),d['family'],
            [(k,read(e)) for k,e in d['restrictions']],d['independent'],d['source'])
        out.append(render(m,'easy'))
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='easy')
    p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0)
    p.add_argument('--format',choices=['json'],default='json');p.add_argument('--replay-source',action='store_true')
    args=p.parse_args()
    if args.count<1:p.error('count must be positive')
    print(json.dumps(replay() if args.replay_source else generate(args.difficulty,args.seed,args.count),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
