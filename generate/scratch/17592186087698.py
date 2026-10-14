#!/usr/bin/env python3
"""Identifying Other Matrices: source-faithful easy families, no plots.

CLI emits local review records only. Distinctness ignores labels, entries, seeds
and choice order when they do not change the assessed matrix properties.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
try:
 import sympy as sp
except ModuleNotFoundError:
 import os, sys
 interpreter=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if not interpreter.is_file() or Path(sys.executable).resolve()==interpreter.resolve():
  raise RuntimeError('Generator requires SymPy in the repository virtual environment')
 os.execv(str(interpreter),[str(interpreter),str(Path(__file__).resolve()),*sys.argv[1:]])
KP_ID=17592186087698
KP_UUID='7b6ddadb-471a-5195-a0f5-fd44bdc8f780'
TITLE='Identifying Other Matrices'
VERSION='matrix-identification-v1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
TEMPLATES={'row':'q-11563','diagonal':'q-126293','other':'q-7830','rows':'q-68751','columns':'q-126287'}
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def identifier(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),x))
def parse(text):
 return [[[sp.sympify(re.sub(r'\\sqrt\{(\d+)\}',r'sqrt(\1)',v.strip())) for v in row.split('&')] for row in m[1].split(r'\\')] for m in MATRIX.finditer(text)]
def matrix(m):return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(str(v) for v in row) for row in m)+r'\end{bmatrix}'
def properties(m):
 r,c=len(m),len(m[0]);assert all(len(row)==c for row in m)
 a=sp.Matrix(m);zero=a.is_zero_matrix;diagonal=r==c and a.is_diagonal();identity=r==c and a==sp.eye(r)
 return (r,c,bool(zero),bool(diagonal),bool(identity))
def fingerprint(q):
 p=q[':question/problem'];ms=parse(p)
 if 'are row vectors' in p:task=('rows',sorted(properties(m)[:2] for m in ms))
 elif 'are column vectors' in p:task=('columns',sorted(properties(m)[:2] for m in ms))
 else:task=('classify',properties(ms[0]))
 return digest(task)
def parameters(template):return {'matrices':[[[str(v) for v in row] for row in m] for m in parse(ORIGINALS[TEMPLATES[template]][':question/problem'])]}
def validate_parameters(t,p):
 assert set(p)=={'matrices'}
 ms=p['matrices'];assert len(ms)==(3 if t in ('rows','columns') else 1)
 props=[]
 for m in ms:
  assert m and m[0] and all(len(row)==len(m[0]) for row in m)
  assert all(sp.sympify(x).is_integer and abs(sp.sympify(x))<=12 for row in m for x in row)
  r,c,z,d,i=properties(m);assert not z;assert 1<=r<=6 and 1<=c<=6 and r*c>1;props.append((r,c,z,d,i))
 if t=='row':assert props[0][0]==1 and props[0][1]>=2 and not props[0][2]
 elif t=='diagonal':assert props[0][3] and not props[0][2] and not props[0][4]
 elif t=='other':assert props[0][0]>1 and props[0][1]>1 and props[0][0]!=props[0][1] and not props[0][2]
 else:assert sorted('row' if r==1 else 'col' if c==1 else 'general' for r,c,*_ in props)==['col','general','row']
 return ms

def sample(t,rng):
 def dense(r,c):
  m=[[rng.randint(-5,5) for _ in range(c)] for _ in range(r)]
  if not any(v for row in m for v in row):m[0][0]=1
  return m
 if t=='row':ms=[dense(1,rng.randint(2,6))]
 elif t=='diagonal':
  n=rng.randint(2,6);ds=[rng.choice([-4,-3,-2,-1,1,2,3,4]) for _ in range(n)]
  if all(v==1 for v in ds):ds[0]=-1
  ms=[[[ds[i] if i==j else 0 for j in range(n)] for i in range(n)]]
 elif t=='other':
  r,c=rng.sample(range(2,7),2);ms=[dense(r,c)]
 else:
  ms=[dense(1,rng.randint(2,6)),dense(rng.randint(2,6),1),dense(rng.randint(2,5),rng.randint(2,5))];rng.shuffle(ms)
 return {'matrices':ms}

def vector_solution(ms,kind):
 lines=[];good=[]
 for name,m in zip('ABC',ms):
  r,c,*_=properties(m);v=kind+' vector'
  if (r==1 if kind=='row' else c==1):
   lines.append(f'- ${name}$ is a {v} since it has only one '+('row.' if kind=='row' else 'column.'));good.append(name)
  elif kind=='row' and c==1:lines.append(f"- ${name}$ is *not* a row vector. It has only one column (and ${r}$ rows), so it's a column vector.")
  elif kind=='column' and r==1:lines.append(f"- ${name}$ is *not* a column vector. It has only one row (and ${c}$ columns), so it's a row vector.")
  else:lines.append(f'- ${name}$ is *not* a {v}, since it has more than $1$ '+('row' if kind=='row' else 'column')+f' (it has ${r if kind=="row" else c}$ '+('rows' if kind=='row' else 'columns')+').')
 return '\n\n'.join(lines)+f'\n\nTherefore, only ${good[0]}$ is a {kind} vector.'

def generate(level='easy',seed=0,template=None,parameters=None):
 if level!='easy':raise ValueError('Unsupported difficulty: no same-backbone moderate/hard evidence')
 rng=random.Random(seed);t=template or rng.choice(list(TEMPLATES));assert t in TEMPLATES
 p=parameters if parameters is not None else sample(t,rng);ms=validate_parameters(t,p)
 source=ORIGINALS[TEMPLATES[t]];iterator=iter(ms)
 problem=MATRIX.sub(lambda _:matrix(next(iterator)),source[':question/problem'])
 solution=vector_solution(ms,'row' if t=='rows' else 'column') if t in ('rows','columns') else source[':question/worked-solution']
 fields=[];banks=[]
 for f in sorted(source[':question/answer-fields'],key=lambda f:f[':answer-field/key']):
  vals=[a[':answer/value'] for a in f[':answer-field/choices']]
  key=f[':answer-field/key'];typ=f[':answer-field/type'][':db/ident']
  good=str((len(ms['ABC'.index(key)])==1) if t=='rows' else (len(ms['ABC'.index(key)][0])==1)).lower() if t in ('rows','columns') else f[':answer-field/correct'][':answer/value']
  banks.append((key,typ,sorted(vals),good))
 identity=digest([VERSION,problem,solution,banks]);qid=identifier(identity)
 for key,typ,vals,good in banks:
  fid=identifier(identity+'/field/'+key);answers=[{':answer/id':identifier(fid+'/'+val),':answer/type':':answer.type/text',':answer/value':val} for val in vals]
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':typ,':answer-field/choices':answers,':answer-field/correct':[':answer/id',identifier(fid+'/'+good)]})
 q={':question/id':qid,':question/difficulty':':question.difficulty/easy',':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'template':t,'profile':TEMPLATES[t],'seed':seed,'parameters':p,'content_fingerprint':identity,'mathematical_fingerprint':fingerprint(q),'source_basis':SOURCE['basis'],'source_question':TEMPLATES[t],'eligible_for_learning':True,'dependencies':{'sympy':sp.__version__}}}

def batch(level,count,seed):
 result=[];seen=set()
 for n in range(max(1000,count*100)):
  t=list(TEMPLATES)[n%len(TEMPLATES)];r=generate(level,seed+n,t);fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:result.append(r);seen.add(fp)
  if len(result)==count:return result
 raise ValueError('Bounded distinct variant domain exhausted; shortage remains')
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',default='easy');a.add_argument('--count',type=int,default=5);a.add_argument('--seed',type=int,default=0);a.add_argument('--template',choices=list(TEMPLATES));a.add_argument('--format',choices=['json','markdown'],default='json');args=a.parse_args()
 records=[generate(args.difficulty,args.seed,args.template)] if args.template else batch(args.difficulty,args.count,args.seed)
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records))
