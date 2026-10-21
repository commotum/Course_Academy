"""Singular 2x2 systems with independent intercept and consistency decisions."""
import argparse,copy,hashlib,json,random,re,uuid
from pathlib import Path
import sympy as sp
from math_format import matrix_tex, normalize_prose, normalize_tex, validate_generated_record
KP_ID=17592186105746
KP_UUID='07f2ae4c-ff07-5b99-a7b0-90f460081eef'
GENERATOR_UUID=str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/generator/'+KP_UUID))
HERE=Path(__file__).with_suffix('')
SNAPSHOT=json.loads((HERE/'source.json').read_text());SOURCE=SNAPSHOT['record']
CASES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
SUPPORTED_LEVELS=('easy','moderate')
y=sp.Symbol('y')
VERSION='independent-residual-v2'
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),x))
def number(s):
 s=s.strip().replace(' ','').replace(r'\,','')
 s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
 s=re.sub(r'(\d|\))(?=y)',r'\1*',s)
 return sp.sympify(s,locals={'y':y,'x':sp.Symbol('x')})
def tex(x):return sp.latex(x).replace(' ','')
def matrix_strings(s):return re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)
def matrix(s):return sp.Matrix([[number(v) for v in row.split('&')] for row in s.split(r'\\')])
def matrices(s):return [matrix(m) for m in matrix_strings(s)]
def scale_value(s,t):
 if t==1:return s
 z=number(s)
 if z.has(sp.Symbol('x')):return s
 return tex(z.subs(y,0)*t+sp.diff(z,y)*y)
def corrected_solution(sid):
 text=CASES[sid][':question/worked-solution']
 if sid=='q-130924':text=text.replace(r'-3 & 10 & 6',r'-3 & 12 & 6')
 if sid=='q-42159':
  text=text.replace(r'1 & 7 & 4 \\ 6 & 42 & -24',r'1 & 7 & 4 \\ 6 & 42 & 24')
 return text

def transform(text,t,solution=False):
 if t==1:return text
 held=[]
 def hold(s):held.append(s);return '@@H'+str(len(held)-1)+'@@'
 def mat(m):
  rows=m[1].split(r'\\');n=len(rows[0].split('&'));out=[]
  for i,row in enumerate(rows):
   entries=row.split('&')
   if n==3:entries[2]=' '+tex(number(entries[2])*t)+' '
   elif n==1 and len(rows)==2 and i==0 and entries[0].strip()!='x':entries[0]=' '+scale_value(entries[0],t)+' '
   out.append('&'.join(entries))
  return hold(r'\begin{bmatrix}'+r'\\'.join(out)+r'\end{bmatrix}')
 text=re.sub(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',mat,text,flags=re.S)
 # Equation RHSs in supplied/reduced systems, solved x and contradictions.
 # Row operations and all coefficient expressions remain fixed.
 text=re.sub(r'(?<![A-Za-z0-9])((?:-?\d*x[+\-0-9y ]*|x[+\-0-9y ]*|0)\s*&?=)([+\-0-9y ]+)',lambda m:m[1]+scale_value(m[2],t),text)
 for i,h in enumerate(held):text=text.replace('@@H'+str(i)+'@@',h)
 return text

def fingerprint(q):
 # Normalize each supplied equation by its x coefficient. Neither common row
 # scaling, row order, choice order nor different author identities adds variety.
 body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/problem'],re.S)
 if body:
  x=sp.Symbol('x');rows=[]
  for row in body[1].split(r'\\'):
   lhs,rhs=row.replace('&','').split('=');lhs=re.sub(r'(\d)(?=x)',r'\1*',lhs);z=number(lhs);rows.append([z.coeff(x),z.coeff(y),number(rhs.rstrip('.'))])
  a=sp.Matrix(rows)
 else:a=next(z for z in matrices(q.get(':question/worked-solution','')) if z.shape==(2,3))
 rows=sorted([tuple(str(a[i,j]/a[i,0]) for j in (1,2)) for i in range(2)])
 return digest(['reduce-and-solve-singular',rows])

def legacy_generate(difficulty='moderate',seed=0,template=None,parameters=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 rng=random.Random(seed);eligible=[s for s,q in CASES.items() if q[':question/difficulty'][':db/ident'].endswith('/'+difficulty)]
 sid=template or rng.choice(eligible)
 if sid not in eligible:raise ValueError('Template difficulty mismatch')
 t=(parameters or {}).get('rhs_scale',rng.choice([-4,-3,-2,-1,1,2,3,4]))
 if t not in [-4,-3,-2,-1,1,2,3,4]:raise ValueError('Outside validated finite domain')
 old=CASES[sid];q={':question/problem':transform(old[':question/problem'],t),':question/worked-solution':transform(corrected_solution(sid),t,True),':question/difficulty':':question.difficulty/'+difficulty}
 fp=fingerprint(q);qid=uid('question/'+fp+'/'+digest([transform(a[':answer/value'],t) for a in old[':question/answer-fields'][0][':answer-field/choices']]));q[':question/id']=qid;f=old[':question/answer-fields'][0];fid=uid(qid+'/selection');choices=[]
 for a in f[':answer-field/choices']:
  val=transform(a[':answer/value'],t);aid=uid(fid+'/'+val);choices.append({':answer/id':aid,':answer/type':a[':answer/type'][':db/ident'],':answer/value':val})
  if a[':answer/id']==f[':answer-field/correct'][':answer/id']:correct=aid
 q[':question/answer-fields']=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]
 values=[(a[':answer/type'],a[':answer/value']) for a in choices]
 key=next(a[':answer/value'] for a in choices if a[':answer/id']==correct)
 return record(q,sid,seed,{'rhs_scale':t},values,key)

def augmented(text):
 """Make the role of every three-column matrix explicit, including replay."""
 def replace(m):
  rows=[row.split('&') for row in m[1].split(r'\\')]
  return matrix_tex([[s.strip() for s in row] for row in rows],augmented=True) if len(rows[0])==3 else m[0]
 return re.sub(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',replace,text,flags=re.S)

def record(q,sid,seed,parameters,values,key):
 q[':question/problem']=normalize_prose(q[':question/problem'])
 q[':question/worked-solution']=normalize_prose(augmented(q[':question/worked-solution']))
 values=[(kind,normalize_tex(value) if kind==':answer.type/math' else normalize_prose(value)) for kind,value in values]
 key=normalize_tex(key) if key!='No solution' else key
 fp=fingerprint(q);qid=uid('question/'+fp+'/'+digest(values));fid=uid(qid+'/selection')
 q[':question/id']=qid
 choices=[{':answer/id':uid(fid+'/'+value),':answer/type':kind,':answer/value':value} for kind,value in values]
 correct=next(a[':answer/id'] for a in choices if a[':answer/value']==key)
 q[':question/answer-fields']=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]
 return validate_generated_record({'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE[':knowledge-point/title']},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'template':sid,'profile':sid,'seed':seed,'parameters':parameters,'mathematical_fingerprint':fp,'source_question_id':CASES[sid][':question/id'],'sympy_version':sp.__version__}})

def source_matrix(sid):
 body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',CASES[sid][':question/problem'],re.S)[1]
 x=sp.Symbol('x');rows=[]
 for row in body.split(r'\\'):
  lhs,rhs=row.replace('&','').split('=');lhs=re.sub(r'(\d)(?=x)',r'\1*',lhs);z=number(lhs)
  rows.append([z.coeff(x),z.coeff(y),number(rhs.rstrip('.'))])
 return sp.Matrix(rows)

def vector(first,second=y):
 return matrix_tex([['x'],['y']])+'='+matrix_tex([[tex(first)],[tex(second)]])+r',\,y\in (-\infty ,\infty )'

def transported_bank(sid,c):
 """Transport the entire source bank; resolve zero-boundary collisions.

 Neither residual nor outcome is an input: controlled decision pairs share
 exactly the same mathematical alternatives, not just the same option count.
 """
 a=source_matrix(sid);c0=a[0,2]/a[0,0];target=c-a[0,1]/a[0,0]*y
 values=[];seen=set()
 for option in CASES[sid][':question/answer-fields'][0][':answer-field/choices']:
  value=option[':answer/value'];kind=option[':answer/type'][':db/ident']
  if value=='No solution':values.append((kind,value));continue
  v=matrices(value)[1];old=v[0];k=old.subs(y,0)
  first=sp.expand(old-k+(k*c/c0 if c0 else k+c));second=v[1]
  # A zero intercept may merge sign-error options. Keep the first occurrence,
  # then use a nearby distinct intercept for each duplicate. Reserve the true
  # family so a replacement cannot preempt a later source-derived occurrence.
  pair=(first,second)
  if pair in seen:
   for delta in [1,-1,2,-2,3,-3,4,-4]:
    candidate=(sp.expand(first+delta),second)
    if candidate not in seen and candidate!=(target,y):pair=candidate;break
   else:raise ValueError('Unable to form a distinct source-profile bank')
  seen.add(pair)
  values.append((kind,value if c==c0 else vector(*pair)))
 if (target,y) not in seen:raise ValueError('Source bank lacks the first-equation solution')
 return values

def extension_solution(a):
 """Source wording with matrices and branch text derived from one instance."""
 p,b,c0,d,e,c1=list(a);s=b/p;c=c0/p;res=c1-d*c
 def mat(rows):return matrix_tex([[tex(v) for v in row] for row in rows],augmented=True)
 initial=mat([[p,b,c0],[d,e,c1]]);normal=mat([[1,s,c],[d,e,c1]]);last=mat([[1,s,c],[0,0,res]])
 steps=[r'M & ='+initial]
 if p!=1:steps[0]+=r' & {R}_{1} & :='+tex(1/p)+r'{R}_{1}';steps.append(r' & \sim'+normal)
 op=(r'-'+tex(d) if d>0 else '+'+tex(-d)) if abs(d)!=1 else ('-' if d>0 else '+')
 steps[-1]+=r' & {R}_{2} & :={R}_{2}'+op+r'{R}_{1}'
 steps.append(r' & \sim'+last+'.')
 equation=tex(sp.Symbol('x')+s*y)
 reduced=r'\left\{\begin{aligned}'+equation+' &='+tex(c)+r' \\ 0x+0y &='+tex(res)+r'.\end{aligned}\right.'
 solution='First, we set up the augmented matrix for the system:\n\n$$\nM='+initial+'\n$$\n\nReducing $M$ to row echelon form, we have\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(steps)+r'\end{aligned}'+'\n$$\n\nThe corresponding system is now\n\n$$\n'+reduced+'\n$$\n\n'
 if res:
  return solution+'However, the final equation $0x+0y='+tex(res)+'$ has no solution. It simplifies to $0='+tex(res)+',$ which is a false statement.\n\nSo, there is no pair $x,y$ that satisfies both equations in the system. Consequently, the overall system has no solution.'
 solved=tex(c-s*y)
 return solution+'Since any pair of numbers $x,y$ is a solution of the final equation $0x+0y=0,$ we can remove this equation from the system. So, our system now consists of a single equation\n\n$$\n'+equation+'='+tex(c)+'.\n$$\n\nThe first variable $(x)$ is the basic variable, and the second variable $(y)$ is the free variable. Solving for the basic variable $(x)$ in terms of the free variable $(y),$ we get $x='+solved+',$ and the general solution is\n\n$$\n'+r'\left\{\begin{aligned}x &='+solved+r' \\ y &=y\end{aligned}\right.'+'\n$$\n\nwhere $y$ is an arbitrary number.\n\nIn vector form, the general solution can be written as\n\n$$\n'+vector(c-s*y)+'.\n$$'

def generate(difficulty='easy',seed=0,template=None,parameters=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 params=parameters or {}
 if set(params)-{'rhs_scale','intercept','residual','second_rhs'}:raise ValueError('Unknown parameter')
 # Only original-parameter source replay preserves a captured outcome. A
 # non-original scale controls the intercept, not the consistency decision.
 if params=={'rhs_scale':1}:return legacy_generate(difficulty,seed,template,params)
 rng=random.Random(seed)
 # Assign the decisive role before selecting numerical/presentation details.
 consistent=rng.choice([False,True])
 eligible=[s for s,q in CASES.items() if q[':question/difficulty'][':db/ident'].endswith('/'+difficulty)]
 sid=template or rng.choice(eligible)
 if sid not in eligible:raise ValueError('Template difficulty mismatch')
 a=source_matrix(sid);c0=a[0,2]/a[0,0]
 if 'rhs_scale' in params:
  t=params['rhs_scale']
  if t not in [-4,-3,-2,-1,1,2,3,4]:raise ValueError('Outside validated finite domain')
  c=c0*t
 else:c=sp.sympify(params.get('intercept',rng.randint(-8,8)))
 if c.is_integer is not True or abs(c)>32:raise ValueError('Intercept must be an integer in [-32,32]')
 res=sp.sympify(params.get('residual',0 if consistent else rng.choice([-6,-5,-4,-3,-2,-1,1,2,3,4,5,6])))
 if 'second_rhs' in params:
  if 'residual' in params:raise ValueError('Specify residual or second_rhs, not both')
  res=sp.sympify(params['second_rhs'])-a[1,0]*c
 if res.is_integer is not True or abs(res)>32:raise ValueError('Residual must be an integer in [-32,32]')
 a[0,2]=a[0,0]*c;a[1,2]=a[1,0]*c+res
 values=transported_bank(sid,c)
 # Key from the instance, rather than from source identity. The same bank is
 # valid for both decisions; identify the matching vector mathematically.
 target=sp.Matrix([c-a[0,1]/a[0,0]*y,y])
 key='No solution' if res else next(v for kind,v in values if kind==':answer.type/math' and matrices(v)[1]==target)
 # Presentation randomness must not depend on whether profile/parameters were
 # sampled or explicitly replayed from generation metadata.
 random.Random(str(seed)+'/bank/'+sid).shuffle(values)
 old=CASES[sid]
 body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',old[':question/problem'],re.S)[1]
 rows=body.split(r'\\');rendered=[]
 for i,row in enumerate(rows):rendered.append(row.split('=')[0]+'='+tex(a[i,2])+('.' if i==1 else ' '))
 prompt=old[':question/problem'].replace(body,r'\\'.join(rendered))
 q={':question/problem':prompt,':question/worked-solution':extension_solution(a),':question/difficulty':':question.difficulty/'+difficulty}
 return record(q,sid,seed,{'intercept':int(c),'residual':int(res)},values,key)

def batch(difficulty,count,seed=0):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 seen=set();out=[]
 for i in range(max(100,count*20)):
  r=generate(difficulty,seed+i*104729)
  fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:seen.add(fp);out.append(r)
  if len(out)==count:return out
 raise ValueError('Requested batch exceeds the available distinct sample')
def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\nWorked solution\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=5);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--output');a=p.parse_args()
 if a.count<1:p.error('--count must be positive')
 records=batch(a.difficulty,a.count,a.seed);rendered=json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records)
 Path(a.output).write_text(rendered+'\n') if a.output else print(rendered)
