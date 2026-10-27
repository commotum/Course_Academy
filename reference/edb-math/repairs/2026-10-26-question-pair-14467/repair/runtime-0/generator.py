#!/usr/bin/env python3
"""Seeded standard-form parallel-line recognition; bank-first target assignment.

Equation rendering and content-derived identities continue the legacy generator.
The current source capture and published exemplars replace its obsolete evidence
and arithmetic-only difficulty rules. No repository imports are used at runtime.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP_ID = 17592186087687
KP_UUID = 'd5bf8c8b-64f1-5552-a59e-78eef021c122'
TITLE = 'Identifying Parallel Lines Given in Standard Form'
VERSION = 'parallel-bank-targets-4.0'
LEVELS = ('easy', 'moderate', 'hard')
INTEGER_SLOPES = tuple(map(F, (-6,-5,-4,-3,-2,-1,1,2,3,4,5,6)))
FRACTION_SLOPES = tuple(F(n,d) for n,d in ((1,2),(2,3),(3,2),(3,4),(4,3),(-1,2),(-2,3),(-3,2),(-3,4),(-4,3)))
NS = uuid.UUID(KP_UUID)

def digest(v):
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(',',':')).encode()).hexdigest()

def uid(v):
    return str(uuid.uuid5(NS, v))

def tex(v):
    v=F(v)
    return str(v.numerator) if v.denominator == 1 else ('-' if v<0 else '')+r'\frac{'+str(abs(v.numerator))+'}{'+str(v.denominator)+'}'

def term(c, var):
    c=F(c)
    return ('' if c==1 else '-' if c==-1 else tex(c))+var

def linear(a, b, first='x', second='y'):
    return term(a,first)+('+' if b>=0 else '-')+term(abs(b),second)

def slope_form(m,b):
    return 'y='+term(m,'x')+(('+' if b>0 else '-')+tex(abs(b)) if b else '')

def standard_form(m,b,scale=1):
    # Choose B so that A, B, C are small integers and -A/B=m, C/B=b.
    B=F(m).denominator*scale
    A=-F(m)*B
    C=F(b)*B
    return linear(A,B)+'='+tex(C)

def equation_data(m,b,scale):
    B=F(m).denominator*scale
    return (-F(m)*B,F(B),F(b)*B)

def aligned(rows):
    return '$$\n'+r'\begin{aligned}'+'\n'+(' \\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$'

def isolate(m,b,scale):
    A,B,C=equation_data(m,b,scale)
    rhs=term(-A,'x')+(('+' if C>0 else '-')+tex(abs(C)) if C else '')
    return aligned([standard_form(m,b,scale).replace('=',' &= '),term(B,'y')+' &= '+rhs,slope_form(m,b).replace('=',' &= ')])

def record(level,given,choices,target,seed,template='authored',prompt=None,solution=None):
    m,b,s=given
    correct=choices[target]['text']
    if prompt is None:
        prompt=f'Which of the following lines is parallel to ${standard_form(m,b,s)}$?'
        if level=='hard':
            prompt=f'Which of the following is a distinct line parallel to ${standard_form(m,b,s)}$?'
    if solution is None:
        solution=('For two distinct nonvertical lines to be parallel, they must have the same slope.\n\n'
          f'To find the slope of ${standard_form(m,b,s)}$, convert to slope-intercept form:\n\n'+isolate(m,b,s)+
          f'\n\nThe slope is the coefficient of $x$, so the required slope is ${tex(m)}$.\n\n')
        if level!='easy':
            solution+='Rewrite the choices in slope-intercept form:\n\n'+aligned([
                c['text']+r' &\quad\Longrightarrow\quad '+slope_form(c['m'],c['b']) for c in choices])+'\n\n'
        matches=[c for c in choices if c['m']==m]
        if len(matches)>1:
            same=next(c for c in matches if c['b']==b)
            solution+=(f'The line ${same["text"]}$ has both the same slope ${tex(m)}$ and the same '
               f'$y$-intercept ${tex(b)}$ as the given line. It is the same line, so it is not a distinct parallel line.\n\n')
        else:
            solution+=f'Only ${correct}$ has slope ${tex(m)}$.\n\n'
        solution+=(f'The line ${correct}$ has slope ${tex(m)}$ and $y$-intercept ${tex(choices[target]["b"])}$, '
          f'different from ${tex(b)}$. Therefore, it is a distinct parallel line.\n\n'
          '$$\n'+correct+'\n$$')
    prompt=normalize_prose(prompt)
    solution=normalize_prose(solution)
    texts=[normalize_tex(c['text']) for c in choices]
    correct=normalize_tex(correct)
    content=digest({'version':VERSION,'level':level,'prompt':prompt,'solution':solution,'choices':sorted(texts),'correct':correct})
    qid=uid('question:'+content)
    fid=uid(qid+':field:selection')
    answers=[{':answer/id':uid(fid+':answer:'+t),':answer/type':':answer.type/math',':answer/value':t} for t in texts]
    rec={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{
        ':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,
        ':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{
        ':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
        ':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[target][':answer/id']]}]},
        'generation':{'version':VERSION,'seed':seed,'template':template,
            'given':{'slope':str(m),'intercept':str(b),'scale':s},
            'decision':{'target_slot':target,'coincident':sum(c['m']==m and c['b']==b for c in choices)>0},
            'content_fingerprint':content,'difficulty_origin':'authored progression; imported observations remain easy',
            'source_support':['b2f31785-e173-518c-a1fd-b069e0834b2a','2a7600a0-ce9a-5126-866d-bc3d1cf82b41'],
            'plot_rating':'none'}}
    return validate_generated_record(rec)

def make_bank(level,rng):
    pool=INTEGER_SLOPES if level=='easy' else INTEGER_SLOPES+FRACTION_SLOPES
    if level=='hard':
        m,n,k=rng.sample(pool,3)
        slopes=[m,m,n,n,k]
    else:
        slopes=rng.sample(pool,5)
    choices=[]
    for m in slopes:
        eligible=[F(b) for b in range(-5,6) if (m,F(b)) not in [(c['m'],c['b']) for c in choices]]
        b=rng.choice(eligible)
        scale=rng.choice((-3,-2,-1,1,2,3))
        choices.append({'m':m,'b':b,'scale':scale,'text':slope_form(m,b) if level=='easy' else standard_form(m,b,scale)})
    rng.shuffle(choices)
    return choices

def target_record(level,choices,target,rng,seed):
    m=choices[target]['m']
    if level=='hard':
        b=next(c['b'] for i,c in enumerate(choices) if i!=target and c['m']==m)
    else:
        b=rng.choice([F(i) for i in range(-5,6) if i!=choices[target]['b']])
    return record(level,(m,b,rng.choice((-3,-2,-1,1,2,3))),choices,target,seed)

def batch(level,count,seed):
    if level=='unclassified':level='easy'
    if level not in LEVELS or count<1:raise ValueError('A supported difficulty and positive count are required')
    rng=random.Random(seed)
    out=[]
    seen=set()
    seen_banks=set()
    pool=INTEGER_SLOPES if level=='easy' else INTEGER_SLOPES+FRACTION_SLOPES
    slope_use={m:0 for m in pool}
    while len(out)<count:
        choices=make_bank(level,rng)
        bank=tuple(sorted((c['m'],c['b']) for c in choices))
        if bank in seen_banks:continue
        # Fixed-bank target swaps are useful tests, but ordinary practice needs
        # fresh normalization work. Use each supported slope before repeating it.
        least_used=min(slope_use.values())
        targets=[i for i,c in enumerate(choices) if slope_use[c['m']]==least_used
                 and (level!='hard' or sum(d['m']==c['m'] for d in choices)==2)]
        if not targets:continue
        target=rng.choice(targets)
        r=target_record(level,choices,target,rng,seed)
        qid=r['question'][':question/id']
        if qid not in seen:
            out.append(r);seen.add(qid);seen_banks.add(bank)
            slope_use[choices[target]['m']]+=1
    return out

def replay(name):
    case=json.loads(Path(__file__).with_name('source-cases.json').read_text())[name]
    choices=[{'m':F(c['slope']),'b':F(c['intercept']),'text':c['text']} for c in case['choices']]
    m,b,s=map(F,case['given'])
    targets=[i for i,c in enumerate(choices) if c['m']==m and c['b']!=b]
    assert len(targets)==1
    return record(case['level'],(m,b,int(s)),choices,targets[0],0,'source-replay:'+name,case['prompt'],case['solution'])

def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--difficulty',choices=(*LEVELS,'all','unclassified'),default='easy')
    cli.add_argument('--count',type=int,default=1)
    cli.add_argument('--seed',type=int,default=0)
    cli.add_argument('--format',choices=('json',),default='json')
    cli.add_argument('--replay',help='Evidence replay by supplied source question UUID')
    args=cli.parse_args()
    try:
        result=[replay(args.replay)] if args.replay else [r for level in (LEVELS if args.difficulty=='all' else (args.difficulty,)) for r in batch(level,args.count,args.seed)]
    except ValueError as e:cli.error(str(e))
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
