"""Independent strict reader for the printed elementary-expression grammar."""
import re
import sympy as s
x,y,S,T=s.symbols('x y s t',real=True)
class Reader:
 def __init__(self,text):
  text=text.replace('\u2061','').replace(r'\operatorname{sin}','SIN').replace(r'\operatorname{cos}','COS').replace(r'\operatorname{ln}','LN')
  text=text.replace('{sin}','SIN').replace('{cos}','COS').replace(r'\sin','SIN').replace(r'\cos','COS').replace(r'\ln','LN').replace(r'\log','LN')
  for t in (r'\left',r'\right',r'\,',r'\!',r'\quad',r'\;',r'\bigl',r'\bigr'):text=text.replace(t,'')
  text=text.replace(r'\cdot','*').replace(r'\times','*')
  self.ts=[];p=0
  while p<len(text):
   if text[p].isspace():p+=1;continue
   m=re.match(r'\\(?:frac|sqrt)\b|SIN|COS|LN|[0-9]+|[xystedABCDEFG{}()\[\]+*/^\-]',text[p:])
   if not m:raise ValueError(('Unsupported printed token',text[p:],text))
   self.ts.append(m[0]);p+=len(m[0])
  self.i=0
 def peek(self):return self.ts[self.i] if self.i<len(self.ts) else None
 def take(self,w=None):
  t=self.peek()
  if t is None or w is not None and t!=w:raise ValueError((w,t,self.ts))
  self.i+=1;return t
 def expr(self):
  v=self.prod()
  while self.peek() in ('+','-'):
   t=self.take();b=self.prod();v=v+b if t=='+' else v-b
  return v
 def prod(self):
  v=self.unary()
  while True:
   t=self.peek()
   if t in ('*','/'):
    self.take();b=self.unary();v=v*b if t=='*' else v/b
   elif t and (t.isdigit() or t in ('x','y','s','t','e','A','B','C','D','E','F','G','{','(','[',r'\frac',r'\sqrt','SIN','COS','LN')):v*=self.unary()
   else:return v
 def unary(self):
  if self.peek() in ('+','-'):
   t=self.take();b=self.unary();return b if t=='+' else -b
  b=self.atom()
  if self.peek()=='^':self.take();b=b**self.unary()
  return b
 def group(self):
  t=self.take();end={'{':'}','(':')','[':']'}[t];v=self.expr();self.take(end);return v
 def function_argument(self):
  numeric=self.peek().isdigit()
  v=self.unary()
  if numeric and self.peek() in ('s','t','x','y','(','{'):v*=self.unary()
  while self.peek() in ('s','t','x','y'):
   v*=self.unary()
  return v
 def atom(self):
  t=self.peek()
  if t in ('{','(','['):return self.group()
  t=self.take()
  if t.isdigit():return s.Integer(t)
  if t in ('x','y','s','t'):return {'x':x,'y':y,'s':S,'t':T}[t]
  if t=='e':return s.E
  if t in ('A','B','C','D','E','F','G'):return s.Symbol(t)
  if t==r'\frac':return self.group()/self.group()
  if t==r'\sqrt':return s.sqrt(self.group())
  if t in ('SIN','COS','LN'):
   exponent=s.Integer(1)
   if self.peek()=='^':self.take();exponent=self.group() if self.peek()=='{' else s.Integer(self.take())
   arg=self.group() if self.peek() in ('(','{') else self.function_argument()
   return {'SIN':s.sin,'COS':s.cos,'LN':s.log}[t](arg)**exponent
  raise ValueError(t)
def read(text):
 r=Reader(text);v=r.expr()
 if r.peek() is not None:raise ValueError(('Unconsumed tokens',r.ts[r.i:]))
 return v
