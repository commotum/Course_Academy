#!/usr/bin/env python3
"""Isolated draft: classify matrices by shape and zero/one patterns.

Seven complete observed profiles; two missing-key originals are public raw
replays. Repaired profiles derive missing keys and solutions, without claiming
observed designations. E/M/H are bounded inspection bands (1–6 / 7–8 / 9–10),
not recovered MA ratings. All keep five-choice radio or three-checkbox layouts.
Exact scalar magnitude is presentation only; no linear algebra operations.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import matrix_tex, normalize_prose, validate_generated_record
KP_ID=17592186087698
KP_UUID='7b6ddadb-471a-5195-a0f5-fd44bdc8f780'
TITLE='Identifying Other Matrices'
VERSION='matrix-classification-isolated-draft-1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
LEVELS=('easy','moderate','hard');BOUNDS={'easy':(1,6),'moderate':(7,8),'hard':(9,10)}
TEMPLATES=('classification','rows','columns','row_sets')
PROFILE_SOURCE={'row':'q-11563','diagonal':'q-126293','other':'q-7830','rows':'q-68751','columns':'q-126287','row_sets_raw':'q-7831','legacy_other_raw':'q-7836','row_sets_repaired':'q-7831','legacy_other_repaired':'q-7836'}
PROFILE_TEMPLATE={'row':'classification','diagonal':'classification','other':'classification','rows':'rows','columns':'columns','row_sets_raw':'row_sets','legacy_other_raw':'classification','row_sets_repaired':'row_sets','legacy_other_repaired':'classification'}
ALIASES={**{v:k for k,v in PROFILE_SOURCE.items() if not k.endswith('repaired')},**{'observed-'+v:k for k,v in PROFILE_SOURCE.items() if not k.endswith('repaired')}}
DEFAULT_PROFILES=('row','diagonal','other','rows','columns','row_sets_repaired','legacy_other_repaired')
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
 q=ORIGINALS[sid];names=re.findall(r'([A-Z])\s*=\s*\\begin\{bmatrix\}',q[':question/problem'])
 return {'names':names,'matrices':parse(q[':question/problem'])}
def guard(p,t,profile,level):
 if set(p)!={'names','matrices'}:raise ValueError('Parameters require names and matrices')
 count=1 if t=='classification' else 3
 if len(p['names'])!=count or len(p['matrices'])!=count:raise ValueError('Source field-layout object count')
 if len(set(p['names']))!=count or any(not re.fullmatch('[A-Z]',n) for n in p['names']):raise ValueError('Distinct uppercase matrix names required')
 if t in ('rows','columns') and p['names']!=list('ABC'):raise ValueError('Checkbox field keys remain A, B, C')
 lo,hi=BOUNDS[level]
 for m in p['matrices']:
  if not isinstance(m,list) or not m or not all(isinstance(row,list) and row for row in m) or len(set(map(len,m)))!=1:raise ValueError('Nonempty rectangular matrix')
  r,c=len(m),len(m[0]);n=max(r,c)
  if not lo<=n<=hi:raise ValueError('Printed inspection-band bounds')
  for row in m:
   for x in row:
    if not isinstance(x,str):raise ValueError('Entry must be exact TeX string')
    if abs(scalar(x))>12:raise ValueError('Bounded familiar entries')
 if level!='easy' and t in ('rows','columns','row_sets'):
  counts=[len(m[0]) if t=='columns' else len(m) for m in p['matrices']]
  if all(n==1 for n in counts) or any(n!=1 and not lo<=n<=hi for n in counts):
   raise ValueError('Authored extended membership requires a longer negative count and every negative queried axis in band')
 if t=='classification':best(p['matrices'][0],bank_values(p,profile)[0][2])
 if t=='row_sets':
  good=tuple(i for i,m in enumerate(p['matrices']) if len(m)==1)
  if good not in ((0,1),(0,2),(0,),(1,),(2,)):raise ValueError('Complete observed subset bank must represent the actual row subset')

def make_matrix(r,c,kind,rng):
 m=[[str(rng.choice((-3,-2,-1,0,1,2,3))) for _ in range(c)] for _ in range(r)]
 if kind=='zero':return [['0']*c for _ in range(r)]
 if kind in ('diagonal','identity'):
  ds=['1']*r if kind=='identity' else [str(rng.choice((-2,-1,0,1,2))) for _ in range(r)]
  if kind=='diagonal':ds[rng.randrange(r)]='-1'
  return [[ds[i] if i==j else '0' for j in range(c)] for i in range(r)]
 # Dense square must remain non-diagonal; vector/general must stay nonzero.
 m[0][0]='2'
 if kind=='square':m[0][1]='1'
 return m

def sample(pf,level,rng):
 t=PROFILE_TEMPLATE[pf];lo,hi=BOUNDS[level];n=lambda:rng.randint(max(2,lo),hi)
 def obj(kind):
  if kind=='singleton':return [['0' if rng.randrange(2) else '1']]
  k=n()
  if kind=='row':r,c=1,k
  elif kind=='column':r,c=k,1
  elif kind in ('square','diagonal','identity'):r=c=k
  else:
   r,c=k,rng.randint(2,hi)
   if r==c:c=2 if r!=2 else 3
  return make_matrix(r,c,kind,rng)
 if t=='classification':
  kinds={'row':('row','column','identity','square','zero'),'diagonal':('diagonal','identity','row','column','other'),'other':('row','identity','square','zero','other'),'legacy_other_raw':('row','column','identity','zero','other'),'legacy_other_repaired':('row','column','identity','zero','other')}[pf]
  kind=rng.choice(kinds);return {'names':[rng.choice('AEFMPQ')],'matrices':[obj(kind)]}
 if t=='row_sets':
  good=rng.choice(((0,1),(0,2),(0,),(1,),(2,)))
  kinds=['row' if i in good else rng.choice(('column','other','square')) for i in range(3)]
  return {'names':list('EFG'),'matrices':[obj(k) for k in kinds]}
 kinds=['row','column','other','square','zero','diagonal','identity']+(['singleton'] if level=='easy' else [])
 ms=[obj(rng.choice(kinds)) for _ in range(3)]
 if level!='easy' and t=='columns':
  ms=[list(map(list,zip(*m))) if len(m[0])>1 and len(m[0])<lo else m for m in ms]
 return {'names':list('ABC'),'matrices':ms}

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
 return [(n,':answer-field.type/checkbox',['false','true'],str(len(m)==1 if t=='rows' else len(m[0])==1).lower()) for n,m in zip(p['names'],p['matrices'])]

def prompt(p,profile):
 src=ORIGINALS[PROFILE_SOURCE[profile]];text=src[':question/problem'];old=source_parameters(PROFILE_SOURCE[profile])['names']
 # Whole matrix and standalone-name slots; never blind entry replacement.
 idx=iter(range(len(p['matrices'])))
 text=MATRIX.sub(lambda m: '@MATRIX'+str(next(idx))+'@',text)
 for i,name in enumerate(old):text=re.sub(r'\b'+name+r'\b','@NAME'+str(i)+'@',text)
 for i,(name,arr) in enumerate(zip(p['names'],p['matrices'])):text=text.replace('@NAME'+str(i)+'@',name).replace('@MATRIX'+str(i)+'@',matrix_tex(arr))
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
 if PROFILE_TEMPLATE[pf]!='classification':return vector_solution(p,'column' if pf=='columns' else 'row')
 cat=LABELS[banks[0][3]];name=p['names'][0]
 if cat=='row':return 'The matrix has only one row. Hence, it is a row vector.'
 if cat=='column':return f'Notice that ${name}$ is a matrix that has a single column. Therefore, it is a column vector.'
 if cat=='diagonal':return "The matrix is square, all the entries that do not lie on the main diagonal are zeros, and the diagonal entries are not all ones. \n\nHence it's a diagonal matrix."
 if cat=='other':return 'The matrix has no special name.'
 if cat=='identity':return 'The matrix is square, all the entries that do not lie on the main diagonal are zeros, and the diagonal entries are all ones. \n\nHence it is an identity matrix.'
 if cat=='zero':return 'All the entries of the matrix are zeros. Hence, it is a zero matrix.'
 return 'The matrix has the same number of rows and columns. Hence, it is a square matrix.'

def semantic(p,t):
 # Entries matter only through equality to zero/one and categorical predicates.
 # Shape is the inspected object; labels/banks/seed/magnitudes are incidental.
 if t in ('rows','row_sets'):return {'task':'row_membership','objects':[{'rows':len(m),'one_column':len(m[0])==1} for m in p['matrices']]}
 if t=='columns':return {'task':'column_membership','objects':[{'columns':len(m[0]),'one_row':len(m)==1} for m in p['matrices']]}
 m=p['matrices'][0];return {'task':'best_category','shape':[len(m),len(m[0])],'predicates':predicates(m)}

def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('Unknown level')
 rng=random.Random(seed);pf=ALIASES.get(profile,profile)
 eligible=[x for x in DEFAULT_PROFILES if template is None or PROFILE_TEMPLATE[x]==template]
 if field_type is not None:eligible=[x for x in eligible if ('checkbox' if PROFILE_TEMPLATE[x] in ('rows','columns') else 'radio')==field_type.removeprefix(':answer-field.type/')]
 if pf is None:
  if not eligible:raise ValueError('Unknown template or unsupported field type')
  pf=rng.choice(eligible)
 if pf not in PROFILE_SOURCE:raise ValueError('Unknown complete bank profile')
 t=PROFILE_TEMPLATE[pf]
 if template is not None and t!=template:raise ValueError('Profile/template mismatch')
 kind='checkbox' if t in ('rows','columns') else 'radio'
 if field_type is not None and field_type.removeprefix(':answer-field.type/')!=kind:raise ValueError('Profile/field mismatch')
 # Complete bank is fixed BEFORE sampling; rejection never pools/replaces choices.
 if parameters is None:
  for attempt in range(1000):
   p=sample(pf,level,rng)
   try:guard(p,t,pf,level);break
   except ValueError:continue
  else:raise ValueError('Whole complete-bank domain exhausted')
 else:p=copy.deepcopy(parameters);guard(p,t,pf,level)
 banks=bank_values(p,pf);raw=pf.endswith('_raw');src=ORIGINALS[PROFILE_SOURCE[pf]]
 problem=prompt(p,pf);sol=normalize_prose(solution(p,pf,banks))
 content={'version':VERSION,'level':None if raw else level,'prompt':problem,'solution':None if raw else sol,'fields':[(k,typ,sorted(vals),None if raw else good) for k,typ,vals,good in banks]}
 fp=digest(content);fields=[]
 for key,typ,vals,good in banks:
  if len(vals)!=len(set(vals)) or good not in vals:raise ValueError('Complete bank invalid or missing correct value')
  fid=uid(fp+'/field/'+key);answers=[{':answer/id':uid(fid+'/'+val),':answer/type':':answer.type/text',':answer/value':val} for val in vals];rng.shuffle(answers)
  f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':typ,':answer-field/choices':answers}
  if not raw:f[':answer-field/correct']=[':answer/id',uid(fid+'/'+good)]
  fields.append(f)
 q={':question/id':uid(fp),':question/problem':problem,':question/answer-fields':fields}
 if not raw:q.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':sol})
 rec={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'draft_only':True,'level':level,'template':t,'profile':pf,'source_question':PROFILE_SOURCE[pf],'seed':seed,'parameters':p,'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'eligible_for_learning':not raw,'evidence_only':raw,'authored_level':level!='easy' or ':question/difficulty' not in src,'difficulty_uncertainty':'Authored inspection-size policy; no observed MA moderate/hard or unrated labels recovered.','derived_key':pf.endswith('_repaired'),'content_fingerprint':fp,'mathematical_fingerprint':digest(semantic(p,t)),'assessed_object':semantic(p,t),'banks':[{'key':k,'values':vals,'criterion':'all_true_membership' if typ.endswith('checkbox') else 'exact_subset' if t=='row_sets' else 'unique_maximal_true_category'} for k,typ,vals,g in banks],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}
 if raw:
  proxy=copy.deepcopy(rec);proxy['question'][':question/worked-solution']='';validate_generated_record(proxy);rec['generation']['math_format']=proxy['generation']['math_format']
 else:validate_generated_record(rec)
 return rec

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def batch(level,count,seed=0,template=None,profile=None,field_type=None):
 records=[];seen=set()
 for offset in range(max(2000,count*200)):
  rec=generate(level,seed+offset,template,field_type,profile=profile);fp=rec['generation']['mathematical_fingerprint']
  if fp in seen:continue
  seen.add(fp);records.append(rec)
  if len(records)==count:return records
 raise ValueError(f'Finite semantic domain exhausted after {len(records)} distinct tasks')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--template',choices=TEMPLATES);ap.add_argument('--profile');ap.add_argument('--field-type',choices=('radio','checkbox'));ap.add_argument('--format',choices=('json','markdown'),default='json');a=ap.parse_args()
 if a.count<1:ap.error('Positive count required')
 records=[r for level in (LEVELS if a.difficulty=='all' else (a.difficulty,)) for r in batch(level,a.count,a.seed,a.template,a.profile,a.field_type)]
 if a.format=='json':print(json.dumps(records,indent=2,ensure_ascii=False))
 else:print('\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+'\n'.join(f[":answer-field/key"]+': '+', '.join(x[':answer/value'] for x in f[':answer-field/choices']) for f in r['question'][':question/answer-fields'])+'\n\n'+r['question'].get(':question/worked-solution','[Original source has no solution or key.]') for r in records))
