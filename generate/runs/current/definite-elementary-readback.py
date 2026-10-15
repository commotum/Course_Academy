"""Root definite-integral reader: actual bounds and separate endpoint values."""
import importlib.util,re
from pathlib import Path
from functools import lru_cache
import sympy as s
z=importlib.util.spec_from_file_location('root_def_elem',Path(__file__).with_name('elementary-integral-readback.py'));P=importlib.util.module_from_spec(z);z.loader.exec_module(P)
x,u=P.x,P.u

def clean(t):
 t=P.clean(t).replace(r'\big','').replace(r'\displaystyle','').replace(r'{\int }',r'\int').replace(r'{|}',r'|').replace(r'\text{d}',r'\mathrm{d}').replace(r'\textrm{d}',r'\mathrm{d}')
 return re.sub(r'\|\}(?=_)','|',t)
scalar=P.scalar
@lru_cache(maxsize=30000)
def equal(a,b):return s.simplify(s.expand_log(a-b,force=True))==0
def group(t,i):
 if t[i]!='{':return t[i],i+1
 depth=1;j=i+1
 while depth:
  assert j<len(t);depth+=(t[j]=='{')-(t[j]=='}');j+=1
 return t[i+1:j-1],j
@lru_cache(maxsize=4000)
def primitive(F,var):
 for e in F.atoms(s.exp):
  c=s.cancel(F/(e*s.diff(e.args[0],var)))
  if not c.has(var):return c*e
 for e in F.atoms(s.Pow):
  if not e.base.has(var)and e.exp.has(var):
   c=s.cancel(F/(e*s.diff(e.exp,var)))
   if not c.has(var):return c*e/s.log(e.base)
 numerator,denominator=s.fraction(s.cancel(F));c=s.simplify(numerator/s.diff(denominator,var))
 assert denominator.has(var)and not c.has(var),('outside source definite primitive families',F)
 return c*s.log(denominator)
def integral(raw):
 text=clean(raw);i=text.index(r'\int');pos=i+4
 while text[pos].isspace():pos+=1
 assert text[pos]=='_',text;lo,pos=group(text,pos+1);assert text[pos]=='^';hi,pos=group(text,pos+1)
 m=re.search(P.DIFF,text[pos:]);assert m,text;body=text[pos:pos+m.start()].strip();body=body[:-len(r'\cdot')]if body.endswith(r'\cdot')else body
 coefficient=scalar(text[:i])if text[:i].strip()else s.Integer(1);F=scalar(body);var=P.P.locals_[m[1]];return coefficient,F,var,scalar(lo),scalar(hi),text[pos+m.end():]
def value(raw):
 text=clean(raw)
 if r'\int'in text:
  c,F,var,lo,hi,end=integral(text);assert not end,end;prim=primitive(F,var);return c*(prim.subs(var,hi)-prim.subs(var,lo)),('integral',c*F,var,lo,hi)
 m=re.search(r'\|_',text)
 if m:
  before=text[:m.start()];after=text[m.end():];lo,pos=group(after,0);assert after[pos]=='^';hi,pos=group(after,pos+1);assert not after[pos:]
  # Normalize the source's extra MathML grouping brace around a bar.
  if before.startswith('{')and before.count('{')>before.count('}'):before=before[1:]
  prim=scalar(before);lo,hi=scalar(lo),scalar(hi);assert prim.has(u)
  return prim.subs(u,hi)-prim.subs(u,lo),('bar',prim,lo,hi)
 return scalar(text),('value',)
def endpoint_terms(raw):
 text=clean(raw);depth=0;pairs=[];start=None
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
   depth+=(c in '({')-(c in ')}')
   if c=='-'and depth==0:
    coeff=scalar(text[:start])if text[:start]else s.Integer(1);return coeff*scalar(body[:i]),coeff*scalar(body[i+1:])
 return None
def blocks(text):return [next(t for t in pair if t)for pair in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',text,re.S)]
def stages(q):
 prompt=q[':question/problem'];sol=q[':question/worked-solution'];given=next(b for b in blocks(prompt)if r'\int'in b).rstrip('= .');c,F,var,lo,hi,end=integral(given);assert var==x and not end
 expected=c*(primitive(F,x).subs(x,hi)-primitive(F,x).subs(x,lo));U=scalar(re.search(r'\$u=([^$]+)\$',sol)[1]);du=s.diff(U,x)
 derivative_block=next(b for b in blocks(sol)if '⟹'in b or r'\Longrightarrow'in b);a,b=re.split(r'⟹|\\quad\\Longrightarrow\\quad',derivative_block,maxsplit=1);assert clean(a.split('=',1)[0])==r'\frac{\mathrm{d}u}{\mathrm{d}x}';actual=scalar(a.split('=',1)[1]);assert equal(actual,du)
 a,b=b.split('=');l=re.fullmatch(r'(.*?)'+P.DIFF,a.strip());r=re.fullmatch(r'(.*?)'+P.DIFF+r'[.]?',b.strip());assert l and r and l[2]=='u'and r[2]=='x';co=lambda t:scalar(t)if clean(t).strip()else s.Integer(1);assert equal(co(l[1])*du,co(r[1]))
 table=re.findall(r'^\| \$([xu])\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',sol,re.M);assert [t[0]for t in table]==['x','u'];xl,xh=[scalar(t)for t in table[0][1:]];ul,uh=[scalar(t)for t in table[1][1:]];assert equal(xl,lo)and equal(xh,hi)and equal(U.subs(x,xl),ul)and equal(U.subs(x,xh),uh)
 N=dict(rows=0,integral_inputs=0,primitive_bars=0,individual_endpoints=0,bound_references=4,differentials=2);last_primitive=None
 aligned=next(b for b in blocks(sol)if r'\begin{aligned}'in b);aligned=re.sub(r'\\(?:begin|end)\{aligned\}','',aligned).replace('&','')
 for row in aligned.split(r'\\'):
  for part in row.split('='):
   if not part.strip():continue
   v,info=value(part);assert equal(v,expected),('wrong definite row',part,v,expected)
   if info[0]=='integral':
    _,body,ivar,bl,bh=info;assert equal(bl,lo if ivar==x else ul)and equal(bh,hi if ivar==x else uh);assert equal(body if ivar==x else body.subs(u,U)*du,c*F);N['integral_inputs']+=1;N['bound_references']+=2
   elif info[0]=='bar':
    _,prim,bl,bh=info;assert equal(bl,ul)and equal(bh,uh)and equal(P.derivative(prim,x,U),c*F);last_primitive=prim;N['primitive_bars']+=1;N['bound_references']+=2
   elif (terms:=endpoint_terms(part))and last_primitive is not None:
    assert equal(terms[0],last_primitive.subs(u,uh))and equal(terms[1],last_primitive.subs(u,ul)),('correlated endpoint arithmetic error',part);N['individual_endpoints']+=2
   N['rows']+=1
 assert N['primitive_bars']==1 and N['individual_endpoints']>=2
 return expected,N
