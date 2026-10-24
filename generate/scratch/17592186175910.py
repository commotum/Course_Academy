#!/usr/bin/env python3
"""Parallel-line equation generator. No database writes.

Source basis 1909, two unrated incomplete sources. Local difficulty labels:
easy = read a nonzero y-intercept, radio; moderate = use a nonzero marked
x-coordinate with rational slope, RHS blank. Hard is unsupported by this package.
Source keys/solutions are mathematically derived additions, not source fidelity.
Observed complete radio bank is replayed by one explicit profile; blank has no
source answer bank. Seed/order/UUID/reference-line intercept do not imply novelty.
Plots: recurring coordinate graphs, Matplotlib; source rasters reused in replay.
CLI --difficulty easy|moderate --count N --seed N --format json|markdown.
"""
from __future__ import annotations

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186175910-source-policy.json'))
    raise SystemExit(0)

import argparse,hashlib,itertools,json,random,uuid,os,sys
from pathlib import Path
try:
 import sympy as sp
except ImportError:
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if __name__=='__main__' and runtime.exists():os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
 raise

KP_ID=17592186175910
KP_UUID='4dcbc520-40b5-5c08-ba56-be105c135240'
TITLE='Finding the Equation of a Line Passing Through a Point'
VERSION='parallel-point-1'
HERE=Path(__file__).resolve().with_suffix('')
os.environ.setdefault('MPLCONFIGDIR',str(HERE/'matplotlib-cache'))
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
TEMPLATES={'intercept_radio':{'level':'easy','kind':'radio'},'point_blank':{'level':'moderate','kind':'blank'}}
SOURCE_ASSETS={'intercept_radio':'images/86/86d6eae2f6bec9ef31d993d09aa56cbca88432678e10e3fa8b4ef72b4058077b.png','point_blank':'images/a4/a4d7c284501bcfffef9626c71e3d768e3edd6b295f4228ee576f647e8cf6d4e9.png'}
SOURCE_IDS={'intercept_radio':'q-44399','point_blank':'q-215701'}
SOURCE_PARAMETERS={'intercept_radio':{'m':'-1','c':'3','x0':0,'y0':-1},'point_blank':{'m':'1/2','c':'0','x0':-4,'y0':4}}
x=sp.Symbol('x',real=True)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def tex(v):return sp.latex(sp.sympify(v)).replace('- ','-')
def rhs(m,b):
 m=sp.Rational(m);b=sp.Rational(b)
 a=('x' if m==1 else '-x' if m==-1 else tex(m)+'x')
 return a+(' + '+tex(b) if b>0 else ' - '+tex(-b) if b<0 else '')
def fingerprint(q):
 # Coordinate point is explicit in new plots' metadata; recover it from the
 # fixed solution for database readback, including source question exclusion.
 import re
 if q.get(':question/math-academy-id')=='e-14361':return digest(['2/3',0,1])
 sol=q.get(':question/worked-solution','')
 found=re.search(r'passes through the point \$\((-?\d+),(-?\d+)\)\$',sol)
 if found:
  m=re.search(r'slope \$([^$]+)\$',sol)[1]
  m=sp.Rational(m) if '\\' not in m else (-1 if m.startswith('-') else 1)*sp.Rational(*map(int,re.findall(r'\d+',m)))
  return digest([str(m),int(found[1]),int(found[2])])
 sid=q.get(':question/math-academy-id')
 for t,s in SOURCE_IDS.items():
  if sid==s:
   p=SOURCE_PARAMETERS[t];return digest([str(sp.Rational(p['m'])),p['x0'],p['y0']])
 # Canonical e-14361 same mathematical task at (0,1), m=2/3.
 if sid=='e-14361':return digest(['2/3',0,1])
 raise ValueError('Unrecognized existing mathematical task; review before generation')
def allowed(template,p):
 m=sp.Rational(p['m']);c=sp.Rational(p['c']);x0=p['x0'];y0=p['y0'];b=y0-m*x0
 if not isinstance(x0,int) or not isinstance(y0,int) or not m or abs(m)>3 or abs(c)>8 or c==b:return False
 if not (-6<=x0<=6 and -6<=y0<=6):return False
 return x0==0 and y0!=0 if template=='intercept_radio' else x0!=0 and m.q>1

def candidates(template):
 if template=='intercept_radio':
  for m,b in itertools.product((-3,-2,-1,1,2,3),(-5,-3,-1,1,3,5)):
   yield {'m':str(m),'c':str(b+2),'x0':0,'y0':b}
 elif template=='point_blank':
  for m,x0,y0 in itertools.product(('1/2','-1/2','2/3','-2/3','3/2','-3/2'),(-6,-4,-2,2,4,6),(-5,-3,-1,1,3,5)):
   b=sp.Integer(y0)-sp.Rational(m)*x0;c=b+2
   if abs(c)<=8:yield {'m':m,'c':str(c),'x0':x0,'y0':y0}
 else:raise ValueError('Unknown template')

def render_plots(p,output_dir):
 os.environ.setdefault('MPLCONFIGDIR',str(HERE/'matplotlib-cache'))
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 import numpy as np
 d=Path(output_dir);d.mkdir(parents=True,exist_ok=True)
 name='parallel-'+digest(p)+'.png';path=d/name
 if path.exists():return str(path)
 m=float(sp.Rational(p['m']));c=float(sp.Rational(p['c']));x0=p['x0'];y0=p['y0'];b=y0-m*x0
 lim=max(8,abs(x0)+3,abs(y0)+3,abs(c)+3,abs(b)+3)
 fig,ax=plt.subplots(figsize=(4.8,4.8));fig.subplots_adjust(left=.12,bottom=.12,right=.93,top=.91)
 xx=np.linspace(-lim,lim,401)
 ax.plot(xx,m*xx+c,color='#194fd0',lw=1.8,label=r'$l_1$')
 ax.plot(xx,m*xx+b,color='#d32020',lw=1.8,label=r'$l_2$')
 ax.axhline(0,color='black',lw=1);ax.axvline(0,color='black',lw=1)
 ax.set(xlim=(-lim,lim),ylim=(-lim,lim),aspect='equal',xlabel='$x$',ylabel='$y$')
 ticks=range(-int(lim),int(lim)+1,2);ax.set_xticks(ticks);ax.set_yticks(ticks);ax.grid(alpha=.16)
 ax.plot([x0],[y0],'o',color='#d32020',ms=6)
 if x0:
  ax.plot([x0,x0],[0,y0],'--',color='gray',lw=1);ax.plot([0,x0],[y0,y0],'--',color='gray',lw=1)
 ax.annotate(f'$({x0},{y0})$',(x0,y0),xytext=(8,12),textcoords='offset points',fontsize=11,bbox={'facecolor':'white','edgecolor':'none','alpha':.9})
 ax.legend(loc='upper left',framealpha=.96);ax.set_title('Parallel lines',fontsize=12)
 fig.savefig(path,dpi=120,metadata={'Software':'Course Academy '+VERSION});plt.close(fig)
 (d/(name+'.json')).write_text(json.dumps({'parameters':p,'m':str(sp.Rational(p['m'])),'l1_intercept':str(sp.Rational(p['c'])),'l2_intercept':str(sp.Integer(y0)-sp.Rational(p['m'])*x0),'marked_point':[x0,y0],'limits':[-lim,lim],'renderer':'Matplotlib','sha256':hashlib.sha256(path.read_bytes()).hexdigest()},indent=2))
 return str(path)

def generate(level,seed=0,template=None,parameters=None,replay=False):
 if level not in ('easy','moderate'):raise ValueError('Unsupported difficulty; hard has no validated template')
 template=template or ('intercept_radio' if level=='easy' else 'point_blank')
 if TEMPLATES[template]['level']!=level:raise ValueError('Difficulty/template mismatch')
 p=dict(parameters or random.Random(seed).choice(list(candidates(template))))
 p['m']=str(sp.Rational(p['m']));p['c']=str(sp.Rational(p['c']))
 if not allowed(template,p):raise ValueError('Parameters outside validated bounds')
 m=sp.Rational(p['m']);c=sp.Rational(p['c']);x0=p['x0'];y0=p['y0'];b=sp.Integer(y0)-m*x0
 if not replay and c!=b+2:raise ValueError('Normal generation fixes reference intercept to b+2; c alone is not a new task')
 if replay and p!=SOURCE_PARAMETERS[template]:raise ValueError('Replay is only for original parameters')
 fp=digest([str(m),x0,y0]);qid=str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION+':'+fp));fid=str(uuid.uuid5(uuid.UUID(qid),'field'))
 asset=SOURCE_ASSETS[template] if replay else render_plots(p,HERE/'images')
 shown=rhs(m,c)
 # Exact source spacing in replay. No hidden equation fragment in the blank.
 if replay and template=='intercept_radio':shown='-x + 3'
 if replay and template=='point_blank':shown=r'\frac{1}{2}x'
 prompt=f'![]({asset})\n\nThe equation of the line $l_{{1}}$ is $y ={shown}$ and the line $l_{{2}}$ is parallel to $l_{{1}}$. What is the equation of $l_{{2}}$?'
 if template=='point_blank':
  if replay:prompt=prompt.replace('$y ='+shown,'$y = '+shown)
  prompt+='$y =$\n{{field-1}}'
 else:
  if not replay:prompt=prompt.replace('$y ='+shown,'$y = '+shown)
 key='selection' if template=='intercept_radio' else 'field-1';kind=TEMPLATES[template]['kind']
 values=['y ='+rhs(m,b),'y = '+rhs(-m,-b),'y ='+rhs(m,-b),'y = '+rhs(-m,0),'y ='+rhs(m,0)] if kind=='radio' else [rhs(m,b)]
 if not replay and kind=='radio':values=['y = '+v.split('=',1)[1].strip() for v in values]
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'value:'+value)),':answer/type':':answer.type/math',':answer/value':value} for value in values]
 sol=f'Since parallel lines have equal slopes, the slope of the new line should be equal to the slope of the line\n\n$$\ny = {rhs(m,c)}\n$$\n\nThe slope of the line\n\n$$\ny = {rhs(m,c)}\n$$\n\nis\n\n$$\n{tex(m)}\n$$\n\nSo, we want a line with the slope ${tex(m)}$ that passes through the point $({x0},{y0})$. Using point-slope form and simplifying, we obtain the equation of the line:\n\n$$\n\\begin{{aligned}}\ny - y_{{1}} &= m(x - x_{{1}}) \\\\\ny - ({y0}) &= {tex(m)}(x - ({x0})) \\\\\ny &= {rhs(m,-m*x0)} + ({y0}) \\\\\ny &= {rhs(m,b)}\n\\end{{aligned}}\n$$'
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/correct':[':answer/id',answers[0][':answer/id']],':answer-field/choices':answers}]},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':'observed-q-44399' if kind=='radio' else None,'source_question':SOURCE_IDS[template],'source_basis':1909,'source_lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','difficulty_origin':'authored workload classification; source unrated','solution_origin':'authored from canonical example sequence','correct_origin':'derived from inspected source graph','mathematical_fingerprint':fp,'domain':'x,y real; m nonzero finite rational','dependencies':{'sympy':sp.__version__,'matplotlib':__import__('matplotlib').__version__,'numpy':__import__('numpy').__version__},'asset':asset,'asset_local':not replay}}

def batch(level,count,seed):
 t='intercept_radio' if level=='easy' else 'point_blank' if level=='moderate' else None
 if not t:raise ValueError('Unsupported level')
 ps=list(candidates(t));random.Random(seed).shuffle(ps)
 if count<1 or count>len(ps):raise ValueError(f'Finite capacity {len(ps)}; requested {count}')
 return [generate(level,seed,t,p) for p in ps[:count]]
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+ '\n'.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186175910-source-policy.json'))

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=('json','markdown'),default='json');args=a.parse_args();r=batch(args.difficulty,args.count,args.seed);print(json.dumps(r,indent=2) if args.format=='json' else '\n\n'.join(map(markdown,r)))
