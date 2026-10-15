#!/usr/bin/env python3
"""Natural-log substitution. Bounded source bank profiles; no database writes."""
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
try:
 import sympy as sp
except ImportError:
 import os
 executable=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 os.execv(str(executable),[str(executable),__file__,*sys.argv[1:]])
H=Path(__file__).with_suffix(''); SOURCE=json.loads((H/'source.json').read_text())['record']
KP_ID=17592186068724; KP_UUID=SOURCE[':knowledge-point/id']; TITLE=SOURCE[':knowledge-point/title']
VERSION='68724-draft-v2'; GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'));SUPPORTED_LEVELS=('easy','moderate','hard')
X=sp.Symbol('x',real=True);T=sp.Symbol('t',real=True)
# source, band, numerator scale k, denominator a*x^n+b*x+c, n, variable
CASES=[('q-132982','easy',-16,2,0,3,2,'t'),('q-12501','easy',1,1,0,10,3,'x'),('q-49451','easy',4,1,0,1,2,'x'),('q-49572','easy',1,1,0,9,10,'x'),('q-72605','easy',10,-5,0,2,5,'x'),('q-72566','moderate',1,1,-1,0,3,'x'),('q-113719','moderate',1,-1,1,1,4,'x'),('q-113720','moderate',1,1,-1,0,5,'x'),('q-113721','moderate',1,1,2,0,2,'x')]
SOURCES={q.get(':question/math-academy-id',str(q[':db/id'])):q for q in SOURCE[':knowledge-point/questions']}
def case(t):return next(c for c in CASES if c[0]==t)
def defaults(c):return dict(zip(('k','a','b','c','n','variable'),c[2:]))
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def digest(x):return hashlib.sha256(str(x).encode()).hexdigest()
def tex(x):return sp.latex(x,order='lex')
def data(p,level):
 k,a,b,c,n=(sp.Rational(p[z])for z in ('k','a','b','c','n'));z=T if p['variable']=='t'else X
 u=a*z**n+b*z+c;v=sp.diff(u,z);numerator=k*z**(n-1)if level=='easy'else v
 ratio=k/(a*n)if level=='easy'else sp.Integer(1)
 return z,u,v,numerator,sp.cancel(numerator/u),ratio
# All dependencies are private file loads; sys.path and mutable shared helpers are unused.
import copy,importlib.util,itertools,re,functools
sys.dont_write_bytecode=True
def private(name):
 spec=importlib.util.spec_from_file_location('kp68724_'+name,H/(name+'.py'));mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
FORMAT=private('math_format');PARSER=private('parser')
TEMPLATES=json.loads((H/'templates.json').read_text())
PARAM_KEYS=('k','a','b','c','n','variable')
def integer(value,name):
 if type(value) is not int:raise TypeError(name+' must be a built-in int')
 return value

def operands(t,p):
 z,u,v,num,f,r=data(p,case(t)[1]);return dict(u=u,v=v,shifted=p['a']*z**p['n']+p['b']+p['c'],altered=p['n']*p['a']*z**(p['n']-1)+p['b']*z+p['c'],reciprocal_c=sp.Rational(1,p['c']) if p['c'] else None,c=sp.Integer(p['c']))
def render(t,p):
 spec=TEMPLATES[t];old=defaults(case(t));original=operands(t,old);actual=operands(t,p)
 # Named mathematical operands are slots. Unchanged operands retain their source
 # lexemes, so exact source replay and genuine variants share this renderer.
 mapping={key:(lexeme if sp.simplify(actual[key]-original[key])==0 else tex(actual[key]))for key,lexeme in spec['original_lexemes'].items()}
 def subst(text):
  return re.sub(r'@@(\w+)@@',lambda m:mapping[m[1]],text)
 return subst(spec['problem']),subst(spec['solution']),[subst(a)for a in spec['answers']]

def parameter_domain(t,level):
 base=defaults(case(t))
 if level=='hard':
  for a,b,c in itertools.product((-2,-3),(2,3,4),range(2,9)):yield dict(base,a=a,b=b,c=c)
 else:
  slot='c'if level=='easy'or t=='q-113719'else'b'
  for n in range(1,20 if t=='q-132982'else 21 if slot=='c'else 13):yield dict(base,**{slot:n*(1 if base[slot]>=0 else -1)})
def checked_parameters(t,level,p):
 if type(p) is not dict or set(p)!=set(PARAM_KEYS):raise ValueError('complete typed parameter mapping required')
 for k in PARAM_KEYS[:-1]:integer(p[k],k)
 if type(p['variable']) is not str:raise TypeError('variable must be str')
 if p not in list(parameter_domain(t,level)):raise ValueError('outside bounded certified parameter domain')
 return dict(p)
def task_fingerprint(q):return digest(sp.srepr(sp.cancel(PARSER.prompt(q[':question/problem']))))
def valid_bank(t,p,values):
 z,u,v,num,f,r=data(p,case(t)[1]);vals=[PARSER.scalar(s)for s in values];derivatives=[sp.cancel(sp.diff(a,z))for a in vals]
 if any(sp.cancel(a-b)==0 for i,a in enumerate(derivatives)for b in derivatives[i+1:]):return False
 return [i for i,d in enumerate(derivatives)if sp.cancel(d-f)==0]==[TEMPLATES[t]['correct']]
_uncached_valid_bank=valid_bank
@functools.lru_cache(maxsize=2048)
def _cached_valid_bank(t,items,values):return _uncached_valid_bank(t,dict(items),values)
def valid_bank(t,p,values):return _cached_valid_bank(t,tuple(p.items()),tuple(values))
def eligible(level):return ['authored-hard']if level=='hard'else[c[0]for c in CASES if c[1]==level]
def generate(level,seed=0,template=None,parameters=None,profile=None,option_seed=None):
 integer(seed,'seed')
 if option_seed is not None:integer(option_seed,'option_seed')
 if level not in SUPPORTED_LEVELS:raise ValueError('unknown difficulty')
 if profile=='reference':
  if template not in SOURCES:raise ValueError('unknown reference')
  return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':copy.deepcopy(SOURCES[template]),'generation':{'template':template,'profile':'reference','source_basis':2275,'reference_only':True}}
 if profile not in (None,'source'):raise ValueError('unknown profile')
 rng=random.Random(seed);selected=template if template is not None else rng.choice(eligible(level))
 if selected not in eligible(level):raise ValueError('template difficulty mismatch')
 t='q-113719'if selected=='authored-hard'else selected
 if parameters is not None:p=checked_parameters(t,level,parameters)
 else:
  domain=list(parameter_domain(t,level));rng.shuffle(domain)
  p=next((p for p in domain if valid_bank(t,p,render(t,p)[2])),None)
  if p is None:raise ValueError('empty domain')
 problem,solution,values=render(t,p)
 if not valid_bank(t,p,values):raise ValueError('whole-bank antiderivative collision')
 original=SOURCES[t];sourcefield=original[':question/answer-fields'][0];correct=TEMPLATES[t]['correct']
 fp=digest(sp.srepr(data(p,case(t)[1])[4]));qid=uid(VERSION+':'+level+':'+selected+':'+fp);fid=uid(qid+':'+sourcefield[':answer-field/key'])
 answers=[{':answer/id':uid(fid+':'+s),':answer/type':':answer.type/math',':answer/value':s}for s in values];correct_id=answers[correct][':answer/id']
 if option_seed is not None:random.Random(option_seed).shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':sourcefield[':answer-field/key'],':answer-field/type':sourcefield[':answer-field/type'][':db/ident'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[field]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_version':VERSION,'template':selected,'bank_profile':t,'profile':'source','seed':seed,'option_seed':option_seed,'parameters':p,'source_basis':2275,'source_lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','source_question_id':original[':db/id'],'authored_extension':level=='hard','domain':'Each real connected interval where the displayed denominator is nonzero; logarithms of absolute values. For the positive quadratic blank the domain is all real numbers.','mathematical_fingerprint':fp,'sympy_version':sp.__version__,'plots':'none'}}
def all_instances(level,template=None):
 for selected in ([template]if template else eligible(level)):
  if selected not in eligible(level):raise ValueError('template difficulty mismatch')
  t='q-113719'if selected=='authored-hard'else selected
  for p in parameter_domain(t,level):
   if valid_bank(t,p,render(t,p)[2]):yield selected,p

def batch(level,count,seed=0,template=None):
 integer(count,'count');integer(seed,'seed')
 if level not in SUPPORTED_LEVELS:raise ValueError('unknown difficulty')
 if count<0:raise ValueError('negative count')
 candidates=list(all_instances(level,template));random.Random(seed).shuffle(candidates);seen=set();records=[]
 for t,p in candidates:
  rec=generate(level,seed,t,p);fp=rec['generation']['mathematical_fingerprint']
  if fp not in seen:records.append(rec);seen.add(fp)
  if len(records)==count:break
 if count==0:return []
 if len(records)!=count:raise ValueError('count exceeds finite distinct mathematical task capacity: '+str(len(records)))
 return records
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),required=True);parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--template');parser.add_argument('--format',choices=('json','markdown'),default='json');args=parser.parse_args()
 try:
  records=[r for level in (SUPPORTED_LEVELS if args.difficulty=='all'else[args.difficulty])for r in batch(level,args.count,args.seed,args.template)]
  print(json.dumps(records,indent=2)if args.format=='json'else'\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']for r in records))
 except (ValueError,TypeError)as e:parser.exit(2,str(e)+'\n')
