"""Visible-expression reader reused from the earlier source validator (test only)."""
import re,sys
from functools import lru_cache
import sympy as s
try: import lark
except ImportError: sys.path.insert(0,'/home/jake/.cache/uv/wheels-v5/pypi/lark/1.2.2-py3-none-any')
from sympy.parsing.latex import parse_latex
from lark import Tree
X,Y,C,K=s.symbols('x y C K', real=True)
def norm(t):
    t=t.strip().replace('\u2061','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(r'\dfrac',r'\frac')
    # Lark otherwise reads sqrt(10) (x-h)^2 as an unsupported call.
    # Explicit multiplication preserves the displayed mathematical product.
    t=re.sub(r'(\\sqrt\{[^{}]+\})\s*(?=\()',r'\1*',t)
    t=re.sub(r'\\operatorname\{(ln|sin|cos|tan|cot|sec|arctan|arcsin)\}',lambda m:'\\'+m[1],t)
    t=re.sub(r'(?<=\))(?=\\(?:sqrt|sin|cos|tan|sec|ln|arcsin))','*',t)
    t=re.sub(r'(?<=[0-9xyz])(?=\\(?:sqrt|sin|cos|tan|sec|ln|arcsin))','*',t)
    t=t.replace(r'\operatorname{asin}',r'\arcsin').replace(r'\operatorname{atan}',r'\arctan')
    t=t.replace(r'{cos}',r'\cos').replace(r'{sec}',r'\sec').replace(r'\arctan',r'\arctan').replace(r'\pm','')
    t=re.sub(r'\\(cos|sec)\^\{([0-9]+)\}\s*(\([^()]*\)|[xytT])',lambda m:'\\'+m[1]+'('+m[3]+')^{'+m[2]+'}',t)
    t=re.sub(r'\\(sin|cos|tan|cot|sec|arctan|arcsin)\s*([xytT])',lambda m:'\\'+m[1]+'('+m[2]+')',t)
    matches=list(re.finditer(r'\\(?:sin|cos|tan|cot|sec|arctan|arcsin|ln)\(',t))
    for m in reversed(matches):
        depth=1;end=m.end()
        while depth:
            if t[end]=='(':depth+=1
            if t[end]==')':depth-=1
            end+=1
        t=t[:m.start()]+'{'+t[m.start():end]+'}'+t[end:]
    t=re.sub(r'(?<=\))\s*(?=e\^)','*',t)
    t=re.sub(r'(?<=\))(?=[A-Za-z{])','*',t)
    t=re.sub(r'(?<=\})(?=\{\\(?:sin|cos|tan|cot|sec|ln|arcsin))','*',t)
    t=re.sub(r'(?<=\})(?=[a-zA-Z])','*',t)
    t=re.sub(r'\\ln(\{\\cos\([^{}]*\)\})',lambda m:'{\\ln('+m[1]+')}',t)
    # Lark uses inverse-function names and can disambiguate exponential base e.
    return t.rstrip('.,')
@lru_cache(None)
def parse(t):
    try:z=parse_latex(norm(t) or '1',backend='lark')
    except Exception as exc:raise AssertionError(('display parse',t,norm(t))) from exc
    if isinstance(z,Tree):
        vals=[v for v in z.children if isinstance(v,s.Basic)]
        assert vals and all(s.simplify(vals[0]-v)==0 for v in vals),(t,z)
        z=vals[0]
    z=z.subs({a:{'e':s.E,'x':X,'t':X,'y':Y,'T':Y,'C':C,'K':K}.get(a.name,a) for a in z.free_symbols})
    return z.replace(lambda q:isinstance(q,s.Pow) and q.base==Y and q.exp.is_Rational and q.exp.q==3 and q.exp.p%2==0,lambda q:s.Abs(Y)**q.exp)
def equal(a,b):return s.simplify(s.trigsimp(a-b,method='fu'))==0
