"""Small fail-closed parser for this KP's exact printed algebra (no SymPy metadata)."""
import re
from functools import lru_cache
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor,rationalize
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor,rationalize)
def group(z,i):
 if z[i]!='{':raise ValueError('Expected group '+z[i:])
 depth=1;j=i+1
 while depth:
  if j>=len(z):raise ValueError('Unclosed group')
  depth+= (z[j]=='{')-(z[j]=='}');j+=1
 return z[i+1:j-1],j

@lru_cache(maxsize=4096)
def math(z):
 z=z.strip().rstrip('.,').replace('⁡','').replace('−','-')
 z=z.replace(r'\operatorname{ln}',r'\ln').replace(r'\dfrac',r'\frac').replace(r'\left','').replace(r'\right','')
 z=z.replace(r'\,','').replace(r'\:','').replace(r'\;','').replace(r'\!','').replace(r'\cdot','*')
 out='';i=0
 while i<len(z):
  if z.startswith(r'\frac',i):
   a,j=group(z,i+5);b,i=group(z,j);out+='(('+str(math(a))+')/('+str(math(b))+'))'
  elif z.startswith(r'\sqrt',i):
   j=i+5;n='2'
   if j<len(z) and z[j]=='[':k=z.index(']',j);n=z[j+1:k];j=k+1
   a,i=group(z,j);out+='(('+str(math(a))+')**(1/('+n+')))'
  elif z.startswith(r'\ln',i):
   j=i+3
   if z[j:j+1]=='{':a,i=group(z,j)
   else:
    mm=re.match(r'\d+',z[j:]);a=mm.group();i=j+len(a)
   out+='log('+str(math(a))+')'
  elif z[i]=='{':a,i=group(z,i);out+='('+str(math(a))+')'
  elif z[i]=='\\':raise ValueError('Unsupported command '+z[i:])
  else:out+=z[i];i+=1
 return parse_expr(out,local_dict={'e':s.E,'log':s.log,'sqrt':s.sqrt},transformations=TRANS)
def equal(a,b):return s.simplify(a-b)==0
