#!/usr/bin/env python3
"""Evaluating scalar Cartesian surface integrals; draft v2, stops at step 7.

Ten source-shaped families are served by moderate defaults. Historical opaque
banks are public evidence profiles, parameterized by a positive integrand scale.
Easy/hard are explicitly authored: constant density after cancellation versus
uncancelled quadratic expansion. Each level is unordered and bounded. Read the
adjacent extraction and validation evidence for historical bank limitations.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
import importlib.util
_chain_spec=importlib.util.spec_from_file_location('surface_family_chains',Path(__file__).with_suffix('')/'family_chains.py')
_chains=importlib.util.module_from_spec(_chain_spec);_chain_spec.loader.exec_module(_chains)
DIR=Path(__file__).with_suffix(''); SOURCE=json.loads((DIR/'source.json').read_text())
KP=SOURCE['record']; ID=17592186105887; VERSION='cartesian-surface-2'
x,y,z=s.symbols('x y z',real=True)
QS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
FAMILIES={'plane_xyz':'q-160836','trig_triangle':'q-161355','paraboloid_xy':'q-161340','plane_linear':'q-161341','plane_log':'q-161347','quadratic_triangle':'q-161348','plane_ratio':'q-161352','reciprocal_triangle':'q-161353','plane_sine':'q-161342','cross_cancel':'q-161351'}
MODERATE=list(FAMILIES)
EASY=['constant_plane','canonical_cancel']
HARD=['quadratic_rectangle_full','quadratic_triangle_full']

def tex(v):
 return s.latex(s.sympify(v),ln_notation=True).replace(r'\log',r'\ln')
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,str(v)))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def component_sum(expr,var):
 terms=s.Add.make_args(s.expand(expr))
 return [s.integrate(t,var) for t in terms]
def signed_sum(items):
 return '+'.join('('+tex(v)+')' for v in items) or '0'
def primitive_tex(terms):return signed_sum(terms)
def evaluated(terms,var,value):
 # Keep every signed primitive component individually substituted and evaluated.
 return signed_sum([t.subs(var,value) for t in terms])
def raw_scale(value,c):
 return value if c==1 else tex(c)+r'\left('+value+r'\right)'

def source_parameters(template):return {'scale':1}
def base_math(f,p):
 """Complete components, never substring replacement in learner prose."""
 a,b,C,L,H,K=[s.sympify(p.get(k,v)) for k,v in [('a',1),('b',1),('c',1),('lo',0),('hi',1),('k',1)]]
 bounds=(L,H,s.Integer(0),K)
 if f=='plane_xyz':g=a*x+b*y;F=C*x*y*z
 elif f=='trig_triangle':g=s.sin(x+y);F=C*z/s.sqrt(1+2*s.cos(x+y)**2);bounds=(0,H,-x,x)
 elif f=='paraboloid_xy':g=s.Rational(1,4)+x*x+y*y;F=C*x*y/s.sqrt(z);bounds=(0,H,-K,s.Integer(1))
 elif f=='plane_linear':g=a*x+b*y;F=C*z
 elif f=='plane_log':g=a*x+b*y;F=C*(z-b*y)/(s.sqrt(1+a*a+b*b)*y);bounds=(L,H,1,s.exp(K))
 elif f=='quadratic_triangle':g=a*x-b*y;F=C*(x*x+z*z);bounds=(0,H,0,K*x)
 elif f=='plane_ratio':g=a*x+b*y;F=C*z/(a*s.sqrt(1+a*a+b*b)*x);bounds=(L,H,0,K*x)
 elif f=='reciprocal_triangle':g=K+x+y;F=C/(s.sqrt(3)*z*z);bounds=(0,H,-x,0)
 elif f=='plane_sine':g=a*x;F=C*z*s.sin(y);bounds=(0,H,0,K*s.pi/2)
 elif f=='cross_cancel':g=a*x-b*y;F=C*(2*a*b*x*y+z*z);bounds=(L,H,0,K)
 elif f=='constant_plane':g=a*x+b*y;F=C
 elif f=='canonical_cancel':g=1+x+y*y;F=C/s.sqrt(z-x+y*y);bounds=(L,H,-K,K)
 elif f=='quadratic_rectangle_full':g=a*x-b*y;F=C*(x*x+x*y+z*z);bounds=(L,H,0,K)
 elif f=='quadratic_triangle_full':g=a*x-b*y;F=C*(x*x+x*y+z*z);bounds=(0,H,0,K*x)
 else:raise ValueError('Unknown template')
 return g,F,tuple(map(s.sympify,bounds))
ORIGINAL={
'plane_xyz':dict(a=1,b=1,c=12,lo=0,hi=1,k=1),
'trig_triangle':dict(c=1,hi='pi'),
'paraboloid_xy':dict(c=1,hi=1,k=2),
'plane_linear':dict(a=1,b=1,c=4,lo=0,hi=1,k=1),
'plane_log':dict(a=2,b=1,c=1,lo=1,hi=2,k=1),
'quadratic_triangle':dict(a=5,b=1,c=1,hi=1,k=2),
'plane_ratio':dict(a=4,b=8,c=1,lo=1,hi=2,k=1),
'reciprocal_triangle':dict(c=1,hi='1/2',k=1),
'plane_sine':dict(a=1,c=2,hi=1,k=1),
'cross_cancel':dict(a=3,b=4,c=1,lo=1,hi=2,k=1)}

def validate_parameters(level,f,p):
 if set(p)-{'a','b','c','lo','hi','k'}:raise ValueError('Unknown parameter')
 g,F,bounds=base_math(f,p);a=s.sympify(p.get('a',1));b=s.sympify(p.get('b',1));c=s.sympify(p.get('c',1));k=s.sympify(p.get('k',1));lo,hi,yl,yh=bounds
 if not (c.is_integer and 1<=c<=12):raise ValueError('Coefficient must be an integer 1..12')
 if not(hi>lo and 0<=lo<=2 and hi<=3):
  if not(f=='trig_triangle' and hi in (s.pi/2,s.pi,s.pi*3/2)):raise ValueError('Bound workload')
 if f!='reciprocal_triangle' and not(k.is_integer and 1<=k<=3):raise ValueError('k must be integer 1..3')
 if f=='reciprocal_triangle' and k not in (1,2,3):raise ValueError('Positive offset')
 if not(a.is_integer and b.is_integer and 1<=a<=5 and 1<=b<=8):raise ValueError('Slope workload')
 if f in ('plane_ratio','plane_log') and lo<1:raise ValueError('Positive denominator domain')
 if f=='plane_sine' and k not in (1,3):raise ValueError('Nonzero familiar sine integral')
 if level=='easy' and not(a<=2 and b<=2 and c<=4 and hi-lo<=2):raise ValueError('Easy workload')
 if level=='hard' and not(2<=a<=4 and 1<=b<=2 and c<=3 and k<=2 and hi<=2):raise ValueError('Hard workload')
 return g,F,bounds

def calculation(g,F,bounds):
 dx,dy=s.diff(g,x),s.diff(g,y);metric=s.sqrt(s.factor(1+dx*dx+dy*dy));pull=F.subs(z,g);density=s.simplify(s.trigsimp(pull*metric));density=s.expand(density)
 lo,hi,yl,yh=bounds
 iy=component_sum(density,y);upper=[t.subs(y,yh) for t in iy];lower=[t.subs(y,yl) for t in iy];outer=s.simplify(sum(upper)-sum(lower));ix=component_sum(outer,x);endhi=[t.subs(x,hi) for t in ix];endlo=[t.subs(x,lo) for t in ix];answer=s.simplify(sum(endhi)-sum(endlo))
 return dx,dy,metric,pull,density,iy,upper,lower,outer,ix,endhi,endlo,answer

def method_bank(f,g,F,bounds,data,profile):
 dx,dy,M,pull,D,*_=data;A=data[-1];lo,hi,yl,yh=bounds
 integ=lambda v:s.simplify(s.integrate(s.integrate(v,(y,yl,yh)),(x,lo,hi)))
 # Select a complete operation bank BEFORE parameters. Each wrong operation
 # arises in the actual substitution/integration, not arbitrary value offsets.
 if f=='constant_plane':
  v=[A,integ(pull),integ(pull*M*M),integ(pull*s.sqrt(1+dx*dx)),integ(pull*M)/(yh-yl)]
  recipes=['correct','omit_metric','square_metric','omit_y_partial','omit_y_width']
 elif f=='canonical_cancel':
  c=s.simplify(D/s.sqrt(2));area=(hi-lo)*(yh-yl)
  v=[A,c*area,2*c*area,-A,c*s.sqrt(2)*(hi-lo)]
  recipes=['correct','lose_sqrt_two','replace_sqrt_two_by_two','reverse_inner_limits','omit_y_width']
 elif f=='trig_triangle':
  v=[A,-A,A/2,2*A,s.integrate(s.integrate(D,(y,0,yh)),(x,lo,hi))]
  recipes=['correct','reverse_inner_limits','incorrect_inner_chain_factor_two','duplicate_outer_integral','replace_lower_y_by_zero']
 elif f in ('paraboloid_xy','plane_log','plane_ratio','reciprocal_triangle'):
  # Post-cancellation integration errors: reverse the inner limits, omit the
  # lower endpoint, evaluate over half the outer interval, duplicate the outer
  # integral. A whole bank is rejected if any method values coincide.
  v=[A,-A,integ(D.subs(y,yh)),s.integrate(s.integrate(D,(y,yl,yh)),(x,lo,(hi+lo)/2)),2*A]
  recipes=['correct','reverse_inner_limits','use_upper_value_as_density','half_outer_interval','duplicate_outer_integral']
 else:
  v=[A,integ(pull),integ(pull*(1+dx*dx+dy*dy)),-A,integ(F.subs(z,0)*M)]
  recipes=['correct','omit_metric','square_metric','reverse_inner_limits','substitute_z_zero']
 return [s.simplify(t) for t in v],recipes

def normal(level,f,p,profile):
 g,F,bounds=validate_parameters(level,f,p);data=calculation(g,F,bounds);dx,dy,M,P,D,iy,up,dn,O,ix,eh,el,A=data
 values,recipes=method_bank(f,g,F,bounds,data,profile)
 for i,v in enumerate(values):
  if v.is_real is False or v.has(s.oo,s.zoo,s.nan) or any(s.simplify(v-w)==0 for w in values[:i]):raise ValueError('Whole-bank rejection: equivalent or invalid required operations')
 lo,hi,yl,yh=bounds
 prompt='Evaluate the surface integral\n\n$$\n'+r'\iint_S '+_chains.integrand_tex(f,p,F,data,tex,x,y)+r'\,\mathrm{d}S'+ '\n$$\n\nwhere $S$ is defined by $z='+tex(g)+'$ for $'+tex(lo)+r'\le x\le '+tex(hi)+'$ and $'+tex(yl)+r'\le y\le '+tex(yh)+'$.'
 opening=QS['q-161341'][':question/worked-solution'].split('For the partial derivatives')[0]
 sol=opening+'For the partial derivatives, we have\n\n$$\n'+r'\frac{∂z}{∂x}=\frac{∂}{∂x}('+tex(g)+')='+tex(dx)+',\n$$\n\nand\n\n$$\n'+r'\frac{∂z}{∂y}=\frac{∂}{∂y}('+tex(g)+')='+tex(dy)+'.\n$$\n\nTherefore, the surface integral can be evaluated as follows:\n\n'
 chain,stage_tags=_chains.build(f,p,g,F,bounds,data,tex,signed_sum,component_sum,x,y)
 sol+='$$\n'+chain+'\n$$'
 return prompt,sol,[tex(v) for v in values],0,{'g':g,'F':F,'bounds':bounds},recipes

def raw(level,f,p,profile):
 """Extracted component-mask replay, scaled integrand and complete bank.

Only scalar integral stages are scaled; the actual surface/partials remain
unchanged. At unit scale the original strings and omissions are exact. This
profile never infers historical wrong-operation intent from scalar values.
"""
 if set(p)!={'scale'}:raise ValueError('Raw profiles accept scale only')
 c=s.sympify(p['scale'])
 if not(c.is_integer and 1<=c<=4):raise ValueError('Raw scale 1..4')
 q=QS[FAMILIES[f]];g,F,bounds=base_math(f,ORIGINAL[f]);prompt=q[':question/problem']
 # Complete surface integral body is one extracted slot, protected from prose.
 if f=='plane_xyz':body='12xyz';replacement=tex(12*c)+'xyz'
 else:
  m=re.search(r'(?:\{∬\}_\{S\})(.*?)(\\,\\text\{d\}S)',prompt,re.S);assert m,prompt
  body=m[1];replacement=raw_scale(body,c)
 prompt=prompt.replace(body,replacement,1)
 solution=None
 if ':question/worked-solution' in q:
  solution=q[':question/worked-solution'];start=solution.index(r'\begin{aligned}');end=solution.index(r'\end{aligned}',start)
  block=solution[start+len(r'\begin{aligned}'):end];rows=block.split(r'\\')
  transformed=[]
  for i,row in enumerate(rows):
   lhs,rhs=row.split('& =',1)
   if i==0:lhs=lhs.replace(body,replacement,1)
   # The formal operator row already denotes f from the scaled prompt.
   if 'f(x,y,g(x,y))' not in rhs:rhs=raw_scale(rhs.strip(),c) if c!=1 else rhs
   transformed.append(lhs+'& ='+rhs)
  solution=solution[:start]+r'\begin{aligned}'+r'\\'.join(transformed)+solution[end:]
 values=[raw_scale(a[':answer/value'],c) for a in q[':question/answer-fields'][0][':answer-field/choices']]
 correct=q[':question/answer-fields'][0].get(':answer-field/correct');ci=None
 if correct:ci=next(i for i,a in enumerate(q[':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==correct[':answer/id'])
 return prompt,solution,values,ci,{'g':g,'F':c*F,'bounds':bounds},['observed_scalar_component_scaled_unresolved']*5

def sample(level,f,rng):
 p={'a':rng.randint(1,2 if level=='easy' else 4),'b':rng.randint(1,2),'c':rng.randint(1,4 if level=='easy' else 3),'lo':rng.randint(0,1),'hi':rng.randint(1,2),'k':rng.randint(1,2)}
 if p['hi']<=p['lo']:p['hi']=p['lo']+1
 if f in ('plane_log','plane_ratio'):p.update(lo=1,hi=2)
 if f=='trig_triangle':p.update(hi=rng.choice(['pi/2','pi','3*pi/2']))
 if f=='plane_sine':p.update(k=rng.choice([1,3]))
 if f=='paraboloid_xy':p.update(k=2)
 if f=='reciprocal_triangle':p.update(hi=rng.choice(['1/2',1,'3/2']),k=rng.randint(1,3))
 if level=='hard':p['a']=rng.randint(2,4)
 return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio shape is supported')
 rng=random.Random(seed);f=template or rng.choice({'easy':EASY,'moderate':MODERATE,'hard':HARD}[level]);israw=profile is not None and profile.startswith('raw:')
 if f not in {'easy':EASY,'moderate':MODERATE,'hard':HARD}[level]:raise ValueError('Template outside difficulty')
 if israw and (f not in FAMILIES or profile!='raw:'+FAMILIES[f]):raise ValueError('Raw profile/template mismatch')
 selected=profile or ('authored:integration_stages' if f in ('canonical_cancel','paraboloid_xy','trig_triangle','plane_log','plane_ratio','reciprocal_triangle') else 'authored:surface_stages')
 if not israw and selected not in ('authored:integration_stages','authored:surface_stages'):raise ValueError('Unknown profile')
 expected_profile='authored:integration_stages' if f in ('canonical_cancel','paraboloid_xy','trig_triangle','plane_log','plane_ratio','reciprocal_triangle') else 'authored:surface_stages'
 if not israw and selected!=expected_profile:raise ValueError('Profile outside template eligibility')
 for attempt in range(200):
  p=parameters if parameters is not None else ({'scale':rng.randint(1,4)} if israw else sample(level,f,rng))
  try:prompt,sol,values,ci,math,recipes=(raw if israw else normal)(level,f,p,selected);break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('No eligible whole instance')
 # Identity is content, no unused parameters, seed, shuffle, profile aliases.
 identity=digest({'v':VERSION,'difficulty':None if israw and ':question/difficulty' not in QS[FAMILIES[f]] else level,'prompt':prompt,'solution':sol,'bank':sorted(values),'correct':None if ci is None else values[ci]})
 fieldid=uid(identity+':selection');answers=[{':answer/id':uid(fieldid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 field={':answer-field/id':fieldid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if ci is not None:field[':answer-field/correct']=[':answer/id',answers[ci][':answer/id']]
 rng.shuffle(answers)
 q={':question/id':uid(identity),':question/problem':prompt,':question/answer-fields':[field]}
 if not israw or ':question/difficulty' in QS[FAMILIES[f]]:q[':question/difficulty']=':question.difficulty/'+level
 if sol is not None:q[':question/worked-solution']=sol
 g,F,bounds=math['g'],math['F'],math['bounds']
 fingerprint=digest({'F':s.srepr(F),'g':s.srepr(g),'bounds':[s.srepr(v) for v in bounds],'response':'evaluate_surface_integral'})
 return {'knowledge_point':{'db_id':ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':f,'profile':selected,'parameters':p,'seed':seed,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_ids':[FAMILIES[f]] if f in FAMILIES else [],'eligible_for_learning':not israw,'evidence_only':israw,'authored_level':level!='moderate' or (not israw and f=='plane_xyz'),'recipes':recipes,'content_identity':identity,'mathematical_fingerprint':fingerprint,'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'domain':list(map(str,bounds))}}
# Easy: two authored constant-after-substitution workloads, no nonconstant integral.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: ten observed families, method-derived complete default banks.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: five distributed terms, three surviving terms; bounded slopes 2..4.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
 q=r['question'];text=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):text+='\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'
 return text+q.get(':question/worked-solution','[Original worked solution absent.]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 out=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(out,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in out))
