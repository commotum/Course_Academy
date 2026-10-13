"""Root complete rational slope relations on an implicit conic, no generator code."""
import importlib.util,re
from pathlib import Path
import sympy as s
z=importlib.util.spec_from_file_location('p',Path(__file__).with_name('ode-scalar-parser.py'));p=importlib.util.module_from_spec(z);z.loader.exec_module(p)
x,y=p.x,p.y

def scalar(tex):return p.scalar(tex.strip().rstrip('.,').replace(r'\dfrac',r'\frac'))
def slope(relation):return -s.diff(relation,x)/s.diff(relation,y)
def same_on_curve(a,b,relation):
 numerator=s.together(a-b).as_numer_denom()[0];return s.groebner([relation],x,y,domain='EX').reduce(s.expand(numerator))[1]==0
