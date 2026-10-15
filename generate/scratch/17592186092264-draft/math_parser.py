"""Private fail-closed printed-TeX reader. Does not import generator/capture code.
Real x is unrestricted: logarithm domains are solved from actual arguments.
"""
import re
import sympy as s
X,U,Y=s.symbols('x u y',real=True)
BASE={'x':X,'u':U,'y':Y,'m':s.Symbol('m',real=True),'f':s.Symbol('f'),'g':s.Symbol('g'),'x_1':s.Symbol('x_1'),'y_1':s.Symbol('y_1')}
def scalar(raw,extra=None):
 text=raw.strip().rstrip('.,').replace('⁡','').replace('−','-').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\qquad','').replace(r'\cdot','*').replace(r'\dfrac',r'\frac')
 text=re.sub(r'\\operatorname\{(ln|log)\}',r'\1',text).replace('\\','')
 text=text.replace('{x}_{1}','x_1').replace('{y}_{1}','y_1').replace('x_{1}','x_1').replace('y_{1}','y_1')
 loc=dict(BASE);loc.update(extra or {})
 names=sorted(loc,key=len,reverse=True)
 pat=r'frac|sqrt|cancel|ln|log|'+ '|'.join(map(re.escape,names))+r'|\d+(?:\.\d+)?|[{}()+\-*/^]'
 tokens=re.findall(pat,text)
 if re.sub(r'\s+','',text)!=''.join(tokens):raise ValueError(('Unparsed printed math',text,tokens))
 pos=0
 def peek():return tokens[pos] if pos<len(tokens) else None
 def eat(tok=None):
  nonlocal pos
  a=peek()
  if a is None or tok is not None and tok!=a:raise ValueError((text,'expected',tok,'got',a))
  pos+=1;return a
 def group():
  o=eat();close={'{':'}','(':')'}[o];z=add();eat(close);return z
 def atom():
  z=peek()
  if z in ('+','-'):eat();return atom()*(1 if z=='+' else -1)
  if z in ('{','('):v=group()
  elif z=='frac':eat();a=group() if peek() in ('{','(') else atom();b=group() if peek() in ('{','(') else atom();v=a/b
  elif z in ('cancel','sqrt'):eat();a=group() if peek() in ('{','(') else atom();v=a if z=='cancel' else s.sqrt(a)
  elif z in ('ln','log'):
   eat();coef=peek() is not None and bool(re.fullmatch(r'\d+',peek()));a=group() if peek()=='(' else atom()
   if coef and peek() in ('x','u','{'):a*=atom()
   v=s.log(a)
  elif z in loc:eat();v=loc[z]
  elif z is not None and re.fullmatch(r'\d+(?:\.\d+)?',z):eat();v=s.Rational(z)
  else:raise ValueError((text,'bad atom',z))
  if peek()=='^':eat();v=v**atom()
  return v
 def mul():
  v=atom()
  while peek() not in (None,'+','-',')','}'):
   if peek() in ('*','/'):op=eat();w=atom();v=v*w if op=='*' else v/w
   else:v*=atom()
  return v
 def add():
  v=mul()
  while peek() in ('+','-'):op=eat();w=mul();v=v+w if op=='+' else v-w
  return v
 v=add()
 if pos!=len(tokens):raise ValueError('Unconsumed math')
 return v

def equal(a,b):return s.simplify(a-b)==0
def function(prompt):
 m=re.search(r'\$([fg])\(x\)\s*=\s*(.*?)\$',prompt)
 if not m:raise ValueError('Missing printed function')
 return m[1],scalar(m[2]),m[2]
def inner_function(raw):
 # Read the logarithm operand, retaining the exact real-domain restriction.
 text=raw.replace(r'\operatorname{ln}',r'\ln').replace('⁡','')
 pos=text.index('ln')+2;prefix=text[:pos-2].rstrip('\\').strip();c=scalar(prefix) if prefix else s.Integer(1)
 arg=scalar(text[pos:]);return c,arg

def derivative_tokens(raw,name):
 text=raw
 # Formal derivatives are evaluated from the actual printed prompt and
 # composite assignment. A stale/foreign dependent variable fails closed.
 pat=r'\\(?:d?frac)\{\\(?:text|textrm|mathrm)\{d\}([fgu]?)\}\{\\(?:text|textrm|mathrm)\{d\}([xu])\}'
 def replace(m):
  pair=(m[1],m[2]);valid={(name,'x'):'DX',(name,'u'):'DU',('u','x'):'UX'}
  if pair not in valid:raise ValueError(('Wrong formal D operand',pair,name))
  return valid[pair]
 text=re.sub(pat,replace,text)
 # Legacy df/dx with unwrapped letters used in the source prompt.
 text=text.replace(r'\frac{d'+name+r'}{dx}','DX')
 if re.search(r'\\(?:d?frac)\{[^}]*d',text):raise ValueError('Unrecognized derivative operator')
 return text

def evaluated(text,loc,expected_point=None):
 text=text.replace(r'\left.','').replace(r'\right','').replace(r'{|}', '|')
 text=re.sub(r'\|\}(_\{x=)',r'}|\1',text)
 count=0
 while '|_{x=' in text:
  at=text.index('|_{x=');end=text.index('}',at);point=scalar(text[at+5:end],loc)
  if expected_point is not None and point!=expected_point:raise ValueError('Stale printed evaluation target')
  start=at-1
  while start>=0 and text[start].isspace():start-=1
  if text[start] in '})':
   closer=text[start];opener='{' if closer=='}' else '(';depth=1;start-=1
   while start>=0 and depth:
    if text[start]==closer:depth+=1
    if text[start]==opener:depth-=1
    start-=1
   start+=1
  else:
   while start>=0 and (text[start].isalnum() or text[start]=='_'):start-=1
   start+=1
  operand=text[start:at].strip();key='EV'+str(count);count+=1
  value=scalar(operand,loc).subs(X,point)
  loc[key]=value;text=text[:start]+key+text[end+1:]
 return text

def split_stages(block):
 block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
 # Keep rows as actual equations: whole line equations, not isolated sides.
 rows=block.split(r'\\');out=[];lhs=None
 for row in rows:
  parts=[p.strip().rstrip('.,') for p in row.split('=')]
  if len(parts)<2:raise ValueError(('Missing equality stage',row))
  if parts[0]:lhs=parts[0]
  if lhs is None:raise ValueError('Missing initial left side')
  out.append([lhs]+parts[1:])
 return out

def read_record(record):
 q=record['question'];prompt=q[':question/problem'];solution=q[':question/worked-solution'];name,fun,raw=function(prompt);c,inner=inner_function(raw)
 domain=s.solve_univariate_inequality(inner>0,X,relational=False);der=s.diff(fun,X)
 point=None;kind='derivative'
 if 'tangent to the curve' in prompt:
  if 'Find the slope' in prompt:
   m=re.search(r'\$x=(.*?)\$',prompt);point=scalar(m[1]);kind='slope'
  else:
   m=re.search(r'at the point \$\((.*)\)\.\$',prompt);px,py=m[1].split(',',1);point=scalar(px);given_y=scalar(py);kind='tangent'
   if not equal(given_y,fun.subs(X,point)):raise ValueError('Supplied tangent point is off the curve')
  if inner.subs(X,point)<=0:raise ValueError('Printed target outside actual logarithm domain')
 target=der if point is None else s.simplify(der.subs(X,point))
 yp=fun.subs(X,point) if point is not None else None
 line=Y-(target*(X-point)+yp) if kind=='tangent' else None
 loc={'DX':der,'DU':c/U,'UX':s.diff(inner,X),name:fun,'u':U}
 if point is not None:loc.update({'m':target,'x_1':point,'y_1':yp})
 blocks=re.findall(r'\$\$(.*?)\$\$',solution,re.S)
 expected=5 if kind=='tangent' else 4 if kind=='slope' else 3
 if len(blocks)!=expected:raise ValueError('Missing operative display block')
 signatures=[]
 for bi,block in enumerate(blocks):
  block=derivative_tokens(block,name);block=evaluated(block,loc,point)
  # Composite function and separate derivative pairs have comma annotations.
  pieces=block.split(r',\,') if bi<2 else [block]
  if bi<2 and len(pieces)!=2:raise ValueError('Missing inner function or separate derivative factor')
  stages=[]
  for piece in pieces:
   for parts in split_stages(piece):
    vals=[scalar(p,loc) for p in parts]
    vals=[v.subs(U,inner) for v in vals]
    if bi==len(blocks)-1 and kind=='tangent':
     for a,b in zip(vals,vals[1:]):
      res=s.expand(a-b);ratio=s.simplify(res/line)
      if ratio==0 or X in ratio.free_symbols or Y in ratio.free_symbols or ratio.is_zero:raise ValueError(('Incorrect whole tangent equation',parts,res,line))
    else:
     if any(not equal(v,vals[0]) for v in vals[1:]):raise ValueError(('Invalid printed equality',parts,vals))
    stages.extend(parts[1:])
  signatures.append(stages)
 # Operative stages remain mandatory even when deleting a true intermediate
 # equality would leave the final answer correct.
 family=record['generation']['template'];src=record['generation']['source_id']
 main=6 if family in ('scale-radio','scale-legacy-radio','scale-blank','power-radio','tangent-scaled','tangent-affine') else 4
 if src=='nonMA-17592186490400':main=4
 counts=[2,2,main]+([2 if src.startswith('nonMA-') else 4 if kind=='slope' else 3] if point is not None else [])+([3] if kind=='tangent' else [])
 if [len(z) for z in signatures]!=counts:raise ValueError(('Erased or extra operative equality stage',counts,[len(z) for z in signatures]))
 # Read ordered operations from printed operands, without generator math_data.
 # The first two displays must state the actual composite and BOTH factors.
 pair=[x.strip().rstrip('.,') for x in derivative_tokens(blocks[0],name).split(r',\,')]
 if [x.split('=')[0].strip() for x in pair]!=[name,'u']:raise ValueError('Changed composite-assignment operands')
 if not equal(scalar(pair[0].split('=',1)[1],loc),c*s.log(U)):raise ValueError('Wrong outer function of u')
 if not equal(scalar(pair[1].split('=',1)[1],loc),inner):raise ValueError('Stale printed inner function')
 pair=[x.strip().rstrip('.,') for x in derivative_tokens(blocks[1],name).split(r',\,')]
 if [x.split('=')[0].strip() for x in pair]!=['DU','UX']:raise ValueError('Changed standalone derivative operands')
 if not equal(scalar(pair[0].split('=',1)[1],loc),c/U):raise ValueError('Wrong outer derivative')
 if not equal(scalar(pair[1].split('=',1)[1],loc),s.diff(inner,X)):raise ValueError('Stale inner derivative coefficient')
 mainparts=[]
 for row in split_stages(derivative_tokens(blocks[2],name)):mainparts.extend(row[1:])
 def group_at(text,start):
  while start<len(text) and text[start].isspace():start+=1
  if text[start]!='{':raise ValueError('Fraction stage lacks explicit group')
  depth=1;end=start+1
  while depth:
   if end>=len(text):raise ValueError('Unclosed stage operand')
   if text[end]=='{':depth+=1
   elif text[end]=='}':depth-=1
   end+=1
  return text[start+1:end-1],end
 def quotient(raw):
  raw=raw.strip().rstrip('.,');sign=1
  if raw.startswith('-'):sign=-1;raw=raw[1:]
  if not raw.startswith(r'\frac'):raise ValueError('Combined fraction stage was erased')
  numerator,end=group_at(raw,5);denominator,end=group_at(raw,end)
  if raw[end:].strip():raise ValueError('Combined fraction stage contains extra operation')
  return sign*scalar(numerator,loc),scalar(denominator,loc)
 # Stage 1: formal df/du times du/dx. Stage 2: still in u.
 # Stage 3: substitute the original actual inner expression, keep chain factor.
 for ix,expected_outer in ((1,c/U),(2,c/inner)):
  factors=mainparts[ix].split(r'\cdot')
  if len(factors)!=2:raise ValueError('Separate chain-factor multiplication was erased')
  if not equal(scalar(factors[0],loc),expected_outer):raise ValueError('Stale outer denominator in chain stage')
  if not equal(scalar(factors[1],loc),s.diff(inner,X)):raise ValueError('Stale printed chain factor')
 if src!='nonMA-17592186490400':
  numerator,denominator=quotient(mainparts[3])
  expected_num,expected_den=(s.Integer(1),-inner) if family=='tangent-shift' else (c*s.diff(inner,X),inner)
  if not equal(numerator,expected_num) or not equal(denominator,expected_den):raise ValueError('Changed actual combined numerator or inner-function denominator')
 if main==6:
  canceled=re.findall(r'\\cancel\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}',mainparts[4])
  if len(canceled)!=2:raise ValueError('Cancellation operation erased')
  if family=='power-radio':expected_cancel=X**(s.Poly(inner,X).degree()-1)
  elif family=='tangent-affine':expected_cancel=-s.diff(inner,X)
  else:expected_cancel=s.diff(inner,X)
  if any(not equal(scalar(v,loc),expected_cancel) for v in canceled):raise ValueError('Wrong canceled factor')
 # Check formal operands and the ordered chain-rule structure explicitly.
 maintext=derivative_tokens(blocks[2],name).replace(' ','').strip()
 if not maintext.startswith(r'\begin{aligned}DX&=DU\cdotUX'):raise ValueError('Changed chain-rule operator backbone')
 for val in re.findall(r'\$x=(.*?)\$',solution):
  if point is not None and scalar(val)!=point:raise ValueError('Stale target in shared prose')
 if kind=='tangent':
  for val in re.findall(r'(?<!\$)\$m=(.*?)\$',solution):
   if not equal(scalar(val),target):raise ValueError('Stale slope in shared prose')
 for v in re.findall(r'(?<!\$)\$\((.*?)\)\$',solution):
  if point is not None:
   px,py=v.split(',',1)
   if not equal(scalar(px),point) or not equal(scalar(py),yp):raise ValueError('Stale supplied point in shared prose')
 for var,rawfun in re.findall(r'(?<!\$)\$([fg])\(x\)=(.*?)\$',solution):
  if var!=name or not equal(scalar(rawfun),fun):raise ValueError('Stale actual function in shared prose')
 # Every field is read as a complete mathematical object in the full prompt.
 fields=q[':question/answer-fields'];banks=[]
 for f in fields:
  if f[':answer-field/type'].endswith('/blank'):
   key=f[':answer-field/key']
   if '{{'+key+'}}' not in prompt:raise ValueError('Missing blank placeholder')
   expected_prefix='$m=$' if kind=='slope' else '$'+r'\frac{\text{d}'+name+r'}{\text{d}x}=$'
   if expected_prefix not in prompt:raise ValueError('Changed blank full context')
  correct=f[':answer-field/correct'][1];hits=0;vals=[]
  for a in f[':answer-field/choices']:
   raw=a[':answer/value']
   if kind=='tangent':
    parts=raw.split('=')
    if len(parts)!=2:raise ValueError('Tangent response must be a full equation')
    res=s.expand(scalar(parts[0])-scalar(parts[1]));ratio=s.simplify(res/line)
    right=ratio!=0 and X not in ratio.free_symbols and Y not in ratio.free_symbols
    val=res/s.Poly(res,Y).coeff_monomial(Y)
   else:val=scalar(raw);right=equal(val,target)
   if right!=(a[':answer/id']==correct):raise ValueError(('Incorrect printed key',raw))
   hits+=right
   if any(equal(val,v) for v in vals):raise ValueError('Equivalent complete-bank options')
   vals.append(val)
  if hits!=1:raise ValueError('Not exactly one true answer')
  if f[':answer-field/type'].endswith('/radio'):
   scale=s.diff(inner,X);poly=s.Poly(inner,X);degree=poly.degree()
   if family=='scale-radio':expected_values=[scale/X,scale*s.log(inner),1/s.log(inner),1/X,1/(scale*X)]
   elif family=='scale-legacy-radio':expected_values=[1/(scale*X),scale/X+1,1/X,1/X+scale,scale/X]
   elif family=='power-radio':expected_values=[degree*X**(degree-1)*s.log(inner),1/X,degree/X**degree,degree/X,1/X**degree]
   elif family=='shift-power-radio':expected_values=[degree*X**(degree-1)/inner,degree*(degree-1)/inner,(degree-1)*X*s.log(inner),X/inner,X**(degree-1)/inner]
   elif family=='tangent-origin':expected_values=[scale*(X-point)+1,scale*(X-point),X-point,X-point+scale,scale*(X-point)+s.log(scale)]
   elif family in ('tangent-shift','tangent-affine'):expected_values=[-target*X+target*point+yp,-target*X-target*point+yp,target*X-target*point+yp,target*X+yp,-2*target*X+yp]
   elif family=='tangent-scaled':expected_values=[2*target*X-c/2-s.log(inner.subs(X,point)),2*target*X-2*c+yp,target*X-c,target*X-c+yp,target*X+c]
   else:raise ValueError('Unknown complete-bank contract')
   if kind=='tangent':expected_values=[Y-z for z in expected_values]
   if len(vals)!=len(expected_values) or any(sum(equal(v,z) for z in expected_values)!=1 for v in vals):raise ValueError('Changed complete profile bank')
  banks.append(vals)
 return {'function':fun,'inner':inner,'domain':domain,'point':point,'kind':kind,'target':target,'stages':signatures,'bank':banks[0]}
