#!/usr/bin/env python3
"""Relocatable power-rule generator. No repository, network, database or asset writes."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import gcd
from pathlib import Path
import random
import sys
import uuid
from math_format import checked_math_content, normalize_prose, normalize_tex

VERSION = '1.1.1'
KP = {'db_id': 17592186064303, 'id': '0b64073e-4aa0-551c-b914-98420b0be338',
      'title': 'Using the Power Rule with Fractional Exponents'}
SOURCE = json.loads(Path(__file__).with_name('source-cases.json').read_text())
BY_ID = {q[':question/math-academy-id']: q for q in SOURCE}
REFS = {'pure': 'q-2971', 'negative': 'q-60579', 'hard': 'q-104647',
        'moderate': 'q-104646', 'target': 'q-86657', 'compound': 'q-2973'}
ORIGINAL = {
 'pure': dict(m=3,d=4,v='e'),
 'negative': dict(m=-12,d=3,v='y'),
 'hard': dict(m=7,b=4,d=3,c=2,v='u'),
 'moderate': dict(m=3,b=2,d=4,v='r'),
 'target': dict(m=3,d=5,v='x'),
 'compound': dict(m=2,d=5,c=4,v='b'),
}

def uid(text):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy/power-rule/v1/' + text))

def frac(q):
    q = F(q)
    return str(q.numerator) if q.denominator == 1 else rf'\frac{{{q.numerator}}}{{{q.denominator}}}'

def slash(q):
    q = F(q)
    return str(q.numerator) if q.denominator == 1 else f'{q.numerator}/{q.denominator}'

def power(base, exp):
    return '{' + base + '}^{' + str(exp) + '}'

def radical(base, m, d):
    index = '' if d == 2 else f'[{d}]'
    return r'\sqrt' + index + '{' + power(base,m) + '}'

def base_for(t,p):
    if t == 'compound': return f'({p["c"]}{p["v"]})'
    if t == 'hard': return r'(\frac{' + str(p['c']) + '}{' + p['v'] + '})'
    return p['v']

def rational_power(base, q):
    q=F(q)
    if q < 0: return r'\frac{1}{' + power(base,slash(-q)) + '}'
    return power(base,slash(q))

def answer_for(t,p,q):
    if t == 'target': return frac(q)
    if t in ('moderate','hard'): return radical(base_for(t,p),q.numerator,q.denominator)
    return rational_power(base_for(t,p),q)

def result(t,p):
    return F(p['m'], p['d'] * (p['b'] if t in ('moderate','hard') else 1))

def chain(items):
    return '$$\n' + r'\begin{aligned}' + items[0] + ' &= ' + (r' \\ &= '.join(items[1:])) + r'\end{aligned}' + '\n$$'

def prompt_solution(t,p):
    B=base_for(t,p); m=p['m']; d=p['d']; q=result(t,p)
    if t in ('moderate','hard'):
        inner=F(m,p['b']) if t=='moderate' else F(1,p['b'])
        outer=F(1,d) if t=='moderate' else F(m,d)
        given=power('(' + power(B,slash(inner)) + ')',slash(outer))
        prompt=f'The equivalent radical expression for ${given}$ is'
        solution='First, we apply the power rule and then we express the resulting fractional power as a radical:\n\n'
        solution+=chain([given,power(B,'('+slash(inner)+')('+slash(outer)+')'),power(B,slash(q)),answer_for(t,p,q)])
    else:
        given=radical(B,m,d)
        if t=='target': prompt=f'Given that ${given}={power(B,"n")},$ what is $n?$'
        elif t=='compound': prompt=f'${given}$ is equivalent to'
        else: prompt=f'What is ${given}$?'
        items=[given,power('('+power(B,m)+')',f'1/{d}'),power(B,str(m)+r'\cdot (1/'+str(d)+')'),power(B,slash(q))]
        if q<0: items.append(rational_power(B,q))
        solution='First, we convert the radical to a fractional exponent, and then we apply the power rule:\n\n'+chain(items)
        if t=='target': solution+='\n\nTherefore, $n='+frac(q)+'.$'
    return prompt,solution

def source_bank(t,p):
    """Each ordered recipe corresponds one-to-one to the captured complete bank."""
    m=p['m']; d=p['d']; B=base_for(t,p); q=result(t,p)
    if t=='pure':
        exps=[q,F(m*d),F(d,m),F(1,m),-q]; values=[rational_power(B,e) for e in exps]; key=0
    elif t=='negative':
        exps=[F(m+d),-q,F(-m*d),q,F(m*d)]; values=[rational_power(B,e) for e in exps]; key=3
    elif t=='moderate':
        b=p['b']; pairs=[(m,b*d),(b,m*b*d),(d,m*b),(d,m+b),(b*d,m)]
        exps=[F(n,k) for k,n in pairs]; values=[radical(B,n,k) for k,n in pairs]; key=4
    elif t=='hard':
        b=p['b']; pairs=[(d,b*m),(b*d,m),(b*m,d),(m,2*d),(m,b*d)]
        exps=[F(n,k) for k,n in pairs]; values=[radical(B,n,k) for k,n in pairs]; key=1
    elif t=='target':
        exps=[F(d,m),q,F(1,m),F(1,d),F(m,d-1)];values=[frac(e) for e in exps];key=1
    else:
        c=p['c'];v=p['v']
        values=[power(f'({c**m}{v})',f'1/{d}'),power(B,f'{d}/{m}'),
                power('('+str(c)+power(v,m)+')',f'1/{d}'),power(B,f'{m}/{d}'),
                str(c)+v+r'\sqrt'+f'[{d}]'+'{'+str(c)+v+'}']
        # Compound errors are not all powers of B; validation parses the complete objects.
        exps=[None,F(d,m),None,q,None];key=3
    return values,key,exps

def near_bank(t,p,rng,bank=None):
    """Uniform-key bank; explicit parameters condition on their given exponent."""
    q=result(t,p)
    if bank is None:
        case='proper' if q<1 else 'improper'
        candidates=EXPONENT_POOLS[t,case]
        if q not in candidates: raise ValueError('exponent outside supported pool')
        bank=[q]+rng.sample([e for e in candidates if e!=q],4)
    exps=list(bank)
    if len(set(exps))!=5 or q not in exps:raise ValueError('invalid complete exponent bank')
    return [answer_for(t,p,e) for e in exps],exps.index(q),exps

@checked_math_content
def make(t,p,*,seed=0,profile='near-miss',shuffle=True,replay=False,bank=None):
    p=dict(p);rng=random.Random(str(seed));prompt,solution=prompt_solution(t,p)
    original=BY_ID[REFS[t]]
    if profile=='source': values,key,exps=source_bank(t,p)
    elif profile=='near-miss': values,key,exps=near_bank(t,p,rng,bank)
    else: raise ValueError('unknown bank profile')
    # Domain clarification is deliberately separate from original prompt mathematics.
    if t=='negative': domain=f'Assume ${p["v"]}\\ne 0$.'
    elif t=='pure' and p['v']=='e': domain=''
    else: domain=f'Assume ${p["v"]}>0$.'
    prompt=normalize_prose(prompt + ('\n\n'+domain if domain else ''))
    solution=normalize_prose(solution);values=[normalize_tex(v) for v in values]
    difficulty={'target':'easy','compound':'easy','moderate':'moderate','hard':'hard','pure':'easy','negative':'moderate'}[t]
    # Identity does not depend on random position, seed, or UUIDs.
    ident=json.dumps([prompt,sorted(values),values[key],difficulty],ensure_ascii=False)
    qid=uid(ident);fid=uid(qid+'/selection')
    answers=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct=answers[key][':answer/id']
    order=list(range(5))
    if shuffle:rng.shuffle(order)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
           ':answer-field/choices':[answers[i] for i in order],':answer-field/correct':[':answer/id',correct]}
    origdiff=original.get(':question/difficulty',{}).get(':db/ident')
    return {'knowledge_point':KP.copy(),'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+difficulty,
             ':question/problem':prompt,':question/answer-fields':[field],':question/worked-solution':solution},
            'generation':{'generator_version':VERSION,'template':t,'bank_profile':profile,'seed':seed,'parameters':p,
              'bank_assignment':'uniform key after bank sampling' if bank is not None else 'conditioned on explicit parameters',
              'source_question_id':original[':question/id'],'source_math_academy_id':REFS[t],
              'source_difficulty':origdiff,'source_replay':replay,
              'domain':'nonzero real' if t=='negative' else 'positive real',
              'case':'proper' if abs(result(t,p))<1 else 'improper',
              'answer_exponents':[None if exps[i] is None else str(exps[i]) for i in order]}}

# Enumerated eligible evidence, not seed-dependent rejection that could hide cases.
def eligible(t,case):
    nums=range(2,18 if t=='hard' else 12 if t=='moderate' else 6 if t=='compound' else 10)
    ds=range(2,7 if t in ('moderate','hard') else 8 if t=='compound' else 10)
    bs=range(2,7 if t=='hard' else 6) if t in ('moderate','hard') else [1]
    out=[]
    for m in nums:
        for b in bs:
            for d in ds:
                n=b*d
                if gcd(m,n)!=1 or m==n or ((m<n)!=(case=='proper')):continue
                out.append((m,b,d))
    return out

POOLS={(t,c):eligible(t,c) for t in ('target','compound','moderate','hard') for c in ('proper','improper')}
EXPONENT_POOLS={k:sorted({F(m,b*d) for m,b,d in pool}) for k,pool in POOLS.items()}
FACTORS={(t,c,q):[(m,b,d) for m,b,d in POOLS[t,c] if F(m,b*d)==q]
         for (t,c),pool in EXPONENT_POOLS.items() for q in pool}


def generate(difficulty,count,seed):
    if difficulty=='unclassified': difficulty='easy'
    if difficulty not in ('easy','moderate','hard'):raise ValueError('unsupported difficulty')
    if count<0:raise ValueError('count must be nonnegative')
    rng=random.Random(seed);records=[];seen=set();attempts=0
    while len(records)<count:
        attempts+=1
        if attempts>max(100,count*100):raise ValueError('requested count exhausted practical unique pool')
        t=rng.choice(['target','compound']) if difficulty=='easy' else difficulty
        case=rng.choice(['proper','improper'])
        bank=rng.sample(EXPONENT_POOLS[t,case],5)
        q=rng.choice(bank)
        m,b,d=rng.choice(FACTORS[t,case,q])
        p={'m':m,'d':d,'v':rng.choice({'target':'xyz','compound':'xyz','moderate':'rst','hard':'uvw'}[t])}
        if t in ('moderate','hard'):p['b']=b
        if t in ('compound','hard'):p['c']=rng.randint(2,6)
        itemseed=rng.getrandbits(64)
        rec=make(t,p,seed=itemseed,bank=bank)
        identity=rec['question'][':question/id']
        if identity in seen:continue
        seen.add(identity);rec['generation']['batch_seed']=seed;rec['generation']['attempt']=attempts;records.append(rec)
    return records

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',default='easy',choices=['unclassified','easy','moderate','hard'])
    ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json'],default='json')
    a=ap.parse_args()
    try: print(json.dumps(generate(a.difficulty,a.count,a.seed),ensure_ascii=False,indent=2))
    except ValueError as e:ap.error(str(e))
if __name__=='__main__':main()
