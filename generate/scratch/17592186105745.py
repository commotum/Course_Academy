"""Singular 2x2 systems: source-faithful RHS scaling, finite signed domain."""
import argparse,copy,hashlib,json,random,re,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186105745
KP_UUID='97cd9132-458b-5234-a3d2-22b633acb74c'
GENERATOR_UUID=str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/generator/'+KP_UUID))
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
CASES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions'] if q[':question/math-academy-id']not in ('q-42156','q-73524')}
SUPPORTED_LEVELS=('easy','moderate')
y=sp.Symbol('y')
VERSION='rhs-scaling-v1'
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
 t=(parameters or {}).get('rhs_scale',rng.choice([-4,-3,-2,-1,1,2,3,4]))
 if t not in [-4,-3,-2,-1,1,2,3,4]:raise ValueError('Outside validated finite domain')
 old=CASES[sid];q={':question/problem':transform(old[':question/problem'],t),':question/worked-solution':transform(old[':question/worked-solution'],t,True),':question/difficulty':':question.difficulty/'+difficulty}
 fp=fingerprint(q);qid=uid('question/'+fp+'/'+sid);q[':question/id']=qid;f=old[':question/answer-fields'][0];fid=uid(qid+'/selection');choices=[]
 for a in f[':answer-field/choices']:
  val=transform(a[':answer/value'],t);aid=uid(fid+'/'+val);choices.append({':answer/id':aid,':answer/type':a[':answer/type'][':db/ident'],':answer/value':val})
  if a[':answer/id']==f[':answer-field/correct'][':answer/id']:correct=aid
 q[':question/answer-fields']=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE[':knowledge-point/title']},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'template':sid,'profile':sid,'seed':seed,'parameters':{'rhs_scale':t},'mathematical_fingerprint':fp,'source_question_id':old[':question/id'],'sympy_version':sp.__version__}}
def batch(difficulty,count,seed=0):
 records=[generate(difficulty,seed,s,{'rhs_scale':t}) for s,q in CASES.items() if q[':question/difficulty'][':db/ident'].endswith('/'+difficulty) for t in [-4,-3,-2,-1,1,2,3,4]]
 random.Random(seed).shuffle(records);seen=set();out=[]
 for r in records:
  fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:seen.add(fp);out.append(r)
 return out[:count]
def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\nWorked solution\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='moderate');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=5);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--output');a=p.parse_args()
 if a.count<1:p.error('--count must be positive')
 records=batch(a.difficulty,a.count,a.seed);rendered=json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records)
 Path(a.output).write_text(rendered+'\n') if a.output else print(rendered)
