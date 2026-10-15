"""Root strict readback for actual separable ODEs and complete solution families."""
import importlib.util,re,functools
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('root_ode_elementary',Path(__file__).with_name('ode-scalar-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
x,y,D,C,K=p.x,p.y,p.z,p.u,p.v
MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$',re.S)
def blocks(text):return [v[2:-2] if v.startswith('$$') else v[1:-1] for v in MATH.findall(text)]
def scalar(raw):
 raw=raw.strip().rstrip('.,:').replace(r'\left','').replace(r'\right','').replace(r'\!','').replace(r'\displaystyle','')
 raw=re.sub(r'\\(?:mathrm|text)\{d\}', 'd',raw)
 raw=re.sub(r'\\text\{\s*\}', '',raw)
 raw=raw.replace(r'\frac{dy}{dx}','z').replace(r'\frac{dT}{dt}','z')
 raw=re.sub(r'\{?y\}?\s*\^?\{?[′\u2032]\}?','z',raw).replace("y'",'z').replace('T','y')
 while r'\sqrt[' in raw:
  m=re.search(r'\\sqrt\[(\d+)\]\{',raw);assert m,raw
  start=m.end();pos=start;depth=1
  while depth:depth+=(raw[pos]=='{')-(raw[pos]=='}');pos+=1
  body=scalar(raw[start:pos-1]);root=body**s.Rational(1,int(m[1]));slot=next(a for a in ('i','j','k') if a not in re.sub(r'\\[A-Za-z]+','',raw));raw=raw[:m.start()]+'('+slot+')'+raw[pos:];return scalar(raw).subs(p.locals_[slot],root)
 if '|' in raw:
  a=raw.index('|');b=raw.index('|',a+1);body=scalar(raw[a+1:b]);slot=next(a for a in ('i','j','k') if a not in re.sub(r'\\[A-Za-z]+','',raw));return scalar(raw[:a]+'('+slot+')'+raw[b+1:]).subs(p.locals_[slot],s.Abs(body))
 raw=raw.replace('C','u').replace('K','v')
 return p.scalar(raw).subs(p.t,x)
def equation(raw):
 lhs,rhs=raw.replace('&','').strip().rstrip('.,').split('=');return scalar(lhs)-scalar(rhs)
def ode(text):
 raw=next(row for b in blocks(text) for row in clean(b).split(r'\\') if '=' in row and any(marker in row for marker in ('′',"y'",r'\frac{\text{d}y}',r'\frac{\mathrm{d}y}',r'\frac{dy}',r'\frac{\text{d}T}',r'\frac{\mathrm{d}T}',r'\frac{dT}')))
 eq=equation(raw);roots=s.solve(eq,D);assert len(roots)==1 and not roots[0].has(D);return roots[0]
def solution(raw):
 raw=raw.strip().rstrip('.,');lhs,rhs=raw.split('=',1);assert lhs.strip() in ('y','T')
 signs=(1,-1) if r'\pm' in rhs else (1,);rhs=rhs.replace(r'\pm','');return tuple(sign*scalar(rhs) for sign in signs)
def real_y_powers(F):
 return F.xreplace({node:(s.sign(y)**int(node.exp.p))*s.Abs(y)**node.exp for node in s.preorder_traversal(F) if isinstance(node,s.Pow) and node.base==y and node.exp.is_Rational and node.exp.q>1 and node.exp.q%2==1})
@functools.lru_cache(maxsize=8192)
def equal(a,b):
 difference=real_y_powers(a-b)
 if s.simplify(s.trigsimp(difference))==0:return True
 if s.trigsimp(difference,method='fu')==0:return True
 if not difference.has(y):return False
 # Separating by y removes y=0. Check both real sign components explicitly.
 positive=s.Symbol('_root_nonzero_y',positive=True)
 return all(s.simplify(s.trigsimp(difference.subs(y,sign*positive)))==0 for sign in (1,-1))
def on_positive_components(expr,conditions):
 mapping={}
 for index,condition in enumerate(conditions):
  pos=s.Symbol('_verified_positive_component_'+str(index),positive=True)
  condition=condition.subs(mapping)
  # Derivatives have already been taken with constants held fixed. This is
  # an invertible pointwise coordinate change on the declared positive set,
  # not differentiation with a variable integration constant.
  for var in (C,K,y,x):
   coef=s.diff(condition,var)
   if coef!=0 and not coef.has(var) and s.diff(condition,var,2)==0:
    replacement=s.simplify((pos-condition.subs(var,0))/coef);expr=s.simplify(expr.subs(var,replacement));mapping[var]=replacement;break
  else:expr=s.simplify(expr.subs(condition,pos))
 return expr
def positive_conditions(text):
 return tuple(scalar(raw.rsplit('>',1)[0].strip()) for raw in blocks(text) if raw.strip().rstrip('.,').endswith('>0') and raw.count('>')==1 and '=' not in raw and r'\quad' not in raw)
@functools.lru_cache(maxsize=4096)
def local_valid(F,rhs,conditions=()):
 if F.has(y):return False
 # Implicit differentiation of a root's defining power avoids incorrect
 # global complex-branch simplification for real odd roots.
 if isinstance(F,s.Pow) and F.exp.q>1 and F.exp.p==1:
  n=int(F.exp.q);G=F.base;return equal(on_positive_components(n*F**(n-1)*rhs.subs(y,F)-s.diff(G,x),conditions),s.Integer(0))
 return equal(on_positive_components(s.diff(F,x)-rhs.subs(y,F),conditions),s.Integer(0))
def full_family(F,rhs,conditions=()):return (F.has(C,K) and (s.diff(F,C)!=0 or s.diff(F,K)!=0) and local_valid(F,rhs,conditions))
def family_equal(a,b):
 # Canonicalize either spelling of the arbitrary constant, then recognize
 # invertible outer functions and affine nonzero reparameterizations.
 a=a.subs(K,C);b=b.subs(K,C)
 if equal(a,b):return True
 if a.func==b.func and a.func in (s.log,s.tan):return family_equal(a.args[0],b.args[0])
 if isinstance(a,s.Pow) and isinstance(b,s.Pow) and a.exp==b.exp:return family_equal(a.base,b.base)
 da,db=s.diff(a,C),s.diff(b,C)
 if da!=0 and db!=0 and s.diff(a,C,2)==s.diff(b,C,2)==0:
  ratio=s.simplify(da/db);shift=s.simplify((a.subs(C,0)-b.subs(C,0))/db);return ratio!=0 and not ratio.has(x,C) and not shift.has(x,C)
 return False
def derivative(F,var):
 # The source explicitly separates on nonzero y (or y-offset) intervals.
 # d ln|f| = f'/f there, with no sign restriction on f.
 logs={node:s.log(node.args[0].args[0]) for node in s.preorder_traversal(F) if node.func==s.log and node.args[0].func==s.Abs}
 return s.diff(F.xreplace(logs),var)
def clean(raw):
 raw=re.sub(r'\\(?:begin|end)\{aligned\}', '',raw).replace('&','').strip().rstrip('.,')
 raw=re.sub(r'\\cancel\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}',r'\1',raw)
 return raw
def integral_side(raw):
 raw=raw.replace(r'\text{d}', 'd').replace(r'\mathrm{d}','d').replace(r'\,','').replace(r'\cdot','*').strip()
 if raw.count(r'\int')>1:
  terms=[integral_side(v) for v in re.split(r'(?=[+-]\s*\\int)',raw) if v.strip()];assert len(terms)==raw.count(r'\int') and len({v for _,v in terms})==1,raw
  return sum(a for a,_ in terms),terms[0][1]
 start=raw.index(r'\int');prefix=raw[:start].strip().rstrip('*');factor=s.Integer(-1 if prefix=='-' else 1) if prefix in ('','+','-') else scalar(prefix);body=raw[start+4:].strip()
 match=re.search(r'd([xyTt])\s*$',body)
 if match:
  var=x if match[1] in ('x','t') else y;body=body[:match.start()].strip().rstrip('*');body=body or '1'
 else:
  match=re.search(r'd([yT])',body);assert match,raw;var=y;body=body[:match.start()]+'1'+body[match.end():]
 return factor*scalar(body),var
def stages(text,rhs,conditions=()):
 counts={'ode_rows':0,'integral_rows':0,'primitive_rows':0,'explicit_family_rows':0}
 affine_constant=None
 for block in blocks(text):
  for row in clean(block).split(r'\\'):
   if '=' in row and row.split('=',1)[0].strip()=='K':
    value=scalar(row.split('=',1)[1]);coef=s.diff(value,C)
    if coef!=0 and not coef.has(C,x,y,K) and s.diff(value,C,2)==0 and not value.has(x,y,K):affine_constant=value
 def candidate_conditions(F):
  if affine_constant is None:return conditions
  if F.has(C) and not F.has(K):return tuple(v.subs(K,affine_constant) for v in conditions)
  if F.has(K) and not F.has(C):
   coefficient=s.diff(affine_constant,C);constant=affine_constant.subs(C,0);return tuple(v.subs(C,(K-constant)/coefficient) for v in conditions)
  return conditions
 for block in blocks(text):
  previous_lhs=None
  for raw in clean(block).split(r'\\'):
   raw=raw.strip().rstrip('.,');
   if '=' not in raw:continue
   lhs,right=raw.split('=',1)
   if not lhs.strip():assert previous_lhs is not None;lhs=previous_lhs;raw=lhs+'='+right
   else:previous_lhs=lhs
   if any(label in raw for label in ('h(x)','g(y)','y(x)','T(t)')):continue
   if r'\int' in raw:
    assert r'\int' in lhs and r'\int' in right,(raw,'unpaired integral')
    A,a=integral_side(lhs);B,b=integral_side(right)
    if a==x and A.has(D):A=A.subs(D,rhs)
    elif a==y:A=A*rhs
    if b==x and B.has(D):B=B.subs(D,rhs)
    elif b==y:B=B*rhs
    assert equal(on_positive_components(A-B,conditions),s.Integer(0)),(raw,A,B);counts['integral_rows']+=1
   elif any(marker in raw for marker in ('′',"y'",r'\frac{\text{d}y}',r'\frac{\mathrm{d}y}',r'\frac{dy}',r'\frac{\text{d}T}',r'\frac{\mathrm{d}T}')):
    roots=s.solve(equation(raw),D);assert len(roots)==1 and equal(on_positive_components(roots[0]-rhs,conditions),s.Integer(0)),(raw,roots,rhs);counts['ode_rows']+=1
   elif lhs.strip() in ('y','T'):
    for F in solution(raw):assert full_family(F,rhs,candidate_conditions(F)),(raw,rhs,F)
    counts['explicit_family_rows']+=1
   elif (any(letter in lhs for letter in ('y','T')) and not any(letter in right for letter in ('y','T'))) and ('C' in right or 'K' in right or r'\ln' in lhs or 'ln' in lhs):
    A,B=scalar(lhs),scalar(right)
    # Primitive equations before inversion have a y-only left side. After
    # exponentiation, compare derivatives using the printed relation A=B.
    if A.func==s.Abs:
     roots=[s.solve(A.args[0]-sign*B,y) for sign in (1,-1)];assert all(len(v)==1 and full_family(v[0],rhs,conditions) for v in roots),(raw,A,B,rhs)
     counts['explicit_family_rows']+=1;continue
    if s.diff(A,y)!=0 and s.diff(A,y,2)==0:
     roots=s.solve(A-B,y);assert len(roots)==1 and full_family(roots[0],rhs,candidate_conditions(roots[0])),(raw,A,B,rhs)
     counts['explicit_family_rows']+=1;continue
    assert equal(on_positive_components(derivative(A,y)*rhs-derivative(B,x),conditions),s.Integer(0)),(raw,A,B,rhs);counts['primitive_rows']+=1
 return counts
