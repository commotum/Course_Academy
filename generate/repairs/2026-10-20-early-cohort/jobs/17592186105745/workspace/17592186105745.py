"""Singular 2x2 systems: source replay and bank-first signed-column practice."""
import argparse,copy,hashlib,json,random,re,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186105745
KP_UUID='97cd9132-458b-5234-a3d2-22b633acb74c'
GENERATOR_UUID=str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/generator/'+KP_UUID))
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
CASES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
SUPPORTED_LEVELS=('easy','moderate')
y=sp.Symbol('y')
VERSION='bank-first-v2'
SCALES=(-4,-3,-2,-1,1,2,3,4)
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
def transform(text,t,solution=False):
 if t==1:return text
 held=[]
 def hold(s):held.append(s);return '@@H'+str(len(held)-1)+'@@'
 def mat(m):
  rows=m[1].split(r'\\');n=len(rows[0].split('&'));out=[]
  for row in rows:
   entries=row.split('&')
   for j,e in enumerate(entries):
    if n==3 and j==2:entries[j]=' '+tex(number(e)*t)+' '
    elif n==1 and len(rows)==2 and j==0:entries[j]=' '+scale_value(e,t)+' '
   out.append('&'.join(entries))
  return hold(r'\begin{bmatrix}'+r'\\'.join(out)+r'\end{bmatrix}')
 text=re.sub(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',mat,text,flags=re.S)
 def angle(m):
  vals=m[1].replace(r'\,','').split(',');return hold('⟨'+','.join(scale_value(v,t) for v in vals)+'⟩')
 text=re.sub('⟨([^⟩]+)⟩',angle,text)
 if solution:
  # Every occurrence of the scalar system RHS and solved basic variable.
  text=re.sub(r'(x[+\-0-9y ]*\s*&?=)([+\-0-9y ]+)',lambda m:m[1]+scale_value(m[2],t),text)
 for i,h in enumerate(held):text=text.replace('@@H'+str(i)+'@@',h)
 return text

def column_transform(text,u,t,solution=False):
 """Apply y-column sign and RHS scale to the captured instructional stages."""
 if u==t==1:return text
 held=[]
 def hold(s):held.append(s);return '@@COLUMN'+str(len(held)-1)+'@@'
 def affine(s):
  z=number(s)
  return tex(z.subs(y,0)*t+sp.diff(z,y)*u*y)
 def mat(m):
  rows=m[1].split(r'\\');n=len(rows[0].split('&'));out=[]
  for row in rows:
   entries=row.split('&')
   if n==3:
    entries[1]=' '+tex(number(entries[1])*u)+' '
    entries[2]=' '+tex(number(entries[2])*t)+' '
   elif n==1 and len(rows)==2 and not number(entries[0]).has(sp.Symbol('x')):
    entries[0]=' '+(affine(entries[0]) if number(entries[0])!=y else entries[0])+' '
   out.append('&'.join(entries))
  return hold(r'\begin{bmatrix}'+r'\\'.join(out)+r'\end{bmatrix}')
 text=re.sub(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',mat,text,flags=re.S)
 text=re.sub('⟨([^⟩]+)⟩',lambda m:hold('⟨'+','.join(affine(v) if number(v)!=y else v for v in m[1].replace(r'\,','').split(','))+'⟩'),text)
 if solution:
  def equation(m):
   left=number(m[1]);right=number(m[2])
   return tex(left.subs(y,u*y))+(' &=' if '&' in m[0] else '=')+tex(right.subs(y,0)*t+sp.diff(right,y)*u*y)
  text=re.sub(r'(?<![0-9A-Za-z])(x(?:\s*[+\-]\s*\d*y)?)\s*&?=\s*([+\-\d y]+)',equation,text)
 for i,h in enumerate(held):text=text.replace('@@COLUMN'+str(i)+'@@',h)
 return text

def field_source(q):
 # q-42156 has an unkeyed duplicate capture; the keyed bank is authoritative.
 return next(f for f in q[':question/answer-fields'] if ':answer-field/correct' in f)

def practice_values(old,bank):
 f=field_source(old);key=f[':answer-field/correct'][':answer/value']
 a=matrices(old[':question/problem'])[0]
 is_ref='then find' not in old[':question/problem'] and 'reduce' in old[':question/problem']
 out=[]
 for u,t in bank:
  b=a[0,1]/a[0,0]*u;c=a[0,2]/a[0,0]*t
  if is_ref:
   out.append(r'M∼\begin{bmatrix}1 & '+tex(b)+' & '+tex(c)+r' \\ 0 & 0 & 0\end{bmatrix}')
  else:
   # Preserve the profile's observed angle/vector wrapper, but give all five
   # candidates the same shape. Each is a possible general solution.
   out.append(column_transform(key,u,t))
 return out

def fingerprint(q):
 a=(matrices(q[':question/problem']) or matrices(q[':question/worked-solution']))[0]
 # Normalized supplied equation and requested operation. Row scales and order add no distinct task.
 r=next(i for i in range(2) if a[i,0]!=0);bc=[str(a[r,j]/a[r,0]) for j in (1,2)]
 role='ref' if 'then find' not in q[':question/problem'] and 'reduce' in q[':question/problem'] else ('solve-ref' if a[1,:]==sp.zeros(1,3) else 'reduce-solve')
 return digest([role,bc])
def generate(difficulty='moderate',seed=0,template=None,parameters=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 rng=random.Random(seed);eligible=[s for s,q in CASES.items() if q[':question/difficulty'][':db/ident'].endswith('/'+difficulty)]
 sid=template or rng.choice(eligible)
 if sid not in eligible:raise ValueError('Template difficulty mismatch')
 p=dict(parameters or {});old=CASES[sid];f=field_source(old)
 profile=p.get('bank_profile','compatible-five')
 if profile not in ('source','compatible-five'):raise ValueError('Unknown bank profile')
 domain=[(u,t) for u in (-1,1) for t in SCALES]
 # Independent streams prevent the first bank draw from revealing the target draw.
 brng=random.Random(digest(['bank',p.get('bank_seed',seed)]));bank=brng.sample(domain,5)
 if profile=='source':
  u=p.get('column_scale',1);t=p.get('rhs_scale',1)
  if u!=1 or t!=1:raise ValueError('Source replay requires original parameters')
  values=[a[':answer/value'] for a in f[':answer-field/choices']]
  target=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
 elif 'bank_pairs' in p:
  bank=[tuple(v) for v in p['bank_pairs']]
  if len(bank)!=5 or len(set(bank))!=5 or any(v not in domain for v in bank):raise ValueError('Invalid bank pairs')
  target=p['target_index']
  if type(target)!=int or not 0<=target<5:raise ValueError('target_index must be 0..4')
  u,t=bank[target];values=practice_values(old,bank)
 elif 'rhs_scale' in p or 'column_scale' in p:
  u=p.get('column_scale',1);t=p.get('rhs_scale',1)
  if (u,t) not in domain:raise ValueError('Outside validated finite domain')
  bank=brng.sample([v for v in domain if v!=(u,t)],4)+[(u,t)]
  brng.shuffle(bank);target=bank.index((u,t));values=practice_values(old,bank)
 else:
  target=p.get('target_index',rng.randrange(5))
  if type(target)!=int or not 0<=target<5:raise ValueError('target_index must be 0..4')
  u,t=bank[target];values=practice_values(old,bank)
 q={':question/problem':column_transform(old[':question/problem'],u,t),':question/worked-solution':column_transform(old[':question/worked-solution'],u,t,True),':question/difficulty':':question.difficulty/'+difficulty}
 fp=fingerprint(q);qid=uid('question/'+fp+'/'+digest(values));q[':question/id']=qid;fid=uid(qid+'/selection');choices=[]
 for i,val in enumerate(values):
  aid=uid(fid+'/'+str(i)+'/'+val);choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':val})
  if i==target:correct=aid
 q[':question/answer-fields']=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE[':knowledge-point/title']},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'template':sid,'profile':sid+'/'+profile,'seed':seed,'parameters':{'rhs_scale':t,'column_scale':u,'bank_profile':profile,'bank_seed':p.get('bank_seed',seed),'bank_pairs':[list(v) for v in bank] if profile!='source' else [],'target_index':target},'mathematical_fingerprint':fp,'source_question_id':old[':question/id'],'sympy_version':sp.__version__}}
def batch(difficulty,count,seed=0):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 rng=random.Random(seed);seen=set();out=[]
 for _ in range(2000):
  r=generate(difficulty,rng.randrange(2**63))
  fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:seen.add(fp);out.append(r)
  if len(out)==count:return out
 raise ValueError('Requested count exceeds sampled distinct finite practice family')
def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\nWorked solution\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='moderate');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=5);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--output');a=p.parse_args()
 if a.count<1:p.error('--count must be positive')
 records=batch(a.difficulty,a.count,a.seed);rendered=json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records)
 Path(a.output).write_text(rendered+'\n') if a.output else print(rendered)
