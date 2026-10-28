#!/usr/bin/env python3
"""Parametrizing a Parabolic Cylinder, immutable math basis 2275 draft.

One quadratic relation, one unrestricted free coordinate; no other surfaces.
All six original practice questions and seven full captured banks replay through
parameterized public profiles, including raw missing attributes and duplicate
fields. Normal questions preserve source solution masks and repair presentation.
Hard normalization code is retained as draft evidence only; public generation rejects it.
See adjacent extraction/validation/review evidence. No EDB operations or plots.
"""
from __future__ import annotations
import argparse, copy, functools, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from math_format import (checked_math_content,
    normalize_prose, normalize_tex, validate_prose, validate_tex)
KP_ID = 17592186175972
KP_UUID = '87b371d9-6172-5ac0-a105-c9887542f0a7'
TITLE = 'Parametrizing a Parabolic Cylinder'
VERSION = 'parabolic-cylinder-2275-v2'
SUPPORTED_LEVELS = ('easy', 'moderate')
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'course-academy-generator'))
SOURCE = {'database':'math','basis':2275,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
AXES = 'xyz'
ORDINAL = ['first','second','third']
TEMPLATES = {
 'dependent_component': {'role':'dependent','sources':['q-103986','q-164443','q-164441','q-164450']},
 'free_component': {'role':'free','sources':['q-164440']},
 'free_component_inline': {'role':'free','sources':['q-103992']},
 'normalized_dependent': {'role':'dependent','sources':[]},
}
# Complete banks: every member derives from the shown base/free coordinate or scale.
# q103986 half-scale linear choice is an observed expression mask, intent unknown.
PROFILES = {
 'q-103986': ('dependent_component', ('half_linear','free_square','base_square','wrong_scaled_square','correct')),
 'q-164443': ('dependent_component', ('correct','free','wrong_scaled_square','base','base_linear')),
 'q-164441': ('dependent_component', ('base_linear','free','free_linear','free_square','correct')),
 'q-164450': ('dependent_component', ('free_square','correct','free','base_linear','free_linear')),
 'q-164440': ('free_component', ('correct','free_square','free_linear','base','dependent')),
 'q-103992': ('free_component_inline', ('base','free_square','sin_base','correct','base_square')),
 'normalized': ('normalized_dependent', ('correct','unnormalized','reciprocal','base_linear','wrong_scaled_square')),
}
OBSERVED_PARAMETERS = {
 'q-103986': dict(base='x',dependent='y',a=4,target='y',argument_order='base_first',relation_order='dependent_first'),
 'q-164443': dict(base='y',dependent='x',a=3,target='x',argument_order='base_first',relation_order='dependent_first'),
 'q-164441': dict(base='x',dependent='y',a=12,target='y',argument_order='base_first',relation_order='dependent_first'),
 'q-164450': dict(base='z',dependent='x',a=8,target='x',argument_order='free_first',relation_order='quadratic_first'),
 'q-164440': dict(base='x',dependent='y',a=6,target='z',argument_order='base_first',relation_order='dependent_first'),
 'q-103992': dict(base='y',dependent='z',a=9,target='x',argument_order='free_first',relation_order='quadratic_first'),
}

def uid(text): return str(uuid.uuid5(uuid.UUID(KP_UUID), text))
def digest(value): return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def square(v, style='braced'):
 return ('{'+v+'}^{2}') if style=='braced' else v+'^{2}'
def mul(c, v):
 c=sp.Rational(c)
 if c==1:return v
 if c.q==1:return str(c)+v
 return r'\frac{'+str(c.p)+'}{'+str(c.q)+'}'+v

def math_values(p, recipes, style='braced'):
 u,v=p['base'],p['free']; c=sp.Rational(p['a'],p['b'])
 dep=mul(c,square(u,style))
 table={'correct': dep if p['role']=='dependent' else v,
 'half_linear':mul(c/2,u),'free_square':square(v,style),'base_square':square(u,style),
 'wrong_scaled_square':mul(c,square(v,style)),'free':v,'base':u,
 'base_linear':mul(c,u),'free_linear':mul(c,v),'dependent':dep,
 'sin_base':r'\sin '+u,'unnormalized':mul(p['a'],square(u,style)),
 'reciprocal':mul(1/c,square(u,style))}
 return [normalize_tex(table[r]) for r in recipes]

def check_complete_bank(p, recipes):
 # Guards apply to the entire selected profile, never a replacement option pool.
 u,v=sp.symbols(p['base']+' '+p['free'], real=True);c=sp.Rational(p['a'],p['b'])
 dep=c*u**2
 table={'correct':dep if p['role']=='dependent' else v,
 'half_linear':c*u/2,'free_square':v**2,'base_square':u**2,
 'wrong_scaled_square':c*v**2,'free':v,'base':u,'base_linear':c*u,
 'free_linear':c*v,'dependent':dep,'sin_base':sp.sin(u),
 'unnormalized':p['a']*u**2,'reciprocal':u**2/c}
 values=[table[r] for r in recipes]
 if len(values)!=5 or len(recipes)!=5:raise ValueError('Incomplete selected bank')
 for i,x in enumerate(values):
  for y in values[i+1:]:
   if sp.expand(x-y)==0:raise ValueError('Reject whole instance: equivalent component options')
 expected=dep if p['role']=='dependent' else v
 if sum(sp.expand(x-expected)==0 for x in values)!=1:raise ValueError('Reject whole instance: nonunique direct-coordinate answer')

def prepare(level,template,parameters,profile,rng,raw):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if profile is not None and profile not in PROFILES:raise ValueError('Unknown complete profile')
 if template is not None and template not in TEMPLATES:raise ValueError('Unknown template')
 eligible = (['normalized'] if level=='hard' else ['q-164450'] if level=='moderate'
             else ['q-103986','q-164443','q-164441','q-164440','q-103992'])
 if profile is None:
  eligible=[x for x in eligible if template is None or PROFILES[x][0]==template]
  if not eligible:raise ValueError('No eligible template/profile for difficulty')
  profile=rng.choice(eligible)
 inferred_template=PROFILES[profile][0]
 if template is not None and template!=inferred_template:raise ValueError('Profile/template mismatch')
 template=inferred_template
 if not raw and profile not in eligible:raise ValueError('Profile outside difficulty workload')
 if raw and profile=='normalized':raise ValueError('Authored profile has no raw source')
 if raw and level!=('moderate' if profile=='q-164450' else 'easy'):raise ValueError('Raw evidence difficulty uses source label; unrated API uses easy metadata only')
 role=TEMPLATES[template]['role']
 if parameters is None:
  base,dep=rng.sample(list(AXES),2);free=next(x for x in AXES if x not in (base,dep))
  if level=='hard':
   pairs=[(a,b) for a in range(2,13) for b in range(2,6) if sp.gcd(a,b)==1]
   a,b=rng.choice(pairs)
  else:a,b=rng.randint(2,12),1
  p=dict(base=base,dependent=dep,a=a,b=b,target=dep if role=='dependent' else free,
         argument_order=('free_first' if level=='moderate' or profile=='q-103992' else 'base_first'),
         relation_order=('quadratic_first' if level=='moderate' or profile=='q-103992' else 'dependent_first'))
 else:p=copy.deepcopy(parameters)
 permitted={'base','dependent','a','b','target','argument_order','relation_order','function'}
 if set(p)-permitted:raise ValueError('Unknown parameters')
 for key in ('base','dependent','a','target','argument_order','relation_order'):
  if key not in p:raise ValueError('Missing parameter '+key)
 p.setdefault('b',1);p.setdefault('function','f')
 if p['base'] not in AXES or p['dependent'] not in AXES or p['base']==p['dependent']:raise ValueError('Distinct Cartesian axes required')
 p['free']=next(x for x in AXES if x not in (p['base'],p['dependent']))
 if p['target']!=(p['dependent'] if role=='dependent' else p['free']):raise ValueError('Target must preserve template role')
 if p['argument_order'] not in ('base_first','free_first') or p['relation_order'] not in ('dependent_first','quadratic_first'):raise ValueError('Unknown order')
 if p['function'] not in ('f','g','h'):raise ValueError('Unsupported function name')
 if type(p['a']) is not int or type(p['b']) is not int:raise ValueError('Integral coefficients required')
 if raw:
  if not 2<=p['a']<=12 or p['b']!=1:raise ValueError('Raw coefficient mask bounds')
 elif level=='hard':
  if not (2<=p['a']<=12 and 2<=p['b']<=5 and sp.gcd(p['a'],p['b'])==1):raise ValueError('Hard requires small coprime normalization with noninteger ratio')
 elif not (2<=p['a']<=12 and p['b']==1):raise ValueError('Copy-component coefficient bounds')
 if not raw and level=='moderate' and (p['argument_order']!='free_first' or p['relation_order']!='quadratic_first'):raise ValueError('Moderate workload: second-listed base, reversed relation')
 p['role']=role
 p['arguments']=[p['base'],p['free']] if p['argument_order']=='base_first' else [p['free'],p['base']]
 return template,profile,p

def render(p,profile,raw):
 u,d,v=p['base'],p['dependent'],p['free']; a,b=p['a'],p['b'];fn=p['function'];args=','.join(p['arguments'])
 t=p['target'];i=AXES.index(t);ordinal=ORDINAL[i];quad=mul(a,square(u));dep=mul(sp.Rational(a,b),square(u))
 vector=[dep if x==d else x for x in AXES]
 masked=vector.copy();masked[i]=r'\text{___}' if raw else '?'
 left=mul(b,d);right=quad
 relation=left+'='+right if p['relation_order']=='dependent_first' else right+'='+left
 inline=profile=='q-103992'
 if inline:
  # Captured inline family uses unbraced y², spaced arguments, and misplaced prose argument.
  ivec=[x.replace(square(u),square(u,'legacy')) for x in masked]
  arg_inline=', '.join(p['arguments']); prose_args=arg_inline
  if raw:prose_args=u+', '+d # source actual shown args free,base; erroneous prose free,dep
  # Parameterized mismatch retains first actual argument, replacing second with dependent.
  if raw:prose_args=p['arguments'][0]+', '+d
  irelation=mul(a,square(u,'legacy'))+' = '+d
  problem='$'+fn+'('+arg_inline+') = ⟨'+', '.join('___' if x==r'\text{___}' else x for x in ivec)+'⟩$\n\n'
  problem+='The vector-valued function $'+fn+'('+prose_args+')$ above parametrizes the parabolic cylinder defined in Cartesian coordinates as $'+irelation+'$. What is the '+ordinal+' component of $'+fn+'$?'
 else:
  problem='$$\n'+fn+'('+args+')=⟨'+r'\,'.join([masked[0]+',',masked[1]+',',masked[2]])+'⟩\n$$\n\n'
  problem+='The vector-valued function $'+fn+'('+args+')$ above parametrizes the parabolic cylinder defined in Cartesian coordinates as $'+relation+'.$ What is the '+ordinal+' component of $'+fn+'?$'
 if not raw and p['role']=='free':
  problem+=' Use the named parameters directly as their corresponding Cartesian coordinates.'
 opening='For any point $(x,y,z)$ on our surface, we obtain the following:\n\n'
 # Exactly preserve source graph-copy stage, including the Cartesian basis order.
 solution=opening+'$$\n'+r'\begin{aligned}'+fn+'('+args+r') & =⟨x,y,z⟩ \\  & =⟨'+r'\,'.join([vector[0]+',',vector[1]+',',vector[2]])+r'⟩\end{aligned}'+'\n$$\n\n'
 solution+='where $'+p['arguments'][0]+r'\in (-\infty ,\infty )$ and $'+p['arguments'][1]+r'\in (-\infty ,\infty ).$'+'\n\n'
 solution+='Therefore, the '+ordinal+' component of $'+fn+'$ is $'+vector[i]+'.$'
 if not raw and p['role']=='free':
  solution='Use the named coordinate parameters directly, so the free-axis coordinate is $'+v+'.$\n\n'+solution
 if profile=='normalized':
  solution='First, write the dependent coordinate as an explicit function of $'+u+'.$\n\n$$\n'+left+'='+right+r'\quad\Longrightarrow\quad '+d+'='+dep+'\n$$\n\n'+solution
 return (problem,solution)

@checked_math_content
def checked_normal(record):return record

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Raw replay: profile='q-164440_raw', parameters=source-case parameters.
 Raw evidence retains omissions/legacy fields and is never eligible for learning.
 """
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only source radio fields supported')
 if level not in SUPPORTED_LEVELS:
  raise ValueError('Unsupported difficulty: hard has no source-backed same-stage template; reserve remains unfilled')
 raw=bool(profile and profile.endswith('_raw'))
 if raw:profile=profile[:-4]
 rng=random.Random(seed)
 template,profile,p=prepare(level,template,parameters,profile,rng,raw)
 problem,solution=render(p,profile,raw)
 problem=normalize_prose(problem);solution=normalize_prose(solution)
 recipes=PROFILES[profile][1]
 if profile=='q-103986' and not raw:
  recipes=('base_linear','free_square','base_square','wrong_scaled_square','correct')
 check_complete_bank(p,recipes)
 banks=[math_values(p,recipes,'legacy' if profile=='q-103992' else 'braced')]
 legacy=None
 if raw and profile=='q-103986':
  legacy=math_values(p,recipes,'legacy');banks=[legacy,banks[0]]
 include_solution=not(raw and profile=='q-103992')
 include_difficulty=not(raw and profile=='q-103992')
 # Presentation identity excludes source/profile aliases and answer order.
 payload={'version':VERSION,'problem':problem,'solution':solution if include_solution else None,
          'difficulty':level if include_difficulty else None,'banks':[sorted(x) for x in banks],
          'correct_presence':[not(raw and ((profile=='q-103986' and i==0) or profile=='q-103992')) for i in range(len(banks))]}
 fingerprint=digest(payload);question_id=uid(fingerprint)
 question={':question/id':question_id,':question/problem':problem}
 if include_solution:question[':question/worked-solution']=solution
 if include_difficulty:question[':question/difficulty']=':question.difficulty/'+level
 fields=[]
 for index,bank in enumerate(banks):
  # Legacy bank ordering is incidental; full values and missing key presence are exact.
  field_id=uid(fingerprint+'/field/'+str(index));choices=[]
  for value in bank:
   choices.append({':answer/id':uid(field_id+'/'+value),':answer/type':':answer.type/math',':answer/value':value})
  field={':answer-field/id':field_id,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
  if payload['correct_presence'][index]:
   correct_value=math_values(p,('correct',),'legacy' if (profile=='q-103992' or raw and profile=='q-103986' and index==0) else 'braced')[0]
   field[':answer-field/correct']=[':answer/id',next(c[':answer/id'] for c in choices if c[':answer/value']==correct_value)]
  rng.shuffle(choices);fields.append(field)
 question[':question/answer-fields']=fields
 # Mathematical task identity excludes incidental coefficient in free-copy tasks,
 # complete banks, profiles, named function and argument-order/format aliases.
 task={'role':p['role'],'target':p['target'],
       'workload':'normalize' if profile=='normalized' else 'copy'}
 if p['role']=='dependent':
  task.update(base=p['base'],dependent=p['dependent'],coefficient=str(sp.Rational(p['a'],p['b'])))
 generation={'version':VERSION,**SOURCE,'seed':seed,'template':template,'profile':profile+('_raw' if raw else ''),
 'parameters':{k:p[k] for k in ('base','dependent','a','b','target','argument_order','relation_order','function')},
 'source_ids':([] if profile=='normalized' else [profile]),'origin':'raw observed evidence' if raw else 'authored missing level' if profile=='normalized' else 'parameterized observed mask with documented repairs',
 'evidence_only':raw,'eligible_for_learning':not raw,'task_fingerprint':digest(task),'content_hash':fingerprint,
 'parameter_fingerprint':digest(task),'coordinate_basis':['x','y','z'],'plot_requirement':'none',
 'difficulty_evidence':'unobserved authored workload; uncertain grade' if level=='hard' else 'authored easy assignment to unrated source' if profile=='q-103992' else 'observed label; axis-permutation extension',
 'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},
 'bank_origin':'observed complete bank' if raw or profile!='q-103986' and profile!='normalized' else 'authored complete method-derived bank',
 'recipes':list(recipes),
 'repairs':[] if raw else ['show missing component with a neutral question mark; radio control renders separately']+(['keep supported duplicate field only; use authored whole bank replacing opaque half-linear mask with omitted square'] if profile=='q-103986' else [])+(['repair prose arguments; infer correct free component; author missing solution and easy label'] if profile=='q-103992' else [])+(['clarify direct-coordinate convention; 6z is otherwise a covering parametrization'] if p['role']=='free' else [])}
 result={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':generation}
 if raw:
  # Shared strict formatter cannot require an absent source worked-solution.
  validate_prose(problem)
  if include_solution:validate_prose(solution)
  for bank in banks:
   for value in bank:validate_tex(value)
  generation['math_format']='course-academy-tex-v1'
  return result
 return checked_normal(result)

# EASY: observed coefficient-copy/dependent and free-axis roles, 2..12 coefficient.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: observed reverse relation, base is the second function argument.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: unsupported; public API rejects this uncalibrated draft workload.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question'];lines=[q[':question/problem'],'']
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  lines.append('Field '+str(i+1)+':')
  for c in f[':answer-field/choices']:lines.append('- $'+c[':answer/value']+'$')
 if ':question/worked-solution' in q:lines += ['','Worked solution:',q[':question/worked-solution']]
 return '\n'.join(lines)

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all')
 parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
 parser.add_argument('--format',choices=['markdown','json'],default='markdown')
 parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
 if args.count<1:parser.error('--count must be positive')
 levels=list(SUPPORTED_LEVELS) if args.difficulty=='all' else [args.difficulty]
 rows=[];used=set()
 for level in levels:
  count=0
  for offset in range(10000):
   rec=generate(level,args.seed+offset,template=args.template,profile=args.profile)
   fp=rec['generation']['task_fingerprint']
   if fp in used:continue
   rows.append(rec);used.add(fp);count+=1
   if count==args.count:break
  if count<args.count:raise ValueError('Finite task capacity exhausted: requested '+str(args.count)+'; distinct produced '+str(count))
 print(json.dumps(_apply_source_notation(rows),ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rows))

from source_notation import install as _install_source_notation, apply as _apply_source_notation
_install_source_notation(globals())

if __name__=='__main__':main()
