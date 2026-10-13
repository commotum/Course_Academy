"""Independent parser for the printed source subset; not generator math."""
import re
from functools import lru_cache
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
x=sp.Symbol('x',positive=True)
@lru_cache(maxsize=None)
def expr(t):
 t=t.replace(r'\left','').replace(r'\right','').replace('⁡','').replace('\u2061','').replace('ln','log');t=t.strip().rstrip('.').replace('⁡','').replace(r'\,','').replace(r'\cdot','*')
 t=re.sub(r'\\operatorname\{(tan|sec|cos|sin|csc|cot)\}',r'\1',t)
 t=re.sub(r'\{(sec|cos|sin|tan|csc|cot)\}',r'\1',t)
 t=re.sub(r'\\(tan|sec|cos|sin|csc|cot)\b',r'\1',t).replace(r'\pi','pi')
 def group(s,i):
  assert s[i]=='{',(s,i)
  d=1;j=i+1
  while d:
   d+=(s[j]=='{')-(s[j]=='}');j+=1
  return s[i+1:j-1],j
 def conv(s):
  out='';i=0
  while i<len(s):
   if s.startswith('\\frac',i) or s.startswith('\\dfrac',i):
    i+=len('\\dfrac') if s.startswith('\\dfrac',i) else len('\\frac');a,i=group(s,i);b,i=group(s,i);out+='(('+conv(a)+')/('+conv(b)+'))'
   elif s.startswith('\\sqrt',i):
    i+=5
    if s[i]=='[':
     j=s.index(']',i);n=s[i+1:j];i=j+1;a,i=group(s,i);out+='(('+conv(a)+')**(1/('+n+')))'
    else:a,i=group(s,i);out+='sqrt('+conv(a)+')'
   elif s[i]=='{':a,i=group(s,i);out+='('+conv(a)+')'
   elif s[i]=='^':out+='**';i+=1
   else:out+=s[i];i+=1
  return out
 t=conv(t)
 # All observed trigonometric functions have one x, numeric, pi, sqrt(x),
 # or parenthesized exact argument; move optional exponents after the call.
 pattern=r'(log|tan|sec|cos|sin|csc|cot)(?:\*\*(\(\d+\)|\d+))?\s*'
 def trig(m):
  start=m.end();assert start<len(t)
  if t[start]=='(':
   d=1;j=start+1
   while d:d+=(t[j]=='(')-(t[j]==')');j+=1
   arg=t[start:j]
  elif t.startswith('sqrt(',start):
   d=1;j=start+5
   while d:d+=(t[j]=='(')-(t[j]==')');j+=1
   arg=t[start:j]
  else:
   mm=re.match(r'x|pi|\d+',t[start:]);assert mm,(t,start);arg=mm[0];j=start+len(arg)
  return m[1]+'('+arg+')'+('**'+m[2] if m[2] else ''),j
 while (m:=re.search(pattern,t)):
  # Remove the found function from later matching by temporary uppercase.
  val,j=trig(m);t=t[:m.start()]+val.replace(m[1],m[1].upper(),1)+t[j:]
 t=t.lower()
 return parse_expr(t,local_dict={'x':x,'pi':sp.pi,**{n:getattr(sp,n) for n in ('tan','sec','cos','sin','csc','cot','sqrt','log')}},transformations=standard_transformations+(implicit_multiplication_application,))
def function(q):
 t=q[':question/problem'];m=re.search(r'(?:f\(x\)|y)\s*=\s*(.*?)(?:\$|\s+when)',t);assert m,t
 return expr(m[1])
@lru_cache(maxsize=None)
def equivalent(a,b):
 delta=sp.expand((a-b).rewrite(sp.cos))
 if delta==0:return True
 # A differing regular evaluation disproves identity, before costly simplification.
 if x in delta.free_symbols:
  for z in (sp.Rational(1,3),sp.Rational(2,5)):
   sample=sp.N(delta.subs(x,z),50)
   if sample.is_real and abs(sample)>sp.Float('1e-35'):return False
 return sp.simplify(delta)==0
