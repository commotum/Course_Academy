#!/usr/bin/env python3
"""2D unit-vector normalization; frozen basis2275; local unregistered draft.

Direct and scalar-combination source backbones. Missing easy is a conservative
small-integer-length direct-vector extension. No 3D, dot products or angles.
"""
from __future__ import annotations
import argparse,copy,hashlib,json,math,random,sys,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix('')
sys.path.insert(0,str(HERE))
from math_format import checked_math_content,matrix_tex,normalize_prose,normalize_tex
KP_ID=17592186059716
KP_UUID='9c45a70b-273c-5fec-a768-40a1cf218628'
TITLE='Calculating a Unit Vector Parallel to a Given Vector'
VERSION='unit-vector-review-2'
SUPPORTED_LEVELS=('easy','moderate','hard')
SOURCE={'database':'math','basis':2275,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
OLD_CATALOG=[(5,12,2),(8,-6,3),(3,8,1),(5,4,2),(7,24,3),(-8,15,2),(20,-21,-2),(9,40,1),(-12,-5,-1),(4,-7,-3),(11,6,2),(2,9,-2)]

def tex(z):return sp.latex(sp.sympify(z))
def vector(v):return matrix_tex([[tex(z)] for z in v])
def align(rows):return '\n$$\n'+r'\begin{aligned}'+(' '+r'\\'+'\n').join(rows)+r'\end{aligned}'+'\n$$'
def bank(profile,x,y):
 x,y=sp.Integer(x),sp.Integer(y);s=x*x+y*y;n=sp.sqrt(s)
 if profile=='q-17709':return [(x/n,-y/n),(x,y),(x/n,y/(3*n)),(x/n,y/n),(x/(2*n),y/n)],3
 if profile=='q-125135':return [(x/(2*n),y/(2*n)),(x/sp.sqrt(n/2),y/sp.sqrt(n/2)),(x/n,y/n),(x/sp.sqrt(n),y/sp.sqrt(n)),(x/(4*n),y/(2*n))],2
 if profile=='q-18058':return [(1/n,x/n),(x/sp.sqrt(s+4),y/sp.sqrt(s+4)),(y/n,x/n),(x/n,y/n),(x/sp.sqrt(s+3),y/sp.sqrt(s+3))],3
 raise ValueError('Unknown complete profile')

def strict_int(v,label):
 if type(v) is not int:raise TypeError(label+' must be a builtin int')

def render(level,p,profile,seed=0):
 for k,v in p.items():
  if k not in ('mode','label'):strict_int(v,k)
 x,y=p['x'],p['y'];n=sp.sqrt(x*x+y*y)
 if x==0 or y==0 or abs(x)==abs(y) or n==1:raise ValueError('Domain excludes zero components, equal absolute components and unit input')
 if p['mode'] not in ('direct','combination'):raise ValueError('Unknown template')
 if profile=='q-125135' and n.is_Integer is not True:raise ValueError('Integer-length profile only')
 if profile=='q-18058' and y==1:raise ValueError('Bank collision for y=1')
 combination=p['mode']=='combination'
 if combination:
  ca,cb=p['ca'],p['cb']
  if (ca,cb) not in ((2,1),(3,1),(1,2),(1,3)):raise ValueError('Unsupported scalar roles')
  a=(p['a1'],p['a2']);b=(sp.Rational(x-ca*a[0],cb),sp.Rational(y-ca*a[1],cb))
  if any(z.q!=1 for z in b):raise ValueError('Operands must be integer vectors')
  target=('' if ca==1 else str(ca))+'a+'+('' if cb==1 else str(cb))+'b'
  prompt=f'Let $a={vector(a)}$ and $b={vector(b)}$.'
 else:target=p.get('label','b');prompt=f'Let ${target}={vector((x,y))}$.'
 prompt+=f' Find a unit vector that is parallel to ${target}$ and points the same direction.'
 solution='Remember that to find a unit vector that is parallel to a given vector'+(' and points the same direction' if combination or target=='n' else '')+', we need to divide the given vector by its length:\n'+align([f'u &= \\frac{{{target}}}{{|{target}|}}'])
 if combination:
  scaled_a=tuple(ca*z for z in a);scaled_b=tuple(cb*z for z in b)
  expression=lambda c,v:('' if c==1 else str(c)+r'\cdot ')+vector(v)
  addition=matrix_tex([[f'{scaled_a[0]}+({scaled_b[0]})'],[f'{scaled_a[1]}+({scaled_b[1]})']])
  solution+="\n\nFirst, let's compute the sum:\n"+align([f'{target} &= '+expression(ca,a)+'+'+expression(cb,b),'&= '+vector(scaled_a)+'+'+vector(scaled_b),'&= '+addition,'&= '+vector((x,y))])
 rows=[f'|{target}| &= \\sqrt{{({x})^2+({y})^2}}']
 if not combination and profile=='q-125135':rows+=['&= '+f'\\sqrt{{{x*x}+{y*y}}}']
 rows+=['&= '+f'\\sqrt{{{x*x+y*y}}}','&= '+tex(n)]
 solution+='\n\nUsing the formula for the magnitude of a vector, we get\n'+align(rows)
 values,correct=bank(profile,x,y)
 solution+=f'\n\nFinally, we divide ${target}$ by its length and get the following unit vector:\n'+align([f'u &= \\frac{{{target}}}{{|{target}|}}','&= '+f'\\frac{{1}}{{{tex(n)}}}\\cdot ({target})','&= '+f'\\frac{{1}}{{{tex(n)}}}\\cdot '+vector((x,y)),'&= '+vector(values[correct])])
 return normalize_prose(prompt),normalize_prose(solution),values,correct

def task_fingerprint(p):
 # Actual supplied task, excluding levels, seed, selected bank and cosmetic labels.
 if p['mode']=='direct':key=['direct',p['x'],p['y']]
 else:
  ca,cb=p['ca'],p['cb'];key=['combination',ca,cb,p['a1'],p['a2'],(p['x']-ca*p['a1'])//cb,(p['y']-ca*p['a2'])//cb]
 return hashlib.sha256(json.dumps(key,separators=(',',':')).encode()).hexdigest()

@checked_math_content
def generate(level,p,profile=None,seed=0):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unknown difficulty')
 strict_int(seed,'seed')
 profile=profile or ('q-17709' if level=='hard' else 'q-125135')
 prompt,solution,values,correct=render(level,p,profile,seed);fp=task_fingerprint(p)
 qid=str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION+':'+fp+':'+profile));fid=str(uuid.uuid5(uuid.UUID(qid),'field:selection'))
 choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'recipe:'+str(i))),':answer/type':':answer.type/math',':answer/value':normalize_tex(vector(v))} for i,v in enumerate(values)]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/requires-calculator':False,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[correct][':answer/id']]}]},'generation':{'version':VERSION,'template':p['mode'],'parameters':copy.deepcopy(p),'bank_profile':profile,'seed':seed,'parameter_fingerprint':fp,'source':SOURCE,'source_ids':['q-17709','q-125138'] if level=='hard' else [profile,'q-70409'],'authored_extension':level=='easy' or p not in original_parameters(),'assets':[],'dependencies':{'sympy':sp.__version__}}}

def original_parameters():return [dict(x=x,y=y,mode='combination',ca=2,cb=1,a1=0,a2=t) for x,y,t in OLD_CATALOG]+[dict(x=x,y=y,mode='direct',label='b') for x,y,t in OLD_CATALOG if math.isqrt(x*x+y*y)**2==x*x+y*y]

def catalog(level):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unknown difficulty')
 rows=[]
 if level=='hard':rows=[(p,'q-17709') for p in original_parameters() if p['mode']=='combination']
 elif level=='moderate':rows=[(p,'q-125135') for p in original_parameters() if p['mode']=='direct']
 for x in range(-12,13):
  for y in range(-12,13):
   if not x or not y or abs(x)==abs(y):continue
   s=x*x+y*y;n=math.isqrt(s)
   if level=='easy' and (n*n!=s or n>13):continue
   if level=='moderate' and y==1 and n*n!=s:continue
   if level=='hard':
    # Operand coordinates and coefficient-side roles vary independently of output.
    for ca,cb,a1,a2 in ((2,1,1,-2),(3,1,-2,3),(1,2,x%2,y%2)):
     p=dict(x=x,y=y,mode='combination',ca=ca,cb=cb,a1=a1,a2=a2)
     rows.append((p,'q-17709'))
   else:rows.append((dict(x=x,y=y,mode='direct',label='b'),'q-125135' if n*n==s else 'q-18058'))
 seen=set();result=[]
 for p,profile in rows:
  fp=task_fingerprint(p)
  if fp not in seen:seen.add(fp);result.append((p,profile))
 return result

def batch(difficulty,count=1,seed=0):
 strict_int(count,'count');strict_int(seed,'seed')
 if count<1:raise ValueError('count must be positive')
 rows=catalog(difficulty)
 if count>len(rows):raise ValueError(f'count exceeds capacity {len(rows)}')
 random.Random(seed).shuffle(rows)
 return [generate(difficulty,p,profile,seed) for p,profile in rows[:count]]

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=SUPPORTED_LEVELS,default='moderate');parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json','markdown'],default='json');args=parser.parse_args()
 try:records=batch(args.difficulty,args.count,args.seed)
 except (ValueError,TypeError) as e:parser.error(str(e))
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\nChoices: '+', '.join('$'+a[':answer/value']+'$' for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+r['question'][':question/worked-solution'] for r in records))
if __name__=='__main__':main()
