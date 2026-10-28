#!/usr/bin/env python3
"""Supplied-gradient, two-component vector chain rule evaluated at a parameter point.

Observed profiles retain all source stages through complete expression masks.
Their scalar distractors are underdetermined evidence, restricted to coherent
function scaling/time dilation. Normal profiles are authored complete operation
banks, with independently varying actual gradient, curve and evaluation point.
No partial banks, DB writes, grading shortcuts, or learner error diagnoses.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
from functools import lru_cache
import sympy as s
ROOT=Path(__file__).with_suffix('')
VERSION='17592186124593-v1'
SOURCE=json.loads((ROOT/'source.json').read_text())
KP=SOURCE['record']; QUESTIONS=KP[':knowledge-point/questions']
t,x,y=s.symbols('t x y',real=True)
I,J=s.symbols('i j',real=True)
NAMESPACE=uuid.UUID('cc017b0d-6418-570a-9a5d-57572e4fe70a')
D=r'\frac{\text{d}}{\text{d}t}[f(r(t))]'
FORMAL=D+r'=∇f(r(t))\cdot {r}^{′}(t).'
TEMPLATES={
 'log_rational':'easy','sin_y':'easy','sqrt_sine':'easy','exp_cancel':'easy',
 'atan_log':'easy','exp_quadratic':'easy','log_sine':'moderate','sqrt_product':'moderate',
 'coupled_trig':'hard','product_exp':'hard'}
SOURCE_NAMES=list(TEMPLATES)[:8]
BY_TEMPLATE=dict(zip(['log_rational','sin_y','sqrt_sine','exp_cancel','atan_log','log_sine','exp_quadratic','sqrt_product'],QUESTIONS))
PROFILES={'observed_'+q[':question/math-academy-id']:n for n,q in BY_TEMPLATE.items()}
PROFILES['raw_observed_q-94878']='sqrt_product'
SOURCE_POINT={'log_rational':'1','sin_y':'pi/2','sqrt_sine':'pi','exp_cancel':'-1',
 'atan_log':'1','exp_quadratic':'1','log_sine':'0','sqrt_product':'pi/8'}

def value(z):
 return s.sympify(z,locals={'pi':s.pi,'t':t,'x':x,'y':y})
def simp(z):
 q=s.factor(s.trigsimp(s.simplify(z)))
 # The curriculum uses exponentials, not hyperbolic functions.
 return s.expand(q.rewrite(s.exp)) if q.has(s.sinh,s.cosh) else q
def tex(z):
 return s.latex(z).replace(r'\log',r'\ln')
def wrap(z): return r'\left('+z+r'\right)'
def vector(z):
 return wrap(tex(z[0]))+r'\,i+'+wrap(tex(z[1]))+r'\,j'
def block(z): return '$$\n'+z+'\n$$'
def aligned(lhs,rows):
 return block(r'\begin{aligned}'+lhs+' & ='+r' \\  & ='.join(rows)+r'\end{aligned}')
def scaled(expr,c):
 return expr if c==1 else tex(c)+r'\cdot '+wrap(expr)
def tid(z):
 return str(uuid.uuid5(NAMESPACE,z))
def dump(z): return json.dumps(z,sort_keys=True,separators=(',',':'),ensure_ascii=False)

def baseline(name):
 """Actual mathematical components, not an answer table."""
 if name=='log_rational':return (2*x/(x*x+3*y),3/(x*x+3*y)),(t,t*t)
 if name=='sin_y':return (s.sin(y),x*s.cos(y)),(t/2,t)
 if name=='sqrt_sine':return (2*x*y*s.cos(x*x),s.sin(x*x)),(s.sqrt(t),t/2)
 if name=='exp_cancel':return (2*x*s.exp(x*x+y),s.exp(x*x+y)),(s.sin(t),t+s.cos(t)**2)
 if name=='atan_log':return (1/x,1/y),(2*t*t+2,s.atan(t))
 if name=='exp_quadratic':return (2*x,2*y),(s.exp(-t),s.exp(t))
 if name=='log_sine':return (y*(s.log(x)+1),x*s.log(x)),(s.exp(2*t),s.sin(2*t))
 if name=='sqrt_product':return (-y*s.sin(x*y),-x*s.sin(x*y)),(2*s.sqrt(t),-2*s.sqrt(t))
 raise ValueError(name)

def dilate_expr(z,k):
 """Replace the mathematical t atom, protecting commands/function labels/operators.

 Masks are complete component RHSs, never a replacement across source prose.
 """
 if k==1:return z
 protected=[]
 def protect(m):
  protected.append(m.group());return '§'+str(len(protected)-1)+'§'
 z=re.sub(r'\\frac\{\\text\{d\}\}\{\\text\{d\}t\}|r\(t\)|r\}\^\{′\}\(t\)|\\[A-Za-z]+',protect,z)
 z=re.sub(r'(?<![A-Za-z])t(?![A-Za-z])',lambda m:wrap(str(k)+'t'),z)
 return re.sub(r'§(\d+)§',lambda m:protected[int(m[1])],z)

def source_masks(name,c,k,raw=False):
 """Parameterized assembly of source complete mathematical component masks.

 c scales f; k dilates the path time. Gradient, composition and scalar derivative
 stages scale coherently. Velocity stages scale by k. All intermediate arithmetic
 and common prose survive, including source-specific redundant rows.
 """
 q=BY_TEMPLATE[name]
 prompt=q[':question/problem'];solution=q[':question/worked-solution']
 # Smallest supported mathematical repair, not a TeX-escape normalization.
 if name=='sqrt_product' and not raw:
  solution=solution.replace(r'(-\frac{1}{\sqrt{t}})i)',r'(-\frac{1}{\sqrt{t}})j)')
 grad,curve=baseline(name)
 point=value(SOURCE_POINT[name])/k
 # Complete gradient and curve RHS slots in the prompt.
 prompt=re.sub(r'(∇f\(x,y\)=)(.*?)(\$)',lambda m:m[1]+scaled(m[2],c)+m[3],prompt)
 prompt=re.sub(r'(r\(t\)=)(.*?)(\$)',lambda m:m[1]+dilate_expr(m[2],k)+m[3],prompt)
 oldpoint=tex(value(SOURCE_POINT[name]))
 # Point slot is the exact complete inline equation in the source header.
 prompt=re.sub(r'(at \$t=).*?(\$)',lambda m:m[1]+(q[':question/problem'].split('at $t=',1)[1].split('$',1)[0] if k==1 else tex(point))+m[2],prompt,count=1)
 parts=re.split(r'(\$\$\n.*?\n\$\$)',solution,flags=re.S)
 math_index=0
 for n,part in enumerate(parts):
  if not part.startswith('$$'):continue
  body=part[3:-3];idx=math_index;math_index+=1
  if idx==0:continue  # abstract formal rule
  if idx==1: # supplied gradient
   left,right=body.split('=',1);body=left+'='+scaled(right,c)
  elif idx in (2,3,4,5):
   # Aligned body is a list of complete RHS component masks.
   a,b=body.split(' & =',1); end=r'\end{aligned}'
   rows=b.removesuffix(end).split(r' \\  & =')
   if idx==2:rows=[scaled(dilate_expr(z,k),c) for z in rows]
   elif idx==3:
    rows=[dilate_expr(rows[0],k)]+[scaled(dilate_expr(z,k),k) for z in rows[1:]]
   elif idx==4:
    dot_left,dot_right=rows[1].split(r'\cdot',1)
    rows=[rows[0],scaled(dilate_expr(dot_left,k),c)+r'\cdot'+scaled(dilate_expr(dot_right,k),k)]+[scaled(dilate_expr(z,k),c*k) for z in rows[2:]]
   else:
    # Numerical evaluation masks are already at the original phase k*t=q.
    # Every equals-separated scalar is scaled, preserving the evaluation stages.
    rows=['='.join(scaled(z,c*k) for z in row.split('=')) for row in rows]
    if k!=1:a=re.sub(r'f\(r\(.*?\)\)',lambda m:'f(r('+tex(point)+'))',a)
   body=a+' & ='+r' \\  & ='.join(rows)+end
  parts[n]='$$\n'+body+'\n$$'
 solution=''.join(parts)
 # Composition/velocity prose input equations use the same complete math masks.
 start=solution.index('First, we substitute'); stop=solution.index('Now, we calculate')
 a=solution[start:stop]
 a=re.sub(r'\$(x|y)=(.*?)\$',lambda m:'$'+m[1]+'='+dilate_expr(m[2],k)+'$',a)
 solution=solution[:start]+a+solution[stop:]
 if k!=1:
  solution=re.sub(r'(Finally, evaluating the above at \$t=).*?(,\$)',lambda m:m[1]+tex(point)+m[2],solution)
 G=tuple(c*z for z in grad);R=tuple(z.subs(t,k*t) for z in curve)
 return prompt,solution,G,R,point

# ===========================================================================
# EASY — six observed supplied-gradient families. Authored coefficient/point
# variation preserves two-coordinate substitution and one two-term dot product.
# ===========================================================================
def model(name,p):
 a,b,d,e,k=[value(p.get(z,1)) for z in ('a','b','d','e','k')]
 if name=='log_rational':G=(2*a*x/(a*x*x+b*y),b/(a*x*x+b*y));R=(d*t,e*t*t)
 elif name=='sin_y':G=(a*s.sin(y),a*x*s.cos(y));R=(b*t,t/d)
 elif name=='sqrt_sine':G=(2*a*x*y*s.cos(x*x),a*s.sin(x*x));R=(s.sqrt(b*t),d*t)
 elif name=='exp_cancel':G=(2*a*x*s.exp(x*x+y),a*s.exp(x*x+y));R=(s.sin(b*t),d*t+s.cos(b*t)**2)
 elif name=='atan_log':G=(a/x,b/y);R=(d*t*t+e,s.atan(k*t))
 elif name=='exp_quadratic':G=(2*a*x,2*b*y);R=(s.exp(-d*t),s.exp(e*t))
 # MODERATE — logs simplify with exponentials or two signed square roots enter
 # a coupled sine gradient. Nonunit derivative factors remain mandatory.
 elif name=='log_sine':G=(a*y*(s.log(x)+1),a*x*s.log(x));R=(s.exp(b*t),s.sin(d*t))
 elif name=='sqrt_product':G=(-a*y*s.sin(x*y),-a*x*s.sin(x*y));R=(b*s.sqrt(t),-d*s.sqrt(t))
 # HARD (authored) — same supplied 2D gradient, extra coupled terms/products.
 # No gradient computation, contextual rate, extra dimension, or new theorem.
 elif name=='coupled_trig':G=(a*y+b*x,a*x+d*y);R=(s.sin(k*t),s.cos(k*t))
 elif name=='product_exp':G=(a*y*s.exp(x*y)+b*x,a*x*s.exp(x*y)+b*y);R=(d*t*t,e*t)
 else:raise ValueError(name)
 return G,R,value(p['point'])

def bounds(name,p):
 keys={'a','b','d','e','k','point'}
 if set(p)-keys:raise ValueError('Unknown parameters: '+str(set(p)-keys))
 if 'point' not in p:raise ValueError('point is required')
 limit=3 if TEMPLATES[name]=='hard' else 4
 for z in keys-{'point'}:
  v=value(p.get(z,1))
  if not v.is_Integer or not 1<=v<=limit:raise ValueError('Coefficient '+z+' outside positive integer workload bounds')
 if TEMPLATES[name]=='moderate' and (value(p.get('b',1))<2 or value(p.get('d',1))<2):raise ValueError('Moderate requires both nonunit curve coefficients')
 if TEMPLATES[name]=='hard' and any(value(p.get(z,1))<2 for z in ('a','b','d')):raise ValueError('Hard requires nonunit coupled coefficients')
 G,R,q=model(name,p)
 if name in ('sqrt_sine','sqrt_product') and q<=0:raise ValueError('Square-root domain t>0')
 if name=='log_rational' and q not in (-2,-1,1,2):raise ValueError('Easy rational evaluation requires a nonzero integer point with magnitude at most 2')
 if name=='atan_log' and q==0:raise ValueError('arctan denominator vanishes')
 if name in ('exp_cancel','exp_quadratic','product_exp') and (q not in (-2,-1,1,2) or (name=='product_exp' and q not in (-1,1))):raise ValueError('Exact exponential workload point invalid')
 if name=='sin_y' and simp(q/value(p.get('d',1))/(s.pi/2)) not in (-3,-2,-1,1,2,3):raise ValueError('Familiar sine evaluation angle required')
 if name=='sqrt_sine' and simp(value(p.get('b',1))*q/s.pi) not in (1,2,3):raise ValueError('Familiar square-root sine argument required')
 if name=='atan_log' and abs(value(p.get('k',1))*q)!=1:raise ValueError('Familiar arctan argument required')
 if name=='sqrt_product' and simp(value(p.get('b',1))*value(p.get('d',1))*q/(s.pi/2)) not in (1,2,3):raise ValueError('Familiar sine product argument required')
 if name=='coupled_trig' and simp(value(p.get('k',1))*q/(s.pi/4)) not in (1,3,5,7):raise ValueError('Hard both coordinates nonzero familiar angle required')
 if name=='log_sine' and q not in (0,s.pi/value(p.get('d',1)),s.pi/(2*value(p.get('d',1)))):raise ValueError('Moderate familiar sine point required')
 return G,R,q

def sample(name,rng):
 p={z:rng.randint(1,3 if TEMPLATES[name]=='hard' else 4) for z in ('a','b','d','e','k')}
 if TEMPLATES[name]=='moderate':p['b']=rng.randint(2,4);p['d']=rng.randint(2,4)
 if TEMPLATES[name]=='hard':
  for z in ('a','b','d'):p[z]=rng.randint(2,3)
 if name=='sin_y':q=p['d']*rng.choice([-3,-2,-1,1,2,3])*s.pi/2
 elif name=='sqrt_sine':q=rng.randint(1,3)*s.pi/p['b']
 elif name=='atan_log':q=s.Rational(rng.choice([-1,1]),p['k'])
 elif name=='sqrt_product':q=s.Rational(rng.randint(1,3),2*p['b']*p['d'])*s.pi
 elif name=='coupled_trig':q=s.Rational(rng.choice([1,3,5,7]),4*p['k'])*s.pi
 elif name=='log_sine':q=rng.choice([s.S.Zero,s.pi/p['d'],s.pi/(2*p['d'])])
 elif name=='product_exp':q=rng.choice([-1,1])
 else:q=rng.choice([-2,-1,1,2])
 p['point']=str(q);return p

@lru_cache(maxsize=2048)
def construct(G,R,q):
 sub={x:R[0],y:R[1]}
 C=tuple(simp(z.subs(sub,simultaneous=True)) for z in G)
 V=tuple(s.diff(z,t) for z in R)
 terms=tuple(s.expand(C[i]*V[i]) for i in range(2))
 derivative=simp(sum(terms));answer=simp(derivative.subs(t,q))
 if answer.has(s.nan,s.zoo,s.oo,-s.oo) or answer.is_real is False:raise ValueError('Undefined or nonreal answer')
 return C,V,terms,derivative,answer

def authored_render(G,R,q):
 C,V,terms,h,answer=construct(G,R,q)
 prompt='Evaluate $'+D+'$ at $t='+tex(q)+'$ given that $∇f(x,y)='+vector(G)+'$ and $r(t)='+vector(R)+'.$'
 raw=tuple(z.subs({x:R[0],y:R[1]},simultaneous=True) for z in G)
 # Preserve the formal operators and ordered differentiation components before
 # evaluated velocity; distinct product masks before expansion and collection.
 solution='The chain rule in vector form states that\n\n'+block(FORMAL)
 solution+='\n\nIn addition, we\'ve been given that\n\n'+block('∇f(x,y)='+vector(G)+'.')
 solution+='\n\nFirst, we substitute $x='+tex(R[0])+'$ and $y='+tex(R[1])+'$ into $∇f(x,y)$ to find $∇f(r(t)):$\n\n'
 # Unsubstituted gradient with explicit coordinate substitution stages keeps
 # factors unevaluated even if SymPy simplifies direct substitution.
 formal_sub=vector(G)+r'\Big|_{x='+tex(R[0])+r',\,y='+tex(R[1])+'}'
 solution+=aligned('∇f(r(t))',[formal_sub,vector(C)])
 solution+='\n\nNow, we calculate the derivative of $r(t),$ which is\n\n'
 velocity=r'\frac{\text{d}}{\text{d}t}'+wrap(tex(R[0]))+r'\,i+\frac{\text{d}}{\text{d}t}'+wrap(tex(R[1]))+r'\,j'
 solution+=aligned(r'{r}^{′}(t)',[velocity,vector(V)+'.'])
 products='+'.join(wrap(tex(C[i]))+r'\cdot '+wrap(tex(V[i])) for i in range(2))
 distributed='+'.join(wrap(tex(z)) for z in terms)
 solution+='\n\nApplying the chain rule, we get\n\n'+aligned(D,[r'∇f(r(t))\cdot {r}^{′}(t)',wrap(vector(C))+r'\cdot '+wrap(vector(V)),products,distributed,tex(h)+'.'])
 evaluation=tex(h)+r'\Big|_{t='+tex(q)+'}'
 # Evaluate each term separately to expose arithmetic before collection.
 evaluated='+'.join(wrap(tex(simp(z.subs(t,q)))) for z in terms)
 solution+='\n\nFinally, evaluating the above at $t='+tex(q)+',$ we obtain\n\n'+aligned(D+r'\Big|_{t='+tex(q)+'}',[evaluation,evaluated,tex(answer)+'.'])
 return prompt,solution

# Complete eligible operation banks. They are different full profiles because
# zeros can make omission/sign banks collide. No member is replaced in place.
OPERATIONS={
 'component_sign':('correct','omit_x','omit_y','reverse_x','reverse_y'),
 'velocity_omission':('correct','omit_dx','omit_dy','omit_both_velocities','sum_velocity'),
 'dot_arithmetic':('correct','subtract_y','negative_dot','product_terms','sum_gradient'),
 'chain_input':('correct','position_dot','second_derivative_dot','swapped_velocity','gradient_norm_squared')}
def operation_bank(G,R,q,profile):
 C,V,terms,h,a=construct(G,R,q)
 A,B=[simp(z.subs(t,q)) for z in terms]
 gx,gy=[simp(z.subs(t,q)) for z in C];vx,vy=[simp(z.subs(t,q)) for z in V]
 vals={'correct':a,'omit_x':B,'omit_y':A,'reverse_x':-A+B,'reverse_y':A-B,
 'omit_dx':gx+B,'omit_dy':A+gy,'omit_both_velocities':gx+gy,'sum_velocity':vx+vy,
 'subtract_y':A-B,'negative_dot':-a,'product_terms':A*B,'sum_gradient':gx+gy,
 'position_dot':gx*R[0].subs(t,q)+gy*R[1].subs(t,q),
 'second_derivative_dot':gx*s.diff(R[0],t,2).subs(t,q)+gy*s.diff(R[1],t,2).subs(t,q),
 'swapped_velocity':gx*vy+gy*vx,'gradient_norm_squared':gx**2+gy**2}
 return [simp(vals[z]) for z in OPERATIONS[profile]]

def bank_valid(vals):
 return all(not z.has(s.zoo,s.nan,s.oo,-s.oo) and z.is_real is not False for z in vals) and all(simp(a-b)!=0 for n,a in enumerate(vals) for b in vals[n+1:])

# Source scalar patterns are parsed symbolic constants with common c*k scaling.
# These are honest evidence replay profiles, not inferred mistake algorithms.
SOURCE_VALUES={
 'log_rational':['1/2','6','1','2','4'],
 'sin_y':['2-pi','0','pi/4','1/2','-1'],
 'sqrt_sine':['-2*pi','1/2','pi','-pi/2','-1'],
 'exp_cancel':['1','2/E','2*E','E','1/2'],
 'atan_log':['1','(pi+2)/pi','(pi+1)/pi','pi/(pi+2)','pi/(pi+1)'],
 'log_sine':['3','4','2','1','0'],
 'exp_quadratic':['2-3*exp(-1)','3*E+exp(-1)','2*exp(2)-2*exp(-2)','4*exp(2)','-4*exp(-1)'],
 'sqrt_product':['-4','0','2','-sqrt(pi)/2','sqrt(pi)/4']}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio layout supported')
 rng=random.Random(seed)
 if profile in PROFILES:
  name=PROFILES[profile]
  if template is not None and template!=name:raise ValueError('Profile/template mismatch')
 elif profile not in (None,*OPERATIONS):raise ValueError('Unknown profile')
 else:name=template or rng.choice([z for z in TEMPLATES if TEMPLATES[z]==level])
 if name not in TEMPLATES or TEMPLATES[name]!=level:raise ValueError('Template/difficulty mismatch')
 if profile in PROFILES:
  p=parameters if parameters is not None else {'c':rng.choice([1,2,3]),'time_scale':rng.choice([1,2,3])}
  if set(p)!={'c','time_scale'}:raise ValueError('Observed replay parameters require c,time_scale')
  c,k=value(p['c']),value(p['time_scale'])
  if not c.is_Integer or not k.is_Integer or not 1<=c<=4 or not 1<=k<=3:raise ValueError('Observed replay bounds exceeded')
  prompt,solution,G,R,q=source_masks(name,c,k,raw=profile.startswith('raw_'))
  vals=[simp(c*k*value(z)) for z in SOURCE_VALUES[name]]
  correct=construct(G,R,q)[4]
  assert sum(simp(z-correct)==0 for z in vals)==1
  # Original scalar notation retained through expression masks at unit scale.
  displayed=[scaled(a[':answer/value'],c*k) for a in BY_TEMPLATE[name][':question/answer-fields'][0][':answer-field/choices']]
  origin='observed_bank_replay_underdetermined'
 else:
  # Choose a COMPLETE profile before building the bank and reject the entire
  # sampled mathematical instance on any collision. Explicit calls never repair.
  profiles=[profile] if profile else list(OPERATIONS)
  if parameters is not None:
   p=dict(parameters);G,R,q=bounds(name,p)
   eligible=[z for z in profiles if bank_valid(operation_bank(G,R,q,z))]
   if not eligible:raise ValueError('Whole instance has no complete eligible operation bank')
   profile=rng.choice(eligible)
  else:
   for _ in range(2000):
    p=sample(name,rng);G,R,q=bounds(name,p);profile=rng.choice(profiles)
    if bank_valid(operation_bank(G,R,q,profile)):break
   else:raise ValueError('No valid full bank after bounded whole-instance sampling')
  vals=operation_bank(G,R,q,profile);correct=vals[0]
  displayed=[tex(z) for z in vals]
  prompt,solution=authored_render(G,R,q)
  origin='authored_missing_level' if level=='hard' else 'authored_parameter_and_bank_extension'
 if not bank_valid(vals):raise ValueError('Whole bank ambiguous or invalid')
 payload={'version':VERSION,'level':level,'problem':prompt,'solution':solution,'bank':sorted(displayed),'correct':tex(correct)}
 identity=tid(dump(payload));fid=tid(identity+'/field/selection')
 answers=[{':answer/id':tid(fid+'/'+z),':answer/type':':answer.type/math',':answer/value':z} for z in displayed]
 correctid=next(a[':answer/id'] for a,z in zip(answers,vals) if simp(z-correct)==0)
 rng.shuffle(answers)
 # Canonical task excludes bank/profile and unused parameter aliases.
 fingerprint=hashlib.sha256(dump({'G':[s.srepr(z) for z in G],'R':[s.srepr(z) for z in R],'point':s.srepr(q)}).encode()).hexdigest()
 return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},
 'question':{':question/id':identity,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correctid]}]},
 'generation':{'version':VERSION,'seed':seed,'template':name,'bank_profile':profile,'parameters':{z:str(v) for z,v in p.items()},'origin':origin,'evidence_only':profile in PROFILES,'eligible_for_learning':profile not in PROFILES,'raw_math_error':profile=='raw_observed_q-94878','mathematical_fingerprint':fingerprint,'basis':SOURCE['basis'],'database':SOURCE['database'],'lineage':SOURCE['lineage'],'source_ids':[BY_TEMPLATE[name][':question/math-academy-id']] if name in BY_TEMPLATE else [],'domain':'Real; all displayed denominators nonzero; square-root path t>0.','operations':list(OPERATIONS[profile]) if profile in OPERATIONS else 'Underdetermined source scalar patterns under coherent c*k scaling'}}

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Six easy supplied-gradient families; workload bounds in bounds()."""
 return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Two observed moderate families with nonunit inner derivatives."""
 return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Authored coupled gradient/cubic exponential composition, same 2D point task."""
 return generate('hard',seed,template,field_type,parameters,profile)
def markdown(z):
 q=z['question'];g=z['generation'];f=q[':question/answer-fields'][0]
 return '### '+g['template']+' — '+q[':question/difficulty'].split('/')[-1]+' ('+g['origin']+')\n\n'+q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

from source_notation import install as _install_source_notation, apply as _apply_source_notation
_install_source_notation(globals())

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 if args.count<1:ap.error('count must be positive')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+n,args.template,profile=args.profile) for l in levels for n in range(args.count)]
 print(json.dumps(_apply_source_notation(records),ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
