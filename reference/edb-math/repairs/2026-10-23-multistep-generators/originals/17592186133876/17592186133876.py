#!/usr/bin/env python3
"""Exact 2D divergence generators and public, parameterized raw evidence replay.

Raw profiles are covariance recipes: scale a whole field, every derivative input,
every derived scalar/vector choice, and all ordered solution rows together.
They are evidence-only; unknown error intent is not promoted to normal banks.
Normal templates have independent bounded coefficients and operation-derived banks.
No EDB writes. See the private extraction/validation evidence for scope and repairs.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, math, random, re, uuid
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).with_suffix('')
VERSION='divergence-2d-v1'
CAPTURE=json.loads((ROOT/'source.json').read_text())
SOURCE=CAPTURE['record']
KP_ID=17592186133876
X,Y=sp.symbols('x y', real=True)
SOURCE_BY_ID={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
# Level scope and response layouts observed at basis 1356; q-105561 is authored moderate.
FAMILIES={
 'q-41817':('easy','cross_polynomial','radio'),
 'q-168601':('easy','zero_component','blank'),
 'q-105554':('easy','trig_power','radio'),
 'q-131170':('easy','cross_rational','radio'),
 'q-131171':('easy','log_product','radio'),
 'q-169201':('easy','cancellation','blank'),
 'q-123172':('easy','opposed_radical','radio'),
 'q-168113':('moderate','fluid','blank'),
 'q-123173':('moderate','exp_trig','radio'),
 'q-123175':('moderate','log_difference','radio'),
 'q-131173':('moderate','exp_product','radio'),
 'q-131174':('moderate','radial_product','radio'),
 'q-105562':('moderate','trig_log','radio'),
 'q-105561':('moderate','exp_cos','radio'),
}
TEMPLATES={v[1]:{'level':v[0],'field_type':v[2],'source_id':k,'origin':'observed'} for k,v in FAMILIES.items()}
TEMPLATES.update({k:{'level':'hard','field_type':'radio','source_id':None,'origin':'authored missing level'} for k in ('affine_log_exp','affine_squares')})
BANK_PROFILES={**{f'raw:{k}':{'template':v[1],'origin':'raw evidence','eligible_default':False} for k,v in FAMILIES.items()},
 **{f'authored:{k}':{'template':k,'origin':'authored operation bank','eligible_default':True} for k,t in TEMPLATES.items() if t['field_type']=='radio'}}

class SampleRejected(ValueError):pass

def tex(v):
 return sp.latex(v).replace(r'\log',r'\ln')
def grouped(v):return r'\left('+v+r'\right)'
def scaled(s,c):
 """An identity coefficient is rendered implicitly; this is a parameter recipe."""
 if c==1:return s
 trailing=''
 if s.endswith('.') or s.endswith(','):s,trailing=s[:-1],s[-1]
 return str(c)+grouped(s)+trailing

def derivative_inputs(s):
 """Ordered formal partial derivative rows; nested parentheses are preserved."""
 pat=re.compile(r'\\frac\{(?:∂|\\partial)\}\{(?:∂|\\partial)\s*([xy])\}\(')
 out=[]
 for m in pat.finditer(s):
  depth=1;i=m.end()
  while i<len(s) and depth:
   if s[i]=='(':depth+=1
   elif s[i]==')':depth-=1
   i+=1
  if depth:raise ValueError('Unbalanced source derivative input')
  out.append((m.group(1),s[m.end():i-1],m.end(),i-1))
 return out

def scale_derivatives(s,c):
 for _,arg,start,end in reversed(derivative_inputs(s)):s=s[:start]+scaled(arg,c)+s[end:]
 return s

def scale_field(s,c):
 # Entire mathematical field RHS is a complete slot, not a short prose token.
 pat=re.compile(r'(\$F\s*=|F\(x,y\)=)([^$\n]+)')
 return pat.sub(lambda m:m[1]+scaled(m[2],c),s)

def scale_solution(s,c):
 s=scale_field(s,c)
 def aligned(m):
  rows=m[1].split(r'\\')
  for i,row in enumerate(rows):
   if '& =' not in row:continue
   lhs,rhs=row.split('& =',1)
   if derivative_inputs(rhs):rhs=scale_derivatives(rhs,c)
   elif re.search(r'\\frac\{(?:∂|\\partial)P\}',rhs):pass
   else:
    lead=rhs[:len(rhs)-len(rhs.lstrip())];tail=rhs[len(rhs.rstrip()):]
    rhs=lead+scaled(rhs.strip(),c)+tail
   rows[i]=lhs+'& ='+rhs
  return r'\begin{aligned}'+r'\\'.join(rows)+r'\end{aligned}'
 return re.sub(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',aligned,s,flags=re.S)

def clean_choice(s):
 # Ignore the Unicode function-application marker for mathematical parsing.
 # Raw profiles retain source notation byte for byte.
 return s.replace('⁡','')

def raw_recipe(source_id,c):
 src=SOURCE_BY_ID[source_id]
 q={':question/problem':scale_field(src[':question/problem'],c)}
 if ':question/difficulty' in src:q[':question/difficulty']=src[':question/difficulty'][':db/ident']
 if ':question/worked-solution' in src:q[':question/worked-solution']=scale_solution(src[':question/worked-solution'],c)
 fields=[]
 for f in src.get(':question/answer-fields',[]):
  out={':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],
       ':answer-field/choices':[{'value':scaled(a[':answer/value'],c),'source_answer':a[':answer/id']} for a in f[':answer-field/choices']]}
  if ':answer-field/correct' in f:out['correct_source']=f[':answer-field/correct'][':answer/id']
  fields.append(out)
 if ':question/answer-fields' in src:q[':question/answer-fields']=fields
 return q

# ============================================================================
# EASY: one symbolic divergence, observed power/trig/quotient/chain workloads.
# a,b are nonzero signed integers with |a|,|b| <=4; cancellation keeps b=-a/3.
# Zero-component and cancellation templates retain blank response shapes.
# ============================================================================
def easy_components(f,p):
 a,b=p['a'],p['b'];r=X**2+Y**2
 return {
  'cross_polynomial':(a*X*Y**2,b*X**2*Y),
  'zero_component':(a*Y**3-1,b*X*Y**2+1),
  'trig_power':(a*Y*sp.sin(X),b*X**2*sp.cos(Y)**2),
  'cross_rational':(a*Y/r,b*X/r),
  'log_product':(a*sp.log(X*Y),b*X*Y),
  'cancellation':(a*X*Y**2,b*Y**3),
  'opposed_radical':(a*sp.sqrt(r),-b*sp.sqrt(r)),
 }[f]

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Same-level symbolic partial derivatives; finite explicit bounds also apply."""
 return generate('easy',seed,template,field_type,parameters,profile)

# ============================================================================
# MODERATE: compute the same two partial derivatives, then substitute a point.
# Familiar angles, y=0 exponential points and integer Pythagorean pairs bound
# arithmetic. Coefficients 1..4; log_difference uses a domain-valid point.
# The unrated source is assigned moderate, never reported as an observed label.
# ============================================================================
def moderate_components(f,p):
 a,b=p['a'],p['b'];r=X**2+Y**2
 return {
  'fluid':(a*X**2*Y,b*X*Y),
  'exp_trig':(a*sp.exp(X)*sp.sin(Y),-b*sp.exp(X)*sp.cos(Y)),
  'log_difference':(a*sp.log(X+Y),b*sp.log(X-Y)),
  'exp_product':(a*X*sp.exp(Y),b*X*Y*sp.exp(Y)),
  'radial_product':(a*X*sp.sqrt(r),b*Y*sp.sqrt(r)),
  'trig_log':(a*Y**2*sp.sin(2*X),b*X*sp.log(Y)),
  'exp_cos':(a*sp.exp(X)*sp.cos(X),b*X*sp.exp(X*Y)),
 }[f]

def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Bounded exact point evaluation without numerical approximations."""
 return generate('moderate',seed,template,field_type,parameters,profile)

# ============================================================================
# HARD: authored missing level; no observed hard question exists.
# Two nonunit affine chain derivatives at an exact point, anchored to e-8740
# and the affine-square sibling e-9489 reduced to two dimensions. No Hessian,
# interpretation, 3D divergence, or added calculus operation is assessed.
# ============================================================================
def hard_components(f,p):
 a,b,d,k=p['a'],p['b'],p['d'],p['k']
 if f=='affine_log_exp':return sp.log(a*X+b*Y),d*X**2*sp.exp(k*Y)
 return (a*X+b*Y)**2,(d*X+k*Y)**2

def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Missing-level authored two-component chain rule workload with nonunit scales."""
 return generate('hard',seed,template,field_type,parameters,profile)

POINTS={
 'fluid':[(1,1),(1,2),(2,1),(2,2)],
 'exp_trig':[(0,sp.pi/2),(0,3*sp.pi/2)],
 'log_difference':[(2,1),(2,-1),(3,1),(3,-1)],
 'exp_product':[(1,0),(2,0),(3,0)],
 'radial_product':[(3,4),(4,3),(-3,4),(3,-4),(5,12),(12,5)],
 'trig_log':[(sp.pi,1),(2*sp.pi,1),(sp.pi/2,1),(3*sp.pi/2,1)],
 'exp_cos':[(sp.pi/2,0),(sp.pi,0)],
 'affine_log_exp':[(1,0),(2,0),(3,0)],
 'affine_squares':[(1,1),(1,-1),(2,1),(2,-1)],
}

def point(p):return tuple(sp.sympify(p[k],locals={'pi':sp.pi}) for k in ('x0','y0'))
def validate_parameters(f,p,raw=False):
 if raw:
  if set(p)!={'c'} or type(p['c']) is not int or not 1<=abs(p['c'])<=4:raise ValueError('Raw scale c must be a nonzero integer with |c|<=4')
  return
 level=TEMPLATES[f]['level'];expected={'a','b'}
 if level!='easy':expected|={'x0','y0'}
 if level=='hard':expected|={'d','k'}
 if set(p)!=expected:raise ValueError(f'Expected parameter keys {sorted(expected)}')
 for k in expected-{'x0','y0'}:
  lo=2 if level=='hard' and k in ('a','d','k') else 1
  v=p[k]
  if type(v)is not int or not lo<=abs(v)<=4 or level!='easy' and v<0:raise ValueError(f'{k} violates finite {level} coefficient bounds')
 if f=='cross_polynomial' and p['a']==p['b']:raise SampleRejected('Cross-polynomial template retains unequal observed component scales')
 if f=='cancellation' and p['a']+3*p['b']!=0:raise ValueError('Cancellation template requires a+3b=0')
 if level!='easy' and point(p) not in POINTS[f]:raise ValueError('Point outside the finite authored arithmetic catalog')
 if level=='hard' and math.gcd(p['a'],p['b'])!=1:raise SampleRejected('Primitive affine logarithm/square coefficients required')
 if f=='affine_squares':
  if math.gcd(p['d'],p['k'])!=1:raise SampleRejected('Primitive second affine square coefficients required')
  u,v=point(p)
  if p['a']*u+p['b']*v==0 or p['d']*u+p['k']*v==0:raise SampleRejected('A hard defining component may not vanish at the point')

def sample(f,rng):
 level=TEMPLATES[f]['level']
 vals=list(range(1,5)) if level!='easy' else [-4,-3,-2,-1,1,2,3,4]
 p={'a':rng.choice(vals),'b':rng.choice(vals)}
 if f=='cancellation':p={'a':rng.choice([-3,3]),'b':0};p['b']=-p['a']//3
 if level=='hard':p.update(a=rng.randint(2,4),d=rng.randint(2,4),k=rng.randint(2,4))
 if level!='easy':p.update(zip(('x0','y0'),map(str,rng.choice(POINTS[f]))))
 return p

def components(f,p):
 level=TEMPLATES[f]['level']
 return {'easy':easy_components,'moderate':moderate_components,'hard':hard_components}[level](f,p)

def reduced(expr):return sp.factor(sp.together(expr))
def add_components(a,b):return tex(a)+'+'+grouped(tex(b))
OPENING='If $F=P\\,i+Q\\,j$ is a vector field on ${R}^{2}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by'
FORMAL=r'\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}'

def normal_recipe(f,p,profile):
 P,Q=components(f,p);px,qy=sp.diff(P,X),sp.diff(Q,Y);div=reduced(px+qy)
 field=TEMPLATES[f]['field_type'];level=TEMPLATES[f]['level']
 vector=grouped(tex(P))+r'\,i+'+grouped(tex(Q))+r'\,j'
 if level=='easy':
  prompt='Given that $F='+vector+',$ what is $\\text{div}\\,F?$'
  answer=div
 else:
  u,v=point(p);answer=sp.simplify(div.subs({X:u,Y:v},simultaneous=True))
  prompt='Consider the vector field $F='+vector+'.$ \nEvaluate $\\nabla\\cdot F$ at the point $('+tex(u)+','+tex(v)+').$'
  if f=='fluid':prompt='The divergence of the velocity field represents the scalar rate of expansion of the fluid per unit of area. '+prompt.replace('F=','V=').replace(' F$',' V$')
 if field=='blank':prompt+='\n\n$\\text{div}\\,'+('V' if f=='fluid' else 'F')+'=$ {{field-1}}'
 # Preserve both held-coordinate components, zeros, and all product/chain terms.
 rows=[r'\nabla\cdot F & ='+FORMAL,
       r' & =\frac{\partial}{\partial x}('+tex(P)+r')+\frac{\partial}{\partial y}('+tex(Q)+')',
       r' & ='+add_components(px,qy),r' & ='+tex(div)+'.']
 solution=OPENING+'\n\n$$\n\\text{div}\\,F=\\nabla\\cdot F='+FORMAL+'.\n$$\n\nWhen differentiating $P$ with respect to $x$, hold $y$ constant; when differentiating $Q$ with respect to $y$, hold $x$ constant.\n\nTherefore, we have\n\n$$\n\\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
 if level!='easy':
  # xreplace simultaneously substitutes every product and protects basis/function labels.
  sub=div.xreplace({X:sp.Symbol('('+tex(u)+')'),Y:sp.Symbol('('+tex(v)+')')})
  ap=px.subs({X:u,Y:v},simultaneous=True);bq=qy.subs({X:u,Y:v},simultaneous=True)
  solution+='\n\nFinally, we evaluate $\\text{div}\\,F$ at the point $('+tex(u)+','+tex(v)+'),$ and obtain\n\n$$\n\\begin{aligned}(\\nabla\\cdot F)('+tex(u)+','+tex(v)+') & ='+tex(sub)+r' \\ & ='+add_components(sp.simplify(ap),sp.simplify(bq))+r' \\ & ='+tex(answer)+r'.\end{aligned}'+'\n$$'
 if f=='fluid':solution=re.sub(r'\bF\b','V',solution)
 vals=[answer];names=['correct divergence']
 if field=='radio':
  # The complete authored bank is chosen before parameters. All four errors are
  # partial-derivative operations, not unrelated numerical perturbations.
  errors=[px-qy,-px-qy,px,2*px+qy]
  if f=='zero_component':raise ValueError('Zero-component bank is blank')
  if level!='easy':errors=[sp.simplify(e.subs({X:u,Y:v},simultaneous=True)) for e in errors]
  vals+=errors;names+=['subtract Q_y','negate both derivatives','omit Q_y','duplicate P_x']
  for i,a in enumerate(vals):
   if a.has(sp.zoo,sp.nan,sp.oo) or a.is_real is False:raise SampleRejected('Invalid whole bank')
   for b in vals[:i]:
    if sp.simplify(a-b)==0:raise SampleRejected('Equivalent complete bank options; reject whole instance')
 q={':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,
    ':question/answer-fields':[{':answer-field/key':'selection' if field=='radio' else 'field-1',':answer-field/type':':answer-field.type/'+field,
      ':answer-field/choices':[{'value':tex(v),'recipe':n} for v,n in zip(vals,names)],'correct_index':0}]}
 return q,{'family':f,'P_x':sp.srepr(px),'Q_y':sp.srepr(qy),'point':list(map(str,point(p))) if level!='easy' else None}

def assemble(q,g,seed):
 q=copy.deepcopy(q)
 canonical=copy.deepcopy(q)
 for f in canonical.get(':question/answer-fields',[]):
  original=f[':answer-field/choices']
  if 'correct_index' in f:f['correct_value']=original[f['correct_index']]['value']
  elif 'correct_source' in f:f['correct_value']=next(a['value'] for a in original if a.get('source_answer')==f['correct_source'])
  f[':answer-field/choices']=sorted([{'value':a['value']} for a in original],key=lambda a:a['value'])
  for key in ('correct_index','correct_source'):f.pop(key,None)
 content=json.dumps({'version':VERSION,'question':canonical},sort_keys=True,ensure_ascii=False)
 ident=lambda tag:str(uuid.uuid5(uuid.NAMESPACE_URL,content+tag))
 q[':question/id']=ident('question')
 for fi,f in enumerate(q.get(':question/answer-fields',[])):
  f[':answer-field/id']=ident('field'+str(fi));answers=[];correct=None
  for i,a in enumerate(f[':answer-field/choices']):
   aid=ident('answer'+str(fi)+a['value']);answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':a['value']})
   if ('correct_index' in f and i==f['correct_index']) or ('correct_source'in f and a.get('source_answer')==f['correct_source']):correct=aid
  if f[':answer-field/type'].endswith('/radio'):random.Random(seed+fi).shuffle(answers)
  f[':answer-field/choices']=answers
  for key in ('correct_index','correct_source'):f.pop(key,None)
  if correct is not None:f[':answer-field/correct']=[':answer/id',correct]
 g.update(version=VERSION,seed=seed,content_sha256=hashlib.sha256(content.encode()).hexdigest(),basis=CAPTURE['basis'],lineage=CAPTURE['lineage'],database_writes=0)
 return {'knowledge_point':{'db_id':KP_ID,'id':SOURCE[':knowledge-point/id'],'title':SOURCE[':knowledge-point/title']},'question':q,'generation':g}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio','blank'):raise ValueError('Unknown field type')
 if profile:
  if profile not in BANK_PROFILES:raise ValueError('Unknown profile')
  implied=BANK_PROFILES[profile]['template']
  if template and template!=implied:raise ValueError('Profile/template mismatch')
  template=implied
 eligible=[n for n,t in TEMPLATES.items() if t['level']==level and (not field_type or t['field_type']==field_type)]
 if not eligible or template and template not in eligible:raise ValueError('Template/level/field mismatch')
 rng=random.Random(seed);f=template or rng.choice(eligible)
 if profile and profile.startswith('raw:'):
  sid=profile[4:];p=dict(parameters) if parameters is not None else {'c':rng.choice([-4,-3,-2,-1,1,2,3,4])}
  validate_parameters(f,p,True);q=raw_recipe(sid,p['c'])
  return assemble(q,{'template':f,'bank_profile':profile,'parameters':p,'origin':'raw evidence only','eligible_learner':False,'evidence_only':True,'eligible_for_learning':False,
    'source_id':sid,'mathematical_fingerprint':hashlib.sha256(json.dumps([f,p],sort_keys=True).encode()).hexdigest()},seed)
 profile=profile or ('authored:'+f if TEMPLATES[f]['field_type']=='radio' else None)
 for _ in range(128):
  p=dict(parameters) if parameters is not None else sample(f,rng)
  try:
   validate_parameters(f,p);q,obj=normal_recipe(f,p,profile)
   return assemble(q,{'template':f,'bank_profile':profile,'parameters':p,'origin':TEMPLATES[f]['origin']+'; authored default bank/standalone presentation',
     'source_id':TEMPLATES[f]['source_id'],'eligible_learner':True,'evidence_only':False,'eligible_for_learning':True,'mathematical_fingerprint':hashlib.sha256(json.dumps(obj,sort_keys=True).encode()).hexdigest()},seed)
  except SampleRejected:
   if parameters is not None:raise
 raise SampleRejected('Bounded complete-bank sampling exhausted')

def markdown(r):
 q=r['question'];lines=['### '+r['generation']['template']+' — '+r['generation']['origin'],'',q[':question/problem'],'']
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:
   correct=a[':answer/id']==f.get(':answer-field/correct',[None,None])[1]
   lines.append('- $'+a[':answer/value']+'$'+(' **correct**' if correct else ''))
 lines+=['',q.get(':question/worked-solution','*No worked solution captured.*')]
 return '\n'.join(lines)

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0)
 ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown')
 ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile',choices=list(BANK_PROFILES));ap.add_argument('--field-type',choices=['blank','radio'])
 args=ap.parse_args()
 if args.count<1:ap.error('count must be positive')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 try:rows=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in levels for i in range(args.count)]
 except ValueError as e:ap.error(str(e))
 print(json.dumps(rows,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
if __name__=='__main__':main()
