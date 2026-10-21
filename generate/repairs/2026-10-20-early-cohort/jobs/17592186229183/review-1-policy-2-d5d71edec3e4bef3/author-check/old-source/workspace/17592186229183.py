#!/usr/bin/env python3
"""Determining an amount at overflow onset; frozen math basis 1356.

Shared helpers + independently documented easy/moderate/hard entrypoints below.
Full positional source masks preserve all blocks, arithmetic rows and omissions.
Historical numerical banks are explicit opaque evidence profiles, never defaults.
Normal complete five-option banks use four defined mistakes in the actual method.
All concentrations are lb/gal, all flow rates gal/min, time minutes, answers lb.
No post-overflow model, plot, database client, writes, registration or commits.
"""
import argparse,hashlib,json,random,re,sys,uuid
from pathlib import Path
from decimal import Decimal,ROUND_HALF_UP,localcontext
import sympy as s
KP_ID=17592186229183
KP_UUID='c652164a-2e94-5e16-a410-5143037af134'
TITLE='Determining an Amount at an Overflow Point'
VERSION='overflow-onset-1'
D=Path(__file__).with_suffix('')
MASKS=json.loads((D/'masks.json').read_text())
SOURCE=json.loads((D/'source.json').read_text())
T=s.Symbol('t',nonnegative=True)
LEVELS=('easy','moderate','hard')

def stable(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+x))
def fmt(x):
 x=s.sympify(x)
 if x.is_Rational:
  for n in range(3):
   if (x*10**n).is_Integer:
    return str(int(x)) if n==0 else f'{float(x):.{n}f}'
 return s.latex(x)
def rounded(x):
 with localcontext() as c:
  c.prec=60
  return str(Decimal(str(s.N(x,55))).quantize(Decimal('.1'),rounding=ROUND_HALF_UP))

def data(p):
 H,v,q,c,rin,rout=(s.Rational(str(p[k])) for k in ('H','v','q','c','rin','rout'))
 d=rin-rout;a=v/d;n=rout/d;A=c*rin;k=A/(n+1);D0=c*v-q;to=(H-v)/d
 ratio=v/H;amount=c*H-D0*ratio**n
 sol=c*(v+d*T)-D0*(v/(v+d*T))**n
 rd=s.Rational(a/(a+to))
 return dict(H=H,v=v,q=q,c=c,rin=rin,rout=rout,d=d,a=a,n=n,nm=n-1,np=n+1,A=A,k=k,D=D0,cv=c*v,to=to,gap=H-v,end=a+to,cH=c*H,reduced_num=a/10,reduced_den=(a+to)/10,rounded=rounded(amount),amount=amount,Q=sol)

def guard(p,level,evidence=False):
 if set(p)!=set(('H','v','q','c','rin','rout')):raise ValueError('Exactly H,v,q,c,rin,rout are required.')
 x=data(p)
 if not (0<x['v']<x['H']<=800 and 0<x['q']<x['cv'] and 0<x['rout']<x['rin']<=60 and 0<x['c']<=2):raise ValueError('Physical/arithmetic bounds violated.')
 if evidence:
  if x['n']!=2:raise ValueError('Observed profiles require source exponent 2.')
 else:
  if not (2<=x['d']<=10 and 5<=x['a']<=100 and x['H']/x['v']<=4):raise ValueError('Authored arithmetic bounds violated.')
  if level in ('easy','moderate') and not(x['q'].is_Integer and x['cv'].is_Integer and (10*x['k']).is_Integer):raise ValueError('Easy/moderate retain integer initial amount/equilibrium amount and one-decimal coefficient workload.')
  if level=='easy' and not(x['n']==2 and x['a'].is_Integer and x['to'].is_Integer):raise ValueError('Easy requires exponent 2 and integer offset/time.')
  if level=='moderate' and not(x['n'] in (3,4) and x['a'].is_Integer and x['to'].is_Integer):raise ValueError('Moderate requires exponent 3/4 and integer offset/time.')
  if level=='hard' and not(x['n'] in (s.Rational(1,2),s.Rational(3,2)) and not x['a'].is_Integer and not x['to'].is_Integer):raise ValueError('Hard requires half-integer exponent and noninteger offset/time.')
 return x

def fill(mask,x,p):
 if s.simplify(x['amount']-s.Rational(x['rounded']))!=0:
  mask=mask.replace('& =<<rounded>>','& ≈<<rounded>>')
 if x['n']!=2:
  mask=mask.replace('<<n>>(<<a>>+t)Q','<<n>>(<<a>>+t)^{<<nm>>}Q')
 values={k:fmt(v) for k,v in x.items() if k not in ('Q','amount','rounded')};values['rounded']=x['rounded']
 # Source lexical form of this complete concentration is independently preserved.
 values['c']=r'\frac{2}{3}' if str(p['c'])=='2/3' else str(p['c']) if '/' not in str(p['c']) else s.latex(s.Rational(str(p['c'])))
 return re.sub(r'<<([a-zA-Z_]+)>>',lambda m:values[m[1]],mask)

def method_bank(x):
 """Whole bank: correct, omitted transient, exponent+1, exponent-1,
 initial amount omitted. No recipe replacement after collision rejection.
 """
 H,v,c,n,D0=x['H'],x['v'],x['c'],x['n'],x['D'];r=v/H
 vals=[x['amount'],c*H,c*H-D0*r**(n+1),c*H-D0*r**(n-1),c*H-c*v*r**n]
 displays=[rounded(v) for v in vals]
 if len(set(displays))!=5 or any(s.N(v)<=0 for v in vals):raise ValueError('Reject whole collided/nonphysical bank.')
 return [(display+r'\,\text{lb}',i==0) for i,display in enumerate(displays)]

def sample(level,rng):
 for _ in range(1000):
  d=rng.randint(2,10);n=2 if level=='easy' else rng.choice([3,4]) if level=='moderate' else rng.choice([s.Rational(1,2),s.Rational(3,2)])
  if level=='hard' and d%2:continue
  a=s.Integer(rng.randint(5,40))+(s.Rational(1,2) if level=='hard' else 0)
  to=s.Integer(rng.randint(5,50))+(s.Rational(1,2) if level=='hard' else 0)
  c=rng.choice(['0.4','0.5','0.6','0.8','1.0','1.2','1.5','2/3']);v=d*a;H=v+d*to
  q=s.Rational(str(c))*v*rng.choice([s.Rational(1,4),s.Rational(1,3),s.Rational(1,2),s.Rational(2,3)])
  p={k:str(vv) for k,vv in dict(H=H,v=v,q=q,c=c,rin=d*(n+1),rout=d*n).items()}
  try:x=guard(p,level);method_bank(x);return p
  except ValueError:continue
 raise RuntimeError('No eligible complete instance found.')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('Unknown difficulty.')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio response shape supported.')
 raw=bool(profile and profile.startswith('observed:'))
 repaired=bool(profile and profile.startswith('repaired:'))
 if profile and not(raw or repaired or profile=='method'):raise ValueError('Unknown profile.')
 if raw or repaired:
  sid=profile.split(':',1)[1]
  if template is not None and template!=sid:raise ValueError('Profile/template mismatch.')
  template=sid
 rng=random.Random(seed)
 template=template or rng.choice(list(MASKS))
 if template not in MASKS:raise ValueError('Unknown template.')
 mask=MASKS[template]
 if (raw or repaired) and level!='easy':raise ValueError('Observed sources are easy or unrated, never observed moderate/hard.')
 p=dict(parameters) if parameters is not None else dict(mask['base']) if raw or repaired else sample(level,rng)
 x=guard(p,level,raw or repaired)
 prompt=fill(mask['prompt'],x,p);solution=fill(mask['solution'],x,p) if mask['solution'] is not None else None
 if not raw:
  if solution is None:solution=fill(MASKS['q-336502']['solution'],x,p).replace('salt','nutrient').replace('reservoir','tank')
  if template=='q-336451':
   solution=solution.replace('minerals','salt').replace(r'\text{kg}',r'\text{lb}');prompt+=' Round to one decimal place.'
  # Varying exact answers still obey one uniform rounded answer specification.
  if template=='q-336451':solution=solution.replace('Finally, the amount','Finally, rounded to one decimal place, the amount')
 banks=[]
 if raw or repaired:
  base=data(mask['base'])
  for f in (mask['fields'] if raw else [mask['fields'][-1]]):
   opts=[]
   for a in f['options']:
    # Historical offsets are evidence-only lexical numerical patterns. Their
    # error interpretation is unresolved; no claim of method derivation.
    off=s.Rational(a['observed_numeric'])-s.Rational(base['rounded'])
    value=rounded(s.Rational(x['rounded'])+off)+a['display_suffix']
    opts.append((value,a['correct'] or (repaired and s.Rational(a['observed_numeric'])==s.Rational(base['rounded']))))
   banks.append((f['key'],f['has_correct'] or repaired,opts))
 else:banks=[('selection',True,method_bank(x))]
 # All displayed content, including full bank and actual level, enters identity.
 payload=[VERSION,level if not raw or mask['has_difficulty'] else None,prompt,solution,[[k,has,sorted(opts)] for k,has,opts in banks]]
 digest=stable(payload);qid=uid(digest);fields=[]
 for i,(key,has,opts) in enumerate(banks):
  fid=uid(qid+':field:'+str(i));answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v,_ in opts]
  correct=[a[':answer/id'] for a,(_,ok) in zip(answers,opts) if ok]
  rng.shuffle(answers)
  f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
  if has:
   if len(correct)!=1:raise ValueError('Missing/ambiguous supplied correct designation.')
   f[':answer-field/correct']=[':answer/id',correct[0]]
  fields.append(f)
 question={':question/id':qid,':question/problem':prompt,':question/answer-fields':fields}
 if not raw or mask['has_difficulty']:question[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:question[':question/worked-solution']=solution
 task=stable([str(x[k]) for k in ('H','v','q','c','rin','rout')])
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'level':level,'difficulty_provenance':'observed' if raw and mask['has_difficulty'] else 'omitted in raw source' if raw else 'authored workload policy','template':template,'profile':profile or 'method','seed':seed,'parameters':{k:str(v) for k,v in p.items()},'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'origin':'source replay' if raw or repaired else 'generated variant','evidence_only':raw or repaired,'eligible_for_learning':not(raw or repaired),'mathematical_fingerprint':task,'content_fingerprint':digest,'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'domain':'0 <= t <= overflow onset; capacity > initial volume, inflow > outflow, incoming concentration > initial concentration','bank_recipes':['correct','omit transient','use exponent n+1','use exponent n-1','omit initial amount'] if not(raw or repaired) else ['opaque historical offsets; not recovered error intent']}}

# EASY: observed exponent 2, integral offset/time; source-shared full method.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE (authored): same onset task; integer exponent 3/4 instead of square.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD (authored): same onset task; rational IF exponent and fractional offset/time.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r):
 q=r['question'];g=r['generation'];out=f"## {g['origin']} — {g['level']} ({g['difficulty_provenance']}) / {g['template']} / {g['profile']}\n\n"+q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):
  correct=f.get(':answer-field/correct',[None,None])[1]
  out+='\n'.join(f"- ${a[':answer/value']}$"+(' **supplied key**' if a[':answer/id']==correct else '') for a in f[':answer-field/choices'])+'\n\n'
 out+=q.get(':question/worked-solution','*Worked solution absent in raw evidence.*')+'\n\n'
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (LEVELS if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,indent=2) if a.format=='json' else '\n'.join(markdown(r) for r in records))
