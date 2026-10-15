#!/usr/bin/env python3
"""Solving for a parameter of a no-solution linear equation; finite faithful banks.

One source bank profile is chosen whole. Observed pattern recipes whose error
intent is unknown remain observed patterns, not psychological claims. All three
levels preserve their source backbone. Exact source Pulls are available only in
observed_raw, which is evidence-only and excluded from the finite served domain.
"""
import argparse, copy, hashlib, importlib.util, itertools, json, random, re, sys, uuid
from functools import lru_cache
from pathlib import Path
import sympy as sp

HERE=Path(__file__).with_suffix('')
KP_ID=17592186204090
KP_UUID='c0e7426e-553d-5f20-811f-15f3a5ea0056'
TITLE='Solving For an Unknown Parameter'
VERSION='no-solution-parameter-v1'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION))
LEVELS=('easy','moderate','hard');SUPPORTED_LEVELS=LEVELS
FROZEN=json.loads((HERE/'source.json').read_text())
CASES={q[':question/math-academy-id']:q for q in FROZEN['record'][':knowledge-point/questions']}
_fmt=importlib.util.spec_from_file_location('_parameter_frozen_math_format',HERE/'math_format.py')
fmt=importlib.util.module_from_spec(_fmt);_fmt.loader.exec_module(fmt)
C_VALUES=tuple(i for i in range(-7,8) if abs(i)>=2)
B_VALUES=tuple(i for i in range(-10,11) if abs(i)>=2)
S_VALUES=tuple(i for i in range(-9,10) if i)
# Every profile's exact source value pattern is retained, including unresolved
# transformations; these are observed numeric recipes, not inferred distractors.
PROFILES={
 'q-287665':('easy',('0','b','1/c','1','c')),
 'q-288135':('easy',('0','c','b','1/abs(b)','-1/c')),
 'q-288107':('easy',('c','abs(b)','0','1','1/c')),
 'q-288593':('moderate',('1/b','-b','b/2','-s','0')),
 'q-288596':('moderate',('1/s','b','-s','-b','-1/b')),
 'q-288143':('hard',('0','c','-c','s','-s')),
 'q-288144':('hard',('c/s','b','-1/c','-s','c')),
}
DEFAULTS={
 'q-287665':{'c':2,'s':0,'b':3},'q-288135':{'c':4,'s':0,'b':-2},
 'q-288107':{'c':5,'s':0,'b':-4},'q-288593':{'c':1,'s':-1,'b':4},
 'q-288596':{'c':1,'s':9,'b':-6},'q-288143':{'c':-3,'s':4,'b':6},
 'q-288144':{'c':-5,'s':-9,'b':10},
}
LABELS={'q-287665':('x','p'),'q-288135':('y','p'),'q-288107':('t','q'),
 'q-288593':('y','q'),'q-288596':('y','q'),'q-288143':('x','q'),'q-288144':('z','p')}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(parent,text):return str(uuid.uuid5(uuid.UUID(parent),text))
def tex(x):
 x=sp.Rational(x)
 return ('-' if x<0 else '')+(str(abs(x.p)) if x.q==1 else rf'\frac{{{abs(x.p)}}}{{{x.q}}}')

def parameters(level,p):
 if level not in LEVELS:raise ValueError('Unknown difficulty')
 if not isinstance(p,dict) or set(p)!={'c','s','b'} or any(type(p[k]) is not int for k in p):raise ValueError('Exactly integer c,s,b required')
 c,s,b=(p[k] for k in ('c','s','b'))
 if b not in B_VALUES:raise ValueError('Nonzero RHS integer with magnitude 2..10 required')
 if level=='easy' and (c not in C_VALUES or s!=0):raise ValueError('Easy: c magnitude 2..7, no shift')
 if level=='moderate' and (c!=1 or s not in S_VALUES):raise ValueError('Moderate: unit multiplier, nonzero shift magnitude 1..9')
 if level=='hard' and (c not in C_VALUES or s not in S_VALUES):raise ValueError('Hard: multiplier magnitude 2..7 and nonzero shift magnitude 1..9')
 return dict(p)

def bank(profile,p):
 if profile not in PROFILES:raise ValueError('Unknown whole-bank profile')
 c,s,b=map(sp.Integer,(p['c'],p['s'],p['b']))
 vals=[]
 for recipe in PROFILES[profile][1]:
  vals.append(sp.sympify(recipe,locals={'c':c,'s':s,'b':b,'abs':sp.Abs},rational=True))
 if any(not v.is_Rational or not v.is_finite for v in vals) or len(set(vals))!=5 or vals.count(-s)!=1:raise ValueError('Invalid complete bank: collision or ambiguous correct value')
 return vals

@lru_cache(None)
def domain(level,profile):
 if profile not in PROFILES or PROFILES[profile][0]!=level:raise ValueError('Bank profile belongs to another difficulty')
 cs=C_VALUES if level!='moderate' else (1,)
 ss=(0,) if level=='easy' else S_VALUES
 out=[]
 for c,s,b in itertools.product(cs,ss,B_VALUES):
  p={'c':c,'s':s,'b':b}
  try:bank(profile,p)
  except ValueError:continue
  out.append((c,s,b))
 return tuple(out)

def fingerprint(level,p):
 # Ignore variable letters, profile, option order, seed and uniform equation scale.
 return digest([level,str(sp.Rational(p['c'],p['b'])),p['s']])

def coefficient(level,p,letter):
 c,s=p['c'],p['s']
 shift=letter+('+'+str(s) if s>0 else str(s)) if s else letter
 return (str(c)+letter) if level=='easy' else ('('+shift+')' if level=='moderate' else str(c)+'('+shift+')')

def render(level,profile,p):
 x,r=LABELS[profile];c,s,b=(p[k] for k in ('c','s','b'));a=coefficient(level,p,r)
 problem=f'Consider the equation in the variable ${x},$ given by\n\n$$\n{a}{x}={b}\n$$\n\nwhere ${r}$ is a constant. Given that this equation has no solution, what is the value of ${r}?$'
 solution='Suppose we have an equation of the form\n\n$$\nax=b\n$$\n\nwhere $a$ and $b$ are constants, and $b\\ne 0.$ If $a=0,$ then the equation has no solution.\n\n'+f'Notice that this equation is in the form $a{x}=b.$ In this case,\n\n$$\na={a},\\,b={b}.\n$$\n\nTherefore, the equation has no solution if\n\n$$\n{a}=0.\n$$\n\nSolving this for ${r},$ we get\n\n$$\n'
 shift=r+('+'+str(s) if s>0 else str(s))
 if level=='easy':solution+=f'{r}=0.'
 elif level=='moderate':solution+=rf'\begin{{aligned}}{shift} &=0 \\ {r} &={-s}.\end{{aligned}}'
 else:solution+=rf'\begin{{aligned}}{a} &=0 \\ \frac{{{a}}}{{{c}}} &=\frac{{0}}{{{c}}} \\ {shift} &=0 \\ {r} &={-s}.\end{{aligned}}'
 solution+='\n$$'
 return problem,solution

@fmt.checked_math_content
def generate(difficulty='easy',seed=0,template=None,parameters=None,profile=None):
 if difficulty not in LEVELS or type(seed) is not int:raise ValueError('Supported level and integer seed required')
 if template is not None and profile is not None and template!=profile:raise ValueError('Template and bank profile disagree')
 profile=profile or template
 rng=random.Random(seed)
 if profile is None:profile=rng.choice([sid for sid,(level,_) in PROFILES.items() if level==difficulty])
 if profile not in PROFILES or PROFILES[profile][0]!=difficulty:raise ValueError('Unknown or cross-level profile')
 if parameters is None:
  c,s,b=rng.choice(domain(difficulty,profile));p={'c':c,'s':s,'b':b}
 else:p=globals()['parameters'](difficulty,parameters)
 if tuple(p[k] for k in ('c','s','b')) not in domain(difficulty,profile):raise ValueError('Parameters outside valid bounded whole-bank domain')
 values=bank(profile,p);source=CASES[profile]
 if p==DEFAULTS[profile]:problem,solution=source[':question/problem'],source[':question/worked-solution']
 else:problem,solution=render(difficulty,profile,p)
 problem,solution=fmt.normalize_prose(problem),fmt.normalize_prose(solution)
 # Match original value spellings at the observed parameters, normalize format.
 raw_values=[a[':answer/value'] for a in source[':question/answer-fields'][0][':answer-field/choices']] if p==DEFAULTS[profile] else [tex(v) for v in values]
 raw_values=[fmt.normalize_tex(v) for v in raw_values]
 qid=ident(GENERATOR_UUID,digest([difficulty,p,profile,problem,solution,raw_values]));fid=ident(qid,'selection')
 answers=[{':answer/id':ident(fid,v),':answer/type':':answer.type/math',':answer/value':v} for v in raw_values]
 f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[values.index(-p['s'])][':answer/id']]}
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[f]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':GENERATOR_UUID,'generator_version':VERSION,'seed':seed,'parameters':p,'template':profile,'bank_profile':profile,'bank_origin':'observed_expression_patterns; distractor psychology unresolved','source_question_id':source[':question/id'],'source_math_academy_id':profile,'source_basis':FROZEN['basis'],'source_lineage':FROZEN['lineage'],'dependencies':{'sympy':sp.__version__},'mathematical_fingerprint':fingerprint(difficulty,p),'evidence_only':False,'eligible':True,'assets':[]}}

def observed_raw(source_id,parameters):
 if source_id not in CASES or parameters!=DEFAULTS[source_id] or any(type(v) is not int for v in parameters.values()):raise ValueError('Exact original MA ID and original parameters required')
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':copy.deepcopy(CASES[source_id]),'generation':{'template':'observed_raw','source_math_academy_id':source_id,'source_basis':FROZEN['basis'],'source_lineage':FROZEN['lineage'],'parameters':copy.deepcopy(parameters),'evidence_only':True,'eligible':False}}

@lru_cache(None)
def inventory(level):
 if level not in LEVELS:raise ValueError('Unknown difficulty')
 out={}
 for profile,(lev,_) in PROFILES.items():
  if lev!=level:continue
  for c,s,b in domain(level,profile):
   p={'c':c,'s':s,'b':b};fp=fingerprint(level,p)
   # Whole profiles vary without claiming a different bank is a new math task.
   if fp not in out or int(fp[:8],16)%2:out[fp]=(profile,c,s,b)
 return tuple(out.values())

def capacity(level='all'):
 if level=='all':return {lev:len(inventory(lev)) for lev in LEVELS}
 return len(inventory(level))

def batch(difficulty,count,seed=0):
 if difficulty not in (*LEVELS,'all') or type(count) is not int or count<0 or type(seed) is not int:raise ValueError('Bounded level, nonnegative integer count and integer seed required')
 levels=LEVELS if difficulty=='all' else (difficulty,)
 candidates=[(lev,p) for lev in levels for p in inventory(lev)]
 if count>len(candidates):raise ValueError(f'Finite substantive capacity {len(candidates)} exceeded')
 random.Random(seed).shuffle(candidates)
 return [generate(lev,seed,profile=profile,parameters={'c':c,'s':s,'b':b}) for lev,(profile,c,s,b) in candidates[:count]]

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--count',type=int,default=9);ap.add_argument('--seed',type=int,default=204090);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--capacity',action='store_true');args=ap.parse_args()
 if args.capacity:print(json.dumps(capacity(args.difficulty),indent=2));return
 try:records=batch(args.difficulty,args.count,args.seed)
 except ValueError as e:ap.error(str(e))
 print(json.dumps({'instances':records},indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
