"""Closed algebra checks for the exact linear/matrix lesson response families."""
import re,sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
R=Path(__file__).resolve().parents[5];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import ENV,environment,cells
symbols={x:sp.Symbol(x)for x in['x','y','k','a','b','c','d','l']}
def scalar(t):
 t=t.replace(r'\lambda','l');t=re.sub(r'\\color\{[^{}]*\}','',t);t=re.sub(r'\\hspace\{[^{}]*\}','',t);t=t.strip().strip('$').replace('−','-');t=re.sub(r'\\(?:displaystyle|textstyle|left|right)\b','',t);t=re.sub(r'\\[,;! ]|\\quad\b|\\qquad\b','',t);t=re.sub(r'\\(?:text|textrm|mathrm)\{[\s\u00a0]*\}','',t)
 def group(pos):
  while pos<len(t)and t[pos].isspace():pos+=1
  if t[pos]!='{':return t[pos],pos+1
  depth=1;end=pos+1
  while depth:
   depth+=(t[end]=='{')-(t[end]=='}');end+=1
  return t[pos+1:end-1],end
 while(m:=re.search(r'\\(?:dfrac|tfrac|frac)',t)):
  num,end=group(m.end());den,end=group(end);t=t[:m.start()]+'('+str(scalar(num))+')/('+str(scalar(den))+')'+t[end:]
 t=t.replace('{-}','-').replace('{+}','+')
 t=t.replace('\\cdot','*').replace('\\times','*').replace('^','**').replace('{','(').replace('}',')').strip().rstrip('.,?')
 assert re.fullmatch(r'[\dxykabcdl+*/().\s-]+',t),(t,'Unsupported scalar')
 return sp.simplify(parse_expr(t,local_dict=symbols,transformations=standard_transformations+(implicit_multiplication_application,)))
def matrices(text):
 out=[]
 for m in ENV.finditer(text):
  if m[1]!='begin'or m[2]not in['bmatrix','vmatrix','pmatrix','matrix','array']:continue
  span=environment(text,m.start());body=text[span[0]:span[1]]
  if m[2]=='array':
   col=re.match(r'\s*\{[^{}]+\}',body);assert col;body=body[col.end():]
  grid=cells(body)
  if grid and all(len(row)==len(grid[0])for row in grid):
   try:a=sp.Matrix([[scalar(x)for x in row]for row in grid])
   except Exception:continue
   out.append({'matrix':a,'start':m.start(),'end':span[2],'environment':m[2]})
 return out

def equations(text):
 found=[]
 for m in ENV.finditer(text):
  if m[1]!='begin'or m[2]not in['aligned','array','cases']:continue
  span=environment(text,m.start());body=text[span[0]:span[1]]
  if m[2]=='array':
   c=re.match(r'\s*\{[^{}]+\}',body);body=body[c.end():]if c else body
  rows=cells(body)
  if not rows or len(rows)!=2:continue
  try:
   result=[]
   for row in rows:
    row=''.join(row);lhs,rhs=row.split('=');result.append(scalar(lhs)-scalar(rhs))
   found.append(result)
  except Exception:continue
 assert found,('No complete two-row system',text[:200])
 return found[0]

def equivalent_rows(first,second):
 assert len(first)==len(second)
 for a,b in zip(first,second):
  ratio=sp.cancel(a/b);assert ratio!=0 and not ratio.free_symbols,(a,b,ratio)
 return True

def filled(q):return{f[':answer-field/key']:next(a[':answer/value']for a in f[':answer-field/choices']if a[':db/id']==f[':answer-field/correct'][':db/id'])for f in q[':question/answer-fields']}
def fill(value,bank):return re.sub(r'\{\{([^{}]+)\}\}',lambda m:bank[m[1]],value)
