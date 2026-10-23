import os,sys,json,re,pathlib,hashlib,platform,collections,shutil,subprocess
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent
PKG=ROOT.parent
sys.path.insert(0,str(PKG))
import generator as g
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
X=s.Symbol('x',real=True)
def save(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2,default=str))
def latex(z):
 z=z.replace('{)}',')').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(' ', '')
 def atom(i):
  if z[i]=='{':
   depth=1;j=i+1
   while depth:
    if z[j]=='{':depth+=1
    elif z[j]=='}':depth-=1
    j+=1
   return convert(z[i+1:j-1]),j
  return z[i],i+1
 def convert(text):return latex(text)
 out='';i=0
 while i<len(z):
  if z.startswith(r'\frac',i) or z.startswith(r'\dfrac',i):
   i+=6 if z.startswith(r'\dfrac',i) else 5
   a,i=atom(i);b,i=atom(i);out+='(('+str(a)+')/('+str(b)+'))'
  elif z.startswith(r'\sqrt',i):
   a,i=atom(i+5);out+='sqrt('+str(a)+')'
  elif z[i]=='{':
   a,i=atom(i);out+='('+str(a)+')'
  elif z[i]=='^':out+='**';i+=1
  else:out+=z[i];i+=1
 return parse_expr(out,local_dict={'x':X,'sqrt':s.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))
def field(r):return r['question'][':question/answer-fields'][0]
def correct(r):
 f=field(r);key=f[':answer-field/correct'];uid=key[1] if isinstance(key,list) else key[':answer/id'];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==uid)
def expected(r):
 prompt=r['question'][':question/problem'].replace('y =','y=');f=prompt.split('$y=',1)[1].split('$')[0].rstrip(',.');y=latex(f);ans=s.diff(y,X)
 m=re.search(r'where \$x=([+-]?\d+)',prompt)
 return s.simplify(ans.subs(X,int(m[1]))) if m else ans
