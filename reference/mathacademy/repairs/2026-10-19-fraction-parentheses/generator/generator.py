#!/usr/bin/env python3
"""Seeded moderate practice for powers of two quotients; database-free."""
import argparse
import copy
import itertools
import json
from pathlib import Path
import random
import uuid
from fractions import Fraction as F

import sympy as S
from math_format import checked_math_content, normalize_prose, normalize_tex

VERSION = '1.1.0'
KP = {'db_id': 17592186110660, 'id': '422bde20-bd83-5a20-b708-734b585ac256',
      'title': 'Using the Power of Quotient Rule with Two Fractions'}
SOURCE_IDS = {'separate': '12eb7643-9611-58a5-926c-4abbb115bd9f',
              'literal': '3cbc76cf-73cd-53cf-89d7-15a5f1f46f2b',
              'scaled': '22efbe5c-dc42-517a-9c47-dc7951665162',
              'numerators': '7d8ea34f-b406-5bc8-9c00-de65d72e9d6d'}
NAMESPACE = uuid.UUID('42602f7a-ab19-4ad7-84ad-059f6564a539')


def uid(data):
    return str(uuid.uuid5(NAMESPACE, json.dumps(data, sort_keys=True)))


def tex(expr):
    return normalize_tex(S.latex(S.cancel(expr), order='none'))


def frac(a, b):
    return r'\frac{' + str(a) + '}{' + str(b) + '}'


def power(a, n):
    return r'\left(' + str(a) + r'\right)^{' + str(n) + '}'


def display(lines):
    return '$$\n' + r'\begin{aligned}' + r' \\ '.join(lines) + r'\end{aligned}' + '\n$$'


def monomial(c, exponents, variables):
    expr = S.Rational(c.numerator, c.denominator)
    for v, e in zip(variables, exponents):
        expr *= S.Symbol(v) ** e
    return expr


def bank_data(t, d):
    """Exact coefficient/exponent tuples; all five members of one profile."""
    p, q = d['p'], d['q']
    if t == 'separate':
        a, b = d['a'], d['b']
        k = F(b**q, a**p)
        coeffs = [F(1, a*a), F(b**q, a)]
        options = [(F(b,a), (q,-p)), (F(a,b), (q,-p))]
        for i,c in enumerate(coeffs):
            options.append((k*k/c if d['mask'] & (1 << i) else c, (p,-q)))
        key = (k,(p,-q))
    elif t == 'scaled':
        a,b,c = d['a'],d['b'],d['c']
        k = F(a*c**p,b)
        coeffs = [F(a,b), F(b,a)]
        options = []
        for i,c0 in enumerate(coeffs):
            options.append((k*k/c0 if d['mask'] & (1 << i) else c0, (-p,-q)))
        options += [(F(a,b),(-1,-1)), (F(a,b),(-p,-p))]
        key = (k,(-p,-q))
    elif t == 'numerators':
        a,b,c = d['a'],d['b'],d['c']
        k = F(b**q,a**p*c**q)
        # Compound arithmetic/power errors: do not repeat the key coefficient
        # on both uniform-power errors (that exposes a middle-degree shortcut).
        options = [(k/b if d['mask'] & 4 else k*b,(p,p)),
                   (k/c if d['mask'] & 8 else k*c,(q,q))]
        for i,c0 in enumerate([F(1,a**p*c**q), F(b**q,a*c)]):
            options.append((k*k/c0 if d['mask'] & (1 << i) else c0, (p,q)))
        key = (k,(p,q))
    else:
        pos = d['negative_position']
        def literal(i,j,reverse=False):
            sign = (-1)**([i,j][pos])
            return (F(sign), (i,-i,-j,j) if reverse else (i,-i,j,-j))
        key = literal(p,q)
        options = [(key[0],literal(p,p)[1]), (key[0],literal(q,q)[1]), literal(p,q,True)]
        options = [(c * (-1 if d.get('mask',0) & (1 << i) else 1), exps) for i,(c,exps) in enumerate(options)] + [(-key[0],key[1])]
    return options + [key]


def assigned_variables(t,d,variables):
    """Only same-side aliases; distinct input names are reusable slot labels."""
    v=list(variables)
    mode=d.get('base_mode','distinct')
    if t=='literal':
        if mode in ('numerators','both'):v[2]=v[0]
        if mode in ('denominators','both'):v[3]=v[1]
        if set(v[::2]) & set(v[1::2]):raise ValueError('cross-side aliases unsupported')
    elif mode=='shared' and t in ('scaled','numerators'):
        v[1]=v[0]
    elif t=='separate' and len(set(v))!=2:
        raise ValueError('cross-side aliases unsupported')
    return v


def valid(t,d):
    variables=assigned_variables(t,d,list('abcd') if t=='literal' else list('xy'))
    vals=[]
    for c,exps in bank_data(t,d):
        merged={}
        for v,e in zip(variables,exps):merged[v]=merged.get(v,0)+e
        vals.append((c,tuple(sorted((v,e) for v,e in merged.items() if e))))
    return len(set(vals)) == 5


def candidates(t, case, mask=0):
    """Small finite domains; choosing a decision case precedes compatible values."""
    out=[]
    for p,q in itertools.permutations(range(2,5),2):
        if ('less' if p<q else 'greater') != case['direction']:
            continue
        if t=='literal':
            pos=case['negative_position']
            if [p,q][pos] % 2 != case['parity']:
                continue
            d={'p':p,'q':q,'negative_position':pos,'mask':mask,'base_mode':case.get('base_mode','distinct')}
            if valid(t,d):out.append(d)
        elif t=='separate':
            for a,b in itertools.product(range(2,6), repeat=2):
                k=F(b**q,a**p)
                kind='unit' if k==1 else 'proper' if k<1 else 'improper'
                d={'a':a,'b':b,'p':p,'q':q,'mask':mask}
                if kind==case['coefficient_case'] and valid(t,d):out.append(d)
        else:
            for a,b,c in itertools.product(range(2 if t=='numerators' else 1,6),range(2,6),range(2,6)):
                k=F(b**q,a**p*c**q) if t=='numerators' else F(a*c**p,b)
                kind=('unit' if k==1 else 'proper' if k<1 else 'improper') if t=='numerators' else ('below_inverse' if k<F(b,a) else 'above_inverse' if k>F(b,a) else 'equal')
                d={'a':a,'b':b,'c':c,'p':p,'q':q,'mask':mask,'base_mode':case.get('base_mode','distinct')}
                if kind==case['coefficient_case'] and valid(t,d):out.append(d)
    return out


def decision_cases(t):
    for direction in ['less','greater']:
        if t=='literal':
            for pos,parity,mode in itertools.product(range(2),range(2),['distinct','numerators','denominators','both']):
                yield {'direction':direction,'negative_position':pos,'parity':parity,'base_mode':mode}
        else:
            kinds=(['proper','unit','improper'] if t=='separate' or (t=='numerators' and direction=='less') else ['proper'] if t=='numerators' else ['below_inverse','above_inverse'])
            for kind,mode in itertools.product(kinds,['distinct'] if t=='separate' else ['distinct','shared']):
                yield {'direction':direction,'coefficient_case':kind,'base_mode':mode}


# Cache every compatible numeric instance by requested case/profile; no rejection loop.
def profile_count(t):
    return 16 if t=='numerators' else 8 if t=='literal' else 4


DOMAINS = {}
for _t in SOURCE_IDS:
    for _case in decision_cases(_t):
        for _mask in range(profile_count(_t)):
            _pool=candidates(_t,_case,_mask)
            if not _pool:
                raise RuntimeError(('empty declared decision case',_t,_case,_mask))
            DOMAINS[(_t,json.dumps(_case,sort_keys=True),_mask)] = _pool


@checked_math_content
def build(t, params, variables=None, shuffle_seed=0, metadata=None):
    d=copy.deepcopy(params)
    p,q=d['p'],d['q']
    variables=variables or (['a','b','c','d'] if t=='literal' else ['s','t'] if t=='separate' else ['v','u'])
    variables=assigned_variables(t,d,variables)
    vals=bank_data(t,d)
    if not valid(t,d):raise ValueError('bank collision')
    expressions=[monomial(c,e,variables) for c,e in vals]
    if len(set(expressions))!=5:raise ValueError('bank collision after variable assignment')
    key=expressions[-1]
    if t=='separate':
        x,y=variables;a,b=d['a'],d['b']
        left=power(frac(x,a),p)+power(frac(b,y),q)
        step1=frac(power(x,p),power(a,p))+r'\cdot '+frac(power(b,q),power(y,q))
        step2=frac(f'{x}^{{{p}}}',a**p)+r'\cdot '+frac(b**q,f'{y}^{{{q}}}')
        step3=frac(f'{b**q}{x}^{{{p}}}',f'{a**p}{y}^{{{q}}}')
    elif t=='scaled':
        x,y=variables;a,b,c=d['a'],d['b'],d['c']
        left=frac(a,b)+power(frac(c,x),p)+power(frac(1,y),q)
        step1=frac(a,b)+r'\cdot '+frac(power(c,p),power(x,p))+r'\cdot '+frac(power(1,q),power(y,q))
        step2=frac(a,b)+r'\cdot '+frac(c**p,f'{x}^{{{p}}}')+r'\cdot '+frac(1,f'{y}^{{{q}}}')
        step3=frac(a*c**p,f'{b}{x}^{{{p}}}{y}^{{{q}}}')
    elif t=='numerators':
        x,y=variables;a,b,c=d['a'],d['b'],d['c']
        left=power(frac(x,a),p)+power(frac(str(b)+y,c),q)
        step1=frac(power(x,p),power(a,p))+r'\cdot '+frac(power(str(b)+y,q),power(c,q))
        step2=frac(f'{x}^{{{p}}}',a**p)+r'\cdot '+frac(f'{b**q}{y}^{{{q}}}',c**q)
        step3=frac(f'{b**q}{x}^{{{p}}}{y}^{{{q}}}',a**p*c**q)
    else:
        x,y,z,w=variables;pos=d['negative_position']
        n1=('-' if pos==0 else '')+x;n2=('-' if pos==1 else '')+z
        left=power(frac(n1,y),p)+power(frac(n2,w),q)
        step1=frac(power(n1,p),power(y,p))+r'\cdot '+frac(power(n2,q),power(w,q))
        first=(-1)**p if pos==0 else 1
        second=(-1)**q if pos==1 else 1
        step2=frac(('-' if first<0 else '')+f'{x}^{{{p}}}',f'{y}^{{{p}}}')+r'\cdot '+frac(('-' if second<0 else '')+f'{z}^{{{q}}}',f'{w}^{{{q}}}')
        step3=frac(('-' if first*second<0 else '')+f'{x}^{{{p}}}{z}^{{{q}}}',f'{y}^{{{p}}}{w}^{{{q}}}') if d.get('base_mode','distinct')!='distinct' else tex(key)
    prompt=normalize_prose('$'+left+'=$')
    notes=''
    for variable in dict.fromkeys(variables):
        if variables.count(variable)>1:
            notes+=f'\n\nApply the product rule: ${variable}^{{{p}}}{variable}^{{{q}}}={variable}^{{{p}+{q}}}={variable}^{{{p+q}}}$.'
    solution=normalize_prose('We apply the power of quotient rule and simplify:\n\n'+display([
        left+' &= '+step1,'&= '+step2,'&= '+step3]+([] if step3==tex(key) else ['&= '+tex(key)])))
    solution=normalize_prose(solution+notes)
    # IDs use normalized content, not the seed or arbitrary labels.
    identity={'prompt':prompt,'bank':sorted(tex(x) for x in expressions)}
    qid=uid(identity); fid=uid([qid,'selection'])
    choices=[{':answer/id':uid([fid,tex(e)]),':answer/type':':answer.type/math',':answer/value':tex(e)} for e in expressions]
    correct=choices[-1][':answer/id']
    random.Random(shuffle_seed).shuffle(choices)
    profile=('authored-product' if t=='numerators' else 'source') if d.get('mask',0)==0 else ('sign-errors-' if t=='literal' else 'compound-coefficient-' if t=='numerators' else 'reflected-')+str(d['mask'])
    return {'knowledge_point':KP.copy(),'question':{
        ':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,
        ':question/difficulty':':question.difficulty/moderate',
        ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',
        ':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,
        ':answer-field/correct':[':answer/id',correct]}]},
        'generation':{'version':VERSION,'template':t,'profile':profile,'parameters':d,
                      'variables':variables,'source_question_ids':[SOURCE_IDS[t]],
                      'domain':'denominators nonzero','dependencies':{'python':'3.13.5','sympy':S.__version__},
                      **(metadata or {})}}


@checked_math_content
def generate(rng, difficulty='moderate', seed=None, index=0):
    if difficulty!='moderate':raise ValueError('Only moderate is supported for sampling')
    t=rng.choice(list(SOURCE_IDS));case=rng.choice(list(decision_cases(t)))
    mask=rng.randrange(profile_count(t))
    pool=DOMAINS[(t,json.dumps(case,sort_keys=True),mask)]
    d=rng.choice(pool)
    variables=rng.sample(list('abcdefghmnpqrstuvwxy'),4 if t=='literal' else 2)
    return build(t,d,variables,rng.getrandbits(64),{'seed':seed,'index':index,'decision_case':case,
        'compatible_count':len(pool),'sampling':'case/profile then uniform compatible numeric tuple'})


def replay():
    """Immutable original parameters and complete banks, with missing fields repaired."""
    return json.loads(Path(__file__).with_name('source_replay.json').read_text())


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',default='moderate',choices=['easy','moderate','hard','unclassified'])
    ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json'],default='json')
    args=ap.parse_args()
    if args.count<1:ap.error('count must be positive')
    band='moderate' if args.difficulty=='unclassified' else args.difficulty
    if band!='moderate':ap.error('unsupported difficulty; only moderate sampling is supported')
    rng=random.Random(args.seed)
    print(json.dumps([generate(rng,band,args.seed,i) for i in range(args.count)],ensure_ascii=False,indent=2))


if __name__=='__main__':main()
