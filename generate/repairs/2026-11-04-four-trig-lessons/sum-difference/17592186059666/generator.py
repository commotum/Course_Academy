#!/usr/bin/env python3
"""Portable exact-cosine generator. No database, repository imports, or asset writes."""
import argparse
import hashlib
import json
import random
import uuid
from functools import lru_cache
from pathlib import Path
import sympy as S
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = {'db_id':17592186059666, 'id':'283415d8-47d7-5d42-8836-0c0b0c4efc85',
      'title':'Finding Exact Values Using the Sum and Difference Formulas'}
VERSION = '2.0.0'
SPECIAL = (30,45,60,120,135,150,210,225,240,300,315,330)
# Values are recalled prerequisite data, not CAS-derived antiderivatives/identities.
COS = {0:S.Integer(1),30:S.sqrt(3)/2,45:S.sqrt(2)/2,60:S.Rational(1,2),90:S.Integer(0),
       120:-S.Rational(1,2),135:-S.sqrt(2)/2,150:-S.sqrt(3)/2,180:-S.Integer(1),
       210:-S.sqrt(3)/2,225:-S.sqrt(2)/2,240:-S.Rational(1,2),270:S.Integer(0),
       300:S.Rational(1,2),315:S.sqrt(2)/2,330:S.sqrt(3)/2}
PROFILES = {
 'formula-and-signs': ('wrong_formula','negate_result','negate_first','double_denominator'),
 'product-and-scale': ('wrong_formula','omit_first','omit_second','halve_denominator'),
 'signed-products': ('negate_first','negate_second','negate_result','double_denominator'),
 'radical-products': ('wrong_formula','omit_second','bad_radical','halve_denominator'),
}

@lru_cache(None)
def values(p,q,s):
    cp,cq=COS[p%360],COS[q%360]
    sp,sq=COS[(90-p)%360],COS[(90-q)%360]
    a,b=S.expand(cp*cq),S.expand(sp*sq)
    return cp,cq,sp,sq,a,b,S.expand(a-s*b)


def tex(v):
    return normalize_tex(S.latex(S.factor_terms(S.expand(v))))


def angle(deg,unit):
    if unit=='degrees': return str(deg)+r'^\circ'
    n=S.Rational(deg,180)
    if not n: return '0'
    sign='-' if n<0 else ''; n=abs(n)
    top=(str(n.p) if n.p!=1 else '')+r'\pi'
    return sign+(top if n.q==1 else r'\frac{'+top+'}{'+str(n.q)+'}')


def trig(name,a): return '\\'+name+r'\left('+a+r'\right)'
def display(t): return '$$\n'+t+'\n$$'
def aligned(rows): return display('\\begin{aligned}\n'+(' \\\\\n'.join(rows))+'\n\\end{aligned}')
def par(v): return r'\left('+tex(v)+r'\right)' if v<0 else tex(v)


def wrong_values(p,q,s):
    cp,cq,sp,sq,a,b,k=values(p,q,s)
    # Concrete in-instance errors, including one radical factor not multiplied.
    bad=lambda v: v.xreplace({S.sqrt(6):S.sqrt(3),S.sqrt(3):S.Integer(3),S.sqrt(2):S.Integer(2)})
    return {'wrong_formula':a+s*b,'negate_result':-k,'negate_first':-a-s*b,
            'negate_second':a+s*b,'omit_first':-s*b,'omit_second':a,
            'double_denominator':k/2,'halve_denominator':2*k,
            'bad_radical':bad(a)-s*bad(b)}


def make_bank(p,q,s,profile):
    k=values(p,q,s)[-1]; errors=wrong_values(p,q,s)
    vals=[k]+[S.expand(errors[n]) for n in PROFILES[profile]]
    if len(set(vals))!=5: return None
    return [(tex(v), 'correct' if i==0 else PROFILES[profile][i-1]) for i,v in enumerate(vals)]


def bank_rank(p,q,s,profile):
    k=values(p,q,s)[-1];errors=wrong_values(p,q,s)
    return sum(bool(errors[n]<k) for n in PROFILES[profile])


def make_record(p,q,s,unit,difficulty,shape,profile='formula-and-signs',rng=None,
                outer=None,bank_override=None,key_override=None,source_ids=None):
    rng=rng or random.Random(0)
    target=p+s*q
    cp,cq,sp,sq,a,b,k=values(p,q,s)
    at,pt,qt=map(lambda x:angle(x,unit),(target,p,q))
    op='+' if s==1 else '-'; join='-' if s==1 else '+'
    name='sum' if s==1 else 'difference'
    split=pt+op+qt
    formula=r'\cos(x'+op+r'y)=\cos x\cos y'+join+r'\sin x\sin y.'
    key=key_override or tex(k)
    # Build the ordered derivation before the answer bank.
    prefix=''
    if outer is not None:
        raise ValueError('This family assesses one forward cosine identity using a supplied split')
    if shape=='radio':
        problem='Find the **exact** value of $'+trig('cos',at)+'$.\n\n*Hint: Use the fact that*\n\n'+display(at+'='+split+'.')
    else:
        problem='Using the fact that\n\n'+display(at+'='+split+',')+'\n\ncalculate the **exact** value of $'+trig('cos',at)+'$.\n\n$'+trig('cos',at)+'=$ {{field-1}}'
    # Keep the long trig expansion in a separate display; numeric rows stay short.
    solution=(prefix+'Recall the '+name+' formula for cosine:\n\n'+display(formula)
              +'\n\nApply it to the decomposition:\n\n'
              +display(trig('cos',at)+'='+trig('cos',split)+'.')+'\n\n'
              +display(trig('cos',pt)+trig('cos',qt)+join+trig('sin',pt)+trig('sin',qt))
              +'\n\nSubstitute the signed special-angle values and combine:\n\n'
              +aligned(['&='+par(cp)+r'\cdot '+par(cq)+join+par(sp)+r'\cdot '+par(sq),
                        '&='+par(a)+join+par(b), '&='+key+'.']))
    problem,solution=normalize_prose(problem),normalize_prose(solution)
    if bank_override is not None:
        bank=[(normalize_tex(v),'source-bank') for v in bank_override]
    elif shape=='radio':
        bank=make_bank(p,q,s,profile)
        if bank is None: raise ValueError('Invalid complete profile')
    else: bank=[(key,'correct')]
    rng.shuffle(bank)
    ident=json.dumps([difficulty,problem,solution,sorted(v for v,_ in bank)],ensure_ascii=False)
    qid=str(uuid.uuid5(uuid.NAMESPACE_URL,'exact-cosine:'+hashlib.sha256(ident.encode()).hexdigest()))
    fid=str(uuid.uuid5(uuid.UUID(qid),'field'))
    choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v,_ in bank]
    correct=next(c[':answer/id'] for c in choices if c[':answer/value']==key)
    field={':answer-field/id':fid,':answer-field/key':'selection' if shape=='radio' else 'field-1',
           ':answer-field/type':':answer-field.type/'+shape,':answer-field/choices':choices,
           ':answer-field/correct':[':answer/id',correct]}
    record={'knowledge_point':KP.copy(),'question':{':question/id':qid,':question/problem':problem,
            ':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,
            ':question/answer-fields':[field]},
            'generation':{'generator_version':VERSION,'template':'supplied-'+name+'-'+shape,
              'parameters':{'p':p,'q':q,'s':s,'unit':unit},
              'calibration':'authored overlapping supplied-split band; no imported hard anchor' if difficulty=='hard' else 'imported same-skill family',
              'bank_profile':profile if shape=='radio' else None,
              'choice_recipes':{c[':answer/id']:recipe for c,(_,recipe) in zip(choices,bank)},
              'source_question_ids':source_ids or (['c338ba7e-729f-5c5d-97ab-549fb226cb62','7f15816e-a4ea-5e54-ac29-0fac8d7bc4b0'] if difficulty=='easy' and shape=='radio' else ['b67c309d-f1ce-5ff4-97dc-3605a30b0439','e4605c71-e2bc-5367-b6ca-7ac14bd5654c'] if difficulty=='easy' else ['9b9e46d2-105c-587e-ad59-8da071cc7eea','c456fc7d-3362-5f0f-892b-2dc7d01dc677'] if shape=='radio' else ['252126f0-142c-514f-8cc9-9ddbe81844d9','cb9a138e-76d2-528f-b913-b0fc66fe6f14']),
              'domain':'real fixed angles; exact radical arithmetic',
              'ordered_path':{'displayed_final':key,'key':key,'steps':['cosine identity','signed special-angle substitution','radical products','fraction combination'],
              'conversions':[],'support':['lesson a9114a20-3220-5a44-b0ed-4e405d4317a4','unit-circle prerequisites','radical product prerequisite']}}}
    return validate_generated_record(record)


@lru_cache(None)
def catalog(difficulty,sign,unit,shape,profile):
    items=[]
    pool=(30,45,60,135) if difficulty=='easy' and shape=='radio' else SPECIAL
    for p in pool:
        for q in pool:
            target=p+sign*q
            if abs(target)>345 or target%30==0 or target%45==0:continue
            if difficulty=='easy' and shape=='radio' and (target%30==0 or p==q):continue
            if difficulty=='easy' and shape=='blank' and not(p in (135,225) and q in (30,60,120,150)):continue
            if difficulty=='hard' and p<90 and q<90:continue
            if difficulty=='hard' and target%30==0:continue
            if shape=='radio' and make_bank(p,q,sign,profile) is None:continue
            items.append((p,q))
    return tuple(items)


def generate(difficulty,count,seed):
    rng=random.Random(seed); out=[]; seen=set(); profiles=list(PROFILES); family_hits={}; profile_hits={}; used_values={}; last_rank={}
    # Decision cases are selected before compatible numerical pairs. Each cycle
    # spans both identity cases; shape/unit phase rotates independently per cycle.
    phase=rng.randrange(2);start=rng.randrange(len(profiles));shape_phase=rng.randrange(4)
    for i in range(count):
        sign=1 if (i+phase)%2==0 else -1
        unit='radians' if (i//2+phase)%2==0 else 'degrees'
        minority=i%4==(i//4+shape_phase)%4
        shape='blank' if difficulty=='hard' or (difficulty=='moderate' and not minority) or (difficulty=='easy' and minority) else 'radio'
        role=(sign,shape)
        occurrence=family_hits.get(role,0);family_hits[role]=occurrence+1
        family=('acute' if occurrence%2==0 else 'signed') if difficulty=='easy' and shape=='radio' else 'any'
        profile_role=(sign,shape,family)
        bank_occurrence=profile_hits.get(profile_role,0);profile_hits[profile_role]=bank_occurrence+1
        unit='radians' if (bank_occurrence+phase)%2==0 else 'degrees'
        preferred=(bank_occurrence+start+(sign==-1))%len(profiles)
        # Select an entire authored bank profile, never fill from a pooled list.
        # Adjacent instances in the same visible family must not teach a fixed
        # numerical-rank strategy when plausible complete profiles can vary it.
        for offset in range(len(profiles)):
            profile=profiles[(preferred+offset)%len(profiles)]
            candidates=list(catalog(difficulty,sign,unit,shape,profile))
            if family!='any':candidates=[(p,q) for p,q in candidates if ((p<90 and q<90)==(family=='acute'))]
            candidates=[(p,q) for p,q in candidates if (p,q,sign) not in seen]
            if shape=='radio' and profile_role in last_rank:
                candidates=[(p,q) for p,q in candidates if bank_rank(p,q,sign,profile)!=last_rank[profile_role]]
            if candidates:break
        else:raise ValueError('No complete plausible profile varies the incidental bank rank')
        groups={}
        for p,q in candidates:groups.setdefault(values(p,q,sign)[-1],[]).append((p,q))
        used=used_values.setdefault(profile_role,set())
        available=sorted(set(groups)-used,key=str)
        if not available:used.clear();available=sorted(groups,key=str)
        outcome=rng.choice(available);used.add(outcome)
        candidates=groups[outcome]
        rng.shuffle(candidates)
        for p,q in candidates:
            target=p+sign*q;outer=None
            r=make_record(p,q,sign,unit,difficulty,shape,profile,rng,outer)
            # Angle roles plus resulting target distinguish semantic instances;
            # shuffled options and different UUIDs do not create new instances.
            sem=(p,q,sign)
            if sem in seen:continue
            seen.add(sem)
            if shape=='radio':last_rank[profile_role]=bank_rank(p,q,sign,profile)
            r['generation'].update(seed=seed,sample_index=i)
            out.append(r);break
        else: raise ValueError('Requested count exceeds this finite decision-case cycle; reduce count')
    return out


SOURCE_PARAMETERS=[(135,30,1,'radians'),(135,120,1,'radians'),(45,30,1,'degrees'),
 (60,225,-1,'degrees'),(150,30,-1,'degrees'),(135,60,1,'degrees'),
 (45,60,-1,'radians'),(45,150,-1,'degrees'),(60,225,-1,'radians'),(30,240,-1,'degrees')]


def replay_source():
    source=json.loads(Path(__file__).with_name('source-cases.json').read_text())
    # published-cases.json captures authored predecessors, not imported calibration.
    parameters=[(*p,None) for p in SOURCE_PARAMETERS]
    out=[]
    for q,(p,b,s,u,outer) in zip(source,parameters):
        f=q[':question/answer-fields'][0]
        band=q[':question/difficulty'][':db/ident'].rsplit('/',1)[1]
        shape=f[':answer-field/type'][':db/ident'].rsplit('/',1)[1]
        r=make_record(p,b,s,u,band,shape,bank_override=[a[':answer/value'] for a in f[':answer-field/choices']],
                      key_override=normalize_tex(f[':answer-field/correct'][':answer/value']),source_ids=[q[':question/id']],outer=outer)
        r['generation']['bank_profile']='source:'+q[':question/id'] if shape=='radio' else None
        out.append(r)
    return out


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=('easy','moderate','hard','unclassified'),default='moderate')
    parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=('json',),default='json');parser.add_argument('--replay-source',action='store_true')
    args=parser.parse_args()
    if args.count<0:parser.error('count must be nonnegative')
    records=replay_source() if args.replay_source else generate('moderate' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed)
    print(json.dumps(records,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
