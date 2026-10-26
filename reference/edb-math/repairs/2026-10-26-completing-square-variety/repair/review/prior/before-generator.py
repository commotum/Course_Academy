#!/usr/bin/env python3
"""Seeded, relocatable completing-the-square generator; exact standard-library arithmetic."""
import argparse
import copy
from fractions import Fraction as F
import json
from pathlib import Path
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = {'db_id':17592186184170, 'id':'1481d4a2-64b4-590a-9dbb-c39d3364bb59',
      'title':'Expressions Containing a Negative Linear Term'}
SOURCES = ['2308b4bc-c09f-5f4c-b879-3bb67c92f885', '71bc1100-5cb2-564e-9a6b-89a542c6c7de',
           'b072df2c-3382-5adf-80f6-f89bc73cbee2', '2b5c9b41-1c42-51fb-96be-bf1a1b427a01',
           'aae80fdb-9519-54f8-9106-0189ec7972b1']

def tex(q):
    q=F(q)
    if q.denominator==1:return str(q.numerator)
    return ('-' if q<0 else '')+r'\frac{'+str(abs(q.numerator))+'}{'+str(q.denominator)+'}'

def term(q):
    q=F(q)
    return ('+'+tex(q)) if q>=0 else tex(q)

def polynomial(m,c,v):return v+'^2-'+str(m)+v+(term(c) if c else '')
def square(h,v):return r'\left('+v+'-'+tex(h)+r'\right)^2'
def result(h,k,v):return square(h,v)+(term(k) if k else '')
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/negative-odd-square/v1/'+s))

def finish(problem,solution,fields,difficulty,generation):
    problem,solution=map(normalize_prose,(problem,solution))
    specs=[]
    for key,kind,values,correct in fields:
        specs.append((key,kind,[normalize_tex(x) for x in values],correct))
    identity=json.dumps([problem,solution,specs,difficulty],sort_keys=True)
    qid=uid(identity)
    af=[]
    for key,kind,values,correct in specs:
        fid=uid(qid+'/'+key)
        choices=[{':answer/id':uid(fid+'/'+str(i)),':answer/type':':answer.type/math',':answer/value':x} for i,x in enumerate(values)]
        af.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,
                   ':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[correct][':answer/id']]})
    record={'knowledge_point':copy.deepcopy(KP),'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+difficulty,
        ':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':af},'generation':generation}
    return validate_generated_record(record)

def construct(m,c,v,difficulty):
    c=F(c);h=F(m,2);sq=h*h;k=c-sq
    assert m in range(3,16,2) and v in ('x','y','t','z')
    p=polynomial(m,c,v); final=result(h,k,v)
    grouped=r'\underbrace{'+v+'^2-2\\cdot '+tex(h)+v+'+'+tex(sq)+r'}_{\text{perfect square}}-'+tex(sq)+(term(c) if c else '')
    solution=(f'The half of the linear coefficient is $-{tex(h)}$. **Add and subtract** its square so the expression keeps its value.\n\n'
       +'$$\n\\begin{aligned}\n'+p+'&='+grouped+r' \\'+'\n&='+square(h,v)+'-'+tex(sq)+(term(c) if c else '')+r' \\'+'\n&='+final+'.\n\\end{aligned}\n$$'
       +'\n\nThe minus sign inside the square produces the required linear term $-'+str(m)+v+'$.')
    fields=[]
    if difficulty in ('easy','moderate'):
        sign='+' if k>=0 else '-'
        hint='Halve the linear coefficient, then add and subtract the square of that half. ' if difficulty=='easy' else ''
        problem=f'Complete the square on ${p}$.\n\n'+hint+f'Fill in the nonnegative numbers.\n\n${p}=({v}-$ '+'{{field-1}} $)^2'+sign+'$ {{field-2}}'
        fields=[('field-1','blank',[tex(h)],0),('field-2','blank',[tex(abs(k))],0)]
        solution+=f'\n\nThe blanks are ${tex(h)}$ and ${tex(abs(k))}$; the sign before the second blank is already supplied.'
    elif difficulty=='hard':
        reverse=tex(c)+'-'+str(m)+v+'+'+v+'^2'
        problem=f'Rewrite ${reverse}$ in the form $({v}+a)^2+b$. Find the signed numbers $a$ and $b$.\n\n$a=$ '+'{{field-1}}\n\n$b=$ {{field-2}}'
        solution=f'Put the quadratic term first: ${reverse}={p}$.\n\n'+solution
        solution+=f'\n\nComparing with $({v}+a)^2+b$ gives $a=-{tex(h)}$ and $b={tex(k)}$.'
        fields=[('field-1','blank',[tex(-h)],0),('field-2','blank',[tex(k)],0)]
    else:raise ValueError(difficulty)
    return finish(problem,solution,fields,difficulty,{'generator_version':1,'template':difficulty,'profile':'guided-blanks' if difficulty=='easy' else 'completion-blanks' if difficulty=='moderate' else 'signed-parameters',
        'parameters':{'m':m,'c':str(c),'variable':v},'domain':'real variable','remainder_case':'zero' if not k else 'positive' if k>0 else 'negative',
        'source_question_ids':SOURCES,'authored_response':True})

def generate(difficulty,count,seed):
    if difficulty not in ('easy','moderate','hard'):raise ValueError(difficulty)
    if count<0:raise ValueError('count must be nonnegative')
    rng=random.Random(seed);out=[]
    case_order=[-1,0,1];rng.shuffle(case_order)
    # Enumerate the supported mathematical domain, not cosmetic renderings.
    catalog=set()
    for m in range(3,16,2):
        for n in range(-9 if difficulty=='easy' else -17,10 if difficulty=='easy' else 18):
            c=F(m*m+n,4)
            if difficulty!='moderate' or c!=0:catalog.add((m,c))
        if difficulty=='easy':catalog.add((m,F(0)))
    remaining=sorted(catalog)
    if count>len(remaining):raise ValueError(f'Requested {count} distinct questions, but this band has {len(remaining)} semantic instances')
    while len(out)<count:
        # Select the outcome before compatible values. Exhausted finite cases
        # yield to remaining cases instead of stranding unused valid instances.
        case=case_order[len(out)] if len(out)<3 else rng.choice(case_order)
        eligible=[(m,c) for m,c in remaining if (c>F(m*m,4))-(c<F(m*m,4))==case]
        if not eligible:
            live=[s for s in case_order if any((c>F(m*m,4))-(c<F(m*m,4))==s for m,c in remaining)]
            case=rng.choice(live)
            eligible=[(m,c) for m,c in remaining if (c>F(m*m,4))-(c<F(m*m,4))==case]
        zero_original=[(m,c) for m,c in remaining if c==0]
        if difficulty=='easy' and len(out)>=3 and rng.randrange(4)==0 and zero_original:eligible=zero_original
        m,c=rng.choice(eligible);remaining.remove((m,c))
        v=rng.choice(('x','y','t','z'))
        r=construct(m,c,v,difficulty)
        r['generation'].update({'seed':seed,'sample_index':len(out)})
        out.append(r)
    return out

def enum(x):return x.get(':db/ident') if isinstance(x,dict) else x

def replay_sources():
    out=[]
    for q in json.loads(Path(__file__).with_name('source-replay.json').read_text()):
        fields=[]
        for f in q[':question/answer-fields']:
            vals=[a[':answer/value'] for a in f[':answer-field/choices']]
            correct=f[':answer-field/correct']
            cid=correct[':answer/id'] if isinstance(correct,dict) else correct[1]
            ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==cid)
            fields.append((f[':answer-field/key'],enum(f[':answer-field/type']).split('/')[-1],vals,ci))
        out.append(finish(q[':question/problem'],q[':question/worked-solution'],fields,enum(q[':question/difficulty']).split('/')[-1],
          {'mode':'source-replay','source_question_ids':[q[':question/id']]}))
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='easy')
    p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0)
    p.add_argument('--format',choices=['json'],default='json');p.add_argument('--replay-source',action='store_true')
    a=p.parse_args()
    if a.count<0:p.error('count must be nonnegative')
    print(json.dumps(replay_sources() if a.replay_source else generate('easy' if a.difficulty=='unclassified' else a.difficulty,a.count,a.seed),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
