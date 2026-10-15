"""Independent bounded parser for displayed rational functions and log primitives.

log|u| is represented by log(u) for interval-wise derivative equivalence; this
never asserts a complex logarithm as a learner answer. All commands are consumed.
"""
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
X=sp.Symbol('x',real=True);T=sp.Symbol('t',real=True);TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)
def group(s,i,opening='{',closing='}'):
 if s[i]!=opening:raise ValueError('expected group '+s[i:])
 depth=1;j=i+1
 while depth:
  depth+=(s[j]==opening)-(s[j]==closing);j+=1
 return s[i+1:j-1],j
def scalar(s):
 s=s.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace('\u2061','').replace(r'\operatorname{ln}',r'\ln').replace(r'\mid','|').strip().rstrip('.,')
 local={'x':X,'t':T,'C':sp.Symbol('C'),'K':sp.Symbol('K'),'u':sp.Symbol('u',real=True)};i=0
 while r'\ln'in s:
  start=s.index(r'\ln');j=start+3
  while s[j].isspace():j+=1
  if s[j]=='|':end=s.index('|',j+1);arg=s[j+1:end];end+=1
  elif s[j]=='(':arg,end=group(s,j,'(',')')
  else:raise ValueError('log argument not delimited')
  token='Log'+chr(65+i);i+=1;local[token]=sp.log(scalar(arg));s=s[:start]+'('+token+')'+s[end:]
 while r'\frac'in s:
  start=s.index(r'\frac');a,j=group(s,start+5);b,j=group(s,j);s=s[:start]+'(('+a+')/('+b+'))'+s[j:]
 if '\\'in s:raise ValueError('unparsed TeX '+s)
 s=s.replace('{','(').replace('}',')')
 return parse_expr(s,local_dict=local,transformations=TRANS)
def prompt(text):
 text=text.replace(r'\dfrac',r'\frac').replace(r'\displaystyle','').replace(r'\textrm d x',r'\text{d}x')
 m=re.search(r'\\int\s*(.*?)\\(?:text|textrm)\{d\}([xt])',text)
 if m:return scalar(m[1])
 m=re.search(r'\\int\s*(.*?)d([xt])',text)
 if m:return scalar(m[1])
 m=re.search(r'integral of \$(.*?)\$ with respect',text)
 if m:return scalar(m[1])
 raise ValueError('integrand not found '+text)
def same(a,b):return sp.simplify(a-b)==0
def equivalent(a,b,z=X):return same(sp.diff(a,z),sp.diff(b,z))
