#!/usr/bin/env python3
"""Direct 3D vector-field line integrals. Local step-7 draft; never uses EDB.

Frozen source: supplied math basis 2853. Eight observed families retain complete
banks with corrected replay solutions. Scalar-field lifts are parameterized by
linearity, without inventing intentions for opaque wrong values.
Normal generators choose complete operation banks before sampling parameters,
reject whole collisions, and compute F(r(t)).r'(t) directly. See instructional-account.md.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
from math_format import normalize_prose, normalize_tex, checked_math_content

ROOT=Path(__file__).resolve().parent
CAPTURE=json.loads((ROOT/'source.json').read_text())
KP=CAPTURE['material']['kp']; KP_ID=17592186133894
VERSION='space-vector-direct-4'
NS=uuid.UUID(KP[':knowledge-point/id'])
x,y,z,t=s.symbols('x y z t',real=True)
OBSERVED={
 'product':17592186134088, 'helix_root':17592186134089,
 'mixed_polynomial':17592186259708, 'trig_cancel':17592186259710,
 'exp_cancel_xy':17592186259714, 'exp_cancel_yz':17592186259717,
 'quotient_exp':17592186284546, 'radical_power':17592186284547,
}
OLDS={q[':db/id']:q for q in KP[':knowledge-point/questions']}
TEMPLATES={**dict.fromkeys(OBSERVED,'hard'),'affine_linear':'easy','permuted_power':'moderate'}
SOURCE_PARAMETERS={
 'product':dict(A=1,B=1,C=1,a=0,b=1),
 'helix_root':dict(A=1,B=1,C=2,a=0,b='pi'),
 'mixed_polynomial':dict(A=1,B=3,C=2,a=0,b=1),
 'trig_cancel':dict(A=1,B=1,C=1,a=0,b='pi/6'),
 'exp_cancel_xy':dict(A=1,B=1,C=1,k=1,l=2,a=0,b=1),
 'exp_cancel_yz':dict(A=2,B=3,C=1,k=1,l=2,a=0,b=1),
 'quotient_exp':dict(A=1,B=1,C=1,k=1,l=1,a=0,b=1),
 'radical_power':dict(A=1,B=1,C=1,a=1,b=2),
}

def tex(v):
 v=s.sympify(v)
 # Retain familiar course exponentials; eager CAS scalar simplification may
 # otherwise turn historical exponential arithmetic into hyperbolic notation.
 hyper={q:q.rewrite(s.exp) for q in s.preorder_traversal(v) if q.func in (s.sinh,s.cosh)}
 if hyper:v=s.expand(v.xreplace(hyper))
 return s.latex(v,fold_short_frac=False).replace(r'\log',r'\ln')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(NS,v))
def equal(a,b):
 delta=s.sympify(a)-s.sympify(b)
 hyper={q:q.rewrite(s.exp) for q in s.preorder_traversal(delta) if q.func in (s.sinh,s.cosh)}
 delta=s.expand(delta.xreplace(hyper))
 if delta==0:return True
 # Every exponential bank uses integer rates/endpoints. A nonzero rational
 # Laurent polynomial in e cannot vanish (e is transcendental), so avoid slow
 # hyperbolic/trigonometric heuristics for these complete-bank comparisons.
 U=s.Symbol('e_polynomial');replacements={q:U**q.args[0] for q in s.preorder_traversal(delta) if q.func==s.exp and q.args[0].is_Integer}
 replacements[s.E]=U
 try:
  numerator=s.fraction(s.cancel(delta.xreplace(replacements)))[0]
  polynomial=s.Poly(numerator,U,domain=s.QQ)
  return polynomial.is_zero
 except (s.PolynomialError,s.CoercionFailed):return s.simplify(s.trigsimp(delta))==0
def vector(v):
 # Complete grouped components prevent numeric concatenation and signed +-.
 return '+'.join(r'\left('+tex(q)+r'\right)\,'+b for q,b in zip(v,'ijk'))
def summands(expr):return list(s.Add.make_args(s.expand(expr)))
def uneval_sum(values):return '+'.join(r'\left('+v+r'\right)' for v in values)
def block(body):return '$$\n'+body+'\n$$'
def aligned(lhs,rows):return block(r'\begin{aligned}'+lhs+' & ='+r' \\ & ='.join(rows)+r'\end{aligned}')

_MATH_CACHE={}
def mathematics(name,p):
 key=(name,tuple(sorted((k,str(v)) for k,v in p.items())))
 if key not in _MATH_CACHE:_MATH_CACHE[key]=_mathematics(name,p)
 return _MATH_CACHE[key]
def _mathematics(name,p):
 A,B,C=[s.sympify(p[q]) for q in ('A','B','C')]
 if name=='affine_linear':
  coords=(x,y,z);perm=p.get('perm','xzy');F=tuple(c*coords['xyz'.index(q)] for c,q in zip((A,B,C),perm));r=tuple(s.sympify(p['v'+q])*t+s.sympify(p['h'+q]) for q in 'xyz')
 elif name=='permuted_power':
  coords=(x,y,z);perm=p.get('perm','yzx');F=tuple(c*coords['xyz'.index(q)] for c,q in zip((A,B,C),perm));r=(t,t**2,t**3)
 elif name=='constant_affine':
  F=(A,B,C); r=tuple(s.sympify(p['v'+q])*t+s.sympify(p['h'+q]) for q in 'xyz')
 elif name=='diagonal_power':F=(A*x,B*y,C*z);r=(t,t**2,t**3)
 elif name=='product':F=(y*z,x*z,x*y);r=(A*t,B*t**2,C*t**3)
 elif name=='mixed_polynomial':F=(x+z,z-y,z**2);r=(A*t**2,B*t**2,C*t)
 elif name=='trig_cancel':F=(x,z,y);r=(-A*s.sin(t),B*s.sec(t),C*s.cos(t))
 elif name=='exp_cancel_xy':
  k,l=map(s.sympify,(p['k'],p['l'])); F=(y,x,z);r=(A*s.exp(-k*t),B*s.exp(s.sympify(p.get('j',k))*t),C*s.exp(l*t))
 elif name=='exp_cancel_yz':
  k,l=map(s.sympify,(p['k'],p['l']));F=(x,z,y);r=(A*s.exp(k*t),B*s.exp(l*t),C*s.exp(s.sympify(p.get('j',-l))*t))
 elif name=='quotient_exp':
  k,l=map(s.sympify,(p['k'],p['l']));F=(z/x,z/y,s.Integer(1));r=(A*s.exp(k*t),B*s.exp(l*t),C*t)
 elif name=='radical_power':F=(s.sqrt(x),s.sqrt(y),z);r=(A*t,B*t,C*t**2)
 elif name=='helix_root':F=(x,y,z);r=(A*s.cos(t),A*s.sin(t),C*s.sqrt(t))
 else:raise ValueError('Unknown template '+name)
 F=tuple(s.sympify(p.get('lift',1))*v for v in F)
 a,b=map(s.sympify,(p['a'],p['b']))
 f=tuple(s.simplify(q.subs(dict(zip((x,y,z),r)),simultaneous=True)) for q in F)
 d=tuple(s.diff(q,t) for q in r)
 products=tuple(s.expand(q*v) for q,v in zip(f,d))
 I=s.simplify(s.trigsimp(sum(products)))
 anti=s.integrate(I,t);q=s.simplify(anti.subs(t,b)-anti.subs(t,a))
 return dict(F=F,r=r,f=f,d=d,products=products,I=I,anti=anti,q=q,a=a,b=b)

# Complete authored bank profiles. Profile selection happens before parameters.
# Each entry is an operation on actual field pullbacks/derivatives/endpoints.
BANKS={
 'affine_linear':('correct','omit_component','sign_error','differential_factor','endpoint_error'),
 'permuted_power':('correct','omit_component','sign_error','differential_factor','endpoint_error'),
 'constant_affine':('correct','reverse_orientation','omit_x','omit_y','omit_z'),
 'diagonal_power':('correct','reverse_orientation','omit_x','omit_y','omit_z'),
 'product':('correct','omit_x','omit_y','omit_z','do_not_differentiate_curve'),
 'mixed_polynomial':('correct','omit_x','omit_y','omit_z','do_not_differentiate_curve'),
 'exp_cancel_xy':('correct','omit_x','omit_y','omit_z','do_not_differentiate_curve'),
 'exp_cancel_yz':('correct','omit_x','omit_y','omit_z','do_not_differentiate_curve'),
 'trig_cancel':('correct','reverse_orientation','omit_half_in_sin_squared_primitive','drop_sine_square_and_half_in_primitive','omit_lower_endpoint_and_half_of_cosine_primitive'),
 'radical_power':('correct','omit_both_radicals','omit_z','omit_factor_two_in_z_derivative','reverse_orientation'),
 'quotient_exp':('correct','omit_both_quotient_components','omit_first_quotient_component','fail_cancel_first_exponential','fail_cancel_both_exponentials'),
 'helix_root':('correct','omit_z','omit_half_in_sqrt_derivative','replace_sqrt_denominator_by_t','move_sqrt_denominator_to_numerator'),
}
def integrate_on(expr,m):
 anti=s.integrate(s.simplify(expr),t)
 return s.simplify(anti.subs(t,m['b'])-anti.subs(t,m['a']))
def legacy_operation_bank(name,p,m):
 Q=m['q'];P=m['products'];a,b=m['a'],m['b'];A,C=map(s.sympify,(p['A'],p['C']))
 if name in ('constant_affine','diagonal_power'):vals=[Q,-Q,*[integrate_on(sum(P)-v,m) for v in P]]
 elif name in ('product','mixed_polynomial','exp_cancel_xy','exp_cancel_yz'):
  vals=[Q,*[integrate_on(sum(P)-v,m) for v in P],integrate_on(sum(m['f']),m)]
 elif name=='trig_cancel':vals=[Q,-Q,2*Q,A*A*(s.sin(b)-s.sin(a)),-A*A*s.cos(2*b)/2]
 elif name=='radical_power':
  R=integrate_on(P[0]+P[1],m);Z=integrate_on(P[2],m);vals=[Q,Z,R,R+Z/2,-Q]
 elif name=='quotient_exp':
  k,l=map(s.sympify,(p['k'],p['l']));vals=[Q,C*(b-a),integrate_on(P[1]+P[2],m),integrate_on(C*k*t*s.exp(-k*t)+P[1]+C,m),integrate_on(C*k*t*s.exp(-k*t)+C*l*t*s.exp(-l*t)+C,m)]
 elif name=='helix_root':vals=[Q,0,2*Q,C*C*(s.sqrt(b)-s.sqrt(a)),C*C*(b*b-a*a)/4]
 vals=list(map(s.simplify,vals))
 if any(equal(v,w) for idx,v in enumerate(vals) for w in vals[:idx]):raise ValueError('Whole-bank collision')
 if any(v.has(s.nan,s.zoo,s.oo,-s.oo) or v.is_real is False for v in vals):raise ValueError('Invalid whole bank')
 return vals

def operation_bank(name,p,m,rng):
 # Generate recognizable mistakes from this exact instance, never numerical filler.
 Q=m['q'];P=m['products']; contributions=[integrate_on(q,m) for q in P]
 candidates=[]
 for i,c in enumerate(contributions):
  for factor,label in [(0,'omit'),(-1,'sign'),(2,'double'),(s.Rational(1,2),'half')]:
   candidates.append((f'{label}_{i}',s.simplify(Q+(factor-1)*c)))
  candidates.append((f'omit_derivative_{i}',integrate_on(sum(P)-P[i]+m['f'][i],m)))
 if m['a']!=0:
  candidates.append(('omit_lower_endpoint',s.simplify(m['anti'].subs(t,m['b']))))
  candidates.append(('add_lower_endpoint',s.simplify(m['anti'].subs(t,m['b'])+m['anti'].subs(t,m['a']))))
 candidates.append(('reverse_orientation',-Q))
 # These families have distinctive primitive mistakes worth retaining.
 if name=='trig_cancel':
  candidates.extend([('omit_primitive_half',2*Q),('extra_primitive_half',Q/2),('integrate_as_sin',p['A']**2*(s.sin(m['b'])-s.sin(m['a'])))])
 if name=='helix_root':candidates.extend([('sqrt_derivative_as_t',p['C']**2*(s.sqrt(m['b'])-s.sqrt(m['a']))),('move_sqrt_to_numerator',p['C']**2*(m['b']**2-m['a']**2)/4)])
 if name=='quotient_exp':
  k,l=map(s.sympify,(p['k'],p['l']));C=s.sympify(p['C'])
  candidates.extend([('fail_cancel_first_exp',integrate_on(C*k*t*s.exp(-k*t)+P[1]+C,m)),('fail_cancel_both_exp',integrate_on(C*k*t*s.exp(-k*t)+C*l*t*s.exp(-l*t)+C,m))])
 # Skip impossible/duplicate mistakes; a profile consists of four actual errors.
 unique=[]
 for label,val in candidates:
  if val.has(s.nan,s.zoo,s.oo,-s.oo) or val.is_real is False or equal(val,Q):continue
  if not any(equal(val,v) for _,v in unique):unique.append((label,val))
 if len(unique)<4:raise ValueError('Insufficient distinct plausible errors')
 def signature(v):
  return (bool(v.has(s.exp,s.E)),bool(v.has(s.log)),bool(v.has(s.sin,s.cos,s.tan,s.sec)),bool(any(q.is_Pow and q.exp.is_Rational and not q.exp.is_Integer for q in s.preorder_traversal(v))),bool(v.has(s.pi)),bool(v.is_Rational))
 # Shuffle complete banks, retaining at least two options of the key's shape/sign.
 # This rejects unique-format and unique-sign giveaways without adding fake errors.
 for _ in range(160):
  picked=rng.sample(unique,4);vals=[Q]+[v for _,v in picked]
  if sum(signature(v)==signature(Q) for v in vals)<2:continue
  sign=lambda v: 1 if float(s.N(v))>0 else -1 if float(s.N(v))<0 else 0
  if Q!=0 and sum(sign(v)==sign(Q) for v in vals)<2:continue
  opposite_pairs=[(i,j) for i,v in enumerate(vals) for j,w in enumerate(vals[:i]) if equal(v,-w)]
  if len(opposite_pairs)==1 and 0 in opposite_pairs[0]:continue
  pbank=[label for label,_ in picked]
  return vals,pbank
 raise ValueError('No complete bank without a shape/sign giveaway')

def bounds(name,p,level):
 expected=set(SOURCE_PARAMETERS.get(name,dict(A=1,B=1,C=1,a=0,b=1)))
 if name in ('affine_linear','permuted_power'):expected.add('perm')
 if name in ('exp_cancel_xy','exp_cancel_yz') and 'j' in p:expected.add('j')
 if 'perm' in p and sorted(p['perm'])!=list('xyz'):raise ValueError('Coordinate permutation required')
 if name in ('constant_affine','affine_linear'):expected|={'vx','vy','vz','hx','hy','hz'}
 if set(p)!=expected:raise ValueError('Exact parameter keys required: '+str(sorted(expected)))
 for key in ('A','B','C'):
  v=s.sympify(p[key]);limit=5 if level=='easy' else 4 if level=='moderate' else 3
  if not v.is_Integer or not 1<=abs(v)<=limit:raise ValueError('Coefficient bound')
 if name in ('radical_power','helix_root') and any(s.sympify(p[q])<=0 for q in ('A','B','C')):raise ValueError('Positive root scales required')
 a,b=map(s.sympify,(p['a'],p['b']))
 if not a<b:raise ValueError('Increasing parameter interval required')
 if name=='trig_cancel':
  if a!=0 or b not in (s.pi/6,s.pi/4,s.pi/3):raise ValueError('Familiar acute trig bound required')
 elif name=='helix_root':
  if s.sympify(p['B'])!=s.sympify(p['A']):raise ValueError('Root helix requires equal circular scales')
  if a not in (1,2) or b not in (s.pi,2*s.pi) or not a<b:raise ValueError('Smooth root helix interval required')
 elif name=='radical_power':
  if not a.is_Integer or not b.is_Integer or not 0<=a<b<=2:raise ValueError('Small nonnegative radical endpoints required')
 else:
  if not a.is_Integer or not b.is_Integer or not 0<=a<b<=2:raise ValueError('Small integer endpoint bound')
 if 'j' in p and p['j'] not in (-2,-1,1,2):raise ValueError('Small signed exponential rate')
 for key in ('k','l'):
  if key in p and s.sympify(p[key]) not in (1,2,3):raise ValueError('Familiar exponential rates')
 if name in ('constant_affine','affine_linear'):
  for q in 'xyz':
   if p['v'+q] not in (-3,-2,-1,1,2,3) or p['h'+q] not in range(-3,4):raise ValueError('Affine workload bound')

def sample(name,rng):
 scales=[1,2,3] if name in ('radical_power','helix_root') else [-3,-2,-1,1,2,3]
 a,b=rng.choice([(0,1),(0,2),(1,2)])
 p=dict(A=rng.choice(scales),B=rng.choice(scales),C=rng.choice(scales),a=a,b=b)
 if name in ('constant_affine','affine_linear'):p.update({key+r:rng.choice([-3,-2,-1,1,2,3]) if key=='v' else rng.randint(-3,3) for key in ('v','h') for r in 'xyz'})
 elif name=='trig_cancel':p.update(a=0,b=rng.choice(['pi/6','pi/4','pi/3']))
 elif name=='helix_root':p.update(a=rng.choice([1,2]),b=rng.choice(['pi','2*pi']));p['B']=p['A']
 elif name=='radical_power':
  a,b=rng.choice([(0,1),(0,2),(1,2)]);p.update(a=a,b=b,C=rng.choice([1,2]))
 elif name in ('exp_cancel_xy','exp_cancel_yz','quotient_exp'):p.update(k=rng.randint(1,3),l=rng.randint(1,3))
 if name in ('affine_linear','permuted_power'):p['perm']=rng.choice(['xyz','xzy','yxz','yzx','zxy','zyx'])
 if name in ('exp_cancel_xy','exp_cancel_yz'):
  p.update(k=rng.choice([1,2]),l=rng.choice([1,2]))
  p['j']=rng.choice([p['k'] if name=='exp_cancel_xy' else -p['l'],rng.choice([-2,-1,1,2])])
 if name=='affine_linear':
  p.update(A=rng.choice([-2,-1,1,2]),B=rng.choice([-2,-1,1,2]),C=rng.choice([-2,-1,1,2]),a=0,b=1)
  for q in 'xyz':p['v'+q]=rng.choice([-2,-1,1,2]);p['h'+q]=rng.choice([-1,0,1])
 if name=='permuted_power':p.update(A=rng.choice([-2,-1,1,2]),B=rng.choice([-2,-1,1,2]),C=rng.choice([-2,-1,1,2]),a=0,b=1)
 return p

def substitution_tex(expr,r):
 # Replace complete symbol atoms, including product factors and sqrt arguments.
 # Held symbols are outside TeX until their mathematical arguments are replaced.
 rendered=tex(expr)
 return re.sub(r'(?<![A-Za-z\\])([xyz])(?![A-Za-z])',lambda m:r'\left('+tex(r['xyz'.index(m[1])])+r'\right)',rendered)

def wrapped_sum(terms, budget=64):
 # Explicit continuation rows keep each operation visible in the actual player.
 rows=[];current=''
 for term in terms:
  addition=('+' if current else '')+term
  if current and len(current+addition)>budget:
   rows.append(current);current=r'{}+'+term
  else:current+=addition
 if current:rows.append(current)
 return r' \\ &\quad '.join(rows)

def vector_terms(values):
 result=[]
 for value,basis in zip(values,'ijk'):
  value=s.sympify(value)
  if value==1:part=''
  elif value==-1:part='-'
  elif value.is_Add:part=r'\left('+tex(value)+r'\right)'
  else:part=tex(value)
  result.append(part+r'\,'+basis)
 return result

def normal_text(name,p,m):
 F,r,f,d=m['F'],m['r'],m['f'],m['d'];a,b=m['a'],m['b']
 prompt=r'Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)='+vector(F)+r'$ and $C$ is the path $r(t)='+vector(r)+r'$ for $t\in ['+tex(a)+','+tex(b)+r']$.'
 formal='+'.join(r'\frac{\mathrm{d}'+q+r'}{\mathrm{d}t}\,'+basis for q,basis in zip('xyz','ijk'))
 operators=[r'\frac{\mathrm{d}}{\mathrm{d}t}\left('+tex(v)+r'\right)\,'+basis for v,basis in zip(r,'ijk')]
 subvec=[r'\left('+substitution_tex(v,r)+r'\right)\,'+basis for v,basis in zip(F,'ijk')]
 products=[r'\left('+tex(q)+r'\right)\left('+tex(v)+r'\right)' for q,v in zip(f,d)]
 distributed=[r'\left('+tex(v)+r'\right)' for product in m['products'] for v in summands(product)]
 anti=m['anti']
 def at(endpoint):return re.sub(r'(?<![A-Za-z\\])t(?![A-Za-z])',lambda _:r'\left('+tex(endpoint)+r'\right)',tex(anti))
 endpoint_row=wrapped_sum([r'\left('+at(b)+r'\right)',r'\left(-\left('+at(a)+r'\right)\right)'])
 evaluated=wrapped_sum([r'\left('+tex(anti.subs(t,b))+r'\right)',r'\left('+tex(-anti.subs(t,a))+r'\right)'])
 inthead=r'\int_{'+tex(a)+'}^{'+tex(b)+'}'
 rows=[inthead+r'F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t',inthead+r'\left('+tex(m['I'])+r'\right)\,\mathrm{d}t',r'\left['+tex(anti)+r'\right]_{'+tex(a)+'}^{'+tex(b)+'}',endpoint_row,evaluated,tex(m['q'])]
 solution='We will use the formula\n\n'+block(r'\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.')
 solution+='\n\nAlong the curve $C,$ we have \n\n'+block(r',\qquad '.join(q+'='+tex(v) for q,v in zip('xyz',r))+'.')
 solution+='\n\nTherefore,\n\n'+aligned('F(r(t))',[wrapped_sum(vector_terms(F)),wrapped_sum(subvec),wrapped_sum(vector_terms(f))])
 solution+='\n\nComputing $r^{\\prime}(t),$ we get \n\n'+aligned(r'r^{\prime}(t)',[formal,wrapped_sum(operators),wrapped_sum(vector_terms(d))])
 solution+='\n\nTherefore,\n\n'+aligned(r'F(r(t))\cdot r^{\prime}(t)',[wrapped_sum(products),wrapped_sum(distributed),tex(m['I'])])
 solution+='\n\nFinally, we evaluate the integral as follows:\n\n'+aligned(r'\int_C F\cdot\mathrm{d}r',rows)
 return prompt,solution

# Immutable source values: these reproduce whole source banks, not inferred errors.
SOURCE_VALUES={
 'product':[0,1,s.Rational(1,4),s.Rational(1,2),s.Rational(1,3)],
 'helix_root':[4*s.pi,s.pi/2,s.pi**2,s.pi,2*s.pi],
 'mixed_polynomial':[16,6,4,8,5],
 'trig_cancel':[s.Rational(1,3),s.Rational(1,8),s.Rational(1,9),s.Rational(1,4),s.Rational(1,2)],
 'exp_cancel_xy':[(s.E-1)/4,(s.exp(4)-1)/2,(s.exp(2)-1)/4,(s.exp(4)-1)/4,(s.exp(2)-1)/2],
 'exp_cancel_yz':[4*s.exp(2)-1,4*s.exp(4)-4,2*s.exp(2)-1,4*s.exp(2)-2,2*s.exp(2)-2],
 'quotient_exp':[1,2+s.E,2,1+s.E,2+s.exp(2)],
 'radical_power':[(a*s.sqrt(2)+b)/6 for a,b in [(7,32),(5,31),(8,47),(16,37),(10,45)]],
}

def clean_source(text):
 return normalize_prose(text.replace('⁡','').replace('′',r"\prime").replace('π',r'\pi ').replace('∈',r'\in '))

def replay_text(name,c,m):
 old=OLDS[OBSERVED[name]]
 prompt,solution=normal_text(name,{**SOURCE_PARAMETERS[name],'lift':c},m)
 if c==1:prompt=clean_source(old[':question/problem'])
 if name=='helix_root':solution='At $t=0$, the given parameterization has an unbounded derivative. Interpret the integral as the limit from $t>0$; the simplified integrand extends continuously to zero.\n\n'+solution
 return prompt,solution

def make_record(level,name,p,profile,seed,prompt,solution,values,correct_index):
 old=OLDS[OBSERVED[name]] if name in OBSERVED else {':question/math-academy-id':'e-9534'};m=mathematics(name,p)
 prompt=normalize_prose(prompt);solution=normalize_prose(solution)
 values=[normalize_tex(v) for v in values]
 task={'field':[s.srepr(v) for v in m['F']], 'curve':[s.srepr(v) for v in m['r']], 'bounds':[s.srepr(m[q]) for q in ('a','b')], 'requested':'direct_scalar_integral'}
 fingerprint=digest(task)
 observed=profile.startswith('observed:')
 original_difficulty=old.get(':question/difficulty',{}).get(':db/ident')
 difficulty=original_difficulty if observed else ':question.difficulty/'+level
 present={'version':VERSION,'difficulty':difficulty,'prompt':prompt,'solution':solution,'bank':sorted(values),'correct_value':values[correct_index]}
 cid=digest(present);qid=uid('question/'+cid);fid=uid('field/'+cid+'/selection')
 answers=[{':answer/id':uid('answer/'+fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct_index][':answer/id']]}
 random.Random(seed).shuffle(answers)
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[f]}
 if difficulty:q[':question/difficulty']=difficulty
 meta={'version':VERSION,'template':name,'bank_profile':profile,'seed':seed,'parameters':p,'mathematical_fingerprint':fingerprint,'content_identity':cid,'evidence_only':False,'eligible_for_learning':True,'recipes':list(BANKS[name]) if not observed else ['lift * source choice '+str(i) for i in range(5)],'provenance':{k:CAPTURE[k] for k in ('database','basis','lineage')},'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'plot_rating':'none','source_id':old[':question/math-academy-id'],'original_difficulty':original_difficulty,'source_missing_key':name=='helix_root'}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':meta}

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unsupported difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Observed layout is radio')
 rng=random.Random(seed)
 # Select a complete profile before its parameters. Explicit parameter calls
 # retain the method-profile contract; explicit observed replay keeps lift=1.
 if profile is None and parameters is None:
  names=[n for n,v in TEMPLATES.items() if v==level]
  name=template or rng.choice(names)
  if name not in names:raise ValueError('Template is outside difficulty')
  template=name
  profile='method:'+name
 if profile and profile.startswith('observed:'):
  name=profile.split(':',1)[1]
  if name not in OBSERVED or template not in (None,name):raise ValueError('Profile/template mismatch')
  lift=dict(lift=1) if parameters is None else dict(parameters)
  if set(lift)!={'lift'} or lift['lift'] not in (-3,-2,-1,1,2,3):raise ValueError('Historical linear-lift domain')
  c=lift['lift'];p={**SOURCE_PARAMETERS[name],'lift':c};m=mathematics(name,p)
  values=[c*v for v in SOURCE_VALUES[name]]
  ci=next(i for i,v in enumerate(values) if equal(v,m['q']))
  prompt,solution=replay_text(name,c,m)
  old=OLDS[OBSERVED[name]]
  rendered=[a[':answer/value'].replace('π',r'\pi ') for a in old[':question/answer-fields'][0][':answer-field/choices']] if c==1 else [tex(v) for v in values]
  return make_record(level,name,p,profile,seed,prompt,solution,rendered,ci)
 names=[n for n,v in TEMPLATES.items() if v==level]
 name=template or rng.choice(names)
 if name not in names:raise ValueError('Template is outside difficulty')
 # Each family has an observed bank and a separately labeled authored bank.
 profile=profile or 'method:'+name
 if profile!='method:'+name:raise ValueError('Unknown complete bank')
 for attempt in range(400):
  p=dict(parameters) if parameters is not None else sample(name,rng)
  bounds(name,p,level);m=mathematics(name,p)
  try:values,recipes=operation_bank(name,p,m,rng)
  except ValueError:
   if parameters is not None:raise
   continue
  prompt,solution=normal_text(name,p,m)
  rec=make_record(level,name,p,profile,seed,prompt,solution,[tex(v) for v in values],0)
  rec['generation']['recipes']=['correct']+recipes
  rec['generation']['sampling_attempts']=attempt+1
  rec['generation']['correct_numerical_rank']=sorted(float(s.N(v)) for v in values).index(float(s.N(values[0])))
  return rec
 raise ValueError('No eligible whole instance after bounded sampling')

# EASY: signed/permuted linear field on an affine spatial path; linear primitive.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: signed/permuted linear field, t/t²/t³; power primitives.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: source-shaped products, sums, cancellation, exponentials, quotients, roots.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def markdown(rec):
 q=rec['question'];g=rec['generation'];f=q[':question/answer-fields'][0]
 lines=[f"### {g['template']} — {'ORIGINAL EVIDENCE (INELIGIBLE)' if g['evidence_only'] else 'GENERATED VARIANT'}",q[':question/problem']]
 lines+=['- $'+a[':answer/value']+'$'+(' **correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else '') for a in f[':answer-field/choices']]
 lines+=[q.get(':question/worked-solution','[No original worked solution; no correct designation; unrated.]')]
 return '\n\n'.join(lines)
def generate_batch(level,seed,count,template=None,profile=None):
 # A small delivered subgroup must not teach a fixed answer-bank rank. Rejection
 # is deterministic and regenerates the mathematical instance and complete bank.
 records=[];ranks={}
 for i in range(count):
  rec=generate(level,seed+i,template,profile=profile)
  name=rec['generation']['template'];seen=ranks.setdefault(name,[])
  if len(seen)==1 and 'correct_numerical_rank' in rec['generation']:
   for retry in range(120):
    if rec['generation']['correct_numerical_rank']!=seen[0]:break
    rec=generate(level,seed+i+1000003*(retry+1),name,profile='method:'+name)
   else:raise ValueError('Cannot construct a rank-varied family batch')
  seen.append(rec['generation'].get('correct_numerical_rank'))
  records.append(rec)
 return records

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard'],default='hard');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=5);parser.add_argument('--format',choices=['json','markdown'],default='json');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
 if args.count<0:parser.error('--count must be nonnegative')
 records=generate_batch(args.difficulty,args.seed,args.count,args.template,args.profile)
 print(json.dumps(_apply_source_notation(records),indent=2,ensure_ascii=False) if args.format=='json' else '\n\n'.join(markdown(r) for r in records))

from source_notation import install as _install_source_notation, apply as _apply_source_notation
_install_source_notation(globals())

if __name__=='__main__':main()
