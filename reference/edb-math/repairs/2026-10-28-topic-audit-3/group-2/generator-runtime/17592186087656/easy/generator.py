#!/usr/bin/env python3
"""Seeded standard-form circle center/radius questions; source replay and easy sampling."""
import argparse,sys, hashlib, itertools, json, random, uuid
import sympy as s
from math_format import normalize_prose, checked_math_content, validate_prose

KP_ID=17592186087656
KP_UUID='89462485-2e28-5727-82c7-7afd0cac6d77'
TITLE='Finding the Center and Radius of a Circle Given Its Equation'
VERSION='circle-extraction-2'
SOURCE={'database':'math','basis':4712,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
SF=(2,3,5,6,7,10,11,13)
INT=tuple(range(-10,11))
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
 'sampled-grid':(),
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
 rad=1/S if recipe.endswith('reciprocal') else S**2 if recipe.endswith('rhs_squared') else S if recipe.endswith('rhs') else r
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
 return ('The general equation of a circle with radius $r$ centered at the point $(a,b)$ is \n\n$$\n'
  '(x-a)^{2}+(y-b)^{2}={r}^{2}.\n$$\n\n'
  "Let's compare the general equation to our equation side-by-side as follows:\n\n$$\n"
  '\\begin{aligned}(x-a)^{2}+(y-b)^{2} & ={r}^{2} \\\\ '+lhs(a,b)+' & ='+tex(S)+' \\\\ '
  +lhs(a,b,True)+' & ='+square+'.\\end{aligned}\n$$\n\n'
  +f'We see that $a={tex(a)},$ $b={tex(b)},$ and $r={rt}.$ \n\n'
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
 else:raise ValueError('Unknown difficulty')
 if profile=='q-117087' and (b!=0 or a==0):raise ValueError('Axis source profile requires b=0 and a nonzero')
 if a==b==0:raise ValueError('Origin-centered equations excluded from this shifted-form sampler')

def sample(level,rng,profile):
 if level!='easy':raise ValueError('Unsupported difficulty')
 sign_case=rng.choice(('++','+-','-+','--','x0','y0'))
 radius_case=rng.choice(('square','nonsquare'))
 a,b=rng.randint(1,10),rng.randint(1,10)
 if sign_case=='x0':a=0;b*=rng.choice((-1,1))
 elif sign_case=='y0':b=0;a*=rng.choice((-1,1))
 else:a*=1 if sign_case[0]=='+' else -1;b*=1 if sign_case[1]=='+' else -1
 if profile=='q-117087':a=rng.choice(tuple(v for v in INT if v));b=0
 return {'a':a,'b':b,'S':rng.choice(SF) if radius_case=='nonsquare' else rng.randint(2,10)**2}
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,v))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level != 'easy':raise ValueError('Unsupported difficulty: only source-backed easy is supported')
 if field_type not in (None,'radio'):raise ValueError('Only source radio layout supported')
 expected='standard_circle_radio'
 if template not in (None,expected):raise ValueError('Unknown template')
 if profile is not None and profile not in BANKS:raise ValueError('Unknown profile')
 if profile and profile.startswith('q-') and level!='easy':raise ValueError('Observed profiles are easy evidence')
 rng=random.Random(seed)
 if profile is None:profile='sampled-grid'
 if profile.startswith('q-'):
  original=ORIGINAL_PARAMETERS[profile.removesuffix('_completed')]
  if parameters is not None and canonical_parameters(parameters)!=canonical_parameters(original):raise ValueError('Source bank profiles are replay-only')
  parameters=original
 # Choose decision roles before incidental magnitudes, including wrong-radius relation.
 radius_error=rng.choice(('rhs','reciprocal'))
 for attempt in range(100):
  p=canonical_parameters(parameters) if parameters is not None else canonical_parameters(sample(level,rng,profile))
  bank=profile
  try:
   guard(level,p,bank)
   correct_text,correct_math=value('correct',p,bank)
   recipes=list(BANKS[bank])
   if bank=='sampled-grid':
    # Select compatible answer-bearing roles, without frequency invariants.
    candidates={}
    for center in ('correct','both','x','y','origin'):
     for radius in ('root',radius_error):
      recipe=center+'_'+radius
      signature=value(recipe,p,bank)[1]
      if signature!=correct_math:candidates.setdefault(signature,recipe)
    banks=[list(bank) for bank in itertools.combinations(candidates.values(),4)
           if any(value(rec,p,profile)[1][2]!=correct_math[2] for rec in bank)]
    recipes=['correct']+rng.choice(banks)
   values=[value(rec,p,bank) for rec in recipes]
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
 sol=None if raw else normalize_prose(worked(p,bank,level))
 prompt=normalize_prose(prompt.replace('?$','$?'))
 values=[(normalize_prose(v),math) for v,math in values]
 correct_text=normalize_prose(correct_text)
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
 record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{
  'version':VERSION,'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'seed':seed,'template':expected,'parameters':serialized,
  'parameter_fingerprint':fp,'content_fingerprint':content,'bank_profile':bank,'bank_origin':'inferred completion' if bank.endswith('_completed') else 'observed' if bank.startswith('q-') else 'authored',
  'recipes':recipes,'attempts':attempt+1,'authored_difficulty':level if level!='easy' or raw or bank.endswith('_completed') else None,
  'source':SOURCE,'source_ids':[bank.removesuffix('_completed')] if bank.startswith('q-') else list(ORIGINAL_PARAMETERS),
  'domain':'Real x,y; S>0; standard form; no expanded squares','plot_rating':'none','plot_assets':{},
  'evidence_only':raw,'eligible_for_learning':not raw,'source_omissions':['difficulty','worked-solution','correct'] if raw else [],
  'authored_extension':not bank.startswith('q-') or level!='easy' or bank.endswith('_completed')}}

 if raw:
  validate_prose(prompt)
  for answer in answers:validate_prose(answer[':answer/value'])
  return record
 return checked_math_content(lambda: record)()

# EASY: observed standard form, integer shifts, integer or square-free roots.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
def markdown(r):
 q,g=r['question'],r['generation'];f=q[':question/answer-fields'][0]
 lines=[f"## Generated {q.get(':question/difficulty','unrated').split('/')[-1]} — {g['bank_profile']}",q[':question/problem'],'']
 for a in f[':answer-field/choices']:lines.append('- '+a[':answer/value']+(' **correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else ''))
 lines+=['',q.get(':question/worked-solution','Source omitted its worked solution and correct designation; evidence only.')]
 return '\n'.join(lines)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard'],default='easy');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=['markdown','json'],default='markdown');a=ap.parse_args()
 if a.count<1:ap.error('count must be positive')
 rs=[generate(level,a.seed+i,a.template,profile=a.profile) for level in [a.difficulty] for i in range(a.count)]
 print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
if __name__=='__main__':main()
