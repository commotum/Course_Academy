#!/usr/bin/env python3
"""Source-faithful checkbox ODE classification, bounded monomial substitution.

Easy/moderate retain observed question layouts, worked-solution wording and all
three field-owned true/false banks. x^d -> x^(d*k), k=1..6, is an explicit
extension of source polynomial degrees. k=1 replays every source verbatim.
Hard is unsupported in this package: no rated hard source establishes a template.
"""
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
try:
 import sympy as sp
except ModuleNotFoundError:
 for p in (Path(__file__).resolve().parents[2]/'.venv/lib').glob('python*/site-packages'):sys.path.insert(0,str(p))
 import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
KP_ID=17592186087868
KP_UUID='739a8f10-413a-5a1d-a47e-4afd0b14eb44'
TITLE='Identifying Homogeneous and Inhomogeneous ODEs'
VERSION='homogeneous-ode-checkbox-v1'
PACKAGE=Path(__file__).with_suffix('')
SOURCE=json.loads((PACKAGE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
SUPPORTED_LEVELS=('easy','moderate')
DOMAIN=tuple(range(1,7))
GENERATOR_ID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
GENERATOR_UUID=GENERATOR_ID
X,Y,D=sp.symbols('x y D')

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def level(q):
 d=q[':question/difficulty'];return (d[':db/ident'] if isinstance(d,dict) else d).split('/')[-1]
def substitute(text,k):
 if k==1:return text
 def monomial(m):
  degree=int(m[1] or m[2] or 1)*k
  return '{x}^{'+str(degree)+'}'
 # P(x), Q(x) denote arbitrary coefficient functions, not a sampled monomial.
 text=text.replace('P(x)','P(@)').replace('Q(x)','Q(@)')
 return re.sub(r'(?<![A-Za-z])(?:\{x\}|x)(?:\^\{(\d+)\}|\^(\d+))?',monomial,text).replace('P(@)','P(x)').replace('Q(@)','Q(x)')
def expression(s):
 s=s.replace('{y}^{′}','D').replace("y'",'D').replace('y^\\prime','D')
 s=re.sub(r'\^\{(\d+)\}',r'**\1',s);s=re.sub(r'\^(\d+)',r'**\1',s)
 s=s.replace('{','').replace('}','').replace('&','').strip().rstrip('.')
 assert re.fullmatch(r'[x yD0-9+*().\-\s]+',s),s
 return sp.expand(parse_expr(s,local_dict={'x':X,'y':Y,'D':D},transformations=standard_transformations+(implicit_multiplication_application,)))
def equation(s):
 l,r=s.split('=');e=sp.expand(expression(l)-expression(r));a=e.coeff(D)
 assert a==1 and sp.diff(e,Y,2)==0 and sp.diff(e,D,2)==0
 p=sp.expand(e.coeff(Y));q=sp.expand(-(e-D-p*Y));assert not q.has(Y,D)
 return p,q

def prompt_equations(q):
 p=q[':question/problem']
 matches=re.findall(r'- \*\*(I|II|III)\.\*\* \$([^$]+)\$',p)
 assert [key for key,_ in matches]==['I','II','III']
 return [(key,equation(s)) for key,s in matches]
def fingerprint(q):
 # Equivalent equations, changed choice order, seeds and target labels do not
 # create a new set of mathematical tasks.
 eq=sorted([(sp.srepr(p),sp.srepr(v)) for _,(p,v) in prompt_equations(q)])
 return digest(['linear-ode-classification',eq])

def generate(difficulty='easy',seed=0,*,template=None,k=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('unsupported: no hard source template; hard shortage remains explicit')
 rng=random.Random(seed)
 eligible=[mid for mid,q in SOURCES.items() if level(q)==difficulty]
 template=template or rng.choice(eligible);k=rng.choice(DOMAIN) if k is None else k
 if template not in eligible or type(k) is not int or k not in DOMAIN:raise ValueError('Unsupported template or degree multiplier outside 1..6')
 source=SOURCES[template]
 q={':question/problem':substitute(source[':question/problem'],k),':question/worked-solution':substitute(source[':question/worked-solution'],k),':question/difficulty':':question.difficulty/'+difficulty}
 semantic=fingerprint(q);qid=uid([VERSION,semantic]);q[':question/id']=qid;q[':question/answer-fields']=[]
 target='inhomogeneous' in q[':question/problem'].splitlines()[0]
 for key,(p,forcing) in prompt_equations(q):
  correct=(forcing!=0) if target else (forcing==0)
  fid=uid([qid,key]);answers=[{':answer/id':uid([fid,value]),':answer/type':':answer.type/text',':answer/value':value} for value in ['false','true']]
  q[':question/answer-fields'].append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':answers,':answer-field/correct':[':answer/id',uid([fid,str(correct).lower()])]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'template':template,'profile':'three-checkbox-boolean-banks','seed':seed,'parameters':{'k':k},'mathematical_key':semantic,'source_basis':SOURCE['basis'],'source_question':template,'domain':'Real x; polynomial coefficient functions and unit y-prime coefficient','extensions':['Monomial degrees multiplied by integer k in 1..6; source k=1 preserved'],'dependencies':{'sympy':sp.__version__}}}
def candidates(difficulty,seed=0):
 if difficulty not in SUPPORTED_LEVELS:generate(difficulty,seed)
 out={}
 for mid,q in SOURCES.items():
  if level(q)==difficulty:
   for k in DOMAIN:
    r=generate(difficulty,seed,template=mid,k=k);out.setdefault(r['generation']['mathematical_key'],r)
 rows=list(out.values());random.Random(seed).shuffle(rows);return rows
def batch(difficulty,count,seed):
 rows=candidates(difficulty,seed)
 if type(count) is not int or count<1 or count>len(rows):raise ValueError(f'finite-limit: {len(rows)} genuinely distinct {difficulty} tasks in bounded package')
 return rows[:count]
def markdown(r):return r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args()
 try:rows=batch(a.difficulty,a.count,a.seed)
 except ValueError as e:p.error(str(e))
 print(json.dumps(rows,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
