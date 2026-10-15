"""Root actual nonlinear trig substitution and each endpoint contribution."""
import importlib.util
from pathlib import Path
import sympy as s
z=importlib.util.spec_from_file_location('root_nonlin_trig_base',Path(__file__).with_name('trig-affine-integral-readback.py'));T=importlib.util.module_from_spec(z);z.loader.exec_module(T)
P=T.P;x=P.x
@T.lru_cache(maxsize=5000)
def primitive(F,var):
 args={f.args[0]for f in F.atoms(s.sin,s.cos,s.sec,s.csc,s.tan,s.cot)}
 for arg in args:
  a=s.diff(arg,var)
  if a==0:continue
  for body,H in((s.sin(arg),-s.cos(arg)),(s.cos(arg),s.sin(arg)),(s.sec(arg)**2,s.tan(arg)),(s.csc(arg)**2,-s.cot(arg)),(s.sec(arg)*s.tan(arg),s.sec(arg))):
   ratio=s.cancel(F/(a*body))
   if not ratio.has(var):return ratio*H
 raise AssertionError(('outside supported nonlinear substitution',F,var))
T.primitive=primitive;T.D.primitive=primitive
def check(q):
 F,lo,hi=T.given(q)
 if lo is not None:
  # The only reciprocal definite family is sec*tan with u in[0,pi/3].
  if F.has(s.sec,s.tan):
   import re
   tab=re.findall(r'^\| \$u\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',q[':question/worked-solution'],re.M);assert len(tab)==1;ul,uh=map(T.D.scalar,tab[0]);assert -s.pi/2<ul<uh<s.pi/2
 return T.check(q,False,False)
