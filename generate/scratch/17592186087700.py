#!/usr/bin/env python3
"""Larger-matrix inverse verification, validated source-shaped generator.

Every source prose/product stage is a mask of complete mathematical objects.
Finite signed simultaneous permutations preserve source arithmetic and inverse
relations. No determinant, adjugate or inversion algorithm is taught or called.
"""
import sys
sys.dont_write_bytecode=True
import argparse,copy,functools,hashlib,itertools,json,random,re,uuid
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import matrix_tex,normalize_prose,checked_math_content
HERE=Path(__file__).with_suffix('');TEMPLATES=json.loads((HERE/'templates.json').read_text());SOURCE=json.loads((HERE/'source.json').read_text())['record']
CAPACITIES={'moderate':204,'hard':288}
TEMPLATE_CAPACITIES={'single-pair':120,'q-11642':24,'q-7913':96,'q-11634':24,'q-11636':24,'q-149818':96,'q-149820':96,'q-149832':24,'q-149833':24,'q-71876':12,'q-71879':24,'q-7905':12,'q-7907':12,'q-7909':24}
VERSION='1.0.0';LEVELS=('moderate','hard');PROFILES=('observed','raw-source');NS=uuid.UUID(SOURCE[':knowledge-point/id']);MAT=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
@functools.lru_cache(maxsize=1024)
def scalar(s):
 s=s.strip();s=re.sub(r'\\(?:d?frac)\{(-?\d+)\}\{(-?\d+)\}',r'(\1)/(\2)',s)
 if not re.fullmatch(r'[-+\d()/ ]+',s):raise ValueError('Only exact rational entries')
 a=sp.sympify(s)
 if not a.is_Rational:raise ValueError('Rational required')
 return a

def mat(rows):return sp.Matrix([[scalar(x) for x in row] for row in rows])
def tex(m):return matrix_tex([[sp.latex(m[i,j]).replace('- ', '-') for j in range(m.cols)] for i in range(m.rows)],augmented=False)
def serial(m):return [[str(m[i,j]) for j in range(m.cols)] for i in range(m.rows)]
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(NS,x))
def sf(s):return sp.Integer(1) if not s else scalar(s)
def original_parameters(template):
 t=TEMPLATES[template];n=len(t['bases'][0]);return {'permutation':list(range(n)),'signs':[1]*n,'witnesses':[b['witness'] for b in t['blocks']]}
def transform(m,p):
 n=m.rows;return sp.Matrix(n,n,lambda i,j:p['signs'][i]*p['signs'][j]*m[p['permutation'][i],p['permutation'][j]])
def words(truth):
 names=[k for k,v in zip(('I','II','III'),truth) if v];return (' and '.join(names)+' only') if names else 'None'
def relation_roles(t):
 blocks=t['blocks'];pairs=[]
 for b in blocks:
  pair=b['pair'];u=tuple(sorted(pair))
  if u not in [tuple(sorted(v)) for v in pairs]:pairs.append(pair)
 third=re.search(r'III[^$]*\$([^$]+)\$',t['prompt_mask'])[1];m=re.search(r'([A-Z])\s*(=|\\ne)\s*\{?([A-Z])\}?\^',third)
 return pairs,[t['labels'].index(m[1]),t['labels'].index(m[3]),m[2]]
def truths(t,actual):
 pairs,third=relation_roles(t);n=actual[0].rows
 out=[actual[a]*actual[b]==sp.eye(n) and actual[b]*actual[a]==sp.eye(n) for a,b in pairs];a,b,op=third;v=actual[a]*actual[b]==sp.eye(n) and actual[b]*actual[a]==sp.eye(n);return out+[not v if op==r'\ne' else v]
def validate_p(p,t):
 n=len(t['bases'][0]);keys={'permutation','signs','witnesses'}
 if not isinstance(p,dict) or set(p)!=keys:raise ValueError('Exactly permutation, signs, witnesses required')
 if not isinstance(p['permutation'],list) or any(type(x)is not int for x in p['permutation']) or sorted(p['permutation'])!=list(range(n)):raise ValueError('Permutation must cover all coordinates')
 if not isinstance(p['signs'],list) or len(p['signs'])!=n or any(type(x)is not int or x not in (-1,1) for x in p['signs']):raise ValueError('Signs must be exactly ±1')
 bases=[transform(mat(x),p) for x in t['bases']];actual=[m*sf(s) for m,s in zip(bases,t['scales'])]
 if not isinstance(p['witnesses'],list) or len(p['witnesses'])!=len(t['blocks']):raise ValueError('One witness per source stage')
 for b,w in zip(t['blocks'],p['witnesses']):
  a,c=b['pair'];prod=actual[a]*actual[c]
  if b['identity']:
   if w is not None or prod!=sp.eye(n):raise ValueError('Identity stage role changed')
  elif type(w)is not int or not 0<=w<n*n or prod[w//n,w%n]==sp.eye(n)[w//n,w%n]:raise ValueError('Witness must disprove identity')
 return bases,actual

def sample_parameters(t,rng):
 n=len(t['bases'][0]);perm=list(range(n));rng.shuffle(perm);p={'permutation':perm,'signs':[rng.choice((-1,1)) for _ in range(n)],'witnesses':[]}
 actual=[transform(mat(x),p)*sf(s) for x,s in zip(t['bases'],t['scales'])]
 for b in t['blocks']:
  a,c=b['pair'];prod=actual[a]*actual[c];eligible=[i for i in range(n*n) if prod[i//n,i%n]!=sp.eye(n)[i//n,i%n]];p['witnesses'].append(None if b['identity'] else rng.choice(eligible))
 return p

def source_render(t,p,raw):
 bases,actual=validate_p(p,t);replace={f'@@M{i}@@':tex(m) for i,m in enumerate(bases)}
 for i,(b,w) in enumerate(zip(t['blocks'],p['witnesses'])):
  for j,slot in enumerate(b['pair']):replace[f'@@O{i}_{j}@@']=tex(transform(mat(b['raw_operands'][j]),p) if raw else bases[slot])
  a,c=b['pair'];v=actual[a]*actual[c]/sf(b['result_scale']);n=v.rows
  replace[f'@@P{i}@@']=tex(v) if w is None else matrix_tex([[sp.latex(v[r,c]) if r*n+c==w else '∗' for c in range(n)] for r in range(n)],augmented=False)
 def fill(s):
  for k,v in replace.items():s=s.replace(k,v)
  return normalize_prose(s)
 problem,solution=fill(t['prompt_mask']),fill(t['solution_mask'])
 if not raw:
  if t['raw_question'][':question/math-academy-id']=='q-7913':
   # Source mislabeled the third product, while its narrative/operands are AC.
   solution=solution.replace(r'\begin{aligned}AB & ='+tex(bases[0])+tex(bases[2]),r'\begin{aligned}AC & ='+tex(bases[0])+tex(bases[2]))
  if t['raw_question'][':question/math-academy-id']=='q-149820':solution=solution.replace(r'$BC=CB={I}_{3}.$',r'$BC=CB={I}_{4}.$')
  solution=solution.replace('fasle','false')
 return problem,solution,truths(t,actual),actual

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS or type(seed)is not int:raise ValueError('Unknown level or noninteger seed')
 if field_type not in (None,'checkbox',':answer-field.type/checkbox'):raise ValueError('Only source-shaped checkbox fields')
 profile='observed' if profile is None else profile
 if profile not in PROFILES:raise ValueError('Unknown complete profile')
 rng=random.Random(seed)
 eligible=[k for k,t in TEMPLATES.items() if t['level']==level]
 template=rng.choice(eligible) if template is None else template
 if template not in eligible:raise ValueError('Template outside difficulty scope')
 raw=profile=='raw-source'
 t=TEMPLATES[template];parameters=copy.deepcopy(parameters) if parameters is not None else sample_parameters(t,rng);problem,solution,correct,objects=source_render(t,parameters,raw);pairs,third=relation_roles(t);roles={'pairs':pairs,'inverse':third}
 # Names, permutation syntax, profile aliases and witness selection do not inflate
 # assessed-task counts. Actual supplied rational objects and roles define it.
 task=digest({'objects':[serial(m) for m in objects],'roles':roles})
 identity=digest({'version':VERSION,'difficulty':level,'problem':problem,'solution':solution,'banks':[['false','true',v] for v in correct]});qid=uid('question:'+identity);fields=[]
 for i,v in enumerate(correct):
  key=('I','II','III')[i];fid=uid(qid+':field:'+key);choices=[{':answer/id':uid(fid+':'+x),':answer/type':':answer.type/text',':answer/value':x} for x in ('false','true')];rng.shuffle(choices)
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid+':'+str(v).lower())]})
 return {'knowledge_point':{'db_id':17592186087700,'id':str(NS),'title':SOURCE[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'level':level,'seed':seed,'template':template,'profile':profile,'parameters':parameters,'mathematical_fingerprint':task,'content_fingerprint':identity,'source_ids':[TEMPLATES[template]['source_id']],'eligible_for_learning':not raw,'evidence_only':raw,'difficulty_status':'source level retained; signed-coordinate transforms preserve dimensions, products, sparsity and arithmetic magnitudes','python_version':sys.version.split()[0],'sympy_version':sp.__version__}}
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def batch(level,seed,count,template=None,profile=None):
 if type(count)is not int or not 1<=count<=1000:raise ValueError('count must be 1..1000; finite sampler')
 levels=LEVELS if level=='all' else (level,);out=[]
 for lev in levels:
  if lev not in LEVELS:raise ValueError('Unknown level')
  if template is not None and template not in TEMPLATE_CAPACITIES:raise ValueError('Unknown template')
  capacity=TEMPLATE_CAPACITIES[template] if template is not None else CAPACITIES[lev]
  if count>capacity:raise ValueError(f'Finite same-method capacity for {template or lev} is {capacity}; requested {count}')
  seen=set();got=[]
  for attempt in range(max(200,count*80)):
   r=generate(lev,seed+attempt,template=template,profile=profile);f=r['generation']['mathematical_fingerprint']
   if f in seen:continue
   seen.add(f);got.append(r)
   if len(got)==count:break
  if len(got)!=count:raise ValueError(f'Finite same-method bank exhausted for {lev}: found {len(got)} of {count} in bounded search')
  out.extend(got)
 return out
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=('json','markdown'),default='markdown');p.add_argument('--template');p.add_argument('--profile',choices=PROFILES);a=p.parse_args();records=batch(a.difficulty,a.seed,a.count,a.template,a.profile)
 if a.format=='json':print(json.dumps(records,indent=2))
 else:
  for r in records:
   q=r['question'];print(q[':question/problem']+'\n\n'+q[':question/worked-solution']);print(json.dumps(q[':question/answer-fields'],indent=2))

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__=='__main__':main()
