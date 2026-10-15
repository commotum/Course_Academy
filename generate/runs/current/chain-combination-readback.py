"""Root reader for actual product/quotient givens, formal operands and equations."""
import importlib.util,re
from pathlib import Path
import sympy as s
z=importlib.util.spec_from_file_location('root_combo_scalar',Path(__file__).with_name('trig-chain-readback.py'));P=importlib.util.module_from_spec(z);z.loader.exec_module(P)
x,t,u,v=P.x,P.P.t,P.u,P.P.v
a=s.Symbol('a',positive=True);P.P.locals_['a']=a
def clean(raw):
 text=P.clean(raw).replace(r'\text{⧸}','')
 text=re.sub(r'\{([xfgyhuv])\}',r'\1',text)
 return text
def scalar(raw):return P.scalar(clean(raw))
def eq(a1,b1):
 delta=s.expand(a1-b1)
 if delta==0:return True
 # Exact rational cancellation after reciprocal-trig identities is cheaper
 # than general trigonometric simplification for most printed chain stages.
 delta=delta.replace(s.tan,lambda z:s.sin(z)/s.cos(z)).replace(s.cot,lambda z:s.cos(z)/s.sin(z)).replace(s.sec,lambda z:1/s.cos(z)).replace(s.csc,lambda z:1/s.sin(z))
 rational=s.cancel(delta)
 if rational==0:return True
 for q in (s.Rational(1,3),s.Rational(1,2)):
  test=delta.subs({x:q,t:q,a:2,u:3,v:5})
  if test.is_finite is not False:
   try:
    if abs(complex(test.evalf(45)))>1e-30:return False
   except (TypeError,ValueError):pass
 numerator=s.fraction(rational)[0]
 # Prove Pythagorean identities algebraically without expanding large phase
 # angles. Each distinct displayed angle gets its own sine/cosine variables.
 angles={node.args[0] for node in numerator.atoms(s.sin,s.cos)}
 substitutions={};cosines=[]
 for n,angle in enumerate(sorted(angles,key=s.srepr)):
  sn,cn=s.symbols(f'root_sine_{n} root_cosine_{n}');substitutions[s.sin(angle)]=sn;substitutions[s.cos(angle)]=cn;cosines.append((sn,cn))
 reduced=s.expand(numerator.xreplace(substitutions))
 for sn,cn in cosines:
  if reduced.is_polynomial(cn):
   poly=s.Poly(reduced,cn);reduced=s.expand(sum(coef*(1-sn**2)**(power[0]//2)*cn**(power[0]%2) for power,coef in poly.terms()))
 if reduced==0:return True
 return P.eq(a1,b1)
def givens(prompt):
 text=clean(prompt);m=re.search(r'\$(?:y|f\(x\)|x\(t\))\s*=\s*(.*?)\$',text);assert m,prompt
 fun=scalar(m[1].split(',')[0]);var=t if 'x(t)' in m[0] else x
 point=re.search(r'at \$x\s*=\s*(.*?)\$',text)
 if not point:point=re.search(r"[fy](?:\^\{\x27\}|\x27)\(([^x][^)]*)\)",text)
 at=scalar(point[1]) if point else None
 return fun,var,at
def definitions(sol,var):
 text=clean(sol);found={name:scalar(raw) for name,raw in re.findall(r'\$([uvgh])\([xt]\)=(.*?)\$',text)}
 assert len(found)==2,(sol,found)
 return found
def value(raw,defs,var,at):
 text=clean(raw).strip().rstrip('.,');evaluate=None
 # Read concrete evaluation targets before replacing their operators.
 m=re.search(r'\|\}?_\{?x=(.*?)\}?$',text)
 if m:
  assert at is not None
  target=scalar(m[1]);assert eq(target,at),(target,at)
  text=text[:m.start()].rstrip('}')
  if text.startswith('{('):text=text[1:]
  evaluate=at
 def named(m):
  name,isprime,arg=m[1],bool(m[2]),scalar(m[3]);assert name in defs
  if arg!=var:assert at is not None and eq(arg,at),(name,arg,at)
  f=defs[name];result=s.diff(f,var) if isprime else f
  return '('+s.latex(result.subs(var,arg)).replace(r'\log',r'\ln')+')'
 names=''.join(n for n in defs if n!='x' or var==t)
 text=re.sub(r"(["+names+r"])(?:\^\{(')\}|('))?\((.*?)\)",lambda m:named(type('Match',(),{'__getitem__':lambda self,i: [None,m[1],m[2] or m[3],m[4]][i]})()),text)
 def formal(m):
  name=m[1];assert m[2]==str(var) and name in defs
  return '('+s.latex(s.diff(defs[name],var)).replace(r'\log',r'\ln')+')'
 text=re.sub(r'\\frac\{\\mathrm\{d\}([fyx])\}\{\\mathrm\{d\}([xt])\}',formal,text)
 text=re.sub(r"([fy])(?:\^\{\x27\}|\x27)",lambda m:'('+s.latex(s.diff(defs[m[1]],var)).replace(r'\log',r'\ln')+')',text)
 if text=='m':assert at is not None;return s.diff(defs['f'],var).subs(var,at)
 result=scalar(text)
 return result.subs(var,evaluate) if evaluate is not None else result
def stages(sol,fun,var,at,quotient=False):
 defs=definitions(sol,var);names=list(defs);first,second=[defs[n] for n in names]
 assert eq(first/second if quotient else first*second,fun),(first,second,fun)
 defs.update(f=fun,y=fun,x=fun)
 blocks=re.findall(r'\$\$(.*?)\$\$',clean(sol),re.S);count=0;formal=0
 for block in blocks:
  carry=None
  for row in block.split(r'\\'):
   for equation in row.replace('&','').strip().rstrip('.,').split(','):
    parts=equation.split('=')
    if len(parts)<2:continue
    if not parts[0].strip():assert carry is not None;parts[0]=carry
    else:carry=parts[0]
    values=[value(z,defs,var,at) for z in parts]
    assert all(eq(z,values[0]) for z in values[1:]),(row,values)
    count+=len(values)-1;formal+=int("'" in clean(row) or r'\frac{\mathrm{d}' in clean(row))
 return count,formal
def blank(prompt,answer,fun,var,at):
 text=clean(prompt).split('\n\n',1)[1].replace('{{field-1}}','('+answer+')').replace('$','')
 if '| --- |' in text:
  rows=[r for r in text.splitlines() if r.startswith('|')];num=rows[0].split('|')[3].strip();den=rows[2].split('|')[3].strip();rhs='('+num+')/('+den+')'
 else:rhs=text.split('=',1)[1].replace('\n','')
 assert eq(scalar(rhs),s.diff(fun,var).subs(var,at) if at is not None else s.diff(fun,var)),(rhs,fun)
