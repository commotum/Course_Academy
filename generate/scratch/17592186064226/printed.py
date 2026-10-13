"""Restricted parser for captured and SymPy-rendered trig TeX; no metadata used."""
import re,functools
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application,convert_xor
x=sp.Symbol('x',real=True);u=sp.Symbol('u',real=True);C=sp.Symbol('C')
def group(t,i):
 assert t[i]=='{',(t,i)
 d=1;j=i+1
 while d:
  d+=(t[j]=='{')-(t[j]=='}');j+=1
 return t[i+1:j-1],j
@functools.lru_cache(maxsize=5000)
def scalar(t):
 t=t.strip().replace('⁡','').replace(r'\u2061','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','').replace(r'\cdot','*').rstrip('.,')
 t=re.sub(r'\\operatorname\{(sin|cos|tan|cot|sec|csc)\}',r'\\\1',t)
 t=re.sub(r'\{(sin|cos|tan|cot|sec|csc)\}',r'\\\1',t)
 while (m:=re.search(r'\\(frac|dfrac|sqrt)',t)):
  a,j=group(t,m.end())
  if m[1] in ('frac','dfrac'):
   b,j=group(t,j);v='(('+str(scalar(a))+')/('+str(scalar(b))+'))'
  else:v='sqrt('+str(scalar(a))+')'
  t=t[:m.start()]+v+t[j:]
 while (m:=re.search(r'\\(sin|cos|tan|cot|sec|csc)',t)):
  j=m.end();power='1'
  if t[j:j+1]=='^':
   if t[j+1]=='{':power,j=group(t,j+1)
   else:power=t[j+1];j+=2
  while t[j:j+1]==' ':j+=1
  if t[j:j+1]=='{':arg,j=group(t,j);arg=arg.strip('()')
  elif t[j:j+1]=='(':
   end=t.index(')',j);arg=t[j+1:end];j=end+1
  else:
   z=re.match(r'\d*\s*[xu]',t[j:]);assert z,(t,j);arg=z[0];j+=len(arg)
  t=t[:m.start()]+'('+m[1]+'('+str(scalar(arg))+')**('+power+'))'+t[j:]
 t=t.replace(r'\pi','pi').replace('{','(').replace('}',')')
 assert '\\' not in t,t
 return parse_expr(t,local_dict={'x':x,'u':u,'C':C,'pi':sp.pi,'sqrt':sp.sqrt,**{f:getattr(sp,f)for f in ('sin','cos','tan','cot','sec','csc')}},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
@functools.lru_cache(maxsize=2000)
def integral(prompt):
 t=prompt.replace(r'{\int }',r'\int').replace(r'\displaystyle','')
 t=re.sub(r'\\(?:text|textrm)\s*\{?\s*d\s*\}?\s*x','dx',t)
 start=t.index(r'\int')+4;lo=hi=None
 if t[start:start+1]=='_':
  a,start=group(t,start+1)if t[start+1]=='{'else(t[start+1],start+2);assert t[start]=='^';b,start=group(t,start+1)if t[start+1]=='{'else(t[start+1],start+2);lo=scalar(a);hi=scalar(b)
 stop=t.index('dx',start)
 return scalar(t[start:stop]),lo,hi

@functools.lru_cache(maxsize=20000)
def same(a,b):
 d=a-b
 if d==0:return True
 # Reduce rational trig functions exactly. Work at their actual arguments;
 # source profiles and transports never need guessed numerical equality.
 replacements={}
 for z in d.atoms(sp.tan,sp.cot,sp.sec,sp.csc):
  t=z.args[0];replacements[z]={sp.tan:sp.sin(t)/sp.cos(t),sp.cot:sp.cos(t)/sp.sin(t),sp.sec:1/sp.cos(t),sp.csc:1/sp.sin(t)}[z.func]
 d=sp.cancel(d.xreplace(replacements))
 if d==0:return True
 args=sorted({z.args[0]for z in d.atoms(sp.sin,sp.cos)},key=str)
 if len(args)==1:
  si,co=sp.symbols('_s _c');num=sp.together(d).as_numer_denom()[0].subs({sp.sin(args[0]):si,sp.cos(args[0]):co})
  try:return sp.rem(num,co**2+si**2-1,co)==0
  except sp.PolynomialError:pass
 return sp.trigsimp(d)==0

