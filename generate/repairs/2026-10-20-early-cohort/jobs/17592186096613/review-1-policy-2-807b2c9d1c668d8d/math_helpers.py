import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
x=sp.Symbol('x', positive=True)
def parse(s):
 s=s.replace(r'\frac{\text{d}}{\text{d}x}', 'D')
 s=s.replace('\\dfrac','\\frac').replace('\\operatorname{ln}','\\ln').replace('\u2061','').replace('\\,','').replace('\\cdot','*').replace('\\left','').replace('\\right','').strip().rstrip('.,')
 def grp(i):
  assert s[i]=='{',s
  start=i+1;depth=1;i+=1
  while depth:
   depth+=(s[i]=='{')-(s[i]=='}');i+=1
  return s[start:i-1],i
 while '\\frac' in s:
  i=s.rfind('\\frac'); a,j=grp(i+5);b,j=grp(j);s=s[:i]+'(('+a+')/('+b+'))'+s[j:]
 s=re.sub(r'(?:\\ln|ln)\s*x',' log(x)',s).replace('^','**').replace('{','(').replace('}',')')
 return parse_expr(s,local_dict={'x':x,'e':sp.E,'log':sp.log,'D':lambda value:sp.diff(value,x)},transformations=standard_transformations+(implicit_multiplication_application,))
def target(r): return sp.diff(parse(re.search(r'\$y\s*=\s*(.*?)\$',r['question'][':question/problem'])[1]),x)
def field(r):return r['question'][':question/answer-fields'][0]
def correct(r):
 f=field(r);return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
