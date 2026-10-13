"""Root actual scalar ds setup for a graph x=g(y), including formal operators."""
import importlib.util,re,functools
from pathlib import Path
import sympy as s
import mpmath as mp
def load(name,file):
 z=importlib.util.spec_from_file_location(name,Path(__file__).with_name(file));m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load('graph_scalar_reader','scalar-line-parser.py');x,y,t=p.x,p.y,p.t
scalar=p.scalar;equal=p.equal
def prompt(text):
 chunks=[z.strip().rstrip('.,?') for z in p.blocks(text)]
 integral=next(z for z in chunks if r'\int' in z);integral=integral.replace(r'{\int }',r'\int').replace('_(C)','_{C}').replace(r'\displaystyle','')
 body=re.sub(r'^.*?\\int_\{?C\}?','',integral);end=re.search(r'\\(?:text|mathrm)\{d\}s|ds',body);assert end,body;F=scalar(body[:end.start()].rstrip().removesuffix(r'\,'))
 curve=next(z for z in chunks if '=' in z and 'x' in z and 'y' in z and r'\int' not in z and z!='y=t' and z!='y=t.')
 l,r=curve.split('=');solutions=s.solve(scalar(l)-scalar(r),x);assert len(solutions)==1;g=solutions[0].subs(y,t)
 pts=[tuple(scalar(v) for v in z[1:-1].split(',')) for z in chunks if z.startswith('(') and z.endswith(')') and ',' in z];assert len(pts)==2
 assert all(equal(a,g.subs(t,b)) for a,b in pts);lo,hi=[z[1] for z in pts];assert hi>lo
 speed=s.sqrt(s.diff(g,t)**2+1);ft=F.subs({x:g,y:t},simultaneous=True);correct=ft*speed
 missing='missing expression' in text
 prefix=s.Integer(1)
 if missing:
  right=integral.split('=',1)[1];prefix=scalar(right[:right.index(r'\int')])
 return F,g,(lo,hi),ft,speed,correct,missing,prefix
def integral(raw):
 raw=raw.replace(r'{\int }',r'\int').replace(r'{\int}',r'\int')
 raw=re.sub(r'\\cdot\s*(?=\\int)','',raw)
 return p.e.integral(raw)
@functools.lru_cache(maxsize=4096)
def value(fn,a,b,dps=65):
 with mp.workdps(dps):
  lo,hi=mp.mpf(str(s.N(a,dps+10))),mp.mpf(str(s.N(b,dps+10)));f=s.lambdify(t,fn,'mpmath');out=mp.quad(f,[lo+(hi-lo)*i/8 for i in range(9)]);assert mp.isfinite(out) and not isinstance(out,mp.mpc);return +out
def same_value(a,b):
 with mp.workdps(65):return abs(a-b)<mp.mpf('1e-42')*max(1,abs(a),abs(b))
def derivatives(raw,g):
 raw=re.sub(r'\\frac\{\\(?:text|mathrm)\{d\}([xy])\}\{\\(?:text|mathrm)\{d\}t\}',lambda m:'('+s.latex(s.diff(g,t) if m[1]=='x' else s.Integer(1))+')',raw)
 pattern=r'\\frac\{\\(?:text|mathrm)\{d\}\}\{\\(?:text|mathrm)\{d\}t\}\('
 inputs=[]
 while re.search(pattern,raw):
  m=re.search(pattern,raw);start=m.end();depth=1;end=start
  while depth:depth+=(raw[end]=='(')-(raw[end]==')');end+=1
  argument=scalar(raw[start:end-1]);inputs.append(argument)
  raw=raw[:m.start()]+'('+s.latex(s.diff(argument,t))+')'+raw[end:]
 if inputs:assert len(inputs)==2 and equal(inputs[0],g) and inputs[1]==t,(inputs,g)
 return raw
def stages(text,details,integral_counts=(3,)):
 F,g,bounds,ft,speed,correct,missing,prefix=details
 n=dict(path_rows=0,formal_operator_rows=0,derivative_rows=0,norm_rows=0,density_rows=0,integral_rows=0,curve_isolation_rows=0)
 for chunk in p.blocks(text):
  raw=chunk.replace('&','').replace(r'\Longrightarrow','⟹').strip().rstrip('.,?')
  if raw.startswith('f(x,y)='):assert equal(scalar(raw.split('=',1)[1]),F)
  if re.search(r'\\le\s*t\\le',raw):
   domain=raw.rsplit('⟩',1)[-1].rsplit(r'\rangle',1)[-1].replace(r'\quad','').replace(r'\,','').lstrip(', ')
   lo,hi=re.split(r'\\le\s*t\\le\s*',domain);assert equal(scalar(lo),bounds[0]) and equal(scalar(hi),bounds[1])
  if raw.startswith('x=x(t)='):assert equal(scalar(raw.split('=')[-1]),g);n['curve_isolation_rows']+=1
  if '⟹' in raw:
   for equation in raw.split('⟹'):
    a,b=equation.replace(r'\,','').strip().split('=');assert equal((scalar(a)-scalar(b)).subs(x,g.subs(t,y)),0);n['curve_isolation_rows']+=1
  if raw.startswith('r(t)='):
   v=p.p.vector(raw.split('=',1)[1].replace(r'\langle','⟨').replace(r'\rangle','⟩').split('⟩')[0]+'⟩');assert len(v)==2 and equal(v[0],g) and v[1]==t;n['path_rows']+=1
  if '=' in raw and r'\int' not in raw and any(z in raw for z in ('{r}^{′}',r'r^{\prime}(t)')):
   raw=raw.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');mode='derivative'
   for row in raw.split(r'\\'):
    left,right=row.split('=',1)
    if '‖' in left or r'\|' in left:mode='norm'
    if r'\frac{\mathrm{d}}' in right or r'\frac{\text{d}}' in right:n['formal_operator_rows']+=1
    right=derivatives(right,g)
    if mode=='derivative':
     v=p.p.p.vector(right);assert all(equal(a,b) for a,b in zip(v,(s.diff(g,t),1,0)));n['derivative_rows']+=1
    else:assert equal(scalar(right),speed,bounds);n['norm_rows']+=1
  if raw.startswith(r'\begin{aligned}f(r(t))'):
   for index,row in enumerate(raw.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')):
    v=scalar(row.split('=',1)[1])
    if v.has(x,y):assert index==0 and equal(v,F);v=v.subs({x:g,y:t},simultaneous=True)
    assert equal(v,ft,bounds);n['density_rows']+=1
  if r'\int' in raw and r'\begin{aligned}' in raw and re.search(r'\\int(?:\s*\})?_\{?C\}?',raw):
   raw=raw.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
   lhs=raw.split('=',1)[0].replace(r'{\int }',r'\int');density=re.sub(r'^.*?\\int_\{?C\}?','',lhs);density=re.sub(r'\\(?:text|mathrm)\{d\}s\s*$','',density).rstrip().removesuffix(r'\,');assert equal(scalar(density),F)
   for row in raw.split(r'\\'):
    rhs=row.split('=',1)[1];rhs=p.e.replace_norm(rhs,speed).replace('f(r(t))','('+s.latex(ft)+')');rhs=re.sub(r'\\cdot\s*(?=\\(?:text|mathrm)\{d\}t)','',rhs);a,b,fn,var=integral(rhs);assert var==t and equal(a,bounds[0]) and equal(b,bounds[1]) and equal(fn,correct,bounds);n['integral_rows']+=1
 assert n['path_rows']==1 and n['formal_operator_rows']>=1 and n['derivative_rows']>=3 and n['norm_rows']>=3 and n['density_rows']>=2 and n['integral_rows'] in integral_counts,n
 return n
