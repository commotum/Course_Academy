from functools import lru_cache
import re,sympy as S
from sympy.parsing.latex import parse_latex
x,y,C,D=S.symbols("x y C D",positive=True)
@lru_cache(None)
def parse(s):
    s = s.replace(r'\mathrm{d}', r'\text{d}').replace(r'\left','').replace(r'\right','')
    s = s.strip().rstrip('.,').replace('\\pm', '').replace('\u2061', '').replace('\\dfrac', '\\frac')
    s = re.sub('\\\\frac\\{\\\\text\\{d\\}y\\}\\{\\\\text\\{d\\}x\\}|\\\\frac\\{dy\\}\\{dx\\}', 'D', s)
    v = parse_latex(s, strict=True)
    return v.xreplace({z: {'x': x, 'y': y, 'C': C, 'D': D, 'e': S.E}.get(str(z), z) for z in v.free_symbols})

@lru_cache(None)
def solve_check(prompt, values, h):
    eq = re.search('\\$\\$([\\s\\S]*?)\\$\\$', prompt)[1].strip().rstrip('.')
    l, r = eq.split('=')
    F = S.expand(parse(l) - parse(r))
    F = S.simplify(-F.subs(D, 0) / S.diff(F, D))
    F = S.expand(F.subs(x, x - h))
    terms = S.Add.make_args(F)
    exponents = {S.simplify(y * S.diff(t, y) / t) for t in terms}
    assert 1 in exponents and len(exponents) == 2, exponents
    n = next((e for e in exponents if e != 1))
    p = S.simplify(-sum((t / y for t in terms if S.simplify(y * S.diff(t, y) / t) == 1)))
    q = S.simplify(sum((t / y ** n for t in terms if S.simplify(y * S.diff(t, y) / t) == n)))
    result = []
    for text in values:
        Y = S.simplify(parse(text.split('=', 1)[1]).subs(x, x - h))
        z = S.powdenest(Y ** (1 - n), force=True)
        if n in (S.Rational(1, 2), S.Rational(3, 4), S.Rational(-1, 2)):
            z = z.replace(S.Abs, lambda v: v)
        z = S.simplify(z)
        res = linear_residual(z, p, q, n)
        result.append({'value': text, 'transformed_z': str(z), 'residual': str(res), 'is_solution': res == 0})
    return {'p': str(p), 'q': str(q), 'n': str(n), 'choices': result}

@lru_cache(None)
def linear_residual(z, p, q, n):
    return S.simplify(S.expand(S.diff(z, x) + (1 - n) * p * z - (1 - n) * q))