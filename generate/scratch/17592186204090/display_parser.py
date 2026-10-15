"""Private frozen rendered-TeX reader, independent of generator formulas."""
import re
from functools import lru_cache
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
SYMBOLS={c:sp.Symbol(c) for c in 'abcpqr stxyz'.replace(' ','')}

@lru_cache(None)
def expression(text):
 text=text.strip().rstrip('.,').replace('&','').replace(r'\,','').replace(' ','')
 text=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',lambda m:'('+m[1]+')/('+m[2]+')',text)
 if not re.fullmatch(r'[a-z0-9()+*/.\-]+',text):raise ValueError('Unexpected rendered expression '+text)
 return parse_expr(text,local_dict=SYMBOLS,transformations=standard_transformations+(implicit_multiplication_application,),evaluate=True)

@lru_cache(None)
def equation(text):
 if text.count('=')!=1:raise ValueError('Equation must have one equals sign')
 left,right=text.split('=');return expression(left),expression(right)

def blocks(prose):return re.findall(r'\$\$\s*([\s\S]*?)\s*\$\$',prose)

def rows(tex):
 tex=tex.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
 return [x.strip() for x in tex.split(r'\\') if x.strip()]

@lru_cache(None)
def value(text):
 x=sp.simplify(expression(text).doit())
 if x.free_symbols or not x.is_Rational:raise ValueError('A finite exact rational is required')
 return sp.Rational(x)
