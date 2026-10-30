"""Small exact-notation reader retained from the original generator."""
import re
from functools import lru_cache
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
T=sp.Symbol('t',real=True)
@lru_cache(maxsize=2048)
def scalar(s):
    """Small independent parser for the observed exact scalar/polynomial notation."""
    s=s.strip().rstrip('.,').replace('−','-').replace('\u2061','').replace(r'\,','').replace(r'\left','').replace(r'\right','')
    s=re.sub(r'\\operatorname\{(sin|cos|tan)\}',r'\1',s)
    s=re.sub(r'\\(sin|cos|tan)',r'\1',s)
    def group(i):
        assert s[i]=='{'; n=1;j=i+1
        while n:
            if s[j]=='{':n+=1
            elif s[j]=='}':n-=1
            j+=1
        return s[i+1:j-1],j
    while r'\frac' in s or r'\sqrt' in s:
        hits=[(s.find(z),z) for z in (r'\frac',r'\sqrt') if z in s];i,z=min(hits)
        a,j=group(i+len(z))
        if z==r'\frac':b,j=group(j);replacement=f'(({scalar(a)})/({scalar(b)}))'
        else:replacement=f'sqrt({scalar(a)})'
        s=s[:i]+replacement+s[j:]
    s=s.replace(r'\pi','pi').replace('{','(').replace('}',')').replace('^','**')
    return sp.simplify(parse_expr(s,local_dict={'t':T,'pi':sp.pi,'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,)))
