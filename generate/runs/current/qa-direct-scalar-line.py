"""Root direct scalar line-integral stages and all operation banks from text."""
import json,re,sys,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R));import importlib.util
ss=importlib.util.spec_from_file_location('root_scalar_shared',R/'qa-parametric-scalar-line.py');base=importlib.util.module_from_spec(ss);ss.loader.exec_module(base)
s,p,e,t,x,y,z=base.s,base.p,base.e,base.t,base.x,base.y,base.z;scalar,equal,groups,right=base.scalar,base.equal,base.groups,base.right
K=17592186133830;D=base.ROOT/f'generate/scratch/{K}'
def prompt(q):
 text=q[':question/problem'];F=scalar(re.search(r'\$f\([^$]*?\)=(.*?)\$',text)[1]);v=re.search(r'r\(t\)=⟨(.*?)⟩',text)[1];curve=tuple(scalar(c) for c in v.replace(r'\,','').split(','));a,b=re.search(r't\\in \[(.*?),(.*?)\]',text).groups();bounds=(scalar(a),scalar(b));assert bounds[1]>bounds[0];pull=s.trigsimp(s.expand(F.subs({x:curve[0],y:curve[1]},simultaneous=True)));speed=p.on_interval(p.speed(curve),bounds);return F,curve,bounds,pull,speed,s.trigsimp(s.expand(pull*speed))
def vector(raw):return p.vector(raw)
def splitcomponents(raw):
 raw=raw.replace(r'\left','').replace(r'\right','').replace('[','(').replace(']',')');assert raw[0]=='(';dep=1;j=1
 while dep:dep+=(raw[j]=='(')-(raw[j]==')');j+=1
 assert raw[j:j+2]=='-(' and raw[-1]==')';result=[]
 for body in (raw[1:j-1],raw[j+2:-1]):
  pieces=[];dep=0;start=0
  for k,c in enumerate(body):
   dep+=(c in '({')-(c in ')}')
   if c=='+' and dep==0:pieces.append(scalar(body[start:k]));start=k+1
  pieces.append(scalar(body[start:]));result.append(pieces)
 return result
def check(rec,C):
 q=rec['question'];F,curve,bounds,pull,speed,I=prompt(q);G=groups(q[':question/worked-solution']);assert len(G)==3;d=[s.diff(c,t) for c in curve];assert right(G[0][0]).count(r'\frac{\text{d}')==2
 op=right(G[0][1]);ops=[]
 for match in re.finditer(r'\\frac\{\\text\{d\}\}\{\\text\{d\}t\}\(',op):
  st=match.end();j=st;dep=1
  while dep:dep+=(op[j]=='(')-(op[j]==')');j+=1
  ops.append(scalar(op[st:j-1]))
 assert len(ops)==2 and all(equal(a,b) for a,b in zip(ops,curve));C['formal_components']+=2
 for idx,row in enumerate(G[0][2:]):
  if r'\|' in row:assert right(row).count(r'\frac{\text{d}')==2;mode='norm';continue
  if idx==0 or (idx==1 and rec['generation']['template']=='involute'):
   actual=vector(right(row));assert all(equal(a,b) for a,b in zip(actual,d+[s.Integer(0)]));C['derivative_components']+=2
  else:assert equal(scalar(right(row)),speed,bounds),(right(row),speed);C['speed_rows']+=1
 for row in G[1]:assert equal(scalar(right(row)),pull,bounds);C['pullback_rows']+=1
 P=None;answer=None;roles=[]
 for row in G[2][1:]:
  raw=right(row)
  if r'\int' in raw:
   aa,bb,fn,var=e.integral(raw);assert var==t and equal(aa,bounds[0]) and equal(bb,bounds[1]) and equal(fn,I,bounds),(raw,fn,I);C['integral_rows']+=1;roles.append('integral')
  elif r'\right]' in raw:
   converted=raw.replace(r'\left[','(').replace(r'\right]',')|');prim,var,aa,bb,val=e.evaluated(converted);assert var==t and equal(aa,bounds[0]) and equal(bb,bounds[1]) and equal(s.diff(prim,t),I,bounds);assert P is None or equal(P,prim);P=prim;answer=val;C['primitive_rows']+=1;roles.append('primitive')
  else:
   assert answer is not None and equal(scalar(raw),answer),(raw,answer);C['evaluation_rows']+=1;roles.append('evaluation')
 assert P is not None;upper,lower=splitcomponents(right(G[2][-2]));um,lm=splitcomponents(right(G[2][-3]));terms=s.Add.make_args(s.expand(P));assert len(upper)==len(lower)==len(um)==len(lm)==len(terms)
 for actual,prior,bound in ((upper,um,bounds[1]),(lower,lm,bounds[0])):
  expected=[s.simplify(term.subs(t,bound)) for term in terms];assert all(equal(a,b) for a,b in zip(actual,prior));assert sorted(map(str,map(s.simplify,actual)))==sorted(map(str,expected));C['individual_endpoint_components']+=len(actual)
 def integrate(fn):return s.simplify(s.integrate(s.trigsimp(s.expand(fn)),(t,*bounds)))
 family=rec['generation']['template'];expected=[answer,integrate(pull),integrate(pull*speed**2)]
 if family=='sum':
  c=s.diff(F,x);offset=s.expand(curve[1]).coeff(t,0);expected +=[integrate((pull-c*offset)*speed),integrate(c*curve[1]*speed)]
 elif family=='reciprocal':
  offset=s.simplify(curve[1]-curve[0]);c=s.simplify(F*(y-x));expected +=[-answer,integrate(c*offset*speed)]
 elif family=='circle_cos':
  c=s.expand(F).coeff(x,2)/2;expected +=[2*answer,integrate(2*c*curve[0]**2*speed)]
 elif family=='circle_sin':
  c=s.expand(F).coeff(y,2);rad=scalar(str(speed));wrong=c*rad**3*(t/2+s.sin(2*t)/4);wrongchain=c*rad**3*(t/2-s.sin(2*t)/2);expected +=[s.simplify(wrong.subs(t,bounds[1])-wrong.subs(t,bounds[0])),s.simplify(wrongchain.subs(t,bounds[1])-wrongchain.subs(t,bounds[0]))]
 elif family=='cubic':
  c=s.expand(F).coeff(x,3);cy=s.expand(F).coeff(y,3);expected +=[integrate(c*(curve[0]**3-curve[1]**3)*speed),integrate((c*curve[0]**3-cy*curve[1]**3)*speed)]
 elif family=='fractional':
  scale=s.expand(curve[1]).coeff(t,2)*2;c=s.diff(F,x);wrong=s.Rational(4,3)*c*scale**2*(t**s.Rational(7,2)/s.Rational(5,2)+t**s.Rational(5,2)/s.Rational(3,2));expected +=[integrate(pull*scale*t),s.simplify(wrong.subs(t,bounds[1])-wrong.subs(t,bounds[0]))]
 elif family=='mixed_fractional':expected +=[integrate(s.diff(F,x)*curve[0]*speed),integrate(s.diff(F,y)*curve[1]*speed)]
 else:
  c=s.expand(F).coeff(x,2);const=F.subs({x:0,y:0});A=s.simplify(speed/t);expected +=[integrate((pull-const)*speed),integrate((c*A*A+const)*speed)]
 f=q[':question/answer-fields'][0];values=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5 and all(sum(equal(v,w) for v in values)==1 for w in expected);assert next(a[':answer/id'] for a in f[':answer-field/choices'] if equal(scalar(a[':answer/value']),answer))==f[':answer-field/correct'][1];C['choices']+=5;C['banks']+=1;C['records']+=1
 return roles
if __name__=='__main__':
 g=base.load(D.with_suffix('.py'),'direct_scalar_generator');source=base.raw(g,K,D);C={k:0 for k in ('records','formal_components','derivative_components','speed_rows','pullback_rows','integral_rows','primitive_rows','evaluation_rows','individual_endpoint_components','choices','banks')};records=json.loads((R/f'qa/{K}-sampled.json').read_text());families={}
 for family,level in g.TEMPLATES.items():records.append(g.generate(level,template=family,seed=937))
 for rec in records:
  roles=check(rec,C);family=rec['generation']['template'];assert family not in families or families[family]==roles;families[family]=roles
 out=dict(status='passed',source=source,readback=C,operative_families=families,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
