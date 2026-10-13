"""Root evaluates the actually printed integrals and component stages."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','surface_parent_parser');H=load(R/'qa-sinusoidal-properties.py','surface_source_reader');V=load(R/'qa-vector-line-stages.py','surface_parent_helpers')
r=s.Symbol('u',nonnegative=True);theta=s.Symbol('v',real=True);p.locals_['u']=r;p.locals_['v']=theta
x,y,z=p.x,p.y,p.z
def scalar(text):
 text=text.replace(r'\theta','v').replace(r'\cancel','')
 text=re.sub(r'(?<![A-Za-z])r(?![A-Za-z])','u',text)
 return p.scalar(text.strip().rstrip('.,'))
def same(a,b):return V.same(a,b)
def group(text,start=0,opener='{',closer='}'):
 assert text[start]==opener,(text,start);depth=0
 for i in range(start,len(text)):
  depth+=(text[i]==opener)-(text[i]==closer)
  if depth==0:return text[start+1:i],i+1
 raise AssertionError(('unclosed group',text))
def split_terms(raw):
 raw=raw.replace(r'\left','').replace(r'\right','');depth=0;parts=[];start=0
 for i,c in enumerate(raw):
  depth+=(c in '({')-(c in ')}')
  if i>0 and depth==0 and c in '+-':parts.append(raw[start:i]);start=i
 parts.append(raw[start:]);return [scalar(z) for z in parts]
class Reader:
 def __init__(self,F,G,B,polar=None,derivative_mode=False):
  self.F,self.G,self.B,self.polar=F,G,B,polar;self.dx,self.dy=s.diff(G,x),s.diff(G,y);self.pref=F.subs(z,G);self.metric=s.sqrt(1+self.dx**2+self.dy**2);self.primitives=[];self.endpoint_terms=0;self.integrals=0;self.derivative_mode=derivative_mode
 def clean(self,raw):
  raw=raw.replace(r'\left','').replace(r'\right','').replace(r'\cancel','').replace(r'\,','').strip().rstrip('.,')
  raw=raw.replace('f(x,y,g(x,y))','('+s.latex(self.pref)+')').replace(r'\frac{∂z}{∂x}','('+s.latex(self.dx)+')').replace(r'\frac{∂z}{∂y}','('+s.latex(self.dy)+')').replace(r'\frac{\partial z}{\partial x}','('+s.latex(self.dx)+')').replace(r'\frac{\partial z}{\partial y}','('+s.latex(self.dy)+')')
  if self.polar:
   pol=self.pref.subs({x:r*s.cos(theta),y:r*s.sin(theta)},simultaneous=True)
   raw=raw.replace(r'f(r\cos\theta,r\sin\theta)','('+s.latex(pol)+')')
  area=s.integrate(self.B[3]-self.B[2],(x,self.B[0],self.B[1])) if self.B else 0
  raw=raw.replace(r'\text{Area}(D)','('+s.latex(area)+')');return raw
 def value(self,raw):
  text=self.clean(raw)
  if not text:return s.Integer(1)
  # Complete double integrals have one actual domain and a differential dA.
  m=re.search(r'\{∬\}_\{(D|\\Delta)\}|\\iint_(D|\\Delta)',text)
  if m:
   domain=next(z for z in m.groups() if z);end=re.search(r'\\(?:text|mathrm)\{d\}(?:A|r\\(?:text|mathrm)\{d\}\\theta)',text[m.end():]);assert end,text
   body=text[m.end():m.end()+end.start()];expr=self.value(body)
   if self.derivative_mode:value=expr
   elif domain=='D' and self.B:lo,hi,yl,yh=self.B;value=s.integrate(s.integrate(s.simplify(s.trigsimp(expr)),(y,yl,yh)),(x,lo,hi))
   else:
    radius,a,b=self.polar
    if domain=='D':expr=expr.subs({x:r*s.cos(theta),y:r*s.sin(theta)},simultaneous=True)*r
    value=s.integrate(s.integrate(s.trigsimp(expr),(r,0,radius)),(theta,a,b))
   return self.value(text[:m.start()]+'('+s.latex(value)+')'+text[m.end()+end.end():])
  m=re.search(r'\\int_',text)
  if m:
   lo,pos=group(text,m.end());assert text[pos]=='^';hi,pos=group(text,pos+1)
   # Differential identifies the actual integration variable. The final one
   # belongs to the outer integral, whose body contains any inner integral.
   diffs=list(re.finditer(r'\\(?:text|mathrm)\{d\}(x|y|r|\\theta)',text[pos:]));assert diffs,text
   diff=diffs[-1];var={'x':x,'y':y,'r':r,r'\theta':theta}[diff[1]];body=text[pos:pos+diff.start()];expr=self.value(body);value=expr if self.derivative_mode else s.integrate(s.simplify(s.trigsimp(expr)),(var,scalar(lo),scalar(hi)));self.integrals+=1
   return self.value(text[:m.start()]+'('+s.latex(value)+')'+text[pos+diff.end():])
  at=text.find('[')
  if at>=0:
   body,pos=group(text,at,'[',']')
   if pos==len(text) or text[pos]!='_':return self.value(text[:at]+'('+body+')'+text[pos:])
   lo,pos=group(text,pos+1);assert text[pos]=='^';hi,pos=group(text,pos+1)
   expr=self.value(body)
   if '=' in lo:
    a,lo=lo.split('=',1);b,hi=hi.split('=',1);assert a==b;var={'x':x,'y':y,'r':r,r'\theta':theta}[a]
   else:
    variables=[v for v in (r,theta) if expr.has(v)];assert len(variables)==1,(body,expr);var=variables[0]
   lo=scalar(lo);hi=scalar(hi);self.primitives.append((expr,var,lo,hi,body));value=s.diff(expr,var) if self.derivative_mode else expr.subs(var,hi)-expr.subs(var,lo)
   return self.value(text[:at]+'('+s.latex(s.simplify(value))+')'+text[pos:])
  return scalar(text)
def check(k):
 g=load(ROOT/f'generate/scratch/{k}.py','surface_'+str(k))
 class Replay:
  @staticmethod
  def generate(level,**kwargs):return g.generate(level or 'hard',**kwargs)
 src=H.source(Replay,k);records=json.loads((R/f'qa/{k}-sampled.json').read_text());n=dict(records=0,formal_partials=0,solution_stages=0,choices=0,printed_integrals=0,primitive_components=0)
 for rec in records:
  q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template']
  body=re.search(r'\\iint_S (.*?)\\,\\mathrm\{d\}S',prompt,re.S)[1];F=scalar(body);G=scalar(re.search(r'defined by \$z=(.*?)\$',prompt)[1]);dx,dy=s.diff(G,x),s.diff(G,y);polar=None
  if k==17592186105887:
   dom=re.findall(r'\$([^$]+)\\le ([xy])\\le ([^$]+)\$',prompt);assert len(dom)==2;B=tuple(scalar(v) for a,_,b in dom for v in (a,b))
  else:
   domain=re.search(r'\\Delta=\\\{\(r,\\theta\):0\\le r\\le (.*?),\\ (.*?)\\le\\theta\\le (.*?)\\\}',sol);assert domain,sol;polar=tuple(scalar(v) for v in domain.groups());B=None
  reader=Reader(F,G,B,polar);density=s.simplify(s.trigsimp(reader.pref*reader.metric))
  if polar:
   radius,a,b=polar;pd=s.trigsimp(density.subs({x:r*s.cos(theta),y:r*s.sin(theta)},simultaneous=True)*r);pd=s.simplify(pd);answer=s.integrate(s.integrate(pd,(r,0,radius)),(theta,a,b))
  else:answer=s.integrate(s.integrate(density,(y,B[2],B[3])),(x,B[0],B[1]))
  answer=s.simplify(answer)
  for axis,want in [('x',dx),('y',dy)]:
   pattern=r'\\frac\{(?:∂|\\partial)\s*z\}\{(?:∂|\\partial)\s*'+axis+r'\}=\\frac\{(?:∂|\\partial)\}\{(?:∂|\\partial)\s*'+axis+r'\}\((.*?)\)=([^,$\n]+)';m=re.search(pattern,sol);assert m and same(scalar(m[1]),G) and same(scalar(m[2]),want),(family,axis);n['formal_partials']+=1
  aligned=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert aligned
  for block in aligned:
   for row in block.split(r'\\'):
    lhs,rhs=re.split(r'&\s*=',row,maxsplit=1);value=reader.value(rhs);assert same(value,answer),(family,rhs,value,answer);n['solution_stages']+=1
    if re.search(r'\]_\{',reader.clean(rhs)):
     derivative_reader=Reader(F,G,B,polar,derivative_mode=True);printed_derivative=derivative_reader.value(rhs);assert len(derivative_reader.primitives)==1
     var=derivative_reader.primitives[0][1]
     if polar:
      first=theta if family=='x_over_r2' else r
      expected=pd if var==first else s.integrate(pd,(first,a,b)) if first==theta else s.integrate(pd,(first,0,radius))
     else:expected=density if var==y else s.integrate(density,(y,B[2],B[3]))
     assert same(printed_derivative,expected),(family,'primitive derivative',rhs,printed_derivative,expected)
  for primitive,var,primitive_lo,primitive_hi,raw in reader.primitives:
   # Primitive component derivatives sum to the actual printed primitive.
   terms=split_terms(raw);assert same(sum(terms),primitive);assert same(sum(s.diff(v,var) for v in terms),s.diff(primitive,var));n['primitive_components']+=len(terms)
  f=q[':question/answer-fields'][0];values=[scalar(v[':answer/value']) for v in f[':answer-field/choices']];assert len(values)==5 and all(not same(v,w) for i,v in enumerate(values) for w in values[:i])
  for opt,value in zip(f[':answer-field/choices'],values):assert same(value,answer)==(opt[':answer/id']==f[':answer-field/correct'][1]);n['choices']+=1
  # Recompute the complete method-derived bank from displayed inputs.
  if polar:
   radius,a,b=polar;integ=lambda v:s.integrate(s.integrate(s.trigsimp(v),(r,0,radius)),(theta,a,b));base=pd/reader.metric
   expected=[answer,integ(base),integ(base*reader.metric**2),s.integrate(s.integrate(pd,(r,0,radius)),(theta,a,(a+b)/2)),s.integrate(s.integrate(pd,(r,0,radius/2)),(theta,a,b))]
  else:
   lo,hi,yl,yh=B;integ=lambda v:s.integrate(s.integrate(s.simplify(s.trigsimp(v)),(y,yl,yh)),(x,lo,hi));P=reader.pref;M=reader.metric
   if family=='constant_plane':expected=[answer,integ(P),integ(P*M*M),integ(P*s.sqrt(1+dx*dx)),answer/(yh-yl)]
   elif family=='canonical_cancel':expected=[answer,answer/s.sqrt(2),answer*s.sqrt(2),-answer,answer/(yh-yl)]
   elif family=='trig_triangle':expected=[answer,-answer,answer/2,2*answer,s.integrate(s.integrate(density,(y,0,yh)),(x,lo,hi))]
   elif family in ('paraboloid_xy','plane_log','plane_ratio','reciprocal_triangle'):expected=[answer,-answer,integ(density.subs(y,yh)),s.integrate(s.integrate(density,(y,yl,yh)),(x,lo,(hi+lo)/2)),2*answer]
   else:expected=[answer,integ(P),integ(P*M*M),-answer,integ(F.subs(z,0)*M)]
  remaining=list(expected)
  for value in values:
   match=[j for j,w in enumerate(remaining) if same(value,w)];assert len(match)==1,(family,value,remaining);remaining.pop(match[0])
  n['printed_integrals']+=reader.integrals;n['records']+=1
 report=dict(status='passed',kp_id=k,source=src,readback=n,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest());(R/f'qa/{k}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
 for k in map(int,sys.argv[1:]):check(k)
