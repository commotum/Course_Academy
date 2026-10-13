"""Parent reads Cartesian points/vectors and complete determinant/norm teaching math."""
import importlib.util,re
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('root_triangle_scalar',P/'vector-math-parser.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
B=(p.i,p.j,p.k)
def basis(v):return sum(a*b for a,b in zip(v,B))
def vector(v):
 v=s.expand(v);z=s.Matrix([v.coeff(b) for b in B]);assert s.simplify(v-basis(z))==0,('Expected actual3vector',v);return z

def task(prompt,kind):
 vals={};arrows={}
 if kind=='vectors':
  pairs=re.findall(r'([a-z])\s*=\s*⟨(.*?)⟩',prompt);assert len(pairs)==2,(prompt,pairs)
  names=[z[0] for z in pairs];u,v=[s.Matrix([p.scalar(z) for z in raw.split(',')]) for name,raw in pairs];assert len(u)==len(v)==3
  vals={name:basis(value) for name,value in zip(names,(u,v))}
 else:
  pairs=re.findall(r'([A-Z])\(([^()]*)\)',prompt);assert len(pairs)==3,(prompt,pairs)
  pts={name:s.Matrix([p.scalar(z) for z in raw.split(',')]) for name,raw in pairs};assert all(len(z)==3 for z in pts.values())
  vals={name.lower():basis(value) for name,value in pts.items()}
  arrows={a+b:basis(pb-pa) for a,pa in pts.items() for b,pb in pts.items() if a!=b}
  if kind=='altitude':
   altitude_label=re.search(r'altitude\s*\$([A-Z]{2})',prompt)[1];altitude=altitude_label[0];other=[z for z in pts if z!=altitude];origin=other[0];end=other[1];u=pts[end]-pts[origin];v=pts[altitude]-pts[origin]
   lengths={a+b:s.sqrt((pb-pa).dot(pb-pa)) for a,pa in pts.items() for b,pb in pts.items() if a!=b}
  else:origin,end,last=pts;u=pts[end]-pts[origin];v=pts[last]-pts[origin]
 w=u.cross(v);norm=s.sqrt(w.dot(w));triangle='parallelogram' not in prompt;area=norm/2 if triangle else norm
 scalars={'A':norm,'TRIANGLE':norm/2}
 if kind=='altitude':scalars.update(lengths);scalars[altitude_label]=norm/s.sqrt(u.dot(u));answer=scalars[altitude_label]
 else:answer=area
 return dict(kind=kind,vals=vals,arrows=arrows,scalars=scalars,u=u,v=v,w=w,norm=norm,answer=answer,triangle=triangle)

def expression(raw,d):
 raw=raw.strip().rstrip('.,').replace(r'\,','').replace(r'\!','')
 if d['kind']!='vectors' and re.fullmatch(r'[a-z]\s*-\s*[a-z]',raw) and all(z in d['vals'] for z in raw.replace(' ','').split('-')):
  a,b=raw.replace(' ','').split('-');return d['vals'][a]-d['vals'][b]
 raw=re.sub(r'\{A\}_\{?△\}?', 'TRIANGLE',raw)
 raw=re.sub(r'\\overset\{\\to\s*\}\{([A-Z]{2})\}',lambda m:'('+s.latex(d['arrows'][m[1]])+')',raw)
 raw=re.sub(r'⟨(.*?)⟩',lambda m:'('+s.latex(basis([p.scalar(z) for z in m[1].split(',')]))+')',raw)
 # Consume exact determinant arrays before interpreting norm bars.
 pattern=re.compile(r'\|\\begin\{(?:aligned|vmatrix)\}((?:(?!\\begin\{).)*?)\\end\{(?:aligned|vmatrix)\}\|',re.S)
 while m:=pattern.search(raw):
  rows=[[p.scalar(cell) for cell in row.split('&')] for row in m[1].split(r'\\')];assert len(rows) in (2,3) and all(len(row)==len(rows) for row in rows)
  val=s.Matrix(rows).det();raw=raw[:m.start()]+'('+s.latex(val)+')'+raw[m.end():]
 # Resolve supplied position vectors, retaining i/j/k as independent basis slots.
 if d['kind']=='vectors':raw=re.sub(r'\\[A-Za-z]+|[a-z]',lambda m:'('+s.latex(d['vals'][m[0]])+')' if m[0] in d['vals'] else m[0],raw)
 # Cross products have two already-resolved vectors. A source norm wraps them.
 if r'\times' in raw:
  assert raw.count(r'\times')==1,raw
  normed=raw.startswith('|') and raw.endswith('|');body=raw[1:-1] if normed else raw;aa,bb=body.split(r'\times');ww=vector(p.scalar(aa)).cross(vector(p.scalar(bb)));return s.sqrt(ww.dot(ww)) if normed else basis(ww)
 while m:=re.search(r'\|([^|]+)\|',raw):
  vv=vector(p.scalar(m[1]));raw=raw[:m.start()]+'('+s.latex(s.sqrt(vv.dot(vv)))+')'+raw[m.end():]
 for name,value in sorted(d['scalars'].items(),key=lambda z:-len(z[0])):raw=re.sub(r'(?<![A-Za-z])'+name+r'(?![A-Za-z])',lambda m:'('+s.latex(value)+')',raw)
 return p.scalar(raw)

def check(q,kind):
 d=task(q[':question/problem'],kind);c=dict(choices=0,solution_sides=0,determinants=0,blocks=0,edges=0)
 for f in q[':question/answer-fields']:
  vs=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];corrects=[z[':answer/id'] for z,v in zip(f[':answer-field/choices'],vs) if s.simplify(v-d['answer'])==0];assert corrects==[f[':answer-field/correct'][1]],(q[':question/problem'],vs,d['answer']);c['choices']+=len(vs)
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S)
 for block in blocks:
  original=block;c['determinants']+=len(re.findall(r'\|\\begin\{aligned\}',block))
  # Matrix internals have row separators that must not split teaching rows.
  arrays=[]
  def save(m):arrays.append(m[0]);return 'MATRIX'+str(len(arrays)-1)
  block=re.sub(r'\|\\begin\{aligned\}((?:(?!\\begin\{).)*?)\\end\{aligned\}\|',save,block,flags=re.S)
  block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','');rows=block.split(r'\\');prev=None
  for row in rows:
   row=re.sub(r'MATRIX(\d+)',lambda m:arrays[int(m[1])],row)
   if '=' not in row:continue
   vals=[]
   for j,side in enumerate(row.split('=')):
    if not side.strip():assert j==0 and prev is not None;v0=prev
    else:v0=expression(side,d)
    vals.append(v0)
   assert all(s.simplify(value-vals[0])==0 for value in vals),('False printed stage',row,vals)
   prev=vals[-1];c['solution_sides']+=len(vals)-1
  if 'q-p' in original or 'b-a' in original:c['edges']+=1
  c['blocks']+=1
 assert c['determinants']==4 and c['solution_sides']>=8,c
 return d,c
