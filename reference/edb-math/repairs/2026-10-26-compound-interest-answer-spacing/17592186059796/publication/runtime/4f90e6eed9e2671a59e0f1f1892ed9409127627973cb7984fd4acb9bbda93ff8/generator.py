"""Seeded initial-amount practice. No service, database, or asset writes."""
import argparse
import json
import math
from pathlib import Path
import random
import uuid
from decimal import Decimal, localcontext
from rounded_finance import initial_bank, away_from_halfway
from rounded_finance import minimum_gap, separated
from math_format import normalize_prose, validate_generated_record

KP = '0c9581f5-67cb-5752-8a45-b84ba4f3577e'
SOURCES = json.loads(Path(__file__).with_name('source_cases.json').read_text())
NS = uuid.UUID('d39eeb28-0ede-44a5-bb40-fde995110054')

def uid(s):
    return str(uuid.uuid5(NS, s))

def dec(n):
    return format(Decimal(str(n)).normalize(), 'f')

def make(context, current, percent, time, rank, position, rng, replay=False):
    places = 0 if context == 'profit' else 2
    unit = 10**places
    rate = Decimal(str(percent))/100
    exponent = rate*time
    with localcontext()as ctx:
        ctx.prec=50
        raw=Decimal(str(current))*(-exponent).exp()
        key=int((raw*unit).to_integral_value(rounding='ROUND_HALF_UP'))
    show = lambda n: f'{n/unit:.{places}f}'
    source = SOURCES[0 if context == 'profit' else 1]
    if replay:
        bank = [7889,7783,7852,7900,7921] if context=='profit' else [337,305,327,343,319]
        prompt = source[':question/problem']
        profile = 'observed-offset-bank'
    else:
        raw,key,bank,recipes=initial_bank(current,rate,time,places,rank,position,rng)
        direction = '*growing*' if percent>0 else '*decreasing*'
        if context=='profit':
            prompt = (f'A forex trader\'s annual profits have been {direction} continuously at a rate of '
                      f'${dec(abs(percent))}\\%$ per year. Her profit this year is $\\${dec(current)}$. '
                      f'What was her profit ${time}$ years ago? Round your answer to the nearest dollar.')
        else:
            prompt = (f'The average gas price in Chicago is $\\${current:.2f}$ per gallon. '
                      f'Gas prices have been {direction} continuously at a rate of ${dec(abs(percent))}\\%$ per month. '
                      f'What was the gas price ${time}$ months ago? Round your answer to the nearest cent.')
        prompt += '\n\n> A scientific calculator is required to answer this question.'
        profile = 'separated-calculation-errors-v2'
    if key not in bank or len(set(bank)) != 5:
        raise ValueError('Invalid bank')
    p = dec(current); r=dec(rate); rt=dec(exponent)
    periods = 'years' if context=='profit' else 'months'
    sign = 'positive for growth' if percent>0 else 'negative for decay'
    final = show(key)
    solution = (f'Use the continuously compounded growth equation $P=P_0e^{{rt}}$. '
                f'The current amount is $P={p}$, the rate is $r={r}$ ({sign}), '
                f'and the elapsed time is $t={time}$ {periods}. The time unit matches the rate. '
                'Substitute and divide by the exponential factor:\n\n$$\n\\begin{aligned}\n'
                f'{p} &= P_0e^{{({r})({time})}} \\\\\n'
                f'{p} &= P_0e^{{{rt}}} \\\\\n'
                f'e^{{{rt}}} &\\approx {math.exp(float(exponent)):.8f} \\\\\n'
                f'P_0 &= \\frac{{{p}}}{{e^{{{rt}}}}} \\\\\n'
                f'&\\approx {raw:.8f} \\\\\n'
                f'&\\approx {final}\n\\end{{aligned}}\n$$\n\n'
                f'The earlier {"profit" if context=="profit" else "gas price"} was '
                f'$\\${final}$'+(' per gallon.' if context=='gas' else '.')+
                ' Round only the final amount; keep full calculator precision in the exponential factor.')
    prompt,solution = map(normalize_prose,(prompt,solution))
    texts = [normalize_prose('$\\$'+show(n)+'$'+(' per gallon' if context=='gas' else '')) for n in bank]
    # Normalize all learner-visible content before deriving identities.
    qid = uid(json.dumps([prompt,solution,sorted(texts)],ensure_ascii=False))
    fid = uid(qid+'/selection')
    choices = [{':answer/id':uid(fid+'/'+v), ':answer/type':':answer.type/text', ':answer/value':v} for v in texts]
    q = {':question/id':qid, ':question/difficulty':':question.difficulty/moderate',
         ':question/problem':prompt, ':question/worked-solution':solution, ':question/requires-calculator':True,
         ':question/answer-fields':[{':answer-field/id':fid, ':answer-field/key':'selection',
         ':answer-field/type':':answer-field.type/radio', ':answer-field/choices':choices,
         ':answer-field/correct':[':answer/id',choices[bank.index(key)][':answer/id']]}]}
    record = {'knowledge_point':{'db_id':17592186059796,'id':KP,'title':'Calculating an Initial Amount'},'question':q,'generation':{'batch_contract':'rounded-finance-spacing-v1','generator_version':2,'knowledge_point_id':KP,
       'template':context,'bank_profile':profile,'bank_recipes':recipes if not replay else ['source_replay']*5,'bank_minimum_gap_units':minimum_gap(key,context),'rounding_places':places,'unrounded_answer':str(raw),'source_difficulty':None,
       'source_ids':[source[':db/id'],source[':question/id'],source[':question/math-academy-id']],
       'supporting_examples':['e-5166',17592186059595,'e-5185',17592186059597],
       'parameters':{'current':current,'percent':percent,'time':time},
       'domain':'positive amount; nonzero signed rate; positive elapsed time',
       'final_expression':final}}
    return validate_generated_record(record)

def generate(count,seed,difficulty='moderate'):
    if difficulty not in ('moderate','unclassified'):
        raise ValueError('Unsupported difficulty: '+difficulty)
    if count < 0: raise ValueError('count must be nonnegative')
    rng=random.Random(seed); result=[]; seen=set(); cases=[]
    for i in range(count):
        if i%5==0:
            ranks=list(range(5)); positions=list(range(5)); rng.shuffle(ranks);rng.shuffle(positions)
        if not cases:
            cases=[(c,s) for c in ('profit','gas') for s in (-1,1)];rng.shuffle(cases)
        context,sign=cases.pop()
        for attempt in range(2000):
            current=rng.randrange(8000,40001,50) if context=='profit' else rng.randint(200,600)/100
            percent=sign*(rng.randint(2,18) if context=='profit' else rng.randint(5,30)/10)
            time=rng.randint(2,8 if context=='profit' else 10)
            semantic=(context,current,percent,time)
            if semantic in seen:continue
            with localcontext()as ctx:
                ctx.prec=50
                trial=Decimal(str(current))*(-Decimal(str(percent))/100*time).exp()
            if not away_from_halfway(trial,0 if context=='profit'else 2):continue
            try: record=make(context,current,percent,time,ranks[i%5],positions[i%5],rng)
            except ValueError as e:
                if str(e).startswith('Insufficient'):continue
                raise
            seen.add(semantic);record['generation'].update(seed=seed,index=i);result.append(record);break
        else:raise RuntimeError('No separated source-supported bank within bounded attempts')
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='moderate');ap.add_argument('--count',type=int,default=5)
    ap.add_argument('--seed',type=int,required=True);ap.add_argument('--format',choices=['json'],default='json');a=ap.parse_args()
    print(json.dumps(generate(a.count,a.seed,a.difficulty),indent=2))
