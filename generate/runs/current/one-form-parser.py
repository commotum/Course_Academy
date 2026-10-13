"""Root's fail-closed reader for printed one-forms and definite integrals."""
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('parent_oneform_scalar',Path(__file__).with_name('vector-math-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
x,y,t,DX,DY,XP,YP=p.x,p.y,p.t,p.i,p.j,p.u,p.v
MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$',re.S)
def blocks(text):return [(v[2:-2] if v.startswith('$$') else v[1:-1]).strip().rstrip('.,') for v in MATH.findall(text)]
def group(raw,start):
 opener=raw[start];assert opener in '{(';close='}' if opener=='{' else ')';depth=1;i=start+1
 while depth:
  assert i<len(raw),raw;depth+=(raw[i]==opener)-(raw[i]==close);i+=1
 return raw[start+1:i-1],i

def scalar(raw):
 raw=re.sub(r'\\sqrt\[3\]\{([^{}]+)\}',r'(\1)^{\\frac{1}{3}}',raw)
 raw=raw.strip().rstrip(',.?');raw=raw.replace(r'\displaystyle','').replace(r'\mathrm{d}x','i').replace(r'\mathrm{d}y','j').replace(r'\text{d}x','i').replace(r'\text{d}y','j').replace('dx','i').replace('dy','j')
 raw=raw.replace(r'{x}^{′}','u').replace(r'{y}^{′}','v').replace(r'x\prime(t)','u').replace(r'y\prime(t)','v')
 raw=raw.replace('x(t)','x').replace('y(t)','y')
 raw=raw.replace(r'\frac{i}{\text{d}t}','u').replace(r'\frac{j}{\text{d}t}','v').replace(r'\frac{i}{\mathrm{d}t}','u').replace(r'\frac{j}{\mathrm{d}t}','v')
 raw=raw.replace(r'\mathrm{d}t','').replace(r'\text{d}t','').replace('dt','').replace(r'\!','').replace(r'\;','').replace('[','(').replace(']',')')
 return p.scalar(raw)
def oneform(text):
 body=next(v for v in blocks(text) if r'\int' in v);body=body.rstrip('=');body=re.sub(r'\{\\int\s*\}',r'\\int',body);body=re.sub(r'\\int(?:\\limits)?_\{?C\}?','',body)
 form=s.expand(scalar(body));P,Q=form.coeff(DX),form.coeff(DY);assert s.simplify(form-P*DX-Q*DY)==0;return P,Q

def wrapper(raw):
 m=re.fullmatch(r'(-?\d+)\\left\((.*)\\right\)',raw,re.S);return (s.Integer(m[1]),m[2]) if m else (s.Integer(1),raw)
def bound(raw,start):
 while raw[start].isspace():start+=1
 if raw[start]=='{':return group(raw,start)
 # Captured limits here use braced groups; authored limits do too.
 if raw[start].isdigit():return raw[start],start+1
 raise AssertionError(('Unbraced bound',raw[start:]))
def integral(raw):
 raw=raw.strip().rstrip('.,');c,raw=wrapper(raw);raw=re.sub(r'\{\\int\s*\}',r'\\int',raw)
 i=raw.index(r'\int');prefix=raw[:i].strip();j=i+len(r'\int');assert raw[j]=='_';low,j=bound(raw,j+1);assert raw[j]=='^';high,j=bound(raw,j+1)
 ftext=raw[j:];f=s.Integer(1) if not re.sub(r'\\(?:,|mathrm\{d\}t|text\{d\}t)|dt','',ftext).strip() else scalar(ftext)
 multiplier=s.Integer(-1) if prefix=='-' else (s.Integer(1) if not prefix else scalar(prefix))
 return c*multiplier*f,scalar(low),scalar(high)
def ellipse(text):
 body=next(v for v in blocks(text) if '=' in v and 'x' in v and 'y' in v and r'\int' not in v);lhs,rhs=map(scalar,body.split('='));poly=s.Poly(lhs-rhs,x,y);assert poly.total_degree()==2 and poly.coeff_monomial(x*y)==poly.coeff_monomial(x)==poly.coeff_monomial(y)==0
 a=s.sqrt(-poly.coeff_monomial(1)/poly.coeff_monomial(x*x));b=s.sqrt(-poly.coeff_monomial(1)/poly.coeff_monomial(y*y));assert a>0 and b>0
 points=[]
 for block in blocks(text):
  v=re.sub(r'^[AB]','',block).replace(r'\left','').replace(r'\right','').strip().rstrip('.,')
  if v.startswith('(') and v.endswith(')'):
   point=tuple(scalar(z) for z in v[1:-1].split(','));assert len(point)==2;points.append(point)
 assert len(points)==2
 angles=[]
 for xx,yy in points:
  possible=[i for i in range(4) if s.simplify(xx-a*s.cos(i*s.pi/2))==s.simplify(yy-b*s.sin(i*s.pi/2))==0];assert len(possible)==1;angles.append(possible[0])
 low,high=angles
 while high<=low:high+=4
 assert 'counterclockwise direction' in text
 return (a*s.cos(t),b*s.sin(t)),(low*s.pi/2,high*s.pi/2),tuple(points)
def equivalent(a,b):return s.simplify(s.trigsimp(a-b))==0
def evaluate_form(P,Q,path):
 X,Y=path;return s.simplify(s.expand(P.subs({x:X,y:Y},simultaneous=True)*s.diff(X,t)+Q.subs({x:X,y:Y},simultaneous=True)*s.diff(Y,t)))

def clean(raw):
 return raw.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').strip().rstrip('.,')
def primitive(raw):
 raw=raw.strip();c,raw=wrapper(raw)
 if not raw.startswith(('{[',r'\left[','[')) and ('{[' in raw or r'\left[' in raw or '[' in raw):
  j=min(i for i in (raw.find('{['),raw.find(r'\left['),raw.find('[')) if i>=0);c*=scalar(raw[:j]);raw=raw[j:]
 # Source uses {[F]}_a^b as well as F{|}_a^b; authored uses left[Fright].
 if raw.startswith('{['):raw=raw[1:];end=raw.index(']}');F=raw[1:end];j=end+2
 elif raw.startswith(r'\left['):end=raw.index(r'\right]');F=raw[6:end];j=end+7
 elif raw.startswith('['):end=raw.index(']');F=raw[1:end];j=end+1
 else:
  marker=raw.index(r'{|}');F=raw[:marker];j=marker+3
 assert raw[j]=='_';lo,j=bound(raw,j+1);assert raw[j]=='^';hi,j=bound(raw,j+1);assert not raw[j:].strip(),raw[j:]
 return c*scalar(F),scalar(lo),scalar(hi)
def stages(text,P,Q,path,limits):
 X,Y=path;lo,hi=limits;f=evaluate_form(P,Q,path);I=None;counts={'paths':0,'derivatives':0,'integrands':0,'primitives':0,'evaluation_rows':0}
 for block in blocks(text):
  block=clean(block)
  if 'r(t)' in block and '=' in block and r'\int' not in block:
   vec=block.split('=')[-1].replace(r'\,','').split(',')[0];v=p.vector(vec);assert equivalent(v[0],X) and equivalent(v[1],Y) and v[2]==0,vec;counts['paths']+=1
  elif ('r\\prime' in block or '{r}^{′}' in block or r'{r}^{\prime}' in block) and '=' in block:
   vec=block.split('=')[-1];v=p.vector(vec);assert equivalent(v[0],s.diff(X,t)) and equivalent(v[1],s.diff(Y,t)) and v[2]==0,vec;counts['derivatives']+=1
  if r'\int' not in block or '=' not in block:continue
  rows=re.split(r'\\\\\s*&?\s*=',block.replace('&',''))
  rows[0]=rows[0].split('=',1)[1]
  for row in rows:
   row=clean(row)
   if r'\int' in row:
    v,a,b=integral(row);v=v.subs({x:X,y:Y,XP:s.diff(X,t),YP:s.diff(Y,t)},simultaneous=True);assert equivalent(v,f),(row,v,f);assert equivalent(a,lo) and equivalent(b,hi);counts['integrands']+=1
   elif re.search(r'(?:\]|\{\|\})\}?_',row):
    I=s.integrate(f,(t,lo,hi)) if I is None else I
    F,a,b=primitive(row);assert equivalent(s.diff(F,t),f),(row,F,f);assert equivalent(a,lo) and equivalent(b,hi);assert equivalent(F.subs(t,b)-F.subs(t,a),I);counts['primitives']+=1
   else:
    I=s.integrate(f,(t,lo,hi)) if I is None else I
    v=scalar(row);assert equivalent(v,I),(row,v,I);counts['evaluation_rows']+=1
 assert counts['paths']==counts['derivatives']==1,counts
 return counts

def cartesian(text,solution):
 equation=next(v for v in blocks(text) if v.startswith('y='));curve=scalar(equation[2:]);points=[]
 for v in blocks(text):
  v=re.sub(r'^[APBQ]','',v).strip().rstrip('.,').replace(r'\left','').replace(r'\right','')
  if v.startswith('(') and v.endswith(')'):
   point=tuple(scalar(z) for z in v[1:-1].split(','));assert len(point)==2;points.append(point)
 assert len(points)==2 and all(equivalent(b,curve.subs(x,a)) for a,b in points)
 block=next(v for v in blocks(solution) if 'r(t)' in v and '=' in v);vec=clean(block).split('=')[-1].replace(r'\,','').split(',')[0];v=p.vector(vec);X,Y=v[:2];assert v[2]==0;tp=s.Symbol('positive_parameter',nonnegative=True);assert equivalent(Y.subs(t,tp),s.powdenest(curve.subs(x,X).subs(t,tp),force=True)),(curve,X,Y)
 tail=block.split(r'\in')[1].replace(r'\left','').replace(r'\right','').strip();end=tail.index(']');lo,hi=[scalar(z) for z in tail[tail.index('[')+1:end].split(',')];assert hi>lo
 assert all(equivalent(a,b.subs(t,u)) for point,u in zip(points,(lo,hi)) for a,b in zip(point,(X,Y)))
 return (X,Y),(lo,hi),curve,tuple(points)

def segment(text,solution):
 points=[]
 for v in blocks(text):
  v=re.sub(r'^[A-Z]','',v).replace(r'\left','').replace(r'\right','').strip().rstrip('.,')
  if v.startswith('(') and v.endswith(')'):
   point=tuple(scalar(z) for z in v[1:-1].split(','));assert len(point)==2;points.append(point)
 assert len(points)==2;A,B=points;path=tuple(a+t*(b-a) for a,b in zip(A,B));checks=0
 vectors=[a*DX+b*DY for a,b in points]
 for block in blocks(solution):
  block=clean(block)
  if block.startswith(('a=','b=')):
   name,raw=block.split('=',1);v=p.vector(raw);n=0 if name=='a' else 1;assert all(equivalent(z,q) for z,q in zip(v,(*points[n],0)));checks+=1
  if 'r(t)' in block and '=' in block:
   rows=re.split(r'\\\\\s*=?\s*',block)
   for row in rows:
    raw=row.split('=')[-1].strip().rstrip(',');raw=re.sub(r'\ba\b','('+s.latex(vectors[0])+')',raw);raw=re.sub(r'\bb\b','('+s.latex(vectors[1])+')',raw);v=p.vector(raw);assert all(equivalent(z,q) for z,q in zip(v,(*path,0))),(raw,v,path);checks+=1
  if block.startswith(('x(t)=','y(t)=')):
   name,raw=block.split('=',1);assert equivalent(scalar(raw),path[0 if name.startswith('x') else 1]);checks+=1
 assert checks>=6,checks
 return path,(s.Integer(0),s.Integer(1)),tuple(points),checks
