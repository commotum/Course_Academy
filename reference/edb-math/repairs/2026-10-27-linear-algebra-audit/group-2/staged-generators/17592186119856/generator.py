"""Seeded span-membership parameter practice. No services, files, or database writes."""
import argparse
import json
import random
import uuid
from pathlib import Path
import sympy as S
from math_format import normalize_prose, normalize_tex, validate_generated_record, matrix_tex, system_tex

KP={'db_id':17592186119856,'id':'fac58a79-2d3f-5ad3-b1ab-c5ce279c4ebe','title':'Finding the Value of an Unknown Such That a Vector Lies in the Span of Given Vectors'}
K=S.Symbol('k')
PROFILES={
 'contributions':('omit_first','omit_second','subtract_second','swap'),
 'coordinates':('rhs_as_coefficients','sum_coefficients','first_coordinate','second_coordinate'),
 'elimination':('plus_numerator_x','plus_numerator_y','omit_determinant','wrong_determinant'),
 'mixed':('subtract_first','swap','second_coordinate','sum_coefficients'),
}
def tex(x): return normalize_tex(S.latex(S.sympify(x)))
def display(x): return '\n\n$$\n'+x+'\n$$\n\n'
def mat(rows): return matrix_tex([[tex(x) for x in row] for row in rows],augmented=True)
def vec(v): return matrix_tex([[tex(x)] for x in v])
def expr(a,b): return tex(a*S.Symbol('x_1')+b*S.Symbol('x_2'))
def uid(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/span/v1/'+s))
def solve(rows,rhs):
 t=rhs.index('k'); known=[i for i in range(3) if i!=t]
 B=S.Matrix([rows[i] for i in known]); d=S.Matrix([rhs[i] for i in known]);x=B.inv()*d
 return t,known,x,S.expand(sum(rows[t][j]*x[j] for j in range(2)))
def error_values(rows,rhs):
 t,known,x,key=solve(rows,rhs); a,b=rows[known[0]];c,d=rows[known[1]];p,q=[rhs[i] for i in known];e,f=rows[t];det=a*d-b*c
 return dict(omit_first=f*x[1],omit_second=e*x[0],subtract_second=e*x[0]-f*x[1],subtract_first=-e*x[0]+f*x[1],swap=e*x[1]+f*x[0],negate=-key,rhs_as_coefficients=e*p+f*q,sum_coefficients=e+f,first_coordinate=p,second_coordinate=q,plus_numerator_x=e*S.Rational(p*d+b*q,det)+f*x[1],plus_numerator_y=e*x[0]+f*S.Rational(a*q+p*c,det),omit_determinant=key*det,wrong_determinant=S.cancel(key*det/(a*d+b*c)) if a*d+b*c else S.nan)
def elimination(rows,rhs):
 # Put known equations first, then perform the exact named operations shown to the learner.
 t,known,x,key=solve(rows,rhs); order=known+[t]
 A=S.Matrix([[*r,K if v=='k' else v] for r,v in zip(rows,rhs)])
 stages=[]
 if order!=[0,1,2]:
  A=A[order,:]; stages.append(('Place the two known-coordinate equations first (a row permutation).',A.copy()))
 if A[0,0]==0:
  A.row_swap(0,1);stages.append((r'Apply $R_1\leftrightarrow R_2$.',A.copy()))
 for col in (0,1):
  pivot=A[col,col]
  if pivot!=1:
   A[col,:]=A[col,:]/pivot;stages.append((rf'Apply $R_{col+1}\leftarrow ({tex(1/pivot)})R_{col+1}$.',A.copy()))
  for row in range(col+1,3):
   factor=A[row,col]
   if factor:
    A[row,:]=A[row,:]-factor*A[col,:]
    A=A.applyfunc(S.expand)
    stages.append((rf'Apply $R_{row+1}\leftarrow R_{row+1}-({tex(factor)})R_{col+1}$.',A.copy()))
 assert S.expand(A[2,2]-(K-key))==0
 return stages,A

def build(rows,rhs,level,bank,profile,source_id=None):
 t,known,x,key=solve(rows,rhs); stages,end=elimination(rows,rhs)
 v=[K if n=='k' else n for n in rhs]
 span=r'$\mathbf{b}\in\operatorname{Span}\{\mathbf{a}_1,\mathbf{a}_2\}$'
 problem='Find the value of $k$ such that '+span+', where'+display(r'\mathbf{a}_1='+vec([r[0] for r in rows])+r',\qquad\mathbf{a}_2='+vec([r[1] for r in rows])+r',\qquad\mathbf{b}='+vec(v)+'.')
 initial=mat([[*r,b] for r,b in zip(rows,v)])
 if level=='easy':
  problem+=r'Use the augmented matrix for $x_1\mathbf{a}_1+x_2\mathbf{a}_2=\mathbf{b}$ to determine when the system is consistent:'+display(initial)
 solution='By definition, '+span+r' exactly when $x_1\mathbf{a}_1+x_2\mathbf{a}_2=\mathbf{b}$ has a solution. Equating coordinates gives'+display(system_tex([expr(*r)+' &='+tex(b) for r,b in zip(rows,v)]))
 solution+='Form the augmented matrix:'+display(initial)
 for instruction,A in stages:solution+=instruction+display(mat(A.tolist()))
 solution+=r'The last row represents $0x_1+0x_2='+tex(K-key)+r'$. Consistency therefore requires'+display(r'\begin{aligned}0 &='+tex(K-key)+r' \\ k &='+tex(key)+r'.\end{aligned}')
 solution+=r'The pivot equations give $x_2='+tex(x[1])+r'$ and $x_1='+tex(x[0])+r'$. These values also establish sufficiency:'+display('('+tex(x[0])+r')\mathbf{a}_1+('+tex(x[1])+r')\mathbf{a}_2='+vec([key if i==t else rhs[i] for i in range(3)])+'.')
 solution+=r'Therefore, $k='+tex(key)+'$ is the only value for which the vector lies in the span.'
 problem=normalize_prose(problem);solution=normalize_prose(solution)
 signature=json.dumps([level,problem,solution,rows,rhs,sorted(tex(b) for b in bank)],sort_keys=True)
 qid=uid(signature);choices=[{':answer/id':uid(qid+'/answer/'+tex(b)),':answer/type':':answer.type/math',':answer/value':tex(b)} for b in bank]
 answer_id=next(a[':answer/id'] for a,b in zip(choices,bank) if b==key)
 record={'knowledge_point':KP.copy(),'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':uid(qid+'/field'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',answer_id]}]},'generation':{'version':'1.0.1-content-identity','template':'span-parameter','profile':profile,'rows':rows,'rhs':rhs,'source_ids':[source_id] if source_id else {'easy':['29e56cc2-36b7-51bd-bd5d-6d1d8ef616b1'],'moderate':['f53bb678-a419-585c-a65e-c61f25afddb3','4e417e2f-54d8-52fa-a283-38ee2e22e96c'],'hard':['e12a2efc-9d88-56c5-96b5-ec530d76269d','d5c520f5-835e-5cc8-a0fb-53c3d5239f5d']}[level],'target_coordinate':t,'combination':[tex(n) for n in x],'final':tex(key)}}
 return validate_generated_record(record)

def sample(rng,level,profile):
 for attempt in range(10000):
  # Decide the target position and dependency case before incidental values.
  t=rng.randrange(3);which=rng.randrange(2);scale=rng.choice([-3,-2,-1,1,2,3])
  if level=='easy':
   a,b=rng.choice([-1,1]),rng.choice([-1,1]);c=rng.choice([-1,1])
   known_rows=[[a,b],[c,2*a*b*c]]
   scale=rng.choice([-2,-1,1,2])
  else:known_rows=[[rng.randint(-3,3) for j in range(2)] for i in range(2)]
  if level=='hard' and any(n==0 for r in known_rows for n in r):continue
  if S.det(S.Matrix(known_rows))==0:continue
  if level in ('easy','moderate'):target=[scale*n for n in known_rows[which]]
  else:
   target=[rng.randint(-4,4) for j in range(2)]
   if any(n==0 for n in target):continue
   if level=='hard' and any(target[0]*r[1]==target[1]*r[0] for r in known_rows):continue
  coefficients=[rng.randint(-4,4) for j in range(2)]
  if coefficients==[0,0] or (level=='hard' and 0 in coefficients):continue
  rows=known_rows.copy();rows.insert(t,target)
  rhs=[r[0]*coefficients[0]+r[1]*coefficients[1] for r in rows];rhs[t]='k'
  _,_,_,key=solve(rows,rhs)
  errors=error_values(rows,rhs);bank=[key]+[S.sympify(errors[name]) for name in PROFILES[profile]]
  if any(n.is_finite!=True or n.is_Integer!=True or abs(n)>100 for n in bank):continue
  if len(set(bank))!=5:continue
  rng.shuffle(bank)
  record=build(rows,rhs,level,bank,profile)
  record['generation'].update(dependency_row=which if level in ('easy','moderate') else None,dependency_scale=scale if level in ('easy','moderate') else None,attempts=attempt+1)
  return record
 raise RuntimeError('No distinct plausible bank found')
def batch_signature(record):
 field=record['question'][':question/answer-fields'][0]
 values=[S.sympify(a[':answer/value']) for a in field[':answer-field/choices']]
 key=S.sympify(record['generation']['final'])
 return sorted(values).index(key),sorted(set(abs(v) for v in values)).index(abs(key)),S.sign(key)

def generate(level,count,seed):
 rng=random.Random(seed)
 # Construct the batch deterministically, including banks, before balancing choice positions.
 # A short practice pool should not reward a fixed numerical rank or answer sign.
 for batch_attempt in range(10000):
  records=[];seen=set()
  for i in range(count):
   profile=rng.choice(list(PROFILES))
   for attempt in range(10000):
    r=sample(rng,level,profile);semantic=json.dumps([r['generation']['rows'],r['generation']['rhs']])
    if semantic not in seen:break
   else:raise RuntimeError('Exhausted semantic instances')
   seen.add(semantic);records.append(r)
  signatures=[batch_signature(r) for r in records]
  if count>=5:
   cap=(3*count+4)//5
   if any(max(sum(s[j]==v for s in signatures) for v in set(s[j] for s in signatures))>cap for j in (0,1)):continue
   if not any(s[2]<0 for s in signatures) or not any(s[2]>0 for s in signatures):continue
  # Each block of five has every correct position exactly once; no fixed positional action.
  positions=[]
  while len(positions)<count:
   block=list(range(5));rng.shuffle(block);positions.extend(block)
  for i,r in enumerate(records):
   f=r['question'][':question/answer-fields'][0];cs=f[':answer-field/choices']
   keyid=f[':answer-field/correct'][1];correct=next(c for c in cs if c[':answer/id']==keyid)
   cs.remove(correct);cs.insert(positions[i],correct)
   r['generation'].update(seed=seed,index=i,batch_attempts=batch_attempt+1)
  return records
 raise RuntimeError('No suitably varied deterministic batch found')

def main():
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate');p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json');a=p.parse_args()
 if a.count<0:p.error('--count must be nonnegative')
 print(json.dumps(generate('moderate' if a.difficulty=='unclassified' else a.difficulty,a.count,a.seed),indent=2))
if __name__=='__main__':main()
