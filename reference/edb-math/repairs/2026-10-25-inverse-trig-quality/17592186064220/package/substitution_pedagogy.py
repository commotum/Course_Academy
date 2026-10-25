"""Scaffolded inverse-trig and exponential substitution task contracts.

Difficulty changes the target decision, not the amount of prerequisite recall.
No imported difficulty labels are claimed for these authored scaffolded tasks.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import uuid
import sympy as s
import inverse_substitution_models as inverse_models
from integration_answer_bank import answer_bank

X,U=s.symbols('x u',real=True)
VERSION='substitution-recognition-3'
INV={17592186064218:'sine',17592186064219:'tangent',17592186064250:'secant',17592186064220:'definite'}
EXP=(17592186184349,17592186184350,17592186184351,17592186184352)
CASES={k:{b:('sine','tangent')if v=='definite'else(v,) for b in('easy','moderate','hard')}for k,v in INV.items()}
for k in EXP[:2]:CASES[k]={b:('square','cube')for b in('easy','moderate','hard')}
CASES[EXP[2]]={'easy':('power_e','power_base'),'moderate':('sqrt_e','root_e','sqrt_base','root_base','log_e','log_base'),'hard':('log_composite',)}
CASES[EXP[3]]={'easy':('square_e','linear_e'),'moderate':('square_base','linear_base'),'hard':('log_e',)}

def tex(z):
 return s.latex(s.sympify(z)).replace(r'\log',r'\ln').replace(r'\operatorname{asin}',r'\arcsin').replace(r'\operatorname{atan}',r'\arctan').replace(r'\operatorname{asec}',r'\operatorname{arcsec}')
def integral(body,var='x',lo=None,hi=None):
 return r'\int'+(''if lo is None else '_{'+tex(lo)+'}^{'+tex(hi)+'}')+' '+body+r'\,\mathrm{d}'+var
def times(c,z):
 return z if c==1 else tex(c)+r'\left('+z+r'\right)'
def block(z):return '$$\n'+z+'\n$$'
def fp(body,lo=None,hi=None):
 return hashlib.sha256(json.dumps([s.srepr(s.simplify(body)),None if lo is None else s.srepr(s.simplify(lo)),None if hi is None else s.srepr(s.simplify(hi))]).encode()).hexdigest()
def inverse(fn,z):return getattr(s,{'sine':'asin','tangent':'atan','secant':'asec'}[fn])(z)

def instance(kp,band,case,rng,profile=0):
 if kp in INV:return inverse_models.instance(kp,band,case,rng,profile)
 a=s.Integer(rng.randint(2,5));n=s.Integer(rng.randint(1,4));lo=hi=None;notes=[];facts=[]
 base=s.E if kp==EXP[0]or case.endswith('_e')or case=='log_composite'else s.Integer(rng.choice((2,3,5)))
 if kp in EXP[:2]:
  power=2 if case=='square'else 3
  slope=s.Integer(1 if band=='easy'else rng.choice((1,2)))
  if band=='hard':slope=-slope
  shift=s.Integer(rng.randint(0,3));inner=slope*X**power+shift;du=s.diff(inner,X)
  body=n*X**(power-1)*base**inner;factor=n/(slope*power);trans=base**U
  prim=base**U if base==s.E else base**U/s.log(base)
  challenge='provided_substitution'if band=='easy'else 'positive_power_inner'if band=='moderate'else 'negative_inner_derivative'
  params={'power':power,'slope':str(slope),'shift':str(shift),'amplitude':str(n),'base':str(base)}
 elif kp==EXP[2]:
  c=s.Integer(rng.randint(1,4));slope=s.Integer(rng.choice((1,2)))if base==s.E else s.Integer(1)
  inner=base**(slope*X)+c;du=s.diff(inner,X)
  role=case.split('_')[0]
  if role=='log':
   if case=='log_composite':
    b=s.Integer(rng.choice((-2,-1,1,2)));inner=s.exp(slope*X)+b*X+c;du=s.diff(inner,X)
   trans=1/U;prim=s.log(U)
  elif role=='power':
   power=rng.choice((2,3));trans=U**power;prim=U**(power+1)/s.Integer(power+1)
  elif role=='sqrt':trans=s.sqrt(U);prim=s.Rational(2,3)*U**s.Rational(3,2)
  else:trans=1/s.sqrt(U);prim=2*s.sqrt(U)
  # For non-natural bases the logarithm appears in du and must be accounted for.
  factor=n/(slope*(1 if base==s.E else s.log(base)))
  outer=s.simplify(factor*du)
  body=outer*trans.subs(U,inner)
  challenge='provided_substitution'if band=='easy'else 'simple_outer_function'if band=='moderate'else 'logarithmic_derivative'
  params={'base':str(base),'slope':str(slope),'offset':str(c),'amplitude':str(n),'outer':role}
  notes.append('Use a connected real interval on which the integrand is defined.'if role=='log'else 'Work where $'+tex(inner)+'>0$.')
 else:
  if band=='hard':
   c=s.Integer(rng.choice((1,2,3)));d=s.Integer(rng.choice((1,2,3)))
   inner=c*s.exp(X)+d;du=c*s.exp(X);trans=1/U;prim=s.log(U);factor=n
   body=n*du/inner;lo=s.log(2);hi=s.log(3)
   facts=[r'e^{\ln 2}=2',r'e^{\ln 3}=3'];params={'scale':str(c),'offset':str(d),'amplitude':str(n),'base':'E'}
  else:
   power=3 if case=='cube_e'else 1 if case.startswith('linear_')else 2
   slope=s.Integer(rng.choice((1,2)));shift=s.Integer(rng.randint(0,2));inner=slope*X**power+shift;du=s.diff(inner,X)
   factor=n/(slope*power);body=n*X**(power-1)*base**inner;trans=base**U;prim=base**U if base==s.E else base**U/s.log(base)
   lo=s.Integer(0);hi=s.log(2)**s.Rational(1,power)if base==s.E else s.Integer(1)
   facts=[r'e^{\ln 2}=2',r'e^{2\ln 2}=4']if base==s.E else []
   params={'power':power,'slope':str(slope),'shift':str(shift),'amplitude':str(n),'base':str(base)}
  challenge='provided_substitution'if band=='easy'else 'base_exponential_bounds'if band=='moderate'else 'logarithmic_derivative_bounds'
 body_tex=tex(body)
 factor=s.simplify(factor);primitive=s.simplify(factor*prim.subs(U,inner))
 return dict(body=body,body_tex=body_tex,inner=inner,du=du,factor=factor,trans=trans,prim=prim,primitive=primitive,lo=lo,hi=hi,notes=notes,facts=facts,params=params,challenge=challenge)

def primtex(expr,z):
 # log(U) primitive is ln|U| on each connected real component.
 if expr==s.log(U):return r'\ln\left|'+tex(z)+r'\right|'
 return tex(expr.subs(U,z))

def render(kp,band,case,m,seed,evidence):
 easy=band=='easy';lo,hi=m['lo'],m['hi'];definite=lo is not None;inverse_choice=kp in INV and not definite
 inner,du,r,trans,prim=(m[k]for k in('inner','du','factor','trans','prim'))
 u0,u1=(None,None)if not definite else tuple(s.simplify(inner.subs(X,v))for v in(lo,hi))
 original=integral(m['body_tex'],lo=lo,hi=hi);target=times(r,integral(tex(trans),'u',u0,u1))
 formula=integral(tex(trans),'u')+'='+primtex(prim,U)+'+C'
 problem=('Evaluate exactly.'if definite else 'Find an antiderivative.')+'\n\n'+block(original)
 if kp==17592186064250:problem+='\n\nWork on a connected interval where $|'+tex(inner)+'|>1$.'
 if kp==EXP[2]and not case.startswith('log'):problem+='\n\nWork where $'+tex(inner)+'>0$.'
 if not inverse_choice and not easy:problem+='\n\n{{answer}}'+(''if definite else ' $+C$')
 else:problem+='\n\n'+('Choose the exact value.'if definite else 'Choose the antiderivative. In each choice, $C$ is an arbitrary constant.')
 sol='Let $u='+tex(inner)+'$. Then $'+r'\mathrm{d}u=('+tex(du)+r')\,\mathrm{d}x$.'
 if m['notes']:sol+='\n\n'+'\n\n'.join(m['notes'])
 if definite:sol+='\n\nTransform both bounds:\n\n'+block(r'\begin{aligned}x='+tex(lo)+r'&\Longrightarrow u='+tex(u0)+r'\\x='+tex(hi)+r'&\Longrightarrow u='+tex(u1)+r'\end{aligned}')
 sol+='\n\nIncluding the differential factor gives\n\n'+block(r'\begin{aligned}&'+original+r'\\&='+target+r'.\end{aligned}')
 if definite and m['facts']:sol+='\n\nEndpoint values: $'+r',\quad '.join(m['facts'])+'$.'
 mathfp=fp(m['body'],lo,hi)
 if not definite:
  key=times(r,primtex(prim,inner));answer=m['primitive'];bank=[(key,'correct')]
  sol+='\n\nUse the integration rule:\n\n'+block(formula+'.')+'\n\n'+block(target+'='+times(r,primtex(prim,U))+'+C.')+'\n\nSubstitute back:\n\n'+block(key+'+C.')
 else:
  first,last=(s.simplify(prim.subs(U,v))for v in(u0,u1));answer=s.simplify(r*(last-first))
  if prim==s.log(U):key=times(r,r'\ln\left('+tex(u1)+r'\right)-\ln\left('+tex(u0)+r'\right)')
  else:key=tex(answer)
  bank=[(key,'correct')]
  sol+='\n\nUse the integration rule:\n\n'+block(formula+'.')+'\n\nEvaluate the primitive and subtract lower from upper:\n\n'+block(times(r,r'\left['+primtex(prim,U)+r'\right]_{'+tex(u0)+'}^{'+tex(u1)+'}')+'='+times(r,r'\left('+tex(last)+r'\right)-\left('+tex(first)+r'\right)')+'.')+'\n\nThe exact answer is\n\n'+block(key+'.')
 if easy or inverse_choice:
  if kp in INV:bank=inverse_models.answer_bank(m,case,mathfp,tex)
  else:bank=answer_bank(answer,r*prim,inner,X,U,mathfp,tex,lower=lo,upper=hi)
  key=next(value for value,label in bank if label=='correct').removesuffix('+C')
  prefix,_,suffix=sol.rsplit('$$',2)
  sol=prefix+'$$\n'+key+(''if definite else '+C')+'.\n$$'+suffix
 version=inverse_models.VERSION if kp in INV else VERSION
 uid=lambda role:str(uuid.uuid5(uuid.UUID(evidence['kp']['id']),version+':'+mathfp+':'+'evaluate'+':'+role))
 answers=[{':answer/id':uid('answer:'+v),':answer/type':':answer.type/math',':answer/value':v}for v,_ in bank]
 correct=next(a[':answer/id']for a,(_,label)in zip(answers,bank)if label=='correct')
 q={':question/id':uid('question'),':question/problem':problem,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+band,':question/answer-fields':[{':answer-field/id':uid('field'),':answer-field/key':'answer',':answer-field/type':':answer-field.type/radio'if easy or inverse_choice else ':answer-field.type/blank',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
 model={k:str(v)if v is not None else None for k,v in dict(integrand=m['body'],substitution=inner,derivative=du,factor=r,transformed=trans,primitive=m['primitive'],lower=lo,upper=hi,result=answer).items()}
 return {'knowledge_point':evidence['kp'],'question':q,'generation':{'version':version,'seed':seed,'template':case,'family':case,'challenge':'recognize_substitution_with_answer_choices'if easy else m['challenge'],'parameters':m['params'],'mathematical_fingerprint':mathfp,'model':model,'batch_contract':version,'source_basis':evidence['basis'],'source_questions':evidence['sources'],'band_origin':evidence['band_origin'][band],'operation':'evaluate','provided_substitution':False,'provided_primitive':False,'provided_endpoint_values':False,'support_policy':'mastered-prerequisite-recall','bank_correct_rank':None,'bank_recipes':[v for _,v in bank],'domain':'Connected real intervals where the displayed integrand is defined; definite intervals contain no singularities.'}}

def generate(kp,level,seed=0,template=None,*,evidence,index=0,attempt=0):
 if kp not in CASES or level not in CASES[kp]:raise ValueError('Unsupported KP/band')
 case=template or random.Random(f'{seed}:{kp}:{level}').choice(CASES[kp][level])
 if case not in CASES[kp][level]:raise ValueError('Unsupported family')
 for offset in range(attempt,attempt+300):
  rng=random.Random(f'{seed}:{kp}:{level}:{case}:{index}:{offset}')
  m=instance(kp,level,case,rng,(index//len(CASES[kp][level]))%4)
  if kp==17592186064250 and level=='moderate' and m['factor'].is_Integer:continue
  record=render(kp,level,case,m,seed,evidence)
  if record['generation']['mathematical_fingerprint']in evidence.get('easy_excluded_tasks'if level=='easy'else 'excluded_tasks',[]):continue
  return record
 raise ValueError('Bounded variant capacity exhausted')
def batch(kp,level,count=8,seed=0,*,evidence,template=None):
 if not 1<=count<=100:raise ValueError('Count must be 1..100')
 cases=list(CASES[kp][level]);random.Random(f'{seed}:{kp}:{level}:order').shuffle(cases);seen=set();shapes={};rows=[]
 for index in range(count):
  for attempt in range(300):
   record=generate(kp,level,seed,template or cases[index%len(cases)],evidence=evidence,index=index,attempt=attempt)
   key=record['generation']['mathematical_fingerprint']
   shape=record['generation']['model']['substitution']
   if key in seen or count>=8 and (shapes.get(shape,0)>=(count+2)//3 ):continue
   rows.append(record);seen.add(key);shapes[shape]=shapes.get(shape,0)+1;break
  else:raise ValueError('Finite unique task capacity exhausted')
 return rows

def cli(kp,folder):
 p=argparse.ArgumentParser();p.add_argument('--difficulty',required=True,choices=('easy','moderate','hard'));p.add_argument('--count',type=int,default=8);p.add_argument('--seed',type=int,default=0);p.add_argument('--template');p.add_argument('--format',choices=('json','markdown'),default='json');a=p.parse_args()
 rows=batch(kp,a.difficulty,a.count,a.seed,evidence=json.loads((Path(folder)/'source-evidence.json').read_text()),template=a.template)
 print(json.dumps(rows,indent=2)if a.format=='json'else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']for r in rows))
