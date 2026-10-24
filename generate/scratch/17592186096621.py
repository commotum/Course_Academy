#!/usr/bin/env python3
"""Bounded source-bank quotient-rule generator; no database operations.

Easy: cos(x)/(c*x**2), source q-2385. Moderate: sin(x)/(c*x),
slope at pi, source q-48507. c is an integer 1..20, including both source
values. Choice profiles are preserved whole. Opaque moderate distractors
are observed algebraic patterns, without inferred misconception feedback.
Other templates remain source evidence, not supported generators. Hard
is an explicitly authored sum-over-sum quotient with two multi-term derivatives. A changed scale changes function and
answer; identities and task fingerprints ignore seed and choice order.
"""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186096621-source-policy.json'))
    raise SystemExit(0)

import argparse,hashlib,json,random,uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix('')
RAW=json.loads((HERE/'source.json').read_text());KP=RAW['record']
KP_ID=17592186096621;KP_UUID=KP[':knowledge-point/id']
GENERATOR_UUID=str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:question-generator:'+KP_UUID))
VERSION='quotient-source-banks-1'
SUPPORTED_LEVELS=('easy','moderate','hard')
CAPACITY={'easy':20,'moderate':20,'hard':9}
X=s.Symbol('x',real=True)
DATA={'q-2385':('easy',10),'q-48507':('moderate',2)}
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),v))
def tex(z):return s.latex(z).replace(r'\log',r'\ln')
def parts(level,c):
 if level=='hard':
  a,b=c
  return X**2+a*s.sin(X),s.exp(X)+b*s.cos(X),None
 return (s.cos(X),c*X**2,None) if level=='easy' else (s.sin(X),c*X,s.pi)
def bank(level,c):
 if level=='hard':
  u,v,_=parts(level,c);du,dv=s.diff(u,X),s.diff(v,X);n=du*v-u*dv
  return [n/v**2,(du*v+u*dv)/v**2,n/v,du/dv,n/u**2]
 if level=='easy':return [(X**2*s.sin(X)-2*s.cos(X))/(c*X**3),(X*s.sin(X)-2*s.cos(X))/(c*X**4),(s.sin(X)-s.cos(X))/(c*X**3),(-X*s.sin(X)-2*s.cos(X))/(c*X**3),(s.sin(X)-2*s.cos(X))/(c*X**3)]
 return [1/(2*s.Integer(c)*s.pi),-s.pi,c*s.pi,-1/s.Integer(c),-1/(c*s.pi)]
def generate(level,seed=0,template=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty; see capabilities.json')
 template=template or ('authored-hard-sums' if level=='hard' else 'q-2385' if level=='easy' else 'q-48507')
 r=random.Random(seed)
 if level=='hard':
  if template!='authored-hard-sums' or profile not in (None,'authored-quotient-operations'):raise ValueError('Hard requires authored complete operation bank')
  p=parameters or {'a':r.randint(1,3),'b':r.randint(1,3)}
  if set(p)!={'a','b'} or any(isinstance(z,bool) or int(z)!=z or not 1<=int(z)<=3 for z in p.values()):raise ValueError('Hard a,b are integers 1..3')
  c=(int(p['a']),int(p['b']));profile='authored-quotient-operations'
 else:
  if template not in DATA or DATA[template][0]!=level:raise ValueError('Unsupported template/level')
  if profile not in (None,'observed'):raise ValueError('Only complete observed profiles supported')
  p=parameters or {'c':r.randint(1,20)}
  if set(p)!={'c'} or isinstance(p['c'],bool) or int(p['c'])!=p['c'] or not 1<=int(p['c'])<=20:raise ValueError('Integer scale c in 1..20 required')
  c=int(p['c']);profile='observed'
 u,v,t=parts(level,c);du,dv=s.diff(u,X),s.diff(v,X);der=s.factor((du*v-u*dv)/v**2)
 if level=='hard':
  a,b=c
  der=(s.exp(X)*(2*X-X**2+a*(s.cos(X)-s.sin(X)))+b*(2*X*s.cos(X)+X**2*s.sin(X)+a))/v**2
 correct=der if t is None else s.simplify(der.subs(X,t));vals=bank(level,c)
 equal=lambda a,b:s.trigsimp(s.expand(s.together(a-b).as_numer_denom()[0]))==0
 assert sum(equal(z,correct) for z in vals)==1
 assert all(not equal(a,b) for i,a in enumerate(vals) for b in vals[:i])
 prompt=('If $f(x)=\\frac{\\cos x}{'+str(c)+r'x^{2}}$, find $f^{\prime}(x)$.' if level=='easy' else 'If a curve $C$ is given by $y=\\frac{\\sin x}{'+str(c)+r'x}$, calculate the slope of the tangent line to the curve at the point where $x=\pi$.')
 if level=='hard':prompt='If $f(x)=\\frac{'+tex(u)+'}{'+tex(v)+r'}$, find $f^{\prime}(x)$ wherever the denominator is nonzero.'
 worked='In this case, the expression for $'+('y' if level=='moderate' else 'f(x)')+'$ is a quotient $\\frac{u(x)}{v(x)}$ with $u(x)='+tex(u)+'$ and $v(x)='+tex(v)+'.$\n\nTherefore, we apply the quotient rule as follows:\n\n'
 rows=[r'\frac{u^{\prime}(x)\cdot v(x)-u(x)\cdot v^{\prime}(x)}{[v(x)]^{2}}',r'\frac{('+tex(u)+r')^{\prime}\cdot ('+tex(v)+')-('+tex(u)+r')\cdot ('+tex(v)+r')^{\prime}}{('+tex(v)+r')^{2}}',r'\frac{('+tex(du)+r')\cdot ('+tex(v)+')-('+tex(u)+r')\cdot ('+tex(dv)+r')}{('+tex(v)+r')^{2}}',tex(der)]
 if level=='easy':
  rows=[rows[0],rows[2],r'\frac{'+tex(s.expand(du*v-u*dv))+r'}{'+tex(v**2)+'}',r'\frac{'+tex(s.factor(du*v-u*dv))+r'}{'+tex(v**2)+'}',tex(der)]
 elif level=='moderate':
  rows=rows[:3]+[r'\frac{'+tex(s.factor(du*v-u*dv))+r'}{'+tex(v**2)+'}',tex(der)]
 worked+='$$\n'+r'\begin{aligned}f^{\prime}(x)&='+r'\\ &='.join(rows)+r'\end{aligned}'+'\n$$'
 if level=='moderate':
  worked+='\n\nTo find the slope of the tangent line, we now substitute $x=\\pi$ into the formula and get\n\n$$\n'+r'\begin{aligned}f^{\prime}(\pi)&=\frac{\pi\cos(\pi)-\sin(\pi)}{'+str(c)+r'\pi^{2}}\\ &=\frac{\pi(-1)-0}{'+str(c)+r'\pi^{2}}\\ &='+tex(correct)+r'.\end{aligned}'+'\n$$\n\nTherefore, the slope of the tangent line is $'+tex(correct)+'.$'
 task=sha([s.srepr(u/v),str(t)])
 content=sha([prompt,worked,sorted(tex(z) for z in vals),'radio','selection'])
 qid=uid('question:'+task);fid=uid('field:'+task+':selection')
 choices=[{':answer/id':uid('answer:'+fid+':'+s.srepr(z)),':answer/type':':answer.type/math',':answer/value':tex(z)} for z in vals]
 cid=next(a[':answer/id'] for a,z in zip(choices,vals) if equal(z,correct))
 r.shuffle(choices)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',cid]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':KP[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'mathematical_fingerprint':task,'content_fingerprint':content,'source_ids':[template] if level!='hard' else ['q-47943','q-47998','e-3638'],'authored_difficulty':level=='hard','source_basis':RAW['basis'],'source_lineage':RAW['lineage'],'domain':'x != 0' if level!='hard' else 'exp(x)+b*cos(x) != 0','plot_rating':'none','sympy_version':s.__version__}}
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def fingerprint(q):
 import sys
 sys.path.insert(0,str(HERE));from math_parser import scalar
 prompt=q[':question/problem']
 if q.get(':question/math-academy-id') in ('q-167328','q-167782'):
  function=-s.exp(X)/(8*s.sin(X));point=None
 else:
  start=prompt.index('=')+1;end=prompt.index('$',start)
  function=scalar(prompt[start:end].strip().rstrip(','));point=None
  if 'slope of the tangent' in prompt:
   start=prompt.rindex('$x=')+3;end=prompt.index('$',start);point=scalar(prompt[start:end])
 return sha([s.srepr(function),str(point)])

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186096621-source-policy.json'))

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 levels=SUPPORTED_LEVELS if a.difficulty=='all' else (a.difficulty,)
 if any(level not in SUPPORTED_LEVELS for level in levels):ap.error('Unsupported difficulty')
 if not 1<=a.count<=min(CAPACITY[level] for level in levels):ap.error('Finite limit: 20 easy, 20 moderate, 9 hard distinct tasks')
 records=[]
 for level in levels:
  parameters=([{'a':a,'b':b} for a in range(1,4) for b in range(1,4)] if level=='hard' else [{'c':c} for c in range(1,21)]);random.Random(a.seed).shuffle(parameters)
  records.extend(generate(level,a.seed+i,a.template,p,a.profile) for i,p in enumerate(parameters[:a.count]))
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(rec['question'][':question/problem']+'\n\n'+'\n'.join('$'+ch[':answer/value']+'$' for ch in rec['question'][':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+rec['question'][':question/worked-solution'] for rec in records))
