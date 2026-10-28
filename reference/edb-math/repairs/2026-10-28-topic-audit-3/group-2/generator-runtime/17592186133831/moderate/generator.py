"""Seeded, portable plane vector line-integral construction. No evaluation."""
import argparse, hashlib, json, random, uuid
import sympy as s
import mpmath as mp
from core import T,X,Y,math_data,tex,vector,block
from math_format import normalize_prose,normalize_tex,validate_generated_record
VERSION='plane-setup-2'
KP={'db_id':17592186133831,'id':'e34a2cbf-0bed-50eb-9e62-7c6e55560cb9','title':'Constructing Line Integrals of a Vector-Valued Functions Over Plane Curves'}
FAMILIES={'easy':['polynomial','rotation','shifted_circle','exponential_root','spiral'],'moderate':['monomial','mixed_polynomial'],'hard':['mixed_spiral']}
SOURCE=dict(zip(FAMILIES['easy'],['q-124638','q-124687','q-124679','q-124680','q-124685']))
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+x))
def simple(x):return s.trigsimp(s.expand(x))
def sample(f,r):
 c=lambda:r.choice([-2,-1,1,2])
 p={'a':c(),'b':c(),'c':c(),'d':c(),'lower':'0','upper':str(r.choice([1,2])),'swap':r.choice([False,True]),'m':2,'n':3}
 if f in ('polynomial','monomial','mixed_polynomial'):p['m'],p['n']=r.sample([2,3,4],2)
 if f=='exponential_root':p.update(lower='1',upper=str(r.choice([2,3])))
 return p

def data(f,p):
 if f=='mixed_polynomial':
  P,Q=p['a']*X+p['b']*Y,p['c']*X*Y
  u,v=T**p['m'],T**p['n'];lo,hi=map(s.sympify,[p['lower'],p['upper']])
 else:
  P,Q,u,v,*rest=math_data(f,p);lo,hi=rest[-2:]
 if p.get('swap'):u,v=v,u
 A,B=[z.subs({X:u,Y:v},simultaneous=True) for z in (P,Q)]
 U,V=s.diff(u,T),s.diff(v,T)
 return P,Q,u,v,A,B,U,V,lo,hi

def products(A,B,U,V):return '('+tex(A)+')('+tex(U)+')+('+tex(B)+')('+tex(V)+')'
def integral(A,B,U,V,lo,hi,multiline):
 a='('+tex(A)+')('+tex(U)+')';b='('+tex(B)+')('+tex(V)+')'
 if multiline:return r'\begin{aligned}&\int_{'+tex(lo)+'}^{'+tex(hi)+r'}\bigl['+a+r'\\&\quad+'+b+r'\bigr]\,\mathrm{d}t\end{aligned}'
 return r'\int_{'+tex(lo)+'}^{'+tex(hi)+r'}\bigl['+a+'+'+b+r'\bigr]\,\mathrm{d}t'

def errors(u,v,U,V):
 # Complete, independently meaningful derivative/pairing errors. No arbitrary
 # numerical displacement of the right answer is used.
 pool=[('swap derivatives',V,U),('reverse x derivative',-U,V),('reverse y derivative',U,-V),('omit x derivative',s.Integer(1),V),('omit y derivative',U,s.Integer(1)),('omit both derivatives',s.Integer(1),s.Integer(1)),('use coordinates instead of derivatives',u,v),('use x coordinate instead of derivative',u,V),('use y coordinate instead of derivative',U,v)]
 # On a spiral: omit either term of a product rule, or get its sign wrong.
 for label,w in [('x',u),('y',v)]:
  if w.has(s.sin(T)) or w.has(s.cos(T)):
   approx=w/T if s.simplify(w/T).has(s.sin(T),s.cos(T)) and w.has(T*s.sin(T),T*s.cos(T)) else None
   if approx is not None:
    for name,z in [('omit trig derivative',approx),('omit derivative of t',s.diff(w,T)-approx),('wrong trig derivative sign',2*approx-s.diff(w,T))]:
     pool.append((label+' '+name,z,V) if label=='x' else (label+' '+name,U,z))
 return pool

def make(level,f,p,r,profile=0):
 P,Q,u,v,A,B,U,V,lo,hi=data(f,p);z=simple(A*U+B*V)
 # A complete rectangular error profile: correct/incorrect substitution
 # crossed with correct/incorrect derivative, plus one second mistake pair.
 # This keeps both operations necessary even with an easy derivative hint,
 # and prevents a unique modal factor intersection from revealing the key.
 field_errors=[('use x for both coordinates',P.subs({X:u,Y:u},simultaneous=True),Q.subs({X:u,Y:u},simultaneous=True)),('use y for both coordinates',P.subs({X:v,Y:v},simultaneous=True),Q.subs({X:v,Y:v},simultaneous=True)),('exchange substituted coordinates',P.subs({X:v,Y:u},simultaneous=True),Q.subs({X:v,Y:u},simultaneous=True)),('reverse first field component',-A,B),('reverse second field component',A,-B)]
 derivative_errors=errors(u,v,U,V)
 def scalar(expr):return float(mp.quad(s.lambdify(T,expr,'mpmath'),[float(lo),float(hi)]))
 for attempt in range(100):
  f1,f2=r.sample(field_errors,2);d1,d2=r.sample(derivative_errors,2)
  if simple(f1[1]-A)==0 and simple(f1[2]-B)==0:continue
  if simple(d1[1]-U)==0 and simple(d1[2]-V)==0:continue
  bank=[('correct',A,B,U,V),(f1[0],f1[1],f1[2],U,V),(d1[0],A,B,d1[1],d1[2]),(f1[0]+'; '+d1[0],f1[1],f1[2],d1[1],d1[2]),(f2[0]+'; '+d2[0],f2[1],f2[2],d2[1],d2[2])]
  scalars=[scalar(s.expand(aa*du+bb*dv)) for _,aa,bb,du,dv in bank]
  if all(abs(scalars[i]-scalars[j])>1e-9 for i in range(5) for j in range(i)):break
 else:raise ValueError('no distinct complete substitution/derivative profile')
 multiline=True
 vals=[normalize_tex(integral(aa,bb,du,dv,lo,hi,multiline)) for _,aa,bb,du,dv in bank]
 prompt=r'Which ordinary definite integral represents $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)='+vector(P,Q)+'$ and $C$ is the path $r(t)='+vector(u,v)+'$ for $t\\in ['+tex(lo)+','+tex(hi)+']$?'
 prompt+='\n\n'+r'Use the supplied parameterization and limits. Select the integral whose integrand is $F(r(t))\cdot r^{\prime}(t)$; do not evaluate it.'
 if level=='easy':prompt+='\n\n'+r'*Hint: $r^{\prime}(t)='+vector(U,V)+r'$. Substitute both coordinates into the field, then take the dot product.*'
 sub=lambda e:tex(e).replace('x','('+tex(u)+')').replace('y','('+tex(v)+')')
 sol='Use the vector line-integral formula:\n\n'+block(r'\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.')
 sol+='\n\nSubstitute the coordinates $x='+tex(u)+'$ and $y='+tex(v)+'$ into both field components:\n\n'+block(r'\begin{aligned}F(r(t))&=('+sub(P)+r')\,i\\&\quad+('+sub(Q)+r')\,j\\&=('+tex(A)+r')\,i\\&\quad+('+tex(B)+r')\,j.\end{aligned}')
 sol+='\n\nDifferentiate each path component:\n\n'+block(r'\begin{aligned}x^{\prime}(t)&=\frac{\mathrm{d}}{\mathrm{d}t}('+tex(u)+')='+tex(U)+r',\\y^{\prime}(t)&=\frac{\mathrm{d}}{\mathrm{d}t}('+tex(v)+')='+tex(V)+r'.\end{aligned}')
 sol+='\n\nMultiply matching components and add:\n\n'+block(r'\begin{aligned}&F(r(t))\cdot r^{\prime}(t)\\&=('+tex(A)+')('+tex(U)+r')\\&\quad+('+tex(B)+')('+tex(V)+r').\end{aligned}')
 if level!='hard':
  sol+='\n\nSimplify the products'+(r' using $\sin^2 t+\cos^2 t=1$ where applicable' if f in ('rotation','shifted_circle','spiral') else '')+':\n\n'+block(r'F(r(t))\cdot r^{\prime}(t)='+tex(z)+'.')
 sol+='\n\nKeep the supplied parameter limits. The required integral is\n\n'+block(integral(A,B,U,V,lo,hi,multiline))
 prompt,sol=normalize_prose(prompt),normalize_prose(sol)
 payload=json.dumps([prompt,sol,sorted(vals),level],ensure_ascii=False)
 qid=uid(hashlib.sha256(payload.encode()).hexdigest());fid=uid(qid+'field')
 answers=[{':answer/id':uid(fid+val),':answer/type':':answer.type/math',':answer/value':val} for val in vals]
 correct=answers[0][':answer/id'];r.shuffle(answers)
 record={'knowledge_point':KP,'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'template':f,'parameters':p,'source_ids':[SOURCE.get(f,'e-6316')],'profile':[a[0] for a in bank],'difficulty_origin':'authored progression; imported coverage easy only'}}
 validate_generated_record(record)
 return record

def generate_batch(level,count,seed):
 r=random.Random(seed);out=[];seen=set();schedule=[]
 while len(out)<count:
  if not schedule:schedule=list(FAMILIES[level]);r.shuffle(schedule)
  f=schedule.pop();
  for attempt in range(100):
   try:rec=make(level,f,sample(f,r),r)
   except ValueError:continue
   ident=rec['question'][':question/id']
   if ident not in seen:break
  else:raise RuntimeError('unable to construct distinct bank')
  out.append(rec);seen.add(ident)
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified','all'],default='easy');ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');a=ap.parse_args()
 if a.count<1:ap.error('count must be positive')
 levels=['easy','moderate','hard'] if a.difficulty=='all' else ['easy' if a.difficulty=='unclassified' else a.difficulty]
 print(json.dumps([rec for level in levels for rec in generate_batch(level,a.count,a.seed)],ensure_ascii=False,indent=2))
if __name__=='__main__':main()
