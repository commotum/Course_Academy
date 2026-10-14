"""Root independently reads printed fields, integrals, primitives and banks."""
import importlib.util,json,re,hashlib,sys,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186133900;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','root_green_parser');x,y,u,v=p.x,p.y,p.u,p.v
g=load(D.with_suffix('.py'),'root_advanced_green');fidelity=load(R/'root-source-fidelity.py','root_green_fidelity');originals,S=fidelity.check(g,K,D)
def eq(a,b):return s.simplify(s.trigsimp(a-b))==0
def math(z):
 z=z.strip().rstrip('.,').replace(r'\theta','v');z=re.sub(r'(?<![A-Za-z])r(?![A-Za-z])','u',z)
 return s.Integer(1) if not z else p.scalar(z)
def group(z,i):
 assert z[i]=='{';j=i+1;depth=1
 while depth:depth+=(z[j]=='{')-(z[j]=='}');j+=1
 return z[i+1:j-1],j
def bounds(z,i):
 out=[]
 for op in ('_','^'):
  assert z[i]==op;i+=1;raw,i=group(z,i);out.append(math(raw))
 return out,i
C=dict(records=0,prompt_components=0,held_partials=0,separate_derivative_terms=0,curl_rows=0,calculation_rows=0,integral_kernels=0,primitive_derivatives=0,individual_endpoints=0,choices=0,whole_method_banks=0,geometry_bounds=0,source_operations=0)
def readrow(z,wanted,allowed_kernels,allowed_primitives):
 z=z.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*')
 while r'\int' in z:
  pos=z.rindex(r'\int');bs,start=bounds(z,pos+len(r'\int'));m=re.search(r'\\mathrm d\s*(\\theta|[xyr])',z[start:]);assert m,z
  axis={'x':x,'y':y,'r':u,r'\theta':v}[m[1]];kernel=math(z[start:start+m.start()]);assert any(eq(kernel,a) for a in allowed_kernels[axis]),('kernel',axis,kernel,allowed_kernels[axis]);C['integral_kernels']+=1
  val=s.integrate(kernel,(axis,*bs));z=z[:pos]+'('+s.latex(val)+')'+z[start+m.end():]
 while r'\big|' in z:
  pos=z.index(r'\big|');bs,end=bounds(z,pos+len(r'\big|'));depth=0;i=pos-1
  while i>=0:
   ch=z[i]
   if ch in '})':depth+=1
   elif ch in '{(':
    if depth==0:break
    depth-=1
   if depth==0 and ch in '*+-':break
   i-=1
  start=i+1;primitive=math(z[start:pos]);axis=next(iter(primitive.free_symbols));assert len(primitive.free_symbols)==1
  # Unary sign was left outside this atom, so allow signed primitive here.
  assert any(eq(s.diff(primitive,axis),a) or eq(s.diff(primitive,axis),-a) for a in allowed_primitives[axis]),('primitive',primitive,axis)
  C['primitive_derivatives']+=1;C['individual_endpoints']+=2
  val=primitive.subs(axis,bs[1])-primitive.subs(axis,bs[0]);z=z[:start]+'('+s.latex(val)+')'+z[end:]
 assert eq(math(z),wanted),('row',z,math(z),wanted);C['calculation_rows']+=1
records=json.load(open(R/f'qa/{K}-sampled.json'))
for f,data in g.FAMILIES.items():records.extend(g.generate(data[0],template=f,seed=n) for n in (631,917))
for rec in records:
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];params=rec['generation']['parameters']
 if family=='annulus_supplied':
  curl=math(re.search(r'\\frac\{\\partial Q\}\{\\partial x\}-\\frac\{\\partial P\}\{\\partial y\}=(.*?)\$',prompt)[1]);P=Q=Py=Qx=None
 else:
  fields=re.search(r'\\oint_\{\\partial [DR]\}\((.*?)\)\\,\\mathrm dx\+\((.*?)\)\\,\\mathrm dy',prompt);assert fields;P,Q=map(math,fields.groups());Py,Qx=s.diff(P,y),s.diff(Q,x);curl=s.factor(Qx-Py);C['prompt_components']+=2
  for name,axis,actual,derived in [('P',y,P,Py),('Q',x,Q,Qx)]:
   m=re.search(r'\\frac\{\\partial '+name+r'\}\{\\partial '+str(axis)+r'\}\s*&\s*=\\frac\{\\partial\}\{\\partial '+str(axis)+r'\}(.*?)=(.*?)=(.*?)(?=\\\\|\\end)',sol);assert m,(family,name)
   assert eq(math(m[1]),actual) and eq(math(m[3]),derived);terms=[math(z) for z in re.split(r'(?<=\\right\))\+(?=\\left\()',m[2])];assert eq(sum(terms),derived)
   expected=[s.diff(z,axis) for z in s.Add.make_args(actual)];assert len(terms)==len(expected) and all(any(eq(a,b) for b in expected) for a in terms),(family,name,actual,terms,expected);C['held_partials']+=1;C['separate_derivative_terms']+=len(terms)
  displayed=re.search(r'\$\$\\frac\{\\partial P\}\{\\partial y\}=(.*?),\\qquad\\frac\{\\partial Q\}\{\\partial x\}=(.*?)\.\$\$',sol);assert displayed and eq(math(displayed[1]),Py) and eq(math(displayed[2]),Qx)
  for body in re.findall(r'\\iint_[DR](.*?)\\,\\mathrm dA',sol):
   if r'\partial' in body:continue
   assert eq(math(body),curl),(family,body,curl);C['curl_rows']+=1
 if family.startswith('annulus'):
  bs=re.search(r'(?<![0-9])(-?\d+)\\le r\\le (-?\d+),0\\le\\theta(?:<|\\le)2\\pi',sol);assert bs;lo,hi=map(s.Integer,bs.groups());assert (int(lo),int(hi))==(params['inner'],params['outer']);C['geometry_bounds']+=2
  polar=s.trigsimp(curl.subs({x:u*s.cos(v),y:u*s.sin(v)})*u);answer=s.integrate(polar,(u,lo,hi),(v,0,2*s.pi))
  if family=='annulus_sin2':radial=u**3;angular=s.sin(2*v);factor=s.simplify(polar/(radial*angular));assert not factor.free_symbols
  elif family=='annulus_odd':angular=s.sin(v);radial=s.simplify(polar/angular);factor=s.Integer(1)
  else:angular=s.Integer(1);n=6 if s.degree(s.Poly(curl,x))==4 else 4;radial=u**(n-1);factor=s.simplify(polar/radial);assert not factor.free_symbols
  allowed={u:[polar,radial,radial*angular,factor*radial],v:[angular,s.integrate(polar,(u,lo,hi)),s.integrate(radial,(u,lo,hi))*angular]};primitives={u:[radial],v:[angular]}
  if family=='annulus_odd':rv=s.integrate(radial,(u,lo,hi));bank=[answer,2*rv,-2*rv,2*s.pi*rv,s.pi*rv]
  elif family=='annulus_sin2':bank=[s.Integer(0)]
  else:bank=[answer,-answer,2*s.pi*factor*hi**n/n,2*s.pi*factor*(hi**n+lo**n)/n,2*s.pi*factor*(hi**(n-1)-lo**(n-1))/(n-1)]
  # Independently enforce source factoring/cancellation operations; zero answer
  # cannot hide an arbitrary radial primitive or removed denominator stage.
  if family=='annulus_sin2':assert r'\frac{\cos(2\theta)}{-2}' in sol and r'\cdot (1-1)\cdot\frac{1}{4}' in sol
  elif family=='annulus_odd':assert r'\frac{'+s.latex(s.simplify(curl/(y*(x*x+y*y))))+'r^5}{5}' in sol and r'-\cos(2\pi)' in sol and r'\left(-1-\left(-1\right)\right)' in sol
  else:assert r'\cos^2\theta+\sin^2\theta' in sol and r'\frac{r^{'+str(n)+'}}{'+str(n)+'}' in sol and '('+str(hi)+')^{'+str(n)+'}' in sol
  C['source_operations']+=1
 else:
  regions=re.findall(r'\\Delta_[12]=\\\{\(x,y\):(-?\d+)\\le x\\le (-?\d+),(-?\d+)\\le y\\le (-?\d+)\\\}',sol);assert len(regions)==2;A,B=[list(map(s.Integer,z)) for z in regions];assert list(map(int,A))==params['outer'] and list(map(int,B))==params['hole'];C['geometry_bounds']+=8
  integrate=lambda F,Z:s.integrate(F,(x,Z[0],Z[1]),(y,Z[2],Z[3]));outer,hole=integrate(curl,A),integrate(curl,B);answer=outer-hole
  # Derive separated factors from actual curl, preserving source conventions.
  gy={'rectangle_y2':y**2,'rectangle_x3y2':y**2,'rectangle_xy':y,'rectangle_shift':2*y,'rectangle_x2y3':4*y**3}[family];gx=s.cancel(curl/gy);assert not gx.has(y)
  allowed={x:[curl,gx],y:[gy,s.integrate(curl,(x,A[0],A[1])),s.integrate(curl,(x,B[0],B[1]))]};primitives={x:[gx],y:[gy]}
  bank=[answer,outer+hole,outer,hole-outer,integrate(Qx,A)-integrate(Qx,B)]
 chains=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);rows=[z.split('&',1)[1].strip().lstrip('=').strip().rstrip('.') for z in chains[-1].split(chr(92)*2) if '&' in z]
 for row in rows:
  if r'\iint' in row:continue
  readrow(row,answer,allowed,primitives)
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];values=[math(a[':answer/value']) for a in choices]
 assert len(values)==len(bank) and all(sum(eq(z,w) for w in bank)==1 for z in values);assert all(not eq(a,b) for a,b in itertools.combinations(values,2));assert [a[':answer/id'] for a,z in zip(choices,values) if eq(z,answer)]==[field[':answer-field/correct'][1]]
 C['choices']+=len(values);C['whole_method_banks']+=1;C['records']+=1
out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
