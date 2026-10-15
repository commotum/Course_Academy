#!/usr/bin/env python3
"""Source-backed 3x3 matrix-column multiplication; pure seeded generator.
Moderate only. No durable writes. See adjacent package for scope and validation.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as s
KP=17592186100867
HERE=Path(__file__).with_suffix('')
CAP=json.loads((HERE/'reference/source.json').read_text()); RECORD=CAP['record']
KP_UUID=RECORD[':knowledge-point/id']; TITLE=RECORD[':knowledge-point/title']
VERSION='matrix3-column-1.0'; SUPPORTED_LEVELS=('moderate',)
SOURCES={q[':question/math-academy-id']:q for q in RECORD[':knowledge-point/questions']}
GROUPS={'named-radio':['q-70188','q-70190','q-77350','q-13557'], 'inline-radio':['q-127267','q-70191','q-77349','q-77351'], 'named-blank':['q-318606'], 'inline-blank':['q-318622'], 'what-radio':['q-13558']}
EXCLUDED={'q-13557':'Unrated, no canonical key or worked solution', 'q-13558':'Unrated, no canonical key or worked solution','q-77349':'Irregular observed distractors: inferred generalization unresolved','q-77351':'One compound distractor has unresolved parameterized recipe'}
ELIGIBLE={t:[p for p in profiles if p not in EXCLUDED] for t,profiles in GROUPS.items() if t!='what-radio'}
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def normalize_tex(t):return t.replace('\\\\begin','\\begin').replace('\\\\end','\\end').replace('\\\\\\\\','\\\\')
def matrices(t):return [[[int(c.strip()) for c in row.split('&')] for row in x.split('\\\\')] for x in MATRIX.findall(t)]
def parameters(q):
 m=matrices(q[':question/problem']);names=re.search(r'Find \$([A-Z])([a-z])\$',q[':question/problem'])
 return {'A':m[0],'v':[row[0] for row in m[1]],'matrix_name':names[1] if names else 'A','vector_name':names[2] if names else 'x'}
def template_of(mid):return next(t for t,ids in GROUPS.items() if mid in ids)
def texmat(rows):return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(map(str,row)) for row in rows)+r'\end{bmatrix}'
def vector(v):return texmat([[x] for x in v])
def dot(p):return tuple(map(int,s.Matrix(p['A'])*s.Matrix(p['v'])))
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),x))
def fingerprint(p):
 # Permuting matching columns/vector entries preserves the identical three sums.
 return digest(sorted(tuple(p['A'][i][j] for i in range(3))+(p['v'][j],) for j in range(3)))
def question_fingerprint(q):return fingerprint(parameters(q))
def bank(mid,p):
 r,t,u=dot(p)
 banks={
 'q-127267':[('correct',(r,t,u)),('negate-third',(r,t,-u)),('negate-second-third',(r,-t,-u)),('negate-second',(r,-t,u)),('repeat-first-negate-third',(r,r,-u))],
 'q-70188':[('correct',(r,t,u)),('negate-second-third',(r,-t,-u)),('negate-third',(r,t,-u)),('negate-first-second',(-r,-t,u)),('negate-second',(r,-t,u))],
 'q-70191':[('correct',(r,t,u)),('negate-second',(r,-t,u)),('negate-second-third',(r,-t,-u)),('negate-first',(-r,t,u)),('negate-third',(r,t,-u))],
 'q-70190':[('correct',(r,t,u)),('negate-third',(r,t,-u)),('negate-second',(r,-t,u)),('negate-first',(-r,t,u)),('negate-first-second',(-r,-t,u))],
 'q-77350':[('correct',(r,t,u)),('negate-first-second',(-r,-t,u)),('swap-second-third',(r,u,t)),('negate-second',(r,-t,u)),('swap-first-third',(u,t,r))]}
 if mid in banks:return banks[mid]
 if mid in EXCLUDED:
  assert p==parameters(SOURCES[mid]),'Unresolved bank is original-parameter replay only'
  f=SOURCES[mid][':question/answer-fields'][0];correct=f.get(':answer-field/correct',{}).get(':answer/id')
  return [('correct' if a[':answer/id']==correct else 'unresolved-observed-'+str(i),tuple(row[0] for row in matrices(normalize_tex(a[':answer/value']))[0])) for i,a in enumerate(f[':answer-field/choices'])]
 return []
def par(n):return '('+str(n)+')' if n<0 else str(n)
def signed_sum(nums):return str(nums[0])+''.join(('+' if n>=0 else '')+str(n) for n in nums[1:])
def render(template,p,profile):
 A=texmat(p['A']);V=vector(p['v']);target=p['matrix_name']+p['vector_name'];AV=A+V
 # Keep the exact observed prompt/table structure and replace its declared slots.
 source=SOURCES[profile];prompt=MATRIX.sub(lambda m: A if m.start()==MATRIX.search(source[':question/problem']).start() else V,source[':question/problem'])
 old=parameters(source);oldtarget=old['matrix_name']+old['vector_name']
 if template.startswith('named'):
  prompt=prompt.replace('$'+oldtarget+'$', '$'+target+'$').replace('$'+oldtarget+'=', '$'+target+'=').replace('$'+old['matrix_name']+'=', '$'+p['matrix_name']+'=').replace('$'+old['vector_name']+'=', '$'+p['vector_name']+'=')
 products=[[a*b for a,b in zip(row,p['v'])] for row in p['A']]
 terms=[[par(a)+r'\cdot '+par(b) for a,b in zip(row,p['v'])] for row in p['A']]
 if template=='named-blank':
  expanded=texmat([[r'\begin{aligned}'+r' \\ '.join(' & + & '.join(row) for row in terms)+r'\end{aligned}']])
  intermediate=texmat([[r'\begin{aligned}'+r' \\ '.join(' & + & '.join(par(z) for z in row) for row in products)+r'\end{aligned}']])
 elif template=='inline-blank':
  expanded=texmat([[r'\begin{aligned}'+r' \\ '.join(' & + & '.join(row) for row in terms)+r'\end{aligned}']])
  intermediate=texmat([[par(row[0]),'+',par(row[1]),'+',par(row[2])] for row in products])
 else:expanded=vector(['+'.join(row) for row in terms]);intermediate=vector([signed_sum(row) for row in products])
 prefix=(target+r' & ='+AV+r' \\  & =') if template.startswith('named') else AV+' & ='
 solution='We multiply each row in the matrix by the column vector using the dot product:\n\n$$\n'+r'\begin{aligned}'+prefix+expanded+r' \\  & ='+intermediate+r' \\  & ='+vector(dot(p))+('.' if template=='inline-blank' else '')+r'\end{aligned}'+'\n$$'
 return prompt,solution

def guard(p):
 assert set(p)=={'A','v','matrix_name','vector_name'} and len(p['A'])==len(p['v'])==3 and all(len(row)==3 for row in p['A'])
 assert all(type(z)is int and -8<=z<=8 for row in p['A'] for z in row)
 assert all(type(z)is int and -8<=z<=8 for z in p['v']) and any(p['v'])
 assert p['matrix_name'] in ('A','B','L','P','N','Z') and p['vector_name'] in ('x','y','z','v','n')
def generate(level,seed=0,template=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: only moderate has complete rated source evidence')
 rng=random.Random(seed);template=template or rng.choice(list(ELIGIBLE))
 if template not in ELIGIBLE:raise ValueError('Unsupported template')
 profile=profile or rng.choice(ELIGIBLE[template])
 if profile not in ELIGIBLE[template]:raise ValueError('Excluded or mismatched source profile')
 for _ in range(1000):
  p=parameters if parameters is not None else {'A':[[rng.randint(-8,8) for _ in range(3)] for _ in range(3)],'v':[rng.randint(-8,8) for _ in range(3)],'matrix_name':rng.choice(('A','B','L','P','N','Z')),'vector_name':rng.choice(('x','y','z','v','n'))}
  if not any(p['v']):continue
  guard(p);entries=bank(profile,p)
  if len({z for _,z in entries})==len(entries):break
  if parameters is not None:raise ValueError('Full source bank collision')
 else:raise ValueError('Sampling bound exhausted')
 prompt,solution=render(template,p,profile)
 ident=digest({'version':VERSION,'level':level,'template':template,'parameters':p,'bank':sorted(v for _,v in entries)})
 qid=uid('question:'+ident);fields=[]
 specs=[('selection',':answer-field.type/radio',entries)] if entries else [(f'field-{i+1}',':answer-field.type/blank',[('correct',(z,))]) for i,z in enumerate(dot(p))]
 for key,typ,values in specs:
  fid=uid(qid+':'+key);choices=[];correct=None
  for recipe,value in values:
   value=vector(value) if len(value)==3 else str(value[0]);aid=uid(fid+':'+value)
   choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
   if recipe=='correct':correct=aid
  rng.shuffle(choices)
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':typ,':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]})
 return {'knowledge_point':{'db_id':KP,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',':question/answer-fields':fields},'generation':{'generator_version':VERSION,'template':template,'bank_profile':profile,'recipes':[recipe for recipe,_ in entries],'parameters':p,'seed':seed,'source_basis':CAP['basis'],'lineage':CAP['lineage'],'source_references':[profile],'mathematical_fingerprint':fingerprint(p),'eligible_for_learning':True,'evidence_only':False,'sympy_version':s.__version__}}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',default='moderate');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--template');parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['json','markdown'],default='json');args=parser.parse_args()
 records=[];seen=set()
 for seed in range(args.seed,args.seed+max(1000,args.count*100)):
  if len(records)>=args.count:break
  r=generate(args.difficulty,seed,args.template);fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:records.append(r);seen.add(fp)
 if len(records)!=args.count:raise ValueError('Distinct sampling limit reached')
 if args.format=='json':print(json.dumps({'instances':records},indent=2))
 else:
  for r in records:print(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']+'\n\n'+json.dumps(r['question'][':question/answer-fields']))
