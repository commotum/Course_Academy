#!/usr/bin/env python3
"""Seeded, relocatable matrix recognition generator. Based on the supplied draft.

Only the source-evidenced easy band is offered. No external writes or assets.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as sp
from math_format import matrix_tex, normalize_prose, validate_generated_record
KP_ID=17592186087698
KP_UUID='7b6ddadb-471a-5195-a0f5-fd44bdc8f780'
TITLE='Identifying Other Matrices'
VERSION='matrix-recognition-package-2'
SOURCE=json.loads((Path(__file__).parent/'source.json').read_text())
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['material']['kp'][':knowledge-point/questions']}
LEVELS=('easy',);BOUNDS={'easy':(1,6)}
TEMPLATES=('classification','rows','columns','row_sets')
PROFILE_SOURCE={'row':'q-11563','diagonal':'q-126293','other':'q-7830','rows':'q-68751','columns':'q-126287','row_sets':'q-7831','legacy_other':'q-7836'}
PROFILE_TEMPLATE={p:('rows' if p=='rows' else 'columns' if p=='columns' else 'row_sets' if p=='row_sets' else 'classification') for p in PROFILE_SOURCE}
ALIASES={v:k for k,v in PROFILE_SOURCE.items()}
DEFAULT_PROFILES=tuple(PROFILE_SOURCE)
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
LABELS={'A row vector':'row','A column vector':'column','A column matrix':'column','A zero matrix':'zero','An identity matrix':'identity','A diagonal matrix':'diagonal','A square matrix':'square','Other':'other'}

def stable(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(x):return hashlib.sha256(stable(x).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),x))
def scalar(v):
 s=str(v)
 if re.fullmatch(r'-?\d+',s):return sp.Integer(s)
 m=re.fullmatch(r'(-?)\\sqrt\{([1-9]\d*)\}',s)
 if m:return (-1 if m[1] else 1)*sp.sqrt(int(m[2]))
 m=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{([1-9]\d*)\}',s)
 if m:return (-1 if m[1] else 1)*sp.Rational(int(m[2]),int(m[3]))
 raise ValueError('Exact integer, rational or numeric radical required')
def parse(prompt):return [[[v.strip() for v in row.split('&')] for row in match[1].split(r'\\')] for match in MATRIX.finditer(prompt)]
def predicates(m):
 a=[[scalar(x) for x in row] for row in m];r,c=len(a),len(a[0]);square=r==c
 zero=all(v==0 for row in a for v in row)
 diagonal=square and all(a[i][j]==0 for i in range(r) for j in range(c) if i!=j)
 identity=diagonal and all(a[i][i]==1 for i in range(r))
 return {'row':r==1,'column':c==1,'zero':zero,'square':square,'diagonal':diagonal,'identity':identity,'other':r>1 and c>1 and r!=c and not zero}
def best(m,bank):
 """Maximal true named predicate; incomparable overlaps reject the whole bank.
 Identity is narrower than diagonal/square; diagonal is narrower than square.
 Zero and row/column do not outrank each other. Singleton vector overlaps are
 never given arbitrary precedence. Other means none of the taught names apply.
 """
 props=predicates(m);true=[v for v in bank if props[LABELS[v]]]
 if any(LABELS[x]=='identity' for x in true):true=[x for x in true if LABELS[x] not in ('diagonal','square')]
 elif any(LABELS[x]=='diagonal' for x in true):true=[x for x in true if LABELS[x]!='square']
 if len(true)!=1:raise ValueError('Bank has absent or ambiguous best category')
 return true[0]
def source_parameters(sid):
 q=ORIGINALS[sid]
 text=q[':question/problem']
 if not parse(text):text='\n'.join(f[':answer-field/key'] for f in q[':question/answer-fields'])
 names=re.findall(r'([A-Z])\s*=\s*\\begin\{bmatrix\}',text)
 return {'names':names,'matrices':parse(text)}

def guard(p,t,profile,level):
 if set(p)!={'names','matrices'}:raise ValueError('Parameters require names and matrices')
 count=1 if t=='classification' else 3
 if len(p['names'])!=count or len(p['matrices'])!=count:raise ValueError('Source field-layout object count')
 if len(set(p['names']))!=count or any(not re.fullmatch('[A-Z]',n) for n in p['names']):raise ValueError('Distinct uppercase matrix names required')
 lo,hi=BOUNDS[level]
 for m in p['matrices']:
  if not isinstance(m,list) or not m or not all(isinstance(row,list) and row for row in m) or len(set(map(len,m)))!=1:raise ValueError('Nonempty rectangular matrix')
  r,c=len(m),len(m[0]);n=max(r,c)
  if not lo<=n<=hi:raise ValueError('Printed inspection-band bounds')
  for row in m:
   for x in row:
    if not isinstance(x,str):raise ValueError('Entry must be exact TeX string')
    if abs(scalar(x))>12:raise ValueError('Bounded familiar entries')
 if t=='classification':
  m=p['matrices'][0];r,c=len(m),len(m[0])
  if r==c==1 or ((r==1 or c==1) and predicates(m)['zero']):raise ValueError('Excluded overlapping singleton or zero-vector names')
  best(m,bank_values(p,profile)[0][2])
 if t=='row_sets':
  good=tuple(i for i,m in enumerate(p['matrices']) if len(m)==1)
  if good not in ((0,1),(0,2),(0,),(1,),(2,)):raise ValueError('Complete observed subset bank must represent the actual row subset')

def make_matrix(r,c,kind,rng):
 if kind=='zero':return [['0']*c for _ in range(r)]
 if kind=='identity':return [['1' if i==j else '0' for j in range(c)] for i in range(r)]
 if kind=='diagonal':
  # A single diagonal defect prevents a first-diagonal-entry shortcut.
  ds=['1']*r if rng.randrange(2) else [str(rng.randint(-12,12)) for _ in range(r)]
  ds[rng.randrange(r)]=str(rng.choice((-3,-2,-1,2,3)))
  return [[ds[i] if i==j else '0' for j in range(c)] for i in range(r)]
 pattern=rng.choice(('dense','sparse','identity_like')) if kind in ('square','other') else 'dense'
 if pattern=='sparse':
  m=[['0']*c for _ in range(r)]
  cells=[(i,j) for i in range(r) for j in range(c) if kind!='square' or i!=j]
  i,j=rng.choice(cells);m[i][j]=str(rng.choice((-3,-2,-1,1,2,3)))
 elif pattern=='identity_like':
  m=[['1' if i==j else '0' for j in range(c)] for i in range(r)]
  if kind=='square':
   i,j=rng.choice([(i,j) for i in range(r) for j in range(c) if i!=j]);m[i][j]=str(rng.choice((-3,-2,-1,1,2,3)))
 else:m=[[str(rng.randint(-12,12)) for _ in range(c)] for _ in range(r)]
 if not any(x!='0' for row in m for x in row):m[rng.randrange(r)][rng.randrange(c)]='2'
 if kind=='square' and not any(m[i][j]!='0' for i in range(r) for j in range(c) if i!=j):
  i,j=rng.choice([(i,j) for i in range(r) for j in range(c) if i!=j]);m[i][j]='2'
 return m

def sample(pf,level,rng):
 t=PROFILE_TEMPLATE[pf]
 def obj(kind):
  if kind=='singleton':return [[str(rng.randint(-12,12))]]
  k=rng.randint(2,6)
  if kind=='row':r,c=1,k
  elif kind=='column':r,c=k,1
  elif kind in ('square','diagonal','identity'):r=c=k
  else:
   r=k;c=rng.choice([v for v in range(2,7) if v!=r])
  return make_matrix(r,c,kind,rng)
 if t=='classification':
  # Every option in the chosen complete source bank is an eligible answer.
  kinds={'row':('row','column','identity','square','zero'),'diagonal':('diagonal','identity','row','column','other'),'other':('row','identity','square','zero','other'),'legacy_other':('row','column','identity','zero','other')}[pf]
  kind=rng.choice(kinds)
  return {'names':[rng.choice('AEFMPQ')],'matrices':[obj(kind)]}
 # Sample answer-bearing subset before any numerical/presentation parameters.
 good=rng.choice(((0,1),(0,2),(0,),(1,),(2,))) if t=='row_sets' else tuple(i for i in range(3) if rng.getrandbits(1))
 kinds=[]
 for i in range(3):
  if t=='columns':kinds.append(rng.choice(('column','singleton')) if i in good else rng.choice(('row','other','square','zero','diagonal','identity')))
  else:kinds.append(rng.choice(('row','singleton')) if i in good else rng.choice(('column','other','square','zero','diagonal','identity')))
 return {'names':rng.sample(list('EFG') if t=='row_sets' else list('ABC'),3),'matrices':[obj(k) for k in kinds]}

def bank_values(p,profile):
 t=PROFILE_TEMPLATE[profile];src=ORIGINALS[PROFILE_SOURCE[profile]]
 if t=='row_sets':
  names=p['names'];subsets=((0,1),(0,2),(0,),(2,),(1,))
  vals=[' and '.join('$'+names[i]+'$' for i in subset)+' only' for subset in subsets]
  good=tuple(i for i,m in enumerate(p['matrices']) if len(m)==1)
  answer=' and '.join('$'+names[i]+'$' for i in good)+' only'
  return [('selection',':answer-field.type/radio',vals,answer)]
 if t=='classification':
  f=src[':question/answer-fields'][0];vals=[a[':answer/value'] for a in f[':answer-field/choices']]
  return [('selection',':answer-field.type/radio',vals,best(p['matrices'][0],vals))]
 return [('$'+n+'='+matrix_tex(m)+'$',':answer-field.type/checkbox',['false','true'],str(len(m)==1 if t=='rows' else len(m[0])==1).lower()) for n,m in zip(p['names'],p['matrices'])]

def prompt(p,profile):
 src=ORIGINALS[PROFILE_SOURCE[profile]];text=src[':question/problem'];old=source_parameters(PROFILE_SOURCE[profile])['names']
 # Whole matrix and standalone-name slots; never blind entry replacement.
 idx=iter(range(len(p['matrices'])))
 text=MATRIX.sub(lambda m: '@MATRIX'+str(next(idx))+'@',text)
 for i,name in enumerate(old):text=re.sub(r'\b'+name+r'\b','@NAME'+str(i)+'@',text)
 for i,(name,arr) in enumerate(zip(p['names'],p['matrices'])):text=text.replace('@NAME'+str(i)+'@',name).replace('@MATRIX'+str(i)+'@',matrix_tex(arr))
 text=re.sub(r'\$([A-Z])\?\$',r'$\1$?',text)
 if PROFILE_TEMPLATE[profile] in ('rows','columns') and 'If none apply' not in text:text+=' If none apply, leave all boxes unchecked.'
 return normalize_prose(text)

def vector_solution(p,kind):
 lines=[];good=[]
 for name,m in zip(p['names'],p['matrices']):
  r,c=len(m),len(m[0]);v=kind+' vector'
  if (r==1 if kind=='row' else c==1):lines.append(f'- ${name}$ is a {v} since it has only one '+('row.' if kind=='row' else 'column.'));good.append(name)
  elif kind=='row' and c==1:lines.append(f"- ${name}$ is *not* a row vector. It has only one column (and ${r}$ rows), so it's a column vector.")
  elif kind=='column' and r==1:lines.append(f"- ${name}$ is *not* a column vector. It has only one row (and ${c}$ columns), so it's a row vector.")
  else:lines.append(f'- ${name}$ is *not* a {v}, since it has more than $1$ '+('row' if kind=='row' else 'column')+f' (it has ${r if kind=="row" else c}$ '+('rows' if kind=='row' else 'columns')+').')
 if len(good)==1:finish=f'Therefore, only ${good[0]}$ is a {v}.'
 elif not good:finish=f'Therefore, none of the matrices are {kind} vectors.'
 else:finish='Therefore, '+('only ' if len(good)<3 else '')+' and '.join('$'+n+'$' for n in good)+f' are {kind} vectors.'
 return normalize_prose('\n\n'.join(lines)+'\n\n'+finish)
def solution(p,pf,banks):
 if PROFILE_TEMPLATE[pf]!='classification':
  if pf=='row_sets':
   good=[n for n,m in zip(p['names'],p['matrices']) if len(m)==1]
   lines=[f'- ${n}$ is '+('a' if len(m)==1 else 'not a')+' row vector.' for n,m in zip(p['names'],p['matrices'])]
   return '\n\n'.join(lines)+'\n\nTherefore, '+' and '.join('$'+n+'$' for n in good)+(' satisfies' if len(good)==1 else ' satisfy')+' the definition.'
  return vector_solution(p,'column' if pf=='columns' else 'row')
 cat=LABELS[banks[0][3]];name=p['names'][0]
 if cat=='row':return 'The matrix has only one row. Hence, it is a row vector.'
 if cat=='column':return f'Notice that ${name}$ is a matrix that has a single column. Therefore, it is a column vector.'
 if cat=='diagonal':return "The matrix is square, all the entries that do not lie on the main diagonal are zeros, and the diagonal entries are not all ones. \n\nHence it's a diagonal matrix."
 if cat=='other':
  m=p['matrices'][0];return f'The matrix has ${len(m)}$ rows and ${len(m[0])}$ columns. It is rectangular, with more than one row and column, so none of the named special types apply.'
 if cat=='identity':return 'The matrix is square, all the entries that do not lie on the main diagonal are zeros, and the diagonal entries are all ones. \n\nHence it is an identity matrix.'
 if cat=='zero':return 'All the entries of the matrix are zeros. Hence, it is a zero matrix.'
 return 'The matrix has the same number of rows and columns. Hence, it is a square matrix.'

def semantic(p,t):
 # Ignore label/seed/entry magnitude and bank profile; preserve ordered evidence.
 if t in ('rows','row_sets','columns'):
  return {'task':'column_membership' if t=='columns' else 'row_membership','shapes':sorted([[len(m),len(m[0])] for m in p['matrices']])}
 m=p['matrices'][0];return {'task':'best_category','shape':[len(m),len(m[0])],'predicates':predicates(m)}

def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None,replay=False):
 if level not in LEVELS:raise ValueError('Unsupported difficulty: '+level)
 rng=random.Random(seed);pf=ALIASES.get(profile,profile)
 eligible=[x for x in DEFAULT_PROFILES if template is None or PROFILE_TEMPLATE[x]==template]
 if field_type is not None:eligible=[x for x in eligible if ('checkbox' if PROFILE_TEMPLATE[x] in ('rows','columns') else 'radio')==field_type.removeprefix(':answer-field.type/')]
 if pf is None:
  if not eligible:raise ValueError('Unsupported template/field')
  pf=rng.choice(eligible)
 if pf not in eligible:raise ValueError('Profile/template/field mismatch')
 t=PROFILE_TEMPLATE[pf];src=ORIGINALS[PROFILE_SOURCE[pf]]
 if replay:parameters=source_parameters(PROFILE_SOURCE[pf])
 p=copy.deepcopy(parameters) if parameters is not None else sample(pf,level,rng)
 guard(p,t,pf,level)
 banks=bank_values(p,pf)
 problem=prompt(p,pf);sol=normalize_prose(solution(p,pf,banks))
 if replay:
  problem=normalize_prose(re.sub(r'\$([A-Z])\?\$',r'$\1$?',src[':question/problem']))
  sol=normalize_prose(src[':question/worked-solution'])
 difficulty=src.get(':question/difficulty',{}).get(':db/ident') if replay else ':question.difficulty/'+level
 content={'version':VERSION,'level':difficulty,'prompt':problem,'solution':sol,'fields':[(k,typ,sorted(vals),good) for k,typ,vals,good in banks]}
 fp=digest(content);fields=[]
 for key,typ,vals,good in banks:
  if len(vals)!=len(set(vals)) or good not in vals:raise ValueError('Invalid complete bank')
  fid=uid(fp+'/field/'+key)
  answers=[{':answer/id':uid(fid+'/'+val),':answer/type':':answer.type/text',':answer/value':val} for val in vals]
  rng.shuffle(answers)
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':typ,':answer-field/choices':answers,':answer-field/correct':[':answer/id',uid(fid+'/'+good)]})
 q={':question/id':uid(fp),':question/problem':problem,':question/answer-fields':fields,':question/worked-solution':sol}
 if difficulty:q[':question/difficulty']=difficulty
 rec={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'level':level,'template':t,'profile':pf,'source_question':PROFILE_SOURCE[pf],'seed':seed,'parameters':p,'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'source_difficulty':src.get(':question/difficulty'),'replay':replay,'content_fingerprint':fp,'mathematical_fingerprint':digest(semantic(p,t)),'assessed_object':semantic(p,t),'sampling_attempts':1,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}
 validate_generated_record(rec)
 return rec

def batch(level,count,seed=0,template=None,profile=None,field_type=None):
 records=[];seen=set()
 for offset in range(max(2000,count*100)):
  rec=generate(level,seed+offset,template,field_type,profile=profile);fp=rec['generation']['mathematical_fingerprint']
  if fp in seen:continue
  seen.add(fp);records.append(rec)
  if len(records)==count:return records
 raise ValueError(f'Finite semantic domain exhausted after {len(records)} distinct tasks')


# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=LEVELS,default='easy');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=5);ap.add_argument('--template',choices=TEMPLATES);ap.add_argument('--profile');ap.add_argument('--field-type',choices=('radio','checkbox'));ap.add_argument('--format',choices=('json',),default='json');a=ap.parse_args()
 if a.count<1:ap.error('Positive count required')
 print(json.dumps(batch(a.difficulty,a.count,a.seed,a.template,a.profile,a.field_type),indent=2,ensure_ascii=False))
