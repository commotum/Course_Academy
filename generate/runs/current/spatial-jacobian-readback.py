"""Root 3D map/matrix/cofactor readers; independent of per-KP generator code."""
import importlib.util,re
from pathlib import Path
import sympy as s
z=importlib.util.spec_from_file_location('parent_spatial_scalar',Path(__file__).with_name('ode-scalar-parser.py'));p=importlib.util.module_from_spec(z);z.loader.exec_module(p)
u,v,w=p.u,p.v,p.t;x,y,z=p.x,p.y,p.z

def scalar(raw):
 raw=raw.strip().rstrip('.,').replace(r'\dfrac',r'\frac').replace(r'\tfrac',r'\frac').replace(r'\text{ }','').replace(r'\qquad','').replace(r'\u2061','').replace(r'\theta','k')
 while True:
  m=re.search(r'\\sqrt\[(\d+)\]\{',raw)
  if not m:break
  end=m.end();start=end;depth=1
  while depth:depth+=(raw[end]=='{')-(raw[end]=='}');end+=1
  raw=raw[:m.start()]+'('+raw[start:end-1]+')^{'+r'\frac{1}{'+m[1]+'}}'+raw[end:]
 raw=re.sub(r'\\operatorname\{(sin|cos|ln|log|exp)\}',lambda m:'\\'+m[1],raw)
 for fun in ('sin','cos','ln','log'):raw=raw.replace('{'+fun+'}', '\\'+fun)
 # Mask coordinate names in commands; mathematical w maps to the distinct real t.
 raw=re.sub(r'\\[A-Za-z]+|[wabc]',lambda m:m[0] if m[0].startswith('\\') else {'w':'t','a':'x','b':'y','c':'z'}[m[0]],raw)
 return p.scalar(raw)
def same(a,b):return s.simplify(s.trigsimp(a-b))==0

def displays(text):return re.findall(r'\$\$(.*?)\$\$',text,re.S)
def components(prompt,out=('x','y','z')):
 block=displays(prompt)[0].strip()
 if '⟶' in block or r'\to' in block:
  tail=re.split(r'⟶|\\to',block)[-1];body=re.search(r'\\begin\{(?:aligned|bmatrix)\}(.*?)\\end\{(?:aligned|bmatrix)\}',tail,re.S)[1];return tuple(scalar(z) for z in body.split(r'\\'))
 parts=re.split(r'\\,|\\qquad\s*',block.rstrip('.'));assert len(parts)==3,block
 assert [q.split('=',1)[0].strip() for q in parts]==list(out),parts
 return tuple(scalar(q.split('=',1)[1]) for q in parts)

def leaf_arrays(text):
 found=[]
 for m in re.finditer(r'\\begin\{(aligned|bmatrix|vmatrix)\}((?:(?!\\begin\{).)*?)\\end\{\1\}',text,re.S):
  rows=m[2].split(r'\\');cells=[row.split('&') for row in rows]
  if len(set(map(len,cells)))!=1:continue
  if any('=' in c for row in cells for c in row):continue
  if '∂' in m[2] or r'\partial' in m[2]:found.append({'span':m.span(),'body':m[2],'formal':True,'shape':(len(rows),len(cells[0]))});continue
  found.append({'span':m.span(),'body':m[2],'formal':False,'matrix':s.Matrix([[scalar(z) for z in row] for row in cells]),'shape':(len(rows),len(cells[0]))})
 return found

def reduce_arrays(raw,formal='0'):
 for arr in reversed(leaf_arrays(raw)):
  a,b=arr['span'];assert a>0 and raw[a-1]=='|' and b<len(raw) and raw[b]=='|',(raw,arr)
  if arr['formal']:replacement=formal
  else:
   M=arr['matrix'];assert M.rows==M.cols;replacement='('+s.latex(M.det())+')'
  raw=raw[:a-1]+replacement+raw[b+1:]
 return raw

def teaching_rows(block):
 text=reduce_arrays(block,'FORMAL');text=text.strip()
 if text.startswith(r'\begin{aligned}'):text=text[len(r'\begin{aligned}'):-len(r'\end{aligned}')]
 return [z.strip().rstrip('.') for z in text.split(r'\\')]

def partials(solution,outputs,inputs):
 labels=re.findall(r'\\frac\{(?:∂|\\partial)\s*([uvwxyz])\}\{(?:∂|\\partial)\s*([uvwxyz])\}\s*&?\s*=(.*?)(?=\s*&|\\\\|\\end\{aligned\})',solution,re.S)
 assert len(labels)==9,(len(labels),solution)
 assert [(a,b) for a,b,_ in labels]==[(a,b) for a in outputs for b in inputs]
 return s.Matrix(3,3,[scalar(z) for _,_,z in labels])

def determinant_stages(solution,J,raw_error=False):
 section=solution.split('Therefore,',1)[1];block=displays(section)[0];arrays=leaf_arrays(block);formal=[a for a in arrays if a['formal']];numeric=[a['matrix'] for a in arrays if not a['formal']];assert len(formal)<=1 and all(a['shape']==(3,3) for a in formal)
 assert numeric and numeric[0]==J,('Printed full matrix',numeric[0],J)
 validminors=[J.minor_submatrix(i,j) for i in range(3) for j in range(3)];errors=[]
 for M in numeric[1:]:
  assert M.shape==(2,2)
  if not any(M==N for N in validminors):errors.append(M)
 if errors:assert raw_error,('Incorrect cofactor minor',errors,J)
 det=J.det();rows=teaching_rows(block)
 for row in rows[1:]:
  rhs=row.split('=',1)[1].replace('&','').strip();assert same(scalar(rhs),det),('Printed determinant stage',row,det)
 return {'formal_matrix':len(formal),'numeric_matrix':1,'cofactor_minors':len(numeric)-1,'known_raw_minor_errors':len(errors),'determinant_rows':len(rows)-1}
