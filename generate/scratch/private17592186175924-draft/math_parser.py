"""Strict displayed scalar grammar, independent of generator AST/metadata."""
import re,sympy as s
SYMS={v:s.Symbol(v,real=True) for v in 'xyzt'}
class Parser:
 def __init__(self,text):
  text=text.replace(r'\theta','t').replace(r'\dfrac',r'\frac')
  text=text.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\quad','').replace(r'\cdot','*').replace('π',r'\pi').replace('⁡','')
  text=re.sub(r'\\operatorname\{(sin|cos|tan|cot)\}',lambda m:'\\'+m[1]+' ',text)
  text=text.replace('{sin}',r'\sin').replace('{cos}',r'\cos')
  self.tokens=[];pos=0
  while pos<len(text):
   if text[pos].isspace():pos+=1;continue
   m=re.match(r'\\(?:frac|pi|sin|cos|tan|cot|sqrt|exp)\b|[0-9]+|[xyzte{}()+\-*/^]',text[pos:])
   if not m:raise ValueError('unsupported scalar at '+repr(text[pos:]))
   self.tokens.append(m[0]);pos+=len(m[0])
  self.i=0
 def peek(self):return self.tokens[self.i] if self.i<len(self.tokens) else None
 def take(self,want=None):
  v=self.peek()
  if v is None or want is not None and v!=want:raise ValueError((want,v))
  self.i+=1;return v
 def add(self):
  v=self.mul()
  while self.peek() in ['+','-']:
   op=self.take();r=self.mul();v=v+r if op=='+' else v-r
  return v
 def mul(self):
  v=self.unary()
  while True:
   p=self.peek()
   if p in ['*','/']:
    op=self.take();r=self.unary();v=v*r if op=='*' else v/r
   elif p is not None and (p.isdigit() or p in list('xyzte')+['{','(',r'\frac',r'\pi',r'\sin',r'\cos',r'\tan',r'\cot',r'\sqrt',r'\exp']):v*=self.unary()
   else:return v
 def unary(self):
  if self.peek() in ['+','-']:
   op=self.take();v=self.unary();return v if op=='+' else -v
  v=self.atom()
  if self.peek()=='^':self.take();v**=self.unary()
  return v
 def group(self):
  a=self.take();v=self.add();self.take('}' if a=='{' else ')');return v
 def atom(self):
  if self.peek() in ['{','(']:return self.group()
  a=self.take()
  if a.isdigit():return s.Integer(a)
  if a in SYMS:return SYMS[a]
  if a=='e':return s.E
  if a==r'\pi':return s.pi
  if a==r'\frac':return self.group()/self.group()
  if a==r'\sqrt':return s.sqrt(self.group())
  if a in [r'\sin',r'\cos',r'\tan',r'\cot',r'\exp']:
   power=s.S.One
   if self.peek()=='^':self.take();power=self.unary()
   arg=self.group() if self.peek() in ['{','('] else self.atom()
   if self.peek() in SYMS and arg.is_number:arg*=self.atom()
   return {r'\sin':s.sin,r'\cos':s.cos,r'\tan':s.tan,r'\cot':s.cot,r'\exp':s.exp}[a](arg)**power
  raise ValueError(a)
def parse(text):
 p=Parser(text);v=p.add()
 if p.peek() is not None:raise ValueError(('unconsumed',p.tokens[p.i:]))
 return v
