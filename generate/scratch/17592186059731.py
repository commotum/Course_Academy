#!/usr/bin/env python3
"""Orthogonal vectors: component products -> zero -> solve one unknown.

Basis1356 source fidelity precedes authored banks. Eight observed prompt/field
families; opaque source scalar banks are explicit evidence profiles, never the
default bank. No plots, database access or additional vector geometry. Hard is
an authored SAME square-root workload with three signed products, two square
terms and a small rational radicand; not an observed MA difficulty label.
See adjacent extraction, source-cases and validator. Exact inputs are guarded.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
import sympy as sp

KP_ID=17592186059731
KP_UUID='8bff08bf-0035-5f05-9607-493b301e8717'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
TITLE='Solving for an Unknown Given Two Perpendicular Vectors'
VERSION='perpendicular-1.0'
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES={
 'linear2':('easy','radio','p','q','n'),
 'linear3':('easy','blank','c','d','k'),
 'square2_blank':('easy','blank','a','b','x'),
 'square2_shared':('moderate','radio','u','v','x'),
 'square2_scaled':('moderate','radio','u','v','x'),
 'square3_collect':('moderate','radio','g','h','r'),
 'square3_shared':('moderate','radio','u','v','a'),
 'repeated3':('moderate','radio','a','b','x'),
 'hard_square3':('hard','radio','g','h','r'),
 'hard_square3_blank':('hard','blank','g','h','r'),
}
DEFAULTS={'easy':['linear2','linear3','square2_blank'], 'moderate':['square2_scaled','square3_collect','square3_shared'], 'hard':['hard_square3','hard_square3_blank']}
# Tuple entries multiply the computed root; these profiles preserve complete
# scalar evidence only. Their authoring intent is explicitly unrecovered.
PROFILES={
 'observed_q1348':('linear2',(sp.Rational(11,7),1,sp.Rational(3,28),2,-1)),
 'observed_q19021':('square2_shared',(sp.Rational(3,2),4,sp.Rational(1,2),2,1)),
 'observed_q19022':('repeated3',(-2,2,1,3,-1)),
 'observed_q101417':('square2_scaled',(sp.Rational(1,3),sp.Rational(5,3),1,sp.Rational(4,3),sp.Rational(2,3))),
 'observed_q19023':('square3_collect',None),
 'observed_q77152':('square3_shared',(sp.Rational(9,4),sp.Rational(1,4),sp.Rational(1,2),2,1)),
}

def tex(x):
 return sp.latex(sp.sympify(x)).replace(r'\sqrt{',r'\sqrt{').replace(' ', '')
def powtex(v): return '{'+v+'}^{2}'
def term(c,body=''):
 c=sp.sympify(c)
 if not body:return tex(c)
 if c==1:return body
 if c==-1:return '-'+body
 return tex(c)+body

def sumtex(items):
 return ''.join(('+' if i and not s.startswith('-') else '')+s for i,s in enumerate(items))
def poly(c,d,v,power=1,constant_first=False):
 b=powtex(v) if power==2 else v
 seq=[term(c,b),tex(d)] if not constant_first else [tex(d),term(c,b)]
 return sumtex([s for s in seq if s!='0']) or '0'
def atom(s):return '('+s+')' if s.startswith('-') else s
def align(rows):return '\n$$\n\\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def vector(items,style='column'):
 return '['+r'\begin{aligned}'+r' \\ '.join(items)+r'\end{aligned}]' if style=='column' else '⟨'+','.join(items)+'⟩'

def mathematics(name,p):
 _,_,u,v,w=TEMPLATES[name]; x=sp.Symbol(w,real=True)
 if name=='linear2':
  a,b,c=p['a'],p['b'],p['c']; U=[a,x]; V=[b,c]; C=a*b; A=c; R=-sp.Rational(C,A); degree=1
 elif name=='linear3':
  a,b,c,d,e=p['a'],p['b'],p['c'],p['d'],p['e']; U=[x,a*x,b]; V=[c,d,e]; A=c+a*d; C=b*e; R=-sp.Rational(C,A) if A else None;degree=1
 elif name=='square2_blank':
  a,b,c,d=p['a'],p['b'],p['c'],p['d'];U=[a*x**2,b];V=[c,d];A=a*c;C=b*d;degree=2;R=None
 elif name=='square2_shared':
  a=p['a'];U=[x,-a];V=[x,a];A=1;C=-a*a;degree=2;R=None
 elif name=='square2_scaled':
  a,b,c=p['a'],p['b'],p['c'];U=[a,b*x];V=[c,x];A=b;C=a*c;degree=2;R=None
 elif name in ('square3_collect','hard_square3','hard_square3_blank'):
  a,b,c,d,e,f=[p[k] for k in 'abcdef'];U=[a*x**2,c,e];V=[b,d*x**2,f];A=a*b+c*d;C=e*f;degree=2;R=None
 elif name=='square3_shared':
  a,b,c,d=[p[k] for k in 'abcd'];U=[x,a,b];V=[x,c,d];A=1;C=a*c+b*d;degree=2;R=None
 elif name=='repeated3':
  t=p['t'];U=[x,-2*t*x,t];V=[x,1,t];A=1;C=t*t;degree=2;R=sp.Integer(t)
 if not A:raise ValueError('dot equation must have nonzero leading coefficient')
 if name!='repeated3' and degree==2:
  rad=-sp.Rational(C,A)
  if rad<=0:raise ValueError('positive square-root radicand required')
  R=p['sign']*sp.sqrt(rad)
 else:rad=None
 return x,U,V,sp.expand(sum(a*b for a,b in zip(U,V))),sp.sympify(R),A,C,rad

def guard(name,p,profile):
 required={'linear2':'abc','linear3':'abcde','square2_blank':'abcd','square2_shared':'a','square2_scaled':'abc','square3_collect':'abcdef','square3_shared':'abcd','repeated3':'t','hard_square3':'abcdef','hard_square3_blank':'abcdef'}[name]
 allowed=set(required)|({'sign'} if name.startswith('square') or name.startswith('hard') else set())
 if set(p)!=allowed:raise ValueError(f'exact parameter keys required: {sorted(allowed)}')
 if any(isinstance(z,bool) or not isinstance(z,int) for z in p.values()):raise ValueError('integer components/sign required')
 if any(not p[k] or abs(p[k])>12 for k in required):raise ValueError('nonzero component coefficients of magnitude <=12 required')
 if 'sign' in p and p['sign'] not in (-1,1):raise ValueError('sign must be +/-1')
 x,U,V,dot,r,A,C,rad=mathematics(name,p)
 if profile and profile.startswith('observed_'):
  if profile not in PROFILES or PROFILES[profile][0]!=name:raise ValueError('profile/template mismatch')
 else:
  level=TEMPLATES[name][0]
  if level=='easy':
   if max(abs(p[k]) for k in required)>8:raise ValueError('easy coefficient bound 8')
   if rad is not None and (rad.q!=1 or sp.sqrt(rad).is_integer is not True or rad>64):raise ValueError('easy requires familiar integer square root')
   if rad is None and (r.q>8 or abs(r)>40):raise ValueError('easy linear answer bounds')
  elif level=='moderate':
   if max(abs(p[k]) for k in required)>9:raise ValueError('moderate coefficient bound 9')
   if rad is not None and (rad.q!=1 or rad>64):raise ValueError('moderate positive integer radicand <=64')
   if name=='repeated3' and not 3<=abs(p['t'])<=8:raise ValueError('repeated-root scope 3..8')
  else:
   if not (2<=abs(A)<=6 and 2<=rad.p<=30 and 2<=rad.q<=6 and sp.sqrt(rad).is_rational is False):raise ValueError('hard needs nonunit collected coefficient and small nonsquare rational radicand')
   if any(abs(p[k])<2 for k in required):raise ValueError('hard all three products must have nonunit component coefficients')
 if U==[0]*len(U) or V==[0]*len(V):raise ValueError('nonzero vectors required')
 return x,U,V,dot,r,A,C,rad

def render(name,p,m):
 level,kind,u,v,w=TEMPLATES[name];x,U,V,dot,r,A,C,rad=m
 # Build complete coordinate slots, never global substring replacements.
 ut=[tex(z).replace(w+'^{2}',powtex(w)) for z in U];vt=[tex(z).replace(w+'^{2}',powtex(w)) for z in V]
 style='angle' if name in ('square2_blank','repeated3') else 'column'
 vs=[vector(ut,style),vector(vt,style)]
 if name=='square2_shared':vs=[r'\begin{bmatrix}'+r' \\ '.join(t)+r'\end{bmatrix}' for t in (ut,vt)]
 relation=f'{w}'+('>0' if p.get('sign',0)>0 else '<0')
 if name=='linear2':prompt=f'Let ${u}={vs[0]}$ and ${v}={vs[1]}.$ Given that ${u}⊥{v}$, find the value of ${w}.$'
 elif name=='linear3':prompt=f'If ${u}={vs[0]},$ ${v}={vs[1]},$ and ${u}⊥{v},$ then ${w}=${{{{field-1}}}}.'
 elif name=='square2_blank':prompt=f'Let ${u}={vs[0]}$ and ${v}={vs[1]}.$ If ${u}⊥{v}$ and ${relation},$ then ${w}=${{{{field-1}}}}.'
 elif name=='repeated3':prompt=f'What is the value of ${w}$ given that ${u} = ⟨{ut[0]},{ut[1]}, {ut[2]}⟩, {v} = ⟨{vt[0]}, {vt[1]}, {vt[2]}⟩$ and ${u}⊥{v}$?'
 elif name=='square2_shared':prompt=f'Let ${u} = {vs[0]}$ and ${v} = {vs[1]}$. Given that ${u}⊥{v}$ and ${w} '+('> 0' if p['sign']>0 else '< 0')+f'$, find the value of ${w}$.'
 else:
  prompt=f'Let ${u}={vs[0]}$ and ${v}={vs[1]}.$ Given that ${u}⊥{v}$ and ${relation}$, find the value of ${w}.$'
  if kind=='blank':prompt+=f'\n\n${w}=${{{{field-1}}}}.'
 lead=f'We know that ${u}⊥{v}$ (${u}$ and ${v}$ are perpendicular) if and only if ${u}\\cdot {v}=0.$'
 formal='+'.join('{'+u+'}_{'+s+r'}\cdot {'+v+'}_{'+s+'}' for s in 'xyz'[:len(U)])
 products='+'.join(atom(a)+r'\cdot '+atom(b) for a,b in zip(ut,vt))
 if name=='linear2':reduced=poly(A,C,w,constant_first=True);evaluated=[reduced]
 elif name=='linear3':reduced=poly(A,C,w);evaluated=[sumtex([term(p['c'],w),term(p['a']*p['d'],w),tex(C)]),reduced]
 elif name=='square2_scaled':reduced=poly(A,C,w,2,True);evaluated=[reduced]
 elif name in ('square3_collect','hard_square3','hard_square3_blank'):
  reduced=poly(A,C,w,2);evaluated=[sumtex([term(p['a']*p['b'],powtex(w)),term(p['c']*p['d'],powtex(w)),tex(C)]),reduced]
 elif name=='repeated3':reduced=sumtex([powtex(w),term(-2*p['t'],w),tex(C)]);evaluated=[reduced]
 else:reduced=poly(A,C,w,2);evaluated=[reduced]
 dotrows=[u+r'\cdot '+v+' & ='+formal,' & ='+products]+[' & ='+s+('.' if i==len(evaluated)-1 else '') for i,s in enumerate(evaluated)]
 rows=[u+r'\cdot '+v+' & =0',reduced+' & =0']
 if name=='linear2':rows +=[tex(C)+' & ='+term(-A,w),w+' & ='+tex(r)]
 elif name=='linear3':rows +=[w+' & ='+tex(r)+'.']
 elif name=='repeated3':rows +=['('+poly(1,-p['t'],w)+')^{2} & =0',poly(1,-p['t'],w)+' & =0',w+' & ='+tex(r)]
 else:
  if A!=1:rows +=[term(A,powtex(w))+' & ='+tex(-C)]
  rows +=[powtex(w)+' & ='+tex(rad),w+r' & =\pm '+tex(sp.sqrt(rad))+('.' if name=='square2_blank' else '')]
 colon='' if name in ('linear3','square2_blank') else ':'
 solution=lead+'\n\nComputing the dot product, we have\n'+align(dotrows)+'\n\nSetting the dot product equal to $0,$ we obtain'+colon+'\n'+align(rows)
 if rad is not None:
  excluded='negative' if p['sign']>0 else 'positive'
  solution+=f'\n\nWe disregard the {excluded} solution since we are told that ${relation}.$ Therefore, ${w}={tex(r)}.$'
 return prompt,solution

def bank(name,p,m,profile):
 _,_,_,_,_=TEMPLATES[name]; x,U,V,dot,r,A,C,rad=m
 if profile in PROFILES:
  if profile=='observed_q19023':
   s=p['sign']; values=[s*sp.sqrt(2*rad),s*rad,s*2*rad,r,s*rad/2]
   strings=[('-' if s<0 else '')+r'\sqrt{'+tex(2*rad)+'}',tex(s*rad),tex(s*2*rad),tex(r),tex(s*rad/2)]
  else:
   values=[r*c for c in PROFILES[profile][1]];strings=[tex(z) for z in values]
  recipes=['opaque_source_anchor_'+str(i+1) for i in range(len(values))]
 elif rad is not None:
  values=[r,-r,p['sign']*rad,p['sign']/sp.sqrt(rad),sp.Integer(0)];strings=[tex(z) for z in values]
  recipes=['correct','opposite_root_violates_sign','omit_square_root','invert_radicand','omit_constant_products']
 elif name=='repeated3':
  values=[r,-r,2*r,r*r,sp.Integer(0)];strings=[tex(z) for z in values]
  recipes=['correct','reverse_sign','use_linear_coefficient_magnitude','use_constant_product','omit_constant_product']
 else:
  values=[r,-r,-sp.Integer(C),-sp.Rational(A,C),sp.Integer(0)];strings=[tex(z) for z in values]
  recipes=['correct','reverse_transposition_sign','omit_coefficient_division','invert_solved_ratio','omit_constant_products']
 if any(z.is_real is not True for z in values) or len({sp.srepr(sp.simplify(z)) for z in values})!=5:raise ValueError('entire five-option bank invalid or equivalent')
 eligible=[i for i,z in enumerate(values) if sp.simplify(dot.subs(x,z))==0 and (rad is None or z*p['sign']>0)]
 if len(eligible)!=1:raise ValueError('bank must have exactly one eligible perpendicular root')
 return strings,eligible[0],recipes

# EASY: original linear 2D radio, collected 3D linear blank, and integer-square
# 2D blank workloads. No hidden progression within any template.
def sample(name,rng):
 if name=='linear2':return dict(a=rng.choice([-7,-5,-3,3,5,7]),b=rng.choice([-6,-4,-2,2,4,6]),c=rng.choice([-6,-4,-2,2,4,6]))
 if name=='linear3':return dict(a=rng.choice([-3,-2,2,3]),b=rng.choice([-6,-4,-2,2,4,6]),c=rng.choice([-5,-3,3,5]),d=rng.choice([-3,-2,2,3]),e=rng.choice([-3,-2,2,3]))
 if name=='square2_blank':
  a=rng.choice([1,2,3,4]);c=rng.choice([1,2]);root=rng.choice([1,2,3]);return dict(a=a,b=-a*root*root,c=c,d=c,sign=rng.choice([-1,1]))
 if name=='square2_shared':return dict(a=rng.randint(2,8),sign=rng.choice([-1,1]))
 if name=='square2_scaled':
  a=rng.choice([2,3,4,6,8,9]);return dict(a=a,b=rng.choice([2,3,4]),c=-rng.choice([2,3,4,6]),sign=rng.choice([-1,1]))
 if name=='square3_shared':return dict(a=rng.choice([2,3,4]),b=rng.choice([2,3,4]),c=-rng.choice([2,3,4]),d=-rng.choice([2,3,4]),sign=rng.choice([-1,1]))
 if name=='repeated3':return dict(t=rng.choice([-7,-6,-5,-4,-3,3,4,5,6,7]))
 # MODERATE: integer radicand. HARD: same three dot products and square-root
 # stages, with two nonunit squared contributions and reduced denominator 2..6.
 bound=9 if name=='square3_collect' else 12
 return dict(a=rng.choice([1,2,3,4]) if name=='square3_collect' else rng.choice([2,3,4]),b=rng.choice([2,3,4]),c=-rng.choice([1,2,3,4]) if name=='square3_collect' else -rng.choice([2,3,4]),d=rng.choice([1,2,3]),e=-rng.randint(2,bound),f=rng.randint(2,4),sign=rng.choice([-1,1]))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in DEFAULTS:raise ValueError('unknown difficulty')
 rng=random.Random(seed)
 if profile and profile.startswith('observed_'):
  if profile not in PROFILES:raise ValueError('unknown observed profile')
  if template is None:template=PROFILES[profile][0]
 choices=[n for n in DEFAULTS[level] if field_type in (None,TEMPLATES[n][1])]
 if template is None:
  if not choices:raise ValueError('no template for requested field type')
  template=rng.choice(choices)
 if template not in TEMPLATES or TEMPLATES[template][0]!=level:raise ValueError('template/level mismatch')
 if field_type not in (None,TEMPLATES[template][1]):raise ValueError('field type mismatch')
 if profile not in (None,'authored_operations') and profile not in PROFILES:raise ValueError('unknown profile')
 kind=TEMPLATES[template][1]
 if kind=='blank' and profile not in (None,'authored_operations'):raise ValueError('blanks have no bank profile')
 for attempt in range(10000):
  p=dict(parameters) if parameters is not None else sample(template,rng)
  try:
   m=guard(template,p,profile);prompt,solution=render(template,p,m)
   if kind=='radio':values,ci,recipes=bank(template,p,m,profile)
   else:values,ci,recipes=[tex(m[4])],0,['exact_unknown_fragment']
   break
  except (ValueError,ZeroDivisionError):
   if parameters is not None:raise
 else:raise ValueError('cannot sample eligible complete instance')
 actual_profile=profile or ('authored_operations' if kind=='radio' else 'blank')
 content={'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(values),'field_type':kind}
 digest=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
 qid=str(uuid.uuid5(uuid.NAMESPACE_URL,'perpendicular:'+digest));fid=str(uuid.uuid5(uuid.UUID(qid),'field'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/math',':answer/value':value} for value in values]
 correct=answers[ci][':answer/id'];rng.shuffle(answers)
 # Mathematical task identity excludes bank, profile, field layout and variable
 # aliases, but preserves ordered printed vector component functions and sign.
 canonical=sp.Symbol('X',real=True)
 fingerprint=hashlib.sha256(json.dumps({'vectors':[[sp.srepr(sp.sympify(z).subs(m[0],canonical)) for z in V] for V in (m[1],m[2])],'sign':p.get('sign')},sort_keys=True).encode()).hexdigest()
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'field-1' if kind=='blank' else 'selection',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'source':SOURCE,'sympy_version':sp.__version__,'seed':seed,'template':template,'parameters':p,'profile':actual_profile,'bank_origin':'observed_opaque_evidence' if actual_profile.startswith('observed_') else 'authored_operations' if kind=='radio' else 'authored_blank_layout' if level=='hard' else 'observed_blank_layout','recipes':recipes,'content_sha256':digest,'mathematical_fingerprint':fingerprint,'authored_level':level=='hard','plot_rating':'none'}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: source integer radicands, sign-root selection; repeated-root prompt
# is an unrated observed family with explicitly authored moderate assignment.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: authored rational radicand extension of square3_collect, same method.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(record):
 q=record['question'];f=q[':question/answer-fields'][0]
 out=q[':question/problem']+'\n\n'
 if f[':answer-field/type'].endswith('/radio'):out+='\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'
 return out+'Worked solution\n\n'+q[':question/worked-solution']

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=list(DEFAULTS) if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
