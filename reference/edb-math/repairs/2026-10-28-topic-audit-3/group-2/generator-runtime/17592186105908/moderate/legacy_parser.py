"""Scalar parser reused from the supplied legacy generator."""
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
TRANS=standard_transformations+(implicit_multiplication_application,)
def parse_math(s):
    """Independent scalar TeX reader, also used by displayed-stage validators."""
    s=str(s).strip().strip('$').rstrip('.')
    while r'\frac' in s or r'\sqrt' in s:
        # innermost commands first (groups without commands are sufficient here)
        old=s
        s=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',lambda m:'(('+m[1]+')/('+m[2]+'))',s)
        s=re.sub(r'\\sqrt\{([^{}]*)\}',lambda m:'sqrt('+m[1]+')',s)
        if s==old: raise ValueError('Unsupported TeX '+s)
    s=s.replace(r'\cdot','*').replace(r'\,','').replace('^','**').replace('{','(').replace('}',')')
    return parse_expr(s,transformations=TRANS)

