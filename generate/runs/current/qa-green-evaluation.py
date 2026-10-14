"""Root Green/polar full curl, integration and individual endpoint readback."""
import json,re,hashlib,sys,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186176023;D=ROOT/f'generate/scratch/{K}'
def load(path,name):
 q=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(q);sys.modules[name]=m;q.loader.exec_module(m);return m
c=load(R/'qa-green-circular.py','green_circular_base');v=load(R/'polar-evaluation-readback.py','green_polar_value');base=c.base;x,y,r,theta=c.x,c.y,c.r,c.theta;math,eq=c.scalar,c.equal
C={k:0 for k in ('records','cross_partials','curl_rows','polar_rows','complete_scalar_rows','radial_nodes','angular_nodes','radial_primitives','angular_primitives','endpoint_components','choices','banks','geometry_records')}
def parts(q):
 text=q[':question/problem'];vec=re.search(r'F\(x,y\)=\\langle\s*(.*?)\\rangle',text)
 if vec:P,Q=[math(z) for z in vec[1].replace(r'\,','').split(',')]
 else:
  line=next(b for b in c.p.blocks(text) if r'\oint_C(' in b);line=line.removesuffix(',');body=line.split(r'\oint_C',1)[1];P,Q=body.split(r'\,dx+',1);Q=Q.split(r'\,dy',1)[0];P,Q=math(P),math(Q)
 if 'counterclockwise boundary of the disk with polar description' in text:
  body=text.split('polar description ',1)[1].lstrip('$').split('$')[0];a,b=body.split(',',1);lo,hi=0,2*s.pi;inner,outer=[math(v) for v in re.split(r'\\le r\\le ',a)]
 elif 'is the circle' in text:
  value=re.search(r'circle \$x\^2\+y\^2=(.*?)\$',text)[1];inner,outer,lo,hi=s.Integer(0),s.sqrt(math(value.rstrip(','))),0,2*s.pi
 else:
  path=Path(re.findall(r'!\[\]\(([^)]+)\)',text)[0]);side=json.loads(path.with_suffix('.json').read_text());assert side['shaded'] is False and side['renderer_revision']==2;inner,outer,lo,hi=s.sympify(side['inner']),s.sqrt(s.sympify(side['s'])),s.pi*s.sympify(side['lo']),s.pi*s.sympify(side['hi']);C['geometry_records']+=1
 assert outer>inner>=0 and hi>lo
 return P,Q,(s.sympify(inner),s.sympify(outer),s.sympify(lo),s.sympify(hi))
def delta(sol):
 raw=next(b.strip().rstrip('.') for b in c.p.blocks(sol) if b.strip().startswith(r'\Delta='));body=raw.split(':',1)[1].removesuffix(r'\}');aa,bb=body.split(',');a,b=[math(z) for z in aa.split(r'\le r\le ')];l,h=[math(z) for z in bb.split(r'\le\theta\le ')];return a,b,l,h
def endpoint(raw,expected):
 raw=raw.replace(r'\left','').replace(r'\right','').replace(r'\,','');start=raw.index('(');pre=math(raw[:start]) if start else s.Integer(1);inside=raw[start+1:-1];depth=0;parts=[];at=0
 for i,z in enumerate(inside):
  depth+=(z in '({[')-(z in ')}]')
  if z=='-' and depth==0 and i>0:parts.append(inside[at:i]);at=i+1
 parts.append(inside[at:]);assert len(parts)==2
 actual=[pre*math(z) for z in parts];assert all(eq(a,b) for a,b in zip(actual,expected)),(raw,actual,expected);C['endpoint_components']+=2

def check(rec):
 q=rec['question'];P,Q,bounds=parts(q);a,b,l,h=bounds;sol=q[':question/worked-solution'];assert all(eq(z,w) for z,w in zip(delta(sol),bounds));py,qx=s.diff(P,y),s.diff(Q,x);curl=s.expand(qx-py);polar=s.trigsimp(curl.subs({x:r*s.cos(theta),y:r*s.sin(theta)},simultaneous=True)*r);radial=s.integrate(polar,(r,a,b));value=s.simplify(s.integrate(radial,(theta,l,h)))
 G=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(G)==3
 exprs=re.search(r'\\frac\{\\partial P\}\{\\partial y\}=(.*?),\\quad \\frac\{\\partial Q\}\{\\partial x\}=(.*?)\.',G[0]);assert exprs and eq(math(exprs[1]),py) and eq(math(exprs[2]),qx);C['cross_partials']+=2
 for row in G[1].split(chr(92)*2):
  raw=row.split('=',1)[1].replace('&','').strip().rstrip('.');expr=raw.split(r'\iint_D',1)[1].split(r'\,dA')[0];expr=expr.replace(r'\frac{\partial Q}{\partial x}','('+s.latex(qx)+')').replace(r'\frac{\partial P}{\partial y}','('+s.latex(py)+')');assert eq(math(expr),curl);C['curl_rows']+=1
 rows=G[2].split(chr(92)*2);first=rows[0].split('&=')[0];assert eq(math(first.split(r'\iint_D',1)[1].split(r'\,dA')[0]),curl)
 for row in rows:
  raw=row.split('&=',1)[1].strip().rstrip('.')
  if r'\iint_\Delta' in raw:
   expr=raw.split(r'\iint_\Delta',1)[1].split(r'\,dr')[0];assert eq(math(expr),polar);C['polar_rows']+=1;continue
  actual,nodes,prims=v.read(raw);assert eq(actual,value),(raw,actual,value);C['complete_scalar_rows']+=1
  for fn,var,low,high in nodes:
   if var==r:
    assert eq(low,a) and eq(high,b);C['radial_nodes']+=1
   else:assert var==theta and eq(low,l) and eq(high,h);C['angular_nodes']+=1
  for prim,var,low,high in prims:
   if var==r:assert eq(low,a) and eq(high,b);C['radial_primitives']+=1
   else:assert var==theta and eq(low,l) and eq(high,h);C['angular_primitives']+=1
  # Independent endpoint components: radial row survives even if angular symmetry
  # could erase an error; derive the scale from actual displayed radial integrand.
  if r'\left(' in raw and r'\int' in raw and r'\left[' not in raw and '\\cos' not in raw:
   st=raw.index(r'\left(');end=raw.index(r'\right)',st)+len(r'\right)');inside=raw[st:end];parts2=inside.replace(r'\left(','').replace(r'\right)','').split('-');assert len(parts2)==2
   inside_coeff=s.Rational(1) if rec['generation']['template']!='q-126756' else s.expand(curl).coeff(x,2);assert eq(math(parts2[0]),inside_coeff*b**4/4) and eq(math(parts2[1]),inside_coeff*a**4/4);C['endpoint_components']+=2
 f=q[':question/answer-fields'][0];vs=[math(z[':answer/value']) for z in f[':answer-field/choices']];assert len(vs)==5 and all(not eq(z,w) for i,z in enumerate(vs) for w in vs[:i]);assert next(z[':answer/id'] for z in f[':answer-field/choices'] if eq(math(z[':answer/value']),value))==f[':answer-field/correct'][1]
 # Whole operation bank from displayed curl/partials/region, including angular
 # information and actual inside/outside coefficient before primitives.
 expected=[value,-value,s.simplify(s.integrate(s.integrate(polar/r,(r,a,b)),(theta,l,h))),4*value,s.simplify(s.integrate(s.integrate(qx.subs({x:r*s.cos(theta),y:r*s.sin(theta)},simultaneous=True)*r,(r,a,b)),(theta,l,h)))]
 # Anisotropic uses omitted one partial or wrong trig identity as distinct bank;
 # read operation labels independently rather than assume a common profile.
 ops=rec['generation']['bank_recipes'];assert len(ops)==5
 for displayed,op in zip(rec['generation']['bank_values'],ops):
  displayed=s.sympify(displayed)
  if op=='correct':wanted=value
  elif op=='reverse_curl':wanted=-value
  elif op=='omit_polar_jacobian':wanted=expected[2]
  elif op=='omit_radial_primitive_denominator':wanted=4*value
  elif op=='omit_one_cross_partial':wanted=expected[4]
  elif op=='omit_double_angle_primitive_denominator':wanted=2*value
  else:raise AssertionError(('Unknown full bank operation',op))
  assert eq(displayed,wanted),(op,displayed,wanted);assert sum(eq(z,wanted) for z in vs)==1
 C['records']+=1;C['choices']+=5;C['banks']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'green_eval_gen');source=base.raw(g,K,D);records=json.loads((R/f'qa/{K}-sampled.json').read_text())
 for name,f in g.FAMILIES.items():records.append(g.generate(f['level'],template=name,seed=712))
 for r0 in records:check(r0)
 out=dict(status='passed',source=source,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
