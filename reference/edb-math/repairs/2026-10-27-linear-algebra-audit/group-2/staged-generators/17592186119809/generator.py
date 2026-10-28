#!/usr/bin/env python3
"""Seeded, relocatable plane-membership questions. No services or database access."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import re
import uuid
from math_format import normalize_prose, normalize_tex, validate_prose, validate_generated_record, matrix_tex

KP = {'db_id': 17592186119809, 'id': 'a04b551f-3323-5b91-b01e-941912cc92be',
      'title': 'Determining Whether a Vector Lies on a Plane'}
NON = r'$\mathbf{u}$ does not lie on $\Pi$'
PROFILES = ('coefficients', 'operations', 'quadratic', 'reverse-quadratic')


def tex(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return ('-' if x < 0 else '') + r'\frac{' + str(abs(x.numerator)) + '}{' + str(x.denominator) + '}'


def vector(v):
    return r'\langle ' + ', '.join(tex(x) for x in v) + r'\rangle'


def linear(a, b):
    out = ''
    for value, variable in [(a, 's'), (b, 't')]:
        if not value:
            continue
        term = ('' if abs(value) == 1 else tex(abs(value))) + variable
        out += ('-' if value < 0 else '+' if out else '') + term
    return out or '0'


def display(body):
    return '$$\n' + body + '\n$$'


def equations(b, c, u):
    return r'\left\{\begin{aligned}' + r' \\ '.join(linear(b[i], c[i]) + ' &=' + tex(u[i]) for i in range(3)) + r'\end{aligned}\right.'


def echelon(b, c, u):
    rows = [[F(b[i]), F(c[i]), F(u[i])] for i in range(3)]
    ops = []
    pivot = 0
    for col in range(2):
        source = next((i for i in range(pivot, 3) if rows[i][col]), None)
        if source is None:
            continue
        if source != pivot:
            rows[pivot], rows[source] = rows[source], rows[pivot]
            ops.append(f'R_{pivot+1} \\leftrightarrow R_{source+1}')
        for i in range(pivot+1, 3):
            if rows[i][col]:
                f = rows[i][col] / rows[pivot][col]
                rows[i] = [x-f*y for x,y in zip(rows[i],rows[pivot])]
                ops.append(f'R_{i+1} \\leftarrow R_{i+1}-({tex(f)})R_{pivot+1}')
        pivot += 1
    if pivot != 2:
        raise ValueError('The direction vectors must span a plane')
    return rows, ops


def analyze(b, c, u):
    rows, ops = echelon(b,c,u)
    residual = rows[2][2]
    t = rows[1][2] / rows[1][1]
    s = (rows[0][2] - rows[0][1]*t) / rows[0][0]
    return s,t,not residual,rows,ops


def profile_values(profile,s,t):
    if profile == 'coefficients':
        return [(s*t,'product'),(s,'first coefficient'),(t,'second coefficient'),(s+t,'sum')]
    if profile == 'operations':
        if not t:
            return []
        return [(s*t,'product'),(s+t,'sum'),(s-t,'difference'),(s/t,'quotient')]
    if profile in ('quadratic','reverse-quadratic'):
        difference,recipe = (s-t,'difference') if profile=='quadratic' else (t-s,'reversed difference')
        return [(s*t,'product'),(s+t,'sum'),(difference,recipe),(s*s+t*t,'sum of squares')]
    raise ValueError(profile)


def build(b,c,u,difficulty,profile='coefficients',rng=None,source=None,bank=None):
    b,c,u = [list(map(F,v)) for v in (b,c,u)]
    s,t,member,rows,ops = analyze(b,c,u)
    correct = tex(s*t) if member else NON
    given = r'\begin{aligned}\mathbf{b}&=' + vector(b) + r' \\ \mathbf{c}&=' + vector(c) + r' \\ \mathbf{u}&=' + vector(u) + r'\end{aligned}'
    prompt = (r'Determine whether $\mathbf{u}$ lies on the plane $\Pi:\mathbf{r}=s\mathbf{b}+t\mathbf{c}$, where $s,t\in\mathbb{R}$ and' + '\n\n' + display(given) + '\n\n' +
              r'If it does, select the value of $s\cdot t$ in $\mathbf{u}=s\mathbf{b}+t\mathbf{c}$. Otherwise, select the statement that $\mathbf{u}$ does not lie on $\Pi$.')
    if difficulty == 'easy':
        prompt += '\n\nUse the component equations\n\n' + display(equations(b,c,u)) + '\n\n**Check all three coordinates.** Use the equations that isolate the coefficients, then verify the remaining equation.'
    initial = matrix_tex([[tex(b[i]),tex(c[i]),tex(u[i])] for i in range(3)],augmented=True)
    final = matrix_tex([[tex(x) for x in row] for row in rows],augmented=True)
    solution = (r'By definition, $\mathbf{u}\in\Pi$ exactly when the same values of $s$ and $t$ satisfy all three coordinate equations. Expanding the vector equation gives' + '\n\n' + display(equations(b,c,u)) + '\n\nSet up the augmented matrix:\n\n' + display(initial))
    if ops:
        solution += '\n\nApply ' + ', then '.join('$'+op+'$' for op in ops) + ':\n\n' + display(final)
    if member:
        solution += ('\n\nThe last row is $0=0$, so it adds no restriction. Back substitute in the two nonzero rows:\n\n' +
                     display(r'\begin{aligned}t&=\frac{'+tex(rows[1][2])+'}{'+tex(rows[1][1])+'}='+tex(t)+r' \\ s&=\frac{'+tex(rows[0][2])+'-('+tex(rows[0][1])+')('+tex(t)+')}{'+tex(rows[0][0])+'}='+tex(s)+r'\end{aligned}') +
                     '\n\nVerify every coordinate:\n\n' + display(r'\begin{aligned}'+r' \\ '.join('('+tex(s)+')('+tex(b[i])+')+('+tex(t)+')('+tex(c[i])+')&='+tex(s*b[i]+t*c[i])+'='+tex(u[i]) for i in range(3))+r'\end{aligned}') +
                     '\n\nAll three coordinates agree, so the vector lies on the plane. Therefore,\n\n' + display(r's\cdot t=('+tex(s)+r')\cdot('+tex(t)+')='+tex(s*t)+'.'))
    else:
        solution += ('\n\nThe last row gives $0='+tex(rows[2][2])+'$, a contradiction. No pair satisfies all three equations. Thus '+NON+'. A product obtained from only two coordinates is not a valid answer.')
    if bank is None:
        vals = profile_values(profile,s,t)
        if len(vals) != 4 or len({x for x,_ in vals}) != 4:
            raise ValueError('Profile has coincident choices; resample the entire instance')
        bank = [(tex(value),':answer.type/math',recipe) for value,recipe in vals] + [(NON,':answer.type/text','membership')]
    choices = []
    for value,typ,recipe in bank:
        value = normalize_tex(value) if typ == ':answer.type/math' else normalize_prose(value)
        if value == correct:
            feedback = 'Correct. ' + (r'The common pair satisfies all three equations and gives $s\cdot t='+tex(s*t)+'$.' if member else 'The coordinate system is inconsistent.')
        elif typ == ':answer.type/text':
            feedback = r'The pair $s='+tex(s)+',t='+tex(t)+'$ satisfies all three coordinates; the vector lies on the plane.'
        elif not member:
            feedback = 'Check all three coordinates before giving a product; the system has no common solution.'
        else:
            feedback = {'first coefficient':r'This is $s$ alone; the question asks for $s\cdot t$.',
                        'second coefficient':r'This is $t$ alone; the question asks for $s\cdot t$.',
                        'sum':r'This uses $s+t$ instead of $s\cdot t$.',
                        'difference':r'This uses $s-t$ instead of $s\cdot t$.',
                        'reversed difference':r'This uses $t-s$ instead of $s\cdot t$.',
                        'quotient':r'This uses $s/t$ instead of $s\cdot t$.',
                        'sum of squares':r'This uses $s^2+t^2$ instead of $s\cdot t$.'}.get(recipe,r'Solve for the common pair, verify all coordinates, then calculate $s\cdot t$.')
        choices.append({':answer/type':typ,':answer/value':value,':answer/feedback':validate_prose(normalize_prose(feedback))})
    prompt,solution = map(normalize_prose,(prompt,solution))
    identity = json.dumps([difficulty,prompt,solution,sorted((a[':answer/type'],a[':answer/value']) for a in choices)],ensure_ascii=False)
    qid = uuid.uuid5(uuid.NAMESPACE_URL,identity)
    uid = lambda name: str(uuid.uuid5(qid,name))
    for i,a in enumerate(choices):
        a[':answer/id'] = uid('answer:'+a[':answer/type']+':'+a[':answer/value'])
    right = [a for a in choices if a[':answer/value']==correct]
    if len(right)!=1:
        raise ValueError('Bank must have exactly one correct value')
    if rng:
        rng.shuffle(choices)
    record = {'knowledge_point':dict(KP),'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+difficulty,
        ':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{
        ':answer-field/id':uid('selection'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
        ':answer-field/choices':choices,':answer-field/correct':[':answer/id',right[0][':answer/id']]}]},
        'generation':{'generator_version':1,'template':'plane-membership','profile':profile,
                      'parameters':{'b':[str(x) for x in b],'c':[str(x) for x in c],'u':[str(x) for x in u]},
                      'source_question_ids': [source] if source else [17592186119620,17592186120306,17592186120304,17592186713334,17592186713321,17592186713317]}}
    return validate_generated_record(record)


def sample_instance(rng,band,member,profile,product_sign=None):
    for attempt in range(10000):
        s,t = [F(rng.randint(-4,4),rng.choice((1,2)) if band=='moderate' else 1) for _ in range(2)]
        if product_sign is not None and ((s*t>0)-(s*t<0))!=product_sign:
            continue
        small = lambda: rng.choice((-3,-2,-1,1,2,3))
        if band=='easy':
            br,cr = [1,0,small()],[0,1,small()]
            independent = (0,1)
        elif band=='moderate':
            br,cr = [small() for _ in range(3)],[small() for _ in range(3)]
            if any(br[i]*cr[j]==br[j]*cr[i] for i,j in [(0,1),(0,2),(1,2)]):
                continue
            independent = (0,1)
        else:
            a,b,c,d = [small() for _ in range(4)]
            if a*d==b*c:
                continue
            factor = rng.choice((-2,-1,2))
            br,cr = [a,factor*a,c],[b,factor*b,d]
            independent = (0,2)
        ur = [s*br[i]+t*cr[i] for i in range(3)]
        if any(x.denominator != 1 for x in ur):
            continue
        if not member:
            unused = next(i for i in range(3) if i not in independent)
            ur[unused] += rng.choice((-2,-1,1,2))
        permutation = rng.sample(range(3),3)
        b,c,u = [[v[i] for i in permutation] for v in (br,cr,ur)]
        # On an inconsistent hard instance forward elimination may use the altered
        # dependent equation only as a contradiction; candidate bank coefficients
        # come from the independent pair selected before construction.
        vals = profile_values(profile,s,t)
        if len(vals)!=4 or len({v for v,_ in vals})!=4:
            continue
        bank = [(tex(v),':answer.type/math',recipe) for v,recipe in vals]+[(NON,':answer.type/text','membership')]
        return build(b,c,u,band,profile,rng,bank=bank)
    raise RuntimeError('Could not construct a distinct plausible bank')


def numeric_choice(value):
    if r'\frac' not in value:
        return F(value)
    match = re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',value)
    if not match:
        raise ValueError('Unexpected authored numerical choice')
    return (-1 if match[1] else 1)*F(int(match[2]),int(match[3]))


def rank_of_key(record):
    field=record['question'][':question/answer-fields'][0]
    key=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
    if key[':answer/type']!=':answer.type/math':
        return None,None
    value=numeric_choice(key[':answer/value'])
    ordered=sorted(numeric_choice(a[':answer/value']) for a in field[':answer-field/choices'] if a[':answer/type']==':answer.type/math')
    return ordered.index(value),value


def generate(difficulty,count,seed):
    if count<0:
        raise ValueError('Count must be nonnegative')
    rng = random.Random(seed)
    records,seen = [],set()
    # Practice positive, negative, and (where banks allow) zero products in each
    # complete error profile and membership branch. Roles precede coefficients.
    roles={}
    for profile in PROFILES:
        for member in (True,False):
            signs=[-1,1,0] if 'quadratic' in profile else [-1,1]
            rng.shuffle(signs)
            roles[profile,member]=[signs,0]
    while len(records)<count:
        plan = [True,True,False,False]
        rng.shuffle(plan)
        for member in plan:
            if len(records)==count:
                break
            profile = rng.choice(PROFILES)
            signs,index=roles[profile,member]
            product_sign=signs[index%len(signs)]
            # Retain zero as a legitimate outcome without allowing two different
            # profiles to make every member in a short batch a zero product.
            prior_member_values=[rank_of_key(r)[1] for r in records if rank_of_key(r)[0] is not None]
            if member and product_sign==0 and prior_member_values and not any(prior_member_values):
                index+=1
                roles[profile,member][1]=index
                product_sign=signs[index%len(signs)]
            for _ in range(10000):
                r = sample_instance(rng,difficulty,member,profile,product_sign)
                qid = r['question'][':question/id']
                if qid not in seen:
                    seen.add(qid);records.append(r);roles[profile,member][1]+=1;break
            else:
                raise RuntimeError('Exhausted unique instances')
    # A finite batch can accidentally make rank a perfect cue within an error
    # profile even when the infinite sampler is sound. Repair that selection
    # effect without removing membership, sign, zero, or profile cases.
    for profile in (*PROFILES,'all-profiles'):
        indexes=[i for i,r in enumerate(records) if (profile=='all-profiles' or r['generation']['profile']==profile) and rank_of_key(r)[0] is not None]
        ranks={rank_of_key(records[i])[0] for i in indexes}
        if len(indexes)>=2 and len(ranks)==1:
            repaired=False
            for replace in reversed(indexes):
                value=rank_of_key(records[replace])[1]
                if not value:
                    continue  # Keep zero's mathematically forced middle rank.
                selected_profile=records[replace]['generation']['profile']
                for _ in range(256):
                    candidate=sample_instance(rng,difficulty,True,selected_profile,(value>0)-(value<0))
                    if rank_of_key(candidate)[0] not in ranks and candidate['question'][':question/id'] not in seen:
                        records[replace]=candidate
                        seen.add(candidate['question'][':question/id'])
                        repaired=True
                        break
                if repaired:
                    break
            if not repaired:
                raise RuntimeError('Cannot diversify answer rank while preserving the selected mathematical roles')
    # A repeated visible bank format must not identify nonmembership without
    # examining the target vector. Keep the membership plan and all member
    # ranks, but move an excess nonmember into a format also used by a member.
    # Fractional banks remain eligible; only this finite-batch correlation is
    # rejected. The source itself has both outcomes with fractional banks.
    def fractional_bank(record):
        return any(numeric_choice(a[':answer/value']).denominator != 1
                   for a in record['question'][':question/answer-fields'][0][':answer-field/choices']
                   if a[':answer/type'] == ':answer.type/math')
    member_formats = {fractional_bank(r) for r in records if rank_of_key(r)[0] is not None}
    if len(member_formats) == 1:
        supported_format = next(iter(member_formats))
        isolated = [i for i, r in enumerate(records)
                    if fractional_bank(r) != supported_format]
        if len(isolated) >= 2:
            # Retain one opposite-format nonmember, so the format is not banned.
            for i in isolated[1:]:
                profile = records[i]['generation']['profile']
                for candidate_profile in (profile, *[p for p in PROFILES if p != profile]):
                    for _ in range(256):
                        candidate = sample_instance(rng, difficulty, False, candidate_profile)
                        qid = candidate['question'][':question/id']
                        if fractional_bank(candidate) == supported_format and qid not in seen:
                            records[i] = candidate
                            seen.add(qid)
                            break
                    else:
                        continue
                    break
                else:
                    raise RuntimeError('Cannot remove bank-format nonmembership cue')
    return records


def replay():
    cases = json.loads(Path(__file__).with_name('source-cases.json').read_text())
    return [build(c['b'],c['c'],c['u'],c['difficulty'],'source-replay',source=c['source_id'],bank=c['bank']) for c in cases]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=('easy','moderate','hard','unclassified'),default='moderate')
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=('json',),default='json')
    parser.add_argument('--replay',action='store_true',help='Replay all captured complete source banks at original parameters')
    args = parser.parse_args()
    records = replay() if args.replay else generate('moderate' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed)
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
