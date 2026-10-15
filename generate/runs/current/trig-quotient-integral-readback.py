"""Root quotient substitution, log-absolute primitives and separate actual endpoints."""
import importlib.util,re
from pathlib import Path
import sympy as s
R=Path(__file__).parent
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
T=load('root_quotient_trig_scalar',R/'trig-affine-integral-readback.py');A=load('root_quotient_D',R/'affine-power-integral-readback.py');D=T.D;P=T.P;x,u=P.x,P.u
# Use a primitive computed from the actual denominator derivative, not KP metadata.
B=load('root_quotient_primitive',R/'definite-elementary-readback.py');D.primitive=B.primitive
base_scalar=P.scalar;P.scalar=lambda raw:base_scalar(re.sub(r'(?<![A-Za-z\\])K(?![A-Za-z])','k',raw))
@T.lru_cache(maxsize=20000)
def eq(a,b):
 delta=s.expand_log(a-b)
 return delta==0 or s.simplify(delta)==0 or T.eq(a,b)
def signed_parts(raw):
 text=D.clean(raw)
 def split(body):
  depth=0
  for i,c in enumerate(body):
   if c in '+-' and i>0 and depth==0 and body[i-1]not in '+-*/^':return P.scalar(body[:i]),(1 if c=='+'else -1)*P.scalar(body[i+1:])
   depth+=(c in '({')-(c in ')}')
  return None
 result=split(text)
 if result is not None:return result
 depth=0;start=None
 for i,c in enumerate(text):
  if c=='(':
   if depth==0:start=i
   depth+=1
  elif c==')':
   depth-=1
   if depth==0 and i==len(text)-1:
    terms=signed_parts(text[start+1:i])
    if terms is None:return None
    prefix=text[:start]
    if prefix in ('','-'):co=s.Integer(-1 if prefix=='-'else 1)
    else:
     try:co=P.scalar(prefix)
     except (ValueError,AssertionError):return None
    return co*terms[0],co*terms[1]
 return None

def check(original):
 q={k:A.mathnorm(v)if k in(':question/problem',':question/worked-solution')else v for k,v in original.items()};F,lo,hi=T.given(q);sol=q[':question/worked-solution'];U=P.scalar(re.search(r'\$u=([^$]+)\$',sol)[1]);du=s.diff(U,x)
 db=next(b for b in D.blocks(sol)if '⟹'in b);l,r=db.split('⟹');assert D.clean(l.split('=',1)[0])==r'\frac{\mathrm{d}u}{\mathrm{d}x}'and eq(P.scalar(l.split('=',1)[1]),du);ll,rr=r.strip().rstrip('.,').split('=');lm=re.fullmatch('(.*?)'+P.DIFF,ll.strip());rm=re.fullmatch('(.*?)'+P.DIFF,rr.strip());assert lm and rm and{lm[2],rm[2]}=={'x','u'}
 def co(m):return s.Integer(-1)if D.clean(m[1])=='-'else P.scalar(m[1])if D.clean(m[1])else s.Integer(1)
 assert eq(co(lm)*(du if lm[2]=='u'else 1),co(rm)*(du if rm[2]=='u'else 1));N=dict(substitutions=1,differentials=2,formal_derivatives=0,integral_sides=0,primitive_sides=0,primitive_bars=0,endpoint_components=0,bound_references=0)
 for b in D.blocks(sol):
  if A.DER in b:
   left,right=b.split('=',1);value,operands=A.verification(left);assert len(operands)==1 and eq(operands[0],U)and eq(value,P.scalar(right));N['formal_derivatives']+=1
 if lo is None:
  expected=None;first_primitive=None
 else:
  table=re.findall(r'^\| \$([xu])\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',sol,re.M);assert[t[0]for t in table]==['x','u'];xl,xh=map(P.scalar,table[0][1:]);ul,uh=map(P.scalar,table[1][1:]);assert lo<hi and eq(xl,lo)and eq(xh,hi)and eq(U.subs(x,lo),ul)and eq(U.subs(x,hi),uh);assert ul.is_positive is True and uh.is_positive is True;N['bound_references']+=4
  # Every definite family uses x without a hidden argument scale. The captured
  # sin/cos intervals and reciprocal trig pole-free components are preserved.
  args={v.args[0]for v in F.atoms(s.sin,s.cos,s.sec,s.csc,s.tan,s.cot)};assert args=={x}
  if F.has(s.sec,s.tan):assert -s.pi/2<lo<hi<s.pi/2
  if F.has(s.csc,s.cot):assert 0<lo<hi<s.pi
  primitive=B.primitive(F,x);expected=s.simplify(primitive.subs(x,hi)-primitive.subs(x,lo));bar=None
 for b in D.blocks(sol):
  if r'\begin{aligned}'not in b:continue
  text=re.sub(r'\\(?:begin|end)\{aligned\}','',b).replace('&','')
  for row in text.split(r'\\'):
   for part in row.split('='):
    if not part.strip():continue
    if lo is None:
     value,inputs=P.side(part,x,U);assert eq(value,F),('actual indefinite quotient stage',part,value,F);N['integral_sides'if inputs else'primitive_sides']+=1
     if not inputs:
      expression=P.scalar(part).subs(u,U)
      if first_primitive is None:first_primitive=expression
      relation=re.search(r'\$K=([^$]+)\$',sol)
      if relation:expression=expression.subs(P.P.locals_['k'],P.scalar(relation[1]))
      assert eq(expression,first_primitive),('primitive constant/operative equality',part,expression,first_primitive)
    else:
     value,info=D.value(part);assert eq(value,expected),('actual definite quotient stage',part,value,expected)
     if info[0]=='integral':
      _,body,v,l,h=info;assert eq(l,lo if v==x else ul)and eq(h,hi if v==x else uh);assert eq(body if v==x else body.subs(u,U)*du,F);N['integral_sides']+=1;N['bound_references']+=2
     elif info[0]=='bar':
      _,bar,l,h=info;assert eq(l,ul)and eq(h,uh)and eq(P.derivative(bar,x,U),F);N['primitive_bars']+=1;N['bound_references']+=2
     else:
      terms=signed_parts(part)
      if terms is not None:
       assert bar is not None;targets=(bar.subs(u,uh),-bar.subs(u,ul));assert(eq(terms[0],targets[0])and eq(terms[1],targets[1]))or(eq(terms[0],targets[1])and eq(terms[1],targets[0])),('correlated logarithmic endpoint error',part,terms,targets);N['endpoint_components']+=2
 if lo is not None:assert N['primitive_bars']==1 and N['endpoint_components']>=2
 return F,expected,N
