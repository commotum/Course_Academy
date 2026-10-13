"""Independent parsing of displayed TeX, not matching hidden recipe metadata."""
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
x,y,D=sp.symbols('x y D',real=True)

def group(s,i):
 if s[i]!='{':raise ValueError(('expected group',s,i))
 depth=1;j=i+1
 while depth:
  if j>=len(s):raise ValueError('unbalanced braces')
  depth+=(s[j]=='{')-(s[j]=='}');j+=1
 return s[i+1:j-1],j

def convert(s):
 out='';i=0
 while i<len(s):
  if s.startswith(r'\frac',i):
   a,j=group(s,i+5);b,i=group(s,j);out+='(('+convert(a)+')/('+convert(b)+'))'
  elif s.startswith(r'\sqrt',i):
   a,i=group(s,i+5);out+='sqrt('+convert(a)+')'
  elif s[i]=='{':
   a,i=group(s,i);out+='('+convert(a)+')'
  elif s[i]=='^':
   i+=1
   if s[i]=='{':a,i=group(s,i)
   else:a=s[i];i+=1
   out+='**('+convert(a)+')'
  else:out+=s[i];i+=1
 return out

def expr(s):
 s=s.replace(r'\frac{\text{d}y}{\text{d}x}','D')
 s=re.sub(r'\\operatorname\{(sin|csc)\}⁡([0-9]*x)',lambda m:' '+m[1]+'('+m[2]+')',s)
 s=s.replace(r'\text{ }','').replace(r'\cdot','*').replace(r'\,','').strip().rstrip('.,')
 s=convert(s)
 return parse_expr(s,local_dict={'x':x,'y':y,'D':D,'e':sp.E,'sin':sp.sin,'csc':sp.csc,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))

def equation(s):
 lhs,rhs=s.split('=');return expr(lhs),expr(rhs)

def resolved(s):
 a,b=equation(s);assert sp.diff(a,D,2)==0 and not b.has(D)
 coeff=sp.diff(a,D);assert coeff!=0
 return sp.simplify((b-a.subs(D,0))/coeff)

def separated(s):
 a,b=equation(s);co=sp.diff(a,D)
 return sp.simplify(sp.diff(co,x))==0 and not a.subs(D,0).has(x) and not b.has(y,D)

def same(a,b):return sp.simplify(sp.expand_power_exp(a-b))==0

def formatting(s):
 assert s.count('$')%2==0
 depth=0
 for c in s:
  depth+=(c=='{')-(c=='}');assert depth>=0
 assert depth==0
 assert not re.search(r'\+\-|\-\-',s)

def math_blocks(s):return re.findall(r'\$\$\s*(.*?)\s*\$\$',s,re.S)

def validate_bank(prompt,solution,bank,correct):
 formatting(prompt);formatting(solution)
 for a in bank:formatting(a)
 ode=resolved(math_blocks(prompt)[0]);assert len(bank)==5
 eqs=[resolved(v) for v in bank]
 valid=[i for i,v in enumerate(bank) if separated(v) and same(eqs[i],ode)]
 assert valid==[correct],('response collision',bank,valid)
 # Equivalent ODEs in unseparated forms are intentional distractors. They are
 # distinct complete response objects because eligibility is part of the task.
 for i,a in enumerate(bank):
  for j,b in enumerate(bank[:i]):
   assert not(same(eqs[i],eqs[j]) and separated(a) and separated(b)),('equivalent separated bank',a,b)
 blocks=math_blocks(solution);assert len(blocks) in (4,5)
 assert 'h(x)g(y)' in blocks[0] and 'h(x)' in blocks[1]
 for block in blocks[2:]:
  if r'\begin{aligned}' in block:
   rows=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
   lhs=None
   for row in rows:
    row=row.replace('&','').strip()
    if row.startswith('='):row=lhs+row
    else:lhs=row.split('=')[0]
    assert same(resolved(row),ode),('wrong stage',row)
  else:assert same(resolved(block),ode),('wrong displayed stage',block)
 assert separated(blocks[-1])
 return {'equivalent_ode_options':sum(same(v,ode) for v in eqs),'eligible_correct_options':len(valid)}

def fingerprint(prompt):
 ode=resolved(math_blocks(prompt)[0])
 # Canonicalize positive numeric exponential bases (4^x = 2^(2x)).
 ode=ode.replace(lambda z:z.is_Pow and z.base.is_number and z.base.is_positive,lambda z:sp.exp(z.exp*sp.expand_log(sp.log(z.base),force=True)))
 return sp.srepr(sp.simplify(ode))
