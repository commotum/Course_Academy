"""Independent closed grammar reader for the displayed source/generated TeX.
Unsupported tokens fail; no eval, answer metadata or generator imports.
"""
import re
import sympy as sp
X,Y,T=sp.symbols('x y t',real=True)

def normalize(s):
 s=s.replace('⁡','').replace('−','-').replace('′',"'")
 s=re.sub(r'\\operatorname\{(sin|cos|ln)\}',lambda m:'\\'+m[1],s)
 s=re.sub(r'\{(ln|sin|cos)\}',lambda m:'\\'+m[1],s)
 s=re.sub(r'\\(sin|cos|ln)\{([xyte0-9]+)\}\^\{([^{}]+)\}',lambda m:'\\'+m[1]+'('+m[2]+'^{'+m[3]+'})',s)
 s=s.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','').replace(r'\cdot','*')
 return s.strip().rstrip('.,')
class Parser:
 def __init__(self,s):
  s=normalize(s);self.ts=[];self.i=0
  while s:
   if s[0].isspace():s=s[1:];continue
   m=re.match(r'\\(?:frac|sqrt|pi|sin|cos|ln)|[0-9]+|[xyte{}()+*/^\-]',s)
   if not m:raise ValueError('Unsupported math: '+repr(s))
   self.ts.append(m[0]);s=s[len(m[0]):]
 def peek(self):return self.ts[self.i] if self.i<len(self.ts) else None
 def take(self,t=None):
  v=self.peek()
  if v is None or t is not None and v!=t:raise ValueError(('expected',t,'got',v))
  self.i+=1;return v
 def expr(self):
  v=self.product()
  while self.peek() in ('+','-'):
   op=self.take();w=self.product();v=v+w if op=='+' else v-w
  return v
 def product(self):
  v=self.unary()
  while True:
   c=self.peek()
   if c in ('*','/'):
    op=self.take();w=self.unary();v=v*w if op=='*' else v/w
   elif c is not None and (c.isdigit() or c in ('x','y','t','e','{','(',r'\pi',r'\frac',r'\sqrt',r'\sin',r'\cos',r'\ln')):v*=self.unary()
   else:return v
 def unary(self):
  if self.peek() in ('+','-'):
   op=self.take();v=self.unary();return -v if op=='-' else v
  return self.power()
 def power(self):
  v=self.atom()
  if self.peek()=='^':
   self.take();w=self.unary();v=v**w
  return v
 def group(self):
  opening=self.take();v=self.expr();self.take('}' if opening=='{' else ')');return v
 def atom(self):
  c=self.peek()
  if c in ('{','('):return self.group()
  c=self.take()
  if c.isdigit():return sp.Integer(c)
  if c in ('x','y','t'):return {'x':X,'y':Y,'t':T}[c]
  if c=='e':return sp.E
  if c==r'\pi':return sp.pi
  if c==r'\frac':return self.group()/self.group()
  if c==r'\sqrt':return sp.sqrt(self.group())
  if c in (r'\sin',r'\cos',r'\ln'):
   exponent=1
   if self.peek()=='^':self.take();exponent=self.unary()
   if self.peek() in ('{','('):
    opening=self.peek();arg=self.group()
    # An exponent following a braced generated function is a function power.
   else:
    arg=self.unary()
    while self.peek() is not None and (self.peek().isdigit() or self.peek() in ('x','y','t','e',r'\pi')):arg*=self.unary()
   return {'\\sin':sp.sin,'\\cos':sp.cos,'\\ln':sp.log}[c](arg)**exponent
  raise ValueError(('unsupported',c))
def expression(s):
 p=Parser(s);v=p.expr()
 if p.peek() is not None:raise ValueError('Unconsumed math '+repr(p.ts[p.i:]))
 return v

def equivalent(v,w):
 return sp.simplify(sp.expand_log(v-w,force=True))==0
