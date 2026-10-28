#!/usr/bin/env python3
"""Seeded, relocatable three-variable potential generator. No I/O except JSON stdout."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import sys
import uuid
import sympy as sp
from math_format import checked_math_content, normalize_prose, normalize_tex

VERSION = '2.0.0'
ROOT = Path(__file__).resolve().parent
PROFILES = json.loads((ROOT / 'profiles.json').read_text())
x, y, z, C = sp.symbols('x y z C', real=True)
a, b, n = sp.symbols('a b n', real=True)
SYMBOLS = dict(zip(('x','y','z','C','a','b','n'), (x,y,z,C,a,b,n)))
SYMBOLS.update(sin=sp.sin,cos=sp.cos,exp=sp.exp,log=sp.log)
VALUES = (-3,-2,-1,1,2,3)
TITLE = 'Reconstructing a Three-Variable Function From Its Gradient'


def expressions(profile, av=1, bv=1, frequency=None):
    p = PROFILES[profile] if isinstance(profile,int) else profile
    if av not in VALUES or bv not in VALUES:
        raise ValueError('Coefficient multipliers must be in '+str(VALUES))
    nv = frequency if frequency is not None else p['frequency']
    if p['frequency'] is not None and nv not in (2,3,4):
        raise ValueError('Frequency must be 2, 3, or 4')
    if p['frequency'] is None and frequency is not None:
        raise ValueError('This profile has no frequency slot')
    subs = {a:av,b:bv,n:nv or 1}
    bank = [sp.expand(sp.sympify(c['recipe'],locals=SYMBOLS).subs(subs)) for c in p['choices']]
    potential = bank[p['correct_index']] - C
    field = [sp.diff(potential,v) for v in (x,y,z)]
    return p, bank, potential, field


def tex(expression):
    if expression.is_Add and C in expression.args:
        return normalize_tex(sp.latex(expression-C,ln_notation=True)+'+C')
    return normalize_tex(sp.latex(expression,ln_notation=True))


def display(value):
    return '\n\n$$\n'+value+'\n$$\n\n'


def plus_function(expr, function):
    return function if expr == 0 else tex(expr)+'+'+function


def partial(v, name='f'):
    return rf'\frac{{\partial {name}}}{{\partial {v}}}'


def solution(potential, field):
    # Group known potential terms by the first integration at which they appear.
    terms = sp.Add.make_args(sp.expand(potential))
    first = sp.Add(*(t for t in terms if t.has(x)))
    second = sp.Add(*(t for t in terms if not t.has(x) and t.has(y)))
    third = sp.expand(potential-first-second)
    fy_known = sp.diff(first,y)
    fz_known = sp.diff(first+second,z)
    gy = sp.simplify(field[1]-fy_known)
    hp = sp.simplify(field[2]-fz_known)
    pfx,pfy,pfz = (partial(v) for v in ('x','y','z'))
    pgy=partial('y','g')
    out = 'The gradient of the function $f(x,y,z)$ is defined as'
    out += display(r'\nabla f(x,y,z)='+pfx+r'\,\mathbf{i}+'+pfy+r'\,\mathbf{j}+'+pfz+r'\,\mathbf{k}.')
    out += 'Since $\\nabla f(x,y,z)=F(x,y,z),$ the function $f(x,y,z)$ must satisfy the following system:'
    out += display(r'\begin{aligned}'+r' \\ '.join(partial(v)+'&='+tex(value) for v,value in zip(('x','y','z'),field))+r'\end{aligned}')
    out += 'First, we integrate $'+pfx+'$ with respect to $x.$ Note that the solution should contain an arbitrary function of $y$ and $z:$'
    out += display(r'\begin{aligned}f(x,y,z)&=\int '+pfx+r'\,\mathrm{d}x \\ &=\int \left('+tex(field[0])+r'\right)\,\mathrm{d}x \\ &='+plus_function(first,'g(y,z)')+r'\end{aligned}')
    out += 'Now, differentiating the above expression with respect to $y,$ we obtain'
    out += display(pfy+'='+plus_function(fy_known,pgy)+'.')
    out += 'Taking $'+pfy+'='+tex(field[1])+'$ into account, we obtain'
    comparison=plus_function(fy_known,pgy)+'&='+tex(field[1])
    if fy_known != 0:
        comparison+=r' \\ '+pgy+'&='+tex(gy)
    out += display(r'\begin{aligned}'+comparison+r'\end{aligned}')
    out += 'Now, we integrate $'+pgy+'$ with respect to $y.$ Note that the solution should contain an arbitrary function of $z:$'
    out += display(r'\begin{aligned}g(y,z)&=\int '+pgy+r'\,\mathrm{d}y \\ &=\int \left('+tex(gy)+r'\right)\,\mathrm{d}y \\ &='+plus_function(second,'h(z)')+r'\end{aligned}')
    out += 'Substituting $g(y,z)='+plus_function(second,'h(z)')+'$ in the expression for $f(x,y,z),$ we get'
    out += display('f(x,y,z)='+plus_function(first+second,'h(z)')+'.')
    out += 'To determine the function $h(z),$ we differentiate $f(x,y,z)$ with respect to $z.$ This gives'
    out += display(pfz+'='+plus_function(fz_known,"h'(z)")+'.')
    out += 'Comparing this derivative with the third component and subtracting the known terms gives'
    # The known derivative and the target component are already displayed.
    # Write the residual directly rather than repeating both long expressions
    # on one line, which can clip the last terms in the learner UI.
    comparison="h'(z)&="+tex(hp)
    out += display(r'\begin{aligned}'+comparison+r' \\ h(z)&='+tex(third+C)+r'\end{aligned}')
    out += 'where $C$ is a constant.\n\nConsequently,'
    out += display('f(x,y,z)='+tex(potential+C)+'.')
    return normalize_prose(out.strip())


def identity(value):
    return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:potential:'+value))


@checked_math_content
def generate(profile=1, av=1, bv=1, frequency=None, seed=0):
    p,bank,potential,field=expressions(profile,av,bv,frequency)
    return build_record(p,bank,potential,field,av,bv,frequency,seed)


@checked_math_content
def build_record(p,bank,potential,field,av,bv,frequency,seed,difficulty=None):
    components=[r'\left('+tex(t)+r'\right)\,\mathbf{'+unit+'}' for t,unit in zip(field,'ijk')]
    vector=r'\begin{aligned}F(x,y,z)&='+components[0]+r' \\ &{}+'+components[1]+r' \\ &{}+'+components[2]+r'.\end{aligned}'
    if p['layout']=='display':
        problem='Consider the function'+display(vector)+'Find $f(x,y,z)$ such that $\\nabla f(x,y,z)=F(x,y,z).$'
    else:
        problem='Find $f(x,y,z)$ such that $\\nabla f(x,y,z)=F(x,y,z),$ where'+display(vector).rstrip()
    if p['domain']=='y > 0':
        problem+='\n\nWork on the domain $y>0.$'
    problem=normalize_prose(problem)
    worked=solution(potential,field)
    values=[normalize_tex('f(x,y,z)='+tex(item)) for item in bank]
    signature=json.dumps([p['profile'],problem,worked,values],sort_keys=True)
    qid=identity(signature)
    fid=identity(qid+':selection')
    choices=[{':answer/id':identity(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':worked,
       ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
       ':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[p['correct_index']][':answer/id']]}]}
    if difficulty is not None or p['source_difficulty'] is not None:
        q[':question/difficulty']=':question.difficulty/'+difficulty if difficulty else p['source_difficulty']
    return {'knowledge_point':{'db_id':17592186124574,'id':'90458c6e-3d72-5235-a1c0-627fe4fd2855','title':TITLE},'question':q,
     'generation':{'generator_version':VERSION,'template':p['profile'],'profile':p['profile'],
      'source_question_id':p['source_id'],'source_difficulty':p['source_difficulty'],'source_basis':7951,
      'seed':seed,'parameters':{'a':av,'b':bv,'n':frequency if frequency is not None else p['frequency']},
      'domain':p['domain'],'choice_recipes':[c['recipe'] for c in p['choices']],
      'dependencies':{'python':'3.13.5','packages':{'sympy':sp.__version__}}}}


def practice(difficulty, profile, av, bv, frequency, seed, role, position, order_seed):
    """Build the whole bank before assigning its answer-bearing role.

    The five residual pairs are possible truths, not four errors tied to one
    fixed recipe. Zero, signed, omitted and doubled residuals remain eligible.
    Thus bank-only rank/shape/modal cues cannot identify the target. Relative
    to a given truth, the alternatives represent sign, factor or spurious/
    missing integration-function errors. All share Fx, so Fy and Fz matter.
    """
    if difficulty not in ('easy','moderate','hard'):
        raise ValueError('Unknown difficulty')
    p,_,original,_=expressions(profile,av,bv,frequency)
    p=dict(p)
    if difficulty=='easy':
        first=av*x*y
        middle=y*z
        last=z
    elif difficulty=='moderate' and profile==0:
        first=av*x**2*y
        middle=y**2*z
        last=z**2
    else:
        terms=sp.Add.make_args(sp.expand(original))
        first=sp.Add(*(t for t in terms if t.has(x)))
        middle=sp.Add(*(t for t in terms if not t.has(x) and t.has(y)))
        last=sp.expand(original-first-middle)
        middle=middle if middle!=0 else bv*y*z
        last=last if last!=0 else z**2
    rng=random.Random(order_seed)
    coefficients=[-2,-1,0,1,2]
    partners=coefficients[:]
    rng.shuffle(partners)
    bank=[sp.expand(first+c*middle+d*last+C) for c,d in zip(coefficients,partners)]
    potential=bank[role]-C
    chosen=bank.pop(role)
    rng.shuffle(bank)
    bank.insert(position,chosen)
    p['correct_index']=position
    p['profile']=difficulty+':'+p['profile']
    p['choices']=[{'recipe':str(v)} for v in bank]
    field=[sp.diff(potential,v) for v in (x,y,z)]
    record=build_record(p,bank,potential,field,av,bv,frequency,seed,difficulty)
    record['generation']['parameters'].update(role=role,position=position,order_seed=order_seed)
    record['generation']['residual_coefficients']=[coefficients[role],partners[role]]
    return record


def sample(difficulty, count, seed):
    if difficulty not in ('easy','moderate','hard'):
        raise ValueError('Unknown difficulty')
    if count < 0:
        raise ValueError('Count must be nonnegative')
    profiles={'easy':[0], 'moderate':[0,7,9,11,12,13], 'hard':[1,2,3,4,5,6,8,10]}[difficulty]
    rng=random.Random(seed)
    result=[]
    seen=set()
    # Each complete five-item block cycles both the answer position and the
    # residual role in independently shuffled orders; this is batch construction,
    # not a seed replacement or a hand-picked publication batch.
    attempts=0
    while len(result)<count:
        positions=list(range(5)); roles=list(range(5))
        rng.shuffle(positions); rng.shuffle(roles)
        for position,role in zip(positions,roles):
            for _ in range(100):
                attempts+=1
                i=rng.choice(profiles)
                av=rng.choice(VALUES); bv=rng.choice(VALUES)
                nv=rng.choice((2,3,4)) if PROFILES[i]['frequency'] else None
                record=practice(difficulty,i,av,bv,nv,seed,role,position,rng.randrange(2**32))
                qid=record['question'][':question/id']
                if qid not in seen:
                    seen.add(qid);result.append(record);break
            else:
                raise ValueError('Could not construct a distinct residual bank')
            if len(result)==count: return result
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',default='hard')
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    parser.add_argument('--replay-source',action='store_true',help='Replay all 14 original parameter banks; incomplete p0 remains unlabeled')
    args=parser.parse_args()
    try:
        records=[generate(i,seed=args.seed) for i in range(len(PROFILES))] if args.replay_source else sample(args.difficulty,args.count,args.seed)
    except ValueError as error:
        parser.error(str(error))
    json.dump(records,sys.stdout,ensure_ascii=False,indent=2)
    sys.stdout.write('\n')

if __name__=='__main__': main()
