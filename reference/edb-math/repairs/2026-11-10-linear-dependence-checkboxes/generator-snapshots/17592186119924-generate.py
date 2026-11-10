#!/usr/bin/env python3
"""Seeded, relocatable inspection practice. No services, database, or asset writes."""
import argparse
import hashlib
import json
import random
import uuid
from fractions import Fraction
from pathlib import Path
from math_format import normalize_prose, validate_generated_record, matrix_tex, system_tex

KP = 17592186119924
KP_UUID = '7eb5ca50-e9f3-5513-aff1-1ada8c225a42'
VERSION = 'inspection-v1'
ROMAN = ['I', 'II', 'III']
NONZERO = [-2, -1, 1, 2]


def uid(namespace, value):
    return str(uuid.uuid5(uuid.UUID(namespace), value))


def number(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else rf'\frac{{{value.numerator}}}{{{value.denominator}}}'


def linear(coefficients, terms):
    parts = []
    for c, t in zip(coefficients, terms):
        if not c:
            continue
        sign = '-' if c < 0 else '+' if parts else ''
        parts.append(sign + ('' if abs(c) == 1 else number(abs(c))) + t)
    return ''.join(parts) or '0'


def vec(values):
    return matrix_tex([[number(x)] for x in values])


def avars(n):
    return [rf'\mathbf{{a}}_{{{i+1}}}' for i in range(n)]


def xvars(n):
    return [rf'x_{{{i+1}}}' for i in range(n)]


def residual(vectors, coefficients):
    return [sum(c*v[i] for c, v in zip(coefficients, vectors)) for i in range(3)]


def subset_label(mask):
    labels = [label for i, label in enumerate(ROMAN) if mask & (1 << i)]
    if not labels:
        return 'None of the statements'
    if len(labels) == 3:
        return 'I, II and III'
    return ' and '.join(labels) + ' only'


def source_label_mask(label):
    return sum(1 << i for i, roman in enumerate(ROMAN)
               if roman in label.replace(' and ', ' ').replace(' only', '').replace(',', '').split())


def display(tex):
    return '$$\n' + tex + '\n$$'


def statements(instance):
    n = len(instance['vectors']); aa = avars(n); xx = xvars(n)
    homogeneous = '+'.join(x+a for x, a in zip(xx, aa)) + r'=\mathbf{0}'
    labels = {}
    truths = {}
    for i, coefficients in enumerate(instance['candidates']):
        labels['candidate'+str(i)] = '$'+linear(coefficients, aa)+r'=\mathbf{0}$.'
        truths['candidate'+str(i)] = not any(residual(instance['vectors'], coefficients))
    labels['unique'] = '$'+homogeneous+'$ only if $'+'='.join(xx)+'=0$.'
    truths['unique'] = instance['independent']
    labels['class'] = 'The set $'+r'\{'+', '.join(aa)+r'\}'+'$ is linearly '+instance['polarity']+'.'
    truths['class'] = instance['independent'] == (instance['polarity'] == 'independent')
    return labels, truths


def system_and_proof(instance):
    """Produce a learner path, never a CAS normal form or a determinant."""
    vv=instance['vectors']; n=len(vv); xx=xvars(n)
    rows = [[v[i] for v in vv] for i in range(3)]
    equations = [linear(row, xx)+'=0' for row in rows]
    system = display(system_tex(equations))
    if not instance['independent'] and instance.get('source_id'):
        # Source witnesses are supplied in a successful candidate except the
        # explicitly observed failed-candidate dependent pair.
        witness=instance['witness']
        candidate = next((c for c in instance['candidates'] if not any(residual(vv,c))), witness)
        proof = ('A nontrivial solution is $' + ', '.join(x+'='+number(c) for x,c in zip(xx,candidate)) + '$. Indeed,\n\n'
                 + display(linear(candidate,avars(n))+'='+linear(candidate,[vec(v) for v in vv])+r'=\mathbf{0}')
                 + '\n\nThese coefficients are not all zero, so the set is **linearly dependent**. Any common nonzero scaling of these coefficients is also a witness.')
        return system, proof
    known={}; lines=[]
    if not instance['independent']:
        free=instance['free_index']; known[free]=Fraction(1)
        lines.append(xx[free]+'&=1')
    while len(known)<n:
        found=False
        for row in rows:
            unknown=[i for i,c in enumerate(row) if c and i not in known]
            if len(unknown)!=1:
                continue
            j=unknown[0]; constant=sum(Fraction(c)*known.get(i,0) for i,c in enumerate(row) if i!=j)
            value=-constant/Fraction(row[j])
            substituted=linear(row,[('('+number(known[i])+')') if i in known else xx[i] for i in range(n)])
            lines.append(substituted+r'&=0\quad\Longrightarrow\quad '+xx[j]+'='+number(value))
            known[j]=value;found=True;break
        if not found:
            raise ValueError('Instance lacks an inspection/back-substitution proof')
    if any(sum(Fraction(c)*known[i] for i,c in enumerate(row)) for row in rows):
        raise ValueError('Constructed witness fails a coordinate')
    path=display(r'\begin{aligned}'+r' \\ '.join(lines)+r'\end{aligned}')
    if instance['independent']:
        proof='Read a coordinate with just one remaining unknown at each step:\n\n'+path+'\n\nEvery coefficient must be zero. Thus the homogeneous equation has only the trivial solution and the set is **linearly independent**.'
    else:
        witness=[known[i] for i in range(n)]
        proof=('Choose one coefficient nonzero and solve the remaining coordinate equations by substitution:\n\n'+path
               +'\n\nThis gives a nontrivial solution. Verify it directly:\n\n'
               +display(linear(witness,avars(n))+'='+linear(witness,[vec(v) for v in vv])+r'=\mathbf{0}')
               +'\n\nThe coefficients are not all zero, so the set is **linearly dependent**.')
    return system, proof


def render(instance, rng=None):
    rng = rng or random.Random(0)
    labels, truths = statements(instance)
    roles=instance['roles']; values=[truths[r] for r in roles]
    n=len(instance['vectors']); aa=avars(n); xx=xvars(n)
    prompt='Consider the following vectors:\n\n'+display(r',\qquad '.join(a+'='+vec(v) for a,v in zip(aa,instance['vectors'])))+'\n\nWhich of the following statements are true?'
    if instance.get('shape')=='checkbox':
        prompt+='\n\nSelect all that apply.'
    else:
        prompt+='\n\n'+'\n\n'.join(label+'. '+labels[role] for label,role in zip(ROMAN,roles))
    solution=('A set is **linearly independent** when the equation $' + '+'.join(x+a for x,a in zip(xx,aa))+r'=\mathbf{0}$ has only the solution $'+'='.join(xx)+'=0$. A nontrivial solution proves **linear dependence**.')
    for index, coefficients in enumerate(instance['candidates']):
        r=residual(instance['vectors'],coefficients)
        expression=linear(coefficients,aa)
        expanded=linear(coefficients,[vec(v) for v in instance['vectors']])
        scaled='+'.join(vec([c*x for x in v]) for c,v in zip(coefficients,instance['vectors']))
        outcome=r'\mathbf{0}' if not any(r) else r'\ne\mathbf{0}'
        last=vec(r)+(('='+outcome) if not any(r) else outcome)
        solution+='\n\nTest the proposed combination:\n\n'+display(r'\begin{aligned}'+expression+'&='+expanded+r' \\ &='+scaled+r' \\ &='+last+r'\end{aligned}')
    system,proof=system_and_proof(instance)
    solution+='\n\nThe homogeneous vector equation gives the coordinate system:\n\n'+system+'\n\n'+proof
    if any(any(residual(instance['vectors'],c)) for c in instance['candidates']):
        solution+='\n\nA failed candidate alone does not prove independence; the homogeneous-equation argument settles the classification.'
    solution+='\n\n'+' '.join(('Statement '+ROMAN[i] if instance.get('shape')!='checkbox' else 'The statement “'+labels[r]+'”')+' is **'+str(truths[r]).lower()+'**.' for i,r in enumerate(roles))
    prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    # Normalize all prose BEFORE computing content-owned identities.
    keys=[normalize_prose(labels[r]) for r in roles]
    content=json.dumps([prompt,solution,keys,instance.get('source_banks')],sort_keys=True)
    qid=uid(KP_UUID,content)
    fields=[]
    if instance.get('shape')=='checkbox':
        for i,key in enumerate(keys):
            fid=uid(qid,'field:'+key)
            choices=[{':answer/id':uid(fid,value),':answer/type':':answer.type/text',':answer/value':value} for value in instance['source_banks'][i]]
            correct=uid(fid,str(values[i]).lower())
            fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]})
    else:
        fid=uid(qid,'field:selection');mask=sum(1<<i for i,t in enumerate(values) if t)
        bank=instance['source_banks'][0][:] if instance.get('source_id') else [subset_label(i) for i in range(8)]
        if not instance.get('source_id'):rng.shuffle(bank)
        correct_label=next(v for v in bank if (source_label_mask(v) if instance.get('source_id') else next(i for i in range(8) if subset_label(i)==v))==mask)
        choices=[{':answer/id':uid(fid,value),':answer/type':':answer.type/text',':answer/value':value} for value in bank]
        fields=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid,correct_label)]}]
    record={'knowledge_point':{'db_id':KP,'id':KP_UUID},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+instance['difficulty'],':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'generator':VERSION,'template':('two-probes' if len(instance['candidates'])==2 else 'one-probe'),'parameters':instance,'source_ids':[instance['source_id']] if instance.get('source_id') else ([17592186120148,17592186275388,17592186564502] if instance['difficulty']=='easy' else [17592186120149,17592186275384,17592186119498] if instance['difficulty']=='moderate' else [17592186120147,17592186275381,17592186120880]),'authored_extension':not bool(instance.get('source_id'))}}
    return validate_generated_record(record)


def make_instance(difficulty, regime, rng):
    independent=regime=='independent'
    if difficulty=='easy':
        a,b=[rng.choice(NONZERO) for _ in range(2)];k=rng.choice([-2,-1,2])
        vectors=[[a,b,0],[k*a,k*b,rng.choice(NONZERO) if independent else 0]]
        witness=[-k,1]; free=1
    else:
        p,q=rng.choice([-1,1]),rng.choice([-1,1])
        r=0 if difficulty=='moderate' else rng.choice(NONZERO)
        s,t=rng.choice(NONZERO),rng.choice(NONZERO)
        # Avoid a parallel pair in the dependent three-vector chain.
        while r*t==s*q:
            s,t=rng.choice(NONZERO),rng.choice(NONZERO)
        u=rng.choice(NONZERO) if independent else 0
        vectors=[[p,0,0],[r,q,0],[s,t,u]]
        witness=[(r*t-s*q)//(p*q),-t//q,1];free=2
    n=len(vectors)
    desired=[False] if independent else ([regime=='success'] if difficulty!='hard' else {'first':[True,False],'second':[False,True],'neither':[False,False]}[regime])
    if difficulty=='hard' and independent:desired=[False,False]
    candidates=[]
    for success in desired:
        for attempt in range(10000):
            if success:
                scale=rng.choice([-2,-1,1,2]);candidate=[scale*x for x in witness]
            else:
                # Identical coefficient-shape support for successful and failed
                # proposals. A visible coordinate test, not size, decides truth.
                if n==2:
                    proposal=[-rng.choice([-2,-1,2]),1]
                else:
                    pp,qq=rng.choice([-1,1]),rng.choice([-1,1])
                    rr=0 if difficulty=='moderate' else rng.choice(NONZERO)
                    ss,tt=rng.choice(NONZERO),rng.choice(NONZERO)
                    if rr*tt==ss*qq:continue
                    proposal=[(rr*tt-ss*qq)//(pp*qq),-tt//qq,1]
                scale=rng.choice(NONZERO);candidate=[scale*x for x in proposal]
                if not any(residual(vectors,candidate)):continue
            # A scalar duplicate would remove the added hard-band decision.
            # Successful cancellations remain eligible at either probe.
            if candidates and all(candidate[i]*candidates[0][j]==candidate[j]*candidates[0][i]
                                  for i in range(n) for j in range(n)):
                continue
            break
        else:raise ValueError('Could not construct distinct candidate decisions')
        candidates.append(candidate)
    # Coordinate/column roles are chosen together with their dependent data.
    rows=list(range(3));rng.shuffle(rows)
    cols=list(range(n));rng.shuffle(cols)
    vectors=[[vectors[j][i] for i in rows] for j in cols]
    candidates=[[c[j] for j in cols] for c in candidates]
    witness=[witness[j] for j in cols]
    roles=['candidate0','candidate1','class'] if difficulty=='hard' else ['candidate0','unique','class'];rng.shuffle(roles)
    return {'difficulty':difficulty,'regime':regime,'vectors':vectors,'candidates':candidates,'independent':independent,'witness':None if independent else witness,'free_index':cols.index(free),'polarity':rng.choice(['independent','dependent']),'roles':roles,'shape':'radio'}


def generate(difficulty, count, seed):
    if difficulty=='unclassified':difficulty='moderate'
    if difficulty not in ('easy','moderate','hard') or count<0:raise ValueError('Invalid difficulty or count')
    rng=random.Random(seed);regimes=['first','second','neither','independent'] if difficulty=='hard' else ['success','failed','independent']
    records=[];seen=set();order=[];success_slots=[]
    for index in range(count):
        if not order:order=regimes[:];rng.shuffle(order)
        regime=order.pop()
        for attempt in range(10000):
            instance=make_instance(difficulty,regime,rng)
            # Semantic deduplication ignores statement/choice order and polarity.
            signature=json.dumps([instance['vectors'],instance['candidates']],sort_keys=True)
            if signature not in seen:break
        else:raise ValueError('Semantic sampling space exhausted')
        seen.add(signature)
        if difficulty=='hard' and regime in ('first','second'):
            # A complete regime cycle must make either displayed probe useful.
            # Balance relative proposal slots without exposing internal candidate
            # identities or changing any mathematics, polarity, or class position.
            if not success_slots:
                success_slots=[0,1];rng.shuffle(success_slots)
            wanted=success_slots.pop()
            positions=[i for i,role in enumerate(instance['roles']) if role.startswith('candidate')]
            successful='candidate0' if regime=='first' else 'candidate1'
            if instance['roles'][positions[wanted]]!=successful:
                a,b=positions
                instance['roles'][a],instance['roles'][b]=instance['roles'][b],instance['roles'][a]
        record=render(instance,rng);record['generation'].update(seed=seed,index=index);records.append(record)
    return records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',default='moderate',choices=['easy','moderate','hard','unclassified'])
    parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    parser.add_argument('--replay-source',action='store_true')
    args=parser.parse_args()
    records=[render(i) for i in json.loads(Path(__file__).with_name('source_cases.json').read_text())] if args.replay_source else generate(args.difficulty,args.count,args.seed)
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
