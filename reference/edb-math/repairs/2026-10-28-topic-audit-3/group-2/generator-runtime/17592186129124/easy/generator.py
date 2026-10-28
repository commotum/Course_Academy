#!/usr/bin/env python3
"""Seeded full-domain sinusoidal range/minimum practice.

Reuses the legacy draft's signed-coefficient/argument and interval-transform
backbone; replaces its incomplete public raw profiles, arithmetic-only hard
sampler and shortcut-bearing served banks. Runtime is entirely local/stdlib.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

LEVELS = ('easy', 'moderate', 'hard')
KP = {'db_id':17592186129124, 'id':'5696c2d5-4e35-5ed3-a4a2-6fe9b158e461',
      'title':'Finding the Range of a Transformed Sinusoidal Function'}
VERSION = '2.0.1'
SOURCES = {
 'range':['9d95e69c-d8b6-504a-9a9e-0e0569042175','8be6063d-ee1d-5aea-9fe3-f1f6572dff56','87e222c7-c912-54d0-9c4f-f1a9126f53ea','78fb970b-1904-59d8-bdde-90d8ecfc1cd7'],
 'minimum':['df79444b-bf13-5349-9442-8567f87e370a'],
 'hard':['c57b5360-bc34-5163-a91e-b827e6d4af93']}


def tex(n):
    n=F(n)
    if n.denominator==1:return str(n.numerator)
    return ('-' if n<0 else '')+r'\frac{'+str(abs(n.numerator))+'}{'+str(n.denominator)+'}'


def signed(n):return ('+' if n>=0 else '-')+tex(abs(n))

def coefficient(n):return '' if n==1 else '-' if n==-1 else tex(n)


def display(rows):return '$$\n'+r'\begin{aligned}'+'\n'+r' \\'.join(rows)+'\n'+r'\end{aligned}'+'\n$$'


def argument(i):
    s=coefficient(i['B'])+'x';c=i['C']
    if c:
        t=tex(abs(c)) if i['unit']!='radian' else (r'\pi' if abs(c)==1 else r'\frac{\pi}{'+str(abs(c))+'}')
        if i['unit']=='degree':t+=r'^{\circ}'
        s+=('+' if c>0 else '-')+t
    return s


def expressions(i):
    t='\\'+i['trig']+r'\left('+argument(i)+r'\right)'
    a,d=i['A'],i['D']
    scaled=coefficient(a)+t
    simple=scaled+(signed(d) if d else '')
    if i['level']=='hard':
        p,q,r,s=(i[k] for k in ('P','Q','R','S'))
        nested=tex(p)+signed(q)+r'\left('+tex(r)+('+' if s>0 else '-')+t+r'\right)'
        expanded=tex(p)+signed(q*r)+signed(q*s)+t
        return t,scaled,simple,nested,expanded
    return t,scaled,simple,simple,None


def solution(i):
    t,scaled,simple,printed,expanded=expressions(i)
    a,d=i['A'],i['D'];lo,hi=d-abs(a),d+abs(a)
    out=i.get('out','f(x)');text=''
    if expanded:
        text='Distribute the outer factor to both terms before finding the vertical transformation:\n\n'
        text+=display([out+'&='+printed, '&='+expanded, '&='+simple])+'\n\n'
    text+='A nonzero horizontal scale and any horizontal shift preserve the full sine or cosine range over all real inputs. Start with\n\n'
    text+=display(['-1&'+r'\le '+t+r'\le 1'])+'\n\n'
    text+='Multiply by $'+tex(a)+'$'+(', reversing both inequalities' if a<0 else '')+'.'
    op=r'\ge ' if a<0 else r'\le '
    rows=[tex(-a)+'&'+op+scaled+op+tex(a)]
    if d:
        text+=' Then '+('add' if d>0 else 'subtract')+' $'+tex(abs(d))+'$.'
        rows.append(tex(d-a)+'&'+op+simple+op+tex(d+a))
    rows.append(tex(lo)+'&'+r'\le '+out+r'\le '+tex(hi))
    text+='\n\n'+display(rows)+'\n\n'
    text+='Both endpoint values and every value between them are attained. '
    if i['response']=='minimum':text+='Therefore, the minimum value is $'+tex(lo)+'$.'
    else:text+='Therefore, the range is $'+out+r'\in['+tex(lo)+','+tex(hi)+']$.'
    return text


# Each sampled profile is a complete four-error tuple. No candidate is appended
# as filler after inspecting an invalid bank. Exact collisions reject that tuple.
def error_values(i):
    a,d,b=F(i['A']),F(i['D']),abs(i['B']);r=abs(a);lo,hi=d-r,d+r
    if i['response']=='range':
        v={'omit_shift':(-r,r), 'reverse_shift':(-d-r,-d+r),
           'omit_amplitude':(d-1,d+1),'horizontal_amplitude':(d-r*b,d+r*b),
           'double_amplitude':(d-2*r,d+2*r),'half_amplitude':(d-r/2,d+r/2),
           'reciprocal_amplitude':(d-1/r,d+1/r),'scale_shift':(a*d-r,a*d+r),
           'half_shift':(d/2-r,d/2+r),'double_shift':(2*d-r,2*d+r),
           'lower_half':(lo,d),'upper_half':(d,hi)}
    else:
        v={'maximum':hi,'midline':d,'omit_shift':-r,'reverse_shift':-d-r,
           'omit_amplitude':d-1,'horizontal_amplitude':d-r*b,
           'double_amplitude':d-2*r,'half_amplitude':d-r/2,
           # Apply the same amplitude errors to the wrong (upper) endpoint.
           # These complete recipes remain meaningful when A=±1 and D=0;
           # no arbitrary numeric filler or instance exclusion is needed.
           'double_amplitude_maximum':d+2*r,'half_amplitude_maximum':d+r/2,
           'reciprocal_amplitude':d-1/r,'scale_shift':a*d-r,
           'half_shift':d/2-r,'double_shift':2*d-r}
    if i['level']=='hard':
        p,q,z,s=(F(i[k]) for k in ('P','Q','R','S'))
        for name,aa,dd in [('omit_outer_constant',q*s,q*z),
                            ('distribute_constant_only',s,p+q*z),
                            ('distribute_trig_only',q*s,p+z),
                            ('reverse_inner_sign',-q*s,p-q*z)]:
            v[name]=(dd-abs(aa),dd+abs(aa)) if i['response']=='range' else dd-abs(aa)
    return v


def safe_bank(values,response):
    if len(set(values))!=5:return False
    if response=='range':
        centers=[(l+h)/2 for l,h in values];radii=[(h-l)/2 for l,h in values]
        cm,rm=Counter(centers),Counter(radii)
        hits=[j for j in range(5) if cm[centers[j]]==max(cm.values()) and rm[radii[j]]==max(rm.values())]
        if hits==[0]:return False
    else:
        paired=[j for j,v in enumerate(values) if v and -v in values]
        if len(paired)==2 and 0 in paired:return False
    return True


def bank_ranks(values,response):
    columns=([values] if response=='minimum' else
             [[v[0] for v in values],[v[1] for v in values],
              [v[1]-v[0] for v in values],[v[1]+v[0] for v in values]])
    return tuple(sorted(set(c)).index(c[0]) for c in columns)


def bank_groups(i):
    # Only learner-visible families; numerical parameters are not cue groups.
    base=(i['level'],i['response'])
    angle='degree' if i['unit']=='degree' else 'other'
    return [base,base+(i['trig'],),base+(i['trig'],angle)]


def bank(i,rng,history=None):
    v=error_values(i);r=F(abs(i['A']));d=F(i['D'])
    correct=(d-r,d+r) if i['response']=='range' else d-r
    profiles=list(itertools.combinations(v,4));rng.shuffle(profiles)
    best=None;best_score=-1
    # The batch owns its banks. Among complete plausible profiles, prefer one
    # that breaks still-constant bank-only ranks in previously served visible
    # families. This changes no function, answer, difficulty or valid boundary.
    pending=[]
    if history:
        for group in bank_groups(i):
            old=history.get(group,[])
            if old:
                for j in range(len(old[0])):
                    seen={row[j] for row in old}
                    if len(seen)==1:pending.append((j,next(iter(seen))))
    for recipes in profiles:
        values=[correct]+[v[k] for k in recipes]
        if not safe_bank(values,i['response']):continue
        ranks=bank_ranks(values,i['response'])
        score=sum(ranks[j]!=previous for j,previous in pending)
        if score>best_score:best=(values,recipes);best_score=score
        if score==len(pending):break
    if best is None:raise ValueError('No complete misconception profile for instance')
    return best


def assemble(i,values,recipes,rng,prompt=None,worked=None):
    t,scaled,simple,printed,_=expressions(i);out=i.get('out','f(x)')
    angle=' (angles in degrees)' if i['unit']=='degree' else ''
    prompt=prompt or (('Find the range of $' if i['response']=='range' else 'Find the minimum value of $')+out+'='+printed+'$ for all real $x$'+angle+'.')
    def answer(v):
        if i['response']=='minimum':return tex(v)
        return out+r'\in['+tex(v[0])+','+tex(v[1])+']'
    return assemble_text(i,prompt,worked or solution(i),[answer(v) for v in values],0,recipes,rng)


def assemble_text(i,prompt,worked,values,correct_index,recipes,rng):
    prompt=normalize_prose(prompt);worked=normalize_prose(worked);values=[normalize_tex(v) for v in values]
    payload={'version':VERSION,'level':i['level'],'prompt':prompt,'solution':worked,'values':sorted(values)}
    identity=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    uid=lambda name:str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/'+identity+'/'+name))
    answers=[{':answer/id':uid('answer/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct=answers[correct_index][':answer/id'];rng.shuffle(answers)
    q={':question/id':uid('question'),':question/problem':prompt,':question/worked-solution':worked,
       ':question/difficulty':':question.difficulty/'+i['level'],':question/answer-fields':[
       {':answer-field/id':uid('field'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
        ':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
    record={'knowledge_point':KP.copy(),'question':q,'generation':{
       'version':VERSION,'template':('nested' if i['level']=='hard' else 'direct')+'_'+i['response'],
       'parameters':i.copy(),'source_ids':SOURCES['hard'] if i['level']=='hard' else SOURCES[i['response']],
       'bank_profile':list(recipes),'domain':'all real x','authored_extension':True,
       'semantic_instance':[i['response'],i['A'],i['D'],i.get('Q'),i.get('R'),i.get('P'),i.get('S')]}}
    return validate_generated_record(record)


def sample(level,rng,response=None,trig=None,unit=None):
    i={'level':level,'response':response or rng.choice(['range','range','minimum']),
       'trig':trig or rng.choice(['sin','cos']),'unit':unit or rng.choice(['linear','radian','degree'])}
    if level=='hard':
        i.update(P=rng.choice([-4,-3,-2,-1,1,2,3,4]),Q=rng.choice([-3,-2,2,3]),
                 R=rng.choice([-3,-2,-1,1,2,3]),S=rng.choice([-1,1]))
        i.update(A=i['Q']*i['S'],D=i['P']+i['Q']*i['R'])
    else:i.update(A=rng.randint(1,6)*(1 if level=='easy' else -1),D=rng.randint(-6,6))
    i['B']=rng.choice([-4,-3,-2,-1,1,2,3,4])
    i['C']=rng.choice([-60,-45,-30,0,30,45,60] if i['unit']=='degree' else [-6,-4,-3,-2,-1,0,1,2,3,4,6] if i['unit']=='radian' else [-3,-2,-1,0,1,2,3])
    return i


def generate_instance(i,seed=0):
    if not i['A'] or not i['B']:raise ValueError('Nonconstant sinusoid required')
    rng=random.Random(seed);values,recipes=bank(i,rng)
    return assemble(i,values,recipes,rng)


def generate_batch(level,count,seed):
    if level=='unclassified':level='moderate'
    rng=random.Random(seed);records=[];seen=set();bank_history={};position_history={}
    # One stream, bounded rejection and semantic uniqueness: horizontal changes
    # alone never count toward batch coverage. Cases are not seed-specific.
    for _ in range(max(1000,count*100)):
        i=sample(level,rng)
        semantic=(i['response'],i['A'],i['D'],i.get('Q'),i.get('R'),i.get('P'),i.get('S'))
        if semantic in seen:continue
        v,recipes=bank(i,rng,bank_history);record=assemble(i,v,recipes,rng)
        ranks=bank_ranks(v,i['response'])
        f=record['question'][':question/answer-fields'][0];answers=f[':answer-field/choices'];key=f[':answer-field/correct'][1]
        previous_positions=[]
        for group in bank_groups(i):
            old=position_history.get(group,[])
            if old and len(set(old))==1:previous_positions.append(old[0])
        positions=list(range(5));rng.shuffle(positions)
        target=min(positions,key=lambda p:sum(p==old for old in previous_positions))
        at=next(j for j,a in enumerate(answers) if a[':answer/id']==key)
        answers[at],answers[target]=answers[target],answers[at]
        for group in bank_groups(i):
            bank_history.setdefault(group,[]).append(ranks)
            position_history.setdefault(group,[]).append(target)
        records.append(record);seen.add(semantic)
        if len(records)==count:return records
    raise ValueError('Requested batch exceeds bounded semantic capacity')


def replay():
    cases=json.loads(Path(__file__).with_name('source-cases.json').read_text());records=[]
    for j,c in enumerate(cases):
        i=c['instance'];r=assemble_text(i,c['prompt'],c['solution'],c['values'],c['correct_index'],['source-replay'],random.Random(j))
        r['generation'].update(source_ids=[c['source_id']],authored_extension=False,evidence_only=True)
        records.append(r)
    return records


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=(*LEVELS,'unclassified'),default='moderate')
    ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--replay-source',action='store_true')
    args=ap.parse_args()
    if args.count<1:ap.error('--count must be positive')
    print(json.dumps(replay() if args.replay_source else generate_batch(args.difficulty,args.count,args.seed),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
