#!/usr/bin/env python3
"""Piecewise line integrals: bounded whole-field scaling of observed families.

Geometry, requested integral and known segment retain their instructional roles.
Scale the entire vector field, supplied integral and complete observed answer bank
by one nonzero integer. This is a conservative same-method extension; it does
not assert a psychological interpretation of the source distractor expressions.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import sys
import uuid
import sympy as s

HERE=Path(__file__).with_suffix('')
SNAPSHOT=json.loads((HERE/'source.json').read_text())
KP_ID=17592186179669
NAMESPACE=uuid.UUID(SNAPSHOT['record'][':knowledge-point/id'])
GENERATOR_UUID=str(uuid.uuid5(NAMESPACE,'piecewise-integral-generator-v1'))
VERSION='1.0.0'
SUPPORTED_LEVELS=('moderate','hard')
SCALES=tuple(range(-8,0))+tuple(range(2,9))
x,y,t=s.symbols('x y t',real=True)
# Each row: field components, oriented parametrizations + bounds, known segment,
# complete observed bank as exact expressions, correct answer and source workload.
DATA={
'q-39342':(x+y,x-y,(2*t,0,0,1),(2-t,t,0,1),1,['2','1','3','4','6'],'1','moderate'),
'q-39674':(x,y,(t,t**2,0,2),(2-2*t,4,0,1),2,['-2','8','0','2','10'],'8','hard'),
'q-39673':(2*x-3*y,x+y,(t,1+t,0,1),(1,2+t,0,1),2,['E-2','-3/2','2+log(3)','2','7/2'],'2','moderate'),
'q-77180':(2*x+y,x-2*y,(1,-1+2*t,0,1),(1-t,1-t,0,1),1,['1','-4','5','-1','3'],'1','moderate'),
'q-77182':(x**2+y,x-y**2,(t,0,0,1),(1-t,-2*t,0,1),2,['8/3','8/5','5/2','2','5'],'8/3','moderate'),
'q-77185':(x-y,y-x,(-2+t,2,0,1),(-1,2-2*t,0,1),1,['1/2','4','-3/2','-15/2','-6'],'-15/2','moderate'),
'q-77191':(x-2*y,y-x,(-2+2*t,t,0,1),(t,1,0,1),2,['-4','5','-3/2','3/2','4'],'-4','moderate'),
'q-77250':(x,0,(t,0,0,2),(t,4-t**2,2,0),1,['-2','2','-4','0','3'],'0','hard'),
'q-77244':(x*y,y,(t,8,0,-2),(t,-t**3,-2,0),1,['-51/5','-112/5','32/5','-23/5','8/5'],'-112/5','hard'),
'q-77258':(x,y**2,(t,-s.sqrt(t),0,4),(4,-2+2*t,0,1),2,['32','8','5','4','16'],'8','hard'),
}
SOURCES={q[':question/math-academy-id']:q for q in SNAPSHOT['record'][':knowledge-point/questions']}
ORIGINAL={k:{'scale':1} for k in SOURCES}

def exact(z):return s.sympify(z)
def tex(z):return s.latex(s.expand(exact(z)))
def integral(p,q,curve):
 a,b,lo,hi=map(exact,curve)
 u=s.expand(p.subs({x:a,y:b},simultaneous=True));v=s.expand(q.subs({x:a,y:b},simultaneous=True))
 dot=s.expand(u*s.diff(a,t)+v*s.diff(b,t))
 return s.integrate(dot,(t,lo,hi)),(a,b,lo,hi,u,v,dot)

def mathematical(template,scale):
 p,q,c1,c2,known,bank,correct,level=DATA[template]
 p,q=scale*exact(p),scale*exact(q)
 i1,z1=integral(p,q,c1);i2,z2=integral(p,q,c2)
 return {'p':p,'q':q,'i1':i1,'i2':i2,'total':s.simplify(i1+i2),'known':known,'curve':z2 if known==1 else z1,'bank':[scale*exact(v) for v in bank],'level':level}

def field_tex(p,q):
 if q==0:return tex(p)+r'\,i'
 return '('+tex(p)+r')\,i+('+tex(q)+r')\,j'

def generated_prompt(template,m):
 prompt=SOURCES[template][':question/problem']
 # Update the supplied integral and complete field, preserving source geometry,
 # target integral, diagram and structural paragraph layout.
 given=m['i1'] if m['known']==1 else m['i2']
 prompt=re.sub(r'(Given that .*?=)(.*?)(,?\$)',lambda z:z[1]+tex(given)+z[3],prompt,count=1)
 start=prompt.index('F(x,y)=')+len('F(x,y)=');end=prompt.index('$',start)
 tail=',' if prompt[start:end].endswith(',') else ''
 return prompt[:start]+field_tex(m['p'],m['q'])+tail+prompt[end:]

def generated_solution(template,m):
 unknown=3-m['known'];given=m['i1'] if m['known']==1 else m['i2'];value=m['i2'] if unknown==2 else m['i1']
 a,b,lo,hi,u,v,dot=m['curve'];da=s.diff(a,t);db=s.diff(b,t);anti=s.integrate(dot,t)
 # Operative source stages: additivity, identify missing piece, parametrization,
 # substituted field, derivative, dot product, evaluation, sum.
 if template=='q-77250':
  # Preserve the source's explicit reversal stage and forward parametrization.
  lo,hi=hi,lo
  text=solution_stages(template,m,unknown,given,-value,a,b,lo,hi,u,v,dot,da,db,anti)
  text=text.replace('The path $C_2$ can be parametrized as','Let $-C_2$ be the same path travelled from $B$ to $A$. The path $-C_2$ can be parametrized as')
  text=text.replace(r'\int_{C_2}F\cdot\mathrm{d}r=\int_',r'\int_{-C_2}F\cdot\mathrm{d}r=\int_')
  anchor=f'$$\\int_C F\\cdot\\mathrm{{d}}r='
  index=text.rindex(anchor)
  text=text[:index]+f'$$\\int_C F\\cdot\\mathrm{{d}}r=\\int_{{C_1}}F\\cdot\\mathrm{{d}}r-\\int_{{-C_2}}F\\cdot\\mathrm{{d}}r=({tex(given)})-({tex(-value)})={tex(m["total"])}.$$'
  return text
 return solution_stages(template,m,unknown,given,value,a,b,lo,hi,u,v,dot,da,db,anti)

def solution_stages(template,m,j,given,value,a,b,lo,hi,u,v,dot,da,db,anti):
 # Descending limits express traversal in the specified orientation.
 return ("We will use the fact that\n\n$$\\int_C F\\cdot\\mathrm{d}r=\\int_{C_1}F\\cdot\\mathrm{d}r+\\int_{C_2}F\\cdot\\mathrm{d}r.$$\n\n"
 +f"We're given the value of the {'first' if m['known']==1 else 'second'} integral, so we only need to work out the {'second' if j==2 else 'first'}.\n\n"
 +f"The path $C_{j}$ can be parametrized as\n\n$$r_{j}(t)=({tex(a)})\\,i+({tex(b)})\\,j,$$\n\n"
 +f"with $t$ running from ${tex(lo)}$ to ${tex(hi)}$. Along this path, $x={tex(a)}$ and $y={tex(b)}$. Therefore,\n\n"
 +f"$$F(r_{j}(t))=({tex(u)})\\,i+({tex(v)})\\,j.$$\n\nComputing the derivative, we get\n\n"
 +f"$$r_{j}'(t)=({tex(da)})\\,i+({tex(db)})\\,j.$$\n\nWe can now compute the dot product:\n\n"
 +f"$$F(r_{j}(t))\\cdot r_{j}'(t)=({tex(u)})({tex(da)})+({tex(v)})({tex(db)})={tex(dot)}.$$\n\n"
 +f"Finally, we can evaluate the integral, as follows:\n\n$$\\int_{{C_{j}}}F\\cdot\\mathrm{{d}}r=\\int_{{{tex(lo)}}}^{{{tex(hi)}}}({tex(dot)})\\,\\mathrm{{d}}t=\\left[{tex(anti)}\\right]_{{{tex(lo)}}}^{{{tex(hi)}}}={tex(value)}.$$\n\n"
 +f"$$\\int_C F\\cdot\\mathrm{{d}}r=({tex(m['i1'])})+({tex(m['i2'])})={tex(m['total'])}.$$")

def generate(difficulty,seed=0,template=None,parameters=None,profile=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 rng=random.Random(seed);eligible=[k for k,v in DATA.items() if v[-1]==difficulty]
 template=template or rng.choice(eligible)
 assert template in eligible
 scale=parameters['scale'] if parameters else rng.choice(SCALES)
 assert isinstance(scale,int) and (scale in SCALES or scale==1)
 m=mathematical(template,scale);source=SOURCES[template]
 qid=str(uuid.uuid5(NAMESPACE,f'v{VERSION}:{template}:scale={scale}'));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 choices=[];correct_id=None;sf=source[':question/answer-fields'][0]
 for expr,old in zip(m['bank'],sf[':answer-field/choices']):
  # Retain source notation exactly on replay; normal output is canonical TeX.
  value=old[':answer/value'] if scale==1 else tex(expr)
  aid=str(uuid.uuid5(uuid.UUID(fid),'value:'+s.srepr(expr)))
  choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
  if s.simplify(expr-m['total'])==0:correct_id=aid
 assert correct_id and len({s.srepr(z) for z in m['bank']})==len(m['bank'])
 question={':question/id':qid,':question/problem':source[':question/problem'] if scale==1 else generated_prompt(template,m),':question/worked-solution':source[':question/worked-solution'] if scale==1 else generated_solution(template,m),':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct_id]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':str(NAMESPACE),'title':SNAPSHOT['record'].get(':knowledge-point/title','Piecewise line integrals')},'question':question,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':template,'profile':'observed-scaled:'+template,'parameters':{'scale':scale},'source_question_id':source[':db/id'],'source_basis':SNAPSHOT['basis'],'domain':list(SCALES),'mathematical_signature':template+':'+str(scale),'dependencies':{'sympy':s.__version__}}}

def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=SUPPORTED_LEVELS,required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');args=ap.parse_args()
 candidates=[(k,scale) for k,d in DATA.items() if d[-1]==args.difficulty for scale in SCALES];random.Random(args.seed).shuffle(candidates)
 if not 0<args.count<=len(candidates):ap.error(f'finite capability: {len(candidates)} distinct variants at this level')
 records=[generate(args.difficulty,args.seed,k,{'scale':scale}) for k,scale in candidates[:args.count]]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
