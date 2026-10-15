"""Root reader: derivatives of actual displayed primitives and integral sides.

Log-absolute derivatives use g'/g on real connected intervals where g!=0;
this differential comparison never treats constant-offset antiderivatives as
independent choices. Formal integral inputs remain explicit parsed operands.
"""
import importlib.util,re
from pathlib import Path
import sympy as s
from functools import lru_cache
z=importlib.util.spec_from_file_location('kp00818_scalar',Path(__file__).with_name('scalar_parser.py'));P=importlib.util.module_from_spec(z);z.loader.exec_module(P)
x,u,C=P.x,P.u,P.v
class RealLogAbs(s.Function):
 def fdiff(self,argindex=1):
  assert argindex==1
  return 1/self.args[0]
DIFF=r'(?:\\(?:text|mathrm|textrm)\{d\}|d)\s*([xyzut])'
def clean(t):
 t=t.strip().replace(r'\u2061','').replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','').replace(r'\;','').replace(r'\dfrac',r'\frac').replace(r'\mid','|').replace(r'\lvert','|').replace(r'\rvert','|')
 t=re.sub(r'\|([^|]+)\|',r'Abs(\1)',t);return re.sub(r'(?<![A-Za-z\\])C(?![A-Za-z])','v',t).strip().rstrip('.,?')
@lru_cache(maxsize=30000)
def scalar(t):
 t=clean(t).replace(r'\displaystyle','').replace(r'\cdot','*').replace(r'\u2061','')
 # Read the source's base-log notation as one mathematical function.
 pattern=r'(?:\{log\}|\\log|log)_'
 while m:=re.search(pattern,t):
  start=m.end();base,end=group(t,start)
  while end<len(t) and (t[end].isspace() or t[end]=='⁡'):end+=1
  if t[end]=='(':
   depth=1;j=end+1
   while depth:depth+=(t[j]=='(')-(t[j]==')');j+=1
   arg=t[end+1:j-1];end=j
  elif t[end]=='{':arg,end=group(t,end)
  elif t[end:end+5]==r'\frac':
   a,j=group(t,end+5);b,end=group(t,j);arg=r'\frac{'+a+'}{'+b+'}'
  else:
   z=re.match(r'(?:[0-9]+|[xu])',t[end:]);assert z,t[end:];arg=z[0];end+=len(arg)
  t=t[:m.start()]+r'\frac{\ln('+arg+r')}{\ln('+base+r')}' +t[end:]
 return P.scalar(t)
def group(t,i):
 if t[i]!='{':return t[i],i+1
 depth=1;j=i+1
 while depth:depth+=(t[j]=='{')-(t[j]=='}');j+=1
 return t[i+1:j-1],j

def eq(a,b,positive=False):
 d=s.expand(a-b)
 if d==0:return True
 if positive:d=s.powdenest(d,force=True)
 return s.simplify(d)==0
def fraction_measure(t):
 for m in list(re.finditer(r'\\frac\{(?:\\(?:text|mathrm|textrm)\{d\}|d)\s*([xu])\}\{',t))[::-1]:
  start=m.end()-1;den,end=group(t,start)
  t=t[:m.start()]+r'\frac{1}{'+den+r'}\,\text{d}'+m[1]+t[end:]
 return t

def integrand(t):
 t=fraction_measure(t)
 m=re.search(r'\\int\s*(.*?)'+DIFF,t,re.S);assert m,('missing actual integral',t);body=m[1].replace(r'\,','').replace(r'\!','').strip();body=body[:-len(r'\cdot')]if body.endswith(r'\cdot')else body
 return scalar(body)if body else s.Integer(1),P.locals_[m[2]],m
def prompt(t):
 if r'\int'in t:return integrand(t)[:2]
 chunks=re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',t,re.S);assert chunks
 variable_match=re.search(r'with respect to\s*\$([xyzut])',t);variable=P.locals_[variable_match[1]]if variable_match else x
 return scalar(chunks[0]),variable
def derivative(value,var,inner=None):
 if inner is not None:value=value.subs(u,inner)
 # This is a real derivative identity on the declared nonzero domains, not a
 # replacement of log|g| by log(g) in learner content or value comparisons.
 value=value.replace(lambda f:f.func==s.log and f.args[0].func==s.Abs,lambda f:RealLogAbs(f.args[0].args[0]))
 result=s.diff(value,var)
 return result.replace(lambda f:f.func==RealLogAbs,lambda f:s.log(s.Abs(f.args[0])))
def side(t,var=x,inner=None,positive=False):
 text=fraction_measure(re.sub(r'\\(?:begin|end)\{aligned\}','',t).replace('&','').strip().rstrip('.,'));formal=[]
 while r'\int'in text:
  start=text.index(r'\int');body,v,m=integrand(text[start:]);assert len(formal)<3
  token=['i','j','k'][len(formal)];symbol=P.locals_[token];formal.append((symbol,body,v));text=text[:start]+'('+token+')'+text[start+m.end():]
 value=scalar(text);rest=value;actual=s.Integer(0);inputs=[]
 for symbol,body,v in formal:
  coeff=s.expand(value).coeff(symbol);assert not coeff.has(var,u,*[z[0]for z in formal]),('nonconstant formal-integral multiplier',t,coeff);rest-=coeff*symbol
  if v==u:assert inner is not None;effective=body.subs(u,inner)*s.diff(inner,var)
  else:assert v==var,('stale differential variable',v,var);effective=body
  actual+=coeff*effective;inputs.append((body,v,coeff))
 if formal:rest=s.simplify(rest)
 assert not rest.has(*[z[0]for z in formal]),('unsupported formal integral tree',t,rest)
 actual+=derivative(rest,var,inner)
 if positive:actual=s.powdenest(actual,force=True)
 return actual,inputs
def stages(solution,expected,var=x,inner=None,positive=False):
 n=dict(integral_sides=0,primitive_sides=0,formal_inputs=0)
 for block in re.findall(r'\$\$(.*?)\$\$',solution,re.S):
  if r'\int'not in block:continue
  text=re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','')
  for row in text.split(r'\\'):
   for part in row.split('='):
    if not part.strip():continue
    value,inputs=side(part,var,inner,positive);assert eq(value,expected,positive),('wrong printed integral/primitive stage',part,value,expected)
    n['integral_sides'if inputs else'primitive_sides']+=1;n['formal_inputs']+=len(inputs)
 assert n['primitive_sides']>0,('no actual primitive solution stage',solution)
 return n
