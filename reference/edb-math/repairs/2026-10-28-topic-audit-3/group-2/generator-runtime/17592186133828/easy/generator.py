#!/usr/bin/env python3
"""Seeded planar vector line-integral evaluation with a three-band progression.

Eight observed moderate families, affine easy practice, and offset-spiral hard
practice. Original source banks are available only as exact evidence-only replay.
Normal practice uses local operation errors and deterministic cue-varied batches.
No plots, external runtime paths, publication, or database operations.
"""
from pathlib import Path
import argparse, hashlib, json, random, sys, uuid, re
from collections import Counter
from functools import lru_cache
sys.dont_write_bytecode=True
import sympy as s
from math_format import normalize_prose, normalize_tex, checked_math_content, cells

KP_ID=17592186133828
HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/'source.json').read_text())
KP=SOURCE['material']['kp']
VERSION='plane-line-integral-4'
x,y,t=s.symbols('x y t', real=True)
NAMESPACE=uuid.UUID(KP[':knowledge-point/id'])
FAMILIES=['log','polynomial','offset_circle','rotation','spiral','parabola','rational','arcsine']
QUESTIONS=dict(zip(FAMILIES,KP[':knowledge-point/questions']))
TEMPLATES={**{f:'moderate' for f in FAMILIES},'affine':'easy','offset_spiral':'hard'}
# Exact source banks support replay; no historical error rationale is inferred.
OPAQUE={
 'log':[4,2,3,1,0], 'polynomial':[s.Rational(55,4),s.Rational(27,4),s.Rational(35,4),s.Rational(89,4),s.Rational(109,4)],
 'offset_circle':[-1,0,2,-2,1], 'rotation':[s.pi,2*s.pi,0,1,2],
 'spiral':[2,2*s.pi**2,s.pi,s.pi**2,2*s.pi], 'parabola':[3,1,4,0,2],
 'rational':[-7,-2,9,2,-11], 'arcsine':[-4-s.sqrt(2),s.sqrt(2),1-s.sqrt(3),-2+s.sqrt(3),2-s.sqrt(3)]}
CORRECT_INDEX={'log':0,'polynomial':4,'offset_circle':2,'rotation':0,'spiral':1,'parabola':1,'rational':0,'arcsine':4}

def visual_length(text):
 # Conservative width estimate used only for display line breaking.
 text=re.sub(r'\\(?:left|right|,|!|quad|qquad)', '', text)
 text=re.sub(r'\\(?:operatorname|text|textrm|mathrm|mathbf|frac|sqrt)', '', text)
 text=re.sub(r'\\([A-Za-z]+)', lambda m: {'cdot':'·','prime':"'",'pi':'π','int':'∫'}.get(m[1],m[1]),text)
 return len(re.sub(r'[{}\s^_]', '',text))

def wrap_rhs(rhs):
 # Break only at top-level binary operators, never within fractions or groups.
 parts=[];start=0;braces=0;parens=0;i=0
 while i<len(rhs):
  char=rhs[i]
  if char=='{':braces+=1
  elif char=='}':braces-=1
  elif char in '([':parens+=1
  elif char in ')]':parens-=1
  if i>start and braces==0 and parens==0 and (char in '+-' or rhs.startswith(r'\cdot',i)):
   parts.append(rhs[start:i]);start=i
  i+=1
 parts.append(rhs[start:])
 lines=[];line=''
 for part in parts:
  if line and visual_length(line+part)>24:lines.append(line);line=part
  else:line+=part
 if line:lines.append(line)
 if len(lines)==1:return rhs
 return r'\begin{aligned}&'+r' \\ &{} '.join(lines)+r'\end{aligned}'

def wrap_display(match):
 body=match[1]
 if not (body.startswith(r'\begin{aligned}') and body.endswith(r'\end{aligned}')):return match[0]
 rows=cells(body[len(r'\begin{aligned}'):-len(r'\end{aligned}')])
 if not rows or any(len(row)!=2 or not row[1].lstrip().startswith('=') for row in rows):return match[0]
 if max(visual_length(''.join(row)) for row in rows)<=24:return match[0]
 lhs=rows[0][0]
 if any(row[0].strip() for row in rows[1:]):return match[0]
 values=[wrap_rhs(row[1].lstrip()[1:].strip()) for row in rows]
 return '$$\n'+r'\begin{gathered}'+lhs+r' \\ \begin{aligned} &='+r' \\ &='.join(values)+r'\end{aligned}\end{gathered}'+'\n$$'

def clean_prose(text):
 text=text.replace('⁡','').replace('′',r"\prime").replace('f(r(t))','F(r(t))').replace('Evaluate$','Evaluate $')
 text=text.replace('{sin}',r'{\sin}').replace('{cos}',r'{\cos}')
 text=normalize_prose(text)
 return re.sub(r'\$\$\n(.*?)\n\$\$',wrap_display,text,flags=re.S)

def tex(e):
 return s.latex(s.sympify(e),order='lex',inv_trig_style='full').replace(r'\log',r'\ln')
def uid(v): return str(uuid.uuid5(NAMESPACE,v))
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def group(e): return '('+tex(e)+')'
def wrapped_group(e): return r'\left({'+wrap_rhs(tex(e))+r'}\right)'
def vec(a,b): return group(a)+r'\,i+'+group(b)+r'\,j'
def align(rows): return '$$\n'+r'\begin{aligned}'+r' \\ '.join(lhs+' & ='+rhs for lhs,rhs in rows)+r'\end{aligned}'+'\n$$'
@lru_cache(maxsize=4096)
def _integrate_unit(e,a,b):
 return s.simplify(s.integrate(s.trigsimp(s.expand_trig(e)),(t,a,b)))
def integrate(e,a,b):
 factor,unit=s.expand_mul(e).as_content_primitive()
 return s.simplify(factor*_integrate_unit(unit,a,b))

class SampleRejected(ValueError): pass

def model(f,p):
 """Exact components, orientation and closed nonsingular interval."""
 c=s.Integer(p.get('c',1))
 d=PATH_DEFAULTS.get(f,{}); k=s.Integer(p.get('k',d.get('k',1))); u=s.Integer(p.get('u',d.get('u',1))); v=s.Integer(p.get('v',d.get('v',1)))
 if f=='affine': return (c*y+p['h'],c*x+p['d']*y+p['j'],p['u']*t+p['v'],p['w']*t+p['z'],s.Integer(p['a']),s.Integer(p['b']))
 if f=='offset_spiral':
  X,Y=(t*s.sin(t),t*s.cos(t)) if not p['swap'] else (t*s.cos(t),t*s.sin(t))
  return (c*x+p['h'],c*y+p['j'],X,Y,s.pi*p['a']/2,s.pi*p['b']/2)
 if f=='log': return (c*s.exp(x),2*c*y,s.log(t),k*t,s.Integer(p['a']),s.Integer(p['b']))
 if f=='polynomial': return (c*x*x*y,c*(x+1),u*t,v+t,s.Integer(p['a']),s.Integer(p['b']))
 if f=='offset_circle': return (c*x,c*(y-1),k*s.sin(t),k*s.cos(t),s.pi*p['a']/2,s.pi*p['b']/2)
 if f=='rotation': return (c*y,-c*x,u*s.sin(t),v*s.cos(t),s.pi*p['a']/2,s.pi*p['b']/2)
 if f=='spiral': return (c*x,c*y,k*t*s.sin(t),k*t*s.cos(t),s.pi*p['a']/2,s.pi*p['b']/2)
 if f=='parabola': return (c*y,c*x,u*t,v*t*t,s.Integer(p['a']),s.Integer(p['b']))
 if f=='rational': return (c*(y+1)/x,-2*c*(x-1)/y,k*k*t*t,k*t-1,s.Integer(p['a']),s.Integer(p['b']))
 if f=='arcsine': return (c*y*s.sin(x),c*(x+y),s.asin(t),k,s.Rational(p['a']),s.Rational(p['b']))
 raise ValueError(f)

PATH_DEFAULTS={'log':{'k':1},'polynomial':{'u':3,'v':2},'offset_circle':{'k':1},
 'rotation':{'u':1,'v':1},'spiral':{'k':1},'parabola':{'u':1,'v':1},
 'rational':{'k':1},'arcsine':{'k':2}}
PATH_DOMAINS={f:{key:([1,2,3] if f=='polynomial' and key=='u' else [0,1,2] if f=='polynomial' and key=='v' else [1,2] if f=='rational' else [1,2,3]) for key in defaults} for f,defaults in PATH_DEFAULTS.items()}

ORIGINAL_PARAMETERS={f:{'c':1,'a':0,'b':1} for f in FAMILIES}
ORIGINAL_PARAMETERS.update({'log':{'c':1,'a':1,'b':2},'offset_circle':{'c':1,'a':0,'b':2},'rotation':{'c':1,'a':0,'b':2},'spiral':{'c':1,'a':0,'b':4},'rational':{'c':1,'a':3,'b':4},'arcsine':{'c':1,'a':'0','b':'1/2'}})

def guard(f,p,observed=False):
 if f=='affine':
  if set(p)!={'c','h','d','j','u','v','w','z','a','b'}:raise ValueError('Affine parameter slots')
  if any(type(v) is not int for v in p.values()):raise ValueError('Integer affine slots')
  if any(abs(p[k])>2 for k in ['c','h','d','j','u','v','w','z']) or not p['c'] or not p['u'] or not p['w']:raise ValueError('Small nonzero slopes and coupling required')
  if not -1<=p['a']<p['b']<=2:raise ValueError('Small affine interval')
 elif f=='offset_spiral':
  if set(p)!={'c','h','j','a','b','swap'}:raise ValueError('Spiral parameter slots')
  if any(type(v) is not int for v in p.values()):raise ValueError('Integer spiral slots')
  if not 1<=abs(p['c'])<=2 or any(abs(p[k])>2 for k in ['h','j']) or not (p['h'] or p['j']):raise ValueError('Nonzero offset and small coefficients required')
  if p['swap'] not in [0,1] or not 0<=p['a']<p['b']<=4:raise ValueError('Quarter-turn regular spiral interval')
 if f in FAMILIES:
  if not {'c','a','b'} <= set(p) or set(p)-{'c','a','b'}-set(PATH_DEFAULTS[f]): raise ValueError('Expected c,a,b and family coordinate slots')
  for key,default in PATH_DEFAULTS[f].items():
   value=p.get(key,default)
   if type(value) is not int or value not in PATH_DOMAINS[f][key]:raise ValueError('Coordinate slot outside family workload: '+key)
   if observed and value!=default:raise ValueError('Observed banks retain source path; use method profile for coordinate changes')
  if type(p['c']) is not int or not 1<=abs(p['c'])<=6: raise ValueError('Nonzero integer |c|<=6 required')
  a,b=s.sympify(p['a']),s.sympify(p['b'])
  if not a.is_Rational or not b.is_Rational or not a<b: raise ValueError('Ordered rational endpoint parameters required')
  if f=='arcsine':
   if a not in [0,s.Rational(1,4),s.Rational(1,2)] or b not in [s.Rational(1,2),s.Rational(3,4)]: raise ValueError('Regular familiar radical endpoints required')
  elif f in ['offset_circle','rotation','spiral']:
   if not (a.is_Integer and b.is_Integer and 0<=a<b<=4): raise ValueError('Quarter-turn endpoint bounds required')
  else:
   lo=2 if f=='rational' else 1 if f=='log' else 0
   hi=5 if f=='rational' else 4 if f in ['log','parabola'] else 2
   if not (a.is_Integer and b.is_Integer and lo<=a<b<=hi): raise ValueError('Endpoints outside family workload')
  if observed and p['c']!=1:raise ValueError('Source replay retains the original field')
  if observed and (p['a'],p['b'])!=(ORIGINAL_PARAMETERS[f]['a'],ORIGINAL_PARAMETERS[f]['b']): raise ValueError('Observed masks retain source interval; use method profile for endpoint changes')
def sample(f,rng):
 if f=='affine':
  return dict(c=rng.choice([-2,-1,1,2]),h=rng.randint(-2,2),d=rng.choice([-1,0,1]),j=rng.randint(-2,2),u=rng.choice([-2,-1,1,2]),v=rng.randint(-2,2),w=rng.choice([-2,-1,1,2]),z=rng.randint(-2,2),a=0,b=1)
 if f=='offset_spiral':
  h,j=rng.choice([(h,j) for h in [-2,-1,0,1,2] for j in [-2,-1,0,1,2] if h or j])
  a,b=sorted(rng.sample(range(5),2))
  return dict(c=rng.choice([-2,-1,1,2]),h=h,j=j,a=a,b=b,swap=rng.randrange(2))
 if f in FAMILIES:
  p=dict(ORIGINAL_PARAMETERS[f]); p['c']=rng.choice([-2,-1,1,2])
  if f=='arcsine': p['a'],p['b']=rng.choice([('0','1/2'),('0','3/4'),('1/4','1/2'),('1/4','3/4'),('1/2','3/4')])
  elif f in ['offset_circle','rotation','spiral']: p['a'],p['b']=sorted(rng.sample(range(5),2))
  else:
   lo,hi=(2,5) if f=='rational' else (1,4) if f=='log' else (0,4) if f=='parabola' else (0,2)
   p['a'],p['b']=sorted(rng.sample(range(lo,hi+1),2))
  p.update({key:rng.choice(values) for key,values in PATH_DOMAINS[f].items()})
  return p
 raise ValueError(f)

# The observed template's mathematical spans are explicit whole-component slots.
# Scaling the field scales every evaluated scalar stage, but never r or r'.
# These masks preserve exact source prose, omissions, row sequence and spelling.
def observed_text(f,c):
 q=QUESTIONS[f]
 prompt=q[':question/problem']
 solution=q[':question/worked-solution']
 # Complete field and substitution components, identified by aligned blocks.
 import re
 field=re.search(r'F\(x,y\)=(.*?)\$ and',prompt).group(1)
 prompt=prompt.replace('F(x,y)='+field,'F(x,y)='+scale_vector(field,c))
 blocks=list(re.finditer(r'\$\$\n(.*?)\n\$\$',solution,re.S))
 changes=[]
 for j,m in enumerate(blocks):
  body=m.group(1)
  if j in [2,4,5]:
   rows=body.split(r' \\  & =')
   # First F-substitution/dot/integral row has a symbolic LHS and RHS.
   first=rows[0]
   lhs,rhs=first.split(' & =',1)
   values=[rhs]+rows[1:]
   out=[]
   for idx,v in enumerate(values):
    ending=''
    if v.endswith(r'\end{aligned}'):
     v=v[:-len(r'\end{aligned}')]; ending=r'\end{aligned}'
    if j==2: value=scale_vector(v,c)
    elif j==4:
     value=scale_dot(v,c) if idx==0 else scaled(v,c)
    else:
     # Formal F(r(t)) row already represents the scaled named field.
     value=v if idx==0 else scale_integral_stage(v,c)
    out.append(value+ending)
   body=lhs+' & ='+r' \\  & ='.join(out)
  changes.append((m.start(1),m.end(1),body))
 for a,b,v in reversed(changes): solution=solution[:a]+v+solution[b:]
 return prompt,solution

def scaled(v,c):
 if c==1:return v
 return group(c)+r'\left('+v.rstrip('.')+r'\right)'+('.' if v.endswith('.') else '')
def scale_vector(v,c): return scaled(v,c)
def scale_dot(v,c):
 if c==1:return v
 left,right=v.split(r'\cdot ',1)
 return scaled(left,c)+r'\cdot '+right

def scale_integral_stage(v,c):
 if c==1:return v
 # Whole definite integral, primitive, and arithmetic stages scale homogeneously.
 return scaled(v,c)

# All normal solutions show held-variable formal operators, substituted vector
# components, derivative operators, component products, expanded sum, primitive,
# each endpoint's individual primitive terms, then collected arithmetic.
def normal_text(f,p,m):
 P,Q,X,Y,a,b=m
 dx,dy=s.diff(X,t),s.diff(Y,t)
 FP=s.simplify(P.subs({x:X,y:Y},simultaneous=True)); FQ=s.simplify(Q.subs({x:X,y:Y},simultaneous=True))
 A=s.expand(FP*dx); B=s.expand(FQ*dy); integrand=s.simplify(s.trigsimp(A+B)); primitive=s.integrate(integrand,t)
 if f=='offset_spiral':
  # Preserve the source-supported product-rule terms; never introduce a phase identity.
  integrand=s.expand(p['c']*t+p['h']*dx+p['j']*dy)
  primitive=s.expand(p['c']*t*t/2+p['h']*X+p['j']*Y)
 terms=s.Add.make_args(primitive)
 def endpoint(z): return '+'.join(group(s.simplify(v.subs(t,z))) for v in terms)
 prompt=r'Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)='+vec(P,Q)+r'$ and $C$ is the path $r(t)='+vec(X,Y)+r'$ for $t\in['+tex(a)+','+tex(b)+r'].$'
 sol='We will use the formula\n\n'+ '$$\n'+r'\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.'+'\n$$'
 sol+='\n\nAlong the curve $C,$ we have\n\n$$\nx='+tex(X)+r',\quad y='+tex(Y)+'.\n$$'
 # Unevaluated substitution deliberately retains nested products and sums.
 def substitute_tex(expr):
  return re.sub(r'\b[xy]\b',lambda m:r'\left('+tex(X if m[0]=='x' else Y)+r'\right)',tex(expr))
 up=substitute_tex(P);uq=substitute_tex(Q)
 sol+='\n\nTherefore,\n\n'+align([('F(r(t))',vec(P,Q)),('',r'\left('+up+r'\right)\,i+\left('+uq+r'\right)\,j'),('',vec(FP,FQ))])
 sol+='\n\nComputing $r^{\\prime}(t),$ we get\n\n'+align([(r'r^{\prime}(t)',r'\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j'),('',r'\frac{\text{d}}{\text{d}t}('+tex(X)+r')\,i+\frac{\text{d}}{\text{d}t}('+tex(Y)+r')\,j'),('',vec(dx,dy))])
 sol+='\n\nTherefore,\n\n'+align([(r'F(r(t))\cdot r^{\prime}(t)',r'\left({'+wrap_rhs(vec(FP,FQ))+r'}\right)\cdot\left({'+wrap_rhs(vec(dx,dy))+r'}\right)'),('',group(FP)+r'\cdot'+group(dx)+'+'+group(FQ)+r'\cdot'+group(dy)),('',wrapped_group(A)+'+'+wrapped_group(B)),('',tex(integrand))])
 value=integrate(integrand,a,b)
 sol+='\n\nFinally, we can evaluate the integral, as follows:\n\n'+align([(r'\int_C F\cdot\text{d}r',r'\int_{'+tex(a)+'}^{'+tex(b)+r'}F(r(t))\cdot r^{\prime}(t)\,\text{d}t'),('',r'\int_{'+tex(a)+'}^{'+tex(b)+r'}\left({'+wrap_rhs(tex(integrand))+r'}\right)\,\text{d}t'),('',r'\left[{'+wrap_rhs(tex(primitive))+r'}\right]_{'+tex(a)+'}^{'+tex(b)+'}'),('','('+endpoint(b)+')-('+endpoint(a)+')'),('',group(primitive.subs(t,b))+'-'+group(primitive.subs(t,a))),('',tex(value))])
 return prompt,sol

# Complete method banks are selected before parameters. Family-specific errors
# avoid a universal answer +/- perturbation bank. No first-valid replacement.
def bank(f,m,profile,rng):
 P,Q,X,Y,a,b=m; FP=P.subs({x:X,y:Y},simultaneous=True); FQ=Q.subs({x:X,y:Y},simultaneous=True); dx=s.diff(X,t);dy=s.diff(Y,t)
 correct=integrate(FP*dx+FQ*dy,a,b)
 if f=='offset_spiral':
  radial_x=s.simplify(X/t);radial_y=s.simplify(Y/t)
  errors=[('omit_radial_product_rule_terms',FP*(dx-radial_x)+FQ*(dy-radial_y)),('double_radial_product_rule_terms',FP*(dx+radial_x)+FQ*(dy+radial_y)),('omit_x_component',FQ*dy),('omit_y_component',FP*dx),('subtract_y_product',FP*dx-FQ*dy)]
 elif f=='rotation':
  errors=[('omit_y_component',FP*dx),('subtract_y_product',FP*dx-FQ*dy),('double_x_component',2*FP*dx+FQ*dy),('double_both_derivatives',2*(FP*dx+FQ*dy))]
 elif f=='offset_circle':
  errors=[('omit_x_component',FQ*dy),('omit_constant_offset',FP*dx+(FQ+P/x)*dy),('reverse_y_derivative',FP*dx-FQ*dy),('forget_negative_cosine_derivative',FP*dx-FQ*dy)]
  # Last two would be identical: use forgetting all coordinate derivatives.
  errors[-1]=('omit_both_derivatives',FP+FQ)
 elif f=='spiral':
  c=s.simplify(P/x)
  radial_x=s.simplify(X/t);radial_y=s.simplify(Y/t)
  errors=[('omit_radial_product_rule_terms',FP*(dx-radial_x)+FQ*(dy-radial_y)),('double_radial_product_rule_terms',FP*(dx+radial_x)+FQ*(dy+radial_y)),('omit_t_in_field',c*radial_x*dx+c*radial_y*dy),('omit_one_product_rule_term',FP*(dx-radial_x)+FQ*dy)]
 elif f=='arcsine':
  c=s.simplify(P/(y*s.sin(x)))
  errors=[('omit_inverse_sine_derivative',FP),('replace_sqrt_by_radicand',FP/(1-t*t)),('reverse_primitive_sign',-FP*dx),('differentiate_as_sqrt',FP*s.sqrt(1-t*t))]
 elif f=='parabola':
  errors=[('swap_coordinate_derivatives',FP*dy+FQ*dx),('omit_t_in_y_derivative',FP*dx+FQ*s.simplify(dy/t)),('omit_x_component',FQ*dy),('omit_y_component',FP*dx)]
 elif f=='log':
  errors=[('omit_log_derivative',FP+FQ*dy),('omit_exponential_component',FQ*dy),('differentiate_log_as_negative_reciprocal',-FP*dx+FQ*dy),('omit_y_derivative_and_field_factor',FP*dx+FQ/2)]
 else:
  errors=[('omit_x_derivative',FP+FQ*dy),('omit_y_derivative',FP*dx+FQ),('omit_x_component',FQ*dy),('subtract_y_product',FP*dx-FQ*dy)]
  if f in ['polynomial','parabola','rational']:
   errors[1]=('omit_y_component',FP*dx)
 # Complete alternatives derive from local component, derivative and endpoint errors.
 errors += [('reverse_orientation',-(FP*dx+FQ*dy)),
            ('double_x_derivative',2*FP*dx+FQ*dy),
            ('double_y_derivative',FP*dx+2*FQ*dy),
            ('swap_derivatives',FP*dy+FQ*dx)]
 candidates=[]
 for name,expr in errors:
  value=integrate(expr,a,b)
  if value.has(s.oo,s.zoo,s.nan) or s.simplify(value-correct)==0:continue
  if not any(s.simplify(value-v)==0 for _,v in candidates):candidates.append((name,value))
 integrand=s.trigsimp(FP*dx+FQ*dy)
 primitive=s.integrate(integrand,t)
 for name,value in [('add_lower_endpoint',primitive.subs(t,b)+primitive.subs(t,a)),('omit_lower_endpoint',primitive.subs(t,b)),('reverse_upper_endpoint',-primitive.subs(t,b)-primitive.subs(t,a))]:
  value=s.simplify(value)
  if not value.has(s.oo,s.zoo,s.nan) and s.simplify(value-correct)!=0 and not any(s.simplify(value-v)==0 for _,v in candidates):candidates.append((name,value))
 if len(candidates)<4:raise SampleRejected('Fewer than four distinct local errors')
 rng.shuffle(candidates)
 for attempt in range(50):
  chosen=rng.sample(candidates,4);vals=[correct]+[v for _,v in chosen]
  if correct!=0 and sum(s.sign(v)==s.sign(correct) for v in vals)<2:continue
  if sum(v.is_Integer==correct.is_Integer for v in vals)<2:continue
  opposite_pairs=[(i,j) for i in range(5) for j in range(i) if s.simplify(vals[i]+vals[j])==0]
  if len(opposite_pairs)==1 and 0 in opposite_pairs[0]:continue
  def shape(v):
   return (bool(v.is_Rational),v.has(s.pi),v.has(s.log),any(q.exp.is_Rational and not q.exp.is_Integer for q in v.atoms(s.Pow)))
  if sum(shape(v)==shape(correct) for v in vals)<2:continue
  # A bank-only intersection of modal pi coefficients must not single out the key.
  try:
   polys=[s.Poly(s.expand(v),s.pi) for v in vals]
   degree=max(poly.degree() for poly in polys)
   if degree>0:
    vectors=[tuple(poly.nth(i) for i in range(degree+1)) for poly in polys]
    modes=[]
    for i in range(degree+1):
     counts=Counter(v[i] for v in vectors);top=max(counts.values());modes.append({v for v,n in counts.items() if n==top})
    intersection=[j for j,v in enumerate(vectors) if all(v[i] in modes[i] for i in range(degree+1))]
    if intersection==[0]:continue
  except (s.PolynomialError,TypeError):pass
  return vals,['correct']+[name for name,_ in chosen]
 raise SampleRejected('No bank without a unique sign or integer-type key')

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ['easy','moderate','hard']: raise ValueError('Unsupported difficulty')
 if field_type not in [None,'radio']:raise ValueError('Only observed radio layout supported')
 if profile and profile.startswith('observed_'):
  family=profile[len('observed_'):]
  if template is not None and template!=family:raise ValueError('Profile/template mismatch')
  template=family
 elif profile not in [None,'method']:raise ValueError('Unknown profile')
 eligible=[f for f,l in TEMPLATES.items() if l==level]
 if template is not None and template not in eligible:raise ValueError('Template outside level')
 rng=random.Random(seed); f=template or rng.choice(eligible); profile=profile or 'method'; observed=profile.startswith('observed_')
 for attempt in range(200):
  p=dict(parameters) if parameters is not None else (dict(ORIGINAL_PARAMETERS[f]) if observed else sample(f,rng))
  try:
   guard(f,p,observed); m=model(f,p)
   if observed:
    vals=[p['c']*v for v in OPAQUE[f]]; recipes=['opaque_homogeneous_pattern']*5; idx=CORRECT_INDEX[f]
    prompt,sol=observed_text(f,p['c'])
    value=integrate(m[0].subs({x:m[2],y:m[3]},simultaneous=True)*s.diff(m[2],t)+m[1].subs({x:m[2],y:m[3]},simultaneous=True)*s.diff(m[3],t),m[4],m[5])
    assert s.simplify(vals[idx]-value)==0
    original_values=[a[':answer/value'] for a in QUESTIONS[f][':question/answer-fields'][0][':answer-field/choices']]
    strings=[v if p['c']==1 else tex(p['c'])+r'\left('+v+r'\right)' for v in original_values]
   else:
    vals,recipes=bank(f,m,profile,rng);idx=0;prompt,sol=normal_text(f,p,m);strings=[tex(v) for v in vals]
   if f=='affine':
    prompt+='\n\n*Hint:* Use $\\int_C F\\cdot\\mathrm d r=\\int_a^b F(r(t))\\cdot r^{\\prime}(t)\\,\\mathrm dt$.'
   if f=='offset_spiral':
    primitive=s.expand(m[0].coeff(x)*t*t/2+p['h']*m[2]+p['j']*m[3])
    sol+='\n\nThe offset terms integrate by the reverse product rule:\n\n'+align([(r'\frac{\mathrm d}{\mathrm dt}\left('+tex(primitive)+r'\right)',tex(s.expand(s.diff(primitive,t))))])
   break
  except SampleRejected:
   if parameters is not None:raise
 else:raise SampleRejected('No eligible complete bank in bounded sampler')
 prompt=clean_prose(prompt);sol=clean_prose(sol);strings=[normalize_tex(v) for v in strings]
 task=digest([level,[s.srepr(z) for z in m]])
 content=digest([VERSION,level,prompt,sol,sorted(strings)])
 qid=uid(content);fid=uid(qid+':selection');answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in strings]
 correct=answers[idx][':answer/id'];rng.shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':s.__version__,'seed':seed,'template':f,'parameters':p,'bank_profile':profile,'bank_origin':'observed opaque homogeneous evidence' if observed else 'authored method-derived','evidence_only':observed,'eligible_for_learning':not observed,'authored_extension':not observed or p['c']!=1,'difficulty_origin':'observed' if level=='moderate' else 'authored','parameter_fingerprint':task,'content_fingerprint':content,'source':{k:SOURCE[k] for k in ['database','basis','lineage']},'source_ids':[QUESTIONS[f][':question/id']] if f in FAMILIES else [],'correct_rank':sorted(range(5),key=lambda j:float(s.N(vals[j],20))).index(idx),'recipes':recipes,'recipe_values':strings,'domain':'nonsingular forward interval; see parameters and instructional account','plot_rating':'none'}}

def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)

def generate_batch(level,seed,count,template=None,profile=None):
 # Deterministic rejection/resampling keeps repeated visible families from sharing
 # one answer rank. Do not hand-pick replacement seeds after seeing a batch.
 records=[];ranks={};positions={};seen=set();cue_ranks={}
 def visible_groups(rec):
  f=rec['generation']['template'];p=rec['generation']['parameters'];c=p['c']
  groups=[('field_sign',f,1 if c>0 else -1),('field_magnitude',f,abs(c)),('signed_field_scale',f,c)]
  if 'swap' in p:groups.append(('coordinate_order',f,p['swap']))
  if 'h' in p and 'j' in p:groups.append(('offset_count',f,int(bool(p['h']))+int(bool(p['j']))))
  return groups
 for i in range(count):
  first=generate(level,seed+i,template,profile=profile)
  family=first['generation']['template']
  for attempt in range(200):
   rec=first if attempt==0 else generate(level,seed+i+1000003*attempt,family,profile=profile)
   rank=rec['generation']['correct_rank'];field=rec['question'][':question/answer-fields'][0]
   position=next(j for j,a in enumerate(field[':answer-field/choices']) if a[':answer/id']==field[':answer-field/correct'][1])
   if rec['question'][':question/id'] in seen:continue
   if profile and profile.startswith('observed_'):
    # Exact replay is evidence, not an extensible practice batch.
    if count!=1:raise ValueError('Source replay requires count=1')
   if family in ranks and rank==ranks[family][-1]:continue
   if family in positions and position==positions[family][-1]:continue
   groups=visible_groups(rec)
   if any(group in cue_ranks and rank==cue_ranks[group][-1] for group in groups):continue
   for group in groups:cue_ranks.setdefault(group,[]).append(rank)
   records.append(rec);seen.add(rec['question'][':question/id']);ranks.setdefault(family,[]).append(rank);positions.setdefault(family,[]).append(position);break
  else:raise SampleRejected('Could not construct a cue-varied deterministic batch')
 return records

def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return ('### Generated — '+q[':question/difficulty'].split('/')[-1]+' / '+rec['generation']['template']+' / '+rec['generation']['bank_profile']+'\n\n'+q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution'])
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard'],default='moderate');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile',choices=['method']);ap.add_argument('--format',choices=['markdown','json'],default='json');a=ap.parse_args()
 if a.count<1:ap.error('Positive count required')
 levels=[a.difficulty]
 recs=generate_batch(a.difficulty,a.seed,a.count,a.template,a.profile)
 print(json.dumps(recs,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,recs)))
if __name__=='__main__':main()
