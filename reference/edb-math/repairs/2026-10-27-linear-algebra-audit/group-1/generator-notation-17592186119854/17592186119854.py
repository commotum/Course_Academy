#!/usr/bin/env python3
"""Three-coefficient linear combinations with exact, small-system elimination.

source_generate retains captured profiles for offline source replay only. Normal
practice constructs new matrices, RHS vectors, targets and mistake-based banks.
"""
import argparse,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
from vector_notation import vector_prose, plain_vector_prose
HERE=Path(__file__).with_suffix('')
from math_format import matrix_tex,system_tex,normalize_prose,normalize_tex,checked_math_content
SOURCE=json.loads((HERE/'source.json').read_text());RAW=SOURCE['record'];KP_ID=17592186119854;KP_UUID=RAW[':knowledge-point/id']
GENERATOR_UUID=str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:generator:'+str(KP_ID)))
VERSION='three-coefficient-systems-3-notation-v1';SUPPORTED_LEVELS=('easy','moderate','hard')
TARGETS={}
CASES={q[':question/math-academy-id']:q for q in RAW[':knowledge-point/questions'] if q.get(':question/difficulty') and q.get(':question/worked-solution') and all(':answer-field/correct' in f for f in q[':question/answer-fields'])}
EXAMPLE=RAW[':knowledge-point/canonical-example']
CASES[EXAMPLE[':question/math-academy-id']]=EXAMPLE
# Operations are replayed in source order; add means Ri := Ri + c Rj.
OPS={
'e-6191':[('swap',0,1),('add',2,1,1),('scale',2,sp.Rational(1,4))],
'q-34243':[('add',2,0,-1),('add',2,1,-2),('scale',2,sp.Rational(1,3))],
'q-74011':[('add',1,0,1),('add',2,1,1)],
'q-74043':[('add',2,0,-4),('swap',1,2),('scale',1,sp.Rational(1,7)),('add',2,1,5)],
'q-34566':[('add',1,0,-2),('add',2,0,-3)],
'q-105168':[('add',1,0,-3),('add',2,0,2)],
'q-105169':[('add',1,0,-5),('add',2,0,2)],
'q-105170':[('add',1,0,1),('add',2,0,-2)],
'q-105172':[('add',1,0,5),('add',2,0,3)],
'q-73992':[('add',2,0,-3),('swap',1,2),('scale',1,sp.Rational(1,2)),('scale',2,sp.Rational(1,5))],
'q-74006':[('add',2,0,-1),('scale',1,-1),('add',2,1,3)],
'q-74028':[('add',2,0,-1),('scale',1,sp.Rational(1,3)),('scale',2,sp.Rational(-1,2))],
'q-74032':[('add',2,0,-1),('swap',1,2),('add',2,1,2),('scale',2,sp.Rational(-1,15))],
'q-74035':[('add',2,0,-3),('add',2,1,-1),('scale',1,sp.Rational(1,5)),('scale',2,-1)],
'q-74046':[('add',2,0,-2),('add',2,1,1),('scale',2,sp.Rational(-1,4))],
'q-105171':[('add',1,0,-2),('add',2,0,1)]}
VARS=sp.symbols('x_1 x_2 x_3')
def parse(q):
 ms=re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)
 vs=[sp.Matrix([sp.Integer(v.strip()) for v in m.split(r'\\')]) for m in ms]
 assert len(vs)==4 and all(v.shape==(3,1) for v in vs)
 return sp.Matrix.hstack(*vs[:3]),vs[3]
def target(sid):return TARGETS.get(sid, (1,1,-1) if sid=='q-74028' else (1,1,1))
def level(sid):return 'moderate' if sid=='e-6191' else CASES[sid][':question/difficulty'][':db/ident'].split('/')[-1]
def states(sid,A,b):
 m=A.row_join(b);out=[m.copy()];labels=[]
 for op in OPS[sid]:
  if op[0]=='add':
   _,i,j,c=op;m[i,:]=m[i,:]+c*m[j,:];label=rf'R_{{{i+1}}}:=R_{{{i+1}}}+({sp.latex(c)})R_{{{j+1}}}'
  elif op[0]=='swap':
   _,i,j=op;m.row_swap(i,j);label=rf'R_{{{i+1}}}\leftrightarrow R_{{{j+1}}}'
  else:
   _,i,c=op;m[i,:]=c*m[i,:];label=rf'R_{{{i+1}}}:=({sp.latex(c)})R_{{{i+1}}}'
  out.append(m.copy());labels.append(label)
 return out,labels
def calc(sid,b):
 A,b0=parse(CASES[sid]);b=sp.Matrix(b);steps,labels=states(sid,A,b)
 if A.det()!=0:
  x=A.inv()*b;value=sum(c*v for c,v in zip(target(sid),x))
 else:
  x=None;value=None;assert list(steps[-1][2,:3])==[0,0,0] and steps[-1][2,3]!=0
 return A,b,steps,labels,x,value

def bank(sid,b,numeric_rank=None):
 if sid=='e-6191':return []
 A,b0=parse(CASES[sid]);_,_,_,_,x0,z0=calc(sid,b0);_,_,ss,_,x,z=calc(sid,b)
 origin=z0 if level(sid)=='moderate' else states(sid,A,b0)[0][-1][2,3]
 anchor=z if level(sid)=='moderate' else ss[-1][2,3]
 if level(sid)=='moderate' and numeric_rank is not None:
  values=sorted(sp.Integer(a[':answer/value']) for a in CASES[sid][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/type'][':db/ident']==':answer.type/math')
  if not 1<=numeric_rank<=len(values):raise ValueError('Invalid numeric rank')
  origin=values[numeric_rank-1]
 out=[]
 for a in CASES[sid][':question/answer-fields'][0][':answer-field/choices']:
  value=a[':answer/value'];typ=a[':answer/type'][':db/ident']
  recipe='literal-no-solution' if typ==':answer.type/text' else f'anchor + ({sp.Integer(value)-origin})'
  out.append({'value':value if typ==':answer.type/text' else str(anchor+sp.Integer(value)-origin),'type':typ,'recipe':recipe,'source_answer_id':a[':answer/id']})
 assert len(set((a['type'],a['value']) for a in out))==5
 return out

def expr(row):return sp.latex(sum(a*x for a,x in zip(row,VARS)))
def mat(m,aug=False):return matrix_tex([[sp.latex(v) for v in m.row(i)] for i in range(m.rows)],augmented=aug)
def display(s):return '\n\n$$\n'+s+'\n$$\n\n'
def system(m):return system_tex([expr(list(m.row(i))[:3])+'='+sp.latex(m[i,3]) for i in range(3)])
def content(sid,b):
 A,b,ss,labels,x,z=calc(sid,b);t=expr(target(sid));eq=r'x_1a_1+x_2a_2+x_3a_3=b'
 p='Consider the vectors'+display(r',\quad '.join('a_'+str(j+1)+'='+mat(A[:,j]) for j in range(3))+r',\quad b='+mat(b))+f'If ${eq},$ then what is ${t}?$'
 # Preserve source stages: scalar vector expansion, collected components, system,
 # augmented matrix, annotated row steps, triangular system, back substitution,
 # concrete linear combination, final requested expression (or contradiction).
 vecsum='+'.join('x_'+str(j+1)+mat(A[:,j]) for j in range(3))
 scaled='+'.join(matrix_tex([[sp.latex(A[i,j]*VARS[j])] for i in range(3)]) for j in range(3))
 collected=matrix_tex([[expr(list(A.row(i)))] for i in range(3)])
 s=f'If ${eq}$, then we have'+display(r'\begin{aligned}'+vecsum+'&='+mat(b)+r' \\ '+scaled+'&='+mat(b)+r' \\ '+collected+'&='+mat(b)+r'\end{aligned}')
 s+='Equating the corresponding components, we get the following system:'+display(system(ss[0]))
 s+='We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:'+display('M='+mat(ss[0],True))
 rows=['M&='+mat(ss[0],True)]
 for m,label in zip(ss[1:],labels):rows.append(r'&\sim '+mat(m,True)+' && '+label)
 s+='Row-reducing the augmented matrix, we get'+display(r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}')
 s+='The system is now'+display(system(ss[-1]))
 if x is None:
  d=sp.latex(ss[-1][2,3]);s+=f'However, the final equation $0={d}$ gives a false statement. So the system has no solution.'
 else:
  m=ss[-1];s+=f'From the third equation, we get $x_3={sp.latex(x[2])}.$ '
  s+='Substituting this value into the second equation, we get'+display(sp.latex(m[1,1])+r'x_2+('+sp.latex(m[1,2])+')('+sp.latex(x[2])+')='+sp.latex(m[1,3])+r'\quad\Rightarrow\quad x_2='+sp.latex(x[1]))
  s+='Finally, substituting these values into the first equation, we obtain'+display(sp.latex(m[0,0])+'x_1+('+sp.latex(m[0,1])+')('+sp.latex(x[1])+')+('+sp.latex(m[0,2])+')('+sp.latex(x[2])+')='+sp.latex(m[0,3])+r'\quad\Rightarrow\quad x_1='+sp.latex(x[0]))
  s+='So, the solution of the system is '+', '.join('$x_'+str(i+1)+'='+sp.latex(v)+'$' for i,v in enumerate(x))+', which means'+display(sp.latex(x[0])+'a_1+('+sp.latex(x[1])+')a_2+('+sp.latex(x[2])+')a_3=b.')
  s+='Consequently,'+display(t+'='+ '+'.join('('+sp.latex(c*v)+')' for c,v in zip(target(sid),x))+'='+sp.latex(z)+'.')
 return normalize_prose(vector_prose(p)),normalize_prose(vector_prose(s))

def structure(sid,b):
 # Quotient equation row scaling/order and permutation of supplied vector columns.
 import itertools
 A,_=parse(CASES[sid]);b=sp.Matrix(b);representations=[]
 for perm in itertools.permutations(range(3)):
  rows=[]
  for i in range(3):
   row=[A[i,j] for j in perm]+[b[i]];pivot=next(v for v in row if v!=0);rows.append(tuple(str(v/pivot) for v in row))
  representations.append((tuple(target(sid)[j] for j in perm),tuple(sorted(rows))))
 return min(representations)
def fingerprint(sid,b):return hashlib.sha256(json.dumps(structure(sid,b)).encode()).hexdigest()

@checked_math_content
def source_generate(difficulty,seed=0,template=None,parameters=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty+'; see capabilities.json')
 rng=random.Random(seed);sid=template or rng.choice(sorted(s for s in CASES if s.startswith('q-') and level(s)==difficulty));assert level(sid)==difficulty
 A,b0=parse(CASES[sid])
 # Decide the answer-bearing bank role before incidental coefficient values.
 numeric_count=sum(a[':answer/type'][':db/ident']==':answer.type/math' for f in CASES[sid].get(':question/answer-fields',[]) for a in f[':answer-field/choices'])
 numeric_rank=rng.randint(1,numeric_count) if difficulty=='moderate' and numeric_count else None
 if parameters is None:
  for _ in range(100):
   if difficulty=='moderate':b=A*sp.Matrix([rng.randint(-7,7) for _ in range(3)])
   else:b=sp.Matrix([rng.randint(-9,9) for _ in range(3)])
   try:calc(sid,b);bank(sid,b)
   except (AssertionError,ValueError):continue
   if b!=b0:break
  else:raise ValueError('Bounded sampler exhausted')
 else:
  b=sp.Matrix(parameters['b'])
  if b.shape!=(3,1) or any(not v.is_Integer for v in b):raise ValueError('RHS must contain three integers')
  bank_rng=random.Random(hashlib.sha256(json.dumps([seed,sid,list(map(str,b))]).encode()).hexdigest())
  numeric_rank=parameters.get('numeric_rank',bank_rng.randint(1,numeric_count)) if numeric_count and difficulty=='moderate' else None
 # Original parameters replay the entire observed bank unless an extension is explicitly requested.
 if b==b0 and (parameters is None or 'numeric_rank' not in parameters):numeric_rank=None
 A,b,ss,labels,x,z=calc(sid,b);options=bank(sid,b,numeric_rank);p,s=content(sid,b);fp=fingerprint(sid,b)
 rng.shuffle(options)
 ident=lambda name:str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),name))
 bank_key=json.dumps(sorted((o['type'],o['value']) for o in options))
 qid=ident(VERSION+':'+sid+':'+fp+':'+bank_key);fid=ident(qid+':selection');answers=[];correct=None
 for o in options:
  aid=ident(fid+':'+o['type']+':'+o['value']);answers.append({':answer/id':aid,':answer/type':o['type'],':answer/value':normalize_tex(o['value']) if o['type']==':answer.type/math' else o['value']})
  if (difficulty=='hard' and o['type']==':answer.type/text') or (difficulty=='moderate' and o['type']==':answer.type/math' and sp.Rational(o['value'])==z):correct=aid
 assert correct is not None or sid=='e-6191'
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':RAW[':knowledge-point/title']},'question':{':question/id':qid,':question/problem':p,':question/worked-solution':s,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[] if sid=='e-6191' else [{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':sid,'bank_profile':sid+(':source-replay' if numeric_rank is None else ':reanchored'), 'numeric_rank':numeric_rank, 'source_kind':'worked-example' if sid=='e-6191' else 'practice','parameters':{'b':list(map(int,b)),**({'numeric_rank':numeric_rank} if numeric_rank is not None else {})},'domain':'fixed observed coefficient matrix; integer RHS; moderate integer solution coordinates in [-7,7], hard inconsistent b in [-9,9]^3','source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'source_question_id':CASES[sid][':question/id'],'mathematical_fingerprint':fp,'recipes':[o['recipe'] for o in options],'sympy':sp.__version__,'assets':[]}}

def source_batch(difficulty,count,seed):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported level')
 if count<1:raise ValueError('Count must be positive')
 out=[];seen=set();templates=sorted(s for s in CASES if s.startswith('q-') and level(s)==difficulty)
 random.Random(seed).shuffle(templates)
 for i in range(max(100,count*20)):
  r=source_generate(difficulty,seed+i,templates[i%len(templates)]);fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:out.append(r);seen.add(fp)
  if len(out)==count:return out
 raise ValueError('Distinct bounded sampler exhausted')

def elimination_ops(A):
 """Produce actual forward elimination, normalizing each available pivot."""
 m=A.copy();ops=[];row=0
 for col in range(3):
  pivot=next((i for i in range(row,3) if m[i,col]),None)
  if pivot is None:continue
  if pivot!=row:m.row_swap(row,pivot);ops.append(('swap',row,pivot))
  v=m[row,col]
  if v!=1:m[row,:]=m[row,:]/v;ops.append(('scale',row,1/v))
  for i in range(row+1,3):
   c=-m[i,col]
   if c:m[i,:]=m[i,:]+c*m[row,:];ops.append(('add',i,row,c))
  row+=1
  if row==3:break
 return ops

def error_values(A,b,t,x):
 """Numeric alternatives are concrete coefficient/translation mistakes."""
 pool={}
 def add(v,why):
  if v.is_Integer:pool.setdefault(int(v),why)
 if x is None:
  # Ignore one inconsistent component and set a free coefficient to zero.
  import itertools
  for rows in itertools.combinations(range(3),2):
   for fixed in range(3):
    cols=[j for j in range(3) if j!=fixed];sub=A.extract(rows,cols)
    if sub.det():
     vals=sub.inv()*b.extract(rows,[0]);y=sp.zeros(3,1)
     for j,v in zip(cols,vals):y[j]=v
     add(sum(t[j]*y[j] for j in range(3)),'ignore a component equation and set a free coefficient to zero')
     for j in range(3):add(sum(t[k]*y[k] for k in range(3))-2*t[j]*y[j],'ignore a component equation and reverse one coefficient sign')
 else:
  z=sum(t[i]*x[i] for i in range(3))
  for i in range(3):
   add(z-t[i]*x[i],'omit coefficient '+str(i+1)+' from the requested expression')
   add(z-2*t[i]*x[i],'reverse the sign of coefficient '+str(i+1))
   add(x[i],'report only coefficient '+str(i+1))
  add(sum(x),'sum coefficients without applying the requested signs')
  add(-z,'reverse the sign of the requested result')
  # Interchanging rows and columns is a translation error specific to this A,b.
  y=A.T.inv()*b
  add(sum(t[i]*y[i] for i in range(3)),'treat the given vectors as rows instead of columns')
 add(sum(t[i]*b[i] for i in range(3)),'use target-vector components as the coefficients')
 return pool

def construct(difficulty,rng,kind=None):
 # Small unimodular triangular cores keep arithmetic secondary to translation.
 U=sp.eye(3)
 for i,j in [(0,1),(0,2),(1,2)]:
  U[i,j]=rng.choice([-1,0,1] if difficulty=='easy' else [-2,-1,0,1,2])
 if difficulty=='easy' and not any(U[i,j] for i,j in [(0,1),(0,2),(1,2)]):U[0,1]=1
 inconsistent=difficulty=='hard' and (kind=='inconsistent' or (kind is None and rng.randrange(2)==0))
 if inconsistent:U[2,:]=sp.zeros(1,3)
 A=U.copy()
 if difficulty!='easy':
  A[1,:]+=rng.choice([-1,1])*A[0,:]
  A[2,:]+=rng.choice([-1,1])*A[0,:]
  if difficulty=='hard':A[2,:]+=rng.choice([-1,1])*A[1,:]
  order=list(range(3));rng.shuffle(order);A=A[order,:]
 # Column permutation changes which coefficient is isolated, including in easy.
 order=list(range(3));rng.shuffle(order);A=A[:,order]
 for i in range(3):
  if rng.randrange(2):A[i,:]=-A[i,:]
 x=sp.Matrix([rng.randint(-3,3) for _ in range(3)])
 b=A*x
 if inconsistent:
  for _ in range(10):
   candidate=b.copy();candidate[rng.randrange(3)]+=rng.choice([-2,-1,1,2])
   if A.row_join(candidate).rank()>A.rank():b=candidate;break
  else:raise ValueError('No inconsistent RHS')
 t=rng.choice([(1,1,1),(1,1,-1),(1,-1,1),(-1,1,1)])
 return A,b,t

@checked_math_content
def generate(difficulty,seed=0,template=None,parameters=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty')
 if template not in (None,'triangular' if difficulty=='easy' else 'coupled'):raise ValueError('Template does not match difficulty')
 rng=random.Random(seed);sid='authored-'+difficulty
 for attempt in range(200):
  if parameters is not None:
   A=sp.Matrix(parameters['A']);b=sp.Matrix(parameters['b']);t=tuple(parameters.get('target',[1,1,1]))
  else:A,b,t=construct(difficulty,rng)
  if A.shape!=(3,3) or b.shape!=(3,1) or any(not v.is_Integer for v in list(A)+list(b)) or t not in [(1,1,1),(1,1,-1),(1,-1,1),(-1,1,1)]:raise ValueError('Invalid integer system or target')
  rank=A.rank()
  if rank<2 or (rank<3 and rank==A.row_join(b).rank()):
   if parameters is not None:raise ValueError('Consistent nonunique coefficients are outside this response contract')
   continue
  x=A.inv()*b if rank==3 else None;z=sum(t[i]*x[i] for i in range(3)) if x is not None else None
  if z is not None and not z.is_Integer:
   if parameters is not None:raise ValueError('Integer response required')
   continue
  pool=error_values(A,b,t,x)
  if z is not None:pool.pop(int(z),None)
  needed=3 if x is not None else 4
  if len(pool)<needed:
   if parameters is not None:raise ValueError('Insufficient distinct plausible errors')
   continue
  break
 else:raise ValueError('Bounded construction exhausted')
 # Reuse the source's displayed expansion/system/elimination/back-substitution stages.
 TARGETS[sid]=t;OPS[sid]=elimination_ops(A)
 CASES[sid]={':question/id':EXAMPLE[':question/id'],':question/difficulty':{':db/ident':':question.difficulty/'+difficulty},':question/problem':display(','.join(mat(A[:,j]) for j in range(3))+','+mat(b))}
 p,s=content(sid,b)
 wrong=rng.sample(sorted(pool),needed)
 opts=[(str(v),':answer.type/math',pool[v]) for v in wrong]
 if x is not None:opts.append((str(z),':answer.type/math','correct requested expression'))
 opts.append(('No solution',':answer.type/text','inconsistency check'))
 rng.shuffle(opts)
 data={'A':[[int(A[i,j]) for j in range(3)] for i in range(3)],'b':list(map(int,b)),'target':list(t)}
 fp=hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
 ident=lambda name:str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),name))
 qid=ident(VERSION+':'+fp+':'+json.dumps(opts));fid=ident(qid+':selection');answers=[];correct=None
 for value,typ,recipe in opts:
  aid=ident(fid+':'+typ+':'+value);answers.append({':answer/id':aid,':answer/type':typ,':answer/value':value})
  if value==('No solution' if x is None else str(z)):correct=aid
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':RAW[':knowledge-point/title']},'question':{':question/id':qid,':question/problem':p,':question/worked-solution':s,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':'triangular' if difficulty=='easy' else 'coupled','parameters':data,'mathematical_fingerprint':fp,'recipes':[o[2] for o in opts],'source_question_id':EXAMPLE[':question/id'],'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'assets':[]}}

def batch(difficulty,count,seed):
 if difficulty not in SUPPORTED_LEVELS or count<1:raise ValueError('Invalid level or count')
 out=[];seen=set();positions=[];ranks=[];hard_classes=[];target_ranks={}
 for i in range(max(100,count*100)):
  r=generate(difficulty,seed+i);f=r['question'][':question/answer-fields'][0];choices=f[':answer-field/choices'];key=f[':answer-field/correct'][1]
  pos=next(j for j,a in enumerate(choices) if a[':answer/id']==key);v=choices[pos][':answer/value'];numeric=v!='No solution'
  # No five-question practice pool should be solved by a constant position/rank,
  # and hard must require reconsidering consistency rather than its level label.
  if len(out)>=2 and positions.count(pos)>=max(2,(count+4)//5):continue
  rank=sorted(int(a[':answer/value']) for a in choices if a[':answer/type']==':answer.type/math').index(int(v)) if numeric else None
  if numeric and ranks.count(rank)>=max(1,(count+1)//2):continue
  target_key=tuple(r['generation']['parameters']['target'])
  if numeric and target_ranks.get((target_key,rank),0)>=max(1,(count+15)//16):continue
  if not numeric and target_ranks.get((target_key,None),0) and not any(target_ranks.get((target_key,k),0) for k in range(4)):continue
  if difficulty=='hard' and count>=2:
   want_numeric=(len(out)%2==0)
   if numeric!=want_numeric:continue
  fp=r['generation']['mathematical_fingerprint']
  if fp in seen:continue
  seen.add(fp);out.append(r);positions.append(pos)
  if numeric:
   ranks.append(rank)
  target_ranks[(target_key,rank)]=target_ranks.get((target_key,rank),0)+1
  hard_classes.append(numeric)
  if len(out)==count:return out
 raise ValueError('Distinct, decision-varied bounded sampler exhausted')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard'],required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--template');ap.add_argument('--format',choices=['json','markdown'],default='json');a=ap.parse_args()
 if a.count<1:ap.error('--count must be positive')
 records=[generate(a.difficulty,a.seed+i,a.template) for i in range(a.count)] if a.template else batch(a.difficulty,a.count,a.seed)
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records))
