#!/usr/bin/env python3
"""Seeded 2D unit-vector normalization, source basis 4457.

Direct and scalar-combination source backbones, complete source-bank replay,
and a declared five-choice normalization-error extension for normal practice.
No database or image writes. Moderate is the source-justified default.
"""
from __future__ import annotations
import argparse,copy,hashlib,json,math,random,sys,uuid
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from math_format import checked_math_content,matrix_tex,normalize_prose,normalize_tex
KP_ID=17592186059716
KP_UUID='9c45a70b-273c-5fec-a768-40a1cf218628'
TITLE='Calculating a Unit Vector Parallel to a Given Vector'
VERSION='unit-vector-package-4'
SUPPORTED_LEVELS=('easy','moderate','hard')
SOURCE={'database':'math','basis':4457,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}


def tex(z):return sp.latex(sp.sympify(z))
def vector(v):return matrix_tex([[tex(z)] for z in v])
def align(rows):return '\n$$\n'+r'\begin{aligned}'+(' '+r'\\'+'\n').join(rows)+r'\end{aligned}'+'\n$$'
def bank(profile,x,y):
 x,y=sp.sympify(x),sp.sympify(y);s=x*x+y*y;n=sp.sqrt(s);v=sp.Matrix([x,y])
 if profile=='q-17709':return [(x/n,-y/n),(x,y),(x/n,y/(3*n)),(x/n,y/n),(x/(2*n),y/n)],3
 if profile=='q-125135':return [tuple(v/(2*n)),tuple(v/sp.sqrt(n/2)),tuple(v/n),tuple(v/sp.sqrt(n)),(x/(4*n),y/(2*n))],2
 if profile=='q-18058':return [(1/n,x/n),tuple(v/sp.sqrt(s+4)),(y/n,x/n),tuple(v/n),tuple(v/sp.sqrt(s+3))],3
 if profile=='q-125137':return [tuple(3*v/(2*n)),tuple(v/sp.sqrt(15*s)),tuple(v/n),tuple(3*v/n),tuple(3*v/sp.sqrt(15*s))],2
 if profile=='q-70415':
  g=sp.gcd(x,y);g=abs(g);R=s/g**2
  return [tuple(v/g/sp.sqrt(R-2)),tuple(v/sp.sqrt(R)),tuple(v/g/sp.sqrt(3*R)),tuple(v/sp.sqrt(R+8)),tuple(v/n)],4
 if profile=='q-70419':return [(x*x/n,y/n),(x/sp.sqrt(s-1),y*y/sp.sqrt(s-1)),tuple(v/n),(y/n,sp.sqrt(x)/n),(x/sp.sqrt(4*n),y*y/sp.sqrt(4*n))],2
 if profile=='e-4301':return [tuple(v/n),tuple(v),tuple(v/(3*n)),tuple(v/(2*n)),(y/n,x/n)],0
 if profile=='authored':return [tuple(v/n)],0
 raise ValueError('Unknown complete profile')

def practice_bank(x,y,rng,p=None):
 """Source-adjacent error operations, not a frozen source-bank size ranking."""
 x,y=sp.sympify(x),sp.sympify(y);n=sp.sqrt(x*x+y*y);u=(x/n,y/n)
 # Each alternative is an identifiable error on this instance: no normalization,
 # opposite direction, one sign, swapped components, missing one division,
 # squared length, Manhattan length, or forgetting to square the components.
 candidates=[(x,y),(-u[0],-u[1]),(-u[0],u[1]),(u[0],-u[1]),(u[1],u[0]),(u[0],y),(x,u[1])]
 for wrong_norm in (n*n,abs(x)+abs(y),sp.sqrt(abs(x)+abs(y))):
  if wrong_norm!=0:candidates.append((x/wrong_norm,y/wrong_norm))
 if p and p['mode']=='combination':
  ca,cb=p['ca'],p['cb'];a=sp.Matrix([sp.sympify(p['a1']),sp.sympify(p['a2'])]);v=sp.Matrix([x,y]);b=(v-ca*a)/cb
  for wrong in (a+cb*b,ca*a+b,a+b):
   length=sp.sqrt(wrong.dot(wrong))
   if length!=0:candidates.append(tuple(wrong/length))
 unique=[];seen={tuple(sp.simplify(z) for z in u)}
 for v in candidates:
  key=tuple(sp.simplify(z) for z in v)
  if key not in seen:unique.append(key);seen.add(key)
 return [u]+rng.sample(unique,4),0

def strict_int(v,label):
 if type(v) is not int:raise TypeError(label+' must be a builtin int')

def render(level,p,profile,seed=0):
 x,y=sp.sympify(p['x']),sp.sympify(p['y']);n=sp.sqrt(x*x+y*y)
 if n==0:raise ValueError('Zero target has no unit direction')
 if p['mode'] not in ('direct','combination'):raise ValueError('Unknown template')
 if profile=='q-125135' and n.is_Integer is not True:raise ValueError('Integer-length profile only')
 if profile=='q-18058' and y==1:raise ValueError('Bank collision for y=1')
 combination=p['mode']=='combination'
 if combination:
  ca,cb=p['ca'],p['cb']
  if ca not in (1,2,3) or cb not in (1,2,3) or ca==cb==1:raise ValueError('Unsupported scalar roles')
  a=(sp.sympify(p['a1']),sp.sympify(p['a2']));b=tuple(sp.simplify((z-ca*v)/cb) for z,v in zip((x,y),a))
  la,lb=p.get('labels',['a','b'])
  target=('' if ca==1 else str(ca))+la+'+'+('' if cb==1 else str(cb))+lb
  prompt=f'Let ${la}={vector(a)}$ and ${lb}={vector(b)}$.'
 else:target=p.get('label','b');prompt=f'Let ${target}={vector((x,y))}$.'
 prompt+=f' Find a unit vector that is parallel to ${target}$ and points the same direction.'
 solution='Remember that to find a unit vector that is parallel to a given vector'+(' and points the same direction' if combination or target=='n' else '')+', we need to divide the given vector by its length:\n'+align([f'u &= \\frac{{{target}}}{{|{target}|}}'])
 if combination:
  scaled_a=tuple(ca*z for z in a);scaled_b=tuple(cb*z for z in b)
  expression=lambda c,v:('' if c==1 else str(c)+r'\cdot ')+vector(v)
  addition=matrix_tex([[f'{tex(scaled_a[0])}+({tex(scaled_b[0])})'],[f'{tex(scaled_a[1])}+({tex(scaled_b[1])})']])
  solution+="\n\nFirst, let's compute the sum:\n"+align([f'{target} &= '+expression(ca,a)+'+'+expression(cb,b),'&= '+vector(scaled_a)+'+'+vector(scaled_b),'&= '+addition,'&= '+vector((x,y))])
 rows=[f'|{target}| &= \\sqrt{{({tex(x)})^2+({tex(y)})^2}}']
 if not combination and profile=='q-125135':rows+=['&= '+f'\\sqrt{{{tex(x*x)}+{tex(y*y)}}}']
 rows+=['&= '+f'\\sqrt{{{tex(sp.simplify(x*x+y*y))}}}','&= '+tex(n)]
 solution+='\n\nUsing the formula for the magnitude of a vector, we get\n'+align(rows)
 values,correct=bank(profile,x,y)
 if n.is_Integer is not True:
  solution+='\n\nFor a radical denominator, use $\\sqrt{R}\\,\\sqrt{R}=R$ to simplify the components; equivalently, $1/\\sqrt{R}=\\sqrt{R}/R$ for $R>0$.\n'
 solution+=f'\n\nFinally, we divide ${target}$ by its length and get the following unit vector:\n'+align([f'u &= \\frac{{{target}}}{{|{target}|}}','&= '+f'\\frac{{1}}{{{tex(n)}}}\\cdot ({target})','&= '+f'\\frac{{1}}{{{tex(n)}}}\\cdot '+vector((x,y)),'&= '+vector(values[correct])])
 return normalize_prose(prompt),normalize_prose(solution),values,correct

def task_fingerprint(p):
 if p['mode']=='direct':key=['direct',p['x'],p['y']]
 else:key=['combination',p['ca'],p['cb'],p['a1'],p['a2'],p['x'],p['y']]
 return hashlib.sha256(json.dumps(key,separators=(',',':')).encode()).hexdigest()

@checked_math_content
def generate(level,p=None,profile='authored',seed=0,replay=False):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
 strict_int(seed,'seed')
 if p is None:p=sample_parameters(level,random.Random(seed))
 if (p['mode']=='combination')!=(level=='hard'):raise ValueError('Template/difficulty mismatch')
 prompt,solution,values,correct=render(level,p,profile,seed)
 rng=random.Random(str(seed)+':bank')
 if profile=='authored':values,correct=practice_bank(p['x'],p['y'],rng,p)
 values=[tuple(sp.simplify(z) for z in v) for v in values]
 if len(set(values))!=len(values):raise ValueError('Bank collision')
 fp=task_fingerprint(p)
 # Content IDs derive from the bank, not the seed or its display ordering.
 key=json.dumps([prompt,solution,sorted([vector(v) for v in values])],sort_keys=True)
 qid=str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION+key));fid=str(uuid.uuid5(uuid.UUID(qid),'field:selection'))
 choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),vector(v))),':answer/type':':answer.type/math',':answer/value':normalize_tex(vector(v))} for v in values]
 correct_id=choices[correct][':answer/id']
 rng.shuffle(choices)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/requires-calculator':False,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct_id]}]},'generation':{'version':VERSION,'template':p['mode'],'parameters':copy.deepcopy(p),'bank_profile':profile,'bank_numeric_rank':sorted(values,key=lambda v:tuple(float(z) for z in v)).index(values[correct]),'seed':seed,'parameter_fingerprint':fp,'source':SOURCE,'source_ids':['q-17709','q-125138','q-70415','q-70419'] if level=='hard' else ['q-125135','q-70409','q-125137','q-18058'],'authored_extension':not replay,'assets':[],'dependencies':{'sympy':sp.__version__}}}

def sample_parameters(level,rng):
 # Easy retains magnitude calculation and normalization, with familiar lengths.
 if level=='easy':
  x,y=rng.choice([(3,4),(4,3),(6,8),(8,6)])
  return dict(mode='direct',x=rng.choice([-1,1])*x,y=rng.choice([-1,1])*y,label=rng.choice(['a','b','n','r']))
 # Choose norm case and signed target before operands and distractor assignments.
 radical=level=='hard' and rng.randrange(3)==0
 if radical:
  m=rng.randint(4,10);x=rng.randint(1,m-1);r=m*m-x*x
  while math.isqrt(r)**2==r:
   x=rng.randint(1,m-1);r=m*m-x*x
  xy=[rng.choice([-1,1])*x, str(rng.choice([-1,1]))+'*sqrt('+str(r)+')']
  if rng.randrange(2):xy.reverse()
 else:
  integer_norm=rng.choice([True,False])
  axis=rng.randrange(12)==0
  while True:
   x,y=rng.randint(0 if axis else 1,12),rng.randint(0 if axis else 1,12);s=x*x+y*y
   if axis:
    if (x==0)!=(y==0) and max(x,y)>=2:break
   elif (math.isqrt(s)**2==s)==integer_norm:break
  xy=[rng.choice([-1,1])*x,rng.choice([-1,1])*y]
 p=dict(mode='combination' if level=='hard' else 'direct',x=xy[0],y=xy[1])
 if level=='moderate':p['label']=rng.choice(['a','b','n','r']);return p
 pairs=[(1,2),(1,3),(2,1),(3,1),(2,3),(3,2)]
 while True:
  ca,cb=rng.choice(pairs);a=[rng.randint(-5,5),rng.randint(-5,5)]
  if radical:
   # Only one operand carries the radical, unscaled, as in q-70419.
   if ca!=1 and cb!=1:continue
   j=next(i for i,z in enumerate(xy) if sp.sympify(z).is_Integer is not True)
   a[j]=sp.sympify(xy[j]) if ca==1 else sp.Integer(0)
  b=[sp.simplify((sp.sympify(z)-ca*v)/cb) for z,v in zip(xy,a)]
  if any(z.is_Integer is not True for i,z in enumerate(b) if not radical or i!=j):continue
  if max(abs(float(z)) for z in b)>16:continue
  p.update(ca=ca,cb=cb,a1=str(a[0]),a2=str(a[1]),labels=rng.choice([['a','b'],['r','s'],['t','v']]))
  return p

SOURCE_PARAMETERS={
 'q-17709':('hard',dict(mode='combination',x=8,y=-6,ca=1,cb=3,a1=-1,a2=0)),
 'q-18058':('moderate',dict(mode='direct',x=3,y=8,label='a')),
 'q-125135':('moderate',dict(mode='direct',x=8,y=-6,label='b')),
 'q-125138':('hard',dict(mode='combination',x=5,y=12,ca=2,cb=1,a1=0,a2=2)),
 'q-70409':('moderate',dict(mode='direct',x=5,y=4,label='n')),
 'q-70415':('hard',dict(mode='combination',x=-6,y=-3,ca=3,cb=2,a1=-2,a2=1,labels=['r','s'])),
 'q-125137':('moderate',dict(mode='direct',x=-3,y=-6,label='r')),
 'q-70419':('hard',dict(mode='combination',x=5,y='sqrt(11)',ca=1,cb=2,a1=-1,a2='sqrt(11)',labels=['t','v'])),
 'e-4301':('hard',dict(mode='combination',x=0,y=-2,ca=1,cb=2,a1=-2,a2=0)),
}

def source_replay():
 fixtures=json.loads((HERE/'source-replay.json').read_text())
 records=[]
 for sid,(level,p) in SOURCE_PARAMETERS.items():
  src=fixtures[sid];profile=sid if src.get(':question/answer-fields') or sid=='e-4301' else 'authored'
  r=generate(level,p,profile,seed=100,replay=True)
  r['question'][':question/problem']=normalize_prose(src[':question/problem'])
  if src.get(':question/worked-solution'):
   r['question'][':question/worked-solution']=normalize_prose(src[':question/worked-solution'].replace('|t+v|','|t+2v|').replace('direction.,','direction,'))
  if ':question/difficulty' not in src:r['question'].pop(':question/difficulty')
  r['generation'].update(source_replay=sid,source_difficulty=src.get(':question/difficulty'),inferred_bank=not bool(src.get(':question/answer-fields')))
  records.append(r)
 return records

def batch(difficulty,count=1,seed=0):
 strict_int(count,'count');strict_int(seed,'seed')
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 if count<1:raise ValueError('count must be positive')
 rng=random.Random(seed);result=[];seen=set();attempts=0
 # A complete batch must not accidentally teach a fixed numerical-rank action
 # inside a visible component family. Resample whole mathematical instances;
 # never inject implausible distractors to change a rank.
 ranks={};positions=list(range(5));random.Random(str(seed)+':positions').shuffle(positions)
 # Small practice pools retain both source-supported magnitude/component cases.
 # Two per represented case also makes conditional rank diversity testable.
 profiles=['integer','radical','integer','radical'] if difficulty!='easy' and count>=4 else []
 random.Random(str(seed)+':profiles').shuffle(profiles)
 while len(result)<count:
  attempts+=1
  if attempts>max(100,count*30):raise ValueError('Unable to find distinct instances')
  r=generate(difficulty,seed=rng.getrandbits(63));fp=r['generation']['parameter_fingerprint']
  if fp in seen:continue
  family='radical-components' if r'\sqrt' in r['question'][':question/problem'] else 'integer-components'
  if len(result)<len(profiles):
   p=r['generation']['parameters']
   case=('radical' if family=='radical-components' else 'integer') if difficulty=='hard' else ('integer' if sp.sqrt(sp.sympify(p['x'])**2+sp.sympify(p['y'])**2).is_Integer else 'radical')
   if case!=profiles[len(result)]:continue
  prior=ranks.get(family,set());rank=r['generation']['bank_numeric_rank']
  if len(prior)==1 and rank in prior:continue
  ranks.setdefault(family,set()).add(rank)
  field=r['question'][':question/answer-fields'][0];cid=field[':answer-field/correct'][1]
  cs=field[':answer-field/choices'];chosen=next(c for c in cs if c[':answer/id']==cid)
  cs.remove(chosen);cs.insert(positions[len(result)%5],chosen)
  seen.add(fp);result.append(r)
 return result

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=SUPPORTED_LEVELS,default='moderate');parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json'],default='json');args=parser.parse_args()
 try:records=batch(args.difficulty,args.count,args.seed)
 except (ValueError,TypeError) as e:parser.error(str(e))
 print(json.dumps(_apply_source_notation(records),indent=2))

from source_notation import install as _install_source_notation, apply as _apply_source_notation
_install_source_notation(globals())

if __name__=='__main__':main()
