"""Easy: two 3x3 column additions, source-owned banks; no moderate/hard evidence.
Slots: matrix, target row, retained pivot column, integer multiples. No plots.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
from functools import lru_cache
KP_ID=17592186161968
KP_UUID='85e1fe3f-e85e-5ab4-a594-c55b84bb789a'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'column-zero-generator-v1'))
HERE=Path(__file__).with_suffix('')
SOURCES={q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
SUPPORTED_LEVELS=('easy',)
PROFILES=tuple(k for k in SOURCES if k != 'q-130614')
def recipes(profile,a,b):
 u=lambda z:1 if z>0 else -1
 return {
 'q-42917':[(-b,a),(a,-u(b)),(a,-b),(a,b),(b,a)],
 'q-91189':[(u(a),b),(-a,b),(a,b),(a,-b),(-b,-a)],
 'q-130609':[(a,b),(b,a),(-a,b),(a,-b),(-a,-b)],
 'q-130610':[(a,b),(-a,b),(-b,-a),(a,-b),(-a,-b)],
 'q-130611':[(b,a),(a,b),(-a,b),(a,-b),(-a,-b)],
 'q-91186':[(a*3,sp.Rational(b,3)),(a,b),(-a,b),(a,-b),(b,a)],
 'q-91187':[(a,-b),(a*3,sp.Rational(b,3)),(a,b),(-a,b),(b,a)],
 'q-91192':[(a,-b),(a,b),(b,a),(-a,b),(a*3,b)],
 'q-91188':[(a,-b),(1-a,-a),(-a,b),(b,a),(a,b)]}[profile]
def matrices(text):
 return [sp.Matrix([[int(v.strip()) for v in row.split('&')] for row in raw.split(r'\\')]) for raw in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def operations(text):
 text=re.sub(r'\s+','',text).replace('{C}','C').replace(r'\,','').replace('$','').replace(':&=',':=')
 return [(int(i)-1,int(p)-1,int((s or '+')+(n or '1'))) for i,j,s,n,p in re.findall(r'C_\{(\d)\}:=C_\{(\d)\}([+-]?)(\d*)C_\{(\d)\}',text) if i==j]
def source_parameters(q):
 A,B=matrices(q[':question/problem'])[:2]
 piv=[p for p in range(3) if A[:,p]==B[:,p]];assert len(piv)==1
 p=piv[0];cols=[c for c in range(3) if c!=p]
 rows=[r for r in range(3) if A[r,p]!=0 and all(A[r,c]!=0 and B[r,c]==0 for c in cols)];assert len(rows)==1
 r=rows[0];ks=[int(-A[r,c]/A[r,p]) if c!=p else 0 for c in range(3)]
 assert all(A[:,c]+ks[c]*A[:,p]==B[:,c] for c in cols)
 return {'A':A.tolist(),'row':r,'pivot':p,'ks':ks}
ORIGINAL={k:source_parameters(q) for k,q in SOURCES.items()}
def tex(M):return r'\begin{bmatrix}'+' \\\\ '.join(' & '.join(str(x) for x in row) for row in sp.Matrix(M).tolist())+r'\end{bmatrix}'
def op(c,p,k):return 'C_{'+str(c+1)+'}:=C_{'+str(c+1)+'}'+('+' if k>0 else '-')+('' if abs(k)==1 else str(abs(k)))+'C_{'+str(p+1)+'}'
def pair(cols,p,ks):return '$'+op(cols[0],p,ks[0])+'$ and $'+op(cols[1],p,ks[1])+'$'
def fingerprint(prompt):
 A,B=matrices(prompt)[:2];return hashlib.sha256(json.dumps([A.tolist(),B.tolist()],default=int).encode()).hexdigest()
def eligible(profile,a,b):
 bank=recipes(profile,a,b)
 return len(set(bank))==5 and bank.count((a,b))==1 and all(sp.sympify(k).is_integer and k!=0 for pair in bank for k in pair)
@lru_cache(None)
def anchor_banks(profile):
 # Every complete bank admits every key: reject at bank level, before selecting a key.
 out=[]
 for a in range(-9,10):
  for b in range(-9,10):
   if not a or not b or not eligible(profile,a,b):continue
   bank=tuple(tuple(int(k) for k in pair) for pair in recipes(profile,a,b))
   if all(abs(k)<=9 for pair in bank for k in pair):out.append(((a,b),bank))
 return tuple(out)
def generate(difficulty='easy',seed=0,template=None,parameters=None,bank_profile=None,bank_anchor=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty '+difficulty)
 rng=random.Random(seed);profile=bank_profile or template or rng.choice(PROFILES)
 if profile=='q-130614':profile='q-130609'
 replay=parameters is not None and any(parameters==pars and (key==profile or key=='q-130614' and profile=='q-130609') for key,pars in ORIGINAL.items())
 if parameters is None:
  if bank_anchor is None:anchor,bank=rng.choice(anchor_banks(profile))
  else:
   anchor=tuple(bank_anchor);bank=tuple(tuple(int(k) for k in pair) for pair in recipes(profile,*anchor))
   assert (anchor,bank) in anchor_banks(profile)
  coeff=rng.choice(bank)
  p=rng.randrange(3);r=rng.randrange(3);cols=[c for c in range(3) if c!=p]
  ks=[0]*3
  for c,k in zip(cols,coeff):ks[c]=k
  for _ in range(200):
   A=sp.Matrix(3,3,[rng.randint(-9,9) for _ in range(9)]);A[r,p]=rng.choice([-5,-3,-2,-1,1,2,3,5])
   for c in cols:A[r,c]=-ks[c]*A[r,p]
   if any(A[z,p]!=0 and all(A[z,c]+ks[c]*A[z,p]==0 for c in cols) for z in range(3) if z!=r):continue
   parameters={'A':A.tolist(),'row':r,'pivot':p,'ks':ks};break
  else:raise ValueError('Bounded sampler exhausted')
 else:
  coeff=tuple(parameters['ks'][c] for c in range(3) if c!=parameters['pivot'])
  if replay:
   anchor=coeff;bank=tuple(tuple(int(k) for k in pair) for pair in recipes(profile,*anchor))
  elif bank_anchor is not None:
   anchor=tuple(bank_anchor);bank=tuple(tuple(int(k) for k in pair) for pair in recipes(profile,*anchor))
   assert (anchor,bank) in anchor_banks(profile)
  else:
   compatible=[(anchor,bank) for anchor,bank in anchor_banks(profile) if coeff in bank]
   if not compatible:raise ValueError('No source-shaped integer bank for these coefficients')
   anchor,bank=rng.choice(compatible)
 parameters=json.loads(json.dumps(parameters,default=int));A=sp.Matrix(parameters['A']);r=parameters['row'];p=parameters['pivot'];ks=parameters['ks'];cols=[c for c in range(3) if c!=p]
 assert A.shape==(3,3) and 0<=r<3 and 0<=p<3 and A[r,p]!=0 and all(ks[c]!=0 and A[r,c]+ks[c]*A[r,p]==0 for c in cols)
 coeff=tuple(ks[c] for c in cols)
 assert len(set(bank))==5 and bank.count(coeff)==1
 bank=list(bank)
 B=A.copy();stages=[]
 for c in cols:B[:,c]=B[:,c]+ks[c]*B[:,p];stages.append(B.copy())
 prompt='$$\nA='+tex(A)+r',\,B='+tex(B)+'\n$$\n\nBy applying elementary column operations of the form $C_i:=C_i+kC_{'+str(p+1)+'},$ the matrix $A$ can be transformed into the matrix $B.$ What are the elementary column operations?'
 direction='to the left of' if p==2 else 'to the right of' if p==0 else 'to the left and to the right of'
 solution='To transform $A$ into $B,$ we need to make entries '+direction+' $a_{'+str(r+1)+str(p+1)+'}='+str(A[r,p])+'$ equal to $0.$\n\nTo do this, we can apply the following elementary column operations:\n\n$$\n'+r'\begin{aligned}A &='+tex(A)+'\n'+ '\n'.join(r'\\ &\xrightarrow{'+op(c,p,ks[c])+'}'+tex(stage) for c,stage in zip(cols,stages))+r'\\ &=B\end{aligned}'+'\n$$\n\nTherefore, the elementary column operations are\n\n'+pair(cols,p,coeff)+'.'
 fp=fingerprint(prompt);qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),fp+profile+json.dumps(bank)));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),str(k))),':answer/type':':answer.type/text',':answer/value':pair(cols,p,k)} for k in bank]
 question={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[bank.index(coeff)][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Using Column Operations to Create a Row of Zeros in a 3x3 Matrix'},'question':question,'generation':{'version':2,'bank_anchor':list(anchor),'bank_policy':'source-replay' if replay else 'bank-first-any-key','seed':seed,'template':'column-zero-3x3','bank_profile':profile,'parameters':parameters,'parameter_fingerprint':fp,'generator_id':GENERATOR_UUID,'sympy_version':sp.__version__}}
def batch(difficulty,count,seed):return [generate(difficulty,seed+i,bank_profile=PROFILES[i%len(PROFILES)]) for i in range(count)]
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',default='easy');a.add_argument('--count',type=int,default=5);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');args=a.parse_args();rows=batch(args.difficulty,args.count,args.seed);print(json.dumps(rows,indent=2) if args.format=='json' else '\n\n'.join(markdown(r) for r in rows))
