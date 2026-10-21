"""Independent narrow TeX parser for this KP's displayed expressions.

It parses rendered TeX, not generation metadata. Unsupported tokens fail closed.
"""
import re
import sympy as sp
X,Y,T,C=sp.symbols('x y t C',real=True)
FUNCS={'ln':sp.log,'log':sp.log,'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,'cot':sp.cot,'sec':sp.sec,'arctan':sp.atan,'atan':sp.atan,'exp':sp.exp}
class Parser:
 def __init__(self,s):
  s=s.replace('\u2061','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','').replace(' ','')
  s=re.sub(r'\\operatorname\{([^}]*)\}',lambda m:'\\'+m[1]+' ',s)
  s=re.sub(r'\{(ln|sec)\}',lambda m:'\\'+m[1]+' ',s)
  s=s.replace(r'\cdot','*').replace(r'\times','*')
  self.tokens=re.findall(r'\\[a-zA-Z]+|[0-9]+(?:\.[0-9]+)?|[a-zA-Z]|[^\s]',s);self.i=0
 def peek(self):return self.tokens[self.i] if self.i<len(self.tokens) else ''
 def pop(self):v=self.peek();self.i+=1;return v
 def expr(self):
  v=self.product()
  while self.peek() in ('+','-'):
   op=self.pop();w=self.product();v=v+w if op=='+' else v-w
  return v
 def product(self):
  v=self.power()
  while self.peek() and self.peek() not in ('+','-',')','}',']','=','|'):
   op=self.peek()
   if op in ('*','/'):
    self.pop();w=self.power();v=v*w if op=='*' else v/w
   else:v*=self.power()
  return v
 def power(self):
  v=self.atom()
  if self.peek()=='_':
   self.pop();suffix=self.atom()
   if not isinstance(v,sp.Symbol):raise ValueError('subscript on unsupported expression')
   v=sp.Symbol(v.name+str(suffix),real=True)
  while self.peek()=='^':
   self.pop();v=v**self.atom()
  return v
 def group(self):
  op=self.pop();close={'{':'}','(':')','[':']'}[op];v=self.expr()
  if self.pop()!=close:raise ValueError('unclosed group')
  return v
 def atom(self):
  token=self.peek()
  if token in ('+','-'):
   self.pop();v=self.power();return v if token=='+' else -v
  if token in ('{','(','['):return self.group()
  if token=='|':
   self.pop();v=self.expr()
   if self.pop()!='|':raise ValueError('absolute value')
   return sp.Abs(v)
  self.pop()
  if token==r'\frac':return self.atom()/self.atom()
  if token==r'\sqrt':
   n=self.group() if self.peek()=='[' else sp.Integer(2)
   return self.atom()**(1/n)
  if token.startswith('\\') and token[1:] in FUNCS:
   fn=FUNCS[token[1:]];power=1
   if self.peek()=='^':self.pop();power=self.atom()
   if self.peek() in ('(','{','|'):arg=self.atom()
   else:arg=self.product()
   return fn(arg)**power
  if token==r'\pi':return sp.pi
  if re.fullmatch(r'[0-9]+(?:\.[0-9]+)?',token):return sp.Rational(token)
  if token=='e':return sp.E
  if token in 'xyt' and len(token)==1:return {'x':X,'y':Y,'t':T}[token]
  if token in ('C','K','u','T'):
   suffix=''
   if self.peek()=='_':
    self.pop();v=self.atom();suffix=str(v)
   return sp.Symbol(token+suffix,real=True)
  raise ValueError('unsupported TeX token '+repr(token))
def expression(s):
 p=Parser(s.rstrip('.,'));v=p.expr()
 if p.peek():raise ValueError('unconsumed '+p.peek()+' in '+s)
 return v

def relation(s):
 sides=s.rstrip('.,').split('=')
 if len(sides)==1:return None,expression(sides[0])
 if len(sides)!=2:raise ValueError('expected one whole equation')
 return expression(sides[0]),expression(sides[1])
def equal_expr(a,b):
 d=sp.simplify(a-b)
 if d==0:return True
 if d.has(sp.sin,sp.cos,sp.tan,sp.cot):return sp.trigsimp(sp.expand_trig(d))==0
 return False

def equivalent(a,b):
 if a[0] is None or b[0] is None:return a[0] is None and b[0] is None and equal_expr(a[1],b[1])
 # Compare whole equations up to a constant scale. All KP bank RHS values are
 # free of y and LHS values depend only on y. This permits exact normalization
 # without expensive ratios of full exponential/trigonometric residuals.
 scale=sp.simplify(a[0]/b[0])
 if scale!=0 and not scale.free_symbols and scale.is_finite is True:
  return equal_expr(a[1],scale*b[1])
 return False
