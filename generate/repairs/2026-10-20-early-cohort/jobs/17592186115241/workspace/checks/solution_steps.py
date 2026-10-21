"""Verify each printed elementary row operation against successive visible matrices."""
import json,re,sys
sys.dont_write_bytecode=True
from validate_repair import E,dump,sp
from witness import expr,system,vec,field,correct
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
rr=sp.symbols('r1 r2 r3 r4');results=[]
records=sum((json.load(open(E/p)) for p in ['fresh.json','source-replay-records.json','counterfactual-records.json','render-records.json']),[])
for r in records:
 q=r['question'];M=system(q[':question/problem']);text=q[':question/worked-solution'];matrices=[]
 for m in re.finditer(r'\\begin\{(array|bmatrix)\}(?:\{[c|]+\})?(.*?)\\end\{\1\}',text,re.S):
  try:a=sp.Matrix([[expr(c) for c in row.split('&')] for row in m[2].split(r'\\')])
  except Exception:continue
  if a.shape==M.shape:matrices.append((m,a))
 tests=[]
 for (prev,A),(nxt,B) in zip(matrices,matrices[1:]):
  gap=text[prev.end():nxt.start()].replace('&','').replace(' ','').replace('{R}','R')
  mt=re.search(r'R_\{([1-4])\}:=(.*?)(?:\\\\|\\end)',gap)
  if not mt:
   assert A==B,('unlabeled changed stage',q[':question/id']);continue
  i=int(mt[1])-1;rhs=re.sub(r'R_\{([1-4])\}',lambda m:'r'+m[1],mt[2].strip())
  rhs=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',rhs)
  e=parse_expr(rhs,local_dict={str(t):t for t in rr},transformations=standard_transformations+(implicit_multiplication_application,))
  expect=A.copy();expect[i,:]=sum((e.coeff(rr[j])*A.row(j) for j in range(A.rows)),sp.zeros(1,A.cols))
  assert expect==B,(q[':question/id'],mt[0]);tests.append(mt[0])
 results.append({'id':q[':question/id'],'tested_printed_operations':len(tests)})
dump('solution-results.json',{'records':len(results),'operations':sum(r['tested_printed_operations'] for r in results),'failures':[],'cases':results})
print(json.dumps({'records':len(results),'operations':sum(r['tested_printed_operations'] for r in results),'failures':0}))
