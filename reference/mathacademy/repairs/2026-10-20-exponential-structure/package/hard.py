"""Exact base-e equations with roots; linear roles vary before target selection."""
from fractions import Fraction as F
import json
from pathlib import Path
import random
import uuid
from math_format import checked_math_content,normalize_prose,normalize_tex,validate_generated_record

KP_ID='4d8c6c93-9d15-5482-8130-25bb9cabf008'
VERSION='1.1.0-hard-variation'
COEFFICIENTS=(-5,-4,-3,-2,-1,1,2,3,4,5)
OFFSETS=tuple(range(-9,0))+tuple(range(1,10))
RADICANDS=(2,3,5,7,10,11,13)
INDICES=tuple(range(2,9))
SOURCES=('06bb1232-0a8a-5e1c-9d8b-cb06e8535b98','d0fb4c30-2477-5421-b3da-f8a97304168e','92f78b35-314c-56cd-8815-b47ddfe81b49')

def uid(parent,text):return str(uuid.uuid5(uuid.UUID(parent),text))
def rational(value):
 value=F(value);return ('-'if value<0 else '')+(str(abs(value.numerator))if value.denominator==1 else rf'\frac{{{abs(value.numerator)}}}{{{value.denominator}}}')
def term(a,v):return ('-'if a<0 else '')+(str(abs(a))if abs(a)!=1 else '')+v
def exponent(a,b,v,order):
 av=term(a,v)
 return (str(b)+('+'if a>0 else '')+av)if order=='constant-first'else(av+('+'if b>0 else '')+str(b))
def logarithm(n):return rf'\ln\left({n}\right)'
def root(n,r):return rf'\sqrt{{{n}}}'if r==2 else rf'\sqrt[{r}]{{{n}}}'
def pair(a,b,r):return F(-b,a),F(1,a*r)
def value(a,b,n,r):
 c,k=pair(a,b,r)
 return rational(c)+('+'if k>0 else '-')+(''if abs(k)==1 else rational(abs(k)))+logarithm(n)
def chain(*lines):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(lines)+r'\end{aligned}'+'\n$$'
def solution(a,b,n,r,v,order):
 exp=exponent(a,b,v,order);rhs=root(n,r);ln=logarithm(n)
 moved=rational(F(1,r))+ln+('+'+str(-b)if b<0 else '-'+str(b))
 text='Take the natural logarithm of both sides:\n\n'+chain(rf'\ln\left(e^{{{exp}}}\right)&=\ln\left({rhs}\right)')
 text+='\n\nUse $\\ln(e^u)=u$ and write the root as a fractional power:\n\n'+chain(exp+rf'&=\ln\left({n}^{{1/{r}}}\right)')
 text+='\n\nApply the power rule for logarithms:\n\n'+chain(exp+'&='+rational(F(1,r))+ln)
 text+='\n\nSubtract the constant term, then divide by the signed coefficient of $'+v+'$:\n\n'+chain(term(a,v)+'&='+moved,v+'&='+value(a,b,n,r))
 text+='\n\nTherefore, $'+v+'='+value(a,b,n,r)+'$.'
 return text

def assemble(problem,worked,values,key,metadata):
 problem,worked=map(normalize_prose,(problem,worked));values=list(map(normalize_tex,values))
 if len(values)!=5 or len(set(values))!=5 or not 0<=key<5:raise ValueError('Five distinct choices and one key required')
 qid=uid(KP_ID,json.dumps([problem,sorted(values),values[key]],ensure_ascii=False));fid=uid(qid,'selection')
 choices=[{':answer/id':uid(fid,v),':answer/type':':answer.type/math',':answer/value':v}for v in values]
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[key][':answer/id']]}
 return {'knowledge_point':{'db_id':17592186087689,'id':KP_ID},'question':{':question/id':qid,':question/difficulty':':question.difficulty/hard',':question/problem':problem,':question/worked-solution':worked,':question/answer-fields':[field]},'generation':{'generator_version':VERSION,'template':'affine-root-rhs-radio','profile':'same-skill-role-bank','source_question_ids':list(SOURCES),'domain':'one real unknown; isolated base-e exponential; positive constant root RHS','supported_generalization':'signed nonzero linear coefficients and offsets, variable names and term ordering; no external rearrangement or rounding',**metadata},'assets':{}}

@checked_math_content
def build(roles,key,n,r,v='x',order='variable-first',choice_order=(0,1,2,3,4),seed=None):
 if n not in RADICANDS or r not in INDICES or v not in ('x','y','t')or order not in ('constant-first','variable-first'):raise ValueError('Unsupported root equation parameters')
 if len(roles)!=5 or not 0<=key<5 or sorted(choice_order)!=list(range(5)):raise ValueError('Invalid bank selection')
 if any(a not in COEFFICIENTS or b not in OFFSETS for a,b in roles):raise ValueError('Nonzero bounded linear coefficient and offset required')
 if len({pair(a,b,r)for a,b in roles})!=5:raise ValueError('Equivalent bank choices')
 a,b=roles[key];exp=exponent(a,b,v,order);values=[v+'='+value(c,d,n,r)for c,d in roles]
 return assemble(f'What is the exact value of ${v}$ if $e^{{{exp}}}={root(n,r)}$?',solution(a,b,n,r,v,order),[values[i]for i in choice_order],list(choice_order).index(key),{'parameters':{'a':a,'b':b,'n':n,'r':r,'variable':v,'order':order},'bank_roles':[list(role)for role in roles],'target_role':key,'choice_order':list(choice_order),'decision_case':('positive'if a>0 else 'negative')+'-coefficient/'+('positive'if b>0 else 'negative')+'-offset','seed':seed})

def generate(count,seed):
 if not 0<=count<=6264:raise ValueError('count must be in 0..6264')
 rng=random.Random(seed);records=[];seen=set()
 while len(records)<count:
  # Choose the full answer-bearing bank before choosing its assessed role.
  # All five answers are solutions to comparable signed affine equations.
  roles=rng.sample([(a,b)for a in COEFFICIENTS for b in OFFSETS],5)
  key=rng.randrange(5);n=rng.choice(RADICANDS);r=rng.choice(INDICES);a,b=roles[key]
  semantic=(a,b,n,r)
  if semantic in seen:continue
  seen.add(semantic)
  rec=build(roles,key,n,r,rng.choice(('x','y','t')),rng.choice(('constant-first','variable-first')),tuple(rng.sample(range(5),5)),seed)
  rec['generation']['index']=len(records);records.append(rec)
 return records

def replay_sources():
 records=[]
 for source in json.loads(Path(__file__).with_name('hard-sources.json').read_text()):
  if not source.get(':question/answer-fields'):continue
  f=source[':question/answer-fields'][0];correct=f[':answer-field/correct'][':answer/id'];values=[a[':answer/value']for a in f[':answer-field/choices']];key=next(i for i,a in enumerate(f[':answer-field/choices'])if a[':answer/id']==correct)
  records.append(assemble(source[':question/problem'],source[':question/worked-solution'],values,key,{'profile':'source-replay','source_question_id':source[':question/id'],'source_math_academy_id':source[':question/math-academy-id']}))
 return [validate_generated_record(record) for record in records]
