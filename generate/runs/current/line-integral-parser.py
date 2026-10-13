"""Parent's printed-prompt/solution endpoint oracle, independent of workers."""
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('parent_line_math',Path(__file__).with_name('vector-math-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$',re.S)
def inner(raw):return raw[2:-2] if raw.startswith('$$') else raw[1:-1]
def math(raw):return p.scalar(raw.strip().rstrip('.,'))
def equal(a,b):return s.simplify(s.trigsimp(a-b))==0
def blocks(text):return [inner(m[0]).strip().rstrip('.,') for m in MATH.finditer(text)]
def vector(raw):
 raw=raw.replace(r'\langle','⟨').replace(r'\rangle','⟩');assert raw.startswith('⟨') and raw.endswith('⟩'),raw
 return tuple(math(part) for part in raw[1:-1].split(','))
def domain(text,axis='t'):
 text=text.replace(r'\,','').strip().rstrip('.,')
 match=re.search(axis+r'\s*\\in\s*\[(.*?),(.*?)\]',text)
 if match:a,b=map(math,match.groups())
 else:
  match=re.fullmatch(r'(.*?)\\le(?:q)?\s*'+axis+r'\s*\\le(?:q)?(.*)',text);assert match,text;a,b=map(math,match.groups())
 assert s.simplify(b-a)>0;return a,b
def parametric(text):
 for body in blocks(text):
  match=re.search(r'r\(t\)\s*=\s*(⟨.*?⟩|\\langle.*?\\rangle)',body,re.S)
  if match:
   rest=body[match.end():].strip().lstrip(',').strip()
   # Supplied-path prompts sometimes put the interval in a separate inline slot.
   if not rest:rest=next(z for z in blocks(text) if r't\in [' in z)
   return vector(match[1]),domain(rest)
 raise AssertionError(('No printed parametrization',text))
def supplied(prompt):
 body=next(z for z in blocks(prompt) if re.match(r'f\(x,y(?:,z)?\)\s*=',z));f=math(body.split('=',1)[1]);path,interval=parametric(prompt);return f,path,interval
def cartesian(prompt,solution):
 body=next(z for z in blocks(prompt) if re.match(r'f\(x,y\)\s*=',z));f=math(body.split('=',1)[1])
 curve_text=prompt.split('curve ',1)[1];relation=blocks(curve_text)[0];assert relation.count('=')==1,relation
 lhs,rhs=map(math,relation.split('='));axis_body=next(z for z in blocks(curve_text) if re.match(r'[xy]\s*\\in',z));axis=axis_body[0];interval=domain(axis_body,axis)
 path,printed_interval=parametric(solution);assert len(path)==2 and interval==printed_interval
 assert equal(path[0 if axis=='x' else 1],p.t),('Independent coordinate',axis,path)
 substitutions={p.x:path[0],p.y:path[1]}
 assert equal(lhs.subs(substitutions,simultaneous=True),rhs.subs(substitutions,simultaneous=True)),('Printed Cartesian relation',relation,path)
 return f,path,interval,None
def missing(prompt,solution):
 body=next(z for z in blocks(prompt) if re.match(r'F(?:\(x,y\))?\s*=',z));raw=body.split('=',1)[1];V=p.vector(raw);assert V[2]==0;F=tuple(V[:2])
 f=math(next(z for z in blocks(solution) if re.match(r'f\(x,y\)\s*=',z)).split('=',1)[1]);assert equal(s.diff(f,p.x),F[0]) and equal(s.diff(f,p.y),F[1]);assert equal(s.diff(F[0],p.y),s.diff(F[1],p.x))
 if any('r(t)=' in z for z in blocks(prompt)):path,interval=parametric(prompt)
 else:
  body=next(z for z in blocks(prompt) if z.startswith('y='));path=(p.t,math(body[2:]).subs(p.x,p.t));interval=domain(next(z for z in blocks(prompt) if z.startswith(r'x\in')),axis='x')
  displayed,di=parametric(solution);assert interval==di and all(equal(a,b) for a,b in zip(path,displayed))
 return f,path,interval,F
def endpoints(f,path,interval):
 a,b=interval;A=tuple(s.simplify(z.subs(p.t,a)) for z in path);B=tuple(s.simplify(z.subs(p.t,b)) for z in path)
 def evaluate(point):return s.simplify(f.subs(dict(zip((p.x,p.y,p.z),point)),simultaneous=True))
 fa,fb=evaluate(A),evaluate(B);return A,B,fa,fb,s.simplify(fb-fa)
def group(raw,start):
 assert raw[start]=='(';depth=1;i=start+1
 while depth:
  assert i<len(raw),raw
  depth+=(raw[i]=='(')-(raw[i]==')');i+=1
 return raw[start+1:i-1],i
def evaluate_calls(raw,f,path):
 raw=raw.replace(r'\left','').replace(r'\right','')
 # Resolve actual f(r(bound)) calls, using balanced parentheses and TeX groups.
 def feval(point):
  value=s.simplify(f.subs(dict(zip((p.x,p.y,p.z),point)),simultaneous=True))
  # Keep the oracle's synthesized replacement in the notation supported by
  # its reader: simplification can introduce cosh even when output has none.
  return value.replace(s.cosh,lambda u:(s.exp(u)+s.exp(-u))/2).replace(s.sinh,lambda u:(s.exp(u)-s.exp(-u))/2)
 while 'f(' in raw:
  start=raw.index('f(');args,end=group(raw,start+1)
  if args.startswith('r('):
   bound,finish=group(args,1);assert finish==len(args);point=tuple(z.subs(p.t,math(bound)) for z in path)
  else:point=tuple(math(z) for z in args.split(','))
  assert len(point)==len(path);raw=raw[:start]+'('+s.latex(feval(point))+')'+raw[end:]
 return math(raw)
def stages(solution,f,path,interval,field=None):
 A,B,fa,fb,I=endpoints(f,path,interval);counts=dict(endpoint_vectors=0,endpoint_prose=0,gradient_components=0,cross_partials=0,final_rows=0)
 for body in blocks(solution):
  if r'\begin{aligned}' in body:
   rows=body.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r'\\');mode=None
   for row in rows:
    assert '=' in row,row;lhs,rhs=row.split('=',1);lhs=lhs.replace('&','').strip();rhs=rhs.strip().rstrip('.,')
    match=re.fullmatch(r'r\((.*)\)',lhs)
    if match:
     bound=math(match[1]);assert bound in interval;expected=tuple(s.simplify(z.subs(p.t,bound)) for z in path);assert all(equal(a,b) for a,b in zip(vector(rhs),expected));counts['endpoint_vectors']+=1;continue
    match=re.search(r'(?:f_([xy])|\{f\}_\{([xy])\})',lhs)
    if match:
     axis=next(z for z in match.groups() if z);assert field is not None and equal(math(rhs),field[0 if axis=='x' else 1]);counts['gradient_components']+=1;continue
    if r'\int' in lhs or '∫' in lhs:mode='integral'
    if mode=='integral':
     if r'\int' in rhs or '∫' in rhs:continue
     assert equal(evaluate_calls(rhs,f,path),I),(row,I);counts['final_rows']+=1
  elif re.match(r'\\frac\{(?:∂|\\partial)\s*P',body) and '=' in body and field is not None:
   rhs=body.rsplit('=',1)[1];assert equal(math(rhs),s.diff(field[0],p.y));counts['cross_partials']+=1
 # All endpoint coordinate prose must agree, even when f happens to erase an error.
 match=re.search(r'Therefore, the coordinates of the endpoints of the path defined by \$C\$ are \$\((.*?)\)\$ and \$\((.*?)\)\.\$',solution,re.S)
 if match:
  for raw,expected in zip(match.groups(),(A,B)):assert all(equal(math(a),b) for a,b in zip(raw.split(','),expected));counts['endpoint_prose']+=1
 return counts
