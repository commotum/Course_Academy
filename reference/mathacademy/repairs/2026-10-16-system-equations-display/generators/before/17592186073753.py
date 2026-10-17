#!/usr/bin/env python3
"""Integer-coefficient substitution systems, math basis 1356; stops at step 7.

All difficulty labels here are AUTHOR DESIGN: captured practice is unrated.
Observed banks are explicit empirical profiles, never default distractor recipes.
The malformed q12457 raw profile is public evidence replay, not an assessment.
Normal whole five-choice banks derive errors from the substitution operation and
reject the entire instance on collisions. No database/renderer dependencies.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as s
KP_ID=17592186073753
KP_UUID='b4352698-7af7-5d74-9c3a-0f951c3e6078'
TITLE='Solving a Challenging System of Linear Equations Using Substitution'
VERSION='challenging-substitution-1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
PROVENANCE={k:SOURCE[k] for k in ('database','basis','lineage')}
TEMPLATES=('pair_first','pair_second','difference','canonical_second')
PROFILE_TEMPLATE={'source_q12444':'pair_first','source_q12457_raw':'pair_second','source_q12457_repaired':'pair_second','source_q18483':'difference'}
SOURCE_PARAMETERS={
 'q-12444':{'A':-3,'B':1,'C':-9,'D':5,'E':4,'F':32,'x':'p','y':'q'},
 'q-12457':{'A':-7,'B':2,'C':18,'D':-6,'E':6,'F':0,'x':'a','y':'b'},
 'q-18483':{'A':0,'B':5,'C':-55,'D':2,'E':3,'F':-3,'x':'p','y':'q'},
 'e-13010':{'A':2,'B':9,'C':6,'D':2,'E':6,'F':8,'x':'u','y':'v'}}

def tex(n):
 n=s.sympify(n)
 if n.is_Rational and n.q!=1:
  return ('-' if n<0 else '')+r'\dfrac{'+str(abs(n.p))+'}{'+str(n.q)+'}'
 return str(n)

def term(c,v):
 c=s.sympify(c)
 if not c:return '0'
 return ('-' if c<0 else '')+('' if abs(c)==1 else tex(abs(c)))+v

def add(*parts):
 # Components stay distinct until the advertised collection operation.
 out=''
 for c,v in parts:
  c=s.sympify(c)
  if c==0:continue
  t=term(c,v) if v else tex(c)
  out+=(' + ' if c>0 and out else ' - ' if c<0 and out else '')+(t.lstrip('-') if out else t)
 return out or '0'

def par(t):return r'\left('+t+r'\right)'
def aligned(rows):return '$$\n'+r'\begin{aligned} '+r' \\ '.join(l+' &= '+r for l,r in rows)+r' \end{aligned}'+'\n$$'
def equations(p,zero=False):
 A,B,C,D,E,F=(s.Integer(p[k]) for k in 'ABCDEF');x,y=p['x'],p['y']
 return [add((A,x),(B,y),(-C,''))+' = 0' if zero else add((A,x),(B,y))+' = '+tex(C),add((D,x),(E,y),(-F,''))+' = 0' if zero else add((D,x),(E,y))+' = '+tex(F)]

def values(p):
 A,B,C,D,E,F=(s.Integer(p[k]) for k in 'ABCDEF')
 det=A*E-B*D
 if not det:raise ValueError('Unique linear-system solution required')
 return s.cancel((C*E-B*F)/det),s.cancel((A*F-C*D)/det)

def isolate(p,t):
 A,B,C,D,E,F=(s.Integer(p[k]) for k in 'ABCDEF');x,y=p['x'],p['y']
 if t=='pair_first':return y,x,B,-A,C,A,B,C,D,E,F,1
 if t=='pair_second':return y,x,E,-D,F,D,E,F,A,B,C,2
 return x,y,D,-E,F,E,D,F,B,A,C,2
 # isolated variable, remaining variable, divisor, numerator slope/constant,
 # printed isolate row (remaining coeff, isolated coeff, constant),
 # other row (remaining coeff, isolated coeff, constant), equation number.

def solution(p,t):
 """Shared source-canonical prose; all intermediate rows retain operations."""
 X,Y=values(p);x,y=p['x'],p['y'];A,B,C,D,E,F=(s.Integer(p[k]) for k in 'ABCDEF')
 if t=='difference':
  rows1=[(add((B,y),(-C,'')),'0'),(term(B,y),tex(C)),(y,tex(Y))]
  rows2=[(add((D,x),(E,y),(-F,'')),'0'),(add((D,x),(E,par(tex(Y))),(-F,'')),'0'),(add((D,x),(E*Y,''),(-F,'')),'0'),(term(D,x),tex(F-E*Y)),(x,tex(X))]
  return ('We will isolate a variable in one of the equations and then substitute it into the other equation. Using equation $\\color{red}(1)$, we can solve for $'+y+'$ as follows:\n\n'+aligned(rows1)+'\n\nThen, we substitute $'+y+'='+tex(Y)+'$ into equation $\\color{blue}(2)$ and solve for $'+x+'$:\n\n'+aligned(rows2)+'\n\nTherefore, $'+x+' - '+y+' = '+tex(X)+' - '+par(tex(Y))+' = '+tex(X-Y)+'$.')
 v,w,d,n,k,ia,ib,ic,oa,ob,oc,num=isolate(p,t);h=k/d;m=n/d;V=X if v==x else Y;W=Y if w==y else X
 eqs=equations(p,True)
 ir=[(add((ib,v),(ia,w),(-ic,'')),'0'),(add((ib,v),(ia,w)),tex(ic)),(term(d,v),add((k,''),(n,w))),(v,r'\dfrac{'+add((k,''),(n,w))+'}{'+tex(d)+'}'),(v,add((h,''),(m,w)))]
 if t=='pair_first':ir=ir[:3]
 sr=[(add((ob,v),(oa,w),(-oc,'')),'0'),(add((ob,'('+add((h,''),(m,w))+')'),(oa,w),(-oc,'')),'0'),(add((ob*h,''),(ob*m,w),(oa,w),(-oc,'')),'0'),(add((ob*h-oc,''),(ob*m+oa,w)),'0'),(term(ob*m+oa,w),tex(oc-ob*h)),(w,tex(W))]
 br=[(add((ob,v),(oa,w),(-oc,'')),'0'),(add((ob,v),(oa,par(tex(W))),(-oc,'')),'0'),(add((ob,v),(oa*W,''),(-oc,'')),'0'),(add((ob,v),(oa*W-oc,'')),'0'),(term(ob,v),tex(oc-oa*W)),(v,tex(V))]
 # Canonical keeps distinct evaluated and collected rows.
 pre="Sometimes, it's handy to assign a number to each equation in a system, so that we can refer to them more easily:\n\n$$\n\\{"+eqs[0]+'(1); '+eqs[1]+'(2)\n$$\n\n'
 return (pre+'We will isolate a variable in one of the equations and then substitute it into the other equation. Using equation $\\color{blue}('+str(num)+')$, we can solve for $'+v+'$ as follows:\n\n'+aligned(ir)+'\n\nThen, we substitute $'+v+'='+add((h,''),(m,w)).replace(' ','')+'$ into equation $\\color{red}('+str(3-num)+')$ and solve for $'+w+'$:\n\n'+aligned(sr)+'\n\nIf we now substitute\n\n$$\n'+w+'='+tex(W)+'\n$$\n\ninto equation $\\color{red}('+str(3-num)+')$, then we can find the value of $'+v+'$:\n\n'+aligned(br)+'\n\nTherefore, the solution to the system of equations is $'+v+'='+tex(V)+'$ and\n\n$$\n'+w+'='+tex(W)+'\n$$\n\n, which can be written as\n\n$$\n\\left('+tex(X)+','+tex(Y)+'\\right)\n$$')

def bank(p,t,profile):
 X,Y=values(p);A,B,C,D,E,F=(s.Integer(p[k]) for k in 'ABCDEF')
 if profile=='source_q12444':return [(X,Y-s.Integer(1)),(X,-Y/3),(X,Y),(Y,X),(-X,Y)],['empirical_y_minus_one','empirical_negative_third_y','correct','swap','reverse_x']
 if profile.startswith('source_q12457'):
  z=C/(abs(A)+B)
  out=[(-2*z,2*z),(3*z/2,-3*z/2),(2*z,-2*z),(z,-z),(-z,z)]
  if profile.endswith('repaired'):out[0]=(X,Y)
  return out,['empirical_negative_double','empirical_three_halves','empirical_double','empirical_unit','empirical_negative_unit']
 if profile=='source_q18483':return [X+Y,X-Y,-X-Y,Y,X],['add','correct','negative_sum','y_only','x_only']
 if t=='difference':
  wrongY=-Y;wrongX=s.cancel((F-E*wrongY)/D)
  return [X-Y,X+Y,Y-X,X,wrongX-wrongY],['correct','add','reverse_subtraction','x_only','reverse_first_isolation_sign']
 v,w,d,n,k,ia,ib,ic,oa,ob,oc,num=isolate(p,t);h=k/d;m=n/d
 def pair(V,W):return (V,W) if v==p['x'] else (W,V)
 W=(oc-ob*h)/(ob*m+oa);V=h+m*W
 wr=(oc-ob*h)/(-ob*m+oa) if -ob*m+oa else s.nan
 wp=pair(h-m*wr,wr)
 wm=(oc-h)/(ob*m+oa);pm=pair(h+m*wm,wm)
 return [(X,Y),wp,pm,pair(h+m*(oc-ob*h),oc-ob*h),(Y,X)],['correct','reverse_isolation_slope','omit_multiplier_on_constant','omit_remaining_variable_division','swap_values']

def normalized(p):
 if set(p)!=set('ABCDEF')|{'x','y'}:raise ValueError('Parameters must be A..F and x,y')
 q={k:int(p[k]) for k in 'ABCDEF'}
 if any(s.sympify(p[k])!=q[k] for k in 'ABCDEF'):raise ValueError('Integer coefficients only')
 q.update(x=p['x'],y=p['y'])
 if q['x'] not in ('x','u','p','a') or q['y'] not in ('y','v','q','b') or q['x']==q['y']:raise ValueError('Unsupported variables')
 if any(abs(q[k])>150 for k in 'ABCDEF'):raise ValueError('Source/sampling arithmetic bounds exceeded')
 values(q)
 return q

def guard(p,level,t,profile):
 if t not in TEMPLATES:raise ValueError('Unknown template')
 if profile!='method':
  if PROFILE_TEMPLATE.get(profile)!=t:raise ValueError('Incompatible explicit evidence profile')
  if profile=='source_q12444' and not(p['B']==1 and p['A'] and p['D'] and p['E']):raise ValueError('Source profile requires unit y coefficient in first equation')
  if profile.startswith('source_q12457') and not(p['A']<0 and p['B']>0 and p['D']==-p['E'] and p['E']>1 and p['F']==0):raise ValueError('Source profile requires its observed homogeneous second-row structure')
  if profile=='source_q18483' and not(p['A']==0 and abs(p['B'])>1 and abs(p['D'])>1 and p['E']):raise ValueError('Source triangular structure required')
  return
 X,Y=values(p)
 if level=='easy':
  if max(abs(p[k]) for k in 'ABDE')>6 or max(abs(p[k]) for k in 'CF')>70 or not(X.is_Integer and Y.is_Integer):raise ValueError('Easy requires small integer coefficients and integer solutions')
 elif level=='moderate':
  if t=='difference' or min(abs(p[k]) for k in 'ABDE')<2 or max(abs(p[k]) for k in 'ABDE')>9 or max(abs(p[k]) for k in 'CF')>110 or not(X.is_Integer and Y.is_Integer):raise ValueError('Moderate requires all nonunit integer coefficients and integer solutions')
 else:
  if t=='difference' or min(abs(p[k]) for k in 'ABDE')<2 or max(abs(p[k]) for k in 'ABDE')>10 or max(abs(p[k]) for k in 'CF')>120 or (X.is_Integer and Y.is_Integer) or max(X.q,Y.q)>12:raise ValueError('Hard requires all nonunit integer coefficients and a bounded fractional solution')
 if t=='pair_first' and abs(p['B'])!=1:raise ValueError('pair_first isolates the unit y coefficient')
 if t=='difference':
  if p['A'] or abs(p['B'])<2 or abs(p['D'])<2:raise ValueError('Difference uses nonunit triangular equations')
 else:
  v,w,d,n,k,*_=isolate(p,t)
  if not d or not n or not k or abs(d)==1 and t!='pair_first':raise ValueError('Nontrivial affine isolation required')
  if not (s.Integer(n)/d).is_Integer or not(s.Integer(k)/d).is_Integer:raise ValueError('Isolated affine expression must simplify to integer coefficients')
  if not (X and Y):raise ValueError('Default tasks retain both nonzero values')

def sample(r,level,t):
 # No progression: each level fixes its arithmetic/response workload.
 x,y=r.choice([('x','y'),('u','v'),('p','q'),('a','b')])
 if t=='difference':
  X,Y=r.choice(range(2,8)),r.choice(range(-9,-1));B,D,E=r.choice(range(2,6)),r.choice(range(2,6)),r.choice(range(2,6))
  return dict(A=0,B=B,C=B*Y,D=D,E=E,F=D*X+E*Y,x=x,y=y)
 if t=='pair_first':
  X,Y=r.choice(range(-7,8)),r.choice(range(-7,8));A,D,E=[r.choice([-5,-4,-3,2,3,4,5]) for _ in range(3)]
  return dict(A=A,B=1,C=A*X+Y,D=D,E=E,F=D*X+E*Y,x=x,y=y)
 lim=6 if level=='easy' else 9 if level=='moderate' else 10
 d=r.choice(range(2,5));m=r.choice([-2,-1,1,2]);h=r.choice([-5,-4,-3,2,3,4,5]);A=r.choice([z for z in range(-lim,lim+1) if abs(z)>=2]);B=r.choice([z for z in range(-lim,lim+1) if abs(z)>=2])
 if t=='pair_second':
  # y=h+m*x from second equation.
  D,E,F=-d*m,d,d*h
  if level=='hard':C=r.choice(range(-40,41))
  else:
   X=r.choice(range(-6,7));Y=h+m*X;C=A*X+B*Y
 else:
  # x=h+m*y from second equation, exactly the canonical's operation.
  D,E,F=d,-d*m,d*h
  if level=='hard':C=r.choice(range(-40,41))
  else:
   Y=r.choice(range(-6,7));X=h+m*Y;C=A*X+B*Y
 return dict(A=A,B=B,C=C,D=D,E=E,F=F,x=x,y=y)

def sample_profile(r,profile):
 p=dict(SOURCE_PARAMETERS['q-12444' if profile=='source_q12444' else 'q-18483' if profile=='source_q18483' else 'q-12457'])
 if profile=='source_q12444':
  X,Y=r.randint(2,8),r.randint(2,8);p['C']=-3*X+Y;p['F']=5*X+4*Y
 elif profile=='source_q18483':
  X,Y=r.randint(8,20),-r.randint(3,12);p['C']=5*Y;p['F']=2*X+3*Y
 else:p['C']=9*r.randint(1,8)
 return p

def uid(salt):return str(uuid.uuid5(uuid.NAMESPACE_URL,salt))
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def canonical_task(p,t):
 # Canonical equation rows modulo nonzero scalar, variable names incidental.
 rows=[]
 for keys in ('ABC','DEF'):
  v=[s.Rational(p[k]) for k in keys];pivot=next(z for z in v if z);rows.append([str(z/pivot) for z in v])
 return digest({'rows':sorted(rows),'response':'difference' if t=='difference' else 'ordered_values'})

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio layout supported')
 profile=profile or 'method';r=random.Random(seed)
 t=template or PROFILE_TEMPLATE.get(profile) or r.choice(['pair_first','canonical_second','difference'] if level=='easy' else ['pair_second','canonical_second'])
 for attempt in range(2000):
  try:
   p=normalized(parameters if parameters is not None else (sample(r,level,t) if profile=='method' else sample_profile(r,profile)));guard(p,level,t,profile)
   vals,recipes=bank(p,t,profile);X,Y=values(p);correct=X-Y if t=='difference' else (X,Y)
   if any(any(not(s.sympify(c).is_Rational) for c in v) if isinstance(v,tuple) else not s.sympify(v).is_Rational for v in vals):raise ValueError('Invalid whole bank')
   signatures=[tuple(map(str,v)) if isinstance(v,tuple) else str(v) for v in vals]
   if len(set(signatures))!=5:raise ValueError('Whole bank collision')
   raw=profile=='source_q12457_raw'
   hits=[i for i,v in enumerate(vals) if v==correct]
   if not raw and len(hits)!=1:raise ValueError('Whole bank must have exactly one correct value')
   if raw and hits:raise ValueError('Raw anomaly profile must retain no valid answer')
   break
  except (ValueError,ZeroDivisionError):
   if parameters is not None:raise
 else:raise ValueError('No whole-bank instance in requested domain')
 eqs=equations(p,t in ('difference','canonical_second'))
 if t=='pair_first':prompt='Using the method of substitution, find the solution of\n$\\{'+ '; '.join(eqs)+'$.'
 elif t=='pair_second':prompt='Using the method of substitution, find the solution of\n\n$\\{'+ '; '.join(eqs)+'$'
 elif t=='difference':prompt='Given the system of equations below, what is the value of $'+p['x']+' - '+p['y']+'$?\n\n$\\{'+ '; '.join(eqs)+'$'
 else:prompt='Solve the following system of equations:\n\n$\\{'+ '; '.join(eqs)+'$'
 sol=solution(p,t)
 displays=[p['x']+' = '+tex(v[0])+', '+p['y']+' = '+tex(v[1]) if isinstance(v,tuple) else tex(v) for v in vals]
 identity=digest({'version':VERSION,'problem':prompt,'solution':sol,'bank':sorted(displays),'field':'radio','difficulty':level})
 qid=uid(identity);fid=uid(qid+'/selection')
 answers=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in displays]
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if not raw:field[':answer-field/correct']=[':answer/id',answers[hits[0]][':answer/id']]
 r.shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[field]},'generation':{'version':VERSION,'source':PROVENANCE,'level':level,'level_origin':'authored: all practice originals unrated','seed':seed,'template':t,'profile':profile,'parameters':p,'mathematical_fingerprint':canonical_task(p,t),'content_identity':identity,'recipes':recipes,'evidence_only':raw,'source_correct_option_missing':raw,'solution_origin':'canonical-derived authored: practice solutions absent','plots':'none'}}

# EASY: nonunit division/distribution, integer solutions, coefficients <=6.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: all nonunit coefficients, integer affine isolation/integer solution.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: same canonical operation, integer coefficients and fractional solution.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile');args=a.parse_args()
 records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
