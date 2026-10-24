"""Independent reader/checker of printed questions, bounds, solutions and banks."""
import hashlib
import json
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, rationalize

X, U, C = sp.symbols('x u C', real=True)


def group(t, i):
    while i < len(t) and t[i].isspace(): i += 1
    if t[i] != '{': return t[i], i+1
    depth = 1;j = i+1
    while depth:
        depth += (t[j] == '{')-(t[j] == '}');j += 1
    return t[i+1:j-1], j


def scalar(t):
    t = t.replace(r'\,', '').strip().rstrip('.,').replace('⁡', '').replace(r'\left', '').replace(r'\right', '').replace(r'\cdot', '*').replace(r'\pi', 'pi')
    t = re.sub(r'\\(?:operatorname|text|textrm)\{(arcsin|arctan|arcsec|arccos|asin|atan|asec)\}', lambda m: {'arcsin':'asin','arctan':'atan','arcsec':'asec','arccos':'acos'}.get(m[1], m[1]), t)
    t = t.replace(r'\arcsin', 'asin').replace(r'\arctan', 'atan')
    def convert(t):
        out = '';i = 0
        while i < len(t):
            m = re.match(r'\\(d?frac|sqrt)', t[i:])
            if m:
                name = m[1];a, j = group(t, i+len(m[0]))
                if name == 'sqrt': out += 'sqrt('+convert(a)+')'
                else:
                    b, j = group(t, j);out += '(('+convert(a)+')/('+convert(b)+'))'
                i = j
            elif t[i] == '|':
                j = t.index('|', i+1);out += '(Abs('+convert(t[i+1:j])+'))';i = j+1
            else: out += t[i];i += 1
        return out
    t = t.replace(r'\ln', 'log').replace(r'\exp', 'exp')
    t = convert(t).replace('{','(').replace('}',')').replace('^','**')
    t = re.sub(r'(asin|atan|asec|acos)([xu])', r'\1(\2)', t)
    assert '\\' not in t, t
    return parse_expr(t, local_dict={'x':X,'u':U,'C':C,'pi':sp.pi,'asin':sp.asin,'atan':sp.atan,'asec':sp.asec,'acos':sp.acos,'sqrt':sp.sqrt,'Abs':sp.Abs,'log':sp.log,'exp':sp.exp,'e':sp.E},
                      transformations=standard_transformations+(implicit_multiplication_application,rationalize))


def integral(t):
    start = t.index(r'\int');prefix = t[:start].strip().rstrip('(').strip();i = start+4;lo = hi = None
    if t[i:i+1] == '_':
        lo, i = group(t, i+1);assert t[i] == '^';hi, i = group(t, i+1);lo, hi = scalar(lo), scalar(hi)
    m = re.search(r'\\(?:mathrm|text|textrm)\{d\}([xu])', t[i:]);assert m, t
    body = t[i:i+m.start()];var = {'x':X,'u':U}[m[1]]
    return (scalar(prefix) if prefix else 1)*scalar(body), var, lo, hi


def source_prompt(t):
    t = t.replace('dx',r'\mathrm{d}x').replace(r'\operatorname{ln}',r'\ln').replace(r'\operatorname{ln}⁡',r'\ln')
    t = t.replace(r'\displaystyle', '').replace(r'{\int }', r'\int').replace('⁡','')
    t = re.sub(r'\\(?:mathrm|text|textrm)\s*\{?\s*d\s*\}?\s*x', 'DIFFERENTIAL', t)
    start = t.index(r'\int');t = t[start:].split('$')[0].split('=')[0].strip().rstrip('.')
    i = 4;lo = hi = None
    if t[i:i+1] == '_':
        lo, i = group(t, i+1);assert t[i] == '^';hi, i = group(t, i+1);lo, hi = scalar(lo), scalar(hi)
    t = t[i:];assert 'DIFFERENTIAL' in t, t
    # A source may put dx in its numerator instead of after the fraction.
    t = t.replace('DIFFERENTIAL', '1' if r'\frac{DIFFERENTIAL}' in t or r'\dfrac{DIFFERENTIAL}' in t else '').replace(r'\,','').strip().rstrip('.,?').strip()
    while t.count('}') > t.count('{') and t.endswith('}'): t = t[:-1].strip()
    return sp.simplify(scalar(t)), lo, hi


def key(body, lo=None, hi=None):
    return hashlib.sha256(json.dumps([sp.srepr(sp.simplify(body)), None if lo is None else sp.srepr(sp.simplify(lo)),
                                     None if hi is None else sp.srepr(sp.simplify(hi))], sort_keys=True, separators=(',', ':')).encode()).hexdigest()


