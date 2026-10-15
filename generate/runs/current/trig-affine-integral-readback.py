"""Root linear trig substitution, actual pole-free limits and signed endpoints."""
import importlib.util,re
from pathlib import Path
from functools import lru_cache
import sympy as s
z=importlib.util.spec_from_file_location('root_trig_def',Path(__file__).with_name('definite-elementary-readback.py'));D=importlib.util.module_from_spec(z);z.loader.exec_module(D)
P=D.P;x,u=P.x,P.u
@lru_cache(maxsize=10000)
def eq(a,b):
 delta=s.expand(a-b)
 if delta==0:return True
 return s.trigsimp(delta)==0 or s.trigsimp(delta.rewrite(s.sin))==0
@lru_cache(maxsize=4000)
def primitive(F,var):
 arguments={f.args[0]for f in F.atoms(s.sin,s.cos,s.tan,s.cot,s.sec,s.csc)}
 for arg in arguments:
  a=s.diff(arg,var)
  if a==0 or a.has(var):continue
  for f,prim in ((s.sec(arg)*s.tan(arg),s.sec(arg)),(s.csc(arg)*s.cot(arg),-s.csc(arg)),(s.sec(arg)**2,s.tan(arg)),(s.csc(arg)**2,-s.cot(arg))):
   coeff=s.cancel(F/(a*f))
   if not coeff.has(var):return coeff*prim
 raise AssertionError(('outside affine reciprocal-trig scope',F,var))
D.primitive=primitive

def endpoint_contributions(raw):
 text=D.clean(raw);depth=0;pairs=[];start=None
 for i,c in enumerate(text):
  if c=='(':
   if depth==0:start=i
   depth+=1
  elif c==')':
   depth-=1
   if depth==0:pairs.append((start,i))
 for start,end in pairs:
  if end!=len(text)-1:continue
  body=text[start+1:end];depth=0
  for i,c in enumerate(body):
   if c in '+-'and i>0 and depth==0 and body[i-1]not in '+-*/^':
    prefix=text[:start];co=D.scalar(prefix)if prefix not in ('','-')else s.Integer(-1 if prefix=='-'else 1);return co*D.scalar(body[:i]),(1 if c=='+'else -1)*co*D.scalar(body[i+1:])
   depth+=(c in '({')-(c in ')}')
 # Some captured solutions print the two trig endpoints without outer brackets.
 # Require an actual trig call: a final simplified sum may reorder terms freely.
 if re.search(r'sec|csc|tan|cot',text):
  depth=0
  for i,c in enumerate(text):
   if c in '+-' and i>0 and depth==0 and text[i-1] not in '+-*/^':
    return D.scalar(text[:i]),(1 if c=='+' else -1)*D.scalar(text[i+1:])
   depth+=(c in '({')-(c in ')}')
 return None

def given(q):
 raw=D.clean(next(b for b in D.blocks(q[':question/problem'])if r'\int'in b).rstrip('= .'))
 if re.search(r'\\int\s*_\{',raw):
  c,F,var,lo,hi,end=D.integral(raw);assert not end and var==x;return c*F,lo,hi
 F,var,_=P.integrand(raw);assert var==x;return F,None,None

def check(q):
 F,lo,hi=given(q);sol=q[':question/worked-solution'];match=re.search(r'\$u=([^$]+)\$',sol);assert match;U=D.scalar(match[1].rstrip(','));a=s.diff(U,x)
 # Ordinary profiles are affine; the one nonaffine record is evidence-only.
 affine=not a.has(x)
 differential=next(b for b in D.blocks(sol)if '⟹'in b);left,right=differential.split('⟹');assert D.clean(left.split('=',1)[0])==r'\frac{\mathrm{d}u}{\mathrm{d}x}';assert eq(D.scalar(left.split('=',1)[1]),a)
 l,r=right.strip().rstrip('.').split('=');lm=re.fullmatch(r'(.*?)'+P.DIFF,l.strip());rm=re.fullmatch(r'(.*?)'+P.DIFF,r.strip());assert lm and rm and{lm[2],rm[2]}=={'x','u'}
 def coeff(raw):return D.scalar(raw)if D.clean(raw).strip()else s.Integer(1)
 assert eq(coeff(lm[1])*(a if lm[2]=='u'else 1),coeff(rm[1])*(a if rm[2]=='u'else 1))
 counts=dict(integral_sides=0,primitive_sides=0,primitive_bars=0,bound_references=0,endpoint_components=0,differentials=2)
 table=re.findall(r'^\| \$([xu])\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',sol,re.M)
 if lo is not None:
  assert affine and a!=0 and len(table)==2;xl,xh=[D.scalar(t)for t in table[0][1:]];ul,uh=[D.scalar(t)for t in table[1][1:]];assert eq(xl,lo)and eq(xh,hi)and eq(U.subs(x,lo),ul)and eq(U.subs(x,hi),uh);counts['bound_references']+=4
  assert a>0 and lo<hi
  # Exactly the captured sin/cos pole-free components are supported.
  # SymPy may rewrite a shifted secant as a shifted cosecant; component
  # boundaries belong to the actual printed u, not that canonical rewrite.
  kernel='cos'if re.search(r'\\(?:sec|tan)|\\operatorname\{(?:sec|tan)\}|\{(?:sec|tan)\}',q[':question/problem'])else'sin';assert(-s.pi/2<ul<uh<s.pi/2)if kernel=='cos'else(0<ul<uh<s.pi)
  prim=primitive(F,x);expected=s.simplify(prim.subs(x,hi)-prim.subs(x,lo))
 else:assert not table;expected=None
 block=next(b for b in D.blocks(sol)if r'\begin{aligned}'in b);text=re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','');bar=None
 for row in text.split(r'\\'):
  for raw in row.split('='):
   if not raw.strip():continue
   if lo is None:
    value,inputs=P.side(raw,x,U);assert eq(value,F),('wrong indefinite actual operand/primitive',raw,value,F);counts['integral_sides'if inputs else'primitive_sides']+=1
   else:
    value,info=D.value(raw);assert eq(value,expected),('wrong actual definite row',raw,value,expected)
    if info[0]=='integral':
     _,body,var,l,h=info;assert var in(x,u)and eq(l,lo if var==x else ul)and eq(h,hi if var==x else uh);assert eq(body if var==x else body.subs(u,U)*a,F);counts['integral_sides']+=1;counts['bound_references']+=2
    elif info[0]=='bar':
     _,bar,l,h=info;assert eq(l,ul)and eq(h,uh)and eq(P.derivative(bar,x,U),F),('primitive bar',q[':question/problem'],raw,bar,l,h,ul,uh,P.derivative(bar,x,U),F);counts['primitive_bars']+=1;counts['bound_references']+=2
    else:
     terms=endpoint_contributions(raw)
     if terms is not None:
      assert bar is not None and eq(terms[0],bar.subs(u,uh))and eq(terms[1],-bar.subs(u,ul)),('correlated signed endpoint error',raw,terms,bar);counts['endpoint_components']+=2
 if lo is not None:assert counts['primitive_bars']==1 and counts['endpoint_components']>=2,(q[':question/problem'],counts)
 return F,expected,counts
