#!/usr/bin/env python3
"""Exact exponential equations with answer roles chosen after a symmetric bank."""
import argparse
import copy
import itertools
import json
import math
from pathlib import Path
import random
import uuid
from math_format import checked_math_content, normalize_prose, normalize_tex

VERSION = '2.0.0'
KP = {'db_id':17592186110593, 'id':'34f4b65e-b93a-51e8-b943-b3b53d47fffb',
      'title':'Finding Exact Solutions to Exponential Equations Using Logarithms'}
SOURCE_IDS = ['q-25124','q-66805','q-100163','q-66801']
OFFSETS = tuple(range(-6,0))+tuple(range(1,7))


def identity(value):
    return str(uuid.uuid5(uuid.UUID(KP['id']), value))


def shifted(text, offset):
    return text if offset == 0 else text+('+' if offset > 0 else '-')+str(abs(offset))


def expression(role):
    base, rhs, offset = role
    return shifted(rf'\log_{{{base}}}({rhs})', offset)


def role_value(role):
    base, rhs, offset = role
    return math.log(rhs)/math.log(base)+offset


@checked_math_content
def build(roles, chosen_role, *, order=None, seed=None):
    """Every role in the same bank can be correct in a same-skill equation."""
    roles = [tuple(r) for r in roles]
    if len(roles) != 5 or len(set(roles)) != 5 or not 0 <= chosen_role < 5:
        raise ValueError('Five distinct roles and one valid selected role are required')
    if any(not(2 <= b <= 9 and 2 <= r <= 40 and (k == 0 or k in OFFSETS)) for b,r,k in roles):
        raise ValueError('Role outside source-justified easy domain')
    if len({k == 0 for b,r,k in roles}) != 1:
        raise ValueError('A bank must consistently assess direct inversion or additive isolation')
    values = [role_value(r) for r in roles]
    if any(abs(a-b) < 1e-10 for i,a in enumerate(values) for b in values[i+1:]):
        raise ValueError('Equivalent choices')
    base,rhs,offset = roles[chosen_role]
    shift = -offset
    exponent = shifted('x',shift)
    correct = expression(roles[chosen_role])
    problem = f'Find the exact solution of the equation ${base}^{{{exponent}}}={rhs}.$'
    logarithm = rf'\log_{{{base}}}({rhs})'
    solution = ('First, we take' if shift else 'We take')+rf' $\log_{{{base}}}$ of both sides of the equation:'
    solution += '\n\n$$\n'+rf'\begin{{aligned}}{base}^{{{exponent}}}&={rhs}\\\log_{{{base}}}({base}^{{{exponent}}})&={logarithm}\end{{aligned}}'+'\n$$'
    solution += '\n\n'+r'Now, we use the fact that $\log_b(b^c)=c$ to simplify the left-hand side. This gives:'
    solution += '\n\n$$\n'+f'{exponent}={logarithm}.'+'\n$$'
    if shift:
        solution += '\n\nFinally, we solve for $x,$ as follows:\n\n$$\n'
        solution += rf'\begin{{aligned}}{exponent}&={logarithm}\\x&={correct}\end{{aligned}}'+'\n$$'
    solution += f'\n\nTherefore, the solution is $x={correct}$.'
    texts = [normalize_tex('x='+expression(r)) for r in roles]
    qid = identity(json.dumps([problem,sorted(texts),texts[chosen_role]],separators=(',',':')))
    fid = identity(qid+'/selection')
    choices = [{':answer/id':identity(fid+'/'+text),':answer/type':':answer.type/math',':answer/value':text} for text in texts]
    order = list(range(5)) if order is None else list(order)
    if sorted(order) != list(range(5)):raise ValueError('Invalid display permutation')
    field = {':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
             ':answer-field/choices':[choices[i] for i in order],':answer-field/correct':[':answer/id',choices[chosen_role][':answer/id']]}
    return {'knowledge_point':KP.copy(),'question':{':question/id':qid,':question/difficulty':':question.difficulty/easy',
        ':question/problem':normalize_prose(problem),':question/worked-solution':normalize_prose(solution),':question/answer-fields':[field]},
        'generation':{'generator_version':VERSION,'template':'direct' if not shift else 'shifted',
            'profile':'same-skill-role-bank','parameters':{'b':base,'r':rhs,'s':shift},
            'bank_roles':roles,'selected_role':chosen_role,'display_order':order,'seed':seed,
            'source_question_ids':SOURCE_IDS,'authored_extension':'Bank assembled before choosing which inverse equation to ask; each answer role is eligible.'},'assets':{}}


def draw_roles(rng, shifted_case):
    # Reject a BANK before choosing its key. A superficial bank property cannot
    # thereby privilege any of its five eligible answer roles.
    for _ in range(1000):
        bases = rng.sample(range(2,10),2)
        arguments = rng.sample(range(2,41),2 if shifted_case else 3)
        offsets = rng.sample(OFFSETS,3) if shifted_case else [0]
        roles = rng.sample(list(itertools.product(bases,arguments,offsets)),5)
        if shifted_case and not(any(k>0 for b,r,k in roles) and any(k<0 for b,r,k in roles)):
            continue
        if len({b for b,r,k in roles}) < 2 or len({r for b,r,k in roles}) < 2:
            continue
        values = [role_value(r) for r in roles]
        if any(abs(a-b)<1e-10 for i,a in enumerate(values) for b in values[i+1:]):continue
        return roles
    raise ValueError('Could not draw a valid role bank')


def generate(difficulty='easy', count=5, seed=0):
    if difficulty != 'easy':raise ValueError('Only easy is supported by the source evidence')
    if type(count) is not int or not 0 <= count <= 1000:raise ValueError('count must be in 0..1000')
    rng = random.Random(seed)
    records,seen = [],set()
    for _ in range(max(1000,count*100)):
        if len(records) == count:return records
        roles = draw_roles(rng,bool(rng.getrandbits(1)))
        chosen = rng.randrange(5)
        base,rhs,offset = roles[chosen]
        semantic = (base,rhs,-offset)
        if semantic in seen:continue
        order = rng.sample(range(5),5)
        records.append(build(roles,chosen,order=order,seed=seed));seen.add(semantic)
    raise ValueError('Requested count exceeds practical finite semantic coverage')


def replay_source(source_id):
    """Replay complete current source banks, including documented local repairs."""
    fixtures = json.loads(Path(__file__).with_name('source-fixtures.json').read_text())
    if source_id not in fixtures:raise ValueError('Unknown source question')
    q = copy.deepcopy(fixtures[source_id])
    return {'knowledge_point':KP.copy(),'question':q,'generation':{'generator_version':VERSION,'source_replay':True,
        'source_question_ids':[source_id],'profile':'captured-source-bank'},'assets':{}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',default='easy',choices=('easy','moderate','hard'))
    parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=('json',),default='json');parser.add_argument('--replay-source',choices=SOURCE_IDS)
    args=parser.parse_args()
    try:records=[replay_source(args.replay_source)] if args.replay_source else generate(args.difficulty,args.count,args.seed)
    except ValueError as error:parser.error(str(error))
    print(json.dumps(records,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
