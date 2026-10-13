#!/usr/bin/env python3
"""Units of first derivatives. Local review only; no EDB writes.

Observed contextual templates preserve their complete five-choice banks and
four-stage solution prose. Unit lexemes are parameterized, rather than source
question payloads returned. Missing-level authored extensions retain the same
operation: dependent units divided by independent units. No differentiation,
numerical conversion, second derivatives, or inverse-function calculation.
Raw farmer evidence is available via profile='raw_observed'; it deliberately
has no correct ref because the displayed bank contains no correct answer.
See evidence classification/extraction for supported source repairs.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186064271
KP_UUID='0fa5bdf9-4b27-5565-9ee1-ecb9f9db4791'
TITLE='Determining the Units of a Derivative'
VERSION='units-derivative-1'
EVIDENCE=Path(__file__).with_suffix('')
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
# Symbols denote named quantity units, not merely physical dimensions. Counts
# retain their object type, and familiar scaled units keep exact scale factors.
M,T,L,C,P,E,Temp=sp.symbols('mass time length dollar point euro temperature',positive=True)
UNITS={
 'gram':('grams',M), 'kilogram':('kilograms',1000*M),
 'milliliter':('milliliters',L**3/1000000), 'liter':('liters',L**3/1000),
 'centimeter':('centimeters',L/100), 'meter':('meters',L),
 'second':('seconds',T), 'minute':('minutes',60*T), 'hour':('hours',3600*T),
 'dollar':('dollars',C), 'euro':('euros',E), 'point':('points',P),
 'ton':('tons',1000000*M), 'degree Fahrenheit':('degrees Fahrenheit',Temp),
 'cupcake':('cupcakes',sp.Symbol('cupcake',positive=True)),
 'visitor':('visitors',sp.Symbol('visitor',positive=True)),
 'visit':('visits',sp.Symbol('visit',positive=True)),
 'item':('items',sp.Symbol('item',positive=True)),
 'package':('packages',sp.Symbol('package',positive=True)),
 'student':('students',sp.Symbol('student',positive=True)),
 'ticket':('tickets',sp.Symbol('ticket',positive=True)),
}
DEFS=json.loads((EVIDENCE/'templates.json').read_text())
TEMPLATES={k:{'level':'easy','origin':'observed','sources':[v['source_id']]} for k,v in DEFS.items()}
TEMPLATES['farmer']['level']='hard'  # Unrated source: authored workload assignment.
TEMPLATES.update({'non_time_power':{'level':'moderate','origin':'authored','sources':[]},'price_rate':{'level':'hard','origin':'authored','sources':[]}})

def atom(k,power=1,plural=True,style='prefix'):
 s=UNITS[k][0] if plural else k
 if power==1:return s
 if style=='suffix':return s+(' squared' if power==2 else ' cubed')
 return ('squared ' if power==2 else 'cubic ')+s

def expression(k,power=1):return UNITS[k][1]**power

def render_terms(p,spec):
 # Complete term recipe (unit slot, exponent, plurality, power spelling),
 # optionally followed by one denominator term. No numerical distractor fits.
 def term(t):
  slot,pow,plural,style=t
  return atom(p[slot],pow,plural,style)
 return term(spec[0])+(' per '+term(spec[1]) if len(spec)==2 else '')

def value_terms(p,spec):
 vals=[expression(p[t[0]],t[1]) for t in spec]
 return vals[0]/vals[1] if len(vals)==2 else vals[0]

def uid(tag):return str(uuid.uuid5(uuid.UUID(KP_UUID),tag))
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def sample_observed(template,rng):
 d=DEFS[template];p=d['parameters'].copy()
 for slot,eligible in d['eligible'].items():p[slot]=rng.choice(eligible)
 if template=='cupcake':p['alt']={'gram':'kilogram','kilogram':'gram'}[p['u']]
 if template=='milk':p['alt']={'liter':'milliliter','milliliter':'liter'}[p['v']]
 return p

def validate_parameters(level,template,p):
 expected=set(DEFS[template]['parameters']) if template in DEFS else {'u','v','power'}
 if set(p)!=expected:raise ValueError('Explicit parameters must have exactly '+str(expected))
 for k,v in p.items():
  if k!='power' and v not in UNITS:raise ValueError('Unknown unit')
 if template in DEFS:
  for slot,eligible in DEFS[template]['eligible'].items():
   if p[slot] not in eligible:raise ValueError('Unit is outside contextual domain')
  # Aliases not exposed as incidental parameters.
  if template=='cupcake' and p['alt']!={'gram':'kilogram','kilogram':'gram'}[p['u']]:raise ValueError('Alternate mass unit must be the other supported unit')
  if template=='milk' and p['alt']!={'liter':'milliliter','milliliter':'liter'}[p['v']]:raise ValueError('Alternate volume unit must be the other supported unit')
 elif template=='non_time_power':
  if p['u'] not in ('centimeter','meter') or p['v'] not in ('item','package','ticket','cupcake') or p['power'] not in (2,3):raise ValueError('Moderate requires a powered length quantity and a count input')
 elif template=='price_rate':
  if p['u'] not in ('ton','kilogram','liter','meter','item','package','ticket','cupcake') or p['v'] not in ('dollar','euro') or p['power']!=1:raise ValueError('Hard requires quantity per price-per-quantity; one compound input')


def observed_content(template,p,profile):
 d=DEFS[template]
 tokens={key:atom(p[slot],power,plural,style) for key,slot,power,plural,style in d['tokens']}
 def fill(s):
  for token,value in tokens.items():s=s.replace(token,value)
  return s
 prompt=fill(d['prompt']);solution=fill(d['solution'])
 bank=[render_terms(p,s) for s in d['bank']]
 vals=[value_terms(p,s) for s in d['bank']]
 if d.get('capital_bank'):bank=[s[0].upper()+s[1:] for s in bank]
 target=expression(p['u'],d['u_power'])/expression(p['v'],d['v_power'])
 if template=='farmer':
  # p is dollars/ton, so tons/(dollars/ton)=tons^2/dollar.
  target=expression(p['u'])**2/expression(p['v'])
  if profile!='raw_observed':
   bank[-1]=atom(p['u'],2)+' per '+atom(p['v'],plural=False)
   vals[-1]=target
 if template=='website':
  # Exact observed prose refers to visitors while prompt says visits. Minimal
  # semantic repair in normal output; observed profile keeps raw teaching text.
  if profile!='observed':solution=solution.replace('visitors','visits').replace('visitor','visit')
  p2=p.copy();p2['u']='visit';bank=[render_terms(p2,s) for s in d['bank']];vals=[value_terms(p2,s) for s in d['bank']]
  target=expression('visit')/expression(p['v'])
 return prompt,solution,bank,vals,target


def authored_content(template,p):
 u,v,power=p['u'],p['v'],p['power']
 U=atom(u,power);V=atom(v);D=r'\frac{\text{d}Q}{\text{d}x}'
 if template=='non_time_power':
  prompt=f'A production process uses $Q(x)$ {U} of material to make $x$ {V}. What are the units of ${D}?$'
  target=expression(u,power)/expression(v)
  correct=U+' per '+atom(v,plural=False)
  bank=[correct,atom(v)+' per '+atom(u,power,False),atom(u)+' per '+atom(v,plural=False),U,V]
  vals=[target,1/target,expression(u)/expression(v),expression(u,power),expression(v)]
  unit_ratio=r'\frac{\text{'+U+r'}}{\text{'+V+'}}'
 else:
  V=atom(v)+' per '+atom(u,plural=False)
  prompt=f'A supplier sells $Q(x)$ {atom(u)} of a product at a price of $x$ {V}. What are the units of ${D}?$'
  target=expression(u)**2/expression(v)
  correct=atom(u,2)+' per '+atom(v,plural=False)
  bank=[correct,atom(u)+' per '+atom(v,plural=False),atom(v)+' per '+atom(u,2,False),atom(v)+' per '+atom(u,plural=False),atom(u)]
  vals=[target,expression(u)/expression(v),1/target,expression(v)/expression(u),expression(u)]
  unit_ratio=r'\frac{\text{'+atom(u)+r'}}{\text{'+V+r'}}=\frac{\text{'+atom(u,2)+r'}}{\text{'+atom(v)+'}}'
 solution=(f'We have that the quantity $Q(x)$ is measured in {U} and the input $x$ is measured in {V}. \n\n'
  +r'$$'+'\n'+r'\begin{aligned}Q(x): & \text{'+U+r'} \\ x: & \text{'+V+r'}\end{aligned}'+'\n$$\n\n'
  +f'The derivative ${D}$ measures a change in $Q(x)$ over a change in $x.$ So, it represents a ratio of the units:\n\n'
  +'$$\n'+r'\begin{aligned}'+D+': & '+unit_ratio+r'\end{aligned}'+'\n$$\n\n'
  +f'Therefore, ${D}$ is measured in "{correct}".')
 return prompt,solution,bank,vals,target


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio fields supported')
 rng=random.Random(seed)
 eligible=[k for k,v in TEMPLATES.items() if v['level']==level]
 template=template or rng.choice(eligible)
 if template not in eligible:raise ValueError('Template does not belong to level')
 observed=template in DEFS
 allowed=(('raw_observed','repaired','authored_default') if template=='farmer' else ('observed','authored_default')) if observed else ('authored_default',)
 profile=profile or ('repaired' if template=='farmer' else 'authored_default' if not observed or template=='website' else 'observed')
 if profile not in allowed:raise ValueError('Unknown profile')
 if profile=='raw_observed' and template!='farmer':raise ValueError('Raw invalid replay is only for farmer')
 if parameters is None:
  if observed:p=sample_observed(template,rng)
  elif level=='moderate':p={'u':rng.choice(('centimeter','meter')),'v':rng.choice(('item','package','ticket','cupcake')),'power':rng.choice((2,3))}
  else:p={'u':rng.choice(('ton','kilogram','liter','meter','item','package','ticket','cupcake')),'v':rng.choice(('dollar','euro')),'power':1}
 else:p=parameters.copy()
 validate_parameters(level,template,p)
 prompt,solution,bank,vals,target=(observed_content(template,p,profile) if observed else authored_content(template,p))
 raw=profile=='raw_observed'
 if len(set(bank))!=5 or any(a==b for i,a in enumerate(vals) for b in vals[i+1:]):raise ValueError('Whole bank has duplicate/equivalent choices')
 matches=[i for i,v in enumerate(vals) if v==target]
 if (len(matches)!=1) and not raw:raise ValueError('Whole bank lacks a unique correct choice')
 signature={'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(bank),'correct':None if raw else bank[matches[0]]}
 identity=digest(signature);fid=uid('field:'+identity)
 choices=[{':answer/id':uid('answer:'+fid+':'+value),':answer/type':':answer.type/text',':answer/value':value} for value in bank]
 correct=None if raw else choices[matches[0]][':answer/id']
 rng.shuffle(choices)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
 if correct:field[':answer-field/correct']=[':answer/id',correct]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':uid('question:'+identity),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'source':SOURCE,'level':level,'seed':seed,'template':template,'profile':profile,'parameters':p,'origin':TEMPLATES[template]['origin'],'sources':TEMPLATES[template]['sources'],'bank_origin':DEFS[template].get('bank_origin','observed') if observed else 'authored','mathematical_fingerprint':digest({'dependent':str(expression('visit' if template=='website' else p['u'],DEFS[template]['u_power'] if observed else p['power'])),'independent':str(expression(p['v'],DEFS[template]['v_power'] if observed else 1)/expression(p['u']) if template in ('farmer','price_rate') else expression(p['v'],DEFS[template]['v_power'] if observed else 1))}),'content_fingerprint':identity,'plot_rating':'none','raw_invalid_evidence':raw,'raw_solution_evidence':template=='website' and profile=='observed','normal_output_eligible':not(raw or (template=='website' and profile=='observed'))}}

# EASY: observed atomic and volume/rate-unit labels; unit choice is categorical.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# MODERATE (authored): powered quantity label / count; no unit conversion.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# HARD (authored): quantity / (currency / same quantity); one compound input.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 levels=('easy','moderate','hard') if a.difficulty=='all' else (a.difficulty,)
 records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
