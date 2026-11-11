import re
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
X=s.Symbol('x',real=True)
def parse(tex):
 tex=tex.replace('\\\\','\\').replace('\\dfrac','\\frac').replace('\\tfrac','\\frac')
 for word in ['\\left','\\right','\\,','\\!','\\;','\\quad','\\qquad']:tex=tex.replace(word,'')
 tex=tex.replace('\\cdot','*').replace('\\pi','pi')
 def group(i):
  if tex[i]=='{':
   depth=1;j=i+1
   while depth:
    depth+=(tex[j]=='{')-(tex[j]=='}');j+=1
   return convert(tex[i+1:j-1]),j
  return tex[i],i+1
 def convert(text):return parse_text(text)
 def parse_text(text):
  nonlocal tex
  outer=tex;tex=text;out='';i=0
  while i<len(tex):
   if tex.startswith('\\frac',i):
    a,j=group(i+5);b,i=group(j);out+='(('+a+')/('+b+'))'
   elif tex.startswith('\\sqrt',i):
    j=i+5;n='2'
    if tex[j]=='[':end=tex.index(']',j);n=tex[j+1:end];j=end+1
    a,i=group(j);out+='(('+a+')^(1/('+n+')))'
   elif tex[i]=='{':a,i=group(i);out+='('+a+')'
   else:out+=tex[i];i+=1
  tex=outer;return out
 output=parse_text(tex).rstrip('., ')
 return parse_expr(output,local_dict={'x':X,'pi':s.pi,'e':s.E},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
def key_value(f):
 v=f.get(':answer-field/correct');cid=v.get(':answer/id') if isinstance(v,dict) else v[1] if isinstance(v,list) else v
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==cid)
def tuple_tex(value):
 value=value.replace('\\left','').replace('\\right','').strip().rstrip('.:').strip('()')
 return [parse(v) for v in value.split(',')]
def extract(q):
 text=q[':question/problem'];curve=re.search(r'\$(?:y|f\(x\))\s*=([^$]+)\$',text)
 if not curve:curve=re.search(r'\$\$\s*y=([^$]+)\$\$',text)
 f=parse(curve[1].split(r'\qquad')[0].strip().rstrip(','))
 point=re.search(r'(?:at (?:the )?point|at)\s+\$([^$]+)\$',text)
 if point:
  x,y=tuple_tex(point[1]);assert s.simplify(f.subs(X,x)-y)==0,('point off curve',f,x,y)
 else:
  xp=re.search(r'coordinate \$([^$]+)\$',text);x=parse(xp[1]);y=f.subs(X,x)
 m=s.simplify(s.diff(f,X).subs(X,x));assert m!=0 and m.is_real is True
 n=-1/m;b=s.simplify(y-n*x)
 return f,x,y,m,n,b
