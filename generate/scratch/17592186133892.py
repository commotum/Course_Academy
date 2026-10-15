#!/usr/bin/env python3
"""Bounded source-faithful line-integral variants, KP 17592186133892.

The supported generalization is homothetic geometry, preserving the observed
integrand and every complete source bank. x²-y uses weighted scaling (x,y)->
(k*x,k²*y). Sparse, unexplained distractors remain explicit expression patterns;
no new pedagogical error interpretations are claimed. Eight profiles x k=1..4.
"""
import argparse, hashlib, json, random, sys, uuid
from importlib.metadata import version
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).with_suffix('');ROOT=HERE.parents[2]
KP_ID=17592186133892;KP_UUID='b0712bb6-c0f8-5551-8362-ae23629aa618'
TITLE='Constructing Line Integrals With Respect to Y';VERSION='1.0.0'
t=sp.Symbol('t',real=True);x,y=sp.symbols('x y',real=True);s,c=sp.sin(t),sp.cos(t)
# Each bank entry is (outside coefficient, integrand). Order matches source.
PROFILES={
'q-124121':dict(kind='line',X=3*t-1,Y=6*t-2,F=x*y,lo=0,hi=1,degree=3,index=1,bank=[(12,t*t-6*t+9),(12,9*t*t-6*t+1),(18,t*t-6*t+9),(18,t*t+6*t+9),(6,9*t*t-6*t+1)]),
'q-124270':dict(kind='line',X=3*t-1,Y=2*t-1,F=x*x-y,lo=0,hi=1,degree=4,index=2,weighted=True,bank=[(9,2*t*t-t+7),(1,18*t*t+t),(2,9*t*t-8*t+2),(3,6*t*t+5),(6,2*t*t+7*t+1)]),
'q-124266':dict(kind='line',X=t-2,Y=2-t,F=3*x+2*y,lo=0,hi=1,degree=2,index=1,bank=[(1,5-2*t),(1,2-t),(1,3*t+1),(1,t*t+3*t-1),(1,1-t*t)]),
'q-124272':dict(kind='line',X=2*t,Y=3*t,F=x*x+y*y,lo=0,hi=1,degree=3,index=4,bank=[(13,t*t),(13,3*t*t+1),(9,3-t*t),(26,3*t*t-1),(39,t*t)]),
'q-124283':dict(kind='circle',X=4*c,Y=4*s,F=x*y,lo=0,hi=sp.pi,degree=3,index=1,excluded='Two distractors evaluate to zero; full bank is not pairwise distinct.',bank=[(32,s*c),(64,s*c*c),(64,s+c),(16,s+c*c),(4,s*s*c)]),
'q-124279':dict(kind='circle',X=3*c,Y=3*s,F=x-y,lo=-sp.pi/2,hi=sp.pi/2,degree=2,index=1,bank=[(3,(c-s)*c*c),(9,(c-s)*c),(1,(c-s)*c),(3,(c-s)*s),(9,(c-s)*s*s)]),
'q-124287':dict(kind='ellipse',X=c,Y=3*s,F=9-y*y,lo=sp.pi/2,hi=2*sp.pi,degree=3,index=2,constant_scales=True,bank=[(9,s*s*c),(27,s*c*c),(27,c**3),(18,s**3),(18,c*c)]),
'q-124277':dict(kind='circle',X=2*c,Y=2*s,F=x*x*y,lo=sp.pi,hi=3*sp.pi/2,degree=4,index=0,bank=[(16,s*c**3),(4,s+c*c),(4,s*s*c*c),(8,s*s*c*c),(8,s*c**3)]),
'q-124293':dict(kind='ellipse',X=2*c,Y=s,F=x*y,lo=sp.pi/2,hi=sp.pi,degree=3,index=2,bank=[(1,2*s+c),(4,s*s*c),(2,s*c*c),(2,s+c*c),(2,s*c)]),
'q-124298':dict(kind='ellipse',X=2*c,Y=4*s,F=3*x*x+y*y,lo=sp.pi,hi=2*sp.pi,degree=3,index=3,excluded='Two complete integrals evaluate to zero, including the designated correct value.',bank=[(16,(3*s*s+1)*c),(8,(3*s*s+1)*s),(16,(s*s+3)*s*s),(16,(s*s+3)*c),(4,(s*s+3)*c*c)])}
SUPPORTED=tuple(p for p,v in PROFILES.items() if not v.get('excluded'))
SNAPSHOT=json.loads((HERE/'source.json').read_text())
def tex(expr):return sp.latex(sp.sympify(expr),fold_short_frac=False).replace(r'{\left(t \right)}',' t')
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def task(profile,k):
 p=PROFILES[profile];X=k*p['X'];Y=k**(2 if p.get('weighted') else 1)*p['Y'];F=p['F']
 if p.get('constant_scales'):F=9*k*k-y*y
 return X,Y,F,sp.sympify(p['lo']),sp.sympify(p['hi'])
def fingerprint(profile,k):return digest([sp.srepr(z) for z in task(profile,k)])
def integral(coef,expr,lo,hi):return (tex(coef) if coef!=1 else '')+rf'\int_{{{tex(lo)}}}^{{{tex(hi)}}}\left({tex(expr)}\right)\,\mathrm{{d}}t'
def plot(profile,k,output_dir=None):
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 import numpy as np
 p=PROFILES[profile];X,Y,_,lo,hi=task(profile,k);ident=fingerprint(profile,k)[:24]
 out=Path(output_dir or HERE/'assets');out.mkdir(parents=True,exist_ok=True);path=out/(ident+'.png')
 if path.exists():return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
 values=np.linspace(float(lo),float(hi),400);xx=np.asarray(sp.lambdify(t,X,'numpy')(values));yy=np.asarray(sp.lambdify(t,Y,'numpy')(values))
 fig,ax=plt.subplots(figsize=(4.6,3.6),layout='constrained');ax.plot(xx,yy,color='#226ab0',lw=2)
 for f in (.3,.7):
  a=float(lo)+(float(hi)-float(lo))*f;b=a+(float(hi)-float(lo))*.04
  ax.annotate('',xy=(float(X.subs(t,b)),float(Y.subs(t,b))),xytext=(float(X.subs(t,a)),float(Y.subs(t,a))),arrowprops=dict(arrowstyle='->',color='#226ab0',lw=1.5))
 endpoints=[]
 for v in (lo,hi):
  px,py=X.subs(t,v),Y.subs(t,v);endpoints.append((float(px),float(py)));ax.scatter([float(px)],[float(py)],s=16,color='#226ab0',zorder=4)
  # Labels pulled inside figure by expanding bounds below.
  ax.annotate(f'({px}, {py})',(float(px),float(py)),xytext=(7,7),textcoords='offset points',fontsize=9)
 ax.axhline(0,color='black',lw=.8);ax.axvline(0,color='black',lw=.8);ax.set_xlabel('$x$');ax.set_ylabel('$y$',rotation=0);ax.set_aspect('equal',adjustable='box');ax.margins(.28);ax.spines[['top','right']].set_visible(False)
 mid=(lo+hi)/2;ax.annotate('$C$',(float(X.subs(t,mid)),float(Y.subs(t,mid))),xytext=(6,9),textcoords='offset points',color='#226ab0');fig.savefig(path,dpi=150);plt.close(fig)
 return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
def generate(difficulty='easy',seed=0,*,profile=None,k=None,replay=False,render=True):
 if difficulty!='easy':raise ValueError('Unsupported difficulty: only easy is evidenced and validated; moderate/hard remain unfilled.')
 rng=random.Random(seed);profile=profile or rng.choice(SUPPORTED);p=PROFILES[profile];k=rng.choice(range(1,5)) if k is None else k
 if type(k)!=int or k not in range(1,5):raise ValueError('Scale k must be an integer in [1,4].')
 if p.get('excluded') and not replay:raise ValueError(p['excluded'])
 X,Y,F,lo,hi=task(profile,k);dy=sp.diff(Y,t);sub=sp.expand(F.subs({x:X,y:Y},simultaneous=True));correct=sp.trigsimp(sub*dy)
 uid=uuid.uuid5(uuid.UUID(KP_UUID),'line-y-v1/'+fingerprint(profile,k));fid=uuid.uuid5(uid,'field/selection')
 bank=[]
 for i,(coef,expr) in enumerate(p['bank']):
  aid=uuid.uuid5(fid,f'answer/{i}');bank.append({':answer/id':str(aid),':answer/type':':answer.type/math',':answer/value':integral(coef*k**p['degree'],expr,lo,hi)})
 field={':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':bank,':answer-field/correct':[':answer/id',bank[p['index']][':answer/id']]}
 start=tuple(sp.simplify(v.subs(t,lo)) for v in (X,Y));end=tuple(sp.simplify(v.subs(t,hi)) for v in (X,Y));point=lambda v:rf'({tex(v[0])},{tex(v[1])})'
 r=rf'r(t)=\langle {tex(X)},\,{tex(Y)}\rangle'
 if p['kind']=='line':
  path=rf'the line segment from the point ${point(start)}$ to the point ${point(end)}$'
  param=rf'The curve $C$ is a line segment with endpoints ${point(start)}$ and ${point(end)}$. It can be parametrized as'+ '\n\n$$\n'+rf'\begin{{aligned}}r(t)&=\langle {tex(start[0])}+t({tex(end[0])}-({tex(start[0])})),\,{tex(start[1])}+t({tex(end[1])}-({tex(start[1])}))\rangle\\&=\langle {tex(X)},\,{tex(Y)}\rangle,\end{{aligned}}'+'\n$$\n\nwhere $0\\le t\\le 1$.'
 else:
  a=sp.simplify(X/c);b=sp.simplify(Y/s)
  if p['kind']=='circle':path=rf'a circle of radius ${tex(a)}$, traversed counterclockwise from the point ${point(start)}$ to the point ${point(end)}$';lead=rf'The curve $C$ is a part-circle of radius ${tex(a)}$ centered at $O$.'
  else:
   equation=rf'{tex(b*b)}x^2+{tex(a*a)}y^2={tex(a*a*b*b)}'
   extent='three-quarters of the ellipse' if hi-lo==3*sp.pi/2 else ('a quarter of the ellipse' if hi-lo==sp.pi/2 else 'the ellipse')
   path=rf'{extent} ${equation}$, traversed counterclockwise from the point ${point(start)}$ to the point ${point(end)}$';lead='The curve $C$ can be parameterized as'
  param=lead+'\n\n$$\n'+r+rf',\qquad {tex(lo)}\le t\le {tex(hi)}.'+'\n$$'
 image=plot(profile,k) if render else f'generate/scratch/{KP_ID}/assets/{fingerprint(profile,k)[:24]}.png'
 prompt=f'![]({image})\n\n'+rf'Which of the following is equivalent to $\int_C\left({tex(F)}\right)\,\mathrm{{d}}y$, where $C$ is the path along {path}, as shown above?'+'\n\n*Hint: Use the parametrization $'+r+'$.*'
 # The ordered source stages are retained: formula, parametrization, dy/dt,
 # substitution (including trig identity when present), assembly. No evaluation.
 substitution=rf'f(r(t))&={tex(F)}\big|_{{x={tex(X)},\,y={tex(Y)}}}\\&={tex(sub)}'
 if p.get('constant_scales'):substitution+=rf'\\&={9*k*k}(1-\sin^2 t)\\&={9*k*k}\cos^2 t'
 if profile=='q-124298':substitution+=rf'\\&={4*k*k}\sin^2 t+{12*k*k}(\sin^2 t+\cos^2 t)\\&={4*k*k}(\sin^2 t+3)'
 answer=bank[p['index']][':answer/value']
 solution='We will use the formula\n\n$$\n'+r'\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.'+'\n$$\n\n'+param+'\n\nComputing $\\frac{\\mathrm{d}y}{\\mathrm{d}t}$, we get the following:\n\n$$\n'+rf'\frac{{\mathrm{{d}}y}}{{\mathrm{{d}}t}}=\frac{{\mathrm{{d}}}}{{\mathrm{{d}}t}}\left({tex(Y)}\right)={tex(dy)}.'+'\n$$\n\n'+rf'Now, since $f(x,y)={tex(F)}$, we obtain'+'\n\n$$\n'+r'\begin{aligned}'+substitution+r'.\end{aligned}'+'\n$$\n\nTherefore, we can write the integral as\n\n$$\n'+rf'\begin{{aligned}}\int_C f(x,y)\,\mathrm{{d}}y&=\int_{{{tex(lo)}}}^{{{tex(hi)}}} f(r(t))\,\frac{{\mathrm{{d}}y}}{{\mathrm{{d}}t}}\,\mathrm{{d}}t\\&=\int_{{{tex(lo)}}}^{{{tex(hi)}}}\left({tex(sub)}\right)\left({tex(dy)}\right)\,\mathrm{{d}}t\\&={answer}.\end{{aligned}}'+'\n$$'
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':str(uid),':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'template':profile,'bank_profile':profile,'parameters':{'k':k},'domains':{'k':[1,2,3,4]},'source_basis':SNAPSHOT['basis'],'lineage':SNAPSHOT['lineage'],'source_question':profile,'evidence_only':bool(p.get('excluded')),'mathematical_fingerprint':fingerprint(profile,k),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':version('matplotlib'),'numpy':version('numpy')},'assets':[image]}}
def batch(difficulty,count,seed=0,render=True):
 if difficulty!='easy':raise ValueError('Unsupported difficulty; moderate and hard remain unfilled.')
 if count<0 or count>32:raise ValueError('Finite domain: at most 32 distinct easy tasks (8 profiles x 4 scales).')
 slots=[(p,k) for p in SUPPORTED for k in range(1,5)];random.Random(seed).shuffle(slots)
 return [generate(difficulty,seed,profile=p,k=k,render=render) for p,k in slots[:count]]
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join(f"- ${a[':answer/value']}$" for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',default='easy');ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');args=ap.parse_args()
 try:rs=batch(args.difficulty,args.count,args.seed)
 except ValueError as e:ap.exit(2,str(e)+'\n')
 print(json.dumps(rs,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
