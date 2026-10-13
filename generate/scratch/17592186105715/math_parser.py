"""Strict parser for frozen reciprocal/log notation; unknown tokens fail."""
import re
import sympy as sp
X=sp.Symbol('x',real=True)
C=sp.Symbol('C',real=True)
class MathParser:
 def __init__(self,text):
  text=text.replace('\\\\','\\').replace(r'\u2061','').replace('⁡','').replace(r'\operatorname{ln}',r'\ln').replace(r'\mid','|')
  text=re.sub(r'(?<![a-z\\])ln',lambda _:r'\ln',text)
  text=text.replace(r'\dfrac',r'\frac').replace(r'\left','').replace(r'\right','').replace(r'\,','')
  self.tokens=[];pos=0
  while pos<len(text):
   if text[pos].isspace():pos+=1;continue
   m=re.match(r'\\(?:frac|sqrt|ln)\b|[0-9]+|[xC{}()|+\-*/^]',text[pos:])
   if not m:raise ValueError('Unknown notation: '+repr(text[pos:]))
   self.tokens.append(m[0]);pos+=len(m[0])
  self.i=0;self.stops=[None]
 def peek(self):return self.tokens[self.i] if self.i<len(self.tokens) else None
 def take(self,expected=None):
  t=self.peek()
  if t is None or expected is not None and t!=expected:raise ValueError('Expected '+str(expected)+' got '+str(t))
  self.i+=1;return t
 def expression(self):
  r=self.product()
  while self.peek() in ('+','-'):
   op=self.take();v=self.product();r=r+v if op=='+' else r-v
  return r
 def product(self):
  r=self.unary()
  while True:
   t=self.peek()
   if t in ('*','/'):
    op=self.take();v=self.unary();r=r*v if op=='*' else r/v
   elif t and (t.isdigit() or t in ('x','C','{','(',r'\frac',r'\sqrt',r'\ln') or t=='|' and self.stops[-1]!='|'):r*=self.unary()
   else:return r
 def unary(self):
  if self.peek() in ('+','-'):
   t=self.take();r=self.unary();return r if t=='+' else -r
  r=self.atom()
  if self.peek()=='^':self.take();r**=self.unary()
  return r
 def atom(self):
  t=self.take()
  if t.isdigit():return sp.Integer(t)
  if t=='x':return X
  if t=='C':return C
  if t in ('{','(','|'):
   closing={'{':'}','(':')','|':'|'}[t];self.stops.append(closing);r=self.expression();self.take(closing);self.stops.pop();return sp.Abs(r) if t=='|' else r
  if t==r'\frac':return self.atom()/self.atom()
  if t==r'\sqrt':return sp.sqrt(self.atom())
  if t==r'\ln':return sp.log(self.atom())
  raise ValueError('Unknown atom '+str(t))
def expression(text):
 p=MathParser(text);r=p.expression()
 if p.peek() is not None:raise ValueError('Unconsumed token '+str(p.peek()))
 return r
def integral_body(text):
 text=text.strip().rstrip('.,=$').replace(r'\displaystyle','').replace(r'\int','').replace(r'\left','').replace(r'\right','')
 text=re.sub(r'\\(?:text|textrm)\{d\}\s*x',lambda _:'DX',text).replace('dx','DX')
 if 'DX' not in text:raise ValueError('Missing differential')
 if re.search(r'\\(?:d?frac)\{DX\}',text):text=text.replace('{DX}','{1}')
 else:text=text.replace('DX','')
 return expression(text)
def prompt_integrand(text):
 m=re.search(r'\$(.*?)\$',text,re.S)
 if not m:raise ValueError('No mathematical prompt')
 return integral_body(m[1])
def branches(e):
 t=sp.Symbol('t',positive=True)
 return [sp.simplify(e.subs(X,sign*t)) for sign in (1,-1)]
def derivative_residual(e,f):
 t=sp.Symbol('t',positive=True)
 return [sp.simplify(sp.diff(e.subs(X,sign*t),t)/sign-f.subs(X,sign*t)) for sign in (1,-1)]
