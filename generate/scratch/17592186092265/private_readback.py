"""Independent printed-math reader. Never imports generator or its computations."""
import sys
sys.dont_write_bytecode=True
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('kp92265_private_scalar',Path(__file__).with_name('private_scalar.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
x=p.x;u=p.u

def group(z,i,opening='{',closing='}'):
 assert z[i]==opening,(z,i);j=i+1;depth=1
 while depth:
  assert j<len(z),(z,i);depth+=(z[j]==opening)-(z[j]==closing);j+=1
 return z[i+1:j-1],j

def scalar(z):
 z=z.strip().rstrip('.,').replace('⁡','').replace('−','-').replace(r'\left','').replace(r'\right','').replace(r'\!','').replace(r'\quad','').replace(r'\,','')
 z=z.replace(r'\operatorname{ln}',r'\ln').replace(r'\operatorname{log}',r'\log').replace('{log}',r'\log')
 z=re.sub(r'(?<![A-Za-z\\])ln',lambda _:r'\ln ',z);z=re.sub(r'(?<![A-Za-z\\])log',lambda _:r'\log ',z)
 while r'\cancel{' in z:
  i=z.index(r'\cancel{');body,end=group(z,i+len(r'\cancel'));z=z[:i]+'('+body+')'+z[end:]
 while r'\log' in z:
  i=z.index(r'\log');j=i+4;base='10'
  if z[j:j+1]=='_':
   j+=1
   if z[j]=='{':base,j=group(z,j)
   else:base=z[j];j+=1
  while z[j:j+1].isspace():j+=1
  if z[j]=='(':body,end=group(z,j,'(',')')
  elif z[j]=='{':body,end=group(z,j)
  else:body=z[j];end=j+1
  z=z[:i]+r'\frac{\ln('+body+r')}{\ln('+base+')}' +z[end:]
 return p.scalar(z.removeprefix('.'))

def eq(a,b):return s.simplify(a-b)==0

def actual(q):
 md=q[':question/problem'];sol=q[':question/worked-solution']
 match=re.search(r'\$(?:y|f\(x\))\s*=\s*(.*?)\$',md);assert match,md
 f=scalar(match[1].rstrip('.,'));der=s.diff(f,x);pointmatch=re.search(r'where \$x=(.*?)\$',md);point=scalar(pointmatch[1]) if pointmatch else None
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==(4 if point is not None else 3)
 comp=blocks[0].strip().rstrip('.')
 # Original captures contain f'(x)=log(u), a documented typo, never served.
 left,right=comp.split('=',1);outer,inner=re.split(r',\s*(?:\\quad|\\,)\s*u=',right)
 inside=scalar(inner);outers=outer.split('=');outside=scalar(outers[-1]);assert all(eq(scalar(v),outside) for v in outers)
 assert eq(outside.subs(u,inside),f),('composite wrong operand',f,inside,outside)
 pair=blocks[1].strip().rstrip('.')
 parts=re.split(r',\s*(?:\\quad|\\,)\s*',pair);assert len(parts)==2,pair
 outsidevalues=parts[0].split('=')[1:];insidevalues=parts[1].split('=')[1:]
 for z in outsidevalues:assert eq(scalar(z),s.diff(outside,u)),('outer derivative',z,outside)
 for z in insidevalues:assert eq(scalar(z),s.diff(inside,x)),('inner derivative',z,inside)
 # Read actual D-symbol operands in the formal first chain row, then all RHS rows.
 chain=blocks[2].split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0];rows=chain.split(r'\\')
 first=rows[0];expected_lhs=r'\frac{\mathrm{d}'+('f' if left.startswith('f') else 'y')+r'}{\mathrm{d}x}'
 assert first.split('&')[0].strip()==expected_lhs,('stale target',first,expected_lhs)
 formal=first.split('&=')[1].strip().rstrip('.')
 assert formal==r'\frac{\mathrm{d}'+('f' if left.startswith('f') else 'y')+r'}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}',formal
 count=0
 for row in rows[1:]:
  rhs=row.split('&=')[1].strip().rstrip('.');rhs=rhs.replace('u','('+s.latex(inside)+')');value=scalar(rhs)
  assert eq(value,der),('printed chain stage',rhs,value,der);count+=1
 answer=s.simplify(der.subs(x,point)) if point is not None else der
 if point is not None:
  assert inside.subs(x,point)>0,('domain',inside,point)
  ev=blocks[3].split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0];evrows=ev.split(r'\\')
  assert 'x='+s.latex(point).replace(r'\left','').replace(r'\right','') in evrows[0]
  for row in evrows:
   rhs=row.split('&=')[1].strip().rstrip('.')
   if '|' in rhs:
    raw,bar=rhs.split('|',1);raw=raw.replace(r'\right','').replace(r'\left','');marked=group(bar,bar.index('_{')+1)[0][2:];assert eq(scalar(marked),point);value=scalar(raw).subs(x,point)
   else:value=scalar(rhs)
   assert eq(value,answer),('tangent evaluation',rhs,value,answer);count+=1
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];values=[scalar(a[':answer/value']) for a in choices]
 correct=[a for a in choices if a[':answer/id']==field[':answer-field/correct'][1]];assert len(correct)==1 and eq(scalar(correct[0][':answer/value']),answer)
 if field[':answer-field/type'].endswith('/radio'):
  assert len(values)==5 and sum(eq(z,answer) for z in values)==1
  for i,z in enumerate(values):
   for other in values[i+1:]:assert not eq(z,other),('bank collision',z,other)
 else:assert len(values)==1 and '{{field-1}}' in md
 assert not inside.equals(0)
 return {'function':str(f),'inner':str(inside),'point':str(point),'answer':str(answer),'printed_stages':count,'choices':len(values),'domain':'inner>0; radical real where present','pole_denominator':str(s.denom(s.cancel(der)))}
