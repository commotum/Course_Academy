"""Easy 3x3 row elimination: two unknown additions, complete source-owned banks.
Same-method slots: pivot row, eliminated column, signed integer matrices.
Moderate/hard are explicitly unsupported; no new mathematical stages invented.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186161967
KP_UUID='908b96db-9463-50b5-89a3-056072c930ba'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'row-zero-generator-v1'))
HERE=Path(__file__).with_suffix('')
SOURCES={q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
SUPPORTED_LEVELS=('easy',)
PROFILES=tuple(SOURCES)
def recipes(profile,a,b):
 u=lambda z:1 if z>0 else -1
 return {
 'q-42531':[(a,-u(b)),(-a,-b),(a,b),(a,-b),(-a,b)],
 'q-91163':[(-a,b),(-b,-a),(a,-b),(-a,-b),(a,b)],
 'q-130444':[(a,-b),(a,b),(-b,-a),(-a,-b),(-a,b)],
 'q-130451':[(-a,b),(a,-b),(a,b),(a,u(b)),(-a,-b)],
 'q-91158':[(-a,b),(b,a),(a,b),(-a,-b),(a,-b)],
 'q-91160':[(-a,b),(a,-b),(a,b),(-a,-b),(b,a)],
 'q-91162':[(a,-b),(a,u(b)),(a,b),(-a,-b),(-a,b)],
 'q-130448':[(-a,-b),(a,-b),(b,a),(-a,b),(a,b)],
 'q-91157':[(-a,-b),(a,b),(a,-b),(-a,b),(-b,-a)],
 'q-91159':[(a,b),(a,-b),(-a,b),(-a,-b),(b,a)],
 }[profile]
UNIT_PROFILES=('q-42531','q-130451','q-91162')
def extra_options(profile,a,b):
 """Source-derived magnitude errors with signs independent of the answer."""
 a,b=abs(a),abs(b)
 shapes=([(1,b)] if a>1 else [])+([(a,1)] if b>1 else []) if profile in UNIT_PROFILES else ([(b,a)] if a!=b else [])
 return [(s*x,t*y) for x,y in shapes for s in (-1,1) for t in (-1,1)]
def generalized_bank(profile,a,b,rng):
 bank=[(s*abs(a),t*abs(b)) for s in (-1,1) for t in (-1,1)]
 bank.append(rng.choice(extra_options(profile,a,b)))
 rng.shuffle(bank)
 return bank
def matrices(text):
 return [sp.Matrix([[int(v.strip()) for v in row.split('&')] for row in raw.split(r'\\')]) for raw in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def clean(text):return re.sub(r'\s+','',text).replace('{R}','R').replace(r'\,','').replace('$','')
def operations(text):
 text=clean(text)
 return [(int(i)-1,int(p)-1,int((sign or '+')+(n or '1'))) for i,j,sign,n,p in re.findall(r'R_\{(\d)\}:=R_\{(\d)\}([+-]?)(\d*)R_\{(\d)\}',text) if i==j]
def source_parameters(q):
 A,B=matrices(q[':question/problem'])[:2]
 pivot=int(re.search(r'k(?:\{R\}|R)_\{(\d)\}',q[':question/problem']).group(1))-1
 targets=[r for r in range(3) if r!=pivot]
 cols=[c for c in range(3) if A[pivot,c]!=0 and all(B[r,c]==0 for r in targets)]
 assert cols
 reference=re.search(r'(?:\{a\}|a)_\{(\d)(\d)\}',q.get(':question/worked-solution',''))
 c=int(reference.group(2))-1 if reference else cols[0]
 assert c in cols and (not reference or int(reference.group(1))-1==pivot)
 ks=[int(-A[r,c]/A[pivot,c]) if r!=pivot else 0 for r in range(3)]
 assert all(A[r,:]+ks[r]*A[pivot,:]==B[r,:] for r in targets) and A[pivot,:]==B[pivot,:]
 return {'A':A.tolist(),'pivot':pivot,'column':c,'ks':ks}
ORIGINAL={k:source_parameters(q) for k,q in SOURCES.items()}
def tex(M):return r'\begin{bmatrix}'+' \\\\ '.join(' & '.join(str(x) for x in row) for row in sp.Matrix(M).tolist())+r'\end{bmatrix}'
def op(r,p,k):return 'R_{'+str(r+1)+'}:=R_{'+str(r+1)+'}'+('+' if k>0 else '-')+('' if abs(k)==1 else str(abs(k)))+'R_{'+str(p+1)+'}'
def pair(targets,p,coeff):return '$'+op(targets[0],p,coeff[0])+'$ and $'+op(targets[1],p,coeff[1])+'$'
def fingerprint(prompt):
 A,B=matrices(prompt)[:2]
 match=re.search(r'k(?:\{R\}|R)_\{(\d)\}',prompt);assert match
 return hashlib.sha256(json.dumps([A.tolist(),B.tolist(),int(match.group(1))],default=int).encode()).hexdigest()
def generate(difficulty='easy',seed=0,template=None,parameters=None,bank_profile=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty '+difficulty)
 rng=random.Random(seed);profile=bank_profile or template or rng.choice(PROFILES)
 if profile not in PROFILES:raise ValueError('Unknown source profile')
 source_replay=parameters is not None and parameters==ORIGINAL[profile]
 if parameters is None:
  for _ in range(300):
   p=rng.randrange(3);c=rng.randrange(3);targets=[r for r in range(3) if r!=p]
   ks=[rng.choice([*range(-9,0),*range(1,10)]) if r!=p else 0 for r in range(3)]
   A=sp.Matrix(3,3,[rng.randint(-10,12) for _ in range(9)]);A[p,c]=rng.choice([-3,-2,-1,1,2,3])
   for r in targets:A[r,c]=-ks[r]*A[p,c]
   if max(abs(A[r,c]) for r in targets)<=12 and extra_options(profile,ks[targets[0]],ks[targets[1]]) and not any(z!=c and A[p,z]!=0 and all(A[r,z]+ks[r]*A[p,z]==0 for r in targets) for z in range(3)):break
  else:raise ValueError('Bounded sampler exhausted')
  parameters={'A':A.tolist(),'pivot':p,'column':c,'ks':ks}
 parameters=json.loads(json.dumps(parameters,default=int));A=sp.Matrix(parameters['A']);p=parameters['pivot'];c=parameters['column'];ks=parameters['ks'];targets=[r for r in range(3) if r!=p]
 assert A.shape==(3,3) and 0<=p<3 and 0<=c<3 and A[p,c]!=0 and ks[p]==0
 assert all(isinstance(k,int) and k!=0 and A[r,c]+k*A[p,c]==0 for r,k in enumerate(ks) if r!=p)
 B=A.copy();stages=[]
 for r in targets:B[r,:]=B[r,:]+ks[r]*B[p,:];stages.append(B.copy())
 # Separate bank RNG keeps replay from explicit parameters identical to sampling.
 bank_rng=random.Random(str(seed)+':bank')
 bank=(recipes(profile,ks[targets[0]],ks[targets[1]]) if source_replay else generalized_bank(profile,ks[targets[0]],ks[targets[1]],bank_rng));assert len(set(bank))==5
 correct=(ks[targets[0]],ks[targets[1]]);assert bank.count(correct)==1
 prompt='$$\nA='+tex(A)+r',\,B='+tex(B)+'\n$$\n\nBy applying elementary row operations of the form $R_{i}:=R_{i}+kR_{'+str(p+1)+'},$ the matrix $A$ can be transformed into the matrix $B.$ What are the elementary row operations?'
 direction=('above' if p==2 else 'below' if p==0 else 'above and below')
 solution='To transform $A$ into $B,$ we need to make the entries '+direction+' $a_{'+str(p+1)+str(c+1)+'}='+str(A[p,c])+'$ equal to $0.$\n\nTo do this, we can apply the following elementary row operations:\n\n$$\n'+tex(A)+'\n'+ '\n'.join(r'\xrightarrow{'+op(r,p,ks[r])+'}'+tex(stage) for r,stage in zip(targets,stages))+'=B\n$$\n\nTherefore, the elementary row operations are\n\n'+pair(targets,p,correct)+'.'
 fp=fingerprint(prompt);qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),fp+profile+json.dumps(sorted(bank))));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),str(coeff))),':answer/type':':answer.type/text',':answer/value':pair(targets,p,coeff)} for coeff in bank]
 question={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[bank.index(correct)][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Using Row Operations to Create a Column of Zeros in a 3x3 Matrix'},'question':question,'generation':{'version':2,'seed':seed,'template':'row-zero-3x3','bank_profile':profile,'bank_mode':'source-replay' if source_replay else 'independent-signs','parameters':parameters,'parameter_fingerprint':fp,'generator_id':GENERATOR_UUID,'sympy_version':sp.__version__}}
def batch_has_counterexamples(rows):
 """Each visible magnitude-error family must refute both sign polarities."""
 groups={}
 fingerprints=set()
 for row in rows:
  meta=row['generation'];fp=meta['parameter_fingerprint']
  if fp in fingerprints:return False
  fingerprints.add(fp)
  params=meta['parameters'];correct=tuple(k for i,k in enumerate(params['ks']) if i!=params['pivot'])
  bank=[tuple(o[2] for o in operations(a[':answer/value'])) for a in row['question'][':question/answer-fields'][0][':answer-field/choices']]
  extra=next(z for z in bank if tuple(map(abs,z))!=tuple(map(abs,correct)))
  shape=tuple(abs(extra[d])!=abs(correct[d]) for d in (0,1))
  signs=groups.setdefault(shape,[set(),set()])
  for d in (0,1):signs[d].add(extra[d]*correct[d]>0)
 return all(all(len(values)==2 for values in signs) for signs in groups.values())

def batch(difficulty,count,seed):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty '+difficulty)
 if count<0:raise ValueError('Count must be nonnegative')
 if count<2:return [generate(difficulty,seed)] if count else []
 rng=random.Random(str(seed)+':batch')
 # A full two-coefficient sign decision requires four cases in each visible
 # bank shape. Small batches choose a shape, not a reduced source family.
 shapes=[(True,False),(False,True),(True,True)]
 if count<8:shapes=[rng.choice(shapes)]
 elif count<12:shapes=[rng.choice(shapes[:2]),shapes[2]]
 rng.shuffle(shapes)
 sizes=[count//len(shapes)+(i<count%len(shapes)) for i in range(len(shapes))]
 rows=[];fingerprints=set()
 for shape,size in zip(shapes,sizes):
  profiles=list(UNIT_PROFILES if shape!=(True,True) else tuple(p for p in PROFILES if p not in UNIT_PROFILES))
  rng.shuffle(profiles)
  # Choose the extra signs independently, then exercise all four possible
  # correct sign pairs against that cue. This also defeats cross-coordinate
  # sign inference, rather than merely reversing the old first-sign cue.
  extra_signs=(rng.choice((-1,1)),rng.choice((-1,1)))
  cases=[(-1,-1),(-1,1),(1,-1),(1,1)]
  rng.shuffle(cases)
  if size<4:
   first=(rng.choice((-1,1)),rng.choice((-1,1)))
   cases=[first,tuple(-v for v in first)]+cases
  plan=cases[:size]+[rng.choice(cases[:4]) for _ in range(max(0,size-len(cases)))]
  rng.shuffle(plan)
  for i,signs in enumerate(plan):
   profile=profiles[i%len(profiles)]
   for attempt in range(10000):
    row=generate(difficulty,rng.getrandbits(64),bank_profile=profile)
    meta=row['generation'];params=meta['parameters']
    correct=tuple(k for r,k in enumerate(params['ks']) if r!=params['pivot'])
    if tuple(1 if k>0 else -1 for k in correct)!=signs:continue
    bank=[tuple(o[2] for o in operations(a[':answer/value'])) for a in row['question'][':question/answer-fields'][0][':answer-field/choices']]
    extra=next(z for z in bank if tuple(map(abs,z))!=tuple(map(abs,correct)))
    if tuple(abs(extra[d])!=abs(correct[d]) for d in (0,1))!=shape:continue
    if tuple(1 if k>0 else -1 for k in extra)!=extra_signs:continue
    if meta['parameter_fingerprint'] in fingerprints:continue
    fingerprints.add(meta['parameter_fingerprint']);rows.append(row);break
   else:raise ValueError('Bounded batch sampler exhausted')
 rng.shuffle(rows)
 assert len(rows)==count and batch_has_counterexamples(rows)
 for row in rows:row['generation']['batch']={'version':2,'seed':seed,'count':count}
 return rows
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',default='easy');a.add_argument('--count',type=int,default=5);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');args=a.parse_args();rows=batch(args.difficulty,args.count,args.seed);print(json.dumps(rows,indent=2) if args.format=='json' else '\n\n'.join(markdown(r) for r in rows))
