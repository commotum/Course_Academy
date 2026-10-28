#!/usr/bin/env python3
"""Seeded conformable matrix products. Ordinary matrices; no database operations.

Backbone: dimension/conformability statement, ordered row-column dot products,
progressive result matrices, conclusion. Complete bank selected before parameters.
Historical opaque banks are source-replay evidence profiles, never defaults.
All normal sampling and explicit inputs use the same coupled arithmetic guards.
"""
import sys
sys.dont_write_bytecode = True
import argparse,copy,hashlib,json,random,re,uuid,itertools
from pathlib import Path
import sympy as sp
import math_format as mf
from product_highlights import product_solution
D=Path(__file__).resolve().parent; SPECS=json.loads((D/'replay-specifications.json').read_text())
VERSION='9047-matrix-product-highlights-3'; KP={'db_id':17592186100872,'id':'92dd864a-8bc0-547c-84c9-ffd562909315','title':'Multiplying Two Matrices When They Are Conformable'}
PROFILES=('two-sum-error','observed-raw','observed-repaired')

def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'))
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+canonical(v)))
def sha(v):return hashlib.sha256(canonical(v).encode()).hexdigest()
def mat(v):return mf.matrix_tex(v,augmented=False)
def mul(a,b):return [list(map(int,row)) for row in (sp.Matrix(a)*sp.Matrix(b)).tolist()]
def factor(x):return '('+str(x)+')' if x<0 else str(x)
def dot(a,b,i,j):return '+'.join(factor(a[i][k])+r'\cdot '+factor(b[k][j]) for k in range(len(b)))
def recipe(r,a,b,c):
 def atom(z):
  if z[0]=='dot':return c[z[1]][z[2]]
  if z[0]=='product':return a[z[1]][z[2]]*b[z[2]][z[3]]
  return (a if z[0]=='A' else b)[z[1]][z[2]]
 return sum(w*atom(z) for w,z in r)
def bounds(level,s):return s['bounds']

def masks(s):
 a,b=s['parameters']['A'],s['parameters']['B']
 m,n,k=len(a),len(b),len(b[0]);out={}
 for rows,inner,cols in itertools.product(itertools.permutations(range(m)),itertools.permutations(range(n)),itertools.permutations(range(k))):
  pair=[[[int(a[i][h]!=0) for h in inner] for i in rows],[[int(b[h][j]!=0) for j in cols] for h in inner]]
  out[canonical(pair)]=pair
 return list(out.values())
MASKS={sid:masks(s) for sid,s in SPECS.items()}
def guard(level,s,p,raw=False):
 if set(p)-{'bank_role'}!= {'A','B','targets'}:raise ValueError('Parameters require A, B, targets, and optional bank_role')
 if 'bank_role' in p and (type(p['bank_role']) is not int or not 0<=p['bank_role']<5):raise ValueError('Invalid bank role')
 a,b,t=p['A'],p['B'],p['targets'];base=s['parameters'];m,n,k=len(base['A']),len(base['B']),len(base['B'][0])
 if len(a)!=m or any(len(r)!=n for r in a) or len(b)!=n or any(len(r)!=k for r in b):raise ValueError('Matrix dimensions outside family')
 if any(type(v) is not int for x in [a,b] for r in x for v in r):raise ValueError('Integer matrix entries required')
 if len(t)!=len(base['targets']) or len({tuple(z) for z in t})!=len(t) or any(len(z)!=2 or any(type(x)is not int for x in z) or not(0<=z[0]<m and 0<=z[1]<k) for z in t):raise ValueError('Invalid target roles')
 if t!=sorted(t):raise ValueError('Targets must be in row-major order')
 if not s['blank'] and t!=[[i,j] for i in range(m) for j in range(k)]:raise ValueError('Full matrix required')
 lim=s['bounds'] if raw else bounds(level,s)
 if any(abs(v)>lim['coefficient'] for x in [a,b] for r in x for v in r):raise ValueError('Operand coefficient cap')
 vals=[a[i][h]*b[h][j] for i in range(m) for j in range(k) for h in range(n)]
 if max(map(abs,vals))>lim['product']:raise ValueError('Individual product cap')
 if max(sum(abs(a[i][h]*b[h][j]) for h in range(n)) for i in range(m) for j in range(k))>lim['dot_l1']:raise ValueError('Dot product collection cap')
 if max(abs(v) for r in mul(a,b) for v in r)>lim['result']:raise ValueError('Result cap')
 if not raw and canonical([[[int(v!=0) for v in row] for row in x] for x in [a,b]]) not in {canonical(z) for z in MASKS[s['source_id']]}:raise ValueError('Sparsity outside source workload orbit')
 return lim

def fill(text,slots):
 if text is None:return None
 return re.sub(r'\{\{([A-Za-z0-9_]+)\}\}',lambda m:slots.get(m[1],m[0]),text)

def solution(s,p,raw):
 a,b,t=p['A'],p['B'],p['targets'];c=mul(a,b);m,n,k=len(a),len(b),len(b[0]);x,y=s['names'];xy=x+y
 slots={'A':mat(a),'B':mat(b),'C':mat(c)}
 at=copy.deepcopy(a);at[0][:2]=[-a[0][0],-a[0][1]];slots['A_typo']=mat(at if raw else a)
 for i in range(m):
  for j in range(k):slots[f'C_{i}_{j}']='$'+str(c[i][j])+'$'
 for z,(i,j) in enumerate(t):
  if raw and s['progress_masks']:
   progress=[[('∗' if v=='*' else c[rr][cc]) for cc,v in enumerate(row)] for rr,row in enumerate(s['progress_masks'][z])]
  else:progress=[[('∗' if [rr,cc] in t[z+1:] else c[rr][cc]) for cc in range(k)] for rr in range(m)]
  slots[f'progress_{z}']=mat(progress);slots[f'dot_{z}']=r'\,'+str(c[i][j])+'='+dot(a,b,i,j)
 if not raw:
  return product_solution(a,b,s['names'],t),slots
 if s['solution_template']:
  return fill(s['solution_template'],slots),slots
 # Authored completion of missing solution uses the identical source shared stages.
 text=(f'Here, ${x}$ is a ${m}\\times {n}$ matrix and ${y}$ is a ${n}\\times {k}$ matrix. \n\n'
       f'There are ${n}$ columns in ${x}$ and ${n}$ rows in ${y},$ so ${x}$ and ${y}$ are conformable for multiplication:\n\n'
       '$$\n'+f'{{{x}}}_{{{m}\\times \\boxed{{\\text{{{n}}}}}}}{{\\cdot }}_{{✓}}{{{y}}}_{{\\boxed{{\\text{{{n}}}}}\\times {k}}}={{{xy}}}_{{{m}\\times {k}}}'+'\n$$\n\n'
       f"Let's compute ${xy},$ one element at a time:\n\n$$\n"+r'\begin{aligned}')
 rows=[' & '+mat(a)+mat(b)+'='+slots[f'progress_{z}']+', &  & '+slots[f'dot_{z}'] for z in range(len(t))]
 return text+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$\n\nTherefore, \n$'+xy+'='+mat(c)+'.$',slots

def make_bank(a,b,role):
 # A complete translated five-point bank. Any of the five points may be
 # correct, so centrality, signs, extrema, and shared entries do not fix the key.
 c=mul(a,b);patterns=[(0,0),(-1,0),(1,0),(0,-1),(0,1)]
 origin=patterns[role]
 return [[[v+point[(i+j)%2]-origin[(i+j)%2] for j,v in enumerate(row)] for i,row in enumerate(c)] for point in patterns]

def build(level,seed,s,p,profile):
 raw=profile=='observed-raw'; observed=profile.startswith('observed-');lim=guard(level,s,p,raw=observed)
 a,b,t=p['A'],p['B'],p['targets']
 if observed and p!=s['parameters']:raise ValueError('Historical banks support original-parameter replay only')
 c=mul(a,b);sol,slots=solution(s,p,raw)
 prompt=fill(s['prompt_template'],slots)
 roles=s['roles'] if observed else {f'field-{z+1}':pos for z,pos in enumerate(t)}
 if s['blank'] and not raw:
  inv={tuple(pos):key for key,pos in roles.items()}
  head=s['prompt_template'].split('\n\n')[0]
  if s['source_id']=='q-318413':head='Determine $AB$ given that'
  prompt=head+'\n\n'+mf.matrix_operands([s['names'][0]+'='+mat(a),s['names'][1]+'='+mat(b)+'.'],stacked=True)+'\n\n'+mf.matrix_answer(''.join(s['names']),[[('{{'+inv[i,j]+'}}') if (i,j) in inv else str(v) for j,v in enumerate(row)] for i,row in enumerate(c)])
 if not observed and s['source_id']=='q-129497':
  prompt='If\n\n'+mf.matrix_operands(['A='+mat(a),'B='+mat(b)],stacked=True)+'\n\nthen $AB=$'
 # Keep each matrix equation immediately above its dot product, avoiding a
 # wide two-column source alignment; operative stage order is unchanged.
 if sol is not None and not raw:sol=sol.replace(', &  & ', ', '+r'\\ & ')
 prompt=mf.normalize_prose(prompt);sol=mf.normalize_prose(sol) if sol is not None else None
 field_data=[]
 if s['blank']:
  for f in s['bank']:
   i,j=roles[f['key']];field_data.append((f['key'],f['type'],[str(c[i][j])],0,f['has_correct']))
 elif observed:
  for f in s['bank']:
   values=[]
   for choice in f['choices']:
    vals=[[recipe(r,a,b,c) for r in row] for row in choice['recipes']];values.append(mat(vals) if choice['matrix'] else str(vals[0][0]))
   correct=f.get('correct_index')
   if correct is None and not raw:
    correct=next(i for i,v in enumerate(values) if v==mat(c))
   field_data.append((f['key'],f['type'],values,correct,f['has_correct']))
 else:
  role=p.get('bank_role',random.Random(seed).randrange(5))
  field_data=[('selection',':answer-field.type/radio',[mat(z) for z in make_bank(a,b,role)],role,True)]
 if not raw:
  for _,_,vs,_,_ in field_data:
   if len(set(vs))!=len(vs):raise ValueError('Whole-bank collision')
 # Coupled bank-value cap: no hidden oversized distractor arithmetic.
 if not observed:
  for _,_,vs,_,_ in field_data:
   for v in vs:
    numbers=[abs(int(x)) for x in re.findall(r'(?<![A-Za-z])[-+]?\d+',v)]
    if numbers and max(numbers)>lim['dot_l1']:raise ValueError('Displayed bank coefficient cap')
 q={':question/problem':prompt}
 if sol is not None and (not raw or s['has_solution']):q[':question/worked-solution']=sol
 if not raw or s['observed_difficulty'] is not None:q[':question/difficulty']=':question.difficulty/'+level
 identity={'level':q.get(':question/difficulty'),'prompt':prompt,'solution':q.get(':question/worked-solution'),'bank':[(key,typ,sorted(values),values[ci] if ci is not None else None,has) for key,typ,values,ci,has in field_data]}
 qid=uid(identity);q[':question/id']=qid;fields=[]
 for key,typ,values,ci,has in field_data:
  fid=uid([qid,key]);answers=[{':answer/id':uid([fid,mf.normalize_tex(v)]),':answer/type':':answer.type/math',':answer/value':mf.normalize_tex(v)} for v in values]
  f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':typ,':answer-field/choices':answers}
  if ci is not None and (not raw or has):f[':answer-field/correct']=[':answer/id',answers[ci][':answer/id']]
  random.Random(str(seed)+key).shuffle(answers);fields.append(f)
 q[':question/answer-fields']=fields
 if ':question/worked-solution' in q:mf.validate_generated_record({'question':q})
 else:
  mf.validate_prose(prompt)
  for f in fields:
   for v in f[':answer-field/choices']:mf.validate_tex(v[':answer/value'])
 return {'knowledge_point':KP.copy(),'question':q,'generation':{'version':VERSION,'seed':seed,'level':level,'template':s['source_id'],'parameters':copy.deepcopy(p),'profile':profile,'bank_profile':s['source_id']+'-opaque-observed' if observed and not s['blank'] else profile,'source_ids':[s['source_id']],'basis':4697,'domains':lim,'evidence_only':raw or (observed and not s['blank']),'eligible_for_learning':not raw and not(observed and not s['blank']),'authored_level':s['observed_difficulty'] is None,'observed_difficulty':s['observed_difficulty'],'math_format':mf.FORMAT_VERSION,'matrix_role':'ordinary coefficient matrix','mathematical_fingerprint':sha({'A':a,'B':b,'targets':t,'assessed_information':'partial matrix' if s['blank'] else 'full matrix','level_demand':level}),'content_fingerprint':sha(identity),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def family(level,template,rng):
 name=template or rng.choice(list(SPECS))
 if name not in SPECS:raise ValueError('Unknown easy family')
 return copy.deepcopy(SPECS[name])

def replay_source(source_id, repaired=False):
 """Evidence API: preserve absent source fields, never used by the serving CLI."""
 s=copy.deepcopy(SPECS[source_id])
 return build('easy',0,s,s['parameters'],'observed-repaired' if repaired else 'observed-raw')

@mf.checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level != 'easy':raise ValueError('Unsupported difficulty; source supports easy only')
 profile=profile or 'two-sum-error'
 if profile not in PROFILES:raise ValueError('Unknown complete bank profile')
 if profile=='observed-raw':raise ValueError('Use replay_source for raw source evidence')
 rng=random.Random(seed)
 if template is None and field_type:
  want=field_type.split('/')[-1]
  if want not in ('radio','blank'):raise ValueError('Unsupported field type')
  template=rng.choice([sid for sid,spec in SPECS.items() if ('blank' if spec['blank'] else 'radio')==want])
 s=family(level,template,rng)
 if field_type and field_type.split('/')[-1] != ('blank' if s['blank'] else 'radio'):raise ValueError('Field type outside family')
 if parameters is not None:return build(level,seed,s,copy.deepcopy(parameters),profile)
 if profile.startswith('observed-'):return build(level,seed,s,copy.deepcopy(s['parameters']),profile)
 p=copy.deepcopy(s['parameters']);cap=min(bounds(level,s)['coefficient'],5)
 # Decide assessed cells and workload-preserving sparsity before numbers.
 if s['blank']:
  cells=[[i,j] for i in range(len(p['A'])) for j in range(len(p['B'][0]))]
  p['targets']=sorted(rng.sample(cells,len(p['targets'])))
 if not s['blank']:p['bank_role']=rng.randrange(5)
 mask=rng.choice(MASKS[s['source_id']]);rejects={}
 for attempt in range(10000):
  for name,pattern in zip(('A','B'),mask):
   p[name]=[[rng.choice([z for z in range(-cap,cap+1) if z]) if present else 0 for present in row] for row in pattern]
  try:
   record=build(level,seed,s,p,profile)
   record['generation']['sampling']={'attempts':attempt+1,'rejections':rejects,'sparsity':mask}
   return record
  except ValueError as exc:
   why=str(exc);rejects[why]=rejects.get(why,0)+1
 raise ValueError('Whole-instance sampler exhausted')
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def markdown(r):
 q=r['question'];g=r['generation'];out=[f"Level: {g['level']}; template: {g['template']}; profile: {g['profile']}",q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  correct=f.get(':answer-field/correct',[None,None])[1];out.append(f"Field {f[':answer-field/key']} ({f[':answer-field/type']}):"+(' [source correct designation absent]' if correct is None else ''))
  out.extend(('✓ ' if a[':answer/id']==correct else '• ')+'$'+a[':answer/value']+'$' for a in f[':answer-field/choices'])
 out.append(q.get(':question/worked-solution','[Source worked solution absent]'));return '\n\n'.join(out)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy'],default='easy');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in [args.difficulty] for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
