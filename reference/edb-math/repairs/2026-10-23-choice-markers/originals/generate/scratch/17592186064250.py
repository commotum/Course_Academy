#!/usr/bin/env python3
"""Source-bank faithful inverse-secant integral generator, bounded positive parameters."""
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
H=Path(__file__).with_suffix('');SOURCE=json.loads((H/'source.json').read_text());KP=17592186064250
KP_UUID=SOURCE['record'][':knowledge-point/id'];VERSION='1.0.0'
GENERATOR_ID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
DOMAIN=range(2,25)
# Each complete observed bank is retained, in source order. Triples are
# (amplitude, inverse-function, argument slope). Interpretations are deliberately
# limited to observed algebraic transformations, not inferred student psychology.
PROFILES={
'q-69476':('moderate','m-prefactor',8,lambda t:(t,t),lambda n,a,b:[(n/2,'sec',n),(1,'sec',n*n),(a/n,'sec',n),(1/n,'sec',n),(2/n,'sec',n/2)],2),
'q-69475':('moderate','m-prefactor',7,lambda t:(t,t),lambda n,a,b:[(a/n,'sec',n),(1/n,'sec',n),(1/n,'sec',n*n),(1/n**2,'sec',n),(1,'sec',n*n)],0),
'q-69477':('moderate','m-prefactor',3,lambda t:(t*t,t),lambda n,a,b:[(1,'sec',n),(a/n,'sec',n),(1/n,'sec',n),(1/n**2,'sec',a),(1,'sec',a)],1),
'q-73715':('moderate','m-prefactor',3,lambda t:(2*t,t),lambda n,a,b:[(1/n,'sec',n),(1/n**2,'sec',n),(a/n,'sec',n),(1/n,'sec',n*n),(1,'sec',n*n)],2),
'q-73716':('moderate','m-unit',4,lambda t:(t,sp.Integer(1)),lambda n,a,b:[(1/n,'sec',n),(1,'sec',n),(n,'sec',n),(1/n,'tan',n),(1,'tan',n)],0),
'q-73717':('hard','h-prefactor',2,lambda t:(t,t),lambda n,a,b:[(a*n,'sec',n),(1/(a*n),'sec',n),(a,'sec',n),(1,'sec',n),(1/a,'sec',n)],2),
'q-114051':('hard','h-root-unit',5,lambda t:(sp.sqrt(t),sp.Integer(1)),lambda n,a,b:[(1,'sec',n),(b,'sec',n),(b,'sec',b),(n,'sec',n),(1,'sec',b)],0),
'q-114052':('hard','h-root-unit',2,lambda t:(sp.sqrt(t),sp.Integer(1)),lambda n,a,b:[(n,'sec',1),(1,'sec',1/n),(1,'sec',n),(n,'sec',n),(b,'sec',n)],2),
'q-114053':('hard','h-root-unit',3,lambda t:(sp.sqrt(t),sp.Integer(1)),lambda n,a,b:[(1,'sec',1/n),(1,'sec',n),(1/n,'sec',1),(1,'sec',b),(n,'sec',1)],1),
'q-114054':('hard','h-root-unit',6,lambda t:(sp.sqrt(t),sp.Integer(1)),lambda n,a,b:[(1/n,'sec',1),(1,'sec',n),(b,'sec',n),(1,'sec',1/n),(n,'sec',1)],1),
'q-114055':('hard','h-root-prefactor',7,lambda t:(sp.sqrt(t),t),lambda n,a,b:[(1,'sec',n),(1,'sec',b),(b*n,'sec',1),(1/n,'sec',1),(a,'sec',n)],4),
'q-114056':('hard','h-root-prefactor',8,lambda t:(sp.sqrt(t),t),lambda n,a,b:[(b*n,'sec',1),(a,'sec',n),(1,'sec',n),(1/n,'sec',1),(b,'sec',1/n)],1),
'q-114057':('hard','h-square-calculate-prefactor',5,lambda t:(2*t,t),lambda n,a,b:[(1,'sec',a*n),(1,'sec',n),(1/a,'sec',n),(a,'sec',n),(a,'sec',1)],3),
'q-49519':('hard','h-denominator',4,lambda t:(t,1/t),lambda n,a,b:[(1/n,'sin',n),(1/n,'tan',n),(n,'sec',n),(2/n,'sec',n*n),(1/n,'sec',n)],4),
'q-49554':('hard','h-denominator',3,lambda t:(t,1/t),lambda n,a,b:[(1/n,'sec',1),(1/n,'sec',n*n),(1/n,'sin',n),(1/n,'sin',n*n),(1/n,'sec',n)],4),
'q-49555':('hard','h-denominator',6,lambda t:(t,1/t),lambda n,a,b:[(1/n,'sin',n),(1/n,'sec',n*n),(1,'sec',n),(1/n,'sec',n),(1,'sec',n*n)],3),
'q-73718':('hard','h-denominator',5,lambda t:(t,1/t),lambda n,a,b:[(n,'tan',n),(1/n,'sec',n),(1/n,'tan',n),(1,'sec',n),(n,'sec',n)],1),
}
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}

def triples(profile,t):
 level,template,base,params,bank,correct=PROFILES[profile];n,a=map(sp.sympify,params(sp.Integer(t)));b=n*n
 return [(sp.simplify(c),f,sp.simplify(k)) for c,f,k in bank(n,a,b)]

def mathematical_key(n,c):return f'inverse-secant-integral:{sp.sstr(sp.simplify(c))}:{sp.sstr(sp.simplify(n*n))}:x'

def parameters(profile,t):
 if isinstance(t,bool) or not isinstance(t,int) or t not in DOMAIN:raise ValueError('parameter t must be an integer in [2,24]')
 level,template,base,params,bank,correct=PROFILES[profile];n,a=map(sp.sympify,params(sp.Integer(t)));c=a/n if level=='moderate' else a
 return n,a,sp.simplify(c)

def eligible(profile,t):
 try:
  n,a,c=parameters(profile,t);vals=triples(profile,t)
  if len(set(vals))!=5:return False
  # Irrational-square-root profiles remain nonsquares, as observed.
  if profile.startswith('q-11405') and profile!='q-114057' and sp.sqrt(t).is_Integer:return False
  return vals[PROFILES[profile][-1]]==(c,'sec',n)
 except ValueError:return False

def value(v):
 c,f,k=v;arg='x' if k==1 else sp.latex(k)+'x'
 expr=r'\text{arc'+f+'}('+arg+')'
 if c!=1:expr=sp.latex(c)+r'\,'+expr
 return expr+'+C'

def render_source(profile,t):
 """Transform numeric tokens simultaneously; preserve the entire source prose/layout."""
 q=ORIGINALS[profile];base=PROFILES[profile][2];n,a,c=parameters(profile,t)
 oldn,olda,_=parameters(profile,base)
 if 'root' in PROFILES[profile][1] and profile!='q-114057':mapping={str(base):str(t)}
 else:
  # Each duplicate base number must imply the same new token. This is why
  # profiles impose observed equal/proportional/square relationships.
  pairs=[(oldn,n),(oldn**2,n**2),(olda,a)]
  if profile=='q-73717':pairs.append((oldn*olda,n*a))
  if profile=='q-114057':pairs.append((oldn*olda,n*a))
  if profile=='q-69477':pairs.append((oldn/olda,n/a))
  mapping={}
  for old,new in pairs:
   if old.is_Integer and old!=1:
    key=str(old);target=str(new)
    assert key not in mapping or mapping[key]==target,(profile,key,mapping.get(key),target)
    mapping[key]=target
 def replace(s):
  s=s.replace('^{2}','^SQUARETOKEN').replace('^2','^SQUARETOKEN')
  return re.sub(r'(?<![0-9])\d+(?![0-9])',lambda m:mapping.get(m[0],m[0]),s).replace('^SQUARETOKEN','^{2}')
 return replace(q[':question/problem']),replace(q[':question/worked-solution'])

def generate(difficulty,seed=0,*,profile=None,t=None):
 if difficulty not in ['moderate','hard']:raise ValueError('Unsupported difficulty: no easy source evidence')
 rng=random.Random(seed);profiles=[p for p,v in PROFILES.items() if v[0]==difficulty]
 if profile is None:profile=rng.choice(profiles)
 if profile not in profiles:raise ValueError('Profile/difficulty mismatch')
 if t is None:t=rng.choice([t for t in DOMAIN if eligible(profile,t)])
 if not eligible(profile,t):raise ValueError('Invalid/ambiguous parameter bank')
 n,a,c=parameters(profile,t);bank=triples(profile,t);key=mathematical_key(n,c)
 # Authored bank is part of identity, but does not create a distinct task.
 qid=str(uuid.uuid5(uuid.UUID(GENERATOR_ID),key+':'+profile));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),repr(v))),':answer/type':':answer.type/math',':answer/value':value(v)} for v in bank]
 problem,solution=render_source(profile,t)
 q={':question/id':qid,':question/problem':problem+'\n\n{{selection}}',':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[PROFILES[profile][-1]][':answer/id']]}]}
 return {'knowledge_point':{'id':KP_UUID,'title':SOURCE['record'][':knowledge-point/title']},'question':q,'generation':{'generator_id':GENERATOR_ID,'version':VERSION,'seed':seed,'template':PROFILES[profile][1],'profile':profile,'parameters':{'t':t,'slope':str(n),'numerator':str(a),'normalized_amplitude':str(c)},'mathematical_key':key,'domain':'real x, |slope*x|>1; principal real arcsec on each connected interval','source_question_ids':[ORIGINALS[profile][':db/id']],'source_basis':SOURCE['basis'],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plots':[],'answer_recipes':[[str(c),f,str(k)] for c,f,k in bank]}}

def batch(difficulty,count,seed):
 if difficulty not in ['moderate','hard']:raise ValueError('Unsupported difficulty')
 candidates=[(p,t) for p,v in PROFILES.items() if v[0]==difficulty for t in DOMAIN if eligible(p,t)]
 random.Random(seed).shuffle(candidates);rows=[];used=set()
 for p,t in candidates:
  r=generate(difficulty,seed,profile=p,t=t);key=r['generation']['mathematical_key']
  if key in used:continue
  used.add(key);rows.append(r)
  if len(rows)==count:return rows
 if count==0:return []
 raise ValueError(f'Finite capability {len(rows)} distinct {difficulty} tasks; requested {count}')

def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(f"- {a[':answer/value']}" for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',required=True);p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');args=p.parse_args()
 if args.count<0:p.error('count must be nonnegative')
 rows=batch(args.difficulty,args.count,args.seed);print(json.dumps(rows,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
