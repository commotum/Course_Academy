#!/usr/bin/env python3
"""Seeded, relocatable continuous-decay final-amount questions; no I/O except JSON."""
import argparse
from decimal import Decimal, ROUND_HALF_UP, localcontext
import json
import random
import uuid
from rounded_finance import minimum_gap, separated
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = '3dcfc681-0632-57a5-bd1e-e03d91d13f37'
SOURCES = {
    'annual': dict(entity=17592186060058, id='051effd0-f0ca-56ac-80f4-c13fb6384d81', ma='q-1442', initial=4120, percent='3.81', duration=7, start=2009, wrong=[3190,2411,1987,4019]),
    'daily': dict(entity=17592186060059, id='c9077fb0-4ca3-538c-9a63-2f4162f39301', ma='q-1445', initial=9830, percent='18', duration=2, start=None, wrong=[2781,2364,1897,2465]),
}

def rounded(x):
    return int(x.to_integral_value(rounding=ROUND_HALF_UP))

def fmt(x):
    return format(Decimal(x), 'f').rstrip('0').rstrip('.') if '.' in format(Decimal(x),'f') else str(x)

def values(template, initial, percent, duration):
    with localcontext() as ctx:
        ctx.prec=45
        rate=-Decimal(percent)/100
        time=duration*(7 if template=='daily' else 1)
        exponent=rate*time
        factor=exponent.exp()
        answer=rounded(initial*factor)
        return rate,time,exponent,factor,answer,[]

def build(template, initial, percent, duration, start=None, *, position=0, rng=None, seed=None, replay=False, rank=None, bank_override=None):
    rng=rng or random.Random(0)
    rate,time,exponent,factor,answer,wrong=values(template,initial,percent,duration)
    if bank_override is not None:
        wrong=list(bank_override)
    elif replay:
        wrong=list(SOURCES[template]['wrong'])
    else:
        rank = rank if rank is not None else rng.randrange(1,6)
        wrong = rng.sample(range(1,answer),rank-1) + rng.sample(range(answer+1,initial),5-rank)
    if not separated(wrong+[answer],answer,'population'):
        raise ValueError('Rounded answers require source-sized spacing')
    if len(set(wrong+[answer])) != 5:
        raise ValueError('Complete source-profile bank collides')
    percent=fmt(percent)
    if template=='annual':
        prompt=(f'In the year ${start}$, there were approximately ${initial}$ crimes in a particular city. '
                f'The police department then promised a ${percent}\\%$ annual *decrease* in crime, continuously compounded. '
                f'According to this model, how many crimes occurred in ${start+duration}$? Round your answer to the nearest integer.')
        conversion=f'The elapsed time is $t={start+duration}-{start}={time}$ years.'
        conclusion=f'According to this model, approximately ${answer}$ crimes occurred in ${start+duration}$.'
    else:
        prompt=(f'In medieval times, there were ${initial}$ people living in a city struck by a plague. '
                f'If the disease resulted in a daily *decrease* in the population at a continuously compounded rate of ${percent}\\%$, '
                f"what was the city's population after ${duration}$ weeks? Round your answer to the nearest integer.")
        conversion=f'The rate is daily, so convert the duration to days: $t={duration}\\times 7={time}$ days.'
        conclusion=f'After ${duration}$ weeks, the population was approximately ${answer}$ people.'
    prompt+='\n\n> A scientific calculator is required to answer this question.'
    # Truncation with ellipsis, never early rounding in the calculation.
    factor_prefix=format(factor,'.12f')[:9]
    solution=(f'The continuously compounded growth equation is $P=P_0e^{{rt}}$. '
              f'The initial amount is $P_0={initial}$. Since the amount decreases, the signed decimal rate is '
              f'$r=-{percent}/100={fmt(rate)}$. {conversion}\n\n'
              'Substitute these values and round only the final amount:\n\n$$\n\\begin{aligned}\n'
              f'P &= P_0e^{{rt}} \\\\\n'
              f'&= {initial}e^{{({fmt(rate)})({time})}} \\\\\n'
              f'&= {initial}e^{{{fmt(exponent)}}} \\\\\n'
              f'&= {initial}({factor_prefix}\\ldots) \\\\\n'
              f'&\\approx {answer}\n'
              '\\end{aligned}\n$$\n\n'+conclusion)
    prompt,solution=normalize_prose(prompt),normalize_prose(solution)
    bank=list(wrong); rng.shuffle(bank); bank.insert(position,answer)
    # Normalize before content-derived identities; position does not create a new question.
    content=[prompt,solution,sorted(bank)]
    identity=str(uuid.uuid5(uuid.UUID(KP),json.dumps(content,ensure_ascii=False)))
    field_id=str(uuid.uuid5(uuid.UUID(identity),'selection'))
    choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(field_id),str(v))), ':answer/type':':answer.type/math', ':answer/value':normalize_tex(str(v))} for v in bank]
    question={':question/id':identity, ':question/problem':prompt, ':question/worked-solution':solution,
              ':question/difficulty':':question.difficulty/moderate', ':question/requires-calculator':True,
              ':question/answer-fields':[{':answer-field/id':field_id, ':answer-field/key':'selection',
                  ':answer-field/type':':answer-field.type/radio', ':answer-field/choices':choices,
                  ':answer-field/correct':[':answer/id',choices[position][':answer/id']]}]}
    source=SOURCES[template]
    return validate_generated_record({'knowledge_point':{'db_id':17592186059798,'id':KP,'title':'Calculating a Final Amount After Continuous Compounding Is Applied'},
        'question':question,'generation':{'batch_contract':'rounded-finance-spacing-v1','version':'1.1.0-separated','seed':seed,'template':template,'profile':'source-exact-bank' if replay else 'authored-independent-numeric-bank',
        'parameters':dict(initial=initial,percent=percent,duration=duration,start=start),
        'source_question_ids':[source['id']], 'source_entity_ids':[source['entity']], 'source_math_academy_ids':[source['ma']],
        'solution_support':[17592186059597,17592186060946], 'source_difficulty':None,'source_replay':replay,
        'correct_rank':sorted(bank).index(answer)+1}})

def generate(count,seed,difficulty='moderate'):
    if difficulty not in ('moderate','unclassified'):
        raise ValueError('Only moderate is supported by this source')
    if count<0: raise ValueError('count must be nonnegative')
    rng=random.Random(seed); records=[]; seen=set(); last={}; first=rng.randrange(2)
    for i in range(count):
        template=('annual','daily')[(i+first)%2]
        old_rank,old_position=last.get(template,(None,None))
        rank=rng.choice([r for r in range(1,6) if r!=old_rank])
        position=rng.choice([p for p in range(5) if p!=old_position])
        for attempt in range(1000):
            percent=str(Decimal(rng.randrange(1 if template=='annual' else 10,121 if template=='annual' else 201))/10)
            duration=rng.randrange(2 if template=='annual' else 1,13 if template=='annual' else 4)
            initial=rng.randrange(100,2001)*10
            start=rng.randrange(1990,2021) if template=='annual' else None
            try: rec=build(template,initial,percent,duration,start,position=position,rng=rng,seed=seed,rank=rank)
            except ValueError: continue
            if rec['generation']['correct_rank']!=rank or rec['question'][':question/id'] in seen: continue
            seen.add(rec['question'][':question/id']); records.append(rec); last[template]=(rank,position); break
        else: raise RuntimeError('Could not construct distinct complete bank')
    return records

def replay(template):
    s=SOURCES[template]
    return build(template,s['initial'],s['percent'],s['duration'],s['start'],replay=True)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',default='moderate',choices=['unclassified','easy','moderate','hard'])
    parser.add_argument('--count',type=int,required=True)
    parser.add_argument('--seed',type=int,required=True)
    parser.add_argument('--format',choices=['json'],default='json')
    args=parser.parse_args()
    try: records=generate(args.count,args.seed,args.difficulty)
    except (ValueError,RuntimeError) as error: parser.error(str(error))
    print(json.dumps(records,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
