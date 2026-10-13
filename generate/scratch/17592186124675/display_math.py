"""Independent display evaluator for this extracted LaTeX subset.

Reads learner text (not generation calculations). Each displayed equality row,
integral/separation row, exponential/log substitution, and decimal approximation
is evaluated from a model solved independently from prompt observations.
"""
import re
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
TRANS=standard_transformations+(implicit_multiplication_application,rationalize,)
def brace(text,pos):
 assert text[pos]=='{';depth=0
 for j in range(pos,len(text)):
  depth+=(text[j]=='{')-(text[j]=='}')
  if depth==0:return text[pos+1:j],j+1
 raise AssertionError('Unbalanced braces')
def normalize(expr):
 expr=expr.replace('⁡','').replace(r'\operatorname{ln}','ln').replace(r'\ln','ln')
 expr=expr.replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').replace(r'\,','').replace(r'\text{d}t','dt')
 expr=re.sub(r'\{t\}_\{1\}','u',expr)
 expr=re.sub(r'\\text\{[^}]*\}','',expr).replace('…','')
 expr=re.sub(r'(?<=\d),(?=\d{3})','',expr)
 expr=re.sub(r'\{e\}','e',expr)
 # Recursively convert only this lesson's fraction/root constructs.
 while r'\frac' in expr or r'\dfrac' in expr or r'\sqrt' in expr:
  m=re.search(r'\\(d?frac|sqrt)',expr);cmd=m.group(1);start=m.start();pos=m.end();A,end=brace(expr,pos)
  if cmd.endswith('frac'):
   B,end=brace(expr,end); rep='(('+normalize(A)+')/('+normalize(B)+'))'
  else:rep='sqrt('+normalize(A)+')'
  expr=expr[:start]+rep+expr[end:]
 while '^' in expr:
  pos=expr.index('^')+1
  if expr[pos]=='{':A,end=brace(expr,pos)
  else:A=expr[pos];end=pos+1
  expr=expr[:pos-1]+'**('+normalize(A)+')'+expr[end:]
 expr=expr.replace(r'\int','').replace('{','(').replace('}',')')
 expr=re.sub(r'ln\|([^|]+)\|',r'ln(\1)',expr)
 expr=expr.replace('kdt','k*dt').replace('kt','k*t').replace('kd','k*d').replace('ku','k*u')
 return expr.strip().rstrip('.,')

def oracle_from_prompt(prompt,name):
 # Extract only numbers displayed in the problem, discarding t>=0 bounds.
 atom=r'\\frac\{\d+\}\{\d+\}|(?<![A-Za-z])\d+(?:\\,\d{3})*(?:\.\d+)?'
 numbers=[parse_expr(normalize(x),transformations=TRANS) for x in re.findall(atom,prompt)]
 if name=='q-37400':k,a,_,n0,time=numbers; t1=s.S.Zero; observed=n0
 elif name=='q-335282':k,a,_,n0,target=numbers; t1=s.S.Zero;observed=n0
 elif name=='q-335280':a,duplicate_a,_,_,n0,tau,n1,target=numbers;assert a==duplicate_a;t1=s.S.Zero;observed=n0;k=s.log((a-n0)/(a-n1))/tau
 elif name in ['q-15370','q-335542']:a,n0,tau,n1,target,_=numbers;t1=s.S.Zero;observed=n0;k=s.log((a-n0)/(a-n1))/tau
 elif name=='q-335578':a,n0,duplicate_a,tau,n1,target,_=numbers;assert a==duplicate_a;t1=s.S.Zero;observed=n0;k=s.log((a-n0)/(a-n1))/tau
 else:
  
  if name=='q-335619':a,n1,t1,n2,t2,last=numbers
  else:a,n1,n2,t1,t2,last=numbers
  observed=n1;k=s.log((a-n1)/(a-n2))/(t2-t1)
  if name=='q-335619':target=last
  else:time=last
 K=s.simplify((a-observed)*s.exp(k*t1));t=s.Symbol('t',real=True);f=a-K*s.exp(-k*t)
 result=f.subs(t,time) if 'time' in locals() else s.log(K/(a-target))/k
 return dict(a=a,K=K,k=k,t=t,f=f,result=result,t0=t1,observed=observed,time=locals().get('time'),target=locals().get('target'),answer=int(s.floor(s.N(result,40)+s.Rational(1,2))))

def evaluate(expr,o,tvalue):
 expr=normalize(expr)
 t=o['t'];f=o['f'];targettime=o['result']
 # Replace displayed quantity function calls using exact exponential solution.
 def function(m):
  arg=parse_expr(m.group(2),local_dict={'t':s.Rational(tvalue),'u':targettime,'d':targettime},transformations=TRANS)
  return '('+str(f.subs(t,arg))+')'
 expr=re.sub(r'([PXTE])\(([^()]+)\)',function,expr)
 variables={key:o[key] for key in ['a','K','k']};variables.update({'t':s.Rational(tvalue),'u':targettime,'d':targettime,'C':-s.log(o['K']),'e':s.E,'ln':s.log,'sqrt':s.sqrt,'dt':s.S.One})
 for name in ['P','X','T','E']:
  variables[name]=f.subs(t,tvalue);variables['d'+name]=s.diff(f,t).subs(t,tvalue)
 result=parse_expr(expr,local_dict=variables,transformations=TRANS)
 assert result.free_symbols==set(),(expr,result)
 return result

def check_solution(prompt,solution,name):
 o=oracle_from_prompt(prompt,name);total=0
 for block in re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S):
  block=re.sub(r'\\(?:begin|end)\{aligned\}','',block)
  inherited=None
  for row in block.split(r'\\'):
   row=row.replace('&','').strip()
   if '=' not in row and '≈' not in row:continue
   is_integral=r'\int' in row
   if is_integral:row=row.replace(r'\int','') # Verify both integrands after dQ substitution.
   parts=re.split(r'(=|≈)',row);parts=[p.strip() for p in parts]
   lhs=parts[0] or inherited
   if not lhs:raise AssertionError(('Missing inherited lhs',row))
   inherited=lhs
   # A continuation decimal '=' is a source approximate display, not exact equality.
   left=lhs
   for j in range(1,len(parts),2):
    op=parts[j];right=parts[j+1]
    for tvalue in [0,1,3]:
     lv=evaluate(left,o,tvalue);rv=evaluate(right,o,tvalue)
     if '…' in right:
      decimals=re.search(r'\.(\d+)',right);tol=10**(-len(decimals.group(1))) if decimals else 1
      assert 0<=float(s.N(lv-rv,25))<tol+1e-10,(name,row,lv,rv)
     elif op=='≈':
      if '…' in left:assert abs(float(s.N(lv-rv,25)))<=0.501,(name,row,lv,rv)
      else:assert int(s.floor(s.N(lv,40)+s.Rational(1,2)))==int(rv),(name,row,lv,rv)
     else:assert abs(float(s.N(lv-rv,30)))<1e-20,(name,row,lv,rv)
    total+=1;left=right
 return o,total
