#!/usr/bin/env python3
"""Exhaustive finite-domain truth, source fidelity, schema, native grading QA."""
import hashlib, importlib.util, itertools, json, re, subprocess, sys, uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('cosine',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.loads((HERE/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};cases=json.loads((HERE/'source-cases.json').read_text())
n=sp.Symbol('n',integer=True)
def expr(raw):
 raw=raw.strip(' .');raw=raw.replace('π',r'\pi').replace(r'\pi','pi')
 raw=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',raw)
 raw=raw.replace(' ','').replace('⁡','').replace('…','')
 raw=re.sub(r'(\d)(pi|n)',r'\1*\2',raw);raw=raw.replace('npi','n*pi').replace('pin','pi*n')
 return sp.sympify(raw,locals={'pi':sp.pi,'n':n})
def printed_truth(line):
 math=re.findall(r'\$([^$]+)\$',line)
 if 'range' in line:
  m=re.search(r'\[([^,]+),([^\]]+)\]',line);return expr(m[1])==-1 and expr(m[2])==1
 if 'output' in line:
  val=expr(next(x.split('=',1)[1] for x in math if x.startswith('y=')));return bool(-1<=val<=1)
 if 'passes through' in line:
  x,y=next(x.strip('()').split(',') for x in math if x.startswith('('));return sp.cos(expr(x))==expr(y)
 if 'axis at' in line and any(x.startswith('y=') for x in math):return expr(next(x.split('=',1)[1] for x in math if x.startswith('y=')))==1
 x=expr(next(x.split('=',1)[1] for x in math if re.match(r'x\s*=',x)))
 target=0 if 'zero' in line or '$x$-axis' in line else 1 if 'maximum' in line else -1
 if n in x.free_symbols:
  step=sp.expand(x).coeff(n)/sp.pi;offset=sp.expand(x).subs(n,0)/sp.pi
  # Exact independent complete-set criterion; also ensures claimed family has
  # ALL required points, not just correct values at its own sampled points.
  return bool((step==1 and (offset-sp.Rational(1,2)).is_integer) if target==0 else step==2 and ((offset-(0 if target==1 else 1))/2).is_integer)
 return sp.cos(x)==target

def formatting(s):
 assert s.count('$')%2==0,'Math delimiter mismatch'
 for math in re.findall(r'\$+([^$]+)\$+',s):
  depth=0
  for ch in math:
   depth+=1 if ch=='{' else -1 if ch=='}' else 0
   assert depth>=0,'Closing brace mismatch'
  assert depth==0,'Opening brace mismatch'
 assert '@@' not in s and '--' not in s and '+-' not in s

def inspect(r):
 q=r['question'];assert set(r['knowledge_point'])=={'db_id','id','title'};assert r['knowledge_point']['db_id']==g.KP_ID;uuid.UUID(q[':question/id'])
 formatting(q[':question/problem']);formatting(q[':question/worked-solution'])
 fields=q[':question/answer-fields']
 for f in fields:
  uuid.UUID(f[':answer-field/id']);values=f[':answer-field/choices'];ids=[a[':answer/id'] for a in values]
  assert len(ids)==len(set(ids));assert f[':answer-field/correct'][0]==':answer/id' and f[':answer-field/correct'][1] in ids
  assert len(values)==(2 if f[':answer-field/type'].endswith('/checkbox') else 1)
  for a in values:uuid.UUID(a[':answer/id']);assert a[':answer/type'] in (':answer.type/text',':answer.type/math');formatting(a[':answer/value'])
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 if r['generation']['claims']:
  lines=[l for l in q[':question/problem'].splitlines() if re.match(r'^(?:- |[1-3]\. |I{1,3}\. )',l)]
  assert len(lines)==3,lines
  actual=tuple(bool(printed_truth(line)) for line in lines)
  assert list(actual)==r['generation']['truth_vector'],(lines,actual,r['generation']['truth_vector'])
  for verdict in re.finditer(r'Statements? (I{1,3}(?: and I{1,3})*) (?:is|are) (true|false)',q[':question/worked-solution']):
   for label in verdict[1].split(' and '):assert actual[('I','II','III').index(label)]==(verdict[2]=='true'), 'Printed solution verdict disagrees with actual claim'
  assert len(fields)==3
  for i,f in enumerate(fields):
   assert f[':answer-field/key']==g.ROMAN[i] and f[':answer-field/type']==':answer-field.type/checkbox'
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==['false','true']
   answer=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
   assert answer==('true' if actual[i] else 'false')

 else:
  assert 'function $y=' in q[':question/problem']; assert ('sin' in q[':question/problem'])==('sin'==r['generation']['parameters']['function'])

def native(label,r):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/checkbox'):
   for a in f[':answer-field/choices']:
    checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Boolean statement truth checked independently from printed prompt'})
  else:
   value=f[':answer-field/choices'][0][':answer/value']
   for val,expected in ((value,'accepted'),('0','rejected')):checks.append({'field_index':i,'submitted':val,'expected':expected,'purpose':'Exact blank / wrong finite input'})
   equivalent={'-1':'-2/2','1':'2/2',r'2\pi':'pi+pi',r'\infty':'infinity',r'-\infty':'-infinity'}[value.strip()]
   checks.append({'field_index':i,'submitted':equivalent,'expected':'accepted','purpose':'Equivalent blank entry'})
 return {'label':label,'record':r,'checks':checks}

def fingerprint(q):
 prompt=q[':question/problem']
 if 'sin' in prompt:return g.digest({'function':'sin','facts':['domain','range','period']})
 lines=[line for line in prompt.splitlines() if re.match(r'^(?:- |[1-3]\. |I{1,3}\. )',line)]
 claims=[]
 for line in lines:
  maths=re.findall(r'\$([^$]+)\$',line)
  if 'range' in line:
   m=re.search(r'\[([^,]+),([^\]]+)\]',line)
   claims.append({'kind':'range','low':str(expr(m[1])),'high':str(expr(m[2]))})
  elif 'output' in line:claims.append({'kind':'output','value':str(expr(next(x.split('=',1)[1] for x in maths if x.startswith('y='))))})
  elif 'passes through' in line:
   x,y=next(x.strip('()').split(',') for x in maths if x.startswith('('));claims.append({'kind':'point','x':str(expr(x)/sp.pi),'y':str(expr(y))})
  elif 'axis at' in line and any(x.startswith('y=') for x in maths):claims.append({'kind':'intercept','value':str(expr(next(x.split('=',1)[1] for x in maths if x.startswith('y='))))})
  else:
   x=expr(next(x.split('=',1)[1] for x in maths if re.match(r'x\s*=',x)))
   kind='zero' if 'zero' in line or '$x$-axis' in line else 'max' if 'maximum' in line else 'min'
   if n in x.free_symbols:claims.append({'kind':kind+'_family','offset':str(sp.expand(x).subs(n,0)/sp.pi),'step':int(sp.expand(x).coeff(n)/sp.pi)})
   else:claims.append({'kind':kind,'value':str(x/sp.pi)})
 return g.digest({'function':'cos','claims':sorted([g.semantics(c) for c in claims],key=g.digest),'facts':None if claims else ('domain','range','period')})
