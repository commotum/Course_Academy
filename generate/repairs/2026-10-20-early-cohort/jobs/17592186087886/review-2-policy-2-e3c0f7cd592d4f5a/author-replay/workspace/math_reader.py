"""Small strict reader for the displayed scalar ODE expressions in this package."""
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
x, y, v, Z = sp.symbols('x y v Z')
D = r'\frac{\text{d}v}{\text{d}x}'
DY = r'\frac{\text{d}y}{\text{d}x}'

def expression(text):
    text = text.replace(D, 'Z').replace(DY, 'Z').replace('\u2061', '')
    text = text.replace(r'\left', '').replace(r'\right', '').replace(r'\,', '')
    text = re.sub(r'\\(?:operatorname|mathrm)\{(sin|cos|tan|sec)\}', r'\1 ', text)
    text = re.sub(r'\\(sin|cos|tan|sec)\b', r'\1 ', text)
    text = text.replace(r'\cdot', '*').replace(r'\times', '*')
    def convert(start, closing=None):
        out = ''; i = start
        while i < len(text):
            c = text[i]
            if closing and c == closing:
                return out, i + 1
            if text.startswith(r'\frac', i):
                i += 5
                assert text[i] == '{', text
                a, i = convert(i + 1, '}')
                assert text[i] == '{', text
                b, i = convert(i + 1, '}')
                out += '((' + a + ')/(' + b + '))'
            elif text.startswith(r'\cancel', i):
                i += 7
                assert text[i] == '{'
                a, i = convert(i + 1, '}'); out += '(' + a + ')'
            elif c in '{(':
                a, i = convert(i + 1, '}' if c == '{' else ')'); out += '(' + a + ')'
            elif c == '^': out += '**'; i += 1
            elif c in '}\\': raise ValueError('Unsupported displayed notation: ' + text[i:])
            else: out += c; i += 1
        assert closing is None, text
        return out, i
    raw, _ = convert(0)
    assert re.fullmatch(r'[A-Za-z0-9+*/().\s-]+', raw), raw
    return parse_expr(raw, local_dict={'x':x, 'y':y, 'v':v, 'Z':Z, 'e':sp.E,
        'sin':sp.sin, 'cos':sp.cos, 'tan':sp.tan, 'sec':sp.sec},
        transformations=standard_transformations + (implicit_multiplication_application,))

def rate(equation):
    left, right = equation.strip().rstrip('.').split('=')
    residual = expression(left) - expression(right)
    assert sp.diff(residual, Z, 2) == 0 and sp.diff(residual, Z) != 0
    return sp.cancel(-residual.subs(Z, 0) / sp.diff(residual, Z))

def prompt_rhs(text):
    formula = text.split('$$')[1].strip().rstrip('.')
    left, right = formula.split('=')
    assert left.strip() == DY
    return expression(right)

def fingerprint(text):
    return sp.srepr(sp.cancel(prompt_rhs(text).subs(y, v*x)))
