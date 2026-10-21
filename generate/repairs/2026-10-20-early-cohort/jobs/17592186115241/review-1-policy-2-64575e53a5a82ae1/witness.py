import re,collections
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
v=sp.symbols('x y z w'); trans=standard_transformations+(implicit_multiplication_application,)
def expr(t):
 t=t.replace('−','-').replace(' ', '').strip().rstrip('.,')
 t=re.sub(r'\{x\}_\{([1-4])\}',lambda m:str(v[int(m[1])-1]),t)
 t=re.sub(r'x_\{([1-4])\}',lambda m:str(v[int(m[1])-1]),t)
 t=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',t)
 return sp.expand(parse_expr(t,local_dict=dict(zip(map(str,v),v)),transformations=trans))
def rawfix(t):return t.replace('\\\\','\\') if r'\\begin' in t else t

def vec(t):
 t=rawfix(t)
 m=re.search(r'\\begin\{(?:bmatrix|aligned)\}(.*?)\\end\{(?:bmatrix|aligned)\}',t,re.S)
 if not m:return None
 return tuple(expr(a) for a in m[1].split(r'\\'))
def system(t):
 m=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',rawfix(t),re.S)
 rows=[]
 n=4 if ('w' in m[1] or '{x}_{4}' in m[1]) else 3 if ('z' in m[1] or '{x}_{3}' in m[1]) else 2
 for line in m[1].split(r'\\'):
  left,right=line.replace('&','').split('='); e=expr(left)-expr(right)
  rows.append([e.coeff(a) for a in v[:n]]+[-e.subs(dict.fromkeys(v,0))])
 return sp.Matrix(rows)
def field(r):return r['question'][':question/answer-fields'][0]
def correct(r):
 f=field(r);ref=f[':answer-field/correct'];return ref[-1] if isinstance(ref,list) else ref[':answer/id']
def mathcheck(r):
 q=r['question']; M=system(q[':question/problem']); n=M.cols-1;R,piv=M.rref(); A=M[:,:-1];b=M[:,-1]; assertions=[]
 assertions.append(('consistent_one_free',n not in piv and n-len(piv)==1))
 valid=[]; bank=[]
 for c in field(r)[':answer-field/choices']:
  vv=vec(c[':answer/value']);bank.append(vv)
  if vv is None:continue
  syms=set().union(*(a.free_symbols for a in vv));dim=len(vv)==n
  works=dim and all(sp.simplify(a)==0 for a in A*sp.Matrix(vv)-b)
  # all solution sets have one parameter and a nonzero direction; rejects an isolated point
  full=works and len(syms)==1 and any(sp.diff(a,next(iter(syms)))!=0 for a in vv)
  if full:valid.append(c[':answer/id'])
 assertions.append(('unique_full_solution_and_key',valid==[correct(r)]))
 stages=[]
 for m in re.finditer(r'\\begin\{(array|bmatrix)\}(?:\{[c|]+\})?(.*?)\\end\{\1\}',q[':question/worked-solution'],re.S):
  try:
   a=sp.Matrix([[expr(c) for c in row.split('&')] for row in m[2].split(r'\\')])
   if a.shape==M.shape:stages.append(a)
  except Exception:pass
 assertions.append(('solution_stages_row_equivalent',bool(stages) and all(a.rref()[0]==R for a in stages)))
 return {'id':q[':question/id'],'matrix':str(M.tolist()),'rank':len(piv),'free_columns':[j for j in range(n) if j not in piv],'assertions':dict(assertions),'pass':all(a[1] for a in assertions),'stages':len(stages)}
def shortcut(r):
 cs=field(r)[':answer-field/choices']; vectors=[vec(c[':answer/value']) for c in cs]
 if any(x is None or len(x)<3 for x in vectors):return {'applicable':False,'id':r['question'][':question/id']}
 # Pure printed-component matching; no algebra, equations, parameter metadata or key used to choose.
 # Normalize whitespace only; expressions are already consistently formatted in these banks.
 strings=[re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',rawfix(c[':answer/value']),re.S) for c in cs]
 if not all(strings):return {'applicable':False,'id':r['question'][':question/id']}
 rows=[[a.strip() for a in x[1].split(r'\\')] for x in strings]
 modes=[];freq=[]
 for j in [0,1]:
  f=collections.Counter(x[j] for x in rows); freq.append(dict(f));mx=max(f.values()); modes.append([a for a,b in f.items() if b==mx])
 candidates=[i for i,row in enumerate(rows) if all(row[j] in modes[j] for j in [0,1])]
 unique_modes=all(len(a)==1 for a in modes)
 selected=cs[candidates[0]][':answer/id'] if len(candidates)==1 else None
 return {'id':r['question'][':question/id'],'applicable':True,'unique_modes':unique_modes,'component_counts':freq,'candidate_positions':[i+1 for i in candidates], 'selected_answer_id':selected,'correct':selected==correct(r),'correct_position':next(i+1 for i,c in enumerate(cs) if c[':answer/id']==correct(r))}
