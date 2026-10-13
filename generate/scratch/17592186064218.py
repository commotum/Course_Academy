#!/usr/bin/env python3
"""Bounded inverse-sine substitution generator; full observed banks, exact source layouts.

One parameter per profile preserves observed coefficient relationships. Numeric
slots are transformed simultaneously; powers of x/u remain fixed. No plot assets.
The ambiguous arcsec-squared bank q-2506 is replay-only, never practice output.
"""
import argparse,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186064218
H=Path(__file__).with_suffix('');SOURCE=json.loads((H/'source.json').read_text())
KP_UUID=SOURCE['record'][':knowledge-point/id'];TITLE=SOURCE['record'][':knowledge-point/title']
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'));VERSION='inverse-sine-substitution-v1'
SUPPORTED_LEVELS=('easy','moderate')
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
# level, Markdown/value template, observed t, numeric slot recipes.
# Source bank values are structural templates, not a pool of inferred errors.
PROFILES={
 'q-2505':('easy','unit-square-equality',2,lambda t:{2:t,4:t*t}),
 'q-2506':('easy','unit-square-equality',3,lambda t:{3:t,9:t*t}),
 'q-49535':('easy','scaled-square-equality',4,lambda t:{2:t//2,4:t,16:t*t}),
 'q-114022':('easy','equal-numerator-calculate',5,lambda t:{5:t,25:t*t}),
 'q-114023':('easy','reciprocal-numerator-calculate',6,lambda t:{6:t,36:t*t}),
 'q-114025':('easy','reciprocal-numerator-calculate',9,lambda t:{9:t,81:t*t}),
 'q-114024':('easy','root-square-numerator-calculate',2,lambda t:{2:t,4:t*t}),
 'q-114027':('easy','root-fixed-numerator-calculate',3,lambda t:{3:t}),
 'q-114032':('easy','root-equal-numerator-calculate',3,lambda t:{3:t}),
 'q-2503':('moderate','unit-constant-equality',3,lambda t:{3:t,9:t*t}),
 'q-4334':('moderate','unit-constant-equality',6,lambda t:{2:t//3,3:t//2,6:t,36:t*t}),
 'q-49547':('moderate','fixed-numerator-equality',7,lambda t:{7:t,49:t*t}),
 'q-114030':('moderate','fixed-numerator-calculate',5,lambda t:{5:t,25:t*t}),
 'q-73712':('moderate','rational-numerator-equality',2,lambda t:{2:t,4:t*t,8:t**3}),
}
def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),s))
def mathematical_fingerprint(profile,t):
 t=sp.Integer(t);level=PROFILES[profile][0]
 if level=='moderate':
  amplitude={'q-2503':1,'q-4334':1,'q-49547':3,'q-114030':2,'q-73712':t**3/3}[profile];constant=t*t;square=1
 else:
  constant=1;square=t if profile in ('q-114024','q-114027','q-114032')else t*t
  amplitude={'q-2505':1,'q-2506':1,'q-49535':2,'q-114022':t,'q-114023':1/t,'q-114025':1/t,'q-114024':t*t,'q-114027':8,'q-114032':t}[profile]
 return digest(sp.sstr(sp.simplify(amplitude/sp.sqrt(constant)))+'|'+sp.sstr(sp.Rational(square,constant)))

def domain(profile):
 if profile=='q-49535':return (4,) # repeated numeric slots have incompatible roles; replay/completion only
 if profile=='q-4334':return (6,12,18,24)
 if profile=='q-73712':return (2,3,4)
 if profile=='q-49547':return tuple(t for t in range(2,13)if t!=9) # 3/t and 1/3 collide at t=9
 if profile in ('q-114024','q-114027','q-114032'):return (2,3,5,6,7,8,10,11,12)
 return tuple(range(2,13))
def candidates(profile):return [{'t':t}for t in domain(profile)]
def transform(s,mapping):
 # Exponents, including malformed source arcsec superscript, are not slots.
 protected=[]
 def hold(m):protected.append(m[0]);return '@POWER'+chr(65+len(protected)-1)+'@'
 s=re.sub(r'\^\{\d+\}|\^\d+',hold,s)
 s=re.sub(r'(?<!\d)\d+(?!\d)',lambda m:str(mapping.get(int(m[0]),int(m[0]))),s)
 for i,value in enumerate(protected):s=s.replace('@POWER'+chr(65+i)+'@',value)
 return s

def generate(difficulty,seed=0,template=None,parameters=None,*,profile=None,replay=False):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported hard: no validated harder template in this bounded package')
 profile=profile or template
 rng=random.Random(seed)
 available=[p for p,v in PROFILES.items()if v[0]==difficulty and p!='q-2506']
 profile=profile or rng.choice(available)
 if profile not in PROFILES or PROFILES[profile][0]!=difficulty:raise ValueError('Profile/level mismatch')
 if profile=='q-2506'and not replay:raise ValueError('Ambiguous arcsec-squared source profile is evidence-only')
 if parameters is None:parameters={'t':rng.choice(domain(profile))}
 if set(parameters)!={'t'}or isinstance(parameters['t'],bool)or not isinstance(parameters['t'],int)or parameters['t']not in domain(profile):raise ValueError('Outside bounded profile domain')
 t=parameters['t'];old=ORIGINALS[profile];mapping=PROFILES[profile][3](t)
 problem=transform(old[':question/problem'],mapping);solution=transform(old[':question/worked-solution'],mapping)
 if profile=='q-49535'and not replay:
  # Source first displayed integral loses its numerator. Preserve raw replay.
  solution=solution.replace(rf'\int \frac{{1}}{{\sqrt{{1-{t*t}',rf'\int \frac{{{t//2}}}{{\sqrt{{1-{t*t}',1)
 qid=uid(VERSION+'|'+profile+'|'+str(t)+'|'+str(replay));fid=uid(qid+'|selection')
 f=old[':question/answer-fields'][0];values=[transform(a[':answer/value'],mapping)for a in f[':answer-field/choices']]
 if len(set(values))!=5:raise ValueError('Colliding bank')
 answers=[{':answer/id':uid(fid+'|'+v),':answer/type':':answer.type/math',':answer/value':v}for v in values]
 correct=transform(f[':answer-field/correct'][':answer/value'],mapping)
 q={':question/id':qid,':question/problem':problem+(''if replay else '\n\n{{selection}}'),':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/type':':answer-field.type/radio',':answer-field/key':'selection',':answer-field/choices':answers,':answer-field/correct':[':answer/id',next(a[':answer/id']for a in answers if a[':answer/value']==correct)]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'seed':seed,'template':PROFILES[profile][1],'profile':profile,'parameters':{'t':t},'source_question_id':old[':db/id'],'source_math_academy_id':profile,'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'domain':'real x; radicand strictly positive, principal arcsin','sampling':'positive bounded source-related slots; nonsquare root profiles','evidence_only':replay,'eligible_for_learning':not replay,'replay':replay,'repairs':['opening-integral-numerator']if profile=='q-49535'and not replay else [],'mathematical_fingerprint':mathematical_fingerprint(profile,t),'numeric_slot_recipes':{str(k):v for k,v in mapping.items()},'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plots':[]}}
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(*args,**kwargs):raise ValueError('Unsupported hard; shortage remains explicit')
def batch(difficulty,count=5,seed=0):
 candidates_=[(p,t)for p,v in PROFILES.items()if v[0]==difficulty and p!='q-2506'for t in domain(p)]
 random.Random(seed).shuffle(candidates_);out=[];seen={mathematical_fingerprint(p,v[2])for p,v in PROFILES.items()}
 seen.add(digest('3/4|9')) # canonical example: 9/(4 sqrt(1-9x^2))
 for p,t in candidates_:
  # One t per selected profile here; final preparation does symbolic deduplication.
  key=mathematical_fingerprint(p,t)
  if key not in seen:out.append(generate(difficulty,seed,p,{'t':t}));seen.add(key)
  if len(out)==count:return out
 raise ValueError('Bounded output exhausted')
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' [correct]'if a[':answer/id']==f[':answer-field/correct'][1]else '')for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=5);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args()
 if a.count<1:p.error('positive count required')
 rows=[r for level in (SUPPORTED_LEVELS if a.difficulty=='all'else[a.difficulty])for r in batch(level,a.count,a.seed)]
 print(json.dumps(rows,indent=2,ensure_ascii=False)if a.format=='json'else '\n\n---\n\n'.join(map(markdown,rows)))
if __name__=='__main__':main()
