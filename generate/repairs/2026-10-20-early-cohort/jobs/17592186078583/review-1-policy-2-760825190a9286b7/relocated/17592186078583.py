#!/usr/bin/env python3
"""Newton cooling model setup, math source basis 2710.

Easy and moderate preserve the observed supplied givens, five-option radio
layout and generic/substituted two-stage solution. Hard is unsupported: the
historical authored extra-reading extension changes supplied information.
Raw source profiles are replay-only and retain source defects; normal output
retains easy banks and uses documented mixed-source moderate practice banks.
The oil duplicate repair and TeX/context corrections remain. No ODE solving.
Task fingerprints exclude initial reading, context, seed and choice ordering.
"""
from __future__ import annotations
import argparse,hashlib,json,pathlib,random,re,uuid
import sympy as sp
HERE=pathlib.Path(__file__).with_suffix('')
KP_ID=17592186078583
KP_UUID='74a902da-f299-54a3-8e93-ad2716d0e887'
TITLE='Modeling Inhibited Decay'
VERSION='inhibited-decay-modeling-v2'
GENERATOR_UUID='c45b6027-8b00-59eb-b305-fc6da1e356a3'
SUPPORTED_LEVELS=('easy','moderate')
T,K=sp.symbols('T k',positive=True)
TEMPLATES=json.loads((HERE/'templates.json').read_text())
LEVELS=SUPPORTED_LEVELS
DEFAULT_TEMPLATES={'easy':['q-105917','q-106936','q-106878','q-106932','q-106877'],'moderate':['q-37365','q-106883','q-106934','q-106935','q-106937']}
PROFILE_LEVELS={sid:x['level'] for sid,x in TEMPLATES.items()}|{'oil_repaired':'easy'}
INITIAL_BOUNDS={'q-37365':(90,110),'q-106883':(120,180),'q-106934':(140,212),'q-106935':(40,99),'q-106937':(200,450)}
DEFAULT_BANKS={
 'oil_repaired':[r'k(T-@@S@@)',r'-kT(T-@@S@@)',r'-kT',r'-k(T+@@S@@)',r'-k(T-@@S@@)']}
# Choose a complete practice bank before sampling temperatures. The two
# ambient-sign distractors remove the length-only cue without padding TeX or
# excluding three-digit initial readings. Explicit source profiles stay raw.
MODERATE_FIFTH={
 'q-37365':r'-k(T-@@SUM@@)', 'q-106883':r'-kT(T-@@S@@)',
 'q-106934':r'@@I@@k(T-@@S@@)', 'q-106935':r'-@@I@@k(T-@@S@@)',
 'q-106937':r'-@@I@@k(T-@@S@@)'}
for _template,_fifth in MODERATE_FIFTH.items():
 _profile=_template+'_practice'
 DEFAULT_BANKS[_profile]=[r'-k(T-@@S@@)',r'-k(T-@@I@@)',r'-k(T+@@S@@)',r'k(T-@@S@@)',_fifth]
 PROFILE_LEVELS[_profile]='moderate'

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
 required={'S'}|({'I'} if level=='moderate' else set())
 if set(params)!=required:raise ValueError('Exact parameter slots required: '+str(sorted(required)))
 p={k:number(v) for k,v in params.items()}
 # Celsius ambient 10..40; Fahrenheit ambient 50..85. No negative temperature
 # or impossible time/population/cumulative-unit options are authored here.
 unit=TEMPLATES[template]['unit'] if template in TEMPLATES else 'C'
 if not ((10<=p['S']<=40) if unit=='C' else (50<=p['S']<=85)):raise ValueError('Ambient outside level/context bounds')
 if 'I'in p:
  minimum,maximum=INITIAL_BOUNDS[template]
  if not max(minimum,p['S']+10)<=p['I']<=maximum:raise ValueError('Initial reading must exceed ambient by at least 10 within thermal bounds')
 return p

def sample(level,rng,template):
 unit=TEMPLATES[template]['unit'] if template in TEMPLATES else 'C'
 S=rng.randint(10,40) if unit=='C' else rng.randint(50,85)
 p={'S':S}
 if level=='moderate':
  minimum,maximum=INITIAL_BOUNDS[template]
  p['I']=rng.randint(max(minimum,S+10),maximum)
 return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio layout supported')
 rng=random.Random(seed)
 source_replay=profile in TEMPLATES
 if profile in TEMPLATES:
  if template is not None and template!=profile:raise ValueError('Observed bank belongs to its extracted prose template')
  template=profile
 if template is None:template=rng.choice(DEFAULT_TEMPLATES[level])
 if template not in DEFAULT_TEMPLATES[level]:raise ValueError('Template does not belong to level')
 profile=profile or ('oil_repaired' if template=='q-106936' else template+'_practice' if level=='moderate' else template)
 if PROFILE_LEVELS.get(profile)!=level:raise ValueError('Profile outside difficulty')
 if profile=='oil_repaired' and template!='q-106936':raise ValueError('Oil repair belongs to oil template')
 if profile.endswith('_practice') and profile!=template+'_practice':raise ValueError('Practice bank belongs to its context')
 explicit=parameters is not None
 for attempt in range(1000):
  p=validate_parameters(level,parameters if explicit else sample(level,rng,template),template)
  raw=source_replay
  prompt=slot(TEMPLATES[template]['prompt'],p) if template in TEMPLATES else None
  solution_mask=TEMPLATES[template]['solution'] if template in TEMPLATES else TEMPLATES['q-106935']['solution']
  solution=slot(solution_mask,p)
  if not raw:
   prompt += ' Write the equation in terms of the given constant $k$.'
   if template=='q-106878':prompt=prompt.replace('temperature of the liquid','temperature of the body')
   if template=='q-106934':prompt=prompt.replace('model the pot temperature','model the soup temperature')
   if template=='q-106936':prompt=prompt.replace('temperature of the liquid','temperature of the oil')
   if template=='q-106932':prompt=prompt.replace('temperature of the liquid','temperature of the chocolate')
  if profile in TEMPLATES:
   values=[slot(v,p) for v in TEMPLATES[profile]['bank']]
   if not raw:values=[v.replace('\\\\','\\') for v in values]
  else:values=[r'\frac{\text{d}T}{\text{d}t}='+slot(v,p) for v in DEFAULT_BANKS[profile]]
  expressions=[read_rhs(v) for v in values];target=-K*(T-p['S'])
  correct=[i for i,v in enumerate(expressions) if sp.expand(v-target)==0]
  duplicate=any(sp.expand(a-b)==0 for i,a in enumerate(expressions) for b in expressions[i+1:])
  # Only the documented raw oil source profile retains its duplicate wrong pair.
  if len(correct)!=1 or (duplicate and not (raw and profile=='q-106936')):
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
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_uuid]}]},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'profile_origin':'raw observed source bank' if raw else 'documented oil duplicate repair' if profile=='oil_repaired' else 'authored mixed-source moderate bank removing length cue' if profile.endswith('_practice') else 'complete observed bank with TeX/context corrections','level_origin':TEMPLATES[template]['level_origin'] if template in TEMPLATES else 'authored hard: additional reading selection, same model setup','source':{'database':'math','basis':5389 if template=='q-106877' else 2710,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'domain':'k>0; T>ambient; all times in minutes; temperatures in one declared scale','parameter_fingerprint':fingerprint,'content_fingerprint':content,'raw_ambiguous_bank':raw and profile=='q-106936','sympy_version':sp.__version__}}

# EASY: single ambient, direct rate/difference recognition. No internal progression.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: distinguish initial and surrounding readings, fixed two solution rows.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# No supported hard template under the observed backbone.
def generate_hard(*args,**kwargs):raise ValueError('Unsupported hard: no same-backbone source evidence')

def markdown(record):
 q=record['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' **[correct]**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=('markdown','json'),default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
 if args.count<1:parser.error('--count must be positive')
 records=[];seen=set()
 for level in (LEVELS if args.difficulty=='all' else (args.difficulty,)):
  accepted=0
  for offset in range(10000):
   r=generate(level,args.seed+offset,template=args.template,profile=args.profile)
   fp=r['generation']['parameter_fingerprint']
   if fp in seen:continue
   seen.add(fp);records.append(r);accepted+=1
   if accepted==args.count:break
  if accepted<args.count:parser.error(f'Finite task domain: requested {args.count}, found {accepted} for {level}')
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
