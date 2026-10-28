"""Small strict independent parser for the exact scalar families in this audit.

Unsupported notation raises. Odd-root branch limits are reported by callers;
this parser's default symbols are positive for logarithm/radical simplification.
"""
import re
import sympy as S
FUNCTIONS={'sin':S.sin,'cos':S.cos,'tan':S.tan,'cot':S.cot,'sec':S.sec,'csc':S.csc,'ln':S.log,'log':lambda x:S.log(x,10),'exp':S.exp,'sinh':S.sinh,'cosh':S.cosh,'tanh':S.tanh,'arctan':S.atan,'arcsin':S.asin,'arccos':S.acos,'abs':S.Abs}
class Parser:
 def __init__(self,text,positive=True):
  value=str(text).strip().replace('−','-');value=re.sub(r'\\(?:text|textrm)\{\s*\}', ' ',value)
  funcs='arcsin|arccos|arctan|sinh|cosh|tanh|sin|cos|tan|sec|csc|cot|ln|log|exp'
  value=re.sub(r'(?<![A-Za-z{])\{('+funcs+r')\}((?:\^\{[^{}]*\})?)⁡?',lambda m:'\\'+m[1]+m[2]+' ',value)
  value=re.sub(r'('+funcs+r')⁡',lambda m:'\\'+m[1]+' ',value)
  value=re.sub(r'(?<![A-Za-z\\])('+funcs+r')(?=⁡|\(|[xyzt])',lambda m:'\\'+m[1]+' ',value)
  value=re.sub(r'\\[,;!]|\\(?:quad|qquad|bigl|bigr|Bigl|Bigr)\b',' ',value)
  self.text=value.replace('⁡','').replace('θ',r'\theta ').replace('π',r'\pi ').replace('α',r'\alpha ').replace('β',r'\beta ');self.i=0;self.positive=positive
 def skip(self):
  while self.i<len(self.text)and self.text[self.i].isspace():self.i+=1
 def peek(self):self.skip();return self.text[self.i:self.i+1]
 def take(self,s):
  self.skip()
  if self.text.startswith(s,self.i):self.i+=len(s);return True
  return False
 def group(self):
  c=self.peek()
  if c not in '{([':return self.atom()
  self.i+=1;close={'{':'}','(':')','[':']'}[c];out=self.expr();assert self.take(close),('unclosed',self.text,self.i,close);return out
 def texarg(self):
  c=self.peek()
  if c in'{([':return self.group()
  if c.isdigit():self.i+=1;return S.Integer(c)
  return self.atom()
 def symbol(self,name):return S.Symbol(name,positive=True)if self.positive else S.Symbol(name,real=True)
 def argument(self):
  if self.peek()in'{([':return self.group()
  start=self.i;a=self.atom()
  # TeX's common unparenthesized numeric function argument, such as sin2x.
  if a.is_number and self.peek().isalpha():a*=self.atom()
  return a
 def atom(self):
  self.skip();c=self.peek()
  if not c:raise ValueError('Missing atom')
  if self.take('+'):return self.atom()
  if self.take('-'):return-self.atom()
  if c in'{([':a=self.group()
  elif c=='|':self.i+=1;a=S.Abs(self.expr());assert self.take('|')
  elif c=='\\':
   self.i+=1;m=re.match(r'[A-Za-z]+|.',self.text[self.i:]);assert m;cmd=m[0];self.i+=len(cmd)
   if cmd in['left','right','displaystyle','textstyle','big','Big','bigg','Bigg',',',';','!','quad','qquad',' ']:return self.atom()
   if cmd in['frac','dfrac','tfrac']:
    n=self.texarg();d=self.texarg();a=n/d
   elif cmd=='sqrt':
    root=self.group()if self.peek()=='['else S.Integer(2);a=self.group()**(1/root)
   elif cmd in['mathbf','mathrm','mathit','mathbb','textrm','text']:a=self.group()
   elif cmd=='color':
    self.skip();assert self.peek()=='{';end=self.text.index('}',self.i);self.i=end+1;return self.atom()
   elif cmd=='pi':a=S.pi
   elif cmd=='infty':a=S.oo
   elif cmd in['theta','alpha','beta','lambda','mu','tau']:a=self.symbol(cmd)
   elif cmd=='operatorname':
    self.skip();assert self.peek()=='{';end=self.text.index('}',self.i);name=self.text[self.i+1:end];self.i=end+1;a=self.function(name)
   elif cmd in FUNCTIONS:a=self.function(cmd)
   else:raise ValueError('Unsupported command '+cmd)
  elif c.isdigit()or c=='.':
   m=re.match(r'(?:\d+(?:\.\d*)?|\.\d+)',self.text[self.i:]);assert m;self.i+=len(m[0]);a=S.Rational(m[0])
  elif c.isalpha():
   self.i+=1;a=S.E if c=='e'else S.Function(c)(self.group())if c in'fghuv'and self.peek()=='('else self.symbol(c)
  else:raise ValueError(('Unsupported atom',self.text,self.i))
  if self.take('_'):
   sub=self.group();a=self.symbol(str(a)+str(sub))
  if self.take('^'):a=a**self.texarg()
  return a
 def function(self,name):
  if name not in FUNCTIONS:raise ValueError('Unsupported function '+name)
  base=None;power=None
  if self.take('_'):base=self.texarg()
  if self.take('^'):power=self.texarg()
  arg=self.argument();a=S.log(arg,base)if base is not None else FUNCTIONS[name](arg)
  if power is not None:
   if power==-1 and name in ['sin','cos','tan']:raise ValueError('Ambiguous inverse trigonometric notation')
   a=a**power
  return a
 def product(self):
  a=self.atom()
  while True:
   c=self.peek()
   if not c or c in'+-=,;?)}]|':break
   if self.take('*')or self.take(r'\cdot')or self.take(r'\times'):a*=self.atom()
   elif self.take('/'):a/=self.atom()
   else:a*=self.atom()
  return a
 def expr(self):
  a=self.product()
  while True:
   if self.take('+'):a+=self.product()
   elif self.take('-'):a-=self.product()
   else:break
  return a
 def parse(self):
  a=self.expr();self.skip()
  if self.i!=len(self.text):raise ValueError(('Unconsumed notation',self.text[self.i:]))
  return a

def parse(s,positive=True):
 s=str(s).strip().rstrip('.,');s=re.sub(r'\\(?:left|right)(?=[()|\[\]])','',s)
 return Parser(s,positive).parse()
def integral_detail(s):
 s=s.strip().strip('$').strip().rstrip('.,?=\\ ');s=re.sub(r'^\\displaystyle\s*','',s)
 s=re.sub(r'^\{\\int\s*\}',lambda m:r'\int',s)
 if s.startswith('{')and s.endswith('}')and s[1:].lstrip().startswith(r'\int'):s=s[1:-1].strip()
 assert s.startswith(r'\int'),s;s=s[4:].strip();bounds=None
 if s.startswith('_'):
  p=Parser(s[1:]);low=p.texarg();assert p.take('^');high=p.texarg();s=p.text[p.i:];bounds=(low,high)
 s=re.sub(r'\\(?:,|;|!|quad|qquad)',' ',s);s=re.sub(r'\\(?:textrm|mathrm|text)\s+d',lambda m:r'\mathrm{d}',s)
 m=re.search(r'(?:\\(?:mathrm|text|textrm)\{d\}|d)\s*(\\theta|[xyztθ])\s*[.,?=]*\s*$',s)
 if not m:raise ValueError(('Missing integral differential',s))
 var='theta'if m[1]in[r'\theta','θ']else m[1];body=s[:m.start()].strip();return parse(body),S.Symbol(var,positive=True),bounds

def integral(s):
 f,x,bounds=integral_detail(s)
 if bounds:raise ValueError('Definite integral requires endpoint evaluation')
 return f,x
