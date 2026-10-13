#!/usr/bin/env python3
"""Modeling Inhibited Growth — exact, bounded equation-construction generators.

Read-only math basis 1356. Source masks and complete banks are extracted in the
private evidence directory; no literal-question replay branch or answer lookup.
Observed scalar ratios are opaque evidence profiles, NOT inferred misconceptions.
Normal easy uses the observed sign/population-factor bank; moderate and hard are
authored coefficient-placement banks. All levels ask only to construct an ODE.
The rational hard catalog is finite, reduced, positive and bounded, including on
explicit calls. Stable content identities include the full displayed bank, fixed
solution and prompt; mathematical fingerprints exclude bank, context aliases and
irrelevant initial stocks. API/CLI are review artifacts, never EDB transactions.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186124674
KP_UUID='53776591-13cc-549e-9f32-c5abaeced1dc'
TITLE='Modeling Inhibited Growth'
VERSION='inhibited-growth-model-1'
BASE=Path(__file__).with_suffix('')
RECIPES=json.loads((BASE/'extracted-recipes.json').read_text())
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
RATIONAL_CATALOG=(sp.Rational(1,2),sp.Rational(1,3),sp.Rational(2,3),sp.Rational(1,4),sp.Rational(3,4),sp.Rational(1,5),sp.Rational(2,5),sp.Rational(3,5))
CONTEXTS={
 'deer':('N','deer','protected forest','years'),
 'students':('T','students','tutoring center','months'),
 'animals':('M','animals','rehabilitation aquarium','months'),
 'cultures':('B','cultures','laboratory incubator','days'),
 'computers':('C','computers','data center','months'),
}
TEMPLATES={**{k:{'level':'easy','origin':'observed','plot':'none'} for k in RECIPES},
 'direct_model':{'level':'easy','origin':'authored-context','plot':'none'},
 'known_integer_rate':{'level':'moderate','origin':'authored-missing-level','plot':'none'},
 'known_fractional_rate':{'level':'hard','origin':'authored-missing-level','plot':'none'}}
BANK_PROFILES={**{'observed_'+k.removeprefix('source_'):{'template':k,'origin':'observed-opaque' if any(r['operation']=='opaque_capacity_ratio' for r in v['choices']) else 'observed-operations'} for k,v in RECIPES.items()},
 **{'repaired_'+k.removeprefix('source_'):{'template':k,'origin':'source-format-repair'} for k in RECIPES},
 'model_operations':{'template':'direct_model','origin':'observed-method/authored-context'},
 'integer_placement':{'template':'known_integer_rate','origin':'authored'},
 'fractional_placement':{'template':'known_fractional_rate','origin':'authored'}}

def digest(value):
 return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def uid(value):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+value))

def integer(value,key,low,high):
 if isinstance(value,bool) or not isinstance(value,int) or not low<=value<=high:raise ValueError(f'{key} must be an integer in [{low},{high}]')
 return value

def slot(mask,p):
 for key,value in p.items():mask=mask.replace('<<'+key+'>>',str(value))
 if '<<' in mask:raise ValueError('unfilled complete-component slot')
 return mask

def frac(value):
 r=sp.Rational(value)
 return str(r.p) if r.q==1 else r'\frac{'+str(r.p)+'}{'+str(r.q)+'}'

def equation(symbol,rhs):return r'\frac{\text{d}'+symbol+r'}{\text{d}t}='+rhs

def model_solution(symbol,A,r,units,place,capacity_definition=None):
 # Shared source formal-model/substitution sequence; no solving stages.
 general=equation(symbol,'k(a-'+symbol+')')
 final=equation(symbol,frac(r)+'('+str(A)+'-'+symbol+')')
 opening=f'The rate at which the number of {units} ${symbol}(t)$ in the {place} changes is proportional to the difference between the maximum capacity and the current number of {units}. Therefore, we have the differential equation'
 return opening+'\n\n$$\n'+general+',\n$$\n\nwhere $a$ is the maximum capacity, and $k>0$ is a constant of proportionality.\n\n'+f'In our case, $a={A}$ {units}, and $k={frac(r)}$. Therefore,\n\n$$\n'+final+'.\n$$'

def assemble(level,seed,template,profile,p,prompt,solution,values,correct_index,*,raw=False,recipe_info=None,symbol='N',rate='k',source_id=None,include_difficulty=True,include_correct=True):
 if len(values)!=5 or len(set(values))!=5:raise ValueError('complete five-option bank required')
 # Mathematical comparison is independently repeated from printed values in validate.py.
 identity={'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(values),'correct':values[correct_index] if include_correct else None,'difficulty':level if include_difficulty else None}
 h=digest(identity);q_id=uid('question:'+h);f_id=uid('field:'+h+':selection')
 choices=[{':answer/id':uid('answer:'+f_id+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 f={':answer-field/id':f_id,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
 if include_correct:f[':answer-field/correct']=[':answer/id',choices[correct_index][':answer/id']]
 random.Random(seed).shuffle(choices)
 q={':question/id':q_id,':question/problem':prompt,':question/answer-fields':[f]}
 if include_difficulty:q[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:q[':question/worked-solution']=solution
 # The response is a whole ODE; initial quantity only supplies irrelevant context.
 fingerprint=digest({'model':'growth_gap','capacity':p['capacity'],'rate':str(rate)})
 evidence_only=raw or profile.startswith('repaired_') and any(r['operation']=='opaque_capacity_ratio' for r in (recipe_info or []))
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'source':SOURCE,'source_id':source_id,'raw_evidence':raw,'evidence_only':evidence_only,'eligible_for_learning':not evidence_only,'origin':BANK_PROFILES[profile]['origin'],'content_sha256':h,'mathematical_fingerprint':fingerprint,'symbol':symbol,'domains':{'capacity':'positive integer; current stock below capacity','k':'positive','time':'t>=0'},'recipes':recipe_info or [],'plots':[]}}


def source_instance(level,seed,template,profile,parameters):
 spec=RECIPES[template]; raw=profile.startswith('observed_')
 allowed={'capacity'}|({'initial'} if spec['initial'] is not None else set())
 if set(parameters)!=allowed:raise ValueError(f'explicit source parameters must be exactly {allowed}')
 A=integer(parameters['capacity'],'capacity',10,5000)
 if 'initial' in parameters:integer(parameters['initial'],'initial',1,A-1)
 prompt=slot(spec['problem_mask'],parameters)
 solution=slot(spec['solution_mask'],parameters) if spec['solution_mask'] is not None else None
 values=[];correct=None;info=[]
 for r in spec['choices']:
  n=sp.Rational(r['scale_numerator'],r['scale_denominator'])*A
  if n.q!=1 or not 1<=n<=20000:raise ValueError('whole observed bank needs bounded integer constants')
  value=slot(r['equation_mask'],{'constant':int(n)})
  values.append(value);info.append({**r,'derived_constant':int(n)})
  if r['operation']=='correct':correct=len(values)-1
 if correct is None:raise ValueError('no derived correct model operation')
 if not raw:
  if spec['source_db_id']==17592186124766:
   # A quantity measured in units cannot approach a maximum measured units/day.
   prompt=prompt.replace('$units/day$','$units$')
  if solution is None:
   s=spec['symbol'];solution=f'The rate of change is proportional to the gap between the maximum quantity and the current quantity. Therefore,\n\n$$\n'+equation(s,'k(a-'+s+')')+',\n$$\n\nwhere $a$ is the maximum quantity and $k>0$.\n\n'+f'Here $a={A}$, so\n\n$$\n'+equation(s,'k('+str(A)+'-'+s+')')+'.\n$$'
 return assemble(level,seed,template,profile,parameters,prompt,solution,values,correct,raw=raw,recipe_info=info,symbol=spec['symbol'],source_id=spec['source_id'],include_difficulty=spec['original_difficulty'] if raw else True,include_correct=spec['original_correct'] if raw else True)


def authored_instance(level,seed,template,profile,p):
 expected={'context','capacity'} if level=='easy' else {'context','capacity','initial','numerator','denominator'}
 if set(p)!=expected:raise ValueError(f'explicit {level} parameters must be exactly {expected}')
 if p['context'] not in CONTEXTS:raise ValueError('context outside finite catalog')
 A=integer(p['capacity'],'capacity',20,500)
 s,units,place,time=CONTEXTS[p['context']]
 if level=='easy':
  r='k';prompt=f'The growth of the number of {units} in a {place} is directly proportional to the difference between its maximum capacity and its current population. Let ${s}(t)$ be the number of {units}, and let $t\\ge 0$ be the time in {time}. If the maximum capacity is ${A}$ {units}, which differential equation models this population? Assume that $k>0$ is a constant of proportionality.'
  rhs=['k('+str(A)+'-'+s+')','-k('+str(A)+'-'+s+')','k'+s+'('+str(A)+'-'+s+')','k{'+s+'}^{2}('+str(A)+'-'+s+')','-k('+str(A)+'+'+s+')']
  solution=f'The rate of change is proportional to the difference between the maximum capacity and the current population. Therefore,\n\n$$\n'+equation(s,'k(a-'+s+')')+',\n$$\n\nwhere $a$ is the maximum capacity and $k>0$.\n\n'+f'Here $a={A}$ {units}, so\n\n$$\n'+equation(s,rhs[0])+'.\n$$'
  recipes=['correct','reverse_gap','population_factor','quadratic_factor','negative_sum']
 else:
  I=integer(p['initial'],'initial',1,A-1);n=integer(p['numerator'],'numerator',1,6);d=integer(p['denominator'],'denominator',1,5);r=sp.Rational(n,d)
  if level=='moderate' and (d!=1 or n not in range(2,7)):raise ValueError('moderate requires integer rate 2..6')
  if level=='hard' and (r not in RATIONAL_CATALOG or sp.gcd(n,d)!=1):raise ValueError('hard requires a reduced rational in the explicit finite catalog')
  rt=frac(r);prompt=f'A {place} initially contains ${I}$ {units}, and its maximum capacity is ${A}$ {units}. Let ${s}(t)$ be the number of {units}, where $t\\ge 0$ is the time in {time}. Its population obeys an inhibited growth model. The rate of increase equals ${rt}$ times the difference between the maximum capacity and the current population. Which differential equation models this population?'
  if level=='moderate':
   rhs=[rt+'('+str(A)+'-'+s+')','('+str(A)+'-'+s+')','-'+rt+'('+str(A)+'-'+s+')',rt+'('+str(I)+'-'+s+')',str(n*A)+'-'+s]
   recipes=['correct','omit_rate','reverse_gap','use_initial_capacity','apply_rate_only_to_capacity']
  else:
   rhs=[rt+'('+str(A)+'-'+s+')',frac(1/r)+'('+str(A)+'-'+s+')',str(n)+'('+str(A)+'-'+s+')',frac(r*A)+'-'+s,rt+'('+str(I)+'-'+s+')']
   recipes=['correct','invert_rate','omit_denominator','apply_rate_only_to_capacity','use_initial_capacity']
  solution=model_solution(s,A,r,units,place)
 return assemble(level,seed,template,profile,p,prompt,solution,[equation(s,x) for x in rhs],0,recipe_info=recipes,symbol=s,rate=r)


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only radio field layout is supported')
 if profile:
  if profile not in BANK_PROFILES:raise ValueError('unknown profile')
  inferred=BANK_PROFILES[profile]['template']
  if template is not None and template!=inferred:raise ValueError('profile does not belong to template')
  template=inferred
 template=template or {'easy':'direct_model','moderate':'known_integer_rate','hard':'known_fractional_rate'}[level]
 if template not in TEMPLATES or TEMPLATES[template]['level']!=level:raise ValueError('template does not belong to level')
 source=template in RECIPES
 if not profile:profile='repaired_'+template.removeprefix('source_') if source else {'easy':'model_operations','moderate':'integer_placement','hard':'fractional_placement'}[level]
 rng=random.Random(seed)
 if parameters is not None:
  p=dict(parameters)
  return source_instance(level,seed,template,profile,p) if source else authored_instance(level,seed,template,profile,p)
 for attempt in range(1000):
  if source:
   spec=RECIPES[template];scale=rng.choice((1,2,3,4));p={'capacity':spec['capacity']*scale}
   if spec['initial'] is not None:p['initial']=spec['initial']*scale
  else:
   p={'capacity':rng.randint(20,500),'context':rng.choice(tuple(CONTEXTS))}
   if level!='easy':
    r=rng.choice(RATIONAL_CATALOG) if level=='hard' else sp.Integer(rng.randint(2,6))
    p.update(initial=rng.randint(1,p['capacity']-1),numerator=int(r.p),denominator=int(r.q))
  try:return source_instance(level,seed,template,profile,p) if source else authored_instance(level,seed,template,profile,p)
  except ValueError:continue
 raise ValueError('no eligible complete bank within bounded sampler')

# EASY: observed direct maximum-to-equation mapping; complete sign/function bank.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: authored nonunit positive integer coefficient, maximum vs initial.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored finite reduced fraction placement, maximum vs initial; no solving.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def markdown(rec):
 q=rec['question'];lines=[q[':question/problem'],'']
 for a in q[':question/answer-fields'][0][':answer-field/choices']:lines.append('- $'+a[':answer/value']+'$'+(' **Correct**' if q[':question/answer-fields'][0].get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else ''))
 if ':question/worked-solution' in q:lines+=['','Worked solution:',q[':question/worked-solution']]
 return '\n'.join(lines)

if __name__=='__main__':
 cli=argparse.ArgumentParser(description=__doc__);cli.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');cli.add_argument('--seed',type=int,default=0);cli.add_argument('--count',type=int,default=1);cli.add_argument('--format',choices=['markdown','json'],default='markdown');cli.add_argument('--template');cli.add_argument('--profile');args=cli.parse_args()
 if args.count<1:cli.error('count must be positive')
 levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
