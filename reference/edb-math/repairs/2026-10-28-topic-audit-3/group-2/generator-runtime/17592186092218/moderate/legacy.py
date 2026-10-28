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
import argparse,hashlib,json,pathlib,random,re,sys,uuid
import sympy as sp
KP_ID=17592186092218
TITLE='Finding the Cartesian Coordinates of a Point Given a Description of the Radius and Angle'
KP_UUID='87f80908-037b-56ae-a2b5-59bdc49f0acb'
VERSION='described-polar-cartesian-1.0'
DIR=pathlib.Path(__file__).parent/'replay_data'
RECIPES=json.loads((DIR/'recipes.json').read_text())
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
FAMILIES={'easy':['degree_unrepeated_radio','radian_mixed_radio','radian_blank','degree_blank'],
          'moderate':list(RECIPES),
          'hard':[t for t in RECIPES if not t.startswith('axis')]}
DEGREES=(0,30,45,60,90,120,135,150,180,210,225,240,270,300,315,330)
NONAXIS=tuple(d for d in DEGREES if d%90)
MODERATE_RADII=tuple(sp.Integer(i) for i in range(2,13))+tuple(sp.Rational(1,i) for i in range(2,7))+(sp.Rational(3,2),sp.Rational(5,2),sp.Rational(7,3))
# Complete historical banks: component patterns, NOT recovered author intent.
# Symbols X,Y are the Cartesian components; C,S are unit-circle components.
RAW_BANKS={
'q-17133':['(-R/2,R*sqrt(3)/2)','(R/2,-R*sqrt(3)/2)','(-R*sqrt(3)/2,-R*sqrt(3)/2)','(-R*sqrt(3)/2,R/2)','(R/2,-R/2)'],
'q-8522':['(-R*sqrt(2)/2,R)','(R*sqrt(2)/2,-R/2)','(R*sqrt(3)/2,-R)','(R,R*sqrt(2)/2)','(R*sqrt(3)/2,-R/2)'],
'q-120328':['(X,Y)','(X/2,Y/2)','(R*sqrt(3)/3,-R*sqrt(3)/3)','(-R*sqrt(2),R*sqrt(2))','(R*sqrt(3)/9,-R*sqrt(3)/9)'],
'q-17124':['(-sqrt(2)/(1/R+1),-sqrt(2)/(1/R+1))','(-sqrt(2)/2,-sqrt(2)/2)','(-R*sqrt(2),-R*sqrt(2))','(X,Y)','(-sqrt(2)/(1/R+2),-sqrt(2)/(1/R+2))'],
'q-17126':['(-X,-Y)','(X,-Y)','(X,-R*sqrt(3)/2)','(-X,Y)','(X,Y)'],
'q-17128':['(0,R)','(0,1)','(0,-R)','(R,0)','(-R,0)'],
'q-17134':['(-X,Y)','(X,-Y/2)','(-X,-Y/2)','(X,Y)','(-X,-Y)'],
'q-17137':['(0,R)','(R,1)','(R,0)','(1,0)','(-R,0)'],
'q-8516':['(-X,R*sqrt(3)/4)','(-X,Y)','(X,R*sqrt(2)/2)','(X,Y)','(X,R*sqrt(3))']}
SUPPORTED_BANKS={'radian_mixed_radio':'source-sign-root','radian_repeated_radio':'source-sign-half','axis_radian_radio':'source-axis-down','axis_zero_radio':'source-axis-right'}
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
 if not r>0 or r>24:raise ValueError('Positive radius at most 24 required')
 return r,a,int(d)

def expected_unit(t):return 'radians' if 'radian' in t or t=='axis_zero_radio' else 'degrees'

def angle_tex(a,unit,t):
 if unit=='degrees':return str(a)+r'^{∘}' if t=='legacy_degree_radio' else '{'+str(a)+r'}^{∘}'
 if a==0:return '0'
 num,den=a.as_numer_denom();pi='π' if t=='legacy_radian_radio' else r'\pi '
 top=('' if num==1 else str(num))+pi
 return top.rstrip() if den==1 else r'\frac{'+top+'}{'+str(den)+'}'

def guard(level,t,r,d,raw):
 if raw:
  if RECIPES[t]['difficulty_present'] and level!=RECIPES[t]['level']:raise ValueError('Raw rated source must retain observed difficulty')
  # Evidence profiles intentionally preserve incomplete or opaque banks, but do not accept unrelated angles.
  case=next(c for c in json.loads((DIR/'source-cases.json').read_text()) if c['template']==t)
  original_d=sp.sympify(case['parameters']['angle'])*(180 if case['parameters']['unit']=='radians' else 1)
  if d!=original_d:raise ValueError('Raw bank angle is evidence-bound; radius can vary')
  return
 if t not in FAMILIES[level]:raise ValueError('Template not supported at this level')
 if level=='easy':
  if r!=1 or not d%90:raise ValueError('Easy: unit radius and familiar nonaxis angle')
 elif level=='moderate':
  if r not in MODERATE_RADII:raise ValueError('Moderate: integer 2..12, reciprocal 1/2..1/6, or 3/2, 5/2, 7/3')
  if t=='axis_radian_radio' and d!=270:raise ValueError('Axis down family requires 270 degrees')
  if t=='axis_zero_radio' and d!=0:raise ValueError('Axis right family requires zero angle')
  if not t.startswith('axis') and not d%90:raise ValueError('Nonaxis family requires a nonquadrantal angle')
 else:
  root=2 if d%90==45 else 3;k=sp.simplify(r/sp.sqrt(root))
  if not k.is_Integer or not 1<=k<=6 or not d%90:raise ValueError('Hard: k sqrt(2) at 45-degree references or k sqrt(3) at 30/60-degree references, k=1..6')

def sample(level,t,rng):
 d=270 if t=='axis_radian_radio' else 0 if t=='axis_zero_radio' else rng.choice(NONAXIS)
 if level=='easy':r=sp.Integer(1)
 elif level=='moderate':r=rng.choice(MODERATE_RADII)
 else:r=rng.randint(1,6)*sp.sqrt(2 if d%90==45 else 3)
 # Supported bank constraints are selected before these parameters, keeping their whole bank.
 if level!='easy' and t=='radian_mixed_radio':d=315
 if level!='easy' and t=='radian_repeated_radio':d=240
 if level=='hard':r=rng.randint(1,6)*sp.sqrt(2 if d%90==45 else 3)
 unit=expected_unit(t);a=sp.Rational(d,180) if unit=='radians' else sp.Integer(d)
 return {'radius':str(r),'angle':str(a),'unit':unit}

def solution_slots(t,r,a,unit,c,s,x,y):
 at=angle_tex(a,unit,t);rt=tex(r);slots={'radius':rt,'angle':at,'cartesian':tuple_tex((x,y))}
 for coordinate,trig,result in [('x',c,x),('y',s,y)]:
  if 'styles' not in RECIPES[t]:continue
  style=RECIPES[t]['styles'][coordinate];slots[coordinate+'_sub']=fill(style['sub_mask'],slots)
  tt=tex(trig)
  if style['negative_numerator'] and trig<0 and tt.startswith('-'+r'\frac{'):tt=tt.replace('-'+r'\frac{',r'\frac{-',1)
  wrapped=style['always_wrapped'] or trig<0
  prefix=style['mul_prefix'] if style['always_wrapped'] else ('' if wrapped else r'\cdot ')
  slots[coordinate+'_mul']=rt+prefix+('('+tt+')' if wrapped else tt)
  slots[coordinate+'_final']=tex(result)
 return slots

def raw_bank(sid,r,x,y):
 env={'R':r,'X':x,'Y':y,'sqrt':sp.sqrt}
 return [tuple(sp.simplify(v) for v in sp.sympify(recipe,locals=env)) for recipe in RAW_BANKS[sid]]

def make(level,seed,t,p,profile):
 rec=RECIPES[t];raw=bool(profile and profile.startswith('raw-'));sid=rec['source_id']
 if raw and profile!='raw-'+sid:raise ValueError('Raw profile belongs to another template')
 r,a,d=exact_input(p)
 if p['unit']!=expected_unit(t):raise ValueError('Wrong angle unit for this template')
 guard(level,t,r,d,raw)
 theta=sp.Rational(d,180)*sp.pi;c=sp.cos(theta);s=sp.sin(theta);x=sp.simplify(r*c);y=sp.simplify(r*s)
 slots=solution_slots(t,r,a,p['unit'],c,s,x,y)
 problem=fill(rec['prompt_mask'],slots)
 solution=fill(rec['solution_mask'],slots) if 'solution_mask' in rec else fill(rec['normal_solution_mask'],slots) if not raw and 'normal_solution_mask' in rec else None
 if not raw and solution is not None:solution=solution.replace('Then, we calculate the $x$-coordinate','Then, we calculate the $y$-coordinate')
 is_radio=rec['fields'][0]['type'].endswith('/radio')
 if is_radio:
  if raw:values=raw_bank(sid,r,x,y)
  else:
   if level!='easy' and t in SUPPORTED_BANKS and profile!='method-sign-scale':
    if t=='radian_mixed_radio' and d!=315:raise ValueError('Source sign-root bank requires 315 degrees')
    if t=='radian_repeated_radio' and d!=240:raise ValueError('Source sign-half bank requires 240 degrees')
    values=raw_bank(sid,r,x,y)
   elif level=='easy':values=[(x,y),(-x,y),(x,-y),(-x,-y),(y,x)] if x!=y and x!=-y else [(x,y),(-x,y),(x,-y),(-x,-y),(2*x,2*y)]
   else:values=[(x,y),(-x,y),(x,-y),(-x,-y),(c,s)]
  if len({tuple(map(str,v)) for v in values})!=len(values):raise ValueError('Whole bank rejected: equivalent options')
  if sum(v==(x,y) for v in values)!=1:raise ValueError('Whole bank rejected: missing/ambiguous correct option')
  # Preserve original per-option comma spacing as an independent component mask.
  spaces={'q-17133':(0,3),'q-8522':(0,3)}
  displayed=[tuple_tex(v,raw and i in spaces.get(sid,())) for i,v in enumerate(values)]
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
 task=digest(['description-to-cartesian',tex(r),str(d)])
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{
 'version':VERSION,'source':SOURCE,'source_ids':[sid],'solution_origin':rec.get('normal_solution_origin','observed worked-solution mask') if not raw else 'observed attribute presence','template':t,'level':level,'seed':seed,'parameters':{k:str(v) for k,v in p.items()},
 'profile':profile or (SUPPORTED_BANKS.get(t,'method-sign-scale') if is_radio and level!='easy' else 'method-sign-scale' if is_radio else 'coordinate-blanks'),'raw_evidence':raw,
 'eligible_for_learning':not raw,'evidence_only':raw,'origin':('observed prompt with authored solution/ref completion and method bank' if t.startswith('legacy') else 'observed component masks and defensible source bank; authored level bounds' if is_radio and level!='easy' and t in SUPPORTED_BANKS and profile!='method-sign-scale' else 'observed component masks; authored level bounds and method bank') if not raw else 'observed raw component-pattern replay',
 'mathematical_fingerprint':task,'content_fingerprint':content,'bank_recipes':RAW_BANKS.get(sid) if is_radio and (raw or level!='easy' and t in SUPPORTED_BANKS and profile!='method-sign-scale') else ['correct','reverse_x_sign','reverse_y_sign','reverse_both_signs','swap_trigonometric_values' if x!=y and x!=-y else 'double_radius'] if is_radio and level=='easy' else BANK_NAMES if is_radio else [],
 'domain':'source angle fixed; positive exact radius <=24; whole evidence-bank constraints' if raw else 'familiar exact angle in [0,360); unit easy radius, finite nonunit rational moderate catalog, matching familiar radical hard radius; level-specific guards',
 'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plot_rating':'none'}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in FAMILIES:raise ValueError('Unknown difficulty')
 rng=random.Random(seed)
 if profile and profile.startswith('raw-'):
  candidates=[t for t,v in RECIPES.items() if v['source_id']==profile[4:]]
 else:candidates=list(FAMILIES[level])
 if profile in SUPPORTED_BANKS.values() and level=='easy':raise ValueError('Source normal banks require nonunit radius')
 if profile in SUPPORTED_BANKS.values():candidates=[t for t in candidates if SUPPORTED_BANKS.get(t)==profile]
 if profile=='method-sign-scale':candidates=[t for t in candidates if RECIPES[t]['fields'][0]['type'].endswith('/radio') and not t.startswith('axis')]
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
 if profile not in (None,'method-sign-scale','coordinate-blanks',*SUPPORTED_BANKS.values()) and not profile.startswith('raw-'):raise ValueError('Unknown bank profile')
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

# Easy: authored missing level. Unit radius isolates exact trigonometric lookup.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: observed direct conversion. Nonunit rational radius scales both values.
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
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--parameters',help='Exact parameter JSON; required for raw evidence profiles');a=ap.parse_args()
 levels=FAMILIES if a.difficulty=='all' else [a.difficulty]
 records=[generate(l,a.seed+i,a.template,parameters=json.loads(a.parameters) if a.parameters else None,profile=a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
