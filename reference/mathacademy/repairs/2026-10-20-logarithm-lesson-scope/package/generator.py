#!/usr/bin/env python3
"""Seeded, relocatable logarithm-law generator. No assets or I/O writes."""
import argparse
import copy
from fractions import Fraction as F
import itertools
import json
from pathlib import Path
import random
import re
import uuid
from math_format import checked_math_content, normalize_prose, normalize_tex

KP = '5dd9426d-8ce3-564d-85c5-4ae82289325d'
PROFILES = ('integer-expand', 'root-expand', 'powers-expand', 'combine-revised')
ALL_PROFILES = PROFILES + ('numeric-combine',)
NUMERIC_CASES = tuple(itertools.product((2, 3, 4), (1, -1)))
SIGNS = tuple(s for s in itertools.product((-1, 1), repeat=3) if len(set(s)) == 2)
BASES = ('10', 'e', '2', '3', '5')
SOURCE_IDS = ('d039db42-48a7-5fd4-9b98-e0ab1ba34d9c', '34847574-efca-5670-8924-e70a3bcc31ce', 'e3b649a8-d282-53b7-b8c8-e883fd47c0b9', '3e2b66a0-666e-508e-a538-22e2d9fb9285')

def banks(profile, p, q):
    h = F(1, 2)
    rows = {
        'integer-expand': [(1,-1,-p),(1,-p,1),(1,p,-1),(p,1,-1),(p,-1,-1)],
        'root-expand': [(p,h,1),(h,p,-1),(p,-h,-1),(p,-p,-1),(h,-p,1)],
        'powers-expand': [(p,q,-h),(p,q,h),(1,-1,-h),(p,1,-h),(1,1,h)],
        'combine-revised': [(p,q,-h),(p,-F(q,2),-h),(1,q,-h),(p,1,-h),(q,p,-h)],
    }[profile]
    return [tuple(map(F, row)) for row in rows]

def log(base, arg):
    name = r'\ln' if base == 'e' else r'\log' if base == '10' else r'\log_{'+base+'}'
    return name + r'\left(' + arg + r'\right)'

def number(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else r'\frac{'+str(x.numerator)+'}{'+str(x.denominator)+'}'

def power(var, exponent):
    exponent = F(exponent)
    if exponent == 1: return var
    if exponent == F(1,2): return r'\sqrt{'+var+'}'
    return var + '^{'+number(exponent)+'}'

def parts(vector):
    return [''.join(power(v,abs(c)) for v,c in zip('xyz',vector) if c*sgn > 0) or '1' for sgn in (1,-1)]

def argument(vector):
    num, den = parts(vector)
    return num if den == '1' else r'\frac{'+num+'}{'+den+'}'

def expanded(base, vector, order=(0,1,2), powered=False):
    terms=[]
    for i in order:
        c=vector[i]
        term = log(base, power('xyz'[i],abs(c))) if powered else ('' if abs(c)==1 else number(abs(c))) + log(base,'xyz'[i])
        terms.append(('-' if c<0 else '+' if terms else '')+term)
    return ''.join(terms)

def solution(base, vector, direction, order=(0,1,2)):
    lhs=log(base,argument(vector)); rhs=expanded(base,vector,order)
    num,den=parts(vector)
    grouped=log(base,num)+'-'+log(base,den)
    powered=expanded(base,vector,order,powered=True)
    display=lambda t:'$$\n'+t+'\n$$'
    if direction=='expand':
        text='The laws of logarithms are:\n\n- $'+log('n','a')+'+'+log('n','b')+'='+log('n','ab')+'$ — the product rule\n\n- $'+log('n','a')+'-'+log('n','b')+'='+log('n',r'\frac{a}{b}')+'$ — the quotient rule\n\n- $'+log('n','c^{m}')+'=m'+log('n','c')+'$ — the power rule\n\n'
        text+='Using the quotient rule for logarithms, we get:\n\n'+display(lhs+'='+grouped)
        text+='\n\nNow, using the product rule for logarithms, we obtain\n\n'+display(grouped+'='+powered)
        root_note=' (a square root is a power of one half)' if any(abs(c)==F(1,2) for c in vector) else ''
        text+='\n\nFinally, using the power rule for logarithms'+root_note+', we have\n\n'+display(powered+'='+rhs)
    else:
        text='Using the power rule for logarithms, we can rewrite the terms as follows:\n\n'+display(rhs+'='+powered)
        text+='\n\nNow, using the product rule for logarithms, we combine the factors with the same sign:\n\n'+display(powered+'='+grouped)
        text+='\n\nFinally, using the quotient rule for logarithms, we get\n\n'+display(grouped+'='+lhs)
    return text+'\n\nTherefore,\n\n'+display(lhs+'='+rhs if direction=='expand' else rhs+'='+lhs)+ '\n\nThese identities hold for $x,y,z>0$.'

def uid(parent,text): return str(uuid.uuid5(uuid.UUID(parent),text))

def record(problem, values, target, worked, meta):
    def reflow(match):
        tex=match.group(1).replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace(r'\\','').replace('&','')
        sides=[part.strip() for part in tex.split('=')]
        if len(sides)<2: return match.group(0)
        return '$$\n'+r'\begin{aligned}& '+(r' \\ &= '.join(sides))+r'\end{aligned}'+'\n$$'
    worked=re.sub(r'\$\$\n(.*?)\n\$\$',reflow,worked,flags=re.S)
    problem,worked=map(normalize_prose,(problem,worked))
    values=list(map(normalize_tex,values))
    assert len(set(values))==5
    qid=uid(KP,json.dumps([problem,sorted(values),values[target]],ensure_ascii=False))
    fid=uid(qid,'selection')
    choices=[{':answer/id':uid(fid,v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    q={':question/id':qid,':question/difficulty':':question.difficulty/moderate',':question/problem':problem,':question/worked-solution':worked,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[target][':answer/id']]}]}
    return {'knowledge_point':{'db_id':17592186054625,'id':KP},'question':q,'generation':{'version':'1.2.0-source-scope','domain':'x,y,z>0; base>0, base!=1',**meta}}

def numeric_coefficients(omitted, a, d):
    return [F(a**p, d)**s for i, (p, s) in enumerate(NUMERIC_CASES) if i != omitted]

def numeric_parameters(omitted):
    # Whole-bank compatibility, independent of the selected target.
    return [(a, d) for a in (2, 3) for d in sorted({2,3,4,5,6,a**2,a**3,a**4-a,a**4})
            if len(set(numeric_coefficients(omitted, a, d))) == 5]

def scalar_argument(c, variable_sign):
    c = F(c)
    numerator = (str(c.numerator) if c.numerator != 1 else '') + ('x' if variable_sign == 1 else '')
    denominator = (str(c.denominator) if c.denominator != 1 else '') + ('x' if variable_sign == -1 else '')
    numerator = numerator or '1'
    return numerator if not denominator else r'\frac{' + numerator + '}{' + denominator + '}'

@checked_math_content
def build_numeric(omitted, target, a, d, variable_sign=1, base='10', order=(0,1,2), choice_order=(0,1,2,3,4)):
    if omitted not in range(6) or target not in range(5): raise ValueError('invalid numerical assignment')
    if (a, d) not in numeric_parameters(omitted): raise ValueError('incompatible numerical bank')
    if variable_sign not in (-1, 1) or base not in BASES: raise ValueError('invalid numerical sign/base')
    for seq, n in ((order, 3), (choice_order, 5)):
        if sorted(seq) != list(range(n)): raise ValueError('invalid permutation')
    cases = [case for i, case in enumerate(NUMERIC_CASES) if i != omitted]
    p, s = cases[target]
    if s != 1 or variable_sign != 1 or tuple(order) not in ((0,1,2),(1,0,2)):
        raise ValueError('Source scope requires a positive powered constant and variable, followed by one subtracted constant')
    signs = (s, variable_sign, -s)
    def terms(args, coefficients=(1,1,1)):
        result = ''
        for i in order:
            result += ('-' if signs[i] < 0 else '+' if result else '')
            result += (str(coefficients[i]) if coefficients[i] != 1 else '') + log(base, args[i])
        return result
    expression = terms((str(a), 'x', str(d)), (p,1,1))
    powered = terms((power(str(a), p), 'x', str(d)))
    evaluated = terms((str(a**p), 'x', str(d)))
    factors = (str(a**p), 'x', str(d))
    num, den = [''.join(sorted((f for f, sign in zip(factors, signs) if sign == side), key=lambda f: f == 'x')) for side in (1,-1)]
    grouped = log(base, num) + '-' + log(base, den)
    quotient = log(base, r'\frac{' + num + '}{' + den + '}')
    coefficients = numeric_coefficients(omitted, a, d)
    values = [log(base, scalar_argument(c, variable_sign)) for c in coefficients]
    answer = values[target]
    display = lambda t: '$$\n' + t + '\n$$'
    worked = 'Using the power rule for logarithms, rewrite the powered numerical term and evaluate the power:\n\n' + display(expression + '=' + powered + '=' + evaluated)
    worked += '\n\nNow, using the product rule for logarithms, combine the factors with the same sign:\n\n' + display(evaluated + '=' + grouped)
    worked += '\n\nFinally, using the quotient rule for logarithms and simplifying the numerical factor, we get\n\n' + display(grouped + '=' + quotient + '=' + answer)
    worked += '\n\nTherefore,\n\n' + display(expression + '=' + answer) + '\n\nThese identities hold for $x>0$.'
    return record('Assume $x>0$.\n\nExpress $' + expression + '$ as a single logarithm.', [values[i] for i in choice_order], choice_order.index(target), worked,
        {'profile':'numeric-combine', 'direction':'combine', 'domain':'x>0; base>0, base!=1', 'omitted':omitted, 'target':target, 'a':a, 'd':d, 'p':p, 'constant_sign':s, 'variable_sign':variable_sign, 'base':base, 'term_order':list(order), 'choice_order':list(choice_order), 'coefficient':str(coefficients[target]), 'bank_coefficients':list(map(str, coefficients)), 'source_question_id':'de20802c-6a7e-5d77-b2ce-26f98dc68b4e', 'extension':'authored five-choice numerical bank; canonical has no captured answer bank'})

@checked_math_content
def build(profile, target, p, q=3, signs=(1,1,-1), perm=(0,1,2), base='10', order=(0,1,2), choice_order=(0,1,2,3,4), raw=False):
    if profile not in PROFILES or target not in range(5): raise ValueError('unsupported profile/target')
    if not 2<=p<=5 or not 2<=q<=5: raise ValueError('powers out of bounds')
    if profile=='powers-expand' and p==q: raise ValueError('distinct powers required')
    if profile=='combine-revised' and (p not in (3,5) or q not in (2,4)): raise ValueError('revised profile bounds')
    if base not in BASES or tuple(signs) not in SIGNS: raise ValueError('invalid base/sign partition')
    for seq,n in ((perm,3),(order,3),(choice_order,5)):
        if sorted(seq)!=list(range(n)): raise ValueError('invalid permutation')
    rows=banks(profile,p,q)
    if not raw:
        mask=[s*(1 if c>0 else -1) for s,c in zip(signs,rows[target])]
        rows=[tuple(row[i]*mask[i] for i in range(3)) for row in rows]
        # perm[i] specifies the visible variable receiving source coordinate i.
        rows=[tuple(row[perm.index(i)] for i in range(3)) for row in rows]
    v=rows[target]
    if sum(c>0 for c in v)!=2 or sum(c<0 for c in v)!=1 or not any(abs(c)!=1 for c in v):
        raise ValueError('Source scope requires two numerator factors, one denominator factor and a non-unit power')
    if [1 if v[i]>0 else -1 for i in order] != [1,1,-1]:
        raise ValueError('Present the positive pair first, followed by the subtracted term')
    direction='combine' if profile=='combine-revised' else 'expand'
    expression=expanded(base,v,order) if direction=='combine' else log(base,argument(v))
    problem=('Express $'+expression+'$ as a single logarithm.' if direction=='combine' else '$'+expression+'=$')
    problem='Assume $x,y,z>0$.\n\n'+problem
    values=[log(base,argument(row)) if direction=='combine' else expanded(base,row,order) for row in rows]
    return record(problem,[values[i] for i in choice_order],choice_order.index(target),solution(base,v,direction,order),{'profile':profile,'direction':direction,'target':target,'p':p,'q':q,'signs':list(signs),'perm':list(perm),'base':base,'term_order':list(order),'choice_order':list(choice_order),'vectors':[[str(c) for c in row] for row in rows],'answer_vector':[str(c) for c in v],'source_question_id':SOURCE_IDS[PROFILES.index(profile)],'extension':'bank-role reassignment' if direction=='expand' else 'revised single-log bank and role reassignment'})

@checked_math_content
def replay(index):
    if index == 4:
        source=json.loads(Path(__file__).with_name('canonical_case.json').read_text())
        adaptation=build_numeric(1, 1, 2, 4)
        values=[a[':answer/value'] for a in adaptation['question'][':question/answer-fields'][0][':answer-field/choices']]
        return record(source[':question/problem'], values, 1, source[':question/worked-solution'], {'profile':'source-replay', 'source_question_id':source[':question/id'], 'original_difficulty':source.get(':question/difficulty'), 'authored_answer_bank':True, 'captured_answer_bank':False, 'domain':'x>0; base>0, base!=1'})
    sources=json.loads(Path(__file__).with_name('source_cases.json').read_text())
    source=next(s for s in sources if s[':question/id']==SOURCE_IDS[index])
    profiles=['integer-expand','root-expand','powers-expand']
    if index in (0,2,3): base=['10','2','3','e'][index]
    else: base='2'
    if index<3:
        params=[(3,2,2),(2,3,1),(2,3,0)][index]
        p,q,target=params
        rows=banks(profiles[index],p,q)
        values=[expanded(base,v) for v in rows]
        vector=rows[target]
        worked=source.get(':question/worked-solution') or solution(base,vector,'expand')
    else:
        target=2; vector=(F(3),F(2),-F(1,2))
        values=[log(base,r'\frac{x^{3}}{\sqrt{y^{2}z}}'),'3'+log(base,r'\frac{xy^{2}}{\sqrt{z}}'),log(base,r'\frac{x^{3}y^{2}}{\sqrt{z}}'),log(base,r'\frac{6xy}{\sqrt{z}}'),r'xy^{2}-\sqrt{z}']
        worked=solution(base,vector,'combine')
    return record(source[':question/problem'],values,target,worked,{'profile':'source-replay','source_question_id':source[':question/id'],'original_difficulty':source.get(':question/difficulty'),'repaired_missing_key':index in (0,3),'repaired_missing_solution':index in (0,3)})

@checked_math_content
def generate(rng, seed=None, index=0):
    profile=rng.choice(ALL_PROFILES)
    target=rng.randrange(5)
    if profile == 'numeric-combine':
        omitted=rng.randrange(6)
        variable_sign=1
        cases=[case for i,case in enumerate(NUMERIC_CASES) if i!=omitted]
        target=rng.choice([i for i,case in enumerate(cases) if case[1]==1])
        a,d=rng.choice(numeric_parameters(omitted))
        r=build_numeric(omitted,target,a,d,variable_sign,rng.choice(BASES),tuple(rng.sample((0,1),2)+[2]),tuple(rng.sample(range(5),5)))
        r['generation'].update(seed=seed,index=index)
        return r
    signs=rng.choice([s for s in SIGNS if s.count(1)==2])
    perm=tuple(rng.sample(range(3),3))
    if profile=='combine-revised': p,q=rng.choice((3,5)),rng.choice((2,4))
    else:
        p=rng.randint(2,5); q=rng.choice([i for i in range(2,6) if i!=p])
    visible=[signs[perm.index(i)] for i in range(3)]
    order=tuple(rng.sample([i for i,s in enumerate(visible) if s>0],2)+[i for i,s in enumerate(visible) if s<0])
    r=build(profile,target,p,q,signs,perm,rng.choice(BASES),order,tuple(rng.sample(range(5),5)))
    r['generation'].update(seed=seed,index=index)
    return r

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--difficulty',required=True,choices=('moderate',))
    parser.add_argument('--count',required=True,type=int)
    parser.add_argument('--seed',required=True,type=int)
    parser.add_argument('--format',required=True,choices=('json',))
    a=parser.parse_args()
    if a.count<0: parser.error('count must be nonnegative')
    rng=random.Random(a.seed)
    print(json.dumps([generate(rng,a.seed,i) for i in range(a.count)],ensure_ascii=False))

if __name__=='__main__': main()
