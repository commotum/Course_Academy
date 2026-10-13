"""Root's strict displayed formula/first-order coordinate chain rule reader."""
import importlib.util,re,functools
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('parent_polar_scalar',Path(__file__).with_name('vector-math-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
x,y,z,R,T=p.x,p.y,p.z,p.u,p.v
MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$',re.S)
def blocks(text):return [(v[2:-2] if v.startswith('$$') else v[1:-1]).strip().rstrip('.,') for v in MATH.findall(text)]
def scalar(raw):
 raw=raw.replace('\\\\','\\').replace(r'\u2061','').replace('θ',r'\theta').replace(r'\theta','v').replace(r'\partial','∂')
 # Token-based replacement of bare radial r, while protecting TeX commands.
 raw=re.sub(r'\\[A-Za-z]+|r',lambda m: 'u' if m[0]=='r' else m[0],raw)
 return p.scalar(raw)
@functools.lru_cache(maxsize=8192)
def equal(a,b):
 if a==b:return True
 # Exact reduction in the sin/cos identity ideal avoids repeated expensive
 # heuristic trig simplification of coupled rational chain-rule expressions.
 delta=s.expand_trig(a-b);A,B=s.symbols('parent_sine parent_cosine')
 rational=delta.xreplace({s.sin(T):A,s.cos(T):B})
 if not rational.has(s.sin,s.cos,s.log):
  num=s.together(rational).as_numer_denom()[0]
  try:return s.rem(s.Poly(num,B),s.Poly(B**2+A**2-1,B)).is_zero
  except s.PolynomialError:pass
 return s.simplify(s.trigsimp(delta))==0

def question(text,direction):
 bs=blocks(text);pattern=r'^([fghwvu])\(\s*'+('x,y,z' if direction=='cylindrical' else 'x,y' if direction=='forward' else r'r,(?:\\theta|θ)')+r'\s*\)\s*=';formula=[]
 for b in bs:
  compact=b.replace(' ','');m=re.match(pattern,compact)
  if m:formula.append((m[1],scalar(b.split('=',1)[1])))
 assert len(formula)==1,(text,formula);name,F=formula[0]
 derivative=next(b for b in bs if '∂'+name in b or r'\partial '+name in b);derivative=re.sub(r'\\partial\s*','∂',derivative);axis='theta' if r'\theta' in derivative or 'θ' in derivative else 'r' if '∂r' in derivative else 'z' if '∂z' in derivative else 'x' if '∂x' in derivative else 'y';assert axis in (('r','theta','z') if direction=='cylindrical' else ('r','theta') if direction=='forward' else ('x','y'))
 if direction in ('forward','cylindrical'):
  fr=s.diff(F,x);ft=s.diff(F,y);sub={x:R*s.cos(T),y:R*s.sin(T)};a=fr.subs(sub,simultaneous=True);b=ft.subs(sub,simultaneous=True);value=a*s.cos(T)+b*s.sin(T) if axis=='r' else -a*R*s.sin(T)+b*R*s.cos(T)
 else:
  a=s.diff(F,R);b=s.diff(F,T);fr=a;ft=b;value=a*s.cos(T)-b/R*s.sin(T) if axis=='x' else a*s.sin(T)+b/R*s.cos(T)
 if direction=='cylindrical':
  fz=s.diff(F,z);cz=fz.subs({x:R*s.cos(T),y:R*s.sin(T)},simultaneous=True)
  if axis=='z':value=cz
  return name,F,axis,fr,ft,s.trigsimp(value),(a,b,cz)
 return name,F,axis,fr,ft,s.trigsimp(value),(a,b)

def clean(raw):return raw.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').strip().rstrip('.,')
def stages(text,details,direction,sequence=False):
 name,F,axis,fr,ft,answer,converted=details;counts={'printed_equalities':0,'basis_definitions':0};ordered=[]
 def expression(raw,polar):
  def replacement(m):
   fn,variable=m[1],m[2];variable='theta' if variable in (r'\theta','θ') else variable
   if fn==name:
    if direction=='cylindrical' and variable=='z':v=converted[2] if polar else s.diff(F,z)
    elif variable==axis:v=answer
    elif direction in ('forward','cylindrical') and variable in ('x','y'):v=(converted if polar else (fr,ft))[0 if variable=='x' else 1]
    elif direction=='inverse' and variable in ('r','theta'):v=(fr,ft)[0 if variable=='r' else 1]
    else:raise AssertionError(('Unexpected partial',m[0],name,axis,direction))
   elif direction in ('forward','cylindrical') and fn in ('x','y','z') and variable in ('r','theta','z'):
    v={('x','r'):s.cos(T),('y','r'):s.sin(T),('x','theta'):-R*s.sin(T),('y','theta'):R*s.cos(T),('x','z'):s.S.Zero,('y','z'):s.S.Zero,('z','r'):s.S.Zero,('z','theta'):s.S.Zero,('z','z'):s.S.One}[(fn,variable)]
   else:raise AssertionError(('Wrong function derivative label',m[0],name))
   return '('+s.latex(v)+')'
  raw=re.sub(r'\\frac\{(?:∂|\\partial\s*)([a-z])\}\{(?:∂|\\partial\s*)(\\theta|θ|[xyrz])\s*\}',replacement,raw)
  return scalar(raw)
 for block in blocks(text):
  block=clean(block)
  if block.startswith(('x=','y=','z=')):
   for component in block.split(','):
    fn,rhs=component.split('=',1);fn=fn.strip();assert fn in ('x','y','z');assert equal(scalar(rhs),z if fn=='z' else R*(s.cos(T) if fn=='x' else s.sin(T)));counts['basis_definitions']+=1
  if r'\frac{∂' not in block and r'\frac{\partial' not in block:continue
  rows=block.split(r'\\');previous=None
  for row in rows:
   for segment in row.replace(r'\,','').split(','):
    if '=' not in segment:continue
    lhs,rhs=segment.split('=',1);lhs=lhs.strip() or previous;assert lhs is not None;previous=lhs
    polar=(r'\theta' in rhs or 'θ' in rhs or re.search(r'(?<![A-Za-z])r(?![A-Za-z])',rhs) is not None or '∂r' in rhs)
    a,b=expression(lhs,polar),expression(rhs,polar);assert equal(a,b),(segment,a,b);counts['printed_equalities']+=1;ordered.append((a,b))
 assert counts['printed_equalities']>=4,counts
 return (counts,ordered) if sequence else counts
