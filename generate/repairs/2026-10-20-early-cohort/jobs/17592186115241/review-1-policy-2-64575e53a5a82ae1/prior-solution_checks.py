import sys,re,json,sympy as sp
sys.dont_write_bytecode=True
from audit import E,dump,expr,system,vec,field,correct
records=sum((json.load(open(E/p)) for p in ['batch.json','fresh.json','source-replay-records.json','counterfactual-records.json','boundary-records.json']),[])
results=[]
for r in records:
 q=r['question']; M=system(q[':question/problem']); n=M.cols-1; text=q[':question/worked-solution'];matrices=[]
 for m in re.finditer(r'\\begin\{(array|bmatrix)\}(?:\{[c|]+\})?(.*?)\\end\{\1\}',text,re.S):
  try:a=sp.Matrix([[expr(c) for c in row.split('&')] for row in m[2].split(r'\\')])
  except Exception:continue
  if a.shape==M.shape:matrices.append((m,a))
 tests=[]
 for (prev,A),(nxt,B) in zip(matrices,matrices[1:]):
  gap=text[prev.end():nxt.start()].replace('&','').replace(' ','').replace('{R}','R')
  mt=re.search(r'R_\{([1-4])\}:=(.*?)(?:\\\\|\\end)',gap)
  if not mt:
   tests.append({'operation':'repeat display','passed':A==B});continue
  i=int(mt[1])-1;rhs=mt[2].strip(); rhs=re.sub(r'R_\{([1-4])\}',lambda m:'r'+m[1],rhs)
  # parse coefficient expression with explicit row symbols via implicit multiplication.
  from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
  rhs=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',rhs)
  e=parse_expr(rhs,local_dict={str(t):t for t in rr},transformations=standard_transformations+(implicit_multiplication_application,))
  expect=A.copy();expect[i,:]=sum((e.coeff(rr[j])*A.row(j) for j in range(A.rows)),sp.zeros(1,A.cols))
  tests.append({'operation':mt[0],'passed':expect==B})
 # Isolated general-solution equations and final vector must agree with independently checked key.
 key=next(vec(c[':answer/value']) for c in field(r)[':answer-field/choices'] if c[':answer/id']==correct(r))
 vectors=[vec(m.group()) for m in re.finditer(r'\\begin\{bmatrix\}[^&]*?\\end\{bmatrix\}',text,re.S)]
 symbolic=[v for v in vectors if v is not None and len(v)==n]
 final=symbolic[-1] if symbolic else None
 results.append({'id':q[':question/id'],'stage_steps':tests,'final_solution_vector_matches_key':final==key,'pass':all(t['passed'] for t in tests) and final==key})
dump('solution-results.json',{'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python solution_checks.py','cases':results,'failures':[r for r in results if not r['pass']]})
print('cases',len(results),'failures',len([r for r in results if not r['pass']]))
