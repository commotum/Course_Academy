#!/usr/bin/env python3
"""Polar point conversion, steps 3–7, frozen math basis 1356.

Private component masks retain all source prompt/solution rows. Raw profiles are
public evidence-only parameterized replays; incomplete/opaque banks never enter
normal sampling. All normal instances use direct r*cos(theta), r*sin(theta),
familiar unit-circle angles, exact arithmetic, and two components only. No EDB,
plotting, registration, or unrelated radius recovery/angle conversion exercises.
See the adjacent classification, extraction, validation and review evidence.
"""
from __future__ import annotations

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186092217-source-policy.json'))
    raise SystemExit(0)

import argparse,hashlib,json,pathlib,random,re,sys,uuid
import sympy as sp
KP_ID=17592186092217
TITLE='Finding the Cartesian Coordinates of a Point Given in Polar Coordinates'
KP_UUID='7f65d032-9acc-5fe6-b7c2-b8293576cb4c'
VERSION='polar-cartesian-1.0'
DIR=pathlib.Path(__file__).with_suffix('')
RECIPES=json.loads((DIR/'recipes.json').read_text())
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
FAMILIES={'easy':['axis_radian_blank','radian_blank','degree_blank','degree_repeated_radio'],
          'moderate':['degree_radio','radian_blank','degree_blank'],
          'hard':['radian_blank','degree_blank','degree_radio','degree_repeated_radio']}
DEGREES=(0,30,45,60,90,120,135,150,180,210,225,240,270,300,315,330)
NONAXIS=tuple(d for d in DEGREES if d%90)
# Complete historical banks: component patterns, NOT recovered author intent.
# Symbols X,Y are the Cartesian components; C,S are unit-circle components.
RAW_BANKS={
'q-8513':['(-X,Y/2)','(X,Y/2)','(X/2,Y/2)','(X,-Y)','(X,Y)'],
'q-8521':['(X,Y)','(Y,X)','(-R*sqrt(2)/2,-R*sqrt(2)/2)','(3/2,Y)','(-R*sqrt(2)/4,Y)'],
'q-120311':['(-R/2,-sqrt(2))','(X,Y)','(-R/2,R/2)','(-X,-1)','(-X,-R/2)'],
'q-8519':['(-X,-Y)','(X,Y)','(X,-Y)','(-R/4,-Y)','(-R/2,-1/2)']}
BANK_NAMES=['correct','reverse_x_sign','reverse_y_sign','reverse_both_signs','omit_radius']

def tex(v):
 return sp.latex(sp.simplify(v)).replace(' ','')
def tuple_tex(v,space=False):return '('+tex(v[0])+(','+' ' if space else ',')+tex(v[1])+')'
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def uid(*parts):return str(uuid.uuid5(uuid.NAMESPACE_URL,'polar-cartesian:'+':'.join(map(str,parts))))
def fill(mask,slots):
 # Slot values are complete mathematical components. Field placeholders survive.
 for k,v in slots.items():mask=mask.replace('{{'+k+'}}',v)
 return mask

def exact_input(p):
 if set(p)!= {'radius','angle','unit'}:raise ValueError('Parameters must be radius, angle, unit')
 if p['unit'] not in ('degrees','radians'):raise ValueError('Unit must be degrees or radians')
 try:r=sp.sympify(p['radius']);a=sp.sympify(p['angle'])
 except Exception as e:raise ValueError('Invalid exact parameters') from e
 if r.has(sp.Float) or a.has(sp.Float) or not r.is_real or not r.is_finite or not a.is_Rational:raise ValueError('Finite real radius and rational angle required')
 d=a if p['unit']=='degrees' else a*180
 if d not in DEGREES:raise ValueError('Use one familiar special angle in [0,360)')
 if not r>0 or r>12:raise ValueError('Positive radius at most 12 required')
 return r,a,int(d)

def angle_tex(a,unit,t):
 if unit=='degrees':return (str(a)+r'^{∘}') if t=='legacy_degree_radio' else '{'+str(a)+r'}^{∘}'
 if a==0:return '0'
 num,den=a.as_numer_denom(); pi='π' if t=='legacy_radian_radio' else r'\pi '
 top=('' if num==1 else str(num))+pi
 return top.rstrip() if den==1 else r'\frac{'+top+'}{'+str(den)+'}'

def expected_unit(t):return 'radians' if 'radian' in t else 'degrees'

def guard(level,t,r,d,raw):
 if expected_unit(t)!= ('radians' if 'radian' in t else 'degrees'):raise ValueError('Invalid template')
 if raw:
  if RECIPES[t]['difficulty_present'] and level!=RECIPES[t]['level']:raise ValueError('Raw rated source must retain observed difficulty')
  return
 if t not in FAMILIES[level]:raise ValueError('Template not supported at this level')
 if level=='easy':
  if not r.is_Integer or r%2 or not 2<=r<=12:raise ValueError('Easy: even integer radius 2..12')
  if t=='axis_radian_blank' and d%90:raise ValueError('Axis family requires a quadrantal angle')
  if t!='axis_radian_blank' and not d%90:raise ValueError('Nonaxis family requires a nonquadrantal angle')
 elif level=='moderate':
  if not r.is_Integer or r%2!=1 or not 3<=r<=11 or not d%90:raise ValueError('Moderate: odd integer radius 3..11, nonaxis angle')
 else:
  # Exactly one familiar radical in r; trig multiplication cancels its square.
  root=2 if d%90==45 else 3
  k=sp.simplify(r/sp.sqrt(root))
  if not k.is_Integer or not 1<=k<=6 or not d%90:raise ValueError('Hard: radius k sqrt(2) at 45-degree references or k sqrt(3) at 30/60-degree references, k=1..6')

def sample(level,t,rng):
 ds=(0,90,180,270) if t=='axis_radian_blank' else NONAXIS
 d=rng.choice(ds)
 if level=='easy':r=rng.choice((2,4,6,8,10,12))
 elif level=='moderate':r=rng.choice((3,5,7,9,11))
 else:r=rng.randint(1,6)*sp.sqrt(2 if d%90==45 else 3)
 unit=expected_unit(t);a=sp.Rational(d,180) if unit=='radians' else sp.Integer(d)
 return {'radius':str(r),'angle':str(a),'unit':unit}

def solution_slots(t,r,a,unit,c,s,x,y):
 at=angle_tex(a,unit,t);rt=tex(r);slots={'polar':'('+rt+(', ' if t.startswith('legacy') else ',')+at+')','cartesian':tuple_tex((x,y))}
 for coordinate,fn,trig,result in [('x','cos',c,x),('y','sin',s,y)]:
  op=r'\operatorname{'+fn+'}⁡'
  slots[coordinate+'_sub']=rt+(r'\cdot ' if t=='axis_radian_blank' else '')+op+'('+at+')'
  tt=tex(trig)
  if t in ('degree_radio','degree_blank'):mul=rt+'('+tt+')'
  elif t=='radian_blank':mul=rt+r'\cdot '+('('+tt+')' if coordinate=='x' else tt)
  else:mul=rt+r'\cdot '+tt
  slots[coordinate+'_mul']=mul;slots[coordinate+'_final']=tex(result)
 return slots

def raw_bank(sid,r,x,y):
 env={'R':r,'X':x,'Y':y,'sqrt':sp.sqrt}
 return [tuple(sp.simplify(v) for v in sp.sympify(recipe,locals=env)) for recipe in RAW_BANKS[sid]]

def make(level,seed,t,p,profile):
 rec=RECIPES[t];raw=bool(profile and profile.startswith('raw-'));sid=rec['source_id']
 if raw and profile!='raw-'+sid:raise ValueError('Raw profile belongs to another template')
 if t.startswith('legacy') and not raw:raise ValueError('Incomplete legacy family is evidence only')
 r,a,d=exact_input(p)
 if p['unit']!=expected_unit(t):raise ValueError('Wrong angle unit for this template')
 guard(level,t,r,d,raw)
 theta=sp.Rational(d,180)*sp.pi;c=sp.cos(theta);s=sp.sin(theta);x=sp.simplify(r*c);y=sp.simplify(r*s)
 slots=solution_slots(t,r,a,p['unit'],c,s,x,y)
 problem=fill(rec['prompt_mask'],slots)
 solution=fill(rec['solution_mask'],slots) if 'solution_mask' in rec else None
 if not raw and solution is not None:solution=solution.replace('coordinate od ','coordinate of ')
 is_radio=rec['fields'][0]['type'].endswith('/radio')
 if is_radio:
  if raw:values=raw_bank(sid,r,x,y)
  else:values=[(x,y),(-x,y),(x,-y),(-x,-y),(c,s)]
  if len({tuple(map(str,v)) for v in values})!=len(values):raise ValueError('Whole bank rejected: equivalent options')
  if sum(v==(x,y) for v in values)!=1:raise ValueError('Whole bank rejected: missing/ambiguous correct option')
  # Preserve original per-option comma spacing as an independent component mask.
  displayed=[tuple_tex(v,raw and sid=='q-8513' and i in (0,1,2,4)) for i,v in enumerate(values)]
 else:displayed=[]
 fields=[]
 canonical=[problem,solution,displayed,[(f['key'],f['type']) for f in rec['fields']],level if not raw or rec['difficulty_present'] else None]
 content=digest([VERSION,canonical]);qid=uid(content)
 for i,f in enumerate(rec['fields']):
  key=f['key'];fid=uid(qid,'field',key)
  strings=displayed if is_radio else [tex(x if key=='field-1' else y)]
  choices=[{':answer/id':uid(fid,v),':answer/type':f['answer_type'],':answer/value':v} for v in strings]
  field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':f['type'],':answer-field/choices':choices}
  if not raw or f['correct_present']:
   ci=values.index((x,y)) if is_radio else 0
   field[':answer-field/correct']=[':answer/id',choices[ci][':answer/id']]
  if is_radio:random.Random(seed).shuffle(choices)
  fields.append(field)
 q={':question/id':qid,':question/problem':problem,':question/answer-fields':fields}
 if not raw or rec['difficulty_present']:q[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:q[':question/worked-solution']=solution
 task=digest(['direct-polar-to-cartesian',tex(x),tex(y)])
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{
 'version':VERSION,'source':SOURCE,'template':t,'level':level,'seed':seed,'parameters':{k:str(v) for k,v in p.items()},
 'profile':profile or ('method-sign-scale' if is_radio else 'coordinate-blanks'),'raw_evidence':raw,
 'eligible_for_learning':not raw,'evidence_only':raw,'origin':'observed component masks / authored parameter bounds and method bank' if not raw else 'observed raw component-pattern replay',
 'mathematical_fingerprint':task,'content_fingerprint':content,'bank_recipes':RAW_BANKS.get(sid) if raw and is_radio else BANK_NAMES if is_radio else [],
 'domain':'familiar exact angle in [0,360), positive radius <=12; normal level-specific guards',
 'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plot_rating':'none'}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in FAMILIES:raise ValueError('Unknown difficulty')
 rng=random.Random(seed)
 if profile and profile.startswith('raw-'):
  candidates=[t for t,v in RECIPES.items() if v['source_id']==profile[4:]]
 else:candidates=list(FAMILIES[level])
 if profile=='method-sign-scale':candidates=[t for t in candidates if RECIPES[t]['fields'][0]['type'].endswith('/radio')]
 if profile=='coordinate-blanks':candidates=[t for t in candidates if RECIPES[t]['fields'][0]['type'].endswith('/blank')]
 if field_type:
  ft=field_type.rsplit('/',1)[-1]
  candidates=[t for t in candidates if RECIPES[t]['fields'][0]['type'].endswith('/'+ft)]
 if template:
  if template not in candidates:raise ValueError('Template incompatible with level/profile/type')
  candidates=[template]
 if not candidates:raise ValueError('No eligible template')
 # Select whole family and bank BEFORE parameters. Never pool/replace distractors.
 t=rng.choice(candidates)
 if profile not in (None,'method-sign-scale','coordinate-blanks') and not profile.startswith('raw-'):raise ValueError('Unknown bank profile')
 if profile=='method-sign-scale' and not RECIPES[t]['fields'][0]['type'].endswith('/radio'):raise ValueError('Radio bank requires radio family')
 if profile=='coordinate-blanks' and not RECIPES[t]['fields'][0]['type'].endswith('/blank'):raise ValueError('Blank profile requires blanks')
 if parameters is not None:return make(level,seed,t,dict(parameters),profile)
 if profile and profile.startswith('raw-'):raise ValueError('Evidence replay requires explicit parameters')
 for _ in range(100):
  p=sample(level,t,rng)
  try:return make(level,seed,t,p,profile)
  except ValueError as e:
   if 'Whole bank' not in str(e):raise
 raise ValueError('No eligible whole instance')

# Easy: observed even-integer radii, axis or familiar special-angle conversion.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: observed direct-conversion route; authored odd radius retains halves.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: authored radical radius; the same two products require radical cancellation.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question'];meta=record['generation'];difficulty=q.get(':question/difficulty','unrated').rsplit('/',1)[-1]
 out=['### '+('Original evidence' if meta['raw_evidence'] else 'Generated variant')+' — '+difficulty,q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  correct=f.get(':answer-field/correct',[None,None])[1]
  out += [f[':answer-field/key']+': '+', '.join('$'+a[':answer/value']+'$'+(' **(correct)**' if a[':answer/id']==correct else '') for a in f[':answer-field/choices'])]
  if correct is None:out += ['Original correct designation: absent.']
 if ':question/worked-solution' in q:out += [q[':question/worked-solution']]
 return '\n\n'.join(out)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 levels=FAMILIES if a.difficulty=='all' else [a.difficulty]
 records=[generate(l,a.seed+i,a.template,profile=a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186092217-source-policy.json'))

if __name__=='__main__':main()
