"""Small independent LaTeX parser for this KP's scalar expression subset.

Supports captured unicode trig notation and SymPy's generated math. It fails
closed on unsupported tokens. This is a review check, never a learner grader.
"""
import re
import sympy as sp
u,v=sp.symbols('u v',real=True)

def parse(text):
 text=text.replace('\u2061','').replace('⁡','').replace('−','-').replace('²','^{2}')
 text=re.sub(r'\\operatorname\{(sin|cos|tan|ln)\}',r'\1',text)
 text=re.sub(r'\{(sin|cos|tan|ln|e)\}',r'\1',text)
 for x in ('left','right'): text=text.replace('\\'+x,'')
 text=text.replace('\\,','').replace('\\cdot','*').replace('\\','')
 tokens=re.findall(r'frac|sqrt|sin|cos|tan|ln|log|[uve]|\d+|[{}()+\-*/^]',text)
 if re.sub(r'\s+','',text)!=''.join(tokens): raise ValueError('Unsupported math: '+text)
 pos=0
 def peek(): return tokens[pos] if pos<len(tokens) else None
 def eat(t=None):
  nonlocal pos
  a=peek()
  if a is None or t is not None and a!=t: raise ValueError(f'Expected {t}, got {a}: {text}')
  pos+=1;return a
 def group():
  opener=eat(); closer={"(":")","{":"}"}.get(opener)
  if closer is None: raise ValueError('Group required')
  result=add();eat(closer);return result
 def atom():
  t=peek()
  if t in ('+','-'):
   eat();return atom()*(1 if t=='+' else -1)
  if t in ('(','{'): z=group()
  elif t=='frac':
   eat(); z=group()/group()
  elif t=='sqrt':
   eat();z=sp.sqrt(group())
  elif t in ('sin','cos','tan','ln','log'):
   eat(); power=None
   if peek()=='^': eat();power=atom()
   # Function input is one atom/group, not an entire adjacent product.
   arg=atom(); z={'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,'ln':sp.log,'log':sp.log}[t](arg)
   if power is not None: z=z**power
  elif t in ('u','v','e'): eat();z={'u':u,'v':v,'e':sp.E}[t]
  elif t and t.isdigit(): eat();z=sp.Integer(t)
  else: raise ValueError(f'Unexpected {t}: {text}')
  if peek()=='^': eat();z=z**atom()
  return z
 def mul():
  z=atom()
  while peek() not in (None,'+','-',')','}'):
   if peek() in ('*','/'): op=eat();a=atom();z=z*a if op=='*' else z/a
   else: z=z*atom()
  return z
 def add():
  z=mul()
  while peek() in ('+','-'): op=eat();a=mul();z=z+a if op=='+' else z-a
  return z
 result=add()
 if pos!=len(tokens): raise ValueError('Trailing tokens')
 return result
