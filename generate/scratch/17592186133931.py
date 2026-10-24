#!/usr/bin/env python3
"""Basis-1356 closed-surface flux generators, steps 3–7 only.

Geometry parameters are substantive integration limits; fixed observed field
structures retain all held-coordinate partials and the individual source chains.
Observed opaque scalar banks are public evidence profiles, never defaults.
Default five-option banks are complete method-derived integration operations.
No database calls, assets, shared-file writes, or runtime source sampling.
"""
from __future__ import annotations

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186133931-source-policy.json'))
    raise SystemExit(0)

import argparse, hashlib, json, random, re, sys, uuid
from functools import lru_cache
from itertools import product
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parent/'17592186133931'
SOURCE=json.loads((ROOT/'source.json').read_text())
KP=SOURCE['record']; QUESTIONS=KP[':knowledge-point/questions']
VERSION='closed-flux-1'
x,y,z=s.symbols('x y z',real=True); VARIABLES=(x,y,z)
NS=uuid.UUID('0b249c36-4d2c-4f2e-bd2f-820e13cdab26')
# Fields are deliberately fixed within each observed family; meaningful variation
# comes from three independent pairs of integration limits, not notation aliases.
FAMILIES={
 'xz':dict(source=17592186134139, F=(2*x*z,x*x+z,s.Integer(2)), factors=(1,1,2*z), anchor=(-1,1,0,1,0,1)),
 'cos':dict(source=17592186134140,F=(x*x*s.cos(z),s.sin(z),x+y),factors=(2*x,1,s.cos(z)),anchor=(0,2,0,1,0,s.pi/2)),
 'xy_a':dict(source=17592186281505,F=(x*x*y,2*z,x*y*z),factors=(x,y,3),anchor=(0,2,0,4,1,2)),
 'log':dict(source=17592186281506,F=(y*s.log(x),z*z,x-y**3),factors=(1/x,y,1),anchor=(1,s.E,0,2,0,2)),
 'affine':dict(source=17592186281507,F=(x*x,2*y,x+y*y),factors=(2*x+2,1,1),anchor=(0,1,1,2,1,3)),
 'xy_b':dict(source=17592186281508,F=(2*y,x*y*y,2*x*y*z),factors=(2*x,2*y,1),anchor=(0,1,1,2,-1,1)),
 'cancel_x':dict(source=17592186374200,F=(y-x*x,x*y,3*x*z),factors=(2*x,1,1),anchor=(1,3,0,2,-1,1)),
 'cancel_x2':dict(source=17592186374207,F=(2*x**3+z,-z,-3*x*x*z),factors=(3*x*x,1,1),anchor=(-1,1,0,3,1,3)),
 'cancel_z':dict(source=17592186430948,F=(y*z*z,-2*y*z,3*z*z),factors=(1,1,4*z),anchor=(-1,2,0,1,-1,2)),
 'exp':dict(source=17592186430950,F=(y+z*z,-x,3*x*x*s.exp(z)),factors=(3*x*x,1,s.exp(z)),anchor=(0,1,1,3,0,s.log(3))),
 # Easy authored from lesson's rectangular-solid tutorial: one constant partial.
 'constant':dict(source=None,F=(2*x+1,3*z,x*y),factors=(2,1,1),anchor=(0,3,0,2,0,1)),
 # Hard authored from this KP's canonical example, never the known-solid sibling.
 'canonical':dict(source=None,F=(s.exp(z),x*x*y*y,4*x*x*y*z),factors=(3*x*x,2*y,1),anchor=(0,1,0,2,1,2)),
}
BYID={q[':db/id']:q for q in QUESTIONS}
for name,d in FAMILIES.items():
 d['F']=tuple(map(s.sympify,d['F']));d['factors']=tuple(map(s.sympify,d['factors']))
 if d['source']:
  q=BYID[d['source']];p=q[':question/problem'];field=re.search(r'\$F\s*=\s*(.*?)\$,? find',p).group(1)
  # F terminal punctuation belongs to the surrounding source mask.
  d['field_text']=field.removesuffix(',')
  if ':question/worked-solution' in q:
   blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
   rows=blocks[0].split(r'\\  & =')
   d['div_rows']=blocks[0]
 else:d['field_text']=None


def tex(v):
 return s.latex(s.sympify(v),mul_symbol=None).replace(r'\log',r'\ln')
def st(v):
 return tex(v)
def group(v):
 t=st(v);return '('+t+')' if s.sympify(v).could_extract_minus_sign() else t
def numberpower(v,n):
 return ('{'+st(v)+'}' if s.sympify(v)>=0 else '('+st(v)+')')+'^{'+str(n)+'}'
def difference(a,b):return '('+st(a)+'-'+group(b)+')'
def primitive_term(v,variable=None):
 # Explicit source conventions, no sinh/cosh or eager expanded endpoint nodes.
 if not v.free_symbols and variable is not None:return (st(v) if v!=1 else "")+str(variable)
 return {s.Integer(1):'',2*x:r'{x}^{2}',x:r'\frac{{x}^{2}}{2}',y:r'\frac{{y}^{2}}{2}',2*y:r'{y}^{2}',3*x*x:r'{x}^{3}',2*z:r'{z}^{2}',4*z:r'2{z}^{2}',s.Integer(3):'3z',1/x:r'\operatorname{ln}⁡x',s.cos(z):r'\operatorname{sin}⁡z',s.exp(z):r'{e}^{z}',2*x+2:r'{x}^{2}+2x',s.Integer(2):'2x'}[v]
def primitive_at(f,a):
 if f==2*x+2:return numberpower(a,2)+'+2('+st(a)+')'
 if f==2*x:return numberpower(a,2)
 if f==3*x*x:return numberpower(a,3)
 if f==s.cos(z):return r'\operatorname{sin}⁡'+('('+st(a)+')' if a else '0')
 if f==s.exp(z):return r'{e}^{'+st(a)+'}'
 if f==1/x:return r'\operatorname{ln}⁡'+(st(a) if a in (1,s.E) else '('+st(a)+')')
 if f==y:return r'\frac{'+numberpower(a,2)+'}{2}'
 return st(s.integrate(f,next(v for v in VARIABLES if v in f.free_symbols)).subs(next(v for v in VARIABLES if v in f.free_symbols),a))

def integral(f,v,a,b):
 body='' if f==1 else ('('+exprtext(f)+')' if f==2*x+2 else exprtext(f))+r'\,'
 return r'{\int }_{'+st(a)+'}^{'+st(b)+'}'+body+r'\text{d}'+str(v)
def exprtext(e):
 # Keep the lesson's explicit factor order and exponent notation.
 mapping={2*x*z:'2xz',x*x+z:r'x^{2} + z',s.Integer(2):'2',x*x*s.cos(z):r'{x}^{2}\operatorname{cos}⁡z',s.sin(z):r'\operatorname{sin}⁡z',x+y:'x+y',x*x*y:r'{x}^{2}y',2*z:'2z',x*y*z:'xyz',y*s.log(x):r'y\operatorname{ln}⁡x',z*z:r'{z}^{2}',x-y**3:r'x-{y}^{3}',x*x:r'{x}^{2}',2*y:'2y',x+y*y:r'x+{y}^{2}',x*y*y:r'x{y}^{2}',2*x*y*z:'2xyz',y-x*x:r'y-{x}^{2}',x*y:'xy',3*x*z:'3xz',2*x**3+z:r'2{x}^{3}+z',-z:'-z',-3*x*x*z:r'-3{x}^{2}z',y*z*z:r'y{z}^{2}',-2*y*z:'-2yz',3*z*z:r'3{z}^{2}',y+z*z:r'y+{z}^{2}',-x:'-x',3*x*x*s.exp(z):r'3{x}^{2}{e}^{z}',2*x*s.cos(z):r'2x\operatorname{cos}⁡z',3*x*y:'3xy',y/x:r'\frac{y}{x}',2*x+2:'2x+2',4*x*y:'4xy',2*x:'2x',3*x*x:r'3{x}^{2}',4*z:'4z',s.exp(z):r'{e}^{z}',s.cos(z):r'\operatorname{cos}⁡z',6*x*x*y:r'6{x}^{2}y',x:'x',y:'y',s.Integer(1):'1',s.Integer(3):'3',1/x:r'\frac{1}{x}',2*x+1:'2x+1',3*z:'3z',x*x*y*y:r'{x}^{2}{y}^{2}',4*x*x*y*z:r'4{x}^{2}yz'}
 return mapping.get(e,tex(e))

THEOREM=('Let $R$ be a simple solid region bounded by a closed surface $S$ with positive (outward) orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $R,$ then the divergence theorem states that\n\n$$\n'+r'{∬}_{S}F\cdot dS={∭}_{R}\text{div}\,F\,\text{d}V.'+'\n$$\n\nComputing the divergence of $F,$ we obtain\n\n$$\n')
MID='\n$$\n\nLet $R$ be the solid region enclosed by $S.$ Then, using the divergence theorem, we have\n\n$$\n'
def aligned(rows,first):return r'\begin{aligned}'+first+' & ='+r' \\  & ='.join(rows)+r'.\end{aligned}'
def source_prompt(name,b,a=2):
 d=FAMILIES[name]
 if d['source']:
  source=BYID[d['source']][':question/problem']
  # Slot the six whole equations. Do not replace naked numbers or variables.
  eq=list(re.finditer(r'\$([xyz])\s*=\s*(.*?)\$',source));assert len(eq)==6
  for i,m in reversed(list(enumerate(eq))):
   old=m.group(2);end=',' if old.endswith(',') else '.' if old.endswith('.') else ''
   # Preserve original variable/equality spacing and source boundary TeX at anchor.
   val=old[:-1] if end else old
   replacement=val if s.sympify(b[i])==s.sympify(d['anchor'][i]) else st(b[i])
   source=source[:m.start(2)]+replacement+end+source[m.end(2):]
  return source
 field=('('+str(a)+r'x+1)\,i+3z\,j+xy\,k' if name=='constant' else r'{e}^{z}\,i+{x}^{2}{y}^{2}\,j+4{x}^{2}yz\,k')
 equations=', '.join('$'+str(VARIABLES[i//2])+'='+st(v)+'$' for i,v in enumerate(b))
 return 'Let $S$ be the boundary of the rectangular prism enclosed by the planes '+equations+'. Given that the surface $S$ is positively (outward) oriented and $F='+field+'$, find the flux of $F$ across $S$.'

def field_data(name,a=2):
 d=FAMILIES[name]
 return ((a*x+1,3*z,x*y),(s.Integer(a),s.Integer(1),s.Integer(1))) if name=='constant' else (d['F'],d['factors'])

@lru_cache(maxsize=None)
def mathdata(name,b,a=2):
 d=FAMILIES[name];F,f=field_data(name,a);partials=tuple(s.diff(C,v) for C,v in zip(F,VARIABLES));div=s.expand(sum(partials));prims=[s.integrate(g,v) for g,v in zip(f,VARIABLES)]
 vals=[s.simplify(P.subs(v,b[2*i+1])-P.subs(v,b[2*i])) for i,(P,v) in enumerate(zip(prims,VARIABLES))]
 return partials,div,f,prims,vals,s.simplify(s.prod(vals))

def solution(name,b,normal=False,a=2):
 d=FAMILIES[name];part,D,fs,Ps,vs,result=mathdata(name,b,a)
 if 'div_rows' in d:divblock=r'\begin{aligned}'+d['div_rows']+r'\end{aligned}'
 else:
  formal='+'.join(r'\frac{∂}{∂'+str(v)+'}('+exprtext(F)+')' for F,v in zip(field_data(name,a)[0],VARIABLES))
  reduced='+'.join('('+exprtext(v)+')' if v.could_extract_minus_sign() else exprtext(v) for v in part)
  divblock=aligned([formal,reduced,exprtext(D)],r'\text{div}\,F')
 dt=exprtext(D);dt='('+dt+')' if name=='affine' else dt
 triple=r'{∭}_{R}'+dt+r'\,\text{d}V'
 repeat=''.join(r'{\int }_{'+st(b[2*i])+'}^{'+st(b[2*i+1])+'}' for i in range(3))+dt+r'\,\text{d}z\,\text{d}y\,\text{d}x'
 # Source spells pi/2 without a TeX fraction in its repeated/primitive limits.
 if name=='cos':repeat=repeat.replace(r'\frac{\pi}{2}',r'\pi /2')
 # Source spaces inside \frac{\pi }{2} and operatorname log are retained.
 if name=='exp':repeat=repeat.replace(r'\ln{\left(3 \right)}',r'\operatorname{ln}⁡3')
 fact=r'\cdot '.join(integral(f,v,b[2*i],b[2*i+1]) for i,(f,v) in enumerate(zip(fs,VARIABLES)))
 # Source factorization has two minimal special spacing conventions.
 if name=='cancel_x2':fact=fact.replace(r'3{x}^{2}\,',r'3{x}^{2}')
 if name=='cos':fact=fact.replace(r'\frac{\pi}{2}',r'\pi /2')
 if name=='exp':fact=fact.replace(r'\ln{\left(3 \right)}',r'\operatorname{ln}⁡3')
 primitive=[]
 for i,(f,v) in enumerate(zip(fs,VARIABLES)):
  a,c=b[2*i:2*i+2]
  if f==1 and name!='log':piece=difference(c,a)
  else:
   p=primitive_term(f,v) if f!=1 else str(v)
   square=r'{['+p+r']}' if '\\frac' in p else '['+p+']'
   piece=square+'_{'+str(v)+'='+st(a)+'}^{'+str(v)+'='+st(c)+'}'
  primitive.append(piece)
 primrow=r'\cdot '.join(primitive)
 if name=='cos':primrow=primrow.replace(r'\frac{\pi}{2}',r'\pi /2')
 if name=='exp':primrow=primrow.replace(r'\ln{\left(3 \right)}',r'\operatorname{ln}⁡3')
 endpoints=[]
 for i,(f,v,P) in enumerate(zip(fs,VARIABLES,Ps)):
  a,c=b[2*i:2*i+2]
  if f==1 and name!='log':piece=st(vs[i])
  elif name in ('cos','log','exp','cancel_x2'):
   high,low=primitive_at(f,c) if f!=1 else st(c),primitive_at(f,a) if f!=1 else group(a)
   piece='('+high+'-'+( '('+low+')' if f==2*x+2 else low)+')'
  elif name=='affine':
   # Source omits the redundant zero polynomial at its zero endpoint.
   high=primitive_at(f,c);low='0' if a==0 else '('+primitive_at(f,a)+')'
   piece='('+high+'-'+low+')'
  else:piece=difference(s.simplify(P.subs(v,c)),s.simplify(P.subs(v,a)))
  endpoints.append(piece)
 endpointrow=r'\cdot '.join(endpoints)
 rows=[triple,repeat,fact,primrow,endpointrow]
 if name in ('cos','log','exp'):
  reduced=[st(q) for q in vs]
  if name=='log':reduced=[difference(1 if b[1]==s.E else s.log(b[1]),0 if b[0]==1 else s.log(b[0])),difference(b[3]**2/2,b[2]**2/2),difference(b[5],b[4])]
  if name=='exp':reduced[2]=difference(s.exp(b[5]),s.exp(b[4]))
  rows.append(r'\cdot '.join(reduced))
 rows.append(st(result))
 # Exact original integral limit formatting is a presentation slot, not a payload branch.
 if d['source'] and ':question/worked-solution' in BYID[d['source']]:
  anchor=d['anchor']
  # Replace complete generated limit values by their observed TeX spelling when equal.
  for i,v in enumerate(b):
   if v==anchor[i] and name=='exp' and i==5:
    rows=[r.replace(st(v),r'\operatorname{ln}⁡3') for r in rows]
   if v==anchor[i] and name=='cos' and i==5:
    rows=[r.replace(r'\operatorname{sin}⁡(\frac{\pi}{2})',r'\operatorname{sin}⁡(\frac{\pi }{2})') for r in rows]
  if name=='log':rows=[r.replace(r'\ln',r'\operatorname{ln}⁡') for r in rows]
 # Normal additive primitive contains individual upper/lower component evaluation.
 extra=''
 if normal and name=='affine':
  a,c=b[:2];extra='\n\nThe individual endpoint terms are\n\n$$\n'+r'\begin{aligned}'+primitive_at(fs[0],c)+'&='+st(c*c)+'+'+group(2*c)+r' \\ '+primitive_at(fs[0],a)+'&='+st(a*a)+'+'+group(2*a)+r'.\end{aligned}'+'\n$$'
 return THEOREM+divblock+MID+aligned(rows,r'{∬}_{S}F\cdot dS')+'\n$$'+extra

# Full five-member authored method bank: one correct and four actual operations.
# Each field has exactly one nonzero separable integrand; differentiation mistakes
# are family-specific where meaningful, otherwise omitted primitive/width factors.
@lru_cache(maxsize=None)
def triple_primitive(e):
 for v in reversed(VARIABLES):e=s.integrate(e,v)
 return e
def box_integral(e,b):
 P=triple_primitive(e);value=0
 for bits in product((0,1),repeat=3):
  value+=(-1)**(3-sum(bits))*P.subs({v:b[2*i+bits[i]] for i,v in enumerate(VARIABLES)})
 return s.simplify(value)

def method_bank(name,b,a=2):
 part,D,fs,Ps,vs,A=mathdata(name,b,a);d=FAMILIES[name]
 def integrate(e):
  return box_integral(e,b)
 if name in ('xy_a','xy_b','cancel_x','cancel_x2','cancel_z','canonical'):
  nonzero=[p for p in part if p!=0]
  omit=integrate(nonzero[0])
  unsigned=integrate(sum(-p if p.could_extract_minus_sign() else p for p in part))
  if name in ('cancel_x','cancel_x2','cancel_z'):wrong1=unsigned;recipe1='drop_negative_partial_sign'
  else:wrong1=omit;recipe1='omit_second_nonzero_partial'
  wrong2=integrate(sum(s.diff(F,v,2) for F,v in zip(field_data(name,a)[0],VARIABLES)));recipe2='differentiate_components_twice'
  # Some twice-differentiated integrals are zero; still an actual wrong operation.
  vals=[A,-A,wrong1,wrong2,A/(b[5]-b[4])]
  recipes=['divergence_integral','reverse_orientation',recipe1,recipe2,'omit_z_width']
 elif name=='cos':
  wrong1=integrate(x*s.cos(z));wrong2=integrate(2*x*s.sin(z));wrong3=s.simplify(vs[0]*vs[1]*(b[5]-b[4]))
  vals=[A,-A,wrong1,wrong2,wrong3];recipes=['divergence_integral','reverse_orientation','omit_power_derivative_factor','use_negative_cos_as_cos_primitive','replace_cos_by_one']
 elif name=='log':
  vals=[A,-A,s.simplify(vs[0]*(b[3]-b[2])*vs[2]),integrate(y),s.simplify(vs[0]*(b[3]**2-b[2]**2)*vs[2])]
  recipes=['divergence_integral','reverse_orientation','omit_y_factor','log_derivative_one','omit_y_primitive_half']
 elif name=='exp':
  vals=[A,-A,s.simplify((b[1]**3-b[0]**3)*vs[1]*(b[5]-b[4])),s.simplify(vs[0]*vs[1]*s.exp(b[5])),s.simplify((b[1]**2-b[0]**2)*vs[1]*vs[2])]
  recipes=['divergence_integral','reverse_orientation','exp_derivative_one','omit_lower_exp_endpoint','wrong_x_primitive_degree']
 elif name=='affine':
  vals=[A,-A,integrate(2*x),integrate(2),s.simplify((b[1]**2+2*b[1])*vs[1]*vs[2])]
  recipes=['divergence_integral','reverse_orientation','omit_constant_partial','omit_x_partial','omit_lower_endpoint']
 elif name=='xz':
  vals=[A,-A,integrate(z),integrate(2),s.simplify(vs[0]*vs[1]*b[5]**2)]
  recipes=['divergence_integral','reverse_orientation','omit_x_derivative_coefficient','hold_z_as_one','omit_lower_z_endpoint']
 else:
  vals=[A,-A,A/(b[1]-b[0]),A/(b[3]-b[2]),A/(b[5]-b[4])]
  recipes=['divergence_integral','reverse_orientation','omit_x_width','omit_y_width','omit_z_width']
 vals=list(map(s.simplify,vals))
 if any(s.simplify(a-c)==0 for i,a in enumerate(vals) for c in vals[:i]):raise ValueError('whole-bank collision')
 return vals,recipes

INTERVALS=[(-1,1),(-1,2),(0,1),(0,2),(0,3),(1,2),(1,3),(1,4),(2,3),(2,4)]
def guard(name,b,level):
 if len(b)!=6:raise ValueError('six box limits required')
 if any(q.is_number is not True or q.is_finite is not True or q.is_real is not True for q in b):raise ValueError('exact finite real limits required')
 if any(s.simplify(b[2*i+1]-b[2*i]).is_positive is not True for i in range(3)):raise ValueError('ordered finite real limits required')
 if name=='log':
  if any(s.simplify(s.log(q)) not in (0,1,2,3) for q in b[:2]):raise ValueError('log endpoints must be e^k, k=0..3')
 elif any(q not in range(-1,6 if level=='easy' else 5) for q in b[:2]):raise ValueError('x limits -1..4')
 if name=='cos':
  if any(q not in (-s.pi/2,0,s.pi/2,s.pi,3*s.pi/2) for q in b[4:]):raise ValueError('familiar half-pi endpoints only')
 elif name=='exp':
  if any(s.simplify(s.exp(q)) not in range(1,6) for q in b[4:]):raise ValueError('z endpoints ln(k), k=1..5')
 elif any(q not in range(-1,6 if level=='easy' else 5) for q in b[4:]):raise ValueError('z limits -1..4')
 if any(q not in range(-1,6 if level=='easy' else 5) for q in b[2:4]):raise ValueError('y limits -1..4')
 if level=='hard' and (b[0]<1 or b[2]<1 or b[1]<=b[0] or b[3]<=b[2]):raise ValueError('hard uses nonzero translated power endpoint pairs')
 if level=='easy' and (b[0]!=0 or b[2]!=0 or b[4]!=0 or sorted([b[1],b[3],b[5]]) not in ([2,3,4],[2,3,5],[2,4,5],[3,4,5])):raise ValueError('easy uses three distinct positive widths 2..5')

def sample(name,rng,level):
 b=[v for _ in range(3) for v in rng.choice(INTERVALS)]
 if name=='log':b[:2]=[s.exp(k) for k in sorted(rng.sample(range(4),2))]
 if name=='cos':b[4:]=sorted(rng.sample([-s.pi/2,0,s.pi/2,s.pi,3*s.pi/2],2))
 if name=='exp':b[4:]=[s.log(k) for k in sorted(rng.sample(range(1,6),2))]
 if level=='hard':b[:4]=[v for _ in range(2) for v in rng.choice([(1,2),(1,3),(1,4),(2,3),(2,4)])]
 if level=='easy':
  w=rng.sample(range(2,6),3);b=[0,w[0],0,w[1],0,w[2]]
 return tuple(map(s.sympify,b))

def identity(payload):return str(uuid.uuid5(NS,json.dumps(payload,sort_keys=True,ensure_ascii=False)))
def source_bank(name,b):
 q=BYID[FAMILIES[name]['source']];anchor=mathdata(name,FAMILIES[name]['anchor'])[-1];A=mathdata(name,b)[-1]
 values=[]
 # Its two log options parameterize the actual z width; interpretation unresolved.
 for a in q[':question/answer-fields'][0][':answer-field/choices']:
  raw=a[':answer/value']
  if 'operatorname' in raw:
   v=(2 if raw.startswith('2') else s.Rational(1,2))*(b[5]-b[4])
   out=(r'2\operatorname{ln}⁡3' if raw.startswith('2') else r'\frac{\operatorname{ln}⁡3}{2}') if b[5]==s.log(3) and b[4]==0 else tex(v)
  else:
   v=s.sympify(raw)*A/anchor;out=tex(s.simplify(v))
  values.append((s.simplify(v),out))
 return values


def setup_record(seed,parameters,profile):
 q=BYID[17592186235537];p={'c':2,'cap':4} if parameters is None else dict(parameters)
 if set(p)!={'c','cap'} or p['c'] not in range(1,5) or p['cap'] not in range(3,7):raise ValueError('setup evidence domain')
 problem=q[':question/problem'].replace('4-x-y',str(p['cap'])+'-x-y')
 sol=q[':question/worked-solution'].replace('4-x-y',str(p['cap'])+'-x-y').replace('2x',str(p['c'])+'x')
 return package('moderate','context_setup',p,problem,sol,[str(p['c'])+'x'],0,profile,seed,'blank',q,False,['observed_integrand_fragment'])

def package(level,name,p,problem,sol,values,correct,profile,seed,kind='radio',raw=None,eligible=True,recipes=None):
 field_key='field-1' if kind=='blank' else 'selection'
 if raw and ':question/difficulty' not in raw:shownlevel=None
 else:shownlevel=level
 canonical={'version':VERSION,'level':shownlevel,'problem':problem,'solution':sol,'bank':sorted(values),'correct':correct if correct is None else values[correct]}
 qid=identity(canonical);fid=identity([qid,field_key]);answers=[{':answer/id':identity([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 f={':answer-field/id':fid,':answer-field/key':field_key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
 if correct is not None:f[':answer-field/correct']=[':answer/id',answers[correct][':answer/id']]
 random.Random(seed).shuffle(answers)
 q={':question/id':qid,':question/problem':problem,':question/answer-fields':[f]}
 if raw and ':question/math-academy-id' in raw:q[':question/math-academy-id']=raw[':question/math-academy-id']
 if shownlevel:q[':question/difficulty']=':question.difficulty/'+shownlevel
 if sol is not None:q[':question/worked-solution']=sol
 if name=='context_setup':task={'field':str(p['c'])+'x','criterion':'integrand'}
 else:
  b=tuple(s.sympify(v) for v in p['bounds']);d=FAMILIES[name]
  task={'F':[s.srepr(v) for v in field_data(name,p.get('a',2))[0]],'bounds':[s.srepr(v) for v in b],'criterion':'outward_flux'}
  if name=='constant':task={'divergence':p.get('a',2),'unordered_widths':sorted(str(b[2*i+1]-b[2*i]) for i in range(3)),'criterion':'outward_flux'}
 return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':name,'level':level,'seed':seed,'parameters':p,'profile':profile,'eligible_for_learning':eligible,'evidence_only':not eligible,'source_id':raw[':db/id'] if raw else FAMILIES.get(name,{}).get('source'),'mathematical_fingerprint':hashlib.sha256(json.dumps(task,sort_keys=True).encode()).hexdigest(),'recipes':recipes,'bank_operations':[{'recipe':recipe,'value':value} for recipe,value in zip(recipes or [],values)],'domain':{'field_smoothness':'x>0' if name=='log' else 'all real coordinates','geometry':'ordered rectangular box' if name!='context_setup' else 'captured prior-part context unavailable','workload':'constant divergence and three distinct widths' if level=='easy' else 'canonical cubic/quadratic translated endpoints' if level=='hard' else 'observed held-partial and source-specific separated-integral chain'},'provenance':{k:SOURCE[k] for k in ['database','basis','lineage']},'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__}}}

# EASY — authored tutorial scope: constant divergence and three box widths.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — observed fixed structures: compute held partials, factor and integrate.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — authored canonical scope: two active partials, cubic and quadratic endpoints.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('level')
 rng=random.Random(seed);raw=None
 if profile and profile.startswith('observed:'):
  source_id=int(profile.split(':')[1])
  if source_id not in BYID:raise ValueError('unknown observed profile')
  raw=BYID[source_id]
  name=next((n for n,d in FAMILIES.items() if d['source']==source_id),'context_setup')
  if template and template!=name:raise ValueError('profile template mismatch')
  if level!='moderate':raise ValueError('observed sources replay at captured/authored moderate scope')
 elif profile not in (None,'method'):raise ValueError('profile')
 else:
  available=['constant'] if level=='easy' else ['canonical'] if level=='hard' else [n for n,d in FAMILIES.items() if d['source']]
  name=template or rng.choice(available)
  if name not in available:raise ValueError('template outside level scope')
 if name=='context_setup':
  if field_type not in (None,'blank'):raise ValueError('blank field')
  return setup_record(seed,parameters,profile)
 if field_type not in (None,'radio'):raise ValueError('radio field')
 if parameters is not None and set(parameters)!=({'bounds','a'} if name=='constant' else {'bounds'}):raise ValueError('parameter keys: bounds, plus a for authored easy')
 a=parameters['a'] if parameters is not None and name=='constant' else rng.choice(range(2,10)) if name=='constant' else 2
 if name=='constant' and (type(a) is not int or a not in range(2,10)):raise ValueError('easy coefficient integer 2..9')
 if raw and parameters is None:parameters={'bounds':list(map(str,FAMILIES[name]['anchor']))}
 attempts=1 if parameters is not None else 500
 for _ in range(attempts):
  b=tuple(s.sympify(v,locals={'e':s.E}) for v in parameters['bounds']) if parameters is not None else sample(name,rng,level)
  # Raw evidence permits source anchors (easy-specific sampling restrictions never apply).
  guard(name,b,level)
  try:
   if raw:
    vals=source_bank(name,b)
    if any(s.simplify(u[0]-v[0])==0 for i,u in enumerate(vals) for v in vals[:i]):raise ValueError('whole observed-bank collision')
    values=[v[1] for v in vals]
    f=raw[':question/answer-fields'][0]
    correct=next((i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')),None)
    recipes=['opaque_observed_scalar_pattern']*len(values)
   else:
    vs,recipes=method_bank(name,b,a);values=list(map(tex,vs));correct=0
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('no eligible whole bank')
 problem=source_prompt(name,b,a)
 sol=None if raw and ':question/worked-solution' not in raw else solution(name,b,normal=not raw,a=a)
 params={'bounds':list(map(str,b))}
 if name=='constant':params['a']=a
 return package(level,name,params,problem,sol,values,correct,profile or 'method',seed,raw=raw,eligible=raw is None,recipes=recipes)

def markdown(r):
 q=r['question'];text=q[':question/problem']+'\n'
 for f in q.get(':question/answer-fields',[]):
  text+='\n'+f[':answer-field/type']+'\n'
  for a in f[':answer-field/choices']:text+='- $'+a[':answer/value']+'$\n'
 if ':question/worked-solution' in q:text+='\n'+q[':question/worked-solution']+'\n'
 return text

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186133931-source-policy.json'))

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 records=[generate(l,a.seed+i,a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n'.join(markdown(r) for r in records))
