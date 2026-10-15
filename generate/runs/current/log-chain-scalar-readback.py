"""Root real-variable scalar reader: composed log bases and branch-safe equality."""
import importlib.util,re
from pathlib import Path
from functools import lru_cache
import sympy as s
z=importlib.util.spec_from_file_location('root_log_chain_scalar',Path(__file__).with_name('ode-scalar-parser.py'));P=importlib.util.module_from_spec(z);z.loader.exec_module(P)
x,u=P.x,P.u

def group(t,i):
 assert t[i]in'({';closing=')'if t[i]=='('else'}';depth=1;j=i+1
 while depth:
  assert j<len(t);depth+=(t[j]==t[i])-(t[j]==closing);j+=1
 return t[i+1:j-1],j

def operand(t,i):
 while i<len(t)and t[i].isspace():i+=1
 if t[i]in'({':
  opening=t[i];body,end=group(t,i)
  # Invisible braces followed by a power belong to the source log argument.
  if opening=='{'and end<len(t)and t[end]=='^':
   p,k=operand(t,end+1);return '('+body+')^('+p+')',k
  return body,end
 if t.startswith(r'\sqrt',i):
  body,end=operand(t,i+5);return r'\sqrt{'+body+'}',end
 if t.startswith(r'\frac',i):
  numerator,end=operand(t,i+5);denominator,end=operand(t,end);return r'\frac{'+numerator+'}{'+denominator+'}',end
 m=re.match(r'-?\d+(?:\s*[xu])?|[xu]',t[i:]);assert m,('unsupported bare log argument',t[i:]);end=i+m.end();body=m[0]
 if end<len(t)and t[end]=='^':p,end=operand(t,end+1);body+='^('+p+')'
 return body,end

@lru_cache(maxsize=20000)
def scalar(raw):
 t=raw.strip().rstrip('.,').replace('⁡','').replace('−','-').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','').replace(r'\cancel','').replace(r'\big','')
 t=t.replace(r'\operatorname{log}',r'\log').replace('{log}',r'\log');t=re.sub(r'(?<![A-Za-z\\])log(?=[_{(xu0-9 ])',r'\\log',t)
 while (m:=re.search(r'\\log(?![A-Za-z])',t)):
  i=m.end()
  while i<len(t)and t[i].isspace():i+=1
  base='10'
  if t[i]=='_':
   i+=1
   if t[i]=='{':base,i=group(t,i)
   else:
    bm=re.match(r'\d+',t[i:]);assert bm;base=bm[0];i+=bm.end()
  arg,end=operand(t,i);t=t[:m.start()]+r'(\ln('+arg+r')/\ln('+base+'))'+t[end:]
 return P.scalar(t.replace('[','(').replace(']',')'))

@lru_cache(maxsize=20000)
def eq(a,b):
 delta=s.expand(a-b)
 if delta==0:return True
 # These operations do not discard signs or logarithm branches. Restrict any
 # domain-dependent simplification explicitly before calling this reader.
 return s.cancel(delta)==0 or s.simplify(delta)==0
