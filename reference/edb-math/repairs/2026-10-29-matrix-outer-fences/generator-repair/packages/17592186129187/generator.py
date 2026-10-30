#!/usr/bin/env python3
"""Seeded symbolic Jacobian questions; portable, database-free review package.
Observed banks are the default. Explicit authored profiles and the canonical
powers extension are retained. See instructional-account.md for scope.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import random
import uuid
import sympy as sp
from math_format import matrix_tex, normalize_tex, normalize_prose, checked_math_content

KP_ID=17592186129187
KP_UUID='d56cec4a-6121-5988-aaea-478fb6048a6d'
TITLE='Finding the Jacobian Determinant of a Transformation'
VERSION='jacobian-2'
PROVENANCE={'database':'math','basis':2850,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
u,v=sp.symbols('u v',real=True)
TEMPLATES={
 'polar':('easy','q-38078',{'a':2,'b':3}),
 'linear':('easy','q-160381',{'a':3,'b':2,'c':1,'d':3}),
 'linear_log':('easy','q-160404',{'a':3,'b':-5}),
 'tan_product':('easy','q-38241',{'k':2}),
 'quadratic':('easy','q-81264',{'a':1,'b':1}),
 'exp_log':('moderate','q-160403',{'a':1,'b':1}),
 'cos_linear':('moderate','q-160405',{'a':4,'b':6}),
 'trig_pair':('moderate','q-81252',{'a':1,'b':1}),
 'exp_quadratic':('moderate','q-160406',{'a':1,'b':1}),
 'log_product':('moderate','q-38244',{'a':2,'b':1}),
 'log_square':('moderate','q-81263',{'a':1,'b':1}),
 'powers':('hard',None,{'a':1,'b':1,'m':3,'n':2,'p':1,'q':1,'r':1,'s':1}),
}
BANK_PROFILES={**{'observed_'+t:{'template':t,'origin':'observed expression replay','source':src} for t,(_,src,_) in TEMPLATES.items() if src},
 **{'authored_'+t:{'template':t,'origin':'authored method errors','source':None} for t in TEMPLATES}}
class SampleRejected(ValueError): pass

def tex(x): return normalize_tex(sp.latex(x,mul_symbol=None, ln_notation=True))
def block(s): return '$$\n'+s+'\n$$'
def mat(a,b,c,d): return r'\begin{vmatrix}'+a+'&'+b+r'\\'+c+'&'+d+r'\end{vmatrix}'
J=r'\frac{\partial(x,y)}{\partial(u,v)}'
PARTIALS=[r'\frac{\partial x}{\partial u}',r'\frac{\partial x}{\partial v}',r'\frac{\partial y}{\partial u}',r'\frac{\partial y}{\partial v}']
def clean(x): return sp.powsimp(sp.factor(sp.trigsimp(sp.cancel(x))), force=True)
def equivalent(a,b): return sp.simplify(sp.trigsimp(a-b))==0

def validate_parameters(t,p):
 expected=TEMPLATES[t][2]
 if set(p)!=set(expected): raise ValueError(f'{t} parameters must be exactly {list(expected)}')
 if any(type(x) is not int for x in p.values()): raise ValueError('Use exact integer parameters')
 if t=='linear':
  if any(not 1<=x<=6 for x in p.values()) or p['a']*p['d']==p['b']*p['c']: raise ValueError('Nonzero small coefficients and nonsingular matrix required')
 elif t=='linear_log':
  if not(2<=p['a']<=6 and -7<=p['b']<=-2): raise ValueError('a positive, b negative')
 elif t=='cos_linear':
  if not(2<=p['a']<=7 and 2<=p['b']<=8 and p['a']!=p['b']): raise ValueError('Positive unequal a,b required')
 elif t=='powers':
  if not(1<=p['a']<=3 and 1<=p['b']<=3 and (p['m'],p['n']) in [(3,2),(2,3),(3,3)]): raise ValueError('Hard scope: small scales and (3,2),(2,3),(3,3) powers')
  if any(p[k] not in (1,2) for k in ('p','q','r','s')):raise ValueError('Hard inner linear coefficients are 1 or 2')
 elif t=='tan_product':
  if not 2<=p['k']<=5: raise ValueError('k must be 2..5')
 elif any(not 1<=x<=5 for x in p.values()): raise ValueError('Positive integer parameters 1..5 required')

def functions(t,p):
 a,b=p.get('a',1),p.get('b',1)
 if t=='polar': return a*u*sp.cos(v),b*u*sp.sin(v),'R^2'
 if t=='linear': return a*u+b*v,p['c']*u+p['d']*v,'R^2'
 if t=='linear_log': return a*u+b*v,sp.log(u+v),'u+v>0'
 if t=='tan_product': return sp.cos(v)*sp.tan(u/p['k']),sp.sin(v),f'cos(u/{p["k"]}) != 0'
 if t=='quadratic': return a*u**2-b*v**2,a*u**2+b*v**2,'R^2'
 if t=='exp_log': return sp.exp(a*u+b*v),sp.log(u*v),'uv>0'
 if t=='cos_linear': return sp.cos(u+v),a*u+b*v,'R^2'
 if t=='trig_pair': return a*sp.sin(u+v),b*sp.cos(u-v),'R^2'
 if t=='exp_quadratic': return sp.exp(u+v),a*u**2+b*v**2,'R^2'
 if t=='log_product': return sp.log(a*u+b*v),u*v,f'{a}*u+{b}*v>0'
 if t=='log_square': return a*u*sp.log(v),b*u**2*v**2,'v>0'
 if t=='powers': return a*(p['p']*u+p['q']*v)**p['m'],b*(p['r']*u-p['s']*v)**p['n'],'R^2'
 raise ValueError(t)

# Complete observed profiles. Symbolic expression shapes are preserved, but the
# original authors' intent is NOT established by scalar/sparse observations.
def observed_bank(t,p,j):
 a,b=p.get('a',1),p.get('b',1)
 if t=='polar': return [('negative_y_scale',-b*u),('x_scale',a*u),('scale_ratio',sp.Rational(a,b)*u),('negative_inverse_ratio',-sp.Rational(b,a)*u),('correct',j)]
 if t=='linear': return [('second_x_plus_first_v',p['c']*u+b*v),('add_diagonal_products',a*p['d']+b*p['c']),('correct',j),('diagonal_product_times_u',a*p['d']*u),('first_x_minus_second_x_v',a*u-p['c']*v)]
 if t=='linear_log': return [('correct',j),('u_over_sum',u/(u+v)),('v_over_sum',v/(u+v)),('twice_a_over_sum',2*a/(u+v)),('log_argument',u+v)]
 if t=='tan_product':
  k=p['k']; base=sp.cos(v)**2/sp.cos(u/k)**2
  return [('correct',j),('invert_inner_scale',k*base),('omit_inner_scale',sp.cos(v)**2/sp.cos(u)**2),('omit_chain_and_subtract',base-sp.cos(v)),('invert_chain_and_add',k*base+sp.cos(v))]
 if t=='quadratic': return [('twice_first_output',2*(a*u**2-b*v**2)),('quadratic_mixed',a*u**2-a*b*u*v+b*v**2),('correct',j),('difference_first_derivatives',4*(a*u-b*v)),('subtract_equal_products',sp.S.Zero)]
 if t=='exp_log':
  e=sp.exp(a*u+b*v)
  return [('zero',sp.S.Zero),('first_output',e),('one',sp.S.One),('correct',j),('omit_linear_numerator',e/(v*u))]
 if t=='cos_linear': return [('coefficient_and_wrong_argument',a*sp.sin(u-v)),('undifferentiated_x',sp.cos(u+v)),('negative_cos_difference',-sp.cos(u-v)),('omit_coefficient',-sp.sin(u+v)),('correct',j)]
 if t=='trig_pair':
  f=a*b*sp.cos(u+v)*sp.sin(u-v); swapped=a*b*sp.cos(u-v)*sp.sin(u+v)
  return [('single_diagonal',f),('correct',j),('swap_arguments',swapped),('double_swap_arguments',2*swapped),('square_trig_factors',f**2)]
 if t=='exp_quadratic':
  e=sp.exp(u+v)
  return [('omit_two_and_add',e*(a*u+b*v)),('add_products',2*e*(a*u+b*v)),('product_of_variables',a*b*e*u*v),('correct',j),('reverse_determinant',-j)]
 if t=='log_product':
  den=a*u+b*v
  return [('omit_inner_a',b*(u-v)/den),('omit_a_and_add',b*(u+v)/den),('swap_variables',(a*v-b*u)/den),('one',sp.S.One),('correct',j)]
 if t=='log_square':
  scale=a*b
  return [('correct',j),('power_coefficient_for_variable',4*scale*u*v*(sp.log(v)-1)),('lose_v_in_log_term',2*scale*u**2*(sp.log(v)-v)),('lose_u_and_v',2*scale*u*v*(sp.log(v)-v)),('double_and_lose_v',4*scale*u**2*(sp.log(v)-v))]
 raise ValueError('No observed profile for authored powers')

def authored_bank(t,p,derivatives,j):
 A,B,C,D=derivatives; P=clean(A*D); Q=clean(B*C)
 # Complete authored method-error banks. Families with zero/cancelling terms
 # require operations on the derivatives that remain distinct as functions.
 if t in ('polar','quadratic','powers','trig_pair'):
  return [('correct',j),('reverse_subtraction',-j),('omit_cross_product',P),('add_products',clean(P+Q)),('multiply_diagonal_products',P*Q)]
 if t=='tan_product':
  k=p['k']
  return [('correct',j),('omit_chain_factor',k*j),('invert_chain_factor',k*k*j),('reverse_sign',-j),('omit_y_derivative',derivatives[0])]
 if t=='linear':
  return [('correct',j),('add_products',P+Q),('reverse_subtraction',-j),('omit_cross_product',P),('omit_diagonal_product',-Q)]
 return [('correct',j),('add_products',clean(P+Q)),('reverse_subtraction',-j),('omit_cross_product',P),('omit_diagonal_product',-Q)]

def sample(t,rng):
 if t=='linear': return dict(zip(('a','b','c','d'),[rng.randint(1,6) for _ in range(4)]))
 if t=='linear_log': return {'a':rng.randint(2,6),'b':-rng.randint(2,7)}
 if t=='tan_product': return {'k':rng.randint(2,5)}
 if t=='cos_linear': return {'a':rng.randint(2,7),'b':rng.randint(2,8)}
 if t=='powers': return {'a':rng.randint(1,3),'b':rng.randint(1,3),**dict(zip(('m','n'),rng.choice([(3,2),(2,3),(3,3)]))),**{k:rng.randint(1,2) for k in ('p','q','r','s')}}
 return {'a':rng.randint(1,5),'b':rng.randint(1,5)}

def solution(t,x,y,ds,j,p):
 d=list(map(tex,ds)); xf,yf=tex(x),tex(y)
 intro='Given a transformation \n\n'+block(r'T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},')+'\n\nthe Jacobian determinant of $T,$ denoted $'+J+'$, is given by\n\n'+block(J+'='+mat(*PARTIALS)+'.')
 signature='x(u,v)' if TEMPLATES[t][0]=='easy' or t=='exp_log' else 'x'
 ys='y(u,v)' if signature=='x(u,v)' else 'y'
 intro+='\n\nHere, we have $'+signature+'='+xf+'$ and $'+ys+'='+yf+'.$\n\nFirst, we find the partial derivatives:\n\n'
 if t in ('tan_product','trig_pair','powers'):
  deriv=r'\begin{aligned}'+r'\\'.join(PARTIALS[i]+'&='+d[i] for i in range(4))+r'\end{aligned}'
 else:
  deriv=r'\begin{aligned}'+PARTIALS[0]+'&='+d[0]+r'&\quad '+PARTIALS[1]+'&='+d[1]+r'\\'+PARTIALS[2]+'&='+d[2]+r'&\quad '+PARTIALS[3]+'&='+d[3]+r'\end{aligned}'
 intro+=block(deriv)+'\n\nTherefore, the corresponding Jacobian determinant is\n\n'
 rows=[J+'&='+mat(*PARTIALS),'&='+mat(*d)]
 if t!='tan_product':
  first=r'\left('+d[0]+r'\right)\cdot\left('+d[3]+r'\right)'
  second=r'\left('+d[1]+r'\right)\cdot\left('+d[2]+r'\right)'
  if t in ('linear','quadratic','linear_log'):
   rows+=['&='+first+'-'+second]
  else:
   rows+=['&='+first,r'&\quad{}-'+second]

 # Preserve the source's extra simplification row for these observed structures.
 if t=='polar':
  rows+=['&='+tex(p['a']*p['b']*u)+r'\left(\cos^2 v+\sin^2 v\right)']
 elif t=='linear': rows+=['&='+str(p['a']*p['d'])+'-'+str(p['b']*p['c'])]
 elif t=='quadratic': rows+=['&='+tex(4*p['a']*p['b']*u*v)+'+'+tex(4*p['a']*p['b']*u*v)]
 elif t=='exp_log': rows+=['&='+tex(ds[0]*ds[3])+'-'+tex(ds[1]*ds[2])]
 rows+=['&='+tex(j)+'.']
 return intro+block(r'\begin{aligned}'+r'\\'.join(rows)+r'\end{aligned}')

def _assemble(level,seed,t,p,profile):
 validate_parameters(t,p); x,y,domain=functions(t,p)
 ds=[sp.diff(x,u),sp.diff(x,v),sp.diff(y,u),sp.diff(y,v)]
 if t=='tan_product': ds[0]=sp.cos(v)/(p['k']*sp.cos(u/p['k'])**2)
 j=clean(ds[0]*ds[3]-ds[1]*ds[2])
 bank=observed_bank(t,p,j) if profile.startswith('observed_') else authored_bank(t,p,ds,j)
 if len(bank)!=5 or any(equivalent(a[1],b[1]) for i,a in enumerate(bank) for b in bank[i+1:]): raise SampleRejected('Whole bank rejected: equivalent choices')
 if sum(equivalent(value,j) for _,value in bank)!=1: raise SampleRejected('Whole bank rejected: ambiguous correct answer')
 canonical={'level':level,'template':t,'parameters':p,'domain':domain}
 finger=hashlib.sha256(json.dumps(canonical,sort_keys=True).encode()).hexdigest()
 display=[(recipe,tex(value)) for recipe,value in bank]
 vector=matrix_tex([['u'],['v']])
 output=matrix_tex([[tex(x)],[tex(y)]])
 if level=='easy' or level=='hard': problem='Find the Jacobian determinant of the transformation $T,$ defined as\n\n'+block('T:'+vector+r'\longrightarrow'+output+'.')
 else: problem='Find the Jacobian determinant of the transformation $T('+vector+')='+output+'.$'
 problem=normalize_prose(problem)
 worked=normalize_prose(solution(t,x,y,ds,j,p))
 content=hashlib.sha256(json.dumps([VERSION,canonical,problem,worked,profile,sorted(display)],sort_keys=True).encode()).hexdigest()
 qid=uuid.uuid5(uuid.UUID(KP_UUID),content); fid=uuid.uuid5(qid,'selection')
 answers=[]; maths={}; correct=None
 for recipe,value in bank:
  aid=str(uuid.uuid5(fid,tex(value))); answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':tex(value)})
  maths[aid]={'expression':sp.srepr(value),'recipe':recipe}
  if equivalent(value,j): correct=aid
 random.Random(seed).shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':worked,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':t,'parameters':p,'parameter_fingerprint':finger,'content_fingerprint':content,'bank_profile':profile,'bank_origin':BANK_PROFILES[profile]['origin'],'authored_extension':level=='hard' or profile.startswith('authored_') or p!=TEMPLATES[t][2],'difficulty_origin':'authored missing level' if level=='hard' else 'observed','source_analysis':{**PROVENANCE,'question_ids':[TEMPLATES[t][1]] if TEMPLATES[t][1] else [],'canonical_id':'e-6810'},'domain':domain,'plot_rating':'none','plot_assets':{},'functions':[sp.srepr(x),sp.srepr(y)],'partial_derivatives':list(map(sp.srepr,ds)),'determinant':sp.srepr(j),'answer_math':maths}}

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'): raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('Only observed radio fields are supported')
 if profile:
  if profile not in BANK_PROFILES: raise ValueError('Unknown bank profile')
  pt=BANK_PROFILES[profile]['template']
  if template and template!=pt: raise ValueError('Template/profile mismatch')
  template=pt
 eligible=[t for t,(l,_,_) in TEMPLATES.items() if l==level]
 if template and template not in eligible: raise ValueError('Template does not belong to requested level')
 rng=random.Random(seed); t=template or rng.choice(eligible)
 profile=profile or ('authored_' if t=='powers' else 'observed_')+t
 for _ in range(100):
  p=dict(parameters) if parameters is not None else sample(t,rng)
  try: return _assemble(level,seed,t,p,profile)
  except ValueError:
   if parameters is not None: raise
 raise SampleRejected('No unambiguous bank after bounded sampling')

# EASY: five observed families; same four derivatives and determinant operation.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: six observed families, including current source q-81263.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: canonical power compositions, matched derivative/chain-rule demands.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question']; g=record['generation']; f=q[':question/answer-fields'][0]
 lines=[f"## Generated {q[':question/difficulty'].split('/')[-1]} — {g['template']}",f"Author metadata: profile `{g['bank_profile']}`, parameters `{g['parameters']}`.",'',q[':question/problem'],'']
 for a in f[':answer-field/choices']: lines+=['- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '')]
 return '\n'.join(lines+['','Worked solution:',q[':question/worked-solution'],''])

def main():
 parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='easy'); parser.add_argument('--seed',type=int,default=0); parser.add_argument('--count',type=int,default=1); parser.add_argument('--template',choices=list(TEMPLATES)); parser.add_argument('--profile',choices=list(BANK_PROFILES)); parser.add_argument('--format',choices=['markdown','json'],default='json'); args=parser.parse_args()
 if args.count<1 or args.difficulty=='all' and (args.template or args.profile): parser.error('Use positive count and specific level for template/profile')
 records=[]; seen=set()
 for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]):
  for i in range(args.count):
   for attempt in range(1000):
    record=generate(level,args.seed+i+attempt*args.count,args.template,profile=args.profile)
    signature=tuple(record['generation']['functions'])
    if signature not in seen:
     seen.add(signature); records.append(record); break
   else: parser.error('Requested count exceeds the available distinct semantic instances')
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__': main()
