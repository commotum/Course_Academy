#!/usr/bin/env python3
"""Modeling Inhibited Growth — exact, bounded equation-construction generators.

Read-only math basis 1356. Source masks and complete banks are extracted in the
private evidence directory; no literal-question replay branch or answer lookup.
Observed scalar ratios are opaque evidence profiles, NOT inferred misconceptions.
Normal easy uses competing capacities and mixed operation/capacity banks; moderate and hard are
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
CURRENT_SOURCES=json.loads((BASE/'current-source-recipes.json').read_text())['sources']
LEARNING_SOURCES={'source_'+str(v['db_id']):v for v in CURRENT_SOURCES.values()}
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
 **{k:{'level':'easy','origin':'observed-context','plot':'none'} for k in LEARNING_SOURCES},
 'direct_model':{'level':'easy','origin':'authored-context','plot':'none'},
 'known_integer_rate':{'level':'moderate','origin':'authored-missing-level','plot':'none'},
 'known_fractional_rate':{'level':'hard','origin':'authored-missing-level','plot':'none'}}
BANK_PROFILES={**{'observed_'+k.removeprefix('source_'):{'template':k,'origin':'observed-opaque' if any(r['operation']=='opaque_capacity_ratio' for r in v['choices']) else 'observed-operations'} for k,v in RECIPES.items()},
 **{'repaired_'+k.removeprefix('source_'):{'template':k,'origin':'source-format-repair'} for k in RECIPES},
 'model_operations':{'template':'direct_model','origin':'observed-method/authored-context'},
 'integer_placement':{'template':'known_integer_rate','origin':'authored'},
 'fractional_placement':{'template':'known_fractional_rate','origin':'authored'}}
BANK_PROFILES.update({'repaired_'+k.removeprefix('source_'):{'template':k,'origin':'source-context/competing-capacity-extension'} for k in LEARNING_SOURCES})

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
 evidence_only=raw
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'source':SOURCE,'source_id':source_id,'raw_evidence':raw,'evidence_only':evidence_only,'eligible_for_learning':not evidence_only,'origin':BANK_PROFILES[profile]['origin'],'content_sha256':h,'mathematical_fingerprint':fingerprint,'symbol':symbol,'domains':{'capacity':'positive integer; current stock below capacity','k':'positive','time':'t>=0'},'recipes':recipe_info or [],'plots':[]}}


def source_instance(level,seed,template,profile,parameters):
 if not profile.startswith('observed_'):
  return learning_easy(seed,template,profile,parameters)
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
 if level=='easy':return learning_easy(seed,template,profile,p)
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


def learning_easy(seed,template,profile,parameters=None):
 """Select a candidate role before values/context; derive all content from it.

 Source replay deliberately remains separate from normal bank construction.
 No observed numerical distractor ratio restricts a new equilibrium.
 """
 rng=random.Random(f'{seed}:easy-bank')
 spec=LEARNING_SOURCES.get(template)
 structural=spec is None or any('^{2}' in c['mask'] for c in spec['choices'])
 kind=('mixed' if structural else 'capacities') if spec else rng.choice(('mixed','capacities'))
 linear_count=3 if kind=='mixed' else 5
 linear_indices=sorted(rng.sample(range(5),linear_count))
 target=rng.choice(linear_indices)
 p=dict(parameters) if parameters is not None else {}
 allowed={'capacity','candidates','target_rank','linear_indices'} | ({'initial'} if spec and spec['initial'] is not None else {'context'} if spec is None else set())
 if set(p)-allowed:raise ValueError('unknown easy parameter')
 if parameters is not None:
  required={'capacity'} | ({'initial'} if spec and spec['initial'] is not None else {'context'} if spec is None else set())
  if not required<=set(p):raise ValueError('missing explicit easy parameter')
 if 'linear_indices' in p:
  linear_indices=p['linear_indices']
  if not isinstance(linear_indices,list) or len(linear_indices)!=linear_count or len(set(linear_indices))!=linear_count:raise ValueError('distinct eligible linear indices required')
  for i in linear_indices:integer(i,'linear index',0,4)
  linear_indices=sorted(linear_indices)
  target=rng.choice(linear_indices)
 if 'target_rank' in p:
  target=integer(p['target_rank'],'target_rank',0,4)
  if target not in linear_indices:raise ValueError('target must be an eligible linear candidate')
 if 'capacity' in p:
  A=integer(p['capacity'],'capacity',10 if spec else 20,5000 if spec else 500)
  if 'candidates' in p:
   candidates=p['candidates']
   if not isinstance(candidates,list) or len(candidates)!=5:raise ValueError('five candidate capacities required')
   for n in candidates:integer(n,'candidate',1,20000)
   if len(set(candidates))!=5:raise ValueError('candidate capacities must be distinct')
   candidates=sorted(candidates)
   if A not in [candidates[i] for i in linear_indices]:raise ValueError('capacity must be an eligible linear candidate')
   if 'target_rank' in p and candidates[target]!=A:raise ValueError('target rank disagrees with equilibrium')
   target=candidates.index(A)
  else:
   low,high=10**(len(str(A))-1),10**len(str(A))-1
   # Rank is sampled from its feasible domain, never silently forced to a source rank.
   feasible=[i for i in linear_indices if A-low>=i and high-A>=4-i]
   if not feasible:
    # Explicit boundary: choose eligible linear positions among feasible ranks.
    feasible=[i for i in range(5) if A-low>=i and high-A>=4-i]
    target=rng.choice(feasible)
    linear_indices=sorted([target]+rng.sample([i for i in range(5) if i!=target],linear_count-1))
   if 'target_rank' not in p:target=rng.choice(feasible)
   if target not in feasible:raise ValueError('target rank infeasible at this boundary')
   candidates=sorted(rng.sample(range(low,A),target)+[A]+rng.sample(range(A+1,high+1),4-target))
 else:
  # First choose the eligible target, then draw compatible values. Two/three digits
  # are presentation strata, not answer roles or different mathematical methods.
  low,high=rng.choice(((20,99),(100,500)))
  candidates=sorted(rng.sample(range(low,high+1),5));A=candidates[target]
  p['capacity']=A
 p['candidates']=candidates;p['target_rank']=target;p['linear_indices']=linear_indices
 if spec:
  s=spec['symbol']
  if spec['initial'] is not None:
   if parameters is None:p['initial']=rng.randint(1,A-1)
   integer(p['initial'],'initial',1,A-1)
  prompt=slot(spec['problem_mask'],p)
  solution=slot(spec['solution_mask'],p) if spec['solution_mask'] else None
  if spec['db_id']==17592186124766:
   prompt=prompt.replace(r'\text{units/day}',r'\text{units}').replace('$units/day$','$units$')
   if solution:solution=solution.replace('units/day','units')
  source_id=next(k for k,v in CURRENT_SOURCES.items() if v is spec)
 else:
  if parameters is None:p['context']=rng.choice(tuple(CONTEXTS))
  if p['context'] not in CONTEXTS:raise ValueError('context outside finite catalog')
  s,units,place,time=CONTEXTS[p['context']]
  prompt=f'The growth of the number of {units} in a {place} is directly proportional to the difference between its maximum capacity and its current population. Let ${s}(t)$ be the number of {units}, and let $t\\ge 0$ be the time in {time}. If the maximum capacity is ${A}$ {units}, which differential equation models this population? Assume that $k>0$ is a constant of proportionality.'
  solution=None;source_id=None
 if solution is None:
  solution='The rate of change is proportional to the difference between the maximum capacity and the current quantity. Therefore,\n\n$$\n'+equation(s,'k(a-'+s+')')+',\n$$\n\nwhere $a$ is the maximum capacity and $k>0$.\n\n'+f'Here $a={A}$, so\n\n$$\n'+equation(s,'k('+str(A)+'-'+s+')')+'.\n$$'
 # Normalize captured doubled slashes only in served content; replay stays exact.
 clean=lambda text:re.sub(r'\\{2,}(?=[A-Za-z])',lambda m:'\\',text)
 prompt=clean(prompt);solution=clean(solution)
 operations=random.Random(f'{seed}:easy-operations').sample(('reverse_gap','population_factor','quadratic_factor','negative_sum'),2) if kind=='mixed' else []
 rhs=[];info=[];operation_iter=iter(operations)
 for i,n in enumerate(candidates):
  if i in linear_indices:
   rhs.append('k('+str(n)+'-'+s+')');info.append('linear_gap');continue
  operation=next(operation_iter)
  gap='('+str(n)+'-'+s+')'
  rhs.append({'reverse_gap':'-k'+gap,'population_factor':'k'+s+gap,'quadratic_factor':'k{'+s+'}^{2}'+gap,'negative_sum':'-k('+str(n)+'+'+s+')'}[operation])
  info.append(operation)
 rec=assemble('easy',seed,template,profile,p,prompt,solution,[equation(s,x) for x in rhs],target,recipe_info=info,symbol=s,source_id=source_id)
 rec['generation'].update(bank_kind=kind,target_rank=target,version='inhibited-growth-easy-repair-2')
 return rec


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only radio field layout is supported')
 if profile:
  if profile not in BANK_PROFILES:raise ValueError('unknown profile')
  inferred=BANK_PROFILES[profile]['template']
  if template is not None and template!=inferred:raise ValueError('profile does not belong to template')
  template=inferred
 template=template or (random.Random(seed).choice(('direct_model',*LEARNING_SOURCES)) if level=='easy' and parameters is None else {'easy':'direct_model','moderate':'known_integer_rate','hard':'known_fractional_rate'}[level])
 if template not in TEMPLATES or TEMPLATES[template]['level']!=level:raise ValueError('template does not belong to level')
 source=template in LEARNING_SOURCES
 if not profile:profile='repaired_'+template.removeprefix('source_') if source else {'easy':'model_operations','moderate':'integer_placement','hard':'fractional_placement'}[level]
 rng=random.Random(seed)
 if level=='easy' and not profile.startswith('observed_'):
  return learning_easy(seed,template,profile,parameters)
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

# Current-source replay is evidence only; it never expands normal learner sampling.
BANK_PROFILES.update({'current_'+mid:{'template':'current_'+mid,'origin':'observed-current-evidence'} for mid in CURRENT_SOURCES})

def replay_current_source(source_id,capacity=None,initial=None,seed=0):
 spec=CURRENT_SOURCES[source_id];A=spec['capacity'] if capacity is None else integer(capacity,'capacity',10,5000)
 p={'capacity':A}
 if spec['initial'] is not None:
  p['initial']=spec['initial'] if initial is None else integer(initial,'initial',1,A-1)
 elif initial is not None:raise ValueError('source has no initial-stock slot')
 values=[];correct=0
 for i,choice in enumerate(spec['choices']):
  n=sp.Rational(choice['numerator'],choice['denominator'])*A
  if n.q!=1 or not 1<=n<=20000:raise ValueError('complete bank requires bounded integer constants')
  values.append(slot(choice['mask'],{'constant':int(n)}))
  if choice['correct']:correct=i
 return assemble('easy',seed,'current_'+source_id,'current_'+source_id,p,slot(spec['problem_mask'],p),slot(spec['solution_mask'],p) if spec['solution_mask'] else None,values,correct,raw=True,symbol=spec['symbol'],source_id=source_id,include_difficulty=spec['difficulty'] is not None,include_correct=any(c['correct'] for c in spec['choices']))

if __name__=='__main__':
 cli=argparse.ArgumentParser(description=__doc__);cli.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');cli.add_argument('--seed',type=int,default=0);cli.add_argument('--count',type=int,default=1);cli.add_argument('--format',choices=['markdown','json'],default='markdown');cli.add_argument('--template');cli.add_argument('--profile');args=cli.parse_args()
 if args.count<1:cli.error('count must be positive')
 levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
