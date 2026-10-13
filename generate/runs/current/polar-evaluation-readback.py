"""Parent independently reduces printed integrals/bracketed primitives to CAS.

Uses the existing fail-closed scalar reader, not a generator's parameter or
answer recipes. Keeps every integral and endpoint primitive as a separate node.
"""
import importlib.util,re,functools
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('parent_polar_setup',Path(__file__).with_name('polar-setup-readback.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
R,T=p.R,p.T
def normalize(text):
 text=text.replace('⁡','').replace('π',r'\pi').replace('θ',r'\theta')
 text=re.sub(r'\\operatorname\{(sin|cos|csc|cot)\}',lambda m:'\\'+m[1],text)
 text=re.sub(r'\\operatorname\{ln\}',r'\\ln',text)
 text=re.sub(r'\{(sin|cos|csc|cot)\}',lambda m:'\\'+m[1],text)
 text=re.sub(r'\\(?:textrm|mathrm|text)\s*\{?\s*d\s*\}?\s*(?:\\,)?\s*(r|\\theta)',lambda m:'DR' if m[1]=='r' else 'DT',text)
 text=text.replace(r'd\theta','DT').replace('dr','DR')
 text=re.sub(r'\\(?:left|right|displaystyle|limits)','',text)
 text=re.sub(r'\{\\int\s*\}',r'\\int',text)
 text=text.replace('{[','[').replace(']}_',']_')
 return re.sub(r'\s+','',text).rstrip('.')
@functools.lru_cache(maxsize=8192)
def integrate(f,var,a,b):return s.integrate(f,(var,a,b))
def read(text):
 text=normalize(text);nodes=[];primitives=[]
 def process(raw):
  # Remove innermost definite integral first. Its differential terminates its
  # complete body; the outer body may include scalar factors before it.
  while r'\int' in raw:
   starts=list(re.finditer(r'\\int_',raw));assert starts,raw
   m=starts[-1];lo,pos=p.group(raw,m.end());assert raw[pos]=='^',raw
   hi,pos=p.group(raw,pos+1);end=re.search(r'DR|DT',raw[pos:]);assert end,raw
   stop=pos+end.start();var=R if end[0]=='DR' else T
   f=process(raw[pos:stop]);a,b=p.scalar(lo),p.scalar(hi)
   nodes.append((f,var,a,b));value=integrate(f,var,a,b)
   raw=raw[:m.start()]+'('+s.latex(value)+')'+raw[stop+2:]
  # Endpoint brackets can nest inside an angular integral. Ordinary arithmetic
  # brackets have no subscript and pass through to the strict scalar reader.
  while True:
   stack=[];found=None
   for i,ch in enumerate(raw):
    if ch=='[':stack.append(i)
    elif ch==']':
     assert stack,raw;start=stack.pop()
     if raw[i+1:i+2]=='_':found=(start,i);break
   if found is None:break
   start,end=found;lo,pos=p.group(raw,end+2);assert raw[pos]=='^',raw
   hi,pos=p.group(raw,pos+1);primitive=process(raw[start+1:end]);a,b=p.scalar(lo),p.scalar(hi)
   var=R if primitive.has(R) else T
   primitives.append((primitive,var,a,b));value=primitive.subs(var,b)-primitive.subs(var,a)
   raw=raw[:start]+'('+s.latex(value)+')'+raw[pos:]
  assert not any(v in raw for v in ('DR','DT',r'\int')),raw
  return p.scalar(raw.replace('[','(').replace(']',')').replace(r'\frac12',r'\frac{1}{2}').replace(r'\frac\pi2',r'\frac{\pi}{2}'))
 value=process(text)
 return s.simplify(value),nodes,primitives
def equal(a,b):return p.equal(a,b)
