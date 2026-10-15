"""Frozen bounded TeX reader for independent rendered-content validation."""
import re
import sympy as sp
X=sp.Symbol("x",real=True);C=sp.Symbol("C",real=True)
def expression(text, extra=None):
 """Private TeX reader, separate from rendering; supports exactly the bounded grammar."""
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 text=text.strip().rstrip('.,').replace('\u2061','').replace(r'\operatorname{ln}',r'\ln')
 text=re.sub(r'(?<![A-Za-z\\])ln',lambda _:r'\ln',text)
 for a,b in [(r'\displaystyle',''),(r'\left',''),(r'\right',''),(r'\cdot','*'),(r'\,',''),(r'\!',''),(r'\mid','|'),(r'\log',r'\ln')]:text=text.replace(a,b)
 def group(s,pos):
  if pos>=len(s) or s[pos]!='{':raise ValueError('Expected TeX group: '+s[pos:])
  depth=1;i=pos+1
  while depth and i<len(s):
   if s[i]=='{':depth+=1
   elif s[i]=='}':depth-=1
   i+=1
  if depth:raise ValueError('Unbalanced TeX')
  return s[pos+1:i-1],i
 def fractions(s):
  while (m:=re.search(r'\\d?frac',s)):
   a,i=group(s,m.end());b,j=group(s,i);s=s[:m.start()]+'(('+fractions(a)+')/('+fractions(b)+'))'+s[j:]
  return s
 text=fractions(text)
 text=re.sub(r'\\ln\s*\|\s*x\s*\|',lambda _:'log(Abs(x))',text)
 # Authored formatter uses logarithms only of positive rational bases or |x|.
 text=re.sub(r'\\ln\s*\{([^{}]*)\}',lambda m:'log('+m[1]+')',text)
 text=re.sub(r'\\ln\s*\(\s*([^()]*)\s*\)',lambda m:'log('+m[1]+')',text)
 text=re.sub(r'\\ln\s*(\d+|x)',lambda m:'log('+m[1]+')',text)
 text=text.replace('{','(').replace('}',')').replace('^','**')
 if '\\' in text or '|' in text:raise ValueError('Unsupported TeX '+text)
 env={'x':X,'C':C,'e':sp.E,'log':sp.log,'Abs':sp.Abs,'f':sp.Function('f'),'g':sp.Function('g')};env.update(extra or {})
 return parse_expr(text,local_dict=env,transformations=standard_transformations+(implicit_multiplication_application,))
