#!/usr/bin/env python3
"""Source-bounded Green conversion generator. Pure generation, no database writes.
Moderate: q-108467 triangle, differential form. Hard: q-109263 parabola/line,
vector form. Conservative coefficient slots a=1..12; fixed source geometry is
an explicit narrower sampling policy (not an essential mathematical restriction).
"""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186133884-source-policy.json'))
    raise SystemExit(0)

import argparse,json,os,random,sys,uuid
from pathlib import Path
try:
 import sympy as sp
except ModuleNotFoundError:
 interpreter=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if __name__=='__main__' and interpreter.exists():os.execv(str(interpreter),[str(interpreter),str(Path(__file__).resolve()),*sys.argv[1:]])
 raise
KP_ID=17592186133884
KP_UUID='48652211-e469-55b9-96cb-2526a4135d34'
TITLE="Expressing a Line Integral as a Repeated Integral Using Green's Theorem"
VERSION='greens-conversion-v1'
DOMAIN=list(range(1,13))
LEVEL_DOMAINS={'moderate':DOMAIN,'hard':list(range(2,13))}
x,y=sp.symbols('x y',real=True)
IMAGES={'moderate':'images/2e/2e63a57e50b60d7f0c6a3ce12d164716e2cba71c6bd4c6df10460a35beba4209.png','hard':'images/e3/e32b8e7d6ce80d7cedad928f9a2f7acc3c3d7f06add7909e856db27d154068d6.png'}
SOURCES={'moderate':'q-108467','hard':'q-109263'}
TEMPLATES={'moderate':'triangle-polynomial','hard':'parabola-vector'}
THEOREM=("Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D$, then Green's theorem states that\n\n$$\n"+r'\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.'+'\n$$')
def tex(v):return sp.latex(sp.sympify(v)).replace(r'\log',r'\ln')
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION+':'+v))
def repeated(integrand,lo,hi,low,high,inner=y,outer=x):
 return r'\int_{'+tex(lo)+'}^{'+tex(hi)+r'}\int_{'+tex(low)+'}^{'+tex(high)+'}'+tex(integrand)+r'\,\mathrm{d}'+str(inner)+r'\,\mathrm{d}'+str(outer)
def mathematics(level,a):
 if level not in SOURCES:raise ValueError('Unsupported level; easy has no source progression')
 if type(a)is not int or a not in DOMAIN:raise ValueError('a must be an integer 1..12')
 if level=='moderate':
  P,Q=a*x*y**2,2*a*x**2*y
  specs=[(2*a*x*y,0,1,0,2*x),(a*x**2*y,0,1,0,2*x),(a*x**2*y**2,0,2,0,2*x),(a*x*y**2,0,1,0,2*x),(2*a*x,0,2,0,x)]
 else:
  P,Q=sp.log(2+x)-a*y**2,x**2+y**2
  specs=[(2*(x+a*y),-1,2,x**2,x+2),(2*(x+a*y),-1,2,x+2,x**2+x+2),(2*(x+a*y),0,2,-x**2,x+2),(2*(x-a*y),0,2,x**2,x+2),(2*a*y-x,-1,2,x**2,x+2)]
 return P,Q,specs

def generate(difficulty='moderate',seed=0,parameters=None,**kwargs):
 if difficulty not in SOURCES:raise ValueError('Unsupported difficulty')
 if kwargs.get('template',TEMPLATES[difficulty])!=TEMPLATES[difficulty]:raise ValueError('Unsupported template')
 if parameters is None:a=random.Random(seed).choice(LEVEL_DOMAINS[difficulty])
 else:
  if set(parameters)!={'a'}:raise ValueError('Expected a parameter')
  a=parameters['a']
 if a not in LEVEL_DOMAINS[difficulty] and not (kwargs.get('source_replay') and difficulty=='hard' and a==1):raise ValueError('Parameter excluded: source hard a=1 has duplicate-valued distractors')
 P,Q,specs=mathematics(difficulty,a);py,qx=sp.diff(P,y),sp.diff(Q,x);curl=sp.simplify(qx-py)
 assert sp.simplify(curl-specs[0][0])==0
 key=difficulty+':'+str(a);qid,fid=uid('q:'+key),uid('f:'+key)
 choices=[{':answer/id':uid(fid+':'+str(tuple(map(sp.srepr,spec)))),':answer/type':':answer.type/math',':answer/value':repeated(*spec)} for spec in specs]
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[0][':answer/id']]}
 integral=r'\oint_C\left('+tex(P)+r'\right)\,dx+\left('+tex(Q)+r'\right)\,dy'
 if difficulty=='moderate':
  prompt='Consider the triangle $C$ in the plane with vertices $(0,0),(1,0)$ and $(1,2),$ traversed counterclockwise, and the region $D$ bounded by $C.$ Express $'+integral+'$ as a repeated integral.'
  rewrite='';region=r'D=\{(x,y):0\le x\le1,\,0\le y\le2x\}.'
 else:
  prompt='Consider the closed curve $C,$ which is the boundary of the region enclosed by the curves $y=x^2$ and $y=x+2,$ traversed counterclockwise. Express $'+r'\oint_C F\cdot dr,$ where $F(x,y)=\langle '+tex(P)+','+tex(Q)+r'\rangle,$ as a repeated integral.'
  rewrite='First, notice that we can rewrite our integral as follows:\n\n$$\n'+r'\oint_C F\cdot dr='+integral+'\n$$\n\n'
  region=r'D=\{(x,y):-1\le x\le2,\,x^2\le y\le x+2\}.'
 solution=(THEOREM+'\n\nThe region $D$ and the curve $C$ for this case are shown below.\n\n![]('+IMAGES[difficulty]+')\n\n'+rewrite+
  'We have that $P(x,y)='+tex(P)+'$ and $Q(x,y)='+tex(Q)+'.$ Therefore,\n\n$$\n'+r'\begin{aligned}\frac{\partial P}{\partial y}&='+tex(py)+r',\\\frac{\partial Q}{\partial x}&='+tex(qx)+r'.\end{aligned}'+'\n$$\n\nWe can express the region $D$ as a type I region as follows:\n\n$$\n'+region+"\n$$\n\nTherefore, applying Green's theorem, we get\n\n$$\n"+
  r'\begin{aligned}'+integral+r'&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA\\'+r'&=\iint_D\left(('+tex(qx)+')-('+tex(py)+r')\right)\,dA\\'+r'&=\iint_D '+tex(curl)+r'\,dA\\'+'&='+choices[0][':answer/value']+r'.\end{aligned}'+'\n$$')
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[field]},'generation':{'version':VERSION,'template':TEMPLATES[difficulty],'bank_profile':SOURCES[difficulty]+'-complete','seed':seed,'parameters':{'a':a},'domain':'integer a in '+('1..12' if difficulty=='moderate' else '2..12')+'; fixed source geometry','source_replay_only':bool(kwargs.get('source_replay')),'source_ids':[SOURCES[difficulty]],'source_basis':2677,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','assets':[IMAGES[difficulty]],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}
def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186133884-source-policy.json'))

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',default='moderate',choices=['easy','moderate','hard']);p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',default='json',choices=['json','markdown']);args=p.parse_args()
 if args.difficulty not in SOURCES:p.error('easy unsupported: no source progression')
 if not 1<=args.count<=len(LEVEL_DOMAINS[args.difficulty]):p.error('finite domain: count must be 1..12')
 recs=[generate(args.difficulty,args.seed,{'a':a}) for a in random.Random(args.seed).sample(LEVEL_DOMAINS[args.difficulty],args.count)]
 print(json.dumps(recs,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,recs)))
