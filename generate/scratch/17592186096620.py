#!/usr/bin/env python3
"""Source-derived easy quotient-rule templates. Pure generation; no database writes.

All parameters are exact bounded integers. Source examples with missing prompt
context or answer fields have explicitly labeled self-contained blank extensions.
Unobserved levels are unsupported by this version, rather than inferred from absence.
"""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186096620-source-policy.json'))
    raise SystemExit(0)

import argparse
import hashlib
import json
import random
import uuid
from pathlib import Path
import sympy as sp

HERE = Path(__file__).with_suffix('')
RAW = json.loads((HERE / 'source.json').read_text())
KP_ID = 17592186096620
KP_UUID = RAW['kp'][':knowledge-point/id']
TITLE = RAW['kp'][':knowledge-point/title']
GENERATOR_ID = str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy:question-generator:' + KP_UUID))
VERSION = 'polynomial-quotients-1'
SUPPORTED_LEVELS = ('easy',)
X, K = sp.symbols('x k', real=True)

# Separate prompt/solution/response structures, even when algebra overlaps.
TEMPLATES = {
 'q-11955': {'kind':'constant-linear','parameters':{'c':-2,'a':4,'b':-9},'field':'radio','profile':'observed-11955','stages':3},
 'q-11966': {'kind':'linear-linear','parameters':{'c':-5,'a':2,'b':-1},'field':'radio','profile':'observed-11966','stages':4,'extension':'Unrated source without solution/correct ref; easy analog q-340297; correct designation computed.'},
 'q-104305': {'kind':'constant-quadratic','parameters':{'c':10,'a':-1,'b':0,'d':3},'field':'blank','profile':'fragment','stages':3,'extension':'Missing source field; explicit blank extension from observed blank response shape.'},
 'q-104309': {'kind':'affine-quadratic','parameters':{'c':-2,'e':3,'a':2,'b':0,'d':-2},'field':'blank','profile':'fragment','stages':5,'extension':'Missing source field; explicit blank extension from observed blank response shape.'},
 'q-340290': {'kind':'constant-monomial','parameters':{'c':2},'field':'blank','profile':'fragment','stages':4},
 'q-128235': {'kind':'symbolic-quadratic','parameters':{'e':-2,'b':4},'field':'blank','profile':'fragment','stages':4,'extension':'Source prompt omits function; supply u/v definitions from captured solution. k is constant.'},
 'q-128335': {'kind':'constant-quadratic','parameters':{'c':7,'a':2,'b':-5,'d':-3},'field':'blank','profile':'fragment','stages':4,'extension':'Source prompt omits function; supply u/v definitions from captured solution.'},
 'q-340287': {'kind':'constant-unit-linear','parameters':{'c':1,'b':1},'field':'blank','profile':'fragment','stages':4},
 'q-340297': {'kind':'linear-linear','parameters':{'c':6,'a':-3,'b':1},'field':'blank','profile':'fragment','stages':4},
 'q-340298': {'kind':'square-linear','parameters':{'b':1},'field':'blank','profile':'fragment','stages':4},
 'q-340303': {'kind':'linear-unit-quadratic','parameters':{'b':1},'field':'blank','profile':'fragment','stages':4},
}

def digest(value):
 return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

def uid(value):
 return str(uuid.uuid5(uuid.UUID(GENERATOR_ID), value))

def tex(value):
 return sp.latex(value)

def derivative_tex(u,v):
 """Retain the source's squared denominator until a real cancellation occurs."""
 n=sp.expand(sp.diff(u,X)*v-u*sp.diff(v,X))
 content=sp.Poly(v,X).content()
 base=sp.cancel(v/content);top=sp.cancel(n/content**2)
 if sp.Poly(sp.gcd(top,base),X).degree()>0:
  return tex(sp.factor(sp.cancel(sp.diff(u/v,X))))
 return r'\frac{'+tex(top)+'}{'+tex(sp.Pow(base,2,evaluate=False))+'}'

def parts(template, p):
 kind = TEMPLATES[template]['kind']
 if kind == 'constant-linear': return sp.Integer(p['c']), p['a']*X+p['b']
 if kind == 'linear-linear': return p['c']*X, p['a']*X+p['b']
 if kind == 'constant-quadratic': return sp.Integer(p['c']), p['a']*X**2+p['b']*X+p['d']
 if kind == 'affine-quadratic': return p['c']*X+p['e'], p['a']*X**2+p['b']*X+p['d']
 if kind == 'constant-monomial': return sp.Integer(p['c']), X**2
 if kind == 'symbolic-quadratic': return X+p['e'], X**2+p['b']*X+K
 if kind == 'constant-unit-linear': return sp.Integer(p['c']), X+p['b']
 if kind == 'square-linear': return X**2, X+p['b']
 if kind == 'linear-unit-quadratic': return X, X**2+p['b']
 raise ValueError(kind)

def parameters(template, seed):
 r = random.Random(seed)
 keys = TEMPLATES[template]['parameters']
 for _ in range(300):
  p = {key:r.randint(-12,12) for key in keys}
  try: validate_parameters(template,p); answer_bank(template,p)
  except ValueError: continue
  return p
 raise ValueError('Bounded sampler could not produce a valid complete bank')

def validate_parameters(template, p):
 if set(p) != set(TEMPLATES[template]['parameters']): raise ValueError('Wrong parameter keys')
 if any(type(z) is not int or not -12 <= z <= 12 for z in p.values()): raise ValueError('Integer parameters in -12..12 required')
 if any(p[key] == 0 for key in ('c','a') if key in p): raise ValueError('Nonzero numerator and leading denominator coefficients required')
 if TEMPLATES[template]['kind'] in ('linear-linear','square-linear') and p['b']==0: raise ValueError('Nonconstant quotient required')
 u,v = parts(template,p)
 if sp.diff(u/v,X)==0: raise ValueError('Constant quotient excluded')

def answer_bank(template,p):
 u,v = parts(template,p)
 correct = sp.cancel(sp.diff(u/v,X))
 profile = TEMPLATES[template]['profile']
 if profile == 'observed-11955':
  c,a,b = map(sp.Integer,(p['c'],p['a'],p['b']))
  if b==0: raise ValueError('Observed profile requires nonzero b')
  # Complete sparse observed algebraic patterns; misconception interpretation
  # remains unresolved. Never pool recipes or invent explanatory feedback.
  numerators = [-c*a/(-b),-c,-c*a,-c/2,-a]
  values = [n/v**2 for n in numerators]
 elif profile == 'observed-11966':
  c,a,b = map(sp.Integer,(p['c'],p['a'],p['b']))
  values = [(-c*a*X+c*b)/v**2,(-2*c*a*X+c*b)/v**2,c*b/v**2,(c*b+c*a*X)/v**2,-c*b/v**2]
 else: values = [correct]
 if sum(sp.cancel(z-correct)==0 for z in values)!=1: raise ValueError('Bank lacks a unique correct option')
 if any(sp.cancel(z-y)==0 for i,z in enumerate(values) for y in values[:i]): raise ValueError('Complete bank collides')
 return values,correct

def generate(level,seed=0,template=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS: raise ValueError('Unsupported difficulty: see capabilities.json')
 template = template or random.Random(seed).choice(list(TEMPLATES))
 if template not in TEMPLATES: raise ValueError('Unknown template')
 t = TEMPLATES[template]
 if profile not in (None,t['profile']): raise ValueError('Profile is not eligible for this template')
 p = parameters if parameters is not None else globals()['parameters'](template,seed)
 validate_parameters(template,p)
 values,correct = answer_bank(template,p)
 u,v = parts(template,p); du,dv = sp.diff(u,X),sp.diff(v,X)
 numerator = sp.expand(du*v-u*dv)
 fraction = lambda n,d:r'\frac{'+tex(n)+'}{'+tex(d)+'}'
 prompt = 'Given that $f(x)='+fraction(u,v)+r'$, find $f^{\prime}(x).$'
 if template in ('q-128235','q-128335'):
  prompt = ('Find the derivative of $f(x)='+fraction(u,v)+r'.$' if template=='q-128235' else r'Calculate $f^{\prime}(x)$ for $f(x)='+fraction(u,v)+r'.$')
 if K in v.free_symbols: prompt += ' Treat $k$ as a constant.'
 if t['field']=='blank': prompt += '\n\n'+r'$f^{\prime}(x)=$'+'\n{{field-1}}'
 worked = 'The numerator and denominator are $u(x)='+tex(u)+'$ and $v(x)='+tex(v)+',$ respectively. Their derivatives are given by\n\n$$\n'+r'\begin{aligned}u^{\prime}(x)&='+tex(du)+r',\\v^{\prime}(x)&='+tex(dv)+r'.\end{aligned}'+'\n$$\n\nApplying the quotient rule, we have\n\n'
 rows = [r'\frac{u^{\prime}(x)\cdot v(x)-u(x)\cdot v^{\prime}(x)}{[v(x)]^2}',
  r'\frac{('+tex(du)+r')\cdot ('+tex(v)+')-('+tex(u)+r')\cdot ('+tex(dv)+r')}{('+tex(v)+r')^2}']
 if t['stages'] >= 4: rows.append(fraction(numerator,sp.Pow(v,2,evaluate=False)))
 if t['stages'] == 5:
  # Same quotient simplification sequence as the affine/quadratic source.
  content=sp.Poly(v,X).content()
  rows.append(fraction(sp.cancel(numerator/content**2),sp.Pow(v/content,2,evaluate=False)))
 rows.append(derivative_tex(u,v))
 worked += '$$\n'+r'\begin{aligned}f^{\prime}(x)&='+r'\\ &='.join(rows)+r'.\end{aligned}'+'\n$$'
 task = digest([sp.srepr(correct),sp.srepr(sp.cancel(v/sp.Poly(v,X).LC()))])
 # Content identity retains response shape and complete profile; mathematical
 # task identity excludes bank, layout, seed and option order.
 rendered_values=[tex(z) for z in values] if t['field']=='radio' else [derivative_tex(u,v)]
 content = digest([VERSION,prompt,worked,t['field'],sorted(rendered_values),derivative_tex(u,v)])
 qid = uid('question:'+content); key='selection' if t['field']=='radio' else 'field-1'; fid=uid('field:'+qid+':'+key)
 choices=[{':answer/id':uid('answer:'+fid+':'+sp.srepr(sp.cancel(z))),':answer/type':':answer.type/math',':answer/value':value} for z,value in zip(values,rendered_values)]
 cid=next(a[':answer/id'] for a,z in zip(choices,values) if sp.cancel(z-correct)==0)
 random.Random(seed).shuffle(choices)
 field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+t['field'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',cid]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':worked,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'template':template,'profile':t['profile'],'parameters':p,'source_ids':[template],'source_basis':RAW['basis'],'source_lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','math_fingerprint':task,'content_fingerprint':content,'domain':tex(v)+r'\ne 0','extension':t.get('extension'),'plot_rating':'none','sympy_version':sp.__version__,'python_random':'random.Random'}}

def generate_easy(seed=0,**kw): return generate('easy',seed,**kw)

def batch(level,count,seed=0,template=None,profile=None):
 if level not in SUPPORTED_LEVELS: raise ValueError('Unsupported difficulty: see capabilities.json')
 if not 0<=count<=1000: raise ValueError('Requested count outside bounded batch policy 0..1000')
 records=[];seen=set()
 for i in range(max(300,count*100)):
  if len(records)==count: break
  rec=generate(level,seed+i,template,profile=profile)
  fp=rec['generation']['math_fingerprint']
  if fp not in seen: seen.add(fp);records.append(rec)
 if len(records)!=count: raise ValueError(f'Finite-limit: {len(records)} distinct tasks found within bounded search')
 return records

def markdown(rec):
 q=rec['question']
 return q[':question/problem']+'\n\n'+'\n'.join('$'+a[':answer/value']+'$' for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']


from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186096620-source-policy.json'))

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 levels=SUPPORTED_LEVELS if a.difficulty=='all' else (a.difficulty,)
 try: records=[r for level in levels for r in batch(level,a.count,a.seed,a.template,a.profile)]
 except ValueError as error: ap.error(str(error))
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
