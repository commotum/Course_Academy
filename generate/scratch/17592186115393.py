#!/usr/bin/env python3
"""Exact, deterministic product-rule questions (math snapshot basis 1356).

The observed easy scalar products are retained despite overlap with the sibling
KP. Moderate dot and hard cross products retain their source workload. Banks are
whole recipes; their uncertain authoring interpretations are documented in the
adjacent extraction report. No source payload or answer lookup is used here.
"""
import argparse
import hashlib
import json
import random
import uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186115393
KP_UUID='d54a6dbe-42cb-5614-ae0b-611de1719b45'
TITLE='Using the Product Rules for Differentiation'
VERSION='1.0.0'
t=sp.Symbol('t', real=True)
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
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
BANK_PROFILES={name+'_observed':{'template':name,'origin':'observed','source_id':row[1]} for name,row in TEMPLATES.items()}
BANK_PROFILES.update({name+'_authored':{'template':name,'origin':'authored','source_id':None} for name in TEMPLATES})
BANK_PROFILES['cross_matrix_legacy']={'template':'cross_matrix','origin':'legacy-source-evidence','source_id':'q-32353'}
class SampleRejected(ValueError): pass

def simp(x):
 # Keep numeric logarithm coefficients readable. SymPy's general simplify can
 # rewrite 5**6*log(5) as log(5**15625), producing thousands of digits.
 expr=sp.expand(x)
 logs={atom:sp.Dummy('log_atom',real=True) for atom in expr.atoms(sp.log)}
 if logs:return sp.simplify(expr.xreplace(logs)).xreplace({dummy:atom for atom,dummy in logs.items()})
 return sp.simplify(expr)

def vec(*x): return sp.Matrix(x)
def tex(x):
 return sp.latex(simp(x)).replace(r'\log',r'\ln').replace(r'\left', '').replace(r'\right','')
def vector(v,style='tuple'):
 if style=='matrix': return r'[\begin{aligned}'+r' \\ '.join(tex(x) for x in v)+r'\end{aligned}]'
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
 if style=='matrix':return r'[\begin{aligned}'+r' \\ '.join(d(x) for x in v)+r'\end{aligned}]'
 if style=='basis':return '+'.join(d(x)+r'\,'+u for x,u in zip(v,'ijk'))
 return '⟨'+r',\,'.join(d(x) for x in v)+'⟩'
def determinant(u,v):return r'|\begin{aligned}i & j & k \\ '+ ' & '.join(tex(x) for x in u)+r' \\ '+' & '.join(tex(x) for x in v)+r'\end{aligned}|'
def minors(u,v):
 def minor(i,j):return r'|\begin{aligned}'+tex(u[i])+' & '+tex(u[j])+r' \\ '+tex(v[i])+' & '+tex(v[j])+r'\end{aligned}|'
 return minor(1,2)+'i-'+minor(0,2)+'j+'+minor(0,1)+'k'
def dot_terms(u,v):return '+'.join('('+tex(a)+')('+tex(b)+')' for a,b in zip(u,v))
def sexpr(x):return [sp.srepr(y) for y in x] if isinstance(x,sp.MatrixBase) else sp.srepr(x)
def grouped(v,style):
 value=vector(v,style)
 return '('+value+')' if style=='basis' else value
def equivalent(a,b):
 if isinstance(a,sp.MatrixBase) and isinstance(b,sp.MatrixBase):return a.shape==b.shape and all(simp(x-y)==0 for x,y in zip(a,b))
 return not isinstance(a,sp.MatrixBase) and not isinstance(b,sp.MatrixBase) and simp(a-b)==0

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

def authored_bank(name,p,f,g,C):
 """Four complete, operation-derived wrong answers; never source numeric fits."""
 level=TEMPLATES[name][0]
 if level=='easy':
  A=g*f.diff(t);B=sp.diff(g,t)*f
  W=[A,B,A-B,2*A+B]
  labels=['omit_scalar_derivative_term','omit_vector_derivative_term','subtract_second_product_term','count_first_product_term_twice']
 elif level=='moderate':
  if g is None:
   A=f.diff(t,2).dot(f);B=f.diff(t).dot(f.diff(t));wrong=f.diff(t,2).dot(f.diff(t))
  else:A=f.diff(t).dot(g);B=f.dot(g.diff(t));wrong=f.diff(t).dot(g.diff(t))
  if name=='dot_self_evaluate':
   x=p['x'];W=[B,-A+B,2*A+B,A/2+B];W=[w.subs(t,x) for w in W]
   labels=['omit_second_derivative_product','reverse_sign_of_second_derivative_product','count_second_derivative_product_twice','omit_factor_two_from_second_derivatives']
  else:
   W=[A,-A if name=='dot_log_reciprocal' else B,-C,wrong]
   labels=['omit_second_product_term','omit_second_product_term_and_reverse_sign' if name=='dot_log_reciprocal' else 'omit_first_product_term','reverse_sign_of_entire_result','multiply_derivatives_instead_of_product_rule']
 else:
  wrong_middle=vec(C[0],-C[1],C[2])
  if g is None:
   W=[f.diff(t).cross(f.diff(t)),-C,wrong_middle,f.diff(t,2).cross(f.diff(t))]
   labels=['retain_only_self_cross_zero_term','reverse_cross_order_in_both_terms','use_positive_middle_cofactor','differentiate_both_inputs_instead_of_product_rule']
  else:
   W=[f.diff(t).cross(g),f.cross(g.diff(t)),-C,wrong_middle]
   labels=['omit_second_cross_product_term','omit_first_cross_product_term','reverse_cross_order_in_both_terms','use_positive_middle_cofactor']
 W=[w.applyfunc(simp) if isinstance(w,sp.MatrixBase) else simp(w) for w in W]
 return W,labels

def render(name,p,f,g,C):
 level,source,style,_=TEMPLATES[name];V=lambda v:vector(v,style);fp=f.diff(t);F=V(f)
 if level=='easy':
  use_u=name=='scalar_power';scalar='u' if use_u else 'v';fn='g' if use_u else 'f';expr='('+scalar+'(t)'+fn+'(t))^{′}';op=scalar+'(t){'+fn+'}^{′}(t)+{'+scalar+'}^{′}(t)'+fn+'(t)'
  prompt=('Find  ' if use_u else 'Find ')+ '$'+expr+'$ '+('where' if use_u else 'given that ')+ ' $'+fn+'(t)='+F+'$ and $'+scalar+'(t)='+tex(g)+'.$'
  rows=[('{'+fn+'}^{′}(t)',dvec(f,style)),('',V(fp)),('{'+scalar+'}^{′}(t)',r'\frac{\text{d}}{\text{d}t}('+tex(g)+')='+tex(sp.diff(g,t)))]
  A=(g*fp).applyfunc(simp);B=(sp.diff(g,t)*f).applyfunc(simp)
  solution='By the scalar function multiple rule, we have'+block(expr+'='+op+('.' if name!='scalar_base' else ''))
  solution+="\n\nLet's find "+('the ' if use_u else '')+'${'+scalar+'}^{′}(t)$ and ${'+fn+'}^{′}(t).$'+block(aligned(rows))
  solution+='\n\nTherefore, we obtain'+block(aligned([(expr,op),('',tex(g)+V(fp)+'+'+tex(sp.diff(g,t))+F),('',V(A)+'+'+V(B)),('',V(C)+('.' if name!='scalar_base' else ''))]))
  return prompt,solution,A,B
 cross=level=='hard';operator=r'\times' if cross else r'\cdot';kind='cross' if cross else 'dot';selfproduct=g is None
 if selfproduct:
  left=f.diff(t,2);right=f;second1=fp;second2=fp;expr='({f}^{′}'+operator+'f)^{′}(t)';op='{f}^{″}(t)'+operator+'f(t)+{f}^{′}(t)'+operator+'{f}^{′}(t)'
  prompt='Given $f(t)='+F+'$, '+('evaluate' if name=='dot_self_evaluate' else 'find')+' $'+(expr.replace('(t)','('+str(p['x'])+')') if name=='dot_self_evaluate' else expr)+'.$'
  rows=[('{f}^{′}(t)',dvec(f,style)),('',V(fp)),('{f}^{″}(t)',dvec(fp,style)),('',V(left))]
  derivative_sentence="Let's now find the first and second derivative of the function."
 else:
  left=fp;right=g;second1=f;second2=g.diff(t);expr='(f'+operator+'g)^{′}(t)';op='{f}^{′}(t)'+operator+'g(t)+f(t)'+operator+'{g}^{′}(t)'
  if name=='cross_matrix': prompt='Find $'+expr+'$ where'+block('f(t)='+F+r',\,g(t)='+V(g))
  else:
   prompt='Find $'+expr+'$'+(', given that ' if name=='dot_polynomial' else ', given that' if not cross else ' given that')+block(aligned([('f(t)',F),('g(t)',V(g))]))
  rows=[('{f}^{′}(t)',dvec(f,style)),('',V(fp)),('{g}^{′}(t)',dvec(g,style)),('',V(second2))]
  if style=='matrix':rows=[('{f}^{′}(t)',dvec(f,style)+'='+V(fp)),('{g}^{′}(t)',dvec(g,style)+'='+V(second2))]
  derivative_sentence="Let's now find the derivatives of each function."
 A=left.cross(right) if cross else simp(left.dot(right));B=second1.cross(second2) if cross else simp(second1.dot(second2))
 if cross:A=A.applyfunc(simp);B=B.applyfunc(simp)
 solution='Using the '+kind+' product rule, we can write:'+block(expr+'='+op)+'\n\n'+derivative_sentence+block(aligned(rows))+('\n\nTherefore, we obtain' if name=='cross_monomials' else '\n\nTherefore, we obtain:')
 if cross:
  first_label='{f}^{″}(t)' if selfproduct else '{f}^{′}(t)';second_label='{f}^{′}(t)' if selfproduct else 'f(t)';other_label='f(t)' if selfproduct else 'g(t)';other2='{f}^{′}(t)' if selfproduct else '{g}^{′}(t)'
  solution+=block(aligned([(first_label+operator+other_label,determinant(left,right)),('',minors(left,right)),('',V(A)),(second_label+operator+other2,determinant(second1,second2)),('',minors(second1,second2)),('',V(B))]))
  solution+='\n\nFinally,'+block(aligned([(expr,V(A)+'+'+V(B)),('',V(C))]))
 else:
  if name=='dot_self_evaluate':
   x=p['x'];evalv=lambda v:v.subs(t,x);Ae=simp(A.subs(t,x));Be=simp(B.subs(t,x));target=expr.replace('(t)','('+str(x)+')')
   solution+=block(aligned([(target,op.replace('(t)','('+str(x)+')')),('',grouped(evalv(left),style)+operator+grouped(evalv(right),style)+'+'+grouped(evalv(second1),style)+operator+grouped(evalv(second2),style)),('',dot_terms(evalv(left),evalv(right))+'+'+dot_terms(evalv(second1),evalv(second2))),('',tex(Ae)+'+'+tex(Be)),('',tex(C))]))
  else:solution+=block(aligned([(expr,op),('',grouped(left,style)+operator+grouped(right,style)+'+'+grouped(second1,style)+operator+grouped(second2,style)),('', '('+dot_terms(left,right)+')+('+dot_terms(second1,second2)+')'),('',tex(A)+'+'+tex(B)),('',tex(C))]))
 return prompt,solution,A,B

def sample(name,rng):
 p=dict(TEMPLATES[name][3])
 for k,v in p.items():
  if k=='x':p[k]=rng.choice([-1,0,1])
  elif k in ('n','p','q','r','m'):p[k]=rng.randint(1,4) if name=='scalar_power' else rng.randint(1,3) if name=='scalar_log' else rng.randint(2,4)
  elif k=='base':p[k]=rng.randint(2,5)
  else:p[k]=rng.randint(1,6)*(-1 if v<0 else 1)
 if name=='scalar_base':p['s']=rng.randint(1,2)
 if name=='scalar_exp':p['b']=rng.randint(1,3);p['a']=rng.randint(1,2)
 if name=='scalar_power':p['p'],p['q'],p['r']=sorted(rng.sample(range(1,5),3));p['n']=rng.randint(1,3)
 if name=='cross_monomials':p['n']=rng.choice([3,4]);p['p']=2;p['q']=rng.choice([2,3])
 return p

def validate_parameters(name,p):
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
 if name=='scalar_log' and p['n']==p['m']:raise SampleRejected('Source bank exchanges become duplicates for equal powers')
 if name=='scalar_exp' and (p['a']<1 or p['b']<1):raise ValueError('Positive exponential rates required')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
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
 for _ in range(200):
  p=dict(parameters) if parameters is not None else sample(name,rng)
  try:
   validate_parameters(name,p);f,g,C,W,labels=build(name,p)
   if BANK_PROFILES[profile]['origin']=='authored':W,labels=authored_bank(name,p,f,g,C)
   if any(equivalent(C,w) for w in W) or any(equivalent(a,b) for i,a in enumerate(W) for b in W[i+1:]):raise SampleRejected('Whole selected bank is ambiguous')
   break
  except SampleRejected:
   if parameters is not None:raise
 else:raise SampleRejected('No eligible complete bank after 200 trials')
 prompt,solution,A,B=render(name,p,f,g,C)
 style=TEMPLATES[name][2]
 if profile=='cross_matrix_legacy':style='bmatrix'
 values=[vector(x,style) if isinstance(x,sp.MatrixBase) else tex(x) for x in [C]+W]
 fp=hashlib.sha256(json.dumps({'template':name,'parameters':p,'domain':'t>0' if name in ('scalar_log','dot_log_reciprocal') else 'real'},sort_keys=True).encode()).hexdigest()
 # Identity includes DISPLAYED bank/profile/layout, and never seed/order.
 content=hashlib.sha256(json.dumps({'template':name,'profile':profile,'parameters':p,'problem':prompt,'solution':solution,'bank':sorted(values)},sort_keys=True).encode()).hexdigest()
 qid=uuid.uuid5(uuid.NAMESPACE_URL,f'course-academy/{KP_UUID}/{VERSION}/{content}');fid=uuid.uuid5(qid,'selection')
 answers=[{':answer/id':str(uuid.uuid5(fid,'math:'+v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 correct=answers[0][':answer/id'];math_values={a[':answer/id']:sexpr(x) for a,x in zip(answers,[C]+W)}
 recipes={a[':answer/id']:label for a,label in zip(answers,['correct']+labels)}
 rng.shuffle(answers)
 field={':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':name,'parameters':p,'parameter_fingerprint':fp,'content_fingerprint':content,'bank_profile':profile,'bank_origin':BANK_PROFILES[profile]['origin'],'source_analysis':{**SOURCE,'question_ids':[TEMPLATES[name][1]]},'plot_rating':'none','plot_assets':{},'domain':'t>0' if name in ('scalar_log','dot_log_reciprocal') else 'real','authored_extension':p!=TEMPLATES[name][3] or BANK_PROFILES[profile]['origin']=='authored','layout_repair':name=='cross_matrix','source_repair':name=='scalar_base','mathematics':{'f':sexpr(f),'g_or_scalar':sexpr(g) if g is not None else None,'correct':sexpr(C),'first_product_term':sexpr(A),'second_product_term':sexpr(B),'answer_values':math_values,'recipes':recipes}}}

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(record):
 q,g=record['question'],record['generation'];f=q[':question/answer-fields'][0]
 lines=['## Generated '+q[':question/difficulty'].split('/')[-1]+' — '+g['template'],'',q[':question/problem'],'']
 for i,a in enumerate(f[':answer-field/choices']):lines.append('- '+chr(65+i)+'. $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else ''))
 return '\n'.join(lines)+'\n\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile',choices=list(BANK_PROFILES));args=ap.parse_args()
 if args.count<1:ap.error('positive count required')
 if args.difficulty=='all' and (args.template or args.profile):ap.error('select a difficulty for template/profile')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 try:records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
 except ValueError as e:ap.error(str(e))
 print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
