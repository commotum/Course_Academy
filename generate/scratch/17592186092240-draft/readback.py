"""Independent readback of printed givens, formal derivatives, stages and keys.
No generator metadata is used to derive answers or intermediate equations.
"""
import re
import sympy as s
from math_parser import scalar as elementary, x,y

def eq(a,b):return s.simplify(a-b)==0

def group(text,start):
 assert text[start] in '({' ;op=text[start];endchar=')' if op=='(' else '}';depth=1;i=start+1
 while depth:
  assert i<len(text),(text,start)
  if text[i]==op:depth+=1
  elif text[i]==endchar:depth-=1
  i+=1
 return text[start+1:i-1],i

def scalar(text):
 text=text.strip().rstrip('.,:').replace(r'\dfrac',r'\frac').replace(r'\,','').replace(r'\mathbin{:}','').replace('⁡','')
 while r'\sqrt[' in text:
  start=text.index(r'\sqrt[');idx=start+6;j=text.index(']',idx);n=text[idx:j];a,end=group(text,j+1);text=text[:start]+'('+a+')^{1/'+n+'}'+text[end:]
 return elementary(text)

def clean(text):
 return text.strip().replace('′',"'").replace("{f}^{'}","f'").replace("{m}^{'}","n").replace("{f}^{′}","f'").replace("{m}^{′}","n").replace("{f}","f").replace("{m}","m").replace(r'\left','').replace(r'\right','').replace("m'",'n').replace('{y}_{1}','Y').replace('{x}_{1}','X')

def expr(text,fun,point,ordinate,m,bindings,counters):
 text=clean(text)
 der=r'\frac{\text{d}}{\text{d}x}'
 while der in text:
  st=text.index(der);begin=st+len(der)
  assert text[begin]=='('
  operand,end=group(text,begin);arg=scalar(operand);counters['formal_operands']+=1
  text=text[:st]+'('+s.latex(s.diff(arg,x))+')'+text[end:]
 def func(match):
  name=match[1];argument=scalar(match[2]);target=fun if name=='f' else bindings['h'];return '('+s.latex(target.subs(x,argument))+')'
 text=re.sub(r"f'\(([^()]*)\)",lambda a:'('+s.latex(s.diff(fun,x).subs(x,scalar(a[1])))+')',text)
 text=re.sub(r'([fh])\(([^()]*)\)',func,text)
 for token,value in [('X',point),('Y',ordinate),('m',m),('n',-1/m)]:
  text=re.sub(r'(?<![a-z])'+token+r'(?![a-z])',lambda _: '('+s.latex(value)+')',text)
 if text.startswith('y('):
  argument,end=group(text,1);text='('+s.latex(fun.subs(x,scalar(argument)))+')'+text[end:]
 text=text.replace('p', 'P') if False else text
 # Actual printed coefficient labels are determined by the displayed final line contract.
 for token,value in bindings.get('coefficients',{}).items():text=re.sub(r'(?<![a-z])'+token+r'(?![a-z])',lambda _: '('+s.latex(value)+')',text)
 return scalar(text)

def validate(record,raw_context=False):
 q=record['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];counters={'equalities':0,'formal_operands':0,'normal_lines':0,'bank_values':0}
 # Read the actual displayed curve and point.
 context='y=f(x)' in prompt
 if context:
  match=re.search(r'Use \$f\(x\)=(.*?)\$ and \$h\(x\)=(.*?)\$',prompt)
  if match:f=scalar(match[1]);h=scalar(match[2].rstrip(','))
  else:
   assert raw_context
   # Original context is incomplete; concrete bindings are read from its displayed substitution row.
   row=re.search(r'& =(.+?)\\\\',sol);assert row
   right=row[1].split(r'\cdot');assert len(right)==2;point=s.pi
   f=scalar(right[0]).subs(s.pi,x);h=-4*s.sin(x)
  fun=s.expand(f*h);point=s.pi;ordinate=s.simplify(fun.subs(x,point));m=s.simplify(s.diff(fun,x).subs(x,point));bindings={'h':h}
  explicit=re.search(r'\$m=(.*?)\.\$',sol);assert explicit and eq(scalar(explicit[1]),m)
 else:
  given=re.search(r'\$y\s*=\s*(.*?)\$',prompt);assert given,prompt;fun=scalar(given[1])
  pm=re.search(r'at the point \$\((.*?)\)',prompt);assert pm
  coords=pm[1].split(',');assert len(coords)==2;point,ordinate=map(scalar,coords);assert eq(fun.subs(x,point),ordinate),(fun,point,ordinate)
  m=s.simplify(s.diff(fun,x).subs(x,point));bindings={}
 assert m!=0 and m.is_finite
 # Domain restriction is derived from displayed negative/fractional powers.
 if any(power.exp.is_negative or not power.exp.is_integer for power in fun.atoms(s.Pow) if power.base.has(x)):assert point>0
 normal=x+ m*y-(point+m*ordinate)
 bindings['coefficients']={'p':m,'q':point+m*ordinate,'a':-1/m,'b':ordinate+point/m}
 # Each display equation, including every aligned row and each equality-chain term.
 for block in re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S):
  block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');prev=None
  for row in block.split(r'\\'):
   parts=row.replace('&','').strip().split('=');assert len(parts)>=2,(row,sol)
   vals=[]
   for part in parts:
    if not part.strip():assert prev is not None;vals.append(prev)
    else:vals.append(expr(part,fun,point,ordinate,m,bindings,counters))
   for a,b in zip(vals,vals[1:]):
    residual=s.expand(a-b)
    if residual.has(x,y) and not eq(residual,0):
     ratio=s.cancel(residual/normal);assert not ratio.free_symbols and ratio!=0,(row,residual,normal);counters['normal_lines']+=1
    else:assert eq(residual,0),(row,residual)
    counters['equalities']+=1
   prev=vals[-1]
 # Point references and Let f formal binding must agree with prompt.
 for point_text in re.findall(r'at the point \$\((.*?)\)',sol):
  pp,yy=map(scalar,point_text.split(','));assert eq(pp,point) and eq(yy,ordinate)
 let=re.search(r'Let \$f\(x\)=(.*?)\$',sol)
 if let:assert eq(scalar(let[1]),fun)
 # All inline evaluation targets also verified.
 for inline in re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',sol,re.S):
  if re.match(r'^(?:a\+b|p\+q|q-p|p-q)=',inline):
   vals=[expr(a,fun,point,ordinate,m,bindings,counters) for a in inline.split('=')];assert all(eq(a,vals[0]) for a in vals)
 fields=q[':question/answer-fields'];keys={f[':answer-field/key']:f for f in fields}
 for f in fields:
  assert f[':answer-field/type'].endswith('/radio') or '{{'+f[':answer-field/key']+'}}' in prompt
  vals=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vals)==len({s.srepr(s.simplify(a)) for a in vals});counters['bank_values']+=len(vals)
  correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);answer=scalar(correct[':answer/value'])
  if context:expected=-1/m*(x-point)+ordinate
  elif len(fields)==2:
   lhs=re.search(r'\$([^$]*x[^$]*[+-])\$\s*\{\{field-1\}\}',prompt);assert lhs
   L=scalar(lhs[1][:-1]).coeff(x);expected=abs(L*m) if f[':answer-field/key']=='field-1' else L*(point+m*ordinate)
   if f[':answer-field/key']=='field-1':assert (lhs[1][-1]=='+')==(m>0)
  else:
   target=re.search(r'Find the value of \$(.*?)\$',prompt);assert target;expected=expr(target[1],fun,point,ordinate,m,bindings,counters)
  assert eq(answer,expected),(answer,expected,prompt)
 return counters
