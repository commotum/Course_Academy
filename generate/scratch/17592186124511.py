#!/usr/bin/env python3
"""Invertible matrix theorem: source-faithful moderate radio/checkbox templates.

Easy and hard have no validated source-backed templates in this package.
Stable IDs depend on mathematical content, never on seed or answer ordering.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import uuid
import sympy as sp

HERE = Path(__file__).with_suffix('')
S = json.loads((HERE/'source.json').read_text())
KP_ID = 17592186124511
KP_UUID = S['record'][':knowledge-point/id']
VERSION = 'imt-1.0.0'
SOURCES = {q[':question/math-academy-id']:q for q in S['record'][':knowledge-point/questions']}
EXCLUDED = {'q-34936':'Unrated, absent canonical answer and solution.',
            'q-142367':'Malformed radio label lI only; intended subset is unresolved. Preserved but excluded.'}
TEMPLATES = tuple(t for t in SOURCES if t not in EXCLUDED)
MATRIX = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
SPEC = {
 'q-34834':('nullspace',5,1), 'q-141199':('vector',4,1),
 'q-141200':('det',6,0), 'q-142358':('nullspace',5,2),
 'q-142474':('nullspace',4,2), 'q-35425':('vector',5,1),
 'q-139977':('nullspace',4,1), 'q-79349':('det',5,0),
 'q-141201':('rank',4,0), 'q-34929':('vector',4,1),
 'q-141198':('det',5,0), 'q-141196':('nullspace',4,2),
}

def digest(obj):
 return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(namespace, value):return str(uuid.uuid5(uuid.UUID(namespace),value))
def coeffs(t):
 text=MATRIX.findall(SOURCES[t][':question/problem'])[0]
 rows=text.split(r'\\');k=SPEC[t][2];out=[]
 for row in rows:
  if '{x}' in row:
   row=re.sub(r'\{x\}_\{([12])\}',r'x\1',row.strip())
   row=re.sub(r'(\d)(x)',r'\1*\2',row)
   expr=sp.sympify(row)
   out.append([int(expr.coeff(sp.Symbol('x'+str(j+1)))) for j in range(k)])
  else:out.append([int(row.strip())]+[0]*(k-1))
 return out
def original(t):
 kind,n,k=SPEC[t];p={'n':n}
 if kind in ('vector','nullspace'):p['matrix']=coeffs(t)
 elif kind=='det':p['det']=int(re.search(r'det\(A\)=(-?\d+)',SOURCES[t][':question/problem'])[1])
 return p

def sample(t,rng):
 kind,n,k=SPEC[t];p=original(t)
 if kind in ('det','rank'):
  p['n']=rng.randint(3,7)
  if kind=='det' and p['det']!=0:p['det']=rng.choice([-4,-3,-2,-1,1,2,3,4])
 else:
  a=p['matrix']
  if kind=='vector':
   while True:
    a=[[rng.randint(-4,4)] for _ in range(n)]
    if any(row[0] for row in a):break
  else:
   # Original zero pattern and number of free parameters stay fixed.
   # Disjoint, nonempty column supports preserve independence.
   a=[[rng.choice([-4,-3,-2,-1,1,2,3,4]) if c else 0 for c in row] for row in a]
  p['matrix']=a
 return p

def numeric_matrix(a):
 return r'\begin{bmatrix}'+r' \\ '.join(str(x) for x in a)+r'\end{bmatrix}'
def symbolic_matrix(a):
 def term(c,j):
  x='{x}_{'+str(j+1)+'}'
  return x if c==1 else '-'+x if c==-1 else str(c)+x
 def row(v):
  terms=[term(c,j) for j,c in enumerate(v) if c]
  return '+'.join(terms).replace('+-','-') if terms else '0'
 return r'\begin{bmatrix}'+r' \\ '.join(row(v) for v in a)+r'\end{bmatrix}'

def render(t,p,text):
 kind,oldn,k=SPEC[t]
 if kind in ('vector','nullspace'):
  old=original(t)['matrix'];a=p['matrix']
  replacements={}
  if kind=='vector':replacements[numeric_matrix([r[0] for r in old])]=numeric_matrix([r[0] for r in a])
  else:
   replacements[symbolic_matrix(old)]=symbolic_matrix(a)
   for j in range(k):replacements[numeric_matrix([r[j] for r in old])]=numeric_matrix([r[j] for r in a])
  for i,(old,new) in enumerate(replacements.items()):text=text.replace(old,'@@M'+str(i)+'@@')
  for i,new in enumerate(replacements.values()):text=text.replace('@@M'+str(i)+'@@',new)
 else:
  if kind=='det':
   oldd=original(t)['det'];text=text.replace('det(A)='+str(oldd),'det(A)=@@DET@@')
  # The n-1 rank claim of q-79349 is a dependent slot, not a fixed 4.
  if t=='q-79349':text=re.sub(r'(?<!\d)4(?!\d)','@@NM1@@',text)
  text=re.sub(r'(?<!\d)'+str(oldn)+r'(?!\d)',str(p['n']),text)
  text=text.replace('@@NM1@@',str(p['n']-1)).replace('@@DET@@',str(p.get('det',0)))
 return text

def domain(t,p):
 kind,n,k=SPEC[t];assert type(p['n']) is int
 if kind in ('det','rank'):
  assert 3<=p['n']<=7
  if kind=='det':assert p['det']==0 if original(t)['det']==0 else p['det'] in [-4,-3,-2,-1,1,2,3,4]
 else:
  assert p['n']==n
  a=sp.Matrix(p['matrix']);assert a.shape==(n,k) and a.rank()==k
  assert all(type(v) is int and -4<=v<=4 for row in p['matrix'] for v in row)
  if kind=='nullspace':assert [[v!=0 for v in row] for row in p['matrix']]==[[v!=0 for v in row] for row in original(t)['matrix']]

def semantic(q):
 """Normalize equivalent given subspaces, sign/magnitude-only determinant changes,
 matrix symbols, statement order, and radio/checkbox layout out of deduplication.
 Ambient dimension and genuinely different given subspaces remain significant.
 """
 text=q[':question/problem']
 if '![](images/6a/6a294de4a5f2ff5755d8ceb5b91bb8920685a1cf2b5e727c5b5fdcfaaf0b89b0.svg)' in text:
  text=text.replace('![](images/6a/6a294de4a5f2ff5755d8ceb5b91bb8920685a1cf2b5e727c5b5fdcfaaf0b89b0.svg)',r'\text{Null}(A)=\{'+symbolic_matrix([[1],[2],[0],[-1]])+r'\,|\,{x}_{1}\in R\}')
 nmatch=re.search(r'(\d+)\s*\\(?:times|cdot)\s*(\d+)',text);n=int(nmatch[1])
 head=text.split('I.')[0].split('- **I.**')[0]
 mats=MATRIX.findall(head)
 if mats:
  raw=mats[0].split(r'\\');k=2 if '{x}_{2}' in mats[0] else 1
  if '{x}' in mats[0]:
   a=[]
   for row in raw:
    row=re.sub(r'\{x\}_\{([12])\}',r'x\1',row.strip());row=re.sub(r'(\d)(x)',r'\1*\2',row)
    expr=sp.sympify(row);a.append([expr.coeff(sp.Symbol('x'+str(j+1))) for j in range(k)])
   kind='nullspace'
  else:a=[[int(row.strip())] for row in raw];kind='vector'
  canonical=[[str(v) for v in row] for row in sp.Matrix(a).T.rref()[0].tolist()]
  given=[kind,n,canonical]
 elif 'det(A)' in head:given=['det',n,int(re.search(r'det\(A\)=(-?\d+)',head)[1])==0]
 elif 'rank' in head:given=['rank',n,n]
 else:given=['col',n,'full']
 # Operative statements in source order are identified before normalizing order.
 statements=re.findall(r'(?:\*\*(?:I|II|III)\.\*\*|(?<![A-Z])(?:III|II|I)\.|(?m:^)[123]\.)\s*([^\n]+)',text)
 def norm(s):return re.sub(r'[\s${}\\]','',s).replace('text','').replace('textrm','').replace('R^','R')
 return digest([given,sorted(norm(s) for s in statements)])
fingerprint=semantic

CLAIMS = {
 'q-34834':('nullity0','not-invertible','rank-n'),
 'q-141199':('nullzero','not-invertible','not-col-full'),
 'q-141200':('invertible','nullzero','nullity-n'),
 'q-142358':('nullity0','invertible','not-col-full'),
 'q-142474':('nullity1','invertible','rank-below-n'),
 'q-35425':('nullity0','invertible','rank-not-n'),
 'q-139977':('nullity1','invertible','rank-below-n'),
 'q-79349':('not-invertible','rank-n-minus1','n-pivots'),
 'q-141201':('invertible','col-zero','nullity0'),
 'q-34929':('nullity-nonzero','invertible','rank-n'),
 'q-141198':('not-invertible','rank-not-n','nullzero'),
 'q-141196':('nullity-nonzero','invertible','col-full'),
}
def compute_truths(t,p):
 kind,_,_=SPEC[t];n=p['n'];rank=nullity=None
 if kind=='nullspace':nullity=sp.Matrix(p['matrix']).rank();rank=n-nullity;inv=nullity==0
 elif kind=='vector':assert sp.Matrix(p['matrix']).rank()==1;inv=False
 elif kind=='det':inv=p['det']!=0;rank=n if inv else None;nullity=0 if inv else None
 else:rank=n;nullity=0;inv=True
 values={'invertible':inv,'not-invertible':not inv,'nullzero':inv,'col-full':inv,'not-col-full':not inv,
         'rank-n':inv,'rank-not-n':not inv,'rank-below-n':not inv,'nullity0':inv,'nullity-nonzero':not inv,
         'nullity1':nullity==1,'nullity-n':nullity==n,'rank-n-minus1':rank==n-1,'n-pivots':rank==n,'col-zero':rank==0}
 return [bool(values[c]) for c in CLAIMS[t]]

def correct_subset(truths):
 return ' and '.join(k for k,b in zip(('I','II','III'),truths) if b)+' only'

def generate(difficulty='moderate',seed=0,template=None,parameters=None,replay=False):
 if difficulty!='moderate':raise ValueError('Unsupported difficulty: '+difficulty+'; no validated source-backed template')
 rng=random.Random(seed);t=template or rng.choice(TEMPLATES);assert t in TEMPLATES
 p=parameters if parameters is not None else sample(t,rng);domain(t,p)
 truths=compute_truths(t,p)
 source=SOURCES[t];prompt=render(t,p,source[':question/problem']);solution=render(t,p,source[':question/worked-solution'])
 # At original parameters this preserves every instructional sentence and bank.
 proto={':question/problem':prompt};fp=semantic(proto)
 qid=ident(KP_UUID,VERSION+':'+digest([t,prompt,solution]));fields=[]
 for sf in source[':question/answer-fields']:
  key=sf[':answer-field/key'];fid=ident(qid,'field:'+key);answers=[]
  for sa in sf[':answer-field/choices']:
   value=sa[':answer/value'];aid=ident(fid,'answer:'+value)
   answers.append({':answer/id':aid,':answer/type':':answer.type/text',':answer/value':value})
  correct=str(truths[('I','II','III').index(key)]).lower() if sf[':answer-field/type'][':db/ident'].endswith('/checkbox') else correct_subset(truths)
  assert correct in [a[':answer/value'] for a in answers]
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':sf[':answer-field/type'][':db/ident'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',ident(fid,'answer:'+correct)]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':S['record'][':knowledge-point/title']},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':t,'profile':t,'parameters':p,'replay':replay,'source':source[':db/id'],'source_basis':S['basis'],'dependency_versions':{'sympy':sp.__version__},'mathematical_fingerprint':fp,'assets':[]}}

def batch(difficulty,count,seed):
 if difficulty!='moderate':raise ValueError('Unsupported difficulty: '+difficulty)
 if count<1:raise ValueError('count must be positive')
 found=[];used=set()
 for offset in range(max(200,50*count)):
  r=generate(difficulty,seed+offset,TEMPLATES[offset%len(TEMPLATES)]);fp=r['generation']['mathematical_fingerprint']
  if fp not in used:found.append(r);used.add(fp)
  if len(found)==count:return found
 raise ValueError('Finite sampling capability: '+str(len(found))+' distinct tasks found; requested '+str(count))
def markdown(r):
 q=r['question'];text=q[':question/problem']+'\n\n'
 for f in q[':question/answer-fields']:
  text+='Field '+f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices'])+'\n'
 return text+'\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='moderate');ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');args=ap.parse_args()
 try:records=batch(args.difficulty,args.count,args.seed)
 except ValueError as e:ap.exit(2,str(e)+'\n')
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__=='__main__':main()
