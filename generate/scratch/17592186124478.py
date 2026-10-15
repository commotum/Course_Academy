"""Easy non-pivot-column identification, retaining complete source bank profiles.

Only the observed echelon-scanning method is supported. Novelty is structural:
shape and pivot positions, never coefficient changes, labels, seeds or bank order.
"""
import argparse, hashlib, itertools, json, random, re, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186124478
KP_UUID='a5f0d2e9-1cf6-5fe4-85cc-f401382f39b2'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'non-pivot-column-generator-v1'))
SUPPORTED_LEVELS=('easy',)
VERSION='1.0.0'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
SNAPSHOT=json.loads((HERE/'snapshot.json').read_text())
CASES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
MAT=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def matrices(text):
 return [sp.Matrix([[sp.Integer(c.strip()) for c in r.split('&')] for r in m.split(r'\\')]) for m in MAT.findall(text)]
def pivots(m):return tuple(next(j for j in range(m.cols) if m[i,j]) for i in range(m.rows) if any(m[i,j] for j in range(m.cols)))
def latex(m):return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(str(m[i,j]) for j in range(m.cols)) for i in range(m.rows))+r'\end{bmatrix}'
def ordinal(i):return f'${i}$'+({1:'st',2:'nd',3:'rd'}.get(i,'th'))
def joined(items):
 return items[0] if len(items)==1 else ' and '.join(items) if len(items)==2 else ', '.join(items[:-1])+', and '+items[-1]
def subset(value,n):return tuple(range(n)) if value=='All the columns are non-pivot' else tuple(int(x)-1 for x in re.findall(r'\$(\d+)\$',value))
def field(sid):
 fs=[f for f in CASES[sid][':question/answer-fields'] if f.get(':answer-field/correct')]
 assert len(fs)==1
 return fs[0]
def fingerprint(q):
 ms=matrices(q[':question/problem'])
 if not ms:return hashlib.sha256(q[':question/problem'].encode()).hexdigest()
 m=ms[0];return json.dumps([m.rows,m.cols,pivots(m)])
DEFAULTS={sid:{'matrix':[[int(x) for x in row] for row in matrices(q[':question/problem'])[0].tolist()],'mapping':list(range(matrices(q[':question/problem'])[0].cols)),'replay':True} for sid,q in CASES.items()}
def generate(difficulty='easy',seed=0,template=None,parameters=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 rng=random.Random(seed);sid=template or rng.choice(list(CASES));old=CASES[sid];base=matrices(old[':question/problem'])[0];n=base.cols
 if parameters is None:
  mapping=list(range(n));rng.shuffle(mapping);ps=sorted(mapping[j] for j in pivots(base));m=sp.zeros(base.rows,n)
  for i,j in enumerate(ps):
   m[i,j]=rng.choice([x for x in range(-9,10) if x])
   for k in range(j+1,n):m[i,k]=rng.randint(-9,9)
  parameters={'matrix':[[int(x) for x in row] for row in m.tolist()],'mapping':mapping,'replay':False}
 p=parameters;assert set(p)=={'matrix','mapping','replay'} and isinstance(p['replay'],bool)
 m=sp.Matrix(p['matrix']);mapping=p['mapping'];assert m.shape==base.shape and sorted(mapping)==list(range(n))
 assert all(x.is_Integer and -9<=x<=9 for x in m)
 ps=pivots(m);assert ps==tuple(sorted(mapping[j] for j in pivots(base)))
 assert len(ps)==len(set(ps)) and len(ps)==len(pivots(base))
 assert all(not any(m[i,j] for j in range(n)) for i in range(len(ps),m.rows))
 non=tuple(j for j in range(n) if j not in ps);assert len(non) in (1,2)
 f=field(sid);values=[]
 for a in f[':answer-field/choices']:
  ss=tuple(sorted(mapping[j] for j in subset(a[':answer/value'],n)))
  value='All the columns are non-pivot' if len(ss)==n else joined([ordinal(j+1) for j in ss])+' only'
  values.append(value)
 # Exact observed typography for original-parameter replay, including legacy typos.
 replay=p['replay'];label=re.search(r'matrix \$(\w)\$',old[':question/problem'])[1]
 if replay:
  assert p==DEFAULTS[sid]
  problem=old[':question/problem'];solution=old[':question/worked-solution'];values=[a[':answer/value'] for a in f[':answer-field/choices']]
 else:
  display='$$\n'+label+'='+latex(m)+'\n$$'
  problem=f'The row echelon form matrix ${label}$ is given below. What are its **non**-pivot columns?\n\n'+display
  solution='Remember that the pivots of a matrix in row echelon form are the first non-zero entries in each row of the matrix.\n\n'
  solution+=f'We can see that ${label}$ has ${len(ps)}$ pivots in the '+joined([ordinal(j+1) for j in ps])+' columns:\n\n'+display+'\n\n'
  solution+='Therefore, the only non-pivot '+('column is the ' if len(non)==1 else 'columns are the ')+joined([ordinal(j+1) for j in non])+(' column.' if len(non)==1 else ' columns.')
 assert len(values)==len(set(values))==5
 correct_index=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
 # Content identity includes full authored bank, but no seed, choice order or replay flag.
 identity=json.dumps([problem,solution,sorted(values)],sort_keys=True)
 qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),identity));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/text',':answer/value':value} for value in values]
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct_index][':answer/id']]}]}
 return {'question':q,'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE[':knowledge-point/title']},'generation':{'generator_id':GENERATOR_UUID,'generator_version':VERSION,'seed':seed,'template':sid,'bank_profile':sid,'parameters':p,'source_question_id':old[':question/id'],'source_basis':SNAPSHOT['basis'],'dependencies':{'sympy':sp.__version__},'assets':[],'mathematical_fingerprint':fingerprint(q)}}
def batch(difficulty,count,seed=0):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 if type(count) is not int or count<0:raise ValueError('Count must be nonnegative integer')
 result=[];seen=set()
 for offset in range(5000):
  if len(result)==count:break
  rec=generate(difficulty,seed+offset);fp=fingerprint(rec['question'])
  if fp not in seen:seen.add(fp);result.append(rec)
 return result
def markdown(rec):
 q=rec['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--output',type=Path);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args()
 records=batch(a.difficulty,a.count,a.seed);value=json.dumps(records,indent=2) if a.format=='json' else '\n\n'.join(markdown(r) for r in records)
 if a.output:a.output.write_text(value+'\n')
 else:print(value)
