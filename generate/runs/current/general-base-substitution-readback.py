"""Root actual general-base substitutions, prime-log aliases, real positive bases."""
import importlib.util,re
from pathlib import Path
from functools import lru_cache
import sympy as s
z=importlib.util.spec_from_file_location('root_general_base_scalar',Path(__file__).with_name('elementary-integral-readback.py'));P=importlib.util.module_from_spec(z);z.loader.exec_module(P)
x,u=P.x,P.u
@lru_cache(maxsize=30000)
def canonical(expr):
 # Positive numeric bases permit this exponential identity on every real x.
 expr=expr.replace(lambda p:p.is_Pow and p.base.is_positive is True and not p.base.has(x,u)and p.exp.has(x,u),lambda p:s.exp(p.exp*s.expand_log(s.log(p.base))))
 return s.expand_log(expr)
@lru_cache(maxsize=30000)
def eq(a,b):
 delta=canonical(a)-canonical(b)
 return delta==0 or s.cancel(delta)==0 or s.simplify(delta)==0

def substitution(q):
 sol=q[':question/worked-solution'];m=re.search(r'\$u=([^$]+)\$',sol)
 if m:U=P.scalar(m[1])
 else:
  block=next(b.strip()for b in re.findall(r'\$\$(.*?)\$\$',sol,re.S)if re.match(r'\s*u=',b));U=P.scalar(block.split('=',1)[1])
 du=s.diff(U,x);assert du!=0
 db=next(b for b in re.findall(r'\$\$(.*?)\$\$',sol,re.S)if '⟹'in b);db=re.sub(r'\\(?:begin|end)\{aligned\}','',db).replace('&','');left,right=db.split('⟹');assert P.clean(left.split('=',1)[0])==r'\frac{\text{d}u}{\text{d}x}'and eq(P.scalar(left.split('=',1)[1]),du)
 l,r=right.strip().rstrip('.,').split('=');lm=re.fullmatch('(.*?)'+P.DIFF,l.strip());rm=re.fullmatch('(.*?)'+P.DIFF,r.strip());assert lm and rm and{lm[2],rm[2]}=={'x','u'}
 def coeff(m):return s.Integer(-1)if P.clean(m[1])=='-'else P.scalar(m[1])if P.clean(m[1])else s.Integer(1)
 assert eq(coeff(lm)*(du if lm[2]=='u'else 1),coeff(rm)*(du if rm[2]=='u'else 1))
 return U

def indefinite(q):
 F,var=P.prompt(q[':question/problem']);assert var==x;U=substitution(q);N=dict(records=1,substitutions=1,differentials=2,integral_sides=0,primitive_sides=0,formal_inputs=0,values=0,pairs=0)
 for b in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S):
  if r'\int'not in b:continue
  text=re.sub(r'\\(?:begin|end)\{aligned\}','',b).replace('&','')
  for row in text.split(r'\\'):
   for part in row.split('='):
    if not part.strip():continue
    val,formal=P.side(part,x,U);assert eq(val,F),('actual general-base formal/primitive stage',part,val,F);N['integral_sides'if formal else'primitive_sides']+=1;N['formal_inputs']+=len(formal)
 f=q[':question/answer-fields'][0];vals=[P.scalar(a[':answer/value'])for a in f[':answer-field/choices']];ds=[P.derivative(v,x)for v in vals];assert[a[':answer/id']for a,d in zip(f[':answer-field/choices'],ds)if eq(d,F)]==[f[':answer-field/correct'][1]]
 for i,d in enumerate(ds):
  for e in ds[:i]:assert not eq(d,e);N['pairs']+=1
 N['values']=len(vals)
 return F,U,N

def task(F):
 # Full positive-base monomial-exponent integrands are determined by their
 # logarithmic derivative and leading nonzero coefficient at x=0.
 lead=F.as_leading_term(x);p=lead.as_powers_dict().get(x,s.Integer(0));assert p.is_integer and p>=0;amplitude=s.simplify(lead/x**p);assert not amplitude.has(x)and amplitude!=0;rate=s.cancel(s.diff(F,x)/F);return str(p),s.srepr(s.expand(canonical(rate))),s.srepr(s.simplify(amplitude))
