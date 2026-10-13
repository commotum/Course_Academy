"""Parent's fail-closed reader of printed first-order ODE and integral stages."""
import importlib.util,re
from functools import lru_cache
from pathlib import Path
import sympy as s
sp=importlib.util.spec_from_file_location('root_direct_scalar',Path(__file__).with_name('ode-scalar-parser.py'));p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p);X=p.x;F=p.u;DF=p.v;CONST=p.z

def normalize(raw):
 raw=raw.strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace('⁡','').replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
 for derivative in [r'\frac{\text{d}y}{\text{d}x}',r'{f}^{′}(x)',r'f^{′}(x)',"f'(x)",r'f\prime(x)']:raw=raw.replace(derivative,'v')
 raw=raw.replace('f(x)','u');raw=re.sub(r'\\[A-Za-z]+|[Cy]',lambda m:m[0] if m[0].startswith('\\') else {'C':'z','y':'u'}[m[0]],raw)
 raw=re.sub(r'\|([^|]+)\|',r'Abs(\1)',raw)
 return raw.strip().rstrip('.,')

def expression(raw):
 raw=normalize(raw);integrals={}
 while r'\int' in raw:
  i=raw.index(r'\int');match=re.search(r'\\(?:text|mathrm)\{d\}x',raw[i+4:]);assert match,raw;j=i+4+match.start();end=i+4+match.end();body=p.scalar(raw[i+4:j]) if raw[i+4:j].strip() else s.Integer(1);coeff=s.expand(body).coeff(DF);assert not coeff.has(X);rest=s.expand(body-coeff*DF);assert not rest.has(F,DF)
  primitive=coeff*F+sum(s.integrate(term,X) for term in s.Add.make_args(s.expand(rest)));symbol=['i','j','k'][len(integrals)];integrals[p.locals_[symbol]]=primitive;raw=raw[:i]+'('+symbol+')'+raw[end:]
 return p.scalar(raw).subs(integrals)

def forcing(prompt):
 maths=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',prompt,re.S);eq=next(z for z in maths if '=' in z);left,right=eq.split('=',1);residual=expression(left)-expression(right);coeff=s.expand(residual).coeff(DF);assert coeff!=0 and not coeff.has(X,F,DF);rest=s.expand(residual-coeff*DF);assert not rest.has(DF);G=s.expand(-rest/coeff);assert not G.has(F,DF,CONST);return G

@lru_cache(maxsize=None)
def derivative(expr):
 val=s.diff(expr,X)
 # sign(h)=h/Abs(h) off h=0; log absolute-value solutions are considered
 # on connected intervals avoiding their poles, as the source requires.
 val=val.replace(lambda v:v.func==s.sign,lambda v:v.args[0]/s.Abs(v.args[0]));return s.cancel(s.expand(val))

def family(choice):
 left,right=choice.split('=',1);residual=s.expand(expression(left)-expression(right));coeff=residual.coeff(F);assert coeff!=0 and not coeff.has(X,F,DF,CONST);rest=s.expand(residual-coeff*F);assert not rest.has(F);v=s.expand(-rest/coeff);assert not v.has(F,DF);return v
