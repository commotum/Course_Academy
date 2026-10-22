#!/usr/bin/env python3
"""Seeded, source-faithful invertible-matrix/rank-nullity questions.

Moderate count templates: uniform integer dilation of n, rank, nullity,
claimed dimensions and counts (k=1..3). The theorem's zero stays fixed.
Vector templates: invertible diagonal coordinate map with entries 1..3,
applied to every prompt/solution vector. A subspace RREF fingerprint rejects
basis-rescalings that do not change the task. Field layouts/banks stay fixed.
Normal practice selects an eligible truth subset before values, then derives
numeric comparisons and theorem-claim polarity. Explicit original parameters
without a truth subset replay the captured source.
"""
import argparse,copy,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix('')
RAW=json.loads((HERE/'source-current.json').read_text())
KP=RAW['record'];KP_ID=17592186184172;KP_UUID=KP[':knowledge-point/id']
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='1.1.0'
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
 if markers:
  assert [m[1] for m in markers]==['I','II','III']
  prefix=text[:markers[0].start()]
  statements=[text[m.end():markers[i+1].start() if i<2 else len(text)].strip().rstrip('-').strip() for i,m in enumerate(markers)]
 else:
  prefix=text.split('Select all that apply.')[0]
  statements=[f[':answer-field/key'] for f in q[':question/answer-fields']]
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

def subset_label(truths):
 labels=[s for s,b in zip(('I','II','III'),truths) if b]
 return 'None' if not labels else labels[0]+' only' if len(labels)==1 else ' and '.join(labels)+' only' if len(labels)==2 else 'I, II, and III'

def allowed_truths(key):
 fs=clean(Q[key])[':question/answer-fields']
 cases=[[bool(mask & (1<<i)) for i in range(3)] for mask in range(8)]
 if len(fs)>1:return cases[1:]
 bank={a[':answer/value'] for a in fs[0][':answer-field/choices']}
 return [t for t in cases if subset_label(t) in bank]

def claim(statement,wanted,t,rng):
 """Retain the source predicate role; vary its tested value or polarity."""
 n,r,u=t['n'],t['rank'],t['nullity']
 def number(actual):return actual if wanted else rng.choice([x for x in range(n+1) if x!=actual])
 if 'rank}' in statement:return re.sub(r'(rank\}\(A\)=)\d+',lambda m:m[1]+str(number(r)),statement)
 if 'nullity}' in statement:return re.sub(r'(nullity\}\(A\)=)\d+',lambda m:m[1]+str(number(u)),statement)
 if '-dimensional' in statement:return re.sub(r'\d+(\$?-dimensional)',lambda m:str(number(r))+m[1],statement)
 if 'non-pivot columns' in statement:return re.sub(r'\$\d+\$',lambda m:'$'+str(number(u))+'$',statement)
 if 'pivot col' in statement:return re.sub(r'\$\d+\$',lambda m:'$'+str(number(r))+'$',statement)
 if 'invertible' in statement:return '$A$ is '+('' if wanted==(r==n) else 'not ')+'invertible'
 if 'det(A)' in statement:return '$det(A)'+('=' if wanted==(r<n) else r'\ne ')+ '0$'
 if 'Col}' in statement:return re.sub(r'(Col\}\(A\))=',lambda m:m[1]+('=' if wanted==(r==n) else r'\ne '),statement)
 raise ValueError('Unknown source predicate: '+statement)

def apply_decisions(q,truths,rng):
 t=task_data(q);old=t['statements']
 new=[claim(s,b,t,rng) for s,b in zip(old,truths)]
 fs=q[':question/answer-fields'];radio=len(fs)==1
 if radio:
  for s,v in zip(old,new):q[':question/problem']=q[':question/problem'].replace(s,v,1)
  f=fs[0];label=subset_label(truths)
  f[':answer-field/correct']=[ ':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==label)]
 else:
  for f,s,b in zip(fs,new,truths):
   f[':answer-field/key']=s
   f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==str(b).lower())]
 # Preserve the source theorem exposition, then derive a concrete solution.
 intro=q[':question/worked-solution'].split("With that in mind, let's examine each statement in turn.")[0]
 # The captured checkbox theorem is too wide for the learning card. Keep its
 # mathematical exposition but put the left side on its own paragraph.
 wide=r'A\text{ is }\text{invertible}\quad\Longleftrightarrow\quad'
 if wide in intro:
  intro=intro.replace('$$\n'+wide,'$A$ is invertible\n\n$$\n'+r'\Longleftrightarrow\quad')
 # One additional source has the whole theorem in a single inline formula.
 intro=intro.replace('$A$ is invertible $\\,⇔\\,', '$A$ is invertible\n\n$\\,⇔\\,')
 n,r,u=t['n'],t['rank'],t['nullity']
 if t['given'][0]=='null-space':
  prefix=q[':question/problem'].split('Select all that apply.')[0].split('\n\nI.')[0]
  basis=[]
  for _,cells in vector_blocks(prefix):
   v=sp.Matrix([scalar(c) for c in cells]);syms=sorted(v.free_symbols,key=str)
   basis.extend([v.diff(s) for s in syms] if syms else [v])
  shown=',\\;'.join(r'\begin{bmatrix}'+r' \\ '.join(map(str,v))+r'\end{bmatrix}' for v in basis)
  given='The supplied null space has the independent spanning vectors\n\n$$\n'+shown+'\n$$\n\nThus $\\text{nullity}(A)='+str(u)+'.$'
 else:
  kind,count=t['given'];given=f'The {count} '+('non-pivot columns give $\\text{nullity}(A)='+str(u) if kind.startswith('non') else 'pivot columns give $\\text{rank}(A)='+str(r))+'.$'
 if t['given'][0]=='pivot-columns':
  substitution=f'{r}+\\text{{nullity}}(A)={n},\\qquad \\text{{nullity}}(A)={n}-{r}={u}.'
 else:
  substitution=f'\\text{{rank}}(A)+{u}={n},\\qquad \\text{{rank}}(A)={n}-{u}={r}.'
 calc='\n\nBy the rank-nullity theorem,\n\n$$\n\\text{rank}(A)+\\text{nullity}(A)=n.\n$$\n\n$$\n'+substitution+'\n$$\n\n'
 calc+=f'Hence $\\text{{rank}}(A)={r}$ and $\\text{{nullity}}(A)={u}$. '
 calc+=('Since rank equals the number of columns, $A$ is invertible and $\\det(A)\\ne 0$.' if r==n else 'Since rank is less than the number of columns, $A$ is not invertible and $\\det(A)=0$.')
 calc+=f' Also, $\\text{{Col}}(A)$ has dimension {r}. The number of pivot columns is {r}, and the number of non-pivot columns is {u}.\n\n'
 def reason(s):
  if 'rank}' in s:return f'$\\text{{rank}}(A)={r}$.'
  if 'nullity}' in s:return f'$\\text{{nullity}}(A)={u}$.'
  if '-dimensional' in s:return f'$\\dim(\\text{{Col}}(A))={r}$.'
  if 'non-pivot columns' in s:return f'The number of non-pivot columns is {u}.'
  if 'pivot col' in s:return f'The number of pivot columns is {r}.'
  if 'invertible' in s:return 'The rank '+('equals' if r==n else 'is less than')+' the number of columns.'
  if 'det(A)' in s:return '$A$ is '+('invertible, so $\\det(A)\\ne 0$.' if r==n else 'not invertible, so $\\det(A)=0$.')
  return f'The column-space dimension is {r}, '+('equal to' if r==n else 'less than')+f' {n}.'
 evaluations='\n\n'.join('- Statement '+(('I','II','III')[i] if radio else '“'+s+'”')+' is '+str(b).lower()+'. '+reason(s) for i,(s,b) in enumerate(zip(new,truths)))
 conclusion=subset_label(truths) if radio else '; '.join(s for s,b in zip(new,truths) if b)
 q[':question/worked-solution']=intro+given+calc+evaluations+'\n\nTherefore, the correct answer is '+conclusion+'.'

def generate(difficulty,seed=0,template=None,parameters=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty+'; no source evidence for an easy band')
 rng=random.Random(seed);keys=sorted(k for k in Q if level_of(k)==difficulty);key=template or rng.choice(keys)
 if key not in keys:raise ValueError('Template/difficulty mismatch')
 if parameters is None:
  # Decide the answer-bearing assignment before choosing incidental values.
  truths=rng.choice(allowed_truths(key))
  parameters={'truths':truths}
  if is_vector(key):parameters['diagonal']=[rng.randint(1,3) for _ in range(n_of(Q[key][':question/problem']))]
  else:
   parameters['scale']=rng.randint(1,3)
   parameters['count']=rng.randint(0,n_of(Q[key][':question/problem'])*parameters['scale'])
 q=clean(Q[key])
 if is_vector(key):
  d=parameters['diagonal'];assert len(d)==n_of(q[':question/problem']) and all(type(x)==int and 1<=x<=3 for x in d)
  for name in (':question/problem',':question/worked-solution'):q[name]=transform_vectors(q[name],d)
 else:
  k=parameters['scale'];assert type(k)==int and 1<=k<=3
  for name in (':question/problem',':question/worked-solution'):q[name]=re.sub(r'\d+',lambda m:str(int(m[0])*k),q[name])
  for f in q[':question/answer-fields']:
   if f[':answer-field/type']==':answer-field.type/checkbox':f[':answer-field/key']=re.sub(r'\d+',lambda m:str(int(m[0])*k),f[':answer-field/key'])
 if 'count' in parameters:
  c=parameters['count'];assert type(c)==int and 0<=c<=n_of(q[':question/problem'])
  q[':question/problem']=re.sub(r'\$\d+\$( (?:non-pivot|pivot) column)',lambda m:'$'+str(c)+'$'+m[1],q[':question/problem'])
 if 'truths' in parameters:
  assert parameters['truths'] in allowed_truths(key)
  apply_decisions(q,parameters['truths'],rng)
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
 p=argparse.ArgumentParser();p.add_argument('--difficulty',required=True);p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--template');p.add_argument('--format',choices=['json'],default='json');a=p.parse_args()
 if a.count<1:p.error('--count must be positive')
 rows=[generate(a.difficulty,a.seed,a.template)] if a.template else batch(a.difficulty,a.count,a.seed)
 print(json.dumps(rows,indent=2))

# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':main()
