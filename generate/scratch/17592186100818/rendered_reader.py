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
def equal(a,b):
 d=a-b
 if d==0:return True
 xp=s.Symbol('positive_x',positive=True);up=s.Symbol('positive_u',positive=True)
 d=d.subs({x:xp,u:up})
 return s.simplify(s.expand_log(d,force=False))==0

def group(t,i):
 if t[i]!='{':return t[i],i+1
 depth=1;j=i+1
 while depth:
  assert j<len(t);depth+=(t[j]=='{')-(t[j]=='}');j+=1
 return t[i+1:j-1],j
@lru_cache(maxsize=4000)
def primitive(F,var):
 # Independently recover the actual displayed function's elementary rule.
 for L in sorted(F.atoms(s.log),key=str):
  D=s.diff(L,var)
  if D==0:continue
  for p in (s.Integer(1),s.Rational(1,2),s.Rational(-1,2),s.Integer(-1),s.Integer(-2)):
   c=s.cancel(F/(D*L**p))
   if not c.has(var):return c*s.log(s.Abs(L)) if p==-1 else c*L**(p+1)/(p+1)
 for p in (s.Integer(1),s.Rational(1,2),s.Rational(-1,2),s.Integer(-1),s.Integer(-2)):
  c=s.cancel(F/var**p)
  if not c.has(var):return c*s.log(s.Abs(var)) if p==-1 else c*var**(p+1)/(p+1)
 raise AssertionError(('outside definite logarithm family',F,var))

def integral(raw):
 text=clean(P.fraction_measure(raw)).strip().rstrip('.,?');i=text.index(r'\int');pos=i+4
 while text[pos].isspace():pos+=1
 assert text[pos]=='_',text;lo,pos=group(text,pos+1);assert text[pos]=='^';hi,pos=group(text,pos+1)
 m=re.search(P.DIFF,text[pos:]);assert m,text;body=text[pos:pos+m.start()].strip();body=body[:-len(r'\cdot')]if body.endswith(r'\cdot')else body
 coefficient=s.Integer(-1)if text[:i].strip()=='-'else scalar(text[:i])if text[:i].strip()else s.Integer(1);F=scalar(body);var=P.P.locals_[m[1]];return coefficient,F,var,scalar(lo),scalar(hi),text[pos+m.end():]
def value(raw):
 text=clean(raw)
 if r'\int'in text:
  c,F,var,lo,hi,end=integral(text);assert not end,end;prim=primitive(F,var);return c*(prim.subs(var,hi)-prim.subs(var,lo)),('integral',c*F,var,lo,hi)
 m=re.search(r'\|_',text)
 if m:
  before=text[:m.start()];after=text[m.end():];lo,pos=group(after,0);assert after[pos]=='^';hi,pos=group(after,pos+1);suffix=after[pos:].strip();assert re.fullmatch(r'\)*',suffix),suffix
  before+=suffix
  # Normalize the source's extra MathML grouping brace around a bar.
  before+='}'*(before.count('{')-before.count('}'))
  prim=scalar(before);lo,hi=scalar(lo),scalar(hi);assert prim.has(u)
  return prim.subs(u,hi)-prim.subs(u,lo),('bar',prim,lo,hi)
 return scalar(text),('value',)
def endpoint_terms(raw):
 text=clean(raw).strip().rstrip('.,');pairs=[];stack=[]
 for i,c in enumerate(text):
  if c=='(':stack.append(i)
  elif c==')':
   start=stack.pop();pairs.append((start,i))
 # Include the entire stage, then every enclosing arithmetic group. A
 # difference's outside coefficient multiplies each endpoint separately.
 for start,end in [(-1,len(text))]+sorted(pairs,key=lambda z:z[0]):
  body=text[start+1:end];depth=0
  for i,c in enumerate(body):
   if c=='-' and depth==0 and i>0 and body[i-1]not in '^*/+-':
    prefix=text[:start]if start>=0 else'';suffix=text[end+1:]if end<len(text)else''
    # Only a whole arithmetic group with scalar outside factors is eligible.
    try:
     outside=text[:start]+'(1)'+text[end+1:]if start>=0 else'1';co=scalar(outside)
     return co*scalar(body[:i]),co*scalar(body[i+1:])
    except (AssertionError,ValueError,IndexError):pass
   depth+=(c in '({')-(c in ')}')
 return None

def blocks(text):return [next(t for t in pair if t)for pair in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',text,re.S)]
def stages(q):
 prompt=q[':question/problem'];sol=q[':question/worked-solution'];given=next(b for b in blocks(prompt)if r'\int'in b).rstrip('= .?(');c,F,var,lo,hi,end=integral(given);assert var==x and not end,(given,end)
 U=scalar(re.search(r'\$u\s*=([^$]+)\$',sol)[1].rstrip('.'));du=s.diff(U,x)
 # Log arguments and sqrt/pole restrictions on the actual definite interval.
 assert lo.is_positive and hi.is_positive
 for L in U.atoms(s.log):
  for bound in (lo,hi):assert s.simplify(L.args[0].subs(x,bound)).is_positive
 ul=s.simplify(U.subs(x,lo));uh=s.simplify(U.subs(x,hi));assert ul.is_nonnegative and uh.is_nonnegative
 derivative_block=next(b for b in blocks(sol)if '⟹'in b or r'\Longrightarrow'in b);a,b=re.split(r'⟹|\\quad\\Longrightarrow\\quad',derivative_block,maxsplit=1)
 assert clean(a.split('=',1)[0])==r'\frac{\mathrm{d}u}{\mathrm{d}x}'
 for part in a.split('=')[1:]:assert equal(scalar(part),du),('false displayed derivative',part,du)
 a,b=b.split('=');a=clean(P.fraction_measure(a));b=clean(P.fraction_measure(b));l=re.fullmatch(r'(.*?)'+P.DIFF,a.strip());r=re.fullmatch(r'(.*?)'+P.DIFF+r'[.]?',b.strip());assert l and r and l[2]=='u'and r[2]=='x',(a,b)
 co=lambda z:scalar(re.sub(r'\\cdot\s*$','',z).strip())if re.sub(r'\\cdot\s*$','',clean(z)).strip()else s.Integer(1)
 assert equal(co(l[1])*du,co(r[1])),('false reciprocal differential',a,b)
 table=re.findall(r'^\| \$([xu])\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',sol,re.M);assert [z[0]for z in table]==['x','u'],table
 xl,xh=map(scalar,table[0][1:]);tl,th=map(scalar,table[1][1:]);assert equal(xl,lo)and equal(xh,hi)and equal(tl,ul)and equal(th,uh),('false table',table)
 prim=primitive(c*F,x);improper_limits=0
 def at(z):
  nonlocal improper_limits
  val=prim.subs(x,z)
  if val.has(s.nan,s.zoo,s.oo,-s.oo)or(c*F).subs(x,z).has(s.nan,s.zoo,s.oo,-s.oo):
   improper_limits+=1;val=s.limit(prim,x,z,dir='+'if z==min(lo,hi)else'-')
  assert not val.has(s.nan,s.zoo,s.oo,-s.oo),('divergent endpoint',z,prim)
  return val
 expected=s.simplify(at(hi)-at(lo));N=dict(rows=0,integral_inputs=0,primitive_bars=0,individual_endpoints=0,bound_references=4,differentials=2,improper_endpoint_limits=improper_limits);last_primitive=None
 aligned=next(b for b in blocks(sol)if r'\begin{aligned}'in b);aligned=re.sub(r'\\(?:begin|end)\{aligned\}','',aligned).replace('&','')
 for row in aligned.split(r'\\'):
  for part in row.split('='):
   if not part.strip():continue
   v,info=value(part);assert equal(v,expected),('wrong definite row',part,v,expected)
   if info[0]=='integral':
    _,body,ivar,bl,bh=info;assert ivar in(x,u);assert equal(bl,lo if ivar==x else ul)and equal(bh,hi if ivar==x else uh),('wrong displayed integral bounds',part)
    assert equal(body if ivar==x else body.subs(u,U)*du,c*F),('wrong displayed integral operand',part,body,c*F)
    N['integral_inputs']+=1;N['bound_references']+=2
   elif info[0]=='bar':
    _,pr,bl,bh=info;assert equal(bl,ul)and equal(bh,uh)and equal(P.derivative(pr,u).subs(u,U)*du,c*F),('wrong primitive despite endpoint result',part)
    last_primitive=pr;N['primitive_bars']+=1;N['bound_references']+=2
   elif (terms:=endpoint_terms(part))and last_primitive is not None:
    assert equal(terms[0],last_primitive.subs(u,uh))and equal(terms[1],last_primitive.subs(u,ul)),('compensating endpoint error',part,terms,last_primitive)
    N['individual_endpoints']+=2
   elif last_primitive is not None and equal(last_primitive.subs(u,ul),s.Integer(0)):
    assert equal(v,last_primitive.subs(u,uh));N['individual_endpoints']+=1
   N['rows']+=1
 assert N['primitive_bars']>=1 and N['individual_endpoints']>=1,N
 return expected,N
