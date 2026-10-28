#!/usr/bin/env python3
"""Trigonometric indefinite integration by parts; captured math basis 7127.

Backbone: one affine linear factor, one observed trig primitive, one application
of parts, then the source's reduction/primitive/collection sequence. Hard keeps
the observed csc²/cot and sec²/tan quotient-to-log substitutions. No repeated parts,
definite bounds, exponential operators or new method branches. Explicit and
sampled inputs obey the same workload bounds. Empirical whole banks reproduce
historical expressions without claiming to know historical error intent.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,sys,uuid
import math_format as fmt
from functools import lru_cache
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
CAPTURE=json.loads((D/'source-data.json').read_text());KP=CAPTURE['record'];KP_ID=17592186064246
VERSION='trig-parts-2';X=s.Symbol('x',real=True);A,B,K,H=s.symbols('a b k h',real=True)
Z=K*X+H;U=A*X+B;S=s.sin(Z);T=s.cos(Z);SC=s.sin(A*X);TC=s.cos(A*X)
# Each tuple is the complete ordered two-component expression, never a pool.
# Empirical banks deliberately retain all source terms, including opaque patterns.
BANK_PARTS={
'q-12564':[(X*S/K**2,T/K),(-S/K,X*T/K**2),(U*S/K,A*T/K**2),(U*S/K**2,T/K),(U*S/K,-X*T/K)],
'q-14437':[(-A*X*s.sin(X),s.cos(X)),(A*X*s.cos(X),-X*s.sin(X)),(TC,X*SC),(-X*s.cos(X),-TC),(-A*X*s.cos(X),A*s.sin(X))],
'q-14449':[(TC,X*SC),(-A*X*s.sin(X),s.cos(X)),(-X*s.cos(X),-TC),(-A*X*s.cos(X),A*s.sin(X)),(A*X*s.cos(X),-X*s.sin(X))],
'q-114297':[(K*S,X*T/(2*K)),(S,-X*T/K),(2*A*X*S/K,A*T/K**2),(A*X*S/K,A*T/K**2),(X*S/K,-T/K**2)],
'q-114299':[(A*X*S/K,A*T/K**2),((A+1)*X*S/2,T/K),(X*S/K,-T/2),(-S/K,X*T/(K+A)),(-S/(2*K),X*T/2)],
'q-114309':[(-U*T/K,A*S/K**2),(-3*U*T/K,S/(3*K)),(-U*T/(2*K),S/(2*K**2)),(-U*T/(3*K),-S/K),(-U*T/(2*K),-S/K)],
'q-114311':[(-U*T,A*S),(X*T,-A*B*S),(U*T,-S),(A*X*T,A**2*S),(-U*T,-A**2*S)],
'q-114312':[(X*S/(3*K),T/K),(S/K**2,X*T/K),(X*S/K,-2*T/K**2),(A*X*S/K,A*T/K**2),(2*S/K,-X*T/(3*K))],
'q-114314':[(U*s.tan(Z),-A*s.log(s.Abs(s.cos(Z)))),(-U*s.cot(Z),A*s.log(s.Abs(s.sin(Z)))),(-U*s.cot(Z),-2*A*s.log(s.Abs(s.cos(Z)))),(U*s.tan(Z),-2*A*s.log(s.Abs(s.sin(Z)))),(-2*U*s.cot(Z),-A*s.log(s.Abs(s.sin(Z))))],
'q-14453':[(-A*X*s.sin(X),A*s.cos(X)),(X*TC,X*SC),(X*TC,-X*SC),(-A*X*s.cos(X),-s.cos(X)),(A*X*s.sin(X),A*s.cos(X))],
'q-74087':[(A*X*S,T),(A*X*S/K,A*T/K**2),(A*X*S,-T/K**2),(A*X*S,T/K),(A*X*S/K,-T)],
'q-74088':[(S,T),(U*S,T/A),(A*S,A*T),(U*S,A*T),(U*S/A,T)],
'q-74090':[(X*S/A,-T),(A*X*S,T/A),(A*X*S,A*T),(A*S,-A*X*T),(A*S,-T)],
'q-12565':[(-K*X*s.cos(X+H)/K,K*s.sin(X+H)/K**2),(T/K,X*S/K**2),(-A*X*T/K,A*S/K**2),(X*T/K**2,-S/K),(X*T/K**2,2*S/K**2)],
'q-14451':[(X*T/K**2,-S/K**2),(-A*X*T/K,A*S/K**2),(s.cos(A*K*X)/K**2,X*s.sin(A*K*X)/K**2),(-X*T/K,S/K**2),(X*T/K**2,S/K)]}
BANK_PARTS['q-2426']=[(U*s.cos(Z),-A*s.sin(Z)),(U*s.tan(Z),A*s.log(s.Abs(s.tan(Z)))),(U*s.tan(Z),A*s.log(s.Abs(s.cos(Z)))),(U*s.cos(Z),A*s.log(s.Abs(s.sin(Z)))),(U*s.tan(Z),-A*s.cos(Z))]
# level, trig family, representative source, optional explicit primitive row.
TEMPLATES={
 'sin_unit':('easy','sin','q-14437',False),
 'cos_frequency':('easy','cos','q-114297',False),
 'cos_frequency_expanded':('easy','cos','q-114299',True),
 'cos_unit_expanded':('easy','cos','q-14453',True),
 'cos_unit':('easy','cos','q-74090',False),
 'sin_frequency':('easy','sin','q-14451',False),
 'affine_cos':('moderate','cos','q-12564',False),
 'affine_sin':('moderate','sin','q-114309',False),
 'affine_sin_unit':('moderate','sin','q-114311',False),
 'phase_cos':('moderate','cos','q-74087',False),
 'affine_cos_unit':('moderate','cos','q-74088',False),
 'phase_sin':('moderate','sin','q-12565',False),
 'csc_log':('hard','csc','q-114314',False),
 'sec_log':('hard','sec','q-2426',False)}
SOURCE_CASES=[
 ('q-12564','affine_cos',dict(a=1,b=3,k=3,h=0)),('q-14437','sin_unit',dict(a=2,b=0,k=1,h=0)),
 ('q-114297','cos_frequency',dict(a=3,b=0,k=3,h=0)),('q-114299','cos_frequency_expanded',dict(a=2,b=0,k=4,h=0)),
 ('q-114309','affine_sin',dict(a=1,b=4,k=2,h=0)),('q-114311','affine_sin_unit',dict(a=2,b=3,k=1,h=0)),
 ('q-114312','cos_frequency',dict(a=1,b=0,k=5,h=0)),('q-114314','csc_log',dict(a=1,b=0,k=1,h=0)),
 ('q-14449','sin_unit',dict(a=5,b=0,k=1,h=0)),('q-14453','cos_unit_expanded',dict(a=6,b=0,k=1,h=0)),
 ('q-74087','phase_cos',dict(a=2,b=0,k=2,h=8)),('q-74088','affine_cos_unit',dict(a=6,b=1,k=1,h=0)),
 ('q-74090','cos_unit',dict(a=10,b=0,k=1,h=0)),('q-12565','phase_sin',dict(a=1,b=0,k=3,h=5)),
 ('q-14451','sin_frequency',dict(a=2,b=0,k=2,h=0)),
 ('q-2426','sec_log',dict(a=1,b=0,k=1,h=0))]
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
CASES={sid:(name,p) for sid,name,p in SOURCE_CASES};MATH=re.compile(r'\$\$.*?\$\$|\$(?!\$).*?\$',re.S)
def tex(v):
 t=s.latex(v).replace(r'\left', '').replace(r'\right','').replace(r'\log',r'\ln')
 for f in ['sin','cos','tan','cot','csc','sec']:t=t.replace('\\'+f,r'\operatorname{'+f+'}')
 return t

def tr(f,z):return r'\operatorname{'+f+'}('+tex(z)+')'
def coeff(c,t):
 c=s.Rational(c)
 if c==1:return t
 if c==-1:return '-'+t
 if c<0:return '-'+coeff(-c,t)
 if c.q==1:return str(c)+t
 return r'\frac{'+('' if c.p==1 else str(c.p))+t+'}{'+str(c.q)+'}'
def add(a,b):return a+('' if b.startswith('-') else '+')+b
def integral(body,var='x'):return r'\int '+body+r'\,\text{d}'+var
def aligned(rows):
 return '$$\n'+r'\begin{aligned}'+r' \\ '.join(left+' & ='+right for left,right in rows)+r'\end{aligned}'+'\n$$'

def validate_parameters(name,p):
 if name not in TEMPLATES:raise ValueError('Unknown template')
 if set(p)!=set('abkh') or any(type(v)!=int for v in p.values()):raise ValueError('Exact integer a,b,k,h keys required')
 a,b,k,h=(p[t] for t in 'abkh');level,f,*_=TEMPLATES[name]
 if not 1<=a<=10 or not 1<=k<=5 or abs(b)>8 or abs(h)>8:raise ValueError('Coefficient/shift bounds exceeded')
 if level=='easy' and (b or h):raise ValueError('Easy has no affine or phase shift')
 if name in ['sin_unit','cos_unit','cos_unit_expanded','affine_sin_unit','affine_cos_unit'] and k!=1:raise ValueError('Unit-frequency template requires k=1')
 if name in ['cos_frequency','cos_frequency_expanded','sin_frequency'] and k==1:raise ValueError('Frequency template requires k=2..5')
 if level=='moderate':
  if name.startswith('affine') and (b==0 or h!=0):raise ValueError('Affine moderate requires nonzero b, h=0')
  if name.startswith('phase') and (b!=0 or h==0 or k==1):raise ValueError('Phase moderate requires nonzero h, b=0, k=2..5')
  # Same source-scale arithmetic: products and reduced final denominators bounded.
  if abs(a*b)>64 or k*k>25:raise ValueError('Coupled moderate arithmetic bound')
 if level=='hard' and (b!=0 or k!=1):raise ValueError('Hard retains monomial u and unit inner slope')
 # All coefficients actually used in the source-shaped reduction fit source ceilings.
 for q in [s.Rational(a,k),s.Rational(a,k*k)]:
  if abs(q.p)>10 or q.q>25:raise ValueError('Reduced by-parts coefficient exceeds source workload')

def sample(name,rng):
 level,f,*_=TEMPLATES[name]
 p=dict(a=rng.randint(1,3 if level=='hard' else 10),b=0,k=1,h=0)
 if name in ['cos_frequency','cos_frequency_expanded','sin_frequency','affine_cos','affine_sin','phase_cos','phase_sin']:p['k']=rng.randint(2,5)
 if name.startswith('affine'):p['b']=rng.choice([n for n in range(-8,9) if n])
 if name.startswith('phase') or level=='hard':p['h']=rng.choice(list(range(-3,4))) if level=='hard' else rng.choice([n for n in range(-8,9) if n])
 return p

def mathdata(name,p):
 a,b,k,h=(s.Integer(p[t]) for t in 'abkh');u=a*X+b;z=k*X+h;f=TEMPLATES[name][1]
 if f=='cos':vp=s.cos(z);v=s.sin(z)/k;correct=u*v+a*s.cos(z)/k**2
 elif f=='sin':vp=s.sin(z);v=-s.cos(z)/k;correct=u*v+a*s.sin(z)/k**2
 elif f=='csc':vp=s.csc(z)**2;v=-s.cot(z);correct=-u*s.cot(z)+a*s.log(s.Abs(s.sin(z)))
 else:vp=s.sec(z)**2;v=s.tan(z);correct=u*s.tan(z)+a*s.log(s.Abs(s.cos(z)))
 return u,z,vp,v,correct

def presentation(name,p,sid):
 a,b,k,h=(s.Integer(p[t]) for t in 'abkh');f=TEMPLATES[name][1]
 u,z,vp,v,correct=mathdata(name,p)
 ut=tex(u); uf='('+ut+')' if b else ut
 zt=tex(z);ft=tr(f,z) if f in ['sin','cos'] else r'\operatorname{'+f+r'}^{2}('+zt+')'
 it=integral(uf+ft)
 if f=='cos':
  vt=coeff(1/k,tr('sin',z));first=coeff(1/k,uf+tr('sin',z))
  second=coeff(a/k**2,tr('cos',z));primitive=coeff(-1/k,tr('cos',z))
  rem=tr('sin',z); redsign=-1
 elif f=='sin':
  vt=coeff(-1/k,tr('cos',z));first=coeff(-1/k,uf+tr('cos',z))
  second=coeff(a/k**2,tr('sin',z));primitive=coeff(1/k,tr('sin',z))
  rem=tr('cos',z);redsign=1
 else:
  other='cot' if f=='csc' else 'tan'; inner='sin' if f=='csc' else 'cos'
  vt=('-' if f=='csc' else '')+tr(other,z);first=('-' if f=='csc' else '')+uf+tr(other,z)
  second=coeff(a,r'\ln|'+tr(inner,z)+'|')
  rem=r'\frac{'+tr('cos' if f=='csc' else 'sin',z)+'}{'+tr(inner,z)+'}'
  redsign=1 if f=='csc' else -1
 final=add(first,second)+'+C'
 formula='$$\n'+r'\int uv^{\prime}\,\mathrm{d}x=uv-\int vu^{\prime}\,\mathrm{d}x.'+'\n$$'
 defs=aligned([('u',ut), (r'u^{\prime}',str(a)),(r'v^{\prime}',ft),('v',vt)])
 # Keep every equality and ordered operator input in visible aligned displays.
 setup=aligned([('uv',uf+r'\left('+vt+r'\right)'),(integral(r'vu^{\prime}'),integral(r'\left('+vt+r'\right)'+str(a)))])
 reduction=add(first,coeff(redsign*a/k,integral(rem)))
 rows=[('I',reduction)]
 if f in ['sin','cos']:
  rows += [('',add(first,coeff(redsign*a/k,'('+primitive+')'))+'+C'),('',final)]
  ending=aligned(rows)
  extra=''
 else:
  # A fresh letter avoids redefining the parts variable while displaying the substitution.
  dr=tr('cos',z) if f=='csc' else '-'+tr('sin',z)
  extra='Use $t='+tr(inner,z)+'$ and $'+r'\mathrm{d}t='+dr+r'\,\mathrm{d}x$. '
  rows += [('',add(first,coeff(a,integral(r'\frac{1}{t}','t')))),('',add(first,coeff(a,r'\ln|t|'))+'+C'),('',final)]
  ending=aligned(rows)
 original=SOURCES[sid][':question/problem']
 prompt=('Calculate ' if 'Calculate' in original else '')+'$$\n'+it+('.' if 'Calculate' in original else '=')+'\n$$'
 worked='Write $I='+it+'$. Use integration by parts.\n\n'+formula+'\n\nChoose the linear factor as $u$:\n\n'+defs+'\n\nSubstitute into the formula:\n\n'+setup+'\n\n'+extra+'Evaluate the remaining integral:\n\n'+ending
 if f in ['sec','csc']:
  worked+='\n\nThis holds on each interval where $'+tr(inner,z)+r'\ne0$.'
 return prompt,worked,final

@lru_cache(maxsize=20000)
def primitive_equivalent(a,b):
 d=s.expand(s.diff((a-b).replace(s.Abs,lambda x:x),X))
 return d==0 or s.trigsimp(d,method='fu')==0

def bank(name,p,profile):
 u,z,vp,v,correct=mathdata(name,p);a=s.Integer(p['a']);k=s.Integer(p['k']);f=TEMPLATES[name][1]
 if profile.startswith('observed:'):
  sid=profile.split(':',1)[1]
  if sid not in CASES or CASES[sid][0]!=name:raise ValueError('Profile/template mismatch')
  subs={A:p['a'],B:p['b'],K:p['k'],H:p['h']};parts=[tuple(t.subs(subs) for t in row) for row in BANK_PARTS[sid]]
  eligible=False;origin='empirical complete-bank expressions; historical intent unresolved'
 elif profile.startswith('authored:grid:'):
  # A complete rectangle of independently possible uv/residual coefficient errors.
  # Whole error profile is chosen before parameters. No first-valid recipe subset.
  style=profile.split(':')[2];direction=profile.split(':')[3]
  q=k if k>1 else a if a>1 else s.Integer(2)
  n,m={'over':(q,q),'under':(1/q,1/q),'mixed':(q,1/q),
       'sign-product':(-1,q),'sign-residual':(q,-1)}[style]
  n,m=s.Rational(n),s.Rational(m)
  residual=correct-u*v
  parts=[(u*v,residual),(u*v,m*residual),(n*u*v,residual),
         (n*u*v,m*residual),((n*n if direction=='forward' else 1/n)*u*v,(m*m if direction=='forward' else 1/m)*residual)]
  eligible=True;origin='authored complete coefficient-error grid: '+style
 else:raise ValueError('Unknown complete bank profile')
 vals=[s.Add(*r) for r in parts]
 # Exact differential comparison models arbitrary constants on regular intervals.
 def local(e):return e.replace(s.Abs,lambda x:x)
 def eq(a,b):return primitive_equivalent(a,b)
 if any(e.has(s.zoo,s.nan,s.oo,s.I) for e in vals):raise ValueError('Invalid whole bank')
 if sum(eq(e,correct) for e in vals)!=1 or any(eq(a,b) for i,a in enumerate(vals) for b in vals[i+1:]):raise ValueError('Ambiguous whole bank')
 return parts,vals,eligible,origin

def fingerprint(name,p):
 u,z,vp,v,c=mathdata(name,p)
 # Source labels, profile, style and option order do not define a mathematical task.
 return hashlib.sha256(s.srepr(s.expand(u)*vp).encode()).hexdigest()
def uid(kind,data):return str(uuid.uuid5(uuid.NAMESPACE_URL,kind+json.dumps(data,sort_keys=True,ensure_ascii=False)))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ['easy','moderate','hard']:raise ValueError('Unknown difficulty')
 if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('Only observed radio response contract supported')
 rng=random.Random(seed);eligible=[n for n,t in TEMPLATES.items() if t[0]==level]
 if profile and profile.startswith('observed:'):
  sid=profile.split(':',1)[1]
  if sid not in CASES:raise ValueError('Unknown observed profile')
  inferred=CASES[sid][0]
  if template is not None and template!=inferred:raise ValueError('Template/profile mismatch')
  template=inferred
 name=template or rng.choice(eligible)
 if name not in eligible:raise ValueError('Template/difficulty mismatch')
 # Select whole profile before any parameters; no first-valid subset selection.
 profile=profile or rng.choice(['authored:grid:'+v for v in ['over','under','mixed','sign-product','sign-residual']])
 if profile.startswith('authored:grid:') and len(profile.split(':'))==3:profile+=':'+rng.choice(['forward','reverse'])
 sid=profile.split(':',1)[1] if profile.startswith('observed:') else TEMPLATES[name][2]
 for attempt in range(1000):
  p=dict(parameters) if parameters is not None else sample(name,rng)
  try:
   validate_parameters(name,p);parts,vals,learning,origin=bank(name,p,profile)
  except (ValueError,ZeroDivisionError):
   if parameters is not None:raise
   continue
  break
 else:raise ValueError('No eligible whole instance')
 prompt,worked,final=presentation(name,p,sid);prompt=fmt.normalize_prose(prompt);worked=fmt.normalize_prose(worked)
 # No answer CAS collapse changes the supplied whole-primitive +C contract.
 values=[fmt.normalize_tex(add(tex(a),tex(b))+'+C') for a,b in parts]
 u,z,vp,v,correct=mathdata(name,p)
 def eq(e):return primitive_equivalent(e,correct)
 ci=next(i for i,e in enumerate(vals) if eq(e))
 identity={'version':VERSION,'difficulty':level,'prompt':prompt,'solution':worked,'bank':sorted(values)};qid=uid('question',identity);fid=uid('field',[qid,'selection'])
 answers=[{':answer/id':uid('answer',[fid,value]),':answer/type':':answer.type/math',':answer/value':value} for value in values]
 ref=[':answer/id',answers[ci][':answer/id']];rng.shuffle(answers)
 record={'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':ref}]},'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'bank_origin':origin,'parameter_fingerprint':fingerprint(name,p),'eligible_for_learning':learning,'evidence_only':not learning,'source_reference':sid,'source_provenance':{k:CAPTURE[k] for k in ['database','basis','lineage']},'domains':('real x; '+('sin' if TEMPLATES[name][1]=='csc' else 'cos')+'(x+h) nonzero on each connected interval' if level=='hard' else 'real x'),'runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'plots':'none'}}
 fmt.validate_generated_record(record)
 for text in [prompt,worked,*values]:
  if any(ord(c)<32 and c not in '\n\t' for c in text):raise ValueError('C0 control character')
 return record

# Easy: one monomial factor and unshifted sin/cos; observed primitive/reduction.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: exactly one affine-linear or phase shift; observed same one-parts chain.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: observed csc², cot ratio and logarithmic substitution, no new trig branch.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
 q=r['question'];g=r['generation'];f=q[':question/answer-fields'][0]
 return '\n\n'.join(['Level: '+q[':question/difficulty'].split('/')[-1]+'; template: '+g['template']+'; profile: '+g['bank_profile']+'; field type: radio',q[':question/problem'],'\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices']),q.get(':question/worked-solution','*Raw source has no worked-solution key.*')])
def batch(level,count,seed):
 if count<0:raise ValueError('Count must be nonnegative')
 rng=random.Random(seed);names=([n for n,t in TEMPLATES.items() if t[0]==level and n not in ['cos_frequency_expanded','cos_unit_expanded']])
 styles=['over','under','mixed','sign-product','sign-residual'];seen=set();out=[]
 # Cycle branches rather than accidentally serving amplitude clones of one branch.
 order=[];profiles=[];occurrences={};start={(n,c):rng.randrange(2) for n in names for c in ['positive','sign-product','sign-residual']}
 while len(out)<count:
  if not order:order=list(names);rng.shuffle(order)
  if not profiles:profiles=list(styles);rng.shuffle(profiles)
  name=order.pop();style=profiles.pop()
  cue_group=(name,style if style.startswith('sign-') else 'positive')
  direction=['forward','reverse'][(start[cue_group]+occurrences.get(cue_group,0))%2]
  occurrences[cue_group]=occurrences.get(cue_group,0)+1
  profile='authored:grid:'+style+':'+direction
  for attempt in range(1000):
   r=generate(level,rng.getrandbits(63),template=name,profile=profile)
   fp=r['generation']['parameter_fingerprint']
   if fp not in seen:break
  else:raise ValueError('Requested batch exceeds semantic support')
  seen.add(fp);r['generation']['batch_seed']=seed;out.append(r)
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all','unclassified'],default='easy');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 level='easy' if args.difficulty=='unclassified' else args.difficulty
 records=[]
 for band in (['easy','moderate','hard'] if level=='all' else [level]):
  if args.template or args.profile:
   records.extend(generate(band,args.seed+i,template=args.template,profile=args.profile) for i in range(args.count))
  else:records.extend(batch(band,args.count,args.seed))
 print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
