"""Root fail-closed readback of same-angle sine/cosine polynomial identities."""
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('p',Path(__file__).with_name('ode-scalar-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
S,C=s.symbols('S C',real=True);basis=s.groebner([C**2+S**2-1],C,S)
def scalar(tex):
 tex=tex.replace(r'\theta','t').replace('θ','t');tex=re.sub(r'(?<![A-Za-z])x(?![A-Za-z])','t',tex)
 value=p.scalar(tex);funcs=value.atoms(s.sin,s.cos);assert all(f.args[0]==p.t for f in funcs),('Unexpected angle workload',tex,funcs)
 value=value.subs({s.sin(p.t):S,s.cos(p.t):C});assert value.free_symbols<={S,C};return s.Poly(s.expand(value),C,S,domain='QQ').as_expr()
def canonical(poly):return basis.reduce(s.expand(poly))[1]
def equal(a,b):return canonical(a-b)==0
