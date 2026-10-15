"""Independent parser of ordinary numerical matrices and scalar matrix products."""
import re
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
MAT=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def scalar(t):
 t=t.strip().replace(' ','');t=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',t);assert re.fullmatch(r'[-+0-9()/]+',t),t
 return s.sympify(t)
def cells(body):
 rows=[[None if c.strip()=='∗' else scalar(c) for c in row.split('&')] for row in body.split(r'\\')];assert len(rows)==len(rows[0]) and len({len(r) for r in rows})==1;return rows
def expression(raw):
 objects=[]
 def repl(m):
  rr=cells(m[1]);objects.append(rr);return 'M'+str(len(objects)-1)
 text=MAT.sub(repl,raw);text=re.sub(r'\\(?:left|right|bigl|bigr|,|;|!)','',text).strip().rstrip('.,')
 text=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',text);text=text.replace('{','(').replace('}',')')
 text=re.sub(r'(M\d+)(?=M)',r'\1*',text);text=re.sub(r'(?<=\))(M\d+)',r'*\1',text)
 assert re.fullmatch(r'[M0-9+*/()\s.\-]+',text),text
 local={f'M{i}':s.Matrix([[0 if c is None else c for c in row] for row in rr]) for i,rr in enumerate(objects)}
 result=parse_expr(text,local_dict=local,transformations=standard_transformations+(implicit_multiplication_application,));assert isinstance(result,s.MatrixBase)
 return result,objects

def named(text):
 result={};bases={}
 for m in re.finditer(r'([A-Z])\s*=\s*',text):
  mat=MAT.match(text,m.end()) or MAT.search(text,m.end())
  if not mat:continue
  prefix=text[m.end():mat.start()]
  if any(z in prefix for z in (',','$','=','\n\n')):continue
  value,objects=expression(text[m.end():mat.end()]);assert len(objects)==1
  result[m[1]]=value;bases[m[1]]=s.Matrix(objects[0])
 return result,bases

def rows(block):
 objects=[]
 def repl(m):objects.append(m[0]);return 'MATRIX'+str(len(objects)-1)
 protected=MAT.sub(repl,block);pieces=protected.split(r'\\');out=[]
 for piece in pieces:
  piece=re.sub(r'MATRIX(\d+)',lambda m:objects[int(m[1])],piece)
  out.append(piece)
 return out
