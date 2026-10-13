#!/usr/bin/env python3
"""Direct 3D vector-field line integrals. Local step-7 draft; never uses EDB.

Frozen source: math, basis 1356. Eight observed families retain full public
historical masks/banks as ineligible evidence. Their scalar-field lifts are
parameterized by linearity, without inventing intentions for opaque wrong values.
Normal generators choose complete operation banks before sampling parameters,
reject whole collisions, and compute F(r(t)).r'(t) directly. See private README.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s

ROOT=Path(__file__).with_suffix('')
CAPTURE=json.loads((ROOT/'source.json').read_text())
KP=CAPTURE['record']; KP_ID=17592186133894
VERSION='space-vector-direct-1'
NS=uuid.UUID(KP[':knowledge-point/id'])
x,y,z,t=s.symbols('x y z t',real=True)
OBSERVED={
 'product':17592186134088, 'helix_root':17592186134089,
 'mixed_polynomial':17592186259708, 'trig_cancel':17592186259710,
 'exp_cancel_xy':17592186259714, 'exp_cancel_yz':17592186259717,
 'quotient_exp':17592186284546, 'radical_power':17592186284547,
}
OLDS={q[':db/id']:q for q in KP[':knowledge-point/questions']}
TEMPLATES={'constant_affine':'easy','diagonal_power':'moderate',**dict.fromkeys(OBSERVED,'hard')}
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
 if name=='constant_affine':
  F=(A,B,C); r=tuple(s.sympify(p['v'+q])*t+s.sympify(p['h'+q]) for q in 'xyz')
 elif name=='diagonal_power':F=(A*x,B*y,C*z);r=(t,t**2,t**3)
 elif name=='product':F=(y*z,x*z,x*y);r=(A*t,B*t**2,C*t**3)
 elif name=='mixed_polynomial':F=(x+z,z-y,z**2);r=(A*t**2,B*t**2,C*t)
 elif name=='trig_cancel':F=(x,z,y);r=(-A*s.sin(t),B*s.sec(t),C*s.cos(t))
 elif name=='exp_cancel_xy':
  k,l=map(s.sympify,(p['k'],p['l'])); F=(y,x,z);r=(A*s.exp(-k*t),B*s.exp(k*t),C*s.exp(l*t))
 elif name=='exp_cancel_yz':
  k,l=map(s.sympify,(p['k'],p['l']));F=(x,z,y);r=(A*s.exp(k*t),B*s.exp(l*t),C*s.exp(-l*t))
 elif name=='quotient_exp':
  k,l=map(s.sympify,(p['k'],p['l']));F=(z/x,z/y,s.Integer(1));r=(A*s.exp(k*t),B*s.exp(l*t),C*t)
 elif name=='radical_power':F=(s.sqrt(x),s.sqrt(y),z);r=(A*t,B*t,C*t**2)
 elif name=='helix_root':F=(x,y,z);r=(A*s.cos(t),A*s.sin(t),C*s.sqrt(t))
 else:raise ValueError('Unknown template '+name)
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
 'constant_affine':('correct','reverse_orientation','omit_x','omit_y','omit_z'),
 'diagonal_power':('correct','reverse_orientation','omit_x','omit_y','omit_z'),
 'product':('correct','omit_x','omit_y','omit_z','do_not_differentiate_curve'),
 'mixed_polynomial':('correct','omit_x','omit_y','omit_z','do_not_differentiate_curve'),
 'exp_cancel_xy':('correct','omit_x','omit_y','omit_z','do_not_differentiate_curve'),
 'exp_cancel_yz':('correct','omit_x','omit_y','omit_z','do_not_differentiate_curve'),
 'trig_cancel':('correct','reverse_orientation','omit_half_in_sin_squared_primitive','drop_sine_square_in_primitive','omit_lower_endpoint_of_cosine_primitive'),
 'radical_power':('correct','omit_both_radicals','omit_z','omit_factor_two_in_z_derivative','reverse_orientation'),
 'quotient_exp':('correct','omit_both_quotient_components','omit_z','fail_cancel_first_exponential','fail_cancel_both_exponentials'),
 'helix_root':('correct','omit_z','omit_half_in_sqrt_derivative','replace_sqrt_denominator_by_t','move_sqrt_denominator_to_numerator'),
}
def integrate_on(expr,m):
 anti=s.integrate(s.simplify(expr),t)
 return s.simplify(anti.subs(t,m['b'])-anti.subs(t,m['a']))
def operation_bank(name,p,m):
 Q=m['q'];P=m['products'];a,b=m['a'],m['b'];A,C=map(s.sympify,(p['A'],p['C']))
 if name in ('constant_affine','diagonal_power'):vals=[Q,-Q,*[integrate_on(sum(P)-v,m) for v in P]]
 elif name in ('product','mixed_polynomial','exp_cancel_xy','exp_cancel_yz'):
  vals=[Q,*[integrate_on(sum(P)-v,m) for v in P],integrate_on(sum(m['f']),m)]
 elif name=='trig_cancel':vals=[Q,-Q,2*Q,A*A*(s.sin(b)-s.sin(a))/2,-A*A*s.cos(2*b)/4]
 elif name=='radical_power':
  R=integrate_on(P[0]+P[1],m);Z=integrate_on(P[2],m);vals=[Q,Z,R,R+Z/2,-Q]
 elif name=='quotient_exp':
  k,l=map(s.sympify,(p['k'],p['l']));vals=[Q,C*(b-a),integrate_on(P[0]+P[1],m),integrate_on(C*k*t*s.exp(-k*t)+P[1]+C,m),integrate_on(C*k*t*s.exp(-k*t)+C*l*t*s.exp(-l*t)+C,m)]
 elif name=='helix_root':vals=[Q,0,2*Q,C*C*(s.sqrt(b)-s.sqrt(a)),C*C*(b*b-a*a)/4]
 vals=list(map(s.simplify,vals))
 if any(equal(v,w) for idx,v in enumerate(vals) for w in vals[:idx]):raise ValueError('Whole-bank collision')
 if any(v.has(s.nan,s.zoo,s.oo,-s.oo) or v.is_real is False for v in vals):raise ValueError('Invalid whole bank')
 return vals

def bounds(name,p,level):
 expected=set(SOURCE_PARAMETERS.get(name,dict(A=1,B=1,C=1,a=0,b=1)))
 if name=='constant_affine':expected|={'vx','vy','vz','hx','hy','hz'}
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
  if not a.is_Integer or not b.is_Integer or not 1<=a<b<=4:raise ValueError('Positive familiar radical endpoints required')
 else:
  if not a.is_Integer or not b.is_Integer or not 0<=a<b<=2:raise ValueError('Small integer endpoint bound')
 for key in ('k','l'):
  if key in p and s.sympify(p[key]) not in (1,2,3):raise ValueError('Familiar exponential rates')
 if name=='constant_affine':
  for q in 'xyz':
   if p['v'+q] not in (-3,-2,-1,1,2,3) or p['h'+q] not in range(-3,4):raise ValueError('Affine workload bound')

def sample(name,rng):
 scales=[1,2,3] if name in ('radical_power','helix_root') else [-3,-2,-1,1,2,3]
 p=dict(A=rng.choice(scales),B=rng.choice(scales),C=rng.choice(scales),a=0,b=rng.choice([1,2]))
 if name=='constant_affine':p.update({key+r:rng.choice([-3,-2,-1,1,2,3]) if key=='v' else rng.randint(-3,3) for key in ('v','h') for r in 'xyz'})
 elif name=='trig_cancel':p['b']=rng.choice(['pi/6','pi/4','pi/3'])
 elif name=='helix_root':p.update(a=rng.choice([1,2]),b=rng.choice(['pi','2*pi']));p['B']=p['A']
 elif name=='radical_power':p.update(a=rng.choice([1,2]),b=rng.choice([3,4]))
 elif name in ('exp_cancel_xy','exp_cancel_yz','quotient_exp'):p.update(k=rng.randint(1,3),l=rng.randint(1,3))
 return p

def substitution_tex(expr,r):
 # Replace complete symbol atoms, including product factors and sqrt arguments.
 # Held symbols are outside TeX until their mathematical arguments are replaced.
 rendered=tex(expr)
 return re.sub(r'(?<![A-Za-z\\])([xyz])(?![A-Za-z])',lambda m:r'\left('+tex(r['xyz'.index(m[1])])+r'\right)',rendered)

def normal_text(name,p,m):
 F,r,f,d=m['F'],m['r'],m['f'],m['d'];a,b=m['a'],m['b']
 prompt=r'Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)='+vector(F)+r'$ and $C$ is the path $r(t)='+vector(r)+r'$ for $t\in ['+tex(a)+','+tex(b)+r']$.'
 formal='+'.join(r'\frac{\mathrm{d}'+q+r'}{\mathrm{d}t}\,'+basis for q,basis in zip('xyz','ijk'))
 operators='+'.join(r'\frac{\mathrm{d}}{\mathrm{d}t}\left('+tex(v)+r'\right)\,'+basis for v,basis in zip(r,'ijk'))
 subvec='+'.join(r'\left('+substitution_tex(v,r)+r'\right)\,'+basis for v,basis in zip(F,'ijk'))
 product_row=uneval_sum([r'\left('+tex(q)+r'\right)\cdot\left('+tex(v)+r'\right)' for q,v in zip(f,d)])
 distributed=uneval_sum([tex(v) for product in m['products'] for v in summands(product)])
 anti_terms=summands(m['anti'])
 subendpoint=[];evalendpoint=[]
 for term in anti_terms:
  at=lambda endpoint:re.sub(r'(?<![A-Za-z\\])t(?![A-Za-z])',lambda _:r'\left('+tex(endpoint)+r'\right)',tex(term))
  subendpoint.extend([at(b),r'-\left('+at(a)+r'\right)'])
  evalendpoint.extend([tex(term.subs(t,b)),tex(-term.subs(t,a))])
 final_lhs=r'\int_C F\cdot\mathrm{d}r'
 inthead=r'\int_{'+tex(a)+'}^{'+tex(b)+'}'
 rows=[inthead+r'F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t',inthead+r'\left('+tex(m['I'])+r'\right)\,\mathrm{d}t',r'\left['+tex(m['anti'])+r'\right]_{'+tex(a)+'}^{'+tex(b)+'}',uneval_sum(subendpoint),uneval_sum(evalendpoint),tex(m['q'])]
 solution='We will use the formula\n\n'+block(r'\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.')
 solution+='\n\nAlong the curve $C,$ we have \n\n'+block(',\\qquad '.join(q+'='+tex(v) for q,v in zip('xyz',r))+'.')
 solution+='\n\nTherefore,\n\n'+aligned('F(r(t))',[vector(F),subvec,vector(f)])
 solution+='\n\nComputing $r^{\\prime}(t),$ we get \n\n'+aligned(r'r^{\prime}(t)',[formal,operators,vector(d)])
 solution+='\n\nTherefore,\n\n'+aligned(r'F(r(t))\cdot r^{\prime}(t)',[r'\left('+vector(f)+r'\right)\cdot\left('+vector(d)+r'\right)',product_row,distributed,tex(m['I'])])
 solution+='\n\nFinally, we evaluate the integral as follows:\n\n'+aligned(final_lhs,rows)
 return prompt,solution

# Historical full mathematical masks. These masks preserve source prose, row
# counts, exact component spelling, missing attributes and anomalies. A lift of
# the field scales every F-dependent complete RHS, including all primitives and
# endpoint expressions; derivatives/coordinates remain fixed. At lift 1, the
# multiplicative unit is printed invisibly, as in ordinary algebra rendering.
def lift_rhs(rhs,c):
 if c==1:return rhs
 suffix=''
 rhs=rhs.rstrip()
 if rhs.endswith('.') :rhs=rhs[:-1];suffix='.'
 return r'\left('+tex(c)+r'\right)\cdot\left('+rhs+r'\right)'+suffix
def lift_block(body,c):
 parts=body.split('=')
 if len(parts)==1:return body
 # End aligned environment belongs to layout, never to a mathematical slot.
 result=[parts[0]]
 for rhs in parts[1:]:
  trailer=''
  if r'\end{aligned}' in rhs:rhs,trailer=rhs.split(r'\end{aligned}',1);trailer=r'\end{aligned}'+trailer
  match=re.search(r'\s*\\\\\s*&?\s*$',rhs)
  rowend=match[0] if match else ''
  core=rhs[:match.start()] if match else rhs
  result.append((core if 'F(r(t))' in core else lift_rhs(core,c))+rowend+trailer)
 return '='.join(result)
def historical_text(name,c):
 old=OLDS[OBSERVED[name]]
 text=old[':question/problem'];start=text.index('F(x');end=text.index('$',start)
 # Source prompt mask owns the complete vector-field value, not symbol substrings.
 field_start=text.index('=',start)+1
 prompt=text[:field_start]+lift_rhs(text[field_start:end],c)+text[end:]
 solution=old.get(':question/worked-solution')
 if solution is not None:
  number=0
  def replace(match):
   nonlocal number
   body=match[1];idx=number;number+=1
   # formula, coordinate block and derivative block don't scale.
   return '$$'+(lift_block(body,c) if idx in (2,4,5) else body)+'$$'
  solution=re.sub(r'\$\$(.*?)\$\$',replace,solution,flags=re.S)
 return prompt,solution

def make_record(level,name,p,profile,seed,prompt,solution,values,correct_index,raw=False):
 old=OLDS.get(OBSERVED.get(name));m=mathematics(name,SOURCE_PARAMETERS[name] if raw else p)
 if raw:
  task={'field':[s.srepr(s.sympify(p['lift'])*v) for v in m['F']], 'curve':[s.srepr(v) for v in m['r']], 'bounds':[s.srepr(m[q]) for q in ('a','b')], 'requested':'direct_scalar_integral'}
 else:
  task_curve=tuple(v-v.subs(t,0) for v in m['r']) if name=='constant_affine' else m['r']
  task={'field':[s.srepr(v) for v in m['F']], 'curve':[s.srepr(v) for v in task_curve], 'bounds':[s.srepr(m[q]) for q in ('a','b')], 'requested':'direct_scalar_integral'}
 fingerprint=digest(task)
 present={'version':VERSION,'difficulty':None if raw and ':question/difficulty' not in old else level,'prompt':prompt,'solution':solution,'bank':sorted(values),'correct_value':values[correct_index] if correct_index is not None else None}
 cid=digest(present);qid=uid('question/'+cid);fid=uid('field/'+cid+'/selection')
 answers=[{':answer/id':uid('answer/'+fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if correct_index is not None:f[':answer-field/correct']=[':answer/id',answers[correct_index][':answer/id']]
 random.Random(seed).shuffle(answers)
 q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[f]}
 if not raw or ':question/difficulty' in old:q[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:q[':question/worked-solution']=solution
 meta={'version':VERSION,'template':name,'bank_profile':profile,'seed':seed,'parameters':p,'mathematical_fingerprint':fingerprint,'content_identity':cid,'evidence_only':raw,'eligible_for_learning':not raw,'recipes':list(BANKS[name]) if not raw else ['historical_scalar_field_lift; intent unresolved']*5,'provenance':{k:CAPTURE[k] for k in ('database','basis','lineage')},'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'plot_rating':'none'}
 if old:meta['source_id']=old[':question/math-academy-id']
 return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':meta}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Observed layout is radio')
 rng=random.Random(seed)
 if profile and profile.startswith('observed:'):
  name=profile.split(':',1)[1]
  if template not in (None,name):raise ValueError('Profile/template mismatch')
  if name not in OBSERVED or level!='hard':raise ValueError('Historical evidence is assigned hard except omission retained')
  p=dict(lift=1) if parameters is None else dict(parameters)
  if set(p)!={'lift'} or s.sympify(p['lift']) not in (-3,-2,-1,1,2,3):raise ValueError('Historical linear-lift domain')
  c=s.sympify(p['lift']);old=OLDS[OBSERVED[name]];prompt,solution=historical_text(name,c)
  original=old[':question/answer-fields'][0];values=[lift_rhs(a[':answer/value'],c) for a in original[':answer-field/choices']]
  correct=original.get(':answer-field/correct');ci=next((i for i,a in enumerate(original[':answer-field/choices']) if correct and a[':answer/id']==correct[':answer/id']),None)
  return make_record(level,name,p,profile,seed,prompt,solution,values,ci,True)
 names=[n for n,v in TEMPLATES.items() if v==level]
 name=template or rng.choice(names)
 if name not in names:raise ValueError('Template is outside difficulty')
 # All defaults are supported source-shaped families, with one complete bank each.
 profile=profile or 'method:'+name
 if profile!='method:'+name:raise ValueError('Unknown complete bank')
 for attempt in range(400):
  p=dict(parameters) if parameters is not None else sample(name,rng)
  bounds(name,p,level);m=mathematics(name,p)
  try:values=operation_bank(name,p,m)
  except ValueError:
   if parameters is not None:raise
   continue
  prompt,solution=normal_text(name,p,m)
  return make_record(level,name,p,profile,seed,prompt,solution,[tex(v) for v in values],0)
 raise ValueError('No eligible whole instance after bounded sampling')

# EASY: authored constant vector field, affine spatial path; one constant primitive.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: canonical-example diagonal field, t/t²/t³; three power primitives.
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
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=2);parser.add_argument('--format',choices=['json','markdown'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
 records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
