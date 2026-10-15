#!/usr/bin/env python3
"""Step 3–7 private draft. Ordinary coefficient matrices; no database operations.

Backbone: dimension/conformability statement, ordered row-column dot products,
progressive result matrices, conclusion. Complete bank selected before parameters.
Historical opaque banks are public parameterized evidence profiles, never defaults.
All normal sampling and explicit inputs use the same coupled arithmetic guards.
"""
import sys
sys.dont_write_bytecode = True
import argparse,copy,hashlib,json,random,re,uuid
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from scripts.question_capture import math_format as mf
D=Path(__file__).with_suffix(''); SPECS=json.loads((D/'replay-specifications.json').read_text())
VERSION='2275-matrix-product-1'; KP={'db_id':17592186100872,'id':'92dd864a-8bc0-547c-84c9-ffd562909315','title':'Multiplying Two Matrices When They Are Conformable'}
PROFILES=('method-sign-omission','observed-raw','observed-repaired')

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
def bounds(level,s):
 if level=='moderate':return {'coefficient':6,'product':12,'dot_l1':24,'result':18}
 if level=='hard':return {'coefficient':5,'product':10,'dot_l1':20,'result':18}
 return s['bounds']
def guard(level,s,p,raw=False):
 if set(p)!= {'A','B','targets'}:raise ValueError('Parameters must be exactly A, B, targets')
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
 if level=='easy' and any((v==0)!=(original==0) for name,x in [('A',a),('B',b)] for row,old in zip(x,base[name]) for v,original in zip(row,old)):raise ValueError('Easy family preserves its exact source zero mask')
 if level in ('moderate','hard') and any(v==0 for x in [a,b] for r in x for v in r):raise ValueError('Authored level requires nonzero dot product terms')
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
 if s['solution_template']:
  return fill(s['solution_template'],slots),slots
 # Authored completion of missing solution uses the identical source shared stages.
 text=(f'Here, ${x}$ is a ${m}\\times {n}$ matrix and ${y}$ is a ${n}\\times {k}$ matrix. \n\n'
       f'There are ${n}$ columns in ${x}$ and ${n}$ rows in ${y},$ so ${x}$ and ${y}$ are conformable for multiplication:\n\n'
       '$$\n'+f'{{{x}}}_{{{m}\\times \\boxed{{\\text{{{n}}}}}}}{{\\cdot }}_{{✓}}{{{y}}}_{{\\boxed{{\\text{{{n}}}}}\\times {k}}}={{{xy}}}_{{{m}\\times {k}}}'+'\n$$\n\n'
       f"Let's compute ${xy},$ one element at a time:\n\n$$\n"+r'\begin{aligned}')
 rows=[' & '+mat(a)+mat(b)+'='+slots[f'progress_{z}']+', &  & '+slots[f'dot_{z}'] for z in range(len(t))]
 return text+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$\n\nTherefore, \n$'+xy+'='+mat(c)+'.$',slots

def make_bank(a,b):
 c=mul(a,b);m,k=len(c),len(c[0]);n=len(b)
 omitted=[[sum(a[i][h]*b[h][j] for h in range(n-1)) for j in range(k)] for i in range(m)]
 alternating=[[sum((-1 if h%2 else 1)*a[i][h]*b[h][j] for h in range(n)) for j in range(k)] for i in range(m)]
 bank=[c,[list(row) for row in zip(*c)],[[-v for v in row] for row in c],omitted,alternating]
 if len({canonical(z) for z in bank})!=5:raise ValueError('Whole-bank collision')
 return bank

def build(level,seed,s,p,profile):
 raw=profile=='observed-raw'; observed=profile.startswith('observed-');lim=guard(level,s,p,raw=observed)
 a,b,t=p['A'],p['B'],p['targets']
 if observed and t!=s['parameters']['targets']:raise ValueError('Observed profiles preserve the source target map; use the normal method profile for target variation')
 c=mul(a,b);sol,slots=solution(s,p,raw)
 prompt=fill(s['prompt_template'],slots)
 roles=s['roles'] if observed else {f'field-{z+1}':pos for z,pos in enumerate(t)}
 if s['blank'] and not observed:
  head=prompt.split('\n\n|')[0];inv={tuple(pos):key for key,pos in roles.items()};rows=[]
  for i,row in enumerate(c):rows.append('| '+('$'+''.join(s['names'])+'=$' if i==0 else '')+' | '+' | '.join('{{'+inv[i,j]+'}}' if (i,j) in inv else '$'+str(v)+'$' for j,v in enumerate(row))+' |')
  prompt=head+'\n\n'+rows[0]+'\n| --- | '+' | '.join('---' for _ in c[0])+' |\n'+'\n'.join(rows[1:])
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
 else:field_data=[('selection',':answer-field.type/radio',[mat(z) for z in make_bank(a,b)],0,True)]
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
 return {'knowledge_point':KP.copy(),'question':q,'generation':{'version':VERSION,'seed':seed,'level':level,'template':s['source_id'],'parameters':copy.deepcopy(p),'profile':profile,'bank_profile':s['source_id']+'-opaque-observed' if observed and not s['blank'] else profile,'source_ids':[s['source_id']],'basis':2275,'domains':lim,'evidence_only':raw or (observed and not s['blank']),'eligible_for_learning':not raw and not(observed and not s['blank']),'authored_level':level!='easy' or s['observed_difficulty'] is None,'math_format':mf.FORMAT_VERSION,'matrix_role':'ordinary coefficient matrix','mathematical_fingerprint':sha({'A':a,'B':b,'targets':t,'assessed_information':'partial matrix' if s['blank'] else 'full matrix','level_demand':level}),'content_fingerprint':sha(identity),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def family(level,template,rng):
 if level=='easy':
  name=template or rng.choice(list(SPECS));
  if name not in SPECS:raise ValueError('Unknown easy family')
  return copy.deepcopy(SPECS[name])
 name='authored-'+level
 if template and template!=name:raise ValueError('Template outside level')
 s=copy.deepcopy(SPECS['q-129495' if level=='moderate' else 'q-1033']);s['source_id']=name;s['observed_difficulty']=None
 return s

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 profile=profile or 'method-sign-omission'
 if profile not in PROFILES:raise ValueError('Unknown complete bank profile')
 if level!='easy' and profile.startswith('observed-'):raise ValueError('No observed missing-level evidence')
 rng=random.Random(seed)
 if level=='easy' and template is None and field_type:
  want=field_type.split('/')[-1]
  if want not in ('radio','blank'):raise ValueError('Unsupported field type')
  template=rng.choice([sid for sid,spec in SPECS.items() if ('blank' if spec['blank'] else 'radio')==want])
 s=family(level,template,rng)
 if field_type and field_type.split('/')[-1] != ('blank' if s['blank'] else 'radio'):raise ValueError('Field type outside family')
 if parameters is not None:return build(level,seed,s,copy.deepcopy(parameters),profile)
 if profile.startswith('observed-'):return build(level,seed,s,copy.deepcopy(s['parameters']),profile)
 for _ in range(10000):
  p=copy.deepcopy(s['parameters']);cap=min(bounds(level,s)['coefficient'],5)
  for name in ('A','B'):
   p[name]=[[0 if level=='easy' and v==0 else rng.choice([z for z in range(-cap,cap+1) if z]) for v in row] for row in p[name]]
  if s['blank']:
   cells=[[i,j] for i in range(len(p['A'])) for j in range(len(p['B'][0]))];p['targets']=sorted(rng.sample(cells,len(p['targets'])))
  try:return build(level,seed,s,p,profile)
  except ValueError:pass
 raise ValueError('Whole-instance sampler exhausted')
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];g=r['generation'];out=[f"Level: {g['level']}; template: {g['template']}; profile: {g['profile']}",q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  correct=f.get(':answer-field/correct',[None,None])[1];out.append(f"Field {f[':answer-field/key']} ({f[':answer-field/type']}):"+(' [source correct designation absent]' if correct is None else ''))
  out.extend(('✓ ' if a[':answer/id']==correct else '• ')+'$'+a[':answer/value']+'$' for a in f[':answer-field/choices'])
 out.append(q.get(':question/worked-solution','[Source worked solution absent]'));return '\n\n'.join(out)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
