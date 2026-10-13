"""Parent extracts the polynomial times a positive exponential from printed TeX."""
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('parent_exp_scalar',Path(__file__).with_name('vector-math-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
x=p.x
MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$',re.S)
def blocks(text):return [m[0][2:-2] if m[0].startswith('$$') else m[0][1:-1] for m in MATH.finditer(text)]
def math(raw):return p.scalar(raw.strip().rstrip('.,?').replace(r'\displaystyle',''))
def read(text):
 body=next(z for z in blocks(text) if '=' in z and '{{' not in z and 'x' in z and not z.strip().startswith('x='))
 a,b=body.split('=',1);expression=math(a)-math(b);terms=s.Add.make_args(expression);factors=[]
 for term in terms:
  expo=[v for v in s.Mul.make_args(term) if (isinstance(v,s.Pow) and x in v.exp.free_symbols and not v.base.free_symbols) or (v.func==s.exp and x in v.args[0].free_symbols)]
  assert len(expo)==1,(body,term,expo);factor=expo[0];assert factor.is_positive and ((factor.func==s.exp and factor.args[0].is_real) or (isinstance(factor,s.Pow) and factor.base!=1 and factor.exp.is_real)),(body,factor)
  factors.append(factor)
 assert all(s.simplify(v/factors[0])==1 for v in factors),body
 exponential=factors[0];polynomial=s.expand(sum(term/factor for term,factor in zip(terms,factors)));P=s.Poly(polynomial,x);assert P.degree()==2
 roots=tuple(sorted(s.solve(polynomial,x),key=lambda z:float(z)));assert len(roots)==2 and all(z.is_real for z in roots),body
 return expression,exponential,polynomial,roots

def equal(a,b):return s.simplify(a-b)==0

def stages(text,expression,exponential,polynomial,roots):
 counts=dict(factor_equations=0,solution_roots=0,positive_exponential_claims=0,product_claims=0)
 # Every displayed full equation in a factoring group retains either the
 # original exponential equation or the independently extracted quadratic.
 for b in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S):
  for row in re.split(r'\\\\',b):
   a,rhs=row.replace('&','').split('=',1)
   val=math(a)-math(rhs);assert equal(val,expression) or equal(val,polynomial),(row,val,expression,polynomial);counts['factor_equations']+=1
 for raw in blocks(text):
  if 'aligned' in raw:continue
  # Source standalone factored quadratics and the zero-product pair.
  if '=0' in raw.replace(' ','') and not raw.strip().startswith(('ab','a=','b=')):
   for piece in re.split(r'\\text\{and\}',raw):
    piece=piece.strip().replace(r'\,','');a,b=piece.split('=',1);val=math(a);assert math(b)==0
    assert equal(val,polynomial) or equal(val,exponential) or val==s.Poly(polynomial,x).LC(),(raw,val)
    counts['factor_equations']+=1
  if re.match(r'x\s*=',raw.strip()):
   content=raw.split('=',1)[1]
   if r'\text{and}' in content:
    values=[math(z.replace('x=','').replace('x =','').replace(r'\,','')) for z in re.split(r'\\text\{and\}',content)]
   else:values=[math(re.sub(r'^\s*x\s*=','',z)) for z in content.strip().rstrip('.,?').split(',') if z.strip()]
   assert values and all(v in roots for v in values),(raw,values,roots);counts['solution_roots']+=len(values)
  if r'\cdot' in raw and '=' in raw and 'x' not in raw:
   a,b=raw.split('=',1);assert equal(math(a),roots[0]*roots[1]) and equal(math(b),roots[0]*roots[1]);counts['product_claims']+=1
 for raw in re.findall(r'\$([^$]*?)\$ is positive for every real number',text):
  assert equal(math(raw),exponential);counts['positive_exponential_claims']+=1
 assert counts['positive_exponential_claims']==1,text
 return counts
