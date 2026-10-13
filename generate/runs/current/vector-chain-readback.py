"""Root reads actual two/three-coordinate chain operators, vectors and dot products."""
import importlib.util,re,functools
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;sp=importlib.util.spec_from_file_location('root_multichain_scalar',P/'ode-scalar-parser.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
x,y,z,t=p.x,p.y,p.z,p.t

def clean(raw):
 raw=raw.strip().rstrip('.,:').replace('⁡','').replace('\\u2061','').replace(r'\left','').replace(r'\right','').replace(r'\,','')
 raw=re.sub(r'\\text\{[\s\u00a0]*\}', '',raw)
 return raw

@functools.lru_cache(maxsize=10000)
def scalar(raw):
 raw=clean(raw).replace('[','(').replace(']',')').replace(r'\operatorname{atan}',r'\operatorname{arctan}')
 # A bare trigonometric numeric argument includes the next parenthesized
 # factor: sin2(t+1) means sin(2(t+1)), not sin(2)*(t+1).
 pat=r'(\\operatorname\{(?:sin|cos|tan|sec|cot|csc)\}|\\(?:sin|cos|tan|sec|cot|csc)|\{(?:sin|cos|tan|sec|cot|csc)\})(\^\{?-?\d+\}?)?\s*([+-]?\d+|\\pi)\s*\('
 pos=0
 while True:
  m=re.search(pat,raw[pos:])
  if not m:break
  start=pos+m.start();openat=pos+m.end()-1;end=openat+1;depth=1
  while depth:
   depth+=(raw[end]=='(')-(raw[end]==')');end+=1
  replacement=m[1]+(m[2] or '')+'('+m[3]+raw[openat:end]+')';raw=raw[:start]+replacement+raw[end:];pos=start+len(replacement)
 return p.scalar(raw)
def formula(raw):
 raw=clean(raw)
 # Source bare inverse-tangent/log arguments consume the complete product xy.
 m=re.fullmatch(r'(?:\\operatorname\{(arctan|ln)\}|\\(arctan|ln))\s*(x\s*y)',raw)
 if m:raw='\\'+(m[1] or m[2])+'('+m[3]+')'
 return scalar(raw)
def vector(raw):
 raw=clean(raw)
 if raw.startswith('⟨') and raw.endswith('⟩'):
  body=raw[1:-1].replace(r'\,','');parts=[];start=0;depth=0
  for i,c in enumerate(body):
   depth+=(c in '([{')-(c in ')]}')
   if c==',' and depth==0:parts.append(body[start:i]);start=i+1
  parts.append(body[start:]);assert len(parts) in (2,3)
  return s.Matrix([scalar(a) for a in parts]+([0] if len(parts)==2 else []))
 value=s.expand(scalar(raw));v=s.Matrix([value.coeff(b) for b in (p.i,p.j,p.k)]);assert s.expand(value-sum(a*b for a,b in zip(v,(p.i,p.j,p.k))))==0;return v

@functools.lru_cache(maxsize=1000)
def given(prompt):
 spans=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',prompt,re.S);functions=[];curves=[]
 for span in spans:
  if re.match(r'[fgh]\(\s*x\s*,\s*y(?:\s*,\s*z)?\s*\)\s*=',span):functions.append((span[0],formula(span.split('=',1)[1])))
  if re.match(r'[rpq]\(t\)\s*=',span):curves.append((span[0],vector(span.split('=',1)[1])))
 assert len(functions)==len(curves)==1
 name,F=functions[0];curve_name,R=curves[0];G=s.Matrix([s.diff(F,v) for v in (x,y,z)]);sub=dict(zip((x,y,z),R));composed=G.subs(sub,simultaneous=True);derivative=R.diff(t);answer=composed.dot(derivative)
 return dict(name=name,curve_name=curve_name,F=F,R=R,G=G,composed=composed,derivative=derivative,answer=answer)
def equal(a,b):
 if isinstance(a,s.MatrixBase) or isinstance(b,s.MatrixBase):return isinstance(a,s.MatrixBase) and isinstance(b,s.MatrixBase) and a.shape==b.shape and all(equal(u,v) for u,v in zip(a,b))
 return scalar_equal(a,b)

@functools.lru_cache(maxsize=40000)
def scalar_equal(a,b):
 # Combine exponentials before trig expansion so sin(theta)^2+cos(theta)^2
 # inside an exponent retains its elementary unit-circle identity.
 def exponents(value):
  value=s.powsimp(value,deep=True,combine='exp')
  return value.xreplace({q:s.exp(s.trigsimp(q.args[0])) for q in value.atoms(s.exp)})
 a,b=exponents(a),exponents(b)
 d=s.expand(a-b)
 if d==0 or s.cancel(d)==0:return True
 # Exact elementary identities; formal rational normal form in the observed
 # exponential/logarithm/trig basis avoids repeated general CAS searches.
 d=s.expand_trig(d);E=s.Symbol('root_exp',positive=True)
 d=d.xreplace({e:E**s.simplify(e.args[0]/t) for e in d.atoms(s.exp) if s.simplify(e.args[0]/t).is_Integer})
 trig=d.atoms(s.sin,s.cos,s.tan,s.sec,s.cot,s.csc);angles=sorted({e.args[0] for e in trig},key=str);pairs={v:(s.Symbol('root_sin'+str(i)),s.Symbol('root_cos'+str(i))) for i,v in enumerate(angles)}
 mp={}
 for e in trig:
  sn,cs=pairs[e.args[0]];mp[e]={s.sin:sn,s.cos:cs,s.tan:sn/cs,s.sec:1/cs,s.cot:cs/sn,s.csc:1/sn}[e.func]
 d=d.xreplace(mp);num=s.fraction(s.cancel(d))[0]
 for sn,cs in pairs.values():
  if num.has(cs):
   try:num=s.rem(num,cs**2+sn**2-1,cs)
   except s.PolynomialError:return s.simplify(s.trigsimp(a-b))==0
 if num==0:return True
 # Unequal rational functions of one shared angle have a nonzero normal form;
 # multiple-angle identities have already been expanded above.
 if len(angles)<=1 and not num.has(s.sin,s.cos,s.exp):return False
 return s.simplify(s.trigsimp(a-b))==0

def formal(raw,d):
 raw=clean(raw)
 # Evaluate each actual formal derivative's argument, never a metadata operand.
 patterns=(r'\frac{∂}{∂x}',r'\frac{∂}{∂y}',r'\frac{∂}{∂z}',r'\frac{\text{d}}{\text{d}t}')
 variables=(x,y,z,t)
 for prefix,var in zip(patterns,variables):
  while prefix in raw:
   at=raw.index(prefix);start=at+len(prefix)
   while start<len(raw) and raw[start].isspace():start+=1
   if raw[start] in '([':openat=start;inner=True
   else:
    head=re.match(r'(?:\\operatorname\{(?:ln|log|sin|cos|arctan)\}|\\(?:ln|log|sin|cos|arctan))\s*\(',raw[start:]);assert head is not None,('Ungrouped formal derivative',raw)
    openat=start+head.end()-1;inner=False
   end=openat+1;depth=1
   while depth:
    if raw[end]==raw[openat]:depth+=1
    elif raw[end]==(')' if raw[openat]=='(' else ']'):depth-=1
    end+=1
   value=s.diff(formula(raw[start+1:end-1] if inner else raw[start:end]),var);raw=raw[:at]+'('+s.latex(value)+')'+raw[end:]
 return raw

def topdot(raw):
 depth=0
 for i,c in enumerate(raw):
  if c in '([{⟨':depth+=1
  if c in ')]}⟩':depth-=1
  if raw.startswith(r'\cdot',i) and depth==0:return raw[:i],raw[i+5:]
 return None

def expression(raw,d):
 raw=clean(raw);name,cn=d['name'],d['curve_name']
 if r'\Big|_{' in raw:
  head,tail=raw.rsplit(r'\Big|_{',1);assert tail.endswith('}')
  substitutions={}
  for item in tail[:-1].split(','):
   key,value=item.split('=',1);key=key.strip();assert key in ('x','y','z','t');var=(x,y,z,t)[('x','y','z','t').index(key)];substitutions[var]=scalar(value)
   if key in ('x','y','z'):assert equal(substitutions[var],d['R'][('x','y','z').index(key)])
   elif 'point' in d:assert equal(substitutions[var],d['point'])
  return expression(head,d).subs(substitutions,simultaneous=True)
 # Actual identities use reference quantities derived from the printed givens.
 if raw=='∇'+name+'(x,y)' or raw=='∇'+name+'(x,y,z)':return d['G']
 if raw=='∇'+name+'('+cn+'(t))':return d['composed']
 if raw in ('{'+cn+'}^{′}(t)',cn+'^{′}(t)'):return d['derivative']
 if raw==r'\frac{\text{d}}{\text{d}t}['+name+'('+cn+'(t))]':return d['answer']
 prefix=r'\frac{\text{d}}{\text{d}t}['+name+'('+cn+'('
 if raw.startswith(prefix) and raw.endswith('))]'):return d['answer'].subs(t,scalar(raw[len(prefix):-3]))
 pair=topdot(raw)
 if pair and ((raw.startswith('∇') or raw.startswith(('(','⟨'))) and pair[1].strip().startswith(('(','⟨','{'+cn))):
  a,b=[expression(v,d) for v in pair]
  if isinstance(a,s.MatrixBase) or isinstance(b,s.MatrixBase):assert isinstance(a,s.MatrixBase) and isinstance(b,s.MatrixBase);return a.dot(b)
 raw=formal(raw,d)
 if raw.startswith('⟨'):return vector(raw)
 if raw.startswith('(') and raw.endswith(')'):
  # Remove one outer pair only if it encloses the complete expression.
  dep=0;whole=True
  for i,c in enumerate(raw):
   dep+=(c=='(')-(c==')')
   if dep==0 and i<len(raw)-1:whole=False;break
  if whole:return expression(raw[1:-1],d)
 value=scalar(raw)
 if value.has(p.i,p.j,p.k):return vector(raw)
 return value

def solution(sol,d):
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);counts=dict(blocks=len(blocks),equalities=0,formal_rows=0,prose_substitutions=0)
 for inline in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',sol,re.S):
  for component in inline.split(','):
   if '=' in component:
    a,b=component.split('=',1)
    if a.strip() in ('x','y','z'):
     assert equal(scalar(b),d['R'][('x','y','z').index(a.strip())]);counts['prose_substitutions']+=1
 for block in blocks:
  raw=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','');previous=None
  for row in raw.split(r'\\'):
   body=row.strip().rstrip('.,');sides=[];start=0;depth=0
   for at,c in enumerate(body):
    depth+=(c=='{')-(c=='}')
    if c=='=' and depth==0:sides.append(body[start:at]);start=at+1
   sides.append(body[start:]);assert len(sides)>=2
   vals=[]
   for i,side in enumerate(sides):
    if not side.strip():assert i==0 and previous is not None;v=previous
    else:v=expression(side,d)
    vals.append(v)
   assert all(equal(v,vals[0]) for v in vals[1:]),('False actual derivative/gradient/dot stage',row,vals)
   previous=vals[-1];counts['equalities']+=len(vals)-1
   if any(a in row for a in (r'\frac{∂}',r'\frac{\text{d}}{\text{d}t}(')):counts['formal_rows']+=1
 return counts
