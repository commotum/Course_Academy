#!/usr/bin/env python3
"""Seeded, relocatable hard power-sum integration generator. No external writes."""
import argparse
from fractions import Fraction as F
import itertools
import json
from math import gcd
from pathlib import Path
import random
import re
import uuid
from math_format import checked_math_content, normalize_prose, normalize_tex

KP = {'db_id':17592186184155,'id':'007f3355-427a-5da4-8af7-22581f1cb1de',
      'title':'Integrating Sums of Power Functions'}
VERSION='1.0.0-format-audit-9122-v1'
ROLES = ('fractional','integer','reciprocal')


def rat(x):
    x=F(x)
    return str(x.numerator) if x.denominator==1 else rf'\frac{{{x.numerator}}}{{{x.denominator}}}'


def power(p, radical=False):
    p=F(p)
    if not p: return '1'
    if p==1: return 'x'
    if radical and p.denominator>1:
        inside='x' if abs(p.numerator)==1 else rf'x^{{{abs(p.numerator)}}}'
        return (rf'\sqrt{{{inside}}}' if p.denominator==2 else rf'\sqrt[{p.denominator}]{{{inside}}}')
    return rf'x^{{{rat(p)}}}'


def term(c,p,radical=True):
    c,p=F(c),F(p)
    if not c:return '0'
    negative_power=radical and p<0
    base=power(-p if negative_power else p,radical)
    numerator=str(abs(c.numerator)) if abs(c.numerator)!=1 or not p else ''
    denominator=str(c.denominator) if c.denominator!=1 else ''
    if negative_power: denominator+=base
    elif p: numerator+=base
    if not numerator:numerator='1'
    return (rf'\frac{{{numerator}}}{{{denominator}}}' if denominator else numerator)


def expression(terms,radical=True):
    out=''
    for c,p in terms:
        c,p=F(c),F(p)
        out+=('-' if c<0 else '+' if out else '')+term(c,p,radical)
    return out


def primitive(terms):
    return [(F(c)/(F(p)+1),F(p)+1) for c,p in terms]


def split_integrals(terms):
    out=''
    for c,p in terms:
        c,p=F(c),F(p)
        out+=('-' if c<0 else '+' if out else '')
        out+=(rat(abs(c)) if abs(c)!=1 else '')+rf'\int {power(p)}\,\mathrm{{d}}x'
    return out


def solution(terms):
    original=expression(terms)
    powers=expression(terms,False)
    steps=''
    for index,(c,p) in enumerate(terms):
        if index==2:steps+=r'\\ &\quad '
        c,p=F(c),F(p)
        steps+=('-' if c<0 else '+' if steps else '')
        steps+=(rat(abs(c)) if abs(c)!=1 else '')
        steps+=rf'\left(\frac{{x^{{{rat(p)}+1}}}}{{({rat(p)}+1)}}\right)'
    return normalize_prose('Using the sum and constant factor rules, we get\n\n$$\n'+
        r'\begin{aligned}& '+rf'\int\left({original}\right)\,\mathrm{{d}}x'+r'\\ &= '+rf'\int\left({powers}\right)\,\mathrm{{d}}x'+
        r'\\ &= '+split_integrals(terms)+r'\\ &= '+steps+r'+C\\ &= '+
        expression(primitive(terms))+r'+C.\end{aligned}'+'\n$$')


def wrong_terms(c,p,seed=0):
    """Three distinct source-grounded term errors, including exponent mistakes."""
    c,p=F(c),F(p);q=p+1;correct=c/q
    candidates=[('omit_division',c),('multiply_new_exponent',c*q),
                ('reverse_sign',-correct),('divide_original_exponent',c/p),
                ('double_correct',2*correct),('halve_correct',correct/2),
                ('divide_new_exponent_twice',c/(q*q))]
    if p+2:candidates.append(('divide_next_exponent',c/(p+2)))
    candidates=[(name,(value,q)) for name,value in candidates]
    candidates.extend([('unchanged_exponent',(correct,p)),
                       ('decrement_exponent',(correct,p-1))])
    if p.denominator>1:candidates.append(('opposite_new_exponent',(correct,-q)))
    random.Random(str(seed)).shuffle(candidates)
    out=[]
    for name,value in candidates:
        if value!=(correct,q) and all(value!=v for _,v in out):out.append((name,value))
        if len(out)==3:return out
    raise AssertionError('coefficient-error domain exhausted')


def sample_design(rng):
    profile=rng.choice(['negative_fractional','positive_fractional'])
    order=rng.choice(list(itertools.permutations(range(3))))
    # Build an answer-neutral binary bank first: every candidate has repeated
    # evidence in every column. Choose which candidate is true independently.
    cube=list(itertools.product((0,1),repeat=3))
    for attempts in range(1,10001):
        bank=rng.sample(cube,5)
        if any(sum(row[j] for row in bank) not in (2,3) for j in range(3)):continue
        pivot=rng.randrange(5)
        correct=bank[pivot]
        recipe=[rng.randrange(1,4) for _ in range(3)]
        states=[[0 if row[j]==correct[j] else recipe[j] for j in range(3)]
                for i,row in enumerate(bank) if i!=pivot]
        return profile,order,states,attempts
    raise RuntimeError('could not sample eligible error assignment')


def sample_parameters(rng,profile):
    d=rng.choice([3,5,7])
    r=rng.choice([r for r in range(1,d) if gcd(r,d)==1])
    p=F(-(d+1),d) if profile=='negative_fractional' else F(r,d)
    coefficients=[rng.choice([-1,1])*rng.randint(1,6) for _ in range(3)]
    return list(zip(coefficients,[p,F(rng.randint(1,7)),F(-rng.randint(2,6))]))


def assemble(prompt,worked,banks,key,difficulty,metadata):
    prompt,worked=normalize_prose(prompt),normalize_prose(worked)
    values=[normalize_tex(v) for v in banks]
    assert len(values)==5 and len(set(values))==5
    basis=json.dumps([prompt,worked,sorted(values),values[key]],ensure_ascii=False)
    qid=uuid.uuid5(uuid.UUID(KP['id']),basis)
    fid=uuid.uuid5(qid,'field:selection')
    choices=[{':answer/id':str(uuid.uuid5(fid,value)),':answer/type':':answer.type/math',
              ':answer/value':value} for value in values]
    q={':question/id':str(qid),':question/problem':prompt,':question/worked-solution':worked,
       ':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',
       ':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,
       ':answer-field/correct':[':answer/id',choices[key][':answer/id']]}]}
    if difficulty:q[':question/difficulty']=':question.difficulty/'+difficulty
    return {'knowledge_point':KP.copy(),'question':q,'generation':{'version':VERSION,**metadata}}


def stringify(terms):return [[str(c),str(p)] for c,p in terms]


@checked_math_content
def generate(seed=0,*,parameters=None,design=None,difficulty='hard'):
    if difficulty not in ('hard','unclassified'):raise ValueError('Only hard is supported; moderate lacks source fields; easy lacks evidence.')
    rng=random.Random(seed)
    if design is None:profile,order,states,attempts=sample_design(rng)
    else:
        profile=design['profile'];order=tuple(design['order']);states=design['states'];attempts=0
    terms=sample_parameters(rng,profile) if parameters is None else [(F(c),F(p)) for c,p in parameters]
    validate_instance(profile,order,states,terms)
    answer=primitive(terms)
    errors=[wrong_terms(c,p,f'{seed}:recipes:{j}') for j,(c,p) in enumerate(terms)]
    candidates=[answer]
    for row in states:
        candidates.append([answer[j] if state==0 else errors[j][state-1][1] for j,state in enumerate(row)])
    rows=[([0,0,0],candidates[0])]+list(zip(states,candidates[1:]))
    rng.shuffle(rows)
    presented=[terms[j] for j in order]
    key=next(i for i,(row,_) in enumerate(rows) if not any(row))
    metadata={'seed':seed,'template':profile,'bank_profile':'distributed-term-errors',
       'parameters':stringify(terms),'role_order':[ROLES[j] for j in order],
       'order':list(order),'design_states':states,'assignment_attempts':attempts,
       'candidate_states':[row for row,_ in rows],
       'bank_terms':[stringify([ts[j] for j in order]) for _,ts in rows],
       'error_recipes':[[name for name,_ in err] for err in errors],
       'domain':'real x != 0; one integration constant on each connected interval',
       'source_references':['q-113848','q-113850','e-373'],'dependencies':{'python':'3.13.5','packages':{}}}
    return assemble('Find the antiderivative of\n$'+expression(presented)+r'.$ For real $x\ne 0$.',
                    solution(presented),[expression([ts[j] for j in order])+'+C' for _,ts in rows],key,'hard',metadata)


def validate_instance(profile,order,states,terms):
    assert profile in ('negative_fractional','positive_fractional')
    assert sorted(order)==[0,1,2]
    assert len(terms)==3
    for c,p in terms:assert F(c).denominator==1 and 1<=abs(c)<=6
    p=F(terms[0][1]);d=p.denominator
    assert d in (3,5,7)
    assert p==F(-(d+1),d) if profile=='negative_fractional' else 0<p<1
    assert terms[1][1].denominator==1 and 1<=terms[1][1]<=7
    assert terms[2][1].denominator==1 and -6<=terms[2][1]<=-2
    assert len(states)==4 and all(len(row)==3 and any(row) and all(s in range(4) for s in row) for row in states)
    assert len(set(map(tuple,states)))==4
    assert all(any(row[j]==0 for row in states) for j in range(3))


def reflow_source_solution(text):
    # Preserve every mathematical token; avoid aligning all RHSs after a wide LHS.
    return re.sub(r'(\\begin\{aligned\})(.*?)\s*&\s*=',
                  lambda m:m[1]+'& '+m[2]+r'\\ &= ',text,count=1,flags=re.S)


@checked_math_content
def replay_source(name):
    rows=json.loads(Path(__file__).with_name('source_cases.json').read_text())
    row=next(r for r in rows if r['source_name']==name)
    if 'banks' not in row:raise ValueError('Source has no answer fields; no faithful replay available.')
    q=row['source'];terms=[(F(c),F(p)) for c,p in row['input']]
    diff=q.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1] or None
    return assemble(q[':question/problem'],reflow_source_solution(q[':question/worked-solution']) if ':question/worked-solution' in q else solution(terms),
        [a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']],row['key'],diff,
        {'template':'source-replay','source_name':name,'source_id':q[':question/id'],
         'source_difficulty':diff,'key_origin':row['key_origin'],
         'solution_origin':'supplied' if ':question/worked-solution' in q else 'authored',
         'parameters':row['input'],'bank_terms':row['banks'],'eligible_for_learning':False})


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',default='hard',choices=['unclassified','easy','moderate','hard'])
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    parser.add_argument('--replay-source',choices=['q-2250','q-29830','q-113848','q-113850'])
    args=parser.parse_args()
    if args.count<0:parser.error('--count must be nonnegative')
    if args.replay_source:records=[replay_source(args.replay_source)]
    else:
        if args.difficulty not in ('hard','unclassified'):parser.error('Only hard generation is supported.')
        rng=random.Random(args.seed)
        records=[generate(rng.getrandbits(64),difficulty=args.difficulty) for _ in range(args.count)]
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
