"""Moderate: three column additions, one given and two requested; source-owned banks.
No easy/hard evidence. Integer entries [-9,9], pivots +/-1,+/-2; bounded
same-method generalization to every row, pivot column and given-column position.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
try:
 import sympy as sp
except ModuleNotFoundError:
 import os,sys
 interpreter=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 os.execv(str(interpreter),[str(interpreter),str(Path(__file__).resolve()),*sys.argv[1:]])
KP_ID=17592186161966
KP_UUID='958cdcf3-aaba-5275-85f8-9531f10b3d0e'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'column-zero-generator-v1'))
HERE=Path(__file__).with_suffix('')
SOURCES={q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
SUPPORTED_LEVELS=('moderate',)
# Complete observed profiles: coefficient pair recipes. Unit errors retain the
# sign of the source coefficient; offsets are observed patterns, not psychology.
def recipes(profile,a,b):
 u=lambda z: 1 if z>0 else -1
 return {
 'q-42563':[(-a-1,b+1),(-a,b),(-a,-b),(a+2,b),(a,b)],
 'q-91208':[(a,b),(a,b+1),(a,-b),(-a,-b),(-b,-a)],
 'q-130619':[(a,-b),(a,b),(-b,-a),(-a,-b),(-a,b)],
 'q-130627':[(-b,-a),(-a,b),(-a,-b),(a,b),(a,-b)],
 'q-42929':[(a,u(b)),(a,b),(b,a),(a,-b),(-a,b)],
 'q-91210':[(a,b),(b,a),(-a,-b),(-b,-a),(a,-b)],
 'q-91211':[(-b,-a),(-a,-b),(a,b),(b,a),(a,-b)],
 'q-91214':[(a,b),(a,u(b)),(b,a),(a,-b),(-a,-b)],
 'q-130624':[(-b,-a),(-a,-b),(-a,b),(a,-b),(a,b)],
 'q-42562':[(a,b),(-b,-a),(a+2,b),(-a,b),(a,-b)],
 'q-91212':[(u(a),u(b)),(a,b-1),(a,b),(-a,-b),(-u(a),-u(b))],
 }[profile]
PROFILES=tuple(k for k,q in SOURCES.items() if ':question/difficulty' in q)
def matrices(text):
 return [sp.Matrix([[int(v.strip()) for v in row.split('&')] for row in raw.split(r'\\')]) for raw in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def clean(text):return re.sub(r'\s+','',text).replace('{C}','C').replace(r'\,','').replace('$','')
def operations(text):
 text=clean(text)
 return [(int(i)-1,int(p)-1,int((sign or '+')+(n or '1'))) for i,j,sign,n,p in re.findall(r'C_\{(\d)\}:=C_\{(\d)\}([+-]?)(\d*)C_\{(\d)\}',text) if i==j]
def source_parameters(q):
 A,B=matrices(q[':question/problem'])[:2]
 ops=operations(q[':question/problem']);assert len(ops)==1
 given,p,_=ops[0]
 rows=[r for r in range(4) if A[r,p]!=0 and all(B[r,c]==0 for c in range(4) if c!=p)]
 assert len(rows)==1
 r=rows[0];ks=[int(-A[r,c]/A[r,p]) if c!=p else 0 for c in range(4)]
 assert all(A[:,c]+ks[c]*A[:,p]==B[:,c] for c in range(4) if c!=p)
 return {'A':A.tolist(),'row':r,'pivot':p,'given':given,'ks':ks}
ORIGINAL={k:source_parameters(q) for k,q in SOURCES.items()}
def tex(M):return r'\begin{bmatrix}'+' \\\\ '.join(' & '.join(str(x) for x in row) for row in sp.Matrix(M).tolist())+r'\end{bmatrix}'
def op(c,p,k):return 'C_{'+str(c+1)+'}:=C_{'+str(c+1)+'}'+('+' if k>0 else '-')+('' if abs(k)==1 else str(abs(k)))+'C_{'+str(p+1)+'}'
def pair(targets,p,coeff):return '$'+op(targets[0],p,coeff[0])+'$ and $'+op(targets[1],p,coeff[1])+'$'
def fingerprint(prompt):
 A,B=matrices(prompt)[:2];given=operations(prompt)
 return hashlib.sha256(json.dumps([A.tolist(),B.tolist(),given],default=int).encode()).hexdigest()
def generate(difficulty='moderate',seed=0,template=None,parameters=None,bank_profile=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty '+difficulty)
 rng=random.Random(seed);profile=bank_profile or template or rng.choice(PROFILES)
 if profile not in PROFILES:raise ValueError('Unrated source profile excluded')
 if parameters is None:
  for _ in range(100):
   p=rng.randrange(4);r=rng.randrange(4);cols=[c for c in range(4) if c!=p];given=rng.choice(cols)
   ks=[rng.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) if c!=p else 0 for c in range(4)]
   A=sp.Matrix(4,4,[rng.randint(-9,9) for _ in range(16)]);A[r,p]=rng.choice([-2,-1,1,2])
   for c in cols:A[r,c]=-ks[c]*A[r,p]
   targets=[c for c in cols if c!=given];bank=recipes(profile,ks[targets[0]],ks[targets[1]])
   if len(set(bank))==5 and not any(A[z,p]!=0 and all(A[z,c]+ks[c]*A[z,p]==0 for c in cols) for z in range(4) if z!=r):break
  else:raise ValueError('Bounded sampler exhausted')
  parameters={'A':A.tolist(),'row':r,'pivot':p,'given':given,'ks':ks}
 parameters=json.loads(json.dumps(parameters,default=int));A=sp.Matrix(parameters['A']);r=parameters['row'];p=parameters['pivot'];given=parameters['given'];ks=parameters['ks'];cols=[c for c in range(4) if c!=p];targets=[c for c in cols if c!=given]
 assert A.shape==(4,4) and 0<=r<4 and given in cols and A[r,p]!=0
 assert all(A[r,c]+ks[c]*A[r,p]==0 for c in cols)
 B=A.copy();stages=[]
 for c in cols:B[:,c]=B[:,c]+ks[c]*B[:,p];stages.append(B.copy())
 bank=recipes(profile,ks[targets[0]],ks[targets[1]]);assert len(set(bank))==5
 correct=(ks[targets[0]],ks[targets[1]]);assert bank.count(correct)==1
 prompt='$$\nA='+tex(A)+r',\,B='+tex(B)+'\n$$\n\nConsider the matrices $A$ and $B$ above. By applying three matrix elementary column operations\n\n'+'\n'.join('- $'+(op(c,p,ks[c]) if c==given else 'C_{'+str(c+1)+r'}:=\ldots')+'$' for c in cols)+'\n\neach of the form $C_i:=C_i+kC_{'+str(p+1)+'},$ the matrix $A$ can be transformed into the matrix $B.$ What are the missing elementary column operations?'
 solution='To transform $A$ into $B,$ we need to make entries in row '+str(r+1)+' other than $a_{'+str(r+1)+str(p+1)+'}='+str(A[r,p])+'$ equal to $0.$\n\nTo do this, we can apply the following elementary column operations:\n\n$$\n'+tex(A)+'\n'+ '\n'.join(r'\xrightarrow{'+op(c,p,ks[c])+'}'+tex(stage) for c,stage in zip(cols,stages))+'=B\n$$\n\nTherefore, the corresponding elementary column operations are\n\n'+pair(targets,p,correct)+'.'
 fp=fingerprint(prompt);qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),fp+profile));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),str(coeff))),':answer/type':':answer.type/text',':answer/value':pair(targets,p,coeff)} for coeff in bank]
 question={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[bank.index(correct)][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Using Column Operations to Create a Row of Zeros in a 4x4 Matrix'},'question':question,'generation':{'version':1,'seed':seed,'template':'column-zero-4x4','bank_profile':profile,'parameters':parameters,'parameter_fingerprint':fp,'generator_id':GENERATOR_UUID,'sympy_version':sp.__version__}}
def batch(difficulty,count,seed):return [generate(difficulty,seed+i,bank_profile=PROFILES[i%len(PROFILES)]) for i in range(count)]
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',default='moderate');a.add_argument('--count',type=int,default=5);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');args=a.parse_args();rows=batch(args.difficulty,args.count,args.seed);print(json.dumps(rows,indent=2) if args.format=='json' else '\n\n'.join(markdown(r) for r in rows))
