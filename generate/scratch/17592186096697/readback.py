"""Private independent parser of actual printed equations, stages, and banks."""
import re
import sympy as s
t,u,v,x,y,z=s.symbols('t u v x y z',real=True);i,j,k=s.symbols('i j k');locals_={'t':t,'u':u,'v':v,'x':x,'y':y,'z':z,'i':i,'j':j,'k':k,'e':s.E,'pi':s.pi}
C,D,Q,R,Y=s.symbols('C D Q R Y',real=True)
locals_.update({'C':C,'D':D,'Q':Q,'R':R,'Y':Y})
functions={'arccos':s.acos,'arcsin':s.asin,'arctan':s.atan,'Abs':s.Abs,'sin':s.sin,'cos':s.cos,'tan':s.tan,'sec':s.sec,'csc':s.csc,'cot':s.cot,'ln':s.log,'log':s.log,'exp':s.exp}
def scalar(raw):
 text=raw.strip().rstrip('.,').replace('⁡','').replace('−','-').replace('π','pi').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*')
 text=re.sub(r'\\operatorname\{(arccos|arcsin|arctan|Abs|sin|cos|tan|sec|csc|cot|ln|log)\}',r'\1',text)
 text=re.sub(r'\{(arccos|arcsin|arctan|Abs|sin|cos|tan|sec|csc|cot|ln|log|e)\}',r'\1',text).replace('\\','')
 tokens=re.findall(r'frac|sqrt|arccos|arcsin|arctan|Abs|sin|cos|tan|sec|csc|cot|ln|log|exp|pi|[tuvxyzijkeCDQRY]|\d+(?:\.\d+)?|[{}()+\-*/^]',text)
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
  elif tok in locals_:eat();z=locals_[tok]
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
def vector(raw):
 if raw.startswith('⟨'):return s.Matrix([scalar(z) for z in raw[1:-1].replace(r'\,','').split(',')])
 if raw.startswith(r'[\begin{aligned}'):
  return s.Matrix([scalar(z) for z in raw[len(r'[\begin{aligned}'):-len(r'\end{aligned}]')].split(r'\\')])
 z=s.expand(scalar(raw));v=s.Matrix([z.coeff(b) for b in (i,j,k)]);assert s.simplify(z-sum(a*b for a,b in zip(v,(i,j,k))))==0;return v

D2=r'\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}'
D1=r'\frac{\text{d}y}{\text{d}x}'
def clean(raw):
 return raw.replace('\\\\frac',r'\frac').replace('\\\\operatorname',r'\operatorname').replace('\\\\,',r'\,').replace('\\u2061','⁡').replace(r'\left','').replace(r'\right','')
def expression(raw):
 raw=clean(raw).strip().rstrip('.,')
 raw=raw.replace(D2,'Q').replace(D1,'R')
 # Actual printed formal integration operators, not metadata stages.
 while r'\int' in raw:
  start=raw.index(r'\int'); end=re.search(r'\\text\{d\}x',raw[start:])
  assert end is not None,('Missing displayed differential',raw)
  finish=start+end.start();integrand=raw[start+4:finish].replace(r'\,','').strip()
  val=expression(integrand) if integrand else s.Integer(1)
  if val==Q:primitive=R
  elif val==R:primitive=Y
  else:primitive=s.integrate(val,x)
  # Substitute a visibly grouped canonical TeX primitive into the remaining
  # expression and recurse. C is held constant by the independent parser.
  raw=raw[:start]+'('+s.latex(primitive).replace(r'\log',r'\ln')+')'+raw[start+end.end():]
 return scalar(raw)
def forcing(problem):
 components=re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',problem,re.S)
 eq=next((a or b for a,b in components if D2 in (a or b)),None)
 assert eq is not None,('No printed second order equation',problem)
 lhs,rhs=eq.strip().rstrip('.').split('=',1)
 residual=expression(lhs)-expression(rhs)
 assert residual.has(Q) and not residual.has(R,Y,C,D)
 result=s.solve(residual,Q)
 assert len(result)==1 and not result[0].has(Q,R,Y,C,D)
 return s.simplify(result[0])
def answer(raw):
 lhs,rhs=raw.split('=',1);assert lhs.strip()=='y'
 return expression(rhs)
def solution_stages(solution):
 blocks=re.findall(r'\$\$(.*?)\$\$',solution,re.S);stages=[];phase=0
 for block in blocks:
  if r'\begin{aligned}' not in block:
   if D2 in block:
    lhs,rhs=block.strip().rstrip('.').split('=',1);stages.append(('rearrange',expression(lhs),expression(rhs),rhs))
   continue
  phase+=1
  content=block.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
  for row in content.split(r'\\'):
   lhs,rhs=row.split('=',1);lhs=lhs.replace('&','').strip();rhs=rhs.strip()
   stages.append((phase,expression(lhs) if lhs else None,expression(rhs),rhs))
 return stages
