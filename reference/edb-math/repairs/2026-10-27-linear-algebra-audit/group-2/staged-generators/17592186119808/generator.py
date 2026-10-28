"""Seeded, relocatable span-membership and coefficient-product generator."""
import argparse
from fractions import Fraction as F
from itertools import combinations, product
import json
from math import prod
from pathlib import Path
import random
from uuid import UUID, uuid5
from math_format import normalize_prose, normalize_tex, validate_generated_record, matrix_operands

KP = 17592186119808
TITLE = 'Determining Whether a Vector Lies in the Span of Given Vectors'
NS = UUID('aaefbc53-9df9-54a0-a969-66e062553d5c')
VERSION = '1.1.1-source-notation'


def tex(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return ('-' if x < 0 else '') + r'\frac{' + str(abs(x.numerator)) + '}{' + str(x.denominator) + '}'


def vector(v):
    return r'\begin{bmatrix}' + r' \\ '.join(map(tex, v)) + r'\end{bmatrix}'


def aug(a):
    n = len(a[0])-1
    return r'\left[\begin{array}{' + 'c'*n + '|c}' + r' \\ '.join(' & '.join(map(tex, row)) for row in a) + r'\end{array}\right]'


def linear(row):
    terms = []
    for j,c in enumerate(row, 1):
        if not c:
            continue
        sign = '-' if c < 0 else ('+' if terms else '')
        terms.append(sign + (tex(abs(c)) if abs(c) != 1 else '') + 'x_{'+str(j)+'}')
    return ''.join(terms) or '0'


def eliminate(A, b):
    """Forward elimination and explicit row operations, then back-substitution."""
    n = len(A[0]); a = [[F(x) for x in row]+[F(y)] for row,y in zip(A,b)]
    stages = []; pivots = []; r = 0
    for col in range(n):
        pick = next((i for i in range(r,len(a)) if a[i][col]), None)
        if pick is None:
            continue
        if pick != r:
            a[r],a[pick] = a[pick],a[r]
            stages.append((rf'R_{{{r+1}}}\leftrightarrow R_{{{pick+1}}}', [row[:] for row in a]))
        for i in range(r+1,len(a)):
            if a[i][col]:
                factor = a[i][col]/a[r][col]
                a[i] = [v-factor*w for v,w in zip(a[i],a[r])]
                op = rf'R_{{{i+1}}}\leftarrow R_{{{i+1}}}-\left({tex(factor)}\right)R_{{{r+1}}}'
                stages.append((op,[row[:] for row in a]))
        pivots.append(col); r += 1
        if r == len(a): break
    bad = next((i for i,row in enumerate(a) if not any(row[:-1]) and row[-1]),None)
    xs = None; back = []
    if bad is None and len(pivots)==n:
        xs = [F(0)]*n
        for i,col in reversed(list(enumerate(pivots))):
            sub = a[i][-1]-sum(a[i][j]*xs[j] for j in range(col+1,n))
            xs[col] = sub/a[i][col]
            # Show each actual substitution, keeping simple rational notation.
            parts = [tex(a[i][-1])]
            for j in range(col+1,n):
                if a[i][j]: parts.append(r'-\left('+tex(a[i][j])+r'\right)\left('+tex(xs[j])+r'\right)')
            rhs = ''.join(parts)
            back.append('x_{'+str(col+1)+r'} &= \frac{'+rhs+'}{'+tex(a[i][col])+'} = '+tex(xs[col]))
    return a, stages, bad, xs, back


def nonmember(n):
    return r'\mathbf{b}\notin\operatorname{Span}\{' + ','.join(r'\mathbf{a}_{'+str(i)+'}' for i in range(1,n+1)) + r'\}'


def build(A, b, band, rng, bank=None, source=None):
    A = [list(map(F,row)) for row in A]; b = list(map(F,b)); n = len(A[0])
    reduced, stages, bad, xs, back = eliminate(A,b)
    assert bad is not None or xs is not None, 'Ambiguous coefficient product'
    names = ','.join(r'\mathbf{a}_{'+str(i)+'}' for i in range(1,n+1))
    span = r'\operatorname{Span}\{' + names+r'\}'
    product = r'\cdot '.join('x_{'+str(i)+'}' for i in range(1,n+1))
    decomposition = '+'.join('x_{'+str(i)+r'}\mathbf{a}_{'+str(i)+'}' for i in range(1,n+1))
    prompt = f'The vectors ${names}$ and $\\mathbf{{b}}$ are given below. Determine whether $\\mathbf{{b}}\\in {span}$. In the affirmative case, find ${product}$ from the decomposition $\\mathbf{{b}}={decomposition}$.'
    cols = list(zip(*A))
    displays = [r'\mathbf{a}_{'+str(j+1)+'}='+vector(col) for j,col in enumerate(cols)]+[r'\mathbf{b}='+vector(b)]
    prompt += '\n\n'+matrix_operands(displays)
    solution = f'By the definition of span, $\\mathbf{{b}}\\in {span}$ exactly when coefficients exist such that\n\n$$\n{decomposition}=\\mathbf{{b}}.\n$$\n\nEquating components gives\n\n$$\n'
    solution += r'\left\{\begin{aligned}'+r' \\ '.join(linear(row)+' &= '+tex(y) for row,y in zip(A,b))+r'\end{aligned}\right.'+'\n$$\n\nSet up the augmented matrix and use elementary row operations:\n\n$$\n'
    solution += aug([row+[y] for row,y in zip(A,b)])+'\n$$'
    for op, matrix in stages:
        solution += '\n\n$$\n'+op+'\n$$\n\n$$\n'+aug(matrix)+'\n$$'
    if bad is not None:
        solution += f'\n\nRow ${bad+1}$ gives $0={tex(reduced[bad][-1])}$, a contradiction. No coefficients satisfy every component, so $\\mathbf{{b}}\\notin {span}$.'
        key = nonmember(n)
    else:
        solution += '\n\nBack-substitution gives\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(back)+r'\end{aligned}'+'\n$$'
        solution += f'\n\nAll component equations hold. Thus $\\mathbf{{b}}\\in {span}$ and the coefficients are unique. Finally,\n\n$$\n{product}='+r'\cdot '.join(r'\left('+tex(x)+r'\right)' for x in xs)+'='+tex(prod(xs))+'.\n$$'
        key = tex(prod(xs))
    recipes = None
    if bank is None:
        bank,recipes = make_bank(A,b,xs,rng)
    else:
        # Captured JSON sometimes contains a double escaped command; decode only
        # the answer strings, not equation row separators in prose.
        bank = [nonmember(n) if 'notin' in v else v.replace('\\\\','\\') for v in bank]
    bank = [normalize_tex(v) for v in bank]
    key = normalize_tex(key)
    assert len(bank)==5 and len(set(bank))==5 and key in bank
    prompt = normalize_prose(prompt); solution = normalize_prose(solution)
    identity = json.dumps([band,prompt,solution,bank],ensure_ascii=False,separators=(',',':'))
    qid = str(uuid5(NS,identity)); fid = str(uuid5(UUID(qid),'selection'))
    answers = [{':answer/id':str(uuid5(UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in bank]
    correct = next(v[':answer/id'] for v in answers if v[':answer/value']==key)
    record = {'knowledge_point':{'db_id':KP,'id':str(NS),'title':TITLE}, 'question':{
        ':question/id':qid, ':question/difficulty':':question.difficulty/'+band,
        ':question/problem':prompt, ':question/worked-solution':solution,
        ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},
        'generation':{'version':VERSION,'template':band+'-span-product','source_ids':source or anchors(band),'source_replay':bool(source),'bank_recipes':recipes,'parameters':{'A':[[str(x) for x in row] for row in A],'b':list(map(str,b))},'outcome':'nonmembership' if bad is not None else 'membership'}}
    return validate_generated_record(record)


def anchors(band):
    return {'easy':['q-34635','q-105208','q-105199'],'moderate':['q-34205','q-34058','q-34115'],'hard':['q-34117','q-34218','q-34639','q-34648']}[band]


def make_bank(A,b,xs,rng):
    n=len(A[0]); nm=nonmember(n)
    if xs is None:
        # Use proper independent subsets, ignore remaining equations, and guess
        # one free coefficient. These are explicit premature-solution errors.
        candidates=[]
        for omit in range(n):
            keep=[j for j in range(n) if j!=omit]
            for rows in combinations(range(len(A)),n-1):
                subA=[[A[i][j] for j in keep] for i in rows]
                for guess in [-2,-1,1,2]:
                    subb=[b[i]-A[i][omit]*guess for i in rows]
                    _,_,bad,sol,_=eliminate(subA,subb)
                    if bad is None and sol is not None:
                        candidates.append((prod(sol)*guess, f'ignore unchecked components; x{omit+1}={guess}; rows={list(rows)}'))
        # All four numeric options are partial-system products, not arbitrary filler.
        rng.shuffle(candidates)
        unique={}
        for val,recipe in candidates: unique.setdefault(val,recipe)
        if len(unique)<4: raise ValueError('insufficient distinct partial-system distractors')
        selected=rng.sample(list(unique),4)
        pairs=[(tex(v),unique[v]) for v in selected]+[(nm,'contradiction')]
    else:
        p=prod(xs)
        pool=[(sum(xs),'sum instead of product'),(-p,'one coefficient sign reversed'),(prod(b[:n]),'target coordinates used as coefficients')]
        pool += [(prod(xs[:j]+xs[j+1:]),f'omit coefficient {j+1}') for j in range(n)]
        for j in range(n):
            for delta in [-1,1]:
                altered=xs[:];altered[j]+=delta
                pool.append((prod(altered),f'coefficient {j+1} recovered with {delta:+d} error'))
        # Sample complete profiles, not individual surviving distractors. Retry
        # another full profile for the SAME instance on collision so a zero
        # product is not suppressed merely because many error recipes also zero.
        profiles=list(combinations(range(len(pool)),3));rng.shuffle(profiles)
        chosen=None
        for profile in profiles:
            trial=[pool[j] for j in profile]
            if len(set([p]+[v for v,_ in trial]))==4:
                chosen=trial;break
        if chosen is None: raise ValueError('no distinct complete bank profile')
        pairs=[(tex(p),'coefficient product')]+[(tex(v),recipe) for v,recipe in chosen]+[(nm,'false nonmembership')]
    rng.shuffle(pairs)
    return [v for v,_ in pairs],[recipe for _,recipe in pairs]


def sample_parameters(band, member, rng):
    n=3 if band=='hard' else 2
    # Assign coefficient sign/zero roles before sampling compatible magnitudes.
    roles=list(product([-1,1],repeat=n))
    roles += [signs[:j]+(0,)+signs[j:] for j in range(n) for signs in product([-1,1],repeat=n-1)]
    signs=rng.choice(roles)
    xs=[F(sign*rng.randint(1,4)) for sign in signs]
    half_slot=rng.choice([None,None]+[j for j in range(n) if signs[j]])
    if half_slot is not None:
        xs[half_slot]=F(signs[half_slot]*rng.choice([1,3]),2)
    k,l,t,m,s=[rng.choice([-3,-2,-1,0,1,2,3]) for _ in range(5)]
    # Keep nontrivial coupling; zero elsewhere remains a valid simplification.
    if k==0: k=rng.choice([-2,-1,1,2])
    d=rng.choice([-2,-1,1,2])
    if band=='easy':
        A=[[1,k],[l,l*k+(d if member else 0)]]
    elif band=='moderate':
        A=[[1,k],[l,l*k+d],[m+s*l,m*k+s*(l*k+d)]]
    else:
        A=[[1,0,k],[l,1,l*k+t],[m,s,m*k+s*t+(d if member else 0)]]
    if half_slot is not None:
        # One small half-integer coefficient, with compatible even vector
        # entries: integer target coordinates and the same elimination method.
        for row in A: row[half_slot]*=2
    b=[sum(a*x for a,x in zip(row,xs)) for row in A]
    if not member:
        b[-1]+=rng.choice([-3,-2,-1,1,2,3])
    if max(abs(x) for row in A for x in row)>10 or max(map(abs,b))>40:
        raise ValueError('incidental arithmetic too large')
    # Simultaneous coordinate permutations are irrelevant mathematically, while
    # generator permutations reassign coefficient roles without changing product.
    rr=list(range(len(A)));cc=list(range(n));rng.shuffle(rr);rng.shuffle(cc)
    return [[A[i][j] for j in cc] for i in rr],[b[i] for i in rr]


def _candidate_batch(band,count,seed,rng):
    records=[];seen=set(); attempts=0
    # Cover both decision branches in a finite batch without coupling outcomes
    # to choice order or coefficients. Random starting branch preserves count=1.
    outcomes=[True,False];rng.shuffle(outcomes)
    for i in range(count):
        member=outcomes[i%2]
        while True:
            attempts+=1
            if attempts>max(1000,1000*count): raise RuntimeError('sampler exhausted')
            try:
                A,b=sample_parameters(band,member,rng)
                record=build(A,b,band,rng)
            except ValueError:
                continue
            semantic=json.dumps([record['generation']['parameters'],record['generation']['outcome']],sort_keys=True)
            if semantic in seen: continue
            seen.add(semantic)
            record['generation'].update({'seed':seed,'index':i})
            records.append(record);break
    return records


def _bank_number(value):
    if r'\frac{' in value:
        import re
        match = re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}', value)
        return F((-1 if match[1] else 1)*int(match[2]),int(match[3]))
    return F(value)


def batch_shortcuts(records):
    """Reject repeatable surface actions, including conditional product shortcuts.

    Groups use only printed matrix sparsity and bank fraction presence. The
    member-only probes explicitly grant membership recognition, then test whether
    numeric rank or a sign/counterpart cue replaces coefficient recovery.
    """
    groups={}
    for record in records:
        q=record['question'];field=q[':question/answer-fields'][0]
        choices=field[':answer-field/choices'];key=field[':answer-field/correct'][1]
        values=[c[':answer/value'] for c in choices]
        index=next(i for i,c in enumerate(choices) if c[':answer/id']==key)
        value=values[index];member='notin' not in value
        nums=[_bank_number(v) for v in values if 'notin' not in v]
        number=_bank_number(value) if member else None
        A=record['generation']['parameters']['A']
        labels=['all','dense' if all(F(x) for row in A for x in row) else 'zero-entry',
                'fraction-bank' if any('frac' in v for v in values) else 'integer-bank']
        for label in labels:
            groups.setdefault(label,[]).append((index,value,member,number,nums))
    failures=[]
    for label,rows in groups.items():
        if len(rows)<2: continue
        if len({r[0] for r in rows})==1: failures.append(label+':fixed-position')
        if len({r[1] for r in rows})==1: failures.append(label+':fixed-value')
        members=[r for r in rows if r[2]]
        if len(members)<2: continue
        if len({sorted(r[4]).index(r[3]) for r in members})==1:
            failures.append(label+':fixed-numeric-rank-after-membership')
        # A unique sign or a unique opposite pair must not identify every key.
        for sign in [-1,1]:
            if all(sum((v>0)-(v<0)==sign for v in r[4])==1 and (r[3]>0)-(r[3]<0)==sign for r in members):
                failures.append(label+':unique-sign')
        for sign in [-1,1]:
            def counterpart(row):
                pair=[v for v in row[4] if v and -v in row[4]]
                return len(pair)==2 and row[3] in pair and (row[3]>0)-(row[3]<0)==sign
            if all(counterpart(row) for row in members): failures.append(label+':opposite-pair-sign')
    return failures


def generate(band,count,seed):
    rng=random.Random(seed)
    # Stream continuation, never a replacement seed or a hand-picked batch.
    # Small teaching requests cannot support comparisons; ordinary batches can.
    for attempt in range(1000):
        records=_candidate_batch(band,count,seed,rng)
        if count<5 or not batch_shortcuts(records): return records
    raise RuntimeError('unable to construct a batch without the tested surface shortcuts')


def replay_sources():
    cases=json.loads(Path(__file__).with_name('source_cases.json').read_text())
    return [build(c['coefficient_matrix'],c['target'],c['difficulty'],random.Random(0),c['choice_bank'],[c['source_id']]) for c in cases]


def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate');p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json');p.add_argument('--replay-source',action='store_true');args=p.parse_args()
    if args.count<0:p.error('count must be nonnegative')
    records=replay_sources() if args.replay_source else generate('moderate' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed)
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
