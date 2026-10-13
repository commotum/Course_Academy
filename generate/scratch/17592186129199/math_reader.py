"""Small independent reader for displayed source/generator TeX expressions.
Rejects unknown tokens. Integral bounds are read from the actual displayed bank.
"""
import re
import sympy as s
x,y=s.symbols('x y',real=True);r=s.Symbol('r',nonnegative=True);theta=s.Symbol('theta',real=True)
LOCAL={'x':x,'y':y,'r':r,'theta':theta,'pi':s.pi,'e':s.E}
def group(text,i):
 assert text[i]=='{';depth=1;j=i+1
 while depth:
  if text[j]=='{':depth+=1
  if text[j]=='}':depth-=1
  j+=1
 return text[i+1:j-1],j

def expr(text):
 text=re.sub(r'\\operatorname\{(sin|cos|ln)\}',r'\\\1',text)
 text=text.replace('⁡','').replace('θ',r'\theta').replace('π',r'\pi').replace('Δ',r'\Delta')
 text=text.replace(r'\left','').replace(r'\right','')
 text=re.sub(r'\{(cos|sin)\}',r'\\\1',text)
 toks=re.findall(r'\\[A-Za-z]+|\d+(?:\.\d+)?|[xyre]|[{}()^+*/-]',text)
 residue=re.sub(r'\\[A-Za-z]+|\d+(?:\.\d+)?|[xyre]|[{}()^+*/-]|\s|[,\u00a0]','',text)
 if residue:raise ValueError(('unparsed',text,residue))
 toks=[t for t in toks if t not in (r'\,',r'\:',r'\ ')]
 i=0
 def atom():
  nonlocal i
  if i>=len(toks):raise ValueError('missing atom '+text)
  t=toks[i];i+=1
  if t=='-':return -atom()
  if t=='+':return atom()
  if t in ('{','('):
   v=add();close='}' if t=='{' else ')'
   if i>=len(toks) or toks[i]!=close:raise ValueError('unclosed '+text)
   i+=1;return v
  if t in (r'\frac',r'\dfrac'):return atom()/atom()
  if t==r'\sqrt':return s.sqrt(atom())
  if t in (r'\sin',r'\cos',r'\ln'):
   power=1
   if i<len(toks) and toks[i]=='^':i+=1;power=atom()
   arg=atom()
   # Legacy sin 2 theta has an implicit numeric function argument.
   if arg.is_number and i<len(toks) and toks[i]==r'\theta':arg*=atom()
   return {r'\sin':s.sin,r'\cos':s.cos,r'\ln':s.log}[t](arg)**power
  if t.startswith('\\'):t=t[1:]
  if t in LOCAL:return LOCAL[t]
  if re.fullmatch(r'\d+(?:\.\d+)?',t):return s.Rational(t)
  raise ValueError(('unknown',t,text))
 def power():
  nonlocal i
  a=atom()
  while i<len(toks) and toks[i]=='^':i+=1;a=a**atom()
  return a
 def mul():
  nonlocal i
  a=power()
  while i<len(toks) and toks[i] not in ('+','-','}',')'):
   t=toks[i]
   if t in ('*','/'):i+=1;b=power();a=a*b if t=='*' else a/b
   else:a*=power()
  return a
 def add():
  nonlocal i
  a=mul()
  while i<len(toks) and toks[i] in ('+','-'):
   t=toks[i];i+=1;b=mul();a=a+b if t=='+' else a-b
  return a
 v=add()
 if i!=len(toks):raise ValueError(('remaining',text,toks[i:]))
 return v

def integral_components(text):
 # Each bank is outer theta integral followed by inner r integral.
 starts=list(re.finditer(r'\\int\s*\}?\s*_',text))
 if len(starts)!=2:raise ValueError(('expected two integrals',text))
 bounds=[];spans=[];ends=[]
 for m in starts:
  i=m.end()
  lo,i=group(text,i)
  if text[i]!='^':raise ValueError(text)
  hi,j=group(text,i+1)
  bounds.extend([lo,hi]);spans.extend([(m.end()+1,i-1),(i+2,j-1)]);ends.append(j)
 tail=text[ends[1]:]
 tail=re.split(r'\\,?\\text\{d\}|\\text\{d\}|\\mathrm\{d\}|drd',tail)[0]
 # Remove trailing spacing before d r; source q161044 uses drdθ.
 tail=re.sub(r'(?:\\[,:]\s*)+$','',tail.strip())
 return bounds,tail,spans

def read_integral(text):
 b,f,_=integral_components(text)
 return [expr(v) for v in b],expr(f)
