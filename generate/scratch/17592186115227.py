#!/usr/bin/env python3
"""Source-backed matrix triple products. Run with the repository .venv Python.

Only observed easy/moderate blank backbones are generated. No speculative radio
banks or hard workloads. Numeric matrix entries are the only variable slots.
"""
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts/question_capture'))
from math_format import matrix_tex, normalize_prose, normalize_tex, checked_math_content
HERE=Path(__file__).with_suffix('')
S=json.loads((HERE/'source.json').read_text())
KP_ID=17592186115227
KP_UUID=S['record'][':knowledge-point/id']
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='matrix-associative-blanks-1.0.0'
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
SOURCES={q[':question/math-academy-id']:q for q in S['record'][':knowledge-point/questions']}
TEMPLATES={k:q for k,q in SOURCES.items() if all(f[':answer-field/type'][':db/ident']==':answer-field.type/blank' for f in q[':question/answer-fields'])}
LEVELS=('easy','moderate')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(ns,label):return str(uuid.uuid5(uuid.UUID(ns),label))
def parse_matrix(body):return sp.Matrix([[sp.sympify(c.strip()) for c in row.split('&')] for row in re.split(r'\\\\',body)])
def matrices(text):return [parse_matrix(m[1]) for m in MATRIX.finditer(text)]
def matrix(m):return matrix_tex([list(m.row(i)) for i in range(m.rows)],augmented=False)
def plain(m):return [[int(m[i,j]) for j in range(m.cols)] for i in range(m.rows)]
def parameters(q):return {k:plain(m) for k,m in zip('ABC',matrices(q[':question/problem']))}
def fingerprint(q):
 # IDs, difficulty, field layout and answer ordering cannot make a new task.
 return digest(parameters(q))
def signed_sum(terms):return ''.join(('+' if i and t>=0 else '')+str(t) for i,t in enumerate(terms))
def factor(n):return '('+str(n)+')' if n<0 else str(n)
def domain(template,p):
 original=parameters(TEMPLATES[template])
 assert set(p)==set('ABC')
 for k in 'ABC':
  assert len(p[k])==len(original[k]) and all(len(row)==len(original[k][0]) for row in p[k])
  assert all(type(v) is int and -7<=v<=7 for row in p[k] for v in row)
 # Keep the observed zero structure in B,C of the three-column blank template.
 if template=='q-320017':assert p['B'][0][2]==p['B'][1][2]==p['C'][2][0]==0

@checked_math_content
def generate(difficulty,seed=0,template=None,parameters=None):
 if difficulty not in LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 rng=random.Random(seed)
 eligible=[k for k,q in TEMPLATES.items() if q[':question/difficulty'][':db/ident'].endswith('/'+difficulty)]
 template=template or rng.choice(eligible)
 if template not in eligible:raise ValueError('Template/difficulty mismatch')
 src=TEMPLATES[template];orig=globals()['parameters'](src)
 p=copy.deepcopy(parameters) if parameters is not None else {k:[[rng.randint(-6,6) for v in row] for row in m] for k,m in orig.items()}
 if parameters is None and template=='q-320017':p['B'][0][2]=p['B'][1][2]=p['C'][2][0]=0
 domain(template,p)
 A,B,C=[sp.Matrix(p[k]) for k in 'ABC'];AB=A*B;BC=B*C;R=AB*C
 left=src[':question/worked-solution'].find('product $AB$')>=0
 first=AB if left else BC
 # Matrix slots in the fixed source solution, retaining source sentence/layout.
 seq=[A,B,first,first,C,R] if left else [B,C,first,A,first,R]
 rendered=[matrix(m) for m in seq]
 if template=='q-320021':
  terms=[int(A[0,j]*B[j,0]) for j in range(B.rows)]
  expr='+'.join(factor(int(A[0,j]))+r'\cdot '+factor(int(B[j,0])) for j in range(B.rows))
  rendered[2:2]=[r'\begin{bmatrix}'+expr+r'\end{bmatrix}',r'\begin{bmatrix}'+signed_sum(terms)+r'\end{bmatrix}']
 if template=='q-319943':
  terms=[int(B[0,j]*C[j,0]) for j in range(C.rows)]
  rendered[2:2]=[r'\begin{bmatrix}'+signed_sum(terms)+r'\end{bmatrix}']
 def replace(text,values):
  assert len(MATRIX.findall(text))==len(values)
  it=iter(values);return MATRIX.sub(lambda _:next(it),text)
 prompt=replace(src[':question/problem'],[matrix(m) for m in (A,B,C)])
 solution=replace(src[':question/worked-solution'],rendered)
 prompt=normalize_prose(prompt);solution=normalize_prose(solution)
 fp=fingerprint({':question/problem':prompt});qid=uid(KP_UUID,'matrix-triple:'+fp)
 fields=[]
 for f in sorted(src[':question/answer-fields'],key=lambda f:f[':answer-field/key']):
  i=int(f[':answer-field/key'].split('-')[-1])-1;value=normalize_tex(str(R[i//R.cols,i%R.cols]));fid=uid(qid,f[':answer-field/key']);aid=uid(fid,'answer:'+value)
  fields.append({':answer-field/id':fid,':answer-field/key':f[':answer-field/key'],':answer-field/type':':answer-field.type/blank',':answer-field/correct':[':answer/id',aid],':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value}]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':S['record'][':knowledge-point/title']},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':template,'profile':None,'parameters':p,'source_basis':S['basis'],'source_question':src[':db/id'],'mathematical_fingerprint':fp,'domain':'Integer entries -7..7; sampled -6..6; fixed source dimensions, all result entries requested. q-320017 retains zero third column of B and last entry of C.','dependencies':{'sympy':sp.__version__},'assets':{}}}

def fresh(difficulty,count,seed=0,excluded=()):
 if difficulty not in LEVELS:raise ValueError('Unsupported difficulty')
 used=set(excluded);out=[]
 for i in range(max(100,count*100)):
  if len(out)>=count:break
  r=generate(difficulty,seed+i);fp=r['generation']['mathematical_fingerprint']
  if fp not in used:out.append(r);used.add(fp)
 if len(out)<count:raise RuntimeError('Bounded sampler could not produce requested count')
 return out

def main():
 a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True,choices=LEVELS);a.add_argument('--count',type=int,default=1);a.add_argument('--seed',type=int,default=0);a.add_argument('--template');a.add_argument('--format',choices=('json','markdown'),default='json');ns=a.parse_args()
 records=[generate(ns.difficulty,ns.seed,ns.template)] if ns.template else fresh(ns.difficulty,ns.count,ns.seed)
 if ns.format=='json':print(json.dumps(records,indent=2))
 else:
  for r in records:print(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'])
if __name__=='__main__':main()
