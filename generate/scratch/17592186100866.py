#!/usr/bin/env python3
"""Multiplying a 2x2 matrix by a column vector. Pure, deterministic generator.
Only easy is source-backed. See adjacent package for replay and capability evidence.
No database writes. Matrices are LaTeX, not plots. Seeds and labels do not define
mathematical distinctness; ordered row dot-product operands do.
"""
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts/question_capture'))
from math_format import matrix_answer
KP=17592186100866
HERE=Path(__file__).with_suffix('')
CAP=json.loads((HERE/'reference/source.json').read_text())
RECORD=CAP['record'];KP_UUID=RECORD[':knowledge-point/id'];TITLE=RECORD[':knowledge-point/title']
VERSION='matrix-column-1.0'
SUPPORTED_LEVELS=('easy',)
SOURCES={q[':question/math-academy-id']:q for q in RECORD[':knowledge-point/questions']}
GROUPS={'named-radio':['q-13564','q-126511','q-126512','q-13565'], 'inline-radio':['q-13555','q-13629','q-13560'], 'named-blank':['q-275589'], 'inline-blank':['q-318640','q-318644'], 'what-radio':['q-13566']}
# q-126512's unexplained irregular bank is replay-only, not invented into a recipe.
ELIGIBLE={k:[i for i in ids if i not in ('q-126512','q-13566')] for k,ids in GROUPS.items() if k!='what-radio'}
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def matrices(text):
 return [[[int(c.strip()) for c in row.split('&')] for row in x.split('\\\\')] for x in MATRIX.findall(text)]
def parameters(q):
 m=matrices(q[':question/problem']);A=m[0];v=[r[0] for r in m[1]]
 names=re.search(r'Find \$([A-Z])([a-z])\$',q[':question/problem'])
 return {'a':A[0][0],'b':A[0][1],'c':A[1][0],'d':A[1][1],'u':v[0],'v':v[1], 'matrix_name':names[1] if names else 'A', 'vector_name':names[2] if names else 'x'}
def template_of(mid):return next(t for t,ids in GROUPS.items() if mid in ids)
def texmat(rows):return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(map(str,row)) for row in rows)+r'\end{bmatrix}'
def vector(x,y):return texmat([[x],[y]])
def dot(p):return tuple(map(int,s.Matrix([[p['a'],p['b']],[p['c'],p['d']]])*s.Matrix([p['u'],p['v']])))
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),x))
def fingerprint(p):
 # Dot-product order within each row is immaterial: swapping columns and vector
 # coordinates together cannot create a different task. Keep row roles ordered.
 cols=sorted([(p['a'],p['c'],p['u']),(p['b'],p['d'],p['v'])])
 return digest(cols)
def question_fingerprint(q):return fingerprint(parameters(q))
def bank(mid,p):
 a,b,c,d,u,v=(p[k] for k in ('a','b','c','d','u','v'));r,t=dot(p)
 if mid=='q-13564':return [('correct',(r,t)),('negate-both',(-r,-t)),('negate-second',(r,-t)),('negate-first',(-r,t)),('reverse-input',(v,u))]
 if mid=='q-126511':return [('correct',(r,t)),('row-sums',(a+b,c+d)),('negative-row-sums',(-a-b,-c-d)),('swap-output',(t,r)),('first-column',(a,c))]
 if mid=='q-13555':return [('correct',(r,t)),('repeat-first',(r,r)),('negate-second',(r,-t)),('negate-both',(-r,-t)),('negate-first',(-r,t))]
 if mid=='q-13565':return [('correct',(r,t)),('swap-negative-both',(-t,-r)),('negate-second',(r,-t)),('negate-both',(-r,-t)),('negative-second-first',(-t,r))]
 if mid=='q-13629':return [('correct',(r,t)),('first-plus-one',(r+1,t)),('second-minus-one',(r,t-1)),('second-plus-one',(r,t+1)),('both-minus-one',(r-1,t-1))]
 if mid=='q-13560':return [('correct',(r,t)),('first-plus-one',(r+1,t)),('swap-output',(t,r)),('repeat-first',(r,r)),('repeat-second',(t,t))]
 # Unrated/incomplete or unresolved banks: retain exact observed discrepancies
 # for original-parameter replay ONLY. Never sample these as learning content.
 if mid in ('q-126512','q-13566'):
  assert p==parameters(SOURCES[mid]),'Unresolved profile permits original parameters only'
  f=SOURCES[mid][':question/answer-fields'][0]
  vals=[]
  for i,z in enumerate(f[':answer-field/choices']):
   m=matrices(z[':answer/value'].replace('\\\\begin','\\begin').replace('\\\\end','\\end'))[0]
   val=tuple(row[0] for row in m);vals.append(('correct' if val==(r,t) else 'unresolved-observed-'+str(i),val))
  return vals
 return []
def group(n):return '('+str(n)+')' if n<0 else str(n)
def answer_layout(prompt):
 # Source tables use border cells for vector brackets and rowspans for labels.
 # Preserve source row/key order while displaying the canonical answer vector.
 prefix,table=prompt.split('\n\n|',1)
 label=re.search(r'\$([^$]+)=',table)[1]
 keys=re.findall(r'\{\{([^{}]+)\}\}',table)
 return prefix+'\n\n'+matrix_answer(label,[['{{'+key+'}}'] for key in keys])
def render(template,p):
 a,b,c,d,u,v=(p[k] for k in ('a','b','c','d','u','v'));r,t=dot(p)
 A=texmat([[a,b],[c,d]]);V=vector(u,v);target=p['matrix_name']+p['vector_name'];AV=A+V
 if template.startswith('named'):
  prompt=f'Find ${target}$ if \n${p["matrix_name"]}={A}$\nand\n${p["vector_name"]}={V}.$'
  if template=='named-blank':prompt=prompt.replace('if \n','if\n')+'\n\n| $'+target+r'=\,\,$ |  | {{field-1}} |  |'+'\n| --- | --- | --- | --- |\n|  | {{field-2}} |  |  |'
 elif template=='inline-blank':prompt='Compute the following:\n\n| $'+AV+r'=\,\,$ |  | {{field-1}} |  |'+'\n| --- | --- | --- | --- |\n|  | {{field-2}} |  |  |'
 elif template=='what-radio':prompt=f'What is ${AV}$?'
 else:prompt=f'${AV}=$'
 prefix=target+'=' if template=='named-blank' else ''
 row1=group(a)+r'\cdot '+group(u)+'+'+group(b)+r'\cdot '+group(v)
 row2=group(c)+r'\cdot '+group(u)+'+'+group(d)+r'\cdot '+group(v)
 solution='We multiply each row in the matrix by the column vector using the dot product. Multiplying the first row, we get\n\n$$\n'+r'\begin{aligned}'+prefix+AV+' & ='+vector(row1,'∗')+'='+vector(r,'∗')+r'.\end{aligned}'+'\n$$\n\nMultiplying the second row, we get\n\n$$\n'+r'\begin{aligned}'+prefix+AV+' & ='+vector(r,row2)+'='+vector(r,t)+r'.\end{aligned}'+'\n$$\n\nTherefore, \n'
 if template.startswith('named'):solution+='$'+target+'='+vector(r,t)+'.$'
 else:solution+='\n$$\n'+AV+'='+vector(r,t)+'.\n$$'
 return prompt,solution

def guard(p):
 assert set(p)=={'a','b','c','d','u','v','matrix_name','vector_name'}
 assert all(type(p[k]) is int and -11<=p[k]<=11 for k in ('a','b','c','d','u','v'))
 assert p['u']!=0 and p['v']!=0
 assert p['matrix_name'] in ('A','Z','X','H') and p['vector_name'] in ('x','y','n','a')
def generate(level,seed=0,template=None,parameters=None,profile=None):
 if level!='easy':raise ValueError('Unsupported band: no source-backed moderate/hard backbone; larger coefficients do not change classification')
 rng=random.Random(seed);template=template or rng.choice(list(ELIGIBLE))
 if template not in ELIGIBLE:raise ValueError('Unsupported template')
 profile=profile or rng.choice(ELIGIBLE[template])
 if profile not in ELIGIBLE[template]:raise ValueError('Excluded or mismatched source bank')
 for _ in range(1000):
  p=dict(parameters) if parameters is not None else {**{k:rng.randint(-11,11) for k in ('a','b','c','d')},'u':rng.choice([i for i in range(-9,10) if i]),'v':rng.choice([i for i in range(-9,10) if i]),'matrix_name':rng.choice(('A','Z','X','H')),'vector_name':rng.choice(('x','y','n','a'))}
  guard(p);entries=bank(profile,p)
  if len(set(v for _,v in entries))==len(entries):break
  if parameters is not None:raise ValueError('Complete bank collision')
 else:raise ValueError('Sampling bound exhausted')
 prompt,solution=render(template,p);r,t=dot(p)
 identity=digest({'version':VERSION,'level':level,'prompt':prompt,'solution':solution,'bank':sorted(vector(*z) for _,z in entries)})
 qid=uid('question:'+identity);fields=[]
 specs=[('selection',':answer-field.type/radio',entries)] if entries else [(f'field-{i+1}',':answer-field.type/blank',[('correct',(z,))]) for i,z in enumerate((r,t))]
 for key,typ,values in specs:
  fid=uid(qid+':'+key);choices=[];correct=None
  for recipe,value in values:
   value=vector(*value) if len(value)==2 else str(value[0]);aid=uid(fid+':'+value)
   choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
   if recipe=='correct':correct=aid
  rng.shuffle(choices)
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':typ,':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]})
 # Apply display normalization after identities are derived so existing seeds,
 # answer fields and correct-answer references retain their exact identities.
 if template.endswith('-blank'):prompt=answer_layout(prompt)
 return {'knowledge_point':{'db_id':KP,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':fields},'generation':{'generator_version':VERSION,'template':template,'bank_profile':profile,'parameters':p,'seed':seed,'source_basis':CAP['basis'],'lineage':CAP['lineage'],'source_references':[profile],'mathematical_fingerprint':fingerprint(p),'eligible_for_learning':True,'evidence_only':False,'sympy_version':s.__version__}}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',default='easy');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--template');parser.add_argument('--count',type=int,default=1);args=parser.parse_args()
 print(json.dumps({'instances':[generate(args.difficulty,args.seed+i,args.template) for i in range(args.count)]},indent=2))
