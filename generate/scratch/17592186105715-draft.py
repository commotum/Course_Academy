#!/usr/bin/env python3
"""Private basis2275 reciprocal integration draft; no database operations.

Observed easy profiles retain their exact algebra and ordered solution operands.
Only documented duplicate wrong primitive families are narrowly repaired. Missing
moderate/hard are authored coefficient calibrations of the same c/x method.
"""
import argparse
import hashlib
import importlib.util
import json
import random
import re
import sys
import uuid
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
# Freeze formatter semantics with this private draft; never import the live helper.
_formatter_path=Path(__file__).with_suffix('')/'math_format.py'
_formatter_spec=importlib.util.spec_from_file_location('reciprocal_private_math_format',_formatter_path)
_formatter=importlib.util.module_from_spec(_formatter_spec)
_formatter_spec.loader.exec_module(_formatter)
normalize_prose=_formatter.normalize_prose
normalize_tex=_formatter.normalize_tex
validate_generated_record=_formatter.validate_generated_record
KP_ID=17592186105715
KP_UUID='cf98ee24-7774-5674-8a1e-63f4f6d225c0'
TITLE='Integrating a Reciprocal Function'
VERSION='reciprocal-draft-2275-1'
SOURCE_BASIS=2275
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
HERE=Path(__file__).with_suffix('')
TEMPLATES=json.loads((HERE/'templates.json').read_text())
LEVELS=('easy','moderate','hard')
SUPPORTED_LEVELS=LEVELS
X=sp.Symbol('x',real=True)
C=sp.Symbol('C',real=True)
SQUAREFREE=(2,3,5,6,7,10,11,13,14,15)
REPAIRS={'q-29934':1,'q-103369':2,'q-103590':3,'q-29831':0}

def integer(value,name):
 if type(value) is not int:raise ValueError(name+' must be an integer')
 return value

def clean(text,answer=False):
 text=text.replace('⁡','').replace(r'\u2061','').replace(r'\operatorname{ln}',r'\ln ')
 if answer:text=text.replace('\\\\','\\')
 text=re.sub(r'(?<![a-z\\])ln',lambda _:r'\ln ',text)
 return normalize_tex(text) if answer else normalize_prose(text)

def render(text,p,answer=False):
 for key,value in p.items():text=text.replace('@@'+key+'@@',str(value))
 if '@@' in text:raise ValueError('Unfilled slot')
 return clean(text,answer)

def coefficient(kind,p):
 n=p.get('n');a=p.get('a',1)
 if kind=='integer':return sp.Integer(n)
 if kind=='negative_integer':return -sp.Integer(n)
 if kind=='reciprocal':return sp.Rational(1,n)
 if kind=='radical':return a/sp.sqrt(n)
 if kind=='negative_radical':return -a/sp.sqrt(n)
 if kind=='negative_rational':return -sp.Rational(p['a'],p['b'])
 raise ValueError('Unknown coefficient structure')

def domain(level,template=None):
 if level not in LEVELS:raise ValueError('Unsupported level')
 template=template or ('q-103369' if level=='easy' else 'rational-authored' if level=='moderate' else 'radical-authored')
 if level=='moderate':
  if template!='rational-authored':return []
  return [{'a':a,'b':b} for a in range(2,15) for b in range(2,16) if sp.gcd(a,b)==1]
 if level=='hard':
  if template!='radical-authored':return []
  return [{'a':a,'n':n} for a in range(2,10) for n in SQUAREFREE]
 if template not in TEMPLATES:return []
 kind=TEMPLATES[template]['kind']
 if kind=='negative_rational':return [{'a':a,'b':b} for a in range(2,8) for b in range(2,12) if sp.gcd(a,b)==1]
 if kind in ('radical','negative_radical'):return [{'n':n} for n in SQUAREFREE]
 return [{'n':n} for n in range(2,21)]

def uid(text):return str(uuid.uuid5(uuid.UUID(KP_UUID),text))
def fingerprint(c):return sp.srepr(sp.simplify(c))
def templates(level):return list(TEMPLATES) if level=='easy' else ['rational-authored'] if level=='moderate' else ['radical-authored']

def spec_for(level,template):
 if template in TEMPLATES:return TEMPLATES[template]
 if level=='moderate' and template=='rational-authored':return TEMPLATES['q-71098']
 if level=='hard' and template=='radical-authored':
  t=dict(TEMPLATES['q-72059'])
  t['problem']=t['problem'].replace(r'-\frac{1}',r'-\frac{@@a@@}')
  t['solution']=t['solution'].replace(r'-\frac{1}',r'-\frac{@@a@@}').replace(r'-\frac{\sqrt{@@n@@}}',r'-\frac{@@a@@\sqrt{@@n@@}}')
  t['values']=[v.replace(r'-\frac{\sqrt{@@n@@}}',r'-\frac{@@a@@\sqrt{@@n@@}}').replace(r'-\frac{1}',r'-\frac{@@a@@}').replace(r'-\frac{@@n@@}',r'-\frac{@@an@@}').replace('-ln', '-@@a@@ln') for v in t['values']]
  return t
 raise ValueError('Template/level mismatch')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 integer(seed,'seed')
 if level not in LEVELS:raise ValueError('Unsupported level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio fields')
 rng=random.Random(seed)
 template=template or rng.choice(templates(level))
 if template not in templates(level):raise ValueError('Template/level mismatch')
 t=spec_for(level,template)
 default='repaired' if template in REPAIRS else 'observed' if template in TEMPLATES else 'authored'
 profile=profile or default
 if profile==template:profile=default
 if profile not in ('raw',default):raise ValueError('Unsupported complete bank profile')
 if profile=='raw' and template not in TEMPLATES:raise ValueError('Authored profile has no source raw bank')
 p=dict(parameters) if parameters is not None else dict(rng.choice(domain(level,template)))
 if any(type(v) is not int for v in p.values()) or p not in domain(level,template):raise ValueError('Outside bounded domain')
 c=coefficient(t['kind'],p)
 rp=p|{'an':p.get('a',1)*p.get('n',1)}
 problem=render(t['problem'],rp)
 solution=render(t['solution'],rp)
 values=[render(v,rp,True) for v in t['values']]
 if profile!='raw' and template in REPAIRS:
  values[REPAIRS[template]]=render(r'-\frac{1}{@@n@@}\ln|x|+C' if template=='q-29831' else r'-@@n@@\ln|x|+C',p,True)
 key=json.dumps([VERSION,level,problem,solution,sorted(values),profile],separators=(',',':'))
 qid=uid('question:'+key);fid=uid('field:'+qid+':selection')
 answers=[{':answer/id':uid('answer:'+fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 correct=answers[t['correct_index']][':answer/id']
 # Option ordering depends only on recorded seed, never on optional sampler calls.
 random.Random(seed).shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':t['field_key'],':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[field]}
 if profile=='raw' and template=='q-29934':
  del q[':question/difficulty'];del q[':question/worked-solution'];del field[':answer-field/correct']
 result={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'profile':profile,'parameters':p,'coefficient':str(c),'mathematical_fingerprint':fingerprint(c),'parameter_fingerprint':fingerprint(c),'source_basis':SOURCE_BASIS,'lineage':LINEAGE,'source_references':[template] if template in TEMPLATES else ['q-71098' if level=='moderate' else 'q-72059'],'authored_difficulty':level!='easy' or template=='q-29934','evidence_only':profile=='raw','eligible_for_learning':profile!='raw','domains':['x>0','x<0'],'plot_requirements':'none','source_error_repair':template if profile=='repaired' else None,'dependencies':{'sympy':sp.__version__},'math_format':'course-academy-tex-v1'}}
 return result if profile=='raw' else validate_generated_record(result)

def catalog(level):
 seen=set();out=[]
 for template in templates(level):
  for p in domain(level,template):
   fp=fingerprint(coefficient(spec_for(level,template)['kind'],p))
   if fp not in seen:seen.add(fp);out.append((template,p))
 return out

def batch(level,count,seed=0,template=None,profile=None):
 integer(count,'count');integer(seed,'seed')
 if count<0:raise ValueError('count must be nonnegative')
 if level not in LEVELS:raise ValueError('Unsupported level')
 pool=catalog(level) if template is None else [(template,p) for p in domain(level,template)]
 if template is not None and template not in templates(level):raise ValueError('Template/level mismatch')
 if count>len(pool):raise ValueError('count exceeds meaningful mathematical capacity '+str(len(pool)))
 random.Random(seed).shuffle(pool)
 return [generate(level,seed,mid,parameters=p,profile=profile) for mid,p in pool[:count]]

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','')

def main():
 a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=(*LEVELS,'all'),required=True);a.add_argument('--count',type=int,default=1);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=('json','markdown'),default='json');a.add_argument('--template');a.add_argument('--profile');p=a.parse_args()
 try:rows=[r for level in LEVELS if p.difficulty in ('all',level) for r in batch(level,p.count,p.seed,p.template,p.profile)]
 except ValueError as e:a.error(str(e))
 print(json.dumps(rows,indent=2) if p.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
if __name__=='__main__':main()
