#!/usr/bin/env python3
"""Identity matrix multiplication, easy; local deterministic previews only."""
import argparse,copy,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts/question_capture'))
from math_format import checked_math_content,normalize_prose,normalize_tex,matrix_tex
ID=17592186100875; VERSION='identity-matrix-1'; HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text());KP=SOURCE['record'];QS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
SUPPORTED=('easy',);EXCLUDED=('q-13763',)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,default=str).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),digest(v)))
def matrix(text):
 t=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)
 if not t:raise ValueError('matrix missing')
 return s.Matrix([[s.Integer(x.strip()) for x in row.split('&')] for row in t[1].split(r'\\')])
def tex(m):return matrix_tex([[str(x) for x in m.row(i)] for i in range(m.rows)],augmented=False)
def original(k):return matrix(QS[k][':question/problem'])
def profile(k,m):
 n=m.rows;z=s.zeros(n);a,b,c,d=list(m)[:4];undef='The product is undefined'
 if k=='q-13762':return [undef,s.diag(*m.diagonal()),-m,z,m]
 if k=='q-13763':return [undef,z,s.eye(n),m,-m]
 if k=='q-130243':return [z,s.Matrix([[b,a],[d,c]]),s.Matrix([[c,d],[a,b]]),m,s.ones(n)]
 if k=='q-75472':return [s.Matrix([[-a,b],[-a,b]]),m,-m,s.Matrix([[-a,b],[b,-a]]),s.Matrix([[b,a],[b,a]])]
 if k=='q-75473':return [m,s.Matrix([[-a,b],[c,-d]]),s.Matrix([[d,b],[-c,a]]),s.Matrix([[b,a],[c,d]]),s.Matrix([[-d,b],[-c,-a]])]
 if k=='q-75479':return [-m,s.Matrix([[c,d],[-a,-b]]),m,s.Matrix([[-a,-b],[c,d]]),s.Matrix([[-a,-b],[d,c]])]
 if k=='q-75474':
  v=list(m);v[0],v[6]=-v[6],v[0];v[1],v[7]=v[7],v[1]
  return [m,s.Matrix(3,3,v),s.Matrix([list(m.row(0))]*3),m[:,[1,0,2]],m[[2,1,0],:]]
 return None

def task(q):
 # Ignore label, side, field form, seed and bank: the supplied matrix is the task.
 m=matrix(q[':question/problem']);return digest([m.rows,m.cols,list(m),'identity-product'])
@checked_math_content
def generate(level='easy',seed=0,template=None,parameters=None,replay=False):
 if level not in SUPPORTED:raise ValueError('unsupported band: '+level)
 rng=random.Random(seed);k=template or rng.choice([x for x in QS if x not in EXCLUDED])
 if k in EXCLUDED and not replay:raise ValueError('unrated incomplete source; evidence replay only')
 old=QS[k];m=original(k)
 if parameters is not None:m=s.Matrix(parameters)
 elif not replay:
  n=m.rows
  for _ in range(200):
   m=s.Matrix(n,n,[rng.randint(-9,9) for _ in range(n*n)])
   if k=='q-75472':
    a=-rng.randint(1,9);b=rng.randint(1,9);m=s.Matrix([[a,b],[b,a]])
   if k=='q-75473':m=s.Matrix([[-rng.randint(1,9),0],[-rng.randint(1,9),-rng.randint(1,9)]])
   if k=='q-75479':
    a=rng.randint(1,9);m=s.Matrix([[a,-a],[0,rng.randint(1,9)]])
   bank=profile(k,m)
   if bank is None or len({str(x) for x in bank})==5:break
  else:raise ValueError('bounded bank search exhausted')
 assert m.shape==original(k).shape
 assert all(v.is_Integer and -9<=v<=9 for v in m)
 if k=='q-75472':assert m[0,0]==m[1,1]<0 and m[0,1]==m[1,0]>0
 if k=='q-75473':assert m[0,1]==0 and all(m[i,j]<0 for i,j in ((0,0),(1,0),(1,1)))
 if k=='q-75479':assert m[0,0]>0 and m[0,1]==-m[0,0] and m[1,0]==0 and m[1,1]>0
 bank=profile(k,m);q={}
 for a in (':question/problem',':question/worked-solution'):
  if a in old:q[a]=re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}',lambda _:tex(m),old[a],flags=re.S)
 if ':question/worked-solution' not in q:
  q[':question/worked-solution']='Any matrix, when multiplied by an identity matrix, remains unchanged (assuming that the multiplication is well defined).\n\nThe matrices have compatible dimensions. Therefore, $A I_3=A='+tex(m)+'$.'
 for a in (':question/problem',':question/worked-solution'):q[a]=normalize_prose(q[a])
 fp=task(q);qid=uid([VERSION,k,fp]);q[':question/id']=qid;q[':question/difficulty']=':question.difficulty/easy';fields=[]
 if bank is not None:
  if len({str(x) for x in bank})!=5:raise ValueError('choice collision')
  fid=uid([qid,'selection']);choices=[]
  for value in bank:
   av=tex(value) if isinstance(value,s.MatrixBase) else value
   choices.append({':answer/id':uid([fid,av]),':answer/type':':answer.type/math' if isinstance(value,s.MatrixBase) else ':answer.type/text',':answer/value':av})
  correct=[a for a in choices if a[':answer/value']==tex(m)];assert len(correct)==1
  fields=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct[0][':answer/id']]}]
 else:
  for i,value in enumerate(m):
   key='field-'+str(i+1);fid=uid([qid,key]);a={':answer/id':uid([fid,str(value)]),':answer/type':':answer.type/math',':answer/value':str(value)}
   fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/blank',':answer-field/choices':[a],':answer-field/correct':[':answer/id',a[':answer/id']]})
 q[':question/answer-fields']=fields
 return {'knowledge_point':{'db_id':ID,'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':k,'profile':k if bank is not None else None,'seed':seed,'parameters':[list(map(int,m.row(i))) for i in range(m.rows)],'source_basis':SOURCE['basis'],'source_question':k,'lineage':SOURCE['lineage'],'sympy':s.__version__,'eligible_for_learning':k not in EXCLUDED,'task_fingerprint':fp}}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--template');p.add_argument('--output',type=Path);p.add_argument('--count',type=int);p.add_argument('--format',choices=('json','markdown'),default='json');a=p.parse_args()
 if a.count is None:records=[generate(a.difficulty,a.seed,a.template)]
 else:
  if not 0<=a.count<=100:raise ValueError('bounded batch size is 0..100')
  if a.difficulty not in SUPPORTED:raise ValueError('unsupported difficulty: '+a.difficulty)
  seen={task(q) for q in QS.values()};seen.add(digest([3,3,[2,3,-1,5,2,7,0,4,6],'identity-product']))
  records=[]
  for offset in range(1000):
   if len(records)==a.count:break
   r=generate(a.difficulty,a.seed+offset,a.template);fp=task(r['question'])
   if fp not in seen:records.append(r);seen.add(fp)
  if len(records)!=a.count:raise ValueError('finite bounded sampling limit: '+str(len(records))+' distinct records; requested '+str(a.count))
 if a.format=='json':text=json.dumps(records if a.count is not None else records[0],indent=2)
 else:text='\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']+'\n\n'+json.dumps(r['question'][':question/answer-fields'],indent=2) for r in records)
 a.output.write_text(text+'\n') if a.output else print(text)
