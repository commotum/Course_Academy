#!/usr/bin/env python3
"""Seeded midline practice. No database or repository-relative runtime imports."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import random
import re
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP_ID=17592186129123
KP_UUID='933b20c7-323f-5443-9cf4-97e87fa2c6fc'
TITLE='Finding the Midline of a Transformed Sinusoidal Function'
VERSION='midline-representations-2'
CASES=('above','below','cross_positive','cross_negative','centered','touch')
# Complete authored misconception banks; collisions reject the whole bank.
PROFILES=(
 ('minimum','maximum','amplitude','sum'),
 ('minimum','maximum','negative_amplitude','sum'),
 ('minimum','maximum','negative_center','double_halving'),
 ('minimum','maximum','half_minimum','half_maximum'),
 ('amplitude','negative_amplitude','sum','negative_sum'),
 ('minimum','maximum','zero','double_halving'),
 ('minimum','amplitude','sum','negative_sum'),
 ('maximum','negative_amplitude','sum','negative_sum'),
 ('half_minimum','half_maximum','sum','negative_sum'),
 ('minimum','maximum','negative_sum','double_halving'),
 ('minimum','maximum','half_maximum','range'),
 ('minimum','maximum','half_minimum','negative_range'))
HARD_PROFILES=(
 ('ignore_inner','ignore_factor','reverse_product','scale_outer'),
 ('minimum','maximum','ignore_inner','ignore_factor'),
 ('minimum','maximum','negative_center','inner_constant'),
 ('amplitude','negative_center','reverse_product','ignore_factor'),
 ('minimum','ignore_inner','reverse_product','scale_outer'),
 ('maximum','inner_constant','ignore_factor','scale_outer'),
 ('minimum','maximum','amplitude','ignore_inner'),
 ('inner_constant','negative_center','ignore_inner','scale_outer'),
 # Forgetting both vertical operations gives zero, a plausible competitor
 # when a small center would otherwise always have the smallest magnitude.
 ('minimum','zero','ignore_inner','scale_outer'),
 ('maximum','zero','reverse_product','ignore_factor'))

def tex(v):
    v=F(v)
    if v.denominator==1:return str(v.numerator)
    return ('-' if v<0 else '')+r'\frac{'+str(abs(v.numerator))+'}{'+str(v.denominator)+'}'

def signed(v):return ('+' if v>=0 else '-')+tex(abs(v))
def par(v):return '('+tex(v)+')' if v<0 else tex(v)
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(o):return str(uuid.uuid5(uuid.UUID(KP_UUID),str(o)))
def enum(o):return o.get(':db/ident') if isinstance(o,dict) else o

def decision(c,a):
    if c>a:return 'above'
    if c < -a:return 'below'
    if c==0:return 'centered'
    if abs(c)==a:return 'touch'
    return 'cross_positive' if c>0 else 'cross_negative'

def error_values(c,a,p,hard):
    values={'minimum':F(c-a),'maximum':F(c+a),'amplitude':F(a),'negative_amplitude':F(-a),'sum':F(2*c),'negative_center':F(-c),'zero':F(0),'half_minimum':F(c-a,2),'half_maximum':F(c+a,2),'double_halving':F(c,2),'negative_sum':F(-2*c),'range':F(2*a),'negative_range':F(-2*a)}
    if hard:
        A,K,D=p['A'],p['K'],p['D']
        values.update(ignore_inner=F(D),ignore_factor=F(D+K),reverse_product=F(D-A*K),scale_outer=F(A*(D+K)),inner_constant=F(K))
    return values

def usable_bank(c, values):
    if len(set(values))!=5:return False
    # Prevent selecting the only positive/negative counterpart when it is the key.
    pairs=[(a,b) for a,b in itertools.combinations(set(values),2) if a!=0 and a==-b]
    return not(len(pairs)==1 and c in pairs[0])

def graph(p,out):
    if out is None:raise ValueError('Set COURSE_ACADEMY_GENERATOR_OUTPUT_DIR for graph output')
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    os.environ.setdefault('MPLCONFIGDIR',str(out/'.matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    name='wave-'+digest({k:p[k] for k in ('center','amplitude','kind','flip')})[:24]+'.png'
    path=out/name
    if not path.exists():
        c,a=p['center'],p['amplitude']
        xs=[-2+4*i/800 for i in range(801)]
        # sine shifted by pi/2 equals cosine: extrema at the vertical axis in either family.
        ys=[c+p['flip']*a*math.cos(math.pi*x) for x in xs]
        fig,ax=plt.subplots(figsize=(6.3,4.0),dpi=120)
        low=min(0,c-a)-1;high=max(0,c+a)+1
        ax.set(xlim=(-2.15,2.15),ylim=(low,high))
        ax.set_xticks([-2,-1,0,1,2],['−2π','−π','0','π','2π'])
        ax.set_yticks(range(low,high+1))
        ax.grid(color='#dbe1e7',linewidth=.65)
        ax.axhline(0,color='#38434f',linewidth=1.2);ax.axvline(0,color='#38434f',linewidth=1.2)
        ax.plot(xs,ys,color='#1767ac',linewidth=2.2)
        ax.set_xlabel('x',loc='right');ax.set_ylabel('y',rotation=0,loc='top')
        ax.tick_params(labelsize=10)
        for spine in ax.spines.values():spine.set_visible(False)
        fig.tight_layout(pad=.9);fig.savefig(path,metadata={'Software':VERSION});plt.close(fig)
    return name

def make(level,p,profile,rng,output_dir=None,source=None):
    c,a=p['center'],p['amplitude'];lo,hi=c-a,c+a
    hard=level=='hard'
    errors=error_values(c,a,p,hard)
    if not source and not usable_bank(c,[F(c)]+[errors[k] for k in profile]):
        raise ValueError('Reject whole colliding or cued bank before rendering assets')
    arg=str(p.get('B',1))+'x'
    if arg.startswith('1x'):arg=arg[1:]
    phase=p.get('phase',0)
    if phase:arg+=('+' if phase>0 else '-')+r'\frac{\pi}{4}'
    trig='\\'+p['kind']+r'\left('+arg+r'\right)'
    if level=='easy':
        prompt=f'Find the equation of the midline for a transformed { {"sin":"sine","cos":"cosine"}[p["kind"]] } function with a minimum value of ${tex(lo)}$ and a maximum value of ${tex(hi)}$.'
    elif level=='moderate':
        image=graph(p,output_dir)
        prompt=f'The graph below shows a transformed { {"sin":"sine","cos":"cosine"}[p["kind"]] } function. Find the equation of its midline.\n\n![A sinusoidal curve on labeled coordinate axes.]({image})'
    else:
        A,K,D=p['A'],p['K'],p['D']
        expr=tex(D)+signed(A)+r'\left['+trig+signed(K)+r'\right]'
        prompt='Find the equation of the midline of the function\n\n$$\nf(x)='+expr+'.\n$$'
    if hard:
        solution=('Distribute the outer factor to both terms inside the brackets:\n\n$$\n'+r'\begin{aligned}'+'\n'+r'f(x) &= '+tex(D)+signed(A)+trig+signed(A*K)+r' \\'+'\n'+r'&= '+tex(A)+trig+signed(c)+'.\n'+r'\end{aligned}'+'\n$$\n\n'+
                  f'The vertical shift is ${tex(c)}$, so the midline is $y={tex(c)}$. The horizontal argument does not change this height.\n\n'+
                  f'As a check, the extrema are ${tex(lo)}$ and ${tex(hi)}$, whose average is $\\frac{{{tex(lo)}+{par(hi)}}}{{2}}={tex(c)}$.')
    else:
        intro=(f'Read the heights of a trough and a crest: the minimum is ${tex(lo)}$ and the maximum is ${tex(hi)}$.\n\n' if level=='moderate' else '')
        solution=intro+'The midline is the horizontal line halfway between the minimum and maximum values. Average their heights:\n\n$$\n'+r'\begin{aligned}'+'\n'+r'y &= \frac{y_{\text{min}}+y_{\text{max}}}{2} \\'+'\n'+r'&= \frac{'+tex(lo)+'+'+par(hi)+r'}{2} \\'+'\n'+r'&= '+tex(c)+'.\n'+r'\end{aligned}'+'\n$$\n\n'+f'Therefore, the midline is $y={tex(c)}$. The half-range ${tex(a)}$ is the amplitude, rather than the vertical shift.'
    if not hard and c==a:
        solution=solution.replace('is the amplitude, rather than the vertical shift.', 'is the amplitude. Here the amplitude and midline height happen to have the same numerical value.')
    errors=error_values(c,a,p,hard)
    values=[F(c)]+[errors[k] for k in profile]
    if source:
        prompt=source[':question/problem']
        # Source solutions retain their explanatory order; only normalize presentation.
        solution=source[':question/worked-solution']
        texts=[normalize_tex(x[':answer/value']) for x in source[':question/answer-fields'][0][':answer-field/choices']]
        values=[F(t.split('=')[1].strip()) for t in texts]
    else:
        if not usable_bank(c,values):raise ValueError('Reject whole colliding or cued bank')
        texts=['y='+tex(v) for v in values]
    # Punctuation in imported equations is presentation, not a mathematical operation.
    prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    texts=[normalize_tex(t) for t in texts]
    content={'version':VERSION,'level':level,'prompt':prompt,'solution':solution,'bank':sorted(texts)}
    qid=uid(digest(content));fid=uid(qid+':selection')
    choices=[{':answer/id':uid(fid+':'+t),':answer/type':':answer.type/math',':answer/value':t} for t in texts]
    correct=next(x[':answer/id'] for x,v in zip(choices,values) if v==c)
    rng.shuffle(choices)
    record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'template':level+'_'+p['kind'],'parameters':p,'decision_case':decision(c,a),'bank_profile':list(profile),'source_ids':([source[':question/id']] if source else []),'authored_extension':not bool(source),'answer_math':tex(c),'content_hash':digest(content)}}
    return validate_generated_record(record)

def sample(level,rng,case,output_dir):
    for _ in range(4000):
        # Select a complete error profile before compatible instance values.
        profile=rng.choice(HARD_PROFILES if level=='hard' else PROFILES)
        a=rng.randint(2,5) if level!='hard' else rng.choice((2,3))
        c=rng.randint(-8,8)
        if decision(c,a)!=case:continue
        p={'center':c,'amplitude':a,'kind':rng.choice(('sin','cos')),'flip':rng.choice((-1,1))}
        # Prompt prose uses full names, while TeX uses the operators.
        if level=='hard':
            A=rng.choice((-a,a));K=rng.choice((-3,-2,-1,1,2,3,4));D=c-A*K
            if abs(D)>6:continue
            p.update(A=A,K=K,D=D,B=rng.randint(1,3),phase=rng.choice((-1,0,1)))
        try:return make(level,p,profile,rng,output_dir)
        except ValueError:continue
    raise RuntimeError('No compatible whole profile after bounded resampling')

def _candidate_batch(level,count,rng,output_dir):
    if count<0:raise ValueError('Count must be nonnegative')
    out=[];seen=set()
    # Without-replacement cycles cover the six geometric cases while available.
    # A finite case (notably center=0) can saturate before the whole domain.
    while len(out)<count:
        cases=list(CASES);rng.shuffle(cases)
        before=len(out)
        for case in cases:
            if len(out)==count:break
            for _ in range(100):
                r=sample(level,rng,case,output_dir)
                p=r['generation']['parameters']
                fingerprint=(p['center'],p['amplitude'],p.get('A'),p.get('K'),p.get('D'))
                if fingerprint not in seen:
                    seen.add(fingerprint);out.append(r);break
            # Exhausting one case must not discard unused instances in others.
        if len(out)==before:
            raise ValueError('Requested batch exceeds available semantic instances')
    return out

def bank_cues(records):
    """Detect simple answer-producing actions in repeated visible families.

    Predictions use only displayed order and choice constants; the key is used
    solely for scoring them. A singleton cannot establish a recurring cue.
    """
    groups=[records]+[[r for r in records if r['generation']['template'].endswith('_'+kind)] for kind in ('sin','cos')]
    for group in groups:
        if len(group)<2:continue
        observations=[]
        for r in group:
            f=r['question'][':question/answer-fields'][0]
            choices=f[':answer-field/choices'];values=[]
            for choice in choices:
                text=choice[':answer/value'].split('=')[-1]
                m=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',text)
                values.append((-1 if m[1] else 1)*F(int(m[2]),int(m[3])) if m else F(text))
            correct=next(i for i,a in enumerate(choices) if a[':answer/id']==f[':answer-field/correct'][1])
            predictions=list(range(5))+[values.index(v) for v in sorted(values)]
            predictions += [values.index(min(values,key=abs)),values.index(max(values,key=abs))]
            for sign in (1,-1):
                eligible=[i for i,v in enumerate(values) if v*sign>0]
                predictions.append(eligible[0] if len(eligible)==1 else 0)
            integers=[i for i,v in enumerate(values) if v.denominator==1]
            predictions += [integers[0] if len(integers)==1 else 0,values.index(0) if 0 in values else 0]
            observations.append([prediction==correct for prediction in predictions])
        if any(all(row[i] for row in observations) for i in range(len(observations[0]))):return True
    return False

def batch(level,count,seed,output_dir):
    if count<0:raise ValueError('Count must be nonnegative')
    rng=random.Random(seed)
    # Continue the same seeded stream on rejection, rather than replacing the
    # runner seed or hand-picking saved records. Numerical and positional cues
    # are assessed within both trigonometric wording families as well as overall.
    for _ in range(1000):
        records=_candidate_batch(level,count,rng,output_dir)
        if not bank_cues(records):return records
    raise ValueError('Unable to construct a batch without a recurring bank cue')

def replay(q,output_dir=None):
    match=re.search(r'minimum value of \$(-?\d+)\$ and a maximum value of \$(-?\d+)',q[':question/problem'])
    lo,hi=map(int,match.groups())
    p={'center':F(lo+hi,2),'amplitude':F(hi-lo,2),'kind':'cos' if 'cosine' in q[':question/problem'] else 'sin','flip':1}
    return make('easy',p,(),random.Random(0),output_dir,source=q)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=('easy','moderate','hard','unclassified'),default='easy')
    ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=('json',),default='json')
    ap.add_argument('--replay-sources',action='store_true')
    args=ap.parse_args();out=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if args.replay_sources:
        result=[replay(q,out) for q in json.loads(Path(__file__).with_name('source-replay.json').read_text())]
    else:result=batch('easy' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed,out)
    print(json.dumps(result,indent=2,default=lambda v:int(v) if isinstance(v,F) and v.denominator==1 else str(v)))
if __name__=='__main__':main()
