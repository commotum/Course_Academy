#!/usr/bin/env python3
"""Bounded easy generator: linear potential, one observed five-image bank.
Other captured families are classified but not supported by this version.
"""
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as s
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).with_suffix('')
KP_ID=17592186179719
KP=json.loads((HERE/'reference/initial/source.json').read_text())['record']
SOURCE=next(q for q in KP[':knowledge-point/questions'] if q[':question/math-academy-id']=='q-122699')
POINTS=((-2,2),(2,2),(2,-2))
COEFFICIENTS=(-3,-2,-1,1,2,3)
SUPPORTED_LEVELS=('easy',)
VERSION='1.0.0'
x,y=s.symbols('x y', real=True)
def vectors(a,b):
 return [[(a*px,a) for px,py in POINTS],[(a,b)]*3,[(a,0)]*3,[(a*px,b) for px,py in POINTS],[(0,b)]*3]
def render(bank,index,out):
 out.mkdir(parents=True,exist_ok=True)
 data={'points':POINTS,'vectors':bank,'index':index,'renderer':VERSION}
 digest=hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
 path=out/(digest+'.png')
 if not path.exists():
  fig,ax=plt.subplots(figsize=(4,4),dpi=120)
  # Identical unit grid and unnormalized arrows in every option, all endpoints visible.
  ax.set(xlim=(-9,9),ylim=(-9,9),aspect='equal',xticks=range(-8,9,2),yticks=range(-8,9,2))
  ax.set_xticks(range(-9,10),minor=True);ax.set_yticks(range(-9,10),minor=True)
  ax.grid(which='both',color='#dddddd',linewidth=.5);ax.axhline(0,color='black',linewidth=.8);ax.axvline(0,color='black',linewidth=.8)
  ax.set_xlabel('x');ax.set_ylabel('y',rotation=0)
  for (px,py),(u,v) in zip(POINTS,bank):
   ax.scatter([px],[py],c='#e5a000',s=18,zorder=4)
   ax.annotate('',xy=(px+u,py+v),xytext=(px,py),arrowprops={'arrowstyle':'->','color':'#287bb0','lw':1.6,'shrinkA':0,'shrinkB':0})
  fig.tight_layout();fig.savefig(path,metadata={'Software':'Course Academy '+VERSION});plt.close(fig)
  path.with_suffix('.json').write_text(json.dumps(data,indent=2))
 return str(path.relative_to(ROOT))
def generate(difficulty='easy',seed=0,template='linear',parameters=None):
 if difficulty!='easy':raise ValueError('Unsupported difficulty: bounded package supports easy only')
 if template!='linear':raise ValueError('Unsupported template')
 rng=random.Random(seed)
 p=parameters or dict(zip(('a','b'),rng.choice([(a,b) for a in COEFFICIENTS for b in COEFFICIENTS if a!=b])))
 a,b=int(p['a']),int(p['b']);assert a in COEFFICIENTS and b in COEFFICIENTS and a!=b
 banks=vectors(a,b);assert len({tuple(v) for v in banks})==5
 f=a*x+b*y;grad=(s.diff(f,x),s.diff(f,y));assert grad==(a,b)
 sig=f'linear-gradient:{a},{b}';qid=str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),sig+':'+VERSION));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 paths=[render(v,i,HERE/'plots') for i,v in enumerate(banks)]
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),str(i))),':answer/type':':answer.type/image',':answer/value':p} for i,p in enumerate(paths)]
 prompt=f'Which of the following diagrams represents the gradient vector field of the function $f(x,y)={s.latex(f)}$?'
 solution=('The gradient vector field of a function $f$ is given by $\\nabla f.$\n\nFirst, we find the partial derivatives:\n\n'
  +f'$$f_x(x,y)=\\frac{{\\partial}}{{\\partial x}}({s.latex(f)})={a},\\qquad f_y(x,y)=\\frac{{\\partial}}{{\\partial y}}({s.latex(f)})={b}.$$\n\n'
  +f'So, the gradient vector field is $\\nabla f(x,y)=({a})\\,i+({b})\\,j.$\n\n'
  +'Next, we sketch the vector field at the points $(-2,2)$, $(2,2)$, and $(2,-2)$. Substitute their coordinates into $\\nabla f$:\n\n'
  +'$$\\begin{aligned}'+r' \\ '.join(f'\\nabla f({px},{py})&=({a})\\,i+({b})\\,j' for px,py in POINTS)+'\\end{aligned}$$\n\n'
  +'Now, draw the vectors starting at their corresponding points:\n\n![]('+paths[1]+')')
 return {'knowledge_point':{'db_id':KP_ID,'title':KP[':knowledge-point/title']},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/correct':[':answer/id',answers[1][':answer/id']],':answer-field/choices':answers}]},'generation':{'generator_version':VERSION,'template':'linear','bank_profile':'q-122699-observed','source_refs':['q-122699'],'seed':seed,'parameters':{'a':a,'b':b},'domain':'R^2','points':POINTS,'vectors':banks,'mathematical_signature':sig,'eligible_for_learning':True,'evidence_only':False,'dependencies':{'sympy':s.__version__,'matplotlib':matplotlib.__version__}}}
def main():
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--template',default='linear');args=p.parse_args()
 if args.difficulty!='easy':p.error('unsupported level; moderate and hard are unfilled')
 domain=[(a,b) for a in COEFFICIENTS for b in COEFFICIENTS if a!=b];random.Random(args.seed).shuffle(domain)
 if not 1<=args.count<=len(domain):p.error('finite limit: 30 distinct linear gradients before excluding existing tasks')
 records=[generate(args.difficulty,args.seed,args.template,{'a':a,'b':b}) for a,b in domain[:args.count]]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records))
if __name__=='__main__':main()
