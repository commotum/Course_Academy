"""Root displayed derivative reader: explicit order, input, function and target roles."""
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('root_higher_scalar',Path(__file__).with_name('ode-scalar-parser.py'));P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
x=P.x
def group(t,at):
 assert t[at] in '({';depth=1;j=at+1
 while depth:
  assert j<len(t);depth+=(t[j] in '({')-(t[j] in ')}');j+=1
 return t[at+1:j-1],j
def clean(t):
 t=t.strip().rstrip('.,?').replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\dfrac',r'\frac')
 for symbol,count in (('′',1),('″',2),('‴',3),('⁗',4)):t=t.replace(symbol,"'"*count)
 t=t.replace(r'\prime',"'");t=re.sub(r'\^\{(\x27+)\}',r'\1',t);t=re.sub(r'\^\{\((\d+)\)\}',lambda m:"'"*int(m[1]),t)
 t=re.sub(r'\{([fghy])\}',r'\1',t);t=re.sub(r'\\(?:text|mathrm|textrm)\{d\}', 'd',t).replace('{d}^','d^')
 # Keep numerator and denominator orders separately, so mismatched orders fail.
 pattern=r'\\frac\{d(?:\^\{?(\d+)\}?)?\s*([fghy]?)\}\{d\{?x\}?(?:\^\{?(\d+)\}?)?\}'
 def operator(m):
  n=int(m[1] or 1);d=int(m[3] or 1);assert n==d and 1<=n<=8,('mismatched derivative orders',m[0]);return '@D'+str(n)+m[2]+'@'
 return re.sub(pattern,operator,t)
def scalar(t,positive=False):
 value=P.scalar(clean(t))
 if positive:
  xp=s.Symbol('root_positive_x',positive=True);value=s.powdenest(value.subs(x,xp),force=True).subs(xp,x)
 return value
def eq(a,b,positive=False):
 if s.expand(a-b)==0:return True
 if positive:
  xp=s.Symbol('root_positive_x',positive=True);a,b=[s.powdenest(z.subs(x,xp),force=True) for z in (a,b)]
 return s.simplify(a-b)==0
def name_order(raw):
 raw=clean(raw);m=re.fullmatch(r"([fghy])(\x27*)\(x\)",raw)
 if m:return m[1],len(m[2])
 m=re.fullmatch(r'@D(\d+)([fghy])@',raw)
 if m:return m[2],int(m[1])
 if raw=='y':return 'y',0
 raise AssertionError(('unsupported supplied function',raw))
def givens(prompt,positive=False):
 candidates=[]
 for block in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',prompt,re.S):
  text=next(z for z in block if z!='')
  if '=' not in text or re.search(r'\{\{(?:field-|selection)',text):continue
  left,right=text.split('=',1)
  try:name,baseorder=name_order(left);fun=scalar(right,positive)
  except (AssertionError,ValueError):continue
  candidates.append((name,baseorder,fun))
 assert len(candidates)==1,('ambiguous or absent supplied function',prompt,candidates)
 return candidates[0]
def stage(block,fun,name,baseorder,order,at=None,positive=False):
 block=re.sub(r'\\(?:begin|end)\{aligned\}','',block);counts=dict(equalities=0,operands=0,targets=0)
 expected=s.diff(fun,x,order-baseorder);expected=expected.subs(x,at) if at is not None else expected
 for row_index,row in enumerate(block.split(r'\\')):
  pieces=[z for z in row.replace('&','').split('=') if z.strip()]
  assert len(pieces)>=(2 if row_index==0 else 1),(row_index,row)
  for raw in pieces:
   result,inputs,targets=value(raw,fun,name,baseorder,at,positive);assert eq(result,expected,positive),(order,row,result,expected)
   for n,operand in inputs:
    assert order-n>=baseorder and eq(operand,s.diff(fun,x,order-n-baseorder),positive),('wrong formal derivative operand/order',order,n,operand)
   for n,target in targets:assert n==order and (target==x if at is None else eq(target,at,positive)),('wrong displayed derivative order/target',order,n,target,at)
   counts['operands']+=len(inputs);counts['targets']+=len(targets);counts['equalities']+=1
 return counts
def value(raw,fun,name,baseorder,at=None,positive=False):
 text=clean(raw);inputs=[];targets=[]
 def derivative(order,target=x):
  assert order>=baseorder,(order,baseorder);return s.diff(fun,x,order-baseorder).subs(x,target)
 def label(match):
  label,primes,argument=match[1],match[2],match[3];assert label==name,(label,name);point=scalar(argument,positive);order=len(primes)
  assert point==x or at is not None and eq(point,at,positive),('stale derivative target',point,at);targets.append((order,point));return '('+s.latex(derivative(order,point),root_notation=False).replace(r'\log',r'\ln')+')'
 text=re.sub(r"([fghy])(\x27*)\((.*?)\)",label,text)
 if text==name:return derivative(0),inputs,[(0,x)]
 def fraction_label(match):
  order,label=int(match[1]),match[2];assert label==name,(label,name);targets.append((order,x));return '('+s.latex(derivative(order),root_notation=False).replace(r'\log',r'\ln')+')'
 text=re.sub(r'@D(\d+)([fghy])@',fraction_label,text)
 while re.search(r'@D\d+@',text):
  m=re.search(r'@D(\d+)@',text);pos=m.end()
  while text[pos].isspace():pos+=1
  arg,end=group(text,pos);operand=scalar(arg,positive);order=int(m[1]);inputs.append((order,operand));text=text[:m.start()]+'('+s.latex(s.diff(operand,x,order),root_notation=False).replace(r'\log',r'\ln')+')'+text[end:]
 # Parenthesized expressions with a prime are derivatives of their actual
 # printed contents; find balanced operands rather than evaluating a template.
 while "'" in text:
  atprime=text.index("'");end=atprime-1
  while text[end].isspace():end-=1
  assert text[end] in ')}',text;depth=1;start=end
  while depth:
   start-=1;assert start>=0;depth+=(text[start] in ')}')-(text[start] in '({')
  arg=text[start+1:end];operand=scalar(arg,positive);n=0;j=atprime
  while j<len(text) and text[j]=="'":n+=1;j+=1
  inputs.append((n,operand));text=text[:start]+'('+s.latex(s.diff(operand,x,n),root_notation=False).replace(r'\log',r'\ln')+')'+text[j:]
 return scalar(text,positive),inputs,targets
