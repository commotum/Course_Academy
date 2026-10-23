#!/usr/bin/env python3
"""Polynomial powers: exact, local draft generator; no EDB operations.

Nine retained layouts plus one fresh source-replay layout. Source mathematical slots are
rendered from parameters; original prose and whitespace skeletons are retained.
Easy defaults use authored two-power grid banks; observed complete banks replay explicitly.
The unrated quartic radio has an authored moderate level and missing-solution
repair. All other levels/layouts are observed. See adjacent extraction/evidence.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
from math_format import normalize_prose, normalize_tex, checked_math_content
KP_ID=17592186096841
KP_UUID='29956ecb-a28a-5406-b8dc-9776e9a3ccee'
TITLE='Differentiating a Polynomial Raised to a Power Using the Chain Rule'
VERSION='polynomial-power-6'
ROOT=Path(__file__).resolve().parent
CAPTURE=json.loads((ROOT/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in CAPTURE['material']['kp'][':knowledge-point/questions']}
# Template identifiers denote layouts; observed profiles preserve full source banks.
TEMPLATES={
 'affine_constant_radio':('easy','radio','q-666','affine_constant'),
 'affine_variable_radio':('easy','radio','q-11410','affine_variable'),
 'affine_blank':('easy','blank','q-340690','affine_constant'),
 'quadratic_derivative':('moderate','blank','q-132974','quadratic'),
 'quadratic_slope_radio':('moderate','radio','q-48622','quadratic'),
 'quadratic_slope':('moderate','blank','q-342630','quadratic_full'),
 'affine_slope':('moderate','blank','q-342663','affine_variable'),
 'quartic_radio':('moderate','radio','q-48625','quartic'),
 'tangent_blank':('hard','blank','q-342910','affine_constant'),
 'tangent_radio':('hard','radio','q-48666','affine_constant')}
PROFILES={'observed_48622':'quadratic_slope_radio','observed_666':'affine_constant_radio','observed_11410':'affine_variable_radio',
          'observed_48625':'quartic_radio','observed_48666':'tangent_radio',
          'authored_affine_constant':'affine_constant_radio','authored_affine_variable':'affine_variable_radio',
          'authored_quartic':'quartic_radio','authored_tangent':'tangent_radio',
          'authored_quadratic_slope':'quadratic_slope_radio'}
SOURCE_CASES=[
 ('q-48622','quadratic_slope_radio',dict(a=3,b=-10,n=4,z=2),'observed_48622'),
 ('q-666','affine_constant_radio',dict(a=6,b=4,n=3),'observed_666'),
 ('q-11410','affine_variable_radio',dict(a=5,b=10,n=6),'observed_11410'),
 ('q-340690','affine_blank',dict(a=-7,b=1,n=4),None),
 ('q-132974','quadratic_derivative',dict(a=2,b=3,n=2),None),
 ('q-342630','quadratic_slope',dict(a=1,b=2,c=1,n=2,z=0),None),
 ('q-342663','affine_slope',dict(a=3,b=1,n=4,z=-1),None),
 ('q-48625','quartic_radio',dict(a=1,b=3,n=2),'observed_48625'),
 ('q-342910','tangent_blank',dict(a=-2,b=3,n=3,z=2),None),
 ('q-48666','tangent_radio',dict(a=-3,b=5,n=4,z=2),'observed_48666')]
MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$',re.S)
def tex(e): return sp.latex(e).replace(r'\left', '').replace(r'\right','')
def power(s,n): return '('+s+')' if n==1 else '('+s+')^{'+str(n)+'}'
def gp(n): return 'g' if n==1 else 'g^{'+str(n)+'}'
def block(s): return '$$\n'+s+'\n$$'
def align(lhs,rhs):
 return block(r'\begin{aligned}'+lhs+' &='+r' \\  &='.join(rhs)+r'\end{aligned}')
def slots(text,replacements):
 count=0
 def sub(m):
  nonlocal count
  i=count;count+=1
  return replacements.get(i,m.group())
 return MATH.sub(sub,text)
def signterm(v,s): return ('+' if v>=0 else '-')+(str(abs(v)) if abs(v)!=1 else '')+s

def maths(name,p):
 family=TEMPLATES[name][3]; v=sp.Symbol('t' if name=='quadratic_derivative' else 'x'); a,b,n=p['a'],p['b'],p['n']
 if family.startswith('affine'):
  inner=a*v+b
  it=(str(b)+signterm(a,str(v))) if family=='affine_constant' else tex(inner)
 elif family=='quadratic': inner=a*v**2+b;it=tex(inner)
 elif family=='quadratic_full': inner=a*v**2+b*v+p['c'];it=tex(inner)
 else: inner=a*v**4+b*v;it=tex(inner)
 di=sp.diff(inner,v); derivative=n*inner**(n-1)*di
 dt=(str(n*a)+power(it,n-1)) if family.startswith('affine') else str(n)+power(it,n-1)+'('+tex(di)+')'
 if family=='quadratic':dt=tex(n*di)+power(it,n-1)
 z=p.get('z'); y=inner.subs(v,z)**n if z is not None else None
 slope=derivative.subs(v,z) if z is not None else None
 answer=(slope*v+y-slope*z if name.startswith('tangent') else slope if z is not None else derivative)
 return v,inner,it,di,derivative,dt,y,slope,sp.expand(answer) if name.startswith('tangent') else answer

DF=r'\frac{\text{d}f}{\text{d}x}'
DG=r'\frac{\text{d}g}{\text{d}x}'
FG=r'\frac{\text{d}f}{\text{d}g}'
def solution(name,p,data):
 v,inner,it,di,d,dt,y,m,answer=data;n=p['n'];source=SOURCES[TEMPLATES[name][2]]
 if name=='quartic_radio':
  # No source solution exists. The repair uses the canonical method wording.
  text=SOURCES['q-11410'][':question/worked-solution']
 else: text=source[':question/worked-solution']
 if name=='quadratic_derivative':
  r={0:'$h(t):$',1:block('h(t)='+power(it,n)),2:block('g(t)='+it+r',\,h(g(t))=g(t)^{'+str(n)+'}.'),
     3:align("g^{′}(t)",["("+it+")^{′}="+tex(di)+r', \\ h^{′}(g(t)) = ('+gp(n)+")^{′}="+str(n)+gp(n-1)+'.']),
     4:align(r'\frac{\text{d}}{\text{d}t}['+power(it,n)+']',[r'h^{′}(t)',r'h^{′}(g(t))\cdot g^{′}(t)',str(n)+gp(n-1)+r'\cdot '+tex(di),dt+'.'])}
  return slots(text,r).replace('h(g(t))','F(g(t))').replace('h^{′}(g(t))','F^{′}(g(t))')
 ispoint='slope' in name or name.startswith('tangent'); offset=2 if ispoint else 0
 product=str(n)+gp(n-1)+r'\cdot ('+tex(di)+')'
 if name=='affine_constant_radio':product=str(n)+r'\cdot '+('('+str(p['a'])+')' if p['a']<0 else str(p['a']))+r'\cdot '+power(it,n-1)
 r={1+offset:block('f='+gp(n)+r',\,g='+it),3+offset:block(FG+'='+str(n)+gp(n-1)+','),
    4+offset:block(DG+'='+tex(di)+'.'),6+offset:align(DF,[product,dt+'.'])}
 if ispoint:
  z=p['z'];iz=inner.subs(v,z);diz=di.subs(v,z)
  substitution=dt.replace(str(v),'('+str(z)+')')
  intermediate=str(n)+power(tex(iz),n-1)+'('+tex(diz)+')'
  evaluation='['+dt+']|_{x='+str(z)+'}'
  rhs=[evaluation,substitution,intermediate,tex(m)+'.']
  if name=='quadratic_slope_radio':rhs=[evaluation,substitution,tex(m)+'.']
  if name=='tangent_blank': rhs=[evaluation,substitution,tex(m)+'.']
  if name=='tangent_radio': rhs=[substitution,tex(m)+'.']
  r[9]='$x='+str(z)+'$';r[10]=align(DF+'|_{x='+str(z)+'}',rhs)
  if name.startswith('tangent'):
   r[11]='$('+str(z)+','+tex(y)+')$';r[12]='$m='+tex(m)+'.$'
   if name=='tangent_blank': stages=[tex(m)+'(x-('+str(z)+'))',tex(m*v-m*z)+('+' if y>=0 else '')+tex(y),tex(answer)]
   else: stages=[tex(m)+'(x-('+str(z)+'))',tex(m*v-m*z),tex(answer)]
   # Retain point-slope then expansion then final RHS; both sides carry y1.
   rows=[r'y-y_1 &=m(x-x_1)', 'y-('+tex(y)+') &='+stages[0],
         ('y &='+stages[1] if name=='tangent_blank' else 'y-('+tex(y)+') &='+stages[1]),'y &='+stages[2]]
   r[13]=block(r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}')
 return slots(text,r)

def prompt(name,p,data):
 v,inner,it,di,d,dt,y,m,answer=data;n=p['n'];original=SOURCES[TEMPLATES[name][2]][':question/problem']
 if name=='quadratic_derivative':
  # Captured indentation makes the field HTML an escaped Markdown code block.
  rendered=slots(original,{0:r'$\frac{\text{d}}{\text{d}t}['+power(it,n)+r']=\,$'})
  return rendered.split('{{field-1}}')[0].rstrip()+'\n\n{{field-1}}'
 if 'slope' in name or name.startswith('tangent'):
  return slots(original,{0:'$f(x)='+power(it,n)+',$',1:'$('+str(p['z'])+','+tex(y)+')$'})
 # The quartic source already places its final period outside the math span.
 return slots(original,{1:'$f(x)='+power(it,n)+('$' if name=='quartic_radio' else '.$')})

LOW_ERRORS=('negative_outer','omit_outer','half_outer','decrement_outer')
HIGH_ERRORS=('increment_outer','increment_outer_twice','double_outer','square_outer')
def select_factor_bank(rng):
 # Assign under/over-estimation roles before coefficients and point sampling.
 # This is a whole authored profile, never the first four valid pooled errors.
 low_count=rng.randrange(5)
 return tuple(sorted(rng.sample(LOW_ERRORS,low_count)+rng.sample(HIGH_ERRORS,4-low_count)))
def factor_bank(n,recipes):
 values=dict(negative_outer=-n,omit_outer=1,half_outer=sp.Rational(n,2),
             decrement_outer=n-1,increment_outer=n+1,increment_outer_twice=n+2,
             double_outer=2*n,square_outer=n*n)
 return [values[label] for label in recipes]

def select_affine_design(rng,parameters=None):
 # Decide the answer-bearing ranks and missing response before numerical values.
 if parameters is None:
  rank=rng.randrange(3);prank=rng.randrange(2)
  missing=rng.choice([(i,j) for i in range(3) for j in range(2) if (i,j)!=(rank,prank)])
  powers=sorted(rng.sample(range(2,7),2))
  slopes=sorted(rng.sample(range(2,8),3))
 else:
  # Explicit mathematical replay: build a compatible bank around those values.
  n=parameters['n'];a=abs(parameters['a'])
  powers=sorted([n,rng.choice([m for m in range(2,7) if m!=n])]);prank=powers.index(n)
  peers=rng.sample([v for v in range(1,max(7,a+2)+1) if v!=a],2)
  slopes=sorted([a]+peers);rank=slopes.index(a)
  missing=rng.choice([(i,j) for i in range(3) for j in range(2) if (i,j)!=(rank,prank)])
 return dict(powers=powers,slopes=slopes,slope_rank=rank,power_rank=prank,missing=list(missing))

def affine_grid_bank(p,data,design):
 v,inner,it,di,d,dt,*_=data
 if set(design)!={'powers','slopes','slope_rank','power_rank','missing'}:raise ValueError('Invalid affine bank design keys')
 powers=design['powers'];slopes=design['slopes'];rank=design['slope_rank'];prank=design['power_rank'];missing=design['missing']
 if (not isinstance(powers,list) or len(powers)!=2 or any(type(x)!=int or not 2<=x<=6 for x in powers)
     or powers!=sorted(set(powers)) or not isinstance(slopes,list) or len(slopes)!=3
     or any(type(x)!=int or x<=0 or x>14 for x in slopes) or slopes!=sorted(set(slopes))
     or type(rank)!=int or rank not in range(3) or type(prank)!=int or prank not in range(2)
     or not isinstance(missing,list) or len(missing)!=2 or any(type(x)!=int for x in missing)
     or missing[0] not in range(3) or missing[1] not in range(2)):
  raise ValueError('Invalid affine bank design')
 correct=(rank,prank);missing=tuple(missing)
 if powers[prank]!=p['n'] or slopes[rank]!=abs(p['a']) or missing==correct:
  raise ValueError('Bank target must match parameters and be present')
 sgn=1 if p['a']>0 else -1
 cells=[correct]+[(i,j) for i in range(3) for j in range(2) if (i,j) not in (correct,missing)]
 return [('correct' if (i,j)==correct else f'grid_{i}_{j}',sgn*slopes[i]*powers[j]*inner**(powers[j]-1),str(sgn*slopes[i]*powers[j])+power(it,powers[j]-1)) for i,j in cells]

def quartic_coefficient_pool(a):
 target=abs(4*a);digits=len(str(target))
 return list(range(max(2,10**(digits-1)),10**digits))

def select_quartic_design(rng,parameters=None):
 # Assign correct coefficient ranks first, then compatible mathematical values.
 if parameters is None:
  rank=rng.randrange(3);outer_rank=rng.randrange(2)
  compatible=[a for a in (1,2,3) if sum(c<4*a for c in quartic_coefficient_pool(a))>=rank
              and sum(c>4*a for c in quartic_coefficient_pool(a))>=2-rank]
  a=rng.choice(compatible)
  n=rng.choice([n for n in range(2,7) if n>2 or outer_rank==0])
 else:
  a=abs(parameters['a']);n=parameters['n'];pool=quartic_coefficient_pool(a)
  rank=rng.choice([i for i in range(3) if sum(c<4*a for c in pool)>=i and sum(c>4*a for c in pool)>=2-i])
  outer_rank=rng.choice([0,1] if n>2 else [0])
 pool=quartic_coefficient_pool(a);target=4*a
 leading=sorted(rng.sample([c for c in pool if c<target],rank)+[target]+rng.sample([c for c in pool if c>target],2-rank))
 peer=rng.choice([k for k in range(2,10) if (k<n if outer_rank else k>n)])
 outer=sorted([n,peer]);missing=rng.choice([(i,j) for i in range(3) for j in range(2) if (i,j)!=(rank,outer_rank)])
 return dict(leading_coefficients=leading,outer_coefficients=outer,leading_rank=rank,outer_rank=outer_rank,missing=list(missing))

def quartic_grid_bank(p,data,design):
 v,inner,it,di,d,dt,*_=data
 if not isinstance(design,dict) or set(design)!={'leading_coefficients','outer_coefficients','leading_rank','outer_rank','missing'}:
  raise ValueError('Invalid quartic bank design keys')
 leading=design['leading_coefficients'];outer=design['outer_coefficients'];rank=design['leading_rank'];prank=design['outer_rank'];missing=design['missing']
 if (not isinstance(leading,list) or len(leading)!=3 or leading!=sorted(set(leading))
     or any(type(c)!=int or c not in quartic_coefficient_pool(p['a']) for c in leading)
     or not isinstance(outer,list) or len(outer)!=2 or outer!=sorted(set(outer))
     or any(type(k)!=int or not 2<=k<=9 for k in outer)
     or type(rank)!=int or rank not in range(3) or type(prank)!=int or prank not in range(2)
     or not isinstance(missing,list) or len(missing)!=2 or any(type(i)!=int for i in missing)
     or missing[0] not in range(3) or missing[1] not in range(2)):
  raise ValueError('Invalid quartic bank design')
 target=(rank,prank)
 if leading[rank]!=abs(4*p['a']) or outer[prank]!=p['n'] or tuple(missing)==target:
  raise ValueError('Quartic bank target must match parameters and be present')
 sign=1 if p['a']>0 else -1
 cells=[target]+[(i,j) for i in range(3) for j in range(2) if (i,j) not in (target,tuple(missing))]
 return [('correct' if (i,j)==target else f'coefficient_grid_{i}_{j}',
          outer[j]*inner**(p['n']-1)*(sign*leading[i]*v**3+p['b']),
          str(outer[j])+power(it,p['n']-1)+'('+tex(sign*leading[i]*v**3+p['b'])+')') for i,j in cells]

# Complete banks are selected before values are constructed.
def bank(name,p,profile,data,recipes=None,bank_design=None):
 v,inner,it,di,d,dt,y,m,answer=data;a,b,n=p['a'],p['b'],p['n']
 if TEMPLATES[name][1]=='blank': return [('correct',answer,dt if name in ('affine_blank','quadratic_derivative') else tex(answer))]
 factor=lambda coeff,k:('' if coeff==1 else '-' if coeff==-1 else tex(coeff))+power(it,k)
 if name.startswith('affine'):
  if profile=='observed_666':
   vals=[('correct',d,dt),('retain_x',d*v,tex(n*a)+str(v)+power(it,n-1)),
    ('divide_inner_coefficient',sp.Rational(n,a)*inner**(n-1),r'\frac{'+power(it,n-1)+'}{'+str(a//n)+'}' if a%n==0 and a//n>1 else factor(sp.Rational(n,a),n-1)),
    ('omit_inner',n*inner**(n-1),factor(n,n-1)),('increment_outer', (n+2)*a*inner**(n+1),factor((n+2)*a,n+1))]
  elif profile=='observed_11410':
   vals=[('correct',d,dt),('retain_exponent',n*a*inner**n,factor(n*a,n)),('omit_outer_multiplier',a*inner**(n-1),factor(a,n-1)),
         ('constant_as_scale',b*inner**(n-1),factor(b,n-1)),('omit_inner',n*inner**(n-1),factor(n,n-1))]
  else:
   vals=affine_grid_bank(p,data,bank_design)
 elif name=='quadratic_slope_radio' and profile=='observed_48622':
  vals=[(label,value,tex(value)) for label,value in [('correct',m),('half_slope',m/2),('eight_slope',8*m),('double_slope',2*m),('double_minus_ten',2*m-10)]]
 elif name=='quadratic_slope_radio':
  slopes=[m]+[c*di.subs(v,p['z'])*inner.subs(v,p['z'])**(n-1) for c in factor_bank(n,recipes)]
  vals=[(label,value,tex(value)) for label,value in zip(('correct',)+recipes,slopes)]
 elif name=='quartic_radio' and profile=='authored_quartic':
  vals=quartic_grid_bank(p,data,bank_design)
 elif name=='quartic_radio':
  major=4*a*v**3
  vals=[('correct',d,dt),('linear_derivative_retains_x',n*inner**(n-1)*(major+b*v),str(n)+power(it,n-1)+'('+tex(major+b*v)+')'),
        ('omit_linear_term',n*major*inner**(n-1),str(n)+'('+tex(major)+')'+power(it,n-1)),
        ('omit_linear_retain_exponent',n*major*inner**n,str(n)+'('+tex(major)+')'+power(it,n)),
        ('raise_inner_derivative',n*inner**(n-1)*di**n,str(n)+power(it,n-1)+power(tex(di),n))]
 else:
  z=p['z'];iz=inner.subs(v,z)
  slopes=[m,-m,a,n,-n] if profile=='observed_48666' else [m]+[c*a*iz**(n-1) for c in factor_bank(n,recipes)]
  labels=(['correct','wrong_sign','use_inner_coefficient_as_slope','use_outer_exponent_as_slope','negate_outer_exponent_as_slope']
          if profile=='observed_48666' else ['correct']+list(recipes))
  vals=[(label,sp.expand(s*v+y-s*z),'y='+tex(sp.expand(s*v+y-s*z))) for label,s in zip(labels,slopes)]
 if any(sp.expand(e1-e2)==0 for i,(_,e1,_) in enumerate(vals) for _,e2,_ in vals[i+1:]):raise ValueError('Whole bank has equivalent options')
 return vals

def validate_parameters(name,p):
 required={'a','b','n'}|({'c'} if name=='quadratic_slope' else set())|({'z'} if 'slope' in name or name.startswith('tangent') else set())
 if set(p)!=required or any(type(x)!=int for x in p.values()):raise ValueError('Exact integer parameters with template keys required')
 if not 2<=p['n']<=6 or not p['a'] or not p['b']:raise ValueError('Need n=2..6, a,b nonzero')
 if any(abs(x)>12 for k,x in p.items() if k!='n'):raise ValueError('Coefficients/point bounds ±12')

def sample(name,rng):
 a=rng.choice([-7,-6,-5,-4,-3,-2,2,3,4,5,6,7]);b=rng.choice([x for x in range(-6,7) if x]);n=rng.randint(2,6)
 if TEMPLATES[name][0]=='easy':b=rng.choice([x for x in range(-10,11) if x])
 if name=='quartic_radio':a=rng.choice([-3,-2,-1,1,2,3]);n=2
 if name in ('quadratic_derivative','quadratic_slope'):a=rng.choice([-3,-2,-1,1,2,3]);n=rng.choice([2,3])
 if 'slope' in name or name.startswith('tangent'):
  a=rng.choice([-3,-2,-1,1,2,3])
  if name.startswith('tangent'):n=rng.choice([3,4])
  if name=='affine_slope':n=4
  if name=='quadratic_slope_radio':n=4
 p=dict(a=a,b=b,n=n)
 if name=='quadratic_slope':p['c']=rng.choice([-3,-2,-1,1,2,3])
 if 'slope' in name or name.startswith('tangent'):p['z']=rng.randint(-2,2)
 return p

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,bank_design=None):
 if type(seed)!=int:raise ValueError('Integer seed required')
 if profile is not None:
  if profile not in PROFILES:raise ValueError('Unknown profile')
  if template and template!=PROFILES[profile]:raise ValueError('Profile belongs to another template')
  template=PROFILES[profile]
 eligible=[k for k,s in TEMPLATES.items() if s[0]==level and (field_type is None or field_type==s[1])]
 if not eligible or template is not None and template not in eligible:raise ValueError('Unsupported level/template/field')
 rng=random.Random(seed);name=template or rng.choice(eligible);lev,kind,sid,fam=TEMPLATES[name]
 if kind=='radio':profile=profile or {'quadratic_slope_radio':'authored_quadratic_slope','affine_constant_radio':'authored_affine_constant','affine_variable_radio':'authored_affine_variable','quartic_radio':'authored_quartic','tangent_radio':'authored_tangent'}[name]
 elif profile is not None:raise ValueError('Blank has no bank')
 recipes=select_factor_bank(rng) if profile in ('authored_tangent','authored_quadratic_slope') else None
 affine_authored=profile in ('authored_affine_constant','authored_affine_variable')
 quartic_authored=profile=='authored_quartic'
 if bank_design is not None and not (affine_authored or quartic_authored):raise ValueError('Bank design only applies to authored coefficient grids')
 if parameters is not None:validate_parameters(name,parameters)
 design=(dict(bank_design) if bank_design is not None else select_affine_design(rng,parameters) if affine_authored
         else select_quartic_design(rng,parameters) if quartic_authored else None)
 for attempt in range(128):
  p=dict(parameters) if parameters is not None else sample(name,rng)
  if affine_authored and parameters is None:
   p['n']=design['powers'][design['power_rank']]
   p['a']=(1 if p['a']>0 else -1)*design['slopes'][design['slope_rank']]
  if quartic_authored and parameters is None:
   p['n']=design['outer_coefficients'][design['outer_rank']]
   p['a']=(1 if p['a']>0 else -1)*design['leading_coefficients'][design['leading_rank']]//4
  validate_parameters(name,p);data=maths(name,p)
  if parameters is None and ('slope' in name or name.startswith('tangent')):
   v,inner,_,di=data[:4];z=p['z']
   if not 1<=abs(inner.subs(v,z))<=3 or di.subs(v,z)==0:continue
  try:vals=bank(name,p,profile,data,recipes,design)
  except ValueError:
   if bank_design is not None:raise
   # Explicit mathematical parameters may need a different compatible bank.
   # Normal generation retains its chosen role design and samples compatible values.
   if parameters is not None and affine_authored:design=select_affine_design(rng,parameters)
   elif parameters is not None:raise
   continue
  break
 else:raise ValueError('Bounded sampling failed')
 problem=normalize_prose(prompt(name,p,data));worked=normalize_prose(solution(name,p,data))
 vals=[(label,expr,normalize_tex(value)) for label,expr,value in vals]
 key='selection' if kind=='radio' else 'field-1'
 content={'version':VERSION,'template':name,'parameters':p,'profile':profile,'domain':'real','problem':problem,'solution':worked,'bank':sorted((label,value) for label,e,value in vals)}
 fingerprint=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
 qid=uuid.uuid5(uuid.UUID(KP_UUID),fingerprint);fid=uuid.uuid5(qid,key)
 answers=[{':answer/id':str(uuid.uuid5(fid,label+':'+value)),':answer/type':':answer.type/math',':answer/value':value} for label,e,value in vals]
 correct=answers[0][':answer/id']
 # Canonical order depends on visible values, never their correct/incorrect roles.
 if affine_authored or quartic_authored:answers.sort(key=lambda a:a[':answer/value'])
 rng.shuffle(answers)
 question={':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':worked,
 ':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'bank_origin':'observed' if profile and profile.startswith('observed') else 'authored' if profile else 'observed', 'authored_level':sid=='q-48625','source_ids':[sid],'source_analysis':{k:CAPTURE[k] for k in ['database','basis','lineage']},'parameter_fingerprint':hashlib.sha256(json.dumps({'inner':sp.srepr(data[1]),'n':p['n'],'z':p.get('z'),'response':'tangent' if name.startswith('tangent') else 'slope' if 'slope' in name else 'derivative'},sort_keys=True).encode()).hexdigest(),'content_fingerprint':fingerprint,'domain':'real','plot_rating':'none','sympy_version':sp.__version__,'bank_design':design,'sampling_attempts':attempt+1,'recipes':[label for label,e,value in vals]}}
# EASY — source affine layouts with authored radio banks and observed blank.
# One integer outer power and a constant inner derivative; coefficient/sign peers.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None,bank_design=None):return generate('easy',seed,template,field_type,parameters,profile,bank_design)
# MODERATE — observed quadratic derivative and affine/quadratic slope blanks.
# The unrated quartic radio receives an explicitly authored moderate assignment.
# Point peers require a small nonzero inner value and inner derivative.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None,bank_design=None):return generate('moderate',seed,template,field_type,parameters,profile,bank_design)
# HARD — observed affine-power tangent equation: full radio equation or RHS blank.
# Powers3/4 and small point values retain source substitution/point-slope workload.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return '\n\n'.join(['**Difficulty:** '+q[':question/difficulty'].split('/')[-1]+'. **Template:** `'+r['generation']['template']+'`. **Profile:** `'+str(r['generation']['bank_profile'])+'`.',q[':question/problem'],'\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices']),q[':question/worked-solution']])
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='easy');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='json');ap.add_argument('--template',choices=TEMPLATES);ap.add_argument('--profile',choices=PROFILES);ap.add_argument('--field-type',choices=['radio','blank']);a=ap.parse_args()
 if a.count<1:ap.error('Positive count required')
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 try:r=[generate(l,a.seed+i,a.template,a.field_type,profile=a.profile) for l in levels for i in range(a.count)]
 except ValueError as e:ap.error(str(e))
 print(json.dumps(r,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(x) for x in r))
if __name__=='__main__':main()
