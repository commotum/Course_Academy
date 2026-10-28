#!/usr/bin/env python3
"""Exact, deterministic product-rule questions (math snapshot basis 8693).

The observed easy scalar products are retained despite overlap with the sibling
KP. Moderate dot and hard cross products retain their source workload. Banks are
whole recipes; their uncertain authoring interpretations are documented in the
adjacent extraction report. No source payload or answer lookup is used here.
"""
import argparse
import functools
import hashlib
import json
import random
import uuid
from pathlib import Path
import sympy as sp
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP_ID=17592186115393
KP_UUID='d54a6dbe-42cb-5614-ae0b-611de1719b45'
TITLE='Using the Product Rules for Differentiation'
VERSION='2.0.0'
t=sp.Symbol('t', real=True)
SOURCE={'database':'math','basis':8693,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
# The complete source bank is bound to each template. A recipe never pools options.
TEMPLATES={
 'scalar_log':('easy','q-128586','tuple',dict(c=2,n=2,m=1)),
 'scalar_power':('easy','q-128587','tuple',dict(a=1,b=1,c=2,p=1,q=2,r=3,n=3)),
 'scalar_exp':('easy','q-128894','tuple',dict(a=1,b=2,s=1)),
 'scalar_base':('easy','q-33446','tuple',dict(base=2,s=1,c=1)),
 'dot_polynomial':('moderate','q-32298','basis',dict(a=20,b=-2,c=2,d=5)),
 'dot_self_cubic':('moderate','q-32804','basis',dict(a=2,b=-2,c=1,d=5)),
 'dot_self_shifted':('moderate','q-32835','tuple',dict(a=1,h=1,b=2,c=1,k=1)),
 'dot_self_evaluate':('moderate','q-32837','basis',dict(a=1,h=1,b=1,k=2,c=4,x=0)),
 'dot_log_reciprocal':('moderate','q-33336','basis',dict(a=1,b=1,c=1,d=1,e=1,h=1)),
 'cross_matrix':('hard','q-32353','matrix',dict(a=3,b=4,c=8,d=2,e=-2,h=5)),
 'cross_monomials':('hard','q-128896','tuple',dict(a=1,b=5,c=1,d=1,e=1,h=1,n=4,p=2,q=3)),
 'cross_shifted':('hard','q-32347','tuple',dict(a=6,b=2,c=6,d=3,e=3,h=4,k=1)),
 'cross_self':('hard','q-32836','tuple',dict(a=1,b=1,c=1,d=1,e=1,h=1)),
}
# q-32353 has a complete first field and solution. Its extra incomplete field
# does not exclude this eligible standalone matrix-form family.
BANK_PROFILES={name+'_observed':{'template':name,'origin':'observed','source_id':row[1]} for name,row in TEMPLATES.items()}
BANK_PROFILES.update({name+'_authored':{'template':name,'origin':'authored','source_id':None} for name in TEMPLATES})

SOURCE_IDS={'q-32298': 'a209f44d-4003-53ab-9d12-642d62514eb3', 'q-32353': '54437c76-a800-5517-9d6f-6a2f64f033aa', 'q-128586': '995d1b63-3fd5-54e1-bbec-560efe7ac735', 'q-128587': 'e2c98f03-8eb1-5c14-ba1a-38fe2722976d', 'q-128894': 'd768288b-91a5-51ed-b29b-7650008bff18', 'q-32804': '19486880-810b-5bd6-a22c-f282191bb018', 'q-32835': '38bbc30d-2715-5fd5-8cc3-adae49e8b272', 'q-32837': '829808f0-e345-5eeb-99ad-5982ddad6fb7', 'q-33336': '8a9de11b-dc85-5ae6-9285-a0d6cc055460', 'q-33446': '360e7d39-e582-5724-9fad-4481a2f3b45b', 'q-128896': 'c21f1368-688b-50ed-bde8-7422d801bdbd', 'q-32347': '5c0ab63c-e0ff-5937-9e2f-94c308127204', 'q-32836': 'd806e973-4767-5c33-a683-2e2483aec09e'}
class SampleRejected(ValueError): pass

@functools.lru_cache(maxsize=16384)
def simp(x):
 # Collect polynomial/rational component arithmetic without changing operator
 # inputs, splitting exponentials, or rewriting numeric logarithms.
 return sp.expand(x, power_exp=False, power_base=False, log=False)

def vec(*x): return sp.Matrix(x)
def tex(x):
 return sp.latex(simp(x)).replace(r'\log',r'\ln').replace(r'\left', '').replace(r'\right','')
def vector(v,style='tuple'):
 if style=='matrix': return r'\begin{bmatrix}'+r' \\ '.join(tex(x) for x in v)+r'\end{bmatrix}'
 if style=='bmatrix': return r'\begin{bmatrix}'+r' \\ '.join(tex(x) for x in v)+r'\end{bmatrix}'
 if style=='basis':
  terms=[]
  for x,u in zip(v,'ijk'):
   if x==0: continue
   z=tex(x)
   if x==1: z=''
   elif x==-1: z='-'
   elif len(sp.Add.make_args(x))>1: z='('+z+')'
   z+=r'\,'+u
   terms.append(('+' if terms and not z.startswith('-') else '')+z)
  return ''.join(terms) or '0'
 return '⟨'+r',\,'.join(tex(x) for x in v)+'⟩'
def block(x):return '\n\n$$\n'+x+'\n$$'
def aligned(rows):return r'\begin{aligned}'+r' \\ '.join(lhs+' & ='+rhs for lhs,rhs in rows)+r'\end{aligned}'
def dvec(v,style):
 d=lambda x:r'\frac{\text{d}}{\text{d}t}('+tex(x)+')'
 if style=='matrix':return r'\begin{bmatrix}'+r' \\ '.join(d(x) for x in v)+r'\end{bmatrix}'
 if style=='basis':return '+'.join(d(x)+r'\,'+u for x,u in zip(v,'ijk'))
 return '⟨'+r',\,'.join(d(x) for x in v)+'⟩'
def determinant(u,v):return r'\begin{vmatrix}i & j & k \\ '+ ' & '.join(tex(x) for x in u)+r' \\ '+' & '.join(tex(x) for x in v)+r'\end{vmatrix}'
def minors(u,v):
 def minor(i,j):return r'\begin{vmatrix}'+tex(u[i])+' & '+tex(u[j])+r' \\ '+tex(v[i])+' & '+tex(v[j])+r'\end{vmatrix}'
 return minor(1,2)+'i-'+minor(0,2)+'j+'+minor(0,1)+'k'
def dot_terms(u,v):return '+'.join('('+tex(a)+')('+tex(b)+')' for a,b in zip(u,v))
def sexpr(x):return [sp.srepr(y) for y in x] if isinstance(x,sp.MatrixBase) else sp.srepr(x)
def grouped(v,style):
 value=vector(v,style)
 return '('+value+')' if style=='basis' else value
def equivalent(a,b):
 if isinstance(a,sp.MatrixBase) and isinstance(b,sp.MatrixBase):return a.shape==b.shape and all(equivalent(x,y) for x,y in zip(a,b))
 if isinstance(a,sp.MatrixBase) or isinstance(b,sp.MatrixBase):return False
 delta=sp.expand(a-b)
 if delta==0:return True
 if abs(complex(delta.subs(t,2).evalf()))>1e-9:return False
 return sp.simplify(delta)==0

# EASY — the four observed scalar-product structures, no level progression.
def build_easy(name,p):
 if name=='scalar_log':
  c,n,m=p['c'],p['n'],p['m']; f=vec(sp.log(t),t**n,t**m); u=c*t
  C=c*vec(sp.log(t)+1,(n+1)*t**n,(m+1)*t**m)
  W=[c*vec(sp.log(t),(n+1)*t**n,t**(sp.Rational(1,2)*m)),vec(sp.log(t)+1,t**m,(n+1)*t**m),c*vec(sp.log(t)+1,(n+1)*t**m,t**n),vec(sp.log(t),(n+1)*t**n,t**n)]
  labels=['omit_log_constant_and_halve_last_exponent','omit_scalar_and_use_last_power_in_both_slots','exchange_last_two_power_structures','omit_scalar_and_log_constant_use_second_power_last']
 elif name=='scalar_power':
  a,b,c,P,Q,R,n=(p[k] for k in ('a','b','c','p','q','r','n')); f=vec(a*t**P,b*t**Q,c*t**R);u=t**n
  C=vec(a*(n+P)*t**(n+P-1),b*(n+Q)*t**(n+Q-1),c*(n+R)*t**(n+R-1))
  W=[vec(c*t**P,b*(n+Q)*t**n,n*R*t**(n+R-2)),vec(t**(n+P),t**n,t**Q),vec(c*t**P,b*(n+Q)*t**(n+Q-1),n*t**(n+R-1)),vec(C[0],b*(n+Q)*t**Q,n*R*t**(n+R-2))]
  labels=['source_mixed_power_and_coefficient_A','source_descending_power_bank','source_mixed_power_and_coefficient_B','retain_first_alter_second_and_third']
 elif name=='scalar_exp':
  a,b,s=p['a'],p['b'],p['s']; f=vec(sp.exp(a*t+s),sp.exp(-a*t),sp.exp(b*t));u=sp.exp(a*t);E=sp.exp(2*a*t+s);F=sp.exp((a+b)*t)
  C=vec(2*a*E,0,(a+b)*F)
  W=[vec(2*a*sp.exp(a*t+s),2*a,2*b*F),vec(a*E,0,-(a+b)*F),vec(a*E,-2*a,b*F),vec(a*E,a,b*F)]
  labels=['leave_first_exponent_uncombined_and_double_second_rate','omit_first_product_term_reverse_last','omit_scalar_derivative_and_miscancel_middle','omit_first_product_term_and_leave_middle_constant']
 else:
  B,s,c=p['base'],p['s'],p['c'];L=sp.log(B);f=vec(B**t,B**(t+s),B**(2*t)+c);u=B**(-t)
  C=vec(0,0,(B**(2*t)-c)*L/B**t)
  W=[vec(L,L,(B**(2*t)-c)*L),vec(0,-L/B**t,0),vec(B**t,0,C[2]),vec(0,L,-c*L/B**t)]
  labels=['drop_scalar_denominator_and_fail_first_cancellations','residual_middle_only','retain_first_exponential','middle_log_and_constant_only_last']
 return f,u,C,W,labels

# MODERATE — dot products, including observed first/second derivatives/evaluation.
def build_moderate(name,p):
 if name=='dot_polynomial':
  a,b,c,d=(p[k] for k in 'abcd'); f=vec(a*t,b*t,c+d*t);g=vec(t**3,t,t**2+t);C=4*a*t**3+3*d*t**2+2*(b+c+d)*t+c
  W=[4*a*t**3+(2*d+1)*t**2+(2*d+c)*t+c,4*a*t**3+3*c*t**2+2*(b+c+d)*t+c,3*a*t**3+3*d*t**2+2*(c+d)*t+c,3*a*t**3+(d+c)*t**2+2*(b+c+d)*t+c]
 elif name=='dot_self_cubic':
  a,b,c,d=(p[k] for k in 'abcd');f=vec(a*t**3,b*t,c+d*t**2);g=None;K=b*b+2*c*d;C=15*a*a*t**4+6*d*d*t**2+K
  W=[3*a*a*t**4+6*d*d*t**2+K,15*a*a*t**4+2*d*d*t**2+b*b+2*c,3*a*a*t**4+2*d*d*t**2+K,15*a*a*t**4+6*d*d*t**2-2*c*d]
 elif name=='dot_self_shifted':
  a,h,b,c,k=(p[z] for z in ('a','h','b','c','k'));f=vec(a*t**2-h,b*t,c*t**3-k);g=None;K=b*b-2*a*h;C=15*c*c*t**4+6*a*a*t**2-6*c*k*t+K
  W=[3*c*c*t**4-2*a*a*t**2+6*c*k*t+K,15*c*c*t**4+6*a*a*t**2+K,15*c*c*t**4-6*c*k*t+K,3*c*c*t**4+2*a*a*t**2-6*c*k*t+K]
 elif name=='dot_self_evaluate':
  a,h,b,k,c,x=(p[z] for z in ('a','h','b','k','c','x'));f=vec(a*t**3-h,b*t**2-k,c*t**2);g=None
  C=simp((f.diff(t,2).dot(f)+f.diff(t).dot(f.diff(t))).subs(t,x));W=[-C,2*C,0,-2*C]
 else:
  a,b,c,d,e,h=(p[k] for k in ('a','b','c','d','e','h'));f=vec(a*sp.log(t),b/t,c*t);g=vec(d*t,e/t,h*sp.log(t));L=a*d+c*h;B=b*e;C=L*(sp.log(t)+1)-2*B/t**3
  W=[L*sp.log(t)+2*B/t**3,C/2,L*(sp.log(t)+1)/2+B/t**3,sp.Integer(0)]
 return f,g,simp(C),list(map(simp,W)),['source_wrong_'+str(i+1) for i in range(4)]

# HARD — cross products with ordered determinant expansion; no unrelated branches.
def build_hard(name,p):
 if name=='cross_matrix':
  a,b,c,d,e,h=(p[k] for k in ('a','b','c','d','e','h'));f=vec(a*t**2,t+b,c);g=vec(t+d,e*t**2,h*t)
  C=vec((2*h-2*c*e)*t+b*h,c-3*a*h*t**2,4*a*e*t**3-2*t-b-d)
  W=[vec(C[2],C[1],C[0]),vec(-C[0],C[1],-C[2]),vec(C[1],C[0],C[2]),vec(C[0]/2,3*a*h*t**2,C[2])]
 elif name=='cross_monomials':
  a,b,c,d,e,h,n,P,Q=(p[k] for k in ('a','b','c','d','e','h','n','p','q'));f=vec(a*t,b,c*t**n);g=vec(d*t**P,e*t**Q,h*t)
  C=vec(b*h-c*e*(n+Q)*t**(n+Q-1),c*d*(n+P)*t**(n+P-1)-2*a*h*t,a*e*(1+Q)*t**Q-b*d*P*t**(P-1))
  W=[vec(b*c*e*t**(n+Q-1),c*d*t**(n+P-1)+n*a*h*t**2,a*e*(1+Q)*t**Q),vec(c*e*t**(n+Q-1)-b*h,n*c*d*t**(n+P-1)+2*a*h*t,C[2]),vec(P*c*e*t**(n+Q-1)+a*h,n*c*d*t**(n+P-1),a*e*t**Q-b*d*t**(P-1)),vec((n+Q)*c*e*t**(n+Q-1),c*d*(n+P)*t**(n+P-1)-b,a*e*(1+Q)*t**Q+2*a*h*t)]
 elif name=='cross_shifted':
  a,b,c,d,e,h,k=(p[z] for z in ('a','b','c','d','e','h','k'));f=vec(a*t**2,b*t,c);g=vec(d,e*t**2,h*t-k)
  A=f.diff(t).cross(g);B=f.cross(g.diff(t));C=A+B
  W=[vec((2*b*h+h)*t-b*k,2*a*e*t**2+2*a*k*t,4*a*e*t**3),A,vec(2*a*h*t-b*k,-(20*a*e+b)*t**2+2*a*k*t,b*d),B]
 else:
  a,b,c,d,e,h=(p[z] for z in ('a','b','c','d','e','h'));f=vec(a-b*t**2,c-d*t**3,e-h*t);g=None
  C=vec(6*d*h*t**2-6*d*e*t,2*b*e-2*b*h*t,-2*b*c+6*a*d*t-4*b*d*t**3)
  W=[vec(C[0],C[1],-2*b*c+8*b*d*t**3),vec(0,0,C[2]),vec(C[0],-C[1],-6*a*d*t+8*b*d*t**3),vec(6*d*h*t**2-6*d*e,-2*b*h*t,C[2])]
 return f,g,C.applyfunc(simp),[w.applyfunc(simp) for w in W],['source_wrong_'+str(i+1) for i in range(4)]

def build(name,p):
 level=TEMPLATES[name][0]
 return {'easy':build_easy,'moderate':build_moderate,'hard':build_hard}[level](name,p)

def authored_bank(name,p,f,g,C,rng):
 """Choose a complete set of instance-derived error operations, then validate it.

 No fixed negative counterpart, omitted term, component majority, or numerical
 rank is part of the response contract. The pool has derivative, product-term,
 and component/cofactor errors. Error selections vary as complete banks.
 """
 level=TEMPLATES[name][0]
 if level=='easy':
  A=g*f.diff(t);B=sp.diff(g,t)*f;wrong=sp.diff(g,t)*f.diff(t)
 elif level=='moderate':
  A=f.diff(t,2).dot(f) if g is None else f.diff(t).dot(g)
  B=f.diff(t).dot(f.diff(t)) if g is None else f.dot(g.diff(t))
  wrong=f.diff(t,2).dot(f.diff(t)) if g is None else f.diff(t).dot(g.diff(t))
 else:
  A=f.diff(t,2).cross(f) if g is None else f.diff(t).cross(g)
  B=f.diff(t).cross(f.diff(t)) if g is None else f.cross(g.diff(t))
  wrong=f.diff(t,2).cross(f.diff(t)) if g is None else f.diff(t).cross(g.diff(t))
 pool=[(A,'omit_second_product_term'),(B,'omit_first_product_term'),
       (A-B,'subtract_second_product_term'),(B-A,'subtract_first_product_term'),
       (2*A+B,'double_first_product_term'),(A+2*B,'double_second_product_term'),
       (A/2+B,'halve_first_derivative_factor'),(A+B/2,'halve_second_derivative_factor'),
       (-C,'reverse_entire_sign'),(2*A-B,'double_first_and_subtract_second'),
       (A-2*B,'subtract_double_second'),(-2*A+B,'subtract_double_first'),
       (-A+2*B,'reverse_first_and_double_second'),(-2*C,'reverse_sign_and_double_result'),
       (-C/2,'reverse_sign_and_halve_result'),(wrong,'multiply_derivatives_instead_of_product_rule')]
 if isinstance(C,sp.MatrixBase):
  for i in range(3):
   for factor,label in [(-1,'reverse_component_sign'),(2,'double_component_derivative'),(sp.Rational(1,2),'halve_component_derivative')]:
    v=C.copy();v[i]*=factor;pool.append((v,label+'_'+str(i)))
   # Differentiate the product as though its i-th component were constant.
   v=C.copy();v[i]=0;pool.append((v,'treat_component_as_constant_'+str(i)))
 # Select recipes before rejecting ambiguous banks. This is not "first valid".
 chosen=rng.sample(pool,4)
 W=[];labels=[]
 for value,label in chosen:
  if name=='dot_self_evaluate':value=value.subs(t,p['x'])
  W.append(value.applyfunc(simp) if isinstance(value,sp.MatrixBase) else simp(value));labels.append(label)
 return W,labels

def modal_key_is_unique(values):
 """Reject banks solvable by intersecting modal coefficients/arguments alone."""
 features=[]
 for answer in values:
  mapping={}
  components=list(answer) if isinstance(answer,sp.MatrixBase) else [answer]
  for index,expression in enumerate(components):
   for term in sp.Add.make_args(sp.expand(expression)):
    coefficient,argument=term.as_coeff_Mul();mapping[(index,argument)]=coefficient
  features.append(mapping)
 slots=set().union(*(set(f) for f in features))
 candidates=[]
 for choice in range(5):
  if all(sum(f.get(slot,0)==features[choice].get(slot,0) for f in features)==max(sum(f.get(slot,0)==other.get(slot,0) for f in features) for other in features) for slot in slots):candidates.append(choice)
 if candidates==[0]:return True
 if isinstance(values[0],sp.MatrixBase):
  component_candidates=[]
  for choice in range(5):
   if all(sum(equivalent(values[choice][c],v[c]) for v in values)==max(sum(equivalent(other[c],v[c]) for v in values) for other in values) for c in range(3)):component_candidates.append(choice)
  if component_candidates==[0]:return True
 pairs=[(a,b) for a in range(5) for b in range(a+1,5) if equivalent(values[a],-values[b])]
 return len(pairs)==1 and 0 in pairs[0]

def render(name,p,f,g,C):
 level,source,style,_=TEMPLATES[name];V=lambda v:vector(v,style);fp=f.diff(t);F=V(f)
 operator=r'\times ' if level=='hard' else r'\cdot '
 D=lambda v:vector(v,'bmatrix') if name=='scalar_base' else V(v)
 rows=[]
 def derivatives(label,original,derived):
  for index in range(3):
   rows.append((label+'_{'+str(index+1)+'}(t)',r'\frac{\mathrm{d}}{\mathrm{d}t}('+tex(original[index])+')='+tex(derived[index])))
  rows.append((label+'(t)',D(derived)))
 if level=='easy':
  scalar='u' if name=='scalar_power' else 'v';fn='g' if name=='scalar_power' else 'f'
  expr='('+scalar+'(t)'+fn+'(t))^{\\prime}'
  rule=scalar+'(t)'+fn+'^{\\prime}(t)+'+scalar+'^{\\prime}(t)'+fn+'(t)'
  prompt='Find $'+expr+'$ given that $'+fn+'(t)='+F+'$ and $'+scalar+'(t)='+tex(g)+'.$'
  derivatives(fn+'^{\\prime}',f,fp)
  rows.append((scalar+'^{\\prime}(t)',r'\frac{\mathrm{d}}{\mathrm{d}t}('+tex(g)+')='+tex(sp.diff(g,t))))
  A=(g*fp).applyfunc(simp);B=(sp.diff(g,t)*f).applyfunc(simp)
  calculation=[('P_1','('+tex(g)+')'+D(fp)),('',D(A)),('P_2','('+tex(sp.diff(g,t))+')'+D(f)),('',D(B))]
  solution='Use the scalar function multiple rule:'+block(expr+'='+rule)
 else:
  selfproduct=g is None;cross=level=='hard';kind='cross' if cross else 'dot'
  if selfproduct:
   expr='(f^{\\prime}'+operator+'f)^{\\prime}(t)'
   rule='f^{\\prime\\prime}(t)'+operator+'f(t)+f^{\\prime}(t)'+operator+'f^{\\prime}(t)'
   prompt='Given $f(t)='+F+'$, '+('evaluate' if name=='dot_self_evaluate' else 'find')+' $'+(expr.replace('(t)','('+str(p['x'])+')') if name=='dot_self_evaluate' else expr)+'.$'
   left,right,second1,second2=f.diff(t,2),f,fp,fp
   derivatives('f^{\\prime}',f,fp);derivatives('f^{\\prime\\prime}',fp,left)
  else:
   expr='(f'+operator+'g)^{\\prime}(t)';rule='f^{\\prime}(t)'+operator+'g(t)+f(t)'+operator+'g^{\\prime}(t)'
   prompt='Find $'+expr+'$ given that'+block(aligned([('f(t)',F),('g(t)',V(g))]))
   left,right,second1,second2=fp,g,f,g.diff(t)
   derivatives('f^{\\prime}',f,fp);derivatives('g^{\\prime}',g,second2)
  A=left.cross(right) if cross else simp(left.dot(right));B=second1.cross(second2) if cross else simp(second1.dot(second2))
  if cross:A=A.applyfunc(simp);B=B.applyfunc(simp)
  solution='Use the '+kind+' product rule, preserving the factor order:'+block(expr+'='+rule)
  calculation=[]
  if cross:
   for n,u,v,result in [(1,left,right,A),(2,second1,second2,B)]:
    label='P_'+str(n);calculation.append((label,determinant(u,v)))
    for component,(i,j,sign) in enumerate([(1,2,''),(0,2,'-'),(0,1,'')]):
     minor=r'\begin{vmatrix}'+tex(u[i])+' & '+tex(u[j])+r' \\ '+tex(v[i])+' & '+tex(v[j])+r'\end{vmatrix}'
     calculation.append(('P_{'+str(n)+','+str(component+1)+'}',sign+minor+'='+tex(result[component])))
    calculation.append((label,V(result)))
  else:
   if name=='dot_self_evaluate':
    x=p['x'];left,right,second1,second2=[v.subs(t,x) for v in (left,right,second1,second2)]
    Ae,Be=simp(A.subs(t,x)),simp(B.subs(t,x));expr=expr.replace('(t)','('+str(x)+')')
    calculation=[('P_1',dot_terms(left,right)),('',tex(Ae)),('P_2',dot_terms(second1,second2)),('',tex(Be))]
   else:calculation=[('P_1',dot_terms(left,right)),('',tex(A)),('P_2',dot_terms(second1,second2)),('',tex(B))]
 solution+=('\n\nWrite intermediate vectors as columns.' if name=='scalar_base' else '')
 solution+='\n\nDifferentiate each component:'+block(aligned(rows))
 solution+='\n\nCalculate the first product-rule term and the second product-rule term, denoted $P_1$ and $P_2$:'+block(aligned(calculation))
 solution+='\n\nAdd the two terms'+(' componentwise' if isinstance(C,sp.MatrixBase) else '')+':'+block(aligned([(expr,'P_1+P_2'),('',V(C) if isinstance(C,sp.MatrixBase) else tex(C))]))
 return prompt,solution,A,B

def sample(name,rng):
 p=dict(TEMPLATES[name][3])
 for k,v in p.items():
  if k=='x':p[k]=rng.choice([-1,0,1])
  elif k in ('n','p','q','r','m'):p[k]=rng.randint(1,4) if name=='scalar_power' else rng.randint(1,3) if name=='scalar_log' else rng.randint(2,4)
  elif k=='base':p[k]=rng.randint(2,5)
  else:p[k]=rng.choice([-3,-2,-1,1,2,3])
 if name=='scalar_base':p['s']=rng.choice([-2,-1,1,2])
 if name=='scalar_exp':p['b']=rng.randint(1,3);p['a']=rng.randint(1,2)
 if name=='scalar_power':p['p'],p['q'],p['r']=sorted(rng.sample(range(1,5),3));p['n']=rng.randint(1,3)
 if name=='cross_monomials':p['n']=rng.choice([3,4]);p['p']=2;p['q']=rng.choice([2,3])
 return p

def validate_parameters(name,p,source_bank=True):
 if set(p)!=set(TEMPLATES[name][3]):raise ValueError('Parameter keys must exactly match '+str(sorted(TEMPLATES[name][3])))
 if any(not isinstance(x,int) or isinstance(x,bool) for x in p.values()):raise ValueError('Exact integer parameters required')
 if any(x==0 for k,x in p.items() if k!='x'):raise ValueError('Nonzero coefficients and shifts required')
 if name=='scalar_base' and p['base']<2:raise ValueError('base >= 2 required')
 for k in ('n','p','q','r','m'):
  if k in p and not 1<=p[k]<=4:raise ValueError('Supported power bounds are 1..4')
 for key,value in p.items():
  if key not in ('n','p','q','r','m','x','base') and abs(value)>max(6,abs(TEMPLATES[name][3][key])):raise ValueError('Coefficient/shift exceeds supported source-inclusive bound')
 if name=='dot_self_evaluate' and p['x'] not in (-1,0,1):raise ValueError('Evaluation point must be -1, 0, or 1')
 if name=='scalar_base' and (p['base']>5 or abs(p['s'])>2):raise ValueError('Supported bases are 2..5 and shifts have magnitude 1..2')
 if name=='scalar_power' and (not 1<=p['n']<=3 or not p['p']<p['q']<p['r']):raise ValueError('Three ascending distinct component powers and scalar power 1..3 required')
 if name=='scalar_log' and (p['n']>3 or p['m']>3):raise ValueError('Supported log-template powers are 1..3')
 if name=='scalar_exp' and (p['a']>2 or p['b']>3):raise ValueError('Supported exponential rates are a=1..2, b=1..3')
 if name=='cross_monomials' and (p['n'] not in (3,4) or p['p']!=2 or p['q'] not in (2,3)):raise ValueError('Unsupported hard monomial power structure')
 if source_bank and name=='scalar_log' and p['n']==p['m']:raise SampleRejected('Source bank exchanges become duplicates for equal powers')
 if name=='scalar_exp' and (p['a']<1 or p['b']<1):raise ValueError('Positive exponential rates required')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,permutation=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only source radio fields are supported')
 if profile:
  if profile not in BANK_PROFILES:raise ValueError('Unknown bank profile')
  implied=BANK_PROFILES[profile]['template']
  if template and template!=implied:raise ValueError('Profile/template mismatch')
  template=implied
 rng=random.Random(seed)
 names=[k for k,v in TEMPLATES.items() if v[0]==level]
 name=template or rng.choice(names)
 if name not in names:raise ValueError('Template/difficulty mismatch')
 profile=profile or name+'_authored'
 authored=BANK_PROFILES[profile]['origin']=='authored'
 if authored:
  p=dict(parameters) if parameters is not None else sample(name,rng)
  validate_parameters(name,p,source_bank=False)
  fixed_order=list(permutation) if permutation is not None else rng.sample(range(3),3)
 for bank_attempt in range(200):
  if not authored:p=dict(parameters) if parameters is not None else sample(name,rng)
  try:
   validate_parameters(name,p,source_bank=not authored);f,g,C,W,labels=build(name,p)
   if BANK_PROFILES[profile]['origin']=='authored':
    order=fixed_order
    if sorted(order)!=[0,1,2]:raise ValueError('Component permutation required')
    f=vec(*(f[i] for i in order))
    if isinstance(g,sp.MatrixBase):g=vec(*(g[i] for i in order))
    if isinstance(C,sp.MatrixBase):
     parity=(-1)**sum(order[i]>order[j] for i in range(3) for j in range(i+1,3)) if level=='hard' else 1
     C=parity*vec(*(C[i] for i in order))
    W,labels=authored_bank(name,p,f,g,C,rng)
   else:order=[0,1,2]
   if any(equivalent(C,w) for w in W) or any(equivalent(a,b) for i,a in enumerate(W) for b in W[i+1:]):raise SampleRejected('Whole selected bank is ambiguous')
   if BANK_PROFILES[profile]['origin']=='authored' and modal_key_is_unique([C]+W):raise SampleRejected('Modal coefficient intersection uniquely identifies key')
   if BANK_PROFILES[profile]['origin']=='authored' and isinstance(C,sp.MatrixBase):
    zero_mask=tuple(z==0 for z in C)
    if any(zero_mask) and not any(tuple(z==0 for z in w)==zero_mask for w in W):raise SampleRejected('Cancellation pattern uniquely identifies key')
   break
  except SampleRejected:
   if parameters is not None and BANK_PROFILES[profile]['origin']!='authored':raise
 else:raise SampleRejected('No eligible complete bank after 200 trials')
 prompt,solution,A,B=render(name,p,f,g,C)
 if name in ('scalar_log','dot_log_reciprocal'):prompt+=' Assume $t>0$.'
 prompt=normalize_prose(prompt);solution=normalize_prose(solution)
 style=TEMPLATES[name][2]
 if profile=='cross_matrix_legacy':style='bmatrix'
 values=[normalize_tex(vector(x,style) if isinstance(x,sp.MatrixBase) else tex(x)) for x in [C]+W]
 fp=hashlib.sha256(json.dumps({'template':name,'parameters':p,'domain':'t>0' if name in ('scalar_log','dot_log_reciprocal') else 'real'},sort_keys=True).encode()).hexdigest()
 # Identity includes DISPLAYED bank/profile/layout, and never seed/order.
 content=hashlib.sha256(json.dumps({'template':name,'profile':profile,'parameters':p,'problem':prompt,'solution':solution,'bank':sorted(values)},sort_keys=True).encode()).hexdigest()
 qid=uuid.uuid5(uuid.NAMESPACE_URL,f'course-academy/{KP_UUID}/{VERSION}/{content}');fid=uuid.uuid5(qid,'selection')
 answers=[{':answer/id':str(uuid.uuid5(fid,'math:'+v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 correct=answers[0][':answer/id'];math_values={a[':answer/id']:sexpr(x) for a,x in zip(answers,[C]+W)}
 recipes={a[':answer/id']:label for a,label in zip(answers,['correct']+labels)}
 rng.shuffle(answers)
 field={':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
 record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'component_order':order,'bank_attempts':bank_attempt+1,'template':name,'parameters':p,'parameter_fingerprint':fp,'content_fingerprint':content,'bank_profile':profile,'bank_origin':BANK_PROFILES[profile]['origin'],'source_analysis':{**SOURCE,'question_ids':[SOURCE_IDS[TEMPLATES[name][1]]],'math_academy_ids':[TEMPLATES[name][1]]},'plot_rating':'none','plot_assets':{},'domain':'t>0' if name in ('scalar_log','dot_log_reciprocal') else 'real','authored_extension':p!=TEMPLATES[name][3] or BANK_PROFILES[profile]['origin']=='authored','layout_repair':name=='cross_matrix','source_repair':name=='scalar_base','mathematics':{'f':sexpr(f),'g_or_scalar':sexpr(g) if g is not None else None,'correct':sexpr(C),'first_product_term':sexpr(A),'second_product_term':sexpr(B),'answer_values':math_values,'recipes':recipes}}}

 return validate_generated_record(record)

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(record):
 q,g=record['question'],record['generation'];f=q[':question/answer-fields'][0]
 lines=['## Generated '+q[':question/difficulty'].split('/')[-1]+' — '+g['template'],'',q[':question/problem'],'']
 for i,a in enumerate(f[':answer-field/choices']):lines.append('- '+chr(65+i)+'. $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else ''))
 return '\n'.join(lines)+'\n\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='moderate');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='json');ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile',choices=list(BANK_PROFILES));args=ap.parse_args()
 if args.count<1:ap.error('positive count required')
 if args.difficulty=='all' and (args.template or args.profile):ap.error('select a difficulty for template/profile')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 try:
  records=[];rng=random.Random(args.seed)
  for level in levels:
   names=[k for k,v in TEMPLATES.items() if v[0]==level]
   schedule=[];seen=set();seen_work={name:set() for name in names};self_dot_ranks=set()
   for i in range(args.count):
    if not schedule:schedule=names.copy();rng.shuffle(schedule)
    name=args.template or (BANK_PROFILES[args.profile]['template'] if args.profile else schedule.pop())
    for attempt in range(200):
     record=generate(level,rng.getrandbits(63),name,profile=args.profile)
     m=record['generation']['mathematics']
     # Ignore presentation; identify the actual functions and task/evaluation.
     signature=json.dumps([name, sorted(m['f']) if level!='hard' else m['f'], m['g_or_scalar'],record['generation']['parameters'].get('x')],sort_keys=True)
     work_parameters=dict(record['generation']['parameters'])
     # Constant exponential offsets do not change the main differentiation rates;
     # shifted constant product components in scalar_base cancel identically.
     if name in ('scalar_exp','scalar_base'):work_parameters.pop('s')
     work=json.dumps(work_parameters,sort_keys=True)
     capacity={'scalar_exp':6,'scalar_base':24}.get(name)
     fresh_work=work not in seen_work[name] or (capacity is not None and len(seen_work[name])>=capacity)
     # Derivative-dot prompts are a recognizable subgroup. Avoid a short
     # batch where a fixed numerical bank rank answers every such item.
     rank=None
     if name.startswith('dot_self_'):
      field=record['question'][':question/answer-fields'][0]
      values=[sp.sympify(m['answer_values'][a[':answer/id']]) for a in field[':answer-field/choices']]
      numbers=[float(v.subs(t,2)) for v in values]
      key=next(j for j,a in enumerate(field[':answer-field/choices']) if a[':answer/id']==field[':answer-field/correct'][1])
      rank=sorted(range(5),key=lambda j:numbers[j]).index(key)
     rank_fresh=rank is None or len(self_dot_ranks)!=1 or rank not in self_dot_ranks
     if signature not in seen and fresh_work and rank_fresh:break
    else:raise SampleRejected('Cannot construct a fresh calculation')
    seen.add(signature);seen_work[name].add(work);records.append(record)
    if rank is not None:self_dot_ranks.add(rank)
 except ValueError as e:ap.error(str(e))
 print(json.dumps(_apply_source_notation(records),ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

from source_notation import install as _install_source_notation, apply as _apply_source_notation
_install_source_notation(globals())

if __name__=='__main__':main()
