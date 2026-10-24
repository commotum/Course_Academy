#!/usr/bin/env python3
"""Finite easy triangle-orientation generator. No database access or durable writes.

All eight relative edge-orientation vectors are the finite mathematical domain.
Coordinates, names, winding, bank profile and seed do not create new tasks.
Uniform vectors are conservative same-method extensions of the six source states.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
import argparse,copy,hashlib,itertools,json,random,re,uuid,os
os.environ.setdefault("MPLCONFIGDIR","/tmp/course-academy-matplotlib")
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
KP_ID=17592186179672
KP_UUID=SOURCE['record'][':knowledge-point/id']
TITLE=SOURCE['record'][':knowledge-point/title']
VERSION='triangle-orientation-1'
LEVELS=('easy',)
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
DOMAIN=tuple(itertools.product((-1,1),repeat=3))
I=sp.symbols('I1:4')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def signs(value):
 parts=re.findall(r'(^|[+-])\{\\int \}_\{\{C\}_\{([123])\}\}F\\cdot \\text\{d\}r',value)
 if len(parts)!=3 or [int(i) for _,i in parts]!=[1,2,3]:raise ValueError('unrecognized three-integral source value: '+value)
 return tuple(-1 if s=='-' else 1 for s,_ in parts)
def integral(i,reverse=False):return r'{\int }_{'+('-' if reverse else '')+r'{C}_{'+str(i)+r'}}F\cdot \text{d}r'
def value(vector):return ''.join(('-' if s<0 else ('+' if i else ''))+integral(i+1) for i,s in enumerate(vector))
def fingerprint(vector):return digest(['triangle-three-directed-edges',list(vector)])
def profile(mid,vector):
 f=SOURCES[mid][':question/answer-fields'][0];correct=signs(f[':answer-field/correct'][':answer/value'])
 # Whole observed bank, in source order. Each recipe is an exact componentwise
 # sign-flip mask relative to that source's correct vector, not a guessed error.
 masks=[tuple(a*b for a,b in zip(signs(o[':answer/value']),correct)) for o in f[':answer-field/choices']]
 return [tuple(a*b for a,b in zip(mask,vector)) for mask in masks],masks

def render_plots(vector,output_dir):
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 import numpy as np
 output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
 path=output_dir/(fingerprint(vector)+'-prompt.png')
 pts=np.array([[-2.,-1.],[3.,-1.],[.7,3.]]) # ABC is positively oriented.
 fig,ax=plt.subplots(figsize=(4.7,4.2),dpi=140)
 for i,s in enumerate(vector):
  a,b=pts[i],pts[(i+1)%3];a,b=(a,b) if s==1 else (b,a);color=['#b82924','#1763a0','#8a5700'][i]
  ax.plot([a[0],b[0]],[a[1],b[1]],color=color,lw=1.8)
  for t in (.35,.65):
   p=a+(t-.045)*(b-a);q=a+(t+.045)*(b-a);ax.annotate('',xy=q,xytext=p,arrowprops=dict(arrowstyle='->',color=color,lw=1.6))
  mid=(a+b)/2;center=pts.mean(axis=0);offset=mid-center;offset=.35*offset/np.linalg.norm(offset)
  ax.text(*(mid+offset),f'$C_{i+1}$',color=color,ha='center',va='center',fontsize=13)
 for label,p in zip('ABC',pts):
  ax.plot(*p,'ko',ms=4);delta=p-pts.mean(axis=0);delta=.28*delta/np.linalg.norm(delta);ax.text(*(p+delta),f'${label}$',ha='center',va='center',fontsize=13)
 ax.annotate('',xy=(3.9,0),xytext=(-2.9,0),arrowprops=dict(arrowstyle='->',color='black',lw=.8))
 ax.annotate('',xy=(0,3.8),xytext=(0,-1.9),arrowprops=dict(arrowstyle='->',color='black',lw=.8))
 ax.text(3.85,-.25,'$x$');ax.text(.15,3.6,'$y$');ax.set(xlim=(-2.9,4.2),ylim=(-2,3.95),aspect='equal');ax.axis('off');fig.tight_layout(pad=.2);fig.savefig(path,metadata={'Software':'Course Academy triangle-orientation-1'});plt.close(fig)
 return {'prompt':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'renderer':'matplotlib','matplotlib':matplotlib.__version__,'points':pts.tolist(),'reference_edges':[[i,(i+1)%3] if s==1 else [(i+1)%3,i] for i,s in enumerate(vector)]}

def solution(vector):
 paths=[('-' if s<0 else '')+f'C_{i+1}' for i,s in enumerate(vector)]
 decomposition=' \\cup '.join(r'\{'+p+r'\}' if p.startswith('-') else p for p in paths)
 reversed_names=[f'$C_{i+1}$' for i,s in enumerate(vector) if s<0]
 note=(('The path '+reversed_names[0]+' is traversed in the opposite direction to its arrow.') if len(reversed_names)==1 else ('The paths '+', '.join(reversed_names)+' are traversed in the opposite direction to their arrows.')) if reversed_names else 'Each component is traversed in the direction of its arrows.'
 directed='+'.join(integral(i+1,s<0) for i,s in enumerate(vector))
 return 'First, notice that we can represent $C$, traversed counterclockwise, as the union of $3$ paths:\n\n$$\nC='+decomposition+'.\n$$\n\n'+note+' Reversing a path changes the sign of its vector line integral.\n\nTherefore, we obtain\n\n$$\n\\begin{aligned}'+r'{\int }_{C}F\cdot \text{d}r'+r' &= '+directed+r' \\ &= '+value(vector)+r'.\end{aligned}'+'\n$$'

def generate(level='easy',seed=0,parameters=None,profile_id=None,output_dir=None):
 if level not in LEVELS:raise ValueError('Unsupported difficulty: '+level+'; no validated source template at this workload')
 rng=random.Random(seed);vector=tuple(parameters['signs']) if parameters is not None else rng.choice(DOMAIN)
 if len(vector)!=3 or any(type(s) is not int for s in vector) or vector not in DOMAIN:raise ValueError('three signs must each be -1 or +1')
 mid=profile_id or rng.choice(sorted(SOURCES));bank,masks=profile(mid,vector);values=[value(v) for v in bank]
 assert len(values)==len(set(values))==5 and bank.count(vector)==1
 asset=render_plots(vector,output_dir or HERE/'plots')
 prompt='![]('+str(Path(asset['prompt']).resolve())+')\n\nWhich of the following is equivalent to the integral $'+r'{\int }_{C}F\cdot \text{d}r'+',$ where $C$ is the closed polygonal path $ABCA$, shown in the diagram above, traversed in the counterclockwise direction?\n\n{{selection}}'
 sol=solution(vector);contract=[prompt,sol,sorted(values),value(vector),'easy'];qid=str(uuid.uuid5(uuid.UUID(KP_UUID),'generated:'+digest(contract)));fid=str(uuid.uuid5(uuid.UUID(qid),'field:selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'value:'+v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[bank.index(vector)][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'parameters':{'signs':list(vector)},'template':'triangle-three-oriented-edges','bank_profile':mid,'recipes':[list(m) for m in masks],'source_basis':SOURCE['basis'],'mathematical_fingerprint':fingerprint(vector),'domain':'eight relative edge orientations; independent formal component integrals; arbitrary vector field','dependencies':{'sympy':sp.__version__},'asset':asset,'extension':all(s==vector[0] for s in vector)}}

def replay_source(mid):
 q=copy.deepcopy(SOURCES[mid]);f=q[':question/answer-fields'][0];vector=signs(f[':answer-field/correct'][':answer/value']);bank,_=profile(mid,vector)
 return {'source_id':mid,'signs':list(vector),'generated_bank':[value(v) for v in bank],'source_bank':[a[':answer/value'] for a in f[':answer-field/choices']],'correct':value(vector),'original':q}

def batch(level,count,seed=0):
 if level not in LEVELS:raise ValueError('Unsupported difficulty: '+level)
 if not 1<=count<=8:raise ValueError('finite-limit: only eight genuinely distinct orientation states')
 domain=list(DOMAIN);rng=random.Random(seed);rng.shuffle(domain)
 return [generate(level,seed+i,{'signs':v}) for i,v in enumerate(domain[:count])]
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('$'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rs=batch(a.difficulty,a.count,a.seed);print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
