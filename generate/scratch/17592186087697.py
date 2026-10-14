#!/usr/bin/env python3
"""Source-replayed easy special-square-matrix recognition; bounded structural slots."""
import argparse, json, random, re, uuid
from pathlib import Path
try:
 import sympy as sp
except ModuleNotFoundError:
 import os,sys
 interpreter=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 os.execv(str(interpreter),[str(interpreter),str(Path(__file__).resolve()),*sys.argv[1:]])
KP_ID=17592186087697
KP_UUID='09fa0899-a3d2-584f-8cdd-a471f8cfd16b'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
SUPPORTED_LEVELS=('easy',)
VERSION='1.0.0'
HERE=Path(__file__).with_suffix('')
TEMPLATES=json.loads((HERE/'templates.json').read_text())
PATTERN=r'([A-Z])\s*=\s*\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}'
def arrays(text):
 out={}
 for m in re.finditer(PATTERN,text):
  raw=re.sub(r'\\text\{[^}]*\}','',m[2])
  out[m[1]]=[[v.strip() for v in row.strip().split('&')] for row in raw.split('\\\\')]
 return out

def properties(rows):
 M=sp.Matrix([[sp.Rational(v) for v in row] for row in rows]);square=M.rows==M.cols
 diagonal=square and all(M[i,j]==0 for i in range(M.rows) for j in range(M.cols) if i!=j)
 identity=square and M==sp.eye(M.rows)
 return diagonal,identity

def fingerprint_text(text):
 kind='identity' if 'identity matrices?' in text else 'diagonal'
 # Ignore labels, order, seeds, magnitudes unrelated to this recognition method.
 items=[]
 for rows in arrays(text).values():
  items.append((len(rows),len(rows[0]),tuple(tuple(0 if sp.Rational(v)==0 else 1 if sp.Rational(v)==1 else 2 for v in row) for row in rows)))
 return json.dumps([kind,sorted(items)],separators=(',',':'))

def generate(difficulty='easy',seed=0,template=None,parameters=None,profile=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Only easy is certified; moderate/hard unsupported')
 rng=random.Random(seed);template=template or rng.choice(list(TEMPLATES));t=TEMPLATES[template]
 if profile not in (None,template):raise ValueError('Unknown checkbox profile')
 if parameters is None:
  matrices=[];ws=[]
  for original,role in zip(t['parameters']['matrices'],t['roles']):
   n=rng.randint(2,4);r,c=n,n
   if role=='rectangular':
    r,c=rng.choice([(a,b) for a in range(2,5) for b in range(2,5) if a!=b])
   rows=[['0']*c for _ in range(r)]
   if role=='identity':
    for i in range(n):rows[i][i]='1'
   elif role=='diagonal':
    for i in range(n):rows[i][i]=rng.choice(['0','1','2','3','-2'])
    if all(rows[i][i]=='1' for i in range(n)):rows[0][0]='2'
   elif role=='offdiagonal':
    for i in range(n):rows[i][i]=rng.choice(['0','1','2','3','-2'])
    count=sum(sp.Rational(v)!=0 for i,row in enumerate(original) for j,v in enumerate(row) if i!=j)
    cells=rng.sample([(i,j) for i in range(n) for j in range(n) if i!=j],count)
    for i,j in cells:rows[i][j]=rng.choice(['1','2','-1','5','7'])
   else:
    # Preserve sparse versus full rectangular source structure, with no new operation.
    dense=all(sp.Rational(v)!=0 for row in original for v in row)
    if dense:rows=[[rng.choice(['1','2']) for j in range(c)] for i in range(r)]
    else:
     for i in range(r):
      for j in range(c):rows[i][j]='1' if i%c==j else '0'
   matrices.append(rows)
   witnesses=[(i+1,j+1) for i,row in enumerate(rows) for j,v in enumerate(row) if i!=j and sp.Rational(v)!=0]
   ws.append(list(rng.choice(witnesses)) if role=='offdiagonal' else None)
  parameters={'matrices':matrices,'witnesses':ws}
 p=json.loads(json.dumps(parameters));matrices=p['matrices'];ws=p['witnesses'];labels=t['labels']
 if len(matrices)!=3 or len(ws)!=3:raise ValueError('Three source-owned matrix and witness slots required')
 if sum(len(M)*len(M[0]) for M in matrices)>36:raise ValueError('Exceeds observed easy inspection workload')
 for M,original,role,w in zip(matrices,t['parameters']['matrices'],t['roles'],ws):
  if not 2<=len(M)<=4 or not 2<=len(M[0])<=4 or any(len(row)!=len(M[0]) for row in M):raise ValueError('Outside bounded shape domain')
  if any(sp.Rational(v) not in range(-3,8) for row in M for v in row):raise ValueError('Outside bounded entry domain')
  diagonal,identity=properties(M)
  if role=='identity' and not identity:raise ValueError('Identity role lost')
  if role=='diagonal' and (not diagonal or identity):raise ValueError('Nonidentity diagonal role lost')
  if role=='rectangular' and len(M)==len(M[0]):raise ValueError('Rectangular role lost')
  if role=='offdiagonal':
   count=lambda rows:sum(sp.Rational(v)!=0 for i,row in enumerate(rows) for j,v in enumerate(row) if i!=j)
   if len(M)!=len(M[0]) or count(M)!=count(original):raise ValueError('Offdiagonal role/count lost')
   if w is None or w[0]==w[1] or not 1<=w[0]<=len(M) or not 1<=w[1]<=len(M[0]) or sp.Rational(M[w[0]-1][w[1]-1])==0:raise ValueError('Invalid witness')
  elif w is not None:raise ValueError('Unexpected witness')
 problem=t['problem'];worked=t['worked_solution']
 matches=list(re.finditer(PATTERN,problem))
 for match,rows,original in reversed(list(zip(matches,matrices,t['parameters']['matrices']))):
  body=match[2] if rows==original else ' \\\\ '.join(' & '.join(row) for row in rows)
  problem=problem[:match.start(2)]+body+problem[match.end(2):]
 for label,rows,w in zip(labels,matrices,ws):
  if w:
   value=rows[w[0]-1][w[1]-1]
   regex=r'\$\{'+label.lower()+r'\}_\{\d\d\}=[^$]+\$'
   worked=re.sub(regex,lambda m:'${'+label.lower()+'}_{'+str(w[0])+str(w[1])+'}='+value+r'\ne 0$',worked)
 qid=str(uuid.uuid5(uuid.UUID(KP_UUID),json.dumps([problem,worked],sort_keys=True)))
 fields=[]
 for label,rows in zip(labels,matrices):
  correct=properties(rows)[int(t['kind']=='identity')];fid=str(uuid.uuid5(uuid.UUID(qid),'field:'+label))
  choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/text',':answer/value':value} for value in ('false','true')]
  fields.append({':answer-field/id':fid,':answer-field/key':label,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[int(correct)][':answer/id']]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Identifying a Special Square Matrix'},'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':worked,':question/difficulty':':question.difficulty/easy',':question/answer-fields':fields},'generation':{'version':VERSION,'template':template,'bank_profile':template,'seed':seed,'parameters':p,'parameter_fingerprint':fingerprint_text(problem),'source_basis':t['basis'],'sympy_version':sp.__version__}}

def batch(difficulty,count,seed):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty')
 if not 0<=count<=1000:raise ValueError('Bounded request count is 1000')
 records=[];used=set()
 for n in range(20000):
  if len(records)>=count:break
  try:r=generate(difficulty,seed+n,template=list(TEMPLATES)[n%len(TEMPLATES)])
  except ValueError:continue
  fp=r['generation']['parameter_fingerprint']
  if fp not in used:records.append(r);used.add(fp)
 return records

def markdown(r):return r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',default='easy');a.add_argument('--count',type=int,default=5);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');p=a.parse_args();rs=batch(p.difficulty,p.count,p.seed);print(json.dumps(rs,indent=2) if p.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
