#!/usr/bin/env python3
"""Draft first-quadrant coordinate practice; registered numeric baseline is untouched.

Seven complete parameterized historical banks are PUBLIC evidence profiles,
including absent grades/solutions/keys. Opaque offset recipes are not promoted to
learning. Defaults use separately authored whole method banks and the observed
seven-row solution. No angles, trigonometric ratios, other quadrants or DB writes.
Missing-level workload policies are authored, not recovered MA classifications.
"""
from __future__ import annotations
import argparse, functools, hashlib, json, math, random, re, sys, uuid
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.question_capture import math_format as MF
HERE = Path(__file__).with_suffix('')
KP_ID = 17592186110754
KP_UUID = '87c18ea8-af12-52bd-8420-ec24ed63de65'
TITLE = 'Using the Pythagorean Theorem on the Unit Circle'
VERSION = 'first-quadrant-coordinate-draft-2'
SOURCE_PARAMETERS = {
 'q-23274':dict(n=49,d=8,known='y'), 'q-65027':dict(n=9,d=5,known='x'),
 'q-124608':dict(n=2,d=3,known='y'), 'q-124611':dict(n=5,d=3,known='y'),
 'q-124613':dict(n=5,d=4,known='x'), 'q-23216':dict(n=1,d=4,known='x'),
 'q-65031':dict(n=4,d=5,known='x')}
EQUATIONS = {'q-23274','q-65027','q-65031'}
UNRATED = {'q-23274','q-65027'}
RAW_PROFILES = tuple('raw:'+x for x in SOURCE_PARAMETERS)
METHOD_PROFILES = ('method-equation','method-value')

def digest(x):
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def tex(x):
 return sp.latex(sp.simplify(x)).replace('- ', '-')

def split_square(n):
 """Canonical c²r decomposition, r squarefree, exact integer arithmetic."""
 c = math.prod(p**(e//2) for p,e in sp.factorint(n).items())
 return c,n//(c*c)

def basic(p):
 if set(p) != {'n','d','known'} or type(p['n']) is not int or type(p['d']) is not int:
  raise ValueError('Exactly integer n,d and known=x|y are required')
 n,d = p['n'],p['d']
 if p['known'] not in ('x','y') or not 3<=d<=15 or not 0<n<d*d:
  raise ValueError('First-quadrant bounded coordinate required')
 return n,sp.Integer(d),d*d-n

def normal_domain(level,p):
 n,d,m = basic(p); d=int(d)
 c,r=split_square(n); b,s=split_square(m)
 # Keep the evaluated square's denominator d², as at every observed anchor;
 # cancellation through r must not introduce a non-square denominator and
 # an unadvertised denominator-rationalization workload.
 if math.gcd(n,d)!=1:return False
 # EASY: observed rational/unit-coefficient radical coordinate; no nontrivial
 # irrational-root extraction. All five labeled Easy sources satisfy this.
 if level=='easy':return d<=8 and (r==1 or c==1) and (b==1 or s==1)
 # MODERATE (authored): canonical/tutorial rational input, nontrivial radical
 # reduction at the existing final row; no extra solution stage or new method.
 if level=='moderate':return r==1 and b>1 and s>1
 # HARD (authored): square a nonunit radical coefficient AND its radicand,
 # then the same subtraction/root/positivity method. Radical notation alone
 # cannot meet this bound. Familiar squarefree r<=15, coefficient c<=4.
 if level=='hard':return r>1 and 2<=c<=4 and r<=15 and s>1
 raise ValueError('Difficulty must be easy, moderate or hard')

def historical_values(name,p):
 """Complete observed expression patterns. Offset intent is underdetermined.

 These are evidence-only parameterized patterns, not inferred learner errors.
 In particular m±1, m±2 and m+2d preserve scalar evidence without claiming
 the source author's operation. No literal source values are returned.
 """
 n,d,m=basic(p); a=sp.sqrt(m)/d
 recipes={
 'q-23274':lambda:[a,sp.sqrt(d-1)/d,-sp.sqrt(m+2*d)/d,-a,sp.sqrt(m+2*d)/d],
 'q-65027':lambda:[sp.sqrt(m+2*sp.sqrt(n))/d,sp.sqrt(m)/d**2,m/d,m/d**2,a],
 'q-124608':lambda:[-sp.sqrt(d*d+n)/d**2,a,sp.sqrt(m-n)/d,-sp.sqrt(m-1)/d**2,sp.sqrt(d*d+n)/d],
 'q-124611':lambda:[sp.sqrt(m-1)/d,sp.sqrt(m)/d**2,a,sp.sqrt(m-1)/d**2,sp.sqrt(n+1)/d],
 'q-124613':lambda:[sp.sqrt(m-2)/d,-sp.sqrt(n-2)/d,-sp.sqrt(m+2)/d,a,sp.sqrt(m)/d**2],
 'q-23216':lambda:[sp.sqrt(n+1)/(d-1),m/(2*d*d),(d-sp.sqrt(n))/d,a,d/(d+sp.sqrt(n))],
 'q-65031':lambda:[sp.sqrt(m)/d**2,m/d**2,a,sp.sqrt(n-1)/d,m/d]}
 return [sp.simplify(x) for x in recipes[name]()],sp.simplify(a)

def method_values(p):
 """One entire bank, selected before parameters: positive root, negative root,
 missing final root, omitted coordinate square, addition instead of subtraction.
 Every wrong expression comes from the displayed Pythagorean method.
 """
 n,d,m=basic(p); g=sp.sqrt(n)/d; a=sp.sqrt(m)/d
 return [a,-a,1-g*g,sp.sqrt(1-g),sp.sqrt(1+g*g)],a

def equivalent(a,b):
 """Exact radical equality via signs and squared values, avoiding expensive
 generic simplification of nested square-root differences."""
 if a==b:return True
 if a.is_negative is not None and b.is_negative is not None and a.is_negative!=b.is_negative:return False
 squared=sp.expand(a*a-b*b)
 if squared.is_zero is not None:return bool(squared.is_zero)
 return sp.simplify(a-b)==0

def check_bank(bank,answer):
 if len(bank)!=5 or any(x.is_real is not True or x.is_finite is not True for x in bank):
  raise ValueError('Whole bank rejected: nonreal/nonfinite or incomplete')
 if any(equivalent(a,b) for i,a in enumerate(bank) for b in bank[i+1:]):
  raise ValueError('Whole bank rejected: equivalent options')
 if sum(equivalent(x,answer) for x in bank)!=1:
  raise ValueError('Whole bank rejected: key multiplicity')

def template_for(profile):
 if profile.startswith('raw:'):
  return 'coordinate-equation' if profile[4:] in EQUATIONS else 'coordinate-value'
 return 'coordinate-equation' if profile=='method-equation' else 'coordinate-value'

def prompt(p,raw=False,name=None):
 given=tex(sp.sqrt(p['n'])/p['d']); k=p['known']; t='y' if k=='x' else 'x'
 if raw and name in UNRATED:
  suffix=f'${given}$. What is the ${t}$-coordinate of $A$?'
 else:
  suffix=f'${given}.$ What is the ${t}$-coordinate of $A?$'
 return f'The point $A$ is located in the first quadrant and lies on the unit circle. The ${k}$-coordinate of $A$ is '+suffix

def solution(p,comma=False):
 n,d,m=basic(p); k=p['known']; t='y' if k=='x' else 'x'
 g,s,v,a=map(tex,(sp.sqrt(n)/d,n/d**2,m/d**2,sp.sqrt(m)/d))
 sub=f'{{({g})}}^{{2}}'
 r2=f'{sub}+{{y}}^{{2}}' if k=='x' else f'{{x}}^{{2}}+{sub}'
 r3=f'{s}+{{y}}^{{2}}' if k=='x' else f'{{x}}^{{2}}+({s})'
 # The source's concrete seven rows stay distinct (including before root
 # extraction) even when two adjacent rows have equal simplified values.
 rows=[r'{x}^{2}+{y}^{2} & =1',r2+' & =1',r3+' & =1',
       f'{{{t}}}^{{2}} & =1-{s}',f'{{{t}}}^{{2}} & ={v}',
       f'{t} & ='+r'\sqrt{'+v+'}',f'{t} & ='+r'\pm '+a+'.']
 return ('Since the point $A$ lies on the unit circle, it must satisfy the Pythagorean theorem: \n\n$$\n{x}^{2}+{y}^{2}=1\n$$\n\n'
  f'Substituting ${k}={g}$ into the above and solving for ${t}$ gives'+(',' if comma else '')+'\n\n$$\n'
  +r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$\n\n'
  f'Since $A$ lies in the first quadrant, ${t}$ must be positive, so we select the positive answer. '
  f'Therefore, our final answer is ${t}={a}.$')

def candidate_parameters(level):
 for d in range(3,16):
  for n in range(1,d*d):
   for k in ('x','y'):
    p=dict(n=n,d=d,known=k)
    if normal_domain(level,p):yield p

@functools.lru_cache(None)
def pool(level):
 return tuple(candidate_parameters(level))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only source radio supported')
 if template not in (None,'coordinate-equation','coordinate-value'):raise ValueError('Unknown template')
 rng=random.Random(seed)
 eligible=[x for x in METHOD_PROFILES if template in (None,template_for(x))]
 if profile is None:profile=rng.choice(eligible) # whole eligible bank BEFORE p
 if profile not in METHOD_PROFILES+RAW_PROFILES:raise ValueError('Unknown complete profile')
 if template is not None and template!=template_for(profile):raise ValueError('Template/profile mismatch')
 raw=profile.startswith('raw:'); name=profile[4:] if raw else None
 if raw and level!='easy':raise ValueError('Observed historical profiles have only Easy or omitted grade')
 if parameters is None:
  if raw:parameters=dict(SOURCE_PARAMETERS[name])
  else:parameters=dict(rng.choice(pool(level)))
 p=dict(parameters); basic(p)
 if raw and (math.isqrt(p['n'])**2==p['n'])!=(name in {'q-23274','q-65027','q-23216','q-65031'}):
  raise ValueError('Historical profile must preserve its rational/radical input class')
 if not raw and not normal_domain(level,p):raise ValueError('Authored workload/domain violation')
 bank,correct=historical_values(name,p) if raw else method_values(p)
 check_bank(bank,correct)
 t='y' if p['known']=='x' else 'x'; values=[]
 for x in bank:
  value=tex(x)
  if template_for(profile)=='coordinate-equation':
   if raw and name in ('q-23274','q-65027'):
    value=t+(' ='+value if value.startswith('-') else ' = '+value)
   else:value=t+'='+value
  values.append(value if raw else MF.normalize_tex(value))
 text=prompt(p,raw,name); worked=None if name in UNRATED else solution(p,name=='q-23216')
 if not raw:text=MF.normalize_prose(text);worked=MF.normalize_prose(worked)
 # Conservative task equivalence: x/y swapping and reversing the two positive
 # coordinates are not used to inflate arithmetic capacity. Target coverage
 # is checked separately. Banks, notation, difficulty and seed are excluded.
 qsquare=sp.Rational(p['n'],p['d']**2)
 task=digest([sorted((str(qsquare),str(1-qsquare))),'positive-unit-circle-coordinate'])
 actual_level=None if name in UNRATED else ':question.difficulty/'+level
 identity=digest([VERSION,text,worked,actual_level,template_for(profile),sorted(values),not (name in UNRATED)])
 qid=str(uuid.uuid5(uuid.UUID(KP_UUID),identity));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 key=next(i for i,x in enumerate(bank) if equivalent(x,correct))
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if name not in UNRATED:field[':answer-field/correct']=[':answer/id',answers[key][':answer/id']]
 rng.shuffle(answers)
 q={':question/id':qid,':question/problem':text,':question/answer-fields':[field]}
 if worked is not None:q[':question/worked-solution']=worked
 if actual_level is not None:q[':question/difficulty']=actual_level
 r={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
    'generation':{'version':VERSION,'seed':seed,'template':template_for(profile),'profile':profile,'parameters':p,
     'source':{'database':'math','basis':2275,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},
     'source_ids':[name] if raw else [],'raw_replay':raw,'evidence_only':raw,'eligible_for_learning':not raw,
     'authored_level':None if raw else level,'mathematical_fingerprint':task,'content_identity':identity,
     'domain':'first quadrant; x²+y²=1; 0<known<1; denominator<=15',
     'bank_interpretation':'observed expression pattern; intention underdetermined' if raw else 'authored method operation bank',
     'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}
 if not raw:MF.validate_generated_record(r)
 return r

def generate_easy(seed=0,**kwargs):
 """Easy observed arithmetic and unit-coefficient radical workload."""
 return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):
 """Authored canonical rational-coordinate / root-extraction workload."""
 return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):
 """Authored nonunit radical-coordinate squaring workload; same backbone."""
 return generate('hard',seed,**kwargs)

def markdown(record):
 q=record['question'];s=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):
  s+='\n'.join('- $'+a[':answer/value']+'$' for a in f.get(':answer-field/choices',[]))
 return s+'\n\n'+q.get(':question/worked-solution','[Original worked solution absent.]')

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all')
 ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2)
 ap.add_argument('--format',choices=('markdown','json'),default='json')
 ap.add_argument('--template');ap.add_argument('--profile')
 args=ap.parse_args()
 if args.count<=0:ap.error('count must be positive')
 levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
