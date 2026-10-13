#!/usr/bin/env python3
"""Deterministic perpendicular-line selection (steps 3–7, local review only).

All banks are complete profiles. Observed profiles reproduce the captured
arithmetic components, including a quarantined malformed quadratic bank. Normal
sampling uses explicitly authored, method-derived line banks. No source answer
lookup or literal-payload replay is used; correctness is computed from slopes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import random
import uuid
import sympy as sp

KP_ID = 17592186110599
KP_UUID = '29005c66-9f30-5862-926f-8a09320d404c'
TITLE = 'Determining Whether Two Lines in Slope-Intercept Form are Perpendicular'
VERSION = '1.0.0'
EVIDENCE = Path(__file__).with_suffix('')
SOURCE = {'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
NS = uuid.UUID(KP_UUID)
TEMPLATES = {'compact':'Source question mark inside math', 'spaced':'Unrated source question mark outside math'}
# Formula names map to full mathematical objects; intercepts are independently
# specified components because the source does not identify their error intent.
PROFILES = {
 'observed-q-72453': {'level':'easy','template':'spaced','ops':['m','minus_one','neg_m','reciprocal','negative_reciprocal'], 'styles':['coefficient']*5,'spacing':'legacy','origin':'observed','source':'q-72453'},
 'observed-q-72525': {'level':'moderate','template':'spaced','ops':['reciprocal','neg_m','m','one','negative_reciprocal'], 'styles':['coefficient','x_fraction','x_fraction','coefficient','coefficient'],'spacing':'legacy','origin':'observed','source':'q-72525','prompt_style':'x_fraction'},
 'observed-q-215888': {'level':'easy','template':'compact','ops':['m','negative_half_m','negative_half_m','negative_reciprocal','m'], 'styles':['coefficient']*5,'spacing':'compact','origin':'observed','source':'q-215888'},
 'observed-q-215890': {'level':'easy','template':'compact','ops':['m','negative_reciprocal','double_m','negative_double_m','m'], 'styles':['coefficient']*5,'spacing':'compact','origin':'observed','source':'q-215890'},
 'observed-q-72524': {'level':'moderate','template':'compact','ops':['one','reciprocal','quadratic_m','quadratic_m','negative_reciprocal'], 'styles':['coefficient','coefficient','x_fraction','x_fraction','coefficient'],'spacing':'compact','origin':'observed','source':'q-72524','prompt_style':'x_fraction','evidence_only':True},
 'repaired-q-72524': {'level':'moderate','template':'compact','ops':['one','reciprocal','m','m','negative_reciprocal'], 'styles':['coefficient','coefficient','x_fraction','x_fraction','coefficient'],'spacing':'compact','origin':'authored source repair','source':'q-72524','prompt_style':'x_fraction'},
 'observed-q-72527': {'level':'easy','template':'compact','ops':['negative_reciprocal','m','horizontal','reciprocal','neg_m'], 'styles':['coefficient']*5,'spacing':'compact','origin':'observed','source':'q-72527'},
 'observed-q-72528': {'level':'easy','template':'compact','ops':['m','negative_reciprocal','reciprocal','neg_m','horizontal'], 'styles':['coefficient']*5,'spacing':'compact','origin':'observed','source':'q-72528'},
}
for _level in ('easy','moderate','hard'):
 PROFILES['authored-'+_level] = {'level':_level,'template':'compact','ops':['m','neg_m','reciprocal','negative_reciprocal','horizontal'],'styles':['coefficient']*5,'spacing':'compact','origin':'authored method bank'}


def rational(value):
 if isinstance(value,bool) or isinstance(value,float): raise ValueError('Use exact integer or rational-string parameters')
 try: result=sp.Rational(value)
 except Exception as exc: raise ValueError('Invalid rational') from exc
 if not result.is_finite: raise ValueError('Finite rationals required')
 return result


def tex(value):
 v=rational(value); sign='-' if v<0 else '';v=abs(v)
 return sign+(str(v.p) if v.q==1 else r'\frac{'+str(v.p)+'}{'+str(v.q)+'}')


def xterm(m,style='coefficient'):
 m=rational(m)
 if m==0:return ''
 sign='-' if m<0 else '';a=abs(m)
 if a==1:return sign+'x'
 if style=='x_fraction' and a.p==1 and a.q>1:return sign+r'\frac{x}{'+str(a.q)+'}'
 return tex(m)+'x'


def line(m,b,style='coefficient',spacing='compact',quadratic=False):
 m,b=rational(m),rational(b)
 term=xterm(m,style)
 if quadratic: term+='x'
 if not term: rhs=tex(b)
 else:
  rhs=term
  if b: rhs+=(' + ' if b>0 else ' - ') + tex(abs(b)) if spacing!='compact' else ('+' if b>0 else '-')+tex(abs(b))
 if spacing=='compact':return 'y='+rhs
 return ('y = ' if m>=0 else 'y =')+rhs


def operation(name,m):
 return {'m':m,'neg_m':-m,'one':sp.S.One,'minus_one':-sp.S.One,
         'reciprocal':1/m,'negative_reciprocal':-1/m,'horizontal':sp.S.Zero,
         'negative_half_m':-m/2,'double_m':2*m,'negative_double_m':-2*m,'quadratic_m':m}[name]


def canonical_parameters(p):
 if set(p)!={'m','b','intercepts'}:raise ValueError('Parameters require exactly m, b, and five intercepts')
 if not isinstance(p['intercepts'],(list,tuple)) or len(p['intercepts'])!=5:raise ValueError('Exactly five intercepts required')
 return {'m':str(rational(p['m'])),'b':str(rational(p['b'])),'intercepts':[str(rational(v)) for v in p['intercepts']]}


def validate_parameters(level,p,profile):
 m=rational(p['m']);b=rational(p['b']);ints=[rational(v) for v in p['intercepts']]
 if not m or abs(m)>12 or m.q>12 or abs(b)>20 or b.q>12 or any(abs(v)>30 or v.q>12 for v in ints):raise ValueError('Parameters outside exact slope/intercept bounds')
 if level=='easy' and m.q!=1:raise ValueError('Easy slopes are integers')
 if level=='moderate' and (abs(m.p)!=1 or not 2<=m.q<=12):raise ValueError('Moderate slopes are signed unit fractions')
 if level=='hard' and (not 2<=abs(m.p)<=9 or not 2<=m.q<=9 or abs(m)==1):raise ValueError('Hard slopes have coprime non-unit numerator and denominator 2..9')
 if profile.startswith('authored-') and (abs(m)==1 or b.q!=1 or any(v.q!=1 for v in ints)):raise ValueError('Authored defaults use non-unit slopes and integer intercepts')
 if profile in ('observed-q-215888','observed-q-215890') and abs(m)!=1:raise ValueError('Unit-slope observed profiles require |m|=1')


def sample(level,rng,profile):
 if profile in ('observed-q-215888','observed-q-215890'):m=rng.choice([-1,1])
 elif level=='easy':m=rng.choice([-1,1])*rng.randint(2,12)
 elif level=='moderate':m=sp.Rational(rng.choice([-1,1]),rng.randint(2,12))
 else:
  eligible=[sp.Rational(s*n,d) for s in (-1,1) for n in range(2,10) for d in range(2,10) if math.gcd(n,d)==1]
  m=rng.choice(eligible)
 return {'m':str(m),'b':str(rng.randint(-12,12)),'intercepts':[str(rng.randint(-12,12)) for _ in range(5)]}


def solution(prompt_line,correct_line,m):
 c=-1/m
 a='(-1)' if m==-1 else tex(m)
 b='(-1)' if c==-1 else tex(c)
 return ('For the two lines to be perpendicular, their slopes must multiply to $-1.$\n\n'
  f'The line ${prompt_line}$ is in slope-intercept form, and its slope is ${tex(m)}.$\n\n'
  f'Looking at the answer choices, the line ${correct_line}$ has a slope of ${tex(c)}.$\n\n'
  'Multiplying the slopes together, we have\n\n$$\n'+a+r'\cdot '+b+'=-1.\n$$\n\n'
  f'Since the slopes multiply to $-1,$ we conclude that the line ${correct_line}$ is perpendicular to the given line.')


def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def assemble(level,seed,template,p,profile):
 spec=PROFILES[profile];m=rational(p['m']);b=rational(p['b'])
 spacing=spec['spacing'];prompt_line=line(m,b,spec.get('prompt_style','coefficient'),spacing)
 # Spaced original prompts include a space after '=' even for negative slopes.
 if template=='spaced':prompt_line=prompt_line.replace('y =-','y = -')
 prompt='Which of the following lines is perpendicular to $'+prompt_line+('?$' if template=='compact' else '$?')
 options=[];math_values=[];correct_values=[]
 for index,(op,style,intercept) in enumerate(zip(spec['ops'],spec['styles'],p['intercepts'],strict=True)):
  slope=operation(op,m);quadratic=op=='quadratic_m'
  value=line(slope,intercept,style,spacing,quadratic)
  # The legacy q72525 bank explicitly writes x/2; the legacy q72453
  # bank writes the coefficient 1/3. These are complete slot renderers.
  poly=sp.expand(slope*sp.Symbol('x')**(2 if quadratic else 1)+rational(intercept))
  math_values.append(str(poly))
  options.append(value)
  if not quadratic and m*slope==-1:correct_values.append(value)
 if len(set(math_values))!=5 or len(correct_values)!=1:raise ValueError('Reject complete bank: duplicate objects or ambiguous perpendicular choice')
 worked=solution(prompt_line,correct_values[0],m)
 # Mathematical identity is the assessed negative reciprocal of the target
 # slope alone. All displayed banks and intercepts belong to content identity.
 task={'target_slope':str(m)}
 pf=digest(task)
 cf=digest({'version':VERSION,'level':level,'template':template,'profile':profile,'parameters':p,'prompt':prompt,'solution':worked,'bank':sorted(options)})
 qid=str(uuid.uuid5(NS,cf));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in options]
 correct=next(a[':answer/id'] for a in answers if a[':answer/value']==correct_values[0])
 random.Random(seed).shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
  'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,
   ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},
  'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'bank_origin':spec['origin'],
   'parameter_fingerprint':pf,'content_fingerprint':cf,'source_analysis':{**SOURCE,'question_ids':[spec['source']] if 'source' in spec else [],'canonical_example':'e-14359'},
   'authored_extension':spec['origin']!='observed','evidence_only':spec.get('evidence_only',False),
   'source_repair':'remove duplicated x from two quadratic distractors' if profile=='repaired-q-72524' else None,
   'correct_designation_origin':'mathematically derived; absent in capture/widget' if profile in ('observed-q-72453','observed-q-72525') else 'computed from displayed slopes',
   'distractor_recipes':[{'operation':op,'slope':str(operation(op,m)),'intercept':v,'power':2 if op=='quadratic_m' else 1,'intercept_intent':'independent component; historical intent unresolved'} for op,v in zip(spec['ops'],p['intercepts'],strict=True)],
   'plot_rating':'none','plot_assets':{},'domain':'nonvertical slope-intercept equations; target slope nonzero',
   'worked_stages':[{'operation':'read slope','value':str(m)},{'operation':'negative reciprocal','value':str(-1/m)},{'operation':'multiply slopes','value':'-1'}]}}


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio fields are supported')
 profile=profile or 'authored-'+level
 if profile not in PROFILES or PROFILES[profile]['level']!=level:raise ValueError('Profile does not belong to difficulty')
 spec=PROFILES[profile];template=template or spec['template']
 if template!=spec['template']:raise ValueError('Profile/template mismatch')
 rng=random.Random(seed)
 for _ in range(128):
  p=canonical_parameters(parameters if parameters is not None else sample(level,rng,profile))
  validate_parameters(level,p,profile)
  try:return assemble(level,seed,template,p,profile)
  except ValueError:
   if parameters is not None:raise
 raise ValueError('No eligible complete bank after bounded sampling')

# EASY — read an integer slope and recognize its negative reciprocal.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — read a signed unit-fraction slope and recognize its negative reciprocal.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — authored non-unit rational slopes; same recognition and product check.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)


def markdown(record):
 q,g=record['question'],record['generation'];f=q[':question/answer-fields'][0]
 correct=f[':answer-field/correct'][1]
 out=[f"## {q[':question/difficulty'].split('/')[-1]} — {g['bank_profile']}",'',q[':question/problem'],'']
 for a in f[':answer-field/choices']:out.append('- $'+a[':answer/value']+'$'+(' **Correct**' if a[':answer/id']==correct else ''))
 return '\n'.join(out+['','**Worked solution**','',q[':question/worked-solution']])


def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all')
 ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1)
 ap.add_argument('--format',choices=['markdown','json'],default='markdown')
 ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile',choices=list(PROFILES))
 args=ap.parse_args()
 if args.count<1:ap.error('Positive count required')
 if args.difficulty=='all' and (args.template or args.profile):ap.error('Explicit profiles/templates require one difficulty')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 try:records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in levels for i in range(args.count)]
 except ValueError as exc:ap.error(str(exc))
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
