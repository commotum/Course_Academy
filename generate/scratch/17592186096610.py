#!/usr/bin/env python3
"""Differentiating ae^x+c, basis 1356. Local generator; stops after guide step 7.

Easy replays all observed formats/banks, including unrated originals assigned easy.
Moderate/hard are explicitly authored exact-arithmetic peers, never chain-rule,
polynomial, other-base, inverse-slope, or tangent-equation questions. See evidence.
Observed replay profiles retain all source options; unknown original error intent
is not presented as recovered. Authored defaults use one complete operation bank.
No database clients/writes, plots, or source-payload return branches.
"""
import argparse
import hashlib
import json
import random
import uuid
from pathlib import Path
import sympy as sp

KP_ID = 17592186096610
KP_UUID = 'bb40a0ff-c3b5-512d-a436-cc2fce456008'
TITLE = 'Differentiating the Product of a Constant and the Exponential Function, Plus a Constant'
VERSION = 'exp-constant-1'
ROOT = Path(__file__).with_suffix('')
SOURCE = {'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
X = sp.Symbol('x',real=True)
TEMPLATES = {
 'legacy_derivative':('easy','radio'),
 'slope_radio':('easy','radio'),
 'derivative_blank':('easy','blank'),
 'slope_blank':('easy','blank'),
 'derivative_radio':('easy','radio'),
 'moderate_slope':('moderate','blank'),
 'hard_slope':('hard','blank'),
}
PROFILES = {'legacy_log_scale':'legacy_derivative','legacy_log_base':'legacy_derivative',
 'slope_zero':'slope_radio','slope_one':'slope_radio','negative_unit':'derivative_radio',
 'blank_alias':'derivative_blank','blank':'derivative_blank','slope_blank':'slope_blank',
 'authored_derivative':'derivative_radio','authored_slope':'slope_radio'}

def tex(v):
 return sp.latex(sp.sympify(v),ln_notation=True).replace(r'\log',r'\ln')
def coeff(a,e='{e}^{x}'):
 a=sp.Rational(a)
 if a==1:return e
 if a==-1:return '-'+e
 return tex(a)+e

def const(p,legacy=False):
 b=sp.Rational(p['b']);kind=p['constant_kind']
 if kind=='ln': s=(r'\ln '+tex(abs(b))) if legacy else ('ln⁡'+tex(abs(b)))
 else:s=tex(abs(b))
 return ('-' if b<0 else '')+s

def additive(left,right):return left+('' if right.startswith('-') else '+')+right

def expression(p,legacy=False):
 c=const(p,legacy);ex=coeff(p['a'],'e^{x}' if legacy else '{e}^{x}')
 if p['order']=='constant_first':
  if legacy:return c+(' - '+ex[1:] if ex.startswith('-') else ' + '+ex)
  return additive(c,ex)
 return additive(ex,c)

def point(p):
 if p['point_kind']=='integer':return tex(sp.Rational(p['point']))
 z=sp.Rational(p['point']);return ('-' if z<0 else '')+'ln⁡'+tex(abs(z))

def point_value(p):
 v=sp.Rational(p['point'])
 return v if p['point_kind']=='integer' else sp.sign(v)*sp.log(abs(v))

def answer_value(p,slope):return sp.simplify(sp.Rational(p['a'])*sp.exp(point_value(p) if slope else X))

def solution(p,slope,nested=False):
 """Source-shared prose and ordered, unevaluated formal derivative/slope rows."""
 c=const(p);a=sp.Rational(p['a']);ex=coeff(a);f=expression(p)
 d=lambda s:r'\frac{\text{d}}{\text{d}x}('+s+')'
 if p['order']=='constant_first':
  distributed=d(c)+'+'+d(ex)
  reduced='0'+('-'+tex(abs(a)) if a<0 else '+'+tex(a))+d('{e}^{x}')
 else:
  distributed=d(ex)+'+'+d(c)
  reduced=tex(a)+d('{e}^{x}')+'+0'
 opening='The derivative of ${e}^{x}$ is just ${e}^{x}$ itself. On the other hand, $'+c+'$ is a constant, so its derivative is $0.$\n\n'
 opening+='First, using the addition rule, we get' if slope else 'Using the addition rule, then, we have '
 rows=r'{f}^{′}(x) & ='+d(f)+r' \\  & ='+distributed+r' \\  & ='+reduced+r' \\  & ='+ex+'.'
 begin=r'\begin{aligned}';end=r'\end{aligned}'
 result=opening+'\n\n$$\n'+begin*(2 if nested else 1)+rows+end*(2 if nested else 1)+'\n$$'
 if slope:
  t=point(p);v=point_value(p);value=answer_value(p,True)
  ev=sp.simplify(sp.exp(v))
  erows=r'{\frac{\text{d}f}{\text{d}x}|}_{x='+t+r'} & ={('+ex+r')\,|}_{x='+t+r'} \\  & ='+coeff(a,'{e}^{'+t+'}')
  if p['point_kind']=='ln' or v==0: erows+=r' \\  & ='+tex(a)+r'\cdot '+tex(ev)
  erows+=r' \\  & ='+tex(value)+'.'
  result+='\n\nTherefore, the slope of the tangent at $x='+t+'$ is\n\n$$\n'+begin+erows+end+'\n$$'
 return result

def prompt(p,t):
 f=expression(p,t=='legacy_derivative')
 if t=='legacy_derivative':return 'Given that $f(x) = '+f+'$, find $f^{′}(x)$.'
 if t=='slope_radio':return 'Given that $f(x)='+f+'$, find the slope of the tangent at $x='+point(p)+'.$'
 if t=='derivative_blank':return 'Given that $f(x)='+f+',$ find ${f}^{′}(x).$\n\n${f}^{′}(x)=$\n{{field-1}}'
 if t=='derivative_radio':return 'Given that $f(x)='+f+',$ find ${f}^{′}(x).$'
 return 'Given that $f(x)='+f+'$, the slope of the tangent line at $x='+point(p)+'$ is{{field-1}}.'

def bank(p,t,profile):
 a=sp.Rational(p['a']);b=sp.Rational(p['b']);c=sp.sign(b)*sp.log(abs(b)) if p['constant_kind']=='ln' else b
 correct=answer_value(p,'slope' in t)
 if profile=='legacy_log_scale':vals=[sp.log(abs(b))*sp.exp(X),a*sp.exp(X)+c,sp.Integer(0),c,correct]
 elif profile=='legacy_log_base':vals=[a*sp.exp(X)+c,c,sp.Integer(0),abs(b)+a*sp.exp(X),correct]
 elif profile=='slope_zero':vals=[sp.log(abs(a)),b,sp.Integer(0),correct,-b]
 elif profile=='slope_one':vals=[sp.Integer(0),sp.Integer(1),correct,sp.exp(a),a]
 elif profile=='negative_unit':vals=[-sp.exp(X),correct,b+a*sp.exp(X),b-sp.exp(X),sp.Integer(0)]
 elif profile=='authored_derivative':vals=[correct,a*sp.exp(X)+c,sp.exp(X),c,sp.Integer(0)]
 elif profile=='authored_slope':vals=[correct,correct+c,a,sp.exp(point_value(p)),sp.Integer(0)]
 else:vals=[correct]
 strings=[]
 for i,v in enumerate(vals):
  s=tex(v).replace('e^{x}','{e}^{x}').replace(r'\ln{\left('+tex(abs(a))+r'\right)}','ln⁡'+tex(abs(a)))
  if profile=='blank_alias' and i==0:strings=[coeff(a),coeff(a,'e^{x}')];break
  if t=='legacy_derivative':
   # Source-preserving complete equation spelling, with component recipes.
   ex=coeff(a,'e^{x}');ct=const(p,True)
   if profile=='legacy_log_scale':s=[r'\ln '+tex(abs(b))+r' \cdot e^{x}',ex+' + '+ct,'0',ct,ex][i]
   else:s=[ex+' + '+ct,ct,'0',tex(abs(b))+' '+('- '+coeff(abs(a),'e^{x}') if a<0 else '+ '+ex),ex][i]
   s='f^{′}(x) ='+('' if s.startswith('-') else ' ')+s
  elif t=='derivative_radio':s='{f}^{′}(x)='+s
  strings.append(s)
 if len(vals)>1 and profile!='blank_alias':
  for i,v in enumerate(vals):
   for j in range(i):
    if sp.simplify(v-vals[j])==0:raise ValueError('Ambiguous whole bank')
 return strings,correct

def validate_parameters(p,level,t,profile):
 if set(p)!={'a','b','constant_kind','order','point','point_kind'}:raise ValueError('Exact parameter keys required')
 a=sp.Rational(p['a']);b=sp.Rational(p['b']);v=sp.Rational(p['point'])
 if not a or not b or abs(a)>20 or abs(b)>20 or b.q!=1:raise ValueError('Nonzero bounded coefficient and integer/log-integer constant required')
 if p['constant_kind'] not in ('ln','integer') or p['order'] not in ('constant_first','exponential_first') or p['point_kind'] not in ('ln','integer'):raise ValueError('Unsupported component')
 if p['point_kind']=='ln' and (not v or abs(v)==1):raise ValueError('Nontrivial positive log argument required')
 if p['constant_kind']=='ln' and abs(b)==1:raise ValueError('Nonzero constant required')
 if level=='easy':
  if a.q!=1 or b.q!=1 or abs(a)<2 or abs(a)>12:raise ValueError('Easy integer bounds')
  if 'slope' in t and not (p['point_kind']=='integer' and v in (0,1) or p['point_kind']=='ln' and v.q==1 and 2<=v<=9):raise ValueError('Easy point bounds')
 if level=='moderate':
  if not (a.q in (2,3,4) and 1<=abs(a.p)<=12 and abs(a)<=6 and p['point_kind']=='ln' and v.q==1 and -9<=v<=-2):raise ValueError('Moderate noninteger coefficient/reciprocal-log bounds')
 if level=='hard':
  if not (a.q in (2,3,4,5) and 1<=abs(a.p)<=12 and abs(a)<=6 and p['point_kind']=='ln' and v.q in (2,3,4,5) and 2<=abs(v.p)<=12 and sp.Rational(1,5)<=abs(v)<=6):raise ValueError('Hard rational coefficient/rational-log bounds')
 if profile in ('legacy_log_scale','legacy_log_base') and (p['constant_kind']!='ln' or p['order']!='constant_first'):raise ValueError('Legacy bank scope')
 if profile=='negative_unit' and (a>=-1 or p['constant_kind']!='integer' or p['order']!='constant_first'):raise ValueError('Negative unit bank scope')
 if profile=='slope_zero' and (p['point_kind']!='integer' or v!=0 or b!=1):raise ValueError('Observed zero bank scope')
 if profile=='slope_one' and (p['point_kind']!='integer' or v!=1):raise ValueError('Observed one bank scope')

def sample(r,level,t,profile):
 a=r.choice(list(range(2,13))+list(range(-12,-1)));b=r.choice(range(2,13))*r.choice([-1,1]);kind=r.choice(['ln','integer']);order=r.choice(['constant_first','exponential_first']);pv=r.choice([0,1]);pk='integer'
 if profile in ('legacy_log_scale','legacy_log_base'):kind='ln';order='constant_first'
 if profile=='negative_unit':a=-abs(a);kind='integer';order='constant_first'
 if profile=='slope_zero':a=abs(a);b=1;kind='integer';order='exponential_first';pv=0
 if profile=='slope_one':pv=1
 if t=='slope_blank':pv=r.randint(2,9);pk='ln'
 if level!='easy':
  aa=[sp.Rational(n,d) for n in range(-12,13) if n for d in range(2,5 if level=='moderate' else 6) if sp.Rational(n,d).q==d and abs(sp.Rational(n,d))<=6]
  a=r.choice(aa);pk='ln';pv=-r.randint(2,9)
  if level=='hard':pv=r.choice([sp.Rational(n,d) for n in range(2,13) for d in range(2,6) if sp.Rational(n,d).q==d and abs(sp.Rational(n,d))!=1 and sp.Rational(n,d)<=6])*r.choice([-1,1])
 return {'a':str(a),'b':str(b),'constant_kind':kind,'order':order,'point':str(pv),'point_kind':pk}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 r=random.Random(seed)
 if profile is not None and profile not in PROFILES:raise ValueError('Unknown profile')
 if template is None and profile is not None:template=level+'_slope' if profile=='slope_blank' and level!='easy' else PROFILES[profile]
 candidates=[t for t,(l,f) in TEMPLATES.items() if l==level and (field_type is None or f==field_type)]
 if not candidates:raise ValueError('Unsupported field layout')
 t=template or r.choice(candidates)
 if t not in candidates:raise ValueError('Template/level/type mismatch')
 if profile is None:profile={'legacy_derivative':'legacy_log_scale','slope_radio':'authored_slope','derivative_radio':'authored_derivative','derivative_blank':'blank','slope_blank':'slope_blank','moderate_slope':'slope_blank','hard_slope':'slope_blank'}[t]
 # The common blank profile is valid for all authored slope peers.
 if PROFILES[profile]!=t and not (profile=='slope_blank' and t in ('moderate_slope','hard_slope')):raise ValueError('Profile mismatch')
 for _ in range(1000):
  p=dict(parameters) if parameters is not None else sample(r,level,t,profile)
  p={k:str(sp.Rational(v)) if k in ('a','b','point') else v for k,v in p.items()}
  try:
   validate_parameters(p,level,t,profile);strings,correct=bank(p,t,profile);break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('No valid complete bank')
 problem=prompt(p,t);slope='slope' in t
 worked=solution(p,slope,t in ('derivative_blank','derivative_radio'))
 ft=TEMPLATES[t][1];key='selection' if ft=='radio' else 'field-1'
 body={'version':VERSION,'problem':problem,'solution':worked,'field':ft,'bank':sorted(strings),'correct':tex(correct)}
 digest=hashlib.sha256(json.dumps(body,sort_keys=True).encode()).hexdigest()
 uid=lambda s:str(uuid.uuid5(uuid.NAMESPACE_URL,str(KP_ID)+':'+digest+':'+s))
 answers=[{':answer/id':uid('answer:'+v),':answer/type':':answer.type/math',':answer/value':v} for v in strings]
 # Correct designation is mathematical, never positional.
 vals=[answer_value(p,slope)] if ft=='blank' else None
 if ft=='blank':correct_id=answers[0][':answer/id']
 else:
  from_index={'legacy_log_scale':4,'legacy_log_base':4,'slope_zero':3,'slope_one':2,'negative_unit':1,'authored_derivative':0,'authored_slope':0}[profile]
  correct_id=answers[from_index][':answer/id'];r.shuffle(answers)
 field={':answer-field/id':uid('field'),':answer-field/key':key,':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}
 fingerprint=hashlib.sha256(json.dumps([str(sp.Rational(p['a'])),str(point_value(p)) if slope else 'x','slope' if slope else 'derivative']).encode()).hexdigest()
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':uid('question'),':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':worked,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'template':t,'parameters':p,'bank_profile':profile,'source':SOURCE,'parameter_fingerprint':fingerprint,'content_hash':digest,'scope':'ae^x+c; real x; no chain rule','authored_level':level!='easy','sympy_version':sp.__version__}}

# Easy: integer coefficient; derivative or source-familiar 0/1/ln(integer) evaluation.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate authored peers: noninteger coefficient and negative ln(integer) point.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard authored peers: noninteger coefficient and signed ln(noninteger rational) point.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('$'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
 records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
