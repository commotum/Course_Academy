"""Fail-closed independent scalar TeX evaluator for audit calculations."""
import re,sys
import sympy as sp
sys.path.insert(0,'scripts')
from question_capture.math_notation import Parser,tokens
FN={'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,'sec':sp.sec,'csc':sp.csc,'cot':sp.cot,'sinh':sp.sinh,'cosh':sp.cosh,'tanh':sp.tanh,'ln':sp.log,'log':sp.log,'exp':sp.exp,'arcsin':sp.asin,'arccos':sp.acos,'arctan':sp.atan,'arcsec':sp.asec,'arccsc':sp.acsc,'arccot':sp.acot}
SYMS={c:sp.Symbol(c,real=True)for c in 'xytuvzabcdekmnPQTVWYZS'};SYMS.update({c:sp.Symbol(c,real=True)for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'if c not in SYMS});SYMS.update({'C':sp.Symbol('C',real=True),'e':sp.E,'pi':sp.pi})
class Unsupported(ValueError):pass
class Evaluate:
 def __init__(self,nodes):self.ns=list(nodes);self.i=0
 def peek(self):return self.ns[self.i]if self.i<len(self.ns)else None
 def consume(self):v=self.peek();self.i+=1;return v
 def symbol(self,n):
  if n is None:return None
  if n[0]=='char':return n[1]
  if n[0]=='command'and n[1]in ('cdot','times'):return '*'
  return None
 def sum(self):
  v=self.product()
  while self.symbol(self.peek())in ('+','-'):
   op=self.symbol(self.consume());b=self.product();v=v+b if op=='+'else v-b
  return v
 def product(self):
  v=self.factor()
  while self.peek()is not None and self.symbol(self.peek())not in ('+','-','=',';',',','|','<','>'):
   op=self.symbol(self.peek())
   if op in ('*','/'):self.consume();b=self.factor();v=v*b if op=='*'else v/b
   else:v*=self.factor()
  return v
 def function(self,fn,power=None,base=None):
  n=self.peek()
  if n is None:raise Unsupported('missing function argument')
  if self.symbol(n)=='|':
   arg=self.absolute()
  elif n[0]in ('fence','group'):
   arg=self.node(self.consume())
  elif n[0]=='script'and n[1][0]in ('fence','group')and not n[2]:
   self.consume();arg=self.node(n[1]);power=evaluate(n[3])if power is None else power*evaluate(n[3])
  else:
   numeric=n[0]=='char'and re.fullmatch(r'\d+(?:\.\d+)?',n[1]);arg=self.factor()
   if numeric and self.peek()is not None and(self.peek()[0]=='char'and self.peek()[1].isalpha()or self.peek()[0]=='script'and self.peek()[1][0]=='char'):arg*=self.factor()
  if fn=='log'and base is not None:v=sp.log(arg,base)
  else:v=FN[fn](arg)
  return v**power if power is not None else v
 def absolute(self):
  assert self.symbol(self.consume())=='|';nodes=[]
  while self.peek()is not None and self.symbol(self.peek())!='|':nodes.append(self.consume())
  if self.peek()is None:raise Unsupported('unclosed absolute value')
  self.consume();return sp.Abs(evaluate(nodes))
 def factor(self):
  n=self.peek();c=self.symbol(n)
  if c in ('+','-'):self.consume();v=self.factor();return v if c=='+'else-v
  if c=='|':return self.absolute()
  n=self.consume()
  if n is None:raise Unsupported('missing operand')
  if n[0]=='operatorname':
   name=''.join(c[1]for c in n[1]if c[0]=='char')
   if name in FN:return self.function(name)
   raise Unsupported('operatorname '+name)
  if n[0]=='styled':
   name=''.join(c[1]for c in n[2]if c[0]=='char')
   if name in FN:return self.function(name)
  if n[0]=='operator':
   if n[1]not in FN:raise Unsupported('operator '+n[1])
   return self.function(n[1])
  if n[0]=='script'and n[1][0]=='operator':
   fn=n[1][1]
   if fn not in FN:raise Unsupported('function '+fn)
   return self.function(fn,evaluate(n[3])if n[3]else None,evaluate(n[2])if n[2]else None)
  return self.node(n)
 def node(self,n):
  kind=n[0]
  if kind=='char':
   t=n[1]
   if re.fullmatch(r'\d+(?:\.\d+)?',t):return sp.Rational(t)
   if t in SYMS:return SYMS[t]
   raise Unsupported('char '+repr(t))
  if kind=='command':
   if n[1]=='pi':return sp.pi
   if n[1]=='infty':return sp.oo
   raise Unsupported('command '+n[1])
  if kind in ('group','fence'):return evaluate(n[1]if kind=='group'else n[2])
  if kind=='frac':return evaluate(n[1])/evaluate(n[2])
  if kind=='number':return sp.Rational(n[1],n[2])
  if kind=='root':return evaluate(n[2])**(1/evaluate(n[1])if n[1]else sp.Rational(1,2))
  if kind=='script':
   if n[2]:
    # Indexed integration constants remain independent constants.
    if n[1]==('char','C'):return sp.Symbol('C'+str(evaluate(n[2])),real=True)**(evaluate(n[3])if n[3]else 1)
    raise Unsupported('subscript '+repr(n))
   return self.node(n[1])**evaluate(n[3])
  if kind=='styled':
   text=''.join(c[1]for c in n[2]if c[0]=='char')
   if text in ('e','x','y','t','C'):return SYMS[text]
   raise Unsupported('styled '+text)
  raise Unsupported('node '+repr(n))
def evaluate(nodes):
 p=Evaluate(nodes);v=p.sum()
 if p.i!=len(p.ns):raise Unsupported('unconsumed '+repr(p.ns[p.i:]))
 return v
def parse(tex):
 tex=tex.strip().strip('$').strip().rstrip('.,');tex=re.sub(r'\\(?:color)\{[^{}]+\}','',tex);tex=tex.replace('−','-')
 tex=re.sub(r'\\operatorname\{(arcsec|arccsc|arcsin|arccos|arctan|sin|cos|tan|ln|log|exp)\}',lambda m:'\\'+m[1]+' ',tex)
 tex=re.sub(r'\\mathrm\{e\}', 'e',tex)
 tex=re.sub(r'(?<![A-Za-z\\])(arcsec|arccsc|arccot|arcsin|arccos|arctan)(?=[A-Za-z(])',lambda m:r'\operatorname{'+m[1]+'}',tex)
 return evaluate(Parser(tokens(tex)).sequence())
if __name__=='__main__':
 tests={r'2xe^{x^2}':2*SYMS['x']*sp.exp(SYMS['x']**2),r'\frac{1}{x^2+1}':1/(SYMS['x']**2+1),r'\ln|x|':sp.log(sp.Abs(SYMS['x'])),r'{\sin}^{2}(x)':sp.sin(SYMS['x'])**2,r'\arctan(x/2)':sp.atan(SYMS['x']/2),r'Ce^{-2t}':SYMS['C']*sp.exp(-2*SYMS['t']),r'5^{x^2}':5**SYMS['x']**2}
 for s,v in tests.items():assert sp.simplify(parse(s)-v)==0,(s,parse(s),v)
 print('parser checks',len(tests))
