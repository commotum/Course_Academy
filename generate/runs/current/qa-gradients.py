"""Independent parent readback: actual functions, partial stages and exact gradients."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(z);z.loader.exec_module(g);return g
p=load(R/'ode-scalar-parser.py','gradienttaskparser');axes=(p.x,p.y,p.z);basis=(p.i,p.j,p.k)
def equal(a,b):return s.simplify(a-b)==0
def scalar(raw):
 raw=re.sub(r'\\(?:text|mathrm)\{[^}]*\}','',raw).replace(r'\mathbf','').replace('\xa0','').replace(r'\dfrac',r'\frac').replace(r'\;','').replace(r'\!','').replace(r'\:','')
 return p.scalar(raw.replace(r'\operatorname{atan}',r'\operatorname{arctan}'))
def vector(raw):
 raw=re.sub(r'⟨([^⟩]*)⟩',lambda m:'('+ '+'.join('('+v+')'+b for v,b in zip(m[1].replace(r'\,','').split(','),'ijk'))+')',raw)
 e=s.expand(scalar(raw));v=tuple(e.coeff(b) for b in basis);assert equal(e,sum(a*b for a,b in zip(v,basis))),('not vector',raw,e);return v
def same(v,w):return len(v)==len(w) and all(equal(a,b) for a,b in zip(v,w))
def task(q):
 t=q[':question/problem'];m=re.search(r'\$([fgh])\(x,\s*y(?:,\s*z)?\)\s*=\s*(.*?)\$',t);assert m,t
 n=3 if re.search(r'[fgh]\(x,\s*y,\s*z\)',t) else 2;F=scalar(m[2]);point=None
 m=re.search(r'(?:at|at the point)\s*\$\((.*?)\)',t)
 if m:point=tuple(scalar(z) for z in m[1].replace(r'\,','').split(','));assert len(point)==n
 D=tuple(s.diff(F,a) for a in axes[:n]);V=tuple(d.subs(dict(zip(axes,point)),simultaneous=True) for d in D) if point else D
 return F,D,V,point,n
def replace_named(raw,F,n):
 def partial(m):
  args=[scalar(z) for z in m[3].replace(r'\,','').split(',')];assert len(args)==n
  return '('+s.latex(s.diff(F,axes['xyz'.index(m[2])]).subs(dict(zip(axes,args)),simultaneous=True),ln_notation=True)+')'
 raw=re.sub(r'\{?([fgh])\}?_\{?([xyz])\}?\(([^()]*)\)',partial,raw)
 def grad(m):
  args=[scalar(z) for z in m[1].replace(r'\,','').split(',')];assert len(args)==n
  return '('+s.latex(sum(s.diff(F,a).subs(dict(zip(axes,args)),simultaneous=True)*b for a,b in zip(axes[:n],basis)),ln_notation=True)+')'
 return re.sub(r'(?:∇|\\nabla\s*)[fgh]\(([^()]*)\)',grad,raw)
def raw_source(g,k):
 original=json.loads((R/f'sources/{k}.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text());counts=dict(prompts=0,solutions=0,fields=0,values=0,keys=0,literal_values=0)
 for c in cases:
  q0=next(q for q in original if c['source_id'] in (q[':db/id'],q[':question/id'],q[':question/math-academy-id']));lv=q0.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/moderate').split('/')[-1]
  q=g.generate(lv,template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile')))['question']
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in q)==(key in q0),(k,c,key)
   if key in q and key!=':question/answer-fields':assert q[key]==(q0[key].get(':db/ident') if isinstance(q0[key],dict) else q0[key]),(k,c,key)
  counts['prompts']+=1;counts['solutions']+=(':question/worked-solution' in q0)
  for f,f0 in zip(q[':question/answer-fields'],q0[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];vals=[a[':answer/value'] for a in f[':answer-field/choices']];old=[a[':answer/value'] for a in f0[':answer-field/choices']];counts['literal_values']+=sum(v in old for v in vals);remaining=[(scalar(v),) if f[':answer-field/type'].endswith('/blank') else vector(v) for v in old]
   for val in vals:
    v=(scalar(val),) if f[':answer-field/type'].endswith('/blank') else vector(val);i=next((j for j,w in enumerate(remaining) if same(v,w)),None);assert i is not None,(k,c,val,old);remaining.pop(i)
   assert not remaining;assert (':answer-field/correct' in f)==(':answer-field/correct' in f0);counts['fields']+=1;counts['values']+=len(f[':answer-field/choices'])
   if ':answer-field/correct' in f:
    a=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);b=f0[':answer-field/correct'][':answer/value'];assert equal(scalar(a),scalar(b)) if f[':answer-field/type'].endswith('/blank') else same(vector(a),vector(b));counts['keys']+=1
 return counts
def bank_readback(k,r,F,D,V,point,n):
 t=r['generation']['template'];x,y,z=axes;A,B=V[:2];ev=lambda e:s.simplify(e.subs(dict(zip(axes,point)),simultaneous=True)) if point else e
 if k==17592186124443:
  if t=='components':return None
  if t=='root':bank=[V,(A/2,B),(A,2*B),(B,A),(A,-B)]
  elif t=='atan_product':
   a=s.simplify(F/(x*s.atan(y)));bank=[V,(A/a,B),(A,B/a),(B,A),(-A,B)]
  elif t=='radial_log':bank=[V,(A/2,B),(2*A,B),(B,A),(-A,B)]
  elif t=='polynomial':
   poly=s.Poly(F,x,y);a=poly.coeff_monomial(x*x);b=poly.coeff_monomial(x*y);c=poly.coeff_monomial(y*y);u,v=point;bank=[(2*a*u,2*c*v),(-b*v,b*u),V,(-b*v,2*c*v),(2*a*u,2*c*v+b*u)]
  elif t=='log_cos':
   co=next(iter(F.atoms(s.cos)));power=co.args[0];n0=s.degree(power,y);b=F.coeff(co);a=F.coeff(s.log(x*y));bank=[(a*x,a*y-b*n0*s.sin(power)),V,(a/x,a/y+b*s.diff(power,y)*s.sin(y)),(a/x,a/y),(a/x,s.diff(power,y)*(a/y-b*s.sin(power)))]
  elif t=='sin_log':
   a=F.coeff(s.sin(x*y));N=s.expand(F-a*s.sin(x*y)).coeff(s.log(y));nx=s.diff(N,x);bank=[(a*y*s.sin(x*y)+nx*s.log(y),a*x*s.sin(x*y)+N/y),(a*x*s.cos(x*y)+nx*s.log(y),a*y*s.cos(x*y)+N/y),(a*y*s.cos(x*y),N/y),(a*x*s.sin(x*y)+nx*s.log(y),a*y*s.sin(x*y)+N/y),V]
  elif t=='atan_ratio':
   arg=next(iter(F.atoms(s.atan))).args[0];k0=s.simplify(y/(x*arg));den=k0*k0*x*x+y*y;bank=[(-k0*x/den,k0*y/den),(k0*x/den,-k0*y/den),(-k0*y*y/den,k0*x*x/den),V,(-A,-B)]
  elif t=='quotient':
   N,den=s.fraction(F);k0=-s.diff(den,y);a=s.diff(N,x);b=s.diff(N,y);c=a*k0+b;bank=[V,(-c*x/den**2,c*y/den**2),(c*y/den**2,c*x/den**2),(-c*x,c*y),(-c*y,c*x)]
  else:
   N,den=s.fraction(F);bank=[V,tuple(ev(s.diff(N,a)/den) for a in axes[:n]),(ev((s.diff(N,x)*den+N*s.diff(den,x))/den**2),B),(A,ev((s.diff(N,y)*den+N*s.diff(den,y))/den**2)),(B,A)]
 else:
  if t=='polynomial':
   terms=[s.expand(F).coeff(a,s.degree(F,a))*a**s.degree(F,a) for a in axes];bank=[V,tuple(term/a for term,a in zip(terms,axes)),*[tuple(-d if i==j else d for j,d in enumerate(V)) for i in range(3)]]
  elif t=='quotient':
   N,den=s.fraction(F);bank=[V,tuple(ev((den*s.diff(N,a)+N*s.diff(den,a))/den**2) for a in axes),tuple(ev(s.diff(N,a)*den-N*s.diff(den,a)) for a in axes),tuple(ev(-N*s.diff(den,a)/den**2) for a in axes),tuple(ev(s.diff(N,a)/den) for a in axes)]
  elif t=='log_point':bank=[V,tuple(2*a for a in V),*[tuple(-d if i==j else d for j,d in enumerate(V)) for i in range(3)]]
  elif t=='expcos_point':
   E=ev(s.exp(x*y));a,b,c=point;bank=[V,tuple(d/E for d in V),tuple(E*d for d in V),tuple(-d for d in V),(V[0],E*(b*s.cos(b*c)-c*s.sin(b*c)),V[2])]
  elif t=='sine_point':bank=[V,*[tuple(-d if i==j else d for j,d in enumerate(V)) for i in range(3)],tuple(-d for d in V)]
  elif t=='sqrt_product':
   u,v,w=[a+s.Integer(d) for a,d in zip(axes,r['generation']['parameters']['shifts'])];assert equal(F,s.sqrt(u*v*w));bank=[V,tuple(2*d for d in V),(v*w/2,u*w/2,u*v/2),(F*u/2,F*v/2,F*w/2),(1/(2*F),F/(2*v),F/(2*w))]
  elif t=='product_log':bank=[V,(F,F,V[2]),(V[0],F,V[2]),(V[0],V[1],F),(V[1],V[0],V[2])]
  else:
   # These five defensible observed whole banks transform with the actual
   # function's translated arguments. Verify that translation independently.
   cases=json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text());c=next(c for c in cases if c['template']==t);orig=json.loads((R/f'sources/{k}.json').read_text())['record'][':knowledge-point/questions'];q0=next(q for q in orig if c['source_id'] in (q[':db/id'],q[':question/id'],q[':question/math-academy-id']));F0=task(q0)[0];sub=dict(zip(axes,[a+s.Integer(d) for a,d in zip(axes,r['generation']['parameters']['shifts'])]));assert equal(F,F0.subs(sub,simultaneous=True));bank=[tuple(e.subs(sub,simultaneous=True) for e in vector(a[':answer/value'])) for a in q0[':question/answer-fields'][0][':answer-field/choices']]
 return [tuple(v)+(s.S.Zero,)*(3-len(v)) for v in bank]

def check(k):
 g=load(ROOT/f'generate/scratch/{k}.py','gradientg'+str(k));src=raw_source(g,k);records=json.loads((R/f'qa/{k}-sampled.json').read_text());stats=dict(records=0,formal_partials=0,scalar_stages=0,vector_stages=0,choices=0)
 for r in records:
  q=r['question'];sol=q[':question/worked-solution']
  if r['generation']['template']=='components':
   t=q[':question/problem'];m=re.search(r'E_x=([^$]+)\$ and \$E_y=([^$]+)',t);assert m,t;V=(scalar(m[1]),scalar(m[2]));F=None;D=V;point=None;n=2
  else:F,D,V,point,n=task(q)
  current=None;evaluated=False
  for block in re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S):
   if not r'\begin{aligned}' in block:continue
   for row in block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
    lhs,rhs=re.split(r'&\s*=',row,maxsplit=1);lhs=lhs.strip();rhs=rhs.strip().rstrip('.,')
    m=re.search(r'\{?[fgh]\}?_\{?([xyz])\}?|\\frac\{∂[fgh]\}\{∂([xyz])\}',lhs)
    if m:
     current='xyz'.index(m[1] or m[2]);evaluated=False
    elif '∇' in lhs or r'\nabla' in lhs:
     current=None
     if F is not None:
      args=re.search(r'[fgh]\(([^()]*)\)',lhs)
      if args:
       av=tuple(scalar(z) for z in args[1].replace(r'\,','').split(','));evaluated=av!=axes[:n]
       if evaluated:assert point is not None and same(av,point),(k,lhs,point)
    formal=re.fullmatch(r'\\frac\{∂\}\{∂([xyz])\}\((.*)\)',rhs,re.S)
    if formal:
     assert current=='xyz'.index(formal[1]);assert equal(scalar(formal[2]),F);stats['formal_partials']+=1;continue
    if F is None:rhs=rhs.replace('E_x',str(V[0])).replace('E_y',str(V[1]))
    else:rhs=replace_named(rhs,F,n)
    if current is not None:
     assert equal(scalar(rhs),D[current]),(k,r['generation']['template'],row,D[current]);stats['scalar_stages']+=1
    else:
     expected=(V if evaluated or F is None else D)+(s.S.Zero,)*(3-n)
     assert same(vector(rhs),expected),(k,r['generation']['template'],row,expected);stats['vector_stages']+=1
  for index,f in enumerate(q[':question/answer-fields']):
   vals=[]
   for a in f[':answer-field/choices']:
    v=(scalar(a[':answer/value']),) if f[':answer-field/type'].endswith('/blank') else vector(a[':answer/value']);want=(V[index],) if len(v)==1 else V+(s.S.Zero,)*(3-n)
    assert same(v,want)==(a[':answer/id']==f[':answer-field/correct'][1]),(k,a,want);assert not any(same(v,w) for w in vals);vals.append(v);stats['choices']+=1
  bank=bank_readback(k,r,F,D,V,point,n)
  if bank is not None:
   actual=[vector(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']];assert len(actual)==len(bank) and all(any(same(v,w) for w in bank) for v in actual),(k,r['generation']['template'],actual,bank);stats['complete_method_banks']=stats.get('complete_method_banks',0)+1
  stats['records']+=1
 out=dict(status='passed',kp_id=k,source=src,readback=stats,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest());(R/f'qa/{k}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':
 for k in map(int,sys.argv[1:]):check(k)
