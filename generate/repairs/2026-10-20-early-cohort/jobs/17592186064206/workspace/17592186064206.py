#!/usr/bin/env python3
"""Bounded source-faithful easy radio generator for linear rational integration."""
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186064206
KP_UUID='fc4294d6-3d60-5c9e-a862-863e1d129049'
TITLE='Integrating a Linear Rational Function'
VERSION='linear-rational-v2'
PACKAGE=Path(__file__).with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
PROFILES=json.loads((PACKAGE/'contract.json').read_text())['profiles']
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(x)))
def tex(x):return sp.latex(sp.Rational(x)).replace('- ', '-')
def denom(a,b):
 if a==1:return 'x'+('+' if b>0 else '')+str(b)
 if a<0:return str(b)+('-x' if a==-1 else str(a)+'x')
 return str(a)+'x'+('+' if b>=0 else '')+str(b)
def fingerprint(p):
 n,a,b=p
 return digest(['rational-integrand',str(sp.Rational(n,a)),str(sp.Rational(b,a))])
def bank(profile,n,a,b):
 d=denom(a,b);log=lambda c,arg:('-' if c==-1 else tex(c) if c!=1 else '')+r'\operatorname{ln}⁡|'+arg+'|+C'
 if profile=='coefficient':return [log(c,d) for c in (sp.Integer(n),sp.Rational(1,n),-sp.Integer(n),-sp.Rational(1,n),sp.Integer(1))]
 if profile=='negative-slope':return [log(c,d) for c in (sp.Rational(1,a),-sp.Rational(1,a),sp.Integer(a),-sp.Integer(a),sp.Integer(-1))]
 if profile=='negative-shift':return [log(1,d),log(-1,d),log(1,'x'),log(-1,'x'),log(-1,denom(a,-b))]
 if profile=='positive-shift':return [log(1,d),log(sp.Rational(1,b),d),log(b,d),log(1,'x'),log(b,'x')]
 raise ValueError('unknown source bank')
def allowed(profile,p):
 if len(p)!=3 or any(type(x)!=int for x in p):return False
 n,a,b=p
 if profile=='coefficient':return a==1 and 2<=n<=9 and 1<=b<=12
 if profile=='negative-slope':return n==1 and -9<=a<=-2 and 1<=b<=12
 if profile=='negative-shift':return n==a==1 and -12<=b<=-1
 if profile=='positive-shift':return n==a==1 and 2<=b<=12
 return False

def source_generate(difficulty='easy',seed=0,template=None,parameters=None):
 if difficulty!='easy':raise ValueError('Unsupported level in this bounded package; see capabilities.json')
 rng=random.Random(seed);sid=template or rng.choice(list(PROFILES));t=PROFILES[sid];profile=t['profile']
 if parameters is None:
  parameters=([rng.randint(2,9),1,rng.randint(1,12)] if profile=='coefficient' else [1,-rng.randint(2,9),rng.randint(1,12)] if profile=='negative-slope' else [1,1,-rng.randint(1,12)] if profile=='negative-shift' else [1,1,rng.randint(2,12)])
 if not allowed(profile,parameters):raise ValueError('Outside validated parameter bounds')
 n,a,b=parameters;values=bank(profile,n,a,b)
 if len(set(values))!=5:raise ValueError('Bank collision')
 def render(s):
  for k,v in {'@@D@@':denom(a,b),'@@N@@':str(n),'@@INV@@':tex(sp.Rational(1,a)),'@@A@@':str(a)}.items():s=s.replace(k,v)
  return s
 fp=fingerprint(parameters)
 # Bank identity matters for reproducible authoring; novelty never depends on it.
 qid=ident(['question',VERSION,fp,digest(sorted(values)),digest([t['prompt'],t['solution']])]);fid=ident([qid,'field','selection'])
 choices=[{':answer/id':ident([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 q={':question/id':qid,':question/problem':render(t['prompt']),':question/worked-solution':render(t['solution']),':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[0][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':profile,'parameters':parameters,'domain':f'x real; x != {sp.Rational(-b,a)}; antiderivative on each connected interval','source_ids':[sid],'mathematical_fingerprint':fp,'sympy':sp.__version__}}

ADDITIONAL=json.loads((PACKAGE/'additional-source.json').read_text())

def log_value(c,arg):
 return ('-' if c==-1 else tex(c) if c!=1 else '')+r'\operatorname{ln}⁡|'+arg+'|+C'

def solution(n,a,b):
 d=denom(a,b);c=sp.Rational(n,a)
 return (f'First, let $u={d}.$ Then differentiating with respect to $x$ gives\n\n$$\n'
         +r'\frac{\text{d}u}{\text{d}x}='+str(a)+r'\quad\Longrightarrow\quad\text{d}x='
         +tex(sp.Rational(1,a))+r'\,\text{d}u.'+'\n$$\n\n'
         +'We can now rewrite the integral in terms of $u,$ solve it, and write the final answer in terms of $x$ as follows:\n\n$$\n'
         +r'\begin{aligned}\int \frac{'+str(n)+'}{'+d+r'}\,\text{d}x & ='
         +str(n)+r'\int \frac{1}{u}\cdot\left('+tex(sp.Rational(1,a))+r'\,\text{d}u\right) \\ & ='
         +tex(c)+r'\int \frac{1}{u}\,\text{d}u \\ & ='+log_value(c,'u')
         +r' \\ & ='+log_value(c,d)+r'\end{aligned}'+'\n$$')

def record(parameters,values,correct,seed,profile,prompt=None,worked=None,template='affine-substitution'):
 n,a,b=parameters
 prompt=prompt or r'Calculate $\int \frac{'+str(n)+'}{'+denom(a,b)+r'}\,\text{d}x.$'
 worked=worked or solution(n,a,b)
 qid=ident(['question',VERSION,prompt,sorted(values)]);fid=ident([qid,'field','selection'])
 choices=[{':answer/id':ident([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':worked,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',ident([fid,correct])]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':parameters,'domain':f'x real; x != {sp.Rational(-b,a)}; antiderivative on each connected interval','source_ids':['d6501a20-6ebd-5786-870e-3527423b6332','58fee417-01ff-5eb4-9db6-9bace2e941d9'],'mathematical_fingerprint':fingerprint(parameters),'sympy':sp.__version__}}

def valid_parameters(p):
 return (len(p)==3 and all(type(v)==int for v in p) and 1<=p[0]<=9
         and 1<=abs(p[1])<=9 and -12<=p[2]<=12)

def candidates(rng,parameters=None,profile=None):
 # Construct the whole eligible bank before assigning the answer-bearing role.
 a=rng.choice([-1,1])*rng.randint(1,9) if parameters is None else parameters[1]
 b=rng.randint(-12,12) if parameters is None else parameters[2]
 profile=profile or rng.choice(['coefficient-choice','argument-choice'])
 if profile=='coefficient-choice':
  ns=rng.sample(range(1,10),5)
  if parameters is not None and parameters[0] not in ns:ns[0]=parameters[0]
  pars=[[n,a,b] for n in ns]
 else:
  other=rng.choice([v for v in range(-12,13) if v!=b])
  ns=rng.sample(range(1,10),2)
  if parameters is not None and parameters[0] not in ns:ns[0]=parameters[0]
  pars=[[n,a,b] for n in ns]+[[n,a,other] for n in rng.sample(range(1,10),3)]
 return profile,pars

def from_candidates(pars,target,seed,profile):
 values=[log_value(sp.Rational(n,a),denom(a,b)) for n,a,b in pars]
 correct=values[target];random.Random(seed).shuffle(values)
 r=record(pars[target],values,correct,seed,profile)
 r['generation']['bank_parameters']=[list(p) for p in pars]
 r['generation']['target_index']=target
 return r

def replay(generation):
 """Reconstruct a batch member including its complete bank and option order."""
 if 'bank_parameters' in generation:
  return from_candidates(generation['bank_parameters'],generation['target_index'],generation['seed'],generation['profile'])
 return generate(seed=generation['seed'],template=generation['template'],parameters=generation['parameters'])

def generate(difficulty='easy',seed=0,template=None,parameters=None):
 if difficulty!='easy':raise ValueError('Unsupported difficulty: '+difficulty)
 rng=random.Random(seed)
 if parameters is not None:
  if not valid_parameters(parameters):raise ValueError('Outside validated parameter bounds')
  if template in PROFILES and parameters==PROFILES[template]['parameters']:
   return source_generate(difficulty,seed,template,parameters)
  if template=='q-49511' and parameters==[2,3,5]:
   q=ADDITIONAL['incomplete'];values=[c[':answer/value'] for c in q[':question/answer-fields'][0][':answer-field/choices']]
   return record(parameters,values,values[1],seed,'source-replay',q[':question/problem'],template=template)
  profile,pars=candidates(rng,parameters)
  r=from_candidates(pars,pars.index(parameters),seed,profile)
  if template=='e-449' and parameters==[3,5,2]:
   q=ADDITIONAL['canonical'];f=r['question'][':question/answer-fields'][0]
   values=[c[':answer/value'] for c in f[':answer-field/choices']]
   return record(parameters,values,log_value(sp.Rational(3,5),'5x+2'),seed,'canonical-replay',q[':question/problem'],q[':question/worked-solution'],template)
  return r
 if template in PROFILES:return source_generate(difficulty,seed,template,PROFILES[template]['parameters'])
 if template=='q-49511':return generate(difficulty,seed,template,[2,3,5])
 if template=='e-449':return generate(difficulty,seed,template,[3,5,2])
 if template is not None:raise ValueError('Unknown template')
 profile,pars=candidates(rng)
 return from_candidates(pars,rng.randrange(5),seed,profile)

def batch(difficulty,count,seed):
 if difficulty!='easy':raise ValueError('Unsupported difficulty: '+difficulty)
 if count<1:raise ValueError('positive count required')
 rng=random.Random(seed);records=[];used=set()
 for group in range(max(2000,count*20)):
  profile,pars=candidates(rng)
  # Retain whole counterfactual groups; do not truncate a group through rejection.
  fps=[fingerprint(p) for p in pars]
  if any(fp in used for fp in fps):continue
  roles=list(range(5));rng.shuffle(roles)
  for target in roles:
   records.append(from_candidates(pars,target,rng.getrandbits(63),profile))
   used.add(fps[target])
   if len(records)==count:return records
 raise ValueError('Finite family exhausted')

def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rs=batch(a.difficulty,a.count,a.seed)
 print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
