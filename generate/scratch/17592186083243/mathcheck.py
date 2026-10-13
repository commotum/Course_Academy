"""Independent, strict parser for rendered slope mathematics; fails closed."""
import re
import sympy as s
T=s.Symbol('t',positive=True)
FUNCTIONS={k:getattr(s,k) for k in ('sin','cos','tan','cot','sec','csc','log')}
class Parser:
 def __init__(self,text):
  text=text.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace('⁡','').replace('′',"'").replace(r'\ln',r'\log')
  text=re.sub(r'\\operatorname\{(sin|cos|tan|cot|sec|csc|ln)\}',lambda m:'\\'+('log' if m[1]=='ln' else m[1])+' ',text)
  text=re.sub(r'\{(sin|cos|tan|cot|sec|csc)\}',lambda m:'\\'+m[1]+' ',text)
  text=text.strip().rstrip('.,')
  self.tokens=[];self.i=0
  for m in re.finditer(r'\\(?:frac|sqrt|pi|sin|cos|tan|cot|sec|csc|log)\b|[0-9]+|[etxy{}()+\-*/^]|\s+|.',text):
   tok=m.group()
   if tok.isspace():continue
   if not re.fullmatch(r'\\(?:frac|sqrt|pi|sin|cos|tan|cot|sec|csc|log)\b|[0-9]+|[etxy{}()+\-*/^]',tok):raise ValueError('unsupported token '+repr(tok)+' in '+text)
   self.tokens.append(tok)
 def peek(self):return self.tokens[self.i] if self.i<len(self.tokens) else None
 def take(self,tok=None):
  r=self.peek()
  if r is None or tok is not None and r!=tok:raise ValueError(('expected',tok,'got',r,self.tokens))
  self.i+=1;return r
 def expr(self):
  a=self.product()
  while self.peek() in ('+','-'):
   op=self.take();b=self.product();a=a+b if op=='+' else a-b
  return a
 def product(self):
  a=self.unary()
  while self.peek() not in (None,'}',')','+','-'):
   if self.peek() in ('*','/'):
    op=self.take();b=self.unary();a=a*b if op=='*' else a/b
   else:a*=self.unary()
  return a
 def unary(self):
  if self.peek() in ('+','-'):
   op=self.take();v=self.unary();return v if op=='+' else -v
  a=self.atom()
  if self.peek()=='^':self.take();a**=self.unary()
  return a
 def atom(self):
  tok=self.take()
  if tok.isdigit():return s.Integer(tok)
  if tok in ('t','x','y','e',r'\pi'):return {'t':T,'x':s.Symbol('x'),'y':s.Symbol('y'),'e':s.E,r'\pi':s.pi}[tok]
  if tok in ('{','('):
   a=self.expr();self.take('}' if tok=='{' else ')');return a
  if tok==r'\frac':return self.atom()/self.atom()
  if tok==r'\sqrt':return s.sqrt(self.atom())
  if tok.startswith('\\') and tok[1:] in FUNCTIONS:
   power=1
   if self.peek()=='^':self.take();power=self.unary()
   unbraced=self.peek() not in ('{','(')
   arg=self.atom()
   if unbraced and arg.is_Number and self.peek()=='t':arg*=self.unary()
   return FUNCTIONS[tok[1:]](arg)**power
  raise ValueError(tok)
def parse(text):
 p=Parser(text.strip().rstrip('.'));result=p.expr()
 if p.peek() is not None:raise ValueError('trailing tokens')
 return result

def eq(a,b):
 z=s.trigsimp(s.simplify(a-b));return z==0

def prompt_curves(text):
 block=re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S)[0]
 x,y,domain=block.split(r',\,')
 return parse(x.split('=',1)[1]),parse(y.split('=',1)[1])

def solution_check(record):
 q=record['question'];x,y=prompt_curves(q[':question/problem']);p=record['generation']['parameters'];u=s.sympify(p['u']);dx=s.diff(x,T);dy=s.diff(y,T);expected=s.simplify(dy/dx)
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)
 assert len(blocks)==4,blocks
 # Read rendered derivative values, including every equality, before ratio and
 # evaluation. Strip aligned row wrappers, preserving derivative definitions.
 derivative=blocks[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
 derivative=derivative.replace('{x}^{′}(t)',"x'(t)").replace('{y}^{′}(t)',"y'(t)")
 derivative=derivative.replace(r'\\',',').replace(r'\,',',').rstrip('.')
 rows=[a.strip() for a in derivative.split(',') if a.strip()]
 prev=None;count=0
 for row in rows:
  parts=row.split('=');lhs=parts[0].strip()
  if lhs in ("x'(t)","y'(t)"):prev=dx if lhs.startswith('x') else dy
  elif lhs:raise AssertionError(('unknown derivative lhs',lhs))
  assert prev is not None
  for v in parts[1:]:assert eq(parse(v),prev),(v,prev);count+=1
 # Every rendered ratio and evaluated value is independently parsed. Evaluation
 # rows compare to prompt-derived derivatives at u rather than generator AST.
 for i,b in enumerate(blocks[2:]):
  b=b.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  for row in b.split(r'\\'):
   rhs=row.split('&',1)[1] if '&' in row else row
   for value in rhs.split('=')[1:]:
    value=value.strip().rstrip('.')
    assert eq(parse(value),expected if i==0 else expected.subs(T,u)),(record['generation']['template'],value,expected if i==0 else expected.subs(T,u));count+=1
 return count
