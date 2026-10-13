"""Parent derives actual displayed3-vector/vertex determinant arithmetic."""
import importlib.util,re
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;sp=importlib.util.spec_from_file_location('root_triple_scalar',P/'vector-math-parser.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
B=(p.i,p.j,p.k)
def basis(v):return sum(a*b for a,b in zip(v,B))
def given(prompt,positions=False,parameter=None):
 mapping={parameter:'t'} if parameter else {}
 def scalar(z):
  z=re.sub(r'\\[A-Za-z]+|[A-Za-z]',lambda m:m[0] if m[0].startswith('\\') else mapping.get(m[0],m[0]),z)
  return p.scalar(z)
 if positions:
  pairs=re.findall(r'([A-Z])\(([^()]*)\)',prompt);assert len(pairs)==4;pairs={n:s.Matrix([scalar(z) for z in raw.split(',')]) for n,raw in pairs};origin=next(iter(pairs));names=[origin+n for n in pairs if n!=origin];vectors=[pairs[n[-1]]-pairs[origin] for n in names];points={n.lower():basis(v) for n,v in pairs.items()};refs={n:basis(v) for n,v in zip(names,vectors)}
 else:
  pairs=re.findall(r'([a-z])\s*=\s*⟨(.*?)⟩',prompt);assert len(pairs)==3;names=[n for n,raw in pairs];vectors=[s.Matrix([scalar(z) for z in raw.split(',')]) for n,raw in pairs];points={};refs={n:basis(v) for n,v in zip(names,vectors)}
 assert all(len(v)==3 for v in vectors);T=s.Matrix.hstack(*vectors).det();return dict(names=names,vectors=vectors,points=points,refs=refs,triple=T,volume=s.Abs(T),parameter=parameter,scalar=scalar)
def expression(raw,d):
 raw=raw.strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace(r'\,','')
 if r'\times' in raw and r'\cdot' in raw:
  cleaned=re.sub(r'\\overset\{\\to\s*\}\{([A-Z]{2})\}',r'\1',raw);cleaned=cleaned.replace(' ','')
  wanted=d['names'][0]+r'\cdot('+d['names'][1]+r'\times'+d['names'][2]+')';assert cleaned==wanted,(cleaned,wanted);return d['triple']
 if raw=='V':return d['volume']
 if raw in d['refs']:return d['refs'][raw]
 raw=re.sub(r'\\overset\{\\to\s*\}\{([A-Z]{2})\}',lambda m:'('+s.latex(d['refs'][m[1]])+')',raw)
 raw=re.sub(r'⟨(.*?)⟩',lambda m:'('+s.latex(basis([d['scalar'](z) for z in m[1].split(',')]))+')',raw)
 if d['points'] and re.fullmatch(r'[a-z]\s*-\s*[a-z]',raw):raw=re.sub(r'\\[A-Za-z]+|[a-z]',lambda m:'('+s.latex(d['points'][m[0]])+')' if m[0] in d['points'] else m[0],raw)
 pat=r'\|\\begin\{(?:aligned|vmatrix)\}((?:(?!\\begin\{).)*?)\\end\{(?:aligned|vmatrix)\}\|'
 while m:=re.search(pat,raw,re.S):
  rows=[[d['scalar'](z) for z in row.split('&')] for row in m[1].split(r'\\')];assert len(rows) in (2,3) and all(len(row)==len(rows) for row in rows);raw=raw[:m.start()]+'('+s.latex(s.Matrix(rows).det())+')'+raw[m.end():]
 while m:=re.search(r'\|([^|]+)\|',raw):raw=raw[:m.start()]+'('+s.latex(s.Abs(d['scalar'](m[1])))+')'+raw[m.end():]
 return d['scalar'](raw)
def rows(block):
 arrays=[]
 def save(m):arrays.append(m[0]);return 'ROOTARRAY'+str(len(arrays)-1)
 block=re.sub(r'\|\\begin\{aligned\}((?:(?!\\begin\{).)*?)\\end\{aligned\}\|',save,block,flags=re.S);block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
 return [re.sub(r'ROOTARRAY(\d+)',lambda m:arrays[int(m[1])],row) for row in block.split(r'\\')]
def solution(solution,d):
 C=dict(blocks=0,equalities=0,arrays=0,vector_subtraction_rows=0)
 for block in re.findall(r'\$\$(.*?)\$\$',solution,re.S):
  C['blocks']+=1;C['arrays']+=len(re.findall(r'\|\\begin\{aligned\}',block));prev=None
  for row in rows(block):
   if '=' not in row:continue
   sides=row.split('=');values=[]
   for n,z in enumerate(sides):
    if not z.strip():assert n==0 and prev is not None;value=prev
    else:value=expression(z,d)
    values.append(value)
   assert all(s.simplify(value-values[0])==0 for value in values[1:]),('False displayed triple stage',row,values);prev=values[-1];C['equalities']+=len(values)-1
   if d['points'] and re.fullmatch(r'\s*[a-z]-[a-z]\s*',sides[-1]):C['vector_subtraction_rows']+=1
 return C
