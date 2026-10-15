#!/usr/bin/env python3
"""Oriented open-curve flux: bounded positive whole-field scaling.

Preserve each observed curve, limits, right normal and five-option profile.
Qualitative vector plots have no magnitude key: positive common scaling leaves
all normalized vectors unchanged. Never sample zero/negative scales with them.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
HERE=Path(__file__).with_suffix('')
SNAPSHOT=json.loads((HERE/'source.json').read_text())
KP_ID=17592186179746
NAMESPACE=uuid.UUID(SNAPSHOT['record'][':knowledge-point/id'])
GENERATOR_UUID=str(uuid.uuid5(NAMESPACE,'question-generator'))
VERSION='1.0.0'
SUPPORTED_LEVELS=('moderate','hard')
SCALES=tuple(range(2,10))
x,y,t=s.symbols('x y t',real=True)
# P,Q,x(t),y(t),lower,upper,level. Every right normal is (y',-x')/|r'|.
DATA={
'q-126940':(x,y,t,t**2,0,1,'moderate'),
'q-127151':(4*y,2*x-1,t**2,t,0,1,'moderate'),
'q-127153':(x,y**2,1/t,t,s.Rational(1,2),2,'moderate'),
'q-127223':(s.Integer(4),s.Integer(2),t/2,1/(2*t),s.Rational(1,2),2,'moderate'),
'q-127227':(5*s.exp(-x),s.Integer(4),s.log(t),t,1,s.E,'moderate'),
'q-127233':(3*x*y,2*x+1,t,t,0,1,'moderate'),
'q-126943':(s.Integer(2),s.Integer(-4),t**2/4,t,0,2,'hard'),
'q-127244':(-3*x**2,s.Integer(1),t,t**3,0,1,'hard'),
'q-127253':(s.Integer(1),s.Integer(1),t,1-t,0,1,'hard'),
'q-127254':(s.Integer(0),2*y**2,-s.log(t),t,1/s.E,1,'hard'),
'q-127256':(y**2,1/x,s.exp(t),t,0,1,'hard'),
'q-127235':(x**2*y,-y,t,1/t,s.Rational(1,2),2,'hard'),
}
SOURCES={q[':question/math-academy-id']:q for q in SNAPSHOT['record'][':knowledge-point/questions']}
EXCLUDED={'q-169206':'Standalone prompt and inspected diagram omit the definition of F; worked solution implies F=(3xy^2,-y^3). Do not supply hidden solution data to learners or silently repair source.'}
ORIGINAL={k:{'scale':1} for k in DATA}

def parse(value):
 value=value.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace('⁡','')
 value=re.sub(r'\\operatorname\{ln\}(\d+)',r'log(\1)',value)
 value=re.sub(r'\\log\{\(\s*(.*?)\s*\)\}',r'log(\1)',value)
 def group(z,i):
  assert z[i]=='{';depth=1;j=i+1
  while depth:
   if z[j]=='{':depth+=1
   if z[j]=='}':depth-=1
   j+=1
  return z[i+1:j-1],j
 while r'\frac' in value:
  i=value.index(r'\frac');a,j=group(value,i+5);b,k=group(value,j)
  value=value[:i]+'(('+a+')/('+b+'))'+value[k:]
 value=value.replace('{','(').replace('}',')')
 return parse_expr(value,local_dict={'x':x,'y':y,'t':t,'e':s.E,'E':s.E,'log':s.log},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))

def tex(z):return s.latex(s.expand(z))
def mathematics(template,scale):
 p,q,a,b,lo,hi,level=DATA[template];p,q=scale*p,scale*q
 u=s.simplify(p.subs({x:a,y:b},simultaneous=True));v=s.simplify(q.subs({x:a,y:b},simultaneous=True))
 da,db=s.diff(a,t),s.diff(b,t);integrand=s.simplify(u*db-v*da)
 anti=s.integrate(integrand,t);answer=s.simplify(anti.subs(t,hi)-anti.subs(t,lo))
 return p,q,a,b,lo,hi,u,v,da,db,integrand,anti,answer

def signature(template,scale):
 p,q,a,b,lo,hi,*_=mathematics(template,scale)
 return json.dumps([s.srepr(s.expand(z)) for z in (p,q,a,b,s.sympify(lo),s.sympify(hi))])

def render(template,scale):
 source=SOURCES[template]
 if scale==1:return source[':question/problem'],source[':question/worked-solution']
 p,q,a,b,lo,hi,u,v,da,db,z,anti,answer=mathematics(template,scale)
 prompt=source[':question/problem'];start=prompt.index('F(x,y)=')+len('F(x,y)=');end=prompt.index('$',start)
 prompt=prompt[:start]+'('+tex(p)+r')\,i+('+tex(q)+r')\,j'+prompt[end:]
 original=source[':question/worked-solution']
 # Preserve the complete source formula, clockwise-normal condition,
 # parameterization/endpoint verification and orientation illustration.
 prefix=original[:original.index('Therefore,\n\n$$\n\\begin{aligned}P(x,y)')]
 solution=prefix+'Therefore,\n\n$$\n'+r'\begin{aligned}P(x,y)&='+tex(p)+'='+tex(u)+r', \\ Q(x,y)&='+tex(q)+'='+tex(v)+r'.\end{aligned}'+'\n$$\n\n'
 solution+='Computing the derivatives of $x(t)$ and $y(t)$ along the curve, we get\n\n$$\n'+r'\begin{aligned}\frac{\mathrm{d}x}{\mathrm{d}t}&=\frac{\mathrm{d}}{\mathrm{d}t}('+tex(a)+')='+tex(da)+r', \\ \frac{\mathrm{d}y}{\mathrm{d}t}&=\frac{\mathrm{d}}{\mathrm{d}t}('+tex(b)+')='+tex(db)+r'.\end{aligned}'+'\n$$\n\n'
 solution+='Finally, we evaluate the integral as follows:\n\n$$\n'+r'\begin{aligned}\int_C F\cdot n\,\mathrm{d}s&=\int_C P\,\mathrm{d}y-Q\,\mathrm{d}x \\ &=\int_{'+tex(s.sympify(lo))+'}^{'+tex(s.sympify(hi))+r'}\left(P\frac{\mathrm{d}y}{\mathrm{d}t}-Q\frac{\mathrm{d}x}{\mathrm{d}t}\right)\mathrm{d}t \\ &=\int_{'+tex(s.sympify(lo))+'}^{'+tex(s.sympify(hi))+'}\\left[('+tex(u)+')('+tex(db)+')-('+tex(v)+')('+tex(da)+r')\right]\mathrm{d}t \\ &=\int_{'+tex(s.sympify(lo))+'}^{'+tex(s.sympify(hi))+'}('+tex(z)+r')\,\mathrm{d}t \\ &=\left['+tex(anti)+r'\right]_{'+tex(s.sympify(lo))+'}^{'+tex(s.sympify(hi))+r'} \\ &=('+tex(anti.subs(t,hi))+')-('+tex(anti.subs(t,lo))+r') \\ &='+tex(answer)+r'.\end{aligned}'+'\n$$'
 return prompt,solution

def generate(difficulty,seed=0,template=None,parameters=None,profile=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 rng=random.Random(seed);eligible=[k for k,d in DATA.items() if d[-1]==difficulty];template=template or rng.choice(eligible)
 assert template in eligible
 scale=parameters['scale'] if parameters else rng.choice(SCALES)
 assert type(scale) is int and (scale in SCALES or scale==1)
 assert profile is None or profile=='observed-scaled:'+template
 src=SOURCES[template];sf=src[':question/answer-fields'][0];answer=mathematics(template,scale)[-1]
 qid=str(uuid.uuid5(NAMESPACE,'v'+VERSION+':'+signature(template,scale)));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 choices=[];correct=None
 for old in sf[':answer-field/choices']:
  expr=s.expand(scale*parse(old[':answer/value']));aid=str(uuid.uuid5(uuid.UUID(fid),s.srepr(expr)))
  choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':old[':answer/value'] if scale==1 else tex(expr)})
  if s.simplify(expr-answer)==0:assert correct is None;correct=aid
 assert correct
 prompt,solution=render(template,scale)
 question={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':str(NAMESPACE),'title':SNAPSHOT['record'][':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':template,'profile':'observed-scaled:'+template,'parameters':{'scale':scale},'source_question_id':src[':db/id'],'source_basis':SNAPSHOT['basis'],'domain':list(SCALES),'mathematical_signature':signature(template,scale),'dependencies':{'sympy':s.__version__}}}

def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');args=ap.parse_args()
 if args.difficulty not in SUPPORTED_LEVELS:ap.error('unsupported level: '+args.difficulty)
 candidates=[(k,scale) for k,d in DATA.items() if d[-1]==args.difficulty for scale in SCALES];random.Random(args.seed).shuffle(candidates)
 if not 0<args.count<=len(candidates):ap.error('finite capability: '+str(len(candidates)))
 records=[generate(args.difficulty,args.seed,k,{'scale':scale}) for k,scale in candidates[:args.count]]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
