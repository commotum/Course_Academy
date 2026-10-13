"""Independent parser for the deliberately bounded displayed expression grammar."""
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
X=sp.Symbol('x',positive=True)
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)
def group(s,start):
    if s[start]!='{':raise ValueError('expected TeX group')
    n=1;j=start+1
    while n:
        if s[j]=='{':n+=1
        elif s[j]=='}':n-=1
        j+=1
    return s[start+1:j-1],j

def scalar(s):
    s=s.replace(r'\,','').strip().rstrip('.,').replace('⁡','').replace('−','-')
    s=s.replace(r'\frac{\text{d}y}{\text{d}x}','D').replace(r'\frac{\text{d}}{\text{d}x}','D')
    s=s.replace(r'\operatorname{ln}',r'\ln').replace(r'\operatorname{log}',r'\log').replace('{log}',r'\log')
    s=s.replace('ln','LOG').replace(r'\LOG','LOG')
    s=re.sub(r'LOG\s*(\d+|x)(?![A-Za-z])',r'log(\1)',s).replace('LOG','log')
    s=re.sub(r'\\log_\{(\d+)\}\s*(?:\{x\}|x)',r'(log(x)/log(\1))',s)
    s=re.sub(r'\\log_(\d+)\s*x',r'(log(x)/log(\1))',s)
    s=re.sub(r'\\log\s*x',r'(log(x)/log(10))',s)
    while r'\frac' in s:
        i=s.index(r'\frac');a,j=group(s,i+5);b,k=group(s,j);s=s[:i]+'(('+a+')/('+b+'))'+s[k:]
    s=s.replace(r'\cdot','*').replace(r'\,','').replace(r'\left','').replace(r'\right','')
    s=s.replace(r'\log', 'log')
    s=s.replace('{','(').replace('}',')').replace('^','**')
    s=re.sub(r'(?<=x)log\(', '*log(',s)
    s=re.sub(r'(?<![A-Za-z])e(?![A-Za-z])','E',s)
    return parse_expr(s,local_dict={'x':X,'E':sp.E,'log':sp.log,'D':lambda f:sp.diff(f,X)},transformations=TRANS)

def prompt(text):
    m=re.search(r'y\s*=([^$]+)\$',text)
    if not m:raise ValueError('missing printed function')
    f=scalar(m[1].rstrip(', '))
    m=re.search(r'at \$x\s*=\s*([^$]+)\$',text)
    if not m:raise ValueError('missing tangent input')
    t=scalar(m[1].rstrip('. '))
    return f,t

def same(a,b):
    d=sp.cancel(sp.expand_log(sp.expand_power_exp(a-b),force=True))
    if d==0:return True
    if d.is_zero is False:return False
    # A single exact counterexample disproves identity; avoid heuristic identity
    # searches for visibly different exponential functions.
    for point in (0,1,2):
        test=sp.cancel(sp.expand_log(d.subs(X,point),force=True))
        if test.is_zero is False:return False
    return d.equals(0) is True
