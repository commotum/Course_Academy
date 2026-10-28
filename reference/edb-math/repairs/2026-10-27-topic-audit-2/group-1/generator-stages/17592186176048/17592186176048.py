#!/usr/bin/env python3
"""Cosine periodicity generator, captured math basis 1356.

All observed radio banks are public profiles. Source recipes describe complete
observed expression patterns, not recovered author intent. Default banks are
separately authored operation banks. observed_raw_q103242 deliberately preserves
its ambiguous duplicated source options as evidence; it is not learner eligible.
Unrated questions receive supported authored levels and worked solutions.
See the adjacent extraction, classification, validation and review evidence.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import random
import uuid
import sympy as sp
from math_format import normalize_prose,normalize_tex

KP_ID=17592186176048
KP_UUID='1c25c3a0-083a-55d5-b688-7347bfafaa9e'
TITLE='Utilizing the Periodicity Property of the Cosine Function'
VERSION='cosine-periodicity-1-format-audit-9122-v1'
ROOT=Path(__file__).with_suffix('')
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES={
 'direct':{'level':'moderate','style':'standard','sources':['q-103242','q-103243']},
 'direct_short':{'level':'moderate','style':'short','sources':['q-70671','q-70672']},
 'affine':{'level':'hard','style':'standard','sources':['q-103279']},
 'legacy_direct':{'level':'moderate','style':'legacy','sources':['q-65179']},
 'legacy_affine':{'level':'hard','style':'legacy','sources':['q-65176']},
 'easy_direct':{'level':'easy','style':'standard','sources':[]},
}
CASES=[
 ('q-65176','hard','legacy_affine',{'c':'sqrt(3)/2','n':-3,'a':4,'b':-1}),
 ('q-65179','moderate','legacy_direct',{'c':'-1/sqrt(3)','n':5,'a':1,'b':0}),
 ('q-103242','moderate','direct',{'c':'-5/8','n':6,'a':1,'b':0}),
 ('q-103243','moderate','direct',{'c':'sqrt(2)/3','n':-7,'a':1,'b':0}),
 ('q-103279','hard','affine',{'c':'3/8','n':-5,'a':4,'b':5}),
 ('q-70671','moderate','direct_short',{'c':'1/2','n':-5,'a':1,'b':0}),
 ('q-70672','moderate','direct_short',{'c':'sqrt(3)/3','n':8,'a':1,'b':0}),
]
PROFILES={f'observed_{s[0].replace("-","")}':s[2] for s in CASES}
PROFILES['observed_raw_q103242']='direct'
PROFILES.update({'authored_direct':None,'authored_affine':None})

def tex(e):
 return sp.latex(sp.sympify(e)).replace('- ','-')

def signed(v,render=tex):
 return ('+' if v>=0 else '-')+render(abs(v))

def angle(n, pi=r'\pi ',spaces=False):
 sign='+' if n>0 else '-'
 if spaces: return 'x '+sign+' '+str(abs(2*n))+pi
 return 'x'+sign+str(abs(2*n))+pi

def target(cos,n,a,b,pi=r'\pi ',spaces=False):
 term=('' if a==1 else '-' if a==-1 else str(a))+cos+'('+angle(n,pi,spaces)+')'
 return term+('' if b==0 else signed(b))

def parameters(level,p,profile):
 if set(p)!= {'c','n','a','b'}: raise ValueError('Require c,n,a,b exactly')
 c=sp.sympify(p['c']); n,a,b=(p[k] for k in ('n','a','b'))
 if c.free_symbols or c.is_real is not True or abs(c)>1 or c==0: raise ValueError('Require real nonzero exact cosine value with |c|<=1')
 if any(type(v) is not int for v in (n,a,b)) or n==0: raise ValueError('Integer nonzero period shift required')
 if level=='easy':
  if not 1<=abs(n)<=2 or (a,b)!=(1,0) or c not in EASY_VALUES: raise ValueError('Easy: familiar value, one/two periods, direct only')
 elif level=='moderate':
  if not 3<=abs(n)<=10 or (a,b)!=(1,0): raise ValueError('Moderate: 3..10 periods, direct only')
 elif level=='hard':
  if not 2<=abs(n)<=10 or not 2<=abs(a)<=6 or not 1<=abs(b)<=6: raise ValueError('Hard: affine with nonunit scale, nonzero offset')
 else: raise ValueError('Unknown difficulty')
 if c.is_Rational and c.q>12: raise ValueError('Rational denominator at most twelve')
 if not c.is_Rational and c not in RADICAL_VALUES: raise ValueError('Supported small exact radicals only')
 return c,n,a,b

EASY_VALUES=tuple(sp.sympify(x) for x in ['-1','1','-1/2','1/2','sqrt(2)/2','-sqrt(2)/2','sqrt(3)/2','-sqrt(3)/2'])
RADICAL_VALUES=tuple(sp.sympify(x) for x in ['sqrt(2)/2','-sqrt(2)/2','sqrt(3)/2','-sqrt(3)/2','sqrt(2)/3','-sqrt(2)/3','sqrt(3)/3','-sqrt(3)/3','1/sqrt(3)','-1/sqrt(3)'])
MOD_VALUES=tuple(sorted({sp.Rational(i,j) for j in range(3,13) for i in range(-j+1,j) if i!=0}|set(RADICAL_VALUES),key=str))

def sample(level,rng):
 c=rng.choice(EASY_VALUES if level=='easy' else MOD_VALUES)
 n=rng.choice([-1,1])*rng.randint(1 if level=='easy' else 3 if level=='moderate' else 2,2 if level=='easy' else 10)
 a,b=(rng.choice([-1,1])*rng.randint(2,6),rng.choice([-1,1])*rng.randint(1,6)) if level=='hard' else (1,0)
 return {'c':str(c),'n':n,'a':a,'b':b}

def bank(profile,c,n,a,b):
 """Complete eligible banks; no pooled distractor selection or lookup values."""
 result=a*c+b
 if profile=='authored_direct': return [c,-c,c+2*sp.pi,c-2*sp.pi,-c+2*sp.pi]
 if profile=='authored_affine': return [result,-a*c+b,a*c-b,c+b,a*(c+b)]
 if profile=='observed_q65176': return [-c,result,c+2*n,-c-b,-a*c/2-b]
 if profile=='observed_q65179': return [-1/c,-1-c,1/c,c,-c]
 if profile in ('observed_q103242','observed_raw_q103242'):
  return [-c,sp.pi+c+2/sp.Integer(c.q),c+2*sp.pi,2*sp.pi+c if 'raw' in profile else c-2*sp.pi,c]
 if profile=='observed_q103243':
  d=sp.denom(c); return [-c,c,c-2*sp.pi,d*c+d,2*sp.pi-c]
 if profile=='observed_q103279': return [result,result/a,-result,2*sp.pi+a*c,2*sp.pi-2*c]
 if profile=='observed_q70671': return [c,c+2*n*sp.pi,c-2*sp.pi,-c,-c-2*n*sp.pi]
 if profile=='observed_q70672': return [c,c+2*sp.pi,-c+2*n*sp.pi,-c,c+2*n*sp.pi]
 raise ValueError('Unknown profile')

def source_presentation(template,c,n,a,b):
 """Full source stages; standard and short layouts are separate templates."""
 style=TEMPLATES[template]['style']; cs=tex(c); cos='cos⁡'; shift=angle(n); tr=target(cos,n,a,b)
 if style=='legacy':
  shown=tex(abs(c))
  if template=='legacy_direct' and sp.simplify(abs(c)-1/sp.sqrt(3))==0: shown=r'\frac{1}{\sqrt{3}}'
  legacy_target=target(r'\cos ',n,a,0,'π',True)+('' if b==0 else (' + ' if b>0 else ' - ')+str(abs(b)))
  prompt='If $\\cos x ='+('-' if c<0 else ' ')+shown+'$, then $'+legacy_target+' =$'
 else:
  prompt='If $'+cos+'x='+cs+('$ for some $x$, then $' if style=='short' else ',$ then $')+tr+'=$'
 prefix='The period of $y='+cos+'x$ is $2\\pi .$ Therefore, for '+('any integer' if style=='short' or style=='legacy' else 'an integer')+' $n$ we have\n\n$$\n'+cos+'x='+cos+'(x+2n\\pi ).\n$$\n\n'
 ns=str(n) if n>0 else '('+str(n)+')'
 sentence='Substituting $n='+str(n)+'$ into the right-hand-side'+(' gives' if style=='short' else ' of the above gives')+'\n\n$$\n'
 reduction=cos+'x='+('' if style=='short' else cos+'(x+2\\cdot '+ns+'\\cdot \\pi )=')+cos+'('+shift+').'
 solution=prefix+sentence+'\\begin{aligned}'+reduction+'\\end{aligned}\n$$\n\nTherefore, if $'+cos+'x='+cs+',$ then $'+cos+'('+shift+')='+cs+'.$'
 if a!=1 or b!=0:
  solution+='\n\nFinally, then\n\n$$\n\\begin{aligned}'+tr+' & ='+str(a)+'('+cs+')'+signed(b)+' \\\\  & ='+tex(a*c)+signed(b)+' \\\\  & ='+tex(a*c+b)+'.\\end{aligned}\n$$'
 return prompt,solution

def hash_data(x): return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(x): return str(uuid.uuid5(uuid.UUID(KP_UUID),x))

# Stable package identity; registration reuses any existing KP reference.
GENERATOR_UUID=uid('question-generator')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if field_type not in (None,'radio'): raise ValueError('Only radio layout is supported')
 if profile not in (None,*PROFILES): raise ValueError('Unknown bank profile')
 if profile and PROFILES[profile]:
  if template and template!=PROFILES[profile]: raise ValueError('Profile/template mismatch')
  template=PROFILES[profile]
 template=template or {'easy':'easy_direct','moderate':'direct','hard':'affine'}.get(level)
 if template not in TEMPLATES or TEMPLATES[template]['level']!=level: raise ValueError('Template/difficulty mismatch')
 profile=profile or ('authored_affine' if level=='hard' else 'authored_direct')
 if profile.startswith('authored_') and (profile=='authored_affine')!=(level=='hard'): raise ValueError('Profile workload mismatch')
 rng=random.Random(seed)
 for _ in range(256):
  p=dict(parameters) if parameters is not None else sample(level,rng)
  c,n,a,b=globals()['parameters'](level,p,profile)
  if profile in ('observed_q103242','observed_raw_q103242') and not c.is_Rational:
   if parameters is not None: raise ValueError('Observed rational bank requires rational c')
   continue
  vals=list(map(sp.simplify,bank(profile,c,n,a,b))); correct=a*c+b
  collision=any(sp.simplify(x-y)==0 for i,x in enumerate(vals) for y in vals[:i])
  if collision and profile!='observed_raw_q103242':
   if parameters is not None: raise ValueError('Whole bank rejected: equivalent options')
   continue
  if sum(sp.simplify(v-correct)==0 for v in vals)!=1: raise ValueError('Bank lacks unique correct choice')
  prompt,solution=source_presentation(template,c,n,a,b)
  if not profile.startswith('observed_'): prompt=prompt.replace('cos⁡',r'\cos '); solution=solution.replace('cos⁡',r'\cos ')
  values=[tex(v) for v in vals]
  if profile=='observed_raw_q103242': values[3]=r'2\pi '+signed(c)
  if profile!='observed_raw_q103242':prompt=normalize_prose(prompt);solution=normalize_prose(solution);values=[normalize_tex(v)for v in values]
  content=hash_data([VERSION,prompt,solution,sorted(values)])
  # Equivalent full-period angles are one mathematical task. Shift count,
  # value aliases, template/profile/variable spelling do not inflate diversity.
  # The full displayed angle is still retained in content identity and checked.
  fingerprint=hash_data({'c':sp.srepr(c),'reduced_angle':'x','a':a,'b':b})
  qid=uid(content); fid=uid(content+':selection')
  answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
  correct_id=next(ans[':answer/id'] for ans,v in zip(answers,vals) if sp.simplify(v-correct)==0)
  rng.shuffle(answers)
  return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
   'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]},
   'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':{'c':str(c),'n':n,'a':a,'b':b},'bank_profile':profile,'bank_origin':'observed' if profile.startswith('observed_') else 'authored','source_analysis':SOURCE,'parameter_fingerprint':fingerprint,'content_fingerprint':content,'plot_rating':'none','plot_assets':{},'raw_source_error':profile=='observed_raw_q103242','mathematical_repair':profile=='observed_q103242','authored_level':level=='easy' or template.startswith('legacy'),'solution_origin':'authored_missing_source' if template.startswith('legacy') or level=='easy' else 'observed_template','sympy_version':sp.__version__}}
 raise ValueError('No eligible complete bank within bounded sampler')

# EASY: missing-source authored direct reduction, familiar value, ±1/±2 periods.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: observed direct reduction of ±3..±10 periods; short/full row layouts.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: same periodic reduction, followed by one nonunit multiplication and sum.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question']; f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

def main():
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all'); ap.add_argument('--seed',type=int,default=0); ap.add_argument('--count',type=int,default=1); ap.add_argument('--format',choices=['markdown','json'],default='markdown'); ap.add_argument('--template',choices=list(TEMPLATES)); ap.add_argument('--profile',choices=list(PROFILES)); args=ap.parse_args()
 if args.count<1 or args.difficulty=='all' and (args.template or args.profile): ap.error('Positive count and specific difficulty required with template/profile')
 if args.difficulty in ('easy','all') and args.count>len(EASY_VALUES):
  ap.error(f'easy: finite capability limit of {len(EASY_VALUES)} distinct tasks; requested {args.count}.')
 records=[];seen=set()
 for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]):
  produced=0
  for i in range(max(512,args.count*32)):
   r=generate(level,args.seed+i,args.template,profile=args.profile)
   fp=r['generation']['parameter_fingerprint']
   if fp in seen: continue
   records.append(r);seen.add(fp);produced+=1
   if produced==args.count: break
  if produced<args.count:
   ap.error(f'{level}: bounded capability limit; requested {args.count}, found {produced} distinct tasks. Period shifts, seed and bank order do not create extra tasks.')
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__': main()
