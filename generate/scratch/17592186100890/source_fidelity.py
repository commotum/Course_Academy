"""Strict source-value parser and full-bank comparison for this KP's grammar.

This reads the original rendered choices, independently of generator recipes.
Unsupported notation fails closed. It never squares radicals to compare them.
No database or learner-grader operations are performed here.
"""
import re
import sympy as sp

X, Y = sp.symbols('x y', real=True)


class MathParser:
    def __init__(self, text):
        text = text.replace('\\\\', '\\').replace(r'\left', '').replace(r'\right', '')
        self.tokens = []
        position = 0
        while position < len(text):
            if text[position].isspace():
                position += 1
                continue
            match = re.match(r'\\(?:frac|sqrt|pi)\b|[0-9]+|[xy{}()+\-*/^]', text[position:])
            if not match:
                raise ValueError(f'Unsupported source notation at {text[position:]!r}')
            self.tokens.append(match.group())
            position += len(match.group())
        self.index = 0

    def peek(self):
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def take(self, expected=None):
        value = self.peek()
        if value is None or expected is not None and value != expected:
            raise ValueError(f'Expected {expected!r}, got {value!r}')
        self.index += 1
        return value

    def expression(self):
        result = self.product()
        while self.peek() in ('+', '-'):
            operator = self.take()
            term = self.product()
            result = result + term if operator == '+' else result - term
        return result

    def product(self):
        result = self.unary()
        while True:
            token = self.peek()
            if token in ('*', '/'):
                operator = self.take()
                term = self.unary()
                result = result * term if operator == '*' else result / term
            elif token is not None and (token.isdigit() or token in ('x','y','{','(',r'\frac',r'\sqrt',r'\pi')):
                result *= self.unary()
            else:
                return result

    def unary(self):
        if self.peek() in ('+', '-'):
            operator = self.take()
            result = self.unary()
            return result if operator == '+' else -result
        result = self.atom()
        if self.peek() == '^':
            self.take('^')
            result **= self.unary()
        return result

    def group(self):
        opening = self.take()
        if opening not in ('{', '('):
            raise ValueError('Expected a grouped expression')
        result = self.expression()
        self.take('}' if opening == '{' else ')')
        return result

    def atom(self):
        token = self.peek()
        if token in ('{', '('):
            return self.group()
        token = self.take()
        if token.isdigit():
            return sp.Integer(token)
        if token in ('x', 'y'):
            return X if token == 'x' else Y
        if token == r'\pi':
            return sp.pi
        if token == r'\frac':
            numerator = self.group()
            denominator = self.group()
            return numerator / denominator
        if token == r'\sqrt':
            return sp.sqrt(self.group())
        raise ValueError(f'Unsupported atom: {token}')


def expression(text):
    parser = MathParser(text)
    value = parser.expression()
    if parser.peek() is not None:
        raise ValueError('Unconsumed source notation')
    return value


def equation(text):
    sides = text.split('=')
    if len(sides) != 2:
        raise ValueError('Expected one complete equation')
    return tuple(expression(side) for side in sides)


def equivalent_equations(a, b):
    """Compare residuals up to a nonzero constant, preserving radical branches.

    All comparisons use the same captured question domain. Rational options in
    this source bank only have possible poles at x=0, excluded by its prompts.
    Do not broaden this checker to other domains without checking their poles.
    """
    left, right = a[0]-a[1], b[0]-b[1]
    if sp.simplify(left-right) == 0:
        return True
    if left == 0 or right == 0:
        return False
    multiplier = sp.cancel(left/right)
    return not multiplier.free_symbols and multiplier.is_zero is False


def match_bank(source_options, generated_options, is_equation=True):
    """One-to-one matching of displayed values AND their correct designations."""
    parse = equation if is_equation else expression
    compare = equivalent_equations if is_equation else lambda a,b: sp.simplify(a-b) == 0
    original = [parse(item['value']) for item in source_options]
    generated = [parse(item['value']) for item in generated_options]
    unused = set(range(len(generated)))
    matches, missing = [], []
    for i, value in enumerate(original):
        candidates = [j for j in sorted(unused)
                      if source_options[i]['correct'] == generated_options[j]['correct'] and compare(value,generated[j])]
        if len(candidates) == 1:
            j = candidates[0]
            unused.remove(j)
            matches.append({'source_index':i,'generated_index':j})
        else:
            missing.append({'source_index':i,'value':source_options[i]['value'],'matches':candidates})
    return {'passed':not missing and not unused and len(original)==len(generated),
            'matches':matches,'missing':missing,
            'extra':[{'generated_index':j,'value':generated_options[j]['value']} for j in sorted(unused)]}
