#!/usr/bin/env python3
"""Adding Square Matrices: source-backed easy 2x2 integer addition."""
import argparse,copy,hashlib,json,random,re,uuid
from pathlib import Path
try:
 import sympy as sp
except ModuleNotFoundError:
 import os,sys
 executable=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if __name__=='__main__':os.execv(str(executable),[str(executable),str(Path(__file__).resolve()),*sys.argv[1:]])
 raise
HERE=Path(__file__).with_suffix('');S=json.loads((HERE/'source.json').read_text())
KP_ID=17592186054648;KP_UUID=S['record'][':knowledge-point/id'];VERSION='1.0.0'
SOURCES={q[':question/math-academy-id']:q for q in S['record'][':knowledge-point/questions']};TEMPLATES=tuple(SOURCES)
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def parse(text):return [[int(x.strip()) for x in row.split('&')] for row in text.split(r'\\')]
def matrices(text):return [parse(m) for m in MATRIX.findall(text)]
def flat(m):return [x for row in m for x in row]
def latex(v):return r'\begin{bmatrix}'+' & '.join(map(str,v[:2]))+r' \\ '+' & '.join(map(str,v[2:]))+r'\end{bmatrix}'
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(parent,x):return str(uuid.uuid5(uuid.UUID(parent),str(x)))
def original(t):
 a,b=matrices(SOURCES[t][':question/problem']);return {'a':flat(a),'b':flat(b)}
def addition(p):return [int(x) for x in sp.Matrix(p['a'])+sp.Matrix(p['b'])]
def bank(t,p):
 a,b=p['a'],p['b'];c=addition(p)
 def changed(index,value):
  d=c.copy();d[index]=value;return d
 if t=='q-101':return [[c[0],-(a[1]-b[1]),c[2],-abs(a[3])-abs(b[3])],[c[0],a[1]-b[1],a[2],c[3]],[-(a[0]-b[0]),-(a[1]-b[1]),c[2],c[3]],c,changed(3,-abs(a[3])-abs(b[3]))]
 if t=='q-11440':return [c,[a[1],a[0],c[2],c[3]],[a[1]]*4,[-c[0],c[1],c[2],-c[3]],[c[0]]*4]
 if t=='q-100':return [[a[0]-b[0],b[1]-a[1],c[2],c[3]],changed(1,b[1]-a[1]),c,[c[1]]*4,changed(0,-c[0])]
 if t=='q-125630':return [changed(2,c[1]),changed(1,b[3]),c,changed(2,c[0]),changed(0,c[0]+1)]
 if t=='q-125631':return [changed(0,a[3]),changed(1,-c[1]),[-c[0],c[1],-c[2],c[3]],c,changed(1,a[1])]
 return None
# Counts of negative first operands enclosed in parentheses in source solutions.
WRAP={'q-100':{1},'q-11440':set(),'q-125630':{1,3},'q-125631':set(),'q-319591':set(),'q-101':set()}
def fingerprint(q):
 ms=matrices(q[':question/problem'])
 if len(ms)!=2:ms=[parse(m) for m in MATRIX.findall(q.get(':question/worked-solution',''))[:2]]
 # Addition is commutative: operand exchange is not a distinct exercise.
 return digest(sorted(ms)) if len(ms)==2 else digest(q[':question/problem'])
def generate(difficulty='easy',seed=0,template=None,parameters=None,replay=False):
 if difficulty!='easy':raise ValueError('Unsupported band; no rated or instructional moderate/hard source backbone')
 rng=random.Random(seed);t=template or rng.choice(TEMPLATES);source=SOURCES[t]
 if parameters is None:
  for _ in range(1000):
   p={'a':[rng.randint(-12,12) for _ in range(4)],'b':[rng.randint(-12,12) for _ in range(4)]};values=bank(t,p)
   if values is None or len({tuple(v) for v in values})==5:break
  else:raise ValueError('Finite rejection bound reached')
 else:p=copy.deepcopy(parameters)
 assert all(len(p[k])==4 and all(type(x)==int and -12<=x<=12 for x in p[k]) for k in ('a','b'))
 c=addition(p);values=bank(t,p)
 if values is not None:assert len({tuple(v) for v in values})==5
 sub=iter((latex(p['a']),latex(p['b'])));prompt=MATRIX.sub(lambda _:next(sub),source[':question/problem'])
 calc=[]
 for i,(a,b) in enumerate(zip(p['a'],p['b'])):
  aa='('+str(a)+')' if a<0 and i in WRAP[t] else str(a)
  bb='('+str(b)+')' if b<0 else str(b);calc.append(aa+'+'+bb)
 if ':question/worked-solution' in source:
  sub=iter((latex(p['a']),latex(p['b']),latex(calc),latex(c)))
  solution=MATRIX.sub(lambda _:next(sub),source[':question/worked-solution'])
 else:
  solution='We add the corresponding entries:\n\n$$\n'+r'\begin{aligned}'+latex(p['a'])+'+'+latex(p['b'])+' & ='+latex(calc)+r' \\  & ='+latex(c)+r'\end{aligned}'+'\n$$'
 ident=uid(KP_UUID,VERSION+':'+digest([t,p,values]));fields=[]
 for i in range(1 if values is not None else 4):
  key='selection' if values is not None else 'field-'+str(i+1);fid=uid(ident,key)
  strings=[latex(v) for v in values] if values is not None else [str(c[i])]
  answers=[{':answer/id':uid(fid,x),':answer/type':':answer.type/math',':answer/value':x} for x in strings]
  correct=latex(c) if values is not None else str(c[i])
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+('radio' if values is not None else 'blank'),':answer-field/choices':answers,':answer-field/correct':[':answer/id',uid(fid,correct)]})
 question={':question/id':ident,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':fields}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':S['record'][':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'seed':seed,'template':t,'profile':t if values is not None else None,'parameters':p,'replay':replay,'source':source[':db/id'],'source_basis':S['basis'],'dependency_versions':{'sympy':sp.__version__},'mathematical_fingerprint':fingerprint(question),'assets':[]}}
def batch(difficulty,count,seed):
 out=[];seen=set()
 for k in range(count*100+1):
  if len(out)==count:return out
  r=generate(difficulty,seed+k,TEMPLATES[k%len(TEMPLATES)]);fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:out.append(r);seen.add(fp)
 raise ValueError('Finite batch search bound reached')
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n\n'.join(f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']) for f in q[':question/answer-fields'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',default='easy');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--template');a.add_argument('--format',choices=['json','markdown'],default='json');args=a.parse_args()
 records=[generate(args.difficulty,args.seed,args.template)] if args.template else batch(args.difficulty,args.count,args.seed)
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
