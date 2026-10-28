#!/usr/bin/env python3
"""Unequal-rate dilution models. Frozen math/basis 1356 evidence, step 7 only.

Easy (authored missing level): supplied draining model, apply Q(0) to alpha+beta.
Moderate (observed): draining model, construct/solve to identify alpha-beta.
Hard (observed): filling model, construct/solve and evaluate at a positive time.
Default banks are authored neighboring numeric alternatives with variable rank.
Ten current source profiles preserve exact complete evidence, including absent
attributes only when absent from the supplied source; never eligible for learning.
Source masks preserve every fixed worked stage at original parameters and expose
quantity slots, with fixed per-family integer powers and stage omissions.
No plots, database reads/writes, shared edits, or registration.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,sys,uuid
from pathlib import Path
from decimal import Decimal,ROUND_HALF_UP
import sympy as sp
from math_format import normalize_prose,normalize_tex
KP_ID=17592186229182
D=Path(__file__).with_suffix('')
RAW=json.loads((D/'source-current.json').read_text());SRC=RAW['record']
SOURCES={q[':question/math-academy-id']:q for q in SRC[':knowledge-point/questions']}
M={x['source_id']:x for x in json.loads((D/'masks.json').read_text())}
VERSION='unequal-dilution-2-format-audit-9122-v1'
t=sp.Symbol('t',real=True)
NAMESPACE=uuid.UUID('2ab1d837-f782-5439-8e25-3c764f9cb5c5')
class IneligibleInstance(ValueError):pass

def exact(x):return sp.Rational(str(x))

def num(x):
 x=exact(x)
 if x.q==1:return str(x.p)
 z=Decimal(int(x.p))/Decimal(int(x.q))
 if x.q%2==0 or x.q%5==0:
  if sp.Rational(str(z))==x:return format(z,'f').rstrip('0').rstrip('.')
 return sp.latex(x)
def round2(x):return str(Decimal(str(sp.N(x,40))).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))
def tex(x):return sp.latex(x).replace('\\log','\\ln')
def fingerprint(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(NAMESPACE,x))
def data(p):
 V,q,c,ri,ro=[exact(p[k]) for k in ['V','q0','c','rin','rout']]
 delta=ri-ro;B=V/abs(delta);m=ro/abs(delta);s=1 if delta>0 else -1
 x=B+s*t;J=c*ri;a=J/(m+s);alpha=a*B;beta=q-alpha
 I=x**(s*m);primitive=J*x**(s*m+1)/(s*(s*m+1));C=beta*B**(s*m)
 Q=a*x+beta*(B/x)**(s*m)
 T=exact(p.get('T',0));ans=q if p.get('kind')=='sum' else alpha-beta if p.get('kind')=='difference' else Q.subs(t,T)
 rat=sp.Rational(B/(B+T))
 return dict(V=V,q0=q,c=c,rin=ri,rout=ro,delta=abs(delta),signed_delta=delta,B=B,m=m,s=s,x=x,J=J,a=a,alpha=alpha,beta=beta,deficit=-beta,I=I,primitive=primitive,C=C,absC=abs(C),Q=Q,T=T,answer=ans,rounded=round2(ans),partT=a*(B+T),BT=B+T,ratioN=rat.p,ratioD=rat.q)
def guard(p,meta,level,evidence=False):
 if 'T' in p and (p['kind']!='amount' or not 1<=exact(p['T'])<=30):raise ValueError('Evaluation time belongs only to amount questions and must be 1..30')
 if any(exact(p[k])<=0 for k in ['V','q0','c','rin','rout']):raise ValueError('Positive physical quantities required')
 if exact(p['rin'])==exact(p['rout']):raise ValueError('Unequal rates required')
 d=data(p)
 for k in ['V','q0','c','rin','rout']:
  if d[k]<=0:raise ValueError('Positive physical quantities required')
 if not (100<=d['V']<=1200 and 1<=d['q0']<=50 and sp.Rational('0.01')<=d['c']<=sp.Rational('0.08') and 4<=d['rin']<=60 and 4<=d['rout']<=60):raise ValueError('Authored arithmetic bounds exceeded')
 original=data(dict(meta['parameters'],kind=meta['kind']))
 if d['m']!=original['m'] or d['s']!=original['s']:raise ValueError('Family integer ratio/direction must be preserved')
 if d['B'].q!=1 or not 15<=d['B']<=200:raise ValueError('Integer normalized volume 15..200 required')
 if p['kind']=='amount':
  if not 1<=d['T']<=30 or d['T'].q!=1:raise ValueError('Evaluation time integer 1..30')
 if d['s']<0 and (d['T']<0 or d['T']>=d['B']):raise ValueError('Before emptying: 0<=t<B')
 if p['kind']!='amount' and 'T' in p:raise ValueError('No unassessed evaluation time parameter')
 return d

def fill(mask,d):
 return re.sub(r'\{\{(\w+)\}\}',lambda m:d['rounded'] if m[1]=='rounded' else num(d[m[1]]),mask)

def observed_bank(meta,d):
 # Exact supplied evidence only: no scaling of opaque source distractors.
 return [a['value']+a['suffix'] for a in meta['bank']]

def authored_bank(d,kind,rng):
 """Choose feasible numeric rank, then distinct nearby source-shaped alternatives.

 These are authored numerical alternatives, not inferred misconception recipes.
 No physical instance is rejected because its transient vanishes or changes sign.
 """
 target=sp.Rational(d['rounded']) if kind=='amount' else d['answer']
 step=sp.Rational(1,100) if kind=='amount' else sp.Integer(1)
 span=100 if kind=='amount' else max(8,int(abs(target)))
 lower=list(range(1,span+1))
 if kind in ['sum','amount']:
  lower=[i for i in lower if target-i*step>0]
 count=rng.choice(range(min(4,len(lower))+1))
 values=[target]+[target-i*step for i in rng.sample(lower,count)]+[target+i*step for i in rng.sample(range(1,span+1),4-count)]
 vals=[round2(x)+r'\,\text{kg}' if kind=='amount' else num(x) for x in values]
 assert len(set(vals))==5
 return vals,0

def signed_term(value,expression):
 if value==0:return ''
 return ('+' if value>0 else '-')+num(abs(value))+expression

def model_solution(d,kind):
 """Full method stages, unit cancellation and IC rows; one fixed solution."""
 V,ri,ro,c,J,B,m,a,alpha,deficit=[num(d[k]) for k in ['V','rin','rout','c','J','B','m','a','alpha','deficit']]
 sign='+' if d['s']>0 else '-';delta=num(d['delta']); x=f'({B}{sign}t)';vol=f'{V}{sign}{delta}t';n=int(d['s']*d['m']);
 I=f'{x}^{{{n}}}';Ip=f'{num(d["m"])}{x}^{{{n-1}}}';P=f'{J}\\cdot\\frac{{1}}{{{abs(n+1)}}}{x}^{{{n+1}}}'
 Q=tex(d['Q']);C=tex(d['C']);cpart=f'{a}{x}';const=tex(d['beta']);
 common=rf'''Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{{dQ}}{{dt}}=Q'_{{\text{{in}}}}-Q'_{{\text{{out}}}}.$$
The units of these rates are $\text{{kg/min}}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{{aligned}}Q'_{{\text{{in}}}}&=({c}\,\frac{{\text{{kg}}}}{{\text{{L}}}})\cdot({ri}\,\frac{{\text{{L}}}}{{\text{{min}}}})\\
&=({c}\,\frac{{\text{{kg}}}}{{\cancel{{\text{{L}}}}}})\cdot({ri}\,\frac{{\cancel{{\text{{L}}}}}}{{\text{{min}}}})\\&={J}\,\text{{kg/min}}.\end{{aligned}}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)={V}+{ri}t-{ro}t=({vol})\,\text{{L}}.$$
The concentration is $\frac{{Q}}{{{vol}}}\,\text{{kg/L}}.$ Hence,
$$\begin{{aligned}}Q'_{{\text{{out}}}}&=({ro}\,\frac{{\text{{L}}}}{{\text{{min}}}})\cdot(\frac{{Q}}{{{vol}}}\,\frac{{\text{{kg}}}}{{\text{{L}}}})\\
&=({ro}\,\frac{{\cancel{{\text{{L}}}}}}{{\text{{min}}}})\cdot(\frac{{Q}}{{{vol}}}\,\frac{{\text{{kg}}}}{{\cancel{{\text{{L}}}}}})\\
&=\frac{{{ro}Q}}{{{vol}}}\,\text{{kg/min}}=\frac{{{m}Q}}{{{B}{sign}t}}\,\text{{kg/min}}.\end{{aligned}}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{{aligned}}\frac{{dQ}}{{dt}}&=Q'_{{\text{{in}}}}-Q'_{{\text{{out}}}}\\&={J}-\frac{{{m}Q}}{{{B}{sign}t}}.\end{{aligned}}$$
Thus,
$$\frac{{dQ}}{{dt}}+\frac{{{m}}}{{{B}{sign}t}}Q={J}.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{{aligned}}I(t)&=e^{{\int {m}/({B}{sign}t)\,dt}}\\&=e^{{{n}\ln|{B}{sign}t|}}\\&=e^{{\ln {x}^{{{n}}}}}\\&={I}.\end{{aligned}}$$
Multiplying both sides by $I(t)={I}$ yields
$$\begin{{aligned}}{I}\cdot(\frac{{dQ}}{{dt}}+\frac{{{m}}}{{{B}{sign}t}}Q)&={I}\cdot {J}\\
{I}\frac{{dQ}}{{dt}}+{Ip}Q&={J}{I}\\\frac{{d}}{{dt}}(Q{I})&={J}{I}.\end{{aligned}}$$
Now, we integrate with respect to $t:$
$$\begin{{aligned}}\int\frac{{d}}{{dt}}(Q{I})\,dt&=\int {J}{I}\,dt\\Q{I}&={P}+C\\Q(t)&={cpart}+C{x}^{{{-n}}}.\end{{aligned}}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)={num(d['q0'])}.$ Thus,
$$\begin{{aligned}}{a}({B}{sign}0)+C({B}{sign}0)^{{{-n}}}&={num(d['q0'])}\\
{alpha}+C({B})^{{{-n}}}&={num(d['q0'])}\\C({B})^{{{-n}}}&={const}\\C&={C}.\end{{aligned}}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)={Q}.$$
'''
 if kind=='difference':
  common+=rf'''Writing this in the supplied normalized form gives
$$Q(t)={alpha}(1-\frac{{t}}{{{B}}}){signed_term(d['beta'],rf'(1-\frac{{t}}{{{B}}})^{{{m}}}')}.$$
Finally, we have $\alpha={alpha},\beta={const},$ and
$$\alpha-\beta={alpha}-({const})={num(d['answer'])}.$$'''
 else:
  T=num(d['T']);xT=f'({B}+{T})';ratio=rf'\frac{{{B}}}{{{B}+{T}}}';r=sp.Rational(d['B']/(d['B']+d['T']))
  common+=rf'''Finally, the amount in the tank ${T}$ minutes after pumping begins is
$$\begin{{aligned}}Q({T})&={a}{xT}{signed_term(d['beta'],rf'({ratio})^{{{m}}}')}\\&={num(d['partT'])}{signed_term(d['beta'],rf'({tex(r)})^{{{m}}}')}\\&\approx {d['rounded']}\,\text{{kg}}.\end{{aligned}}$$
This is rounded to two decimal places.'''
 return common

def sample(meta,rng,transient_sign):
 base=meta['parameters'];m=data(dict(base,kind=meta['kind']))['m'];s=1 if base['rin']>base['rout'] else -1
 delta=rng.choice([4,5,6,8,10,12]);ro=int(m*delta);ri=ro+s*delta
 B=rng.choice([18,25,30,40,50,60,70,80,90,100]);V=B*delta
 c=rng.choice([sp.Rational(i,100) for i in range(2,9)]+[sp.Rational(i,1000) for i in [25,35,45,55,65,75]])
 alpha=c*V
 step=rng.choice([sp.Integer(1),sp.Rational(1,10)])
 if transient_sign==0:q=alpha
 else:
  lo=1 if transient_sign<0 else max(1,sp.floor(alpha/step)*step+step)
  hi=min(50,sp.ceiling(alpha/step)*step-step) if transient_sign<0 else 50
  if lo>hi:raise IneligibleInstance('Resample quantities compatible with selected sign')
  q=rng.randint(int(sp.ceiling(lo/step)),int(sp.floor(hi/step)))*step
 return dict(V=V,q0=str(q),c=str(c),rin=ri,rout=ro,**({'T':rng.randint(3,25)} if meta['kind']=='amount' else {}))

# EASY: authored missing-level initial-condition interpretation.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: observed draining solve-and-identify coefficients (m=3 or 4).
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: observed filling solve-and-evaluate (m=1,2,3), exact work then rounding.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ['easy','moderate','hard']:raise ValueError('Unknown difficulty')
 if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('Only source-shaped radio supported')
 rng=random.Random(seed)
 if profile and profile.startswith('observed:'):
  st=profile.split(':',1)[1]
  if template and template!=st:raise ValueError('Profile/template mismatch')
  template=st
 meta=M.get(template) if template else rng.choice([x for x in M.values() if x['level']==level])
 if not meta or meta['level']!=level:raise ValueError('Template level mismatch')
 template=meta['source_id'];raw=profile==f'observed:{template}'
 transient_sign=rng.choice([-1,0,1])
 if raw and (parameters is None or any(exact(parameters[k])!=sp.Rational(v) for k,v in meta['parameters'].items())):raise ValueError('Observed profiles require exact source parameters')
 if profile not in [None,'authored-operations',f'observed:{template}']:raise ValueError('Unknown profile')
 for attempt in range(2000):
  try:
   p=dict(parameters) if parameters is not None else sample(meta,rng,transient_sign);p['kind']=meta['kind']
   if set(p)-{'V','q0','c','rin','rout','T','kind'}:raise ValueError('Unknown parameter')
   d=guard(p,meta,level,evidence=raw)
   if raw:
    vals=observed_bank(meta,d)
    if len(set(vals))!=5:raise IneligibleInstance('Opaque replay bank collision')
    correct=next((i for i,a in enumerate(meta['bank']) if a['correct']),None)
   else:vals,correct=authored_bank(d,meta['kind'],rng)
   break
  except (IneligibleInstance,ValueError):
   if parameters is not None:raise
 else:raise IneligibleInstance('No complete eligible instance')
 prompt=fill(meta['prompt_mask'],d)
 if raw:
  prompt=SOURCES[template][':question/problem']
  solution=SOURCES[template].get(':question/worked-solution')
 elif meta['kind']=='sum':solution=rf'''At $t=0,$ the supplied model gives $Q(0)=\alpha(1-0/{num(d['B'])})+\beta(1-0/{num(d['B'])})^{{{num(d['m'])}}}=\alpha+\beta.$ The initial amount is ${num(d['q0'])}\,\text{{kg}},$ so $\alpha+\beta={num(d['q0'])}.$'''
 else:solution=model_solution(d,meta['kind'])
 if not raw:prompt=normalize_prose(prompt);solution=normalize_prose(solution)if solution is not None else None;vals=[normalize_tex(v)for v in vals]
 identity=fingerprint(dict(version=VERSION,level=level if not raw or ':question/difficulty' in meta['raw_keys'] else None,prompt=prompt,solution=solution,bank=sorted(vals),correct=None if correct is None else vals[correct]))
 qid=uid(identity);fid=uid(qid+':selection');choices=[{':answer/id':uid(fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
 if correct is not None:field[':answer-field/correct']=[':answer/id',choices[correct][':answer/id']]
 rng.shuffle(choices)
 q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
 if ':question/requires-calculator' in SOURCES[template]:q[':question/requires-calculator']=SOURCES[template][':question/requires-calculator']
 if not raw or ':question/difficulty' in meta['raw_keys']:q[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:q[':question/worked-solution']=solution
 mathematical={'kind':meta['kind'],'V':str(d['V']),'q0':str(d['q0']),'c':str(d['c']),'rin':str(d['rin']),'rout':str(d['rout'])}
 if meta['kind']=='amount':mathematical['T']=str(d['T'])
 if meta['kind']=='sum':mathematical={'kind':'sum','initial_amount':str(d['q0'])}
 return {'knowledge_point':{'db_id':KP_ID,'id':str(NAMESPACE),'title':SRC[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':template,'profile':profile or 'authored-operations','seed':seed,'parameters':{k:str(v) for k,v in p.items() if k!='kind'},'mathematical_fingerprint':fingerprint(mathematical),'content_fingerprint':identity,'origin':'observed evidence replay' if raw else 'authored numeric bank and worked solution','difficulty_origin':'observed' if level!='easy' and ':question/difficulty' in meta['raw_keys'] else 'authored','eligible_for_learning':not raw,'evidence_only':raw,'bank_interpretation':'exact opaque source bank replay' if raw else 'rank-variable neighboring numeric alternatives','domain':f"t >= 0; V(t)>0"+ (f"; t < {num(d['B'])} min" if d['s']<0 else '; no capacity supplied; no overflow event assessed'),'source_parameter_replay':all(exact(p[k])==sp.Rational(v) for k,v in meta['parameters'].items()),'source':{k:RAW[k] for k in ['database','basis','lineage']},'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plots':'none'}}

def markdown(rec):
 q=rec['question'];g=rec['generation'];s=f"{g['template']} | {g['profile']} | {q.get(':question/difficulty','unrated original')} | eligible={g['eligible_for_learning']}\n\n{q[':question/problem']}\n\n"
 for f in q.get(':question/answer-fields',[]):
  key=f.get(':answer-field/correct',[None,None])[1]
  for a in f[':answer-field/choices']:s+=f"- ${a[':answer/value']}$"+(' [correct]' if a[':answer/id']==key else '')+'\n'
 return s+'\n'+q.get(':question/worked-solution','[Original omits worked solution.]')+'\n'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--originals',action='store_true',help='Replay captured originals with absent keys preserved');a=ap.parse_args()
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 if a.originals:
  cases=json.loads((D/'source-cases.json').read_text());recs=[generate(c['level'],a.seed,template=c['template'],parameters=c['parameters'],profile=c['bank_profile']) for c in cases if c['level'] in levels and (a.template is None or c['template']==a.template) and (a.profile is None or c['bank_profile']==a.profile)]
 else:recs=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(recs,indent=2) if a.format=='json' else '\n---\n'.join(map(markdown,recs)))
if __name__=='__main__':main()
