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
                j = t.index('|', i+1);out += 'Abs('+convert(t[i+1:j])+')';i = j+1
            else: out += t[i];i += 1
        return out
    t = convert(t).replace('{','(').replace('}',')').replace('^','**')
    t = re.sub(r'(asin|atan|asec|acos)([xu])', r'\1(\2)', t)
    assert '\\' not in t, t
    return parse_expr(t, local_dict={'x':X,'u':U,'C':C,'pi':sp.pi,'asin':sp.asin,'atan':sp.atan,'asec':sp.asec,'acos':sp.acos,'sqrt':sp.sqrt,'Abs':sp.Abs},
                      transformations=standard_transformations+(implicit_multiplication_application,rationalize))


def integral(t):
    start = t.index(r'\int');prefix = t[:start].strip();i = start+4;lo = hi = None
    if t[i:i+1] == '_':
        lo, i = group(t, i+1);assert t[i] == '^';hi, i = group(t, i+1);lo, hi = scalar(lo), scalar(hi)
    m = re.search(r'\\(?:mathrm|text|textrm)\{d\}([xu])', t[i:]);assert m, t
    body = t[i:i+m.start()];var = {'x':X,'u':U}[m[1]]
    return (scalar(prefix) if prefix else 1)*scalar(body), var, lo, hi


def source_prompt(t):
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


def primitive(body, family):
    # Read coefficients from the printed integrand, independent of parameters.
    if family == 'sine':
        poly = sp.Poly(sp.cancel(1/body**2), X);a = poly.nth(0);b = -poly.nth(2)
        assert poly.degree() == 2 and a > 0 and b > 0
        s = sp.sqrt(b/a);return sp.asin(s*X)/sp.sqrt(b), s
    if family == 'tangent':
        poly = sp.Poly(sp.cancel(1/body), X);a = poly.nth(0);b = poly.nth(2)
        assert poly.degree() == 2 and a > 0 and b > 0
        s = sp.sqrt(b/a);return sp.atan(s*X)/sp.sqrt(a*b), s
    poly = sp.Poly(sp.cancel(1/(body*sp.Abs(X))**2), X);a = -poly.nth(0);b = poly.nth(2)
    assert poly.degree() == 2 and a > 0 and b > 0
    s = sp.sqrt(b/a);return sp.asec(s*X)/sp.sqrt(a), s


def equivalent(a, b, family, slope):
    if sp.simplify(a-b) == 0: return True
    if family != 'secant': return False
    for sign in (1, -1):
        for point in (sp.Rational(3,2), sp.Integer(2), sp.Integer(3)):
            delta = (a-b).subs(X, sign*point/slope)
            if abs(complex(sp.N(delta, 30))) > 1e-20: return False
    return True


def expression(t):
    t = t.strip().rstrip('.')
    if '[' in t:
        prefix, rest = t.split('[',1);inner, tail = rest.split(']',1)
        assert tail[0] == '_';lo,i = group(tail,1);assert tail[i] == '^';hi,end = group(tail,i+1)
        value = scalar(inner);return (scalar(prefix) if prefix else 1)*(value.subs(U,scalar(hi))-value.subs(U,scalar(lo)))
    return scalar(t)


def check(record, family):
    q = record['question'];blocks = re.findall(r'\$\$\s*(.*?)\s*\$\$', q[':question/problem'], re.S)
    body, var, lo, hi = integral(blocks[0]);assert var == X
    prim, s = primitive(body,family);answer = prim if lo is None else sp.simplify(prim.subs(X,hi)-prim.subs(X,lo))
    if lo is not None:
        assert lo < hi
        if family == 'sine': assert -1 < s*lo < s*hi < 1
    sol = q[':question/worked-solution'];arg = scalar(re.search(r'substitution \$u=(.*?)\.\$',sol)[1]);assert sp.simplify(arg-s*X) == 0
    equalities = 0
    for block in re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S):
        if r'\frac{\mathrm{d}u}' in block:
            derivative, dx = block.split(r',\qquad');assert scalar(derivative.split('=')[1]) == s
            assert sp.simplify(scalar(dx.split('=')[1].split(r'\mathrm{d}u')[0])*s-1) == 0;equalities += 2;continue
        if r'\Longrightarrow' in block:
            for row, endpoint in zip(block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'), (lo,hi)):
                left,right = row.split(r'\Longrightarrow');assert scalar(left.split('=')[1].replace('&','')) == endpoint
                first,last = right.split('u=')[1].split('=');assert sp.simplify(scalar(first)-s*endpoint) == 0
                assert sp.simplify(scalar(last)-s*endpoint) == 0;equalities += 3
            continue
        if r'\qquad' in block and '|u|' in block:
            for equation in block.split(r',\qquad'):
                sides = [scalar(v).subs(U,arg) for v in equation.split('=')]
                for a,b in zip(sides,sides[1:]): assert equivalent(a,b,family,s);equalities += 1
            continue
        if r'\begin{aligned}' not in block:
            left,right = block.split('=',1)
            if r'\int' in left:
                f,v,l,h = integral(left);assert equivalent(sp.diff(scalar(right),U).subs(U,X), f.subs(U,X), family, 1)
            else: assert sp.simplify(scalar(left)-scalar(right)) == 0
            equalities += 1;continue
        rows = block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
        for part in [term.strip() for row in rows for term in row.replace('&','').split('=') if term.strip()]:
            if r'\int' in part:
                f,v,l,h = integral(part)
                if v == U:
                    f = f.subs(U,arg)*s
                    if l is not None: assert sp.simplify(l-s*lo) == 0 and sp.simplify(h-s*hi) == 0
                else: assert l == lo and h == hi
                assert equivalent(f,body,family,s), (part,f,body)
            else:
                value = expression(part).subs(U,arg)
                if lo is None: assert equivalent(sp.diff(value,X),body,family,s), (part,value,body)
                else: assert sp.simplify(value-answer) == 0, (part,value,answer)
            equalities += 1
    for f in q[':question/answer-fields']:
        correct = f[':answer-field/correct'][1];values = [];matches = []
        for a in f[':answer-field/choices']:
            value = scalar(a[':answer/value']);values.append(value)
            expected = answer
            if f[':answer-field/key'] == 'argument': expected = s*hi
            if f[':answer-field/key'] == 'coefficient':
                expected = sp.simplify(answer/sp.atan(s*hi))
            yes = equivalent(sp.diff(value,X),body,family,s) if lo is None else sp.simplify(value-expected) == 0
            if yes: matches.append(a[':answer/id'])
        assert matches == [correct], (q[':question/id'],f,answer,matches)
        if f[':answer-field/type'].endswith('/radio'):
            for i in range(5):
                for j in range(i):
                    assert not equivalent(sp.diff(values[i]-values[j],X),0,family,s) if lo is None else sp.simplify(values[i]-values[j]) != 0
    return {'equalities':equalities,'answer':answer,'body':body,'lower':lo,'upper':hi,'slope':s}
