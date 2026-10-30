#!/usr/bin/env python3
"""Seeded cross-product practice; no repository imports, files or services."""
import argparse
import json
import random
import uuid
from itertools import combinations
from math_format import normalize_prose, normalize_tex, validate_generated_record

VERSION = '1.2.0'
KP = {'db_id': 17592186203898, 'id': '88c81beb-9b15-56ae-bb46-ce5cbc1d0ea5',
      'title': 'Calculating Cross Product Expressions Using Anticommutativity'}
PROFILES = {
 'easy': [('left','coordinate','radio'), ('left','basis','radio'), ('right','basis','radio'),
          ('right','coordinate','blank'), ('right','basis','blank')],
 'moderate': [(s,n,'blank') for s in ('left','right') for n in ('coordinate','basis')],
 'hard': [('double',n,'radio') for n in ('coordinate','basis')],
}
SOURCE_IDS = {
 'easy': ['fc1132a9-2d61-580a-962e-790b83f18349','ef9d2387-b7ae-53f7-b8c6-1610d51dc482',
          'a0f3ebcb-819b-5060-93c1-2a4bba4f43b1','34251e9f-6d6e-5593-b05c-d3a2ed14c7e5','3b5ecce5-4519-5318-90df-e9ee9bf806a2'],
 'moderate': ['e746ff9c-9f50-594b-8773-1ffdd380a3c1','cab06a75-19db-5a30-a8e2-e30108934976'],
 'hard': ['b0ab30bc-8e0d-58ed-bb44-53e554f692a6'],
}

def scale(c,v): return [c*x for x in v]
def add(*vs): return [sum(x) for x in zip(*vs)]
def cross(a,b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def vec(v, notation):
    if notation == 'coordinate': return r'\langle' + ','.join(map(str,v)) + r'\rangle'
    return combination([(c,r'\mathbf '+s) for c,s in zip(v,'ijk')]) if any(v) else r'\mathbf0'
def combination(terms):
    out=''
    for c,s in terms:
        if not c: continue
        out += ('-' if c<0 else '+' if out else '') + (str(abs(c)) if abs(c)!=1 else '') + s
    return out or r'\mathbf0'
def linear(terms): return combination([(c,r'\mathbf '+x) for c,x in terms])
def product(i,j): return r'\mathbf '+i+r'\times\mathbf '+j
def expression(left,right):
    def factor(t): return '('+linear(t)+')' if len(t)>1 else linear(t)
    return factor(left)+r'\times'+factor(right)
def display(rows): return '$$\n'+r'\begin{aligned}'+'\n'+r'\\'.join(rows)+'\n'+r'\end{aligned}'+'\n$$'
def ordered_terms(left,right): return [(c*d,x,y,c,d) for c,x in left for d,y in right]
def result_of(spec):
    values={tuple(g['pair']):g['value'] for g in spec['givens']}
    contributions=[]
    for c,x,y,_,_ in ordered_terms(spec['left'],spec['right']):
        if x==y: continue
        v=values.get((x,y))
        if v is None: v=scale(-1,values[(y,x)])
        contributions.append(scale(c,v))
    return add(*contributions)

def derivation(spec):
    left,right=spec['left'],spec['right'];n=spec['notation']; terms=ordered_terms(left,right)
    expr=expression(left,right)
    # Split long four-term expansions into two rows in the actual learning UI.
    pieces=[(c,'('+product(x,y)+')') for c,x,y,_,_ in terms]
    chunks=[pieces] if len(pieces)==2 else [pieces[:2],pieces[2:]]
    expansion=[('&=' if i==0 else r'&\quad{}'+('+' if chunk[0][0]>0 else ''))+combination(chunk)
               for i,chunk in enumerate(chunks)]
    text='Distribute without changing the order of the vector factors, and extract the scalars.\n\n'
    text+=display([expr]+expansion)
    givens={tuple(g['pair']):g['value'] for g in spec['givens']}
    steps=[]; substitute=[];contributions=[]; reduced=[]
    for c,x,y,_,_ in terms:
        if x==y:
            steps.append('$'+product(x,y)+r'=\mathbf0'+ '$')
        else:
            direct=(x,y) in givens
            p=(x,y) if direct else (y,x)
            if not direct: steps.append('$'+product(x,y)+'=-('+product(*p)+')$')
            coeff=c if direct else -c
            reduced.append((coeff,'('+product(*p)+')'))
            substitute.append((coeff,'('+vec(givens[p],n)+')'))
            contributions.append(scale(coeff,givens[p]))
    text+='\n\nUse '+', '.join(steps)+'. The self product vanishes; each reversed pair changes sign.\n\n'
    # One equation per block keeps even large three-term substitutions within the UI.
    text+=display([r'&'+combination(reduced)])
    for (coeff,_),g in zip(substitute, [next(g['value'] for g in spec['givens'] if tuple(g['pair'])==((x,y) if (x,y) in givens else (y,x))) for c,x,y,_,_ in terms if x!=y]):
        text+='\n\n'+display(['&'+str(coeff)+r'\bigl('+vec(g,n)+r'\bigr)='+vec(scale(coeff,g),n)])
    ans=result_of(spec)
    text+='\n\nCollect the three components:\n\n'
    rows=[]
    for i,s in enumerate('ijk'):
        summands='+'.join('('+str(v[i])+')' for v in contributions)
        rows.append('&'+summands+'='+str(ans[i]))
    if len(contributions)>1:
        text+=display(rows)+'\n\n'
    text+=display(['&'+expr+'='+vec(ans,n)])
    return text

def easy_bank(spec, profile, rng):
    terms=ordered_terms(spec['left'],spec['right'])
    c,x,y,_,_=next(t for t in terms if t[1]!=t[2]); d=next(t[0] for t in terms if t[1]==t[2])
    g=spec['givens'][0];o=1 if g['pair']==[x,y] else -1;k=c*o
    candidates=[(-k,'omit pair reversal'), (o,'omit survivor scalar'),
                (-o,'omit scalar and reverse sign'),
                (k+d*o,'retain self product as given product'),
                (k-d*o,'subtract self product as given product'),
                (d*o,'use self-term scalar instead of survivor scalar')]
    pool={}
    for coefficient,reason in candidates:
        if coefficient != k:pool.setdefault(coefficient,reason)
    if len(pool)<4:return [],[]
    selected=rng.sample(list(pool),4)
    bank=[scale(k,g['value'])]+[scale(t,g['value']) for t in selected]
    if bank_only_candidates(bank)==[0]:return [],[]
    # Another bank-only cue: a unique opposite-pair member which is also the
    # midpoint of two options. Complete self-sum error sets previously exposed it.
    centers=[i for i,v in enumerate(bank) if scale(-1,v) in bank
             and any(add(v,h) in bank and add(v,scale(-1,h)) in bank for h in bank if any(h))]
    if centers==[0]:return [],[]
    return bank,['correct']+[pool[t] for t in selected]

def bank_only_candidates(bank):
    """A bank must not expose its answer through the old balanced error recipe.

    This probe uses option vectors only. It does not read the target or givens.
    """
    return [i for i, v in enumerate(bank)
            if any(add(*(bank[k] for k in ids)) == scale(d, v)
                   for ids in combinations(range(5), 4) for d in (2, 3))]

def hard_bank(spec,profile,rng):
    # Mix independently interpretable errors rather than serving complete sets of
    # sign flips or omissions: those sets reveal their center by bank arithmetic.
    terms=[]
    values={tuple(g['pair']):g['value'] for g in spec['givens']}
    for c,x,y,a,b in ordered_terms(spec['left'],spec['right']):
        if x==y: continue
        v=values.get((x,y))
        if v is None: v=scale(-1,values[(y,x)])
        terms.append((scale(c,v),a,b,v))
    ans=add(*(t[0] for t in terms));pool={}
    def error(value,reason):
        if value != ans:pool.setdefault(tuple(value),reason)
    for contribution,a,b,v in terms:
        error(add(ans,scale(-2,contribution)), 'reverse one surviving ordered pair incorrectly')
        error(add(ans,scale(-1,contribution)), 'omit one surviving term')
        if a != 1:
            error(add(ans,scale(-1,contribution),scale(b,v)), 'omit the signed scalar on the left factor of one term')
        if b != 1:
            error(add(ans,scale(-1,contribution),scale(a,v)), 'omit the signed scalar on the right factor of one term')
    if len(pool)<4:return [],[]
    selected=rng.sample(list(pool),4)
    bank=[ans]+[list(v) for v in selected]
    # Reject the specific demonstrated bank-only answer cue. This changes only
    # distractor selection, never eligible mathematical outcomes or cancellations.
    if bank_only_candidates(bank)==[0]:return [],[]
    return bank,['correct']+[pool[v] for v in selected]

def source_refs(spec):
    if spec['band']=='hard':
        return ['b0ab30bc-8e0d-58ed-bb44-53e554f692a6',
                'afcc8d33-fe9b-5c65-a7f2-97b6d0a1032f' if spec['notation']=='coordinate' else 'c3e9b2b8-80c6-5b5f-a8f3-154d30b790dd']
    if spec['band']=='moderate':
        return ['e746ff9c-9f50-594b-8773-1ffdd380a3c1' if spec['notation']=='coordinate' else 'cab06a75-19db-5a30-a8e2-e30108934976']
    profile=(spec['side'],spec['notation'],spec['response'])
    return [dict(zip(PROFILES['easy'],SOURCE_IDS['easy']))[profile]]

def build(spec, rng=None, replay_bank=None):
    rng=rng or random.Random(0);spec=json.loads(json.dumps(spec));n=spec['notation'];ans=result_of(spec)
    expr=expression(spec['left'],spec['right'])
    prompt='Find $'+expr+'$, given:\n\n'+'\n\n'.join('$'+product(*g['pair'])+'='+vec(g['value'],n)+'$.' for g in spec['givens'])
    solution=derivation(spec)
    if spec['response']=='blank':
        if n=='coordinate':
            prompt+='\n\n$'+expr+r'=\langle$ {{field-1}} $,$ {{field-2}} $,$ {{field-3}} $\rangle$'
        else:
            prompt+='\n\n$'+expr+'=$ {{field-1}} $\\mathbf i+$ {{field-2}} $\\mathbf j+$ {{field-3}} $\\mathbf k$'
        values=[[str(c)] for c in ans];errors=['independent component entry'];corrects=[str(c) for c in ans]
    else:
        if replay_bank is not None:
            bank,correct_index=replay_bank
            raw=[normalize_tex(x) for x in bank];correct_value=raw[correct_index];errors=['historical source bank replay']*len(raw)
        else:
            bank,errors=(hard_bank(spec,spec['bank_profile'],rng) if spec['band']=='hard' else easy_bank(spec,spec['bank_profile'],rng))
            if len(bank)!=5 or len(set(map(tuple,bank)))!=5:return None
            raw=[vec(v,n) for v in bank];correct_value=raw[0]
        indexed=list(zip(raw,errors));rng.shuffle(indexed);raw,errors=map(list,zip(*indexed))
        values=[raw];corrects=[correct_value]
    prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    values=[[normalize_tex(x) for x in v] for v in values];corrects=[normalize_tex(x) for x in corrects]
    # Content identity is calculated only after the shared prose normalization.
    identity=json.dumps([spec['band'],prompt,solution,values,corrects],ensure_ascii=False,separators=(',',':'))
    ns=uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/cross-product/'+identity)
    uid=lambda name:str(uuid.uuid5(ns,name))
    fields=[]
    for i,(vals,correct) in enumerate(zip(values,corrects)):
        key='selection' if spec['response']=='radio' else 'field-'+str(i+1)
        choices=[{':answer/id':uid(key+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
        fields.append({':answer-field/id':uid(key),':answer-field/key':key,':answer-field/type':':answer-field.type/'+spec['response'],
                       ':answer-field/choices':choices,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in choices if a[':answer/value']==correct)]})
    record={'knowledge_point':KP.copy(),'question':{':question/id':str(ns),':question/difficulty':':question.difficulty/'+spec['band'],
       ':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},
       'generation':{'generator_version':VERSION,'instance':spec,'source_question_ids':source_refs(spec), 'bank_errors':errors}}
    return validate_generated_record(record)

def sample_spec(band,profile,rng):
    side,notation,response=profile
    bank_profile=rng.choice(['signs','omissions'] if band=='hard' else ['paired','self-sum'])
    coeff=lambda:rng.choice([-3,-2,-1,1,2,3])
    if band!='hard':
        repeated,other=rng.sample(list('ab'),2)
        survivor=rng.choice([-4,-3,-2,2,3,4]) if response=='radio' else coeff()
        self_c=rng.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) if response=='radio' else coeff();outer=1 if band=='easy' else rng.choice([2,3,4])
        terms=[(survivor,other),(self_c,repeated)];rng.shuffle(terms)
        left,right=(terms,[(outer,repeated)]) if side=='left' else ([(outer,repeated)],terms)
        _,x,y,_,_=next(t for t in ordered_terms(left,right) if t[1]!=t[2])
        v=[rng.randint(-3,3) for _ in range(3)]
        if not any(v):v[rng.randrange(3)]=1
        givens=[{'pair':[y,x],'value':v}]
        witnesses=None
    else:
        x,y,z=rng.sample(list('abc'),3)
        left=[(coeff(),x),(coeff(),z)];right=[(coeff(),y),(coeff(),z)]
        rng.shuffle(left);rng.shuffle(right)
        survivors=[(u,v) for _,u,v,_,_ in ordered_terms(left,right) if u!=v]
        reversed_set=set(rng.sample(range(3),rng.randint(1,3)))
        witnesses={s:[rng.randint(-1,1) for _ in range(3)] for s in 'abc'}
        givens=[]
        for i,(u,v) in enumerate(survivors):
            if i in reversed_set:u,v=v,u
            value=cross(witnesses[u],witnesses[v])
            if not any(value):return None
            givens.append({'pair':[u,v],'value':value})
        rng.shuffle(givens)
    return {'band':band,'side':side,'notation':notation,'response':response,'left':left,'right':right,
            'givens':givens,'witnesses':witnesses,'bank_profile':bank_profile}

def bank_rank_signature(record):
    """Scores for predeclared bank-only rank/position strategies, no givens."""
    spec=record['generation']['instance']
    if spec['response']!='radio':return None
    field=record['question'][':question/answer-fields'][0]
    correct=next(i for i,a in enumerate(field[':answer-field/choices'])
                 if a[':answer/id']==field[':answer-field/correct'][1])
    # The bank has already been independently derived from this instance; use
    # the same formatting function to map its displayed vector to components.
    def parse(value):
        import re
        if value.startswith(r'\langle'):
            return list(map(int,value[7:-7].split(',')))
        terms=re.findall(r'([+-]?)(\d*)\\mathbf ([ijk])',value)
        result=[0,0,0]
        for sign,n,x in terms:result['ijk'.index(x)]+=(-1 if sign=='-' else 1)*int(n or 1)
        return result
    vectors=[parse(a[':answer/value']) for a in field[':answer-field/choices']]
    signature={'position':correct}
    for name,fn in [('norm',lambda v:sum(x*x for x in v)),('lex',tuple),
                    ('sum',sum),('positive',lambda v:sum(x>0 for x in v)),
                    ('zeros',lambda v:sum(x==0 for x in v))]:
        values=[fn(v) for v in vectors]
        # Include stable display-order tie breaking in both sorting directions.
        for reverse in (False,True):
            order=sorted(range(5),key=lambda i:values[i],reverse=reverse)
            signature[name+str(reverse)]=order.index(correct)
    return signature

def batch_cue_free(candidate,accepted):
    signature=bank_rank_signature(candidate)
    if signature is None:return True
    spec=candidate['generation']['instance']
    # Coordinate and basis notation, and the visible single-factor side, are
    # recognizable subgroups. Do not let a constant rank answer a whole pool.
    for dimensions in [('notation',),('side',)]:
        group=[r for r in accepted if r['generation']['instance']['response']=='radio'
               and all(r['generation']['instance'][d]==spec[d] for d in dimensions)]
        if group and any(all(bank_rank_signature(r)[key]==value for r in group)
                         for key,value in signature.items()):return False
    return True

def generate(band,count,seed):
    if count<0:raise ValueError('count must be nonnegative')
    rng=random.Random(seed);out=[];seen=set();schedule=[];attempts=0
    while len(out)<count:
        if not schedule:
            schedule=PROFILES[band].copy();rng.shuffle(schedule)
        profile=schedule[0]
        spec=sample_spec(band,profile,rng);attempts+=1
        if attempts>max(1000,count*1000):raise RuntimeError('unable to construct enough distinct valid banks')
        if spec is None:continue
        record=build(spec,rng)
        if record is None:continue
        if not batch_cue_free(record,out):continue
        semantic=json.dumps([record['question'][':question/problem'], result_of(spec)],sort_keys=True)
        if semantic in seen:continue
        seen.add(semantic);schedule.pop(0)
        record['generation'].update(seed=seed,index=len(out),construction_attempt=attempts)
        out.append(record)
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='easy')
    p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,required=True)
    p.add_argument('--format',choices=['json'],default='json');a=p.parse_args()
    print(json.dumps(generate('easy' if a.difficulty=='unclassified' else a.difficulty,a.count,a.seed),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
