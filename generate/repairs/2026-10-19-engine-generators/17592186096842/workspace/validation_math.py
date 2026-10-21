#!/usr/bin/env python3
"""Independent displayed-math, source fidelity, identity and native grading audit."""
from pathlib import Path
import importlib.util,json,re,subprocess,hashlib,sys,itertools
import sympy as sp
from functools import lru_cache
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parent
import generator as g
x=sp.Symbol('x',real=True);u=sp.Symbol('u',positive=True)
DY,DU,UX=sp.symbols('DY DU UX')
TRANS=standard_transformations+(implicit_multiplication_application,)

@lru_cache(maxsize=40000)
def displayed(latex):
    """Small independent parser for the observed algebra grammar, not answer metadata.

    Braced closing delimiters are valid source TeX grouping, normalized here.
    No antlr dependency or numeric answer lookup is used.
    """
    latex=re.sub(r'\\frac([0-9])([0-9])',r'\\frac{\1}{\2}',latex)
    s=latex.replace(r'\,','').strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace('{)}',')').replace(r'\cdot','*')
    for a,b in [(g.D,'DY'),(g.DU,'DU'),(g.UX,'UX')]:s=s.replace(a,b)
    def group(i):
        assert s[i]=='{',repr(s)
        depth=1;j=i+1
        while depth:
            if s[j]=='{':depth+=1
            if s[j]=='}':depth-=1
            j+=1
        return s[i+1:j-1],j
    out='';i=0
    while i<len(s):
        if s.startswith(r'\frac',i):
            first,j=group(i+5);second,i=group(j)
            out+='(('+str(displayed(first))+')/('+str(displayed(second))+'))'
        elif s.startswith(r'\sqrt',i):
            arg,i=group(i+5);out+='sqrt('+str(displayed(arg))+')'
        elif s[i]=='{':
            arg,i=group(i);out+='('+str(displayed(arg))+')'
        elif s[i]=='^':out+='**';i+=1
        elif s[i]=='\\':raise AssertionError('Unsupported displayed macro '+s[i:])
        else:out+=s[i];i+=1
    return parse_expr(out,local_dict={'x':x,'u':u,'DY':DY,'DU':DU,'UX':UX,'sqrt':sp.sqrt},transformations=TRANS)

@lru_cache(maxsize=50000)
def equal(a,b):
    # All learner derivatives operate where inner>0. Positive radical branches
    # justify force only after those domain constraints have been checked.
    if a==b:return True
    difference=sp.cancel(sp.powdenest(a,force=True)-sp.powdenest(b,force=True))
    if difference==0:return True
    if difference.is_zero is False:return False
    # Exact real witnesses disprove an identity without a costly simplification.
    for point in (25,-25,1,-1):
        witness=difference.subs(x,point)
        if witness.is_real is True and witness.is_finite is True and witness.is_zero is False:return False
    return sp.simplify(difference)==0
