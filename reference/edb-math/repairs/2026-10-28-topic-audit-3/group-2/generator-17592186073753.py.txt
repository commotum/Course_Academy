#!/usr/bin/env python3
"""Portable, seeded substitution-system generator; source math basis 4613.

Preserves older templates for replay and explicit use. Current moderate blanks
and hard scalar banks follow labeled source practice. Unrated malformed q-12457
is evidence only; its corrected profile is explicit. No database or asset writes.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as s
from math_format import system_tex, normalize_prose, normalize_tex, checked_math_content
KP_ID=17592186073753
KP_UUID='b4352698-7af7-5d74-9c3a-0f951c3e6078'
TITLE='Solving a Challenging System of Linear Equations Using Substitution'
VERSION='challenging-substitution-3-portable'
HERE=Path(__file__).resolve().parent
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
 pre="Sometimes, it's handy to assign a number to each equation in a system, so that we can refer to them more easily:\n\n$$\n"+system_tex(eqs,annotations=['(1)','(2)'])+'\n$$\n\n'
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
  X,Y=r.choice(range(-9,10)),r.choice(range(-9,10));B,D,E=r.choice(range(2,6)),r.choice(range(2,6)),r.choice(range(2,6))
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

def legacy_generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
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
 if t=='pair_first':prompt='Using the method of substitution, find the solution of\n\n$$\n'+system_tex(eqs)+'\n$$'
 elif t=='pair_second':prompt='Using the method of substitution, find the solution of\n\n'+('$\\{'+ '; '.join(eqs)+'$' if raw else '$$\n'+system_tex(eqs)+'\n$$')
 elif t=='difference':prompt='Given the system of equations below, what is the value of $'+p['x']+' - '+p['y']+'$?\n\n$$\n'+system_tex(eqs,annotations=['(1)','(2)'])+'\n$$'
 else:prompt='Solve the following system of equations:\n\n$$\n'+system_tex(eqs)+'\n$$'
 prompt=normalize_prose(prompt)
 sol=normalize_prose(solution(p,t))
 displays=[p['x']+' = '+tex(v[0])+', '+p['y']+' = '+tex(v[1]) if isinstance(v,tuple) else tex(v) for v in vals]
 identity=digest({'version':VERSION,'problem':prompt,'solution':sol,'bank':sorted(displays),'field':'radio','difficulty':level})
 qid=uid(identity);fid=uid(qid+'/selection')
 answers=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in displays]
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if not raw:field[':answer-field/correct']=[':answer/id',answers[hits[0]][':answer/id']]
 r.shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[field]},'generation':{'version':VERSION,'source':PROVENANCE,'level':level,'level_origin':'authored: all practice originals unrated','seed':seed,'template':t,'profile':profile,'parameters':p,'mathematical_fingerprint':canonical_task(p,t),'content_identity':identity,'recipes':recipes,'attempts':attempt+1,'evidence_only':raw,'source_correct_option_missing':raw,'solution_origin':'canonical-derived authored: practice solutions absent','plots':'none'}}


MODERN = ('blank_pair', 'easy_pair', 'affine_difference', 'triangular_sum')
SOURCE_ROWS = {
 'q-112214':dict(A=21,B=-9,C=0,D=-15,E=5,F=-10,x='x',y='y'),
 'q-181207':dict(A=3,B=-6,C=-18,D=4,E=3,F=-2,x='p',y='q'),
 'q-18555':dict(A=-6,B=2,C=14,D=0,E=5,F=-25,x='a',y='b'),
}

def modern_equations(p, t):
 if t == 'blank_pair':
  return [add((p['A'],p['x']),(p['B'],p['y']))+' = '+str(p['C']),
          add((p['D'],p['x']),(p['E'],p['y']),(-p['F'],''))+' = 0']
 if t == 'triangular_sum':
  rows=[]
  for a,b,c in ((p['A'],p['B'],p['C']),(p['D'],p['E'],p['F'])):
   if a and b: rows.append(term(b,p['y'])+' = '+add((-a,p['x']),(c,'')))
   else: rows.append(add((a,p['x']),(b,p['y']),(-c,''))+' = 0')
  return rows
 return equations(p,True)

def modern_solution(p,t,row,j,direction):
 rows=[list(map(s.Integer,(p['A'],p['B'],p['C']))), list(map(s.Integer,(p['D'],p['E'],p['F'])))]
 vals=values(p);names=[p['x'],p['y']];w=1-j
 d,n,c=rows[row][j],rows[row][w],rows[row][2]
 ob,oa,oc=rows[1-row][j],rows[1-row][w],rows[1-row][2]
 h,m=c/d,-n/d;v,z=names[j],names[w];V,W=vals[j],vals[w]
 intro='We number the equations so that we can refer to them more easily:\n\n$$\n'+system_tex(modern_equations(p,t),annotations=['(1)','(2)'])+'\n$$\n\n'
 if t=='triangular_sum':
  ir=[(add((d,v),(-c,'')),'0'),(term(d,v),tex(c)),(v,tex(V))]
  sr=[(modern_equations(p,t)[1-row].split(' = ')[0],modern_equations(p,t)[1-row].split(' = ')[1]),
      (add((ob,par(tex(V))),(oa,z)),tex(oc)),
      (add((ob*V,''),(oa,z)),tex(oc)),(term(oa,z),tex(oc-ob*V)),(z,tex(W))]
  text=intro+'We will isolate a variable in one of the equations and then substitute it into the other equation. Using equation $('+str(row+1)+')$, we can solve for $'+v+'$ as follows:\n\n'+aligned(ir)
  text+='\n\nThen, we substitute $'+v+'='+tex(V)+'$ into equation $('+str(2-row)+')$ and solve for $'+z+'$:\n\n'+aligned(sr)
 else:
  ir=[(add((d,v),(n,z)),tex(c)),(term(d,v),add((-n,z),(c,''))),(v,add((m,z),(h,'')))]
  expr=add((m,z),(h,''))
  sr=[(add((ob,v),(oa,z),(-oc,'')),'0'),
      (add((ob,par(expr)),(oa,z),(-oc,'')),'0'),
      (add((ob*m,z),(ob*h,''),(oa,z),(-oc,'')),'0'),
      (term(ob*m+oa,z),tex(oc-ob*h)),(z,tex(W))]
  if t in ('blank_pair','easy_pair'):
   br=[(add((d,v),(n,par(tex(W)))),tex(c)),(add((d,v),(n*W,'')),tex(c)),(term(d,v),tex(c-n*W)),(v,tex(V))]
  else:
   br=[(v,expr),(v,add((m,par(tex(W))),(h,''))),(v,tex(V))]
  text=intro+'We will isolate a variable in one of the equations and then substitute it into the other equation. Using equation $('+str(row+1)+')$, we can solve for $'+v+'$ as follows:\n\n'+aligned(ir)
  text+='\n\nThen, we substitute $'+v+'='+expr+'$ into equation $('+str(2-row)+')$ and solve for $'+z+'$:\n\n'+aligned(sr)
  text+='\n\nIf we now substitute $'+z+'='+tex(W)+'$ back into '+('equation $('+str(row+1)+')$' if t in ('blank_pair','easy_pair') else '$'+v+'='+expr+'$')+', then we can find the value of $'+v+'$:\n\n'+aligned(br)
 text+='\n\nTherefore, the solution to the system of equations is $'+p['x']+'='+tex(vals[0])+',\\,'+p['y']+'='+tex(vals[1])+'$, which can be expressed as $('+tex(vals[0])+','+tex(vals[1])+')$.'
 if t not in ('blank_pair','easy_pair'):
  if t=='triangular_sum':lhs=p['x']+'+'+p['y'];nums=tex(vals[0])+'+'+par(tex(vals[1]));ans=sum(vals)
  else:
   a,b=(0,1) if direction=='x-y' else (1,0)
   lhs=names[a]+'-'+names[b];nums=tex(vals[a])+'-'+par(tex(vals[b]));ans=vals[a]-vals[b]
  text+=' So,\n\n$$\n'+lhs+'='+nums+'='+tex(ans)+'.\n$$'
 return text

def modern_bank(p,t,direction,row=0,j=0,candidate_pairs=None):
 X,Y=values(p)
 if t=='blank_pair':return [X,Y]
 if t=='easy_pair':
  if candidate_pairs is None:raise ValueError('Easy bank requires explicit shared candidates')
  pairs=[tuple(map(s.Rational,v)) for v in candidate_pairs]
  rows=[(p['A'],p['B'],p['C']),(p['D'],p['E'],p['F'])]
  a,b,c=rows[row]
  if len(pairs)!=5 or len(set(pairs))!=5 or (X,Y) not in pairs:
   raise ValueError('Easy bank must contain five distinct candidates and the solution')
  if any(not all(z.is_Integer and abs(z)<=6 for z in v) or a*v[0]+b*v[1]!=c for v in pairs):
   raise ValueError('Easy candidates must satisfy isolation row within integer bounds')
  return [(X,Y)]+[v for v in pairs if v!=(X,Y)]
 if t=='triangular_sum':return [X+Y,-X-Y,X-Y,Y-X,-2*Y]
 diff=X-Y if direction=='x-y' else Y-X
 return [diff,X+Y,-diff,0,-X-Y]

def easy_candidate_pool(p,row,j):
 a,b,c=[(p['A'],p['B'],p['C']),(p['D'],p['E'],p['F'])][row]
 d,n=(a,b) if j==0 else (b,a)
 if abs(d)!=1 or not n or not c:raise ValueError('Easy isolation requires unit divisor and nonzero slope/intercept')
 return [(x,y) for x in range(-6,7) for y in range(-6,7) if a*x+b*y==c]

def easy_sample(r,row,j):
 # Build an exchangeable complete bank before assigning correctness. The other
 # equation carries the decisive evidence, as required by tutorial 8131.
 d=r.choice([-1,1]);m=r.choice([-2,-1,1,2]);h=r.choice([-6,-5,-4,-3,-2,-1,1,2,3,4,5,6])
 iz=[0,0,d*h];iz[j]=d;iz[1-j]=-d*m
 provisional=dict(zip('ABCDEF',iz+iz));provisional.update(x='x',y='y')
 candidates=r.sample(easy_candidate_pool(provisional,0,j),5)
 X,Y=r.choice(candidates)
 a,b=r.choice([-7,-6,-5,-4,-3,-2,2,3,4,5,6,7]),r.choice([-7,-6,-5,-4,-3,-2,2,3,4,5,6,7])
 if iz[0]*b-iz[1]*a==0:raise ValueError('Parallel coefficient rows')
 other=[a,b,a*X+b*Y]
 rows=[iz,other] if row==0 else [other,iz]
 p=dict(zip('ABCDEF',rows[0]+rows[1]));p.update(x='x',y='y')
 return p,candidates

def modern_sample(r,t,row,j,signs):
 # Answer-bearing assignments (row, variable, signs, response) precede values.
 vals=[0 if sign==0 else sign*r.randint(1,6) for sign in signs]
 X,Y=vals;w=1-j
 d=r.choice([-1,1] if t=='easy_pair' else [-5,-4,-3,-2,2,3,4,5])
 m=0 if t=='triangular_sum' else r.choice([-3,-2,-1,1,2,3])
 h=vals[j]-m*vals[w]
 iz=[0,0,d*h];iz[j]=d;iz[w]=-d*m
 if t=='affine_difference':
  import math
  g=math.gcd(X,Y)
  if not g:raise ValueError('Degenerate homogeneous equation')
  scale=r.choice([-3,-2,2,3]);other=[scale*Y//g,-scale*X//g,0]
  if min(abs(other[0]),abs(other[1]))<2:raise ValueError('Nonunit hard coefficients')
 elif t=='triangular_sum':
  a,b=r.choice([-6,-5,-4,-3,-2,2,3,4,5,6]),r.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
  other=[a,b,a*X+b*Y]
 else:
  a,b=r.choice([-7,-6,-5,-4,-3,-2,2,3,4,5,6,7]),r.choice([-7,-6,-5,-4,-3,-2,2,3,4,5,6,7])
  other=[a,b,a*X+b*Y]
 rows=[iz,other] if row==0 else [other,iz]
 p=dict(zip('ABCDEF',rows[0]+rows[1]));p.update(x='x',y='y')
 if max(abs(p[k]) for k in 'ABDE')>30:raise ValueError('Coefficient bound')
 values(p)
 return p

@checked_math_content
def generate(level='moderate',seed=0,template=None,field_type=None,parameters=None,profile=None,
             isolate_row=None,isolate_variable=None,direction=None,candidate_pairs=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unsupported difficulty')
 if template in TEMPLATES or (profile and profile.startswith('source_')):
  rec=legacy_generate(level,seed,template,field_type,parameters,profile)
  if rec['generation']['evidence_only']:raise ValueError('Raw malformed source profile is evidence only; use replay_source')
  return rec
 r=random.Random(seed)
 t=template or ('easy_pair' if level=='easy' else 'blank_pair' if level=='moderate' else r.choice(['affine_difference','triangular_sum']))
 if t not in MODERN or {'easy_pair':'easy','blank_pair':'moderate','affine_difference':'hard','triangular_sum':'hard'}[t]!=level:raise ValueError('Template/difficulty mismatch')
 if field_type not in (None,'blank' if t=='blank_pair' else 'radio'):raise ValueError('Field type mismatch')
 row=r.randrange(2) if isolate_row is None else isolate_row
 j=r.randrange(2) if isolate_variable is None else isolate_variable
 if row not in (0,1) or j not in (0,1):raise ValueError('Isolation role out of bounds')
 direction=direction or r.choice(['x-y','y-x'])
 if direction not in ('x-y','y-x'):raise ValueError('Unknown difference direction')
 # Select a solution sign case first. Zero is allowed where the complete bank permits it.
 signs=None if t=='easy_pair' else r.choice([(a,b) for a in (-1,0,1) for b in (-1,0,1)] if t=='blank_pair' else [(-1,-1),(-1,1),(1,-1),(1,1)])
 rejected={}
 for attempt in range(1000):
  try:
   if t=='easy_pair' and parameters is None:
    p,easy_pairs=easy_sample(r,row,j)
   else:
    p=normalized(parameters) if parameters is not None else modern_sample(r,t,row,j,signs)
    easy_pairs=candidate_pairs
    if t=='easy_pair' and easy_pairs is None:
     pool=easy_candidate_pool(p,row,j);correct=values(p)
     if correct not in pool:raise ValueError('Easy solution outside candidate bounds')
     easy_pairs=[correct]+r.sample([v for v in pool if v!=correct],4)
   rows=[(p['A'],p['B'],p['C']),(p['D'],p['E'],p['F'])]
   d=rows[row][j];n=rows[row][1-j]
   if not d or (t=='triangular_sum')!=(n==0):raise ValueError('Isolation role mismatch')
   if t!='triangular_sum' and (rows[row][2]%d or n%d):raise ValueError('Affine isolate must have integer coefficients')
   vals=modern_bank(p,t,direction,row,j,easy_pairs)
   if t!='blank_pair' and len(set(vals))!=5:raise ValueError('Whole bank collision')
   break
  except (ValueError,ZeroDivisionError) as e:
   if parameters is not None:raise
   rejected[str(e)]=rejected.get(str(e),0)+1
 else:raise ValueError('No valid instance for chosen role/sign case')
 p['x'],p['y']=r.choice([('x','y'),('p','q'),('a','b'),('u','v')]) if parameters is None else (p['x'],p['y'])
 X,Y=values(p);eqs=modern_equations(p,t)
 if t=='easy_pair':signs=[int(s.sign(X)),int(s.sign(Y))]
 if t=='easy_pair':
  prompt='Using the method of substitution, find the solution of\n\n$$\n'+system_tex(eqs)+'\n$$'
 elif t=='blank_pair':
  prompt='Consider the following system of equations:\n\n$$\n'+system_tex(eqs)+'\n$$\n\nFind the solution $('+p['x']+','+p['y']+')$ to this system using the method of substitution.\n\n$('+p['x']+','+p['y']+')=($\n{{field-1}}\n$,$\n{{field-2}}\n$)$'
 else:
  target=p['x']+'+'+p['y'] if t=='triangular_sum' else (p['x']+'-'+p['y'] if direction=='x-y' else p['y']+'-'+p['x'])
  prompt='Given the system of equations below, what is the value of $'+target+'$?\n\n$$\n'+system_tex(eqs)+'\n$$'
 prompt=normalize_prose(prompt);sol=normalize_prose(modern_solution(p,t,row,j,direction))
 displays=[normalize_tex(p['x']+' = '+tex(v[0])+', '+p['y']+' = '+tex(v[1]) if isinstance(v,tuple) else tex(v)) for v in vals]
 identity=digest({'version':VERSION,'problem':prompt,'bank':sorted(displays),'template':t,'difficulty':level})
 qid=uid(identity);fields=[]
 if t=='blank_pair':
  for index in (1,0): # preserve captured array order; keys own coordinate mapping
   key='field-'+str(index+1);fid=uid(qid+'/'+key);aid=uid(fid+'/'+displays[index])
   choice={':answer/id':aid,':answer/type':':answer.type/math',':answer/value':displays[index]}
   fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/blank',':answer-field/choices':[choice],':answer-field/correct':[':answer/id',aid]})
 else:
  fid=uid(qid+'/selection')
  correct_display=displays[0]
  if t=='easy_pair':displays.sort() # presentation randomness independent of the assigned key
  choices=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in displays]
  correct=next(a[':answer/id'] for a in choices if a[':answer/value']==correct_display);r.shuffle(choices)
  fields=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
  'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':fields},
  'generation':{'version':VERSION,'source':PROVENANCE,'seed':seed,'template':t,'profile':'easy_consistent_isolation' if t=='easy_pair' else t,'parameters':p,'isolate_row':row,'isolate_variable':j,'direction':direction if t=='affine_difference' else None,'solution_sign_case':signs,'attempts':attempt+1,'rejections':rejected,'mathematical_fingerprint':digest({'system':canonical_task(p,'pair_first'),'response':'pair' if t in ('blank_pair','easy_pair') else 'sum' if t=='triangular_sum' else direction}),'source_refs':{'easy_pair':['q-12444'],'blank_pair':['q-181207'],'affine_difference':['q-112214'],'triangular_sum':['q-18555']}[t],'plots':'none'}}

def replay_source(source_id,repair=False):
 """Immutable source replay with explicit, documented key-only/correct-bank repair."""
 import copy
 source=next(q for q in SOURCE['material']['kp'][':knowledge-point/questions'] if q[':question/math-academy-id']==source_id)
 q=copy.deepcopy(source)
 # Flatten captured enum maps, remove database-local IDs; preserve all substantive fields.
 def flatten(obj):
  if isinstance(obj,list):return [flatten(x) for x in obj]
  if not isinstance(obj,dict):return obj
  if ':db/ident' in obj:return obj[':db/ident']
  return {k:flatten(v) for k,v in obj.items() if k!=':db/id'}
 q=flatten(q)
 for f in q[':question/answer-fields']:
  if isinstance(f.get(':answer-field/correct'),dict):f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
 if repair and source_id in SOURCE_PARAMETERS:
  p=SOURCE_PARAMETERS[source_id];t={'q-12444':'pair_first','q-12457':'pair_second','q-18483':'difference'}[source_id]
  q[':question/worked-solution']=normalize_prose(solution(p,t))
  f=q[':question/answer-fields'][0];X,Y=values(p)
  expected=tex(X-Y) if t=='difference' else p['x']+' = '+tex(X)+', '+p['y']+' = '+tex(Y)
  if source_id=='q-12457':
   a=next(a for a in f[':answer-field/choices'] if a[':answer/value'].replace(' ','')=='a=-4,b=4')
   a[':answer/value']=expected;a[':answer/id']=uid(f[':answer-field/id']+'/'+expected)
  for a in f[':answer-field/choices']:
   if a[':answer/value'].replace(' ','')==expected.replace(' ',''):f[':answer-field/correct']=[':answer/id',a[':answer/id']]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'source_id':source_id,'replay':True,'repair':repair,'source_difficulty':source.get(':question/difficulty'),'evidence_only':not repair and source_id in SOURCE_PARAMETERS}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard'],default='moderate');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['json'],default='json');args=a.parse_args()
 if args.count<0:a.error('--count must be nonnegative')
 print(json.dumps([generate(args.difficulty,args.seed+i) for i in range(args.count)],indent=2))
