"""Parent's fail-closed parser for displayed elementary ODE expressions."""
import re
import sympy as s
t,u,v,x,y,z=s.symbols('t u v x y z',real=True);i,j,k=s.symbols('i j k');a,b=s.symbols('alpha beta',real=True)
locals_={'a':a,'b':b,'t':t,'u':u,'v':v,'x':x,'y':y,'z':z,'i':i,'j':j,'k':k,'e':s.E,'pi':s.pi}
functions={'arccos':s.acos,'arcsin':s.asin,'arctan':s.atan,'Abs':s.Abs,'sin':s.sin,'cos':s.cos,'tan':s.tan,'sec':s.sec,'csc':s.csc,'cot':s.cot,'ln':s.log,'log':s.log,'exp':s.exp}
def scalar(raw):
 raw=raw.replace(r'\alpha','a').replace(r'\beta','b')
 extra={}
 while ')^{′}' in raw:
  end=raw.index(')^{′}');depth=1;start=end-1
  while depth:
   if raw[start]==')':depth+=1
   elif raw[start]=='(':depth-=1
   start-=1
  start+=1;name='D'+str(len(extra));extra[name]=s.diff(scalar(raw[start+1:end]),x)
  raw=raw[:start]+name+raw[end+len(')^{′}'): ]
 lookup={**locals_,**extra}
 text=raw.strip().rstrip('.,').replace('⁡','').replace('−','-').replace('π','pi').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*')
 text=re.sub(r'\\operatorname\{(arccos|arcsin|arctan|Abs|sin|cos|tan|sec|csc|cot|ln|log)\}',r'\1',text)
 text=re.sub(r'\{(arccos|arcsin|arctan|Abs|sin|cos|tan|sec|csc|cot|ln|log|e)\}',r'\1',text).replace('\\','')
 tokens=re.findall(r'frac|sqrt|arccos|arcsin|arctan|Abs|sin|cos|tan|sec|csc|cot|ln|log|exp|pi|D\d+|[abtuvxyzijke]|\d+(?:\.\d+)?|[{}()+\-*/^]',text)
 assert re.sub(r'\s+','',text)==''.join(tokens),('Unsupported parent math',text)
 pos=0
 def peek():return tokens[pos] if pos<len(tokens) else None
 def eat(expected=None):
  nonlocal pos
  z=peek();assert z is not None and (expected is None or z==expected),(text,expected,z);pos+=1;return z
 def group():
  opener=eat();closer={'(' : ')','{':'}'}[opener];z=add();eat(closer);return z
 def atom():
  tok=peek()
  if tok in ('+','-'):eat();return atom()*(1 if tok=='+' else -1)
  if tok in ('(','{'):z=group()
  elif tok=='frac':
   eat();numerator=group() if peek() in ('{','(') else atom();denominator=group() if peek() in ('{','(') else atom();z=numerator/denominator
  elif tok=='sqrt':eat();z=s.sqrt(group() if peek() in ('{','(') else atom())
  elif tok in functions:
   eat();power=None
   if peek()=='^':eat();power=atom()
   # Bare sin 2t and ln 2t have a coefficient in their argument; grouped
   # functions consume exactly that group, leaving later products outside.
   coefficient=peek() is not None and (bool(re.fullmatch(r'\d+(?:\.\d+)?',peek())) or peek()=='pi')
   # Visible parentheses delimit a function argument; a power following them
   # applies to the function. Invisible TeX braces around t in sin{t}^3
   # instead group the argument's t^3, as in the captured source notation.
   visible_group=peek()=='(' or peek()=='{' and pos+1<len(tokens) and tokens[pos+1]=='('
   arg=group() if visible_group else atom()
   if coefficient and peek() in ('pi','e'):arg*=atom()
   if coefficient and peek() in ('t','u','v','x','y','z','{'):arg*=atom()
   z=functions[tok](arg)
   if power is not None:z=z**power
  elif tok in lookup:eat();z=lookup[tok]
  elif tok is not None and re.fullmatch(r'\d+(?:\.\d+)?',tok):eat();z=s.Rational(tok)
  else:raise ValueError(('Parent token',text,tok))
  if peek()=='^':eat();z=z**atom()
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
