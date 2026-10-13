"""Independent parser for displayed polynomial/rational TeX, without generator helpers."""
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
X,K=sp.symbols('x k',real=True)

def group(text,start):
 if text[start]!='{': raise ValueError('Expected braced mathematical group')
 depth=1;i=start+1
 while i<len(text) and depth:
  if text[i]=='{':depth+=1
  if text[i]=='}':depth-=1
  i+=1
 if depth:raise ValueError('Unclosed TeX group')
 return text[start+1:i-1],i

def parse(text):
 text=text.strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(r'\dfrac',r'\frac')
 while r'\frac' in text:
  start=text.index(r'\frac');a=start+5
  while text[a].isspace():a+=1
  num,end=group(text,a)
  while text[end].isspace():end+=1
  den,end=group(text,end)
  text=text[:start]+'(('+str(parse(num))+')/('+str(parse(den))+'))'+text[end:]
 text=text.replace('{','(').replace('}',')')
 if '\\' in text:raise ValueError('Unparsed TeX '+text)
 return parse_expr(text,local_dict={'x':X,'k':K},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))

def function(prompt):
 match=re.search(r'\$f\(x\)\s*=\s*(.*?)\$',prompt)
 if not match:raise ValueError('Missing displayed function definition')
 return parse(match.group(1))

def fingerprint(q):
 f=function(q[':question/problem'])
 # Recover the original denominator before cancellation so removable holes
 # remain part of the mathematical task/domain, while scalar rescalings do not.
 value=re.search(r'\$f\(x\)\s*=\s*(.*?)\$',q[':question/problem']).group(1)
 start=value.index(r'\frac')+5
 while value[start].isspace():start+=1
 _,end=group(value,start)
 while value[end].isspace():end+=1
 den,_=group(value,end);v=parse(den)
 poly=sp.Poly(v,X)
 domain=sp.cancel(v/poly.LC())
 import hashlib,json
 return hashlib.sha256(json.dumps([sp.srepr(sp.cancel(sp.diff(f,X))),sp.srepr(domain)],sort_keys=True,ensure_ascii=False).encode()).hexdigest()
