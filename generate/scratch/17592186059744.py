#!/usr/bin/env python3
"""Source-derived transposition of a single row or column; no arithmetic on entries."""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).with_suffix('');SOURCE=json.loads((HERE/'source.json').read_text());S=SOURCE
KP_ID=17592186059744;KP_UUID=SOURCE['record'][':knowledge-point/id'];TITLE=SOURCE['record'][':knowledge-point/title'];VERSION='1.0.0';SUPPORTED_LEVELS=('easy','moderate')
MATRIX=re.compile(r'\\begin\{(?:bmatrix|matrix)\}(.*?)\\end\{(?:bmatrix|matrix)\}',re.S)
def expression(t):
 t=t.strip().replace('$','')
 return sp.simplify(parse_expr(t,transformations=standard_transformations+(implicit_multiplication_application,),local_dict={c:sp.Symbol(c) for c in 'abcdefghijklmnopqrstuvwxyz'},evaluate=True).subs({sp.Float('0.01'):sp.Rational(1,100),sp.Float('-0.1'):sp.Rational(-1,10)}))
def matrix_object(t):
 m=MATRIX.search(t)
 if m is None:
  # Canonical legacy \matrix TeX uses a single backslash separator.
  m=re.search(r'\\matrix\s*\{(.*?)\}',t,re.S);assert m,t
  content=m[1].strip();rows=re.split(r'\\+\s*',content)
 else:rows=re.split(r'\\\\',m[1].strip())
 rows=[r.strip() for r in rows if r.strip()]
 return tuple(tuple(expression(z) for z in r.split('&')) for r in rows)
def tex(x):return sp.sstr(sp.sympify(x)).replace('**','^').replace('*','')
def matrix(rows):return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(tex(z) for z in row) for row in rows)+r'\end{bmatrix}'
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def fingerprint(q):
 rows=matrix_object(q[':question/problem']);return digest([[str(z) for z in row] for row in rows])
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
SPECS=json.loads((HERE/'source-specs.json').read_text());TEMPLATES=tuple(t for t in SPECS if t!='q-1048')
def original(t):return {'entries':SPECS[t]['entries']}
def recipes(profile,v,orientation):
 """Each pair is (output orientation, ordered entry expressions)."""
 opposite='column' if orientation=='row' else 'row';rev=list(reversed(v));neg=[-z for z in v]
 if profile=='row-sign-reverse':return [(opposite,v),(opposite,rev),(orientation,rev),(opposite,neg),(orientation,[-v[3],-v[2],v[1],v[0]])]
 if profile=='column-swap':return [(opposite,v),(opposite,[v[0],v[3],v[2],v[1]]),(orientation,rev),(orientation,v),(opposite,rev)]
 if profile=='column-sign-reverse':return [(opposite,v),(orientation,[-z for z in rev]),(opposite,rev),(opposite,neg),(orientation,rev)]
 if profile=='column-negate':return [(orientation,neg),(opposite,neg),(orientation,rev),(opposite,rev),(opposite,v)]
 if profile=='column-reciprocal-reverse':return [(orientation,rev),(orientation,[1/z for z in rev]),(opposite,v),(opposite,rev),(orientation,[-z for z in rev])]
 if profile=='column-reciprocal':return [(orientation,rev),(orientation,[1/z for z in v]),(opposite,rev),(orientation,neg),(opposite,v)]
 if profile=='unrated-reshape':return [('square',v),(opposite,neg),(orientation,rev),(opposite,v),(opposite,rev)]
 raise ValueError(profile)
def shaped(v,orientation):
 return [list(v)] if orientation=='row' else [[z] for z in v] if orientation=='column' else [list(v[:2]),list(v[2:])]
def sample(t,rng):
 spec=SPECS[t];v=[expression(z) for z in spec['entries']]
 if spec['difficulty']=='easy':return [sp.Integer(rng.randint(-20,20)) for _ in v]
 result=[]
 for z in v:
  # Preserve monomial / two-term entry structure and variable roles; change real coefficients.
  expanded=sp.expand(z);terms=[]
  for term in sp.Add.make_args(expanded):
   coeff,rest=term.as_coeff_Mul();terms.append(sp.sign(coeff)*rng.randint(1,6)*rest)
  result.append(sum(terms))
 return result

def generate(difficulty,seed=0,template=None,parameters=None,replay=False):
 if difficulty not in SUPPORTED_LEVELS and not (replay and template=='q-1048'):raise ValueError('Unsupported difficulty '+difficulty)
 candidates=[t for t in TEMPLATES if SPECS[t]['difficulty']==difficulty]
 rng=random.Random(seed);t=template or rng.choice(candidates);spec=SPECS[t];src=SOURCES[t]
 assert spec['difficulty']==difficulty or (replay and t=='q-1048')
 v=[expression(z) for z in parameters['entries']] if parameters else sample(t,rng)
 assert len(v)==len(spec['entries']) and all(z.is_finite is not False for z in v)
 ori=spec['orientation'];given=shaped(v,ori);answer=[list(row) for row in zip(*given)]
 profile=spec['profile'];values=[]
 if profile!='blank':
  if 'reciprocal' in profile and any(z==0 for z in v):raise ValueError('Zero reciprocal distractor')
  values=[matrix(shaped(z,o)) for o,z in recipes(profile,v,ori)]
  objects=[matrix_object(z) for z in values]
  if len(set(objects))!=len(objects):raise ValueError('Equivalent options')
  if sum(obj==tuple(map(tuple,answer)) for obj in objects)!=1:raise ValueError('Ambiguous bank')
 # One content identity per exact mathematical task, independent of seed and bank.
 fp=digest([[str(z) for z in row] for row in given]);qid=str(uuid.uuid5(uuid.UUID(KP_UUID),'transpose:'+fp))
 problem=MATRIX.sub(lambda m:matrix(given),src[':question/problem'])
 if ':question/worked-solution' in src:solution=MATRIX.sub(lambda m:matrix(answer),src[':question/worked-solution'])
 else:solution='To find the transpose, we interchange the rows and columns:\n\n$$\nG^T='+matrix(answer)+'\n$$'
 fields=[]
 source_fields=sorted(src[':question/answer-fields'],key=lambda f:(f[':answer-field/key'],not bool(f.get(':answer-field/correct'))))
 if profile!='blank':source_fields=source_fields[:1] # q-1045 has a redundant historical field with no key.
 for i,sf in enumerate(source_fields):
  key=sf[':answer-field/key'];fid=str(uuid.uuid5(uuid.UUID(qid),'field:'+key));blank=profile=='blank'
  vals=[tex(v[int(key.split('-')[-1])-1])] if blank else values
  choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'answer:'+value)),':answer/type':':answer.type/math',':answer/value':value} for value in vals]
  correct=tex(v[int(key.split('-')[-1])-1]) if blank else matrix(answer)
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/blank' if blank else ':answer-field.type/radio',':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in choices if a[':answer/value']==correct)],':answer-field/choices':choices})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':t,'bank_profile':profile,'parameters':{'entries':[str(z) for z in v]},'orientation':ori,'domain':'real numeric entries or formal real algebraic entries; reciprocal distractors exclude zero','mathematical_fingerprint':fp,'replay':replay,'assets':[],'source_basis':SOURCE['basis'],'source_question':src[':db/id'],'eligible_for_learning':t!='q-1048','dependency_versions':{'sympy':sp.__version__}}}
def batch(difficulty,count,seed):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty '+difficulty)
 result=[];seen=set()
 for attempt in range(max(100,count*30)):
  try:r=generate(difficulty,seed+attempt)
  except ValueError:continue
  fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:result.append(r);seen.add(fp)
  if len(result)==count:return result
 raise ValueError('Bounded sampler could not produce distinct requested count')
def markdown(r):
 q=r['question'];text=q[':question/problem']+'\n\n'+q[':question/worked-solution']
 for f in q[':question/answer-fields']:
  text+='\n\n'+f[':answer-field/key']+': '+', '.join(a[':answer/value']+(' [correct]' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])
 return text
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',required=True);p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--template');p.add_argument('--format',choices=('json','markdown'),default='json');a=p.parse_args()
 rs=batch(a.difficulty,a.count,a.seed) if not a.template else [generate(a.difficulty,a.seed+i,a.template) for i in range(a.count)]
 print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
