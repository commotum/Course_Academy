#!/usr/bin/env python3
"""Modeling Inhibited Decay: deterministic Newton cooling equation setup.

Read-only snapshot math/basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1.
The adjacent templates.json contains extracted complete component masks, not
question payloads. All eight source cases use the same parameterized generation
path as changed cases. Source profiles preserve observed complete banks; q106936
is an explicitly raw ambiguous bank (two equivalent WRONG options). Normal easy
output uses a repaired/default whole operation bank. Seven observed solutions
replay exactly; q105917 has an authored shared two-stage solution and inferred
key/level. No fabricated original matches. Source semantic wording slips remain
in raw profiles; normal q106878 describes a body throughout and q106934 soup.

Easy: identify given ambient in a directly stated proportionality relation.
Moderate: identify ambient separately from initial temperature, as captured.
Hard (authored): same generic/substituted Newton cooling setup, with initial and
later observed readings present, as in the actual lesson's Newton tutorial.
No fitting k, initial-value equation, time evaluation, integration or solving.
Hard extra reading discrimination is a design claim, not an observed level.
Within each level all instances have the same two displayed solution stages.

Finite integer sampling policies are documented below; source original values
remain eligible for their respective raw profiles. Explicit invalid parameters
never resample. Full banks are chosen before constructing options; any invalid
member rejects the whole instance. No arbitrary random scalar distractors.
Fixed displayed content has fixed IDs independent of seed/choice order. Task
fingerprints contain ambient and whether additional reading discrimination is
assessed, not distractor banks or incidental times/initial-temperature changes.
Content IDs include full prompt, solution and complete bank. JSON is review data,
never transaction EDN. No database imports, plots or database writes.

CLI: .venv/bin/python generate/scratch/17592186078583.py --difficulty all
Validation: .venv/bin/python generate/scratch/17592186078583/validate.py
"""
from __future__ import annotations
import argparse,hashlib,json,pathlib,random,re,uuid
import sympy as sp
HERE=pathlib.Path(__file__).with_suffix('')
KP_ID=17592186078583
KP_UUID='74a902da-f299-54a3-8e93-ad2716d0e887'
TITLE='Modeling Inhibited Decay'
VERSION='inhibited-decay-modeling-v1'
T,K=sp.symbols('T k',positive=True)
TEMPLATES=json.loads((HERE/'templates.json').read_text())
LEVELS=('easy','moderate','hard')
DEFAULT_TEMPLATES={'easy':['q-105917','q-106936','q-106878'],'moderate':['q-37365','q-106883','q-106934','q-106935','q-106937'],'hard':['observed-reading']}
PROFILE_LEVELS={sid:x['level'] for sid,x in TEMPLATES.items()}|{'easy_default':'easy','oil_repaired':'easy','moderate_default':'moderate','hard_default':'hard'}
INITIAL_BOUNDS={'q-37365':(90,110),'q-106883':(120,180),'q-106934':(140,212),'q-106935':(40,99),'q-106937':(200,450),'observed-reading':(40,99)}
DEFAULT_BANKS={
 'easy_default':[r'-k(T-@@S@@)',r'k(T-@@S@@)',r'-k(T+@@S@@)',r'-kT(T-@@S@@)',r'-kT'],
 'oil_repaired':[r'k(T-@@S@@)',r'-kT(T-@@S@@)',r'-kT',r'-k(T+@@S@@)',r'-k(T-@@S@@)'],
 'moderate_default':[r'-k(T-@@S@@)',r'-k(T-@@I@@)',r'-@@I@@k(T-@@S@@)',r'-k(T-(@@I@@+@@S@@))',r'k(T-@@S@@)'],
 'hard_default':[r'-k(T-@@S@@)',r'-k(T-@@I@@)',r'-k(T-@@M@@)',r'-k(T-(@@I@@-@@S@@))',r'k(T-@@S@@)']}

def digest(data):return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def number(value):
 v=sp.Rational(str(value))
 if v.q!=1:raise ValueError('Integer temperature/time slots only')
 return int(v)
def slot(mask,params):
 if 'I' in params:mask=mask.replace('@@SUM@@',str(params['I']+params['S']))
 for key,value in params.items():mask=mask.replace('@@'+key+'@@',str(value))
 if '@@' in mask:raise ValueError('Unfilled complete component slot')
 return mask

def read_rhs(value):
 """Parse the entire displayed RHS, including implicit multiplication."""
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 rhs=value.split('=',1)[-1].replace('{','').replace('}','').replace(' ','')
 return parse_expr(rhs,local_dict={'T':T,'k':K},transformations=standard_transformations+(implicit_multiplication_application,))

def validate_parameters(level,params,template):
 required={'S'}|({'I'} if level in ('moderate','hard') else set())|({'M','h'} if level=='hard' else set())
 if set(params)!=required:raise ValueError('Exact parameter slots required: '+str(sorted(required)))
 p={k:number(v) for k,v in params.items()}
 # Celsius ambient 10..40; Fahrenheit ambient 50..85. No negative temperature
 # or impossible time/population/cumulative-unit options are authored here.
 unit=TEMPLATES[template]['unit'] if template in TEMPLATES else 'C'
 if not ((10<=p['S']<=40) if unit=='C' else (50<=p['S']<=85)):raise ValueError('Ambient outside level/context bounds')
 if 'I'in p:
  minimum,maximum=INITIAL_BOUNDS[template]
  if not max(minimum,p['S']+10)<=p['I']<=maximum:raise ValueError('Initial reading must exceed ambient by at least 10 within thermal bounds')
 if level=='hard':
  if not p['S']+5<=p['M']<=p['I']-5:raise ValueError('Observed reading must lie strictly between ambient and initial')
  if not 1<=p['h']<=20:raise ValueError('Positive observed minutes bounded 1..20')
 return p

def sample(level,rng,template):
 unit=TEMPLATES[template]['unit'] if template in TEMPLATES else 'C'
 S=rng.randint(10,40) if unit=='C' else rng.randint(50,85)
 p={'S':S}
 if level in ('moderate','hard'):
  minimum,maximum=INITIAL_BOUNDS[template]
  p['I']=rng.randint(max(minimum,S+10),maximum)
 if level=='hard':p.update(M=rng.randint(S+5,p['I']-5),h=rng.randint(1,20))
 return p

def hard_prompt(p):
 return (f"A container of water initially has a temperature of ${{{p['I']}}}^{{∘}}\\text{{C}}.$ After ${p['h']}$ {'minute' if p['h']==1 else 'minutes'} in a room at ${{{p['S']}}}^{{∘}}\\text{{C}},$ its temperature is ${{{p['M']}}}^{{∘}}\\text{{C}}.$ "
 "The temperature $T(t)$ of the water decreases at a rate that obeys Newton's law of cooling. Here, $T$ is measured in degrees Celsius, and $t>0$ is the time in minutes. "
 "Which differential equation could be used to model the water temperature? Assume that $k>0$ is a constant of proportionality.")

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio layout supported')
 rng=random.Random(seed)
 if profile in TEMPLATES:
  if template is not None and template!=profile:raise ValueError('Observed bank belongs to its extracted prose template')
  template=profile
 if template is None:template=rng.choice(DEFAULT_TEMPLATES[level])
 if template not in DEFAULT_TEMPLATES[level]:raise ValueError('Template does not belong to level')
 profile=profile or level+'_default'
 if PROFILE_LEVELS.get(profile)!=level:raise ValueError('Profile outside difficulty')
 if profile=='oil_repaired' and template!='q-106936':raise ValueError('Oil repair belongs to oil template')
 explicit=parameters is not None
 for attempt in range(1000):
  p=validate_parameters(level,parameters if explicit else sample(level,rng,template),template)
  raw=profile in TEMPLATES
  prompt=slot(TEMPLATES[template]['prompt'],p) if template in TEMPLATES else hard_prompt(p)
  solution_mask=TEMPLATES[template]['solution'] if template in TEMPLATES else TEMPLATES['q-106935']['solution']
  solution=slot(solution_mask,p)
  if not raw:
   prompt += ' Write the equation in terms of the given constant $k$.'
   if template=='q-106878':prompt=prompt.replace('temperature of the liquid','temperature of the body')
   if template=='q-106934':prompt=prompt.replace('model the pot temperature','model the soup temperature')
   if template=='q-106936':prompt=prompt.replace('temperature of the liquid','temperature of the oil')
  if raw:values=[slot(v,p) for v in TEMPLATES[profile]['bank']]
  else:values=[r'\frac{\text{d}T}{\text{d}t}='+slot(v,p) for v in DEFAULT_BANKS[profile]]
  expressions=[read_rhs(v) for v in values];target=-K*(T-p['S'])
  correct=[i for i,v in enumerate(expressions) if sp.expand(v-target)==0]
  duplicate=any(sp.expand(a-b)==0 for i,a in enumerate(expressions) for b in expressions[i+1:])
  # Only the documented raw oil source profile retains its duplicate wrong pair.
  if len(correct)!=1 or (duplicate and profile!='q-106936'):
   if explicit:raise ValueError('Whole bank rejected: ambiguity/equivalent member')
   continue
  break
 else:raise ValueError('Could not sample eligible complete bank')
 task={'model':'Newton cooling','ambient':p['S'],'ambient_unit':TEMPLATES[template]['unit'] if template in TEMPLATES else 'C','ambient_selection_from':1 if level=='easy' else 2 if level=='moderate' else 3}
 fingerprint=digest(task)
 content=digest({'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(values)})
 qid=uuid.uuid5(uuid.NAMESPACE_URL,f'course-academy/{KP_UUID}/{VERSION}/{content}');fid=uuid.uuid5(qid,'selection')
 answers=[{':answer/id':str(uuid.uuid5(fid,'math:'+v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 correct_uuid=answers[correct[0]][':answer/id'];rng.shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_uuid]}]},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'profile_origin':'observed structural bank' if raw else 'authored complete operation bank','level_origin':TEMPLATES[template]['level_origin'] if template in TEMPLATES else 'authored hard: additional reading selection, same model setup','source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'domain':'k>0; T>ambient; all times in minutes; temperatures in one declared scale','parameter_fingerprint':fingerprint,'content_fingerprint':content,'raw_ambiguous_bank':profile=='q-106936','sympy_version':sp.__version__}}

# EASY: single ambient, direct rate/difference recognition. No internal progression.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: distinguish initial and surrounding readings, fixed two solution rows.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD, AUTHORED: initial and later observed reading are not the fixed surroundings.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' **[correct]**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=('markdown','json'),default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
 if args.count<1:parser.error('--count must be positive')
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (LEVELS if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
