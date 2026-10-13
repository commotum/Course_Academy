#!/usr/bin/env python3
"""Bounded, source-bank-preserving point/line distance generator.

The only parameter extension is a positive integral dilation 1..9 of a
complete source geometry and its complete distance bank. No bank mixing.
"""
import argparse
import hashlib
import json
import os
import random
import re
import uuid
from pathlib import Path
import sympy as sp

KP_ID = 17592186073811
KP_UUID = 'd7030a12-bd18-5f8b-84eb-28b6f216f972'
TITLE = 'Finding the Distance Between a Point and a Line'
VERSION = 'point-line-dilation-v1'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
PACKAGE = Path(__file__).with_suffix('')
SOURCE = json.loads((PACKAGE/'source.json').read_text())['record']
SOURCES = {q[':question/math-academy-id']: q for q in SOURCE[':knowledge-point/questions']}
# A*x+B*y=C; x0,y0. Keep source profiles separate, including ±unit slopes.
CASES = {
    'q-114341': [3,2,6,1,-5],
    'q-114343': [-1,1,-2,-1,5],
    'q-74417': [1,1,2,-1,-3],
    'q-74420': [-1,3,-9,5,-8],
    'q-114358': [5,2,10,-5,3],
    'q-114364': [3,2,-6,2,'1/2'],
    'q-74435': [2,1,-2,-3,-6],
}

def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def ident(x):
    return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(x)))

def tex(x):
    return sp.latex(sp.simplify(x)).replace('- ', '-')

def value(text):
    m=re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}',text)
    return sp.Integer(m[1] or 1)*sp.sqrt(int(m[2])) if m else sp.Rational(text)

def data(sid,k):
    A,B,C,x0,y0=map(sp.Rational,CASES[sid])
    C,x0,y0=C*k,x0*k,y0*k
    m=-A/B; b=C/B; n=-1/m; c=y0-n*x0
    h=sp.cancel((c-b)/(m-n)); j=sp.cancel(m*h+b)
    d=sp.sqrt((h-x0)**2+(j-y0)**2)
    return dict(A=A,B=B,C=C,x0=x0,y0=y0,m=m,b=b,n=n,c=c,h=h,j=j,d=d)

def line(m,b):
    return 'y='+tex(m*sp.Symbol('x')+b)

def equation(z,hard):
    if not hard:return line(z['m'],z['b'])
    return tex(z['B']*sp.Symbol('y')+z['A']*sp.Symbol('x'))+'='+tex(z['C'])

def fingerprint_geometry(A,B,C,x0,y0):
    # Equation rescaling, display order and bank identity do not create novelty.
    A,B,C,x0,y0=map(sp.Rational,(A,B,C,x0,y0))
    return digest(['point-line',str(A/B),str(C/B),str(x0),str(y0)])

def fingerprint(p):
    sid,k=p;z=data(sid,k)
    return fingerprint_geometry(*(z[a] for a in ('A','B','C','x0','y0')))

def render_plots(z,sid,k):
    """Same geometry as the answer: blue line, red point, dashed normal, square."""
    os.environ.setdefault('MPLCONFIGDIR','/tmp/course-academy-distance-mpl')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Polygon
    cache=PACKAGE/'assets'/f'{sid}-{k}-render2.png'
    cache.parent.mkdir(exist_ok=True)
    if not cache.exists():
        P=np.array([float(z['x0']),float(z['y0'])]); H=np.array([float(z['h']),float(z['j'])])
        normal=(P-H)/np.linalg.norm(P-H); tangent=np.array([1,float(z['m'])]);tangent/=np.linalg.norm(tangent)
        dist=float(z['d']);s=dist*.10
        fig,ax=plt.subplots(figsize=(5,4),dpi=120)
        ends=np.array([H-1.15*dist*tangent,H+1.15*dist*tangent]);ax.plot(ends[:,0],ends[:,1],color='#2878b8',lw=2)
        ax.plot([H[0],P[0]],[H[1],P[1]],'k--',lw=1)
        ax.scatter(*P,color='red',s=25,zorder=5);ax.scatter(*H,color='#2878b8',s=18,zorder=5)
        ax.add_patch(Polygon([H,H+s*tangent,H+s*(tangent+normal),H+s*normal],color='#f4cd70'))
        ax.annotate('$('+tex(z['x0'])+','+tex(z['y0'])+')$',P,xytext=(12*normal[0],12*normal[1]),textcoords='offset points',fontsize=12,ha='left' if normal[0]>=0 else 'right',va='bottom' if normal[1]>=0 else 'top')
        ax.text(*(H+(P-H)*.52+s*tangent),'?',fontsize=14)
        Q=H-.75*dist*tangent-.18*dist*normal
        ax.text(*Q,'$'+equation(z,sid.startswith('q-11435') or sid in ('q-114364','q-74435'))+'$',fontsize=11,rotation=float(np.degrees(np.arctan(float(z['m'])))))
        allpoints=np.vstack([ends,P,Q]);lo=allpoints.min(axis=0)-.45*dist;hi=allpoints.max(axis=0)+.45*dist
        ax.set_xlim(lo[0],hi[0]);ax.set_ylim(lo[1],hi[1]);ax.set_aspect('equal');ax.axis('off')
        fig.savefig(cache,facecolor='white',metadata={'Software':VERSION});plt.close(fig)
    content=cache.read_bytes();sha=hashlib.sha256(content).hexdigest()
    return {'path':f'images/{sha[:2]}/{sha}.png','local_path':str(cache.relative_to(PACKAGE.parents[2])),'sha256':sha,'role':'worked-solution'}

def solution(z,eq,hard,asset):
    t={a:tex(v) for a,v in z.items()}; given=line(z['m'],z['b']);perp=line(z['n'],z['c'])
    result=''
    if hard:
        result="First, we rewrite the equation of the given line in slope-intercept form:\n\n$$\n\\begin{aligned}"+eq.replace('=',' & =')+r' \\ y & ='+tex(z['m']*sp.Symbol('x')+z['b'])+'\\end{aligned}\n$$\n\n'
    result+="Let's draw a diagram describing our situation.\n\n![]("+asset['path']+")\n\n"
    result+=("Next" if hard else "First")+", we find the equation of the line that's perpendicular to $"+given+'$ and passes through the point $('+t['x0']+','+t['y0']+').$\n\n'
    result+='The given line has a slope of $'+t['m']+',$ so our perpendicular line must have a slope of $'+t['n']+'.$\n\n'
    result+='Using point-slope form and simplifying, we obtain the equation of the perpendicular line:\n\n$$\n'+r'\begin{aligned}y-y_1 & =m(x-x_1) \\ y-('+t['y0']+r') & ='+t['n']+r'(x-('+t['x0']+r')) \\ y & ='+tex(z['n']*sp.Symbol('x')+z['c'])+'\\end{aligned}\n$$\n\n'
    result+='We now find the point where the two lines intersect. To do this, we solve the following system of equations:\n\n$$\n'+r'\begin{aligned}'+given+r' \\ '+perp+'\\end{aligned}\n$$\n\n'
    result+='We can solve this system by putting the two equations equal to one another and solving for $x.$ This gives\n\n$$\n'+r'\begin{aligned}'+tex(z['m']*sp.Symbol('x')+z['b'])+' & ='+tex(z['n']*sp.Symbol('x')+z['c'])+r' \\ ('+tex(z['m']-z['n'])+r')x & ='+tex(z['c']-z['b'])+r' \\ x & ='+t['h']+'\\end{aligned}\n$$\n\n'
    result+='Substituting $x='+t['h']+'$ into either of the two equations gives $y='+t['j']+'.$ So, our solution is $x='+t['h']+'$ and $y='+t['j']+'.$ Therefore, the lines intersect at the point $('+t['h']+','+t['j']+').$\n\n'
    result+='Finally, we find the distance $d$ between the points $('+t['x0']+','+t['y0']+')$ and $('+t['h']+','+t['j']+'):$\n\n$$\n'+r'\begin{aligned}d & =\sqrt{(x_2-x_1)^2+(y_2-y_1)^2} \\ & =\sqrt{('+t['h']+'-('+t['x0']+r'))^2+('+t['j']+'-('+t['y0']+r'))^2} \\ & =\sqrt{'+tex((z['h']-z['x0'])**2)+'+'+tex((z['j']-z['y0'])**2)+r'} \\ & ='+t['d']+'\\end{aligned}\n$$\n\n'
    result+='Therefore, we conclude that the shortest distance between the point $('+t['x0']+','+t['y0']+')$ and the line $'+eq+'$ is $'+t['d']+'.$'
    return result

def generate(difficulty='moderate',seed=0,template=None,parameters=None):
    if difficulty not in ('moderate','hard'):raise ValueError('Unsupported level; see capabilities.json')
    eligible=[sid for sid in CASES if SOURCES[sid][':question/difficulty'][':db/ident'].endswith('/'+difficulty)]
    rng=random.Random(seed);sid=template or rng.choice(eligible)
    k=parameters[1] if parameters else rng.randint(2,9)
    if sid not in eligible or type(k)!=int or not 1<=k<=9:raise ValueError('Outside validated bounded profile')
    if parameters and parameters!=[sid,k]:raise ValueError('Parameter/template mismatch')
    z=data(sid,k);old=SOURCES[sid];of=old[':question/answer-fields'][0];hard=difficulty=='hard';eq=equation(z,hard)
    values=[tex(k*value(a[':answer/value'])) for a in of[':answer-field/choices']]
    correct=tex(k*value(of[':answer-field/correct'][':answer/value']))
    if len(set(values))!=5 or correct!=tex(z['d']):raise ValueError('Invalid source profile')
    if k==1:
        problem=old[':question/problem'];worked=old[':question/worked-solution']
        if sid=='q-114358':worked=worked.replace(r'\frac{29}{10}x & =0',r'-\frac{29}{10}x & =0')
        ref=re.search(r'!\[\]\((.*?)\)',worked)[1];path=Path('/media/jake/SSD/EDB/math')/ref
        assets=[{'path':ref,'local_path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'role':'worked-solution','unchanged_source_asset':True}]
    else:
        assets=[render_plots(z,sid,k)];problem='Find the shortest distance between the point $('+tex(z['x0'])+','+tex(z['y0'])+')$ and the line $'+eq+'.$';worked=solution(z,eq,hard,assets[0])
    fp=fingerprint([sid,k]);qid=ident(['question',VERSION,fp,digest(sorted(values)),sid]);fid=ident([qid,'field','selection'])
    choices=[{':answer/id':ident([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    aid=next(a[':answer/id'] for a in choices if a[':answer/value']==correct)
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':worked,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',aid]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':sid,'parameters':[sid,k],'domain':'Euclidean plane over the real numbers; distance positive; nonzero finite slopes','source_ids':[sid],'mathematical_fingerprint':fp,'assets':assets,'sympy':sp.__version__,'sampling_policy':'positive integral dilation 1..9; k=1 source replay, k>=2 new candidates','solution_fidelity':'original source at k=1 with documented sign correction; normalized numeric alignments for k>1, same instructional sequence'}}

def batch(difficulty,count,seed=0):
    candidates=[generate(difficulty,seed,sid,[sid,k]) for sid in CASES if SOURCES[sid][':question/difficulty'][':db/ident'].endswith('/'+difficulty) for k in range(2,10)]
    random.Random(seed).shuffle(candidates)
    if count>len(candidates):raise ValueError('Finite validated family exhausted; shortage remains explicit')
    return candidates[:count]

def markdown(rec):
    q=rec['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',default='moderate');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rs=batch(a.difficulty,a.count,a.seed)
    print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
