"""Frozen independent parser for this bounded rational/log display grammar.

Absolute-value branches are evaluated separately on x>0 and x<0; K is positive.
No live question_capture imports. Every TeX command is consumed.
"""
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
X=sp.Symbol('x',real=True);K=sp.Symbol('K',positive=True);C=sp.Symbol('C',real=True);TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)
def group(s,i,op='{',cl='}'):
 if s[i]!=op:raise ValueError('group expected '+s[i:])
 dep=1;j=i+1
 while dep and j<len(s):dep+=(s[j]==op)-(s[j]==cl);j+=1
 if dep:raise ValueError('unclosed group')
 return s[i+1:j-1],j
def scalar(s,sign=1):
 s=s.strip().rstrip('.,').replace('\u2061','').replace(r'\operatorname{ln}',r'\ln').replace(r'\mid','|').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(r'\dfrac',r'\frac')
 s=re.sub(r'(?<![a-z\\])ln',lambda _:r'\ln',s)
 local={'x':X,'K':K,'C':C};idx=0
 while r'\ln'in s:
  i=s.index(r'\ln');j=i+3
  while s[j].isspace():j+=1
  if s[j]=='(':arg,end=group(s,j,'(',')')
  elif s[j]=='|':end=s.index('|',j+1)+1;arg=s[j:end]
  elif s[j]=='K':arg='K';end=j+1
  else:raise ValueError('unsupported log argument '+s[j:])
  name='Log'+chr(65+idx);idx+=1;local[name]=sp.log(scalar(arg,sign));s=s[:i]+'('+name+')'+s[end:]
 while '|'in s:
  i=s.index('|');j=s.index('|',i+1);arg=s[i+1:j];name='Abs'+chr(65+idx);idx+=1;a=scalar(arg,sign);local[name]=sign*X if a==X else sp.Abs(a);s=s[:i]+'('+name+')'+s[j+1:]
 while r'\frac'in s:
  i=s.index(r'\frac');a,j=group(s,i+5);b,j=group(s,j);s=s[:i]+'(('+a+')/('+b+'))'+s[j:]
 if '\\'in s:raise ValueError('unconsumed TeX '+s)
 if not s:return sp.Integer(1)
 return parse_expr(s.replace('{','(').replace('}',')'),local_dict=local,transformations=TRANS)
def prompt(s,sign=1):
 m=re.search(r'antiderivative of \$(.*?)\$',s);assert m
 return scalar(m[1].rstrip('?'),sign)
def evaluate_row(s,sign=1):
 s=s.strip().rstrip('.,');n=0;local={}
 # Replace every formal indefinite integral by its exact primitive.
 while r'\int'in s:
  i=s.index(r'\int');m=re.search(r'\\text\{d\}x',s[i+4:]);assert m,(s,i)
  end=i+4+m.end();body=s[i+4:i+4+m.start()].replace(r'\,','').strip();expr=scalar(body,sign)
  name='J'+chr(65+n);n+=1;local[sp.Symbol(name)]=sp.integrate(expr,X);s=s[:i]+'('+name+')'+s[end:]
 # Parser's implicit-multiplication transform requires explicit protected J tokens.
 for name,value in local.items():s=s.replace(str(name),'('+sp.sstr(value).replace('log(',r'\ln(').replace('**','^')+')')
 return scalar(s,sign)
def same(a,b):return sp.cancel(sp.together(a-b))==0
