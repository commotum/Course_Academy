"""Independent fail-closed parser of actual displayed elementary ODE TeX.

No generation metadata is used. Formal derivative postfixes differentiate their
actual displayed inputs; symbols preserve the ordered trial/component stages.
"""
import re
import sympy as s
x=s.Symbol('x',real=True);A,alpha,beta,Y,YC,YP,DC,DP=s.symbols('A alpha beta Y YC YP DC DP',real=True)
LOCALS={str(z):z for z in [x,A,alpha,beta,Y,YC,YP,DC,DP]};LOCALS['e']=s.E
TOKENS=r'alpha|beta|frac|YC|YP|DC|DP|A|Y|x|e|′|\d+|[{}()+\-*/^]'
def scalar(raw):
 t=raw.strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*')
 for a,b in [('{y}_{p}^{′}','DP'),('{y}_{c}^{′}','DC'),('{y}^{′}','DY'),('y^{′}','DY'),('{y}_{p}(x)','YP'),('{y}_{c}(x)','YC'),('{y}_{p}','YP'),('{y}_{c}','YC'),('y_{c}','YC'),('y(x)','Y')]:t=t.replace(a,b)
 t=t.replace(r'\frac','frac').replace(r'\alpha','alpha').replace(r'\beta','beta').replace('{e}','e').replace('y','Y')
 tokens=re.findall(TOKENS,t);assert re.sub(r'\s+','',t)==''.join(tokens),('Unsupported math tokens',raw,t)
 pos=0
 def peek():return tokens[pos] if pos<len(tokens) else None
 def eat(expected=None):
  nonlocal pos
  v=peek();assert v is not None and (expected is None or v==expected),(raw,expected,v);pos+=1;return v
 def group():
  op=eat();z=add();eat('}' if op=='{' else ')');return z
 def atom():
  v=peek()
  if v in ('+','-'):eat();return atom()*(1 if v=='+' else -1)
  if v in ('(','{'):z=group()
  elif v=='frac':eat();a=group();b=group();z=a/b
  elif v in LOCALS:eat();z=LOCALS[v]
  elif v and v.isdigit():eat();z=s.Integer(v)
  else:raise ValueError(('Unsupported token',raw,v))
  if peek()=='^':
   eat()
   if peek()=='{' and pos+1<len(tokens) and tokens[pos+1]=='′':eat('{');eat('′');eat('}');z=s.diff(z,x)
   else:z=z**atom()
  return z
 def mul():
  z=atom()
  while peek() not in (None,'+','-',')','}'):
   if peek() in ('*','/'):op=eat();v=atom();z=z*v if op=='*' else z/v
   else:z*=atom()
  return z
 def add():
  z=mul()
  while peek() in ('+','-'):op=eat();v=mul();z=z+v if op=='+' else z-v
  return z
 z=add();assert pos==len(tokens);return z

def eq(raw):
 left,right=raw.replace('&','').split('=',1);return scalar(left),scalar(right)
def displays(text):return re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S)
def rows(raw):
 if r'\begin{aligned}' in raw:raw=raw.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');return [z.strip() for z in raw.split(r'\\')]
 return [raw]
def equal(a,b):return s.simplify(s.expand(a-b))==0
