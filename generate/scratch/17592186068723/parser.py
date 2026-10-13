"""Independent bounded TeX parser for displayed algebra; rejects leftover commands."""
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
X=sp.Symbol('x',real=True)
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)
def group(s,i):
    if s[i]!='{':raise ValueError('expected group')
    depth=1;j=i+1
    while depth:
        depth+=(s[j]=='{')-(s[j]=='}');j+=1
    return s[i+1:j-1],j
def scalar(s):
    s=s.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').strip().rstrip('.,')
    while r'\frac' in s or r'\sqrt' in s:
        indices=[(s.find(cmd),cmd)for cmd in (r'\frac',r'\sqrt')if cmd in s];i,cmd=min(indices)
        a,j=group(s,i+len(cmd))
        if cmd==r'\frac':
            b,j=group(s,j);value='(('+a+')/('+b+'))'
        else:value='sqrt('+a+')'
        s=s[:i]+value+s[j:]
    if '\\' in s:raise ValueError('unparsed TeX '+s)
    s=s.replace('{','(').replace('}',')')
    s=re.sub(r'(?<=[x0-9)])sqrt\(',r'*sqrt(',s)
    return parse_expr(s,local_dict={'x':X,'C':sp.Symbol('C'),'u':sp.Symbol('u',positive=True),'sqrt':sp.sqrt},transformations=TRANS)
def prompt(text):
    raw=re.search(r'\\int\s*(.*?)\\(?:text|textrm)\{d\}x',text)
    if not raw:
        raw=re.search(r'\\int\s*(.*?)dx',text)
    if not raw:raise ValueError('integrand not found')
    return scalar(raw[1])
def same(a,b):
    # Power denesting is valid on the explicit positive-inner root domain.
    return sp.simplify(sp.powdenest(a-b,force=True))==0
