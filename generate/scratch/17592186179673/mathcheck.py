"""Independent TeX-to-SymPy checks of actual learner-facing expressions.
Restricted to this KP's captured notation; unsupported strings fail closed.
"""
import re
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
x,y,t,DX,DY,XP,YP=s.symbols('x y t DX DY XP YP',real=True)

def group(z,i):
 if z[i]!='{':raise ValueError('group expected: '+z[i:])
 depth=1;j=i+1
 while depth:
  if z[j]=='{':depth+=1
  if z[j]=='}':depth-=1
  j+=1
 return z[i+1:j-1],j

def expr(z):
 z=z.replace('\u2061','').strip().rstrip(',.')
 z=z.replace(r'\operatorname{cos}',r'\cos').replace(r'\operatorname{sin}',r'\sin')
 z=re.sub(r'\{(cos|sin)\}',lambda m:'\\'+m[1],z)
 z=z.replace(r'{x}^{′}', '(XP)').replace(r'{y}^{′}','(YP)')
 z=z.replace(r'x\prime(t)','(XP)').replace(r'y\prime(t)','(YP)')
 z=z.replace(r'\frac{dx}{\text{d}t}','(XP)').replace(r'\frac{dy}{\text{d}t}','(YP)')
 z=z.replace(r'\frac{\text{d}x}{\text{d}t}','(XP)').replace(r'\frac{\text{d}y}{\text{d}t}','(YP)')
 z=z.replace(r'\mathrm{d}x','(DX)').replace(r'\mathrm{d}y','(DY)').replace('dx','(DX)').replace('dy','(DY)')
 z=z.replace(r'\text{d}t','').replace(r'\mathrm{d}t','').replace('dt','')
 z=re.sub(r'\\(?:left|right|,|!|;|quad|displaystyle)', '', z)
 z=z.replace(r'\cdot','*').replace(r'\pi','pi')
 # Group-aware operators; leave structural products for implicit multiplication.
 while '\\frac' in z or '\\sqrt' in z:
  m=re.search(r'\\(frac|sqrt)',z);i=m.end();a,j=group(z,i)
  if m[1]=='frac':b,k=group(z,j);v='(('+str(expr(a))+')/('+str(expr(b))+'))'
  else:k=j;v='sqrt('+str(expr(a))+')'
  z=z[:m.start()]+v+z[k:]
 # e raised to an expression (must precede ordinary power processing).
 while re.search(r'\{?e\}?\^\{',z):
  m=re.search(r'\{?e\}?\^',z);a,j=group(z,m.end());z=z[:m.start()]+'(exp('+str(expr(a))+'))'+z[j:]
 # Trigonometric argument is one parenthesized group or familiar 2t/t/pi.
 pattern=r'\\(sin|cos)(?:\^\{([^{}]+)\})?\s*'
 while (m:=re.search(pattern,z)):
  i=m.end()
  if z[i]=='{':
   arg,j=group(z,i)
  elif z[i]=='(':
   dep=1;j=i+1
   while dep:
    if z[j]=='(':dep+=1
    if z[j]==')':dep-=1
    j+=1
   arg=z[i+1:j-1]
  else:
   n=re.match(r'(?:\d*)?(?:t|pi)(?:\s*/\s*\d+)?|\d+',z[i:])
   if not n:raise ValueError('trig argument '+z[i:])
   arg=n[0];j=i+len(n[0])
  power='**('+m[2]+')' if m[2] else ''
  z=z[:m.start()]+m[1]+'('+str(expr(arg))+')'+power+z[j:]
 z=z.replace('{','(').replace('}',')').replace('^','**')
 if '\\' in z or '[' in z or ']' in z:raise ValueError('unhandled TeX '+z)
 return parse_expr(z,local_dict={'x':x,'y':y,'t':t,'DX':DX,'DY':DY,'XP':XP,'YP':YP,'pi':s.pi,'sin':s.sin,'cos':s.cos,'exp':s.exp,'sqrt':s.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))

def outer_scale(z):
 # Our linearity wrapper is the only wrapper added to observed arithmetic masks.
 m=re.fullmatch(r'(-?\d+)\\left\((.*)\\right\)',z,flags=re.S)
 return (int(m[1]),m[2]) if m else (1,z)

def integral(z):
 c,z=outer_scale(z.strip());z=z.replace(r'{\int }',r'\int')
 i=z.index(r'\int');pre=z[:i].strip();j=i+len(r'\int')
 assert z[j]=='_';lo,j=group(z,j+1);assert z[j]=='^';hi,j=group(z,j+1)
 f=expr(z[j:]) if re.sub(r'\\(?:,|text\{d\}t|mathrm\{d\}t)', '', z[j:]).strip() else s.Integer(1);coef=expr(pre) if pre not in ['','-'] else (-1 if pre=='-' else 1)
 return c*coef*f,expr(lo),expr(hi)

def printed_oneform(prompt):
 z=prompt.split('$')[1].rstrip(',');c,z=outer_scale(z)
 z=z.replace(r'{\int }_{C}','').replace(r'\int_C','')
 f=c*expr(z)
 P=s.diff(f,DX);Q=s.diff(f,DY)
 if s.simplify(f-P*DX-Q*DY)!=0:raise ValueError('not linear one-form')
 return P,Q

def equivalence(a,b):return s.simplify(s.trigsimp(a-b))==0

def printed_geometry(prompt):
 parts=prompt.split('$');curve=next(z for z in parts if '=' in z and 'x' in z and 'y' in z and 'int' not in z)
 l,r=curve.split('=');pol=expr(l);rhs=expr(r)
 a=s.sqrt(rhs/s.expand(pol).coeff(x,2));b=s.sqrt(rhs/s.expand(pol).coeff(y,2))
 ends=[]
 for z in parts:
  if re.match(r'^[AB]?\(',z.strip()):
   z=re.sub(r'^[AB]?\(','',z.strip()).rstrip('.,)').replace(r'\left','').replace(r'\right','');u,v=z.split(',');ends.append((expr(u),expr(v)))
 if len(ends)!=2:raise ValueError('printed endpoints not found')
 angles=[]
 for u,v in ends:
  matches=[j for j in range(4) if equivalence(u,a*s.cos(j*s.pi/2)) and equivalence(v,b*s.sin(j*s.pi/2))]
  if len(matches)!=1:raise ValueError('endpoint not on quarter arc')
  angles.append(matches[0])
 j,k=angles
 while k<=j:k+=4
 return a,b,j*s.pi/2,k*s.pi/2

def displayed_integrand(prompt):
 P,Q=printed_oneform(prompt);a,b,lo,hi=printed_geometry(prompt)
 X,Y=a*s.cos(t),b*s.sin(t)
 f=s.simplify(P.subs({x:X,y:Y},simultaneous=True)*s.diff(X,t)+Q.subs({x:X,y:Y},simultaneous=True)*s.diff(Y,t))
 # In this source family endpoint undefined coefficients cancel continuously.
 # Any interior coefficient pole is rejected even when a formal simplification
 # might hide it; observed singular paths contain no interior coordinate zero.
 den=s.denom(s.together(P))*s.denom(s.together(Q))
 for z in [x,y]:
  if den.has(z) and s.simplify(den.subs(z,0))==0:
   zeros=[n*s.pi/2 for n in range(9) if (n%2==1 if z==x else n%2==0)]
   if any(lo<v<hi for v in zeros):raise ValueError('interior one-form pole')
 return f,lo,hi,X,Y

def stage_value(z,X,Y):
 c,z=outer_scale(z.strip())
 if r'\int' in z:
  f,lo,hi=integral(z)
  f=f.subs({x:X,y:Y,XP:s.diff(X,t),YP:s.diff(Y,t)},simultaneous=True)
  return ('integrand',s.simplify(c*f),lo,hi)
 # Evaluated antiderivative row has a final _{a}^{b} suffix.
 if '_{' in z and '^{' in z:
  i=z.rfind('_{');lo,j=group(z,i+1)
  if z[j]!='^':raise ValueError('evaluation suffix')
  hi,j=group(z,j+1)
  if z[j:].strip():raise ValueError('trailing evaluation text')
  pre=z[:i].replace(r'\left','').replace(r'\right','').replace(r'{|}','')
  if pre.startswith('{[') and pre.endswith(']}'):pre=pre[2:-2]
  elif pre.startswith('[') and pre.endswith(']'):pre=pre[1:-1]
  F=expr(pre)
  return ('primitive',c*F,expr(lo),expr(hi))
 return ('value',c*expr(z.replace('[','(').replace(']',')')))

def check_solution_rows(record,source_parts=None):
 q=record['question'];f,lo,hi,X,Y=displayed_integrand(q[':question/problem'])
 sol=q[':question/worked-solution'];bodies=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,flags=re.S)
 body=bodies[-1];rows=re.split(r'\\\\\s*&\s*=',body)
 lhs,rhs=rows[0].split(' & =',1);rows[0]=rhs
 val=None if all(r'\int' in z for z in rows) else s.simplify(s.integrate(f,(t,lo,hi)))
 checks=[]
 for row in rows:
  parsed=stage_value(row,X,Y)
  if parsed[0]=='integrand':assert equivalence(parsed[1],f),(row,parsed[1],f);assert equivalence(parsed[2],lo) and equivalence(parsed[3],hi)
  elif parsed[0]=='primitive':assert equivalence(s.diff(parsed[1],t),f),(row,parsed[1],f);assert equivalence(parsed[2],lo) and equivalence(parsed[3],hi)
  else:assert equivalence(parsed[1],val),(row,parsed[1],val)
  checks.append(parsed[0])
 return checks

def check_tangent(record):
 q=record['question'];a,b,lo,hi=printed_geometry(q[':question/problem']);X,Y=a*s.cos(t),b*s.sin(t)
 blocks=q[':question/worked-solution'].split('$$')[1::2][:2]
 for index,block in enumerate(blocks):
  body=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split('=')[-1]
  first,rest=body.split(r'\,i+',1);second=rest.split(r'\,j',1)[0]
  A,B=expr(first),expr(second)
  assert equivalence(A,X if index==0 else s.diff(X,t))
  assert equivalence(B,Y if index==0 else s.diff(Y,t))
  if index==0:
   m=re.search(r't\\in\s*\[([^\]]+)\]',body);assert m
   L,H=m[1].split(',');assert equivalence(expr(L),lo) and equivalence(expr(H),hi)
 return 3

def bank_scalar_audit(answers):
 """Exact polynomial quadrature or independent 70-digit exponential quadrature."""
 import mpmath as m
 values=[];details=[]
 for a in answers:
  f,L,H=integral(a[':answer/value'])
  if f.has(s.exp):
   with m.workdps(70):
    fn=s.lambdify(t,f,'mpmath');lo=m.mpf(str(s.N(L,75)));hi=m.mpf(str(s.N(H,75)));v=m.quad(fn,[lo,(lo+hi)/2,hi]);values.append(v);details.append({'method':'70-digit independent quadrature','value':m.nstr(v,65)})
  else:
   v=s.simplify(s.integrate(f,(t,L,H)));values.append(v);details.append({'method':'exact symbolic quadrature','value':str(v)})
 duplicates=[]
 for i in range(len(values)):
  for j in range(i):
   if isinstance(values[i],s.Basic) and isinstance(values[j],s.Basic):equal=equivalence(values[i],values[j])
   else:
    with m.workdps(70):
     u=m.mpf(str(s.N(values[i],75))) if isinstance(values[i],s.Basic) else values[i]
     v=m.mpf(str(s.N(values[j],75))) if isinstance(values[j],s.Basic) else values[j]
     equal=abs(u-v)<m.mpf('1e-50')
   if equal:duplicates.append([j,i])
 return {'values':details,'equal_complete_integrals':duplicates,'valid_unique_bank':not duplicates}
