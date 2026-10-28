#!/usr/bin/env python3
"""Seeded guided integrating-factor questions; all runtime files are local."""
import argparse
import hashlib
import json
import random
import uuid

import sympy as S
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = {'db_id': 17592186217248, 'id': '7cbedeed-6ac6-5ed8-bd25-9a85eda9577b',
      'title': 'Finding an Integrating Factor for an Inexact Equation: Condition on X Satisfied'}
SOURCES = {
    'easy': {'math_academy_id': 'q-337400', 'entity_id': 17592186311851},
    'linear': {'math_academy_id': 'q-337161', 'entity_id': 17592186311807},
    'constant': {'math_academy_id': 'q-337476', 'entity_id': 17592186311852},
    'power': {'math_academy_id': 'q-337523', 'entity_id': 17592186311855},
}
ORIGINAL = {'easy': {'a': 2}, 'linear': {'a': 4, 'b': 3},
            'constant': {'a': 3, 'b': -2}, 'power': {'c': 3, 'k': 1, 'b': 4}}
x, y = S.symbols('x y', real=True)
DX, DY = r'\,\text{d}x', r'\,\text{d}y'
COND = r'\frac{1}{Q}(\frac{\partial P}{\partial y}-\frac{\partial Q}{\partial x})'
FORMULA = r'\exp(\int g(x)\,\text{d}x)'


def tex(expr):
    return normalize_tex(S.latex(expr, order='lex', ln_notation=True))


def exptex(expr):
    return 'e^{' + tex(expr) + '}'


def display(expr):
    return '$$\n' + expr + '\n$$'


def aligned(rows):
    return display(r'\begin{aligned}' + r' \\ '.join(rows) + r'\end{aligned}')


def par(expr):
    return '(' + tex(expr) + ')'


def equation(p, q):
    return par(p) + DX + '+' + ('' if q == 1 else tex(q)) + DY + '=0'


def times_equation(factor, eq):
    return factor + '(' + eq[:-2] + ')=0'


def derive(family, params):
    """Ordered mathematical instance; printing never reorders operator inputs."""
    p = dict(params)
    if family == 'easy':
        a = S.Integer(p['a']); P, Q = a*x*y, S.Integer(1)
        g, F = a*x, a*x**2/2
        given = equation(P, Q)
    elif family == 'linear':
        a, b = S.Integer(p['a']), S.Integer(p['b'])
        P, Q = -a*x*y-b*x, S.Integer(1)
        g, F = -a*x, -a*x**2/2
        given = "y'=" + tex(a*x*y+b*x)
    elif family == 'constant':
        a, b = S.Integer(p['a']), S.Integer(p['b'])
        P, Q = -a*y-b, S.Integer(1)
        g, F = -a, -a*x
        given = "y'=" + tex(a*y+b)
    elif family == 'power':
        c, k, b = (S.Integer(p[v]) for v in ('c', 'k', 'b'))
        d = c*(k+1)
        P, Q = b*x**2+d*y, c*x
        g, F = k/x, k*S.log(x)
        given = tex(c*x) + "y'=" + tex(-d*y-b*x**2)
    else:
        raise ValueError('unknown family')
    factor = tex(x**p['k']) if family == 'power' else exptex(F)
    return dict(P=P, Q=Q, py=S.diff(P,y), qx=S.diff(Q,x), g=g, F=F,
                given=given, factor=factor, eq=equation(P,Q))


def banks(family, p, v):
    """One complete observed bank profile per family; key is first until shuffle."""
    theorem = [COND] + [r'\frac{1}{'+den+r'}(\frac{\partial P}{\partial y}'+sign+r'\frac{\partial Q}{\partial x})'
                           for den, sign in [('P','+'),('Q','+'),('P','-')]]
    formula = [FORMULA, r'\exp(-\int g(x)\,\text{d}x)', r'\exp(g(x))', r'\exp(-g(x))']
    a, b = S.Integer(p.get('a', 0)), S.Integer(p.get('b', 0))
    eq, g, py, qx = (v[z] for z in ('eq','g','py','qx'))
    if family == 'easy':
        conversion = None
        dp = [tex(py), '1', tex(-py), '0']
        dq = ['0','1',tex(py),'-1']
        quotient = [tex(g), tex(-g), exptex(-a*x), exptex(a*x)]
        factors = [v['factor'], exptex(-a*x), exptex(a*x), exptex(-v['F'])]
    elif family == 'linear':
        conversion = [eq, DX+'-'+par(a*x*y)+DY+'=0', equation(b*x-a*x*y,1),
                      DX+'-'+par(a*x*y+b*x)+DY+'=0']
        dp = [tex(py), '1', '0', tex(-b)]
        dq = ['0','x',tex(py),'1']
        quotient = [tex(g),tex(-g),exptex(-a*x/2),exptex(a*x/2)]
        factors = [v['factor'],exptex(a*x),exptex(-v['F']),exptex(-a*x)]
    elif family == 'constant':
        conversion = [eq, DX+'-'+par(a*y+b)+DY+'=0', DX+'-'+par(a*y)+DY+'=0', equation(b,1)]
        dp = [tex(py),'0','1',tex(a)]
        dq = ['0','1',tex(-a),'x']
        quotient = [tex(g),exptex(-a*x),exptex(a*x),tex(a)]
        factors = [v['factor'],exptex(-x**2),exptex(x**2),exptex(a*x)]
    else:
        c, k = S.Integer(p['c']), S.Integer(p['k']); d = c*(k+1)
        conversion = [eq,equation(b*x**2-d*y,c*x), DX+'-'+par(d*y+b*x**2)+DY+'=0',
                      par(v['P'])+DY+'+'+tex(c*x)+DX+'=0']
        if d == 0:
            conversion = [eq, equation(-b*x**2,c*x), equation(b*x**2,1),
                          par(v['P'])+DY+'+'+tex(c*x)+DX+'=0']
        dp = [tex(py),'0',tex(-d),'1'] if d != 0 else ['0','1','-1','x']
        dq = [tex(qx),tex(c*x**2),tex(2*c*x),'0']
        quotient = [tex(g),exptex(-g),tex(-g),exptex(g)]
        factors = [v['factor'],exptex(-k*x),tex(x**(-k)),exptex(k*x)]
    result = [theorem,formula]
    if conversion:
        result.append(conversion)
    result += [dp,dq,quotient,factors,[times_equation(f,eq) for f in factors]]
    return [[normalize_tex(z) for z in bank] for bank in result]


def generate(family, params, rng=None, profile=None, difficulty=None):
    rng = rng or random.Random(0)
    difficulty = difficulty or ('easy' if family == 'easy' else 'moderate')
    if difficulty not in ('easy', 'moderate', 'hard') or (difficulty == 'hard' and family == 'easy'):
        raise ValueError('invalid scaffold for family')
    v = derive(family, params)
    profile = profile or rng.choice(['double', 'half'])
    banklist = banks(family,params,v)
    if profile != 'source':
        if profile not in ('double', 'half'):
            raise ValueError('unknown bank profile')
        scale = S.Integer(2) if profile == 'double' else S.Rational(1, 2)
        multipliers = [S.Integer(1), S.Integer(-1), scale, -scale]
        offset = len(banklist)-5
        for j, name in enumerate(('py', 'qx', 'g')):
            if v[name] != 0:
                banklist[offset+j] = [tex(m*v[name]) for m in multipliers]
        factors = [(tex(x**(m*params['k'])) if (m*params['k']).is_Integer else 'x^{'+tex(m*params['k'])+'}') if family == 'power' else exptex(m*v['F'])
                   for m in multipliers]
        banklist[-2] = factors
        banklist[-1] = [times_equation(f, v['eq']) for f in factors]
    if any(len(set(bank)) != 4 for bank in banklist):
        raise ValueError('duplicate bank')
    n = 0
    def blank():
        nonlocal n
        n += 1
        return '{{field-' + str(n) + '}}'
    intro = ('Suppose we would like to find an **integrating factor** to convert the differential equation\n\n' +
             display(v['given']) + '\n\ninto an exact equation. Select the correct options in the reasoning below.')
    if family == 'power':
        intro += ' Work on the interval $x>0$.'
    else:
        intro += ' Take $x$ to be real.'
    theorem_intro = ('For a differential equation of the form\n\n' + display(r'P(x,y)'+DX+r'+Q(x,y)'+DY+'=0') +
                     '\n\nif\n\n' + display(blank()+'=g(x)') +
                     '\n\nwhere $g(x)$ is independent of $y$, an integrating factor is\n\n' +
                     display('I(x)='+blank()) + '\n\nwhere $\\exp(x)$ denotes $e^x$.')
    prompt = intro + '\n\n' + theorem_intro
    if family != 'easy':
        prompt += '\n\nFirst, rewrite our equation in differential form:\n\n' + display(blank())
    denote = display('P(x,y)='+tex(v['P'])+r',\qquad Q(x,y)='+tex(v['Q']))
    prompt += "\n\nLet's denote\n\n"+denote+'\n\nNow compute the partial derivatives:\n\n'
    prompt += display(r'\frac{\partial P}{\partial y}='+blank())+'\n\n'
    prompt += display(r'\frac{\partial Q}{\partial x}='+blank())+'\n\nSince\n\n'
    prompt += display(COND+'='+blank())+'\n\nis a function of $x$ only, an integrating factor is\n\n'
    prompt += display('I(x)='+blank())+'\n\nand multiplication gives the exact equation\n\n'+display(blank())

    sol = ('For a differential equation of the form\n\n'+display(r'P(x,y)'+DX+r'+Q(x,y)'+DY+'=0')+
           '\n\nif\n\n'+display(COND+'=g(x)')+'\n\nwhere $g(x)$ is independent of $y$, an integrating factor is\n\n'+
           display('I(x)='+FORMULA)+'.\n\nHere $\\exp(x)=e^x$.')
    if family != 'easy':
        sol += '\n\nFirst, rewrite our equation in differential form:\n\n'+display(v['eq'])
    sol += "\n\nLet's denote\n\n"+denote+'\n\nCompute the partial derivatives:\n\n'
    sol += aligned([r'\frac{\partial P}{\partial y}&=\frac{\partial}{\partial y}'+par(v['P'])+'='+tex(v['py']),
                    r'\frac{\partial Q}{\partial x}&=\frac{\partial}{\partial x}'+par(v['Q'])+'='+tex(v['qx'])])
    sol += '\n\nThen\n\n'+aligned([COND+r'&=\frac{1}{'+tex(v['Q'])+'}('+tex(v['py'])+'-('+tex(v['qx'])+'))',
                                     '&='+tex(v['g'])])
    sol += '\n\nThis is a function of $x$ only. Choose the multiplicative constant to be one. Thus\n\n'
    evaluated = tex(v['F'])
    rows = ['I(x)&='+r'\exp(\int ('+tex(v['g'])+r')\,\text{d}x)',
            '&='+r'\exp('+evaluated+')','&='+v['factor']]
    sol += aligned(rows)
    if family == 'power':
        sol += '\n\nOn $x>0$, the power rule for logarithms gives $\\exp(k\\ln x)=x^k$.'
    sol += '\n\nMultiply the original differential equation by this integrating factor:\n\n'
    sol += aligned(['I(x)('+v['eq'][:-2]+')&=I(x)\\cdot 0',
                    times_equation(v['factor'],v['eq']).replace('=0','&=0')])
    if difficulty == 'hard':
        # Keep the mathematical instance and remove only the guiding checkpoints.
        banklist = [banklist[2], banklist[-3], banklist[-2], banklist[-1]]
        convention = (' Work on $x>0$ and choose $I(1)=1$.' if family == 'power'
                      else ' Take $x$ to be real and choose the multiplicative constant to be one.')
        prompt = ('Find an **integrating factor** depending on $x$ alone that makes the equation exact:\n\n'
                  + display(v['given']) + '\n\nUse the differential form obtained by moving the right-hand side '
                  'to the left and multiplying by $\\text{d}x$, without dividing by the coefficient of '
                  "$y'$. In this form, $P$ is the coefficient of $\\text{d}x$ and $Q$ is the coefficient "
                  'of $\\text{d}y$.' + convention
                  + '\n\nDifferential form:\n\n' + display('{{field-1}}')
                  + '\n\nCompute the quotient:\n\n' + display(COND + '={{field-2}}')
                  + '\n\nAn integrating factor is\n\n' + display('I(x)={{field-3}}')
                  + '\n\nand multiplication gives the exact equation\n\n' + display('{{field-4}}'))
    elif family == 'power':
        prompt += "\n\nUse the displayed differential form without dividing by the coefficient of $y'$, and choose $I(1)=1$."
    else:
        prompt += '\n\nChoose the multiplicative constant to be one.'
    prompt, sol = normalize_prose(prompt), normalize_prose(sol)
    # Identities depend on normalized content and the complete bank, never the seed or ordering.
    content = json.dumps([prompt,sol,banklist],sort_keys=True)
    qid = uuid.uuid5(uuid.UUID(KP['id']),hashlib.sha256(content.encode()).hexdigest())
    fields = []
    for i, bank in enumerate(banklist,1):
        fid = uuid.uuid5(qid,'field-'+str(i)); choices=[]
        for val in bank:
            aid = str(uuid.uuid5(fid,val))
            choices.append({':answer/id':aid, ':answer/type':':answer.type/math', ':answer/value':val})
        correct = choices[0][':answer/id']; rng.shuffle(choices)
        fields.append({':answer-field/id':str(fid),':answer-field/key':'field-'+str(i),
                       ':answer-field/type':':answer-field.type/select',':answer-field/choices':choices,
                       ':answer-field/correct':[':answer/id',correct]})
    record = {'knowledge_point':KP,'question':{':question/id':str(qid),':question/problem':prompt,
              ':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+difficulty,
              ':question/answer-fields':fields},
              'generation':{'generator_version':4,'template':family,'bank_profile':profile,'scaffold':difficulty,
                            'parameters':params,'domain':'x>0' if family=='power' else 'real x',
                            'source_references':[SOURCES[family]],'source_difficulty':'easy' if family=='easy' else 'moderate'}}
    return validate_generated_record(record)


def sample_params(family,rng):
    sign = rng.choice([-1,1])
    if family == 'easy': return {'a':sign*rng.choice([2,4,6,8])}
    if family == 'linear': return {'a':sign*rng.choice([2,4,6,8]),'b':rng.choice([-7,-5,-3,-2,2,3,5,7])}
    if family == 'constant': return {'a':sign*rng.randint(2,6),'b':rng.choice([-7,-5,-3,-2,2,3,5,7])}
    return {'k':rng.choice([-3,-2,-1]) if sign<0 else rng.choice([1,2,3]),'c':rng.randint(2,5),
            'b':rng.choice([-7,-5,-4,-2,2,4,5,7])}



def decision_ranks(family, params, profile, difficulty):
    """Bank-only numerical ranks for sampled arithmetic fields.

    Track only assessed numerical entries. The theorem and the always-zero
    Q_x checkpoint in constant-Q families are legitimate fixed recall targets.
    The zero P_y cancellation stays eligible, but must not accidentally give
    a mixed zero/nonzero family a constant rank selector.
    """
    values = derive(family, params)
    names = ['g', 'F'] if difficulty == 'hard' else ['py', 'qx', 'g', 'F']
    scale = S.Integer(2) if profile == 'double' else S.Rational(1, 2)
    result = {}
    for name in names:
        if name == 'qx' and family != 'power':
            continue
        value = values[name].subs(x, 2)
        if value == 0:
            # The distinct zero-derivative bank is [0, 1, -1, x].
            result[name] = (1, True)
        else:
            errors = [value, -value, scale*value, -scale*value]
            rank = sorted(range(4), key=lambda index: errors[index]).index(0)
            result[name] = (rank, False)
    return result


def batch(difficulty,count,seed):
    if difficulty == 'unclassified': difficulty='moderate'
    if difficulty not in ('easy','moderate','hard'): raise ValueError('Unsupported difficulty: '+difficulty)
    if count<0: raise ValueError('count must be nonnegative')
    # Finite semantic catalogs sampled without replacement; choose rule family before coefficients.
    rng=random.Random(seed); result=[]; used=set(); attempts=0
    occurrences={}; profile_start={}; position_previous={}; rank_history={}
    capacity = 8 if difficulty=='easy' else 8*8+10*8+6*4*8
    if count>capacity: raise ValueError(f'Request exceeds finite semantic capacity {capacity}')
    while len(result)<count:
        attempts+=1
        if attempts>capacity*100: raise ValueError('Unable to fill finite batch')
        family = 'easy' if difficulty=='easy' else rng.choice(['linear','constant','power'])
        occurrence=occurrences.get(family,0)
        if family not in profile_start:
            profile_start[family]=rng.randrange(2)
        profile=['double','half'][(profile_start[family]+occurrence)%2]
        params=sample_params(family,rng); key=(family,tuple(sorted(params.items())))
        if key in used: continue
        try: rec=generate(family,params,rng,profile=profile,difficulty=difficulty)
        except ValueError: continue
        ranks = decision_ranks(family, params, profile, difficulty)
        history = rank_history.setdefault(family, {})
        if any(history.get(name) and len({old[0] for old in history[name]}) == 1
               and rank == history[name][0][0]
               and not (zero and all(old[1] for old in history[name]))
               for name, (rank, zero) in ranks.items()):
            continue
        for name, rank in ranks.items():
            history.setdefault(name, []).append(rank)
        # Keep repeated recognizable families from acquiring an always-select-
        # position cue in a small practice pool. Draw afresh from the other
        # positions rather than imposing a predictable rotation. Wrong choices
        # retain their independent shuffle.
        ff=rec['question'][':question/answer-fields']
        if family not in position_previous:
            position_previous[family]=[None for _ in ff]
        for j,field in enumerate(ff):
            choices=field[':answer-field/choices']
            correct=next(z for z in choices if z[':answer/id']==field[':answer-field/correct'][1])
            choices.remove(correct)
            position=rng.choice([i for i in range(4) if i!=position_previous[family][j]])
            choices.insert(position,correct)
            position_previous[family][j]=position
        occurrences[family]=occurrence+1
        used.add(key); rec['generation']['seed']=seed
        result.append(rec)
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--difficulty',required=True,choices=['unclassified','easy','moderate','hard'])
    p.add_argument('--count',required=True,type=int);p.add_argument('--seed',required=True,type=int)
    p.add_argument('--format',choices=['json'],default='json');a=p.parse_args()
    print(json.dumps(batch(a.difficulty,a.count,a.seed),ensure_ascii=False,indent=2))


if __name__=='__main__': main()
