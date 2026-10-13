#!/usr/bin/env python3
"""Circle center/radius extraction; frozen v1, math basis 1356.
Only standard-form equations: no constructing circles, distance, midpoint,
completion of squares, intercepts, or coordinate transforms. All recipes build
complete five-option banks; explicit invalid parameters fail, never resample.
See private evidence for source layout/provenance, missing-level design and QA.
"""
import argparse,sys, hashlib, json, random, uuid
from pathlib import Path
import sympy as s

KP_ID=17592186087656
KP_UUID='89462485-2e28-5727-82c7-7afd0cac6d77'
TITLE='Finding the Center and Radius of a Circle Given Its Equation'
VERSION='circle-extraction-frozen-1'
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
X,Y=s.symbols('x y', real=True)
SF=(2,3,5,6,7,10,11,13)
RED=(8,12,18,20,24,27,28,32,45,48,50,63,72,75,80,98)
INT=tuple(range(-10,11))
RAT=tuple(sorted({s.Rational(n,d) for d in (2,3) for n in range(-9,10) if n and n%d}))
# Complete operation banks. Recipes are sign extraction, forgetting the square
# root, dropping offsets, and squaring the equation's RHS a second time.
BANKS={
 'q-7521':('correct_rhs','both_rhs','origin_root','both_root','correct'),
 'q-7527':('correct','correct_rhs','both_root','both_rhs','correct_rhs_squared'),
 'q-117087':('both_rhs','origin_root','both_root','correct_rhs','correct'),
 'q-70900':('y_root','x_root','both_root','correct_rhs','correct'),
 'q-70935':('correct_rhs','both_rhs','both_root','correct','y_rhs'),
 'q-70933':('correct','correct_rhs','both_root','x_root','both_rhs'),
 'q-117084':('both_rhs','correct','both_root','correct_rhs','y_root'),
 'q-117086':('both_rhs','origin_root','correct','both_root','correct_rhs'),
 'authored':('correct','both_root','x_root','y_root','correct_rhs'),
 'authored_axis':('correct','both_root','correct_rhs','both_rhs','origin_root'),
}
BANKS['q-7527_completed']=BANKS['q-7527']
ORIGINAL_PARAMETERS={
 'q-7521':{'a':2,'b':3,'S':6},'q-7527':{'a':-5,'b':-1,'S':4},
 'q-117087':{'a':5,'b':0,'S':3},'q-70900':{'a':2,'b':-2,'S':9},
 'q-70935':{'a':-3,'b':-3,'S':5},'q-70933':{'a':-1,'b':-6,'S':16},
 'q-117084':{'a':-5,'b':3,'S':81},'q-117086':{'a':7,'b':10,'S':100}}

def tex(v):return s.latex(s.sympify(v))
def term(v,c,explicit=False,space=False):
 if not c and not explicit:return '{'+v+'}^{2}'
 op='-' if c>=0 or explicit else '+'
 mag=('('+tex(c)+')' if c<0 else tex(c)) if explicit else tex(abs(c))
 sep=' ' if space else ''
 return '('+v+sep+op+sep+mag+')^{2}'
def lhs(a,b,explicit=False,space=False):return term('x',a,explicit,space)+(' + ' if space else '+')+term('y',b,explicit,space)
def equation(p,explicit=False,space=False):return lhs(p['a'],p['b'],explicit,space)+(' = ' if space else '=')+tex(p['S'])

def value(recipe,p,profile):
 if profile=='q-7527_completed':profile='q-7527'
 a,b,S=p['a'],p['b'],p['S'];r=s.sqrt(S)
 if recipe.startswith('both'):a,b=-a,-b
 elif recipe.startswith('x_'):a=-a
 elif recipe.startswith('y_'):b=-b
 elif recipe.startswith('origin'):a,b=0,0
 rad=S**2 if recipe.endswith('rhs_squared') else S if recipe.endswith('rhs') else r
 # q-7527 preserves its redundant square and the source's positive-center space.
 rt=tex(S)+'^{2}' if recipe.endswith('rhs_squared') else tex(rad)
 comma=', ' if profile=='q-7527' and recipe.startswith('both') else ','
 article='the ' if profile in ('q-117087','q-117084','q-117086') else ''
 return f'The center is $({tex(a)}{comma}{tex(b)})$ and {article}radius is ${rt}$',(a,b,rad)

def worked(p,profile,level="easy"):
 a,b,S=p['a'],p['b'],p['S'];r=s.sqrt(S);rt=tex(r)
 if r.is_Integer: square='{'+rt+'}^{2}'
 elif profile=='q-117087':square='{('+rt+')}^{2}'
 else:square='('+rt+')^{2}'
 reduction=''
 if level=='hard':
  c=s.Integer(r.as_coeff_Mul()[0]);d=s.Integer(S/c**2)
  reduction='The radius is the positive square root of the right-hand side:\n\n$$\nr=\\sqrt{'+tex(S)+'}=\\sqrt{'+tex(c*c)+r'\cdot '+tex(d)+'}='+rt+'.\n$$\n\n'
 return ('The general equation of a circle with radius $r$ centered at the point $(a,b)$ is \n\n$$\n'
  '(x-a)^{2}+(y-b)^{2}={r}^{2}.\n$$\n\n'
  "Let's compare the general equation to our equation side-by-side as follows:\n\n$$\n"
  '\\begin{aligned}(x-a)^{2}+(y-b)^{2} & ={r}^{2} \\\\ '+lhs(a,b)+' & ='+tex(S)+' \\\\ '
  +lhs(a,b,True)+' & ='+square+'.\\end{aligned}\n$$\n\n'
  +reduction+f'We see that $a={tex(a)},$ $b={tex(b)},$ and $r={rt}.$ \n\n'
  +f'Therefore, the circle is centered at $({tex(a)},{tex(b)})$ and its radius is ${rt}.$')

def canonical_parameters(p):
 if set(p)!= {'a','b','S'}:raise ValueError('Exactly a, b, S required')
 return {k:s.Rational(str(v)) for k,v in p.items()}
def guard(level,p,profile):
 a,b,S=(p[k] for k in ('a','b','S'))
 if profile.startswith('q-'):
  # Original profiles retain easy arithmetic forms, including signed/zero shifts.
  if level!='easy' or a not in INT or b not in INT or S not in (*SF,*(i*i for i in range(2,11))):raise ValueError('Observed easy domain violated')
 elif level=='easy':
  if a not in INT or b not in INT or S not in (*SF,*(i*i for i in range(2,11))):raise ValueError('Easy domain violated')
 elif level=='moderate':
  if not ((a in RAT and b in INT and b!=0) or (b in RAT and a in INT and a!=0)) or S not in SF:raise ValueError('Moderate: exactly one rational shift; square-free RHS')
 elif level=='hard':
  if a not in RAT or b not in RAT or S not in RED:raise ValueError('Hard: two rational shifts; reducible nonsquare RHS')
 else:raise ValueError('Unknown difficulty')
 if profile=='authored_axis' and (level!='easy' or bool(a)==bool(b)):raise ValueError('Authored axis bank requires one zero offset at easy')
 if profile=='q-117087' and (b!=0 or a==0):raise ValueError('Axis source profile requires b=0 and a nonzero')
 if a==b==0:raise ValueError('Centered-at-origin tasks belong to prerequisite topic')

def sample(level,rng,profile):
 if level=='easy':
  nonzero=tuple(v for v in INT if v)
  if profile=='q-117087':a,b=rng.choice(nonzero),0
  elif profile=='authored_axis':
   a,b=rng.choice(nonzero),0
   if rng.randrange(2):a,b=b,a
  elif profile=='authored':a,b=rng.choice(nonzero),rng.choice(nonzero)
  else:a,b=rng.choice(INT),rng.choice(INT)
  return {'a':a,'b':b,'S':rng.choice((*SF,*(i*i for i in range(2,11))))}
 if level=='moderate':
  a,b=rng.choice(RAT),rng.choice(tuple(v for v in INT if v));
  if rng.randrange(2):a,b=b,a
  return {'a':a,'b':b,'S':rng.choice(SF)}
 return {'a':rng.choice(RAT),'b':rng.choice(RAT),'S':rng.choice(RED)}
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,v))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unsupported level')
 if field_type not in (None,'radio'):raise ValueError('Only source radio layout supported')
 expected='standard_circle_radio'
 if template not in (None,expected):raise ValueError('Unknown template')
 if profile is not None and profile not in BANKS:raise ValueError('Unknown profile')
 if profile and profile.startswith('q-') and level!='easy':raise ValueError('Observed profiles are easy evidence')
 rng=random.Random(seed)
 if profile is None:
  if parameters is not None:
   explicit=canonical_parameters(parameters)
   profile='authored_axis' if not explicit['a'] or not explicit['b'] else 'authored'
  else:profile=rng.choice(('authored','authored_axis')) if level=='easy' else 'authored'
 for attempt in range(100):
  p=canonical_parameters(parameters) if parameters is not None else sample(level,rng,profile)
  bank=profile
  try:
   guard(level,p,bank)
   correct_text,correct_math=value('correct',p,bank)
   values=[value(rec,p,bank) for rec in BANKS[bank]]
   signatures=[tuple(map(s.simplify,item[1])) for item in values]
   if len(set(signatures))!=5:raise ValueError('Complete bank collision')
  except ValueError:
   if parameters is not None:raise
   continue
  break
 else:raise ValueError('No valid complete bank')
 raw=bank=='q-7527'
 article='the ' if bank in ('q-117087','q-117084','q-117086') else ''
 prompt=f'What is the center and {article}radius of the circle with equation $'+equation(p,space=bank in ('q-7527','q-7527_completed'))+('$?' if bank in ('q-7527','q-7527_completed') else '?$')
 sol=None if raw else worked(p,bank,level)
 serialized={k:str(v) for k,v in p.items()}
 fp=digest(serialized) # complete standard equation defines assessed extraction task
 content=digest({'version':VERSION,'difficulty':None if raw else level,'prompt':prompt,'solution':sol,'values':sorted(v[0] for v in values),'correct':None if raw else value('correct',p,bank)[0]})
 qid=uid(content);fid=uid(qid+':selection')
 answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/text',':answer/value':v} for v,_ in values]
 correct=next(a[':answer/id'] for a in answers if a[':answer/value']==correct_text)
 rng.shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
 if not raw:q.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':sol});field[':answer-field/correct']=[':answer/id',correct]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{
  'version':VERSION,'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'seed':seed,'template':expected,'parameters':serialized,
  'parameter_fingerprint':fp,'content_fingerprint':content,'bank_profile':bank,'bank_origin':'inferred completion' if bank.endswith('_completed') else 'observed' if bank.startswith('q-') else 'authored',
  'recipes':list(BANKS[bank]),'authored_difficulty':level if level!='easy' or raw or bank.endswith('_completed') else None,
  'source':SOURCE,'source_ids':[bank.removesuffix('_completed')] if bank.startswith('q-') else list(ORIGINAL_PARAMETERS),
  'domain':'Real x,y; S>0; standard form; no expanded squares','plot_rating':'none','plot_assets':{},
  'evidence_only':raw,'eligible_for_learning':not raw,'source_omissions':['difficulty','worked-solution','correct'] if raw else [],
  'authored_extension':not bank.startswith('q-') or level!='easy' or bank.endswith('_completed')}}

# EASY: observed standard form, integer shifts, integer or square-free roots.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE (authored): exactly one noninteger rational shift; no root reduction.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored): two noninteger rational shifts and one familiar root reduction.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q,g=r['question'],r['generation'];f=q[':question/answer-fields'][0]
 lines=[f"## Generated {q.get(':question/difficulty','unrated').split('/')[-1]} — {g['bank_profile']}",q[':question/problem'],'']
 for a in f[':answer-field/choices']:lines.append('- '+a[':answer/value']+(' **correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else ''))
 lines+=['',q.get(':question/worked-solution','Source omitted its worked solution and correct designation; evidence only.')]
 return '\n'.join(lines)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=['markdown','json'],default='markdown');a=ap.parse_args()
 if a.count<1:ap.error('count must be positive')
 rs=[generate(level,a.seed+i,a.template,profile=a.profile) for level in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
if __name__=='__main__':main()
