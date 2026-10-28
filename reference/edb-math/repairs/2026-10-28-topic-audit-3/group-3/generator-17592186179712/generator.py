#!/usr/bin/env python3
import sys
sys.dont_write_bytecode=True
from audit_runtime import asset_payload,normalize_question
from math_format import normalize_prose,normalize_tex
"""Seeded contour/gradient diagram selection; no database or repository imports."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import random
import uuid
import tempfile

os.environ.setdefault('MPLCONFIGDIR', tempfile.mkdtemp(prefix='ca-gradient-mpl-'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from math_format import normalize_prose, validate_generated_record

VERSION = '1.0.1-audit9837'
KP = {'db_id': 17592186179712, 'id': '364d2c9a-6e9a-57f8-aa57-c10ee223061b',
      'title': 'Using the Relationship Between the Vector Field of a Function and Its Contour Plot'}
DIRECTIONS = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1),(2,1),(-2,-1),(1,-2),(-1,2)]
LINE = [(0,0,0,d,e) for d,e in DIRECTIONS]
QUADRATIC = [(1,0,1,0,0),(1,0,4,0,0),(4,0,1,0,0),(-1,0,-1,0,0),
             (-1,0,-4,0,0),(-4,0,-1,0,0),(1,0,-1,0,0),(-1,0,1,0,0),
             (0,1,0,0,0),(0,-1,0,0,0)]
PARABOLIC = [(a,0,0,0,e) for a in [-1,1] for e in [-1,1]] + [(0,0,c,d,0) for c in [-1,1] for d in [-1,1]]
CONTOUR = [QUADRATIC[i] for i in [0,1,2,6,8]] + [(1,0,0,0,e) for e in [-1,1]] + [(0,0,1,d,0) for d in [-1,1]] + [LINE[i] for i in [0,2,4,6,8,10]]
CENTERS = [(0,0),(-1,0),(1,0),(0,-1),(0,1)]
def source_ids(level,m):
    if level=='easy':return [17592186707988]
    a,b,c,d,e=m['coeff']
    if not(a or b or c):return [17592186383027,17592186387304] if level=='moderate' else [17592186407566]
    if b:return [17592186179574,17592186179967] if level=='moderate' else [17592186179574]
    if a and c:
        if a*c<0:return [17592186387311] if level=='moderate' else [17592186256728]
        if a==c:return [17592186179967] if level=='moderate' else [17592186179971]
        return [17592186256718,17592186707980] if level=='moderate' else [17592186256726]
    return [17592186383020] if level=='moderate' else [17592186256720,17592186707986]


def level_rows(m):
    a,b,c,d,e=m['coeff'];h,k=m['center'];u=coordinate('x',h);v=coordinate('y',k)
    rows=[r'f(x,y)&=c',expression(m)+r'&=c']
    if a and e and not(b or c or d):
        rhs=(term(k,'')+term(e,'c')+term(-e*a,u+'^2')).lstrip('+')
        rows.append('y&='+rhs)
    elif c and d and not(a or b or e):
        rhs=(term(h,'')+term(d,'c')+term(-d*c,v+'^2')).lstrip('+')
        rows.append('x&='+rhs)
    elif b:
        rows.append(v+r'&='+('-' if b<0 else '')+r'\frac{c}{'+u+r'}\quad(c\ne0)')
        rows.append(r'c=0&:\quad '+u+r'=0\ \text{or}\ '+v+r'=0')
    return rows



def identity(obj):
    return hashlib.sha256(json.dumps(asset_payload(obj),sort_keys=True,separators=(',',':')).encode()).hexdigest()


def uid(obj):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'ca-gradient-v1/'+identity(obj)))


def model(coeff, center=(0,0)):
    return {'coeff':list(coeff), 'center':list(center) if any(coeff[:3]) else [0,0]}


def value(m,x,y):
    a,b,c,d,e=m['coeff'];h,k=m['center'];u=x-h;v=y-k
    return a*u*u+b*u*v+c*v*v+d*u+e*v


def gradient(m,x,y):
    a,b,c,d,e=m['coeff'];h,k=m['center'];u=x-h;v=y-k
    return 2*a*u+b*v+d, b*u+2*c*v+e


def term(coef,body):
    if not coef:return ''
    return ('-' if coef<0 else '+') + (str(abs(coef)) if abs(coef)!=1 or not body else '') + body


def coordinate(name,shift):
    return name if shift==0 else r'\left('+name+('+' if shift<0 else '-')+str(abs(shift))+r'\right)'


def expression(m):
    a,b,c,d,e=m['coeff'];h,k=m['center'];u=coordinate('x',h);v=coordinate('y',k)
    return ''.join(term(co,body) for co,body in [(a,u+'^2'),(b,u+v),(c,v+'^2'),(d,u),(e,v)]).lstrip('+') or '0'


def gradient_tex(m):
    a,b,c,d,e=m['coeff'];h,k=m['center'];u=coordinate('x',h);v=coordinate('y',k)
    def lin(p,q,r):return ''.join([term(p,u),term(q,v),term(r,'')]).lstrip('+') or '0'
    return r'\left\langle '+lin(2*a,b,d)+','+lin(b,2*c,e)+r'\right\rangle'


def geometry(m):
    a,b,c,d,e=m['coeff']
    if not(a or b or c):return 'parallel straight lines'
    if b:return 'rectangular hyperbolas, with the two intersecting straight lines at the zero level'
    if a and c:
        if a*c<0:return 'axis-aligned hyperbolas, with two intersecting straight lines at the zero level'
        if a==c:return 'concentric circles'
        return 'ellipses stretched '+('horizontally' if abs(a)<abs(c) else 'vertically')
    if a:return ('upward' if -a/e>0 else 'downward')+'-opening parabolas'
    return ('right' if -c/d>0 else 'left')+'-opening parabolas'


def direction_reason(m):
    a,b,c,d,e=m['coeff'];h,k=m['center']
    center=f'$({h},{k})$'
    if not(a or b or c):
        return f'The labels increase in the normal direction proportional to $({d},{e})$. A perpendicular field pointing the opposite way would decrease the function.'
    if b:
        return f'Relative to {center}, increasing the product of the two coordinates increases the function.' if b>0 else f'Relative to {center}, decreasing the product of the two coordinates increases the function.'
    if a and c:
        if a*c>0:
            return f'Values increase {"away from" if a>0 else "toward"} the center {center}. Compare oblique points too: the two coordinate directions are weighted in the ratio ${abs(a)}:{abs(c)}$.'
        return f'With the other coordinate fixed, values increase {"away from" if a>0 else "toward"} $x={h}$ horizontally and {"away from" if c>0 else "toward"} $y={k}$ vertically.'
    if a:
        return f'With $x$ fixed, moving {"up" if e>0 else "down"} increases the function. With $y$ fixed, moving {"away from" if a>0 else "toward"} $x={h}$ increases it.'
    return f'With $y$ fixed, moving {"right" if d>0 else "left"} increases the function. With $x$ fixed, moving {"away from" if c>0 else "toward"} $y={k}$ increases it.'


class Plots:
    def __init__(self,root):
        self.root=Path(root).resolve();self.root.mkdir(parents=True,exist_ok=True)
        plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
    def draw(self,m,mode,offset=0):
        name='plot-'+identity([VERSION,m,mode,offset])+'.png';path=self.root/name
        if path.exists():return str(path)
        fig,ax=plt.subplots(figsize=(3.4,3.4),dpi=120)
        ax.set(xlim=(-3,3),ylim=(-3,3),aspect='equal',xticks=[-2,-1,1,2],yticks=[-2,-1,1,2])
        for side in ['left','bottom']:
            ax.spines[side].set_position('zero');ax.spines[side].set_color('#555')
        for side in ['right','top']:ax.spines[side].set_visible(False)
        ax.tick_params(labelsize=8,length=2);ax.text(2.79,-.35,'x');ax.text(.13,2.77,'y')
        if mode in ['contour','labeled','overlay','labeled-overlay']:
            t=np.linspace(-3,3,321);X,Y=np.meshgrid(t,t);Z=value(m,X,Y)+offset
            a,b,c,d,e=m['coeff']
            levels=[1,2,4,7,10] if a*c>0 and not b else [-4,-2,0,2,4]
            if a*c>0 and a<0:levels=[-10,-7,-4,-2,-1]
            levels=[q+offset for q in levels]
            cs=ax.contour(X,Y,Z,levels=levels,colors='#b87508',linewidths=1.4)
            if mode in ['labeled','labeled-overlay']:ax.clabel(cs,inline=True,fmt='%g',fontsize=9)
            if a*c>0:ax.plot(*m['center'],'.',color='#b87508',ms=3)
        if mode in ['field','overlay','labeled-overlay']:
            t=np.linspace(-2.4,2.4,7);U,V=np.meshgrid(t,t);P,Q=gradient(m,U,V);N=np.hypot(P,Q)
            P=np.divide(P,N,out=np.zeros_like(P),where=N>1e-10)*.43;Q=np.divide(Q,N,out=np.zeros_like(Q),where=N>1e-10)*.43
            ax.quiver(U,V,P,Q,angles='xy',scale_units='xy',scale=1,color='#24658a',width=.006,headwidth=4,headlength=5,pivot='mid')
            if np.any(N<1e-10):ax.plot(U[N<1e-10],V[N<1e-10],'.',color='#24658a',ms=3)
            a,b,c,d,e=m['coeff']
            if not(d or e) and (a or b or c):ax.plot(*m['center'],'.',color='#24658a',ms=3)
        fig.savefig(path,bbox_inches='tight',pad_inches=.12,facecolor='white',metadata={'Software':'Course Academy gradient generator '+VERSION})
        plt.close(fig)
        return str(path)


def make_record(level,target,bank,plots,rng,offset=0,profile='controlled'):
    # All dependent visible objects originate in this target and bank.
    bank=list(bank);rng.shuffle(bank)
    choice_mode='contour' if level=='moderate' else 'field'
    choices=[{':answer/type':':answer.type/image',':answer/value':plots.draw(m,choice_mode)} for m in bank]
    exp=expression(target);gtex=gradient_tex(target);shape=geometry(target)
    reminder='Recall that gradient vectors are **perpendicular** to level curves and point toward **increasing** function values.'
    if level=='easy':
        given=plots.draw(target,'labeled',offset)
        prompt=f'The labeled lines are level curves of a function $f(x,y)$.\n\n![Labeled level curves]({given})\n\n{reminder} Which diagram could show its gradient vector field? Arrows show directions only.'
    elif level=='moderate':
        given=plots.draw(target,'field')
        prompt=f'The diagram shows the gradient vector field of a function $f(x,y)$. Which of the following could be a contour plot of $f$? Arrows show directions only.\n\n![Given gradient directions]({given})'
    else:
        prompt=f'Which of the following could be the gradient vector field of $f(x,y)={exp}$? Use the relationship between level curves and gradient directions. Arrows show directions only.'
    if level=='easy':
        a,b,c,d,e=target['coeff']
        sol=f'The level curves are {shape}. A normal is proportional to $({d},{e})$. Use the labels to choose its sense: moving in that direction raises the labels, so it is the gradient direction. Tangent arrows fail perpendicularity; the opposite normal points toward smaller labels.'
        overlay=plots.draw(target,'labeled-overlay',offset)
    else:
        intro='First set $f(x,y)=c$.' if level=='hard' else 'The field must be perpendicular to every regular level curve. One compatible function, used here to check the geometric match, is '+f'$f(x,y)={exp}$.'
        sol=intro+'\n\n'+ '$$\n'+r'\begin{aligned}'+r'\\'.join(level_rows(target))+r'\end{aligned}'+'\n$$\n\n'+f'These level curves are {shape}. '+direction_reason(target)
        if level=='hard':
            contours=plots.draw(target,'labeled')
            sol+=f'\n\n![Derived labeled level curves]({contours})'
        else:
            sol+=' Unlabeled contours do not specify which side has larger values; the required test for these choices is perpendicularity, including at off-axis points.'
        sol+=f'\n\nA derivative check gives $\\nabla f={gtex}$. These directions are normal to the level curves and point toward increasing values. Other curve shapes have a different normal direction somewhere; a reversed field, if offered, points downhill.'
        overlay=plots.draw(target,'overlay')
    sol+=f'\n\n![Matching contours and gradient directions]({overlay})'
    final=plots.draw(target,choice_mode)
    sol+=f'\n\nTherefore choose this diagram:\n\n![Correct diagram]({final})'
    prompt=normalize_prose(prompt);sol=normalize_prose(sol)
    key=identity([VERSION,level,prompt,sol,[c[':answer/value'] for c in choices]])
    # IDs depend on normalized content, not a replay nonce.
    for c in choices:c[':answer/id']=uid([key,c[':answer/value']])
    correct=next(c[':answer/id'] for c,m in zip(choices,bank) if m==target)
    record={'knowledge_point':dict(KP),'question':{':question/id':uid(key),':question/difficulty':':question.difficulty/'+level,
        ':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':uid([key,'selection']),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},
        'generation':{'version':VERSION,'template':level,'profile':profile,'target':target,'bank':bank,'label_offset':offset,
                      'source_ids':source_ids(level,target),'domain':'real plane','arrow_contract':'direction only'}}
    return validate_generated_record(record)


def generate(level,count,seed,output):
    rng=random.Random(seed);plots=Plots(output);out=[];seen=set()
    profiles=['line'] if level=='easy' else ['contour'] if level=='moderate' else ['quadratic','parabolic','line']
    rng.shuffle(profiles);centers=list(CENTERS);rng.shuffle(centers);block=0
    while len(out)<count:
        if block>max(1000,count*50):raise ValueError('Requested count exceeds available semantic instances')
        profile=profiles[block%len(profiles)]
        catalog={'line':LINE,'contour':CONTOUR,'quadratic':QUADRATIC,'parabolic':PARABOLIC}[profile]
        # Constant fields have no center: no manufactured geometric diversity.
        center=(0,0) if profile=='line' else centers[(block//len(profiles))%len(centers)]
        bank=[model(c,center) for c in rng.sample(catalog,5)]
        targets=list(bank);rng.shuffle(targets)
        for target in targets:
            # Different banks/ordering do not create new assessed instances.
            sem=identity([level,target])
            if sem in seen:continue
            seen.add(sem)
            r=make_record(level,target,bank,plots,rng,offset=rng.choice([-1,0,1]) if level=='easy' else 0,profile=profile)
            r['generation'].update({'seed':seed,'block':block})
            out.append(r)
            if len(out)==count:break
        block+=1
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate')
    p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json')
    p.add_argument('--replay-source',action='store_true',help='Replay retained complete source records, without sampling')
    args=p.parse_args()
    if args.count<0:p.error('--count must be nonnegative')
    if args.replay_source:
        print(Path(__file__).with_name('source-replay.json').read_text());return
    output=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if not output:p.error('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR must name the generated asset directory')
    print(json.dumps(generate('moderate' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed,output),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
