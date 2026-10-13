#!/usr/bin/env python3
"""Direct plane vector-field line-integral evaluation; frozen step-7 draft.

Eight observed moderate radio families, each with a public homogeneous evidence
profile. Opaque historical scalar choices are not claimed as recovered error
algorithms. Normal families use complete independently derived operation banks.
Easy and hard are authored, with distinct enforced workloads. No plots or EDB.
"""
from pathlib import Path
import argparse, hashlib, json, random, sys, uuid
from functools import lru_cache
import sympy as s

KP_ID=17592186133828
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
KP=SOURCE['record']
VERSION='plane-line-integral-1'
x,y,t=s.symbols('x y t', real=True)
NAMESPACE=uuid.UUID(KP[':knowledge-point/id'])
FAMILIES=['log','polynomial','offset_circle','rotation','spiral','parabola','rational','arcsine']
QUESTIONS=dict(zip(FAMILIES,KP[':knowledge-point/questions']))
TEMPLATES={'affine':'easy',**{f:'moderate' for f in FAMILIES},'mixed_power':'hard'}
# Opaque source banks have a defined homogeneous extension, used only as evidence.
OPAQUE={
 'log':[4,2,3,1,0], 'polynomial':[s.Rational(55,4),s.Rational(27,4),s.Rational(35,4),s.Rational(89,4),s.Rational(109,4)],
 'offset_circle':[-1,0,2,-2,1], 'rotation':[s.pi,2*s.pi,0,1,2],
 'spiral':[2,2*s.pi**2,s.pi,s.pi**2,2*s.pi], 'parabola':[3,1,4,0,2],
 'rational':[-7,-2,9,2,-11], 'arcsine':[-4-s.sqrt(2),s.sqrt(2),1-s.sqrt(3),-2+s.sqrt(3),2-s.sqrt(3)]}
CORRECT_INDEX={'log':0,'polynomial':4,'offset_circle':2,'rotation':0,'spiral':1,'parabola':1,'rational':0,'arcsine':4}

def tex(e):
 return s.latex(s.sympify(e),order='lex').replace(r'\log',r'\ln')
def uid(v): return str(uuid.uuid5(NAMESPACE,v))
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def group(e): return '('+tex(e)+')'
def vec(a,b): return group(a)+r'\,i+'+group(b)+r'\,j'
def align(rows): return '$$\n'+r'\begin{aligned}'+r' \\ '.join(lhs+' & ='+rhs for lhs,rhs in rows)+r'\end{aligned}'+'\n$$'
@lru_cache(maxsize=4096)
def integrate(e,a,b): return s.simplify(s.integrate(s.trigsimp(s.expand_trig(e)),(t,a,b)))

class SampleRejected(ValueError): pass

def model(f,p):
 """Exact components, orientation and closed nonsingular interval."""
 c=s.Integer(p.get('c',1))
 if f=='log': return (c*s.exp(x),2*c*y,s.log(t),t,s.Integer(p['a']),s.Integer(p['b']))
 if f=='polynomial': return (c*x*x*y,c*(x+1),3*t,2+t,s.Integer(p['a']),s.Integer(p['b']))
 if f=='offset_circle': return (c*x,c*(y-1),s.sin(t),s.cos(t),s.pi*p['a']/2,s.pi*p['b']/2)
 if f=='rotation': return (c*y,-c*x,s.sin(t),s.cos(t),s.pi*p['a']/2,s.pi*p['b']/2)
 if f=='spiral': return (c*x,c*y,t*s.sin(t),t*s.cos(t),s.pi*p['a']/2,s.pi*p['b']/2)
 if f=='parabola': return (c*y,c*x,t,t*t,s.Integer(p['a']),s.Integer(p['b']))
 if f=='rational': return (c*(y+1)/x,-2*c*(x-1)/y,t*t,t-1,s.Integer(p['a']),s.Integer(p['b']))
 if f=='arcsine': return (c*y*s.sin(x),c*(x+y),s.asin(t),s.Integer(2),s.Rational(p['a']),s.Rational(p['b']))
 if f=='affine':
  return (p['A']*y,p['B']*x+p['D']*y,p['h']+p['u']*t,p['k']+p['v']*t,s.Integer(0),s.Integer(1))
 if f=='mixed_power':
  return (p['A']*x*y+p['B']*y,p['D']*x*x+p['E']*y,p['u']*t*t,p['v']*t**3+p['k'],s.Integer(0),s.Integer(1))
 raise ValueError(f)

ORIGINAL_PARAMETERS={f:{'c':1,'a':0,'b':1} for f in FAMILIES}
ORIGINAL_PARAMETERS.update({'log':{'c':1,'a':1,'b':2},'offset_circle':{'c':1,'a':0,'b':2},'rotation':{'c':1,'a':0,'b':2},'spiral':{'c':1,'a':0,'b':4},'rational':{'c':1,'a':3,'b':4},'arcsine':{'c':1,'a':'0','b':'1/2'}})

def guard(f,p,observed=False):
 if f in FAMILIES:
  if set(p)!= {'c','a','b'}: raise ValueError('Expected c,a,b')
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
  if observed and (p['a'],p['b'])!=(ORIGINAL_PARAMETERS[f]['a'],ORIGINAL_PARAMETERS[f]['b']): raise ValueError('Observed masks retain source interval; use method profile for endpoint changes')
 else:
  keys={'A','B','D','h','k','u','v'} if f=='affine' else {'A','B','D','E','u','v','k'}
  if set(p)!=keys or any(type(v) is not int or abs(v)>4 for v in p.values()): raise ValueError('Exact seven bounded integer parameters required')
  mandatory=keys-({'h','k'} if f=='affine' else set())
  if any(p[z]==0 for z in mandatory): raise ValueError('Defining coefficients must be nonzero')
  if f=='affine' and (abs(p['u'])==1 or abs(p['v'])==1): raise ValueError('Nonunit line slopes preserve bank distinctions')
  if f=='affine' and p['A']*p['v']*p['u']+(p['B']*p['u']+p['D']*p['v'])*p['v']==0: raise SampleRejected('Affine integral must retain its linear term')

def sample(f,rng):
 if f in FAMILIES:
  p=dict(ORIGINAL_PARAMETERS[f]); p['c']=rng.choice([z for z in range(-6,7) if z])
  if f=='arcsine': p['a'],p['b']=rng.choice([('0','1/2'),('0','3/4'),('1/4','1/2'),('1/4','3/4'),('1/2','3/4')])
  elif f in ['offset_circle','rotation','spiral']: p['a'],p['b']=sorted(rng.sample(range(5),2))
  else:
   lo,hi=(2,5) if f=='rational' else (1,4) if f=='log' else (0,4) if f=='parabola' else (0,2)
   p['a'],p['b']=sorted(rng.sample(range(lo,hi+1),2))
  return p
 keys=['A','B','D','h','k','u','v'] if f=='affine' else ['A','B','D','E','u','v','k']
 p={k:rng.choice([-4,-3,-2,2,3,4]) for k in keys}; return p

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
 terms=s.Add.make_args(primitive)
 def endpoint(z): return '+'.join(group(s.simplify(v.subs(t,z))) for v in terms)
 prompt=r'Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)='+vec(P,Q)+r'$ and $C$ is the path $r(t)='+vec(X,Y)+r'$ for $t\in['+tex(a)+','+tex(b)+r'].$'
 sol='We will use the formula\n\n'+ '$$\n'+r'\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.'+'\n$$'
 sol+='\n\nAlong the curve $C,$ we have\n\n$$\nx='+tex(X)+r',\quad y='+tex(Y)+'.\n$$'
 # Unevaluated substitution deliberately retains nested products and sums.
 up=P.subs({x:X,y:Y},simultaneous=True); uq=Q.subs({x:X,y:Y},simultaneous=True)
 sol+='\n\nTherefore,\n\n'+align([('F(r(t))',vec(P,Q)),('',vec(up,uq)),('',vec(FP,FQ))])
 sol+='\n\nComputing $r^{\\prime}(t),$ we get\n\n'+align([(r'r^{\prime}(t)',r'\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j'),('',r'\frac{\text{d}}{\text{d}t}('+tex(X)+r')\,i+\frac{\text{d}}{\text{d}t}('+tex(Y)+r')\,j'),('',vec(dx,dy))])
 sol+='\n\nTherefore,\n\n'+align([(r'F(r(t))\cdot r^{\prime}(t)','('+vec(FP,FQ)+r')\cdot('+vec(dx,dy)+')'),('',group(FP)+r'\cdot'+group(dx)+'+'+group(FQ)+r'\cdot'+group(dy)),('',group(A)+'+'+group(B)),('',tex(integrand))])
 value=integrate(integrand,a,b)
 sol+='\n\nFinally, we can evaluate the integral, as follows:\n\n'+align([(r'\int_C F\cdot\text{d}r',r'\int_{'+tex(a)+'}^{'+tex(b)+r'}F(r(t))\cdot r^{\prime}(t)\,\text{d}t'),('',r'\int_{'+tex(a)+'}^{'+tex(b)+'}('+tex(integrand)+r')\,\text{d}t'),('',r'\left['+tex(primitive)+r'\right]_{'+tex(a)+'}^{'+tex(b)+'}'),('','('+endpoint(b)+')-('+endpoint(a)+')'),('',group(primitive.subs(t,b))+'-'+group(primitive.subs(t,a))),('',tex(value))])
 return prompt,sol

# Complete method banks are selected before parameters. Family-specific errors
# avoid a universal answer +/- perturbation bank. No first-valid replacement.
def bank(f,m,profile):
 P,Q,X,Y,a,b=m; FP=P.subs({x:X,y:Y},simultaneous=True); FQ=Q.subs({x:X,y:Y},simultaneous=True); dx=s.diff(X,t);dy=s.diff(Y,t)
 correct=integrate(FP*dx+FQ*dy,a,b)
 if f=='rotation':
  errors=[('omit_y_component',FP*dx),('subtract_y_product',FP*dx-FQ*dy),('double_x_component',2*FP*dx+FQ*dy),('double_both_derivatives',2*(FP*dx+FQ*dy))]
 elif f=='offset_circle':
  errors=[('omit_x_component',FQ*dy),('omit_constant_offset',FP*dx+(FQ+P/x)*dy),('reverse_y_derivative',FP*dx-FQ*dy),('forget_negative_cosine_derivative',FP*dx+FQ*s.sin(t))]
  # Last two would be identical: use forgetting all coordinate derivatives.
  errors[-1]=('omit_both_derivatives',FP+FQ)
 elif f=='spiral':
  c=s.simplify(P/x)
  errors=[('omit_radial_product_rule_terms',c*X*t*s.cos(t)+c*Y*(-t*s.sin(t))),('double_radial_product_rule_terms',2*c*X*s.sin(t)+c*X*t*s.cos(t)+2*c*Y*s.cos(t)-c*Y*t*s.sin(t)),('omit_t_in_field',c*s.sin(t)*dx+c*s.cos(t)*dy),('omit_one_product_rule_term',FP*(dx-s.sin(t))+FQ*dy)]
 elif f=='arcsine':
  c=s.simplify(P/(y*s.sin(x)))
  errors=[('omit_inverse_sine_derivative',FP),('replace_sqrt_by_radicand',2*c*t/(1-t*t)),('reverse_primitive_sign',-FP*dx),('differentiate_as_sqrt',2*c*t*s.sqrt(1-t*t))]
 elif f=='parabola':
  errors=[('swap_coordinate_derivatives',FP*dy+FQ*dx),('omit_t_in_y_derivative',FP*dx+FQ*2),('omit_x_component',FQ*dy),('omit_y_component',FP*dx)]
 elif f=='log':
  errors=[('omit_log_derivative',FP+FQ*dy),('omit_exponential_component',FQ*dy),('differentiate_log_as_negative_reciprocal',-FP*dx+FQ*dy),('omit_y_derivative_and_field_factor',FP*dx+FQ/2)]
 else:
  errors=[('omit_x_derivative',FP+FQ*dy),('omit_y_derivative',FP*dx+FQ),('omit_x_component',FQ*dy),('subtract_y_product',FP*dx-FQ*dy)]
  if f in ['polynomial','parabola','rational']:
   errors[1]=('omit_y_component',FP*dx)
 vals=[correct]+[integrate(expr,a,b) for _,expr in errors]
 if any(v.has(s.oo,s.zoo,s.nan) for v in vals) or any(s.simplify(v-w)==0 for i,v in enumerate(vals) for w in vals[:i]): raise SampleRejected('Complete operation bank collides or is invalid')
 # Avoid unique sign and uniquely integer/noninteger correct-answer cues.
 sign=s.sign(correct)
 if sum(s.sign(v)==sign for v in vals)<2: raise SampleRejected('Unique correct sign')
 if sum(v.is_Integer==correct.is_Integer for v in vals)<2: raise SampleRejected('Unique correct number type')
 return vals,['correct']+[name for name,_ in errors]

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if field_type not in [None,'radio']:raise ValueError('Only observed radio layout supported')
 if profile and profile.startswith('observed_'):
  family=profile[len('observed_'):]
  if template is not None and template!=family:raise ValueError('Profile/template mismatch')
  template=family
 elif profile not in [None,'method']:raise ValueError('Unknown profile')
 eligible=[f for f,l in TEMPLATES.items() if l==level]
 if template is not None and template not in eligible:raise ValueError('Template outside level')
 rng=random.Random(seed); f=template or rng.choice(eligible); observed=bool(profile and profile.startswith('observed_')); profile=profile or 'method'
 for attempt in range(200):
  p=dict(parameters) if parameters is not None else (dict(ORIGINAL_PARAMETERS[f],c=rng.choice([1,2,3,-1,-2,-3])) if observed else sample(f,rng))
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
    vals,recipes=bank(f,m,profile);idx=0;prompt,sol=normal_text(f,p,m);strings=[tex(v) for v in vals]
   break
  except SampleRejected:
   if parameters is not None:raise
 else:raise SampleRejected('No eligible complete bank in bounded sampler')
 task=digest([level,[s.srepr(z) for z in m]])
 content=digest([VERSION,level,prompt,sol,sorted(strings)])
 qid=uid(content);fid=uid(qid+':selection');answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in strings]
 correct=answers[idx][':answer/id'];rng.shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':s.__version__,'seed':seed,'template':f,'parameters':p,'bank_profile':profile,'bank_origin':'observed opaque homogeneous evidence' if observed else 'authored method-derived','evidence_only':observed,'eligible_for_learning':not observed,'authored_extension':not observed,'difficulty_origin':'observed' if level=='moderate' else 'authored','parameter_fingerprint':task,'content_fingerprint':content,'source':{k:SOURCE[k] for k in ['database','basis','lineage']},'source_ids':[QUESTIONS[f][':question/id']] if f in FAMILIES else [],'recipes':recipes,'plot_rating':'none'}}

# EASY — authored canonical linear field on affine line, nonunit slopes.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — eight observed nonlinear substitution/derivative families, unordered.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — authored two non-affine power coordinates and four nonzero field terms.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return ('### Generated — '+q[':question/difficulty'].split('/')[-1]+' / '+rec['generation']['template']+' / '+rec['generation']['bank_profile']+'\n\n'+q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution'])
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=['markdown','json'],default='markdown');a=ap.parse_args()
 if a.count<1:ap.error('Positive count required')
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 recs=[generate(l,a.seed+i,a.template,profile=a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(recs,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,recs)))
if __name__=='__main__':main()
