#!/usr/bin/env python3
"""Gradient of three-variable functions; local step 3–7 generator, basis 1356.

Observed moderate families retain complete source formal-partial, chain/product,
reduction, vector-component and evaluation stages. Translated argument components
are authored same-method extensions, NOT recovered source sampling parameters.
Opaque historical numerical banks are public evidence profiles, ineligible for
normal practice. All normal profiles contain five complete method-derived values.
Easy and hard are authored curriculum-anchored workload bands; see classification.
No plots, database access, registration, engine changes, or transactions.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
KP=SOURCE['record']; KP_ID=KP[':db/id']; VERSION='three-gradient-v1'
SPEC=importlib.util.spec_from_file_location('gradient_display_parser',ROOT/'display_parser.py')
P=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(P)
x,y,z=P.x,P.y,P.z;VARS=(x,y,z);BASIS=(P.i,P.j,P.k)
FAMILIES=('sqrt_product','root_log','log_point','product_log','power_exp','variable_power','expcos_point','exp_sin','composite_log','sine_point')
ORIGINALS=dict(zip(FAMILIES,KP[':knowledge-point/questions']))
POINTS={'log_point':(s.Integer(2),s.Integer(3),s.Integer(1)), 'expcos_point':(s.Rational(1,2),s.Integer(1),s.pi),'sine_point':(s.Integer(1),s.Integer(-1),s.pi)}
OPAQUE={'sqrt_product','log_point','product_log','expcos_point','sine_point'}
TEMPLATES={'easy':('polynomial',),'moderate':FAMILIES,'hard':('quotient',)}
NAMESPACE=uuid.UUID('54ca58b5-2037-4a87-b85f-10cb38ae7792')
def uid(v):return str(uuid.uuid5(NAMESPACE,str(v)))
def mathematically_equal(a,b):
 d=s.sympify(a)-s.sympify(b)
 if d==0:return True
 # Exact positive rational counterexamples establish inequality cheaply;
 # only equality or inconclusive cases require general simplification.
 value=d.subs({x:5,y:6,z:7})
 if value.is_zero is False:return False
 return s.simplify(d)==0
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def tex(e):return s.latex(e).replace(r'\log',r'\ln')
def clean(t):return re.sub(r'\\text\{[^}]*\}','',t).replace(r'\mathbf','').replace('⁡','')
def parse(t):return P.scalar(clean(t))
def vecparse(t):
 a=s.expand(parse(t));out=tuple(a.coeff(b) for b in BASIS)
 if s.simplify(a-sum(t*b for t,b in zip(out,BASIS)))!=0:raise ValueError('Not a complete vector: '+t)
 return out

def vect(v):
 # Always explicit groups prevent adjoining numeric factors and subtraction signs.
 return '+'.join('('+tex(t)+r')\,\mathbf '+b for t,b in zip(v,'ijk')).replace('+-','-')

def formula_from_prompt(t):
 a=re.search(r'[fgh]\(x,y,z\)\s*=([^$]+)',t)
 if not a:raise ValueError('Function absent from prompt')
 return parse(a[1].strip().rstrip('.,'))

def argument_slots(t,shifts):
 """Transform complete scalar/vector math components, protecting ONLY commands.

No prose, function argument tuples, basis names or partial-operator denominators
are processed here. The caller splits those semantic components beforehand.
"""
 commands=[]
 def protect(m):commands.append(m[0]);return '@'+str(len(commands)-1)+'@'
 t=re.sub(r'\\[A-Za-z]+(?:\{(?:ln|cos|sin)\})?',protect,t)
 # A coordinate is an atom, including when it was a bare exponent or ln input.
 t=re.sub('[xyz]',lambda m: m[0] if shifts['xyz'.index(m[0])]==0 else '{('+m[0]+('+' if shifts['xyz'.index(m[0])]>0 else '-')+str(abs(shifts['xyz'.index(m[0])]))+')}',t)
 for i,c in enumerate(commands):t=t.replace('@'+str(i)+'@',c)
 return t

def translate_solution(t,shifts):
 if not any(shifts):return t  # Identity of the same renderer; no literal question branch.
 def block(m):
  b=m[1];parts=b.split(r'\\');out=[]
  for row in parts:
   if '& =' not in row:raise ValueError('Unknown aligned shape')
   left,right=row.split('& =',1)
   if r'\frac{∂}{∂' in right:
    k=right.index('}(')+2;right=right[:k]+argument_slots(right[k:],shifts)
   elif re.search(r'\{[fgh]\}_\{[xyz]\}\(x,y,z\)',right):pass
   else:right=argument_slots(right,shifts)
   out.append(left+'& ='+right)
  return r'\begin{aligned}'+r'\\'.join(out)+r'\end{aligned}'
 return re.sub(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',block,t,flags=re.S)

def point_string(p,spaces=False):
 return ','.join(tex(t) for t in p)+( ' ' if spaces else '')

def source_atom(v):
 t=tex(v).replace('- ','-')
 return t+' ' if v in (s.pi,-s.pi) else t

def coefficient(v,basis,spacing=r'\,'):
 sign='-' if s.sympify(v).could_extract_minus_sign() else ''
 absval=-v if sign else v
 return sign+('' if absval==1 else source_atom(absval))+spacing+basis

def point_solution(family,p,raw):
 """Numeric masks always compute all rows, including original-parameter replay."""
 q=ORIGINALS[family];sol=q[':question/worked-solution'];a,b,c=p
 ta,tb,tc=map(source_atom,p)
 if family=='log_point':
  sol=sol.replace('2,3,1',point_string(p))
  replacements={'2':ta,'3':tb,'1':tc}
  sol=re.sub(r'\\frac\{1\}\{2\\cdot ([123])\}',lambda m:r'\frac{1}{2\cdot '+replacements[m[1]]+'}',sol)
  final=historic_vector((1/(2*a),1/(2*b),1/(2*c)))+'.'
  sol=sol.replace(r'\frac{1}{4}\text{ }i+\frac{1}{6}\text{ }j+\frac{1}{2}\text{ }k.',final)
 elif family=='sine_point':
  sol=sol.replace(r'1,-1,\pi ',point_string(p,True))
  co=s.cos(a*b*c);trig=r'\operatorname{cos}⁡('+source_atom(a*b*c)+')'
  substituted='('+tb+')('+tc+')'+trig+r'\text{ }i+('+ta+')('+tc+')'+trig+r'\text{ }j+('+ta+')('+tb+')'+trig+r'\text{ }k'
  def product(v,t):
   st='('+source_atom(t)+')'
   if v==-1:return '-'+st
   if v==1:return st
   sv=source_atom(v)
   return ('('+sv+')' if s.sympify(v).could_extract_minus_sign() else sv)+st
  mid='+'.join(product(v,co)+r'\text{ }'+basis for v,basis in zip((b*c,a*c,a*b),'ijk')).replace('+-','-')
  final=historic_vector(tuple(s.simplify(v*co) for v in (b*c,a*c,a*b)))
  originals=[r'(-1)(\pi )\operatorname{cos}⁡(-\pi )\text{ }i+(1)(\pi )\operatorname{cos}⁡(-\pi )\text{ }j+(1)(-1)\operatorname{cos}⁡(-\pi )\text{ }k',r'(-\pi )(-1)\text{ }i+\pi (-1)\text{ }j-(-1)\text{ }k',r'\pi \text{ }i-\pi \text{ }j+\text{ }k']
  for old,new in zip(originals,(substituted,mid,final)):sol=sol.replace(old,new)
 elif family=='expcos_point':
  sol=sol.replace(r'\frac{1}{2},1,\pi ',point_string(p,True))
  arg=tb+tc if c in (s.pi,-s.pi) and c>0 else '('+tb+')('+tc+')'
  trc=r'\operatorname{cos}⁡('+arg+')';trs=r'\operatorname{sin}⁡('+arg+')'
  fac='{e}^{('+str(a)+')('+tb+')}'
  cj=tc if c>0 else '('+tc+')'
  substituted=fac+'('+tb+trc+r'\,i+('+ta+trc+'-'+cj+trs+r')\,j-'+tb+trs+r'\,k)'
  co,si=s.cos(b*c),s.sin(b*c);E=exponential_style(a*b)
  mid=E+'('+coefficient(b*co,'i',spacing='')+coefficient(a*co-c*si,'j')+r'-0\,k)'
  # For positive cosine, positive coefficient j needs its visible separator.
  mid=mid.replace('i'+coefficient(a*co-c*si,'j'),'i'+('+' if a*co-c*si>0 else '')+coefficient(a*co-c*si,'j'))
  common_sign='-' if co==-1 else ''
  bi='' if b==1 else source_atom(b)
  final=common_sign+E+'('+bi+'i+'+source_atom(a)+r'\,j).'
  originals=[r'{e}^{(1/2)(1)}(1\operatorname{cos}⁡(1\pi )\,i+(\frac{1}{2}\operatorname{cos}⁡(1\pi )-\pi \operatorname{sin}⁡(1\pi ))\,j-1\operatorname{sin}⁡(1\pi )\,k)',r'\sqrt{e}(-i-\frac{1}{2}\,j-0\,k)',r'-\sqrt{e}(i+\frac{1}{2}\,j).']
  for old,new in zip(originals,(substituted,mid,final)):sol=sol.replace(old,new)
 return sol if raw else repair(sol)

def repair(sol):
 # Three observed point families mislabel the general vector's y/z components.
 for name in 'fh':
  for space in (r'\text{ }',r'\,'):
   sol=sol.replace('{'+name+r'}_{x}(x,y,z)'+space+'j','{'+name+r'}_{y}(x,y,z)'+space+'j').replace('{'+name+r'}_{x}(x,y,z)'+space+'k','{'+name+r'}_{z}(x,y,z)'+space+'k')
 return sol

def method_bank(family,F,gradient,p,shifts=(0,0,0)):
 """Whole banks, selected before parameters; errors follow the printed method."""
 if family=='log_point':
  a,b,c=p;return [gradient,(1/a,1/b,1/c),(-1/(2*a),1/(2*b),1/(2*c)),(1/(2*a),-1/(2*b),1/(2*c)),(1/(2*a),1/(2*b),-1/(2*c))]
 if family=='expcos_point':
  a,b,c=p;co,si=s.cos(b*c),s.sin(b*c);E=s.exp(a*b);v=(b*co,a*co-c*si,-b*si)
  return [gradient,v,tuple(s.exp(2*a*b)*d for d in v),tuple(-d for d in gradient),(E*b*co,E*(b*co-c*si),-E*b*si)]
 if family=='sine_point':return [gradient,*[tuple(-d if i==j else d for j,d in enumerate(gradient)) for i in range(3)],tuple(-d for d in gradient)]
 if family=='sqrt_product':
  # Removing the outer 1/2 factor; treating square root as identity;
  # exchanging reciprocal coordinates with direct ones; omit x chain factor.
  u,v,w=[a+d for a,d in zip(VARS,shifts)];r=s.sqrt(u*v*w)
  return [gradient,tuple(2*d for d in gradient),(v*w/2,u*w/2,u*v/2),(r*u/2,r*v/2,r*w/2),(1/(2*r),r/(2*v),r/(2*w))]
 # For other symbolic families the entire observed algebraic bank is defensible
 # except product_log's first option: use omitted held-coordinate differentiation.
 if family=='product_log':return [gradient,(F,F,gradient[2]),(gradient[0],F,gradient[2]),(gradient[0],gradient[1],F),(gradient[1],gradient[0],gradient[2])]
 raise ValueError('No authored method bank')

def historic_vector(v,unit_last_text=True):
 out=''
 for j,(d,basis) in enumerate(zip(v,'ijk')):
  d=s.simplify(d)
  if d==0:continue
  neg=d.could_extract_minus_sign();v=-d if neg else d
  sign='-' if neg else ('+' if out else '')
  coefficient='' if v==1 else tex(v)
  if v==s.pi:coefficient+=' '
  spacing=r'\text{ }' if not (j==2 and v==1 and not unit_last_text) else ''
  out+=sign+coefficient+spacing+basis
 return out

def exponential_style(e):
 return r'\sqrt{e}' if e==s.Rational(1,2) else tex(s.exp(e))

def numeric_raw_display(family,p,values):
 a,b,c=p
 if family=='log_point':return [historic_vector(v,unit_last_text=False) for v in values]
 if family=='sine_point':return [historic_vector(v) for v in values]
 if family=='expcos_point':
  E=exponential_style(a*b);E2=exponential_style(2*a*b)
  bi='' if b==1 else tex(b)
  aj=tex(a)+r'\,j';cj=tex(c)+' '+r'\,j'
  return [E2+'('+bi+'i-'+aj+')',E2+'('+bi+'i-'+aj+'+k)',E+'(-'+bi+'i+'+cj+'-k)','-'+E+'('+bi+'i+'+cj+'-k)','-'+E+'('+bi+'i+'+aj+')']
 raise ValueError(family)

def numeric_raw_bank(family,p):
 a,b,c=p
 if family=='log_point':return [(1/a,1/b,1/c),(1/a,s.sqrt(a*b)/(a*b),-s.sqrt(a)/(a*c)),(1/(2*a),1/(2*b),1/(2*c)),(2*a,2*b,-2*c),(1/a,1/b,-1/c)]
 if family=='sine_point':return [(b*c*s.cos(a*b*c),a*c*s.cos(a*b*c),a*b*s.cos(a*b*c)),(c,c,c),(c,c,1),(1,-c,1),(-c,c,1)]
 if family=='expcos_point':
  E=s.exp(a*b);E2=s.exp(2*a*b)
  return [(E2*b,-E2*a,0),(E2*b,-E2*a,E2),(E*(-b),E*c,-E),(-E*b,-E*c,E),(-E*b,-E*a,0)]
 raise ValueError(family)

def observed(family,parameters,profile):
 raw=profile=='observed_raw';q=ORIGINALS[family]
 if family in POINTS:
  if set(parameters)-{'point'}:raise ValueError('Unknown parameters')
  p=tuple(s.sympify(v,locals={'pi':s.pi}) for v in parameters.get('point',POINTS[family]));shifts=(0,0,0)
  if len(p)!=3:raise ValueError('Point must have three coordinates')
  if family=='log_point' and any(not v.is_Integer or not 1<=v<=6 for v in p):raise ValueError('Log point coordinates must be integers 1..6')
  if family=='sine_point' and (p[0] not in (-2,-1,1,2) or p[1] not in (-2,-1,1,2) or s.simplify(p[0]*p[1]*p[2]/s.pi) not in (-2,-1,1,2)):raise ValueError('Sine point must have familiar nonzero multiple-pi product')
  if family=='expcos_point' and (p[0] not in (s.Rational(1,2),s.Rational(1,3),1,2) or p[1] not in (1,2,3) or p[0]==p[1] or s.simplify(p[1]*p[2]/s.pi) not in (-2,-1,1,2)):raise ValueError('Expcos point outside bounded familiar-angle workload')
  F=formula_from_prompt(q[':question/problem']);G=tuple(s.diff(F,v) for v in VARS);gradient=tuple(s.simplify(d.subs(dict(zip(VARS,p)))) for d in G)
  problem=q[':question/problem'];old=POINTS[family]
  oldtext={'log_point':'2,3,1','sine_point':r'1,-1,\pi ','expcos_point':r'\frac{1}{2},1,\pi '}[family]
  problem=problem.replace(oldtext,point_string(p,family!='log_point'))
  solution=point_solution(family,p,raw)
  if raw:
   vals=numeric_raw_bank(family,p)
   displays=numeric_raw_display(family,p,vals)
  else:vals=method_bank(family,F,gradient,p);displays=[vect(v) for v in vals]
  params={'point':[str(v) for v in p]}
 else:
  if set(parameters)-{'shifts'}:raise ValueError('Unknown parameters')
  shifts=tuple(parameters.get('shifts',(0,0,0)));p=None
  if len(shifts)!=3 or any(type(d)is not int or abs(d)>3 for d in shifts):raise ValueError('Three integer shifts, absolute value <=3 required')
  originalF=formula_from_prompt(q[':question/problem']);sub=dict(zip(VARS,[v+d for v,d in zip(VARS,shifts)]));F=originalF.subs(sub,simultaneous=True);gradient=tuple(s.diff(F,v) for v in VARS)
  # Only the complete function body is a slot. Labels remain f(x,y,z).
  m=re.search(r'([fgh]\(x,y,z\)\s*=)([^$]+)',q[':question/problem']);problem=q[':question/problem'][:m.start(2)]+argument_slots(m[2],shifts)+q[':question/problem'][m.end(2):]
  solution=translate_solution(q[':question/worked-solution'],shifts)
  if not raw:solution=repair(solution)
  if raw or family not in OPAQUE:
   displays=[argument_slots(a[':answer/value'],shifts) for a in q[':question/answer-fields'][0][':answer-field/choices']];vals=[vecparse(v) for v in displays]
  else:
   vals=method_bank(family,F,gradient,p,shifts);displays=[vect(v) for v in vals]
  params={'shifts':list(shifts)}
 expected=s.Matrix(gradient)
 correct=[i for i,v in enumerate(vals) if all(mathematically_equal(a,b) for a,b in zip(v,expected))]
 if len(correct)!=1:raise ValueError('Complete bank has ambiguous/absent correct vector')
 for i,v in enumerate(vals):
  for other in vals[:i]:
   if all(mathematically_equal(a,b) for a,b in zip(v,other)):raise ValueError('Reject whole bank: equivalent vectors')
 if any(s.sympify(t).has(s.zoo,s.nan,s.oo) for v in vals for t in v):raise ValueError('Invalid bank')
 return problem,solution,displays,correct[0],params,F,p

# EASY: authored polynomial partials, one monomial contribution per component.
# Three held-coordinate formal rows + power rules + vector assembly, no chains.
def easy(parameters):
 if set(parameters)-{'coefficients','powers'}:raise ValueError('Unknown easy parameter')
 a=tuple(parameters.get('coefficients',(1,2,3)));n=tuple(parameters.get('powers',(2,2,2)))
 if len(a)!=3 or any(type(v)is not int or v==0 or abs(v)>5 for v in a):raise ValueError('Nonzero integer coefficients with |a|<=5')
 if len(n)!=3 or any(type(v)is not int or v not in (2,3) for v in n):raise ValueError('Easy powers 2 or 3')
 terms=[c*v**k for c,v,k in zip(a,VARS,n)];F=sum(terms);G=tuple(s.diff(F,v) for v in VARS)
 rows=[]
 for v,d in zip(VARS,G):
  rhs='+'.join('('+tex(s.diff(t,v))+')' for t in terms)
  rows.extend([r'{g}_{'+str(v)+r'}(x,y,z) & =\frac{∂}{∂'+str(v)+'}('+tex(F)+')',r' & ='+rhs,r' & ='+tex(d)])
 solution='First, we find the partial derivatives:\n\n'+aligned(rows)+'\n\nTherefore, the gradient is\n\n'+aligned([formal('g'),r' & ='+vect(G)])
 bank=[G,tuple(t/v for t,v in zip(terms,VARS)),*[(tuple(-d if i==j else d for j,d in enumerate(G))) for i in range(3)]]
 return 'Find $∇g(x,y,z)$ given that $g(x,y,z)='+tex(F)+'.$',solution,[vect(v) for v in bank],0,{'coefficients':list(a),'powers':list(n)},F,None

# HARD: authored quotient partials; two nonzero numerator/denominator terms in
# every coordinate quotient, then substitution at a signed small integer point.
# Canonical evaluation and prerequisite quotient rule, no gradient-properties KP.
def hard(parameters):
 if set(parameters)-{'coefficients','point'}:raise ValueError('Unknown hard parameter')
 a,b,c=parameters.get('coefficients',(1,2,1));rawpoint=parameters.get('point',(1,2,1))
 if any(isinstance(v,float) or not s.sympify(v).is_Integer for v in rawpoint):raise ValueError('Hard coordinates must be exact integers')
 p=tuple(map(s.Integer,rawpoint))
 if any(type(v)is not int or not 1<=abs(v)<=3 for v in (a,b,c)):raise ValueError('Hard coefficient absolute values 1..3')
 if len(p)!=3 or any(v==0 or abs(v)>3 for v in p):raise ValueError('Hard coordinates nonzero integers |v|<=3')
 N=a*x*y*z;D=b*x+c*y+z;F=N/D;subs=dict(zip(VARS,p))
 if D.subs(subs)==0:raise ValueError('Zero denominator')
 G=tuple(s.diff(F,v) for v in VARS);rows=[];formal_components=[]
 for v,g in zip(VARS,G):
  dn=s.diff(N,v);dd=s.diff(D,v);numer=D*dn-N*dd
  # Neither numerator contribution may vanish after substitution.
  if D.subs(subs)*dn.subs(subs)==0 or N.subs(subs)*dd==0 or g.subs(subs)==0:raise ValueError('Hard workload degeneracy')
  quotient=r'\frac{('+tex(D)+')('+tex(dn)+')-('+tex(N)+')('+tex(dd)+')}{('+tex(D)+')^2}'
  rows.extend([r'{g}_{'+str(v)+r'}(x,y,z) & =\frac{∂}{∂'+str(v)+'}('+tex(F)+')',r' & ='+quotient,r' & ='+tex(s.factor(g))])
  formal_components.append(quotient)
 E=tuple(s.simplify(g.subs(subs)) for g in G)
 subrow=vect(tuple(s.sympify(g).subs(subs) for g in G))
 # Keep the individually substituted numerator/denominator products unevaluated.
 eval_components=[]
 for v in VARS:
  dn=s.diff(N,v);dd=s.diff(D,v)
  eval_components.append(r'\frac{('+tex(D.subs(subs))+')('+tex(dn.subs(subs))+')-('+tex(N.subs(subs))+')('+tex(dd)+')}{('+tex(D.subs(subs))+')^2}')
 evector='+'.join('('+d+r')\,\mathbf '+v for d,v in zip(eval_components,'ijk'))
 solution='First, we find the partial derivatives:\n\n'+aligned(rows)+'\n\nTherefore, the gradient is\n\n'+aligned([formal('g'),r' & ='+vect(G),r'∇g('+point_string(p)+r') & ='+evector,r' & ='+subrow,r' & ='+vect(E)])
 # Quotient numerator plus instead of minus; omit D^2; drop numerator
 # derivative contribution; differentiate denominator as constant.
 errors=[tuple(((D*s.diff(N,v)+N*s.diff(D,v))/D**2).subs(subs) for v in VARS),tuple((s.diff(N,v)*D-N*s.diff(D,v)).subs(subs) for v in VARS),tuple((-N*s.diff(D,v)/D**2).subs(subs) for v in VARS),tuple((s.diff(N,v)/D).subs(subs) for v in VARS)]
 bank=[E,*errors]
 if any(all(mathematically_equal(u,v) for u,v in zip(one,two)) for i,one in enumerate(bank) for two in bank[:i]):raise ValueError('Reject whole quotient bank')
 return 'Evaluate $∇g(x,y,z)$ at the point $('+point_string(p)+')$ if $g(x,y,z)='+tex(F)+'.$',solution,[vect(v) for v in bank],0,{'coefficients':[a,b,c],'point':[str(v) for v in p]},F,p

def aligned(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def formal(name):return '∇'+name+r'(x,y,z) & ='+ '+'.join('{'+name+'}_{'+v+r'}(x,y,z)\,\mathbf '+b for v,b in zip('xyz','ijk'))

def sample(level,family,rng):
 if level=='easy':return {'coefficients':[rng.choice([i for i in range(-5,6) if i]) for _ in VARS],'powers':[rng.choice((2,3)) for _ in VARS]}
 if level=='hard':return {'coefficients':[rng.choice((-3,-2,-1,1,2,3)) for _ in VARS],'point':[rng.choice((-3,-2,-1,1,2,3)) for _ in VARS]}
 if family=='log_point':return {'point':[rng.randint(1,6) for _ in VARS]}
 if family=='sine_point':
  a,b=rng.choice((-2,-1,1,2)),rng.choice((-2,-1,1,2));return {'point':[a,b,str(rng.choice((-2,-1,1,2))*s.pi/(a*b))]}
 if family=='expcos_point':
  a,b=rng.choice((s.Rational(1,2),s.Rational(1,3),s.Integer(1),s.Integer(2))),rng.randint(1,3)
  return {'point':[str(a),b,str(rng.choice((-2,-1,1,2))*s.pi/b)]}
 return {'shifts':[rng.randint(-3,3) for _ in VARS]}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in TEMPLATES:raise ValueError('Difficulty must be easy, moderate or hard')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio field supported')
 rng=random.Random(seed)
 if template is None:
  eligible=list(TEMPLATES[level])
  if level=='moderate' and profile=='observed_method':eligible=[t for t in eligible if t not in OPAQUE]
  if level=='moderate' and profile=='authored_method':eligible=[t for t in eligible if t in OPAQUE]
  template=rng.choice(eligible)
 if template not in TEMPLATES[level]:raise ValueError('Template outside requested workload')
 profile=profile or ('authored_method' if template in OPAQUE or level!='moderate' else 'observed_method')
 if profile not in ('observed_raw','observed_method','authored_method'):raise ValueError('Unknown whole bank')
 if level!='moderate' and profile!='authored_method':raise ValueError('Authored levels only use authored_method')
 if level=='moderate' and template in OPAQUE and profile=='observed_method':raise ValueError('Opaque historical bank is evidence only')
 if level=='moderate' and template not in OPAQUE and profile=='authored_method':raise ValueError('Use the complete defensible observed_method bank')
 for attempt in range(1000):
  inputs=parameters if parameters is not None else sample(level,template,rng)
  try:
   data=easy(inputs) if level=='easy' else hard(inputs) if level=='hard' else observed(template,inputs,profile)
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('No valid whole-bank instance')
 problem,solution,displays,correct,params,F,p=data
 # Actual rendered content, not parameter aliases/seed, establishes identity.
 identity=digest({'version':VERSION,'level':level,'problem':problem,'solution':solution,'bank':sorted(displays),'correct':displays[correct]})
 fieldid=uid(identity+'/selection');answers=[{':answer/id':uid(fieldid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in displays];correctid=answers[correct][':answer/id'];rng.shuffle(answers)
 q={':question/id':uid(identity),':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fieldid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correctid]}]}
 mathematical=digest({'level':level,'function':s.srepr(F),'evaluated_gradient':None if p is None else [s.srepr(s.simplify(s.diff(F,v).subs(dict(zip(VARS,p))))) for v in VARS],'requested':'three held-coordinate partials and gradient'})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':template,'parameters':params,'bank_profile':profile,'profile_origin':('historical_evidence' if profile=='observed_raw' else 'authored_method_bank' if profile=='authored_method' else 'observed_expression_operations'),'evidence_only':profile=='observed_raw','eligible_for_learning':profile!='observed_raw','seed':seed,'mathematical_fingerprint':mathematical,'content_identity':identity,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_ids':[] if level!='moderate' else [ORIGINALS[template][':question/id']],'scope':'first held-coordinate partial derivatives only','domain':domain(template,params),'runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'plots':[]}}

def domain(template,params):
 if template=='quotient':return 'Denominator nonzero at the stated point; work in a neighborhood where it remains nonzero.'
 if template in ('sqrt_product','root_log','log_point','product_log','variable_power','composite_log'):return 'Work on the open positive-argument component (all translated x,y,z are positive); roots and logarithms are real.'
 return 'Real coordinates; the displayed function and its first partial derivatives exist.'

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(record):
 q=record['question'];rows=[q[':question/problem'],'']
 for f in q.get(':question/answer-fields',[]):rows += [str(i+1)+'. $'+a[':answer/value']+'$' for i,a in enumerate(f[':answer-field/choices'])]
 rows += ['',q.get(':question/worked-solution','')];return '\n'.join(rows)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=(*TEMPLATES,'all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=('markdown','json'),default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
 if args.count<1:parser.error('count must be positive')
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (TEMPLATES if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
