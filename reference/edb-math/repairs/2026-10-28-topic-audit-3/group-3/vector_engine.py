"""Independent fail-closed mathematical interpreter for audit expressions."""
import re,sys
from pathlib import Path
import sympy as sp
sys.path.insert(0,'scripts')
from question_capture.math_format import MATH,normalize_source_tex,normalize_tex,ENV,environment,cells
from symbolic import parse as scalar_parse,SYMS,Unsupported
X=[SYMS[c]for c in'xyz'];B=[SYMS[c]for c in'ijk']
def maths(text):
 return[m[0][2:-2]if m[0].startswith(('$$',r'\[',r'\('))else m[0][1:-1]for m in MATH.finditer(text)]
def scalar(tex):
 tex=normalize_source_tex(tex).replace(r'\,',' ').replace(r'\;',' ').replace(r'\:',' ').strip().strip('$').strip().rstrip('.,?');tex=re.sub(r'(?<![A-Za-z])\{(sin|cos|tan|sec|csc|cot|ln|log)\}',lambda m:'\\'+m[1]+' ',tex);tex=tex.replace('π',r'\pi ').replace('θ',' T').replace(r'\theta',' T').replace('∗',r'\cdot ').replace('⋅',r'\cdot ')
 # Mathematical font roles do not alter scalar coefficients in this independent algebraic check.
 for _ in range(4):tex=re.sub(r'\\(?:mathbf|boldsymbol|mathit|mathrm)\s*\{([^{}]*)\}',r'{\1}',tex)
 tex=re.sub(r'\\(?:mathbf|boldsymbol|mathit)\s+([A-Za-z])',r'\1',tex)
 tex=re.sub(r'\\(?:text|textrm)\{[\s\u00a0]*\}','',tex)
 tex=re.sub(r'\\displaystyle|\\limits|\\hspace\{[^{}]*\}','',tex).replace(r'\,',' ').replace(r'\;',' ').replace(r'\:',' ')
 return scalar_parse(tex)
def matrices(tex):
 tex=normalize_tex(tex);out=[]
 for m in ENV.finditer(tex):
  if m[1]!='begin'or m[2]not in['matrix','bmatrix','pmatrix','vmatrix','array']:continue
  env=environment(tex,m.start())
  if not env:raise Unsupported('unbalanced matrix')
  body=tex[env[0]:env[1]]
  if m[2]=='array':body=re.sub(r'^\s*\{[lcr|]+\}','',body)
  grid=cells(body)
  if grid and len({len(r)for r in grid})==1:
   try:out.append({'value':sp.Matrix([[scalar(c)for c in row]for row in grid]),'start':m.start(),'end':env[2],'tex':tex[m.start():env[2]]})
   except Exception:continue
 return out

def split_top(tex,delimiter=','):
 depth=0;start=0;parts=[]
 for i,c in enumerate(tex):
  if c in'{([':depth+=1
  elif c in'})]':depth-=1
  elif c==delimiter and depth==0:parts.append(tex[start:i]);start=i+1
 parts.append(tex[start:]);return parts

def vector(tex):
 tex=normalize_source_tex(tex).strip().strip('$').strip().rstrip('.,?');ms=matrices(tex)
 if len(ms)==1 and ms[0]['value'].cols==1:return ms[0]['value']
 angle=re.search(r'(?:⟨|\\langle)\s*([\s\S]*?)(?:⟩|\\rangle)',tex)
 if angle:
  v=sp.Matrix([scalar(c)for c in split_top(angle[1])]);prefix=tex[:angle.start()].strip();suffix=tex[angle.end():].strip()
  if prefix and'='in prefix:prefix=prefix.rsplit('=',1)[1].strip()
  if prefix:v=scalar(prefix)*v
  if suffix:raise Unsupported('vector has unparsed suffix')
  return v
 if'='in tex:tex=tex.rsplit('=',1)[1]
 e=sp.expand(scalar(tex));coeff=[sp.diff(e,b)for b in B]
 if any(c.has(*B)for c in coeff)or sp.simplify(e-sum(c*b for c,b in zip(coeff,B)))!=0:raise Unsupported('not a linear basis-vector expression')
 if not any(c!=0 for c in coeff):raise Unsupported('zero or scalar ambiguous vector dimension')
 return sp.Matrix(coeff[:3 if coeff[2]!=0 else 2])

def definitions(problem):
 out={}
 for tex in maths(problem):
  tex=re.sub(r'\\(?:begin|end)\{aligned\}','',tex).replace('&','').replace(r'\\',';')
  hits=list(re.finditer(r'(?<![A-Za-z])([fghFGHψφ]|\\psi|\\phi)\s*\(\s*([xyzuvwt](?:\s*,\s*[xyzuvwt]){0,2})\s*\)\s*=\s*',tex))
  for i,m in enumerate(hits):
   if tex[:m.start()].rstrip().endswith(('∇',r'\nabla')):continue
   rhs=tex[m.end():hits[i+1].start()if i+1<len(hits)else len(tex)]
   rhs=split_top(rhs)[0].split(';')[0].strip().rstrip('.,?');rhs=re.split(r'\\(?:quad|qquad)',rhs)[0]
   try:out[m[1]]={'variables':[SYMS[c]for c in m[2].replace(' ','').split(',')],'expression':scalar(rhs),'tex':rhs}
   except Exception:pass
 return out

def tuples(tex):
 tex=normalize_source_tex(tex).replace(r'\left','').replace(r'\right','');out=[]
 for m in re.finditer(r'\(([^()]*,[^()]*)\)',tex):
  parts=split_top(m[1])
  if len(parts)not in[2,3]:continue
  try:
   p=tuple(scalar(v)for v in parts)
   if all(not a.free_symbols for a in p):out.append(p)
  except Exception:pass
 return out

def equal(a,b):
 if isinstance(a,sp.MatrixBase)or isinstance(b,sp.MatrixBase):
  if not isinstance(a,sp.MatrixBase)or not isinstance(b,sp.MatrixBase)or a.shape!=b.shape:return False
  return all(sp.simplify(sp.trigsimp((x-y).rewrite(sp.sin)))==0 for x,y in zip(a,b))
 return sp.simplify(sp.trigsimp((a-b).rewrite(sp.sin)))==0
