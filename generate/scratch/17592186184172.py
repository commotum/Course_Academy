#!/usr/bin/env python3
"""Seeded, source-faithful invertible-matrix/rank-nullity questions.

Moderate count templates: uniform integer dilation of n, rank, nullity,
claimed dimensions and counts (k=1..3). The theorem's zero stays fixed.
Vector templates: invertible diagonal coordinate map with entries 1..3,
applied to every prompt/solution vector. A subspace RREF fingerprint rejects
basis-rescalings that do not change the task. Field layouts/banks stay fixed.
"""
import argparse,copy,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix('')
RAW=json.loads((HERE/'source.json').read_text())
KP=RAW['record'];KP_ID=17592186184172;KP_UUID=KP[':knowledge-point/id']
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='1.0.0'
Q={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
SUPPORTED_LEVELS=('moderate','hard')
VECTOR=re.compile(r'\\begin\{(aligned|bmatrix)\}((?:(?!\\begin\{).)*?)\\end\{\1\}',re.S)
SYMBOLS={s:sp.Symbol(s) for s in ['a','b','x1','x2','x3']}

def vector_blocks(text):
 for m in VECTOR.finditer(text):
  cells=[c.strip() for c in m[2].split(r'\\')]
  if len(cells)<2 or any('&' in c or '\\text' in c or '=' in c for c in cells):continue
  yield m,cells

def scalar(cell):
 cell=re.sub(r'\{x\}_\{(\d)\}',r'x\1',cell)
 if re.fullmatch(r'-?\d+',cell):return sp.Integer(cell)
 m=re.fullmatch(r'(-?\d*)(a|b|x[123])',cell)
 if not m:raise ValueError('Unparsed vector entry: '+cell)
 a=m[1];return sp.Integer(-1 if a=='-' else 1 if not a else int(a))*SYMBOLS[m[2]]

def transform_vectors(text,diag):
 if all(d==1 for d in diag):return text
 def repl(m):
  cells=[c.strip() for c in m[2].split(r'\\')]
  if len(cells)!=len(diag) or any('&' in c or '\\text' in c or '=' in c for c in cells):return m[0]
  result=[]
  for cell,d in zip(cells,diag):
   val=scalar(cell)
   if d==1 or val==0:result.append(cell);continue
   match=re.fullmatch(r'(-?\d*)(.*)',cell);coeff=match[1];tail=match[2]
   if not tail:result.append(str(int(cell)*d))
   else:
    coeff=-1 if coeff=='-' else 1 if not coeff else int(coeff)
    new=coeff*d;result.append(('' if new==1 else '-' if new==-1 else str(new))+tail)
  return r'\begin{'+m[1]+'}'+r' \\ '.join(result)+r'\end{'+m[1]+'}'
 return VECTOR.sub(repl,text)

def is_vector(key):return bool(list(vector_blocks(Q[key][':question/problem'])))
def level_of(key):return Q[key][':question/difficulty'][':db/ident'].split('/')[-1]
def n_of(text):return int(re.search(r'\$(\d+)\s*\\times\s*(\d+)\$',text)[1])

def clean(q):
 r={k:q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
 r[':question/difficulty']=q[':question/difficulty'][':db/ident']
 r[':question/answer-fields']=[]
 for f in sorted(q[':question/answer-fields'],key=lambda x:x[':answer-field/key']):
  r[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':a[':answer/type'][':db/ident'],':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]})
 return copy.deepcopy(r)

def normalize_statement(s):
 return re.sub(r'\s+','',s.replace('**','').replace('$','').replace('\\textrm','\\text').rstrip('.'))

def task_data(q):
 text=q[':question/problem'];n=n_of(text)
 markers=list(re.finditer(r'(?<![A-Z])(?:\*\*)?(I|II|III)\.(?:\*\*)?\s*',text))
 assert [m[1] for m in markers]==['I','II','III']
 prefix=text[:markers[0].start()]
 statements=[text[m.end():markers[i+1].start() if i<2 else len(text)].strip().rstrip('-').strip() for i,m in enumerate(markers)]
 blocks=list(vector_blocks(prefix))
 if blocks:
  cols=[]
  for m,cells in blocks:
   v=sp.Matrix([scalar(c) for c in cells]);syms=sorted(v.free_symbols,key=str)
   cols.extend([v.diff(s) for s in syms] if syms else [v])
  B=sp.Matrix.hstack(*cols);assert B.rows==n
  u=B.rank();r=n-u
  subspace=[list(map(str,row)) for row in B.T.rref()[0].tolist() if any(row)]
  given=['null-space',subspace]
 else:
  m=re.search(r'\$(\d+)\$ (non-pivot|pivot) column',prefix);assert m,prefix
  count=int(m[1]);u=count if m[2]=='non-pivot' else n-count;r=n-u
  given=[m[2]+'-columns',count]
 assert 0<=r<=n
 return {'n':n,'rank':r,'nullity':u,'given':given,'statements':statements}

def fingerprint(q):
 t=task_data(q)
 return json.dumps([t['n'],t['given'],[normalize_statement(s) for s in t['statements']]],sort_keys=True)

def default_parameters(key):return {'diagonal':[1]*n_of(Q[key][':question/problem'])} if is_vector(key) else {'scale':1}

def generate(difficulty,seed=0,template=None,parameters=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty+'; no source evidence for an easy band')
 rng=random.Random(seed);keys=sorted(k for k in Q if level_of(k)==difficulty);key=template or rng.choice(keys)
 if key not in keys:raise ValueError('Template/difficulty mismatch')
 if parameters is None:parameters={'diagonal':[rng.randint(1,3) for _ in range(n_of(Q[key][':question/problem']))]} if is_vector(key) else {'scale':rng.randint(1,3)}
 q=clean(Q[key])
 if is_vector(key):
  d=parameters['diagonal'];assert len(d)==n_of(q[':question/problem']) and all(type(x)==int and 1<=x<=3 for x in d)
  for name in (':question/problem',':question/worked-solution'):q[name]=transform_vectors(q[name],d)
 else:
  k=parameters['scale'];assert type(k)==int and 1<=k<=3
  for name in (':question/problem',':question/worked-solution'):q[name]=re.sub(r'\d+',lambda m:str(int(m[0])*k),q[name])
 bank=json.dumps([(f[':answer-field/key'],f[':answer-field/type'],sorted(a[':answer/value'] for a in f[':answer-field/choices'])) for f in q[':question/answer-fields']],sort_keys=True)
 identity=uuid.uuid5(uuid.UUID(GENERATOR_UUID),fingerprint(q)+bank);q[':question/id']=str(identity)
 for f in q[':question/answer-fields']:
  old=f[':answer-field/correct'][1];f[':answer-field/id']=str(uuid.uuid5(identity,'field:'+f[':answer-field/key']))
  for a in f[':answer-field/choices']:
   original=a[':answer/id'];a[':answer/id']=str(uuid.uuid5(uuid.UUID(f[':answer-field/id']),'answer:'+a[':answer/value']))
   if original==old:f[':answer-field/correct'][1]=a[':answer/id']
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':KP[':knowledge-point/title']},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'template':key,'profile':key,'seed':seed,'parameters':parameters,'source_id':key,'source_basis':RAW['basis'],'python':sys.version.split()[0],'sympy':sp.__version__,'fingerprint':hashlib.sha256(fingerprint(q).encode()).hexdigest()}}

def batch(level,count,seed):
 out=[];used=set();keys=sorted(k for k in Q if level_of(k)==level)
 for i in range(max(count*100,len(keys))):
  r=generate(level,seed+i,keys[i%len(keys)]);fp=fingerprint(r['question'])
  if fp not in used:out.append(r);used.add(fp)
  if len(out)>=count:break
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--difficulty',required=True);p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--template');a=p.parse_args()
 rows=[generate(a.difficulty,a.seed,a.template)] if a.template else batch(a.difficulty,a.count,a.seed)
 print(json.dumps(rows,indent=2))

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':main()
