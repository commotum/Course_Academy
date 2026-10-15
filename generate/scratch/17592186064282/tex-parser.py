"""Private scalar readback; fraction shorthand accepts single TeX tokens only."""
import re
import sympy as s
t,u,v,x,y,z=s.symbols('t u v x y z',real=True);i,j,k=s.symbols('i j k');locals_={'t':t,'u':u,'v':v,'x':x,'y':y,'z':z,'i':i,'j':j,'k':k,'e':s.E,'pi':s.pi}
functions={'arccos':s.acos,'arcsin':s.asin,'arctan':s.atan,'Abs':s.Abs,'sin':s.sin,'cos':s.cos,'tan':s.tan,'sec':s.sec,'csc':s.csc,'cot':s.cot,'ln':s.log,'log':s.log,'exp':s.exp}
def validate_fraction_shorthand(raw):
 """Reject a multi-digit unbraced fraction component before math readback.

 TeX consumes one character/control sequence per unbraced argument. Numeric
 lexical tokens such as 13 cannot stand for a complete fraction argument.
 """
 for match in re.finditer(r'\\(?:d?frac)(?![A-Za-z])',raw):
  pos=match.end()
  for _ in range(2):
   while pos<len(raw) and raw[pos].isspace():pos+=1
   if pos>=len(raw):raise ValueError('Missing TeX fraction argument')
   if raw[pos]=='{':
    depth=1;pos+=1
    while pos<len(raw) and depth:
     depth+=(raw[pos]=='{')-(raw[pos]=='}');pos+=1
    if depth:raise ValueError('Unclosed TeX fraction argument')
   elif raw[pos].isdigit():
    end=pos+1
    while end<len(raw) and raw[end].isdigit():end+=1
    if end-pos>1:raise ValueError('Multi-digit TeX fraction argument requires braces')
    pos=end
   elif raw[pos]=='\\':
    command=re.match(r'\\(?:[A-Za-z]+|.)',raw[pos:])
    if not command:raise ValueError('Missing TeX control-sequence argument')
    pos+=command.end()
   elif raw[pos].isalpha():pos+=1
   else:raise ValueError('TeX fraction argument requires explicit braces')

def scalar(raw):
 validate_fraction_shorthand(raw)
 text=raw.strip().rstrip('.,').replace('⁡','').replace('−','-').replace('π','pi').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*')
 text=re.sub(r'\\operatorname\{(arccos|arcsin|arctan|Abs|sin|cos|tan|sec|csc|cot|ln|log)\}',r'\1',text)
 text=re.sub(r'\{(arccos|arcsin|arctan|Abs|sin|cos|tan|sec|csc|cot|ln|log|e)\}',r'\1',text).replace('\\','')
 tokens=re.findall(r'frac|sqrt|arccos|arcsin|arctan|Abs|sin|cos|tan|sec|csc|cot|ln|log|exp|pi|[tuvxyzijke]|\d+(?:\.\d+)?|[{}()+\-*/^]',text)
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
   eat()
   def argument():
    if peek()=='{':return group()
    token=peek()
    # A multi-digit lexical token is several TeX argument tokens. Never read
    # an unbraced 13 as a complete numerator/denominator or grouped argument.
    if token in locals_ and len(token)==1:eat();return locals_[token]
    if token is not None and re.fullmatch(r'\d',token):eat();return s.Integer(token)
    raise ValueError(('Fraction argument requires explicit braces',text,token))
   numerator=argument();denominator=argument();z=numerator/denominator
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
