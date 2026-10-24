"""Retained reviewer bank-only probe and independent visible-math parser."""

import collections,json,re

from pathlib import Path

import sympy as s

from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor

x=s.Symbol("x")

def load(path): return json.loads(Path(path).read_text())

def save(path,obj): Path(path).write_text(json.dumps(obj,indent=2)+"\n")

def parse(t):
 t=t.replace('\u2061','').replace(r'\operatorname{ln}','ln').replace(r'\ln','ln')
 t=t.replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').replace(r'\,','').replace(' ', '')
 if t.startswith('y='):t=t[2:]
 def group(i):
  assert t[i]=='{', (t,i)
  depth=1;j=i+1
  while depth:
   depth+=(t[j]=='{')-(t[j]=='}');j+=1
  return t[i+1:j-1],j
 while r'\frac' in t:
  i=t.index(r'\frac'); a,j=group(i+5);b,k=group(j)
  t=t[:i]+'(('+a+')/('+b+'))'+t[k:]
 t=t.replace('{','(').replace('}',')')
 t=re.sub(r'ln(\d+)',r'ln(\1)',t)
 t=re.sub(r'(?<=[0-9x)])ln', '*ln',t)
 assert '\\' not in t,t
 return parse_expr(t,local_dict={'x':x,'ln':s.log},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))

def choices(rec):return rec['question'][':question/answer-fields'][0][':answer-field/choices']

def correct(rec):return rec['question'][':question/answer-fields'][0][':answer-field/correct'][1]

def expected(rec):
 # Read displayed function and point, not generation answer metadata.
 p=rec['question'][':question/problem']; expr=re.search(r'(?:y|f\(x\))\s*=\s*([^$]+)',p)[1].rstrip(',.')
 y=parse(expr);d=s.diff(y,x)
 if 'point where' in p:
  t=parse(re.search(r'point where \$x=([^$]+)',p)[1].rstrip('.'))
  return s.expand(d.subs(x,t)*(x-t)+y.subs(x,t)) if 'equation' in p else d.subs(x,t)
 if '{{field-1}}' in p and r'\cdot' in p.split('{{field-1}}')[1]:return s.simplify(d/(y))
 return d

def cue(rec):
 # DECLARED INPUT: complete bank ONLY. No target, key, source recipe, metadata,
 # bounds or derivative reasoning. Count slope signs; inspect repeated coefficients
 # and standalone rational constant. This is a recognizable bank-layout recipe.
 vals=[(a,parse(a[':answer/value'])) for a in choices(rec)]
 slopes=[s.expand(v).coeff(x) for a,v in vals]
 signs=[int(s.sign(v)) for v in slopes]; majority=collections.Counter(signs).most_common(1)[0][0]
 counts=collections.Counter(slopes)
 candidates=[]
 for (a,v),slope,sign in zip(vals,slopes,signs):
  rational_part=s.expand(v.subs(x,0)).as_coeff_Add()[0]
  if sign==majority and counts[slope]==2 and rational_part>0:candidates.append(a[':answer/id'])
 return candidates[0] if len(candidates)==1 else None

def probes(records):
 return {'allowed_information':'Bank-only: displayed option expressions, slope-sign counts, repeated x coefficients and sign of rational constant. No target, keys, parameters or correct-output catalog. Symbolic extraction recognizes these superficial bank roles; no differentiation or curve evaluation.',
  'total':len(records),'correct':sum(cue(r)==correct(r) for r in records),'random_baseline':0.2,
  'cases':[{'id':r['question'][':question/id'],'seed':r.get('generation',{}).get('seed'),'predicted':cue(r),'correct':correct(r),'success':cue(r)==correct(r),'point':r.get('generation',{}).get('parameters',{}).get('point')} for r in records]}
