"""Restricted, independent parser for the captured trig-chain TeX grammar.

Rejects unsupported syntax and trailing tokens. No eval or generator metadata.
"""
import re
import sympy as s
x=s.Symbol('x',real=True)
FUN={'sin':s.sin,'cos':s.cos,'cot':s.cot,'csc':s.csc,'sec':s.sec,'tan':s.tan,'ln':s.log,'sqrt':s.sqrt}
def scalar(text):
 text=text.replace('\u2061','').replace(r'\,','').replace(r'\cdot','*')
 text=re.sub(r'\\operatorname\{(sin|cos|cot|csc|sec|tan|ln)\}',r'\\\1',text)
 text=re.sub(r'\{(sin|cos|cot|csc|sec|tan)\}',r'\\\1',text)
 text=text.replace(r'\left','').replace(r'\right','').replace('[','(').replace(']',')').strip().rstrip('.')
 # Require every nonwhitespace character to have a token.
 parts=re.findall(r'\\(?:sin|cos|cot|csc|sec|tan|ln|sqrt|frac)|[0-9]+|[a-z]|[+*/^(){}-]',text)
 if ''.join(parts)!=re.sub(r'\s+','',text):raise ValueError('Unsupported syntax: '+text)
 i=0
 def peek():return parts[i] if i<len(parts) else None
 def take():
  nonlocal i
  t=peek();i+=1;return t
 def group():
  start=take();end=')' if start=='(' else '}'
  val=expr()
  if take()!=end:raise ValueError('Unclosed group')
  return val
 def exponent():
  take()
  return group() if peek() in ('{','(') else atom()
 def atom():
  t=peek()
  if t in ('{','('):v=group()
  elif t=='-':take();v=-atom()
  elif t=='+':take();v=atom()
  elif t==r'\frac':
   take();n=group();d=group();v=n/d
  elif t and t.startswith('\\'):
   take();fun=FUN[t[1:]];power=exponent() if peek()=='^' else None
   if peek() in ('{','('):arg=group()
   else:
    # Unparenthesized captured trig arguments are one numeric monomial.
    arg=atom()
    while peek() and (peek().isdigit() or peek()=='x'):arg*=atom()
   v=fun(arg)
   if power is not None:v=v**power
  elif t and t.isdigit():take();v=s.Integer(t)
  elif t and t.isalpha():take();v=x if t=='x' else s.Symbol(t,real=True)
  else:raise ValueError('Missing atom at '+str(t))
  if peek()=='^':v=v**exponent()
  return v
 def product():
  v=atom()
  while peek() and peek() not in ('+','-',')','}'):
   t=peek()
   if t in ('*','/'):take();w=atom();v=v*w if t=='*' else v/w
   else:v*=atom()
  return v
 def expr():
  v=product()
  while peek() in ('+','-'):
   t=take();w=product();v=v+w if t=='+' else v-w
  return v
 v=expr()
 if i!=len(parts):raise ValueError('Trailing syntax')
 return v

def given(prompt):
 m=re.search(r'\$[fhy]\(x\)\s*=([^$]+)\$',prompt)
 if not m:m=re.search(r'\$[fhy]\s*=([^$]+)\$',prompt)
 if not m:raise ValueError('No function in prompt')
 f=scalar(m[1]);p=re.search(r"\$\{[fhy]\}\^\{(?:′|')\}\((-?\d+)\)",prompt)
 return f,int(p[1]) if p else None

def equal(a,b):
 if a==b:return True
 d=s.expand(a-b)
 if d==0:return True
 # A stable nonzero witness distinguishes bank objects without asking a
 # symbolic simplifier to expand unrelated high-frequency trig functions.
 # Correctness equalities must still reduce exactly to zero below.
 for point in (s.Rational(1,7),s.Rational(2,7)):
  n=s.N(d.subs(x,point),80)
  if n.is_number and abs(complex(n))>1e-25:
   finer=s.N(d.subs(x,point),120)
   assert abs(complex(finer)-complex(n))<1e-20
   return False
 return s.trigsimp(s.simplify(d))==0

def solution_final(solution):
 # Last equality inside final aligned environment.
 aligned=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)
 if not aligned:raise ValueError('No worked solution aligned environment')
 last=aligned[-1].split('& =')[-1] if '& =' in aligned[-1] else aligned[-1].split('&=')[-1]
 return scalar(last.strip())

def solution_stages(solution,prompt):
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',solution,re.S)
 if len(blocks)<3:raise ValueError('Missing chain decomposition')
 split=lambda b:re.split(r',\\(?:,|quad|qquad)',b.strip())
 parts=split(blocks[0].replace(r'v\,v=',r'v,\,v='));assert len(parts)==3,parts
 rhs=[scalar(z.split('=',1)[1]) for z in parts]
 u=s.Symbol('u',real=True);v=s.Symbol('v',real=True)
 f,point=given(prompt)
 composed=rhs[0].subs(u,rhs[1]).subs(v,rhs[2]);assert equal(f,composed),'Wrong composition'
 derivative_parts=split(blocks[1]);assert len(derivative_parts)==3,derivative_parts
 ds=[scalar(z.split('=',1)[1]) for z in derivative_parts]
 expected=[s.diff(rhs[0],u),s.diff(rhs[1],v),s.diff(rhs[2],x)]
 assert all(equal(a,b) for a,b in zip(ds,expected)),'Wrong component derivative'
 derivative=s.diff(f,x)
 aligned=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)
 checks=0
 for n,block in enumerate(aligned):
  rows=re.split(r'\\\\',block)
  for row in rows:
   if '&' not in row:continue
   val=row.split('&',1)[1].strip()
   if not val.startswith('='):continue
   val=val[1:].strip()
   if r'\frac{\text{d}' in val or r'\frac{\mathrm{d}' in val:continue
   obj=scalar(val)
   if n==0:obj=obj.subs(u,rhs[1]).subs(v,rhs[2]);target=derivative
   else:target=derivative.subs(x,point)
   assert equal(obj,target),(val,obj,target)
   checks+=1
 assert checks>=2,'Missing numerical/substituted stages'
 return checks
