"""Structural identities for common displayed math notation, without algebra."""
import re
from fractions import Fraction


# Use the same symbol spellings as the live MathML extractor. ASCII letters
# remain letters: the variable product pi must never turn into the symbol π.
SYMBOLS = dict(zip('αβγδθλμρσωπ∞±∓≤≥≠→∈∉∪∩∫∑∏×⋅·÷',
    ('alpha beta gamma delta theta lambda mu rho sigma omega pi infty pm mp '
     'leq geq neq rightarrow in notin cup cap int sum prod times cdot cdot div').split()))
ALIASES = {'dfrac':'frac', 'tfrac':'frac', 'le':'leq', 'ge':'geq', 'ne':'neq',
           'to':'rightarrow'}
LAYOUT = {'displaystyle','textstyle','scriptstyle','scriptscriptstyle','left','right',
          'big','Big','bigg','Bigg','bigl','bigr','Bigl','Bigr','biggl','biggr',
          'Biggl','Biggr','quad','qquad','enspace','thinspace'}
OPERATORS = {'sin','cos','tan','sec','csc','cot','sinh','cosh','tanh','ln','log',
             'exp','arcsin','arccos','arctan','arg','lim','min','max'}
SUPERSCRIPTS = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻', '0123456789+-')
SUBSCRIPTS = str.maketrans('₀₁₂₃₄₅₆₇₈₉₊₋', '0123456789+-')
UNITS = ('ft','in','yd','mi','mm','cm','km','m','kg','mg','lb','oz','g','ms','min','hr','s','h')


def quantity_identity(value):
    """Reconcile legacy numeric unit suffixes with explicitly typeset units."""
    unit = '(?:'+'|'.join(UNITS)+')'
    styled = r'\\(?:text|mathrm)\{\s*'+unit+r'\s*\}'
    block = '(?:'+unit+'|'+styled+r'|\{'+styled+r'\})'
    match = re.fullmatch(r'([+-]?(?:\d+(?:\.\d*)?|\.\d+))\s*'
                        r'(?:(?:\\[,; ]|\\quad)\s*)*('+block+r')'
                        r'\s*(?:\^\{([+-]?\d+)\}|\^([+-]?\d)|([²³]))?',
                        value.strip().strip('$').replace('−','-'))
    if not match:
        return None
    name = re.sub(r'\\(?:text|mathrm)|[{}\s]', '', match[2])
    exponent = match[3] or match[4] or (match[5].translate(SUPERSCRIPTS) if match[5] else '1')
    return ('quantity',tokens(match[1]),name,exponent)


def tokens(value):
    value = value.strip().strip('$').replace('−','-')
    value = re.sub('[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+', lambda m:'^{'+m[0].translate(SUPERSCRIPTS)+'}', value)
    value = re.sub('[₀₁₂₃₄₅₆₇₈₉₊₋]+', lambda m:'_{'+m[0].translate(SUBSCRIPTS)+'}', value)
    result = []
    literal_depth, pending_literal = 0, False
    for match in re.finditer(r'\\[A-Za-z]+|\\.|[\s\S]', value):
        token = match[0]
        if token == r'\text':
            pending_literal = True
        elif token == '{':
            if pending_literal or literal_depth:
                literal_depth += 1
            pending_literal = False
        elif token == '}' and literal_depth:
            literal_depth -= 1
        if token in SYMBOLS:
            token = '\\' + SYMBOLS[token]
        if token.startswith('\\'):
            name = token[1:]
            if name in LAYOUT or name in (',',';','!',':',' '):
                continue
            token = '|' if name in ('mid','vert','lvert','rvert') else '\\' + ALIASES.get(name,name)
        elif token.isspace() and not literal_depth:
            continue
        result.append(token)
    return tuple(result)


def sequence_identity(nodes):
    nodes = tuple(nodes)
    # Legacy lim_(...) and MathML {lim}_{...} identify a limit only
    # when the subscript contains an explicit approach arrow.
    normalized = []
    for node in nodes:
        if node[0] == 'script' and node[2]:
            subscript = node[2]
            if (len(subscript) == 1 and subscript[0][0] == 'fence' and
                subscript[0][1] == '(' and subscript[0][3] == ')'):
                subscript = subscript[0][2]
            if ('command','rightarrow') in subscript:
                base = node[1]
                if base == ('group', (('char','l'),('char','i'),('char','m'))):
                    node = ('script',('operator','lim'),subscript,node[3])
                elif (base == ('char','m') and
                      normalized[-2:] == [('char','l'),('char','i')]):
                    del normalized[-2:]
                    node = ('script',('operator','lim'),subscript,node[3])
                elif base == ('operator','lim'):
                    node = ('script',base,subscript,node[3])
        normalized.append(node)
    nodes = tuple(normalized)
    # A whole quotient whose two arguments are explicitly fenced has the same
    # scope as a stacked fraction. Leave unfenced slash expressions untouched.
    if (len(nodes) == 3 and nodes[1] == ('char','/') and
        all(n[0] == 'fence' and n[1] == '(' and n[3] == ')' for n in (nodes[0],nodes[2]))):
        return (('frac',fraction_argument((nodes[0],)),fraction_argument((nodes[2],))),)
    # Convert only a whole numeric ratio, including one used as an exponent.
    # Do not change x^1/3, 1/(3x), or a fraction's argument boundaries.
    if all(n[0] == 'char' for n in nodes):
        ratio = re.fullmatch(r'([+-]?\d+)/([+-]?\d+)', ''.join(n[1] for n in nodes))
        if ratio:
            return (('frac', tuple(('char',c) for c in re.findall(r'[+-]|\d+',ratio[1])),
                     tuple(('char',c) for c in re.findall(r'[+-]|\d+',ratio[2]))),)
    # MathQuill places a numerator's leading minus outside a whole fraction.
    # Move it only for a product, never across a sum or an exponent on the
    # fraction itself. Argument boundaries and function inputs stay intact.
    if len(nodes) == 1 and nodes[0][0] == 'frac':
        numerator, denominator = nodes[0][1:]
        factors = numerator[1:]
        if (numerator[:1] == (('char','-'),) and factors and all(
                (n[0] == 'char' and re.fullmatch(r'[A-Za-z0-9.]+',n[1])) or
                n[0] in ('script','root','frac','fence','group','operator','operatorname')
                for n in factors)):
            return (('char','-'),('frac',factors,denominator))
    return nodes


def fraction_argument(nodes):
    # Fraction braces already group the entire numerator/denominator. Fencing
    # that whole argument adds no scope; fences around only part still matter.
    while len(nodes) == 1 and nodes[0][0] == 'fence' and nodes[0][1] == '(' and nodes[0][3] == ')':
        nodes = nodes[0][2]
    return nodes


def scalar_identity(nodes):
    """Exact numeric literals only; no symbolic algebra or rounding tolerance."""
    def number(parts):
        if not all(n[0] == 'char' for n in parts):
            return None
        value = ''.join(n[1] for n in parts)
        return Fraction(value) if re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)', value) else None
    value = number(nodes)
    if value is None:
        sign = 1
        if len(nodes) == 2 and nodes[0] in (('char','-'),('char','+')):
            sign = -1 if nodes[0][1] == '-' else 1
            nodes = nodes[1:]
        if len(nodes) != 1 or nodes[0][0] != 'frac':
            return None
        numerator, denominator = number(nodes[0][1]), number(nodes[0][2])
        if numerator is None or denominator is None or not denominator:
            return None
        value = sign * numerator / denominator
    return ('number',value.numerator,value.denominator)


class Parser:
    def __init__(self, source):
        self.source, self.position = source, 0

    def take(self):
        if self.position == len(self.source):
            raise ValueError('Incomplete mathematical notation')
        token = self.source[self.position]
        self.position += 1
        return token

    def argument(self):
        if self.position < len(self.source) and self.source[self.position] == '{':
            self.position += 1
            return self.sequence('}')
        # An unbraced TeX argument consumes one token: x^23 means x^2 then 3,
        # and \frac12 has separate numerator and denominator arguments.
        return (self.atom(combine_digits=False),)

    def sequence(self, closing=None):
        nodes = []
        while self.position < len(self.source):
            token = self.source[self.position]
            # Older MathML captures put the closing glyph of a scripted fence
            # in a TeX group: (x+1{)}^2. It still closes the displayed fence.
            if closing in (')', ']', r'\}') and self.source[self.position:self.position+3] == ('{', closing, '}'):
                self.position += 3
                return sequence_identity(nodes)
            if token == closing:
                self.position += 1
                return sequence_identity(nodes)
            if token == '}':
                raise ValueError('Unexpected closing group')
            if token in ('^','_') and nodes:
                self.position += 1
                argument = self.argument()
                base = nodes.pop()
                slot = 2 if token == '_' else 3
                if base[0] == 'script' and not base[slot]:
                    parts = list(base)
                else:
                    parts = ['script',base,(),()]
                parts[slot] = argument
                nodes.append(tuple(parts))
            elif token == '⁡':
                self.position += 1
                # MathML places a function's application marker AFTER its
                # exponent: {sec}^{2}⁡(x). It marks the scripted name, not the
                # preceding variable factors. Plain sec^2 without this local
                # evidence remains a product of variables.
                if nodes and nodes[-1][0] == 'script':
                    base = nodes[-1][1]
                    parts = base[1] if base[0] == 'group' else (base,)
                    if all(n[0] == 'char' and n[1].isalpha() for n in parts):
                        name = ''.join(n[1] for n in parts)
                        if name in OPERATORS:
                            nodes[-1] = ('script',('operator',name),*nodes[-1][2:])
                            continue
                    if base[0] in ('operator','operatorname'):
                        continue
                if nodes and nodes[-1][0] in ('operator', 'operatorname'):
                    # Explicitly serialized MathML function names already carry
                    # the application boundary; do not append a second marker.
                    continue
                start = len(nodes)
                while start and nodes[start-1][0] == 'char' and nodes[start-1][1].isalpha():
                    start -= 1
                name = ''.join(n[1] for n in nodes[start:])
                if name in OPERATORS:
                    nodes[start:] = [('operator',name)]
                else:
                    nodes.append(('apply',))
            else:
                nodes.append(self.atom())
        if closing is not None:
            raise ValueError('Unclosed mathematical group')
        return sequence_identity(nodes)

    def atom(self, combine_digits=True):
        token = self.take()
        if token.isascii() and token.isdigit():
            # A displayed multi-digit base is one numeric atom: 11^{x} and
            # {11}^{x} must attach the exponent to the same complete number.
            while combine_digits and self.position < len(self.source) and self.source[self.position].isascii() and self.source[self.position].isdigit():
                token += self.take()
            return ('char',token)
        if token == '{':
            content = self.sequence('}')
            return content[0] if len(content) == 1 else ('group',content)
        if token in ('(', '[', r'\{'):
            end = {'(':')','[':']',r'\{':r'\}'}[token]
            return ('fence',token,self.sequence(end),end)
        if token == r'\frac':
            numerator = fraction_argument(self.argument())
            denominator = fraction_argument(self.argument())
            return ('frac',numerator,denominator)
        if token == r'\sqrt':
            index = ()
            if self.position < len(self.source) and self.source[self.position] == '[':
                self.position += 1
                index = self.sequence(']')
            return ('root',index,self.argument())
        if token == r'\operatorname':
            argument = self.argument()
            if all(n[0] == 'char' for n in argument):
                name = ''.join(n[1] for n in argument)
                if name in OPERATORS:
                    return ('operator',name)
            return ('operatorname',argument)
        if token in (r'\mathrm',r'\mathit',r'\text'):
            argument = self.argument()
            if len(argument) == 1 and argument[0][0] == 'char' and argument[0][1].isalnum():
                return argument[0]
            return ('styled',token,argument)
        if token[0] == '\\':
            name = token[1:]
            return ('operator',name) if name in OPERATORS else ('command',name)
        return ('char',token)


def identity(value):
    # Whole Roman-numeral graph labels have been imported both bare and as
    # typeset text. Do not strip styling or spaces from arbitrary text.
    label = re.fullmatch(r'\\(?:text|mathrm)\{([IVXLCDM]+)\}', value.strip().strip('$'))
    if label:
        value = label[1]
    quantity = quantity_identity(value)
    if quantity is not None:
        return repr(quantity)
    source = tokens(value)
    try:
        nodes = Parser(source).sequence()
        return repr(scalar_identity(nodes) or ('math',nodes))
    except ValueError:
        # Unsupported/unbalanced notation still has a stable token identity.
        # It cannot collide with a successfully parsed expression.
        return repr(('tokens',source))
