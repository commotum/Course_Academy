"""Root reader of actual particular-solution ODEs, conditions and full fragments."""
import importlib.util,re
from functools import lru_cache
from pathlib import Path
import sympy as s
sp=importlib.util.spec_from_file_location('root_particular_scalar',Path(__file__).with_name('ode-scalar-parser.py'));p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
X=p.x;F=p.u;DF=p.v;C=p.z;SUB=p.t

def normalize(raw):
 raw=raw.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').strip().rstrip('.,').replace('⁡','')
 raw=raw.replace(r'\frac{\text{d}y}{\text{d}x}','v')
 raw=re.sub(r'\{?[fgy]\}?\^\{′\}(?:\(x\))?|[fgy]\x27(?:\(x\))?', 'v',raw)
 raw=raw.replace('f(x)','@@F@@').replace('g(x)','@@F@@')
 raw=re.sub(r'\\[A-Za-z]+|[Cyu]',lambda m:m[0] if m[0].startswith('\\') else {'C':'z','y':'@@F@@','u':'t'}[m[0]],raw).replace('@@F@@','u')
 raw=re.sub(r'\|([^|]+)\|',r'Abs(\1)',raw)
 return raw

def expression(raw):
 raw=normalize(raw)
 while r'\int' in raw:
  i=raw.index(r'\int');m=re.search(r'\\text\{d\}([xtu])',raw[i+4:]);assert m,raw;j=i+4+m.start();end=i+4+m.end();var=X if m[1]=='x' else SUB;body=p.scalar(raw[i+4:j]) if raw[i+4:j].replace(r'\,','').strip() else s.Integer(1);a=s.expand(body).coeff(DF);assert not a.has(X,SUB);rest=s.expand(body-a*DF);assert not rest.has(DF,F)
  primitive=F if m[1]=='u' else a*F+sum(s.integrate(v,var) for v in s.Add.make_args(s.expand(rest)));assert m[1]!='u' or body==1;raw=raw[:i]+'('+s.latex(primitive).replace(r'\log',r'\ln')+')'+raw[end:]
 return p.scalar(raw)
def problem(prompt):
 ic=re.search(r'([fgy])\(([^)]*)\)\s*=\s*(-?\d+)',prompt);assert ic,prompt;name=ic[1];t=expression(ic[2]);v=s.Integer(ic[3]);assert not t.free_symbols
 blocks=re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',prompt,re.S);eq=next(a or b for a,b in blocks if 'v' in normalize(a or b));left,right=eq.split('=',1);res=s.expand(expression(left)-expression(right));coeff=res.coeff(DF);assert coeff!=0 and not coeff.has(F,DF,C);G=s.cancel(-(res-coeff*DF)/coeff);assert not G.has(F,DF,C);assert G.subs(X,t).is_finite;return G,t,v,name

def interval(expr,t):
 # The only observed logarithmic absolute argument is 1+2x. The IVP's
 # connected interval excludes its root, so the initial sign holds throughout.
 return expr.replace(lambda z:z.func==s.Abs and z.args[0]==1+2*X and z.args[0].subs(X,t)>0,lambda z:z.args[0])
def equal(a,b,t):return s.simplify(interval(a-b,t))==0
@lru_cache(maxsize=None)
def derivative(v):
 d=s.diff(v,X);d=d.replace(lambda z:z.func==s.sign,lambda z:z.args[0]/s.Abs(z.args[0]));return s.cancel(s.expand(d))
def primitive(G):return sum(s.integrate(v,X) for v in s.Add.make_args(s.expand(G)))
def responses(q,name):
 f=q[':question/answer-fields'][0];kind=(f[':answer-field/type'].get(':db/ident') if isinstance(f[':answer-field/type'],dict) else f[':answer-field/type']).split('/')[-1];vals=[]
 for a in f[':answer-field/choices']:
  if kind=='radio':
   lhs,rhs=a[':answer/value'].split('=',1);assert lhs.strip()==('y' if name=='y' else name+'(x)');vals.append(expression(rhs))
  else:vals.append(expression(a[':answer/value']))
 prefix=0
 if kind=='blank':
  assert len(vals)==1;m=re.search(r'\$[^$]*?=([^$]*)\$\{\{'+re.escape(f[':answer-field/key'])+r'\}\}',q[':question/problem']);assert m;qprefix=m[1].replace(r'\,','').strip().rstrip('+');prefix=expression(qprefix) if qprefix else 0
 return vals,[v+prefix for v in vals]
