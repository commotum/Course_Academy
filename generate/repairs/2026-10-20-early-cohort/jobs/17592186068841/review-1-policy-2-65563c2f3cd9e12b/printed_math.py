"""Small independent reader for the elementary TeX actually printed by these cases.
No generator spec, mapping, bank, family-equivalence helper or metadata is used as a math oracle.
"""
import re,json,sys
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent
X,Y,K,C,D=s.symbols('x y K C D',real=True)
class Tex:
 def __init__(self,t):
  t=t.replace('\u2061','').replace('′',"'")
  t=t.replace(r'\frac{\text{d}y}{\text{d}x}','D').replace(r'\dfrac{\textrm{d}y}{\textrm{d}x}','D')
  t=re.sub(r'\{y\}\^\{[\u2032\']\}', 'D',t).replace("y'",'D')
  t=re.sub(r'\\operatorname\{(sin|cos|arcsin|arctan|ln|sec)\}',lambda m:'\\'+m[1]+' ',t)
  t=t.replace(r'\left','').replace(r'\right','').replace(r'\,',' ').replace(r'\!',' ').replace(r'\cdot','*').replace(r'\times','*').replace(r'\,','')
  self.a=re.findall(r'\\[A-Za-z]+|\d+(?:\.\d+)?|[A-Za-z]|[^\s]',t);self.i=0
 def peek(self):return self.a[self.i] if self.i<len(self.a) else ''
 def take(self):v=self.peek();self.i+=1;return v
 def atom(self):
  a=self.take()
  if a in ['{','(','[']:
   v=self.expr();end={ '{':'}','(':')','[':']'}[a];assert self.take()==end,(a,self.a,self.i);return v
  if a==r'\frac' or a==r'\dfrac':return self.atom()/self.atom()
  if a==r'\sqrt':
   degree=2
   if self.peek()=='[': degree=self.atom()
   return self.atom()**(s.Integer(1)/degree)
  fun={r'\sin':s.sin,r'\cos':s.cos,r'\sec':s.sec,r'\arcsin':s.asin,r'\arctan':s.atan,r'\ln':s.log,r'\log':s.log,r'\exp':s.exp}
  if a in fun:
   if self.peek()=='^':
    self.take();power=self.signed();return fun[a](self.power())**power
   return fun[a](self.power())
  if a=='e':return s.E
  if a in 'xyKCD' and len(a)==1:return {'x':X,'y':Y,'K':K,'C':C,'D':D}[a]
  if re.fullmatch(r'\d+(?:\.\d+)?',a):return s.Rational(a)
  raise ValueError('Unknown token '+repr(a))
 def power(self):
  v=self.atom()
  if self.peek()=='^':self.take();v=v**self.signed()
  return v
 def signed(self):
  if self.peek() in ['+','-']:
   t=self.take();return self.signed()*(1 if t=='+' else -1)
  return self.power()
 def product(self):
  v=self.signed()
  while self.peek() and self.peek() not in ['+','-','}',')',']','=']:
   if self.peek()=='*':self.take();v*=self.signed()
   elif self.peek()=='/':self.take();v/=self.signed()
   else:v*=self.signed()
  return v
 def expr(self):
  v=self.product()
  while self.peek() in ['+','-']:
   op=self.take();v+=(1 if op=='+' else -1)*self.product()
  return v
 def all(self):
  v=self.expr();assert self.i==len(self.a),(self.a,self.i);return v

def parse(t):return Tex(t).all()
def value(t):return parse(t.split('=',1)[-1])
def rhs(prompt):
 ode=re.findall(r'\$([^$]+)\$',prompt)[0].rstrip('.,')
 l,r=ode.split('=');return s.solve(parse(l)-parse(r),D)[0]
def correct(r):
 f=r['question'][':question/answer-fields'][0];id=f[':answer-field/correct'][1];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==id)
