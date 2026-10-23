import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
x,y,z=sp.symbols('x y z')
def expr(s):
 s=s.strip().replace(' ','').replace('⟨','').replace('⟩','')
 s=re.sub(r'\\(?:d?frac)\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
 for a,b in [('{x}_{1}','x'),('{x}_{2}','y'),('{x}_{3}','z'),('x_{1}','x'),('x_{2}','y'),('x_{3}','z')]:s=s.replace(a,b)
 s=s.replace(r'\left','').replace(r'\right','').replace(r'\,','').rstrip('.')
 return parse_expr(s,local_dict={'x':x,'y':y,'z':z},transformations=standard_transformations+(implicit_multiplication_application,),evaluate=True)
def vec(s):
 if s.startswith('\\\\begin') or s.startswith('⟨') and '\\\\frac' in s:s=s.replace('\\\\','\\')
 if s.startswith('⟨'):parts=s[1:-1].split(',')
 else:parts=s.removeprefix(r'\begin{bmatrix}').removesuffix(r'\end{bmatrix}').split(r'\\')
 return tuple(expr(a) for a in parts)
def equations(q):
 body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/problem'],re.S)[1]
 return [expr(a)-expr(b) for a,b in (row.replace('&','').split('=') for row in body.split(r'\\'))]
def inspect(r):
 q=r['question'];f=q[':question/answer-fields'][0];eq=equations(q);sol=sp.solve(eq,(x,y,z));v=tuple(sol[t] for t in (x,y,z));bank=[vec(a[':answer/value']) for a in f[':answer-field/choices']];correct=f[':answer-field/correct'];cid=correct[1] if isinstance(correct,list) else correct[':answer/id'];idx=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==cid)
 assert len(set(bank))==5 and bank.count(v)==1 and bank[idx]==v,(q[':question/id'],v,bank)
 # Independently evaluate every equality in the generated two displayed substitution chains.
 chains=[]
 for block in re.findall(r'\$\$(.*?)\$\$',q.get(':question/worked-solution',''),re.S):
  for chain in block.split('⟹'):
   chain=chain.replace(r'\,','').strip()
   terms=chain.split('=')
   if len(terms)<2:continue
   vals=[sp.simplify(expr(t).subs(sol)) for t in terms]
   assert len(set(vals))==1,(q[':question/id'],chain,vals)
   chains.append(chain)
 return {'id':q[':question/id'],'profile':r.get('generation',{}).get('profile'),'solution':list(map(str,v)),'bank':[list(map(str,a)) for a in bank],'correct_index':idx,'equations':list(map(str,eq)),'checked_solution_chains':chains}
