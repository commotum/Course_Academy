"""Root strict reader for printed linear ODEs, integrating factors and solution families."""
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('parent_ode_base',Path(__file__).with_name('one-form-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
x,y,C,YP=p.x,p.y,p.p.z,p.p.v

def scalar(raw):
 raw=raw.replace('\\\\','\\').replace(r'\u2061','').replace('⁡','').strip().rstrip('.,')
 raw=raw.replace(r'\frac{\text{d}y}{\text{d}x}','v').replace(r'\frac{dy}{dx}','v').replace(r'\frac{\mathrm{d}y}{\mathrm{d}x}','v').replace(r'\ln |x|',r'\ln x').replace('C','z')
 return p.scalar(raw)
def equation(raw):
 raw=raw.split(',')[0].strip().rstrip('.,');lhs,rhs=raw.split('=');return s.expand(scalar(lhs)-scalar(rhs))
def ode(text):
 body=next(v for v in p.blocks(text) if '=' in v and any(z in v for z in (r'\frac{dy}',r'\frac{\text{d}y}',r'\frac{\mathrm{d}y}')))
 e=equation(body);A=e.coeff(YP);B=e.coeff(y);D=s.simplify(e-A*YP-B*y);assert A!=0 and not D.has(y,YP);return s.simplify(B/A),s.simplify(-D/A)
def transformed(raw):
 raw=raw.replace('\\\\','\\').replace(r'\u2061','').replace('⁡','').strip().rstrip('.,');lhs,rhs=raw.split('=');prefix=next(z for z in (r'\frac{d}{dx}',r'\frac{\text{d}}{\text{d}x}') if lhs.startswith(z));body=lhs[len(prefix):];f=scalar(body);I=s.expand(f).coeff(y);assert p.equivalent(f,y*I) and I!=0
 return s.diff(I,x)/I,s.simplify(scalar(rhs)/I)
def same_transformation(a,b):return all(p.equivalent(z,w) for z,w in zip(transformed(a),transformed(b)))
def solution(raw):
 v=scalar(raw);poly=s.Poly(s.expand(v),C);assert poly.degree()<=1;return poly.coeff_monomial(1),poly.coeff_monomial(C)
def valid_solution(raw,P,Q):
 a,b=solution(raw);return b!=0 and p.equivalent(s.diff(a,x)+P*a,Q) and p.equivalent(s.diff(b,x)+P*b,0)
def same_family(raw1,raw2):
 a,b=solution(raw1);d,e=solution(raw2)
 if b==0 or e==0:return b==e==0 and p.equivalent(a,d)
 ratio=s.simplify(b/e);offset=s.simplify((a-d)/e);return not ratio.has(x) and ratio!=0 and not offset.has(x)
def same_factor(raw1,raw2):
 ratio=s.simplify(scalar(raw1)/scalar(raw2));return ratio!=0 and not ratio.has(x)

def expanded_equation(raw):
 raw=raw.strip().rstrip('.,').replace('\\\\','\\').replace(r'\u2061','').replace('⁡','');raw=raw.replace(r'\left','').replace(r'\right','');lhs,rhs=raw.split('=')
 for prefix in (r'\frac{d}{dx}',r'\frac{\text{d}}{\text{d}x}'):
  if prefix in lhs:
   j=lhs.index(prefix);pre=lhs[:j];start=j+len(prefix);body,k=p.group(lhs,start);assert not lhs[k:].strip();v=scalar(body);I=s.expand(v).coeff(y);assert p.equivalent(v,y*I)
   z=scalar(pre) if pre.strip() else s.Integer(1);lhs_expr=z*(y*s.diff(I,x)+YP*I);break
 else:lhs_expr=scalar(lhs)
 e=s.expand(lhs_expr-scalar(rhs));A=e.coeff(YP);B=e.coeff(y);D=s.simplify(e-A*YP-B*y);assert A!=0 and not D.has(YP,y)
 return s.simplify(B/A),s.simplify(-D/A)
def positive_equal(a,b):
 a,b=map(s.sympify,(a,b));xx=s.Symbol('positive_x',positive=True);return p.equivalent(s.powdenest(a.subs(x,xx),force=True),s.powdenest(b.subs(x,xx),force=True))
def integrating_stage(raw,P):
 # An indefinite exponent integral selects a representative primitive; the
 # nonzero constant multiplier is irrelevant to the integrating factor.
 raw=raw.strip().rstrip('.,').replace(r'\text{d}x','dx').replace('P(x)','('+s.latex(P)+')');raw=raw.replace(r'\int P(x)\,dx',s.latex(s.integrate(P,x)))
 if r'\int' in raw:
  a=raw.index(r'\int')+4;b=raw.index('dx',a);term=raw[a:b].replace(r'\,','');raw=raw[:a-4]+s.latex(s.integrate(scalar(term),x))+raw[b+2:]
 return scalar(raw)
def stages(text,P,Q,solve=False):
 text=resolve_u(text)
 counts={'named_coefficients':0,'integrating_factor_rows':0,'equation_rows':0,'solution_rows':0}
 for b in p.blocks(text):
  b=p.clean(b)
  if b.startswith(('P(x)=','Q(x)=')):
   
   for segment in b.replace(r'\,','').split(','):
    name,body=segment.split('=',1);assert positive_equal(scalar(body),P if name=='P(x)' else Q);counts['named_coefficients']+=1
  if b.startswith('I(x)') and '=' in b:
   rows=re.split(r'\\\\\s*=?\s*',b)
   for row in rows:
    row=row.split('=')[-1].strip();I=integrating_stage(row,P);assert positive_equal(s.diff(I,x),P*I),(row,P,I);counts['integrating_factor_rows']+=1
  elif '=' in b and ('frac{dy}' in b or 'frac{\\text{d}y}' in b or 'frac{d}{dx}' in b or 'frac{\\text{d}}{\\text{d}x}' in b):
   if 'P(x)' in b or 'I(x)' in b:continue
   for row in b.split(r'\\'):
    if r'\int' in row or ('C' in row and 'y' in row):continue
    actual=expanded_equation(row.strip());assert all(positive_equal(z,w) for z,w in zip(actual,(P,Q))),(row,actual,P,Q);counts['equation_rows']+=1
  if solve and '=' in b and 'y' in b and 'C' in b:
   for row in b.split(r'\\'):
    if r'\int' in row or 'C' not in row:continue
    lhs,rhs=row.split('=',1)
    if lhs.strip().startswith('y(') or 'y' not in lhs:continue
    L=scalar(lhs);R=scalar(rhs);coef=s.expand(L).coeff(y);assert coef!=0;candidate=s.simplify((R-(L-coef*y))/coef);a=s.expand(candidate).coeff(C,0);c=s.expand(candidate).coeff(C);assert c!=0 and positive_equal(s.diff(a,x)+P*a,Q) and positive_equal(s.diff(c,x)+P*c,0),(row,candidate);counts['solution_rows']+=1
 return counts

def remove_integrals(raw):
 raw=raw.replace(r'\text{d}x','dx').replace(r'\mathrm{d}x','dx')
 while r'\int' in raw:
  j=raw.index(r'\int');start=j+4;end=raw.index('dx',start);body=raw[start:end].replace(r'\,','').strip()
  if r'\frac{d}{dx}' in body or r'\frac{\text{d}}{\text{d}x}' in body:
   # Normalize differential marker earlier only affected textd derivative dx.
   prefix=next(z for z in (r'\frac{d}{dx}',r'\frac{\text{d}}{dx}') if body.startswith(z));v,k=p.group(body,len(prefix));assert not body[k:].strip();F=scalar(v)
  else:F=s.integrate(scalar(body),x)
  raw=raw[:j]+'('+s.latex(F).replace('z','C')+')'+raw[end+2:]
 return raw

def antiderivative_rows(text,P,Q):
 text=resolve_u(text)
 count=0
 for b in p.blocks(text):
  b=p.clean(b)
  if not '=' in b or 'y' not in b:continue
  rows=b.split(r'\\')
  for row in rows:
   if '=' not in row:continue
   lhs,rhs=row.split('=',1)
   if lhs.strip().startswith('y('):continue
   if 'y' not in lhs or not (r'\int' in rhs or 'C' in rhs):continue
   if r'\int' in lhs:continue
   L=scalar(lhs);coef=s.expand(L).coeff(y);assert coef!=0 and p.equivalent(L,coef*y)
   if not positive_equal(s.diff(coef,x),P*coef):
    assert lhs.strip()=='y' and 'C' in rhs;continue
   primitive=scalar(remove_integrals(rhs));assert positive_equal(s.diff(primitive,x),coef*Q),(row,primitive,coef,Q)
   assert positive_equal(s.diff(coef,x),P*coef);count+=1
 return count

def initial(text):
 for b in p.blocks(text):
  matches=list(re.finditer(r'y\(',b))
  for match in reversed(matches):
   point,j=p.group(b,match.end()-1)
   if point=='x':continue
   rest=b[j:].strip()
   if not rest.startswith('='):continue
   value=rest[1:].split(',')[0].strip().rstrip('.,');return scalar(point),scalar(value)
 raise AssertionError(('No initial condition',text))
def initial_rows(text,P,Q,point,y0):
 general=[]
 for b in p.blocks(text):
  for row in p.clean(b).split(r'\\'):
   if '=' not in row:continue
   lhs,rhs=row.split('=',1)
   if lhs.strip()=='y' and 'C' in rhs:general.append(scalar(rhs))
 assert general,text
 G=general[-1];a,b=solution(s.latex(G).replace('z','C'));constant=s.simplify((y0-a.subs(x,point))/b.subs(x,point));assert not constant.has(x,C);counts={'initial_condition_rows':0,'particular_solution_rows':0}
 for block in p.blocks(text):
  block=p.clean(block)
  if re.match(r'y\(',block) and '=' in block:
   rows=block.split(r'\\')
   for row in rows:
    lhs,rhs=row.split('=',1);rhs=scalar(rhs).subs(C,constant)
    if lhs.strip().startswith('y('):
     z,k=p.group(lhs.strip(),1);assert positive_equal(scalar(z),point);L=y0
    else:L=scalar(lhs).subs(C,constant)
    assert positive_equal(L,rhs),(row,constant,point,y0);counts['initial_condition_rows']+=1
  elif re.match(r'y\s*=',block) and 'C' not in block:
   for row in block.split(r'\\'):
    Y=scalar(row.split('=',1)[1]);assert positive_equal(s.diff(Y,x)+P*Y,Q) and positive_equal(Y.subs(x,point),y0);counts['particular_solution_rows']+=1
 assert counts['initial_condition_rows']>=3 and counts['particular_solution_rows']>=1,counts
 return counts

def resolve_u(text):
 definitions=[b for b in p.blocks(text) if b.strip().startswith('u=') and ',' not in b]
 if not definitions:return text
 assert len(definitions)==1;U=scalar(definitions[0].split('=',1)[1].rstrip(':'));assert U.free_symbols<={x};dU=s.diff(U,x)
 def replace(match):
  raw=match.group();raw=raw.replace(r'\text{d}u','('+s.latex(dU)+r')\text{d}x').replace(r'\mathrm{d}u','('+s.latex(dU)+r')\mathrm{d}x')
  return re.sub(r'\bu\b',lambda _: '('+s.latex(U)+')',raw)
 return p.MATH.sub(replace,text)

def ibp_variables(text):
 definitions=[b for b in p.blocks(text) if b.startswith('u=') and '{v}^{′}=' in b]
 if not definitions:return 0
 assert len(definitions)==1;parts=definitions[0].rstrip(',').split(',');assert len(parts)==3 and parts[0].startswith('u=') and parts[1].startswith('{u}^{′}=') and parts[2].startswith('{v}^{′}=')
 U=scalar(parts[0].split('=',1)[1]);dU=scalar(parts[1].split('=',1)[1]);dV=scalar(parts[2].split('=',1)[1]);V=scalar(next(b for b in p.blocks(text) if b.startswith('v=')).split('=',1)[1]);assert positive_equal(s.diff(U,x),dU) and positive_equal(s.diff(V,x),dV);return 1
