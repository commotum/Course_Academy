"""Easy non-pivot-column identification with one checkbox per matrix column.

Only the observed echelon-scanning method is supported. Novelty is structural:
shape and pivot positions, never coefficient changes, labels, seeds or bank order.
"""
import argparse, hashlib, itertools, json, random, re, uuid
from pathlib import Path
import sympy as sp
from math_format import matrix_tex, normalize_prose, checked_math_content
KP_ID=17592186124478
KP_UUID='a5f0d2e9-1cf6-5fe4-85cc-f401382f39b2'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'non-pivot-column-generator-v1'))
SUPPORTED_LEVELS=('easy',)
VERSION='2.0.0'
HERE=Path(__file__).resolve().parent
SNAPSHOT=json.loads((HERE/'source.json').read_text())
SOURCE=SNAPSHOT['kp']
CASES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
MAT=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def matrices(text):
 return [sp.Matrix([[sp.Integer(c.strip()) for c in r.split('&')] for r in m.split(r'\\')]) for m in MAT.findall(text)]
def pivots(m):return tuple(next(j for j in range(m.cols) if m[i,j]) for i in range(m.rows) if any(m[i,j] for j in range(m.cols)))
def latex(m):return matrix_tex([[str(m[i,j]) for j in range(m.cols)] for i in range(m.rows)])
def ordinal(i):return f'${i}$'+({1:'st',2:'nd',3:'rd'}.get(i,'th'))
def joined(items):
 return items[0] if len(items)==1 else ' and '.join(items) if len(items)==2 else ', '.join(items[:-1])+', and '+items[-1]
def subset(value,n):return tuple(range(n)) if value=='All the columns are non-pivot' else tuple(int(x)-1 for x in re.findall(r'\$(\d+)\$',value))
def checkbox_fields(qid,m,selected):
 fields=[]
 for j in range(m.cols):
  key=normalize_prose(f'Column {j+1}: $'+latex(m[:,j])+'$');fid=str(uuid.uuid5(uuid.UUID(qid),key))
  answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/text',':answer/value':value} for value in ('false','true')]
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[int(j in selected)][':answer/id']]})
 return fields
def fingerprint(q):
 ms=matrices(q[':question/problem'])
 if not ms:return hashlib.sha256(q[':question/problem'].encode()).hexdigest()
 m=ms[0];return json.dumps([m.rows,m.cols,pivots(m)])
DEFAULTS={sid:{'matrix':[[int(x) for x in row] for row in matrices(q[':question/problem'])[0].tolist()],'label':re.search(r'matrix \$(\w)\$',q[':question/problem'])[1],'replay':True} for sid,q in CASES.items()}
SHAPES=tuple(sorted({matrices(q[':question/problem'])[0].shape for q in CASES.values()}))
def ranks(rows,cols):return tuple(r for r in range(2,min(rows,4)+1) if 1<=cols-r<=2)
def structural_cases():return [(rows,cols,ps) for rows,cols in SHAPES for r in ranks(rows,cols) for ps in itertools.combinations(range(cols),r)]

@checked_math_content
def generate(difficulty='easy',seed=0,template=None,parameters=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 rng=random.Random(seed);sid=template or rng.choice(list(CASES));old=CASES[sid]
 if parameters is None:
  rows,n=rng.choice(SHAPES);rank=rng.choice(ranks(rows,n))
  ps=tuple(sorted(rng.sample(range(n),rank)));m=sp.zeros(rows,n)
  for i,j in enumerate(ps):
   m[i,j]=rng.choice([x for x in range(-9,10) if x])
   for k in range(j+1,n):m[i,k]=rng.randint(-9,9)
  parameters={'matrix':[[int(x) for x in row] for row in m.tolist()],'label':rng.choice(('A','B','P','R')),'replay':False}
 p=parameters
 if set(p)!={'matrix','label','replay'} or type(p['replay']) is not bool:raise ValueError('Invalid parameters')
 m=sp.Matrix(p['matrix']);n=m.cols
 assert m.shape in SHAPES and p['label'] in ('A','B','P','R')
 assert all(x.is_Integer and -9<=x<=9 for x in m)
 ps=pivots(m)
 assert len(ps)==len(set(ps)) and ps==tuple(sorted(ps)) and len(ps) in ranks(m.rows,n)
 assert all(not any(m[i,j] for j in range(n)) for i in range(len(ps),m.rows))
 non=tuple(j for j in range(n) if j not in ps);assert len(non) in (1,2)
 # Preserve the captured mathematics and solution, with documented wording repairs.
 replay=p['replay'];label=p['label']
 if replay:
  assert p==DEFAULTS[sid]
  problem=old[':question/problem'];solution=old[':question/worked-solution']
 else:
  display='$$\n'+label+'='+latex(m)+'\n$$'
  problem=f'The row echelon form matrix ${label}$ is given below. What are its **non**-pivot columns?\n\n'+display+'\n\nSelect all that apply.'
  solution='Remember that the pivots of a matrix in row echelon form are the first non-zero entries in each row of the matrix.\n\n'
  solution+=f'We can see that ${label}$ has ${len(ps)}$ pivots in the '+joined([ordinal(j+1) for j in ps])+' columns:\n\n'+display+'\n\n'
  solution+='Therefore, the only non-pivot '+('column is the ' if len(non)==1 else 'columns are the ')+joined([ordinal(j+1) for j in non])+(' column.' if len(non)==1 else ' columns.')
 problem=normalize_prose(problem);solution=normalize_prose(solution)
 # Checkbox content determines identity, independent of seed or historical bank.
 identity=json.dumps([problem,solution,[[f'Column {j+1}',j in non] for j in range(n)]],sort_keys=True)
 qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),identity))
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':checkbox_fields(qid,m,non)}
 return {'question':q,'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE[':knowledge-point/title']},'generation':{'generator_id':GENERATOR_UUID,'generator_version':VERSION,'seed':seed,'template':'ref-complement','bank_profile':'boolean-per-column','parameters':p,'source_question_id':old[':question/id'],'source_basis':SNAPSHOT['basis'],'dependencies':{'sympy':sp.__version__},'assets':[],'mathematical_fingerprint':fingerprint(q)}}
def batch(difficulty,count,seed=0):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 if type(count) is not int or count<0:raise ValueError('Count must be nonnegative integer')
 if count>len(structural_cases()):raise ValueError('Count exceeds finite structural family')
 result=[];seen=set()
 for offset in range(5000):
  if len(result)==count:break
  rec=generate(difficulty,seed+offset);fp=fingerprint(rec['question'])
  if fp not in seen:seen.add(fp);result.append(rec)
 if len(result)!=count:raise RuntimeError('Could not sample requested distinct structural cases')
 return result
def markdown(rec):
 q=rec['question'];return q[':question/problem']+'\n\n'+'\n'.join('- [ ] '+f[':answer-field/key'] for f in q[':question/answer-fields'])+'\n\n'+q[':question/worked-solution']

# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--output',type=Path);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args()
 records=batch(a.difficulty,a.count,a.seed);value=json.dumps(records,indent=2) if a.format=='json' else '\n\n'.join(markdown(r) for r in records)
 if a.output:a.output.write_text(value+'\n')
 else:print(value)
