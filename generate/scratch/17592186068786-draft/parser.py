"""Private, deliberately bounded TeX readback for the displayed fractional family."""
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
SYMBOLS={c:sp.Symbol(c,real=True) for c in ('x','y','s','u')}
# The square-root substitution is positive on the declared real connected interval.
SYMBOLS['u']=sp.Symbol('u',positive=True)
def group(s,i):
 if i>=len(s) or s[i]!='{':raise ValueError('braced TeX operand required')
 depth=1;j=i+1
 while depth and j<len(s):
  if s[j]=='{':depth+=1
  if s[j]=='}':depth-=1
  j+=1
 if depth:raise ValueError('unbalanced operand')
 return s[i+1:j-1],j

def scalar(text):
 def convert(s):
  out='';i=0
  while i<len(s):
   if s.startswith(r'\frac',i) or s.startswith(r'\dfrac',i):
    i+=6 if s.startswith(r'\dfrac',i) else 5;a,i=group(s,i);b,i=group(s,i);out+='(('+convert(a)+')/('+convert(b)+'))'
   elif s.startswith(r'\sqrt',i):
    a,i=group(s,i+5);out+='sqrt('+convert(a)+')'
   elif s[i]=='{':
    a,i=group(s,i);out+='('+convert(a)+')'
   else:out+=s[i];i+=1
  return out
 text=text.strip().replace('+C','').replace(r'\,','').replace(r'\cdot','*').replace(r'\displaystyle','')
 text=convert(text)
 if re.search(r'[^0-9xysu\s+*/^().qrt-]',text):raise ValueError('unrecognized math '+repr(text))
 return parse_expr(text,local_dict=dict(SYMBOLS,sqrt=sp.sqrt),transformations=standard_transformations+(convert_xor,implicit_multiplication_application))

def integral(text):
 """Read exactly one formal integral, preserving its variable and integrand."""
 text=text.strip();start=text.index(r'\int');prefix=text[:start].strip()
 suffix=text[start+4:];m=re.search(r'\\text\{d\}([xysu])',suffix)
 if not m:raise ValueError('missing formal differential')
 if suffix[m.end():].strip():raise ValueError('unexpected formal suffix')
 coeff=scalar(prefix) if prefix not in ('','-') else (-1 if prefix=='-' else 1)
 return coeff,scalar(suffix[:m.start()]),SYMBOLS[m[1]]

def prompt(text):
 start=text.index(r'\int');m=re.search(r'\\text\{d\}([xysu])',text[start:])
 if not m:raise ValueError('missing prompt differential')
 return integral(text[start:start+m.end()])

def rows(solution):
 body=solution.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0]
 out=[]
 for i,row in enumerate(body.split(r'\\')):
  parts=row.split('& =')
  if i==0:out.extend([s.strip()for s in parts])
  else:
   if len(parts)!=2 or parts[0].strip():raise ValueError('unexpected aligned row')
   out.append(parts[1].strip())
 return out
