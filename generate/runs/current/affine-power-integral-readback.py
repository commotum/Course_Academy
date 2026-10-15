"""Root actual affine-power integrals, formal derivative operands and positive branches."""
import importlib.util,re
from pathlib import Path
from functools import lru_cache
import sympy as s
z=importlib.util.spec_from_file_location('root_affine_power_scalar',Path(__file__).with_name('elementary-integral-readback.py'));P=importlib.util.module_from_spec(z);z.loader.exec_module(P)
x,u=P.x,P.u;W=s.Symbol('W',positive=True)
def mathnorm(t):
 t=re.sub(r'(?<![A-Za-z\\])d[ystz](?![A-Za-z])','dx',t)
 return re.sub(r'(?<![A-Za-z\\])[ystz](?![A-Za-z])','x',t)
def blocks(t):return [mathnorm(b)for b in re.findall(r'\$\$(.*?)\$\$',t,re.S)]
def coordinate(U,lower=0):
 a=s.diff(U,x);b=U.subs(x,0);assert a!=0 and not a.has(x)
 return (W+lower-b)/a
@lru_cache(maxsize=40000)
def eq(a,b,coord=None):
 delta=a-b
 if delta==0:return True
 if coord is not None:delta=delta.subs(x,coord)
 return s.cancel(delta)==0 or s.simplify(delta)==0
DER=r'\frac{\text{d}}{\text{d}x}'
def verification(raw):
 text=P.clean(raw.replace('✓',''));operands=[];computed={}
 while DER in text:
  at=text.index(DER);i=at+len(DER)
  while text[i].isspace():i+=1
  opening=text[i];assert opening in '([';closing=')'if opening=='('else']';depth=1;j=i+1
  while depth:
   assert j<len(text);depth+=(text[j]==opening)-(text[j]==closing);j+=1
  operand=P.scalar(text[i+1:j-1]);operands.append(operand);token=('i','j','k')[len(operands)-1];computed[P.P.locals_[token]]=s.diff(operand,x);text=text[:at]+'('+token+')'+text[j:]
 return P.scalar(text).subs(computed),operands

def check(q,lower=0,positive=False,stages=True):
 F,var=P.prompt(mathnorm(next(b for b in re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',q[':question/problem'],re.S)if r'\int'in b)));assert var==x
 sol=q[':question/worked-solution'];U=P.scalar(mathnorm(re.search(r'let\s+\$u=([^$]+)\$',sol,re.I)[1]));a=s.diff(U,x);assert a!=0 and not a.has(x);coord=coordinate(U,lower)if positive else None
 n=dict(records=1,substitutions=1,integral_sides=0,primitive_sides=0,formal_integrals=0,verification_sides=0,formal_derivatives=0,whole_primitive_operands=0,values=0,pairs=0)
 f=q[':question/answer-fields'][0];vals=[P.scalar(mathnorm(v[':answer/value']))for v in f[':answer-field/choices']];ds=[P.derivative(v,x)for v in vals];correct=next(v for z,v in zip(f[':answer-field/choices'],vals)if z[':answer/id']==f[':answer-field/correct'][1]);assert [z[':answer/id']for z,d in zip(f[':answer-field/choices'],ds)if eq(d,F,coord)]==[f[':answer-field/correct'][1]],('bank key',q[':question/problem'],ds,F)
 for i,d in enumerate(ds):
  for e in ds[:i]:assert not eq(d,e,coord),('modulo constant duplicate',q[':question/problem'],d,e);n['pairs']+=1
 n['values']=len(vals)
 if not stages:return F,U,n
 bb=blocks(sol);assert len(bb)==4
 diff=bb[1];left,right=diff.split('⟹');assert P.clean(left.split('=')[0])==r'\frac{\text{d}u}{\text{d}x}'and eq(P.scalar(left.split('=',1)[1]),a)
 l,r=right.strip().rstrip('.,').split('=');assert P.clean(l)==r'\text{d}x';dm=re.fullmatch(r'(.*?)'+P.DIFF,r.strip());assert dm and dm[2]=='u';co=s.Integer(-1)if P.clean(dm[1])=='-'else P.scalar(dm[1])if P.clean(dm[1])else s.Integer(1);assert eq(co*a,1)
 for block in (bb[0],bb[2]):
  text=re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','')
  for row in text.split(r'\\'):
   for part in row.split('='):
    if not part.strip():continue
    value,formal=P.side(part,x,U);assert eq(value,F,coord),('actual integral/primitive stage',part,value,F);n['integral_sides'if formal else'primitive_sides']+=1;n['formal_integrals']+=len(formal)
 text=re.sub(r'\\(?:begin|end)\{aligned\}','',bb[3]).replace('&','');first=True
 for row in text.split(r'\\'):
  for part in row.split('='):
   if not part.strip():continue
   value,operands=verification(part);assert eq(value,F,coord),('actual derivative verification',part,value,F)
   if first:assert len(operands)==1 and eq(P.derivative(operands[0]-correct,x),0,coord);n['whole_primitive_operands']+=1;first=False
   n['formal_derivatives']+=len(operands);n['verification_sides']+=1
 return F,U,n
