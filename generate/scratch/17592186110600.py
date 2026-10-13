#!/usr/bin/env python3
"""Perpendicular selection from a standard-form line; steps 3–7 only.

Observed replay profiles are complete banks with parameterized slope operations
and independent candidate intercepts. Incidental extra slopes have explicit u
slots: their numerical evidence does not determine an error algorithm. Authored
defaults use a complete five-member method-derived bank. No learner feedback,
plots, EDB transactions, or inferred author intent. See adjacent evidence.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186110600
KP_UUID='e732f270-1d6f-5ff8-8792-d9b329ea858d'
TITLE='Determining Whether Two Lines in Standard Form are Perpendicular'
VERSION='standard-perpendicular-v1'
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES={'easy':('standard3',),'moderate':('standard3','standard4'),'hard':('standard4',)}
# Each list is a complete bank, never a first-valid pool. u is an incidental
# source candidate slope, not a proposed wrong operation. d are independent
# candidate intercepts, whose values do not affect perpendicularity.
PROFILES={
 'q-44404':('moderate','standard3',('perpendicular','u','negative_slope','slope','reciprocal'),0),
 'q-44514':('easy','standard3',('slope','negative_slope','u','perpendicular','reciprocal'),3),
 'q-23378':('easy','standard3',('perpendicular','u','negative_slope','slope','half_slope'),0),
 'q-23618':('easy','standard3',('reciprocal','slope','perpendicular','u','negative_slope'),2),
 'q-23621':('moderate','standard3',('horizontal_slope_constant','slope','perpendicular','reciprocal','negative_slope'),2),
 'q-28338':('moderate','standard4',('slope','negative_slope','perpendicular','u','reciprocal'),2),
 'q-28341':('easy','standard3',('negative_slope','slope','perpendicular','double_perpendicular','u'),2),
 'q-59763':('easy','standard3',('negative_slope','slope','perpendicular','reciprocal','negative_slope'),2),
 'authored':(None,None,('perpendicular','slope','negative_slope','reciprocal','horizontal'),0),
}

def digest(data): return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def tex(q):
 q=sp.Rational(q)
 return ('-' if q<0 else '')+(str(abs(q.p)) if q.q==1 else r'\frac{'+str(abs(q.p))+'}{'+str(q.q)+'}')
def term(q,var,style='coefficient'):
 q=sp.Rational(q)
 if q==0:return ''
 if q==1:return var
 if q==-1:return '-'+var
 if style=='numerator_x' and abs(q.p)==1 and q.q>1:
  return ('-' if q<0 else '')+r'\frac{'+var+'}{'+str(q.q)+'}'
 return tex(q)+var

def linear(m,b,var='x',style='coefficient'):
 first=term(m,var,style);b=sp.Rational(b)
 return first+('+' if b>0 and first else '')+(tex(b) if b or not first else '')

def standard(a,b,c): return term(a,'x')+('+' if b>0 else '')+term(b,'y')+'='+str(c)
def slope_ops(m,p):
 return {'perpendicular':-1/m,'slope':m,'negative_slope':-m,'reciprocal':1/m,
         'half_slope':m/2,'double_perpendicular':-2/m,'u':sp.Rational(p.get('u',0)),
         'horizontal':sp.Rational(0),'horizontal_slope_constant':sp.Rational(0)}

def check_parameters(level,template,p,profile):
 if set(p)-{'a','b','c','d','u'}:raise ValueError('Unknown mathematical parameters')
 for k in ('a','b','c'):
  if not isinstance(p.get(k),int) or isinstance(p[k],bool):raise ValueError('Integer a,b,c required')
 a,b,c=p['a'],p['b'],p['c']
 if not a or not b or abs(c)>24:raise ValueError('Nonzero line coefficients; |c|<=24')
 m=sp.Rational(-a,b)
 if level=='easy' and not (m.q==1 and 2<=abs(m.p)<=9 and abs(b)<=5):raise ValueError('Easy integer-slope scope')
 if level=='moderate' and not (m.q>=2 and m.q<=9 and 1<=abs(m.p)<=5 and abs(a)<=30 and abs(b)<=30 and c%b==0):raise ValueError('Moderate rational-slope scope')
 if level=='hard' and not (2<=abs(m.p)<=9 and 2<=m.q<=9 and abs(a)<=27 and abs(b)<=27 and c%b!=0 and math.gcd(abs(a),abs(b))>=2):raise ValueError('Hard rational-slope scope')
 if template=='standard4' and math.gcd(abs(a),abs(b))<2:raise ValueError('Four-row conversion requires reducible slope')
 if abs(m)==1:raise ValueError('Whole-bank slope collision')
 if len(p.get('d',[]))!=5:raise ValueError('Exactly five candidate intercepts required')
 if any(abs(sp.Rational(d))>24 or sp.Rational(d).q>10 for d in p['d']):raise ValueError('Candidate intercept bounds')
 if 'u' in p and (abs(sp.Rational(p['u']))>9 or sp.Rational(p['u']).q>9):raise ValueError('Incidental slope bounds')
 if profile!='authored' and PROFILES[profile][:2]!=(level,template):raise ValueError('Source bank incompatible with level/template')
 if 'u' in PROFILES[profile][2] and 'u' not in p:raise ValueError('Observed incidental slope parameter u required')

# EASY — integer target slope, one conversion and one negative reciprocal.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — rational target slope, same three/four conversion rows.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — authored: two nonunit slope components and fractional intercept,
# with common factor 2 or 3. Still selection of a known line, never solve for k.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def sample(level,template,rng):
 if level=='easy':
  b=rng.choice([-1,1])*rng.randint(1,5);m=rng.choice([-1,1])*rng.randint(2,9);a=-b*m;c=rng.randint(-24,24)
 elif level=='moderate':
  num=rng.randint(1,5);den=rng.randint(2,9)
  if math.gcd(num,den)>1:raise ValueError('Reject complete parameter sample')
  scale=rng.randint(2,3) if template=='standard4' else 1
  a=rng.choice([-1,1])*num*scale;b=rng.choice([-1,1])*den*scale
  c=b*rng.randint(-2,2)
 else:
  num=rng.randint(2,9);den=rng.randint(2,9)
  if math.gcd(num,den)>1:raise ValueError('Reject complete parameter sample')
  scale=rng.randint(2,3);a=rng.choice([-1,1])*num*scale;b=rng.choice([-1,1])*den*scale;c=rng.randint(-24,24)
 return {'a':a,'b':b,'c':c,'d':[rng.randint(-12,12) for _ in range(5)]}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in TEMPLATES:raise ValueError('Unsupported level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Radio only')
 profile=profile or 'authored'
 if profile not in PROFILES:raise ValueError('Unknown profile')
 if profile!='authored':
  pl,pt,_,_=PROFILES[profile]
  if pl!=level or template not in (None,pt):raise ValueError('Incompatible profile/template')
  template=pt
 template=template or ('standard4' if level=='hard' else 'standard3')
 if template not in TEMPLATES[level]:raise ValueError('Template outside difficulty scope')
 rng=random.Random(seed)
 for _ in range(512):
  try:
   p=dict(parameters) if parameters is not None else sample(level,template,rng)
   if parameters is None and 'u' in PROFILES[profile][2]:p['u']=str(sp.Rational(rng.choice([-1,1])*rng.randint(1,5),rng.randint(1,9)))
   p['d']=[str(sp.Rational(d)) for d in p['d']]
   if 'u' in p:p['u']=str(sp.Rational(p['u']))
   check_parameters(level,template,p,profile)
   return assemble(level,seed,template,p,profile)
  except ValueError:
   if parameters is not None:raise
 raise ValueError('No eligible whole-bank sample in bounded attempts')

def assemble(level,seed,template,p,profile):
 a,b,c=p['a'],p['b'],p['c'];m=sp.Rational(-a,b);n=sp.Rational(c,b)
 ops=slope_ops(m,p);recipes=PROFILES[profile][2];correct_index=PROFILES[profile][3]
 pairs=[(ops[r],sp.Rational(d)) for r,d in zip(recipes,p['d'],strict=True)]
 # q-23621's first option is a constant equation, with value m rather than d.
 for i,r in enumerate(recipes):
  if r=='horizontal_slope_constant':pairs[i]=(sp.Rational(0),m)
 if len(set(pairs))!=5 or sum(m*s==-1 for s,_ in pairs)!=1 or m*pairs[correct_index][0]!=-1:
  raise ValueError('Reject whole bank: duplicate equations or ambiguous perpendicularity')
 style='numerator_x' if profile=='q-28341' else 'coefficient'
 values=['y='+linear(s,d,style=style if r in ('perpendicular','double_perpendicular') else 'coefficient') for (s,d),r in zip(pairs,recipes,strict=True)]
 given=standard(a,b,c);chosen=values[correct_index];perp=tex(-1/m)
 rows=[term(a,'x')+('+' if b>0 else '')+term(b,'y')+' & ='+str(c),term(b,'y')+' & ='+linear(-a,c)]
 if template=='standard4':
  rawm=('-' if m<0 else '')+r'\frac{'+str(abs(a))+'}{'+str(abs(b))+'}x'
  rawn=('-' if n<0 else '+')+r'\frac{'+str(abs(c))+'}{'+str(abs(b))+'}' if c else ''
  rows.append('y & ='+rawm+rawn)
 rows.append('y & ='+linear(m,n))
 slope_product=('('+tex(m)+')' if m<0 else tex(m))+r'\cdot '+('('+perp+')' if -1/m<0 else perp)+'=-1.'
 prompt='Which of the following lines is perpendicular to $'+given+'?$'
 solution=('For the two lines to be perpendicular, their slopes must multiply to $-1.$\n\n'
  'To find the slope of the given line $'+given+',$ we convert to slope-intercept form:\n\n$$\n'+r'\begin{aligned}'+' \\\\ '.join(rows)+r'\end{aligned}'+'\n$$\n\n'
  'In slope-intercept form, the slope is the $x$-coefficient. So, the slope of the given line is $'+tex(m)+'.$\n\n'
  'Looking at the answer choices, the line $'+chosen+'$ has a slope of $'+perp+'.$\n\n'
  'Multiplying the slopes together, we have\n\n$$\n'+slope_product+'\n$$\n\n'
  'Since the slopes multiply to $-1,$ we conclude that the line $'+chosen+'$ is perpendicular to the given line.')
 # Canonical assessed task is direction of given line only. Its intercept,
 # candidate bank, source profile and arithmetic layout do not inflate variety.
 task=digest({'kp':KP_ID,'slope':str(m)})
 parameter=digest({'a':a,'b':b,'c':c})
 content=digest({'version':VERSION,'level':level,'prompt':prompt,'solution':solution,'bank':sorted(values),'correct':chosen})
 qid=uuid.uuid5(uuid.NAMESPACE_URL,f'course-academy/{KP_UUID}/{content}');fid=uuid.uuid5(qid,'selection')
 answers=[{':answer/id':str(uuid.uuid5(fid,'math:'+v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 cid=answers[correct_index][':answer/id'];rng=random.Random(seed);rng.shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]}]},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'bank_origin':'authored' if profile=='authored' else 'observed','authored_extension':level=='hard' or profile=='authored','source_analysis':SOURCE,'sympy_version':sp.__version__,'task_fingerprint':task,'mathematical_task_fingerprint':task,'parameter_fingerprint':parameter,'content_fingerprint':content,'recipes':list(recipes),'plot_rating':'none','plot_assets':{}}}

def markdown(record):
 q=record['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 if args.count<1:ap.error('Count must be positive')
 try:records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (TEMPLATES if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 except ValueError as ex:ap.error(str(ex))
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
