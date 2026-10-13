#!/usr/bin/env python3
"""Local column-vector generator, steps 3–7 only, math basis 1356.

Observed nested-column masks retain the shared componentwise solution sentence
and the substitution, evaluated scalar products, collected inner vector, and
final subtraction/addition stages. Raw profiles preserve source attribute
presence (including missing difficulty, fields, solutions and correct refs).
Historical banks have opaque residual-vector recipes: useful replay evidence,
never default learning banks or claimed recovered misconceptions. Normal banks
are complete explicit method operations, selected before parameter sampling.
No DB, engine edits, image models, or plots. See private evidence/README.md.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186059712
KP_UUID='8a21360f-af5f-5730-85b2-b617de30eaf6'
TITLE='Calculating Sums and Scalar Multiplication of Column Vectors'
VERSION='column-vectors-1'
ROOT=Path(__file__).resolve().parent / str(KP_ID)
SOURCE=json.loads((ROOT/'source.json').read_text())
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
OPENING='To compute the result, we just need to perform the required operations with each component separately:'
# outer sign, inner sign, original unit coefficient positions, source notation
TEMPLATES={
 'nested_minus_minus':(-1,-1,1,0,'bmatrix','q-18040'),
 'nested_minus_plus':(-1,1,1,0,'bmatrix','q-18041'),
 'nested_minus_plus_left_scaled':(-1,1,0,1,'aligned','q-70412'),
 'nested_plus_minus':(1,-1,1,0,'aligned','q-70414'),
 'two_vectors':(1,1,1,0,'bmatrix',None),
}
SOURCE_PARAMETERS={
 'q-18040':dict(a=[4,-2],b=[3,3],c=[-8,4],k=1,q=2,r=3),
 'q-18041':dict(a=[1,1],b=[4,1],c=[-1,2],k=1,q=2,r=5),
 'q-70412':dict(a=[4,-7],b=[2,4],c=[4,-6],k=3,q=1,r=4),
 'q-70414':dict(a=[-1,1],b=[2,5],c=[1,2],k=1,q=2,r=2),
}
SOURCE_TEMPLATE={v[-1]:k for k,v in TEMPLATES.items() if v[-1]}
# Historical numerical interpretation is underdetermined. These are residual
# vectors relative to the correct whole vector, not plausible-error assertions.
RESIDUALS={'q-18040':[(0,0),(5,2),(60,-12),(60,0),(0,-12)],
           'q-18041':[(0,-2),(6,24),(1,0),(-2,0),(0,0)]}
NORMAL_PROFILE='authored-component-operations'

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,x))
def matrix(v,style='bmatrix'):
 if style=='bmatrix':return r'\begin{bmatrix}'+str(v[0])+r' \\ '+str(v[1])+r'\end{bmatrix}'
 return r'[\begin{aligned}'+str(v[0])+r' \\ '+str(v[1])+r'\end{aligned}]'
def scale(k,v):return [int(k*x) for x in v]
def add(a,b,s=1):return [int(x+s*y) for x,y in zip(a,b)]
def coefficient(k,symbol):
 if k==1:return symbol
 return ('('+str(k)+')' if k<0 else str(k))+symbol

def expression(t,p):
 o,i,*_=TEMPLATES[t]
 if t=='two_vectors':return 'a'+('+' if o==1 else '-')+coefficient(p['q'],'b')
 space=' ' if TEMPLATES[t][4]=='bmatrix' else ''
 return coefficient(p['k'],'a')+space+('+' if o==1 else '-')+space+'('+coefficient(p['q'],'b')+space+('+' if i==1 else '-')+space+coefficient(p['r'],'c')+')'

def prompt(t,p):
 style=TEMPLATES[t][4]; a,b=matrix(p['a'],style),matrix(p['b'],style);ex=expression(t,p)
 if t=='two_vectors':return f'Let $a = {a}$ and $b = {b}$. Find ${ex}$.'
 c=matrix(p['c'],style)
 if style=='bmatrix':return f'Let $a = {a}$, $b = {b}$ and $c = {c}$. Find ${ex}$.'
 return f'Let $a={a}$, $b={b}$ and $c={c}.$ Find ${ex}.$'

def product(k,v,style):
 m=matrix(v,style)
 return m if k==1 else ('('+str(k)+')' if k<0 else str(k))+r'\cdot '+m

def stages(t,p):
 o,i,*_=TEMPLATES[t];style=TEMPLATES[t][4]; a,b=p['a'],p['b'];q=p['q'];os='+' if o==1 else '-'
 if t=='two_vectors':
  return [matrix(a,style)+os+product(q,b,style),matrix(a,style)+os+matrix(scale(q,b),style),matrix(add(a,scale(q,b),o),style)]
 k,r=p['k'],p['r']; c=p['c'];ins='+' if i==1 else '-';ka,qb,rc=scale(k,a),scale(q,b),scale(r,c);inner=add(qb,rc,i)
 return [product(k,a,style)+os+'('+product(q,b,style)+ins+product(r,c,style)+')',
         matrix(ka,style)+os+'('+matrix(qb,style)+ins+matrix(rc,style)+')',
         matrix(ka,style)+os+matrix(inner,style),matrix(add(ka,inner,o),style)]

def solution(t,p):
 rows=stages(t,p);ex=expression(t,p)
 if TEMPLATES[t][4]=='aligned':
  return OPENING+'\n\n$$\n'+r'\begin{aligned}'+ex+' & ='+rows[0]+''.join(r' \\  & ='+s for s in rows[1:])+r'\end{aligned}'+'\n$$'
 return OPENING+'\n\n$$\n'+r'\begin{aligned}'+'\n'+ex+' &= '+rows[0]+''.join(' '+r'\\'+'\n&= '+s for s in rows[1:])+'\n'+r'\end{aligned}'+'\n$$'

def bank(t,p,profile):
 o,i,*_=TEMPLATES[t];a,b=p['a'],p['b'];q=p['q'];qb=scale(q,b)
 if t=='two_vectors':
  good=add(a,qb,o)
  return [good,add(a,qb,-o),add(a,b,o),add(a,[q*b[0],b[1]],o),add(a,[b[0],q*b[1]],o)],['correct','reverse_sum_sign','omit_scalar','scale_top_only','scale_bottom_only']
 k,r,c=p['k'],p['r'],p['c'];ka,rc=scale(k,a),scale(r,c);inner=add(qb,rc,i);good=add(ka,inner,o)
 if profile.startswith('raw-') or profile.startswith('completed-'):
  sid=profile.split('-',1)[1]
  if sid in RESIDUALS:return [add(good,d) for d in RESIDUALS[sid]],['opaque_residual_'+str(n) for n in range(5)]
 # Whole nested operation mistakes. For the unit-q family omit the k scalar
 # instead; the bank is selected by family before any parameter sampling.
 omitted=add(a,inner,o) if TEMPLATES[t][3] else add(ka,add(b,rc,i),o)
 return [good,add(ka,inner,-o),add(ka,add(qb,rc,-i),o),omitted,add(ka,add(qb,c,i),o)],['correct','reverse_outer_sign','reverse_inner_sign','omit_left_scalar' if TEMPLATES[t][3] else 'omit_b_scalar','omit_c_scalar']

def validate_parameters(level,t,p,raw=False):
 keys={'a','b','q'} if t=='two_vectors' else {'a','b','c','k','q','r'}
 if set(p)!=keys:raise ValueError('Exact parameter keys required: '+str(sorted(keys)))
 for key in keys:
  if key in 'abc':
   if not isinstance(p[key],(list,tuple)) or len(p[key])!=2 or any(type(v)!=int or abs(v)>8 for v in p[key]):raise ValueError('Two integer components of absolute value <=8 required')
   if p[key]==[0,0] or tuple(p[key])==(0,0):raise ValueError('Zero operand vector excluded')
  elif type(p[key])!=int or abs(p[key])>5 or p[key]==0:raise ValueError('Nonzero integer scalar, absolute value <=5 required')
 if raw:
  if level!='moderate':raise ValueError('Source supported working level is moderate')
  if t=='two_vectors':raise ValueError('No raw two-vector source')
  _,_,ku,qu,*_=TEMPLATES[t]
  if (ku and p['k']!=1) or (qu and p['q']!=1):raise ValueError('Raw source mask unit coefficient must remain 1')
  return
 if level=='easy':
  if t!='two_vectors' or not 2<=p['q']<=5:raise ValueError('Easy: two operands and one positive nonunit scale')
 elif level=='moderate':
  if t=='two_vectors':raise ValueError('Moderate requires nested three-operand calculation')
  _,_,ku,qu,*_=TEMPLATES[t]
  if (ku and p['k']!=1) or (not ku and not 2<=p['k']<=5):raise ValueError('Moderate left-scale bound')
  if (qu and p['q']!=1) or (not qu and not 2<=p['q']<=5):raise ValueError('Moderate b-scale bound')
  if not 2<=p['r']<=5:raise ValueError('Moderate c-scale bound')
 elif level=='hard':
  if t=='two_vectors' or any(not 2<=abs(p[x])<=5 for x in ['k','q','r']) or not any(p[x]<0 for x in ['k','q','r']):raise ValueError('Hard requires three nonunit scales, at least one negative')
 else:raise ValueError('Unknown level')
 if not any(v<0 for key in keys if key in 'abc' for v in p[key]):raise ValueError('Signed component arithmetic required')

def sample(level,t,rng):
 p={key:[rng.randint(-8,8),rng.randint(-8,8)] for key in ('ab' if level=='easy' else 'abc')}
 if level=='easy':p['q']=rng.randint(2,5)
 elif level=='moderate':
  _,_,ku,qu,*_=TEMPLATES[t];p.update(k=1 if ku else rng.randint(2,5),q=1 if qu else rng.randint(2,5),r=rng.randint(2,5))
 else:p.update({key:rng.choice([-5,-4,-3,-2,2,3,4,5]) for key in ['k','q','r']})
 return p

# Easy: authored two-vector column sum, two scalar component products.
# Moderate: observed three-vector nested sum, four scalar component products.
# Hard: authored same nested sum, six signed nonunit component products.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ['easy','moderate','hard']:raise ValueError('Unknown difficulty')
 if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('Only observed radio response layout supported')
 rng=random.Random(seed);raw=bool(profile and profile.startswith('raw-'));completed=bool(profile and profile.startswith('completed-'))
 sid=profile.split('-',1)[1] if raw or completed else None
 if sid and sid not in ORIGINALS:raise ValueError('Unknown source profile')
 if profile not in [None,NORMAL_PROFILE] and not sid:raise ValueError('Unknown profile')
 if sid:
  expected=SOURCE_TEMPLATE[sid]
  if template and template!=expected:raise ValueError('Source profile/template mismatch')
  template=expected
 template=template or ('two_vectors' if level=='easy' else rng.choice(list(TEMPLATES)[:4]))
 if template not in TEMPLATES:raise ValueError('Unknown template')
 profile=profile or NORMAL_PROFILE
 # Eligible complete profile/family selected before parameters. Reject the
 # whole instance if any options collide; never replace one failed member.
 for attempt in range(10000):
  p=parameters if parameters is not None else (SOURCE_PARAMETERS[sid] if sid else sample(level,template,rng))
  try:
   validate_parameters(level,template,p,raw or completed)
   values,recipes=bank(template,p,profile)
   if len(set(map(tuple,values)))!=5:raise ValueError('Whole-bank collision')
   break
  except ValueError:
   if parameters is not None or sid:raise
 else:raise RuntimeError('Sampler exhausted')
 q={':question/problem':prompt(template,p)}
 original=ORIGINALS.get(sid,{})
 if not raw or ':question/worked-solution' in original:q[':question/worked-solution']=solution(template,p)
 if not raw or ':question/difficulty' in original:q[':question/difficulty']=':question.difficulty/'+level
 if not raw or ':question/answer-fields' in original:
  field={':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio'}
  style='bmatrix' # original observed options use bmatrix regardless prompt notation
  field[':answer-field/choices']=[{':answer/type':':answer.type/math',':answer/value':matrix(v,style)} for v in values]
  q[':question/answer-fields']=[field]
 else:field=None
 mathematical=task_components(template,p)
 fingerprint=digest(mathematical)
 content=digest({'version':VERSION,'level':q.get(':question/difficulty'),'question':q,'correct':None if raw else values[0] if not sid else _correct(template,p),'presence':sorted(q)})
 q[':question/id']=uid(content)
 if field:
  field[':answer-field/id']=uid(content+'/selection')
  for a in field[':answer-field/choices']:a[':answer/id']=uid(content+'/selection/'+a[':answer/value'])
  if not raw:
   good=matrix(_correct(template,p)); selected=next(a for a in field[':answer-field/choices'] if a[':answer/value']==good)
   field[':answer-field/correct']=[':answer/id',selected[':answer/id']]
  rng.shuffle(field[':answer-field/choices'])
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'source':{k:SOURCE[k] for k in ['database','basis','lineage']},'seed':seed,'level':level,'template':template,'bank_profile':profile,'parameters':p,'parameter_fingerprint':fingerprint,'mathematical_fingerprint':fingerprint,'content_identity':content,'source_id':sid,'evidence_only':raw or completed,'eligible_for_learning':not(raw or completed),'recipe_operations':recipes,'authored_level':level!='moderate','completion':None if raw else {'fields':'inferred radio where absent','correct_ref':'independently derived where absent','solution':'shared source stages where absent'},'domain':{'component_abs_max':8,'scalar_abs_max':5,'whole_bank_rejection':True},'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def task_components(t,p):
 # Fold sign/scalar spellings into the actual coefficient of each supplied
 # vector. Notation, profile, unit-factor aliases, and shuffling are incidental.
 o,i,*_=TEMPLATES[t]
 if t=='two_vectors':return [p['a'],p['b'],1,o*p['q']]
 return [p['a'],p['b'],p['c'],p['k'],o*p['q'],o*i*p['r']]

def _correct(t,p):
 o,i,*_=TEMPLATES[t]
 if t=='two_vectors':return add(p['a'],scale(p['q'],p['b']),o)
 return add(scale(p['k'],p['a']),add(scale(p['q'],p['b']),scale(p['r'],p['c']),i),o)
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(record):
 q=record['question']; g=record['generation'];label=f"Generated {g['level']}"
 if g['evidence_only']:label=f"Evidence profile; working level {g['level']}; original difficulty "+('absent' if ':question/difficulty' not in ORIGINALS[g['source_id']] else 'moderate')
 parts=[f"{label} | {g['template']} | {g['bank_profile']}",q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  parts.extend(f"- ${a[':answer/value']}$" for a in f[':answer-field/choices'])
 if ':question/worked-solution' in q:parts.extend(['',q[':question/worked-solution']])
 return '\n\n'.join(parts)
def main():
 a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile');args=a.parse_args()
 if args.count<1:a.error('--count must be positive')
 records=[generate(level,args.seed+n,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for n in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
