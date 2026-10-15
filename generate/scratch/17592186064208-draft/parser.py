"""Private fail-closed rendered TeX reader; no generator or shared parser imports."""
import re
import sympy as s
x=s.Symbol('x',real=True);C=s.Symbol('C',real=True);K=s.Symbol('K',positive=True)
class Reader:
 def __init__(self,raw):
  z=raw.strip().rstrip('.,').replace('⁡','').replace('\u00a0','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(r'\mid','|').replace(r'\dfrac',r'\frac')
  z=re.sub(r'\\text\{\s*\}', '',z)
  z=z.replace(r'\operatorname{ln}',r'\ln').replace('\\','')
  self.t=re.findall(r'frac|ln|[xCK]|\d+|[{}()+\-*/|]',z);self.i=0;self.denominators=[]
  assert ''.join(self.t)==re.sub(r'\s+','',z),('unsupported TeX',raw,z)
 def peek(self):return self.t[self.i] if self.i<len(self.t) else None
 def eat(self,v=None):
  z=self.peek();assert z is not None and (v is None or z==v),(v,z,self.t);self.i+=1;return z
 def group(self):
  a=self.eat();b={'(':')','{':'}','|':'|'}[a];z=self.add(stop=b);self.eat(b);return s.Abs(z) if a=='|' else z
 def atom(self):
  z=self.peek()
  if z in ('+','-'):self.eat();return self.atom()*(1 if z=='+' else -1)
  if z in ('(','{','|'):return self.group()
  if z=='frac':
   self.eat();n=self.group();d=self.group();self.denominators.append(d);return n/d
  if z=='ln':self.eat();return s.log(self.atom())
  if z in ('x','C','K'):self.eat();return {'x':x,'C':C,'K':K}[z]
  if z is not None and z.isdigit():self.eat();return s.Integer(z)
  raise ValueError(('atom',z,self.t))
 def mul(self,stop=None):
  z=self.atom()
  while self.peek() not in (None,'+','-',')','}',stop):
   if self.peek() in ('*','/'):
    op=self.eat();a=self.atom();z=z*a if op=='*' else z/a
   else:z*=self.atom()
  return z
 def add(self,stop=None):
  z=self.mul(stop)
  while self.peek() in ('+','-'):op=self.eat();v=self.mul(stop);z=z+v if op=='+' else z-v
  return z
 def read(self):
  z=self.add();assert self.i==len(self.t),(self.t,self.i);return z

def scalar(z):return Reader(z).read()
def log_normal(z):
 """Exact real log identities with absolute rational factors, K>0; no forced signs."""
 def abslog(arg):
  num,den=s.fraction(s.cancel(arg));out=0
  for poly,sign in ((num,1),(den,-1)):
   coeff,factors=s.factor_list(poly,x);out+=sign*s.log(s.Abs(coeff))
   for f,n in factors:
    assert s.degree(f,x)==1,('nonlinear factor',f)
    a=f.coeff(x);b=f.subs(x,0);out+=sign*n*(s.log(s.Abs(a))+s.log(s.Abs(x+b/a)))
  return out
 replacements={}
 for node in z.atoms(s.log):
  a=node.args[0]
  if a==K:replacements[node]=node
  elif a.func==s.Abs:replacements[node]=abslog(a.args[0])
  else:
   factors=s.Mul.make_args(a);assert K in factors and len(factors)==2,(node,factors)
   other=next(v for v in factors if v!=K);assert other.func==s.Abs,node
   replacements[node]=s.log(K)+abslog(other.args[0])
 return s.expand(z.xreplace(replacements))
def derivative(z):
 """Derivative on each component of the original real pole-free domain."""
 z=log_normal(z);out=0
 for term in s.Add.make_args(z):
  if term.has(s.log):
   logs=list(term.atoms(s.log));assert len(logs)==1,term;l=logs[0];a=l.args[0]
   if not a.has(x):continue
   assert a.func==s.Abs,term;u=a.args[0];out+=(term/l)*s.diff(u,x)/u
  else:out+=s.diff(term,x)
 return s.cancel(out)
def integral_operands(z):
 z=z.replace(r'\displaystyle','').replace(r'\dfrac',r'\frac').replace(r'\left','').replace(r'\right','')
 z=z.replace(r'\textrm d x',r'\text{d}x').replace(r'\textrm{d}x',r'\text{d}x')
 pieces=re.findall(r'\\int\s*(.*?)\\,?\\text\{d\}x',z)
 if not pieces:pieces=re.findall(r'\\int\s*(.*?)dx',z)
 assert pieces,('missing integral',z)
 return [scalar(v.removesuffix('\\,')) for v in pieces]
