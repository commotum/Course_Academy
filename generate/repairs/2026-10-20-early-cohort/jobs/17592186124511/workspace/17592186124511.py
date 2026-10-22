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
S = json.loads((HERE/'source-current.json').read_text())
KP_ID = 17592186124511
KP_UUID = S['record'][':knowledge-point/id']
VERSION = 'imt-2.1.0'
SOURCES = {q[':question/math-academy-id']:q for q in S['record'][':knowledge-point/questions']}
EXCLUDED = {'q-34936':'Missing correct answer and worked solution in supplied source.'}
TEMPLATES = tuple(t for t in SOURCES if t not in EXCLUDED)
MATRIX = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
SPEC = {
 'q-34834':('nullspace',5,1), 'q-141199':('vector',4,1),
 'q-141200':('det',6,0), 'q-142358':('nullspace',5,2),
 'q-142474':('nullspace',4,2), 'q-35425':('vector',5,1),
 'q-139977':('nullspace',4,1), 'q-79349':('det',5,0),
 'q-141201':('rank',4,0), 'q-34929':('vector',4,1),
 'q-141198':('det',5,0), 'q-141196':('nullspace',4,2),
 'q-142472':('det',3,0), 'q-142473':('det',4,0), 'q-141197':('col',5,0),
 'q-142367':('vector',4,1),
}

def source_choice(t,value):
 # Preserve the captured bank, correcting this documented Roman-numeral typo.
 return 'II only' if t=='q-142367' and value=='lI only' else value

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
 if kind in ('det','rank','col'):
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
 if kind in ('det','rank','col'):
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
 'q-142472':('not-invertible','rank-n','n-pivots'),
 'q-142473':('invertible','not-col-full','nullzero'),
 'q-141197':('invertible','rank-n','nullity-nonzero'),
 'q-142367':('nullity-nonzero','invertible','col-full'),
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

def _field(qid,key,values,correct,kind):
 fid=ident(qid,'field:'+key)
 return {':answer-field/id':fid,':answer-field/key':key,':answer-field/type':kind,
         ':answer-field/choices':[{':answer/id':ident(fid,'answer:'+v),':answer/type':':answer.type/text',':answer/value':v} for v in values],
         ':answer-field/correct':[':answer/id',ident(fid,'answer:'+correct)]}

def _record(t,p,seed,prompt,solution,definitions,replay):
 canonical_fields=sorted((key,sorted(values),correct,kind) for key,values,correct,kind in definitions)
 qid=ident(KP_UUID,VERSION+':'+digest([prompt,solution,canonical_fields]))
 fs=[_field(qid,*d) for d in definitions]
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,
    ':question/difficulty':':question.difficulty/moderate',':question/answer-fields':fs}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':S['record'][':knowledge-point/title']},
         'question':q,'generation':{'version':VERSION,'seed':seed,'template':t,'profile':t,'parameters':p,
         'replay':replay,'source':SOURCES[t][':db/id'],'source_basis':S['basis'],
         'dependency_versions':{'sympy':sp.__version__},'mathematical_fingerprint':fingerprint(q),'assets':[]}}

def fingerprint(q):
 # Canonicalize givens, discard choice order and source identity, include all claims.
 text=q[':question/problem'];head=text.split('I.')[0].split('Select all')[0]
 mats=MATRIX.findall(head)
 if mats:
  raw=mats[0].split(r'\\');xs=sp.symbols('x1 x2');a=[]
  for row in raw:
   v=sp.sympify(re.sub(r'(\d)(x)',r'\1*\2',re.sub(r'\{x\}_\{([12])\}',r'x\1',row.strip())))
   a.append([v.coeff(x) for x in xs] if v.free_symbols else [v])
  # Numeric zeros in a symbolic column still need the common width.
  if any('x' in row for row in raw):
   a=[]
   for row in raw:
    v=sp.sympify(re.sub(r'(\d)(x)',r'\1*\2',re.sub(r'\{x\}_\{([12])\}',r'x\1',row.strip())))
    a.append([v.coeff(x) for x in xs])
  canonical=str(sp.Matrix(a).T.rref()[0].tolist())
  head=MATRIX.sub(canonical,head)
 head=re.sub(r'det\(A\)=(-?\d+)',lambda m:'det(A)='+('zero' if int(m[1])==0 else 'nonzero'),head)
 claims=re.findall(r'(?:^|\n)(?:III|II|I)\. ([^\n]+)',text)
 if not claims:claims=[f[':answer-field/key'] for f in q[':question/answer-fields']]
 return digest([re.sub(r'\s','',head),sorted(re.sub(r'\s','',c) for c in claims)])

def _facts(t,p):
 kind,_,_=SPEC[t];n=p['n']
 if kind=='nullspace':k=sp.Matrix(p['matrix']).rank();return False,n-k,k
 if kind=='vector':return False,None,None
 if kind=='det':return (True,n,0) if p['det'] else (False,None,None)
 return True,n,0

def claim_pool(role,n,inv,rank,k):
 # All proposed comparisons are determined by the supplied evidence.
 if role in ('invertible','not-invertible'):
  return [(r'A\text{ is invertible}',inv),(r'A\text{ is not invertible}',not inv)]
 if role in ('nullzero',):
  return [(r'\text{Null}(A)'+op+r'\{0\}', inv if op=='=' else not inv) for op in ('=',r'\ne ')]
 if role in ('col-full','not-col-full','col-zero'):
  return [(r'\text{Col}(A)'+op+'{R}^{'+str(n)+'}',inv if op=='=' else not inv) for op in ('=',r'\ne ')]
 if role=='n-pivots':
  # In singular cases only n pivots can be decided, and negation supplies its complement.
  return [(r'A\text{ has }'+str(n)+r'\text{ pivot columns}',inv),(r'A\text{ does not have }'+str(n)+r'\text{ pivot columns}',not inv)]
 if role.startswith('rank-'):
  pool=[(r'\text{rank}(A)='+str(n),inv),(r'\text{rank}(A)\ne '+str(n),not inv),(r'\text{rank}(A)<'+str(n),not inv)]
  if rank is not None:pool.extend((r'\text{rank}(A)='+str(v),rank==v) for v in (n-1,n+1))
  return pool
 # Nullity comparisons: known k supports numerical claims; unknown k only zero/nonzero.
 values=sorted({0,1,n,k} - {None}) if k is not None else [0]
 return [(r'\text{dim(Null}(A))'+op+str(v), (k==v if k is not None else inv) if op=='=' else (k!=v if k is not None else not inv)) for v in values for op in ('=',r'\ne ')]

def generate(difficulty='moderate',seed=0,template=None,parameters=None,replay=False):
 if difficulty!='moderate':raise ValueError('Unsupported difficulty: '+difficulty)
 rng=random.Random(seed);t=template or rng.choice(TEMPLATES)
 if t not in TEMPLATES:raise ValueError('Unsupported template: '+t)
 source=SOURCES[t];kind,n,k=SPEC[t]
 if replay:
  p=original(t) if parameters is None else parameters
  if p!=original(t):raise ValueError('Replay requires original parameters')
  ds=[]
  for f in source[':question/answer-fields']:
   ds.append((f[':answer-field/key'],[source_choice(t,a[':answer/value']) for a in f[':answer-field/choices']],source_choice(t,f[':answer-field/correct'][':answer/value']),f[':answer-field/type'][':db/ident']))
  return _record(t,p,seed,source[':question/problem'],source[':question/worked-solution'],ds,True)
 isradio=source[':question/answer-fields'][0][':answer-field/type'][':db/ident'].endswith('/radio')
 hasnone=any(f[':answer-field/key']=='None of the above' for f in source[':question/answer-fields'])
 bank=[source_choice(t,a[':answer/value']) for a in source[':question/answer-fields'][0][':answer-field/choices']] if isradio else None
 if parameters is None:
  # Choose decision assignment before compatible givens and statement relations.
  if isradio:
   target=rng.choice(bank);mask=[label in target.split(' only')[0].split(' and ') for label in ('I','II','III')]
  else:
   bits=rng.randint(0 if hasnone else 1,7);mask=[bool(bits&(1<<j)) for j in range(3)]
  p=sample(t,rng)
  if kind=='det':p['det']=rng.choice([0,-4,-1,1,3])
  if kind=='nullspace':
   # Coordinate assignment is incidental; preserve immediate independence/counting.
   rng.shuffle(p['matrix'])
  inv,rank,nullity=_facts(t,p)
  p['claims']=[rng.choice([text for text,b in claim_pool(c,p['n'],inv,rank,nullity) if bool(b)==mask[i]]) for i,c in enumerate(CLAIMS[t])]
 else:
  p=json.loads(json.dumps(parameters));inv,rank,nullity=_facts(t,p)
  if 'claims' not in p:raise ValueError('Explicit parameters require three visible claims')
  mask=[]
  for c,text in zip(CLAIMS[t],p['claims']):
   matches=[b for txt,b in claim_pool(c,p['n'],inv,rank,nullity) if txt==text]
   if len(matches)!=1:raise ValueError('Undetermined or unsupported claim: '+text)
   mask.append(bool(matches[0]))
 if len(p['claims'])!=3:raise ValueError('Three claims required')
 if type(p['n']) is not int or not 3<=p['n']<=7:raise ValueError('Dimension outside domain')
 if kind in ('vector','nullspace'):
  a=sp.Matrix(p['matrix'])
  if a.shape!=(n,k) or a.rank()!=k or p['n']!=n:raise ValueError('Invalid nonzero independent vector data')
  if any(type(v) is not int or not -4<=v<=4 for row in p['matrix'] for v in row):raise ValueError('Coefficient outside domain')
 if kind=='det' and (type(p['det']) is not int or not -4<=p['det']<=4):raise ValueError('Determinant outside domain')
 inv,rank,nullity=_facts(t,p);n=p['n'];claims=p['claims'];ds=[]
 target=correct_subset(mask) if any(mask) else 'None of the above'
 if isradio and target not in bank:raise ValueError('Subset absent from complete source bank')
 if not isradio and not any(mask) and not hasnone:raise ValueError('No correct selectable option')
 if kind=='vector':given='$v='+numeric_matrix([r[0] for r in p['matrix']])+r'$ is a solution of $Ax=0$'
 elif kind=='nullspace':given='$$\n'+r'\text{Null}(A)=\{'+symbolic_matrix(p['matrix'])+r'\mid '+','.join('{x}_{'+str(j+1)+'}' for j in range(k))+r'\in\mathbb{R}\}?'+ '\n$$'
 elif kind=='det':given='$det(A)='+str(p['det'])+'$'
 elif kind=='rank':given=r'$\text{rank}(A)='+str(n)+'$'
 else:given=r'$\text{Col}(A)={R}^{'+str(n)+'}$'
 prompt='Which of the following statements are true, given that $A$ is a $'+str(n)+r'\times '+str(n)+'$ matrix and '+given+('' if kind=='nullspace' else '?')
 if isradio:
  prompt+='\n\n'+'\n\n'.join(label+'. $'+c+'$' for label,c in zip(('I','II','III'),claims))
  values=bank[:];rng.shuffle(values);ds=[('selection',values,target,':answer-field.type/radio')]
 else:
  prompt+='\n\nSelect all that apply.'
  ds=[('$'+c+'$',['false','true'],str(b).lower(),':answer-field.type/checkbox') for c,b in zip(claims,mask)]
  rng.shuffle(ds)
  if hasnone:ds.append(('None of the above',['false','true'],str(not any(mask)).lower(),':answer-field.type/checkbox'))
 theorem=(r'$$ A\text{ is invertible}\quad\Longleftrightarrow\quad\left\{\begin{aligned}'
          +r'\text{Col}(A)&=\mathbb{R}^{'+str(n)+r'} \\ \text{rank}(A)&='+str(n)
          +r' \\ \text{Null}(A)&=\{0\} \\ \text{nullity}(A)&=0\end{aligned}\right. $$')
 solution='Since $A$ is a $'+str(n)+r'\times '+str(n)+'$ matrix, the invertible matrix theorem states the following:\n\n'+theorem+'\n\n'
 if kind=='nullspace':
  basis=' + '.join('{x}_{'+str(j+1)+'}'+numeric_matrix([row[j] for row in p['matrix']]) for j in range(k))
  solution+='The supplied nullspace can be written as the span of the independent vectors in\n\n$$'+basis+'$$\n\nHence '+r'$\text{dim(Null}(A))='+str(k)+'$, so $A$ is not invertible.\n\n'
 elif kind=='vector':solution+=r'Since $v\ne 0$ and $Av=0$, the nullspace contains a nonzero vector. Thus $A$ is not invertible. This does not determine its exact rank or nullity.'+'\n\n'
 elif kind=='det':solution+='$det(A)='+str(p['det'])+'$, so $A$ is '+('invertible' if inv else 'not invertible')+'.\n\n'
 else:solution+='The given full '+('rank' if kind=='rank' else 'column space')+' implies that $A$ is invertible.\n\n'
 consequence=(r'We have $\text{rank}(A)='+str(n)+r'$, $\text{nullity}(A)=0$, $\text{Null}(A)=\{0\}$, and $\text{Col}(A)=\mathbb{R}^{'+str(n)+'}$.' if inv else r'We have $\text{rank}(A)<'+str(n)+r'$, $\text{nullity}(A)>0$, $\text{Null}(A)\ne\{0\}$, and $\text{Col}(A)\ne\mathbb{R}^{'+str(n)+'}$.')
 if kind=='nullspace':consequence+=' In particular, '+r'$\text{rank}(A)='+str(rank)+r'$ and $\text{nullity}(A)='+str(nullity)+'$.'
 solution+=consequence+"\n\nWith that in mind, let's examine each statement in turn.\n\n"
 for label,c,b,role in zip(('I','II','III'),claims,mask,CLAIMS[t]):
  if role in ('invertible','not-invertible'):reason='$A$ is '+('invertible' if inv else 'not invertible')+'.'
  elif role=='nullzero':reason=r'$\text{Null}(A)'+('=' if inv else r'\ne ')+r'\{0\}$.'
  elif role in ('col-full','not-col-full','col-zero'):reason=r'$\text{Col}(A)'+('=' if inv else r'\ne ')+r'\mathbb{R}^{'+str(n)+'}$.'
  elif role.startswith('rank-') or role=='n-pivots':reason=r'$\text{rank}(A)'+('='+str(rank) if rank is not None else '<'+str(n))+'$; the rank counts pivot columns.'
  else:reason=r'$\text{nullity}(A)'+('='+str(nullity) if nullity is not None else '>0')+'$.'
  judgment=('- Statement '+label+' is '+str(b).lower()+': $'+c+'$.' if isradio else '- Statement $'+c+'$ is '+str(b).lower()+'.')
  solution+=judgment+' '+reason+'\n\n'

 displayed_target=target if isradio or not any(mask) else '; '.join('$'+c+'$' for c,b in zip(claims,mask) if b)+' only'
 solution+='Therefore, the correct answer is '+displayed_target+'.'
 return _record(t,p,seed,prompt,solution,ds,False)

def _batch_records(difficulty,count,seed,order):
 if difficulty!='moderate':raise ValueError('Unsupported difficulty: '+difficulty)
 if count<1:raise ValueError('count must be positive')
 found=[];used=set();checkbox_counts={};radio_subsets=set();radio_positions=set()
 for offset in range(max(200,50*count)):
  # Rejection resamples the same profile, preserving source-family reachability.
  r=generate(difficulty,seed+offset,order[len(found)%len(order)]);fp=r['generation']['mathematical_fingerprint']
  if fp in used:continue
  fs=r['question'][':question/answer-fields']
  if fs[0][':answer-field/type'].endswith('/checkbox'):
   group=len(fs)
   selected=sum(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])=='true' for f in fs)
   seen=checkbox_counts.setdefault(group,set())
   if selected in seen:continue
   seen.add(selected)
   if seen=={1,2,3}:seen.clear()
  else:
   f=fs[0];choices=f[':answer-field/choices']
   key=next(a[':answer/value'] for a in choices if a[':answer/id']==f[':answer-field/correct'][1])
   position=next(i for i,a in enumerate(choices) if a[':answer/id']==f[':answer-field/correct'][1])
   if {a[':answer/value'] for a in choices}<=radio_subsets:radio_subsets.clear()
   if len(radio_positions)==5:radio_positions.clear()
   if key in radio_subsets or position in radio_positions:continue
   radio_subsets.add(key);radio_positions.add(position)
  found.append(r);used.add(fp)
  if len(found)==count:return found
 raise ValueError('Finite sampling capability: '+str(len(found))+' distinct tasks found; requested '+str(count))
def batch(difficulty,count,seed):
 order=list(TEMPLATES);random.Random(seed).shuffle(order)
 return _batch_records(difficulty,count,seed,order)
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

# Bundle the shared policy, with source-backed None already constructed explicitly.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ('batch','generate'):
 globals()[_policy_name]=_nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':main()
